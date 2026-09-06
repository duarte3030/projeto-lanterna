#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AS PORTAS MORTAS DE GALAR: warp da fonte que nao tem para onde levar.

    python3 dev_scripts/portas_mortas_galar.py            # relatorio, nao grava
    python3 dev_scripts/portas_mortas_galar.py --lista    # uma linha por porta
    python3 dev_scripts/portas_mortas_galar.py --aplicar  # grava
    python3 dev_scripts/portas_mortas_galar.py --demo     # autoteste, nao grava

## O que sao as 226

Saida de varredura do G3 (`pendencias_warp` em `dev_scripts/galar_mundo.json`), e
o tipo `porta_morta` de `dev_scripts/fila_galar.py`. Duas familias, medidas e nao
escritas:

    188  o destino da fonte e mapa vanilla do FireRed que o demake nao
         redesenhou, entao ele NAO EXISTE na nossa arvore (0.0 responde por 95
         e 1.76 por 25);
     38  o destino existe, mas o warp de CHEGADA que a fonte cita nao existe
         nele (a fonte pede o warp 13 de um mapa que tem 7).

O G3 resolveu as duas do mesmo jeito: apontou o warp para ELE MESMO. Sao 225
auto-warps de 226. Auto-warp em porta de verdade e defeito visivel: o jogador
encosta na porta, a tela apaga e ele reaparece no mesmo lugar.

## A MEDICAO QUE MANDA NO CONSERTO: so 49 das 226 disparam

Warp so dispara se o TILE embaixo dele tiver comportamento de porta, escada ou
seta (`valida_warp_tile.warp_morto`, a mesma tabela que a `lente_portas` usa).
Medido nesta arvore, celula a celula:

    49  o tile e porta (34 `MB_ANIMATED_DOOR`), escada (10 `MB_LADDER` e 1
        `MB_UP_RIGHT_STAIR_WARP`) ou seta (4 `MB_SOUTH_ARROW_WARP`): a porta
        existe no desenho, o jogador a ve e ela devolve ele para o proprio lugar;
   177  o tile e `MB_NORMAL`, `MB_TALL_GRASS`, `MB_BOOKSHELF` e afins: o warp
        NUNCA e chamado pelo motor. Nao ha porta desenhada ali, e portanto nao
        ha porta para fechar.

Essa divisao e a razao de este gerador nao aplicar o mesmo remedio nas 226. Por
placa de "Closed for renovations." em cima de 176 tiles que nao sao porta seria
plantar 176 letreiros no meio do chao.

## O MOLDE E O DO MASTER, e ele veio das 44 portas fechadas da rodada 13

