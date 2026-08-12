#!/usr/bin/env python3
"""Diz PARA ONDE vai a ROM, e quanto dá para recuperar sem tirar conteúdo.

Uso:
    python3 dev_scripts/orcamento_rom.py            # relatório completo
    python3 dev_scripts/orcamento_rom.py --consumo  # só a tabela de consumo
    python3 dev_scripts/orcamento_rom.py --duplicado
    python3 dev_scripts/orcamento_rom.py --especies
    python3 dev_scripts/orcamento_rom.py --demo     # autoverificação

Por que existe: "a ROM está em 96%" não diz o que cortar. A fonte de verdade é o
`pokeemerald.map` que o linker escreve na última build, porque ele lista TODA
seção de entrada com endereço, tamanho e arquivo-objeto de origem. Nada aqui é
estimado a partir do tamanho de PNG na árvore: o que não estiver no mapa não
está na ROM.

Três medidas independentes:

  1. CONSUMO. Soma as seções de entrada com endereço em 0x08000000..0x0A000000,
     agrupadas por objeto e por símbolo, e classifica em categoria de conteúdo
     (gráfico de Pokémon, cry, tileset, texto de script, treinador, código).
  2. DUPLICADO. Passa SHA-1 nos binários já convertidos em build.nosync/assets.
     Arquivo idêntico ali é byte idêntico dentro da ROM, porque o linker não
     junta INCBIN igual: cada cópia paga o preço inteiro.
  3. ESPÉCIES POR CHAVE DE CONFIGURAÇÃO. Cada espécie/forma nasce dentro de um
     `#if P_FAMILY_X` (ou P_MEGA_EVOLUTIONS, P_GIGANTAMAX_FORMS...), e cada
     família aponta para um P_GEN_N_POKEMON em include/config/species_enabled.h.
     O script soma o custo (sprite, ícone, paleta, pegada, follower e cry) por
     chave, o que responde "quanto a ROM devolve se eu desligar a geração N".

ARMADILHA MEDIDA: o tamanho de um símbolo aqui é a distância até o PRÓXIMO
símbolo listado. Dado `static` não aparece no mapa, então ele é cobrado do
símbolo global anterior. Por isso o total por símbolo bate com a seção, mas uma
linha isolada pode estar inflada. Quando o número importa, confira com a segunda
medida: o custo dos cries também é somado a partir dos arquivos .bin em disco, e
as duas contas fecham dentro de 5%.
"""
import hashlib
import os
import re
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPA = os.path.join(RAIZ, "pokeemerald.map")
ASSETS = os.path.join(RAIZ, "build.nosync", "assets")
CRIES = os.path.join(RAIZ, "sound", "direct_sound_samples", "cries")
SPECIES_INFO = os.path.join(RAIZ, "src", "data", "pokemon", "species_info")
SPECIES_ENABLED = os.path.join(RAIZ, "include", "config", "species_enabled.h")

ROM_INI, ROM_FIM = 0x08000000, 0x0A000000
TAM_ROM = 32 * 1024 * 1024

RE_SECAO = re.compile(r"^\s(\S+)\s+0x([0-9a-f]{8,})\s+0x([0-9a-f]+)\s+(\S+)\s*$")
RE_CONT = re.compile(r"^\s+0x([0-9a-f]{8,})\s+0x([0-9a-f]+)\s+(\S+)\s*$")
RE_SO_NOME = re.compile(r"^\s(\S+)\s*$")
RE_SIMBOLO = re.compile(r"^\s+0x([0-9a-f]{8})\s+([A-Za-z_][\w.]*)\s*$")

# objeto -> categoria de conteúdo. A ordem importa: primeiro que casa vence.
CATEGORIAS = [
    ("data/sound_data.o", "som (cries, música, amostras)"),
    ("src/pokemon.o", "gráficos e dados de Pokémon"),
    ("data/maps.o", "layouts e blockdata dos mapas"),
    ("src/tilesets.o", "tilesets (tiles, metatiles, paletas)"),
    ("data/event_scripts.o", "scripts e texto de mapa"),
    ("src/graphics.o", "gráficos diversos (batalha, itens, treinador)"),
    ("src/event_object_movement.o", "sprites de overworld"),
    ("src/data.o", "tabela de treinadores (gTrainers)"),
    ("src/trainer_slide.o", "falas de treinador (sTrainerSlides)"),
    ("src/fonts.o", "fontes"),
    ("data/map_events.o", "objetos, warps e placas dos mapas"),
    ("data/battle_anim_scripts.o", "scripts de animação de batalha"),
]

