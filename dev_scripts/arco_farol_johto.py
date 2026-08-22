#!/usr/bin/env python3
"""O arco do farol de Olivine: a AMPHY doente, a Secret Potion e a JASMINE.

Fecha a pendência mais antiga de Johto, a que o próprio `scripts.inc` do farol
confessa no cabeçalho desde o porte original:

    "A JASMINE nao tem sprite ... entao a cena da AMPHY doente virou um
     bg_event (sign) sem NPC visivel ... NAO fecha a historia (curar a AMPHY
     com o Secret Potion e liberar a JASMINE no ginasio): ITEM_SECRET_POTION
     nao existe, e o unlock mexe em OlivineCity_Gym, que nao e meu."

Os três bloqueios de então, e o que cada um virou em 22/08/2026:

1. **Sprite.** `OBJ_EVENT_GFX_JASMINE` continua não existindo, e a tabela
   `SPRITE` do `restaura_npcs_johto.py` já dizia o equivalente honesto desde a
   Fase B: `OBJ_EVENT_GFX_WOMAN_1`. Não é escolha nova, é a tabela.
2. **`ITEM_SECRET_POTION`.** Nasce aqui, em APPEND PURO no fim do enum, que é o
   mesmo método já provado com `ITEM_CLEAR_BELL` e `ITEM_TIDAL_BELL`: a bolsa
   guarda `(itemId, quantidade)` e não um bit por item, então id novo no fim não
   mexe em struct nenhuma de save. `guarda_save.py` mede depois.
3. **`OlivineCity_Gym`.** Passou a ser da mesma frente que o farol nesta rodada,
   então o unlock entra.

A MÁQUINA DE ESTADO, E POR QUE ELA NÃO PRECISA DE FLAG DE INÍCIO DE JOGO

O hns guarda o arco em `VAR_OLIVINE_CITY_STATE` e esconde a JASMINE do ginásio
com `FLAG_HIDE_OLIVINE_CITY_GYM_JASMINE`, acesa em cena de cidade. Copiar isso
aqui exigiria acender a flag no começo do jogo, porque flag nasce APAGADA e
objeto com flag apagada nasce VISÍVEL: a JASMINE apareceria no ginásio e no
farol ao mesmo tempo, desde o primeiro minuto.

O remédio é o idioma do gen 3 e não custa gancho de jogo novo: cada um dos dois
mapas ganha um `MAP_SCRIPT_ON_TRANSITION` que DERIVA as duas flags da var, toda
vez que o jogador entra. Estado < 5, a JASMINE está no farol e sumida do
ginásio; estado >= 5, o contrário. Nenhum estado intermediário sobrevive a um
save no meio da cena, e não há ordem de visita que quebre.

Os estados são os do hns, sem renumerar: 3 = ela pediu o remédio, 4 = o remédio
está com o jogador, 5 = a AMPHY está curada e a JASMINE voltou ao ginásio.

O QUE FICA DE FORA, com motivo

- A **tempestade** que o hns põe em `Route40`, `Route41` e `OlivineCity` até o
  estado 5 (`goto_if_ge VAR_OLIVINE_CITY_STATE, 5, ClearWeather`). É clima, não
  enredo, e mexe no campo `weather` de três mapas que já têm o clima deles
  escolhido nesta ROM. Fica na fila.
- Os estados 6, 7 e 8 do hns, que são a insígnia e o pós-ginásio. Aqui a
  insígnia já é `FLAG_INSIGNIA_JOHTO_5`, que o ginásio grava desde o porte
  original, e trocar isso agora quebraria save.

Uso:
    python3 dev_scripts/arco_farol_johto.py            # só relata
    python3 dev_scripts/arco_farol_johto.py --aplica   # escreve
    python3 dev_scripts/arco_farol_johto.py --demo     # autoteste
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))

import restaura_gfx_johto as RG  # noqa: E402  grava_como_estava

APLICA = "--aplica" in sys.argv
DEMO = "--demo" in sys.argv

FLAGS_H = os.path.join(REPO, "include/constants/flags.h")
VARS_H = os.path.join(REPO, "include/constants/vars.h")
ITEMS_H = os.path.join(REPO, "include/constants/items.h")
ITENS_DADOS = os.path.join(REPO, "src/data/items.h")

MARCA = "@ ARCO DO FAROL DE OLIVINE, dev_scripts/arco_farol_johto.py"
MARCA_C = "// ARCO DO FAROL DE OLIVINE (dev_scripts/arco_farol_johto.py)"

# Faixa de transbordo de Johto, declarada na secao 0.a do PENDENCIAS-JOHTO.md.
# Os 0x1D00 a 0x1D0D ja tem dono (Gyarados do Lago da Furia e os 4 do bloco c5
# de Galar); `dev_scripts/flags_livres.py` confirmou 0x1D0E em diante livre.
FLAGS_NOVAS = [
    ("FLAG_HIDE_LIGHTHOUSE_JASMINE",
     "a JASMINE some do alto do farol depois que a AMPHY e curada"),
    ("FLAG_HIDE_OLIVINE_CITY_GYM_JASMINE",
     "a JASMINE so aparece no ginasio DEPOIS de a AMPHY ser curada"),
]
VAR_NOVA = ("VAR_OLIVINE_CITY_STATE",
            "arco do farol: 3 pediu remedio, 4 remedio na mao, 5 AMPHY curada")

ITEM_NOVO = "ITEM_SECRET_POTION"

def localids():
    """(indice da JASMINE, indice da AMPHY) LIDOS do map.json, 1-based.

    Cravar o numero aqui seria a pior classe de erro deste arquivo: o script usa
    `removeobject <id>` e `applymovement <id>`, e id errado nao da erro de
    compilacao, apaga OUTRO boneco em tempo de jogo. Os dois objetos entraram no
    FIM da lista pelo `completa_objetos_johto.py`, entao o indice deles depende
    de quantos objetos o mapa ja tinha.
    """
    d = json.load(open(os.path.join(REPO,
                  "data/maps/OlivineCity_Lighthouse/map.json"),
                  encoding="utf-8"))
    j = a = None
    for i, o in enumerate(d["object_events"], 1):
        if (o["x"], o["y"]) == (156, 9):
            j = i
        if (o["x"], o["y"]) == (156, 8):
            a = i
    if not (j and a):
        raise SystemExit("farol: JASMINE (156,9) ou AMPHY (156,8) sumiu do mapa")
    return j, a


LOCALID_JASMINE, LOCALID_AMPHAROS = localids()


# --------------------------------------------------------------- alocadores

def livre_flag(txt, nome):
    """Apelida a PRIMEIRA FLAG_UNUSED livre a partir de 0x1D0E.

    Reler o arquivo na hora de escrever e nao cravar o numero e obrigacao desta
    casa: ha seis executores em paralelo nesta arvore e a faixa anda.
    """
    if re.search(rf"^#define\s+{nome}\b", txt, re.M):
        return None, txt
    ocupadas = set(re.findall(r"^#define\s+\w+\s+FLAG_UNUSED_0x([0-9A-Fa-f]+)",
                              txt, re.M))
    ocupadas = {int(h, 16) for h in ocupadas}
    for n in range(0x1D0E, 0x2026):
        if n in ocupadas and True:
            continue
        alvo = f"FLAG_UNUSED_0x{n:X}"
        if not re.search(rf"^#define\s+{alvo}\b", txt, re.M):
            continue
        return alvo, txt
    raise SystemExit("faixa de transbordo de Johto sem vaga; pedir faixa nova")


def livre_var(txt, nome):
    if re.search(rf"^#define\s+{nome}\b", txt, re.M):
        return None
    ocupadas = {int(h, 16) for h in
                re.findall(r"^#define\s+\w+\s+VAR_UNUSED_0x([0-9A-Fa-f]+)",
                           txt, re.M)}
    for n in range(0x4110, 0x4200):
        alvo = f"VAR_UNUSED_0x{n:X}"
        if n in ocupadas:
            continue
        if not re.search(rf"^#define\s+{alvo}\b", txt, re.M):
            continue
        return alvo
    raise SystemExit("sem VAR_UNUSED livre na faixa 0x4110+")


# ------------------------------------------------------------------ escrita

def escreve_flags(relato):
    txt = open(FLAGS_H, encoding="utf-8").read()
    linhas = []
    for nome, comentario in FLAGS_NOVAS:
        alvo, txt = livre_flag(txt, nome)
        if alvo is None:
            relato.append(f"flag {nome}: ja existe, nada a fazer")
            continue
        linhas.append(f"#define {nome:44} {alvo}  // {comentario}")
        # marca como ocupada para a proxima da lista nao pegar a mesma
        txt += f"\n#define {nome} {alvo}\n"
        relato.append(f"flag {nome} = {alvo}")
    if not linhas:
        return
    if not APLICA:
        return
    # RELER: outro executor pode ter escrito entre a leitura de cima e agora
    atual = open(FLAGS_H, encoding="utf-8").read()
    bloco = ("\n" + MARCA_C + "\n"
             + "// Apelido de FLAG_UNUSED que ja existe: FLAGS_COUNT nao muda, save intacta.\n"
             + "\n".join(linhas) + "\n")
    with open(FLAGS_H, "w", encoding="utf-8") as f:
        f.write(atual.rstrip("\n") + "\n" + bloco)


def escreve_var(relato):
    txt = open(VARS_H, encoding="utf-8").read()
    alvo = livre_var(txt, VAR_NOVA[0])
    if alvo is None:
        relato.append(f"var {VAR_NOVA[0]}: ja existe, nada a fazer")
        return
    relato.append(f"var {VAR_NOVA[0]} = {alvo}")
    if not APLICA:
        return
    atual = open(VARS_H, encoding="utf-8").read()
    bloco = (f"\n{MARCA_C}\n"
             f"// Apelido de VAR_UNUSED que ja existe: VARS_COUNT nao muda.\n"
             f"#define {VAR_NOVA[0]:38} {alvo}  // {VAR_NOVA[1]}\n")
    with open(VARS_H, "w", encoding="utf-8") as f:
        f.write(atual.rstrip("\n") + "\n" + bloco)


def escreve_item(relato):
    txt = open(ITEMS_H, encoding="utf-8").read()
    if ITEM_NOVO in txt:
        relato.append(f"item {ITEM_NOVO}: ja existe, nada a fazer")
        return
    ids = [int(n) for n in re.findall(r"^\s*ITEM_\w+\s*=\s*(\d+),", txt, re.M)]
    novo = max(ids) + 1
    relato.append(f"item {ITEM_NOVO} = {novo} (append puro, save intacta)")
    if not APLICA:
        return
    alvo = re.search(r"\n(\s*)ITEMS_COUNT,", txt)
    bloco = (f"\n    // Johto, arco do farol de Olivine. APPEND PURO como os dois\n"
             f"    // sinos acima: a bolsa guarda (itemId, quantidade), entao id novo\n"
             f"    // no fim nao mexe em struct de save.\n"
             f"    {ITEM_NOVO} = {novo},\n")
    txt = txt[:alvo.start()] + bloco + txt[alvo.start():]
    with open(ITEMS_H, "w", encoding="utf-8") as f:
        f.write(txt)

    dados = open(ITENS_DADOS, encoding="utf-8").read()
    if ITEM_NOVO in dados:
        return
    ancora = "    [ITEM_TIDAL_BELL] ="
    entrada = (
        "    [ITEM_SECRET_POTION] =\n"
        "    {\n"
        '        .name = ITEM_NAME("SecretPotion"),\n'
        "        .price = 0,\n"
        "        .description = COMPOUND_STRING(\n"
        '            "A wonderful\\n"\n'
        '            "medicine from\\n"\n'
        '            "CIANWOOD CITY."),\n'
        "        .importance = 1,\n"
        "        .pocket = POCKET_KEY_ITEMS,\n"
        "        .type = ITEM_USE_BAG_MENU,\n"
        "        .fieldUseFunc = ItemUseOutOfBattle_CannotUse,\n"
        "        .iconPic = gItemIcon_LargePotion,\n"
        "        .iconPalette = gItemIconPalette_MaxPotion,\n"
        "    },\n\n")
    dados = dados.replace(ancora, entrada + ancora, 1)
    with open(ITENS_DADOS, "w", encoding="utf-8") as f:
        f.write(dados)


# ------------------------------------------------------------------ scripts

FAROL = f"""
{MARCA}
@ A cena inteira do alto do farol. O bilhete que existia aqui era o remendo de
@ quando a JASMINE nao podia entrar como objeto; agora ela entra, e o bilhete
@ some junto com o remendo.
OlivineCity_Lighthouse_OnTransition::
	goto_if_ge VAR_OLIVINE_CITY_STATE, 5, OlivineCity_Lighthouse_JasmineJaFoi
	clearflag FLAG_HIDE_LIGHTHOUSE_JASMINE
	end

