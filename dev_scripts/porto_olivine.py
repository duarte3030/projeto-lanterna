#!/usr/bin/env python3
"""Refino de `OlivineCity` (tema PORTO E FAROL), no `gTileset_OlivineCity`,
inteiramente com arte que o cartucho JÁ TEM compilada.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: 22,4% do chão andável a pé (216 células de 963) é UM
metatile, o 905. E o 905 não é uma praça: é a TRAMA, o calçamento de losangos
diagonais que serve de rua, de lote e de esplanada do porto ao mesmo tempo.
Rotulando o `map.bin` célula a célula, as 216 se desenham em quatro pedaços: a
avenida norte (colunas 19 a 21, linhas 15 a 45), o ramo oeste (linhas 29 a 38),
o ramo leste (colunas 30 a 32) e, o maior deles, a ESPLANADA DO PORTO (linhas 46
a 49, colunas 6 a 32, 91 células). Olivine é a cidade do farol da Jasmine e do
cais que leva a Cianwood, e o que ela mostra na beira do mar é um lençol de
calçamento vazio.

A TRAMA NÃO ACEITA O TRUQUE DE ECRUTEAK, MAS ACEITA O ESPELHO, e essa é a
primeira medição que muda o tamanho da rodada. Em Ecruteak o calçamento era um
desenho FECHADO dentro do metatile, e por isso dava para reembaralhar os
quadrantes e ganhar onze lajes novas de graça. Aqui não: os quatro tiles do 905
(593, 594, 609 e 610, da paleta 1 do primário) formam um padrão CONTÍNUO de
período 16, e ladrilhar o 905 cinco por cinco mostra uma trama de losangos que
atravessa a fronteira do metatile sem costura. Qualquer REARRANJO de quadrante
rompe a diagonal no meio da célula e lê como defeito, não como variante.

O que ele aceita é uma coisa só, e ela não é rearranjo: o ESPELHO HORIZONTAL do
metatile inteiro (594H, 593H na linha de cima e 610H, 609H na de baixo). Ele
inverte o sentido da diagonal sem quebrar nenhuma linha, e encostado na trama
normal desenha uma junta em ESPINHA DE PEIXE, que é padrão de calçamento de
verdade e não emenda torta. E não é invenção desta passada: o próprio
`gTileset_OlivineCity` já trazia essa orientação nos metatiles 660 a 663, 668 e
669, todos vivos no mapa. Foi essa a peça que virou a AVENIDA (item 6 do
desenho); o resto da variedade veio de móvel e de material novo, não de laje.

O ATALHO QUE EXISTE E QUE FOI RECUSADO, escrito aqui para ninguém tentar de
novo: o metatile 449 do PRIMÁRIO é byte a byte a mesma coisa que o 905 (mesmas
quatro entradas, mesma camada de cima vazia, mesmo atributo 0x0000), e o mapa já
usa os dois. Trocar metade das 216 células de 905 por 449 derrubaria a régua para
11% sem mudar UM PIXEL da tela. A régua conta id de metatile, e um id novo com
distância de cor zero engana a régua e não enfeita nada. Esta passada não faz
isso, e a conferência (`--confere`) mede também o carimbo por FAMÍLIA VISUAL,
somando os ids que desenham a mesma coisa, justamente para que a nota não possa
ser comprada com duplicata.

O ORÇAMENTO, medido nesta árvore e não herdado de briefing:

  split      `layout_version: "johto"`, que é `bigPrimary`: primário de 640
             tiles, 640 metatiles e 7 paletas; secundário de 384 tiles, 384
             metatiles e 6 paletas (vagas 7 a 12). O id global do metatile
             secundário é 640 + local.
  tiles      o `tiles.png` do secundário tem 240 tiles de 384 e sobram 144
             vagas. Esta passada NÃO GASTA NENHUMA: nenhum pixel novo entra no
             repositório.
  metatiles  o `metatiles.bin` tem 340 entradas de 384 e o
             `metatile_attributes.bin` tem 680 B (2 bytes por metatile). Esta
             passada NÃO CRESCE os arquivos: ela sobrescreve vaga MORTA, e vaga
             morta aqui tem definição estreita, medida e conferida em tempo de
             gravação: entrada que nem `OlivineCity` nem `Route40` escrevem no
             `map.bin` E cujo conteúdo atual é o preenchimento de grama
             (620, 621, 19, 637 na camada de baixo e nada na de cima). São 66
             vagas assim para 20 peças, e as 14 que só a `Route40` usa (676, 749, 750, 757,
             758, 765, 766, 773, 774, 781, 782, 789, 790 e 978) ficam intactas,
             senão a prova de zero pixel da rota irmã reprova.
  paleta     ZERO cor nova. Toda peça desta passada aponta para tile e paleta
             que já estão compilados.

  Ou seja: custo em tile ZERO, custo em cor ZERO, custo em ROM ZERO. Os quatro
  arquivos tocados têm exatamente o mesmo tamanho de antes (map.bin 7.488 B,
  metatiles.bin 5.440 B, metatile_attributes.bin 680 B, tiles.png 3.217 B e
  intocado), e a `pokeemerald.gba` continua com os mesmos 33.554.432 B.

O QUE A RÉGUA MEDE DEPOIS, com as duas contas: por ID o carimbo cai de 22,4%
(905, 216 de 963) para 8,1% (827, 75 de 931), e o metatile mais repetido deixa
de ser a trama e passa a ser o tijolo da orla, que já existia. Por FAMÍLIA
VISUAL, somando a trama nas duas orientações mais o 449 do primário, ela cai de
26,3% para 17,0%. A segunda conta é a honesta e é a que manda: ela existe para
que a nota não possa ser comprada com duplicata (ver o parágrafo do 449).

O DESENHO, e a regra dele é uma frase: A ESPLANADA VIRA CAIS DE TRABALHO. São
seis peças, e cada uma sai de arte que o repositório já tinha e que NENHUM dos
dois mapas do tileset usava:

  1. O CAIS DE PEDRA. O calçamento de tijolo do porto (o metatile 827, quatro
     vezes o tile 701 da vaga 8) sobe da orla para dentro da esplanada: as
     linhas 48 e 49 inteiras, mais uma língua nas linhas 46 e 47 na frente do
     píer. A cópia é ANDÁVEL, atributo 0x0000, e não o 0x1000 do 827, porque a
     regra 3 da onda cobra `(comportamento, layerType)` idêntico em toda célula
     que continua andável e a trama que ela substitui é `NORMAL`. Com a camada
     de cima vazia, `COVERED` e `NORMAL` desenham o MESMO pixel (o
     `DrawMetatile` de `src/field_camera.c` só troca o BG de destino), então a
     cópia andável não é um segundo desenho, é o mesmo desenho com o atributo
     certo. Dois bueiros (o tile 700, aquele disco escuro que o tileset
     desenhou e ninguém usou) entram salpicados para o cais não virar lençol.
  2. OS GUARDA-SÓIS. O secundário tem DOIS guarda-sóis inteiros, um amarelo e um
     azul, desenhados e nunca escritos em mapa nenhum: a copa alta (tiles 646 a
     649 e 663 a 666 da vaga 7), a copa baixa (650 a 653 e 667 a 669) e o pé
     (692 e 693). Na fonte eles se apoiam no tijolo; aqui a camada de baixo
     passa a ser a trama, e o resto é o mesmo. As duas linhas de copa ficam
     ANDÁVEIS com atributo 0x0000, que é o que o próprio tileset já dizia delas
     e o mesmo da trama; só o pé vira sólido, com `layerType` COVERED, como a
     regra 5 exige.
  3. O PAINEL DO PORTO. O toldo amarelo de três células (tiles 680 a 685 e 686 a
     691 da vaga 7) montado sobre a trama, com as pernas 893 e 892, que já vêm
     desenhadas sobre o tijolo e caem exatamente na linha do cais novo. Sólido e
     COVERED, das seis células.
  4. AS BALIZAS DE AMARRAÇÃO. O metatile 944 (par de balizas sobre a trama) já
     existe no tileset e a cidade já o usa; esta passada espalha mais seis pela
     beira da esplanada e pela avenida.
  5. OS ARBUSTOS. A camada de cima dos metatiles 26 e 27 do PRIMÁRIO (tiles 38,
     39, 54 e 55 da vaga 0), o mesmo par que Ecruteak usou, remontado sobre a
     trama. Peça de DUAS células, sólida, para quebrar a avenida norte e o ramo
     leste sem fechar passagem. Nenhum par entra numa rua de duas células de
     largura, e nenhum entra na frente de porta: os dois primeiros lugares
     escolhidos (25,42) e (19,39) saíram justamente porque um ficava na saída do
     Mercado e o outro na saída da casa 3.
  6. A AVENIDA EM ESPINHA DE PEIXE. Todo o que ainda era trama 905 dentro do
     retângulo das colunas 18 a 22, linhas 15 a 45, passa para a trama
     ESPELHADA. É a avenida que desce do norte até o cais, e ela ganha um
     calçamento com o sentido invertido: a cidade passa a ter hierarquia de
     rua, com a avenida numa direção e os lotes na outra. Custa ZERO tile e ZERO
     cor, e a junta é limpa porque o espelho não quebra a diagonal.

O QUE FICOU DE FORA, e o motivo:

  - A COLAGEM DE MADEIRA. O primário tem um deque de tábuas inteiro e andável
    (metatiles 354 a 372, atributo 0x0000) que seria o piso perfeito de um
    pátio de carga. Ele está fora porque as peças de BORDA dele têm a grama
    PINTADA no tile: encostadas no calçamento elas mostram uma franja verde. Só
    o miolo (o 363) é limpo, e miolo sem borda encosta no calçamento em ângulo
    reto, que é o defeito de retalho que a onda já pagou uma vez.
  - AS LAJES DE VARIANTE POR REARRANJO. Explicado acima: a trama é contínua e
    nenhum rearranjo de quadrante sobrevive à diagonal. O único movimento que
    ela aceita é o espelho horizontal do metatile inteiro, e ele entrou.
  - O CANTEIRO DE GRAMA na esplanada. O anel de transição (441, 443, 444, 448,
    450, 451, 452 e 457) é todo `COVERED`, e um canteiro decente precisa de um
    anel de 6x5 células. Caberia com oito cópias de atributo, mas ele comeria a
    esplanada inteira e deixaria o cais sem lugar. Fica para uma próxima.

A LENTE, e ela é quem decide o atributo de cada peça. A regra 3 da onda cobra
`(comportamento, layerType)` idêntico em toda célula que continua andável, e a
trama 905 é (0x00, NORMAL). Logo:

  - todo PISO novo (o cais, as suas duas variantes de bueiro e a trama
    espelhada da avenida) entra com atributo 0x0000, igual à trama, e a célula
    continua andável: a lente não se mexe;
  - toda COPA de guarda-sol entra com 0x0000 e continua andável, que é o que o
    tileset já dizia dela (o 876 e o 884 da fonte são 0x0000);
  - todo MÓVEL (pé de guarda-sol, painel, baliza, arbusto) entra com 0x1000,
    ou seja COVERED, e a célula vira sólida. COVERED põe as DUAS camadas abaixo
    do sprite (`DrawMetatile`), então o jogador parado ao sul aparece na frente
    da peça, que é o que a regra 3 da onda pede da base de um móvel.

Uso:
    python3 dev_scripts/porto_olivine.py            # planeja e mostra, sem gravar
    python3 dev_scripts/porto_olivine.py --aplicar  # grava tileset e map.bin
    python3 dev_scripts/porto_olivine.py --desfazer # volta ao master
    python3 dev_scripts/porto_olivine.py --confere  # a régua, por id e por família
    python3 dev_scripts/porto_olivine.py --demo     # auto-teste (bloco T205)
"""
import collections
import json
import os
import struct
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")