PREFIXOS_ESPECIE = [
    "gMonFrontPic_", "gMonBackPic_", "gMonShinyPalette_", "gMonPalette_",
    "gMonIcon_", "gMonFootprint_", "gObjectEventPic_", "Cry_",
]

CHAVES_FORMA = [
    "P_GIGANTAMAX_FORMS", "P_MEGA_EVOLUTIONS", "P_TERA_FORMS",
    "P_PRIMAL", "P_ULTRA_BURST", "P_FUSION_FORMS",
]


def kb(n):
    return "%.1f" % (n / 1024.0)


# ---------------------------------------------------------------- 1. consumo

def le_mapa(caminho=MAPA):
    """Devolve [(secao, endereco, tamanho, objeto)] só do que está na ROM."""
    linhas = open(caminho, encoding="utf-8", errors="replace").read().split("\n")
    fora = []
    i = 0
    while i < len(linhas):
        m = RE_SECAO.match(linhas[i])
        if m:
            fora.append((m.group(1), int(m.group(2), 16), int(m.group(3), 16), m.group(4)))
            i += 1
            continue
        m = RE_SO_NOME.match(linhas[i])
        if m and i + 1 < len(linhas):
            c = RE_CONT.match(linhas[i + 1])
            if c:
                fora.append((m.group(1), int(c.group(1), 16), int(c.group(2), 16), c.group(3)))
                i += 2
                continue
        i += 1
    return [r for r in fora if ROM_INI <= r[1] < ROM_FIM]


def simbolos(linhas, objeto, secao=".rodata"):
    """Símbolos de uma seção, com tamanho pela distância até o próximo."""
    for i, l in enumerate(linhas):
        m = RE_SECAO.match(l)
        if not (m and m.group(4) == objeto and m.group(1) == secao):
            continue
        if int(m.group(2), 16) < ROM_INI:
            continue
        base, tam = int(m.group(2), 16), int(m.group(3), 16)
        achados, j = [], i + 1
        while j < len(linhas) and (linhas[j].startswith(" " * 16) or not linhas[j].strip()):
            s = RE_SIMBOLO.match(linhas[j])
            if s:
                achados.append((int(s.group(1), 16), s.group(2)))
            j += 1
        achados.sort()
        return [((achados[k + 1][0] if k + 1 < len(achados) else base + tam) - a, n)
                for k, (a, n) in enumerate(achados)]
    return []


def consumo(regs):
    por_objeto = defaultdict(int)
    for _, _, tam, obj in regs:
        por_objeto[obj] += tam
    por_cat = defaultdict(int)
    for obj, tam in por_objeto.items():
        cat = next((c for chave, c in CATEGORIAS if obj == chave), None)
        if cat is None:
            cat = "código e dados do motor" if obj.startswith(("src/", "/", "..")) else "outros dados"
        por_cat[cat] += tam
    return por_objeto, por_cat


# -------------------------------------------------------------- 2. duplicado

def duplicados(base=ASSETS, extensoes=(".smol", ".fastSmol", ".smolTM", ".gbapal", ".1bpp", ".4bpp")):
    """Agrupa por SHA-1 os binários já convertidos. Devolve {ext: (grupos, bytes)}."""
    por_ext = defaultdict(lambda: defaultdict(list))
    for dp, _, fn in os.walk(base):
        for f in fn:
            ext = next((e for e in extensoes if f.endswith(e)), None)
            if ext is None:
                continue
            p = os.path.join(dp, f)
            with open(p, "rb") as fh:
                dado = fh.read()
            por_ext[ext][(hashlib.sha1(dado).hexdigest(), len(dado))].append(p)
    fora = {}
    for ext, grupos in por_ext.items():
        repetidos = [(k[1], v) for k, v in grupos.items() if len(v) > 1]
        fora[ext] = (repetidos, sum(t * (len(v) - 1) for t, v in repetidos))
    return fora


