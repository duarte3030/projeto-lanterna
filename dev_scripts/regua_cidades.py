#!/usr/bin/env python3
"""Mede o quanto cada CIDADE e VILA do cartucho 1 e "sem graca", e lista as mais pobres.

Contexto (06/09/2026, playtest do Gui): "a cidade esta muito feia, e assim
mesmo?" sobre `CanalaveCity`, e "as cidades sem graca do ROM hack voce podia dar
uma enfeitada tematica". A regua de arte que ja existia (`completude.py`,
`PISO_ARTE = 10`) conta metatiles DISTINTOS por mapa, e essa conta nao enxerga o
defeito que o Gui viu: Canalave tem 201 metatiles distintos, muito acima do
piso, e mesmo assim a praca dela e um tapete cinza liso de centenas de celulas
iguais. Vocabulario grande com repeticao grande continua sendo mapa sem graca.

As tres colunas desta regua, e o motivo de cada uma:

  - `liso`: quantos por cento das celulas ANDAVEIS de exterior usam o metatile
    mais comum do mapa. E a coluna que casa com o olho: e o "tapete" de chao
    repetido. Canalave marca 35,5% num mapa de 1.342 celulas andaveis, ou seja
    477 celulas exatamente iguais.
  - `liso3`: o mesmo somando os TRES metatiles mais comuns. Separa o mapa que
    tem um chao so do que tem chao + duas costuras, que e o caso do demake de
    Sinnoh (o conversor emite pouca variante).
  - `d/100`: metatiles distintos por 100 celulas andaveis. E densidade, nao
    contagem: um mapa de 70x64 com 250 metatiles distintos e MAIS pobre que uma
    vila de 20x20 com 100, e a contagem crua diz o contrario.

E mais duas de cenario, lidas do `map.json`: `plc` (bg_events, as placas e os
sinais) e `obj` (object_events). Elas nao entram na nota; estao aqui porque
mapa sem placa e sem NPC tambem le como vazio, e a lista precisa mostrar isso
ao lado do desenho.

QUEM ENTRA NA CONTA. `map_type` TOWN ou CITY das quatro regioes do cartucho 1
(Kanto, Johto, Hoenn, Sinnoh; Unova e Galar sao do cartucho 2 e ficam fora por
decisao de escopo). O `map_type` sozinho nao basta: o conversor do demake de
Sinnoh carimbou TOWN em lago, rota e floresta (`Route220`, `LakeValor`,
`EternaForest`, `ValleyWindworks`), e esses nao sao cidade. Saem por NOME, em
`NAO_E_CIDADE`, e a lista de fora e impressa junto para ninguem achar que
sumiram calados. Saem tambem os mapas de menos de `PISO_CELULAS` celulas
andaveis, que sao os tres cotocos 1x1 da Battle Zone (`FightArea`,
`SurvivalArea`, `ResortArea`), ja cortados do denominador pelos CORTES_DO_GUI.

QUEM PODE SER ENFEITADO. Medir e uma coisa, mexer e outra. `--pobres` marca com
`vanilla` todo mapa cujo `map.bin` nunca recebeu commit NOSSO (`git log
--follow`): sao os de Kanto (portados do pokefirered) e os de Hoenn (Emerald
intocado). Sala pequena do Emerald e decisao da Game Freak, nao defeito nosso,
e a mesma regra ja valia em `arte_mapas_pobres.py` para os 21 pobres de Hoenn.

Uso:
    python3 dev_scripts/regua_cidades.py            # tabela inteira
    python3 dev_scripts/regua_cidades.py --pobres   # so as 10 mais pobres
    python3 dev_scripts/regua_cidades.py --json     # saida para outra ferramenta
    python3 dev_scripts/regua_cidades.py --demo     # auto-teste
"""
import collections
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")

REGIOES = ["Kanto", "Johto", "Hoenn", "Sinnoh"]

