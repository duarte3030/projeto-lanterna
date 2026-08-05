#!/usr/bin/env python3
"""Fecha as placas (bg_event) de Unova que o import original deixou para tras.

Medido em 05/08/2026: o BW3G tem 507 bg_event nos mapas que ja estao aqui, e a
ROM tinha 390. Os 117 que faltavam **nao sao placa de texto**: `importa_unova.py`
so aceita bg_event que resolve para um texto do gen 2, e nenhum destes 117 tem
texto proprio. Todos sao COMPORTAMENTO, e cada familia precisa de uma decisao:

| familia                     | n  | o que este script faz                       |
|-----------------------------|----|---------------------------------------------|
| `jumpstd gymstatue1`        | 15 | porta o texto do gen 2, que e so o nome do  |
|                             |    | mapa + "#MON GYM" (data/text/std_text.asm). |
|                             |    | O que ficou de fora antes era o gymstatue2, |
|                             |    | que monta LIDER e VITORIAS em tempo de exec |
| `jumpstd apartmentstairs`   |  7 | texto do gen 2, palavra por palavra         |
| `jumpstd elevatorbutton`    |  4 | so som, igual ao gen 2: nao tem texto       |
| maquina de cassino          | 54 | `playslotmachine`, que este repo ja tem     |
| gruta escondida             | 22 | item aleatorio da tabela do BW3G, uma flag  |
|                             |    | por gruta                                   |
| PC do quarto do jogador     |  1 | `EventScript_PC`, que este repo ja tem      |

Fica de fora de proposito (e sai no relatorio): as consoles de sala de link
(TradeCenter, Colosseum, TimeCapsule, o quadro de recordes do Pokecenter 2F),
que sao cabo de link e nao existem aqui; o elevador da Castelia Plaza, que e a
mesma pendencia dos 7 warps de elevador ja documentada em PLANO-UNOVA.md; e a
estante e o poster do quarto do jogador, que no proprio BW3G estao comentados ou
sao decoracao.

Duas trocas honestas, e estao marcadas no codigo gerado:

1. **Card flip vira caca-niquel.** O BW3G tem dois minijogos de cassino; este
   repo so tem o caca-niquel de Mauville. A alternativa era deixar 20 maquinas
   mudas no meio do salao.
2. **A gruta escondida da uma vez, nao por dia.** No gen 2 ela reenche com o
   contador diario; portar isso e mecanica nova. Uma flag por gruta faz o item
   sair uma vez so, que e o comportamento de item escondido que o motor ja tem.

Faixa de flag: 0x4B4 a 0x4EE, reservada a esta frente. Gasta uma por gruta.

Uso:
    python3 dev_scripts/importa_placas_unova.py            # so relata
    python3 dev_scripts/importa_placas_unova.py --aplica   # escreve

E idempotente: pula toda placa que ja esta no map.json na mesma coordenada,
entao rodar duas vezes nao duplica nada.

Compatibilidade de save: bg_event nao tem indice guardado na save (quem guarda e
warp, objeto e flag), entao acrescentar placa e sempre seguro. As unicas flags
gastas saem da faixa acima, que ja esta dentro de FLAGS_COUNT.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
os.chdir(REPO)

import importa_unova as iu  # noqa: E402  (reusa le_grupos, le_eventos, jumpstd_de)

APLICA = "--aplica" in sys.argv
BW3G = iu.BW3G

# Primeira flag da faixa exclusiva desta frente. Cada gruta escondida consome
# uma; ver o cabecalho.
FLAG_BASE = 0x4B4
FLAG_TETO = 0x4EE

# Tabelas de item da gruta escondida, copiadas de data/items/hidden_grotto.asm
# do BW3G. O gen 2 sorteia 1 de 16 com peso pela repeticao, e por isso a lista
# repete item de proposito: manter a repeticao mantem a chance.
TIERS = {
    1: ["RED_SHARD", "RED_SHARD", "BLUE_SHARD", "BLUE_SHARD", "GREEN_SHARD",
        "GREEN_SHARD", "YELLOW_SHARD", "YELLOW_SHARD", "MOOMOO_MILK",
        "MOOMOO_MILK", "PEARL", "PEARL", "ETHER", "ETHER", "REVIVE", "REVIVE"],
    2: ["RED_SHARD", "BLUE_SHARD", "GREEN_SHARD", "YELLOW_SHARD", "DAMP_ROCK",
        "HEAT_ROCK", "SMOOTH_ROCK", "ICY_ROCK", "BIG_PEARL", "BIG_PEARL",
        "PROTEIN", "IRON", "CARBOS", "CALCIUM", "HP_UP", "ELIXER"],
    3: ["DAMP_ROCK", "DAMP_ROCK", "HEAT_ROCK", "HEAT_ROCK", "SMOOTH_ROCK",
        "SMOOTH_ROCK", "ICY_ROCK", "ICY_ROCK", "PROTEIN", "IRON", "CARBOS",
        "CALCIUM", "PP_UP", "MAX_ELIXER", "MAX_REVIVE", "RARE_CANDY"],
}

# Estes ficam de fora, e o motivo esta no cabecalho. Casado por substring do
# rotulo do script do gen 2.
FORA = {
    "ConsoleScript": "sala de link (cabo), nao existe aqui",
    "LinkRecordSign": "quadro de recordes de link, nao existe aqui",
    "ElevatorScript": "elevador, mesma pendencia dos 7 warps ja documentada",
    "BookshelfScript": "no proprio BW3G o corpo esta todo comentado",
    "PosterScript": "decoracao (describedecoration), nao e placa",
}


def corpo_de(asm, rotulo):
    """As linhas do rotulo ate o proximo rotulo. '' se o rotulo nao existir."""
    m = re.search(rf"^{re.escape(rotulo)}:+\s*$", asm, re.M)
    if not m:
        return ""
    linhas = []
    for ln in asm[m.end():].splitlines():
        if re.match(r"^\w+:", ln):
            break
        linhas.append(ln)
    return "\n".join(linhas)


def placa(x, y, rotulo):
    return {"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": rotulo}


# --------------------------------------------------------------------- blocos
# compartilhados: um `::` global, emitido no primeiro mapa que precisar dele.

def bloco_gruta(tier):
    itens = ", ".join(iu.item_gen3(i) for i in TIERS[tier])
    return f"""
