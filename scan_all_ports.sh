#!/bin/bash

IPS=(
  "194.204.217.65"
  "194.204.217.205"
  "194.204.217.173"
  "81.192.44.133"
  "41.248.240.121"
)

PORTS=(22 25 80 443 465 587 993 995 3306 8080 8443 2082 2086 2087 2095 2096)

for ip in "${IPS[@]}"; do
  echo ""
  echo "=== $ip ==="
  for port in "${PORTS[@]}"; do
    (echo >/dev/tcp/$ip/$port) 2>/dev/null && echo "✓ Port $port مفتوح"
  done
done
