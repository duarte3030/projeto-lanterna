#!/usr/bin/env python3
"""Fecha o resto do bloco B4 de Sinnoh: o treinador da fonte que os dois scripts
irmãos não alcançam.

Uso:
    python3 dev_scripts/treinadores_faltantes_sinnoh.py            # só relata
    python3 dev_scripts/treinadores_faltantes_sinnoh.py --aplica
    python3 dev_scripts/treinadores_faltantes_sinnoh.py --demo

## Por que existe um terceiro script, e não um remendo nos dois primeiros

Medido em 12/08/2026, contra os 536 `res/field/events/events_*.json` do
pokeplatinum: a fonte põe **417 objetos de treinador** no mapa, em **403
constantes distintas**. Aqui, **395** já eram batalháveis (citadas por
`trainerbattle` E com bloco `=== TRAINER_X ===` em `src/data/trainers.party`).
Faltavam **30 constantes / 31 objetos**, e nenhum deles cabe no laço dos dois
irmãos, porque os dois exigem a MESMA coisa: um objeto importado, mudo, num mapa
cujo alinhamento com a fonte fecha objeto a objeto.

- `treinadores_rota_sinnoh.py` e `treinadores_masmorra_sinnoh.py` rodam hoje com
  saldo **zero**: dentro do que eles enxergam, não sobrou ninguém.
- O que sobrou é de três tipos, e só o primeiro é remendável ali:
  **(1)** mapa cujo alinhamento quebra DEPOIS do treinador (`OreburghMine_B2F`:
  seis pessoas na fonte, cinco aqui, e quem falta é o terceiro Machop, que vem
  atrás dos dois workers que interessam);
  **(2)** mapa de planta REAPROVEITADA, onde o importador nunca pôs ninguém
  (`CanalaveCity_Gym` é interior de Hoenn emprestado, com só o Byron dentro, e
  `StarkMountainOutside` é a antecâmara provisória de 13x9);
  **(3)** metade de mapa que aqui virou um mapa só (`Route204` casa com
  `events_route_204_south`, e as gêmeas moram em `events_route_204_north`).

## O que este script NÃO faz, e a medida que provou não ser preciso

Não toca em `include/constants/opponents.h` nem em `src/data/trainers.party`.
**Medido antes de escrever uma linha: as 30 constantes que faltavam JÁ estão
declaradas e JÁ têm bloco de time.** Id novo duplicaria time e texto na ROM e
daria duas flags de "já venci" à mesma pessoa. Maior id declarado: 2440; o teto
subiu para 4000 em 12/08; a faixa 2441-3999 continua inteira, e este bloco gasta
**zero** dela.

Os níveis dos blocos são os que a sessão de importação já remapeou para a faixa
de Sinnoh (Colin 147/149 contra 6/8 na fonte). Reescrevê-los para o nível cru da
fonte seria desfazer o trabalho do bloco B8 dentro do B4; espécie, item e golpe
são os da fonte e foram conferidos.

## De onde sai cada campo (medido na fonte, não lembrado)

- **quem é treinador**: objeto da fonte cujo `script` é `str` e começa com
  `TRAINER_`.
- **raio de visão**: `data[0]` do mesmo objeto (sem `data`, raio 0).
- **fala**: `res/trainers/data/<slug>.json`, campo `messages`. Em gen 4 a fala
  mora junto com o time, não no banco de texto do mapa.
- **metade da dupla**: `double_battle_id`, nunca a ordem no arquivo.
- **sprite**: `texto_sinnoh.sprite_esperado`, a MESMA tabela que o importador
  usou, então nenhum gráfico novo entra.

## Coordenada é decisão humana, e por isso está numa tabela à mão

Nos três mapas de `NOVOS` a planta **não é a do Platinum** (duas são emprestadas
e a terceira é a outra metade da rota), então converter a coordenada da fonte
por proporção poria gente dentro de parede. As coordenadas foram escolhidas à
mão, e o que a ferramenta faz sozinha é RECUSAR a que não presta, com quatro
guardas mecânicas:

1. dentro do mapa e com colisão 0 no `map.bin` do layout;
2. nenhum objeto, warp ou bg_event já naquele tile;
3. comportamento do metatile é chão comum (não é porta, escada nem seta de
   warp): boneco em cima de porta esconde a porta;
4. **conectividade**: o conjunto de tiles alcançáveis a partir do primeiro warp
   do mapa tem que ser o MESMO antes e depois, tirando os tiles que os bonecos
   passam a ocupar. É a guarda que impede fechar corredor com gente, e foi ela
   que reprovou a primeira escolha para as gêmeas da Route204: (10,3) e (11,3)
   com o `Npc1` já parado em (12,3) tampavam as três colunas do corredor do
   norte e deixavam a saída de cima inalcançável a pé.

## Direção: `LOOK_AROUND` nos criados, de propósito

`treinadores_masmorra_sinnoh.py` só porta a direção da fonte quando o boneco
está na coordenada da fonte, porque "virado para oeste" numa planta emprestada
aponta para outra parede. Aqui NENHUM criado está na coordenada da fonte, então
todos ficam com `MOVEMENT_TYPE_LOOK_AROUND`, que enxerga girando e faz o raio de
visão valer em qualquer direção.

## Objeto novo entra no FIM da lista

A save guarda ÍNDICE de objeto (`objectEvents[]`). Acrescentar no fim não mexe em
índice de ninguém; inserir no meio quebraria a save do Gui, que está congelada.
Os criados levam `"origem": "pokeplatinum_b4"`, valor DIFERENTE do
`"pokeplatinum"` que o importador grava: os irmãos comparam com igualdade exata,
e marcar igual faria a contagem de alinhamento deles crescer e reprovar mapa que
hoje passa.
"""
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import texto_sinnoh as T          # noqa: E402
import treinadores_rota_sinnoh as R  # noqa: E402
import valida_mapas_sinnoh as V   # noqa: E402
import valida_warp_tile as W      # noqa: E402