Unova_EventScript_GrutaTier{tier}::
	lockall
	msgbox Unova_Text_AchouGruta, MSGBOX_DEFAULT
	randomelement {itens}
	giveitem VAR_RESULT
	releaseall
	end
"""


COMPARTILHADO = {
    "Unova_Text_AchouGruta": """
Unova_Text_AchouGruta::
	.string "Hey! It's a\\n"
	.string "hidden grotto!$"
""",
    "Unova_Text_GrutaVazia": """
Unova_Text_GrutaVazia::
	.string "There's nothing\\n"
	.string "here anymore.$"
""",
    "Unova_EventScript_GrutaVazia": """
Unova_EventScript_GrutaVazia::
	msgbox Unova_Text_GrutaVazia, MSGBOX_SIGN
	end
""",
    "Unova_EventScript_EscadaPredio": """
@ jumpstd apartmentstairs do BW3G; texto de data/text/std_text.asm
Unova_EventScript_EscadaPredio::
	msgbox Unova_Text_EscadaPredio, MSGBOX_SIGN
	end

Unova_Text_EscadaPredio::
	.string "The door to the\\n"
	.string "stairwell is closed.$"
""",
    "Unova_EventScript_BotaoElevador": """
@ jumpstd elevatorbutton do BW3G: som e nada mais, igual la
Unova_EventScript_BotaoElevador::
	lockall
	playse SE_PIN
	delay 15
	playse SE_DING_DONG
	waitse
	releaseall
	end
""",
    "Unova_EventScript_CacaNiquel": """
