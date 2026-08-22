#!/usr/bin/env python3
"""Liga as item balls de Johto que entraram sem item, quando a fonte diz qual é.

Último elo do encadeamento que começa em `completa_objetos_johto.py`. Aquele
gerador põe o objeto que faltava no estado do sanitize (bola muda);
`restaura_gfx_johto.py` dá gráfico a quem não é gente e `restaura_npcs_johto.py`
dá identidade a quem é. Sobra uma família que nenhum dos dois atende: a bola que
a fonte diz ser BOLA MESMO. Para essas, `restaura_gfx_johto` escreve no censo
"a fonte diz BOLA aqui, já está certo" e para, porque dar item é outra decisão.

MEDIDO em 22/08/2026: são 5, e a fonte nomeia o item de todas em uma linha
(`SlowpokeWell_B1F_EventScript_Item_Great_Ball:: finditem ITEM_GREAT_BALL`).

A REGRA, e ela é estreita de propósito: só entra bola cujo script na fonte seja
**exatamente** um `finditem` seguido de `end`, e cujo item EXISTA nesta build.
Qualquer coisa além disso (condição, cena, item que não existe aqui) é recusada
com o motivo. Não há adivinhação de item em lugar nenhum: item que a fonte não
nomeia não vira bola, vira linha de relatório.

A FLAG, e por que ela não sai da faixa das item balls

`dev_scripts/liga_bolas_johto.py` tem a faixa `FLAG_ITEM_BALLS_JSU_START` e ela
ACABOU (`teto_da_faixa()` devolve 0x0A1 e o próximo offset seria 0x0A6). Mover
essa fronteira é operação de 1.375 linhas em `flags.h` e o próprio arquivo diz
que quem gerar bola nova NÃO pode entrar lá em append. Então estas 4 usam a
faixa de TRANSBORDO de Johto (0x1D0E em diante, seção 0.a do
`PENDENCIAS-JOHTO.md`), apelidando `FLAG_UNUSED` que já existe: `FLAGS_COUNT`
não muda e a save fica intacta. É a mesma faixa que o `completa_placas_johto.py`
e o `arco_farol_johto.py` usam nesta rodada.

Uso:
    python3 dev_scripts/bolas_faltantes_johto.py            # só relata
    python3 dev_scripts/bolas_faltantes_johto.py --aplica   # escreve
    python3 dev_scripts/bolas_faltantes_johto.py --demo     # autoteste
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))

import restaura_npcs_johto as RN  # noqa: E402  HNS, mapas_de_johto
import restaura_gfx_johto as RG   # noqa: E402  eh_mudo, grava_como_estava

HNS = RN.HNS
APLICA = "--aplica" in sys.argv
DEMO = "--demo" in sys.argv

FLAGS_H = os.path.join(REPO, "include/constants/flags.h")
ITEMS_H = os.path.join(REPO, "include/constants/items.h")
MARCA = "@ Item balls ligadas por dev_scripts/bolas_faltantes_johto.py"
MARCA_C = "// ITEM BALLS DE JOHTO (dev_scripts/bolas_faltantes_johto.py)"

BOLAS = ("OBJ_EVENT_GFX_ITEM_BALL", "OBJ_EVENT_GFX_POKE_BALL")
SO_FINDITEM = re.compile(r"^\s*finditem\s+(ITEM_\w+)\s*$\s*^\s*end\s*$",
                         re.M)


def itens_do_build(_cache=set()):
    if not _cache:
        txt = open(ITEMS_H, encoding="utf-8").read()
        _cache.update(re.findall(r"^\s*(ITEM_\w+)\s*=", txt, re.M))
        _cache.update(re.findall(r"^#define\s+(ITEM_\w+)", txt, re.M))
    return _cache


def item_do_rotulo(texto_fonte, rotulo):
    """ITEM_X se o script for exatamente `finditem ITEM_X` + `end`."""
    m = re.search(rf"^{re.escape(rotulo)}::?\s*$\n((?:(?!^\w+::?\s*$).*\n)*)",
                  texto_fonte, re.M)
    if not m:
        return None, "rotulo nao existe na fonte"
    corpo = "\n".join(l.split("@")[0] for l in m.group(1).splitlines()
                      if l.strip())
    achou = SO_FINDITEM.match(corpo + "\n")
    if not achou:
        return None, "o script da fonte nao e um finditem simples"
    item = achou.group(1)
    if item not in itens_do_build():
        return None, f"{item} nao existe nesta build"
    return item, None


def apelido(mapa, item, usados):
    base = ("FLAG_ITEM_JOHTO_" + re.sub(r"\W", "", mapa.upper()) + "_"
            + item[len("ITEM_"):])
    nome, n = base, 1
    while nome in usados:
        n += 1
        nome = f"{base}_{n}"
    usados.add(nome)
    return nome


def monta():
    txt_flags = open(FLAGS_H, encoding="utf-8").read()
    usados = set(re.findall(r"^#define\s+(FLAG_\w+)", txt_flags, re.M))
    plano, censo = {}, []
    for mapa in sorted(RN.mapas_de_johto()):
        p = os.path.join(REPO, "data/maps", mapa, "map.json")
        fp = os.path.join(HNS, "data/maps", mapa, "map.json")
        fi = os.path.join(HNS, "data/maps", mapa, "scripts.inc")
        if not (os.path.exists(p) and os.path.exists(fp)):
            continue
        dados = json.load(open(p, encoding="utf-8"))
        fonte = json.load(open(fp, encoding="utf-8")).get("object_events", [])
        por_coord = {}
        for o in fonte:
            por_coord.setdefault((o["x"], o["y"]), []).append(o)
        texto = open(fi, encoding="utf-8").read() if os.path.exists(fi) else ""
        novas = []
        for o in dados.get("object_events", []):
            if not RG.eh_mudo(o):
                continue
            cands = [c for c in por_coord.get((o["x"], o["y"]), [])
                     if c.get("graphics_id") in BOLAS]
            if not cands:
                continue
            rotulo = cands[0].get("script")
            linha = {"mapa": mapa, "x": o["x"], "y": o["y"], "rotulo": rotulo}
            if not rotulo or rotulo in ("NULL", "0"):
                linha["motivo"] = "a bola da fonte nao tem script"
                censo.append(linha)
                continue
            item, motivo = item_do_rotulo(texto, rotulo)
            if motivo:
                linha["motivo"] = motivo
                censo.append(linha)
                continue
            flag = apelido(mapa, item, usados)
            o["graphics_id"] = "OBJ_EVENT_GFX_ITEM_BALL"
            o["script"] = rotulo
            o["flag"] = flag
            linha.update(item=item, flag=flag, entrou=True)
            novas.append((rotulo, item))
            censo.append(linha)
        if novas:
            plano[mapa] = (dados, novas)
    return plano, censo


def escreve(plano):
    linhas_flag = []
    for mapa, (dados, novas) in plano.items():
        RG.grava_como_estava(
            os.path.join(REPO, "data/maps", mapa, "map.json"), dados)
        p = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
        atual = open(p, encoding="utf-8").read()
        if MARCA in atual:
            continue
        corpo = [MARCA]
        for rotulo, item in novas:
            corpo.append(f"{rotulo}::")
            corpo.append(f"\tfinditem {item}")
            corpo.append("\tend")
            corpo.append("")
        with open(p, "w", encoding="utf-8") as f:
            f.write(atual.rstrip("\n") + "\n\n" + "\n".join(corpo))
    return linhas_flag


def escreve_flags(censo):
    """Apelida as flags novas em flags.h, relendo o arquivo na hora."""
    novas = [l for l in censo if l.get("entrou")]
    if not novas:
        return []
    txt = open(FLAGS_H, encoding="utf-8").read()
    ocupadas = {int(h, 16) for h in
                re.findall(r"^#define\s+\w+\s+FLAG_UNUSED_0x([0-9A-Fa-f]+)",
                           txt, re.M)}
    linhas, feito = [], []
    for l in novas:
        if re.search(rf"^#define\s+{l['flag']}\b", txt, re.M):
            feito.append(f"{l['flag']}: ja existe")
            continue
        alvo = None
        for n in range(0x1D0E, 0x2026):
            if n in ocupadas:
                continue
            if not re.search(rf"^#define\s+FLAG_UNUSED_0x{n:X}\b", txt, re.M):
                continue
            alvo = n
            break
        if alvo is None:
            raise SystemExit("faixa de transbordo de Johto sem vaga")
        ocupadas.add(alvo)
        linhas.append(f"#define {l['flag']:56} FLAG_UNUSED_0x{alvo:X}")
        feito.append(f"{l['flag']} = FLAG_UNUSED_0x{alvo:X}  ({l['item']})")
    if linhas and APLICA:
        atual = open(FLAGS_H, encoding="utf-8").read()
        bloco = ("\n" + MARCA_C + "\n"
                 "// Apelido de FLAG_UNUSED que ja existe: FLAGS_COUNT nao "
                 "muda, save intacta.\n" + "\n".join(linhas) + "\n")
        with open(FLAGS_H, "w", encoding="utf-8") as f:
            f.write(atual.rstrip("\n") + "\n" + bloco)
    return feito


def demo():
    """A régua do `finditem` simples, que é a única coisa que decide aqui."""
    fonte = ("X::\n\tfinditem ITEM_GREAT_BALL\n\tend\n\n"
             "Y::\n\tlock\n\tfinditem ITEM_GREAT_BALL\n\tend\n\n"
             "Z::\n\tfinditem ITEM_QUE_NAO_EXISTE\n\tend\n")
    assert item_do_rotulo(fonte, "X") == ("ITEM_GREAT_BALL", None)
    assert item_do_rotulo(fonte, "Y")[0] is None, "script com cena tem que cair"
    assert item_do_rotulo(fonte, "Z")[0] is None, "item inexistente tem que cair"
    assert item_do_rotulo(fonte, "W")[0] is None, "rotulo ausente tem que cair"
    assert "ITEM_GREAT_BALL" in itens_do_build()
    assert "ITEM_TM_SHOCK_WAVE" not in itens_do_build(), (
        "se este item passou a existir, a bola de OlivineCity (53,47) deixou "
        "de ser recusa e o relatorio desta rodada envelheceu")

    plano, censo = monta()
    entram = [l for l in censo if l.get("entrou")]
    # nenhuma flag repetida, senao dois objetos dividem o mesmo bit e pegar um
    # apaga o outro
    flags = [l["flag"] for l in entram]
    assert len(flags) == len(set(flags)), "flag repetida entre duas bolas"
    print(f"demo ok: {len(entram)} bolas entrariam, "
          f"{len(censo) - len(entram)} recusadas")


def main():
    if DEMO:
        demo()
        return 0
    plano, censo = monta()
    entram = [l for l in censo if l.get("entrou")]
    print(f"bolas ligadas: {len(entram)}   recusadas: "
          f"{len(censo) - len(entram)}\n")
    for l in censo:
        if l.get("entrou"):
            print(f"  OK  {l['mapa']:30} ({l['x']},{l['y']}) {l['item']}")
        else:
            print(f"  NAO {l['mapa']:30} ({l['x']},{l['y']}) {l['motivo']}")
    print("\nflags:")
    for f in escreve_flags(censo):
        print(f"   {f}")
    if APLICA:
        escreve(plano)
        print("\nescrito.")
    else:
        print("\n(nada escrito; rode com --aplica)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
