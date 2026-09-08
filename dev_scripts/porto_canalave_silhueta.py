#!/usr/bin/env python3
"""Dá a Canalave a SILHUETA de porto: farol, veleiros e engradados.

O `porto_canalave.py` (rodada 13) resolveu a água com o bote e os tambores de
Slateport. O `porto_canalave_arte.py` resolveu a BEIRA com os cabeços de
amarração do Golden Glazed. Sobrou o que se vê de LONGE, e é justamente isso que
faz uma cidade parecer porto: o farol e o barco grande atracado. Canalave não
tinha nada disso, e a razão não era gosto nem preguiça, era ORÇAMENTO DE
PALETA.

O QUE DESTRAVOU. O motor tem `NUM_PALS_TOTAL 13` (`include/fieldmap.h`), ou
seja, sete vagas de paleta para o secundário no layout `emerald`, da 6 à 12.
Canalave gastava as sete e a rodada anterior teve que espremer o kit inteiro do
cais em UMA vaga de 15 cores. O `dev_scripts/compacta_paletas.py`, do commit
anterior, reempacotou as sete vagas em quatro sem aproximar uma cor sequer
(53 cores cabiam em 60 lugares) e devolveu as vagas 10, 11 e 12. Este script
gasta as três.

A FRENTE ANTERIOR TENTOU O CAMINHO CARO E REPROVOU. Ela trocou o PAR INTEIRO de
tilesets de Canalave pelo do GS Chronicles para ganhar espaço: o carimbo
dominante da cidade subiu de 26,9% para 83,7% e os 224 metatiles do mapa caíram
para 82, com árvore e calçada de losango sem par. O laudo está em
`amostras-tileset/refino/porto2-reprova/`. Compactar paleta ganha o mesmo espaço
e não tira um pixel do lugar, o que o render antes/depois do commit anterior
provou com 0 pixel de diferença em 622.592.

AS TRÊS PEÇAS, E O QUE CADA UMA CUSTA. Medido tile a tile e cor a cor, não
estimado:

  vaga 10  VELEIRO     15 cores, 16 células   Golden Glazed 0x3DF92C
  vaga 11  FAROL       15 cores, 39 células   Golden Glazed 0x3DF92C
  vaga 12  ENGRADADO    5 cores, 24 células   Scorched Silver 0x4929B4

O PÓRTICO DE DOCA EXISTE, FOI INSTALADO, E FOI TIRADO. Ele é real: o secundário
`0x4929B4` do Scorched Silver tem um pórtico completo em aço vermelho, com duas
torres treliçadas, viga de travessa e gancho, por 6 cores e 22 tiles, e a prova
está em `amostras-tileset/refino/guindaste-scorched-silver.png`. Ele entrou na
baía do norte em (13, 7) e o render mostrou o defeito: as duas torres treliçadas
terminam em MAR ABERTO, sem nada embaixo. Pórtico de doca corre sobre trilho no
cais, não flutua, e na fonte ele está exatamente assim, com as pernas no
concreto entre duas darsenas. Guindaste bonito na água lê como bug, não como
arte, então ele saiu do mapa e do kit.

AS TRÊS SAÍDAS FORAM MEDIDAS, E AS TRÊS REPROVAM. Nenhuma foi descartada de
cabeça:

  1. MUDAR DE LUGAR. Varridas as 1.980 posições do mapa de 38x64 para uma peça
     de 6x5. Só 17 põem os DOIS pés fora da água com todas as células
     sobreponíveis; 16 dessas 17 esbarram em célula já desenhada por outra
     ferramenta, em evento ou no corredor da balsa. Sobra UMA, (6, 21), no
     largo oeste, e o portão do próprio script a recusa: as duas torres
     cortam o largo e os COMPONENTES de chão andável sobem de 8 para 9. Não
     existe posição em que o pé caia sobre concreto JÁ SÓLIDO: toda borda de
     cais deste mapa (517, 526, 563, 568, 569, 570, 400, 402) desenha na
     camada de CIMA, e a regra de acréscimo proíbe apagar isso.
  2. ATRAVESSAR O CANAL, que é a pose da fonte e pediria só alargar a viga de
     6 para 8 células. Morre na geometria: o cais leste, x=20, tem POSTE de luz
     (metatile 816) nas linhas 16, 19 e 22, e a maior corrida limpa de 525 é de
     DUAS linhas, contra as CINCO que a torre precisa. O cais oeste, x=13, é
     526 de ponta a ponta e nunca é sobreponível.
  3. PÔR CHÃO EMBAIXO DAS PERNAS. O cais do `0x4929B4` não vem: as dezessete
     células de cais e beira dele (112, 114, 121, 122, 393, 400, 402, 408, 410,
     44, 60, 593, 664, 666, 672, 673, 674) dão 0 de 4 quadrantes sob a regra do
     primário, porque a fonte pinta o cais dela com a paleta do PRIMÁRIO dela:
     é chão dela, não é peça. Quebrando a regra e levando o chão cru, uma
     plataforma mínima na água (piso 593, meios-fios 664 e 666, e as duas
     beiras que encostam na água, 112 e 114) custa 13 cores, 12 delas NOVAS,
     para as 4 vagas livres da paleta 12. Só o piso e os meios-fios já custam 6
     cores, 5 novas: falta UMA, a mesma conta da passarela.

O QUE FICOU DE FORA, E POR QUÊ. O CAIS DE MADEIRA do Golden Glazed foi pedido
junto com o veleiro e o farol, e não coube, e o número é este: o cais inteiro
custa 12 cores; as três células caras dele (os metatiles 722, 723 e 724, a
sombra debaixo do deque, na paleta 10 da fonte) sozinhas levam 7 dessas 12, e
sem elas sobra uma passarela magra de 5 cores. Enquanto o pórtico estava na
vaga 12 ela não cabia: pórtico (6) mais engradado (5) mais passarela (5) dá 16
cores para 15 lugares, e faltava UMA. Com o pórtico fora, a vaga 12 usa 5 das
15 e a passarela CABE, com 5 cores de folga. Ela continua de fora porque este
commit é um conserto pontual e não uma frente de arte nova; a conta fica aqui
pronta para a próxima.

A escolha entre a passarela e o engradado não foi de gosto, foi de PORTÃO. A
régua da onda é o carimbo dominante da cidade, medido pela
`dev_scripts/regua_cidades.py`, e ela conta só célula ANDÁVEL: o metatile 521
ocupava 198 das 736 andáveis, 26,9%, e o teto de reprovação é 25%. Farol,
veleiro e passarela moram todos na ÁGUA, que não é andável e não entra no
denominador: com eles instalados o carimbo continuava exatos 26,9%, e a rodada
reprovava com a cidade linda. É também por isso que tirar o pórtico não mexe no
carimbo: ele morava na água. O engradado é a única peça que pisa em
calçada. Com seis montes de 2 por 2 o carimbo cai para 24,4% de 712. Por isso
ele entrou e a passarela ficou de fora, com o custo dela anotado aqui para a
próxima frente, que só precisa de 1 cor livre em qualquer vaga.

A REGRA DE MONTAGEM, e a armadilha que ela resolve. A camada de BAIXO do
metatile novo é a do CHÃO DE CANALAVE, igual à célula que estava ali, e a de
CIMA é a peça. Só que a fonte nem sempre desenha a peça na camada de cima: o
Golden Glazed desenhou a porta e a saia do farol (os metatiles 826, 827, 833,
834 e 835) só na camada de BAIXO dele. Instalado do jeito ingênuo, o farol
saía com buracos de água no meio da base, e isso foi visto no render, não
deduzido. A regra é: **o quadrante de baixo SOBE quando o de cima está vazio**.
E o contrário também vale: quadrante que a fonte pinta com uma paleta do
PRIMÁRIO dela é o chão dela, não é peça, e não vem; no lugar dele fica o nosso
chão. Foi assim que o veleiro fechou em 15 cores exatas: o único quadrante de
paleta primária dele (o tile 446 no metatile 665, uma sombra de água) ficou de
fora e a espuma do nosso canal aparece no lugar.

O ATRIBUTO do metatile novo é COPIADO INTEIRO do metatile antigo, então
`behavior` e `layerType` da célula não mudam nem por um bit, e a suíte não tem
como reclamar de comportamento.

COLISÃO: o que muda, e por que é seguro.
  - O casco do veleiro e a base do farol viram SÓLIDOS (colisão 0 para 1)
    porque estão em cima de ÁGUA, que nunca foi andável a pé.
  - O engradado também vira sólido, e esse pisa em CALÇADA. É o único caso em
    que uma célula andável some, e por isso ele passa por dois portões, não um:
    nenhuma outra célula pode sair do alcance a pé além das que o monte ocupa, e
    o número de COMPONENTES de chão andável não pode subir. O segundo portão não
    é decoração: medido em 06/09/2026, um dos candidatos do sudoeste fechava um
    bolso de calçada e levava os componentes de 8 para 9. Ele foi recusado pela
    própria heurística, que testa monte a monte antes de aceitar.
  - O alcance por ÁGUA muda no óbvio (a célula ocupada deixa de ser água), e a
    conferência exige exatamente isso e nada mais: nenhuma célula de água que
    sobrou pode ficar inalcançável. Se alguma ficasse, o script RECUSA em vez de
    afogar uma rota de surf.
  - Colisão 1 para 0 em ZERO células, sempre, e a conferência mede.

ONDE CADA PEÇA ENCOSTA, e por que ali. As âncoras são FIXAS, escritas em
`POSICOES` logo abaixo, e não heurísticas: são três estruturas grandes num mapa
de geometria muito específica, e escolher a dedo é mais revisável do que uma
regra que ninguém consegue conferir de cabeça.
  - farol na baía do norte, encostado na costa oeste, onde há 5 por 9 de água
    aberta e o pé do farol cai exatamente na linha de terra. Ele é o contrário
    do pórtico e é por isso que fica: a linha de baixo dele é uma SAIA de
    concreto desenhada na própria arte, que encosta no muro da costa, e não uma
    perna solta.
  - dois veleiros na mesma baía, um de cada lado do eixo, longe do farol. Barco
    em cima da água está certo: barco flutua.
  - engradados espalhados pela calçada perto da água, pela regra de
    `_postos_engradado`, que é a única peça sem âncora fixa.

O CORREDOR DE TESTE DA BALSA fica em `x=19`, linhas 33 a 51, e sete casos da
suíte dependem dele. Nada deste kit chega perto: a peça mais ao sul é um
engradado, e a conferência recusa qualquer célula de corredor.

Idempotente: vagas fixas, e o plano guarda o valor ANTIGO de cada célula em
`dev_scripts/porto_canalave_silhueta.json`. Rodar duas vezes dá byte idêntico.

ORDEM: `porto_canalave.py`, `porto_canalave_arte.py`, `compacta_paletas.py`,
depois este.

CRÉDITO: Pokémon Golden Glazed v2.6, do hacker que assina 'Golden', derivado do
Pokémon Glazed de redriders180 e Lucbui; e Pokémon Scorched Silver v1.3, de
Sloo, sobre pokeemerald-expansion da RHH. As fichas estão em
`fontes-mapas/romhacks/golden-glazed/README.md` e
`fontes-mapas/romhacks/scorched-silver/README.md`, e o crédito também está no
`CREDITS.md`. Nenhuma ROM e nenhum dump entram no repo: o que entra é asset
convertido, como manda a regra 1 da seção 4 do PRD-REFINO.

Uso:
    python3 dev_scripts/porto_canalave_silhueta.py             # mede e mostra o plano
    python3 dev_scripts/porto_canalave_silhueta.py --aplicar   # escreve tileset e mapa
    python3 dev_scripts/porto_canalave_silhueta.py --desfazer  # devolve o map.bin
    python3 dev_scripts/porto_canalave_silhueta.py --demo      # auto-teste curto
    python3 dev_scripts/porto_canalave_silhueta.py --autoteste # suíte cheia
    python3 dev_scripts/porto_canalave_silhueta.py --extrair
        remonta o kit lendo as ROMs privadas em fontes-mapas/romhacks/. Só quem
        tem as ROMs roda isso; o resto do mundo usa o kit convertido do JSON.
"""
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

