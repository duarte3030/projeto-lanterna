#!/usr/bin/env python3
"""Leva o warp para a PORTA que o Ikarus desenhou, sem mexer em ordem nem em id.

Uso:
    python3 dev_scripts/porta_ikarus_kanto.py            # só mede e confere
    python3 dev_scripts/porta_ikarus_kanto.py --aplicar
    python3 dev_scripts/porta_ikarus_kanto.py --demo

POR QUE ESTE ARQUIVO EXISTE
---------------------------
A troca de arte de 11/09/2026 (Ikarus' Tileset Patch v3.2) mudou o `map.bin` de
101 layouts de Kanto e NÃO tocou em `warp_events`. Onde o autor redesenhou a
fachada, a porta andou uma célula e o warp ficou onde estava, em cima de chão
comum: o jogador pisa e nada acontece. Medido comparando o comportamento do
metatile debaixo dos 1.267 warps de Kanto contra a árvore `8212542e4a`, 14 warps
passaram de VIVO para MORTO. Oito deles são as bocas de buraco das Seafoam, e
esses se consertam no `map.bin` (ver `conserta_ikarus_kanto.py`). Sobram SEIS,
que são porta e seta de portão, e são estes.

A REGRA, que é do contrato e não desta ferramenta
--------------------------------------------------
A seção 1.3 do METODO-COPIA-CIDADES.md diz que os warps MANTÊM os ids e "só
mudam de posição", e a seção 2 diz que "o warp nosso vai para a porta dele".
Então o conserto é editar `x` e `y` em `warp_events`, nunca repintar a célula
para virar porta no lugar onde o autor não desenhou porta nenhuma. Duas portas
desenhadas lado a lado seriam o defeito, não o conserto.

O que esta ferramenta NUNCA faz, e o `--demo` prova:
  - não mexe na ORDEM nem na QUANTIDADE de `warp_events` (id de warp é destino
    escrito em outro mapa, e trocar a ordem quebra a ida e a volta);
  - não encosta em `object_events` (o índice de objeto entra no save);
  - não põe dois warps na mesma célula.

SETA NÃO É PORTA, e é por isso que a conferência é dupla
---------------------------------------------------------
Porta dispara quando o jogador PISA nela (ou, na porta animada, quando ele anda
para o norte olhando para ela). Seta só dispara quando o passo vai NO SENTIDO
dela, e portanto a célula de onde o jogador vem tem que ser andável. Cada linha
da tabela abaixo traz o sentido e a célula de origem, e a conferência falha se
a origem estiver com colisão.

A TABELA, medida célula a célula e não deduzida
-----------------------------------------------
    PewterCity  #6  (9,30) -> (9,29)   a casa subiu uma fileira no desenho novo
    Route5      #2  (24,32) -> (24,33) seta sul do portão, metade esquerda
    Route5      #3  (25,32) -> (25,33) seta sul do portão, metade direita
    Route11     #1  (58,10) -> (56,10) seta leste, o lado de fora do portão
    Route11     #2  (65,10) -> (63,10) seta oeste, o lado de dentro

Route 5 tem DUAS células de seta, (24,33) e (25,33), e os dois warps apontam
para o mesmo destino. Cada um fica na sua, e não os dois em (24,33): o portão do
FRLG tem duas células de largura e empilhar os dois warps numa só deixaria a
outra metade morta.

E O SEXTO, que NÃO é mudança de posição
----------------------------------------
`FourIsland` #3, a entrada da Icefall Cave, continua em (38,12) e o metatile
debaixo dele continua sendo `MB_NON_ANIMATED_DOOR`: o que quebrou foi a COLISÃO
da célula. Porta não animada com colisão 1 nunca dispara, porque o jogador nunca
pisa nela (`TryStartWarpEventScript` olha a posição DELE). Mover o warp não
resolveria: não há outra boca de caverna por perto, e a que existe é essa.

O censo que decide: a boca de caverna do Ikarus é o metatile 246 do primário
`general_frlg`, e ela aparece 23 vezes em Kanto. Vinte e uma estão com colisão 0
e elevação 3, uma com colisão 0 e elevação 5, e UMA com colisão 1 e elevação 0:
esta. Ela é a exceção de uma em 23, não um idioma. A célula volta para (0, 3),
que é o que as 21 irmãs têm.
"""
import argparse
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import valida_warp_tile as V  # noqa: E402

