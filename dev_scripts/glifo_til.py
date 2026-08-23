#!/usr/bin/env python3
"""O TIL DE 'ã' E 'õ', DESENHADO POR CIMA DO TREMA QUE NINGUEM USA.

O PROBLEMA, medido em 23/08/2026. Os arquivos de fala de Galar tinham 315
ocorrencias de "ä" e ZERO de "ã": "Näo", "irmä", "coraçäo", "geraçöes". A 0.q
registrou isso como "obra de fonte, nao de script", e estava certa pela metade.
Sao DUAS metades, e as duas ficam aqui e no `charmap.txt`:

  1. A FONTE (a ROM do demake `ultimate-plus-v1.2.1.2`) escreve "não" como
     `E2 F4 E3`, medido byte a byte em `0x818376`. No charmap do FireRed, de
     onde o demake saiu, `F4` e o trema alemao 'ä'; o demake REDESENHOU o
     glifo daquele byte como til e passou a escrever portugues nele. O byte
     esta certo, o nome dele e que era alemao.
  2. O nosso `charmap.txt` tinha `'ä' = F4`, entao o tradutor decodificava
     `F4` como "ä" e o assembler reencodava "ä" de volta em `F4`: a ida e
     volta byte a byte fechava, e por isso o defeito nunca virou erro de
     build. O `charmap.txt` passou a chamar `F1 F2 F4 F5` de 'Ã' 'Õ' 'ã' 'õ',
     que e o que a fonte quer dizer com eles.

Falta o desenho, e e o que este script faz: nos nove `graphics/fonts/latin_*.png`
os glifos `F1 F2 F4 F5` trocam o trema pelo TIL. Nao ha invencao de pixel: o
til vem do 'Ñ' (`0x14`) e do 'ñ' (`0x29`) do MESMO arquivo, sobreposto ao 'A'
'O' 'a' 'o' do MESMO arquivo, para o til sair com o mesmo peso e o mesmo
alinhamento do resto daquela fonte.

CUSTO ZERO DE COMPATIBILIDADE, e foi medido antes de escolher: 'Ä', 'Ö', 'ä' e
'ö' nao tem UM usuario neste repo fora dos arquivos de Galar (varredura de
`data/`, `src/`, `include/`, `tools/`). O unico trema vivo e o 'Ü' de "JÜRGEN"
em `src/data/battle_frontier/apprentice.h`, que e o byte `F3` e NAO e tocado
aqui; 'ü' (`F6`) tambem fica como esta.

Idempotente: rodar duas vezes nao muda nada na segunda.
"""

import argparse
import glob
import os
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CEL = 16          # a celula do PNG de fonte e 16x16, um glifo por celula

# (glifo a redesenhar, letra base, glifo com o til, base do glifo com o til)
PARES = ((0xF1, 0xBB, 0x14, 0xC8),   # Ã <- A + til do Ñ
         (0xF2, 0xC9, 0x14, 0xC8),   # Õ <- O + til do Ñ
         (0xF4, 0xD5, 0x29, 0xE2),   # ã <- a + til do ñ
         (0xF5, 0xE3, 0x29, 0xE2))   # õ <- o + til do ñ
FUNDO = (0, 3)    # indices de paleta que sao fundo dentro da celula


def celula(px, b):
    """[[indice de paleta]] 16x16 do glifo `b`."""
    r, c = divmod(b, CEL)
    return [[px[c * CEL + x, r * CEL + y] for x in range(CEL)]
            for y in range(CEL)]


def escreve(px, b, m):
    r, c = divmod(b, CEL)
    for y in range(CEL):
        for x in range(CEL):
            px[c * CEL + x, r * CEL + y] = m[y][x]


def com_til(base, til, til_base):
    """A letra `base` com o til de `til`, e nada mais.

    As linhas do til sao as em que o glifo com til difere da letra dele; sao
    elas, e so elas, que descem sobre a letra base. Pixel de tinta da letra
    base NUNCA e apagado: se as duas coisas disputassem a mesma linha, a letra
    ganharia, e o `--demo` cobraria a diferenca.
    """
    saida = [linha[:] for linha in base]
    for y in range(CEL):
        if til[y] == til_base[y]:
            continue
        for x in range(CEL):
            if base[y][x] in FUNDO:
                saida[y][x] = til[y][x]
    return saida