ALVO = "CanalaveCity"
DESTINO = f"{RAIZ}/data/tilesets/secondary/canalave"
PRIMARIO = f"{RAIZ}/data/tilesets/primary/general_sinnoh"
KIT = f"{RAIZ}/dev_scripts/porto_canalave_silhueta_kit.json"
PLANO = f"{RAIZ}/dev_scripts/porto_canalave_silhueta.json"
OUTROS_PLANOS = (f"{RAIZ}/dev_scripts/porto_canalave.json",
                 f"{RAIZ}/dev_scripts/porto_canalave_arte.json",
                 f"{RAIZ}/dev_scripts/enfeita_cidades.json")

META_LOCAL_0 = 320      # primeira vaga de metatile deste kit (o kit do cais vai
                        # ate a 307, e as vagas daqui em diante estao em branco)
BASE_TILE_0 = 192       # primeira vaga de tile (o tiles.png tem 192 em uso)
TETO_TILES = 512
TETO_META = 512

# As fontes. O md5 fica aqui para o kit nunca ser remontado de uma ROM diferente.
FONTES = {
    "golden-glazed": dict(
        arquivo="Pokémon Golden Glazed.gba",
        md5="f602010e5769fc0454fca4cc8eb77a4b",
        primario=0x3DF704, secundario=0x3DF92C,
        autor="'Golden', derivado do Glazed de redriders180 e Lucbui"),
    "scorched-silver": dict(
        arquivo="Pokémon Scorched Silver.gba",
        md5="f7af51cecd3e170cc373fba01753053c",
        primario=0x49240C, secundario=0x4929B4,
        autor="Sloo, sobre pokeemerald-expansion da RHH"),
}

