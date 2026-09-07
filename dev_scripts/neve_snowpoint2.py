#!/usr/bin/env python3
"""Segunda passada de arte em `SnowpointCity`: CALCADA, VARIANTE DE ARVORE e
MOBILIA SOLIDA no `gTileset_Snowpoint`.

POR QUE EXISTE, e por que a primeira passada nao bastou. O commit 44cb13b7b7
importou cinco pecas PLANAS de neve do Golden Glazed e derrubou o carimbo
dominante de `SnowpointCity` de 87,9% para 66,8% do chao andavel a pe (regua de
`dev_scripts/regua_cidades.py`). O Gui olhou o resultado e disse que ficou pouco:
a cidade continuava um mar branco com duzentos pinheiros IGUAIS em grade. A conta
explica o olho. A primeira passada so sabia fazer marca de chao, porque a
definicao de pronto dela proibia colisao 0 -> 1, e sem solidificar celula nao
entra boneco, poste, cerca nem pedra. E marca de chao sozinha nao quebra a
sensacao de carimbo: o que carimba nao e a textura, e a REPETICAO da mesma
arvore e a ausencia de qualquer coisa construida.

A LEI MUDOU em 07/09/2026 e e ela que destrava esta passada: colisao 0 -> 1 e
PERMITIDA em celula que nao seja caminho, warp, evento nem alcance de script,
desde que o ALCANCE A PE continue o mesmo. Colisao 1 -> 0 segue proibida.

AS TRES FRENTES DESTE SCRIPT, em ordem de impacto medido:

1. CALCADA DE PEDRA SOB NEVE. A cidade nao tinha caminho nenhum: quem sai da
   porta do ginasio pisa na mesma neve lisa que existe no meio do bosque. O
   mapa de neve do proprio Golden Glazed (grupo 0, mapa 0) resolve isso com
   uma calcada de pedra clara com moldura, e a medida dele e a prova de que o
   alvo do Gui e alcancavel: 13,1% de carimbo dominante em 352 celulas
   andaveis, com 69 metatiles distintos, contra os nossos 66,8% em 794.
   A calcada entra como nove-fatias completo (nove pecas de borda mais quatro
   cantos concavos) e e desenhada onde as pessoas ANDAM: o esqueleto sai de um
   caminho de custo minimo entre as portas do mapa, e depois engorda.
2. VARIANTE DE ARVORE. As 193 arvores 2x2 do bosque sao o MESMO bloco
   (520,521 / 528,529), celula por celula. Duas arvores novas do Golden Glazed
   entram como bloco 2x2 alternativo, e a escolha por arvore e um rodizio sobre
   a lista embaralhada por posicao: nao e xadrez, nao tem periodo.
   Arvore troca por arvore e SOLIDO por SOLIDO: nenhuma dessas celulas muda de
   colisao, de elevacao nem de alcance.
3. MOBILIA SOLIDA. Placa, poste, cerca, pedra com neve e arbusto seco JA
   EXISTEM desenhados no nosso `gTileset_Snowpoint` (metatiles 515, 585, 593,
   594, 577, 516, 547 e 517) e nenhum mapa os usava. Custam zero tile e zero
   paleta: o que faltava era o direito de solidificar a celula. O unico movel
   importado e o arbusto sob neve do Golden Glazed (metatile 25), que e a
   pecinha branca que aparece dezenas de vezes no mapa dele e nao tem
   equivalente aqui.

O QUE NAO ENTROU, e por que nao. BONECO DE NEVE. O par `0x3DF704`/`0x3DF7AC` do
Golden Glazed nao tem um: os 288 metatiles do secundario foram renderizados e
olhados um a um nesta frente. Existe um bom no `Scorched Silver`, tileset
`0x4924B4`, metatiles 70 (cabeca com olho e nariz) sobre 78 (corpo), com uma
variante de chapeu vermelho no 71, e ele usa a paleta 1 do PRIMARIO daquele
hack. POSTE DE LUZ DE FERRO do Golden Glazed (metatiles 159/167/175 e 226/230)
usa a paleta 9 do secundario dele. Os dois cabem em tile, e nenhum dos dois cabe
em PALETA: o `gTileset_Snowpoint` tem UMA vaga de paleta livre, a 10, porque
`NUM_PALS_TOTAL` e 13 (`include/fieldmap.h`), seis vagas sao do primario e das
sete do secundario as vagas 6, 7, 8, 9, 11 e 12 ja estao em uso por 259
metatiles vivos. A vaga 10 foi para a CALCADA, que e a unica das tres que move
a regua: boneco e poste somados dariam menos de 10 celulas.

DE ONDE VEM A ARTE. Mesma fonte e mesmo par da primeira passada: `Pokemon
Golden Glazed` (base Emerald, o mesmo motor deste repo), primario `0x3DF704` e
secundario `0x3DF7AC`. A escolha do par ja foi provada em 44cb13b7b7 (atlas
rotulado da recon batendo metatile a metatile, e o mapa g00m00 desenhado direto
da ROM contra o mesmo mapa desenhado pelo `render_maps.py` a partir do tileset
extraido, zero pixel diferente de 409.600) e esta passada nao muda de fonte, so
pega outras pecas do mesmo secundario. A ROM e privada e nao entra no repo
(regra 1 do PRD): o que entra e o asset convertido em
`dev_scripts/neve_snowpoint2_kit.json`, com os tiles ja em nibbles e a paleta ja
em RGB. `--extrai` regenera esse arquivo a partir da ROM na maquina que tem
`fontes-mapas/`; `--aplicar` nunca abre a ROM. Credito em `CREDITS.md`, regra 2.

COMO CADA PECA E MONTADA, e o que ela herda de quem:

  - CALCADA: metatile importado INTEIRO do hack (as duas camadas), so trocando
    o indice de tile para a vaga nova e o numero da paleta de 11 para 10. O
    ATRIBUTO e o do metatile 513 INTEIRO (0x0021), nao o do hack: a celula
    continua ANDAVEL e a regra 3 desta onda cobra `(comportamento, layerType)`
    identico em toda celula andavel. Copiando o atributo inteiro, os dois saem
    identicos por construcao.
  - ARVORE: metatile importado inteiro do hack, paleta 6 (que ja e a nossa
    desde a primeira passada). O ATRIBUTO e o da NOSSA arvore que ele
    substitui, posicao por posicao (520, 521, 528 ou 529), e os quatro valem
    0x0000.
  - ARBUSTO SOB NEVE: a camada de BAIXO e a do nosso 513, entrada por entrada,
    byte a byte, porque o arbusto fica em cima da NOSSA neve e nao da do hack;
    a camada de CIMA vem inteira do hack. O atributo e `attr_gg & 0xF000`, ou
    seja o layerType do hack (COVERED, 1) com comportamento ZERADO: comportamento
    e id semantico e a regra 7 do PRD proibe importar id, so arte. A celula fica
    SOLIDA, entao a regra 3 nao a cobre.
  - MOBILIA NOSSA: nenhum metatile novo, nenhum atributo novo. So o bit de
    colisao da celula do mapa vai de 0 para 1.

ONDE CADA COISA CAI, e isso e julgamento com portao, nao sorteio:

  - A calcada nasce do esqueleto de custo minimo entre as portas (ginasio,
    centro pokemon, loja, templo, as duas casas do norte, a entrada norte do
    mapa e o porto). O custo penaliza curva e penaliza andar colado no solido,
    entao o caminho sai pelo MEIO do corredor, que e onde uma calcada de
    verdade fica. Depois o esqueleto engorda em Chebyshev 1 e passa por uma
    limpeza que apaga toda celula que ficaria com menos de duas de largura,
    porque o nove-fatias do hack nao tem peca de faixa de uma celula.
  - Movel de BEIRA (pedra, arbusto, arbusto de neve) exige vizinho solido: e o
    que encosta no bosque, como neve empilhada.
  - Movel de RUA (placa, poste, cerca) exige vizinho de CALCADA: e mobiliario
    urbano, e mobiliario urbano fica na beira da rua, nao no meio do mato.
  - Nenhum movel cai em evento nem na orla de 1 celula em volta dele, nem em
    celula que a suite critica ANDA (`enfeita_cidades.corredores_de_teste`,
    que ja custou sete casos de balsa em Canalave), nem em celula que o
    `enfeita_cidades.py` reservou, nem a menos de 2 celulas da borda.
  - Cada movel novo passa pelo PORTAO DE ALCANCE na hora, nao so no fim: se
    solidificar aquela celula tirar do alcance a pe qualquer celula que nao
    seja ela mesma, o movel e desfeito e o gerador segue.

Idempotente: vaga de tile, de paleta e de metatile sao fixas, e o plano guarda o
valor antigo de cada celula em `dev_scripts/neve_snowpoint2.json`. Rodar duas
vezes da byte identico.

ORDEM: `neve_snowpoint.py` primeiro, depois `enfeita_cidades.py`, e este por
ultimo. Ele planeja sobre a grade que ESTA no disco (as duas passadas anteriores
ja desenhadas) e so encosta em celula de neve lisa nossa (metatile 513 ou um dos
onze metatiles da primeira passada, 680 a 690, que tem o mesmo atributo 0x0021).

Uso:
    python3 dev_scripts/neve_snowpoint2.py             # mede e mostra o plano
    python3 dev_scripts/neve_snowpoint2.py --aplicar   # escreve tileset e mapa
    python3 dev_scripts/neve_snowpoint2.py --desfazer  # devolve o map.bin
    python3 dev_scripts/neve_snowpoint2.py --demo      # auto-teste
    python3 dev_scripts/neve_snowpoint2.py --autoteste # idem
    python3 dev_scripts/neve_snowpoint2.py --extrai    # regera o kit a partir da ROM
"""
import collections
import heapq
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402
import neve_snowpoint as N1          # noqa: E402

