#!/usr/bin/env python3
"""ONDA 2, LOTE F: as PORTAS DE SCRIPT dos órfãos de Galar de origem viva.

    python3 dev_scripts/portas_script_galar.py            # mede e relata
    python3 dev_scripts/portas_script_galar.py --seco     # mede, não grava nada
    python3 dev_scripts/portas_script_galar.py --demo     # autoteste
    python3 dev_scripts/portas_script_galar.py --aplicar  # grava os arquivos

## O que este gerador é, e o que ele NÃO é

`dev_scripts/anda_scripts_galar.py` mediu, andando o bytecode do demake, que
141 órfãos de Galar existem hoje, que 95 deles são alcançados por um `warp`
DENTRO de script, e que **40 são alcançados a partir de mapa VIVO**, somando
**77 portas**. Aquele script mede; este TRANSCREVE, no dialeto do pokeemerald.

Ele não desenha conteúdo. Ele pega o script da fonte que contém o `warp`,
manda o MESMO tradutor que o c3 (`dev_scripts/cenas_galar.py`) e o c4a
(`dev_scripts/objetos_galar.py`) já usam escrever aquele script inteiro, e o
que o tradutor recusar sai daqui com o motivo, nunca pela metade. Cena inteira
ou nada é a regra dos dois blocos anteriores e continua sendo a daqui: meia
porta é pior do que porta nenhuma, porque ela compila.

## Os quatro baldes, e quem é dono de quê

A porta pende de alguma coisa no mapa de ORIGEM. Medindo o objeto da fonte
contra o nosso `map.json` **pela coordenada** (nunca pela ordem: é a lição do
`de_para_de_objetos` do c3), a classificação sai assim, e o `--demo` reprova se
os totais mudarem calados:

  * **A** — o objeto da fonte NÃO está no nosso array (o G4 o recusou, quase
    sempre porque o gráfico dele é um Pokémon e devolver sprite de gente
    mentiria a espécie). A porta precisa de um `object_events` NOVO, que sai
    daqui como PEDIDO em `onda2_lote_f_pedidos_mapjson.json`, porque este lote
    não é dono de `map.json`.
  * **B** — o objeto existe e está MUDO (`script` vale `"0"`). A porta precisa
    só de um pedido de repontar o campo `script` para o rótulo daqui.
  * **C** — o objeto existe e já tem rótulo de OUTRO dono. Medido em
    07/09/2026: são `GalarObj_*` (6 portas) e `GalarTrn_*` (10 portas), e
    **não** `GalarFala_*`/`GalarSelvagem_*`/`GalarEstatico_*` como a abertura
    da onda supôs. Os 6 `GalarObj_*` **já têm o `warp` escrito** (o c4a portou
    a cena inteira, `warp` incluído): não há trabalho, e este gerador os
    registra como já feitos. Os 10 `GalarTrn_*` moram em
    `data/scripts/galar_treinadores.inc`, que é de outro dono e é REGENERADO:
    escrever lá seria perder na próxima geração, e repontar o `map.json` seria
    desfeito calado por `treinadores_galar.py`, que escreve o campo `script`
    sem regra de precedência (linha 1149 de lá). Eles saem como PENDÊNCIA.
  * **D** — a porta é `coord_events` (gatilho de coordenada). Nenhum `map.json`
    de Galar tem `coord_events` hoje (o G4 os deixou vazios de propósito), e o
    gatilho novo sai como pedido, com a coordenada, a var e o valor da fonte.

## POR QUE O NÚMERO DE ÓRFÃOS NÃO CAI SÓ POR ESTE ARQUIVO EXISTIR

Medido em 07/09/2026, lendo `dev_scripts/valida_conectividade.py`: a varredura
de "warp escrito dentro de script" abre **`data/maps/<dir>/scripts.inc`**, e só
ele. Warp que mora em `data/scripts/galar_*.inc` (que é onde TODA a fase de
conteúdo de Galar escreve, este arquivo incluído) é invisível para a régua de
conectividade. Prova: `GalarObj_G03M08_o19` já faz `warp MAP_GALAR_HULBURY_01,
12, 27` desde o c4a, e `MAP_GALAR_HULBURY_01` continua na lista de órfãos.

Ou seja: **enquanto a régua não ler os `.inc` compartilhados, nenhuma porta
transcrita aqui muda a contagem de órfãos**, e isso vale igualmente para as que
já estavam escritas. A conta de "quantos dos 40 deixam de ser órfão" que este
gerador imprime é feita com o grafo da própria régua MAIS as arestas que ele
transcreveu, e está marcada como simulação para não virar segunda verdade.

## Var, flag e texto

Var: uma por MAPA de origem, `VAR_GALAR_PORTA_<CHAVE>`, apelido de
`VAR_UNUSED_*` livre medido pelo mesmo pré-processador do c3
(`cenas_galar.vars_livres`), em bloco delimitado no fim de
`include/constants/vars.h`. Flag: faixa 0x2200-0x227F, exclusiva deste lote, e
gasta SÓ por flag que o próprio script da fonte acende e lê; flag que esconde
objeto importado continua com o nome que o c4b lhe deu
(`FLAG_GALAR_ESCONDE_<hex>`, lido do header), porque duas flags para a mesma
flag da fonte fariam o NPC sumir num script e continuar no outro. Flag que o
script só LÊ, e que quem acende é código C do demake, recusa a cena inteira:
dar flag a ela seria decidir por conta própria qual ramo o jogador vê.

Texto: o demake fala PORTUGUÊS e Galar tem de falar inglês (decisão 32 do Gui).
O `aplica_traducao_galar.py` traduz depois, casando por RÓTULO contra
`traducao_galar.json`, e rótulo novo deste lote não está lá; então a tradução
sai daqui, na hora, pela tabela `TRADUCAO`, com o `GLOSSARIO-GALAR.md` na mão e
a requebra por pixel de `texto_placas_sinnoh.requebra` (208 px). Texto em
português SEM entrada na tabela recusa a cena inteira, e é por isso que o
`--demo` mede idioma e largura no que o gerador emite, antes de o `.inc` sair.

## O QUE ESTE LOTE ENTREGOU, medido em 07/09/2026

7 portas transcritas (balde A, os táxis Corviknight de Isle of Armor, Hammerlocke
e Wild Area, mais o recepcionista de Motostoke no balde B, 8 ao todo), 6 já
estavam escritas pelo c4a, e 63 saíram com motivo. Os motivos que mais pesam,
e nenhum deles é conserto deste lote: 26 portas em `checkflag` de flag de motor
do demake, 10 em var de save fora da faixa do FireRed (0x5467), 7 em
`trainerbattle` (o `blocos()` do c3 não dimensiona a macro), 10 em rótulo de
outro dono, e 5 em gatilho cuja var da fonte lê fora do array.

Na régua: com as arestas deste lote visíveis, Galar cai de **141 para 135**
órfãos e o alcance sobe de 2.052 para 2.058. Os seis que saem são
`ISLE_OF_ARMOR_01`, `STOW_ON_SIDE_01`, `WEDGEHURST_09`, `WILD_AREA_17` e, por
tabela, `WILD_AREA_18` e `WILD_AREA_CAVE_01`.
"""
import argparse
import collections
import glob
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import anda_scripts_galar as AND                # noqa: E402
import fala_galar as FALA                       # noqa: E402
import cenas_galar as C3                        # noqa: E402
import objetos_galar as OBJ                     # noqa: E402
import gente_galar as GENTE                     # noqa: E402
import tabela_gfx_galar as GFX                  # noqa: E402
import estaticos_galar as EST                   # noqa: E402
import texto_placas_sinnoh as REQUEBRA          # noqa: E402
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts/qa"))
import checa_texto as QA_TEXTO                  # noqa: E402

INC = f"{RAIZ}/data/scripts/galar_portas_script.inc"
EVENT_S = f"{RAIZ}/data/event_scripts.s"
LINHA_INCLUDE = '\t.include "data/scripts/galar_portas_script.inc"'
# ONDA 3, LOTE M: os pedidos saem em arquivo NOVO. Os tres arquivos da onda 2
# (`onda2_lote_f_pedidos_mapjson.json`, `..._pendentes_estaticos.txt` e
# `..._tocados.txt`) ficam CONGELADOS no disco como historia daquela onda: este
# gerador nao os reescreve mais, e o que eles diziam passou a caber no proprio
# JSON de pedidos, nas secoes `nao_feitas`, `ja_escritas` e `rotulos_escritos`.
PEDIDOS = f"{RAIZ}/dev_scripts/onda3_lote_m_pedidos_mapjson.json"
FALTA_TRADUZIR = f"{RAIZ}/dev_scripts/onda3_lote_m_falta_traduzir.json"
VARS_H = f"{RAIZ}/include/constants/vars.h"
FLAGS_H = f"{RAIZ}/include/constants/flags.h"
TREINADORES_INC = f"{RAIZ}/data/scripts/galar_treinadores.inc"

MARCA_VAR_INI = ("// >>> Fase de conteudo de Galar, onda 2 lote F: vars de porta "
                 "de script (dev_scripts/portas_script_galar.py) >>>")
MARCA_VAR_FIM = "// <<< Fase de conteudo de Galar, onda 2 lote F <<<"
MARCA_FLAG_INI = ("// >>> Fase de conteudo de Galar, onda 2 lote F: flags de porta "
                  "de script (dev_scripts/portas_script_galar.py) >>>")
MARCA_FLAG_FIM = "// <<< Fase de conteudo de Galar, onda 2 lote F, flags <<<"

# Faixa de flag EXCLUSIVA deste lote, dada pela condutora na abertura da onda 2.
PRIMEIRA_FLAG = 0x2200
ULTIMA_FLAG = 0x227F

# A REPARTICAO DOS BALDES, medida em 08/09/2026 na arvore de HOJE (onda 3,
# lote M). O --demo reprova se mudar sem que alguem venha aqui mudar o numero
# de proposito: total que anda calado e como a onda descobre tarde que a fonte
# ou a arvore mexeu.
#
# Os tres primeiros numeros MUDARAM em relacao a onda 2 (A 22, B 22, C 16), e
# nao por defeito: a obra da onda 2 mexeu no `map.json`, que e exatamente o que
# estes tres medem. O porque de cada um esta ao lado, e cada um foi conferido
# rodando `--seco` nesta arvore:
#
#   * `portas` e `destinos` NAO mudaram (77 e 40): eles saem so da FONTE, e a
#     fonte e a mesma ROM do demake.
#   * A caiu de 22 para 15, -7: sao os 7 `object_events` de taxi Corviknight que
#     o lote F pediu e o fechador da onda 2 colou. Objeto que passa a existir no
#     nosso `map.json` deixa de ser "o G4 nao pos" e vira B ou C.
#   * B caiu de 22 para 2, -20: objeto MUDO e o que tem `script` valendo "0", e
#     os lotes F e I penduraram rotulo em 20 deles. Sobraram os 2 de
#     `Galar_Route0202` e `Galar_Route0901` que caem em UNDERWATER_01.
#   * C subiu de 16 para 43, +27: e o outro lado da mesma moeda (os 20 que
#     sairam de B mais os 7 que sairam de A). A composicao de hoje e
#     `GalarObj_` 6, `GalarFalaI_` 19, `GalarTrn_` 10 e `GalarPorta_` 8, e os 8
#     ultimos sao os DESTE gerador, colados pelo fechador da onda 2.
#   * D continua 17: `coord_events` sai da fonte, e nenhum mapa de Galar tinha
#     ou tem gatilho no `map.json`.
#
# PREVISAO para quem rodar isto DEPOIS de o fechador desta onda colar os
# pedidos, para ninguem cacar defeito onde nao ha: cada `object_events` novo
# tira 1 de A e poe 1 em C, e A + B + C = 60 e invariante. Com os 10 taxis que
# este lote pede, a repartição do dia seguinte e A 5, B 2, C 53, D 17.
#
# CONFERIDO no fechamento de 06/09/2026, e a previsao acima bateu na virgula:
# com os 10 taxis colados, `--demo` mediu A 5 e C 53, e B e D nao se mexeram.
# A recalibracao entra aqui porque a repartição foi PREVISTA antes da obra e a
# conta fecha (A -10, C +10, A + B + C = 60), e nao porque a régua incomodou.
ESPERADO = {"portas": 77, "destinos": 40, "A": 5, "B": 2, "C": 53, "D": 17}

PREFIXO = "GalarPorta_"

# PRECEDENCIA DE `script`, e ela nao e opiniao deste arquivo: `GalarPorta_` esta
# em `objetos_galar.MANDAM_MAIS` (linha 126 de la), que e a LISTA UNICA lida por
# `objetos_galar.manda_mais` (linha 129) e por `fala_galar._manda_mais` (linha
# 745). Quer dizer: os geradores que escrevem `GalarObj_`, `GalarFalaI_` e
# `GalarFala_` ja se recusam a escrever por cima de um rotulo daqui, e por isso
# uma porta PODE tomar o objeto deles sem que a proxima geracao a desfaca.
#
# `GalarTrn_` entrou nesta lista na onda 3, lote M: `treinadores_galar.py`
# passou a chamar o MESMO `manda_mais` antes de escrever o campo `script`
# (linha ~1149 de la), que era o unico dos quatro que escrevia sem perguntar.
#
# `GalarPorta_` esta aqui por um motivo diferente e igualmente importante: e o
# NOSSO prefixo. Sem esta linha, a segunda passada deste gerador ve o rotulo que
# ele mesmo escreveu como "rotulo de outro dono", recusa a porta e APAGA o
# `.inc` inteiro em silencio. E a mesma armadilha que o `--demo-galar` do
# `distribui_dex.py` pagou em 07/09/2026 (ver ESTADO-CARTUCHO-2.md, "Armadilhas
# de gerador que a proxima rodada herda", ultimo item).
#
# `GalarObj_` NAO entra: as 6 portas dele ja tem o `warp` escrito pelo c4a (a
# cena inteira foi portada, `warp` incluido) e sao registradas como ja feitas.
# Tomar objeto de quem ja resolveu a porta seria trocar seis por meia duzia com
# risco de perder o resto da cena.
TOMAVEIS = ("GalarPorta_", "GalarFalaI_", "GalarFala_", "GalarTrn_")

# Dos TOMAVEIS, os que sao FALA pura: para tomar um deles e preciso PROVAR que
# a porta contem a fala, e a prova e o ponteiro da fonte. `fila_galar.json`
# guarda o `ponteiro_fonte` de que cada rotulo de fala nasceu; se ele for o
# mesmo ponto de entrada desta porta, a transcricao daqui e a MESMA cena mais o
# `warp`, e o rotulo antigo vira ROM parada, nunca conteudo perdido. Ponteiro
# diferente recusa a porta: seria calar um NPC para abrir uma porta.
TOMAVEIS_DE_FALA = ("GalarFalaI_", "GalarFala_")

