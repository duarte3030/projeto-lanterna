#!/usr/bin/env python3
"""Lente do CARIMBO DE COMPORTAMENTO: refino de arte não pode mudar regra de jogo.

POR QUE ELA EXISTE
------------------
O PRD do REFINO manda, no passo 6 da seção 3.3, conferir que os bits 10 a 15 de
cada palavra do `map.bin` (colisão e elevação) ficam idênticos quando a arte de
um mapa é trocada. Em 06/09/2026 o `de_para_metatiles.py` mostrou que ISSO NÃO
BASTA: o COMPORTAMENTO do metatile (grama alta, água, porta, escada, degrau,
gelo) não mora no `map.bin`, mora no `metatile_attributes.bin` do TILESET, nos
bits 0 a 7 (9 no formato FireRed), com o tipo de camada nos bits 12 a 15. Ver
`include/global.fieldmap.h`.

Consequência: dá para trocar a arte com a colisão intacta e mesmo assim a grama
alta parar de gerar encontro, a água parar de aceitar Surf, a porta deixar de ser
porta e o degrau deixar de pular, EM SILÊNCIO, com o passo 6 do PRD todo verde.

O condutor Fable tornou a regra dupla obrigatória em todo mapa tocado pelo
refino, e mandou que ela virasse lente PERMANENTE em vez de checagem de uma
rodada. É este arquivo.

COMO ELA MEDE
-------------
Para cada mapa da lista carimbada, dois resumos criptográficos por célula:

    carimbo de COMPORTAMENTO   (behavior, layerType) de cada célula, na ordem de
                               leitura do `map.bin`, resolvido pelo
                               `metatile_attributes.bin` do par de tilesets do
                               layout. É o que o motor consulta para decidir
                               encontro, Surf, porta, escada e degrau.
    carimbo de CAMINHO         os bits 10 a 15 de cada palavra do `map.bin`
                               (colisão e elevação). É o passo 6 do PRD.

Os dois ficam gravados em `carimbo_comportamento.json`, e a lente refaz a conta
a partir dos arquivos e compara. Divergência é achado.

O QUE ELA NÃO MEDE
------------------
Ela não olha desenho: trocar o tile de um metatile sem mudar o atributo é MUDA
para esta lente, e é assim de propósito, porque refino de arte é exatamente isso.
Ela também não roda o jogo; quem prova comportamento é a suíte do emulador.

REBASE, e por que ele é deliberado
----------------------------------
Mudança legítima de colisão ou de comportamento (um conserto de caminho, uma
porta nova) faz a lente acusar, e tem que fazer. Nesse caso o carimbo é
regravado A MÃO, com `--carimba`, no MESMO commit da mudança, e o motivo vai na
mensagem. Carimbo regravado por reflexo, para "limpar o vermelho", devolve a
lente ao nada.

USO
---
    python3 dev_scripts/qa/lente_carimbo.py            # varre e imprime
    python3 dev_scripts/qa/lente_carimbo.py --carimba  # regrava a linha de base
    python3 dev_scripts/qa/lente_carimbo.py --demo     # autoteste
"""
import hashlib
import json
import os
import struct
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
RAIZ_DEV = os.path.dirname(AQUI)
if RAIZ_DEV not in sys.path:
    sys.path.insert(0, RAIZ_DEV)

import comum  # noqa: E402

REPO = comum.RAIZ
CARIMBO = os.path.join(AQUI, "carimbo_comportamento.json")

# Ver include/global.fieldmap.h.
ATTR_BEHAVIOR_EMERALD = 0x00FF
ATTR_BEHAVIOR_FRLG = 0x01FF
ATTR_LAYER_MASK = 0xF000
ATTR_LAYER_SHIFT = 12
# No formato de 4 bytes do FireRed a camada mora nos bits 29 e 30.
ATTR_LAYER_MASK_FRLG = 0x60000000
ATTR_LAYER_SHIFT_FRLG = 29

MAPGRID_METATILE_ID_MASK = 0x03FF
MAPGRID_RESTO_SHIFT = 10

