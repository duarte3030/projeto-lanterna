#!/usr/bin/env python3
"""Porta os treinadores de Kanto do pret/pokefirered para o formato .party daqui.

Uso:
    python3 dev_scripts/importa_treinadores_kanto.py /caminho/do/pokefirered

O que faz, em duas frentes:

1. Renumera, em include/constants/opponents_frlg.h, os nomes que scripts de mapa
   realmente usam, tirando-os da faixa 0..623 (que colide com Hoenn/Johto/Sinnoh
   no MESMO espaco de ids) e jogando para 1400..1799, faixa exclusiva de Kanto.
   Sem isso, TRAINER_LEADER_BROCK vale 314, que e TRAINER_SHELBY_2, um montanhista
   de Hoenn: quem entra no ginasio de Pewter luta contra o Shelby.

2. Escreve o time de verdade de cada um em src/data/trainers.party, APENSANDO no
   fim. Nada e inventado: especie, nivel, IV, golpes e item saem iguais aos do
   pokefirered. Classe e pic sao resolvidas contra as constantes que existem
   NESTE repo, lidas em tempo de execucao, preferindo sempre o ramo _FRLG.

A lista de quem entra vem de dev_scripts/kanto_usados.txt (nome<TAB>id<TAB>mapas),
ou do caminho passado em --usados.
"""
import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADER = os.path.join(REPO, "include/constants/opponents_frlg.h")
PARTY = os.path.join(REPO, "src/data/trainers.party")

# Faixa exclusiva desta frente. Abaixo de 1400 ja esta ocupado por Hoenn, Johto e
# Sinnoh; 1800+ e de outra frente.
ID_MIN, ID_MAX = 1400, 1799

MARCA = "=== ACERVO KANTO (importa_treinadores_kanto.py) ==="

# Classe do pokefirered sem equivalente aqui, nem com sufixo _FRLG nem sem ele.
CLASSE_SUB = {
    "TRAINER_CLASS_PKMN_TRAINER": "TRAINER_CLASS_PKMN_TRAINER_1",
    "TRAINER_CLASS_PKMN_TRAINER_UNUSED": "TRAINER_CLASS_PKMN_TRAINER_2",
}

# Pic do pokefirered sem equivalente aqui.
PIC_SUB = {}

# Golpes que o expansion renomeou.
RENOMEIA_MOVE = {
    "MOVE_FAINT_ATTACK": "MOVE_FEINT_ATTACK",
    "MOVE_VICEGRIP": "MOVE_VISE_GRIP",
    "MOVE_SMELLINGSALT": "MOVE_SMELLING_SALTS",
}

AI_SUB = {
    "AI_SCRIPT_CHECK_BAD_MOVE": "AI_FLAG_CHECK_BAD_MOVE",
    "AI_SCRIPT_TRY_TO_FAINT": "AI_FLAG_TRY_TO_FAINT",
    "AI_SCRIPT_CHECK_VIABILITY": "AI_FLAG_CHECK_VIABILITY",
}


def le(caminho):
    return open(caminho, encoding="utf-8", errors="replace").read()


def constantes(caminho, prefixo):
    return set(re.findall(rf"\b{prefixo}[A-Z0-9_]+", le(os.path.join(REPO, caminho))))


def blocos_de_chave(corpo):
    """Os grupos {...} de primeiro nivel. Regex nao serve: o mon tem um
    `.moves = {...}` dentro, e [^{}]* nunca casa o bloco de fora."""
    fora, prof, inicio = [], 0, None
    for i, c in enumerate(corpo):
        if c == "{":
            if prof == 0:
                inicio = i + 1
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0:
                fora.append(corpo[inicio:i])
    return fora


def parse_parties(texto):
    """symbol -> lista de mons. Resolve as macros DUMMY_* por substituicao previa."""
    dummies = {}
    for m in re.finditer(r"#define (DUMMY_\w+)\s+\\\n((?:.*\\\n)*.*)", texto):
        dummies[m.group(1)] = m.group(2).replace("\\", " ")
    saida = {}
    for m in re.finditer(
        r"static const struct TrainerMon\w+ (\w+)\[\] = \{(.*?)\n?\};", texto, re.S
    ):
        nome, corpo = m.group(1), m.group(2)
        for d, texto_d in dummies.items():
            corpo = re.sub(rf"\b{d}\b", texto_d, corpo)
        mons = []
        for b in blocos_de_chave(corpo):
            if ".species" not in b:
                continue
            campo = lambda p: (re.search(p, b).group(1) if re.search(p, b) else None)
            moves = re.search(r"\.moves\s*=\s*\{([^}]*)\}", b)
            mons.append({
                "lvl": campo(r"\.lvl\s*=\s*(\d+)"),
                "species": campo(r"\.species\s*=\s*(SPECIES_\w+)"),
                "item": campo(r"\.heldItem\s*=\s*(ITEM_\w+)"),
                "iv": campo(r"\.iv\s*=\s*(\d+)"),
                "moves": [x.strip() for x in moves.group(1).split(",")
                          if x.strip().startswith("MOVE_")] if moves else [],
            })
        saida[nome] = mons
    return saida