# TOWN/CITY que nao e cidade: o conversor do demake carimbou o tipo errado.
NAO_E_CIDADE = re.compile(
    r"^(Route\d|Lake[A-Z]|.*Forest$|MtSilver|SafariZoneGate|ValleyWindworks"
    r"|.*_Connection_)", re.I)

# Abaixo disso o mapa e cotoco, nao cidade. Os tres da Battle Zone tem UMA
# celula andavel cada.
PISO_CELULAS = 20

# Quantas cidades a lista curta mostra.
QUANTAS = 10


def _completude():
    import completude
    return completude


def _layouts(_c={}):
    if not _c:
        d = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
        _c.update({l["id"]: l for l in d["layouts"] if l.get("id")})
    return _c


def cidades():
    """[(regiao, nome_do_mapa)] de toda cidade e vila do cartucho 1, e as recusadas."""
    C = _completude()
    grupo = C.todos_os_mapas(RAIZ)
    dentro, fora = [], []
    for regiao in REGIOES:
        for nome in sorted(C.nossos_da_regiao(grupo, C.REGIOES[regiao]["grupo"])):
            p = f"{RAIZ}/data/maps/{nome}/map.json"
            if not os.path.isfile(p):
                continue
            d = json.load(open(p))
            if d.get("map_type") not in ("MAP_TYPE_TOWN", "MAP_TYPE_CITY"):
                continue
            if NAO_E_CIDADE.match(nome):
                fora.append((regiao, nome, "nao e cidade (nome)"))
                continue
            dentro.append((regiao, nome))
    return dentro, fora


def base_do_secundario(layout):
    """Onde comeca o indice de metatile do SECUNDARIO neste layout.

    512 no `layout_version: "emerald"` (Hoenn e Sinnoh) e 640 no `johto`, que e
    `bigPrimary` (`NUM_METATILES_IN_PRIMARY_FRLG` de `include/fieldmap.h`, e o
    `tools/mapjson/mapjson.cpp` e quem traduz a versao do layout em
    `bigPrimary`). Ate 09/09/2026 a regua cravava 512 por herdar o
    `comportamento()` de `arte_ginasios_sinnoh.py`, que nasceu para Sinnoh, e
    por isso lia TODA cidade de Johto no lugar errado: o metatile da faixa 512 a
    639, que e do primario, era procurado no secundario, e o metatile alto do
    secundario caia fora do arquivo e voltava comportamento 0. Como o
    comportamento so serve aqui para tirar a AGUA da conta, o estrago aparecia
    como celula de agua contada como chao andavel (ou o contrario), o que move
    a coluna `liso` das cidades de Johto.

    KANTO CONTINUA EM 512 DE PROPOSITO, e isso NAO e o mesmo defeito. Os
    layouts `frlg` tambem sao `bigPrimary`, mas o
    `data/tilesets/primary/general_frlg/metatile_attributes.bin` deste
    repositorio tem 2.560 bytes para 640 metatiles, ou seja atributo de
    **4 bytes**, e nao de 2 como o resto do repo (medido: as palavras saem no
    padrao 29, 0x2000, 29, 0x2000, que e comportamento seguido de layerType).
    Ninguem nesta arvore sabe ler esse formato, e mudar so a base faria a regua
    trocar uma leitura errada por outra leitura errada, calada. Enquanto o
    formato de 4 bytes nao for tratado, as linhas de Kanto desta regua sao
    leitura APROXIMADA e estao registradas como risco aberto no ESTADO.
    """
    versao = (layout.get("layout_version") or "emerald") if layout else "emerald"
    return 640 if versao == "johto" else 512


def _beh_agua():
    import enfeita_cidades
    return enfeita_cidades.agua()