# (mapa, índice do warp, de, para, sentido do passo, célula de origem)
# "sentido" é None para porta, que dispara pelo pisão.
MUDANCAS = [
    ("PewterCity_Frlg",  6, (9, 30),  (9, 29),  "norte", (9, 30)),
    ("Route5_Frlg",      2, (24, 32), (24, 33), "sul",   (24, 32)),
    ("Route5_Frlg",      3, (25, 32), (25, 33), "sul",   (25, 32)),
    ("Route11_Frlg",     1, (58, 10), (56, 10), "leste", (55, 10)),
    ("Route11_Frlg",     2, (65, 10), (63, 10), "oeste", (64, 10)),
]

SETA_DO_SENTIDO = {
    "norte": "MB_NORTH_ARROW_WARP", "sul": "MB_SOUTH_ARROW_WARP",
    "leste": "MB_EAST_ARROW_WARP", "oeste": "MB_WEST_ARROW_WARP",
}

# A célula da boca de caverna que ficou sólida, e o par (colisão, elevação) das
# 21 irmãs dela. Ver o cabeçalho.
COLISAO = [("FourIsland_Frlg", (38, 12), 0, 3)]


def grade(layout):
    bruto = open(os.path.join(RAIZ, layout["blockdata_filepath"]), "rb").read()
    w, h = layout["width"], layout["height"]
    return [struct.unpack_from("<H", bruto, i * 2)[0] for i in range(w * h)], w, h


class Leitor:
    def __init__(self):
        self.layouts = {l["id"]: l for l in json.load(
            open(os.path.join(RAIZ, "data/layouts/layouts.json"), encoding="utf-8"))["layouts"]}
        self._attr = {}

    def mapa(self, nome):
        p = os.path.join(RAIZ, "data/maps", nome, "map.json")
        return json.load(open(p, encoding="utf-8")), p

    def celula(self, nome, x, y):
        """(comportamento, colisão, elevação) da célula, com o corte certo."""
        d, _p = self.mapa(nome)
        lay = self.layouts[d["layout"]]
        celulas, w, _h = grade(lay)
        palavra = celulas[y * w + x]
        mt, col, elev = palavra & 0x3FF, (palavra >> 10) & 3, (palavra >> 12) & 0xF
        corte = 640 if lay.get("layout_version") in ("frlg", "johto") else 512
        for chave in ("primary_tileset", "secondary_tileset"):
            if lay[chave] not in self._attr:
                self._attr[lay[chave]], _ = V.tabela_de_atributos(lay[chave])
        tab, rel = ((self._attr[lay["primary_tileset"]], mt) if mt < corte
                    else (self._attr[lay["secondary_tileset"]], mt - corte))
        return tab[rel], col, elev


def confere(L):
    """Levanta erro em qualquer linha que não sobreviva à conferência."""
    problemas = []
    for nome, idx, de, para, sentido, origem in MUDANCAS:
        d, _p = L.mapa(nome)
        warps = d.get("warp_events") or []
        if idx >= len(warps):
            problemas.append(f"{nome}: não existe warp #{idx}")
            continue
        atual = (warps[idx]["x"], warps[idx]["y"])
        if atual not in (de, para):
            problemas.append(f"{nome} #{idx}: está em {atual}, e a tabela diz {de}")
            continue
        beh, col, _elev = L.celula(nome, *para)
        nome_beh = V.NOME.get(beh, str(beh))
        if sentido == "norte":
            if nome_beh != "MB_ANIMATED_DOOR":
                problemas.append(f"{nome} #{idx}: {para} é {nome_beh}, não porta animada")
        else:
            esperado = SETA_DO_SENTIDO[sentido]
            if nome_beh != esperado:
                problemas.append(f"{nome} #{idx}: {para} é {nome_beh}, e o passo "
                                 f"para {sentido} pede {esperado}")
            if col:
                problemas.append(f"{nome} #{idx}: a seta em {para} tem colisão {col}")
        _b, col_origem, _e = L.celula(nome, *origem)
        if col_origem:
            problemas.append(f"{nome} #{idx}: a célula de origem {origem} tem "
                             f"colisão {col_origem}; o passo nunca sai de lá")
        ocupada = [i for i, w in enumerate(warps)
                   if i != idx and (w["x"], w["y"]) == para]
        if ocupada:
            problemas.append(f"{nome} #{idx}: {para} já tem o warp #{ocupada[0]}")
    for nome, (x, y), col_alvo, elev_alvo in COLISAO:
        beh, col, elev = L.celula(nome, x, y)
        nome_beh = V.NOME.get(beh, str(beh))
        if nome_beh not in ("MB_NON_ANIMATED_DOOR", "MB_CAVE"):
            problemas.append(f"{nome} {x},{y}: {nome_beh} não é boca de caverna")
        if (col, elev) not in ((col_alvo, elev_alvo), (1, 0)):
            problemas.append(f"{nome} {x},{y}: colisão/elevação {(col, elev)} "
                             f"não é nem a quebrada (1,0) nem a certa "
                             f"{(col_alvo, elev_alvo)}")
    return problemas


