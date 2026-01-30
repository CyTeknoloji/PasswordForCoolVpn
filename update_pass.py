import requests
import json
import re

def vpn_password_al():
    # URL'yi senin görselindeki gibi güncelledik
    url = "https://www.vpnbook.com/freevpn/openvpn"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"Siteye erişilemedi. Hata kodu: {response.status_code}")
            return None

        content = response.text

        # Görseldeki "PASSWORD" kutusunun içindeki 7 haneli şifreyi yakalayalım.
        # Genellikle "PASSWORD" başlığından sonra gelen ilk küçük harf/rakam dizisidir.
        
        # 1. Yöntem: Metin bazlı arama (Görseldeki pvgz9pq gibi yapıları arar)
        # Next.js yapısında şifre genellikle çift tırnaklar arasında kalır.
        bulunanlar = re.findall(r'\"([a-z0-9]{7,8})\"', content)
        
        for aday in bulunanlar:
            # vpnbook kullanıcı adını ve bazı sistem kelimelerini eleyelim
            if aday not in ['vpnbook', 'openvpn', 'display', 'version', 'initial']:
                print(f"Şifre yakalandı: {aday}")
                return aday

        # 2. Yöntem: Daha spesifik arama
        match = re.search(r'PASSWORD.*?([a-z0-9]{7,8})', content, re.IGNORECASE | re.DOTALL)
        if match:
            sifre = match.group(1).strip()
            print(f"Alternatif yöntemle yakalandı: {sifre}")
            return sifre

    except Exception as e:
        print(f"Hata: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Dosya güncellendi. Yeni şifre: {yeni_sifre}")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Şifre hala bulunamadı. Lütfen URL'yi veya sayfa yapısını kontrol et.")
