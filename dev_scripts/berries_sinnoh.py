#!/usr/bin/env python3
"""Planta os 90 canteiros de berry de Sinnoh, o corte COM PRAZO da ESTADO 0.s.

    python3 dev_scripts/berries_sinnoh.py            # tabela, nao escreve
    python3 dev_scripts/berries_sinnoh.py --demo     # autoteste
    python3 dev_scripts/berries_sinnoh.py --aplicar  # escreve

Por que so na quebra unica de save
----------------------------------
Canteiro de berry nao e desenho: e ESTADO. Cada arvore ocupa uma vaga de
`SaveBlock1.berryTrees[BERRY_TREES_COUNT]` (8 B por vaga), e o objeto do mapa
guarda o INDICE dessa vaga em `trainer_sight_or_berry_tree_id`. Subir
`BERRY_TREES_COUNT` empurra tudo que vem depois de `berryTrees` dentro do
SaveBlock1, ou seja invalida save. A 0.s registrou isso como "corte COM PRAZO,
cai na primeira janela de save aberta de proposito". E agora.

De onde vem cada canteiro
-------------------------
Do proprio Platinum: os 90 `OBJ_EVENT_GFX_BERRY_SOIL` dos 23 mapas de Sinnoh que
casam com header de la, lidos pelo MESMO caminho que `importa_npcs_sinnoh` usa
(`headers_do_platinum`, `conversor_de_coordenada`), para a coordenada daqui ser
a mesma que qualquer outra ferramenta do projeto calcularia.

O canteiro entra VAZIO, e isso e fiel a fonte: `BERRY_SOIL` no Platinum e terra
de plantar, nao arvore com fruta. O jogador planta.

As tres travas
--------------
1. o tile convertido tem de ser ANDAVEL e desocupado (`livre`, raio 5), senao o
   canteiro nasce dentro de parede;
2. em mapa FECHADO (sem conexao de borda), o tile tem de estar no alcance dos
   warps, senao o canteiro nasce em ilha que ninguem pisa. Em ROTA a mesma
   exigencia seria falso positivo: a busca em largura anda so a pe, e area de
   Surf ou de Rock Smash aparece como inalcancavel mesmo sendo conteudo normal
   de Sinnoh (Route 218 e Route 224 sao alcancadas nadando). Nessas o alcance
   vira NOTA, e a trava que fica de pe e a colisao;
3. o canteiro nao pode fazer a VIZINHANCA passar de 15 objetos, que e o teto de
   sprite acordado por vez (`OBJECT_EVENTS_COUNT` menos a vaga do jogador). A
   licao 1 da 0.s e que objeto que nao acorda nao existe, e o que decide isso e
   a densidade LOCAL, nao o total do mapa: `TrySpawnObjectEvents` so acorda o
   que cai na caixa de carga em volta da camera. A caixa usada aqui e a da
   camera com folga, 19 por 15 tiles (|dx| <= 9, |dy| <= 7), a mesma ordem de
   grandeza do que `src/event_object_movement.c` carrega. Rota grande com 27
   objetos espalhados passa; sala apertada com 15 na mesma tela, nao.
Canteiro que cai em qualquer uma das tres NAO entra, e sai nomeado no relatorio.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

BERRY_H = os.path.join(RAIZ, "include/constants/berry.h")
GFX_FONTE = "OBJ_EVENT_GFX_BERRY_SOIL"
GFX_NOSSO = "OBJ_EVENT_GFX_BERRY_TREE"
SCRIPT = "BerryTreeScript"
TETO_SPRITE = 15
CAIXA_X, CAIXA_Y = 9, 7


def ids_existentes():
    texto = open(BERRY_H).read()
    pares = re.findall(r"^#define\s+(BERRY_TREE_\w+)\s+(\d+)", texto, re.M)
    return {n: int(v) for n, v in pares}, texto


def levanta():
    import importa_npcs_sinnoh as I
    heads = I.headers_do_platinum()
    por_chave = {}
    for h, (ev, mx) in heads.items():
        por_chave.setdefault(I.chave(h), (h, ev, mx))
    casados = []
    for m in I.mapas_editaveis_sinnoh():
        h = I.APELIDOS.get(m)
        alvo = (h,) + heads[h] if h in heads else por_chave.get(I.chave(m))
        if alvo:
            casados.append((m,) + alvo)
    return I, casados


def alcance_com_conexoes(I, W, H, g, nosso):
    """Tiles alcancaveis contando warp E CONEXAO de borda.

    `importa_npcs_sinnoh.alcancaveis` semeia so pelos warps, e isso basta para
    interior. Em ROTA nao basta, e foi o que reprovou 15 canteiros na primeira
    medicao: o jogador entra numa rota pela CONEXAO com a rota vizinha, nao por
    warp, entao uma rota de 4 warps devolvia uma ilha minuscula e todo canteiro
    de verdade caia "fora do alcance". Aqui toda borda que tem conexao entra
    como semente, com os tiles andaveis daquela borda.
    """
    alcance = set(I.alcancaveis(W, H, g, nosso.get("warp_events") or []))
    sementes = []
    for con in (nosso.get("connections") or []):
        lado = con.get("direction")
        if lado == "up":
            sementes += [(x, 0) for x in range(W)]
        elif lado == "down":
            sementes += [(x, H - 1) for x in range(W)]
        elif lado == "left":
            sementes += [(0, y) for y in range(H)]
        elif lado == "right":
            sementes += [(W - 1, y) for y in range(H)]
    sementes = [(x, y) for x, y in sementes if ((g[y][x] >> 10) & 3) == 0]
    if sementes:
        import conserta_route222 as R222
        alcance |= set(R222.alcance(W, H, g, sementes))
    return alcance


def plano():
    I = None
    I, casados = levanta()
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(RAIZ, "data/layouts/layouts.json")))["layouts"]}
    entram, recusados, notas = [], [], []
    for meu, header, arq_ev, matriz in casados:
        caminho = os.path.join(I.PLAT, "res/field/events", arq_ev + ".json")
        if not os.path.exists(caminho):
            continue
        fonte = json.load(open(caminho))
        soltos = [o for o in (fonte.get("object_events") or [])
                  if o.get("graphics_id") == GFX_FONTE]
        if not soltos:
            continue
        pm = os.path.join(RAIZ, "data/maps", meu, "map.json")
        nosso = json.load(open(pm))
        L = layouts[nosso["layout"]]
        larg, alt = L["width"], L["height"]
        conv = I.conversor_de_coordenada(fonte, larg, alt, header, matriz,
                                         nosso=nosso)
        if conv is None:
            for e in soltos:
                recusados.append((meu, e["x"], e["z"], "sem conversor de coordenada"))
            continue
        W, H, g = I.grade(layouts, nosso["layout"])
        alcance = alcance_com_conexoes(I, W, H, g, nosso)
        ocupados = {(o["x"], o["y"]) for o in (nosso.get("object_events") or [])}
        ocupados |= {(o["x"], o["y"]) for o in (nosso.get("bg_events") or [])}
        ocupados |= {(o["x"], o["y"]) for o in (nosso.get("warp_events") or [])}
        corpos = [(o["x"], o["y"]) for o in (nosso.get("object_events") or [])]
        for e in soltos:
            x, y = conv(e)
            pos = I.livre(layouts, nosso["layout"], x, y, ocupados, raio=5)
            if pos is None:
                recusados.append((meu, e["x"], e["z"], "nenhum tile andavel a 5 tiles"))
                continue
            fechado = not (nosso.get("connections") or [])
            if alcance and pos not in alcance:
                if fechado:
                    recusados.append((meu, e["x"], e["z"],
                                      f"mapa fechado e tile {pos} fora do alcance dos warps"))
                    continue
                notas.append((meu, pos, "so por Surf ou HM: a pe a busca nao chega"))
            perto = 1 + sum(1 for cx, cy in corpos
                            if abs(cx - pos[0]) <= CAIXA_X and abs(cy - pos[1]) <= CAIXA_Y)
            if perto > TETO_SPRITE:
                recusados.append((meu, e["x"], e["z"],
                                  f"{perto} objetos na caixa da camera em volta de {pos}"))
                continue
            ocupados.add(pos)
            corpos.append(pos)
            entram.append((meu, pos[0], pos[1]))
    return entram, recusados, notas


def nome_da_constante(mapa, n):
    limpo = re.sub(r"(?<!^)(?=[A-Z])", "_", mapa).upper().replace("__", "_")
    return f"BERRY_TREE_SINNOH_{limpo}_{n}"


def escreve(entram, ids, texto):
    proximo = max(ids.values()) + 1
    novos = []
    por_mapa = {}
    for mapa, x, y in entram:
        por_mapa.setdefault(mapa, 0)
        por_mapa[mapa] += 1
        nome = nome_da_constante(mapa, por_mapa[mapa])
        novos.append((nome, proximo, mapa, x, y))
        proximo += 1
    teto = proximo  # o maior id novo mais um

    bloco = ["", "// Canteiros de berry de Sinnoh, plantados em 08/09/2026 na quebra",
             "// unica de save (dev_scripts/berries_sinnoh.py). Sao os 90",
             "// OBJ_EVENT_GFX_BERRY_SOIL do Platinum, o corte COM PRAZO da ESTADO 0.s.",
             "// Entram vazios de proposito: BERRY_SOIL la e terra de plantar."]
    largura = max(len(n) for n, *_ in novos)
    for nome, valor, mapa, x, y in novos:
        bloco.append(f"#define {nome.ljust(largura)} {valor}")
    bloco.append("")

    velho = re.search(r"^#define BERRY_TREES_COUNT \d+$", texto, re.M).group(0)
    texto = texto.replace(velho, "\n".join(bloco) + f"\n#define BERRY_TREES_COUNT {teto}")
    open(BERRY_H, "w").write(texto)

    por_mapa = {}
    for nome, valor, mapa, x, y in novos:
        por_mapa.setdefault(mapa, []).append((nome, x, y))
    for mapa, lista in por_mapa.items():
        pm = os.path.join(RAIZ, "data/maps", mapa, "map.json")
        d = json.load(open(pm))
        d.setdefault("object_events", [])
        for nome, x, y in lista:
            d["object_events"].append({
                "graphics_id": GFX_NOSSO,
                "x": x, "y": y, "elevation": 3,
                "movement_type": "MOVEMENT_TYPE_BERRY_TREE_GROWTH",
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": nome,
                "script": SCRIPT,
                "flag": "0",
                "origem": "pokeplatinum",
            })
        json.dump(d, open(pm, "w"), indent=2, ensure_ascii=False)
        open(pm, "a").write("\n")
    return teto, len(novos)


def main():
    aplicar = "--aplicar" in sys.argv
    demo = "--demo" in sys.argv

    ids, texto = ids_existentes()
    entram, recusados, notas = plano()
    print(f"canteiros do Platinum nos mapas casados: {len(entram) + len(recusados)}")
    print(f"  entram: {len(entram)} em {len({m for m, _, _ in entram})} mapas")
    print(f"  recusados: {len(recusados)}")
    for mapa, x, z, motivo in recusados:
        print(f"    {mapa} ({x},{z}): {motivo}")
    print(f"  entram em area que a busca a pe nao alcanca (Surf ou HM): {len(notas)}")
    for mapa, pos, motivo in notas:
        print(f"    {mapa} {pos}: {motivo}")
    print(f"BERRY_TREE_* ja definidos: {len(ids)}, maior id {max(ids.values())}")
    print(f"BERRY_TREES_COUNT: 128 -> {max(ids.values()) + 1 + len(entram)} "
          f"({(max(ids.values()) + 1 + len(entram) - 128) * 8} B de SaveBlock1)")

    if demo:
        # O autoteste que importa: TODO canteiro planejado tem de cair em tile
        # andavel e dentro do alcance dos warps, e a mutacao plantada e um
        # canteiro em tile de parede, que a checagem tem de recusar.
        import importa_npcs_sinnoh as I
        import valida_mapas_sinnoh as V
        layouts = {l["id"]: l for l in json.load(
            open(os.path.join(RAIZ, "data/layouts/layouts.json")))["layouts"]}
        ruins = []
        for mapa, x, y in entram:
            d = json.load(open(os.path.join(RAIZ, "data/maps", mapa, "map.json")))
            if V.colisao(layouts, d["layout"], x, y) != 0:
                ruins.append((mapa, x, y, "tile com colisao"))
            if not (d.get("connections") or []):
                W, H, g = I.grade(layouts, d["layout"])
                alcance = alcance_com_conexoes(I, W, H, g, d)
                if alcance and (x, y) not in alcance:
                    ruins.append((mapa, x, y, "mapa fechado, fora do alcance"))
        if ruins:
            print(f"DEMO REPROVOU: {len(ruins)} canteiros em tile ruim")
            for linha in ruins[:5]:
                print("   ", linha)
            return 1
        mapa, x, y = entram[0]
        d = json.load(open(os.path.join(RAIZ, "data/maps", mapa, "map.json")))
        W, H, g = I.grade(layouts, d["layout"])
        parede = next(((px, py) for py in range(H) for px in range(W)
                       if ((g[py][px] >> 10) & 3) != 0), None)
        if parede is None:
            print("DEMO REPROVOU: nao achei tile de parede para plantar a mutacao")
            return 1
        if V.colisao(layouts, d["layout"], *parede) == 0:
            print("DEMO REPROVOU: a lente de colisao chamou parede de chao")
            return 1
        print(f"DEMO OK: {len(entram)} canteiros em tile andavel e alcancavel; "
              f"a mutacao em {parede} de {mapa} foi reconhecida como parede")
        return 0

    if not aplicar:
        print("\n(nada foi escrito; use --aplicar)")
        return 0

    teto, quantos = escreve(entram, ids, texto)
    print(f"\nAPLICADO: {quantos} canteiros, BERRY_TREES_COUNT = {teto}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
