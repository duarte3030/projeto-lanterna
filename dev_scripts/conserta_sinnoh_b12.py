#!/usr/bin/env python3
"""Consertos da rodada 12 (caca a bugs) em Sinnoh: flag orfa, ator trocado,
ordem de warp e janela de sprite.

    python3 dev_scripts/conserta_sinnoh_b12.py            # so relata
    python3 dev_scripts/conserta_sinnoh_b12.py --aplicar
    python3 dev_scripts/conserta_sinnoh_b12.py --demo

Cada secao e IDEMPOTENTE: ela reconhece o proprio conserto e nao escreve de
novo. Rodar duas vezes seguidas tem que deixar o `git diff` igual.

A. HearthomeCity_Gym acendia uma flag que NINGUEM le
----------------------------------------------------
`setflag FLAG_SINNOH_ESCONDE_HEARTHOME_CITY_ROUTE_209_BLOCKADE` no fecho da
Fantina, e nenhum `object_event` da arvore usa essa flag (medido: `grep` em
`data/` da 1 ocorrencia, a propria linha). O comentario acima dela supunha que
"o objeto do bloqueio ja mora em HearthomeCity/map.json"; nao mora.

A escolha foi entre POR o bloqueio, como a fonte, e TIRAR o `setflag`. Tirar,
e o motivo e medido, nao gosto:

1. Na fonte o bloqueio sao dois NPCs (`LOCALID_POKEFAN_M_2` e `LOCALID_HIKER_2`
   de `events_hearthome_city.json`, os dois com `hidden_flag`
   FLAG_HIDE_HEARTHOME_CITY_ROUTE_209_BLOCKADE). Aqui a saida de Hearthome para
   a Route 209 NAO e a pe: e o predio de portao `Route209_Access`, e a fatia
   andavel dele e a faixa x=1..11, y=4..6. Selar aquilo pede TRES corpos numa
   coluna, nao dois, ou seja o bloqueio da fonte nao se traduz um por um.
2. E, o que decide: o SELETOR DE CAPITULO nao acende flag de esconder.
   `ChapterJump_AplicaCapitulo` (src/chapter_jump.c) roda
   `EventScript_ResetAllMapFlags` e depois so `MarcaGinasioVencido`, que acende
   insignia, "derrotado" e id de treinador. Quem saltasse para um capitulo
   DEPOIS da Fantina acharia o bloqueio DE PE e ficaria trancado fora da Route
   209, sem nenhum jeito de desfazer isso pelo proprio seletor. Bloqueio de
   corpo que o seletor nao sabe abrir e pior que rota aberta cedo.

O que sai e uma linha que MENTE. A porcentagem nao muda, o enredo nao muda, e a
sequencia continua exatamente como estava antes desta rodada.

B. PokemonLeagueNorthPokecenter1F: a cena do rival move a PICNICKER
-------------------------------------------------------------------
O objeto do rival (OBJ_EVENT_GFX_RICH_BOY em (10,3), atras de
FLAG_SINNOH_ESCONDE_POKEMON_LEAGUE_NORTH_POKECENTER_1F_RIVAL) entrou em
`442735a754` e foi APAGADO em `73432f3dad`, quando `importa_npcs_sinnoh`
reescreveu a lista de objetos deste mapa a partir da fonte.

O script nao caiu junto, e por isso o defeito e mudo: `local_id` sem nome e a
POSICAO na lista mais um (`tools/mapjson/mapjson.cpp:444`). Com o rival fora, o
mapa ficou com 7 objetos e o `addobject 7` / `applymovement 7` / `removeobject 7`
da cena passaram a mirar o 7o da lista, que e a PICNICKER de (2,6). Resultado no
jogo: a moca do canto faz o "!", anda ate o jogador, luta como BARRY e some do
mapa para sempre. Build verde, validador verde, e o `clearflag` do topo da cena
sem dono.

O objeto volta na POSICAO 7 (indice 6), e nao no fim, justamente para o `7` do
script continuar certo; a PICNICKER passa a ser o 8, e ninguem cita o 8.

C. VerityLakefront: `releaseall` antes do `warp`, `fadescreen` sem `waitstate`
------------------------------------------------------------------------------
A ordem era `releaseall` / `playse` / `fadescreen FADE_TO_BLACK` / `warp` /
`fadescreen FADE_FROM_BLACK` / `end`. O `warp` cria a task de troca de mapa
(`DoWarp`, src/field_screen_effect.c) e poe `LockPlayerFieldControls()`; o
`releaseall` de antes desfaz isso, entao o jogador anda e abre menu no meio do
fade. E sem `waitstate` o script segue rodando por cima da troca de mapa.

A ordem certa e a que o proprio repo ja usa (RustboroCity/scripts.inc:602):
`warp` / `waitstate` / `releaseall` / `end`. O `fadescreen FADE_FROM_BLACK` sai:
o proprio warp faz o fade de volta, e o par de fades brigava.

D. Janela de sprite: `Restaurant` e `GalacticHQ_Hall`
-----------------------------------------------------
`gObjectEvents` tem OBJECT_EVENTS_COUNT vagas e a 0 e do jogador, entao sobram
15 por tela. `TrySpawnObjectEvents` NAO acorda o resto quando elas acabam: sem
erro, sem aviso, e objeto que nao acordou tambem nao e solido. E a licao 1 da
0.s, agora cobrada em dois mapas que a 0.s nao mediu.

- `Restaurant` e 10x9: o mapa INTEIRO cabe dentro de uma janela de 20x17, entao
  espalhar nao existe como opcao. Os 19 viram 15, e quem sai e escolhido por
  prioridade declarada (quem tem script ou e treinador primeiro, depois quem
  esta mais PERTO da porta, e por ultimo a ordem do arquivo), com a lista dos
  que sairam impressa.
- `GalacticHQ_Hall` e 51x33 e tem corredor vazio de sobra, entao ali o conserto
  e ESPALHAR: o grunt mudo (sem script) que estoura a janela anda para o tile
  livre mais proximo que nao estoura nenhuma. Ninguem e apagado enquanto houver
  para onde ir; quem nao couber nem assim sai, e sai na lista.

F. Tumulo de mapa cortado que voltou a ter elenco
--------------------------------------------------
Os 12 `*Pokecenter2F` de Sinnoh que a auditoria acusou como inalcancaveis SAO
mapas cortados, e o corte esta feito: `region_map_section` em `MAPSEC_NONE`, zero
warp, e a escada do 1F ja virou lapide (`CanalaveCityPokecenter1F` tem dois warps
na MESMA coordenada (6,8), que e a assinatura da lapide de
`remove_mapas_cortados.py`). Nao ha porta viva apontando para eles, entao nao ha
lapide nova a por.

O que ha e o contrario: `remove_mapas_cortados` deixa o tumulo com ZERO evento, e
depois disso um importador voltou a povoa-los. Medido em 23/08/2026: **69 tumulos
de Sinnoh com evento dentro**, entre eles os 12 Pokecenters. Nao e defeito de
jogo (ninguem chega la), e sim peso de ROM e mentira de censo: o objeto conta no
numerador de `completude` enquanto o denominador daquele mapa esta zerado.

A porta por onde eles entraram JA esta fechada: `importa_npcs_sinnoh` le
`completude.cortes_da_regiao` e poe teto 0 em mapa cortado (medido:
`CanalaveCityPokecenter2F` devolve `{'object_events','bg_events','warp_events'}`).
Entao aqui basta varrer o que ficou para tras.

A regua GLOBAL tambem contava tumulo, e isso saiu em `valida_conectividade.py`:
mapa sem warp, sem conexao e com `MAPSEC_NONE` nao entra no denominador de
alcance, e o numero de tumulos e dito em voz alta na mesma linha.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))

VAGAS_DE_SPRITE = None          # lido do .h em `vagas_de_sprite()`
JANELA = (20, 17)               # a mesma janela da regra B7 da auditoria


def le(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def escreve(p, s, aplicar):
    if aplicar:
        with open(p, "w", encoding="utf-8") as f:
            f.write(s)


def vagas_de_sprite():
    """15: OBJECT_EVENTS_COUNT menos a vaga 0, que e sempre do jogador.

    Lido do `.h`, e nao decorado, pelo mesmo motivo do `--demo` da 0.s: quem
    mexer no motor tem que quebrar aqui.
    """
    global VAGAS_DE_SPRITE
    if VAGAS_DE_SPRITE is None:
        txt = le(os.path.join(REPO, "include/constants/global.h"))
        m = re.search(r"^#define\s+OBJECT_EVENTS_COUNT\s+(\d+)", txt, re.M)
        if not m:
            raise SystemExit("global.h: OBJECT_EVENTS_COUNT nao achado")
        VAGAS_DE_SPRITE = int(m.group(1)) - 1
    return VAGAS_DE_SPRITE


# ------------------------------------------------------------------ A e C
def _troca_em_arquivo(rel, velho, novo, aplicar, relato):
    p = os.path.join(REPO, rel)
    s = le(p)
    if novo in s:
        relato.append(f"  {rel}: ja consertado")
        return 0
    if velho not in s:
        raise SystemExit(f"{rel}: ancora nao bate (arvore mudou embaixo)")
    escreve(p, s.replace(velho, novo, 1), aplicar)
    relato.append(f"  {rel}: consertado")
    return 1


FLAG_ORFA = "FLAG_SINNOH_ESCONDE_HEARTHOME_CITY_ROUTE_209_BLOCKADE"

A_VELHO = (
    "@ HEARTHOME_CITY_ROUTE_209_BLOCKADE` (o objeto do bloqueio ja mora em\n"
    "@ HearthomeCity/map.json, fora dos meus arquivos desta onda) e `ClearFlag\n")
A_NOVO = (
    "@ HEARTHOME_CITY_ROUTE_209_BLOCKADE` (o objeto do bloqueio NAO mora em\n"
    "@ HearthomeCity/map.json, e a linha saiu em 23/08/2026; ver o cabecalho de\n"
    "@ dev_scripts/conserta_sinnoh_b12.py) e `ClearFlag\n")
A_VELHO2 = f"\tsetflag {FLAG_ORFA}\n"

C_VELHO = """	releaseall
	playse SE_M_SURF
	fadescreen FADE_TO_BLACK
	warp MAP_LAKE_VERITY_LOW_WATER, 39, 47
	fadescreen FADE_FROM_BLACK
	end