PLANO = f"{RAIZ}/dev_scripts/porto_olivine.json"
# A REFERENCIA. Todo o plano desta passada e funcao PURA do commit de
# referencia, e nunca da arvore de trabalho. Sem isso o script nao e
# idempotente: depois de aplicado, as vagas que ele escreveu deixam de parecer
# mortas, a avenida deixa de parecer trama, e uma segunda rodada de --aplicar
# escolheria OUTRAS vagas e escreveria OUTRO mapa, calada. Medido em 09/09/2026,
# quando o auto-teste acusou 95 celulas num plano de 153.
REF = "master"
DESTINO = f"{RAIZ}/data/tilesets/secondary/olivine_city"

PRIMARIO = "gTileset_JohtoGeneral"
SECUNDARIO = "gTileset_OlivineCity"
ALVO = "OlivineCity"
# os DOIS layouts que dividem o gTileset_OlivineCity. A rota e a prova de nao
# regressao: ela tem que renderizar com ZERO pixel diferente.
IRMAOS = ["OlivineCity", "Route40"]

N_META_PRI = 640
TETO_META = 384
TETO_REGUA = 20.0

TRAMA = 905           # o calcamento de losangos, o carimbo desta cidade
TIJOLO = 827          # o calcamento de tijolo da orla do porto
LAYER_COVERED = 0x1000

