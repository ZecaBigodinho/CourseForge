"""
Aplica um trecho de gabarito sobre o código de uma classe da aula, para testar modificações.

Formato do trecho (o mesmo exibido ao aluno):
- linhas na coluna 0 (antes do primeiro "    def") = código fora da classe → entra antes da classe;
- blocos "    def nome(...)" = métodos novos ou que substituem os de mesmo nome na classe.
"""
import re


def _metodos(trecho: str) -> list[tuple[str, str]]:
    linhas = trecho.splitlines()
    inicios = [i for i, l in enumerate(linhas) if re.match(r"^    (@\w+.*|def \w+)", l)]
    blocos, i = [], 0
    while i < len(inicios):
        ini = inicios[i]
        # decoradores ficam junto do def seguinte
        while linhas[ini].strip().startswith("@") and i + 1 < len(inicios):
            i += 1
        fim = inicios[i + 1] if i + 1 < len(inicios) else len(linhas)
        while fim > ini and (not linhas[fim - 1].strip() or not linhas[fim - 1].startswith("    ")):
            fim -= 1
        corpo = "\n".join(linhas[ini:fim])
        nome = re.search(r"def (\w+)", corpo).group(1)
        blocos.append((nome, corpo))
        i += 1
    return blocos


def _fora_da_classe(trecho: str) -> str:
    saida = []
    for linha in trecho.splitlines():
        if re.match(r"^    (@\w+|def \w+)", linha):
            break
        saida.append(linha)
    return "\n".join(saida)


def aplicar(fonte: str, classe: str, trecho: str) -> str:
    inicio_classe = fonte.index(f"class {classe}")
    fonte = fonte[:inicio_classe] + _fora_da_classe(trecho) + "\n\n" + fonte[inicio_classe:]
    for nome, corpo in _metodos(trecho):
        padrao = re.compile(rf"^    def {nome}\(.*?(?=^    def |^    @|^\S|\Z)", re.S | re.M)
        if padrao.search(fonte[fonte.index(f"class {classe}"):]):
            base = fonte.index(f"class {classe}")
            fonte = fonte[:base] + padrao.sub(lambda m: corpo + "\n\n", fonte[base:], count=1)
        else:
            # método novo: entra no fim da classe (antes do primeiro código na coluna 0 depois dela)
            corpo_classe = fonte.index("\n", fonte.index(f"class {classe}")) + 1
            fim = re.search(r"^\S", fonte[corpo_classe:], re.M)
            pos = corpo_classe + fim.start() if fim else len(fonte)
            fonte = fonte[:pos] + corpo + "\n\n" + fonte[pos:]
    return fonte
