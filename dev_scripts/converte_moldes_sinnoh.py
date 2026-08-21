#!/usr/bin/env python3
"""Troca o molde de portao 13x9 pela geometria de verdade, na grade do Platinum.

    python3 dev_scripts/converte_moldes_sinnoh.py --dry-run
    python3 dev_scripts/converte_moldes_sinnoh.py --demo
    python3 dev_scripts/converte_moldes_sinnoh.py --aplicar OreburghGateB1F

O que este script conserta
--------------------------
Treze mapas de Sinnoh NAO TEM MAPA: eles vestem o molde de portao de 13x9. O
criterio nunca e nome, e a comparacao de `map.bin` que `planta_provisoria` ja
fazia. Ela sempre pegou os 13; quem enxergava so 12 era a LISTA ESCRITA A MAO
da fila, que escondia o `OreburghGateB1F` (medido em 21/08/2026).

Portao que E portao continua vestindo o molde, e isso esta certo. O que separa
vitima de portao legitimo tambem e medida, nao lista: **portao no Platinum tem a
grade 2D VAZIA**, porque o interior dele e modelo 3D e a grade so marca um aro
fino de parede. O corte e a densidade de colisao, em `PISO_COLISAO`.

De onde sai a geometria
-----------------------
Da mesma grade 2D de 32x32 por tile que o `demake_ds.py` ja lia
(`res/field/maps/data/map_data_NNN.bin`, u16 por tile: bit 15 = colisao, bits
0..7 = comportamento). Duas tradicoes, porque o terreno decide:

- **Caverna** (`MAP_TYPE_CAVE`): a traducao de `converte_cavernas_sinnoh.py`,
  com rocha de duas faces. Vale porque a geometria de uma caverna E a colisao
  dela, e o `0x00` sem colisao ali e vazio fora do mapa, nao chao.
- **Exterior**: a traducao de `demake_ds.traduz_gen4`, com grama, agua e parede
  de arvore. Ali o `0x00` sem colisao E chao.

Alinhamento de coordenada, sem adivinhacao
------------------------------------------
Oito dos treze tem matriz PROPRIA, e nesse caso a coordenada do evento da fonte
ja e local: alinhamento de graca. Os outros dividem a `map_matrix_000`, o mapa
do mundo, e ai o recorte sai das celulas que levam o nome do header, o que da um
offset EXATO em multiplo de 32. Nenhum dos dois caminho usa escala, que e a
regra que a Route 222 ja provou errada.

A porta de volta da Stark Mountain
----------------------------------
A fonte tem UM warp so em `StarkMountainOutside`, para a `StarkMountainRoom1`,
porque no Platinum entra-se ali andando pela matriz do mundo. Converter cru
deixaria a Stark de MAO UNICA, que a licao 4.1 do ESTADO proibe. Decisao do
condutor em 21/08/2026: **inventar a porta de volta para a Route 227**, que e o
que a planta provisoria ja fazia. Ela entra por `PORTAS_INVENTADAS`, declarada e
nao escondida, porque porta que a fonte nao tem tem que estar escrita em algum
lugar que alguem le.

Idempotencia
------------
`--aplicar` marca o `map.json` com `origem_geometria`. Rodar de novo no mesmo
mapa nao escreve nada e diz "ja convertido". O layout novo entra no FIM de
`layouts.json` e o mapa nao muda de lugar em `map_groups.json`, entao nenhum
indice velho anda e a save nao quebra.
"""
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import converte_cavernas_sinnoh as C   # noqa: E402
import demake_ds as D                  # noqa: E402
import fecha_portas_sinnoh as F        # noqa: E402
import importa_npcs_sinnoh as I        # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAT = F.PLAT

# Fracao de tiles COM colisao a partir da qual a grade carrega um mapa de
# verdade. Medido em 21/08/2026 nos 25 mapas do repo que vestem o molde:
#
#   os 12 portoes legitimos       6,3% a 12,7% de colisao
#   as 13 vitimas                25,3% a 97,8% de colisao
#
# O mecanismo, e nao a correlacao: portao do Platinum tem o interior DESENHADO
# em 3D, e a grade 2D dele so marca um aro fino de parede, com o miolo vazio.
# Grade vazia nao tem o que converter, entao ela e o corte certo. Contar tile
# ANDAVEL nao separa e foi a primeira tentativa errada: pela regra frouxa o
# portao parece campo aberto (936 de 1024 livres), e pela regra estrita a
# `SpringPath`, que e vitima, cai junto dos portoes com 2 tiles nomeados.
PISO_COLISAO = 0.20

# Os que JA SAIRAM do molde, e que por isso nao aparecem mais em `alvos()`.
# Existe para o `--demo` continuar afirmando alguma coisa sobre eles: mapa
# convertido some da medida e nenhuma outra checagem do autoteste o alcanca.
# Os 8 que faltam foram CORTADOS do escopo por decisao do Gui em 21/08/2026 e
# ficam vestindo o molde de proposito.
CONVERTIDOS = ("OreburghGateB1F", "IronIsland", "MtCoronetOutsideSouth",
               "MtCoronetOutsideNorth", "Route204North")