# O preenchimento de grama que marca vaga MORTA no secundario. Vaga com
# qualquer outro conteudo pode ser arte de verdade e nao se escreve nela.
GRAMA_MORTA = (620, 621, 19, 637)

# As quatro entradas da camada de baixo da trama (tile do primario, paleta 1).
TRAMA_BAIXO = ((593, 0, 0, 1), (594, 0, 0, 1), (609, 0, 0, 1), (610, 0, 0, 1))
# A MESMA trama espelhada na horizontal, quadrante a quadrante. Nao e rearranjo:
# e o metatile inteiro virado, o que inverte a diagonal e casa com a trama
# normal sem costura (o proprio tileset ja usava essa orientacao nos metatiles
# 660 a 663, 668 e 669).
TRAMA_ESPELHO = ((594, 1, 0, 1), (593, 1, 0, 1), (610, 1, 0, 1), (609, 1, 0, 1))
# O tijolo do porto, na vaga 8 do secundario.
TIJOLO_BAIXO = ((701, 0, 0, 8),) * 4
VAZIO = ((0, 0, 0, 0),) * 4


def _w(t):
    """Empacota (tile, espelho horizontal, espelho vertical, paleta) numa word."""
    tile, h, v, pal = t
    return (tile & 0x3FF) | (h << 10) | (v << 11) | (pal << 12)


def entradas(baixo, cima=VAZIO):
    return [_w(t) for t in baixo] + [_w(t) for t in cima]


