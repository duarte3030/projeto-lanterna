#!/usr/bin/env python3
"""G4 da obra de Galar: os 240 ids de grafico do demake -> OBJ_EVENT_GFX_* nossos.

Uso:
    python3 dev_scripts/tabela_gfx_galar.py            # imprime a tabela e as contagens
    python3 dev_scripts/tabela_gfx_galar.py --demo     # remede a fonte e confere a tabela

Molde: a TROCA_SPRITE de `valida_mapas_sinnoh.py` (id da fonte -> sprite nosso,
uma linha documentada por vez, e um autoteste que recusa destino que esta build
nao desenha).

O QUE A MEDICAO DERRUBOU (leia antes de mexer)
----------------------------------------------
O plano supunha que "os ids ate ~150 do demake tendem a ser os do FireRed base".
MEDIDO em 18/08/2026, e e FALSO:

1. A tabela viva de graficos do demake esta em 0x08EB1000 e tem 240 entradas
   (o teto do FireRed, onde comeca OBJ_EVENT_GFX_VARS). O FireRed original tem
   152. Achada por varredura estrutural (array de ponteiros cujos alvos tem
   width/height em {8,16,32,64,128}, size multiplo de 32 e os quatro ponteiros
   internos dentro da ROM) e CONFIRMADA por referencia de codigo: o literal
   0x08EB1000 aparece em 0x0805F2F4, dentro da area de codigo.
2. Cruzando essa tabela com a geometria de CADA um dos 152 graficos do
   pokefirered (largura, altura, inanimate lidos do
   src/data/object_events/object_event_graphics_info.h), casam 17 de 152, e o
   melhor deslocamento alternativo (-3 a +3) nao passa de 17. Ou seja: NAO ha
   correspondencia de id com o FireRed em nenhum alinhamento. O autor trocou o
   conjunto inteiro por arte propria (o proprio jogador virou 32x32, contra
   16x32 do FireRed).
3. Uma segunda varredura procurou uma tabela ANTIGA sobrevivente (posicao onde
   40+ entradas casassem com a geometria do FireRed): nao existe nenhuma.

Portanto o papel de cada id NAO sai de nome nenhum: foi lido do desenho. Cada
sprite usado foi renderizado da ROM (primeiro quadro, 4bpp, paleta do proprio
grafico, tabela de paletas medida em 0x0828FD30) e classificado a olho em
folha de contato. A geometria medida (16x16 / 16x32 / 32x32 / 64x64 / 128x64)
entra como CONFERENCIA: `--demo` remede a ROM e reprova se ela mudar.

AS TRES CATEGORIAS
------------------
- `pessoa`: gente. Entra no mapa, com o sprite generico mais proximo do que o
  desenho mostra (genero, idade, classe aparente). A arte e do demake e nao tem
  equivalente aqui, entao o que se preserva e o PAPEL, nunca a semelhanca.
- `placa`: o unico id de placa (162, um poste com "?"). Entra como
  OBJ_EVENT_GFX_SIGN.
- `pokemon` e `cenario`: NAO entram. Motivo por linha na tabela. Em resumo:
  Pokemon generico mentiria a especie (mesma lei que deixou os Pokemon de
  Sinnoh de fora, ver NOMES_PROPRIOS em importa_npcs_sinnoh.py), e
  arvore/pedra/Poke Ball/feixe de raide sao objeto que so existe com script:
  mudo, viram bloqueio permanente ou promessa falsa.
"""
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

ROM_DEMAKE = os.path.join(os.path.dirname(RAIZ),
                          "fontes-mapas/galar-swsh/ultimate-plus-v1.2.1.2.gba")
# Medidos nesta ROM, nao chutados. Ver item 1 do docstring.
TABELA_GFX = 0x08EB1000
N_GFX = 240
# Id dinamico: no FireRed 240..255 sao OBJ_EVENT_GFX_VAR_0..F, resolvidos em
# tempo de execucao por var. Sem a cena que carrega a var, nao ha grafico.
PRIMEIRO_VAR = 240

# Sprite da casa: usado quando um id aparecer no mapa e nao estiver na tabela.
# Nao deveria acontecer (o --demo cobre os 190 ids usados), e por isso ele e
# gente comum e nao um sprite chamativo: se aparecer, e um homem a mais numa
# rua, nao um crash.
PADRAO = "OBJ_EVENT_GFX_MAN"

