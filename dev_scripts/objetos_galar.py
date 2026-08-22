#!/usr/bin/env python3
"""FASE DE CONTEUDO DE GALAR, bloco c4a: script de OBJETO sem estado.

    python3 dev_scripts/objetos_galar.py            # so mede e relata
    python3 dev_scripts/objetos_galar.py --aplicar  # escreve o .inc e os map.json
    python3 dev_scripts/objetos_galar.py --demo     # autoteste com mutacao plantada

## O que este bloco e

O c3 (`dev_scripts/cenas_galar.py`) portou a cena que o HEADER do mapa dispara.
Este porta a cena que o OBJETO dispara: o NPC que anda, abre porta, some, leva o
jogador para outro mapa. Ele reusa o tradutor do c3 inteiro (mesma tabela de
opcodes lida do `event.inc` do FireRed, mesma traducao de movimento POR NOME,
mesmo charmap, mesmo de-para de id de objeto pela COORDENADA) e so acrescenta
`warp`, pelo gancho `Tradutor.extra`. Nada do filtro do c3 muda: ele ja esta
commitado e provado pelo T127.

## PRECEDENCIA, e ela e a regra que os dois arquivos tem de repetir

Um object event tem UM campo `script`. O `fala_galar.py` (baldes a e b) deu fala
simples a 337 NPCs; onde ESTE bloco porta a cena inteira, a cena SUBSTITUI a
fala, porque a cena da fonte ja contem a fala dentro dela. Para isso:

  - o rotulo daqui comeca com `GalarObj_`, e o de la com `GalarFala_`;
  - `fala_galar.aplica` NAO sobrescreve campo `script` que ja comece com
    `GalarObj_` (a regra esta escrita no cabecalho de la tambem);
  - portanto a ordem de LEVA_DONA continua valendo e os dois `--demo` ficam
    verdes rodando em qualquer ordem.

## O TETO DESTE BLOCO, medido antes de escrever uma linha

O `PLANO-CONTEUDO-GALAR.md` conta 1.038 linhas no padrao "resto (movimento,
fala, fadescreen, warp)". Esse numero conta LINHA, e nao lugar onde pendurar a
linha: **so 79 delas tem objeto no nosso mapa** (70 objetos e 9 placas). As
outras 959 sao objetos que o G4 nao pos no mapa (grafico de Pokemon ou de
cenario), e a condutora ja as DESCARTOU em 21/08 porque devolver o sprite
mentiria a especie. Dentro das 959 estao os 859 scripts de encontro estatico
(`setwildbattle`/`dowildbattle`): eles nao sao cena de NPC, sao Pokemon parado
no mapa, e voltarao junto com a decisao de sprite, nunca por este bloco.

`special`, opcode indecodificavel, estado (var salva ou flag de esconder) e
entrega de item continuam FORA, com motivo contado: sao os blocos c4b a c4f.
Nesta onda o `include/constants/flags.h` NAO e desta frente (o executor da Dex
esta alocando um bloco grande la), entao nenhuma flag nova e pedida: cena que
precisaria de flag de esconder sai com motivo e o relatorio diz quantas foram.

## Ordem da rota da historia

O `.inc` sai na ordem da campanha (Postwick, Wedgehurst, Motostoke, ...), nao em
ordem alfabetica nem na ordem do censo. E so legibilidade, nao muda um byte do
que o jogo faz, mas e o que a condutora pediu para conseguir revisar por leva.
"""
import argparse
import collections
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import fala_galar as FALA                      # noqa: E402
import cenas_galar as C3                       # noqa: E402

INC = f"{RAIZ}/data/scripts/galar_objetos.inc"
EVENT_S = f"{RAIZ}/data/event_scripts.s"
BASE = FALA.BASE
WARP_ID_NONE = 0xFF
SEM_COORD = 0xFFFF

