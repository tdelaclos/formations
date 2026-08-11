from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "sentinel" / "docs"
CHAPTER = re.compile(r"^\d+\.\d+-.*\.md$")
INFOGRAPHIC = re.compile(
    r"\n## Infographie de révision\s*\n.*?(?=\n## |\Z)",
    re.S,
)
MERMAID = re.compile(r"```mermaid\n(.*?)```", re.S)
H2 = re.compile(r"^## (.+)$", re.M)
NUMBER = re.compile(r"^# Chapitre (\d+\.\d+)\b", re.M)


def normalize_opening(text: str) -> str:
    """Normalise uniquement les blancs du cartouche, sans réécrire le contenu."""
    marker = "\n## Vous êtes ici\n"
    if marker not in text:
        return text
    prefix, rest = text.split(marker, 1)
    lines = prefix.splitlines()
    if not lines:
        return text

    # Conserver les lignes de contenu, mais réduire les blancs successifs.
    compact: list[str] = []
    blank = False
    for line in lines:
        if not line.strip():
            if compact and not blank:
                compact.append("")
            blank = True
        else:
            compact.append(line.rstrip())
            blank = False
    while compact and compact[-1] == "":
        compact.pop()

    # Le formalisme commun sépare le H1, le cartouche de campagne et la citation.
    rebuilt: list[str] = []
    for line in compact:
        if rebuilt and line.startswith("> ") and rebuilt[-1] != "" and not rebuilt[-1].startswith(">"):
            rebuilt.append("")
        elif rebuilt and line.startswith("> *") and rebuilt[-1].startswith("> **"):
            rebuilt.append("")
        rebuilt.append(line)

    return "\n".join(rebuilt) + marker + rest


def diagram_type(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("%%"):
            continue
        return line.split()[0]
    return "unknown"


def simple_flowchart(body: str) -> bool:
    lines = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.strip().startswith("%%")]
    if not lines or not lines[0].startswith(("flowchart", "graph")):
        return False
    edges = sum("-->" in ln or "-." in ln or "==>" in ln for ln in lines[1:])
    # Heuristique volontairement conservative : signaler, ne pas supprimer.
    return edges <= 1 and len(lines) <= 5


def main() -> None:
    report: list[str] = [
        "# Audit Mermaid et structure des chapitres",
        "",
        "Ce rapport est généré temporairement pour la passe d'harmonisation.",
        "Les diagrammes simples sont signalés pour revue humaine mais ne sont pas supprimés automatiquement.",
        "",
    ]
    total = 0
    with_infographic = 0
    with_image = 0
    simple = 0
    structural_issues: list[str] = []

    for path in sorted(DOCS.glob("campagne_*/*.md")):
        if not CHAPTER.match(path.name):
            continue
        total += 1
        text = path.read_text(encoding="utf-8")
        match = NUMBER.search(text)
        if not match:
            structural_issues.append(f"- `{path.relative_to(ROOT)}` : numéro de chapitre introuvable dans le H1")
            continue
        number = match.group(1)

        image = path.parent / "media" / f"recap-{number}.png"
        had_infographic = bool(INFOGRAPHIC.search(text))
        if had_infographic:
            with_infographic += 1
        replacement = ""
        if image.exists():
            with_image += 1
            replacement = (
                f"\n## Schéma récapitulatif\n\n"
                f"![Récapitulatif visuel du chapitre {number}](media/recap-{number}.png)\n"
            )
        text = INFOGRAPHIC.sub(replacement, text)
        text = normalize_opening(text)
        path.write_text(text, encoding="utf-8")

        h2s = H2.findall(text)
        expected = ["Vous êtes ici", "Objectifs pédagogiques", "Pourquoi ce chapitre existe"]
        if h2s[:3] != expected:
            structural_issues.append(
                f"- `{path.relative_to(ROOT)}` : premiers H2 = {h2s[:3]!r}"
            )

        diagrams = list(MERMAID.finditer(text))
        types: dict[str, int] = {}
        simple_here: list[str] = []
        for d in diagrams:
            body = d.group(1)
            dtype = diagram_type(body)
            types[dtype] = types.get(dtype, 0) + 1
            if simple_flowchart(body):
                simple += 1
                before = text[: d.start()]
                headings = H2.findall(before)
                context = headings[-1] if headings else "début de chapitre"
                simple_here.append(context)
        type_summary = ", ".join(f"{k}: {v}" for k, v in sorted(types.items())) or "aucun"
        report.append(f"## {number} — `{path.name}`")
        report.append("")
        report.append(f"- Mermaid : **{len(diagrams)}** ({type_summary})")
        report.append(f"- Image récapitulative : **{'oui' if image.exists() else 'non'}**")
        if simple_here:
            report.append("- Diagrammes très simples à revoir : " + "; ".join(f"`{x}`" for x in simple_here))
        report.append("")

    # Détecter les anciens titres résiduels après transformation.
    residual = []
    for path in sorted(DOCS.glob("campagne_*/*.md")):
        if CHAPTER.match(path.name) and "## Infographie de révision" in path.read_text(encoding="utf-8"):
            residual.append(path)

    report.insert(5, f"- Chapitres analysés : **{total}**")
    report.insert(6, f"- Anciennes infographies retirées/remplacées : **{with_infographic}**")
    report.insert(7, f"- PNG récapitulatifs raccordés : **{with_image}**")
    report.insert(8, f"- Diagrammes très simples signalés : **{simple}**")
    report.insert(9, "")
    report.append("## Anomalies structurelles")
    report.append("")
    report.extend(structural_issues or ["Aucune anomalie sur les trois premiers H2."])
    report.append("")
    report.append("## Contrôles")
    report.append("")
    report.append(f"- `Infographie de révision` résiduelle : **{len(residual)}**")

    audit = ROOT / "mermaid-audit.md"
    audit.write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