# TRADUCAO do texto que as portas deste lote levam junto. Chave: o corpo EXATO
# da `.string` como a fonte o entrega (com `\\n`, `\\l`, `\\p` e `{PLAYER}` no
# lugar), sem o `$`. Valor: o ingles, pelo GLOSSARIO-GALAR.md, requebrado
# depois contra 208 px pelo `texto_placas_sinnoh.requebra`.
#
# Ela existe aqui, e nao em `dev_scripts/traducao_galar.json`, porque aquele
# arquivo casa por ROTULO e os rotulos deste lote nao existiam quando ele foi
# levantado; poe-los la sem o `.inc` correspondente faria o aplicador de
# traducao listar rotulo que ninguem escreve. Texto novo nasce em ingles.
#
# Regra do glossario aplicada linha a linha: erro de digitacao do demake NAO e
# reproduzido, token de controle sai na mesma ordem e quantidade, e a requebra
# por pixel e quem decide onde `\\n` e `\\l` caem.
TRADUCAO = {
    # Galar_Motostoke06, o recepcionista do hotel que leva o jogador para
    # dormir. "desafiantes de ginasio" -> "Gym Challengers" (glossario, secao 3);
    # "cerimonia de abertura" -> "opening ceremony" (oficial SwSh). O erro de
    # digitacao do demake (falta de acento, virgula, caixa) NAO e reproduzido:
    # o glossario, secao 5, item 1, manda escrever ingles correto.
    r"Vocês são desafiantes de ginasio\ncerto?\ppor hoje podem descansar\n amanha sera a cerimonia de abertura.":
        r"You're Gym Challengers, right?\pYou can rest for today. Tomorrow is the opening ceremony.",
    r"então é isso {PLAYER}\n vamos descansar e amanha\p vai ser o grande dia.":
        r"So that's it, {PLAYER}. Let's rest.\pTomorrow is the big day.",
    r"Este hotel é conhecido \ninternacionalmente!!!":
        r"This hotel is known all over the world!",
}


_RESGATE = {}


def resgate_de_texto():
    """{portugues da fonte: ingles} do lote I da onda 2, se o arquivo existir.

    E o `dev_scripts/resgate_galar_texto.json` que `objetos_galar.py` levantou:
    107 pares ja aprovados, ja escritos em `galar_objetos_i.inc` e ja contados
    pelo `checa_texto`. Lido, nunca escrito por este lote.
    """
    if not _RESGATE:
        caminho = OBJ.TEXTO_I
        if os.path.exists(caminho):
            _RESGATE.update({e["pt"]: e["en"]
                             for e in json.load(open(caminho,
                                                     encoding="utf-8"))["entradas"]})
        _RESGATE.setdefault("", "")
    return _RESGATE


# --------------------------------------------------------------- medicao ----

class AndadorComCoord(AND.Andador):
    """O andador do lote AB, guardando tambem o x/y do `warp`.

    O `anda_scripts_galar.py` so precisava do MAPA de destino, entao ele le
    tres bytes do argumento e segue. Aqui o alvo e escrever o comando, e o
    `warp` do FireRed leva `map` (grupo, num), indice de chegada e x/y (2+2),
    sete bytes ao todo (`asm/macros/map.inc` do pokefirered, e `ScrCmd_warp` em
    `src/scrcmd.c:719`). Sem o x/y nao da para transcrever nada.
    """

    def anda(self, inicio, limite=4000):
        achados, vistos, pilha = [], set(), [inicio]
        passos = 0
        while pilha:
            p = pilha.pop()
            if not self.valido(p) or p in vistos:
                continue
            o = p - AND.ROM_BASE
            while True:
                passos += 1
                if passos > limite:
                    break
                if o + 1 > len(self.rom) or (o + AND.ROM_BASE) in vistos:
                    break
                vistos.add(o + AND.ROM_BASE)
                op = self.rom[o]
                if op == AND.PREENCHIMENTO:
                    break
                if op not in self.tab:
                    break
                nome, tam = self.tab[op]
                if op in AND.WARPS and o + 8 <= len(self.rom):
                    grupo, num = self.rom[o + 1], self.rom[o + 2]
                    if op in AND.SO_MAPA:
                        achados.append((nome, grupo, num, None, None, None))
                    else:
                        achados.append((nome, grupo, num, self.rom[o + 3],
                                        struct.unpack_from("<H", self.rom, o + 4)[0],
                                        struct.unpack_from("<H", self.rom, o + 6)[0]))
                if op == 0x5C:
                    tipo = self.rom[o + 1]
                    if tipo not in AND.TRAINERBATTLE:
                        break
                    n_ptr, cont = AND.TRAINERBATTLE[tipo]
                    tam = AND.TRAINERBATTLE_CAB + 4 * n_ptr
                    if cont is not None:
                        alvo = self.u32(o + AND.TRAINERBATTLE_CAB + 4 * cont)
                        if self.valido(alvo):
                            pilha.append(alvo)
                if tam is None:
                    break
                if op in AND.IR or op in AND.IR_COND:
                    desl = 1 if op in AND.IR else 2
                    alvo = self.u32(o + desl)
                    if not self.valido(alvo):
                        break
                    pilha.append(alvo)
                    if op == 0x05:
                        break
                if op in AND.PARA:
                    break
                o += tam
        return achados


def fonte():
    """(de_para, src, complemento, rom, andador, orfaos) da fonte e da arvore."""
    cen = json.load(open(AND.CENSO, encoding="utf-8"))
    dp = cen["de_para"]
    mapas = json.load(open(os.path.join(AND.EXTRAIDOS, "mapas.json"),
                           encoding="utf-8"))
    comp = json.load(open(os.path.join(AND.EXTRAIDOS, "complemento.json"),
                          encoding="utf-8"))
    src = {}
    for g in mapas:
        for i, m in enumerate(g["mapas"]):
            src["g%02dm%02d" % (g["grupo"], i)] = m
    rom = open(AND.ROM, "rb").read()
    and_ = AndadorComCoord(rom, AND.tabela_de_opcodes())
    return dp, src, comp, rom, and_, set(AND.carrega_orfaos())


def portas():
    """As portas de script de ORIGEM VIVA que caem em orfao. Uma por warp."""
    dp, src, comp, _rom, and_, orfaos = fonte()
    id_de = {k: v["mapa"] for k, v in dp.items()}
    nome_de = {k: v["nome"] for k, v in dp.items()}
    fora = []
    for f in sorted(dp):
        if id_de[f] in orfaos:
            continue           # origem tem que ser mapa VIVO
        for rotulo, p in AND.pontos_de_entrada(and_, comp.get(f), src[f]):
            for nome, grupo, num, warp, x, y in and_.anda(p):
                d = "g%02dm%02d" % (grupo, num)
                if d not in dp or id_de[d] not in orfaos:
                    continue
                fora.append({
                    "fonte": f, "origem": id_de[f], "origem_dir": nome_de[f],
                    "rotulo_fonte": rotulo, "ptr": "0x%X" % p, "comando": nome,
                    "destino_fonte": d, "destino": id_de[d],
                    "destino_dir": nome_de[d],
                    "warp_de_chegada": warp, "wx": x, "wy": y,
                })
    return fora


def classifica(lista):
    """Poe `balde`, o dado da fonte e o dado do nosso mapa em cada porta."""
    dp, src, _comp, _rom, _and, _orf = fonte()
    docs = {}

    def doc(nome):
        c = "%s/data/maps/%s/map.json" % (RAIZ, nome)
        if c not in docs:
            docs[c] = json.load(open(c))
        return c, docs[c]

    for p in lista:
        chave = p["fonte"]
        nome = dp[chave]["nome"]
        caminho, d = doc(nome)
        p["nosso_dir"] = nome
        p["caminho"] = caminho
        por_tile = collections.defaultdict(list)
        for i, o in enumerate(d.get("object_events", [])):
            por_tile[(o["x"], o["y"])].append(i + 1)
        rot = p["rotulo_fonte"]
        if rot.startswith("objeto "):
            lid = int(rot.split()[1])
            alvo = int(p["ptr"], 16)
            # O `local_id` da fonte NAO e unico (medido: g03m05 tem dois
            # objetos com local_id 25), entao o casamento e pelo PONTEIRO de
            # script, que e o que o andador usou como ponto de entrada.
            cands = [(i, o) for i, o in enumerate(src[chave]["objetos"])
                     if o["local_id"] == lid and o.get("script")
                     and int(o["script"], 16) + AND.ROM_BASE == alvo]
            if len(cands) != 1:
                p["balde"] = "?"
                p["motivo"] = "objeto da fonte ambiguo (%d candidatos)" % len(cands)
                continue
            idx, so = cands[0]
            p.update(tipo="objeto", src_i=idx, src_local_id=lid,
                     src_x=so["x"], src_y=so["y"], src_gfx=so["grafico"],
                     src_mov=so["movimento"], src_flag=so["flag"],
                     src_elev=so["elevacao"], src_alcance=so["alcance"],
                     src_trainer=so["trainer_type"])
            cand = por_tile.get((so["x"], so["y"]), [])
            p["nossos_no_tile"] = cand
            if len(cand) == 1:
                oe = d["object_events"][cand[0] - 1]
                p["nosso_local_id"] = cand[0]
                p["nosso_script"] = str(oe.get("script") or "0")
                p["nosso_gfx"] = oe.get("graphics_id")
                p["balde"] = "B" if p["nosso_script"] in ("0", "") else "C"
            else:
                p["nosso_local_id"] = None
                p["nosso_script"] = None
                p["balde"] = "A"
        elif rot.startswith("gatilho"):
            m = re.match(r"gatilho \((\d+),(\d+)\)", rot)
            x, y = int(m.group(1)), int(m.group(2))
            co = [(i, c) for i, c in enumerate(src[chave].get("coords") or [])
                  if c["x"] == x and c["y"] == y
                  and c.get("script")
                  and int(c["script"], 16) + AND.ROM_BASE == int(p["ptr"], 16)]
            if len(co) != 1:
                p["balde"] = "?"
                p["motivo"] = "gatilho da fonte ambiguo (%d)" % len(co)
                continue
            idx, c = co[0]
            p.update(balde="D", tipo="gatilho", src_i=idx, src_x=x, src_y=y,
                     src_var=c["var"], src_valor=c["valor"])
        else:
            p["balde"] = "?"
            p["motivo"] = "porta de cena (map script), fora deste lote"
    return lista, docs


# Gfx da fonte que este lote propoe como Pokemon do overworld, e a EVIDENCIA de
# cada um. Nao e leitura de sprite: e o cruzamento de tres coisas medidas.
# O motor ja sabe desenhar Pokemon no mapa (`OBJ_EVENT_GFX_SPECIES(X)` em
# include/constants/event_objects.h:511, usado por dev_scripts/estaticos_galar.py
# em 73 mapas), entao aqui nao ha impedimento tecnico: o que falta e o NOME.
PROPOSTA_DE_ESPECIE = {
    232: ("CORVIKNIGHT",
          "a tabela de gfx chama o 232 de 'corvo de armadura 64x64'; os 7 "
          "objetos deste gfx que abrem porta warpam para o balcao de taxi "
          "(Stow-on-Side 01, Isle of Armor 01, Wild Area 17), e as placas "
          "daquele balcao ja dizem 'This Corviknight takes you to ...' "
          "(GalarFala_G00M07_bg0 a bg5). Corviknight e o taxi voador de "
          "Sword/Shield e SPECIES_CORVIKNIGHT existe nesta build."),
    145: ("CORVIKNIGHT",
          "PROPOSTA da onda 3, lote M, pela MESMA evidencia que a condutora da "
          "onda 2 aceitou para o gfx 232 (decisao 1 do fechamento). As 10 "
          "portas deste gfx warpam TODAS para MAP_GALAR_STOW_ON_SIDE_01, que e "
          "o balcao de taxi: os 8 NPCs de balcao daquele mapa ja falam 'This "
          "Corviknight takes you to' e 'This Corviknight isn't ready to fly!' "
          "(GalarFala_G00M07_o11 a o18, data/scripts/galar_fala.inc:23-186). O "
          "gfx e 64x64 como o 232 e tem 32 usos contra os 30 dele, que e "
          "aproximadamente um por cidade. A tabela de gfx chama o 145 de "
          "'morcego rosa 64x64', e essa descricao NAO foi conferida contra o "
          "sprite nesta rodada: e o unico ponto em que esta proposta pode "
          "estar errada, e por isso ela sai como pendente e nao como fato."),
}


def sprite_do_gfx(gid):
    """(graphics_id, decisao pendente ou None) para um gfx da FONTE.

    Gfx de gente sai pela tabela de de-para de sempre. Gfx de POKEMON nao tem
    de-para: a condutora descartou esses objetos em 21/08 porque devolver
    sprite de gente mentiria a especie. Aqui eles voltam, porque o motor
    desenha Pokemon no overworld, mas o NOME da especie continua sendo decisao
    de quem conduz: o que este lote faz e propor com a evidencia junto, e
    marcar o pedido como pendente para o fechador nao colar no escuro.
    """
    sprite, cat, _papel = GFX.traduz(gid)
    if sprite:
        return sprite, None
    if gid in PROPOSTA_DE_ESPECIE:
        especie, porque = PROPOSTA_DE_ESPECIE[gid]
        return ("OBJ_EVENT_GFX_SPECIES(%s)" % especie,
                "PROPOSTA, precisa do sim da condutora: " + porque)
    return None, ("gfx %d da fonte e %s e nao tem sprite nosso; sem decisao de "
                  "especie este pedido nao pode ser colado" % (gid, cat))


# ------------------------------------------- bytecode: os dois remendos do M --
#
# O `cenas_galar.blocos()` e a desmontagem que os tres blocos de Galar usam, e
# ele e de OUTRO dono: este lote nao o edita. O que ele faz aqui e uma copia com
# DUAS diferencas declaradas, trocada por dentro so enquanto uma porta e
# traduzida (`TradutorPorta.cena`), e devolvida no `finally`.
#
#   1. `trainerbattle` deixa de derrubar a cena. O `blocos()` para em
#      "macro de tamanho variavel" porque a tabela de opcodes nao dimensiona o
#      0x5C, e por isso 6 portas caiam inteiras e as 10 de `GalarTrn_*` nem
#      chegavam a ser tentadas. O tamanho existe e ja esta medido em
#      `anda_scripts_galar.TRAINERBATTLE`: 6 bytes de cabecalho mais 4 por
#      ponteiro, com o numero de ponteiros dado pelo TIPO.
#   2. A GUARDA DE MOTOR DO DEMAKE sai, e sai pela regra da condutora da onda 3:
#      flag ou var do motor do demake que so CONDICIONA a porta vira flag nossa
#      quando a condicao faz parte do enredo, e SOME quando ela so escondia a
#      porta por mecanica que nao existe aqui. Aqui ela some, e a medicao diz
#      por que: as tres guardas medidas (`0x5467`, a var de "taxi liberado";
#      `0x825`, a flag de motor do demake) nao tem UM SO escritor na nossa
#      arvore. Dar flag a elas nao seria transcrever a condicao, seria escrever
#      uma porta que nunca abre, e o `checa_scripts` C14 ("flag lida que ninguem
#      acende") cobraria isso com razao.
#
# Como a guarda some, e nao vira `if` sempre verdadeiro: o ramo que CHEGA a um
# `warp` fica, sem condicao; o ramo que nao chega e apagado com o `checkflag` /
# `compare` que o guardava. Sem esta segunda parte o resultado seria os DOIS
# ramos rodando em fila (a mensagem de "ainda nao da" e logo depois a viagem),
# que e pior do que qualquer um dos dois.

