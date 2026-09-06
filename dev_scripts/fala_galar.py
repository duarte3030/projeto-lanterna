#!/usr/bin/env python3
"""FASE DE CONTEUDO DE GALAR, baldes (a) fala e (b) flag: le o roteiro da FONTE.

    python3 dev_scripts/fala_galar.py             # so a tabela dos quatro baldes
    python3 dev_scripts/fala_galar.py --gravar    # + dev_scripts/galar_roteiros.json
    python3 dev_scripts/fala_galar.py --aplicar   # + escreve mapa, script e flags
    python3 dev_scripts/fala_galar.py --demo      # autoteste com mutacao plantada

## Por que este arquivo existe

A obra G0..G5 trouxe Galar inteira como GEOMETRIA e deixou 3.257 linhas de
cobranca em `dev_scripts/fila_galar.json`, cada uma com um PONTEIRO para o
script da fonte e nada mais. Ponteiro nao e classificacao: sem abrir o
bytecode, ninguem sabe se aquele NPC diz uma frase (custo zero de estado), da
um item (custo de uma flag) ou move meio mapa (custo de var e cena). Este
arquivo abre o bytecode.

O desmontador nao tem tabela de opcode digitada a mao: ele PARSEIA
`fontes-mapas/pokefirered/asm/macros/event.inc`, que e a fonte de verdade do
motor de script do FireRed, e monta {opcode: (nome, tamanhos)}. Licao 4.11 do
ESTADO: teste (e ferramenta) que guarda copia de um fato envelhece calado.

## Os quatro baldes, e a regra de cada um

    a_fala      o script inteiro, seguindo TODOS os ramos, usa so comando sem
                estado (travar, encarar, falar, soltar, terminar) e tem UM
                texto. Vira `msgbox TEXTO, MSGBOX_NPC` (ou MSGBOX_SIGN).
    b_flag      acrescenta a isso flag PERSISTENTE e/ou a entrega padrao de
                item (`callstd STD_OBTAIN_ITEM/STD_FIND_ITEM`). Custa uma flag
                do pool novo por linha.
    c_var_cena  usa var salva, movimento, cena, batalha selvagem, `special`,
                warp, loja: precisa da maquina de vars de Galar, que ainda nao
                foi desenhada. NAO se executa aqui.
    d_treinador `trainerbattle` no bytecode ou `trainer_type` sadio na fonte.
                Fase F congelada pelo Gui (ESTADO 0.h): mede-se, nao se executa.

DECODIFICACAO INCOMPLETA CAI EM c, NUNCA EM a OU b. Se qualquer ramo do script
bate em opcode que o FireRed nao tem (o demake reaproveita espaco de dado como
se fosse codigo em alguns ponteiros), a linha e `indeciso` e fica no balde c.
Emitir fala a partir de um script que nao foi lido inteiro seria inventar.

## O texto vem da fonte, e quando nao vem o NPC continua mudo

Texto com `FD` (marcador de buffer: nome do jogador, do item, do Pokemon) ou
`FC` (codigo de controle) NAO entra: o buffer que o enche e comando de estado
que este balde nao executa, entao a frase sairia com um buraco. Essas linhas
ficam pendentes, e o NPC continua mudo. Nunca se inventa fala.

## Ordem de uso das ferramentas de Galar, que e a lei LEVA_DONA

    python3 dev_scripts/gente_galar.py  --gravar   # flags dos itens escondidos
    python3 dev_scripts/mundo_galar.py  --gravar   # mapas e scripts.inc
    python3 dev_scripts/fala_galar.py   --aplicar  # ESTE, por ultimo
    python3 dev_scripts/fila_galar.py   --gravar   # a fila reconta a verdade

PRECEDENCIA: rotulo `GalarObj_*` (bloco c4a, dev_scripts/objetos_galar.py) VENCE
`GalarFala_*`. Onde a cena inteira do objeto foi portada, ela ja contem a fala
que este balde daria, e por isso `aplica()` nao sobrescreve campo `script` que ja
comece com `GalarObj_`. A mesma regra esta escrita no cabecalho de la.

`mundo_galar.py` reescreve `data/maps/Galar_*/{map.json,scripts.inc}` inteiros.
Por isso este arquivo NAO escreve dentro de `scripts.inc`: a fala mora em
`data/scripts/galar_fala.inc`, arquivo so dele, e no `map.json` ele toca apenas
os campos `script` e `flag` dos object events que ele mesmo reconheceu, mais os
bg events de placa que ele acrescenta. Rodar `mundo_galar.py` de novo apaga
esses campos; rodar este de novo os repoe, e o `--conferir` mostra a diferenca.
"""
import argparse
import collections
import glob
import json
import os
import re
import struct

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.dirname(RAIZ)
PKFR = os.path.join(FONTES, "fontes-mapas/pokefirered")
ROM_FONTE = os.path.join(FONTES,
                         "fontes-mapas/galar-swsh/ultimate-plus-v1.2.1.2.gba")
FILA = f"{RAIZ}/dev_scripts/fila_galar.json"
CENSO_GENTE = f"{RAIZ}/dev_scripts/galar_gente.json"
ROTEIROS = f"{RAIZ}/dev_scripts/galar_roteiros.json"
INC = f"{RAIZ}/data/scripts/galar_fala.inc"
FLAGS_H = f"{RAIZ}/include/constants/flags.h"
EVENT_S = f"{RAIZ}/data/event_scripts.s"

BASE = 0x08000000
MARCA_INI = "// >>> Fase de conteudo de Galar, baldes a e b (dev_scripts/fala_galar.py) >>>"
MARCA_FIM = "// <<< Fase de conteudo de Galar, baldes a e b <<<"

# Reserva pedida pela condutora: 150 flags no minimo tem que sobrar do pool
# livre para a maquina de vars/cena que ainda nao foi desenhada.
RESERVA_DE_CENA = 150

# =========================================================================== #
# O PIPELINE NASCE EM INGLES (onda 3, lote L1, 08/09/2026)
#
# ARMADILHA QUE ISTO FECHA, e ela foi MEDIDA pelo lote I da onda 2: ate aqui os
# tres geradores de Galar (`fala_galar.py`, `cenas_galar.py`,
# `objetos_galar.py`) escreviam o texto da fonte em PORTUGUES, e o ingles so
# entrava depois, numa segunda passada de `dev_scripts/aplica_traducao_galar.py`
# por ROTULO. Quem rodasse o modo padrao e parasse ali devolvia Galar inteira ao
# portugues, e a regua T07 de `dev_scripts/qa/checa_texto.py` reprovava. Pior:
# todo bloco NOVO nascia em portugues e sem entrada no de-para, de modo que
# nenhuma cena nova podia entrar sem quebrar o portao. Foi por isso que o lote I
# nao reabriu nenhuma das recusas do c4a.
#
# A REGRA AGORA, e ela vale para os tres geradores:
#
#   1. bloco cujo ROTULO esta em `dev_scripts/traducao_galar.json` sai com o
#      `en` de la (e o de-para por rotulo continua sendo a fonte de verdade do
#      julgamento de traducao);
#   2. rotulo NOVO cujo TEXTO da fonte esta em
#      `dev_scripts/resgate_galar_texto.json` (chave `pt`) sai com o `en` de la;
#   3. texto que nenhum dos dois cobre e que a REGUA DO PORTAO nao chama de
#      portugues sai como esta (e o caso de "...", de nome proprio e dos blocos
#      que a fonte ja tem em ingles);
#   4. texto que nenhum dos dois cobre e que a REGUA DO PORTAO chama de
#      portugues NAO E ESCRITO. Ele entra em `dev_scripts/onda3_falta_traduzir.
#      json`, a linha da fila fica `adiada` com motivo "texto sem traducao", e o
#      bloco (na fala) ou a cena inteira (na cena) fica de fora.
#
# POR QUE A REGUA DO PORTAO, E NAO UMA MAIS DURA. O gate tem de ser o MESMO
# criterio do `checa_texto.T07`. Uma regua propria e mais dura aqui deixaria o
# gerador recusar bloco que o portao aceita (e o portao e quem decide se a
# rodada passa); uma mais frouxa deixaria passar o que o portao reprova. Duas
# reguas para o mesmo fato e o defeito que a licao 4.11 do ESTADO nomeia.
# Consequencia MEDIDA e escrita aqui para ninguem a descobrir de novo: 83 blocos
# de `galar_fala.inc`, 35 de `galar_objetos.inc` e 1 de `galar_cenas.inc` caem
# na regra 3 sem estar em de-para nenhum, e alguns deles sao portugues curto que
# a regua do portao nao acusa (ela pede DOIS marcadores). Eles continuam na
# arvore exatamente como estavam; o relatorio de cada gerador os conta na linha
# `neutro sem de-para`.
#
# O UNICO HERDADO. `GalarFala_G09M10_o14_Text` e o bloco em portugues que o T07
# de Galar acusa (o defeito de charmap deixado a vista de proposito pela onda
# 2). Ele cai na regra 4 e seria apagado da arvore por este pipeline, o que
# mudaria a arvore sem ninguem ter pedido e faria o T07 de Galar cair de 1 para
# 0, escondendo um defeito conhecido. Ele fica, pela lista abaixo, e aparece na
# lista de falta traduzir como qualquer outro.
# =========================================================================== #
TRADUCAO_JSON = f"{RAIZ}/dev_scripts/traducao_galar.json"
RESGATE_JSON = f"{RAIZ}/dev_scripts/resgate_galar_texto.json"
FALTA_JSON = f"{RAIZ}/dev_scripts/onda3_falta_traduzir.json"

HERDADOS_SEM_TRADUCAO = frozenset(("GalarFala_G09M10_o14_Text",))

# Motivo que a fila recebe quando o bloco fica de fora por falta de traducao.
# E CONSTANTE porque os tres geradores o escrevem e a fila tem de saber
# reconhecer o que ela mesma ja escreveu; sem isso a fila muda a cada passada.
MOTIVO_SEM_TRADUCAO = (
    "texto sem traducao: a fonte tem fala e nem "
    "dev_scripts/traducao_galar.json (por rotulo) nem "
    "dev_scripts/resgate_galar_texto.json (por texto) tem o ingles dela. "
    "O texto pendente esta em dev_scripts/onda3_falta_traduzir.json.")


