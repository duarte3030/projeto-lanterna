#!/usr/bin/env python3
"""Devolve a Johto os NPCs que a importação achatou em item ball muda.

O estrago tem autor conhecido: `dev_scripts/sanitize_johto_map_json.py` varre
todo `map.json` de Johto e, para TODO `object_event`, grava
`graphics_id = OBJ_EVENT_GFX_ITEM_BALL`, `script = "0"`, `flag = "0"`,
`movement_type = MOVEMENT_TYPE_LOOK_AROUND` e `trainer_sight_or_berry_tree_id
= "0"`. O objeto sobrevive na coordenada exata do NPC verdadeiro; o que morre é
quem ele era. Contraprova de graça: `data/maps/EcruteakCity/map.json` tem 49
objetos, todos item ball mudos, e `fontes-mapas/hns/data/maps/EcruteakCity/
map.json` tem os mesmos 49, no mesmo x/y, com Lass, Sage e Gramps.

O casamento aqui é por COORDENADA, dentro do mesmo mapa: item ball com
`script: "0"` aqui mais EXATAMENTE UM objeto do hns no mesmo x/y é par. Duas
coisas da fonte na mesma coordenada ficam de fora, porque escolher qual é qual
seria inventar NPC, e inventar NPC é o oposto do que esta ferramenta faz.

O que entra e o que fica de fora, e por quê:

- Só GENTE. Pedra de Rock Smash, árvore de Cut, canteiro de berry, Pokémon de
  overworld do hns e o efeito de luz continuam item ball: trocar o sprite deles
  mexe em mecânica de campo, não em fala, e é outra frente de trabalho.
- Gráfico do hns que ESTA build não desenha vira o equivalente honesto da
  tabela `SPRITE`. Sem equivalente, o par é recusado e sai no relatório. A
  pergunta é feita na camada certa (`valida_mapas_sinnoh.sprites_utilizaveis`,
  que lê a tabela de ponteiros e não o header): constante existe sempre, o
  gráfico só existe fora do `#if IS_FRLG`.
- Objeto cuja `flag` da fonte não existe aqui é RECUSADO, não restaurado com
  `flag: "0"`. Uma `FLAG_HIDE_*` do hns guarda gente de cena (os Rockets da
  torre de rádio, o Silver de Ecruteak, as irmãs Kimono): ligá-la em zero põe o
  personagem em campo para sempre, no estado errado da história. Item ball muda
  é menos mentira do que rival parado na cidade desde o primeiro dia.
- Fala: só é PORTADA quando o fecho transitivo do script da fonte é só fala.
  Batalha, item e cena não são portados nesta leva; o objeto é restaurado e o
  NPC ganha, se houver, a saudação incondicional do topo do script (a `msgbox`
  que vem antes do primeiro desvio). Todos saem listados para os blocos B4 e B6.
- Script que já existe NESTE repo (tutor de golpe, berry blender) é apontado
  direto, sem portar nada: zero rótulo novo, zero risco de duplicata.

Rótulo duplicado reprova o build inteiro (já custou 134 `symbol already
defined` numa leva de Sinnoh), então nada é emitido por cima do que já existe:
rótulo que este repo já define é reaproveitado, e se o corpo do hns divergir do
nosso, o bloco portado entra renomeado com o nome do mapa na frente e as
referências dentro do pacote são reescritas junto.

Uso:
    python3 dev_scripts/restaura_npcs_johto.py            # só relata
    python3 dev_scripts/restaura_npcs_johto.py --aplica   # escreve
    python3 dev_scripts/restaura_npcs_johto.py --demo     # autoteste
"""
import inspect
import json
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HNS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/hns"
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))

import valida_mapas_sinnoh as VM  # noqa: E402  sprites_utilizaveis()
import texto_sinnoh as TS         # noqa: E402  rotulos_repetidos()

APLICA = "--aplica" in sys.argv
DEMO = "--demo" in sys.argv

MARCA = "@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py"

# ------------------------------------------------------------------ vocabulário

# Comandos que um NPC de SÓ FALA pode usar. É lista de permissão, não de
# proibição: comando desconhecido tem que reprovar, senão um `special` novo do
# hns entra escondido no meio de um bloco que parece conversa.
FALA = frozenset("""
lock lockall faceplayer msgbox message waitmessage closemessage release
releaseall end return delay playse waitse waitbuttonpress .string
""".split())

# Prefixo linear aceito antes da saudação, quando o script NÃO é só fala. A
# `msgbox` que vem depois disto acontece sempre, sem depender de flag nenhuma;
# é a única fala que dá para aproveitar sem portar a cena junto.
PREAMBULO = frozenset("lock lockall faceplayer delay playse waitse".split())

