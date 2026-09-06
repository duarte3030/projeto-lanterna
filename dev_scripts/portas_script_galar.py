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
PEDIDOS = f"{RAIZ}/dev_scripts/onda2_lote_f_pedidos_mapjson.json"
PENDENTES = f"{RAIZ}/dev_scripts/onda2_lote_f_pendentes_estaticos.txt"
TOCADOS = f"{RAIZ}/dev_scripts/onda2_lote_f_tocados.txt"
VARS_H = f"{RAIZ}/include/constants/vars.h"
FLAGS_H = f"{RAIZ}/include/constants/flags.h"

MARCA_VAR_INI = ("// >>> Fase de conteudo de Galar, onda 2 lote F: vars de porta "
                 "de script (dev_scripts/portas_script_galar.py) >>>")
MARCA_VAR_FIM = "// <<< Fase de conteudo de Galar, onda 2 lote F <<<"
MARCA_FLAG_INI = ("// >>> Fase de conteudo de Galar, onda 2 lote F: flags de porta "
                  "de script (dev_scripts/portas_script_galar.py) >>>")
MARCA_FLAG_FIM = "// <<< Fase de conteudo de Galar, onda 2 lote F, flags <<<"

# Faixa de flag EXCLUSIVA deste lote, dada pela condutora na abertura da onda 2.
PRIMEIRA_FLAG = 0x2200
ULTIMA_FLAG = 0x227F

# Os totais que a medicao de 07/09/2026 deu. O --demo reprova se mudarem sem
# que alguem venha aqui mudar o numero de proposito: total que anda calado e
# como a onda descobre tarde que a fonte ou a arvore mexeu.
ESPERADO = {"portas": 77, "destinos": 40, "A": 22, "B": 22, "C": 16, "D": 17}

PREFIXO = "GalarPorta_"

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
        """O texto da fonte, JA EM INGLES e requebrado contra 208 px.

        Galar fala INGLES (decisao 32 do Gui, PRD-CARTUCHO-2.md), e o texto do
        demake e portugues. O `aplica_traducao_galar.py` traduz DEPOIS, casando
        por rotulo contra `traducao_galar.json`, e rotulo novo deste lote nao
        esta la: sair daqui em portugues poria um T07 novo no `checa_texto` e
        so seria consertado quando alguem lembrasse de reabrir o JSON. Entao a
        traducao sai daqui mesmo, na hora, pela tabela TRADUCAO abaixo.

        Texto em portugues SEM entrada na tabela recusa a cena inteira, em vez
        de escorregar para o `.inc`: e a mesma regra de tudo o mais aqui.
        """
        linhas = super().texto(ptr, rotulo)
        bruto = re.match(r'\t\.string "(.*)\$"$', linhas[1]).group(1)
        en = TRADUCAO.get(bruto)
        if en is None:
            limpo = re.sub(r"\{[^}]*\}", " ", bruto)
            limpo = limpo.replace("\\n", " ").replace("\\l", " ").replace("\\p", " ")
            if len(QA_TEXTO.PT_MARCADORES.findall(limpo)) >= 1:
                raise C3.Recusa("texto em portugues sem traducao na tabela do "
                                "lote F: %r" % bruto[:60])
            en = bruto
        self.traduzidos[bruto] = en
        return ["%s:" % rotulo, '\t.string "%s$"' % REQUEBRA.requebra(en)]


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
    for m in re.finditer(r"#define\s+(FLAG_GALAR_ESCONDE_([0-9A-F]+))\s",
                         open(f"{RAIZ}/include/constants/flags.h").read()):
        escondidas_com_nome[int(m.group(2), 16)] = m.group(1)

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
        bs, falha = C3.blocos(rom, tab, int(ptr, 16) - C3.BASE)
        if falha:
            continue
        acende = {a[0] for b in bs for n, a in b.ins if n == "setflag" and a}
        le = {a[0] for b in bs for n, a in b.ins if n == "checkflag" and a}
        locais = sorted((acende & le) - set(esconde_glob))
        if locais:
            flags_locais[(chave, ptr)] = locais

    # Var por MAPA de origem, como no c3. So gasta endereco quem entrar.
    livres = C3.vars_livres()
    aceitas, recusas = [], []
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
        if p0["balde"] == "C" and all(ja_transcrita(g, ja) for g in grupo):
            base["ja_feita"] = True
            aceitas.append(dict(base, corpo=None, extras=None,
                                rot=p0["nosso_script"], acao="ja_escrita"))
            continue
        if p0["balde"] == "C":
            nega("rotulo de outro dono (%s) em arquivo REGERADO; vai como "
                 "pendencia" % (p0["nosso_script"] or "?"))
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
        if p0["balde"] == "D":
            ruins = sorted({g["src_var"] for g in grupo
                            if not (0x4000 <= (g["src_var"] or 0) <= 0x40FF)})
            if ruins:
                nega("var de gatilho da fonte fora da faixa de var do FireRed "
                     "(%s): o que a fonte le ali e indefinido"
                     % ", ".join("0x%04X" % v for v in ruins))
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
        bs, falha = C3.blocos(rom, tab, int(ptr, 16) - C3.BASE)
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
        rot = rotulo(p0)
        try:
            # `cena()` recebe OFFSET, nao ponteiro: `blocos()` indexa `rom[off]`
            # direto. Passar o ponteiro de ROM (0x08...) nao levanta erro
            # nenhum: `blocos` descarta o offset por estar fora da ROM, devolve
            # zero blocos, e a cena sai como "no-op depois da traducao". Foi
            # assim que 39 portas apareceram como no-op na primeira medicao.
            corpo, usadas = t.cena(int(ptr, 16) - AND.ROM_BASE, rot)
        except C3.Recusa as e:
            nega(str(e))
            continue
        if not any(("\twarp " in l or "\twarpsilent " in l) for l in corpo):
            nega("a traducao passou mas nao emitiu warp nenhum")
            continue
        aceitas.append(dict(base, corpo=corpo, rot=rot, acao="escrita",
                            usadas=dict(usadas), vars_citadas=sorted(nomes_var),
                            flags_locais=list(flags_locais.get((chave, ptr),
                                                              ()))))

    # Enderecos de var: so para quem entrou, na ordem da chave da FONTE.
    usa_var = sorted({a["chave"] for a in aceitas if a.get("vars_citadas")})
    vars_alocadas = {}
    for i, chave in enumerate(usa_var):
        if i >= len(livres):
            break
        vars_alocadas[nome_var_de[chave]] = livres[i]

    # Enderecos de FLAG, da faixa exclusiva deste lote, na ordem (chave da
    # fonte, flag). So gasta quem entrou, como no c3 e no c4a.
    quer = sorted({(a["chave"], f) for a in aceitas
                   for f in a.get("flags_locais") or ()})
    flags_alocadas = {}
    for i, (chave, f) in enumerate(quer):
        end = PRIMEIRA_FLAG + i
        if end > ULTIMA_FLAG:
            raise SystemExit("faixa de flag do lote F (0x%04X-0x%04X) esgotada"
                             % (PRIMEIRA_FLAG, ULTIMA_FLAG))
        flags_alocadas[nome_flag_local(chave, f)] = end
    return aceitas, recusas, docs, vars_alocadas, flags_alocadas, lista