# ------------------------------------------------------------------ o CATALOGO
# Cada peca e um metatile novo, escrito numa vaga morta. `attr` 0x0000 mantem a
# celula ANDAVEL e igual a trama; 0x1000 e COVERED e a celula vira SOLIDA.
# A ordem desta lista e a ordem de alocacao das vagas, e ela nao muda depois de
# aplicada: mudar a ordem mudaria o id de cada peca e sujaria o diff a toa.
CATALOGO = [
    # ---- o cais de pedra (piso, ANDAVEL) ----
    ("cais",        TIJOLO_BAIXO, VAZIO, 0x0000),
    ("cais_bueiro_e", ((700, 0, 0, 8), (701, 0, 0, 8), (701, 0, 0, 8), (701, 0, 0, 8)),
     VAZIO, 0x0000),
    ("cais_bueiro_d", ((701, 0, 0, 8), (700, 0, 0, 8), (701, 0, 0, 8), (701, 0, 0, 8)),
     VAZIO, 0x0000),
    # ---- guarda-sol amarelo (copa ANDAVEL, pe SOLIDO) ----
    ("gs_am_alto_e", TRAMA_BAIXO,
     ((646, 0, 0, 7), (647, 0, 0, 7), (648, 0, 0, 7), (649, 0, 0, 7)), 0x0000),
    ("gs_am_alto_d", TRAMA_BAIXO,
     ((647, 1, 0, 7), (646, 1, 0, 7), (649, 1, 0, 7), (648, 1, 0, 7)), 0x0000),
    ("gs_am_baixo_e", TRAMA_BAIXO,
     ((650, 0, 0, 7), (651, 0, 0, 7), (652, 0, 0, 7), (653, 0, 0, 7)), 0x0000),
    ("gs_am_baixo_d", TRAMA_BAIXO,
     ((651, 1, 0, 7), (650, 1, 0, 7), (653, 1, 0, 7), (652, 1, 0, 7)), 0x0000),
    # ---- guarda-sol azul ----
    ("gs_az_alto_e", TRAMA_BAIXO,
     ((663, 0, 0, 7), (664, 0, 0, 7), (665, 0, 0, 7), (666, 0, 0, 7)), 0x0000),
    ("gs_az_alto_d", TRAMA_BAIXO,
     ((664, 1, 0, 7), (663, 1, 0, 7), (666, 1, 0, 7), (665, 1, 0, 7)), 0x0000),
    ("gs_az_baixo_e", TRAMA_BAIXO,
     ((667, 0, 0, 7), (668, 0, 0, 7), (652, 0, 0, 7), (669, 0, 0, 7)), 0x0000),
    ("gs_az_baixo_d", TRAMA_BAIXO,
     ((668, 1, 0, 7), (667, 1, 0, 7), (669, 1, 0, 7), (652, 1, 0, 7)), 0x0000),
    # ---- o painel do porto, 3x2, SOLIDO ----
    ("pn_alto_e", TRAMA_BAIXO,
     ((680, 0, 0, 7), (681, 0, 0, 7), (683, 0, 0, 7), (684, 0, 0, 7)), 0x1000),
    ("pn_alto_m", TRAMA_BAIXO,
     ((681, 0, 0, 7), (681, 0, 0, 7), (684, 0, 0, 7), (684, 0, 0, 7)), 0x1000),
    ("pn_alto_d", TRAMA_BAIXO,
     ((681, 0, 0, 7), (682, 0, 0, 7), (684, 0, 0, 7), (685, 0, 0, 7)), 0x1000),
    ("pn_baixo_e", TRAMA_BAIXO,
     ((686, 0, 0, 7), (687, 0, 0, 7), (689, 0, 0, 7), (690, 0, 0, 7)), 0x1000),
    ("pn_baixo_m", TRAMA_BAIXO,
     ((687, 0, 0, 7), (687, 0, 0, 7), (690, 0, 0, 7), (690, 0, 0, 7)), 0x1000),
    ("pn_baixo_d", TRAMA_BAIXO,
     ((687, 0, 0, 7), (688, 0, 0, 7), (690, 0, 0, 7), (691, 0, 0, 7)), 0x1000),
    # ---- o arbusto, par de duas celulas, SOLIDO ----
    ("arbusto_e", TRAMA_BAIXO,
     ((38, 0, 0, 0), (39, 0, 0, 0), (54, 0, 0, 0), (55, 0, 0, 0)), 0x1000),
    ("arbusto_d", TRAMA_BAIXO,
     ((39, 1, 0, 0), (38, 1, 0, 0), (55, 1, 0, 0), (54, 1, 0, 0)), 0x1000),
    # ---- a trama ESPELHADA, o calcamento da avenida (piso, ANDAVEL) ----
    ("trama_espelho", TRAMA_ESPELHO, VAZIO, 0x0000),
]

# Pecas que JA existem no tileset e que esta passada so espalha pelo mapa.
BALIZA = 944          # par de balizas de amarracao sobre a trama, COVERED
PERNA_E = 893         # perna esquerda do painel, ja desenhada sobre o tijolo
PERNA_D = 892         # perna direita
# O pe do guarda-sol JA existe desenhado sobre o tijolo, e o cais novo e de
# tijolo: nao ha peca nova para ele. O 882 tem a arte na METADE DIREITA da
# celula e o 880 na esquerda, entao o par vai na ordem 882 (celula da esquerda)
# e 880 (celula da direita), com o mastro nascendo na juncao das duas.
PE_E = 882
PE_D = 880

# --------------------------------------------------------------- a PLANTA
# Toda coordenada e (coluna, linha) e foi conferida contra o `map.bin` do
# master: `_valida` reprova a rodada inteira se qualquer celula alvo nao for a
# trama 905 hoje, ou se uma celula que vira solida tiver evento em cima.

# O cais: faixas (linha, coluna inicial, coluna final), inclusive nas pontas.
CAIS = [(48, 6, 32), (49, 9, 32), (46, 18, 22), (47, 18, 22)]
# Os bueiros, dentro do cais.
BUEIROS = [(15, 49, "cais_bueiro_e"), (27, 49, "cais_bueiro_d"), (24, 48, "cais_bueiro_e")]
# Guarda-sois: (coluna da celula esquerda, linha da copa alta, cor).
GUARDA_SOIS = [(7, 46, "am"), (10, 46, "az")]
# O painel do porto: coluna esquerda e linha de cima do toldo. As pernas caem
# na linha de baixo, ja dentro do cais.
PAINEL = (14, 46)
# Balizas de amarracao, celula a celula.
BALIZAS = [(6, 47), (9, 47), (17, 47), (30, 44), (30, 46), (19, 42)]
# A AVENIDA em espinha de peixe: todo o que ainda for trama 905 dentro deste
# retangulo vira a trama ESPELHADA. Ele para na linha 45 porque as linhas 46 e
# 47 desta faixa ja sao a lingua do cais.
AVENIDA = (18, 22, 15, 45)
# Arbustos: (coluna da celula esquerda, linha). Ocupa duas celulas.
ARBUSTOS = [(12, 46), (18, 24), (18, 28), (10, 29), (20, 39), (28, 42), (31, 43)]


# ------------------------------------------------------- leitura do que e nosso
def _layouts(_c={}):
    if not _c:
        d = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
        _c.update({l["id"]: l for l in d["layouts"] if l.get("id")})
    return _c


def layout_de(mapa):
    d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json"))
    return _layouts()[d["layout"]], d


