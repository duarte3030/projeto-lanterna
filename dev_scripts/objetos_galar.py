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
import guarda_colisao_vars as GUARDA           # noqa: E402

INC = f"{RAIZ}/data/scripts/galar_objetos.inc"
EVENT_S = f"{RAIZ}/data/event_scripts.s"
BASE = FALA.BASE
WARP_ID_NONE = 0xFF
SEM_COORD = 0xFFFF

# Faixa de Galar para as flags de ESCONDER do bloco c4b. 0x1C00-0x1C20 sao os
# itens escondidos do G4, 0x1C21-0x1C58 as bolas do fala_galar.py, 0x1C59 a
# FLAG_HIDE_GIRATINA e 0x1CFF a FLAG_GALAR_QA_ANDAR. Comeca em 0x1C80 com folga
# de proposito, para uma leva nova de bolas nao encostar aqui.
PRIMEIRA_FLAG_ESCONDE = 0x1C80
ULTIMA_FLAG_ESCONDE = 0x1CFE

MARCA_FLAG_INI = ("// >>> Fase de conteudo de Galar, bloco c4b: flags de esconder "
                  "(dev_scripts/objetos_galar.py) >>>")
MARCA_FLAG_FIM = "// <<< Fase de conteudo de Galar, bloco c4b <<<"
MARCA_VAR_INI = ("// >>> Fase de conteudo de Galar, bloco c4d: vars de etapa de "
                 "objeto (dev_scripts/objetos_galar.py) >>>")