# --------------------------------------------------------------- escrita ----

CABECALHO = """@ Portas de SCRIPT dos orfaos de Galar (onda 2, lote F).
@ Gerado por dev_scripts/portas_script_galar.py; NAO editar a mao.
@
@ Cada rotulo aqui e a transcricao FIEL de um script do demake que contem
@ `warp` e cai num mapa que hoje nenhum caminho alcanca. O tradutor e o mesmo
@ do c3 (cenas_galar.py) e do c4a (objetos_galar.py); o que ele recusa nao
@ aparece aqui, aparece no relatorio com motivo.
@
@ PRECEDENCIA: o rotulo daqui comeca com `GalarPorta_`. Ele so e pendurado em
@ objeto que estava MUDO (`script` valia "0") ou em objeto/gatilho NOVO, e
@ nunca por cima de `GalarObj_`, `GalarFala_`, `GalarTrn_`, `GalarSelvagem_`
@ ou `GalarEstatico_`. Quem escrever campo `script` de map.json de Galar
@ depois desta onda precisa respeitar `GalarPorta_` do mesmo jeito que ja
@ respeita `GalarObj_`, senao a porta se apaga calada.
"""


def corpo_inc(aceitas):
    partes = [CABECALHO]
    escritas = [a for a in aceitas if a["acao"] == "escrita"]
    for a in sorted(escritas, key=lambda z: (z["chave"], z["rot"])):
        partes.append("\n@ ---- %s (%s), %s -> %s ----\n"
                      % (a["origem_dir"], a["chave"], a["ptr"],
                         ", ".join(a["destinos"])))
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