ALVO = "SnowpointCity"
DESTINO = f"{RAIZ}/data/tilesets/secondary/snowpoint"
KIT_JSON = f"{RAIZ}/dev_scripts/neve_snowpoint2_kit.json"
PLANO = f"{RAIZ}/dev_scripts/neve_snowpoint2.json"

IRMAOS = N1.IRMAOS          # os cinco layouts que dividem o gTileset_Snowpoint
CHAO = N1.CHAO              # 513, a neve lisa
KIT1 = list(range(680, 691))  # os onze metatiles da primeira passada
TETO_TILES = 512
TETO_META = 512
MARGEM = 2

TILE_LOCAL_0 = 238          # primeira vaga de tile livre depois da 1a passada
META_LOCAL_0 = 179          # primeira vaga de metatile livre (id global 691)
PAL_NOVA = 10               # unica vaga de paleta livre do gTileset_Snowpoint
PAL_GG_CALCADA = 11         # de onde ela vem no secundario do hack
PAL_MATA = 6                # a paleta da 1a passada, ja nossa

FONTE = dict(slug="golden-glazed", ts1=0x3DF704, ts2=0x3DF7AC,
             hack="Pokemon Golden Glazed", mapa="grupo 0 mapa 0 (a cidade de neve)")

# ------------------------------------------------------------------- o KIT
# CALCADA: nove-fatias completo. A chave e a forma da vizinhanca ja calcada.
CALCADA = {
    "NO": 256, "N": 257, "NL": 258,
    "O": 264, "C": 265, "L": 266,
    "SO": 272, "S": 273, "SL": 274,
    "no": 259, "nl": 260, "so": 267, "sl": 268,   # cantos CONCAVOS (chanfro)
}
ORDEM_CALCADA = ["NO", "N", "NL", "O", "C", "L", "SO", "S", "SL",
                 "no", "nl", "so", "sl"]

# ARVORE: bloco 2x2 do hack que substitui o nosso (520,521 / 528,529). Onde o
# hack so tem a METADE ESQUERDA desenhada, a direita e a mesma arte com o bit
# de espelho horizontal ligado, que e o que o proprio hack faz nos pares 5/6,
# 13/14 e 77/78 e nao custa tile novo.
ARVORES = [
    dict(nome="pinheiro copado", gg=[(13, 0), (14, 0), (21, 0), (22, 0)]),
    dict(nome="pinheiro esguio", gg=[(133, 0), (133, 1), (141, 0), (141, 1)]),
]
NOSSA_ARVORE = [520, 521, 528, 529]     # ordem de leitura do bloco 2x2

# MOVEL IMPORTADO: so um, o arbusto sob neve. `sobre_nossa_neve` troca a camada
# de baixo do hack pela do nosso 513.
MOVEIS_GG = [
    dict(nome="arbusto sob neve", gg=25, espelha=False),
    dict(nome="arbusto sob neve espelhado", gg=25, espelha=True),
]

# MOVEL NOSSO: metatile que JA existe no gTileset_Snowpoint e que nenhum dos
# cinco mapas usava. Custa zero tile, zero paleta e zero metatile novo.
#   `onde`: "beira"   = precisa de vizinho SOLIDO (encosta no bosque)
#           "rua"     = precisa de vizinho de CALCADA (mobiliario urbano)
# O metatile 547 foi TIRADO desta lista depois de olhar o render: ele nao e um
# pedregulho solto, e um pedaco de PAREDE de barranco, e sozinho na neve vira um
# retangulo marrom chapado.
MOVEIS_NOSSOS = [
    dict(nome="pedra com neve",      mt=516, onde="beira", quantos=16, espaco=4),
    dict(nome="arbusto seco",        mt=517, onde="beira", quantos=16, espaco=4),
    dict(nome="placa de madeira",    mt=515, onde="rua",   quantos=6,  espaco=8),
    dict(nome="poste",               mt=585, onde="rua",   quantos=12, espaco=4),
    dict(nome="poste baixo",         mt=593, onde="rua",   quantos=10, espaco=4),
    dict(nome="cerca",               mt=594, onde="rua",   quantos=10, espaco=4),
    dict(nome="cerca de canto",      mt=577, onde="rua",   quantos=8,  espaco=4),
]
TETO_MOVEIS = 110
ESPACO_ENTRE_MOVEIS = 2     # Chebyshev minimo entre dois moveis QUAISQUER

N4 = E.N4
DIAG = {"no": (-1, -1), "nl": (1, -1), "so": (-1, 1), "sl": (1, 1)}