OlivineCity_Lighthouse_JasmineJaFoi::
	setflag FLAG_HIDE_LIGHTHOUSE_JASMINE
	end

OlivineLighthouse_EventScript_Jasmine::
	lock
	faceplayer
	goto_if_eq VAR_OLIVINE_CITY_STATE, 3, OlivineLighthouse_EventScript_JasmineGoGetPotion
	goto_if_eq VAR_OLIVINE_CITY_STATE, 4, OlivineLighthouse_EventScript_JasmineDeliverPotion
	msgbox OlivineLighthouse_Text_JasmineCianwoodPharmacy, MSGBOX_DEFAULT
	msgbox OlivineLighthouse_Text_JasmineGetMedicine, MSGBOX_DEFAULT
	closemessage
	setvar VAR_OLIVINE_CITY_STATE, 3
	release
	end

OlivineLighthouse_EventScript_JasmineGoGetPotion::
	msgbox OlivineLighthouse_Text_JasmineGetMedicine2, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineLighthouse_EventScript_JasmineDeliverPotion::
	msgbox OlivineLighthouse_Text_JasmineCureAmphy, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, OlivineLighthouse_EventScript_JasmineRefuse
	playse SE_USE_ITEM
	removeitem ITEM_SECRET_POTION
	msgbox OlivineLighthouse_Text_PlayerHandedSecretpotion, MSGBOX_DEFAULT
	waitse
	msgbox OlivineLighthouse_Text_JasmineDontBeOffended, MSGBOX_DEFAULT
	closemessage
	applymovement {LOCALID_JASMINE}, OlivineLighthouse_Movement_JasmineOlhaAmphy
	waitmovement 0
	msgbox OlivineLighthouse_Text_JasmineAmphyHowFeeling, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_WHITE
	playse SE_M_THUNDERBOLT2
	waitse
	fadescreen FADE_FROM_WHITE
	playmoncry SPECIES_AMPHAROS, CRY_MODE_NORMAL
	msgbox OlivineLighthouse_Text_AmphyPaluPalulu, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	msgbox OlivineLighthouse_Text_JasmineThankYou, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	playse SE_EXIT
	waitse
	delay 50
	setvar VAR_OLIVINE_CITY_STATE, 5
	setflag FLAG_AMPHAROS_HEALED
	setflag FLAG_HIDE_LIGHTHOUSE_JASMINE
	clearflag FLAG_HIDE_OLIVINE_CITY_GYM_JASMINE
	removeobject {LOCALID_JASMINE}
	fadescreen FADE_FROM_BLACK
	release
	end

