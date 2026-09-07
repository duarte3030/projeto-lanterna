#!/usr/bin/env python3
"""Tira da ROM o CONTEUDO dos mapas cortados pelo Gui, sem mexer em indice.

    python3 dev_scripts/remove_mapas_cortados.py             # tabela, nao escreve
    python3 dev_scripts/remove_mapas_cortados.py --dry-run   # idem, explicito
    python3 dev_scripts/remove_mapas_cortados.py --demo      # autoteste com mutacao plantada
    python3 dev_scripts/remove_mapas_cortados.py --aplicar   # escreve

O que este script faz, e por que NAO apaga a pasta
--------------------------------------------------
Os 110 mapas de `completude.CORTES_DO_GUI` (modo `deficit`) saem do escopo mas
NAO podem sair das TABELAS, porque duas coisas que a save guarda sao INDICES:

1. `SaveBlock1.location.mapGroup` / `mapNum` (0x04). O numero do mapa e a
   POSICAO dele dentro do grupo em `data/maps/map_groups.json`. Medido em
   22/08/2026: os 110 cortados estao ESPALHADOS NO MEIO de nove grupos
   (`gMapGroup_IndoorSinnohPortas` perde 38 de 128, do indice 1 ao 123), entao
   apagar a entrada desloca o id de TODO mapa vivo que vem depois e a save do
   Gui volta em outro lugar. Nenhum grupo perde so o fim.
2. `SaveBlock1.mapLayoutId` (0x32). O id de LAYOUT e o ordinal dentro de
   `data/layouts/layouts.json` (ver `include/constants/layouts.h`, gerado).
   Apagar layout desloca o de todo mundo depois dele. `guarda_save.py` NAO
   cobre este segundo caso: e um ponto cego dele, registrado aqui.

Por isso o mapa cortado vira TUMULO: a entrada continua na tabela e no lugar, o
id nao anda, e o que sai e o PESO. Medido no `pokeemerald.map` da build
`852be4632a`: 196.659 B (192,0 KB) de blockdata, borda, eventos, script, texto
e tabela de mato presos nesses 110 mapas.

O que o tumulo perde
--------------------
- `map.json` vira cabecalho sem evento nenhum (0 objetos, 0 warps, 0 placas,
  0 coord_events, sem conexao), com `region_map_section` em `MAPSEC_NONE` para
  que `valida_conectividade.py` nao passe a acusar 108 orfaos de Sinnoh que sao
  cortes, e nao defeito.
- `scripts.inc` fica so com o rotulo `<Mapa>_MapScripts:: .byte 0`, que o
  `header.inc` gerado exige. Texto mora dentro do proprio scripts.inc de cada
  mapa (conferido: nenhum `_Text_` de cortado vive em outro arquivo), entao
  some junto.
- o LAYOUT exclusivo do mapa encolhe para 1x1 (2 B de blockdata, 8 B de borda).
  Encolher em vez de apagar e o que salva o `mapLayoutId`. Layout
  COMPARTILHADO com mapa vivo nao e tocado: sao 6 (os moldes de Oreburgh e o
  `LAYOUT_ROUTE208_ACCESS`).
- a tabela de mato dele sai de `src/data/wild_encounters.json`, POR CHAVE
  (`map`), nunca reescrevendo o arquivo: a Dex esta editando outras entradas do
  mesmo arquivo nesta mesma rodada.

A porta que ficava viva do outro lado
-------------------------------------
29 warps de 23 mapas VIVOS levavam a mapa cortado (mais um `warpsilent` dentro
do script do marinheiro de Snowpoint). O tile fica, o warp some, e uma placa
nova diz que esta fechado.

"O warp some" NAO e apagar a entrada da lista: `dest_warp_id` e indice, e 15
mapas vivos tem warp de terceiro apontando para indice DEPOIS do que sairia
(HearthomeCity perderia os indices 7 e 8 de 16 e desalinharia 14 ponteiros).
Entao o warp vira LAPIDE: a entrada continua no mesmo indice e passa a repetir
as coordenadas do warp DOADOR (o warp vivo de menor indice do mesmo mapa). Duas
entradas no mesmo tile: `GetWarpEventAtPosition` devolve a PRIMEIRA, entao a
lapide nunca dispara, e o tile da porta antiga fica sem warp nenhum, que e o
que `TryStartWarpEventScript` (src/field_control_avatar.c:988) precisa para nao
fazer nada. Doador tem que ter indice MENOR que a lapide, senao ela sombrearia
ele; conferido caso a caso.

Tres mapas nao tem doador porque TODOS os warps deles iam para cortado
(`RockPeakRuins`, `Unova_MobileTradeRoom`, `Unova_MobileBattleRoom`). Nesses a
entrada e apagada de verdade, e o script confere antes que nenhum mapa VIVO
aponte para indice deslocado.

METADE DE PORTA NAO FECHA (regra nova de 06/09/2026, ver `gemea_viva`). Porta de
duas celulas tem um warp em cada metade, e em HearthomeCity as duas metades da
MESMA porta tinham destino diferente na fonte: (8,6) ia para o portao de Amity
Square, cortado, e (9,6) ia para o ForeignBuilding, vivo. A primeira passada
fechou so a metade cortada, e sobrou meia porta: quem encostasse na coluna da
esquerda apertava para cima e nada acontecia, e ainda lia placa de obras na porta
da igreja. Foi um dos defeitos que o Gui trouxe do playtest de 06/09/2026. Agora a metade
cortada ADOTA o destino da metade viva, e nao ha placa nenhuma nesse mapa.

A PLACA FALA INGLES E E UMA SO. O texto mora em `data/scripts/portas_fechadas.inc`
(`Common_Text_PortaFechada`), e o rotulo de cada mapa so aponta para la.

Idempotente: rodar duas vezes nao muda nada (o tumulo ja e tumulo, a lapide ja
esta na coordenada do doador, a placa ja existe).
"""
import json
import os
import re
import shutil
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import completude as C                      # noqa: E402  a tabela CORTES_DO_GUI