# ------------------------------------------------------------------ extracao
def extrai():
    """Regera `neve_snowpoint2_kit.json` a partir da ROM privada do hack.

    So roda na maquina que tem `fontes-mapas/romhacks/`. O que sai daqui e o
    asset convertido (tiles em nibbles e paleta em RGB), nunca a ROM.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("nao achei fontes-mapas/romhacks: --extrai so roda na "
                         "maquina que tem as ROMs. O kit ja extraido esta em "
                         + os.path.relpath(KIT_JSON, RAIZ))
    sys.path.insert(0, f"{ferr}/ferramentas")
    import hashlib
    from gbamap import Rom  # noqa: E402
    pasta = os.path.join(ferr, FONTE["slug"])
    gba = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")][0]
    caminho = os.path.join(pasta, gba)
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    r = Rom(caminho)
    t1 = r.parse_tileset(FONTE["ts1"])
    t2 = r.parse_tileset(FONTE["ts2"])
    npri = r.n_tiles_pri

    def entradas(local):
        return list(struct.unpack_from("<8H", t2["meta"], local * 16))

    def nibbles(dados, local):
        """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
        b = dados[local * 32:local * 32 + 32]
        return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
                 for x in range(8)] for y in range(8)]

    # A NEVE LISA DO HACK, achada por evidencia e nao por constante decorada: o
    # metatile 12 do secundario e chao de neve com uma mudinha em cima, e as
    # quatro entradas da camada de BAIXO dele sao o mesmo tile. Esse tile e a
    # neve lisa do hack, e todo tile com os MESMOS 64 nibbles tambem e (o hack
    # guarda duas copias, as vagas 16 e 35). Quem estiver nesta lista nao entra
    # no nosso tileset: no lugar dele vai a neve do NOSSO metatile 513, senao a
    # arvore importada chega com um retangulo de neve mais clara em volta.
    baixo12 = entradas(12)[:4]
    if len({x & 0x3FF for x in baixo12}) != 1:
        raise SystemExit("o metatile 12 do hack deixou de ser chao liso; a "
                         "deteccao da neve do hack precisa de outra ancora")
    ref = (baixo12[0] & 0x3FF) - npri
    alvo_px = nibbles(t2["tiles"], ref)
    neve_gg = sorted(k for k in range(len(t2["tiles"]) // 32)
                     if nibbles(t2["tiles"], k) == alvo_px)

    quero = ([("calcada", CALCADA[k]) for k in ORDEM_CALCADA]
             + [("arvore", g) for a in ARVORES for g, _e in a["gg"]]
             + [("movel", m["gg"]) for m in MOVEIS_GG])
    pecas, precisa_sec, precisa_pri = [], set(), set()
    vistos = set()
    for papel, local in quero:
        if local in vistos:
            continue
        vistos.add(local)
        ents = entradas(local)
        for k, v in enumerate(ents):
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            if idx == 0:
                continue
            if ip not in (PAL_MATA, PAL_GG_CALCADA):
                raise SystemExit("metatile %d do hack usa a paleta %d, e o kit "
                                 "so importa a %d e a %d"
                                 % (local, ip, PAL_MATA, PAL_GG_CALCADA))
            if idx < npri:
                precisa_pri.add(idx)
            elif (idx - npri) not in neve_gg or k >= 4:
                precisa_sec.add(idx - npri)
        pecas.append(dict(papel=papel, gg=local, ents=ents,
                          attr=struct.unpack_from("<H", t2["attr"], local * 2)[0]))

    cores = struct.unpack_from("<16H", t2["pal"], PAL_GG_CALCADA * 32)
    dados = dict(
        fonte=dict(hack=FONTE["hack"], arquivo=gba, md5=md5,
                   ts1="0x%X" % FONTE["ts1"], ts2="0x%X" % FONTE["ts2"],
                   mapa=FONTE["mapa"], n_tiles_pri=npri),
        paleta={str(PAL_NOVA): [[((c >> s) & 0x1F) * 255 // 31 for s in (0, 5, 10)]
                                for c in cores]},
        tiles_sec={str(k): nibbles(t2["tiles"], k) for k in sorted(precisa_sec)},
        tiles_pri={str(k): nibbles(t1["tiles"], k) for k in sorted(precisa_pri)},
        neve_do_hack=neve_gg,
        pecas=pecas,
    )
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles do secundario, %d do primario, 1 paleta, "
          "%d pecas" % (os.path.relpath(KIT_JSON, RAIZ), len(precisa_sec),
                        len(precisa_pri), len(pecas)))
    return 0


# --------------------------------------------------------------------- leitura
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com as ROMs"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def _entradas(bin_meta, local):
    return list(struct.unpack_from("<8H", bin_meta, local * 16))


def _espelha4(quad):
    """Espelho horizontal de uma camada: troca as colunas e liga o bit 0x400."""
    fora = []
    for q in (1, 0, 3, 2):
        v = quad[q]
        fora.append(0 if (v & 0x3FF) == 0 else (v ^ 0x400))
    return fora


# ------------------------------------------------------------------ importacao
def desenha_kit():
    """(tiles_novos, metas, attrs, carimbos), sem escrever nada em lugar nenhum.

    `carimbos` sai como dicionario de tres listas: `calcada` (por forma),
    `arvores` (blocos 2x2) e `moveis` (um a um).
    """
    dados = kit()
    npri = dados["fonte"]["n_tiles_pri"]
    meta_snow = open(f"{DESTINO}/metatiles.bin", "rb").read()
    attr_snow = open(f"{DESTINO}/metatile_attributes.bin", "rb").read()

    chao_ents = _entradas(meta_snow, CHAO - 512)
    attr_chao = struct.unpack_from("<H", attr_snow, (CHAO - 512) * 2)[0]
    if chao_ents[4:] != [0, 0, 0, 0]:
        raise SystemExit("o metatile %d ja usa a camada de cima" % CHAO)

    por_gg = {}
    for p in dados["pecas"]:
        por_gg.setdefault(p["gg"], p)

    tiles_novos, mapa_tile = {}, {}
    proximo = [TILE_LOCAL_0]

    def vaga(lado, idx):
        """Vaga NOSSA para um tile do hack. `lado` e 's' (secundario) ou 'p'."""
        chave = (lado, idx)
        if chave not in mapa_tile:
            fonte = dados["tiles_sec" if lado == "s" else "tiles_pri"]
            if str(idx) not in fonte:
                raise SystemExit("o kit em disco nao tem o tile %s%d" % (lado, idx))
            mapa_tile[chave] = proximo[0]
            tiles_novos[proximo[0]] = fonte[str(idx)]
            proximo[0] += 1
        return mapa_tile[chave]

    neve_gg = set(dados.get("neve_do_hack") or [])

    def traduz(v, quadrante=None):
        """Entrada do hack -> entrada nossa: mesmo tile, vaga nova, paleta nova.

        `quadrante` so vem preenchido para as quatro entradas da camada de
        BAIXO. Ali valem duas trocas, e as duas existem pelo mesmo motivo: a
        neve do fundo tem que ser a NOSSA.

          - tile 0 e transparente nas duas camadas (`render_maps.desenhar_tile`
            pula a cor 0), entao no fundo ele mostra o BACKDROP do BG, que aqui
            e azul-escuro. Trocando pela entrada do nosso 513, a peca importada
            pousa na nossa neve em vez de num buraco.
          - o tile de neve lisa DO HACK e branco puro e a nossa neve e
            azulada com salpico: deixar o do hack desenha um retangulo mais
            claro em volta da arvore importada, que foi exatamente o defeito
            que o primeiro render desta frente mostrou.
        """
        idx, ip = v & 0x3FF, (v >> 12) & 0xF
        if quadrante is not None and (idx == 0 or (idx >= npri and
                                                  (idx - npri) in neve_gg)):
            return chao_ents[quadrante]
        if idx == 0:
            return 0
        if ip == PAL_MATA:
            nova_pal = PAL_MATA
        elif ip == PAL_GG_CALCADA:
            nova_pal = PAL_NOVA
        else:
            raise SystemExit("entrada com paleta %d, fora do kit" % ip)
        lado, local = ("p", idx) if idx < npri else ("s", idx - npri)
        return (v & 0x0C00) | (512 + vaga(lado, local)) | (nova_pal << 12)

    metas, attrs = {}, {}
    carimbos = {"calcada": {}, "arvores": [], "moveis": []}
    proximo_meta = [META_LOCAL_0]

    def poe(ents, attr):
        local = proximo_meta[0]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo_meta[0] += 1
        return 512 + local

    def achata(ents, nome):
        """Desce a camada de CIMA para a de baixo, quando isso nao muda um pixel.

        POR QUE. A calcada e ANDAVEL e por isso herda o atributo inteiro do 513,
        que tem layerType NORMAL: nesse modo a camada de CIMA vai para o BG1,
        que desenha ACIMA do jogador. O `mapas_qa.py` mediu e acusou: 40 celulas
        de E3, "metatile 692 desenha por cima do jogador", em SnowpointCity. Nao
        da para consertar mudando o layerType, porque a regra 3 desta onda cobra
        `(comportamento, layerType)` identico em toda celula andavel.

        Da para consertar sem tocar em pixel, e a conta e das entradas CRUAS do
        hack: nas duas unicas pecas de calcada em que ele usa a camada de cima
        (a 257 e a 273), ela ou repete o que a de baixo ja tem ou cai num
        quadrante em que a de baixo esta vazia. Cor 0 e transparente nas duas
        camadas (`render_maps.desenhar_tile`), entao descer a entrada para uma
        vaga vazia embaixo desenha o MESMO pixel. Se algum dia aparecer um
        quadrante com desenho DIFERENTE nas duas camadas, isto para o script em
        vez de escolher uma calado.
        """
        baixo, cima = list(ents[:4]), list(ents[4:])
        for q in range(4):
            if not (cima[q] & 0x3FF):
                continue
            if not (baixo[q] & 0x3FF) or baixo[q] == cima[q]:
                baixo[q], cima[q] = cima[q], 0
            else:
                raise SystemExit("%s: o quadrante %d tem desenho DIFERENTE nas "
                                 "duas camadas e a peca e andavel" % (nome, q))
        return baixo + cima

    def importa(gg, espelha=False, achatar=None):
        """As oito entradas do metatile `gg` do hack, ja traduzidas.

        O espelho e o achatamento sao aplicados ANTES da traducao, nas entradas
        CRUAS do hack. Se fossem depois, o espelho viraria tambem a neve NOSSA
        que entra no lugar da neve do hack (e a nossa neve e um desenho de 2x2
        tiles em que cada quadrante tem o seu), e o achatamento acharia a camada
        de baixo ja preenchida com essa neve em vez de vazia.
        """
        ents = por_gg[gg]["ents"]
        if espelha:
            ents = _espelha4(ents[:4]) + _espelha4(ents[4:])
        if achatar:
            ents = achata(ents, achatar)
        return ([traduz(v, q) for q, v in enumerate(ents[:4])]
                + [traduz(v) for v in ents[4:]])

    # 1. CALCADA: metatile inteiro do hack, atributo INTEIRO do nosso 513, e as
    #    duas camadas achatadas em uma so (ver `achata`).
    for forma in ORDEM_CALCADA:
        carimbos["calcada"][forma] = poe(
            importa(CALCADA[forma], achatar="calcada %s" % forma), attr_chao)

    # 2. ARVORE: metatile inteiro do hack, atributo da NOSSA arvore da posicao.
    for arv in ARVORES:
        ids = []
        for pos, (gg, esp) in enumerate(arv["gg"]):
            nosso = NOSSA_ARVORE[pos]
            a = struct.unpack_from("<H", attr_snow, (nosso - 512) * 2)[0]
            ids.append(poe(importa(gg, bool(esp)), a))
        carimbos["arvores"].append(dict(nome=arv["nome"], ids=ids))

    # 3. MOVEL IMPORTADO: camada de baixo do NOSSO 513, camada de cima do hack.
    for m in MOVEIS_GG:
        p = por_gg[m["gg"]]
        ents = _espelha4(p["ents"][4:]) if m["espelha"] else p["ents"][4:]
        cima = [traduz(v) for v in ents]
        if all(x == 0 for x in cima):
            raise SystemExit("%s: o metatile %d do hack nao desenha nada em cima"
                             % (m["nome"], m["gg"]))
        # comportamento ZERADO de proposito: comportamento e id semantico e a
        # regra 7 do PRD proibe importar id do hack, so arte. O layerType e o do
        # hack (COVERED), que e o que poe o jogador NA FRENTE do arbusto.
        gid = poe(chao_ents[:4] + cima, p["attr"] & 0xF000)
        carimbos["moveis"].append(dict(nome=m["nome"], mt=gid, onde="beira",
                                       quantos=12, espaco=5, importado=True))

    # 4. MOVEL NOSSO: em regra nada de novo no tileset, so o direito de usar.
    #    A excecao e o metatile cujo COMPORTAMENTO nao e MB_NORMAL. O 516 (a
    #    pedra com touca de neve) esta gravado como 0x02, MB_TALL_GRASS, e
    #    nenhum mapa o usava, entao ninguem tinha notado. Usa-lo como esta
    #    planta grama alta numa cidade de neve: o `mapas_qa.py` acusou D1,
    #    "tem grama alta e NENHUMA tabela de encontro". Trocar o atributo do 516
    #    esta PROIBIDO (metatile vivo de tileset compartilhado por seis
    #    layouts), entao entra uma COPIA dele em vaga livre, com os mesmos oito
    #    tiles byte a byte, o mesmo layerType e o comportamento zerado.
    for m in MOVEIS_NOSSOS:
        local = m["mt"] - 512
        ents = _entradas(meta_snow, local)
        if len(set(ents)) == 1 and ents[0] <= 2:
            raise SystemExit("o metatile %d esta vazio no disco" % m["mt"])
        a = struct.unpack_from("<H", attr_snow, local * 2)[0]
        # So clona quem traz comportamento ESTRANHO. Comportamento 0x00
        # (MB_NORMAL) nao diz nada, e 0x21 e o comportamento do proprio chao de
        # neve desta cidade, que ja esta em 794 celulas e nao significa nada
        # numa celula solida. O que nao pode ficar e o 0x02 do metatile 516,
        # que e MB_TALL_GRASS.
        estranho = (a & 0xFF) not in (0x00, attr_chao & 0xFF)
        mt = poe(list(ents), a & 0xF000) if estranho else m["mt"]
        carimbos["moveis"].append(dict(nome=m["nome"], mt=mt, onde=m["onde"],
                                       quantos=m["quantos"], espaco=m["espaco"],
                                       importado=False, copia_de=m["mt"]))

    if proximo[0] > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo[0]))
    if proximo_meta[0] > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)

    # A vaga de metatile so serve se for ENCHIMENTO do dumper (as oito entradas
    # iguais e baixas) ou se ja tiver exatamente o que este kit escreve (rodar
    # duas vezes), e NENHUM dos cinco mapas do tileset pode usar o id.
    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    usados = set()
    for nome in IRMAOS:
        usados |= {c & 0x3FF for c in G.grade(nome)[4]}
    for local, ents in metas.items():
        gid = 512 + local
        antigo = _entradas(meta_snow, local)
        if not enchimento(antigo) and antigo != ents:
            raise SystemExit("vaga de metatile %d ja esta ocupada por outra coisa"
                             % gid)
        if gid in usados and enchimento(antigo):
            raise SystemExit("algum dos cinco mapas usa o metatile %d e a vaga "
                             "esta vazia" % gid)

    # A vaga de paleta tem que estar livre em TODO metatile que nao seja do kit.
    for local in range(len(meta_snow) // 16):
        if local in metas:
            continue
        for v in _entradas(meta_snow, local):
            if (v & 0x3FF) and ((v >> 12) & 0xF) == PAL_NOVA:
                raise SystemExit("a paleta %d ja e usada pelo metatile %d"
                                 % (PAL_NOVA, 512 + local))
    return tiles_novos, metas, attrs, carimbos


def grava_tileset(tiles_novos, metas, attrs):
    from PIL import Image
    dados = kit()
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    alvo = max(TILE_LOCAL_0 + len(tiles_novos), (antigo.size[1] // 8) * cols)
    linhas = (alvo + cols - 1) // cols
    novo = Image.new("P", (antigo.size[0], linhas * 8), 0)
    novo.putpalette(antigo.getpalette())
    novo.paste(antigo, (0, 0))
    px = novo.load()
    for v, tile in tiles_novos.items():
        x0, y0 = (v % cols) * 8, (v // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    novo.save(f"{DESTINO}/tiles.png")

    cores = dados["paleta"][str(PAL_NOVA)]
    with open(f"{DESTINO}/palettes/%02d.pal" % PAL_NOVA, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))

    meta = bytearray(open(f"{DESTINO}/metatiles.bin", "rb").read())
    attr = bytearray(open(f"{DESTINO}/metatile_attributes.bin", "rb").read())
    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------------------- a calcada
def esqueleto(v, W, H, d, elegivel):
    """Caminho de custo minimo ligando as portas do mapa, em ordem de leitura.

    O custo nao e so distancia. Andar colado num solido custa mais, para a
    calcada sair pelo MEIO do corredor e nao raspando o bosque; virar custa
    mais, para a rua sair reta como rua de verdade; e celula que nao pode
    receber calcada custa muito mais, mas nao e proibida, senao o caminho nao
    atravessa a soleira das portas nem os pedacos de chao que nao sao neve
    lisa nossa.
    """
    def andavel(i):
        return not ((v[i] >> 10) & 3)

    def perto_de_solido(x, y):
        return sum(1 for dx, dy in N4
                   if not (0 <= x + dx < W and 0 <= y + dy < H)
                   or ((v[(y + dy) * W + x + dx] >> 10) & 3))

    def custo(x, y):
        c = 1.0 + 2.0 * perto_de_solido(x, y)
        if (x, y) not in elegivel:
            c += 12.0
        return c

    def caminho(ini, fim):
        """Dijkstra com estado (celula, direcao), para poder cobrar a curva."""
        alvo = set(fim)
        dist = {}
        fila = [(0.0, ini[0], ini[1], 0, 0)]
        pai = {}
        while fila:
            g, x, y, dx0, dy0 = heapq.heappop(fila)
            if (x, y, dx0, dy0) in dist:
                continue
            dist[(x, y, dx0, dy0)] = g
            if (x, y) in alvo and (dx0, dy0) != (0, 0):
                saida, no = [], (x, y, dx0, dy0)
                while no in pai:
                    saida.append((no[0], no[1]))
                    no = pai[no]
                saida.append((no[0], no[1]))
                return saida
            for dx, dy in N4:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    continue
                if not andavel(ny * W + nx):
                    continue
                # A CURVA E CARA de proposito: com pouca multa o caminho de
                # custo minimo desce em escada e a calcada dilatada sai com
                # dente de serra. Com multa alta ele anda reto ate o corredor
                # acabar, que e como rua de cidade e desenhada.
                curva = 9.0 if (dx0, dy0) != (0, 0) and (dx, dy) != (dx0, dy0) else 0.0
                no = (nx, ny, dx, dy)
                if no in dist:
                    continue
                pai[no] = (x, y, dx0, dy0)
                heapq.heappush(fila, (g + custo(nx, ny) + curva, nx, ny, dx, dy))
        return []

    # As soleiras: a celula andavel logo abaixo de cada porta, que e onde o
    # jogador pousa. Mais a entrada norte do mapa e as duas pontas do porto.
    portas = []
    for w in (d.get("warp_events") or []):
        x, y = w["x"], w["y"]
        for dx, dy in ((0, 1), (0, 0), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and andavel(ny * W + nx):
                portas.append((nx, ny))
                break
    chao = sorted(p for p in elegivel)
    if chao:
        # entrada norte do mapa, e as duas pontas do porto: sem elas a calcada
        # para na porta do centro pokemon e o sul da cidade fica sem rua.
        ymin, ymax = min(y for _, y in chao), max(y for _, y in chao)
        for alvo_y, quantos in ((ymin, 1), (ymax, 2)):
            faixa = [p for p in chao if abs(p[1] - alvo_y) <= 1]
            if not faixa:
                continue
            xs = sorted({p[0] for p in faixa})
            escolhas = [xs[len(xs) // 4], xs[3 * len(xs) // 4]][:quantos] \
                if quantos > 1 else [min(xs, key=lambda x: abs(x - W // 2))]
            for xe in escolhas:
                portas.append(min((p for p in faixa if p[0] == xe),
                                  key=lambda p: abs(p[1] - alvo_y)))
    # PRACA DE VAZIO. Ligar so porta com porta deixa a cidade com bolsao de
    # neve grande e vazio que rua nenhuma toca, e vazio grande e o que faz o
    # mapa parecer preenchido em vez de desenhado. Todo miolo de vazio (celula
    # cujo 5x5 inteiro ainda e neve nossa) entra como PONTO A LIGAR, um por
    # bolsao: o mais central de cada aglomerado.
    miolo = {p for p in elegivel
             if all((p[0] + dx, p[1] + dy) in elegivel
                    for dx in range(-2, 3) for dy in range(-2, 3))}
    vistos, bolsoes = set(), []
    for p in sorted(miolo):
        if p in vistos:
            continue
        pilha, grupo = [p], []
        vistos.add(p)
        while pilha:
            q = pilha.pop()
            grupo.append(q)
            for dx, dy in N4:
                r = (q[0] + dx, q[1] + dy)
                if r in miolo and r not in vistos:
                    vistos.add(r)
                    pilha.append(r)
        if len(grupo) >= 6:
            bolsoes.append(grupo)
    for grupo in bolsoes:
        cx = sum(q[0] for q in grupo) / len(grupo)
        cy = sum(q[1] for q in grupo) / len(grupo)
        portas.append(min(grupo, key=lambda q: (q[0] - cx) ** 2 + (q[1] - cy) ** 2))

    # LIGACAO EM ARVORE, nao em fila: ligar porta 0 a 1, 1 a 2 e assim por
    # diante daria um zigue-zague que atravessa a cidade inteira toda vez. Aqui
    # cada porta nova se liga a QUALQUER ponto ja ligado, que e a rua mais curta
    # que serve, e o resultado e uma rede de rua com cruzamento.
    ossos = set([portas[0]])
    for p in portas[1:]:
        trecho = caminho(p, ossos)
        if not trecho:
            continue
        ossos |= set(trecho)
    return ossos, portas


def area_calcada(v, W, H, d, elegivel):
    """O conjunto de celulas que viram calcada, ja limpo e com >= 2 de largura."""
    ossos, portas = esqueleto(v, W, H, d, elegivel)
    pav = set()
    for x, y in ossos:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                p = (x + dx, y + dy)
                if p in elegivel:
                    pav.add(p)
    # LARGURA VARIAVEL: tres celulas de largura e o minimo, e no corredor
    # apertado e tudo que cabe. Onde SOBRA espaco (a celula e as oito em volta
    # dela ainda sao neve nossa), a rua abre para cinco: e o que separa uma
    # trilha de uma avenida, e e onde a cidade ganha praca.
    def folgada(p):
        return all((p[0] + dx, p[1] + dy) in elegivel
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1))

    pav |= {(x + dx, y + dy) for x, y in ossos
            for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)
            if (x + dx, y + dy) in elegivel and folgada((x + dx, y + dy))}
    # PRACA DE PORTA: quem sai de um predio pisa num largo, nao numa faixa de
    # tres. Cada soleira ganha o retangulo 5x3 em volta dela, no que couber.
    for x, y in portas:
        for dx in range(-2, 3):
            for dy in range(-1, 2):
                if (x + dx, y + dy) in elegivel:
                    pav.add((x + dx, y + dy))
    # ENCHER BURACO E CHANFRO: celula de neve cercada de calcada nos quatro
    # lados vira calcada (senao fica uma ilha de uma celula no meio da praca), e
    # celula cercada em tres lados tambem, que e o dente de serra que a
    # dilatacao deixa na beira. Repete ate estabilizar.
    while True:
        entra = {p for p in elegivel if p not in pav
                 and sum(1 for dx, dy in N4 if (p[0] + dx, p[1] + dy) in pav) >= 3}
        if not entra:
            break
        pav |= entra
    # LIMPEZA: o nove-fatias do hack nao tem peca de faixa de UMA celula, entao
    # toda celula que nao tenha vizinho calcado no eixo vertical E no horizontal
    # sai. Repete ate estabilizar, porque tirar uma pode desqualificar a vizinha.
    while True:
        fora = {(x, y) for x, y in pav
                if not ((x, y - 1) in pav or (x, y + 1) in pav)
                or not ((x - 1, y) in pav or (x + 1, y) in pav)}
        if not fora:
            break
        pav -= fora
    return pav, portas


def forma_calcada(pav, x, y):
    """Qual peca do nove-fatias cabe nesta celula."""
    n = (x, y - 1) in pav
    s = (x, y + 1) in pav
    o = (x - 1, y) in pav
    l = (x + 1, y) in pav
    if not n and not o:
        return "NO"
    if not n and not l:
        return "NL"
    if not s and not o:
        return "SO"
    if not s and not l:
        return "SL"
    if not n:
        return "N"
    if not s:
        return "S"
    if not o:
        return "O"
    if not l:
        return "L"
    for k, (dx, dy) in DIAG.items():
        if (x + dx, y + dy) not in pav:
            return k
    return "C"


# ---------------------------------------------------------------- plano do mapa
def plano_mapa(carimbos, base=None):
    """(L, W, H, v, escritas, contas)."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    elev_chao = collections.Counter(
        (c >> 12) & 0xF for c in v
        if (c & 0x3FF) == CHAO and not ((c >> 10) & 3)).most_common(1)[0][0]

    nossa_neve = {CHAO} | set(KIT1)

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    elegivel = {(i % W, i // W) for i in range(W * H)
                if andavel(i) and (v[i] & 0x3FF) in nossa_neve
                and ((v[i] >> 12) & 0xF) == elev_chao
                and beh(v[i] & 0x3FF) not in AG}

    escritas = {}

    # ------------------------------------------------------------- 1. calcada
    pav, portas = area_calcada(v, W, H, d, elegivel)
    for x, y in sorted(pav):
        escritas[y * W + x] = ((v[y * W + x] & 0xFC00)
                               | carimbos["calcada"][forma_calcada(pav, x, y)])

    # ------------------------------------------------------------- 2. arvores
    def mt(x, y):
        return v[y * W + x] & 0x3FF if 0 <= x < W and 0 <= y < H else -1

    blocos = [(x, y) for y in range(H - 1) for x in range(W - 1)
              if [mt(x, y), mt(x + 1, y), mt(x, y + 1), mt(x + 1, y + 1)]
              == NOSSA_ARVORE]
    # rodizio sobre a lista EMBARALHADA por posicao: nao e xadrez e nao tem
    # periodo, e mesmo assim a conta de cada variante fica equilibrada.
    ordem = sorted(blocos, key=lambda p: (((p[0] * 2654435761) ^ (p[1] * 40503))
                                          * 2246822519) & 0xFFFFFFFF)
    conta_arv = collections.Counter()
    # 3 em cada 7 continuam a nossa arvore: variedade nao e trocar tudo.
    roda = [None, ARVORES[0]["nome"], None, ARVORES[1]["nome"], None,
            ARVORES[0]["nome"], ARVORES[1]["nome"]]
    por_nome = {a["nome"]: a for a in carimbos["arvores"]}
    for k, (x, y) in enumerate(ordem):
        nome = roda[k % len(roda)]
        if nome is None:
            conta_arv["a nossa"] += 1
            continue
        ids = por_nome[nome]["ids"]
        for pos, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            j = (y + dy) * W + x + dx
            escritas[j] = (v[j] & 0xFC00) | ids[pos]
        conta_arv[nome] += 1

    # -------------------------------------------------------------- 3. moveis
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    # O que o `enfeita_cidades.py` desenhou nesta cidade fica de fora, mas SO a
    # celula: aqui nao vale a orla de 1 que o `neve_snowpoint.py` usa, porque
    # aquilo era para dois carimbos de CHAO nao se encostarem, e movel encostado
    # em enfeite e cidade cheia, nao cidade errada.
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))

    aplicado = list(v)
    for i, val in escritas.items():
        aplicado[i] = val
    ini = E.partidas(d, W, H, v)
    antes = E.alcance(v, W, H, ini)
    novos_solidos, postos = [], []
    conta_mov = collections.Counter()
    por_movel = collections.defaultdict(list)

    def solido(x, y):
        return 0 <= x < W and 0 <= y < H and ((aplicado[y * W + x] >> 10) & 3)

    def nao_liga(grade, x, y):
        """Os vizinhos andaveis de (x,y) ainda se falam sem passar por (x,y)?

        E o teste de ponto de articulacao, e ele existe porque o portao de
        alcance sozinho nao pega corredor com warp dos dois lados (ver
        `componentes`). A busca comeca no primeiro vizinho andavel e tem que
        chegar em todos os outros.
        """
        viz = [(x + dx, y + dy) for dx, dy in N4
               if 0 <= x + dx < W and 0 <= y + dy < H
               and not ((grade[(y + dy) * W + x + dx] >> 10) & 3)]
        if len(viz) < 2:
            return False
        vistos = {viz[0]}
        fila = [viz[0]]
        falta = set(viz[1:])
        while fila and falta:
            cx, cy = fila.pop()
            ea = (grade[cy * W + cx] >> 12) & 0xF
            for dx, dy in N4:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in vistos:
                    continue
                j = ny * W + nx
                if (grade[j] >> 10) & 3:
                    continue
                eb = (grade[j] >> 12) & 0xF
                if ea and eb and ea != eb:
                    continue
                vistos.add((nx, ny))
                falta.discard((nx, ny))
                fila.append((nx, ny))
        return bool(falta)

    def cabe(m, x, y, so_chao):
        i = y * W + x
        if so_chao and (aplicado[i] & 0x3FF) != CHAO:
            return False
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas or (x, y) not in elegivel:
            return False
        # Vale a neve lisa (513) e tambem as onze pecas planas da primeira
        # passada (680 a 690): as tres coisas tem o mesmo atributo 0x0021 e o
        # mesmo papel de chao, e boa parte das celulas de BEIRA da cidade e da
        # primeira passada, que foi justamente atras de encosto de solido.
        if (aplicado[i] & 0x3FF) not in nossa_neve:
            return False
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        if any(max(abs(x - px), abs(y - py)) < m["espaco"]
               for px, py in por_movel[m["nome"]]):
            return False
        if m["onde"] == "beira":
            if not any(solido(x + dx, y + dy) for dx, dy in N4):
                return False
        else:
            if not any((x + dx, y + dy) in pav for dx, dy in N4):
                return False
        return True

    ordem_cel = sorted(((x, y) for y in range(H) for x in range(W)),
                       key=lambda p: ((p[0] * 2654435761 + p[1] * 40503) & 0xFFFF, p))
    lista = carimbos["moveis"]
    # DUAS VARREDURAS, e a ordem tem consequencia medida. Na primeira o movel so
    # entra em neve lisa 513, que e o carimbo que este trabalho existe para
    # quebrar; na segunda ele aceita tambem as pecas planas da primeira passada.
    # Com uma varredura so, o movel comia peca da primeira passada antes de comer
    # carimbo e a regua PIOROU de 18,7% para 21,2%: o denominador caia e o
    # numerador nao.
    for so_chao in (True, False):
        for x, y in ordem_cel:
            if sum(conta_mov.values()) >= TETO_MOVEIS:
                break
            giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
            for k in range(len(lista)):
                m = lista[(giro + k) % len(lista)]
                if conta_mov[m["nome"]] >= m["quantos"]:
                    continue
                if not cabe(m, x, y, so_chao):
                    continue
                i = y * W + x
                antigo = aplicado[i]
                # elevacao PRESERVADA (bits 12 a 15), colisao ligada, metatile novo.
                aplicado[i] = (antigo & 0xF000) | (1 << 10) | m["mt"]
                # PORTAO DE ALCANCE na hora, e nao so no fim: se solidificar esta
                # celula tirar do alcance a pe qualquer OUTRA celula, o movel e
                # desfeito e o gerador segue, como faz o enfeita_cidades.py.
                perdidas = (antes - E.alcance(aplicado, W, H, ini)) \
                    - set(novos_solidos) - {(x, y)}
                if perdidas or nao_liga(aplicado, x, y):
                    aplicado[i] = antigo
                    continue
                escritas[i] = aplicado[i]
                novos_solidos.append((x, y))
                postos.append((x, y))
                por_movel[m["nome"]].append((x, y))
                conta_mov[m["nome"]] += 1
                break

    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d celulas ficariam inalcancaveis, ex.: %s"
                         % (ALVO, len(perdidas), sorted(perdidas)[:6]))
    for x, y in E.eventos(d):
        if (x, y) in antes and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcancavel"
                             % (ALVO, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (ALVO, "; ".join(queixas)))
    contas = dict(calcada=len(pav), arvores=dict(conta_arv),
                  moveis=dict(conta_mov), solidos=len(novos_solidos),
                  portas=portas)
    return L, W, H, v, escritas, contas


# ----------------------------------------------------------- ligacao a pe
def componentes(v, W, H):
    """{celula: rotulo} dos pedacos de chao andavel ligados a pe.

    POR QUE NAO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda e
    alcancavel a partir de algum ponto de partida", e ponto de partida ali e
    warp OU objeto. Snowpoint tem warp dos DOIS lados do corredor de duas
    celulas da linha 14 (as casas do norte de um lado, a cidade do outro):
    fechar o corredor inteiro nao tira NENHUMA celula do alcance, porque cada
    metade continua alcancavel a partir do proprio warp, e mesmo assim o
    jogador que entra pela cidade nao chega mais nas casas. Medido nesta frente
    em 07/09/2026, com uma sabotagem que o portao antigo deixou passar verde.
    Este aqui olha a LIGACAO entre as celulas, que e o que o jogador sente.
    """
    rot, prox = {}, 0
    for y in range(H):
        for x in range(W):
            if (v[y * W + x] >> 10) & 3 or (x, y) in rot:
                continue
            fila, prox = [(x, y)], prox + 1
            rot[(x, y)] = prox
            while fila:
                cx, cy = fila.pop()
                ea = (v[cy * W + cx] >> 12) & 0xF
                for dx, dy in N4:
                    nx, ny = cx + dx, cy + dy
                    if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in rot:
                        continue
                    j = ny * W + nx
                    if (v[j] >> 10) & 3:
                        continue
                    eb = (v[j] >> 12) & 0xF
                    if ea and eb and ea != eb:
                        continue
                    rot[(nx, ny)] = prox
                    fila.append((nx, ny))
    return rot


def ligacao_intacta(antes, depois, solidificadas):
    """Nenhum pedaco de chao se PARTIU, e nenhum se juntou a outro.

    Devolve a lista de queixas, vazia quando esta tudo bem.
    """
    mau = []
    por_rotulo = collections.defaultdict(set)
    for p, r in antes.items():
        if p not in solidificadas:
            por_rotulo[r].add(p)
    for r, cels in por_rotulo.items():
        vistos = {depois.get(p) for p in cels}
        if len(vistos) > 1:
            mau.append("o pedaco %d de chao se partiu em %d" % (r, len(vistos)))
    juntou = collections.defaultdict(set)
    for p, r in depois.items():
        if p in antes:
            juntou[r].add(antes[p])
    for r, origens in juntou.items():
        if len(origens) > 1:
            mau.append("dois pedacos de chao que eram separados se juntaram")
    return mau


# ------------------------------------------------------------------ regua
def regua(v, W, H, L, escritas=None):
    """(carimbo dominante, celulas andaveis a pe, id do carimbo) como a regua."""
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    cel = list(v)
    for i, val in (escritas or {}).items():
        cel[i] = val
    and_ = [c & 0x3FF for c in cel
            if not ((c >> 10) & 3) and beh(c & 0x3FF) not in AG]
    top = collections.Counter(and_).most_common(1)[0]
    return 100.0 * top[1] / len(and_), len(and_), top[0]


# ---------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def base_de(guardado):
    """A grade como esta no disco, so tirando o que ESTA passada escreveu."""
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    print("kit 2: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
          "novos (locais %d a %d, ids %d a %d), paleta %d"
          % (len(tiles_novos), TILE_LOCAL_0, TILE_LOCAL_0 + len(tiles_novos) - 1,
             TETO_TILES, TETO_TILES - TILE_LOCAL_0 - len(tiles_novos),
             len(metas), min(metas), max(metas), 512 + min(metas),
             512 + max(metas), PAL_NOVA))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    base = base_de(guardado)
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base)
    print("calcada: %d celulas | arvores: %s | moveis: %d em %d tipos"
          % (contas["calcada"],
             ", ".join("%s x%d" % kv for kv in sorted(contas["arvores"].items())),
             contas["solidos"], len(contas["moveis"])))
    print("  moveis: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["moveis"].items())))
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("regua (chao andavel a pe): carimbo %d com %.1f%% de %d celulas ANTES; "
          "carimbo %d com %.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
    print("celulas do mapa mudadas: %d" % len(escritas))
    if aplicar:
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(saida), *saida))
        guardado[ALVO] = {"celulas": [[i, v[i], escritas[i]]
                                      for i in sorted(escritas)]}
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("aplicado")
    return escritas


def desfaz():
    guardado = carrega_plano()
    if ALVO not in guardado:
        print("nada a desfazer")
        return 0
    d, L, W, H, v = G.grade(ALVO)
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
    print("desfeitas %d celulas" % n)
    return 0


# ------------------------------------------------------------------ auto-teste
def demo():
    mau = []
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    meta_snow = open(f"{DESTINO}/metatiles.bin", "rb").read()
    attr_snow = open(f"{DESTINO}/metatile_attributes.bin", "rb").read()
    attr_chao = struct.unpack_from("<H", attr_snow, (CHAO - 512) * 2)[0]
    chao_ents = _entradas(meta_snow, CHAO - 512)
    ids_calcada = set(carimbos["calcada"].values())
    ids_arvore = {i for a in carimbos["arvores"] for i in a["ids"]}
    ids_movel_novo = {m["mt"] for m in carimbos["moveis"] if m["importado"]}

    # 1. orcamento
    if TILE_LOCAL_0 + len(tiles_novos) > TETO_TILES:
        mau.append("estoura o teto de tiles")
    if max(metas) >= TETO_META:
        mau.append("estoura o teto de metatiles")
    if not 6 <= PAL_NOVA <= 12:
        mau.append("paleta %d nao e vaga de secundario" % PAL_NOVA)

    # 2. a calcada e ANDAVEL: atributo inteiro do 513, comportamento e layerType
    for local, gid in ((g - 512, g) for g in ids_calcada):
        if attrs[local] != attr_chao:
            mau.append("calcada %d: atributo 0x%04X, esperado 0x%04X"
                       % (gid, attrs[local], attr_chao))

    # 3. a arvore herda o atributo da NOSSA arvore da posicao
    for a in carimbos["arvores"]:
        for pos, gid in enumerate(a["ids"]):
            esperado = struct.unpack_from("<H", attr_snow,
                                          (NOSSA_ARVORE[pos] - 512) * 2)[0]
            if attrs[gid - 512] != esperado:
                mau.append("%s: metatile %d com atributo 0x%04X, esperado 0x%04X"
                           % (a["nome"], gid, attrs[gid - 512], esperado))

    # 4. o movel importado pisa na NOSSA neve e nao importa comportamento
    for gid in ids_movel_novo:
        ent = metas[gid - 512]
        if ent[:4] != chao_ents[:4]:
            mau.append("movel %d nao tem a neve de Snowpoint embaixo" % gid)
        if attrs[gid - 512] & 0xFF:
            mau.append("movel %d importou comportamento 0x%02X do hack"
                       % (gid, attrs[gid - 512] & 0xFF))

    # 5. paleta: so a 6 (a da primeira passada), a 10 (a que este kit traz) e as
    #    que o NOSSO metatile 513 ja usava, que sao as que entram junto com a
    #    neve nossa substituida na camada de baixo.
    pals_ok = {PAL_MATA, PAL_NOVA} | {(x >> 12) & 0xF for x in chao_ents if x & 0x3FF}
    for local, ent in metas.items():
        for x in ent:
            if (x & 0x3FF) and ((x >> 12) & 0xF) not in pals_ok:
                mau.append("metatile %d aponta para a paleta %d, que nao e do kit"
                           % (512 + local, (x >> 12) & 0xF))

    # 6. o plano do mapa
    guardado = carrega_plano()
    base = base_de(guardado)
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base)
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val

    for i, val in escritas.items():
        x, y = i % W, i // W
        mt_novo, mt_velho = val & 0x3FF, v[i] & 0x3FF
        col_novo, col_velho = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("mudou ELEVACAO em (%d,%d)" % (x, y))
        if col_velho and not col_novo:
            mau.append("colisao 1 -> 0 em (%d,%d), que segue proibida" % (x, y))
        if mt_novo in ids_calcada:
            if col_novo != col_velho or mt_velho not in ({CHAO} | set(KIT1)):
                mau.append("calcada em celula errada em (%d,%d)" % (x, y))
        elif mt_novo in ids_arvore:
            if not col_velho or not col_novo:
                mau.append("arvore trocada em celula nao solida em (%d,%d)" % (x, y))
        else:
            if col_velho or not col_novo:
                mau.append("movel em (%d,%d) nao e solidificacao 0 -> 1" % (x, y))
            if mt_velho not in ({CHAO} | set(KIT1)):
                mau.append("movel fora da nossa neve lisa em (%d,%d)" % (x, y))
            if (x, y) in ev:
                mau.append("movel em cima do evento (%d,%d)" % (x, y))

    # 7. (comportamento, layerType) de toda celula ANDAVEL fica igual
    ap = G._attrs(L["primary_tileset"])
    asec = G._attrs(L["secondary_tileset"])

    def atributo(mt_id):
        """Atributo de um metatile, com o kit desta rodada valendo por cima.

        O kit pode ainda nao estar no disco (primeira rodada antes do
        `--aplicar`), e nesse caso o valor certo e o que o `desenha_kit`
        acabou de montar, nao o enchimento do dumper que esta no arquivo.
        """
        if mt_id >= 512:
            local = mt_id - 512
            if local in attrs:
                return attrs[local]
            return asec[local] if local < len(asec) else 0
        return ap[mt_id] if mt_id < len(ap) else 0

    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("celula andavel (%d,%d) mudou (comportamento, layerType)"
                       % (i % W, i // W))
            break

    # 8. alcance a pe: perde SO as celulas que viraram solidas, e ganha nenhuma
    ini = E.partidas(d, W, H, v)
    antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
    solidificadas = {(i % W, i // W) for i in escritas
                     if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
    # A igualdade nao e "o mesmo conjunto": movel novo TIRA do alcance a celula
    # que ele ocupa, e e isso que a lei nova de 07/09/2026 permite. O que nao
    # pode e perder QUALQUER OUTRA celula, nem ganhar nenhuma. (Parte das
    # celulas solidificadas ja nao estava no alcance porque e bolsao fechado
    # dentro do bosque, entao a inclusao e num sentido so.)
    if (antes - depois) - solidificadas:
        mau.append("o alcance a pe perdeu %d celulas alem das solidificadas: %s"
                   % (len((antes - depois) - solidificadas),
                      sorted((antes - depois) - solidificadas)[:6]))
    if depois - antes:
        mau.append("o alcance a pe GANHOU celula, e nenhuma peca abre passagem")
    # 8b. LIGACAO a pe: nenhum pedaco de chao se partiu nem se juntou a outro.
    #     Este e o caso que pega o corredor com warp dos dois lados, que o 8
    #     sozinho deixa passar verde (ver o comentario de `componentes`).
    mau += ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                           solidificadas)

    # 9. a calcada nunca fica com faixa de UMA celula, que o kit nao sabe desenhar
    pav = {(i % W, i // W) for i, val in escritas.items()
           if (val & 0x3FF) in ids_calcada}
    for x, y in pav:
        if not ((x, y - 1) in pav or (x, y + 1) in pav):
            mau.append("calcada de uma celula de altura em (%d,%d)" % (x, y))
            break
        if not ((x - 1, y) in pav or (x + 1, y) in pav):
            mau.append("calcada de uma celula de largura em (%d,%d)" % (x, y))
            break

    # 10. variedade de arvore: tres silhuetas e distribuicao SEM periodo
    trocadas = sum(n for k, n in contas["arvores"].items() if k != "a nossa")
    if len([k for k in contas["arvores"] if k != "a nossa"]) < 2:
        mau.append("menos de duas variantes de arvore entraram")
    if trocadas < 60:
        mau.append("so %d arvores trocadas" % trocadas)
    # XADREZ, e o teste tem que olhar o CANTO DO BLOCO 2x2 e nao a celula: cada
    # bloco escreve quatro celulas, duas de cada paridade, entao contar celula
    # da sempre 50/50 e o caso nunca reprova. A conta e por bloco, e em tres
    # eixos: (x+y) par, x par e y par. Se qualquer um deles decidir a variante
    # em mais de 80% dos blocos, a distribuicao virou padrao.
    de_id = {i: a["nome"] for a in carimbos["arvores"] for i in a["ids"]}
    bloco_de = {}
    for i, val in escritas.items():
        nome = de_id.get(val & 0x3FF)
        if nome is None:
            continue
        x, y = i % W, i // W
        # o canto do bloco e a celula do quadrante 0 daquela variante
        if (val & 0x3FF) == [a for a in carimbos["arvores"]
                             if a["nome"] == nome][0]["ids"][0]:
            bloco_de[(x, y)] = nome
    # E O CANTO DO BLOCO que interessa, nao a celula: cada bloco escreve quatro
    # celulas, duas de cada paridade, entao contar celula da sempre 50/50 e o
    # caso nunca reprova. E a conta certa nao e "os blocos estao numa paridade
    # so" (a mata e uma grade alinhada, isso e verdade sempre): e "saber a
    # paridade JA DIZ qual variante caiu ali".
    for rotulo, chave in (("(x+y)", lambda p: (p[0] + p[1]) % 2),
                          ("x", lambda p: (p[0] // 2) % 2),
                          ("y", lambda p: (p[1] // 2) % 2),
                          ("x+y do bloco", lambda p: (p[0] // 2 + p[1] // 2) % 2)):
        tabela = collections.defaultdict(collections.Counter)
        for p, nome in bloco_de.items():
            tabela[chave(p)][nome] += 1
        acertos = sum(c.most_common(1)[0][1] for c in tabela.values())
        total = sum(sum(c.values()) for c in tabela.values())
        if total and len(set(bloco_de.values())) > 1 and acertos / total > 0.8:
            mau.append("a paridade de %s adivinha a variante de arvore em %d de "
                       "%d blocos: virou xadrez" % (rotulo, acertos, total))

    # 11. idempotente
    base2 = list(saida)
    for i in sorted(escritas):
        if base2[i] == escritas[i]:
            base2[i] = v[i]
    if base2 != list(v):
        mau.append("desfazer nao devolve a base")
    _, _, _, _, escritas2, _ = plano_mapa(carimbos, base2)
    if escritas2 != escritas:
        mau.append("segunda passada deu plano diferente")

    # 12. o trabalho tem que valer a pena: a regua precisa cair para 20% ou menos
    a, na, _ = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > 20.0:
        mau.append("a regua ainda marca %.1f%% de carimbo dominante" % b)

    # 13. O QUE ESTA NO DISCO e o que o kit manda. Sem este caso o auto-teste so
    #     confere o que ele mesmo acabou de calcular em memoria: foi a licao da
    #     quinta sabotagem de 44cb13b7b7, em que sabotar o atributo e um tile
    #     DIRETO NO DISCO deixava os sete casos anteriores verdes.
    from PIL import Image
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.convert("P").load()

    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    postas = [l for l in metas if not enchimento(_entradas(meta_snow, l))]
    if not postas:
        print("aviso: o kit ainda nao foi aplicado no tileset; caso 13 nao roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ent in metas.items():
            if _entradas(meta_snow, local) != ent:
                mau.append("metatile %d no disco nao e o do kit" % (512 + local))
            if struct.unpack_from("<H", attr_snow, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (512 + local))
        for vaga, tile in tiles_novos.items():
            if (vaga // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga)
                continue
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % vaga)
        pal = [l.split() for l in
               open(f"{DESTINO}/palettes/%02d.pal" % PAL_NOVA).read().split("\n")[3:]
               if l.strip()]
        if [[int(z) for z in c] for c in pal[:16]] != kit()["paleta"][str(PAL_NOVA)]:
            mau.append("a paleta %d no disco nao e a do kit" % PAL_NOVA)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    print("DEMO VERDE: %d tiles, %d metatiles, 1 paleta, %d celulas de calcada, "
          "%d arvores trocadas, %d moveis, regua de %.1f%% para %.1f%%, 13 casos"
          % (len(tiles_novos), len(metas), contas["calcada"], trocadas,
             contas["solidos"], a, b))
    return 0


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    if "--desfazer" in sys.argv:
        return desfaz()
    roda("--aplicar" in sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
