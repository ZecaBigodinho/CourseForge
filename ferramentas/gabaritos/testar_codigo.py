"""
Confere o código dos cursos de Web, TypeScript, React e Java (o testar.py cuida dos cursos de Python).

    python ferramentas/gabaritos/testar_codigo.py

O que é conferido em cada bloco de código das aulas (inclusive os dos gabaritos):
- js         ➔ sintaxe, com `node --check`;
- ts / tsx   ➔ sintaxe, com o compilador do TypeScript (`ts.transpileModule`; os tipos não são checados,
               porque os exemplos usam bibliotecas que não estão instaladas aqui);
- java       ➔ compilação de verdade com `javac`. As classes que compilam sozinhas ajudam a compilar
               as outras da mesma aula (e do mesmo módulo).

Blocos **completos** (com título de arquivo, que começam com import/export, ou classes Java) precisam
passar: se falharem, é ERRO. **Trechos soltos** (pedaços de JSX, uma linha de exemplo, o código de
um exercício "encontre os erros") são testados dentro de uma função ou de um fragmento; se ainda
assim não passarem, viram AVISO (para conferir à mão), sem falhar o teste.

Precisa de node e de um JDK no PATH, e do pacote `typescript` (variável TYPESCRIPT_DIR com a pasta
node_modules, `npm install typescript` na raiz do projeto, ou instalado com -g). Sai com 1 se houver ERRO.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CURSOS = ["desenvolvimento_web", "typescript", "react", "java"]
LINGUAGENS = {"js", "javascript", "ts", "tsx", "java"}
RE_ABRE = re.compile(r'^(\s*)```(\w+)(?:\s+title="([^"]*)")?\s*$')
RE_TIPO = re.compile(r"^(?:public\s+)?(?:(?:final|abstract|sealed|non-sealed|static)\s+)*"
                     r"(class|interface|record|enum)\s+(\w+)", re.M)
NL = "\n"
sys.stdout.reconfigure(encoding="utf-8")


def blocos(arquivo: Path):
    """[(linha, linguagem, título, código)] de todos os blocos de código do arquivo."""
    linhas = arquivo.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(linhas):
        m = RE_ABRE.match(linhas[i])
        if m and m.group(2) in LINGUAGENS:
            recuo, inicio, corpo = m.group(1), i + 1, []
            i += 1
            while i < len(linhas) and linhas[i].strip() != "```":
                corpo.append(linhas[i][len(recuo):] if linhas[i].startswith(recuo) else linhas[i])
                i += 1
            yield inicio, m.group(2), m.group(3), textwrap.dedent(NL.join(corpo)) + NL
        i += 1


def rodar(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


# ---------------------------------------------------------------- JavaScript
def testar_js(itens, pasta: Path):
    falhas = []
    for n, (onde, codigo, completo) in enumerate(itens):
        tentativas = [codigo] if completo else [codigo, "function __trecho() {" + NL + codigo + NL + "}" + NL]
        primeiro = None
        for k, c in enumerate(tentativas):
            arq = pasta / f"bloco{n}_{k}.mjs"
            arq.write_text(c, encoding="utf-8")
            r = rodar(["node", "--check", str(arq)])
            if r.returncode == 0:
                primeiro = None
                break
            msg = [l.strip() for l in r.stderr.splitlines() if "Error" in l]
            primeiro = primeiro or (msg[0] if msg else "erro de sintaxe")
        if primeiro:
            falhas.append((onde, ("" if completo else "trecho solto: ") + primeiro, not completo))
    return falhas


# ---------------------------------------------------------------- TypeScript / TSX
VERIFICADOR_TS = r"""
const ts = require(process.argv[2]);
const itens = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
const NL = String.fromCharCode(10);
function erros(codigo, tsx) {
  const r = ts.transpileModule(codigo, { reportDiagnostics: true, fileName: tsx ? 'x.tsx' : 'x.ts',
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext, jsx: ts.JsxEmit.ReactJSX } });
  return (r.diagnostics || []).map(d => {
    const pos = d.file ? d.file.getLineAndCharacterOfPosition(d.start) : null;
    return (pos ? 'linha ' + (pos.line + 1) + ': ' : '') + ts.flattenDiagnosticMessageText(d.messageText, ' ');
  });
}
const saida = [];
for (const [onde, codigo, tsx, completo] of itens) {
  const e = erros(codigo, tsx);
  if (!e.length) continue;
  if (completo) { saida.push([onde, e[0], false]); continue; }
  const embrulhos = ['function __trecho() {' + NL + codigo + NL + '}',
                     'const __x = (<>' + NL + codigo + NL + '</>);',
                     'function __j() { return (<>' + NL + codigo + NL + '</>); }',
                     'const __o = {' + NL + codigo + NL + '};',
                     '<div' + NL + codigo + NL + '/>;'];
  if (!embrulhos.some(c => erros(c, true).length === 0)) saida.push([onde, 'trecho solto: ' + e[0], true]);
}
console.log(JSON.stringify(saida));
"""


def achar_typescript() -> str:
    for c in (os.environ.get("TYPESCRIPT_DIR", ""), str(RAIZ / "node_modules")):
        if c and (Path(c) / "typescript").exists():
            return str(Path(c) / "typescript")
    r = rodar(["npm", "root", "-g"], shell=os.name == "nt")
    global_ = Path(r.stdout.strip()) / "typescript"
    if global_.exists():
        return str(global_)
    sys.exit("Pacote typescript não encontrado: npm install typescript (ou TYPESCRIPT_DIR=<node_modules>)")


def testar_ts(itens, pasta: Path):
    (pasta / "verificar.js").write_text(VERIFICADOR_TS, encoding="utf-8")
    (pasta / "itens.json").write_text(json.dumps(itens), encoding="utf-8")
    r = rodar(["node", str(pasta / "verificar.js"), achar_typescript(), str(pasta / "itens.json")])
    if r.returncode:
        sys.exit(r.stderr)
    return [tuple(x) for x in json.loads(r.stdout)]


# ---------------------------------------------------------------- Java
IMPORTS = NL.join(f"import java.{p}.*;" for p in ("util", "util.function", "util.stream", "io", "nio.file", "time")) + NL


def compilar(arquivos: dict, pasta: Path) -> str:
    """Compila {Nome: código}; devolve as mensagens de erro ('' = compilou)."""
    shutil.rmtree(pasta, ignore_errors=True)
    pasta.mkdir()
    for nome, codigo in arquivos.items():
        (pasta / f"{nome}.java").write_text(codigo, encoding="utf-8")
    r = rodar(["javac", "-encoding", "UTF-8", "-nowarn", "-d", str(pasta / "out"), *map(str, pasta.glob("*.java"))])
    return "" if r.returncode == 0 else r.stdout + r.stderr


def nome_do_tipo(codigo: str):
    publico = re.search(r"^public\s+(?:(?:final|abstract|sealed)\s+)*(?:class|interface|record|enum)\s+(\w+)", codigo, re.M)
    if publico:
        return publico.group(1)
    m = RE_TIPO.search(codigo)
    return m.group(2) if m else None


def eh_tipo_completo(codigo: str) -> bool:
    """Antes da primeira classe só há imports, package, comentários e anotações?"""
    m = RE_TIPO.search(codigo)
    if not m:
        return False
    antes = [l.strip() for l in codigo[:m.start()].splitlines() if l.strip()]
    return all(l.startswith(("import ", "package ", "//", "/*", "*", "@")) for l in antes)


def separar(codigo: str) -> tuple[str, str]:
    """Bloco "misto" (uma classe e, depois dela, código solto, como '// no main: ...'):
    devolve (a classe, o resto). Conta as chaves a partir da primeira classe; ignora as de strings."""
    m = RE_TIPO.search(codigo)
    nivel, i, dentro_string = 0, codigo.index("{", m.end()), None
    while i < len(codigo):
        c = codigo[i]
        if dentro_string:
            if c == "\\":
                i += 1
            elif c == dentro_string:
                dentro_string = None
        elif c in "\"'":
            dentro_string = c
        elif c == "{":
            nivel += 1
        elif c == "}":
            nivel -= 1
            if nivel == 0:
                return codigo[:i + 1] + NL, codigo[i + 1:]
        i += 1
    return codigo, ""


def so_comentario(texto: str) -> bool:
    return all(not l.strip() or l.strip().startswith("//") for l in texto.splitlines())


def primeira_linha_de_erro(saida: str) -> str:
    for linha in saida.splitlines():
        if "error:" in linha or "erro:" in linha:
            return linha.replace("\\", "/").split("/")[-1].strip()
    return saida.strip().splitlines()[0] if saida.strip() else "erro"


def testar_java(por_aula, pasta: Path):
    """1ª passada: classes que compilam sozinhas viram apoio (da aula e do módulo).
    2ª passada: as que dependem de outras compilam com esse apoio; trechos soltos vão num método."""
    falhas = []
    trabalho = pasta / "java"
    apoio: dict = {}
    pendentes, pendentes_resto = [], []
    da_aula: dict = {}     # todas as classes completas de cada aula (a última versão de cada nome)
    for aula, itens in por_aula.items():
        for onde, codigo in itens:
            nome = nome_do_tipo(codigo)
            if nome and eh_tipo_completo(codigo):
                codigo, resto = separar(codigo)
                if not so_comentario(resto):
                    if RE_TIPO.search(resto):          # outra classe depois: mais um bloco completo
                        itens.append((onde + " (2ª classe)", resto))
                    else:                              # código solto depois da classe: vira trecho
                        pendentes_resto.append((aula, onde + " (depois da classe)", None, resto, None))
                da_aula.setdefault(str(aula), {})[nome] = codigo
                erro = compilar({nome: codigo}, trabalho)
                if erro:
                    pendentes.append((aula, onde, nome, codigo, erro))
                else:
                    apoio.setdefault(aula.parent.name, {})[nome] = codigo
                    apoio.setdefault(str(aula), {})[nome] = codigo
            else:
                pendentes.append((aula, onde, None, codigo, None))
    for aula, onde, nome, codigo, erro in pendentes + pendentes_resto:
        contexto = {**apoio.get(aula.parent.name, {}), **da_aula.get(str(aula), {})}
        if nome:
            if "cannot find symbol" in erro or "não pode encontrar" in erro:
                erro = compilar({**{k: v for k, v in contexto.items() if k != nome}, nome: codigo}, trabalho)
            if erro:
                falhas.append((onde, primeira_linha_de_erro(erro), False))
            continue
        tentativas = [IMPORTS + "class Trecho {" + NL + "  void trecho() throws Exception {" + NL + codigo + NL + "  }" + NL + "}" + NL,
                      IMPORTS + "class Trecho {" + NL + codigo + NL + "}" + NL]
        primeiro = None
        for t in tentativas:
            e = compilar({**contexto, "Trecho": t}, trabalho)
            if not e:
                primeiro = None
                break
            primeiro = primeiro or e
        if primeiro:
            falhas.append((onde, "trecho solto: " + primeira_linha_de_erro(primeiro), True))
    return falhas


# ---------------------------------------------------------------- principal
def main() -> int:
    js, ts_itens, java = [], [], {}
    for curso in CURSOS:
        for arq in sorted((RAIZ / "cursos" / curso).glob("modulo_*/*.md")):
            for linha, lang, titulo, codigo in blocos(arq):
                onde = f"{arq.relative_to(RAIZ / 'cursos').as_posix()}:{linha}"
                completo = bool(titulo) or bool(re.match(r"\s*(import|export)\b", codigo))
                if lang in ("js", "javascript"):
                    js.append((onde, codigo, completo))
                elif lang in ("ts", "tsx"):
                    ts_itens.append((onde, codigo, lang == "tsx", completo))
                else:
                    java.setdefault(arq, []).append((onde, codigo))
    total = len(js) + len(ts_itens) + sum(len(v) for v in java.values())
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp)
        falhas = testar_js(js, pasta) + testar_ts(ts_itens, pasta) + testar_java(java, pasta)
    for onde, erro, aviso in falhas:
        print(f"  [{'AVISO' if aviso else 'ERRO '}] {onde}  {erro}")
    erros = [f for f in falhas if not f[2]]
    print(f"\n{total} blocos (JS {len(js)}, TS/TSX {len(ts_itens)}, Java {total - len(js) - len(ts_itens)}): "
          f"{len(erros)} com erro, {len(falhas) - len(erros)} avisos.")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
