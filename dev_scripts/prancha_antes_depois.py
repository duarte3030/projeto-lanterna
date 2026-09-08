#!/usr/bin/env python3
"""Monta a prancha antes/depois de um mapa e MEDE o pixel que mudou.

Por que existe. O portão de arte desta onda do REFINO não é "o render ficou
parecido", é um par de números: quantos pixels mudaram no mapa que era para
mudar, e ZERO pixel no mapa que não era. As frentes de Snowpoint e de Canalave
montaram essa prancha na mão, cada uma do seu jeito, e a regra do PRD ("boa
notícia é suspeita: render igual sem diff de pixel medido não é prova") pedia
uma ferramenta só, que sempre imprime o número junto da imagem.

O QUE ELE FAZ, e são duas coisas de uma vez:

  1. `--par antes.png depois.png saida.png` cola os dois lado a lado em 2x, com
     rótulo, e imprime quantos pixels diferem e em que retângulo eles caem. É a
     imagem que o Gui olha para vetar cidade a cidade.
  2. `--zero antes.png depois.png` é o portão dos mapas VIZINHOS, os que dividem
     o tileset com a cidade mexida e não podiam mudar. Ele não desenha nada:
     devolve código 1 se um único pixel diferir, e imprime o primeiro par de
     coordenadas em que difere, que é o que faz a falha ser investigável em vez
     de só vermelha.

DUAS ARMADILHAS, e as duas já morderam alguém nesta obra:

  - TAMANHO DIFERENTE não é "quase igual". Se o mapa mudou de largura, o par
     não é comparável e a resposta certa é falhar dizendo os dois tamanhos, não
     recortar o menor. Recortar transformaria "a planta mudou", que é o pior
     defeito possível nesta onda, em "mudaram alguns pixels".
  - PNG INDEXADO com paletas diferentes pode ter os MESMOS índices e cores
     diferentes na tela, e comparar índice daria zero com a imagem trocada. A
     comparação é feita em RGB, depois de converter os dois.

Uso:
    python3 dev_scripts/prancha_antes_depois.py --par a.png d.png saida.png \\
            [--titulo "CelesticTown"] [--escala 2]
    python3 dev_scripts/prancha_antes_depois.py --zero a.png d.png
    python3 dev_scripts/prancha_antes_depois.py --demo
"""
import os
import sys
import tempfile

from PIL import Image, ImageDraw

FUNDO = (24, 24, 24)
TEXTO = (235, 235, 235)
REALCE = (220, 60, 60)


def _abre_rgb(caminho):
    if not os.path.exists(caminho):
        raise SystemExit("nao existe: %s" % caminho)
    return Image.open(caminho).convert("RGB")


def compara(caminho_a, caminho_b):
    """(n_diferentes, total, retangulo, primeiro_par). Falha dura se o tamanho mudar."""
    a, b = _abre_rgb(caminho_a), _abre_rgb(caminho_b)
    if a.size != b.size:
        raise SystemExit(
            "tamanho diferente, os dois nao sao comparaveis: %s tem %dx%d e %s "
            "tem %dx%d. Num mapa isso significa que a PLANTA mudou, que e o "
            "defeito que esta onda proibe." % (
                os.path.basename(caminho_a), a.width, a.height,
                os.path.basename(caminho_b), b.width, b.height))
    pa, pb = a.load(), b.load()
    n = 0
    x0 = y0 = 10 ** 9
    x1 = y1 = -1
    primeiro = None
    for y in range(a.height):
        for x in range(a.width):
            if pa[x, y] != pb[x, y]:
                n += 1
                if primeiro is None:
                    primeiro = (x, y, pa[x, y], pb[x, y])
                x0, y0 = min(x0, x), min(y0, y)
                x1, y1 = max(x1, x), max(y1, y)
    ret = None if x1 < 0 else (x0, y0, x1, y1)
    return n, a.width * a.height, ret, primeiro