def mede(nome):
    """As tres colunas de desenho e as duas de cenario de um mapa.

    "Andavel" e andavel A PE. A primeira versao contava so `colisao == 0`, e a
    AGUA do Emerald tem colisao 0 (quem barra e a elevacao, e quem atravessa e o
    Surf): em Canalave isso fazia o metatile mais comum "andavel" ser o RIO, com
    477 das 1.342 celulas, e a coluna `liso` marcava 35,5% de "chao liso" que era
    canal. Com a agua fora, Canalave marca 27,5% e Snowpoint sobe para 87,5%,
    que e o retrato certo: a praca de neve dela e um lencol de um metatile so.
    """
    d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))
    L = _layouts()[d["layout"]]
    W, H = L["width"], L["height"]
    b = open(f"{RAIZ}/{L['blockdata_filepath']}", "rb").read()
    n = min(W * H, len(b) // 2)
    celulas = struct.unpack_from("<%dH" % n, b, 0)
    import arte_ginasios_sinnoh as G
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"],
                          base_do_secundario(L))
    AG = _beh_agua()
    metatiles = [c & 0x3FF for c in celulas]
    andavel = [metatiles[i] for i in range(n)
               if not ((celulas[i] >> 10) & 3) and beh(metatiles[i]) not in AG]
    if len(andavel) < PISO_CELULAS:
        return None
    freq = collections.Counter(andavel)
    top = freq.most_common(3)
    return {
        "mapa": nome, "w": W, "h": H,
        "andaveis": len(andavel),
        "distintos": len(set(metatiles)),
        "dens": round(len(set(metatiles)) * 100.0 / len(andavel), 2),
        "liso": round(top[0][1] * 100.0 / len(andavel), 1),
        "liso3": round(sum(v for _, v in top) * 100.0 / len(andavel), 1),
        "chao": top[0][0],
        "placas": len(d.get("bg_events") or []),
        "objetos": len(d.get("object_events") or []),
    }


def _nosso(nome, regiao, _c={}):
    """True se o `map.bin` DIFERE do da fonte da regiao. Igual byte a byte = vanilla.

    A primeira versao perguntava ao `git log --follow` se algum commit "nosso"
    tinha tocado o arquivo, e ERRAVA: `LittlerootTown/map.bin` so tem dois
    commits, `f61810a8f9 Dump maps` e `89d35e82a2 Move 'map attributes' into
    'layouts'`, e o segundo nao esta em nenhuma lista de assunto de upstream que
    de para escrever sem chutar. Com ele, os quatro mapas vanilla de Hoenn
    (Littleroot, Dewford, Lavaridge, Mauville) entraram na lista de intervencao.
    Comparar BYTE A BYTE com a fonte e medicao, nao heuristica: Kanto sai do
    pokefirered e Hoenn do pokeemerald, os dois no mesmo formato. Johto e
    Sinnoh nao tem fonte comparavel (gen 2 e gen 4, outro formato), entao todo
    mapa deles e nosso por construcao, que e a verdade: foram convertidos aqui.
    """
    chave = (nome, regiao)
    if chave in _c:
        return _c[chave]
    fontes = {"Kanto": "pokefirered", "Hoenn": "pokeemerald"}
    resposta = True
    if regiao in fontes:
        L = _layouts()[json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))["layout"]]
        rel = L["blockdata_filepath"]
        base = f"{_completude().FONTES}/{fontes[regiao]}"
        # Kanto entrou com o sufixo `_Frlg` na pasta de layout
        # (`PalletTown_Frlg`), e a fonte nao tem: sem tirar o sufixo, TODO mapa
        # de Kanto some da comparacao e passa por nosso.
        tenta = [f"{base}/{rel}", f"{base}/{rel.replace('_Frlg/', '/')}"]
        for fonte in tenta:
            if os.path.exists(fonte):
                resposta = (open(fonte, "rb").read()
                            != open(f"{RAIZ}/{rel}", "rb").read())
                break
    _c[chave] = resposta
    return resposta


def tabela():
    dentro, fora = cidades()
    linhas = []
    for regiao, nome in dentro:
        m = mede(nome)
        if m is None:
            fora.append((regiao, nome, "cotoco: menos de %d celulas andaveis" % PISO_CELULAS))
            continue
        m["regiao"] = regiao
        linhas.append(m)
    linhas.sort(key=lambda m: (-m["liso"], m["dens"]))
    return linhas, fora


