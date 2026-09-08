#!/usr/bin/env python3
"""G4 da obra de Galar: os NPCs mudos e os itens escondidos dos 438 mapas.

Uso:
    python3 dev_scripts/gente_galar.py --demo       # autoteste, nao grava nada
    python3 dev_scripts/gente_galar.py --conferir   # simula e imprime o censo
    python3 dev_scripts/gente_galar.py --gravar     # grava flags.h + censo
    python3 dev_scripts/gente_galar.py --aplicar    # grava + ACRESCENTA nos mapas

Na obra NOVA (mapa que ainda nao existe em disco) quem escreve
`data/maps/Galar_*/map.json` e o `mundo_galar.py`, que importa daqui a funcao
`eventos_do_mapa()` e ja sai com o mapa completo. Ordem daquela obra:

    python3 dev_scripts/gente_galar.py --gravar     # flags primeiro
    python3 dev_scripts/mundo_galar.py --gravar     # mapas depois

DEPOIS QUE A FASE DE CONTEUDO COMECOU, `mundo_galar.py --gravar` deixou de ser
o caminho para levar objeto novo do G4 ao mapa, e isso foi MEDIDO em 06/09/2026,
na onda 5: reescrever os 438 `map.json` hoje derrubaria 140 `region_map_section`
do `conserta_mapsec_galar.py`, 178 `bg_events` (113 placas, 45 de porta fechada e
20 do lote I), 9 `coord_events` de porta de script, os warps que o lote S ligou e
todo o `scripts.inc` de cena. Por isso o `--aplicar` daqui e CIRURGICO: ele le o
`map.json` que existe, preserva byte a byte tudo o que ja esta la (inclusive o
`script` que o c4 pendurou num NPC do G4) e so ACRESCENTA, no fim da lista, o
objeto do G4 que ainda nao esta no mapa. Nada e removido e nenhum indice de
objeto existente anda de lugar, que e o que a save do Gui exige.

    python3 dev_scripts/gente_galar.py --aplicar
    python3 dev_scripts/estaticos_galar.py --aplicar   # repoe o bloco dele no FIM

O que entra, e por que o resto nao entra
----------------------------------------
Decisao 5 da condutora (NPC entra MUDO) e decisao 6 (item escondido com flag
nova da faixa 0x1C00+). Sobre esses dois trilhos, SEIS filtros MEDIDOS:

1. CATEGORIA DO GRAFICO (`tabela_gfx_galar.py`). Entra gente e placa. Cenario
   de script (arvore, monte de pedra, Poke Ball, feixe de covil de raide) nao
   entra porque mudo ele e bloqueio permanente ou promessa falsa. Um monte de
   pedra sem Rock Smash tranca caverna para sempre. Pokemon TAMBEM entra desde
   22/08/2026: `OBJ_EVENT_GFX_SPECIES` existe nesta build e a lei de Sinnoh
   ("sprite generico mente a especie") deixou de valer aqui. Quem separa o
   Pokemon de cenario do encontro jogavel e o filtro 6.

6. ENCONTRO ESTATICO E DO c5, NAO DO G4. Objeto cuja ARTE e de Pokemon E cujo
   script da fonte executa `setwildbattle` ou `seteventmon` nao entra por aqui:
   o dono dele e o `estaticos_galar.py` (bloco c5), que o poe no mapa com a
   especie certa, com `setwildbattle` e com a flag de renascimento. Regra
   escrita em 06/09/2026, na onda 5, e ela existe por uma medicao: com a tabela
   de gfx nova o G4 passaria a gravar 1.982 objetos em vez de 1.204, mas 531
   desses 778 novos JA sao encontro do c5, e o c5 larga o que o G4 ja pos no
   mapa (guarda `if l["no_mapa"]: continue`). Sem esta regra o placar de
   estaticos cairia de 1.018 para 498, ou seja trocaria 520 encontros jogaveis
   por 520 enfeites mudos. Com ela o ganho e limpo: 247 objetos que sao Pokemon
   de cenario ou tem script que nao e batalha, mais ate 11 que o c5 recusava e
   agora pode aceitar.

   As DUAS condicoes sao necessarias, e a segunda tambem: 4 objetos de arte de
   GENTE (nadadora, mulher, piquenique, operario) tem `setwildbattle` no script
   da fonte e ja estao no mapa desde a onda 1. Cobrar so o `setwildbattle`
   apagaria esses quatro NPCs sem que o c5 os repusesse, porque ele os recusa
   por especie sem nome e por opcode indecodificavel `[V]`.

2. TILE NAO ANDAVEL -> nao entra. Medido: 1.192 dos 4.254 objetos limpos (28%)
   estao em tile de colisao != 0. Nos 344 mapas de FRLG que este repo ja tem,
   esse numero e 4,4% (72 de 1.641), que e o balconista atras do balcao. O
   excesso e outra coisa, e da para ver: 774 dos 1.192 estao no MESMO metatile
   (592, colisao 1), quase todos nas linhas y=0 e y=1, dentro da parede do topo
   do mapa, com movimento 0 e sem script. E o deposito do autor: NPC nao usado
   estacionado fora da area jogavel. O plano permitia realocar pelo vizinho
   andavel; MEDIDO, realocar seria pior: despejaria doze fantasmas dentro de
   cada sala pequena (ver g07m14, que tem 12 estacionados e 1 NPC de verdade).
   Entao vale a segunda opcao do plano, "vai para a sujeira com motivo". O preco
   e perder os ~4% de balconista legitimo, que nesta obra seria mudo de qualquer
   jeito (o G3 ja deixou a enfermeira de fora do heal location de proposito).

3. TILE DE WARP -> nao entra. NPC e solido: em cima de uma porta ele tranca a
   porta, e o G3 acabou de abrir 1.247 delas.

4. TILE DE CURA (7,4) dos 12 mapas com heal location -> nao entra. Nascer
   dentro de um NPC e o unico jeito de o jogador ficar presoIndeed sem saida.

5. MOVIMENTO QUE PRECISA DE CENA -> nao entra. INVISIBLE (NPC invisivel e
   solido = parede invisivel) e BERRY_TREE_GROWTH (arvore de baga sem id de
   arvore).

O que e ZERADO no mapa e anotado no censo para a fase de conteudo:
- `trainer_type`: 146 objetos limpos tem trainer_type sadio na fonte. Treinador
  ativo sem time e sem cena e emboscada muda, entao vai TRAINER_TYPE_NONE no
  mapa e o valor da fonte fica no censo.
- `flag`: 953 objetos tem flag de historia na fonte. Nao existe flag de historia
  nesta obra (decisao 5), entao vai "0" e o valor fica no censo.
- `script`: vai "0". Os ponteiros de script sao a fila do G5.

Movimento
---------
Os dois enums (FireRed e o nosso) sao o MESMO de 0x00 a 0x43: mesmo valor,
mesmo nome, os dois descendem de Ruby. `--demo` reconfere isso contra
`fontes-mapas/pokefirered/include/constants/event_object_movement.h` quando ela
existe, em vez de acreditar. Divergem so no fim, e ai a traducao e por papel:

    FR 0x44-0x47 WALK_IN_PLACE_FAST_*  ->  nosso JOG_IN_PLACE_*
    FR 0x48-0x4B JOG_IN_PLACE_*        ->  nosso RUN_IN_PLACE_*
    FR 0x4C      INVISIBLE             ->  igual (mas filtrado, ver item 5)
    FR 0x4D-0x4F RAISE_HAND_AND_*      ->  MOVEMENT_TYPE_FACE_DOWN (nao temos
                                           "levantar a mao"; parar de frente e
                                           o mais perto de ficar parado)

Alcance de movimento
--------------------
`movement_range_x/y` sai 0 para todo mundo. O extrator do G0 nao leu o campo
(ele fica em +0x0A do template de 24 B, entre o movimento e o trainer_type), e
alcance 0 deixa o NPC no lugar, que e o comportamento seguro: NPC mudo que
perambula pode parar em cima de porta ou corredor, e ai vira o problema do
filtro 3 com pernas.

Itens escondidos
----------------
So `kind == 7` (BG_EVENT_HIDDEN_ITEM, o mesmo valor nos dois motores) vira item.
Os `kind` 0 a 4 sao placa/script e ficam no censo: sem script nao ha o que ler.
Os `kind` 5 e 6 nao existem em nenhum dos dois motores (o extrator do G0
decodificou item neles porque a regra dele era `kind >= 5`), entao tambem vao
para o censo, como lixo de leitura.

O `item` da fonte e id do FireRed, e o nosso items.h e outro (a expansao
inseriu itens de outras geracoes no meio). A traducao e por NOME, via
`fontes-mapas/pokefirered/include/constants/items.h`: id da fonte -> nome do
FireRed -> mesmo nome aqui. Item que nao existir aqui vai para o censo como
pendencia; NADA de criar item.

Cada item ganha uma flag NOVA em `FLAG_ITEM_GALAR_*`, apelidando
`FLAG_UNUSED_0x1C00` em diante (faixa autorizada pela decisao 6, conferida
livre: 0 dos 1.062 enderecos de 0x1C00 a 0x2025 tinham apelido). Apelidar flag
existente nao mexe em FLAGS_COUNT, entao a save do Gui nao muda de tamanho.
O motor guarda `hiddenItemId = flag - FLAG_HIDDEN_ITEMS_START` em 13 bits, e
0x1C00 - 0x1F4 = 6.668 cabe com folga em 8.191.
"""
import argparse
import collections
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import tabela_gfx_galar as G  # noqa: E402

