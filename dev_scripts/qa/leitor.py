#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Leitor comum dos scripts de evento do Pokémon Claude.

Não faz julgamento nenhum: só transforma os `.inc` em estruturas que os
checadores (`checa_scripts.py`, `checa_texto.py`) consomem. Fica separado
para que os dois não precisem reimplementar a mesma tokenização.

Uso como biblioteca:

    import leitor
    arv = leitor.Arvore("/caminho/do/pokeemerald-expansion")
"""

import json
import os
import re
import sys

# RAIZ do repo, DEDUZIDA do lugar do proprio arquivo (dev_scripts/qa/x.py ->
# duas pastas acima). Ate 23/08/2026 estas ferramentas moravam fora do repo e
# cravavam o caminho absoluto do Mac do Gui; promovidas para dentro, caminho
# cravado seria mentira na primeira copia da arvore (worktree, /tmp do --demo,
# CI). A variavel de ambiente continua ganhando, que e como o --demo aponta
# para a arvore mutante.
RAIZ_PADRAO = os.environ.get(
    "QA_REPO", os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))

RE_ROTULO = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)(::?)\s*$")
RE_DEFINE = re.compile(r"^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)\s+(.*)$")


def tira_comentario(linha):
    """Remove o comentário `@`, respeitando aspas simples e duplas."""
    fora = []
    aspa = None
    i = 0
    while i < len(linha):
        c = linha[i]
        if aspa:
            fora.append(c)
            if c == "\\":
                if i + 1 < len(linha):
                    fora.append(linha[i + 1])
                    i += 2
                    continue
            elif c == aspa:
                aspa = None
        else:
            if c in "\"'":
                aspa = c
                fora.append(c)
            elif c == "@":
                break
            else:
                fora.append(c)
        i += 1
    return "".join(fora)


def parte_args(texto):
    """Quebra a lista de argumentos por vírgula de topo (fora de aspas/parênteses)."""
    args = []
    atual = []
    nivel = 0
    aspa = None
    i = 0
    while i < len(texto):
        c = texto[i]
        if aspa:
            atual.append(c)
            if c == "\\" and i + 1 < len(texto):
                atual.append(texto[i + 1])
                i += 2
                continue
            if c == aspa:
                aspa = None
        elif c in "\"'":
            aspa = c
            atual.append(c)
        elif c in "([":
            nivel += 1
            atual.append(c)
        elif c in ")]":
            nivel -= 1
            atual.append(c)
        elif c == "," and nivel == 0:
            args.append("".join(atual).strip())
            atual = []
        else:
            atual.append(c)
        i += 1
    resto = "".join(atual).strip()
    if resto or args:
        args.append(resto)
    return [a for a in args if a != "" or len(args) == 1]


class Bloco(object):
    """Um rótulo e os comandos que vêm dele até o próximo rótulo."""

    __slots__ = ("rotulo", "global_", "arquivo", "linha", "cmds", "textos")

    def __init__(self, rotulo, global_, arquivo, linha):
        self.rotulo = rotulo
        self.global_ = global_
        self.arquivo = arquivo
        self.linha = linha
        self.cmds = []      # lista de (linha, nome, [args])
        self.textos = []    # lista de (linha, diretiva, conteudo_bruto)


def le_inc(caminho):
    """Devolve a lista de blocos de um arquivo `.inc`/`.s`."""
    blocos = []
    atual = None
    with open(caminho, "r", encoding="utf-8", errors="replace") as fh:
        for n, bruta in enumerate(fh, 1):
            linha = tira_comentario(bruta.rstrip("\n"))
            if not linha.strip():
                continue
            m = RE_ROTULO.match(linha.strip())
            if m and not linha.startswith((" ", "\t")):
                atual = Bloco(m.group(1), m.group(2) == "::", caminho, n)
                blocos.append(atual)
                continue
            corpo = linha.strip()
            if atual is None:
                atual = Bloco("<preambulo:%s>" % os.path.basename(caminho),
                              False, caminho, n)
                blocos.append(atual)
            pedacos = corpo.split(None, 1)
            nome = pedacos[0]
            resto = pedacos[1] if len(pedacos) > 1 else ""
            if nome.startswith("."):
                if nome in (".string", ".asciz", ".ascii"):
                    atual.textos.append((n, nome, resto))
                atual.cmds.append((n, nome, parte_args(resto) if resto else []))
            else:
                atual.cmds.append((n, nome, parte_args(resto) if resto else []))
    return blocos


def le_defines(caminho):
    """#define NOME VALOR de um header C, sem expandir macro com argumento."""
    out = {}
    if not os.path.exists(caminho):
        return out
    with open(caminho, "r", encoding="utf-8", errors="replace") as fh:
        for linha in fh:
            m = RE_DEFINE.match(linha)
            if not m:
                continue
            nome, valor = m.group(1), m.group(2).split("//")[0].split("/*")[0].strip()
            if "(" in nome:
                continue
            out[nome] = valor
    return out


def resolve_num(txt, defines, prof=0):
    """Tenta virar inteiro, seguindo #define encadeado. None se não der."""
    if txt is None or prof > 12:
        return None
    t = txt.strip()
    if not t:
        return None
    try:
        return int(t, 0)
    except ValueError:
        pass
    if t in defines:
        return resolve_num(defines[t], defines, prof + 1)
    m = re.match(r"^\(\s*(.*)\s*\)$", t)
    if m:
        return resolve_num(m.group(1), defines, prof + 1)
    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\+\s*(.+)$", t)
    if m:
        a = resolve_num(m.group(1), defines, prof + 1)
        b = resolve_num(m.group(2), defines, prof + 1)
        if a is not None and b is not None:
            return a + b
    return None


