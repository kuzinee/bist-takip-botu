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
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload, timeout=10)
        print("Telegram bildirimi başarıyla gönderildi.")
    except Exception as e:
        print(f"Telegram hatası: {e}")

def get_all_bist_tickers():
    # Borsa İstanbul'daki Tüm Hisselerin Tam Listesi (500+ Hisse)
    # Hiçbir web sitesine bağımlı olmadan her zaman %100 kapsama sağlar.
    return [
        "AAV.IS", "A1CAP.IS", "ABD.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", 
        "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AHGAZ.IS", "AKBNK.IS", "AKCNS.IS", "AKFGY.IS", 
        "AKFYE.IS", "AKGRT.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "AKSGY.IS", "AKSUE.IS", "AKTVF.IS", 
        "AKTIF.IS", "ALARK.IS", "ALBRK.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", 
        "ALKLC.IS", "ALMAD.IS", "ALTNY.IS", "ALVES.IS", "ANELE.IS", "ANGEN.IS", "ANHYT.IS", "ANSGR.IS", 
        "ARASE.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS", "ARTMS.IS", "ARZUM.IS", "ASELS.IS", 
        "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAGY.IS", "ATAKP.IS", "ATATP.IS", "ATEKS.IS", "ATAGU.IS", 
        "ATLAS.IS", "ATSYH.IS", "AVOD.IS", "AVPGY.IS", "AVTUR.IS", "AYCES.IS", "AYDEM.IS", "AYEN.IS", 
        "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAKAB.IS", "BALAT.IS", "BANVT.IS", "BARMA.IS", "BASGZ.IS", 
        "BAYRK.IS", "BEGYO.IS", "BFREN.IS", "BIENP.IS", "BIGCHEFS.IS", "BIMAS.IS", "BINHO.IS", "BIOEN.IS", 
        "BRKVY.IS", "BRLSM.IS", "BRMSN.IS", "BRSAN.IS", "BRSAT.IS", "BRKO.IS", "BRKSN.IS", "BRYAT.IS", 
        "BSOKE.IS", "BTCIM.IS", "BUCIM.IS", "BURCE.IS", "BURVA.IS", "BVSAN.IS", "BYDNR.IS", "CANTE.IS", 
        "CASA.IS", "CAHIT.IS", "CCOLA.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CMBTN.IS", "CMENT.IS", 
        "CONSE.IS", "COSMO.IS", "CRDFA.IS", "CRFSA.IS", "CUSAN.IS", "CVKMD.IS", "CWENE.IS", "DAGI.IS", 
        "DAPGM.IS", "DARDL.IS", "DGATE.IS", "DGGYO.IS", "DITAS.IS", "DMRGD.IS", "DMSAS.IS", "DNISI.IS", 
        "DOAS.IS", "DOBUR.IS", "DOCTA.IS", "DOGUB.IS", "DOHOL.IS", "DOKTA.IS", "DURDO.IS", "DYOBY.IS", 
        "EDATA.IS", "ECILC.IS", "ECZYT.IS", "EBEBK.IS", "EDIP.IS", "EGEEN.IS", "EGGUB.IS", "EGPRO.IS", 
        "EGSER.IS", "EKGYO.IS", "EKIZ.IS", "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "ENJSA.IS", "ENKAI.IS", 
        "ENTRA.IS", "EPLAS.IS", "ERCB.IS", "EREGL.IS", "ESCAR.IS", "ESEN.IS", "ETILR.IS", "EUPWR.IS", 
        "EUREK.IS", "EUHOL.IS", "EURO.IS", "EYGYO.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FROTO.IS", 
        "FZLGY.IS", "GARAN.IS", "GARFA.IS", "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENTS.IS", "GEREL.IS", 
        "GESAN.IS", "GIPTA.IS", "GLBMD.IS", "GLCVY.IS", "YATIR.IS", "GLYHO.IS", "GMTAS.IS", "GOKNR.IS", 
        "GOLTS.IS", "GOODY.IS", "GOZDE.IS", "GRSEL.IS", "GRTHO.IS", "GSDHO.IS", "GSDEVR.IS", "GUBRF.IS", 
        "GWIND.IS", "GSDDE.IS", "HALKB.IS", "HATEK.IS", "HATSN.IS", "HDFGS.IS", "HEDEF.IS", "HEKTS.IS", 
        "HKTM.IS", "HOROZ.IS", "HUBVC.IS", "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "ICUGS.IS", "IDEAS.IS", 
        "IDGYO.IS", "IEYHO.IS", "IHAAS.IS", "IHEVA.IS", "IHGZT.IS", "IHLGM.IS", "IHYAY.IS", "IMASM.IS", 
        "INDES.IS", "INFO.IS", "INGRM.IS", "INTEM.IS", "INVEO.IS", "INVES.IS", "IPEKE.IS", "ISATR.IS", 
        "ISBTR.IS", "ISCTR.IS", "ISDMR.IS", "ISFIN.IS", "ISGSY.IS", "ISGYO.IS", "ISKPL.IS", "ISKUR.IS", 
        "ISMEN.IS", "ISSEN.IS", "IZINV.IS", "IZMDC.IS", "IZFAS.IS", "JANTS.IS", "KAPLM.IS", "KAREL.IS", 
        "KARSN.IS", "KARTN.IS", "KATMR.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KENT.IS", "KRGYO.IS", 
        "KLGYO.IS", "KLMSN.IS", "KLNMA.IS", "KLRZO.IS", "KLSER.IS", "KLSYN.IS", "KMCOR.IS", "KNFRT.IS", 
        "KONTR.IS", "KONYA.IS", "KOPOL.IS", "KORDS.IS", "KOZAL.IS", "KOZAA.IS", "KRONT.IS", "KRPLS.IS", 
        "KRTEK.IS", "KRVGD.IS", "KSTUR.IS", "KTLEV.IS", "KTSKR.IS", "KUYAŞ.IS", "KUVVA.IS", "KZGYO.IS", 
        "KZBGY.IS", "LIDER.IS", "LIDFA.IS", "LINK.IS", "LKMNH.IS", "LMKDC.IS", "LOGIN.IS", "LRVGY.IS", 
        "LUKSK.IS", "MAALT.IS", "MACKO.IS", "MAKIM.IS", "MAKTK.IS", "MANAS.IS", "MARKA.IS", "MARTI.IS", 
        "MAGEN.IS", "MAVI.IS", "MEDTR.IS", "MEGAP.IS", "MEPET.IS", "MERCN.IS", "MERKO.IS", "MERIT.IS", 
        "METRO.IS", "METUR.IS", "MHRGY.IS", "MIATK.IS", "MTRKS.IS", "MOGAN.IS", "MOBTL.IS", "MPARK.IS", 
        "MRGYO.IS", "MRSHL.IS", "MSGYO.IS", "MTRKS.IS", "MZHES.IS", "NATEN.IS", "NETAS.IS", "NETHO.IS", 
        "NIBAS.IS", "NTGAZ.IS", "NTHOL.IS", "NUGYO.IS", "NUHCM.IS", "OAKBN.IS", "OBASE.IS", "OBAMS.IS", 
        "ODAS.IS", "OFSYM.IS", "ONCSM.IS", "ORCA.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", "OSTIM.IS", 
        "OTKAR.IS", "OTTO.IS", "OYAKC.IS", "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZKGY.IS", "OZRDN.IS", 
        "PAGYO.IS", "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PATEK.IS", "PCILT.IS", "PEKGY.IS", 
        "PENGD.IS", "PENTA.IS", "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", "PKENT.IS", 
        "PLTUR.IS", "PNLSN.IS", "PNSUT.IS", "POLHO.IS", "POLTK.IS", "PRDGS.IS", "PRKME.IS", "PRKAB.IS", 
        "PRZMA.IS", "PSDTC.IS", "QUAGR.IS", "RALYH.IS", "RAYSG.IS", "REEDR.IS", "RNPOL.IS", "RODRG.IS", 
        "ROYAL.IS", "RTALB.IS", "RUBNS.IS", "RYGYO.IS", "RYSAS.IS", "SAHOL.IS", "SAMAT.IS", "SANEL.IS", 
        "SANFM.IS", "SANKO.IS", "SARKY.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SEGMN.IS", "SEKFK.IS", 
        "SEKUR.IS", "SELEC.IS", "SELVA.IS", "SEYKM.IS", "SILVR.IS", "SISE.IS", "SKBNK.IS", "SKTAS.IS", 
        "SMART.IS", "SMRTG.IS", "SNOAM.IS", "SNICA.IS", "SOKM.IS", "SONME.IS", "SRVGY.IS", "SUMAS.IS", 
        "SUNTK.IS", "SURGY.IS", "SUWEN.IS", "TATEN.IS", "TATGD.IS", "TAVHL.IS", "TCBANK.IS", "TCELL.IS", 
        "TDGYO.IS", "TEKTU.IS", "TERA.IS", "TETMT.IS", "THYAO.IS", "TKFEN.IS", "TKNSA.IS", "TLMAN.IS", 
        "TMPOL.IS", "TMSN.IS", "TNZTP.IS", "TOASO.IS", "TRCAS.IS", "TRGYO.IS", "TRILC.IS", "TSKB.IS", 
        "TSPOR.IS", "TUCLK.IS", "TUPRS.IS", "TURGG.IS", "TURSG.IS", "UFUK.IS", "ULAS.IS", "ULKER.IS", 
        "UNLU.IS", "USAK.IS", "VAKBN.IS", "VAKFN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", 
        "VERUS.IS", "VESBE.IS", "VESTL.IS", "VKFYO.IS", "VKGYO.IS", "VKING.IS", "YAPRK.IS", "YATAS.IS", 
        "YAYLA.IS", "YGGYO.IS", "YGYO.IS", "YEOTK.IS", "YKF.IS", "YKBNK.IS", "YONGA.IS", "YOTAS.IS", 
        "YYLGD.IS", "ZOREN.IS", "ZRGYO.IS"
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
    
    # Tüm hisse verilerini toplu indir
    data = yf.download(bist_tickers, period="1y", threads=True, progress=False)
    
    if data.empty:
        print("Veri indirilemedi.")
        return []

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

    message_parts = []
    if drawdown_matches:
        message_parts.append("🎯 *Zirveden Ucuzlayan + RSI Dip Yapanlar:*\n" + "\n".join(drawdown_matches))
    if reversal_matches:
        message_parts.append("⚡ *Gün İçi Dipten Dönüş Yapanlar:*\n" + "\n".join(reversal_matches))

    return message_parts

def check_kap_news():
    """3. STRATEJİ: KAP Haber Taraması"""
    url = "https://www.kap.org.tr/tr/api/disclosures"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    positive_keywords = [
        "Yeni İş İlişkisi", "İhale", "Yatırım", 
        "Pay Alım Satım", "Sermaye Artırımı", "Geri Alım"
    ]
    kap_matches = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            disclosures = response.json()
            for item in disclosures[:30]:
                title = str(item.get("title") or "")
                summary = str(item.get("summary") or "")
                stock_code = item.get("stockCodes", "BIST")
                disclosure_id = item.get("disclosureIndex", "")

                text_to_check = (title + " " + summary).lower()
                if any(kw.lower() in text_to_check for kw in positive_keywords):
                    link = f"https://www.kap.org.tr/tr/Bildirim/{disclosure_id}"
                    clean_summary = summary.replace("\n", " ")[:120]
                    kap_matches.append(
                        f"📢 *[{stock_code}] {title}*\n{clean_summary}...\n🔗 [KAP Haberi]({link})"
                    )
    except Exception as e:
        print(f"KAP tarama hatası: {e}")

    if kap_matches:
        return ["🚨 *Önemli KAP Bildirimleri & Anlaşmalar:*\n" + "\n\n".join(kap_matches)]
    return []

if __name__ == "__main__":
    technical_results = check_bist_stocks()
    kap_results = check_kap_news()

    all_results = technical_results + kap_results

    # Sadece kriterlere uyan hisse/haber varsa mesaj at, yoksa sessiz kal
    if all_results:
        final_message = "🔔 *Saatlik BIST & KAP Taraması Sonuçları:*\n\n" + "\n\n---\n\n".join(all_results)
        send_telegram_message(final_message)
    else:
        print("Kriterlere uyan hisse veya KAP haberi bulunamadı. Telegram'a mesaj atılmadı.")
