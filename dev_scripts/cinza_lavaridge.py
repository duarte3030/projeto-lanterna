#!/usr/bin/env python3
"""Refino de `LavaridgeTown` (tema VULCÃO, FUMAROLA E CINZA), no
`gTileset_Lavaridge`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: das 183 células andáveis a pé, **87 (47,5%) são o
metatile 1**, a grama lisa do `gTileset_General`. A vila da Flannery é a única
das quatro regiões que fica na encosta de um vulcão ativo e o chão dela é o
mesmo verde chapado de uma vila de praia: fora a rede de areia que o Emerald já
desenhou ligando as portas, a fonte termal e a parede de rocha do Monte Chimney,
tudo que se pisa é um tapete de dezesseis pixels repetido oitenta e sete vezes.
As 87 células estão TODAS na elevação 3 e TODAS com o atributo `0x0000`
(comportamento zero, `layerType` NORMAL); isso foi medido, não suposto, e é o que
permite tratá-las como um carimbo só.

O QUE ESTA PASSADA NÃO FAZ, e o motivo é medido:

  NÃO ABRE TRILHA. O gerador do motor sabe traçar caminho de custo mínimo entre
  as portas, e foi assim que a rua de `LittlerootTown` nasceu. Aqui isso seria
  uma SEGUNDA rede correndo em paralelo à rede de areia que o Emerald já
  desenhou (autotile 280 a 298, 32 células andáveis, medidas), duas ruas
  dizendo a mesma coisa.
  `trilha=None`, como em `PetalburgCity`.

  NÃO MEXE NA REDE DE AREIA QUE JÁ EXISTE. O metatile 297 (10 células) e o 296,
  o 298, o 281, o 288, o 289 e o 290 são PEÇAS DE BORDA de um autotile que o
  Emerald já pintou: trocar uma delas por uma variante de miolo abriria costura
  na rua. Depois desta passada é o 297 que vira o carimbo dominante, com 10
  células, e isso é resultado aceito e não descuido.

  NÃO IMPORTA UM PIXEL. Ver a seção da FONTE, abaixo.

  NÃO COMPACTA O TILESET, e é isto que fecha o risco dos PINOS DE ANIMAÇÃO. O
  `gTileset_Lavaridge` tem 464 tiles de 512 e 251 deles são mortos, ou seja
  havia vaga de sobra para compactar; só que esta passada gasta ZERO tile, então
  compactar não pagaria nada e mexeria numa renumeração que o
  `src/tileset_anims.c` não conhece. Medido com `dev_scripts/pinos_anim.py`:
  `TilesetAnim_Lavaridge` sobrescreve em tempo de execução as vagas de tile
  **160 a 163 e 288 a 295** do secundário, 12 vagas, e escrever ali não quebra
  build nenhum, não muda um pixel de render estático e só aparece dentro do
  jogo. Como o `tiles.png` e os dezesseis `.pal` saem byte a byte iguais (o
  `git diff` prova), as doze vagas continuam sendo exatamente a animação.

O QUE ESTA PASSADA FAZ, na ordem em que paga:

  1. O CHÃO NOVO É ARRANJO E CÓPIA DO QUE JÁ EXISTE. Nenhum tile, nenhuma cor.
     Só metatile NOVO em vaga que ainda não existia no `metatiles.bin` (o
     arquivo tinha 441 metatiles e CRESCEU, então nenhum metatile antigo foi
     tocado), mais uso DIRETO de dois metatiles que o tileset já desenhou com o
     atributo `0x0000` e a camada de cima vazia, o 788 e o 517. Sobre esses
     dois, o que é medido e o que não é: o 517 não é usado por NENHUM dos treze
     irmãos, e o 788 é usado pelo `MtChimney`, só que como célula SÓLIDA, a
     parede de rocha da montanha. Escrevê-lo em Lavaridge como chão andável não
     muda um pixel do `MtChimney`, porque a colisão mora no `map.bin` de cada
     mapa e o metatile em si não foi alterado; a prova de pixel dos treze
     irmãos, na seção OS IRMÃOS, é o que fecha isso.

  2. A CROSTA VULCÂNICA. Os remendos de TERRA queimada usam o autotile de nove
     peças do `gTileset_General` (259 a 277), que já vem com canto arredondado e
     franja desenhada, e o MIOLO deles recebe PEDRA-POMES: o metatile 788 (rocha
     escura), o 517 (rocha rosada) e mais duas cópias de comportamento zerado do
     519 (rocha com estouro branco) e da camada de baixo do 720 (rocha de
     Jagged Pass). O anel de terra não é enfeite, é o que impede o retalho: a
     rocha rosada está a 96,7 a 138,0 de distância pixel a pixel da GRAMA e a
     42,2 a 64,1 do miolo da TERRA. Encostada na grama ela seria um buraco;
     dentro do anel marrom ela é crosta de lava fria, que é o que a encosta do
     Monte Chimney tem.

  3. A GRAMA CHAMUSCADA. Os remendos de GRAMA GASTA usam o autotile 464 a 482, e
     o miolo deles ganha, além dos arranjos do motor, DUAS peças que o próprio
     `gTileset_Lavaridge` já desenhou: os metatiles 614 e 615. Isso não é sorte:
     eles são feitos dos tiles 249, 250, 297 e 298 com a paleta 2, que são
     EXATAMENTE os tiles do autotile de grama gasta do primário. São arranjos da
     mesma arte que o tileset já trazia prontos, a 35,2 e 41,4 do miolo 473.
     Entram com comportamento zerado (o original é `0x0065`).

  4. O RUÍDO DE ARRANJO na grama que sobra, por espelho e mistura de quadrante
     dos tiles 2 e 3. Custo zero, e é a camada SUTIL: ela não é o enfeite, é o
     fundo, e sem ela o gramado repetiria o mesmo bloco de dezesseis pixels.

  5. A MOBÍLIA DE BEIRA, em células solidificadas, sempre com comportamento
     ZERADO e `layerType` COVERED, sempre encostada em prédio, muro ou rocha.

O QUE FICOU DE FORA, com o motivo medido:

  - Os metatiles 516 e 721 como variante de chão: o 516 tem a camada de baixo
    IDÊNTICA à do 517 (distância 0,0 pixel a pixel; o que muda entre eles é a
    camada de cima) e o 721 tem a camada de baixo idêntica à do 720. Pôr os dois
    pares seria pagar vaga de metatile para desenhar a mesma coisa duas vezes.
  - Os metatiles 697 e 698 ("areia com respingo de água quente", que seriam a
    peça mais temática do tileset inteiro): a faísca branca deles mora na CAMADA
    DE CIMA, e chão com camada de cima em `layerType` NORMAL desenha a faísca
    ACIMA do sprite do jogador. O Emerald aceita isso nas duas células que já
    existem na cidade; abrir a regra para chão novo derrubaria o portão 2 do
    `confere`, que existe justamente para isso. Ficaram de fora como CHÃO.
  - As placas 679 (`gTileset_Lavaridge`) e 305 (`gTileset_General`): placa sem
    texto atrás é promessa que o jogo não cumpre, a mesma razão de Littleroot.
  - Os metatiles 504 e 505 do primário, o pedregulho redondo: atributo `0x10D1`,
    comportamento 209, que é rocha de FORÇA. Remontar a arte dela como enfeite
    poria no gramado uma peça que o jogador vai tentar empurrar a vida inteira.
  - Os arbustos 14, 30 e 31 do primário, que Littleroot usou: Lavaridge é quente
    e seca, e encher a encosta do vulcão de touceira verde é o contrário do que
    esta cidade é. A moita que entra é a 536, a moita ESCURA do próprio
    `gTileset_Lavaridge`.

A FONTE DE ARTE, e a REPROVAÇÃO dos dois candidatos, com a razão SEPARADA por
tipo, porque os dois foram reprovados por motivos diferentes e juntá-los num
número só seria inventar. O índice `/tmp/claude-501/FONTES-POR-TILESET.md` dá
dois candidatos para `secondary/lavaridge`: o `light-platinum` (`0x286D84`, arte
nova 0,959, 7 usos, mapa de amostra g00m02) e o `golden-glazed` (`0x3DF794`,
arte nova 0,871, 10 usos, mapa de amostra g26m32). Os DOIS foram renderizados
com `fontes-mapas/romhacks/ferramentas/render_hack.py` e OLHADOS, e as médias
abaixo saem dos blocos de chão mais uniformes de cada render, achados por
variância e não escolhidos a dedo:

  - `golden-glazed 0x3DF794` é uma CIDADE DE NEVE: chão branco, pinheiro,
    boneco de neve. Média RGB do chão dele (231,235,237), contra os
    (116,197,165) da nossa grama, os (217,201,128) da nossa areia e os
    (159,99,83) da nossa pedra-pomes escura: **140,4, 114,7 e 217,5** de
    distância, todas muito acima do critério de ~50 que Pastoria, Sandgem e
    Hearthome fixaram. REPROVADO por COR e por tema na mesma medida: neve na
    encosta de um vulcão em atividade não é escolha de gosto, é erro de mapa.

  - `light-platinum 0x286D84` é uma CIDADE MODERNA: calçamento ornamental
    cinza-bege com roseta grande, casa de telhado laranja, árvore de outono,
    chafariz e lago. Média RGB do calçamento (185,185,161), que contra a nossa
    pedra-pomes rosada (191,150,141) dá **41,3** e contra a nossa areia
    (217,201,128) dá **48,5**: ele PASSA no critério de cor, e dizer o contrário
    seria fabricar número. A reprovação dele é de DESENHO, e são duas coisas
    medidas: (a) o tema, que é praça de cidade grande e não vila de fonte
    termal, e (b) a BORDA, que ele não tem. O calçamento dele é um tapete de
    padrão contínuo sem as nove peças de transição para grama; importá-lo
    exigiria DESENHAR a borda, que é exatamente a lição que Pastoria pagou
    (textura de chão sem borda de transição vira retalho). A grama do próprio
    hack, medida no mesmo render, fica em (139,187,83), a 85,7 da nossa, então
    nem o par calçamento-mais-grama-dele viria coerente.

O que o chão de Lavaridge precisa não é de outra cinza, é de VARIAÇÃO da cinza
que já existe: o `gTileset_Lavaridge` sozinho tem 441 metatiles desenhados dos
quais a cidade usa 130, e as peças desta passada JÁ VÊM com a borda, porque são
autotile do nosso primário. Por não importar nada, o `CREDITS.md` NÃO É TOCADO:
abrir seção vazia seria mentira de arquivo.

O MOTOR É O DE `mato_littleroot.py`, e isso é decisão, não preguiça. Aquele
arquivo tem o autotile com abertura 3x3, o espalhamento em retângulo, os dois
portões de alcance e de componentes conexos, a régua de cor que corta arranjo
invisível, a conferência com doze regras e o auto-teste com nove sabotagens, e
NADA disso é de Petalburg: as constantes de tileset, carimbo, famílias e móveis
são de módulo e são trocadas aqui. O que Lavaridge precisa e aquele motor não
tem é (a) variante de chão feita de metatile INTEIRO do secundário e não de um
par [a,b,b,a] e (b) móvel remontado a partir do SECUNDÁRIO (o motor só remonta
do primário). As duas coisas entram neste arquivo, depois que o kit do motor sai
pronto, e o `confere` do motor as julga com as mesmas regras.

OS IRMÃOS. O `data/layouts/layouts.json` dá QUINZE layouts com
`secondary_tileset` igual a `gTileset_Lavaridge`, e é o maior número da onda.
TREZE deles têm `map.bin` no disco e um mapa em `data/maps` (LavaridgeTown,
Route112, MtChimney, JaggedPass, FieryPath e os oito andares do MagmaHideout);
os outros dois, `MagmaHideout_3F_1R_Entei_Layout` e
`MagmaHideout_3F_1R_Modern_Layout`, apontam para `map.bin` que NÃO EXISTE no
disco e não têm mapa nenhum. Isso é achado desta passada, não é obra dela, e
não foi consertado aqui: layout sem blockdata é assunto de quem os criou.

A PROVA É DE PIXEL, e não de construção. Os treze foram renderizados com o
`dev_scripts/render_maps.py` contra uma árvore de referência montada do commit
`e80642fd6b` (`git archive`) e comparados imagem a imagem: DOZE saem com o md5
IDÊNTICO, ZERO pixel de diferença em 4.024.064 pixels somados, e só
`LavaridgeTown` muda, 9.770 pixels de 102.400 (9,54%). Conferido de lado, e é o
outro jeito de dizer a mesma coisa: dos 35 metatiles que este kit cria (ids 953
a 987), NENHUM aparece no `map.bin` de nenhum dos doze; só o de Lavaridge os
escreve, e escreve 19 deles, deixando 16 peças de kit sem uso no mapa (288
bytes que ficam no tileset à espera de quem quiser, o preço de gerar o kit
inteiro em vez de gerar peça sob encomenda).

Uso:
    python3 dev_scripts/cinza_lavaridge.py
    python3 dev_scripts/cinza_lavaridge.py --aplicar
    python3 dev_scripts/cinza_lavaridge.py --desfazer
    python3 dev_scripts/cinza_lavaridge.py --demo
    python3 dev_scripts/cinza_lavaridge.py --so-tileset
"""
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import enfeita_cidades as E          # noqa: E402
import mato_littleroot as M          # noqa: E402