GRUPO_REGIAO = [
    ("Sinnoh", ("Sinnoh", "TeamGalactic", "SinnohLeague", "SinnohCavernas",
                "SinnohInteriores", "SinnohTownsRoutes", "SpecialAreasSinnoh",
                "DungeonsSinnoh", "IndoorTwinleaf", "IndoorSandgem",
                "IndoorJubilife", "IndoorOreburgh", "IndoorFloaroma")),
    ("Unova", ("Unova",)),
    ("Johto", ("Johto",)),
    ("Kanto", ("Frlg",)),
]


class Arvore(object):
    def __init__(self, raiz=RAIZ_PADRAO):
        self.raiz = raiz
        self.blocos = {}          # rotulo -> Bloco (o primeiro achado)
        self.blocos_dup = {}      # rotulo -> [Bloco, ...]
        self.arquivos = {}        # caminho -> [Bloco]
        self.mapa_do_arquivo = {}  # caminho -> nome do mapa (ou None)
        self.mapas = {}           # nome do mapa -> json
        self.regiao = {}          # nome do mapa -> regiao
        self._carrega_scripts()
        self._carrega_mapas()
        self._carrega_constantes()

    # ------------------------------------------------------------------ carga
    def _arquivos_de_script(self):
        alvo = []
        d = os.path.join(self.raiz, "data", "maps")
        for nome in sorted(os.listdir(d)):
            p = os.path.join(d, nome, "scripts.inc")
            if os.path.exists(p):
                alvo.append((p, nome))
        for extra in ("data/event_scripts.s",):
            pe = os.path.join(self.raiz, extra)
            if os.path.exists(pe):
                alvo.append((pe, None))
        for base in ("data/scripts", "data/text"):
            db = os.path.join(self.raiz, base)
            for dirp, _, arqs in os.walk(db):
                for a in sorted(arqs):
                    if a.endswith(".inc"):
                        alvo.append((os.path.join(dirp, a), None))
        return alvo

    def _carrega_scripts(self):
        for caminho, mapa in self._arquivos_de_script():
            blocos = le_inc(caminho)
            self.arquivos[caminho] = blocos
            self.mapa_do_arquivo[caminho] = mapa
            for b in blocos:
                self.blocos_dup.setdefault(b.rotulo, []).append(b)
                self.blocos.setdefault(b.rotulo, b)

    def _carrega_mapas(self):
        gp = os.path.join(self.raiz, "data", "maps", "map_groups.json")
        grupos = json.load(open(gp))
        do_grupo = {}
        for g in grupos.get("group_order", []):
            for m in grupos.get(g, []):
                do_grupo[m] = g
        d = os.path.join(self.raiz, "data", "maps")
        for nome in sorted(os.listdir(d)):
            p = os.path.join(d, nome, "map.json")
            if not os.path.exists(p):
                continue
            try:
                self.mapas[nome] = json.load(open(p))
            except Exception:
                continue
            g = do_grupo.get(nome, "")
            if nome.startswith("Galar_"):
                self.regiao[nome] = "Galar"
                continue
            reg = "Hoenn"
            for r, chaves in GRUPO_REGIAO:
                if any(k in g for k in chaves):
                    reg = r
                    break
            self.regiao[nome] = reg

    def _carrega_constantes(self):
        inc = os.path.join(self.raiz, "include")
        self.defines = {}
        for sub in ("constants", ""):
            d = os.path.join(inc, sub) if sub else inc
            if not os.path.isdir(d):
                continue
            arqs = sorted(os.listdir(d))
            ordem = [a for a in arqs if "_frlg" in a] + \
                    [a for a in arqs if "_frlg" not in a]
            for a in ordem:
                if a.endswith(".h"):
                    self.defines.update(le_defines(os.path.join(d, a)))
        # specials
        self.specials = set()
        sp = os.path.join(self.raiz, "data", "specials.inc")
        if os.path.exists(sp):
            for linha in open(sp, encoding="utf-8", errors="replace"):
                m = re.match(r"\s*def_special\s+([A-Za-z_][A-Za-z0-9_]*)", linha)
                if m:
                    self.specials.add(m.group(1))

    # ------------------------------------------------------------- utilidades
    ARQUIVO_REGIAO = [("galar_", "Galar"), ("sinnoh_", "Sinnoh"),
                      ("unova", "Unova"), ("johto", "Johto"),
                      ("_frlg", "Kanto"), ("sinnoh", "Sinnoh")]

    def regiao_do_arquivo(self, caminho):
        m = self.mapa_do_arquivo.get(caminho)
        if m:
            return self.regiao.get(m, "Hoenn")
        base = os.path.basename(caminho)
        for pedaco, reg in self.ARQUIVO_REGIAO:
            if pedaco in base:
                return reg
        return "comum"

    def objetos_do_mapa(self, nome):
        j = self.mapas.get(nome)
        if not j:
            return []
        return j.get("object_events", []) or []


if __name__ == "__main__":
    raiz = sys.argv[1] if len(sys.argv) > 1 else RAIZ_PADRAO
    arv = Arvore(raiz)
    print("arquivos    :", len(arv.arquivos))
    print("blocos      :", sum(len(v) for v in arv.arquivos.values()))
    print("rotulos     :", len(arv.blocos))
    print("mapas       :", len(arv.mapas))
    print("defines     :", len(arv.defines))
    print("specials    :", len(arv.specials))
    from collections import Counter
    print("por regiao  :", Counter(arv.regiao.values()))
