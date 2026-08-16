#!/usr/bin/env python3
"""Obra 2 de Unova, bloco B1: traduz `changeblock` do BW3G em `setmetatile` daqui.

Uso:
    python3 dev_scripts/changeblock_gen2.py --demo              # autoteste, nao grava
    python3 dev_scripts/changeblock_gen2.py --fila              # tabela dos 12 da fila
    python3 dev_scripts/changeblock_gen2.py --fila --todos      # tabela dos 39 possiveis
    python3 dev_scripts/changeblock_gen2.py VillageBridge       # .inc na saida padrao
    python3 dev_scripts/changeblock_gen2.py Dreamyard --trecho pedaco.asm
    python3 dev_scripts/changeblock_gen2.py Dreamyard --trecho -    # trecho pelo stdin

O QUE ESTE SCRIPT FAZ, E O QUE ELE NAO FAZ

Faz: ler as linhas `changeblock x, y, $bloco` de um mapa do BW3G e imprimir as
linhas `.inc` equivalentes, prontas para colar num `data/maps/Unova_*/scripts.inc`.
Nao faz: escrever em mapa nenhum, criar flag ou var, decidir QUANDO a cena roda
(isso e o gatilho, e e trabalho do executor), nem mexer em `map.bin`.

--------------------------------------------------------------------------------
1. POR QUE UMA CHAMADA VIRA QUATRO, E POR QUE A COORDENADA NAO TEM CONTA NENHUMA

Um bloco do gen 2 tem 32x32 px = 2x2 metatiles do GBA. Logo `changeblock` mexe em
QUATRO celulas nossas: (x,y), (x+1,y), (x,y+1) e (x+1,y+1), na ordem CE, CD, BE,
BD, que e a mesma ordem do `tilecoll` da fonte (a mesma que
`blockdata_unova.converte_arte` ja usa para gravar o `map.bin`).

A coordenada e IDENTIDADE, sem multiplicar nem dividir, e isso foi lido no codigo
da fonte, nao lembrado:

  - `engine/overworld/scripting.asm:2586` (`Script_changeblock`) le x e y crus,
    soma 4 em cada (a borda do mapa do gen 2) e chama `GetBlockLocation`;
  - `home/map.asm:1803` (`GetBlockLocation`) faz `srl` em x e em y, ou seja
    DIVIDE POR DOIS antes de indexar o bloco.

Quer dizer: o parametro do `changeblock` ja vem na unidade de 16x16 px do gen 2,
que e exatamente a unidade de metatile do gen 3. Coerente com a medicao: todo x e
todo y de `changeblock` do BW3G sao PARES (o `--demo` cobra isso), porque so
coordenada par cai no canto de um bloco. Coordenada impar seria defeito da fonte,
e aqui vira erro, nao arredondamento calado.

2. DE ONDE SAI O METATILE: A MESMA TABELA DA CONVERSAO ESTATICA, SEM COPIA

`tileset_gen2.converte(tileset)` devolve `quad2mt[(bloco, quadrante)] -> metatile`
(e `masmorra2mt` para os mapas de ambiente CAVE/DUNGEON, onde o chao vira
`chao_caverna` e por isso sorteia encontro). O id que vai no script e `512 + mt`,
o mesmo `+512` do tileset secundario que o `map.bin` grava. Colisao e elevacao
saem de `tileset_gen2.colisao_da_classe` (andavel 0/3, agua 0/1, bloqueado 1/0).

Nada disso e tabela nova: se o `map.bin` do mapa esta certo, este script esta
certo, e o teste (a) do `--demo` reconstroi o `map.bin` inteiro por esse caminho e
compara byte a byte com o disco.

Precedente humano: `data/maps/Unova_StriatonGym/scripts.inc`, onde o
`changeblock 6, 2, $6a` (a escada do CILAN) foi traduzido a mao em 12/08/2026. O
teste (b) do `--demo` refaz aquela traducao e cobra o mesmo resultado.

3. OS NUMEROS DO DESENHO (medidos em 15/08/2026, refeitos por `--fila`)

A FILA E DERIVADA, NAO DIGITADA: `dev_scripts/fila_b6.json`, linhas com
`regiao == "unova"` e `tipo == "changeblock"`, sao 108 cenas em 12 mapas. E a
mesma fila canonica do B6, entao ela nao pode divergir daqui por copia velha
(ha uma copia literal em `FILA_LITERAL`, so como paraquedas se o JSON mudar de
forma; quando ele cai, o script AVISA no stderr em vez de fingir).

Fila de 12 mapas: 306 triplas (x, y, bloco) distintas, 1224 quadrantes, e
    696 de 1224 iguais ao `map.bin`   -> `@ igual ao map.bin`
     91 mudam elevacao de/para agua   -> `setmetatileinrange` com elevacao
      4 mudam comportamento de warp   -> `@ ATENCAO: muda warp`
Os 91 de agua sao de VirbankCity (51), VillageBridge (32) e VictoryRoadCave1F (8);
os 4 de warp sao VictoryRoadCave1F (2), DragonspiralTower2F (1) e Dreamyard (1).
Os cinco numeros sao cobrados no `--demo`: se um deles nao fechar, o defeito e da
tabela, da fila ou do desenho, e o assert TEM que quebrar em vez de ser ajustado.
Universo total (todo mapa do BW3G com `changeblock` e com arte propria ja na
build, superconjunto da fila): 39 mapas, 590 triplas, 2360 quadrantes, ZERO
buracos. Os testes (a) e (c) rodam nos 39, que e mais forte que rodar nos 12.

4. AS ARMADILHAS, TODAS MEDIDAS NO CODIGO DESTE REPO

a) `setmetatile` NAO MEXE NA ELEVACAO. `MapGridSetMetatileIdAt`
   (src/fieldmap.c:474) preserva os bits 12-15 de proposito. Fora da agua isso e
   inofensivo (elevacao 0 casa com tudo, `IsElevationMismatchAt` devolve FALSE);
   NA AGUA e o defeito inteiro: a celula ficaria com o desenho de agua e a
   elevacao 3 do chao que estava ali, e o jogador atravessaria a pe. Por isso a
   decisao da condutora (15/08/2026): quadrante que muda elevacao de/para agua
   sai como `setmetatileinrange x, y, x, y, mt, colisao, ELEVACAO EXPLICITA`.

b) `setmetatileinrange` sem o ultimo parametro grava elevacao ZERO, nao "mantem".
   A macro tem `elevation=0xFF` como padrao e `NativeFunc_SetMetatileInRange`
   (src/scrcmd.c:2760-2794) so faz o OR da elevacao quando ela e < 15; como quem
   escreve a celula e `MapGridSetMetatileEntryAt`, que grava a PALAVRA INTEIRA, o
   0xFF nao vira "sem mudanca", vira elevacao 0. Este gerador sempre escreve a
   elevacao quando usa essa macro.

c) `hasCollision = TRUE` grava colisao 3, nao 1 (`MAPGRID_COLLISION_MASK`, e
   `MAPGRID_IMPASSABLE` do `setmetatile` e o MESMO valor, include/global.fieldmap.h:11
   e :36). Bloqueia igual (o motor testa != 0), entao nao ha risco de caminho; o
   unico lugar do repo que compara `== 1` e `src/fldeff_cut.c`, e la o `BUGFIX`
   ja troca por `!= 0`. Consequencia pratica: uma linha marcada `@ igual ao
   map.bin` com colisao TRUE grava 3 onde o estatico tem 1. Mesmo efeito de
   bloqueio, valor diferente; a marca fala do ESTADO ALVO, nao do byte.

d) AS CHAMADAS QUE NAO MUDAM NADA NAO PODEM SUMIR. 696 dos 1224 quadrantes ja
   estao no `map.bin` com o mesmo metatile: sao as chamadas de RESTAURAR estado
   (a cena abre a porta e depois fecha). Quem apagar por "nao faz nada" quebra a
   volta ao estado inicial. Elas saem marcadas, nunca omitidas.

e) WARP MUDO. A conversao estatica poe `MB_NON_ANIMATED_DOOR` embaixo de warp que
   a fonte deixou sobre chao (`blockdata_unova.forca_warps`, 170 portas). Um
   `changeblock` por cima devolve o metatile cru e MATA o warp. Os quadrantes em
   que o comportamento entra ou sai da lista de warp
   (`valida_warp_tile.COMPORTA_WARP`) saem com `@ ATENCAO: muda warp` para o
   executor conferir contra os `warp_events` do `map.json`.

f) Comportamento de metatile se le pelo NOME (regra da casa,
   `valida_warp_tile.NOME`): neste repo `0x60` e `MB_NON_ANIMATED_DOOR` e `0x61`
   e `MB_LADDER`, que NAO e a numeracao do pokeemerald de origem.

5. O QUE ESTE SCRIPT SE RECUSA A FAZER

Mapa cujo tileset ainda nao tem arte propria na build, ou cujo layout ainda aponta
para o tileset EMPRESTADO, sai como erro em vez de saida. Traduzir bloco para
metatile de um tileset que o mapa nao carrega escreveria lixo bonito.
"""
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import blockdata_unova as bd      # noqa: E402  quadrantes/mapas_unova/comportamentos
import importa_unova as iu        # noqa: E402  BW3G
import tileset_gen2 as tg         # noqa: E402  quad2mt/masmorra2mt/colisao_da_classe
import valida_warp_tile as vw     # noqa: E402  NOME e COMPORTA_WARP