# id da fonte -> (categoria, sprite nosso ou None, papel LIDO DO DESENHO)
#
# Categoria "pessoa"/"placa" entra no mapa; "pokemon"/"cenario" vai para o censo.
# O sprite e sempre da familia FRLG quando existe, porque os tilesets de Galar
# saem do FireRed e misturar o traco de Hoenn com o de Kanto na mesma rua salta
# aos olhos.
TABELA = {
    # --- protagonista e rivais do demake (paleta de jogador, slot 0) ---------
    0:  ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "menina protagonista de gorro (Gloria); 168 usos, o autor reusa o proprio jogador como NPC"),
    7:  ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "a mesma menina, outra pose"),
    8:  ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "a mesma menina, outra pose"),
    9:  ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "a mesma menina, outra pose"),
    12: ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "a mesma menina, outra pose"),
    14: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de cabelo branco e casaco roxo"),
    15: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina de maria-chiquinha preta e laco vermelho"),
    17: ("pessoa", "OBJ_EVENT_GFX_LITTLE_BOY_FRLG", "crianca pequena, 16x16 na fonte (a unica desse tamanho que e gente)"),
    # --- gente comum de rua ------------------------------------------------
    18: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "menino louro de camisa vermelha"),
    19: ("pessoa", "OBJ_EVENT_GFX_BUG_CATCHER_FRLG", "menino de bone verde"),
    20: ("pessoa", "OBJ_EVENT_GFX_MAN", "homem de bone branco e roupa escura"),
    21: ("pessoa", "OBJ_EVENT_GFX_WORKER_M", "homem de uniforme escuro e bone marrom"),
    22: ("pessoa", "OBJ_EVENT_GFX_BEAUTY_FRLG", "moca loura de casaco; 212 usos, o rosto mais comum da regiao"),
    23: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de cabelo castanho"),
    24: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina de cabelo claro e roupa vermelha"),
    25: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "menino de bone preto e camisa verde"),
    26: ("pessoa", "OBJ_EVENT_GFX_MAN", "homem moreno de camisa vermelha"),
    27: ("pessoa", "OBJ_EVENT_GFX_WOMAN_1_FRLG", "moca de avental rosa"),
    28: ("pessoa", "OBJ_EVENT_GFX_WOMAN_2_FRLG", "mulher de cabelo castanho e vestido vermelho"),
    29: ("pessoa", "OBJ_EVENT_GFX_WOMAN_3_FRLG", "mulher de cabelo roxo e vestido branco"),
    30: ("pessoa", "OBJ_EVENT_GFX_GENTLEMAN_FRLG", "homem de terno escuro"),
    31: ("pessoa", "OBJ_EVENT_GFX_OLD_WOMAN_FRLG", "senhora de cabelo lilas e vestido azul"),
    32: ("pessoa", "OBJ_EVENT_GFX_BALDING_MAN", "senhor careca"),
    33: ("pessoa", "OBJ_EVENT_GFX_FISHER", "pessoa de chapeu preto largo e macacao"),
    34: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina de rosa com touca de orelhas"),
    35: ("pessoa", "OBJ_EVENT_GFX_OLD_WOMAN_FRLG", "senhora de cabelo branco e roupa rosa"),
    36: ("pessoa", "OBJ_EVENT_GFX_WOMAN_2_FRLG", "mulher de coque e camisa amarela"),
    37: ("pessoa", "OBJ_EVENT_GFX_WOMAN_3_FRLG", "mulher morena de coque"),
    38: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "menino ruivo de camisa verde"),
    39: ("pessoa", "OBJ_EVENT_GFX_WORKER_M", "pessoa de bone verde e uniforme; 105 usos"),
    40: ("pessoa", "OBJ_EVENT_GFX_WORKER_F", "par feminino do 39, mesmo uniforme; 106 usos"),
    41: ("pessoa", "OBJ_EVENT_GFX_MAN", "homem moreno de camisa azul; 101 usos"),
    42: ("pessoa", "OBJ_EVENT_GFX_WOMAN_2_FRLG", "mulher de coque e roupa vermelha; 100 usos"),
    43: ("pessoa", "OBJ_EVENT_GFX_BEAUTY_FRLG", "moca loura de roupa branca"),
    44: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "menino de bone preto e camisa vermelha"),
    46: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina loura de vestido azul"),
    47: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de camisa azul"),
    48: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina loura de bone azul"),
    49: ("pessoa", "OBJ_EVENT_GFX_ROCKET_M", "punk de moicano e roupa preta (Team Yell)"),
    50: ("pessoa", "OBJ_EVENT_GFX_ROCKET_F", "punk de cabelo rosa (Team Yell)"),
    51: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de camisa azul escura"),
    52: ("pessoa", "OBJ_EVENT_GFX_BUG_CATCHER_FRLG", "crianca de bone azul"),
    53: ("pessoa", "OBJ_EVENT_GFX_WORKER_M", "homem de chapeu escuro e macacao laranja (mineiro)"),
    54: ("pessoa", "OBJ_EVENT_GFX_FISHER", "homem de bandana"),
    55: ("pessoa", "OBJ_EVENT_GFX_SCIENTIST", "pessoa de jaleco branco e oculos"),
    56: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "crianca de bone azul e camisa laranja"),
    57: ("pessoa", "OBJ_EVENT_GFX_BUG_CATCHER_FRLG", "crianca de bone amarelo"),
    58: ("pessoa", "OBJ_EVENT_GFX_POKE_MANIAC_FRLG", "crianca de cabelo cinza"),
    60: ("pessoa", "OBJ_EVENT_GFX_POLICEMAN", "pessoa de bone azul e uniforme; 208 usos, o segundo rosto mais comum"),
    61: ("pessoa", "OBJ_EVENT_GFX_BLACK_BELT_FRLG", "pessoa morena de bone e roupa azul"),
    62: ("pessoa", "OBJ_EVENT_GFX_CAPTAIN", "pessoa de quepe e uniforme branco"),
    64: ("pessoa", "OBJ_EVENT_GFX_NURSE_FRLG", "moca de cabelo rosa e touca (enfermeira)"),
    65: ("pessoa", "OBJ_EVENT_GFX_WORKER_M", "guarda de bone e uniforme"),
    66: ("pessoa", "OBJ_EVENT_GFX_MAN", "homem de cabelo escuro"),
    67: ("pessoa", "OBJ_EVENT_GFX_WOMAN_1_FRLG", "mulher de cabelo castanho"),
    68: ("pessoa", "OBJ_EVENT_GFX_WOMAN_2_FRLG", "moca de vestido vermelho; 142 usos"),
    69: ("pessoa", "OBJ_EVENT_GFX_PICNICKER_FRLG", "menina de bone vermelho; 77 usos"),
    71: ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_M", "pessoa morena de cabelo roxo e roupa dourada"),
    72: ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_M", "pessoa de cabelo roxo agachada; 61 usos"),
    73: ("pessoa", "OBJ_EVENT_GFX_SCIENTIST", "pessoa de jaleco e cabelo castanho"),
    75: ("pessoa", "OBJ_EVENT_GFX_ROCKER", "pessoa de cabelo preto e branco e roupa escura"),
    77: ("pessoa", "OBJ_EVENT_GFX_PICNICKER_FRLG", "menina ruiva de maria-chiquinha"),
    78: ("pessoa", "OBJ_EVENT_GFX_GENTLEMAN_FRLG", "homem de terno claro"),
    79: ("pessoa", "OBJ_EVENT_GFX_OLD_WOMAN_FRLG", "senhora de cabelo branco e vestido"),
    80: ("pessoa", "OBJ_EVENT_GFX_CAMPER_FRLG", "pessoa de chapeu de palha e roupa de campo"),
    81: ("pessoa", "OBJ_EVENT_GFX_SWIMMER_F_LAND", "moca morena de cabelo azul e roupa de banho"),
    82: ("pessoa", "OBJ_EVENT_GFX_POKE_MANIAC_FRLG", "crianca de cabelo branco e camisa laranja"),
    83: ("pessoa", "OBJ_EVENT_GFX_ROCKER", "pessoa de cabelo preto e roupa escura"),
    84: ("pessoa", "OBJ_EVENT_GFX_WOMAN_3_FRLG", "pessoa de chapeu azul e quimono"),
    85: ("pessoa", "OBJ_EVENT_GFX_OLD_MAN_1", "pessoa de cabelo branco e roupa branca"),
    86: ("pessoa", "OBJ_EVENT_GFX_BLACK_BELT_FRLG", "pessoa de cabelo laranja e roupa escura"),
    87: ("pessoa", "OBJ_EVENT_GFX_OLD_MAN_2", "senhor de cabelo branco, oculos e jaleco"),
    88: ("pessoa", "OBJ_EVENT_GFX_WOMAN_1_FRLG", "mulher de cabelo roxo e blusa vermelha"),
    89: ("pessoa", "OBJ_EVENT_GFX_BEAUTY_FRLG", "moca de cabelo claro comprido"),
    90: ("pessoa", "OBJ_EVENT_GFX_WOMAN_3_FRLG", "pessoa morena de cabelo preto"),
    191: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina ruiva, 16x32 na fonte"),
    197: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de cabelo azul, 16x32 na fonte"),
    207: ("pessoa", "OBJ_EVENT_GFX_CHANNELER", "figura encapuzada cinza; o CHANNELER e a unica tunica que temos"),
    223: ("pessoa", "OBJ_EVENT_GFX_SCIENTIST", "pessoa de oculos e cabelo azul"),
    225: ("pessoa", "OBJ_EVENT_GFX_PICNICKER_FRLG", "moca de chapeu branco"),
    229: ("pessoa", "OBJ_EVENT_GFX_OLD_MAN_LYING_DOWN", "pessoa DEITADA no chao; casa em papel e em tamanho (32x32 nos dois lados)"),
    # --- placa --------------------------------------------------------------
    162: ("placa", "OBJ_EVENT_GFX_SIGN", "poste com uma placa de '?'; 29 usos"),
    # --- Pokemon: nao entram (especie desconhecida, e sprite generico mente) --
    16:  ("pokemon", None, "quadrupede pequeno de orelha grande, 16x32; 103 usos"),
    45:  ("pokemon", None, "vulto escuro"),
    59:  ("pokemon", None, "mariposa branca"),
    63:  ("pokemon", None, "bicho de fogo laranja"),
    70:  ("pokemon", None, "bicho escuro pequeno"),
    74:  ("pokemon", None, "bicho de fogo de asas largas"),
    93:  ("pokemon", None, "passaro laranja"),
    94:  ("pokemon", None, "dragao escuro"),
    98:  ("pokemon", None, "morcego roxo"),
    99:  ("pokemon", None, "bicho verde"),
    100: ("pokemon", None, "bicho azul"),
    101: ("pokemon", None, "cogumelo rosa"),
    103: ("pokemon", None, "cristal verde"),
    106: ("pokemon", None, "cabeca amarela"),
    107: ("pokemon", None, "bicho bege redondo"),
    109: ("pokemon", None, "bicho branco"),
    110: ("pokemon", None, "bicho preto e branco"),
    111: ("pokemon", None, "bicho amarelo"),
    112: ("pokemon", None, "bicho marrom"),
    113: ("pokemon", None, "aranha roxa"),
    114: ("pokemon", None, "raposa escura"),
    115: ("pokemon", None, "bicho claro"),
    116: ("pokemon", None, "bicho escuro"),
    117: ("pokemon", None, "bola preta"),
    118: ("pokemon", None, "bicho cinza"),
    119: ("pokemon", None, "bicho verde e laranja"),
    120: ("pokemon", None, "bicho de folhas"),
    121: ("pokemon", None, "bicho marrom de garras"),
    122: ("pokemon", None, "bicho cinza de asas"),
    123: ("pokemon", None, "bicho escuro de crista"),
    124: ("pokemon", None, "bicho de cabelo branco; 54 usos"),
    125: ("pokemon", None, "bicho rosa"),
    126: ("pokemon", None, "bicho laranja"),
    127: ("pokemon", None, "bicho branco redondo"),
    128: ("pokemon", None, "bicho azul claro"),
    129: ("pokemon", None, "bicho dourado"),
    130: ("pokemon", None, "bicho escuro de armadura"),
    131: ("pokemon", None, "bicho de casco"),
    132: ("pokemon", None, "passaro azul"),
    133: ("pokemon", None, "bicho verde e vermelho"),
    134: ("pokemon", None, "bicho de armadura clara"),
    135: ("pokemon", None, "bicho roxo"),
    136: ("pokemon", None, "bicho branco de crista; 63 usos"),
    137: ("pokemon", None, "peixe-serra azul; 72 usos"),
    138: ("pokemon", None, "passaro azul e branco"),
    139: ("pokemon", None, "bicho bege"),
    140: ("pokemon", None, "baleia azul 64x64; 40 usos"),
    141: ("pokemon", None, "bicho pequeno amarelo"),
    142: ("pokemon", None, "bicho de bracos abertos"),
    143: ("pokemon", None, "bicho vermelho e azul"),
    144: ("pokemon", None, "bicho de cabeca verde"),
    145: ("pokemon", None, "morcego rosa 64x64; 32 usos"),
    146: ("pokemon", None, "aranha azul e rosa 64x64"),
    147: ("pokemon", None, "morcego bege; 83 usos"),
    153: ("pokemon", None, "bicho verde de folha"),
    154: ("pokemon", None, "coelho branco"),
    155: ("pokemon", None, "bicho azul de chama"),
    157: ("pokemon", None, "bicho marrom"),
    158: ("pokemon", None, "bicho verde e branco"),
    160: ("pokemon", None, "bicho cinza de cabeca grande"),
    168: ("pokemon", None, "passaro amarelo"),
    169: ("pokemon", None, "bicho marrom de martelo"),
    170: ("pokemon", None, "bicho verde e branco"),
    173: ("pokemon", None, "bicho laranja de garras"),
    176: ("pokemon", None, "bicho marrom de oculos; 24 usos"),
    177: ("pokemon", None, "bicho laranja e preto"),
    179: ("pokemon", None, "coelho cinza 64x64"),
    180: ("pokemon", None, "vulto alado preto 64x64"),
    181: ("pokemon", None, "bicho dourado alado 64x64"),
    182: ("pokemon", None, "dragao laranja"),
    183: ("pokemon", None, "bicho vermelho 64x64"),
    185: ("pokemon", None, "fantasma rosa"),
    190: ("pokemon", None, "bicho verde pequeno, 16x32"),
    198: ("pokemon", None, "bicho amarelo, 16x32"),
    199: ("pokemon", None, "bicho vermelho, 16x32"),
    200: ("pokemon", None, "bicho marrom, 16x32"),
    201: ("pokemon", None, "bicho azul, 16x32"),
    202: ("pokemon", None, "bicho amarelo e vermelho, 16x32; 13 usos"),
    209: ("pokemon", None, "bicho verde, 16x32"),
    221: ("pokemon", None, "bicho cinza espinhoso"),
    224: ("pokemon", None, "bicho vermelho e preto"),
    227: ("pokemon", None, "inseto laranja"),
    228: ("pokemon", None, "inseto amarelo"),
    230: ("pokemon", None, "cacto verde"),
    231: ("pokemon", None, "bicho enorme dormindo, 64x64"),
    232: ("pokemon", None, "corvo de armadura 64x64; 30 usos"),
    233: ("pokemon", None, "passaro lendario vermelho e dourado 64x64"),
    234: ("pokemon", None, "lendario branco e azul 64x64"),
    235: ("pokemon", None, "serpente de metal 64x64; 38 usos"),
    237: ("pokemon", None, "lendario roxo alado 64x64"),
    # --- cenario e objeto de script: nao entram -----------------------------
    91:  ("cenario", None, "feixe de luz de covil de raide, 64x64; 45 usos. Sem a cena de raide e um poste luminoso solido"),
    92:  ("cenario", None, "Poke Ball no chao, 16x16; 74 usos. Item VISIVEL: qual item e so o script sabe, e Poke Ball que nao se pega e promessa falsa"),
    95:  ("cenario", None, "muda de arvore; 17 usos. Obstaculo de campo"),
    97:  ("cenario", None, "pedra redonda 16x16, o unico grafico marcado inanimate na fonte"),
    105: ("cenario", None, "arvore frutifera 64x64; 23 usos. Sem script vira parede permanente"),
    108: ("cenario", None, "trem 64x64"),
    148: ("cenario", None, "monte de pedras 64x64; 155 usos. Obstaculo de Rock Smash sem Rock Smash e caverna trancada para sempre"),
    149: ("cenario", None, "estrela escura no chao 64x64; 27 usos. Marca de covil da Wild Area"),
    150: ("cenario", None, "caixa vermelha 16x16; 56 usos"),
    151: ("cenario", None, "estacao de trem 128x64, o unico grafico desse tamanho"),
    161: ("cenario", None, "caixa de presente"),
    193: ("cenario", None, "anel dourado sobre fundo vermelho, 16x32"),
    196: ("cenario", None, "cristal branco, 16x32"),
    203: ("cenario", None, "marca de X, 16x32"),
    204: ("cenario", None, "marca de X, 16x32"),
    208: ("cenario", None, "Poke Ball 16x16; 20 usos. Mesmo motivo do 92"),
    239: ("cenario", None, "letreiro escrito PIERS, 64x64"),
}