# As pecas, em metatiles da FONTE. `None` e celula vazia da grade retangular.
# `solida` diz quais LINHAS da peca viram colisao 1 quando caem na agua.
PECAS = collections.OrderedDict([
    ("veleiro", dict(fonte="golden-glazed", vaga=10,
                     macicos=(657, 658, 659, 660, 661, 665, 666, 667, 668, 669),
                     grade=[
                         [None, None, 635, None, None],
                         [None, None, 643, 644, None],
                         [None, 650, 651, 652, None],
                         [657, 658, 659, 660, 661],
                         [665, 666, 667, 668, 669],
                     ])),
    ("farol", dict(fonte="golden-glazed", vaga=11, macicos="tudo", grade=[
        [None, 777, 778, 779, None],
        [784, 785, 786, 787, 788],
        [792, 793, 794, 795, 796],
        [None, 801, 802, 803, None],
        [None, 809, 810, 811, None],
        [816, 817, 818, 819, 820],
        [824, 825, 826, 827, 828],
        [832, 833, 834, 835, 836],
        [840, 841, 842, 843, 844],
    ])),
    # o engradado e a unica peca que pisa em CALCADA, e e ela que quebra o
    # carimbo: as outras duas moram na agua e nao entram no denominador da
    # regua_cidades.py, que so conta celula ANDAVEL.
    ("engradado", dict(fonte="scorched-silver", vaga=12, macicos="tudo", grade=[
        [589, 590],
        [597, 598],
    ])),
])

# Onde cada instancia encosta: (peca, x do canto superior esquerdo, y).
POSICOES = [
    ("farol", 5, 1),
    ("veleiro", 20, 1),
    ("veleiro", 25, 4),
]

# O engradado nao tem ancora fixa: ele e ESPALHADO pela calcada, e as regras
# sao estas. Medido no mapa de 38x64: o metatile dominante e o 521 com 198 das
# 736 celulas andaveis, ou 26,9%.
MAX_ENGRADADOS = 8
ESPACO_ENGRADADO = 4        # Chebyshev entre dois montes
DIST_AGUA_ENGRADADO = 8     # engradado e coisa de doca, nao de quintal
FOLGA_EVENTO = 1            # nunca colado num evento

N4 = E.N4


def componentes_de_chao(grade, W, H, beh, AG):
    """Quantos pedaços SEPARADOS de chão andável o mapa tem.

    É o portão que não depende de onde o jogador nasce: se uma peça partir uma
    praça em duas, este número sobe, mesmo que os dois pedaços continuem
    alcançáveis por warps diferentes.
    """
    chao = {i for i in range(len(grade))
            if not ((grade[i] >> 10) & 3) and beh(grade[i] & 0x3FF) not in AG}
    vistos, n = set(), 0
    for i in chao:
        if i in vistos:
            continue
        n += 1
        fila = collections.deque([i])
        vistos.add(i)
        while fila:
            j = fila.popleft()
            x, y = j % W, j // W
            for dx, dy in N4:
                nx, ny = x + dx, y + dy
                k = ny * W + nx
                if 0 <= nx < W and 0 <= ny < H and k in chao and k not in vistos:
                    vistos.add(k)
                    fila.append(k)
    return n


def _par_do_layout():
    L = G.grade(ALVO)[1]
    return L["primary_tileset"], L["secondary_tileset"]


# ------------------------------------------------------------------ utilidades
def _le(caminho):
    with open(caminho, "rb") as f:
        return f.read()


def entradas(bin_meta, local):
    return [struct.unpack_from("<H", bin_meta, local * 16 + i * 2)[0] for i in range(8)]


class Nosso:
    """Os dois tilesets do layout de Canalave, lidos do disco."""

    def __init__(self):
        self.meta_sec = _le(f"{DESTINO}/metatiles.bin")
        self.attr_sec = _le(f"{DESTINO}/metatile_attributes.bin")
        self.meta_pri = _le(f"{PRIMARIO}/metatiles.bin")
        self.attr_pri = _le(f"{PRIMARIO}/metatile_attributes.bin")

    def ent(self, gid):
        if gid >= 512:
            return entradas(self.meta_sec, gid - 512)
        return entradas(self.meta_pri, gid)

    def attr(self, gid):
        if gid >= 512:
            return struct.unpack_from("<H", self.attr_sec, (gid - 512) * 2)[0]
        return struct.unpack_from("<H", self.attr_pri, gid * 2)[0]

    def sobreponivel(self, gid):
        """A camada de cima desta célula pode ser trocada sem perder desenho?

        Vale quando ela está vazia (água, calçada) ou quando ela é igual à de
        baixo, que é o vício do gerador do demake: o mesmo tile desenhado duas
        vezes, o que dá o mesmo pixel com ou sem a camada de cima.
        """
        e = self.ent(gid)
        return all(v == 0 for v in e[4:]) or e[:4] == e[4:]


# ----------------------------------------------------------------- kit de arte
def carrega_kit():
    if not os.path.exists(KIT):
        raise SystemExit("falta %s: rode --extrair" % KIT)
    with open(KIT, encoding="utf-8") as f:
        return json.load(f)