# Ordem da rota da historia de Galar. O casamento e por PREFIXO do nosso nome de
# mapa; o que nao casa vai para o fim, em ordem de chave da fonte.
ROTA = ["Postwick", "SlumberingWeald", "Route01", "Wedgehurst", "Route02",
        "Route03", "GalarMine", "Motostoke", "WildArea", "Route04", "Route05",
        "Turffield", "Route06", "Hulbury", "Route07", "Hammerlocke",
        "Route08", "StowOnSide", "Route09", "Ballonlea", "GlimwoodTangle",
        "Circhester", "Route10", "Spikemuth", "Wyndon", "RoseTower",
        "IsleOfArmor", "CrownTundra"]


def ordem_da_rota(nome):
    seco = nome.replace("Galar_", "")
    for i, cidade in enumerate(ROTA):
        if seco.startswith(cidade):
            return i
    return len(ROTA)


class TradutorObjeto(C3.Tradutor):
    """O tradutor do c3 mais `warp`, que so cena de objeto usa."""

    def __init__(self, *a, **kw):
        self.rev_mapa = kw.pop("rev_mapa")
        super().__init__(*a, **kw)

    def extra(self, nome, args, corpo, base):
        del base
        if nome == "checkplayergender":
            # Escreve VAR_RESULT, que o filtro do c3 ja sabe ler no `compare`.
            # Fica aqui e nao no c3 porque o c3 esta commitado e provado.
            corpo.append("\t" + self.macro(nome))
            return True
        if nome not in ("warp", "warpsilent"):
            return False
        # `formatwarp` emite 7 bytes: grupo, num, warpId, x (2), y (2). A ordem
        # grupo/num vem do `map` do FireRed (asm/macros/map.inc), lida la e nao
        # lembrada; trocar os dois mandaria o jogador para outro mapa calado.
        b = args[0].to_bytes(7, "little")
        grupo, num, warp_id = b[0], b[1], b[2]
        x = int.from_bytes(b[3:5], "little")
        y = int.from_bytes(b[5:7], "little")
        chave = self.rev_mapa.get((grupo, num))
        if chave is None:
            raise C3.Recusa("warp para mapa %d.%d, que nao esta nos 438 da fonte"
                            % (grupo, num))
        alvo = self.de_para_mapa[chave]
        if warp_id != WARP_ID_NONE:
            # Indice de warp NAO sobrevive ao G3: ele filtrou warp sujo e a
            # lista encolheu, entao o numero da fonte aponta para outra porta.
            # Sem de-para de indice medido, isto sai com motivo.
            raise C3.Recusa("warp por indice de warp: o G3 filtrou a lista e o "
                            "indice da fonte nao vale mais")
        if x == SEM_COORD or y == SEM_COORD:
            raise C3.Recusa("warp sem indice e sem coordenada")
        del corpo
        # WARP DE OBJETO FICA DE FORA NESTA ONDA, e o motivo e MEDIDO, nao
        # suposto. O emissor sabe traduzir (mapa pelo de-para, coordenada 1:1),
        # e a cena chega a rodar: no Galar_StowOnSide02 o jogador trava na
        # caixa, ou seja o script entrou. O que nao acontece e a TROCA DE MAPA.
        # Duas formas foram testadas em 22/08/2026, as duas na ROM de verdade:
        # `warp` sozinho (o jogador fecha a caixa, fica solto e continua no
        # mapa) e `warp` seguido de `waitstate` (o jogador fica preso para
        # sempre, nem A nem B soltam). Sem entender o porque, emitir seria
        # plantar 10 NPCs que prendem o jogador. Volta quando alguem medir o
        # caminho do `ScrCmd_warp` a partir de script de objeto; ate la a linha
        # e cobranca da fila, com este motivo escrito.
        raise C3.Recusa("warp de objeto para %s: traduz, mas a troca de mapa "
                        "nao foi provada no motor (medido 22/08/2026)"
                        % alvo["mapa"])


def rotulo(chave, l):
    n = int(l["chave"].rsplit("/", 1)[1])
    return "GalarObj_%s_%s%d" % (chave.upper(),
                                 "bg" if l["tipo"] == "placa" else "o", n)