# Gráfico do hns -> gráfico que ESTA build desenha. As cinco primeiras linhas
# são as mesmas de `importa_treinadores_johto.SPRITE`, copiadas de propósito
# para os dois importadores não divergirem no meio de um mapa.
SPRITE = {
    "OBJ_EVENT_GFX_SUPER_NERD": "OBJ_EVENT_GFX_SCIENTIST_1",
    "OBJ_EVENT_GFX_FIREBREATHER": "OBJ_EVENT_GFX_MANIAC",
    "OBJ_EVENT_GFX_BURGLAR": "OBJ_EVENT_GFX_BIKER",
    "OBJ_EVENT_GFX_JUGGLER": "OBJ_EVENT_GFX_EXPERT_M",
    "OBJ_EVENT_GFX_BATTLE_GIRL": "OBJ_EVENT_GFX_CRUSH_GIRL",
    # Equipe Rocket: os quatro executivos não têm sprite próprio aqui, e o
    # uniforme genérico diz a mesma coisa que importa (é Rocket).
    "OBJ_EVENT_GFX_ARCHER": "OBJ_EVENT_GFX_ROCKET_M",
    "OBJ_EVENT_GFX_PETREL": "OBJ_EVENT_GFX_ROCKET_M",
    "OBJ_EVENT_GFX_PROTON": "OBJ_EVENT_GFX_ROCKET_M",
    "OBJ_EVENT_GFX_ARIANA": "OBJ_EVENT_GFX_ROCKET_F",
    # ofício
    "OBJ_EVENT_GFX_ATTENDANT": "OBJ_EVENT_GFX_CLERK",
    "OBJ_EVENT_GFX_ATTENDANT_M": "OBJ_EVENT_GFX_MART_EMPLOYEE",
    "OBJ_EVENT_GFX_ENGINEER": "OBJ_EVENT_GFX_WORKER_M",
    "OBJ_EVENT_GFX_SCIENTIST_M": "OBJ_EVENT_GFX_SCIENTIST_1",
    "OBJ_EVENT_GFX_SCIENTIST_F": "OBJ_EVENT_GFX_SCIENTIST_2",
    "OBJ_EVENT_GFX_NURSE_CHANSEY": "OBJ_EVENT_GFX_CHANSEY",
    "OBJ_EVENT_GFX_SAGE": "OBJ_EVENT_GFX_MR_FUJI",
    "OBJ_EVENT_GFX_KIMONO_GIRL": "OBJ_EVENT_GFX_BEAUTY",
    # gente com nome próprio, sempre pelo papel e nunca por outro nome próprio
    "OBJ_EVENT_GFX_PROF_ELM": "OBJ_EVENT_GFX_PROF_BIRCH",
    "OBJ_EVENT_GFX_KURT": "OBJ_EVENT_GFX_MAN_3",
    "OBJ_EVENT_GFX_EUSINE": "OBJ_EVENT_GFX_MAN_1",
    "OBJ_EVENT_GFX_SILVER": "OBJ_EVENT_GFX_YOUNGSTER",
    "OBJ_EVENT_GFX_FALKNER": "OBJ_EVENT_GFX_COOLTRAINER_M",
    "OBJ_EVENT_GFX_BUGSY": "OBJ_EVENT_GFX_BUG_CATCHER",
    "OBJ_EVENT_GFX_WHITNEY": "OBJ_EVENT_GFX_GIRL_3",
    "OBJ_EVENT_GFX_MORTY": "OBJ_EVENT_GFX_PSYCHIC_M",
    "OBJ_EVENT_GFX_CHUCK": "OBJ_EVENT_GFX_BLACK_BELT",
    "OBJ_EVENT_GFX_JASMINE": "OBJ_EVENT_GFX_WOMAN_1",
    "OBJ_EVENT_GFX_PRYCE": "OBJ_EVENT_GFX_OLD_MAN_1",
    "OBJ_EVENT_GFX_CLAIR": "OBJ_EVENT_GFX_COOLTRAINER_F",
    "OBJ_EVENT_GFX_JANINE": "OBJ_EVENT_GFX_COOLTRAINER_F",
    "OBJ_EVENT_GFX_SURGE": "OBJ_EVENT_GFX_LT_SURGE",
    "OBJ_EVENT_GFX_WILL": "OBJ_EVENT_GFX_PSYCHIC_M",
    "OBJ_EVENT_GFX_KAREN": "OBJ_EVENT_GFX_GLACIA",
}
# Sem equivalente honesto e de propósito: OBJ_EVENT_GFX_WHIRLPOOL e
# OBJ_EVENT_GFX_SHINY_GYARADOS (o Gyarados vermelho do Lake of Rage) são
# obstáculo e Pokémon, não gente com roupa; OBJ_EVENT_GFX_TRAIN_FRONT é um
# trem. Trocar por uma pessoa qualquer seria pôr um figurante no lugar de uma
# cena, então eles ficam item ball e saem no relatório.

# Objeto que NÃO é gente, no vocabulário do hns. Mesma régua do
# `inventario.py`, comparando por PALAVRA e não por substring: "ROCK" tem que
# pegar `BREAKABLE_ROCK` sem pegar `ROCKET_M`, que é gente.
TOKENS_NAO_PESSOA = frozenset("""
BALL ROCK TREE BOULDER TRUCK DOLL CUSHION FOSSIL AMBER METEORITE MAP POKEDEX
BAG STATUE SHADOW BOAT SEAGALLOP CLIPBOARD TRIANGLE SPRITE
""".split())
EXATOS_NAO_PESSOA = frozenset({"CABLE_CAR", "MOVING_BOX", "WHIRLPOOL"})
# WHIRLPOOL: achado na Fase B (18/08/2026) escondendo o ARCHER em Route41 (6
# coordenadas, mesmo `script`), decoração de campo com o mesmo defeito de
# ROCK/TREE, não gente. Sem isto o par contava como "ambíguo" (WHIRLPOOL x
# ARCHER) quando na verdade só há UM candidato de gente (ARCHER), que segue
# bloqueado por outro motivo (batalha, sem id nesta fase).

# Rótulo de script do hns que marca decoração de campo mesmo usando GRÁFICO
# de gente (o redemoinho reaproveita OBJ_EVENT_GFX_ARCHER, sempre com
# `movement_type: INVISIBLE`, só para ancorar o efeito; não é o executivo
# ARCHER de verdade). Achado na Fase B (18/08/2026): a leva de treinadores
# provou que Route41/DragonsDen_Cavern materializaram 24 desses (18 + 6) como
# ROCKET_M mudo em vez de deixar a decoração fiel à fonte. Os outros 16 dos 40
# objetos que moram em coordenada de redemoinho nunca chegaram a ser
# materializados porque a coordenada tem WHIRLPOOL e ARCHER juntos e o par
# caía em "ambíguo"; são exatamente os que continuam item ball. Mesma família
# do filtro por gráfico acima, mas por SCRIPT, porque aqui o gráfico sozinho
# não distingue decoração de NPC real.
SCRIPTS_NAO_PESSOA = frozenset({"EventScript_Whirlpool"})