def constroi_kit(saida=KIT):
    """Monta o JSON do kit lendo as ROMs privadas, uma vez, e nunca mais.

    O que sai daqui é asset CONVERTIDO: paleta em RGB, tiles em nibble e a
    posição de cada quadrante. Nenhum byte de ROM entra no repo.
    """
    import hashlib
    ferramentas = ("/Users/duarte/Projetos/pokemon-claude/fontes-mapas/"
                   "romhacks/ferramentas")
    romhacks = os.path.dirname(ferramentas)
    sys.path.insert(0, ferramentas)
    from gbamap import Rom          # noqa: E402

    def cor(bgr):
        return ((bgr & 31) << 3, ((bgr >> 5) & 31) << 3, ((bgr >> 10) & 31) << 3)

    abertas = {}
    for slug, ficha in FONTES.items():
        caminho = os.path.join(romhacks, slug, ficha["arquivo"])
        md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
        if md5 != ficha["md5"]:
            raise SystemExit("%s: md5 %s, esperado %s" % (slug, md5, ficha["md5"]))
        rom = Rom(caminho)
        t1 = rom.parse_tileset(ficha["primario"])
        t2 = rom.parse_tileset(ficha["secundario"])
        if not t1 or not t2:
            raise SystemExit("%s: tileset invalido" % slug)
        pals = []
        for i in range(16):
            fonte = t1 if i < rom.n_pal_pri else t2
            pals.append(struct.unpack_from("<16H", fonte["pal"], i * 32)
                        if len(fonte["pal"]) >= (i + 1) * 32 else (0,) * 16)
        abertas[slug] = (rom, t1, t2, pals)

    def quadrante(slug, mt, q):
        """A entrada que DESENHA o quadrante q, com a regra da subida.

        Camada de cima primeiro; se ela estiver vazia ou for chão da fonte
        (paleta do primário dela), a de baixo sobe; se ela também não servir, o
        quadrante fica vazio e o nosso chão aparece.
        """
        rom, t1, t2, _pals = abertas[slug]
        origem, idx = (t1, mt) if mt < rom.n_meta_pri else (t2, mt - rom.n_meta_pri)
        ents = struct.unpack_from("<8H", origem["meta"], idx * 16)
        for v in (ents[4 + q], ents[q]):
            if (v & 0x3FF) and ((v >> 12) & 0xF) >= rom.n_pal_pri:
                return v
        return None

    def pixels(slug, tid):
        rom, t1, t2, _pals = abertas[slug]
        dados, base = ((t1["tiles"], tid * 32) if tid < rom.n_tiles_pri
                       else (t2["tiles"], (tid - rom.n_tiles_pri) * 32))
        saida = []
        for y in range(8):
            linha = dados[base + y * 4:base + y * 4 + 4]
            saida.append([linha[x >> 1] & 0xF if x % 2 == 0 else linha[x >> 1] >> 4
                          for x in range(8)])
        return saida

    tiles, mapa_tile = [], {}
    paletas, pecas = {}, {}
    for nome, peca in PECAS.items():
        slug, vaga = peca["fonte"], peca["vaga"]
        _rom, _t1, _t2, pals = abertas[slug]
        cores, mapa_cor = paletas.setdefault(vaga, ([], {}))
        celulas = []
        for dy, linha in enumerate(peca["grade"]):
            for dx, mt in enumerate(linha):
                if mt is None:
                    continue
                quadros = []
                for q in range(4):
                    v = quadrante(slug, mt, q)
                    if v is None:
                        quadros.append(None)
                        continue
                    tid, pal = v & 0x3FF, (v >> 12) & 0xF
                    chave = (slug, tid, pal)
                    if chave not in mapa_tile:
                        novo = []
                        for linha_px in pixels(slug, tid):
                            fora = []
                            for c in linha_px:
                                if c == 0:
                                    fora.append(0)
                                    continue
                                rgb = cor(pals[pal][c])
                                if rgb not in mapa_cor:
                                    if len(cores) >= 15:
                                        raise SystemExit(
                                            "a vaga de paleta %d passa de 15 cores "
                                            "na peca %s" % (vaga, nome))
                                    cores.append(rgb)
                                    mapa_cor[rgb] = len(cores)
                                fora.append(mapa_cor[rgb])
                            novo.append(fora)
                        mapa_tile[chave] = len(tiles)
                        tiles.append(novo)
                    quadros.append([mapa_tile[chave], 1 if v & 0x400 else 0,
                                    1 if v & 0x800 else 0])
                macico = (peca["macicos"] == "tudo" or mt in peca["macicos"])
                celulas.append([dx, dy, quadros, 1 if macico else 0])
        pecas[nome] = dict(fonte=slug, vaga=vaga, celulas=celulas,
                           largura=max(len(l) for l in peca["grade"]),
                           altura=len(peca["grade"]))

    kit = dict(
        fontes={s: dict(rom=f["arquivo"], md5=f["md5"], autor=f["autor"],
                        primario="0x%X" % f["primario"],
                        secundario="0x%X" % f["secundario"])
                for s, f in FONTES.items()},
        paletas={str(v): [[0, 0, 0]] + [list(c) for c in cs]
                          + [[0, 0, 0]] * (15 - len(cs))
                 for v, (cs, _m) in paletas.items()},
        tiles=["".join("%x" % c for linha in t for c in linha) for t in tiles],
        pecas=pecas)
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(kit, f, indent=1, ensure_ascii=False)
    print("kit gravado em %s: %d tiles, %d pecas, cores por vaga %s"
          % (saida, len(tiles), len(pecas),
             {v: len(cs) for v, (cs, _m) in sorted(paletas.items())}))
    return kit


# -------------------------------------------------------------- instalacao
def grava_tileset(kit):
    from PIL import Image
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    precisa = BASE_TILE_0 + len(kit["tiles"])
    if precisa > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)" % (TETO_TILES, precisa))
    linhas = (precisa + cols - 1) // cols
    novo = Image.new("P", (antigo.size[0], linhas * 8), 0)
    novo.putpalette(antigo.getpalette())
    novo.paste(antigo, (0, 0))
    px = novo.load()
    for i, hexa in enumerate(kit["tiles"]):
        vaga = BASE_TILE_0 + i
        x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = int(hexa[y * 8 + x], 16)
    novo.save(f"{DESTINO}/tiles.png")
    for vaga, cores in sorted(kit["paletas"].items()):
        with open(f"{DESTINO}/palettes/%02d.pal" % int(vaga), "w", newline="") as f:
            f.write("JASC-PAL\r\n0100\r\n16\r\n")
            for c in cores:
                f.write("%d %d %d\r\n" % tuple(c))


