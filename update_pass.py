import requests
import json
import re

def vpn_password_al():
    # Görseldeki doğru alt sayfa
    url = "https://www.vpnbook.com/freevpn/openvpn"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            return None

        content = response.text

        # 1. YÖNTEM: Next.js Veri Bloklarını Tara (En Garantisi)
        # Sitedeki tüm JSON benzeri yapıları bulur
        json_blocks = re.findall(r'\{[^{}]+\}', content)
        
        # Ekran görüntündeki güncel şifre: pvgz9pq (7 karakter)
        # Şifre kalıbı: Sadece küçük harf ve rakamdan oluşan 7 veya 8 karakterli diziler
        sifre_kalibi = re.compile(r'^[a-z0-9]{7,8}$')

        for blok in json_blocks:
            # JSON içindeki tırnak içindeki kelimeleri ayıkla
            kelimeler = re.findall(r'"([^"]+)"', blok)
            for kelime in kelimeler:
                # 'viewport', 'width', 'vpnbook' gibi teknik kelimeleri filtrele
                if sifre_kalibi.match(kelime):
                    if kelime not in ['viewport', 'vpnbook', 'openvpn', 'display', 'initial', 'charset']:
                        print(f"Şifre Bulundu: {kelime}")
                        return kelime

        # 2. YÖNTEM: Eğer üstteki bulamazsa, metin içindeki Password kutusunu manuel tara
        # Next.js bazen veriyi 'props' içinde gönderir
        if "pvgz9pq" in content or "Password" in content:
            # Password kelimesinden sonra gelen ilk 7-8 haneli alfanümerik dize
            match = re.search(r'Password.*?([a-z0-9]{7,8})', content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1)

    except Exception as e:
        print(f"Hata: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    # Dosya içeriğini tam istediğin formatta (sadece password anahtarıyla) yazar
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"İşlem Başarılı: {dosya_adi} -> {yeni_sifre}")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Şifre yakalanamadı. Site koruması veya yapı değişikliği var.")
