#!/usr/bin/env python3
"""Traz NPC, placa e mobiliário de Sinnoh do pokeplatinum para os nossos map.json.

    python3 dev_scripts/importa_npcs_sinnoh.py            # só relata
    python3 dev_scripts/importa_npcs_sinnoh.py --aplicar  # escreve os map.json

A fonte é `fontes-mapas/pokeplatinum/res/field/events/events_*.json`, ligada ao
nosso mapa pelo nome do MAP_HEADER que `include/data/map_headers.h` associa a
cada arquivo de eventos.

Quatro decisões que valem mais que o código, todas tomadas por segurança:

1. **Coordenada.** O `z` deles é o nosso `y` (o `y` deles é altura). Mas mapa de
   rua no Platinum não usa coordenada local: usa coordenada GLOBAL da matriz de
   Sinnoh, e Jubilife começa em x=140, z=743. Pior, os nossos layouts de Sinnoh
   NÃO são os layouts do Platinum (a nossa Jubilife é 70x64; a matriz dela lá tem
   outra forma), então nem descontar o canto da matriz alinha os dois. Medido:
   os deltas entre o mesmo NPC nos dois lados variam de (89,724) a (164,732)
   dentro do MESMO mapa. Não existe offset.
   Por isso: interior (coordenada já local e dentro do nosso layout) entra
   IGUAL; mapa de rua entra por **proporção** da caixa da matriz do Platinum
   sobre o nosso layout, e depois `valida_mapas_sinnoh.py --corrigir` empurra
   quem caiu em tile bloqueado. A posição relativa se mantém, a exata não.
   Quem não couber de jeito nenhum fica de fora, nunca fora do mapa.

2. **`hidden_flag`.** Os `FLAG_HIDE_*` do Platinum não existem aqui. A política é
   NÃO importar objeto com hidden_flag: quem nasce escondido é NPC de história
   (grunt da Galáctica trancando estrada, lendário de lago), e trazer isso sem a
   flag põe um bloqueio permanente no caminho do jogador. Objeto de rua comum tem
   `hidden_flag: "0"` e passa.

3. **`script`.** Lá é número de índice; aqui é rótulo. NPC importado entra MUDO
   (`script: "0"`) e `trainer_type` forçado para NONE, porque treinador sem time
   é batalha contra o vazio. Placa aponta para um rótulo genérico compartilhado.

4. **Mobiliário nunca vira NPC.** Pedra de Strength virada NPC tranca caverna
   para sempre. Toda a lista `GRAFICOS_PROIBIDOS` fica de fora.

   **EMENDA DE 18/08/2026, decisão da condutora.** Esta decisão proíbe virar
   BONECO, e nunca proibiu portar o obstáculo como obstáculo. As 447 pedras de
   `OBJ_EVENT_GFX_ROCK_SMASH` de Sinnoh entram por
   `dev_scripts/pedras_sinnoh.py` como PEDRA de verdade
   (`OBJ_EVENT_GFX_BREAKABLE_ROCK` mais `EventScript_RockSmash`, os dois
   nativos, os mesmos que a Hoenn de fábrica usa na Route 111). Isso é
   fidelidade, não invenção: a fonte tem o obstáculo, e o que a decisão 4
   barrava era transformá-lo em gente. O medo escrito acima continua de pé e
   virou portão medido, não confiança: `pedras_sinnoh.py` prova por busca em
   largura, tratando toda pedra nova como bloqueio e SEM Rock Smash na mochila,
   que ninguém fica preso, e pedra que tranca não entra. Quem for reabrir isto
   leia a seção datada de 18/08 do `PLANO-OBRAS-SINNOH.md` antes.
   O resto da `GRAFICOS_PROIBIDOS` (canteiro, VENT, BOLLARD, pedra de Strength)
   segue de fora, e a régua é a mesma: só sai da lista quem tiver mecânica
   nativa E portão que prove que não tranca.
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import valida_mapas_sinnoh as V  # noqa: E402  reaproveita sprites_utilizaveis e TROCA_SPRITE
import sprites_sinnoh as SPR  # noqa: E402  de-para dos 26 sprites de Sinnoh
# 22/08/2026: os 26 nomes proprios de Sinnoh DEIXARAM de ser "sem sprite aqui".
# `dev_scripts/sprites_sinnoh.py` desenhou os 26, e a tabela mora la porque quem
# desenha e quem sabe o que existe. Aplicada ANTES do filtro NOMES_PROPRIOS.
DE_PARA_SINNOH = SPR.de_para()
import conserta_route222 as R222  # noqa: E402  reaproveita a BFS com regra de elevacao

PLAT = os.path.join(os.path.dirname(REPO), "fontes-mapas/pokeplatinum")
APLICAR = "--aplicar" in sys.argv

# Rótulo único para toda placa importada. Ver decisão 3 no topo.
SCRIPT_PLACA = "Sinnoh_EventScript_PlacaImportada"

# Censo linha a linha de TODO evento da fonte que este gerador olhou: o que
# entrou, onde caiu, por que regra, e o motivo de quem ficou de fora. Artefato,
# não se edita à mão (mesma régua da decisão 10 do plano).
CENSO = os.path.join(REPO, "dev_scripts", "npcs_sinnoh_censo.tsv")

# Marca de origem gravada em cada evento importado. O mapjson ignora campo que
# não conhece, então ela é inerte na ROM e serve para uma coisa só: rodar
# --aplicar duas vezes não pode DOBRAR a população da cidade. Mapa que já tem a
# marca é pulado inteiro, e o script diz quantos pulou.
MARCA = {"origem": "pokeplatinum"}

# Objeto que empurra, bloqueia, dá item ou é cenário: não vira NPC. Decisão 4.
# ponytail: sem esta lista, os 110 BERRY_SOIL, 62 VENT e 16 BOLLARD de Sinnoh
# viravam OBJ_EVENT_GFX_MAN_1 e a cidade ganhava 190 pessoas de pé em cima de
# canteiro. Pedra de Strength virada NPC tranca caverna para sempre.
GRAFICOS_PROIBIDOS = (
    "BOULDER", "ROCK_SMASH", "CUT_TREE", "BREAKABLE", "ITEM_BALL", "POKEBALL",
    "BERRY_TREE", "BERRY_SOIL", "MOVING_BOX", "TRUCK", "MACHINE", "SUBMARINE",
    "VENT", "BOLLARD", "MAILBOX", "BOOK", "MOSS_ROCK", "ICE_ROCK", "SNOWBALL",
    "CAVE_PAINTING", "BRIEFCASE", "_DOOR", "WALL_BLOCKING", "GRUNTS_GROUP",
    "FOSSIL", "OLD_AMBER", "METEORITE", "CLIPBOARD",
)

# Placa do Platinum é objeto, não bg_event. Vira placa nossa em vez de gente.
GRAFICOS_PLACA = ("SIGNBOARD", "ARROW_SIGNPOST", "MAP_SIGNPOST",
                  "TRAINER_TIPS_SIGNPOST", "GYM_SIGNPOST")

# EMENDA DE 22/08/2026: a metade POKÉMON de NOMES_PROPRIOS não é mais pendência.
#
# A lista abaixo nasceu em 05/08/2026, quando esta ROM não tinha sprite de
# overworld de espécie nenhuma, e ela junta duas coisas diferentes: gente de nome
# próprio (Cynthia, Byron, os oito líderes), que continua sem sprite e continua
# de fora, e ESPÉCIE DE POKÉMON, que desde a entrada de Galar (bloco 0.n,
# 22/08/2026) tem sprite de verdade: `OBJ_EVENT_GFX_SPECIES(NOME)` já é usado
# 1.811 vezes nos nossos map.json e `valida_mapas_sinnoh.desenhavel` já o
# reconhece pela forma. Ou seja: pôr o Magikarp do leito do Lago Valor como
# MAGIKARP não é "trocar por genérico", é o sprite CERTO, e a decisão do Gui de
# 05/08 (o mapa não pode mentir) manda pôr, não deixar de fora.
#
# A régua é o nome: gfx da fonte cujo miolo é uma `SPECIES_*` deste fork vira
# espécie; o resto segue a regra velha. Nada é digitado à mão, a lista sai de
# `include/constants/species.h`.
_ESPECIES = None


def especies():
    """Nomes de espécie deste fork, lidos de include/constants/species.h."""
    global _ESPECIES
    if _ESPECIES is None:
        txt = open(os.path.join(REPO, "include/constants/species.h")).read()
        _ESPECIES = set(re.findall(r"\bSPECIES_([A-Z0-9_]+)\b", txt))
        _ESPECIES -= {"NONE", "EGG", "COUNT", "TABLES_TERMIN", "OLD_UNOWN_B"}
    return _ESPECIES


# GRUPO DE `hidden_flag` CUJA CENA JÁ EXISTE NESTA ROM (balde b1).
#
# A decisão 2 do topo continua valendo palavra por palavra: objeto com flag SEM
# a cena que a apaga planta bloqueio permanente. O que muda aqui é que para
# estes grupos a cena EXISTE, com `setflag` escrito em mapa nosso e provado em
# suíte, então o objeto pode entrar carregando a NOSSA flag e some no mesmo
# instante em que o resto do grupo já some hoje. Cada linha foi conferida com
# `grep setflag` em data/maps antes de entrar; quem não tiver cena não entra.
GRUPOS_COM_CENA = {
    # os 20 grunts do Hall do QG já estão no mapa com esta flag (map.json feito
    # à mão); o resto do grupo é o MESMO momento de enredo, a queda do Saturn.
    "FLAG_HIDE_GALACTIC_HQ_HALL_GRUNTS": "FLAG_GALACTICA_QG_TOMADO",
    # decisão da condutora, 17/08/2026 (PLANO-OBRAS-SINNOH.md): semântica
    # idêntica à do Hall. setflag em GalacticHQ_1F:203 e GalacticHQ_2F:191.
    "FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC": "FLAG_GALACTICA_QG_TOMADO",
    # cena da espinha: setflag em SpearPillar, MtCoronet3F/4F/5F/6F,
    # MtCoronet_1F_North_Room1 e MtCoronet1FTunnelRoom.
    "FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS": "FLAG_GALACTICA_MT_CORONET",
    "FLAG_HIDE_SPEAR_PILLAR_GRUNTS": "FLAG_GALACTICA_MT_CORONET",
    # setflag em EternaCity:19, TeamGalacticEternaBuilding_3F:76 e _4F:31.
    "FLAG_HIDE_ETERNA_CITY_GALACTIC_GRUNTS": "FLAG_GALACTICA_ETERNA",
    # setflag em LakeVerity/scripts.inc (a Mars cai e somem ela e os grunts).
    "FLAG_HIDE_LAKE_VERITY_TEAM_GALACTIC": "FLAG_GALACTICA_LAGO_VERITY",
    # setflag em ValleyWindworks, FloaromaTown e Route205_South.
    "FLAG_HIDE_VALLEY_WINDWORKS_BUILDING_TEAM_GALACTIC": "FLAG_GALACTICA_WINDWORKS",
    "FLAG_HIDE_VALLEY_WINDWORKS_BUILDING_GALACTIC_GRUNT_1": "FLAG_GALACTICA_WINDWORKS",
    "FLAG_HIDE_VALLEY_WINDWORKS_OUTSIDE_GRUNT_M": "FLAG_GALACTICA_WINDWORKS",
    # setflag em JubilifeCity/scripts.inc.
    "FLAG_HIDE_JUBILIFE_GALACTIC_GRUNTS": "FLAG_GALACTICA_JUBILIFE",
    # setflag em CelesticTown/scripts.inc.
    "FLAG_HIDE_CELESTIC_TOWN_GRUNT_M": "FLAG_GALACTICA_CELESTIC",
    # os dois guardas da porta do QG em Veilstone ja usam esta flag no nosso
    # map.json (VeilstoneCity/scripts.inc:15 e :32).
    "FLAG_HIDE_VEILSTONE_GALACTIC_GRUNTS": "FLAG_GALACTICA_QG_TOMADO",
}


# FLAG MORTA DA FONTE: ninguem acende, ninguem apaga, logo o objeto e VISIVEL.
#
# Terceiro caminho do balde (b), e o mais barato dos tres, porque nao pede cena
# nenhuma: o campo `hidden_flag` do evento cita uma flag que NENHUM script e
# NENHUM .c do pokeplatinum toca. Flag que ninguem acende nasce apagada, e no
# motor da fonte objeto de flag apagada aparece: ou seja, no jogo ORIGINAL essa
# gente esta sempre la. Recusa-los "por seguranca" nao era seguranca, era mapa
# vazio de graca.
#
# A lista NAO se escreve a mao: `flags_mortas_da_fonte()` varre
# `res/field/scripts`, `src` e `include` do pokeplatinum e considera morta a
# flag que so aparece dentro dos proprios `res/field/events/*.json` (e no
# `generated/vars_flags.txt`, que e so o enum). Medido em 22/08/2026: 372 flags
# distintas, 486 objetos.
#
# DUAS EXCLUSOES, e as duas sao medida e nao gosto:
#   - `FLAG_MAP_LOCAL_HIDE_OBSTACLE_*` fica de fora: e a familia de obstaculo
#     que o motor da fonte administra em C por mapa, e todo objeto dela e pedra
#     ou bloco, que `pedras_sinnoh.py` ja traz como obstaculo de verdade;
#   - quem esta em GRUPOS_COM_CENA tem precedencia, porque ali a NOSSA ROM tem
#     cena e a flag nossa e melhor que flag nenhuma.
_VIVAS = None


_CENA_NOSSA = None


def cena_nossa(hf):
    """Nome da NOSSA flag quando a cena deste grupo ja existe em data/maps.

    O bloco `B6 Sinnoh, flags dos grupos de hidden_flag` de
    `include/constants/flags.h` guarda, em comentario, o `FLAG_HIDE_*` da fonte
    que cada `FLAG_SINNOH_ESCONDE_*` apelida. Quando esse apelido JA APARECE num
    scripts.inc nosso, o grupo tem dono: a cena faz `clearflag` + `addobject` num
    LOCALID especifico, e plantar um segundo corpo com a mesma flag faria a cena
    revelar DOIS. Nesse caso o objeto continua fora, e o motivo do censo passa a
    dizer de quem e a cena, em vez de repetir "decisao 2".
    """
    global _CENA_NOSSA
    if _CENA_NOSSA is None:
        import glob as _glob
        alias = {}
        for ln in open(os.path.join(REPO, "include/constants/flags.h"),
                       encoding="utf-8"):
            m = re.match(r"#define (FLAG_SINNOH_[A-Z0-9_]+)\s+FLAG_UNUSED_"
                         r"0x[0-9A-Fa-f]+\s*//\s*(FLAG_[A-Z0-9_]+)", ln)
            if m:
                alias[m.group(2)] = m.group(1)
        txt = "".join(open(a, encoding="utf-8", errors="ignore").read()
                      for a in _glob.glob(os.path.join(REPO,
                                                       "data/maps/*/scripts.inc")))
        usadas = set(re.findall(r"\bFLAG_SINNOH_[A-Z0-9_]+", txt))
        _CENA_NOSSA = {k: v for k, v in alias.items() if v in usadas}
    return _CENA_NOSSA.get(hf)


def flag_morta(hf):
    """True quando NENHUM script e NENHUM .c/.h do pokeplatinum toca esta flag."""
    if hf.startswith("FLAG_MAP_LOCAL"):
        return False
    return hf not in _flags_vivas_da_fonte()


def _flags_vivas_da_fonte():
    global _VIVAS
    if _VIVAS is None:
        import glob as _glob
        vivas = set()
        for raiz in ("res/field/scripts", "src", "include"):
            for arq in _glob.glob(os.path.join(PLAT, raiz, "**", "*"),
                                  recursive=True):
                if not os.path.isfile(arq):
                    continue
                try:
                    txt = open(arq, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                vivas.update(re.findall(r"\bFLAG_[A-Z0-9_]+", txt))
        _VIVAS = vivas
    return _VIVAS

# GRUPO DE `hidden_flag` QUE NÃO É ENREDO: é RODÍZIO (balde b2).
#
# Aqui a `hidden_flag` da fonte não guarda marco de história nenhum: ela sorteia
# quem aparece HOJE, e o dia seguinte sorteia outro. Lido no script da fonte,
# não deduzido:
#
#   `res/field/scripts/scripts_restaurant.s` acende as NOVE flags de casal em
#   `Restaurant_ResetTrainers` e depois `ClearFlag` num subconjunto sorteado por
#   `GetRandom`, e acende TODAS de novo entre 23h e 9h (`Restaurant_SetClosed`);
#   `res/field/scripts/scripts_pokemon_center_daily_trainers.s` faz o mesmo com
#   o treinador do dia dos Pokécenters.
#
# Ou seja: NÃO existe cena que "apaga a flag para sempre", e esperar por ela é
# esperar por nada. O medo da decisão 2 (objeto escondido para sempre virando
# bloqueio) também não se aplica: aqui o objeto entra VISÍVEL e mudo, e o
# restaurante fica sempre cheio em vez de sempre vazio. O que segura o risco de
# corpo em corredor é o portão 5 (`sem_tranca`), não a flag.
GRUPOS_SEM_ENREDO = frozenset({
    "FLAG_HIDE_RESTAURANT_ISMAEL_HARLEY", "FLAG_HIDE_RESTAURANT_ROMAN_KYLIE",
    "FLAG_HIDE_RESTAURANT_LEONARDO_REBECCA", "FLAG_HIDE_RESTAURANT_EUGENE_ALISON",
    "FLAG_HIDE_RESTAURANT_ESTEBAN_MEREDITH", "FLAG_HIDE_RESTAURANT_EMANUEL_BLYTHE",
    "FLAG_HIDE_RESTAURANT_DARRYL_VALERIE", "FLAG_HIDE_RESTAURANT_KENDRICK_GABRIELLA",
    "FLAG_HIDE_RESTAURANT_EMILIO_KAYLEE",
    "FLAG_HIDE_POKECENTER_DAILY_TRAINER_1", "FLAG_HIDE_POKECENTER_DAILY_TRAINER_2",
})


# BALDE (a) LIBERADO EM 23/08/2026: quem tem sprite PROPRIO agora entra.
#
# A lista `NOMES_PROPRIOS` abaixo continua sendo a de 05/08/2026 e continua
# querendo dizer a mesma coisa: gente de nome proprio nao vira boneco generico,
# porque lider de ginasio com cara de nadador e o mapa mentindo. O que mudou nao
# foi a decisao, foi o ESTOQUE: os 26 sprites `OBJ_EVENT_GFX_SINNOH_*` (Candice,
# Cynthia, Cyrus, Byron, Roark, os oito lideres, os comandantes, o Looker...)
# passaram a existir nesta ROM. A regua agora e de-para pelo NOME, e ela NAO se
# escreve a mao: procura-se `OBJ_EVENT_GFX_SINNOH_<NOME>` na tabela de graficos
# que a build realmente desenha (`valida_mapas_sinnoh.sprites_utilizaveis`), e
# quem nao estiver la continua de fora com o motivo antigo. Hoje o unico que
# sobra e o GAME_DIRECTOR. Personagem com `hidden_flag` segue a regra do balde
# (b) como qualquer outro objeto: sprite nao e passe livre para entrar em cena
# que nao existe.
def sprite_proprio(sprites, _c={}):
    """{NOME da fonte: OBJ_EVENT_GFX_SINNOH_NOME} que esta build desenha."""
    if not _c:
        _c.update({n: f"OBJ_EVENT_GFX_SINNOH_{n}" for n in NOMES_PROPRIOS
                   if f"OBJ_EVENT_GFX_SINNOH_{n}" in sprites})
    return _c


# SPRITE PROPRIO SO ENTRA EM OBJETO QUE NAO CONTRADIZ, 23/08/2026.
#
# O de-para de `sprite_proprio()` casa pelo NOME DO OBJETO DA FONTE, e a fonte
# rotula como MARS o objeto de CENA da comandante em `ValleyWindworksBuilding`:
# ela aparece, fala e some, e quem fica no mapa e o pai da familia. O casamento
# do sprite com o objeto NOSSO era por VIZINHANCA pura (<= 1 tile, com script
# qualquer), entao a cara da Mars foi parar no objeto cujo script e a fala
# portada que comeca com "Papa:". Sprite e script sao as duas metades da mesma
# afirmacao de identidade, e discordar e o mapa mentindo, que e exatamente o
# que a decisao do Gui de 05/08/2026 proibe.
#
# A regra agora: objeto nosso so recebe o sprite proprio de uma pessoa quando
#   - ele e MUDO (`script` "0"): nao afirma ser ninguem, e o sprite so da cara
#     ao corpo que a fonte pos ali; ou
#   - o script dele E DA PESSOA: o nome dela aparece no ROTULO ou no texto
#     alcancavel a partir dele (a fala, a constante de treinador, o rotulo de
#     uma sub-rotina). E assim que a Candice de Snowpoint continua passando: o
#     rotulo dela e `_EventScript_Leader`, mudo sobre o nome, mas o corpo tem
#     `TRAINER_SINNOH_LEADER_CANDICE`.
# Quem nao passa fica com o sprite generico que ja tinha, e o censo diz por que.
def blocos_de_script(_c={}):
    """{rotulo: corpo} de todo .inc de script do repo, lido uma vez."""
    if _c:
        return _c
    import glob
    arqs = (glob.glob(f"{REPO}/data/maps/*/scripts.inc")
            + glob.glob(f"{REPO}/data/scripts/*.inc"))
    for caminho in arqs:
        try:
            texto = open(caminho, encoding="utf-8").read()
        except OSError:
            continue
        rot, corpo = None, []
        for l in texto.split("\n"):
            m = re.match(r"^([A-Za-z_]\w*):{1,2}\s*$", l)
            if m:
                if rot:
                    _c.setdefault(rot, "\n".join(corpo))
                rot, corpo = m.group(1), []
            elif rot:
                corpo.append(l)
        if rot:
            _c.setdefault(rot, "\n".join(corpo))
    return _c


def texto_do_script(rotulo, teto=40):
    """Todo o texto ALCANCAVEL a partir de `rotulo`, rotulos seguidos inclusive.

    Sem seguir os saltos a Candice reprovaria por acidente: o `goto_if_set` dela
    leva a um rotulo, e o nome da pessoa costuma estar do outro lado do salto.
    """
    blocos = blocos_de_script()
    vistos, fila, saida = set(), [rotulo], [rotulo]
    while fila and len(vistos) < teto:
        r = fila.pop()
        if r in vistos or r not in blocos:
            continue
        vistos.add(r)
        corpo = blocos[r]
        saida.append(corpo)
        for s in re.findall(r"[A-Za-z_]\w*", corpo):
            if s in blocos and s not in vistos:
                fila.append(s)
    return "\n".join(saida)


def script_e_da_pessoa(nome, rotulo):
    """O script `rotulo` fala como `nome` (MARS, CRASHER_WAKE, ...)?"""
    if not rotulo or str(rotulo) in ("0", ""):
        return True   # objeto mudo nao afirma identidade nenhuma
    alvo = re.escape(nome.upper())
    return bool(re.search(r"(?<![A-Z])%s(?![A-Z])" % alvo,
                          texto_do_script(str(rotulo)).upper()))


def pode_vestir(obj, proprio):
    """(pode, motivo). Portao unico dos DOIS pontos que repintam objeto nosso."""
    nome = proprio.replace("OBJ_EVENT_GFX_SINNOH_", "")
    rot = str(obj.get("script", "0"))
    if script_e_da_pessoa(nome, rot):
        return True, None
    return False, ("script %s nao fala como %s: sprite generico %s fica"
                   % (rot, nome, obj.get("graphics_id")))


# Personagem com nome próprio e Pokémon: sem sprite aqui, e trocar por genérico
# faz o mapa mentir (líder de ginásio com cara de nadador). Fica de fora e é
# registrado em PENDENCIAS-NPC-SINNOH.md. Decisão do Gui, 05/08/2026.
NOMES_PROPRIOS = (
    "CYNTHIA", "CYRUS", "MARS", "JUPITER", "SATURN", "CHARON", "ROARK",
    "GARDENIA", "MAYLENE", "CRASHER_WAKE", "FANTINA", "BYRON", "CANDICE",
    "VOLKNER", "AARON", "BERTHA", "FLINT", "LUCIAN", "PALMER", "LOOKER",
    "BUCK", "MIRA", "CHERYL", "MARLEY", "RILEY", "JASMINE", "GAME_DIRECTOR",
    "UXIE", "AZELF", "MESPRIT", "ARCEUS", "DARKRAI", "SHAYMIN", "HEATRAN",
    "REGIGIGAS", "CRESSELIA", "GIRATINA", "ROTOM", "PACHIRISU", "BUNEARY",
    "CROAGUNK", "HAPPINY", "STARLY", "DRIFLOON", "MAGIKARP", "TORCHIC",
    "SHROOMISH",
)

# Mapa que outro agente está editando neste bloco, ou que não faz sentido povoar.
#
# TRAVA DE ESCRITA, NUNCA RÉGUA DE MEDIÇÃO. Até 11/08/2026 esta lista era
# descontada dentro de `nossos_mapas_sinnoh()`, que é a régua que o
# `completude.py` usa: `CanalaveCity_Gym` e `SandgemTown_House1` estão na ROM e
# no `map_groups.json` e mesmo assim contavam como ausentes, exatamente o mesmo
# defeito de medida que segurava as seis salas da Elite dos Quatro por causa do
# nome. Quem não pode escrever agora não é quem não existe: use
# `mapas_editaveis_sinnoh()` para escrever e `nossos_mapas_sinnoh()` para medir.
NAO_TOCAR = ("CanalaveCity_Gym", "SandgemTown_House1")

# Nome que a normalização não casa sozinha. Nosso mapa -> MAP_HEADER do Platinum.
APELIDOS = {
    # Os três andares da Victory Road de Sinnoh entram com prefixo de região
    # porque `MAP_VICTORY_ROAD_1F` e `LAYOUT_VICTORY_ROAD_1F` já são de HOENN
    # (ver `fecha_portas_sinnoh.RENOMEADOS`). Sem estes três pares o mapa
    # existiria na ROM e `completude.py` continuaria contando ele como ausente.
    "SinnohVictoryRoad1F": "MAP_HEADER_VICTORY_ROAD_1F",
    "SinnohVictoryRoad2F": "MAP_HEADER_VICTORY_ROAD_2F",
    "SinnohVictoryRoadB1F": "MAP_HEADER_VICTORY_ROAD_B1F",
    "TwinleafTown_MainHouse_1F": "MAP_HEADER_TWINLEAF_TOWN_PLAYER_HOUSE_1F",
    "TwinleafTown_MainHouse_2F": "MAP_HEADER_TWINLEAF_TOWN_PLAYER_HOUSE_2F",
    "Twinleaf_Town_RivalsHouse_F1": "MAP_HEADER_TWINLEAF_TOWN_RIVAL_HOUSE_1F",
    "Twinleaf_Town_RivalsHouse_F2": "MAP_HEADER_TWINLEAF_TOWN_RIVAL_HOUSE_2F",
    "TwinleafTown_Haouse1": "MAP_HEADER_TWINLEAF_TOWN_NORTHEAST_HOUSE",
    "TwinleafTown_House2": "MAP_HEADER_TWINLEAF_TOWN_SOUTHWEST_HOUSE",
    "SandgemTown_RowanLab": "MAP_HEADER_SANDGEM_TOWN_POKEMON_RESEARCH_LAB",
    "SandgemTown_House1": "MAP_HEADER_SANDGEM_TOWN_HOUSE",
    "SandgemTown_RivalHouse_F1": "MAP_HEADER_SANDGEM_TOWN_COUNTERPART_HOUSE_1F",
    "SandgemTown_RivalHouse_F2": "MAP_HEADER_SANDGEM_TOWN_COUNTERPART_HOUSE_2F",
    "JubilifeCity_Flat1_F1": "MAP_HEADER_JUBILIFE_CITY_CONDOMINIUMS_1F",
    "JubilifeCity_Flat1_F2": "MAP_HEADER_JUBILIFE_CITY_CONDOMINIUMS_2F",
    "JubilifeCity_Flat2_F1": "MAP_HEADER_JUBILIFE_CITY_SOUTH_HOUSE_1F",
    "JubilifeCity_Flat2_F2": "MAP_HEADER_JUBILIFE_CITY_SOUTH_HOUSE_2F",
    "JubilifeCity_Flat3_F1": "MAP_HEADER_JUBILIFE_CITY_SOUTHWEST_HOUSE_1F",
    "JubilifeCity_Flat3_F2": "MAP_HEADER_JUBILIFE_CITY_SOUTHWEST_HOUSE_2F",
    "JubilifeCity_JubilifeTV_F1": "MAP_HEADER_JUBILIFE_TV_1F",
    "JubilifeCity_JubilifeTV_F2": "MAP_HEADER_JUBILIFE_TV_2F",
    "JubilifeCity_JubilifeTV_F3": "MAP_HEADER_JUBILIFE_TV_3F",
    "JubilifeCity_JubilifeTV_F4": "MAP_HEADER_JUBILIFE_TV_4F",
    "JubilifeCity_PoketchCompany_F1": "MAP_HEADER_POKETCH_CO_1F",
    "JubilifeCity_PoketchCompany_F2": "MAP_HEADER_POKETCH_CO_2F",
    "JubilifeCity_PoketchCompany_F3": "MAP_HEADER_POKETCH_CO_3F",
    "JubilifeCity_PokemonSchool": "MAP_HEADER_TRAINERS_SCHOOL",
    "OreburghCity_Flat1_F1": "MAP_HEADER_OREBURGH_CITY_NORTHWEST_HOUSE_1F",
    "OreburghCity_Flat1_F2": "MAP_HEADER_OREBURGH_CITY_NORTHWEST_HOUSE_2F",
    "OreburghCity_Flat2_F1": "MAP_HEADER_OREBURGH_CITY_NORTH_HOUSE_1F",
    "OreburghCity_Flat2_F2": "MAP_HEADER_OREBURGH_CITY_NORTH_HOUSE_2F",
    "OreburghCity_Flat3_F1": "MAP_HEADER_OREBURGH_CITY_EAST_HOUSE_1F",
    "OreburghCity_Flat3_F2": "MAP_HEADER_OREBURGH_CITY_EAST_HOUSE_2F",
    "OreburghCity_House1": "MAP_HEADER_OREBURGH_CITY_MIDDLE_HOUSE",
    "OreburghCity_House2": "MAP_HEADER_OREBURGH_CITY_WEST_HOUSE",
    "OreburghCity_House3": "MAP_HEADER_OREBURGH_CITY_SOUTH_HOUSE",
    "FloaromaTown_House1": "MAP_HEADER_FLOAROMA_TOWN_SOUTHEAST_HOUSE",
    "FloaromaTown_House2": "MAP_HEADER_FLOAROMA_TOWN_MIDDLE_HOUSE",
    "FloaromaTwon_PokemonCenter_2F": "MAP_HEADER_FLOAROMA_TOWN_POKECENTER_2F",
    "ValleyWindworks": "MAP_HEADER_VALLEY_WINDWORKS_OUTSIDE",
    "SinnohLeague_Entrance": "MAP_HEADER_POKEMON_LEAGUE",
    # As seis salas da Elite dos Quatro de Sinnoh JA ESTAO na ROM desde
    # `20ac2eaac4`, e as batalhas foram provadas no emulador em `T82.1` a
    # `T82.5`. `completude.py` contava as seis como ausentes porque o nome daqui
    # e `SinnohLeague_*` e o do Platinum e `POKEMON_LEAGUE_*`: mapa que existe
    # sumindo da conta por causa do nome e o mesmo defeito de regua que segurava
    # Unova em `Rt5NimbasaGate`. Nada de mapa entra aqui, so a medida acerta.
    "SinnohLeague_AaronsRoom": "MAP_HEADER_POKEMON_LEAGUE_AARON_ROOM",
    "SinnohLeague_BerthasRoom": "MAP_HEADER_POKEMON_LEAGUE_BERTHA_ROOM",
    "SinnohLeague_FlintsRoom": "MAP_HEADER_POKEMON_LEAGUE_FLINT_ROOM",
    "SinnohLeague_LuciansRoom": "MAP_HEADER_POKEMON_LEAGUE_LUCIAN_ROOM",
    "SinnohLeague_ChampionsRoom": "MAP_HEADER_POKEMON_LEAGUE_CHAMPION_ROOM",
    "SinnohLeague_HallOfFame": "MAP_HEADER_POKEMON_LEAGUE_HALL_OF_FAME",
    # Mesmo caso, por nome de predio: a loja de flores de Floaroma e
    # `MAP_HEADER_FLOWER_SHOP` la, sem o nome da cidade na frente.
    "FloaromaTown_FlowerShop": "MAP_HEADER_FLOWER_SHOP",
    # Os 3F dos dois predios de Jubilife que ja estao na ROM. No Platinum eles
    # sao os andares marcados UNUSED do MESMO predio (Flat1 e o condominio,
    # Flat2 e a casa do sul); Flat3 nao entra porque a casa do sudoeste do
    # Platinum so tem 1F e 2F, entao o nosso 3F nao tem par la.
    "JubilifeCity_Flat1_F3": "MAP_HEADER_UNUSED_JUBILIFE_CITY_CONDOMINIUMS_3F",
    "JubilifeCity_Flat2_F3": "MAP_HEADER_UNUSED_JUBILIFE_CITY_SOUTH_HOUSE_3F",
    "SunyshoreCity_Gym": "MAP_HEADER_SUNYSHORE_CITY_GYM_ROOM_1",
    "HearthomeCity_Gym": "MAP_HEADER_HEARTHOME_CITY_GYM_ENTRANCE_ROOM",
    "Route204": "MAP_HEADER_ROUTE_204_SOUTH",
    "Route206_North": "MAP_HEADER_ROUTE_206_CYCLING_ROAD_NORTH_GATE",
    "Route206_South": "MAP_HEADER_ROUTE_206_CYCLING_ROAD_SOUTH_GATE",
    "Route208_Access": "MAP_HEADER_ROUTE_208_GATE_TO_HEARTHOME_CITY",
    "Route209_Access": "MAP_HEADER_ROUTE_209_GATE_TO_HEARTHOME_CITY",
    "Route212_Access": "MAP_HEADER_ROUTE_212_GATE_TO_HEARTHOME_CITY",
    "Route213_Access": "MAP_HEADER_ROUTE_213_GATE_TO_PASTORIA_CITY",
    "Route214_Access": "MAP_HEADER_ROUTE_214_GATE_TO_VEILSTONE_CITY",
    "Route215_Access": "MAP_HEADER_ROUTE_215_GATE_TO_VEILSTONE_CITY",
    "Route218_East": "MAP_HEADER_ROUTE_218_GATE_TO_JUBILIFE_CITY",
    "Route218_West": "MAP_HEADER_ROUTE_218_GATE_TO_CANALAVE_CITY",
    "Route222_Access": "MAP_HEADER_ROUTE_222_GATE_TO_SUNYSHORE_CITY",
    "Route225_Access": "MAP_HEADER_ROUTE_225_GATE_TO_FIGHT_AREA",
    "Route226_Access": "MAP_HEADER_ROUTE_226_HOUSE",
    "HotelGrandLake": "MAP_HEADER_GRAND_LAKE_ROUTE_213_LOBBY",
    # O `DistortionWorld` esta na ROM desde 21/08/2026 (dev_scripts/
    # distortion_world.py) e a regua contava ele como AUSENTE por causa do
    # nome: a pasta e `DistortionWorld` e o header e o da SALA DO GIRATINA. E o
    # mesmo defeito de medida das seis salas da Elite dos Quatro. Nada de mapa
    # entra aqui, so a medida acerta.
    "DistortionWorld": "MAP_HEADER_DISTORTION_WORLD_GIRATINA_ROOM",
}

# Prefixos que identificam mapa de Sinnoh no nosso data/maps.
PREFIXOS = V.PREFIXOS_SINNOH


def nossos_mapas_sinnoh():
    """ponytail: o prefixo "Route2" de valida_mapas_sinnoh.py pega Route26 a
    Route29, que são de Johto, e "Lake" pega LakeOfRage. Rota de Sinnoh tem
    três dígitos (201 a 230), e é assim que elas se separam."""
    base = os.path.join(REPO, "data/maps")
    # ponytail: prefixo nao alcanca predio de nome proprio (Cafe, Villa,
    # GameCorner, CycleShop, PokemonDayCare). O grupo alcanca: mapa que mora num
    # grupo com "Sinnoh" no nome E de Sinnoh, sem lista de nome para envelhecer.
    grupos = json.load(open(os.path.join(base, "map_groups.json")))
    por_grupo = {m for g in grupos.get("group_order", []) if "sinnoh" in g.lower()
                 for m in grupos.get(g, [])}

    def da_regiao(n):
        if n in por_grupo:
            return True
        if n.startswith("Route"):
            # sem ancora no fim: "Route205House" e de Sinnoh tanto quanto
            # "Route205_South". Route26 a Route29 (Johto) tem dois digitos e
            # nao casam com Route2[0-3]\d, que exige tres.
            return bool(re.match(r"Route2[0-3]\d", n))
        if n.startswith("LakeOfRage"):
            return False
        return any(n.startswith(p) for p in PREFIXOS)
    return [n for n in sorted(os.listdir(base))
            if not n.endswith("_Frlg") and da_regiao(n)
            and os.path.exists(os.path.join(base, n, "map.json"))]


def mapas_editaveis_sinnoh():
    """A régua MENOS a trava de escrita. Só quem VAI ESCREVER usa esta lista.

    Separada de `nossos_mapas_sinnoh()` em 11/08/2026: quem mede quanto de
    Sinnoh existe não pode perder mapa que existe só porque outro agente está
    editando ele hoje.
    """
    return [n for n in nossos_mapas_sinnoh() if n not in NAO_TOCAR]


def headers_do_platinum():
    """MAP_HEADER_X -> (arquivo de eventos, id da matriz)."""
    txt = open(os.path.join(PLAT, "include/data/map_headers.h")).read()
    fora = {}
    for bloco in re.finditer(r"\[(MAP_HEADER_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},",
                             txt, re.S):
        nome, corpo = bloco.group(1), bloco.group(2)
        ev = re.search(r"\.eventsArchiveID\s*=\s*(\w+)", corpo)
        mx = re.search(r"\.mapMatrixID\s*=\s*(\w+)", corpo)
        if ev and ev.group(1).startswith("events_"):
            fora[nome] = (ev.group(1), mx.group(1) if mx else None)
    return fora


SINONIMOS = [
    ("pokemoncenter", "pokecenter"), ("pokmoncenter", "pokecenter"),
    ("pokemonleague", "pokemonleague"), ("pokmonleague", "pokemonleague"),
    ("condominiums", "flat"), ("apartments", "flat"),
    ("trainersschool", "pokemonschool"), ("poketchco", "poketchcompany"),
    ("jubilifetv", "jubilifecityjubilifetv"),
]


def chave(nome):
    n = nome.lower().replace("_", "").replace("-", "")
    n = re.sub(r"^mapheader", "", n)
    for a, b in SINONIMOS:
        n = n.replace(a, b)
    n = re.sub(r"f(\d)$", r"\1f", n)      # _F1 e 1F são o mesmo andar
    n = re.sub(r"b(\d)f$", r"b\1f", n)
    n = n.replace("route2", "route2")
    return n


def caixa_da_matriz(matriz_id, header):
    """Canto e tamanho, em tiles, que o header ocupa na matriz do Platinum."""
    p = os.path.join(PLAT, "res/field/matrices", f"{matriz_id}.json")
    if not os.path.exists(p):
        return None
    grade = json.load(open(p))["headers"]
    cels = [(r, c) for r, linha in enumerate(grade)
            for c, h in enumerate(linha) if h == header]
    if not cels:
        return None
    r0 = min(r for r, _ in cels); r1 = max(r for r, _ in cels)
    c0 = min(c for _, c in cels); c1 = max(c for _, c in cels)
    return c0 * 32, r0 * 32, (c1 - c0 + 1) * 32, (r1 - r0 + 1) * 32


# Mapa cujo layout AQUI e REDESENHO 1 PARA 1 da caixa da matriz do Platinum: a
# conversao certa e TRANSLACAO, e a escala proporcional abaixo e que esta
# errada. Nao e palpite, e o que os WARPS do proprio mapa provam (ver
# `deslocamento_de_warp`): eles existem nos dois arquivos, sao poucos e
# inequivocos, e se UM deslocamento unico leva todos os nossos aos da fonte,
# entao a planta e a mesma e so foi transladada.
#
# MEDIDO em 18/08/2026 na Route 222, e foi o que tirou tres placas de dentro de
# parede. A escala comprime o x (a caixa da fonte tem 96 colunas, o nosso layout
# tem 92, e `int(x*91/95)` engole ate 4 tiles), enquanto os warps das duas casas
# batem exatos em dx=736 / dz=767: as portas da fonte (795,784) e (801,784) sao
# as nossas (59,17) e (65,17). Com a translacao, as placas caem em (57,17),
# (68,17), (85,17) e (13,20): duas delas na parede logo ao lado de cada porta,
# com o tile de leitura andavel embaixo, exatamente como a fonte desenha (la a
# placa fica 2 tiles a esquerda de uma porta e 3 a direita da outra, e aqui
# tambem). Pela escala elas caiam em (54,16) e (65,16), no meio da faixa de
# parede das linhas 15-17, sem NENHUM vizinho andavel: placa que o jogador nunca
# consegue ler.
#
# POR QUE UMA LISTA e nao o teste rodando em todo mapa: o teste de warp passa em
# 50 mapas de Sinnoh e mudaria a conversao de 8 deles (EternaCityCondominiums2F,
# FloaromaTown, HearthomeCity_Gym, HotelGrandLake, Route205_North, Route221,
# Route222, WaywardCave1F), com 15 placas ja gravadas. Mover placa ja gravada e
# conteudo, e conteudo se mede um a um: cada uma tem que ser conferida na grade
# de colisao antes, como as quatro da Route 222 foram. Quem for medir o proximo
# mapa acrescenta o header aqui, move as placas dele no map.json na mesma
# rodada, e escreve a medicao junto. Sem mover as placas, `itens_escondidos_
# sinnoh.alinha_por_coordenada` passa a ver orfao e recusa o mapa inteiro.
# LISTA AUTORIZADA, e entrar nela e DECISAO MEDIDA, nunca automatica: o teste de
# warp diz que a translacao e possivel, nao que as placas ja gravadas do mapa
# caem em tile legivel depois de mover. Os outros 7 mapas que passam no teste
# estao na FILA DE CONTEUDO (dev_scripts/fila_b6.py,
# "sinnoh:placas:7_mapas_por_escala"), com o criterio de aceite escrito.
REDESENHO_1PARA1 = {
    "MAP_HEADER_ROUTE_222",
}


def deslocamento_de_warp(fonte, nosso):
    """(dx, dz) UNICO que leva todo warp NOSSO a um warp da fonte, ou None.

    Criterio de "este layout e a planta da fonte transladada". Warp e a melhor
    testemunha que existe para isso: ele tem que casar dos dois lados para o
    jogo funcionar, entao ninguem o desenha "mais ou menos". Exige pelo menos
    dois warps (um so admite qualquer deslocamento) e um unico candidato
    (ambiguidade nao e prova).
    """
    ns = nosso.get("warp_events") or []
    fs = {(w["x"], w["z"]) for w in fonte.get("warp_events", [])}
    if len(ns) < 2 or not fs:
        return None
    cands = {(fx - ns[0]["x"], fz - ns[0]["y"]) for fx, fz in fs}
    bons = [d for d in cands
            if all((w["x"] + d[0], w["y"] + d[1]) in fs for w in ns)]
    return bons[0] if len(bons) == 1 else None


# ------------------------------------------------------------------ geometria
#
# Tres coisas medidas em 18/08/2026, na onda de povoar mapa vazio de Sinnoh, e
# que sao a diferenca entre "NPC entrou" e "NPC entrou em lugar que existe":
#
# 1. PLANTA PROVISORIA. `AmitySquare`, `StarkMountainOutside`, `BattleFrontier`
#    e `IronIsland` nao tem mapa: tem o MOLDE DE PORTAO 13x9. Medido byte a
#    byte contra `data/layouts/Route226_Access/map.bin`: os quatro sao
#    identicos a ele em TODAS as linhas menos a linha 1, onde as portas sao
#    furadas (BattleFrontier difere em 4 tiles, IronIsland em 2, os dois so em
#    y=1). Por a fonte de um mapa de 48x47 dentro de 13x9 e plantar coordenada
#    que vai ter que ser refeita no dia em que o mapa real entrar. Recusado.
# 2. ANDAVEL NAO BASTA, TEM QUE SER ALCANCAVEL. A regra do motor conta
#    elevacao (`IsElevationMismatchAt`), e a lição da Route 222 e que um bolso
#    de 4 tiles parece estrada na colisao. A BFS de `conserta_route222.alcance`
#    e a mesma, semeada pelos NOSSOS warps: quem nasce fora do alcance deles e
#    NPC que ninguem encontra.
# 3. PLACA SEM TILE DE LEITURA e placa que o jogador nunca abre (o defeito das
#    tres da Route 222). Exige vizinho ortogonal ALCANCAVEL, nao so andavel.

_STENCIL = None

# Os dois moldes de portao 13x9 do repo. `LAYOUT_ROUTE226_ACCESS` vem primeiro
# por historia, mas quem manda e o que ainda mede 13x9 (ver `planta_provisoria`).
MOLDES = ("LAYOUT_ROUTE226_ACCESS", "LAYOUT_ROUTE208_ACCESS")


def grade(layouts, layout_id):
    """(largura, altura, matriz de palavras) do map.bin do layout."""
    L = layouts[layout_id]
    W, H = L["width"], L["height"]
    b = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
    return W, H, [[struct.unpack("<H", b[(y * W + x) * 2:(y * W + x) * 2 + 2])[0]
                   for x in range(W)] for y in range(H)]


def planta_provisoria(layouts, layout_id):
    """True quando o layout e o molde de portao 13x9, com portas trocadas.

    Medido em 21/08/2026: existem DOIS moldes no repo, `LAYOUT_ROUTE226_ACCESS`
    e `LAYOUT_ROUTE208_ACCESS`, e o segundo e byte a byte igual ao primeiro fora
    da linha das portas. Esta funcao ja pegava os dois pela comparacao de
    blockdata; quem enxergava so 12 vitimas era a LISTA ESCRITA A MAO da fila,
    que escondia o `OreburghGateB1F`. Nao ha conserto a fazer aqui, e o
    autoteste abaixo passou a fixar isso para ninguem "consertar" o que funciona.
    """
    global _STENCIL
    L = layouts[layout_id]
    if (L["width"], L["height"]) != (13, 9):
        return False
    if layout_id in MOLDES:
        return True
    if _STENCIL is None:
        # O MOLDE DE REFERENCIA NAO E FIXO, e isso e conserto de 22/08/2026 com
        # a medida junto: o commit `721c77fb63` ("os 111 mapas cortados saem da
        # ROM") encolheu `LAYOUT_ROUTE226_ACCESS` para 1x1, e desde entao esta
        # funcao lia 2 bytes como se fossem 234 e respondia False para TODO
        # mundo, calada. O portao inteiro estava morto e o `--demo` vermelho.
        # Agora o estencil e o primeiro molde que ainda MEDE 13x9.
        alvo = next((m for m in MOLDES if m in layouts
                     and (layouts[m]["width"], layouts[m]["height"]) == (13, 9)),
                    None)
        if alvo is None:
            return False
        _STENCIL = grade(layouts, alvo)[2]
    g = grade(layouts, layout_id)[2]
    return all(g[y] == _STENCIL[y] for y in range(L["height"]) if y != 1)


def alcancaveis(W, H, g, warps):
    """Tiles que o jogador alcanca entrando pelos warps do mapa.

    Warp costuma cair em tile de porta, que e bloqueado: nesse caso a semente e
    o vizinho andavel dele, que e onde o jogador pousa de verdade.
    """
    sementes = []
    for w in warps:
        x, y = w.get("x"), w.get("y")
        if not (isinstance(x, int) and isinstance(y, int)):
            continue
        if not (0 <= x < W and 0 <= y < H):
            continue
        if ((g[y][x] >> 10) & 3) == 0:
            sementes.append((x, y))
            continue
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and ((g[ny][nx] >> 10) & 3) == 0:
                sementes.append((nx, ny))
    return R222.alcance(W, H, g, sementes) if sementes else set()


def conversor_de_coordenada(fonte, larg, alt, header, matriz, nosso=None,
                            vazio=False):
    """(x do Platinum, z do Platinum) -> (x, y) nosso, para UM mapa.

    Extraida de `main()` em 11/08/2026 e nao reescrita: `itens_escondidos_sinnoh`
    precisa da MESMA conta para reencontrar, pela coordenada, qual evento da
    fonte virou qual `bg_event` nosso. Duas copias da formula divergiriam calado
    no dia em que uma fosse ajustada, e o preco seria item escondido posto no
    lugar errado, exatamente o que a ferramenta existe para evitar.

    `nosso` e o map.json daqui, e serve so ao caminho de translacao dos mapas de
    `REDESENHO_1PARA1`; sem ele a funcao se comporta como sempre.

    `vazio=True` diz que este mapa NAO TEM NENHUM evento importado ainda, e so
    entao a translacao provada por warp vale sem estar na lista autorizada. A
    lista existe por um motivo que nao se aplica a mapa vazio: mudar a regra de
    quem JA tem placa gravada orfana a placa (ver o comentario de
    `REDESENHO_1PARA1`). Onde nao ha nada gravado nao ha nada para orfanar, e
    entao a prova dos warps e a melhor regua disponivel, sempre melhor que a
    escala. Quem chama sem `vazio` continua recebendo o comportamento de antes,
    byte a byte: `itens_escondidos_sinnoh`, `texto_sinnoh`, `maquina_sinnoh` e
    `fila_b6` reencontram evento ja gravado e nao podem mudar de conta.

    A regra escolhida fica em `conv.regra`, para o censo dizer por que cada
    coordenada e a que e.
    """
    def marca(f, regra):
        f.regra = regra
        return f

    d = deslocamento_de_warp(fonte, nosso) if nosso is not None else None
    if header in REDESENHO_1PARA1 and nosso is not None:
        if d is None:
            raise SystemExit(
                f"{header} esta em REDESENHO_1PARA1 mas os warps nao provam "
                "um deslocamento unico. Ou o mapa mudou, ou a lista mentiu: "
                "meca de novo antes de importar nada.")
    elif not (vazio and d is not None):
        d = None
    if d is not None:
        dx, dz = d

        def conv_translacao(e):
            return (min(max(e["x"] - dx, 0), larg - 1),
                    min(max(e["z"] - dz, 0), alt - 1))
        return marca(conv_translacao,
                     f"translacao provada por {len(nosso.get('warp_events') or [])} "
                     f"warps, d=({dx},{dz})")
    todos = fonte.get("object_events", []) + fonte.get("bg_events", [])
    if not todos:
        return None
    xs = [e["x"] for e in todos]
    zs = [e["z"] for e in todos]
    if min(xs) >= 0 and min(zs) >= 0 and max(xs) < larg and max(zs) < alt:
        return marca(lambda e: (e["x"], e["z"]),
                     "identidade (coordenada da fonte ja local e dentro do layout)")
    cx = caixa_da_matriz(matriz, header) if matriz else None
    if not cx:
        # sem matriz: usa a própria nuvem de eventos como caixa
        cx = (min(xs), min(zs), max(1, max(xs) - min(xs) + 1),
              max(1, max(zs) - min(zs) + 1))
    ox, oz, cw, ch = cx

    def conv(e):
        x = int((e["x"] - ox) * (larg - 1) / max(1, cw - 1))
        y = int((e["z"] - oz) * (alt - 1) / max(1, ch - 1))
        return min(max(x, 0), larg - 1), min(max(y, 0), alt - 1)
    return marca(conv, f"escala da caixa {cw}x{ch} da matriz sobre {larg}x{alt}")


def main():
    sprites = V.sprites_utilizaveis()
    V.confere_tabela_de_trocas(sprites)
    movimentos = V.constantes("include/constants/event_object_movement.h", "MOVEMENT_TYPE_")
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}

    heads = headers_do_platinum()
    por_chave = {}
    for h, (ev, mx) in heads.items():
        por_chave.setdefault(chave(h), (h, ev, mx))

    tocado = set()   # map.json que mudou só por conserto de sprite de espécie
    nossos = mapas_editaveis_sinnoh()
    casados, sem_par = [], []
    for m in nossos:
        h = APELIDOS.get(m)
        alvo = (h,) + heads[h] if h in heads else por_chave.get(chave(m))
        (casados.append((m,) + alvo) if alvo else sem_par.append(m))

    print(f"mapas de Sinnoh nossos: {len(nossos)}  casados: {len(casados)}  "
          f"sem par no Platinum: {len(sem_par)}")
    if "--sem-par" in sys.argv:
        for m in sem_par:
            print("   ", m)

    stats = {"objetos": 0, "placas": 0, "fora_hidden": 0, "fora_mobilia": 0,
             "fora_coord": 0, "fora_sem_espaco": 0, "fora_nome_proprio": 0,
             "trocas": 0, "mapas": 0, "ja_importado": 0,
             "fora_planta_provisoria": 0, "fora_inalcancavel": 0,
             "fora_placa_ilegivel": 0, "fora_teto_64": 0, "empurrados": 0,
             "fora_escala_nao_provada": 0, "fora_teto_fonte": 0}
    censo = [("mapa", "tipo", "x_fonte", "z_fonte", "x_nosso", "y_nosso",
              "gfx", "trainer_type", "regra", "motivo")]

    def linha(m, tipo, e, pos, gfx, regra, motivo):
        censo.append((m, tipo, e.get("x", ""), e.get("z", ""),
                      pos[0] if pos else "", pos[1] if pos else "", gfx,
                      e.get("trainer_type", ""), regra, motivo))

    # O censo tem que SOBREVIVER a idempotencia: rodar de novo pula o mapa que
    # ja foi escrito, e sem isto a segunda rodada apagaria justamente a linha
    # que diz onde cada objeto entrou. Linha de mapa ja importado e reaproveitada
    # do censo anterior.
    antigo = {}
    if os.path.exists(CENSO):
        for l in open(CENSO, encoding="utf-8"):
            c = tuple(l.rstrip("\n").split("\t"))
            if len(c) == len(censo[0]) and c[0] != "mapa":
                antigo.setdefault(c[0], []).append(c)

    # CORTES DO GUI: mapa cujo campo saiu do porte nao recebe evento novo. Nao e
    # regua (a regua ja o desconta) e sim ROM: povoar as 18 salas de pilar da
    # Turnback Cave custaria bytes num mapa que outro executor esta REMOVENDO da
    # ROM. A lista e a MESMA que mede, `completude.CORTES_DO_GUI`.
    import completude as _CP
    _rx, _defi = _CP.cortes_da_regiao("Sinnoh")

    trocados, deixados = {}, {}
    for meu, header, arq_ev, matriz in casados:
        cortado = _defi.get(meu) or ()
        pe = os.path.join(PLAT, "res/field/events", arq_ev + ".json")
        if not os.path.exists(pe):
            continue
        fonte = json.load(open(pe))
        pm = os.path.join(REPO, "data/maps", meu, "map.json")
        d = json.load(open(pm))
        L = layouts[d["layout"]]
        larg, alt = L["width"], L["height"]

        existentes = (d.get("object_events") or []) + (d.get("bg_events") or [])
        # IDEMPOTENCIA POR EVENTO, e nao por mapa (22/08/2026, decisao do Gui
        # "completa ate ficar 100 em tudo").
        #
        # Ate aqui, mapa com UM evento da marca era pulado INTEIRO na rodada
        # seguinte. Medido no dia: 306 dos 474 mapas casados caiam nesse ramo, e
        # com eles ia embora quase todo o deficit de Sinnoh (499 objetos e 91
        # placas contra a fonte). Idempotencia de MAPA mede a rodada; o que
        # interessa medir e o EVENTO.
        #
        # Duas guardas no lugar do pulo, e as duas sao de contagem, nao de fe:
        #
        # 1. RECLAMACAO POR COORDENADA. Evento da fonte cuja coordenada
        #    convertida ja tem um objeto NOSSO com a marca (dele ou de um
        #    vizinho a 1 tile, que e o empurrao que o proprio gerador da) e
        #    considerado JA IMPORTADO e nao entra de novo. Cada objeto so pode
        #    ser reclamado uma vez, senao dois eventos vizinhos casariam com o
        #    mesmo e o segundo viraria duplicata.
        # 2. TETO DA FONTE. Nenhum mapa pode terminar com mais objeto (ou mais
        #    placa) do que a FONTE tem. E a mesma régua do `completude.py`, e ela
        #    fecha a porta para qualquer duplicata que a guarda 1 deixe passar:
        #    no pior caso o mapa para em 100%, nunca em 130%.
        ja_import = [e for e in existentes
                     if e.get("origem") == "pokeplatinum"]
        if ja_import:
            stats["ja_importado"] += 1
        reclamados = set()

        def reclama(x, y, lista, gfx=None):
            """True se ja existe evento NOSSO em (x,y) ou ao lado que E este.

            A primeira versao so olhava objeto com a MARCA `pokeplatinum`, e isso
            criou 30 clones em 12 mapas na propria rodada de 22/08/2026: os
            treinadores de rota entraram no repo por OUTRA ferramenta
            (`treinadores_rota_sinnoh.py`), sem marca nenhuma e um tile acima da
            coordenada da fonte, entao o importador nao os reconheceu e plantou
            uma copia de cada um logo abaixo. Em `Route222` foram DEZ, e tres
            delas caem em cima da estrada: o T107.1 congelou em (89,19).
            Quem reclama agora e QUALQUER objeto nosso a <= 1 tile com o MESMO
            `graphics_id`, marcado ou nao. Fora de par de gfx, a marca continua
            valendo sozinha, que e o caso de placa e de objeto sem sprite igual.
            """
            for e in lista:
                if id(e) in reclamados:
                    continue
                if abs(e.get("x", -99) - x) > 1 or abs(e.get("y", -99) - y) > 1:
                    continue
                if e.get("origem") == "pokeplatinum" or (
                        gfx is not None and e.get("graphics_id") == gfx):
                    reclamados.add(id(e))
                    reclama.ultimo = e
                    return True
            reclama.ultimo = None
            return False

        # TETO DA FONTE, medido COMO A REGUA MEDE (corrigido em 22/08/2026).
        #
        # Ate aqui o teto contava `len(fonte["object_events"])` cru, e a fonte
        # guarda PLACA como object_event (SIGNBOARD, ARROW_SIGNPOST, ...).
        # `completude.le_plat` tira essas placas do denominador de `objetos` e as
        # soma em `placas`, entao o teto era mais FROUXO que a regua: em
        # JubilifeCity a fonte tem 22 objetos para a regua e 27 registros crus, e
        # os cinco de diferenca eram cinco NPC a mais do que o Platinum tem. O
        # teto agora desconta a placa, e o portao volta a dizer a verdade que o
        # cabecalho dele promete: nenhum mapa termina com mais objeto do que o
        # Platinum tem.
        objs_fonte = [o for o in (fonte.get("object_events") or [])
                      if not any(t in o.get("graphics_id", "")
                                 for t in GRAFICOS_PLACA)]
        teto_fonte = (0 if "object_events" in cortado else
                      len(objs_fonte) - len(d.get("object_events") or []))
        teto_bg = (0 if "bg_events" in cortado else
                   len(fonte.get("bg_events") or [])
                   - len(d.get("bg_events") or []))

        # Portao 1: geometria de verdade. NPC em planta emprestada e coordenada
        # que vai ter que ser refeita.
        if planta_provisoria(layouts, d["layout"]):
            stats["fora_planta_provisoria"] += 1
            for e in fonte.get("object_events", []):
                linha(meu, "objeto", e, None, e.get("graphics_id", ""), "-",
                      f"planta provisoria: {d['layout']} e o molde de portao 13x9")
            for e in fonte.get("bg_events", []):
                linha(meu, "placa", e, None, "-", "-",
                      f"planta provisoria: {d['layout']} e o molde de portao 13x9")
            continue

        conv = conversor_de_coordenada(fonte, larg, alt, header, matriz, d,
                                       vazio=not existentes)
        if conv is None:
            continue
        regra = getattr(conv, "regra", "?")
        # Portao 1.5, REABERTO em 22/08/2026 com a decisao do Gui "completa ate
        # ficar 100 em tudo", e a reabertura vem com a medida do porque.
        #
        # A escala foi fechada em 18/08 porque a correcao da Route 222 provou
        # que ela punha placa DENTRO DE PAREDE, sem nenhum vizinho andavel: o
        # jogador nunca leria. O defeito era real, mas o conserto foi grosso, e
        # o preco esta medido: com o portao fechado, 1.328 eventos da fonte em
        # mapa de ESCOPO ficavam de fora, quase todo o deficit de objetos de
        # Sinnoh, e mapas inteiros de rua (Route 207 a 215, Route 224,
        # EternaCity, SolaceonTown) paravam de crescer.
        #
        # O que MUDOU desde 18/08 nao e a confianca na escala, e o portao
        # DEPOIS dela. Hoje todo evento colocado passa por tres provas que na
        # epoca da Route 222 nao existiam, e sao exatamente as que pegam o
        # defeito daquele dia:
        #   - objeto tem que cair em tile ALCANCAVEL a pe pelos warps (`pisa`),
        #     com empurrao de no maximo 1 tile, senao e recusado;
        #   - placa tem que ter tile de LEITURA andavel (`leitura_de_placa`),
        #     que e literalmente a regua da Route 222;
        #   - e nada pode passar do que a FONTE tem (`teto_fonte`).
        # Ou seja: a escala escolhe a REGIAO do mapa, e o portao decide se
        # aquele tile serve. Coordenada aproximada com prova de tile e forma
        # honesta; coordenada aproximada sem prova era o defeito.
        #
        # A regra continua escrita no censo, evento a evento, para que a
        # diferenca entre "identidade" e "escala" nunca vire invisivel.
        if regra.startswith("escala"):
            regra += " + portao de alcance (22/08/2026)"
        W, H, g = grade(layouts, d["layout"])
        pisa = alcancaveis(W, H, g, d.get("warp_events") or [])
        # Mapa sem warp semeavel (a Liga entra por script) nao tem como provar
        # alcance: cai para "andavel", que e a regua antiga, e o censo diz.
        if not pisa:
            pisa = {(x, y) for y in range(H) for x in range(W)
                    if ((g[y][x] >> 10) & 3) == 0}
            regra += " | alcance nao semeavel (sem warp), so andavel"
        teto = 64 - len(d.get("object_events") or [])
        ja = {(o.get("x"), o.get("y")) for o in (d.get("object_events") or [])}
        ja |= {(o.get("x"), o.get("y")) for o in (d.get("bg_events") or [])}
        # CORPO NAO NASCE EM CIMA DE WARP NEM COLADO EM GATILHO, 23/08/2026.
        #
        # A regra de placa sobre warp (logo abaixo) e legitima e foi medida: o
        # jogo original faz isso. OBJETO sobre warp e outra coisa, e custou dois
        # casos: no ValleyWindworksBuilding um grunt novo nasceu em (4,8), que e
        # o warp 1 do mapa, e no OreburghGate_1F uma pedra empurrada caiu em
        # (8,22), o unico tile por onde se chega ao `coord_event` de (7,22) que
        # entrega o HM de Rock Smash. O T101.6 e o T100.10 reprovaram sem que o
        # mapa tivesse ficado desconexo: o que quebrou foi a CENA. Gatilho e
        # tile de roteiro, entao corpo novo fica a pelo menos um tile dele.
        ja |= {(w.get("x"), w.get("y")) for w in (d.get("warp_events") or [])}
        ja |= corredor_de_gatilho(d, layouts)
        # ponytail: NÃO tratar tile de warp como ocupado. Parecia defeito ter
        # placa em cima de porta, e 4 chegaram a ser removidas em 05/08/2026.
        # Medido depois, contra o jogo original: nós temos 30 de 2376 placas
        # sobre warp (1,26%), o pokeemerald vanilla tem 19 de 720 (2,64%) e o
        # pokefirered 5 de 702 (0,71%). O vanilla tem o DOBRO da nossa taxa:
        # é padrão do jogo, não defeito, e filtrar tiraria placa boa.
        novos_obj, novas_placas = [], []

        for e in fonte.get("object_events", []):
            g = e.get("graphics_id", "")
            # ponytail: comparar contra o nome INTEIRO fazia "VENT" casar com
            # "OBJ_EVENT_GFX_ACE_TRAINER_F" (e-VENT-o) e jogar 806 NPC fora em
            # silêncio. Substring só vale depois de tirar o prefixo comum.
            classe = g.replace("OBJ_EVENT_GFX_", "")
            # Espécie ANTES de tudo: o nome dela cai dentro de NOMES_PROPRIOS
            # (Magikarp, Starly, Buneary) e dentro de GRAFICOS_PROIBIDOS se
            # alguma família nova de sprite repetir uma palavra da lista. Ver a
            # emenda de 22/08/2026 no topo.
            especie = classe if classe in especies() else None
            proprio = None if especie else sprite_proprio(sprites).get(classe)
            # Tem sprite proprio agora: sai do balde (a) e segue o fluxo normal
            # (hidden_flag, teto, alcancabilidade) como qualquer NPC. O filtro
            # NOMES_PROPRIOS e por SUBSTRING, entao renomear nao bastava:
            # "SINNOH_CYNTHIA" continua contendo "CYNTHIA". Por isso a chave.
            tem_sprite = not especie and g in DE_PARA_SINNOH
            if tem_sprite:
                g = DE_PARA_SINNOH[g]
                classe = g.replace("OBJ_EVENT_GFX_", "")
            # Ordem importa para o relatório: mobiliário sai como mobiliário, e
            # só depois o que sobrou é medido pela hidden_flag.
            if not especie and any(t in classe for t in GRAFICOS_PROIBIDOS):
                stats["fora_mobilia"] += 1
                linha(meu, "objeto", e, None, g, regra,
                      "mobiliario/item, decisao 4: nunca vira NPC")
                continue
            if not especie and not tem_sprite and any(
                    t in classe for t in NOMES_PROPRIOS):
                stats["fora_nome_proprio"] += 1
                deixados[g] = deixados.get(g, 0) + 1
                linha(meu, "objeto", e, None, g, regra,
                      "nome proprio sem sprite aqui")
                continue
            nossa_flag = "0"
            hf = str(e.get("hidden_flag", "0"))
            if hf not in ("0", "0x0"):
                if cena_nossa(hf) and hf not in GRUPOS_COM_CENA:
                    stats["fora_cena_nossa"] = stats.get("fora_cena_nossa", 0) + 1
                    linha(meu, "objeto", e, None, g, regra,
                          f"grupo com dono: {cena_nossa(hf)} ja tem cena nossa "
                          "que revela este elenco, e segundo corpo duplicaria")
                    continue
                if hf in GRUPOS_COM_CENA:
                    nossa_flag = GRUPOS_COM_CENA[hf]
                    stats["grupo_com_cena"] = stats.get("grupo_com_cena", 0) + 1
                elif hf in GRUPOS_SEM_ENREDO:
                    stats["grupo_rodizio"] = stats.get("grupo_rodizio", 0) + 1
                elif flag_morta(hf):
                    stats["flag_morta"] = stats.get("flag_morta", 0) + 1
                else:
                    stats["fora_hidden"] += 1
                    linha(meu, "objeto", e, None, g, regra,
                          f"hidden_flag {e.get('hidden_flag')}, decisao 2")
                    continue
            if any(t in classe for t in GRAFICOS_PLACA):
                x, y = conv(e)
                if reclama(x, y, d.get("bg_events") or []):
                    linha(meu, "placa", e, (x, y), g, regra,
                          "ja importado em rodada anterior (placa nossa com a "
                          "marca nesta coordenada)")
                    continue
                if len(novas_placas) >= max(0, teto_bg):
                    # A placa da fonte que e OBJETO (SIGNBOARD) vira `bg_event`
                    # nosso, e a regua compara bg com bg: sem este teto o mapa
                    # sai com mais placa do que o Platinum tem e a coluna passa
                    # de 100 por construcao, nao por conteudo.
                    stats["fora_teto_fonte"] += 1
                    linha(meu, "placa", e, (x, y), g, regra,
                          f"teto da fonte: este mapa ja tem tanta placa quanto "
                          f"o Platinum ({len(fonte.get('bg_events') or [])})")
                    continue
                if (x, y) in ja:
                    linha(meu, "placa", e, (x, y), g, regra, "tile ja ocupado")
                elif not leitura_de_placa(layouts, d["layout"], x, y):
                    stats["fora_placa_ilegivel"] += 1
                    linha(meu, "placa", e, (x, y), g, regra,
                          "sem tile de leitura andavel: o jogador nunca leria")
                else:
                    ja.add((x, y))
                    novas_placas.append(placa(x, y))
                    linha(meu, "placa", e, (x, y), g, regra, so_com_hm(pisa, x, y))
                continue
            # NOME PROPRIO NAO GANHA GEMEO, 23/08/2026. Quando a fonte traz um
            # personagem de nome proprio e a NOSSA rodada de historia ja escreveu
            # ele a mao com script (a Candice do ginasio de Snowpoint e o caso:
            # `SnowpointCity_Gym_EventScript_Leader` em (11,2), com sprite
            # generico WOMAN_5), o `reclama` nao o reconhecia, porque compara
            # graphics_id, e plantava uma SEGUNDA Candice muda ao lado. O certo
            # e o contrario: quem manda e o objeto com SCRIPT, e o que ele ganha
            # do sprite novo e a CARA.
            if proprio:
                gemeo = next((o for o in (d.get("object_events") or [])
                              if id(o) not in reclamados
                              and str(o.get("script", "0")) not in ("0", "")
                              and max(abs(o.get("x", -99) - conv(e)[0]),
                                      abs(o.get("y", -99) - conv(e)[1])) <= 1),
                             None)
                if gemeo is not None:
                    reclamados.add(id(gemeo))
                    pode, porque = pode_vestir(gemeo, proprio)
                    if not pode:
                        stats["sprite_recusado"] = stats.get("sprite_recusado", 0) + 1
                        linha(meu, "objeto", e, conv(e), g, regra,
                              "ja existe a mao com script, e " + porque)
                        continue
                    if gemeo.get("graphics_id") != proprio:
                        gemeo["graphics_id"] = proprio
                        stats["sprite_corrigido"] = stats.get("sprite_corrigido", 0) + 1
                        tocado.add(pm)
                    linha(meu, "objeto", e, conv(e), g, regra,
                          f"ja existe a mao com script: so o sprite virou {proprio}")
                    continue
            if reclama(*conv(e), d.get("object_events") or [], g):
                # CONSERTO DE SPRITE, 22/08/2026: quem entrou em rodada anterior
                # como espécie caiu em OBJ_EVENT_GFX_MAN_1, porque naquela data
                # não havia sprite de overworld de Pokémon nesta ROM. Agora há, e
                # deixar o Pikachu com cara de homem é o mapa mentindo, que é
                # exatamente o que a decisão do Gui de 05/08 proíbe. Só o
                # graphics_id muda; posição, flag e script ficam como estão.
                velho = getattr(reclama, "ultimo", None)
                novo_g = (f"OBJ_EVENT_GFX_SPECIES({especie})" if especie
                          else proprio)
                # MESMO PORTAO do gemeo, e por isso ele e uma funcao. Este
                # caminho tambem repinta objeto NOSSO, e casa por coordenada e
                # marca, nao por identidade: sem o portao ele repoe o defeito
                # que o de cima passou a recusar.
                recusa_sprite = None
                if velho is not None and proprio and not especie:
                    pode, recusa_sprite = pode_vestir(velho, proprio)
                    if not pode:
                        stats["sprite_recusado"] = stats.get("sprite_recusado", 0) + 1
                        novo_g = None
                if velho is not None and novo_g and velho.get("graphics_id") != novo_g:
                    velho["graphics_id"] = novo_g
                    stats["sprite_corrigido"] = stats.get("sprite_corrigido", 0) + 1
                    tocado.add(pm)
                linha(meu, "objeto", e, conv(e), g, regra,
                      "ja importado em rodada anterior (objeto nosso com a "
                      "marca nesta coordenada)"
                      + (", e " + recusa_sprite if recusa_sprite else ""))
                continue
            if len(novos_obj) >= max(0, teto_fonte):
                stats["fora_teto_fonte"] += 1
                linha(meu, "objeto", e, None, g, regra,
                      f"teto da fonte: este mapa ja tem tanto objeto quanto o "
                      f"Platinum ({len(fonte.get('object_events') or [])})")
                continue
            if len(novos_obj) >= teto:
                stats["fora_teto_64"] += 1
                linha(meu, "objeto", e, None, g, regra,
                      "teto de 64 templates por mapa, cortado por ordem da fonte")
                continue
            gfx_fonte = g
            if especie:
                g = f"OBJ_EVENT_GFX_SPECIES({especie})"
            elif proprio:
                g = proprio
            elif g not in sprites:
                novo = V.TROCA_SPRITE.get(g)
                if not novo:
                    trocados[g] = trocados.get(g, 0) + 1
                    novo = V.SPRITE_PADRAO
                stats["trocas"] += 1
                g = novo
            mov = e.get("movement_type", V.MOVIMENTO_PADRAO)
            if mov not in movimentos:
                mov = V.MOVIMENTO_PADRAO
            x, y = conv(e)
            # Portao 2: tem que cair em tile ALCANCAVEL. Empurrao de 1 tile e
            # correcao de arredondamento; empurrao de 8 (o `livre` antigo) e
            # invencao de posicao, e nao entra em mapa que nasce agora.
            # Portao 2: tem que cair em tile ALCANCAVEL, com empurrao de no
            # maximo RAIO tiles.
            #
            # RAIO subiu de 1 para 3 em 22/08/2026, a pedido do Gui ("reposicione
            # a <= 3 tiles o resto"), e o numero nao e novo: e o MESMO empurrao
            # que `bolas_sinnoh.py` usa desde 22/08 para as bolas de item, no
            # mesmo mapa e com a mesma grade. Com 1 tile, 55 objetos da fonte em
            # mapa de escopo caiam fora so por arredondamento da escala. O que
            # segura a honestidade nao e o raio, e a PROVA: o tile de destino
            # tem que estar em `pisa` (alcancavel a pe pelos warps) e livre, e o
            # censo escreve quantas casas cada um andou.
            RAIO = 3
            pos = next(((x + dx, y + dy) for r in range(RAIO + 1)
                        for dx in range(-r, r + 1) for dy in range(-r, r + 1)
                        if max(abs(dx), abs(dy)) == r
                        and (x + dx, y + dy) in pisa
                        and (x + dx, y + dy) not in ja), None)
            if pos is None:
                stats["fora_inalcancavel"] += 1
                linha(meu, "objeto", e, (x, y), gfx_fonte, regra,
                      f"coordenada nao cai em tile alcancavel "
                      f"(nem {RAIO} tiles ao lado)")
                continue
            passos = max(abs(pos[0] - x), abs(pos[1] - y))
            if passos:
                stats["empurrados"] += 1
            linha(meu, "objeto", e, pos, gfx_fonte, regra,
                  "" if not passos else f"empurrado {passos} tile(s), gfx {g}"
                  if g != gfx_fonte else f"empurrado {passos} tile(s)")
            ja.add(pos)
            novos_obj.append({
                "graphics_id": g, "x": pos[0], "y": pos[1], "elevation": 3,
                "movement_type": mov,
                "movement_range_x": e.get("movement_range_x", 0),
                "movement_range_y": e.get("movement_range_z", 0),
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": "0", "flag": nossa_flag, **MARCA,
            })

        for e in fonte.get("bg_events", []):
            x, y = conv(e)
            if reclama(x, y, d.get("bg_events") or []):
                linha(meu, "placa", e, (x, y), "-", regra,
                      "ja importado em rodada anterior (placa nossa com a "
                      "marca nesta coordenada)")
                continue
            if len(novas_placas) >= max(0, teto_bg):
                stats["fora_teto_fonte"] += 1
                linha(meu, "placa", e, (x, y), "-", regra,
                      f"teto da fonte: este mapa ja tem tanta placa quanto o "
                      f"Platinum ({len(fonte.get('bg_events') or [])})")
                continue
            if (x, y) in ja:
                linha(meu, "placa", e, (x, y), "-", regra, "tile ja ocupado")
                continue
            if not leitura_de_placa(layouts, d["layout"], x, y):
                stats["fora_placa_ilegivel"] += 1
                linha(meu, "placa", e, (x, y), "-", regra,
                      "sem tile de leitura andavel: o jogador nunca leria")
                continue
            ja.add((x, y))
            novas_placas.append(placa(x, y))
            linha(meu, "placa", e, (x, y), "-", regra, so_com_hm(pisa, x, y))

        # PORTÃO 5, novo em 22/08/2026: corpo novo não pode TRANCAR o mapa.
        #
        # Os portões 1 a 4 provam que o tile é alcançável; nenhum deles provava
        # que o mapa CONTINUA alcançável depois de o corpo ocupar o tile. Num
        # corredor de uma casa só isso tranca o jogador, e é o mesmo medo que
        # `pedras_sinnoh.py` já cobra por busca em largura desde 18/08. A régua
        # é a mesma daquele: tratando todo objeto novo como bloqueio, todo pouso
        # de warp do mapa continua alcançável a partir do primeiro. Quem
        # desconectar sai, um por vez e na ordem inversa da fonte, para nunca
        # jogar fora os bons por causa de um mau.
        #
        # ARMADILHA: `g` foi RECICLADO como graphics_id dentro do laço acima e
        # não é mais a grade. A grade se relê, nunca se supõe.
        if novos_obj:
            novos_obj = sem_tranca(layouts, d, novos_obj, stats, linha, meu)
        stats["fora_coord"] += len(fonte.get("coord_events", []))
        if not (novos_obj or novas_placas or pm in tocado):
            continue
        stats["objetos"] += len(novos_obj)
        stats["placas"] += len(novas_placas)
        stats["mapas"] += 1
        # Objeto novo SEMPRE no fim: a save guarda índice de objeto.
        d["object_events"] = (d.get("object_events") or []) + novos_obj
        d["bg_events"] = (d.get("bg_events") or []) + novas_placas
        if APLICAR:
            json.dump(d, open(pm, "w"), indent=2, ensure_ascii=False)

    with open(CENSO, "w", encoding="utf-8") as f:
        for l in censo:
            f.write("\t".join(str(c) for c in l) + "\n")
    print(f"\ncenso: {len(censo) - 1} linhas em {os.path.relpath(CENSO, REPO)}")
    print("\nresumo:", stats)
    if trocados:
        print("\nsprites sem troca conhecida (viraram", V.SPRITE_PADRAO + "):")
        for g, n in sorted(trocados.items(), key=lambda kv: -kv[1]):
            print(f"  {n:5}  {g}")
    if deixados:
        print("\nNPC deixado de fora por ser nome próprio sem sprite:")
        for g, n in sorted(deixados.items(), key=lambda kv: -kv[1]):
            print(f"  {n:5}  {g}")
    print("\naplicado" if APLICAR else "\nnada escrito (use --aplicar)")
    return 0


def corredor_de_gatilho(d, layouts, alcance=8):
    """Tiles de APROXIMACAO do que o jogador PRECISA alcancar, livres de corpo
    novo: os `coord_event` e o tile de conversa de todo objeto COM SCRIPT.

    Gatilho de coordenada e o unico evento do jogo que o jogador dispara ANDANDO,
    e todo roteiro de teste chega nele por perna reta e saturante. Corpo novo em
    qualquer tile daquela reta nao desconecta nada (os portoes de conectividade
    passam limpos) e mesmo assim mata a cena, porque o jogador para antes. Foi o
    que reprovou o T100.10 (pedra em (8,22), unico tile de aproximacao do
    gatilho de (7,22) do OreburghGate_1F) e o T101.6 (grunt em (5,2) na linha do
    gatilho de (7,2) do ValleyWindworksBuilding), os dois com o mapa conexo.

    A reserva e o proprio tile, os oito vizinhos e a RETA andavel nas quatro
    direcoes ate `alcance` tiles ou ate a primeira parede. Nao e o mapa inteiro:
    e o corredor por onde se chega, que e o que roteiro usa.
    """
    gat = d.get("coord_events") or []
    # TILE DE CONVERSA, acrescentado em 23/08/2026 depois do segundo caso da
    # mesma familia: NPC com script existe para ser falado, e corpo novo
    # encostado nele rouba o unico tile de onde se fala. Custou o T115.3, o
    # T125.11 e o T125.12: um NPC importado nasceu em (11,3) do ginasio de
    # Snowpoint, colado na lider, e as tres provas que sobem a coluna 11 para
    # falar com a Candice pararam um tile antes. O `coord_event` ja estava
    # protegido; faltava o objeto.
    fala = [o for o in (d.get("object_events") or [])
            if str(o.get("script", "0")) not in ("0", "")]
    if not (gat or fala):
        return set()
    W, H, g = grade(layouts, d["layout"])
    fora = {(o["x"] + dx, o["y"] + dy) for o in fala
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
    for c in gat:
        cx, cy = c.get("x", -99), c.get("y", -99)
        if not (0 <= cx < W and 0 <= cy < H):
            continue
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                fora.add((cx + dx, cy + dy))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = cx, cy
            for _ in range(alcance):
                x, y = x + dx, y + dy
                if not (0 <= x < W and 0 <= y < H) or ((g[y][x] >> 10) & 3):
                    break
                fora.add((x, y))
    return fora


def sem_tranca(layouts, d, novos, stats, linha, meu):
    """Tira do lote o objeto novo que desconecta o mapa.

    Régua igual à de `pedras_sinnoh.py`: com TODO objeto (os que já estavam e os
    novos) tratado como bloqueio, todo pouso de warp continua alcançável a
    partir do primeiro. Quem quebrar isso sai, um por vez e de trás para a
    frente, e vira linha de censo com o motivo em vez de sumir calado.
    """
    W, H, gr = grade(layouts, d["layout"])
    warps = d.get("warp_events") or []
    alvos = sorted({(w.get("x"), w.get("y")) for w in warps
                    if isinstance(w.get("x"), int) and isinstance(w.get("y"), int)
                    and 0 <= w["x"] < W and 0 <= w["y"] < H})
    if len(alvos) < 2:
        return novos                      # sem dois warps não há o que desconectar
    fixos = {(o.get("x"), o.get("y")) for o in (d.get("object_events") or [])}

    def passa(lote):
        bloq = fixos | {(o["x"], o["y"]) for o in lote}
        g2 = [[(v | (1 << 10)) if (x, y) in bloq else v
               for x, v in enumerate(linhaG)] for y, linhaG in enumerate(gr)]
        # SEMENTE NO PRIMEIRO WARP, e nao em todos. `alcancaveis` semeia cada
        # warp que recebe, entao semear a lista inteira punha TODO pouso dentro
        # de `viz` por construcao e este portao passava sempre: era um portao
        # decorativo. Medido em 23/08/2026 pelo T124.2, que reprovou porque um
        # corpo novo em (21,10) do IronIsland selou o warp de (21,9), o unico
        # caminho de volta ao 1F, e este `passa` deixou entrar. Semeando so o
        # primeiro warp, o teste vira o que o docstring sempre prometeu:
        # "todo pouso de warp continua alcancavel A PARTIR DO PRIMEIRO".
        viz = alcancaveis(W, H, g2, warps[:1])
        return all(any((x + dx, y + dy) in viz or (x, y) in viz
                       for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)))
                   for x, y in alvos)

    if passa(novos):
        return novos
    lote = list(novos)
    for o in reversed(list(novos)):
        lote.remove(o)
        stats["fora_tranca"] = stats.get("fora_tranca", 0) + 1
        linha(meu, "objeto", {"x": o["x"], "z": o["y"]}, (o["x"], o["y"]),
              o["graphics_id"], "-",
              "TRANCA: com este corpo um warp do mapa deixa de ser alcancavel")
        if passa(lote):
            break
    return lote


def so_com_hm(pisa, x, y):
    """Aviso, nao recusa: a placa e legivel, mas o tile de leitura nao sai dos
    warps deste mapa a pe. Em Mt Coronet isso quase sempre quer dizer Surf,
    Strength ou Rock Climb, que a BFS nao modela e a fonte tambem exige.
    """
    perto = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
    return "" if any(p in pisa for p in perto) else \
        "legivel, mas o tile de leitura nao sai dos warps a pe (Surf/Strength?)"


def placa(x, y):
    return {"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
            "script": SCRIPT_PLACA, **MARCA}


def livre(layouts, layout_id, x, y, ocupados, raio=8):
    """Tile andável e desocupado mais perto de (x,y). None se não houver."""
    for r in range(0, raio + 1):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if r and max(abs(dx), abs(dy)) != r:
                    continue
                p = (x + dx, y + dy)
                if p in ocupados:
                    continue
                if V.colisao(layouts, layout_id, *p) == 0:
                    return p
    return None


def leitura_de_placa(layouts, layout_id, x, y):
    """Direções de onde essa placa PODE ser lida: vizinho ortogonal andável.

    `BG_EVENT_PLAYER_FACING_ANY` lê de qualquer lado, então basta UM vizinho
    andável. Placa sem nenhum é placa que o jogador nunca abre, e foi o defeito
    de (54,16) e (65,16) na Route 222.
    """
    fora = []
    L = layouts[layout_id]
    for d, (dx, dy) in (("N", (0, -1)), ("S", (0, 1)),
                        ("W", (-1, 0)), ("E", (1, 0))):
        nx, ny = x + dx, y + dy
        if 0 <= nx < L["width"] and 0 <= ny < L["height"] \
                and V.colisao(layouts, layout_id, nx, ny) == 0:
            fora.append(d)
    return fora


def demo():
    """As regras que a primeira versão errou, e a que custou três placas."""
    # 1. andar escrito de dois jeitos é o mesmo andar
    assert chave("JubilifeCity_PokemonCenter_1F") == chave("MAP_HEADER_JUBILIFE_CITY_POKECENTER_1F")
    # 2. mapas diferentes continuam diferentes
    assert chave("Route205_North") != chave("MAP_HEADER_ROUTE_205_SOUTH")

    # 3. `deslocamento_de_warp` só responde com PROVA.
    f = {"warp_events": [{"x": 800, "z": 700}, {"x": 810, "z": 705}]}
    assert deslocamento_de_warp(
        f, {"warp_events": [{"x": 64, "y": 10}, {"x": 74, "y": 15}]}) == (736, 690)
    # um warp só admite qualquer deslocamento: não é prova, e vira None
    assert deslocamento_de_warp(f, {"warp_events": [{"x": 64, "y": 10}]}) is None
    # nosso warp que não cai em warp nenhum da fonte derruba o candidato
    assert deslocamento_de_warp(
        f, {"warp_events": [{"x": 64, "y": 10}, {"x": 70, "y": 15}]}) is None

    # 4. AS QUATRO PLACAS DA ROUTE 222, medidas no map.bin de verdade.
    # Antes da translação, (54,16) e (65,16) estavam no meio da faixa de parede
    # das linhas 15-17, sem UM vizinho andável, e (81,16) só era legível pelo
    # lado. Com o deslocamento que os warps provam (736,767), as quatro caem em
    # tile legível, e as duas de parede ficam com o tile de leitura embaixo,
    # colado na porta de cada casa, como a fonte desenha.
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    d = json.load(open(os.path.join(REPO, "data/maps/Route222/map.json"),
                       encoding="utf-8"))
    fonte = json.load(open(os.path.join(
        PLAT, "res/field/events/events_route_222.json")))
    assert deslocamento_de_warp(fonte, d) == (736, 767)
    # As QUATRO da licao de 18/08 continuam cobradas uma a uma, com o lado de
    # leitura que a translacao entrega. O que deixou de ser cobrado e a lista
    # FECHADA: a idempotencia por evento de 22/08/2026 traz placa nova para o
    # mesmo mapa a cada rodada (esta trouxe a de (70,25)), e um `==` de conjunto
    # transforma "importou mais" em vermelho. O invariante de verdade nunca foi
    # "sao exatamente estas quatro", e sim "NENHUMA placa importada fica sem
    # tile de leitura", que e literalmente o defeito da Route 222.
    esperado = {(85, 17): ["S", "W", "E"], (13, 20): ["N", "S", "W", "E"],
                (57, 17): ["S"], (68, 17): ["S"]}
    achado = {}
    for b in d["bg_events"]:
        if b.get("origem") == "pokeplatinum":
            achado[(b["x"], b["y"])] = leitura_de_placa(
                layouts, d["layout"], b["x"], b["y"])
    for k, v in esperado.items():
        assert achado.get(k) == v, (k, achado.get(k))
    ilegiveis = {k: v for k, v in achado.items() if not v}
    assert not ilegiveis, ilegiveis

    # 5. PLANTA PROVISORIA. Medido byte a byte: `IronIsland` tem map.bin
    # proprio e mesmo assim E o molde de portao `Route226_Access`, diferindo so
    # na linha 1, onde as portas sao furadas.
    #
    # O `LAYOUT_BATTLEFRONTIER` SAIU desta prova em 22/08/2026, e a razao esta
    # medida: a obra de tirar da ROM os mapas CORTADOS ja o encolheu para 1x1
    # (`data/layouts/BattleFrontier/map.bin` tem 2 bytes), entao ele deixou de
    # ser 13x9 e `planta_provisoria` responde False com razao. A prova estava
    # VERMELHA desde o commit da 0.l e nao por causa desta rodada; trocar o alvo
    # e medicao, nao afrouxamento, e o `IronIsland` continua guardando o portao.
    assert not planta_provisoria(layouts, "LAYOUT_BATTLEFRONTIER")
    # `LAYOUT_IRONISLAND` tambem saiu: o `converte_moldes_sinnoh.py` reescreveu
    # `data/layouts/IronIsland/map.bin` com a planta 32x32 do Platinum em
    # 21/08/2026, e o layout velho de 13x9 aponta para o MESMO arquivo. Ele
    # continua existindo so porque indice de layout que anda quebra save.
    assert not planta_provisoria(layouts, "LAYOUT_IRONISLAND")
    # O SEGUNDO molde, fixado em 21/08/2026: `LAYOUT_ROUTE208_ACCESS` e igual ao
    # de cima fora da linha das portas, e e ele que vestia o `OreburghGateB1F`.
    # Sem esta linha, alguem "simplifica" a comparacao para um `==` de nome e
    # perde metade das vitimas sem que nada fique vermelho.
    assert planta_provisoria(layouts, "LAYOUT_ROUTE208_ACCESS")
    # E a prova de que o estencil se conserta sozinho: com o molde historico
    # encolhido para 1x1, quem responde tem que ser o segundo, e nao "False para
    # todo mundo". Sem esta linha o portao volta a morrer calado.
    assert any(planta_provisoria(layouts, m) for m in MOLDES)
    # e nao pode ser um "13x9 e provisorio" preguicoso: a loja de flores tem
    # 15x9 e a Mt Coronet 5F e 32x32, e as duas sao planta de verdade.
    assert not planta_provisoria(layouts, "LAYOUT_MT_CORONET_5F")
    assert not planta_provisoria(layouts, "LAYOUT_FLOAROMA_TOWN_FLOWER_SHOP")

    # 6. MUTACAO PLANTADA no alcance. Emparedo, NA GRADE EM MEMORIA, os quatro
    # vizinhos de cada warp de MtCoronet5F e exijo que o alcance caia a zero.
    # Sem isto a BFS poderia estar devolvendo "todo tile andavel" e o portao de
    # posicao seria enfeite: e exatamente o erro que poe NPC em ilha fechada.
    m5 = json.load(open(os.path.join(REPO, "data/maps/MtCoronet5F/map.json")))
    W, H, g = grade(layouts, m5["layout"])
    warps = m5["warp_events"]
    antes = alcancaveis(W, H, g, warps)
    assert len(antes) > 100, len(antes)
    for w in warps:
        for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)):
            x, y = w["x"] + dx, w["y"] + dy
            if 0 <= x < W and 0 <= y < H:
                g[y][x] |= 1 << 10          # colisao 1: parede
    assert alcancaveis(W, H, g, warps) == set()

    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