def _regua_do_portao():
    """O modulo `dev_scripts/qa/checa_texto.py`, importado, nunca copiado."""
    import importlib
    import sys as _sys
    qa = os.path.join(RAIZ, "dev_scripts", "qa")
    if qa not in _sys.path:
        _sys.path.insert(0, qa)
    return importlib.import_module("checa_texto")


def idioma_do_texto(texto):
    """"pt", "en" ou "neutro" pelo MESMO criterio do T07 do portao."""
    ct = _regua_do_portao()
    limpo = re.sub(r"\{[^}]*\}", " ", texto or "")
    for c in ("\\n", "\\l", "\\p"):
        limpo = limpo.replace(c, " ")
    en = len(ct.EN_MARCADORES.findall(limpo))
    pt = len(ct.PT_MARCADORES.findall(limpo))
    if en >= 2 and en > pt:
        return "en"
    if pt >= 2 and pt > en:
        return "pt"
    return "neutro"


def so_requebrou(pt, en):
    """O de-para nao traduziu nada: as MESMAS palavras, so com outra quebra.

    Acontece porque o demake deixou pedaco de texto do FireRed em ingles, e o
    de-para guardou esse pedaco como se fosse traducao (12 entradas do de-para
    por texto tem `pt` igual a `en`, e mais quatro so mudam onde cai o `\\n`).
    Nesses casos o texto que ja esta na arvore fica como esta: requebrar bloco
    que ninguem traduziu mudaria arquivo sem mudar jogo, e a requebra por PIXEL
    e obra propria, com medicao propria. O bloco original ja passou pelo teto de
    208 px do portao na rodada em que entrou.
    """
    def limpo(t):
        for c in ("\\n", "\\l", "\\p"):
            t = t.replace(c, " ")
        return " ".join(t.split())
    return limpo(pt) == limpo(en)


def linhas_de_texto(rotulo, corpo, dois_pontos=":", indent="\t", quebra=True):
    """Bloco `.string` de um texto, do jeito EXATO do aplicador.

    A quebra em varias `.string` e a mesma de
    `aplica_traducao_galar.escreve_bloco`, e nao uma segunda implementacao dela:
    o `en` do de-para ja vem requebrado por PIXEL, com `\\n`, `\\l` e `\\p`
    dentro, e cada pedaco tem de virar uma linha. Emitir tudo numa `.string` so
    compila igual, mas daria arquivo diferente do que o aplicador escreveu, e a
    prova de "arvore identica" desta rodada morreria por formatacao.
    """
    if not quebra:
        # Texto que NAO veio do de-para (regra 3 e o herdado da regra 4) nunca
        # passou pelo aplicador: ele esta na arvore numa `.string` so, do jeito
        # que o proprio gerador o escreveu. Requebra-lo aqui mudaria 89 blocos
        # de `galar_fala.inc` que ninguem pediu para mudar. Quebra so o que o
        # de-para ja entregou requebrado por pixel.
        return ["%s%s" % (rotulo, dois_pontos),
                '%s.string "%s$"' % (indent, corpo)]
    partes = re.split(r"(\\[nlp])", corpo)
    linhas, i = [], 0
    while i < len(partes):
        pedaco = partes[i] + (partes[i + 1] if i + 1 < len(partes) else "")
        linhas.append(pedaco)
        i += 2
    if not linhas:
        linhas = [""]
    linhas[-1] += "$"
    return ["%s%s" % (rotulo, dois_pontos)] + [
        '%s.string "%s"' % (indent, l) for l in linhas]


class Traducao:
    """De-para de saida dos tres geradores, e o caderno do que falta.

    Estado de PROCESSO, e por isso e um objeto e nao um dicionario solto: quem
    pergunta tambem registra, e o registro tem de sobreviver a cena inteira ser
    recusada depois (a cena morre, o texto continua faltando).
    """

    def __init__(self, traducao=None, resgate=None):
        self.por_rotulo, self.por_texto = {}, {}
        caminho = traducao if traducao is not None else TRADUCAO_JSON
        if os.path.exists(caminho):
            for e in json.load(open(caminho, encoding="utf-8"))["entradas"]:
                self.por_rotulo[e["rotulo"]] = e["en"]
        caminho = resgate if resgate is not None else RESGATE_JSON
        if os.path.exists(caminho):
            for e in json.load(open(caminho, encoding="utf-8"))["entradas"]:
                self.por_texto.setdefault(e["pt"], e["en"])
        self.faltam = collections.OrderedDict()   # pt -> [chaves]
        # Linha da fila que ESTA rodada conseguiu escrever. Serve so ao caderno
        # de falta: sem ela o arquivo so cresceria, e um texto traduzido depois
        # continuaria cobrado para sempre.
        self.resolvidas = set()
        self.conta = collections.Counter()

    def resolve(self, rotulo, pt, chave=None):
        """(texto a escrever, origem) ou (None, motivo) quando falta traducao.

        `chave` e a linha da fila a que o bloco pertence, e so serve para o
        caderno saber a quem cobrar.
        """
        # `identico` E UM VEREDITO, e nao um detalhe: 12 das 107 entradas do
        # de-para por texto guardam texto que a FONTE ja tem em ingles (sobra do
        # FireRed dentro do demake), com `en` igual ao `pt`. Nesses o de-para nao
        # traduziu nada, e requebrar o bloco mudaria a arvore sem mudar uma
        # letra do jogo. Pior, mudaria de tabela: o rotulo da lista de loja em
        # `objetos_galar.lista_de_loja` e numerado por LINHA ja emitida
        # (`len(self.extras_gancho)`), entao uma `.string` a mais renomeia o
        # `_MartN` seguinte. Medido em 08/09/2026 no `GalarObj_G00M06_o3`:
        # `_Mart2` virava `_Mart3`.
        en = self.por_rotulo.get(rotulo)
        if en is not None:
            self.conta["por rotulo"] += 1
            self.resolvidas.add(chave or rotulo)
            if so_requebrou(pt, en):
                return pt, "identico"
            return en, "rotulo"
        en = self.por_texto.get(pt)
        if en is not None:
            self.conta["por texto"] += 1
            self.resolvidas.add(chave or rotulo)
            if so_requebrou(pt, en):
                return pt, "identico"
            return en, "texto"
        if rotulo in HERDADOS_SEM_TRADUCAO:
            self.conta["herdado"] += 1
            self.anota(pt, chave or rotulo)
            return pt, "herdado"
        if idioma_do_texto(pt) != "pt":
            self.conta["neutro sem de-para"] += 1
            self.resolvidas.add(chave or rotulo)
            return pt, "neutro"
        self.conta["sem traducao"] += 1
        self.anota(pt, chave or rotulo)
        return None, "sem traducao"

    def anota(self, pt, chave):
        self.faltam.setdefault(pt, [])
        if chave not in self.faltam[pt]:
            self.faltam[pt].append(chave)

    def chaves_faltando(self):
        """As linhas da fila que ficaram devendo texto, sem repetir."""
        fora = set()
        for chaves in self.faltam.values():
            fora |= set(chaves)
        return fora

    def corpo_falta(self, de_disco=None):
        """O caderno inteiro: o que ESTA rodada achou, mais o que ja estava.

        UNIAO, e nao substituicao, porque os TRES geradores escrevem no mesmo
        arquivo e cada um so enxerga a sua parte: `fala_galar.py --aplicar`
        rodando depois de `objetos_galar.py --aplicar` apagaria os textos do
        outro se aqui fosse simples troca. Medido em 08/09/2026, e por isso esta
        escrito: o arquivo caiu de 22 textos para 1 na primeira vez.

        Nao vira lixeira: a chave que ESTA rodada conseguiu escrever
        (`resolvidas`) sai do que veio do disco, entao um texto traduzido depois
        deixa de ser cobrado sozinho.
        """
        faltam = collections.OrderedDict()
        if de_disco:
            resolvidas = self.resolvidas - self.chaves_faltando()
            for e in de_disco.get("distintos", []):
                sobra = [c for c in e["chaves"] if c not in resolvidas]
                if sobra:
                    faltam[e["pt"]] = sobra
        for pt, chaves in self.faltam.items():
            juntas = faltam.get(pt, [])
            faltam[pt] = juntas + [c for c in chaves if c not in juntas]
        return json.dumps(
            {"_leia": "textos da fonte sem traducao escrita em "
                      "dev_scripts/traducao_galar.json (por rotulo) nem em "
                      "dev_scripts/resgate_galar_texto.json (por texto). "
                      "Enquanto estiverem aqui o bloco NAO e escrito, e a "
                      "linha da fila fica adiada. Escrito pelos tres geradores "
                      "de Galar (onda 3, lote L1).",
             "distintos": [{"pt": pt, "chaves": sorted(ch)}
                           for pt, ch in sorted(faltam.items())]},
            indent=1, ensure_ascii=False) + "\n"

    def grava_falta(self, gravar, caminho=None):
        """Escreve o caderno. Devolve 1 se o arquivo mudaria, 0 se nao."""
        caminho = caminho or FALTA_JSON
        de_disco = None
        if os.path.exists(caminho):
            de_disco = json.load(open(caminho, encoding="utf-8"))
        corpo = self.corpo_falta(de_disco)
        if os.path.exists(caminho) and open(caminho, encoding="utf-8").read() == corpo:
            return 0
        if gravar:
            open(caminho, "w", encoding="utf-8").write(corpo)
        return 1