# Os mapas que o REFINO toca, e por isso os que ficam carimbados. A lista cresce
# a cada onda: mapa que ganha arte nova entra AQUI e o carimbo dele é gravado
# ANTES da troca, senão a lente nasce cega justo no mapa que ela existe para
# vigiar. Fora do refino ninguém precisa carimbar mapa nenhum.
SOB_CARIMBO = (
    # Sinnoh: a régua de pobreza de 06/09/2026, da mais lisa para a menos.
    "SnowpointCity", "CelesticTown", "SolaceonTown", "OreburghCity",
    "JubilifeCity", "TwinleafTown", "SunyshoreCity", "VeilstoneCity",
    "SandgemTown", "PastoriaCity", "FloaromaTown", "EternaCity",
    "CanalaveCity", "HearthomeCity",
    # Os outros mapas dos mesmos tilesets secundários, que o import de kit pode
    # sujar sem ninguém olhar: eles não mudam, e é isso que a lente afirma.
    "AcuityLakefront", "LakeAcuity", "Route216", "Route217",
    # Johto: os alvos da onda 3.
    "CianwoodCity", "BlackthornCity", "GoldenrodCity", "EcruteakCity",
    "Mahoganytown", "OlivineCity", "AzaleaTown", "VioletCity",
    "Route41", "Route44", "Route45", "Route47", "Route48", "Route26",
    "MtSilver_MountainSide",
    # Hoenn: a onda 4 do REFINO. ATE 09/09/2026 A LENTE ERA MUDA EM HOENN, e
    # isso era buraco e nao escolha: as primeiras cidades da onda fecharam com
    # "0 achado(s)" que era 0 porque NENHUM mapa de Hoenn estava nesta lista,
    # ou seja a lente nunca as mediu. As duas frentes da onda acharam o mesmo
    # buraco no mesmo dia e cada uma tapou a sua parte; aqui as duas listas
    # entram juntas.
    #
    # As tres cidades do gTileset_Petalburg vem com as TRES ROTAS que dividem o
    # mesmo secundario com elas. As rotas entram pela mesma razao das de Sinnoh
    # e de Johto: elas NAO mudam, e e isso que a lente afirma. Enquanto a onda 4
    # nao chegar nelas, um achado numa Route101 e respingo de kit, nunca desenho
    # novo. Sootopolis nao traz irmao porque o `gTileset_Sootopolis` e de UM
    # mapa so.
    "LittlerootTown", "PetalburgCity", "OldaleTown",
    "Route101", "Route102", "Route103",
    "SootopolisCity",
    # Dewford entra com os CINCO irmaos do gTileset_Dewford, e ela e o caso em
    # que a lente mais serve: e a unica cidade desta onda que COMPACTOU o
    # tileset, ou seja renumerou as vagas de tile por baixo de 379 metatiles. A
    # compactacao nao pode mudar comportamento nenhum, e e exatamente isso que
    # o carimbo afirma daqui para a frente.
    "DewfordTown", "Route105", "Route106", "Route107",
    "BirthIsland_Exterior", "NavelRock_Exterior",
    # Lavaridge entra com os DOZE irmaos do gTileset_Lavaridge que tem mapa em
    # disco. O layouts.json lista QUINZE layouts com esse secundario, e dois
    # deles (MagmaHideout_3F_1R_Entei_Layout e MagmaHideout_3F_1R_Modern_Layout)
    # apontam para um `map.bin` que NAO EXISTE no disco: ficam de fora porque
    # nao ha o que carimbar, e isso e achado registrado, nao conserto.
    "LavaridgeTown", "Route112", "MtChimney", "JaggedPass", "FieryPath",
    "MagmaHideout_1F", "MagmaHideout_2F_1R", "MagmaHideout_2F_2R",
    "MagmaHideout_2F_3R", "MagmaHideout_3F_1R", "MagmaHideout_3F_2R",
    "MagmaHideout_3F_3R", "MagmaHideout_4F",
    # MauvilleCity entra com QUATRO dos seis irmaos do gTileset_Mauville. O
    # layouts.json lista SETE layouts com esse secundario e um deles,
    # LAYOUT_ROUTE111_NO_MIRAGE_TOWER, e layout SEM pasta em data/maps/: ele tem
    # `map.bin` proprio e nao tem `map.json`, entao a lente nao consegue medi-lo
    # (ela le o layout pelo map.json do mapa) e ele ficaria MUDO, que e achado.
    # Fica de fora por isso, e a prova de que ele nao mudou e outra, feita no
    # commit: os 55 metatiles que o kit escreve nao aparecem em nenhuma das 230
    # celulas distintas dele. VerdanturfTown, a segunda cidade deste secundario,
    # entra no commit DELA, e nao aqui: carimbar o mapa dela antes de a passada
    # dela rodar deixaria o carimbo velho um commit inteiro.
    "MauvilleCity", "Route110", "Route111", "Route117", "Route118",
    # VerdanturfTown e a SEGUNDA cidade do gTileset_Mauville, e entra no commit
    # dela e nao no de Mauville: carimbar o mapa dela um commit antes de a
    # passada dela rodar deixaria o carimbo velho de proposito. Os quatro irmaos
    # ja entraram acima e o carimbo deles NAO muda aqui, porque esta passada nao
    # toca o tileset: ela so escreve o data/layouts/VerdanturfTown/map.bin.
    "VerdanturfTown",
    # Rustboro entra com os SETE irmaos do gTileset_Rustboro que tem mapa em
    # disco. O layouts.json lista NOVE layouts com esse secundario, e um deles
    # (PetalburgWoods_Old_Layout) aponta para
    # `data/layouts/PetalburgWoods_Old/map.bin`, arquivo que NAO EXISTE: fica de
    # fora porque nao ha o que carimbar, e isso e achado registrado, nao
    # conserto. Nenhum `blockdata_filepath` se repete entre os oito, ou seja
    # nenhum deles empresta o `map.bin` de outro.
    #
    # Rustboro e, junto com Dewford, a segunda cidade da onda que COMPACTOU o
    # tileset: a renumeracao de vaga de tile passou por baixo de 350 metatiles e
    # de oito mapas. Compactacao nao pode mudar comportamento nenhum, e e
    # exatamente isso que o carimbo afirma daqui para a frente.
    "RustboroCity", "Route104", "Route116", "PetalburgWoods",
    "Route104_Prototype", "SouthernIsland_Exterior",
    "SouthernIsland_Interior", "FarawayIsland_Entrance",
)