def _ler(nome):
    """O arquivo como esta na arvore AGORA. So a conferencia usa isso."""
    return open(f"{DESTINO}/{nome}", "rb").read()


def _base(rel, _c={}):
    """O arquivo como esta no commit de REFERENCIA. E daqui que o plano sai."""
    if rel not in _c:
        _c[rel] = subprocess.check_output(["git", "-C", RAIZ, "show", f"{REF}:{rel}"])
    return _c[rel]


def _base_sec(nome):
    return _base(f"data/tilesets/secondary/olivine_city/{nome}")


def grade(mapa, base=True):
    """O `map.bin` do mapa. `base=True` le o commit de referencia, que e o que o
    PLANO usa; `base=False` le a arvore, que e o que a CONFERENCIA usa."""
    L, d = layout_de(mapa)
    W, H = L["width"], L["height"]
    b = (_base(L["blockdata_filepath"]) if base
         else open(f"{RAIZ}/{L['blockdata_filepath']}", "rb").read())
    return list(struct.unpack_from("<%dH" % (W * H), b, 0)), W, H, L, d


def eventos(d):
    s = set()
    for chave in ("object_events", "warp_events", "bg_events", "coord_events"):
        for e in d.get(chave) or []:
            s.add((e["x"], e["y"]))
    return s


def _metas_sec(_c={}):
    if not _c:
        b = _base_sec("metatiles.bin")
        _c["b"] = b
        _c["n"] = len(b) // 16
    return _c


def usados_pelos_irmaos(_c={}):
    """Todo metatile que qualquer um dos dois mapas do tileset escreve."""
    if not _c:
        u = collections.Counter()
        for mapa in IRMAOS:
            v, W, H, _, _ = grade(mapa)
            for c in v:
                u[c & 0x3FF] += 1
        _c.update(u)
    return _c


def vagas_mortas(_c=[]):
    """Vaga local do secundario que ninguem escreve E que so tem grama de
    preenchimento. As duas condicoes juntas, nunca uma so: a primeira sozinha
    deixaria escrever por cima de arte boa (o guarda-sol desta passada saiu
    justamente de vaga NAO usada e com arte), e a segunda sozinha deixaria
    escrever numa grama que a `Route40` desenha."""
    if _c:
        return _c
    m = _metas_sec()
    b, n = m["b"], m["n"]
    u = usados_pelos_irmaos()
    for i in range(n):
        if u.get(N_META_PRI + i, 0):
            continue
        ws = struct.unpack_from("<8H", b, i * 16)
        baixo = tuple(w & 0x3FF for w in ws[:4])
        pal = tuple((w >> 12) & 0xF for w in ws[:4])
        if baixo == GRAMA_MORTA and pal == (0, 0, 0, 0) and not any(ws[4:]):
            _c.append(i)
    return _c


def catalogo(_c={}):
    """Cada peca do CATALOGO com a vaga (local e id global) em que ela mora."""
    if _c:
        return _c
    mortas = vagas_mortas()
    if len(mortas) < len(CATALOGO):
        raise SystemExit("so ha %d vagas mortas para %d pecas"
                         % (len(mortas), len(CATALOGO)))
    for k, (nome, baixo, cima, attr) in enumerate(CATALOGO):
        local = mortas[k]
        _c[nome] = {"nome": nome, "local": local, "id": N_META_PRI + local,
                    "entradas": entradas(baixo, cima), "attr": attr}
    return _c


# --------------------------------------------------------------- o PLANO
def _celulas():
    """{(x, y): (metatile, colisao)} de tudo que esta passada escreve."""
    c = catalogo()
    fora = {}

    def po(x, y, nome_ou_id, solido):
        mid = nome_ou_id if isinstance(nome_ou_id, int) else c[nome_ou_id]["id"]
        if (x, y) in fora:
            raise SystemExit("duas pecas disputam a celula (%d,%d)" % (x, y))
        fora[(x, y)] = (mid, 1 if solido else 0)

    # 1. o cais de pedra
    especial = {(x, y): nome for x, y, nome in BUEIROS}
    for linha, c0, c1 in CAIS:
        for x in range(c0, c1 + 1):
            po(x, linha, especial.get((x, linha), "cais"), False)

    # 2. os guarda-sois
    for x, y, cor in GUARDA_SOIS:
        po(x, y, f"gs_{cor}_alto_e", False)
        po(x + 1, y, f"gs_{cor}_alto_d", False)
        po(x, y + 1, f"gs_{cor}_baixo_e", False)
        po(x + 1, y + 1, f"gs_{cor}_baixo_d", False)
        # o pe cai na linha do cais novo, entao ele e a peca de tijolo que o
        # tileset ja tinha, e nao uma peca nova sobre a trama
        fora.pop((x, y + 2), None)
        fora.pop((x + 1, y + 2), None)
        po(x, y + 2, PE_E, True)
        po(x + 1, y + 2, PE_D, True)

    # 3. o painel do porto. As pernas sobrescrevem duas celulas do cais, e por
    #    isso entram DEPOIS dele e com `fora.pop`, nao com `po`: a colisao delas
    #    e que muda, e o cais ja tinha escrito ali.
    px, py = PAINEL
    for k, suf in enumerate(("e", "m", "d")):
        po(px + k, py, f"pn_alto_{suf}", True)
        po(px + k, py + 1, f"pn_baixo_{suf}", True)
    for x, perna in ((px, PERNA_E), (px + 2, PERNA_D)):
        fora.pop((x, py + 2), None)
        po(x, py + 2, perna, True)

    # 4. as balizas
    for x, y in BALIZAS:
        po(x, y, BALIZA, True)

    # 5. os arbustos
    for x, y in ARBUSTOS:
        po(x, y, "arbusto_e", True)
        po(x + 1, y, "arbusto_d", True)

    # 6. a avenida em espinha de peixe. Ela entra POR ULTIMO e so em celula
    #    livre: onde ja ha guarda-sol, painel, baliza, arbusto ou cais, quem
    #    manda e a peca, e o piso dela e o proprio desenho da peca.
    v, W, H, _, _ = grade(ALVO)      # do commit de referencia, ver REF
    x0, x1, y0, y1 = AVENIDA
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (x, y) in fora:
                continue
            if (v[y * W + x] & 0x3FF) == TRAMA and not ((v[y * W + x] >> 10) & 3):
                po(x, y, "trama_espelho", False)
    return fora