@ Maquina de cassino do BW3G. O `special SlotMachine` do gen 2 vira o
@ caca-niquel que este repo ja tem em MauvilleCity_GameCorner; quem chama define
@ VAR_0x8004 (0 a 11) com o numero da maquina, que e o que da a sorte de cada uma.
@ ponytail: o card flip do BW3G cai aqui tambem, porque este repo nao tem
@ segundo minijogo de cassino. O certo seria portar o card flip.
Unova_EventScript_CacaNiquel::
	lockall
	checkitem ITEM_COIN_CASE
	goto_if_eq VAR_RESULT, FALSE, MauvilleCity_GameCorner_EventScript_NoCoinCase
	specialvar VAR_RESULT, GetSlotMachineId
	playslotmachine VAR_RESULT
	releaseall
	end
""",
}
for _t in TIERS:
    COMPARTILHADO[f"Unova_EventScript_GrutaTier{_t}"] = bloco_gruta(_t)


# ------------------------------------------------------------------ o trabalho

grupos = iu.le_grupos()
idx = iu.indice_asm()

motivos = Counter()
recusadas = []
emitidos = set()
plano = []          # (nome_do_mapa, [bg novos], trecho para scripts.inc)
flag_de_gruta = {}  # rotulo da gruta no BW3G -> numero de flag
aliases = []        # linhas novas de include/constants/flags.h

for _, mapas in grupos:
    for camel, const, w, h, tileset, amb, land, mus in mapas:
        nome = iu.PREFIXO + camel
        dir_mapa = f"{REPO}/data/maps/{nome}"
        p = idx.get(camel)
        if not os.path.isdir(dir_mapa) or not p:
            continue
        asm = open(p, encoding="utf-8", errors="replace").read()
        ev = iu.le_eventos(asm, camel)
        nosso = json.load(open(f"{dir_mapa}/map.json"))
        temos = {(b["x"], b["y"]) for b in nosso.get("bg_events", [])}

        novos, trechos, precisa = [], [], []
        n_maquina = 0
        for x, y, kind, script in ev["bg"]:
            if (x, y) in temos or kind == "ITEM":
                continue
            corpo = corpo_de(asm, script)
            std = iu.jumpstd_de(asm, script)

            fora = next((v for k, v in FORA.items() if k in script), None)
            if fora:
                motivos[fora] += 1
                recusadas.append(f"{nome}/{script}: {fora}")
                continue

            if std == "gymstatue1":
                rot = f"{nome}_EventScript_EstatuaGinasio"
                if rot not in emitidos:
                    emitidos.add(rot)
                    # mapnametotext do gen 2 = o nome do landmark do mapa
                    trechos.append(
                        f"\n@ jumpstd gymstatue1 do BW3G: nome do mapa + \"#MON GYM\"\n"
                        f"{rot}::\n\tmsgbox {nome}_Text_EstatuaGinasio, MSGBOX_SIGN\n\tend\n"
                        f"\n{nome}_Text_EstatuaGinasio::\n"
                        f"\t.string \"{land.replace('_', ' ')}\\n\"\n"
                        f"\t.string \"POKéMON GYM$\"\n")
                novos.append(placa(x, y, rot))
                motivos["estatua de ginasio"] += 1
                continue

            if std == "apartmentstairs":
                precisa.append("Unova_EventScript_EscadaPredio")
                novos.append(placa(x, y, "Unova_EventScript_EscadaPredio"))
                motivos["escada de predio"] += 1
                continue

            if std == "elevatorbutton":
                precisa.append("Unova_EventScript_BotaoElevador")
                novos.append(placa(x, y, "Unova_EventScript_BotaoElevador"))
                motivos["botao de elevador"] += 1
                continue

            m = re.search(r"hiddengrotto\s+\w+,\s*HIDDENGROTTO_TIER_(\d)", corpo)
            if m:
                tier = int(m.group(1))
                if script not in flag_de_gruta:
                    n = FLAG_BASE + len(flag_de_gruta)
                    if n > FLAG_TETO:
                        raise SystemExit("faixa de flag 0x4B4-0x4EE estourou")
                    flag_de_gruta[script] = n
                    aliases.append(
                        f"#define FLAG_UNOVA_GRUTA_{script.replace('HiddenGrotto', '').upper():<24}"
                        f" FLAG_UNUSED_0x{n:03X}")
                rot = f"{nome}_EventScript_Gruta{flag_de_gruta[script]:03X}"
                flag = f"FLAG_UNOVA_GRUTA_{script.replace('HiddenGrotto', '').upper()}"
                if rot not in emitidos:
                    emitidos.add(rot)
                    trechos.append(
                        f"\n@ Gruta escondida do BW3G (tier {tier}). ponytail: la ela reenche\n"
                        f"@ todo dia; aqui e uma flag e o item sai uma vez so.\n"
                        f"{rot}::\n"
                        f"\tgoto_if_set {flag}, Unova_EventScript_GrutaVazia\n"
                        f"\tsetflag {flag}\n"
                        f"\tgoto Unova_EventScript_GrutaTier{tier}\n")
                precisa += ["Unova_Text_AchouGruta", "Unova_Text_GrutaVazia",
                            "Unova_EventScript_GrutaVazia",
                            f"Unova_EventScript_GrutaTier{tier}"]
                novos.append(placa(x, y, rot))
                motivos["gruta escondida"] += 1
                continue

            if "special SlotMachine" in corpo or "CardFlip" in script \
                    or "SlotsMachine" in script:
                rot = f"{nome}_EventScript_Maquina{n_maquina}"
                trechos.append(
                    f"\n{rot}::\n\tsetvar VAR_0x8004, {n_maquina % 12}\n"
                    f"\tgoto Unova_EventScript_CacaNiquel\n")
                precisa.append("Unova_EventScript_CacaNiquel")
                novos.append(placa(x, y, rot))
                n_maquina += 1
                motivos["maquina de cassino"] += 1
                continue

            if "special PlayersHousePC" in corpo:
                novos.append(placa(x, y, "EventScript_PC"))
                motivos["PC do quarto"] += 1
                continue

            motivos["sem regra"] += 1
            recusadas.append(f"{nome}/{script}: sem regra")

        if not novos:
            continue
        cab = ("\n@ Placas trazidas do BW3G por "
               "dev_scripts/importa_placas_unova.py\n")
        for lab in precisa:
            if lab not in emitidos:
                emitidos.add(lab)
                trechos.insert(0, COMPARTILHADO[lab])
        plano.append((nome, novos, cab + "".join(trechos)))

total = sum(len(n) for _, n, _ in plano)
print(f"mapas tocados: {len(plano)}   placas novas: {total}")
for k, v in motivos.most_common():
    print(f"  {v:4d}  {k}")
print(f"flags gastas: {len(flag_de_gruta)} "
      f"(0x{FLAG_BASE:03X} a 0x{FLAG_BASE + len(flag_de_gruta) - 1:03X})")
if recusadas:
    print(f"\nrecusadas: {len(recusadas)}")
    for r in recusadas[:8]:
        print("   ", r)

if not APLICA:
    print("\n(nada escrito; rode com --aplica)")
    sys.exit(0)

for nome, novos, trecho in plano:
    p = f"{REPO}/data/maps/{nome}/map.json"
    d = json.load(open(p))
    d.setdefault("bg_events", []).extend(novos)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(f"{REPO}/data/maps/{nome}/scripts.inc", "a", encoding="utf-8") as f:
        f.write(trecho)

if aliases:
    p = f"{REPO}/include/constants/flags.h"
    s = open(p).read()
    marca = "\n@FIM_FLAGS_UNOVA_GRUTA\n"
    if "FLAG_UNOVA_GRUTA_" not in s:
        alvo = "#define FLAG_HIDE_TOWER_FUJI"
        bloco = ("// Grutas escondidas de Unova (dev_scripts/importa_placas_unova.py).\n"
                 "// Faixa 0x4B4 a 0x4EE, reservada a essa frente em 05/08/2026.\n"
                 + "\n".join(aliases) + "\n\n")
        s = s.replace(alvo, bloco + alvo, 1)
        open(p, "w").write(s)

print(f"escrito: {total} placas em {len(plano)} mapas, "
      f"{len(aliases)} flags apelidadas")