# ---------------------------------------------------------------------------
def layouts():
    with open(os.path.join(REPO, "data/layouts/layouts.json"), encoding="utf-8") as f:
        return {l["id"]: l for l in json.load(f)["layouts"]}


_PASTAS = None


def pasta_do_tileset(rotulo):
    """gTileset_Snowpoint -> caminho absoluto da pasta, ou None.

    Delegado ao `valida_warp_tile.py`, que já resolve apelido de asset
    (ASSET_ALIAS) e alias de alias. Duas verdades de leitura de tileset é o tipo
    de coisa que diverge calada.
    """
    global _PASTAS
    if not rotulo or rotulo == "0":
        return ""
    if _PASTAS is None:
        import valida_warp_tile as vwt
        vwt.RAIZ = REPO
        vwt.PASTAS = None
        _PASTAS = vwt._mapa_de_pastas()
    return _PASTAS.get(rotulo)


def atributos(rotulo):
    """Devolve lista de (behavior, layerType) por metatile local do tileset.

    A largura da entrada sai da divisão do `metatile_attributes.bin` pelo número
    de metatiles do `metatiles.bin` (16 bytes cada): 2 no Emerald e no Ruby, 4 no
    FireRed. Deduzir pela base do jogo em vez de medir é a armadilha que já
    custou uma rodada nesta obra.
    """
    d = pasta_do_tileset(rotulo)
    if not d:
        return None
    pa, pm = os.path.join(d, "metatile_attributes.bin"), os.path.join(d, "metatiles.bin")
    if not (os.path.exists(pa) and os.path.exists(pm)):
        return None
    n = os.path.getsize(pm) // 16
    if not n:
        return []
    b = open(pa, "rb").read()
    largura = len(b) // n if n else 0
    fora = []
    if largura == 4:
        for i in range(0, n * 4, 4):
            v = struct.unpack_from("<I", b, i)[0]
            fora.append((v & ATTR_BEHAVIOR_FRLG,
                         (v & ATTR_LAYER_MASK_FRLG) >> ATTR_LAYER_SHIFT_FRLG))
    elif largura == 2:
        for i in range(0, n * 2, 2):
            v = struct.unpack_from("<H", b, i)[0]
            fora.append((v & ATTR_BEHAVIOR_EMERALD,
                         (v & ATTR_LAYER_MASK) >> ATTR_LAYER_SHIFT))
    else:
        return None
    return fora


