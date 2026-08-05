#!/usr/bin/env python3
"""Converte os treinadores dos 8 ginásios de Johto do hns para o formato .party.

Uso:
    python3 dev_scripts/import_johto_gym_trainers.py ../fontes-mapas/hns

Escreve src/data/trainers_johto.party (acervo) e imprime o mesmo conteúdo, que
depois é anexado a src/data/trainers.party, que é o arquivo que compila.

Espécie, nível, item e golpes saem iguais aos do hns. Classe e pic são resolvidas
contra as constantes que existem NESTE repo, lidas em tempo de execução: as do
ramo `_FRLG` são recusadas de propósito, porque esta build é Emerald.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "src/data/trainers_johto.party")

# hns -> nome neste repo. Prefixo JOHTO_ porque ROD, RONALD, ROXANNE, JASMINE e
# outros já existem em Emerald com outro time.
TRAINERS = {
    # Violet, Falkner
    "TRAINER_ROD": "TRAINER_JOHTO_BIRD_KEEPER_ROD",
    "TRAINER_ABE": "TRAINER_JOHTO_BIRD_KEEPER_ABE",
    "TRAINER_FALKNER_1": "TRAINER_JOHTO_LEADER_FALKNER",
    # Azalea, Bugsy
    "TRAINER_AL": "TRAINER_JOHTO_BUG_CATCHER_AL",
    "TRAINER_JOSH": "TRAINER_JOHTO_BUG_CATCHER_JOSH",
    "TRAINER_BENNY": "TRAINER_JOHTO_BUG_CATCHER_BENNY",
    "TRAINER_AMY_AND_MAY": "TRAINER_JOHTO_TWINS_AMY_AND_MAY",
    "TRAINER_BUGSY_1": "TRAINER_JOHTO_LEADER_BUGSY",
    # Goldenrod, Whitney
    "TRAINER_CARRIE": "TRAINER_JOHTO_LASS_CARRIE",
    "TRAINER_BRIDGET": "TRAINER_JOHTO_LASS_BRIDGET",
    "TRAINER_VICTORIA": "TRAINER_JOHTO_BEAUTY_VICTORIA",
    "TRAINER_SAMANTHA": "TRAINER_JOHTO_BEAUTY_SAMANTHA",
    "TRAINER_WHITNEY_1": "TRAINER_JOHTO_LEADER_WHITNEY",
    # Ecruteak, Morty
    "TRAINER_JEFFREY": "TRAINER_JOHTO_SAGE_JEFFREY",
    "TRAINER_PING": "TRAINER_JOHTO_SAGE_PING",
    "TRAINER_MARTHA": "TRAINER_JOHTO_MEDIUM_MARTHA",
    "TRAINER_GRACE": "TRAINER_JOHTO_MEDIUM_GRACE",
    "TRAINER_MORTY_1": "TRAINER_JOHTO_LEADER_MORTY",
    # Olivine, Jasmine
    "TRAINER_JASMINE_1": "TRAINER_JOHTO_LEADER_JASMINE",
    # Cianwood, Chuck
    "TRAINER_YOSHI": "TRAINER_JOHTO_BLACK_BELT_YOSHI",
    "TRAINER_LAO": "TRAINER_JOHTO_BLACK_BELT_LAO",
    "TRAINER_NOB": "TRAINER_JOHTO_BLACK_BELT_NOB",
    "TRAINER_LUNG": "TRAINER_JOHTO_BLACK_BELT_LUNG",
    "TRAINER_CHUCK_1": "TRAINER_JOHTO_LEADER_CHUCK",
    # Mahogany, Pryce
    "TRAINER_RONALD": "TRAINER_JOHTO_GENTLEMAN_RONALD",
    "TRAINER_BRAD": "TRAINER_JOHTO_SKIER_BRAD",
    "TRAINER_DOUGLAS": "TRAINER_JOHTO_BOARDER_DOUGLAS",
    "TRAINER_ROXANNE": "TRAINER_JOHTO_SKIER_ROXANNE",
    "TRAINER_CLARISSA": "TRAINER_JOHTO_SKIER_CLARISSA",
    "TRAINER_PRYCE_1": "TRAINER_JOHTO_LEADER_PRYCE",
    # Blackthorn, Clair
    "TRAINER_CODY": "TRAINER_JOHTO_COOLTRAINER_CODY",
    "TRAINER_FRAN": "TRAINER_JOHTO_COOLTRAINER_FRAN",
    "TRAINER_PAUL": "TRAINER_JOHTO_COOLTRAINER_PAUL",
    "TRAINER_MIKE": "TRAINER_JOHTO_COOLTRAINER_MIKE",
    "TRAINER_LOLA": "TRAINER_JOHTO_COOLTRAINER_LOLA",
    "TRAINER_CLAIR_1": "TRAINER_JOHTO_LEADER_CLAIR",
}

# Classe do hns que este repo não tem. O resto passa direto: trainerproc aceita
# a constante escrita por extenso, então só o que não existe aqui precisa troca.
CLASSE = {
    "TRAINER_CLASS_SAGE": "TRAINER_CLASS_EXPERT",
    "TRAINER_CLASS_MEDIUM": "TRAINER_CLASS_HEX_MANIAC",
    "TRAINER_CLASS_SKIER": "TRAINER_CLASS_LADY",
    "TRAINER_CLASS_BOARDER": "TRAINER_CLASS_CAMPER",
    "TRAINER_CLASS_COOLTRAINERF": "TRAINER_CLASS_COOLTRAINER_2",
    "TRAINER_CLASS_COOLTRAINERM": "TRAINER_CLASS_COOLTRAINER",
}

# Pic do hns que este repo não tem. Líder de Johto não tem retrato nesta ROM:
# usa o do líder de Hoenn do mesmo tipo, que é arte que já existe.
PIC = {
    "TRAINER_PIC_SAGE": "TRAINER_PIC_EXPERT_M",
    "TRAINER_PIC_MEDIUM": "TRAINER_PIC_HEX_MANIAC",
    "TRAINER_PIC_SKIER": "TRAINER_PIC_LADY",
    "TRAINER_PIC_BOARDER": "TRAINER_PIC_CAMPER",
    "TRAINER_PIC_COOLTRAINERM": "TRAINER_PIC_COOLTRAINER_M",
    "TRAINER_PIC_COOLTRAINERF": "TRAINER_PIC_COOLTRAINER_F",
    "TRAINER_PIC_LEADER_FALKNER": "TRAINER_PIC_LEADER_WINONA",
    "TRAINER_PIC_LEADER_BUGSY": "TRAINER_PIC_BUG_CATCHER",
    "TRAINER_PIC_LEADER_WHITNEY": "TRAINER_PIC_LEADER_ROXANNE",
    "TRAINER_PIC_LEADER_MORTY": "TRAINER_PIC_ELITE_FOUR_PHOEBE",
    "TRAINER_PIC_LEADER_JASMINE": "TRAINER_PIC_LEADER_ROXANNE",
    "TRAINER_PIC_LEADER_CHUCK": "TRAINER_PIC_LEADER_BRAWLY",
    "TRAINER_PIC_LEADER_PRYCE": "TRAINER_PIC_ELITE_FOUR_GLACIA",
    "TRAINER_PIC_LEADER_CLAIR": "TRAINER_PIC_ELITE_FOUR_GLACIA",
}

# Golpes e itens que o hns escreve com outro nome (ou que sumiram do expansion).
RENOMEIA_MOVE = {
    "MOVE_FAINT_ATTACK": "MOVE_FEINT_ATTACK",
}


def le(caminho):
    return open(caminho, encoding="utf-8", errors="replace").read()


def constantes(caminho, prefixo):
    return set(re.findall(rf"\b{prefixo}[A-Z0-9_]+", le(os.path.join(REPO, caminho))))


def parse_parties(texto):
    """symbol -> lista de dicts com species, lvl, heldItem, moves."""
    saida = {}
    for m in re.finditer(
        r"static const struct TrainerMon\w+ (\w+)\[\] = \{(.*?)\n\};", texto, re.S
    ):
        nome, corpo = m.group(1), m.group(2)
        mons = []
        for bloco in re.finditer(r"\{(.*?)\}(?=\s*,)", corpo, re.S):
            b = bloco.group(1)
            if ".species" not in b:
                continue
            mon = {
                "lvl": re.search(r"\.lvl\s*=\s*(\d+)", b),
                "species": re.search(r"\.species\s*=\s*(SPECIES_\w+)", b),
                "item": re.search(r"\.heldItem\s*=\s*(ITEM_\w+)", b),
                "iv": re.search(r"\.iv\s*=\s*(\d+)", b),
            }
            moves = re.search(r"\.moves\s*=\s*\{([^}]*)\}", b)
            mon = {k: (v.group(1) if v else None) for k, v in mon.items()}
            mon["moves"] = (
                [x.strip() for x in moves.group(1).split(",") if x.strip().startswith("MOVE_")]
                if moves
                else []
            )
            mons.append(mon)
        saida[nome] = mons
    return saida


def parse_trainers(texto):
    saida = {}
    for m in re.finditer(r"\[(TRAINER_\w+)\] =\s*\{(.*?)\n    \},", texto, re.S):
        tid, corpo = m.group(1), m.group(2)
        if tid not in TRAINERS:
            continue
        saida[tid] = {
            "class": (re.search(r"\.trainerClass\s*=\s*(\w+)", corpo) or [None, None])[1]
            if re.search(r"\.trainerClass\s*=\s*(\w+)", corpo)
            else None,
            "pic": (re.search(r"\.trainerPic\s*=\s*(\w+)", corpo).group(1)
                    if re.search(r"\.trainerPic\s*=\s*(\w+)", corpo) else None),
            "name": (re.search(r'\.trainerName\s*=\s*_\("([^"]*)"\)', corpo).group(1)
                     if re.search(r'\.trainerName\s*=\s*_\("([^"]*)"\)', corpo) else tid),
            "double": ".doubleBattle = TRUE" in corpo,
            "items": re.findall(r"(ITEM_\w+)", (re.search(r"\.items\s*=\s*\{([^}]*)\}", corpo).group(1)
                                                if re.search(r"\.items\s*=\s*\{([^}]*)\}", corpo) else "")),
            "party": (re.search(r"\.party\s*=\s*\w+\((\w+)\)", corpo).group(1)
                      if re.search(r"\.party\s*=\s*\w+\((\w+)\)", corpo) else None),
        }
        saida[tid]["class"] = (re.search(r"\.trainerClass\s*=\s*(\w+)", corpo).group(1)
                               if re.search(r"\.trainerClass\s*=\s*(\w+)", corpo) else None)
    return saida


def titulo(nome):
    return nome.title()


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    hns = os.path.abspath(sys.argv[1])
    trainers = parse_trainers(le(os.path.join(hns, "src/data/trainers.h")))
    parties = parse_parties(le(os.path.join(hns, "src/data/trainer_parties.h")))

    species_ok = constantes("include/constants/species.h", "SPECIES_")
    moves_ok = constantes("include/constants/moves.h", "MOVE_")
    itens_ok = constantes("include/constants/items.h", "ITEM_")
    classes_ok = constantes("include/constants/trainers.h", "TRAINER_CLASS_")
    pics_ok = constantes("include/constants/trainers.h", "TRAINER_PIC_")

    def resolve(valor, tabela, existentes, rotulo):
        """Constante do hns -> constante daqui. Recusa o ramo _FRLG de propósito."""
        alvo = tabela.get(valor, valor)
        if alvo in existentes and not alvo.endswith("_FRLG"):
            return alvo
        faltando.append(f"{rotulo} {valor} sem equivalente nesta build")
        return None

    faltando, linhas = [], []
    for hns_id, novo_id in TRAINERS.items():
        t = trainers.get(hns_id)
        if not t:
            faltando.append(f"treinador {hns_id} nao achado em trainers.h")
            continue
        mons = parties.get(t["party"], [])
        if not mons:
            faltando.append(f"time {t['party']} de {hns_id} vazio")
            continue
        classe = resolve(t["class"], CLASSE, classes_ok, f"classe de {hns_id}:")
        pic = resolve(t["pic"], PIC, pics_ok, f"pic de {hns_id}:")
        if not classe:
            classe = "TRAINER_CLASS_PKMN_TRAINER_1"
        if not pic:
            pic = "TRAINER_PIC_HIKER"

        linhas.append(f"=== {novo_id} ===")
        linhas.append(f"Name: {titulo(t['name'])}")
        linhas.append(f"Class: {classe}")
        linhas.append(f"Pic: {pic}")
        itens = [i for i in t["items"] if i != "ITEM_NONE"]
        for i in itens:
            if i not in itens_ok:
                faltando.append(f"item {i} de {hns_id} nao existe aqui")
        itens = [i for i in itens if i in itens_ok]
        if itens:
            linhas.append("Items: " + " / ".join(itens))
        linhas.append("Double Battle: " + ("Yes" if t["double"] else "No"))

        for mon in mons:
            sp = mon["species"]
            if sp not in species_ok:
                faltando.append(f"especie {sp} de {hns_id} nao existe aqui")
                continue
            item = mon["item"]
            cabeca = sp
            if item and item != "ITEM_NONE":
                if item in itens_ok:
                    cabeca += f" @ {item}"
                else:
                    faltando.append(f"item {item} de {hns_id} nao existe aqui")
            linhas.append("")
            linhas.append(cabeca)
            linhas.append(f"Level: {mon['lvl'] or 5}")
            iv = mon["iv"]
            if iv:
                # hns guarda iv 0..255; o .party quer 0..31 por stat.
                v = min(31, int(int(iv) * 31 / 255))
                linhas.append(
                    f"IVs: {v} HP / {v} Atk / {v} Def / {v} SpA / {v} SpD / {v} Spe")
            for mv in mon["moves"]:
                mv = RENOMEIA_MOVE.get(mv, mv)
                if mv == "MOVE_NONE":
                    continue
                if mv not in moves_ok:
                    faltando.append(f"golpe {mv} de {hns_id} nao existe aqui")
                    continue
                linhas.append(f"- {mv}")
        linhas.append("")

    cabecalho = (
        "/* ponytail: os 8 ginasios de Johto, portados de fontes-mapas/hns por\n"
        "   dev_scripts/import_johto_gym_trainers.py. Este arquivo e ACERVO: quem\n"
        "   compila e src/data/trainers.party, para onde estes blocos sao copiados.\n"
        "   Comentario em bloco porque o formato .party nao aceita barra dupla. */\n\n"
    )
    open(OUT, "w", encoding="utf-8").write(cabecalho + "\n".join(linhas) + "\n")
    print(f"escrito {OUT}: {len(TRAINERS) - len([f for f in faltando if 'treinador' in f])} treinadores")
    if faltando:
        print("\nPENDENCIAS:")
        for f in sorted(set(faltando)):
            print("  ", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