# Porta que a FONTE nao tem e nos precisamos, para nao deixar mapa de mao unica.
# mapa nosso -> (mapa destino, warp de destino). Ver o cabecalho.
PORTAS_INVENTADAS = {
    "StarkMountainOutside": ("MAP_ROUTE227", "1"),
}

# Canto de arvore bloqueante do `gTileset_GeneralSinnoh`, o mesmo metatile 470
# que o `demake_ds.traduz_gen4` ja usa para parede de exterior. Formato do
# pokeemerald: 10 bits de metatile, 2 de colisao, 4 de elevacao.
ARVORE_TOPO = 470 | (1 << 10)

# TILE DEBAIXO DO WARP, e ele nao e enfeite: neste motor o warp NAO dispara em
# chao comum, quem dispara e o COMPORTAMENTO do metatile. Warp gravado sobre
# grama vira mapa de mao unica calado, que e a licao 4.1 do ESTADO. Custou uma
# rodada em 21/08/2026: o OreburghGateB1F saiu da primeira conversao com o warp
# em cima do metatile 513 (chao de caverna) e o jogador entrava e nao voltava.
#
# Os dois valores sao os que o `converte_cavernas_sinnoh.py` ja mediu nos mapas
# de caverna do repo, e o 575 e exatamente o que o lado de cima da escada usa
# (`LAYOUT_OREBURGH_GATE_1F` em (19,5), conferido no map.bin).
ESCADA = C.ESCADA    # metatile 575, MB_LADDER: escada entre andares
SAIDA = C.SAIDA      # metatile 519, MB_SOUTH_ARROW_WARP: boca de caverna

# EXTERIOR. Medidos em 21/08/2026 varrendo os `metatile_attributes.bin` dos dois
# tilesets de Sinnoh e conferidos EM USO nos warps que ja funcionam:
#
#   MB_ANIMATED_DOOR      general_sinnoh 33, 65, 97, 461, 475; petalburg 553, 556, 594
#   MB_NON_ANIMATED_DOOR  general_sinnoh 167                (unico)
#   MB_NORTH_ARROW_WARP   general_sinnoh 484; petalburg 574
#   MB_SOUTH_ARROW_WARP   general_sinnoh 36, 311; petalburg 626
#   MB_EAST_ARROW_WARP    general_sinnoh 94                 (unico)
#   MB_WEST_ARROW_WARP    general_sinnoh 93                 (unico)
#
# A escolha e a porta NAO animada e as setas do PRIMARIO, e por dois motivos
# medidos. Primeiro, porta animada e casada com a FACHADA do predio (as 8
# variantes sao portas de casa, de Mart, de Centro; por isso `SandgemTown` usa
# 594, 97 e 65 em tres portas vizinhas), e nao ha fachada nenhuma nestes 11
# mapas ate alguem desenhar. Segundo, `gTileset_GeneralSinnoh` e o primario de
# TODOS os layouts de Sinnoh, entao estes valores valem em caverna e em rua sem
# depender do secundario; as setas do petalburg (574, 626) nao tem irma de leste
# nem de oeste e deixariam metade das bordas sem valor.
PORTA = 167 | (3 << 12)        # MB_NON_ANIMATED_DOOR, em uso na VerityLakefront
SETA = {"N": 484, "S": 36, "L": 94, "O": 93}
SETA = {k: v | (3 << 12) for k, v in SETA.items()}

# Tipos de mapa NOSSOS que contam como subterraneo do outro lado da escada.
SUBTERRANEOS = ("MAP_TYPE_UNDERGROUND", "MAP_TYPE_UNDERWATER")
# ... e os que sao "dentro de alguma coisa", que se entra por porta e nao por
# borda de mapa.
FECHADOS = SUBTERRANEOS + ("MAP_TYPE_INDOOR", "MAP_TYPE_SECRET_BASE")


def comportamento(metatile, primario="gTileset_GeneralSinnoh",
                  secundario="gTileset_CaveSinnoh"):
    """`MB_*` de um metatile, LIDO da tabela de atributos do tileset.

    Existe para o autoteste poder afirmar que os valores acima sao porta de
    verdade em vez de numero decorado. Metatile < 512 mora no primario; o resto
    no secundario, deslocado de 512. Comportamento sao os 9 bits de baixo do u16.
    """
    ts = primario if metatile < 512 else secundario
    pasta = re.sub(r"(?<!^)(?=[A-Z])", "_", ts[len("gTileset_"):]).lower()
    for sub in ("primary", "secondary"):
        caminho = f"{REPO}/data/tilesets/{sub}/{pasta}/metatile_attributes.bin"
        if os.path.exists(caminho):
            b = open(caminho, "rb").read()
            i = (metatile if metatile < 512 else metatile - 512) * 2
            bruto = struct.unpack_from("<H", b, i)[0] & 0x1FF
            nomes = re.findall(r"^\s*(MB_\w+)", open(
                f"{REPO}/include/constants/metatile_behaviors.h").read(), re.M)
            return nomes[bruto] if bruto < len(nomes) else str(bruto)
    return None