def grava_metatiles(novos, attrs):
    meta = bytearray(_le(f"{DESTINO}/metatiles.bin"))
    attr = bytearray(_le(f"{DESTINO}/metatile_attributes.bin"))
    for local, ent in novos.items():
        for i, valor in enumerate(ent):
            struct.pack_into("<H", meta, local * 16 + i * 2, valor)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    with open(f"{DESTINO}/metatiles.bin", "wb") as f:
        f.write(bytes(meta))
    with open(f"{DESTINO}/metatile_attributes.bin", "wb") as f:
        f.write(bytes(attr))


# ------------------------------------------------------------- passo do mapa
def agua_alcance(v, W, H, AG, beh):
    """Componente de água ligada às bordas do mapa: quem surfa chega."""
    molhada = {i for i in range(W * H)
               if not ((v[i] >> 10) & 3) and beh(v[i] & 0x3FF) in AG}
    ini = [i for i in molhada
           if i % W in (0, W - 1) or i // W in (0, H - 1)
           or any(0 <= (i % W) + dx < W and 0 <= (i // W) + dy < H
                  and ((i // W + dy) * W + (i % W) + dx) not in molhada
                  for dx, dy in N4)]
    vis, fila = set(ini), collections.deque(ini)
    while fila:
        i = fila.popleft()
        x, y = i % W, i // W
        for dx, dy in N4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H:
                j = ny * W + nx
                if j in molhada and j not in vis:
                    vis.add(j)
                    fila.append(j)
    return vis


def _postos_engradado(kit, nosso, v, W, H, d, beh, AG, proibidas, ocupado):
    """Onde os montes de engradado caem. Determinístico, sem aleatoriedade.

    Regra, e cada linha dela tem um motivo:
      - só em bloco 2x2 do metatile DOMINANTE da cidade, porque o alvo da peça
        é justamente esse carimbo e não a variedade em geral;
      - a até `DIST_AGUA_ENGRADADO` células de água, porque engradado é coisa de
        doca;
      - nunca em cima nem colado num evento, nunca em corredor de teste da
        suíte, nunca em célula cuja camada de cima já desenha alguma coisa;
      - espaçados por `ESPACO_ENGRADADO` em Chebyshev, senão viram um muro.
    A ordem é por (distância à água, coordenada), então duas rodadas dão a mesma
    lista.
    """
    andaveis = [i for i in range(W * H)
                if not ((v[i] >> 10) & 3) and beh(v[i] & 0x3FF) not in AG]
    if not andaveis:
        return []
    dominante = collections.Counter(v[i] & 0x3FF for i in andaveis).most_common(1)[0][0]
    molhadas = [(i % W, i // W) for i in range(W * H) if beh(v[i] & 0x3FF) in AG]
    eventos = set(E.eventos(d))

    def perto_da_agua(x, y):
        return any(abs(x - mx) + abs(y - my) <= DIST_AGUA_ENGRADADO
                   for mx, my in molhadas)

    largura = kit["pecas"]["engradado"]["largura"]
    altura = kit["pecas"]["engradado"]["altura"]
    candidatos = []
    for y in range(1, H - altura):
        for x in range(1, W - largura):
            celulas = [(x + a, y + b) for a in range(largura) for b in range(altura)]
            if not all(v[cy * W + cx] & 0x3FF == dominante for cx, cy in celulas):
                continue
            if any(c in proibidas or c in ocupado for c in celulas):
                continue
            if any(abs(cx - ex) + abs(cy - ey) <= FOLGA_EVENTO
                   for cx, cy in celulas for ex, ey in eventos):
                continue
            if not all(nosso.sobreponivel(v[cy * W + cx] & 0x3FF) for cx, cy in celulas):
                continue
            if not perto_da_agua(x, y):
                continue
            dist = min(abs(x - mx) + abs(y - my) for mx, my in molhadas)
            candidatos.append((dist, y, x))
    # e agora o teste que nenhuma regra de espaco pega: o monte nao pode PARTIR
    # a calcada. Medido em 06/09/2026, um dos candidatos do sudoeste fechava um
    # bolso e levava os componentes de chao de 8 para 9. O teste roda por
    # candidato, com o mapa como ele fica DEPOIS dos montes ja aceitos.
    base = componentes_de_chao(v, W, H, beh, AG)
    grade = list(v)
    postos = []
    for _dist, y, x in sorted(candidatos):
        if len(postos) >= MAX_ENGRADADOS:
            break
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENGRADADO for px, py in postos):
            continue
        tentativa = list(grade)
        celulas = [(x + a, y + b) for a in range(largura) for b in range(altura)]
        for cx, cy in celulas:
            tentativa[cy * W + cx] |= 0x0400
        if componentes_de_chao(tentativa, W, H, beh, AG) > base:
            continue
        grade = tentativa
        postos.append((x, y))
    return postos


def plano_mapa(kit, nosso, v, W, H, d):
    """(escolha, proibidas) a partir das âncoras fixas mais os engradados."""
    _ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    proibidas = set(gelo) | set(E.eventos(d))
    escolha = {}     # (x, y) -> (nome da peca, dx, dy)
    beh = G.comportamento(*_par_do_layout())
    AG = E.agua()
    fixas = list(POSICOES)
    reservado = set()
    for nome, ax, ay in fixas:
        for dx, dy, _q, _m in kit["pecas"][nome]["celulas"]:
            reservado.add((ax + dx, ay + dy))
    fixas += [("engradado", x, y) for x, y in
              _postos_engradado(kit, nosso, v, W, H, d, beh, AG, proibidas, reservado)]
    for nome, ax, ay in fixas:
        peca = kit["pecas"][nome]
        for dx, dy, _quadros, _macico in peca["celulas"]:
            x, y = ax + dx, ay + dy
            if not (0 <= x < W and 0 <= y < H):
                raise SystemExit("%s em (%d,%d) sai do mapa" % (nome, ax, ay))
            if (x, y) in proibidas:
                raise SystemExit("%s encosta em evento ou corredor de teste em "
                                 "(%d,%d)" % (nome, x, y))
            if (x, y) in escolha:
                raise SystemExit("duas pecas na mesma celula (%d,%d)" % (x, y))
            if not nosso.sobreponivel(v[y * W + x] & 0x3FF):
                raise SystemExit("%s em (%d,%d) apagaria desenho da camada de "
                                 "cima do metatile %d"
                                 % (nome, x, y, v[y * W + x] & 0x3FF))
            escolha[(x, y)] = (nome, dx, dy)
    return escolha, proibidas


def monta_metatiles(kit, nosso, v, W, escolha, guardado=None):
    """(escritas, metatiles novos, atributos, vagas) a partir da escolha."""
    quadros_de = {}
    for nome, peca in kit["pecas"].items():
        for dx, dy, quadros, macico in peca["celulas"]:
            quadros_de[(nome, dx, dy)] = (quadros, macico)

    pares = sorted({(v[y * W + x] & 0x3FF, chave)
                    for (x, y), chave in escolha.items()})
    if len(pares) + META_LOCAL_0 > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles (%d vagas)"
                         % (TETO_META, len(pares)))
    usados = {c & 0x3FF for c in G.grade(ALVO)[4]}
    meta_can = _le(f"{DESTINO}/metatiles.bin")
    guardado = guardado if guardado is not None else carrega_plano()
    nossas_vagas = {int(k) for k in guardado.get("kit", {}).get("metatiles", {})}

    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    vaga, novos, attrs = {}, {}, {}
    local = META_LOCAL_0
    for chao, chave in pares:
        nome = chave[0]
        pal = kit["pecas"][nome]["vaga"]
        ent_chao = nosso.ent(chao)
        quadros, _macico = quadros_de[chave]
        cima = []
        for quadro in quadros:
            if quadro is None:
                cima.append(0)          # quadrante vazio: o chao aparece inteiro
                continue
            tile_local, hf, vf = quadro
            valor = (512 + BASE_TILE_0 + tile_local) | (pal << 12)
            if hf:
                valor |= 0x400
            if vf:
                valor |= 0x800
            cima.append(valor)
        antigo = entradas(meta_can, local)
        if not enchimento(antigo) and antigo != ent_chao[:4] + cima \
                and local not in nossas_vagas:
            raise SystemExit("vaga de metatile %d ja esta ocupada" % (512 + local))
        if (512 + local) in usados and enchimento(antigo):
            raise SystemExit("o mapa usa o metatile %d" % (512 + local))
        novos[local] = ent_chao[:4] + cima
        attrs[local] = nosso.attr(chao)      # behavior E layerType, inteiros
        vaga[(chao, chave)] = 512 + local
        local += 1

    escritas = {}
    for (x, y), chave in sorted(escolha.items()):
        i = y * W + x
        chao = v[i] & 0x3FF
        _quadros, macico = quadros_de[chave]
        bits = v[i] & 0xFC00
        if macico and not ((v[i] >> 10) & 3):
            bits |= 0x0400                   # colisao 0 vira 1: a peca e materia
        escritas[i] = bits | vaga[(chao, chave)]
    return escritas, novos, attrs, vaga


# --------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def base_de(guardado):
    """A grade sem NADA deste script (os outros planos ficam de pé)."""
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def _monta_tudo():
    kit = carrega_kit()
    nosso = Nosso()
    guardado = carrega_plano()
    d, L, W, H, _v0 = G.grade(ALVO)
    v = base_de(guardado)
    escolha, proibidas = plano_mapa(kit, nosso, v, W, H, d)
    escritas, novos, attrs, vaga = monta_metatiles(kit, nosso, v, W, escolha, guardado)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    return dict(kit=kit, nosso=nosso, d=d, L=L, W=W, H=H, v=v, saida=saida,
                escolha=escolha, escritas=escritas, novos=novos, attrs=attrs,
                vaga=vaga, guardado=guardado)


def roda(aplicar):
    t = _monta_tudo()
    kit, novos = t["kit"], t["novos"]
    contas = collections.Counter()
    for nome, _dx, dy in t["escolha"].values():
        contas[nome] += 1
    cores = ", ".join("pal %s=%d cores" % (vg, len([c for c in cs[1:] if c != [0, 0, 0]]))
                      for vg, cs in sorted(kit["paletas"].items()))
    print("kit: %d tiles novos (vagas %d a %d de %d), %s"
          % (len(kit["tiles"]), BASE_TILE_0, BASE_TILE_0 + len(kit["tiles"]) - 1,
             TETO_TILES, cores))
    print("no mapa: " + ", ".join("%s x%d" % (k, n) for k, n in sorted(contas.items()))
          + " | %d celulas, %d metatiles novos (locais %d a %d)"
          % (len(t["escritas"]), len(novos), min(novos), max(novos)))
    solidas = sum(1 for i, val in t["escritas"].items()
                  if ((val >> 10) & 3) and not ((t["v"][i] >> 10) & 3))
    print("colisao: %d celulas viraram solidas (0 -> 1), 0 viraram passaveis "
          "(1 -> 0)" % solidas)
    mau = confere(t)
    if mau:
        print("RECUSADO:")
        for x in mau:
            print("  -", x)
        return 1
    if not aplicar:
        return 0

    grava_tileset(kit)
    grava_metatiles(novos, t["attrs"])
    saida = list(G.grade(ALVO)[4])
    for idx, antigo, novo in t["guardado"].get(ALVO, {}).get("celulas", []):
        if saida[idx] == novo:
            saida[idx] = antigo
    for i, val in t["escritas"].items():
        saida[i] = val
    with open(f"{RAIZ}/{t['L']['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(saida), *saida))
    guardado = t["guardado"]
    guardado[ALVO] = {"celulas": [[i, t["v"][i], t["escritas"][i]]
                                  for i in sorted(t["escritas"])]}
    guardado["kit"] = {
        "base_tile": BASE_TILE_0,
        "metatiles": {str(gid - 512): [chao, list(chave)]
                      for (chao, chave), gid in t["vaga"].items()}}
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    print("aplicado")
    return 0


def desfaz():
    guardado = carrega_plano()
    if ALVO not in guardado:
        print("nada a desfazer")
        return 0
    _d, L, _W, _H, v = G.grade(ALVO)
    v, n = list(v), 0
    for idx, antigo, novo in guardado[ALVO]["celulas"]:
        if v[idx] == novo:
            v[idx] = antigo
            n += 1
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(v), *v))
    guardado.pop(ALVO)
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    print("desfeitas %d celulas da silhueta" % n)
    return 0


# ------------------------------------------------------------------- conferes
def confere(t, saida=None, novos=None, attrs=None):
    """A lista de reprovações. Vazia = passou."""
    v, W, H, d, L = t["v"], t["W"], t["H"], t["d"], t["L"]
    nosso, kit = t["nosso"], t["kit"]
    saida = t["saida"] if saida is None else saida
    novos = t["novos"] if novos is None else novos
    attrs = t["attrs"] if attrs is None else attrs
    mau = []
    beh_disco = G.comportamento(L["primary_tileset"], L["secondary_tileset"])

    def beh(mt):
        if mt - 512 in attrs:
            return attrs[mt - 512] & 0x1FF
        return beh_disco(mt)

    AG = E.agua()

    # 1. colisao: 1 -> 0 em ZERO celulas, e 0 -> 1 so onde uma peca escreveu.
    #    Quem autoriza o 0 -> 1 nao e esta regra, e o portao de alcance do item
    #    5: aqui so se garante que nenhuma celula muda de colisao por acidente.
    for i in range(len(v)):
        a, b = (v[i] >> 10) & 3, (saida[i] >> 10) & 3
        if a and not b:
            mau.append("colisao 1 virou 0 em (%d,%d)" % (i % W, i // W))
        if not a and b and i not in t["escritas"]:
            mau.append("colisao 0 virou 1 sem peca em (%d,%d)" % (i % W, i // W))
    # os bits 12 a 15 (elevacao) nunca mudam
    if [x >> 12 for x in v] != [x >> 12 for x in saida]:
        mau.append("a elevacao mudou em alguma celula")

    # 2. (behavior, layerType) identico celula a celula, lido do attributes
    def attr_de(gid):
        return attrs[gid - 512] if (gid - 512) in attrs else nosso.attr(gid)

    ruins = 0
    for i in range(len(v)):
        a, b = nosso.attr(v[i] & 0x3FF), attr_de(saida[i] & 0x3FF)
        if (a & 0x00FF, (a >> 12) & 0xF) != (b & 0x00FF, (b >> 12) & 0xF):
            ruins += 1
    if ruins:
        mau.append("(behavior, layerType) mudou em %d celulas" % ruins)

    # 3. nenhuma peca em cima de evento nem de corredor de teste
    ev = set(E.eventos(d))
    corr = E.corredores_de_teste(ALVO, v, W, H, d)
    for i in t["escritas"]:
        p = (i % W, i // W)
        if p in ev:
            mau.append("escreveu no evento (%d,%d)" % p)
        if p in corr:
            mau.append("escreveu no corredor de teste (%d,%d)" % p)

    # 4. camada de baixo do metatile novo == camada de baixo do chao trocado
    for i, val in t["escritas"].items():
        antigo, novo = v[i] & 0x3FF, val & 0x3FF
        if novo - 512 not in novos:
            mau.append("(%d,%d) aponta para metatile fora do kit" % (i % W, i // W))
        elif nosso.ent(antigo)[:4] != novos[novo - 512][:4]:
            mau.append("a camada de baixo mudou em (%d,%d)" % (i % W, i // W))

    # 5. alcance A PE, pelos DOIS portoes.
    #    O `E.alcance` e a BFS do motor: ela anda por colisao e elevacao e nao
    #    sabe o que e agua, entao toda celula de agua com colisao 0 conta como
    #    "alcancavel" nela. Exigir igualdade CRUA aqui seria proibir qualquer
    #    0 -> 1, inclusive em cima d'agua, que e o que a rodada autoriza. O
    #    portao certo tem duas metades:
    #      a) nada novo fica alcancavel, e nenhuma celula alcancavel se perde
    #         alem das que a peca ocupou;
    #      b) o portao de CHAO: nenhuma celula de comportamento de TERRA sai do
    #         alcance, nem uma. Esse e o que fala do pe do jogador de verdade.
    ini = E.partidas(d, W, H, v)
    antes_pe = E.alcance(v, W, H, ini)
    depois_pe = E.alcance(saida, W, H, ini)
    ocupadas_xy = {(i % W, i // W) for i in t["escritas"]
                   if ((saida[i] >> 10) & 3) and not ((v[i] >> 10) & 3)}
    if depois_pe - antes_pe:
        mau.append("%d celulas ficaram alcancaveis a pe do nada"
                   % len(depois_pe - antes_pe))
    perdidas_pe = (antes_pe - depois_pe) - ocupadas_xy
    if perdidas_pe:
        mau.append("%d celulas sairam do alcance a pe sem a peca ocupar (ex.: %s)"
                   % (len(perdidas_pe), sorted(perdidas_pe)[:3]))
    # b) COMPONENTES DE CHAO, o portao que nao depende de onde o jogador nasce:
    #    o chao andavel nao pode ganhar componente nenhum. Se um monte de
    #    engradado partisse uma praca em duas, a contagem subiria e este teste
    #    reprova, mesmo que os dois pedacos continuem alcancaveis pelos warps.
    #    O comportamento do lado DEPOIS sai do `beh` local, e não do
    #    `beh_disco`: os metatiles do kit ainda NÃO existem no
    #    `metatile_attributes.bin` quando a conferência roda, então ler do disco
    #    devolve zero, e zero é MB_NORMAL, ou seja, chão. As seis células de
    #    mastro e vela do veleiro, que são ÁGUA com colisão 0, viravam dois
    #    componentes de chão do nada, e o portão reprovava a própria peça que
    #    acabara de aprovar. Medido em 07/09/2026 rodando o script sobre a
    #    árvore limpa: com `beh_disco` dos dois lados dá 8 para 10; com o `beh`
    #    local dá 8 para 8. Antes de 07/09 o erro ficava escondido porque o
    #    arquivo de atributos já trazia as vagas escritas pela rodada anterior,
    #    ou seja, o portão só estava certo por acidente do estado do disco.
    ca = componentes_de_chao(v, W, H, beh_disco, AG)
    cb = componentes_de_chao(saida, W, H, beh, AG)
    if cb > ca:
        mau.append("os componentes de chao andavel subiram de %d para %d" % (ca, cb))

    # 6. alcance por AGUA: a unica diferenca permitida sao as celulas ocupadas.
    #    Nenhuma celula de agua que SOBROU pode ficar inalcancavel.
    antes = agua_alcance(v, W, H, AG, beh_disco)
    depois = agua_alcance(saida, W, H, AG, beh)
    ocupadas = {i for i in t["escritas"] if (saida[i] >> 10) & 3}
    if depois - antes:
        mau.append("%d celulas de agua ficaram alcancaveis do nada"
                   % len(depois - antes))
    perdidas = (antes - depois) - ocupadas
    if perdidas:
        mau.append("%d celulas de agua ficaram inalcancaveis (ex.: %s)"
                   % (len(perdidas), sorted((i % W, i // W) for i in perdidas)[:3]))

    # 7. orcamento
    if BASE_TILE_0 + len(kit["tiles"]) > TETO_TILES:
        mau.append("estoura o teto de tiles")
    if novos and max(novos) >= TETO_META:
        mau.append("estoura o teto de metatiles")
    for vg, cores in kit["paletas"].items():
        if len(cores) != 16:
            mau.append("a paleta %s do kit nao tem 16 entradas" % vg)

    # 8. as vagas de paleta do kit nao podem ser usadas por metatile de fora
    minhas = {int(vg) for vg in kit["paletas"]}
    meta_can = _le(f"{DESTINO}/metatiles.bin")
    vistos = {c & 0x3FF for c in saida}
    for local in range(len(meta_can) // 16):
        if local in novos or (512 + local) not in vistos:
            continue
        for valor in entradas(meta_can, local):
            if ((valor >> 12) & 0xF) in minhas:
                mau.append("a paleta %d ja e usada pelo metatile %d"
                           % ((valor >> 12) & 0xF, 512 + local))
                break
    return mau


def demo():
    t = _monta_tudo()
    mau = confere(t)
    if len(t["escritas"]) < 90:
        mau.append("so %d celulas escritas" % len(t["escritas"]))
    # idempotencia do plano
    escolha2, _p = plano_mapa(t["kit"], t["nosso"], list(t["v"]), t["W"], t["H"], t["d"])
    if escolha2 != t["escolha"]:
        mau.append("segunda passada deu plano diferente")
    if mau:
        print("DEMO VERMELHA")
        for x in mau:
            print("  -", x)
        return 1
    print("DEMO VERDE: %d tiles, %d metatiles, %d celulas, 8 conferes"
          % (len(t["kit"]["tiles"]), len(t["novos"]), len(t["escritas"])))
    return 0


def autoteste():
    """A suíte cheia, com quatro provas NEGATIVAS."""
    falhas = []
    t = _monta_tudo()
    mau = confere(t)
    print("1. conferes no plano de verdade: %s"
          % ("VERDE" if not mau else "VERMELHO %s" % mau))
    if mau:
        falhas.append("plano de verdade reprovou")

    # peca no chao certo: tudo que vira solido tem que estar em agua
    beh = G.comportamento(t["L"]["primary_tileset"], t["L"]["secondary_tileset"])
    AG = E.agua()
    virou = [i for i, val in t["escritas"].items()
             if ((val >> 10) & 3) and not ((t["v"][i] >> 10) & 3)]
    na_agua = sum(1 for i in virou if beh(t["v"][i] & 0x3FF) in AG)
    print("2. colisao 0 -> 1: %d celulas, %d em agua e %d em calcada (engradado); "
          "1 -> 0 em 0" % (len(virou), na_agua, len(virou) - na_agua))

    # idempotencia e desfazer
    base2 = list(t["saida"])
    for i in t["escritas"]:
        if base2[i] == t["escritas"][i]:
            base2[i] = t["v"][i]
    ok_desfaz = base2 == list(t["v"])
    escolha2, _p = plano_mapa(t["kit"], t["nosso"], base2, t["W"], t["H"], t["d"])
    print("3. desfazer devolve a base: %s | segunda passada igual: %s"
          % ("VERDE" if ok_desfaz else "VERMELHO",
             "VERDE" if escolha2 == t["escolha"] else "VERMELHO"))
    if not ok_desfaz or escolha2 != t["escolha"]:
        falhas.append("nao e idempotente")

    # PROVA NEGATIVA 1: tirar a colisao de uma celula que ja era solida
    solidas = [i for i in range(len(t["v"])) if (t["v"][i] >> 10) & 3]
    sab = list(t["saida"])
    sab[solidas[0]] &= ~0x0C00
    m = confere(t, saida=sab)
    print("4. prova negativa (colisao 1 virou 0): %s"
          % ("ACUSOU: %s" % m[0] if m else "NAO ACUSOU"))
    if not m:
        falhas.append("nao acusou colisao 1 -> 0")

    # PROVA NEGATIVA 2: fechar uma calcada que peca nenhuma encostou
    seca = next(i for i in range(len(t["v"]))
                if not ((t["v"][i] >> 10) & 3) and beh(t["v"][i] & 0x3FF) not in AG
                and i not in t["escritas"])
    sab = list(t["saida"])
    sab[seca] |= 0x0400
    m = confere(t, saida=sab)
    print("5. prova negativa (calcada fechada sem peca): %s"
          % ("ACUSOU: %s" % m[0] if m else "NAO ACUSOU"))
    if not m:
        falhas.append("nao acusou colisao 0 -> 1 sem peca")

    # PROVA NEGATIVA 3: sabotar o behavior de um metatile novo
    attrs_sab = dict(t["attrs"])
    alvo = sorted(attrs_sab)[0]
    attrs_sab[alvo] = (attrs_sab[alvo] & 0xFF00) | 0x2A
    m = confere(t, attrs=attrs_sab)
    print("6. prova negativa (behavior sabotado): %s"
          % ("ACUSOU: %s" % m[0] if m else "NAO ACUSOU"))
    if not m:
        falhas.append("nao acusou behavior sabotado")

    # PROVA NEGATIVA 4: sabotar a camada de baixo de um metatile novo
    novos_sab = {k: list(vv) for k, vv in t["novos"].items()}
    novos_sab[alvo][0] ^= 1
    m = confere(t, novos=novos_sab)
    print("7. prova negativa (camada de baixo sabotada): %s"
          % ("ACUSOU: %s" % m[0] if m else "NAO ACUSOU"))
    if not m:
        falhas.append("nao acusou camada de baixo sabotada")

    if falhas:
        print("AUTOTESTE VERMELHO")
        for f in falhas:
            print("  -", f)
        return 1
    print("AUTOTESTE VERDE: 7 blocos, %d celulas escritas" % len(t["escritas"]))
    return 0


def main():
    if "--extrair" in sys.argv:
        constroi_kit()
        return 0
    if "--demo" in sys.argv:
        return demo()
    if "--autoteste" in sys.argv:
        return autoteste()
    if "--desfazer" in sys.argv:
        return desfaz()
    return roda("--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