PLAT = T.PLAT
EVENTOS = os.path.join(PLAT, "res/field/events")
APLICA = "--aplica" in sys.argv

MARCA = "pokeplatinum_b4"

# Objeto importado que já é esta pessoa, num mapa cujo alinhamento quebra depois
# dela. Chave: nosso mapa -> arquivo de eventos da fonte. O ÍNDICE não está aqui:
# ele é medido por alinhamento de PREFIXO (ver `indice_por_prefixo`), senão esta
# tabela seria a mesma adivinhação que ela existe para evitar.
REUSO = {
    "OreburghMine_B2F": ("events_oreburgh_mine_b2f",
                         ("TRAINER_WORKER_COLIN", "TRAINER_WORKER_MASON")),
}

# Treinador da fonte que NÃO tem boneco aqui, e onde ele vai ficar.
# (constante da fonte, x, y). Constante repetida = as duas metades de uma
# batalha dupla, na ordem de `double_battle_id`.
NOVOS = {
    # Interior emprestado de Hoenn (o port nunca construiu o prédio), 23x21.
    # Os sete espalhados pelas duas metades da sala, nenhum no corredor da
    # coluna 21 que leva ao Byron nem no tile do warp de saída.
    "CanalaveCity_Gym": ("events_canalave_city_gym", (
        ("TRAINER_WORKER_GERARDO", 3, 18),
        ("TRAINER_WORKER_JACKSON", 6, 15),
        ("TRAINER_BLACK_BELT_DAVID", 12, 16),
        ("TRAINER_BLACK_BELT_RICKY", 3, 11),
        ("TRAINER_WORKER_GARY", 10, 8),
        ("TRAINER_ACE_TRAINER_BREANNA", 18, 11),
        ("TRAINER_ACE_TRAINER_CESAR", 19, 8),
    )),
    # Antecâmara provisória de 13x9 (planta da Route226_Access). O Darien é a
    # única pessoa do mapa na fonte; fica na linha de baixo do corredor, fora da
    # linha 5, que é a que liga os dois warps.
    "StarkMountainOutside": ("events_stark_mountain_outside", (
        ("TRAINER_DRAGON_TAMER_DARIEN", 6, 6),
    )),
    # Route204 aqui é a rota inteira e casa com a metade SUL da fonte. As gêmeas
    # são da metade norte, e vão lado a lado como na fonte, na clareira larga do
    # norte (linha 8, 12 tiles de largura), nunca no corredor de três colunas.
    "Route204": ("events_route_204_north", (
        ("TRAINER_TWINS_LIV_AND_LIZ", 15, 8),
        ("TRAINER_TWINS_LIV_AND_LIZ", 16, 8),
    )),
}