def imprime(linhas, fora, so_pobres=False, com_vanilla=True):
    cab = ("%-7s %-30s %-9s %6s %5s %6s %6s %6s %4s %4s %s"
           % ("regiao", "mapa", "w x h", "andav", "dist", "d/100", "liso", "liso3",
              "plc", "obj", "dono"))
    print(cab)
    print("-" * len(cab))
    mostradas = 0
    for m in linhas:
        dono = ""
        if com_vanilla:
            dono = "nosso" if _nosso(m["mapa"], m["regiao"]) else "vanilla"
        if so_pobres:
            if dono == "vanilla":
                continue
            if mostradas >= QUANTAS:
                break
            mostradas += 1
        print("%-7s %-30s %-9s %6d %5d %6.2f %5.1f%% %5.1f%% %4d %4d %s"
              % (m["regiao"], m["mapa"], "%dx%d" % (m["w"], m["h"]), m["andaveis"],
                 m["distintos"], m["dens"], m["liso"], m["liso3"], m["placas"],
                 m["objetos"], dono))
    if not so_pobres:
        print("\n%d cidades e vilas medidas." % len(linhas))
        print("fora da conta (%d):" % len(fora))
        for regiao, nome, motivo in sorted(fora):
            print("  %-7s %-30s %s" % (regiao, nome, motivo))