ALVO = "LavaridgeTown"
KIT_JSON = f"{RAIZ}/dev_scripts/cinza_lavaridge_kit.json"

# O bloco de teste DESTA rodada é o único que o varredor de corredores pula: os
# casos dele foram escritos DEPOIS do desenho e a partir dele, então tratá-los
# como corredor a preservar seria circular. Esta linha tem que vir DEPOIS do
# `import mato_littleroot`, que põe o bloco 210 aqui ao ser carregado.
E.BLOCO_PROPRIO = "215_cinza_lavaridge.json"

# ------------------------------------------- as constantes do motor, trocadas
M.DESTINO = f"{RAIZ}/data/tilesets/secondary/lavaridge"
M.SECUNDARIO = "gTileset_Lavaridge"
M.PRIMARIO = "gTileset_General"
M.PLANO = f"{RAIZ}/dev_scripts/cinza_lavaridge.json"

# Os TREZE irmãos com `map.bin` e mapa próprios, lidos do layouts.json.
M.IRMAOS = ["LavaridgeTown", "Route112", "MtChimney", "JaggedPass", "FieryPath",
            "MagmaHideout_1F", "MagmaHideout_2F_1R", "MagmaHideout_2F_2R",
            "MagmaHideout_2F_3R", "MagmaHideout_3F_1R", "MagmaHideout_3F_2R",
            "MagmaHideout_3F_3R", "MagmaHideout_4F"]

