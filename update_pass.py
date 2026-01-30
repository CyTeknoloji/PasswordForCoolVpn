import cloudscraper
import json
import re

def vpn_password_al():
    # En üst düzey tarayıcı taklidi
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True,
            'mobile': False
        }
    )
    
    url = "https://www.vpnbook.com/freevpn/openvpn"
    
    try:
        response = scraper.get(url, timeout=30)
        content = response.text

        # Eğer site tamamen engelliyorsa içeriği görelim (Debug için)
        if "vpnbook" not in content.lower():
            print("Site içeriği bot korumasına takıldı, veri alınamıyor.")
            return None

        # STRATEJİ: Görselde şifre 'pvgz9pq' gibi 7 haneli. 
        # Genellikle "password":"..." veya >pvgz9pq< şeklinde durur.
        
        # Tüm 7 haneli, en az 1 rakam içeren ve 'vpnbook' olmayan dizileri bul
        # Bu sefer regex'i çok daraltıyoruz
        pattern = r'[a-z0-9]{7}'
        matches = re.findall(pattern, content)
        
        # Yasaklı kelime listesini genişletelim
        blacklist = ['viewport', 'justify', 'visible', 'static', 'chunks', 'charset', 'display', 'version', '180x180', 'favicon']

        for aday in matches:
            # 1. Kriter: Harf ve rakam karışık olmalı (sadece harf veya sadece rakam olanları ele)
            if any(c.isdigit() for c in aday) and any(c.isalpha() for c in aday):
                # 2. Kriter: Yasaklı listede olmamalı
                if aday not in blacklist and "vpnbook" not in aday:
                    # 3. Kriter: Genellikle şifreler sesli harf içermeyebilir veya rastgeledir
                    print(f"Potansiyel Şifre Bulundu: {aday}")
                    return aday

    except Exception as e:
        print(f"Hata: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"GUNCELLEME BASARILI: {yeni_sifre}")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        # Eğer hala bulamazsa, manuel girmek için JSON'u bozma
        print("Sifre hala yakalanamıyor.")
