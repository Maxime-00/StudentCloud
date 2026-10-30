#!/usr/bin/env bash
# Genereert een self-signed / interne-CA certificaat voor de Nginx reverse
# proxy van de Studentencloud (M07 — TLS via goedgekeurd publicatiepad).
#
# Doel: TLS-terminatie op poort 443 voor de interne cloud, zonder publiek
# domein. De browser meldt een onbekende certificaatuitgever (verwacht bij een
# self-signed cert); éénmalig accepteren. Voor productie kan dit certificaat
# vervangen worden door een certificaat van een interne CA.
#
# Gebruik (op de VM):
#   sudo bash infrastructure/scripts/gen-selfsigned-cert.sh
#
# Output:
#   /etc/nginx/ssl/studentencloud.key  (privésleutel)
#   /etc/nginx/ssl/studentencloud.crt  (self-signed certificaat, 365 dagen)

set -euo pipefail

OUT_DIR="/etc/nginx/ssl"
KEY="${OUT_DIR}/studentencloud.key"
CRT="${OUT_DIR}/studentencloud.crt"
DAYS=365
# Hostnaam die als Common Name wordt gebruikt.
CN="studentencloud"
# Subject Alternative Names: de hostnaam(en) en IP die de proxy serveert.
# Aanjastpen indien het publicatiepad een andere hostnaam/IP krijgt.
SAN="DNS:studentencloud,DNS:studentencloud.vives.local,IP:10.20.254.141"

sudo mkdir -p "${OUT_DIR}"

echo "Genereer self-signed certificaat (${DAYS} dagen) in ${OUT_DIR} ..."
sudo openssl req -x509 -nodes -newkey rsa:4096 \
  -keyout "${KEY}" -out "${CRT}" \
  -days "${DAYS}" \
  -subj "/CN=${CN}" \
  -addext "subjectAltName=${SAN}"

sudo chmod 600 "${KEY}"
sudo chmod 644 "${CRT}"

echo "Klaar."
echo "  cert : ${CRT}"
echo "  key  : ${KEY}"
echo ""
echo "Verificatie:"
echo "  sudo openssl x509 -in ${CRT} -noout -subject -issuer -dates -ext subjectAltName"
echo "  sudo nginx -t && sudo systemctl reload nginx"
