#!/usr/bin/env python3
"""Reprova ASSET_ALIAS cujo asset deixou de ser igual ao do canônico.

Uso:
    python3 dev_scripts/guarda_alias.py            # varredura (0 = verde)
    python3 dev_scripts/guarda_alias.py --lista    # imprime também os apelidos íntegros
    python3 dev_scripts/guarda_alias.py --demo     # autoteste com mutação plantada

Não precisa de build: lê só os arquivos versionados.

Por que existe
--------------
`dedupe_assets.py` troca a definição duplicada de um asset por um ALIAS de link
(`ASSET_ALIAS`), medindo os bytes convertidos no momento em que roda. O apelido
custa zero byte de ROM, mas cria uma armadilha silenciosa: dali em diante os
dois símbolos são o MESMO endereço, e quem editar só um dos lados muda o outro
sem pedir e sem erro de build.

Foi o que aconteceu em 11/09/2026. `gTilesetPalettes_EverGrandeSinnoh` era
apelido de `gTilesetPalettes_EverGrande`. Quando Hoenn recebeu as paletas do
Blazing Emerald v1.6, o apelido levou as cores novas para os mapas de SINNOH
que usam `gTileset_EverGrandeSinnoh` (`LAYOUT_POKMON_LEAGUE` e `LAYOUT_ROUTE224`):
11,23% dos pixels da Liga mudaram sem ninguém pedir. Nada ficou vermelho, porque
os arquivos de Sinnoh no disco continuavam certos; só o símbolo é que era o de
Hoenn. Render que lê pasta de tileset (`render_maps.py`) também não vê: o erro
mora no link, não na árvore.

Por que ele compara a FONTE, e não a saída do build
---------------------------------------------------
Tentei primeiro comparar `build.nosync/assets/`, que é o que `dedupe_assets.py`
mede. Não serve, e a razão é do próprio mecanismo: assim que um símbolo vira
alias, o `INCBIN`/`INCGFX` dele some, o `make` PARA de converter a fonte do
apelido, e não existe saída de build para comparar. Medido em 11/09/2026: de
414 apelidos, só 39 ainda tinham saída, e nenhuma paleta de tileset (a família
que quebrou) estava entre eles.

Então ele compara os arquivos versionados, normalizando exatamente o que o
`gbagfx` também descarta, e nada além disso:

    .pal (JASC-PAL)  números das cores, sem ligar para CRLF nem espaço.
    .png para paleta  as 16 primeiras cores da paleta do PNG.
    .png para tiles   o plano de ÍNDICES (`Image.tobytes()`), não o RGB.
    o resto (.bin)    bytes crus.

E em toda cor, os três canais entram em BGR555 (`>> 3`), porque é o que a ROM
guarda: dois PNG com `#F8F8F8` e `#FFFFFF` viram a mesma cor no GBA. Sem essa
quantização a varredura acusava 33 famílias que estão certas, e validador com
falso positivo ensina a ignorar a saída.
"""
import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFESTO = os.path.join(RAIZ, "dev_scripts", "dedupe_assets.json")
PREFIXO_BUILD = "build.nosync/assets/"

# O nome do símbolo é o único lugar onde a região aparece, e roda_qa.py conta
# por região. Sem isto tudo cairia na coluna "comum".
REGIOES = ("Sinnoh", "Johto", "Kanto", "Unova", "Galar", "Hoenn")

# Achado REAL, medido, que este executor não conserta: o dono é outra frente.
# Mesma convenção do `PENDENTES` de `prova_blazing_bytes.py`. Sai da lista quando
# a frente dona consertar; não entra nada aqui sem dono escrito.
#   CONSERTADO EM 11/09/2026 e por isso a lista está VAZIA:
#   gTilesetTiles_KantoGeneral era apelido de gTilesetTiles_General_Frlg, o Ikarus
#   Tileset Patch v3.2 (commit 44009d0aab) trocou general_frlg/tiles.png, e o
#   apelido levou a arte de KANTO para NationalPark_Layout e
#   NationalPark_BugContest_Layout, que são de JOHTO. O símbolo ganhou INCGFX
#   próprio apontando para data/tilesets/primary/kanto_general/tiles.png, que no
#   disco já era o general_frlg de antes do Ikarus, byte a byte.
PENDENTES = set()