# o `metatiles.bin` do secundário tem 441 metatiles hoje: o kit vai DEPOIS
M.META_LOCAL_0 = 441
M.CARIMBO = 1                       # a grama lisa do primário
M.CARIMBO2 = 473                    # existe no motor, mas esta cidade não usa
M.BASES_MOVEL = [1]                 # uma base só: a grama
M.SUFIXO_BASE = {1: ""}

# TRÊS famílias, e não as quatro do motor. A quarta (areia) sairia do kit sem
# uso nenhum: esta cidade não recebe remendo de areia, porque o autotile de
# areia é o mesmo da rua que o Emerald já desenhou e remendo solto de areia no
# gramado leria como pedaço de rua caído fora da rua.
M.FAMILIAS = {
    "grama": dict(a=2, b=3, pal=2, fill=1, auto=None),
    "gasta": dict(a=266, b=282, pal=2, fill=473,
                  auto=[464, 465, 466, 472, 473, 474, 480, 481, 482]),
    # o miolo da terra (268) é MB_BERRY_TREE_SOIL (`0x00A0`): entra REMONTADO,
    # com a mesma arte e comportamento ZERADO. Pintá-lo cru mudaria o
    # comportamento de célula ANDÁVEL e poria solo de amoreira sem amoreira.
    "terra": dict(a=268, b=284, pal=3, fill=None,
                  auto=[259, 260, 261, 267, None, 269, 275, 276, 277]),
}

