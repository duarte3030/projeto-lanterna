#!/usr/bin/env python3
"""As pedras de Rock Smash de Sinnoh, do pokeplatinum para os nossos map.json.

    python3 dev_scripts/pedras_sinnoh.py            # so mede e grava o censo
    python3 dev_scripts/pedras_sinnoh.py --aplicar  # escreve os map.json
    python3 dev_scripts/pedras_sinnoh.py --demo     # autoteste, nao grava nada

POR QUE ESTE ARQUIVO EXISTE, medido em 18/08/2026
-------------------------------------------------
A onda de povoar mapa vazio de Sinnoh mediu 594 objetos da fonte em 62 mapas
nossos que entraram sem nenhum objeto, e **447 deles sao
`OBJ_EVENT_GFX_ROCK_SMASH`**, quase todos nas salas de pilar da Turnback Cave
(30 por sala) e no Mt Coronet. O buraco de objetos de Sinnoh nao e gente que
falta, e PEDRA que falta.

A decisao 4 do `importa_npcs_sinnoh.py` ("mobiliario nunca vira NPC") continua
valendo e nao e o que este arquivo faz: ela proibe virar BONECO, e pedra de
Rock Smash aqui entra como PEDRA, com o `OBJ_EVENT_GFX_BREAKABLE_ROCK` e o
`EventScript_RockSmash` que o motor ja tem e que a Hoenn de fabrica usa na
Route 111. E fidelidade, nao invencao.

O PORTAO QUE MANDA MAIS QUE A FIDELIDADE: NINGUEM PODE FICAR PRESO
------------------------------------------------------------------
Pedra e obstaculo de verdade, e obstaculo mal posto tranca o jogador. Antes de
gravar qualquer pedra, este script prova por busca em largura (a mesma
`conserta_route222.alcance`, com regra de elevacao) que, **tratando toda pedra
nova como bloqueio e SEM Rock Smash na mochila**, todo alvo do mapa continua
alcancavel a partir do primeiro: os pousos de todos os warps, mais os tiles de
leitura de item. Pedra que desconecta qualquer alvo NAO ENTRA, e vira linha de
censo com o tile e o motivo.

A prova roda nos DOIS estados, porque so o estado bloqueado nao basta:
- com as pedras: todos os alvos conectados (senao o jogador entra e nao sai);
- sem as pedras (o mapa depois de quebrar tudo): idem, e o alcance com pedra e
  subconjunto do alcance sem pedra. Se essa inclusao falhar, a conta esta
  errada, porque tirar bloqueio nunca pode fechar caminho.

A ORDEM IMPORTA e e por isso que a aceitacao e uma a uma: as pedras entram na
ordem da fonte e cada uma so entra se, JUNTO COM AS JA ACEITAS, o mapa continua
conectado. Medir as 30 de uma vez diria "reprovado" e jogaria fora as 29 boas.

A FLAG DE CADA PEDRA
--------------------
`EventScript_RockSmash` termina em `removeobject`, que faz
`FlagSet(GetObjectEventFlagIdByObjectEventId(...))`
(`src/event_object_movement.c:1700`). Duas consequencias medidas:

- **`flag: "0"` e VENENO.** Nao ha guarda de `flagId != 0`: o spawn le
  `!FlagGet(template->flagId)` direto (`src/event_object_movement.c:2893`).
  Quebrar uma pedra de flag 0 acenderia a flag 0 e sumiria com TODO objeto de
  flag 0 do mapa, que e quase todo NPC do jogo.
- **Flag permanente nao e preciso, e por isso esta onda NAO GASTA FAIXA.** A
  faixa `FLAG_TEMP_*` (`TEMP_FLAGS_START` 0x0 a `TEMP_FLAGS_END` 0x1F) e
  zerada na troca de mapa, entao pedra quebrada fica quebrada enquanto o
  jogador esta na sala e volta quando ele sai e entra de novo. E exatamente o
  que a Hoenn de fabrica faz (Route 111 usa `FLAG_TEMP_11`, `_12`, ...), e e o
  comportamento do jogo original.

Isso poe um TETO REAL de pedras por mapa: `TEMPS_LIVRES`. Duas pedras com a
mesma temp somem juntas, entao cada pedra do MESMO mapa precisa da sua. Temp e
por sessao de mapa, entao mapas diferentes reusam as mesmas a vontade. Quem
passar do teto e cortado pela ordem da fonte e vira linha de censo.
"""
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import importa_npcs_sinnoh as I     # noqa: E402  headers, chave, APELIDOS, grade
import arte_ginasios_sinnoh as AG   # noqa: E402  tabela de comportamento do par de tileset
import conserta_route222 as R222    # noqa: E402  a BFS com regra de elevacao

APLICAR = "--aplicar" in sys.argv
CENSO = os.path.join(REPO, "dev_scripts", "pedras_sinnoh_censo.tsv")
MARCA = {"origem": "pokeplatinum-pedra"}
PLAT_EV = os.path.join(I.PLAT, "res/field/events")
SCRIPT = "EventScript_RockSmash"

