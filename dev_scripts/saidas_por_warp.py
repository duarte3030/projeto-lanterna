#!/usr/bin/env python3
"""Troca as CONEXÕES de uma cidade copiada por pares de warp de seta.

Uso:
    python3 dev_scripts/saidas_por_warp.py --cidade TwinleafTown
    python3 dev_scripts/saidas_por_warp.py --cidade TwinleafTown --aplicar

POR QUE ISSO EXISTE (a regra de motor medida em 11/09/2026)
-----------------------------------------------------------
`LoadMapFromCameraTransition` (`src/overworld.c:911`) recarrega, na travessia
por CONEXÃO, só o tileset SECUNDÁRIO. O jogo original pode fazer isso porque
garante primário comum entre mapas ligados. Cidade copiada com PAR PRÓPRIO
quebra essa garantia: ao atravessar a pé, a rota vizinha inteira passa a ser
desenhada com o primário da CIDADE, e sai lixo (medido na frente A: Route 37
com árvore laranja e estrada preta). Pinar índice de costura não resolve, porque
o problema não é o número do metatile, é o tileset que o motor deixou de trocar.

A saída, decidida no contrato (`METODO-COPIA-CIDADES.md`, seção 3.1): a cidade
copiada NÃO tem conexão. Cada saída vira um par de warps de seta, com fade:

  * na borda da CIDADE, a célula andável ganha `MB_<DIR>_ARROW_WARP` e um
    `warp_event` que cai na rota;
  * na borda da ROTA, a célula espelhada ganha `MB_<DIR OPOSTA>_ARROW_WARP` e o
    `warp_event` de volta;
  * as duas conexões (a da cidade e a da rota) saem dos `map.json`.

`TryArrowWarp` (`src/field_control_avatar.c:958`) exige as DUAS coisas na mesma
célula: o comportamento de seta E um `warp_event`. O jogador PISA na célula e
SEGURA a direção; `DoWarp` faz o fade. O tile de trás da borda é
intransponível de graça (`GetBorderBlockAt` devolve `MAPGRID_IMPASSABLE`), então
quem não segura a direção só esbarra.

O QUE ESTA FERRAMENTA NÃO INVENTA
---------------------------------
Ela não escolhe onde fica a saída: ela usa a COLISÃO dos dois mapas. A saída é
o conjunto de células da borda da cidade que são andáveis E cuja célula
espelhada na rota (pelo `offset` da conexão de hoje, ou pelo que o dossiê
recalculou) também é andável. Se a interseção sair vazia, ela PARA e diz qual
lado está tapado: é decisão de desenho, e desenho não se gera por script
(seção 0.ae do ESTADO).

O METATILE DE SETA
------------------
Comportamento é atributo de METATILE, não de célula, então a célula da saída não
pode reaproveitar o metatile do chão: mudar o atributo dele mudaria toda célula
que o usa, no mapa inteiro e nos mapas irmãos. A ferramenta MINTA um GÊMEO: uma
vaga de metatile livre que recebe as 8 palavras e o atributo do chão original,
com o `behavior` trocado pela seta. O gêmeo desenha o MESMO pixel do chão (é a
mesma cópia de palavras), então a saída continua sendo a rua que o autor
desenhou.

  * do lado da CIDADE o gêmeo vai para o primário NOVO dela (que sobra vaga);
  * do lado da ROTA ele vai para o SECUNDÁRIO da rota, numa vaga que NENHUM
    layout da árvore referencia hoje. Medido em 11/09/2026: petalburg_sinnoh
    tem 385 vagas assim, mauville_sinnoh 386, rustboro_sinnoh 201 e jubilife
    153. Escrever numa vaga não referenciada não muda um pixel de nenhum outro
    mapa e não cresce arquivo nenhum.

Palavra de metatile do secundário pode apontar para tile do primário (o índice
de tile é global, 0..1023), então copiar as palavras de um metatile do primário
para uma vaga do secundário desenha igual.

SAVE
----
`warp_event` NOVO entra sempre no FIM da lista: os ids de todos os warps de hoje
ficam onde estão, e é por número que os outros mapas apontam para eles
(contrato, seção 1, item 3). Nenhuma flag e nenhuma var nova.
"""
import argparse
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MASCARA_ID = 0x03FF
MASCARA_COLISAO = 0x0C00
DESLOC_COLISAO = 10