BW3G = iu.BW3G
QUAD = ("CE", "CD", "BE", "BD")               # a ordem do `tilecoll` do gen 2
DESLOC = ((0, 0), (1, 0), (0, 1), (1, 1))
ELEV_AGUA = bd.AGUA[1]                        # ELEVATION_SURF, hoje 1

RE_CHANGEBLOCK = re.compile(
    r"^\s*changeblock\s+(\d+)\s*,\s*(\d+)\s*,\s*\$([0-9a-fA-F]+)", re.M)

# Calibragem da condutora, 15/08/2026. Nao e enfeite: e o que pega o dia em que a
# tabela de tileset mudar e a agua ou o warp mudarem de lugar calados.
AGUA_ESPERADA = {"VirbankCity": 51, "VillageBridge": 32, "VictoryRoadCave1F": 8}
WARP_ESPERADO = {"VictoryRoadCave1F": 2, "DragonspiralTower2F": 1, "Dreamyard": 1}
DESENHO = {"triplas": 306, "quadrantes": 1224, "igual": 696, "agua": 91, "warp": 4}

# Paraquedas: a fila de verdade e derivada de `fila_b6.json` (ver `fila()`), e esta
# copia so entra se aquele arquivo for regenerado com outra estrutura. Copiada em
# 15/08/2026 das 108 cenas `regiao=unova tipo=changeblock`.
FILA_LITERAL = (
    "DragonspiralTower2F", "Dreamyard", "IcirrusCitySouth", "Rt11", "Rt18",
    "SeasideCave1F", "VictoryRoadCave1F", "VillageBridge", "VirbankCity",
    "VirbankComplexB1F", "VirbankComplexB2F", "VirbankComplexOutside",
)
FILA_B6 = f"{RAIZ}/dev_scripts/fila_b6.json"