`dev_scripts/remove_mapas_cortados.py`, funcao `fecha_portas` (o bloco `modo ==
"lapide"`), e o retrato dela no `ESTADO.md` ("O retrato das 44: sao 22 mapas, 26
portas e 24 tumulos"). O molde tem tres partes, e as tres estao reproduzidas
aqui:

 1. LAPIDE. A entrada de warp NAO e apagada: ela fica no mesmo indice e recebe a
    COPIA INTEIRA de um warp DOADOR do proprio mapa (x, y, `dest_map` e
    `dest_warp_id`), mais os campos `porta_original` (a celula e o destino que
    ela tinha) e `fechado`. O tile da porta velha fica SEM warp em cima, que e o
    que `TryStartWarpEventScript` (src/field_control_avatar.c) precisa para nao
    fazer nada. Indice fica onde estava, entao nenhum ponteiro de entrada e
    nenhum `warp` de script anda de lugar.
 2. PLACA. Um `bg_event` do tipo `sign` na parede vizinha da porta que fechou
    (a mesma escolha de celula do `_tile_da_placa` do master), apontando para um
    script que so faz `msgbox ..., MSGBOX_SIGN`.
 3. O TEXTO E UM SO E FALA INGLES. `Common_Text_PortaFechada` em
    `data/scripts/portas_fechadas.inc`: "Closed for renovations.". Aqui o rotulo
    e `GalarPortaFechada`, em `data/scripts/galar_portas_fechadas.inc`, e ele
    aponta para esse mesmo texto: um rotulo para os 40 e poucos mapas de Galar,
    em vez de uma copia por mapa.

## Os seis vereditos, e quando cada um vale

    ja_viva     o warp NAO e auto-warp: ele ja aponta para mapa vivo e a volta
                existe. Nada a fazer; a linha da fila fecha por medicao.
    religada    o warp DISPARA e o indice dele e alvo de warp vivo de OUTRO
                mapa, ou seja ele e a saida por onde alguem entrou. Fechar
                prenderia o jogador dentro, e apagar quebraria o warp de quem
                entra. Ele passa a devolver para o mapa de onde a entrada vem
                (ida e volta), que e a regra 18 da rodada 13 ("quem entra por
                uma porta sai por ela").
    lapide      o warp DISPARA e o mapa tem outro warp que sirva de doador.
                Molde do master, com placa.
    apagada     o warp DISPARA e o mapa NAO tem doador nenhum (todos os warps
                dele sao porta morta e todos disparam). Modo `apagado` do
                master. Confere antes que nenhum ponteiro vivo, de `map.json` ou
                de `warp` de script, cite indice deslocado.
    inerte      o warp NAO dispara. Fica onde esta e ganha `fechado` e
                `porta_original`, que e o mesmo vocabulario da lapide. Sem
                placa, porque nao ha porta desenhada. Mexer no indice aqui seria
                risco por ganho zero.
    adiada      o warp DISPARA e MAIS DE UM mapa entra por este mesmo indice.
                Nao existe UMA volta certa, e devolver para o primeiro da lista
                seria sortear o destino; a volta certa e o retorno dinamico de
                predio compartilhado (`DefinirRetornoPredioCompartilhado`, os
                consertos 1 e 3 da rodada 13), que e SCRIPT e nao `map.json`.
                A linha da fila continua cobrando, com o motivo escrito.

DOADOR PODE SER OUTRA PORTA MORTA INERTE, e isso e de proposito. O master so
tinha doador vivo; aqui ha mapa cujos warps sao TODOS porta morta. Quando um
deles e inerte (tile que nao dispara), ele serve de doador do mesmo jeito: a
lapide vira uma copia dele, em cima de um tile que nao dispara, e o motor nunca
chama nenhum dos dois. Isso fecha a porta sem apagar entrada nenhuma, e por isso
`apagada` sobra so para o mapa em que TODOS os warps disparam.

Idempotente: rodar duas vezes nao muda byte nenhum (a lapide ja esta na celula
do doador, a placa ja existe, o inerte ja tem `fechado`).

DONO DE ARQUIVO: este gerador escreve `warp_events` e `bg_events` de
`data/maps/Galar_*/map.json`, `data/scripts/galar_portas_fechadas.inc`, o
include dele em `data/event_scripts.s` e as linhas `porta_morta` de
`dev_scripts/fila_galar.json`. Nada mais. Ele RE-LE cada `map.json` no instante
de gravar e troca so essas duas chaves, porque outras frentes escrevem
`object_events` nos mesmos arquivos ao mesmo tempo.
"""
import argparse
import collections
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts", "qa"))

import remove_mapas_cortados as R          # noqa: E402  o molde, e `constantes()`
import lendarios_sinnoh as LS              # noqa: E402  blockdata e `anda`
import valida_warp_tile as vwt             # noqa: E402  `warp_morto`
import lente_portas as LP                  # noqa: E402  `Grade` e `DE_FAMILIA`

MAPS = f"{RAIZ}/data/maps"
MUNDO = f"{RAIZ}/dev_scripts/galar_mundo.json"
FILA = f"{RAIZ}/dev_scripts/fila_galar.json"
INC = f"{RAIZ}/data/scripts/galar_portas_fechadas.inc"
INC_REL = "data/scripts/galar_portas_fechadas.inc"
EVENT_SCRIPTS = f"{RAIZ}/data/event_scripts.s"
DEPOIS_DE = 'data/scripts/galar_placas_c.inc'

ROTULO = "GalarPortaFechada"
# O TEXTO NAO E NOVO: e o mesmo `Common_Text_PortaFechada` das 44 portas
# fechadas da rodada 13, em `data/scripts/portas_fechadas.inc`. Esta constante e
# a copia que o `--demo` cruza com o arquivo do master, para o dia em que alguem
# mudar a frase la e esquecer daqui.
TEXTO = "Closed for renovations."
ROTULO_TEXTO = "Common_Text_PortaFechada"
INC_TEXTO_MASTER = f"{RAIZ}/data/scripts/portas_fechadas.inc"

MARCA_FECHADO = "porta morta de Galar, ver dev_scripts/portas_mortas_galar.py"
ORIGEM_PLACA = "porta fechada (portas_mortas_galar.py)"

CORPO_INC = f"""@ A placa das PORTAS MORTAS de Galar, e ela e UMA SO para a regiao inteira.
@
@ Porta morta e warp que a fonte de Galar tem e que nao tem para onde levar aqui:
@ ou o destino e mapa vanilla do FireRed que o demake nao redesenhou, ou o warp
@ de chegada que a fonte cita nao existe no destino. O G3 apontou os 226 para
@ eles mesmos, e auto-warp em porta de verdade e defeito visivel: o jogador
@ encosta na porta, a tela apaga e ele reaparece no mesmo lugar.
@
@ O molde e o mesmo das 44 portas fechadas da rodada 13
@ (`dev_scripts/remove_mapas_cortados.py`, funcao `fecha_portas`): a entrada de
@ warp vira lapide na celula de um doador do proprio mapa, o tile da porta fica
@ sem warp em cima e uma placa `sign` na parede vizinha diz por que.
@
@ O TEXTO E O DO MASTER, e nao uma copia: `{ROTULO_TEXTO}` mora em
@ `data/scripts/portas_fechadas.inc`, em ingles, porque o jogo fala ingles do
@ inicio ao fim (a unica fala em portugues que sobrava foi a que o Gui achou na
@ porta da igreja de Hearthome, no playtest de 06/09/2026). Aqui ha UM rotulo
@ para a regiao inteira em vez de um por mapa, que era so heranca de como o
@ gerador do corte funcionava.
{ROTULO}::
\tmsgbox {ROTULO_TEXTO}, MSGBOX_SIGN
\tend
"""


# ------------------------------------------------------------------- a leitura
def mundo():
    return json.load(open(MUNDO, encoding="utf-8"))


def le(m):
    return json.load(open(f"{MAPS}/{m}/map.json", encoding="utf-8"))


def mapas_todos():
    return {m: le(m) for m in R.todos_os_mapas()}


def ponteiros_de_entrada(mapas, const):
    """{(pasta, indice): [quem aponta]}, so de warp de OUTRO mapa.

    Auto-referencia nao conta: warp que aponta para o proprio indice e
    exatamente a porta morta que estamos fechando, e conta-la travaria o
    conserto contra ele mesmo.
    """
    inv = {v: k for k, v in const.items()}
    dentro = collections.defaultdict(list)
    for n, d in mapas.items():
        for i, w in enumerate(d.get("warp_events") or []):
            alvo = inv.get(w.get("dest_map"))
            wid = str(w.get("dest_warp_id"))
            if alvo is None or not wid.isdigit() or alvo == n:
                continue
            dentro[(alvo, int(wid))].append((n, i))
    return dentro


PAT_WARP_SCRIPT = re.compile(
    r"\bwarp(?:silent|hole|teleport|door|spin)?\s+(MAP_[A-Z0-9_]+)\s*,\s*(\d+)")


def warps_de_script(const):
    """{(pasta, indice): n} dos `warp MAP_X, N` escritos nos .inc.

    LICAO DA RODADA 13, escrita no ESTADO: "mapa sem `warp_event` de entrada nao
    e mapa orfao ate o `grep` no `scripts.inc` dizer que e". Varredura de warp
    nao enxerga entrada de script, e apagar um `warp_event` desloca os indices
    que esses comandos citam.
    """
    inv = {v: k for k, v in const.items()}
    saida = collections.Counter()
    alvos = [f"{MAPS}/{m}/scripts.inc" for m in R.todos_os_mapas()]
    alvos += [os.path.join(f"{RAIZ}/data/scripts", f)
              for f in sorted(os.listdir(f"{RAIZ}/data/scripts"))
              if f.endswith(".inc")]
    for p in alvos:
        if not os.path.exists(p):
            continue
        for mm, wid in PAT_WARP_SCRIPT.findall(
                open(p, encoding="utf-8", errors="replace").read()):
            if mm in inv:
                saida[(inv[mm], int(wid))] += 1
    return saida


class Tiles:
    """Comportamento de cada celula, por mapa, com cache. Le o blockdata."""

    def __init__(self):
        self.lente = LP.Grade(RAIZ)
        self.cache = {}

    def de(self, m, d):
        if m not in self.cache:
            try:
                self.cache[m] = self.lente.de(d)
            except Exception:                                   # noqa: BLE001
                self.cache[m] = None
        return self.cache[m]

    def dispara(self, m, d, x, y):
        """True se o motor chama o warp que estiver nessa celula."""
        c = self.de(m, d)
        if not c or (x, y) not in c:
            return False
        morto, _ = vwt.warp_morto(c[(x, y)][0], c[(x, y)][1])
        return not morto

    def e_porta(self, m, d, x, y):
        c = self.de(m, d)
        return bool(c and (x, y) in c and c[(x, y)][0] in LP.DE_FAMILIA)


def tile_da_placa(m, d, wx, wy, ocupados):
    """Parede vizinha da porta; se nao houver, a propria porta.

    Mesma escolha do `_tile_da_placa` do master, e na mesma ordem de vizinhos
    (cima, esquerda, direita, baixo), para a placa cair no mesmo lugar que ela
    cairia se o gerador do corte tivesse fechado esta porta.
    """
    try:
        W, H, g = LS.grade(d["layout"])
    except Exception:                                           # noqa: BLE001
        return wx, wy
    for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
        x, y = wx + dx, wy + dy
        if 0 <= x < W and 0 <= y < H and not LS.anda(g[y][x]) \
                and (x, y) not in ocupados:
            return x, y
    return (wx, wy) if (wx, wy) not in ocupados else None


# -------------------------------------------------------------------- o plano
def plano():
    """Devolve (linhas, avisos). Uma linha por porta morta, com o veredito."""
    mu = mundo()
    depara = mu["de_para"]
    const = R.constantes()
    mapas = mapas_todos()
    dentro = ponteiros_de_entrada(mapas, const)
    de_script = warps_de_script(const)
    t = Tiles()
    avisos = []

    mortos = collections.defaultdict(set)
    pend = {}
    for p in mu["pendencias_warp"]:
        m = depara[p["mapa_fonte"]]["nome"]
        mortos[m].add(p["warp"])
        pend[(m, p["warp"])] = p

    linhas = []
    for (m, i), p in sorted(pend.items()):
        d = mapas[m]
        ws = d.get("warp_events") or []
        if i >= len(ws):
            # JA APAGADA numa passada anterior. O `apagada` so acontece em mapa
            # cujos warps sao TODOS porta morta (ver o veredito), entao depois
            # de aplicado o mapa fica com ZERO warps e nenhum indice sobrevive
            # para ser mal endereçado. Sem esta volta, a segunda passada
            # levantaria aviso e o gerador deixaria de ser idempotente.
            if ws:
                avisos.append("%s: warp %d nao existe e o mapa ainda tem %d "
                              "warps: o indice pode ter sido deslocado por "
                              "fora" % (m, i, len(ws)))
                continue
            linhas.append(dict(
                chave="%s/warp/%d" % (p["mapa_fonte"], p["warp"]),
                mapa=m, i=i, x=p.get("x"), y=p.get("y"), auto=False,
                dispara=False, porta=False, entram=[], script=0,
                destino_fonte=p.get("destino_fonte"),
                warp_id_fonte=p.get("warp_id_fonte"),
                motivo_fonte=p.get("motivo", ""),
                veredito="apagada", placa=None, doador=None, volta=None,
                detalhe="ja apagada em passada anterior: o mapa ficou com zero "
                        "warps, modo `apagado` do master"))
            continue
        w = ws[i]
        x, y = w.get("x"), w.get("y")
        # Depois de aplicada, a lapide guarda a celula da PORTA em
        # `porta_original` e o `x`/`y` dela e o do doador. Reler a porta daqui
        # e o que faz a segunda passada medir a mesma coisa que a primeira.
        o = w.get("porta_original")
        if o and len(o) >= 2:
            x, y = o[0], o[1]
        auto = w.get("dest_map") == const.get(m)
        dispara = t.dispara(m, d, x, y)
        entram = dentro.get((m, i), [])
        linha = dict(
            chave="%s/warp/%d" % (p["mapa_fonte"], p["warp"]),
            mapa=m, i=i, x=x, y=y, auto=auto, dispara=dispara,
            porta=t.e_porta(m, d, x, y),
            entram=entram, script=de_script.get((m, i), 0),
            destino_fonte=p.get("destino_fonte"),
            warp_id_fonte=p.get("warp_id_fonte"),
            motivo_fonte=p.get("motivo", ""),
            veredito=None, detalhe="", placa=None, doador=None, volta=None)
        linhas.append(linha)

    # ---- 0. JA APLICADA: o proprio map.json diz o que esta passada fez.
    # Sem esta leitura a segunda passada leria a lapide (que copiou o destino
    # vivo do doador) como "ja viva" e o relatorio mentiria sobre o que ha no
    # disco, mesmo gravando zero. O campo e o mesmo vocabulario do master.
    for l in linhas:
        if l["veredito"]:
            continue
        w = mapas[l["mapa"]]["warp_events"][l["i"]]
        if w.get("religada"):
            l["veredito"] = "religada"
            l["detalhe"] = "ja aplicada: " + w["religada"]
        elif w.get("fechado"):
            o = w.get("porta_original") or []
            mudou = len(o) >= 2 and (o[0], o[1]) != (w.get("x"), w.get("y"))
            l["veredito"] = "lapide" if mudou else "inerte"
            l["detalhe"] = "ja aplicada: " + w["fechado"]

    # ---- 1. ja viva: o warp nao e auto-warp e a volta existe
    for l in linhas:
        if l["auto"] or l["veredito"]:
            continue
        w = mapas[l["mapa"]]["warp_events"][l["i"]]
        inv = {v: k for k, v in const.items()}
        alvo = inv.get(w["dest_map"])
        wid = str(w["dest_warp_id"])
        volta = ""
        if alvo and wid.isdigit():
            aw = (mapas[alvo].get("warp_events") or [])
            if int(wid) < len(aw) and aw[int(wid)].get("dest_map") == const.get(l["mapa"]):
                volta = ", e a volta existe"
        l["veredito"] = "ja_viva"
        l["detalhe"] = ("o warp ja aponta para %s warp %s%s: rodada anterior o "
                        "religou, nao ha o que fechar" % (w["dest_map"], wid, volta))

    # ---- 2. religada: e a SAIDA por onde alguem entra
    for l in linhas:
        if l["veredito"] or not l["dispara"] or not l["entram"]:
            continue
        donos = sorted({o[0] for o in l["entram"]})
        w = (mapas[l["mapa"]].get("warp_events") or [])[l["warp"]] \
            if isinstance(l.get("warp"), int) else {}
        if w.get("dest_map") == "MAP_DYNAMIC":
            # JA RESOLVIDA por retorno dinamico. O motor grava a origem sozinho
            # em `SetupWarp` (src/field_control_avatar.c) quando o warp de
            # DESTINO e `MAP_DYNAMIC`, e devolve o jogador pela porta por onde
            # ele entrou, qualquer que ela seja. O `special` das Battle Tents
            # NAO entra aqui de proposito: a guarda dele repoe o retorno pelo
            # `escapeWarp` sempre que a origem nao e mapa AO AR LIVRE, e as duas
            # origens desta porta (Galar_IsleOfArmor28 e Galar_IsleOfArmor33)
            # sao MAP_TYPE_NONE e MAP_TYPE_INDOOR. Com o special, a porta
            # mandaria para o ultimo ponto de fuga em vez da rua.
            l["veredito"] = "religada"
            l["detalhe"] = ("porta compartilhada resolvida por MAP_DYNAMIC: %d "
                            "mapas entram por este indice (%s) e o motor grava "
                            "a origem de cada entrada"
                            % (len(donos), ", ".join(donos)))
            continue
        if len(donos) > 1:
            # PORTA COMPARTILHADA. Mais de um mapa entra por este mesmo indice,
            # entao nao existe UMA volta certa: devolver para o primeiro da
            # lista seria sortear o destino. Quem resolve isso e o mecanismo de
            # retorno dinamico dos predios compartilhados
            # (`DefinirRetornoPredioCompartilhado`, conserto 1 e 3 da rodada
            # 13), que e SCRIPT e nao `map.json`, ou seja fora do dono deste
            # arquivo. Fica adiada, com o pedido escrito.
            l["veredito"] = "adiada"
            l["detalhe"] = (
                "porta compartilhada: %d mapas entram neste mapa por este "
                "indice (%s). Devolver para um deles sortearia o destino, e a "
                "volta certa e o retorno dinamico de predio compartilhado "
                "(`DefinirRetornoPredioCompartilhado`), que e script"
                % (len(donos), ", ".join(donos)))
            continue
        origem, oi = l["entram"][0]
        l["veredito"] = "religada"
        l["volta"] = (const[origem], oi)
        l["detalhe"] = (
            "%s warp %d entra neste mapa por este indice: fechar prenderia o "
            "jogador dentro e apagar quebraria a entrada, entao a porta passa a "
            "devolver para la (quem entra por uma porta sai por ela)"
            % (origem, oi))

    # ---- 3. lapide / apagada, para o que dispara
    for m in sorted(mortos):
        d = mapas[m]
        ws = d.get("warp_events") or []
        deste = [l for l in linhas if l["mapa"] == m]
        fechar = [l for l in deste if l["dispara"] and not l["veredito"]]
        if not fechar:
            continue
        # Doador: warp que NAO vai ser fechado e cujo tile nao e a porta que
        # estamos fechando. Vivo tem preferencia; porta morta INERTE serve, e o
        # motivo esta no docstring. Indice menor primeiro, como no master.
        fecha_idx = {l["i"] for l in fechar}
        cand = [j for j in range(len(ws)) if j not in fecha_idx]
        for l in fechar:
            menores = [j for j in cand if j < l["i"]]
            doador = (menores[0] if menores else (cand[0] if cand else None))
            if doador is None:
                l["veredito"] = "apagada"
                l["detalhe"] = ("todos os warps deste mapa sao porta morta e "
                                "todos disparam: nao ha doador, e o modo e o "
                                "`apagado` do master")
            else:
                l["veredito"] = "lapide"
                l["doador"] = doador
                dele = {x["i"]: x["veredito"] for x in deste}
                if doador not in dele:
                    qual = "doador vivo"
                elif dele[doador] in ("religada", "ja_viva"):
                    qual = "doador vivo, %s nesta mesma passada" % dele[doador]
                else:
                    qual = "doador inerte, ver o docstring"
                l["detalhe"] = ("lapide na celula do warp %d (%s), molde de "
                                "remove_mapas_cortados.fecha_portas"
                                % (doador, qual))

    # ---- 4. inerte: o que sobrou nao dispara
    for l in linhas:
        if l["veredito"]:
            continue
        l["veredito"] = "inerte"
        l["detalhe"] = ("o tile (%d,%d) nao tem comportamento de porta, escada "
                        "nem seta: o motor nunca chama este warp, e nao ha "
                        "porta desenhada para fechar" % (l["x"], l["y"]))

    # ---- 5. a placa, so onde a porta e desenhada
    ocupa = collections.defaultdict(set)
    for m in sorted(mortos):
        d = mapas[m]
        # As placas que ESTE gerador ja plantou nao contam como celula ocupada:
        # se contassem, a segunda passada acharia a parede tomada e escolheria
        # outra celula, plantando uma placa nova ao lado da que ja existe.
        ocupa[m] = {(b.get("x"), b.get("y")) for b in (d.get("bg_events") or [])
                    if b.get("origem") != ORIGEM_PLACA}
    # UMA PLACA POR PORTA, e nao por celula: celulas vizinhas com o MESMO
    # comportamento sao a MESMA porta desenhada (a seta de saida do FRLG tem
    # tres tiles de largura, a porta de predio tem dois). E a mesma unidade que
    # o `blocos()` da `lente_portas` usa, e sem ela a porta de duas metades
    # ganharia duas placas iguais lado a lado.
    ja_tem = collections.defaultdict(set)
    fechadas = [l for l in linhas
                if l["veredito"] in ("lapide", "apagada") and l["porta"]]
    for l in sorted(fechadas, key=lambda z: (z["mapa"], z["y"], z["x"])):
        c = t.de(l["mapa"], mapas[l["mapa"]])
        meu = c[(l["x"], l["y"])][0]
        vizinha = any((l["x"] + dx, l["y"] + dy) in ja_tem[l["mapa"]]
                      and c.get((l["x"] + dx, l["y"] + dy), (None,))[0] == meu
                      for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)))
        if vizinha:
            l["detalhe"] += (" (a placa e a da celula vizinha: as duas sao a "
                             "mesma porta desenhada)")
            continue
        ja_tem[l["mapa"]].add((l["x"], l["y"]))
        alvo = tile_da_placa(l["mapa"], mapas[l["mapa"]], l["x"], l["y"],
                             ocupa[l["mapa"]])
        if alvo is None:
            avisos.append("%s (%d,%d): sem celula livre para a placa"
                          % (l["mapa"], l["x"], l["y"]))
            continue
        l["placa"] = list(alvo)
        ocupa[l["mapa"]].add(alvo)

    # ---- 6. guarda do modo apagado: indice deslocado nao pode ter dono
    for m in sorted(mortos):
        apaga = sorted(l["i"] for l in linhas
                       if l["mapa"] == m and l["veredito"] == "apagada")
        if not apaga:
            continue
        for j in range(min(apaga), len(mapas[m].get("warp_events") or [])):
            donos = [o for o in dentro.get((m, j), [])]
            if donos or de_script.get((m, j)):
                avisos.append(
                    "%s: apagar o warp %d desloca o indice %d, que tem dono "
                    "(%s%s)" % (m, min(apaga), j, donos,
                                " + %d warp de script" % de_script[(m, j)]
                                if de_script.get((m, j)) else ""))
    return linhas, avisos


# ------------------------------------------------------------------ a gravacao
def aplica(linhas, avisos):
    """Grava. Devolve (mapas_tocados, mudou_algo)."""
    if avisos:
        raise SystemExit("nao gravo com aviso aberto:\n  " + "\n  ".join(avisos))
    const = R.constantes()
    por_mapa = collections.defaultdict(list)
    for l in linhas:
        por_mapa[l["mapa"]].append(l)
    tocados, mudaram = [], []
    for m in sorted(por_mapa):
        # RE-LEITURA no instante de gravar: outras frentes escrevem
        # `object_events` no mesmo arquivo enquanto isto roda.
        p = f"{MAPS}/{m}/map.json"
        d = json.load(open(p, encoding="utf-8"))
        antes = json.dumps([d.get("warp_events"), d.get("bg_events")],
                           sort_keys=True)
        ws = d.get("warp_events") or []
        tinha_bg = "bg_events" in d
        bgs = d.get("bg_events") or []
        for l in sorted(por_mapa[m], key=lambda z: z["i"]):
            if l["i"] >= len(ws):
                continue                    # ja apagada em passada anterior
            w = ws[l["i"]]
            orig = w.get("porta_original") or [l["x"], l["y"],
                                               "fonte %s warp %s"
                                               % (l["destino_fonte"],
                                                  l["warp_id_fonte"])]
            if l["veredito"] == "ja_viva":
                continue
            if w.get("fechado") or w.get("religada"):
                continue                    # ja aplicada, ver a regra 0 do plano
            if l["veredito"] == "religada":
                ws[l["i"]] = dict(w, dest_map=l["volta"][0],
                                  dest_warp_id=str(l["volta"][1]),
                                  religada=l["detalhe"])
                ws[l["i"]].pop("fechado", None)
                ws[l["i"]].pop("porta_original", None)
            elif l["veredito"] == "lapide":
                doa = ws[l["doador"]]
                ws[l["i"]] = dict(w, x=doa["x"], y=doa["y"],
                                  dest_map=doa["dest_map"],
                                  dest_warp_id=doa["dest_warp_id"],
                                  porta_original=orig, fechado=MARCA_FECHADO)
            elif l["veredito"] == "inerte":
                ws[l["i"]] = dict(w, porta_original=orig, fechado=MARCA_FECHADO)
        apaga = {l["i"] for l in por_mapa[m] if l["veredito"] == "apagada"}
        if apaga:
            ws = [w for i, w in enumerate(ws) if i not in apaga]
        for l in por_mapa[m]:
            if not l["placa"]:
                continue
            x, y = l["placa"]
            if any(b.get("x") == x and b.get("y") == y for b in bgs):
                continue
            bgs.append({"type": "sign", "x": x, "y": y, "elevation": 0,
                        "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                        "script": ROTULO, "origem": ORIGEM_PLACA})
        d["warp_events"] = ws
        if tinha_bg or bgs:
            # Chave nova entraria no FIM do dict e o `map.json` sairia fora da
            # ordem canonica; so entra quando ha placa de verdade para gravar.
            d["bg_events"] = bgs
        depois = json.dumps([d.get("warp_events"), d.get("bg_events")],
                            sort_keys=True)
        tocados.append(m)
        if antes != depois:
            mudaram.append(m)
            R.grava_json(p, d)
    escreve_inc()
    return tocados, mudaram


def escreve_inc():
    novo = CORPO_INC
    velho = open(INC, encoding="utf-8").read() if os.path.exists(INC) else None
    if velho != novo:
        open(INC, "w", encoding="utf-8").write(novo)
    t = open(EVENT_SCRIPTS, encoding="utf-8").read()
    if INC_REL in t:
        return
    linha = '\t.include "%s"\n' % INC_REL
    alvo = '\t.include "%s"\n' % DEPOIS_DE
    if alvo not in t:
        raise SystemExit("nao achei %s em data/event_scripts.s" % DEPOIS_DE)
    open(EVENT_SCRIPTS, "w", encoding="utf-8").write(t.replace(alvo, alvo + linha, 1))


MOTIVO = {
    "ja_viva": "porta viva: %s",
    "religada": "religada por dev_scripts/portas_mortas_galar.py: %s",
    "lapide": "fechada por dev_scripts/portas_mortas_galar.py (lapide + placa, "
              "molde das 44 da rodada 13): %s",
    "apagada": "fechada por dev_scripts/portas_mortas_galar.py (warp apagado, "
               "modo `apagado` do master): %s",
    "inerte": "fechada por dev_scripts/portas_mortas_galar.py (marcada inerte, "
              "sem placa): %s",
    "adiada": "adiada por dev_scripts/portas_mortas_galar.py: %s",
}

# `adiada` e o unico veredito que NAO fecha a linha da fila: ela continua
# cobrando, com o motivo escrito. O vocabulario e o do `fila_galar.py`.
STATUS_DA_FILA = {"ja_viva": "feita", "religada": "feita", "lapide": "feita",
                  "apagada": "feita", "inerte": "feita", "adiada": "adiada"}


def grava_fila(linhas):
    """Fecha as linhas `porta_morta` de dev_scripts/fila_galar.json.

    So elas: o arquivo e re-lido aqui e regravado inteiro, e qualquer outro
    tipo passa intocado, porque outras frentes decidem os outros tres tipos.
    """
    doc = json.load(open(FILA, encoding="utf-8"))
    de = {l["chave"]: l for l in linhas}
    n = 0
    for l in doc["linhas"]:
        if l.get("tipo") != "porta_morta" or l["chave"] not in de:
            continue
        p = de[l["chave"]]
        l["status"] = STATUS_DA_FILA[p["veredito"]]
        l["motivo_do_status"] = MOTIVO[p["veredito"]] % p["detalhe"]
        n += 1
    with open(FILA, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
    return n


# ------------------------------------------------------------------ relatorios
def imprime(linhas, avisos, lista=False):
    c = collections.Counter(l["veredito"] for l in linhas)
    print("%d portas mortas em %d mapas"
          % (len(linhas), len({l["mapa"] for l in linhas})))
    print("  disparam: %d   nao disparam: %d"
          % (sum(1 for l in linhas if l["dispara"]),
             sum(1 for l in linhas if not l["dispara"])))
    for k in ("ja_viva", "religada", "lapide", "apagada", "inerte", "adiada"):
        print("  %-10s %4d" % (k, c[k]))
    print("  placas: %d" % sum(1 for l in linhas if l["placa"]))
    if lista:
        for l in sorted(linhas, key=lambda z: (z["mapa"], z["i"])):
            print("  %-26s w%-3d (%3d,%3d) %-9s %s"
                  % (l["mapa"], l["i"], l["x"], l["y"], l["veredito"],
                     l["detalhe"][:90]))
    for a in avisos:
        print("  AVISO " + a)


# ----------------------------------------------------------------------- demo
def demo():
    linhas, avisos = plano()
    f = []

    # 1. as 226 da varredura entram inteiras, e cada uma tem veredito
    if len(linhas) + len(avisos) != len(mundo()["pendencias_warp"]):
        f.append("plano nao cobre as %d pendencias"
                 % len(mundo()["pendencias_warp"]))
    if any(l["veredito"] is None for l in linhas):
        f.append("ha linha sem veredito")

    # 2. o texto e o do master, byte a byte, e nao uma copia nova
    t = open(INC_TEXTO_MASTER, encoding="utf-8").read()
    if f'{ROTULO_TEXTO}:' not in t or f'.string "{TEXTO}$"' not in t:
        f.append("o texto do master mudou: %s / %s nao batem"
                 % (ROTULO_TEXTO, TEXTO))
    if ROTULO_TEXTO not in CORPO_INC:
        f.append("o .inc de Galar nao aponta para o texto do master")

    # 3. quem dispara nao pode ficar inerte, e quem nao dispara nao ganha placa
    if any(l["dispara"] and l["veredito"] == "inerte" for l in linhas):
        f.append("porta que dispara ficou inerte")
    if any(l["placa"] and not l["porta"] for l in linhas):
        f.append("placa em celula que nao e porta")

    # 4. lapide copia o doador do PROPRIO mapa e nao a si mesma
    for l in linhas:
        if l["veredito"] != "lapide" or l["doador"] is None:
            continue
        if l["doador"] == l["i"]:
            f.append("%s: lapide doando para si mesma" % l["mapa"])
        outros = {z["i"] for z in linhas
                  if z["mapa"] == l["mapa"] and z["veredito"] in ("lapide", "apagada")}
        if l["doador"] in outros:
            f.append("%s: doador e outra porta que esta sendo fechada" % l["mapa"])

    # 5. indice de quem tem dono nunca e apagado nem deslocado
    if any("desloca o indice" in a for a in avisos):
        f.append("modo apagado deslocaria indice com dono")

    # 6. religada devolve para quem entra, e nunca para o proprio mapa
    const = R.constantes()
    for l in linhas:
        if l["veredito"] != "religada" or not l["volta"]:
            continue
        if l["volta"][0] == const[l["mapa"]]:
            f.append("%s: religada apontando para o proprio mapa" % l["mapa"])

    # 7. a placa nunca cai em cima de bg_event que ja existe
    for l in linhas:
        if not l["placa"]:
            continue
        d = le(l["mapa"])
        for b in (d.get("bg_events") or []):
            if [b.get("x"), b.get("y")] == l["placa"] \
                    and b.get("origem") != ORIGEM_PLACA:
                f.append("%s: placa em cima de bg_event alheio em %s"
                         % (l["mapa"], l["placa"]))

    # 8. duas placas nunca na mesma celula
    pl = collections.Counter((l["mapa"], tuple(l["placa"])) for l in linhas if l["placa"])
    if any(v > 1 for v in pl.values()):
        f.append("duas placas na mesma celula: %s"
                 % [k for k, v in pl.items() if v > 1][:3])

    # 9. o plano e idempotente: rodar de novo da o mesmo veredito
    outras, _ = plano()
    if [(l["chave"], l["veredito"]) for l in outras] != \
            [(l["chave"], l["veredito"]) for l in linhas]:
        f.append("o plano nao e idempotente")

    print("\n".join("  FALHA " + x for x in f) if f else "demo: OK")
    imprime(linhas, avisos)
    return 1 if f else 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--lista", action="store_true")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--fila", action="store_true",
                   help="fecha as linhas porta_morta de fila_galar.json")
    a = p.parse_args()
    if a.demo:
        raise SystemExit(demo())
    linhas, avisos = plano()
    imprime(linhas, avisos, a.lista)
    if a.aplicar:
        tocados, mudaram = aplica(linhas, avisos)
        print("\n%d mapas no plano, %d gravados" % (len(tocados), len(mudaram)))
        # A lista e dos mapas que o PLANO altera, e nao dos que a ultima
        # passada gravou: na segunda passada nada e gravado e o arquivo ficaria
        # vazio, dizendo que o lote nao tocou em nada.
        altera = sorted({l["mapa"] for l in linhas
                         if l["veredito"] not in ("ja_viva", "adiada")})
        open(f"{RAIZ}/dev_scripts/onda2_lote_g_tocados.txt", "w",
             encoding="utf-8").write("\n".join(altera) + "\n")
    if a.fila:
        print("fila: %d linhas porta_morta fechadas" % grava_fila(linhas))


if __name__ == "__main__":
    main()