FONTE = os.path.join(os.path.dirname(RAIZ), "fontes-mapas/galar-swsh/extraidos-ultimate")
PKFR = os.path.join(os.path.dirname(RAIZ), "fontes-mapas/pokefirered")
CENSO_MUNDO = f"{RAIZ}/dev_scripts/galar_mundo.json"
CENSO = f"{RAIZ}/dev_scripts/galar_gente.json"
FLAGS_H = f"{RAIZ}/include/constants/flags.h"

PRIMEIRA_FLAG = 0x1C00        # decisao 6
ULTIMA_FLAG = 0x2025          # fim da faixa livre medida
# Endereco da faixa de Galar que a MAO reservou e este alocador NAO pode entregar.
# Lição da maquina de Sinnoh (ESTADO 0.e): gerador que nao sabe o que a mao
# decidiu desfaz a decisao calado. FLAG_GALAR_QA_ANDAR (0x1CFF) e a flag de teste
# que abre o destino GALAR no barco (G5, data/scripts/travessia_regioes.inc).
RESERVADAS_A_MAO = {0x1CFF: "FLAG_GALAR_QA_ANDAR (G5, destino de teste no barco)"}

# NPC que a fonte NAO tem e a obra precisa. Um so ate agora, e ele existe para o
# Gui poder VOLTAR de Galar: a travessia liga Galar ao barco atras de flag de
# teste (PLANO-OBRAS-GALAR.md, decisao 12) e sem marinheiro do lado de la a
# viagem seria de mao unica. Ele reusa o menu de destinos que os outros cinco
# portos ja usam (data/scripts/travessia_regioes.inc), entao Galar entra e sai
# pelas mesmas regras, sem `case` novo em porto nenhum.
# O tile (23,17) de Wedgehurst05 foi MEDIDO no blockdata: colisao 0, elevacao 3,
# comportamento MB_NORMAL, sem warp e sem objeto da fonte em cima, e o jogador
# desembarca colado nele em (23,18), tambem elevacao 3.
OBJETOS_A_MAO = {
    "MAP_GALAR_WEDGEHURST_05": [{
        "motivo": "marinheiro da travessia (G5); NPC de obra, nao vem da fonte",
        "objeto": {
            "graphics_id": "OBJ_EVENT_GFX_SAILOR",
            "x": 23, "y": 17, "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
            "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0",
            "script": "Travessia_EventScript_MarinheiroGalar",
            "flag": "0",
        },
    }],
}
MARCA_INICIO = "// >>> G4 Galar, itens escondidos (dev_scripts/gente_galar.py) >>>"
MARCA_FIM = "// <<< G4 Galar, itens escondidos <<<"