# ------------------------------------------------------------------ leitura
def _matriz(n):
    return json.load(open(os.path.join(
        PLAT, f"res/field/matrices/map_matrix_{n:03d}.json")))


def grade_do_mapa(header):
    """(largura, altura, grade crua, (offset_x, offset_y)) do header do DS.

    Diferente do `grade_do_header` do conversor de caverna em duas coisas que so
    aparecem fora de masmorra: ele nao sabe pular `MAP_NONE` (a matriz do mundo
    tem buraco) e ele nao RECORTA o mapa dentro da matriz do mundo, o que daria
    960x960 para um mapa de 32x32.
    """
    n = int(C.headers()[header]["mapMatrixID"].split("_")[-1])
    m = _matriz(n)
    linhas = m.get("maps") or []
    if not linhas:
        return 0, 0, [], (0, 0)
    nomes = m.get("headers") or []
    if n == 0:
        celulas = [(cx, cy) for cy, r in enumerate(nomes)
                   for cx, v in enumerate(r) if v == header]
        if not celulas:
            return 0, 0, [], (0, 0)
        x0, x1 = min(c[0] for c in celulas), max(c[0] for c in celulas)
        y0, y1 = min(c[1] for c in celulas), max(c[1] for c in celulas)
    else:
        x0, y0 = 0, 0
        x1, y1 = len(linhas[0]) - 1, len(linhas) - 1
        celulas = [(cx, cy) for cy in range(y1 + 1) for cx in range(x1 + 1)]
    larg, alt = (x1 - x0 + 1) * D.LADO, (y1 - y0 + 1) * D.LADO
    grade = [0] * (larg * alt)
    for cx, cy in celulas:
        nome = linhas[cy][cx]
        if nome == "MAP_NONE":
            continue
        pedaco = D.grade_gen4(int(nome.split("_")[1]))
        for i, v in enumerate(pedaco):
            grade[((cy - y0) * D.LADO + i // D.LADO) * larg
                  + (cx - x0) * D.LADO + i % D.LADO] = v
    return larg, alt, grade, (x0 * D.LADO, y0 * D.LADO)


def e_caverna(header):
    return C.headers()[header]["mapType"] == "MAP_TYPE_CAVE"


def densidade_de_colisao(grade):
    """Fracao de tiles com o bit 15 ligado. Ver `PISO_COLISAO`."""
    return sum(1 for v in grade if v & 0x8000) / len(grade) if grade else 0.0


def _tipo_do_mapa(dest_map):
    """`map_type` do NOSSO mapa de destino de um warp, pelo id `MAP_*`."""
    g = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    for grupo in g.get("group_order", []):
        for m in g.get(grupo, []):
            arq = f"{REPO}/data/maps/{m}/map.json"
            if os.path.exists(arq):
                d = json.load(open(arq))
                if d.get("id") == dest_map:
                    return d.get("map_type")
    return None


def tile_de_warp(caverna, dest_map, pos=None, tamanho=None, pal=None):
    """Palavra que tem que ficar DEBAIXO do warp, ou None se nao for medida.

    Warp nao dispara em chao comum neste motor: quem dispara e o comportamento
    do metatile. A escolha sai do DESTINO, e nao do gosto:

    - dentro de caverna: escada se o outro lado tambem e subterraneo, boca de
      caverna se nao (a regra que `converte_cavernas_sinnoh.py` ja usava);
    - em exterior, indo para lugar FECHADO (predio, portao, caverna): porta;
    - em exterior, indo para outro EXTERIOR: seta, e a direcao sai da borda mais
      proxima, porque seta de gen 3 dispara quando o jogador anda NAQUELE
      sentido. Warp de borda existe justamente para sair do mapa por ali.
    """
    if caverna:
        return ESCADA if _tipo_do_mapa(dest_map) in SUBTERRANEOS else SAIDA
    if _tipo_do_mapa(dest_map) in FECHADOS:
        return PORTA
    if pos is None or tamanho is None:
        return None
    x, y = pos
    larg, alt = tamanho
    perto = [(y, "N"), (alt - 1 - y, "S"), (x, "O"), (larg - 1 - x, "L")]
    if pal is None:
        return SETA[min(perto)[1]]
    # A DIRECAO DA SETA SAI DE POR ONDE O JOGADOR CHEGA, e nao da borda mais
    # proxima. Custou o T85.7 em 21/08/2026: o warp 0 do IronIsland caiu em
    # (15,20), cuja borda mais proxima e a de baixo, e ganhou seta SUL; mas o
    # tile de cima, (15,19), e ROCHA, entao nao ha de onde andar para o sul e a
    # seta NUNCA dispara. Mapa com entrada e sem saida de novo, calado.
    #
    # Seta dispara quando o jogador anda NAQUELE sentido. Ele chega vindo do
    # vizinho andavel, logo a seta aponta para o lado OPOSTO ao vizinho: vizinho
    # ao norte quer dizer que ele desce, ou seja seta SUL.
    vizinhos = {"N": (x, y - 1), "S": (x, y + 1),
                "O": (x - 1, y), "L": (x + 1, y)}
    oposto = {"N": "S", "S": "N", "O": "L", "L": "O"}
    livres = {k for k, (vx, vy) in vizinhos.items()
              if 0 <= vx < larg and 0 <= vy < alt and _andavel(pal[vy * larg + vx])}
    if not livres:
        # Warp cercado de rocha nao tem seta que preste. Devolver None faz o
        # `aplica` RECUSAR o mapa, que e melhor do que gravar mao unica.
        return None
    # O filtro ja carrega a inversao: fica a seta cuja direcao de entrada
    # (`oposto`) tem vizinho andavel. Entre as que sobram vale a mais perto da
    # borda, que e a regra velha e continua certa quando ha mais de um lado.
    return SETA[min(d for d in perto if oposto[d[1]] in livres)[1]]


def traduz(header, larg, alt, grade):
    if e_caverna(header):
        return C.traduz(larg, alt, grade)
    return D.traduz_gen4(grade, larg)


# ------------------------------------------------------------------ alvos
def _layouts():
    return {l["id"]: l for l in json.load(
        open(f"{REPO}/data/layouts/layouts.json"))["layouts"] if l.get("id")}


def _header_de(meu, heads=None, deles=None):
    if heads is None:
        heads = I.headers_do_platinum()
    if deles is None:
        deles = {}
        for h in heads:
            deles.setdefault(I.chave(h), h)
    h = I.APELIDOS.get(meu) or deles.get(I.chave(meu))
    return h if h in heads else None


def alvos():
    """[(mapa, header)] dos mapas que vestem molde E tem geometria na fonte.

    A lista SAI da medida, nunca de nome escrito a mao: quem entra e quem passa
    no `planta_provisoria` (comparacao de blockdata contra o molde) e cuja grade
    do Platinum tem colisao suficiente para carregar um mapa (`PISO_COLISAO`).
    """
    layouts = _layouts()
    heads = I.headers_do_platinum()
    deles = {}
    for h in heads:
        deles.setdefault(I.chave(h), h)
    g = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    saida = []
    for grupo in g.get("group_order", []):
        for meu in g.get(grupo, []):
            arq = f"{REPO}/data/maps/{meu}/map.json"
            if not os.path.exists(arq):
                continue
            lid = json.load(open(arq)).get("layout")
            if lid not in layouts or not I.planta_provisoria(layouts, lid):
                continue
            h = _header_de(meu, heads, deles)
            if h is None:
                continue
            _larg, _alt, grade, _off = grade_do_mapa(h)
            if grade and densidade_de_colisao(grade) >= PISO_COLISAO:
                saida.append((meu, h))
    return saida


# ------------------------------------------------------------------ plano
def _andavel(palavra):
    return (palavra >> 10) & 3 == 0


def _perto(regiao, larg, x, y):
    """Tile andavel mais proximo de (x,y) dentro do corpo do mapa."""
    if y * larg + x in regiao:
        return x, y
    return min(((i % larg, i // larg) for i in regiao),
               key=lambda c: (c[0] - x) ** 2 + (c[1] - y) ** 2)


def plano(meu, header):
    """Tudo que a conversao de um mapa produz, sem escrever nada."""
    larg, alt, grade, (ox, oy) = grade_do_mapa(header)
    palavras = traduz(header, larg, alt, grade)
    regiao = C.regiao_principal(palavras, larg, alt)
    d = json.load(open(f"{REPO}/data/maps/{meu}/map.json"))

    fonte = json.load(open(os.path.join(
        PLAT, "res/field/events", I.headers_do_platinum()[header][0] + ".json")))

    def local(e):
        return e["x"] - ox, e["z"] - oy

    conta = {"chao": 0, "colisao": 0, "fora": 0}
    for tipo in ("object_events", "bg_events", "warp_events"):
        for e in fonte.get(tipo) or []:
            x, y = local(e)
            if not (0 <= x < larg and 0 <= y < alt):
                conta["fora"] += 1
            elif _andavel(palavras[y * larg + x]):
                conta["chao"] += 1
            else:
                conta["colisao"] += 1

    # Os eventos que JA estao no nosso map.json foram plantados na coordenada do
    # molde e nao valem nada na planta nova. Eles sao reancorados pela FONTE,
    # casando pelo `script`/`graphics_id` na ordem em que a fonte os lista: e o
    # mesmo pareamento por evento da fonte que a leva de 18/08 provou ser o
    # unico que nao esconde duplicata.
    # Duas passadas, e a segunda existe porque casar so por `graphics_id`
    # deixaria objeto para tras: o importador troca o sprite da fonte pelo
    # equivalente daqui (`OBJ_EVENT_GFX_CYCLIST_F` virou
    # `OBJ_EVENT_GFX_CYCLING_TRIATHLETE_F` no OreburghGateB1F), e o que sobra
    # sem par ficaria na coordenada do MOLDE, que na planta nova pode ser pedra.
    nossos = list(d.get("object_events") or [])
    livres = list(fonte.get("object_events") or [])
    casa = {}
    for i, obj in enumerate(nossos):
        e = next((e for e in livres
                  if e.get("graphics_id") == obj.get("graphics_id")), None)
        if e is not None:
            livres.remove(e)
            casa[i] = e
    # Na segunda passada so entra GENTE. O que sobra na fonte e em maioria
    # pedra, bloco de Strength e item ball, que o importador nunca trouxe
    # (`GRAFICOS_PROIBIDOS`, decisao 4 dele) e que tem gerador proprio. Sem
    # este filtro o ciclista do OreburghGateB1F casava com a primeira pedra da
    # lista e ia parar do outro lado da caverna.
    gente = [e for e in livres if not any(
        t in str(e.get("graphics_id", "")).replace("OBJ_EVENT_GFX_", "")
        for t in I.GRAFICOS_PROIBIDOS)]
    for i, obj in enumerate(nossos):
        if i not in casa and gente:
            casa[i] = gente.pop(0)
    # A lista sai por INDICE, nunca por referencia de objeto: `plano` carrega o
    # `map.json` por conta propria e quem escreve carrega outro, entao guardar o
    # dict daqui faria a escrita mexer numa copia e nao no arquivo (custou uma
    # rodada em 21/08/2026: os warps andavam e os NPCs nao).
    objetos = []
    for i, obj in enumerate(nossos):
        # Sem par na fonte o objeto ainda tem que sair da parede: ele e
        # empurrado para o corpo do mapa a partir de onde estava.
        e = casa.get(i)
        alvo = local(e) if e else (obj["x"], obj["y"])
        objetos.append((i, _perto(regiao, larg, *alvo)))

    warps = []
    fw = list(fonte.get("warp_events") or [])
    for i, w in enumerate(d.get("warp_events") or []):
        inventada = PORTAS_INVENTADAS.get(meu)
        if inventada and w["dest_map"] == inventada[0]:
            # Porta que a fonte nao tem: ela vai para a borda andavel mais
            # proxima da que o molde usava, e fica declarada como inventada.
            x, y = _perto(regiao, larg, w["x"], w["y"])
            warps.append((i, (x, y), "inventada", w["dest_map"]))
            continue
        if fw:
            e = fw.pop(0)
            x, y = _perto(regiao, larg, *local(e))
            warps.append((i, (x, y), "fonte", w["dest_map"]))
        else:
            x, y = _perto(regiao, larg, w["x"], w["y"])
            warps.append((i, (x, y), "sem par na fonte", w["dest_map"]))

    # O tile debaixo do warp e carimbado AQUI, no plano, e nao na escrita: o
    # `--dry-run` precisa dizer se algum warp ficaria sem porta, e o `--demo`
    # precisa conferir isso sem gravar nada.
    sem_porta = []
    for _i, (x, y), _motivo, dest in warps:
        palavra = tile_de_warp(e_caverna(header), dest, (x, y), (larg, alt),
                               palavras)
        if palavra is None:
            sem_porta.append(dest)
        else:
            palavras[y * larg + x] = palavra

    return {"larg": larg, "alt": alt, "palavras": palavras, "regiao": regiao,
            "sem_porta": sem_porta,
            "conta": conta, "objetos": objetos, "warps": warps,
            "caverna": e_caverna(header), "offset": (ox, oy)}


def arte(palavras):
    return len({p & 0x3FF for p in palavras})


def arte_atual(meu):
    lid = json.load(open(f"{REPO}/data/maps/{meu}/map.json"))["layout"]
    b = open(f"{REPO}/{_layouts()[lid]['blockdata_filepath']}", "rb").read()
    return len({(b[i] | (b[i + 1] << 8)) & 0x3FF for i in range(0, len(b), 2)})


# ------------------------------------------------------------------ escrita
def lid_de(header):
    return "LAYOUT_" + F.const_do_header(header)[len("MAP_"):]


def convertido(meu, header):
    """Convertido de VERDADE: a marca no map.json E o layout existindo.

    A marca sozinha mentia. Medido em 21/08/2026, com seis executores na mesma
    arvore: um `git restore` de outra frente levou embora o `layouts.json` e o
    `data/layouts/IronIsland/` e deixou os quatro `map.json` apontando para
    layout que nao existe mais. `--aplicar` respondia "ja convertido, nada a
    fazer" e o repo ficava quebrado calado. Guarda que so olha um lado dos dois
    arquivos que a conversao escreve nao e guarda.
    """
    arq = f"{REPO}/data/maps/{meu}/map.json"
    if not os.path.exists(arq):
        return False
    d = json.load(open(arq))
    if not d.get("origem_geometria"):
        return False
    return lid_de(header) in _layouts()


def aplica(meu, header):
    """Escreve layout novo e reancora os eventos. Idempotente."""
    arq = f"{REPO}/data/maps/{meu}/map.json"
    d = json.load(open(arq))
    if convertido(meu, header):
        return f"{meu}: ja convertido, nada a fazer"
    p = plano(meu, header)
    if p["sem_porta"]:
        return (f"{meu}: RECUSADO. {len(p['sem_porta'])} warp(s) ficariam sem "
                f"tile de porta ({', '.join(p['sem_porta'])}), e warp em chao "
                f"comum nao dispara neste motor: o mapa nasceria de mao unica. "
                f"So ha metatile de porta MEDIDO para tileset de caverna; para "
                f"exterior alguem tem que medir qual e a porta do "
                f"`gTileset_PetalburgSinnoh` e por em `tile_de_warp`")
    pasta = meu
    dst = f"{REPO}/data/layouts/{pasta}"
    os.makedirs(dst, exist_ok=True)
    open(f"{dst}/map.bin", "wb").write(
        struct.pack(f"<{len(p['palavras'])}H", *p["palavras"]))
    borda = C.ROCHA_TOPO if p["caverna"] else ARVORE_TOPO
    open(f"{dst}/border.bin", "wb").write(struct.pack("<4H", *([borda] * 4)))

    lid = lid_de(header)
    lay = json.load(open(f"{REPO}/data/layouts/layouts.json"))
    if not any(l.get("id") == lid for l in lay["layouts"]):
        # FIM da lista, sempre: indice de layout que anda quebra ROM ja gravada.
        # NOME unico, e nao so id unico. O `layouts.inc` gera simbolo de
        # assembler a partir do NOME (`<nome>_Blockdata`, `<nome>_Border`), e
        # nome repetido para o assembler com "symbol already defined". Bate de
        # verdade: o `IronIsland` vestia um molde que se chamava
        # `IronIsland_Layout`, entao o layout novo dele nasceu homonimo e a
        # build quebrou (medido em 21/08/2026). O molde velho NAO pode ser
        # apagado para resolver, porque indice de layout que anda quebra ROM ja
        # gravada; quem cede e o nome do novo.
        nomes = {l.get("name") for l in lay["layouts"]}
        nome = f"{pasta}_Layout"
        if nome in nomes:
            nome = f"{pasta}_Layout_Platinum"
        assert nome not in nomes, nome
        lay["layouts"].append({
            "id": lid, "name": nome,
            "width": p["larg"], "height": p["alt"],
            "primary_tileset": "gTileset_GeneralSinnoh",
            # Os dois pares mais usados de Sinnoh, contados em `layouts.json`:
            # 102 layouts de caverna usam CaveSinnoh e 52 de rua usam
            # PetalburgSinnoh. Nenhum tileset novo nasce aqui.
            "secondary_tileset": ("gTileset_CaveSinnoh" if p["caverna"]
                                  else "gTileset_PetalburgSinnoh"),
            "border_filepath": f"data/layouts/{pasta}/border.bin",
            "blockdata_filepath": f"data/layouts/{pasta}/map.bin",
            "layout_version": "emerald"})
        json.dump(lay, open(f"{REPO}/data/layouts/layouts.json", "w"),
                  indent=2, ensure_ascii=False)
        open(f"{REPO}/data/layouts/layouts.json", "a").write("\n")

    d["layout"] = lid
    if p["caverna"]:
        d["map_type"] = "MAP_TYPE_UNDERGROUND"
    for i, pos in p["objetos"]:
        d["object_events"][i]["x"], d["object_events"][i]["y"] = pos
    for i, pos, motivo, dest in p["warps"]:
        d["warp_events"][i]["x"], d["warp_events"][i]["y"] = pos
        if motivo == "inventada":
            d["warp_events"][i]["origem"] = (
                "porta inventada: a fonte nao tem volta aqui (entra-se andando "
                "pela matriz do mundo). Decisao do condutor em 21/08/2026, "
                "porque mao unica e proibida pela licao 4.1 do ESTADO")
    d["origem_geometria"] = (
        f"converte_moldes_sinnoh.py: grade 2D do Platinum ({header}), "
        f"{p['larg']}x{p['alt']}, offset {p['offset']}. Antes vestia o molde "
        f"de portao 13x9")
    json.dump(d, open(arq, "w"), indent=2, ensure_ascii=False)
    open(arq, "a").write("\n")
    return (f"{meu}: {p['larg']}x{p['alt']}, {len(p['objetos'])} objetos e "
            f"{len(p['warps'])} warps reancorados, arte {arte(p['palavras'])}")


# ------------------------------------------------------------------ saidas
def dry_run():
    print(f"{'mapa':24s} {'tipo':9s} {'planta':9s} {'KB':>6s} "
          f"{'chao':>5s} {'coli':>5s} {'fora':>5s} {'arte':>10s}  porta")
    for meu, header in alvos():
        p = plano(meu, header)
        kb = p["larg"] * p["alt"] * 2 / 1024
        print(f"{meu:24s} {'caverna' if p['caverna'] else 'exterior':9s} "
              f"{p['larg']}x{p['alt']:<6d} {kb:6.1f} "
              f"{p['conta']['chao']:5d} {p['conta']['colisao']:5d} "
              f"{p['conta']['fora']:5d} "
              f"{arte_atual(meu):4d} -> {arte(p['palavras']):3d}"
              f"  {'ok' if not p['sem_porta'] else 'FALTA MEDIR (' + str(len(p['sem_porta'])) + ')'}")
    return 0


def demo():
    """Autoteste com mutacao plantada: o que quebra tem que ser PEGO."""
    layouts = _layouts()

    # 1. Os dois moldes sao reconhecidos como molde, e mapa de verdade nao e.
    assert I.planta_provisoria(layouts, "LAYOUT_ROUTE226_ACCESS")
    assert I.planta_provisoria(layouts, "LAYOUT_ROUTE208_ACCESS")
    assert not I.planta_provisoria(layouts, "LAYOUT_MT_CORONET_5F")

    # 2. O corte de portao legitimo x vitima e o que separa a lista. Os 25 que
    #    vestem molde tem que sair em 13 vitimas e 12 portoes, e o gap medido
    #    (12,7% contra 25,3%) tem que continuar existindo, senao o piso virou
    #    chute. Mutacao plantada: com o piso no chao, portao entra junto.
    nomes = {m for m, _ in alvos()}
    assert "HearthomeCityEastGateToAmitySquare" not in nomes, nomes
    for ja in CONVERTIDOS:
        assert ja not in nomes, f"{ja} ja foi convertido: tem que SAIR de alvos()"
    # 13 vitimas medidas, 5 ja convertidas (o B1F em 21/08 e os 4 do escopo em
    # 21/08), 8 CORTADAS do escopo por decisao do Gui e que ficam como estao.
    assert len(nomes) == 8, sorted(nomes)
    global PISO_COLISAO
    guarda, PISO_COLISAO = PISO_COLISAO, 0.0
    try:
        largo = {m for m, _ in alvos()}
        assert "HearthomeCityEastGateToAmitySquare" in largo
        assert len(largo) == 20, len(largo)
    finally:
        PISO_COLISAO = guarda

    # 2.b OS METATILES DE PORTA SAO PORTA DE VERDADE, lido da tabela de
    #     atributos do tileset e nunca decorado. Warp em tile sem comportamento
    #     de porta nao dispara, e o mapa nasce de mao unica calado: foi o
    #     defeito do OreburghGateB1F em 21/08/2026. Mutacao plantada logo
    #     abaixo: chao de caverna NAO pode passar por porta.
    assert comportamento(ESCADA & 0x3FF) == "MB_LADDER"
    assert comportamento(SAIDA & 0x3FF) == "MB_SOUTH_ARROW_WARP"
    assert comportamento(PORTA & 0x3FF) == "MB_NON_ANIMATED_DOOR"
    for lado, esperado in (("N", "MB_NORTH_ARROW_WARP"), ("S", "MB_SOUTH_ARROW_WARP"),
                           ("L", "MB_EAST_ARROW_WARP"), ("O", "MB_WEST_ARROW_WARP")):
        assert comportamento(SETA[lado] & 0x3FF) == esperado, lado
    assert comportamento(C.CHAO & 0x3FF) == "MB_CAVE"        # a mutacao plantada
    assert comportamento(C.ROCHA_TOPO & 0x3FF) != "MB_NON_ANIMATED_DOOR"

    # 2.c Nenhum dos 12 fica sem porta. Enquanto a coluna `porta` do --dry-run
    #     disser "FALTA MEDIR", a conversao nao e um comando so.
    for meu, header in alvos():
        assert not plano(meu, header)["sem_porta"], meu

    # 3. A densidade e do bit 15, e so dele.
    assert densidade_de_colisao([0x0000] * 3 + [0x8000]) == 0.25
    assert densidade_de_colisao([0x00FF] * 4) == 0.0

    # 4. O `map.bin` que sai tem uma palavra por tile, nem uma a mais.
    meu, header = next((m, h) for m, h in alvos() if m == "SendoffSpring")
    p = plano(meu, header)
    assert len(p["palavras"]) == p["larg"] * p["alt"]
    assert all(0 <= w < 0x10000 for w in p["palavras"])

    # 4.b O QUE JA FOI CONVERTIDO continua de pe, e a checagem vale para TODOS
    #     eles e nao so para o primeiro. Sao 5: o OreburghGateB1F de 21/08 e os
    #     4 do escopo do Gui na mesma data. O que prova a conversao e o ARQUIVO,
    #     nao o plano: layout proprio com o tamanho da grade do Platinum, tile
    #     de porta debaixo de cada warp e todo objeto em tile andavel. Sem esta
    #     checagem o defeito da primeira rodada (warp sobre chao comum, mapa de
    #     mao unica) voltaria calado, porque mapa convertido ja nao esta em
    #     `alvos()` e nenhuma outra afirmacao do demo o alcanca.
    #
    #     Mutacao plantada: apagar a linha do layout em `layouts.json` (foi o
    #     que um `git restore` de outra frente fez de verdade em 21/08/2026)
    #     tem que ser pego aqui, e nao pela build meia hora depois.
    heads = I.headers_do_platinum()
    deles = {}
    for h in heads:
        deles.setdefault(I.chave(h), h)
    for meu in CONVERTIDOS:
        d = json.load(open(f"{REPO}/data/maps/{meu}/map.json"))
        header = _header_de(meu, heads, deles)
        assert convertido(meu, header), f"{meu}: marca ou layout sumiu"
        assert d["layout"] == lid_de(header), (meu, d["layout"])
        L = layouts_agora = _layouts()[d["layout"]]
        larg, alt, grade, _off = grade_do_mapa(header)
        assert (L["width"], L["height"]) == (larg, alt), (meu, L["width"], larg)
        bin_ = open(f"{REPO}/{L['blockdata_filepath']}", "rb").read()
        assert len(bin_) == larg * alt * 2, meu

        def palavra_em(x, y, _b=bin_, _w=L["width"]):
            i = (y * _w + x) * 2
            return _b[i] | (_b[i + 1] << 8)
        for w in d["warp_events"]:
            mb = comportamento(palavra_em(w["x"], w["y"]) & 0x3FF,
                               secundario=L["secondary_tileset"])
            assert ("DOOR" in mb or "WARP" in mb or mb == "MB_LADDER"), (meu, mb)
        for o in d.get("object_events") or []:
            assert _andavel(palavra_em(o["x"], o["y"])), (meu, o["graphics_id"])

    # 4.c NOME de layout e unico em TODA a lista, e nao so o id. O simbolo do
    #     assembler sai do nome, entao dois layouts homonimos param a build com
    #     "symbol already defined", que foi o que o IronIsland fez em
    #     21/08/2026 (o molde velho dele ja se chamava `IronIsland_Layout`).
    import collections as _c
    repetidos = [n for n, k in _c.Counter(
        l.get("name") for l in json.load(open(
            f"{REPO}/data/layouts/layouts.json"))["layouts"]).items() if k > 1]
    assert not repetidos, repetidos

    # 5. Nenhum evento reancorado nasce dentro de parede, e isso vale para TODOS
    #    os 13, nao so para o que esta sendo convertido hoje. Mutacao plantada:
    #    um objeto empurrado para tile de rocha tem que ser pego aqui.
    for meu, header in alvos():
        q = plano(meu, header)
        for _i, pos in q["objetos"]:
            assert pos and _andavel(q["palavras"][pos[1] * q["larg"] + pos[0]]), meu
        for _i, pos, _m, _d in q["warps"]:
            palavra = q["palavras"][pos[1] * q["larg"] + pos[0]]
            assert _andavel(palavra), meu
            # Warp em chao comum NAO dispara. A checagem e pelo COMPORTAMENTO
            # lido do tileset, nao por uma lista de numeros: assim ela continua
            # valendo quando alguem acrescentar um metatile de porta novo.
            # Mutacao plantada: trocar o carimbo por CHAO tem que ser pego aqui,
            # e foi o defeito de 21/08/2026.
            mb = comportamento(palavra & 0x3FF, secundario=(
                "gTileset_CaveSinnoh" if q["caverna"]
                else "gTileset_PetalburgSinnoh"))
            assert ("DOOR" in mb or "WARP" in mb or mb == "MB_LADDER"), (meu, mb)
    pedra = next(i for i, w in enumerate(p["palavras"]) if not _andavel(w))
    assert not _andavel(p["palavras"][pedra])

    # 6. Warp reancorado tem que cair no CORPO do mapa, senao o jogador pousa
    #    num bolsao de onde nao sai. E a licao que o conversor de caverna pagou.
    for _i, (x, y), _m, _d in p["warps"]:
        assert y * p["larg"] + x in p["regiao"]

    # 7. Mao unica e proibida: todo warp nosso tem volta do outro lado.
    por_id = {}
    g = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    for grupo in g.get("group_order", []):
        for m in g.get(grupo, []):
            arq = f"{REPO}/data/maps/{m}/map.json"
            if os.path.exists(arq):
                d = json.load(open(arq))
                por_id[d["id"]] = d
    for meu, _h in alvos():
        d = por_id[json.load(open(f"{REPO}/data/maps/{meu}/map.json"))["id"]]
        for w in d.get("warp_events") or []:
            alvo = por_id.get(w["dest_map"])
            assert alvo, (meu, w["dest_map"])
            assert any(v["dest_map"] == d["id"]
                       for v in alvo.get("warp_events") or []), (meu, w)

    print("demo ok")
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    if "--aplicar" in sys.argv:
        pedidos = [a for a in sys.argv[1:] if not a.startswith("-")]
        if not pedidos:
            print("--aplicar exige o nome dos mapas (nunca escreve os 13 de "
                  "uma vez: a conversao dos 12 exteriores e decisao do Gui)")
            return 2
        todos = dict(alvos())
        for meu in pedidos:
            # Idempotencia: mapa ja convertido SAI da lista de alvos (ele deixou
            # de vestir o molde), entao o header tem que sair do casamento por
            # nome, e nao de `alvos()`. Isso tambem e o que deixa `--aplicar`
            # REFAZER a metade que outra frente apagou: `convertido` olha o
            # `map.json` E o `layouts.json`, e nao so a marca.
            header = todos.get(meu) or _header_de(meu)
            if header is None:
                print(f"{meu}: nao esta na lista medida de molde")
                return 2
            if convertido(meu, header):
                print(f"{meu}: ja convertido, nada a fazer")
                continue
            print(aplica(meu, header))
        return 0
    return dry_run()


if __name__ == "__main__":
    sys.exit(main())