def marca_fila_sem_traducao(gravar, chaves=None, fila=None):
    """Deixa `adiada` toda linha cujo bloco ficou de fora por falta de ingles.

    NAO reabre linha `feita` nem `descartada`: `feita` e calculada pela arvore
    (`fila_galar.feitas()`) e `descartada` guarda decisao ja tomada, com motivo
    proprio. O que esta funcao cobre e o caso novo do pipeline em ingles: a
    linha TEM script portavel e o unico impedimento e o texto sem traducao, que
    e decisao de conteudo e nao medicao.

    Idempotente pelo motivo: escrever duas vezes o mesmo texto nao conta
    mudanca, e por isso `MOTIVO_SEM_TRADUCAO` e constante.
    """
    chaves = chaves if chaves is not None else traducao().chaves_faltando()
    caminho = fila or FILA
    doc = json.load(open(caminho, encoding="utf-8"))
    n = 0
    for l in doc["linhas"]:
        if l["chave"] not in chaves:
            continue
        if l.get("status") in ("feita", "descartada"):
            continue
        novo = "adiada", "onda 3, lote L1, 08/09/2026: " + MOTIVO_SEM_TRADUCAO
        if (l.get("status"), l.get("motivo_do_status")) != novo:
            l["status"], l["motivo_do_status"] = novo
            n += 1
    if gravar and n:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return n


def demo_pipeline_ingles():
    """Autoteste comum aos tres geradores: bloco novo sem traducao NAO e escrito.

    Roda contra de-paras de mentira, nunca contra os do repo: o caso tem de
    reprovar quando alguem quebrar a regra, e nao quando alguem traduzir mais um
    texto. As frases de prova sao feitas de MARCADORES da regua T07, e nao de
    fala do demake.
    """
    falhas = []
    t = Traducao(traducao="/nao/existe.json", resgate="/nao/existe.json")
    t.por_rotulo["QA_ComRotulo_Text"] = "Answer by the label."
    t.por_texto["qa aqui uma sua"] = "Answer by the text."

    en, origem = t.resolve("QA_ComRotulo_Text", "qa aqui uma sua", "qa/objeto/0")
    if (en, origem) != ("Answer by the label.", "rotulo"):
        falhas.append("o rotulo tem de vencer o texto: %r" % ((en, origem),))
    en, origem = t.resolve("QA_Novo_Text", "qa aqui uma sua", "qa/objeto/1")
    if (en, origem) != ("Answer by the text.", "texto"):
        falhas.append("rotulo novo tinha de casar pelo texto: %r" % ((en, origem),))
    en, origem = t.resolve("QA_Orfao_Text", "qa aqui uma seu sua", "qa/objeto/2")
    if en is not None or origem != "sem traducao":
        falhas.append("texto em portugues sem de-para NAO podia ser escrito: %r"
                      % ((en, origem),))
    if "qa/objeto/2" not in t.chaves_faltando():
        falhas.append("o bloco sem traducao nao entrou no caderno de falta")
    if t.chaves_faltando() & {"qa/objeto/0", "qa/objeto/1"}:
        falhas.append("bloco COM traducao foi parar no caderno de falta")
    en, origem = t.resolve("QA_Ingles_Text", "Sailor: the ship is here.",
                           "qa/objeto/3")
    if en != "Sailor: the ship is here." or origem != "neutro":
        falhas.append("texto que a regua nao chama de portugues tinha de passar "
                      "como esta: %r" % ((en, origem),))
    en, origem = t.resolve("QA_Rewrap_Text", "One two\\nthree.", "qa/objeto/4")
    t.por_texto["One two\\nthree."] = "One two three."
    en, origem = t.resolve("QA_Rewrap_Text", "One two\\nthree.", "qa/objeto/4")
    if (en, origem) != ("One two\\nthree.", "identico"):
        falhas.append("de-para que so requebra tinha de deixar o texto como "
                      "esta: %r" % ((en, origem),))

    # o caderno so cresce, e a fila recebe o motivo constante
    import tempfile
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                      encoding="utf-8")
    json.dump({"linhas": [
        {"chave": "qa/objeto/2", "status": "pendente", "motivo_do_status": ""},
        {"chave": "qa/objeto/9", "status": "descartada",
         "motivo_do_status": "decisao antiga"}]}, tmp, ensure_ascii=False)
    tmp.close()
    n = marca_fila_sem_traducao(True, t.chaves_faltando(), tmp.name)
    doc = json.load(open(tmp.name, encoding="utf-8"))
    if n != 1 or doc["linhas"][0]["status"] != "adiada":
        falhas.append("a linha sem traducao nao ficou adiada (%d)" % n)
    if doc["linhas"][1]["status"] != "descartada":
        falhas.append("linha descartada foi reaberta pela falta de traducao")
    if marca_fila_sem_traducao(True, t.chaves_faltando(), tmp.name) != 0:
        falhas.append("marca_fila_sem_traducao nao e idempotente")
    os.unlink(tmp.name)
    return falhas


_TRAD = None


def traducao():
    """A instancia unica do de-para de saida, compartilhada pelos geradores.

    UMA so, e de proposito: `objetos_galar.py` importa `cenas_galar.py` e este
    arquivo, e os tres escrevem no MESMO caderno de falta. Duas instancias
    dariam dois cadernos e o segundo apagaria o primeiro.
    """
    global _TRAD
    if _TRAD is None:
        _TRAD = Traducao()
    return _TRAD


def reinicia_traducao(t=None):
    """Troca a instancia unica. So os autotestes chamam."""
    global _TRAD
    _TRAD = t
    return _TRAD


# ---------------------------------------------------------------- opcodes ---
TAM = {".byte": 1, ".2byte": 2, ".4byte": 4}
# Macros auxiliares do FireRed e o tamanho em bytes que cada uma emite.
AUX = {"map": 2, "stringvar": 1, "formatwarp": 7}
# `trainerbattle` (0x5C) tem tamanho por TIPO, e o tipo e o byte seguinte.
# Vem de asm/macros/event.inc, ramo a ramo do `.if \type == ...`.
TRAINERBATTLE = {0: 14, 1: 14, 2: 18, 3: 10, 4: 18, 5: 10, 6: 22, 7: 14,
                 8: 22, 9: 6}


def tabela_de_opcodes(caminho=None):
    """{opcode: (nome, [tamanhos dos argumentos])} lido do event.inc do FireRed.

    Macro com argumento opcional (`.ifb`) fica com o PRIMEIRO ramo: o ramo do
    `.else` e outro opcode (applymovement 0x4F contra applymovement_at 0x50).
    Macro que este parser nao consegue dimensionar entra com tamanho None e o
    desmontador para nela, em vez de chutar e sair andando por cima de dado.
    """
    txt = open(caminho or f"{PKFR}/asm/macros/event.inc").read()
    tab = {}
    for m in re.finditer(r"^\t\.macro\s+(\w+)([^\n]*)\n(.*?)^\t\.endm",
                         txt, re.S | re.M):
        nome, corpo = m.group(1), m.group(3)
        linhas = [l.split("@")[0].strip() for l in corpo.split("\n")]
        linhas = [l for l in linhas if l]
        ramos = [linhas]
        if linhas and linhas[0].startswith(".ifb"):
            # MACRO DE DOIS RAMOS: `.ifb \map` separa `applymovement` (0x4F) de
            # `applymovement_at` (0x50), e o mesmo vale para waitmovement,
            # removeobject e addobject. Ate 22/08/2026 este parser guardava so o
            # PRIMEIRO ramo, e com isso 0x50, 0x52, 0x54 e 0x56 ficavam fora da
            # tabela: script que os usasse virava "opcode indecodificavel" e a
            # cena caia no balde errado. Agora os DOIS ramos entram.
            corte, outro, prof = [], [], 0
            alvo = corte
            for l in linhas[1:]:
                if l.startswith(".if"):
                    prof += 1
                    alvo.append(l)
                elif l.startswith(".endif"):
                    if prof == 0:
                        break
                    prof -= 1
                    alvo.append(l)
                elif l.startswith(".else") and prof == 0:
                    alvo = outro
                else:
                    alvo.append(l)
            ramos = [corte, outro]
        for ramo in ramos:
            if not ramo or not ramo[0].startswith(".byte 0x"):
                continue
            toks = ramo[0].split()
            if len(toks) != 2:
                continue
            op = int(toks[1], 16)
            sufixo = nome if ramo is ramos[0] else nome + "_at"
            tamanhos, ok = [], True
            for l in ramo[1:]:
                p = l.split(None, 1)
                if p[0] in TAM:
                    tamanhos.extend([TAM[p[0]]] *
                                    ((p[1].count(",") + 1) if len(p) > 1 else 1))
                elif p[0] in AUX:
                    tamanhos.append(AUX[p[0]])
                else:
                    ok = False
                    break
            if not ok:
                tab.setdefault(op, (sufixo, None))
                continue
            if op in tab and tab[op][1] is not None:
                continue
            tab[op] = (sufixo, tamanhos)
    return tab


# --------------------------------------------------------------- charmap ----
def charmap(caminho=None):
    """{byte: caractere} do charmap.txt DESTE repo, so as entradas de 1 byte."""
    mapa = {}
    for l in open(caminho or f"{RAIZ}/charmap.txt"):
        l = l.split("@")[0].strip()
        if "=" not in l:
            continue
        esq, dir_ = l.split("=", 1)
        by = dir_.split()
        if len(by) != 1:
            continue
        try:
            b = int(by[0], 16)
        except ValueError:
            continue
        esq = esq.strip()
        if esq.startswith("'") and esq.endswith("'") and len(esq) >= 3:
            mapa.setdefault(b, esq[1:-1])
    return mapa


CONTROLE = {0xFE: "\\n", 0xFA: "\\l", 0xFB: "\\p"}


# --------------------------------------------------------------- vocabulario -
# Comando que NAO deixa marca no save nem no mapa. Balde (a) e exatamente isto.
SEM_ESTADO = {
    "nop", "nop1", "end", "return", "goto", "call", "lock", "lockall",
    "faceplayer", "release", "releaseall", "loadword", "loadbyte", "callstd",
    "message", "waitmessage", "waitbuttonpress", "closemessage", "delay",
    "playse", "waitse", "playfanfare", "waitfanfare", "textcolor",
    "waitmoncry", "playmoncry", "showmonpic", "hidemonpic", "erasebox",
    "gotostd", "callstd_if", "gotostd_if", "goto_if", "call_if",
    "compare_var_to_value", "compare_var_to_var",
}
# Acrescenta o balde (b): flag persistente e a entrega padrao de item.
SO_FLAG = {"setflag", "clearflag", "checkflag", "removeobject", "addobject",
           "hideobject", "showobject", "setorcopyvar", "copyvarifnotzero",
           "checkitemspace", "additem", "bufferitemname", "checkitem"}
