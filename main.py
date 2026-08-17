import os
import requests
import yfinance as yf
import pandas as pd

# ==============================================================================
# 📌 ÖZEL TAKİP LİSTENİZ (HER TARAMADA EN ÜSTTE ANLIK FİYATI BİLDİRİLECEK HİSSELER)
# Hisse kodlarının sonuna ".IS" ekleyerek yazabilirsiniz.
# ==============================================================================
SPECIAL_WATCHLIST = [
    "MIATK.IS",
    "ARDYZ.IS"
]

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

def check_special_watchlist():
    if not SPECIAL_WATCHLIST:
        return []
    
    print("Özel takip listesindeki hisselerin fiyatları çekiliyor...")
    matches = []
    
    try:
        data = yf.download(SPECIAL_WATCHLIST, period="5d", interval="1m", group_by='ticker', threads=True, progress=False)
        
        for ticker in SPECIAL_WATCHLIST:
            try:
                symbol = ticker.replace(".IS", "")
                
                if len(SPECIAL_WATCHLIST) == 1:
                    df_stock = data.dropna()
                else:
                    if ticker not in data or data[ticker].empty:
                        continue
                    df_stock = data[ticker].dropna()

                if df_stock.empty:
                    continue

                last_price = df_stock["Close"].iloc[-1]
                
                daily_data = yf.Ticker(ticker).history(period="2d")
                if len(daily_data) >= 2:
                    prev_close = daily_data["Close"].iloc[-2]
                    change_pct = ((last_price - prev_close) / prev_close) * 100
                    change_str = f" (%{change_pct:+.2f})"
                else:
                    change_str = ""

                matches.append(f"• *{symbol}*: {last_price:.2f} TL{change_str}")
            except Exception as e:
                print(f"{ticker} fiyatı çekilemedi: {e}")
                continue
    except Exception as e:
        print(f"Özel liste veri çekme hatası: {e}")

    if matches:
        return ["📌 *Özel Takip Listesi Anlık Durum:*\n" + "\n".join(matches)]
    return []