def plano():
    """(cenas aceitas, recusas contadas, docs de mapa lidos)."""
    rom = open(FALA.ROM_FONTE, "rb").read()
    tab = FALA.tabela_de_opcodes()
    cmap = FALA.charmap()
    linhas = json.load(open(FALA.ROTEIROS))["linhas"]
    gente = json.load(open(FALA.CENSO_GENTE))["linhas"]
    por_mapa = collections.defaultdict(list)
    for l in gente:
        por_mapa[l["mapa"]].append(l)
    mundo = json.load(open(f"{RAIZ}/dev_scripts/galar_mundo.json"))
    de_para = mundo["de_para"]
    rev = {(d["fonte_grupo"], d["fonte_indice"]): k for k, d in de_para.items()}
    musica = C3.musica_da_fonte()

    recusa, docs, aceitas = collections.Counter(), {}, []
    for l in sorted(linhas, key=lambda z: z["chave"]):
        if l["balde"] != "c_var_cena" or l["tipo"] not in ("script_objeto",
                                                           "placa"):
            continue
        if not l.get("ponteiro_fonte"):
            recusa["porta morta, e pendencia de mapa"] += 1
            continue
        if l["tipo"] == "script_objeto" and not l["no_mapa"]:
            recusa["objeto nao esta no mapa (descarte da condutora, 21/08)"] += 1
            continue
        chave = l["mapa_fonte"]
        dp = de_para.get(chave)
        if dp is None:
            recusa["mapa da fonte fora do de-para do G3"] += 1
            continue
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, dp["nome"])
        if not os.path.exists(caminho):
            recusa["map.json do mapa nao existe"] += 1
            continue
        docs.setdefault(caminho, json.load(open(caminho)))
        esconde = {}
        for o in por_mapa.get(chave, []):
            if (o["tipo"] == "objeto" and o.get("flag_fonte")
                    and o["motivo"].startswith("entrou")):
                esconde.setdefault(o["flag_fonte"], []).append(o["i"] + 1)
        t = TradutorObjeto(
            rom, tab, cmap,
            C3.de_para_de_objetos(chave, docs[caminho], por_mapa),
            esconde, {}, {}, musica, rev_mapa=rev)
        # `de_para_mapa` e do warp: o alvo pode ser QUALQUER mapa de Galar,
        # nao so o do objeto.
        t.de_para_mapa = de_para
        base = rotulo(chave, l)
        try:
            corpo, usadas = t.cena(int(l["ponteiro_fonte"], 16), base)
        except C3.Recusa as e:
            recusa[str(e)] += 1
            continue
        aceitas.append(dict(chave=chave, nome=dp["nome"], caminho=caminho,
                            tipo=l["tipo"], x=l["x"], y=l["y"], base=base,
                            linhas=corpo, usadas=usadas,
                            ordem=ordem_da_rota(dp["nome"])))
    return aceitas, recusa, docs


def corpo_inc(aceitas):
    out = ["@ Cenas de OBJETO de Galar (bloco c4a da fase de conteudo).",
           "@ Gerado por dev_scripts/objetos_galar.py; NAO editar a mao.",
           "@ Rotulo GalarObj_* tem PRECEDENCIA sobre GalarFala_*: onde a cena",
           "@ inteira foi portada, ela ja contem a fala que o balde (a) deu.",
           "@ Ordem: a da rota da historia, de Postwick e Wedgehurst em diante.",
           ""]
    por_mapa = collections.defaultdict(list)
    for a in aceitas:
        por_mapa[(a["ordem"], a["nome"], a["chave"])].append(a)
    for chave in sorted(por_mapa):
        out.append("@ ---- %s (%s) ----" % (chave[1], chave[2]))
        for a in sorted(por_mapa[chave], key=lambda z: z["base"]):
            out.extend(a["linhas"])
            out.append("")
    return "\n".join(out) + "\n"