def _valida(v, W, H, d, fora):
    """Reprova ANTES de gravar. Cada item aqui ja quebrou uma rodada em alguma
    cidade desta onda."""
    ev = eventos(d)
    mau = []
    for (x, y), (mid, col) in sorted(fora.items()):
        if not (0 <= x < W and 0 <= y < H):
            mau.append("(%d,%d) fora do mapa" % (x, y))
            continue
        antes = v[y * W + x]
        if (antes & 0x3FF) != TRAMA:
            mau.append("(%d,%d) hoje e o metatile %d, nao a trama %d"
                       % (x, y, antes & 0x3FF, TRAMA))
        if ((antes >> 10) & 3) != 0:
            mau.append("(%d,%d) hoje ja e solida" % (x, y))
        if col and (x, y) in ev:
            mau.append("(%d,%d) tem evento em cima e viraria solida" % (x, y))
    if mau:
        raise SystemExit("PLANTA REPROVADA:\n  " + "\n  ".join(mau))


def plano():
    v, W, H, L, d = grade(ALVO)
    fora = _celulas()
    _valida(v, W, H, d, fora)
    return v, W, H, L, d, fora


# --------------------------------------------------------------- a REGUA
# Familia visual: ids diferentes que desenham o MESMO chao. E o antidoto contra
# comprar nota com duplicata (ver o paragrafo do 449 no cabecalho).
def familia_visual(metas_novos=None):
    """{id: id representante} para os metatiles de CHAO desta cidade."""
    fam = {}
    c = catalogo()
    # a trama pura: o 905 do secundario, o 449 do primario e todo id novo cuja
    # camada de baixo seja a trama e a de cima esteja vazia.
    for mid in (905, 449, 660, 661, 662, 663, 668, 669):
        fam[mid] = 905
    for peca in c.values():
        cima = peca["entradas"][4:]
        baixo = tuple(w & 0x3FF for w in peca["entradas"][:4])
        if not any(cima):
            if baixo in (tuple(t[0] for t in TRAMA_BAIXO),
                         tuple(t[0] for t in TRAMA_ESPELHO)):
                fam[peca["id"]] = 905
            elif set(baixo) <= {700, 701}:
                fam[peca["id"]] = TIJOLO
    fam[TIJOLO] = TIJOLO
    for mid in (816, 817, 867, 875, 881, 883, 888, 889, 890, 891):
        fam[mid] = TIJOLO
    return fam


def regua(v, W, H, metas_novos=None, attrs_novos=None):
    """As duas contas: por ID (o que a `regua_cidades.py` mede) e por FAMILIA."""
    import enfeita_cidades
    ag = enfeita_cidades.agua()
    apri = struct.unpack("<640H", open(
        f"{RAIZ}/data/tilesets/primary/johto_general/metatile_attributes.bin", "rb").read())
    b = (bytearray(_ler("metatile_attributes.bin")) if attrs_novos is None
         else attrs_novos)
    asec = struct.unpack("<%dH" % (len(b) // 2), bytes(b))

    def attr(m):
        return apri[m] if m < N_META_PRI else (
            asec[m - N_META_PRI] if m - N_META_PRI < len(asec) else 0)

    andaveis = [c & 0x3FF for c in v
                if not ((c >> 10) & 3) and (attr(c & 0x3FF) & 0xFF) not in ag]
    freq = collections.Counter(andaveis)
    fam = familia_visual()
    ffam = collections.Counter(fam.get(m, m) for m in andaveis)
    n = len(andaveis)
    return {"andaveis": n,
            "id_top": freq.most_common(1)[0],
            "id_pct": round(freq.most_common(1)[0][1] * 100.0 / n, 1),
            "fam_top": ffam.most_common(1)[0],
            "fam_pct": round(ffam.most_common(1)[0][1] * 100.0 / n, 1),
            "freq": freq, "ffam": ffam}


# --------------------------------------------------------------- a GRAVACAO
def grava_tileset():
    """Escreve metatiles.bin e metatile_attributes.bin A PARTIR DA REFERENCIA.
    Nenhum dos dois muda de TAMANHO, e o `tiles.png` nem e aberto: esta passada
    nao tem pixel novo."""
    meta = bytearray(_base_sec("metatiles.bin"))
    attr = bytearray(_base_sec("metatile_attributes.bin"))
    n0, a0 = len(meta), len(attr)
    mortas = set(vagas_mortas())
    for peca in catalogo().values():
        local = peca["local"]
        if local not in mortas:
            raise SystemExit("a vaga %d nao esta morta: escrever nela quebraria "
                             "a Route40" % (local + N_META_PRI))
        for i, w in enumerate(peca["entradas"]):
            struct.pack_into("<H", meta, local * 16 + i * 2, w)
        struct.pack_into("<H", attr, local * 2, peca["attr"])
    if len(meta) != n0 or len(attr) != a0:
        raise SystemExit("os binarios de metatile mudaram de tamanho")
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))
    return len(catalogo())