def layout_do_mapa(mapa):
    """(largura, altura, palavras do map.bin, tileset primario, secundario)."""
    d = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                       encoding="utf-8"))
    todos = {l["id"]: l for l in json.load(open(
        os.path.join(REPO, "data/layouts/layouts.json"), encoding="utf-8"))["layouts"]}
    l = todos[d["layout"]]
    b = open(os.path.join(REPO, l["blockdata_filepath"]), "rb").read()
    pal = struct.unpack("<%dH" % (len(b) // 2), b)
    return l["width"], l["height"], pal, l["primary_tileset"], l["secondary_tileset"]


def comportamento(prim, sec, mt):
    """Comportamento do metatile, com o corte primario/secundario em 512."""
    if mt < len(prim):
        return prim[mt]
    i = mt - 512
    return sec[i] if 0 <= i < len(sec) else -1


def componentes(w, h, pal, bloqueados):
    """Ilhas de tiles andáveis, tratando `bloqueados` como parede.

    Sem ponto de partida de propósito. A primeira versão fazia busca a partir do
    primeiro warp do mapa e reprovava as gêmeas da Route204 como "inalcançáveis":
    a metade NORTE da rota não se liga à metade sul a pé, o caminho é por dentro
    da Ravaged Path. Ilha desligada é geografia da fonte, não defeito; o que não
    pode é uma ilha que existia PARTIR em duas por causa de um boneco novo.
    """
    livre = [((pal[y * w + x] >> 10) & 3) == 0 and (x, y) not in bloqueados
             for y in range(h) for x in range(w)]
    vistos, fora = set(), []
    for y0 in range(h):
        for x0 in range(w):
            if not livre[y0 * w + x0] or (x0, y0) in vistos:
                continue
            ilha, fila = {(x0, y0)}, [(x0, y0)]
            vistos.add((x0, y0))
            while fila:
                x, y = fila.pop()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in vistos \
                            and livre[ny * w + nx]:
                        vistos.add((nx, ny))
                        ilha.add((nx, ny))
                        fila.append((nx, ny))
            fora.append(ilha)
    return fora


def ocupados(d, com_os_meus=True):
    """Todo tile que já tem objeto, warp ou placa no nosso map.json.

    `com_os_meus=False` ignora o que ESTA ferramenta já pôs (`origem` igual a
    MARCA). Sem isso a guarda reprovaria a própria escrita na segunda rodada e o
    `--demo` ficaria vermelho depois de um `--aplica` bem-sucedido, que é a
    lição 4.11: teste que guarda cópia de um fato envelhece calado.
    """
    fora = set()
    for chave in ("object_events", "warp_events", "bg_events", "coord_events"):
        for e in d.get(chave) or []:
            if e.get("x") is None:
                continue
            if not com_os_meus and e.get("origem") == MARCA:
                continue
            fora.add((e["x"], e["y"]))
    return fora


def recusa_coordenada(mapa, pontos):
    """[] se as coordenadas prestam, senão a lista de motivos.

    Quatro guardas, nesta ordem: dentro do mapa, tile andável e livre, chão
    comum (não porta nem escada), e conectividade preservada.
    """
    d = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                       encoding="utf-8"))
    w, h, pal, ts1, ts2 = layout_do_mapa(mapa)
    prim, _ = W.tabela_de_atributos(ts1)
    sec, _ = W.tabela_de_atributos(ts2)
    tomados = ocupados(d, com_os_meus=False)
    males = []
    novos = set()
    for x, y in pontos:
        if not (0 <= x < w and 0 <= y < h):
            males.append((x, y, "fora do mapa"))
            continue
        pal_i = pal[y * w + x]
        if (pal_i >> 10) & 3:
            males.append((x, y, "tile de colisao"))
            continue
        if (x, y) in tomados or (x, y) in novos:
            males.append((x, y, "tile ja ocupado"))
            continue
        beh = comportamento(prim or [], sec or [], pal_i & 0x3FF)
        if beh in W.COMPORTA_WARP:
            males.append((x, y, "tile de porta/escada: esconderia a passagem"))
            continue
        novos.add((x, y))
    if males or not novos:
        return males
    # Boneco que já está no mapa TAMBÉM tapa o tile dele. Sem isso a régua
    # mentia dos dois lados: o corredor de três colunas do norte da Route204 já
    # tem o `Npc1` parado em (12,3), e ignorá-lo fazia a mutação plantada passar.
    solidos = {(o["x"], o["y"]) for o in (d.get("object_events") or [])
               if o.get("x") is not None and o.get("origem") != MARCA}
    depois = componentes(w, h, pal, solidos | novos)
    for ilha in componentes(w, h, pal, solidos):
        resto = ilha - novos
        if resto and not any(resto <= nova for nova in depois):
            males.append((None, None, f"a ilha de {len(ilha)} tile(s) em "
                                      f"{sorted(ilha)[0]} parte em duas"))
    for x, y in novos:
        if not any(any((x + dx, y + dy) in nova for nova in depois)
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            males.append((x, y, "ninguem chega perto: batalha inalcancavel"))
    return males


def fonte_do_arquivo(arq):
    return json.load(open(os.path.join(EVENTOS, arq + ".json"), encoding="utf-8"))


def objetos_da_constante(fonte, constante):
    """Objetos da fonte com esta constante, na ordem de `double_battle_id`."""
    achados = [o for o in fonte.get("object_events", [])
               if o.get("script") == constante]
    return sorted(achados, key=lambda o: o.get("double_battle_id") or 0)


def indice_por_prefixo(mapa, fonte, constante):
    """Índice do NOSSO objeto que é esta pessoa, ou None se não der para provar.

    O importador não gravou o índice de origem, então a ligação é por ORDEM. A
    ordem inteira não fecha nestes mapas (é por isso que os irmãos recusam), mas
    o PREFIXO até a pessoa que interessa pode fechar: se as posições 0..k baterem
    uma a uma no `graphics_id`, quem está em k aqui é quem está em k lá, e o que
    o importador descartou está depois. Qualquer furo antes de k e devolve None.
    """
    sprites = V.sprites_utilizaveis()
    f_npcs, _ = T.separa_fonte(fonte)
    alvo = [i for i, o in enumerate(f_npcs) if o.get("script") == constante]
    if len(alvo) != 1:
        return None
    k = alvo[0]
    d = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                       encoding="utf-8"))
    nossos = [(i, o) for i, o in enumerate(d.get("object_events") or [])
              if o.get("origem") == "pokeplatinum"]
    if k >= len(nossos):
        return None
    for i in range(k + 1):
        if T.sprite_esperado(f_npcs[i], sprites) != nossos[i][1].get("graphics_id"):
            return None
    return nossos[k][0]