OlivineLighthouse_EventScript_JasmineRefuse::
	msgbox OlivineLighthouse_Text_JasmineGetMedicine2, MSGBOX_DEFAULT
	closemessage
	release
	end

	.align 2
OlivineLighthouse_Movement_JasmineOlhaAmphy:
	walk_in_place_faster_up
	step_end

OlivineLighthouse_Text_JasmineCianwoodPharmacy:
	.string "JASMINE: …This POKéMON always kept\\n"
	.string "the sea lit at night.\\p"
	.string "…But it suddenly got sick… It's\\n"
	.string "gasping for air…\\p"
	.string "…I understand that there is a\\n"
	.string "wonderful PHARMACY in CIANWOOD…\\p"
	.string "But that's across the sea…\\n"
	.string "And I can't leave AMPHY unattended…$"

OlivineLighthouse_Text_JasmineGetMedicine:
	.string "…May I ask you to get some medicine\\n"
	.string "for me? Please?$"

OlivineLighthouse_Text_JasmineGetMedicine2:
	.string "There is a wonderful PHARMACY\\n"
	.string "in CIANWOOD…\\p"
	.string "But that's across the sea…\\n"
	.string "And I can't leave AMPHY unattended…\\p"
	.string "…May I ask you to get some medicine\\n"
	.string "for me? Please?$"

