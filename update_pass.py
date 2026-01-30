import requests
import json
import re

def vpn_password_al():
    url = "https://www.vpnbook.com/freevpn"
    # Siteye istek gönderiyoruz
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Sitedeki "Password: <b>abc123</b>" yapısını arıyoruz
        # Not: Sitenin HTML yapısına göre burayı ince ayar çekebiliriz
        match = re.search(r'Password: <b>(.*?)</b>', response.text)
        if match:
            yeni_sifre = match.group(1).strip()
            print(f"Yeni şifre bulundu: {yeni_sifre}")
            return yeni_sifre
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json" # Dosya adının tam doğru olduğundan emin ol
    
    # Mevcut JSON'u oku
    with open(dosya_adi, 'r') as f:
        data = json.load(f)
    
    # Şifreyi güncelle (JSON yapın { "password": "..." } şeklindeyse)
    data['pass'] = yeni_sifre
    
    # JSON'u geri kaydet
    with open(dosya_adi, 'w') as f:
        json.dump(data, f, indent=4)
    print("JSON başarıyla güncellendi.")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Şifre bulunamadı, site yapısı değişmiş olabilir.")
