import requests
import json
import re

def vpn_password_al():
    url = "https://www.vpnbook.com/freevpn"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            content = response.text
            
            # Next.js verileri genellikle __NEXT_DATA__ içinde veya direkt metin olarak bulunur
            # Şifreyi "Password: " ifadesinden hemen sonraki tırnaklar veya taglar arasında arayalım
            # Yeni yapıda şifre muhtemelen düz metin veya bir JSON objesi içinde
            
            # 1. Deneme: Ham metin içinde Password ara (Next.js'in render ettiği metin)
            match = re.search(r'Password:\s*([a-zA-Z0-9]+)', content)
            
            if not match:
                # 2. Deneme: HTML tagları arasına gizlenmişse
                match = re.search(r'Password:.*?>(.*?)<', content, re.DOTALL)

            if match:
                sifre = match.group(1).strip()
                # Eğer çok uzunsa veya garip karakterler varsa temizleyelim
                if 4 < len(sifre) < 15:
                    print(f"Buldum! Yeni Şifre: {sifre}")
                    return sifre

            # 3. Deneme: Eğer hala bulamadıysa, tüm sayfadaki 7-8 karakterli alfanümerik dizileri tara
            # VPNBook şifreleri genelde 7-8 hanelidir.
            print("Standart yöntemle bulunamadı, derin tarama yapılıyor...")
            potential_passwords = re.findall(r'([a-zA-Z0-9]{7,8})', content)
            # Bu kısım riskli olabilir ama çaresiz kalırsak loglardan bakarız
            print(f"Olası şifreler: {potential_passwords[:5]}")
            
        else:
            print(f"Erişim hatası: {response.status_code}")
    except Exception as e:
        print(f"Hata: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Başarılı! {dosya_adi} güncellendi.")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Maalesef şifre Next.js yapısı içinden ayıklanamadı.")