def regiao_de(nome):
    for r in REGIOES:
        if r in nome:
            return r
    return "comum"


def _fonte_versionada(raiz, fonte):
    """build.nosync/assets/<x>.<conversões> -> o arquivo que o repo versiona."""
    caminho = fonte[len(PREFIXO_BUILD):] if fonte.startswith(PREFIXO_BUILD) else fonte
    while True:
        if os.path.exists(os.path.join(raiz, caminho)):
            return caminho
        if os.path.exists(os.path.join(raiz, caminho + ".png")):
            return caminho + ".png"
        base, ext = os.path.splitext(caminho)
        if not ext:
            return None
        caminho = base


def _artefato(fonte):
    """Que asset o build tira desta fonte: paleta, tiles ou bytes crus."""
    nome = fonte.lower()
    if "gbapal" in nome:
        return "paleta"
    if "4bpp" in nome or "8bpp" in nome:
        return "tiles"
    return "cru"


def assinatura(raiz, fonte):
    """O que a ROM veria desta fonte, sem o que o gbagfx descarta."""
    rel = _fonte_versionada(raiz, fonte)
    if rel is None:
        return None
    artefato = _artefato(fonte)
    caminho = os.path.join(raiz, rel)

    if rel.endswith(".pal"):
        campos = open(caminho, encoding="utf-8", errors="replace").read().split()
        # JASC-PAL: cabeçalho "JASC-PAL", "0100", "<n cores>", depois R G B.
        return ("paleta", tuple(int(v) >> 3 for v in campos[3:]))

    if rel.endswith(".png"):
        from PIL import Image
        imagem = Image.open(caminho)
        if artefato == "paleta":
            paleta = imagem.getpalette() or []
            return ("paleta", tuple(v >> 3 for v in paleta[:48]))
        if imagem.mode != "P":
            return ("tiles", open(caminho, "rb").read())
        return ("tiles", imagem.tobytes())

    return ("cru", open(caminho, "rb").read())


def _assinaturas(raiz, fontes):
    saida = []
    for fonte in fontes:
        try:
            uma = assinatura(raiz, fonte)
        except Exception as erro:  # PNG corrompido, paleta com lixo
            return None, f"{fonte} ({erro})"
        if uma is None:
            return None, fonte
        saida.append(uma)
    return saida, None


def varre(raiz=RAIZ, manifesto=MANIFESTO):
    """Devolve (achados, censo)."""
    with open(manifesto, encoding="utf-8") as fp:
        dados = json.load(fp)

    achados, faltando, iguais, pendentes = [], [], [], []
    for familia in dados["familias"]:
        canonico = familia["canonico"]
        base, faltou = _assinaturas(raiz, canonico["fontes"])
        if base is None:
            faltando.append((canonico["nome"], faltou))
            continue
        for alias in familia["aliases"]:
            atual, faltou = _assinaturas(raiz, alias["fontes"])
            if atual is None:
                faltando.append((alias["nome"], faltou))
            elif atual != base:
                if alias["nome"] in PENDENTES:
                    pendentes.append((alias["nome"], canonico["nome"]))
                    continue
                achados.append({
                    "regra": "AL1",
                    "classe": "trava",
                    "regiao": regiao_de(alias["nome"]),
                    "arquivo": familia["arquivo"],
                    "alias": alias["nome"],
                    "canonico": canonico["nome"],
                    "texto": (f"{alias['nome']} é ASSET_ALIAS de {canonico['nome']}, "
                              "e os arquivos já não batem"),
                })
            else:
                iguais.append((alias["nome"], canonico["nome"]))

    return achados, {"iguais": len(iguais), "pares": iguais, "faltando": faltando,
                     "pendentes": pendentes}