# ------------------------------------------------------------------- inventario

def mapas(_cache={}):
    """CamelCase do BW3G -> (nome daqui, layout, tileset da fonte, ambiente)."""
    if not _cache:
        itens, _ = bd.mapas_unova()
        for nome, l, tset, camel, _arq, _w, _h, amb in itens:
            _cache[camel] = (nome, l, tset, amb)
    return _cache


def fila(_cache=[]):
    """Os 12 mapas da Obra 2, lidos da fila canonica do B6 e nao digitados aqui.

    Fonte: `dev_scripts/fila_b6.json`, as 108 cenas com `regiao == "unova"` e
    `tipo == "changeblock"`. Se o JSON for regenerado com outra estrutura (ou
    sumir), cai em `FILA_LITERAL` e AVISA no stderr: fila errada em silencio
    faria o `--demo` cobrar os numeros do desenho da lista errada.
    """
    if _cache:
        return _cache[0]
    camel, motivo = [], ""
    try:
        cenas = json.load(open(FILA_B6))
        destinos = {c["mapa_destino"] for c in cenas
                    if c.get("regiao") == "unova" and c.get("tipo") == "changeblock"}
        camel = sorted(c for c, info in mapas().items() if info[0] in destinos)
        if len(camel) != len(FILA_LITERAL):
            motivo = f"{len(camel)} mapas, esperava {len(FILA_LITERAL)}"
    except (OSError, ValueError, KeyError, TypeError) as e:
        motivo = f"{type(e).__name__}: {e}"
    if motivo:
        print(f"aviso: {FILA_B6} nao deu a fila ({motivo}); usando FILA_LITERAL",
              file=sys.stderr)
        camel = sorted(FILA_LITERAL)
    _cache.append(camel)
    return camel


