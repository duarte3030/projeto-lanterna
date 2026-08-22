#!/usr/bin/env python3
"""As bolas de item VISÍVEIS de Sinnoh, do pokeplatinum para os nossos map.json.

    python3 dev_scripts/bolas_sinnoh.py            # só mede e grava o censo
    python3 dev_scripts/bolas_sinnoh.py --demo     # autoteste, não grava
    python3 dev_scripts/bolas_sinnoh.py --aplicar  # escreve (mexe em flags.h)

POR QUE EXISTE, medido em 22/08/2026
------------------------------------
O `importa_npcs_sinnoh.py` recusa `OBJ_EVENT_GFX_POKEBALL` pela decisão 4
("mobiliário nunca vira NPC"), e a decisão continua certa: bola virada boneco é
gente de pé em cima de um item. Só que a recusa cobra caro, e o número está
medido: **272 bolas da fonte em mapas de ESCOPO**, o maior bloco isolado do
déficit de objetos de Sinnoh (517 na medição do mesmo dia). É a mesma emenda
que as 447 pedras de Rock Smash já receberam em 18/08: a decisão proíbe virar
BONECO, e nunca proibiu portar o objeto COMO ELE É.

Bola de item é mecânica NATIVA deste motor, e não invenção: `OBJ_EVENT_GFX_
ITEM_BALL` mais `Common_EventScript_FindItem`, que lê o item de
`trainer_sight_or_berry_tree_id` e a quantidade de `movement_range_x`
(`src/item_ball.c:10-25`, medido). É o mesmo par que a Hoenn de fábrica usa.

DE ONDE SAI O ITEM DE CADA BOLA, e por que não é chute
------------------------------------------------------
No Platinum, objeto com `script` entre 7000 e 7999 é ITEM VISÍVEL
(`SCRIPT_ID_OFFSET_VISIBLE_ITEMS`, `include/script_manager.h:95`), e o índice é
`script - 7000` dentro da tabela `res/field/scripts/scripts_visible_items.s`. O
arquivo é texto: a tabela é a sequência de `ScriptEntry`, e o corpo de cada
rótulo diz o item e a quantidade em duas linhas,

    VisibleItems_Route202_Potion:
        SetVar VAR_0x8008, ITEM_POTION
        SetVar VAR_0x8009, 1

Medido: 328 entradas, 327 com item, e **326 dos 327 itens existem neste fork
com o mesmo nome**. O único que não existe é `ITEM_LUNAR_WING`, da Fullmoon
Island, que está cortada do porte. Não há tabela de tradução a manter.

OS PORTÕES, na mesma ordem do importador de NPC
------------------------------------------------
1. tile ALCANÇÁVEL a pé pelos warps, com empurrão de no máximo `RAIO` tiles
   (bola em tile que ninguém pisa é item que ninguém pega), e o censo escreve
   quantas casas cada uma andou;
2. tile livre de objeto, placa e warp;
3. teto de 64 templates por mapa e teto da FONTE (nenhum mapa termina com mais
   objeto do que o Platinum tem);
4. item que existe aqui.
Quem não passa vira linha de censo com o motivo, nunca bola no lugar errado.

A FLAG, e por que ela é permanente
-----------------------------------
Ao contrário da pedra de Rock Smash (que usa `FLAG_TEMP_*` de propósito, porque
o jogo original faz a pedra voltar), item pego tem que ficar pego para sempre.
Uma flag por bola, apelido de `FLAG_UNUSED_*` da faixa livre medida por
`flags_livres.py`, portanto **custo ZERO de save**: a faixa já existe no bloco
gravado e só ganha nome. O bloco entra em APPEND no fim de `flags.h`, e o
endereço de uma flag JÁ GRAVADA nunca se move (é história, como o
`liga_bolas_johto.py` escreveu).
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import conserta_route222 as R222            # noqa: E402
import importa_npcs_sinnoh as I             # noqa: E402

APLICAR = "--aplicar" in sys.argv
PLAT = I.PLAT
FLAGS_H = f"{REPO}/include/constants/flags.h"
CENSO = f"{REPO}/dev_scripts/bolas_sinnoh_censo.tsv"

GFX = "OBJ_EVENT_GFX_ITEM_BALL"
SCRIPT = "Common_EventScript_FindItem"
MARCA = {"origem": "pokeplatinum-bola"}

ABRE = ("// >>> Bolas de item visíveis de Sinnoh "
        "(dev_scripts/bolas_sinnoh.py, 22/08/2026) >>>")
FECHA = "// <<< Bolas de item visíveis de Sinnoh <<<"

# Primeira flag da maior faixa contígua livre medida por `flags_livres.py` em
# 22/08/2026 (0x20D2 a 0x319D, 4.300 flags). O alocador nunca reusa endereço já
# apelidado: ele lê o flags.h de hoje antes de escrever.
FAIXA = (0x20D2, 0x319D)

FONTE_TABELA = "res/field/scripts/scripts_visible_items.s"

# Empurrão máximo, em tiles, de uma bola que caiu em parede. O importador de NPC
# usa 1, e por um motivo bom: NPC 3 tiles fora muda com quem o jogador fala. A
# bola não fala e não anda, e a régua dela é outra: o que importa é que ela
# esteja ALCANÇÁVEL e na mesma região do mapa. Medido em 22/08/2026 com raio 1,
# 154 das 320 bolas da fonte eram recusadas por tile; com raio 3 as recusas
# caem, e o censo escreve tile a tile quantas casas cada uma andou, para que
# ninguém confunda "empurrada 3" com "coordenada da fonte".
RAIO = 3


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


# --------------------------------------------------------------- a tabela
def tabela(_cache={}):
    """índice (script - 7000) -> (ITEM_X, quantidade), lido do .s da fonte."""
    if _cache:
        return _cache["t"]
    s = open(os.path.join(PLAT, FONTE_TABELA), encoding="utf-8").read()
    rotulos = re.findall(r"^    ScriptEntry (\w+)", s, re.M)
    corpo = {m.group(1): m.group(2)
             for m in re.finditer(r"^(\w+):\n((?:    .*\n)+)", s, re.M)}
    saida = {}
    for i, r in enumerate(rotulos):
        b = corpo.get(r, "")
        it = re.search(r"SetVar VAR_0x8008, (ITEM_\w+)", b)
        q = re.search(r"SetVar VAR_0x8009, (\d+)", b)
        if it:
            saida[i] = (it.group(1), int(q.group(1)) if q else 1)
    _cache["t"] = saida
    return saida


def itens_do_fork(_cache={}):
    if not _cache:
        _cache["s"] = set(re.findall(
            r"^\s*(ITEM_\w+)",
            open(f"{REPO}/include/constants/items.h", encoding="utf-8").read(),
            re.M))
    return _cache["s"]


def bolas_da_fonte(fonte):
    """Objetos da fonte que são item VISÍVEL, na ordem em que ela os lista."""
    fora = []
    for e in fonte.get("object_events") or []:
        s = e.get("script")
        if isinstance(s, int) and 7000 <= s < 8000:
            fora.append(e)
    return fora


# ---------------------------------------------------------------- as flags
def apelidados(txt):
    """Todo FLAG_UNUSED_0xNNN que já tem apelido apontando para ele."""
    return set(re.findall(r"\bFLAG_UNUSED_(0x[0-9A-Fa-f]+)\b",
                          "\n".join(l for l in txt.splitlines()
                                    if not re.match(r"\s*#define\s+FLAG_UNUSED_",
                                                    l))))


def alocador(txt):
    """Gerador de nomes `FLAG_UNUSED_0xNNN` livres dentro de `FAIXA`."""
    usados = {int(h, 16) for h in apelidados(txt)}
    existe = set(re.findall(r"#define\s+FLAG_UNUSED_(0x[0-9A-Fa-f]+)\b", txt))
    existe = {int(h, 16) for h in existe}
    for n in range(FAIXA[0], FAIXA[1] + 1):
        if n not in usados and n in existe:
            yield f"FLAG_UNUSED_0x{n:X}"


def apelido(mapa, item, usados):
    base = "FLAG_ITEM_SINNOH_BOLA_" + re.sub(
        r"[^A-Z0-9]", "", mapa.upper()) + "_" + item[len("ITEM_"):]
    nome, n = base, 1
    while nome in usados:
        n += 1
        nome = f"{base}_{n}"
    usados.add(nome)
    return nome


# ------------------------------------------------------------------ main
def main():
    if "--demo" in sys.argv:
        return demo()
    layouts = {l["id"]: l for l in json.load(
        open(f"{REPO}/data/layouts/layouts.json"))["layouts"]}
    heads = I.headers_do_platinum()
    por_chave = {}
    for h, (ev, mx) in heads.items():
        por_chave.setdefault(I.chave(h), (h, ev, mx))
    tab = tabela()
    itens = itens_do_fork()
    txt_flags = open(FLAGS_H, encoding="utf-8").read()
    livre = alocador(txt_flags)
    nomes = set(re.findall(r"#define\s+(FLAG_\w+)", txt_flags))

    censo = [("mapa", "x_fonte", "z_fonte", "x_nosso", "y_nosso", "item",
              "qtd", "flag", "regra", "motivo")]
    stats = {"bolas": 0, "mapas": 0, "ja_tem": 0, "fora_tile": 0,
             "fora_ocupado": 0, "fora_item": 0, "fora_teto": 0,
             "fora_sem_indice": 0, "empurradas": 0, "fora_planta": 0}
    novas_flags = []

    for meu in I.mapas_editaveis_sinnoh():
        if meu in _cortados():
            continue
        h = I.APELIDOS.get(meu)
        alvo = (h,) + heads[h] if h in heads else por_chave.get(I.chave(meu))
        if not alvo:
            continue
        header, arq_ev, matriz = alvo
        pe = os.path.join(PLAT, "res/field/events", arq_ev + ".json")
        if not os.path.exists(pe):
            continue
        fonte = json.load(open(pe))
        cruas = bolas_da_fonte(fonte)
        if not cruas:
            continue
        pm = f"{REPO}/data/maps/{meu}/map.json"
        d = json.load(open(pm))
        if I.planta_provisoria(layouts, d["layout"]):
            stats["fora_planta"] += len(cruas)
            for e in cruas:
                censo.append((meu, e["x"], e["z"], "", "", "", "", "", "-",
                              "planta provisoria: molde de portao 13x9"))
            continue
        objs = d.get("object_events") or []
        conv = I.conversor_de_coordenada(fonte, layouts[d["layout"]]["width"],
                                         layouts[d["layout"]]["height"],
                                         header, matriz, d,
                                         vazio=not objs)
        if conv is None:
            continue
        regra = getattr(conv, "regra", "?")
        W, H, g = I.grade(layouts, d["layout"])
        pisa = I.alcancaveis(W, H, g, d.get("warp_events") or [])
        if not pisa:
            pisa = {(x, y) for y in range(H) for x in range(W)
                    if ((g[y][x] >> 10) & 3) == 0}
            regra += " | alcance nao semeavel (sem warp), so andavel"
        ja = {(o.get("x"), o.get("y")) for o in objs}
        ja |= {(o.get("x"), o.get("y")) for o in (d.get("bg_events") or [])}
        ja |= {(w.get("x"), w.get("y")) for w in (d.get("warp_events") or [])}
        # bola nossa que JA existe reclama a da fonte, pela coordenada: e a
        # mesma idempotencia por evento do importador de NPC.
        antigas = [o for o in objs if o.get("origem") == "pokeplatinum-bola"
                   or GFX in str(o.get("graphics_id"))]
        reclamados = set()
        teto = min(64 - len(objs),
                   len(fonte.get("object_events") or []) - len(objs))
        novas = []
        for e in cruas:
            idx = e["script"] - 7000
            if idx not in tab:
                stats["fora_sem_indice"] += 1
                censo.append((meu, e["x"], e["z"], "", "", "", "", "", regra,
                              f"script {e['script']} sem entrada na tabela de "
                              f"itens visiveis da fonte"))
                continue
            item, qtd = tab[idx]
            x, y = conv(e)
            velha = next((o for o in antigas if id(o) not in reclamados
                          and abs(o["x"] - x) <= 1 and abs(o["y"] - y) <= 1),
                         None)
            if velha is not None:
                reclamados.add(id(velha))
                stats["ja_tem"] += 1
                censo.append((meu, e["x"], e["z"], x, y, item, qtd, "", regra,
                              "ja existe bola nossa nesta coordenada"))
                continue
            if item not in itens:
                stats["fora_item"] += 1
                censo.append((meu, e["x"], e["z"], x, y, item, qtd, "", regra,
                              f"{item} nao existe neste fork"))
                continue
            pos = next(((x + dx, y + dy) for r in range(RAIO + 1)
                        for dx in range(-r, r + 1) for dy in range(-r, r + 1)
                        if max(abs(dx), abs(dy)) == r
                        and (x + dx, y + dy) in pisa
                        and (x + dx, y + dy) not in ja), None)
            if pos is None:
                stats["fora_tile"] += 1
                censo.append((meu, e["x"], e["z"], x, y, item, qtd, "", regra,
                              "coordenada nao cai em tile alcancavel livre "
                              "(nem 1 tile ao lado)"))
                continue
            if len(novas) >= max(0, teto):
                stats["fora_teto"] += 1
                censo.append((meu, e["x"], e["z"], x, y, item, qtd, "", regra,
                              "teto de 64 templates ou teto da fonte"))
                continue
            if pos != (x, y):
                stats["empurradas"] += 1
            flag = apelido(meu, item, nomes)
            alvo_flag = next(livre, None)
            if alvo_flag is None:
                censo.append((meu, e["x"], e["z"], x, y, item, qtd, "", regra,
                              "a faixa de FLAG_UNUSED reservada acabou"))
                break
            novas_flags.append((flag, alvo_flag, item))
            ja.add(pos)
            censo.append((meu, e["x"], e["z"], pos[0], pos[1], item, qtd,
                          flag, regra,
                          "" if pos == (x, y) else
                          f"empurrada {max(abs(pos[0]-x), abs(pos[1]-y))} tile(s)"))
            novas.append({
                "graphics_id": GFX, "x": pos[0], "y": pos[1],
                "elevation": ((g[pos[1]][pos[0]] >> 12) & 0xF) or 3,
                "movement_type": "MOVEMENT_TYPE_LOOK_AROUND",
                "movement_range_x": qtd, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": item,
                "script": SCRIPT, "flag": flag, **MARCA})
        if not novas:
            continue
        stats["bolas"] += len(novas)
        stats["mapas"] += 1
        d["object_events"] = objs + novas      # append: a save guarda indice
        if APLICAR:
            json.dump(d, open(pm, "w"), indent=2, ensure_ascii=False)

    if APLICAR and novas_flags:
        larg = max(len(n) for n, _a, _i in novas_flags) + 2
        bloco = [ABRE,
                 "// Uma flag por bola, permanente: item pego fica pego. Os",
                 "// enderecos sao apelidos de FLAG_UNUSED da faixa livre medida",
                 "// por flags_livres.py, portanto custo ZERO de save."]
        for n, a, it in novas_flags:
            bloco.append(f"#define {n:<{larg}}{a}  // {it}")
        bloco.append(FECHA)
        with open(FLAGS_H, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(bloco) + "\n")

    with open(CENSO, "w", encoding="utf-8") as f:
        for l in censo:
            f.write("\t".join(str(c) for c in l) + "\n")
    print(f"censo: {len(censo) - 1} linhas em {os.path.relpath(CENSO, REPO)}")
    print("resumo:", stats)
    print(f"flags novas: {len(novas_flags)}")
    print("\naplicado" if APLICAR else "\nnada escrito (use --aplicar)")
    return 0


# --------------------------------------------------------------- autoteste
def demo():
    """O que prova que a bola é bola, e não boneco com nome de item."""
    tab = tabela()
    # 1. a tabela da fonte é lida por ÍNDICE, e o índice é a posição do
    #    ScriptEntry. Duas âncoras conhecidas, uma no começo e uma no meio.
    assert tab[0] == ("ITEM_POTION", 1), tab[0]
    assert tab[1] == ("ITEM_REPEL", 1), tab[1]
    assert len(tab) >= 320, len(tab)

    # 2. o item de cada bola existe NESTE fork, fora a exceção medida.
    itens = itens_do_fork()
    faltam = sorted({i for i, _q in tab.values() if i not in itens})
    assert faltam == ["ITEM_LUNAR_WING"], faltam

    # 3. o motor lê item de `trainer_sight_or_berry_tree_id` e quantidade de
    #    `movement_range_x`: se alguém trocar os campos, o jogador ganha o item
    #    errado calado. A prova é o próprio src, não a memória.
    src = open(f"{REPO}/src/item_ball.c", encoding="utf-8").read()
    assert "movementRangeX" in src and "trainerRange_berryTreeId" in src

    # 4. o alocador de flag NÃO devolve endereço que já tem apelido. Mutação
    #    plantada: apelidar a próxima livre tem que fazer o alocador pulá-la.
    txt = open(FLAGS_H, encoding="utf-8").read()
    primeira = next(alocador(txt))
    sujo = txt + f"\n#define FLAG_TESTE_PLANTADO {primeira}\n"
    assert next(alocador(sujo)) != primeira

    # 5. e o apelido não colide com nome que já existe no header.
    nomes = set(re.findall(r"#define\s+(FLAG_\w+)", txt))
    a = apelido("Route209", "ITEM_POTION", set(nomes))
    assert a not in nomes and a.startswith("FLAG_ITEM_SINNOH_BOLA_")

    # 6. bola da fonte é a que tem script na faixa 7000-7999, e SÓ ela. Um
    #    script de placa (2500+) ou de item escondido (8000+) não pode entrar.
    falso = {"object_events": [{"script": 2500}, {"script": 8000},
                               {"script": 7000}, {"script": 6999}]}
    assert [e["script"] for e in bolas_da_fonte(falso)] == [7000]
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
