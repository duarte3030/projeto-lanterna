#!/usr/bin/env python3
"""Traz as placas de Johto do hns, com o script e o texto de cada uma.

Johto entrou na ROM com 34 das 502 placas do original (6,8%). Os letreiros,
avisos de rota, caixas de correio e o "a porta esta trancada" nunca vieram: a
importacao original trouxe mapa, warp e objeto, e parou ai.

O que este script NAO faz, de proposito: ele nao inventa texto e nao aceita
placa cujo script dependa de algo que este repo nao tem. Placa que fala de
evento inexistente e pior que placa nenhuma, porque parece conteudo e nao e.
Por isso todo bloco passa por tres portoes antes de entrar:

  1. todo comando usado existe em asm/macros/ (o hns tem macro propria)
  2. toda CONSTANTE usada existe nos nossos include/ (FLAG_, VAR_, ITEM_...)
  3. todo label referenciado ou ja existe aqui, ou vem junto no mesmo pacote

Placa que reprova em qualquer um fica de fora e sai no relatorio.

Uso:
    python3 dev_scripts/importa_placas_johto.py            # so relata
    python3 dev_scripts/importa_placas_johto.py --aplica   # escreve
"""
import json
import os
import re
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HNS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/hns"
APLICA = "--aplica" in sys.argv

# ---------------------------------------------------------------- vocabulario

