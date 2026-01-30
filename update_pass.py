import requests
import json
import re

def vpn_password_al():
    url = "https://www.vpnbook.com/freevpn"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            html_content = response.text
            
            # 1. Yöntem: Standart <li>Password: <b>sifre</b></li> yapısını dene
            match = re.search(r'Password:\s*<b>(.*?)</b>', html_content, re.IGNORECASE)
            
            # 2. Yöntem: Eğer üstteki olmazsa, sadece "Password:" kelimesinden sonraki metni yakala
            if not match:
                # Password: kelimesinden sonraki HTML etiketlerini temizleyip kelimeyi alır
                match = re.search(r'Password:\s*<[^>]+>([^<]+)<', html_content, re.IGNORECASE)
            
            # 3. Yöntem: Ham metin üzerinden (tag bağımsız)
            if not match:
                match = re.search(r'Password:\s*(\w+)', html_content, re.IGNORECASE)

            if match:
                yeni_sifre = match.group(1).strip()
                # Eğer şifre içinde HTML kalıntısı varsa temizle (örn: </b>)
                yeni_sifre = re.sub('<[^<]+?>', '', yeni_sifre)
                print(f"Buldum! Şifre: {yeni_sifre}")
                return yeni_sifre
            else:
                # Debug için sayfanın bir kısmını yazdıralım (Actions loglarında görebilmek için)
                print("Hata: Şifre etiketi bulunamadı. Sayfa içeriği değişmiş.")
                print("Sayfa başlığı:", re.search(r'<title>(.*?)</title>', html_content))
        else:
            print(f"Siteye erişim hatası: {response.status_code}")
    except Exception as e:
        print(f"Sistem hatası: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    try:
        data = {}
        # Dosya varsa oku
        try:
            with open(dosya_adi, 'r') as f:
                data = json.load(f)
        except:
            print("Dosya bulunamadı, yeni oluşturuluyor.")

        # Güncelle
        data['password'] = yeni_sifre
        
        with open(dosya_adi, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"JSON dosyası '{yeni_sifre}' ile güncellendi.")
        return True
    except Exception as e:
        print(f"JSON kayıt hatası: {e}")
        return False

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
