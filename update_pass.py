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

        # STRATEJİ: vpnbook kullanıcı adından sonra gelen ilk şifreyi bul.
        # Görselde USERNAME: vpnbook, PASSWORD: [şifre] şeklinde bir hiyerarşi var.
        
        # vpnbook kelimesini bul ve ondan sonraki 200 karakterlik alanı incele
        parts = content.split("vpnbook")
        
        for i in range(1, len(parts)):
            # vpnbook'tan sonra gelen bölümdeki tırnak içindeki veya tag içindeki dizileri ara
            # Genellikle Next.js verisinde "vpnbook","password":"pvgz9pq" gibi durur.
            candidates = re.findall(r'"([a-z0-9]{7,8})"', parts[i])
            
            for aday in candidates:
                # Yasaklı kelimeleri filtrele
                if aday not in ['vpnbook', 'justify', 'display', 'initial', 'charset', 'version', 'visible']:
                    # Şifre mutlaka rakam içermelidir (VPNBook şifrelerinin genel özelliği)
                    if any(char.isdigit() for char in aday):
                        print(f"Doğru Şifre Yakalandı: {aday}")
                        return aday

    except Exception as e:
        print(f"Hata: {e}")
    return None

def json_guncelle(yeni_sifre):
    dosya_adi = "password.json"
    data = {"password": yeni_sifre}
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"İşlem Başarılı: {dosya_adi} -> {yeni_sifre}")

if __name__ == "__main__":
    sifre = vpn_password_al()
    if sifre:
        json_guncelle(sifre)
    else:
        print("Şifre bulunamadı.")
