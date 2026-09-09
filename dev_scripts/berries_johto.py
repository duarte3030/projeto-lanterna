#!/usr/bin/env python3
"""Da id e script as 36 arvores de berry mudas de Johto e do WorldHub.

    python3 dev_scripts/berries_johto.py            # tabela, nao escreve
    python3 dev_scripts/berries_johto.py --demo     # autoteste
    python3 dev_scripts/berries_johto.py --aplicar  # escreve

Por que so na SEGUNDA e ULTIMA quebra de save
---------------------------------------------
Arvore de berry nao e desenho: e ESTADO. Cada arvore ocupa uma vaga de
`SaveBlock1.berryTrees[BERRY_TREES_COUNT]` (8 B por vaga), e o objeto do mapa
guarda o INDICE dessa vaga em `trainer_sight_or_berry_tree_id`. Subir
`BERRY_TREES_COUNT` empurra tudo que vem depois de `berryTrees` dentro do
SaveBlock1, ou seja invalida save.

O item 12 da fila de bugs de 08/09/2026 mediu as 36 e as deixou como estavam,
porque a janela da quebra unica ja tinha fechado. O Gui reabriu a janela na
resposta 58 do mesmo dia ("pode subir o teto das IDs, nao tem problema quebrar
save"), e esta e a SEGUNDA e ULTIMA quebra: `SAVE_LAYOUT_REVISION` vai de 2 para
3 e a regra "nunca mais" volta a valer depois dela.

O defeito que estas 36 tinham
-----------------------------
Todas nasceram com `trainer_sight_or_berry_tree_id` igual a 0 e `script` igual a
"0". Id 0 nao e "sem id": e a vaga `berryTrees[0]`, que jogo nenhum planta, e por
isso as 36 liam o mesmo estado permanentemente vazio. Sem script, o aperto de A
nem chegava no `BerryTreeScript`. Elas eram desenho de arvore, nao arvore. As 36
tambem estavam com `MOVEMENT_TYPE_LOOK_AROUND`, que e o movimento de gente, e nao
o `MOVEMENT_TYPE_BERRY_TREE_GROWTH` que faz o objeto reavaliar o estagio da
planta (`MovementType_BerryTreeGrowth`, src/event_object_movement.c:4386).

De onde vem a berry de cada uma
-------------------------------
Da fonte, `fontes-mapas/hns` (Heart n Soul, o demake de HGSS que ja e a fonte dos
mapas de Johto desta arvore). Ela desenha as MESMAS 36 arvores, nas MESMAS
coordenadas, cada uma com id proprio e com a berry escrita no nome do id
(`BERRY_TREE_ORAN_1` em Route29 15,11 e por diante), e planta cada uma com
`BERRY_STAGE_BERRIES` no `new_game.inc` dela. Nenhuma das 36 fica sem fonte: a
casacao e por coordenada exata, e arvore que nao casar e RECUSADA em vez de
receber berry escolhida no chute.

O id da fonte nao e reaproveitado, so a ESPECIE da berry. A fonte repete id
entre mapas (o WorldHub dela usa os mesmos ids das rotas, e Route26 usa o
`BERRY_TREE_ROUTE_118_SITRUS_1` de Hoenn), e id repetido e o defeito que este
script existe para matar: duas arvores no mesmo indice sao a mesma arvore, e
colher uma esvazia a outra.

As duas travas
--------------
1. toda arvore das 36 tem de casar com uma arvore da fonte na coordenada exata,
   e o nome do id da fonte tem de terminar numa berry que existe em
   `include/constants/berries.h`. Sem isso nao ha berry para plantar;
2. nenhum id novo pode repetir id que ja existe, e a numeracao entra toda DEPOIS
   do maior id em uso (append), que e a unica forma de mexer em indice de save
   sem mover o que ja esta gravado.

Alcance entra como NOTA, e nao como trava: a arvore ja esta no mapa desde a
importacao de Johto, este script nao move nem cria objeto nenhum. Recusar aqui
por alcance apagaria a berry de uma arvore que continuaria plantada na tela.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

BERRY_H = os.path.join(RAIZ, "include/constants/berry.h")
BERRIES_H = os.path.join(RAIZ, "include/constants/berries.h")
NEW_GAME = os.path.join(RAIZ, "data/scripts/new_game.inc")
FONTE = os.path.expanduser("~/Projetos/pokemon-claude/fontes-mapas/hns")
GFX = "OBJ_EVENT_GFX_BERRY_TREE"
SCRIPT = "BerryTreeScript"
MOVIMENTO = "MOVEMENT_TYPE_BERRY_TREE_GROWTH"
ESTAGIO = "BERRY_STAGE_BERRIES"
FOLGA = 8  # vagas livres deixadas depois do ultimo id, para a proxima arvore
           # nao precisar de outra quebra de save


def especies_de_berry():
    """As berries que existem, lidas de FOREACH_BERRY."""
    texto = open(BERRIES_H).read()
    m = re.search(r"#define FOREACH_BERRY\(F\)(.*?)\n\n", texto, re.S)
    corpo = m.group(1) if m else texto
    return set(re.findall(r"F\((\w+)\)", corpo))


def ids_existentes():
    texto = open(BERRY_H).read()
    pares = re.findall(r"^#define\s+(BERRY_TREE_\w+)\s+(\d+)", texto, re.M)
    return {n: int(v) for n, v in pares}, texto


def arvores_mudas():
    """As arvores desta arvore que estao com id 0 e sem script, em ordem estavel."""
    saida = []
    for mapa in sorted(os.listdir(os.path.join(RAIZ, "data/maps"))):
        pm = os.path.join(RAIZ, "data/maps", mapa, "map.json")
        if not os.path.exists(pm):
            continue
        d = json.load(open(pm))
        for i, o in enumerate(d.get("object_events") or []):
            if (o.get("graphics_id") == GFX
                    and str(o.get("trainer_sight_or_berry_tree_id")) == "0"):
                saida.append((mapa, i, o["x"], o["y"]))
    return saida


def arvores_da_fonte():
    """{(mapa, x, y): nome do id na fonte} para toda arvore de berry do hns."""
    saida = {}
    base = os.path.join(FONTE, "data/maps")
    if not os.path.isdir(base):
        return saida
    for mapa in os.listdir(base):
        pm = os.path.join(base, mapa, "map.json")
        if not os.path.exists(pm):
            continue
        try:
            d = json.load(open(pm))
        except Exception:
            continue
        for o in d.get("object_events") or []:
            if str(o.get("graphics_id", "")).endswith("BERRY_TREE"):
                saida[(mapa, o["x"], o["y"])] = str(
                    o.get("trainer_sight_or_berry_tree_id"))
    return saida


def berry_do_nome(nome, especies):
    """A ESPECIE escrita no nome do id da fonte, ou None.

    `BERRY_TREE_ORAN_1` -> ORAN, `BERRY_TREE_ROUTE_118_SITRUS_1` -> SITRUS,
    `BERRY_TREE_ROUTE_102_ORAN` -> ORAN. Le de tras para a frente e para na
    primeira palavra que e berry de verdade, para `ROUTE`, `118` e afins nunca
    virarem especie.
    """
    if not nome or nome == "0":
        return None
    for parte in reversed(nome.replace("BERRY_TREE_", "").split("_")):
        if parte in especies:
            return parte
    return None


def sufixo_do_mapa(mapa):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", mapa).upper().replace("__", "_")


def plano():
    especies = especies_de_berry()
    fonte = arvores_da_fonte()
    mudas = arvores_mudas()
    entram, recusadas = [], []
    contagem = {}
    for mapa, indice, x, y in mudas:
        nome_fonte = fonte.get((mapa, x, y))
        if nome_fonte is None:
            recusadas.append((mapa, x, y, "a fonte hns nao desenha arvore nesta coordenada"))
            continue
        berry = berry_do_nome(nome_fonte, especies)
        if berry is None:
            recusadas.append((mapa, x, y,
                              f"o id da fonte ({nome_fonte}) nao termina em berry conhecida"))
            continue
        chave = (mapa, berry)
        contagem[chave] = contagem.get(chave, 0) + 1
        entram.append({"mapa": mapa, "indice": indice, "x": x, "y": y,
                       "berry": berry, "fonte": nome_fonte,
                       "n": contagem[chave]})
    # so numera _1, _2 quando a mesma berry repete no mesmo mapa
    for e in entram:
        prefixo = "BERRY_TREE_WORLD_HUB" if e["mapa"] == "WorldHub" else \
            f"BERRY_TREE_JOHTO_{sufixo_do_mapa(e['mapa'])}"
        total = contagem[(e["mapa"], e["berry"])]
        sufixo = f"_{e['n']}" if total > 1 else ""
        e["nome"] = f"{prefixo}_{e['berry']}{sufixo}"
    return entram, recusadas


def escreve(entram, ids, texto):
    proximo = max(ids.values()) + 1
    for e in entram:
        e["id"] = proximo
        proximo += 1
    teto = proximo + FOLGA

    bloco = [
        "",
        "// Arvores de berry de Johto e do WorldHub, plantadas em 08/09/2026 na",
        "// SEGUNDA e ULTIMA quebra de save do cartucho 1 (resposta 58 do Gui,",
        "// dev_scripts/berries_johto.py). Sao as 36 que o item 12 da fila de bugs",
        "// mediu com `trainer_sight_or_berry_tree_id` 0 e `script` \"0\", ou seja",
        "// lendo `berryTrees[0]` e mudas para sempre. A berry de cada uma vem da",
        "// fonte `fontes-mapas/hns`, que desenha as MESMAS 36 nas MESMAS",
        "// coordenadas; so a ESPECIE veio de la, nunca o id, porque a fonte repete",
        "// id entre mapas e id repetido e o defeito que isto conserta.",
    ]
    largura = max(len(e["nome"]) for e in entram)
    for e in entram:
        bloco.append(f"#define {e['nome'].ljust(largura)} {e['id']}")
    bloco.append("")
    bloco.append(f"// As {FOLGA} vagas entre {proximo - 1} e {teto - 1} ficam livres de proposito:")
    bloco.append("// a janela de save fechou de novo com esta quebra, entao arvore nova daqui")
    bloco.append("// para a frente sai da folga em vez de custar outra save.")

    velho = re.search(r"^#define BERRY_TREES_COUNT \d+$", texto, re.M).group(0)
    texto = texto.replace(velho, "\n".join(bloco) + f"\n#define BERRY_TREES_COUNT {teto}")
    open(BERRY_H, "w").write(texto)

    por_mapa = {}
    for e in entram:
        por_mapa.setdefault(e["mapa"], []).append(e)
    for mapa, lista in por_mapa.items():
        pm = os.path.join(RAIZ, "data/maps", mapa, "map.json")
        d = json.load(open(pm))
        for e in lista:
            o = d["object_events"][e["indice"]]
            assert o["graphics_id"] == GFX and o["x"] == e["x"] and o["y"] == e["y"], \
                f"o indice {e['indice']} de {mapa} nao e mais a arvore medida"
            o["trainer_sight_or_berry_tree_id"] = e["nome"]
            o["script"] = SCRIPT
            o["movement_type"] = MOVIMENTO
        json.dump(d, open(pm, "w"), indent=2, ensure_ascii=False)
        open(pm, "a").write("\n")

    linhas = ["", "\t@ Johto e WorldHub, 08/09/2026. A berry de cada uma vem da fonte",
              "\t@ hns, que planta as 36 com BERRY_STAGE_BERRIES no new_game dela."]
    largura = max(len(e["nome"]) for e in entram) + 1
    ultimo = None
    for e in sorted(entram, key=lambda e: (e["mapa"], e["id"])):
        if e["mapa"] != ultimo:
            linhas.append("")
            linhas.append(f"\t@ {e['mapa']}")
            ultimo = e["mapa"]
        linhas.append(f"\tsetberrytree {(e['nome'] + ',').ljust(largura)} "
                      f"{('BERRY_ID_' + e['berry'] + ',').ljust(18)} {ESTAGIO}")
    ng = open(NEW_GAME).read()
    alvo = "\tsetberrytree BERRY_TREE_ROUTE_130_LIECHI, BERRY_ID_LIECHI, BERRY_STAGE_BERRIES\n\treturn"
    assert alvo in ng, "nao achei o fim de EventScript_ResetAllBerries"
    ng = ng.replace(alvo, alvo.replace("\n\treturn", "\n" + "\n".join(linhas) + "\n\treturn"))
    open(NEW_GAME, "w").write(ng)
    return teto, len(entram)


def main():
    aplicar = "--aplicar" in sys.argv
    demo = "--demo" in sys.argv

    ids, texto = ids_existentes()
    entram, recusadas = plano()
    print(f"arvores mudas (id 0 e sem script): {len(entram) + len(recusadas)}")
    print(f"  entram: {len(entram)} em {len({e['mapa'] for e in entram})} mapas")
    print(f"  recusadas: {len(recusadas)}")
    for mapa, x, y, motivo in recusadas:
        print(f"    {mapa} ({x},{y}): {motivo}")
    maior = max(ids.values())
    teto = maior + 1 + len(entram) + FOLGA
    antes = int(re.search(r"BERRY_TREES_COUNT (\d+)", texto).group(1))
    print(f"BERRY_TREE_* ja definidos: {len(ids)}, maior id {maior}")
    print(f"BERRY_TREES_COUNT: {antes} -> {teto} (folga de {FOLGA}), "
          f"{(teto - antes) * 8} B de SaveBlock1")
    por_berry = {}
    for e in entram:
        por_berry[e["berry"]] = por_berry.get(e["berry"], 0) + 1
    print("berries, tiradas da fonte: " +
          ", ".join(f"{k} x{v}" for k, v in sorted(por_berry.items())))

    if demo:
        # O autoteste que importa: nenhuma das 36 pode ficar sem fonte, nenhum
        # nome pode repetir, nenhum id novo pode cair em cima de id existente, e
        # a mutacao plantada (uma coordenada que a fonte nao desenha) tem de ser
        # RECUSADA em vez de receber berry de chute.
        ruins = []
        if recusadas:
            ruins.append(f"{len(recusadas)} arvore(s) sem fonte")
        if len(entram) != 36:
            ruins.append(f"esperava 36 arvores mudas, achei {len(entram)}")
        nomes = [e["nome"] for e in entram]
        if len(set(nomes)) != len(nomes):
            ruins.append("nome de id repetido entre as novas")
        if set(nomes) & set(ids):
            ruins.append(f"nome ja existia em berry.h: {sorted(set(nomes) & set(ids))[:3]}")
        if ruins:
            print("DEMO REPROVOU: " + "; ".join(ruins))
            return 1
        especies = especies_de_berry()
        fonte = arvores_da_fonte()
        alvo = entram[0]
        falsa = (alvo["mapa"], alvo["x"] + 777, alvo["y"] + 777)
        if berry_do_nome(fonte.get(falsa), especies) is not None:
            print("DEMO REPROVOU: a coordenada inventada achou berry na fonte")
            return 1
        if berry_do_nome("BERRY_TREE_ROUTE_118_SITRUS_1", especies) != "SITRUS":
            print("DEMO REPROVOU: a leitura da especie pegou ROUTE ou o numero")
            return 1
        print(f"DEMO OK: as {len(entram)} arvores tem fonte na coordenada exata, "
              f"nome unico e id em append; a coordenada {falsa[1]},{falsa[2]} "
              f"inventada em {falsa[0]} foi recusada")
        return 0

    if not aplicar:
        for e in entram:
            print(f"  {e['mapa']:<16} ({e['x']:>3},{e['y']:>3})  {e['berry']:<7} "
                  f"<- {e['fonte']}")
        print("\n(nada foi escrito; use --aplicar)")
        return 0

    teto, quantas = escreve(entram, ids, texto)
    print(f"\nAPLICADO: {quantas} arvores, BERRY_TREES_COUNT = {teto}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