def parse_trainers(texto):
    saida = {}
    for m in re.finditer(r"\[(TRAINER_\w+)\] =\s*\{(.*?)\n    \},", texto, re.S):
        tid, corpo = m.group(1), m.group(2)
        campo = lambda p: (re.search(p, corpo).group(1)
                           if re.search(p, corpo) else None)
        itens = re.search(r"\.items\s*=\s*\{([^}]*)\}", corpo)
        saida[tid] = {
            "class": campo(r"\.trainerClass\s*=\s*(\w+)"),
            "pic": campo(r"\.trainerPic\s*=\s*(\w+)"),
            "name": campo(r'\.trainerName\s*=\s*_\("([^"]*)"\)') or "",
            "music": campo(r"(TRAINER_ENCOUNTER_MUSIC_\w+)"),
            "female": "F_TRAINER_FEMALE" in corpo,
            "double": ".doubleBattle = TRUE" in corpo,
            "ai": re.findall(r"AI_SCRIPT_\w+", corpo),
            "items": re.findall(r"ITEM_\w+", itens.group(1)) if itens else [],
            "party": campo(r"\.party\s*=\s*\w+\((\w+)\)"),
            "macro": campo(r"\.party\s*=\s*(\w+)\("),
        }
    return saida


def resolve(valor, subs, existentes):
    """Constante do pokefirered -> constante daqui. Prefere sempre o ramo _FRLG,
    porque este repo guarda a arte de Kanto sob esse sufixo."""
    if valor is None:
        return None, None
    if valor in subs:
        return subs[valor], f"{valor} -> {subs[valor]}"
    if valor + "_FRLG" in existentes:
        return valor + "_FRLG", None
    if valor in existentes:
        return valor, None
    return None, f"{valor} SEM EQUIVALENTE"