MARCA_VAR_FIM = "// <<< Fase de conteudo de Galar, bloco c4d <<<"
FLAGS_H = f"{RAIZ}/include/constants/flags.h"
VARS_H = f"{RAIZ}/include/constants/vars.h"

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
        G = FALA._gente()
        self.itens_fonte = G.itens_da_fonte()
        self.itens_nossos = G.nossos_itens()
        self.especies_fonte = C3.constantes(
            f"{C3.PKFR}/include/constants/species.h", "SPECIES")
        self.especies_nossas = set(re.findall(
            r"\bSPECIES_[A-Z0-9_]+\b",
            open(f"{RAIZ}/include/constants/species.h").read()))

    def item(self, ident):
        nome = self.itens_fonte.get(ident)
        if nome is None or nome not in self.itens_nossos:
            raise C3.Recusa("item %d da fonte sem equivalente no nosso items.h"
                            % ident)
        return nome

    def especie(self, ident):
        """Nome da especie, NUNCA o numero.

        O id interno do Gen 3 nao e o da Pokedex nacional, e o nosso motor
        numera por nacional: traduzir por VALOR daria outro Pokemon a partir de
        Treecko. Por nome o assembler resolve, e nome que nao existe aqui
        recusa a cena em vez de entregar bicho errado.
        """
        nome = self.especies_fonte.get(ident)
        if nome is None or nome not in self.especies_nossas:
            raise C3.Recusa("especie %d da fonte sem nome no nosso species.h"
                            % ident)
        return nome

    def lista_de_loja(self, ptr, base):
        """Rotulo da lista `.2byte ITEM_*` da loja, terminada por ITEM_NONE."""
        if not (BASE <= ptr < BASE + len(self.rom)):
            raise C3.Recusa("lista de loja fora da rom")
        off, itens = ptr - BASE, []
        for i in range(32):
            v = int.from_bytes(self.rom[off + i * 2:off + i * 2 + 2], "little")
            if v == 0:
                break
            itens.append(self.item(v))
        else:
            raise C3.Recusa("lista de loja sem fim")
        if not itens:
            raise C3.Recusa("lista de loja vazia")
        rot = "%s_Mart%d" % (base, len(self.extras_gancho))
        self.extras_gancho.extend(["\t.align 2", "%s:" % rot]
                                  + ["\t.2byte %s" % i for i in itens]
                                  + ["\t.2byte ITEM_NONE"])
        return rot

    def extra(self, nome, args, corpo, base):
        if nome == "givemon":
            corpo.append("\t%s %s, %d, %s" % (self.macro(nome),
                                              self.especie(args[0]), args[1],
                                              self.item(args[2]) if args[2]
                                              else "ITEM_NONE"))
            return True
        if nome == "giveegg":
            corpo.append("\t%s %s" % (self.macro(nome), self.especie(args[0])))
            return True
        if nome in ("additem", "removeitem", "checkitem", "checkitemspace"):
            corpo.append("\t%s %s, %d" % (self.macro(nome), self.item(args[0]),
                                          args[1]))
            return True
        if nome == "bufferitemname":
            corpo.append("\t%s %d, %s" % (self.macro(nome), args[0],
                                          self.item(args[1])))
            return True
        if nome == "pokemart":
            corpo.append("\t%s %s" % (self.macro(nome),
                                      self.lista_de_loja(args[0], base)))
            return True
        if nome == "playmoncry":
            corpo.append("\t%s %s, %d" % (self.macro(nome),
                                          self.especie(args[0]), args[1]))
            return True
        if nome == "showmonpic":
            corpo.append("\t%s %s, %d, %d" % (self.macro(nome),
                                              self.especie(args[0]), args[1],
                                              args[2]))
            return True
        if nome == "message":
            rot = "%s_Msg%d" % (base, len(self.extras_gancho))
            self.extras_gancho.extend(self.texto(args[0], rot))
            corpo.append("\t%s %s" % (self.macro(nome), rot))
            return True
        if nome in ("showmoneybox", "showcoinsbox", "hidecoinsbox",
                    "updatecoinsbox"):
            corpo.append("\t%s %d, %d" % (self.macro(nome), args[0], args[1]))
            return True
        if nome in ("hidemoneybox", "updatemoneybox"):
            # No FireRed os dois levam x/y; aqui `hidemoneybox` nao leva nada e
            # `updatemoneybox` leva so o `disable`. Traduzir e DESCARTAR a
            # coordenada, que e do layout da caixa e nao da cena.
            corpo.append("\t" + self.macro(nome))
            return True
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
    """(aceitas, recusas, docs, flags alocadas, vars alocadas).

    DUAS PASSADAS, pelo mesmo motivo do c3: a primeira usa nome de FLAG e de VAR
    de ensaio so para descobrir quais cenas passam no filtro e o que cada uma
    consome; a segunda escreve com os nomes de verdade. Endereco so e gasto por
    cena que ENTROU, e a ordem de alocacao e a da chave da FONTE, nunca a da
    descoberta, para o bloco em vars.h/flags.h nao virar diff a cada rodada.
    """
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

    # Flag de esconder da FONTE -> objetos que ela esconde, em TODOS os mapas.
    # O escopo e global de proposito: 21 das 49 linhas medidas mexem na flag de
    # um objeto de OUTRO mapa, que e como a fonte faz o NPC sumir do lugar de
    # onde ele saiu.
    esconde_glob = collections.defaultdict(list)
    for o in gente:
        if (o["tipo"] == "objeto" and o.get("flag_fonte")
                and o["motivo"].startswith("entrou")):
            esconde_glob[o["flag_fonte"]].append((o["mapa"], o["i"] + 1))

    docs, cobrar = {}, []
    recusa = collections.Counter()
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
        dp = de_para.get(l["mapa_fonte"])
        if dp is None:
            recusa["mapa da fonte fora do de-para do G3"] += 1
            continue
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, dp["nome"])
        if not os.path.exists(caminho):
            recusa["map.json do mapa nao existe"] += 1
            continue
        docs.setdefault(caminho, json.load(open(caminho)))
        cobrar.append((l, dp, caminho))

    # Var de estado que cada mapa usa, e QUAL delas ganha a casa: a mais citada
    # nas cenas daquele mapa (empate pelo endereco menor). E o preco declarado
    # do desenho "uma var por MAPA", o mesmo do c3.
    quantas = collections.defaultdict(collections.Counter)
    for l, _dp, _c in cobrar:
        ins, falha = C3.blocos(rom, tab, int(l["ponteiro_fonte"], 16))
        if falha:
            continue
        for b in ins:
            for nome, args in b.ins:
                if (nome in ("setvar", "addvar", "subvar", "compare_var_to_value")
                        and args and 0x4010 <= args[0] < 0x4200):
                    quantas[l["mapa_fonte"]][args[0]] += 1
    var_escolhida = {c: max(v, key=lambda a: (v[a], -a))
                     for c, v in quantas.items()}

    def traduz(nome_flag_de, nome_var_de):
        fora, motivos = [], collections.Counter()
        usou_flag, usou_var = set(), set()
        for l, dp, caminho in cobrar:
            chave = l["mapa_fonte"]
            esconde = {f: ids for f, ids in
                       ((f, [i for m, i in v if m == chave])
                        for f, v in esconde_glob.items()) if ids}
            nomes_flag = {f: nome_flag_de(f) for f in esconde_glob}
            var = var_escolhida.get(chave)
            nomes_var = {var: nome_var_de(chave)} if var else {}
            t = TradutorObjeto(
                rom, tab, cmap,
                C3.de_para_de_objetos(chave, docs[caminho], por_mapa),
                esconde, nomes_var, nomes_flag, musica, rev_mapa=rev)
            t.de_para_mapa = de_para
            base = rotulo(chave, l)
            try:
                corpo, usadas = t.cena(int(l["ponteiro_fonte"], 16), base)
            except C3.Recusa as e:
                motivos[str(e)] += 1
                continue
            citadas = {f for f in esconde_glob
                       if nomes_flag[f] and nomes_flag[f] in "\n".join(corpo)}
            usou_flag |= citadas
            if var and nomes_var[var] and nomes_var[var] in "\n".join(corpo):
                usou_var.add(chave)
            fora.append(dict(chave=chave, nome=dp["nome"], caminho=caminho,
                             tipo=l["tipo"], x=l["x"], y=l["y"], base=base,
                             linhas=corpo, usadas=usadas, flags=citadas,
                             ordem=ordem_da_rota(dp["nome"])))
        return fora, motivos, usou_flag, usou_var

    _e, _m, quer_flag, quer_var = traduz(lambda f: "FLAG_GALAR_ENSAIO_%03X" % f,
                                         lambda c: "VAR_GALAR_ENSAIO")

    pool_f = [f for f in range(PRIMEIRA_FLAG_ESCONDE, ULTIMA_FLAG_ESCONDE + 1)
              if "FLAG_UNUSED_0x%04X" % f in open(FLAGS_H).read()]
    if len(quer_flag) > len(pool_f):
        raise SystemExit("PARE: %d flags de esconder pedidas e %d livres na "
                         "faixa de Galar" % (len(quer_flag), len(pool_f)))
    flags = {f: ("FLAG_GALAR_ESCONDE_%03X" % f, pool_f[i])
             for i, f in enumerate(sorted(quer_flag))}

    # Var: se o c3 ja deu casa para a MESMA var da fonte naquele mapa, reusa o
    # nome dele em vez de queimar um endereco novo para o mesmo estado.
    do_c3 = vars_do_c3()
    livres = [v for v in C3.vars_livres() if v not in do_c3.values()]
    novas = [c for c in sorted(quer_var) if c not in do_c3]
    if len(novas) > len(livres):
        raise SystemExit("PARE: %d vars de etapa pedidas e %d livres"
                         % (len(novas), len(livres)))
    variaveis = {c: ("VAR_GALAR_%s_OBJ" % c.upper(), livres[i])
                 for i, c in enumerate(novas)}

    def nome_var(chave):
        if chave in do_c3:
            return "VAR_GALAR_%s_CENA" % chave.upper()
        return variaveis[chave][0] if chave in variaveis else None

    aceitas, motivos, _f, _v = traduz(
        lambda f: flags[f][0] if f in flags else None, nome_var)
    recusa.update(motivos)
    return aceitas, recusa, docs, flags, variaveis, esconde_glob


