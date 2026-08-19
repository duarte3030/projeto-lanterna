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
import conserta_route222 as R222    # noqa: E402  a BFS com regra de elevacao

APLICAR = "--aplicar" in sys.argv
CENSO = os.path.join(REPO, "dev_scripts", "pedras_sinnoh_censo.tsv")
MARCA = {"origem": "pokeplatinum-pedra"}
SCRIPT = "EventScript_RockSmash"
GFX = "OBJ_EVENT_GFX_BREAKABLE_ROCK"

# Temps que este script NAO pode usar, e o motivo de cada uma:
# 0x0  nao e flag, e o "sem flag" de todo objeto (ver o cabecalho).
# 0x7  `P_FLAG_FORCE_SHINY` aponta para ela desde 18/08/2026 (ESTADO 0.f):
#      acende-la faz todo selvagem nascer shiny.
# 0xE  o motor usa para nao criar o Pokemon que segue.
TEMPS_PROIBIDAS = {0x0, 0x7, 0xE}
TEMPS_LIVRES = [f"FLAG_TEMP_{n:X}" for n in range(0x1, 0x20)
                if n not in TEMPS_PROIBIDAS]


def andavel(v):
    return ((v >> 10) & 3) == 0


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


def pedras_da_fonte(fonte):
    return [e for e in fonte.get("object_events", [])
            if "ROCK_SMASH" in e.get("graphics_id", "")]


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
        if any(o.get("origem") == "pokeplatinum-pedra" for o in objs):
            stats["ja_importado"] += 1
            censo.extend(antigo.get(meu) or [(
                meu, "", "", "", "", "", "-",
                "ja importado em rodada anterior (ver a marca no map.json)")])
            continue
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
        if regra.startswith("escala"):
            stats["fora_escala_nao_provada"] += len(cruas)
            for e in cruas:
                censo.append((meu, e["x"], e["z"], "", "", "", regra,
                              "regra de coordenada nao provada (escala)"))
            continue

        W, H, g = I.grade(layouts, d["layout"])
        alvos, soltos = linha_de_base(W, H, g, d)
        if soltos:
            stats["alvos_ja_soltos"] += soltos
        saidas = pousos(W, H, g, {"warp_events": d.get("warp_events") or []})
        base_andavel = R222.alcance(W, H, g, saidas)
        ocupados = {(o["x"], o["y"]) for o in objs}
        ocupados |= {(w["x"], w["y"]) for w in (d.get("warp_events") or [])}
        aceitas, novas = [], []
        teto = min(len(TEMPS_LIVRES), 64 - len(objs))
        for e in cruas:
            x, y = conv(e)
            if not andavel(g[y][x]):
                stats["fora_tile"] += 1
                censo.append((meu, e["x"], e["z"], x, y, "", regra,
                              "tile nao e andavel: pedra invisivel dentro de "
                              "parede"))
                continue
            if (x, y) in ocupados:
                stats["fora_ocupado"] += 1
                censo.append((meu, e["x"], e["z"], x, y, "", regra,
                              "tile ja ocupado por objeto ou warp"))
                continue
            if len(aceitas) >= teto:
                stats["fora_teto_temp" if len(TEMPS_LIVRES) <= 64 - len(objs)
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
            aceitas.append((x, y))
            ocupados.add((x, y))
            flag = TEMPS_LIVRES[len(aceitas) - 1]
            censo.append((meu, e["x"], e["z"], x, y, flag, regra, ""))
            elev = (g[y][x] >> 12) & 0xF
            novas.append({
                "graphics_id": GFX, "x": x, "y": y,
                "elevation": elev if elev else 3,
                "movement_type": "MOVEMENT_TYPE_LOOK_AROUND",
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": SCRIPT, "flag": flag, **MARCA,
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

    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