MAPS = f"{RAIZ}/data/maps"
# O texto da placa MORA EM UM LUGAR SO, `data/scripts/portas_fechadas.inc`, e
# esta constante e a copia que o `--demo` cruza com ele. Ate 06/09/2026 cada
# mapa carregava a sua propria copia da frase, e a frase estava EM PORTUGUES
# ("Fechado. Área em obras.") dentro de um jogo que fala ingles do inicio ao
# fim. Foi a unica fala em portugues que sobrou no jogo, e o Gui a encontrou no
# playtest, na porta da igreja de Hearthome.
TEXTO_PLACA = "Closed for renovations."
ROTULO_TEXTO = "Common_Text_PortaFechada"
INC_TEXTO = "data/scripts/portas_fechadas.inc"
MARCA = "@ >>> porta fechada (remove_mapas_cortados.py) >>>"


# --------------------------------------------------------------------- leitura
def cortados():
    """Os mapas do modo `deficit` de CORTES_DO_GUI que existem em data/maps."""
    fora = []
    for x in C.CORTES_DO_GUI:
        if x["modo"] == "deficit":
            fora += x["alvo"]
    return sorted({m for m in fora if os.path.isdir(f"{MAPS}/{m}")})


def grupos():
    return json.load(open(f"{MAPS}/map_groups.json", encoding="utf-8"))


def todos_os_mapas(g=None):
    g = g or grupos()
    return [m for grp in g["group_order"] for m in g[grp]]


def constantes():
    """nome de pasta -> MAP_*, pelo par (grupo, indice), nunca por regex.

    Mesma razao de `valida_conectividade.tabela_de_constantes`: derivar a
    constante do CamelCase erra em `OreburghCity_PokemonCenter_1F`.
    """
    g = grupos()
    pos = {(gi, i): m for gi, grp in enumerate(g["group_order"])
           for i, m in enumerate(g[grp])}
    h = open(f"{RAIZ}/include/constants/map_groups.h", encoding="utf-8").read()
    saida = {}
    for const, num, gi in re.findall(
            r"(MAP_[A-Z0-9_]+)\s*=\s*\((\d+) \| \((\d+) << 8\)\)", h):
        k = (int(gi), int(num))
        if k in pos:
            saida[pos[k]] = const
    return saida


def le_mapa(m):
    return json.load(open(f"{MAPS}/{m}/map.json", encoding="utf-8"))


def grava_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def layouts_json():
    return json.load(open(f"{RAIZ}/data/layouts/layouts.json", encoding="utf-8"))


# ------------------------------------------------------------------- a medicao
def bytes_por_mapa():
    """{mapa: bytes de ROM} lido do `pokeemerald.map` da ultima build.

    Tamanho de arquivo mentiria: `map.json` nao entra na ROM, `scripts.inc`
    entra COMPILADO, e o blockdata e compartilhado quando o layout e. Aqui cada
    simbolo do linker recebe (proximo endereco - este) e e atribuido ao mapa
    cujo nome e o prefixo MAIS LONGO dele (senao `Route225` come
    `Route225House`).
    """
    p = f"{RAIZ}/pokeemerald.map"
    if not os.path.exists(p):
        return {}
    nomes = sorted(set(todos_os_mapas()), key=len, reverse=True)
    pat = re.compile(r"^\s+0x([0-9a-f]{8})\s+(\S+)$")
    syms = {}
    for ln in open(p, errors="replace"):
        g = pat.match(ln.rstrip("\n"))
        if g:
            a = int(g.group(1), 16)
            if 0x08000000 <= a < 0x0A000000:
                syms.setdefault(a, []).append(g.group(2))
    addrs = sorted(syms)
    saida = {}
    for i, a in enumerate(addrs):
        tam = (addrs[i + 1] - a) if i + 1 < len(addrs) else 0
        dono = None
        for s in syms[a]:
            cand = s[1:] if s.startswith("g") and not s.startswith("gMap") else s
            for n in nomes:
                if cand.startswith(n) and (len(cand) == len(n) or cand[len(n)] == "_"):
                    dono = n
                    break
            if dono:
                break
        if dono:
            saida[dono] = saida.get(dono, 0) + tam
    return saida