def demo():
    """Casos que ja quebraram esta regua, ou que ela existe para pegar."""
    mau = []
    linhas, fora = tabela()
    por_nome = {m["mapa"]: m for m in linhas}

    # 0. A AGUA nao conta como chao andavel. Se contasse, Canalave marcaria o
    #    rio como "chao liso" e a regua leria 35,5% em vez de 27,5%.
    if "CanalaveCity" in por_nome and por_nome["CanalaveCity"]["andaveis"] > 1300:
        mau.append("CanalaveCity com %d celulas andaveis: a agua voltou a contar"
                   % por_nome["CanalaveCity"]["andaveis"])

    # 1. Canalave entra, e entra pobre. E o mapa da reclamacao do Gui.
    if "CanalaveCity" not in por_nome:
        mau.append("CanalaveCity ficou fora da conta")
    else:
        m = por_nome["CanalaveCity"]
        if m["liso"] < 20:
            mau.append("CanalaveCity com liso %.1f%%, esperado 20%%+" % m["liso"])
        if m["distintos"] < 100:
            mau.append("CanalaveCity com %d distintos: leitura errada do map.bin"
                       % m["distintos"])

    # 2. O que NAO e cidade tem que sair, e Route220 e o caso que enganou a
    #    primeira versao (map_type TOWN numa rota).
    nomes = {m["mapa"] for m in linhas}
    for falso in ("Route220", "LakeValor", "EternaForest", "ValleyWindworks"):
        if falso in nomes:
            mau.append("%s entrou como cidade" % falso)

    # 3. Os tres cotocos 1x1 da Battle Zone sao cortados pelo piso de celulas.
    for cotoco in ("FightArea", "SurvivalArea", "ResortArea"):
        if cotoco in nomes:
            mau.append("%s (1x1) entrou como cidade" % cotoco)

    # 4. As quatro regioes aparecem, e nenhuma das duas de fora aparece.
    regs = {m["regiao"] for m in linhas}
    if regs != set(REGIOES):
        mau.append("regioes medidas %s, esperado %s" % (sorted(regs), REGIOES))

    # 5. Mapa vanilla de Kanto e de Hoenn e reconhecido como vanilla, e um de
    #    Sinnoh como nosso. Sem isso a lista de intervencao pega mapa da Game
    #    Freak: foi exatamente o que a versao por `git log` fez com Littleroot,
    #    Dewford, Lavaridge e Mauville.
    if _nosso("LittlerootTown", "Hoenn"):
        mau.append("LittlerootTown marcado como nosso")
    if _nosso("PalletTown_Frlg", "Kanto"):
        mau.append("PalletTown_Frlg marcado como nosso")
    if not _nosso("CanalaveCity", "Sinnoh"):
        mau.append("CanalaveCity marcado como vanilla")

    # 6. `liso` e mesmo a fracao do metatile mais comum: conferido na mao.
    m = por_nome["CanalaveCity"]
    L = _layouts()[json.load(open(f"{RAIZ}/data/maps/CanalaveCity/map.json"))["layout"]]
    b = open(f"{RAIZ}/{L['blockdata_filepath']}", "rb").read()
    cel = struct.unpack_from("<%dH" % (L["width"] * L["height"]), b, 0)
    import arte_ginasios_sinnoh as G
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"],
                          base_do_secundario(L))
    AG = _beh_agua()
    andavel = [c & 0x3FF for c in cel
               if not ((c >> 10) & 3) and beh(c & 0x3FF) not in AG]
    esperado = round(collections.Counter(andavel).most_common(1)[0][1] * 100.0
                     / len(andavel), 1)
    if abs(esperado - m["liso"]) > 0.05:
        mau.append("liso %.1f != conta na mao %.1f" % (m["liso"], esperado))

    # 7. A base do secundario e 640 em Johto e 512 em Sinnoh, e o caso traz o
    #    PAR NEGATIVO dentro dele: com a base forcada de volta para 512, alguma
    #    cidade de Johto tem que MUDAR de leitura. Sem essa metade o caso passa
    #    a valer nada no dia em que alguem "consertar" o conserto.
    lay_johto = _layouts()[json.load(
        open(f"{RAIZ}/data/maps/BlackthornCity/map.json"))["layout"]]
    lay_sinnoh = _layouts()[json.load(
        open(f"{RAIZ}/data/maps/CanalaveCity/map.json"))["layout"]]
    if base_do_secundario(lay_johto) != 640:
        mau.append("base do secundario de BlackthornCity != 640")
    if base_do_secundario(lay_sinnoh) != 512:
        mau.append("base do secundario de CanalaveCity != 512")
    import arte_ginasios_sinnoh as G7
    mudou = []
    for cidade in ("CianwoodCity", "BlackthornCity", "GoldenrodCity",
                   "EcruteakCity", "OlivineCity", "AzaleaTown", "VioletCity"):
        L7 = _layouts()[json.load(
            open(f"{RAIZ}/data/maps/%s/map.json" % cidade))["layout"]]
        b7 = open(f"{RAIZ}/{L7['blockdata_filepath']}", "rb").read()
        n7 = min(L7["width"] * L7["height"], len(b7) // 2)
        cel7 = struct.unpack_from("<%dH" % n7, b7, 0)
        AG7 = _beh_agua()
        conta = {}
        for base in (640, 512):
            f7 = G7.comportamento(L7["primary_tileset"], L7["secondary_tileset"], base)
            conta[base] = sum(1 for c in cel7
                              if not ((c >> 10) & 3) and f7(c & 0x3FF) not in AG7)
        if conta[640] != conta[512]:
            mudou.append(cidade)
    if not mudou:
        mau.append("com a base forcada para 512 NENHUMA cidade de Johto muda: "
                   "o caso 7 nao esta provando nada")

    if mau:
        print("DEMO VERMELHA")
        for x in mau:
            print("  -", x)
        return 1
    print("DEMO VERDE: %d cidades medidas, %d fora, 8 casos" % (len(linhas), len(fora)))
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    linhas, fora = tabela()
    if "--json" in sys.argv:
        for m in linhas:
            m["dono"] = "nosso" if _nosso(m["mapa"], m["regiao"]) else "vanilla"
        print(json.dumps(linhas, indent=1, ensure_ascii=False))
        return 0
    imprime(linhas, fora, so_pobres="--pobres" in sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