def prancha(caminho_a, caminho_b, saida, titulo="", escala=2):
    """Cola os dois lado a lado em `escala`x, com rotulo, e devolve a medida."""
    n, total, ret, _ = compara(caminho_a, caminho_b)
    a, b = _abre_rgb(caminho_a), _abre_rgb(caminho_b)
    if escala != 1:
        tam = (a.width * escala, a.height * escala)
        a = a.resize(tam, Image.NEAREST)
        b = b.resize(tam, Image.NEAREST)

    margem, faixa, vao = 12, 26, 16
    largura = margem * 2 + a.width + vao + b.width
    altura = margem * 2 + faixa + a.height
    folha = Image.new("RGB", (largura, altura), FUNDO)
    folha.paste(a, (margem, margem + faixa))
    folha.paste(b, (margem + a.width + vao, margem + faixa))

    lapis = ImageDraw.Draw(folha)
    cabeca = "%s  %santes (esquerda) contra depois (direita), %dx" % (
        titulo, "" if not titulo else "| ", escala)
    lapis.text((margem, 4), cabeca, fill=TEXTO)
    lapis.text((margem, margem + faixa - 14), "antes", fill=TEXTO)
    lapis.text((margem + a.width + vao, margem + faixa - 14), "depois", fill=TEXTO)
    conta = "%d pixels diferentes de %d (%.2f%%)" % (n, total, 100.0 * n / total)
    if ret:
        conta += "  |  retangulo do que mudou: (%d,%d) a (%d,%d)" % ret
    lapis.text((margem + 200, 4), conta, fill=TEXTO if n else REALCE)

    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    folha.save(saida)
    return n, total, ret


def demo():
    """Auto-teste, com o par negativo: a comparacao tem que saber REPROVAR."""
    erros = []
    with tempfile.TemporaryDirectory() as tmp:
        a = os.path.join(tmp, "a.png")
        b = os.path.join(tmp, "b.png")
        c = os.path.join(tmp, "c.png")
        outro = os.path.join(tmp, "outro.png")
        base = Image.new("RGB", (32, 16), (10, 120, 40))
        base.save(a)
        base.save(b)
        mudada = base.copy()
        mudada.putpixel((5, 7), (200, 10, 10))
        mudada.putpixel((6, 7), (200, 10, 10))
        mudada.save(c)
        Image.new("RGB", (32, 20), (10, 120, 40)).save(outro)

        # caso 1, positivo: igual e igual.
        n, total, ret, _ = compara(a, b)
        if n or ret is not None:
            erros.append("caso 1: dois PNGs iguais deram %d diferencas" % n)

        # caso 2, prova negativa: dois pixels trocados TEM que aparecer, e o
        # retangulo tem que cercar exatamente eles.
        n, _, ret, primeiro = compara(a, c)
        if n != 2:
            erros.append("caso 2: dois pixels trocados deram %d" % n)
        if ret != (5, 7, 6, 7):
            erros.append("caso 2: retangulo %s, esperado (5, 7, 6, 7)" % (ret,))
        if primeiro != (5, 7, (10, 120, 40), (200, 10, 10)):
            erros.append("caso 2: primeiro par %s" % (primeiro,))

        # caso 3, prova negativa: tamanho diferente e falha dura, nao recorte.
        try:
            compara(a, outro)
            erros.append("caso 3: tamanho diferente passou sem falhar")
        except SystemExit:
            pass

        # caso 4: a prancha sai do tamanho previsto e o arquivo existe.
        saida = os.path.join(tmp, "prancha.png")
        n, _, _ = prancha(a, c, saida, titulo="teste", escala=2)
        if not os.path.exists(saida):
            erros.append("caso 4: a prancha nao foi gravada")
        else:
            folha = Image.open(saida)
            esperado = (12 * 2 + 64 + 16 + 64, 12 * 2 + 26 + 32)
            if folha.size != esperado:
                erros.append("caso 4: prancha %s, esperado %s" % (folha.size, esperado))
        if n != 2:
            erros.append("caso 4: a prancha contou %d diferencas" % n)

    for erro in erros:
        print("  VERMELHO", erro)
    print("prancha_antes_depois --demo:", "VERDE" if not erros else "VERMELHO (%d)" % len(erros))
    return 1 if erros else 0


def main():
    argv = sys.argv[1:]
    if "--demo" in argv or "--autoteste" in argv:
        return demo()
    if "--zero" in argv:
        i = argv.index("--zero")
        a, b = argv[i + 1], argv[i + 2]
        n, total, ret, primeiro = compara(a, b)
        if n:
            print("VERMELHO %s: %d pixels de %d diferem, retangulo %s, primeiro "
                  "(%d,%d) %s -> %s" % (os.path.basename(b), n, total, ret,
                                        primeiro[0], primeiro[1], primeiro[2], primeiro[3]))
            return 1
        print("zero pixel de %d diferente em %s" % (total, os.path.basename(b)))
        return 0
    if "--par" in argv:
        i = argv.index("--par")
        a, b, saida = argv[i + 1], argv[i + 2], argv[i + 3]
        titulo = argv[argv.index("--titulo") + 1] if "--titulo" in argv else ""
        escala = int(argv[argv.index("--escala") + 1]) if "--escala" in argv else 2
        n, total, ret = prancha(a, b, saida, titulo, escala)
        print("%s: %d pixels de %d diferentes (%.2f%%), retangulo %s"
              % (saida, n, total, 100.0 * n / total, ret))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