def vars_do_c3():
    """{chave da fonte: endereco} que `cenas_galar.py` ja declarou em vars.h."""
    texto = open(VARS_H).read()
    fora = {}
    for nome, end in re.findall(
            r"#define\s+VAR_GALAR_(G\d+M\d+)_CENA\s+VAR_UNUSED_0x([0-9A-Fa-f]{4})",
            texto):
        fora[nome.lower()] = int(end, 16)
    return fora


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


def aplica(aceitas, docs, gravar, flags=None, variaveis=None,
           esconde_glob=None):
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

    # c4b: o objeto que a FONTE esconde por flag passa a carregar essa flag no
    # campo `flag` do map.json. Sem isso o `setflag` da cena acende um endereco
    # que ninguem le, e o NPC continua de pe: a flag so esconde quando o motor
    # sabe de qual objeto ela e (`GetObjectEventFlagIdByObjectEventId`).
    de_para_nome = {}
    if flags and esconde_glob:
        mundo = json.load(open(f"{RAIZ}/dev_scripts/galar_mundo.json"))
        gente = json.load(open(FALA.CENSO_GENTE))["linhas"]
        por_mapa = collections.defaultdict(list)
        for o in gente:
            por_mapa[o["mapa"]].append(o)
        for f, (nome_flag, _end) in sorted(flags.items()):
            for chave, i_fonte in esconde_glob[f]:
                dp = mundo["de_para"].get(chave)
                if dp is None:
                    continue
                caminho = "%s/data/maps/%s/map.json" % (RAIZ, dp["nome"])
                if caminho not in docs:
                    continue
                nosso = C3.de_para_de_objetos(chave, docs[caminho],
                                              por_mapa).get(i_fonte)
                if nosso is None:
                    continue
                o = docs[caminho]["object_events"][nosso - 1]
                if str(o.get("flag", "0")) != nome_flag:
                    o["flag"] = nome_flag
                    mudou["flag_de_objeto"] += 1
                de_para_nome[nome_flag] = True

    for arq, mi, mf, bloco in (
            (FLAGS_H, MARCA_FLAG_INI, MARCA_FLAG_FIM, bloco_flags(flags or {})),
            (VARS_H, MARCA_VAR_INI, MARCA_VAR_FIM, bloco_vars(variaveis or {}))):
        atual = open(arq).read()
        novo_txt = C3.poe_bloco(atual, mi, mf, bloco)
        if novo_txt != atual:
            mudou[os.path.basename(arq)] += 1
            if gravar:
                open(arq, "w").write(novo_txt)

    for c, d in docs.items():
        if json.dumps(d, sort_keys=True) != antes[c]:
            mudou["mapa"] += 1
            if gravar:
                with open(c, "w") as f:
                    json.dump(d, f, indent=2, ensure_ascii=False)
                    f.write("\n")
    return mudou, recusa, corpo