def get_all_bist_tickers():
    # Borsa İstanbul Tüm Hisseler (500+ Hisse Tam Liste)
    return [
        "AAV.IS", "A1CAP.IS", "ABD.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", 
        "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", 
        "AKFYE.IS", "AKGRT.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "AKSGY.IS", "AKSUE.IS", "ALARK.IS", 
        "ALBRK.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALTNY.IS", "ALVES.IS", 
        "ANELE.IS", "ANGEN.IS", "ANHYT.IS", "ANSGR.IS", "ARASE.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", 
        "ARSAN.IS", "ARTMS.IS", "ARZUM.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAGY.IS", 
        "ATAKP.IS", "ATATP.IS", "ATEKS.IS", "ATLAS.IS", "ATSYH.IS", "AVOD.IS", "AVPGY.IS", "AVTUR.IS", 
        "AYCES.IS", "AYDEM.IS", "AYEN.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAKAB.IS", "BALAT.IS", 
        "BANVT.IS", "BARMA.IS", "BASGZ.IS", "BAYRK.IS", "BEGYO.IS", "BFREN.IS", "BIENP.IS", "BIGCHEFS.IS", 
        "BIMAS.IS", "BINHO.IS", "BIOEN.IS", "BRKVY.IS", "BRLSM.IS", "BRMSN.IS", "BRSAN.IS", "BRSAT.IS", 
        "BRKSN.IS", "BRYAT.IS", "BSOKE.IS", "BTCIM.IS", "BUCIM.IS", "BURCE.IS", "BURVA.IS", "BVSAN.IS", 
        "BYDNR.IS", "CANTE.IS", "CASA.IS", "CCOLA.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CMBTN.IS", 
        "CMENT.IS", "CONSE.IS", "COSMO.IS", "CRDFA.IS", "CRFSA.IS", "CUSAN.IS", "CVKMD.IS", "CWENE.IS", 
        "DAGI.IS", "DAPGM.IS", "DARDL.IS", "DGATE.IS", "DGGYO.IS", "DITAS.IS", "DMRGD.IS", "DMSAS.IS", 
        "DNISI.IS", "DOAS.IS", "DOBUR.IS", "DOCTA.IS", "DOGUB.IS", "DOHOL.IS", "DOKTA.IS", "DURDO.IS", 
        "DYOBY.IS", "EDATA.IS", "ECILC.IS", "ECZYT.IS", "EBEBK.IS", "EDIP.IS", "EGEEN.IS", "EGGUB.IS", 
        "EGPRO.IS", "EGSER.IS", "EKGYO.IS", "EKIZ.IS", "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "ENJSA.IS", 
        "ENKAI.IS", "ENTRA.IS", "EPLAS.IS", "ERCB.IS", "EREGL.IS", "ESCAR.IS", "ESEN.IS", "ETILR.IS", 
        "EUPWR.IS", "EUREK.IS", "EUHOL.IS", "EURO.IS", "EYGYO.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", 
        "FROTO.IS", "FZLGY.IS", "GARAN.IS", "GARFA.IS", "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENTS.IS", 
        "GEREL.IS", "GESAN.IS", "GIPTA.IS", "GLBMD.IS", "GLCVY.IS", "GLYHO.IS", "GMTAS.IS", "GOKNR.IS", 
        "GOLTS.IS", "GOODY.IS", "GOZDE.IS", "GRSEL.IS", "GRTHO.IS", "GSDHO.IS", "GUBRF.IS", "GWIND.IS", 
        "HALKB.IS", "HATEK.IS", "HATSN.IS", "HDFGS.IS", "HEDEF.IS", "HEKTS.IS", "HKTM.IS", "HOROZ.IS", 
        "HUBVC.IS", "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "IDEAS.IS", "IDGYO.IS", "IEYHO.IS", "IHAAS.IS", 
        "IHEVA.IS", "IHGZT.IS", "IHLGM.IS", "IHYAY.IS", "IMASM.IS", "INDES.IS", "INFO.IS", "INGRM.IS", 
        "INTEM.IS", "INVEO.IS", "INVES.IS", "IPEKE.IS", "ISCTR.IS", "ISDMR.IS", "ISFIN.IS", "ISGSY.IS", 
        "ISGYO.IS", "ISKPL.IS", "ISMEN.IS", "ISSEN.IS", "IZMDC.IS", "JANTS.IS", "KAPLM.IS", "KAREL.IS", 
        "KARSN.IS", "KARTN.IS", "KATMR.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KENT.IS", "KRGYO.IS", 
        "KLGYO.IS", "KLMSN.IS", "KLNMA.IS", "KLRZO.IS", "KLSER.IS", "KLSYN.IS", "KNFRT.IS", "KONTR.IS", 
        "KONYA.IS", "KOPOL.IS", "KORDS.IS", "KOZAL.IS", "KOZAA.IS", "KRONT.IS", "KRPLS.IS", "KRTEK.IS", 
        "KRVGD.IS", "KSTUR.IS", "KTLEV.IS", "KTSKR.IS", "KUYAŞ.IS", "KZGYO.IS", "KZBGY.IS", "LIDER.IS", 
        "LIDFA.IS", "LINK.IS", "LKMNH.IS", "LMKDC.IS", "LRVGY.IS", "LUKSK.IS", "MAALT.IS", "MACKO.IS", 
        "MAKIM.IS", "MAKTK.IS", "MANAS.IS", "MARKA.IS", "MARTI.IS", "MAGEN.IS", "MAVI.IS", "MEDTR.IS", 
        "MEGAP.IS", "MEPET.IS", "MERCN.IS", "MERKO.IS", "MERIT.IS", "METRO.IS", "METUR.IS", "MHRGY.IS", 
        "MIATK.IS", "MTRKS.IS", "MOGAN.IS", "MOBTL.IS", "MPARK.IS", "MRGYO.IS", "MRSHL.IS", "MSGYO.IS", 
        "NATEN.IS", "NETAS.IS", "NETHO.IS", "NIBAS.IS", "NTGAZ.IS", "NTHOL.IS", "NUGYO.IS", "NUHCM.IS", 
        "OBASE.IS", "OBAMS.IS", "ODAS.IS", "OFSYM.IS", "ONCSM.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", 
        "OSTIM.IS", "OTKAR.IS", "OTTO.IS", "OYAKC.IS", "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZKGY.IS", 
        "OZRDN.IS", "PAGYO.IS", "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PATEK.IS", "PCILT.IS", 
        "PEKGY.IS", "PENGD.IS", "PENTA.IS", "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", 
        "PKENT.IS", "PLTUR.IS", "PNLSN.IS", "PNSUT.IS", "POLHO.IS", "POLTK.IS", "PRDGS.IS", "PRKME.IS", 
        "PRKAB.IS", "PRZMA.IS", "PSDTC.IS", "QUAGR.IS", "RALYH.IS", "RAYSG.IS", "REEDR.IS", "RNPOL.IS", 
        "RODRG.IS", "RTALB.IS", "RUBNS.IS", "RYGYO.IS", "RYSAS.IS", "SAHOL.IS", "SAMAT.IS", "SANEL.IS", 
        "SANFM.IS", "SANKO.IS", "SARKY.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SEGMN.IS", "SEKFK.IS", 
        "SEKUR.IS", "SELEC.IS", "SELVA.IS", "SEYKM.IS", "SILVR.IS", "SISE.IS", "SKBNK.IS", "SKTAS.IS", 
        "SMART.IS", "SMRTG.IS", "SNICA.IS", "SOKM.IS", "SONME.IS", "SRVGY.IS", "SUMAS.IS", "SUNTK.IS", 
        "SURGY.IS", "SUWEN.IS", "TATEN.IS", "TATGD.IS", "TAVHL.IS", "TCELL.IS", "TDGYO.IS", "TEKTU.IS", 
        "TERA.IS", "TETMT.IS", "THYAO.IS", "TKFEN.IS", "TKNSA.IS", "TLMAN.IS", "TMPOL.IS", "TMSN.IS", 
        "TNZTP.IS", "TOASO.IS", "TRCAS.IS", "TRGYO.IS", "TRILC.IS", "TSKB.IS", "TSPOR.IS", "TUCLK.IS", 
        "TUPRS.IS", "TURGG.IS", "TURSG.IS", "UFUK.IS", "ULAS.IS", "ULKER.IS", "UNLU.IS", "USAK.IS", 
        "VAKBN.IS", "VAKFN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS", "VESBE.IS", 
        "VESTL.IS", "VKFYO.IS", "VKGYO.IS", "VKING.IS", "YAPRK.IS", "YATAS.IS", "YAYLA.IS", "YGGYO.IS", 
        "YGYO.IS", "YEOTK.IS", "YKBNK.IS", "YONGA.IS", "YYLGD.IS", "ZOREN.IS", "ZRGYO.IS"
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

            # 1. STRATEJİ: Zirveden Düşüş + RSI Dip
            if -35 <= drawdown <= -20 and last_rsi <= 35:
                drawdown_matches.append(
                    f"• *{symbol}*: Zirveden %{drawdown:.1f} | RSI: {last_rsi:.1f} ({last_price:.2f} TL)"
                )

            # 2. STRATEJİ: Son 3-4 Günde Dipten Yönünü Yukarı Çevirenler
            recent_closes = close_series.tail(4).values
            recent_volumes = df_stock['Volume'].tail(4).values
            avg_vol = df_stock['Volume'].tail(20).mean()

            # Koşullar: %3+ prim, yeşil gün çoğunluğu, hacim teyidi ve EMA5 kırılımı
            four_day_return = ((recent_closes[-1] - recent_closes[0]) / recent_closes[0]) * 100
            green_days = sum(1 for i in range(1, len(recent_closes)) if recent_closes[i] > recent_closes[i-1])
            volume_confirmed = recent_volumes[-1] > avg_vol
            ema5 = close_series.ewm(span=5, adjust=False).mean().iloc[-1]
            above_ema5 = last_price > ema5

            if four_day_return >= 3.0 and green_days >= 2 and volume_confirmed and above_ema5:
                reversal_matches.append(
                    f"🚀 *{symbol}*: Son 4 Günde %{four_day_return:.1f} Yükseliş Başlattı (Hacim Destekli, {last_price:.2f} TL)"
                )

        except Exception:
            continue

    message_parts = []
    if drawdown_matches:
        message_parts.append("🎯 *Zirveden Ucuzlayan + RSI Dip Yapanlar:*\n" + "\n".join(drawdown_matches))
    if reversal_matches:
        message_parts.append("🚀 *Dipten Yönünü Yukarı Çevirenler (Son 3-4 Gün Yükseliş Trendi):*\n" + "\n".join(reversal_matches))

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
    special_results = check_special_watchlist()
    technical_results = check_bist_stocks()
    kap_results = check_kap_news()

    all_results = special_results + technical_results + kap_results

    if all_results:
        final_message = "🔔 *Saatlik BIST & KAP Taraması Sonuçları:*\n\n" + "\n\n---\n\n".join(all_results)
    else:
        final_message = "ℹ️ *BIST & KAP Taraması Tamamlandı*\nBu taramada belirlenen kriterlere uyan teknik hisse sinyali veya önemli KAP haberi bulunamadı."

    send_telegram_message(final_message)