def grava_mapa(v, W, H, L, fora):
    novo = list(v)
    for (x, y), (mid, col) in fora.items():
        i = y * W + x
        p = novo[i]
        novo[i] = (mid & 0x3FF) | (col << 10) | (p & 0xF000)
    b = struct.pack("<%dH" % (W * H), *novo)
    caminho = f"{RAIZ}/{L['blockdata_filepath']}"
    if len(b) != os.path.getsize(caminho):
        raise SystemExit("o map.bin mudaria de tamanho")
    open(caminho, "wb").write(b)
    return novo


def roda(aplicar):
    v, W, H, L, d, fora = plano()
    antes = regua(v, W, H)
    novo = list(v)
    for (x, y), (mid, col) in fora.items():
        i = y * W + x
        novo[i] = (mid & 0x3FF) | (col << 10) | (v[i] & 0xF000)
    # a regua do DEPOIS precisa dos atributos novos ja em memoria
    attrs = bytearray(_base_sec("metatile_attributes.bin"))
    for peca in catalogo().values():
        struct.pack_into("<H", attrs, peca["local"] * 2, peca["attr"])
    depois = regua(novo, W, H, attrs_novos=attrs)
    solidas = sum(1 for _, (_, c) in fora.items() if c)
    print("%s  %dx%d" % (ALVO, W, H))
    print("  pecas novas de metatile ....... %d (vagas mortas, arquivo do mesmo tamanho)"
          % len(catalogo()))
    print("  vagas mortas disponiveis ...... %d" % len(vagas_mortas()))
    print("  celulas mudadas ............... %d" % len(fora))
    print("  celulas solidificadas ......... %d" % solidas)
    print("  carimbo por ID:      %d (%d celulas de %d, %.1f%%)  ->  %d (%d de %d, %.1f%%)"
          % (antes["id_top"][0], antes["id_top"][1], antes["andaveis"], antes["id_pct"],
             depois["id_top"][0], depois["id_top"][1], depois["andaveis"], depois["id_pct"]))
    print("  carimbo por FAMILIA: %d (%d celulas, %.1f%%)  ->  %d (%d, %.1f%%)"
          % (antes["fam_top"][0], antes["fam_top"][1], antes["fam_pct"],
             depois["fam_top"][0], depois["fam_top"][1], depois["fam_pct"]))
    if not aplicar:
        print("\n(nada gravado; use --aplicar)")
        return 0
    grava_tileset()
    grava_mapa(v, W, H, L, fora)
    json.dump({"mapa": ALVO,
               "pecas": {n: p["id"] for n, p in catalogo().items()},
               "celulas": ["%d,%d,%d,%d" % (x, y, m, c)
                           for (x, y), (m, c) in sorted(fora.items())],
               "carimbo_antes_id": antes["id_pct"], "carimbo_depois_id": depois["id_pct"],
               "carimbo_antes_familia": antes["fam_pct"],
               "carimbo_depois_familia": depois["fam_pct"]},
              open(PLANO, "w"), indent=1, ensure_ascii=False)
    print("\ngravado. plano em %s" % PLANO)
    return 0


def desfaz():
    _base.__defaults__[0].clear() if _base.__defaults__ else None
    alvos = ["data/layouts/OlivineCity/map.bin",
             "data/tilesets/secondary/olivine_city/metatiles.bin",
             "data/tilesets/secondary/olivine_city/metatile_attributes.bin"]
    subprocess.check_call(["git", "-C", RAIZ, "checkout", REF, "--"] + alvos)
    if os.path.exists(PLANO):
        os.remove(PLANO)
    print("desfeito: %s" % ", ".join(alvos))
    return 0


def confere():
    v, W, H, L, d = grade(ALVO, base=False)
    r = regua(v, W, H)
    print("%s: %d celulas andaveis a pe" % (ALVO, r["andaveis"]))
    print("  por ID      : %d com %d celulas, %.1f%%" % (r["id_top"][0], r["id_top"][1], r["id_pct"]))
    print("  por FAMILIA : %d com %d celulas, %.1f%%" % (r["fam_top"][0], r["fam_top"][1], r["fam_pct"]))
    for m, n in r["freq"].most_common(8):
        print("      id %4d %4d" % (m, n))
    return 0 if max(r["id_pct"], r["fam_pct"]) < TETO_REGUA else 1


