import time
import requests
from bs4 import BeautifulSoup

# --- CONFIGURAZIONE ---
# Inserisci il token del tuo bot Telegram (lo ottieni da @BotFather)
TOKEN_TELEGRAM = "IL_TUO_TELEGRAM_BOT_TOKEN"
# Inserisci il tuo ID Chat di Telegram (lo ottieni da @userinfobot)
CHAT_ID_UTENTE = "IL_TUO_CHAT_ID"

# L'URL della pagina del prodotto da monitorare (Esempio generico)
URL_PRODOTTO = "https://www.esempio-ecommerce.com/prodotto-tech"
# Il prezzo sotto il quale vuoi ricevere la notifica
PREZZO_SOGLIA = 150.00


def ottieni_prezzo(url):
    """Svolge lo scraping della pagina per trovare il prezzo."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        risposta = requests.get(url, headers=headers)
        soup = BeautifulSoup(risposta.text, "html.parser")

        # NOTA: Questa classe cambia a seconda del sito web.
        # Devi ispezionare la pagina del sito e trovare la classe corretta del prezzo.
        tag_prezzo = soup.find("span", class_="price-value")

        if tag_prezzo:
            # Pulisce la stringa del prezzo e la converte in float
            testo_prezzo = (
                tag_prezzo.text.replace("€", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )
            return float(testo_prezzo)
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")
    return None


def invia_notifica_telegram(messaggio):
    """Invia un messaggio di testo al tuo bot Telegram."""
    url_api = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID_UTENTE, "text": messaggio}
    requests.post(url_api, json=payload)


def avvia_monitoraggio():
    print("Monitoraggio avviato...")
    while True:
        prezzo_attuale = ottieni_prezzo(URL_PRODOTTO)

        if prezzo_attuale:
            print(f"Prezzo controllato: {prezzo_attuale}€")

            if prezzo_attuale <= PREZZO_SOGLIA:
                messaggio = f"🚨 SCONTO! Il prodotto è sceso a {prezzo_attuale}€!\nLink: {URL_PRODOTTO}"
                invia_notifica_telegram(messaggio)
                print("Notifica inviata! Metto in pausa il monitoraggio per 12 ore.")
                time.sleep(43200)  # Evita di spammare se il prezzo resta basso

        # Controlla il prezzo ogni ora (3600 secondi)
        time.sleep(3600)


if __name__ == "__main__":
    avvia_monitoraggio()