# --------------------------------------------------- quem aponta para o cortado
def portas_vivas(cort=None, const=None):
    """[(mapa vivo, [indices de warp que vao para cortado], doador ou None)].

    `doador` e o indice do warp VIVO de menor indice do mesmo mapa, e ele so
    serve se for MENOR que todos os indices a fechar (senao a lapide sombreia).
    """
    cort = set(cort or cortados())
    const = const or constantes()
    ccons = {const[m] for m in cort if m in const}
    saida = []
    for m in todos_os_mapas():
        if m in cort or not os.path.exists(f"{MAPS}/{m}/map.json"):
            continue
        ws = le_mapa(m).get("warp_events", []) or []
        fecha = [i for i, w in enumerate(ws) if w.get("dest_map") in ccons]
        if not fecha:
            continue
        doador = next((i for i, w in enumerate(ws)
                       if w.get("dest_map") not in ccons), None)
        if doador is not None and doador > min(fecha):
            doador = None
        saida.append((m, fecha, doador))
    return saida


def ponteiros_de_entrada(cort=None, const=None):
    """{(mapa, warp_id): [(origem viva, indice)]} - so origem VIVA importa."""
    cort = set(cort or cortados())
    const = const or constantes()
    nome_de = {v: k for k, v in const.items()}
    dentro = {}
    for m in todos_os_mapas():
        if m in cort or not os.path.exists(f"{MAPS}/{m}/map.json"):
            continue
        for i, w in enumerate(le_mapa(m).get("warp_events", []) or []):
            d = nome_de.get(w.get("dest_map"))
            if d and d not in cort:
                try:
                    dentro.setdefault((d, int(w.get("dest_warp_id"))), []).append((m, i))
                except (TypeError, ValueError):
                    pass
    return dentro


def ilhados(cort=None, const=None):
    """Mapa VIVO que PERDE o unico caminho porque o vizinho dele foi cortado.

    `passagem_obrigatoria` nao pega isto: mapa que fica SOZINHO no proprio
    componente nunca aparece como componente PARTIDO. O filtro `perdeu` existe
    para nao virar ruido: metade da ROM (base secreta, sala de Battle Frontier,
    Trade Center) so e alcancavel por `special` e apareceria aqui sem ter
    perdido nada.

    Medido em 22/08/2026: sai `RockPeakRuins`, cujo unico warp ia para a
    `Route228`. Nao e defeito desta ferramenta, e escopo: quem decide se o mapa
    entra no corte e o Gui.
    """
    cort = set(cort or cortados())
    const = const or constantes()
    nome_de = {v: k for k, v in const.items()}
    todos = [m for m in todos_os_mapas() if os.path.exists(f"{MAPS}/{m}/map.json")]
    dados = {m: le_mapa(m) for m in todos}
    sai = {}
    for m, d in dados.items():
        viz = {nome_de.get(w.get("dest_map")) for w in (d.get("warp_events") or [])}
        viz |= {nome_de.get(c.get("map")) for c in (d.get("connections") or [])
                if isinstance(c, dict)}
        sai[m] = viz - {None}
    entra = {}
    for m, v in sai.items():
        for x in v:
            entra.setdefault(x, set()).add(m)
    presos = []
    for m in todos:
        if m in cort:
            continue
        vizinhos = sai[m] | entra.get(m, set())
        if (vizinhos & cort) and not (vizinhos - cort):
            presos.append(m)
    return presos


def passagem_obrigatoria(cort=None, const=None):
    """Mapas vivos que DEIXAM de se alcancar quando os cortados somem.

    BFS no grafo de warp + conexao + `destinos_dinamicos`, warp tratado como
    bidirecional (porta e porta nos dois sentidos). Lista vazia = nenhum
    cortado e corredor entre dois vivos.
    """
    cort = set(cort or cortados())
    const = const or constantes()
    nome_de = {v: k for k, v in const.items()}
    adj, todos = {}, todos_os_mapas()
    for m in todos:
        if not os.path.exists(f"{MAPS}/{m}/map.json"):
            continue
        d = le_mapa(m)
        viz = set()
        for w in d.get("warp_events", []) or []:
            n = nome_de.get(w.get("dest_map"))
            if n:
                viz.add(n)
        for c in d.get("connections") or []:
            n = nome_de.get(c.get("map")) if isinstance(c, dict) else None
            if n:
                viz.add(n)
        for n in d.get("destinos_dinamicos") or []:
            n = nome_de.get(n)
            if n:
                viz.add(n)
        for v in viz:
            adj.setdefault(m, set()).add(v)
            adj.setdefault(v, set()).add(m)

    def componentes(nos):
        nos, vis, out = set(nos), set(), []
        for s in nos:
            if s in vis:
                continue
            fila, comp = [s], []
            vis.add(s)
            while fila:
                x = fila.pop()
                comp.append(x)
                for y in adj.get(x, ()):
                    if y in nos and y not in vis:
                        vis.add(y)
                        fila.append(y)
            out.append(comp)
        return out

    vivos = [m for m in todos if m not in cort]
    idx = {m: i for i, c in enumerate(componentes(vivos)) for m in c}
    quebras = []
    for c in componentes(todos):
        vs = [m for m in c if m not in cort]
        if len({idx[m] for m in vs}) > 1:
            quebras.append(sorted(vs))
    return quebras


