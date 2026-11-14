# Client-HTTP-con-Socket

Client HTTP in Python: costruisce a mano una richiesta HTTP/1.1 con
un socket TCP, per mostrare come funziona davvero il protocollo.

> **L'idea da portarsi a casa:** un browser, alla fine, apre una connessione
> TCP e ci scrive del testo.

---

## La lezione interattiva

Apri **[`Lezione.html`](Lezione.html)**: è la pagina che accompagna la lezione, con
la richiesta smontata pezzo per pezzo, un simulatore, le domande
dell'esercizio, il quiz finale e il glossario.

Nel Codespace si apre così (poi clicca **Apri nel browser** nell'avviso che compare):

```bash
python3 -m http.server 8000
```

Sul tuo computer basta un doppio clic sul file.

| File | A cosa serve |
|---|---|
| `Lezione.html` | La lezione interattiva |
| `client_http.py` | Lo stesso client, con argomenti e lettura completa della risposta |

## Indice

1. [Prima di iniziare](#1-prima-di-iniziare)
2. [Dimostrazione](#2-dimostrazione)
3. [Esercizio](#3-esercizio)
4. [Problemi frequenti](#5-problemi-frequenti)

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
| `percorso` | `/Lezione.html` | `/` |
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

## 4. Problemi frequenti

| Messaggio / comportamento | Causa probabile | Cosa fare |
|---|---|---|
| `socket.gaierror: Name or service not known` | Nome dell'host sbagliato, oppure niente connessione | Controlla di aver scritto solo il nome (`example.com`), **senza** `http://` e senza `/` finale |
| `ConnectionRefusedError` o `TimeoutError` alla connessione | Il sito non accetta connessioni sulla porta 80, oppure la rete della scuola la blocca | Prova un altro host, oppure usa il Codespace |
| `HTTP/1.1 301 Moved Permanently` | Il sito accetta solo `https://` | Normale: guarda l'intestazione `Location`, poi scegli un sito in `http://` |
| Lo script resta fermo 5 secondi | Riga vuota mancante (prova D) | Se non hai usato `--senza-riga-vuota`, prova un altro sito |
| `Network is unreachable` | Il sito ha anche un indirizzo IPv6 e la rete non lo supporta | Aggiorna `client_http.py`: la versione attuale usa solo IPv4 |
| `python3: command not found` (Windows) | Su Windows il comando ha un altro nome | Usa `python` o `py` |