# Direção da saída vista da CIDADE -> (seta na cidade, seta na rota).
# A seta é a direção em que o jogador SEGURA o d-pad para atravessar.
OPOSTA = {"up": "down", "down": "up", "left": "right", "right": "left"}
SETA = {"up": "MB_NORTH_ARROW_WARP", "down": "MB_SOUTH_ARROW_WARP",
        "left": "MB_WEST_ARROW_WARP", "right": "MB_EAST_ARROW_WARP"}


# ------------------------------------------------------------------ leitura ---

def pasta_do_simbolo(simbolo, secundario):
    nome = re.sub(r"(?<!^)(?=[A-Z])", "_", simbolo.replace("gTileset_", "")).lower()
    sub = "secondary" if secundario else "primary"
    return os.path.join(RAIZ, "data/tilesets", sub, nome)


def le_u16(caminho):
    with open(caminho, "rb") as f:
        b = f.read()
    return list(struct.unpack(f"<{len(b) // 2}H", b))


def grava_u16(caminho, palavras):
    with open(caminho, "wb") as f:
        f.write(struct.pack(f"<{len(palavras)}H", *palavras))


def le_layouts():
    with open(os.path.join(RAIZ, "data/layouts/layouts.json"), encoding="utf-8") as f:
        return json.load(f)


def indice_de_mapas():
    """MAP_X -> (nome de pasta, dados do map.json)."""
    fora = {}
    base = os.path.join(RAIZ, "data/maps")
    for nome in sorted(os.listdir(base)):
        caminho = os.path.join(base, nome, "map.json")
        if not os.path.exists(caminho):
            continue
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
        fora[dados["id"]] = (nome, dados)
    return fora


def tabela_mb():
    """MB_* -> número, lido do enum, nunca cravado.

    Número de comportamento anda quando alguém insere um `MB_` no meio do enum,
    e comportamento cravado envelhece calado. Mesma disciplina do
    `valida_warp_tile.py`.
    """
    caminho = os.path.join(RAIZ, "include/constants/metatile_behaviors.h")
    with open(caminho, encoding="utf-8") as f:
        texto = f.read()
    corpo = texto[texto.index("enum"):]
    corpo = corpo[corpo.index("{") + 1: corpo.index("}")]
    fora, proximo = {}, 0
    for linha in corpo.split(","):
        linha = re.sub(r"//.*", "", linha).strip()
        if not linha:
            continue
        if "=" in linha:
            nome, valor = [p.strip() for p in linha.split("=", 1)]
            proximo = int(valor, 0)
        else:
            nome = linha
        fora[nome] = proximo
        proximo += 1
    return fora


# ------------------------------------------------------------ o mapa e a rota -

class Mapa:
    def __init__(self, nome_pasta, mj, layouts):
        self.pasta = nome_pasta
        self.mj = mj
        self.lay = layouts[mj["layout"]]
        self.W, self.H = self.lay["width"], self.lay["height"]
        self.caminho_bin = os.path.join(RAIZ, self.lay["blockdata_filepath"].lstrip("./"))
        self.blocos = le_u16(self.caminho_bin)
        self.prim = self.lay["primary_tileset"]
        self.sec = self.lay["secondary_tileset"]
        # Atributos na numeração GLOBAL do mapa: 0..511 do primário (completado
        # com zero quando o arquivo é menor) e 512.. do secundário.
        a = le_u16(os.path.join(pasta_do_simbolo(self.prim, False),
                                "metatile_attributes.bin"))
        a = a[:512] + [0] * max(0, 512 - len(a))
        a += le_u16(os.path.join(pasta_do_simbolo(self.sec, True),
                                 "metatile_attributes.bin"))
        self.atributos = a + [0] * max(0, 1024 - len(a))

    def bloco(self, x, y):
        return self.blocos[y * self.W + x]

    def andavel(self, x, y):
        return ((self.bloco(x, y) & MASCARA_COLISAO) >> DESLOC_COLISAO) == 0

    def mid(self, x, y):
        return self.bloco(x, y) & MASCARA_ID

    def comportamento(self, x, y):
        return self.atributos[self.mid(x, y)] & 0x00FF


