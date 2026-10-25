"""Abre o Sistema Escolar falando com o Neon pelo repassador local (127.0.0.1:6543).

Monta a DATABASE_URL só em memória e passa ao app pela variável de ambiente
(o load_dotenv do app não sobrescreve variáveis que já existem). Nada é impresso.
Uso:  python abrir_pelo_repassador.py <pasta_do_projeto>
"""
import os
import subprocess
import sys
from pathlib import Path

from dotenv import dotenv_values
from psycopg.conninfo import conninfo_to_dict, make_conninfo

pasta = Path(sys.argv[1])
d = conninfo_to_dict(dotenv_values(pasta / ".env")["DATABASE_URL"])
endpoint = d["host"].split(".")[0].removesuffix("-pooler")
d.update(host="127.0.0.1", port="6543", options=f"endpoint={endpoint}")
env = {**os.environ, "DATABASE_URL": make_conninfo(**d)}
subprocess.Popen([sys.executable, "main.py"], cwd=pasta, env=env,
                 creationflags=subprocess.CREATE_NO_WINDOW)
print("app aberto pelo repassador")