# Ids que a fonte usa e que nao tem entrada na tabela de graficos do demake.
# 255 e OBJ_EVENT_GFX_VAR_F: grafico dinamico, so existe depois que uma cena
# escreve a var. Sem cena, nao ha o que desenhar.
DINAMICOS = {255: "grafico dinamico (VAR_F); so a cena que escreve a var sabe o que e"}


def traduz(gid):
    """(sprite, categoria, papel). sprite None = nao entra no mapa."""
    if gid in TABELA:
        cat, sprite, papel = TABELA[gid]
        return sprite, cat, papel
    if gid >= PRIMEIRO_VAR:
        return None, "dinamico", DINAMICOS.get(gid, "grafico dinamico por var")
    return PADRAO, "pessoa", "id sem linha na tabela; sprite padrao da casa"


# ------------------------------------------------------------------ medicao --

def mede_rom():
    """(id -> (w, h, inanimate)) lido da tabela viva da ROM do demake."""
    rom = open(ROM_DEMAKE, "rb").read()
    base = 0x08000000
    fora = {}
    for i in range(N_GFX):
        p = struct.unpack_from("<I", rom, TABELA_GFX - base + 4 * i)[0]
        o = p - base
        fora[i] = (struct.unpack_from("<h", rom, o + 8)[0],
                   struct.unpack_from("<h", rom, o + 10)[0],
                   bool((rom[o + 12] >> 6) & 1))
    return fora


