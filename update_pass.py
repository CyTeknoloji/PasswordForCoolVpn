import requests
import json
import re

def vpn_password_al():
    url = "https://www.vpnbook.com/freevpn"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"Siteye erişilemiyor: {response.status_code}")
            return None

        content = response.text

        # 1. YÖNTEM: Next.js içindeki JSON verisini ayıkla
        # Next.js verileri genellikle <script id="__NEXT_DATA__" type="application/json">...</script> arasındadır
        next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', content)
        if next_data:
            json_str = next_data.group(1)
            # JSON içindeki tüm 7-8 karakterli şifre benzeri yapıları ara
            # VPNBook şifreleri genellikle rakam ve küçük harf karışımıdır
            sifre_adaylari = re.findall(r'\"([a-z0-9]{7,8})\"', json_str)
            for aday in sifre_adaylari:
                # Bildiğimiz bazı kelimeleri eleyelim (index, search vb.)
                if aday not in ['version', 'scripts', 'display', 'initial']:
                    print(f"JSON içinden aday bulundu: {aday}")
                    return aday

        # 2. YÖNTEM: Eğer üstteki bulamazsa, ham metin içinde "Password:" kelimesine en yakın 7-8 haneli kelimeyi bul
        # Bu yöntem HTML etiketlerinden bağımsızdır
        password_bolgesi = re.search(r'Password:.*?([a-z0-9]{7,8})', content, re.IGNORECASE | re.DOTALL)
        if password_bolgesi:
            sifre = password_bolgesi.group(1).strip()
            print(f"Ham metinden yakalandı: {sifre}")
            return sifre

        print("Hata: Hiçbir yöntemle şifre yakalanamadı.")
        # Hata çözmek için sayfanın bir kısmını tekrar görelim
        print("Sayfa içeriği (Snippet):", content[1000:2000])

    except Exception as e:
        print(f"Hata: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"İşlem Tamam! {dosya_adi} güncellendi.")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Şifre hala alınamıyor. VPNBook yapıyı çok sıkılaştırmış olabilir.")