# Empurrao maximo, em tiles, de um obstaculo que caiu em parede ou em tile
# ocupado. Mesmo numero de bolas_sinnoh.py e do importador de NPC.
RAIO_EMPURRAO = 3
GFX = "OBJ_EVENT_GFX_BREAKABLE_ROCK"

# AS TRES FAMILIAS DE OBSTACULO DE HM, acrescentadas em 22/08/2026 pela decisao
# do Gui "completa ate ficar 100 em tudo". A emenda de 18/08 que abriu a pedra
# vale igual para as outras duas, e pelo mesmo motivo: a decisao 4 do importador
# proibe virar BONECO, nunca proibiu portar o obstaculo COMO OBSTACULO. As tres
# tem mecanica NATIVA neste motor, e nenhuma e invencao:
#
#   fonte                     nosso gfx                       script do motor
#   OBJ_EVENT_GFX_ROCK_SMASH  OBJ_EVENT_GFX_BREAKABLE_ROCK    EventScript_RockSmash
#   OBJ_EVENT_GFX_CUT_TREE    OBJ_EVENT_GFX_CUTTABLE_TREE     EventScript_CutTree
#   ..._STRENGTH_BOULDER      OBJ_EVENT_GFX_PUSHABLE_BOULDER  EventScript_StrengthBoulder
#
# Os tres pares foram LIDOS de mapa que ja esta na ROM (CeladonCity_Frlg para a
# arvore, BurnedTower_B1F para o bloco), nao lembrados. Medido em 22/08/2026 nos
# mapas de ESCOPO: 148 pedras, 36 arvores e 39 blocos da fonte fora, o segundo
# maior bloco do deficit de objetos depois das bolas de item.
#
# O PORTAO E O MESMO PARA AS TRES, e ele e que segura o bloco de Strength: a
# prova por busca em largura trata todo obstaculo novo como bloqueio PERMANENTE
# e sem HM nenhuma na mochila. Bloco que tranca ou que fecha bolso nao entra.
FAMILIAS = (
    ("ROCK_SMASH", GFX, SCRIPT),
    ("CUT_TREE", "OBJ_EVENT_GFX_CUTTABLE_TREE", "EventScript_CutTree"),
    ("STRENGTH_BOULDER", "OBJ_EVENT_GFX_PUSHABLE_BOULDER",
     "EventScript_StrengthBoulder"),
    # SNOWBALL NAO ESTA AQUI, e o motivo esta medido: no ginasio de Snowpoint
    # o chao e MB_ICE, e em gelo o motor entra em movimento forcado antes de
    # `TryPushBoulder`, entao bloco empurravel ali seria parede permanente. A
    # bola de neve e BATENTE de puzzle, nao obstaculo de HM, e mora em
    # `dev_scripts/bolas_neve_sinnoh.py` com a regua do escorregao.
)

# Familias que o jogador EMPURRA em vez de destruir.
#
# Elas passam pelos MESMOS portoes das outras, e isso e de proposito: tratar o
# bloco como parede permanente e MAIS duro do que a realidade (empurrar so
# abre caminho, nunca fecha), entao quem passa no portao estrito esta provado
# com folga. O `resolve_puzzle` existe para a pergunta INVERSA, a do condutor:
# "existe sequencia que leva ate a Candice?". Ele nao roda por mapa no
# `--aplicar` (seria redundante e caro), roda no `--demo`, que e onde a
# afirmacao vive.
EMPURRAVEIS = ("STRENGTH_BOULDER", "SNOWBALL")

# MB_ICE, lido de include/constants/metatile_behaviors.h em 23/08/2026.
MB_ICE = 32

# Temps que este script NAO pode usar, e o motivo de cada uma:
# 0x0  nao e flag, e o "sem flag" de todo objeto (ver o cabecalho).
# 0x7  `P_FLAG_FORCE_SHINY` aponta para ela desde 18/08/2026 (ESTADO 0.f):
#      acende-la faz todo selvagem nascer shiny.
# 0xE  o motor usa para nao criar o Pokemon que segue.
TEMPS_PROIBIDAS = {0x0, 0x7, 0xE}
TEMPS_LIVRES = [f"FLAG_TEMP_{n:X}" for n in range(0x1, 0x20)
                if n not in TEMPS_PROIBIDAS]


# CORTES DO GUI: mapa cujo campo `object_events` saiu do porte nao recebe objeto
# novo. Nao e regua (a regua ja o desconta), e ROM: escrever pedra dentro das 18
# salas de pilar da Turnback Cave custaria bytes num mapa que outro executor
# esta REMOVENDO da ROM. A lista e a mesma que mede, `completude.CORTES_DO_GUI`.
def _cortados(_c={}):
    if not _c:
        import completude as _CP
        _rx, defi = _CP.cortes_da_regiao("Sinnoh")
        _c["s"] = {m for m, campos in defi.items() if "object_events" in campos}
    return _c["s"]


def andavel(v):
    return ((v >> 10) & 3) == 0