def demo():
    """Autoteste: um apelido que divergiu tem de ser mordido, e só ele."""
    import shutil
    import tempfile

    base = tempfile.mkdtemp(prefix="guarda-alias-demo-")
    try:
        pasta = os.path.join(base, "data", "falso", "palettes")
        os.makedirs(pasta)

        def escreve(nome, cores):
            with open(os.path.join(pasta, nome), "w", encoding="utf-8") as fp:
                fp.write("JASC-PAL\n0100\n%d\n" % len(cores))
                for r, g, b in cores:
                    fp.write(f"{r} {g} {b}\n")

        cores = [(0, 0, 0), (248, 248, 248), (16, 32, 64)]
        escreve("canonico.pal", cores)
        # Mesmas cores, fim de linha e arredondamento diferentes: em BGR555 é a
        # MESMA paleta, então não pode ser mordido.
        with open(os.path.join(pasta, "igual.pal"), "wb") as fp:
            fp.write(b"JASC-PAL\r\n0100\r\n3\r\n0 0 0\r\n255 255 255\r\n17 33 65\r\n")
        escreve("divergiu.pal", [(0, 0, 0), (248, 0, 0), (16, 32, 64)])

        raiz_pal = "data/falso/palettes"
        sintetico = {
            "gerado_por": "demo",
            "familias": [{
                "md5": "0" * 32,
                "bytes": 0,
                "arquivo": "src/falso.h",
                "canonico": {"nome": "gFalso_Canonico",
                             "fontes": [f"{PREFIXO_BUILD}{raiz_pal}/canonico.pal.gbapal"]},
                "aliases": [
                    {"nome": "gFalso_IgualSinnoh",
                     "fontes": [f"{PREFIXO_BUILD}{raiz_pal}/igual.pal.gbapal"]},
                    {"nome": "gFalso_DivergiuSinnoh",
                     "fontes": [f"{PREFIXO_BUILD}{raiz_pal}/divergiu.pal.gbapal"]},
                ],
            }],
        }
        caminho = os.path.join(base, "manifesto.json")
        with open(caminho, "w", encoding="utf-8") as fp:
            json.dump(sintetico, fp)

        achados, censo = varre(raiz=base, manifesto=caminho)
        nomes = [a["alias"] for a in achados]
        if nomes != ["gFalso_DivergiuSinnoh"]:
            print(f"  guarda_alias: esperava morder só o divergente, mordeu {nomes}")
            return 1
        if censo["iguais"] != 1:
            print(f"  guarda_alias: CRLF e arredondamento viraram achado ({censo['iguais']} íntegros)")
            return 1
        if achados[0]["regiao"] != "Sinnoh":
            print(f"  guarda_alias: região saiu {achados[0]['regiao']}")
            return 1
        return 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lista", action="store_true", help="imprime os apelidos íntegros também")
    ap.add_argument("--demo", action="store_true", help="autoteste com mutação plantada")
    args = ap.parse_args()
    if args.demo:
        codigo = demo()
        print("DEMO VERDE" if codigo == 0 else "DEMO REPROVOU")
        return codigo

    achados, censo = varre()
    for alias, canonico in censo["pendentes"]:
        print(f"PENDENTE  {alias} (alias de {canonico}) divergiu, e o conserto é de outra "
              "frente; ver PENDENTES no topo deste arquivo")
    if args.lista:
        for alias, canonico in censo["pares"]:
            print(f"IGUAL  {alias} -> {canonico}")
    if censo["faltando"]:
        # Manifesto citando arquivo que saiu da árvore (Galar, cortada do
        # cartucho 1). Não é defeito de alias: é entrada velha de manifesto.
        print(f"AVISO: {len(censo['faltando'])} entrada(s) do manifesto sem arquivo na árvore")
        for nome, fonte in censo["faltando"][:10]:
            print(f"  {nome}: {fonte}")
        if len(censo["faltando"]) > 10:
            print(f"  ... e mais {len(censo['faltando']) - 10}")

    if achados:
        print()
        print(f"ACHADO: {len(achados)} alias com asset diferente do canônico")
        for a in achados:
            print(f"  {a['arquivo']}: {a['texto']}")
        print()
        print("Conserto: dar asset próprio ao apelido (INCBIN/INCGFX dele mesmo) ou igualar os")
        print("dois lados de propósito. Alias que deixou de valer pinta mapa errado sem avisar.")
        return 1

    print(f"ALIAS COERENTE: {censo['iguais']} apelidos conferidos, "
          "todos com arquivo igual ao do canônico")
    return 0


if __name__ == "__main__":
    sys.exit(main())
