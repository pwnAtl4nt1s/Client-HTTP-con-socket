import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "example.com"
percorso = sys.argv[2] if len(sys.argv) > 2 else "/"
opzioni = sys.argv[3:]

nome, _, porta = host.partition(":")
porta = int(porta) if porta else 80

righe = [f"GET {percorso} HTTP/1.1"]
if "--senza-host" not in opzioni:
    righe.append(f"Host: {host}")
richiesta = "".join(riga + "\r\n" for riga in righe)
if "--senza-riga-vuota" not in opzioni:
    richiesta += "\r\n"

print("=== RICHIESTA (i \\r\\n sono visibili) ===")
print(repr(richiesta))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
    s.connect((nome, porta))
except OSError as errore:
    sys.exit(f"\nConnessione a {nome}:{porta} non riuscita: {errore}\n"
             "Prova un altro host, per esempio example.com")
s.sendall(richiesta.encode("ascii"))

def ricevi():
    pezzo = s.recv(4096)
    if not pezzo:
        raise ConnectionError
    return pezzo


dati = intestazioni = corpo = b""
try:
    while b"\r\n\r\n" not in dati:
        pezzo = s.recv(4096)
        if not pezzo:
            break
        dati += pezzo

    intestazioni, _, corpo = dati.partition(b"\r\n\r\n")
    lunghezza = None
    a_pezzi = False
    for riga in intestazioni.split(b"\r\n")[1:]:
        chiave, _, valore = riga.partition(b":")
        if chiave.strip().lower() == b"content-length":
            lunghezza = int(valore)
        if chiave.strip().lower() == b"transfer-encoding":
            a_pezzi = b"chunked" in valore.lower()

    if a_pezzi:
        resto, corpo, pezzi = corpo, b"", 0
        while True:
            while b"\r\n" not in resto:
                resto += ricevi()
            riga, _, resto = resto.partition(b"\r\n")
            n = int(riga.split(b";")[0], 16)
            while len(resto) < n + 2:
                resto += ricevi()
            corpo += resto[:n]
            resto = resto[n + 2:]
            if n == 0:
                break
            pezzi += 1
        nome_pezzi = "pezzo" if pezzi == 1 else "pezzi"
        fine = f"Transfer-Encoding: chunked, {pezzi} {nome_pezzi} e poi il pezzo finale lungo 0"
    elif lunghezza is not None:
        fine = f"Content-Length: {lunghezza} byte"
        while len(corpo) < lunghezza:
            pezzo = s.recv(4096)
            if not pezzo:
                break
            corpo += pezzo
    else:
        fine = "chiusura della connessione da parte del server"
        while pezzo := s.recv(4096):
            corpo += pezzo
except ConnectionError:
    fine = "il server ha chiuso la connessione prima della fine annunciata"
except socket.timeout:
    fine = "nessuna fine: il server non ha più mandato nulla per 5 secondi"
finally:
    s.close()

print("\n=== RISPOSTA ===")
if dati:
    print((intestazioni or dati).decode("latin-1"))
    print()
    print(corpo.decode("utf-8", errors="replace"))
else:
    print("(nessun byte ricevuto)")
print(f"\n=== Come ho capito che la risposta era finita: {fine} ===")