def proxima_flag_livre(flags):
    """Vaga da faixa de Galar que este bloco AINDA nao usou (para o plante)."""
    usadas = {e for _n, e in flags.values()}
    texto = open(FLAGS_H).read()
    for f in range(PRIMEIRA_FLAG_ESCONDE, ULTIMA_FLAG_ESCONDE + 1):
        if f not in usadas and "FLAG_UNUSED_0x%04X" % f in texto:
            return f
    raise SystemExit("faixa de flags de Galar esgotada")


def proxima_var_livre(variaveis):
    # `C3.vars_livres()` tira os blocos de Galar do header antes de medir, entao
    # ele devolve como LIVRE tambem o que o c3 e o c4d ja apelidaram. Para o
    # plante da mutacao a vaga tem que ser uma que NINGUEM usa, senao o grupo
    # acusado vem com tres nomes e o caso reprova por si mesmo.
    usadas = {e for _n, e in variaveis.values()} | set(vars_do_c3().values())
    for v in C3.vars_livres():
        if v not in usadas:
            return v
    raise SystemExit("faixa de vars esgotada")


def bloco_flags(flags):
    if not flags:
        return ""
    out = [MARCA_FLAG_INI,
           "// Uma flag por FLAG DE ESCONDER da fonte, bloco c4b. A fonte ja",
           "// pendura essa flag no proprio object event; aqui ela ganha nome e",
           "// o campo `flag` do map.json passa a cita-la, para o motor saber",
           "// de qual objeto ela e.",
           "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/objetos_galar.py; nao editar a mao."]
    larg = max(len(n) for n, _e in flags.values()) + 2
    for f in sorted(flags):
        nome, end = flags[f]
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // flag 0x%03X da fonte"
                   % (larg, nome, end, f))
    out.append(MARCA_FLAG_FIM)
    return "\n".join(out) + "\n"


