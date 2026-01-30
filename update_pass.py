import requests
import json
import re

def vpn_password_al():
    url = "https://www.vpnbook.com/freevpn/openvpn"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            return None

        content = response.text

        # 1. ADIM: Next.js'in ana veri bloğunu yakala
        next_data_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', content)
        
        if next_data_match:
            json_data = json.loads(next_data_match.group(1))
            
            # JSON içinde derinlemesine arama yapan fonksiyon
            def find_password(obj):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        # Şifre genellikle 'password' anahtarında veya 'text' içindedir
                        if k.lower() == 'password' and isinstance(v, str):
                            return v
                        # Eğer anahtar ismi farklıysa, 7-8 haneli rakam içeren değerleri kontrol et
                        if isinstance(v, str) and 7 <= len(v) <= 8 and any(char.isdigit() for char in v):
                            if v not in ['viewport', '180x180', 'vpnbook', 'justify']:
                                return v
                        res = find_password(v)
                        if res: return res
                elif isinstance(obj, list):
                    for item in obj:
                        res = find_password(item)
                        if res: return res
                return None

            sifre = find_password(json_data)
            if sifre:
                print(f"Sistemin derinliklerinden yakalandı: {sifre}")
                return sifre

        # 2. ADIM: Yedek yöntem (Eğer JSON bloğu değişirse)
        # vpnbook kelimesinden hemen sonra gelen 7 haneli rakamlı kelimeyi al
        match = re.findall(r'\"([a-z0-9]{7,8})\"', content)
        for aday in match:
            if any(char.isdigit() for char in aday) and aday not in ['180x180', 'apple-touch-icon']:
                return aday

    except Exception as e:
        print(f"Hata: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"İşlem Tamam: {dosya_adi} -> {yeni_sifre}")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Şifre bulunamadı.")