# Batalha de treinador: balde (d), Fase F congelada.
TREINADOR = {"trainerbattle"}

STD_ITEM = (0, 1)          # STD_OBTAIN_ITEM, STD_FIND_ITEM
STD_MSG = (2, 3, 4, 5, 6)  # MSGBOX_NPC, SIGN, DEFAULT, YESNO, AUTOCLOSE
# STD_OBTAIN_DECORATION/PUT_ITEM_AWAY/RECEIVED_ITEM: mexem na mochila por
# caminho que este balde nao porta. Caem em c de proposito.
STD_OUTRO = (7, 8, 9)

# Faixas do FireRed. Var >= 0x8000 e especial (EWRAM, nao salva); 0x4000-0x400F
# e temporaria de mapa. Flag < 0x20 e temporaria; >= 0x4000 e especial.
def var_salva(v):
    return 0x4010 <= v < 0x4000 + 0x100 or 0x4000 <= v < 0x8000 and v > 0x400F


def flag_salva(f):
    return 0x20 <= f < 0x4000


class Roteiro:
    """O que a leitura do bytecode achou a partir de um ponteiro da fonte."""

    def __init__(self):
        self.ops = collections.Counter()
        self.textos = []            # [(offset, tipo de callstd)]
        self.flags = []
        self.vars = []
        self.itens = []             # [(item, quantidade)]
        self.falha = None
        self.blocos = 0
        self.moldura = set()   # lock/lockall/faceplayer/release/releaseall


def desmonta(rom, tab, inicio, maxi=400):
    r = Roteiro()
    vistos, pilha = set(), [inicio]
    while pilha:
        off = pilha.pop()
        if off in vistos or not (0 <= off < len(rom)):
            continue
        vistos.add(off)
        r.blocos += 1
        palavra, ultimo_var = {}, None
        for _ in range(maxi):
            if off + 1 > len(rom):
                r.falha = r.falha or "fim de rom"
                break
            op = rom[off]
            if op not in tab:
                r.falha = r.falha or "opcode 0x%02X" % op
                break
            nome, tams = tab[op]
            if nome == "trainerbattle":
                t = rom[off + 1]
                if t not in TRAINERBATTLE:
                    r.falha = r.falha or "trainerbattle tipo %d" % t
                    break
                r.ops[nome] += 1
                off += TRAINERBATTLE[t]
                continue
            if tams is None:
                r.falha = r.falha or ("macro variavel " + nome)
                break
            args, p = [], off + 1
            for s in tams:
                if p + s > len(rom):
                    args = None
                    break
                args.append(int.from_bytes(rom[p:p + s], "little"))
                p += s
            if args is None:
                r.falha = r.falha or "fim de rom"
                break
            r.ops[nome] += 1
            if nome in ("lock", "lockall", "faceplayer", "release", "releaseall"):
                r.moldura.add(nome)
            if nome == "loadword" and len(args) == 2:
                palavra[args[0]] = args[1]
            elif nome in ("setflag", "clearflag", "checkflag") and args:
                r.flags.append(args[0])
            elif nome in ("setvar", "addvar", "subvar", "copyvar",
                          "setorcopyvar", "copyvarifnotzero") and args:
                r.vars.append(args[0])
                if args[0] in (0x8000, 0x8001) and len(args) > 1:
                    ultimo_var = (args[0], args[1])
                    if args[0] == 0x8000:
                        palavra["item"] = args[1]
                    else:
                        palavra["qtd"] = args[1]
            elif nome == "callstd" and args:
                if args[0] in STD_OUTRO:
                    r.ops["callstd_de_mochila"] += 1
                elif args[0] in STD_ITEM:
                    r.itens.append((palavra.get("item", 0),
                                    palavra.get("qtd", 1)))
                elif args[0] in STD_MSG and 0 in palavra:
                    alvo = palavra[0]
                    if BASE <= alvo < BASE + len(rom):
                        r.textos.append((alvo - BASE, args[0]))
            elif nome in ("message", "vmessage") and args:
                if BASE <= args[0] < BASE + len(rom):
                    r.textos.append((args[0] - BASE, 4))
            if nome == "goto":
                if BASE <= args[0] < BASE + len(rom):
                    pilha.append(args[0] - BASE)
                break
            if nome in ("call", "goto_if", "call_if"):
                alvo = args[-1]
                if BASE <= alvo < BASE + len(rom):
                    pilha.append(alvo - BASE)
            if nome in ("end", "return"):
                break
            off = p
        else:
            r.falha = r.falha or "script longo demais"
        del ultimo_var
    return r


def tabela_de_map_script(rom, off, maxi=16):
    """[(tipo, offset do script)] da tabela de map script do FireRed.

    A LICAO desta rodada: `map_script_ptr` do de-para NAO aponta para bytecode,
    aponta para a tabela `.byte type / .4byte script` terminada por type 0
    (asm/macros/map.inc, `map_script`). Desmontar a partir dali le a tabela como
    se fosse codigo: o primeiro byte 3 (ON_FRAME_TABLE) vira `return`, e o
    censo sai limpo e errado. Os 256 map_script da fila caem todos no balde c
    por isto, nao por medida de estado.
    """
    fora = []
    for i in range(maxi):
        p = off + i * 5
        if p + 5 > len(rom):
            break
        tipo = rom[p]
        if tipo == 0:
            break
        ptr = int.from_bytes(rom[p + 1:p + 5], "little")
        fora.append((tipo, ptr - BASE if BASE <= ptr < BASE + len(rom) else None))
    return fora


# Marcador 0xFD (placeholder) que ATRAVESSA sem buffer, porque quem o preenche e
# o motor e nao o script: `{PLAYER}` e o nome do jogador e `{RIVAL}` o do rival, e
# os dois bytes sao IDENTICOS no charmap do FireRed e no nosso (FD 01 e FD 06,
# conferido nos dois arquivos em 22/08/2026). Os outros (`{STR_VAR_1}` a
# `{STR_VAR_3}`, FD 02 a FD 04) continuam RECUSANDO a frase, e de proposito: quem
# os enche e `buffer*`, comando de estado, e sem ele a frase sai com um buraco.
PLACEHOLDER_SEM_BUFFER = {0x01: "{PLAYER}", 0x06: "{RIVAL}"}
# Codigo de controle 0xFC. `COLOR` (FC 01, com um byte de cor) e o unico que
# aparece nas frases de Galar, 312 vezes, e ele ATRAVESSA pelo nome, nao e
# descartado: o nosso charmap tem `COLOR` no MESMO byte (FC 01) e os mesmos
# nomes de cor nos mesmos valores, entao `{COLOR DARK_GRAY}` assembla FC 01 02,
# igual ao byte da fonte. Isso importa mais do que parece: o `--demo` daqui
# confere a volta BYTE A BYTE contra a ROM da fonte, e codigo descartado nao
# volta. Os valores medidos nas frases de Galar sao 2, 4, 5, 6 e 8. Qualquer
# outro codigo 0xFC continua recusando a frase, porque o tamanho do argumento
# dele nao esta medido aqui e adivinhar comeria letra.
COR_DO_BYTE = {0x00: "TRANSPARENT", 0x01: "WHITE", 0x02: "DARK_GRAY",
               0x03: "LIGHT_GRAY", 0x04: "RED", 0x05: "LIGHT_RED",
               0x06: "GREEN", 0x07: "LIGHT_GREEN", 0x08: "BLUE",
               0x09: "LIGHT_BLUE"}


def texto(rom, cmap, off, limite=1000):
    """(texto decodificado, motivo de recusa ou None)."""
    saida = []
    i = 0
    while i < limite:
        if off + i >= len(rom):
            return "", "texto sem fim"
        b = rom[off + i]
        if b == 0xFF:
            return "".join(saida), None
        if b == 0xFD:
            if off + i + 1 >= len(rom):
                return "", "texto sem fim"
            arg = rom[off + i + 1]
            nome = PLACEHOLDER_SEM_BUFFER.get(arg)
            if nome is None:
                return "", ("texto com marcador 0xFD %02X (buffer/controle)"
                            % arg)
            saida.append(nome)
            i += 2
            continue
        if b == 0xFC:
            if off + i + 2 >= len(rom):
                return "", "texto sem fim"
            arg, cor = rom[off + i + 1], rom[off + i + 2]
            if arg != 0x01 or cor not in COR_DO_BYTE:
                return "", ("texto com marcador 0xFC %02X (buffer/controle)"
                            % arg)
            saida.append("{COLOR %s}" % COR_DO_BYTE[cor])
            i += 3
            continue
        if b in CONTROLE:
            saida.append(CONTROLE[b])
            i += 1
            continue
        c = cmap.get(b)
        if c is None:
            return "", "byte 0x%02X fora do charmap" % b
        saida.append(c)
        i += 1
    return "", "texto sem fim"


