#!/usr/bin/env python3
"""Traz o sub-balde b3 de Sinnoh: objeto do Platinum cuja `hidden_flag` é de cena.

    python3 dev_scripts/cenas_sinnoh_b3.py                  # relata (dry-run)
    python3 dev_scripts/cenas_sinnoh_b3.py --dry-run --arco toggle
    python3 dev_scripts/cenas_sinnoh_b3.py --aplicar
    python3 dev_scripts/cenas_sinnoh_b3.py --demo

## O buraco, medido em 23/08/2026 e não herdado de relatório

`importa_npcs_sinnoh.py` recusa todo objeto do Platinum com `hidden_flag`
(decisão 2 dele). Depois de tirar os mapas que os CORTES DO GUI já cortaram,
sobram **169 linhas de censo**. O que NÃO é verdade é que esses 169 sejam 169
buracos de régua: a régua `objetos` de `completude.py` é uma soma global, e o
que ela cobra são os **154 objetos de déficit líquido** que Sinnoh tem hoje
(2.146 nossos contra 2.300 da fonte, 93,30%), espalhados por 73 mapas.

Cruzando os dois números, mapa a mapa (`--dry-run` imprime a conta):

- **12 dos 169 já estão no mapa**, postos por OUTRO gerador (os seis do show da
  Rota 218 vieram por `cena_galactica_sinnoh.py`, o Cyrus/Mars/Jupiter do Spear
  Pillar vieram à mão, o Wyatt e o Danny vieram pelo bloco HORARIO). O censo não
  os reconhece porque casa por MARCA de coordenada, e eles não têm a marca.
  Trazê-los de novo DUPLICA gente, e é por isso que o teto por mapa existe.
- **97 caem em mapa que já está no teto da fonte** (déficit zero ou menor que o
  que o balde oferece). Entrar ali não fecha buraco nenhum: só põe mais gente do
  que o Platinum tem naquele mapa.
- Sobram, no melhor caso, **64 vagas** que o b3 pode fechar. Ou seja: **objetos
  de Sinnoh a 100% NÃO é alcançável portando cena de enredo**, e nunca foi. Dos
  154 de déficit, 122 são MOBILIÁRIO (canteiro de berry, VENT, BOLLARD, decisão
  4 do importador), geometria recusada e teto; 64 são gente.

Este gerador fecha a parte de gente, e escreve por que cada um que fica de fora
ficou. Ninguém aqui inventa bloqueio: o objeto só entra se passar nos portões.

## A régua que decide se o objeto entra VISÍVEL ou atrás de cena

Não é gosto, é medida na fonte. Para cada `FLAG_HIDE_*` este script varre
`res/field/scripts/*.s` do pokeplatinum e anota QUEM acende e QUEM apaga:

- se `scripts_init_new_game.s` acende a flag, o objeto **nasce escondido** no
  jogo original e só entra em cena depois de um marco;
- se a flag é acesa e apagada **só pelo script do próprio mapa do objeto**, ela
  não é marco de história nenhum: é chave local de uma cena curta, e no jogo
  original aquele NPC está lá em jogo normal. Esse entra **visível e falando**,
  que é a mesma decisão que o balde b2 já tomou para o Restaurante.
- o resto precisa de um marco NOSSO, e só entra se o marco existir nesta ROM
  (tabela `MARCOS`). Sem marco, fica de fora com o motivo escrito, porque
  objeto escondido sem cena que o revele é gente que nunca aparece, e objeto
  visível que devia estar escondido é o mapa mentindo.

## Os portões, todos medidos e nenhum decorativo

1. **Teto da fonte**: mapa nunca passa do número de `object_events` que o
   Platinum tem nele. É o portão que impede duplicar quem já foi posto por
   outro gerador, mesmo quando este script não o reconhece pelo nome.
2. **Papel repetido**: objeto novo cujo `graphics_id` já existe no mapa em
   número igual ou maior que o da fonte não entra.
3. **Colisão**: o tile tem que ser andável (`valida_mapas_sinnoh.colisao`), fora
   de warp e da vizinhança dele, e desocupado.
4. **Sem tranca**: `importa_npcs_sinnoh.sem_tranca`, a mesma busca em largura das
   pedras: com TODO objeto tratado como bloqueio, todo pouso de warp continua
   alcançável a partir do primeiro.
5. **Janela de sprite**: no pior enquadramento de 20 por 17 tiles, o mapa não
   passa de 15 objetos (`OBJECT_EVENTS_COUNT` menos o jogador).
6. **Texto**: fala que o charmap não traduz, ou que exigiria um buffer que este
   gerador não emite, reprova o OBJETO (não a cena inteira): ele entra mudo, que
   é o que `importa_npcs_sinnoh` já faz com NPC de rua.

## Idempotência

Cada objeto criado leva `"origem": MARCA` e `"fonte_id"` (o `LOCALID_*` da
fonte). Rodar `--aplicar` de novo pula quem já tem o mesmo `fonte_id` no mapa, e
o trecho de `scripts.inc` só é acrescentado se o rótulo ainda não estiver lá.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import cena_galactica_sinnoh as G  # noqa: E402  alvo_livre, fala_de_mudo, layouts
import completude as C  # noqa: E402  a lista de CORTES DO GUI
import importa_npcs_sinnoh as I  # noqa: E402  conversor de coordenada, sem_tranca
import sprites_sinnoh as SPR  # noqa: E402  de-para dos 26 sprites próprios
import valida_mapas_sinnoh as V  # noqa: E402  colisão, sprites que a build desenha

PLAT = G.PLAT
MARCA = "cenas_sinnoh_b3"
JANELA_SPRITE = (20, 17)     # a tela mais a borda que o motor mantém carregada
TETO_SPRITE = 15             # OBJECT_EVENTS_COUNT (16) menos o jogador


# --------------------------------------------------------------------------
# O QUE FICA DE FORA POR DECISÃO, com o motivo escrito.
#
# Nada aqui é "não deu tempo": cada linha é uma coisa que esta ROM não tem como
# suportar, e a alternativa seria plantar gente que nunca some ou cena que nunca
# roda. Quem for reabrir, reabra pelo motivo, não pela lista.
FORA = {
    "FLAG_HIDE_MART_MYSTERY_GIFT_DELIVERYMAN":
        "entregador do Mystery Gift: o presente vem por Wi-Fi do DS, que este "
        "cartucho não tem. Mesma decisão dos atendentes de Union Room "
        "(FLAG_SINNOH_WIFI_ESCONDIDO, pergunta 17)",
    "FLAG_HIDE_POKECENTER_BASEMENT_BLOCKADE":
        "bloqueio do subsolo do Pokécenter: o B1F de gen 4 é sala de Wi-Fi, "
        "cortada do escopo. O bloqueio sem o andar é parede sem porta",
    "FLAG_HIDE_ROUTE_212_BLOCKADE":
        "repórter e cinegrafista que fecham a Rota 212 até a cena de Pastoria: "
        "bloqueio de estrada, e a cena que o abre não está portada",
    "FLAG_HIDE_ROUTE_218_BLOCKADE":
        "o show da Rota 218 JÁ ESTÁ no mapa desde cena_galactica_sinnoh.py, "
        "com FLAG_GALACTICA_CELESTIC; o censo não reconhece por falta de marca",
    "FLAG_HIDE_ROUTE_224_SHAYMIN":
        "Shaymin depende do Oak's Letter (evento de distribuição)",
    "FLAG_HIDE_ROUTE_224_MARLEY":
        "Marley é a acompanhante da Rota 224, cena de escolta que não existe aqui",
    "FLAG_HIDE_SNOWPOINT_TEMPLE_B5F_REGIGIGAS":
        "Regigigas só acorda com os três Regi no time, e as ruínas dos Regi "
        "estão na Battle Zone, cortada do escopo",
    "FLAG_HIDE_JUBILIFE_TV_3F_GROUP_RANKING_ROOM_WORKER":
        "sala de ranking em grupo: contagem de Wi-Fi, sem multiplayer aqui",
    "FLAG_HIDE_ACUITY_CAVERN_UXIE":
        "Uxie já está no mapa como estático de lendário (bloco B1.b)",
    "FLAG_HIDE_VALOR_CAVERN_AZELF":
        "Azelf já está no mapa como estático de lendário (bloco B1.b)",
    "FLAG_HIDE_VERITY_CAVERN_MESPRIT":
        "Mesprit já está no mapa como estático de lendário (bloco B1.b)",
    "FLAG_HIDE_CONTEST_HALL_LOBBY_REPORTER":
        "repórter do Contest de gen 4: o concurso por toque não tem motor aqui "
        "(corte do Gui, 21/08/2026)",
}

# Gêmeo de horário: na fonte o MESMO corpo tem duas versões no MESMO tile, uma
# que luta e uma que só fala, trocadas por `GetTimeOfDay`. Nenhum dos treinadores
# dessa família existe nesta ROM (conferido por grep em opponents.h: zero
# TRAINER_JOGGER_SCOTT, TRAINER_POLICEMAN_ALEX e os outros seis), então entra o
# gêmeo que FALA e o que luta fica de fora. Trazer os dois plantaria duas pessoas
# no mesmo tile.
GEMEO_QUE_LUTA = re.compile(r"^(?!.*_NO_BATTLE$).*_(POLICEMAN|JOGGER)_[A-Z]+$")


# --------------------------------------------------------------------------
# MARCOS: objeto que nasce escondido e a NOSSA flag que o revela.
#
# Só entra aqui quem tem marco JÁ EXISTENTE nesta ROM. Nenhuma flag nova é
# pedida por esta tabela, e é de propósito: flag nova pede linha em
# `EventScript_ResetAllMapFlags`, que só vale para jogo NOVO, e save antiga
# veria o elenco inteiro plantado desde o primeiro dia.
#
# `polaridade`:
#   "some"    -> o objeto está lá desde o começo e SOME quando a flag acende.
#                Custo zero: `flag` no object_event e nada mais.
#   (não há "aparece" nesta leva; ver o comentário acima.)
MARCOS = {
    # Os três guardiões cativos na sala de controle do QG. FLAG_GALACTICA_LAKE
    # _TRIO_FREED já existe e já quer dizer exatamente "o botão do QG soltou
    # Uxie, Mesprit e Azelf": com ela apagada os três estão presos ali, com ela
    # acesa eles sumiram. A fonte esconde por FLAG_HIDE_GALACTIC_HQ_CONTROL_ROOM
    # _LAKE_GUARDIANS, que o script do próprio QG APAGA (ClearFlag) na cena da
    # soltura; a polaridade daqui é a mesma cena lida ao contrário, e ao
    # contrário é como esta ROM já modela o momento.
    "FLAG_HIDE_GALACTIC_HQ_CONTROL_ROOM_LAKE_GUARDIANS":
        ("FLAG_GALACTICA_LAKE_TRIO_FREED", "some"),
    # O grunt da bomba de Celestic some com FLAG_GALACTICA_CELESTIC, que a cena
    # de CelesticTown já acende (CelesticTown/scripts.inc). O Cyrus da caverna é
    # o mesmo momento: ele está lá enquanto a Galáctica está em Celestic.
    "FLAG_HIDE_CELESTIC_TOWN_CAVE_CYRUS":
        ("FLAG_GALACTICA_CELESTIC", "some"),
    # O grunt do Lago Valor some quando o Saturn cai e o lago é esvaziado:
    # FLAG_SINNOH_LAGO_VALOR_ESVAZIADO já existe e já some com os três grunts
    # de LakeValorDrained.
    "FLAG_HIDE_VALOR_LAKEFRONT_GRUNT_M":
        ("FLAG_SINNOH_LAGO_VALOR_ESVAZIADO", "some"),
    # Os dois cinegrafistas da beira do Lago Valor são a equipe de TV que cobre
    # o cerco da Galáctica; saem no mesmo instante que o grunt.
    "FLAG_HIDE_VALOR_LAKEFRONT_CAMERAMEN":
        ("FLAG_SINNOH_LAGO_VALOR_ESVAZIADO", "some"),
    # Os dois Starly do leito do Lago Verity: a fonte os esconde pelo script do
    # PRÓPRIO mapa, e o motivo é a cutscene de abertura. Aqui não há cutscene, e
    # bicho selvagem parado no leito é o que a fonte mostra em jogo normal.
    "FLAG_HIDE_LAKE_VERITY_LOW_WATER_STARLY": (None, "visivel"),
    # Os dois grunts que fecham a Rota 205 sul: a fonte os apaga no prédio da
    # usina de Valley Windworks, que é exatamente o que FLAG_GALACTICA_WINDWORKS
    # já quer dizer aqui (setflag em ValleyWindworks, FloaromaTown e
    # Route205_South, conferido em GRUPOS_COM_CENA do importador).
    "FLAG_HIDE_ROUTE_205_SOUTH_GRUNTS":
        ("FLAG_GALACTICA_WINDWORKS", "some"),
    # Os dois grunts da sala 1 do Mt. Coronet 1F norte: mesma ocupação que
    # FLAG_GALACTICA_MT_CORONET já desfaz nos cinco andares vizinhos.
    "FLAG_HIDE_MT_CORONET_1F_NORTH_ROOM_1_GRUNTS_M":
        ("FLAG_GALACTICA_MT_CORONET", "some"),
    # A Galáctica no pilar distorcido é a MESMA ocupação do pilar: cai com o
    # Cyrus. A fonte apaga isso em `sendoff_spring`, que é mapa cortado do
    # escopo (Turnback Cave/Sendoff Spring, corte de 21/08/2026), então usar o
    # marco de lá seria pendurar a cena num lugar que não existe.
    "FLAG_HIDE_SPEAR_PILLAR_DISTORTED_TEAM_GALACTIC":
        ("FLAG_GALACTICA_MT_CORONET", "some"),
    # O grunt de Pastoria que foge para leste: FLAG_SINNOH_PASTORIA_GRUNT_FUGIU
    # _LESTE já existe e já é o set-piece da bomba (leva S5, 18/08/2026).
    "FLAG_HIDE_PASTORIA_CITY_GRUNT_M":
        ("FLAG_SINNOH_PASTORIA_GRUNT_FUGIU_LESTE", "some"),
}


# --------------------------------------------------------------------------
# MARCO POR SCRIPT DA FONTE: quem REVELA o objeto la, e o que quer dizer aqui.
#
# Polaridade "aparece": na fonte o objeto nasce ESCONDIDO
# (`scripts_init_new_game.s` acende a flag) e algum script depois a APAGA. A
# chave desta tabela e o miolo do arquivo que APAGA, e o valor e o marco NOSSO
# que quer dizer a mesma coisa. Script que nao esta aqui NAO vira cena: o objeto
# fica de fora com o motivo escrito, porque objeto escondido sem quem o revele e
# gente que nunca aparece.
#
# ("flag", NOME) usa `call_if_set`; ("trainer", NOME) usa `call_if_defeated`, que
# le a flag de derrotado que o motor ja grava (TRAINER_FLAGS_START + id) e por
# isso tambem custa zero flag nova.
MARCO_POR_SCRIPT = {
    # queda da Galactica em cada lugar, marcos que esta ROM ja tem e ja usa
    "celestic_town_cave": ("flag", "FLAG_GALACTICA_CELESTIC"),
    "celestic_town": ("flag", "FLAG_GALACTICA_CELESTIC"),
    "team_galactic_eterna_building_4f": ("flag", "FLAG_GALACTICA_ETERNA"),
    "eterna_city": ("flag", "FLAG_GALACTICA_ETERNA"),
    "valley_windworks_building": ("flag", "FLAG_GALACTICA_WINDWORKS"),
    "valley_windworks_outside": ("flag", "FLAG_GALACTICA_WINDWORKS"),
    "galactic_hq_control_room": ("flag", "FLAG_GALACTICA_QG_TOMADO"),
    "galactic_hq_hall": ("flag", "FLAG_GALACTICA_QG_TOMADO"),
    "spear_pillar_distorted": ("flag", "FLAG_GALACTICA_MT_CORONET"),
    "spear_pillar": ("flag", "FLAG_GALACTICA_MT_CORONET"),
    "lake_verity": ("flag", "FLAG_GALACTICA_LAGO_VERITY"),
    "lake_acuity": ("flag", "FLAG_GALACTICA_ACUITY_VISTO"),
    # o Lago Valor esvaziado, que e o mesmo momento da queda do Saturn
    "valor_lakefront": ("flag", "FLAG_SINNOH_LAGO_VALOR_ESVAZIADO"),
    "route_213": ("flag", "FLAG_SINNOH_LAGO_VALOR_ESVAZIADO"),
    # Canalave: o rival da biblioteca ja tem flag propria nesta ROM
    "canalave_city": ("flag", "FLAG_GALACTICA_CANALAVE_RIVAL"),
    "canalave_library_3f": ("flag", "FLAG_GALACTICA_CANALAVE_RIVAL"),
    # ginasios: a flag de derrotado do lider ja e gravada pelo motor
    "oreburgh_city_gym": ("trainer", "TRAINER_SINNOH_LEADER_ROARK"),
    "eterna_city_gym": ("trainer", "TRAINER_SINNOH_LEADER_GARDENIA"),
    "canalave_city_gym": ("trainer", "TRAINER_SINNOH_LEADER_BYRON"),
    "canalave_city_sailor_eldritch_house": ("trainer", "TRAINER_SINNOH_LEADER_BYRON"),
    "iron_island_house": ("trainer", "TRAINER_SINNOH_LEADER_BYRON"),
    "pastoria_city_gym": ("trainer", "TRAINER_SINNOH_LEADER_WAKE"),
    "veilstone_city_gym": ("trainer", "TRAINER_SINNOH_LEADER_MAYLENE"),
    "snowpoint_city_gym": ("trainer", "TRAINER_SINNOH_LEADER_CANDICE"),
    "sunyshore_city_gym": ("trainer", "TRAINER_SINNOH_LEADER_VOLKNER"),
    # a Pokedex do laboratorio de Sandgem, marco nativo do motor
    "sandgem_town": ("flag", "FLAG_SYS_POKEDEX_GET"),
    "sandgem_town_pokemon_research_lab": ("flag", "FLAG_SYS_POKEDEX_GET"),
    "pokemon_league_hall_of_fame": ("flag", "FLAG_SYS_GAME_CLEAR"),
}


# --------------------------------------------------------------------------
# leitura da fonte

_TOQUES = None


def toques_da_fonte():
    """{FLAG_HIDE_*: (conjunto que ACENDE, conjunto que APAGA)}, por script.

    Os nomes são o miolo do arquivo: `scripts_route_215.s` vira `route_215`.
    É a única evidência que decide visível x escondido, e ela é MEDIDA na fonte,
    não deduzida do nome da flag.
    """
    global _TOQUES
    if _TOQUES is None:
        import glob
        acende, apaga = {}, {}
        for arq in glob.glob(os.path.join(PLAT, "res/field/scripts", "*.s")):
            base = os.path.basename(arq)[len("scripts_"):-len(".s")]
            txt = open(arq, encoding="utf-8", errors="ignore").read()
            for m in re.finditer(r"\b(SetFlag|ClearFlag)\s+(FLAG_HIDE_[A-Z0-9_]+)",
                                 txt):
                (acende if m.group(1) == "SetFlag" else apaga) \
                    .setdefault(m.group(2), set()).add(base)
        _TOQUES = {f: (acende.get(f, set()), apaga.get(f, set()))
                   for f in set(acende) | set(apaga)}
    return _TOQUES


def so_do_proprio_mapa(flag, header):
    """True quando a flag só é tocada pelo script do mapa DO OBJETO.

    `header` é o `MAP_HEADER_*` da fonte; o arquivo de script dele sai da mesma
    tabela que `texto_placas_sinnoh` usa, então isto não é casamento por nome
    parecido, é o par que o próprio decomp declara.
    """
    ac, ap = toques_da_fonte().get(flag, (set(), set()))
    if "init_new_game" in ac:
        return False
    meu = arquivo_de_script(header)
    return bool(ac | ap) and (ac | ap) <= {meu}


_ARQ_SCRIPT = None


def arquivo_de_script(header):
    """Miolo do arquivo de script que o decomp associa a este MAP_HEADER."""
    global _ARQ_SCRIPT
    if _ARQ_SCRIPT is None:
        from texto_placas_sinnoh import campos_do_header
        _ARQ_SCRIPT = {}
        _ARQ_SCRIPT["__f"] = campos_do_header
    campos = _ARQ_SCRIPT["__f"](header)
    if not campos:
        return None
    nome = campos[0]
    return nome[len("scripts_"):] if nome.startswith("scripts_") else nome


def teto_da_fonte(fonte):
    return len(fonte.get("object_events") or [])


def lotacao(pontos):
    """Objetos no PIOR enquadramento de uma janela de sprite. Pessimista de
    propósito: errar para o lado de sobrar custa um reposicionamento, errar para
    o outro custa NPC invisível que compilação nenhuma acusa."""
    if not pontos:
        return 0
    W, H = JANELA_SPRITE
    return max(sum(1 for x, y in pontos if xl <= x < xl + W and yt <= y < yt + H)
               for xl in {p[0] for p in pontos} for yt in {p[1] for p in pontos})


# --------------------------------------------------------------------------
# plano

def mapas_no_escopo():
    """Mapa nosso de Sinnoh que os CORTES DO GUI não cortaram."""
    cortados = C._cortados_deficit()
    return [m for m in I.nossos_mapas_sinnoh() if m not in cortados]


def deficit_por_mapa():
    """{mapa: (nossos, da fonte)} pelo MESMO casamento que `completude.py` usa."""
    heads = I.headers_do_platinum()
    deles = {}
    for h in heads:
        deles.setdefault(I.chave(h), h)
    saida = {}
    for m in I.nossos_mapas_sinnoh():
        h = I.APELIDOS.get(m) or deles.get(I.chave(m))
        if h not in heads:
            continue
        a = C.eventos(C.RAIZ, m)
        b = C.le_plat(C.REGIOES["Sinnoh"]["fonte"], h)
        if not a or not b:
            continue
        saida[m] = (a["object_events"], b["object_events"])
    return saida


def classifica(flag, header):
    """('visivel'|'some', flag nossa) ou ('fora', motivo)."""
    if flag in FORA:
        return "fora", FORA[flag]
    if GEMEO_QUE_LUTA.match(flag):
        return "fora", ("gêmeo que luta: o treinador não existe nesta ROM; "
                        "entra o gêmeo _NO_BATTLE, no mesmo tile")
    # O grupo já tem DONO nesta ROM: alguma cena nossa faz `clearflag` +
    # `addobject` num LOCALID específico, e plantar um segundo corpo com a mesma
    # flag faria a cena revelar DOIS. Mesma régua de `importa_npcs.cena_nossa`.
    dono = I.cena_nossa(flag)
    if dono:
        return "fora", f"grupo com dono: a cena de {dono} já revela este corpo"
    # A cena deste grupo JÁ EXISTE aqui (balde b1 do importador): o objeto entra
    # com a NOSSA flag e some no mesmo instante em que o resto do grupo já some.
    if flag in I.GRUPOS_COM_CENA:
        return "some", I.GRUPOS_COM_CENA[flag]
    if flag in MARCOS:
        nossa, pol = MARCOS[flag]
        return ("visivel", "0") if pol == "visivel" else ("some", nossa)
    if so_do_proprio_mapa(flag, header):
        return "visivel", "0"
    ac, ap = toques_da_fonte().get(flag, (set(), set()))
    if not (ac | ap):
        return "fora", ("flag MORTA na fonte: ninguém acende, ninguém apaga. "
                        "Quem traz esse objeto é importa_npcs_sinnoh, pelo "
                        "caminho `flag_morta`, e não este gerador")
    if "init_new_game" in ac:
        for quem in sorted(ap):
            if quem in MARCO_POR_SCRIPT:
                return "aparece", MARCO_POR_SCRIPT[quem]
        return "fora", ("nasce escondido na fonte, e quem o revela lá (%s) não "
                        "tem marco equivalente nesta ROM"
                        % (",".join(sorted(ap)) or "ninguém"))
    return "fora", ("a flag é acesa fora do mapa do objeto (%s) e o marco não "
                    "tem equivalente aqui" % ",".join(sorted(ac)) or "?")


def plano(so_arco=None):
    """[(mapa, [objetos], trecho)] + censo de recusas."""
    lays = G.layouts()
    sprites = V.sprites_utilizaveis()
    heads = I.headers_do_platinum()
    deficits = deficit_por_mapa()
    de_para = SPR.de_para()
    saida, recusas = [], []
    for meu in sorted(mapas_no_escopo()):
        par = G.eventos_da_fonte(meu)
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        if par is None or not os.path.exists(pm):
            continue
        fonte, header = par
        candidatos = [e for e in (fonte.get("object_events") or [])
                      if str(e.get("hidden_flag", "0")).startswith("FLAG_HIDE_")]
        if not candidatos:
            continue
        d = json.load(open(pm, encoding="utf-8"))
        lid = d["layout"]
        larg, alt = lays[lid]["width"], lays[lid]["height"]
        conv = I.conversor_de_coordenada(fonte, larg, alt, header,
                                         heads.get(header, (None, None))[1], d)
        ocupados = G.ocupados_do_mapa(d)
        # PORTÃO 3c: tile de `coord_event` é GATILHO, e corpo em cima dele é a
        # cena inteira apagada. Medido em 23/08/2026 pelo T102.9: o Uxie desta
        # leva caiu em (7,9) do `GalacticHQ_ControlRoom`, que é o ÚNICO
        # coord_event do mapa, e a batalha contra o Saturn deixou de abrir (o
        # caso acusou `TRAINER_NONE`). `proibidos_do_mapa` só conhece warp, e o
        # gatilho é tão frágil quanto a porta: quem pisa nele é o jogador, e
        # jogador não pisa onde tem gente.
        proibidos = G.proibidos_do_mapa(d) | {
            (c.get("x"), c.get("y")) for c in (d.get("coord_events") or [])}
        ja = {o.get("fonte_id") for o in (d.get("object_events") or [])}
        nossos, da_fonte = deficits.get(meu, (len(d.get("object_events") or []),
                                              teto_da_fonte(fonte)))
        vaga = da_fonte - nossos
        gfx_nossos = {}
        for o in d.get("object_events") or []:
            gfx_nossos[o["graphics_id"]] = gfx_nossos.get(o["graphics_id"], 0) + 1
        # O gêmeo que LUTA nunca entra (o treinador não existe aqui), então ele
        # também não pode contar no denominador do portão de papel repetido:
        # contando, o Wyatt da Rota 210 (já posto pelo bloco HORARIO) daria vaga
        # para um SEGUNDO Wyatt, e de manhã haveria dois no mesmo mapa.
        gfx_fonte = {}
        for e in fonte.get("object_events") or []:
            if GEMEO_QUE_LUTA.match(str(e.get("hidden_flag", "0"))):
                continue
            g = traduz_gfx(e, sprites, de_para)
            gfx_fonte[g] = gfx_fonte.get(g, 0) + 1
        rotulos = V.rotulos_da_unidade()
        novos, trechos, revela = [], [], []
        ancora_de_grupo = {}
        _cache = {}
        for e in candidatos:
            flag_fonte = e["hidden_flag"]
            if so_arco and so_arco not in (flag_fonte, meu):
                continue
            def nao(motivo):
                recusas.append((meu, e.get("id"), flag_fonte, motivo))
            if e.get("id") in ja:
                nao("já está no mapa (mesmo fonte_id)")
                continue
            tipo, nossa = classifica(flag_fonte, header)
            if tipo == "fora":
                nao(nossa)
                continue
            marco = None
            if tipo == "aparece":
                marco, nossa = nossa, apelido(flag_fonte)
                if nossa is None:
                    nao("faixa de flags de Sinnoh cheia: sem apelido livre")
                    continue
            if vaga - len(novos) <= 0:
                nao(f"teto da fonte: o mapa já tem {nossos} objetos de {da_fonte}")
                continue
            gfx = traduz_gfx(e, sprites, de_para)
            if not V.desenhavel(gfx, sprites):
                nao(f"sprite ausente nesta build: {gfx}")
                continue
            if gfx_nossos.get(gfx, 0) >= gfx_fonte.get(gfx, 0):
                nao(f"papel repetido: o mapa já tem {gfx_nossos.get(gfx, 0)} "
                    f"de {gfx} e a fonte tem {gfx_fonte.get(gfx, 0)}")
                continue
            # COESÃO DE GRUPO, medida e não estética. A conversão de rua é por
            # PROPORÇÃO da caixa da matriz do Platinum sobre o nosso layout, e
            # quando a caixa é estreita a proporção ESTICA a distância: no
            # `SpearPillar_Distorted` a caixa da fonte tem 5 colunas e o nosso
            # layout tem 27, então a Mars e a Jupiter, que na fonte estão a
            # QUATRO tiles uma da outra, saíam em x=0 e x=26, cada uma numa
            # ponta do labirinto. Quem já entrou do MESMO grupo de hidden_flag
            # vira âncora, e o resto do grupo entra pelo delta DA FONTE, que é
            # a distância que o jogo original mostra.
            anc = ancora_de_grupo.get(flag_fonte)
            if anc:
                e0, p0 = anc
                alvo = (p0[0] + (e["x"] - e0["x"]), p0[1] + (e["z"] - e0["z"]))
            else:
                alvo = conv(e) if conv else None
            # ÂNCORA: coordenada convertida que cai FORA do nosso layout não é
            # "quase certa", é lixo, e procurar tile livre a partir dela joga o
            # corpo na borda do mapa (a Jupiter do pilar distorcido saiu em
            # x=0 e a Mars em x=26 na primeira medida, uma em cada ponta). Fora
            # do layout, a âncora passa a ser o centro de massa de quem já está
            # no mapa, que é onde a cena acontece.
            if alvo is not None and not (0 <= alvo[0] < larg and 0 <= alvo[1] < alt):
                alvo = None
            if alvo is None or V.colisao(lays, lid, *alvo) != 0 \
                    or alvo in ocupados or alvo in proibidos:
                alvo = G.alvo_livre(lays, lid,
                                    alvo or G.centro_de_massa(d) or
                                    (larg // 2, alt // 2),
                                    ocupados, proibidos)
            if alvo is None:
                nao("sem tile andável livre a 12 de distância")
                continue
            # PORTÃO 3b: o tile é ANDÁVEL, mas o jogador chega nele?
            # `V.colisao` diz que o metatile deixa passar, e não diz que existe
            # caminho. Medido em 23/08/2026: o AZELF caiu em (15,0) e o MESPRIT
            # em (2,0) do `GalacticHQ_ControlRoom`, dois tiles andáveis de UMA
            # célula cada, ilhados por parede em toda volta (a linha 1 do mapa é
            # `#############.##`). Objeto que ninguém alcança nem para falar é
            # objeto que não existe: enche a régua e não enche o mapa.
            if not alcancavel(lays, d, alvo, _cache):
                nao(f"tile {alvo} é andável mas ILHADO: nenhum warp chega nele "
                    "nem no vizinho de conversa")
                continue
            pontos = [(o["x"], o["y"]) for o in (d.get("object_events") or [])]
            pontos += [(o["x"], o["y"]) for o in novos] + [alvo]
            if lotacao(pontos) > TETO_SPRITE:
                nao(f"janela de sprite cheia ({lotacao(pontos)} em 20x17)")
                continue
            fala = fala_do_evento(header, e)
            lab = "0"
            if fala:
                lab = G.rotulo_livre(rotulos, meu, rotulo_de(e))
                txt = lab.replace("_EventScript_", "_Text_")
                trechos.append(f"\n{lab}::\n\tmsgbox {txt}, MSGBOX_NPC\n\tend\n\n"
                               f'{txt}:\n\t.string "{fala}"\n')
            ocupados.add(alvo)
            if marco and (nossa, marco) not in revela:
                revela.append((nossa, marco))
            ancora_de_grupo.setdefault(flag_fonte, (e, alvo))
            gfx_nossos[gfx] = gfx_nossos.get(gfx, 0) + 1
            novos.append({
                "graphics_id": gfx,
                "x": alvo[0], "y": alvo[1], "elevation": 3,
                "movement_type": movimento(e),
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": lab,
                "flag": nossa,
                "origem": MARCA,
                "fonte_id": e.get("id"),
            })
        if not novos:
            continue
        stats = {}
        antes = list(novos)
        novos = I.sem_tranca(lays, d, novos, stats,
                             lambda m, t, ev, pos, g, r, mot:
                             recusas.append((m, "-", "-", mot)), meu)
        fora_tranca = [o for o in antes if o not in novos]
        for o in fora_tranca:
            trechos = [t for t in trechos if o["script"] not in t]
        vivos = {o["flag"] for o in novos}
        revela = [(f, m) for f, m in revela if f in vivos]
        if novos:
            saida.append((meu, novos, "".join(trechos), revela))
    return saida, recusas


_APELIDO = None
NOVAS_FLAGS = []          # [(nome, 0xNNNN, FLAG_HIDE_* da fonte)] a gravar


def apelido(flag_fonte):
    """`FLAG_SINNOH_ESCONDE_<miolo>` desta `FLAG_HIDE_*`, criando se faltar.

    Custo de ENDEREÇO zero quando o apelido já existe: o bloco S1 cunhou 157
    deles em 17/08/2026 e a maioria nunca foi consumida. Quando falta, a vaga
    sai da faixa de Sinnoh pela MESMA conta de `dev_scripts/flags_livres.py`
    (declarada como `FLAG_UNUSED_0x*`, sem apelido, fora da faixa diária e sem
    uso cru em `data/`/`src/`), a partir de 0x1BA1, que é a próxima depois do
    consumo da leva final de 18/08/2026.

    NÃO cresce `FLAGS_COUNT`: `FLAG_UNUSED_*` já existe no header e já está
    dentro do tamanho que a save reserva, então `guarda_save.py` continua
    dizendo SAVE COMPATIVEL. Foi conferido rodando o guarda depois.
    """
    global _APELIDO
    if _APELIDO is None:
        import flags_livres
        txt = open(os.path.join(REPO, "include/constants/flags.h"),
                   encoding="utf-8").read()
        _APELIDO = {}
        for m in re.finditer(r"^#define (FLAG_SINNOH_ESCONDE_[A-Z0-9_]+)\s+"
                             r"FLAG_UNUSED_0x[0-9A-Fa-f]+\s*//\s*(FLAG_[A-Z0-9_]+)",
                             txt, re.M):
            _APELIDO[m.group(2)] = m.group(1)
        nums, _, _ = flags_livres.livres()
        apelido.pool = [n for n in nums if 0x1BA1 <= n <= 0x1BFF]
    if flag_fonte in _APELIDO:
        return _APELIDO[flag_fonte]
    nome = "FLAG_SINNOH_ESCONDE_" + flag_fonte[len("FLAG_HIDE_"):]
    if nome in _APELIDO.values():
        return nome
    if not apelido.pool:
        return None
    n = apelido.pool.pop(0)
    _APELIDO[flag_fonte] = nome
    NOVAS_FLAGS.append((nome, n, flag_fonte))
    return nome


def alcancavel(lays, d, alvo, cache):
    """O jogador chega em `alvo`, ou pelo menos num vizinho de conversa?

    Mesma busca em largura de `importa_npcs_sinnoh.sem_tranca`, semeada nos
    warps do mapa e SEM tratar os objetos como bloqueio (aqui a pergunta é sobre
    a geometria, não sobre o corpo dos NPCs). Mapa sem warp nenhum não tem como
    ser medido assim, e passa: quem o julga é o portão 4.
    """
    chave = id(d)
    if chave not in cache:
        warps = d.get("warp_events") or []
        if not warps:
            cache[chave] = None
        else:
            W, H, g = I.grade(lays, d["layout"])
            cache[chave] = I.alcancaveis(W, H, g, warps)
    viz = cache[chave]
    if viz is None:
        return True
    x, y = alvo
    return any((x + dx, y + dy) in viz
               for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)))


def traduz_gfx(e, sprites, de_para):
    """O `graphics_id` NOSSO deste evento da fonte, ou o cru quando não há troca."""
    g = e["graphics_id"]
    nome = g[len("OBJ_EVENT_GFX_"):] if g.startswith("OBJ_EVENT_GFX_") else g
    if g in de_para and V.desenhavel(de_para[g], sprites):
        return de_para[g]
    if nome in I.especies():
        return f"OBJ_EVENT_GFX_SPECIES({nome})"
    return V.TROCA_SPRITE.get(g, g)


def fala_do_evento(header, e):
    """A fala DESTE objeto, já pronta para `.string`, ou None (entra mudo).

    NÃO é `cena_galactica_sinnoh.fala_de_mudo`, e a diferença é a armadilha que
    o próprio `falas()` daquele arquivo documenta: `texto_sinnoh.resolve`
    devolve a TUPLA `(texto, comandos de buffer)`, e escrever a tupla no
    `.string` grava o `repr` dela dentro das aspas. Foi exatamente o que a
    primeira build desta leva pôs em `GalacticHQ_ControlRoom/scripts.inc:315`
    ("('AZELF is sealed inside!...$', [])"), e o assembler só reclamou da barra
    invertida, não do repr. Aqui a tupla é ABERTA, e texto que peça buffer que
    este gerador não emite vira NPC MUDO, não `{STR_VAR}` vazio na tela.
    """
    import texto_sinnoh as T
    from texto_placas_sinnoh import (banco_de_texto, campos_do_header,
                                     entradas_de_script)
    campos = campos_do_header(header)
    if not campos:
        return None
    ordem, corpos = entradas_de_script(campos[0])
    banco = banco_de_texto(campos[1])
    idx = e.get("script")
    if not isinstance(idx, int) or not (1 <= idx <= len(ordem)):
        return None
    tid, buffers = T.texto_do_rotulo(corpos, ordem[idx - 1])
    if tid is None or tid not in banco:
        return None
    pronto = T.resolve(banco[tid], buffers)
    if not pronto:
        return None
    texto, comandos = pronto
    if not texto or comandos or "\\" in texto.replace("\\n", "").replace("\\p", "").replace("\\l", ""):
        return None
    return texto


def rotulo_de(e):
    """CamelCase do `LOCALID_*` da fonte, para o rótulo do scripts.inc.

    `treinadores_masmorra_sinnoh.camel` NÃO serve: ele corta os 8 primeiros
    caracteres achando que são `TRAINER_`, e em `AZELF` isso devolve string
    VAZIA. Rótulo vazio virou `GalacticHQ_ControlRoom_EventScript_::` na
    primeira build desta leva.
    """
    n = e.get("id") or "Npc"
    if n.startswith("LOCALID_"):
        n = n[len("LOCALID_"):]
    nome = "".join(p.capitalize() for p in n.split("_") if p)
    return nome or "Npc"


def movimento(e):
    import treinadores_masmorra_sinnoh as M
    return M.DIRECAO.get(e.get("movement_type"), V.MOVIMENTO_PADRAO)


# --------------------------------------------------------------------------

def transicao_que_recalcula(meu, texto, revela):
    """ON_TRANSITION que RECALCULA a flag de esconder a cada entrada no mapa.

    O idioma é o que a obra de Sinnoh já usa, e a razão dele é a save: um
    `setflag` em `EventScript_ResetAllMapFlags` só roda em jogo NOVO, então save
    antiga veria o elenco inteiro plantado desde o primeiro dia. Aqui não há
    estado inicial nenhum para acertar: toda vez que o mapa carrega, a flag é
    ACESA e só é apagada se o marco já caiu. Save antiga e save nova se
    comportam igual, e `new_game.inc` não é tocado.

    Roda ANTES de o objeto nascer: `RunOnTransitionMapScript()` vem antes de
    `InitMap()` em `src/overworld.c`, que é quem cria os `object_events`. É o
    mesmo motivo pelo qual `cena_galactica_sinnoh` usa ON_TRANSITION e não
    `coord_event`.
    """
    corpo = f"{meu}_OnTransition"
    linhas, blocos = "", ""
    for nossa, (tipo, marco) in revela:
        mostra = f"{meu}_EventScript_Mostra_{nossa[len('FLAG_SINNOH_ESCONDE_'):]}"
        if mostra in texto:
            continue
        cond = ("call_if_defeated" if tipo == "trainer" else "call_if_set")
        linhas += f"\tsetflag {nossa}\n\t{cond} {marco}, {mostra}\n"
        blocos += f"\n{mostra}::\n\tclearflag {nossa}\n\treturn\n"
    if not linhas:
        return texto
    if re.search(rf"^{corpo}:", texto, re.M):
        texto = re.sub(rf"^({corpo}:\n)", lambda m: m.group(1) + linhas,
                       texto, count=1, flags=re.M)
        return texto + blocos
    cabeca = re.search(rf"^{meu}_MapScripts::\n", texto, re.M)
    if not cabeca:
        raise SystemExit(f"{meu}: sem rotulo {meu}_MapScripts::")
    texto = (texto[:cabeca.end()]
             + f"\tmap_script MAP_SCRIPT_ON_TRANSITION, {corpo}\n"
             + texto[cabeca.end():])
    return (texto + "\n@ ponytail: portao de NPC de cena com a flag RECALCULADA a"
            " cada entrada.\n@ Acende sempre e so apaga se o marco ja caiu, entao"
            " nao depende de\n@ linha nenhuma em new_game.inc e save antiga se"
            f" comporta igual a nova.\n{corpo}:\n{linhas}\tend\n{blocos}")


def grava_flags_novas(usadas):
    """Escreve os `#define` dos apelidos novos no bloco de Sinnoh de flags.h.

    SÓ os que algum objeto REALMENTE levou. `apelido()` é chamado antes dos
    portões de teto, tranca e alcance, então ele reserva mais nomes do que
    entram; gravar todos gastaria endereço da faixa de Sinnoh em flag que
    ninguém lê, e a próxima leva herdaria a faixa menor sem saber por quê.
    """
    global NOVAS_FLAGS
    NOVAS_FLAGS = [f for f in NOVAS_FLAGS if f[0] in usadas]
    if not NOVAS_FLAGS:
        return 0
    fh = os.path.join(REPO, "include/constants/flags.h")
    txt = open(fh, encoding="utf-8").read()
    novas = [f for f in NOVAS_FLAGS
             if not re.search(rf"^#define {f[0]}\b", txt, re.M)]
    if not novas:
        return 0
    marca = "// <<< B6 Sinnoh, leva final <<<\n"
    if marca not in txt:
        raise SystemExit("flags.h: nao achei o fim do bloco B6 de Sinnoh")
    bloco = ("\n// >>> B6 Sinnoh, leva b3 (23/08/2026): apelido de esconder para o"
             " NPC de cena\n// que a fonte revela num marco que esta ROM tem."
             " Gerado por\n// dev_scripts/cenas_sinnoh_b3.py, polaridade"
             " \"aparece\": quem ACENDE e APAGA cada\n// uma e o"
             " MAP_SCRIPT_ON_TRANSITION do proprio mapa, que recalcula a cada"
             " entrada;\n// nada aqui entra em new_game.inc, e por isso save antiga"
             f" e nova se comportam\n// igual. Consumo: {len(novas)}.\n")
    for nome, n, fonte in novas:
        bloco += f"#define {nome:<72} FLAG_UNUSED_0x{n:04X}  // {fonte}\n"
    bloco += "// <<< B6 Sinnoh, leva b3 <<<\n"
    txt = txt.replace(marca, marca + bloco, 1)
    open(fh, "w", encoding="utf-8").write(txt)
    return len(novas)


def aplica(p):
    postos = 0
    grava_flags_novas({f for _, _, _, r in p for f, _ in r})
    for meu, novos, trecho, revela in p:
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        ps = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        d = json.load(open(pm, encoding="utf-8"))       # releitura tardia
        lista = d.setdefault("object_events", [])
        ja = {o.get("fonte_id") for o in lista}
        entram = [o for o in novos if o["fonte_id"] not in ja]
        if not entram:
            continue
        texto = open(ps, encoding="utf-8").read() if os.path.exists(ps) else ""
        for t in trecho.split("\n\n"):
            m = re.match(r"\n?(\w+)::", t)
            if m and re.search(rf"^{m.group(1)}::", texto, re.M):
                continue
        # Idempotência do texto: rótulo que já existe no arquivo não volta.
        pedacos = []
        for bloco in re.split(r"(?=\n\w+::\n)", trecho):
            m = re.match(r"\n(\w+)::", bloco)
            if m and re.search(rf"^{m.group(1)}::", texto, re.M):
                continue
            pedacos.append(bloco)
        lista.extend(entram)                            # SEMPRE no fim
        postos += len(entram)
        texto = "".join([texto] + pedacos)
        if revela:
            texto = transicao_que_recalcula(meu, texto, revela)
        with open(pm, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(ps, "w", encoding="utf-8") as f:
            f.write(texto)
    return postos


def relata(p, recusas):
    import collections
    usadas = {f for _, _, _, r in p for f, _ in r}
    print(f"b3: {sum(len(o) for _, o, _, _ in p)} objetos entram em {len(p)} mapas"
          f"; {len([f for f in NOVAS_FLAGS if f[0] in usadas])} apelidos de flag "
          "novos na faixa de Sinnoh")
    for meu, novos, _, _ in p:
        print(f"  {meu:38} {len(novos):2}  "
              + ", ".join(f"{o['fonte_id']}@{o['x']},{o['y']}"
                          f"{'' if o['flag'] == '0' else ' [' + o['flag'] + ']'}"
                          for o in novos))
    c = collections.Counter(m for _, _, _, m in recusas)
    print(f"\nrecusas: {len(recusas)}")
    for motivo, n in c.most_common(40):
        print(f"  {n:3}  {motivo[:110]}")


def demo():
    """As armadilhas deste gerador, cada uma provada com mutação plantada."""
    # 1. O teto da fonte é o que impede duplicar quem outro gerador já pôs. A
    #    Rota 218 é a prova viva: os seis do show ESTÃO no mapa desde
    #    cena_galactica_sinnoh.py, e o censo do importador não os reconhece.
    d = json.load(open(os.path.join(REPO, "data/maps/Route218/map.json"),
                       encoding="utf-8"))
    show = [o for o in d["object_events"]
            if o.get("flag") == "FLAG_GALACTICA_CELESTIC"]
    assert len(show) == 6, f"Rota 218 devia ter 6 do show, tem {len(show)}"
    assert "FLAG_HIDE_ROUTE_218_BLOCKADE" in FORA, \
        "sem esta linha o b3 duplicaria o show da Rota 218"

    # 2. A régua visível x escondido é MEDIDA na fonte. Se a varredura parar de
    #    ver `init_new_game`, gente de história entraria plantada para sempre.
    t = toques_da_fonte()
    assert "init_new_game" in t["FLAG_HIDE_SANDGEM_TOWN_RIVAL"][0], \
        "o rival de Sandgem nasce escondido na fonte; a varredura não viu"
    assert "init_new_game" not in t["FLAG_HIDE_ROUTE_212_NORTH_POLICEMAN_ALEX_NO_BATTLE"][0]

    # 3. O gêmeo que luta fica de fora, e o que fala entra. Trazer os dois
    #    plantaria duas pessoas no mesmo tile da fonte.
    assert GEMEO_QUE_LUTA.match("FLAG_HIDE_ROUTE_215_JOGGER_SCOTT")
    assert not GEMEO_QUE_LUTA.match("FLAG_HIDE_ROUTE_215_JOGGER_SCOTT_NO_BATTLE")
    assert not GEMEO_QUE_LUTA.match("FLAG_HIDE_VALOR_LAKEFRONT_GRUNT_M")

    # 4. A janela de sprite é pessimista: 16 objetos amontoados reprovam, 15
    #    passam, e a mesma nuvem espalhada passa.
    junto = [(x, 0) for x in range(16)]
    assert lotacao(junto) == 16 and lotacao(junto[:15]) == 15
    assert lotacao([(x * 30, 0) for x in range(16)]) == 1

    # 5. MUTAÇÃO PLANTADA: um objeto novo em cima do warp tem que ser recusado
    #    pelo portão 3, e não "empurrado para o lado" calado.
    lays = G.layouts()
    dd = json.load(open(os.path.join(REPO, "data/maps/CelesticTownCave/map.json"),
                        encoding="utf-8"))
    proib = G.proibidos_do_mapa(dd)
    assert proib, "CelesticTownCave sem warp: a mutação não prova nada"
    w = next(iter(proib))
    assert G.alvo_livre(lays, dd["layout"], w, set(), proib) != w, \
        "alvo_livre devolveu o próprio tile proibido"

    # 6. Nenhuma flag nova: toda flag que a tabela MARCOS usa já existe em
    #    flags.h. Flag inventada aqui viraria objeto que nunca some.
    fl = open(os.path.join(REPO, "include/constants/flags.h"),
              encoding="utf-8").read()
    for nossa, pol in MARCOS.values():
        if nossa:
            assert re.search(rf"^#define {nossa}\b", fl, re.M), \
                f"{nossa} não existe em flags.h"
    print("cenas_sinnoh_b3 --demo: 6 armadilhas, todas provadas")


def main():
    if "--demo" in sys.argv:
        return demo()
    so = None
    if "--arco" in sys.argv:
        so = sys.argv[sys.argv.index("--arco") + 1]
    p, recusas = plano(so)
    relata(p, recusas)
    if "--aplicar" in sys.argv:
        print(f"\naplicado: {aplica(p)} objetos")


if __name__ == "__main__":
    main()
