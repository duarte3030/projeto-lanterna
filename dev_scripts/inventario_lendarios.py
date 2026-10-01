#!/usr/bin/env python3
"""Inventário MEDIDO de todo lendário, mítico, sublendário e ultra-fera do cartucho 1.

    python3 dev_scripts/inventario_lendarios.py            # tabela TSV no stdout
    python3 dev_scripts/inventario_lendarios.py --guarda   # portão: nível 50..100 e nenhum em cidade
    python3 dev_scripts/inventario_lendarios.py --demo     # autoteste com mutação plantada

Regra do Gui de 01/10/2026 (respostas 111 e 112, ESTADO 0.ar): todo lendário,
mítico e ultra-fera encontrável ou dado de presente no cartucho 1 tem nível
entre 50 e 100, e nenhum mora em mapa de cidade. Os times de líder da Fase F
NÃO entram aqui: eles são `trainers.party`, não `seteventmon`/`setwildbattle`/
`givemon`.

Lenda = espécie com `isSubLegendary`, `isRestrictedLegendary`, `isMythical` ou
`isUltraBeast` no `species_info`. Paradox NÃO conta (não é lendário). Formas de
macro (Arceus, Genesect, Ogerpon e afins) herdam a marca da espécie-base pelo
número de dex, porque o `_blocos` do catálogo não as enxerga.

Fontes varridas, todas lidas do disco: `data/maps/*/scripts.inc` e
`data/scripts/*.inc` (`seteventmon`, `setwildbattle`, `givemon`), os objetos
`OBJ_EVENT_GFX_SPECIES(...)` de cada `map.json` (para a coordenada) e os
errantes de `src/roamer.c` (`TryAddRoamer`).
"""
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

MARCAS = ("isSubLegendary", "isRestrictedLegendary", "isMythical", "isUltraBeast")
NIVEL_MIN, NIVEL_MAX = 50, 100
MACRO = re.compile(r"^\s*(seteventmon|setwildbattle|givemon)\s+(SPECIES_[A-Z0-9_]+)\s*,\s*(\d+)", re.M)
ROTULO = re.compile(r"^([A-Za-z0-9_]+)::?\s*$", re.M)


def marcas_de_lenda():
    """{SPECIES_X: categoria} lido dos nove arquivos de família."""
    txt_dex = open(os.path.join(RAIZ, "include/constants/pokedex.h")).read()
    fora, por_dex = {}, {}
    for gen in range(1, 10):
        txt = open(os.path.join(RAIZ, "src/data/pokemon/species_info",
                                f"gen_{gen}_families.h"), encoding="utf-8").read()
        for m in re.finditer(r"^\s*\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*$", txt, re.M):
            i = txt.index("{", m.end())
            nivel, j = 0, i
            while j < len(txt):
                if txt[j] == "{":
                    nivel += 1
                elif txt[j] == "}":
                    nivel -= 1
                    if nivel == 0:
                        break
                j += 1
            corpo = txt[i:j]
            cat = None
            if re.search(r"\.isUltraBeast\s*=\s*TRUE", corpo):
                cat = "ultra-fera"
            elif re.search(r"\.isMythical\s*=\s*TRUE", corpo):
                cat = "mítico"
            elif re.search(r"\.isRestrictedLegendary\s*=\s*TRUE", corpo):
                cat = "lendário"
            elif re.search(r"\.isSubLegendary\s*=\s*TRUE", corpo):
                cat = "sublendário"
            dex = re.search(r"\.natDexNum\s*=\s*(NATIONAL_DEX_[A-Z0-9_]+)", corpo)
            if cat:
                fora[m.group(1)] = cat
                if dex:
                    por_dex.setdefault(dex.group(1), cat)
        # Formas por macro (ARCEUS_SPECIES_INFO, GENESECT_SPECIES_INFO,
        # OGERPON_SPECIES_INFO...): a marca mora no corpo do #define.
        macros = {}
        for m in re.finditer(r"^#define\s+([A-Z0-9_]+_SPECIES_INFO)\b(.*?)(?=^\S)",
                             txt, re.M | re.S):
            corpo = m.group(2)
            for chave, nome in (("isUltraBeast", "ultra-fera"), ("isMythical", "mítico"),
                                ("isRestrictedLegendary", "lendário"),
                                ("isSubLegendary", "sublendário")):
                if re.search(r"\.%s\s*=\s*TRUE" % chave, corpo):
                    macros[m.group(1)] = nome
                    break
        for m in re.finditer(r"^\s*\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*([A-Z0-9_]+_SPECIES_INFO)\b",
                             txt, re.M):
            if m.group(2) in macros:
                fora.setdefault(m.group(1), macros[m.group(2)])
    # Apelidos de species.h (SPECIES_GIRATINA = SPECIES_GIRATINA_ALTERED).
    sp = open(os.path.join(RAIZ, "include/constants/species.h")).read()
    for m in re.finditer(r"^\s*(?:#define\s+)?(SPECIES_[A-Z0-9_]+)\s*=?\s*(SPECIES_[A-Z0-9_]+)\s*,?\s*$", sp, re.M):
        if m.group(2) in fora:
            fora.setdefault(m.group(1), fora[m.group(2)])
    return fora, por_dex