def bloco_vars(variaveis):
    if not variaveis:
        return ""
    out = [MARCA_VAR_INI,
           "// Uma var por MAPA para a etapa que a cena de OBJETO guarda",
           "// (bloco c4d). Mapa que o c3 ja atendeu com VAR_GALAR_*_CENA reusa",
           "// aquela var e nao aparece aqui: mesmo estado, mesma casa.",
           "// Apelidar VAR_UNUSED nao mexe em VARS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/objetos_galar.py; nao editar a mao."]
    larg = max(len(n) for n, _e in variaveis.values()) + 2
    for c in sorted(variaveis):
        nome, end = variaveis[c]
        out.append("#define %-*s VAR_UNUSED_0x%04X  // mapa %s da fonte"
                   % (larg, nome, end, c))
    out.append(MARCA_VAR_FIM)
    return "\n".join(out) + "\n"


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
    aceitas, recusa, docs, flags, variaveis, esconde = plano()

    # 1. PRECEDENCIA: nenhum objeto pode ficar com os dois scripts, e o rotulo
    #    daqui tem que ser o que sobrou no map.json.
    if any(not a["base"].startswith("GalarObj_") for a in aceitas):
        falhas.append("rotulo do c4a fora do prefixo GalarObj_")
    _mudou, rec, corpo1 = aplica(aceitas, docs, False, flags, variaveis,
                                 esconde)
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
        aceitas2, _r2, docs2, f2, v2, e2 = plano()
        mudou2, _rec2, _c2 = aplica(aceitas2, docs2, False, f2, v2, e2)
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

    # 6. MUTACAO PLANTADA: DUAS flags de esconder de Galar na MESMA vaga tem
    #    que REPROVAR no portao, e o mesmo para DUAS vars de mapa. E o defeito
    #    que este bloco poderia introduzir, ja que ele aloca nos dois headers.
    #    A arvore de mentira e a mesma receita do `--demo` do c3: headers
    #    copiados, resto do repo por link, lista autorizada de VERDADE.
    import shutil, tempfile
    for perfil, header, rotulo_pool, vaga in (
            ("flags", "include/constants/flags.h", "FLAG_UNUSED_0x%04X",
             proxima_flag_livre(flags)),
            ("vars", "include/constants/vars.h", "VAR_UNUSED_0x%04X",
             proxima_var_livre(variaveis))):
        GUARDA.usa(perfil)
        P = GUARDA.PREFIXO
        with tempfile.TemporaryDirectory() as tmp:
            for h in list(GUARDA.HEADERS) + [os.path.join("include", x)
                                             for x in GUARDA.PONTA]:
                destino = os.path.join(tmp, h)
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                if not os.path.exists(destino):
                    shutil.copy(os.path.join(RAIZ, h), destino)
            for r in ("data", "src", "test"):
                os.symlink(os.path.join(RAIZ, r), os.path.join(tmp, r))
            os.makedirs(os.path.join(tmp, "plante"))
            alvo = os.path.join(tmp, header)
            texto = open(alvo).read()
            corte = texto.rindex("#endif")
            open(alvo, "w").write(
                texto[:corte]
                + "#define %s_GALAR_PLANTADA_A %s\n" % (P, rotulo_pool % vaga)
                + "#define %s_GALAR_PLANTADA_B %s\n" % (P, rotulo_pool % vaga)
                + texto[corte:])
            open(os.path.join(tmp, "plante", "usa.inc"), "w").write(
                "%s_GALAR_PLANTADA_A %s_GALAR_PLANTADA_B\n" % (P, P))
            raizes = ["data", "src", "include", "test", "plante"]
            novas = GUARDA.portao(base=tmp, raizes=raizes,
                                  caminho_autorizadas=GUARDA.AUTORIZADAS,
                                  verboso=False)
            if not (len(novas) == 1 and int(novas[0]["endereco"], 16) == vaga
                    and set(novas[0]["nomes"]) == {"%s_GALAR_PLANTADA_A" % P,
                                                   "%s_GALAR_PLANTADA_B" % P}):
                falhas.append("duas %s de Galar na mesma vaga NAO reprovaram: %r"
                              % (perfil, novas))
            open(os.path.join(tmp, "plante", "usa.inc"), "w").write(
                "%s_GALAR_PLANTADA_A\n" % P)
            if GUARDA.portao(base=tmp, raizes=raizes,
                             caminho_autorizadas=GUARDA.AUTORIZADAS,
                             verboso=False):
                falhas.append("alocacao sozinha de %s reprovou: viraria ruido"
                              % perfil)
    GUARDA.usa("vars")
    if GUARDA.portao(verboso=False) or GUARDA.stubs(verboso=False):
        falhas.append("o portao de vars esta vermelho na arvore")
    GUARDA.usa("flags")
    if GUARDA.portao(verboso=False) or GUARDA.stubs(verboso=False):
        falhas.append("o portao de flags esta vermelho na arvore")
    GUARDA.usa("vars")

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
    aceitas, recusa, docs, flags, variaveis, esconde = plano()
    mudou, rec, _c = aplica(aceitas, docs, a.aplicar, flags, variaveis,
                            esconde)
    relatorio(aceitas, recusa)
    print("flags de esconder: %d | vars de etapa novas: %d"
          % (len(flags), len(variaveis)))
    print("\n%s: %r" % ("gravado" if a.aplicar else "mudaria", dict(mudou)))
    for base, motivo in rec[:10]:
        print("  nao aplicado: %s %s" % (base, motivo))


if __name__ == "__main__":
    main()
