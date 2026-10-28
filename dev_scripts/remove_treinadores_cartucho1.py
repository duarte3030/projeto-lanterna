#!/usr/bin/env python3
"""Fase 0 do cartucho 2: tira os treinadores que só o mundo de Kanto, Johto,
Hoenn e Sinnoh usava.

Roda DEPOIS de dev_scripts/remove_regioes_cartucho1.py. Um treinador fica se
o nome TRAINER_* dele aparece, fora de comentário, em código que ficou:
src/, include/, data/ (scripts, mapas, .s) ou test/. Os outros saem de
src/data/trainers.party e, quando o define é de include/constants/opponents.h,
o define sai também.

Os ids NÃO são compactados: cada treinador que fica mantém o número (e a flag
de treinador 0x500+id). A faixa que vagou é medida e impressa.

include/constants/opponents_frlg.h fica intacto: é a numeração do build FRLG
do mesmo repo. Os 474 treinadores de Kanto do .party de Emerald usam esses
números (1400..2273) sem define em opponents.h.

Uso: python3 dev_scripts/remove_treinadores_cartucho1.py [--aplicar]
"""
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OP = "include/constants/opponents.h"
FR = "include/constants/opponents_frlg.h"
PARTY = "src/data/trainers.party"
FORA = {OP, FR, PARTY, "src/data/trainers_frlg.party",
        "src/data/trainers_johto.party", "src/data/trainers_sinnoh.party"}


def le(p):
    return open(os.path.join(RAIZ, p), encoding="utf-8", errors="ignore").read()


def sem_comentario(t, ext):
    if ext in (".c", ".h", ".party"):
        t = re.sub(r"/\*.*?\*/", " ", t, flags=re.S)
        t = re.sub(r"//[^\n]*", " ", t)
    elif ext in (".inc", ".s"):
        t = re.sub(r"@[^\n]*", " ", t)
    return t


def citados():
    arqs = subprocess.run(["git", "ls-files", "src", "include", "data", "test"], cwd=RAIZ,
                          capture_output=True, text=True).stdout.split()
    out = set()
    for a in arqs:
        ext = os.path.splitext(a)[1]
        if a in FORA or ext not in (".c", ".h", ".inc", ".s", ".json", ".party"):
            continue
        if not os.path.exists(os.path.join(RAIZ, a)):
            continue
        out |= set(re.findall(r"\bTRAINER_\w+", sem_comentario(le(a), ext)))
    return out


def faixas_livres(usados, maximo):
    out, ini = [], None
    for i in range(1, maximo):
        if i not in usados and ini is None:
            ini = i
        if (i in usados or i == maximo - 1) and ini is not None:
            fim = i - 1 if i in usados else i
            out.append((ini, fim))
            ini = None
    return sorted(out, key=lambda f: f[0] - f[1])


def main():
    aplicar = "--aplicar" in sys.argv
    op_txt = le(OP)
    op = {k: int(v) for k, v in re.findall(r"^#define (TRAINER_\w+)\s+(\d+)\b", op_txt, re.M)}
    fr = {k: int(v) for k, v in re.findall(r"^#define (TRAINER_\w+)\s+(\d+)\b", le(FR), re.M)}
    party = le(PARTY)
    # bloco = do "=== TRAINER_X ===" até o próximo "===" (ou fim)
    partes = re.split(r"(?=^=== TRAINER_\w+ ===)", party, flags=re.M)
    cab, blocos = partes[0], partes[1:]
    nome = lambda b: re.match(r"=== (TRAINER_\w+) ===", b).group(1)
    cit = citados()
    cit.add("TRAINER_NONE")
    valor = lambda n: op.get(n, fr.get(n))
    antes = {valor(nome(b)) for b in blocos}
    fica_b = [b for b in blocos if nome(b) in cit]
    sai_b = [nome(b) for b in blocos if nome(b) not in cit]
    depois = {valor(nome(b)) for b in fica_b}
    sai_def = sorted(k for k in op if k not in cit and k != "TRAINER_NONE")
    maximo = 4000
    print(f"treinadores no .party de Emerald: {len(blocos)} -> {len(fica_b)} ({len(sai_b)} saem)")
    print(f"  dos que saem, com define só em opponents_frlg.h (Kanto): "
          f"{sum(1 for n in sai_b if n not in op)}")
    print(f"defines literais em opponents.h: {len(op)} -> {len(op) - len(sai_def)}")
    print(f"ids ocupados (pelo .party): {len(antes)} -> {len(depois)}; "
          f"livres de {maximo}: {maximo - len(antes)} -> {maximo - len(depois)}")
    print(f"maior id ocupado: {max(antes)} -> {max(depois)}")
    print("maiores faixas contíguas livres depois:",
          ", ".join(f"{a}..{b} ({b - a + 1})" for a, b in faixas_livres(depois, maximo)[:6]))
    if aplicar:
        open(os.path.join(RAIZ, PARTY), "w", encoding="utf-8").write(cab + "".join(fica_b))
        sai_set = set(sai_def)
        linhas = [l for l in op_txt.split("\n")
                  if not (re.match(r"#define (TRAINER_\w+)\s+\d+\b", l)
                          and re.match(r"#define (TRAINER_\w+)", l).group(1) in sai_set)]
        open(os.path.join(RAIZ, OP), "w", encoding="utf-8").write("\n".join(linhas))
        for p in ("src/data/trainers_johto.party", "src/data/trainers_sinnoh.party"):
            if os.path.exists(os.path.join(RAIZ, p)):
                os.remove(os.path.join(RAIZ, p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