BG_HIDDEN_ITEM = 7            # BG_EVENT_HIDDEN_ITEM, igual nos dois motores
MOV_BERRY_TREE = 0x0C
MOV_INVISIVEL = 0x4C
CURA_X, CURA_Y = 7, 4         # DEFAULT_POKEMON_CENTER_X/Y, ver item 10 do G3

# Os dois tetos de objeto por mapa, os MESMOS do `estaticos_galar.py` e do
# `distribui_dex.py`. Do 16o template dentro de uma janela de sprite o motor
# desiste CALADO, entao acrescentar objeto sem cobrar os dois seria gravar
# fantasma que nenhuma compilacao acusa.
TETO_OBJETOS = 64             # OBJECT_EVENT_TEMPLATES_COUNT
JANELA_SPRITE = (20, 17)      # TrySpawnObjectEvents, com MAP_OFFSET 7
TETO_SPRITE = 15              # OBJECT_EVENTS_COUNT - 1 (o jogador)

# Comandos da fonte que marcam encontro estatico. Ver o filtro 6 do docstring.
CMD_ENCONTRO = ("setwildbattle", "seteventmon")

# Traducao de movimento do fim do enum. Ver o docstring.
MOV_SUBSTITUTO = {
    0x44: "MOVEMENT_TYPE_JOG_IN_PLACE_DOWN",
    0x45: "MOVEMENT_TYPE_JOG_IN_PLACE_UP",
    0x46: "MOVEMENT_TYPE_JOG_IN_PLACE_LEFT",
    0x47: "MOVEMENT_TYPE_JOG_IN_PLACE_RIGHT",
    0x48: "MOVEMENT_TYPE_RUN_IN_PLACE_DOWN",
    0x49: "MOVEMENT_TYPE_RUN_IN_PLACE_UP",
    0x4A: "MOVEMENT_TYPE_RUN_IN_PLACE_LEFT",
    0x4B: "MOVEMENT_TYPE_RUN_IN_PLACE_RIGHT",
    0x4D: "MOVEMENT_TYPE_FACE_DOWN",
    0x4E: "MOVEMENT_TYPE_FACE_DOWN",
    0x4F: "MOVEMENT_TYPE_FACE_DOWN",
}