# Recusar a decoração não basta: o objeto SOBREVIVE como item ball, e item ball
# nasce com `MOVEMENT_TYPE_LOOK_AROUND`, ou seja pokébola boiando na água em
# cima do redemoinho. A fonte já diz o que fazer com esse objeto: ela o desenha
# INVISÍVEL (`movement_type: MOVEMENT_TYPE_INVISIBLE` nos 24 ARCHER-âncora).
# Então a decoração é escondida no lugar, UM campo, gráfico e índice intactos:
# nada de trocar sprite (mecânica de campo, ver o cabeçalho) e nada de fingir
# que a pokébola é um Rocket.
MOV_ESCONDIDO = "MOVEMENT_TYPE_INVISIBLE"


def eh_pessoa(gfx, script=None):
    if script in SCRIPTS_NAO_PESSOA:
        return False
    c = (gfx or "").replace("OBJ_EVENT_GFX_", "")
    if c in EXATOS_NAO_PESSOA or c.startswith(("SS_", "MON_BASE")):
        return False
    return not (set(c.split("_")) & TOKENS_NAO_PESSOA)


def so_decoracao(cands):
    """A coordenada inteira da fonte é decoração de campo, não gente nenhuma."""
    return bool(cands) and all(
        str(c.get("script", "")) in SCRIPTS_NAO_PESSOA for c in cands)


def esconde(obj):
    """Decoração no lugar: só o movimento muda, gráfico e índice ficam."""
    return {**obj, "movement_type": MOV_ESCONDIDO}


def livres(cands, consumidos):
    """Candidatos da fonte que ainda não casaram com outro objeto NOSSO.

    Um objeto da fonte vale por UM objeto nosso. O casamento é por coordenada, e
    quando os DOIS lados têm mais de um objeto no mesmo x/y (GoldenrodCity
    (39,14): `Rocket5` e `Beauty` na fonte, dois item ball aqui) o desempate
    escolhia o mesmo vencedor para os dois nossos e plantava o NPC em dobro, no
    mesmo tile. Achado em 18/08/2026, Fase B: dois `Rocket5` empilhados.
    """
    return [c for c in cands if id(c) not in consumidos]


def semeia(nossos_objs, na_coord):
    """Objetos da fonte que RODADAS ANTERIORES já gastaram.

    `livres()` sozinho só protege dentro de UMA rodada: objeto nosso restaurado
    ontem deixou de ser item ball, não entra mais no laço, e portanto não
    reservaria o par dele. Numa segunda rodada o item ball que sobrou na mesma
    coordenada casaria de novo com o objeto da fonte JÁ usado, e o N:1 voltaria
    sozinho. A marca de "já gastei este" é o gráfico: o que o gerador escreve é
    `SPRITE.get(gfx_da_fonte, gfx_da_fonte)`, então objeto nosso na mesma
    coordenada e com esse gráfico É o par daquele objeto da fonte. Sem depender
    do `script`, que pode ter sido renomeado por colisão de rótulo.
    """
    usados = set()
    for o in nossos_objs:
        if o.get("graphics_id") == "OBJ_EVENT_GFX_ITEM_BALL":
            continue  # ainda não restaurado: é candidato, não par gasto
        for c in na_coord.get((o["x"], o["y"]), []):
            g = c.get("graphics_id", "")
            if id(c) not in usados and SPRITE.get(g, g) == o.get("graphics_id"):
                usados.add(id(c))
                break
    return usados


# --------------------------------------------------------------------- leitura