# --------------------------------------------------------------------- escrita
def esvazia_mapa(m):
    """O cabecalho fica, o conteudo sai. Devolve True se mudou alguma coisa."""
    p = f"{MAPS}/{m}/map.json"
    d = le_mapa(m)
    novo = dict(d)
    novo["region_map_section"] = "MAPSEC_NONE"
    novo["connections"] = None
    for k in ("object_events", "warp_events", "coord_events", "bg_events"):
        novo[k] = []
    novo["destinos_dinamicos"] = []
    novo["cortado_por"] = "decisao do Gui 21/08/2026, ver PLANO-ESCOPO.md"
    mudou = novo != d
    if mudou:
        grava_json(p, novo)
    ps = f"{MAPS}/{m}/scripts.inc"
    corpo = (f"@ Mapa CORTADO do escopo (PLANO-ESCOPO.md). O rotulo abaixo fica\n"
             f"@ porque header.inc, gerado, aponta para ele.\n\n"
             f"{m}_MapScripts::\n\t.byte 0\n")
    if not os.path.exists(ps) or open(ps, encoding="utf-8", errors="replace").read() != corpo:
        open(ps, "w", encoding="utf-8").write(corpo)
        mudou = True
    return mudou


def layouts_exclusivos(cort=None):
    """Layouts usados SO por mapa cortado (os compartilhados nao sao tocados)."""
    cort = set(cort or cortados())
    uso = {}
    for m in todos_os_mapas():
        if os.path.exists(f"{MAPS}/{m}/map.json"):
            uso.setdefault(le_mapa(m).get("layout"), []).append(m)
    dos_cortados = {le_mapa(m).get("layout") for m in cort}
    return sorted(l for l in dos_cortados
                  if l and all(x in cort for x in uso.get(l, [])))


def encolhe_layouts(lista, aplicar=False):
    """1x1: 2 B de blockdata e 8 B de borda. O ORDINAL do layout nao muda."""
    L = layouts_json()
    liberado, mexidos = 0, 0
    for x in L["layouts"]:
        if x["id"] not in lista:
            continue
        bd = f"{RAIZ}/{x['blockdata_filepath']}"
        bo = f"{RAIZ}/{x['border_filepath']}"
        antes = sum(os.path.getsize(p) for p in (bd, bo) if os.path.exists(p))
        if x["width"] == 1 and x["height"] == 1 and antes <= 10:
            continue
        mexidos += 1
        liberado += antes - 10
        if aplicar:
            x["width"], x["height"] = 1, 1
            os.makedirs(os.path.dirname(bd), exist_ok=True)
            open(bd, "wb").write(b"\x00\x00")
            open(bo, "wb").write(b"\x00\x00" * 4)
    if aplicar and mexidos:
        grava_json(f"{RAIZ}/data/layouts/layouts.json", L)
    return mexidos, liberado


def tira_mato(cort=None, const=None, aplicar=False):
    """Tira as tabelas de mato dos cortados POR CHAVE, sem reescrever o resto."""
    cort = set(cort or cortados())
    const = const or constantes()
    ccons = {const[m] for m in cort if m in const}
    p = f"{RAIZ}/src/data/wild_encounters.json"
    W = json.load(open(p, encoding="utf-8"))
    fora = []
    for grupo in W["wild_encounter_groups"]:
        enc = grupo.get("encounters")
        if not enc:
            continue
        fica = [e for e in enc if e.get("map") not in ccons]
        fora += [e["map"] for e in enc if e.get("map") in ccons]
        grupo["encounters"] = fica
    if fora and aplicar:
        grava_json(p, W)
    return fora


def _placa_em(d, x, y, script):
    for b in d.get("bg_events") or []:
        if b.get("script") == script:
            return False
    d.setdefault("bg_events", []).append({
        "type": "sign", "x": x, "y": y, "elevation": 0,
        "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
        "script": script,
        "origem": "porta fechada (remove_mapas_cortados.py)",
    })
    return True


def _tile_da_placa(d, wx, wy, ocupados):
    """Parede vizinha da porta; se nao houver, a propria porta."""
    import lendarios_sinnoh as LS
    try:
        W, H, g = LS.grade(d["layout"])
    except Exception:
        return wx, wy
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        x, y = wx + dx, wy + dy
        if 0 <= x < W and 0 <= y < H and not LS.anda(g[y][x]) and (x, y) not in ocupados:
            return x, y
    return wx, wy


def celula_da_porta(d, ws, i):
    """(x, y) da porta ORIGINAL do warp i, mesmo depois de ele virar lapide."""
    o = ws[i].get("porta_original")
    return (o[0], o[1]) if o else (ws[i]["x"], ws[i]["y"])


