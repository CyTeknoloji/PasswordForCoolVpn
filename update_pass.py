import requests
import json
import re

def vpn_password_al():
    url = "https://www.vpnbook.com/freevpn"
    # Daha detaylı bir User-Agent (Sanki gerçek bir Windows/Chrome kullanıcısı gibi)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            content = response.text
            
            # YÖNTEM A: En yaygın etiket yapısı
            matches = re.findall(r'Password:\s*<b>(.*?)</b>', content, re.IGNORECASE)
            
            # YÖNTEM B: Eğer A bulamazsa (etiketler arası boşluk varsa)
            if not matches:
                matches = re.findall(r'Password:.*?>(.*?)<', content, re.IGNORECASE | re.DOTALL)

            if matches:
                # Sayfada birden fazla password olabilir, genellikle sonuncular günceldir.
                # Ama biz 'kısa ve harf-rakam karışık' olanı arıyoruz (genelde 7-8 karakter)
                for potential_pass in matches:
                    clean_pass = potential_pass.strip()
                    # Şifre kriteri: 5-10 karakter arası, sadece harf ve rakam
                    if 5 <= len(clean_pass) <= 12 and clean_pass.isalnum():
                        print(f"Buldum! Şifre: {clean_pass}")
                        return clean_pass
            
            # Hiçbiri olmazsa loglara sayfanın bir kısmını dök (Hata çözmek için)
            print("Hata: Şifre kalıbı bulunamadı.")
            print("Sayfa içeriğinden kesit (ilk 500 karakter):", content[:500])
            
        else:
            print(f"Erişim engellendi! Durum kodu: {response.status_code}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"JSON '{yeni_sifre}' ile güncellendi.")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Şifre hala alınamıyor.")
