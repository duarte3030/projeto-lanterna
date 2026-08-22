#!/usr/bin/env python3
"""FASE DE CONTEUDO DE GALAR, bloco c5: os ENCONTROS ESTATICOS da fonte.

    python3 dev_scripts/estaticos_galar.py                 # so mede e relata
    python3 dev_scripts/estaticos_galar.py --dry-run MAPA  # o que entraria num mapa
    python3 dev_scripts/estaticos_galar.py --aplicar       # escreve .inc, map.json, flags.h
    python3 dev_scripts/estaticos_galar.py --demo          # autoteste com mutacao plantada

## O que este bloco e, e por que ele nao e o c4

O demake de Galar poe o Pokemon SELVAGEM no overworld, como em Sword/Shield: um
objeto com grafico de Pokemon parado no mapa, e o script dele e
`setwildbattle` + `dowildbattle`. O G4 barrou esses objetos em 18/08/2026 com a
regra certa para a epoca ("grafico de Pokemon mentiria a especie", 1.549 linhas
de censo), porque naquele dia o unico destino possivel era um sprite generico de
NPC. Hoje nao e mais: `OBJ_EVENT_GFX_SPECIES(X)` existe nesta build e o
`distribui_dex.py` ja pos 106 estaticos com ela. A especie deixou de ser chute e
virou dado lido, entao o barramento caiu.

DECISAO DO GUI, 22/08/2026: o teto de seis regioes fica, Galar fica, e o
conteudo proprio de Galar entra. Este arquivo e a primeira leva dele.

## De onde sai a ESPECIE, e por que o id NAO serve

O `setwildbattle` da fonte carrega um id de especie do DEMAKE, e o demake tem
tabela expandida: os ids passam de 1.200 e nao sao nem os do FireRed nem os da
dex nacional (id 331 la e `Sharpedo`, nao Cacnea). Traduzir por VALOR poria
outro bicho no mapa, calado.

Entao a traducao e por NOME, lida da propria ROM da fonte: `gSpeciesNames` do
demake, 11 bytes por entrada, ACHADA POR ANCORA (o offset nao e digitado: a
funcao procura a cadeia "Bulbasaur" e so aceita a base em que o indice 10 e
"Caterpie", o 25 e "Pikachu", o 151 e "Mew" e o 1102 e "Grookey"; a ROM tem DUAS
tabelas de nome, a vanilla curta e a expandida, e so a expandida passa nas
quatro). O nome vira `SPECIES_<NOME>` e so entra se a constante existir AQUI.

### As formas, que sao o unico lugar onde o nome sozinho mente

Na tabela do demake, `Meowth` aparece tres vezes (o de Kanto, o de Galar e o
Gigantamax) com o MESMO nome. Nome repetido e ambiguidade, e ambiguidade nao
vira palpite: id repetido so entra se estiver em `AJUSTE` abaixo, com a decisao
escrita uma a uma; qualquer outro id de nome repetido e RECUSADO com motivo. As
14 entradas Gigantamax (1234 a 1247, exatamente a lista Venusaur..Melmetal) sao
recusadas de proposito: forma Gigantamax nao e encontro selvagem comum.

## COMUM contra UNICO, medido e nao arbitrado

    UNICO   o script da fonte acende a PROPRIA flag de esconder do objeto, ou
            seja o encontro se apaga para sempre quando resolvido. Sao 7 em
            toda a Galar (Zacian, Calyrex, Nihilego, Meltan e tres Slowpoke de
            Galar). Cada um gasta UMA flag do pool de Galar e ganha script
            proprio, com a flag acesa so em VITORIA ou CAPTURA (o mesmo idioma
            do `distribui_dex.py`, que o T123 ja prova).
    COMUM   todo o resto. Nao gasta flag NENHUMA. O script e
            `setwildbattle` + `dowildbattle` + `Common_EventScript_RemoveStaticPokemon`,
            e esse `removeobject VAR_LAST_TALKED` NAO e persistente: o motor
            tira o objeto da lista viva, e `TrySpawnObjectEvents` o recria a
            partir do template quando o mapa recarrega, porque o campo `flag`
            dele e 0. Ou seja o Pokemon some ao ser enfrentado e volta quando o
            jogador sai e reentra, que e exatamente o que a fonte faz (os 826
            scripts dela terminam em `removeobject` sem `setflag`).

`Common_EventScript_RemoveStaticPokemon` ja existe em `data/event_scripts.s` e
faz o fade + `removeobject VAR_LAST_TALKED` + `release` + `end`. Nao se escreve
de novo o que o motor ja tem.

## Uma cena por (especie, nivel, item), e nao uma por objeto

`removeobject` resolve o argumento por `VarGet`, entao `VAR_LAST_TALKED` (0x800F)
aponta em tempo de execucao para o objeto com que o jogador falou
(`src/field_control_avatar.c:366`). Por isso os 24 Rolycoly de nivel 20 dividem
UM script. Sem isso seriam centenas de copias do mesmo bytecode na ROM.

## NIVEL: o da fonte, e so o da fonte

A curva de Galar e decisao pendente do Gui (a fonte e de pos-jogo, mediana 50 e
picos de 80). Aqui nao se rebaixa nem se sobe nada: o nivel e o do PRIMEIRO
`setwildbattle` do script. Script que sorteia ESPECIE (mesa de raide, ate 59
especies num `random`) e recusado inteiro: escolher uma das 59 seria inventar
qual, e replicar o sorteio custaria ROM que esta rodada nao tem.

## Os portoes de geometria, e o que cada um custa

Tile do objeto e o da FONTE, 1:1, e ele tem de: estar dentro do mapa, ser
ANDAVEL no nosso `map.bin`, nao ser tile de warp (trancaria a porta), nao ter
objeto nosso em cima, e estar ALCANCAVEL. A alcancabilidade e a BFS de colisao e
elevacao do `lendarios_sinnoh.py`, com uma semente a mais que aquele arquivo nao
precisava: as CONEXOES de mapa. Metade dos mapas da Wild Area nao tem warp
nenhum e so se entra neles por conexao; sem essa semente a BFS devolvia o mapa
inteiro como inalcancavel (medido: 398 linhas perdidas por isso, viraram 140).

Depois vem os dois tetos de objeto, os mesmos do `distribui_dex.py`:
`OBJECT_EVENT_TEMPLATES_COUNT` = 64 por mapa, e a JANELA DE SPRITE de 20 por 17
tiles com 15 slots (do 16o template dentro da janela o motor desiste calado).
Quem nao cabe fica na fila com motivo, na ordem da chave da fonte, que e estavel.

## ORDEM DA CORRENTE (lei LEVA_DONA), com este arquivo dentro

    python3 dev_scripts/gente_galar.py      --gravar
    python3 dev_scripts/mundo_galar.py      --gravar
    python3 dev_scripts/fala_galar.py       --aplicar
    python3 dev_scripts/objetos_galar.py    --aplicar
    python3 dev_scripts/estaticos_galar.py  --aplicar   # ESTE, depois dos objetos
    python3 dev_scripts/fila_galar.py       --gravar

Este arquivo so ACRESCENTA object events, sempre no FIM da lista, e marca cada
um com `origem` e `origem_chave`. Acrescentar no fim e obrigatorio: o `c3` e o
`c4` casam objeto por INDICE (`local_id` = posicao + 1), entao inserir no meio
trocaria o dono de uma cena calado. A limpeza da rodada apaga TODO objeto com a
nossa marca antes de escrever, em todos os mapas de Galar, senao o gerador que
so escreve mente na segunda rodada.
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
import lendarios_sinnoh as LS                  # noqa: E402
import guarda_colisao_vars as GUARDA           # noqa: E402

INC = f"{RAIZ}/data/scripts/galar_estaticos.inc"
CENSO = f"{RAIZ}/dev_scripts/galar_estaticos.json"
EVENT_S = f"{RAIZ}/data/event_scripts.s"
FLAGS_H = f"{RAIZ}/include/constants/flags.h"
MUNDO = f"{RAIZ}/dev_scripts/galar_mundo.json"
MARCA = "estaticos_galar"

MARCA_FLAG_INI = ("// >>> Fase de conteudo de Galar, bloco c5: encontros estaticos "
                  "(dev_scripts/estaticos_galar.py) >>>")
MARCA_FLAG_FIM = "// <<< Fase de conteudo de Galar, bloco c5 <<<"

# Faixa propria, longe da do c4b (0x1C80-0x1CFE) para uma leva nova de la nao
# encostar aqui. 0x1D0A-0x2025 e a segunda maior faixa contigua livre medida por
# `flags_livres.py` em 22/08/2026 (796 flags).
PRIMEIRA_FLAG = 0x1D0A
ULTIMA_FLAG = 0x1D49

TETO_OBJETOS = 64          # OBJECT_EVENT_TEMPLATES_COUNT
JANELA_SPRITE = (20, 17)   # TrySpawnObjectEvents, com MAP_OFFSET 7
TETO_SPRITE = 15           # OBJECT_EVENTS_COUNT - 1 (o jogador)

# Nome que o demake escreve diferente do nosso. Sao ERROS DE DIGITACAO DA FONTE
# (as duas primeiras) e um acento que o charmap resolve para outra letra, e cada
# um foi conferido contra include/constants/species.h desta arvore.
GRAFIA = {
    "Corvknight": "SPECIES_CORVIKNIGHT",   # a fonte come o `i`
    "Blacphalon": "SPECIES_BLACEPHALON",   # a fonte come o `e`
    "Flabébé": "SPECIES_FLABEBE",
    "Farfetch’d": "SPECIES_FARFETCHD",     # apostrofo tipografico
    "Sirfetch’d": "SPECIES_SIRFETCHD",
}

# NOME REPETIDO NA TABELA DA FONTE: decisao uma a uma, e id que nao esta aqui e
# recusado. Medido em 22/08/2026 lendo a propria tabela do demake: o bloco 1102+
# e a dex de Galar, e dentro dele 1212 a 1233 sao as formas regionais e 1234 a
# 1247 sao os catorze Gigantamax (Venusaur..Melmetal, na ordem exata da lista).
AJUSTE = {
    1212: "SPECIES_MEOWTH_GALAR",
    1215: "SPECIES_SLOWPOKE_GALAR",
    1216: "SPECIES_SLOWBRO_GALAR",
    1217: "SPECIES_FARFETCHD_GALAR",
    1221: "SPECIES_ARTICUNO_GALAR",
    1222: "SPECIES_ZAPDOS_GALAR",
    1223: "SPECIES_MOLTRES_GALAR",
    1224: "SPECIES_SLOWKING_GALAR",
    1226: "SPECIES_ZIGZAGOON_GALAR",
    1227: "SPECIES_LINOONE_GALAR",
    1229: "SPECIES_DARUMAKA_GALAR",
    1230: "SPECIES_DARMANITAN_GALAR",
    1231: None,   # Darmanitan de Galar em modo Zen: forma de batalha, nao de mapa
    1232: "SPECIES_YAMASK_GALAR",
    1233: "SPECIES_STUNFISK_GALAR",
}
GMAX_RECUSA = "forma Gigantamax: nao e encontro selvagem comum"
REPETIDO_RECUSA = ("id de forma na tabela da fonte sem decisao medida "
                   "(nome repetido)")


# --------------------------------------------------------- nomes da fonte ---
def _inverso_do_charmap():
    cm = FALA.charmap()
    inv = {}
    for b in sorted(cm):
        inv.setdefault(cm[b], b)
    return cm, inv


def nomes_da_fonte(rom=None):
    """{id do demake: nome do Pokemon}, da tabela de nomes da PROPRIA ROM.

    ANCORA, nunca offset digitado. A ROM tem duas tabelas: a vanilla do FireRed
    (para ate ~411) e a expandida do hack. As duas comecam com "Bulbasaur" no
    indice 1, e por isso a ancora exige as QUATRO conferencias abaixo; so a
    expandida responde "Grookey" no 1102.
    """
    rom = rom if rom is not None else open(FALA.ROM_FONTE, "rb").read()
    cm, inv = _inverso_do_charmap()

    def nome(base, i):
        fora = []
        for b in rom[base + i * 11:base + i * 11 + 11]:
            if b == 0xFF:
                break
            fora.append(cm.get(b, "?"))
        return "".join(fora)

    alvo = bytes(inv[c] for c in "Bulbasaur")
    for m in re.finditer(re.escape(alvo), rom):
        base = m.start() - 11
        if (nome(base, 10) == "Caterpie" and nome(base, 25) == "Pikachu"
                and nome(base, 151) == "Mew" and nome(base, 1102) == "Grookey"):
            # A LEITURA NAO PARA NA PRIMEIRA ENTRADA SUJA, e nem numa sequencia
            # delas. Duas coisas medidas na fonte obrigam isso:
            #   - a entrada 19 e o byte 0xAD seguido de "Rattata", ou seja a
            #     propria fonte tem uma entrada torta no meio de dados bons;
            #   - as entradas 252 a 276 sao os "?????" que o Gen 3 deixa vazios,
            #     e parar nelas cortaria a tabela em 251 nomes, com toda a
            #     traducao saindo "id fora da tabela" com cara de ROM errada.
            # Entao a varredura vai ate 1300 (o ultimo nome de verdade e o 1267,
            # `Urshifu`) e guarda so o que decodifica como nome. Id que nao
            # entrou aqui e recusado la na frente, com motivo, nunca adivinhado.
            limpo = re.compile(r"[A-Za-z][A-Za-z0-9 .:’\-éö♂♀]*")
            fora = {}
            for i in range(1, 1300):
                n = nome(base, i)
                if limpo.fullmatch(n or ""):
                    fora[i] = n
            return fora
    raise SystemExit("PARE: a tabela de nomes de especie do demake nao foi "
                     "achada pela ancora. A ROM da fonte mudou?")


def de_para_especie(rom=None):
    """{id do demake: (SPECIES_* nosso, None)} ou {id: (None, motivo)}."""
    nomes = nomes_da_fonte(rom)
    nossos = set(re.findall(r"\bSPECIES_[A-Z0-9_]+\b",
                            open(f"{RAIZ}/include/constants/species.h").read()))
    # PRIMEIRA OCORRENCIA DO NOME = a forma BASE. A tabela do demake e montada
    # em blocos (as especies primeiro, depois megas, Gigantamax e formas
    # regionais), e por isso o menor id de cada nome e sempre o bicho comum:
    # `Sharpedo` aparece em 331 (o normal) e em 899 (o Mega). Ocorrencia
    # POSTERIOR e forma, e forma so entra pela mao, em AJUSTE.
    primeiro = {}
    for i in sorted(nomes):
        primeiro.setdefault(nomes[i], i)
    fora = {}
    for i, n in nomes.items():
        if i in AJUSTE:
            alvo = AJUSTE[i]
            if alvo is None:
                fora[i] = (None, "forma de batalha, nao de mapa")
            elif alvo in nossos:
                fora[i] = (alvo, None)
            else:
                fora[i] = (None, "%s nao existe no nosso species.h" % alvo)
            continue
        alvo = GRAFIA.get(n) or ("SPECIES_"
                                 + re.sub(r"[^A-Z0-9]+", "_", n.upper()).strip("_"))
        if primeiro[n] != i:
            # Ocorrencia repetida = mega, Gigantamax ou forma regional. Sem
            # decisao medida em AJUSTE nao se escolhe qual: o palpite entregaria
            # outro Pokemon com o mesmo nome na tela.
            gmax = alvo + "_GMAX"
            fora[i] = (None, GMAX_RECUSA if gmax in nossos else REPETIDO_RECUSA)
            continue
        fora[i] = (alvo, None) if alvo in nossos else (
            None, "%s nao existe no nosso species.h" % alvo)
    return fora


# ------------------------------------------------------------- geometria ----
def sementes(d, W, H, g):
    """Onde o jogador pode chegar VINDO DE FORA: warps mais bordas de conexao.

    A borda inteira entra como semente porque a conexao entrega o jogador em
    qualquer coluna (ou linha) da borda, e o mapa de destino nao declara onde.
    """
    s = list(LS.sementes_dos_warps(d, W, H, g))
    for c in (d.get("connections") or []):
        dr = c.get("direction")
        if dr == "up":
            s += [(x, 0) for x in range(W)]
        elif dr == "down":
            s += [(x, H - 1) for x in range(W)]
        elif dr == "left":
            s += [(0, y) for y in range(H)]
        elif dr == "right":
            s += [(W - 1, y) for y in range(H)]
    return [(x, y) for x, y in s
            if 0 <= x < W and 0 <= y < H and LS.anda(g[y][x])]


def lotacao(pontos):
    """Quantos templates caem, no PIOR caso, dentro de UMA janela de sprite.

    Copiada em espirito do `distribui_dex.lotacao`: varre a janela ancorada em
    cada objeto, e e pessimista de proposito. Errar para o lado de sobrar custa
    um reposicionamento; errar para o outro custa um Pokemon invisivel que
    nenhuma compilacao acusa.
    """
    if not pontos:
        return 0
    W, H = JANELA_SPRITE
    return max(sum(1 for x, y in pontos if xl <= x < xl + W and yt <= y < yt + H)
               for xl in {p[0] for p in pontos} for yt in {p[1] for p in pontos})


# ---------------------------------------------------------------- leitura ---
def _elevacoes():
    """{(chave da fonte, indice do objeto): elevacao da fonte}."""
    import gente_galar
    por_chave, _ = gente_galar.carrega()
    fora = {}
    for chave, d in por_chave.items():
        for j, o in d["objetos"]:
            fora[(chave, j)] = o.get("elevacao", 0)
    return fora


def _encontros(rom, tab, linhas):
    """[(linha, especie_id, nivel, item_id)] das linhas com `setwildbattle`.

    Recusa por dentro fica em `motivos`, e nao vira silencio.
    """
    fora, motivos = [], collections.Counter()
    for l in linhas:
        if l["tipo"] != "script_objeto" or not l.get("ponteiro_fonte"):
            continue
        if l["no_mapa"]:
            # Objeto que o G4 JA pos no mapa como NPC: a cena dele e do c4,
            # nao daqui, e sobrescrever seria roubar o dono da linha.
            continue
        ins, _falha = C3.blocos(rom, tab, int(l["ponteiro_fonte"], 16))
        swb = [args for b in ins for n, args in b.ins
               if n == "setwildbattle" and len(args) >= 3]
        if not swb:
            continue
        if len({a[0] for a in swb}) != 1:
            motivos["sorteio de %d especies no script (mesa de raide)"
                    % len({a[0] for a in swb})] += 1
            continue
        fora.append((l, swb[0][0], swb[0][1], swb[0][2]))
    return fora, motivos


def _unicos(rom, tab, linhas, flag_do_objeto):
    """Chaves cujo script acende a PROPRIA flag de esconder do objeto."""
    fora = set()
    for l in linhas:
        i = int(l["chave"].rsplit("/", 1)[1])
        f = flag_do_objeto.get((l["mapa_fonte"], i), 0)
        if not f:
            continue
        ins, _ = C3.blocos(rom, tab, int(l["ponteiro_fonte"], 16))
        if any(n == "setflag" and args and args[0] == f
               for b in ins for n, args in b.ins):
            fora.add(l["chave"])
    return fora


def plano():
    """(aceitas, recusa, flags). `aceitas` ja vem na ordem de gravacao."""
    rom = open(FALA.ROM_FONTE, "rb").read()
    tab = FALA.tabela_de_opcodes()
    linhas = json.load(open(FALA.ROTEIROS))["linhas"]
    gente = json.load(open(FALA.CENSO_GENTE))["linhas"]
    flag_do_objeto = {(o["mapa"], o["i"]): o.get("flag_fonte", 0)
                      for o in gente if o["tipo"] == "objeto"}
    de_para_mapa = json.load(open(MUNDO))["de_para"]
    especies = de_para_especie(rom)
    elev = _elevacoes()
    itens_fonte = FALA._gente().itens_da_fonte()
    itens_nossos = FALA._gente().nossos_itens()

    brutos, recusa = _encontros(rom, tab, linhas)
    unicos = _unicos(rom, tab, [l for l, *_ in brutos], flag_do_objeto)

    # Primeira peneira: especie e mapa. Depois vem a geometria, mapa a mapa.
    por_mapa = collections.defaultdict(list)
    for l, sp, lv, it in sorted(brutos, key=lambda z: z[0]["chave"]):
        alvo, motivo = especies.get(sp, (None, "id %d fora da tabela de nomes "
                                               "da fonte" % sp))
        if alvo is None:
            recusa[motivo] += 1
            continue
        dp = de_para_mapa.get(l["mapa_fonte"])
        if dp is None:
            recusa["mapa da fonte fora do de-para do G3"] += 1
            continue
        if not os.path.exists(f"{RAIZ}/data/maps/{dp['nome']}/map.json"):
            recusa["map.json do mapa nao existe"] += 1
            continue
        nome_item = itens_fonte.get(it)
        if it and nome_item not in itens_nossos:
            nome_item = None      # item segurado sem equivalente: cai fora, a
            # especie nao muda por isso e o encontro continua fiel.
        por_mapa[dp["nome"]].append(dict(
            chave=l["chave"], mapa=dp["nome"], especie=alvo, nivel=lv,
            item=nome_item if it else None,
            x=l["x"], y=l["y"],
            elevacao=elev.get((l["mapa_fonte"],
                               int(l["chave"].rsplit("/", 1)[1])), 0),
            unico=l["chave"] in unicos))

    tab_lay = LS.layouts()
    aceitas = []
    for nome in sorted(por_mapa):
        d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))
        W, H, g = LS.grade(d["layout"], tab_lay)
        # Os objetos que JA estao no mapa. A nossa propria marca sai da conta:
        # o gerador nao pode enxergar a rodada anterior como parede, senao a
        # segunda passada devolve outro resultado e ele deixa de ser idempotente.
        fixos = [(o["x"], o["y"]) for o in d.get("object_events", [])
                 if o.get("origem") != MARCA]
        ocupado = set(fixos)
        warps = {(w["x"], w["y"]) for w in d.get("warp_events", [])}
        alc = LS.alcance(W, H, g, sementes(d, W, H, g), bloq=ocupado)
        postos = []
        for c in por_mapa[nome]:
            p = (c["x"], c["y"])
            if not (0 <= p[0] < W and 0 <= p[1] < H):
                recusa["tile fora do mapa"] += 1
            elif not LS.anda(g[p[1]][p[0]]):
                recusa["tile nao andavel no nosso map.bin"] += 1
            elif p in warps:
                recusa["tile de warp: trancaria a porta"] += 1
            elif p in ocupado:
                recusa["tile ja ocupado por objeto nosso"] += 1
            elif p not in alc:
                recusa["tile inalcancavel (BFS de colisao e elevacao)"] += 1
            elif len(fixos) + len(postos) + 1 > TETO_OBJETOS:
                recusa["mapa no teto de %d objetos" % TETO_OBJETOS] += 1
            elif lotacao(fixos + postos + [p]) > TETO_SPRITE:
                recusa["janela de sprite cheia (%d templates em 20x17)"
                       % TETO_SPRITE] += 1
            else:
                postos.append(p)
                ocupado.add(p)
                aceitas.append(c)
                continue
        del postos

    # Flag so para os unicos, e so para os que ENTRARAM, na ordem da chave da
    # fonte: endereco nao se gasta por linha recusada e nao anda de lugar entre
    # rodadas.
    livres = [f for f in range(PRIMEIRA_FLAG, ULTIMA_FLAG + 1)
              if "FLAG_UNUSED_0x%04X" % f in open(FLAGS_H).read()]
    querem = [c for c in sorted(aceitas, key=lambda z: z["chave"]) if c["unico"]]
    if len(querem) > len(livres):
        raise SystemExit("PARE: %d flags de estatico unico pedidas e %d livres "
                         "na faixa 0x%04X-0x%04X"
                         % (len(querem), len(livres), PRIMEIRA_FLAG, ULTIMA_FLAG))
    flags = {}
    for i, c in enumerate(querem):
        c["flag"] = nome_da_flag(c["chave"])
        flags[c["chave"]] = (c["flag"], livres[i])
    return aceitas, recusa, flags


# ----------------------------------------------------------------- nomes ----
def _seco(chave):
    k, _tipo, i = chave.split("/")
    return "%s_O%s" % (k.upper(), i)


def nome_da_flag(chave):
    return "FLAG_GALAR_ESTATICO_" + _seco(chave)


def rotulo(c):
    if c["unico"]:
        return "GalarEstatico_" + _seco(c["chave"])
    return "GalarSelvagem_%s_L%d%s" % (
        c["especie"].replace("SPECIES_", ""), c["nivel"],
        "_" + c["item"].replace("ITEM_", "") if c["item"] else "")


def local_id(c):
    return "LOCALID_GALAR_ESTATICO_" + _seco(c["chave"])


# ------------------------------------------------------------------ .inc ----
def _abre(c):
    """A abertura comum: travar, encarar, gritar. Sem isso o encontro e mudo."""
    return ["\tlock", "\tfaceplayer", "\twaitse",
            "\tplaymoncry %s, CRY_MODE_ENCOUNTER" % c["especie"],
            "\tdelay 40", "\twaitmoncry"]


def _arg_mon(c):
    return "%s, %d%s" % (c["especie"], c["nivel"],
                         ", " + c["item"] if c["item"] else "")


def trecho_comum(c):
    """Um por (especie, nivel, item). Nao gasta flag: o Pokemon RENASCE.

    `removeobject VAR_LAST_TALKED` tira o objeto da lista VIVA e nao da save;
    como o template fica com `flag` 0, `TrySpawnObjectEvents` o recria quando o
    mapa recarrega, e e isso que faz o Pokemon do overworld voltar quando o
    jogador sai e reentra.

    O ID DO OBJETO E GUARDADO EM `VAR_TEMP_1` ANTES DA BATALHA, e isso e
    conserto de defeito MEDIDO em 22/08/2026, nao gosto. `VAR_LAST_TALKED`
    (0x800F) e `gSpecialVar_LastTalked`, e `ProcessPlayerFieldInput`
    (src/field_control_avatar.c:168) o ZERA em todo quadro em que o campo aceita
    comando. Depois da batalha, se um quadro de campo roda antes de o script
    voltar, `removeobject VAR_LAST_TALKED` remove o objeto 0, ou seja nenhum, e o
    Pokemon fica de pe: a MESMA execucao de emulador passou uma vez e reprovou
    quatro, sempre por isso. `VAR_TEMP_1` atravessa a batalha porque
    `ClearTempFieldEventData` so e chamada em warp e carga de mapa
    (src/overworld.c:893 e 958), nunca na volta de uma batalha.

    E O `removeobject` TEM QUE FICAR DEPOIS DO `dowildbattle`. Tirar o objeto
    ANTES tambem conserta a corrida, e foi tentado: o jogador fica CONGELADO no
    lugar para sempre, porque o `lock` prende o objeto selecionado e o `release`
    da volta nao acha mais quem soltar. Medido no emulador em 22/08/2026.

    FLAG_SYS_CTRL_OBJ_DELETE nao entra: medido nesta arvore, NENHUM codigo em
    `src/` le essa flag (so `event_data.c` a apaga), entao ela seria enfeite.
    """
    r = rotulo(c)
    return ["%s::" % r] + _abre(c) + [
        "\tcopyvar VAR_TEMP_1, VAR_LAST_TALKED",
        "\tsetwildbattle %s" % _arg_mon(c),
        "\tdowildbattle",
        "\tfadescreenswapbuffers FADE_TO_BLACK",
        "\tremoveobject VAR_TEMP_1",
        "\tfadescreenswapbuffers FADE_FROM_BLACK",
        "\trelease",
        "\tend", ""]


def trecho_unico(c):
    """Idioma do `distribui_dex._trecho_estatico`: a flag so acende em VITORIA
    ou CAPTURA. Fuga e derrota deixam o encontro de pe, que e o que o jogador
    espera de um lendario."""
    r = rotulo(c)
    return ["%s::" % r] + _abre(c) + [
        "\tseteventmon %s" % _arg_mon(c),
        "\tsetflag FLAG_SYS_CTRL_OBJ_DELETE",
        "\tspecial BattleSetup_StartLegendaryBattle",
        "\tclearflag FLAG_SYS_CTRL_OBJ_DELETE",
        "\tsetvar VAR_LAST_TALKED, %s" % local_id(c),
        "\tspecialvar VAR_RESULT, GetBattleOutcome",
        "\tgoto_if_eq VAR_RESULT, B_OUTCOME_WON, %s_Some" % r,
        "\tgoto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, %s_Some" % r,
        "\trelease", "\tend", "",
        "%s_Some::" % r,
        "\tsetflag %s" % c["flag"],
        "\tgoto Common_EventScript_RemoveStaticPokemon",
        "\tend", ""]


def corpo_inc(aceitas):
    out = ["@ Encontros estaticos de Galar (bloco c5 da fase de conteudo).",
           "@ Gerado por dev_scripts/estaticos_galar.py; NAO editar a mao.",
           "@ COMUM: uma cena por (especie, nivel, item), compartilhada por todos",
           "@ os objetos daquele encontro, porque `removeobject` resolve",
           "@ VAR_LAST_TALKED em tempo de execucao. UNICO: uma cena por objeto,",
           "@ com flag propria acesa so em vitoria ou captura.",
           ""]
    vistos = {}
    for c in sorted(aceitas, key=lambda z: (not z["unico"], rotulo(z), z["chave"])):
        r = rotulo(c)
        if r in vistos:
            continue
        vistos[r] = True
        out += trecho_unico(c) if c["unico"] else trecho_comum(c)
    return "\n".join(out) + "\n"


def bloco_flags(flags):
    if not flags:
        return ""
    out = [MARCA_FLAG_INI,
           "// Uma flag por encontro UNICO (o que a fonte apaga para sempre).",
           "// O encontro COMUM nao aparece aqui de proposito: ele renasce, e",
           "// renascer nao custa endereco nenhum.",
           "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/estaticos_galar.py; nao editar a mao."]
    larg = max(len(n) for n, _e in flags.values()) + 2
    for chave in sorted(flags):
        nome, end = flags[chave]
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // %s"
                   % (larg, nome, end, chave))
    out.append(MARCA_FLAG_FIM)
    return "\n".join(out) + "\n"


# --------------------------------------------------------------- gravacao ---
def objeto_json(c):
    o = {
        "graphics_id": "OBJ_EVENT_GFX_SPECIES(%s)"
                       % c["especie"].replace("SPECIES_", ""),
        "x": c["x"], "y": c["y"], "elevation": c["elevacao"],
        "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
        "movement_range_x": 0, "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0",
        "script": rotulo(c),
        "flag": c.get("flag", "0"),
        "origem": MARCA, "origem_chave": c["chave"],
    }
    if c["unico"]:
        o = {"local_id": local_id(c), **o}
    return o


def escreve_censo(aceitas, recusa):
    """Censo do bloco c5, para a régua não ter de reparsear a ROM da fonte.

    `completude.py` roda em segundos e não pode abrir a ROM do demake; sem este
    arquivo, o único número de estático que ela alcança é o NOSSO (os 795 que
    gravamos), e denominador feito da própria resposta mede 100% para sempre e
    esconde os que ficaram de fora. Aqui fica o número do LADO DA FONTE:
    `da_fonte` = tudo que a fonte oferece como encontro estático, aceito ou
    recusado, que é o que entra no denominador da coluna `objetos`.
    """
    censo = {"da_fonte": len(aceitas) + sum(recusa.values()),
             "aceitos": len(aceitas),
             "recusa": dict(recusa),
             "gerado_por": "dev_scripts/estaticos_galar.py --aplicar"}
    with open(CENSO, "w") as f:
        json.dump(censo, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    return censo


def aplica(aceitas, flags, gravar, recusa=None):
    import glob
    mudou = collections.Counter()
    corpo = corpo_inc(aceitas)
    if gravar:
        if recusa is not None:
            escreve_censo(aceitas, recusa)
        open(INC, "w").write(corpo)
        fonte = open(EVENT_S).read()
        linha = '\t.include "data/scripts/galar_estaticos.inc"'
        if linha not in fonte:
            open(EVENT_S, "w").write(fonte.rstrip("\n") + "\n" + linha + "\n")

    por_mapa = collections.defaultdict(list)
    for c in sorted(aceitas, key=lambda z: z["chave"]):
        por_mapa[c["mapa"]].append(c)
    for caminho in sorted(glob.glob(f"{RAIZ}/data/maps/Galar_*/map.json")):
        nome = os.path.basename(os.path.dirname(caminho))
        d = json.load(open(caminho))
        antes = json.dumps(d, sort_keys=True)
        # LIMPEZA ANTES DE ESCREVER, em TODOS os mapas de Galar: encontro que
        # deixou de passar no filtro tem de sumir do mapa junto com o rotulo,
        # senao o map.json aponta para um simbolo que o .inc nao tem mais e a
        # build so acusa no LINK.
        d["object_events"] = [o for o in d.get("object_events", [])
                              if o.get("origem") != MARCA]
        d["object_events"] += [objeto_json(c) for c in por_mapa.get(nome, [])]
        if json.dumps(d, sort_keys=True) != antes:
            mudou["mapa"] += 1
            mudou["objeto"] += len(por_mapa.get(nome, []))
            if gravar:
                with open(caminho, "w") as f:
                    json.dump(d, f, indent=2, ensure_ascii=False)
                    f.write("\n")

    atual = open(FLAGS_H).read()
    novo = C3.poe_bloco(atual, MARCA_FLAG_INI, MARCA_FLAG_FIM, bloco_flags(flags))
    if novo != atual:
        mudou["flags.h"] += 1
        if gravar:
            open(FLAGS_H, "w").write(novo)
    return mudou, corpo


# ------------------------------------------------------------- relatorio ----
def sonda_janela(aceitas):
    """[(lotacao, objetos, novos, mapa)] dos mapas mais cheios, do pior para o
    menos pior. E a SONDA da janela de sprite: ela nao depende de emulador e
    responde a pergunta que nenhuma compilacao responde, que e quantos templates
    o motor teria de acordar de uma vez no pior canto de cada mapa."""
    por = collections.defaultdict(list)
    for c in aceitas:
        por[c["mapa"]].append((c["x"], c["y"]))
    fora = []
    for nome, meus in por.items():
        d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))
        fixos = [(o["x"], o["y"]) for o in d.get("object_events", [])
                 if o.get("origem") != MARCA]
        fora.append((lotacao(fixos + meus), len(fixos) + len(meus), len(meus),
                     nome))
    fora.sort(reverse=True)
    return fora


def relatorio(aceitas, recusa, flags):
    comuns = [c for c in aceitas if not c["unico"]]
    print("encontros estaticos aplicados: %d em %d mapas (%d comuns, %d unicos)"
          % (len(aceitas), len({c["mapa"] for c in aceitas}), len(comuns),
             len(aceitas) - len(comuns)))
    print("especies distintas: %d | cenas no .inc: %d | flags gastas: %d"
          % (len({c["especie"] for c in aceitas}),
             len({rotulo(c) for c in aceitas}), len(flags)))
    print("de fora: %d linhas" % sum(recusa.values()))
    for m, c in recusa.most_common(20):
        print("  %5d  %s" % (c, m))
    pior = sonda_janela(aceitas)[:5]
    print("\njanela de sprite (teto %d) e teto de objeto (%d), os cinco piores:"
          % (TETO_SPRITE, TETO_OBJETOS))
    for lot, objs, novos, nome in pior:
        print("  janela %2d | objetos %2d | novos %2d | %s"
              % (lot, objs, novos, nome))


def dry_run(aceitas, recusa, mapa):
    meus = [c for c in aceitas if c["mapa"] == mapa]
    print("%s: %d encontros" % (mapa, len(meus)))
    for c in sorted(meus, key=lambda z: (z["y"], z["x"])):
        print("  (%3d,%3d) el%-2d %-28s LV%-3d %-10s %s"
              % (c["x"], c["y"], c["elevacao"], c["especie"], c["nivel"],
                 "unico" if c["unico"] else "comum", rotulo(c)))
    if meus:
        print("  lotacao da janela de sprite (so os nossos): %d de %d"
              % (lotacao([(c["x"], c["y"]) for c in meus]), TETO_SPRITE))
    del recusa


# ------------------------------------------------------------------ demo ----
def demo():
    falhas = []
    aceitas, recusa, flags = plano()

    # 1. A ANCORA da tabela de nomes: ela e a unica coisa aqui que nao vem de um
    #    header, e um deslocamento de 11 bytes trocaria TODO Pokemon pelo
    #    vizinho, calado. Plante: uma base deslocada tem que falhar a ancora.
    rom = open(FALA.ROM_FONTE, "rb").read()
    nomes = nomes_da_fonte(rom)
    for i, esperado in ((1, "Bulbasaur"), (151, "Mew"), (1102, "Grookey"),
                        (1233, "Stunfisk")):
        if nomes.get(i) != esperado:
            falhas.append("tabela de nomes: %d devia ser %s e e %r"
                          % (i, esperado, nomes.get(i)))

    # 2. MUTACAO PLANTADA: traduzir por VALOR em vez de por NOME. O id 331 da
    #    fonte e `Sharpedo`; se alguem trocar a traducao por "o id e o nosso",
    #    331 vira SPECIES_ id 331, que nesta arvore e outro bicho. O caso
    #    reprova se o de-para deixar de citar o nome.
    dp = de_para_especie(rom)
    if dp.get(331, (None, ""))[0] != "SPECIES_SHARPEDO":
        falhas.append("de-para por nome quebrado: 331 devia dar SPECIES_SHARPEDO "
                      "e deu %r" % (dp.get(331),))
    nossos = re.findall(r"^\s*#define\s+(SPECIES_[A-Z0-9_]+)\s",
                        open(f"{RAIZ}/include/constants/species.h").read(), re.M)
    if len(nossos) > 331 and nossos[331] == "SPECIES_SHARPEDO":
        falhas.append("o plante nao seria visto: por valor daria o mesmo bicho")

    # 3. MUTACAO PLANTADA: forma que o nome nao distingue nao pode passar. O
    #    1239 e o Meowth Gigantamax e o 1212 e o de Galar: os dois se chamam
    #    "Meowth", e traduzir pelo nome cru poria o de Kanto nos dois lugares.
    if dp.get(1212, (None, ""))[0] != "SPECIES_MEOWTH_GALAR":
        falhas.append("1212 devia ser o Meowth de Galar e deu %r" % (dp.get(1212),))
    if dp.get(1239, (None, ""))[0] is not None:
        falhas.append("1239 (Meowth Gigantamax) passou como %r" % (dp.get(1239),))
    if dp.get(1234, (None, ""))[0] is not None:
        falhas.append("1234 (Venusaur Gigantamax) passou como %r" % (dp.get(1234),))

    # 4. Nenhum encontro pode nascer em cima de coisa que ja existe, nem fora do
    #    alcance do jogador. Reconferido AQUI contra o map.json de hoje, e nao
    #    contra a memoria do `plano()`, que e quem poderia estar errado.
    tab_lay = LS.layouts()
    por_mapa = collections.defaultdict(list)
    for c in aceitas:
        por_mapa[c["mapa"]].append(c)
    for nome, cs in por_mapa.items():
        d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))
        W, H, g = LS.grade(d["layout"], tab_lay)
        fixos = [(o["x"], o["y"]) for o in d.get("object_events", [])
                 if o.get("origem") != MARCA]
        warps = {(w["x"], w["y"]) for w in d.get("warp_events", [])}
        alc = LS.alcance(W, H, g, sementes(d, W, H, g), bloq=set(fixos))
        meus = [(c["x"], c["y"]) for c in cs]
        if len(set(meus)) != len(meus):
            falhas.append("%s: dois encontros no mesmo tile" % nome)
        for p in meus:
            if p in set(fixos):
                falhas.append("%s: encontro em cima de objeto que ja existia %r"
                              % (nome, p))
            if p in warps:
                falhas.append("%s: encontro em cima de warp %r" % (nome, p))
            if p not in alc:
                falhas.append("%s: encontro inalcancavel %r" % (nome, p))
        if len(fixos) + len(meus) > TETO_OBJETOS:
            falhas.append("%s: %d objetos, acima do teto %d"
                          % (nome, len(fixos) + len(meus), TETO_OBJETOS))
        if lotacao(fixos + meus) > TETO_SPRITE:
            falhas.append("%s: %d templates numa janela de sprite (teto %d)"
                          % (nome, lotacao(fixos + meus), TETO_SPRITE))

    # 5. Rotulo unico por corpo, e corpo unico por rotulo: dois encontros com o
    #    mesmo rotulo e nivel diferente entregariam o nivel de quem chegou
    #    primeiro em todos os mapas.
    corpo = corpo_inc(aceitas)
    rots = re.findall(r"^(\w+)::", corpo, re.M)
    if len(set(rots)) != len(rots):
        falhas.append("rotulo repetido no .inc")
    por_rot = collections.defaultdict(set)
    for c in aceitas:
        por_rot[rotulo(c)].add((c["especie"], c["nivel"], c["item"]))
    for r, v in por_rot.items():
        if len(v) != 1:
            falhas.append("o rotulo %s serve a %d encontros diferentes: %r"
                          % (r, len(v), sorted(v)))

    # 6. Flag: so unico gasta, e cada um gasta a sua.
    if {c["chave"] for c in aceitas if c["unico"]} != set(flags):
        falhas.append("flags alocadas nao batem com os encontros unicos")
    if len({e for _n, e in flags.values()}) != len(flags):
        falhas.append("duas flags de estatico no mesmo endereco")
    for c in aceitas:
        if not c["unico"] and c.get("flag", "0") != "0":
            falhas.append("encontro comum com flag: ele nao renasceria")

    # 7. IDEMPOTENCIA: gerar duas vezes da o mesmo texto, e aplicar em cima do
    #    que ja esta gravado nao mexe em mapa nenhum.
    if corpo != corpo_inc(aceitas):
        falhas.append("o .inc nao e estavel entre duas geracoes")
    if os.path.exists(INC) and open(INC).read() == corpo:
        a2, _r2, f2 = plano()
        mudou2, _c2 = aplica(a2, f2, False)
        if mudou2["mapa"]:
            falhas.append("segunda passada mexeria em %d mapas: nao e idempotente"
                          % mudou2["mapa"])

    # 8. MUTACAO PLANTADA: duas flags de Galar na MESMA vaga tem que REPROVAR no
    #    portao de colisao, e alocacao sozinha nao pode reprovar. Mesma receita
    #    do `--demo` do c4.
    import shutil
    import tempfile
    GUARDA.usa("flags")
    P = GUARDA.PREFIXO
    vaga = proxima_flag_livre(flags)
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
        alvo = os.path.join(tmp, "include/constants/flags.h")
        texto = open(alvo).read()
        corte = texto.rindex("#endif")
        open(alvo, "w").write(
            texto[:corte]
            + "#define %s_GALAR_C5_A FLAG_UNUSED_0x%04X\n" % (P, vaga)
            + "#define %s_GALAR_C5_B FLAG_UNUSED_0x%04X\n" % (P, vaga)
            + texto[corte:])
        raizes = ["data", "src", "include", "test", "plante"]
        open(os.path.join(tmp, "plante", "usa.inc"), "w").write(
            "%s_GALAR_C5_A %s_GALAR_C5_B\n" % (P, P))
        novas = GUARDA.portao(base=tmp, raizes=raizes,
                              caminho_autorizadas=GUARDA.AUTORIZADAS,
                              verboso=False)
        if not (len(novas) == 1 and int(novas[0]["endereco"], 16) == vaga):
            falhas.append("duas flags de estatico na mesma vaga NAO reprovaram: "
                          "%r" % novas)
        open(os.path.join(tmp, "plante", "usa.inc"), "w").write(
            "%s_GALAR_C5_A\n" % P)
        if GUARDA.portao(base=tmp, raizes=raizes,
                         caminho_autorizadas=GUARDA.AUTORIZADAS, verboso=False):
            falhas.append("alocacao sozinha reprovou: viraria ruido")
    if GUARDA.portao(verboso=False) or GUARDA.stubs(verboso=False):
        falhas.append("o portao de flags esta vermelho na arvore")
    GUARDA.usa("vars")

    # 9. O QUE A PENEIRA RECUSOU NAO PODE ESTAR NO MAPA (portao do fechador,
    #    22/08/2026). Os 293 recusados nao tem caso de emulador possivel, e a
    #    razao e a propria recusa: tile nao andavel, tile ja ocupado e tile
    #    inalcancavel sao EXATAMENTE os lugares onde o jogador nao chega, entao
    #    andar por cima nao separa "o objeto nao existe" de "o objeto existe e
    #    eu nao consigo chegar la". Prova de emulador nao alcanca isto, e por
    #    isso a prova e de script, aqui, sobre o `map.json` gravado: a UNIAO das
    #    chaves que a fonte oferece menos as que entraram nao pode aparecer em
    #    mapa nenhum, cada chave aceita aparece UMA vez, e nao existe objeto
    #    nosso com chave que a fonte nao tenha.
    import glob as _glob
    _brutos, _ = _encontros(open(FALA.ROM_FONTE, "rb").read(),
                            FALA.tabela_de_opcodes(),
                            json.load(open(FALA.ROTEIROS))["linhas"])
    candidatas = {l["chave"] for l, *_ in _brutos}
    entraram = {c["chave"] for c in aceitas}
    recusadas = candidatas - entraram
    no_mapa = collections.Counter()
    for caminho in _glob.glob(f"{RAIZ}/data/maps/Galar_*/map.json"):
        for o in json.load(open(caminho)).get("object_events", []):
            if o.get("origem") == MARCA:
                no_mapa[o.get("origem_chave")] += 1
    intrusas = sorted(recusadas & set(no_mapa))
    if intrusas:
        falhas.append("%d chaves RECUSADAS estao no map.json, a primeira e %s"
                      % (len(intrusas), intrusas[0]))
    if set(no_mapa) - candidatas:
        falhas.append("objeto nosso com chave que a fonte nao tem: %r"
                      % sorted(set(no_mapa) - candidatas)[:3])
    if set(no_mapa) != entraram:
        falhas.append("as chaves no map.json nao sao as aceitas (%d contra %d)"
                      % (len(no_mapa), len(entraram)))
    repetidas = [k for k, n in no_mapa.items() if n != 1]
    if repetidas:
        falhas.append("chave aceita gravada mais de uma vez: %r" % repetidas[:3])
    print("recusadas fora do mapa: %d de %d chaves da fonte, e as %d aceitas "
          "estao gravadas uma vez cada" % (len(recusadas), len(candidatas),
                                           len(entraram)))

    print("demo: %s" % ("OK" if not falhas else "REPROVADO"))
    for f in falhas:
        print("  FALHA", f)
    relatorio(aceitas, recusa, flags)
    return 1 if falhas else 0


def proxima_flag_livre(flags):
    usadas = {e for _n, e in flags.values()}
    texto = open(FLAGS_H).read()
    for f in range(PRIMEIRA_FLAG, ULTIMA_FLAG + 1):
        if f not in usadas and "FLAG_UNUSED_0x%04X" % f in texto:
            return f
    raise SystemExit("faixa de flags do c5 esgotada")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--dry-run", metavar="MAPA")
    a = ap.parse_args()
    if a.demo:
        raise SystemExit(demo())
    aceitas, recusa, flags = plano()
    if a.dry_run:
        dry_run(aceitas, recusa, a.dry_run)
        return
    mudou, _c = aplica(aceitas, flags, a.aplicar, recusa)
    relatorio(aceitas, recusa, flags)
    print("\n%s: %r" % ("gravado" if a.aplicar else "mudaria", dict(mudou)))


if __name__ == "__main__":
    main()