def com_changeblock():
    """[CamelCase] de todo mapa do BW3G que tem `changeblock` e ja tem arte."""
    ja = bd.arte_disponivel()
    saida = []
    for arq in sorted(os.listdir(f"{BW3G}/maps")):
        if not arq.endswith(".asm"):
            continue
        camel = arq[:-4]
        info = mapas().get(camel)
        if info is None or info[2] not in ja:
            continue
        if RE_CHANGEBLOCK.search(open(f"{BW3G}/maps/{arq}").read()):
            saida.append(camel)
    return saida


def contexto(camel):
    """Tudo que a traducao de UM mapa precisa, ja conferido."""
    info = mapas().get(camel)
    if info is None:
        raise SystemExit(f"{camel}: nao e mapa de Unova convertido "
                         f"(nome CamelCase do BW3G, ex.: VillageBridge)")
    nome, l, tset, amb = info
    ja = bd.arte_disponivel()
    if tset not in ja:
        raise SystemExit(f"{camel}: o tileset `{tset}` ainda nao tem arte propria na "
                         f"build. Sem ela nao existe metatile de destino honesto.")
    if l["secondary_tileset"] != ja[tset]:
        raise SystemExit(f"{camel}: o layout ainda aponta para {l['secondary_tileset']}, "
                         f"e a arte e {ja[tset]}. Rode blockdata_unova.py --gravar antes.")
    ts = bd._tileset_convertido(tset)
    return {
        "camel": camel, "nome": nome, "layout": l, "tileset": tset, "ambiente": amb,
        "ts": ts,
        "q2m": ts["masmorra2mt"] if amb in tg.MASMORRA else ts["quad2mt"],
        "coll": bd.quadrantes(tset + "_collision.asm"),
        "mapbin": open(f"{RAIZ}/{l['blockdata_filepath']}", "rb").read(),
        "beh": bd.comportamentos(l),
    }


# --------------------------------------------------------------------- leitura

def chamadas(camel, texto=None):
    """[(origem, x, y, bloco, linha crua)] na ordem do arquivo.

    `texto` sobrepoe a fonte: e assim que se traduz um TRECHO colado, sem precisar
    de arquivo intermediario.
    """
    if texto is None:
        arq = f"maps/{camel}.asm"
        texto = open(f"{BW3G}/{arq}").read()
    else:
        arq = "(trecho)"
    saida = []
    for i, ln in enumerate(texto.splitlines(), 1):
        m = RE_CHANGEBLOCK.match(ln)
        if m:
            saida.append((f"{arq}:{i}", int(m.group(1)), int(m.group(2)),
                          int(m.group(3), 16), ln.strip()))
    return saida


# -------------------------------------------------------------------- traducao