def pedidos_de_mapjson(aceitas, lista):
    """Os pedidos que o FECHADOR cola nos map.json. Este lote nao os aplica."""
    obj, coord, script = [], [], []
    por_rot = {a["rot"]: a for a in aceitas if a["acao"] == "escrita"}
    vistos_obj, vistos_coord = set(), set()
    for a in aceitas:
        if a["acao"] != "escrita":
            continue
        for p in a["linhas"]:
            if p["balde"] == "B":
                chave = (p["nosso_dir"], p["nosso_local_id"])
                if chave in vistos_obj:
                    continue
                vistos_obj.add(chave)
                script.append({
                    "mapa": p["nosso_dir"],
                    "indice_do_object_event": p["nosso_local_id"] - 1,
                    "x": p["src_x"], "y": p["src_y"],
                    "campo": "script", "valor": a["rot"],
                    "era": p["nosso_script"],
                    "porque": "objeto mudo que na fonte abre a porta para %s"
                              % ", ".join(a["destinos"]),
                })
            elif p["balde"] == "A":
                chave = (p["nosso_dir"], p["src_x"], p["src_y"])
                if chave in vistos_obj:
                    continue
                vistos_obj.add(chave)
                sprite, decisao = sprite_do_gfx(p["src_gfx"])
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
                coord.append({
                    "mapa": p["nosso_dir"],
                    "coord_event": {
                        "type": "trigger", "x": p["src_x"], "y": p["src_y"],
                        "elevation": 0,
                        "var": "VAR_GALAR_PORTA_%s" % p["fonte"].upper(),
                        "var_value": p["src_valor"],
                        "script": a["rot"],
                    },
                    "var_da_fonte": "0x%04X" % (p["src_var"] or 0),
                    "porque": "gatilho da fonte que abre a porta para %s"
                              % ", ".join(a["destinos"]),
                })
    return {
        "gerado_por": "dev_scripts/portas_script_galar.py",
        "para": "o fechador da onda 2 (dono dos map.json)",
        "leia_antes": (
            "Este lote NAO edita map.json. Cada item abaixo esta no formato "
            "exato do repo. `script_de_objeto` reponta o campo `script` de um "
            "objeto que estava MUDO; `object_events` e `coord_events` sao "
            "eventos NOVOS, e entram no FIM da lista (a save guarda indice de "
            "object_event; ver ESTADO, 'Compatibilidade de save')."),
        "object_events": obj,
        "coord_events": coord,
        "script_de_objeto": script,
    }


def texto_pendentes(recusas, aceitas):
    linhas = [
        "# Onda 2, lote F: portas de script que este lote NAO escreveu, e por que.",
        "# Gerado por dev_scripts/portas_script_galar.py; NAO editar a mao.",
        "#",
        "# O nome do arquivo vem da abertura da onda, que esperava achar as",
        "# portas do balde C em `galar_estaticos.inc` (rotulos GalarSelvagem_* e",
        "# GalarEstatico_*). MEDIDO em 07/09/2026, isso NAO acontece: nenhuma das",
        "# 77 portas cai em GalarSelvagem_*, GalarEstatico_* nem GalarFala_*. O",
        "# balde C real e GalarObj_* (ja escritas pelo c4a, com warp e tudo) e",
        "# GalarTrn_*, que mora em data/scripts/galar_treinadores.inc.",
        "#",
        "# Por que GalarTrn_* nao entra aqui: aquele arquivo e REGERADO por",
        "# dev_scripts/treinadores_galar.py, e o gerador de la escreve o campo",
        "# `script` do map.json SEM regra de precedencia (linha 1149). Escrever",
        "# no .inc ou repontar o objeto seria desfeito calado na proxima",
        "# geracao, que e exatamente o conflito que o git nao marca.",
        "",
    ]
    ja = [a for a in aceitas if a["acao"] == "ja_escrita"]
    if ja:
        linhas.append("## JA FEITAS pelo c4a (nada a fazer), %d entradas" % len(ja))
        for a in sorted(ja, key=lambda z: z["rot"]):
            linhas.append("  %-34s %-26s -> %s"
                          % (a["rot"], a["origem_dir"], ", ".join(a["destinos"])))
        linhas.append("")
    # As do balde C que moram em arquivo de OUTRO dono ganham secao propria,
    # com o alvo do warp escrito por extenso: quem pegar so precisa acrescentar
    # essas tres linhas ao molde do gerador de treinador, depois do
    # `trainerbattle`, e a porta fica de pe.
    trn = [r for r in recusas if "arquivo REGERADO" in r["motivo"]]
    if trn:
        linhas.append("## PARA O DONO DE dev_scripts/treinadores_galar.py, "
                      "%d portas" % sum(r["portas"] for r in trn))
        linhas.append("#")
        linhas.append("# O objeto de origem ja tem rotulo GalarTrn_*; na fonte o")
        linhas.append("# MESMO script faz a batalha e o warp. Acrescentar ao fim")
        linhas.append("# do molde de treinador, depois do msgbox de derrota:")
        linhas.append("#     warp <MAPA>, <x>, <y>")
        linhas.append("#     waitstate")
        linhas.append("# Os tres numeros de cada linha estao abaixo, lidos do")
        linhas.append("# bytecode em 07/09/2026 (comando 0x39, argumento `map` +")
        linhas.append("# indice de chegada 255 + x/y).")
        for r in sorted(trn, key=lambda z: z["origem_dir"]):
            for g in r["linhas"]:
                linhas.append("  %-26s %-11s %-34s warp %s, %d, %d"
                              % (r["origem_dir"], r["ptr"],
                                 g.get("nosso_script") or "?",
                                 g["destino"], g["wx"], g["wy"]))
        linhas.append("")

    por_motivo = collections.defaultdict(list)
    for r in recusas:
        por_motivo[r["motivo"]].append(r)
    linhas.append("## RECUSADAS, %d entradas de script, %d portas"
                  % (len(recusas), sum(r["portas"] for r in recusas)))
    for motivo, rs in sorted(por_motivo.items(),
                             key=lambda z: (-sum(r["portas"] for r in z[1]), z[0])):
        linhas.append("")
        linhas.append("### %s  (%d portas, %d scripts)"
                      % (motivo, sum(r["portas"] for r in rs), len(rs)))
        for r in sorted(rs, key=lambda z: (z["origem_dir"], z["ptr"])):
            alvos = ", ".join("%s (%d,%d)" % (g["destino"], g["wx"], g["wy"])
                              for g in r["linhas"])
            linhas.append("  balde %s  %-26s %-11s -> %s"
                          % (r["balde"], r["origem_dir"], r["ptr"], alvos))
    return "\n".join(linhas) + "\n"


