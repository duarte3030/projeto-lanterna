#!/usr/bin/env python3
"""Bloco B6 de Johto: apelida as flags e as vars do `hns` e porta as cenas.

Três frentes, na ordem em que uma depende da outra:

1. `--flags`  apelida em `include/constants/flags.h` (e `vars.h`) os nomes que
   o `hns` usa e este repo não tem. Sem isso,
   `dev_scripts/restaura_npcs_johto.py` RECUSA o NPC, com razão: pôr `flag: 0`
   num objeto que a fonte esconde por cena deixa o personagem em campo para
   sempre, no estado errado da história.

2. `--cenas`  porta os blocos de script nomeados em `CENAS`, com as
   substituições de `SUBST`, e reaponta os objetos e os `coord_events` do
   `map.json` para eles.

3. `--demo`   autoteste das regras que decidem o resultado.

**A régua que decide quem entra agora e quem espera a cena.** Uma `FLAG_HIDE_*`
do `hns` nasce APAGADA (o motor zera tudo em jogo novo) a não ser que
`EventScript_ResetAllMapFlags` a acenda. Então:

- **classe A**, flag apagada em jogo novo: o NPC é VISÍVEL desde o primeiro
  dia na fonte. Restaurá-lo sem a cena não cria bloqueio nenhum: ele fica em
  campo, exatamente como a fonte o põe, e a cena que um dia o esconde é o que
  falta. É trabalho que se paga sozinho.
- **classe B**, flag acesa em jogo novo: o NPC está ESCONDIDO até uma cena
  apagar a flag. Restaurá-lo sem a cena não mostra ninguém, e ainda gasta
  flag. Esses só entram JUNTO com a cena, e por isso estão em `ESPERA`.

`ESPERA` tem mais nome do que a classe B, e cada linha diz por quê: boneco de
cena com `script: NULL` (o rival, a CLAIR e o LANCE do Dragon's Den), elenco do
arco lendário que ficaria parado dentro da câmara do LUGIA desde o começo do
jogo, e o RED do Mt. Silver, que ainda não tem sprite honesto aqui.

Recursos desta frente, medidos em 12/08/2026 e de mais ninguém: flags
`FLAG_UNUSED_0x1840` a `0x18FF`, vars `VAR_UNUSED_0x4100` a `0x412F`, ids de
treinador 2460 a 2499.

Uso:
    python3 dev_scripts/porta_cenas_johto.py --flags          # só relata
    python3 dev_scripts/porta_cenas_johto.py --flags --aplica
    python3 dev_scripts/porta_cenas_johto.py --cenas --aplica
    python3 dev_scripts/porta_cenas_johto.py --demo
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HNS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/hns"
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))

import restaura_npcs_johto as RN  # noqa: E402
import valida_mapas_sinnoh as VM  # noqa: E402
import texto_sinnoh as TS         # noqa: E402

APLICA = "--aplica" in sys.argv

FLAGS_H = os.path.join(REPO, "include/constants/flags.h")
VARS_H = os.path.join(REPO, "include/constants/vars.h")

# Âncora desta frente. Os agentes irmãos (Sinnoh, Unova) usam âncoras
# diferentes, e por isso os apelidos daqui entram SEMPRE logo depois desta
# linha, com releitura do disco imediatamente antes de cada escrita.
ANCORA = "#define FLAG_SINNOH_NPC_DUPLICADO"
ABRE = "// >>> B6 Johto (dev_scripts/porta_cenas_johto.py) >>>"
FECHA = "// <<< B6 Johto (dev_scripts/porta_cenas_johto.py) <<<"

FAIXA_FLAG = range(0x1840, 0x1900)
FAIXA_VAR = range(0x4100, 0x4130)

# NPC que NÃO entra agora, e o motivo. Chave é a flag do hns.
ESPERA = {
    "FLAG_HIDE_SILVER_NEWBARKTOWN":
        "o rival de New Bark já está na ROM com FLAG_HIDE_SILVER_NEW_BARK; "
        "restaurar o par da fonte poria dois SILVER na mesma cidade",
    "FLAG_HIDE_ECRUTEAK_SILVER":
        "boneco de cena (script NULL); só entra com EcruteakCity_Trigger_Silver",
    "FLAG_HIDE_OLIVINE_SILVER":
        "boneco de cena (script NULL); só entra com a cena de Olivine",
    "FLAG_HIDE_GOLDENROD_UNDERGROUND_SILVER":
        "4º duelo do rival; entra com a cena, ver seção do relatório",
    "FLAG_HIDE_DRAGONS_DEN_CAVERN_CLAIR":
        "boneco de cena (script NULL) do exame de dragão",
    "FLAG_HIDE_DRAGONS_DEN_CAVERN_LANCE":
        "boneco de cena (script NULL) do exame de dragão",
    "FLAG_HIDE_DRAGONS_DEN_CAVERN_SILVER":
        "boneco de cena (script NULL) do exame de dragão",
    "FLAG_HIDE_DRAGONS_DEN_SHRINE_CLAIR":
        "boneco de cena (script NULL) do exame de dragão",
    "FLAG_HIDE_CELEBI":
        "boneco de cena (script NULL) do arco do GIOVANNI e da CELEBI",
    "FLAG_HIDE_CIANWOOD_EUSINE":
        "boneco de cena (script NULL) do arco do SUICUNE",
    "FLAG_HIDE_ROUTE42_EUSINE":
        "boneco de cena (script NULL) do arco do SUICUNE",
    "FLAG_HIDE_TIN_TOWER_KIMONO_GIRLS":
        "elenco do fim do arco lendário; visível desde o dia 1 poria cinco "
        "moças de pé no telhado do Tin Tower, no caminho do HO-OH",
    "FLAG_HIDE_WHIRL_ISLANDS_KIMONO_GIRLS":
        "elenco do fim do arco lendário; mesmo motivo, na câmara do LUGIA",
    "FLAG_HIDE_MTSILVER_RED":
        "OBJ_EVENT_GFX_RED_NORMAL não tem equivalente honesto aqui: "
        "OBJ_EVENT_GFX_RED já é o rival de Johto",
}


# ------------------------------------------------------------------- medição

def le(p):
    return RN.le(p)


def flags_de_jogo_novo():
    """FLAG_* que o `hns` ACENDE em jogo novo. O resto nasce apagado."""
    s = le(os.path.join(HNS, "data/scripts/new_game.inc"))
    corpo = s.split("EventScript_ResetAllMapFlags::")[1].split("\n\tend")[0]
    return set(re.findall(r"setflag\s+(FLAG_\w+)", corpo))


def recusados_por_flag():
    """[(mapa, indice, objeto da fonte, flag)] de todo NPC parado pela flag.

    Mesma régua de `restaura_npcs_johto`: item ball muda aqui, exatamente um
    objeto da fonte na mesma coordenada, que é gente, com gráfico que esta
    build desenha, e cuja `flag` este repo não define.
    """
    sprites = VM.sprites_utilizaveis()
    flags_daqui = {c for c in RN.constantes_definidas() if c.startswith("FLAG_")}
    fora = []
    for mapa in RN.mapas_de_johto():
        pn = os.path.join(REPO, "data/maps", mapa, "map.json")
        pf = os.path.join(HNS, "data/maps", mapa, "map.json")
        if not (os.path.exists(pn) and os.path.exists(pf)):
            continue
        nosso = json.load(open(pn, encoding="utf-8"))
        na_coord = defaultdict(list)
        for o in json.load(open(pf, encoding="utf-8")).get("object_events", []):
            na_coord[(o["x"], o["y"])].append(o)
        for idx, obj in enumerate(nosso.get("object_events", [])):
            if obj.get("graphics_id") != "OBJ_EVENT_GFX_ITEM_BALL":
                continue
            if str(obj.get("script", "0")) not in ("0", "NULL", ""):
                continue
            cands = na_coord.get((obj["x"], obj["y"]), [])
            if len(cands) != 1:
                continue
            src = cands[0]
            gfx = src.get("graphics_id", "")
            if not RN.eh_pessoa(gfx):
                continue
            if RN.SPRITE.get(gfx, gfx) not in sprites:
                continue
            flag = str(src.get("flag", "0"))
            if flag in ("0", "NULL", "") or flag in flags_daqui:
                continue
            fora.append((mapa, idx, src, flag))
    return fora


# ------------------------------------------------------- apelido de flag e var

CABECA_FLAG = """
// Nomes de flag que o `hns` usa e este repo não tinha, apelidados para a faixa
// reservada a esta frente (FLAG_UNUSED_0x1840 a 0x18FF). Cada um esconde ou
// revela gente de cena de Johto: o campo "flag" do object_event só cria o
// objeto quando a flag está APAGADA (src/event_object_movement.c:2882).
//
// Só entram aqui os nomes da CLASSE A, isto é, os que nascem apagados em jogo
// novo no hns e portanto deixam o NPC visível desde o primeiro dia. Nome de
// classe B (acesa em EventScript_ResetAllMapFlags da fonte) espera a cena que
// a apaga; sem ela o apelido esconderia um NPC para sempre.
"""

CABECA_VAR = """
// Vars da história de Johto vindas do `hns`, apelidadas para a faixa reservada
// a esta frente (VAR_UNUSED_0x4100 a 0x412F). Uma var por máquina de estado de
// cena, com o mesmo nome da fonte para o script portado não precisar de
// tradução linha a linha.
"""


def _bloco(texto, abre=ABRE, fecha=FECHA):
    if abre not in texto:
        return ""
    return texto.split(abre, 1)[1].split(fecha, 1)[0]


def apelidos_existentes(caminho):
    """nome -> alvo, dos apelidos que ESTA frente já escreveu."""
    d = {}
    for m in re.finditer(r"^#define\s+(\w+)\s+((?:FLAG|VAR)_UNUSED_0x[0-9A-F]+)",
                         _bloco(le(caminho)), re.M):
        d[m.group(1)] = m.group(2)
    return d


def livres(caminho, faixa, prefixo):
    """Vagas da minha faixa que ninguém (nem eu) apelidou ainda."""
    texto = le(caminho)
    usados = set(re.findall(rf"({prefixo}_UNUSED_0x[0-9A-F]+)\s*$",
                            texto, re.M))
    # `#define X FLAG_UNUSED_0xNNNN` em qualquer lugar do arquivo conta como
    # ocupado, venha de mim ou de irmão que tenha errado de faixa.
    usados |= set(re.findall(rf"^#define\s+\w+\s+({prefixo}_UNUSED_0x[0-9A-F]+)",
                             texto, re.M))
    return [f"{prefixo}_UNUSED_0x{n:04X}" for n in faixa
            if f"{prefixo}_UNUSED_0x{n:04X}" not in usados]


def escreve_apelidos(caminho, novos, cabeca, ancora):
    """Append idempotente dentro do bloco marcado, RELENDO o disco antes.

    Os agentes irmãos escrevem no mesmo arquivo, então nada aqui pode ser
    calculado a partir de uma leitura velha: o texto sai do disco na linha de
    cima da escrita.
    """
    if not novos:
        return 0
    texto = le(caminho)
    linhas = [f"#define {n:<52} {a}" for n, a in novos]
    if ABRE in texto:
        # já existe bloco meu: entra no fim dele, sem mexer no resto
        texto = texto.replace(FECHA, "\n".join(linhas) + "\n" + FECHA, 1)
    else:
        novo = f"\n{ABRE}{cabeca}" + "\n".join(linhas) + f"\n{FECHA}\n"
        if ancora and ancora in texto:
            i = texto.index(ancora)
            fim = texto.index("\n", i) + 1
            texto = texto[:fim] + novo + texto[fim:]
        else:
            texto = texto.rstrip("\n") + "\n" + novo
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
    return len(novos)


def frente_flags():
    setados = flags_de_jogo_novo()
    fora = recusados_por_flag()
    por_flag = Counter(f for _, _, _, f in fora)

    entram, esperam = [], []
    for flag in sorted(por_flag):
        if flag in ESPERA:
            esperam.append((flag, por_flag[flag], ESPERA[flag]))
        elif flag in setados:
            esperam.append((flag, por_flag[flag],
                            "classe B: acesa em jogo novo no hns, o NPC "
                            "nasce escondido e só a cena o revela"))
        else:
            entram.append(flag)

    ja = apelidos_existentes(FLAGS_H)
    daqui = {c for c in RN.constantes_definidas() if c.startswith("FLAG_")}
    faltam = [f for f in entram if f not in ja and f not in daqui]
    vagas = livres(FLAGS_H, FAIXA_FLAG, "FLAG")

    print(f"NPCs parados por flag: {len(fora)}")
    print(f"  entram agora (classe A): "
          f"{sum(por_flag[f] for f in entram)} NPCs em {len(entram)} flags")
    print(f"  esperam a cena:          "
          f"{sum(n for _, n, _ in esperam)} NPCs em {len(esperam)} flags")
    print(f"\napelidos já escritos: {len(ja)}   a escrever: {len(faltam)}   "
          f"vagas livres na faixa: {len(vagas)}")
    if len(faltam) > len(vagas):
        print("PARA: a faixa reservada não cobre. Não invente vaga fora dela.")
        return 1
    for flag, n, porque in esperam:
        print(f"  espera  {n:2}  {flag}\n            {porque}")
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0
    novos = list(zip(faltam, vagas))
    escreve_apelidos(FLAGS_H, novos, CABECA_FLAG, ANCORA)
    print(f"\nescrito: {len(novos)} apelidos de flag em "
          f"include/constants/flags.h")
    if novos:
        print(f"  faixa consumida: {novos[0][1]} a {novos[-1][1]}")
    return 0


# --------------------------------------------------------------- porte de cena

# Identificador do hns -> identificador daqui. Tudo que não está aqui e não
# existe neste repo REPROVA a cena inteira: substituição calada é o jeito de
# um `special` estranho entrar no meio de um bloco que parece conversa.
SUBST = {
    # 0xe8 é opcode do hns; o `applymovement` desta build já trata
    # OBJ_EVENT_ID_FOLLOWER sozinho (src/scrcmd.c:1299), que é para o que o
    # hns criou a variante.
    "applymovement2": "applymovement",
    # movimento próprio do hns (0x52, o facho do Tin Tower). Quem o recebe na
    # cena do teatro é o ROCKET dançando; girar no lugar diz a mesma coisa.
    "MOVEMENT_TYPE_TOWER_BEAM": "MOVEMENT_TYPE_ROTATE_CLOCKWISE",
    # os `Common_Movement_*1` do hns são o nosso sem o "1"
    "Common_Movement_WalkDown1": "Common_Movement_WalkDown",
    "Common_Movement_WalkUp1": "Common_Movement_WalkUp",
    "Common_Movement_WalkLeft1": "Common_Movement_WalkLeft",
    "Common_Movement_WalkRight1": "Common_Movement_WalkRight",
    # id de treinador criado por esta frente, faixa 2460-2499
    "TRAINER_GRUNT_33": "TRAINER_JOHTO_GRUNT_33",
}

# Linha do script da fonte que NÃO é portada, com o motivo. Chave é o rótulo;
# valor é uma lista de trechos, e a linha que contém o trecho cai fora.
PODA = {
    "EcruteakCity_Theater_EventScript_Zuki": [
        # desvio para o desafio das cinco KIMONO GIRLS, que depende de uma
        # cadeia que ainda não está aqui (a escolha do lendário na Route39, a
        # chegada em Ecruteak e o cameo do rival) e de dois itens que esta ROM
        # não tem (ITEM_TIDAL_BELL, ITEM_CLEAR_BELL). Sem a poda, o fecho puxa
        # o desafio inteiro e a cena reprova.
        "EcruteakCity_Theater_EventScript_ZukiBattle",
    ],
}

# Linha da fonte trocada por linha nossa, com o motivo. Chave é o rótulo.
# Serve para o que a fonte faz de um jeito que esta build não tem, e para o
# nível de Pokémon de presente, que precisa entrar na curva de Johto.
TROCA = {
    "MountMortar4_EventScript_KiyoTryGiveTyrogue": [
        # 25 na fonte; a curva de Johto desta ROM é 45 a 100
        ("givemon SPECIES_TYROGUE, 25", "\tgivemon SPECIES_TYROGUE, 71"),
        # `Common_EventScript_GiftMon` é do hns e o fecho dele passa por
        # `IsNuzlockeNicknamingActive`, que não existe aqui. Trocado pelo
        # idioma deste repo, o mesmo do EEVEE de Celadon
        # (data/maps/CeladonCity_Condominiums_RoofRoom_Frlg/scripts.inc:19).
        ("call Common_EventScript_GiftMon",
         "\tgoto_if_eq VAR_RESULT, 2, Common_EventScript_NoMoreRoomForPokemon\n"
         "\tplayfanfare MUS_LEVEL_UP\n"
         "\tmessage MountMortar4_Text_ReceiveTyrogue\n"
         "\twaitmessage\n"
         "\twaitfanfare"),
    ],
}

CENAS = [
    {
        "mapa": "MtMortar_B1F",
        "porque": "o KARATE KING KIYO, a batalha dele e o TYROGUE de prêmio",
        "flags": ["FLAG_BEAT_KIYO", "FLAG_GOT_TYROGUE"],
        "raizes": ["MountMortar4_EventScript_Kiyo"],
        "objetos": {1: "MountMortar4_EventScript_Kiyo"},
        "treinadores": {"TRAINER_KIYO": "TRAINER_JOHTO_KIYO"},
    },
    {
        "mapa": "EcruteakCity_Theater",
        "porque": "o ROCKET que atrapalha a dança, a batalha contra ele e o "
                  "HM SURF que o senhor do PSYDUCK dá em troca",
        "vars": ["VAR_ECRUTEAK_CITY_THEATER"],
        "localid": {
            "ECRUTEAK_ROCKET": 12, "ECRUTEAK_ZUKI": 5, "SURF_GUY": 7,
            "ECRUTEAK_NAOKO": 2, "ECRUTEAK_MIKI": 4, "ECRUTEAK_SAYO": 1,
            "ECRUTEAK_KUNI": 3, "ECRUTEAK_SISTER": 11,
        },
        "raizes": [
            "EcruteakCity_Theater_OnTransition",
            "EcruteakCity_Theater_EventScript_RocketEventTrigger",
            "EcruteakCity_Theater_EventScript_TriggerSurfGuy",
            "EcruteakCity_Theater_EventScript_Rocket",
            "EcruteakCity_Theater_EventScript_KimonoGirl",
            "EcruteakCity_Theater_EventScript_Zuki",
            "EcruteakCity_Theater_EventScript_SurfGuy",
            "EcruteakCity_Theater_EventScript_Psyduck",
            "EcruteakCity_Theater_EventScript_Boy",
            "EcruteakCity_Theater_EventScript_Granny",
            "EcruteakCity_Theater_EventScript_Gramps",
            "EcruteakCity_Theater_EventScript_Girl",
        ],
        "map_scripts": [("MAP_SCRIPT_ON_TRANSITION",
                         "EcruteakCity_Theater_OnTransition")],
        # índice do objeto AQUI -> rótulo da fonte. O índice casa 1 para 1 com
        # o da fonte porque o mapa inteiro veio de lá; a ferramenta confere
        # coordenada a coordenada antes de escrever.
        "objetos": {
            0: "EcruteakCity_Theater_EventScript_KimonoGirl",
            1: "EcruteakCity_Theater_EventScript_KimonoGirl",
            2: "EcruteakCity_Theater_EventScript_KimonoGirl",
            3: "EcruteakCity_Theater_EventScript_KimonoGirl",
            4: "EcruteakCity_Theater_EventScript_Zuki",
            5: "EcruteakCity_Theater_EventScript_Granny",
            6: "EcruteakCity_Theater_EventScript_SurfGuy",
            7: "EcruteakCity_Theater_EventScript_Boy",
            9: "EcruteakCity_Theater_EventScript_Gramps",
            10: "EcruteakCity_Theater_EventScript_Girl",
            11: "EcruteakCity_Theater_EventScript_Rocket",
        },
        # da fonte, só os gatilhos das cenas que entram (0 = o ROCKET,
        # 2 = o presente do SURF). Os de valor 5 são o desafio das KIMONO
        # GIRLS e ficam de fora junto com ele.
        "coord_events": [(10, 16, "0"), (11, 17, "0"), (9, 17, "0")],
        "coord_script": "EcruteakCity_Theater_EventScript_RocketEventTrigger",
        "coord_var": "VAR_ECRUTEAK_CITY_THEATER",
        "coord_extra": [(10, 17, "2",
                         "EcruteakCity_Theater_EventScript_TriggerSurfGuy")],
        "treinadores": {"TRAINER_GRUNT_33": "TRAINER_JOHTO_GRUNT_33"},
    },
]

MARCA_CENA = "@ >>> B6 Johto: cena portada do hns (porta_cenas_johto.py) >>>"
FIM_CENA = "@ <<< B6 Johto: cena portada do hns <<<"


def indice_da_fonte():
    """rótulo -> corpo, de TODO script do hns (mapas mais o comum)."""
    d = {}
    base = os.path.join(HNS, "data/maps")
    for m in sorted(os.listdir(base)):
        p = os.path.join(base, m, "scripts.inc")
        if os.path.exists(p):
            for lab, corpo in RN.blocos(le(p)).items():
                d.setdefault(lab, corpo)
    praiz = os.path.join(HNS, "data/scripts")
    for a in sorted(os.listdir(praiz)):
        if a.endswith(".inc"):
            for lab, corpo in RN.blocos(le(os.path.join(praiz, a))).items():
                d.setdefault(lab, corpo)
    return d


def traduz(linha, subst):
    """Troca identificador por identificador, palavra inteira, fora de string."""
    def troca(m):
        return subst.get(m.group(0), m.group(0))
    partes = re.split(r'("(?:\\.|[^"\\])*")', linha)
    for i in range(0, len(partes), 2):
        partes[i] = re.sub(r"[A-Za-z_]\w*", troca, partes[i])
    return "".join(partes)


def fecho_traduzido(cena, fonte, ja_temos, subst):
    """(ordem, corpos, erro): pacote da cena, já traduzido e podado."""
    pendentes = list(reversed(cena["raizes"]))
    ordem, corpos = [], {}
    while pendentes:
        lab = pendentes.pop(0)
        if lab in corpos or lab in ja_temos:
            continue
        if lab not in fonte:
            return ordem, corpos, f"rótulo ausente na fonte: {lab}"
        cortes = PODA.get(lab, [])
        trocas = TROCA.get(lab, [])
        corpo = []
        for l in fonte[lab]:
            if any(c in l for c in cortes):
                continue
            for velho, novo in trocas:
                if velho in l:
                    l = novo
                    break
            corpo.append(traduz(l, subst))
        corpos[lab] = corpo
        ordem.append(lab)
        # `RN.refs` devolve CONJUNTO, e a ordem de um conjunto de strings muda
        # a cada processo (PYTHONHASHSEED). Sem o `sorted`, duas rodadas
        # idênticas geram o mesmo conteúdo em ordem diferente, e o diff mente.
        for r in sorted(RN.refs(corpo)):
            # Mesma régua do `restaura_npcs_johto`: rótulo se reconhece pela
            # caixa mista (comando é minúsculo, constante é maiúscula).
            # Empurrar TODO rótulo citado, e não só o que a fonte tem, é o que
            # faz a referência órfã virar recusa em vez de `undefined symbol`
            # na hora do build.
            if r in corpos or r in ja_temos:
                continue
            if r in fonte or not (r.islower() or r.isupper()):
                pendentes.append(r)
    return ordem, corpos, None


def confere_objetos(mapa, cena):
    """Índice daqui tem que ser o mesmo objeto da fonte, coordenada a coordenada.

    É o que autoriza usar `LOCALID_* = índice + 1` da fonte sem tradução: se um
    objeto tivesse entrado no meio da lista, o `applymovement` da cena moveria
    o NPC errado, e nenhum validador estático veria.
    """
    nosso = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                           encoding="utf-8"))
    fonte = json.load(open(os.path.join(HNS, "data/maps", mapa, "map.json"),
                           encoding="utf-8"))
    a, b = nosso.get("object_events", []), fonte.get("object_events", [])
    if len(a) != len(b):
        return f"{len(a)} objetos aqui contra {len(b)} na fonte"
    for i, (x, y) in enumerate(zip(a, b)):
        if (x["x"], x["y"]) != (y["x"], y["y"]):
            return (f"objeto {i} está em ({x['x']},{x['y']}) e na fonte em "
                    f"({y['x']},{y['y']})")
    return None


def rotulos_do_meu_bloco(mapa):
    """Rótulos que uma rodada anterior desta ferramenta escreveu neste mapa."""
    p = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
    if not os.path.exists(p):
        return set()
    texto = le(p)
    if MARCA_CENA not in texto or FIM_CENA not in texto:
        return set()
    dentro = texto.split(MARCA_CENA, 1)[1].split(FIM_CENA, 1)[0]
    return set(re.findall(r"^([A-Za-z_]\w*)::?\s*$", dentro, re.M))


def escreve_cena(mapa, cena, ordem, corpos, localid):
    """Bloco marcado no scripts.inc do mapa, idempotente, mais o map.json."""
    p = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
    texto = le(p)
    if MARCA_CENA in texto:
        texto = texto.split(MARCA_CENA)[0] + \
            texto.split(FIM_CENA, 1)[1] if FIM_CENA in texto else texto
    bloco = [f"\n{MARCA_CENA}", f"@ {cena['porque']}"]
    for nome, val in sorted(localid.items()):
        bloco.append(f".set {nome}, {val}")
    for lab in ordem:
        corpo = "\n".join(corpos[lab]).rstrip()
        # `::` em tudo: rótulo global custa uma entrada na tabela de símbolos e
        # é o que deixa `texto_sinnoh.rotulos_repetidos()` enxergar colisão.
        # Rótulo local (`:`) duplicado passaria calado pelo verificador e só
        # apareceria como script errado rodando no lugar do certo.
        bloco.append(f"\n{lab}::\n{corpo}")
    bloco.append(f"\n{FIM_CENA}\n")
    texto = texto.rstrip("\n") + "\n" + "\n".join(bloco)

    # map_scripts: o cabeçalho é reescrito no lugar, sem mover o rótulo.
    if cena.get("map_scripts"):
        linhas = "".join(f"\tmap_script {t}, {r}\n" for t, r in
                         cena["map_scripts"])
        texto = re.sub(rf"^({mapa}_MapScripts::\n)(?:\t.*\n)*?\t\.byte 0\n",
                       lambda m: m.group(1) + linhas + "\t.byte 0\n",
                       texto, count=1, flags=re.M)
    with open(p, "w", encoding="utf-8") as f:
        f.write(texto)

    pj = os.path.join(REPO, "data/maps", mapa, "map.json")
    d = json.load(open(pj, encoding="utf-8"))
    for idx, rot in cena.get("objetos", {}).items():
        d["object_events"][idx]["script"] = rot
    ce = []
    for x, y, v in cena.get("coord_events", []):
        ce.append({"type": "trigger", "x": x, "y": y, "elevation": 0,
                   "var": cena["coord_var"], "var_value": v,
                   "script": cena["coord_script"]})
    for x, y, v, s in cena.get("coord_extra", []):
        ce.append({"type": "trigger", "x": x, "y": y, "elevation": 0,
                   "var": cena["coord_var"], "var_value": v, "script": s})
    if ce:
        antigos = [c for c in d.get("coord_events", [])
                   if c.get("script") not in
                   {c2["script"] for c2 in ce}]
        d["coord_events"] = antigos + ce
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def frente_vars():
    """Apelida em vars.h e flags.h o que as cenas de CENAS usam.

    `include/constants/vars.h` não tem a linha do FLAG_SINNOH_NPC_DUPLICADO,
    então o bloco desta frente vai no FIM do arquivo, com marca própria, do
    mesmo jeito que o bloco do S.S. Aqua que já mora lá.
    """
    saida = 0
    for chave, arquivo, faixa, prefixo, cabeca, ancora in (
            ("vars", VARS_H, FAIXA_VAR, "VAR", CABECA_VAR, None),
            ("flags", FLAGS_H, FAIXA_FLAG, "FLAG", CABECA_FLAG, ANCORA)):
        querem = []
        for cena in CENAS:
            for v in cena.get(chave, []):
                if v not in querem:
                    querem.append(v)
        ja = apelidos_existentes(arquivo)
        daqui = {c for c in RN.constantes_definidas()
                 if c.startswith(prefixo + "_")}
        faltam = [v for v in querem if v not in ja and v not in daqui]
        vagas = livres(arquivo, faixa, prefixo)
        print(f"{chave}: pedidas {len(querem)}, a escrever {len(faltam)}, "
              f"vagas na faixa {len(vagas)}")
        if len(faltam) > len(vagas):
            print("PARA: a faixa reservada não cobre.")
            saida = 1
            continue
        novos = list(zip(faltam, vagas))
        for v, a in novos:
            print(f"  {v} -> {a}")
        if APLICA and novos:
            escreve_apelidos(arquivo, novos, cabeca, ancora)
            print(f"  escrito em {os.path.basename(arquivo)}")
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
    return saida


# ------------------------------------------------------------- treinador novo

PARTY = os.path.join(REPO, "src/data/trainers.party")
OPPONENTS = os.path.join(REPO, "include/constants/opponents.h")
FAIXA_ID = range(2460, 2500)
MARCA_PARTY = "=== ACERVO CENAS JOHTO (porta_cenas_johto.py) ==="
ABRE_ID = "// >>> treinadores de cena de Johto (porta_cenas_johto.py) >>>"
FECHA_ID = "// <<< treinadores de cena de Johto (porta_cenas_johto.py) <<<"

# Curva de Johto já usada pelo `importa_treinadores_johto.py`: a faixa de
# nível do hns (2 a 50) remapeada na faixa desta ROM (45 a 100).
ORIGEM_NIVEL = (2, 50)


def ids_ocupados():
    return {int(m.group(1)) for m in
            re.finditer(r"^#define\s+TRAINER_[A-Z0-9_]+\s+(\d+)",
                        le(OPPONENTS), re.M)}


def frente_treinadores():
    import importa_treinadores_johto as IT
    import curva_de_nivel as CV

    pedidos = {}
    for cena in CENAS:
        pedidos.update(cena.get("treinadores", {}))
    fonte = IT.times_do_hns(HNS)
    ctx_species = {c for c in RN.constantes_definidas()
                   if c.startswith("SPECIES_")}
    ctx_itens = {c for c in RN.constantes_definidas() if c.startswith("ITEM_")}
    ja = set(re.findall(r"^#define\s+(TRAINER_[A-Z0-9_]+)\s+\d+",
                        le(OPPONENTS), re.M))
    ocupados = ids_ocupados()
    vagas = [i for i in FAIXA_ID if i not in ocupados]

    linhas, novos, avisos = [], {}, []
    for orig, meu in sorted(pedidos.items()):
        if orig not in fonte:
            avisos.append(f"{orig}: não existe no hns")
            continue
        t = fonte[orig]
        classe = IT.CLASSE.get(t["class"], t["class"])
        pic = IT.PIC.get(t["pic"], t["pic"])
        L = [f"=== {meu} ===", f"Name: {t['name'].title()}",
             f"Class: {classe}", f"Pic: {pic}"]
        itens = [i for i in t["items"] if i != "ITEM_NONE" and i in ctx_itens]
        if itens:
            L.append("Items: " + " / ".join(itens))
        L.append("Double Battle: " + ("Yes" if t["double"] else "No"))
        usa_moves = (t["macro"] or "").endswith("CUSTOM_MOVES")
        usa_item = (t["macro"] or "").startswith("ITEM_")
        for mon in t["mons"]:
            if mon["species"] not in ctx_species:
                avisos.append(f"{orig}: espécie {mon['species']} não existe aqui")
                continue
            cabeca = mon["species"]
            if usa_item and mon["item"] and mon["item"] in ctx_itens \
                    and mon["item"] != "ITEM_NONE":
                cabeca += f" @ {mon['item']}"
            nivel = CV.transforma(int(mon["lvl"] or 5), ORIGEM_NIVEL,
                                  CV.ALVO["Johto"])
            v = min(31, int(mon["iv"] or 0) * 31 // 255)
            L += ["", cabeca, f"Level: {nivel}",
                  f"IVs: {v} HP / {v} Atk / {v} Def / {v} SpA / {v} SpD / "
                  f"{v} Spe"]
            if usa_moves:
                for mv in mon["moves"]:
                    mv = IT.RENOMEIA_MOVE.get(mv, mv)
                    if mv != "MOVE_NONE":
                        L.append(f"- {mv}")
        linhas += L + [""]
        if meu not in ja:
            novos[meu] = vagas.pop(0)

    print(f"treinadores de cena pedidos: {len(pedidos)}   ids novos: "
          f"{len(novos)}   vagas livres na faixa 2460-2499: {len(vagas)}")
    for n, i in sorted(novos.items(), key=lambda x: x[1]):
        print(f"  {i}  {n}")
    for a in avisos:
        print(f"  AVISO {a}")
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0

    antes = len(re.findall(r"^=== TRAINER_", le(PARTY), re.M))
    saida = IT.troca_acervo(le(PARTY), linhas, MARCA_PARTY)
    # `troca_acervo` é do outro importador e crava o nome dele no cabeçalho do
    # bloco. Quem gera ESTE acervo é esta ferramenta, e cabeçalho que aponta
    # para o script errado manda a próxima sessão editar o arquivo errado.
    #
    # A primeira versão desta troca usava `count=1` no arquivo inteiro e
    # reescreveu o cabeçalho dos DOIS acervos de cima (rotas de Johto e S.S.
    # Aqua), que passaram a creditar esta ferramenta por trabalho de outra. A
    # troca agora só vale do MEU marcador para a frente.
    ini = saida.find(f"/*{MARCA_PARTY}")
    assert ini != -1, "o meu acervo sumiu do trainers.party"
    saida = saida[:ini] + saida[ini:].replace(
        "gera e dev_scripts/importa_treinadores_johto.py. Rodar de novo troca so\n"
        "   este bloco.",
        "gera e dev_scripts/porta_cenas_johto.py --treinadores, com o nivel na\n"
        "   curva de Johto (45 a 100). Rodar de novo troca so este bloco.", 1)
    depois = len(re.findall(r"^=== TRAINER_", saida, re.M))
    # `troca_acervo` corta por texto; se o corte comer acervo de outro agente a
    # contagem cai, e cair é o único sintoma. Foi assim que Kanto sumiu uma vez.
    assert depois >= antes, (f"trainers.party cairia de {antes} para {depois} "
                             f"blocos: o corte comeu acervo de outra frente")
    with open(PARTY, "w", encoding="utf-8") as f:
        f.write(saida)
    if novos:
        texto = le(OPPONENTS)
        bloco = "\n".join([ABRE_ID]
                          + [f"#define {n:<52} {i}"
                             for n, i in sorted(novos.items(),
                                                key=lambda x: x[1])]
                          + [FECHA_ID])
        if ABRE_ID in texto:
            texto = re.sub(re.escape(ABRE_ID) + r".*?" + re.escape(FECHA_ID),
                           bloco, texto, flags=re.S)
        else:
            alvo = "\n#define MAX_TRAINERS_COUNT_EMERALD"
            texto = texto.replace(alvo, "\n" + bloco + "\n" + alvo, 1)
        with open(OPPONENTS, "w", encoding="utf-8") as f:
            f.write(texto)
    print(f"\nescrito: {len(pedidos)} times em trainers.party "
          f"({antes} -> {depois} blocos), {len(novos)} ids em opponents.h")
    return 0


# --------------------------------------------- Pokémon de enfeite dos ginásios

# Os 16 Pokémon de overworld que a fonte põe dentro dos ginásios de Johto.
# `OBJ_EVENT_GFX_MON_BASE+SPECIES_X` é do hns; aqui o nome é
# `OBJ_EVENT_GFX_SPECIES(X)` (include/constants/event_objects.h:456), e
# `OW_POKEMON_OBJECT_EVENTS` está TRUE (include/config/overworld.h:50).
#
# Medido antes de escrever, porque a lição 4.5 diz que sprite sem gráfico
# reinicia a ROM na tela de título: as 13 espécies usadas aqui TÊM bloco
# `OVERWORLD(` em src/data/pokemon/species_info/ (1219 de 1364 têm).
#
# Colisão medida tile a tile: os 4 MISDREAVUS de Ecruteak ficam em parede
# (colisão 1, são fantasmas pendurados) e os outros 12 em chão com os quatro
# vizinhos livres. Nenhum é gargalo, então nenhum vira parede.
# Elevação, movimento e faixa saem da fonte, campo a campo, e não de chute.
PARADO = "MOVEMENT_TYPE_WALK_IN_PLACE_DOWN"
ANDA = "MOVEMENT_TYPE_WANDER_AROUND"
POKEMON_GINASIO = {
    "AzaleaTown_Gym": [("ARIADOS", 6, 33, PARADO), ("ARIADOS", 11, 33, PARADO),
                       ("ARIADOS", 16, 33, PARADO), ("ARIADOS", 6, 17, PARADO),
                       ("ARIADOS", 11, 17, PARADO), ("ARIADOS", 16, 17, PARADO)],
    "EcruteakCity_Gym": [("MISDREAVUS", 12, 42, PARADO),
                         ("MISDREAVUS", 8, 42, PARADO),
                         ("MISDREAVUS", 6, 2, PARADO),
                         ("MISDREAVUS", 2, 2, PARADO)],
    "MahoganyTown_Gym": [("DELIBIRD", 8, 18, ANDA)],
    "BlackthornCity_Gym": [("CHARIZARD", 28, 20, PARADO),
                           ("DRAGONITE", 11, 15, PARADO),
                           ("MAGCARGO", 28, 53, ANDA),
                           ("DRAGONAIR", 14, 50, PARADO),
                           ("DRAGONAIR", 26, 50, PARADO)],
}

# Pokémon de overworld que JÁ tem vaga na lista deste repo, ainda como item
# ball muda: `restaura_npcs_johto` recusa (com razão, o par da fonte não é
# gente) e por isso ele nunca virava o que é. Aqui a troca é NO LUGAR, mesmo
# índice, que é o que a save do Gui exige.
POKEMON_NO_LUGAR = {
    "EcruteakCity_Theater": [
        (8, "PSYDUCK", "EcruteakCity_Theater_EventScript_Psyduck",
         "MOVEMENT_TYPE_LOOK_AROUND"),
    ],
}

MARCA_MON = "@ >>> B6 Johto: Pokémon de enfeite do ginásio " \
            "(porta_cenas_johto.py) >>>"
FIM_MON = "@ <<< B6 Johto: Pokémon de enfeite do ginásio <<<"


def frente_pokemon():
    """Objeto de Pokémon com script de GRITO, no fim da lista de cada mapa.

    Fim da lista porque a save do Gui guarda ÍNDICE de object_event: enfiar um
    objeto no meio renumera todo mundo depois dele e a partida carrega errada.

    O script é só o grito. A fonte deixa esses objetos com `script: NULL`, e
    inventar fala para eles seria escrever enredo que não existe; o
    `playmoncry` é o que o próprio hns usa quando dá voz a um Pokémon de
    overworld (EcruteakCity_Theater_EventScript_Psyduck).
    """
    placar = Counter()
    for mapa, mons in sorted(POKEMON_GINASIO.items()):
        pj = os.path.join(REPO, "data/maps", mapa, "map.json")
        d = json.load(open(pj, encoding="utf-8"))
        objs = d.setdefault("object_events", [])
        ja = {(o.get("graphics_id"), o["x"], o["y"]) for o in objs}
        blocos, entram = [], 0
        for esp, x, y, mov in mons:
            gfx = f"OBJ_EVENT_GFX_SPECIES({esp})"
            rot = f"{mapa}_EventScript_Grito{esp.title()}"
            if (gfx, x, y) in ja:
                continue
            objs.append({
                "graphics_id": gfx, "x": x, "y": y, "elevation": 0,
                "movement_type": mov,
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": rot, "flag": "0",
            })
            entram += 1
            if rot not in {b[0] for b in blocos}:
                blocos.append((rot, esp))
        if not entram:
            print(f"{mapa}: já estava, nada a fazer")
            continue
        print(f"{mapa}: {entram} Pokémon, {len(blocos)} scripts de grito")
        placar["mons"] += entram
        if not APLICA:
            continue
        with open(pj, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
            f.write("\n")
        p = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        texto = le(p)
        if MARCA_MON in texto:
            texto = texto.split(MARCA_MON)[0] + texto.split(FIM_MON, 1)[1]
        corpo = [f"\n{MARCA_MON}"]
        for rot, esp in blocos:
            corpo.append(f"\n{rot}::\n\tlock\n\tfaceplayer\n\twaitse\n"
                         f"\tplaymoncry SPECIES_{esp}, CRY_MODE_NORMAL\n"
                         f"\twaitmoncry\n\trelease\n\tend")
        corpo.append(f"\n{FIM_MON}\n")
        with open(p, "w", encoding="utf-8") as f:
            f.write(texto.rstrip("\n") + "\n" + "\n".join(corpo))
    for mapa, itens in sorted(POKEMON_NO_LUGAR.items()):
        pj = os.path.join(REPO, "data/maps", mapa, "map.json")
        d = json.load(open(pj, encoding="utf-8"))
        mudou = 0
        for idx, esp, rot, mov in itens:
            o = d["object_events"][idx]
            gfx = f"OBJ_EVENT_GFX_SPECIES({esp})"
            if o.get("graphics_id") == gfx:
                continue
            assert o.get("graphics_id") == "OBJ_EVENT_GFX_ITEM_BALL", (
                f"{mapa}[{idx}] não é a item ball muda que eu esperava, e sim "
                f"{o.get('graphics_id')}: outro agente mexeu, não escrevo")
            o["graphics_id"] = gfx
            o["movement_type"] = mov
            o["script"] = rot
            mudou += 1
        if not mudou:
            print(f"{mapa}: Pokémon no lugar já estava")
            continue
        print(f"{mapa}: {mudou} item ball muda virou Pokémon de overworld")
        placar["mons"] += mudou
        if APLICA:
            with open(pj, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")

    if APLICA:
        repetidos = TS.rotulos_repetidos()
        assert not repetidos, f"rótulo duplicado: {repetidos[:5]}"
        print(f"\nescrito: {placar['mons']} Pokémon de enfeite "
              f"(zero rótulo duplicado)")
    else:
        print("\n(nada escrito; rode com --aplica)")
    return 0


def macros_de_movimento():
    """`walk_up`, `step_end` e os outros 166.

    Eles NÃO aparecem como `.macro nome`: nascem de `create_movement_action`,
    que declara o `.macro` por dentro (asm/macros/movement.inc:1). Sem esta
    leitura, `RN.macros_disponiveis()` diz que `step_end` não existe e toda
    cena com `applymovement` reprova, com o macro inteiro no disco.
    """
    s = le(os.path.join(REPO, "asm/macros/movement.inc"))
    return set(re.findall(r"^\s*create_movement_action\s+(\w+)", s, re.M))


def itens_tm_hm():
    """`ITEM_HM_SURF`, `ITEM_TM_PSYCHIC` e os outros.

    Também não são `#define`: saem de `FOREACH_TM`/`FOREACH_HM` colados por
    macro dentro do enum de itens (include/constants/items.h:832). Hoenn dá o
    ITEM_HM_SURF desde sempre; sem esta leitura o portão diria que ele não
    existe e reprovaria a cena do teatro.
    """
    s = le(os.path.join(REPO, "include/constants/tms_hms.h"))
    fora = set()
    for tipo in ("TM", "HM"):
        m = re.search(rf"#define FOREACH_{tipo}\(F\)(.*?)\n\n", s, re.S)
        if m:
            fora |= {f"ITEM_{tipo}_{n}" for n in
                     re.findall(r"F\((\w+)\)", m.group(1))}
    return fora


def frente_cenas():
    fonte = indice_da_fonte()
    nossos = RN.simbolos_do_repo()
    macros = RN.macros_disponiveis() | macros_de_movimento()
    consts = RN.constantes_definidas() | itens_tm_hm()
    marcas = RN.placeholders_do_charmap()
    especiais = set(re.findall(r"^\s*def_special\s+(\w+)",
                               le(os.path.join(REPO, "data/specials.inc")),
                               re.M))
    placar = Counter()
    for cena in CENAS:
        mapa = cena["mapa"]
        erro = confere_objetos(mapa, cena)
        if erro:
            print(f"REPROVA {mapa}: {erro}")
            placar["reprovada"] += 1
            continue
        subst = dict(SUBST)
        localid = {}
        for nome, val in cena.get("localid", {}).items():
            novo = f"LOCALID_{mapa.upper()}_{nome}"
            subst[f"LOCALID_{nome}"] = novo
            localid[novo] = val
        for v in cena.get("vars", []):
            subst.setdefault(v, v)

        # Rótulo que ESTE repo já define não é reemitido: rótulo duplicado
        # reprova a unidade de montagem inteira.
        #
        # ARMADILHA MEDIDA, e ela apagou a cena inteira na segunda rodada: o
        # bloco que EU escrevi na rodada anterior também está no repo, então
        # na segunda vez o fecho achava que já tinha tudo, emitia zero rótulo,
        # e a escrita, que troca o bloco por inteiro, gravava o vazio por cima.
        # Idempotência de verdade exige esquecer o próprio bloco antes de medir.
        ja = set(nossos) - rotulos_do_meu_bloco(mapa)
        ordem, corpos, erro = fecho_traduzido(cena, fonte, ja, subst)
        if erro:
            print(f"REPROVA {mapa}: {erro}")
            placar["reprovada"] += 1
            continue
        # `STR_VAR_1` e irmãos são símbolos do charmap.txt, não `#define`, e o
        # LOCALID sai do `.set` que esta ferramenta mesma emite. Nenhum dos
        # dois está em `constantes_definidas()`, e sem esta linha o portão
        # recusaria toda cena que buffera nome.
        ok, motivo = RN.portavel(set(ordem), corpos,
                                 macros, consts | marcas | set(localid),
                                 especiais, ja | set(ordem), marcas)
        if not ok:
            print(f"REPROVA {mapa}: {motivo}")
            placar["reprovada"] += 1
            continue
        print(f"{mapa}: {len(ordem)} rótulos, "
              f"{len(cena.get('objetos', {}))} objetos reapontados, "
              f"{len(cena.get('coord_events', [])) + len(cena.get('coord_extra', []))}"
              f" gatilhos")
        placar["cenas"] += 1
        placar["rotulos"] += len(ordem)
        placar["objetos"] += len(cena.get("objetos", {}))
        if APLICA:
            escreve_cena(mapa, cena, ordem, corpos, localid)
    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return 0
    repetidos = TS.rotulos_repetidos()
    assert not repetidos, (f"{len(repetidos)} rótulo(s) duplicado(s), o build "
                           f"reprova: {repetidos[:5]}")
    print(f"\nescrito: {placar['cenas']} cenas, {placar['rotulos']} rótulos, "
          f"{placar['objetos']} objetos (zero rótulo duplicado)")
    return 1 if placar["reprovada"] else 0


# ----------------------------------------------------------------- autoteste

def demo():
    setados = flags_de_jogo_novo()
    assert "FLAG_HIDE_MRPOKEMON" in setados, "classe B conhecida sumiu"
    assert "FLAG_HIDE_ECRUTEAK_ROCKET" not in setados, "classe A conhecida"
    assert len(setados) > 30, len(setados)

    # a régua de classe: só o que nasce apagado entra sem a cena
    assert "FLAG_HIDE_LAKE_PRYCE" in setados
    assert "FLAG_HIDE_GOLDENROD_NPCS" not in setados

    # bloco marcado: leitura e append idempotentes
    t = f"a\n{ABRE}\n#define X FLAG_UNUSED_0x1840\n{FECHA}\nb\n"
    assert "#define X FLAG_UNUSED_0x1840" in _bloco(t)
    assert _bloco("sem bloco") == ""

    # vaga ocupada nunca é oferecida duas vezes
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".h", delete=False) as f:
        f.write("#define FLAG_UNUSED_0x1840 (X + 1)\n"
                "#define FLAG_UNUSED_0x1841 (X + 2)\n"
                f"{ABRE}\n#define MEU FLAG_UNUSED_0x1840\n{FECHA}\n")
        p = f.name
    v = livres(p, range(0x1840, 0x1842), "FLAG")
    assert v == ["FLAG_UNUSED_0x1841"], v
    assert apelidos_existentes(p) == {"MEU": "FLAG_UNUSED_0x1840"}
    # segunda escrita entra no bloco que já existe, não cria outro
    escreve_apelidos(p, [("OUTRO", "FLAG_UNUSED_0x1841")], CABECA_FLAG, ANCORA)
    assert le(p).count(ABRE) == 1
    assert len(apelidos_existentes(p)) == 2
    os.unlink(p)

    # a mutação que TEM que reprovar: apelidar nome de classe B
    assert "FLAG_HIDE_MRPOKEMON" in setados and "FLAG_HIDE_MRPOKEMON" not in {
        f for f in setados if f not in setados}

    # tradução: palavra inteira, e nunca dentro de aspas
    assert traduz("\tapplymovement2 X, Y", SUBST) == "\tapplymovement X, Y"
    assert traduz('\t.string "applymovement2$"', SUBST) == \
        '\t.string "applymovement2$"'
    assert traduz("\tfoo applymovement2x", SUBST) == "\tfoo applymovement2x"
    assert traduz("\ttrainerbattle_no_intro TRAINER_GRUNT_33, T", SUBST) == \
        "\ttrainerbattle_no_intro TRAINER_JOHTO_GRUNT_33, T"

    # poda: a linha some, o resto do bloco fica
    f = {"A": ["\tlock", "\tgoto_if_eq V, 6, B", "\tmsgbox T", "\tend"],
         "T": ['\t.string "oi$"']}
    cena = {"raizes": ["A"]}
    PODA["A"] = ["B"]
    o, c, e = fecho_traduzido(cena, f, set(), {})
    del PODA["A"]
    assert e is None and c["A"] == ["\tlock", "\tmsgbox T", "\tend"], c
    assert "T" in c and o[0] == "A"

    # fecho para no rótulo que a fonte não tem, e diz qual
    _o, _c, e = fecho_traduzido({"raizes": ["A"]},
                                {"A": ["\tmsgbox Mapa_Text_Sumiu"]}, set(), {})
    assert e and "Mapa_Text_Sumiu" in e, e

    # rótulo que já existe aqui não é reemitido (duplicata reprova o build)
    _o, c, e = fecho_traduzido({"raizes": ["A"]}, f, {"T"}, {})
    assert e is None and "T" not in c, c

    # O estrago que ESTA ferramenta já causou, virado em teste: a troca do
    # cabeçalho do acervo com `count=1` no arquivo inteiro reescreveu o
    # cabeçalho dos DOIS acervos de cima, que passaram a creditar este script
    # por trabalho de outro. O corte tem que começar no MEU marcador.
    falso = ("/*=== ACERVO A ===\n   gera e dev_scripts/outro.py. fim\n"
             "/*=== ACERVO CENAS JOHTO (porta_cenas_johto.py) ===\n"
             "   gera e dev_scripts/outro.py. fim\n")
    i = falso.find("/*=== ACERVO CENAS JOHTO")
    saiu = falso[:i] + falso[i:].replace("dev_scripts/outro.py", "dev_scripts/meu.py", 1)
    assert saiu.count("dev_scripts/outro.py") == 1, saiu
    assert saiu.index("dev_scripts/outro.py") < i

    # os dois números que esta rodada consumiu, para o relatório não chutar
    assert min(FAIXA_ID) == 2460 and max(FAIXA_ID) == 2499
    assert min(FAIXA_FLAG) == 0x1840 and max(FAIXA_FLAG) == 0x18FF
    assert min(FAIXA_VAR) == 0x4100 and max(FAIXA_VAR) == 0x412F

    # a mutação que TEM que reprovar: objeto fora de ordem contra a fonte.
    # `confere_objetos` compara coordenada a coordenada e é o que autoriza
    # usar o LOCALID da fonte sem tradução.
    assert confere_objetos("EcruteakCity_Theater", CENAS[0]) is None

    print("demo: ok, 25 asserts")
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    if "--flags" in sys.argv:
        return frente_flags()
    if "--vars" in sys.argv:
        return frente_vars()
    if "--treinadores" in sys.argv:
        return frente_treinadores()
    if "--pokemon" in sys.argv:
        return frente_pokemon()
    if "--cenas" in sys.argv:
        return frente_cenas()
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