# DIRETO: metatile do primário que JÁ é COVERED, JÁ tem a camada de baixo igual
# à do carimbo (os tiles 2 e 3 na paleta 2) e nenhum irmão precisa dele. Custo
# ZERO: o kit não cria metatile nenhum para eles, só os escreve no mapa.
M.MOVEIS_DIRETOS = [
    dict(nome="pedra",        mt=110),
    dict(nome="pedra virada", mt=111),
    dict(nome="matacao",      mt=224),
    dict(nome="mourao",       mt=307),
]
# O motor remonta a camada de cima do PRIMÁRIO. Lavaridge não usa essa lista: a
# mobília temática dela mora no secundário e entra pela `MOVEIS_SECUNDARIOS`,
# logo abaixo.
M.MOVEIS_REMONTADOS = []
# CERCA: corrida horizontal de células sólidas. As três peças já existem no
# primário, já são COVERED e já têm a camada de baixo do carimbo.
M.CERCA = dict(esq=328, meio=329, dir=330)

# O motor exige Chebyshev 2 entre dois móveis QUAISQUER, e isso é bom numa vila
# larga como Littleroot. Aqui é medido que sufoca: com 2, o plano coloca OITO
# peças e deixa a bica e a bacia da fonte termal de fora; com 1, coloca CATORZE
# e as duas entram. A razão é o tamanho do chão livre: depois dos remendos e das
# 32 células que os eventos e as pernas de teste congelam, sobram cerca de 25
# células de carimbo para mobília, e num vão desse tamanho a distância 2 proíbe
# quase toda segunda peça. Duas pedras a uma célula uma da outra leem como um
# amontoado de rocha, que é o que a encosta de um vulcão tem.
M.ESPACO_ENTRE_MOVEIS = 1

