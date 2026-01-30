import cloudscraper
import json
import re

def vpn_password_al():
    # Cloudflare engeline takılmamak için scraper oluşturuyoruz
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    url = "https://www.vpnbook.com/freevpn/openvpn"
    
    try:
        response = scraper.get(url, timeout=30)
        if response.status_code != 200:
            print(f"Siteye erişim engellendi. Durum: {response.status_code}")
            return None

        content = response.text

        # 1. YÖNTEM: Next.js veri havuzunu deşiyoruz
        # Bu blokta şifre kesinlikle bulunur
        next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', content)
        
        if next_data:
            data = json.loads(next_data.group(1))
            
            # Tüm JSON ağacını stringe çevirip içinde 7 haneli şifreyi arayalım
            json_str = json.dumps(data)
            # vpnbook kullanıcı adından hemen sonra gelen 7 haneli şifreyi bul
            # Örnek: "vpnbook","password":"pvgz9pq"
            match = re.search(r'"password":"([a-z0-9]{7,8})"', json_str)
            if match:
                sifre = match.group(1)
                print(f"Bulunan Şifre: {sifre}")
                return sifre

        # 2. YÖNTEM: Ham metin taraması (Yedek)
        # "pvgz9pq" gibi 7-8 haneli ve içinde rakam olan kelimeleri bul
        potential = re.findall(r'[a-z0-9]{7,8}', content)
        for aday in potential:
            if any(char.isdigit() for char in aday):
                if aday not in ['vpnbook', 'viewport', 'justify', 'visible', '180x180']:
                    print(f"Yedek yöntemle bulundu: {aday}")
                    return aday

    except Exception as e:
        print(f"Hata: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Güncelleme Başarılı: {yeni_sifre}")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Şifre hala alınamıyor. Cloudflare botu durdurmuş olabilir.")