NOMES_DE_WARP = set(AND.WARPS.values())
GUARDAS = ("checkflag", "compare_var_to_value")
DESVIOS = ("goto_if", "call_if")


def _desmonta(rom, tab, inicio, maxi=400):
    """([Bloco], falha), igual a cenas_galar.blocos mais o `trainerbattle`.

    O `trainerbattle` entra na lista de instrucoes com os argumentos
    [tipo, id do treinador na fonte, local_id, ponteiro...] e a travessia segue
    LINEARMENTE depois dele, que e o que o motor faz: `gotopostbattlescript`
    devolve o controle para a linha seguinte a macro. O ponteiro de CONTINUACAO
    (o `cont` da tabela) entra na fila de blocos, senao o `warp` que mora dentro
    da continuacao ficaria invisivel.
    """
    fora, vistos, fila, falha = [], set(), [inicio], None
    while fila:
        off = fila.pop(0)
        if off in vistos or not (0 <= off < len(rom)):
            continue
        vistos.add(off)
        b = C3.Bloco(off)
        # Offset de cada instrucao, na mesma ordem de `b.ins`. Quem precisa
        # dele e `tira_guarda_de_motor`, para saber onde comeca o caminho de
        # QUEDA (a condicao falsa) de um `goto_if`/`call_if`.
        b.offs = []
        fora.append(b)
        for _ in range(maxi):
            op = rom[off]
            if op == C3.ENCHIMENTO and b.ins and b.ins[-1][0] in DESVIOS:
                b.offs.append(off)
                b.ins.append(("end", []))
                b.enchimento = True
                break
            if op not in tab:
                falha = falha or "opcode 0x%02X" % op
                break
            nome, tams = tab[op]
            if op == 0x5C:
                tipo = rom[off + 1]
                if tipo not in AND.TRAINERBATTLE:
                    falha = falha or "trainerbattle de tipo %d" % tipo
                    break
                n_ptr, cont = AND.TRAINERBATTLE[tipo]
                tam = AND.TRAINERBATTLE_CAB + 4 * n_ptr
                if off + tam > len(rom):
                    falha = falha or "fim de rom"
                    break
                args = [tipo,
                        int.from_bytes(rom[off + 2:off + 4], "little"),
                        int.from_bytes(rom[off + 4:off + 6], "little")]
                for i in range(n_ptr):
                    p = off + AND.TRAINERBATTLE_CAB + 4 * i
                    args.append(int.from_bytes(rom[p:p + 4], "little"))
                b.offs.append(off)
                b.ins.append(("trainerbattle", args))
                if cont is not None:
                    alvo = args[3 + cont]
                    if C3.BASE <= alvo < C3.BASE + len(rom):
                        fila.append(alvo - C3.BASE)
                off += tam
                continue
            if tams is None:
                falha = falha or "macro de tamanho variavel: " + nome
                break
            args, p = [], off + 1
            for s in tams:
                if p + s > len(rom):
                    args = None
                    break
                args.append(int.from_bytes(rom[p:p + s], "little"))
                p += s
            if args is None:
                falha = falha or "fim de rom"
                break
            b.offs.append(off)
            b.ins.append((nome, args))
            if nome == "goto":
                if C3.BASE <= args[0] < C3.BASE + len(rom):
                    fila.append(args[0] - C3.BASE)
                break
            if nome in ("call", "goto_if", "call_if"):
                alvo = args[-1]
                if C3.BASE <= alvo < C3.BASE + len(rom):
                    fila.append(alvo - C3.BASE)
            if nome in ("end", "return"):
                break
            off = p
        else:
            falha = falha or "script longo demais"
    return fora, falha


def _tem_warp(rom, tab, alvo, teto=24):
    """True quando algum caminho a partir do OFFSET `alvo` chega a um `warp`."""
    bs, _falha = _desmonta(rom, tab, alvo, maxi=200)
    return any(n in NOMES_DE_WARP for b in bs[:teto] for n, _a in b.ins)


def _e_guarda_de_motor(nome, args, nome_da_flag, nome_da_var):
    """True quando a instrucao le flag/var que a NOSSA arvore nao tem dono.

    A regua e a mesma de `cenas_galar.Tradutor.flag` e `.var`, e nao uma
    heuristica ao lado dela: e exatamente o que faria a cena inteira cair.
    """
    if nome == "checkflag":
        return args[0] not in nome_da_flag
    if nome == "compare_var_to_value":
        v = args[0]
        return not (0x8000 <= v < 0x8100) and v not in nome_da_var
    return False


def tira_guarda_de_motor(rom, tab, bs, nome_da_flag, nome_da_var):
    """Apaga as guardas de motor do demake dos blocos. Devolve o que apagou.

    Devolve (soltas, escolhem). `soltas` e [(nome, valor, "abre"/"fecha"/
    "morta")], para o relatorio dizer o que a porta perdeu sem ninguem reler o
    `.inc`. `escolhem` e a lista das guardas que NAO sairam porque os DOIS lados
    delas levam a um `warp`: essas nao escondem a porta, escolhem entre portas, e
    a cena inteira cai (a flag continua sem nome e `self.flag()` a derruba logo
    a seguir, com o motivo da fonte).
    """
    soltas, escolhe, criadas = [], [], set()
    for b in bs:
        velhas, offs = list(b.ins), list(getattr(b, "offs", []))
        novas, i = [], 0
        while i < len(b.ins):
            nome, args = b.ins[i]
            prox = b.ins[i + 1] if i + 1 < len(b.ins) else None
            if (nome == "checkflag" and (prox is None or prox[0] not in DESVIOS)
                    and _e_guarda_de_motor(nome, args, nome_da_flag,
                                           nome_da_var)
                    and not any(n == "compare_var_to_value" and a
                                and a[0] == 0x800D
                                for n, a in b.ins[i + 1:])):
                # `checkflag` sem `goto_if`/`call_if` depois nao decide NADA: e
                # a mesma leitura morta que `cenas_galar._arruma_rabo` ja
                # transforma em comentario depois da emissao (a trava C27 de
                # 23/08/2026). So que ela nunca chega la quando a flag e do
                # motor do demake, porque `self.flag()` derruba a cena antes.
                # Sai aqui, e sai com a unica ressalva que importa: se alguem
                # comparar VAR_RESULT depois no MESMO bloco, o `checkflag` NAO
                # e morto, e a linha fica onde esta para a cena cair como antes.
                soltas.append((nome, args[0], "morta"))
                i += 1
                continue
            if (nome in GUARDAS and prox and prox[0] in DESVIOS
                    and _e_guarda_de_motor(nome, args, nome_da_flag,
                                           nome_da_var)):
                alvo = prox[1][-1]
                abre = (C3.BASE <= alvo < C3.BASE + len(rom)
                        and _tem_warp(rom, tab, alvo - C3.BASE))
                # O CAMINHO DE QUEDA (condicao falsa) tambem tem de ser medido,
                # e nao medi-lo foi o defeito que esta rodada pagou. Em
                # `Galar_Wyndon03` (0x88C5B68) a fonte encadeia dez estagios de
                # `checkflag F; goto_if 1, <proximo>; msgbox; warp; end`: a
                # guarda nao ESCONDE a porta, ela ESCOLHE qual das dez portas o
                # jogador pega. Tratar cada uma como "o ramo guardado leva ao
                # warp, entao vire goto incondicional" apagava o `warp` da
                # queda em cada estagio e deixava um corredor de dez `goto` com
                # UMA porta no fim. O relatorio dizia oito destinos e o jogo
                # entregava um.
                cai = (offs[i + 2] if i + 2 < len(offs) else None)
                queda = cai is not None and _tem_warp(rom, tab, cai)
                if abre and queda:
                    escolhe.append((nome, args[0]))
                    novas.append((nome, args))
                    novas.append(prox)
                    i += 2
                    continue
                soltas.append((nome, args[0], "abre" if abre else "fecha"))
                if abre:
                    # So o ramo guardado leva a porta: ele fica, sem condicao.
                    # `goto_if` vira `goto` e o que vinha depois dele no bloco
                    # morre junto, porque no bytecode ele so rodava quando a
                    # condicao era FALSA, e ali nao ha porta nenhuma.
                    nova = ("call" if prox[0] == "call_if" else "goto", [alvo])
                    criadas.add(id(nova))
                    novas.append(nova)
                    if prox[0] == "goto_if":
                        break
                i += 2
                continue
            novas.append((nome, args))
            i += 1
        # CHAMADA DE RABO. A guarda que sai deixa `call X` seguido de `return`,
        # e no bytecode da fonte esse `return` era o rabo da SUBROTINA que a
        # condicao chamava. Com a condicao fora, `call X; return` e a mesma
        # coisa que `goto X` (o `end` de X para o script de qualquer jeito), so
        # que a primeira forma deixa um `return` que nenhum `call` alcanca, e o
        # `checa_scripts` C06 cobra isso com razao: e ROM gasta com uma linha
        # que nunca roda. Medido em 08/09/2026: sem esta troca, os 9 balcoes de
        # taxi somavam 9 achados C06 novos.
        if (len(novas) >= 2 and novas[-1][0] == "return"
                and novas[-2][0] == "call"
                and id(novas[-2]) in criadas):
            alvo_rabo = novas[-2][1][0]
            novas = novas[:-2] + [("goto", [alvo_rabo])]
        b.ins = novas
        del velhas
    return soltas, escolhe


def tira_fala_sem_traducao(rom, cmap, bs):
    """Apaga o `msgbox` cuja fala ninguem verteu. Devolve o portugues que saiu.

    DECISAO da condutora da onda 3: texto sem traducao vira LISTA (o
    `onda3_lote_m_falta_traduzir.json`) e o script sai SEM a fala, em vez de a
    porta inteira cair. Este lote nao traduz texto novo.

    O par que sai e sempre `loadword 0, <ponteiro>` + `callstd <caixa de
    msgbox>`, que e o unico idioma de fala que o tradutor do c3 reconhece; e o
    par sai INTEIRO, porque `loadword` sozinho carrega um ponteiro que nada le
    e `callstd` sozinho abre uma caixa com o texto anterior.

    A regua e a do L1 (`fala_galar.traducao()` mais `idioma_do_texto`, a mesma
    funcao que o T07 do portao usa), consultada por TEXTO: o rotulo destas falas
    nem existe ainda, entao o degrau por rotulo nunca poderia acertar. O que
    muda aqui e o LADO em que a duvida cai, e a mudanca esta MEDIDA:

    Nos tres geradores de fala a regra 3 do L1 deixa passar o que a regua nao
    chama de portugues ("neutro"), e isso e certo LA, porque la o texto ja esta
    na arvore e mexer nele mudaria arquivo sem mudar jogo. Aqui o texto e NOVO,
    e a conta se inverte. Medido em 08/09/2026 sobre o corpo que este gerador
    emitia com a regra 3: de 16 blocos `.string`, 7 eram portugues visivel ("O
    campeao dessa fase do World Tornament e, {PLAYER}.", "Tudo bem sem
    resentimentos agora voce pode seguir em frente") e SO 4 deles a regua do
    portao acusaria, porque ela pede DOIS marcadores e essas frases tem um. Ou
    seja: seguir a regra 3 poria portugues novo em Galar, que fala ingles por
    decisao 32 do Gui, sem que o T07 subisse um numero.

    Entao aqui o teste e de PROVA e nao de suspeita: escreve-se o bloco quando o
    de-para o cobre ou quando a regua do portao o chama de "en"; o resto sai e e
    listado. Isto nao e uma segunda regua de idioma (a funcao e a mesma), e ela
    so consegue TIRAR texto, nunca escrever o errado. O preco esta contado: o
    "neutro" que era ingles curto sai junto, e aparece na lista de espera com o
    resto.
    """
    fora = []
    dp = FALA.traducao()
    for b in bs:
        novas, i = [], 0
        while i < len(b.ins):
            nome, args = b.ins[i]
            prox = b.ins[i + 1] if i + 1 < len(b.ins) else None
            if (nome == "loadword" and args and args[0] == 0 and prox
                    and prox[0] == "callstd" and prox[1]
                    and prox[1][0] in C3.STD_MSGBOX
                    and C3.BASE <= args[1] < C3.BASE + len(rom)):
                pt, motivo = FALA.texto(rom, cmap, args[1] - C3.BASE)
                if (not motivo and pt not in TRADUCAO
                        and pt not in dp.por_texto
                        and FALA.idioma_do_texto(pt) != "en"):
                    fora.append(pt)
                    i += 2
                    continue
            novas.append((nome, args))
            i += 1
        b.ins = novas
    return fora


def poda(bs):
    """So os blocos que o primeiro ainda alcanca, na ordem de descoberta.

    Tirar uma guarda pode deixar um bloco sem ninguem que o chame (o ramo de
    "ainda nao da" do balcao de taxi e o caso). Emiti-lo daria rotulo morto no
    `.inc`; podar aqui e barato porque nenhuma REFERENCIA e criada nesta fase,
    so removida, e `cena()` ja recusa ramo para offset nao visitado.
    """
    por_inicio = {b.inicio: b for b in bs}
    vivos, fila = set(), [bs[0].inicio] if bs else []
    while fila:
        o = fila.pop()
        if o in vivos or o not in por_inicio:
            continue
        vivos.add(o)
        for nome, args in por_inicio[o].ins:
            if nome in ("goto", "call", "goto_if", "call_if"):
                fila.append(args[-1] - C3.BASE)
    return [b for b in bs if b.inicio in vivos]


def treinador_do_rotulo(rotulo, texto=None):
    """(constante do treinador, rotulo do texto de derrota) de galar_treinadores.

    LIDO do `.inc` que `treinadores_galar.py` gera, e nunca remontado de cabeca:
    o numero do treinador sai da numeracao daquele gerador, e o rotulo de
    derrota e o unico texto de treinador que existe em ingles nesta arvore. Ler
    o arquivo tambem e a prova de que o rotulo ainda esta la; sumiu, a porta cai
    com motivo em vez de deixar um `.inc` que nao linka.
    """
    if texto is None:
        if not os.path.exists(TREINADORES_INC):
            return None, None
        texto = open(TREINADORES_INC).read()
    m = re.search(r"^%s::\n((?:\t.*\n)+)" % re.escape(rotulo), texto, re.M)
    if not m:
        return None, None
    b = re.search(r"^\ttrainerbattle\w*\s+(\w+),\s*(\S+?),?\s*(\S*)$",
                  m.group(1), re.M)
    if not b:
        return None, None
    derrota = "%s_Derrota" % rotulo
    if ("\n%s:\n" % derrota) not in texto:
        return None, None
    return b.group(1), derrota