def peca(mapa, bruto, nossa, usados):
    """(rotulo, raio, trecho de scripts.inc, bytes de texto) ou None."""
    dados = R.dados_do_treinador(bruto["script"])
    if dados is None:
        return None
    texto = R.falas(dados, bruto.get("double_battle_id", 1))
    if texto is None:
        return None
    intro, derrota, depois, faltou, duplo = texto
    lab = R.rotulo_livre(usados, mapa, R.camel(bruto, bruto["script"]))
    txt = lab.replace("_EventScript_", "_Text_")
    batalha = (f"\ttrainerbattle_double {nossa}, {txt}Intro, {txt}Defeat, "
               f"{txt}NoPartner\n") if duplo else \
        f"\ttrainerbattle_single {nossa}, {txt}Intro, {txt}Defeat\n"
    trecho = (f"\n{lab}::\n{batalha}"
              f"\tmsgbox {txt}Post, MSGBOX_AUTOCLOSE\n\tend\n\n"
              f'{txt}Intro:\n\t.string "{intro}"\n\n'
              f'{txt}Defeat:\n\t.string "{derrota}"\n\n'
              f'{txt}Post:\n\t.string "{depois}"\n')
    b = len(intro) + len(derrota) + len(depois)
    if duplo:
        trecho += f'\n{txt}NoPartner:\n\t.string "{faltou}"\n'
        b += len(faltou)
    return lab, str((bruto.get("data") or [0])[0]), trecho, b