def le(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def macros_disponiveis():
    m = set()
    for raiz, _, arqs in os.walk(f"{REPO}/asm/macros"):
        for a in arqs:
            m |= set(re.findall(r"^\s*\.macro\s+([A-Za-z_][\w]*)",
                                le(os.path.join(raiz, a)), re.M))
    # diretivas do montador, que nao sao macro nossa
    m |= {".string", ".byte", ".2byte", ".4byte", ".align", ".include",
          ".string_ja", ".ifdef", ".endif", ".else", ".ifndef", ".set"}
    return m


def constantes_definidas():
    """Tudo que os include/ definem: #define, enum e constantes de asm."""
    c = set()
    for raiz, _, arqs in os.walk(f"{REPO}/include"):
        for a in arqs:
            s = le(os.path.join(raiz, a))
            c |= set(re.findall(r"^\s*#\s*define\s+([A-Z_][A-Z0-9_]*)", s, re.M))
            c |= set(re.findall(r"^\s*([A-Z_][A-Z0-9_]{3,})\s*[,=]", s, re.M))
    for raiz, _, arqs in os.walk(f"{REPO}/asm/macros"):
        for a in arqs:
            s = le(os.path.join(raiz, a))
            c |= set(re.findall(r"^\s*\.set\s+([A-Z_][A-Z0-9_]*)", s, re.M))
            # ponytail: MSGBOX_SIGN e companhia sao `NOME = 3` dentro do macro,
            # nao #define. Sem esta linha o portao 2 recusava toda placa do
            # jogo, que e exatamente o caso comum.
            c |= set(re.findall(r"^\s*([A-Z_][A-Z0-9_]{3,})\s*=", s, re.M))
    return c


# ------------------------------------------------------------------- parsing

# ponytail: parser de bloco, nao de assembly. Um label no comeco da linha abre
# bloco e vai ate o proximo label. Basta para o que este script faz, e o
# portao 1 recusa qualquer coisa que ele nao tenha entendido.
LABEL = re.compile(r"^([A-Za-z_][\w]*)::?\s*$")


def blocos(texto):
    """label -> lista de linhas do corpo (sem a linha do proprio label)."""
    out, atual = {}, None
    for linha in texto.split("\n"):
        m = LABEL.match(linha)
        if m:
            atual = m.group(1)
            out[atual] = []
        elif atual is not None:
            out[atual].append(linha)
    return out


def simbolos_do_repo():
    """Todo label ja definido nos nossos data/ e src/ de script."""
    s = set()
    for raiz, _, arqs in os.walk(f"{REPO}/data"):
        for a in arqs:
            if a.endswith((".inc", ".s")):
                s |= set(re.findall(r"^([A-Za-z_][\w]*)::?\s*$",
                                    le(os.path.join(raiz, a)), re.M))
    return s


SPECIALS = set(re.findall(r"^\s*def_special\s+(\w+)",
                          le(f"{REPO}/data/specials.inc"), re.M))

PALAVRA = re.compile(r"[A-Za-z_][\w]*")


def special_faltando(linhas):
    """`special NameRival` monta para SPECIAL_NameRival, que nao existe aqui, e
    o erro sai como '.if nao constante' dentro do macro, longe da causa."""
    for l in linhas:
        m = re.match(r"\s*special(?:var)?\s+(?:\w+\s*,\s*)?(\w+)", l.split("@")[0])
        if m and m.group(1) not in SPECIALS:
            return m.group(1)
    return None


def refs(linhas):
    """Identificadores citados no corpo, fora de string literal."""
    fora = []
    for l in linhas:
        l = re.sub(r'"(\\.|[^"\\])*"', " ", l)  # tira o texto entre aspas
        l = l.split("@")[0]
        fora.append(l)
    return set(PALAVRA.findall("\n".join(fora)))


def comandos(linhas):
    c = set()
    for l in linhas:
        l = l.split("@")[0].strip()
        if l and not LABEL.match(l + "\n"):
            c.add(l.split()[0].rstrip(":"))
    return c


# --------------------------------------------------------------------- coleta

MACROS = macros_disponiveis()
CONSTS = constantes_definidas()
NOSSOS = simbolos_do_repo()

# Indice global do hns: placa de um mapa cita script de outro com frequencia
# (a porta de BellchimeTrail usa o texto de Route7). Sem isto, 183 placas
# caiam por "label ausente" so porque o bloco morava no vizinho.
GLOBAL = {}
for _m in sorted(os.listdir(f"{HNS}/data/maps")):
    _p = f"{HNS}/data/maps/{_m}/scripts.inc"
    if os.path.exists(_p):
        for _lab, _corpo in blocos(le(_p)).items():
            GLOBAL.setdefault(_lab, _corpo)

grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
mapas = sorted({m for g, v in grupos.items()
                if g.endswith("_Johto") for m in v})

motivos = Counter()
recusadas = []
EMITIDOS = set()
plano = []  # (mapa, [bg novos], texto a acrescentar em scripts.inc)

for mapa in mapas:
    fonte_json = f"{HNS}/data/maps/{mapa}/map.json"
    nosso_json = f"{REPO}/data/maps/{mapa}/map.json"
    if not (os.path.exists(fonte_json) and os.path.exists(nosso_json)):
        continue
    fonte = json.load(open(fonte_json))
    nosso = json.load(open(nosso_json))
    faltam = [b for b in fonte.get("bg_events", [])
              if not any(n["x"] == b["x"] and n["y"] == b["y"]
                         for n in nosso.get("bg_events", []))]
    if not faltam:
        continue

    fonte_inc = f"{HNS}/data/maps/{mapa}/scripts.inc"
    bl = dict(GLOBAL)
    if os.path.exists(fonte_inc):
        bl.update(blocos(le(fonte_inc)))  # o do proprio mapa manda

    novos, precisa = [], set()
    for b in faltam:
        alvo = b.get("script", "0")
        if alvo in ("0", "NULL", ""):
            motivos["placa sem script"] += 1
            continue
        # fecho transitivo do que a placa precisa e que ainda nao temos
        pendentes, pacote, erro = [alvo], set(), None
        while pendentes:
            lab = pendentes.pop()
            if lab in pacote or lab in NOSSOS or lab in EMITIDOS:
                continue
            if lab not in bl:
                erro = f"label ausente: {lab}"
                break
            pacote.add(lab)
            corpo = bl[lab]
            desconhecido = comandos(corpo) - MACROS
            if desconhecido:
                erro = f"comando fora dos macros: {sorted(desconhecido)[0]}"
                break
            sp = special_faltando(corpo)
            if sp:
                erro = f"special inexistente: {sp}"
                break
            for r in refs(corpo):
                if r in bl:
                    pendentes.append(r)
                elif r.isupper() and len(r) > 3 and r not in CONSTS \
                        and r not in NOSSOS and not r.isdigit():
                    erro = f"constante inexistente: {r}"
                    break
            if erro:
                break
        if erro:
            motivos[erro.split(":")[0]] += 1
            recusadas.append(f"{mapa}/{alvo}: {erro}")
            continue
        novos.append(b)
        precisa |= pacote

    if not novos:
        continue
    # ponytail: `::` (global) em tudo, inclusive texto. Um mesmo bloco pode ser
    # puxado por dois mapas; o segundo nao redefine, so aponta para o primeiro,
    # e label local nao atravessa arquivo.
    trecho = ""
    novos_labels = [l for l in sorted(precisa) if l not in EMITIDOS]
    if novos_labels:
        trecho = "\n@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py\n"
        for lab in novos_labels:
            EMITIDOS.add(lab)
            trecho += f"\n{lab}::\n" + "\n".join(bl[lab]).rstrip() + "\n"
    plano.append((mapa, novos, trecho))

total = sum(len(n) for _, n, _ in plano)
print(f"mapas tocados: {len(plano)}   placas novas: {total}")
if motivos:
    print("recusadas:", dict(motivos))
    for r in recusadas[:12]:
        print("   ", r)

if not APLICA:
    print("\n(nada escrito; rode com --aplica)")
    sys.exit(0)

for mapa, novos, trecho in plano:
    p = f"{REPO}/data/maps/{mapa}/map.json"
    d = json.load(open(p))
    d.setdefault("bg_events", []).extend(novos)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if trecho:
        with open(f"{REPO}/data/maps/{mapa}/scripts.inc", "a",
                  encoding="utf-8") as f:
            f.write(trecho)
print(f"escrito: {total} placas em {len(plano)} mapas")
