"""Registre Prometheus à cardinalité bornée introduit en campagne 12."""

import threading

from configuration import Settings
from state import is_ready
from version import REVISION, VERSION


def escape_label_value(value: str) -> str:
    """Protège le format texte contre guillemets, antislashs et retours ligne."""

    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


class Metrics:
    """Petit registre autonome adapté au laboratoire, pas un client complet."""

    buckets = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.in_flight = 0
        self.requests: dict[tuple[str, str], int] = {}
        self.duration_count: dict[str, int] = {}
        self.duration_sum: dict[str, float] = {}
        self.duration_buckets: dict[str, list[int]] = {}

    def start_request(self) -> None:
        with self.lock:
            self.in_flight += 1

    def finish_request(self, route: str, code: int, duration: float) -> None:
        """Enregistre uniquement route normalisée et code, jamais URL ou utilisateur."""

        with self.lock:
            self.in_flight -= 1
            key = (route, str(code))
            self.requests[key] = self.requests.get(key, 0) + 1
            self.duration_count[route] = self.duration_count.get(route, 0) + 1
            self.duration_sum[route] = self.duration_sum.get(route, 0.0) + duration
            counts = self.duration_buckets.setdefault(route, [0] * len(self.buckets))
            for index, boundary in enumerate(self.buckets):
                if duration <= boundary:
                    counts[index] += 1

    def render(self, settings: Settings) -> str:
        """Produit le format d'exposition texte compris par Prometheus."""

        with self.lock:
            lines = [
                "# HELP sentinel_build_info Information de construction de Sentinel.",
                "# TYPE sentinel_build_info gauge",
                "sentinel_build_info{"
                f'version="{escape_label_value(VERSION)}",'
                f'revision="{escape_label_value(REVISION)}"'
                "} 1",
                "# HELP sentinel_http_requests_total Requêtes HTTP terminées.",
                "# TYPE sentinel_http_requests_total counter",
            ]
            for (route, code), value in sorted(self.requests.items()):
                lines.append(
                    f'sentinel_http_requests_total{{method="GET",route="{route}",code="{code}"}} {value}'
                )
            lines.extend([
                "# HELP sentinel_http_requests_in_flight Requêtes HTTP en cours.",
                "# TYPE sentinel_http_requests_in_flight gauge",
                f"sentinel_http_requests_in_flight {self.in_flight}",
                "# HELP sentinel_http_request_duration_seconds Durée des requêtes HTTP.",
                "# TYPE sentinel_http_request_duration_seconds histogram",
            ])
            for route in sorted(self.duration_count):
                for boundary, value in zip(self.buckets, self.duration_buckets[route]):
                    lines.append(
                        f'sentinel_http_request_duration_seconds_bucket{{route="{route}",le="{boundary}"}} {value}'
                    )
                count = self.duration_count[route]
                lines.extend([
                    f'sentinel_http_request_duration_seconds_bucket{{route="{route}",le="+Inf"}} {count}',
                    f'sentinel_http_request_duration_seconds_sum{{route="{route}"}} {self.duration_sum[route]:.9f}',
                    f'sentinel_http_request_duration_seconds_count{{route="{route}"}} {count}',
                ])

            dependency_up = 1 if is_ready(settings) else 0
            last_success = settings.state_file.stat().st_mtime if settings.state_file.exists() else 0
            lines.extend([
                "# HELP sentinel_dependency_up État des dépendances bornées.",
                "# TYPE sentinel_dependency_up gauge",
                f'sentinel_dependency_up{{name="state"}} {dependency_up}',
                "# HELP sentinel_last_success_unixtime Date du dernier diagnostic réussi.",
                "# TYPE sentinel_last_success_unixtime gauge",
                f"sentinel_last_success_unixtime {last_success:.6f}",
            ])
            return "\n".join(lines) + "\n"
