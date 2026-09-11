#!/usr/bin/env python3
"""Copia uma cidade inteira de uma ROM hack para dentro do nosso repositório.

CONTRATO: `Pokemon Claude/METODO-COPIA-CIDADES.md`, decisão do Gui de 10/09/2026.
A regra zero é **não se inventa desenho**: copia-se o desenho do autor do hack,
inteiro (`map.bin`, `border.bin`, tiles, metatiles, atributos, paletas), e o jogo
continua sendo o nosso (warps, NPCs, gatilhos, scripts, conexões).

----------------------------------------------------------------------------
O QUE A MEDIÇÃO MOSTROU, E POR QUE O DESENHO DESTA FERRAMENTA É ESTE
----------------------------------------------------------------------------
A seção 3 do contrato manda a cidade copiada usar o NOSSO primário de Johto,
porque o motor desenha o mapa vizinho de uma conexão com os TILESETS DO MAPA
ATUAL, e sem primário comum a conexão vira lixo. Medido em 10/09/2026, essa
regra, ao pé da letra, **não é implementável**:

- `gTileset_JohtoGeneral` mais um secundário de cidade dão 384 vagas de metatile,
  384 de tile e 6 de paleta para arte nova.
- A Goldenrod do Scorched Silver usa **364 metatiles, 499 tiles e 8 paletas**; a
  do GS Chronicles usa **305, 626 e 12**. Nenhuma cabe, e o gargalo é o TILE.
- Nenhum metatile do hack casa com o nosso primário por prova de pixel: **0 de
  364**. São dois conjuntos de arte diferentes; casar por imagem é aproximar cor,
  e aproximar cor foi exatamente o que o Gui recusou em 09/09 (ESTADO 0.ae).

O que a costura EXIGE de verdade não é "o mesmo primário": é que **todo índice de
metatile que o mapa vizinho usa na faixa que a conexão desenha signifique a mesma
coisa nos dois lados**. Isso é bem menos que o primário inteiro. Medido, faixa de
8 tiles, por cidade: de 27 a 83 índices de primário e de 0 a 54 de secundário.

Daí o desenho: **a cidade ganha um PAR DE TILESETS PRÓPRIO** (primário novo de 640
e secundário novo de 384, usados só por ela) em que:

1. os índices que a costura usa são **pinados**: recebem o metatile que o nosso
   tileset de hoje tem naquele índice, redesenhado com os mesmos pixels e com o
   mesmo `(behavior, layerType)`;
2. todo o resto é a arte do hack, byte a byte;
3. as paletas dos dois lados são **empacotadas** nas 13 vagas do motor, sem
   aproximar cor nenhuma: duas cores só se fundem quando são o MESMO RGB.

Orçamento resultante: 1.024 vagas de metatile, 1.024 de tile e 13 de paleta, das
quais a costura come de 100 a 140 metatiles e de 2 a 6 paletas. Medido, as oito
cidades do Scorched Silver cabem. **As duas do GS Chronicles (Goldenrod e Violet)
NÃO cabem**: elas sozinhas pedem 12 e 11 vagas de paleta, e sobra 1 e 2 para uma
costura que precisa de 5 e 4. Isso é pergunta para o Gui, não escolha da
ferramenta, e está no relatório da frente.

----------------------------------------------------------------------------
E A COSTURA POR CONEXÃO NÃO EXISTE: MEDIDO EM 11/09/2026, EM ECRUTEAK
----------------------------------------------------------------------------
O pino acima conserta METADE de uma costura que, no fim, não tem conserto:

1. **O sentido inverso não tem pino.** De dentro da rota, a faixa da CIDADE é
   desenhada com o tileset DA ROTA. Consertar isso pediria mudar
   `gTileset_JohtoGeneral`, que é da região inteira. Só há um jeito: fazer as
   linhas de borda da cidade usarem os índices PINADOS, e aí a cidade perde a
   arte do autor nessas linhas (`dev_scripts/repinta_faixa_de_costura.py` faz e
   prova isso).
2. **E, mesmo com os dois sentidos pinados, ATRAVESSAR quebra tudo.**
   `LoadMapFromCameraTransition` (src/overworld.c, linhas 911 e 912) recarrega,
   numa travessia por conexão, **apenas o tileset SECUNDÁRIO e as paletas dele**:
   o jogo original garante que mapas ligados por conexão compartilham o
   PRIMÁRIO, então ele nunca recarrega o primário. Cidade copiada tem primário
   próprio, logo o jogador que anda da cidade para a rota leva o primário da
   cidade junto, e a rota inteira passa a ser desenhada com as paletas do hack.
   Medido em foto de emulador: árvore laranja, estrada preta, borda de lixo.

**A conclusão, e ela vale para TODA cidade que esta ferramenta copiar:** a cidade
copiada NÃO PODE TER CONEXÃO DE MAPA com vizinho que não compartilhe o primário
dela, ou seja, na prática, com nenhum. As travessias viram WARP (portão, prédio
ou tile de seta), que faz carga completa de mapa e não tem o defeito. Em Ecruteak
as quatro saídas viraram warp: portão a oeste, portão a leste, prédio dos sábios
ao norte e um par de MB_SOUTH_ARROW_WARP ao sul. `--costura` fica para o caso de
uma cidade que, por acaso, mantenha vizinho de primário igual.

----------------------------------------------------------------------------
A PROVA
----------------------------------------------------------------------------
Nada aqui é "ficou parecido". A ferramenta só fecha quando:

- **fidelidade**: o render do mapa copiado, feito a partir dos arquivos do repo,
  é IDÊNTICO pixel a pixel ao render do mapa do hack feito direto da ROM;
- **costura**: cada índice pinado renderiza IDÊNTICO ao que ele renderiza hoje no
  par de tilesets antigo, e tem o mesmo `(behavior, layerType)`;
- **planta**: os bits 10 a 15 de cada célula (colisão e elevação), que são do
  autor do hack, chegam intactos.

Qualquer uma dessas falhando, ela para e diz o número. Não existe modo "aplica
assim mesmo".

----------------------------------------------------------------------------
O QUE ELA NÃO FAZ, DITO NA CARA
----------------------------------------------------------------------------
- Não move warp, NPC, gatilho nem placa. Diz onde cada um caiu e o que há embaixo.
- Não recalcula offset de conexão. Diz o tamanho velho e o novo.
- Não escreve script nenhum, não cria flag nem var.
- Não aproxima cor, não quantiza, não "varia carimbo", não espalha peça.

USO
---
    python3 dev_scripts/copia_cidade.py --hack scorched-silver --mapa g0m0 \\
        --nosso AzaleaTown --saida /tmp/x --medir      # só mede, não escreve
    ...                                                 # monta em --saida
    ... --aplicar                                       # escreve no repo
    python3 dev_scripts/copia_cidade.py --demo          # provas, inclusive negativas
"""
import argparse
import json
import os
import random
import re
import shutil
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image  # noqa: E402

import render_maps as rm  # noqa: E402
import de_para_metatiles as dp  # noqa: E402

FERRAMENTAS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/ferramentas"
RAIZ_HACKS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
sys.path.insert(0, FERRAMENTAS)

import gbamap  # noqa: E402
import extrai_tileset as ext  # noqa: E402

REPO = rm.REPO
META_PX = rm.META_PX

MAPGRID_METATILE_ID_MASK = 0x03FF
MAPGRID_RESTO_MASK = 0xFC00

# Faixa do mapa vizinho que a conexão desenha. O motor guarda MAP_OFFSET = 7
# blocos de folga de cada lado (`include/fieldmap.h`); 8 é 7 mais um, e ser
# conservador aqui só custa vaga de metatile, que sobra.
FAIXA_COSTURA = 8