def categoria(especie, marcas, por_dex):
    if especie in marcas:
        return marcas[especie]
    # forma de macro: herda pela raiz do nome (ARCEUS_FIRE -> ARCEUS)
    partes = especie.replace("SPECIES_", "").split("_")
    for k in range(len(partes) - 1, 0, -1):
        base = "SPECIES_" + "_".join(partes[:k])
        if base in marcas:
            return marcas[base]
        nd = "NATIONAL_DEX_" + "_".join(partes[:k])
        if nd in por_dex:
            return por_dex[nd]
    return None


def mapas_de_cidade():
    """Pastas de mapa cujo `map_type` é cidade (MAP_TYPE_TOWN / MAP_TYPE_CITY),
    menos as que a conversão de Sinnoh marcou como cidade sem ser
    (`niveis_lendarios.NAO_E_CIDADE`: Eterna Forest, lagos, rotas)."""
    import niveis_lendarios as NL
    fora = set()
    for cam in glob.glob(f"{RAIZ}/data/maps/*/map.json"):
        d = json.load(open(cam, encoding="utf-8"))
        if d.get("map_type") in ("MAP_TYPE_TOWN", "MAP_TYPE_CITY"):
            fora.add(os.path.basename(os.path.dirname(cam)))
    return fora - NL.NAO_E_CIDADE


def objetos_por_script(pasta, raiz=RAIZ):
    cam = f"{raiz}/data/maps/{pasta}/map.json"
    if not os.path.exists(cam):
        return {}
    d = json.load(open(cam, encoding="utf-8"))
    fora = {}
    for o in d.get("object_events", []):
        s = o.get("script")
        if s:
            fora.setdefault(s, []).append(o)
    return fora


def varre(raiz=RAIZ):
    marcas, por_dex = marcas_de_lenda()
    linhas = []
    arquivos = sorted(glob.glob(f"{raiz}/data/maps/*/scripts.inc")) + \
        sorted(glob.glob(f"{raiz}/data/scripts/*.inc"))
    for cam in arquivos:
        txt = open(cam, encoding="utf-8").read()
        pasta = os.path.basename(os.path.dirname(cam)) if "/maps/" in cam else \
            "data/scripts/" + os.path.basename(cam)
        rotulos = [(m.start(), m.group(1)) for m in ROTULO.finditer(txt)]
        objs = objetos_por_script(pasta, raiz) if "/maps/" in cam else {}
        for m in MACRO.finditer(txt):
            esp, nivel = m.group(2), int(m.group(3))
            cat = categoria(esp, marcas, por_dex)
            if not cat:
                continue
            rot = None
            for p, r in rotulos:
                if p <= m.start():
                    rot = r
            linha = txt.count("\n", 0, m.start()) + 1
            # objeto do mapa cujo script é o rótulo (ou o rótulo-pai do bloco)
            xy = "-"
            if rot in objs:
                xy = f"{objs[rot][0]['x']},{objs[rot][0]['y']}"
            if xy == "-":
                # o rótulo do objeto pode ser outro (Intro/Battle): procura pelo gfx
                cand = [o for lst in objs.values() for o in lst
                        if o.get("graphics_id", "").endswith("(%s)" % esp.replace("SPECIES_", ""))]
                if len(cand) == 1:
                    xy = f"{cand[0]['x']},{cand[0]['y']}"
            linhas.append(dict(mapa=pasta, xy=xy, especie=esp, categoria=cat,
                               como=m.group(1), nivel=nivel, rotulo=rot,
                               arquivo=os.path.relpath(cam, raiz), linha=linha))
    roamer = open(f"{raiz}/src/roamer.c", encoding="utf-8").read()
    for m in re.finditer(r"TryAddRoamer\((SPECIES_[A-Z0-9_]+),\s*(\d+)\)", roamer):
        cat = categoria(m.group(1), marcas, por_dex)
        if cat:
            linhas.append(dict(mapa="errante (src/roamer.c)", xy="-", especie=m.group(1),
                               categoria=cat, como="errante", nivel=int(m.group(2)),
                               rotulo="TryAddRoamer", arquivo="src/roamer.c",
                               linha=roamer.count("\n", 0, m.start()) + 1))
    return linhas


