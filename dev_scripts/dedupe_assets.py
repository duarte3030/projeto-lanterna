#!/usr/bin/env python3
"""Tira da ROM os assets que aparecem DUAS vezes com os mesmos bytes.

Uso:
    python3 dev_scripts/dedupe_assets.py --censo     # o que é duplicata de quê
    python3 dev_scripts/dedupe_assets.py --aplicar   # reescreve (idempotente)
    python3 dev_scripts/dedupe_assets.py --demo      # prova por md5 + autoteste

Por que existe
--------------
`INCBIN`/`INCGFX` cola os bytes do arquivo dentro do símbolo. O linker NÃO junta
dois símbolos de conteúdo igual (o `ld` do arm-none-eabi não tem ICF), então
`gObjectEventPic_ArceusFighting` e `gObjectEventPic_ArceusNormal`, que citam o
MESMO png, pagam 1284 bytes cada um, 18 vezes. Medido na árvore de 18/08/2026:
252 famílias, 102,5 KB de bytes repetidos, todos confirmados no
`pokeemerald.map`. Aplicado, o linker caiu de 32.283.792 B (96,21%) para
32.180.336 B (95,90%), 101,0 KB de volta, com EWRAM e IWRAM sem mexer um byte.

O mecanismo
-----------
Compartilhamento de ponteiro, sem tocar no motor: a definição duplicada vira um
ALIAS de link para a canônica.

    - const u32 gObjectEventPic_ArceusFighting[] = INCGFX_COMP("...", ".4bpp", "...");
    + extern const u32 gObjectEventPic_ArceusFighting[ARRAY_COUNT(gObjectEventPic_ArceusNormal)] ASSET_ALIAS(gObjectEventPic_ArceusNormal);

O alias custa ZERO byte de ROM (`nm -S` mostra os dois nomes no mesmo endereço e
com o mesmo tamanho), o tipo continua igual, `sizeof` continua certo (vem de
`ARRAY_COUNT` do canônico, então nem config que troca `.4bpp` por `.4bpp.smol`
desalinha) e nenhum consumidor precisa ser caçado: quem escreve
`.footprint = gMonFootprint_Caterpie` continua compilando.

Regras de segurança, todas medidas e não presumidas
---------------------------------------------------
1. MESMO ARQUIVO. `__attribute__((alias))` exige o alvo definido na mesma
   unidade de tradução. Família espalhada por dois arquivos é IGNORADA.
2. MESMA GUARDA DE PREPROCESSADOR. A pilha de `#if` do canônico tem que ser
   PREFIXO da pilha do duplicado, senão existe configuração que liga o duplicado
   e desliga o canônico, e o link quebra. `#else`/`#elif` entram na pilha
   negados, então irmãos nunca casam.
3. CANÔNICO ANTES. O alias sempre aponta para símbolo que aparece acima dele no
   arquivo.
4. Corpo com `#if` dentro é IGNORADO.

O RISCO REAL, e como ele é pego
-------------------------------
Asset compartilhado é observável se alguém EDITAR uma cópia esperando efeito
local: depois da dedupe, mexer em `graphics/pokemon/caterpie/footprint.png` não
muda nada, calado, porque o símbolo do Caterpie virou alias do Metapod. Por isso
os arquivos duplicados NÃO são apagados e `--demo` refaz o md5 de cada arquivo
original contra o do canônico: editou uma cópia, o demo fica VERMELHO e diz qual
é o canônico. Cada canônico também leva um comentário com o número de
consumidores, e a lista inteira vive em `dev_scripts/dedupe_assets.json`.

O que este script NÃO resolve
-----------------------------
1. 13,6 KB em 55 restos cujos membros moram em guardas IRMÃS (um
   `#if P_FAMILY_X` por espécie, então nenhum membro serve de canônico para os
   outros). Só sairia criando um símbolo canônico novo fora das guardas.
2. As ~1063 paletas zeradas de 32 B dos tilesets (~33 KB), que EXIGEM mudança de
   motor. Elas não são símbolos:
são LINHAS de `const u16 gTilesetPalettes_X[][16]`, e `struct Tileset.palettes`
é `const u16 (*)[16]`, um bloco contíguo de 16 paletas. Compartilhar linha
exigiria trocar o campo por uma tabela de ponteiros e mexer em quem carrega
paleta de tileset. Só o BLOCO inteiro de 512 B dá para compartilhar, e isso este
script já faz.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = "build.nosync/assets/"
MAPA = os.path.join(RAIZ, "pokeemerald.map")
MANIFESTO = os.path.join(RAIZ, "dev_scripts", "dedupe_assets.json")
DIRS = ("src", "include", "data")

MARCA = "dedupe_assets.py"

RE_DEF = re.compile(
    r'^(\s*)((?:static\s+)?const\s+\w+\s+)(\w+)\s*((?:\[[^\]]*\])+)\s*=\s*(.*)$')
RE_INCGFX = re.compile(
    r'INCGFX_(U8|U16|U32|COMP)\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*(?:,\s*"([^"]*)"\s*)?\)')
RE_INCBIN = re.compile(r'INCBIN_(U8|U16|U32|COMP)\(\s*((?:"[^"]+"\s*,?\s*)+)\)')
RE_SIMBOLO_MAPA = re.compile(r'^\s+0x0([89a-f][0-9a-f]{6})\s+([A-Za-z_]\w*)\s*$')


def fontes(corpo):
    """Arquivos construídos que um corpo de definição cola, na ordem."""
    saida = []
    for m in RE_INCGFX.finditer(corpo):
        tipo, src, ext, args = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        # Espelha tools/preproc/c_file.cpp: argumento vira parte do nome.
        sufixo = "".join(c if c.isalnum() else "_" for c in args)
        saida.append(ASSETS + src + sufixo + ext + (".smol" if tipo == "COMP" else ""))
    for m in RE_INCBIN.finditer(corpo):
        tipo = m.group(1)
        for p in re.findall(r'"([^"]+)"', m.group(2)):
            saida.append(p + (".smol" if tipo == "COMP" else ""))
    return saida


def digere(lista):
    """(md5, bytes) do conteúdo colado, ou None se algum arquivo não existe."""
    h = hashlib.md5()
    total = 0
    for rel in lista:
        caminho = os.path.join(RAIZ, rel)
        try:
            with open(caminho, "rb") as fp:
                b = fp.read()
        except OSError:
            return None
        h.update(b)
        total += len(b)
    return h.hexdigest(), total


def arquivos_fonte():
    for base in DIRS:
        for raiz, _, nomes in os.walk(os.path.join(RAIZ, base)):
            if "build" in raiz:
                continue
            for n in sorted(nomes):
                if n.endswith((".c", ".h")):
                    yield os.path.relpath(os.path.join(raiz, n), RAIZ)


def varre(rel):
    """Definições com INCBIN/INCGFX de um arquivo, com a pilha de guardas."""
    with open(os.path.join(RAIZ, rel), encoding="utf-8", errors="replace") as fp:
        linhas = fp.read().split("\n")
    guardas, achados, i = [], [], 0
    while i < len(linhas):
        ln = linhas[i]
        nu = ln.lstrip()
        if nu.startswith("#"):
            d = nu[1:].lstrip()
            d = d.split("//")[0].split("/*")[0].strip()
            if d.startswith(("ifdef", "ifndef", "if")):
                guardas.append(d)  # texto cru: `ifdef X` != `ifndef X`
            elif d.startswith("elif"):
                if guardas:
                    guardas[-1] = "!(" + guardas[-1] + ")&&" + d[4:].strip()
            elif d.startswith("else"):
                if guardas:
                    guardas[-1] = "!(" + guardas[-1] + ")"
            elif d.startswith("endif"):
                if guardas:
                    guardas.pop()
            i += 1
            continue
        m = RE_DEF.match(ln)
        if not m or m.group(2).startswith("static"):
            i += 1
            continue
        # Junta até o ';' de profundidade zero.
        ini, prof, fim = i, 0, None
        corpo = []
        j = i
        while j < len(linhas) and fim is None:
            texto = linhas[j] if j > i else m.group(5)
            corpo.append(texto)
            for c in texto:
                if c == "{":
                    prof += 1
                elif c == "}":
                    prof -= 1
                elif c == ";" and prof <= 0:
                    fim = j
                    break
            j += 1
        if fim is None:
            i += 1
            continue
        texto_corpo = "\n".join(corpo)
        i = fim + 1
        if "INCBIN" not in texto_corpo and "INCGFX" not in texto_corpo:
            continue
        if re.search(r'^\s*#', texto_corpo, re.M):
            continue  # guarda dentro do corpo: não mexe
        f = fontes(texto_corpo)
        if not f:
            continue
        achados.append({
            "arquivo": rel, "nome": m.group(3), "tipo": m.group(2).strip(),
            "dims": m.group(4), "recuo": m.group(1),
            "linha_ini": ini, "linha_fim": fim,
            "guardas": list(guardas), "fontes": f,
        })
    return achados


def simbolos_na_rom():
    if not os.path.exists(MAPA):
        return None
    dentro = set()
    with open(MAPA, encoding="utf-8", errors="replace") as fp:
        for ln in fp:
            m = RE_SIMBOLO_MAPA.match(ln)
            if m:
                dentro.add(m.group(2))
    return dentro


def prefixo(a, b):
    return len(a) <= len(b) and all(x == y for x, y in zip(a, b))


def familias():
    """Famílias deduplicáveis: canônico + aliases seguros, por md5."""
    defs = []
    for rel in arquivos_fonte():
        defs.extend(varre(rel))
    por_hash = defaultdict(list)
    for d in defs:
        dig = digere(d["fontes"])
        if dig is None:
            continue
        d["md5"], d["bytes"] = dig
        if d["bytes"] == 0:
            continue
        por_hash[(d["arquivo"], dig[0], dig[1])].append(d)

    saida, sobras = [], []
    for (arq, md5, tam), membros in por_hash.items():
        if len(membros) < 2:
            continue
        membros.sort(key=lambda d: d["linha_ini"])
        # Guloso: o canônico não é "o primeiro", é o que ACEITA mais membros
        # (guarda dele prefixo da do alias, e definido acima dele). Quem sobra
        # tenta de novo, então uma família vira várias subfamílias.
        restantes = membros
        while len(restantes) > 1:
            melhor = None
            for c in restantes:
                cabem = [d for d in restantes
                         if d is not c and d["linha_ini"] > c["linha_ini"]
                         and prefixo(c["guardas"], d["guardas"])]
                if melhor is None or len(cabem) > len(melhor[1]):
                    melhor = (c, cabem)
            if not melhor[1]:
                sobras.append((arq, tam, len(restantes)))
                break
            canon, aliases = melhor
            saida.append({"arquivo": arq, "md5": md5, "bytes": tam,
                          "canonico": canon, "aliases": aliases})
            usados = {id(canon)} | {id(d) for d in aliases}
            restantes = [d for d in restantes if id(d) not in usados]
    saida.sort(key=lambda f: -f["bytes"] * len(f["aliases"]))
    return saida, sobras


def linha_alias(d, canon):
    dims = d["dims"]
    # preenche só a dimensão MAIS EXTERNA; as internas ficam como estavam
    interna = dims[dims.index("]") + 1:]
    novo = "[ARRAY_COUNT(%s)]%s" % (canon["nome"], interna)
    return ("%sextern %s %s%s ASSET_ALIAS(%s); // %s: mesmos %d B (md5 %s)"
            % (d["recuo"], d["tipo"], d["nome"], novo, canon["nome"],
               MARCA, d["bytes"], d["md5"][:8]))


def comentario_canonico(canon, n):
    return ("%s// %s: compartilhado por %d consumidores (lista em "
            "dev_scripts/dedupe_assets.json); editar este arquivo muda TODOS."
            % (canon["recuo"], MARCA, n + 1))


def censo(so_rom=True):
    fams, sobras = familias()
    rom = simbolos_na_rom() if so_rom else None
    print("== CENSO DE DUPLICATA BYTE A BYTE ==")
    if rom:
        print("   (KB confirmado no pokeemerald.map: símbolo que sobreviveu ao --gc-sections)")
    total = total_rom = 0
    for f in fams:
        n = len(f["aliases"])
        desp = f["bytes"] * n
        total += desp
        if rom is not None:
            vivos = sum(1 for d in f["aliases"] if d["nome"] in rom)
            if f["canonico"]["nome"] in rom:
                total_rom += f["bytes"] * vivos
        if desp >= 1024:
            print("%8.1f KB  x%-4d %7d B  %s  <- %s"
                  % (desp / 1024, n + 1, f["bytes"], f["canonico"]["nome"],
                     f["arquivo"]))
            print("             consumidores: %s"
                  % ", ".join(d["nome"] for d in f["aliases"][:6])
                  + (" ..." if n > 6 else ""))
    print("-- %d famílias, %.1f KB repetidos (%.1f KB confirmados na ROM) --"
          % (len(fams), total / 1024, total_rom / 1024))
    if sobras:
        perdido = sum(t * (n - 1) for _, t, n in sobras)
        print("-- %d restos sem canônico possível (guardas de #if irmãs, ex.: um "
              "`#if P_FAMILY_X` por espécie): %.1f KB deixados na mesa --"
              % (len(sobras), perdido / 1024))
    return fams


def aplicar():
    fams, _ = familias()
    if not fams:
        print("nada a fazer: nenhuma família duplicada")
        return 0
    por_arquivo = defaultdict(list)
    for f in fams:
        por_arquivo[f["arquivo"]].append(f)
    # Rodar de novo não pode APAGAR o manifesto: depois da primeira passada as
    # famílias já viraram alias e somem da varredura. Acumula.
    manifesto = {"gerado_por": "dev_scripts/dedupe_assets.py", "familias": []}
    if os.path.exists(MANIFESTO):
        with open(MANIFESTO, encoding="utf-8") as fp:
            manifesto["familias"] = json.load(fp)["familias"]
    ja = {f["canonico"]["nome"] for f in manifesto["familias"]}
    trocados = bytes_salvos = 0
    for rel, lista in sorted(por_arquivo.items()):
        caminho = os.path.join(RAIZ, rel)
        with open(caminho, encoding="utf-8") as fp:
            linhas = fp.read().split("\n")
        edicoes = []
        for f in lista:
            canon = f["canonico"]
            edicoes.append((canon["linha_ini"], canon["linha_ini"] - 1,
                            [comentario_canonico(canon, len(f["aliases"]))]))
            for d in f["aliases"]:
                edicoes.append((d["linha_ini"], d["linha_fim"],
                                [linha_alias(d, canon)]))
                trocados += 1
                bytes_salvos += d["bytes"]
            if canon["nome"] in ja:
                continue
            manifesto["familias"].append({
                "md5": f["md5"], "bytes": f["bytes"], "arquivo": rel,
                "canonico": {"nome": canon["nome"], "fontes": canon["fontes"]},
                "aliases": [{"nome": d["nome"], "fontes": d["fontes"]}
                            for d in f["aliases"]],
            })
        # de baixo para cima, para os números de linha não deslizarem
        edicoes.sort(key=lambda e: -e[0])
        for ini, fim, novo in edicoes:
            linhas[ini:fim + 1] = novo  # fim < ini => insere antes de `ini`
        with open(caminho, "w", encoding="utf-8") as fp:
            fp.write("\n".join(linhas))
        print("%-40s %d famílias" % (rel, len(lista)))
    with open(MANIFESTO, "w", encoding="utf-8") as fp:
        json.dump(manifesto, fp, indent=1, ensure_ascii=False)
        fp.write("\n")
    print("%d referências viraram alias, %.1f KB de ROM de volta"
          % (trocados, bytes_salvos / 1024))
    print("manifesto: dev_scripts/dedupe_assets.json")
    return trocados


def prova():
    """md5 de cada referência reescrita contra o canônico. É a prova pedida."""
    if not os.path.exists(MANIFESTO):
        print("sem manifesto: rode --aplicar antes")
        return False
    with open(MANIFESTO, encoding="utf-8") as fp:
        manifesto = json.load(fp)
    ok = ausentes = 0
    ruins = []
    for f in manifesto["familias"]:
        dc = digere(f["canonico"]["fontes"])
        if dc is None:
            ruins.append("canônico %s: arquivo sumiu" % f["canonico"]["nome"])
            continue
        if dc[0] != f["md5"]:
            ruins.append("canônico %s mudou (md5 %s, manifesto diz %s): %s"
                         % (f["canonico"]["nome"], dc[0][:8], f["md5"][:8],
                            " ".join(f["canonico"]["fontes"])))
            continue
        for a in f["aliases"]:
            da = digere(a["fontes"])
            if da is None:
                ausentes += 1  # não é mais construído: ninguém o referencia
                continue
            if da != dc:
                ruins.append("%s aponta para %s mas seus arquivos têm outros "
                             "bytes agora (md5 %s != %s). Editou uma cópia "
                             "esperando efeito local? Edite %s."
                             % (a["nome"], f["canonico"]["nome"], da[0][:8],
                                dc[0][:8], " ".join(f["canonico"]["fontes"])))
            else:
                ok += 1
    print("PROVA md5 (fonte): %d referências byte-idênticas ao canônico, %d com "
          "arquivo original já não construído, %d PROBLEMAS"
          % (ok, ausentes, len(ruins)))
    for r in ruins[:20]:
        print("  ! " + r)
    return prova_na_rom(manifesto) and not ruins


def prova_na_rom(manifesto):
    """A prova que vale: os bytes DENTRO da ROM, no endereço do símbolo.

    Confere que alias e canônico caem no MESMO endereço e que o que está lá tem
    o md5 do asset. Sem isto, `--demo` só compararia arquivo com arquivo e não
    provaria nada sobre a ROM construída.
    """
    rom_bin = os.path.join(RAIZ, "pokeemerald.gba")
    if not (os.path.exists(MAPA) and os.path.exists(rom_bin)):
        print("PROVA na ROM: PULADA (falta pokeemerald.map ou pokeemerald.gba)")
        return True
    ender = {}
    with open(MAPA, encoding="utf-8", errors="replace") as fp:
        for ln in fp:
            m = RE_SIMBOLO_MAPA.match(ln)
            if m:
                ender[m.group(2)] = int(m.group(1), 16) | 0x08000000
    with open(rom_bin, "rb") as fp:
        rom = fp.read()
    # Um mesmo nome pode ser definido nos DOIS lados de um `#if/#else` (ex.:
    # gMonPalette_Aron sai de normal.pal ou de normal_gba.pal). Se a dedupe caiu
    # no ramo que esta configuração NÃO compila, a ROM tem os bytes do outro
    # ramo, e isso não é defeito: é só não conferível daqui.
    vivos = {}
    for rel in arquivos_fonte():
        for d in varre(rel):
            dig = digere(d["fontes"])
            if dig:
                vivos.setdefault(d["nome"], set()).add(dig)
    ok = fora = outro_ramo = 0
    ruins = []
    for f in manifesto["familias"]:
        a_canon = ender.get(f["canonico"]["nome"])
        if a_canon is None:
            fora += 1
            continue
        corte = rom[a_canon - 0x08000000:a_canon - 0x08000000 + f["bytes"]]
        if hashlib.md5(corte).hexdigest() != f["md5"]:
            nas_fontes = vivos.get(f["canonico"]["nome"], set())
            if any(hashlib.md5(rom[a_canon - 0x08000000:
                                   a_canon - 0x08000000 + t]).hexdigest() == h
                   for h, t in nas_fontes):
                outro_ramo += 1
                continue
            ruins.append("%s: os %d B em 0x%08X não são o asset"
                         % (f["canonico"]["nome"], f["bytes"], a_canon))
            continue
        for a in f["aliases"]:
            if ender.get(a["nome"]) == a_canon:
                ok += 1
            elif a["nome"] not in ender:
                fora += 1  # --gc-sections tirou: ninguém referencia
            else:
                ruins.append("%s em 0x%08X, mas o canônico %s está em 0x%08X"
                             % (a["nome"], ender[a["nome"]],
                                f["canonico"]["nome"], a_canon))
    print("PROVA na ROM: %d aliases no MESMO endereço do canônico, com os bytes "
          "do asset conferidos por md5; %d fora da ROM; %d em ramo de #if que "
          "esta configuração não compila; %d PROBLEMAS"
          % (ok, fora, outro_ramo, len(ruins)))
    for r in ruins[:20]:
        print("  ! " + r)
    return not ruins


def demo():
    assert fontes('INCGFX_U8("graphics/x/footprint.png", ".1bpp")') == \
        [ASSETS + "graphics/x/footprint.png.1bpp"]
    assert fontes('INCGFX_COMP("g/o.png", ".4bpp", "-mwidth 8 -mheight 8")') == \
        [ASSETS + "g/o.png_mwidth_8__mheight_8.4bpp.smol"]
    assert fontes('INCBIN_U32("sound/a.bin")') == ["sound/a.bin"]
    assert prefixo(["A"], ["A", "B"]) and not prefixo(["A", "B"], ["A", "C"])
    assert not prefixo(["A"], ["!(A)"])
    d = {"dims": "[][16]", "tipo": "const u16", "nome": "gDup", "recuo": "    ",
         "bytes": 512, "md5": "abcd1234" * 4}
    linha = linha_alias(d, {"nome": "gCanon"})
    assert "gDup[ARRAY_COUNT(gCanon)][16] ASSET_ALIAS(gCanon);" in linha, linha
    d["dims"] = "[]"
    assert "gDup[ARRAY_COUNT(gCanon)] ASSET_ALIAS(gCanon);" in linha_alias(
        d, {"nome": "gCanon"})
    print("autoteste do parser: ok")
    return prova() if os.path.exists(MANIFESTO) else True


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--censo", action="store_true")
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args()
    if a.aplicar:
        aplicar()
    elif a.demo:
        sys.exit(0 if demo() else 1)
    else:
        censo()


if __name__ == "__main__":
    main()
