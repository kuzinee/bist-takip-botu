import os
import requests
import pandas as pd
import numpy as np
import yfinance as yf

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID")

BIST_HISSELER = [
    "AGHOL.IS", "AKBNK.IS", "AKSA.IS", "ALARK.IS", "ARCLK.IS", "ARDYZ.IS", "ASELS.IS", 
    "BIMAS.IS", "BRSAN.IS", "DOAS.IS", "EGGUB.IS", "ENKAI.IS", "EREGL.IS", "FROTO.IS", 
    "GARAN.IS", "GENIL.IS", "HEKTS.IS", "ISCTR.IS", "KCHOL.IS", "KONTR.IS", "KOZAL.IS", 
    "KUVVA.IS", "MGROS.IS", "MIATK.IS", "ODAS.IS", "OYAKC.IS", "PETKM.IS", "PGSUS.IS", 
    "SAHOL.IS", "SISE.IS", "SASA.IS", "THYAO.IS", "TOASO.IS", "TRALT.IS", "TCELL.IS", "TUPRS.IS"
]

def rsi_hesapla(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def telegram_mesaj_gonder(mesaj_metni):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj_metni}
    res = requests.post(url, json=payload, timeout=10)
    if res.status_code != 200:
        print(f"Telegram Hatasi: {res.text}")
        res.raise_for_status()

def hisse_taramasi():
    fırsat_hisseleri = []
    
    for hisse in BIST_HISSELER:
        try:
            df = yf.download(hisse, period="6mo", interval="1d", progress=False)
            if len(df) < 30: continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            df['RSI'] = rsi_hesapla(df['Close'], 14)
            df['SMA20'] = df['Close'].rolling(window=20).mean()
            df['SMA50'] = df['Close'].rolling(window=50).mean()
            
            son_fiyat = float(df['Close'].iloc[-1])
            son_rsi = float(df['RSI'].iloc[-1])
            sma20 = float(df['SMA20'].iloc[-1])
            sma50 = float(df['SMA50'].iloc[-1])
            en_yuksek_20g = float(df['High'].iloc[-21:-1].max())
            
            hisse_adi = hisse.replace(".IS", "")
            durum = None
            
            # Kriter 1: Direnç Kırılımına Yakın (RSI 45 - 68 Arası)
            if 45 <= son_rsi <= 68 and son_fiyat >= (en_yuksek_20g * 0.95) and son_fiyat > sma20:
                durum = "Direnç Kırılım Adayı 🚀"
                
            # Kriter 2: Dipte Yatay Toplanan / Soğuk RSI (RSI 35 - 50 Arası + SMA20 Üstü)
            elif 35 <= son_rsi <= 50 and son_fiyat > sma20 and sma20 > sma50:
                durum = "Dipte Yatay Konsolide 💤"
                
            # Kriter 3: Düzeltmesini Tamamlamış Tepki Adayı (RSI 40 - 55 Arası)
            elif 40 <= son_rsi <= 55 and son_fiyat > sma20:
                durum = "Trend Üstü Güçlenme 📈"

            if durum:
                fırsat_hisseleri.append(f"{hisse_adi} | Fiyat: {son_fiyat:.2f} | RSI: {son_rsi:.1f} | Durum: {durum}")
                
        except Exception as e:
            continue
            
    if fırsat_hisseleri:
        mesaj = "🔍 BIST FIRSAT TARAMA SONUÇLARI 🔍\n\n" + "\n".join(fırsat_hisseleri)
    else:
        mesaj = "Piyasada belirlenen 3 farklı kritere uyan hisse bulunamadı."
        
    telegram_mesaj_gonder(mesaj)

if __name__ == "__main__":
    hisse_taramasi()