# --------------------------------------------------- 3. espécies por guarda

def familia_para_geracao(caminho=SPECIES_ENABLED):
    texto = open(caminho, encoding="utf-8", errors="replace").read()
    return {m.group(1): m.group(2)
            for m in re.finditer(r"^#define\s+(P_FAMILY_\w+)\s+(\S+)", texto, re.M)}


def guardas_das_especies(pasta=SPECIES_INFO):
    """SPECIES_X -> lista de condições #if ativas onde a entrada foi declarada."""
    fora = {}
    for g in range(1, 10):
        caminho = os.path.join(pasta, "gen_%d_families.h" % g)
        if not os.path.exists(caminho):
            continue
        pilha = []
        for linha in open(caminho, encoding="utf-8", errors="replace"):
            s = linha.strip()
            if s.startswith("#if"):
                pilha.append(s)
            elif s.startswith("#endif") and pilha:
                pilha.pop()
            m = re.match(r"\[SPECIES_([A-Z0-9_]+)\]\s*=", s)
            if m:
                fora[m.group(1)] = list(pilha)
    return fora


def chave_da_guarda(condicoes, fam2gen):
    texto = " ".join(condicoes)
    for k in CHAVES_FORMA:
        if k in texto:
            return k
    fams = re.findall(r"(P_FAMILY_\w+)", texto)
    if fams:
        return fam2gen.get(fams[0], fams[0])
    return "sem guarda"


def camel(const):
    return "".join(p.capitalize() for p in const.split("_"))


def custo_por_guarda(linhas):
    """Custo de gráfico + cry por chave de configuração, medido no mapa."""
    fam2gen = familia_para_geracao()
    guardas = guardas_das_especies()
    sym2const = {camel(c): c for c in guardas}
    total, quantos = defaultdict(int), defaultdict(set)
    for tam, nome in simbolos(linhas, "src/pokemon.o") + simbolos(linhas, "data/sound_data.o"):
        for p in PREFIXOS_ESPECIE:
            if not nome.startswith(p):
                continue
            const = sym2const.get(nome[len(p):])
            if const:
                k = chave_da_guarda(guardas[const], fam2gen)
                total[k] += tam
                quantos[k].add(const)
            break
    return total, quantos


def custo_cries_em_disco(pasta=CRIES):
    """Segunda medida, independente do mapa: o .bin de cada cry no disco."""
    if not os.path.isdir(pasta):
        return {}
    fam2gen = familia_para_geracao()
    guardas = guardas_das_especies()
    tam = {f[:-4]: os.path.getsize(os.path.join(pasta, f))
           for f in os.listdir(pasta) if f.endswith(".bin")}
    total = defaultdict(int)
    for const, cond in guardas.items():
        n = const.lower()
        if n in tam:
            total[chave_da_guarda(cond, fam2gen)] += tam[n]
    return total


# ------------------------------------------------------------------ saída

def relatorio(quais):
    if not os.path.exists(MAPA):
        sys.exit("sem %s: rode uma build (em worktree isolada) antes." % MAPA)
    linhas = open(MAPA, encoding="utf-8", errors="replace").read().split("\n")
    regs = le_mapa()
    if "consumo" in quais:
        por_objeto, por_cat = consumo(regs)
        soma = sum(por_cat.values())
        print("== PARA ONDE VAI A ROM ==  (%s KB mapeados de %s KB de cartucho)"
              % (kb(soma), kb(TAM_ROM)))
        for c, v in sorted(por_cat.items(), key=lambda x: -x[1]):
            print("  %10s KB  %5.1f%%  %s" % (kb(v), 100.0 * v / TAM_ROM, c))
        print("\n-- 15 maiores objetos --")
        for o, v in sorted(por_objeto.items(), key=lambda x: -x[1])[:15]:
            print("  %10s KB  %5.1f%%  %s" % (kb(v), 100.0 * v / TAM_ROM, o))
    if "especies" in quais:
        print("\n== CUSTO DE ESPÉCIE POR CHAVE DE CONFIGURAÇÃO ==")
        total, quantos = custo_por_guarda(linhas)
        disco = custo_cries_em_disco()
        print("  %10s  %6s  %-24s %s" % ("KB (mapa)", "formas", "chave", "cry KB (disco)"))
        for k, v in sorted(total.items(), key=lambda x: -x[1]):
            print("  %10s  %6d  %-24s %s" % (kb(v), len(quantos[k]), k, kb(disco.get(k, 0))))
        gens = sum(total.get("P_GEN_%d_POKEMON" % i, 0) for i in range(6, 10))
        print("  -> desligar as gerações 6 a 9 devolve %s KB (%.2f MB)"
              % (kb(gens), gens / 1048576.0))
    if "duplicado" in quais:
        print("\n== GRÁFICO DUPLICADO BYTE A BYTE (build.nosync/assets) ==")
        if not os.path.isdir(ASSETS):
            print("  sem build.nosync/assets: nada a medir.")
        else:
            for ext, (grupos, desperdicio) in sorted(duplicados().items(),
                                                     key=lambda x: -x[1][1]):
                print("  %10s KB desperdiçados em %4d grupos  %s"
                      % (kb(desperdicio), len(grupos), ext))
                for t, v in sorted(grupos, key=lambda x: -x[0] * (len(x[1]) - 1))[:3]:
                    print("      %8s KB  x%-3d  %s" % (kb(t * (len(v) - 1)), len(v),
                                                       os.path.relpath(v[0], RAIZ)))