def gemea_viva(d, ws, i, ccons):
    """Indice do warp VIVO que divide a MESMA porta com o warp `i`, ou None.

    ACHADO NO PLAYTEST DE 06/09/2026, e a razao desta regra existir. Porta de
    DUAS celulas tem um warp em cada metade, e em HearthomeCity as duas metades
    da mesma porta tinham destinos DIFERENTES na fonte: (8,6) ia para o portao
    de Amity Square, que o Gui cortou, e (9,6) ia para o ForeignBuilding, que
    esta vivo. Fechar so a metade cortada deixou meia porta: o jogador que
    encostasse na coluna da esquerda apertava para cima e nao acontecia nada, e
    ainda lia a placa de obras na porta da igreja. Ele reportou como "nao estou
    entrando no castelo bonito da esquerda".

    A metade cortada ADOTA o destino da metade viva em vez de virar lapide.
    Gemea e a celula VIZINHA nas quatro direcoes que tem o MESMO metatile (e a
    mesma porta desenhada, e nao duas portas encostadas) e um warp VIVO em cima.
    """
    import lendarios_sinnoh as LS
    try:
        W, H, g = LS.grade(d["layout"])
    except Exception:
        return None
    x, y = celula_da_porta(d, ws, i)
    if not (0 <= x < W and 0 <= y < H):
        return None
    meu = g[y][x] & 0x3FF
    vivos = {}
    for j, w in enumerate(ws):
        if j == i or w.get("dest_map") in ccons or w.get("fechado"):
            continue
        vivos.setdefault((w["x"], w["y"]), j)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        p = (x + dx, y + dy)
        if p in vivos and 0 <= p[0] < W and 0 <= p[1] < H \
                and (g[p[1]][p[0]] & 0x3FF) == meu:
            return vivos[p]
    return None


def fecha_portas(cort=None, const=None, aplicar=False):
    """Lapide no warp, placa ao lado. Devolve [(mapa, indices, modo, placa)]."""
    cort = set(cort or cortados())
    const = const or constantes()
    ccons = {const[x] for x in cort if x in const}
    dentro = ponteiros_de_entrada(cort, const)
    feito = []
    for m, fecha, doador in portas_vivas(cort, const):
        d = le_mapa(m)
        ws = d["warp_events"]
        # METADE DE PORTA VIVA ADOTA A GEMEA, e nunca vira lapide (ver
        # `gemea_viva`): fechar meia porta e pior que fechar a porta inteira.
        adotam = {}
        for i in list(fecha):
            j = gemea_viva(d, ws, i, ccons)
            if j is not None:
                adotam[i] = j
        for i, j in adotam.items():
            x, y = celula_da_porta(d, ws, i)
            ws[i] = {"x": x, "y": y, "elevation": ws[j]["elevation"],
                     "dest_map": ws[j]["dest_map"],
                     "dest_warp_id": ws[j]["dest_warp_id"],
                     "gemea": f"metade da mesma porta do warp {j}"}
        fecha = [i for i in fecha if i not in adotam]
        ocupados = {(b["x"], b["y"]) for b in (d.get("bg_events") or [])}
        script = f"{m}_EventScript_PortaFechada"
        alvo = None
        if not fecha:
            modo = "gemea"
        elif doador is not None:
            modo = "lapide"
            dx, dy = ws[doador]["x"], ws[doador]["y"]
            doa = ws[doador]
            for i in fecha:
                if not ws[i].get("porta_original"):
                    alvo = alvo or _tile_da_placa(d, ws[i]["x"], ws[i]["y"], ocupados)
                    orig = [ws[i]["x"], ws[i]["y"], ws[i]["dest_map"]]
                else:
                    orig = ws[i]["porta_original"]
                # COPIA INTEIRA do doador, nao so a coordenada: o destino
                # tambem, senao a lapide fica apontando para um tumulo de 0
                # warps e `valida_conectividade` a conta como warp quebrado.
                ws[i] = dict(ws[i], x=dx, y=dy,
                             dest_map=doa["dest_map"],
                             dest_warp_id=doa["dest_warp_id"],
                             porta_original=orig,
                             fechado="porta fechada, ver PLANO-ESCOPO.md")
        else:
            modo = "apagado"
            k = min(fecha)
            presos = [t for idx in range(k, len(ws)) for t in dentro.get((m, idx), [])]
            if presos:
                raise SystemExit(f"{m}: apagar warp {k} desloca ponteiro vivo {presos}")
            if fecha:
                alvo = _tile_da_placa(d, ws[fecha[0]]["x"], ws[fecha[0]]["y"], ocupados)
            d["warp_events"] = [w for i, w in enumerate(ws) if i not in set(fecha)]
        if alvo:
            _placa_em(d, alvo[0], alvo[1], script)
        feito.append((m, fecha + sorted(adotam), modo, alvo))
        if aplicar:
            grava_json(f"{MAPS}/{m}/map.json", d)
            if alvo:
                _append_script_placa(m, script)
    return feito


def _append_script_placa(m, script):
    p = f"{MAPS}/{m}/scripts.inc"
    t = open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""
    if script in t:
        return
    t += (f"\n{MARCA}\n{script}::\n"
          f"\tmsgbox {ROTULO_TEXTO}, MSGBOX_SIGN\n\tend\n"
          f"@ <<< porta fechada <<<\n")
    open(p, "w", encoding="utf-8").write(t)