def carimbos(celulas, atrib):
    """(sha do comportamento, sha do caminho) de uma lista de palavras do map.bin.

    `atrib` é a função índice global de metatile -> (behavior, layerType), e ela
    devolve None quando o índice não existe em tileset nenhum. Índice sem
    atributo entra no carimbo como a marca 0xFFFF/0xFF, e NÃO é silenciado: se um
    import de kit apontar para vaga vazia, o carimbo muda e a lente acusa.
    """
    comp = bytearray()
    cam = bytearray()
    for palavra in celulas:
        mt = palavra & MAPGRID_METATILE_ID_MASK
        par = atrib(mt)
        if par is None:
            comp += struct.pack("<HB", 0xFFFF, 0xFF)
        else:
            comp += struct.pack("<HB", par[0] & 0xFFFF, par[1] & 0xFF)
        cam.append((palavra >> MAPGRID_RESTO_SHIFT) & 0x3F)
    return (hashlib.sha256(bytes(comp)).hexdigest(),
            hashlib.sha256(bytes(cam)).hexdigest())


def mede(nome, mapa_de_layouts=None):
    """Carimbo de um mapa da árvore. Devolve dict, ou None quando não dá para medir."""
    caminho = os.path.join(REPO, "data/maps", nome, "map.json")
    if not os.path.exists(caminho):
        return None
    with open(caminho, encoding="utf-8") as f:
        m = json.load(f)
    L = (mapa_de_layouts or layouts()).get(m.get("layout"))
    if not L:
        return None
    bin_path = os.path.join(REPO, L.get("blockdata_filepath", ""))
    if not os.path.exists(bin_path):
        return None
    w, h = L["width"], L["height"]
    dados = open(bin_path, "rb").read()
    if len(dados) < w * h * 2:
        return None
    celulas = struct.unpack_from("<%dH" % (w * h), dados, 0)

    pri = atributos(L.get("primary_tileset"))
    sec = atributos(L.get("secondary_tileset"))
    if pri is None:
        return None
    n_pri = len(pri)

    def atrib(mt):
        if mt < n_pri:
            return pri[mt]
        if sec is None:
            return None
        i = mt - n_pri
        return sec[i] if i < len(sec) else None

    sha_comp, sha_cam = carimbos(celulas, atrib)
    return dict(w=w, h=h, celulas=w * h, layout=m.get("layout"),
                primario=L.get("primary_tileset"), secundario=L.get("secondary_tileset"),
                comportamento=sha_comp, caminho=sha_cam)


# ---------------------------------------------------------------------------
def carrega_base():
    if not os.path.exists(CARIMBO):
        return {}
    with open(CARIMBO, encoding="utf-8") as f:
        return json.load(f).get("mapas", {})


_REGIOES = None


def regiao_de(nome):
    global _REGIOES
    if _REGIOES is None:
        import lente_warps
        tabela = lente_warps.tabela_de_constantes()
        _REGIOES = {}
        for mapa, (_const, grupo) in tabela.items():
            _REGIOES[mapa] = "Hoenn"
            for chave, r in lente_warps.GRUPO_DE_REGIAO:
                if chave in grupo:
                    _REGIOES[mapa] = r
                    break
    return _REGIOES.get(nome, "comum")