class TradutorPorta(OBJ.TradutorObjeto):
    """O tradutor do c4a mais a tabela de especie do demake.

    O c3 traduz `setwildbattle`/`playmoncry`/`showmonpic` pela tabela de
    especies do POKEFIRERED, que tem 412 entradas. O demake tem 1.241, e a
    especie 1182 (0x49E), que e a que aparece em tres portas de Hammerlocke,
    esta fora do alcance daquela tabela: a cena inteira caia com "especie 1182
    da fonte sem nome no nosso species.h", que e verdade sobre a tabela do
    FireRed e falso sobre a nossa.

    Quem ja resolveu isso e `dev_scripts/estaticos_galar.py`: ele LE a tabela de
    NOMES da propria ROM do demake e casa por nome com o nosso `species.h`,
    recusando forma repetida (mega, Gigantamax, regional) em vez de escolher.
    Aqui a unica coisa nova e usar aquela tabela; nao ha nome montado a mao, e
    especie sem par continua recusando a cena inteira. Medido em 07/09/2026:
    1182 e `SPECIES_ETERNATUS`, que e o que a cena de Hammerlocke pede.
    """

    # SUBSTITUICAO DE PASSO, e ela e DECISAO DECLARADA, nao traducao.
    # O FRLG tem `MOVEMENT_ACTION_FACE_<dir>_FAST` (0x4-0x7) e este motor nao
    # tem passo nenhum com esse nome. Os dois viram o objeto para a MESMA
    # direcao e param no MESMO estado; a unica diferenca e que o `_FAST` pula os
    # quadros de espera da virada. Trocar pelo `FACE_<dir>` normal custa alguns
    # quadros de animacao e nao muda um bit do que o jogador leva consigo, e sem
    # a troca quatro portas caem inteiras (as tres do Eternatus em Hammerlocke,
    # que levam a Postwick 02, e a de Motostoke 06 para Wedgehurst 09).
    # Nenhum outro `_FAST` entra: `WALK_FAST_*` e `WALK_IN_PLACE_FAST*` mudam
    # VELOCIDADE de deslocamento, e ali a troca desencontraria a cena.
    SUBSTITUICAO_DE_PASSO = {
        "MOVEMENT_ACTION_FACE_DOWN_FAST": "MOVEMENT_ACTION_FACE_DOWN",
        "MOVEMENT_ACTION_FACE_UP_FAST": "MOVEMENT_ACTION_FACE_UP",
        "MOVEMENT_ACTION_FACE_LEFT_FAST": "MOVEMENT_ACTION_FACE_LEFT",
        "MOVEMENT_ACTION_FACE_RIGHT_FAST": "MOVEMENT_ACTION_FACE_RIGHT",
    }

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        nossos = C3.constantes(
            f"{RAIZ}/include/constants/event_object_movement.h",
            "MOVEMENT_ACTION")
        self.passos_trocados = {}
        self.traduzidos = {}
        self.sem_traducao = []      # texto da fonte que ninguem verteu ainda
        self.falas_cortadas = []    # fala que saiu por falta de ingles
        self.guardas_soltas = []    # guardas de motor do demake que sairam
        self.treinador = None       # (constante, rotulo de derrota) ou None
        self.batalhas_sem_treinador = []
        self.batalhas_escritas = []
        self.sem_objeto = False     # gatilho/placa: nao ha objeto selecionado
        self.n_batalha = 0
        for valor, nome in list(self.mov_nomes.items()):
            alvo = self.SUBSTITUICAO_DE_PASSO.get(nome)
            if alvo and self.mov_de_para.get(valor) is None and alvo in nossos:
                self.mov_nomes[valor] = alvo
                self.mov_de_para[valor] = nossos[alvo]
                self.passos_trocados[nome] = alvo

    def especie(self, ident):
        alvo, _motivo = EST.de_para_especie().get(ident, (None, None))
        if alvo:
            return alvo
        return super().especie(ident)

    def texto(self, ptr, rotulo):
        """O texto da fonte em ingles: a TABELA DAQUI primeiro, o resto do L1.

        ONDA 3: o `cenas_galar.Tradutor.texto` deixou de ser o decodificador
        cru que o lote F herdou e passou a ser o pipeline de traducao dos tres
        degraus (rotulo em `traducao_galar.json`, texto em
        `resgate_galar_texto.json`, regua do portao), com caderno proprio do que
        falta. Este lote NAO tem regua de traducao propria nenhuma: duas reguas
        para o mesmo fato e a licao 4.11. O que sobra aqui e SEMENTE, e ela e
        pequena e datada: das tres falas que o lote F verteu a mao na onda 2,
        UMA entrou depois no `resgate_galar_texto.json` e DUAS nao (medido em
        08/09/2026). Sem estas duas linhas, a porta do hotel de Motostoke, que
        ja esta escrita e colada, cairia nesta rodada por falta de ingles, e o
        `.inc` perderia um rotulo que o `map.json` chama.
        """
        if not (C3.BASE <= ptr < C3.BASE + len(self.rom)):
            raise C3.Recusa("ponteiro de texto fora da rom")
        bruto, motivo = FALA.texto(self.rom, self.cmap, ptr - C3.BASE)
        if motivo:
            raise C3.Recusa("texto recusado: " + motivo)
        en = TRADUCAO.get(bruto)
        if en is not None:
            # A requebra por PIXEL e obrigatoria aqui e nao no de-para: os pares
            # do de-para ja vem requebrados (o aplicador da onda 2 os requebrou),
            # e os desta tabela sao ingles cru escrito a mao no lote F.
            # `linhas_de_texto` so PARTE o texto nos `\n`/`\l`/`\p` que ja
            # existem; sem a requebra a caixa estoura os 208 px e o proprio
            # `--demo` reprova.
            en = REQUEBRA.requebra(en)
            self.traduzidos[bruto] = en
            return FALA.linhas_de_texto(rotulo, en)
        try:
            return super().texto(ptr, rotulo)
        except C3.Recusa as e:
            # O caderno do L1 (`onda3_falta_traduzir.json`) e de outro dono, e
            # este lote nao escreve nele. O que ele guarda e a MESMA falta, de
            # olho no proprio `onda3_lote_m_falta_traduzir.json`, com a porta e
            # os destinos ao lado, que o caderno compartilhado nao tem por que
            # saber.
            if str(e) == FALA.MOTIVO_SEM_TRADUCAO:
                self.sem_traducao.append(bruto)
            raise

    # -- os dois remendos do lote M -----------------------------------------

    def cena(self, inicio, base):
        """A cena do c3/c4a, com a desmontagem deste lote no lugar da dele.

        A troca e por CHAMADA e devolvida no `finally`: nenhum outro gerador
        importa este arquivo, e mesmo assim deixar `cenas_galar.blocos` trocado
        depois de sair daqui seria efeito colateral em modulo de outro dono.
        """
        def blocos_daqui(rom, tab, ini, maxi=400):
            bs, falha = _desmonta(rom, tab, ini, maxi)
            if falha:
                return bs, falha
            soltas, escolhem = tira_guarda_de_motor(
                rom, tab, bs, self.nome_da_flag, self.nome_da_var)
            self.guardas_soltas.extend(soltas)
            if escolhem:
                raise C3.Recusa(
                    "guarda de motor do demake que ESCOLHE entre portas, e nao "
                    "esconde uma: %s. Os dois lados dela levam a warp, entao "
                    "tirar a condicao seria escolher o destino por conta "
                    "propria" % ", ".join(sorted(
                        "%s 0x%X" % (n, v) for n, v in escolhem)))
            self.falas_cortadas.extend(
                tira_fala_sem_traducao(rom, self.cmap, bs))
            return poda(bs), None

        velho = C3.blocos
        C3.blocos = blocos_daqui
        try:
            return super().cena(inicio, base)
        finally:
            C3.blocos = velho

    def extra(self, nome, args, corpo, base):
        if nome == "trainerbattle":
            return self._batalha(args, corpo, base)
        return super().extra(nome, args, corpo, base)

    def _batalha(self, args, corpo, base):
        """A batalha da fonte pelo MOLDE SEM FALA, que e o que a C28 exige.

        O molde com intro (`trainerbattle_single` e irmaos) passa por `special
        SetTrainerFacingDirection`, e esse special assere que ha objeto de
        evento selecionado (`src/battle_setup.c:1258`). Porta de GATILHO nao tem
        objeto nenhum selecionado, e o cartucho para na tela azul: e a trava
        C28, achada no playtest de 06/09/2026. O caminho sem intro
        (`trainerbattle_no_intro` -> `EventScript_DoNoIntroTrainerBattle`) nao
        chama o special, e por isso e o unico molde que serve para as duas
        entradas; usa-lo tambem no objeto custa a fala de abertura, que este
        lote nao teria como escrever de qualquer jeito (traduzir texto novo esta
        fora do escopo).
        `goto_if_defeated` vem junto porque o molde sem intro NAO confere a flag
        de vitoria por dentro, e sem ele o treinador rebate toda vez que o
        jogador passa (mesma licao do T147.8, 22/08/2026).
        """
        tipo, fid = args[0], args[1]
        if self.treinador is None:
            # DECISAO da condutora da onda 3: `trainerbattle` em porta sai pelo
            # molde sem fala SE houver treinador; senao, so o `warp`. Nao ha
            # treinador quando a entrada e gatilho ou quando o objeto nao passou
            # por `treinadores_galar.py`, e ali nao existe constante para
            # nomear: inventar um id seria escolher um time por conta propria.
            # A batalha some, e some DECLARADA, no `.inc` e no relatorio.
            self.batalhas_sem_treinador.append((fid, tipo))
            corpo.append("\t@ trainerbattle tipo %d, treinador %d da fonte: "
                         "SAIU. Nenhum treinador nosso foi numerado para esta "
                         "entrada por treinadores_galar.py, e a porta segue so "
                         "com o warp (decisao da condutora, onda 3 lote M)."
                         % (tipo, fid))
            return True
        const, derrota = self.treinador
        fim = "%s_Batalha%d_Fim" % (base, self.n_batalha)
        self.n_batalha += 1
        corpo.append("\t@ trainerbattle tipo %d, treinador %d da fonte, pelo "
                     "molde SEM INTRO (C28)" % (tipo, fid))
        corpo.append("\t%s %s, %s" % (self.macro("goto_if_defeated"), const, fim))
        if self.sem_objeto:
            # `EventScript_DoNoIntroTrainerBattle` faz `applymovement
            # VAR_LAST_TALKED, ...` sem perguntar, e numa entrada sem objeto
            # `gSpecialVar_LastTalked` vale LOCALID_NONE. Apontar para o jogador
            # e o remendo do FireRed vanilla (`Route24_EventScript_BattleRocket`)
            # e e no-op visivel, porque `reveal_trainer` em objeto que nao e
            # BURIED nem disfarce nao faz nada.
            corpo.append("\t%s VAR_LAST_TALKED, LOCALID_PLAYER"
                         % self.macro("setvar"))
        corpo.append("\t%s %s, %s" % (self.macro("trainerbattle_no_intro"),
                                      const, derrota))
        corpo.append("%s:" % fim)
        self.batalhas_escritas.append((fid, const))
        return True


def nome_flag_local(chave, f):
    """Nome da flag que o proprio script da fonte acende e le.

    O nome carrega a CHAVE DA FONTE e o hex da flag, e nao o nome do mapa nosso
    (o G3 renomeia 140 dos 438) nem um contador (contador anda quando uma cena
    entra ou sai do filtro, e o header inteiro vira diff).
    """
    return "FLAG_GALAR_PORTA_%s_%03X" % (chave.upper(), f)


def rotulo(p):
    """Rotulo estavel: sai da chave da FONTE, como em todos os blocos de Galar.

    O G3 renomeia 140 dos 438 mapas; rotulo com nome nosso vira diff sozinho na
    proxima renomeacao.
    """
    return "%s%s_%s%d" % (PREFIXO, p["fonte"].upper(),
                          "c" if p["tipo"] == "gatilho" else "o", p["src_i"])


# -------------------------------------------------------------- traducao ----

def ja_transcrita(p, textos_inc):
    """True quando algum .inc de Galar ja escreve ESTE warp (destino + x/y).

    E o caso dos `GalarObj_*` do c4a, que portaram a cena inteira e levaram o
    `warp` junto: o lote nao tem trabalho ali, e contar como pendente faria a
    fila mentir para cima.
    """
    return (p["destino"], str(p["wx"]), str(p["wy"])) in textos_inc


def warps_dos_inc():
    fora = set()
    for f in sorted(glob.glob(f"{RAIZ}/data/scripts/galar_*.inc")):
        if os.path.abspath(f) == os.path.abspath(INC):
            continue
        for m in re.finditer(r"^\s*warp(?:silent)?\s+(MAP_[A-Z0-9_]+),\s*(\d+),"
                             r"\s*(\d+)", open(f).read(), re.M):
            fora.add((m.group(1), m.group(2), m.group(3)))
    return fora


_LAYOUTS = {}


def alcancavel(chave, nosso_dir, x, y, docs):
    """(True, None) quando o jogador consegue falar com um objeto em (x, y).

    Tres condicoes, e as tres sao as do proprio `gente_galar.py`: o tile e
    andavel, ha pelo menos um vizinho andavel (senao nao ha de onde encarar), e
    o tile nao e de warp (NPC em cima de warp tranca a porta).
    """
    if not _LAYOUTS:
        _LAYOUTS.update(tamanho_do_mapa())
    caminho = "%s/data/maps/%s/map.json" % (RAIZ, nosso_dir)
    if caminho not in docs:
        docs[caminho] = json.load(open(caminho))
    d = docs[caminho]
    w, h = _LAYOUTS[d["layout"]]
    if any(v.get("x") == x and v.get("y") == y
           for v in (d.get("warp_events") or [])):
        return False, "em cima de tile de warp"
    if not GENTE.andavel(chave, w, h, x, y):
        return False, "tile nao andavel"
    vizinhos = [(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))]
    if not any(0 <= a < w and 0 <= b < h and GENTE.andavel(chave, w, h, a, b)
               for a, b in vizinhos):
        return False, "sem vizinho andavel de onde encarar"
    return True, None