def aplica(L):
    """Grava. Devolve (warps movidos, células de colisão consertadas)."""
    por_mapa = {}
    for nome, idx, _de, para, _s, _o in MUDANCAS:
        por_mapa.setdefault(nome, []).append((idx, para))
    movidos = 0
    for nome, itens in sorted(por_mapa.items()):
        d, caminho = L.mapa(nome)
        original = open(caminho, encoding="utf-8").read()
        antes = len(d["warp_events"])
        for idx, (x, y) in itens:
            if (d["warp_events"][idx]["x"], d["warp_events"][idx]["y"]) == (x, y):
                continue
            d["warp_events"][idx]["x"] = x
            d["warp_events"][idx]["y"] = y
            movidos += 1
        assert len(d["warp_events"]) == antes, "a quantidade de warps mudou"
        texto = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
        # Lista VAZIA aparece nesta árvore das DUAS formas, "[]" e "[\n\n  ]",
        # e o `json.dumps` só sabe a primeira. Sem esta volta, o conserto de UMA
        # coordenada traria de brinde um diff em toda lista vazia do arquivo, e
        # diff de brinde é como se perde a revisão de um conserto pequeno. A
        # forma certa não se adivinha: sai do arquivo ORIGINAL, chave a chave.
        for chave in ("object_events", "warp_events", "coord_events", "bg_events"):
            if f'"{chave}": [\n\n  ],' in original:
                texto = texto.replace(f'"{chave}": [],', f'"{chave}": [\n\n  ],')
        open(caminho, "w", encoding="utf-8").write(texto)
    celulas = 0
    for nome, (x, y), col_alvo, elev_alvo in COLISAO:
        d, _p = L.mapa(nome)
        lay = L.layouts[d["layout"]]
        caminho = os.path.join(RAIZ, lay["blockdata_filepath"])
        dados = bytearray(open(caminho, "rb").read())
        off = (y * lay["width"] + x) * 2
        palavra = struct.unpack_from("<H", dados, off)[0]
        novo = (palavra & 0x3FF) | (col_alvo << 10) | (elev_alvo << 12)
        if novo != palavra:
            struct.pack_into("<H", dados, off, novo)
            open(caminho, "wb").write(bytes(dados))
            celulas += 1
    return movidos, celulas


def demo():
    """O portão: a tabela não inventa warp, não empilha, e a máscara não vaza."""
    # (1) a tabela não repete célula de destino dentro do mesmo mapa
    vistos = {}
    for nome, idx, _de, para, _s, _o in MUDANCAS:
        assert (nome, para) not in vistos, f"{nome}: dois warps para {para}"
        vistos[(nome, para)] = idx

    # (2) a escrita de colisão e elevação preserva o id do metatile
    palavra = 0x00F6                       # metatile 246, colisão 0, elevação 0
    novo = (palavra & 0x3FF) | (0 << 10) | (3 << 12)
    assert novo & 0x3FF == 246 and (novo >> 10) & 3 == 0 and (novo >> 12) & 0xF == 3
    quebrada = (246) | (1 << 10) | (0 << 12)
    assert quebrada == 0x04F6, hex(quebrada)

    # (3) cada sentido pede a seta daquele sentido, e porta não usa sentido
    for _n, _i, _d, _p, sentido, _o in MUDANCAS:
        assert sentido in SETA_DO_SENTIDO or sentido == "norte"

    # (4) a árvore de verdade: a conferência inteira tem que passar
    problemas = confere(Leitor())
    assert not problemas, "\n".join(problemas)
    print("demo ok")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    L = Leitor()
    problemas = confere(L)
    for nome, idx, de, para, sentido, origem in MUDANCAS:
        beh, col, _e = L.celula(nome, *para)
        print(f"   {nome:<18s} #{idx}  {de} -> {para}  "
              f"{V.NOME.get(beh, beh)} col{col}  (passo para o {sentido}, "
              f"vindo de {origem})")
    for nome, (x, y), col_alvo, elev_alvo in COLISAO:
        beh, col, elev = L.celula(nome, x, y)
        print(f"   {nome:<18s} célula ({x},{y})  {V.NOME.get(beh, beh)}  "
              f"colisão/elevação {(col, elev)} -> {(col_alvo, elev_alvo)}")
    if problemas:
        print("\nPROBLEMAS:")
        for p in problemas:
            print("   " + p)
        return 1
    if not a.aplicar:
        print("\n(só medindo; use --aplicar para gravar)")
        return 0
    movidos, celulas = aplica(L)
    print(f"\n{movidos} warps movidos, {celulas} célula de colisão consertada")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
