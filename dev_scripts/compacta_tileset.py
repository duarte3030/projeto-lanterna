#!/usr/bin/env python3
"""Devolve as vagas de TILE que um tileset secundário gasta com tile morto.

O que trava o REFINO (o PRD-REFINO, seções 2.1 e 3.3) não é desenho, é vaga. A
operação que o `porto_canalave.py` provou, importar peça de arte pronta para
dentro do secundário de uma cidade sem desenhar um pixel, só repete nas outras
cidades se houver espaço de tile lá dentro. E vários secundários estão no teto:
512 tiles no layout `emerald`, 384 no `johto` e no `frlg` (1024 menos o primário
de 512 ou de 640, ver `GetNumTilesInPrimary` em `src/fieldmap.c`).

O achado que este script explora: a maior parte do que está no teto é TILE
MORTO. Tile que veio junto no import da folha de arte e que nenhum metatile
daquele tileset referencia. Medido em 06/09/2026 nesta árvore, contando tile do
próprio secundário que não aparece em nenhuma das 8 entradas de nenhum metatile
do `metatiles.bin` dele:

    gTileset_Canalave        512 tiles, 342 mortos, teto 512
    gTileset_CianwoodCity    384 tiles, 290 mortos, teto 384
    gTileset_Snowpoint       448 tiles, 232 mortos, teto 512
    gTileset_Blackthorn      272 tiles, 197 mortos, teto 384

O QUE ELE FAZ. Reescreve o `tiles.png` guardando só os tiles vivos, na mesma
ordem relativa, e reescreve o `metatiles.bin` remapeando o índice de tile das 8
entradas de cada metatile. Os flips (bits 10 e 11) e a paleta (bits 12 a 15) de
cada entrada ficam byte a byte iguais, porque a máscara aplicada é `& 0xFC00`. O
`metatile_attributes.bin` não é tocado. Nenhum `map.bin` é tocado, porque o
índice de METATILE não muda: o que muda é só o índice de TILE dentro do
metatile. Por isso colisão, elevação, warp, objeto e alcance de gatilho ficam
idênticos, e a regra 4 da seção 4 do PRD é cumprida por construção, não por
cuidado.

TRÊS CUIDADOS QUE CUSTARIAM A RODADA:

1. TILE 0 É ESPECIAL. Em quase todo tileset ele é o tile vazio, e a cor de
   índice 0 é a transparência do desenho. Ele fica, na vaga 0, mesmo quando
   nenhum metatile o referencia. Na prática ele quase nunca é referenciado: a
   entrada "vazia" de metatile vale 0x0000, que aponta para o tile 0 do
   PRIMÁRIO, não para o do secundário. Se ele fosse removido junto com os
   mortos, todo tile do secundário andaria uma vaga para trás.

2. TILE DO PRIMÁRIO NÃO É NOSSO. Metatile de secundário referencia à vontade
   tile do primário (índice abaixo de 512 no `emerald`, de 640 no `johto` e no
   `frlg`). Esses índices passam intactos e não entram na conta.

3. O PRIMÁRIO TAMBÉM REFERENCIA TILE DO SECUNDÁRIO, e isso é real nesta árvore,
   não hipótese. Medido: `gTileset_JohtoBuilding` (241 tiles), o
   `gTileset_JohtoNorthWest` (41), o `gTileset_Galar11` (27) e o
   `gTileset_JohtoNorthEast` (2, o metatile 588, que pede os tiles 812 e 813)
   têm metatiles que apontam para o espaço do secundário. O primário é
   COMPARTILHADO por muitos secundários, então o índice dele não pode ser
   remapeado. Este script trata esses tiles como PINOS: eles ficam na vaga
   exata em que estavam, e a compactação escorrega os outros por cima das vagas
   livres. O pino só é cravado quando o metatile do primário é ALCANÇÁVEL, ou
   seja, quando ele aparece em algum `map.bin` de um layout que casa esse
   primário com esse secundário; quando não é alcançável o script diz isso na
   tela e não paga o preço da vaga. `--fixar-orfaos` crava mesmo assim.

A LARGURA continua 128 px, 16 tiles por linha, e a última linha é completada com
tile em branco (todos os pixels no índice 0), porque o formato exige linha
cheia.

BACKUP e `--desfazer`: os arquivos originais são copiados para
`build/compacta_tileset/<pasta>/` antes de qualquer escrita. `build/` está no
`.gitignore`, então o backup não suja a árvore; em compensação um `make clean`
leva o backup junto, e aí o caminho de volta é o git.

Uso:
    python3 dev_scripts/compacta_tileset.py                      # censo de todos os secundários
    python3 dev_scripts/compacta_tileset.py gTileset_Snowpoint   # mede um, sem escrever
    python3 dev_scripts/compacta_tileset.py gTileset_Snowpoint --aplicar
    python3 dev_scripts/compacta_tileset.py gTileset_Snowpoint --desfazer
    python3 dev_scripts/compacta_tileset.py --demo               # autoteste de unidade
    python3 dev_scripts/compacta_tileset.py --autoteste          # prova na árvore de verdade
"""
import os
import re
import shutil
import struct
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
os.environ.setdefault("REPO_MAPAS", RAIZ)
import render_maps as R      # noqa: E402
import pinos_anim as PA      # noqa: E402