def constantes(caminho, prefixo):
    """valor -> nome, para um header de #define NOME valor."""
    fora = {}
    for m in re.finditer(rf"^#define\s+({prefixo}[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)\s*$",
                         open(caminho).read(), re.M):
        fora[int(m.group(2), 0)] = m.group(1)
    return fora


_CACHE = {}


def nossos_movimentos():
    if "mov" not in _CACHE:
        _CACHE["mov"] = constantes(f"{RAIZ}/include/constants/event_object_movement.h",
                                   "MOVEMENT_TYPE_")
    return _CACHE["mov"]


def nossos_itens():
    if "itens" not in _CACHE:
        _CACHE["itens"] = set(re.findall(r"\b(ITEM_[A-Z0-9_]+)\b",
                                         open(f"{RAIZ}/include/constants/items.h").read()))
    return _CACHE["itens"]


def itens_da_fonte():
    """id do FireRed -> nome do item no FireRed."""
    if "fr_itens" not in _CACHE:
        caminho = f"{PKFR}/include/constants/items.h"
        _CACHE["fr_itens"] = constantes(caminho, "ITEM_") if os.path.exists(caminho) else {}
    return _CACHE["fr_itens"]


def movimento(valor):
    nomes = nossos_movimentos()
    if valor in MOV_SUBSTITUTO:
        return MOV_SUBSTITUTO[valor]
    return nomes.get(valor, "MOVEMENT_TYPE_NONE")


# ---------------------------------------------------------------- leitura ----

def carrega():
    """(por_chave, de_para). por_chave[g00m06] = dict com objetos e bg limpos."""
    if "fonte" in _CACHE:
        return _CACHE["fonte"]
    grupos = json.load(open(f"{FONTE}/mapas.json"))
    sujeira = json.load(open(f"{FONTE}/galar_sujeira.json"))
    de_para = json.load(open(CENSO_MUNDO))["de_para"]
    rejeitados = collections.defaultdict(set)
    for r in sujeira["reprovados"]:
        rejeitados[(r["mapa"], r["tipo"])].add(r["i"])

    por_chave = {}
    _CACHE["warp_bruto"] = {}
    for g in grupos:
        for i, m in enumerate(g["mapas"]):
            if not m.get("novo"):
                continue
            chave = "g%02dm%02d" % (g["grupo"], i)
            por_chave[chave] = {
                "objetos": [(j, o) for j, o in enumerate(m.get("objetos", []))
                            if j not in rejeitados[(chave, "objetos")]],
                "bg": [(j, b) for j, b in enumerate(m.get("bg_events", []))
                       if j not in rejeitados[(chave, "bg")]],
            }
            _CACHE["warp_bruto"][chave] = [
                w for j, w in enumerate(m.get("warps", []))
                if j not in rejeitados[(chave, "warps")]]
    _CACHE["fonte"] = (por_chave, de_para)
    return _CACHE["fonte"]


def blockdata(chave):
    if chave not in _CACHE.setdefault("bd", {}):
        _CACHE["bd"][chave] = open(f"{FONTE}/blockdata/{chave}.bin", "rb").read()
    return _CACHE["bd"][chave]


def andavel(chave, w, h, x, y):
    if not (0 <= x < w and 0 <= y < h):
        return False
    bd = blockdata(chave)
    o = (y * w + x) * 2
    if o + 2 > len(bd):
        return False
    return ((struct.unpack_from("<H", bd, o)[0] >> 10) & 3) == 0


def tiles_de_cura():
    """{MAP_*: (x, y)} das heal locations que o G3 gravou."""
    if "cura" not in _CACHE:
        doc = json.load(open(CENSO_MUNDO))
        _CACHE["cura"] = {h["map"]: (h["x"], h["y"])
                          for h in doc.get("heal_locations", [])}
    return _CACHE["cura"]


