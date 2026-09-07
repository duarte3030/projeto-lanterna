#!/usr/bin/env python3
"""De-para de metatiles entre dois pares de tilesets, para o REFINO de arte.

POR QUE ELE EXISTE
------------------
O PRD do REFINO (secao 3.3, passo 2, e risco 7) diz que trocar a arte de um mapa
sem mexer na planta exige, para cada metatile do tileset ANTIGO usado no
`map.bin`, achar o metatile do tileset NOVO que representa a mesma coisa, e que
isso e "trabalho de olho, e nao tem script que faca". Tem: este.

O FURO DO PRD QUE ESTE SCRIPT FECHA
-----------------------------------
A regra 4 da secao 4 e o passo 6 da secao 3.3 mandam conferir so os bits 10 a 15
do `map.bin` (colisao e elevacao). ISSO NAO BASTA. O COMPORTAMENTO do metatile
(grama alta, agua, porta, escada, degrau, gelo, encontro selvagem) nao mora no
`map.bin`: mora no `metatile_attributes.bin` do TILESET, nos bits 0 a 7
(`METATILE_ATTR_BEHAVIOR_MASK`), com o tipo de camada nos bits 12 a 15
(`METATILE_ATTR_LAYER_MASK`). Ver `include/global.fieldmap.h`.

Consequencia: da para trocar o tileset com os bits de colisao intactos e mesmo
assim a grama alta parar de gerar encontro, a agua parar de aceitar Surf, a porta
deixar de ser porta e o degrau deixar de pular, EM SILENCIO, com a verificacao do
PRD toda verde.

Por isso a regra dura desta ferramenta: **o de-para preserva
`(behavior, layerType)`, celula a celula, em 100% das celulas do mapa.** Uma
celula diferente reprova a conversao. Isso e aplicado duas vezes, de proposito:
como filtro na hora de escolher o candidato, e como verificacao independente
depois (`--verifica`), que refaz a conta a partir dos arquivos.

DUAS VERDADES DE DESENHO SAO PROIBIDAS (regra 5 da secao 4 do PRD), entao o
desenhador aqui e o do `render_maps.py`, importado: `carregar_tileset`,
`entradas_metatile`, `desenhar_tile`, `resolver_tile`, `carregar_paletas`.

SAIDAS
------
1. O plano, em JSON: de-para, distancia de cada par e lista de pendencias.
2. A folha de contato, em PNG: os pares lado a lado, ampliados 4x, o antigo a
   esquerda e o novo a direita, da pior distancia para a melhor. E ela que
   transforma o "trabalho de olho" em cinco minutos de conferencia.

USO
---
    # planeja (nao escreve no repo, so no diretorio de saida)
    python3 dev_scripts/de_para_metatiles.py \
        --pri-origem gTileset_GeneralSinnoh --pri-destino gTileset_General \
        --mapas SnowpointCity CanalaveCity --limiar 0.16

    # aplica (reescreve map.bin e layouts.json; guarda backup .antes)
    ... --aplica

    # confere um mapa ja convertido, ou um plano ainda nao aplicado
    python3 dev_scripts/de_para_metatiles.py --verifica --plano SAIDA/plano.json
    python3 dev_scripts/de_para_metatiles.py --verifica --mapas SnowpointCity

    python3 dev_scripts/de_para_metatiles.py --demo
    python3 dev_scripts/de_para_metatiles.py --autoteste

Tileset pode ser um rotulo instalado no repo (`gTileset_Nome`) ou uma pasta solta
de tileset extraido (qualquer caminho com `tiles.png`, `palettes/`,
`metatiles.bin` e `metatile_attributes.bin`).
"""
import argparse
import json
import math
import os
import re
import struct
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw

import render_maps as rm

REPO = rm.REPO
META_PX = rm.META_PX

# Ver include/global.fieldmap.h. O `--autoteste` confere estes dois numeros
# contra o header, para o dia em que alguem mudar o formato do atributo.
METATILE_ATTR_BEHAVIOR_MASK = 0x00FF
METATILE_ATTR_LAYER_MASK = 0xF000
METATILE_ATTR_LAYER_SHIFT = 12

# 10 bits baixos do map.bin = indice de metatile; 10 a 15 = colisao e elevacao.
MAPGRID_METATILE_ID_MASK = 0x03FF
MAPGRID_RESTO_MASK = 0xFC00

SAIDA_PADRAO = os.environ.get(
    "SAIDA_DE_PARA",
    "/Users/duarte/Documents/CLAUDE/Claude Workspace - Pokemon Rom Hacks/"
    "Pokemon Claude/amostras-tileset/refino/de-para",
)

# Pesos da metrica de distancia visual.
#
# COR pesa mais do que ESTRUTURA porque a cor media dos quadrantes 8x8 e o que
# separa grama de calcada, areia de agua, telhado vermelho de telhado azul: e a
# pergunta "isso e a mesma coisa?" que o de-para precisa responder. A estrutura
# (magnitude de gradiente) entra como desempate, porque ela e o que separa
# telhado de parede e borda de miolo quando as duas tem a mesma cor media. Se a
# estrutura pesasse alto, qualquer bloco liso casaria com qualquer bloco liso, o
# que e exatamente o retalho que a ferramenta existe para evitar.
PESO_COR = 0.75
PESO_ESTRUTURA = 0.25