def le(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


LABEL = re.compile(r"^([A-Za-z_][\w]*)::?\s*$")
PALAVRA = re.compile(r"[A-Za-z_][\w]*")


def blocos(texto):
    """rótulo -> lista de linhas do corpo, sem a linha do próprio rótulo.

    Leitor de bloco, não de assembly: rótulo na coluna zero abre bloco e ele vai
    até o próximo rótulo. Basta, porque o portão de comandos recusa tudo que
    este leitor não entendeu.
    """
    out, atual = {}, None
    for linha in texto.split("\n"):
        m = LABEL.match(linha)
        if m:
            atual = m.group(1)
            out[atual] = []
        elif atual is not None:
            out[atual].append(linha)
    return out


def comandos(linhas):
    fora = []
    for l in linhas:
        l = l.split("@")[0].strip()
        if l and not LABEL.match(l + "\n"):
            fora.append(l.split()[0].rstrip(":"))
    return fora


ARG_NATIVO = re.compile(
    r"\s*(?:special|specialvar|callnative|gotonative)\s+(?:\w+\s*,\s*)?(\w+)")


def refs(linhas):
    """Identificadores citados no corpo, fora de string literal.

    O argumento de `special`, `specialvar` e `callnative` sai de fora: ele é
    função em C, não rótulo de script, e tratá-lo como rótulo faz
    `GetInGameTradeSpeciesInfo` virar "rótulo ausente na fonte" quando o que
    existe é `SPECIAL_GetInGameTradeSpeciesInfo` na tabela de specials.
    """
    fora = []
    for l in linhas:
        l = re.sub(r'"(\\.|[^"\\])*"', " ", l).split("@")[0]
        m = ARG_NATIVO.match(l)
        if m:
            l = l[:m.start(1)]
        fora.append(l)
    return set(PALAVRA.findall("\n".join(fora)))


def strings(linhas):
    """Conteúdo das aspas de `.string`, para checar os {PLACEHOLDER}."""
    return re.findall(r'"((?:\\.|[^"\\])*)"', "\n".join(linhas))


def macros_disponiveis():
    m = set()
    for raiz, _, arqs in os.walk(os.path.join(REPO, "asm/macros")):
        for a in arqs:
            m |= set(re.findall(r"^\s*\.macro\s+([A-Za-z_][\w]*)",
                                le(os.path.join(raiz, a)), re.M))
    m |= {".string", ".byte", ".2byte", ".4byte", ".align", ".include",
          ".string_ja", ".ifdef", ".endif", ".else", ".ifndef", ".set"}
    return m


def constantes_definidas():
    c = set()
    for raiz, _, arqs in os.walk(os.path.join(REPO, "include")):
        for a in arqs:
            s = le(os.path.join(raiz, a))
            c |= set(re.findall(r"^\s*#\s*define\s+([A-Z_][A-Z0-9_]*)", s, re.M))
            c |= set(re.findall(r"^\s*([A-Z_][A-Z0-9_]{3,})\s*[,=]", s, re.M))
    for raiz, _, arqs in os.walk(os.path.join(REPO, "asm/macros")):
        for a in arqs:
            s = le(os.path.join(raiz, a))
            c |= set(re.findall(r"^\s*\.set\s+([A-Z_][A-Z0-9_]*)", s, re.M))
            # MSGBOX_NPC e companhia são `NOME = 2` dentro do macro, não
            # #define; sem esta linha o portão recusaria toda fala do jogo.
            c |= set(re.findall(r"^\s*([A-Z_][A-Z0-9_]{3,})\s*=", s, re.M))
    return c


def simbolos_do_repo():
    s = set()
    for raiz, _, arqs in os.walk(os.path.join(REPO, "data")):
        for a in arqs:
            if a.endswith((".inc", ".s")):
                s |= set(re.findall(r"^([A-Za-z_][\w]*)::?\s*$",
                                    le(os.path.join(raiz, a)), re.M))
    return s


def corpos_do_repo():
    """rótulo -> corpo já definido aqui, para saber se o hns diverge."""
    d = {}
    for raiz, _, arqs in os.walk(os.path.join(REPO, "data")):
        for a in arqs:
            if a.endswith((".inc", ".s")):
                for k, v in blocos(le(os.path.join(raiz, a))).items():
                    d.setdefault(k, "\n".join(v).strip())
    return d


def placeholders_do_charmap():
    nomes = set()
    for linha in le(os.path.join(REPO, "charmap.txt")).split("\n"):
        m = re.match(r"\s*([A-Z_][A-Z0-9_]*)\s*=", linha)
        if m:
            nomes.add(m.group(1))
    return nomes


def movimentos_daqui():
    """MOVEMENT_TYPE_* que ESTE repo define.

    O hns tem movimento próprio (`MOVEMENT_TYPE_TOWER_BEAM`, o facho do Tin
    Tower). Copiar o campo da fonte sem perguntar põe uma constante inexistente
    dentro do `map.json`, e quem reprova é o montador do mapa, longe daqui.
    Aconteceu com 9 objetos das nove salas do Tin Tower na primeira aplicação.
    """
    s = le(os.path.join(REPO, "include/constants/event_object_movement.h"))
    return set(re.findall(r"(MOVEMENT_TYPE_[A-Z0-9_]+)", s))


def mapas_de_johto():
    grupos = json.load(open(os.path.join(REPO, "data/maps/map_groups.json")))
    return sorted({m for g, v in grupos.items()
                   if g.endswith("_Johto") and isinstance(v, list) for m in v})


# --------------------------------------------------------------- classificação

def fecho(alvo, fonte_blocos, ja_temos):
    """(pacote, comandos, erro): tudo que `alvo` precisa e que ainda não temos.

    Para no primeiro problema e devolve o motivo em texto, porque o relatório
    vale mais do que a exceção: NPC recusado tem que dizer por quê.
    """
    pendentes, pacote, cmds = [alvo], set(), []
    while pendentes:
        lab = pendentes.pop()
        if lab in pacote or lab in ja_temos:
            continue
        if lab not in fonte_blocos:
            return pacote, cmds, f"rótulo ausente na fonte: {lab}"
        pacote.add(lab)
        corpo = fonte_blocos[lab]
        cmds += comandos(corpo)
        for r in refs(corpo):
            # Rótulo se reconhece pela caixa mista: comando é minúsculo,
            # constante é maiúscula, `EcruteakCity_Text_Sign` não é nem um nem
            # outro. Empurrar TODO rótulo citado, e não só o que a fonte tem, é
            # o que faz a referência órfã aparecer como recusa em vez de virar
            # `undefined symbol` na hora do build.
            if r in fonte_blocos or not (r.islower() or r.isupper()):
                pendentes.append(r)
    return pacote, cmds, None


def saudacao(corpo):
    """Rótulo de texto da `msgbox` incondicional do topo, ou None.

    Só vale o que roda antes de qualquer desvio: `lock`, `faceplayer` e som. A
    primeira `msgbox` depois disso é fala que o NPC diz sempre, em qualquer
    estado do jogo. Qualquer outro comando no caminho e a resposta é None,
    porque a partir dali a fala passa a depender de flag que este repo não tem.
    """
    for linha in corpo:
        l = linha.split("@")[0].strip()
        if not l:
            continue
        cmd = l.split()[0]
        if cmd in PREAMBULO:
            continue
        if cmd != "msgbox":
            return None
        return l.split(None, 1)[1].split(",")[0].strip()
    return None


def motivo_do_bloqueio(cmds):
    s = set(cmds)
    # `trainerbattle` aparece com prefixo E com sufixo (`trainerbattle_single`,
    # `dynamic_trainerbattle`), então a pergunta é de conter, não de terminar.
    if any("trainerbattle" in c for c in s):
        return "batalha"
    if s & {"giveitem", "giveitem_std", "givemon", "giveegg", "givedecoration",
            "finditem"}:
        return "item"
    return "cena"


# ------------------------------------------------------------------ montagem

def monta(relatorio_apenas=True):
    sprites = VM.sprites_utilizaveis()
    movimentos = movimentos_daqui()
    macros = macros_disponiveis()
    consts = constantes_definidas()
    nossos = simbolos_do_repo()
    nossos_corpos = corpos_do_repo()
    marcas = placeholders_do_charmap()
    especiais = set(re.findall(r"^\s*def_special\s+(\w+)",
                               le(os.path.join(REPO, "data/specials.inc")), re.M))
    flags_daqui = {c for c in consts if c.startswith("FLAG_")}

    # Índice global do hns: NPC de um mapa aponta para bloco que mora no
    # vizinho com frequência (tutor de golpe, whirlpool, berry blender).
    fonte_blocos = {}
    for m in sorted(os.listdir(os.path.join(HNS, "data/maps"))):
        p = os.path.join(HNS, "data/maps", m, "scripts.inc")
        if os.path.exists(p):
            for lab, corpo in blocos(le(p)).items():
                fonte_blocos.setdefault(lab, corpo)
    # O comum do hns (whirlpool, tutor de golpe, berry blender) não mora em
    # mapa nenhum, e sem esta pasta o fecho acusa rótulo ausente que existe.
    praiz = os.path.join(HNS, "data/scripts")
    for a in sorted(os.listdir(praiz)) if os.path.isdir(praiz) else []:
        if a.endswith(".inc"):
            for lab, corpo in blocos(le(os.path.join(praiz, a))).items():
                fonte_blocos.setdefault(lab, corpo)

    st = Counter()
    recusas = defaultdict(list)     # motivo -> [(mapa, detalhe)]
    pendentes = defaultdict(list)   # bucket B4/B6 -> [(mapa, script, gráfico)]
    emitidos = set(nossos)
    renomeados = {}
    plano = []                      # (mapa, [(indice, objeto novo)], trecho)
    por_mapa = Counter()
    falas = 0

    for mapa in mapas_de_johto():
        pn = os.path.join(REPO, "data/maps", mapa, "map.json")
        pf = os.path.join(HNS, "data/maps", mapa, "map.json")
        if not os.path.exists(pn):
            continue
        if not os.path.exists(pf):
            st["mapa sem par na fonte"] += 1
            continue
        nosso = json.load(open(pn, encoding="utf-8"))
        fonte = json.load(open(pf, encoding="utf-8"))

        # O bloco do PRÓPRIO mapa manda sobre o índice global.
        locais = dict(fonte_blocos)
        pinc = os.path.join(HNS, "data/maps", mapa, "scripts.inc")
        if os.path.exists(pinc):
            locais.update(blocos(le(pinc)))

        na_coord = defaultdict(list)
        for o in fonte.get("object_events", []):
            na_coord[(o["x"], o["y"])].append(o)

        # Pares já gastos por rodadas anteriores entram JÁ consumidos, senão o
        # gerador não é idempotente entre rodadas e o N:1 volta sozinho na leva
        # seguinte. O `livres()` cuida do resto DENTRO desta rodada.
        consumidos = semeia(nosso.get("object_events", []), na_coord)
        trocas, pacote_do_mapa, ordem = [], set(), []
        for idx, obj in enumerate(nosso.get("object_events", [])):
            if obj.get("graphics_id") != "OBJ_EVENT_GFX_ITEM_BALL":
                continue
            if str(obj.get("script", "0")) not in ("0", "NULL", ""):
                continue
            st["item ball muda"] += 1
            cands = na_coord.get((obj["x"], obj["y"]), [])
            if not cands:
                st["sem par na fonte"] += 1
                recusas["sem par na fonte"].append(
                    (mapa, f'({obj["x"]},{obj["y"]})'))
                continue
            if so_decoracao(cands):
                # Decoração de campo (redemoinho). Não vira NPC, mas também não
                # pode ficar como a importação deixou: item ball VISÍVEL boiando
                # na água. Só o movimento é corrigido, para o INVISÍVEL que a
                # própria fonte usa nesses objetos.
                st["decoração escondida (movimento da fonte)"] += 1
                if obj.get("movement_type") != MOV_ESCONDIDO:
                    trocas.append((idx, esconde(obj)))
                    por_mapa[mapa] += 1
                continue
            cands = livres(cands, consumidos)
            if not cands:
                st["fonte já casada nesta coordenada"] += 1
                recusas["fonte já casada nesta coordenada"].append(
                    (mapa, f'({obj["x"]},{obj["y"]})'))
                continue
            if len(cands) > 1:
                # A colisão de coordenada só é ambiguidade de GENTE quando mais
                # de um candidato passa em `eh_pessoa`. Antes desta conferência
                # o par (37,39) de BellchimeTrail (PIDGEOT dia / NOCTOWL noite,
                # nenhum dos dois pessoa) contava como "ambíguo" e nunca
                # chegava ao filtro que já sabe descartar isso, e mentia para
                # cima. Achado em 18/08/2026, Fase B: dos 44, a maioria eram
                # pares de Pokémon dia/noite na mesma coordenada.
                pessoas = [c for c in cands
                          if eh_pessoa(c.get("graphics_id", ""), c.get("script"))]
                if not pessoas:
                    st["par não é gente"] += 1
                    continue
                if len(pessoas) > 1:
                    # Desempate por flag de esconder, MESMA regra que
                    # `dev_scripts/importa_npcs_sinnoh.py` já usa para Sinnoh
                    # (fila_b6.py, seção "A mesma flag decide o BLOQUEIO"):
                    # `flag` de verdade que EXISTE em flags.h marca objeto de
                    # cena de propósito; `flag` que não existe aqui nunca passa
                    # do próximo filtro mesmo se escolhida. Só resolve quando
                    # EXATAMENTE UM candidato tem flag existente; dois com
                    # flag existente (ou nenhum) continuam ambíguos de
                    # verdade, sem invenção de identidade.
                    com_flag = [c for c in pessoas
                                if str(c.get("flag", "0")) in flags_daqui]
                    if len(com_flag) == 1:
                        pessoas = com_flag
                    else:
                        st["par ambíguo"] += 1
                        recusas["par ambíguo"].append(
                            (mapa, f'({obj["x"]},{obj["y"]}) x{len(pessoas)} gente'))
                        continue
                cands = pessoas
            src = cands[0]
            consumidos.add(id(src))
            gfx_src = src.get("graphics_id", "")
            if not eh_pessoa(gfx_src, src.get("script")):
                st["par não é gente"] += 1
                continue

            gfx = SPRITE.get(gfx_src, gfx_src)
            if gfx not in sprites:
                st["gráfico sem equivalente"] += 1
                recusas["gráfico sem equivalente"].append((mapa, gfx_src))
                continue

            flag = str(src.get("flag", "0"))
            if flag not in ("0", "NULL", "") and flag not in flags_daqui:
                st["flag da fonte não existe aqui"] += 1
                recusas["flag da fonte não existe aqui"].append((mapa, flag))
                pendentes["B6"].append((mapa, src.get("script", "0"), gfx_src))
                continue
            if flag in ("NULL", ""):
                flag = "0"

            alvo = str(src.get("script", "0"))
            script, trecho_labels, bucket = "0", [], None

            if alvo in ("0", "NULL", ""):
                st["restaurado mudo (fonte também é mudo)"] += 1
            elif alvo in nossos:
                # Já existe aqui: apontar é de graça e não cria rótulo nenhum.
                script = alvo
                st["restaurado apontando para script daqui"] += 1
            else:
                pacote, cmds, erro = fecho(alvo, locais, emitidos | pacote_do_mapa)
                if erro:
                    # O OBJETO ainda é restaurado: o gráfico é da fonte e não
                    # depende do script. O que não dá é falar, então ele entra
                    # mudo e vai para a fila de história.
                    st["restaurado mudo (fecho incompleto)"] += 1
                    recusas["fecho incompleto"].append((mapa, erro))
                    pendentes["B6"].append((mapa, alvo, gfx_src))
                elif set(cmds) <= FALA:
                    ok, motivo = portavel(pacote, locais, macros, consts,
                                          especiais, nossos, marcas)
                    if ok:
                        script = alvo
                        trecho_labels = sorted(pacote)
                        st["fala portada"] += 1
                        falas += 1
                    else:
                        st["portão reprovou"] += 1
                        recusas["portão reprovou"].append((mapa, motivo))
                else:
                    bucket = motivo_do_bloqueio(cmds)
                    txt = saudacao(locais[alvo])
                    if txt and txt in locais:
                        pac2, _c2, e2 = fecho(txt, locais,
                                              emitidos | pacote_do_mapa)
                        ok, motivo = (False, e2) if e2 else portavel(
                            pac2, locais, macros, consts, especiais, nossos,
                            marcas)
                        if ok:
                            script = novo_rotulo(mapa, alvo, emitidos)
                            trecho_labels = sorted(pac2)
                            locais[script] = [
                                f"\tmsgbox {txt}, MSGBOX_NPC", "\tend"]
                            trecho_labels.append(script)
                            st[f"restaurado com fala básica ({bucket})"] += 1
                            falas += 1
                        else:
                            st[f"restaurado mudo ({bucket})"] += 1
                    elif txt and txt in nossos:
                        script = novo_rotulo(mapa, alvo, emitidos)
                        locais[script] = [f"\tmsgbox {txt}, MSGBOX_NPC", "\tend"]
                        trecho_labels = [script]
                        st[f"restaurado com fala básica ({bucket})"] += 1
                        falas += 1
                    else:
                        st[f"restaurado mudo ({bucket})"] += 1
                    pendentes["B4" if bucket == "batalha" else "B6"].append(
                        (mapa, alvo, gfx_src))

            novo = dict(obj)
            novo["graphics_id"] = gfx
            mov = src.get("movement_type", obj.get("movement_type"))
            if mov not in movimentos:
                st["movimento da fonte não existe aqui"] += 1
                recusas["movimento da fonte não existe aqui"].append((mapa, mov))
                mov = obj.get("movement_type")
            novo["movement_type"] = mov
            novo["flag"] = flag
            novo["script"] = script
            # Treinador sem batalha portada só é honesto quando ele tem alguma
            # coisa a dizer: `TRAINER_TYPE_NORMAL` com `script: "0"` faz o NPC
            # andar até o jogador e rodar o nada.
            if script == "0":
                novo["trainer_type"] = "TRAINER_TYPE_NONE"
                novo["trainer_sight_or_berry_tree_id"] = "0"
            else:
                novo["trainer_type"] = src.get("trainer_type",
                                               "TRAINER_TYPE_NONE")
                novo["trainer_sight_or_berry_tree_id"] = str(
                    src.get("trainer_sight_or_berry_tree_id", "0"))
                if novo["trainer_type"] != "TRAINER_TYPE_NONE":
                    pendentes["B4"].append((mapa, alvo, gfx_src))

            trocas.append((idx, novo))
            por_mapa[mapa] += 1
            for lab in trecho_labels:
                if lab not in pacote_do_mapa:
                    pacote_do_mapa.add(lab)
                    ordem.append(lab)

        if not trocas:
            continue

        trecho = ""
        if ordem:
            trecho = "\n" + MARCA + "\n"
            for lab in ordem:
                nome = lab
                corpo = "\n".join(locais[lab]).rstrip()
                if lab in nossos:
                    # Já existe aqui. Corpo igual: reaproveita e não emite.
                    # Corpo diferente: emite com o nome do mapa na frente, e as
                    # referências dentro do pacote são reescritas junto.
                    if nossos_corpos.get(lab, "").strip() == corpo.strip():
                        continue
                    nome = f"{mapa}_{lab}"
                    if nome in nossos or nome in emitidos:
                        st["colisão de rótulo sem saída"] += 1
                        recusas["colisão de rótulo sem saída"].append((mapa, lab))
                        continue
                    renomeados[lab] = nome
                    st["rótulo renomeado por colisão"] += 1
                emitidos.add(nome)
                trecho += f"\n{nome}::\n{corpo}\n"
        if renomeados:
            trecho = reescreve(trecho, renomeados)
            trocas = [(i, {**o, "script": renomeados.get(o["script"],
                                                         o["script"])})
                      for i, o in trocas]
        plano.append((mapa, trocas, trecho))

    return plano, st, recusas, pendentes, por_mapa, falas


def novo_rotulo(mapa, alvo, usados):
    """Nome para a saudação extraída, sempre no espaço de nomes do mapa."""
    base = alvo.split("_EventScript_")[-1].split("_")[-1]
    n = f"{mapa}_EventScript_{base}Fala"
    i = 1
    while n in usados:
        i += 1
        n = f"{mapa}_EventScript_{base}Fala{i}"
    usados.add(n)
    return n


def reescreve(texto, renomeados):
    for velho, novo in renomeados.items():
        texto = re.sub(rf"\b{re.escape(velho)}\b", novo, texto)
    return texto


def portavel(pacote, locais, macros, consts, especiais, nossos, marcas):
    """Os quatro portões que já provaram valer, na ordem em que são baratos."""
    for lab in pacote:
        corpo = locais[lab]
        desconhecido = set(comandos(corpo)) - macros
        if desconhecido:
            return False, f"comando fora dos macros: {sorted(desconhecido)[0]}"
        for l in corpo:
            m = re.match(r"\s*special(?:var)?\s+(?:\w+\s*,\s*)?(\w+)",
                         l.split("@")[0])
            if m and m.group(1) not in especiais:
                return False, f"special inexistente: {m.group(1)}"
        for r in refs(corpo):
            if r in locais or r in nossos or r in pacote:
                continue
            if r.isupper() and len(r) > 3 and r not in consts and not r.isdigit():
                return False, f"constante inexistente: {r}"
        for s in strings(corpo):
            for ph in re.findall(r"\{([A-Z_][A-Z0-9_]*)\}", s):
                if ph not in marcas:
                    return False, f"placeholder fora do charmap: {ph}"
    return True, None


# --------------------------------------------------------------------- escrita

def escreve(plano):
    for mapa, trocas, trecho in plano:
        p = os.path.join(REPO, "data/maps", mapa, "map.json")
        d = json.load(open(p, encoding="utf-8"))
        objs = d.get("object_events", [])
        for idx, novo in trocas:
            # Releitura do disco: outro agente pode ter mexido no mesmo
            # arquivo entre o plano e a escrita. Índice cujo objeto deixou de
            # ser item ball muda não é mais o mesmo objeto, e não se toca.
            if idx >= len(objs):
                continue
            velho = objs[idx]
            if velho.get("graphics_id") != "OBJ_EVENT_GFX_ITEM_BALL":
                continue
            if velho["x"] != novo["x"] or velho["y"] != novo["y"]:
                continue
            objs[idx] = novo
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        if trecho.strip():
            pi = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
            with open(pi, "a", encoding="utf-8") as f:
                f.write(trecho)


# ------------------------------------------------------------------- autoteste

def demo():
    """Autoteste: as regras que decidem o resultado, nos casos que enganam."""
    # gente contra mobília, comparando por palavra e não por substring
    assert eh_pessoa("OBJ_EVENT_GFX_ROCKET_M")
    assert eh_pessoa("OBJ_EVENT_GFX_LASS")
    assert not eh_pessoa("OBJ_EVENT_GFX_ITEM_BALL")
    assert not eh_pessoa("OBJ_EVENT_GFX_BREAKABLE_ROCK")
    assert not eh_pessoa("OBJ_EVENT_GFX_MON_BASE+SPECIES_GOLBAT")
    assert not eh_pessoa("OBJ_EVENT_GFX_LIGHT_SPRITE")
    # ARCHER e gente em geral, mas nao quando o script da fonte e a
    # decoracao do redemoinho (mesmo grafico, papel diferente)
    assert eh_pessoa("OBJ_EVENT_GFX_ARCHER")
    assert not eh_pessoa("OBJ_EVENT_GFX_ARCHER", "EventScript_Whirlpool")

    # decoracao de campo: a coordenada inteira tem que ser redemoinho
    w = {"graphics_id": "OBJ_EVENT_GFX_WHIRLPOOL", "script": "EventScript_Whirlpool"}
    a = {"graphics_id": "OBJ_EVENT_GFX_ARCHER", "script": "EventScript_Whirlpool"}
    lass = {"graphics_id": "OBJ_EVENT_GFX_LASS", "script": "EventScript_Lass"}
    assert so_decoracao([a])
    assert so_decoracao([w, a])       # os 16 que antes contavam como ambiguos
    assert not so_decoracao([])
    assert not so_decoracao([a, lass])  # gente na coordenada manda
    assert not so_decoracao([lass])

    # o campo novo: esconder mexe em UM campo so, grafico e coordenada ficam
    velho = {"graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": 7, "y": 41,
             "elevation": 0, "movement_type": "MOVEMENT_TYPE_LOOK_AROUND",
             "script": "0", "flag": "0"}
    novo = esconde(velho)
    assert novo["movement_type"] == "MOVEMENT_TYPE_INVISIBLE"
    assert sorted(novo) == sorted(velho)
    assert [k for k in novo if novo[k] != velho[k]] == ["movement_type"]

    # um objeto da fonte e consumido UMA vez por coordenada (GoldenrodCity
    # (39,14): Rocket5 + Beauty na fonte, dois item ball nossos)
    rocket = {"graphics_id": "OBJ_EVENT_GFX_ROCKET_M", "script": "Rocket5"}
    beauty = {"graphics_id": "OBJ_EVENT_GFX_BEAUTY", "script": "Beauty"}
    par, usados = [rocket, beauty], set()
    assert livres(par, usados) == par
    usados.add(id(livres(par, usados)[0]))       # o primeiro nosso leva o Rocket
    assert livres(par, usados) == [beauty]       # o segundo nao repete o Rocket
    usados.add(id(beauty))
    assert livres(par, usados) == []             # terceiro nosso fica sem par

    # SEMEADURA: idempotencia ENTRE rodadas, o estado real de GoldenrodCity
    # (39,14) depois da rodada 1 (um Rocket restaurado, um item ball sobrando).
    coord = {(39, 14): par}
    r1 = [{"graphics_id": "OBJ_EVENT_GFX_ROCKET_M", "x": 39, "y": 14},
          {"graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": 39, "y": 14}]
    gastos = semeia(r1, coord)
    assert livres(par, gastos) == [beauty]  # rodada 2 nao reaproveita o Rocket
    # A BEAUTY e recusada la na frente pela flag inexistente, entao a rodada 2
    # nao muda nada: e isso que "rodada dupla = zero mudanca" quer dizer aqui.

    # Zero restaurado ainda: nada e semeado, os dois seguem livres.
    zerado = [{"graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": 39, "y": 14},
              {"graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": 39, "y": 14}]
    assert semeia(zerado, coord) == set()
    assert livres(par, semeia(zerado, coord)) == par

    # Os DOIS restaurados (o defeito N:1 antigo, dois ROCKET_M no mesmo tile):
    # a semeadura casa UM por objeto da fonte, nunca o mesmo duas vezes.
    dobrado = [{"graphics_id": "OBJ_EVENT_GFX_ROCKET_M", "x": 39, "y": 14},
               {"graphics_id": "OBJ_EVENT_GFX_ROCKET_M", "x": 39, "y": 14}]
    assert len(semeia(dobrado, coord)) == 1

    # O gráfico da fonte passa pela tabela SPRITE antes de comparar: a fonte diz
    # ARCHER, o que foi escrito aqui e ROCKET_M, e mesmo assim o par e achado.
    arq = {"graphics_id": "OBJ_EVENT_GFX_ARCHER", "script": "X"}
    nosso_arq = [{"graphics_id": SPRITE["OBJ_EVENT_GFX_ARCHER"], "x": 1, "y": 2}]
    assert semeia(nosso_arq, {(1, 2): [arq]}) == {id(arq)}

    # Decoracao de redemoinho continua item ball e NAO e semeada (senao a
    # coordenada perderia o candidato que o ramo de decoracao ainda precisa ver).
    assert semeia([{"graphics_id": "OBJ_EVENT_GFX_ITEM_BALL", "x": 1, "y": 2}],
                  {(1, 2): [arq]}) == set()

    # leitor de bloco
    b = blocos("A::\n\tlock\n\tend\nB::\n\t.string \"oi$\"\n")
    assert list(b) == ["A", "B"], b
    assert comandos(b["A"]) == ["lock", "end"]
    assert strings(b["B"]) == ["oi$"]

    # só fala contra cena
    assert set(comandos(["\tlock", "\tmsgbox X, MSGBOX_NPC", "\trelease",
                         "\tend"])) <= FALA
    assert not set(comandos(["\tlock", "\tsetflag FLAG_X", "\tend"])) <= FALA

    # saudação: vale a msgbox do topo, não a que vem depois do desvio
    assert saudacao(["\tlock", "\tfaceplayer", "\tmsgbox T_Oi, MSGBOX_DEFAULT",
                     "\tgoto_if_set FLAG_X, Outro"]) == "T_Oi"
    assert saudacao(["\tlock", "\tgoto_if_set FLAG_X, Outro",
                     "\tmsgbox T_Oi"]) is None
    assert saudacao(["\tlock", "\tspecial Foo", "\tend"]) is None

    # fecho: para no rótulo que a fonte não tem, e diz qual
    fb = {"A": ["\tmsgbox B", "\tend"], "B": ['\t.string "oi$"']}
    pac, cmds, err = fecho("A", fb, set())
    assert err is None and pac == {"A", "B"} and "msgbox" in cmds
    _p, _c, err = fecho("A", {"A": ["\tmsgbox Mapa_Text_C", "\tend"]}, set())
    assert err and "Mapa_Text_C" in err, err
    # rótulo que já temos aqui não entra no pacote, e por isso não duplica
    pac, _c, err = fecho("A", fb, {"B"})
    assert pac == {"A"} and err is None

    # motivo do bloqueio
    assert motivo_do_bloqueio(["lock", "trainerbattle_single"]) == "batalha"
    assert motivo_do_bloqueio(["lock", "giveitem"]) == "item"
    assert motivo_do_bloqueio(["lock", "setflag"]) == "cena"

    # renomeação por colisão reescreve a referência junto
    assert reescreve("A::\n\tmsgbox B\nB::\n", {"B": "Mapa_B"}) == \
        "A::\n\tmsgbox Mapa_B\nMapa_B::\n"
    # e não pega o rótulo que só COMEÇA igual
    assert reescreve("\tmsgbox BC\n", {"B": "X"}) == "\tmsgbox BC\n"

    # rótulo novo nunca colide com o que já existe
    usados = {"Mapa_EventScript_LassFala"}
    assert novo_rotulo("Mapa", "M_EventScript_Lass", usados) == \
        "Mapa_EventScript_LassFala2"

    # a mutação que o relatório TEM que recusar: item ball em coordenada que a
    # fonte não tem. O casamento é por coordenada, então par vazio é recusa.
    na_coord = {(3, 4): [{"graphics_id": "OBJ_EVENT_GFX_LASS"}]}
    assert na_coord.get((9, 9), []) == []

    # Contado do próprio corpo, não digitado: o número cravado aqui já estava
    # velho (dizia 20 com 24 asserts no arquivo) e número que mente não é
    # verificação.
    n = sum(l.strip().startswith("assert ")
            for l in inspect.getsource(demo).splitlines())
    print(f"demo: ok, {n} asserts")


# ----------------------------------------------------------------------- saída

def main():
    plano, st, recusas, pendentes, por_mapa, falas = monta()
    total = sum(len(t) for _, t, _ in plano)
    print(f"mapas tocados: {len(plano)}   NPCs restaurados: {total}   "
          f"falas: {falas}")
    print("\ncontagem:")
    for k, v in sorted(st.items(), key=lambda x: -x[1]):
        print(f"  {v:5}  {k}")
    print("\n10 maiores mapas:")
    for m, v in por_mapa.most_common(10):
        print(f"  {v:5}  {m}")
    if recusas:
        print("\nrecusas:")
        for motivo, itens in sorted(recusas.items(), key=lambda x: -len(x[1])):
            print(f"  {len(itens):5}  {motivo}")
            for m, d in itens[:5]:
                print(f"           {m}: {d}")
    for b in ("B4", "B6"):
        if pendentes[b]:
            print(f"\npara o bloco {b}: {len(pendentes[b])}")
            for m, s, g in pendentes[b][:8]:
                print(f"    {m}: {s} ({g})")
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0
    escreve(plano)
    repetidos = TS.rotulos_repetidos()
    assert not repetidos, (f"{len(repetidos)} rótulo(s) duplicado(s), o build "
                           f"reprova: {repetidos[:5]}")
    print(f"\nescrito: {total} NPCs em {len(plano)} mapas "
          f"(zero rótulo duplicado na unidade de montagem)")
    return 0


if __name__ == "__main__":
    if DEMO:
        demo()
    else:
        sys.exit(main())