def chaves_do_c5():
    """{(chave, indice)} dos objetos cujo script da fonte tem encontro estatico.

    Filtro 6 do docstring. A leitura e a MESMA que o `estaticos_galar.py` faz
    (mesmo decodificador, mesma ROM, mesma tabela de opcodes), para os dois
    lados da regra nunca discordarem sobre quem e o dono da linha.

    Importa `fala_galar`/`cenas_galar` DE DENTRO da funcao de proposito: o
    `mundo_galar.py` importa este arquivo e nao pode herdar um ciclo de import,
    e quem so quer o censo nao precisa carregar a ROM.
    """
    if "c5" in _CACHE:
        return _CACHE["c5"]
    import fala_galar as FALA                     # noqa: E402
    import cenas_galar as C3                      # noqa: E402
    if not os.path.exists(FALA.ROM_FONTE):
        raise SystemExit(
            "PARE: %s nao existe, e sem a ROM da fonte nao da para saber quais "
            "objetos sao encontro estatico do c5. Rodar assim gravaria centenas "
            "de Pokemon MUDOS por cima dos encontros jogaveis." % FALA.ROM_FONTE)
    rom = open(FALA.ROM_FONTE, "rb").read()
    tab = FALA.tabela_de_opcodes()
    por_chave, de_para = carrega()
    fora = set()
    for chave in sorted(por_chave):
        if chave not in de_para:
            continue
        for j, o in por_chave[chave]["objetos"]:
            ptr = str(o.get("script") or "0")
            if ptr in ("0", "0x0", "0x00000000"):
                continue
            try:
                ins, _falha = C3.blocos(rom, tab, int(ptr, 16))
            except Exception:
                continue
            nomes = {n for b in ins for n, _a in b.ins}
            if nomes & set(CMD_ENCONTRO):
                fora.add((chave, j))
    _CACHE["c5"] = fora
    return fora


def warps_limpos(chave):
    """(x, y) dos warps que o G0 aprovou; e a mesma lista que o G3 gravou."""
    if chave not in _CACHE.setdefault("warps", {}):
        _CACHE["warps"][chave] = {(w["x"], w["y"])
                                  for w in _CACHE["warp_bruto"].get(chave, [])}
    return _CACHE["warps"][chave]


# ------------------------------------------------------------- construcao ----

def _flags_dos_itens():
    """{(chave, indice_bg): (nome_da_flag, ITEM_*)}, alocado em ordem estavel.

    Ordem: chave da fonte, depois indice do bg. Nao depende do nome nosso (que a
    renomeacao do G3 pode mudar), entao rodar de novo nao renumera flag.
    """
    if "flags" in _CACHE:
        return _CACHE["flags"]
    por_chave, de_para = carrega()
    fr = itens_da_fonte()
    nossos = nossos_itens()
    fora, pendentes = {}, []
    prox = PRIMEIRA_FLAG
    vistos = collections.Counter()
    for chave in sorted(por_chave):
        if chave not in de_para:
            continue
        nome_mapa = de_para[chave]["mapa"].replace("MAP_GALAR_", "")
        for j, b in por_chave[chave]["bg"]:
            if b.get("kind") != BG_HIDDEN_ITEM:
                continue
            bruto = b.get("item", 0)
            nome_fr = fr.get(bruto)
            if not bruto or not nome_fr or nome_fr not in nossos:
                pendentes.append((chave, j, bruto, nome_fr))
                continue
            while prox in RESERVADAS_A_MAO:
                prox += 1
            if prox > ULTIMA_FLAG:
                pendentes.append((chave, j, bruto, "faixa de flag esgotada"))
                continue
            curto = nome_fr.replace("ITEM_", "")
            base = "FLAG_ITEM_GALAR_%s_%s" % (nome_mapa, curto)
            vistos[base] += 1
            nome = base if vistos[base] == 1 else "%s_%d" % (base, vistos[base])
            fora[(chave, j)] = (nome, nome_fr, prox)
            prox += 1
    _CACHE["flags"] = (fora, pendentes)
    return _CACHE["flags"]


