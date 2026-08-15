import os
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("HATA: TELEGRAM_TOKEN veya CHAT_ID eksik.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload, timeout=10)
        print("Telegram bildirimi gönderildi.")
    except Exception as e:
        print(f"Telegram hatası: {e}")

def get_all_bist_tickers():
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx"
    headers = {"User-Agent": "Mozilla/5.0"}
    tickers = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        select_box = soup.find("select", {"id": "ddlHisseTek"})
        if select_box:
            for option in select_box.find_all("option"):
                code = option.get("value")
                if code and code.strip():
                    tickers.append(f"{code.strip()}.IS")
    except Exception as e:
        print(f"Liste çekme hatası: {e}")

    if not tickers:
        tickers = [
            "THYAO.IS", "GARAN.IS", "ASELS.IS", "EREGL.IS", "SISE.IS", 
            "AKBNK.IS", "KCHOL.IS", "TUPRS.IS", "BIMAS.IS", "SAHOL.IS",
            "EKGYO.IS", "PGSUS.IS", "YKBNK.IS", "ISCTR.IS", "HEKTS.IS"
        ]
    return tickers

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def check_bist_stocks():
    bist_tickers = get_all_bist_tickers()
    data = yf.download(bist_tickers, period="1y", threads=True, progress=False)
    
    if data.empty:
        print("Veri indirilemedi.")
        return

    drawdown_matches = []
    reversal_matches = []

    for ticker in bist_tickers:
        try:
            # 1. STRATEJİ: Zirveden Düşüş + RSI Dip
            close_series = data["Close"][ticker].dropna()
            if len(close_series) >= 30:
                last_price = close_series.iloc[-1]
                peak_price = close_series.max()
                drawdown = ((last_price - peak_price) / peak_price) * 100
                rsi_series = calculate_rsi(close_series)
                last_rsi = rsi_series.iloc[-1]

                if -35 <= drawdown <= -20 and last_rsi <= 35:
                    symbol = ticker.replace(".IS", "")
                    drawdown_matches.append(
                        f"• *{symbol}*: Zirveden %{drawdown:.1f} | RSI: {last_rsi:.1f} ({last_price:.2f} TL)"
                    )

            # 2. STRATEJİ: Gün İçi Dipten Dönüş / Sıçrama
            df_stock = pd.DataFrame({
                'Open': data['Open'][ticker],
                'High': data['High'][ticker],
                'Low': data['Low'][ticker],
                'Close': data['Close'][ticker],
                'Volume': data['Volume'][ticker]
            }).dropna()

            if len(df_stock) >= 20:
                today = df_stock.iloc[-1]
                open_p, high_p, low_p, close_p = today['Open'], today['High'], today['Low'], today['Close']
                vol_today = today['Volume']
                avg_vol = df_stock['Volume'].tail(20).mean()

                day_range = high_p - low_p
                if day_range > 0:
                    lower_tail = min(open_p, close_p) - low_p
                    tail_ratio = lower_tail / day_range
                    reversal_pct = ((close_p - low_p) / low_p) * 100

                    if tail_ratio >= 0.55 and reversal_pct >= 2.5 and vol_today > avg_vol:
                        symbol = ticker.replace(".IS", "")
                        reversal_matches.append(
                            f"⚡ *{symbol}*: Dipten %{reversal_pct:.1f} Sıçradı ({close_p:.2f} TL)"
                        )

        except Exception:
            continue

    # Raporlama
    message_parts = []
    if drawdown_matches:
        message_parts.append("🎯 *Zirveden Ucuzlayan + RSI Dip Yapanlar:*\n" + "\n".join(drawdown_matches))
    if reversal_matches:
        message_parts.append("⚡ *Gün İçi Dipten Dönüş Yapanlar:*\n" + "\n".join(reversal_matches))

    if not message_parts:
        final_message = "ℹ️ Bugün hiçbir kriterimize (Zirve Düşüşü veya Gün İçi Dönüş) uyan hisse bulunamadı."
    else:
        final_message = "\n\n---\n\n".join(message_parts)

    send_telegram_message(final_message)

if __name__ == "__main__":
    check_bist_stocks()