BACKUP = os.path.join(RAIZ, "build", "compacta_tileset")
TILE_PX = 8
COLUNAS = 16                 # 128 px de largura, o formato do repo
ALVOS_PADRAO = ("gTileset_Snowpoint", "gTileset_Canalave",
                "gTileset_Blackthorn", "gTileset_CianwoodCity")


# ------------------------------------------------------------------- leitura
def tiles_do_png(caminho):
    """Devolve (lista de tiles 8x8 de índices de cor, paleta achatada, info)."""
    img = Image.open(caminho)
    if img.mode != "P":
        raise SystemExit(f"{caminho} nao e PNG indexado (mode={img.mode})")
    largura, altura = img.size
    if largura % TILE_PX or altura % TILE_PX:
        raise SystemExit(f"{caminho}: {largura}x{altura} nao e multiplo de 8")
    px = img.load()
    cols = largura // TILE_PX
    tiles = []
    for i in range((largura // TILE_PX) * (altura // TILE_PX)):
        x0 = (i % cols) * TILE_PX
        y0 = (i // cols) * TILE_PX
        tiles.append(tuple(tuple(px[x0 + x, y0 + y] for x in range(TILE_PX))
                           for y in range(TILE_PX)))
    return tiles, img.getpalette(), dict(img.info), cols


def grava_png(caminho, tiles, paleta, info, cols=COLUNAS):
    """Escreve a tira de tiles de volta, indexada, com a mesma paleta."""
    linhas = (len(tiles) + cols - 1) // cols
    largura, altura = cols * TILE_PX, linhas * TILE_PX
    img = Image.new("P", (largura, altura), 0)
    img.putpalette(paleta)
    px = img.load()
    for i, tile in enumerate(tiles):
        x0 = (i % cols) * TILE_PX
        y0 = (i // cols) * TILE_PX
        for y in range(TILE_PX):
            for x in range(TILE_PX):
                px[x0 + x, y0 + y] = tile[y][x]
    extra = {}
    if "transparency" in info:
        extra["transparency"] = info["transparency"]
    img.save(caminho, **extra)


def entradas(bin_meta):
    """Todas as palavras de 16 bits do metatiles.bin, em ordem."""
    return [struct.unpack_from("<H", bin_meta, i)[0] for i in range(0, len(bin_meta), 2)]


# ------------------------------------------------------------------ contexto
def _layouts_por_secundario():
    fora = {}
    for layout in R.carregar_layouts().values():
        fora.setdefault(layout["secondary_tileset"], []).append(layout)
    return fora


def base_do_layout(layout):
    """NUM_TILES_IN_PRIMARY do layout: 640 no johto/frlg, 512 no emerald."""
    versao = layout.get("layout_version") or "emerald"
    return 640 if versao in ("johto", "frlg") else 512


def contexto(rotulo, todos=None):
    """Pasta, base de índice e layouts que usam o tileset como secundário."""
    todos = todos if todos is not None else _layouts_por_secundario()
    layouts = todos.get(rotulo, [])
    if not layouts:
        raise SystemExit(f"{rotulo} nao e secundario de nenhum layout")
    bases = {base_do_layout(l) for l in layouts}
    if len(bases) > 1:
        raise SystemExit(
            f"{rotulo} e usado com layout_version misturado (bases {sorted(bases)}); "
            "o mesmo indice de tile significaria coisas diferentes por mapa")
    return R.caminho_tileset(rotulo), bases.pop(), layouts


def pinos_do_primario(rotulo, pasta_sec, base, layouts, fixar_orfaos=False):
    """Tiles do secundário que algum metatile do PRIMÁRIO referencia.

    Devolve (pinos_cravados, avisos). O pino só é cravado quando o metatile do
    primário aparece em algum `map.bin` que casa esse primário com esse
    secundário, ou quando `fixar_orfaos` manda cravar de qualquer jeito.
    """
    pinos, avisos = set(), []
    primarios = {}
    for layout in layouts:
        primarios.setdefault(layout["primary_tileset"], []).append(layout)
    for rotulo_pri, usos in sorted(primarios.items()):
        pasta_pri = R.caminho_tileset(rotulo_pri)
        meta_pri = open(os.path.join(pasta_pri, "metatiles.bin"), "rb").read()
        palavras = entradas(meta_pri)
        suspeitos = {}
        for m in range(len(palavras) // 8):
            locais = {(palavras[m * 8 + i] & 0x3FF) - base
                      for i in range(8) if (palavras[m * 8 + i] & 0x3FF) >= base}
            if locais:
                suspeitos[m] = locais
        if not suspeitos:
            continue
        usados = set()
        for layout in usos:
            dados = open(os.path.join(RAIZ, layout["blockdata_filepath"]), "rb").read()
            usados |= {struct.unpack_from("<H", dados, i)[0] & 0x3FF
                       for i in range(0, len(dados), 2)}
        for m, locais in sorted(suspeitos.items()):
            alcancavel = m in usados
            if alcancavel or fixar_orfaos:
                pinos |= locais
                avisos.append(f"pino: {rotulo_pri} metatile {m} pede os tiles locais "
                              f"{sorted(locais)} do secundario"
                              + ("" if alcancavel else " (orfao, cravado a pedido)"))
            else:
                avisos.append(f"orfao NAO cravado: {rotulo_pri} metatile {m} pede os tiles "
                              f"locais {sorted(locais)}, mas nenhum map.bin desses layouts "
                              f"usa o metatile {m}")
    return pinos, avisos


# --------------------------------------------------------------------- plano
def monta_plano(rotulo, fixar_orfaos=False, todos=None):
    """Mede o tileset e devolve o plano de compactação, sem escrever nada."""
    pasta, base, layouts = contexto(rotulo, todos)
    tiles, paleta, info, cols = tiles_do_png(os.path.join(pasta, "tiles.png"))
    meta = open(os.path.join(pasta, "metatiles.bin"), "rb").read()
    palavras = entradas(meta)

    pinos, avisos = pinos_do_primario(rotulo, pasta, base, layouts, fixar_orfaos)

    vivos = set()
    for palavra in palavras:
        idx = palavra & 0x3FF
        if idx >= base:
            vivos.add(idx - base)
    # METATILE QUEBRADO, e ele existe de verdade nesta arvore. O
    # `gTileset_PetalburgSinnoh` tem 65 metatiles que pedem tile local acima do
    # tamanho do `tiles.png` (o import original trouxe metatile a mais e tile a
    # menos). Recusar o tileset inteiro por causa deles custava a compactacao de
    # um secundario usado por 62 layouts. A saida so vale se eles forem
    # PROVADAMENTE mortos: se nenhum `map.bin` de nenhum layout desenha aquele
    # metatile, as 8 entradas dele saem do remapeamento e ficam byte a byte
    # iguais, exatamente como ja estao. Se UM deles for desenhado, a recusa
    # continua, porque aí o tileset esta quebrado em jogo e nao e assunto desta
    # ferramenta.
    fora = sorted(t for t in vivos if t >= len(tiles))
    congelados = set()
    if fora:
        quebrados = set()
        for m in range(len(palavras) // 8):
            for i in range(8):
                idx = palavras[m * 8 + i] & 0x3FF
                if idx >= base and idx - base >= len(tiles):
                    quebrados.add(m)
                    break
        desenhados, sem_arquivo = set(), []
        for layout in layouts:
            caminho = os.path.join(RAIZ, layout["blockdata_filepath"])
            if not os.path.exists(caminho):
                # Layout declarado no layouts.json cujo map.bin nao existe em
                # disco. Sao os tumulos das remocoes do cartucho 1; sem arquivo
                # nao ha celula desenhada, entao nao entram na conta, mas ficam
                # listados para ninguem achar que foram esquecidos.
                sem_arquivo.append(layout["name"])
                continue
            dados = open(caminho, "rb").read()
            desenhados |= {struct.unpack_from("<H", dados, i)[0] & 0x3FF
                           for i in range(0, len(dados), 2)}
        if sem_arquivo:
            avisos.append("sem map.bin em disco, fora da conta de desenhado: %d layouts (%s%s)"
                          % (len(sem_arquivo), ", ".join(sem_arquivo[:4]),
                             ", ..." if len(sem_arquivo) > 4 else ""))
        # O indice de um metatile do SECUNDARIO no map.bin e `base + local`.
        # Comparar tambem com o local cru era o erro obvio desta conta: o local
        # 226 tambem existe como metatile do PRIMARIO, e todo mapa desenha
        # algum, entao a checagem acusava todos os 65 como vivos.
        vivos_quebrados = sorted(m for m in quebrados if (base + m) in desenhados)
        if vivos_quebrados:
            raise SystemExit(
                f"{rotulo}: metatile pede tile local {fora[:5]} e o tiles.png so "
                f"tem {len(tiles)}, e os metatiles {vivos_quebrados[:5]} sao "
                f"DESENHADOS por algum map.bin")
        congelados = quebrados
        avisos.append(f"metatile quebrado congelado: {len(quebrados)} metatiles pedem "
                      f"tile local acima de {len(tiles) - 1} e nenhum map.bin os "
                      f"desenha; as entradas deles ficam byte a byte iguais")
        vivos = set()
        for m in range(len(palavras) // 8):
            if m in congelados:
                continue
            for i in range(8):
                idx = palavras[m * 8 + i] & 0x3FF
                if idx >= base:
                    vivos.add(idx - base)

    # Pino de ANIMAÇÃO. O `src/tileset_anims.c` escreve tile cru direto na VRAM
    # numa vaga fixa e não sabe que a numeração mudou; renumerar por baixo dele
    # não quebra o build nem muda um pixel do render estático, e só aparece
    # dentro do jogo. Ver `dev_scripts/pinos_anim.py`.
    vagas_anim, anim_ativa, explicacao_anim = PA.pinos_de_anim(rotulo)
    if anim_ativa:
        pinos |= vagas_anim
        avisos.append("pino de animacao: %s (%s)"
                      % (PA.faixas(vagas_anim), explicacao_anim))

    pinos = {p for p in pinos if p < len(tiles)}
    manter = vivos | pinos | {0}      # o tile 0 nunca sai e nunca sai do lugar
    pinos |= {0}

    tamanho = max(len(manter), (max(pinos) + 1) if pinos else 0)
    ordem = [None] * tamanho
    for p in sorted(pinos):
        ordem[p] = p
    livres = (i for i in range(tamanho) if ordem[i] is None)
    for velho in sorted(manter - pinos):
        ordem[next(livres)] = velho

    de_para = {}
    for novo, velho in enumerate(ordem):
        if velho is not None:
            de_para[velho] = novo

    return dict(rotulo=rotulo, pasta=pasta, base=base, teto=1024 - base,
                layouts=[l["id"] for l in layouts], tiles=tiles, paleta=paleta,
                info=info, colunas=cols, meta=meta, vivos=vivos, pinos=pinos,
                congelados=congelados,
                manter=manter, ordem=ordem, de_para=de_para, avisos=avisos,
                mortos=len(tiles) - len(manter), antes=len(tiles),
                depois=tamanho)


def aplica_plano(plano):
    """Gera (tiles novos, metatiles.bin novo) a partir do plano."""
    branco = tuple(tuple(0 for _ in range(TILE_PX)) for _ in range(TILE_PX))
    novos = [plano["tiles"][v] if v is not None else branco for v in plano["ordem"]]
    resto = (-len(novos)) % COLUNAS
    novos += [branco] * resto

    base, de_para = plano["base"], plano["de_para"]
    saida = bytearray(plano["meta"])
    congelados = plano.get("congelados") or set()
    for i in range(0, len(saida), 2):
        if (i // 16) in congelados:
            continue                      # metatile quebrado e morto: byte igual
        palavra = struct.unpack_from("<H", saida, i)[0]
        idx = palavra & 0x3FF
        if idx < base:
            continue                      # tile do primário: não é nosso
        # a máscara guarda os flips (bits 10 e 11) e a paleta (bits 12 a 15)
        nova = (palavra & 0xFC00) | (base + de_para[idx - base])
        struct.pack_into("<H", saida, i, nova)
    return novos, bytes(saida)


GRAFICOS = os.path.join(RAIZ, "src", "data", "tilesets", "graphics.h")


def _linha_num_tiles(rotulo, texto=None):
    """(o texto do graphics.h, a linha do INCGFX deste tileset, o número declarado).

    Devolve (texto, None, None) quando o tileset não declara `-num_tiles`.
    """
    texto = texto if texto is not None else open(GRAFICOS, encoding="utf-8").read()
    nome = rotulo.replace("gTileset_", "gTilesetTiles_")
    padrao = re.compile(
        r'^(const u32 %s\[\] = INCGFX_U32\([^\n]*?"-num_tiles )(\d+)( -Wnum_tiles"\);)$'
        % re.escape(nome), re.M)
    m = padrao.search(texto)
    if not m:
        return texto, None, None
    return texto, m, int(m.group(2))


def ajusta_num_tiles(rotulo, total):
    """Reescreve `-num_tiles` do tileset no `src/data/tilesets/graphics.h`.

    POR QUE ISTO EXISTE, e o defeito que ele fecha. 66 dos tilesets desta árvore
    declaram `-num_tiles N -Wnum_tiles` na linha do `INCGFX_U32`, e o `-Wnum_tiles`
    manda o compilador de gráficos RECUSAR o build quando o `tiles.png` tem mais
    tiles do que o declarado, e avisar quando tem menos. Compactar um tileset
    ENCOLHE o `tiles.png`, e até 09/09/2026 este script não mexia no
    `graphics.h`: o Dewford foi de 512 para 208 tiles com a linha ainda dizendo
    503, e o build parou com "greater than the maximum possible value (208)".

    Nunca tinha doído porque os quatro secundários já compactados (Canalave,
    Snowpoint, Cianwood, Blackthorn) são de Sinnoh e de Johto e entraram no repo
    SEM `-num_tiles`. Toda compactação em Hoenn e em Kanto bate nisso.

    Tileset sem `-num_tiles` na linha não ganha um: acrescentar declaração onde
    não havia é decisão de quem escreveu o `graphics.h`, não deste script.
    """
    texto, m, antigo = _linha_num_tiles(rotulo)
    if m is None:
        return None
    if antigo == total:
        return antigo
    novo = texto[:m.start()] + m.group(1) + str(total) + m.group(3) + texto[m.end():]
    with open(GRAFICOS, "w", encoding="utf-8") as f:
        f.write(novo)
    return antigo


# ------------------------------------------------------------------- escrita
def _pasta_backup(plano):
    return os.path.join(BACKUP, os.path.basename(plano["pasta"]))


def escreve(plano):
    novos, meta = aplica_plano(plano)
    destino = _pasta_backup(plano)
    os.makedirs(destino, exist_ok=True)
    for nome in ("tiles.png", "metatiles.bin"):
        guardado = os.path.join(destino, nome)
        if not os.path.exists(guardado):
            shutil.copy2(os.path.join(plano["pasta"], nome), guardado)
    guardado_h = os.path.join(destino, "graphics.h")
    if not os.path.exists(guardado_h) and os.path.exists(GRAFICOS):
        shutil.copy2(GRAFICOS, guardado_h)
    grava_png(os.path.join(plano["pasta"], "tiles.png"), novos,
              plano["paleta"], plano["info"])
    with open(os.path.join(plano["pasta"], "metatiles.bin"), "wb") as f:
        f.write(meta)
    rotulo = plano.get("rotulo")
    if rotulo:
        antigo = ajusta_num_tiles(rotulo, len(novos))
        if antigo is None:
            print(f"  aviso      {rotulo} nao declara -num_tiles no graphics.h; "
                  f"nada a ajustar la")
        elif antigo != len(novos):
            print(f"  graphics.h -num_tiles de {rotulo}: {antigo} -> {len(novos)}")
    return len(novos)


def desfaz(rotulo):
    pasta = R.caminho_tileset(rotulo)
    guardado = os.path.join(BACKUP, os.path.basename(pasta))
    if not os.path.isdir(guardado):
        raise SystemExit(f"nao ha backup em {guardado}")
    for nome in ("tiles.png", "metatiles.bin"):
        shutil.copy2(os.path.join(guardado, nome), os.path.join(pasta, nome))
    # O `-num_tiles` volta junto, senao o desfazer deixa o graphics.h dizendo o
    # numero do tileset compactado e o build recusa o tileset original. O numero
    # vem do graphics.h GUARDADO, e nao da contagem de tiles do png devolvido:
    # a declaracao original pode ser MENOR que o png (o Fortree declarava 493
    # para um png de 496, porque a ultima linha do png e enchimento), e
    # recontar trocaria a declaracao do repo por outra, calada.
    guardado_h = os.path.join(guardado, "graphics.h")
    if os.path.exists(guardado_h):
        with open(guardado_h, encoding="utf-8") as f:
            _, m, original = _linha_num_tiles(rotulo, f.read())
        if original is not None:
            antigo = ajusta_num_tiles(rotulo, original)
            if antigo is not None and antigo != original:
                print(f"{rotulo}: graphics.h -num_tiles {antigo} -> {original}")
    print(f"{rotulo}: devolvido de {guardado}")
    return 0


# ---------------------------------------------------------------- conferência
def confere(plano, novos, meta_novo):
    """Prova de equivalência: cada entrada de metatile desenha o mesmo tile.

    Compara entrada por entrada o par (pixels do tile 8x8, flips, paleta) antes
    e depois. Tile do primário entra na conta como o próprio índice, porque o
    primário não é tocado.
    """
    velhas, novas = entradas(plano["meta"]), entradas(meta_novo)
    if len(velhas) != len(novas):
        return [f"{plano['rotulo']}: o metatiles.bin mudou de tamanho"]
    base, tiles = plano["base"], plano["tiles"]
    congelados = plano.get("congelados") or set()
    erros = []
    for i, (a, b) in enumerate(zip(velhas, novas)):
        if (i // 8) in congelados:
            # Metatile quebrado e morto: a exigencia dele nao e "desenha o mesmo
            # tile", que e impossivel porque o tile nunca existiu, e sim
            # "continua byte a byte igual".
            if a != b:
                erros.append(f"entrada {i}: metatile congelado mudou "
                             f"({a:04X} -> {b:04X})")
            continue
        if (a & 0xFC00) != (b & 0xFC00):
            erros.append(f"entrada {i}: flips/paleta mudaram ({a:04X} -> {b:04X})")
            continue
        ia, ib = a & 0x3FF, b & 0x3FF
        if ia < base or ib < base:
            if ia != ib:
                erros.append(f"entrada {i}: tile do primario mudou ({ia} -> {ib})")
            continue
        pa, pb = tiles[ia - base], novos[ib - base]
        if pa != pb:
            erros.append(f"entrada {i}: o tile {ia} virou {ib} e o desenho mudou")
    return erros


# -------------------------------------------------------------------- relato
def relata(plano):
    print(f"{plano['rotulo']}")
    print(f"  pasta      {os.path.relpath(plano['pasta'], RAIZ)}")
    print(f"  base       {plano['base']} (teto de {plano['teto']} tiles no secundario)")
    print(f"  layouts    {len(plano['layouts'])}: {', '.join(plano['layouts'][:6])}"
          + (" ..." if len(plano["layouts"]) > 6 else ""))
    print(f"  tiles      {plano['antes']} -> {plano['depois']}"
          f"  (vivos {len(plano['vivos'])}, pinos {sorted(plano['pinos'] - {0})}, "
          f"mortos {plano['mortos']})")
    livre_antes = plano["teto"] - plano["antes"]
    livre_depois = plano["teto"] - ((plano["depois"] + COLUNAS - 1) // COLUNAS * COLUNAS)
    print(f"  vagas      {livre_antes} livres antes, {livre_depois} depois "
          f"(+{livre_depois - livre_antes})")
    for aviso in plano["avisos"]:
        print(f"  aviso      {aviso}")


def censo():
    todos = _layouts_por_secundario()
    linhas = []
    for rotulo in sorted(todos):
        try:
            plano = monta_plano(rotulo, todos=todos)
        except SystemExit as e:
            linhas.append((rotulo, None, None, None, str(e)))
            continue
        linhas.append((rotulo, plano["antes"], plano["mortos"], plano["teto"], ""))
    linhas.sort(key=lambda l: -(l[2] or 0))
    print(f"{'secundario':34}{'tiles':>7}{'mortos':>8}{'teto':>7}")
    for rotulo, antes, mortos, teto, erro in linhas:
        if erro:
            print(f"{rotulo:34}{'':>7}{'':>8}{'':>7}  {erro}")
        elif mortos:
            print(f"{rotulo:34}{antes:>7}{mortos:>8}{teto:>7}")
    return 0


# ------------------------------------------------------------------ autoteste
def demo():
    """Os erros que a primeira versão cometeria, cada um com o seu caso."""
    branco = tuple(tuple(0 for _ in range(8)) for _ in range(8))

    # 1. A máscara. Trocar o índice de tile não pode encostar em flip nem em
    #    paleta. 0xB9FF = paleta 11, flip H e V, tile 0x1FF.
    base = 512
    de_para = {0x1FF - base: 7}
    a = 0xBDFF
    b = (a & 0xFC00) | (base + de_para[(a & 0x3FF) - base])
    assert (b >> 12) == 0xB, hex(b)
    assert (b & 0x0C00) == (a & 0x0C00), (hex(a), hex(b))
    assert (b & 0x3FF) == base + 7, hex(b)

    # 2. Entrada vazia (0x0000) aponta para o tile 0 do PRIMÁRIO, não para o do
    #    secundário. Se ela fosse contada como referência, o tile 0 do
    #    secundário pareceria vivo e a conta de mortos mentiria.
    assert (0x0000 & 0x3FF) < base

    # 3. Tile 0 fica na vaga 0 mesmo sem ninguém referenciar, e os vivos
    #    escorregam preservando a ordem relativa.
    plano = dict(base=base, de_para=None, tiles=[branco] * 10,
                 meta=b"", ordem=None)
    manter, pinos = {3, 5, 9} | {0}, {0}
    ordem = [None] * len(manter)
    for p in sorted(pinos):
        ordem[p] = p
    livres = (i for i in range(len(ordem)) if ordem[i] is None)
    for velho in sorted(manter - pinos):
        ordem[next(livres)] = velho
    assert ordem == [0, 3, 5, 9], ordem

    # 4. Pino do primário: o tile 6 tem que continuar NA VAGA 6, e os outros
    #    escorregam por cima das vagas que sobraram.
    manter, pinos = {2, 4, 6, 8} | {0}, {0, 6}
    tamanho = max(len(manter), max(pinos) + 1)
    ordem = [None] * tamanho
    for p in sorted(pinos):
        ordem[p] = p
    livres = (i for i in range(tamanho) if ordem[i] is None)
    for velho in sorted(manter - pinos):
        ordem[next(livres)] = velho
    assert ordem[6] == 6, ordem
    assert ordem == [0, 2, 4, 8, None, None, 6], ordem

    # 5. A última linha é completada até fechar 16 tiles por linha.
    for n, esperado in ((1, 16), (16, 16), (17, 32), (76, 80)):
        assert n + ((-n) % COLUNAS) == esperado, (n, esperado)

    # 6. Prova negativa: um de-para errado (dois índices trocados) tem que ser
    #    ACUSADO pela conferência, não passar calado.
    t = [branco] + [tuple(tuple((i * 8 + y * 8 + x) % 16 for x in range(8))
                          for y in range(8)) for i in range(1, 5)]
    fake = dict(rotulo="fake", base=base, tiles=t,
                meta=struct.pack("<8H", *(base + i for i in (0, 1, 2, 3, 4, 1, 2, 3))))
    certo = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
    novos = [t[v] for v in range(5)]
    meta_ok = bytearray(fake["meta"])
    assert not confere(fake, novos, bytes(meta_ok)), "o caso certo nao pode acusar"
    trocado = dict(certo)
    trocado[1], trocado[2] = certo[2], certo[1]
    meta_ruim = bytearray(fake["meta"])
    for i in range(0, len(meta_ruim), 2):
        p = struct.unpack_from("<H", meta_ruim, i)[0]
        struct.pack_into("<H", meta_ruim, i,
                         (p & 0xFC00) | (base + trocado[(p & 0x3FF) - base]))
    erros = confere(fake, novos, bytes(meta_ruim))
    assert erros, "o de-para trocado passou calado, a conferencia nao serve"

    print("demo ok")
    return 0


def autoteste(rotulos=None):
    """A prova na árvore de verdade, sem escrever: pixel a pixel por entrada."""
    rotulos = rotulos or list(ALVOS_PADRAO)
    todos = _layouts_por_secundario()
    falhas = 0
    for rotulo in rotulos:
        plano = monta_plano(rotulo, todos=todos)
        novos, meta = aplica_plano(plano)
        erros = confere(plano, novos, meta)

        # prova negativa no caso de verdade: trocar dois tiles vivos de lugar
        # tem que ser acusado.
        vivos = sorted(plano["vivos"] - plano["pinos"])
        acusou = None
        if len(vivos) >= 2:
            torto = dict(plano["de_para"])
            a, b = vivos[0], vivos[1]
            torto[a], torto[b] = torto[b], torto[a]
            sujo = bytearray(plano["meta"])
            congelados = plano.get("congelados") or set()
            for i in range(0, len(sujo), 2):
                if (i // 16) in congelados:
                    continue
                p = struct.unpack_from("<H", sujo, i)[0]
                idx = p & 0x3FF
                if idx >= plano["base"]:
                    struct.pack_into("<H", sujo, i,
                                     (p & 0xFC00) | (plano["base"] + torto[idx - plano["base"]]))
            acusou = bool(confere(plano, novos, bytes(sujo)))

        estado = "OK " if (not erros and acusou is not False) else "FALHA"
        if erros or acusou is False:
            falhas += 1
        print(f"{estado} {rotulo}: {plano['antes']} -> {plano['depois']} tiles, "
              f"{len(entradas(plano['meta']))} entradas conferidas, "
              f"{len(erros)} divergencias, prova negativa "
              f"{'acusou' if acusou else 'NAO acusou' if acusou is False else 'sem par'}")
        for e in erros[:5]:
            print("      ", e)
    print(f"\n{len(rotulos) - falhas}/{len(rotulos)} tilesets conferidos.")
    return 1 if falhas else 0


# ---------------------------------------------------------------------- main
def main():
    argv = sys.argv[1:]
    if "--demo" in argv:
        return demo()
    rotulos = [a for a in argv if not a.startswith("--")]
    if "--autoteste" in argv:
        return autoteste(rotulos or None)
    if "--desfazer" in argv:
        if not rotulos:
            raise SystemExit("--desfazer precisa do nome do tileset")
        for rotulo in rotulos:
            desfaz(rotulo)
        return 0
    if not rotulos:
        return censo()

    fixar = "--fixar-orfaos" in argv
    todos = _layouts_por_secundario()
    for rotulo in rotulos:
        plano = monta_plano(rotulo, fixar_orfaos=fixar, todos=todos)
        relata(plano)
        if "--aplicar" in argv:
            novos, meta = aplica_plano(plano)
            erros = confere(plano, novos, meta)
            if erros:
                print("  RECUSADO: a conferencia acusou")
                for e in erros[:5]:
                    print("   ", e)
                return 1
            total = escreve(plano)
            print(f"  aplicado   tiles.png com {total} tiles, backup em "
                  f"{os.path.relpath(_pasta_backup(plano), RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
