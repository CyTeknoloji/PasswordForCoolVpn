from playwright.sync_api import sync_playwright
import json
import re

def vpn_password_al():
    with sync_playwright() as p:
        # Gerçek bir kullanıcı gibi görünmek için detaylı ayarlar
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        try:
            print("Siteye gidiliyor...")
            # 'networkidle' yerine 'domcontentloaded' (daha hızlı) kullanıyoruz
            page.goto("https://www.vpnbook.com/freevpn/openvpn", wait_until="domcontentloaded", timeout=60000)
            
            # Şifrenin içinde olduğu kutunun yüklenmesi için kritik bekleyiş
            # 'vpnbook' metni ekranda görünene kadar bekle (en fazla 20 sn)
            page.wait_for_selector("text=vpnbook", timeout=20000)
            
            # Sayfanın tam metnini al
            body_text = page.inner_text("body")
            
            # Analiz: vpnbook kelimesinden sonra gelen 7-8 haneli harf+rakam yapısını yakala
            if "vpnbook" in body_text:
                # Kullanıcı adından sonraki bölüme odaklan
                after_username = body_text.split("vpnbook")[-1]
                
                # Regex: Sadece küçük harf ve rakam içeren 7-8 haneli ilk kelimeyi al
                # (Sitedeki 180x180 gibi statik değerleri elemek için harf+rakam şartı koyuyoruz)
                match = re.search(r'([a-z0-9]{7,8})', after_username)
                
                if match:
                    sifre = match.group(1).strip()
                    # Teknik terimleri ele
                    if sifre not in ['static', 'chunks', 'viewport', 'visible']:
                        print(f"BULDUM! Güncel Şifre: {sifre}")
                        return sifre

            print("Hata: Şifre metni sayfada bulunamadı.")
            
        except Exception as e:
            print(f"Hata detayı: {e}")
        finally:
            browser.close()
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump({"pass": yeni_sifre}, f, indent=4)
    print(f"JSON başarıyla güncellendi: {yeni_sifre}")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
