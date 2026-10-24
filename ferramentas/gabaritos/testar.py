"""
Executa os gabaritos das aulas e confere o resultado de cada um.

    python ferramentas/gabaritos/testar.py                 # todos os casos
    python ferramentas/gabaritos/testar.py poo banco_04    # só alguns arquivos de casos/
    python ferramentas/gabaritos/testar.py -v              # mostra a saída de cada gabarito

Cada caso é (aula, nível, código, entrada[, teste]):
- código  = o gabarito, lido da aula com G(aula, nível) — a aula é a fonte única;
- entrada = o que seria digitado no input(), uma resposta por linha;
- teste   = (opcional) programa que roda no lugar do código; "# === gabarito ===" dentro
            dele é trocado pelo código. Serve para preparar arquivos ou conferir resultados.
- "# === arquivo: nome.py ===" divide o programa em vários arquivos; executa o último.

Sai com código 1 se algum gabarito falhar.
"""
import argparse
import importlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PASTA = Path(__file__).resolve().parent
sys.path[:0] = [str(PASTA), str(PASTA / "casos")]
sys.stdout.reconfigure(encoding="utf-8")

RE_ARQ = re.compile(r"^# === arquivo: (\S+) ===$", re.M)


def arquivos(codigo: str) -> list[tuple[str, str]]:
    partes = RE_ARQ.split(codigo)
    if len(partes) == 1:
        return [("solucao.py", codigo)]
    return list(zip(partes[1::2], partes[2::2]))


def executar(codigo: str, entrada: str, teste: str | None) -> subprocess.CompletedProcess:
    programa = (teste or codigo).replace("# === gabarito ===", codigo)
    with tempfile.TemporaryDirectory() as pasta:
        # Camada que permite testar janelas Tkinter/CustomTkinter (ver _gui.py)
        (Path(pasta) / "_gui.py").write_text((PASTA / "_gui.py").read_text(encoding="utf-8"), encoding="utf-8")
        partes = arquivos(programa)
        for nome, conteudo in partes:
            destino = Path(pasta) / nome
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(conteudo, encoding="utf-8")
        principal = Path(pasta) / partes[-1][0]
        # A pasta do script entra no sys.path, então os arquivos do gabarito se importam entre si
        return subprocess.run([sys.executable, "-E", "-X", "utf8", str(principal)], input=entrada,
                              capture_output=True, text=True, encoding="utf-8", cwd=pasta, timeout=60)


def main() -> int:
    parser = argparse.ArgumentParser(description="Testa os gabaritos das aulas.")
    parser.add_argument("casos", nargs="*", help="arquivos de casos/ (sem .py); padrão: todos")
    parser.add_argument("-v", "--verboso", action="store_true", help="mostra a saída de cada gabarito")
    args = parser.parse_args()

    nomes = args.casos or sorted(p.stem for p in (PASTA / "casos").glob("*.py") if not p.stem.startswith("_"))
    total = falhas = 0
    for nome in nomes:
        print(f"\n## {nome}")
        for caso in importlib.import_module(nome).GABARITOS:
            aula, nivel, codigo, entrada = caso[:4]
            teste = caso[4] if len(caso) > 4 else None
            total += 1
            r = executar(codigo, entrada, teste)
            ok = r.returncode == 0 and "Traceback" not in r.stderr
            falhas += not ok
            print(f"  [{'OK ' if ok else 'ERRO'}] {aula} · {nivel}")
            if args.verboso or not ok:
                saida = (r.stdout + r.stderr).strip().splitlines()
                print("        " + "\n        ".join(saida[-25:]))

    print(f"\n{total - falhas}/{total} gabaritos executaram sem erro.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