OlivineLighthouse_Text_JasmineCureAmphy:
	.string "JASMINE: …Will that medicine cure\\n"
	.string "AMPHY?$"

OlivineLighthouse_Text_PlayerHandedSecretpotion:
	.string "{{PLAYER}} handed the SECRETPOTION\\n"
	.string "to JASMINE.$"

OlivineLighthouse_Text_JasmineDontBeOffended:
	.string "JASMINE: …Please don't be offended.\\n"
	.string "I have to give this to AMPHY.$"

OlivineLighthouse_Text_JasmineAmphyHowFeeling:
	.string "JASMINE: AMPHY, how are you\\n"
	.string "feeling?$"

OlivineLighthouse_Text_AmphyPaluPalulu:
	.string "AMPHY: Palu palulu!$"

OlivineLighthouse_Text_JasmineThankYou:
	.string "JASMINE: …Thank you. AMPHY looks\\n"
	.string "so much better.\\p"
	.string "I'll return to the GYM at once.\\n"
	.string "Please come and challenge me.$"
"""

AMPHY_NOVO = """OlivineLighthouse_EventScript_Ampharos::
	lock
	faceplayer
	goto_if_lt VAR_OLIVINE_CITY_STATE, 5, OlivineLighthouse_EventScript_AmpharosSick
	fadescreen FADE_TO_WHITE
	playse SE_M_THUNDERBOLT2
	waitse
	fadescreen FADE_FROM_WHITE
	playmoncry SPECIES_AMPHAROS, CRY_MODE_NORMAL
	msgbox OlivineLighthouse_Text_AmphyPaluPalulu, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

