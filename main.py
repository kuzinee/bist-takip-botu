import os
import requests
import yfinance as yf
import pandas as pd

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("HATA: TELEGRAM_TOKEN veya CHAT_ID eksik.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # Telegram'ın 4096 karakter sınırına takılmamak için mesajı parçalara bölme
    for i in range(0, len(message), 4000):
        chunk = message[i:i+4000]
        payload = {
            "chat_id": CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        try:
            requests.post(url, data=payload, timeout=10)
            print("Telegram bildirimi gönderildi.")
        except Exception as e:
            print(f"Telegram hatası: {e}")

def get_all_bist_tickers():
    return [
        "AAV.IS", "A1CAP.IS", "ABD.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", 
        "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", 
        "AKFYE.IS", "AKGRT.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "AKSGY.IS", "AKSUE.IS", "ALARK.IS", 
        "ALBRK.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALTNY.IS", "ARCLK.IS", 
        "ARDYZ.IS", "ASELS.IS", "ASTOR.IS", "BIMAS.IS", "BRSAN.IS", "CCOLA.IS", "CWENE.IS", "DOAS.IS", 
        "EGEEN.IS", "EKGYO.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS", "EUPWR.IS", "FROTO.IS", "GARAN.IS", 
        "GESAN.IS", "GUBRF.IS", "HEKTS.IS", "ISCTR.IS", "KCAER.IS", "KCHOL.IS", "KONTR.IS", "KOZAL.IS", 
        "MIATK.IS", "ODAS.IS", "OTKAR.IS", "OYAKC.IS", "PETKM.IS", "PGSUS.IS", "REEDR.IS", "SAHOL.IS", 
        "SASA.IS", "SISE.IS", "SKBNK.IS", "SMRTG.IS", "SOKM.IS", "TCELL.IS", "THYAO.IS", "TKFEN.IS", 
        "TOASO.IS", "TUPRS.IS", "VAKBN.IS", "VESBE.IS", "VESTL.IS", "YKBNK.IS"
    ]

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
    print(f"Toplam {len(bist_tickers)} hisse taranıyor...")
    
    try:
        data = yf.download(bist_tickers, period="6m", interval="1d", group_by='ticker', threads=True, progress=False)
    except Exception as e:
        print(f"Veri indirme hatası: {e}")
        return []

    drawdown_matches = []
    reversal_matches = []

    for ticker in bist_tickers:
        try:
            if ticker not in data or data[ticker].empty:
                continue
                
            df_stock = data[ticker].dropna()
            if len(df_stock) < 30:
                continue

            close_series = df_stock["Close"]
            last_price = close_series.iloc[-1]
            peak_price = close_series.max()
            drawdown = ((last_price - peak_price) / peak_price) * 100
            
            rsi_series = calculate_rsi(close_series)
            last_rsi = rsi_series.iloc[-1]

            symbol = ticker.replace(".IS", "")

            # 1. Strateji: Zirveden Düşüş + RSI Dip
            if -35 <= drawdown <= -20 and last_rsi <= 35:
                drawdown_matches.append(
                    f"• *{symbol}*: Zirveden %{drawdown:.1f} | RSI: {last_rsi:.1f} ({last_price:.2f} TL)"
                )

            # 2. Strateji: Gün İçi Dipten Dönüş
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
                    reversal_matches.append(
                        f"⚡ *{symbol}*: Dipten %{reversal_pct:.1f} Sıçradı ({close_p:.2f} TL)"
                    )

        except Exception:
            continue

    message_parts = []
    if drawdown_matches:
        message_parts.append("🎯 *Zirveden Ucuzlayan + RSI Dip Yapanlar:*\n" + "\n".join(drawdown_matches))
    if reversal_matches:
        message_parts.append("⚡ *Gün İçi Dipten Dönüş Yapanlar:*\n" + "\n".join(reversal_matches))

    return message_parts

def check_kap_news():
    url = "https://www.kap.org.tr/tr/api/disclosures"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    positive_keywords = ["Yeni İş İlişkisi", "İhale", "Yatırım", "Pay Alım Satım", "Sermaye Artırımı", "Geri Alım"]
    kap_matches = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200 and response.text.startswith('['):
            disclosures = response.json()
            for item in disclosures[:20]:
                title = str(item.get("title") or "")
                summary = str(item.get("summary") or "")
                stock_code = item.get("stockCodes", "BIST")
                disclosure_id = item.get("disclosureIndex", "")

                text_to_check = (title + " " + summary).lower()
                if any(kw.lower() in text_to_check for kw in positive_keywords):
                    link = f"https://www.kap.org.tr/tr/Bildirim/{disclosure_id}"
                    clean_summary = summary.replace("\n", " ")[:100]
                    kap_matches.append(
                        f"📢 *[{stock_code}] {title}*\n{clean_summary}...\n🔗 [KAP Haberi]({link})"
                    )
    except Exception as e:
        print(f"KAP tarama hatası: {e}")

    if kap_matches:
        return ["🚨 *Önemli KAP Bildirimleri:*\n" + "\n\n".join(kap_matches)]
    return []

if __name__ == "__main__":
    technical_results = check_bist_stocks()
    kap_results = check_kap_news()

    all_results = technical_results + kap_results

    # Sadece belirlenen kriterlere uyan hisse veya KAP haberi varsa Telegram'a mesaj gönderir
    if all_results:
        final_message = "🔔 *Saatlik BIST & KAP Taraması Sonuçları:*\n\n" + "\n\n---\n\n".join(all_results)
        send_telegram_message(final_message)
    else:
        print("Kriterlere uyan hisse veya KAP haberi bulunamadı. Telegram'a mesaj atılmadı.")