def tile_de_gatilho(chave, nosso_dir, x, y, docs):
    """"andavel..." quando o jogador pisa em (x, y), ou o motivo de nao pisar."""
    if not _LAYOUTS:
        _LAYOUTS.update(tamanho_do_mapa())
    caminho = "%s/data/maps/%s/map.json" % (RAIZ, nosso_dir)
    if caminho not in docs:
        docs[caminho] = json.load(open(caminho))
    d = docs[caminho]
    w, h = _LAYOUTS[d["layout"]]
    if not (0 <= x < w and 0 <= y < h):
        return "fora do mapa (%dx%d)" % (w, h)
    if not GENTE.andavel(chave, w, h, x, y):
        return "tile nao andavel"
    em_warp = any(v.get("x") == x and v.get("y") == y
                  for v in (d.get("warp_events") or []))
    return ("andavel (colisao 0 no map.bin)"
            + (", e em cima de warp: o gatilho dispara antes da porta"
               if em_warp else ", e fora de tile de warp"))


_SAIDAS_FONTE = {}


def saidas_de_script_da_fonte():
    """{chave da fonte: quantos `warp` SAEM daquele mapa por script}.

    A regra de ida e volta nao pode olhar so o nosso `map.json`: o mapa de
    chegada de uma porta de script quase sempre e um mapa cuja SAIDA tambem e
    porta de script (o balcao de taxi de Stow-on-Side nao tem `warp_event`
    nenhum, e no demake se sai dele por script). Contar so `warp_events` diria
    "o jogador fica preso" para a rede de taxi inteira, e isso e defeito da
    MEDICAO, nao do jogo.
    """
    if _SAIDAS_FONTE:
        return _SAIDAS_FONTE
    dp, src, comp, _rom, and_, _orf = fonte()
    for f in sorted(dp):
        n = 0
        for _rot, p in AND.pontos_de_entrada(and_, comp.get(f), src[f]):
            n += len(and_.anda(p))
        _SAIDAS_FONTE[f] = n
    return _SAIDAS_FONTE


def saidas_do_destino(destino_dir, docs, destino_fonte=None):
    """(n_warps, n_conexoes, n_warps_de_script_da_fonte) do mapa de chegada."""
    caminho = "%s/data/maps/%s/map.json" % (RAIZ, destino_dir)
    if caminho not in docs:
        docs[caminho] = json.load(open(caminho))
    d = docs[caminho]
    por_script = (saidas_de_script_da_fonte().get(destino_fonte, 0)
                  if destino_fonte else 0)
    return (len(d.get("warp_events") or []), len(d.get("connections") or []),
            por_script)


def tamanho_do_mapa():
    """{nome do layout: (w, h)} e {dir do mapa: layout}, para conferir o x/y."""
    lay = {l["id"]: (l["width"], l["height"])
           for l in json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}
    return lay


def vars_ja_de_galar():
    """Enderecos de var que os OUTROS blocos de Galar ja apelidaram em vars.h.

    ARMADILHA MEDIDA em 08/09/2026, e ela e calada: `cenas_galar.vars_livres()`
    tira do header TODOS os blocos "Fase de conteudo de Galar" antes de medir,
    de proposito, para que a segunda rodada de um gerador nao veja as vars que
    ele mesmo alocou como ocupadas. O efeito colateral e que ela devolve como
    livres as vars dos OUTROS blocos de Galar tambem: hoje 0x4100, 0x4107 a
    0x410F, 0x4112, 0x4113, 0x4115 e 0x4116 aparecem livres e estao todas em
    uso pelo c1 (`VAR_GALAR_*_CENA`) e pelo c4d (`VAR_GALAR_*_OBJ`). Alocar
    dali daria a MESMA casa de save para dois estados diferentes, e nada ficaria
    vermelho. Aqui a lista dos outros blocos volta a contar; so o bloco DESTE
    gerador continua fora.
    """
    texto = open(VARS_H).read()
    texto = re.sub("%s.*?%s" % (re.escape(MARCA_VAR_INI), re.escape(MARCA_VAR_FIM)),
                   "", texto, flags=re.S)
    fora = set()
    for bloco in re.finditer(r"// >>> Fase de conteudo de Galar.*?// <<< Fase "
                             r"de conteudo de Galar[^\n]*\n", texto, re.S):
        for m in re.finditer(r"VAR_UNUSED_0x([0-9A-Fa-f]{4})", bloco.group(0)):
            fora.add(int(m.group(1), 16))
    return fora


def chave_da_fila(rotulo):
    """`GalarFalaI_G13M00_o1` -> `g13m00/objeto/1`, ou None."""
    m = re.match(r"Galar(?:FalaI|Fala)_([A-Z0-9]+)_o(\d+)$", str(rotulo or ""))
    return "%s/objeto/%s" % (m.group(1).lower(), m.group(2)) if m else None


_FILA = {}


def ponteiro_da_fala(rotulo):
    """O `ponteiro_fonte` de que o rotulo de FALA nasceu, ou None.

    E a prova de que a porta CONTEM a fala: mesmo ponto de entrada, mesma cena
    traduzida, mais o `warp`. Sem esta igualdade a porta nao toma o objeto.
    """
    if not _FILA:
        f = json.load(open(f"{RAIZ}/dev_scripts/fila_galar.json",
                           encoding="utf-8"))
        for l in (f["linhas"] if isinstance(f, dict) else f):
            if l.get("ponteiro_fonte"):
                _FILA[l["chave"]] = int(l["ponteiro_fonte"], 16) + AND.ROM_BASE
    chave = chave_da_fila(rotulo)
    return _FILA.get(chave) if chave else None


