import os
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("HATA: TELEGRAM_TOKEN veya CHAT_ID tanımlı değil!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print("Telegram bildirimi başarıyla gönderildi.")
        else:
            print(f"Telegram Hatası ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"Telegram bağlantı hatası: {e}")

def get_all_bist_tickers():
    print("İş Yatırım üzerinden hisse listesi çekiliyor...")
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    tickers = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        select_box = soup.find("select", {"id": "ddlHisseTek"})
        if select_box:
            for option in select_box.find_all("option"):
                code = option.get("value")
                if code and code.strip():
                    tickers.append(f"{code.strip()}.IS")
    except Exception as e:
        print(f"İş Yatırım bağlantı hatası: {e}")

    # İş Yatırım engellenirse yedek BIST 100/Likit listesi
    if not tickers:
        print("İş Yatırım'dan liste çekilemedi. Yedek hisse listesi devreye alınıyor...")
        tickers = [
            "THYAO.IS", "GARAN.IS", "ASELS.IS", "EREGL.IS", "SISE.IS", 
            "AKBNK.IS", "KCHOL.IS", "TUPRS.IS", "BIMAS.IS", "SAHOL.IS",
            "EKGYO.IS", "PGSUS.IS", "YKBNK.IS", "ISCTR.IS", "HEKTS.IS",
            "KORDS.IS", "SASA.IS", "PETKM.IS", "ASTOR.IS", "KONTR.IS"
        ]

    print(f"Toplam {len(tickers)} adet hisse taranacak.")
    return tickers

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def check_bist_stocks():
    bist_tickers = get_all_bist_tickers()
    
    print("Fiyat verileri indiriliyor...")
    data = yf.download(bist_tickers, period="1y", threads=True, progress=False)
    
    if data.empty or "Close" not in data:
        print("HATA: Fiyat verisi alınamadı.")
        send_telegram_message("⚠️ Fiyat verileri çekilemedi.")
        return

    df = data["Close"]
    matched_stocks = []

    for ticker in df.columns:
        series = df[ticker].dropna()
        if len(series) < 30:
            continue

        last_price = series.iloc[-1]
        peak_price = series.max()
        drawdown = ((last_price - peak_price) / peak_price) * 100
        
        rsi_series = calculate_rsi(series)
        last_rsi = rsi_series.iloc[-1]

        if -35 <= drawdown <= -20 and last_rsi <= 35:
            symbol = ticker.replace(".IS", "")
            matched_stocks.append(
                f"• *{symbol}*: Zirveden %{drawdown:.1f} | RSI: {last_rsi:.1f} (Fiyat: {last_price:.2f} TL)"
            )

    print(f"Kriterlere uyan hisse sayısı: {len(matched_stocks)}")

    if matched_stocks:
        message = (
            f"🎯 *Zirveden Ucuzlayan + RSI Dip Yapan Hisseler ({len(matched_stocks)} Adet):*\n\n"
            + "\n".join(matched_stocks)
        )
    else:
        message = "ℹ️ Kriterlere uyan (Zirveden %20-%35 düşmüş ve RSI < 35) hisse bulunamadı."

    send_telegram_message(message)

if __name__ == "__main__":
    check_bist_stocks()
