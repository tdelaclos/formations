# Campagne 12 — Supervision et audit

Cette campagne transforme le socle Sentinel en système observable et auditable. Elle sépare les journaux d'exploitation, les preuves issues du noyau et les métriques, puis les réunit dans un dispositif de détection, d'alerte et de visualisation exploitable pendant un incident.

## Parcours

1. [Centraliser les journaux avec Rsyslog](12.1-centraliser-journaux-rsyslog.md) ;
2. [auditer le système avec `auditd`](12.2-auditer-systeme-auditd.md) ;
3. [contrôler l'intégrité des fichiers avec AIDE](12.3-controler-integrite-fichiers-aide.md) ;
4. [superviser Sentinel avec Prometheus](12.4-superviser-sentinel-prometheus.md) ;
5. [concevoir des alertes avec Alertmanager](12.5-concevoir-alertes-alertmanager.md) ;
6. [construire le tableau de bord Sentinel](12.6-construire-tableau-bord-sentinel.md).

## Résultat attendu

À la fin de la campagne, l'apprenant dispose d'une chaîne Rsyslog chiffrée, d'une politique Audit persistante, d'une baseline AIDE maîtrisée, d'une collecte Prometheus, d'alertes testées et d'un tableau de bord Grafana versionné. Les preuves produites permettent de distinguer une panne, une dérive et une action humaine.

Les chapitres suivent le formalisme défini dans le [`GUIDE-REDACTION.md`](../GUIDE-REDACTION.md).