# ------------------------------------------------------- o que o motor não tem
# 1. VARIANTE DE CHÃO feita de metatile INTEIRO. O motor só sabe montar chão a
#    partir de um par [a,b,b,a]; estas peças são arte que o `gTileset_Lavaridge`
#    já desenhou com a camada de baixo cheia e a de cima vazia.
#    `direto=True`  -> o metatile já tem o atributo do carimbo (`0x0000`) e é
#                      escrito no mapa como está: custo ZERO.
#    `direto=False` -> a camada de baixo é copiada para um metatile NOVO com
#                      comportamento ZERADO, porque o original tem o dele.
CHAO_SECUNDARIO = {
    "terra": [
        dict(nome="pedra-pomes escura", de=788, direto=True),
        dict(nome="pedra-pomes rosada", de=517, direto=True),
        dict(nome="pedra-pomes com estouro", de=519, direto=False),
        dict(nome="pedra-pomes de Jagged Pass", de=720, direto=False),
    ],
    "gasta": [
        dict(nome="poca de vapor", de=614, direto=False),
        dict(nome="poca de vapor virada", de=615, direto=False),
    ],
}

# 2. MÓVEL REMONTADO A PARTIR DO SECUNDÁRIO: a camada de CIMA da peça, posta
#    sobre a camada de baixo do carimbo, com `layerType` COVERED e comportamento
#    ZERADO. Sem a remontagem a peça viria com o chão de ROCHA do Monte Chimney
#    embaixo e deixaria um quadrado rosa no meio do gramado.
MOVEIS_SECUNDARIOS = [
    dict(nome="rocha vulcanica",         de=694),
    dict(nome="rocha vulcanica virada",  de=695),
    dict(nome="matacao escuro",          de=712),
    dict(nome="matacao escuro virado",   de=713),
    dict(nome="bica de agua quente",     de=597),
    dict(nome="bacia de pedra",          de=596),
    dict(nome="moita seca",              de=536),
    dict(nome="poste de pedra",          de=653),
    dict(nome="cerca de madeira",        de=687),
]


