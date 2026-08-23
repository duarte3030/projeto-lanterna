#!/usr/bin/env python3
"""Base compartilhada da auditoria de ESTADO DE JOGO (flags, vars, itens, treinadores, save).

Só leitura sobre o repo. Resolve nome -> número pelo PRÉ-PROCESSADOR (lição 4.6
do ESTADO: quem resolve o valor é o cpp, não o texto do define), carrega os
`map.json` e todos os `.inc` de script uma vez só e deixa em cache no disco.
"""
import functools
import json
import os
import re
import subprocess
import sys

# RAIZ do repo, DEDUZIDA do lugar do proprio arquivo (dev_scripts/qa/x.py ->
# duas pastas acima). Ate 23/08/2026 estas ferramentas moravam fora do repo e
# cravavam o caminho absoluto do Mac do Gui; promovidas para dentro, caminho
# cravado seria mentira na primeira copia da arvore (worktree, /tmp do --demo,
# CI). A variavel de ambiente continua ganhando, que e como o --demo aponta
# para a arvore mutante.
RAIZ = os.environ.get("POKE_RAIZ", os.environ.get(
    "QA_REPO", os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))))
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")

PONTAS = ["constants/flags.h", "constants/vars.h", "constants/items.h",
          "constants/opponents.h", "constants/species.h", "constants/moves.h",
          "constants/abilities.h", "constants/event_objects.h",
          "constants/global.h", "constants/pokemon.h", "text.h"]
SONDA = re.compile(r'^@@ "(\w+)" @@ (.*)$')


def _cc():
    for cc in ("cc", "gcc", "clang"):
        if subprocess.run(["which", cc], capture_output=True).returncode == 0:
            return cc
    raise SystemExit("sem pré-processador C no PATH")


def resolve(nomes):
    """nome -> inteiro que o cpp entrega. Nome que não vira inteiro fica de fora."""
    nomes = sorted(set(nomes))
    fonte = "".join('#include "%s"\n' % h for h in PONTAS)
    fonte += "".join('@@ "%s" @@ %s\n' % (n, n) for n in nomes)
    saida = subprocess.run(
        [_cc(), "-E", "-P", "-I", os.path.join(RAIZ, "include"), "-x", "c", "-"],
        input=fonte, capture_output=True, text=True)
    if saida.returncode != 0:
        raise SystemExit("cpp reprovou:\n" + saida.stderr[:3000])
    fora = {}
    for linha in saida.stdout.splitlines():
        m = SONDA.match(linha.strip())
        if not m:
            continue
        try:
            fora[m.group(1)] = eval(m.group(2).strip(), {"__builtins__": {}}, {})
        except Exception:
            pass
    return fora


def resolve_em(inc_dir, nomes):
    """Igual a `resolve`, mas contra uma árvore de include ARBITRÁRIA.

    Serve para comparar a árvore de hoje com a de um commit antigo exportado
    por `git archive`, que é como se mede atribuição de endereço entre ROMs.
    """
    nomes = sorted(set(nomes))
    fonte = "".join('#include "%s"\n' % h for h in
                    ["constants/flags.h", "constants/vars.h",
                     "constants/global.h", "constants/pokemon.h", "text.h"])
    fonte += "".join('@@ "%s" @@ %s\n' % (n, n) for n in nomes)
    saida = subprocess.run([_cc(), "-E", "-P", "-I", inc_dir, "-x", "c", "-"],
                           input=fonte, capture_output=True, text=True)
    if saida.returncode != 0:
        raise SystemExit("cpp reprovou em %s:\n%s" % (inc_dir, saida.stderr[:2000]))
    fora = {}
    for linha in saida.stdout.splitlines():
        m = SONDA.match(linha.strip())
        if not m:
            continue
        try:
            fora[m.group(1)] = eval(m.group(2).strip(), {"__builtins__": {}}, {})
        except Exception:
            pass
    return fora


def defines(header):
    """nome -> corpo textual do ÚLTIMO #define do arquivo."""
    fora = {}
    rx = re.compile(r"^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)[ \t]+(.*)$", re.M)
    for m in rx.finditer(open(os.path.join(RAIZ, header), encoding="utf-8",
                              errors="replace").read()):
        fora[m.group(1)] = m.group(2).split("//")[0].split("/*")[0].strip()
    return fora


@functools.lru_cache(maxsize=1)
def mapas():
    """lista de (nome_da_pasta, dict do map.json)."""
    base = os.path.join(RAIZ, "data", "maps")
    fora = []
    for d in sorted(os.listdir(base)):
        p = os.path.join(base, d, "map.json")
        if os.path.isfile(p):
            try:
                fora.append((d, json.load(open(p, encoding="utf-8"))))
            except Exception as e:
                fora.append((d, {"_erro": str(e)}))
    return fora