def traduz(camel, texto=None, ctx=None):
    """[(origem, x, y, bloco, linha, [quadrante x4])].

    Cada quadrante e um dict com o que a saida precisa E com o que o executor
    precisa conferir: metatile, colisao, elevacao, se e igual ao `map.bin`, se
    muda elevacao de/para agua e se muda comportamento de warp.
    """
    ctx = ctx or contexto(camel)
    l = ctx["layout"]
    w, h = l["width"], l["height"]
    saida = []
    for origem, x, y, bloco, linha in chamadas(camel, texto):
        if x % 2 or y % 2:
            raise SystemExit(f"{origem}: changeblock em ({x},{y}), coordenada impar. "
                             f"O gen 2 divide por 2 para achar o bloco, entao isso e "
                             f"defeito da fonte e nao arredondamento nosso.")
        classes = ctx["coll"].get(bloco)
        if classes is None:
            raise SystemExit(f"{origem}: bloco ${bloco:02x} nao existe no "
                             f"{ctx['tileset']}_collision.asm")
        quads = []
        for i, (dx, dy) in enumerate(DESLOC):
            X, Y = x + dx, y + dy
            if not (0 <= X < w and 0 <= Y < h):
                raise SystemExit(f"{origem}: quadrante {QUAD[i]} cai em ({X},{Y}), "
                                 f"fora do layout {w}x{h}")
            mt = ctx["q2m"].get((bloco, i))
            if mt is None:
                raise SystemExit(f"{origem}: bloco ${bloco:02x} quadrante {QUAD[i]} "
                                 f"sem metatile em {ctx['tileset']}")
            classe = classes[i]
            if ctx["ambiente"] in tg.MASMORRA and classe == "chao":
                classe = "chao_caverna"     # a mesma regra do `converte_arte`
            col, elev = tg.colisao_da_classe(classe)
            novo = 512 + mt
            v = struct.unpack_from("<H", ctx["mapbin"], (Y * w + X) * 2)[0]
            velho, velho_col, velho_elev = v & 0x3FF, (v >> 10) & 3, (v >> 12) & 0xF
            mb_velho, mb_novo = ctx["beh"](velho), ctx["beh"](novo)
            quads.append({
                "q": QUAD[i], "x": X, "y": Y, "metatile": novo, "classe": classe,
                "colisao": col, "elevacao": elev,
                "igual": (velho, velho_col, velho_elev) == (novo, col, elev),
                "agua": (velho_elev == ELEV_AGUA) != (elev == ELEV_AGUA),
                "warp": (mb_velho in vw.COMPORTA_WARP) != (mb_novo in vw.COMPORTA_WARP),
                "mb_velho": vw.NOME.get(mb_velho, mb_velho),
                "mb_novo": vw.NOME.get(mb_novo, mb_novo),
            })
        saida.append((origem, x, y, bloco, linha, quads))
    return saida


# ----------------------------------------------------------------------- saida

def _bool(v):
    return "TRUE" if v else "FALSE"


def linhas_inc(camel, texto=None, ctx=None):
    """As linhas `.inc` de um mapa, prontas para colar. Uma lista de strings."""
    ctx = ctx or contexto(camel)
    itens = traduz(camel, texto, ctx)
    saida = [
        f"@ {ctx['nome']}: changeblock do BW3G traduzido por "
        f"dev_scripts/changeblock_gen2.py.",
        f"@ Tileset {ctx['tileset']} -> {ctx['layout']['secondary_tileset']}, "
        f"ambiente {ctx['ambiente']}. Um bloco do gen 2 = 2x2 metatiles (CE, CD, BE, BD).",
        "@ Linha marcada `igual ao map.bin` NAO pode ser apagada: e restauracao de estado.",
    ]
    for origem, x, y, bloco, linha, quads in itens:
        saida.append("")
        saida.append(f"\t@ {origem}  {linha}")
        for qd in quads:
            if qd["warp"]:
                saida.append(f"\t@ ATENCAO: muda warp em ({qd['x']},{qd['y']}): "
                             f"{qd['mb_velho']} -> {qd['mb_novo']}, conferir warp_events")
        if any(qd["agua"] for qd in quads):
            # decisao da condutora (15/08/2026): agua nao passa por `setmetatile`,
            # que preserva a elevacao antiga. Aqui a chamada se abre em quatro.
            for qd in quads:
                marca = []
                if qd["igual"]:
                    marca.append("igual ao map.bin")
                if qd["agua"]:
                    marca.append(f"água: elevação explícita {qd['elevacao']}")
                rabo = ("   @ " + ", ".join(marca)) if marca else ""
                if qd["agua"]:
                    saida.append(f"\tsetmetatileinrange {qd['x']}, {qd['y']}, "
                                 f"{qd['x']}, {qd['y']}, {qd['metatile']}, "
                                 f"{_bool(qd['colisao'])}, {qd['elevacao']}{rabo}")
                else:
                    saida.append(f"\tsetmetatile {qd['x']}, {qd['y']}, "
                                 f"{qd['metatile']}, {_bool(qd['colisao'])}{rabo}")
            continue
        iguais = [qd["q"] for qd in quads if qd["igual"]]
        rabo = ("   @ igual ao map.bin: "
                + ("os 4" if len(iguais) == 4 else ", ".join(iguais))) if iguais else ""
        saida.append("\tchangeblock_gen2 %d, %d, %s, %s%s" % (
            x, y, ", ".join(str(qd["metatile"]) for qd in quads),
            ", ".join(_bool(qd["colisao"]) for qd in quads), rabo))
    return saida