class Cofre:
    """UM registro de tileset por SÍMBOLO, carregado e gravado uma vez só.

    Nasceu de um defeito medido no emulador em 11/09/2026, e o defeito é a razão
    de a classe existir nesta forma. A primeira versão tinha um objeto de
    tileset por MAPA. Sandgem, a Route 201, a Route 219 e a Route 202 usam todas
    o mesmo par (`general_sinnoh` + `petalburg_sinnoh`), então quatro objetos
    diferentes leram o MESMO arquivo, cada um mintou o gêmeo dele na MESMA
    primeira vaga livre (512) e cada um gravou o arquivo inteiro por cima do
    anterior. Sobrou um gêmeo só, com o comportamento da última rota gravada, e
    o `map.bin` das outras três apontando para ele. Na prova do motor
    (`T999`), a borda sul de Sandgem devolveu `MB_NORMAL` e a borda norte da
    Route 219 devolveu `MB_SOUTH_ARROW_WARP` quando devia ser `NORTH`: o
    jogador segurava para baixo e não saía do lugar.

    Aqui cada símbolo é lido uma vez, a lista de vagas é UMA por símbolo, e a
    gravação acontece uma vez, no fim.

    O executor de Twinleaf achou o MESMO defeito por outro caminho, no mesmo
    dia, e a medida dele fecha com esta: a Route 201 e a Route 220 dividem o
    par, a Route 220 entra na lista só para perder a conexão, e era ela que
    gravava o `petalburg_sinnoh` original por cima. As três células da borda da
    Route 201 ficavam apontando para metatiles vazios com `MB_NORMAL`, com
    saída morta e três buracos no desenho da rota, enquanto a ferramenta
    imprimia "3 gêmeos mintados". O conserto dele era a chave do cache pelo PAR
    em vez da pasta do mapa; este é mais largo, porque também impede que a vaga
    escolhida seja uma que OUTRO mapa já desenha.
    """

    def __init__(self, layouts):
        self.layouts = layouts
        self.dados = {}          # simbolo -> {"metatiles", "attrs", "pasta", "sec"}
        self.vagas = {}          # simbolo -> lista de índices GLOBais livres
        self.tocados = set()

    def carrega(self, simbolo, secundario):
        if simbolo not in self.dados:
            pasta = pasta_do_simbolo(simbolo, secundario)
            self.dados[simbolo] = {
                "pasta": pasta, "sec": secundario,
                "metatiles": le_u16(os.path.join(pasta, "metatiles.bin")),
                "attrs": le_u16(os.path.join(pasta, "metatile_attributes.bin"))}
        return self.dados[simbolo]

    def simbolo_do_indice(self, mapa, indice):
        return (mapa.sec, True) if indice >= 512 else (mapa.prim, False)

    def palavras(self, mapa, indice):
        sim, sec = self.simbolo_do_indice(mapa, indice)
        d = self.carrega(sim, sec)
        i = indice - 512 if sec else indice
        return list(d["metatiles"][i * 8:(i + 1) * 8])

    def atributo(self, mapa, indice):
        sim, sec = self.simbolo_do_indice(mapa, indice)
        d = self.carrega(sim, sec)
        i = indice - 512 if sec else indice
        return d["attrs"][i]

    def livres(self, simbolo, secundario):
        """Índices que NENHUM layout da árvore desenha com este tileset.

        A conta é sobre a árvore inteira, e não sobre um mapa: `petalburg_sinnoh`
        serve 62 layouts e `general_sinnoh` serve Sinnoh inteira. Escrever numa
        vaga que outro mapa usa mudaria a arte DELE, calado. Medido em
        11/09/2026: petalburg_sinnoh tem 385 vagas assim, mauville_sinnoh 386,
        rustboro_sinnoh 201 e jubilife 153.
        """
        if simbolo in self.vagas:
            return self.vagas[simbolo]
        d = self.carrega(simbolo, secundario)
        n = len(d["metatiles"]) // 8
        chave = "secondary_tileset" if secundario else "primary_tileset"
        usados = set()
        for l in self.layouts.values():
            if l[chave] != simbolo:
                continue
            for campo in ("blockdata_filepath", "border_filepath"):
                c = os.path.join(RAIZ, l[campo].lstrip("./"))
                if not os.path.exists(c):
                    continue
                for w in le_u16(c):
                    usados.add(w & MASCARA_ID)
        base = 512 if secundario else 0
        # O índice 0 do primário fica de fora por princípio: `MAPGRID_UNDEFINED`
        # e "célula sem desenho" moram nele, e ninguém quer uma seta ali.
        self.vagas[simbolo] = [base + i for i in range(n)
                               if (base + i) not in usados and (base + i) != 0]
        return self.vagas[simbolo]

    def minta(self, mapa, base, comportamento, preferir_secundario=False):
        """O gêmeo de `base` com outro comportamento. Devolve (índice, é novo?).

        O gêmeo copia as 8 palavras e o atributo do original e troca só os 8
        bits de `behavior`: mesma imagem, mesmo `layerType`, mesmo terreno. Uma
        palavra de metatile do secundário pode apontar para tile do primário (o
        índice de tile é global, 0..1023), então o gêmeo desenha igual mesmo
        quando muda de lado.
        """
        if (self.atributo(mapa, base) & 0x00FF) == (comportamento & 0x00FF):
            # O metatile JÁ é a seta certa. Isso não é sorte: o Retro Platinum
            # resolve a saída das cidades dele exatamente assim, com
            # `MB_*_ARROW_WARP` na borda (nove células na Floaroma da fonte).
            # Copiada a arte, a seta do autor vem junto, e o que falta é só o
            # `warp_event` em cima dela.
            return base, False
        palavras = self.palavras(mapa, base)
        attr = (self.atributo(mapa, base) & ~0x00FF) | (comportamento & 0x00FF)
        ordem = ([(mapa.sec, True), (mapa.prim, False)] if preferir_secundario
                 else [(mapa.prim, False), (mapa.sec, True)])
        # 1) o gêmeo idêntico já existe? (duas saídas na mesma rua, mesmo chão)
        for sim, sec in ordem:
            d = self.carrega(sim, sec)
            for cand in self.livres(sim, sec):
                i = cand - 512 if sec else cand
                if (list(d["metatiles"][i * 8:(i + 1) * 8]) == palavras
                        and d["attrs"][i] == attr):
                    return cand, False
        # 2) senão, a primeira vaga livre
        for sim, sec in ordem:
            vagas = self.livres(sim, sec)
            if not vagas:
                continue
            alvo = vagas.pop(0)
            d = self.carrega(sim, sec)
            i = alvo - 512 if sec else alvo
            d["metatiles"][i * 8:(i + 1) * 8] = palavras
            d["attrs"][i] = attr
            self.tocados.add(sim)
            return alvo, True
        raise SystemExit(f"sem vaga de metatile para o gêmeo da seta em "
                         f"{mapa.prim} / {mapa.sec}")

    def escreve(self):
        for simbolo in sorted(self.tocados):
            d = self.dados[simbolo]
            grava_u16(os.path.join(d["pasta"], "metatiles.bin"), d["metatiles"])
            grava_u16(os.path.join(d["pasta"], "metatile_attributes.bin"), d["attrs"])
        return sorted(self.tocados)