def eventos_do_mapa(chave, w, h, nome_mapa=None):
    """(object_events, bg_events, linhas_de_censo) de UM mapa, ja em JSON nosso."""
    por_chave, _ = carrega()
    dados = por_chave.get(chave)
    if dados is None:
        return [], [], []
    flags, _pend = _flags_dos_itens()
    ocupado_por_warp = warps_limpos(chave)
    cura = tiles_de_cura().get(nome_mapa)
    nomes_mov = nossos_movimentos()

    objetos, bgs, censo = [], [], []
    for j, o in dados["objetos"]:
        gid = o["grafico"]
        sprite, cat, papel = G.traduz(gid)
        base = {"mapa": chave, "tipo": "objeto", "i": j, "gfx": gid,
                "x": o["x"], "y": o["y"], "papel": papel,
                "script_fonte": o.get("script"),
                "trainer_type_fonte": o.get("trainer_type", 0),
                "flag_fonte": o.get("flag", 0)}
        if sprite is None:
            censo.append(dict(base, motivo="grafico e %s, nao vira NPC" % cat))
            continue
        if cat == "pokemon" and (chave, j) in chaves_do_c5():
            # Filtro 6: o dono e o c5. Ver o docstring.
            censo.append(dict(base, motivo="encontro estatico: o dono e o c5 "
                                           "(estaticos_galar.py), nao o G4"))
            continue
        mov = o.get("movimento", 0)
        if mov in (MOV_INVISIVEL, MOV_BERRY_TREE):
            censo.append(dict(base, motivo="movimento %s precisa de cena"
                                            % nomes_mov.get(mov, hex(mov))))
            continue
        if not andavel(chave, w, h, o["x"], o["y"]):
            censo.append(dict(base, motivo="tile nao andavel (NPC estacionado na fonte)"))
            continue
        if (o["x"], o["y"]) in ocupado_por_warp:
            censo.append(dict(base, motivo="em cima de tile de warp; trancaria a porta"))
            continue
        if cura and (o["x"], o["y"]) == cura:
            censo.append(dict(base, motivo="em cima do tile de cura do heal location"))
            continue
        elev = o.get("elevacao", 0)
        nota_elev = ""
        if elev > 15:
            nota_elev = "elevacao %d da fonte nao cabe em 4 bits; virou 0" % elev
            elev = 0
        objetos.append({
            "graphics_id": sprite,
            "x": o["x"], "y": o["y"], "elevation": elev,
            "movement_type": movimento(mov),
            "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0",
            "script": "0",
            "flag": "0",
        })
        # G5: o ponteiro de script da fonte TAMBEM manda anotar. Antes so
        # trainer_type/flag/elevacao geravam linha, e por isso 671 NPCs que
        # entraram mudos COM cena na fonte nao apareciam em censo nenhum: a
        # `fila_galar.py` cobrava 1.970 quando a fonte tem 2.641. Censo que nao
        # ve o trabalho faz a fila mentir para baixo.
        tem_script = str(o.get("script") or "0") not in ("0", "0x0", "0x00000000")
        if o.get("trainer_type") or o.get("flag") or nota_elev or tem_script:
            censo.append(dict(base, motivo="entrou mudo",
                              anotacao=(nota_elev or "script/trainer_type/flag da "
                                        "fonte guardados para a fase de conteudo")))

    for j, b in dados["bg"]:
        kind = b.get("kind")
        base = {"mapa": chave, "tipo": "bg", "i": j, "kind": kind,
                "x": b.get("x"), "y": b.get("y")}
        if kind != BG_HIDDEN_ITEM:
            if kind is not None and kind <= 4:
                censo.append(dict(base, motivo="placa/script sem script; fase de conteudo",
                                  script_fonte=b.get("script")))
            else:
                censo.append(dict(base, motivo="kind %s nao existe em nenhum dos dois "
                                               "motores; lixo de leitura" % kind))
            continue
        achado = flags.get((chave, j))
        if achado is None:
            censo.append(dict(base, motivo="item escondido sem item traduzivel",
                              item_fonte=b.get("item")))
            continue
        nome_flag, item, _end = achado
        bgs.append({
            "type": "hidden_item",
            "x": b["x"], "y": b["y"], "elevation": 0,
            "item": item, "flag": nome_flag,
            "quantity": 1, "underfoot": False,
        })
    for extra in OBJETOS_A_MAO.get(nome_mapa or "", []):
        # APPEND no FIM da lista, sempre: a save guarda indice de object_event
        # (`objectEvents[]`/`objectEventTemplates[]`), entao NPC novo so entra
        # depois de todos os que a fonte deu. Ver ESTADO, "Compatibilidade de save".
        objetos.append(dict(extra["objeto"]))
        censo.append({"mapa": chave, "tipo": "objeto", "i": len(objetos) - 1,
                      "x": extra["objeto"]["x"], "y": extra["objeto"]["y"],
                      "papel": "a mao", "motivo": extra["motivo"]})
    return objetos, bgs, censo


def constroi():
    """Roda os 438 e devolve (por_chave, censo, resumo)."""
    por_chave, de_para = carrega()
    total = collections.Counter()
    censo = []
    saida = {}
    for chave in sorted(por_chave):
        dp = de_para.get(chave)
        if dp is None:
            continue
        objs, bgs, linhas = eventos_do_mapa(chave, dp["w"], dp["h"], dp["mapa"])
        saida[chave] = (objs, bgs)
        censo.extend(linhas)
        total["objetos"] += len(objs)
        total["itens"] += len(bgs)
    for l in censo:
        total["censo_" + (l.get("motivo", "?").split(";")[0][:24])] += 1
    return saida, censo, total