def arquivos():
    return sorted(glob.glob(os.path.join(RAIZ, "graphics/fonts/latin_*.png")))


def aplica(gravar):
    mudou = 0
    for caminho in arquivos():
        im = Image.open(caminho)
        px = im.load()
        alterou = False
        for alvo, base, til, til_base in PARES:
            novo = com_til(celula(px, base), celula(px, til),
                           celula(px, til_base))
            if novo != celula(px, alvo):
                escreve(px, alvo, novo)
                alterou = True
        if alterou:
            mudou += 1
            print("  %-46s F1 F2 F4 F5 redesenhados"
                  % os.path.basename(caminho))
            if gravar:
                im.save(caminho)
    print("%d de %d PNG de fonte %s"
          % (mudou, len(arquivos()), "gravados" if gravar else "a gravar"))
    return mudou


def desenha(m, larg=8):
    return "\n".join("".join(".#+*"[m[y][x]] for x in range(larg))
                     for y in range(CEL))


def demo():
    """Cada caso mede uma coisa que o desenho tem de garantir."""
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print("  %-64s %s" % (nome, "ok" if cond else "REPROVOU"))
        ok = ok and cond

    for caminho in arquivos():
        px = Image.open(caminho).load()
        nome = os.path.basename(caminho)
        for alvo, base, til, til_base in PARES:
            b, t, tb = (celula(px, base), celula(px, til),
                        celula(px, til_base))
            novo = com_til(b, t, tb)
            linhas_til = [y for y in range(CEL) if t[y] != tb[y]]
            # 1. o til CHEGOU: o glifo novo difere da letra base, e difere
            #    exatamente nas linhas em que o Ñ difere do N.
            caso("%s %02X: o til desce, e so nas linhas do til"
                 % (nome, alvo),
                 [y for y in range(CEL) if novo[y] != b[y]] and
                 all(y in linhas_til for y in range(CEL) if novo[y] != b[y]))
            # 2. a LETRA continua inteira: nenhum pixel de tinta dela sumiu.
            caso("%s %02X: nenhum pixel da letra foi apagado" % (nome, alvo),
                 all(novo[y][x] == b[y][x] for y in range(CEL)
                     for x in range(CEL) if b[y][x] not in FUNDO))
            # 3. IDEMPOTENTE: desenhar de novo sobre o resultado nao muda.
            caso("%s %02X: desenhar duas vezes da o mesmo" % (nome, alvo),
                 com_til(novo, t, tb) == novo)
            # 4. MUTACAO PLANTADA: se a letra base ja fosse o proprio glifo
            #    com til, o caso 1 nao teria o que provar. Aqui o par
            #    negativo: sobre o Ñ nao ha til NOVO a acrescentar.
            caso("%s %02X: par negativo (til sobre quem ja tem) nao muda"
                 % (nome, alvo), com_til(t, t, tb) == t)
    # 5. o charmap TEM de chamar esses bytes de til, senao o desenho e mentira
    cm = open(os.path.join(RAIZ, "charmap.txt"), encoding="utf-8").read()
    for c, b in (("ã", "F4"), ("õ", "F5"), ("Ã", "F1"), ("Õ", "F2")):
        caso("charmap.txt tem '%s' = %s" % (c, b),
             ("'%s'" % c) in cm and ("= %s" % b) in cm)
    for c in ("'ä'", "'ö'", "'Ä'", "'Ö'"):
        caso("charmap.txt NAO tem mais %s (dois nomes, um byte)" % c,
             c not in cm)
    print("\n%s" % ("demo verde" if ok else "DEMO REPROVOU"))
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--mostrar", action="store_true",
                   help="desenha os quatro glifos de latin_normal.png")
    a = p.parse_args()
    if a.demo:
        return demo()
    if a.mostrar:
        px = Image.open(os.path.join(RAIZ,
                                     "graphics/fonts/latin_normal.png")).load()
        for alvo, _, _, _ in PARES:
            print("=== %02X ===" % alvo)
            print(desenha(celula(px, alvo)))
        return 0
    return 0 if aplica(a.aplicar) >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