# --------------------------------------------------------------- a travessia --

def faixa(direcao, mapa, lado_cidade):
    """A linha de borda de um mapa, e como andar sobre ela.

    Devolve (eixo, fixo, comprimento), onde `eixo` é "x" quando a linha é
    horizontal. `lado_cidade` diz se estamos na cidade (borda de saída) ou na
    rota (borda de chegada, que é a OPOSTA).
    """
    d = direcao if lado_cidade else OPOSTA[direcao]
    if d == "up":
        return "x", 0, mapa.W
    if d == "down":
        return "x", mapa.H - 1, mapa.W
    if d == "left":
        return "y", 0, mapa.H
    return "y", mapa.W - 1, mapa.H


def celula(eixo, variavel, fixo):
    return (variavel, fixo) if eixo == "x" else (fixo, variavel)


def ocupadas(mj):
    """Células que já têm jogo em cima: `object_event` ou `bg_event`.

    A seta troca o METATILE da célula, e trocar o metatile de uma cova de berry
    (`MB_BERRY_TREE_SOIL`) apaga a cova debaixo da árvore que o `object_event`
    ainda referencia. O caso é real: as 7 células andáveis da borda norte de
    Oreburgh de hoje são todas cova de berry, do canteiro que a quebra de save
    de 09/09 plantou.

    O `bg_event` entrou em 11/09/2026, na saída norte de Oreburgh: a placa
    `Sinnoh_EventScript_PlacaImportada` fica em (12,31) da Route 207, bem no meio
    das 6 colunas de travessia. Seta de warp e placa na mesma célula brigam: o
    jogador que anda para a placa é teleportado antes de poder ler. A célula sai
    da saída, e a placa fica onde está.
    """
    return ({(o["x"], o["y"]) for o in (mj.get("object_events") or [])} |
            {(b["x"], b["y"]) for b in (mj.get("bg_events") or [])})