@functools.lru_cache(maxsize=1)
def scripts():
    """lista de (caminho relativo, texto) de todo .inc de script."""
    fora = []
    # `.s` junto com `.inc`: `data/event_scripts.s` tem roteiro de verdade
    # (é ele quem faz `setvar VAR_MAP_SCENE_ROUTE16`), e deixá-lo de fora fazia
    # a var do Snorlax aparecer como "lida e nunca escrita".
    base = os.path.join(RAIZ, "data")
    for dp, _, fn in os.walk(base):
        for f in fn:
            if not f.endswith((".inc", ".s")):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, RAIZ)
            fora.append((rel, open(p, encoding="utf-8", errors="replace").read()))
    return fora


def mapa_do_script(rel):
    """`data/maps/X/scripts.inc` -> X; senão None."""
    m = re.match(r"data/maps/([^/]+)/", rel)
    return m.group(1) if m else None




# --- enums (ITEM_*, SPECIES_*, MOVE_*, TRAINER_*, OBJ_EVENT_GFX_*) ------------
# O cpp NÃO resolve membro de enum. Aqui a medida é feita COMPILANDO e RODANDO
# um programa que imprime cada nome, que é a única leitura que não chuta.
CABECALHOS_ENUM = ["constants/items.h", "constants/species.h",
                   "constants/opponents.h", "constants/moves.h",
                   "constants/abilities.h", "constants/event_objects.h",
                   "constants/opponents_frlg.h"]
# Só para COLHER nomes: `tms_hms.h` e `berries.h` já entram pelo include de
# items.h, mas os nomes de TM e HM (`ITEM_TM_SHOCK_WAVE`, `ITEM_HM_SURF`) moram
# lá, e sem varrer o arquivo eles ficavam de fora da tabela e 55 `giveitem`
# legítimos apareciam como "item que não existe".
CABECALHOS_SO_NOME = ["constants/tms_hms.h", "constants/berries.h"]


def _candidatos(prefixos):
    fora = set()
    rx = re.compile(r"\b(%s)_[A-Za-z0-9_]+" % "|".join(prefixos))
    for h in CABECALHOS_ENUM + CABECALHOS_SO_NOME:
        p = os.path.join(RAIZ, "include", h)
        if not os.path.exists(p):
            continue
        texto = open(p, encoding="utf-8", errors="replace").read()
        texto = re.sub(r"//[^\n]*", "", texto)
        texto = re.sub(r"/\*.*?\*/", "", texto, flags=re.S)
        for m in rx.finditer(texto):
            fora.add(m.group(0))
    return fora


@functools.lru_cache(maxsize=8)
def enums(prefixos=("ITEM", "SPECIES", "TRAINER", "MOVE", "ABILITY", "OBJ_EVENT_GFX"),
          extras=()):
    """nome -> valor, medido por COMPILAÇÃO nativa.

    `extras` entra para que nome citado por script possa ser testado mesmo sem
    aparecer escrito num header: `ITEM_TM_SHOCK_WAVE` nasce da macro
    `FOREACH_TM` de `constants/tms_hms.h` e não existe como texto em lugar
    nenhum. Nome que não compila fica de FORA do resultado, e é exatamente essa
    ausência que serve de prova de "não existe".
    """
    nomes = sorted(_candidatos(prefixos) | set(extras))
    import tempfile
    d = tempfile.mkdtemp(prefix="qa_enum_")

    def tenta(lista):
        c = os.path.join(d, "p.c")
        with open(c, "w") as f:
            f.write("#include <stdio.h>\n")
            for h in CABECALHOS_ENUM:
                f.write('#include "%s"\n' % h)
            f.write("int main(void){\n")
            for n in lista:
                f.write('printf("%s=%d\\n", "{0}", (int){0});\n'.format(n))
            f.write("return 0;}\n")
        b = os.path.join(d, "p")
        r = subprocess.run([_cc(), "-w", "-ferror-limit=0", "-I",
                            os.path.join(RAIZ, "include"), "-o", b, c],
                           capture_output=True, text=True)
        if r.returncode != 0:
            return None, r.stderr
        s = subprocess.run([b], capture_output=True, text=True)
        fora = {}
        for linha in s.stdout.splitlines():
            k, _, v = linha.partition("=")
            fora[k] = int(v)
        return fora, ""

    for _ in range(6):
        fora, erro = tenta(nomes)
        if fora is not None:
            return fora
        ruins = set(re.findall(r"use of undeclared identifier .(\w+).", erro))
        ruins |= set(re.findall(r".(\w+). undeclared", erro))
        if not ruins:
            raise SystemExit("probe de enum não compila e não diz o nome:\n" + erro[:2000])
        nomes = [n for n in nomes if n not in ruins]
    raise SystemExit("probe de enum não convergiu")


if __name__ == "__main__":
    print("mapas:", len(mapas()))
    print("scripts .inc:", len(scripts()))
    v = resolve(["FLAG_BADGE01_GET", "VAR_TEMP_1", "ITEM_POTION", "TRAINER_FLAGS_START"])
    print(v)
    e = enums()
    print("enums:", len(e), e.get("ITEM_POTION"), e.get("SPECIES_BULBASAUR"), e.get("TRAINER_NONE"))