def plano():
    """(aceitas, recusas, docs, vars, flags). Uma passada por PORTA distinta."""
    lista, docs = classifica(portas())
    rom = open(FALA.ROM_FONTE, "rb").read()
    tab = FALA.tabela_de_opcodes()
    cmap = FALA.charmap()
    gente = json.load(open(FALA.CENSO_GENTE))["linhas"]
    por_mapa = collections.defaultdict(list)
    for l in gente:
        por_mapa[l["mapa"]].append(l)
    mundo = json.load(open(f"{RAIZ}/dev_scripts/galar_mundo.json"))
    de_para = mundo["de_para"]
    rev = {(d["fonte_grupo"], d["fonte_indice"]): k for k, d in de_para.items()}
    musica = C3.musica_da_fonte()
    lay = tamanho_do_mapa()
    dir_layout = {}
    for caminho in glob.glob(f"{RAIZ}/data/maps/*/map.json"):
        d = json.load(open(caminho))
        dir_layout[os.path.basename(os.path.dirname(caminho))] = d.get("layout")

    esconde_glob = collections.defaultdict(list)
    for o in gente:
        if (o["tipo"] == "objeto" and o.get("flag_fonte")
                and o["motivo"].startswith("entrou")):
            esconde_glob[o["flag_fonte"]].append((o["mapa"], o["i"] + 1))

    # As flags de esconder que o c4b JA batizou, lidas do header (nunca
    # remontadas de cabeca: o nome carrega o hex da FONTE, e inventar um nome
    # que nao esta la so quebra no link).
    escondidas_com_nome = {}
    texto_flags = open(f"{RAIZ}/include/constants/flags.h").read()
    for m in re.finditer(r"#define\s+(FLAG_GALAR_ESCONDE_([0-9A-F]+))\s",
                         texto_flags):
        escondidas_com_nome[int(m.group(2), 16)] = m.group(1)
    # E as flags de MOTOR do demake que o lote L1 da onda 3 batizou na faixa
    # 0x2300-0x237F (`FLAG_GALAR_MOTOR_<hex da fonte>`, escritas por
    # `objetos_galar.py`). Elas entram aqui pela MESMA razao das de esconder:
    # duas flags para a mesma flag da fonte fariam o portao ler uma coisa num
    # script e outra no vizinho. E a diferenca pratica e grande: flag COM nome e
    # transcrita, e so flag SEM nome nenhum cai na regra de "some" da condutora.
    # Medido em 08/09/2026: L1 batizou 0x26C, 0x26D, 0x26F, 0x467, 0x4B3, 0x4B6,
    # 0x826, 0x827 e 0x829, e NENHUMA delas e uma das que este lote solta
    # (0x824, 0x825 e a var 0x5467). Ou seja hoje esta linha nao muda um numero;
    # ela existe para o dia em que L1 crescer a lista.
    for m in re.finditer(r"#define\s+(FLAG_GALAR_MOTOR_([0-9A-F]+))\s",
                         texto_flags):
        escondidas_com_nome.setdefault(int(m.group(2), 16), m.group(1))

    ja = warps_dos_inc()
    # Uma PORTA e um par (script de entrada, warp). Varios warps saem do mesmo
    # script (o balcao de Wyndon manda para 12 mapas), e um script so e
    # traduzido UMA vez: a chave de traducao e o ponto de entrada.
    por_entrada = collections.OrderedDict()
    for p in lista:
        por_entrada.setdefault((p["fonte"], p["ptr"]), []).append(p)

    # Flag LOCAL: a que o proprio script acende e le. Medida antes do laco,
    # sobre o bytecode, para o nome existir na primeira passada e o endereco
    # nao depender da ordem em que as cenas passam no filtro.
    flags_locais = {}
    for (chave, ptr), _g in por_entrada.items():
        bs, falha = _desmonta(rom, tab, int(ptr, 16) - C3.BASE)
        if falha:
            continue
        acende = {a[0] for b in bs for n, a in b.ins if n == "setflag" and a}
        le = {a[0] for b in bs for n, a in b.ins if n == "checkflag" and a}
        locais = sorted((acende & le) - set(esconde_glob))
        if locais:
            flags_locais[(chave, ptr)] = locais

    # Var por MAPA de origem, como no c3. So gasta endereco quem entrar. A
    # lista de livres passa pelo filtro de `vars_ja_de_galar()`: sem ele este
    # lote alocaria por cima do c1 e do c4d, calado (ver o docstring de la).
    ocupadas = vars_ja_de_galar()
    livres = [v for v in C3.vars_livres() if v not in ocupadas]
    aceitas, recusas, sem_traducao = [], [], []
    nome_var_de = {}

    for (chave, ptr), grupo in por_entrada.items():
        p0 = grupo[0]
        alvo_destinos = sorted({g["destino"] for g in grupo})
        base = {"chave": chave, "ptr": ptr, "balde": p0["balde"],
                "origem": p0["origem"], "origem_dir": p0["nosso_dir"],
                "caminho": p0["caminho"], "destinos": alvo_destinos,
                "portas": len(grupo), "linhas": grupo}

        def nega(motivo):
            recusas.append(dict(base, motivo=motivo))

        if p0["balde"] == "?":
            nega(p0.get("motivo", "fora dos quatro baldes"))
            continue

        # BALDE C, e e aqui que a onda 3 muda de comportamento. Ate a onda 2
        # toda porta com rotulo de outro gerador saia como pendencia; agora ela
        # sai como pendencia SO quando o dono nao respeita `GalarPorta_`.
        base["tomado_de"] = None
        if p0["balde"] == "C":
            dono = str(p0["nosso_script"] or "0")
            prefixo = next((t for t in TOMAVEIS if dono.startswith(t)), None)
            if prefixo is None:
                if all(ja_transcrita(g, ja) for g in grupo):
                    base["ja_feita"] = True
                    aceitas.append(dict(base, corpo=None, extras=None,
                                        rot=dono, acao="ja_escrita"))
                else:
                    nega("rotulo de dono que NAO respeita %s (%s); vai como "
                         "pendencia" % (PREFIXO, dono))
                continue
            if prefixo in TOMAVEIS_DE_FALA:
                de_onde = ponteiro_da_fala(dono)
                if de_onde != int(p0["ptr"], 16):
                    nega("rotulo de fala %s nasceu de outro ponteiro da fonte "
                         "(%s, e esta porta e %s): a porta nao contem a fala, e "
                         "toma-lo calaria o NPC"
                         % (dono, "0x%X" % de_onde if de_onde else "nenhum",
                            p0["ptr"]))
                    continue
            base["tomado_de"] = dono

        # CORTE REGISTRADO. `cortado_por` no `map.json` e decisao ja tomada
        # (PLANO-ESCOPO.md): os quatro `Galar_WyndonIndoor05/10/15/20`, por
        # exemplo, sao salas de reserva do demake, blockdata copia byte a byte
        # de mapa vivo, carimbadas pelo lote AB2 da onda 1. A regua de
        # conectividade tira esses mapas da conta de orfao, e por isso porta
        # escrita a partir de um deles nao credita NADA: ela compila, ocupa ROM
        # e nunca roda, porque ninguem alcanca a origem. Medido em 08/09/2026:
        # sem este portao, 4 das portas escritas saiam de mapa cortado e o
        # relatorio contava 4 destinos que continuavam orfaos.
        # Destino cortado e pior ainda: seria porta para dentro de conteudo que
        # o Gui mandou tirar.
        cortes = []
        if docs[p0["caminho"]].get("cortado_por"):
            cortes.append("origem %s" % p0["nosso_dir"])
        for g in grupo:
            cam = "%s/data/maps/%s/map.json" % (RAIZ, g["destino_dir"])
            if cam not in docs:
                docs[cam] = json.load(open(cam))
            if docs[cam].get("cortado_por"):
                cortes.append("destino %s" % g["destino"])
        if cortes:
            nega("mapa com corte registrado (`cortado_por`): %s"
                 % ", ".join(sorted(set(cortes))))
            continue

        # Ida e volta: destino sem saida nenhuma PRENDE o jogador. Isso e bug
        # de verdade, e nao desenho, entao a porta inteira sai com motivo.
        preso, so_por_script = [], []
        for d in alvo_destinos:
            g0 = next(g for g in grupo if g["destino"] == d)
            n_w, n_c, n_s = saidas_do_destino(g0["destino_dir"], docs,
                                              g0["destino_fonte"])
            if (n_w, n_c, n_s) == (0, 0, 0):
                preso.append(d)
            elif (n_w, n_c) == (0, 0):
                so_por_script.append(d)
        if preso:
            nega("destino sem saida nenhuma (nem warp, nem conexao, nem warp "
                 "de script na fonte): %s" % ", ".join(preso))
            continue
        base["saida_so_por_script"] = so_por_script
        # O x/y do warp tem que caber no mapa de destino.
        fora_do_mapa = []
        for g in grupo:
            wh = lay.get(dir_layout.get(g["destino_dir"]))
            if wh and not (0 <= g["wx"] < wh[0] and 0 <= g["wy"] < wh[1]):
                fora_do_mapa.append("%s (%d,%d) em mapa %dx%d"
                                    % (g["destino_dir"], g["wx"], g["wy"],
                                       wh[0], wh[1]))
        if fora_do_mapa:
            nega("coordenada de chegada fora do mapa: " + "; ".join(fora_do_mapa))
            continue

        # PORTAO DO OBJETO NOVO (balde A). Objeto que o G4 nao pos no mapa volta
        # aqui, mas so se o jogador PUDER falar com ele: tile andavel, pelo
        # menos um vizinho andavel para o jogador ficar de frente, e fora de
        # tile de warp (NPC em cima de warp tranca a porta, que e a regra que o
        # proprio `gente_galar.py` aplica). Porta que compila e que ninguem
        # alcanca e divida com cara de trabalho feito.
        if p0["balde"] == "A":
            ruins = []
            for g in grupo:
                ok, porque = alcancavel(chave, g["nosso_dir"], g["src_x"],
                                        g["src_y"], docs)
                if not ok:
                    ruins.append("(%d,%d): %s" % (g["src_x"], g["src_y"], porque))
            if ruins:
                nega("objeto novo em lugar onde o jogador nao fala com ele: "
                     + "; ".join(sorted(set(ruins))))
                continue

        # PORTAO DO GATILHO, medido em 07/09/2026 lendo os dois motores.
        # `ShouldTriggerScriptRun` (src/field_control_avatar.c:1179) compara
        # `*GetVarPointer(trigger)` com o `index`, e quando o ponteiro e nulo
        # ele trata o numero como FLAG. No FireRed, `GetVarPointer` devolve
        # `&vars[idx - 0x4000]` para TUDO entre 0x4000 e 0x8000, e o array tem
        # 256 posicoes (VARS_END 0x40FF): var de gatilho como 0x6026 le 8.230
        # posicoes depois do fim do array, ou seja lixo. Var abaixo de 0x4000
        # (a fonte tem uma em 0x0003) devolve o proprio numero la e vira leitura
        # de FLAG aqui. Nos dois casos NAO EXISTE transcricao fiel: o que a
        # fonte faz e indefinido. Passa so o que esta na faixa declarada.
        # PORTAO DO GATILHO, refeito na onda 3 pela decisao da condutora: gatilho
        # de coordenada com var fora do array ganha `VAR_UNUSED` livre e pedido
        # de `coord_events`, em vez de cair.
        #
        # O que o portao da onda 2 media continua VERDADE e continua escrito:
        # `ShouldTriggerScriptRun` (src/field_control_avatar.c:1179) compara
        # `*GetVarPointer(trigger)` com o `index`, e no FireRed `GetVarPointer`
        # devolve `&vars[idx - 0x4000]` para tudo entre 0x4000 e 0x8000 num
        # array de 256 posicoes (VARS_END 0x40FF): 0x6026 le 8.230 posicoes
        # depois do fim. So que a conclusao dele estava um passo atras. O
        # `coord_event` que sai daqui e um evento NOVO, escrito por nos: quem
        # escolhe a var e este gerador, nao a fonte. O endereco da fonte deixa
        # de ser dado a copiar e passa a ser so a procedencia da linha (vai no
        # pedido, em `var_da_fonte`).
        #
        # O que NAO da para escolher e o VALOR: `var_value` vem da fonte, e uma
        # var recem-apelidada nasce em 0. Gatilho que so dispara com a var em 3
        # e gatilho que nunca dispara, porque nenhum script nosso escreve nela.
        # Esse cai, e cai com o numero na mao.
        if p0["balde"] == "D":
            mortos = sorted({g["src_valor"] for g in grupo if g["src_valor"]})
            if mortos:
                nega("gatilho da fonte so dispara com a var valendo %s, e "
                     "nenhum script nosso escreve nessa var: o coord_event "
                     "nasceria morto"
                     % ", ".join(str(v) for v in mortos))
                continue

        esconde = {f: [i for m, i in v if m == chave]
                   for f, v in esconde_glob.items()}
        esconde = {f: v for f, v in esconde.items() if v}
        # NOME DE FLAG, e aqui esta a diferenca deste lote para o c4a.
        #
        # 1. Flag que ESCONDE objeto importado ja tem dono: o c4b batizou cada
        #    uma de `FLAG_GALAR_ESCONDE_<hex da fonte>` em include/constants/
        #    flags.h. Reusar o NOME de la e obrigatorio; alocar uma segunda
        #    flag para a mesma flag da fonte faria o NPC sumir num script e
        #    continuar no outro. Flag de esconder que o c4b nao batizou nao
        #    ganha nome aqui: a faixa dela e do c4b, nao deste lote.
        # 2. Flag que ESTE MESMO script acende e le e caso diferente: ela nao
        #    depende de nada de fora, entao dar a ela uma flag da faixa
        #    EXCLUSIVA deste lote (0x2200-0x227F) transcreve o ramo sem
        #    inventar historia. Flag que o script so LE, e que quem acende e o
        #    codigo C do demake, continua recusando a cena inteira: dar flag a
        #    ela seria decidir por conta propria qual ramo o jogador ve.
        nomes_flag = {f: escondidas_com_nome[f] for f in esconde
                      if f in escondidas_com_nome}
        for f in flags_locais.get((chave, ptr), ()):
            nomes_flag[f] = nome_flag_local(chave, f)
        nome_var_de.setdefault(chave, "VAR_GALAR_PORTA_%s" % chave.upper())
        # Toda var salva da fonte que este script cita ganha o MESMO nome, que e
        # o preco declarado de "uma var por MAPA" que o c3 ja paga.
        bs, falha = _desmonta(rom, tab, int(ptr, 16) - C3.BASE)
        nomes_var = {}
        if not falha:
            for b in bs:
                for nome, args in b.ins:
                    if (nome in ("setvar", "addvar", "subvar",
                                 "compare_var_to_value")
                            and args and 0x4010 <= args[0] < 0x4200):
                        nomes_var[args[0]] = nome_var_de[chave]
        t = TradutorPorta(
            rom, tab, cmap,
            C3.de_para_de_objetos(chave, docs[p0["caminho"]], por_mapa),
            esconde, nomes_var, nomes_flag, musica, rev_mapa=rev)
        t.de_para_mapa = de_para
        # O treinador so existe quando o objeto DESTA porta ja foi numerado por
        # `treinadores_galar.py`, e o rotulo dele e o que estava no `map.json`.
        if base["tomado_de"] and base["tomado_de"].startswith("GalarTrn_"):
            const, derrota = treinador_do_rotulo(base["tomado_de"])
            if const is None:
                nega("o objeto tem %s, mas galar_treinadores.inc nao entrega "
                     "nem a constante nem o texto de derrota dele"
                     % base["tomado_de"])
                continue
            t.treinador = (const, derrota)
        t.sem_objeto = p0["balde"] == "D"
        rot = rotulo(p0)
        # A quem o caderno de traducao do L1 cobra o texto que falta. Porta nao
        # e linha da fila (a fila nao tem tipo `porta`), entao a chave e o
        # ROTULO daqui, que e o unico nome estavel que esta porta tem.
        t.chave_da_fila = rot
        try:
            # `cena()` recebe OFFSET, nao ponteiro: `blocos()` indexa `rom[off]`
            # direto. Passar o ponteiro de ROM (0x08...) nao levanta erro
            # nenhum: `blocos` descarta o offset por estar fora da ROM, devolve
            # zero blocos, e a cena sai como "no-op depois da traducao". Foi
            # assim que 39 portas apareceram como no-op na primeira medicao.
            corpo, usadas = t.cena(int(ptr, 16) - AND.ROM_BASE, rot)
        except C3.Recusa as e:
            for pt in list(t.sem_traducao) + list(t.falas_cortadas):
                sem_traducao.append({"origem": p0["nosso_dir"], "ptr": ptr,
                                     "rotulo": rot, "destinos": alvo_destinos,
                                     "pt": pt, "saiu_do_script": False})
            nega(str(e))
            continue
        if not any(("\twarp " in l or "\twarpsilent " in l) for l in corpo):
            nega("a traducao passou mas nao emitiu warp nenhum")
            continue
        # COBERTURA, e ela nasceu de um defeito medido nesta rodada: uma porta
        # pode passar por tudo e ainda assim entregar MENOS destinos do que
        # promete, se a cirurgia de guarda ou o filtro comerem um ramo pelo
        # caminho. Aqui a conta e direta: os `warp` que o corpo emite tem de
        # cobrir todos os (mapa, x, y) que esta entrada alcanca na fonte. O que
        # nao cobrir cai inteiro, porque contar destino que o jogador nao chega
        # e pior do que nao ter escrito a porta.
        emitidos = set(re.findall(r"^\twarp(?:silent)?\s+(MAP_[A-Z0-9_]+),\s*"
                                  r"(\d+),\s*(\d+)", "\n".join(corpo), re.M))
        faltam = sorted({(g["destino"], str(g["wx"]), str(g["wy"]))
                         for g in grupo} - emitidos)
        if faltam:
            nega("a traducao emitiu warp, mas nao para %s: a porta entregaria "
                 "menos destinos do que a fonte alcanca"
                 % ", ".join("%s (%s,%s)" % f for f in faltam))
            continue
        for pt in t.falas_cortadas:
            sem_traducao.append({"origem": p0["nosso_dir"], "ptr": ptr,
                                 "rotulo": rot, "destinos": alvo_destinos,
                                 "pt": pt, "saiu_do_script": True})
        aceitas.append(dict(base, corpo=corpo, rot=rot, acao="escrita",
                            usadas=dict(usadas), vars_citadas=sorted(nomes_var),
                            falas_cortadas=list(t.falas_cortadas),
                            guardas_soltas=t.guardas_soltas,
                            batalhas_escritas=t.batalhas_escritas,
                            batalhas_sem_treinador=t.batalhas_sem_treinador,
                            flags_locais=list(flags_locais.get((chave, ptr),
                                                              ()))))

    # Enderecos de var: so para quem entrou, na ordem da chave da FONTE. Entra
    # tambem quem NAO cita var no bytecode mas pede `coord_events`: o gatilho
    # que sai daqui e disparado por UMA var, e o nome dela tem de existir no
    # header, senao o `map.json` do fechador aponta para simbolo que nao linka.
    usa_var = sorted({a["chave"] for a in aceitas
                      if a.get("vars_citadas")
                      or any(g["balde"] == "D" for g in a["linhas"])})
    vars_alocadas = {}
    for i, chave in enumerate(usa_var):
        if i >= len(livres):
            raise SystemExit("acabaram as vars livres de verdade (%d) para as "
                             "%d que este lote pede" % (len(livres), len(usa_var)))
        vars_alocadas[nome_var_de[chave]] = livres[i]

    # Enderecos de FLAG, da faixa exclusiva deste lote, na ordem (chave da
    # fonte, flag). So gasta quem entrou, como no c3 e no c4a.
    quer = sorted({(a["chave"], f) for a in aceitas
                   for f in a.get("flags_locais") or ()})
    flags_alocadas = {}
    for i, (chave, f) in enumerate(quer):
        end = PRIMEIRA_FLAG + i
        if end > ULTIMA_FLAG:
            raise SystemExit("faixa de flag deste lote (0x%04X-0x%04X) esgotada"
                             % (PRIMEIRA_FLAG, ULTIMA_FLAG))
        flags_alocadas[nome_flag_local(chave, f)] = end
    return (aceitas, recusas, docs, vars_alocadas, flags_alocadas, lista,
            sem_traducao)


# --------------------------------------------------------------- escrita ----

CABECALHO = """@ Portas de SCRIPT dos orfaos de Galar (onda 2 lote F; onda 3 lote M).
@ Gerado por dev_scripts/portas_script_galar.py; NAO editar a mao.
@
@ Cada rotulo aqui e a transcricao do script do demake que contem `warp` e cai
@ num mapa que nenhum caminho alcanca. O tradutor e o mesmo do c3
@ (cenas_galar.py) e do c4a (objetos_galar.py); o que ele recusa nao aparece
@ aqui, aparece no relatorio com motivo.
@
@ TRES COISAS SAEM DO SCRIPT DA FONTE, e as tres aparecem em comentario no
@ bloco em que acontecem, nunca caladas:
@   * FALA CORTADA: fala que este lote nao consegue escrever em ingles. Galar
@     fala ingles (decisao 32 do Gui) e este lote nao traduz texto novo; o
@     portugues esta em dev_scripts/onda3_lote_m_falta_traduzir.json.
@   * GUARDA DE MOTOR DO DEMAKE SOLTA: `checkflag`/`compare` de flag ou var que
@     NENHUM script nosso escreve. Dar nome a ela seria escrever porta que nunca
@     abre; o ramo que leva ao `warp` fica, o outro sai.
@   * trainerbattle SEM treinador nosso: a batalha sai e a porta segue so com o
@     `warp`. Quando ha treinador numerado por treinadores_galar.py, a batalha
@     FICA, pelo molde sem intro (`goto_if_defeated` + `trainerbattle_no_intro`),
@     que e o unico que a C28 deixa passar em entrada sem objeto selecionado.
@
@ PRECEDENCIA: o rotulo daqui comeca com `GalarPorta_`, e ele esta em
@ `objetos_galar.MANDAM_MAIS`, a lista UNICA que objetos_galar.py (linha 129),
@ fala_galar.py (linha 745) e treinadores_galar.py (desde a onda 3) consultam
@ antes de escrever o campo `script` de um map.json de Galar. Por isso a porta
@ PODE tomar objeto que tem `GalarObj_`, `GalarFala_`, `GalarFalaI_` ou
@ `GalarTrn_`: o rotulo antigo continua definido no `.inc` dele e vira ROM
@ parada, e nada se perde, porque a porta transcreve a MESMA cena da fonte mais
@ o `warp` (no caso da fala, com a igualdade de ponteiro provada) ou a MESMA
@ batalha (no caso do treinador, chamando o texto de derrota dele).
@ Quem escrever campo `script` de map.json de Galar depois desta onda precisa
@ chamar `objetos_galar.manda_mais` antes, senao a porta se apaga calada.
"""


def corpo_inc(aceitas):
    partes = [CABECALHO]
    escritas = [a for a in aceitas if a["acao"] == "escrita"]
    for a in sorted(escritas, key=lambda z: (z["chave"], z["rot"])):
        partes.append("\n@ ---- %s (%s), %s -> %s ----\n"
                      % (a["origem_dir"], a["chave"], a["ptr"],
                         ", ".join(a["destinos"])))
        for pt in a.get("falas_cortadas") or []:
            partes.append("@ FALA CORTADA por falta de ingles (onda 3, lote M; "
                          "o portugues esta em\n@ "
                          "dev_scripts/onda3_lote_m_falta_traduzir.json): %r\n"
                          % pt[:70])
        for n, v, q in a.get("guardas_soltas") or []:
            partes.append("@ GUARDA DE MOTOR DO DEMAKE SOLTA: %s 0x%X, ramo "
                          "%s (nenhum script nosso escreve nela)\n"
                          % (n, v, q))
        partes.append("\n".join(a["corpo"]) + "\n")
    if not escritas:
        partes.append("\n@ Nenhuma porta passou no tradutor nesta rodada.\n")
    return "".join(partes)


def bloco_vars(vars_alocadas):
    if not vars_alocadas:
        return ""
    linhas = [MARCA_VAR_INI,
              "// Uma var por MAPA de origem, como no c3. Apelido de",
              "// VAR_UNUSED_* livre, medido por cenas_galar.vars_livres().",
              ]
    for nome, end in sorted(vars_alocadas.items(), key=lambda z: z[1]):
        linhas.append("#define %s VAR_UNUSED_0x%04X" % (nome, end))
    linhas.append(MARCA_VAR_FIM)
    return "\n".join(linhas) + "\n"