# ---------------------------------------------------------------------- medida

def medida(camel, ctx=None):
    """{triplas, quadrantes, igual, agua, warp, chamadas} de um mapa."""
    ctx = ctx or contexto(camel)
    itens = traduz(camel, None, ctx)
    vistos, m = set(), {"chamadas": len(itens), "triplas": 0, "quadrantes": 0,
                        "igual": 0, "agua": 0, "warp": 0}
    for _origem, x, y, bloco, _linha, quads in itens:
        if (x, y, bloco) in vistos:
            continue
        vistos.add((x, y, bloco))
        m["triplas"] += 1
        for qd in quads:
            m["quadrantes"] += 1
            for k in ("igual", "agua", "warp"):
                m[k] += 1 if qd[k] else 0
    return m


def tabela(todos=False):
    linhas, tot = [], {}
    for camel in (com_changeblock() if todos else fila()):
        m = medida(camel)
        linhas.append((camel, m))
        for k, v in m.items():
            tot[k] = tot.get(k, 0) + v
    linhas.sort(key=lambda r: -r[1]["triplas"])
    print(f"{'mapa':26} {'chama':>6} {'tripla':>7} {'quadr':>6} {'igual':>6} "
          f"{'agua':>5} {'warp':>5}")
    for camel, m in linhas:
        print(f"{camel:26} {m['chamadas']:6} {m['triplas']:7} {m['quadrantes']:6} "
              f"{m['igual']:6} {m['agua']:5} {m['warp']:5}")
    print(f"{'TOTAL (' + str(len(linhas)) + ' mapas)':26} {tot['chamadas']:6} "
          f"{tot['triplas']:7} {tot['quadrantes']:6} {tot['igual']:6} "
          f"{tot['agua']:5} {tot['warp']:5}")
    return linhas, tot


# --------------------------------------------------------------------- demo

