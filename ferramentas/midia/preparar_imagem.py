"""
Prepara uma imagem para as aulas: recorta (opcional), reduz a largura, converte para WebP
e remove os metadados. Padrão completo em ferramentas/midia/README.md.

    python ferramentas/midia/preparar_imagem.py captura.png destino.webp
    python ferramentas/midia/preparar_imagem.py captura.png destino.webp --recorte 0,0,1200,800
"""
import argparse
import sys
from pathlib import Path

from PIL import Image

LARGURA_MAXIMA = 1400
TAMANHO_MAXIMO = 300 * 1024  # bytes


def preparar(origem: Path, destino: Path, recorte: tuple[int, int, int, int] | None = None,
             qualidade: int = 85) -> int:
    """Grava destino em WebP e devolve o tamanho em bytes."""
    with Image.open(origem) as imagem:
        imagem = imagem.convert("RGB")  # descarta transparência e metadados
        if recorte:
            imagem = imagem.crop(recorte)
        if imagem.width > LARGURA_MAXIMA:
            altura = round(imagem.height * LARGURA_MAXIMA / imagem.width)
            imagem = imagem.resize((LARGURA_MAXIMA, altura), Image.LANCZOS)
        destino.parent.mkdir(parents=True, exist_ok=True)
        imagem.save(destino, "WEBP", quality=qualidade, method=6)
    return destino.stat().st_size


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepara uma imagem para as aulas (WebP).")
    parser.add_argument("origem", type=Path)
    parser.add_argument("destino", type=Path, help="arquivo .webp de destino")
    parser.add_argument("--recorte", help="esquerda,topo,direita,baixo (pixels da imagem original)")
    parser.add_argument("--qualidade", type=int, default=85)
    args = parser.parse_args()

    if args.destino.suffix.lower() != ".webp":
        print("O destino precisa terminar em .webp", file=sys.stderr)
        return 1
    recorte = tuple(int(n) for n in args.recorte.split(",")) if args.recorte else None
    tamanho = preparar(args.origem, args.destino, recorte, args.qualidade)
    print(f"{args.destino} — {tamanho / 1024:.0f} KB")
    if tamanho > TAMANHO_MAXIMO:
        print("Atenção: passou de 300 KB. Recorte mais ou use --qualidade 75.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
