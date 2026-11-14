# Client-HTTP-con-Socket

Client HTTP in Python: costruisce a mano una richiesta HTTP/1.1 con
un socket TCP, per mostrare come funziona davvero il protocollo.

> **L'idea da portarsi a casa:** un browser, alla fine, apre una connessione
> TCP e ci scrive del testo.

---

## La lezione interattiva

Apri **[`index.html`](index.html)**: è la pagina che accompagna la lezione, con
la richiesta smontata pezzo per pezzo, un simulatore, le domande
dell'esercizio, il quiz finale e il glossario.

Nel Codespace si apre così (poi clicca **Apri nel browser** nell'avviso che compare):

```bash
python3 -m http.server 8000
```

Sul tuo computer basta un doppio clic sul file.

| File | A cosa serve |
|---|---|
| `index.html` | La lezione interattiva |
| `client_http.py` | Lo stesso client, con argomenti e lettura completa della risposta |

## Indice

1. [Prima di iniziare](#1-prima-di-iniziare)
2. [Dimostrazione](#2-dimostrazione)
3. [Esercizio](#3-esercizio)
4. [Spiegazione](#4-spiegazione)
5. [Problemi frequenti](#5-problemi-frequenti)

---

## 1. Prima di iniziare

Serve solo **Python 3** e, per il confronto, **curl**. Nel Codespace ci sono
già tutti e due. Lo script usa solo la libreria standard: non c'è niente da
installare.

**Con GitHub Codespaces (consigliato)**

1. Su questa pagina clicca **Code → Codespaces → Create codespace on main**.
2. Aspetta che si apra l'editor, poi apri il terminale (**Terminale → Nuovo terminale**).
3. Controlla che tutto funzioni:

   ```bash
   python3 --version
   ```

   ```bash
   curl --version
   ```

**Sul tuo computer**

```bash
git clone https://github.com/pwnAtl4nt1s/Client-HTTP-con-Socket.git
```

```bash
cd Client-HTTP-con-Socket
```

Su Windows, se `python3` non viene trovato, usa `python` (o `py`) al suo posto.

### Com'è fatto il comando

```
python3 client_http.py [host] [percorso] [opzioni]
```

| Parte | Esempio | Se la ometti |
|---|---|---|
| `host` | `example.com` | `example.com` |
| `percorso` | `/index.html` | `/` |
| opzione `--senza-host` | | La riga `Host` viene inviata |
| opzione `--senza-riga-vuota` | | La riga vuota finale viene inviata |

Le opzioni vanno **dopo** host e percorso.

---

## 2. Dimostrazione

### 2.1 Lo script

```bash
python3 client_http.py
```

Lo script fa quattro cose:

1. **costruisce a mano** la richiesta: una riga `GET / HTTP/1.1`, la riga `Host`
   e una riga vuota;
2. la **stampa con `repr()`**, così si vedono i caratteri `\r\n` che di solito sono invisibili;
3. apre un **socket TCP** verso `example.com`, **porta 80**, e ci scrive il testo;
4. stampa la **risposta** e, in fondo, **come ha capito che era finita**.

L'output ha tre parti:

```
=== RICHIESTA (i \r\n sono visibili) ===
'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n'

=== RISPOSTA ===
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Transfer-Encoding: chunked
...

<!doctype html>
...

=== Come ho capito che la risposta era finita: Transfer-Encoding: chunked, 1 pezzo e poi il pezzo finale lungo 0 ===
```

Con altri siti l'ultima riga cambia. Per esempio `neverssl.com` dichiara la
lunghezza:

```
=== Come ho capito che la risposta era finita: Content-Length: 3961 byte ===
```

### 2.2 La stessa richiesta con curl

```bash
curl -v http://example.com/
```

Nell'output di `curl -v`:

- le righe con **`>`** sono la richiesta inviata da curl;
- le righe con **`<`** sono le intestazioni della risposta;
- le righe con **`*`** sono commenti di curl (connessione, indirizzo IP…).

Confrontale con l'output dello script: il testo è lo stesso. curl aggiunge solo
qualche intestazione in più, come `User-Agent` e `Accept`.

---

## 3. Esercizio

Per ogni prova: **lancia il comando, guarda la prima riga della risposta e
l'ultima riga dell'output** ("Come ho capito che la risposta era finita"), poi
rispondi alle domande. Scrivi le risposte su un foglio o in un file di testo.

### Prova A – Cambia il percorso

```bash
python3 client_http.py example.com /pagina-che-non-esiste
```

- Qual è la prima riga della risposta? Che cosa significa il numero?
- La connessione TCP è riuscita? Come fai a saperlo?

### Prova B – Cambia l'host

Serve un sito ancora raggiungibile in `http://` (senza la "s"), per esempio:

```bash
python3 client_http.py neverssl.com /
```

```bash
python3 client_http.py httpforever.com /
```

Prova anche un sito che accetta solo `https`, per esempio `www.wikipedia.org` o `github.com`.

- Che codice di risposta ottieni da questi siti? Cerca l'intestazione `Location`:
  dove ti stanno mandando, e perché?
- La fine della risposta è stata capita sempre nello stesso modo?

### Prova C – Togli la riga `Host`

```bash
python3 client_http.py example.com / --senza-host
```

- Che cosa cambia nella richiesta stampata?
- Che cosa risponde il server? Perché, secondo te, la riga `Host` è necessaria?

### Prova D – Togli la riga vuota finale

```bash
python3 client_http.py example.com / --senza-riga-vuota
```

Attenzione: lo script resterà fermo qualche secondo. È normale, fa parte della prova.

- Quanto tempo passa prima che succeda qualcosa? Che cosa stampa lo script alla fine?
- Che cosa sta aspettando il server?

### Prova E (facoltativa) – Confronto con curl

```bash
curl -v http://example.com/pagina-che-non-esiste
```

```bash
curl -v -H "Host:" http://example.com/
```

Il secondo comando chiede a curl di **non** mandare la riga `Host`.

- I risultati sono gli stessi delle prove A e C?

### Da consegnare / raccontare

In poche righe, con parole tue:

1. Com'è fatta una richiesta HTTP? (Che cos'è `\r\n`?)
2. A che cosa serve la riga vuota?
3. Come fa il client a capire che la risposta è finita?

Le risposte sono nella sezione 4: provaci prima da solo!

---

## 4. Spiegazione

### La richiesta è testo

Una richiesta HTTP è fatta di righe di caratteri ASCII, ognuna chiusa da
**`\r\n`** (*carriage return* + *line feed*, cioè "torna a inizio riga" e
"vai a capo"):

```
GET / HTTP/1.1\r\n
Host: example.com\r\n
\r\n
```

- **Prima riga**: metodo (`GET`), percorso (`/`), versione del protocollo (`HTTP/1.1`).
- **Intestazioni**, una per riga, nella forma `Nome: valore`.
- **`Host`** dice al server quale sito vogliamo. Sullo stesso indirizzo IP possono
  esserci molti siti diversi, e il server deve sapere quale scegliere. In
  HTTP/1.1 è **obbligatoria**: senza, il server di solito risponde
  `400 Bad Request` (prova C).

### A che cosa serve la riga vuota

**Segna la fine delle intestazioni.** TCP trasporta un flusso continuo di byte,
senza "confini": il server non può sapere da solo se abbiamo finito di scrivere.
Senza la riga vuota resta in attesa di altre intestazioni e non risponde
(prova D). Alla fine si arrende uno dei due: lo script dopo 5 secondi, oppure
il server, che chiude la connessione.

### Come il client capisce che la risposta è finita

Anche la risposta ha la stessa forma: una riga di stato (es. `HTTP/1.1 200 OK`),
le intestazioni, **una riga vuota**, e poi il corpo (la pagina vera e propria).
Per sapere dove finisce il corpo ci sono due modi:

- **`Content-Length: N`**: il server dichiara in anticipo quanti byte manderà.
  Il client legge esattamente N byte e sa di aver finito, anche se la
  connessione resta aperta.
- **Chiusura della connessione**: se manca `Content-Length`, il server chiude
  il socket quando ha finito. Il client legge finché `recv()` non restituisce
  0 byte.

Esiste anche un terzo modo, `Transfer-Encoding: chunked`: il corpo arriva a
pezzi, ognuno preceduto dalla sua lunghezza in esadecimale, e un pezzo lungo 0
segna la fine. Oggi `example.com` risponde proprio così. Lo script lo
riconosce: ricompone il corpo e dice quanti pezzi sono arrivati.

### Perché proprio la porta 80?

È la porta standard di HTTP. I siti in `https://` usano la porta 443 e
cifrano tutto con TLS: lì il testo non si potrebbe scrivere "a mano" con un
semplice socket. Per questo servono siti ancora in `http://`.

---

## 5. Problemi frequenti

| Messaggio / comportamento | Causa probabile | Cosa fare |
|---|---|---|
| `socket.gaierror: Name or service not known` | Nome dell'host sbagliato, oppure niente connessione | Controlla di aver scritto solo il nome (`example.com`), **senza** `http://` e senza `/` finale |
| `ConnectionRefusedError` o `TimeoutError` alla connessione | Il sito non accetta connessioni sulla porta 80, oppure la rete della scuola la blocca | Prova un altro host, oppure usa il Codespace |
| `HTTP/1.1 301 Moved Permanently` | Il sito accetta solo `https://` | Normale: guarda l'intestazione `Location`, poi scegli un sito in `http://` |
| Lo script resta fermo 5 secondi | Riga vuota mancante (prova D) | Se non hai usato `--senza-riga-vuota`, prova un altro sito |
| `Network is unreachable` | Il sito ha anche un indirizzo IPv6 e la rete non lo supporta | Aggiorna `client_http.py`: la versione attuale usa solo IPv4 |
| `python3: command not found` (Windows) | Su Windows il comando ha un altro nome | Usa `python` o `py` |