def diagnostico_de_parede(W, H, g, base, x, y):
    """Por que a pedra da fonte cai em parede, MEDIDO, e não "dívida de geometria".

    ATÉ 21/08/2026 este caso virava a linha de censo "tile nao e andavel: pedra
    invisivel dentro de parede", e o ESTADO 0.g leu isso como dívida da nossa
    conversão ("a conversão do Platinum marca o tile da pedra como bloqueado").
    A medição da onda das pedras derrubou essa leitura, com número:

    - **A conversão não corrompeu geometria nenhuma.** O nosso `map.bin` é BYTE
      A BYTE o do demake 2D em `fontes-mapas/sinnoh` nos três mapas que
      concentram 8 das 31 pedras (OreburghGate_1F, MtCoronet_1F_South,
      MtCoronet_B1F); em RavagedPath, que tem as outras 23, há UM tile de
      diferença no mapa inteiro, em (26,1), que é a boca de caverna aberta de
      propósito por `abre_bocas_cavernas_sinnoh.py` e fica a 20 tiles da pedra
      mais próxima. Não há o que consertar no conversor de blockdata: ele não
      mexeu em nenhum desses tiles.
    - **A parede é do DEMAKE, não nossa.** Quem desenhou Sinnoh em 2D não
      desenhou nem a pedra de Rock Smash nem a passagem atrás dela: pôs rocha
      maciça. 29 das 31 pedras caem em tile com ZERO vizinho ALCANÇÁVEL, ou
      seja num bloco de parede em que o jogador nunca encosta. Abrir esses
      tiles não restaura passagem nenhuma: fura buraco para dentro de rocha e
      obriga a inventar o corredor do outro lado, que é desenho de fase e
      decisão do Gui, não conversão.
    - **Deslocamento não explica.** Varredura de todos os (dx,dz) de -20 a 20:
      o melhor deslocamento põe 18 das 27 pedras de RavagedPath em tile andável
      contra 4 da identidade, mas casa ZERO warp; e os warps provam que não há
      translação única (os (19,50) e (28,44) da fonte são os nossos (19,40) e
      (28,35), dz 10 e 9). O demake REDESENHOU o mapa, não transladou.

    Devolve o motivo escrito, com o número que o sustenta, para o censo parar de
    acusar o conversor por um buraco que é da fonte.
    """
    viz = [(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
           if 0 <= x + dx < W and 0 <= y + dy < H]
    alcanc = sum(1 for t in viz if t in base)
    if alcanc == 0:
        return ("parede maciça do demake: ZERO vizinho alcançável, a fonte 2D "
                "não desenhou nem a pedra nem a passagem atrás dela")
    gg = [linha[:] for linha in g]
    gg[y][x] &= ~(3 << 10)
    ganho = len(R222.alcance(W, H, gg, sorted(base))) - len(base)
    return (f"saliência de parede do demake: {alcanc} vizinho(s) alcançável(is)"
            f", e abrir o tile ganharia só {ganho} tile(s)")


def pousos(W, H, g, mapa):
    """Tiles que o mapa PRECISA manter ligados: pouso de cada warp e leitura de
    cada item. Se dois deles deixarem de se alcancar, uma pedra prendeu alguem.
    """
    alvos = []
    fontes = [(w["x"], w["y"]) for w in (mapa.get("warp_events") or [])]
    fontes += [(o["x"], o["y"]) for o in (mapa.get("object_events") or [])
               if "FindItem" in str(o.get("script", ""))]
    fontes += [(b["x"], b["y"]) for b in (mapa.get("bg_events") or [])
               if b.get("type", "").startswith("hidden_item")]
    for x, y in fontes:
        if not (0 <= x < W and 0 <= y < H):
            continue
        if andavel(g[y][x]):
            alvos.append((x, y))
            continue
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and andavel(g[ny][nx]):
                alvos.append((nx, ny))
                break
    return sorted(set(alvos))


def conectado(W, H, g, alvos, bloqueados):
    """True se, com `bloqueados` fechados, todo alvo alcanca o primeiro alvo.

    `alvos` tem que ser a LINHA DE BASE do mapa (o que ja se alcancava com zero
    pedra), nunca a lista crua. Medido em 18/08/2026: `MtCoronet4FRooms1And2` e
    `MtCoronet_1F_South` ja nascem com warp fora do alcance a pe (a fonte pede
    Surf ou Strength ali, e a nossa BFS nao modela nenhum dos dois). Cobrar
    conectividade ABSOLUTA nesses mapas reprova TODA pedra por um defeito que
    nao e da pedra. A pergunta certa e "esta pedra tirou alguma coisa que
    existia?", nao "este mapa e perfeito?".
    """
    if len(alvos) < 2:
        return True
    gg = [linha[:] for linha in g]
    for x, y in bloqueados:
        gg[y][x] |= 1 << 10
    vistos = R222.alcance(W, H, gg, [alvos[0]])
    return all(a in vistos for a in alvos[1:])


def sem_bolso(W, H, g, saidas, base_andavel, bloqueados):
    """NINGUEM FICA PRESO: todo tile que dava para pisar antes das pedras ainda
    chega a alguma saida depois delas.

    O portao de pares de alvo acima nao basta e a medicao mostrou por que: em
    `WaywardCave1F` e `MtCoronet4FRooms1And2` a linha de base liga UM alvo so
    (os outros warps ja nascem fora do alcance a pe, defeito anterior e nao
    desta onda), e com um alvo so o portao de pares nao tem dente nenhum. Este
    aqui tem: pedra que fecha um bolso sem saida reprova mesmo num mapa de um
    warp. Bolso QUE JA EXISTIA nao conta, porque a regua e `base_andavel`.
    """
    gg = [linha[:] for linha in g]
    for x, y in bloqueados:
        gg[y][x] |= 1 << 10
    salvos = R222.alcance(W, H, gg, saidas)
    return all(t in salvos for t in base_andavel if t not in bloqueados)


def linha_de_base(W, H, g, mapa):
    """Os alvos que o mapa JA liga com zero pedra. E a regua do portao."""
    alvos = pousos(W, H, g, mapa)
    if len(alvos) < 2:
        return alvos, 0
    base = R222.alcance(W, H, g, [alvos[0]])
    ligados = [alvos[0]] + [a for a in alvos[1:] if a in base]
    return ligados, len(alvos) - len(ligados)


def familia_de(e):
    """(gfx nosso, script) do obstaculo da fonte, ou None se nao for um."""
    g = e.get("graphics_id", "")
    for chave, gfx, script in FAMILIAS:
        if chave in g:
            return gfx, script
    return None


def pedras_da_fonte(fonte):
    return [e for e in fonte.get("object_events", [])
            if familia_de(e) is not None]


def main():
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    heads = I.headers_do_platinum()
    por_chave = {}
    for h, (ev, mx) in heads.items():
        por_chave.setdefault(I.chave(h), (h, ev, mx))

    censo = [("mapa", "x_fonte", "z_fonte", "x_nosso", "y_nosso", "flag",
              "regra", "motivo")]
    stats = {"pedras": 0, "mapas": 0, "ja_importado": 0, "fora_tranca": 0,
             "fora_tile": 0, "fora_ocupado": 0, "fora_teto_temp": 0,
             "fora_planta_provisoria": 0, "fora_escala_nao_provada": 0,
             "fora_teto_64": 0, "alvos_ja_soltos": 0, "fora_bolso": 0}
    pico = (0, "")
    # O censo tem que sobreviver a idempotencia: a segunda rodada pula o mapa ja
    # escrito, e sem isto apagaria a linha que diz onde cada pedra entrou.
    antigo = {}
    if os.path.exists(CENSO):
        for l in open(CENSO, encoding="utf-8"):
            c = tuple(l.rstrip("\n").split("\t"))
            if len(c) == len(censo[0]) and c[0] != "mapa":
                antigo.setdefault(c[0], []).append(c)

    for meu in I.mapas_editaveis_sinnoh():
        if meu in _cortados():
            continue
        h = I.APELIDOS.get(meu)
        alvo = (h,) + heads[h] if h in heads else por_chave.get(I.chave(meu))
        if not alvo:
            continue
        header, arq_ev, matriz = alvo
        pe = os.path.join(I.PLAT, "res/field/events", arq_ev + ".json")
        if not os.path.exists(pe):
            continue
        fonte = json.load(open(pe))
        cruas = pedras_da_fonte(fonte)
        if not cruas:
            continue

        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        d = json.load(open(pm))
        objs = d.get("object_events") or []
        # IDEMPOTENCIA POR PEDRA, e nao por mapa (22/08/2026).
        #
        # Ate aqui, mapa que ja tivesse UMA pedra da marca era pulado INTEIRO, e
        # com ele iam embora todas as pedras que passaram a caber depois. Foi o
        # que segurou os quatro mapas do corredor: `corredores_sinnoh.py` abriu
        # 63 tiles de parede em RavagedPath, OreburghGate_1F, MtCoronet_1F_South
        # e MtCoronet_B1F, e a rodada seguinte respondia "ja importado" e escrevia
        # ZERO. Idempotencia de mapa mede a rodada, e o que interessa medir e a
        # PEDRA: a que ja esta la cai em "tile ja ocupado" no laco normal, que e
        # a mesma guarda, so que por evento.
        #
        # As pedras que JA estao no mapa entram em `aceitas` antes do laco, senao
        # a prova de conectividade julgaria as novas num mapa em que as velhas
        # nao bloqueiam nada, e a FLAG_TEMP delas sai da lista de livres, senao
        # duas pedras do mesmo mapa dividiriam a flag e sumiriam juntas.
        ja_pedras = [(o["x"], o["y"]) for o in objs
                     if o.get("origem") == "pokeplatinum-pedra"]
        usadas = {o.get("flag") for o in objs}
        livres = [f for f in TEMPS_LIVRES if f not in usadas]
        if I.planta_provisoria(layouts, d["layout"]):
            stats["fora_planta_provisoria"] += len(cruas)
            for e in cruas:
                censo.append((meu, e["x"], e["z"], "", "", "", "-",
                              f"planta provisoria: {d['layout']} e o molde de "
                              "portao 13x9"))
            continue

        L = layouts[d["layout"]]
        conv = I.conversor_de_coordenada(fonte, L["width"], L["height"],
                                         header, matriz, d, vazio=True)
        if conv is None:
            continue
        regra = getattr(conv, "regra", "?")
        # A ESCALA FOI REABERTA em 22/08/2026, com a mesma medida que reabriu a
        # do `importa_npcs_sinnoh.py`: o defeito que fechou o portao (evento
        # dentro de parede, na Route 222) e hoje PEGO pelos portoes que rodam
        # depois dela, e aqui eles sao os mais duros da casa. Obstaculo so entra
        # se o tile for andavel, se ninguem ficar preso (`conectado`) e se
        # nenhum bolso nascer (`sem_bolso`), tudo com a HM fora da mochila. Ou
        # seja: a escala escolhe a regiao e a busca em largura decide. Medido no
        # dia: 70 obstaculos de mapa em ESCOPO estavam parados so por este
        # portao. A regra continua escrita no censo, linha a linha.
        if regra.startswith("escala"):
            regra += " + portao de conectividade (22/08/2026)"

        W, H, g = I.grade(layouts, d["layout"])
        _beh = AG.comportamento(L["primary_tileset"], L["secondary_tileset"])
        tem_gelo = any(_beh(g[yy][xx] & 0x3FF) == MB_ICE
                       for yy in range(H) for xx in range(W)
                       if andavel(g[yy][xx]))
        alvos, soltos = linha_de_base(W, H, g, d)
        if soltos:
            stats["alvos_ja_soltos"] += soltos
        saidas = pousos(W, H, g, {"warp_events": d.get("warp_events") or []})
        base_andavel = R222.alcance(W, H, g, saidas)
        ocupados = {(o["x"], o["y"]) for o in objs}
        ocupados |= {(w["x"], w["y"]) for w in (d.get("warp_events") or [])}
        aceitas, novas = list(ja_pedras), []
        teto = len(ja_pedras) + min(len(livres), 64 - len(objs))
        # IDEMPOTENCIA COM EMPURRAO: a pedra que JA ESTA no mapa tem que ser
        # reconhecida ANTES do empurrao, e nao depois.
        #
        # Ate o empurrao entrar (22/08/2026), a guarda era "tile ja ocupado":
        # a pedra da rodada anterior ocupava o tile da fonte e a nova era
        # recusada. Com empurrao isso VIRA DEFEITO, e ele foi medido no mesmo
        # dia: o tile estava ocupado, o empurrao achava o vizinho livre e
        # gravava uma SEGUNDA pedra ao lado; seis rodadas seguidas somaram 235
        # copias e a coluna `objetos` de Sinnoh passou de 100% por duplicata.
        # A guarda agora e a mesma do `reclama` do importador de NPC: pedra
        # nossa da MESMA familia a <= RAIO_EMPURRAO da coordenada da fonte
        # RECLAMA aquela pedra da fonte, uma vez so (`reclamadas`), e a fonte
        # segue em frente.
        marcadas = [o for o in objs if o.get("origem") == MARCA["origem"]]
        reclamadas = set()

        def ja_esta(x0, y0, gfx):
            for o in marcadas:
                if id(o) in reclamadas or o.get("graphics_id") != gfx:
                    continue
                if max(abs(o["x"] - x0), abs(o["y"] - y0)) <= RAIO_EMPURRAO:
                    reclamadas.add(id(o))
                    return True
            return False

        for e in cruas:
            x0, y0 = conv(e)
            if ja_esta(x0, y0, familia_de(e)[0]):
                stats["ja_importado"] += 1
                for c in antigo.get(meu, []):
                    if (str(c[1]), str(c[2])) == (str(e["x"]), str(e["z"])):
                        censo.append(c)
                        break
                continue
            # EMPURRAO DE ATE 3 TILES, 22/08/2026, a pedido do Gui ("reposicione
            # a <= 3 tiles o resto"). Antes daqui o obstaculo cujo tile caia em
            # parede ou em cima de outro objeto era simplesmente recusado, e
            # medido no censo do dia isso sozinho custava 93 obstaculos em
            # "tile ja ocupado" e 36 em "parede macica". O raio e o MESMO de
            # `bolas_sinnoh.py` e do importador de NPC, no mesmo mapa e na mesma
            # grade. O que continua mandando sao os portoes DEPOIS: o tile de
            # destino tem que ser andavel, livre, ALCANCAVEL a pe (esta em
            # `base_andavel`) e passar por `conectado` e `sem_bolso`. Empurrar
            # nunca afrouxa a prova de que ninguem fica preso.
            pos = next(((x0 + dx, y0 + dy) for r in range(RAIO_EMPURRAO + 1)
                        for dx in range(-r, r + 1) for dy in range(-r, r + 1)
                        if max(abs(dx), abs(dy)) == r
                        and 0 <= x0 + dx < W and 0 <= y0 + dy < H
                        and andavel(g[y0 + dy][x0 + dx])
                        and (x0 + dx, y0 + dy) not in ocupados
                        and (x0 + dx, y0 + dy) in base_andavel), None)
            if pos is None:
                if not (0 <= x0 < W and 0 <= y0 < H) or not andavel(g[y0][x0]):
                    stats["fora_tile"] += 1
                    censo.append((meu, e["x"], e["z"], x0, y0, "", regra,
                                  diagnostico_de_parede(W, H, g, base_andavel,
                                                        x0, y0)))
                else:
                    stats["fora_ocupado"] += 1
                    censo.append((meu, e["x"], e["z"], x0, y0, "", regra,
                                  "tile ja ocupado por objeto ou warp, e nao ha "
                                  f"tile livre alcancavel a ate {RAIO_EMPURRAO}"))
                continue
            x, y = pos
            passos = max(abs(x - x0), abs(y - y0))
            # BLOCO EMPURRAVEL NAO ENTRA EM PISO DE GELO. Medido em
            # 23/08/2026, e a medida derruba a hipotese com que este bloco foi
            # pedido: no ginasio de Snowpoint o chao e MB_ICE (comportamento
            # 32), e em tile de gelo o motor entra em MOVIMENTO FORCADO
            # (`sForcedMovementFuncs` / `MetatileBehavior_IsIce_2`,
            # src/field_player_avatar.c:164) ANTES de chegar em
            # `TryPushBoulder` (:1031). Ou seja: com FLAG_SYS_USE_STRENGTH
            # acesa a mao e o jogador encostado no bloco, o empurrao NAO
            # acontece; o bloco vira parede permanente no meio do escorregao.
            # Isso e fiel ao gen 4 (la a bola de neve e o BATENTE do puzzle de
            # gelo, nao um bloco de Strength), so que aqui ele custaria caro: as
            # 19 bolas caem na coluna 11, que e o corredor de gelo pelo qual as
            # provas do T115 e do T125 chegam na Candice e na Alicia. Enquanto
            # nao houver batente de gelo de verdade neste motor, o obstaculo
            # empurravel fica de fora do gelo, e o balde continua medido.
            # A regra e POR MAPA e nao por tile, e o motivo esta na medida: o
            # que derrota o empurrao e o ESCORREGAO, e quem escorrega e o
            # jogador, em qualquer lugar da sala de gelo. Pela regra por tile,
            # a bola de (11,16) sobrevivia (aquele tile e
            # MB_IMPASSABLE_WEST_AND_EAST, marcador do labirinto) e tapava
            # justamente a coluna 11, o corredor das provas do T115 e do T125.
            if any(k in (e.get("graphics_id", "") or "") for k in EMPURRAVEIS) \
                    and tem_gelo:
                stats["fora_gelo"] = stats.get("fora_gelo", 0) + 1
                censo.append((meu, e["x"], e["z"], x, y, "", regra,
                              "piso de GELO: o motor entra em movimento forcado "
                              "antes de TryPushBoulder, entao bloco empurravel "
                              "aqui e parede permanente"))
                continue
            # OBSTACULO EMPURRADO NAO ENTRA EM CORREDOR, 23/08/2026.
            #
            # `conectado` e `sem_bolso` provam que ninguem fica PRESO, e isso
            # continua valendo; nenhum dos dois, porem, impede que a pedra
            # empurrada TAMPE um corredor de um tile de largura e mande o
            # jogador dar a volta. Medido no dia: uma pedra do RavagedPath
            # andou 1 tile e caiu em (18,39), que e a boca do tunel que o
            # `corredores_sinnoh.py` abriu de proposito na rodada 7 para
            # desilhar 133 tiles; o mapa continuava conexo (o gerador de
            # corredor segue dizendo "0 ilhados"), mas as rotas do T148.5, .6 e
            # .7 passavam a dar a volta e os tres reprovavam. Tile de corredor
            # tem no maximo DOIS vizinhos andaveis; tile de salao tem tres ou
            # quatro. O empurrao passa a exigir tres, ou seja: a pedra
            # empurrada cai onde ha espaco, e onde a fonte MANDOU (passos == 0)
            # ela entra do mesmo jeito, porque ali o estreito e intencao do
            # jogo original e nao arredondamento nosso.
            #
            # A BOCA DO MAPA tem a mesma regra e o mesmo motivo: todo roteiro de
            # teste comeca no pouso de um warp, entao obstaculo empurrado a tres
            # tiles ou menos de um warp e o que mais quebra rota ja provada. No
            # RavagedPath uma pedra andou 1 tile e caiu em (18,39), a dois tiles
            # do warp 0: o mapa continuava conexo e mesmo assim os T148.5, .6 e
            # .7 reprovavam, porque as pernas saturantes deles passavam a bater
            # nela. Onde a FONTE manda (passos == 0) a pedra entra na boca sem
            # discussao, que e o jogo original.
            if passos:
                viz = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                          if 0 <= x + dx < W and 0 <= y + dy < H
                          and andavel(g[y + dy][x + dx]))
                if (x, y) in I.corredor_de_gatilho(d, layouts):
                    stats["fora_gatilho"] = stats.get("fora_gatilho", 0) + 1
                    censo.append((meu, e["x"], e["z"], x, y, "", regra,
                                  "empurrada para o corredor de aproximacao de "
                                  "um coord_event: obstaculo empurrado nao "
                                  "tranca gatilho"))
                    continue
                perto = min((max(abs(x - w["x"]), abs(y - w["y"]))
                             for w in (d.get("warp_events") or [])), default=99)
                if perto <= 3:
                    stats["fora_boca"] = stats.get("fora_boca", 0) + 1
                    censo.append((meu, e["x"], e["z"], x, y, "", regra,
                                  f"empurrada para {perto} tile(s) de um warp: "
                                  "obstaculo empurrado nao nasce na boca do mapa"))
                    continue
                if viz < 3:
                    stats["fora_corredor"] = stats.get("fora_corredor", 0) + 1
                    censo.append((meu, e["x"], e["z"], x, y, "", regra,
                                  f"empurrada para corredor de {viz} vizinho(s): "
                                  "obstaculo empurrado nao tampa passagem"))
                    continue
            if len(aceitas) >= teto:
                stats["fora_teto_temp" if len(livres) <= 64 - len(objs)
                      else "fora_teto_64"] += 1
                censo.append((meu, e["x"], e["z"], x, y, "", regra,
                              f"teto de {teto} pedras neste mapa (FLAG_TEMP "
                              "livres / 64 templates), corte pela ordem da fonte"))
                continue
            if not conectado(W, H, g, alvos, aceitas + [(x, y)]):
                stats["fora_tranca"] += 1
                censo.append((meu, e["x"], e["z"], x, y, "", regra,
                              "TRANCA: com esta pedra um warp ou item do mapa "
                              "deixa de ser alcancavel sem Rock Smash"))
                continue
            if not sem_bolso(W, H, g, saidas, base_andavel,
                             aceitas + [(x, y)]):
                stats["fora_bolso"] += 1
                censo.append((meu, e["x"], e["z"], x, y, "", regra,
                              "BOLSO: com esta pedra sobra tile pisavel de onde "
                              "nao se chega a nenhum warp, sem Rock Smash"))
                continue
            ocupados.add((x, y))
            flag = livres[len(novas)]
            aceitas.append((x, y))
            censo.append((meu, e["x"], e["z"], x, y, flag, regra,
                          "" if not passos else f"empurrado {passos} tile(s)"))
            elev = (g[y][x] >> 12) & 0xF
            novas.append({
                "graphics_id": familia_de(e)[0], "x": x, "y": y,
                "elevation": elev if elev else 3,
                "movement_type": "MOVEMENT_TYPE_LOOK_AROUND",
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": familia_de(e)[1], "flag": flag, **MARCA,
            })
        if not novas:
            continue
        # A prova do outro estado: o mapa com TODAS as pedras quebradas continua
        # conectado, e o alcance com pedra cabe dentro do alcance sem pedra.
        # o OUTRO estado, o mapa com tudo quebrado: continua conectado e o
        # alcance com pedra cabe dentro do alcance sem pedra.
        assert conectado(W, H, g, alvos, []), meu
        assert sem_bolso(W, H, g, saidas, base_andavel, []), meu
        assert R222.alcance(W, H, [[(v | (1 << 10)) if (x, y) in set(aceitas)
                                    else v for x, v in enumerate(linha)]
                                   for y, linha in enumerate(g)],
                            saidas) <= base_andavel, meu
        stats["pedras"] += len(novas)
        stats["mapas"] += 1
        pico = max(pico, (len(novas), meu))
        d["object_events"] = objs + novas   # append: a save guarda indice
        if APLICAR:
            json.dump(d, open(pm, "w"), indent=2, ensure_ascii=False)

    with open(CENSO, "w", encoding="utf-8") as f:
        for l in censo:
            f.write("\t".join(str(c) for c in l) + "\n")
    print(f"censo: {len(censo) - 1} linhas em {os.path.relpath(CENSO, REPO)}")
    print("resumo:", stats)
    print(f"temps livres por mapa: {len(TEMPS_LIVRES)}   "
          f"pico de pedras num mapa: {pico[0]} ({pico[1]})")
    print("\naplicado" if APLICAR else "\nnada escrito (use --aplicar)")
    return 0


