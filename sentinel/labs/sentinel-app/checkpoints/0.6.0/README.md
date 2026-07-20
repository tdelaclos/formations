# Sentinel 0.6.0

Ce checkpoint correspond à l'intégration FreeIPA de la campagne 8. Il conserve le mTLS de 0.5.0 et ajoute une autorisation applicative fondée sur les identités DNS présentes dans le SAN des certificats clients.

Nouveautés :

- validation cryptographique de la chaîne cliente ;
- extraction des identités `DNS` du `subjectAltName` ;
- liste fermée `allowed_dns_names` ;
- réponse HTTP 403 pour un certificat de confiance dont l'identité n'est pas autorisée ;
- healthcheck mTLS utilisant le nom présent dans le SAN du serveur.

## Organisation du code

Le nouveau module `identity.py` intervient après `tls_support.py` : TLS valide la chaîne de confiance, puis l'application compare les SAN DNS à la liste autorisée. Le code rend ainsi visible la différence pédagogique entre authentification et autorisation.

```bash
python3 src/sentinel.py --config config/sentinel.conf --check-config
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf serve
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf --healthcheck
python3 -m unittest discover -s tests -v
```

La configuration fournie garde TLS désactivé afin de rester exécutable sans clé privée dans Git. Le laboratoire FreeIPA délivre les certificats, active le mTLS et remplace les identités documentaires par les noms réels.