def sprites_desenhaveis():
    import valida_mapas_sinnoh as V
    return V.sprites_utilizaveis()


def confere(gids_usados=None):
    """Autoteste. Devolve lista de problemas (vazia = tudo certo)."""
    problemas = []
    desenhaveis = sprites_desenhaveis()
    for gid, (cat, sprite, _) in sorted(TABELA.items()):
        if cat in ("pessoa", "placa"):
            if not sprite:
                problemas.append("id %d e %s e nao tem sprite" % (gid, cat))
            elif sprite not in desenhaveis:
                problemas.append("id %d aponta para %s, que esta build nao desenha"
                                 % (gid, sprite))
        elif sprite is not None:
            problemas.append("id %d e %s e nao devia ter sprite" % (gid, cat))
    if PADRAO not in desenhaveis:
        problemas.append("o sprite padrao %s nao e desenhavel" % PADRAO)

    if os.path.exists(ROM_DEMAKE):
        medido = mede_rom()
        for gid in sorted(TABELA):
            if gid not in medido:
                problemas.append("id %d nao existe na tabela da ROM" % gid)
        # A tabela viva tem 240 entradas: se a ROM mudar de versao e ela
        # encolher, o numero abaixo muda e o caso morre aqui, nao no jogo.
        if len(medido) != N_GFX:
            problemas.append("tabela da ROM tem %d entradas, esperado %d"
                             % (len(medido), N_GFX))
    else:
        problemas.append("ROM do demake nao encontrada em %s" % ROM_DEMAKE)

    if gids_usados:
        faltando = sorted(g for g in gids_usados
                          if g not in TABELA and g < PRIMEIRO_VAR)
        if faltando:
            problemas.append("ids usados sem linha na tabela: %s" % faltando)
    return problemas


def main():
    demo = "--demo" in sys.argv
    problemas = confere()
    cats = {}
    for gid, (cat, sprite, _) in TABELA.items():
        cats.setdefault(cat, []).append(gid)
    print("tabela de gfx de Galar: %d ids classificados de %d na tabela da ROM"
          % (len(TABELA), N_GFX))
    for cat in ("pessoa", "placa", "pokemon", "cenario"):
        ids = cats.get(cat, [])
        print("  %-8s %3d ids" % (cat, len(ids)))
    destinos = sorted({s for c, s, _ in TABELA.values() if s})
    print("  sprites nossos usados: %d (%s)" % (len(destinos), ", ".join(
        d.replace("OBJ_EVENT_GFX_", "") for d in destinos)))
    if problemas:
        print("\nPROBLEMAS:")
        for p in problemas:
            print("  -", p)
        return 1
    print("\nautoteste: OK")
    if demo:
        medido = mede_rom()
        print("geometria medida na ROM (amostra):")
        for gid in (0, 17, 92, 148, 151, 162, 229):
            print("   id %3d %s  %s" % (gid, medido[gid], TABELA[gid][2][:60]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