"""
C_NOVO = """	playse SE_M_SURF
	delay 30
	warp MAP_LAKE_VERITY_LOW_WATER, 39, 47
	waitstate
	releaseall
	end
"""


def secao_a(aplicar, relato):
    relato.append("A. flag orfa do ginasio de Hearthome")
    p = os.path.join(REPO, "data/maps/HearthomeCity_Gym/scripts.inc")
    s = le(p)
    if A_VELHO2 not in s:
        relato.append("  ja consertado")
        return 0
    s = s.replace(A_VELHO, A_NOVO, 1).replace(A_VELHO2, "", 1)
    escreve(p, s, aplicar)
    relato.append(f"  removido `setflag {FLAG_ORFA}`")
    return 1


def secao_c(aplicar, relato):
    relato.append("C. ordem de warp em VerityLakefront")
    return _troca_em_arquivo("data/maps/VerityLakefront/scripts.inc",
                             C_VELHO, C_NOVO, aplicar, relato)


# ---------------------------------------------------------------------- B
RIVAL_DA_LIGA = {
    "graphics_id": "OBJ_EVENT_GFX_RICH_BOY",
    "x": 10,
    "y": 3,
    "elevation": 3,
    "movement_type": "MOVEMENT_TYPE_FACE_UP",
    "movement_range_x": 0,
    "movement_range_y": 0,
    "trainer_type": "TRAINER_TYPE_NONE",
    "trainer_sight_or_berry_tree_id": "0",
    "script": "0",
    "flag": "FLAG_SINNOH_ESCONDE_POKEMON_LEAGUE_NORTH_POKECENTER_1F_RIVAL",
    "origem": ("pokeplatinum: LOCALID_LEAGUE_NORTH_RIVAL. Sem local_id, entao o "
               "id dele e a POSICAO na lista mais um: ele TEM que ser o 7o, "
               "porque PokemonLeagueNorthPokecenter1F_EventScript_CoordEvent_"
               "Rival faz addobject/applymovement/removeobject 7. Entrou em "
               "442735a754, foi apagado por importa_npcs_sinnoh em 73432f3dad "
               "(a cena passou a mover a PICNICKER) e voltou em 23/08/2026 por "
               "dev_scripts/conserta_sinnoh_b12.py."),
}
POSICAO_DO_RIVAL = 6            # indice 6 == local_id 7


def secao_b(aplicar, relato):
    relato.append("B. rival do Pokecenter da Liga")
    p = os.path.join(REPO, "data/maps/PokemonLeagueNorthPokecenter1F/map.json")
    d = json.load(open(p, encoding="utf-8"))
    objs = d.get("object_events", [])
    if any(o.get("flag") == RIVAL_DA_LIGA["flag"] for o in objs):
        relato.append("  ja consertado")
        return 0
    if len(objs) < POSICAO_DO_RIVAL:
        raise SystemExit("PokemonLeagueNorthPokecenter1F: menos de 6 objetos")
    objs.insert(POSICAO_DO_RIVAL, dict(RIVAL_DA_LIGA))
    d["object_events"] = objs
    if aplicar:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
    relato.append(f"  rival reposto no indice {POSICAO_DO_RIVAL} (local_id 7); "
                  f"o mapa vai a {len(objs)} objetos")
    return 1


# ---------------------------------------------------------------------- E
# NPC que a fonte esconde no jogo novo, o marco desta ROM que o revela, e o
# script que precisa parar de se esconder sozinho. O idioma e o da 0.s: a flag e
# RECALCULADA no ON_TRANSITION do proprio mapa, entao save velha e save nova se
# comportam igual e `new_game.inc` nao e tocado.
#
# Cada marco foi conferido nos DOIS lados: onde a fonte faz o ClearFlag, e quem
# acende o equivalente aqui.
#
#   Celestic elder   scripts_celestic_town_cave.s:133      FLAG_GALACTICA_CELESTIC
#                                                          (CelesticTown:140)
#   Route205 youngster scripts_valley_windworks_building.s:110
#                                                          FLAG_GALACTICA_WINDWORKS
#                                                          (ValleyWindworks:64)
#   Prof. Rowan      scripts_pokemon_league_hall_of_fame.s:207
#                                                          FLAG_SYS_GAME_CLEAR
#                                                          (post_battle_event_funcs.c:44)
CENAS = [
    ("CelesticTownNorthHouse",
     "FLAG_SINNOH_ESCONDE_CELESTIC_TOWN_NORTH_HOUSE_ELDER",
     "FLAG_GALACTICA_CELESTIC"),
    ("Route205_South",
     "FLAG_SINNOH_ESCONDE_ROUTE_205_SOUTH_YOUNGSTER",
     "FLAG_GALACTICA_WINDWORKS"),
    ("VeilstoneStoreB1F",
     "FLAG_SINNOH_ESCONDE_VEILSTONE_STORE_B1F_PROF_ROWAN",
     "FLAG_SYS_GAME_CLEAR"),
]

# O Rowan se escondia sozinho no fim da fala. Com o ON_TRANSITION recalculando a
# flag ele voltaria na proxima entrada, e a fala e de pos-jogo: some por um mapa
# e volta no seguinte e pior que ficar de pe. A linha sai, e ele fica de pe no
# armazem depois do Hall da Fama, que e onde a fonte o poe.
ROWAN_VELHO = ("\tmsgbox VeilstoneStoreB1F_Text_DoesLifeContinueToThrillYou, "
               "MSGBOX_DEFAULT\n"
               "\tsetflag FLAG_SINNOH_ESCONDE_VEILSTONE_STORE_B1F_PROF_ROWAN\n")
ROWAN_NOVO = ("\tmsgbox VeilstoneStoreB1F_Text_DoesLifeContinueToThrillYou, "
              "MSGBOX_DEFAULT\n"
              "\t@ 23/08/2026: o `setflag` de esconder saiu daqui. Quem manda na\n"
              "\t@ flag agora e o ON_TRANSITION do mapa, que a recalcula a cada\n"
              "\t@ entrada a partir de FLAG_SYS_GAME_CLEAR.\n")


def secao_e(aplicar, relato):
    relato.append("E. NPC que nascia escondido e ninguem trazia")
    import cenas_sinnoh_b3 as B3
    n = 0
    for mapa, esconde, marco in CENAS:
        p = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        s = le(p)
        novo = B3.transicao_que_recalcula(mapa, s, [(esconde, ("flag", marco))])
        if novo == s:
            relato.append(f"  {mapa}: ja consertado")
            continue
        escreve(p, novo, aplicar)
        relato.append(f"  {mapa}: ON_TRANSITION recalcula {esconde} por {marco}")
        n += 1
    n += _troca_em_arquivo("data/maps/VeilstoneStoreB1F/scripts.inc",
                           ROWAN_VELHO, ROWAN_NOVO, aplicar, relato)
    return n


# ---------------------------------------------------------------------- D
LUZ = "OBJ_EVENT_GFX_ELECTRIC_LIGHT"     # a unica famılia que nao gasta vaga


def gasta_vaga(o):
    return (o.get("graphics_id") or "") != LUZ


def pior_janela(pts):
    """(maior contagem, canto) entre TODAS as janelas de 20x17 possiveis.

    Mais severa, de proposito, que a regra B7 da auditoria: ela ancora a janela
    em (x,y) do MESMO objeto, e por isso um mapa 10x9 (o `Restaurant`, onde a
    tela inteira cabe dentro da janela) sai dela com "15" so porque um NPC foi
    empurrado para a direita. O maximo de verdade e sobre a grade inteira, e
    basta varrer o produto dos x com os y dos objetos: deslizar a janela para a
    direita ate a borda esquerda encostar num objeto nao perde nenhum, e o mesmo
    vale para baixo.
    """
    lj, aj = JANELA
    xs, ys = sorted({x for x, _ in pts}), sorted({y for _, y in pts})
    pior, canto = 0, None
    for cx in xs:
        faixa = [y for x, y in pts if cx <= x < cx + lj]
        if len(faixa) <= pior:
            continue
        for cy in ys:
            n = sum(1 for y in faixa if cy <= y < cy + aj)
            if n > pior:
                pior, canto = n, (cx, cy)
    return pior, canto


def cabe_mais_um(pts, p):
    """True se por um objeto em `p` mantem toda janela dentro das vagas.

    So olha as janelas que CONTEM `p`: `pts` ja esta dentro do teto, entao
    nenhuma outra janela pode estourar por causa dele.
    """
    lj, aj = JANELA
    px, py = p
    teto = vagas_de_sprite() - 1
    for cx in range(px - lj + 1, px + 1):
        faixa = [y for x, y in pts if cx <= x < cx + lj]
        if len(faixa) <= teto:
            continue
        for cy in range(py - aj + 1, py + 1):
            if sum(1 for y in faixa if cy <= y < cy + aj) > teto:
                return False
    return True


def camada(o, quantos_usam):
    """0 ATOR (nao move nem corta), 1 multidao com fala, 2 mudo.

    O que separa ator de multidao nao e ter script, e o script ser SO DELE. Em
    GalacticHQ_Hall os 16 grunts silenciosos dividem
    `GalacticHQ_Hall_EventScript_SilentGrunt`, e o Cyrus tem o dele: mover o
    Cyrus quebraria a cena, mover um grunt de formacao nao quebra nada.
    """
    lab = str(o.get("script") or "0")
    treinador = str(o.get("trainer_type") or "") not in ("", "TRAINER_TYPE_NONE")
    if lab in ("0", "0x0"):
        return 2
    return 0 if (treinador or quantos_usam.get(lab, 0) == 1) else 1


def na_soleira(o, portas):
    """NPC no tile de porta ou ORTOGONAL a ele.

    Ele e o primeiro a sair, e nao o ultimo: NPC mudo plantado na soleira e o
    que tranca o jogador assim que ele entra. Medido no `Restaurant`, onde o
    15o objeto (um CHEF em (4,7)) nunca acordava por falta de vaga e, ao
    acordar com o conserto, passaria a fechar o warp (4,8) pelo norte.
    """
    for px, py in portas:
        if abs(o["x"] - px) + abs(o["y"] - py) <= 1:
            return True
    return False


def prioridade(i, o, portas, quantos_usam):
    """Menor = fica onde esta, e o desempate e a ORDEM DO ARQUIVO.

    Ator, depois multidao com fala, depois mudo, e por ultimo o mudo na
    soleira. A ordem do arquivo como desempate nao e preguica: e ela que o
    motor usa em `TrySpawnObjectEvents`, entao cortar de tras para frente e
    cortar exatamente quem ja nao acordava.
    """
    c = camada(o, quantos_usam)
    if c == 2 and na_soleira(o, portas):
        c = 3
    return (c, i)


def grade(layout_id):
    """(W, H, [linhas de u16]) do blockdata do layout. Copia curta da leitura
    que `qa/mapas_qa.grade` e `dev_scripts/valida_warp_tile` ja fazem."""
    import struct
    L = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json"),
             encoding="utf-8"))["layouts"]}[layout_id]
    W, H = L["width"], L["height"]
    b = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
    return W, H, [list(struct.unpack_from(f"<{W}H", b, y * W * 2))
                  for y in range(H)]


def alcancaveis(W, H, linhas, sementes):
    """Flood fill de tile andavel a partir dos warps do mapa.

    Sem isto o espalhador poe grunt DENTRO das duas camaras seladas de
    GalacticHQ_Hall (x 7..19 e 31..43, y 20..27), que nao tem porta: o NPC
    existe, gasta vaga e ninguem nunca o ve.

    ponytail: le so os 2 bits de colisao, e NAO le MB_IMPASSABLE_*. O teto e
    conhecido e foi medido nesta rodada: a fileira 15 de GalacticHQ_Hall tem
    (12,15) e (14,15) como MB_IMPASSABLE_WEST, e `IsMetatileDirectionallyImpas-
    sable` cobra isso tambem na SAIDA do tile, entao quem vem do leste por ali
    para antes do corredor oeste. Isso muda o CAMINHO, nao o alcance (o oeste
    entra pela fileira 18, e o T157.1 prova andando ate (0,10)), e por isso a
    leitura simples basta aqui. Quem precisar de mais um dia: puxar a tabela de
    comportamento do tileset como `qa/mapas_qa.Arvore.comportamento` faz.
    """
    from collections import deque
    vistos, fila = set(), deque()
    for x, y in sementes:
        if 0 <= x < W and 0 <= y < H:
            vistos.add((x, y))
            fila.append((x, y))
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in vistos \
                    and ((linhas[ny][nx] >> 10) & 3) == 0:
                vistos.add((nx, ny))
                fila.append((nx, ny))
    return vistos


def tiles_livres(d, elevacoes):
    """Tiles onde da para POR um NPC: andavel, na elevacao dele, sem warp,
    sem coord_event e sem objeto em cima.

    Warp e coord_event ficam de fora porque objeto em cima deles e defeito
    proprio (as regras B2 e B3 da auditoria), e consertar uma regra criando
    outra nao e conserto."""
    W, H, linhas = grade(d["layout"])
    proibido = set()
    for w in d.get("warp_events", []):
        proibido |= {(w["x"], w["y"]), (w["x"] + 1, w["y"]), (w["x"] - 1, w["y"]),
                     (w["x"], w["y"] + 1), (w["x"], w["y"] - 1)}
    proibido |= {(c["x"], c["y"]) for c in d.get("coord_events", [])}
    proibido |= {(o["x"], o["y"]) for o in d.get("object_events", [])}
    vivos = alcancaveis(W, H, linhas,
                        [(w["x"], w["y"]) for w in d.get("warp_events", [])])
    fora = []
    for y in range(H):
        for x in range(W):
            v = linhas[y][x]
            if ((v >> 10) & 3) != 0 or (x, y) in proibido or (x, y) not in vivos:
                continue
            if ((v >> 12) & 0xF) in elevacoes:
                fora.append((x, y))
    return fora


def secao_d(aplicar, relato):
    relato.append("D. janela de sprite")
    n = 0
    for mapa in ("Restaurant", "GalacticHQ_Hall"):
        p = os.path.join(REPO, "data/maps", mapa, "map.json")
        d = json.load(open(p, encoding="utf-8"))
        objs = d.get("object_events", [])
        pts = [(o["x"], o["y"]) for o in objs if gasta_vaga(o)]
        pior, _ = pior_janela(pts)
        if pior <= vagas_de_sprite():
            relato.append(f"  {mapa}: ja cabe ({pior} na pior janela)")
            continue
        antes = pior
        elevacoes = {0} | {int(o.get("elevation", 3) or 0) for o in objs}
        livres = tiles_livres(d, elevacoes)
        portas = [(w["x"], w["y"]) for w in d.get("warp_events", [])]
        quantos_usam = {}
        for o in objs:
            lab = str(o.get("script") or "0")
            quantos_usam[lab] = quantos_usam.get(lab, 0) + 1
        ordem = sorted(range(len(objs)),
                       key=lambda i: prioridade(i, objs[i], portas, quantos_usam))
        mantidos, mexidos, cortados = [], [], []
        postos = set()
        for i in ordem:
            o = objs[i]
            if not gasta_vaga(o):
                mantidos.append(i)
                continue
            alvo = (o["x"], o["y"])
            pos_atuais = [(objs[j]["x"], objs[j]["y"]) for j in mantidos
                          if gasta_vaga(objs[j])]
            if alvo not in postos and cabe_mais_um(pos_atuais, alvo):
                mantidos.append(i)
                postos.add(alvo)
                continue
            if camada(o, quantos_usam) == 0:
                # ATOR: fica onde a cena o poe, custe o que custar. Se ele nao
                # coube, quem tem de sair e a multidao em volta, e ela ja saiu
                # (a ordem garante que os atores foram os primeiros).
                mantidos.append(i)
                postos.add(alvo)
                continue
            # nao cabe onde esta: procura o tile livre mais proximo que caiba
            achou = None
            for x, y in sorted(livres,
                               key=lambda t: abs(t[0] - alvo[0]) + abs(t[1] - alvo[1])):
                if (x, y) in postos:
                    continue
                if cabe_mais_um(pos_atuais, (x, y)):
                    achou = (x, y)
                    break
            if achou:
                o["x"], o["y"] = achou
                mantidos.append(i)
                mexidos.append((i + 1, alvo, achou))
                postos.add(achou)
            else:
                cortados.append((i + 1, o.get("graphics_id"), alvo))
        vivos = [objs[i] for i in sorted(mantidos)]
        d["object_events"] = vivos
        depois, _ = pior_janela([(o["x"], o["y"]) for o in vivos if gasta_vaga(o)])
        if aplicar:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
        relato.append(f"  {mapa}: pior janela {antes} -> {depois} "
                      f"(objetos {len(objs)} -> {len(vivos)}, "
                      f"{len(mexidos)} movidos, {len(cortados)} cortados)")
        for idx, gfx, pos in cortados:
            relato.append(f"     corta #{idx} {gfx} de {pos}")
        for idx, de, para in mexidos[:8]:
            relato.append(f"     move  #{idx} {de} -> {para}")
        if len(mexidos) > 8:
            relato.append(f"     ... e mais {len(mexidos) - 8} movidos")
        n += 1
    return n


# ---------------------------------------------------------------------- F
def e_tumulo(d):
    """Mapa cortado ja esvaziado: sem warp, sem conexao e fora do mapa-mundi."""
    return (str(d.get("region_map_section")) == "MAPSEC_NONE"
            and not d.get("warp_events")
            and not d.get("connections"))


def secao_f(aplicar, relato):
    relato.append("F. tumulo de mapa cortado com elenco dentro")
    import completude as CP
    _rx, deficit = CP.cortes_da_regiao("Sinnoh")
    mapas, eventos = 0, 0
    for meu in sorted(deficit):
        p = os.path.join(REPO, "data/maps", meu, "map.json")
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        if not e_tumulo(d):
            continue
        n = sum(len(d.get(k) or ()) for k in
                ("object_events", "bg_events", "coord_events"))
        if not n:
            continue
        for k in ("object_events", "bg_events", "coord_events"):
            if k in d:
                d[k] = []
        if aplicar:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
        mapas += 1
        eventos += n
    relato.append(f"  {eventos} eventos tirados de {mapas} tumulos")
    return 1 if mapas else 0


# --------------------------------------------------------------------- demo
def demo():
    # 1. a janela e medida como a auditoria mede, e 15 e lido do motor
    assert vagas_de_sprite() == 15, vagas_de_sprite()
    pts = [(10 + i % 5, 9 + i // 5) for i in range(16)]
    assert pior_janela(pts)[0] == 16
    assert pior_janela(pts[:15])[0] == 15
    # 2. objeto longe NAO conta na mesma janela
    assert pior_janela(pts[:15] + [(40, 40)])[0] == 15
    # 2b. e a regua nao se deixa enganar por deslocar objeto DENTRO de um mapa
    #     menor que a janela: 19 pontos num 10x9 sao 19 em qualquer arrumacao.
    quadrado = [(i % 10, i // 10) for i in range(19)]
    assert pior_janela(quadrado)[0] == 19
    assert pior_janela([(9 - x, 8 - y) for x, y in quadrado])[0] == 19
    # 2c. `cabe_mais_um` concorda com `pior_janela`
    assert cabe_mais_um(pts[:14], (12, 10))
    assert not cabe_mais_um(pts[:15], (12, 10))
    # 3. prioridade: quem tem script fica na frente de quem nao tem
    ator = {"x": 0, "y": 0, "script": "X_EventScript_Cyrus"}
    massa = {"x": 0, "y": 0, "script": "X_EventScript_SilentGrunt"}
    mudo = {"x": 0, "y": 0, "script": "0"}
    q = {"X_EventScript_Cyrus": 1, "X_EventScript_SilentGrunt": 16, "0": 14}
    assert (camada(ator, q), camada(massa, q), camada(mudo, q)) == (0, 1, 2)
    assert prioridade(0, ator, [(9, 9)], q) < prioridade(0, massa, [(9, 9)], q)
    assert prioridade(0, massa, [(9, 9)], q) < prioridade(0, mudo, [(9, 9)], q)
    # 4. mudo na SOLEIRA sai antes de qualquer outro mudo, mesmo o de indice
    #    maior; e ator na soleira nao vira soleira nenhuma.
    soleira = {"x": 0, "y": 1, "script": "0"}
    longe = {"x": 9, "y": 9, "script": "0"}
    assert na_soleira(soleira, [(0, 0)]) and not na_soleira(longe, [(0, 0)])
    assert prioridade(9, longe, [(0, 0)], q) < prioridade(0, soleira, [(0, 0)], q)
    assert prioridade(0, ator, [(0, 0)], q) < prioridade(0, soleira, [(0, 0)], q)
    # 5. local_id do rival: a posicao escolhida tem que dar 7, que e o numero
    #    que o script cita. Se alguem trocar a constante, isto morde.
    assert POSICAO_DO_RIVAL + 1 == 7
    s = le(os.path.join(REPO, "data/maps/PokemonLeagueNorthPokecenter1F",
                        "scripts.inc"))
    assert "addobject 7" in s and "removeobject 7" in s
    # 6. os tres marcos existem e sao acesos por alguem
    for _, esconde, marco in CENAS:
        fh = le(os.path.join(REPO, "include/constants/flags.h"))
        assert re.search(rf"^#define {esconde}\b", fh, re.M), esconde
        assert re.search(rf"^#define {marco}\b", fh, re.M), marco
    # 6b. tumulo e reconhecido pelos TRES sinais, e mapa vivo nao e tumulo
    assert e_tumulo({"region_map_section": "MAPSEC_NONE"})
    assert not e_tumulo({"region_map_section": "MAPSEC_SINNOH_WEST"})
    assert not e_tumulo({"region_map_section": "MAPSEC_NONE",
                         "warp_events": [{"x": 0, "y": 0}]})
    assert not e_tumulo({"region_map_section": "MAPSEC_NONE",
                         "connections": [{"map": "MAP_X"}]})
    # 7. a ordem nova de warp e a canonica do proprio repo
    assert C_NOVO.index("waitstate") < C_NOVO.index("releaseall")
    assert C_NOVO.index("warp ") < C_NOVO.index("waitstate")
    print("demo ok")


def main():
    aplicar = "--aplicar" in sys.argv
    relato, n = [], 0
    for f in (secao_a, secao_b, secao_c, secao_e, secao_d, secao_f):
        n += f(aplicar, relato)
    print("\n".join(relato))
    print(f"\n{n} consertos" + ("" if aplicar else "  (nada escrito; rode com --aplicar)"))
    return 0


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