def varre():
    """Devolve (achados, censo). Achado é divergência contra a linha de base."""
    base = carrega_base()
    mapa_de_layouts = layouts()
    achados = []
    censo = dict(carimbados=len(base), medidos=0, mudos=0)
    for nome, esperado in sorted(base.items()):
        agora = mede(nome, mapa_de_layouts)
        if agora is None:
            censo["mudos"] += 1
            achados.append(dict(regra="K4", classe="trava", regiao=regiao_de(nome),
                                mapa=nome, detalhe="mapa carimbado sumiu da árvore "
                                "ou não pode ser medido"))
            continue
        censo["medidos"] += 1
        if agora["celulas"] != esperado.get("celulas"):
            achados.append(dict(regra="K3", classe="trava", regiao=regiao_de(nome),
                                mapa=nome,
                                detalhe="o mapa mudou de tamanho: %sx%s virou %sx%s"
                                % (esperado.get("w"), esperado.get("h"),
                                   agora["w"], agora["h"])))
            continue
        if agora["comportamento"] != esperado.get("comportamento"):
            achados.append(dict(regra="K1", classe="trava", regiao=regiao_de(nome),
                                mapa=nome,
                                detalhe="o COMPORTAMENTO de alguma célula mudou "
                                "(behavior ou layerType)"))
        if agora["caminho"] != esperado.get("caminho"):
            achados.append(dict(regra="K2", classe="trava", regiao=regiao_de(nome),
                                mapa=nome,
                                detalhe="a COLISÃO ou a ELEVAÇÃO de alguma célula "
                                "mudou (bits 10 a 15)"))
    return achados, censo


def celulas_divergentes(nome):
    """Onde exatamente o mapa divergiu, para o conserto não ser adivinhação.

    Refaz a comparação célula a célula contra o carimbo, e devolve a lista de
    (x, y, o que mudou). Só serve quando o mapa não mudou de tamanho.
    """
    base = carrega_base().get(nome)
    if not base:
        return []
    caminho_json = os.path.join(REPO, "data/maps", nome, "map.json")
    if not os.path.exists(caminho_json):
        return []
    # Não há como reconstruir a célula antiga a partir de um sha; o que esta
    # função entrega é a lista de células do mapa ATUAL com o comportamento
    # delas, para o operador comparar com o `.antes` que o script de refino
    # guardou. Sem `.antes`, ela devolve vazio e diz por quê.
    antes = os.path.join(REPO, "data/maps", nome, "map.bin.antes")
    L = layouts().get(json.load(open(caminho_json, encoding="utf-8"))["layout"])
    if not (L and os.path.exists(antes)):
        return []
    w, h = L["width"], L["height"]
    velho = struct.unpack_from("<%dH" % (w * h), open(antes, "rb").read(), 0)
    novo = struct.unpack_from(
        "<%dH" % (w * h), open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read(), 0)
    pri = atributos(L.get("primary_tileset")) or []
    sec = atributos(L.get("secondary_tileset")) or []

    def atrib(mt):
        if mt < len(pri):
            return pri[mt]
        i = mt - len(pri)
        return sec[i] if i < len(sec) else None

    fora = []
    for i, (a, b) in enumerate(zip(velho, novo)):
        x, y = i % w, i // w
        if (a >> MAPGRID_RESTO_SHIFT) != (b >> MAPGRID_RESTO_SHIFT):
            fora.append((x, y, "caminho"))
        elif atrib(a & MAPGRID_METATILE_ID_MASK) != atrib(b & MAPGRID_METATILE_ID_MASK):
            fora.append((x, y, "comportamento"))
    return fora