# ------------------------------------------------------------------- demo

DEMO_MAPA = """Linker script and memory map

.text           0x08000000   0x000100
 .text          0x08000000       0x80 src/alfa.o
                0x08000000                Comeco
                0x08000040                Meio
 .text          0x08000080       0x80 src/beta.o

.rodata         0x08000100   0x000200
 .rodata        0x08000100      0x100 src/pokemon.o
                0x08000100                gMonFrontPic_Bulbasaur
                0x08000180                Cry_Bulbasaur
 .rodata.longa
                0x08000200      0x100 data/sound_data.o
 .ewram         0x02000000       0x40 src/gama.o
"""


def demo():
    import tempfile
    d = tempfile.mkdtemp()
    p = os.path.join(d, "demo.map")
    open(p, "w").write(DEMO_MAPA)
    regs = le_mapa(p)
    objs = {o: t for _, _, t, o in regs}
    # só o que está na ROM entra: .ewram em 0x02000000 fica de fora
    assert "src/gama.o" not in objs, objs
    # a linha de continuação (nome numa linha, endereço na seguinte) é lida
    assert objs["data/sound_data.o"] == 0x100, objs
    assert objs["src/alfa.o"] == 0x80 and objs["src/beta.o"] == 0x80, objs
    linhas = open(p, encoding="utf-8", errors="replace").read().split("\n")
    s = dict((n, t) for t, n in simbolos(linhas, "src/pokemon.o"))
    # tamanho de símbolo é a distância até o próximo; o último vai até o fim da seção
    assert s["gMonFrontPic_Bulbasaur"] == 0x80, s
    assert s["Cry_Bulbasaur"] == 0x80, s
    # pilha de #if: espécie declarada dentro de duas guardas carrega as duas
    fonte = os.path.join(d, "gen_1_families.h")
    open(fonte, "w").write(
        "#if P_FAMILY_BULBASAUR\n    [SPECIES_BULBASAUR] =\n"
        "#if P_MEGA_EVOLUTIONS\n    [SPECIES_VENUSAUR_MEGA] =\n#endif\n#endif\n"
        "    [SPECIES_SOLTA] =\n")
    g = guardas_das_especies(d)
    assert len(g["BULBASAUR"]) == 1, g
    assert len(g["VENUSAUR_MEGA"]) == 2, g
    assert g["SOLTA"] == [], g
    f2g = {"P_FAMILY_BULBASAUR": "P_GEN_1_POKEMON"}
    # forma especial ganha a chave da forma, não a da geração da família
    assert chave_da_guarda(g["VENUSAUR_MEGA"], f2g) == "P_MEGA_EVOLUTIONS"
    assert chave_da_guarda(g["BULBASAUR"], f2g) == "P_GEN_1_POKEMON"
    assert camel("VENUSAUR_MEGA") == "VenusaurMega"
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        pedidos = {a.lstrip("-") for a in sys.argv[1:] if a.startswith("--")}
        relatorio(pedidos or {"consumo", "especies", "duplicado"})