def demo():
    universo = com_changeblock()
    doze = fila()
    assert len(universo) >= len(doze), f"so {len(universo)} mapas com changeblock e arte"
    assert set(doze) <= set(universo), \
        f"fila com mapa sem arte ou sem changeblock: {sorted(set(doze) - set(universo))}"

    # (a) a tabela nao e nova: se ela vale, o `map.bin` do disco nasce dela.
    #     Byte a byte, e nao "parecido": um metatile trocado aqui e um mapa que
    #     muda de cara quando a cena roda.
    for camel in universo:
        ctx = contexto(camel)
        nome = ctx["nome"]
        gerado = bd.gera(so=nome)[0][nome]
        assert gerado == ctx["mapbin"], \
            f"(a) {nome}: blockdata reconstruido != data/layouts/{nome}/map.bin"

    # (a2) boa noticia e suspeita: (a) so prova que ESTE script le o mesmo
    #      `quad2mt` que o `blockdata_unova`. O comportamento que o gerador cita
    #      nos comentarios vem do `metatile_attributes.bin` DO DISCO, que podia
    #      estar velho. Aqui os dois se cruzam.
    #
    #      EXCECAO, 15/08/2026 (B4): o disco pode divergir da tabela DE PROPOSITO,
    #      quando uma ferramenta troca o comportamento de um metatile depois da
    #      conversao. Hoje sao `porta_de_saida_unova.py` (porta -> seta sul) e
    #      `pedra_buraco_unova.py` (porta -> buraco de Mt. Pyre, os 4 buracos de
    #      pedra). A lista de excecao NAO e digitada aqui: ela vem do ALVOS das
    #      proprias ferramentas, entao desfazer a ferramenta faz o assert voltar
    #      sozinho, e metatile que ninguem declarou continua cobrado.
    import pedra_buraco_unova as pb          # noqa: E402  (so o --demo precisa)
    import porta_de_saida_unova as ps        # noqa: E402
    ctx = contexto("Dreamyard")
    tset = ctx["layout"]["secondary_tileset"]
    trocados = {mt for (ts, mt) in list(pb.ALVOS) + [tuple(a) for a in ps.ALVOS]
                if ts == tset}
    atr = ctx["ts"]["atributos"]
    for mt in range(ctx["ts"]["n_metatiles"]):
        if 512 + mt in trocados:
            continue
        do_disco = ctx["beh"](512 + mt)
        da_tabela = struct.unpack_from("<H", atr, mt * 2)[0]
        assert do_disco == da_tabela, \
            f"(a2) metatile {mt} do dreamyard: disco diz {do_disco}, tabela diz {da_tabela}"

    # (b) o precedente escrito a mao em 12/08/2026 (a escada do CILAN).
    itens = traduz("StriatonGym")
    assert itens, "(b) StriatonGym sem changeblock na fonte"
    alvo = [i for i in itens if (i[1], i[2], i[3]) == (6, 2, 0x6a)]
    assert alvo, "(b) o `changeblock 6, 2, $6a` sumiu da fonte"
    quads = {qd["q"]: qd for qd in alvo[0][5]}
    escrito = open(f"{RAIZ}/data/maps/Unova_StriatonGym/scripts.inc").read()
    mao = {(int(x), int(y)): (int(mt), col) for x, y, mt, col in
           re.findall(r"^\s*setmetatile (\d+), (\d+), (\d+), (\w+)", escrito, re.M)}
    for q, (x, y) in (("BE", (6, 3)), ("BD", (7, 3))):
        assert (x, y) in mao, f"(b) o precedente nao tem setmetatile em ({x},{y})"
        mt, col = mao[(x, y)]
        assert quads[q]["metatile"] == mt, \
            f"(b) {q}: gerador diz {quads[q]['metatile']}, a mao diz {mt}"
        assert _bool(quads[q]["colisao"]) == col, \
            f"(b) {q}: gerador diz {_bool(quads[q]['colisao'])}, a mao diz {col}"
        assert not quads[q]["igual"], f"(b) {q} deveria MUDAR o map.bin"
    for q in ("CE", "CD"):
        assert quads[q]["igual"], \
            f"(b) {q} deveria ser igual ao map.bin (por isso o humano nao escreveu a linha)"

    # (c) zero buraco: toda tripla de todo mapa da fila resolve. `traduz` levanta
    #     SystemExit em bloco sem metatile, entao rodar sem excecao E o teste.
    tot = {"triplas": 0, "quadrantes": 0, "igual": 0, "agua": 0, "warp": 0}
    porto = {}
    for camel in universo:
        m = medida(camel)
        porto[camel] = m
        for k in tot:
            tot[k] += m[k]
    assert tot["quadrantes"] == 4 * tot["triplas"], "(c) quadrante por tripla != 4"

    # (d) a calibragem do desenho, mapa a mapa. Se a tabela de tileset mudar e a
    #     agua ou o warp andarem de lugar, e aqui que aparece.
    for camel, n in AGUA_ESPERADA.items():
        assert porto[camel]["agua"] == n, \
            f"(d) {camel}: {porto[camel]['agua']} quadrantes de agua, o desenho mediu {n}"
    for camel, n in WARP_ESPERADO.items():
        assert porto[camel]["warp"] == n, \
            f"(d) {camel}: {porto[camel]['warp']} quadrantes de warp, o desenho mediu {n}"
    assert sum(AGUA_ESPERADA.values()) == DESENHO["agua"] and \
        sum(WARP_ESPERADO.values()) == DESENHO["warp"], \
        "(d) a calibragem do desenho foi mexida sem medir de novo"

    # (d2) os cinco numeros do desenho, cobrados na FILA de 12 (nao no universo).
    #      Se um nao fechar, o errado e o desenho ou a fila, e este assert e o
    #      unico lugar onde isso aparece. NAO afrouxar: reportar a diferenca.
    doze_soma = {k: sum(porto[c][k] for c in doze) for k in DESENHO}
    assert doze_soma == DESENHO, (
        "(d2) a fila de 12 nao bate com o desenho:\n"
        + "\n".join(f"    {k}: medido {doze_soma[k]}, desenho {v}"
                    for k, v in DESENHO.items() if doze_soma[k] != v)
        + "\n  fila lida: " + ", ".join(doze))

    # (e) a macro e o gerador sao uma coisa so: sem os quatro `setmetatile` na
    #     ordem CE, CD, BE, BD a saida deste script compila e mente.
    ev = open(f"{RAIZ}/asm/macros/event.inc").read()
    corpo = re.search(r"\.macro changeblock_gen2\b(.*?)\.endm", ev, re.S)
    assert corpo, "(e) a macro changeblock_gen2 nao esta em asm/macros/event.inc"
    postos = re.findall(r"setmetatile\s+([^,]+),\s*([^,]+),\s*\\(\w+),\s*\\(\w+)",
                        corpo.group(1))
    assert len(postos) == 4, f"(e) a macro expande em {len(postos)} setmetatile, esperava 4"
    for i, (px, py, mt, col) in enumerate(postos):
        assert (mt, col) == (f"mt{i}", f"col{i}"), f"(e) posicao {i} usa \\{mt} e \\{col}"
        assert ("+1" in px) == bool(DESLOC[i][0]), f"(e) x do quadrante {QUAD[i]} errado"
        assert ("+1" in py) == bool(DESLOC[i][1]), f"(e) y do quadrante {QUAD[i]} errado"

    print(f"OK: fila de {len(doze)} mapas (fila_b6.json, regiao=unova tipo=changeblock): "
          f"{doze_soma['triplas']} triplas distintas, {doze_soma['quadrantes']} quadrantes, "
          f"{doze_soma['igual']} iguais ao map.bin, {doze_soma['agua']} de agua, "
          f"{doze_soma['warp']} mudam warp. Bate com o desenho nos cinco numeros.")
    print(f"OK: universo de {len(universo)} mapas com changeblock e arte "
          f"(superconjunto da fila): {tot['triplas']} triplas, {tot['quadrantes']} "
          f"quadrantes, {tot['igual']} iguais, {tot['agua']} de agua, {tot['warp']} de warp.")
    print("OK (a) blockdata reconstruido byte a byte nos 39.")
    print("OK (b) StriatonGym 6,2,$6a bate com o que esta escrito a mao.")
    print("OK (c) zero buraco: toda tripla resolve na tabela.")
    print("OK (d) agua e warp na calibragem do desenho, mapa a mapa.")
    print("OK (d2) os 5 numeros do desenho fecham na fila de 12.")
    print("OK (e) a macro changeblock_gen2 expande nos 4 setmetatile certos.")


def main():
    arg = sys.argv[1:]
    if "--demo" in arg:
        return demo()
    if "--fila" in arg:
        tabela("--todos" in arg)
        return
    if not arg or arg[0].startswith("-"):
        raise SystemExit(__doc__.split("\n\n")[1])
    camel = arg[0]
    texto = None
    if "--trecho" in arg:
        p = arg[arg.index("--trecho") + 1]
        texto = sys.stdin.read() if p == "-" else open(p).read()
    print("\n".join(linhas_inc(camel, texto)))


if __name__ == "__main__":
    main()
