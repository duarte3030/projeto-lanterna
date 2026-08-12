#!/usr/bin/env python3
"""B1.b: as 20 salas sorteadas da Turnback Cave, com o sorteio em script.

    python3 dev_scripts/turnback_cave_sinnoh.py            # so relata
    python3 dev_scripts/turnback_cave_sinnoh.py --aplicar  # escreve
    python3 dev_scripts/turnback_cave_sinnoh.py --demo     # autoteste

Como o Platinum faz, lido do decomp e nao de memoria
----------------------------------------------------
`src/scrcmd.c:6089`, `ScrCmd_InitTurnbackCave(pillarsSeen, roomsVisited)`. Toda
sala da Turnback Cave tem QUATRO warps, nas mesmas quatro coordenadas
((11,1), (20,11), (11,20), (2,11)), e ao entrar o comando **reescreve o destino
dos tres warps por onde o jogador NAO entrou**, todos para o mesmo destino
sorteado:

1. `pillarsSeen >= 3`  -> sala da Giratina;
2. senao `roomsVisited >= 30` -> Entrance, ou seja o jogo expulsa;
3. senao 25% -> `PILLAR_ROOM`, a sala que tem o pilar;
4. senao -> `pillarRooms[rand % 6 + pillarsSeen * 6]`, um dos seis quartos do
   nivel de pilar atual.

E por isso que nenhuma delas e destino de warp ESTATICO na fonte, e por isso o
conversor de caverna dava zero aqui: nao faltava geometria, faltava o sorteio.

Como fica no GBA, sem inventar mecanica
---------------------------------------
O pokeemerald ja tem a mesma peca, e ela e nativa: warp cujo destino e
`MAP_DYNAMIC` cai em `gSaveBlock1Ptr->dynamicWarp`
(`SetupWarp` -> `SetWarpDestinationToDynamicWarp`, `src/field_control_avatar.c`),
e o script escreve esse destino com `setdynamicwarp`. Entao as quatro portas de
cada sala sao warps normais com destino `MAP_DYNAMIC`, e um `MAP_SCRIPT_ON_TRANSITION`
roda o sorteio quando o mapa carrega, ANTES de o jogador pisar em qualquer porta.
Nada de `coord_event`: porta continua sendo porta, e nao ha risco de o gatilho
disparar em cima do tile onde o jogador acabou de aparecer.

`setdynamicwarp` guarda UM destino, entao as quatro portas de uma sala levam ao
mesmo lugar e o jogador chega sempre pela porta 0 (a do norte). No Platinum cada
porta guarda o `dest_warp_id` da porta oposta, o que faria sair pelo lado
"certo". Nao da para reproduzir com um slot so, e o efeito e invisivel: as salas
sao um labirinto sorteado e todas as quatro portas de uma sala levam ao MESMO
destino tambem la.
    ponytail: chegar sempre pela porta 0 e a simplificacao; so vale trocar se
    algum dia existir um dynamicWarp por porta, e isso e mexer no motor.

Cinco layouts, vinte e um mapas
-------------------------------
Medido com hash da grade 2D, nao suposto: as 18 salas de pilar sao **tres**
grades distintas, cada uma repetida seis vezes (rooms 1 e 2 de cada nivel sao
iguais entre si, idem 3 e 4, idem 5 e 6). Com a `PILLAR_ROOM` e a sala da
Giratina dao 5 layouts para 21 headers. Os 21 headers entram porque a fonte tem
os 21 e `completude.py` conta header; o blockdata e que nao precisa ser copiado
16 vezes, e com a ROM em 95% isso importa (2 KB por layout de 32x32). Sao 20
mapas NOVOS: a `TURNBACK_CAVE_ENTRANCE`, que e a vigesima primeira sala, ja esta
na ROM desde 06/08 e aqui so troca o destino das quatro portas dela.

Alcance a pe, e como ele e PROVADO
----------------------------------
`valida_conectividade.py` anda pelo grafo de warp estatico, e warp `MAP_DYNAMIC`
nao tem destino escrito: sem ajuda, as 21 salas apareceriam como "nenhum caminho
alcanca" mesmo estando alcancaveis no jogo. A ajuda e DADO, nao regra escondida:
cada mapa novo grava em `destinos_dinamicos` a lista de para onde as portas dele
podem mandar, e o validador soma essa lista aos vizinhos. O `--demo` exige que
essa lista seja EXATAMENTE o conjunto de `setdynamicwarp` do script gerado, senao
a lista viraria uma segunda verdade que envelhece calada.

Compatibilidade de save: mapa novo no FIM de um grupo com vaga, layout novo no
FIM de `layouts.json`, var nova numa faixa livre, e no `TurnbackCaveEntrance`,
que ja esta na ROM, NENHUM warp e criado ou movido: os quatro que ja existiam
(e que apontavam para o proprio mapa, ou seja nao levavam a lugar nenhum) so
trocam de destino.
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import converte_cavernas_sinnoh as C     # noqa: E402
import fecha_portas_sinnoh as F          # noqa: E402
import importa_npcs_sinnoh as I          # noqa: E402
import valida_mapas_sinnoh as V          # noqa: E402
import valida_warp_tile as W             # noqa: E402

APLICAR = "--aplicar" in sys.argv
GRUPO = "gMapGroup_SinnohCavernas"
ENTRADA = "TurnbackCaveEntrance"
ARQ_SCRIPT = f"{REPO}/data/scripts/turnback_cave.inc"

# Var da faixa liberada pelo condutor (0x41C0 e 0x41C1). A faixa 0x4100-0x41BF
# esta com os tres agentes do B6 e nao se encosta nela.
VARS = [("VAR_TURNBACK_PILARES_VISTOS", "VAR_UNUSED_0x41C0", 0x41C0),
        ("VAR_TURNBACK_SALAS_VISITADAS", "VAR_UNUSED_0x41C1", 0x41C1)]

PILARES, SALAS = VARS[0][0], VARS[1][0]
LIMITE_PILARES = 3      # `pillarsSeen >= 3` no scrcmd do Platinum
LIMITE_SALAS = 30       # `roomsVisited >= 30`
CHANCE_PILAR = 25       # `LCRNG_Next() % 100 < 25`

GIRATINA = "MAP_HEADER_TURNBACK_CAVE_GIRATINA_ROOM"
PILAR = "MAP_HEADER_TURNBACK_CAVE_PILLAR_ROOM"


def salas_de_pilar():
    """Os 18 headers de quarto, na ordem do vetor `pillarRooms` do Platinum."""
    return [f"MAP_HEADER_TURNBACK_CAVE_PILLAR_{p}_ROOM_{r}"
            for p in (1, 2, 3) for r in (1, 2, 3, 4, 5, 6)]


def todos():
    return salas_de_pilar() + [PILAR, GIRATINA]


# ------------------------------------------------------------------ grades
def grades():
    """header -> assinatura da grade 2D. Layout e compartilhado por assinatura.

    A assinatura sai da grade CRUA do DS, nao do nome: contar com o nome faria a
    ferramenta acreditar que ha 18 plantas onde a fonte tem 3.
    """
    saida = {}
    for h in todos():
        _l, _a, g = C.grade_do_header(h)
        saida[h] = hash(tuple(g))
    return saida


def donos():
    """assinatura -> header cujo nome batiza o layout (o primeiro da ordem)."""
    ass = grades()
    dono = {}
    for h in todos():
        dono.setdefault(ass[h], h)
    return {h: dono[ass[h]] for h in todos()}


# ------------------------------------------------------------------ script
def rotulo(header):
    return F.nome_de_pasta(header)


def sorteio():
    """O trecho de `data/scripts/turnback_cave.inc`, e a lista de destinos.

    Devolve (texto, {mapa nosso -> destinos que o sorteio pode dar}).
    """
    quartos = salas_de_pilar()
    const = {h: F.const_do_header(h) for h in todos()}
    ent = "MAP_TURNBACK_CAVE_ENTRANCE"
    t = []
    t.append("@ Turnback Cave: o sorteio de sala.\n"
             "@ Gerado por dev_scripts/turnback_cave_sinnoh.py, que explica no topo\n"
             "@ de onde cada regra saiu (src/scrcmd.c:6089 do pokeplatinum).\n"
             "@ A porta e warp normal com destino MAP_DYNAMIC; quem decide para onde\n"
             "@ ela leva e o `setdynamicwarp` que roda no ON_TRANSITION da sala.\n")
    t.append("TurnbackCave_OnTransitionEntrada::\n"
             f"\tsetvar {PILARES}, 0\n"
             f"\tsetvar {SALAS}, 0\n"
             "\tgoto TurnbackCave_Sorteia\n\tend\n")
    t.append("TurnbackCave_OnTransitionSala::\n"
             f"\taddvar {SALAS}, 1\n"
             "\tgoto TurnbackCave_Sorteia\n\tend\n")
    t.append("@ A sala do pilar e a unica que conta pilar. Tres pilares abrem a\n"
             "@ sala da Giratina, que e a regra 1 do scrcmd.\n"
             "TurnbackCave_OnTransitionPilar::\n"
             f"\taddvar {SALAS}, 1\n"
             f"\taddvar {PILARES}, 1\n"
             "\tgoto TurnbackCave_Sorteia\n\tend\n")
    t.append("@ Da sala da Giratina so se sai para a entrada.\n"
             "TurnbackCave_OnTransitionGiratina::\n"
             f"\tsetdynamicwarp {ent}, 0\n\tend\n")
    t.append("TurnbackCave_Sorteia::\n"
             f"\tgoto_if_ge {PILARES}, {LIMITE_PILARES}, TurnbackCave_ParaGiratina\n"
             f"\tgoto_if_ge {SALAS}, {LIMITE_SALAS}, TurnbackCave_ParaEntrada\n"
             f"\trandom 100\n"
             f"\tgoto_if_lt VAR_RESULT, {CHANCE_PILAR}, TurnbackCave_ParaPilar\n"
             f"\tswitch {PILARES}\n"
             "\tcase 1, TurnbackCave_Nivel2\n"
             "\tcase 2, TurnbackCave_Nivel3\n"
             "\tgoto TurnbackCave_Nivel1\n\tend\n")
    t.append("TurnbackCave_ParaGiratina::\n"
             f"\tsetdynamicwarp {const[GIRATINA]}, 0\n\tend\n")
    t.append("TurnbackCave_ParaEntrada::\n"
             f"\tsetdynamicwarp {ent}, 0\n\tend\n")
    t.append("TurnbackCave_ParaPilar::\n"
             f"\tsetdynamicwarp {const[PILAR]}, 0\n\tend\n")
    for nivel in (1, 2, 3):
        seis = quartos[(nivel - 1) * 6:nivel * 6]
        corpo = [f"TurnbackCave_Nivel{nivel}::", "\trandom 6", "\tswitch VAR_RESULT"]
        for i, h in enumerate(seis[:-1]):
            corpo.append(f"\tcase {i}, TurnbackCave_Nivel{nivel}Sala{i}")
        corpo.append(f"\tsetdynamicwarp {const[seis[-1]]}, 0")
        corpo.append("\tend")
        for i, h in enumerate(seis[:-1]):
            corpo.append(f"\nTurnbackCave_Nivel{nivel}Sala{i}::")
            corpo.append(f"\tsetdynamicwarp {const[h]}, 0")
            corpo.append("\tend")
        t.append("\n".join(corpo) + "\n")
    texto = "\n".join(t)

    # de cada mapa, para onde as portas dele podem levar. Sai da MESMA tabela
    # que gera o script; o --demo confere que os dois batem.
    quartos_por_nivel = [quartos[0:6], quartos[6:12], quartos[12:18]]
    saida = {}
    for h in todos():
        if h == GIRATINA:
            saida[F.nome_de_pasta(h)] = [ent]
            continue
        # da entrada e de qualquer quarto o sorteio alcanca, ao longo de uma
        # partida, os tres niveis, a sala do pilar, a Giratina e a saida
        alvos = [ent, const[PILAR], const[GIRATINA]]
        alvos += [const[x] for grupo in quartos_por_nivel for x in grupo]
        saida[F.nome_de_pasta(h)] = alvos
    saida[ENTRADA] = [const[PILAR], const[GIRATINA]] + \
        [const[x] for grupo in quartos_por_nivel for x in grupo]
    return texto, saida


# ------------------------------------------------------------------- vars
def poe_vars():
    """Apelida as duas VAR_UNUSED da faixa liberada, RELENDO o arquivo antes.

    Releitura obrigatoria: os agentes do B6 escrevem no mesmo arquivo, e uma
    copia carregada no comeco da ferramenta apagaria o que eles puseram no meio.
    """
    caminho = f"{REPO}/include/constants/vars.h"
    texto = open(caminho).read()
    novas = []
    for nome, ancora, valor in VARS:
        if re.search(rf"#define\s+{nome}\b", texto):
            continue
        m = re.search(rf"(#define\s+{ancora}\s+0x[0-9A-Fa-f]+.*\n)", texto)
        if not m:
            raise SystemExit(f"ancora {ancora} nao esta mais em vars.h")
        linha = f"#define {nome:40} 0x{valor:04X} // Turnback Cave, B1.b\n"
        texto = texto[:m.end()] + linha + texto[m.end():]
        novas.append(nome)
    if novas:
        open(caminho, "w").write(texto)
    return novas


# ---------------------------------------------------------------- escrita
def escreve_layout(pasta, header, larg, alt, palavras):
    d = f"{REPO}/data/layouts/{pasta}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/map.bin", "wb").write(struct.pack(f"<{len(palavras)}H", *palavras))
    open(f"{d}/border.bin", "wb").write(struct.pack("<4H", *([C.ROCHA_TOPO] * 4)))
    return {
        "id": "LAYOUT_" + F.const_do_header(header)[len("MAP_"):],
        "name": f"{pasta}_Layout", "width": larg, "height": alt,
        "primary_tileset": "gTileset_GeneralSinnoh",
        "secondary_tileset": "gTileset_CaveSinnoh",
        "border_filepath": f"data/layouts/{pasta}/border.bin",
        "blockdata_filepath": f"data/layouts/{pasta}/map.bin",
        "layout_version": "emerald",
    }


def registra_layout(lay):
    arq = f"{REPO}/data/layouts/layouts.json"
    todos_lay = json.load(open(arq))
    todos_lay["layouts"].append(lay)
    json.dump(todos_lay, open(arq, "w"), indent=2, ensure_ascii=False)
    F.layouts()[lay["id"]] = lay


def pendentes():
    pastas = set(os.listdir(f"{REPO}/data/maps"))
    return [h for h in todos() if F.nome_de_pasta(h) not in pastas]


def main():
    if "--demo" in sys.argv:
        return demo()

    heads = I.headers_do_platinum()
    pend = pendentes()
    dono = donos()
    print(f"salas sorteadas que faltam: {len(pend)} de {len(todos())} novas "
          f"(a 21a, a entrada, ja esta na ROM)")
    print(f"layouts distintos necessarios: {len(set(dono.values()))}")
    for h in pend:
        _l, _a, g = C.grade_do_header(h)
        print(f"   {h.replace('MAP_HEADER_', ''):40} layout de "
              f"{dono[h].replace('MAP_HEADER_TURNBACK_CAVE_', '')}, "
              f"{C.chao_de_caverna(g)} tiles de chao de masmorra")
    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        return 0

    novas_vars = poe_vars()
    texto, dinamicos = sorteio()
    os.makedirs(os.path.dirname(ARQ_SCRIPT), exist_ok=True)
    open(ARQ_SCRIPT, "w").write(texto)

    sprites = V.sprites_utilizaveis()
    movimentos = V.constantes("include/constants/event_object_movement.h",
                              "MOVEMENT_TYPE_")
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    F.grupo_com_vaga(grupos, GRUPO)
    modelo = json.load(open(f"{REPO}/data/maps/{ENTRADA}/map.json"))
    incs, feitos = [], 0
    layouts_feitos = {}

    for header in pend:
        pasta = F.nome_de_pasta(header)
        larg, alt, g = C.grade_do_header(header)
        d_dono = dono[header]
        if d_dono not in layouts_feitos:
            pal = list(C.traduz(larg, alt, g))
            regiao = C.regiao_principal(pal, larg, alt)
            portas = []
            arq = os.path.join(C.PLAT, "res/field/events",
                               heads[d_dono][0] + ".json")
            for wp in json.load(open(arq)).get("warp_events", []):
                x, y = C.poe_warp(regiao, larg, int(wp["x"]), int(wp["z"]))
                if (x, y) in portas:
                    continue
                pal[y * larg + x] = C.ESCADA
                portas.append((x, y))
            lay = escreve_layout(F.nome_de_pasta(d_dono), d_dono, larg, alt, pal)
            registra_layout(lay)
            layouts_feitos[d_dono] = (lay, portas)
        lay, portas = layouts_feitos[d_dono]

        d = dict(modelo)
        d.pop("connections", None)
        d["id"] = F.const_do_header(header)
        d["name"] = pasta
        d["layout"] = lay["id"]
        # As quatro portas. Destino MAP_DYNAMIC: quem escolhe e o ON_TRANSITION.
        d["warp_events"] = [{"x": x, "y": y, "elevation": 0,
                             "dest_map": "MAP_DYNAMIC", "dest_warp_id": "0"}
                            for x, y in portas]
        d["coord_events"] = []
        objs, bg, trecho = F.conteudo_do_mapa(
            header, pasta, larg, alt, sprites, movimentos, lay["id"])
        d["object_events"] = objs
        d["bg_events"] = bg
        d["origem"] = ("pokeplatinum: geometria convertida da grade 2D "
                       "(map_data); as portas sao MAP_DYNAMIC e o sorteio esta "
                       "em data/scripts/turnback_cave.inc")
        d["destinos_dinamicos"] = dinamicos[pasta]
        os.makedirs(f"{REPO}/data/maps/{pasta}", exist_ok=True)
        json.dump(d, open(f"{REPO}/data/maps/{pasta}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        if header == GIRATINA:
            alvo = "TurnbackCave_OnTransitionGiratina"
        elif header == PILAR:
            alvo = "TurnbackCave_OnTransitionPilar"
        else:
            alvo = "TurnbackCave_OnTransitionSala"
        open(f"{REPO}/data/maps/{pasta}/scripts.inc", "w").write(
            f"{pasta}_MapScripts::\n"
            f"\tmap_script MAP_SCRIPT_ON_TRANSITION, {alvo}\n"
            f"\t.byte 0\n{trecho}")
        grupos[F.grupo_com_vaga(grupos, GRUPO)].append(pasta)
        incs.append(f'\t.include "data/maps/{pasta}/scripts.inc"\n')
        feitos += 1

    # A entrada JA esta na ROM: nenhum warp e criado nem movido, os quatro que
    # apontavam para o proprio mapa so trocam de destino.
    p_ent = f"{REPO}/data/maps/{ENTRADA}/map.json"
    d_ent = json.load(open(p_ent))
    trocados = 0
    for wp in d_ent["warp_events"]:
        if wp["dest_map"] == d_ent["id"]:
            wp["dest_map"], wp["dest_warp_id"] = "MAP_DYNAMIC", "0"
            trocados += 1
    d_ent["destinos_dinamicos"] = dinamicos[ENTRADA]
    json.dump(d_ent, open(p_ent, "w"), indent=2, ensure_ascii=False)
    inc_ent = f"{REPO}/data/maps/{ENTRADA}/scripts.inc"
    corpo = open(inc_ent).read()
    if "MAP_SCRIPT_ON_TRANSITION" not in corpo:
        corpo = corpo.replace(
            f"{ENTRADA}_MapScripts::\n\t.byte 0",
            f"{ENTRADA}_MapScripts::\n"
            "\tmap_script MAP_SCRIPT_ON_TRANSITION, "
            "TurnbackCave_OnTransitionEntrada\n\t.byte 0", 1)
        open(inc_ent, "w").write(corpo)

    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    # o include do sorteio entra UMA vez. Sem esta guarda a segunda rodada da
    # ferramenta (que nao cria mapa nenhum) o repetia, e include repetido e
    # simbolo repetido no montador: quebra a build sem criar mapa nenhum.
    linha_sorteio = '\t.include "data/scripts/turnback_cave.inc"\n'
    ja = linha_sorteio in open(f"{REPO}/data/event_scripts.s").read()
    with open(f"{REPO}/data/event_scripts.s", "a") as f:
        f.writelines(incs)
        if not ja:
            f.write(linha_sorteio)
    print(f"\naplicado: {feitos} salas, {len(layouts_feitos)} layouts, "
          f"{trocados} portas da entrada agora sorteiam, "
          f"vars novas: {', '.join(novas_vars) or 'nenhuma'}")
    return 0


# -------------------------------------------------------------- autoteste
def demo():
    """O que precisa ser verdade para o sorteio nao ser labirinto quebrado."""
    # 1. as 20 salas novas existem na fonte e TODAS convertem pelo motor de
    #    caverna.
    #    Se uma nao converter, ela entraria como sala vazia no meio do sorteio.
    for h in todos():
        _l, _a, g = C.grade_do_header(h)
        assert C.chao_de_caverna(g) >= 8, (h, C.chao_de_caverna(g))
    assert len(todos()) == 20, len(todos())   # a 21a sala, a entrada, ja esta na ROM

    # 2. as 18 salas de pilar sao TRES grades, nao dezoito. Medido por hash da
    #    grade crua. Se a fonte tivesse 18 plantas, copiar 3 seria mentira; como
    #    ela tem 3, copiar 18 seriam 30 KB de ROM a toa.
    ass = grades()
    assert len(set(ass[h] for h in salas_de_pilar())) == 3, "as 18 salas mudaram"
    assert len(set(donos().values())) == 5, "deviam ser 5 layouts"

    # 3. as quatro portas de toda sala estao nas MESMAS quatro coordenadas, que e
    #    o que deixa uma planta servir as seis salas do nivel.
    heads = I.headers_do_platinum()
    esperado = {(11, 1), (20, 11), (11, 20), (2, 11)}
    for h in todos():
        arq = os.path.join(C.PLAT, "res/field/events", heads[h][0] + ".json")
        p = {(int(w["x"]), int(w["z"]))
             for w in json.load(open(arq)).get("warp_events", [])}
        assert p == esperado, (h, p)

    # 4. o script cita as 20 salas novas, e a lista `destinos_dinamicos` e EXATAMENTE
    #    o conjunto de `setdynamicwarp` dele. Sem isto a lista viraria uma
    #    segunda verdade, e o validador de conectividade acreditaria nela.
    texto, dinamicos = sorteio()
    citados = set(re.findall(r"setdynamicwarp (MAP_[A-Z0-9_]+)", texto))
    consts = {F.const_do_header(h) for h in todos()}
    assert consts <= citados, consts - citados
    assert citados == set(dinamicos[ENTRADA]) | {"MAP_TURNBACK_CAVE_ENTRANCE"}, (
        citados ^ (set(dinamicos[ENTRADA]) | {"MAP_TURNBACK_CAVE_ENTRANCE"}))
    for pasta, alvos in dinamicos.items():
        assert set(alvos) <= citados, (pasta, set(alvos) - citados)

    # 5. as quatro regras do scrcmd estao no script, com os numeros da fonte.
    for pedaco in (f"goto_if_ge {PILARES}, {LIMITE_PILARES}",
                   f"goto_if_ge {SALAS}, {LIMITE_SALAS}",
                   f"goto_if_lt VAR_RESULT, {CHANCE_PILAR}",
                   "random 6"):
        assert pedaco in texto, pedaco
    #    e cada nivel sorteia os SEIS quartos dele, nem cinco nem sete
    for nivel in (1, 2, 3):
        bloco = texto.split(f"TurnbackCave_Nivel{nivel}::")[1]
        if nivel < 3:
            bloco = bloco.split(f"TurnbackCave_Nivel{nivel + 1}::")[0]
        salas = re.findall(r"setdynamicwarp (MAP_[A-Z0-9_]+)", bloco)
        seis = salas_de_pilar()[(nivel - 1) * 6:nivel * 6]
        assert set(salas) == {F.const_do_header(h) for h in seis}, (nivel, salas)

    # 6. a var nova sai de uma VAR_UNUSED que ainda existe, e NAO da faixa do B6.
    vars_h = open(f"{REPO}/include/constants/vars.h").read()
    for nome, ancora, valor in VARS:
        assert 0x41C0 <= valor <= 0x41C1, hex(valor)
        assert (re.search(rf"#define\s+{nome}\b", vars_h)
                or re.search(rf"#define\s+{ancora}\b", vars_h)), (nome, ancora)

    # 7. o tile das portas tem que DISPARAR, lido da tabela do motor. Warp que
    #    existe e nao dispara ja custou levas inteiras aqui (licao 4.1).
    prim, _ = F._atributos("gTileset_GeneralSinnoh")
    seg, _ = F._atributos("gTileset_CaveSinnoh")
    mt = C.ESCADA & 0x3FF
    tab, rel = (prim, mt) if mt < 512 else (seg, mt - 512)
    assert tab[rel] in W.COMPORTA_WARP, hex(C.ESCADA)

    # 8. depois de aplicado: toda sala tem as quatro portas MAP_DYNAMIC, o mapa
    #    da entrada nao ganhou nem perdeu warp (save congelada), e as portas dele
    #    que apontavam para si mesmas agora sorteiam.
    pastas = set(os.listdir(f"{REPO}/data/maps"))
    conferidos = 0
    for h in todos():
        pasta = F.nome_de_pasta(h)
        if pasta not in pastas:
            continue
        d = json.load(open(f"{REPO}/data/maps/{pasta}/map.json"))
        assert len(d["warp_events"]) == 4, (pasta, len(d["warp_events"]))
        assert all(w["dest_map"] == "MAP_DYNAMIC" for w in d["warp_events"]), pasta
        assert d.get("destinos_dinamicos"), pasta
        conferidos += 1
    if conferidos:
        d_ent = json.load(open(f"{REPO}/data/maps/{ENTRADA}/map.json"))
        assert len(d_ent["warp_events"]) == 5, len(d_ent["warp_events"])
        assert sum(1 for w in d_ent["warp_events"]
                   if w["dest_map"] == "MAP_DYNAMIC") == 4, d_ent["warp_events"]
        assert d_ent["warp_events"][4]["dest_map"] == "MAP_SENDOFF_SPRING"
        assert "MAP_SCRIPT_ON_TRANSITION" in open(
            f"{REPO}/data/maps/{ENTRADA}/scripts.inc").read()
    print(f"demo ok ({conferidos} salas conferidas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