def bloco_flags(flags_alocadas):
    if not flags_alocadas:
        return ""
    linhas = [MARCA_FLAG_INI,
              "// Faixa EXCLUSIVA deste lote (0x2200-0x227F), dada na abertura da",
              "// onda 2. So entra flag que o PROPRIO script da fonte acende e le;",
              "// flag de esconder continua sendo do c4b, pelo nome dele.",
              ]
    for nome, end in sorted(flags_alocadas.items(), key=lambda z: z[1]):
        linhas.append("#define %-42s FLAG_UNUSED_0x%04X" % (nome, end))
    linhas.append(MARCA_FLAG_FIM)
    return "\n".join(linhas) + "\n"


def pedidos_de_mapjson(aceitas, lista, recusas=(), vars_alocadas=None,
                       docs=None):
    """Os pedidos que o FECHADOR cola nos map.json. Este lote nao os aplica."""
    obj, coord, script = [], [], []
    vars_alocadas = vars_alocadas or {}
    docs = {} if docs is None else docs
    vistos_obj, vistos_coord = set(), set()
    for a in aceitas:
        if a["acao"] != "escrita":
            continue
        for p in a["linhas"]:
            if p["balde"] in ("B", "C"):
                chave = (p["nosso_dir"], p["nosso_local_id"])
                if chave in vistos_obj:
                    continue
                vistos_obj.add(chave)
                era = str(p["nosso_script"] or "0")
                if era == a["rot"]:
                    # O fechador da onda anterior JA colou este reponte. Pedir
                    # de novo faria a lista mentir para cima e daria trabalho
                    # que ja esta feito; e tambem e a prova de idempotencia que
                    # o `--demo` cobra.
                    continue
                if era in ("0", ""):
                    porque = ("objeto mudo que na fonte abre a porta para %s"
                              % ", ".join(a["destinos"]))
                else:
                    porque = (
                        "objeto que hoje aponta para %s; na fonte o MESMO "
                        "script abre a porta para %s, e %s tem precedencia "
                        "sobre %s (objetos_galar.MANDAM_MAIS). O rotulo antigo "
                        "continua no .inc e passa a ser ROM parada."
                        % (era, ", ".join(a["destinos"]), PREFIXO,
                           era.split("_")[0] + "_"))
                script.append({
                    "mapa": p["nosso_dir"],
                    "indice_do_object_event": p["nosso_local_id"] - 1,
                    "x": p["src_x"], "y": p["src_y"],
                    "campo": "script", "valor": a["rot"],
                    "era": era,
                    "porque": porque,
                })
            elif p["balde"] == "A":
                chave = (p["nosso_dir"], p["src_x"], p["src_y"])
                if chave in vistos_obj:
                    continue
                vistos_obj.add(chave)
                sprite, decisao = sprite_do_gfx(p["src_gfx"])
                ok_tile, porque_tile = alcancavel(p["fonte"], p["nosso_dir"],
                                                  p["src_x"], p["src_y"], docs)
                obj.append({
                    "mapa": p["nosso_dir"],
                    "onde": "append no FIM de object_events (a save guarda "
                            "indice de object_event)",
                    "object_event": {
                        "graphics_id": sprite,
                        "x": p["src_x"], "y": p["src_y"],
                        "elevation": p["src_elev"] if p["src_elev"] <= 15 else 0,
                        "movement_type": GENTE.movimento(p["src_mov"]),
                        "movement_range_x": 0, "movement_range_y": 0,
                        "trainer_type": "TRAINER_TYPE_NONE",
                        "trainer_sight_or_berry_tree_id": "0",
                        "script": a["rot"], "flag": "0",
                    },
                    "tile_provado": ("andavel, com vizinho andavel de onde "
                                     "encarar, e fora de tile de warp"
                                     if ok_tile else porque_tile),
                    "gfx_da_fonte": p["src_gfx"],
                    "papel_da_fonte": GFX.TABELA.get(p["src_gfx"], (None, None,
                                                                    "?"))[2],
                    "decisao_pendente": decisao,
                    "porque": "objeto da fonte que abre a porta para %s e que o "
                              "G4 nao pos no mapa" % ", ".join(a["destinos"]),
                })
            elif p["balde"] == "D":
                chave = (p["nosso_dir"], p["src_x"], p["src_y"])
                if chave in vistos_coord:
                    continue
                vistos_coord.add(chave)
                # O tile de um GATILHO tem de ser PISAVEL (o jogador anda em
                # cima dele), e a mesma medicao de colisao que o portao do
                # objeto usa serve: `gente_galar.andavel` sobre o `map.bin`.
                # A diferenca e que gatilho PODE cair em tile de warp; o que
                # nao pode e cair em tile que ninguem pisa, porque ai o
                # `coord_event` seria linha morta no `map.json`.
                prova_tile = tile_de_gatilho(p["fonte"], p["nosso_dir"],
                                             p["src_x"], p["src_y"], docs)
                if not prova_tile.startswith("andavel"):
                    raise SystemExit(
                        "coord_event de %s em (%d,%d): %s"
                        % (p["nosso_dir"], p["src_x"], p["src_y"], prova_tile))
                # ONDA 3, FECHAMENTO: gatilho que o fechador JA COLOU sai do
                # pedido, pela mesma lei do balde A (`objeto que ja aponta para
                # o rotulo daqui nao vira pedido`). Sem esta linha o arquivo de
                # pedidos continuava pedindo os 9 `coord_events` depois de eles
                # estarem no `map.json`, e a rodada seguinte os colaria em
                # dobro. A chave e o ROTULO, que e unico por porta.
                cam_g = "%s/data/maps/%s/map.json" % (RAIZ, p["nosso_dir"])
                if cam_g not in docs:
                    docs[cam_g] = json.load(open(cam_g))
                if any(c.get("script") == a["rot"]
                       for c in (docs[cam_g].get("coord_events") or [])):
                    continue
                nome_var = "VAR_GALAR_PORTA_%s" % p["fonte"].upper()
                if nome_var not in vars_alocadas:
                    raise SystemExit(
                        "coord_event de %s pediria a var %s, que este lote nao "
                        "alocou em vars.h" % (p["nosso_dir"], nome_var))
                coord.append({
                    "mapa": p["nosso_dir"],
                    "coord_event": {
                        "type": "trigger", "x": p["src_x"], "y": p["src_y"],
                        "elevation": 0,
                        "var": nome_var,
                        "var_value": p["src_valor"],
                        "script": a["rot"],
                    },
                    "tile_provado": prova_tile,
                    "var_da_fonte": "0x%04X" % (p["src_var"] or 0),
                    "porque": "gatilho da fonte que abre a porta para %s. A var "
                              "e NOSSA (a da fonte e so procedencia): gatilho e "
                              "evento novo, e quem escolhe o endereco e este "
                              "gerador." % ", ".join(a["destinos"]),
                })
    escritas = [a for a in aceitas if a["acao"] == "escrita"]
    return {
        "gerado_por": "dev_scripts/portas_script_galar.py",
        "para": "o fechador da onda 3 (dono dos map.json)",
        "leia_antes": (
            "Este lote NAO edita map.json. Cada item abaixo esta no formato "
            "exato do repo. `script_de_objeto` reponta o campo `script`: quando "
            "`era` vale \"0\" o objeto estava mudo, e quando `era` traz um "
            "rotulo o dono dele RESPEITA `GalarPorta_` "
            "(objetos_galar.MANDAM_MAIS, a lista unica que objetos_galar.py, "
            "fala_galar.py e, desde esta onda, treinadores_galar.py consultam "
            "antes de escrever). `object_events` e `coord_events` sao eventos "
            "NOVOS, e entram no FIM da lista (a save guarda indice de "
            "object_event; ver ESTADO, 'Compatibilidade de save')."),
        "object_events": obj,
        "coord_events": coord,
        "script_de_objeto": script,
        "rotulos_escritos": [
            {"rotulo": a["rot"], "origem": a["origem_dir"], "ptr": a["ptr"],
             "destinos": a["destinos"], "tomado_de": a.get("tomado_de"),
             "guardas_de_motor_soltas": [
                 "%s 0x%X (%s)" % (n, v, q)
                 for n, v, q in a.get("guardas_soltas") or []],
             "batalhas_escritas": [
                 "treinador %d da fonte -> %s" % (f, c)
                 for f, c in a.get("batalhas_escritas") or []],
             "batalhas_sem_treinador": [
                 "treinador %d da fonte, tipo %d" % (f, t)
                 for f, t in a.get("batalhas_sem_treinador") or []]}
            for a in sorted(escritas, key=lambda z: z["rot"])],
        "ja_escritas_por_outro_gerador": [
            {"rotulo": a["rot"], "origem": a["origem_dir"],
             "destinos": a["destinos"]}
            for a in sorted([a for a in aceitas if a["acao"] == "ja_escrita"],
                            key=lambda z: z["rot"])],
        "nao_feitas": [
            {"motivo": r["motivo"], "balde": r["balde"],
             "origem": r["origem_dir"], "ptr": r["ptr"],
             "destinos": ["%s (%s,%s)" % (g["destino"], g["wx"], g["wy"])
                          for g in r["linhas"]]}
            for r in sorted(recusas, key=lambda z: (z["motivo"],
                                                    z["origem_dir"], z["ptr"]))],
    }


def falta_traduzir(sem_traducao):
    """O texto da fonte que NINGUEM verteu ainda, para o Gui decidir.

    MESMO formato de `dev_scripts/onda2_lote_i_falta_traduzir.json` (`_leia` no
    topo, lista `distintos`, cada item com `pt` e `chaves`), para quem for
    traduzir nao ter de aprender um segundo arquivo. As tres chaves a mais por
    item (`en` vazio, `destinos` e `porta_saiu_sem_a_fala`) sao acrescimo, nao
    troca: dizem o que a porta perde enquanto o texto nao volta.

    Este lote NAO traduz texto novo. Quando a porta passa em tudo o mais, a
    fala sai do script (`porta_saiu_sem_a_fala` true) e a porta entra; quando o
    que falta derruba a cena inteira, ela fica de fora e o item aparece aqui
    com `porta_saiu_sem_a_fala` false.
    """
    por_pt = collections.OrderedDict()
    for e in sorted(sem_traducao, key=lambda z: (z["pt"], z.get("rotulo") or "")):
        d = por_pt.setdefault(e["pt"], {"pt": e["pt"], "en": "", "chaves": [],
                                        "destinos": [],
                                        "porta_saiu_sem_a_fala": False})
        chave = "%s (%s, %s)" % (e.get("rotulo") or "?", e["origem"], e["ptr"])
        if chave not in d["chaves"]:
            d["chaves"].append(chave)
        for x in e["destinos"]:
            if x not in d["destinos"]:
                d["destinos"].append(x)
        d["porta_saiu_sem_a_fala"] |= bool(e.get("saiu_do_script"))
    return {
        "_leia": (
            "textos da fonte sem traducao escrita em "
            "dev_scripts/traducao_galar.json (por rotulo) nem em "
            "dev_scripts/resgate_galar_texto.json (por texto), achados pelas "
            "PORTAS de script de Galar (onda 3, lote M). Preencher `en` pelo "
            "GLOSSARIO-GALAR.md, no maximo 208 px por linha "
            "(dev_scripts/texto_placas_sinnoh.py), com os tokens de controle na "
            "mesma ordem e quantidade do `pt`; depois mover o par para "
            "dev_scripts/resgate_galar_texto.json e rodar "
            "dev_scripts/portas_script_galar.py --aplicar de novo. "
            "`porta_saiu_sem_a_fala` true quer dizer que a porta ESTA no jogo e "
            "so a caixa de texto ficou de fora; false quer dizer que a porta "
            "inteira esta esperando este texto."),
        "distintos": [por_pt[k] for k in sorted(por_pt)],
    }


def aplica(aceitas, recusas, vars_alocadas, flags_alocadas, lista, gravar,
           sem_traducao=()):
    corpo = corpo_inc(aceitas)
    peds = pedidos_de_mapjson(aceitas, lista, recusas, vars_alocadas)
    mudou = collections.Counter()
    if gravar:
        antes = open(INC).read() if os.path.exists(INC) else None
        if antes != corpo:
            open(INC, "w").write(corpo)
            mudou["inc"] += 1
        fonte_s = open(EVENT_S).read()
        if LINHA_INCLUDE not in fonte_s:
            open(EVENT_S, "w").write(fonte_s.rstrip("\n") + "\n"
                                     + LINHA_INCLUDE + "\n")
            mudou["event_scripts.s"] += 1
        texto = open(VARS_H).read()
        novo = C3.poe_bloco(texto, MARCA_VAR_INI, MARCA_VAR_FIM,
                            bloco_vars(vars_alocadas))
        if novo != texto:
            open(VARS_H, "w").write(novo)
            mudou["vars.h"] += 1
        texto = open(FLAGS_H).read()
        novo = C3.poe_bloco(texto, MARCA_FLAG_INI, MARCA_FLAG_FIM,
                            bloco_flags(flags_alocadas))
        if novo != texto:
            open(FLAGS_H, "w").write(novo)
            mudou["flags.h"] += 1
        for caminho, conteudo in (
                (PEDIDOS, json.dumps(peds, indent=1, ensure_ascii=False) + "\n"),
                (FALTA_TRADUZIR,
                 json.dumps(falta_traduzir(sem_traducao), indent=1,
                            ensure_ascii=False) + "\n")):
            velho = open(caminho).read() if os.path.exists(caminho) else None
            if velho != conteudo:
                open(caminho, "w").write(conteudo)
                mudou[os.path.basename(caminho)] += 1
    return peds, mudou


# ------------------------------------------------------------- relatorio ----