# Limiar calibrado em 06/09/2026 OLHANDO a folha de contato da prova do vizinho
# (gTileset_GeneralSinnoh para gTileset_General, sobre os 101 metatiles de
# primario que SnowpointCity e CanalaveCity usam). O que a folha mostrou:
#   d <= 0,08  casamento certo (agua com borda de areia vira agua com borda de
#              areia, na mesma orientacao; grama vira grama)
#   0,08 a 0,11  mesma familia, peca diferente (janela vira janela de outra cor)
#   d >= 0,11  errado de verdade (borda de arvore virou grama com cerca; canto
#              de predio branco virou copa de arvore; agua com margem virou agua
#              lisa). Casamento ruim e pior que casamento nenhum, porque produz
#              cidade em retalho: acima do limiar o metatile vira PENDENCIA.
# 0,09 e o corte que aceita a faixa boa, tolera a faixa "mesma familia" e recusa
# os dois piores casos, que juntos ocupavam 379 celulas das duas cidades.
LIMIAR_PADRAO = 0.09


# ---------------------------------------------------------------- utilitarios


def _nomes_de_behavior():
    """{valor: 'MB_NOME'} lido do enum de include/constants/metatile_behaviors.h."""
    caminho = os.path.join(REPO, "include/constants/metatile_behaviors.h")
    nomes = {}
    if not os.path.exists(caminho):
        return nomes
    with open(caminho, encoding="utf-8") as f:
        texto = f.read()
    m = re.search(r"enum\s*\{(.*?)\n\};", texto, re.DOTALL)
    if not m:
        return nomes
    proximo = 0
    for bruto in m.group(1).split(","):
        linha = re.sub(r"//.*", "", bruto).strip()
        if not linha:
            continue
        mm = re.match(r"^(MB_[A-Z0-9_]+)\s*(?:=\s*(0x[0-9A-Fa-f]+|\d+))?$", linha)
        if not mm:
            continue
        if mm.group(2):
            proximo = int(mm.group(2), 0)
        nomes.setdefault(proximo, mm.group(1))
        proximo += 1
    return nomes


NOMES_BEHAVIOR = _nomes_de_behavior()


def nome_behavior(valor):
    return NOMES_BEHAVIOR.get(valor, f"0x{valor:02X}")


def carregar_layouts():
    return rm.carregar_layouts()


def layout_do_mapa(nome, layouts):
    """Aceita nome de mapa (data/maps/<nome>) ou id de layout (LAYOUT_*)."""
    if nome.startswith("LAYOUT_"):
        layout = layouts.get(nome)
        if layout is None:
            raise ValueError(f"layout {nome} nao existe em layouts.json")
        return layout
    caminho = os.path.join(REPO, "data/maps", nome, "map.json")
    if not os.path.exists(caminho):
        raise ValueError(f"mapa {nome} nao existe em data/maps/")
    with open(caminho, encoding="utf-8") as f:
        mapa = json.load(f)
    layout = layouts.get(mapa["layout"])
    if layout is None:
        raise ValueError(f"layout {mapa['layout']} do mapa {nome} nao existe")
    return layout


_SOLTOS = 0


def rotulo_de_spec(spec):
    """Rotulo `gTileset_X` para um spec que pode ser rotulo ou pasta solta.

    Pasta solta entra pelo mesmo caminho do tileset instalado: registra-se a
    pasta no mapa de pastas do render_maps e usa-se um rotulo sintetico. Assim
    o carregador continua sendo UM so.
    """
    global _SOLTOS
    if spec.startswith("gTileset_"):
        return spec
    pasta = os.path.abspath(os.path.expanduser(spec))
    if not os.path.isdir(pasta):
        raise ValueError(f"tileset solto: {pasta} nao e pasta")
    for obrigatorio in ("tiles.png", "palettes", "metatiles.bin"):
        if not os.path.exists(os.path.join(pasta, obrigatorio)):
            raise ValueError(f"tileset solto {pasta}: falta {obrigatorio}")
    _SOLTOS += 1
    chave = f"Solto{_SOLTOS}_{os.path.basename(pasta)}"
    rm._MAPA_TILESETS[chave] = pasta
    return "gTileset_" + chave


_CACHE_TS = {}


def carregar(rotulo):
    """Tileset completo: o que o render_maps carrega, mais os atributos."""
    if rotulo in _CACHE_TS:
        return _CACHE_TS[rotulo]
    ts = rm.carregar_tileset(rotulo)  # tiles, paletas, metatiles
    pasta = rm.caminho_tileset(rotulo)
    ts["rotulo"] = rotulo
    ts["pasta"] = pasta
    ts["n_metatiles"] = len(ts["metatiles"]) // 16

    caminho_attr = os.path.join(pasta, "metatile_attributes.bin")
    if not os.path.exists(caminho_attr):
        caminho_attr = os.path.join(os.path.dirname(pasta), "metatile_attributes.bin")
    bruto = open(caminho_attr, "rb").read()
    # Emerald: 2 bytes por metatile. O autoteste confere a coerencia de tamanho.
    n_attr = len(bruto) // 2
    attrs = []
    for i in range(n_attr):
        valor = struct.unpack_from("<H", bruto, i * 2)[0]
        attrs.append(
            (
                valor & METATILE_ATTR_BEHAVIOR_MASK,
                (valor & METATILE_ATTR_LAYER_MASK) >> METATILE_ATTR_LAYER_SHIFT,
            )
        )
    ts["atributos"] = attrs
    _CACHE_TS[rotulo] = ts
    return ts


