# حفظ هذا الملف باسم: oppo_scan.py
# nano oppo_scan.py  ثم لصق الكود، ثم Ctrl+X ثم Y ثم Enter

import requests
import json
import time
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# الأصول المسموح بها رسمياً
LEGAL_ASSETS = [
    "https://id.oppo.com",
    "https://id.heytap.com",
    "https://safe.heytap.com",
    "https://cloud.oppo.com"
]

# الألوان لـ Termux
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

def clear_screen():
    print("\033[2J\033[H")  # مسح الشاشة في Termux

clear_screen()

print(f"{CYAN}{'='*55}{RESET}")
print(f"{CYAN}🔍 OPPO BUG BOUNTY - PASSIVE RECONNAISSANCE{RESET}")
print(f"{WHITE}📅 الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
print(f"{CYAN}{'='*55}{RESET}")
print(f"\n{YELLOW}⚠️ استطلاع سلبي - لا طلبات ضارة{RESET}")
print(f"{GREEN}✅ مسموح ضمن سياسة HackerOne{RESET}\n")

results = {}

for asset in LEGAL_ASSETS:
    print(f"{WHITE}📌 فحص: {asset}{RESET}")
    print("-" * 40)
    
    asset_info = {}
    
    try:
        resp = requests.get(asset, timeout=15, verify=False)
        asset_info['status_code'] = resp.status_code
        
        if resp.status_code == 200:
            print(f"  {GREEN}✅ HTTP {resp.status_code}{RESET}")
        elif resp.status_code == 403:
            print(f"  {YELLOW}⚠️ HTTP {resp.status_code} - ممنوع (قد يكون WAF){RESET}")
        else:
            print(f"  {RED}❌ HTTP {resp.status_code}{RESET}")
            
        print(f"  {WHITE}📋 Server: {resp.headers.get('Server', 'N/A')}{RESET}")
        
    except requests.exceptions.Timeout:
        print(f"  {RED}❌ مهلة انتهت (Timeout){RESET}")
        asset_info['error'] = 'timeout'
        results[asset] = asset_info
        continue
    except Exception as e:
        print(f"  {RED}❌ خطأ: {str(e)[:50]}{RESET}")
        asset_info['error'] = str(e)
        results[asset] = asset_info
        continue
    
    # فحص robots.txt
    try:
        robots_url = f"{asset}/robots.txt"
        robots = requests.get(robots_url, timeout=8, verify=False)
        if robots.status_code == 200:
            print(f"  {GREEN}🤖 robots.txt موجود{RESET}")
        else:
            print(f"  {YELLOW}📄 robots.txt: {robots.status_code}{RESET}")
    except:
        print(f"  {YELLOW}⚠️ robots.txt: تعذر الوصول{RESET}")
    
    # فحص sitemap.xml
    try:
        sitemap_url = f"{asset}/sitemap.xml"
        sitemap = requests.get(sitemap_url, timeout=8, verify=False)
        if sitemap.status_code == 200:
            print(f"  {GREEN}🗺️ sitemap.xml موجود{RESET}")
    except:
        pass
    
    # الـ Cookies
    if 'Set-Cookie' in resp.headers:
        cookie_preview = resp.headers['Set-Cookie'][:40]
        print(f"  {YELLOW}🍪 Cookies موجودة: {cookie_preview}...{RESET}")
    
    results[asset] = asset_info
    time.sleep(0.8)  # تأخير أطول قليلاً لـ Termux
    print()

# الملخص النهائي
print(f"{CYAN}{'='*55}{RESET}")
print(f"{CYAN}📊 ملخص النتائج{RESET}")
print(f"{CYAN}{'='*55}{RESET}")

online_count = 0
for asset, info in results.items():
    if 'status_code' in info and info['status_code'] == 200:
        online_count += 1
        print(f"  {GREEN}🟢 {asset}{RESET}")
    elif 'status_code' in info:
        print(f"  {RED}🔴 {asset} (HTTP {info['status_code']}){RESET}")
    else:
        print(f"  {RED}🔴 {asset} (غير متاح){RESET}")

print(f"\n{GREEN}✅ الأصول المتاحة: {online_count}/{len(LEGAL_ASSETS)}{RESET}")
print(f"\n{YELLOW}📌 انتظر التعليمات التالية...{RESET}")
