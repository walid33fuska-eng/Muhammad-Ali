import requests
import json

# الروابط المستخرجة من نطاق OPPO المسموح به
targets = [
    "https://zhongbao.heytap.com",
    "https://zhongbao-ear.heytap.com",
    "https://www.coloros.com",
    "https://developers.oppomobile.com"
]

# مسارات شائعة قد تحتوي على ملفات منسية أو ثغرات أمنية (برمجية ومنطقية)
paths_to_check = [
    "/robots.txt",
    "/.git/HEAD",
    "/.env",
    "/config.json",
    "/wp-json/",
    "/api/v1/",
    "/v1/api"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:109.0) Gecko/109.0 Firefox/113.0"
}

print("[+] بدء فحص الأصول المصرح بها لشركة OPPO...")
print("-" * 50)

for target in targets:
    print(f"\n[*] فحص الهدف الرئيسي: {target}")
    try:
        # فحص استجابة الموقع الرئيسي
        main_resp = requests.get(target, headers=headers, timeout=7, allow_redirects=True)
        print(f"    [-] الحالة: {main_resp.status_code}")
        print(f"    [-] الخادم: {main_resp.headers.get('Server', 'غير معروف')}")
        
        # فحص المسارات الحساسة بحثاً عن ملفات مكشوفة
        for path in paths_to_check:
            url = f"{target}{path}"
            resp = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
            
            # إذا كانت الحالة 200 فهذا يعني أن الملف موجود ومكشوف!
            if resp.status_code == 200:
                print(f"    [🔥 ثغرة محتملة] تم العثور على مسار نشط: {url} (Status: 200)")
            elif resp.status_code == 403:
                print(f"    [!] مسار محمي أو محظور: {url} (Status: 403)")
                
    except requests.exceptions.RequestException as e:
        print(f"    [X] تعذر الاتصال بالهدف: {target}")

print("\n" + "-" * 50)
print("[+] انتهى الفحص الأولي بنجاح. يمكنك الآن صياغة تقريرك إذا وجدت مسارات مكشوفة.")