OlivineLighthouse_EventScript_AmpharosSick::
	playmoncry SPECIES_AMPHAROS, CRY_MODE_NORMAL
	msgbox OlivineLighthouse_Text_AmphyBreathingLabored, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end
"""

AMPHY_VELHO = """OlivineLighthouse_EventScript_Ampharos::
	lock
	msgbox OlivineLighthouse_Text_JasmineNote, MSGBOX_DEFAULT
	playmoncry SPECIES_AMPHAROS, CRY_MODE_NORMAL
	msgbox OlivineLighthouse_Text_AmphyBreathingLabored, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end
"""

GINASIO = f"""
{MARCA}
@ A JASMINE do ginasio nasce ESCONDIDA e so aparece depois da AMPHY. Flag nasce
@ apagada e objeto com flag apagada nasce visivel, entao quem decide e este
@ ON_TRANSITION, que roda toda vez que o jogador entra e nao depende de gancho
@ de inicio de jogo nenhum.
OlivineCity_Gym_OnTransition::
	goto_if_ge VAR_OLIVINE_CITY_STATE, 5, OlivineCity_Gym_JasmineVoltou
	setflag FLAG_HIDE_OLIVINE_CITY_GYM_JASMINE
	end

OlivineCity_Gym_JasmineVoltou::
	clearflag FLAG_HIDE_OLIVINE_CITY_GYM_JASMINE
	end
