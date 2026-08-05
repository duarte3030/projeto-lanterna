#!/usr/bin/env python3
"""Gera os treinadores de rota/caverna/predio de Unova a partir do BW3G.

Escreve tres coisas, todas so ACRESCENTANDO:
  include/constants/opponents.h   constantes TRAINER_UNOVA_* a partir de 1800
  src/data/trainers.party         um bloco `=== TRAINER_X ===` para CADA constante
  dev_scripts/importa_unova.py    a tabela TREINADORES, no molde da LIDERES

Roda de novo sem duplicar: cada destino tem marcador proprio e o trecho antigo e
substituido inteiro.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BW3G = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/bw3g"
BASE_ID = 1800
TETO_ID = 2199
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

MARCA_INI = "# >>> TREINADORES DE UNOVA (gerado) >>>"
MARCA_FIM = "# <<< TREINADORES DE UNOVA (gerado) <<<"

# Classe do BW3G -> (classe, retrato, sexo) desta build. O gen 3 nao tem as
# classes de gen 5, entao cada uma cai na mais parecida em papel e visual; a
# lista das trocas vai no relatorio. Sufixo _D e _T do BW3G sao a MESMA classe
# com outro grupo de times (variante de dia/noite), entao caem na mesma linha.
CLASSE = {
    "YOUNGSTER":     ("Youngster", "Youngster", "Male"),
    "LASS":          ("Lass", "Lass", "Female"),
    "ACE_TRAINERM":  ("Cooltrainer", "Cooltrainer M", "Male"),
    "ACE_TRAINERF":  ("Cooltrainer", "Cooltrainer F", "Female"),
    "ARTIST":        ("TRAINER_CLASS_PAINTER_FRLG", "TRAINER_PIC_PAINTER_FRLG", "Female"),
    "BACKERSM":      ("Pokefan", "Pokefan M", "Male"),
    "BACKERSF":      ("Pokefan", "Pokefan F", "Female"),
    "BACKPACKERM":   ("Camper", "Camper", "Male"),
    "BACKPACKERF":   ("Picnicker", "Picnicker", "Female"),
    "BAKER":         ("Kindler", "Kindler", "Male"),
    "BLACKBELT":     ("Black Belt", "Black Belt", "Male"),
    "BATTLE_GIRL":   ("Battle Girl", "Battle Girl", "Female"),
    "BIKER":         ("TRAINER_CLASS_BIKER_FRLG", "TRAINER_PIC_BIKER_FRLG", "Male"),
    "ROUGHNECK":     ("TRAINER_CLASS_CUE_BALL_FRLG", "TRAINER_PIC_CUE_BALL_FRLG", "Male"),
    "CYCLISTM":      ("Triathlete", "Cycling Triathlete M", "Male"),
    "CYCLISTF":      ("Triathlete", "Cycling Triathlete F", "Female"),
    "DANCER":        ("Beauty", "Beauty", "Female"),
    "DEPOT_AGENT":   ("Gentleman", "Gentleman", "Male"),
    "DOCTOR":        ("TRAINER_CLASS_SCIENTIST_FRLG", "TRAINER_PIC_SCIENTIST_FRLG", "Male"),
    "NURSE":         ("Lady", "Lady", "Female"),
    "FISHER":        ("Fisherman", "Fisherman", "Male"),
    "GENTLEMAN":     ("Gentleman", "Gentleman", "Male"),
    "GUITARIST":     ("Guitarist", "Guitarist", "Male"),
    "HARLEQUIN":     ("TRAINER_CLASS_JUGGLER_FRLG", "TRAINER_PIC_JUGGLER_FRLG", "Male"),
    "HEX_MANIAC":    ("Hex Maniac", "Hex Maniac", "Female"),
    "HIKER":         ("Hiker", "Hiker", "Male"),
    "HOOPSTER":      ("Black Belt", "Black Belt", "Male"),
    "JANITOR":       ("TRAINER_CLASS_ENGINEER_FRLG", "TRAINER_PIC_ENGINEER_FRLG", "Male"),
    "LADY":          ("Lady", "Lady", "Female"),
    "LINEBACKER":    ("Black Belt", "Black Belt", "Male"),
    "MAID":          ("Parasol Lady", "Parasol Lady", "Female"),
    "MUSICIAN":      ("Guitarist", "Guitarist", "Male"),
    "NURSERY_AIDE":  ("Pkmn Breeder", "Pokemon Breeder F", "Female"),
    "PARASOL_LADY":  ("Parasol Lady", "Parasol Lady", "Female"),
    "PILOT":         ("Sailor", "Sailor", "Male"),
    "POKEFANM":      ("Pokefan", "Pokefan M", "Male"),
    "POKEFANF":      ("Pokefan", "Pokefan F", "Female"),
    "PKMN_BREEDERM": ("Pkmn Breeder", "Pokemon Breeder M", "Male"),
    "PKMN_BREEDERF": ("Pkmn Breeder", "Pokemon Breeder F", "Female"),
    "PKMN_RANGERM":  ("Pkmn Ranger", "Pokemon Ranger M", "Male"),
    "PKMN_RANGERF":  ("Pkmn Ranger", "Pokemon Ranger F", "Female"),
    "POLICEMAN":     ("Expert", "Expert M", "Male"),
    "PRESCHOOLERM":  ("Ninja Boy", "Ninja Boy", "Male"),
    "PRESCHOOLERF":  ("Tuber F", "Tuber F", "Female"),
    "PSYCHICM":      ("Psychic", "Psychic M", "Male"),
    "PSYCHICF":      ("Psychic", "Psychic F", "Female"),
    "RICH_BOY":      ("Rich Boy", "Rich Boy", "Male"),
    "SCHOOL_KIDM":   ("School Kid", "School Kid M", "Male"),
    "SCHOOL_KIDF":   ("School Kid", "School Kid F", "Female"),
    "SCIENTISTM":    ("TRAINER_CLASS_SCIENTIST_FRLG", "TRAINER_PIC_SCIENTIST_FRLG", "Male"),
    "SCIENTISTF":    ("TRAINER_CLASS_SCIENTIST_FRLG", "TRAINER_PIC_SCIENTIST_FRLG", "Female"),
    "SMASHER":       ("Battle Girl", "Battle Girl", "Female"),
    "SOCIALITE":     ("Beauty", "Beauty", "Female"),
    "SWIMMERM":      ("Swimmer M", "Swimmer M", "Male"),
    "SWIMMERF":      ("Swimmer F", "Swimmer F", "Female"),
    "TWINS":         ("Twins", "Twins", "Female"),
    "VETERANM":      ("Expert", "Expert M", "Male"),
    "VETERANF":      ("Expert", "Expert F", "Female"),
    "WORKER":        ("TRAINER_CLASS_ENGINEER_FRLG", "TRAINER_PIC_ENGINEER_FRLG", "Male"),
    # Time Plasma. Nao ha classe de Plasma nesta build; os grunts e os sabios
    # caem na equipe vila generica que existe (Rocket do FRLG) e em Expert.
    "GRUNTM":        ("TRAINER_CLASS_TEAM_ROCKET_FRLG", "TRAINER_PIC_ROCKET_GRUNT_M_FRLG", "Male"),
    "GRUNTF":        ("TRAINER_CLASS_TEAM_ROCKET_FRLG", "TRAINER_PIC_ROCKET_GRUNT_F_FRLG", "Female"),
    "GIALLO":        ("Expert", "Expert M", "Male"),
    "RYOKU":         ("Expert", "Expert M", "Male"),
    "BRONIUS":       ("Expert", "Expert M", "Male"),
    "GORM":          ("Expert", "Expert M", "Male"),
}


def classe_base(c):
    for suf in ("_D", "_T"):
        if c.endswith(suf) and c[:-len(suf)] in CLASSE:
            return c[:-len(suf)]
    return c


# ---------------------------------------------------------------- leitura


def le_classes():
    """CLASSE do BW3G -> [const, ...] na ordem em que o grupo de times os numera."""
    saida, atual = {}, None
    for ln in open(f"{BW3G}/constants/trainer_constants.asm"):
        m = re.match(r"\s*trainerclass\s+(\w+)", ln)
        if m:
            atual = saida.setdefault(m.group(1), [])
            continue
        m = re.match(r"\s*const\s+(\w+)", ln)
        if m and atual is not None:
            atual.append(m.group(1))
    return saida


def le_times():
    """rotulo `XGroup` -> [ {nome, mons:[{nivel, especie}]} ] na ordem do arquivo."""
    saida, cur = {}, None
    for ln in open(f"{BW3G}/data/trainers/parties.asm"):
        m = re.match(r"^(\w+Group):", ln)
        if m:
            cur = saida.setdefault(m.group(1), [])
            continue
        if cur is None:
            continue
        m = re.match(r'\s*db\s+"([^"]*)@",\s*(TRAINERTYPE_\w+)', ln)
        if m:
            cur.append(dict(nome=m.group(1), tipo=m.group(2), mons=[]))
            continue
        if not cur:
            continue
        m = re.match(r"\s*db\s+(\d+),\s*([A-Z][A-Z0-9_]*)\s*(;.*)?$", ln)
        if m:
            cur[-1]["mons"].append((int(m.group(1)), m.group(2)))
    return saida


def grupo_de(classe, times):
    k = classe.replace("_", "").lower()
    for g in times:
        gk = g[:-len("Group")].lower()
        if gk == k or (k.endswith("t") and gk == k[:-1]):
            return g
    return None


def le_objetos(idx, mapas):
    """[ {mapa, script, raio, classe, const, visto, perde} ] dos mapas gerados."""
    re_obj = re.compile(r"\s*object_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),\s*(\w+),\s*(-?\d+),"
                        r"\s*(-?\d+),\s*(-?\w+),\s*(-?\w+),\s*(\w+),\s*OBJECTTYPE_(\w*),"
                        r"\s*(-?\w+),\s*(\w+)")
    re_trn = re.compile(r"\s*trainer\s+(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+),")
    saida = []
    for camel in sorted(mapas):
        p = idx.get(camel)
        if not p:
            continue
        asm = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(rf"^{camel}_MapEvents:", asm, re.M)
        if not m:
            continue
        for ln in asm[m.end():].splitlines():
            mo = re_obj.match(ln)
            if not mo or mo.group(10) != "TRAINER":
                continue
            script = mo.group(12)
            ms = re.search(rf"^{script}:+\s*$", asm, re.M)
            if not ms:
                continue
            mt = None
            for l2 in asm[ms.end():].splitlines()[:6]:
                if re.match(r"^\w+:", l2):
                    break
                mt = re_trn.match(l2)
                if mt:
                    break
            if not mt:
                continue
            saida.append(dict(mapa=camel, script=script, raio=mo.group(11),
                              classe=mt.group(1), const=mt.group(2),
                              visto=mt.group(4), perde=mt.group(5)))
    return saida


# ---------------------------------------------------------------- escrita


def troca_bloco(texto, ini, fim, novo):
    i, f = texto.find(ini), texto.find(fim)
    if i >= 0 and f > i:
        return texto[:i] + novo + texto[f + len(fim):]
    return None


def main():
    classes = le_classes()
    times = le_times()
    mapas = {d[len("Unova_"):] for d in os.listdir(f"{RAIZ}/data/maps") if d.startswith("Unova_")}

    import importa_unova as iu
    idx = iu.indice_asm()
    objs = le_objetos(idx, mapas)

    # id por (classe, const): dois objetos podem apontar para o MESMO treinador
    # (as gemeas do BW3G sao dois sprites e um time so), e nesse caso dividem id.
    pares = sorted({(o["classe"], o["const"]) for o in objs})
    if len(pares) > TETO_ID - BASE_ID + 1:
        raise SystemExit(f"{len(pares)} treinadores nao cabem em {BASE_ID}..{TETO_ID}")
    id_de = {p: BASE_ID + i for i, p in enumerate(pares)}
    nome_de = {p: "TRAINER_UNOVA_" + p[1] for p in pares}
    if len(set(nome_de.values())) != len(nome_de):
        raise SystemExit("constante de treinador repetida")

    # ------- constantes
    p = f"{RAIZ}/include/constants/opponents.h"
    s = open(p).read()
    ini_h = "// >>> treinadores de rota de Unova (gerado) >>>"
    fim_h = "// <<< treinadores de rota de Unova (gerado) <<<"
    velho = troca_bloco(s, ini_h, fim_h, "")
    if velho is not None:
        # sem isto cada rodada deixa uma linha em branco a mais empilhada aqui
        s = re.sub(r"\n{3,}(#define TRAINERS_COUNT_EMERALD)", r"\n\n\1", velho)
    ja = set(re.findall(r"^#define (TRAINER_[A-Z0-9_]+)\s", s, re.M))
    colide = [n for n in nome_de.values() if n in ja]
    if colide:
        raise SystemExit(f"constante ja existe: {colide[:5]}")
    linhas = ["", ini_h,
              "// Treinadores de rota, caverna e predio de Unova (BW3G, de Azure_Keys).",
              "// Gerados por dev_scripts/gera_treinadores_unova.py na faixa 1800..2199, que e a",
              "// reservada para Unova. CADA um destes tem bloco proprio em",
              "// src/data/trainers.party: constante sem bloco nao e treinador, e apelido",
              "// do id de outra pessoa, e o jogo entrega o time errado sem avisar."]
    for pr in pares:
        linhas.append(f"#define {nome_de[pr]:<52} {id_de[pr]}")
    linhas += [fim_h, ""]
    alvo = "#define TRAINERS_COUNT_EMERALD"
    i = s.index(alvo)
    s = s[:i] + "\n".join(linhas) + "\n" + s[i:]
    # o teto declarado tem que cobrir o maior id em uso
    s = re.sub(r"^#define TRAINERS_COUNT_EMERALD\s+\d+",
               f"#define TRAINERS_COUNT_EMERALD     {max(id_de.values()) + 1}", s, count=1, flags=re.M)
    open(p, "w").write(s)

    # ------- times
    blocos = []
    faltando = []
    for pr in pares:
        cl, co = pr
        g = grupo_de(cl, times)
        lst = classes.get(cl, [])
        if not g or co not in lst or lst.index(co) >= len(times[g]):
            faltando.append(pr)
            continue
        t = times[g][lst.index(co)]
        base = classe_base(cl)
        if base not in CLASSE:
            faltando.append(pr)
            continue
        gclass, gpic, sexo = CLASSE[base]
        b = [f"=== {nome_de[pr]} ===",
             f"Name: {t['nome'] or 'TRAINER'}",
             f"Class: {gclass}", f"Pic: {gpic}", f"Gender: {sexo}",
             "Double Battle: No"]
        for nivel, esp in t["mons"]:
            b += ["", f"SPECIES_{esp}", f"Level: {nivel}"]
        blocos.append("\n".join(b))
    if faltando:
        raise SystemExit(f"sem time ou sem classe: {faltando[:10]}")

    p = f"{RAIZ}/src/data/trainers.party"
    s = open(p).read().rstrip("\n")
    # O corte e pelo SENTINELA sozinho, nunca pelo texto do comentario: mudar uma
    # palavra da descricao ja fez esta rodada nao achar o trecho antigo e anexar
    # uma SEGUNDA copia dos 348 blocos, o que o gcc so acusou la no fim com
    # "initialized field overwritten". O sentinela nao muda nunca.
    marca = "/* >>> treinadores de rota de Unova (gerado) >>> */"
    if marca in s:
        s = s[:s.index(marca)].rstrip("\n")
    cab = (f"\n\n{marca}\n"
           "/* Treinadores de rota, caverna e predio de Unova (BW3G, de Azure_Keys).\n"
           "   Gerado por dev_scripts/gera_treinadores_unova.py; um bloco por constante da\n"
           "   faixa 1800..2199, porque constante sem bloco vira apelido do id alheio. */\n")
    s += cab + "\n" + "\n\n".join(blocos) + "\n"
    open(p, "w").write(s)

    # ------- tabela no importador
    por_script = {}
    for o in objs:
        pr = (o["classe"], o["const"])
        por_script[(o["mapa"], o["script"])] = (nome_de[pr], o["visto"], o["perde"], o["raio"])
    linhas = [MARCA_INI,
              "# Treinadores de rota, caverna e predio: mesmo molde da LIDERES acima, so",
              "# que gerado por dev_scripts/gera_treinadores_unova.py a partir do macro",
              "# `trainer CLASSE, ID, EVENTO, VistoText, VenceText, ...` do BW3G. A chave e",
              "# (mapa, rotulo do script do objeto OBJECTTYPE_TRAINER); dois objetos podem",
              "# apontar para o mesmo treinador (as gemeas), e ai dividem o id de proposito.",
              "# O ultimo campo e o raio de visao lido do proprio object_event.",
              "TREINADORES = {"]
    for (mp, sc) in sorted(por_script):
        tr, vi, pe, ra = por_script[(mp, sc)]
        linhas.append(f'    ("{mp}", "{sc}"):')
        linhas.append(f'        ("{tr}", "{vi}", "{pe}", {ra}),')
    linhas += ["}", MARCA_FIM]
    bloco = "\n".join(linhas) + "\n"

    p = f"{RAIZ}/dev_scripts/importa_unova.py"
    s = open(p).read()
    novo = troca_bloco(s, MARCA_INI, MARCA_FIM, bloco.rstrip("\n"))
    if novo is None:
        alvo = "\ndef script_lider("
        s = s.replace(alvo, "\n" + bloco + "\n" + alvo.lstrip("\n"), 1)
    else:
        s = novo
    open(p, "w").write(s)

    print(f"objetos treinador: {len(objs)}")
    print(f"treinadores distintos: {len(pares)}  ids {BASE_ID}..{max(id_de.values())}")
    print(f"blocos em trainers.party: {len(blocos)}")
    print(f"entradas na TREINADORES: {len(por_script)}")


def confere():
    """Le o que esta GRAVADO e afirma as tres coisas que o compilador nao afirma.

    A do meio e a que custou caro no projeto: constante de treinador sem bloco em
    trainers.party nao da erro nenhum, ela vira apelido do id de outra pessoa e o
    jogo entrega o time errado calado. As outras duas pegam id fora da faixa
    reservada e especie que nao existe nesta build (essa so estouraria no `ld`,
    com a regiao inteira ja gerada).
    """
    import glob
    party = open(f"{RAIZ}/src/data/trainers.party").read()
    blocos = re.findall(r"^=== (TRAINER_[A-Z0-9_]+) ===", party, re.M)
    # so o trecho que ESTE script gera: os 13 chefes (1367..1379) entraram antes,
    # em outra faixa, e nao sao assunto daqui
    op = open(f"{RAIZ}/include/constants/opponents.h").read()
    i = op.index("// >>> treinadores de rota de Unova (gerado) >>>")
    f = op.index("// <<< treinadores de rota de Unova (gerado) <<<")
    ids = dict(re.findall(r"^#define (TRAINER_UNOVA_[A-Z0-9_]+)\s+(\d+)\s*$", op[i:f], re.M))
    usados = set()
    for a in glob.glob(f"{RAIZ}/data/maps/Unova_*/scripts.inc"):
        usados |= set(re.findall(r"\bTRAINER_[A-Z0-9_]+\b", open(a, errors="ignore").read()))

    repetidos = {b for b in blocos if blocos.count(b) > 1}
    assert not repetidos, f"bloco repetido em trainers.party: {sorted(repetidos)[:5]}"

    sem_bloco = sorted(u for u in usados if u not in set(blocos))
    assert not sem_bloco, f"treinador sem time proprio (vira apelido): {sem_bloco[:5]}"

    fora = sorted(n for n, v in ids.items() if not BASE_ID <= int(v) <= TETO_ID)
    assert not fora, f"id fora de {BASE_ID}..{TETO_ID}: {fora[:5]}"

    esp = set(re.findall(r"\b(SPECIES_[A-Z0-9_]+)\b",
                         open(f"{RAIZ}/include/constants/species.h").read()))
    citadas = set(re.findall(r"^(SPECIES_[A-Z0-9_]+)$", party, re.M))
    assert citadas <= esp, f"especie inexistente: {sorted(citadas - esp)[:5]}"

    print(f"ok: {len(blocos)} blocos, {len(ids)} constantes de Unova em "
          f"{BASE_ID}..{TETO_ID}, {len(usados)} usadas por mapa, todas com time proprio")


if __name__ == "__main__":
    if "--conferir" in sys.argv:
        confere()
    else:
        main()