# ------------------------------------------------------------------- auto-teste
def demo():
    """Auto-teste do bloco T205. Nao checa beleza: checa que a passada sabe
    REPROVAR, e que as contas que o relatorio afirma sao as do arquivo."""
    falhas = []

    def caso(n, cond, msg):
        print("  T205.%d %s %s" % (n, "ok  " if cond else "FALHA", msg))
        if not cond:
            falhas.append(n)

    v, W, H, L, d = grade(ALVO, base=False)     # a arvore de HOJE
    r = regua(v, W, H)
    aplicado = os.path.exists(PLANO)

    # 1. A regua da arvore de HOJE, medida no arquivo e nao no plano.
    if aplicado:
        caso(1, r["id_pct"] < TETO_REGUA and r["fam_pct"] < TETO_REGUA,
             "carimbo por id %.1f%% e por familia %.1f%%, os dois abaixo de %.0f%%"
             % (r["id_pct"], r["fam_pct"], TETO_REGUA))
    else:
        caso(1, abs(r["id_pct"] - 22.4) < 0.2,
             "master ainda: o carimbo mede %.1f%% (o master mede 22,4%%)" % r["id_pct"])

    # 2. A trama e CONTINUA, e a diagonal dela so aceita DUAS montagens: a
    #    canonica e o ESPELHO HORIZONTAL do metatile inteiro (que inverte a
    #    diagonal e casa em espinha de peixe). Qualquer outra permutacao dos
    #    quatro tiles rompe a linha no meio da celula e le como defeito. Este
    #    caso varre as pecas que ESTA passada escreve, uma a uma.
    canon = tuple((t[0], t[1]) for t in TRAMA_BAIXO)
    espelho = tuple((t[0], t[1]) for t in TRAMA_ESPELHO)
    c = catalogo()
    tortas = []
    for peca in c.values():
        baixo = tuple(((w & 0x3FF), (w >> 10) & 1) for w in peca["entradas"][:4])
        if {t[0] for t in baixo} == {t[0] for t in canon} and baixo not in (canon, espelho):
            tortas.append(peca["nome"])
    caso(2, not tortas,
         "as %d pecas desta passada so usam a trama na ordem canonica ou no espelho "
         "horizontal: %s" % (len(c), tortas or "nenhuma torta"))

    # 3. Vaga morta e vaga morta MESMO: nenhuma das 14 que so a Route40 usa
    #    entrou na lista, e nenhuma vaga com arte entrou.
    u = usados_pelos_irmaos()
    mortas = set(vagas_mortas())
    invasao = [N_META_PRI + i for i in mortas if u.get(N_META_PRI + i, 0)]
    caso(3, not invasao and len(mortas) >= len(CATALOGO),
         "%d vagas mortas, nenhuma usada por Olivine ou Route40 (%s)"
         % (len(mortas), invasao or "ok"))

    # 4. O CONTRARIO dos casos de solidez: o cais novo continua ANDAVEL, e o
    #    atributo dele e identico ao da trama que ele substituiu.
    c = catalogo()
    piso = [c[n] for n in ("cais", "cais_bueiro_e", "cais_bueiro_d",
                           "gs_am_alto_e", "gs_am_alto_d", "gs_am_baixo_e",
                           "gs_am_baixo_d", "gs_az_alto_e", "gs_az_alto_d",
                           "gs_az_baixo_e", "gs_az_baixo_d")]
    caso(4, all(p["attr"] == 0x0000 for p in piso),
         "as %d pecas de piso e de copa entram com atributo 0x0000, igual ao 905"
         % len(piso))

    # 5. Todo movel e COVERED. NORMAL poria a camada de cima no BG1 e o jogador
    #    andaria por dentro do cenario (o defeito E3 do mapas_qa).
    movel = [p for p in c.values() if p["attr"] != 0x0000]
    caso(5, movel and all(p["attr"] & 0xF000 == LAYER_COVERED for p in movel),
         "as %d pecas de movel sao COVERED" % len(movel))

    # 6. A AGUA de Surf nao foi tocada. Nenhuma celula do plano cai em celula de
    #    comportamento de agua, e a contagem de agua do mapa nao mudou.
    import enfeita_cidades
    ag = enfeita_cidades.agua()
    apri = struct.unpack("<640H", open(
        f"{RAIZ}/data/tilesets/primary/johto_general/metatile_attributes.bin", "rb").read())
    asec = struct.unpack("<%dH" % (len(_ler("metatile_attributes.bin")) // 2),
                         _ler("metatile_attributes.bin"))
    beh = lambda m: (apri[m] if m < N_META_PRI else asec[m - N_META_PRI]) & 0xFF
    # A agua e o risco numero um desta cidade (Surf), e o numero nao pode ser
    #    magico: ele sai do MASTER, lido do git, e nao de constante escrita a
    #    mao. Compara-se o CONJUNTO de celulas de agua, nao so a contagem.
    velho = struct.unpack("<%dH" % (W * H), _base("data/layouts/OlivineCity/map.bin"))
    agua_antes = {i for i, cel in enumerate(velho) if beh(cel & 0x3FF) in ag}
    agua_agora = {i for i, cel in enumerate(v) if beh(cel & 0x3FF) in ag}
    fora = _celulas()
    toca_agua = [xy for xy in fora if beh(velho[xy[1] * W + xy[0]] & 0x3FF) in ag]
    caso(6, not toca_agua and agua_antes == agua_agora,
         "as %d celulas de comportamento de agua sao AS MESMAS do master, celula a "
         "celula, e o plano nao toca nenhuma" % len(agua_agora))

    # 7. A planta do plano bate com o arquivo. Antes de aplicar, toda celula
    #    alvo e a trama; depois, nenhuma delas e mais a trama 905.
    alvo_trama = [xy for xy in fora if (v[xy[1] * W + xy[0]] & 0x3FF) == TRAMA]
    if aplicado:
        caso(7, not alvo_trama,
             "as %d celulas do plano sairam da trama" % len(fora))
    else:
        caso(7, len(alvo_trama) == len(fora),
             "as %d celulas do plano sao trama 905 no master" % len(fora))

    print("DEMO VERDE" if not falhas else "DEMO VERMELHA nos casos %s" % falhas)
    return 1 if falhas else 0


def main():
    a = sys.argv[1:]
    if "--demo" in a:
        return demo()
    if "--desfazer" in a:
        return desfaz()
    if "--confere" in a:
        return confere()
    return roda("--aplicar" in a)


if __name__ == "__main__":
    sys.exit(main())