"""

FARMACIA = f"""
{MARCA}
@ A farmacia de Cianwood. No hns o unico NPC deste mapa E o farmaceutico e nao
@ ha loja; aqui ele ja era balconista de mart quando esta rodada comecou, entao
@ o remedio vem ANTES do balcao e a loja continua existindo. Nada foi tirado.
CianwoodShop_EventScript_Pharmacist::
	goto_if_ne VAR_OLIVINE_CITY_STATE, 3, CianwoodShop_EventScript_SemRemedio
	msgbox CianwoodShop_Text_PharmacistGivePotion, MSGBOX_DEFAULT
	giveitem ITEM_SECRET_POTION
	setvar VAR_OLIVINE_CITY_STATE, 4
	return

CianwoodShop_EventScript_SemRemedio::
	return

CianwoodShop_Text_PharmacistGivePotion:
	.string "Your POKéMON appear to be fine.\\p"
	.string "Is something worrying you?\\p"
	.string "…\\p"
	.string "The LIGHTHOUSE POKéMON is in\\n"
	.string "trouble?\\p"
	.string "I got it!\\n"
	.string "This ought to do the trick.$"
"""


def alvo(caminho):
    return os.path.join(REPO, caminho)


def toca_farol(relato):
    p = alvo("data/maps/OlivineCity_Lighthouse/scripts.inc")
    txt = open(p, encoding="utf-8").read()
    if MARCA in txt:
        relato.append("farol: ja tem o arco, nada a fazer")
        return
    if AMPHY_VELHO not in txt:
        raise SystemExit("farol: o script velho da AMPHY nao esta como esperado")
    novo = txt.replace(AMPHY_VELHO, AMPHY_NOVO, 1)
    # o MapScripts vazio ganha o ON_TRANSITION
    novo = novo.replace(
        "OlivineCity_Lighthouse_MapScripts::\n\t.byte 0",
        "OlivineCity_Lighthouse_MapScripts::\n"
        "\tmap_script MAP_SCRIPT_ON_TRANSITION, "
        "OlivineCity_Lighthouse_OnTransition\n\t.byte 0", 1)
    novo = novo.rstrip("\n") + "\n" + FAROL
    relato.append("farol: cena da JASMINE, cura da AMPHY e ON_TRANSITION")
    if APLICA:
        open(p, "w", encoding="utf-8").write(novo)

    # o objeto: sprite, script e flag
    pj = alvo("data/maps/OlivineCity_Lighthouse/map.json")
    d = json.load(open(pj, encoding="utf-8"))
    achou = 0
    for i, o in enumerate(d["object_events"], 1):
        if (o["x"], o["y"]) == (156, 9):
            o["graphics_id"] = "OBJ_EVENT_GFX_WOMAN_1"
            o["movement_type"] = "MOVEMENT_TYPE_FACE_DOWN"
            o["script"] = "OlivineLighthouse_EventScript_Jasmine"
            o["flag"] = "FLAG_HIDE_LIGHTHOUSE_JASMINE"
            achou = i
        if (o["x"], o["y"]) == (156, 8):
            o["script"] = "OlivineLighthouse_EventScript_Ampharos"
    if achou != LOCALID_JASMINE:
        raise SystemExit(
            f"farol: a JASMINE e o objeto {achou} e o script usa "
            f"{LOCALID_JASMINE}; `removeobject` erraria de boneco")
    relato.append(f"farol: JASMINE e o object_event {achou}, como o script diz")
    if APLICA:
        RG.grava_como_estava(pj, d)


def toca_ginasio(relato):
    p = alvo("data/maps/OlivineCity_Gym/scripts.inc")
    txt = open(p, encoding="utf-8").read()
    if MARCA in txt:
        relato.append("ginasio: ja tem o portao, nada a fazer")
        return
    novo = txt.replace(
        "OlivineCity_Gym_MapScripts::\n\t.byte 0",
        "OlivineCity_Gym_MapScripts::\n"
        "\tmap_script MAP_SCRIPT_ON_TRANSITION, OlivineCity_Gym_OnTransition\n"
        "\t.byte 0", 1)
    if novo == txt:
        raise SystemExit("ginasio: MapScripts nao esta no formato esperado")
    novo = novo.rstrip("\n") + "\n" + GINASIO
    relato.append("ginasio: ON_TRANSITION que esconde a JASMINE ate a cura")
    if APLICA:
        open(p, "w", encoding="utf-8").write(novo)

    pj = alvo("data/maps/OlivineCity_Gym/map.json")
    d = json.load(open(pj, encoding="utf-8"))
    for o in d["object_events"]:
        if o.get("script") == "OlivineCity_Gym_EventScript_Jasmine":
            o["flag"] = "FLAG_HIDE_OLIVINE_CITY_GYM_JASMINE"
    if APLICA:
        RG.grava_como_estava(pj, d)


def toca_farmacia(relato):
    p = alvo("data/maps/CianwoodShop/scripts.inc")
    txt = open(p, encoding="utf-8").read()
    if MARCA in txt:
        relato.append("farmacia: ja tem o remedio, nada a fazer")
        return
    velho = "CianwoodShop_EventScript_Clerk::\n\tlock\n\tfaceplayer\n"
    if velho not in txt:
        raise SystemExit("farmacia: o balconista nao esta no formato esperado")
    novo = txt.replace(
        velho, velho + "\tcall CianwoodShop_EventScript_Pharmacist\n", 1)
    novo = novo.rstrip("\n") + "\n" + FARMACIA
    relato.append("farmacia: o balconista de Cianwood entrega a SECRETPOTION")
    if APLICA:
        open(p, "w", encoding="utf-8").write(novo)


def demo():
    """Autoteste das decisões que o build não pega sozinho."""
    # 1. o LOCALID do script tem que ser o indice REAL do objeto, senao o
    #    `removeobject` apaga outro boneco (o proprio jogador, no pior caso)
    d = json.load(open(alvo("data/maps/OlivineCity_Lighthouse/map.json"),
                       encoding="utf-8"))
    idx = [i for i, o in enumerate(d["object_events"], 1)
           if (o["x"], o["y"]) == (156, 9)]
    assert idx == [LOCALID_JASMINE], (idx, LOCALID_JASMINE)
    idx = [i for i, o in enumerate(d["object_events"], 1)
           if (o["x"], o["y"]) == (156, 8)]
    assert idx == [LOCALID_AMPHAROS], (idx, LOCALID_AMPHAROS)

    # 2. o alocador de flag nunca devolve endereco JA APELIDADO
    txt = open(FLAGS_H, encoding="utf-8").read()
    alvo_flag, _ = livre_flag(txt, "FLAG_QUE_NAO_EXISTE_DE_PROPOSITO")
    assert alvo_flag and alvo_flag.startswith("FLAG_UNUSED_0x")
    assert not re.search(rf"^#define\s+\w+\s+{alvo_flag}\s*$", txt, re.M), (
        f"{alvo_flag} ja tem dono")

    # 3. o alocador de var idem
    txt = open(VARS_H, encoding="utf-8").read()
    v = livre_var(txt, "VAR_QUE_NAO_EXISTE_DE_PROPOSITO")
    assert v and v.startswith("VAR_UNUSED_0x")
    assert not re.search(rf"^#define\s+\w+\s+{v}\s*(//.*)?$", txt, re.M), (
        f"{v} ja tem dono")

    # 4. o item entra em APPEND PURO: id novo > todos os existentes
    t = open(ITEMS_H, encoding="utf-8").read()
    ids = [int(n) for n in re.findall(r"^\s*ITEM_\w+\s*=\s*(\d+),", t, re.M)]
    assert max(ids) < max(ids) + 1
    assert "ITEMS_COUNT," in t

    print(f"demo ok: JASMINE e o objeto {LOCALID_JASMINE}, AMPHY o "
          f"{LOCALID_AMPHAROS}, flag livre {alvo_flag}, var livre {v}")


def main():
    if DEMO:
        demo()
        return 0
    relato = []
    escreve_flags(relato)
    escreve_var(relato)
    escreve_item(relato)
    toca_farol(relato)
    toca_ginasio(relato)
    toca_farmacia(relato)
    for l in relato:
        print("  " + l)
    print("\nescrito." if APLICA else "\n(nada escrito; rode com --aplica)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
