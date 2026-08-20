import pandas as pd
import numpy as np
import yfinance as yf

# BIST 100 Hisseleri Listesi (Ekstra hisseler eklenebilir)
BIST_HISSELER = [
    "AGHOL.IS", "AKBNK.IS", "AKSA.IS", "ALARK.IS", "ARCLK.IS", "ARDYZ.IS", "ASELS.IS", 
    "BIMAS.IS", "BRSAN.IS", "C enterprise.IS", "DOAS.IS", "EGGUB.IS", "EKGYO.IS", "ENKAI.IS", 
    "EREGL.IS", "FROTO.IS", "GARAN.IS", "GENIL.IS", "HEKTS.IS", "ISCTR.IS", "KCHOL.IS", 
    "KONTR.IS", "KOZAL.IS", "KUVVA.IS", "MGROS.IS", "MIATK.IS", "ODAS.IS", "OYAKC.IS", 
    "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SISE.IS", "SASA.IS", "THYAO.IS", "TOASO.IS", 
    "TRALT.IS", "TCELL.IS", "TUPRS.IS", "YKBNK.IS"
]

def rsi_hesapla(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def hisse_taramasi():
    fırsat_hisseleri = []
    
    print("BIST Taraması Başlatılıyor...\n")
    
    for hisse in BIST_HISSELER:
        try:
            # Son 6 aylık günlük veriyi çek
            df = yf.download(hisse, period="6mo", interval="1d", progress=False)
            
            if len(df) < 30:
                continue
            
            # Sütun isimlerini düzelt (yfinance MultiIndex temizleme)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            # İndikatör Hesaplamaları
            df['RSI'] = rsi_hesapla(df['Close'], 14)
            df['SMA20'] = df['Close'].rolling(window=20).mean()
            df['SMA50'] = df['Close'].rolling(window=50).mean()
            
            son_fiyat = df['Close'].iloc[-1]
            son_rsi = df['RSI'].iloc[-1]
            son_sma20 = df['SMA20'].iloc[-1]
            
            # Son 20 günün en yüksek seviyesi (Direnç/Kırılım bölgesi)
            en_yuksek_20g = df['High'].iloc[-21:-1].max()
            
            # --- FİLTRE KRİTERLERİ ---
            # 1. RSI henüz aşırı alımda değil (40 - 62 arası)
            rsi_uygun = 40 <= son_rsi <= 62
            
            # 2. Fiyat SMA20 üstünde (Pozitif Trend)
            trend_pozitif = son_fiyat > son_sma20
            
            # 3. Fiyat son 20 günün zirvesine yakın (%3 bandında) veya kırmaya çalışıyor
            kirilim_potansiyeli = son_fiyat >= (en_yuksek_20g * 0.97)
            
            if rsi_uygun and trend_pozitif and kirilim_potansiyeli:
                fırsat_hisseleri.append({
                    "Hisse": hisse.replace(".IS", ""),
                    "Son Fiyat": round(son_fiyat, 2),
                    "RSI (14)": round(son_rsi, 2),
                    "SMA20": round(son_sma20, 2),
                    "Durum": "Yataya Bağlamış / Kırılım Adayı"
                })
        except Exception as e:
            continue
            
    # Sonuçları Tablo Şeklinde Bas
    sonuc_df = pd.DataFrame(fırsat_hisseleri)
    if not sonuc_df.empty:
        print(sonuc_df.to_string(index=False))
    else:
        print("Kriterlere uyan hisse bulunamadı.")

if __name__ == "__main__":
    hisse_taramasi()