def guarda(linhas, cidades, tabela=None):
    """Três regras: nível 50..100, nível igual ao do LUGAR (niveis_lendarios.py),
    e nenhum encontro em mapa de cidade (o presente de laboratório pode)."""
    if tabela is None:
        import niveis_lendarios as NL
        tabela = NL.NIVEL
    erros = []
    for l in linhas:
        if not (NIVEL_MIN <= l["nivel"] <= NIVEL_MAX):
            erros.append(f"{l['especie']} em {l['mapa']} ({l['arquivo']}:{l['linha']}) "
                         f"nível {l['nivel']}, fora de {NIVEL_MIN}..{NIVEL_MAX}")
        elif l["mapa"] not in tabela:
            erros.append(f"{l['especie']} em {l['mapa']}: mapa sem nível em niveis_lendarios.py")
        elif tabela[l["mapa"]][0] != l["nivel"]:
            erros.append(f"{l['especie']} em {l['mapa']} ({l['arquivo']}:{l['linha']}) "
                         f"nível {l['nivel']}, a tabela do lugar diz {tabela[l['mapa']][0]}")
        if l["mapa"] in cidades and l["como"] != "givemon":
            erros.append(f"{l['especie']} em {l['mapa']} {l['xy']}: lendário em mapa de cidade")
    return erros


def demo():
    linhas = varre()
    cidades = mapas_de_cidade()
    base = guarda(linhas, cidades)
    if base:
        print("DEMO: a árvore já reprova, a demo não prova nada:\n  " + "\n  ".join(base))
        return 1
    if not linhas or not cidades:
        print("DEMO: inventário ou lista de cidades vazia: varredura cega")
        return 1
    ok = True
    m1 = [dict(linhas[0], nivel=49)]
    if not guarda(m1, cidades):
        print("DEMO: nível 49 passou calado"); ok = False
    m2 = [dict(linhas[0], nivel=101)]
    if not guarda(m2, cidades):
        print("DEMO: nível 101 passou calado"); ok = False
    m3 = [dict(linhas[0], mapa=sorted(cidades)[0], como="seteventmon")]
    if not guarda(m3, cidades):
        print("DEMO: lendário em cidade passou calado"); ok = False
    m4 = [dict(linhas[0], mapa=sorted(cidades)[0], como="givemon")]
    tab = {sorted(cidades)[0]: (linhas[0]["nivel"], "demo")}
    if guarda(m4, cidades, tab):
        print("DEMO: presente de laboratório em cidade reprovou (não deveria)"); ok = False
    import niveis_lendarios as NL
    alvo = NL.NIVEL[linhas[0]["mapa"]][0]
    outro = 50 if alvo != 50 else 55
    if not guarda([dict(linhas[0], nivel=outro)], cidades):
        print("DEMO: nível dentro da faixa mas diferente do lugar passou calado"); ok = False
    if not guarda([dict(linhas[0], mapa="MapaInventado")], cidades):
        print("DEMO: mapa sem nível na tabela passou calado"); ok = False
    if "EternaForest" in cidades:
        print("DEMO: Eterna Forest contada como cidade"); ok = False
    print(f"DEMO: {'VERDE' if ok else 'VERMELHO'} ({len(linhas)} pontos lidos, {len(cidades)} cidades)")
    return 0 if ok else 1


def main():
    if "--demo" in sys.argv:
        return demo()
    linhas = varre()
    if "--guarda" in sys.argv:
        erros = guarda(linhas, mapas_de_cidade())
        for e in erros:
            print("  " + e)
        print(f"LENDÁRIOS: {len(linhas)} pontos, {len(erros)} achado(s)")
        return 1 if erros else 0
    print("mapa\txy\tespecie\tcategoria\tcomo\tnivel\trotulo\tarquivo:linha")
    for l in sorted(linhas, key=lambda l: (l["mapa"], l["especie"])):
        print(f"{l['mapa']}\t{l['xy']}\t{l['especie']}\t{l['categoria']}\t{l['como']}\t"
              f"{l['nivel']}\t{l['rotulo']}\t{l['arquivo']}:{l['linha']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