def texto_tocados(aceitas, pedidos):
    linhas = ["# Onda 2, lote F: mapas e rotulos tocados.",
              "# Gerado por dev_scripts/portas_script_galar.py.",
              "",
              "## Rotulos escritos em data/scripts/galar_portas_script.inc"]
    for a in sorted([a for a in aceitas if a["acao"] == "escrita"],
                    key=lambda z: z["rot"]):
        linhas.append("  %-38s %-26s -> %s"
                      % (a["rot"], a["origem_dir"], ", ".join(a["destinos"])))
    for nome, chave in (("object_events", "object_events"),
                        ("coord_events", "coord_events"),
                        ("script_de_objeto", "script_de_objeto")):
        linhas.append("")
        linhas.append("## Pedidos de map.json: %s (%d)"
                      % (nome, len(pedidos[chave])))
        for p in pedidos[chave]:
            linhas.append("  %s" % p["mapa"])
    return "\n".join(linhas) + "\n"


def aplica(aceitas, recusas, vars_alocadas, flags_alocadas, lista, gravar):
    corpo = corpo_inc(aceitas)
    peds = pedidos_de_mapjson(aceitas, lista)
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
        for caminho, conteudo in ((PEDIDOS, json.dumps(peds, indent=1,
                                                       ensure_ascii=False) + "\n"),
                                  (PENDENTES, texto_pendentes(recusas, aceitas)),
                                  (TOCADOS, texto_tocados(aceitas, peds))):
            velho = open(caminho).read() if os.path.exists(caminho) else None
            if velho != conteudo:
                open(caminho, "w").write(conteudo)
                mudou[os.path.basename(caminho)] += 1
    return peds, mudou


# ------------------------------------------------------------- relatorio ----

def relata(aceitas, recusas, lista, vars_alocadas, flags_alocadas, peds):
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


# -------------------------------------------------------------- autoteste ---

def demo():
    falhou = []

    def confere(o_que, deu, esperado):
        ok = deu == esperado
        print("  %-64s %s  (%s)" % (o_que, "OK" if ok else "CAIU", deu))
        if not ok:
            falhou.append(o_que)

    lista = portas()
    confere("as portas medidas sao as 77 do lote AB", len(lista),
            ESPERADO["portas"])
    confere("elas caem em 40 destinos orfaos",
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

    aceitas, recusas, docs, vars_alocadas, flags_alocadas, lista2 = plano()
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
    peds = pedidos_de_mapjson(aceitas, lista2)
    confere("nenhum pedido de reponte mexe em rotulo de outro dono",
            [p for p in peds["script_de_objeto"] if p["era"] not in ("0", "")],
            [])
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
    aceitas, recusas, docs, vars_alocadas, flags_alocadas, lista = plano()
    peds, mudou = aplica(aceitas, recusas, vars_alocadas, flags_alocadas, lista,
                         gravar=args.aplicar and not args.seco)
    relata(aceitas, recusas, lista, vars_alocadas, flags_alocadas, peds)
    if args.aplicar and not args.seco:
        print("\ngravado: %s" % (", ".join("%s(%d)" % (k, v)
                                           for k, v in sorted(mudou.items()))
                                 or "nada mudou"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