def travessias(cidade, rota, direcao, offset, mb, proibidos):
    """As células da borda em que dá para atravessar, nos dois mapas.

    `offset` é o da conexão de hoje, com a semântica medida em
    `FillSouthConnection` (`src/fieldmap.c:264`): a coluna 0 da rota encosta na
    coluna `offset` da cidade, logo `coordenada_da_rota = coordenada_da_cidade -
    offset`.
    """
    eixo_c, fixo_c, n_c = faixa(direcao, cidade, True)
    eixo_r, fixo_r, n_r = faixa(direcao, rota, False)
    ocup_c, ocup_r = ocupadas(cidade.mj), ocupadas(rota.mj)
    pares, tapados = [], []
    for v in range(n_c):
        cx, cy = celula(eixo_c, v, fixo_c)
        if not cidade.andavel(cx, cy):
            continue
        if (cx, cy) in ocup_c:
            tapados.append(((cx, cy), "object_event ou bg_event em cima da célula"))
            continue
        if cidade.comportamento(cx, cy) in proibidos:
            tapados.append(((cx, cy), f"comportamento {mb[cidade.comportamento(cx, cy)]}"))
            continue
        vr = v - offset
        if not (0 <= vr < n_r):
            tapados.append(((cx, cy), "fora da rota"))
            continue
        rx, ry = celula(eixo_r, vr, fixo_r)
        if not rota.andavel(rx, ry):
            tapados.append(((cx, cy), f"rota bloqueada em ({rx},{ry})"))
            continue
        if (rx, ry) in ocup_r:
            tapados.append(((cx, cy), f"object_event na rota em ({rx},{ry})"))
            continue
        if rota.comportamento(rx, ry) in proibidos:
            tapados.append(((cx, cy),
                            f"rota com comportamento "
                            f"{mb[rota.comportamento(rx, ry)]} em ({rx},{ry})"))
            continue
        pares.append(((cx, cy), (rx, ry)))
    return pares, tapados


