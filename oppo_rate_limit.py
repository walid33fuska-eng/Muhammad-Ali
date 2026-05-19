import requests
import time
from datetime import datetime
import urllib3

urllib3.disable_warnings()

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

print(f"{CYAN}Rate Limiting Test - OPPO{RESET}\n")

url = "https://id.oppo.com/v3/auth/login"

# محاولات تسجيل دخول فاشلة متتالية
success_count = 0
failed_count = 0
blocked_count = 0

for i in range(20):  # 20 محاولة
    data = {
        "email": f"fake{i}@test.com",
        "password": "wrongpassword123"
    }
    
    try:
        r = requests.post(url, json=data, timeout=10, verify=False)
        
        if r.status_code == 429:  # Too Many Requests
            print(f"{RED}❌ محاولة {i+1}: تم الحظر! (429 Too Many Requests){RESET}")
            blocked_count += 1
            break
        elif r.status_code == 401 or r.status_code == 400:
            print(f"{YELLOW}⚠️ محاولة {i+1}: فاشلة ({r.status_code}){RESET}")
            failed_count += 1
        else:
            print(f"{GREEN}✅ محاولة {i+1}: {r.status_code}{RESET}")
            success_count += 1
            
    except Exception as e:
        print(f"{RED}خطأ: {e}{RESET}")
    
    time.sleep(0.2)  # 0.2 ثانية بين كل محاولة

print(f"\n{CYAN}{'='*40}{RESET}")
print(f"النتيجة: {failed_count} فاشلة, {blocked_count} محظورة")

if blocked_count > 0:
    print(f"{GREEN}✅ النظام يحمي نفسه - يوجد Rate Limiting{RESET}")
else:
    print(f"{RED}⚠️ لا يوجد Rate Limiting واضح - قد يكون ثغرة{RESET}")