def fecha_barco_snowpoint(aplicar=False):
    """O marinheiro de Snowpoint ja tinha o ramo `Fechado`: ele passa a ser o unico."""
    p = f"{MAPS}/SnowpointCity/scripts.inc"
    t = open(p, encoding="utf-8", errors="replace").read()
    velho = ("\tgoto_if_unset FLAG_ELITE_SINNOH_VENCIDA, "
             "SnowpointCity_EventScript_SailorFechado\n")
    novo = ("@ A Battle Zone saiu do escopo (PLANO-ESCOPO.md, 21/08/2026): a viagem\n"
            "@ some e o marinheiro fica no ramo que ja existia.\n"
            "\tgoto SnowpointCity_EventScript_SailorFechado\n")
    if velho not in t:
        return False
    corta = t.index(velho)
    fim = t.index("SnowpointCity_EventScript_SailorFechado::", corta)
    if aplicar:
        open(p, "w", encoding="utf-8").write(t[:corta] + novo + "\n" + t[fim:])
    return True


# Simbolo que NASCEU dentro de um mapa cortado e que um mapa VIVO usa.
#
# Achado pelo LINKER, nao pela leitura: a varredura de prefixo tinha descartado
# `Unova_EventScript_CacaNiquel` como colisao de substring (`Unova_GameCorner`
# tem `GameCorner` dentro), e so o `undefined reference` da build de 22/08/2026
# mostrou que o caca-niquel de NIMBASA (vivo) chama o roteiro que morava no
# GAME CORNER DA CASTELIA PLAZA (cortado). O corpo vai INTEIRO para o mapa
# vivo que o usa; nada aqui e reescrito, e a copia e literal.
MIGRAR = [
    ("Unova_CasteliaPlazaGameCorner", "Unova_GameCorner",
     "Unova_EventScript_CacaNiquel",
     "Unova_EventScript_CacaNiquel::\n"
     "\tlockall\n"
     "\tcheckitem ITEM_COIN_CASE\n"
     "\tgoto_if_eq VAR_RESULT, FALSE, MauvilleCity_GameCorner_EventScript_NoCoinCase\n"
     "\tspecialvar VAR_RESULT, GetSlotMachineId\n"
     "\tplayslotmachine VAR_RESULT\n"
     "\treleaseall\n"
     "\tend\n"),
]


def migra_simbolos(aplicar=False):
    """Leva para o mapa VIVO o rotulo que o mapa cortado exportava."""
    feito = []
    for origem, destino, simbolo, corpo in MIGRAR:
        p = f"{MAPS}/{destino}/scripts.inc"
        t = open(p, encoding="utf-8", errors="replace").read()
        if f"{simbolo}::" in t:
            continue
        feito.append((simbolo, origem, destino))
        if aplicar:
            open(p, "w", encoding="utf-8").write(
                t + f"\n@ migrado de {origem}, que virou tumulo "
                    f"(remove_mapas_cortados.py)\n" + corpo)
    return feito


def tira_turnback_inc(aplicar=False):
    """`data/scripts/turnback_cave.inc` so serve a Turnback, que saiu inteira."""
    inc = f"{RAIZ}/data/scripts/turnback_cave.inc"
    ev = f"{RAIZ}/data/event_scripts.s"
    linha = '\t.include "data/scripts/turnback_cave.inc"\n'
    t = open(ev, encoding="utf-8").read()
    if linha not in t and not os.path.exists(inc):
        return False
    if aplicar:
        if linha in t:
            open(ev, "w", encoding="utf-8").write(t.replace(linha, ""))
        if os.path.exists(inc):
            os.remove(inc)
    return True


# ----------------------------------------------------------------------- saida
def tabela(cort, medida, portas, mato):
    por_porta = {m: (f, modo) for m, f, modo, _ in portas}
    origem = {}
    const = constantes()
    ccons = {const[m]: m for m in cort if m in const}
    for m, f, _modo, _ in portas:
        for i in f:
            pass
    for m in todos_os_mapas():
        if m in cort or not os.path.exists(f"{MAPS}/{m}/map.json"):
            continue
        for w in le_mapa(m).get("warp_events", []) or []:
            if w.get("dest_map") in ccons:
                origem.setdefault(ccons[w["dest_map"]], []).append(m)
    linhas = []
    for m in cort:
        kb = medida.get(m, 0) / 1024
        quem = ", ".join(sorted(set(origem.get(m, [])))) or "ninguem vivo"
        linhas.append((m, kb, quem, "tumulo"))
    return linhas, por_porta


