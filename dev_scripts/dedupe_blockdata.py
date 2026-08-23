#!/usr/bin/env python3
"""Deduplica blockdata e borda de layout em data/layouts/layouts.inc.

O `mapjson layouts` emite um `.incbin` por layout, mesmo quando dois layouts têm
o MESMO `map.bin` byte a byte (462 dos 2.064 mapas são cópia exata de outro, o
grosso vindo dos interiores repetidos de Galar). Cada cópia paga o tamanho
inteiro em ROM. Este passo roda logo depois do gerador e faz o layout repetido
apontar para o `.incbin` do primeiro, sem tocar em `map.bin`, em `layouts.json`
nem no motor: o ponteiro `.map` da `struct MapLayout` passa a ser o mesmo
endereço, e os bytes lidos são exatamente os mesmos de antes.

Uso:
    python3 dev_scripts/dedupe_blockdata.py data/layouts/layouts.inc
    python3 dev_scripts/dedupe_blockdata.py --demo
"""

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ALVO = RAIZ / "data/layouts/layouts.inc"

# NomeDoSimbolo::
# \t.incbin "caminho"
BLOCO = re.compile(r'^(\w+)::\n\t\.incbin "([^"]+)"\n', re.M)


def _hash(caminho):
    return hashlib.md5((RAIZ / caminho).read_bytes()).hexdigest()


def plano(texto):
    """Devolve (aliases, canonicos): alias -> simbolo canonico de conteudo igual."""
    primeiro = {}
    aliases = {}
    for m in BLOCO.finditer(texto):
        nome, caminho = m.group(1), m.group(2)
        h = _hash(caminho)
        if h in primeiro:
            aliases[nome] = primeiro[h]
        else:
            primeiro[h] = nome
    return aliases


def aplica(texto, aliases):
    if not aliases:
        return texto
    # 1. apaga o bloco .incbin do simbolo repetido
    def corta(m):
        return "" if m.group(1) in aliases else m.group(0)
    texto = BLOCO.sub(corta, texto)
    # 2. troca as referencias `.4byte Simbolo` pelo canonico
    ref = re.compile(r'^(\t\.4byte )(' + "|".join(map(re.escape, aliases)) + r')$', re.M)
    texto = ref.sub(lambda m: m.group(1) + aliases[m.group(2)], texto)
    return texto


def confere(antes, depois, aliases):
    """Prova: todo layout continua apontando para os MESMOS bytes de antes."""
    # endereco logico de cada simbolo antes = conteudo do arquivo que ele embutia
    conteudo = {m.group(1): _hash(m.group(2)) for m in BLOCO.finditer(antes)}
    definidos_depois = {m.group(1) for m in BLOCO.finditer(depois)}

    REF = re.compile(r'^\t\.4byte (\w+)$', re.M)
    refs_antes = REF.findall(antes)
    refs_depois = REF.findall(depois)
    assert len(refs_antes) == len(refs_depois), \
        f"numero de referencias mudou: {len(refs_antes)} -> {len(refs_depois)}"

    for a, d in zip(refs_antes, refs_depois):
        if a not in conteudo:          # gTileset_*, referencia que nao e blockdata
            assert a == d, f"referencia nao-blockdata mexida: {a} -> {d}"
            continue
        assert d in definidos_depois, f"{d} ficou sem definicao"
        assert conteudo[a] == conteudo[d], \
            f"{a} apontava para conteudo diferente de {d}"

    for alias, canon in aliases.items():
        assert alias not in definidos_depois, f"{alias} deveria ter sumido"
        assert canon in definidos_depois, f"{canon} sumiu"
        assert conteudo[alias] == conteudo[canon]
    return len(refs_antes)


def economia(texto, aliases):
    total = 0
    for m in BLOCO.finditer(texto):
        if m.group(1) in aliases:
            total += (RAIZ / m.group(2)).stat().st_size
    return total


def recem_gerado():
    """layouts.inc RECEM saido do mapjson, num diretorio temporario.

    O `--demo` lia o arquivo do DISCO, e o disco JA passou por este passo
    dentro do make: la ele acha 0 repetidos e imprime "0 B de volta", verde e
    vazio. E a mesma armadilha dos dois `--demo` consertados em 22/08/2026:
    autoteste tem de saber que o gerador ja rodou, e a linha de base e o
    gerador, nunca o disco.
    """
    saida = Path(tempfile.mkdtemp(prefix="dedupe-blockdata-"))
    subprocess.run([str(RAIZ / "tools/mapjson/mapjson"), "layouts", "emerald",
                    str(RAIZ / "data/layouts/layouts.json"), str(saida),
                    str(saida)], check=True, cwd=RAIZ)
    return saida / "layouts.inc"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo", nargs="?", default=str(ALVO))
    ap.add_argument("--demo", action="store_true",
                    help="mede e confere sem gravar")
    args = ap.parse_args()

    temporario = None
    if args.demo:
        caminho = recem_gerado()
        temporario = caminho.parent
    else:
        caminho = Path(args.arquivo)
    if not caminho.exists():
        print(f"sem {caminho}, nada a fazer")
        return 0

    antes = caminho.read_text(encoding="utf-8")
    aliases = plano(antes)
    depois = aplica(antes, aliases)
    refs = confere(antes, depois, aliases)
    econ = economia(antes, aliases)

    print(f"layouts.inc: {len(BLOCO.findall(antes))} blobs, "
          f"{len(aliases)} repetidos, {refs} referencias conferidas, "
          f"{econ} B ({econ/1024:.1f} KB) de volta")

    if args.demo:
        assert aliases, "nenhum layout repetido no mapjson recem-rodado: ou a fonte mudou ou o plano parou de achar"
        assert econ > 0, econ
        shutil.rmtree(temporario, ignore_errors=True)
        print("demo ok")
        return 0
    if depois != antes:
        caminho.write_text(depois, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