N_META_PRI = 640      # layout_version "johto" => bigPrimary
N_TILES_PRI = 640
N_PAL_PRI = 7
N_META_SEC = 1024 - N_META_PRI
N_TILES_SEC = 1024 - N_TILES_PRI
N_PAL_TOTAL = 13
CORES_POR_PALETA = 15  # a entrada 0 é transparente no BG e nunca é desenhada

FUNDO_PROVA = (255, 0, 255)


# ------------------------------------------------------------------ utilidades


def acha_rom(slug):
    if os.path.isfile(slug):
        return slug
    pasta = os.path.join(RAIZ_HACKS, slug)
    gbas = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")]
    if not gbas:
        raise SystemExit("ERRO: nenhuma .gba em %s" % pasta)
    return os.path.join(pasta, gbas[0])


def parse_gm(texto):
    t = texto.lower().strip()
    m = re.match(r"^g(\d+)m(\d+)$", t)
    if not m:
        raise SystemExit("ERRO: --mapa tem que ser da forma g0m1")
    return int(m.group(1)), int(m.group(2))


def nome_de_mapa_constante(constante):
    bruto = constante.replace("MAP_", "")
    cand = "".join(p.capitalize() for p in bruto.split("_"))
    if os.path.isdir(os.path.join(REPO, "data/maps", cand)):
        return cand
    alvo = bruto.replace("_", "").lower()
    for nome in sorted(os.listdir(os.path.join(REPO, "data/maps"))):
        if nome.replace("_", "").lower() == alvo:
            return nome
    return None


def flip_h(grade):
    return tuple(tuple(reversed(linha)) for linha in grade)


def flip_v(grade):
    return tuple(reversed(grade))


def orientacoes(grade):
    """As quatro orientações, com os bits de flip que levam a cada uma."""
    return [(grade, False, False),
            (flip_h(grade), True, False),
            (flip_v(grade), False, True),
            (flip_h(flip_v(grade)), True, True)]


# ------------------------------------------------------ leitura de um tileset