def carimba():
    """Regrava a linha de base a partir da árvore. Deliberado, nunca automático."""
    mapa_de_layouts = layouts()
    mapas, mudos = {}, []
    for nome in SOB_CARIMBO:
        m = mede(nome, mapa_de_layouts)
        if m is None:
            mudos.append(nome)
            continue
        mapas[nome] = m
    fora = dict(
        aviso="Gerado por dev_scripts/qa/lente_carimbo.py --carimba. Regravar "
              "isto sem um motivo escrito no commit desliga a lente.",
        mapas=mapas)
    # Escreve em temporário e renomeia: lição 6 da rodada 13, `open(..., \"w\")`
    # antes da validação trunca o arquivo quando a validação cai.
    tmp = CARIMBO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(fora, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    os.replace(tmp, CARIMBO)
    print("carimbados %d mapas em %s" % (len(mapas), CARIMBO))
    if mudos:
        print("NAO medidos (%d): %s" % (len(mudos), ", ".join(mudos)))
    return 0


# ---------------------------------------------------------------------------
def demo():
    """Autoteste com mutação plantada: se a lente parar de morder, cai."""
    ruim = 0

    def falso(msg):
        nonlocal ruim
        ruim = 1
        print(f"  lente_carimbo DEMO: {msg}")

    # 1. As máscaras têm que bater com o header, para o dia em que o formato do
    #    atributo mudar e ninguém avisar esta lente.
    hdr = open(os.path.join(REPO, "include/global.fieldmap.h"), encoding="utf-8").read()
    if "0x00FF" not in hdr or "0xF000" not in hdr:
        falso("global.fieldmap.h nao tem mais as mascaras 0x00FF e 0xF000")

    # 2. O carimbo separa comportamento de caminho. Trocar o metatile por um de
    #    MESMO comportamento não pode mexer no carimbo de comportamento; trocar
    #    por um de comportamento diferente TEM que mexer. E mexer na colisão só
    #    pode mexer no carimbo de caminho.
    tab = {1: (0, 0), 2: (0, 0), 3: (33, 0), 4: (0, 1)}
    at = lambda mt: tab.get(mt)                                   # noqa: E731
    base_comp, base_cam = carimbos([1, 1, 1, 1], at)
    igual_comp, igual_cam = carimbos([1, 2, 1, 2], at)
    if (igual_comp, igual_cam) != (base_comp, base_cam):
        falso("trocar por metatile de MESMO (behavior, layer) mudou o carimbo")
    outro_comp, outro_cam = carimbos([1, 3, 1, 1], at)
    if outro_comp == base_comp:
        falso("mudanca de BEHAVIOR passou batido: a lente esta cega")
    if outro_cam != base_cam:
        falso("mudanca de behavior sujou o carimbo de CAMINHO, que nao mudou")
    camada_comp, _ = carimbos([1, 4, 1, 1], at)
    if camada_comp == base_comp:
        falso("mudanca de layerType passou batido")
    _, colisao_cam = carimbos([1, 1 | (1 << 10), 1, 1], at)
    if colisao_cam == base_cam:
        falso("mudanca de COLISAO passou batido")
    _, elev_cam = carimbos([1, 1 | (3 << 12), 1, 1], at)
    if elev_cam == base_cam:
        falso("mudanca de ELEVACAO passou batido")

    # 3. Índice de metatile sem atributo (vaga vazia do tileset) tem que mudar o
    #    carimbo, senão import de kit apontando para o vazio passa calado.
    vazio_comp, _ = carimbos([1, 99, 1, 1], at)
    if vazio_comp == base_comp:
        falso("metatile sem atributo entrou como se fosse igual")

    # 4. A linha de base tem que existir e cobrir os mapas do refino.
    base = carrega_base()
    if len(base) < 20:
        falso(f"a linha de base tem so {len(base)} mapas: alguem a esvaziou")
    for obrigatorio in ("SnowpointCity", "CanalaveCity"):
        if obrigatorio not in base:
            falso(f"{obrigatorio} saiu da linha de base, e ele e alvo do refino")

    # 5. A árvore tem que estar limpa contra o carimbo.
    achados, censo = varre()
    if censo["mudos"]:
        falso(f"{censo['mudos']} mapa(s) carimbado(s) nao pode(m) ser medido(s)")
    if achados:
        falso("%d divergencia(s): %s" % (
            len(achados), ", ".join(sorted({a["mapa"] for a in achados}))[:200]))

    if not ruim:
        print("demo ok")
    return ruim


def main():
    if "--carimba" in sys.argv:
        return carimba()
    if "--demo" in sys.argv:
        return demo()
    achados, censo = varre()
    print("carimbados %(carimbados)d, medidos %(medidos)d, mudos %(mudos)d" % censo)
    for a in achados:
        print("  %-4s %-24s %s" % (a["regra"], a["mapa"], a["detalhe"]))
    print("%d achado(s)" % len(achados))
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