def classifica(linha, r, textos_ok):
    """(balde, motivo). A ordem importa: d ganha de c, c ganha de b, b de a."""
    ops = set(r.ops)
    if ops & TREINADOR or linha.get("trainer_type_fonte", 0):
        return "d_treinador", "trainerbattle no bytecode" if ops & TREINADOR \
            else "trainer_type %d na fonte" % linha["trainer_type_fonte"]
    if r.falha:
        return "c_var_cena", "decodificacao incompleta: " + r.falha
    fora = ops - SEM_ESTADO - SO_FLAG
    if fora:
        return "c_var_cena", "comando de estado: " + ",".join(sorted(fora)[:4])
    if any(v not in (0x8000, 0x8001) and not (0x8000 <= v <= 0x800F)
           for v in r.vars):
        return "c_var_cena", "escreve var salva"
    if any(not flag_salva(f) for f in r.flags):
        return "c_var_cena", "mexe em flag especial/temporaria"
    if r.itens:
        # Bola de item: `finditem`/`giveitem` com item literal. Sem item
        # literal (VAR_0x8000 vindo de copyvar) nao da para escrever a linha.
        if any(i for i, _ in r.itens) and len(r.itens) == 1:
            return "b_flag", "entrega de item padrao"
        return "c_var_cena", "item vindo de var, nao de literal"
    if not textos_ok:
        return "c_var_cena", "sem texto aproveitavel"
    if len(textos_ok) != 1:
        return "c_var_cena", ("%d textos, os baldes a e b so escrevem um"
                              % len(textos_ok))
    if ops & SO_FLAG:
        return "b_flag", "uma fala atras de flag"
    return "a_fala", "so fala"


# -------------------------------------------------------------- varredura ---
def carrega():
    rom = open(ROM_FONTE, "rb").read()
    tab = tabela_de_opcodes()
    cmap = charmap()
    fila = json.load(open(FILA))["linhas"]
    return rom, tab, cmap, fila


def varre(rom, tab, cmap, fila):
    saida = []
    for l in fila:
        p = l.get("ponteiro_fonte")
        if l["tipo"] == "map_script" and p:
            tab_ms = tabela_de_map_script(rom, int(p, 16))
            saida.append(dict(
                l, balde="c_var_cena",
                motivo_balde="tabela de map script (%s): cena, precisa de var"
                             % ",".join(str(t) for t, _ in tab_ms) or "vazia",
                tipos_map_script=[t for t, _ in tab_ms],
                texto=None, tipo_msgbox=None, item=0, item_qtd=0, n_flags=0,
                bytes_texto=0))
            continue
        if not p:
            saida.append(dict(l, balde="c_var_cena",
                              motivo_balde="porta morta, e pendencia de mapa",
                              texto=None, bytes_texto=0))
            continue
        r = desmonta(rom, tab, int(p, 16))
        textos, recusa = [], None
        vistos = set()
        for off, tipo in r.textos:
            if off in vistos:
                continue
            vistos.add(off)
            t, motivo = texto(rom, cmap, off)
            if motivo:
                recusa = recusa or motivo
                continue
            textos.append((t, tipo))
        balde, motivo = classifica(l, r, textos)
        if balde in ("a_fala", "b_flag") and recusa:
            balde, motivo = "c_var_cena", recusa
        saida.append(dict(
            l, balde=balde, motivo_balde=motivo,
            texto=textos[0][0] if textos else None,
            tipo_msgbox=textos[0][1] if textos else None,
            item=r.itens[0][0] if r.itens else 0,
            item_qtd=r.itens[0][1] if r.itens else 0,
            n_flags=len(r.flags),
            moldura=sorted(r.moldura),
            bytes_texto=sum(len(t.encode()) for t, _ in textos)))
    return saida


def tabela(linhas):
    por = collections.defaultdict(collections.Counter)
    for l in linhas:
        por[l["balde"]][l["tipo"]] += 1
        por[l["balde"]]["_total"] += 1
    return por


def imprime(linhas):
    por = tabela(linhas)
    tipos = ["script_objeto", "placa", "map_script", "porta_morta"]
    print("%-14s %8s  %s" % ("balde", "total",
                             "  ".join("%14s" % t for t in tipos)))
    for b in ("a_fala", "b_flag", "c_var_cena", "d_treinador"):
        c = por[b]
        print("%-14s %8d  %s" % (b, c["_total"],
                                 "  ".join("%14d" % c[t] for t in tipos)))
    print("%-14s %8d" % ("TOTAL", len(linhas)))
    ind = [l for l in linhas
           if l["motivo_balde"].startswith("decodificacao incompleta")]
    print("\ndentro de c_var_cena: %d indecisos (bytecode nao lido inteiro)"
          % len(ind))
    ab = [l for l in linhas if l["balde"] in ("a_fala", "b_flag")]
    print("texto dos baldes a+b: %d bytes crus em %d linhas"
          % (sum(l["bytes_texto"] for l in ab), len(ab)))
    print("flags que o balde b consome: %d"
          % sum(1 for l in linhas if l["balde"] == "b_flag"))
    mot = collections.Counter(l["motivo_balde"].split(":")[0]
                              for l in linhas if l["balde"] == "c_var_cena")
    print("\nmotivos de c_var_cena:")
    for m, c in mot.most_common(12):
        print("  %5d  %s" % (c, m))


# ------------------------------------------------------------------ plano ---
TIPO_MSGBOX = {2: "MSGBOX_NPC", 3: "MSGBOX_SIGN", 4: "MSGBOX_DEFAULT",
               5: "MSGBOX_YESNO", 6: "MSGBOX_AUTOCLOSE"}
# Primeira flag da faixa de Galar ainda livre. 0x1C00-0x1C20 sao os itens
# escondidos do G4 e 0x1CFF e a FLAG_GALAR_QA_ANDAR (dona anotada em flags.h).
PRIMEIRA_FLAG_BOLA = 0x1C21
ULTIMA_FLAG_BOLA = 0x1CFE


def _gente():
    import gente_galar
    return gente_galar


def rotulo(chave, l):
    """Rotulo estavel: sai da chave da FONTE, nunca do nosso nome de mapa.

    O G3 renomeia 140 dos 438 mapas (ESTADO 0.f). Rotulo com nome nosso muda de
    nome sozinho na proxima renomeacao, e o `.inc` inteiro vira diff.
    """
    k = chave.upper()
    if l["tipo"] == "placa":
        return "GalarFala_%s_bg%d" % (k, int(l["chave"].rsplit("/", 1)[1]))
    return "GalarFala_%s_o%d" % (k, int(l["chave"].rsplit("/", 1)[1]))


def plano(linhas):
    """(falas, placas, bolas, recusados). So o que da para executar HOJE."""
    G = _gente()
    por_chave, de_para = G.carrega()
    itens_fr = G.itens_da_fonte()
    nossos = G.nossos_itens()
    falas, placas, bolas, recusa = [], [], [], []

    def nega(l, motivo):
        recusa.append({"chave": l["chave"], "balde": l["balde"], "motivo": motivo})

    for l in linhas:
        chave = l["mapa_fonte"]
        dp = de_para.get(chave)
        if dp is None:
            nega(l, "mapa da fonte nao esta no de-para do G3")
            continue
        if l["balde"] == "a_fala":
            # A TRADUCAO ENTRA AQUI, e nao depois (onda 3, lote L1). O bloco de
            # texto so existe se houver ingles para ele: sem isso o `.inc`
            # nasceria em portugues e o `script` do map.json apontaria para um
            # rotulo que o portao T07 reprova. Ver o cabecalho do de-para de
            # saida no alto deste arquivo.
            if l["tipo"] == "script_objeto":
                if not l["no_mapa"]:
                    nega(l, "NPC nao entrou no mapa no G4")
                    continue
                r = rotulo(chave, l)
                en, _origem = traducao().resolve("%s_Text" % r, l["texto"],
                                                 l["chave"])
                if en is None:
                    nega(l, MOTIVO_SEM_TRADUCAO)
                    continue
                falas.append(dict(l, nome=dp["nome"], rotulo=r, texto_en=en,
                                  do_de_para=_origem in ("rotulo", "texto")))
            elif l["tipo"] == "placa":
                r = rotulo(chave, l)
                en, _origem = traducao().resolve("%s_Text" % r, l["texto"],
                                                 l["chave"])
                if en is None:
                    nega(l, MOTIVO_SEM_TRADUCAO)
                    continue
                placas.append(dict(l, nome=dp["nome"], rotulo=r, texto_en=en,
                                   do_de_para=_origem in ("rotulo", "texto")))
        elif l["balde"] == "b_flag":
            if not l["item"]:
                nega(l, "balde b sem item literal: e fala atras de flag, fica")
                continue
            if l["no_mapa"]:
                nega(l, "objeto ja entrou como NPC mudo; dar finditem o apagaria")
                continue
            nome_fr = itens_fr.get(l["item"])
            if nome_fr is None or nome_fr not in nossos:
                nega(l, "item %d da fonte sem equivalente no nosso items.h"
                        % l["item"])
                continue
            j = int(l["chave"].rsplit("/", 1)[1])
            bruto = dict(por_chave[chave]["objetos"]).get(j)
            if bruto is None:
                nega(l, "objeto foi para a sujeira do G0")
                continue
            x, y = bruto["x"], bruto["y"]
            if not G.andavel(chave, dp["w"], dp["h"], x, y):
                nega(l, "bola em tile nao andavel: o jogador nunca a alcanca")
                continue
            if (x, y) in G.warps_limpos(chave):
                nega(l, "bola em cima de warp: trancaria a porta")
                continue
            if G.tiles_de_cura().get(dp["mapa"]) == (x, y):
                nega(l, "bola em cima do tile de cura")
                continue
            bolas.append(dict(l, nome=dp["nome"], rotulo=rotulo(chave, l),
                              item_nome=nome_fr, x=x, y=y,
                              elevation=min(bruto.get("elevacao", 3), 15)))
    bolas.sort(key=lambda b: b["chave"])
    for i, b in enumerate(bolas):
        end = PRIMEIRA_FLAG_BOLA + i
        b["flag"] = "FLAG_BOLA_GALAR_%s_%02d" % (b["mapa_fonte"].upper(),
                                                 int(b["chave"].rsplit("/", 1)[1]))
        b["flag_end"] = end
    return falas, placas, bolas, recusa


