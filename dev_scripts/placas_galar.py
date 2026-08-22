#!/usr/bin/env python3
"""FASE DE CONTEUDO DE GALAR: as PLACAS que sobraram no balde c.

    python3 dev_scripts/placas_galar.py            # so mede e relata
    python3 dev_scripts/placas_galar.py --aplicar  # escreve o .inc e os map.json
    python3 dev_scripts/placas_galar.py --demo     # autoteste

## Por que existe um script so para placa

O balde (a) do `fala_galar.py` ja pos 52 placas: as cujo script da fonte SO
mostra texto. As outras 66 cairam no balde (c) porque o script delas tambem
mexe em estado (`setvar`, `special`, `dofieldeffect`, `setmetatile`). Isso e
bloqueio de OBJETO, nao de PLACA, e a diferenca e o ponto deste bloco:

**Uma placa diz o que diz.** Um bg_event de tipo `sign` no nosso motor abre a
caixa, mostra o texto e fecha (`Std_MsgboxSign` tranca e solta sozinho). Ele nao
anda, nao some, nao entrega item e nao guarda estado. Entao o estado que o
script da fonte carrega ao lado do texto **nao tem onde caber numa placa**: ou
ele pertence a outra coisa do mapa (a maquina de slot fica no objeto, nao na
tabuleta que fala dela), ou ele e maquinaria do motor do demake que esta ROM nao
tem. Portar so o texto nao e porte parcial disfarcado: e o contrato inteiro do
que uma placa faz.

Esse contrato ja estava em uso, e nao e invencao desta onda: as 52 placas do
balde (a) sao emitidas assim mesmo, com `lock/faceplayer` da fonte DESCARTADOS
(ver o comentario em `fala_galar.corpo_inc`, "PLACA usa MSGBOX_SIGN e nada
mais"). Este bloco so estende o mesmo contrato as que o filtro de OBJETO tinha
barrado.

## O que continua de fora, e por que

- **Placa sem texto aproveitavel.** Sem texto nao ha placa: inventar frase seria
  escrever conteudo que a fonte nao tem.
- **Placa cujo bytecode nao decodifica** (`opcode 0xFF`, que e enchimento de
  espaco livre): o ponteiro nao aponta para script nenhum.
- **Os 68 registros de bg da fonte SEM ponteiro de script.** Eles entram no
  denominador da regua (sao bg de verdade na fonte) e nao tem uma letra para
  mostrar. Ficam de fora contados; 33 deles ja estao no mapa como
  `hidden_item` do G4, que nao precisa de script.

## Precedencia

O campo `script` de um bg_event e unico, como o de objeto. A ordem e:
`GalarTrn_` (batalha) > `GalarObj_` (cena) > `GalarFala_` (fala) > `GalarPlaca_`
(este bloco). Este script NUNCA sobrescreve um bg que ja tenha script, e nunca
grava duas vezes na mesma coordenada.
"""
import argparse
import collections
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import fala_galar as FALA   # noqa: E402

INC = f"{RAIZ}/data/scripts/galar_placas.inc"
EVENT_S = f"{RAIZ}/data/event_scripts.s"
ANTES = ("GalarTrn_", "GalarObj_", "GalarFala_")


def rotulo(chave):
    """GalarPlaca_<MAPA DA FONTE>_bg<N>, o padrao que a fila sabe ler."""
    mapa, tipo, i = chave.split("/")
    return "GalarPlaca_%s_%s%d" % (mapa.upper(),
                                   "bg" if tipo == "bg" else "o", int(i))


def plano(incluir_feitas=False):
    """(aceitas, recusa). So placa do balde c com texto de verdade.

    `incluir_feitas` e so do `--demo`: depois de um `--aplicar` toda placa deste
    bloco vira `feita` e o plano fica VAZIO, o que reprovava um gerador
    idempotente e correto (medido em 22/08/2026, no fechamento da rodada 7).
    Com ela o autoteste volta a ver a lista inteira e julga o que foi colocado,
    em vez de julgar o que ainda falta colocar.
    """
    rom, tab, cmap, fila = FALA.carrega()
    linhas = FALA.varre(rom, tab, cmap, fila)
    aceitas, recusa = [], collections.Counter()
    for l in sorted(linhas, key=lambda z: z["chave"]):
        if l["tipo"] != "placa" or l["balde"] != "c_var_cena":
            continue
        if l["status"] == "feita" and not incluir_feitas:
            recusa["placa que outro balde ja colocou"] += 1
            continue
        p = l.get("ponteiro_fonte")
        if not p:
            recusa["bg da fonte sem ponteiro de script"] += 1
            continue
        r = FALA.desmonta(rom, tab, int(p, 16))
        textos, motivo = [], None
        vistos = set()
        for off, _tipo in r.textos:
            if off in vistos:
                continue
            vistos.add(off)
            t, mot = FALA.texto(rom, cmap, off)
            if mot:
                motivo = motivo or mot
                continue
            if t.strip():
                textos.append(t)
        if not textos:
            recusa["sem texto aproveitavel" + (": " + motivo if motivo else "")] += 1
            continue
        aceitas.append(dict(l, rotulo=rotulo(l["chave"]), texto_placa=textos[0],
                            n_textos=len(textos)))
    return aceitas, recusa