class Lado:
    """Um par primário+secundário já em memória, com o split certo.

    Serve tanto para o hack (pastas soltas extraídas da ROM) quanto para o nosso
    repositório (rótulos `gTileset_*`). O desenho é sempre o do `render_maps`,
    para não existirem duas verdades de desenho (regra 5 da seção 4 do
    PRD-REFINO).
    """

    def __init__(self, spec_pri, spec_sec, n_meta_pri, n_tiles_pri, n_pal_pri):
        self.par = dp.Par(spec_pri, spec_sec, "johto" if n_meta_pri == 640 else "emerald")
        self.par.n_meta_pri = n_meta_pri
        self.par.n_pal_pri = n_pal_pri
        self.n_meta_pri = n_meta_pri
        self.n_tiles_pri = n_tiles_pri
        self.n_pal_pri = n_pal_pri
        self.pri = self.par.pri
        self.sec = self.par.sec
        # O render_maps decide primário/secundário de TILE por len(tiles do
        # primário). Se o tiles.png do primário não tiver exatamente o split, os
        # dois discordam e todo índice de tile do secundário anda de lugar.
        if len(self.pri["tiles"]) != n_tiles_pri:
            raise SystemExit(
                "ERRO: o tiles.png do primário tem %d tiles e o split é %d. "
                "Sem isso o índice de tile do secundário anda." % (len(self.pri["tiles"]), n_tiles_pri))

    def local(self, idx):
        if idx < self.n_meta_pri:
            if idx >= self.pri["n_metatiles"]:
                return None
            return self.pri, idx
        loc = idx - self.n_meta_pri
        if loc >= self.sec["n_metatiles"]:
            return None
        return self.sec, loc

    def atributo(self, idx):
        alvo = self.local(idx)
        if alvo is None:
            return None
        ts, loc = alvo
        if loc >= len(ts["atributos"]):
            return None
        return ts["atributos"][loc]

    def entradas(self, idx):
        """As 8 entradas de um metatile, já resolvidas em conteúdo.

        Devolve lista de (grade_do_tile, flip_h, flip_v, cores_da_paleta,
        chave_da_paleta) ou None onde não há tile.
        """
        alvo = self.local(idx)
        if alvo is None:
            return None
        ts, loc = alvo
        saida = []
        for idx_tile, fh, fv, idx_pal in rm.entradas_metatile(ts["metatiles"], loc):
            tile = rm.resolver_tile(self.pri, self.sec, idx_tile)
            fonte = self.pri if idx_pal < self.n_pal_pri else self.sec
            cores = fonte["paletas"].get(idx_pal)
            if tile is None or cores is None:
                saida.append(None)
                continue
            grade = tuple(tuple(linha) for linha in tile)
            chave = (id(fonte), idx_pal)
            saida.append((grade, fh, fv, tuple(tuple(c) for c in cores), chave))
        return saida

    def desenha(self, idx, fundo=FUNDO_PROVA):
        ent = self.entradas(idx)
        if ent is None:
            return None
        img = Image.new("RGB", (META_PX, META_PX), fundo)
        px = img.load()
        for camada in (0, 1):
            for q in range(4):
                e = ent[camada * 4 + q]
                if e is None:
                    continue
                grade, fh, fv, cores, _ = e
                qx, qy = (q % 2) * rm.TILE_PX, (q // 2) * rm.TILE_PX
                rm.desenhar_tile(px, qx, qy, grade, cores, fh, fv)
        return img


# ------------------------------------------------------- empacotar as paletas


def cores_usadas(entradas_por_metatile):
    """{chave_de_paleta: (cores_visiveis, cores16_originais)}.

    Cor visível é a que algum PIXEL de algum tile realmente usa com aquela
    paleta. Contar as 16 cores declaradas no `.pal` desperdiça vaga: medido,
    Goldenrod do Scorched Silver declara 8 paletas de 16 e usa 61 cores.
    """
    visiveis = {}
    originais = {}
    for entradas in entradas_por_metatile:
        if entradas is None:
            continue
        for e in entradas:
            if e is None:
                continue
            grade, _fh, _fv, cores, chave = e
            originais[chave] = cores
            alvo = visiveis.setdefault(chave, set())
            for linha in grade:
                for c in linha:
                    if c:
                        alvo.add(cores[c] if c < len(cores) else (0, 0, 0))
    return visiveis, originais


def empacota_paletas(visiveis, vagas=N_PAL_TOTAL, cap=CORES_POR_PALETA, tentativas=3000, semente=7):
    """Junta paletas de origem em no máximo `vagas` grupos de `cap` cores.

    REGRA DE OURO, herdada do `compacta_paletas.py`: se duas cores não são
    idênticas, elas NÃO se fundem. Não há quantização nem distância de cor. Duas
    paletas de origem entram no mesmo grupo quando a UNIÃO das cores que elas
    realmente usam cabe em 15.

    A unidade do agrupamento é a paleta de ORIGEM inteira: um tile indexa uma
    paleta só, então as cores de uma origem têm de cair todas no mesmo grupo.
    """
    chaves = list(visiveis)
    melhor = None
    rnd = random.Random(semente)
    for t in range(tentativas):
        ordem = sorted(chaves, key=lambda k: -len(visiveis[k])) if t == 0 else rnd.sample(chaves, len(chaves))
        grupos = []
        for k in ordem:
            s = visiveis[k]
            escolha = None
            for i, g in enumerate(grupos):
                u = len(g["cores"] | s)
                if u <= cap and (escolha is None or u < escolha[1]):
                    escolha = (i, u)
            if escolha is not None:
                grupos[escolha[0]]["cores"] |= s
                grupos[escolha[0]]["origens"].append(k)
            else:
                grupos.append({"cores": set(s), "origens": [k]})
        if melhor is None or len(grupos) < len(melhor):
            melhor = grupos
        if len(melhor) <= vagas:
            break
    return melhor


# ------------------------------------------------------------------- o núcleo


class Copia:
    def __init__(self, args):
        self.args = args
        self.slug = args.hack
        self.caminho_rom = acha_rom(args.hack)
        self.rom = gbamap.Rom(self.caminho_rom)
        self.g, self.m = parse_gm(args.mapa)
        with open(os.path.join(FERRAMENTAS, "inv", args.hack + ".json"), encoding="utf-8") as f:
            inv = json.load(f)
        grupos = {x["g"]: x for x in inv["grupos"]}
        if self.g not in grupos or self.m >= len(grupos[self.g]["mapas"]) or not grupos[self.g]["mapas"][self.m]:
            raise SystemExit("ERRO: %s não tem g%dm%d" % (args.hack, self.g, self.m))
        self.hdr = grupos[self.g]["mapas"][self.m]
        self.lay_hack = self.hdr["layout"]

        self.split_hack = self.detecta_split()
        self.layouts = rm.carregar_layouts()
        with open(os.path.join(REPO, "data/maps", args.nosso, "map.json"), encoding="utf-8") as f:
            self.mapa_nosso = json.load(f)
        self.lay_nosso = self.layouts[self.mapa_nosso["layout"]]
        if self.lay_nosso.get("layout_version") != "johto":
            raise SystemExit("ERRO: esta frente só copia mapa de layout_version 'johto'; "
                             "%s é '%s'." % (args.nosso, self.lay_nosso.get("layout_version")))

    # ------------------------------------------------------------- lado hack

    def detecta_split(self):
        """Split de VRAM do hack, escolhido por quem deixa menos tile preto."""
        from render_hack import Render
        guardado = (self.rom.n_meta_pri, self.rom.n_tiles_pri, self.rom.n_pal_pri)
        melhor = None
        for nm, nt, npal in ((512, 512, 6), (640, 640, 7), (512, 512, 7), (640, 640, 6)):
            self.rom.n_meta_pri, self.rom.n_tiles_pri, self.rom.n_pal_pri = nm, nt, npal
            try:
                img = Render(self.rom).mapa(self.hdr)
            except Exception:
                img = None
            if img is None:
                continue
            px = img.load()
            pretos = total = 0
            for y in range(0, img.size[1], 8):
                for x in range(0, img.size[0], 8):
                    total += 1
                    if px[x, y] == (0, 0, 0):
                        pretos += 1
            frac = pretos / total if total else 1.0
            if melhor is None or frac < melhor[0] - 0.005:
                melhor = (frac, nm, nt, npal)
        self.rom.n_meta_pri, self.rom.n_tiles_pri, self.rom.n_pal_pri = guardado
        if melhor is None:
            raise SystemExit("ERRO: nenhum split de VRAM desenhou o mapa do hack.")
        return melhor

    def le_mapa_hack(self):
        L = self.lay_hack
        w, h = L["w"], L["h"]
        n = w * h
        if L["blockdata"] + n * 2 > len(self.rom.rom):
            raise SystemExit("ERRO: blockdata do hack fora da ROM")
        palavras = list(struct.unpack_from("<%dH" % n, self.rom.rom, L["blockdata"]))
        bw = bh = 2
        if self.rom.frlg and L["off"] + 0x1A <= len(self.rom.rom):
            cbw, cbh = self.rom.rom[L["off"] + 0x18], self.rom.rom[L["off"] + 0x19]
            if 1 <= cbw <= 4 and 1 <= cbh <= 4:
                bw, bh = cbw, cbh
        nb = bw * bh
        borda = list(struct.unpack_from("<%dH" % nb, self.rom.rom, L["border"])) \
            if L["border"] + nb * 2 <= len(self.rom.rom) else [0] * nb
        return w, h, palavras, bw, bh, borda

    def extrai_hack(self, destino):
        _frac, nm, nt, npal = self.split_hack
        pri = os.path.join(destino, "hack_primario")
        sec = os.path.join(destino, "hack_secundario")
        # guardar e repor o split do gbamap: o extrai_tileset usa r.n_meta_pri
        # para saber quantos metatiles ler de cada lado.
        r = gbamap.Rom(self.caminho_rom)
        r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = nm, nt, npal
        for offset, saida, is_sec in ((self.lay_hack["ts1"], pri, False), (self.lay_hack["ts2"], sec, True)):
            ts = r.parse_tileset(offset)
            if ts is None:
                raise SystemExit("ERRO: 0x%06X não parseia como tileset" % offset)
        ext.extrai(self.caminho_rom, self.lay_hack["ts1"], pri, False, "hack_primario", nm, "2")
        ext.extrai(self.caminho_rom, self.lay_hack["ts2"], sec, True, "hack_secundario", nm, "2")
        return pri, sec

    # ------------------------------------------------------------ lado nosso

    def lado_de(self, pri, sec):
        """Um `Lado` por par de tilesets, guardado, porque abrir custa caro."""
        chave = (pri, sec)
        if not hasattr(self, "_lados"):
            self._lados = {}
        if chave not in self._lados:
            self._lados[chave] = Lado(pri, sec, N_META_PRI, N_TILES_PRI, N_PAL_PRI)
        return self._lados[chave]

    def costura(self):
        """Índices que os vizinhos usam na faixa da conexão, e de QUEM é a arte.

        Medido em 11/09/2026 em Ecruteak, e é a correção da regra antiga: pinar
        só o que usa O MESMO tileset deixa a costura suja quando o vizinho usa um
        primário IRMÃO. Route37 é `gTileset_JohtoGeneral` e Ecruteak é
        `gTileset_JohtoNorthWest`; hoje os 12 índices que a Route37 usa na faixa
        desenham DIFERENTE nos dois (12 de 12, prova de pixel), mas desenham
        árvore dos dois lados, então o jogador não vê defeito. Trocado o primário
        da cidade pela arte do hack, os mesmos 12 índices viram telhado e água: aí
        sim é lixo. Então o índice é pinado com a arte do TILESET DO VIZINHO, seja
        ele qual for, e não com a do nosso.

        Devolve {indice: (primario_do_vizinho, secundario_do_vizinho)} e o
        detalhe por conexão. Quando dois vizinhos pedem o MESMO índice com arte
        diferente, ganha o primeiro da lista de `connections` e o conflito é
        DENUNCIADO, nunca resolvido no escuro.
        """
        pin = {}
        conflitos = []
        detalhe = []
        so = getattr(self.args, "costura", None)
        so = [x.strip() for x in so.split(",")] if so else None
        for c in (self.mapa_nosso.get("connections") or []):
            if so is not None and c["direction"] not in so:
                detalhe.append({"direcao": c["direction"], "mapa": c["map"],
                                "situacao": "fora de --costura: a faixa dele nunca entra na câmera de dentro da cidade",
                                "primario": "-", "secundario": "-", "indices_da_faixa": 0, "indices_pinados": 0})
                continue
            alvo = nome_de_mapa_constante(c["map"])
            if alvo is None:
                detalhe.append({"direcao": c["direction"], "mapa": c["map"], "situacao": "pasta não achada"})
                continue
            with open(os.path.join(REPO, "data/maps", alvo, "map.json"), encoding="utf-8") as f:
                vj = json.load(f)
            lv = self.layouts.get(vj["layout"])
            if lv is None:
                detalhe.append({"direcao": c["direction"], "mapa": alvo, "situacao": "layout não achado"})
                continue
            dados = open(os.path.join(REPO, lv["blockdata_filepath"]), "rb").read()
            w, h = lv["width"], lv["height"]
            d = c["direction"]
            if d == "up":
                ys, xs = range(max(0, h - FAIXA_COSTURA), h), range(w)
            elif d == "down":
                ys, xs = range(0, min(h, FAIXA_COSTURA)), range(w)
            elif d == "left":
                ys, xs = range(h), range(max(0, w - FAIXA_COSTURA), w)
            elif d == "right":
                ys, xs = range(h), range(0, min(w, FAIXA_COSTURA))
            else:
                detalhe.append({"direcao": d, "mapa": alvo, "situacao": "sem faixa (dive/emerge)"})
                continue
            par = (lv["primary_tileset"], lv["secondary_tileset"])
            achados = set()
            for y in ys:
                for x in xs:
                    v = struct.unpack_from("<H", dados, (y * w + x) * 2)[0] & MAPGRID_METATILE_ID_MASK
                    achados.add(v)
            meus = 0
            for v in sorted(achados):
                if v not in pin:
                    pin[v] = par
                    meus += 1
                elif pin[v] != par:
                    dono = self.lado_de(*pin[v])
                    meu = self.lado_de(*par)
                    a, b = dono.desenha(v), meu.desenha(v)
                    igual = (a is not None and b is not None and a.tobytes() == b.tobytes()
                             and dono.atributo(v) == meu.atributo(v))
                    if not igual:
                        conflitos.append({"indice": v, "fica_com": list(pin[v]), "perdeu": [alvo, list(par)]})
            detalhe.append({"direcao": d, "mapa": alvo,
                            "primario": lv["primary_tileset"], "secundario": lv["secondary_tileset"],
                            "indices_da_faixa": len(achados), "indices_pinados": meus})
        return pin, detalhe, conflitos

    # ---------------------------------------------------------------- montar

    def monta(self, destino, so_medir=False):
        os.makedirs(destino, exist_ok=True)
        pasta_pri, pasta_sec = self.extrai_hack(destino)
        _frac, nm, nt, npal = self.split_hack
        hack = Lado(pasta_pri, pasta_sec, nm, nt, npal)
        nosso = Lado(self.lay_nosso["primary_tileset"], self.lay_nosso["secondary_tileset"],
                     N_META_PRI, N_TILES_PRI, N_PAL_PRI)

        w, h, palavras, bw, bh, borda = self.le_mapa_hack()
        usados = sorted({v & MAPGRID_METATILE_ID_MASK for v in palavras + borda})
        dono_do_pin, detalhe_conexoes, conflitos_costura = self.costura()
        pin = sorted(dono_do_pin)

        # -------- entradas de cada metatile dos dois lados
        ent_hack = {i: hack.entradas(i) for i in usados}
        quebrados = [i for i, e in ent_hack.items() if e is None]
        if quebrados:
            raise SystemExit("ERRO: o hack usa %d metatiles que não existem no tileset dele: %s"
                             % (len(quebrados), quebrados[:10]))
        ent_pin = {i: self.lado_de(*dono_do_pin[i]).entradas(i) for i in pin}
        pin_quebrado = [i for i, e in ent_pin.items() if e is None]
        if pin_quebrado:
            raise SystemExit("ERRO: costura pede metatile que o nosso tileset não tem: %s" % pin_quebrado[:10])

        # -------- paletas
        vis_hack, orig_hack = cores_usadas(ent_hack.values())
        vis_pin, orig_pin = cores_usadas(ent_pin.values())
        visiveis = dict(vis_hack)
        originais = dict(orig_hack)
        for k, v in vis_pin.items():
            visiveis[k] = visiveis.get(k, set()) | v
            originais[k] = orig_pin[k]
        grupos = empacota_paletas(visiveis)
        cabe_pal = len(grupos) <= N_PAL_TOTAL

        # -------- vagas de metatile
        pin_pri = [i for i in pin if i < N_META_PRI]
        pin_sec = [i for i in pin if i >= N_META_PRI]
        vagas_meta = (N_META_PRI - len(pin_pri)) + (N_META_SEC - len(pin_sec))
        cabe_meta = len(usados) <= vagas_meta

        medida = {
            "hack": self.slug, "mapa_hack": "g%dm%d" % (self.g, self.m),
            "rom": os.path.basename(self.caminho_rom),
            "nosso": self.args.nosso,
            "split_hack": {"metatiles": nm, "tiles": nt, "paletas": npal,
                           "frac_preto": round(self.split_hack[0], 5)},
            "tamanho_hack": [w, h], "tamanho_nosso": [self.lay_nosso["width"], self.lay_nosso["height"]],
            "border_hack": [bw, bh],
            "metatiles_do_hack": len(usados),
            "costura": {"pinados_primario": len(pin_pri), "pinados_secundario": len(pin_sec),
                        "indices": pin, "conexoes": detalhe_conexoes,
                        "conflitos": conflitos_costura,
                        "dono": {str(i): list(dono_do_pin[i]) for i in pin}},
            "paletas": {"origens": len(visiveis), "cores_distintas": len(set().union(*visiveis.values()) if visiveis else set()),
                        "grupos": len(grupos), "vagas": N_PAL_TOTAL, "cabe": cabe_pal},
            "metatiles": {"precisa": len(usados), "vagas": vagas_meta, "cabe": cabe_meta},
        }

        if not (cabe_pal and cabe_meta):
            medida["veredito"] = "NAO CABE"
            self.medida = medida
            return medida, None
        if so_medir:
            # o custo de tile só é conhecido depois de resolver a paleta de cada
            # entrada, e isso é o próprio plano; medir de verdade é montar.
            pass

        # -------- vaga de paleta por origem
        slot_de_origem = {}
        cores_do_slot = []
        for i, g in enumerate(grupos):
            ordenadas = sorted(g["cores"])
            cores_do_slot.append(ordenadas)
            for k in g["origens"]:
                slot_de_origem[k] = i
        # cor 0 (transparente) copiada de uma origem do grupo, só para o .pal
        # ficar legível no Porymap; ela nunca é desenhada.
        zero_do_slot = []
        for i, g in enumerate(grupos):
            k = g["origens"][0]
            zero_do_slot.append(originais[k][0] if originais.get(k) else (0, 0, 0))

        indice_no_slot = [{c: j + 1 for j, c in enumerate(cores_do_slot[i])} for i in range(len(grupos))]

        # -------- tiles: a unidade é (conteúdo canônico, vaga de paleta)
        tiles = {}          # (grade_canonica, slot) -> indice novo
        ordem_tiles = []

        # O TILE 0 TEM DE SER VAZIO, e isto não é estética: é contrato do motor.
        # `DrawMetatile` (src/field_camera.c) escreve o VALOR 0 direto no tilemap
        # do BG1 em todo metatile COVERED e no do BG2 em todo SPLIT, para dizer
        # "aqui não tem nada nesta camada". Valor 0 é tile 0 com paleta 0, e todo
        # tileset do jogo tem o tile 0 transparente, então isso desenha nada.
        # A ferramenta empacotava os tiles do hack a partir do índice 0 e punha
        # ARTE no tile 0: medido em Ecruteak em 11/09/2026, o resultado é um
        # bloco opaco desenhado POR CIMA de cada célula COVERED e por cima do
        # JOGADOR, que some da tela. O render do repo não via nada disso, porque
        # ele desenha metatile por metatile e não emula a regra do BG1.
        # Por isso o primeiro tile da fila é, sempre, o tile todo na cor 0.
        vazio = tuple(tuple(0 for _ in range(rm.TILE_PX)) for _ in range(rm.TILE_PX))
        tiles[(vazio, 0)] = 0
        ordem_tiles.append((vazio, 0))

        def resolve_tile(grade, fh, fv, cores, chave):
            """Devolve (indice_novo, flip_h, flip_v) do tile já remapeado."""
            slot = slot_de_origem[chave]
            mapa_cor = indice_no_slot[slot]
            # remapeia os nibbles do tile para a ordem de cor do grupo
            novo = tuple(tuple(0 if c == 0 else mapa_cor[cores[c] if c < len(cores) else (0, 0, 0)]
                               for c in linha) for linha in grade)
            for cand, cfh, cfv in orientacoes(novo):
                achado = tiles.get((cand, slot))
                if achado is not None:
                    return achado, fh ^ cfh, fv ^ cfv
            idx = len(ordem_tiles)
            tiles[(novo, slot)] = idx
            ordem_tiles.append((novo, slot))
            return idx, fh, fv

        # Quadrante VAZIO: o metatile do hack aponta para um tile que NÃO existe
        # no tileset do próprio hack. Acontece de verdade: o ginásio de Ecruteak
        # do GS Chronicles (g10m16) tem 11 referências de tile acima dos 63 tiles
        # que o secundário dele carrega, medido em 11/09/2026. O render do hack
        # desenha isso como nada (fundo), e é isso que o autor vê. Escrever tile
        # 0 com paleta 0 no lugar INVENTA um bloco cinza que o autor nunca
        # desenhou, e foi o que reprovou a prova B com 1.920 pixels. O certo é um
        # tile todo na cor 0 (transparente), que desenha nada dos dois lados.
        # Ele é contado e DENUNCIADO no relatório, nunca escondido.
        quadrantes_vazios = []

        def tile_vazio():
            return tiles[(vazio, 0)]

        def monta_metatile(entradas, dono=None):
            saida = []
            for k, e in enumerate(entradas):
                if e is None:
                    quadrantes_vazios.append([dono, k])
                    saida.append((tile_vazio(), False, False, 0))
                    continue
                grade, fh, fv, cores, chave = e
                idx, nfh, nfv = resolve_tile(grade, fh, fv, cores, chave)
                saida.append((idx, nfh, nfv, slot_de_origem[chave]))
            return saida

        montado_pin = {i: monta_metatile(ent_pin[i], ("pin", i)) for i in pin}
        montado_hack = {i: monta_metatile(ent_hack[i], ("hack", i)) for i in usados}
        medida["quadrantes_vazios"] = {"n": len(quadrantes_vazios), "onde": quadrantes_vazios[:40]}

        n_tiles = len(ordem_tiles)
        medida["tiles"] = {"precisa": n_tiles, "vagas": N_TILES_PRI + N_TILES_SEC,
                           "cabe": n_tiles <= N_TILES_PRI + N_TILES_SEC}
        if n_tiles > N_TILES_PRI + N_TILES_SEC:
            medida["veredito"] = "NAO CABE"
            self.medida = medida
            return medida, None

        # -------- vagas de metatile: pinados no lugar, hack no que sobra
        de_para = {}
        livres_pri = [i for i in range(N_META_PRI) if i not in set(pin_pri)]
        livres_sec = [i for i in range(N_META_PRI, 1024) if i not in set(pin_sec)]
        fila = livres_pri + livres_sec
        for j, idx_hack in enumerate(usados):
            de_para[idx_hack] = fila[j]

        # -------- monta os dois tilesets
        def entrada_bin(t):
            idx, fh, fv, pal = t
            return (idx & 0x3FF) | (0x400 if fh else 0) | (0x800 if fv else 0) | ((pal & 0xF) << 12)

        meta_pri = bytearray(16 * N_META_PRI)
        meta_sec = bytearray(16 * N_META_SEC)
        attr_pri = bytearray(2 * N_META_PRI)
        attr_sec = bytearray(2 * N_META_SEC)

        def grava(idx_global, entradas, attr):
            if idx_global < N_META_PRI:
                alvo_meta, alvo_attr, loc = meta_pri, attr_pri, idx_global
            else:
                alvo_meta, alvo_attr, loc = meta_sec, attr_sec, idx_global - N_META_PRI
            for k, t in enumerate(entradas):
                struct.pack_into("<H", alvo_meta, loc * 16 + k * 2, entrada_bin(t))
            comportamento, camada = attr
            struct.pack_into("<H", alvo_attr, loc * 2, (comportamento & 0xFF) | ((camada & 0xF) << 12))

        for i in pin:
            grava(i, montado_pin[i], self.lado_de(*dono_do_pin[i]).atributo(i) or (0, 0))
        for i in usados:
            grava(de_para[i], montado_hack[i], hack.atributo(i) or (0, 0))

        plano = {
            "medida": medida, "de_para": de_para, "pin": pin, "dono_do_pin": dono_do_pin,
            "grupos_paleta": [{"slot": i, "cores": cores_do_slot[i], "zero": list(zero_do_slot[i]),
                               "n_cores": len(cores_do_slot[i])} for i in range(len(grupos))],
            "tiles": ordem_tiles, "meta_pri": bytes(meta_pri), "meta_sec": bytes(meta_sec),
            "attr_pri": bytes(attr_pri), "attr_sec": bytes(attr_sec),
            "mapa": {"w": w, "h": h, "palavras": palavras, "bw": bw, "bh": bh, "borda": borda},
            "hack_lado": hack, "nosso_lado": nosso,
            "montado_pin": montado_pin, "montado_hack": montado_hack,
        }
        medida["veredito"] = "CABE"
        self.medida = medida
        self.plano = plano
        return medida, plano


# ------------------------------------------------------------------ escrever


def escreve_tileset(pasta, tiles, faixa, grupos, meta, attr, n_tiles_arquivo):
    """Grava tiles.png, palettes/, metatiles.bin e metatile_attributes.bin."""
    os.makedirs(os.path.join(pasta, "palettes"), exist_ok=True)
    largura = 16 * 8
    n_linhas = (n_tiles_arquivo + 15) // 16
    img = Image.new("P", (largura, n_linhas * 8), 0)
    px = img.load()
    for i, idx in enumerate(faixa):
        grade = tiles[idx][0]
        ox, oy = (i % 16) * 8, (i // 16) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = grade[y][x]
    plana = []
    base = grupos[0]["cores"] if grupos else []
    for c in [tuple(grupos[0]["zero"])] + [tuple(c) for c in base] if grupos else []:
        plana += list(c)
    plana += [0] * (768 - len(plana))
    img.putpalette(plana)
    img.save(os.path.join(pasta, "tiles.png"))

    for slot in range(16):
        cores = [(0, 0, 0)] * 16
        g = next((x for x in grupos if x["slot"] == slot), None)
        if g:
            cores[0] = tuple(g["zero"])
            for j, c in enumerate(g["cores"]):
                cores[j + 1] = tuple(c)
        ext.escreve_pal(os.path.join(pasta, "palettes", "%02d.pal" % slot), cores)

    with open(os.path.join(pasta, "metatiles.bin"), "wb") as f:
        f.write(meta)
    with open(os.path.join(pasta, "metatile_attributes.bin"), "wb") as f:
        f.write(attr)


def escreve_saida(copia, plano, destino):
    """Escreve, em --saida, tudo que `--aplicar` depois copia para o repo."""
    tiles = plano["tiles"]
    if any(any(v for v in linha) for linha in tiles[0][0]):
        raise SystemExit("ERRO: o tile 0 do tileset novo não é vazio. O motor "
                         "escreve tile 0 no BG1 de todo metatile COVERED; com "
                         "arte ali, ela tapa a célula e o jogador.")
    n = len(tiles)
    faixa_pri = list(range(min(n, N_TILES_PRI)))
    faixa_sec = list(range(N_TILES_PRI, n))
    grupos = plano["grupos_paleta"]
    pasta_pri = os.path.join(destino, "tileset_primario")
    pasta_sec = os.path.join(destino, "tileset_secundario")
    escreve_tileset(pasta_pri, tiles, faixa_pri, [g for g in grupos if g["slot"] < N_PAL_PRI],
                    plano["meta_pri"], plano["attr_pri"], N_TILES_PRI)
    escreve_tileset(pasta_sec, tiles, faixa_sec, [g for g in grupos if g["slot"] >= N_PAL_PRI],
                    plano["meta_sec"], plano["attr_sec"], max(1, len(faixa_sec)))

    mp = plano["mapa"]
    de_para = plano["de_para"]
    novo = bytearray()
    for v in mp["palavras"]:
        idx = v & MAPGRID_METATILE_ID_MASK
        novo += struct.pack("<H", (de_para[idx] & MAPGRID_METATILE_ID_MASK) | (v & MAPGRID_RESTO_MASK))
    with open(os.path.join(destino, "map.bin"), "wb") as f:
        f.write(novo)
    nb = bytearray()
    for v in mp["borda"][:4]:
        idx = v & MAPGRID_METATILE_ID_MASK
        nb += struct.pack("<H", (de_para[idx] & MAPGRID_METATILE_ID_MASK) | (v & MAPGRID_RESTO_MASK))
    while len(nb) < 8:
        nb += struct.pack("<H", 0)
    with open(os.path.join(destino, "border.bin"), "wb") as f:
        f.write(nb[:8])
    return pasta_pri, pasta_sec


# --------------------------------------------------------------------- provas


def desenha_mapa(lado, w, h, palavras, fundo=(0, 0, 0)):
    """Mapa inteiro desenhado por um Lado. Um só desenhador, sem segunda verdade."""
    img = Image.new("RGB", (w * META_PX, h * META_PX), fundo)
    cache = {}
    for i, v in enumerate(palavras):
        idx = v & MAPGRID_METATILE_ID_MASK
        if idx not in cache:
            cache[idx] = lado.desenha(idx, fundo)
        peca = cache[idx]
        if peca is None:
            continue
        img.paste(peca, ((i % w) * META_PX, (i // w) * META_PX))
    return img


def difere(a, b):
    """(n_pixels_diferentes, primeiro (x,y) diferente) entre duas imagens RGB."""
    if a.size != b.size:
        return -1, None
    pa, pb = a.load(), b.load()
    n = 0
    primeiro = None
    for y in range(a.size[1]):
        for x in range(a.size[0]):
            if pa[x, y] != pb[x, y]:
                n += 1
                if primeiro is None:
                    primeiro = (x, y)
    return n, primeiro


def prova(copia, plano, destino):
    """As três provas que o contrato exige. Falha dura, sem 'aplica assim mesmo'."""
    resultado = {}
    mp = plano["mapa"]
    hack = plano["hack_lado"]
    nosso = plano["nosso_lado"]

    # A. a extração da ROM é fiel: o desenho pelo tileset extraído bate com o
    #    desenho feito direto da ROM pelo render_hack (outro código, outro
    #    caminho de dado).
    from render_hack import Render
    r = gbamap.Rom(copia.caminho_rom)
    _f, nm, nt, npal = copia.split_hack
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = nm, nt, npal
    img_rom = Render(r).mapa(copia.hdr)
    img_ext = desenha_mapa(hack, mp["w"], mp["h"], mp["palavras"])
    n_a, onde_a = difere(img_rom, img_ext)
    resultado["extracao_fiel"] = {"pixels_diferentes": n_a, "primeiro": onde_a}

    # B. a cópia é fiel: o desenho a partir dos ARQUIVOS DO REPO bate com o do
    #    hack, pixel a pixel.
    novo = Lado(os.path.join(destino, "tileset_primario"),
                os.path.join(destino, "tileset_secundario"),
                N_META_PRI, N_TILES_PRI, N_PAL_PRI)
    palavras_novas = []
    dados = open(os.path.join(destino, "map.bin"), "rb").read()
    for i in range(len(dados) // 2):
        palavras_novas.append(struct.unpack_from("<H", dados, i * 2)[0])
    img_copia = desenha_mapa(novo, mp["w"], mp["h"], palavras_novas)
    n_b, onde_b = difere(img_ext, img_copia)
    resultado["copia_fiel"] = {"pixels_diferentes": n_b, "primeiro": onde_b}

    # C. a costura é fiel: cada índice pinado desenha igual e tem o mesmo
    #    (behavior, layerType) de hoje.
    ruins = []
    for i in plano["pin"]:
        dono = copia.lado_de(*plano["dono_do_pin"][i])
        a, b = dono.desenha(i), novo.desenha(i)
        if a is None or b is None or a.tobytes() != b.tobytes():
            ruins.append((i, "pixel"))
            continue
        if dono.atributo(i) != novo.atributo(i):
            ruins.append((i, "atributo %s != %s" % (dono.atributo(i), novo.atributo(i))))
    resultado["costura_fiel"] = {"pinados": len(plano["pin"]), "ruins": ruins[:20], "n_ruins": len(ruins)}

    # D. a planta do autor chegou intacta: bits 10 a 15 iguais, célula a célula.
    n_d = sum(1 for a, b in zip(mp["palavras"], palavras_novas)
              if (a & MAPGRID_RESTO_MASK) != (b & MAPGRID_RESTO_MASK))
    resultado["colisao_intacta"] = {"celulas_diferentes": n_d}

    resultado["passou"] = (n_a == 0 and n_b == 0 and not ruins and n_d == 0)
    return resultado, img_rom, img_copia


def relatorio_de_jogo(copia, plano, destino):
    """Onde cada warp, objeto e placa NOSSO caiu, e o que há embaixo dele.

    Matéria-prima do remapeamento. A ferramenta não move nada: mover é escolha
    de desenho, e escolha de desenho é de gente.
    """
    mp = plano["mapa"]
    novo = Lado(os.path.join(destino, "tileset_primario"),
                os.path.join(destino, "tileset_secundario"),
                N_META_PRI, N_TILES_PRI, N_PAL_PRI)
    dados = open(os.path.join(destino, "map.bin"), "rb").read()
    w, h = mp["w"], mp["h"]

    def sob(x, y):
        if not (0 <= x < w and 0 <= y < h):
            return None
        v = struct.unpack_from("<H", dados, (y * w + x) * 2)[0]
        idx = v & MAPGRID_METATILE_ID_MASK
        attr = novo.atributo(idx) or (0, 0)
        return {"metatile": idx, "behavior": attr[0], "layer": attr[1],
                "colisao": (v >> 10) & 0x3, "elevacao": (v >> 12) & 0xF}

    saida = {"tamanho_novo": [w, h],
             "tamanho_antigo": [copia.lay_nosso["width"], copia.lay_nosso["height"]],
             "warps": [], "objetos": [], "placas": [], "gatilhos": []}
    for nome, chave in (("warps", "warp_events"), ("objetos", "object_events"),
                        ("placas", "bg_events"), ("gatilhos", "coord_events")):
        for i, e in enumerate(copia.mapa_nosso.get(chave) or []):
            x, y = e.get("x"), e.get("y")
            saida[nome].append({"i": i, "x": x, "y": y, "dentro": bool(sob(x, y)), "sob": sob(x, y),
                                "id": e.get("dest_warp_id") if chave == "warp_events" else e.get("local_id")})
    return saida


def prancha(copia, destino, img_hack, img_copia):
    """A prancha do portão de gosto: nosso antes | hack | cópia, na mesma escala.

    É esta imagem que o condutor Fable abre e o Gui aprova. Sem ela a cidade não
    entra no master, por mais verde que esteja o build (lição 3 da ESTADO 0.ae).
    """
    antes = Lado(copia.lay_nosso["primary_tileset"], copia.lay_nosso["secondary_tileset"],
                 N_META_PRI, N_TILES_PRI, N_PAL_PRI)
    dados = open(os.path.join(REPO, copia.lay_nosso["blockdata_filepath"]), "rb").read()
    w, h = copia.lay_nosso["width"], copia.lay_nosso["height"]
    palavras = [struct.unpack_from("<H", dados, i * 2)[0] for i in range(w * h)]
    img_antes = desenha_mapa(antes, w, h, palavras)

    partes = [("nosso ANTES", img_antes), ("hack (%s)" % copia.slug, img_hack), ("CÓPIA", img_copia)]
    margem, faixa = 12, 22
    alt = max(p[1].size[1] for p in partes) + faixa + margem * 2
    larg = sum(p[1].size[0] for p in partes) + margem * (len(partes) + 1)
    folha = Image.new("RGB", (larg, alt), (24, 24, 24))
    from PIL import ImageDraw
    d = ImageDraw.Draw(folha)
    x = margem
    for rotulo, img in partes:
        folha.paste(img, (x, faixa + margem))
        d.text((x, 6), "%s  %dx%d" % (rotulo, img.size[0] // META_PX, img.size[1] // META_PX),
               fill=(255, 255, 255))
        x += img.size[0] + margem
    caminho = os.path.join(destino, "%s-antes-depois.png" % copia.args.nosso)
    folha.save(caminho)
    return caminho


def _snake(label):
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", label).lower()
    return re.sub(r"[^a-z0-9_]", "_", s)


def aplica(copia, plano, destino):
    """Escreve no repositório. Só acrescenta declaração; nunca mexe no que existe.

    O `mapLayoutId` NÃO muda e a pasta do layout é a mesma: o layout é
    substituído no lugar, que é o que a seção 1 do contrato exige para a save
    continuar valendo.
    """
    base = re.sub(r"[^A-Za-z0-9]", "", copia.args.nosso)
    rot_pri, rot_sec = base + "CopiaPri", base + "CopiaSec"
    alvos = []
    for rotulo, origem, lado in ((rot_pri, "tileset_primario", "primary"),
                                 (rot_sec, "tileset_secundario", "secondary")):
        rel = "data/tilesets/%s/%s" % (lado, _snake(rotulo))
        dst = os.path.join(REPO, rel)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(destino, origem), dst)
        alvos.append((rotulo, rel, lado == "secondary"))

    caminhos = {
        "graphics": os.path.join(REPO, "src/data/tilesets/graphics.h"),
        "metatiles": os.path.join(REPO, "src/data/tilesets/metatiles.h"),
        "headers": os.path.join(REPO, "src/data/tilesets/headers.h"),
    }
    textos = {k: open(p, encoding="utf-8").read() for k, p in caminhos.items()}
    add = {k: "" for k in caminhos}
    for rotulo, rel, is_sec in alvos:
        if "gTilesetTiles_%s[]" % rotulo not in textos["graphics"]:
            add["graphics"] += '\nconst u32 gTilesetTiles_%s[] = INCGFX_U32("%s/tiles.png", ".4bpp.smol");\n' % (rotulo, rel)
            # ALIGNED(4) não é enfeite: `LoadTilesetPalette` copia a paleta com
            # CpuFastCopy/LoadPaletteFast, que exigem alinhamento de 4 bytes, e
            # todo `gTilesetPalettes_*` do repositório tem isso. Sem ele o
            # alinhamento fica por sorte do linker.
            add["graphics"] += "\nconst u16 ALIGNED(4) gTilesetPalettes_%s[][16] =\n{\n" % rotulo
            for i in range(16):
                add["graphics"] += '    INCGFX_U16("%s/palettes/%02d.pal", ".gbapal"),\n' % (rel, i)
            add["graphics"] += "};\n"
        if "gMetatiles_%s[]" % rotulo not in textos["metatiles"]:
            add["metatiles"] += 'const u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin");\n' % (rotulo, rel)
            add["metatiles"] += 'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % (rotulo, rel)
        if "gTileset_%s =" % rotulo not in textos["headers"]:
            add["headers"] += ("\nconst struct Tileset gTileset_%s =\n{\n"
                               "    .isCompressed = TRUE,\n    .isSecondary = %s,\n"
                               "    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n"
                               "    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n"
                               "    .callback = NULL,\n};\n") % (rotulo, "TRUE" if is_sec else "FALSE",
                                                                 rotulo, rotulo, rotulo, rotulo)
    for k, bloco in add.items():
        if bloco:
            with open(caminhos[k], "a", encoding="utf-8") as f:
                f.write(bloco)

    caminho_layouts = os.path.join(REPO, "data/layouts/layouts.json")
    with open(caminho_layouts, encoding="utf-8") as f:
        doc = json.load(f)
    mp = plano["mapa"]
    for L in doc["layouts"]:
        if L["id"] == copia.lay_nosso["id"]:
            L["width"], L["height"] = mp["w"], mp["h"]
            L["primary_tileset"] = "gTileset_" + rot_pri
            L["secondary_tileset"] = "gTileset_" + rot_sec
    with open(caminho_layouts, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")

    for nome in ("map.bin", "border.bin"):
        chave = "blockdata_filepath" if nome == "map.bin" else "border_filepath"
        shutil.copyfile(os.path.join(destino, nome), os.path.join(REPO, copia.lay_nosso[chave]))
    return rot_pri, rot_sec


def imprime(m):
    print("== %s %s -> %s" % (m["hack"], m["mapa_hack"], m["nosso"]))
    print("   ROM %s | split %d/%d/%d (%.2f%% preto)" % (
        m["rom"], m["split_hack"]["metatiles"], m["split_hack"]["tiles"],
        m["split_hack"]["paletas"], m["split_hack"]["frac_preto"] * 100))
    print("   tamanho: hack %dx%d | nosso %dx%d | borda %dx%d" % (
        m["tamanho_hack"][0], m["tamanho_hack"][1], m["tamanho_nosso"][0], m["tamanho_nosso"][1],
        m["border_hack"][0], m["border_hack"][1]))
    c = m["costura"]
    print("   costura: %d índices de primário e %d de secundário pinados" % (
        c["pinados_primario"], c["pinados_secundario"]))
    for x in c["conexoes"]:
        if "situacao" in x:
            print("     %-6s %-24s %s" % (x.get("direcao"), x.get("mapa"), x["situacao"]))
        else:
            print("     %-6s %-22s %-24s %-26s faixa %3d, pinados %3d" % (
                x["direcao"], x["mapa"], x["primario"].replace("gTileset_", ""),
                x["secundario"].replace("gTileset_", ""),
                x["indices_da_faixa"], x["indices_pinados"]))
    for cf in c.get("conflitos", [])[:10]:
        print("     CONFLITO no índice %d: fica com %s; %s pediu outra arte"
              % (cf["indice"], cf["fica_com"][0].replace("gTileset_", ""), cf["perdeu"][0]))
    if len(c.get("conflitos", [])) > 10:
        print("     ... e mais %d conflitos de costura" % (len(c["conflitos"]) - 10))
    p, mt = m["paletas"], m["metatiles"]
    print("   paleta:   %2d origens, %3d cores distintas -> %2d grupos de %2d vagas  %s" % (
        p["origens"], p["cores_distintas"], p["grupos"], p["vagas"], "CABE" if p["cabe"] else "NÃO CABE"))
    print("   metatile: %4d de %4d vagas  %s" % (mt["precisa"], mt["vagas"], "CABE" if mt["cabe"] else "NÃO CABE"))
    if "tiles" in m:
        t = m["tiles"]
        print("   tile:     %4d de %4d vagas  %s" % (t["precisa"], t["vagas"], "CABE" if t["cabe"] else "NÃO CABE"))
    qv = m.get("quadrantes_vazios")
    if qv and qv["n"]:
        print("   AVISO: %d quadrantes do hack apontam para tile que NÃO existe no "
              "tileset dele; viraram tile transparente (o autor também vê nada ali): %s"
              % (qv["n"], qv["onde"][:6]))
    print("   VEREDITO: %s" % m.get("veredito", "?"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--hack")
    ap.add_argument("--mapa")
    ap.add_argument("--nosso")
    ap.add_argument("--saida")
    ap.add_argument("--medir", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--costura", help="direções de conexão a PINAR (ex.: down,up). "
                                      "O que fica de fora é porque a faixa dele nunca entra na câmera "
                                      "de dentro da cidade, e isso tem de estar medido no relatório.")
    a = ap.parse_args()
    if a.demo:
        sys.exit(demo())
    for k in ("hack", "mapa", "nosso", "saida"):
        if not getattr(a, k):
            raise SystemExit("ERRO: falta --%s" % k)
    os.makedirs(a.saida, exist_ok=True)
    c = Copia(a)
    medida, plano = c.monta(a.saida, so_medir=a.medir)
    imprime(medida)
    with open(os.path.join(a.saida, "medida.json"), "w", encoding="utf-8") as f:
        json.dump(medida, f, indent=1, ensure_ascii=False)
    if plano is None:
        return 1
    if a.medir:
        return 0
    escreve_saida(c, plano, a.saida)
    res, img_hack, img_copia = prova(c, plano, a.saida)
    print("   prova A, extração fiel à ROM:  %d pixels diferentes" % res["extracao_fiel"]["pixels_diferentes"])
    print("   prova B, cópia fiel ao hack:   %d pixels diferentes" % res["copia_fiel"]["pixels_diferentes"])
    print("   prova C, costura intacta:      %d de %d índices pinados ruins" % (
        res["costura_fiel"]["n_ruins"], res["costura_fiel"]["pinados"]))
    print("   prova D, colisão do autor:     %d células diferentes" % res["colisao_intacta"]["celulas_diferentes"])
    jogo = relatorio_de_jogo(c, plano, a.saida)
    fora = {k: "%d de %d fora" % (sum(1 for x in v if not x["dentro"]), len(v))
            for k, v in jogo.items() if k in ("warps", "objetos", "placas", "gatilhos")}
    print("   camada de jogo: %s fora do mapa novo" % fora)
    with open(os.path.join(a.saida, "prova.json"), "w", encoding="utf-8") as f:
        json.dump({"prova": res, "jogo": jogo}, f, indent=1, ensure_ascii=False)
    img_hack.save(os.path.join(a.saida, "hack.png"))
    img_copia.save(os.path.join(a.saida, "copia.png"))
    if not res["passou"]:
        print("   REPROVOU: a cópia não é fiel. Nada disso pode entrar no repo.")
        return 1
    print("   PROVA COMPLETA: a cópia é byte a byte o desenho do autor.")
    print("   prancha: %s" % prancha(c, a.saida, img_hack, img_copia))
    if a.aplicar:
        rp, rs = aplica(c, plano, a.saida)
        print("   APLICADO no repo: gTileset_%s + gTileset_%s, layout %s agora %dx%d" % (
            rp, rs, c.lay_nosso["id"], plano["mapa"]["w"], plano["mapa"]["h"]))
    return 0


def demo():
    """Provas da ferramenta, com as NEGATIVAS junto.

    Prova positiva sozinha não vale: um comparador que devolve sempre 'igual'
    passa em todas elas. Por isso cada prova aqui tem o par que TEM de falhar.
    """
    falhas = []

    def checa(cond, msg):
        print("   %-68s %s" % (msg, "OK" if cond else "FALHOU"))
        if not cond:
            falhas.append(msg)

    print("1. empacotador de paleta: só funde cor IDÊNTICA")
    a = {("x", 0): {(i, 0, 0) for i in range(12)}}
    a[("x", 1)] = {(i, 0, 0) for i in range(12)}          # mesmas 12 cores
    g = empacota_paletas(a)
    checa(len(g) == 1, "duas paletas com as MESMAS 12 cores viram 1 grupo")
    b = {("y", 0): {(i, 0, 0) for i in range(12)},
         ("y", 1): {(0, i, 0) for i in range(12)}}         # 24 cores distintas
    g = empacota_paletas(b)
    checa(len(g) == 2, "NEGATIVA: 24 cores distintas NÃO cabem em um grupo de 15")
    c = {("z", i): {(i, i, i)} for i in range(20)}
    g = empacota_paletas(c, vagas=13)
    checa(len(g) == 2, "20 cores de 1 cor cada empacotam em 2 grupos de 15")

    print("2. orientações: os bits de flip compõem certo")
    grade = tuple(tuple((x + y * 8) & 0xF for x in range(8)) for y in range(8))
    quatro = orientacoes(grade)
    checa(len({g for g, _, _ in quatro}) == 4, "as quatro orientações são distintas")
    checa(quatro[0][0] == grade and quatro[0][1] is False and quatro[0][2] is False,
          "a primeira orientação é a identidade, sem flip")
    checa(flip_h(flip_h(grade)) == grade and flip_v(flip_v(grade)) == grade,
          "flip aplicado duas vezes volta ao original")

    print("3. comparador de imagem: acusa UM pixel")
    i1 = Image.new("RGB", (16, 16), (10, 20, 30))
    i2 = i1.copy()
    checa(difere(i1, i2) == (0, None), "duas imagens iguais dão 0 diferença")
    i2.load()[7, 9] = (10, 20, 31)
    n, onde = difere(i1, i2)
    checa(n == 1 and onde == (7, 9), "NEGATIVA: um pixel trocado é acusado, com a posição")
    checa(difere(i1, Image.new("RGB", (16, 17)))[0] == -1, "NEGATIVA: tamanho diferente reprova")

    print("4. máscaras do map.bin (include/fieldmap.h)")
    checa(MAPGRID_METATILE_ID_MASK == 0x03FF and MAPGRID_RESTO_MASK == 0xFC00,
          "índice de metatile são os 10 bits baixos; colisão e elevação, os 6 altos")
    v = 0x1234
    novo = (0x2AB & MAPGRID_METATILE_ID_MASK) | (v & MAPGRID_RESTO_MASK)
    checa((novo & MAPGRID_RESTO_MASK) == (v & MAPGRID_RESTO_MASK) and (novo & 0x3FF) == 0x2AB,
          "trocar o índice preserva colisão e elevação do autor do hack")

    print("5. split do nosso layout 'johto' (include/fieldmap.h + src/fieldmap.c)")
    checa((N_META_PRI, N_TILES_PRI, N_PAL_PRI) == (640, 640, 7),
          "bigPrimary: 640 metatiles, 640 tiles, 7 paletas no primário")
    checa(N_META_SEC == 384 and N_TILES_SEC == 384 and N_PAL_TOTAL == 13,
          "sobram 384 metatiles, 384 tiles e 6 vagas de paleta para o secundário")

    print("6. atributo de metatile: 4 bytes do FireRed viram 2 do Emerald")
    saida, perdas = ext.attr_frlg_para_emerald(struct.pack("<I", 0x12 | (2 << 29)))
    got = struct.unpack("<H", saida)[0]
    checa((got & 0xFF) == 0x12 and (got >> 12) == 2 and not perdas,
          "behavior nos bits 0-7 e layerType nos 12-15")
    _s, perdas2 = ext.attr_frlg_para_emerald(struct.pack("<I", 0x1A0))
    checa(len(perdas2) == 1, "NEGATIVA: behavior >= 256 não cabe em 8 bits e é DENUNCIADO")

    print("\n%s" % ("demo PASSOU" if not falhas else "demo REPROVOU: " + "; ".join(falhas)))
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