# ------------------------------------------------------------------ saida ---
def corpo_inc(falas, placas, bolas):
    out = ["@ Fala de Galar, baldes (a) e (b) da fase de conteudo.",
           "@ Gerado por dev_scripts/fala_galar.py; NAO editar a mao.",
           "@ O texto vem do demake (fontes-mapas/galar-swsh), lido do bytecode",
           "@ do FireRed. Onde a fonte nao tem texto, o NPC continua mudo.",
           ""]
    por_mapa = collections.defaultdict(list)
    for l in falas + placas + bolas:
        por_mapa[(l["mapa_fonte"], l["nome"])].append(l)
    for (chave, nome) in sorted(por_mapa):
        out.append("@ ---- %s (%s) ----" % (nome, chave))
        for l in sorted(por_mapa[(chave, nome)], key=lambda z: z["chave"]):
            r = l["rotulo"]
            out.append("%s::" % r)
            if "item_nome" in l:
                qtd = l["item_qtd"] or 1
                out.append("\tfinditem %s%s" % (l["item_nome"],
                                                ", %d" % qtd if qtd != 1 else ""))
                out.append("\tend")
                out.append("")
                continue
            if l["tipo"] == "placa":
                # PLACA usa MSGBOX_SIGN e nada mais, mesmo quando a fonte poe
                # `lock/faceplayer` em volta. `faceplayer` num bg event vira
                # objeto errado (nao ha objeto falado), e `Std_MsgboxSign` ja
                # trava e solta. Mesmo molde do data/scripts/sinnoh_placas.inc.
                out.append("\tmsgbox %s_Text, MSGBOX_SIGN" % r)
                out.append("\tend")
                out.append("")
                out.extend(linhas_de_texto("%s_Text" % r, l["texto_en"],
                                           quebra=l["do_de_para"]))
                out.append("")
                continue
            mold = set(l.get("moldura") or [])
            if "lockall" in mold:
                out.append("\tlockall")
            elif "lock" in mold:
                out.append("\tlock")
            if "faceplayer" in mold:
                out.append("\tfaceplayer")
            out.append("\tmsgbox %s_Text, %s"
                       % (r, TIPO_MSGBOX.get(l["tipo_msgbox"], "MSGBOX_DEFAULT")))
            if "releaseall" in mold:
                out.append("\treleaseall")
            elif "release" in mold:
                out.append("\trelease")
            out.append("\tend")
            out.append("")
            out.extend(linhas_de_texto("%s_Text" % r, l["texto_en"],
                                       quebra=l["do_de_para"]))
            out.append("")
    return "\n".join(out) + "\n"


def bloco_de_flags(bolas):
    if not bolas:
        return ""
    out = [MARCA_INI,
           "// Uma flag por bola de item de Galar, da faixa 0x1C21 em diante",
           "// (a faixa 0x1C00+ e da obra de Galar; 0x1C00-0x1C20 sao os itens",
           "// escondidos do G4 e 0x1CFF e a FLAG_GALAR_QA_ANDAR).",
           "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/fala_galar.py; nao editar a mao."]
    larg = max(len(b["flag"]) for b in bolas) + 2
    for b in bolas:
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // %s"
                   % (larg, b["flag"], b["flag_end"], b["item_nome"]))
    out.append(MARCA_FIM)
    return "\n".join(out) + "\n"


def substitui_bloco(texto_arq, bloco):
    """Troca o bloco marcado, ou acrescenta no fim. Idempotente por construcao."""
    i = texto_arq.find(MARCA_INI)
    if i < 0:
        if not bloco:
            return texto_arq
        return texto_arq.rstrip("\n") + "\n\n" + bloco
    j = texto_arq.find(MARCA_FIM, i)
    j = len(texto_arq) if j < 0 else j + len(MARCA_FIM) + 1
    return texto_arq[:i] + bloco + texto_arq[j:]


def _traduzido(corpo, arquivo="data/scripts/galar_fala.inc"):
    """`corpo` com cada bloco trocado pelo ingles de traducao_galar.json.

    Faz EM MEMORIA o que `dev_scripts/aplica_traducao_galar.py` faz no disco, e
    reusa as funcoes DELE (`_bloco`, `corpo_do_bloco`, `escreve_bloco`) de
    proposito: uma segunda implementacao poderia fechar verde aqui com o
    aplicador de verdade escrevendo outra coisa. Bloco sem entrada no JSON, ou
    cujo portugues nao bate byte a byte, fica como esta -- e e assim que um
    bloco NOVO aparece como diferenca em vez de sumir calado.
    """
    import aplica_traducao_galar as TRAD
    caminho = f"{RAIZ}/dev_scripts/traducao_galar.json"
    if not os.path.exists(caminho):
        return corpo
    for e in json.load(open(caminho, encoding="utf-8"))["entradas"]:
        if e["arquivo"] != arquivo:
            continue
        achados = list(TRAD._bloco(e["rotulo"]).finditer(corpo))
        if len(achados) != 1:
            continue
        m = achados[0]
        atual, _cifrao = TRAD.corpo_do_bloco(m.group(3))
        if atual != e["pt"]:
            continue
        corpo = (corpo[:m.start()]
                 + TRAD.escreve_bloco(m.group(1), m.group(2), e["en"])
                 + corpo[m.end():])
    return corpo


def _manda_mais(script):
    """O prefixo de `script` com precedencia sobre a fala solta, ou None.

    `GalarObj_*` e a cena inteira do bloco c4a, e ja contem a fala. Os outros
    vem de `objetos_galar.MANDAM_MAIS`, que e a lista unica: hoje so
    `GalarPorta_*`, do lote F da onda 2. O import e tardio porque
    `objetos_galar` importa ESTE modulo, e no topo daria ciclo.
    """
    import objetos_galar
    s = str(script or "")
    for p in ("GalarObj_",) + tuple(objetos_galar.MANDAM_MAIS):
        if s.startswith(p):
            return p
    return None


def casa_objeto(mapa_json, x, y):
    """Indice UNICO do object event naquele tile, ou (None, motivo).

    Casar por coordenada da FONTE, nunca por ordem: o G4 pula objeto por
    filtro, entao o indice da fonte nao e o nosso. Tile com dois objetos
    reprova em vez de escolher (licao de Oreburgh, ESTADO 0.g).
    """
    achados = [i for i, o in enumerate(mapa_json.get("object_events", []))
               if o["x"] == x and o["y"] == y]
    if len(achados) == 1:
        return achados[0], None
    return None, ("nenhum objeto nosso em (%d,%d)" % (x, y) if not achados
                  else "%d objetos no mesmo tile (%d,%d)" % (len(achados), x, y))


