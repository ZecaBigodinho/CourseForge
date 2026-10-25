"""Repassador TCP local (127.0.0.1:6543 -> servidor do Neon:5432), para simular queda de rede só no app.

Lê o .env do projeto de teste apenas em memória; não imprime nada da connection string.
Uso:  python repassador.py <pasta_do_projeto>   (rodar em segundo plano; matar o processo = "cair a rede")
"""
import socket
import sys
import threading
from pathlib import Path

from dotenv import dotenv_values
from psycopg.conninfo import conninfo_to_dict

alvo = conninfo_to_dict(dotenv_values(Path(sys.argv[1]) / ".env")["DATABASE_URL"])["host"]


def bombear(origem, destino):
    try:
        while dados := origem.recv(65536):
            destino.sendall(dados)
    except OSError:
        pass
    finally:
        for s in (origem, destino):
            try:
                s.close()
            except OSError:
                pass


servidor = socket.socket()
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("127.0.0.1", 6543))
servidor.listen()
print("repassador no ar", flush=True)
while True:
    cliente, _ = servidor.accept()
    remoto = socket.create_connection((alvo, 5432), timeout=10)
    remoto.settimeout(None)
    threading.Thread(target=bombear, args=(cliente, remoto), daemon=True).start()
    threading.Thread(target=bombear, args=(remoto, cliente), daemon=True).start()