def corpo_inc(aceitas):
    out = ["@ Placas de Galar que sobraram do balde c da fase de conteudo.",
           "@ Gerado por dev_scripts/placas_galar.py; NAO editar a mao.",
           "@ Uma placa diz o que diz: MSGBOX_SIGN e mais nada. O estado que o",
           "@ script da fonte carrega ao lado do texto nao cabe numa placa.",
           ""]
    por_mapa = collections.defaultdict(list)
    for l in aceitas:
        por_mapa[l["mapa"]].append(l)
    for mapa in sorted(por_mapa):
        out.append("@ ---- %s ----" % mapa)
        for l in sorted(por_mapa[mapa], key=lambda z: z["chave"]):
            r = l["rotulo"]
            out += ["%s::" % r,
                    "\tmsgbox %s_Text, MSGBOX_SIGN" % r,
                    "\tend", "",
                    "%s_Text:" % r,
                    '\t.string "%s$"' % l["texto_placa"], ""]
    return "\n".join(out) + "\n"


def aplica(aceitas, gravar):
    mudou, recusa = collections.Counter(), []
    por_mapa = collections.defaultdict(list)
    for l in aceitas:
        por_mapa[l["mapa"]].append(l)
    for mapa, lista in sorted(por_mapa.items()):
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, mapa)
        if not os.path.exists(caminho):
            recusa.append({"chave": mapa, "motivo": "map.json nao existe"})
            continue
        doc = json.load(open(caminho))
        antes = json.dumps(doc, sort_keys=True)
        bgs = doc.setdefault("bg_events", [])
        ja = {b.get("script") for b in bgs}
        ocupado = {(b.get("x"), b.get("y")) for b in bgs}
        for l in sorted(lista, key=lambda z: z["chave"]):
            if l["rotulo"] in ja:
                continue
            if (l["x"], l["y"]) in ocupado:
                recusa.append({"chave": l["chave"],
                               "motivo": "ja ha bg em (%d,%d)" % (l["x"], l["y"])})
                continue
            bgs.append({"type": "sign", "x": l["x"], "y": l["y"], "elevation": 0,
                        "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                        "script": l["rotulo"]})
            ocupado.add((l["x"], l["y"]))
            mudou["placa"] += 1
        if json.dumps(doc, sort_keys=True) != antes:
            mudou["mapa"] += 1
            if gravar:
                with open(caminho, "w") as f:
                    json.dump(doc, f, indent=2, ensure_ascii=False)
                    f.write("\n")
    if gravar:
        open(INC, "w").write(corpo_inc(aceitas))
        s = open(EVENT_S).read()
        linha = '\t.include "data/scripts/galar_placas.inc"'
        if linha not in s:
            open(EVENT_S, "w").write(s.rstrip("\n") + "\n" + linha + "\n")
    return mudou, recusa


def ja_no_mapa(aceitas):
    """Quantas das aceitas ja estao gravadas como bg_event no map.json."""
    n = 0
    for l in aceitas:
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, l["mapa"])
        if not os.path.exists(caminho):
            continue
        bgs = json.load(open(caminho)).get("bg_events") or []
        n += any(b.get("script") == l["rotulo"] for b in bgs)
    return n


def demo():
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print("  %-62s %s" % (nome, "ok" if cond else "REPROVOU"))
        ok = ok and cond

    aceitas, recusa = plano(incluir_feitas=True)
    caso("o plano aceita mais de 30 placas", len(aceitas) > 30)
    caso("toda placa aceita tem texto nao vazio",
         all(l["texto_placa"].strip() for l in aceitas))
    caso("nenhuma chave repete", len({l["chave"] for l in aceitas}) == len(aceitas))
    corpo = corpo_inc(aceitas)
    caso("todo rotulo do .inc aparece uma vez so",
         all(corpo.count("\n%s::" % l["rotulo"]) == 1 for l in aceitas))
    caso("o .inc so emite MSGBOX_SIGN",
         "MSGBOX_" in corpo and "MSGBOX_DEFAULT" not in corpo
         and "MSGBOX_NPC" not in corpo)
    caso("nenhuma placa emite lock/faceplayer",
         "faceplayer" not in corpo and "\tlock" not in corpo)
    # PRECEDENCIA: coordenada que ja tem bg de outro balde e RECUSADA, nunca
    # sobrescrita. O par negativo e uma placa plantada em cima de um bg que ja
    # existe: ela tem de sair na lista de recusa e nao entrar no mapa.
    mudou, rec = aplica(aceitas, gravar=False)
    caso("a aplicacao seca coloca mais de 30, ou elas ja estao no mapa",
         mudou["placa"] + ja_no_mapa(aceitas) > 30)
    vitima = None
    for l in aceitas:
        d = json.load(open("%s/data/maps/%s/map.json" % (RAIZ, l["mapa"])))
        bgs = d.get("bg_events") or []
        if bgs:
            vitima = dict(l, x=bgs[0]["x"], y=bgs[0]["y"])
            break
    caso("achou onde plantar o par negativo", vitima is not None)
    if vitima:
        _m, _r = aplica([vitima], gravar=False)
        caso("placa plantada em cima de bg existente e RECUSADA",
             _m["placa"] == 0 and any("ja ha bg" in x["motivo"] for x in _r))
    # PAR NEGATIVO: rodar duas vezes nao pode dobrar nada.
    caso("aplicar de novo sobre o mesmo estado nao inventa placa",
         aplica(aceitas, gravar=False)[0]["placa"] == mudou["placa"])
    print("\n%s" % ("demo verde" if ok else "DEMO REPROVOU"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    aceitas, recusa = plano()
    print("placas portadas do balde c: %d em %d mapas"
          % (len(aceitas), len({l["mapa"] for l in aceitas})))
    print("de fora: %d" % sum(recusa.values()))
    for m, n in recusa.most_common():
        print("  %4d  %s" % (n, m))
    mudou, rec = aplica(aceitas, gravar=a.aplicar)
    print("mudaria: %s | recusas de colocacao: %d" % (dict(mudou), len(rec)))
    for r in rec[:8]:
        print("   %s: %s" % (r["chave"], r["motivo"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