def aplica(falas, placas, bolas, gravar):
    """Devolve (mudancas, recusas). Sem `gravar`, so simula."""
    mudou, recusa = collections.Counter(), []
    por_nome = collections.defaultdict(lambda: {"falas": [], "placas": [],
                                                "bolas": []})
    for l in falas:
        por_nome[l["nome"]]["falas"].append(l)
    for l in placas:
        por_nome[l["nome"]]["placas"].append(l)
    for l in bolas:
        por_nome[l["nome"]]["bolas"].append(l)

    for nome, d in sorted(por_nome.items()):
        caminho = "%s/data/maps/%s/map.json" % (RAIZ, nome)
        if not os.path.exists(caminho):
            recusa.append({"chave": nome, "motivo": "map.json nao existe"})
            continue
        doc = json.load(open(caminho))
        antes = json.dumps(doc, sort_keys=True)
        for l in d["falas"]:
            i, motivo = casa_objeto(doc, l["x"], l["y"])
            if i is None:
                recusa.append({"chave": l["chave"], "motivo": motivo})
                continue
            # PRECEDENCIA (regra do bloco c4a, 22/08/2026): cena INTEIRA vence
            # fala simples. Um object event tem UM campo `script`; onde
            # `dev_scripts/objetos_galar.py` portou a cena da fonte, ela ja
            # contem a fala que este balde daria, e sobrescrever aqui apagaria
            # a cena calado na proxima rodada de LEVA_DONA. Hoje os dois
            # conjuntos sao disjuntos por construcao (este balde so pega
            # a_fala/b_flag e o c4a so pega c_var_cena), entao esta guarda e
            # cinto de seguranca, nao conserto de defeito visto.
            #
            # LOTE F DA ONDA 2 (07/09/2026): `GalarPorta_*` entrou na mesma
            # regra. `dev_scripts/portas_script_galar.py` reaponta o `script`
            # de alguns objetos para a porta que o demake abre por script, e
            # esse rotulo NAO e derivavel da fonte que este gerador le: escrever
            # por cima apagaria a porta sem deixar rastro. A lista dos prefixos
            # que mandam mais mora em `objetos_galar.MANDAM_MAIS`, um lugar so.
            dono = _manda_mais(doc["object_events"][i].get("script"))
            if dono:
                recusa.append({"chave": l["chave"],
                               "motivo": "%s tem precedencia sobre a fala"
                                         % dono})
                continue
            doc["object_events"][i]["script"] = l["rotulo"]
            mudou["fala"] += 1
        # bg de placa: append no fim, depois dos itens escondidos do G4.
        #
        # DEFEITO ACHADO EM 22/08/2026 (rodada 9), e ele era latente ate agora:
        # a guarda era so pelo ROTULO, e por isso este bloco acrescentava um bg
        # NOVO em cima de uma coordenada que outro balde ja tinha ocupado. Com o
        # leitor de texto passando a decodificar `{PLAYER}`, cinco placas do
        # `objetos_galar.py` (que roda DEPOIS deste, e tem precedencia) cairam
        # exatamente nessas coordenadas e o `map.json` ficou com DOIS bg_events
        # no mesmo tile; o `objetos_galar.aplica` entao recusava a colocacao com
        # "2 bg events no mesmo tile" e a placa dele sumia. A guarda passou a ser
        # pela COORDENADA, que e o que o motor enxerga: um tile, uma placa.
        ja = {b.get("script") for b in doc.get("bg_events", [])}
        ocupado_bg = {(b.get("x"), b.get("y")) for b in doc.get("bg_events", [])}
        for l in sorted(d["placas"], key=lambda z: z["chave"]):
            if l["rotulo"] in ja:
                continue
            if (l["x"], l["y"]) in ocupado_bg:
                recusa.append({"chave": l["chave"],
                               "motivo": "ja ha bg em (%d,%d)" % (l["x"], l["y"])})
                continue
            ocupado_bg.add((l["x"], l["y"]))
            doc.setdefault("bg_events", []).append({
                "type": "sign", "x": l["x"], "y": l["y"], "elevation": 0,
                "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                "script": l["rotulo"]})
            mudou["placa"] += 1
        # bola: APPEND no fim da lista de objetos, sempre. A save guarda indice
        # de object event; objeto novo no meio renumeraria os que ja existem.
        ja_o = {o.get("script") for o in doc.get("object_events", [])}
        for l in sorted(d["bolas"], key=lambda z: z["chave"]):
            if l["rotulo"] in ja_o:
                continue
            doc.setdefault("object_events", []).append({
                "graphics_id": "OBJ_EVENT_GFX_ITEM_BALL",
                "x": l["x"], "y": l["y"], "elevation": l["elevation"],
                "movement_type": "MOVEMENT_TYPE_NONE",
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": l["rotulo"], "flag": l["flag"]})
            mudou["bola"] += 1
        if json.dumps(doc, sort_keys=True) != antes:
            mudou["mapa"] += 1
            if gravar:
                with open(caminho, "w") as f:
                    json.dump(doc, f, indent=2, ensure_ascii=False)
                    f.write("\n")
    return mudou, recusa


def escreve_inc(falas, placas, bolas, gravar):
    corpo = corpo_inc(falas, placas, bolas)
    if gravar:
        open(INC, "w").write(corpo)
        fonte = open(EVENT_S).read()
        linha = '\t.include "data/scripts/galar_fala.inc"'
        if linha not in fonte:
            open(EVENT_S, "w").write(fonte.rstrip("\n") + "\n" + linha + "\n")
    return corpo


def escreve_flags(bolas, gravar):
    bloco = bloco_de_flags(bolas)
    atual = open(FLAGS_H).read()
    novo = substitui_bloco(atual, bloco)
    if gravar and novo != atual:
        open(FLAGS_H, "w").write(novo)
    return novo


# ------------------------------------------------------------------- demo ---
def demo():
    """Autoteste. Nao grava nada, e planta mutacoes para provar que sao vistas."""
    falhas = []
    rom, tab, cmap, fila = carrega()

    # 1. a tabela de opcodes saiu do event.inc do FireRed, e nao de memoria.
    for op, nome in ((0x02, "end"), (0x05, "goto"), (0x09, "callstd"),
                     (0x0F, "loadword"), (0x4F, "applymovement"),
                     (0x53, "removeobject"), (0x5C, "trainerbattle")):
        if tab.get(op, ("?",))[0] != nome:
            falhas.append("opcode 0x%02X devia ser %s, veio %s"
                          % (op, nome, tab.get(op, ("?",))[0]))
    if len(tab) < 200:
        falhas.append("tabela de opcodes pequena demais: %d" % len(tab))

    linhas = varre(rom, tab, cmap, fila)
    falas, placas, bolas, recusa = plano(linhas)

    # 2. IDA E VOLTA DO TEXTO: reescrever o texto emitido com o NOSSO charmap
    # tem que devolver byte a byte o que a fonte tem. Sem isto, acento vira
    # outro caractere e ninguem percebe ate alguem ler a placa no jogo.
    inverso = {}
    for b, c in sorted(cmap.items()):
        inverso.setdefault(c, b)
    ctrl = {"\\n": 0xFE, "\\l": 0xFA, "\\p": 0xFB}
    # As chaves que o `texto()` emite tambem tem de saber voltar, senao esta
    # prova viraria "nenhuma frase com {PLAYER} passa" e o guarda mediria a si
    # mesmo. Cada uma volta ao byte EXATO que o assembler geraria.
    chaves = {"{PLAYER}": bytes([0xFD, 0x01]), "{RIVAL}": bytes([0xFD, 0x06])}
    for b_cor, nome_cor in COR_DO_BYTE.items():
        chaves["{COLOR %s}" % nome_cor] = bytes([0xFC, 0x01, b_cor])
    ruins = 0
    for l in falas + placas:
        bruto, i, saida = l["texto"], 0, []
        while i < len(bruto):
            if bruto[i] == "{":
                fim = bruto.find("}", i)
                token = bruto[i:fim + 1] if fim > 0 else None
                if token not in chaves:
                    ruins += 1
                    break
                saida.extend(chaves[token])
                i = fim + 1
                continue
            if bruto[i] == "\\" and bruto[i:i + 2] in ctrl:
                saida.append(ctrl[bruto[i:i + 2]])
                i += 2
                continue
            b = inverso.get(bruto[i])
            if b is None:
                ruins += 1
                break
            saida.append(b)
            i += 1
        else:
            off = int(l["ponteiro_fonte"], 16)
            achado = bytes(saida)
            # o offset do texto nao esta na linha; refaz pelo desmontador
            r = desmonta(rom, tab, off)
            alvos = [o for o, _t in r.textos]
            if not alvos or rom[alvos[0]:alvos[0] + len(achado)] != achado:
                ruins += 1
    if ruins:
        falhas.append("%d textos nao voltam byte a byte pelo charmap" % ruins)

    # 2b. O TIL, COM MUTACAO PLANTADA (23/08/2026). O passo 2 acima fechava
    # verde com o defeito dentro: a fonte escreve "nao" com o byte 0xF4, o
    # charmap chamava 0xF4 de trema alemao, e a ida e volta batia byte a byte
    # com o jogador lendo "N-trema-o" em 315 lugares. Prova que fecha e prova
    # que nao mede: byte igual nao e letra certa. Estes quatro casos medem a
    # LETRA, e o ultimo planta a mutacao.
    if cmap.get(0xF4) != "\u00e3":
        falhas.append("0xF4 devia decodificar como a-til, veio %r"
                      % cmap.get(0xF4))
    if inverso.get("\u00e3") != 0xF4:
        falhas.append("a-til devia voltar em 0xF4, veio %r"
                      % inverso.get("\u00e3"))
    com_til = [l for l in falas + placas if "\u00e3" in l["texto"]]
    # Piso 50, medido em 23/08/2026: 90 falas e placas trazem a-til. O piso
    # existe para o caso vazio, nao para congelar o numero.
    if len(com_til) < 50:
        falhas.append("so %d frases com a-til: o de-para do til nao pegou"
                      % len(com_til))
    if inverso.get("\u00e4") is not None:
        falhas.append("o trema ainda tem byte no charmap: 'N-trema-o' voltaria "
                      "a atravessar a ida e volta sem ninguem ver")
    if com_til:
        mutante = com_til[0]["texto"].replace("\u00e3", "\u00e4")
        if all(inverso.get(c) is not None for c in mutante if c.isalpha()):
            falhas.append("MUTACAO PLANTADA PASSOU: %r voltou pelo charmap; "
                          "o portao do til e cego" % mutante[:40])

    # 3. rotulo unico, senao o assembler junta duas falas numa so.
    rot = [l["rotulo"] for l in falas + placas + bolas]
    if len(set(rot)) != len(rot):
        falhas.append("rotulo repetido: %d de %d" % (len(rot) - len(set(rot)),
                                                     len(rot)))

    # 4. flag: dentro da faixa de Galar, sem repetir, sem pisar nas do G4 nem
    # na FLAG_GALAR_QA_ANDAR, e com a reserva de cena de pe.
    ends = [b["flag_end"] for b in bolas]
    if ends and (min(ends) < PRIMEIRA_FLAG_BOLA or max(ends) > ULTIMA_FLAG_BOLA):
        falhas.append("flag de bola fora da faixa 0x%04X-0x%04X"
                      % (PRIMEIRA_FLAG_BOLA, ULTIMA_FLAG_BOLA))
    if len(set(ends)) != len(ends):
        falhas.append("flag de bola repetida")
    livres = ULTIMA_FLAG_BOLA - PRIMEIRA_FLAG_BOLA + 1 - len(ends)
    if livres < RESERVA_DE_CENA:
        falhas.append("sobram %d flags na faixa de Galar, menos que a reserva %d"
                      % (livres, RESERVA_DE_CENA))

    # 5. bola nunca em tile que trave o jogo (o plano ja filtra; aqui e prova).
    G = _gente()
    _pc, de_para = G.carrega()
    for b in bolas:
        dp = de_para[b["mapa_fonte"]]
        if not G.andavel(b["mapa_fonte"], dp["w"], dp["h"], b["x"], b["y"]):
            falhas.append("bola %s em tile nao andavel" % b["chave"])
        if (b["x"], b["y"]) in G.warps_limpos(b["mapa_fonte"]):
            falhas.append("bola %s em cima de warp" % b["chave"])

    # 6. IDEMPOTENCIA de verdade: aplicar em cima do que ja esta gravado nao
    # muda mapa nenhum, e o .inc sai igual duas vezes.
    corpo1 = corpo_inc(falas, placas, bolas)
    corpo2 = corpo_inc(falas, placas, bolas)
    if corpo1 != corpo2:
        falhas.append("o .inc nao e estavel entre duas geracoes")
    mudou, _r = aplica(falas, placas, bolas, gravar=False)
    # O .inc no disco E A SAIDA CRUA DESTE GERADOR OUTRA VEZ, desde a onda 3
    # (lote L1, 08/09/2026): o ingles passou a entrar NA GERACAO, e nao mais
    # numa segunda passada de `aplica_traducao_galar.py`.
    #
    # HISTORIA, para ninguem refazer o caminho: entre 06/09 (decisao 32, commit
    # 2f16420f7c) e 07/09 este caso comparava a saida crua, em portugues, com um
    # arquivo ja traduzido, e reprovava sempre; em 07/09 ele passou a traduzir o
    # corpo em memoria antes de comparar (`_traduzido`). Com o pipeline em
    # ingles esse passo virou identidade -- o corpo ja sai traduzido -- e a
    # mutacao plantada de entao ("a traducao tem de mudar alguma coisa")
    # reprovava por medir a si mesma. A comparacao voltou a ser direta, e a
    # mutacao plantada mudou de lugar: ela agora prova que o GERADOR traduz.
    aplicado = os.path.exists(INC) and open(INC).read() == corpo1
    if os.path.exists(INC) and not aplicado:
        falhas.append("data/scripts/galar_fala.inc gravado NAO e o que este "
                      "gerador produz hoje (mutacao a mao, fonte mudou, ou "
                      "bloco novo sem traducao): rode --aplicar")
    # MUTACAO PLANTADA: com os dois de-paras VAZIOS, o corpo tem de sair
    # diferente. Sem esta linha, um `resolve` que devolvesse sempre o portugues
    # da fonte fecharia verde: a comparacao acima so diz que o arquivo bate com
    # o gerador, nao que o gerador traduz.
    velha = traducao()
    try:
        reinicia_traducao(Traducao(traducao="/nao/existe.json",
                                   resgate="/nao/existe.json"))
        _f, _p, _b, _r = plano(linhas)
        sem_de_para = corpo_inc(_f, _p, _b)
    finally:
        reinicia_traducao(velha)
    if sem_de_para == corpo1:
        falhas.append("o corpo sai igual com e sem os de-paras: o gerador nao "
                      "esta traduzindo, e esta comparacao mede a si mesma")
    # e o outro lado da mesma prova: sem de-para, o que ficaria de fora e
    # exatamente o que a regua do portao chama de portugues.
    if len(_f) + len(_p) >= len(falas) + len(placas):
        falhas.append("sem de-para nenhum, o gerador escreveu tanto quanto com "
                      "de-para: o degrau 4 da regra nao esta mordendo")
    if aplicado and mudou["mapa"]:
        falhas.append("segunda passada ainda mexeria em %d mapas: nao e idempotente"
                      % mudou["mapa"])

    # 7. MUTACAO PLANTADA 1: um texto corrompido no .inc tem de ser visto.
    sujo = corpo1.replace(".string \"", ".string \"XX", 1)
    if sujo == corpo1 or sujo == corpo_inc(falas, placas, bolas):
        falhas.append("mutacao de texto no .inc nao seria vista")

    # 8. MUTACAO PLANTADA 2: dois objetos no mesmo tile tem de REPROVAR o
    # casamento por coordenada, em vez de escolher um.
    finge = {"object_events": [{"x": 5, "y": 5}, {"x": 5, "y": 5}]}
    i, motivo = casa_objeto(finge, 5, 5)
    if i is not None or "2 objetos" not in (motivo or ""):
        falhas.append("casamento por coordenada aceitou tile ambiguo")
    i, motivo = casa_objeto({"object_events": [{"x": 1, "y": 1}]}, 1, 1)
    if i != 0:
        falhas.append("casamento por coordenada perdeu o caso simples")

    # 9. MUTACAO PLANTADA 3: bloco de flags trocado tem de voltar ao lugar.
    atual = open(FLAGS_H).read()
    bloco = bloco_de_flags(bolas)
    sujo_h = substitui_bloco(atual, bloco.replace("0x1C21", "0x0001", 1))
    if substitui_bloco(sujo_h, bloco) != substitui_bloco(atual, bloco):
        falhas.append("substituicao do bloco de flags nao repoe o bloco certo")

    # ONDA 3, LOTE L1: o pipeline nasce em ingles. O caso e comum aos tres
    # geradores e mora em `demo_pipeline_ingles` para nao virar tres copias.
    falhas.extend(demo_pipeline_ingles())

    print("demo: %s" % ("OK" if not falhas else "REPROVADO"))
    for f in falhas:
        print("  FALHA", f)
    print("  opcodes %d | linhas %d | falas %d | placas %d | bolas %d | recusas %d"
          % (len(tab), len(linhas), len(falas), len(placas), len(bolas),
             len(recusa)))
    return 1 if falhas else 0


# Motivo de recusa dos baldes a e b que NAO muda sozinho: o dado da fonte nao
# existe ou nao decodifica. Vira `descartada`. Todo o resto vira `adiada`,
# porque uma decisao futura destrava a linha. Mesma lei do
# `MOTIVO_TERMINAL_OBJ` de objetos_galar.py.
MOTIVO_TERMINAL_FALA = (
    "mapa da fonte nao esta no de-para do G3",
    "objeto foi para a sujeira do G0",
    "NPC nao entrou no mapa no G4",
)


def devolve_para_fila(linhas, recusa, gravar):
    """Escreve na fila o motivo MEDIDO de cada linha de balde a ou b recusada.

    Acrescentado em 06/09/2026 pelo lote C da onda 1, no mesmo formato do
    `devolve_para_fila` de objetos_galar.py e pela mesma razao: a fila cobra
    linha a linha, e recusa que so vira contagem no relatorio deixa a linha
    pendente para sempre, sem que ninguem saiba por que ela nao entrou.

    Este modo NAO escreve mapa, .inc nem flag: so o motivo. Linha que ja tem
    decisao (`feita`, `descartada`, `adiada`) nao e tocada, entao rodar de novo
    nao reabre nada.

    Onde o balde b recusou por "objeto ja entrou como NPC mudo", o motivo ganha
    o SEGUNDO fato medido aqui: o id de item da fonte fora da tabela de itens
    do FireRed (0..374). Os dois juntos sao a linha inteira, e sem o segundo a
    proxima rodada acharia que basta escolher entre NPC e bola.
    """
    G = _gente()
    itens_fr = G.itens_da_fonte()
    por_chave = {l["chave"]: l for l in linhas}
    fila = f"{RAIZ}/dev_scripts/fila_galar.json"
    doc = json.load(open(fila))
    motivos = {}
    for r in recusa:
        m = r["motivo"]
        l = por_chave.get(r["chave"])
        if l and l.get("balde") == "b_flag" and l.get("item"):
            if itens_fr.get(l["item"]) is None:
                m += ("; e o item %d da fonte esta fora da tabela de itens do "
                      "FireRed (0..374): nao ha o que entregar" % l["item"])
        motivos[r["chave"]] = m
    n, quadro = 0, collections.Counter()
    for l in doc["linhas"]:
        if l["status"] in ("feita", "descartada", "adiada"):
            continue
        m = motivos.get(l["chave"])
        if not m:
            continue
        st = ("descartada" if any(t in m for t in MOTIVO_TERMINAL_FALA)
              else "adiada")
        l["status"] = st
        l["motivo_do_status"] = ("baldes a e b, lote C da onda 1, 06/09/2026: "
                                 + m)
        n += 1
        quadro[st] += 1
    if gravar and n:
        with open(fila, "w") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return n, quadro


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gravar", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--fila", action="store_true",
                    help="devolve o motivo medido de cada linha recusada para "
                         "dev_scripts/fila_galar.json (com --gravar, escreve; "
                         "NUNCA escreve map.json, .inc nem flag)")
    ap.add_argument("--amostra", type=int, default=0)
    a = ap.parse_args()
    if a.demo:
        raise SystemExit(demo())
    rom, tab, cmap, fila = carrega()
    linhas = varre(rom, tab, cmap, fila)
    imprime(linhas)
    falas, placas, bolas, recusa = plano(linhas)
    print("\nEXECUTAVEL HOJE: %d falas de NPC, %d placas, %d bolas de item"
          % (len(falas), len(placas), len(bolas)))
    mot = collections.Counter(r["motivo"].split(":")[0] for r in recusa)
    for m, c in mot.most_common(10):
        print("  recusado %5d  %s" % (c, m))
    if a.fila:
        # O interruptor aqui e `--gravar`, e NAO `--aplicar`: `--aplicar` deste
        # arquivo escreve map.json, e na onda 1 o map.json de Galar tem outro
        # dono. Devolver motivo para a fila nao precisa disso.
        n, quadro = devolve_para_fila(linhas, recusa, a.gravar)
        print("\nfila: %d linhas dos baldes a e b ganharam motivo medido" % n)
        for st, c in sorted(quadro.items()):
            print("   %-12s %d" % (st, c))
    print("\ntraducao na geracao: %s" % dict(traducao().conta))
    print("textos sem traducao (distintos): %d, em %d linhas da fila"
          % (len(traducao().faltam), len(traducao().chaves_faltando())))
    if a.aplicar:
        if traducao().grava_falta(True):
            print("gravado %s" % FALTA_JSON)
        n_ft = marca_fila_sem_traducao(True)
        print("fila: %d linhas ficaram adiadas por texto sem traducao" % n_ft)
        escreve_inc(falas, placas, bolas, True)
        escreve_flags(bolas, True)
        mudou, rec = aplica(falas, placas, bolas, True)
        print("\ngravado: %d falas, %d placas, %d bolas em %d map.json"
              % (mudou["fala"], mudou["placa"], mudou["bola"], mudou["mapa"]))
        for r in rec[:10]:
            print("  nao aplicado: %s %s" % (r["chave"], r["motivo"]))
        if len(rec) > 10:
            print("  ... mais %d" % (len(rec) - 10))
    if a.amostra:
        print("\namostra do balde a:")
        for l in [x for x in linhas if x["balde"] == "a_fala"][:a.amostra]:
            print("  %-26s %-22s %r" % (l["chave"], l["mapa"], l["texto"][:90]))
        print("\namostra do balde b:")
        for l in [x for x in linhas if x["balde"] == "b_flag"][:a.amostra]:
            print("  %-26s item=%d x%d flags=%d %r" %
                  (l["chave"], l["item"], l["item_qtd"], l["n_flags"],
                   (l["texto"] or "")[:60]))
    if a.gravar:
        # O TEXTO nao entra no censo: ele ja mora em data/scripts/galar_fala.inc,
        # que e o porte de verdade. Guardar a fala duas vezes so cria duas
        # verdades e uma delas envelhece.
        linhas = [{k: v for k, v in l.items() if k != "texto"} for l in linhas]
        json.dump({"gerado_por": "dev_scripts/fala_galar.py",
                   "fonte": "fontes-mapas/galar-swsh (datamine, fora do repo)",
                   "linhas": linhas}, open(ROTEIROS, "w"), indent=1,
                  ensure_ascii=False)
        print("\ngravado %s (%d linhas)" % (ROTEIROS, len(linhas)))


if __name__ == "__main__":
    main()
