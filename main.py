import os
import requests
import pandas as pd

# GitHub Secrets veya Çevre Değişkenleri
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID") # Secret isminize göre güncelleyin

def telegram_mesaj_gonder(mesaj_metni):
    """
    Telegram API üzerinden mesaj gönderir. 
    Hata durumunda exception fırlatarak GitHub Actions'ın patlamasını sağlar.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj_metni
        # parse_mode satırı biçimlendirme hatalarını önlemek için kaldırılmıştır.
    }
    
    response = requests.post(url, json=payload, timeout=10)
    
    # Telegram 400, 401, 404 gibi bir hata döndürürse burada patlayacak ve Actions loguna yazacak
    if response.status_code != 200:
        print(f"[HATA] Telegram Mesajı Gönderilemedi! Hata Kodu: {response.status_code}, Detay: {response.text}")
        response.raise_for_status()
    else:
        print("[BAŞARILI] Telegram mesajı iletildi.")

def main():
    print("İşlem başlatılıyor...")
    
    # 1. Veri İşleme / Analiz Adımı (Örnek Mantık)
    # df = pd.read_csv('T1.csv') ...
    
    bulunan_sonuclar = [] # Analiz sonucu elde edilen veriler
    
    # 2. Telegram Gönderim Kontrolü
    if bulunan_sonuclar:
        mesaj = "=== ANALİZ SONUÇLARI ===\n\n"
        for satir in bulunan_sonuclar:
            mesaj += f"- {satir}\n"
        
        telegram_mesaj_gonder(mesaj)
    else:
        # Veri çıkmadığında da bilgilendirme göndererek sistemin çalıştığını teyit edin
        bilgi_mesaji = "Sistem çalıştı: Belirtilen kriterlere uyan yeni bir sonuç bulunamadı."
        print(bilgi_mesaji)
        telegram_mesaj_gonder(bilgi_mesaji)

if __name__ == "__main__":
    main()