def blocos_party(nome, t, mons, ctx):
    """Um bloco .party. Devolve (linhas, avisos)."""
    avisos = []
    classe, aviso = resolve(t["class"], CLASSE_SUB, ctx["classes"])
    if aviso:
        avisos.append(f"classe: {aviso}")
    pic, aviso = resolve(t["pic"], PIC_SUB, ctx["pics"])
    if aviso:
        avisos.append(f"pic: {aviso}")
    if not pic:
        return None, avisos + [f"{nome}: sem pic utilizavel, pulado"]

    L = [f"=== {nome} ==="]
    L.append(f"Name: {t['name'].title()}")
    if classe:
        L.append(f"Class: {classe}")
    L.append(f"Pic: {pic}")
    L.append("Gender: " + ("Female" if t["female"] else "Male"))
    # encounterMusic_gender junta o jingle e o bit de sexo no mesmo campo; aqui
    # sao duas linhas. Sem esta, todo treinador de Kanto entra com o jingle padrao.
    if t["music"] and t["music"] in ctx["musicas"]:
        L.append(f"Music: {t['music']}")
    elif t["music"]:
        avisos.append(f"{nome}: musica {t['music']} nao existe aqui")
    itens = [i for i in t["items"] if i != "ITEM_NONE" and i in ctx["itens"]]
    if itens:
        L.append("Items: " + " / ".join(itens))
    L.append("Double Battle: " + ("Yes" if t["double"] else "No"))
    ai = [AI_SUB[a] for a in dict.fromkeys(t["ai"]) if a in AI_SUB]
    if ai:
        L.append("AI: " + " / ".join(ai))

    # ITEM_* / NO_ITEM_* e *_CUSTOM_MOVES / *_DEFAULT_MOVES dizem quais campos do
    # struct valem. Sem CUSTOM_MOVES o jogo usa os 4 ultimos golpes de nivel, que
    # e exatamente o default do trainerproc: nao escrever move nenhum.
    macro = t["macro"] or "NO_ITEM_DEFAULT_MOVES"
    usa_item = macro.startswith("ITEM_")
    usa_moves = macro.endswith("CUSTOM_MOVES")

    for mon in mons:
        sp = mon["species"]
        if sp not in ctx["species"]:
            avisos.append(f"{nome}: especie {sp} nao existe aqui, mon pulado")
            continue
        cabeca = sp
        if usa_item and mon["item"] and mon["item"] != "ITEM_NONE":
            if mon["item"] in ctx["itens"]:
                cabeca += f" @ {mon['item']}"
            else:
                avisos.append(f"{nome}: item {mon['item']} nao existe aqui")
        L += ["", cabeca, f"Level: {mon['lvl'] or 5}"]
        # pokefirered guarda iv 0..255 num numero so; o .party quer 0..31 por stat.
        # A conta e a mesma do jogo: fixedIV = iv * MAX_PER_STAT_IVS / 255.
        v = min(31, int(mon["iv"] or 0) * 31 // 255)
        L.append(f"IVs: {v} HP / {v} Atk / {v} Def / {v} SpA / {v} SpD / {v} Spe")
        if usa_moves:
            for mv in mon["moves"]:
                mv = RENOMEIA_MOVE.get(mv, mv)
                if mv == "MOVE_NONE":
                    continue
                if mv not in ctx["moves"]:
                    avisos.append(f"{nome}: golpe {mv} nao existe aqui")
                    continue
                L.append(f"- {mv}")
    return L, avisos


def renumera(nomes_ok):
    """Reescreve os #define dos nomes portados para a faixa 1400+, na ordem em que
    aparecem no header. Devolve {nome: novo_id}."""
    texto = le(HEADER)
    ordem = [n for n in re.findall(r"^#define (TRAINER_\w+)\s", texto, re.M)
             if n in nomes_ok]
    if len(ordem) + ID_MIN > ID_MAX + 1:
        sys.exit(f"faixa {ID_MIN}..{ID_MAX} nao cabe {len(ordem)} treinadores")
    novos = {n: ID_MIN + i for i, n in enumerate(ordem)}
    def troca(m):
        nome = m.group(1)
        if nome not in novos:
            return m.group(0)
        return f"#define {nome:<42} {novos[nome]}"
    texto = re.sub(r"^#define (TRAINER_\w+)\s+(\d+)\s*$", troca, texto, flags=re.M)
    open(HEADER, "w", encoding="utf-8").write(texto)
    return novos


def apensa(linhas):
    """Troca o acervo de Kanto no fim de trainers.party, sem tocar no resto."""
    texto = le(PARTY)
    corte = texto.find(f"/*{MARCA}")
    if corte != -1:
        texto = texto[:corte]
    texto = texto.rstrip("\n") + "\n\n"
    texto += (
        f"/*{MARCA}\n"
        "   Times portados de pret/pokefirered. Nada aqui foi escrito a mao: quem\n"
        "   gera e dev_scripts/importa_treinadores_kanto.py. Rodar de novo troca so\n"
        "   este bloco. Comentario em bloco porque o formato .party nao aceita //. */\n\n"
    )
    open(PARTY, "w", encoding="utf-8").write(texto + "\n".join(linhas) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("firered", help="raiz do clone de pret/pokefirered")
    ap.add_argument("--usados", default=os.path.join(REPO, "dev_scripts/kanto_usados.txt"))
    a = ap.parse_args()

    quero = [l.split("\t")[0].strip()
             for l in le(a.usados).strip().split("\n") if l.strip()]
    trainers = parse_trainers(le(os.path.join(a.firered, "src/data/trainers.h")))
    parties = parse_parties(le(os.path.join(a.firered, "src/data/trainer_parties.h")))
    ctx = {
        "species": constantes("include/constants/species.h", "SPECIES_"),
        "moves": constantes("include/constants/moves.h", "MOVE_"),
        "itens": constantes("include/constants/items.h", "ITEM_"),
        "classes": constantes("include/constants/trainers.h", "TRAINER_CLASS_"),
        "pics": constantes("include/constants/trainers.h", "TRAINER_PIC_"),
        "musicas": constantes("include/constants/trainers.h", "TRAINER_ENCOUNTER_MUSIC_"),
    }
    # So o que existe FORA do acervo desta ferramenta conta como "ja tem time":
    # o bloco que ela mesma escreveu vai ser substituido, entao nao bloqueia nada.
    anterior = le(PARTY).split(f"/*{MARCA}")[0]
    ja_tem = set(re.findall(r"^=== (TRAINER_\w+) ===", anterior, re.M))

    linhas, avisos, ok, fora = [], [], [], []
    for nome in quero:
        # Nome renomeado aqui para nao colidir com Johto: o dado esta no original.
        fonte = nome if nome in trainers else re.sub(r"_FRLG$", "", nome)
        t = trainers.get(fonte)
        if not t:
            fora.append(f"{nome}: nao existe em pokefirered")
            continue
        mons = parties.get(t["party"] or "", [])
        if not mons:
            fora.append(f"{nome}: time {t['party']} vazio em pokefirered")
            continue
        if nome in ja_tem:
            fora.append(f"{nome}: ja tem entrada em trainers.party, nao mexido")
            continue
        bloco, av = blocos_party(nome, t, mons, ctx)
        avisos += av
        if bloco is None:
            fora.append(f"{nome}: pulado")
            continue
        linhas += bloco + [""]
        ok.append(nome)

    novos = renumera(set(ok))
    apensa(linhas)

    print(f"portados: {len(ok)} de {len(quero)}")
    print(f"ids {min(novos.values())}..{max(novos.values())} (faixa {ID_MIN}..{ID_MAX})")
    if fora:
        print(f"\nFORA ({len(fora)}):")
        for f in fora:
            print("  ", f)
    if avisos:
        print(f"\nAVISOS ({len(set(avisos))}):")
        for f in sorted(set(avisos)):
            print("  ", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