def relatorio(aplicar=False):
    cort = cortados()
    const = constantes()
    medida = bytes_por_mapa()
    quebras = passagem_obrigatoria(cort, const)
    exclusivos = layouts_exclusivos(cort)
    portas = fecha_portas(cort, const, aplicar=False)
    linhas, _ = tabela(cort, medida, portas, [])
    total = sum(medida.get(m, 0) for m in cort)
    print(f"mapas cortados que existem em data/maps: {len(cort)}")
    print(f"peso medido no pokeemerald.map: {total} B ({total/1024:.1f} KB)")
    print()
    print(f"{'mapa':44s} {'KB':>7}  quem apontava")
    for m, kb, quem, _v in sorted(linhas, key=lambda x: -x[1])[:25]:
        print(f"{m:44s} {kb:7.1f}  {quem[:60]}")
    print(f"... e mais {max(0, len(linhas)-25)} com peso menor")
    print()
    print(f"layouts exclusivos dos cortados (encolhem para 1x1): {len(exclusivos)}")
    n, lib = encolhe_layouts(exclusivos, aplicar=False)
    print(f"  blockdata+borda que sai: {lib} B ({lib/1024:.1f} KB) em {n} layouts")
    print(f"tabelas de mato a tirar: {len(tira_mato(cort, const, aplicar=False))}")
    print()
    print(f"portas vivas a fechar: {sum(len(f) for _m, f, _mo, _p in portas)} "
          f"warps em {len(portas)} mapas")
    for m, f, modo, placa in portas:
        print(f"  {m:34s} warps {f} -> {modo:8s} placa em {placa}")
    print()
    print(f"simbolos a migrar para mapa vivo: {migra_simbolos(aplicar=False)}")
    print("passagem obrigatoria entre dois mapas VIVOS: "
          f"{'NENHUMA' if not quebras else quebras}")
    ilhas = ilhados(cort, const)
    print(f"mapas VIVOS que ficam sem caminho nenhum: "
          f"{'NENHUM' if not ilhas else ilhas}")
    if not aplicar:
        print("\n(--dry-run: nada foi escrito)")
        return 0

    mudou = sum(1 for m in cort if esvazia_mapa(m))
    n, lib = encolhe_layouts(exclusivos, aplicar=True)
    fora = tira_mato(cort, const, aplicar=True)
    fecha_portas(cort, const, aplicar=True)
    migra_simbolos(aplicar=True)
    fecha_barco_snowpoint(aplicar=True)
    tira_turnback_inc(aplicar=True)
    print(f"\nAPLICADO: {mudou} mapas viraram tumulo, {n} layouts encolhidos "
          f"({lib/1024:.1f} KB), {len(fora)} tabelas de mato fora.")
    return 0


