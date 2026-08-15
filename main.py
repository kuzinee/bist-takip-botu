import os
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Mesaj gönderilemedi: {e}")

def get_all_bist_tickers():
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        select_box = soup.find("select", {"id": "ddlHisseTek"})
        tickers = []
        if select_box:
            for option in select_box.find_all("option"):
                code = option.get("value")
                if code and code.strip():
                    tickers.append(f"{code.strip()}.IS")
        return tickers
    except Exception as e:
        print(f"Hisse listesi çekilemedi: {e}")
        return []

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
    if not bist_tickers:
        return

    data = yf.download(bist_tickers, period="1y", threads=True, progress=False)
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