# ------------------------------------------------------------------ execução --

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cidade", required=True,
                   help="nome da pasta do NOSSO mapa, ex.: TwinleafTown")
    p.add_argument("--offsets", help="JSON {\"MAP_ROUTE201\": -4} com offsets "
                                     "recalculados pelo dossiê (sobrepõe os de hoje)")
    p.add_argument("--sem-travessia", default="",
                   help="lista de MAP_* em que é ESPERADO não haver travessia a "
                        "pé (conexão decorativa, como a rota de mar). Sem "
                        "declarar aqui, travessia zero é ERRO e a ferramenta "
                        "não aplica")
    p.add_argument("--apesar-de", default="",
                   help="lista de MB_* que DEIXAM de bloquear a saída, com o "
                        "motivo medido pelo executor. Nasceu da saída norte de "
                        "Oreburgh: o metatile 268 do general_sinnoh, que é o chão "
                        "da entrada da cidade na Route 207, carrega "
                        "MB_BERRY_TREE_SOIL, mas nenhuma das 6 células tem árvore "
                        "de berry em cima (as 4 da rota estão em (2..5,2)). "
                        "Bloquear ali era proteger uma cova que não existe.")
    p.add_argument("--so-seta-do-autor", action="store_true",
                   help="só vira saída a célula que JÁ tem a seta do autor do "
                        "hack (MB_<DIR>_ARROW_WARP) na arte copiada. Existe "
                        "para a cidade cuja planta foi RECORTADA: o corte "
                        "transforma chão de meio de mapa em borda, e sem isto "
                        "a ferramenta abriria saída em toda célula andável do "
                        "corte, que é saída que nem o autor nem o nosso jogo "
                        "de hoje têm (medido em Floaroma: 7 no sul, das quais "
                        "só 3 são seta do autor)")
    p.add_argument("--aplicar", action="store_true",
                   help="grava map.bin, metatiles e map.json dos dois lados")
    args = p.parse_args()

    layouts = {l["id"]: l for l in le_layouts()["layouts"]}
    mapas = indice_de_mapas()
    por_pasta = {n: (i, d) for i, (n, d) in mapas.items()}
    if args.cidade not in por_pasta:
        raise SystemExit(f"mapa {args.cidade} não achado em data/maps/")
    id_cidade, mj_cidade = por_pasta[args.cidade]
    cidade = Mapa(args.cidade, mj_cidade, layouts)
    mb = tabela_mb()
    por_numero = {v: k for k, v in mb.items()}
    # Comportamento que carrega JOGO na célula, não só chão: trocar o metatile
    # aqui apagaria a cova de berry, o esconderijo ou a entrada de base secreta
    # que um `object_event` ou um script ainda referencia.
    proibidos = {mb[n] for n in ("MB_BERRY_TREE_SOIL", "MB_SECRET_BASE_SPOT_RED_CAVE",
                                 "MB_SECRET_BASE_SPOT_BROWN_CAVE",
                                 "MB_SECRET_BASE_SPOT_YELLOW_CAVE",
                                 "MB_SECRET_BASE_SPOT_BLUE_CAVE",
                                 "MB_SECRET_BASE_ENTRANCE", "MB_IMPASSABLE_EAST")
                 if n in mb}
    liberados = {m.strip() for m in args.apesar_de.split(",") if m.strip()}
    for nome in sorted(liberados):
        if nome not in mb:
            raise SystemExit(f"--apesar-de: {nome} não existe no enum MB_*")
        proibidos.discard(mb[nome])
        print(f"  --apesar-de {nome}: deixa de bloquear a saída")

    offsets_forcados = {}
    if args.offsets:
        with open(args.offsets, encoding="utf-8") as f:
            offsets_forcados = json.load(f)

    esperado_sem_travessia = {m.strip() for m in args.sem_travessia.split(",")
                              if m.strip()}
    conexoes = [c for c in (mj_cidade.get("connections") or [])
                if c.get("direction") in OPOSTA]
    if not conexoes:
        print(f"{args.cidade}: nenhuma conexão de mapa. Nada a converter.")
        return 0

    print(f"=== {args.cidade} ({id_cidade}) {cidade.W}x{cidade.H} ===")
    print(f"  par: {cidade.prim} + {cidade.sec}")

    cofre = Cofre(layouts)
    print(f"  vagas livres: {len(cofre.livres(cidade.prim, False))} no primário "
          f"{cidade.prim}, {len(cofre.livres(cidade.sec, True))} no secundário "
          f"{cidade.sec} (a conta é sobre a ÁRVORE INTEIRA, não sobre este mapa)")

    planos, erros = [], []
    cache_rotas = {}
    for c in conexoes:
        direcao, alvo = c["direction"], c["map"]
        if alvo not in mapas:
            erros.append(f"{direcao}: mapa {alvo} não existe")
            continue
        offset = int(offsets_forcados.get(alvo, c.get("offset", 0)))
        nome_r, mj_r = mapas[alvo]
        rota = cache_rotas.setdefault(alvo, Mapa(nome_r, mj_r, layouts))
        if rota.prim != cidade.prim:
            pass  # é o esperado depois do par próprio; a conexão é que sai
        pares, tapados = travessias(cidade, rota, direcao, offset, por_numero,
                                    proibidos)
        if args.so_seta_do_autor:
            seta_daqui = mb[SETA[direcao]]
            sem_seta = [par for par in pares
                        if cidade.comportamento(*par[0]) != seta_daqui]
            pares = [par for par in pares
                     if cidade.comportamento(*par[0]) == seta_daqui]
            for (cx, cy), _ in sem_seta:
                tapados.append(((cx, cy), "sem a seta do autor "
                                          "(--so-seta-do-autor)"))
        print(f"  {direcao:5s} -> {alvo:24s} offset {offset:4d}: "
              f"{len(pares)} célula(s) de travessia, {len(tapados)} tapada(s)")
        if args.so_seta_do_autor:
            print(f"      --so-seta-do-autor: {len(sem_seta)} célula(s) "
                  f"andável(is) descartada(s) por não ter seta do autor "
                  f"{[c for c, _ in sem_seta]}")
        for (cx, cy), motivo in tapados[:4]:
            print(f"      tapada cidade({cx},{cy}): {motivo}")
        if pares and alvo in esperado_sem_travessia:
            # A flag é AUTORITATIVA, e não só um perdão para o caso de zero.
            # Medido em 11/09/2026 na borda sul de Twinleaf, DEPOIS de a arte do
            # hack entrar: a linha 33 passa a ter 20 células de colisão 0 (8 de
            # lago, 12 de gramado decorativo atrás da mata), e 16 delas casam
            # com o mar da Route220. Abrir warp ali seria inventar passagem que
            # o jogo de hoje não tem: a conexão sul é cosmética, a borda do
            # nosso mapa de hoje não tem uma única célula andável, e o dossiê
            # registra a travessia de Surf como passagem NOVA. Quem declara
            # `--sem-travessia` está dizendo que aquele lado NÃO ganha saída;
            # só a conexão sai, e o que o jogador vê além da borda passa a ser
            # o `border.bin` da cidade.
            print(f"      {len(pares)} candidata(s) DESCARTADA(S) por "
                  f"--sem-travessia: a conexão sai, a saída não é aberta")
            pares = []
        if not pares:
            if alvo in esperado_sem_travessia:
                # Conexão decorativa: hoje já não se atravessa a pé ali (a rota
                # de mar ao sul de Twinleaf, o mar a oeste de Jubilife). A
                # conexão sai do mesmo jeito, porque com primário próprio ela
                # desenharia lixo; o que o jogador passa a ver além da borda é
                # o `border.bin` da cidade, que também é o do hack.
                print(f"      sem travessia a pé, e isso era esperado "
                      f"(--sem-travessia): a conexão sai mesmo assim")
                planos.append({"direcao": direcao, "alvo": alvo, "rota": rota,
                               "offset": offset, "pares": []})
            else:
                erros.append(f"{direcao} -> {alvo}: NENHUMA célula andável "
                             f"coincide (offset {offset}). Decisão de desenho: "
                             f"mexer no offset, abrir a saída, ou declarar em "
                             f"--sem-travessia se a conexão for decorativa.")
            continue
        planos.append({"direcao": direcao, "alvo": alvo, "rota": rota,
                       "offset": offset, "pares": pares})

    if erros:
        print("  ERROS:")
        for e in erros:
            print(f"    {e}")
        if args.aplicar:
            print("  NÃO APLICO: conserte as saídas acima primeiro.")
            return 1

    # --- montagem -----------------------------------------------------------
    novos_warps_cidade = []
    plano_rotas = {}
    for plano in planos:
        rota = plano["rota"]
        seta_c = mb[SETA[plano["direcao"]]]
        seta_r = mb[SETA[OPOSTA[plano["direcao"]]]]
        entrada = plano_rotas.setdefault(rota.pasta, {"rota": rota,
                                                      "warps": [], "celulas": []})
        for (cx, cy), (rx, ry) in plano["pares"]:
            base_c = cidade.mid(cx, cy)
            gemeo_c, novo_c = cofre.minta(cidade, base_c, seta_c)
            base_r = rota.mid(rx, ry)
            # Do lado da ROTA o gêmeo prefere o SECUNDÁRIO: o primário
            # `general_sinnoh` serve Sinnoh inteira e tem 1 vaga livre só,
            # medida em 11/09/2026.
            gemeo_r, novo_r = cofre.minta(rota, base_r, seta_r,
                                          preferir_secundario=True)
            novos_warps_cidade.append({
                "celula": (cx, cy), "gemeo": gemeo_c, "base": base_c,
                "novo": novo_c, "alvo": plano["alvo"], "destino": (rx, ry)})
            entrada["warps"].append({
                "celula": (rx, ry), "gemeo": gemeo_r, "base": base_r,
                "novo": novo_r, "alvo": id_cidade})
            entrada["celulas"].append(((rx, ry), gemeo_r))

    # ids: o warp NOVO entra no fim das duas listas, e um aponta para o outro.
    base_id_cidade = len(mj_cidade.get("warp_events") or [])
    for i, w in enumerate(novos_warps_cidade):
        w["id_aqui"] = base_id_cidade + i
    contador = {}
    for nome, e in plano_rotas.items():
        base = len(e["rota"].mj.get("warp_events") or [])
        for i, w in enumerate(e["warps"]):
            w["id_aqui"] = base + i
        contador[nome] = base
    # casamento 1 para 1, na ordem em que foram criados
    pilha = {}
    for nome, e in plano_rotas.items():
        pilha[nome] = list(e["warps"])
    for w in novos_warps_cidade:
        nome = mapas[w["alvo"]][0]
        par = pilha[nome].pop(0)
        w["destino_id"] = par["id_aqui"]
        par["destino_id"] = w["id_aqui"]

    print(f"  warps novos: {len(novos_warps_cidade)} na cidade "
          f"(ids {base_id_cidade}..{base_id_cidade + len(novos_warps_cidade) - 1}), "
          + ", ".join(f"{len(e['warps'])} em {n} (a partir do id {contador[n]})"
                      for n, e in plano_rotas.items()))
    mintados = sum(1 for w in novos_warps_cidade if w["novo"])
    mintados_r = sum(1 for e in plano_rotas.values() for w in e["warps"] if w["novo"])
    print(f"  gêmeos de seta mintados: {mintados} no primário da cidade, "
          f"{mintados_r} nos secundários das rotas")

    if not args.aplicar:
        print("  (só medição; use --aplicar para gravar)")
        return 0

    # --- gravação -----------------------------------------------------------
    for w in novos_warps_cidade:
        cx, cy = w["celula"]
        i = cy * cidade.W + cx
        cidade.blocos[i] = (cidade.blocos[i] & ~MASCARA_ID) | w["gemeo"]
    grava_u16(cidade.caminho_bin, cidade.blocos)

    mj_cidade.setdefault("warp_events", [])
    for w in novos_warps_cidade:
        mj_cidade["warp_events"].append({
            "x": w["celula"][0], "y": w["celula"][1], "elevation": 0,
            "dest_map": w["alvo"], "dest_warp_id": str(w["destino_id"])})
    mj_cidade["connections"] = [
        c for c in (mj_cidade.get("connections") or [])
        if c["map"] not in {p["alvo"] for p in planos}]
    if not mj_cidade["connections"]:
        mj_cidade["connections"] = None
    grava_mapa(args.cidade, mj_cidade)

    for nome, e in plano_rotas.items():
        rota = e["rota"]
        for (rx, ry), gemeo in e["celulas"]:
            i = ry * rota.W + rx
            rota.blocos[i] = (rota.blocos[i] & ~MASCARA_ID) | gemeo
        grava_u16(rota.caminho_bin, rota.blocos)
        rota.mj.setdefault("warp_events", [])
        for w in e["warps"]:
            rota.mj["warp_events"].append({
                "x": w["celula"][0], "y": w["celula"][1], "elevation": 0,
                "dest_map": id_cidade, "dest_warp_id": str(w["destino_id"])})
        rota.mj["connections"] = [c for c in (rota.mj.get("connections") or [])
                                  if c["map"] != id_cidade] or None
        grava_mapa(nome, rota.mj)
        print(f"  gravado: {nome} ({len(e['warps'])} warps, conexão com "
              f"{id_cidade} removida)")

    tocados = cofre.escreve()
    print(f"  gravado: {args.cidade} ({len(novos_warps_cidade)} warps novos, "
          f"{len(planos)} conexões removidas)")
    print(f"  tilesets tocados, uma vez cada: {', '.join(tocados) or 'nenhum'}")
    return 0


def grava_mapa(nome_pasta, dados):
    caminho = os.path.join(RAIZ, "data/maps", nome_pasta, "map.json")
    # `indent=2` e SEM quebra de linha no fim: é a formatação exata que os 1.594
    # map.json da árvore já têm (conferido por round-trip em Route203), e sair
    # dela encheria o diff de ruído em arquivo que outras frentes também tocam.
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    sys.exit(main())