# ------------------------------------------------------------------------ demo
def demo():
    """Autoteste. As duas mutacoes plantadas sao as duas que MATAM o jogo."""
    cort = cortados()
    const = constantes()
    # O numero NAO fica cravado (23/08/2026): ele estava em 111 e a lista do Gui
    # ja tinha ido a 113, entao o `--demo` reprovava por envelhecimento e nao por
    # defeito. O que vale afirmar aqui e que `cortados()` le a MESMA lista que
    # mede (`completude.CORTES_DO_GUI`, modo `deficit`) e nao perde entrada pelo
    # caminho: numero decorado envelhece, cruzamento nao.
    declarados = {m for x in C.CORTES_DO_GUI if x["modo"] == "deficit"
                  for m in x["alvo"]}
    assert set(cort) == {m for m in declarados if os.path.isdir(f"{MAPS}/{m}")}
    # A LINHA DE BAIXO JA FOI `assert len(cort) >= 100`, e ela envelheceu do jeito
    # que o comentario acima tinha acabado de proibir: em 07/09/2026 a decisao 48
    # do Gui devolveu 32 mapas ao escopo (ver `ressuscita_mapas_sinnoh.py`), a
    # conta caiu de 102 para 70 e o `--demo` reprovou por ENVELHECIMENTO, com a
    # tabela sa e a ferramenta certa. O que esta trava precisa provar e que a
    # lista nao se esvaziou nem virou outra coisa, e isso se prova por
    # CRUZAMENTO: a Battle Zone e o maior bloco cortado e nenhuma decisao a
    # revogou, entao ela tem que estar inteira aqui. Se um dia ela voltar
    # tambem, esta linha muda junto com a tabela, e nao um ano depois.
    zona = {m for x in C.CORTES_DO_GUI
            if x["modo"] == "deficit" and x["grupo"].startswith("Battle Zone")
            for m in x["alvo"]}
    assert zona and zona <= set(cort), sorted(zona - set(cort))

    # 1. mapa que e PASSAGEM OBRIGATORIA entre dois vivos reprova.
    #    Planto um cortado no meio do unico caminho: se o BFS nao acusar, a
    #    ferramenta esta cega e um corte partiria o mundo em dois.
    quebras = passagem_obrigatoria(cort, const)
    so_ilhados = all(len(q) == 1 or set(q) <= {"Unova_MobileTradeRoom",
                                               "Unova_MobileBattleRoom"}
                     for q in quebras)
    assert so_ilhados, quebras
    falso = cort + ["Route214"]          # Route214 e corredor de Sinnoh
    assert passagem_obrigatoria(falso, const), \
        "o BFS nao viu a passagem obrigatoria plantada"

    # 2. warp VIVO apontando para mapa removido reprova. Depois de aplicar,
    #    nenhum warp de mapa vivo pode ter destino cortado.
    ccons = {const[m] for m in cort if m in const}
    vivos_apontando = [m for m in todos_os_mapas()
                       if m not in cort and os.path.exists(f"{MAPS}/{m}/map.json")
                       and any(w.get("dest_map") in ccons and
                               not w.get("fechado")
                               for w in (le_mapa(m).get("warp_events") or []))]
    if os.environ.get("REMOVE_CORTADOS_APLICADO"):
        assert not vivos_apontando, vivos_apontando

    # 3. o doador da lapide TEM que ter indice menor, senao ela sombreia ele.
    for m, fecha, doador in portas_vivas(cort, const):
        assert doador is None or doador < min(fecha), (m, fecha, doador)

    # 4. layout compartilhado com mapa vivo nunca entra na lista de encolher.
    excl = set(layouts_exclusivos(cort))
    for m in todos_os_mapas():
        if m in cort or not os.path.exists(f"{MAPS}/{m}/map.json"):
            continue
        assert le_mapa(m).get("layout") not in excl, m

    # 5. NENHUM CAPITULO DO SELETOR LARGA O JOGADOR NUM TUMULO.
    #    Pergunta do condutor em 22/08/2026: "da para entrar num tumulo pelo
    #    seletor de capitulo?". A resposta e medida, e nao lembrada: o seletor
    #    (src/chapter_jump.c) so oferece HEAL_LOCATION de cidade de ginasio e de
    #    Liga, e nenhuma delas mora em mapa cortado. Nada precisou sair; o que
    #    faltava era a trava, porque cortar uma cidade de ginasio um dia daria
    #    um capitulo que teleporta para um mapa vazio SEM SAIDA, e nem o build
    #    nem a suite diriam nada. Chapter Jump e o unico caminho do jogo que
    #    ignora warp.
    curas = re.findall(r"CURA\((HEAL_LOCATION_[A-Z0-9_]+)\)",
                       open(f"{RAIZ}/src/chapter_jump.c", encoding="utf-8").read())
    # ESTA LINHA JA FOI `assert len(curas) > 40`, e ela morreu ANTES desta onda:
    # o commit 4aca7c5647 ("Cartucho 1, onda 1: o codigo para de conhecer Unova e
    # Galar") tirou os capitulos daquelas duas regioes e a conta bateu em 40
    # exatos, ou seja o `--demo` ja reprovava no commit base 7262639f25, por
    # envelhecimento e nao por defeito. Numero decorado de novo, o terceiro
    # deste arquivo. O que precisa ser verdade aqui e so que o regex continua
    # casando alguma coisa: quem realmente trava o passo 5 e o laco abaixo, que
    # confere CADA cura contra heal_locations.json e contra a lista de tumulos, e
    # esse laco nao vale nada se a lista vier vazia por regex quebrado.
    assert curas, "o regex de CURA() parou de casar em src/chapter_jump.c"
    mapa_da_cura = {h["id"]: h["map"] for h in json.load(
        open(f"{RAIZ}/src/data/heal_locations.json", encoding="utf-8")
    )["heal_locations"]}
    tumulos = {const[m] for m in cort if m in const}
    for c in curas:
        assert c in mapa_da_cura, f"{c} nao existe em heal_locations.json"
        assert mapa_da_cura[c] not in tumulos, \
            f"o capitulo de {c} larga o jogador em {mapa_da_cura[c]}, que e tumulo"

    # 6. a placa e UMA SO, esta em INGLES, e o arquivo compartilhado tem
    #    exatamente o texto que esta constante promete. Antes de 06/09/2026 a
    #    checagem so perguntava se o acento cabia no charmap, e por isso ficou
    #    muda enquanto a unica fala em portugues do jogo estava em 22 mapas.
    inc = open(f"{RAIZ}/{INC_TEXTO}", encoding="utf-8").read()
    assert f'{ROTULO_TEXTO}:\n\t.string "{TEXTO_PLACA}$"' in inc, INC_TEXTO
    assert TEXTO_PLACA.isascii(), TEXTO_PLACA
    for mapa in os.listdir(MAPS):
        f = f"{MAPS}/{mapa}/scripts.inc"
        if not os.path.isfile(f):
            continue
        corpo = open(f, encoding="utf-8", errors="replace").read()
        if "_EventScript_PortaFechada" in corpo:
            assert f"{mapa}_Text_PortaFechada" not in corpo, \
                f"{mapa} ainda tem copia propria do texto da placa"

    # 7. METADE DE PORTA VIVA NUNCA FECHA. Mutacao plantada: ponho de volta em
    #    HearthomeCity o warp cortado de (8,6), que divide porta com o warp vivo
    #    do ForeignBuilding em (9,6), e cobro que `gemea_viva` ache o vizinho.
    #    Sem esta regra o mapa volta a ter meia porta, que foi o defeito do
    #    playtest e nao aparece em nenhum validador estatico.
    d = le_mapa("HearthomeCity")
    ws = list(d["warp_events"])
    alvo = next(i for i, w in enumerate(ws)
                if w["dest_map"] == "MAP_FOREIGN_BUILDING" and (w["x"], w["y"]) == (9, 6))
    ws.append({"x": 8, "y": 6, "elevation": 0,
               "dest_map": "MAP_HEARTHOME_CITY_WEST_GATE_TO_AMITY_SQUARE",
               "dest_warp_id": "0"})
    ccons = {const[m] for m in cort if m in const}
    assert gemea_viva(d, ws, len(ws) - 1, ccons) == alvo, "gemea_viva ficou cega"
    #    contraprova: warp de porta SOLTA (sem vizinho de mesmo metatile) nao
    #    pode achar gemea nenhuma, senao a regra reabriria porta que e corte.
    ws[-1] = dict(ws[-1], x=29, y=26)
    assert gemea_viva(d, ws, len(ws) - 1, ccons) is None, \
        "gemea_viva casou porta que nao e a mesma"
    print("demo: ok")
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    return relatorio(aplicar="--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
