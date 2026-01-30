import cloudscraper
import json
import re

def vpn_password_al():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    # Görseldeki kesin adres
    url = "https://www.vpnbook.com/freevpn/openvpn"
    
    try:
        response = scraper.get(url, timeout=30)
        if response.status_code != 200:
            return None

        content = response.text

        # 1. YÖNTEM: vpnbook kullanıcı adını "çapa" (anchor) olarak kullan
        # Kullanıcı adından sonraki 500 karakteri tara
        if "vpnbook" in content:
            after_username = content.split("vpnbook")[-1][:500]
            # Sadece tırnak içindeki 7 haneli, rakam içeren dizileri bul
            candidates = re.findall(r'\"([a-z0-9]{7,8})\"', after_username)
            
            for aday in candidates:
                # Kesin elemeler: Teknik kelimeler ve senin yakaladığın hatalı kodlar
                if aday in ['8f193b7f', 'viewport', 'justify', 'visible', 'static', 'chunks']:
                    continue
                
                # Şifre kriteri: En az bir rakam içermeli ve sadece harf/rakam olmalı
                if any(char.isdigit() for char in aday) and aday.isalnum():
                    print(f"Doğrulandı! Şifre: {aday}")
                    return aday

        # 2. YÖNTEM: Eğer üstteki bulamazsa tüm sayfada "password":"sifre" kalıbını ara
        match = re.search(r'\"password\":\"([a-z0-9]{7,8})\"', content)
        if match:
            return match.group(1)

    except Exception as e:
        print(f"Hata: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Başarıyla güncellendi: {yeni_sifre}")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Şifre hala yakalanamıyor, manuel kontrol gerekebilir.")