def split_do_layout(versao):
    """(n_metatiles_no_primario, n_paletas_do_primario) por layout_version."""
    if versao in ("johto", "frlg"):
        return 640, 7
    return 512, 6


class Par:
    """Par primario+secundario com o split do layout, e o que ele sabe dizer."""

    def __init__(self, spec_pri, spec_sec, versao):
        self.rotulo_pri = rotulo_de_spec(spec_pri)
        self.rotulo_sec = rotulo_de_spec(spec_sec)
        self.versao = versao or "emerald"
        self.pri = carregar(self.rotulo_pri)
        self.sec = carregar(self.rotulo_sec)
        self.n_meta_pri, self.n_pal_pri = split_do_layout(self.versao)

    @property
    def chave(self):
        return (self.rotulo_pri, self.rotulo_sec, self.versao)

    def local(self, idx):
        """(tileset, indice_local) de um indice global de metatile, ou None."""
        if idx < self.n_meta_pri:
            if idx >= self.pri["n_metatiles"]:
                return None
            return self.pri, idx
        loc = idx - self.n_meta_pri
        if loc >= self.sec["n_metatiles"]:
            return None
        return self.sec, loc

    def valido(self, idx):
        return self.local(idx) is not None

    def atributo(self, idx):
        """(behavior, layerType) do metatile, ou None se o indice nao existe."""
        alvo = self.local(idx)
        if alvo is None:
            return None
        ts, loc = alvo
        if loc >= len(ts["atributos"]):
            return None
        return ts["atributos"][loc]

    def indices(self):
        for i in range(self.pri["n_metatiles"]):
            yield i
        for i in range(self.sec["n_metatiles"]):
            yield self.n_meta_pri + i

    def desenhar(self, idx):
        """Imagem 16x16 RGB do metatile, com o mesmo desenhador do render_maps."""
        alvo = self.local(idx)
        if alvo is None:
            return None
        ts_meta, loc = alvo
        fundo = self.pri["paletas"][0][0]
        img = Image.new("RGB", (META_PX, META_PX), fundo)
        px = img.load()
        entradas = rm.entradas_metatile(ts_meta["metatiles"], loc)
        for camada in (0, 1):
            for q in range(4):
                idx_tile, flip_h, flip_v, idx_pal = entradas[camada * 4 + q]
                tile = rm.resolver_tile(self.pri, self.sec, idx_tile)
                if tile is None:
                    continue
                fonte_pal = self.pri if idx_pal < self.n_pal_pri else self.sec
                cores = fonte_pal["paletas"].get(idx_pal)
                if cores is None:
                    continue
                qx, qy = (q % 2) * rm.TILE_PX, (q // 2) * rm.TILE_PX
                rm.desenhar_tile(px, qx, qy, tile, cores, flip_h, flip_v)
        return img


# ------------------------------------------------------------------- metrica


def vetor_cor(img):
    """Cor media dos 4 quadrantes 8x8, normalizada: 12 numeros em 0..1."""
    px = img.load()
    saida = []
    for qy in (0, 8):
        for qx in (0, 8):
            somas = [0, 0, 0]
            for y in range(qy, qy + 8):
                for x in range(qx, qx + 8):
                    cor = px[x, y]
                    somas[0] += cor[0]
                    somas[1] += cor[1]
                    somas[2] += cor[2]
            saida.extend(s / (64.0 * 255.0) for s in somas)
    return saida


def vetor_estrutura(img):
    """Magnitude de gradiente reduzida a blocos 4x4: 16 numeros em 0..1."""
    px = img.load()
    cinza = [
        [0.299 * px[x, y][0] + 0.587 * px[x, y][1] + 0.114 * px[x, y][2] for x in range(16)]
        for y in range(16)
    ]
    mag = [[0.0] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            dx = cinza[y][x + 1] - cinza[y][x] if x + 1 < 16 else 0.0
            dy = cinza[y + 1][x] - cinza[y][x] if y + 1 < 16 else 0.0
            mag[y][x] = math.hypot(dx, dy)
    saida = []
    for by in range(4):
        for bx in range(4):
            soma = 0.0
            for y in range(by * 4, by * 4 + 4):
                for x in range(bx * 4, bx * 4 + 4):
                    soma += mag[y][x]
            # 255*sqrt(2) e a magnitude maxima possivel de um pixel.
            saida.append(min(1.0, soma / (16.0 * 255.0 * math.sqrt(2))))
    return saida


def caracteristicas(img):
    return (vetor_cor(img), vetor_estrutura(img))


def distancia(a, b):
    cor_a, est_a = a
    cor_b, est_b = b
    dc = sum((x - y) ** 2 for x, y in zip(cor_a, cor_b)) / len(cor_a)
    de = sum((x - y) ** 2 for x, y in zip(est_a, est_b)) / len(est_a)
    return math.sqrt(PESO_COR * dc + PESO_ESTRUTURA * de)


# ------------------------------------------------------------------- planejar


def celulas_usadas(layout):
    """{indice_de_metatile: quantas celulas} lido do map.bin do layout."""
    caminho = os.path.join(REPO, layout["blockdata_filepath"])
    dados = open(caminho, "rb").read()
    contagem = {}
    for i in range(len(dados) // 2):
        valor = struct.unpack_from("<H", dados, i * 2)[0]
        idx = valor & MAPGRID_METATILE_ID_MASK
        contagem[idx] = contagem.get(idx, 0) + 1
    return contagem


def planejar_grupo(par_o, par_d, contagem, limiar, desempate_indice=True):
    """De-para de um grupo: so os metatiles que aparecem no map.bin.

    O filtro de `(behavior, layerType)` e DURO: candidato com par diferente nao
    entra na disputa, nem que seja visualmente identico.
    """
    # candidatos do destino, agrupados por (behavior, layer)
    por_attr = {}
    caract_d = {}
    for idx in par_d.indices():
        attr = par_d.atributo(idx)
        if attr is None:
            continue
        img = par_d.desenhar(idx)
        if img is None:
            continue
        caract_d[idx] = caracteristicas(img)
        por_attr.setdefault(attr, []).append(idx)

    de_para = {}
    pendencias = []
    for idx_antigo in sorted(contagem):
        if not par_o.valido(idx_antigo):
            # indice fora do range do par de origem: o mapa ja estava torto,
            # nao e a conversao que quebra. Vira pendencia para ninguem
            # converter em cima de lixo.
            pendencias.append(
                {
                    "indice_antigo": idx_antigo,
                    "behavior": None,
                    "behavior_nome": None,
                    "layer": None,
                    "celulas": contagem[idx_antigo],
                    "motivo": "indice invalido no par de origem",
                }
            )
            continue
        attr = par_o.atributo(idx_antigo)
        img_o = par_o.desenhar(idx_antigo)
        c_o = caracteristicas(img_o)
        candidatos = por_attr.get(attr, [])
        if not candidatos:
            pendencias.append(
                {
                    "indice_antigo": idx_antigo,
                    "behavior": attr[0],
                    "behavior_nome": nome_behavior(attr[0]),
                    "layer": attr[1],
                    "celulas": contagem[idx_antigo],
                    "motivo": "sem candidato de mesmo (behavior, layerType)",
                }
            )
            continue
        melhor, melhor_d = None, None
        for idx_novo in candidatos:
            d = distancia(c_o, caract_d[idx_novo])
            if melhor_d is None or d < melhor_d - 1e-12:
                melhor, melhor_d = idx_novo, d
            elif desempate_indice and abs(d - melhor_d) <= 1e-12 and idx_novo == idx_antigo:
                # empate exato: fica com o indice que ja esta no map.bin, porque
                # ele deixa a conversao com o menor diff possivel.
                melhor, melhor_d = idx_novo, d
        if melhor_d > limiar:
            pendencias.append(
                {
                    "indice_antigo": idx_antigo,
                    "behavior": attr[0],
                    "behavior_nome": nome_behavior(attr[0]),
                    "layer": attr[1],
                    "celulas": contagem[idx_antigo],
                    "motivo": f"melhor candidato acima do limiar (d={melhor_d:.4f} > {limiar})",
                    "melhor_recusado": melhor,
                    "distancia_recusada": round(melhor_d, 6),
                }
            )
            continue
        de_para[idx_antigo] = {
            "novo": melhor,
            "distancia": round(melhor_d, 6),
            "behavior": attr[0],
            "behavior_nome": nome_behavior(attr[0]),
            "layer": attr[1],
            "celulas": contagem[idx_antigo],
        }
    return de_para, pendencias


def montar_grupos(mapas, layouts, args):
    """Agrupa os mapas por (par de origem, par de destino)."""
    grupos = {}
    for nome in mapas:
        layout = layout_do_mapa(nome, layouts)
        pri_o = args.pri_origem or layout["primary_tileset"]
        sec_o = args.sec_origem or layout["secondary_tileset"]
        if layout["primary_tileset"] != pri_o or layout["secondary_tileset"] != sec_o:
            raise ValueError(
                f"{nome}: o layout usa ({layout['primary_tileset']}, "
                f"{layout['secondary_tileset']}), nao o par de origem pedido "
                f"({pri_o}, {sec_o})"
            )
        ver_o = args.versao_origem or layout.get("layout_version") or "emerald"
        pri_d = args.pri_destino or pri_o
        sec_d = args.sec_destino or sec_o
        ver_d = args.versao_destino or ver_o
        chave = (pri_o, sec_o, ver_o, pri_d, sec_d, ver_d)
        grupos.setdefault(chave, []).append((nome, layout))
    return grupos


def planejar(mapas, layouts, args):
    grupos = montar_grupos(mapas, layouts, args)
    conversoes = []
    for chave, itens in grupos.items():
        pri_o, sec_o, ver_o, pri_d, sec_d, ver_d = chave
        par_o = Par(pri_o, sec_o, ver_o)
        par_d = Par(pri_d, sec_d, ver_d)
        contagem = {}
        for _nome, layout in itens:
            for idx, n in celulas_usadas(layout).items():
                contagem[idx] = contagem.get(idx, 0) + n
        de_para, pendencias = planejar_grupo(
            par_o, par_d, contagem, args.limiar, desempate_indice=not args.sem_desempate_indice
        )
        conversoes.append(
            {
                "origem": {"primario": pri_o, "secundario": sec_o, "layout_version": ver_o},
                "destino": {"primario": pri_d, "secundario": sec_d, "layout_version": ver_d},
                "mapas": [n for n, _ in itens],
                "layouts": [l["id"] for _, l in itens],
                "metatiles_usados": len(contagem),
                "de_para": {str(k): v for k, v in sorted(de_para.items())},
                "pendencias": sorted(pendencias, key=lambda p: -p["celulas"]),
            }
        )
    plano = {
        "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "limiar": args.limiar,
        "pesos": {"cor": PESO_COR, "estrutura": PESO_ESTRUTURA},
        "conversoes": conversoes,
    }
    return plano


# --------------------------------------------------------- folha de contato


def folha_de_contato(plano, caminho_png, titulo=""):
    """PNG com os pares lado a lado, 4x, do pior casamento para o melhor."""
    escala = 4
    lado = META_PX * escala  # 64
    margem = 8
    largura = 3 * lado + 2 * margem + 420
    linhas = []
    for conv in plano["conversoes"]:
        par_o = Par(
            conv["origem"]["primario"], conv["origem"]["secundario"], conv["origem"]["layout_version"]
        )
        par_d = Par(
            conv["destino"]["primario"],
            conv["destino"]["secundario"],
            conv["destino"]["layout_version"],
        )
        for chave, item in conv["de_para"].items():
            linhas.append((item["distancia"], int(chave), item, par_o, par_d, False))
        for p in conv["pendencias"]:
            linhas.append((float("inf"), p["indice_antigo"], p, par_o, par_d, True))
    linhas.sort(key=lambda t: (-(t[0] if t[0] != float("inf") else 1e9), t[1]))

    altura_linha = lado + 10
    altura = margem + max(1, len(linhas)) * altura_linha + 40
    img = Image.new("RGB", (largura, altura), (24, 24, 28))
    draw = ImageDraw.Draw(img)
    draw.text((margem, margem), titulo or "de-para de metatiles", fill=(255, 255, 255))
    y = margem + 24
    for dist, idx_antigo, item, par_o, par_d, pendente in linhas:
        img_o = par_o.desenhar(idx_antigo)
        if img_o is not None:
            img.paste(img_o.resize((lado, lado), Image.NEAREST), (margem, y))
        if pendente:
            draw.rectangle(
                [margem + lado + 10, y, margem + 2 * lado + 10, y + lado], outline=(220, 40, 40), width=2
            )
            draw.line(
                [margem + lado + 10, y, margem + 2 * lado + 10, y + lado], fill=(220, 40, 40), width=2
            )
            draw.line(
                [margem + lado + 10, y + lado, margem + 2 * lado + 10, y], fill=(220, 40, 40), width=2
            )
            texto = (
                f"PENDENCIA  antigo {idx_antigo}  {item.get('behavior_nome')}  "
                f"lay={item.get('layer')}  celulas={item['celulas']}\n{item['motivo']}"
            )
            cor_txt = (255, 140, 140)
        else:
            img_n = par_d.desenhar(item["novo"])
            if img_n is not None:
                img.paste(img_n.resize((lado, lado), Image.NEAREST), (margem + lado + 10, y))
            texto = (
                f"antigo {idx_antigo}  ->  novo {item['novo']}   d={dist:.4f}\n"
                f"{item['behavior_nome']}  lay={item['layer']}  celulas={item['celulas']}"
            )
            cor_txt = (235, 235, 235)
        draw.text((margem + 2 * lado + 24, y + 16), texto, fill=cor_txt)
        y += altura_linha
    os.makedirs(os.path.dirname(caminho_png), exist_ok=True)
    img.save(caminho_png)
    return caminho_png


# ------------------------------------------------------------- as duas provas


def converter_bytes(dados, de_para_int):
    """Reescreve so os 10 bits baixos de cada palavra. Bits 10 a 15 intactos."""
    saida = bytearray(dados)
    for i in range(len(dados) // 2):
        valor = struct.unpack_from("<H", dados, i * 2)[0]
        idx = valor & MAPGRID_METATILE_ID_MASK
        novo = de_para_int.get(idx)
        if novo is None:
            continue
        struct.pack_into("<H", saida, i * 2, (valor & MAPGRID_RESTO_MASK) | (novo & MAPGRID_METATILE_ID_MASK))
    return bytes(saida)


def prova_bits_altos(antes, depois):
    """(iguais, total) dos bits 10 a 15 palavra a palavra."""
    if len(antes) != len(depois):
        return 0, max(len(antes), len(depois)) // 2
    total = len(antes) // 2
    iguais = 0
    for i in range(total):
        a = struct.unpack_from("<H", antes, i * 2)[0]
        b = struct.unpack_from("<H", depois, i * 2)[0]
        if (a & MAPGRID_RESTO_MASK) == (b & MAPGRID_RESTO_MASK):
            iguais += 1
    return iguais, total


def prova_comportamento(antes, par_o, depois, par_d):
    """(iguais, total, exemplos) de `(behavior, layerType)` celula a celula."""
    total = min(len(antes), len(depois)) // 2
    iguais = 0
    exemplos = []
    for i in range(total):
        a = struct.unpack_from("<H", antes, i * 2)[0] & MAPGRID_METATILE_ID_MASK
        b = struct.unpack_from("<H", depois, i * 2)[0] & MAPGRID_METATILE_ID_MASK
        attr_a = par_o.atributo(a)
        attr_b = par_d.atributo(b)
        if attr_a == attr_b:
            iguais += 1
        elif len(exemplos) < 8:
            exemplos.append(
                {
                    "celula": i,
                    "antigo": a,
                    "novo": b,
                    "attr_antigo": [attr_a[0], attr_a[1]] if attr_a else None,
                    "attr_novo": [attr_b[0], attr_b[1]] if attr_b else None,
                    "behavior_antigo": nome_behavior(attr_a[0]) if attr_a else None,
                    "behavior_novo": nome_behavior(attr_b[0]) if attr_b else None,
                }
            )
    return iguais, total, exemplos


def verificar_plano(plano, layouts, verboso=True):
    """Simula a conversao do plano em memoria e roda as duas provas.

    Nao escreve nada. Devolve True se as duas fecharem 100% em todos os mapas.
    """
    tudo_ok = True
    for conv in plano["conversoes"]:
        par_o = Par(
            conv["origem"]["primario"], conv["origem"]["secundario"], conv["origem"]["layout_version"]
        )
        par_d = Par(
            conv["destino"]["primario"],
            conv["destino"]["secundario"],
            conv["destino"]["layout_version"],
        )
        de_para_int = {int(k): v["novo"] for k, v in conv["de_para"].items()}
        for nome in conv["mapas"]:
            layout = layout_do_mapa(nome, layouts)
            caminho = os.path.join(REPO, layout["blockdata_filepath"])
            antes = open(caminho, "rb").read()
            depois = converter_bytes(antes, de_para_int)
            ib, tb = prova_bits_altos(antes, depois)
            ic, tc, exemplos = prova_comportamento(antes, par_o, depois, par_d)
            pb = 100.0 * ib / tb if tb else 0.0
            pc = 100.0 * ic / tc if tc else 0.0
            ok = (ib == tb) and (ic == tc)
            tudo_ok = tudo_ok and ok
            if verboso:
                print(
                    f"{'OK  ' if ok else 'FALHA'} {nome}: bits 10-15 iguais {pb:.2f}% "
                    f"({ib}/{tb}) | (behavior, layerType) iguais {pc:.2f}% ({ic}/{tc})"
                )
                if not ok:
                    for e in exemplos:
                        print(
                            f"      celula {e['celula']}: {e['antigo']} -> {e['novo']}  "
                            f"{e['behavior_antigo']} -> {e['behavior_novo']}  "
                            f"lay {e['attr_antigo']} -> {e['attr_novo']}"
                        )
    return tudo_ok


def verificar_no_disco(mapas, layouts, verboso=True):
    """Confere um mapa JA convertido contra o backup `.antes` gravado no aplicar."""
    tudo_ok = True
    for nome in mapas:
        layout = layout_do_mapa(nome, layouts)
        caminho = os.path.join(REPO, layout["blockdata_filepath"])
        backup = caminho + ".antes"
        meta = backup + ".json"
        if not (os.path.exists(backup) and os.path.exists(meta)):
            print(f"FALHA {nome}: sem backup {os.path.basename(backup)} (nunca foi convertido?)")
            tudo_ok = False
            continue
        with open(meta, encoding="utf-8") as f:
            info = json.load(f)
        par_o = Par(info["origem"]["primario"], info["origem"]["secundario"], info["origem"]["layout_version"])
        par_d = Par(
            info["destino"]["primario"], info["destino"]["secundario"], info["destino"]["layout_version"]
        )
        antes = open(backup, "rb").read()
        depois = open(caminho, "rb").read()
        ib, tb = prova_bits_altos(antes, depois)
        ic, tc, _exemplos = prova_comportamento(antes, par_o, depois, par_d)
        ok = (ib == tb) and (ic == tc)
        tudo_ok = tudo_ok and ok
        if verboso:
            pb = 100.0 * ib / tb if tb else 0.0
            pc = 100.0 * ic / tc if tc else 0.0
            print(
                f"{'OK  ' if ok else 'FALHA'} {nome}: bits 10-15 iguais {pb:.2f}% "
                f"({ib}/{tb}) | (behavior, layerType) iguais {pc:.2f}% ({ic}/{tc})"
            )
    return tudo_ok


# -------------------------------------------------------------------- aplicar


def aplicar(plano, layouts):
    """Reescreve map.bin e layouts.json. Recusa se houver pendencia ou prova ruim."""
    for conv in plano["conversoes"]:
        com_celula = [p for p in conv["pendencias"] if p["celulas"] > 0]
        if com_celula:
            print(
                f"RECUSADO: {len(com_celula)} pendencia(s) ocupam celula no mapa "
                f"({sum(p['celulas'] for p in com_celula)} celulas). Resolva antes de aplicar."
            )
            return False
    if not verificar_plano(plano, layouts, verboso=True):
        print("RECUSADO: a verificacao de (behavior, layerType) ou de bits altos nao fechou 100%.")
        return False

    caminho_layouts = os.path.join(REPO, "data/layouts/layouts.json")
    with open(caminho_layouts, encoding="utf-8") as f:
        dados = json.load(f)
    por_id = {l["id"]: l for l in dados["layouts"]}

    for conv in plano["conversoes"]:
        de_para_int = {int(k): v["novo"] for k, v in conv["de_para"].items()}
        for nome, id_layout in zip(conv["mapas"], conv["layouts"]):
            layout = por_id[id_layout]
            caminho = os.path.join(REPO, layout["blockdata_filepath"])
            antes = open(caminho, "rb").read()
            backup = caminho + ".antes"
            if not os.path.exists(backup):
                with open(backup, "wb") as f:
                    f.write(antes)
                with open(backup + ".json", "w", encoding="utf-8") as f:
                    json.dump(
                        {"mapa": nome, "origem": conv["origem"], "destino": conv["destino"]},
                        f,
                        ensure_ascii=False,
                        indent=2,
                    )
            with open(caminho, "wb") as f:
                f.write(converter_bytes(antes, de_para_int))
            layout["primary_tileset"] = conv["destino"]["primario"]
            layout["secondary_tileset"] = conv["destino"]["secundario"]
            if conv["destino"]["layout_version"] != "emerald":
                layout["layout_version"] = conv["destino"]["layout_version"]
            print(f"aplicado: {nome} ({id_layout})")

    with open(caminho_layouts, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return True


# ------------------------------------------------------------------- autoteste


class _Args:
    def __init__(self, **kw):
        self.pri_origem = None
        self.sec_origem = None
        self.pri_destino = None
        self.sec_destino = None
        self.versao_origem = None
        self.versao_destino = None
        self.limiar = LIMIAR_PADRAO
        self.sem_desempate_indice = False
        self.__dict__.update(kw)


def _img_lisa(cor):
    return Image.new("RGB", (16, 16), cor)


def _img_listrada(a, b):
    img = Image.new("RGB", (16, 16), a)
    d = ImageDraw.Draw(img)
    for y in range(0, 16, 2):
        d.line([(0, y), (15, y)], fill=b)
    return img


def autoteste():
    falhas = []

    def checa(cond, msg):
        print(("OK   " if cond else "FALHA") + " " + msg)
        if not cond:
            falhas.append(msg)

    # 1. as mascaras batem com o header do jogo
    header = open(os.path.join(REPO, "include/global.fieldmap.h"), encoding="utf-8").read()
    checa(
        "#define METATILE_ATTR_BEHAVIOR_MASK 0x00FF" in header,
        "METATILE_ATTR_BEHAVIOR_MASK 0x00FF confere com global.fieldmap.h",
    )
    checa(
        "#define METATILE_ATTR_LAYER_MASK    0xF000" in header,
        "METATILE_ATTR_LAYER_MASK 0xF000 confere com global.fieldmap.h",
    )

    # 2. a reescrita mexe so nos 10 bits baixos
    original = struct.pack("<4H", 0x0001, 0xFC02, 0x8403, 0x03FF)
    convertido = converter_bytes(original, {1: 7, 2: 8, 3: 9, 0x3FF: 0})
    ib, tb = prova_bits_altos(original, convertido)
    checa(ib == tb == 4, f"bits 10 a 15 preservados em 100% das palavras ({ib}/{tb})")
    novos = [struct.unpack_from("<H", convertido, i * 2)[0] & 0x3FF for i in range(4)]
    checa(novos == [7, 8, 9, 0], f"indices trocados corretamente: {novos}")

    # 3. a metrica: identidade da zero, e cor separa mais que textura
    grama = caracteristicas(_img_lisa((60, 150, 60)))
    grama2 = caracteristicas(_img_listrada((60, 150, 60), (70, 160, 70)))
    calcada = caracteristicas(_img_lisa((190, 190, 180)))
    checa(distancia(grama, grama) == 0.0, "distancia de um metatile para ele mesmo e zero")
    checa(
        distancia(grama, grama2) < distancia(grama, calcada),
        f"grama x grama listrada ({distancia(grama, grama2):.4f}) < grama x calcada "
        f"({distancia(grama, calcada):.4f})",
    )
    checa(
        abs(distancia(grama, calcada) - distancia(calcada, grama)) < 1e-12,
        "a distancia e simetrica",
    )

    # 4. a prova de comportamento REPROVA quando o behavior muda
    class _ParFalso:
        def __init__(self, tabela):
            self.tabela = tabela

        def atributo(self, idx):
            return self.tabela.get(idx)

    antes = struct.pack("<2H", 0x0005, 0x0005)
    depois = struct.pack("<2H", 0x0009, 0x0005)
    par_a = _ParFalso({5: (2, 0)})  # MB_TALL_GRASS
    par_b = _ParFalso({5: (2, 0), 9: (0, 0)})  # MB_NORMAL no lugar da grama
    ic, tc, exemplos = prova_comportamento(antes, par_a, depois, par_b)
    checa(ic == 1 and tc == 2, f"a prova de comportamento pega a celula trocada ({ic}/{tc})")
    checa(
        bool(exemplos) and exemplos[0]["behavior_novo"] != exemplos[0]["behavior_antigo"],
        "o exemplo de falha nomeia o behavior antigo e o novo",
    )

    # 5. o filtro de (behavior, layerType) e duro mesmo com sosia visual
    layouts = carregar_layouts()
    par = Par("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh", "emerald")
    attrs = {}
    for idx in par.indices():
        a = par.atributo(idx)
        if a:
            attrs.setdefault(a, []).append(idx)
    checa(len(attrs) > 1, f"o par de teste tem {len(attrs)} pares (behavior, layerType) distintos")
    de_para, pend = planejar_grupo(par, par, {i: 1 for i in list(attrs.values())[0][:5]}, LIMIAR_PADRAO)
    checa(
        all(par.atributo(int(k)) == par.atributo(v["novo"]) for k, v in de_para.items()),
        "todo par escolhido preserva (behavior, layerType)",
    )
    checa(not pend, "sem pendencia num de-para do tileset para ele mesmo")

    print()
    if falhas:
        print(f"{len(falhas)} autoteste(s) FALHARAM.")
        return 1
    print("autoteste: tudo verde.")
    return 0


# ------------------------------------------------------------------------ demo


def demo():
    """Demonstracao curta: identidade fecha, e um de-para errado reprova."""
    layouts = carregar_layouts()
    mapas = ["SnowpointTemple1F"]

    print("== prova da identidade: GeneralSinnoh+CaveSinnoh para eles mesmos ==")
    args = _Args()
    plano = planejar(mapas, layouts, args)
    conv = plano["conversoes"][0]
    total = len(conv["de_para"])
    identicos = sum(1 for k, v in conv["de_para"].items() if int(k) == v["novo"])
    zeros = sum(1 for v in conv["de_para"].values() if v["distancia"] == 0.0)
    print(
        f"{total} metatiles usados | mapeiam para si: {identicos} | distancia zero: {zeros} "
        f"| pendencias: {len(conv['pendencias'])}"
    )
    ok_ident = verificar_plano(plano, layouts)

    print()
    print("== prova negativa: de-para fabricado trocando grama por outra coisa ==")
    par = Par("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh", "emerald")
    sabotado = json.loads(json.dumps(plano))
    trocas = 0
    for chave, item in sabotado["conversoes"][0]["de_para"].items():
        attr = par.atributo(int(chave))
        if trocas >= 3:
            break
        for cand in par.indices():
            outro = par.atributo(cand)
            if outro and outro != attr:
                item["novo"] = cand
                trocas += 1
                break
    print(f"{trocas} pares sabotados (behavior trocado de proposito)")
    ok_sab = verificar_plano(sabotado, layouts)

    print()
    print(f"identidade fechou 100%: {ok_ident}")
    print(f"sabotado passou na verificacao: {ok_sab}  (tem que ser False)")
    return 0 if (ok_ident and not ok_sab) else 1


# ------------------------------------------------------------------------ main


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--mapas", nargs="*", default=[], help="nomes de mapa ou ids LAYOUT_*")
    p.add_argument("--pri-origem", help="tileset primario de origem (rotulo ou pasta)")
    p.add_argument("--sec-origem", help="tileset secundario de origem (rotulo ou pasta)")
    p.add_argument("--pri-destino", help="tileset primario de destino (rotulo ou pasta)")
    p.add_argument("--sec-destino", help="tileset secundario de destino (rotulo ou pasta)")
    p.add_argument("--versao-origem", help="layout_version da origem (emerald, frlg, johto)")
    p.add_argument("--versao-destino", help="layout_version do destino")
    p.add_argument("--limiar", type=float, default=LIMIAR_PADRAO)
    p.add_argument("--sem-desempate-indice", action="store_true",
                   help="no empate exato, NAO prefere o mesmo indice (auditoria da identidade)")
    p.add_argument("--saida", default=SAIDA_PADRAO)
    p.add_argument("--nome", default="de-para", help="prefixo dos arquivos de saida")
    p.add_argument("--sem-folha", action="store_true", help="nao gerar a folha de contato")
    p.add_argument("--aplica", action="store_true")
    p.add_argument("--verifica", action="store_true")
    p.add_argument("--plano", help="JSON de plano para --verifica")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--autoteste", action="store_true")
    args = p.parse_args()

    if args.autoteste:
        return autoteste()
    if args.demo:
        return demo()

    layouts = carregar_layouts()

    if args.verifica:
        if args.plano:
            with open(args.plano, encoding="utf-8") as f:
                plano = json.load(f)
            return 0 if verificar_plano(plano, layouts) else 1
        if not args.mapas:
            p.error("--verifica precisa de --plano ou de --mapas")
        return 0 if verificar_no_disco(args.mapas, layouts) else 1

    if not args.mapas:
        p.error("informe --mapas")

    plano = planejar(args.mapas, layouts, args)
    os.makedirs(args.saida, exist_ok=True)
    caminho_json = os.path.join(args.saida, f"{args.nome}.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(plano, f, ensure_ascii=False, indent=2)
    print(f"plano: {caminho_json}")

    for conv in plano["conversoes"]:
        casados = len(conv["de_para"])
        usados = conv["metatiles_usados"]
        cel_pend = sum(pp["celulas"] for pp in conv["pendencias"])
        print(
            f"  {conv['origem']['primario']}+{conv['origem']['secundario']} -> "
            f"{conv['destino']['primario']}+{conv['destino']['secundario']}: "
            f"{casados}/{usados} metatiles casados ({100.0 * casados / usados:.1f}%), "
            f"{len(conv['pendencias'])} pendencias em {cel_pend} celulas"
        )

    if not args.sem_folha:
        caminho_png = os.path.join(args.saida, f"{args.nome}.png")
        folha_de_contato(plano, caminho_png, titulo=args.nome)
        print(f"folha de contato: {caminho_png}")

    ok = verificar_plano(plano, layouts)
    if args.aplica:
        return 0 if aplicar(plano, layouts) else 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