def _entradas(mt_id):
    return M._entradas_qq(mt_id)


def _attr_de(mt_id):
    import arte_ginasios_sinnoh as G
    if mt_id < 512:
        return G._attrs(M.PRIMARIO)[mt_id]
    return G._attrs(M.SECUNDARIO)[mt_id - 512]


def desenha_kit():
    """O kit do motor MAIS as peças que só Lavaridge tem.

    Devolve `(metas, attrs, kit)` no mesmo formato do motor, para que
    `M.roda`, `M.confere` e `M.demo` funcionem sem saber que houve extensão.
    """
    metas, attrs, kit = KIT_DO_MOTOR()
    proximo = [(max(metas) + 1) if metas else M.META_LOCAL_0]
    base_ent, attr_chao = M.chao_nosso()

    def poe(ents, attr):
        local = proximo[0]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo[0] += 1
        return 512 + local

    # ------------------------------------------------ 1. o CHÃO do secundário
    for nome_fam, pecas in CHAO_SECUNDARIO.items():
        for p in pecas:
            ents = _entradas(p["de"])
            if any(e & 0x3FF for e in ents[4:]) and p["direto"]:
                raise SystemExit(
                    "o chão %d tem arte na camada de cima e foi marcado como "
                    "direto: em layerType NORMAL essa arte desenharia ACIMA do "
                    "jogador" % p["de"])
            if p["direto"]:
                if _attr_de(p["de"]) != attr_chao:
                    raise SystemExit(
                        "o chão direto %d tem atributo 0x%04X e o carimbo tem "
                        "0x%04X" % (p["de"], _attr_de(p["de"]), attr_chao))
                mt = p["de"]
            else:
                # só a camada de BAIXO: a de cima, quando existe, é o que o
                # original desenha acima do jogador e não pode entrar em chão.
                mt = poe(list(ents[:4]) + [0, 0, 0, 0], attr_chao)
            kit["familias"][nome_fam]["variantes"].append(
                dict(nome="%s %s" % (nome_fam, p["nome"]), mt=mt, de=p["de"],
                     direto=p["direto"]))

    # --------------------------------------------- 2. os MÓVEIS do secundário
    vistos = {}
    for m in MOVEIS_SECUNDARIOS:
        cima = tuple(_entradas(m["de"])[4:])
        if not any(e & 0x3FF for e in cima):
            raise SystemExit("o metatile %d não tem arte na camada de cima"
                             % m["de"])
        if cima in vistos:
            raise SystemExit(
                "a camada de cima de %d é IDÊNTICA à de %d: as duas peças "
                "desenhariam a mesma coisa e uma delas é vaga jogada fora"
                % (m["de"], vistos[cima]))
        vistos[cima] = m["de"]
        kit["moveis"].append(dict(nome=m["nome"], remontado=True, de=m["de"],
                                  base=M.CARIMBO,
                                  mt=poe(list(base_ent) + list(cima), 0x1000)))

    if proximo[0] > M.TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % M.TETO_META)

    # A vaga só serve se ainda NÃO EXISTIR no arquivo. Esta conferência é a
    # mesma do motor, repetida aqui porque as peças acima entram depois dela.
    disco = M._ler("metatiles.bin")
    for local, ents in metas.items():
        if local < len(disco) // 16:
            antigo = list(struct.unpack_from("<8H", disco, local * 16))
            if antigo != ents and not (len(set(antigo)) == 1 and antigo[0] <= 2):
                raise SystemExit("a vaga de metatile %d já está ocupada"
                                 % (512 + local))
    return metas, attrs, kit