def plano():
    """[(mapa, [reuso], [novo], corpo)] mais recusas."""
    consts = R.constantes_de_treinador()
    com_time = R.blocos_com_time()
    ja = R.usados_em_scripts()
    sprites = V.sprites_utilizaveis()
    saida, recusas = [], []

    for mapa in sorted(set(REUSO) | set(NOVOS)):
        pm = os.path.join(REPO, "data/maps", mapa, "map.json")
        ps = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        if not os.path.exists(pm):
            recusas.append((mapa, "mapa nao existe aqui", ""))
            continue
        inc = R.le(ps) if os.path.exists(ps) else ""
        usados = set(__import__("re").findall(r"^(\w+)::?", inc, 8))
        reusos, criados, corpo = [], [], ""

        pedidos = []
        if mapa in REUSO:
            arq, lista = REUSO[mapa]
            pedidos += [(arq, c, None) for c in lista]
        if mapa in NOVOS:
            arq, lista = NOVOS[mapa]
            pedidos += [(arq, c, (x, y)) for c, x, y in lista]

        # As coordenadas do mapa inteiro são conferidas de uma vez: conectividade
        # é propriedade do conjunto, não de um ponto.
        pontos = [p for _a, _c, p in pedidos if p]
        males = recusa_coordenada(mapa, pontos) if pontos else []
        if males:
            for m in males:
                recusas.append((mapa, "coordenada recusada", m))
            continue

        vistos_const = {}
        for arq, constante, ponto in pedidos:
            nossa = "TRAINER_SINNOH_" + constante[len("TRAINER_"):]
            fonte = fonte_do_arquivo(arq)
            copias = objetos_da_constante(fonte, constante)
            if not copias:
                recusas.append((mapa, "constante nao esta na fonte", constante))
                continue
            n = vistos_const.get(constante, 0)
            if n >= len(copias):
                recusas.append((mapa, "mais copias do que a fonte tem", constante))
                continue
            bruto = copias[n]
            vistos_const[constante] = n + 1
            if nossa not in consts:
                recusas.append((mapa, "sem constante", nossa))
                continue
            if nossa not in com_time:
                recusas.append((mapa, "sem bloco em trainers.party", nossa))
                continue
            if nossa in ja:
                recusas.append((mapa, "ja citado por script", nossa))
                continue
            if n == 0:
                p = peca(mapa, bruto, nossa, usados)
                if p is None:
                    recusas.append((mapa, "fala nao traduz", nossa))
                    continue
                lab, raio, trecho, b = p
                corpo += trecho
                vistos_const[constante + "@rotulo"] = lab
            else:
                # Segunda metade da dupla: rótulo e texto próprios, mesma
                # constante, mesmo `trainerbattle_double`.
                p = peca(mapa, bruto, nossa, usados)
                if p is None:
                    recusas.append((mapa, "fala nao traduz", nossa))
                    continue
                lab, raio, trecho, b = p
                corpo += trecho
            if ponto is None:
                i = indice_por_prefixo(mapa, fonte, constante)
                if i is None:
                    recusas.append((mapa, "prefixo de alinhamento nao fecha",
                                    constante))
                    continue
                reusos.append((i, lab, raio, nossa, b))
            else:
                criados.append({
                    "graphics_id": T.sprite_esperado(bruto, sprites),
                    "x": ponto[0], "y": ponto[1], "elevation": 3,
                    "movement_type": V.MOVIMENTO_PADRAO,
                    "movement_range_x": 0, "movement_range_y": 0,
                    "trainer_type": "TRAINER_TYPE_NORMAL",
                    "trainer_sight_or_berry_tree_id": raio,
                    "script": lab, "flag": "0", "origem": MARCA,
                })
            # Só depois de tudo dar certo a constante vira "já usada": duas
            # pessoas com a mesma flag de derrotado é o defeito que isso evita.
            if n + 1 == len(copias):
                ja.add(nossa)
        if reusos or criados:
            saida.append((mapa, reusos, criados, corpo))
    return saida, recusas