def relata(aceitas, recusas, lista, vars_alocadas, flags_alocadas, peds,
           sem_traducao=()):
    baldes = collections.Counter(p["balde"] for p in lista)
    print("portas de script de origem viva: %d, em %d destinos"
          % (len(lista), len({p["destino"] for p in lista})))
    print("por balde: " + ", ".join("%s=%d" % (k, baldes[k])
                                    for k in sorted(baldes)))
    feitas = collections.Counter()
    for a in aceitas:
        for p in a["linhas"]:
            feitas[(p["balde"], a["acao"])] += 1
    print("\nportas resolvidas:")
    for (b, acao), n in sorted(feitas.items()):
        print("  balde %s  %-12s %d" % (b, acao, n))
    n_rec = sum(r["portas"] for r in recusas)
    print("portas NAO resolvidas: %d (em %d scripts)" % (n_rec, len(recusas)))
    por_motivo = collections.Counter()
    for r in recusas:
        por_motivo[r["motivo"]] += r["portas"]
    for m, n in por_motivo.most_common(12):
        print("  %3d  %s" % (n, m))
    dest_ok = set()
    for a in aceitas:
        dest_ok.update(a["destinos"])
    print("\ndestinos cobertos por porta escrita ou ja escrita: %d de %d"
          % (len(dest_ok), len({p["destino"] for p in lista})))
    print("pedidos de map.json: %d object_events, %d coord_events, "
          "%d repontes de script, em %d mapas"
          % (len(peds["object_events"]), len(peds["coord_events"]),
             len(peds["script_de_objeto"]),
             len({p["mapa"] for k in ("object_events", "coord_events",
                                      "script_de_objeto") for p in peds[k]})))
    print("vars alocadas: %d  %s"
          % (len(vars_alocadas),
             ", ".join("%s=0x%04X" % (n, v)
                       for n, v in sorted(vars_alocadas.items())) or "-"))
    print("flags alocadas: %d  %s"
          % (len(flags_alocadas),
             ", ".join("%s=0x%04X" % (n, v)
                       for n, v in sorted(flags_alocadas.items())) or "-"))
    guardas = collections.Counter()
    bat_ok, bat_fora = 0, 0
    tomados = collections.Counter()
    for a in aceitas:
        for n, v, q in a.get("guardas_soltas") or []:
            guardas["%s 0x%X (%s)" % (n, v, q)] += 1
        bat_ok += len(a.get("batalhas_escritas") or [])
        bat_fora += len(a.get("batalhas_sem_treinador") or [])
        if a.get("tomado_de"):
            tomados[a["tomado_de"].split("_")[0] + "_"] += 1
    print("\nguardas de motor do demake soltas: %d" % sum(guardas.values()))
    for g, n in sorted(guardas.items()):
        print("  %3d  %s" % (n, g))
    print("batalhas transcritas pelo molde sem intro: %d; batalhas sem "
          "treinador nosso (so o warp): %d" % (bat_ok, bat_fora))
    print("objetos tomados por precedencia: %s"
          % (", ".join("%s%d" % (k, v) for k, v in sorted(tomados.items()))
             or "-"))
    cortadas = {e["pt"] for e in sem_traducao if e.get("saiu_do_script")}
    print("falas sem traducao: %d distintas, %d cortadas de porta escrita"
          % (len({e["pt"] for e in sem_traducao}), len(cortadas)))


# -------------------------------------------------------------- autoteste ---

def demo():
    falhou = []

    def confere(o_que, deu, esperado):
        ok = deu == esperado
        print("  %-64s %s  (%s)" % (o_que, "OK" if ok else "CAIU", deu))
        if not ok:
            falhou.append(o_que)

    lista = portas()
    confere("as portas medidas sao as %d do lote AB" % ESPERADO["portas"],
            len(lista), ESPERADO["portas"])
    confere("elas caem em %d destinos orfaos" % ESPERADO["destinos"],
            len({p["destino"] for p in lista}), ESPERADO["destinos"])
    confere("todo warp e por COORDENADA (indice 255), nunca por indice",
            sorted({p["warp_de_chegada"] for p in lista}), [255])
    confere("nenhuma porta ficou sem x/y",
            [p["ptr"] for p in lista if p["wx"] is None], [])

    lista, _docs = classifica(lista)
    baldes = collections.Counter(p["balde"] for p in lista)
    for b in "ABCD":
        confere("balde %s tem %d portas" % (b, ESPERADO[b]), baldes[b],
                ESPERADO[b])
    confere("nenhuma porta ficou fora dos quatro baldes", baldes["?"], 0)

    # A de-para de objeto e pela COORDENADA, e a prova disso e o grafico: se o
    # casamento fosse por ordem, o sprite do nosso objeto nao teria por que
    # bater com o papel que a tabela de gfx da a fonte.
    ruins = [p for p in lista
             if p["balde"] in ("B", "C") and p.get("nosso_gfx")
             and GFX.traduz(p["src_gfx"])[0]
             and GFX.traduz(p["src_gfx"])[0] != p["nosso_gfx"]]
    confere("em B e C o sprite nosso bate com o gfx da fonte", ruins, [])

    (aceitas, recusas, docs, vars_alocadas, flags_alocadas, lista2,
     sem_traducao) = plano()
    confere("toda porta esta ou aceita ou recusada, sem sumir",
            sum(a["portas"] for a in aceitas) + sum(r["portas"] for r in recusas),
            ESPERADO["portas"])
    confere("todo rotulo escrito comeca com " + PREFIXO,
            sorted({a["rot"][:len(PREFIXO)] for a in aceitas
                    if a["acao"] == "escrita"}) or [PREFIXO], [PREFIXO])
    escritas = [a for a in aceitas if a["acao"] == "escrita"]
    confere("toda porta escrita emitiu warp",
            [a["rot"] for a in escritas
             if not any("\twarp" in l for l in a["corpo"])], [])
    # A porta entrega TODOS os destinos que promete. Sem esta linha,
    # `GalarPorta_G13M07_o0` passava anunciando oito destinos e emitindo um so
    # (a cirurgia de guarda tinha comido os outros sete `warp`).
    confere("toda porta escrita emite warp para TODOS os destinos que promete",
            [a["rot"] for a in escritas
             if sorted({(g["destino"], str(g["wx"]), str(g["wy"]))
                        for g in a["linhas"]}
                       - set(re.findall(
                           r"^\twarp(?:silent)?\s+(MAP_[A-Z0-9_]+),\s*(\d+),"
                           r"\s*(\d+)", "\n".join(a["corpo"]), re.M)))], [])
    confere("nenhum destino escrito e mapa sem saida",
            [a["rot"] for a in escritas
             if any(saidas_do_destino(
                 next(g["destino_dir"] for g in a["linhas"]
                      if g["destino"] == d), docs,
                 next(g["destino_fonte"] for g in a["linhas"]
                      if g["destino"] == d)) == (0, 0, 0)
                 for d in a["destinos"])], [])
    # Idempotencia: gerar duas vezes tem que dar o MESMO texto.
    confere("o corpo do .inc e estavel entre duas geracoes",
            corpo_inc(aceitas) == corpo_inc(aceitas), True)
    peds = pedidos_de_mapjson(aceitas, lista2, recusas, vars_alocadas)
    # A regua da onda 2 dizia "nenhum reponte mexe em rotulo NENHUM". Na onda 3
    # o reponte por PRECEDENCIA passou a ser o trabalho principal do lote, e a
    # regua muda de lugar sem afrouxar: o reponte so pode cair em rotulo de
    # gerador que RESPEITA `GalarPorta_`. Se cair em outro, a proxima geracao
    # daquele gerador apaga a porta em silencio, que e o defeito que esta linha
    # existe para pegar.
    confere("nenhum pedido de reponte mexe em rotulo de dono que nao respeita "
            + PREFIXO,
            sorted({p["era"] for p in peds["script_de_objeto"]
                    if p["era"] not in ("0", "")
                    and not p["era"].startswith(TOMAVEIS)}), [])
    # A LISTA E UMA SO, e esta linha e a prova disso: se alguem acrescentar um
    # prefixo aqui e esquecer `objetos_galar.MANDAM_MAIS`, os geradores de la
    # continuam escrevendo por cima e a porta se apaga na geracao seguinte.
    # `GalarObj_`/`GalarFala_`/`GalarFalaI_` sao do proprio `objetos_galar.py` e
    # do `fala_galar.py`, que consultam a lista; `GalarTrn_` passou a consultar
    # nesta onda; `GalarPorta_` e o nosso.
    confere("GalarPorta_ esta na lista unica de precedencia de objetos_galar",
            PREFIXO in OBJ.MANDAM_MAIS, True)
    confere("treinadores_galar.py consulta a mesma lista antes de escrever "
            "`script`",
            "manda_mais" in open(f"{RAIZ}/dev_scripts/treinadores_galar.py").read(),
            True)
    confere("todo reponte que toma rotulo de FALA nasceu do MESMO ponteiro",
            [p["era"] for p in peds["script_de_objeto"]
             if p["era"].startswith(TOMAVEIS_DE_FALA)
             and ponteiro_da_fala(p["era"]) != int(
                 next(a["ptr"] for a in escritas if a["rot"] == p["valor"]), 16)],
            [])
    # IDEMPOTENCIA DE VERDADE: um objeto que JA aponta para o rotulo certo nao
    # vira pedido. Sem isto a segunda rodada pediria de novo o que o fechador ja
    # colou, e a fila mentiria para cima.
    confere("objeto que ja aponta para o rotulo daqui nao vira pedido",
            [p["mapa"] for p in peds["script_de_objeto"]
             if p["era"] == p["valor"]], [])
    # A ARMADILHA QUE APAGA O `.inc`: se o gerador deixar de reconhecer o
    # proprio prefixo, toda porta ja colada volta como "rotulo de outro dono", o
    # corpo sai vazio e o `--aplicar` apaga o arquivo calado.
    confere("nenhuma porta foi recusada por ter o rotulo DESTE gerador",
            [r["ptr"] for r in recusas if PREFIXO in r["motivo"]
             and "nao respeita" in r["motivo"]], [])
    # A prova de verdade nao e "os rotulos de ontem continuam la": e que NENHUM
    # `map.json` fique chamando um rotulo que o `.inc` desta rodada nao define.
    # E o que o link acusaria, tarde, e o que a passada de ontem quase causou.
    chamados = set()
    for caminho in glob.glob(f"{RAIZ}/data/maps/*/map.json"):
        d = json.load(open(caminho))
        for ev in (d.get("object_events") or []) + (d.get("coord_events") or []) \
                + (d.get("bg_events") or []):
            alvo = str(ev.get("script") or "")
            if alvo.startswith(PREFIXO):
                chamados.add(alvo)
    definidos = set(re.findall(r"^(%s\w+)::" % PREFIXO, corpo_inc(aceitas), re.M))
    confere("nenhum map.json chama rotulo daqui que o .inc nao define",
            sorted(chamados - definidos), [])
    # VAR: o endereco tem de ser livre DE VERDADE, e nao so livre para a regua
    # do c3, que tira os blocos de Galar do header antes de medir.
    confere("nenhuma var alocada colide com outro bloco de Galar",
            sorted(set(vars_alocadas.values()) & vars_ja_de_galar()), [])
    confere("todo coord_event pede var que este lote alocou",
            sorted({p["coord_event"]["var"] for p in peds["coord_events"]}
                   - set(vars_alocadas)), [])
    confere("todo coord_event dispara com a var em 0 (var nova nasce em 0)",
            [p["mapa"] for p in peds["coord_events"]
             if p["coord_event"]["var_value"] != 0], [])
    # BATALHA: so pelo molde SEM INTRO, que e o que a C28 deixa passar em
    # entrada sem objeto, e sempre com o portao de "ja venci" na frente.
    corpo_bat = corpo_inc(aceitas)
    confere("nenhuma batalha escrita usa molde COM intro",
            re.findall(r"^\ttrainerbattle(?!_no_intro)\w*", corpo_bat, re.M), [])
    # So linha de CODIGO (comeca com tabulacao e nao e comentario): o cabecalho
    # do arquivo cita o nome do molde em prosa, e sem este filtro o autoteste
    # reprovava a propria documentacao.
    linhas_bat = corpo_bat.split("\n")
    confere("toda linha de trainerbattle_no_intro tem goto_if_defeated antes",
            [i for i, l in enumerate(linhas_bat)
             if l.startswith("\ttrainerbattle_no_intro")
             and not any(x.startswith("\tgoto_if_defeated")
                         for x in linhas_bat[max(0, i - 3):i])], [])
    confere("todo pedido aponta para rotulo que o .inc escreve",
            sorted(({p["valor"] for p in peds["script_de_objeto"]}
                    | {p["object_event"]["script"] for p in peds["object_events"]}
                    | {p["coord_event"]["script"] for p in peds["coord_events"]})
                   - {a["rot"] for a in escritas}), [])
    confere("todo pedido de objeto novo tem sprite ou decisao pendente escrita",
            [p["mapa"] for p in peds["object_events"]
             if not p["object_event"]["graphics_id"] and not p["decisao_pendente"]],
            [])
    # IDIOMA e LARGURA, as duas reguas do qa/checa_texto.py, medidas no texto
    # que ESTE gerador emite e nao no arquivo do disco: assim o autoteste
    # reprova antes de o `.inc` sair, e nao depois.
    corpo = corpo_inc(aceitas)
    pt, largo = [], []
    for m in re.finditer(r'\.string "(.*)\$"', corpo):
        bruto = m.group(1)
        limpo = re.sub(r"\{[^}]*\}", " ", bruto)
        limpo = limpo.replace("\\n", " ").replace("\\l", " ").replace("\\p", " ")
        if len(QA_TEXTO.PT_MARCADORES.findall(limpo)) >= 1:
            pt.append(bruto[:40])
        for caixa in bruto.split("\\p"):
            for linha in re.split(r"\\[nl]", caixa):
                if REQUEBRA.largura_px(linha) > REQUEBRA.LARGURA_CAIXA:
                    largo.append(linha[:40])
    confere("zero portugues no texto que este lote escreve", pt, [])
    confere("zero linha acima de %d px" % REQUEBRA.LARGURA_CAIXA, largo, [])
    confere("a traducao nao inventou nem perdeu token de controle",
            [k for k, v in TRADUCAO.items()
             if sorted(re.findall(r"\\[nlp]|\{[^}]*\}", k)) and
             sorted(re.findall(r"\{[^}]*\}", k)) != sorted(re.findall(r"\{[^}]*\}", v))],
            [])
    # Fala sem traducao NAO some: ela sai listada, e a porta espera.
    confere("toda porta recusada por falta de traducao esta na lista de espera",
            sorted({r["ptr"] for r in recusas
                    if "sem traducao" in r["motivo"]}
                   - {e["ptr"] for e in sem_traducao}), [])
    print("\n%s" % ("autoteste: tudo de pe" if not falhou
                    else "autoteste: %d caiu" % len(falhou)))
    return 1 if falhou else 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seco", action="store_true", help="nao grava nada")
    ap.add_argument("--aplicar", action="store_true", help="grava os arquivos")
    ap.add_argument("--demo", action="store_true", help="autoteste")
    args = ap.parse_args()
    if args.demo:
        return demo()
    (aceitas, recusas, docs, vars_alocadas, flags_alocadas, lista,
     sem_traducao) = plano()
    peds, mudou = aplica(aceitas, recusas, vars_alocadas, flags_alocadas, lista,
                         gravar=args.aplicar and not args.seco,
                         sem_traducao=sem_traducao)
    relata(aceitas, recusas, lista, vars_alocadas, flags_alocadas, peds,
           sem_traducao)
    if args.aplicar and not args.seco:
        print("\ngravado: %s" % (", ".join("%s(%d)" % (k, v)
                                           for k, v in sorted(mudou.items()))
                                 or "nada mudou"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