def demo():
    """Mutacao plantada: uma pedra no gargalo TEM que ser reprovada."""
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}

    # 1. nenhuma temp perigosa entra na lista de trabalho
    assert "FLAG_TEMP_7" not in TEMPS_LIVRES   # P_FLAG_FORCE_SHINY
    assert "FLAG_TEMP_E" not in TEMPS_LIVRES   # follower
    assert len(TEMPS_LIVRES) == len(set(TEMPS_LIVRES)) == 0x1F - len(TEMPS_PROIBIDAS) + 1

    # 2. MUTACAO PLANTADA, num mapa de verdade: SolaceonRuinsRoom1NorthwestDeadEnd
    #    e um beco de 3x3 com UM warp em (5,3). Ponho um alvo falso do outro
    #    lado do unico corredor e emparedo o corredor com uma "pedra": a conta
    #    TEM que dizer desconectado. Sem esta prova o portao seria enfeite, e o
    #    enfeite tranca jogador.
    d = json.load(open(os.path.join(
        REPO, "data/maps/SolaceonRuinsRoom1NorthwestDeadEnd/map.json")))
    W, H, g = I.grade(layouts, d["layout"])
    # o beco: linhas 2 a 4, colunas 2 a 5, com (3,3) de parede no meio
    assert andavel(g[3][4]) and andavel(g[3][5]) and not andavel(g[3][3])
    alvos = [(5, 3), (2, 2)]
    assert conectado(W, H, g, alvos, [])           # sem pedra, conectado
    # (4,3) e (4,2) e (4,4) sao a garganta inteira entre (5,3) e (2,2)
    assert not conectado(W, H, g, alvos, [(4, 2), (4, 3), (4, 4)])
    # e UMA pedra no meio da garganta nao tranca, porque sobra volta por cima
    assert conectado(W, H, g, alvos, [(4, 3)])

    # 2b. MUTACAO PLANTADA que TRANCA, e o portao tem que reprovar: com o unico
    #     warp em (5,3), a coluna 4 e a garganta inteira, porque (3,3) ja e
    #     parede. Uma pedra em (4,2) MAIS uma em (4,4) fecham (2,2), (3,2),
    #     (2,3), (2,4) e (3,4) num bolso sem saida: quem entrasse la nao sairia
    #     mais. E por isto que o portao existe, e por isto que ele reprova.
    saidas = [(5, 3)]
    base = R222.alcance(W, H, g, saidas)
    assert sem_bolso(W, H, g, saidas, base, [])                  # sem pedra, ok
    assert sem_bolso(W, H, g, saidas, base, [(4, 3)])            # uma so, ok
    assert sem_bolso(W, H, g, saidas, base, [(4, 2)])            # a volta cobre
    assert not sem_bolso(W, H, g, saidas, base, [(4, 2), (4, 4)])
    assert not sem_bolso(W, H, g, saidas, base, [(4, 2), (4, 3), (4, 4)])

    # 3. o outro estado: tirar bloqueio NUNCA fecha caminho.
    gg = [l[:] for l in g]
    com = R222.alcance(W, H, [[(v | (1 << 10)) if (x, y) == (4, 3) else v
                               for x, v in enumerate(linha)]
                              for y, linha in enumerate(gg)], [(5, 3)])
    sem = R222.alcance(W, H, gg, [(5, 3)])
    assert com <= sem and com != sem

    # 4. MUTACAO PLANTADA no diagnostico de parede, em RavagedPath, que e o
    #    mapa das 23 pedras. Sem esta prova o motivo do censo voltaria a ser
    #    texto de fe, e foi texto de fe que fez o ESTADO culpar o conversor.
    dr = json.load(open(os.path.join(REPO, "data/maps/RavagedPath/map.json")))
    W, H, g = I.grade(layouts, dr["layout"])
    saidas = pousos(W, H, g, {"warp_events": dr.get("warp_events") or []})
    base = R222.alcance(W, H, g, saidas)
    # (7,37) e uma das 23: parede com ZERO vizinho alcancavel
    assert not andavel(g[37][7])
    assert "parede maciça" in diagnostico_de_parede(W, H, g, base, 7, 37)
    # A ARMADILHA que separa "andavel" de "alcancavel" continua sendo provada,
    # so que noutro tile, e a troca e MEDICAO e nao conserto de teste:
    # `corredores_sinnoh.py` ligou em 22/08/2026 os 133 tiles de TERRA ilhados
    # de RavagedPath, e com eles (11,12) passou a ser alcancavel, ou seja o
    # (12,12) desta prova virou saliencia de verdade. O que NAO foi ligado, de
    # proposito, sao os 124 tiles de elevacao 1 (agua de Surf): cavar corredor
    # de pedra por dentro do lago o secaria. (25,4) e parede cujo unico vizinho
    # andavel e agua, e por isso ainda separa as duas reguas.
    assert not andavel(g[4][25])
    assert any(andavel(g[b][a]) and (a, b) not in base
               for a, b in ((25, 3), (25, 5), (24, 4), (26, 4)))
    assert "parede maciça" in diagnostico_de_parede(W, H, g, base, 25, 4)
    # e o (12,12), que ANTES do corredor era parede maciça, agora responde
    # saliencia: a mesma funcao, a mesma pergunta, o mapa e que mudou.
    assert andavel(g[12][11]) and (11, 12) in base
    assert "saliência" in diagnostico_de_parede(W, H, g, base, 12, 12)
    # MUTACAO PLANTADA do outro lado: MtCoronet_B1F (28,14) e a unica familia
    # que sobra, saliencia de verdade, com vizinho ALCANCAVEL. Se o diagnostico
    # colapsar num rotulo so, este assert cai.
    dm = json.load(open(os.path.join(REPO, "data/maps/MtCoronet_B1F/map.json")))
    Wm, Hm, gm = I.grade(layouts, dm["layout"])
    bm = R222.alcance(Wm, Hm, gm,
                      pousos(Wm, Hm, gm,
                             {"warp_events": dm.get("warp_events") or []}))
    assert not andavel(gm[14][28])
    assert "saliência" in diagnostico_de_parede(Wm, Hm, gm, bm, 28, 14)

    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