# O motor chama `desenha_kit` pelo nome de módulo DELE, então a troca é aqui, e
# a função original fica guardada em `KIT_DO_MOTOR` ANTES da troca: sem isso o
# `desenha_kit` daqui chamaria a si mesmo.
KIT_DO_MOTOR = M.desenha_kit
M.desenha_kit = desenha_kit


# ------------------------------------------------------------------ LAVARIDGE
CIDADE = dict(
    # sem trilha: a cidade já tem a rede de areia do Emerald ligando as portas
    trilha=None,
    remendos=[
        # a CROSTA VULCÂNICA: terra queimada com miolo de pedra-pomes
        dict(familia="terra", quantos=2, larg=(4, 5), alt=(3, 3), espaco=3,
             semente=0x1A7A),
        # a GRAMA CHAMUSCADA pelo calor da montanha
        dict(familia="gasta", quantos=2, larg=(3, 4), alt=(3, 3), espaco=3,
             semente=0x1A7B),
    ],
    # as regiões primeiro: o chão de carimbo desta cidade é fita estreita entre
    # a rua de areia, os prédios e a parede de rocha, e só existem 14 cantos de
    # retângulo 3x3 nas 87 células (medido). Mobília posta antes comeria quase
    # todos, como aconteceu em Petalburg e em Oldale.
    regioes_antes=True,
    ruido=[(1, "grama")],
    moveis={"rocha vulcanica": (3, 2), "rocha vulcanica virada": (3, 2),
            "matacao escuro": (2, 3), "matacao escuro virado": (2, 3),
            "bica de agua quente": (1, 4), "bacia de pedra": (1, 4),
            "moita seca": (3, 2), "poste de pedra": (2, 3),
            "cerca de madeira": (2, 3),
            "pedra": (3, 2), "pedra virada": (3, 2), "matacao": (2, 3),
            "mourao": (2, 3)},
    cercas=2, cerca_comp=(3, 4), cerca_espaco=8,
    min_regiao=27,
)


def grava_kit(kit):
    """O kit em JSON, para a mensagem de commit e para o `--desfazer` humano."""
    saida = dict(
        alvo=ALVO, primario=M.PRIMARIO, secundario=M.SECUNDARIO,
        familias={nome: dict(fill=f["fill"], auto=f["auto"],
                             variantes=[dict(nome=c["nome"], mt=c["mt"],
                                             de=c.get("de"),
                                             direto=c.get("direto", False))
                                        for c in f["variantes"]],
                             cortados=f["cortados"])
                  for nome, f in kit["familias"].items()},
        moveis=[dict(nome=m["nome"], mt=m["mt"], de=m.get("de"),
                     remontado=m.get("remontado", False)) for m in kit["moveis"]],
        cerca=kit["cerca"])
    with open(KIT_JSON, "w") as f:
        json.dump(saida, f, indent=1, ensure_ascii=False)


def roda(aplicar):
    metas, attrs, kit = desenha_kit()
    if aplicar:
        grava_kit(kit)
    return M.roda(ALVO, CIDADE, aplicar)


def main():
    if "--desfazer" in sys.argv:
        return M.desfaz(ALVO)
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return M.demo(ALVO, CIDADE)
    if "--so-tileset" in sys.argv:
        metas, attrs, kit = desenha_kit()
        M.grava_tileset(metas, attrs)
        grava_kit(kit)
        print("tileset escrito: %d metatiles novos, 0 tiles, 0 cores" % len(metas))
        return 0
    return roda("--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