# ---------------------------------------------------------------- gravar -----

def bloco_flags():
    flags, pendentes = _flags_dos_itens()
    linhas = [MARCA_INICIO,
              "// DONO DA FAIXA 0x1C00 em diante: a obra de Galar",
              "// (PLANO-OBRAS-GALAR.md, decisao 6). Uma flag por item escondido",
              "// dos bg events limpos da fonte, na ordem da chave da fonte.",
              "// Gerado por dev_scripts/gente_galar.py; nao editar a mao.",
              "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT, entao nao invalida save."]
    largura = max([len(n) for n, _, _ in flags.values()] or [40])
    for (_chave, _j), (nome, item, end) in sorted(flags.items(), key=lambda t: t[1][2]):
        linhas.append("#define %-*s FLAG_UNUSED_0x%04X  // %s"
                      % (largura, nome, end, item))
    linhas.append(MARCA_FIM)
    return "\n".join(linhas) + "\n"


def escreve_flags(gravar):
    texto = open(FLAGS_H).read()
    bloco = bloco_flags()
    if MARCA_INICIO in texto:
        novo = re.sub(re.escape(MARCA_INICIO) + r".*?" + re.escape(MARCA_FIM) + r"\n",
                      bloco, texto, flags=re.S)
    else:
        # Antes do #endif final do header.
        corte = texto.rstrip().rfind("#endif")
        novo = texto[:corte] + "\n" + bloco + "\n" + texto[corte:]
    if gravar and novo != texto:
        with open(FLAGS_H, "w") as f:
            f.write(novo)
    return novo != texto


def escreve_censo(censo, total, gravar):
    flags, pendentes = _flags_dos_itens()
    _por, de_para = carrega()
    doc = {
        "gerado_por": "dev_scripts/gente_galar.py",
        "fonte": "demake Sword and Shield Ultimate Plus v1.2.1.2 (FireRed)",
        "objetos_gravados": total["objetos"],
        "itens_gravados": total["itens"],
        "faixa_de_flag": {"primeira": "0x%04X" % PRIMEIRA_FLAG,
                          "ultima_usada": "0x%04X" % (PRIMEIRA_FLAG + len(flags) - 1)
                          if flags else None,
                          "consumidas": len(flags),
                          "teto_da_faixa": "0x%04X" % ULTIMA_FLAG},
        "itens": [{"mapa_fonte": c, "bg": j, "mapa": de_para.get(c, {}).get("mapa"),
                   "item": item, "flag": nome, "endereco": "0x%04X" % end}
                  for (c, j), (nome, item, end) in sorted(flags.items(),
                                                          key=lambda t: t[1][2])],
        "itens_pendentes": [{"mapa": c, "bg": j, "item_fonte": it, "nome_fonte": n}
                            for c, j, it, n in pendentes],
        "linhas": censo,
    }
    if gravar:
        with open(CENSO, "w") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return doc


# ------------------------------------------------------------------ demo -----