def main():
    tudo, recusas = plano()
    nr = sum(len(r) for _m, r, _c, _b in tudo)
    nc = sum(len(c) for _m, _r, c, _b in tudo)
    bytes_txt = sum(x[4] for _m, r, _c, _b in tudo for x in r)
    print(f"treinadores a ligar: {nr + nc} em {len(tudo)} mapas "
          f"({nr} reusando boneco importado, {nc} com objeto novo no fim da lista)")
    print("zero id novo, zero flag nova, zero bloco novo em trainers.party")
    for mapa, r, c, _b in tudo:
        print(f"  {mapa:24s} reuso={len(r)} novos={len(c)}")
    if recusas:
        print("\nrecusados:")
        for x in recusas:
            print("   ", *x)
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0

    feitos = recusados = 0
    for mapa, reusos, criados, corpo in tudo:
        pm = os.path.join(REPO, "data/maps", mapa, "map.json")
        # Releitura tardia: outro agente pode ter mexido no mesmo arquivo entre o
        # planejamento e agora. Recusa em vez de sobrescrever.
        atual = json.load(open(pm, encoding="utf-8"))
        lista = atual.get("object_events")
        if lista is None:
            lista = atual["object_events"] = []
        n = 0
        for i, lab, raio, _nossa, _b in reusos:
            if i >= len(lista):
                recusados += 1
                continue
            ev = lista[i]
            if ev.get("origem") != "pokeplatinum" \
                    or str(ev.get("script", "0")) not in R.MUDO \
                    or str(ev.get("flag", "0")) not in R.SEM_FLAG:
                recusados += 1
                continue
            ev["script"] = lab
            ev["trainer_type"] = "TRAINER_TYPE_NORMAL"
            ev["trainer_sight_or_berry_tree_id"] = raio
            n += 1
        tomados = ocupados(atual)
        for novo in criados:
            if (novo["x"], novo["y"]) in tomados:
                recusados += 1
                continue
            lista.append(novo)
            tomados.add((novo["x"], novo["y"]))
            n += 1
        if not n:
            continue
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(atual, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(os.path.join(REPO, "data/maps", mapa, "scripts.inc"), "a",
                  encoding="utf-8") as f:
            f.write("\n@ Treinador do pokeplatinum que os dois scripts irmaos nao "
                    "alcancam\n@ (dev_scripts/treinadores_faltantes_sinnoh.py)\n"
                    + corpo)
        feitos += n
    print(f"\nligados: {feitos}   recusados na releitura: {recusados}")
    return 0


def demo():
    """Uma armadilha por caso, todas medidas na fonte ou no map.bin."""
    import re

    # 1. a lacuna que este script fecha é REAL e é medida, não copiada: todo
    #    treinador da tabela está na fonte e não tem par batalhável aqui.
    ja = R.usados_em_scripts()
    com_time = R.blocos_com_time()
    pedidos = [(a, c) for a, lista in REUSO.values() for c in lista] + \
              [(a, c) for a, lista in NOVOS.values() for c, _x, _y in lista]
    for arq, c in pedidos:
        assert os.path.exists(os.path.join(EVENTOS, arq + ".json")), arq
        assert objetos_da_constante(fonte_do_arquivo(arq), c), (arq, c)

    # 2. nenhuma constante nova: as 30 já estão declaradas e já têm time. Se um
    #    dia isso deixar de valer, o script tem que parar, não inventar id.
    consts = R.constantes_de_treinador()
    for _arq, c in pedidos:
        n = "TRAINER_SINNOH_" + c[len("TRAINER_"):]
        assert n in consts, f"{n} nao esta em opponents.h"
        assert n in com_time, f"{n} nao tem bloco em trainers.party"

    # 3. id e rótulo ÚNICOS em opponents.h. A checagem certa é de unicidade, não
    #    de existência: dois rótulos no mesmo id dão a mesma flag de derrotado a
    #    duas pessoas, e o build nem reclama.
    txt = R.le(os.path.join(REPO, "include/constants/opponents.h"))
    pares = re.findall(r"#define\s+(TRAINER_\w+)\s+(\d+)", txt)
    nomes = [a for a, _b in pares]
    ids = [int(b) for _a, b in pares]
    assert len(set(nomes)) == len(nomes), "rotulo repetido em opponents.h"
    assert len(set(ids)) == len(ids), "id repetido em opponents.h"
    teto = int(re.search(r"MAX_TRAINERS_COUNT_EMERALD\s+(\d+)", txt).group(1))
    assert max(ids) < teto, f"id acima do teto {teto}"

    # 4. as coordenadas escolhidas passam nas quatro guardas.
    for mapa, (_arq, lista) in NOVOS.items():
        assert not recusa_coordenada(mapa, [(x, y) for _c, x, y in lista]), mapa

    # 5. MUTAÇÃO PLANTADA, e é a que interessa: a guarda de conectividade tem
    #    que reprovar o par de gêmeas na escolha ERRADA. Com o `Npc1` parado em
    #    (12,3), pôr as duas em (10,3) e (11,3) tampa as três colunas do
    #    corredor do norte da Route204 e a saída de cima fica inalcançável a pé.
    #    Se este assert ficar verde, a guarda parou de guardar.
    ruim = recusa_coordenada("Route204", [(10, 3), (11, 3)])
    assert any("parte em duas" in str(m[2]) for m in ruim), \
        "a guarda de conectividade parou de pegar corredor fechado"

    # 5b. e as outras três guardas também: parede, tile ocupado e porta.
    assert any("colisao" in m[2] for m in recusa_coordenada("Route204", [(0, 0)]))
    assert any("ocupado" in m[2] for m in recusa_coordenada("Route204", [(12, 3)]))
    # (12,19) do ginásio de Canalave é o segundo tile do tapete de saída: tem
    # comportamento de seta de warp e NÃO tem warp declarado em cima, então é o
    # caso que separa a guarda de porta da guarda de tile ocupado.
    assert any("porta" in m[2]
               for m in recusa_coordenada("CanalaveCity_Gym", [(12, 19)]))

    # 6. o alinhamento de PREFIXO é o que autoriza o reuso, e ele tem que ser
    #    verdadeiro: os dois workers da OreburghMine_B2F são as posições 0 e 1
    #    dos dois lados, e o que o importador descartou (um Machop) vem depois.
    f = fonte_do_arquivo("events_oreburgh_mine_b2f")
    gente, _ = T.separa_fonte(f)
    assert [o.get("script") for o in gente[:2]] == \
        ["TRAINER_WORKER_COLIN", "TRAINER_WORKER_MASON"]
    assert len(gente) == 6, "a fonte da OreburghMine_B2F mudou de tamanho"
    for c in ("TRAINER_WORKER_COLIN", "TRAINER_WORKER_MASON"):
        i = indice_por_prefixo("OreburghMine_B2F", f, c)
        assert i is not None, c

    # 7. a metade da dupla vem de `double_battle_id`, nunca da ordem, e as duas
    #    falas são diferentes: Liv fala por 1 e Liz por 2.
    f = fonte_do_arquivo("events_route_204_north")
    par = objetos_da_constante(f, "TRAINER_TWINS_LIV_AND_LIZ")
    assert [o["double_battle_id"] for o in par] == [1, 2]
    d = R.dados_do_treinador("TRAINER_TWINS_LIV_AND_LIZ")
    assert R.falas(d, 1)[0].startswith("Liv:") and R.falas(d, 2)[0].startswith("Liz:")
    assert R.falas(d, 1)[3] and R.falas(d, 1)[4], "dupla precisa do NoPartner"

    # 8. a fala sai da fonte, nunca daqui.
    d = R.dados_do_treinador("TRAINER_WORKER_COLIN")
    cru = [m for m in d["messages"] if m["type"] == "TRMSG_PRE_BATTLE"][0]
    assert cru["en_US"][0].split()[0].strip(",") in R.falas(d, 1)[0]

    # 9. nenhum rótulo duplicado na unidade de montagem inteira depois do que
    #    este script escreveu (os 2018 scripts.inc viram um event_scripts.s só).
    rep = T.rotulos_repetidos()
    assert not rep, f"{len(rep)} rotulo(s) duplicado(s): {rep[:5]}"

    # 10. e todo script citado por map.json dos mapas desta leva existe no
    #     scripts.inc do mesmo mapa, com o texto fechando em `$`.
    for mapa in sorted(set(REUSO) | set(NOVOS)):
        pm = os.path.join(REPO, "data/maps", mapa, "map.json")
        ps = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        inc = R.le(ps) if os.path.exists(ps) else ""
        rot = set(re.findall(r"^(\w+)::?", inc, re.M))
        d = json.load(open(pm, encoding="utf-8"))
        for o in (d.get("object_events") or []) + (d.get("bg_events") or []):
            s = str(o.get("script", "0"))
            if s in R.MUDO or "_EventScript_" not in s or s.startswith("Sinnoh_"):
                continue
            assert s in rot, f"{mapa}: script citado e inexistente: {s}"
        for bloco in re.findall(r'^(\w+:\n(?:\t\.string ".*"\n)+)', inc, re.M):
            assert bloco.rstrip().endswith('$"'), f"{mapa}: texto sem $ final"

    print("demo ok (13 casos; mutacao de corredor fechado reprovada como devia, "
          "zero id novo, zero rotulo duplicado)")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