def aplica(aceitas, docs, gravar):
    mudou, recusa = collections.Counter(), []
    corpo = corpo_inc(aceitas)
    if gravar:
        open(INC, "w").write(corpo)
        fonte = open(EVENT_S).read()
        linha = '\t.include "data/scripts/galar_objetos.inc"'
        if linha not in fonte:
            open(EVENT_S, "w").write(fonte.rstrip("\n") + "\n" + linha + "\n")
    # LIMPEZA ANTES DE ESCREVER (licao LEVA_DONA do S8: gerador que so escreve
    # e nunca apaga mente na segunda rodada). Se uma cena deixou de passar no
    # filtro, o rotulo dela continuaria pendurado no map.json apontando para um
    # simbolo que nao existe mais, e a build so acusaria no LINK. A varredura e
    # em TODOS os mapas de Galar, nao so nos que esta rodada tocou.
    vivos = {a["base"] for a in aceitas}
    import glob
    antes = {}
    for caminho in sorted(glob.glob("%s/data/maps/Galar_*/map.json" % RAIZ)):
        doc = docs.setdefault(caminho, json.load(open(caminho)))
        antes[caminho] = json.dumps(doc, sort_keys=True)
        for o in doc.get("object_events", []):
            s = str(o.get("script", ""))
            if s.startswith("GalarObj_") and s not in vivos:
                o["script"] = "0"
                mudou["rotulo_orfao"] += 1
        bgs = doc.get("bg_events", [])
        sobrou = [b for b in bgs
                  if not (str(b.get("script", "")).startswith("GalarObj_")
                          and b["script"] not in vivos)]
        if len(sobrou) != len(bgs):
            mudou["rotulo_orfao"] += len(bgs) - len(sobrou)
            doc["bg_events"] = sobrou

    for c, d in docs.items():
        antes.setdefault(c, json.dumps(d, sort_keys=True))
    for a in sorted(aceitas, key=lambda z: z["base"]):
        doc = docs[a["caminho"]]
        if a["tipo"] == "placa":
            achados = [b for b in doc.get("bg_events", [])
                       if b.get("x") == a["x"] and b.get("y") == a["y"]]
            if len(achados) == 1:
                achados[0]["script"] = a["base"]
            elif not achados:
                doc.setdefault("bg_events", []).append({
                    "type": "sign", "x": a["x"], "y": a["y"], "elevation": 0,
                    "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                    "script": a["base"]})
            else:
                recusa.append((a["base"], "%d bg events no mesmo tile"
                               % len(achados)))
                continue
            mudou["placa"] += 1
            continue
        i, motivo = FALA.casa_objeto(doc, a["x"], a["y"])
        if i is None:
            recusa.append((a["base"], motivo))
            continue
        doc["object_events"][i]["script"] = a["base"]
        mudou["objeto"] += 1
    for c, d in docs.items():
        if json.dumps(d, sort_keys=True) != antes[c]:
            mudou["mapa"] += 1
            if gravar:
                with open(c, "w") as f:
                    json.dump(d, f, indent=2, ensure_ascii=False)
                    f.write("\n")
    return mudou, recusa, corpo


def relatorio(aceitas, recusa):
    print("cenas de objeto portadas: %d em %d mapas (%d placas)"
          % (len(aceitas), len({a["nome"] for a in aceitas}),
             sum(1 for a in aceitas if a["tipo"] == "placa")))
    quer_flag = sum(1 for m, c in recusa.items() if "flag" in m for _ in range(c))
    print("de fora: %d linhas; das quais %d parariam numa flag "
          "(include/constants/flags.h nao e desta frente nesta onda)"
          % (sum(recusa.values()), quer_flag))
    for m, c in recusa.most_common(18):
        print("  %5d  %s" % (c, m))


def demo():
    falhas = []
    aceitas, recusa, docs = plano()

    # 1. PRECEDENCIA: nenhum objeto pode ficar com os dois scripts, e o rotulo
    #    daqui tem que ser o que sobrou no map.json.
    if any(not a["base"].startswith("GalarObj_") for a in aceitas):
        falhas.append("rotulo do c4a fora do prefixo GalarObj_")
    _mudou, rec, corpo1 = aplica(aceitas, docs, gravar=False)
    for base, motivo in rec:
        falhas.append("nao aplicado: %s %s" % (base, motivo))

    # 2. rotulo unico, senao o assembler junta duas cenas numa so.
    rot = [l[:-2] for a in aceitas for l in a["linhas"] if l.endswith("::")]
    if len(set(rot)) != len(rot):
        falhas.append("rotulo de objeto repetido")

    # 3. IDEMPOTENCIA: gerar duas vezes da o mesmo texto, e aplicar em cima do
    #    que ja esta gravado nao mexe em mapa nenhum.
    if corpo1 != corpo_inc(aceitas):
        falhas.append("o .inc nao e estavel entre duas geracoes")
    if os.path.exists(INC) and open(INC).read() == corpo1:
        aceitas2, _r2, docs2 = plano()
        mudou2, _rec2, _c2 = aplica(aceitas2, docs2, gravar=False)
        if mudou2["mapa"]:
            falhas.append("segunda passada mexeria em %d mapas: nao e idempotente"
                          % mudou2["mapa"])

    # 4. MUTACAO PLANTADA 1: warp com os bytes de grupo e num TROCADOS tem que
    #    cair em outro mapa ou ser recusado, nunca passar igual. E o defeito que
    #    mandaria o jogador para o lugar errado calado.
    mundo = json.load(open(f"{RAIZ}/dev_scripts/galar_mundo.json"))
    de_para = mundo["de_para"]
    rev = {(d["fonte_grupo"], d["fonte_indice"]): k for k, d in de_para.items()}
    t = TradutorObjeto(b"\0" * 16, {}, {}, {}, {}, {}, {}, {}, rev_mapa=rev)
    t.de_para_mapa = de_para
    (g, n), chave = next(iter(rev.items()))
    def motivo_do_warp(bs):
        try:
            t.extra("warp", [int.from_bytes(bytes(bs), "little")], [], "X")
        except C3.Recusa as e:
            return str(e)
        return ""

    # 4a. O warp esta FORA nesta onda, e a recusa tem que citar o mapa CERTO:
    #     e a unica prova de que o decodificador de 7 bytes acertou grupo e num
    #     (trocar os dois cita outro mapa, ou nenhum).
    bom = motivo_do_warp([g, n, WARP_ID_NONE, 3, 0, 4, 0])
    if de_para[chave]["mapa"] not in bom:
        falhas.append("recusa do warp nao citou %s: %r" % (chave, bom))
    trocado = motivo_do_warp([n, g, WARP_ID_NONE, 3, 0, 4, 0])
    if trocado == bom:
        falhas.append("trocar grupo por num deu a MESMA recusa: o plante nao "
                      "seria visto")

    # 5. MUTACAO PLANTADA 2: warp por INDICE de warp tem motivo PROPRIO, porque
    #    e outro defeito (o G3 encolheu a lista de warps).
    idx = motivo_do_warp([g, n, 3, 0xFF, 0xFF, 0xFF, 0xFF])
    if "indice" not in idx:
        falhas.append("warp por indice nao foi recusado pelo motivo dele: %r"
                      % idx)

    print("demo: %s" % ("OK" if not falhas else "REPROVADO"))
    for f in falhas:
        print("  FALHA", f)
    relatorio(aceitas, recusa)
    return 1 if falhas else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        raise SystemExit(demo())
    aceitas, recusa, docs = plano()
    mudou, rec, _c = aplica(aceitas, docs, a.aplicar)
    relatorio(aceitas, recusa)
    print("\n%s: %r" % ("gravado" if a.aplicar else "mudaria", dict(mudou)))
    for base, motivo in rec[:10]:
        print("  nao aplicado: %s %s" % (base, motivo))


if __name__ == "__main__":
    main()