def demo():
    falhas = []
    probs = G.confere()
    if probs:
        falhas += ["tabela de gfx: " + p for p in probs]

    # 1. os dois enums de movimento sao o mesmo de 0x00 a 0x43.
    caminho_fr = f"{PKFR}/include/constants/event_object_movement.h"
    if os.path.exists(caminho_fr):
        fr = constantes(caminho_fr, "MOVEMENT_TYPE_")
        nosso = nossos_movimentos()
        difs = [v for v in range(0x00, 0x44) if fr.get(v) != nosso.get(v)]
        if difs:
            falhas.append("enum de movimento diverge do FireRed em %s" % difs)
        print("movimento: 0x00-0x43 identico ao FireRed (%d valores conferidos)"
              % len(range(0x00, 0x44)))
    else:
        print("movimento: pokefirered ausente, identidade 0x00-0x43 NAO reconferida")
    for v, nome in MOV_SUBSTITUTO.items():
        if nome not in nossos_movimentos().values():
            falhas.append("substituto de movimento %s (0x%02X) nao existe aqui" % (nome, v))

    saida, censo, total = constroi()
    if total["objetos"] == 0:
        falhas.append("nenhum objeto gravado")

    # 2. nenhum objeto em tile nao andavel, em cima de warp, ou fora do mapa.
    _por, de_para = carrega()
    ruins = 0
    for chave, (objs, bgs) in saida.items():
        dp = de_para[chave]
        for o in objs:
            if not andavel(chave, dp["w"], dp["h"], o["x"], o["y"]):
                ruins += 1
    if ruins:
        falhas.append("%d objetos gravados em tile nao andavel" % ruins)

    # 2.b (G5) o censo VE todo objeto que a fonte mandou falar. Sem esta trava a
    # `fila_galar.py` conta menos trabalho do que existe, e cala.
    por_chave, de_para = carrega()
    na_fonte = sum(1 for chave in por_chave if chave in de_para
                   for _j, o in por_chave[chave]["objetos"]
                   if str(o.get("script") or "0") not in ("0", "0x0", "0x00000000"))
    _s, censo, _t = constroi()
    no_censo = sum(1 for l in censo if l.get("tipo") == "objeto"
                   and str(l.get("script_fonte") or "0") not in ("0", "0x0", "0x00000000"))
    if na_fonte != no_censo:
        falhas.append("censo ve %d objetos com script e a fonte tem %d"
                      % (no_censo, na_fonte))

    # 3. flags: contiguas, dentro da faixa, sem nome repetido.
    flags, pendentes = _flags_dos_itens()
    ends = sorted(e for _n, _i, e in flags.values())
    esperado = []
    prox = PRIMEIRA_FLAG
    while len(esperado) < len(ends):
        if prox not in RESERVADAS_A_MAO:
            esperado.append(prox)
        prox += 1
    if ends and ends != esperado:
        falhas.append("faixa de flag nao e contigua a partir de 0x%04X (pulando as "
                      "reservadas a mao)" % PRIMEIRA_FLAG)
    if set(ends) & set(RESERVADAS_A_MAO):
        falhas.append("o alocador entregou uma flag reservada a mao: %s"
                      % sorted(set(ends) & set(RESERVADAS_A_MAO)))
    if ends and ends[-1] > ULTIMA_FLAG:
        falhas.append("faixa de flag estourou 0x%04X" % ULTIMA_FLAG)
    nomes = [n for n, _i, _e in flags.values()]
    if len(set(nomes)) != len(nomes):
        falhas.append("nome de flag repetido")

    # 4. o item cabe nos 11 bits que o motor reserva (include/global.fieldmap.h).
    valores = constantes(f"{RAIZ}/include/constants/items.h", "ITEM_")
    por_nome = {v: k for k, v in valores.items()}
    grandes = [i for _n, i, _e in flags.values() if por_nome.get(i, 0) >= (1 << 11)]
    if grandes:
        falhas.append("itens com id >= 2048 nao cabem no bg event: %s" % grandes)

    # 5. idempotencia: rodar duas vezes da o mesmo bloco de flags.
    b1 = bloco_flags()
    _CACHE.pop("flags", None)
    _flags_dos_itens()
    if bloco_flags() != b1:
        falhas.append("bloco de flags nao e estavel entre rodadas")

    print("objetos gravados: %d | itens escondidos: %d | linhas de censo: %d"
          % (total["objetos"], total["itens"], len(censo)))
    print("flags consumidas: %d (0x%04X..0x%04X), itens pendentes: %d"
          % (len(flags), ends[0] if ends else 0, ends[-1] if ends else 0, len(pendentes)))
    if falhas:
        print("\nDEMO REPROVADO:")
        for f in falhas:
            print("  -", f)
        return 1
    print("\ndemo: OK")
    return 0


def conferir():
    saida, censo, total = constroi()
    flags, pendentes = _flags_dos_itens()
    motivos = collections.Counter(l["motivo"].split(";")[0] for l in censo)
    print("objetos gravados: %d" % total["objetos"])
    print("itens escondidos gravados: %d" % total["itens"])
    print("flags consumidas: %d de %d na faixa" % (len(flags), ULTIMA_FLAG - PRIMEIRA_FLAG + 1))
    print("\ncenso, por motivo:")
    for m, n in motivos.most_common():
        print("  %5d  %s" % (n, m))
    if pendentes:
        print("\nitens sem equivalente no nosso items.h: %d" % len(pendentes))
    cheios = sorted(((len(o), c) for c, (o, _b) in saida.items()), reverse=True)[:8]
    print("\nmapas com mais NPC:", ", ".join("%s(%d)" % (c, n) for n, c in cheios))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true")
    p.add_argument("--conferir", action="store_true")
    p.add_argument("--gravar", action="store_true")
    a = p.parse_args()
    if a.demo:
        return demo()
    if a.conferir:
        conferir()
        return 0
    if a.gravar:
        saida, censo, total = constroi()
        mudou = escreve_flags(True)
        escreve_censo(censo, total, True)
        flags, pendentes = _flags_dos_itens()
        print("flags.h %s; %d flags de item" % ("atualizado" if mudou else "sem mudanca",
                                                len(flags)))
        print("censo em %s (%d linhas)" % (CENSO, len(censo)))
        print("agora rode: python3 dev_scripts/mundo_galar.py --gravar")
        return 0
    conferir()
    return 0


if __name__ == "__main__":
    sys.exit(main())
