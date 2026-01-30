from playwright.sync_api import sync_playwright
import json
import time
import re

def vpn_password_al():
    with sync_playwright() as p:
        # Tarayıcıyı başlat (headless=True: arkaplanda çalışır)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        try:
            print("Siteye gidiliyor...")
            page.goto("https://www.vpnbook.com/freevpn/openvpn", wait_until="networkidle", timeout=60000)
            
            # JavaScript'in kutuları doldurması için biraz bekleyelim
            page.wait_for_timeout(5000) 
            
            # Görseldeki "PASSWORD" yazısını bul ve yanındaki/altındaki metni al
            # Next.js yapısında şifre genellikle bir div içinde 'pvgz9pq' gibi durur.
            content = page.content()
            
            # Strateji: Sitedeki tüm metni çek ve 'vpnbook' (username) kelimesinden sonra gelen 
            # ilk 7-8 haneli harf-rakam karışık kelimeyi yakala.
            # (Bu yöntem görseldeki hiyerarşiyi tam taklit eder)
            
            # Önce kullanıcı adını bulalım (referans noktası)
            body_text = page.inner_text("body")
            if "vpnbook" in body_text:
                # Kullanıcı adından sonraki kısmı kes
                after_username = body_text.split("vpnbook")[-1]
                
                # Bu kısımdaki ilk 7-8 haneli, rakam içeren kelimeyi bul
                match = re.search(r'([a-z0-9]{7,8})', after_username)
                
                if match:
                    sifre = match.group(1).strip()
                    # Teknik kelimeleri engelle
                    if sifre not in ['static', 'chunks', 'viewport', 'visible']:
                        print(f"Buldum! Şifre ekranda göründüğü gibi: {sifre}")
                        return sifre

            print("Hata: Şifre metni ekranda tespit edilemedi.")
            
        except Exception as e:
            print(f"Tarayıcı hatası: {e}")
        finally:
            browser.close()
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump({"password": yeni_sifre}, f, indent=4)
    print(f"JSON Başarıyla Yazıldı: {yeni_sifre}")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
