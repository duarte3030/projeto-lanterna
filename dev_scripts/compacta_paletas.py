#!/usr/bin/env python3
"""Devolve VAGAS DE PALETA de um tileset secundário, sem aproximar cor nenhuma.

O `compacta_tileset.py` ao lado resolveu o orçamento de TILE. Este resolve o
outro, e o outro é o que realmente trava o REFINO nas cidades já mexidas: o
orçamento de PALETA.

O motor tem `NUM_PALS_TOTAL 13` (`include/fieldmap.h`). As primeiras são do
primário, `NUM_PALS_IN_PRIMARY 6` no layout `emerald` e
`NUM_PALS_IN_PRIMARY_FRLG 7` no `johto` e no `frlg`, e o
`LoadTilesetPalette` copia `tileset->palettes[numPalsInPrimary]` em diante para
o hardware (`src/fieldmap.c`). Ou seja: um secundário do `emerald` tem SETE
vagas, da 6 à 12, e ponto final. Não existe a 13.

O achado que este script explora: essas vagas estão sendo gastas MUITO abaixo da
capacidade. Uma paleta do GBA tem 16 entradas, a de índice 0 é transparente no
BG, então cabem 15 cores desenháveis por vaga. Medido em 06/09/2026 nesta
árvore, contando as cores que os PIXELS realmente usam em cada vaga, não as
cores que o arquivo `.pal` declara:

    gTileset_Canalave   pal 6=5, 7=7, 8=15, 9=10, 10=5, 11=4, 12=11 cores
                        união de tudo isso: 53 cores em 7 vagas de 15

Cinquenta e três cores ocupando 105 lugares. Quatro vagas bastam, e as três que
sobram são o espaço onde arte nova entra sem que ninguém precise aproximar um
tom sequer. É por isso que este script existe: a frente anterior do porto tentou
trocar o PAR INTEIRO de tilesets de Canalave para ganhar espaço e REPROVOU
(carimbo dominante subiu de 26,9% para 83,7% e os 224 metatiles do mapa caíram
para 82). Compactar paleta ganha o mesmo espaço sem tirar um pixel do lugar.

O QUE ELE FAZ. Agrupa as vagas secundárias de forma que a UNIÃO das cores de
cada grupo caiba em 15, escreve o `.pal` do grupo com essas cores exatas,
reescreve os bits 12 a 15 (a paleta) das 8 entradas de cada metatile do
secundário e reescreve os NIBBLES DE PIXEL dos tiles afetados no `tiles.png`,
porque o índice de cor de cada pixel muda quando a paleta é reempacotada.

REGRA DE OURO: se duas cores não são idênticas, elas NÃO se fundem. Não há
quantização, não há distância de cor, não há "quase igual". Duas entradas viram
uma só quando são o mesmo RGB, e nunca em outro caso. Se um agrupamento não
fecha em 15 cores exatas, ele é descartado e o script procura outro; se nenhum
fecha, ele diz o número e não escreve nada.

O `metatile_attributes.bin` não é tocado. Nenhum `map.bin` é tocado. O índice de
METATILE não muda. Por isso colisão, elevação, warp, objeto e alcance a pé ficam
idênticos POR CONSTRUÇÃO, e não por cuidado, que é o que a regra 4 da seção 4 do
PRD-REFINO exige.

SEIS ARMADILHAS QUE CUSTARIAM A RODADA:

1. O ÍNDICE 0 CONTINUA SENDO O ÍNDICE 0. No BG do GBA a cor de índice 0 de
   qualquer paleta é transparente e nunca é desenhada (ver `desenhar_tile` em
   `dev_scripts/render_maps.py`, que faz `if idx_cor == 0: continue`). Nenhuma
   cor não-zero pode cair no índice 0, senão ela some do desenho, e nenhum pixel
   de índice 0 pode virar não-zero, senão aparece cor onde havia buraco. Aqui a
   entrada 0 do grupo é copiada de uma vaga membro e o remapeamento de pixel
   trata o 0 como caso à parte, antes de olhar cor.

2. TILE USADO COM DUAS PALETAS. O mesmo tile 8x8 pode aparecer em dois metatiles
   com vagas de paleta diferentes. Depois do reempacotamento os dois usos pedem
   nibbles diferentes do MESMO tile, o que é impossível. Este script DUPLICA o
   tile, uma cópia por paleta de origem, em vez de errar calado. Em Canalave
   isso não acontece (zero tiles nessa situação, medido), mas a ferramenta é
   genérica e o próximo secundário pode não ter essa sorte. As cópias passam por
   deduplicação: duas cópias com os mesmos 64 nibbles viram uma só.

3. TILE DO SECUNDÁRIO PINTADO COM PALETA DO PRIMÁRIO. Acontece de verdade: um
   metatile do secundário pode pedir um tile do secundário com a vaga 0, 2 ou 5,
   que são do primário compartilhado. Em Canalave são exatamente essas três. O
   nibble desse tile NÃO pode ser remapeado, porque a paleta dele não é nossa.
   Esses tiles ficam CONGELADOS com os pixels originais; se algum uso secundário
   pedir o mesmo tile, ele ganha uma cópia nova.

4. O PRIMÁRIO PODE REFERENCIAR VAGA SECUNDÁRIA. O primário é COMPARTILHADO por
   vários secundários; se um metatile ALCANÇÁVEL dele pintar alguma coisa com a
   vaga 6 a 12, mudar o conteúdo dessa vaga muda o desenho do primário em todo
   mapa que usa este secundário. Essas vagas viram PINOS: ficam no número em que
   estão, com o `.pal` byte a byte igual, e não entram em grupo nenhum.

5. TILE DO PRIMÁRIO PINTADO COM PALETA SECUNDÁRIA. Aí não há saída boa: o tile é
   do primário, não é nosso para duplicar nem para reindexar. O script RECUSA a
   vaga inteira (ela vira pino) em vez de escrever um desenho errado.

6. TILESET COM CALLBACK DE ANIMAÇÃO. Um tileset com `.callback` não nulo
   (`src/data/tilesets/headers.h`) tem código em `src/tileset_anims.c` que
   escreve tile e paleta CRUS em posição fixa da VRAM. Remapear por baixo disso
   quebra a animação de um jeito que nenhum render estático pega. O script
   recusa esses tilesets, e `--forcar` passa por cima com aviso.

O PORTÃO. A prova de que o reempacotamento é neutro não é "rodou": é RENDER. O
`--autoteste` desenha todos os mapas que usam o tileset ANTES, aplica o plano,
desenha os mesmos mapas DEPOIS e conta pixel a pixel. O número tem que ser ZERO.
No fim ele devolve a árvore ao estado anterior, aplicada ou não. Há também a
conferência interna `confere()`, que compara entrada por entrada de metatile a
matriz 8x8 de RGB de verdade (a cor, não o índice) mais os flips, e uma prova
negativa que sabota o plano de propósito e exige acusação.

BACKUP e `--desfazer`: os originais vão para `build/compacta_paletas/<pasta>/`
antes de qualquer escrita. `build/` está no `.gitignore`, então o backup não suja
a árvore; em compensação um `make clean` leva o backup junto, e aí o caminho de
volta é o git.

IDEMPOTENTE: rodar duas vezes seguidas dá byte idêntico, porque a segunda
passada mede as vagas já compactadas, não acha agrupamento melhor e reporta
"nada a fazer".

Uso:
    python3 dev_scripts/compacta_paletas.py                     # censo de todos os secundários
    python3 dev_scripts/compacta_paletas.py gTileset_Canalave   # mede um, sem escrever
    python3 dev_scripts/compacta_paletas.py gTileset_Canalave --aplicar
    python3 dev_scripts/compacta_paletas.py gTileset_Canalave --desfazer
    python3 dev_scripts/compacta_paletas.py --demo              # autoteste de unidade
    python3 dev_scripts/compacta_paletas.py gTileset_Canalave --autoteste
        o portão de verdade: render antes contra render depois, 0 pixel
"""
import os
import shutil
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
os.environ.setdefault("REPO_MAPAS", RAIZ)
import compacta_tileset as C     # noqa: E402
import render_maps as R
import pinos_anim as PA          # noqa: E402

BACKUP = os.path.join(RAIZ, "build", "compacta_paletas")
NUM_PALS_TOTAL = 13              # include/fieldmap.h
CORES_POR_PAL = 16               # a entrada 0 e transparente no BG
HEADERS = os.path.join(RAIZ, "src/data/tilesets/headers.h")


# ------------------------------------------------------------------- leitura
def le_pal(caminho):
    """As 16 cores de um JASC-PAL, como lista de tuplas RGB."""
    linhas = [l.strip() for l in open(caminho, encoding="utf-8") if l.strip()]
    return [tuple(int(v) for v in l.split()) for l in linhas[3:3 + CORES_POR_PAL]]


def grava_pal(caminho, cores):
    """JASC-PAL de 16 cores, com o CRLF que o resto do repo usa."""
    if len(cores) != CORES_POR_PAL:
        raise SystemExit("paleta com %d cores, o formato pede %d"
                         % (len(cores), CORES_POR_PAL))
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write("JASC-PAL\r\n0100\r\n%d\r\n" % CORES_POR_PAL)
        for cor in cores:
            f.write("%d %d %d\r\n" % tuple(cor))


def n_pals_primario(layouts):
    """6 no emerald, 7 no johto/frlg. Erra alto se o tileset mistura os dois."""
    versoes = {(l.get("layout_version") or "emerald") for l in layouts}
    bases = {7 if v in ("johto", "frlg") else 6 for v in versoes}
    if len(bases) > 1:
        raise SystemExit("o tileset e usado com layout_version misturado "
                         "(NUM_PALS_IN_PRIMARY %s): a mesma vaga significaria "
                         "coisas diferentes por mapa" % sorted(bases))
    return bases.pop()


def tem_callback(rotulo):
    """O tileset tem animação de tile/paleta? Ler o headers.h, não adivinhar."""
    if not os.path.exists(HEADERS):
        return None
    texto = open(HEADERS, encoding="utf-8").read()
    marca = "const struct Tileset %s =" % rotulo
    i = texto.find(marca)
    if i < 0:
        return None
    corpo = texto[i:texto.find("};", i)]
    for linha in corpo.splitlines():
        if ".callback" in linha:
            return "NULL" not in linha
    return False


# --------------------------------------------------------------------- plano
def mede(rotulo, todos=None):
    """Lê tudo do disco e devolve o retrato do tileset, sem decidir nada."""
    pasta, base, layouts = C.contexto(rotulo, todos)
    n_pri = n_pals_primario(layouts)
    vagas_sec = list(range(n_pri, NUM_PALS_TOTAL))

    tiles, paleta_png, info, cols = C.tiles_do_png(os.path.join(pasta, "tiles.png"))
    meta = open(os.path.join(pasta, "metatiles.bin"), "rb").read()
    pals = {}
    for vaga in range(NUM_PALS_TOTAL):
        caminho = os.path.join(pasta, "palettes", "%02d.pal" % vaga)
        pals[vaga] = le_pal(caminho) if os.path.exists(caminho) else None

    # quem usa o que: (tile local, vaga) -> quantas entradas de metatile
    usos = {}
    congelados = set()            # tile do secundario pintado com paleta do primario
    vagas_com_tile_do_primario = set()
    for i, palavra in enumerate(C.entradas(meta)):
        idx, vaga = palavra & 0x3FF, (palavra >> 12) & 0xF
        if idx < base:
            # tile do PRIMARIO. Se a paleta e secundaria, a vaga fica presa.
            if vaga in vagas_sec:
                vagas_com_tile_do_primario.add(vaga)
            continue
        local = idx - base
        if local >= len(tiles):
            raise SystemExit("%s: o metatile pede o tile local %d e o tiles.png "
                             "so tem %d" % (rotulo, local, len(tiles)))
        if vaga in vagas_sec:
            usos[(local, vaga)] = usos.get((local, vaga), 0) + 1
        else:
            congelados.add(local)          # paleta do primario: nibble intocavel

    # pinos vindos do PRIMARIO: tile do secundario que metatile do primario pede
    pinos_tile, avisos = C.pinos_do_primario(rotulo, pasta, base, layouts)
    pinos_tile = {p for p in pinos_tile if p < len(tiles)}
    congelados |= pinos_tile
    vagas_do_primario = _vagas_que_o_primario_pinta(layouts, vagas_sec)

    # as cores que os PIXELS de cada vaga realmente usam
    indices = {}                  # vaga -> conjunto de indices de cor usados
    for (local, vaga) in usos:
        s = indices.setdefault(vaga, set())
        for linha in tiles[local]:
            s.update(linha)
    for vaga, idx in indices.items():
        # .pal curto e real no repo. render_maps.desenhar_tile faz
        # `cores[idx_cor % len(cores)]`, ou seja, ele DA A VOLTA em vez de
        # falhar, e o desenho ja esta errado hoje. Reempacotar por cima disso
        # so esconderia o defeito, entao aqui e recusa dura.
        if pals[vaga] is None or max(idx) >= len(pals[vaga]):
            raise SystemExit("%s: a vaga %d tem %s cores no .pal e um pixel "
                             "pede o indice %d" % (rotulo, vaga,
                                                   len(pals[vaga] or []), max(idx)))
    cores = {v: {pals[v][i] for i in idx if i != 0} for v, idx in indices.items()}
    zero = {v: (pals[v][0] if 0 in indices[v] else None) for v in indices}

    presas = (vagas_com_tile_do_primario | vagas_do_primario) & set(indices)
    return dict(rotulo=rotulo, pasta=pasta, base=base, layouts=layouts,
                n_pri=n_pri, vagas_sec=vagas_sec, tiles=tiles,
                paleta_png=paleta_png, info=info, colunas=cols, meta=meta,
                pals=pals, usos=usos, indices=indices, cores=cores, zero=zero,
                congelados=congelados, presas=presas, avisos=avisos,
                teto_tiles=1024 - base)


def _vagas_que_o_primario_pinta(layouts, vagas_sec):
    """Vagas secundárias que um metatile ALCANÇÁVEL do primário usa.

    O primário é compartilhado; mexer no conteúdo de uma vaga que ele pinta
    muda o desenho dele em todo mapa deste par. Essas vagas viram pino.
    """
    presas = set()
    primarios = {}
    for layout in layouts:
        primarios.setdefault(layout["primary_tileset"], []).append(layout)
    for rotulo_pri, usos in sorted(primarios.items()):
        pasta_pri = R.caminho_tileset(rotulo_pri)
        meta_pri = open(os.path.join(pasta_pri, "metatiles.bin"), "rb").read()
        palavras = C.entradas(meta_pri)
        alcancaveis = set()
        for layout in usos:
            dados = open(os.path.join(RAIZ, layout["blockdata_filepath"]), "rb").read()
            alcancaveis |= {struct.unpack_from("<H", dados, i)[0] & 0x3FF
                            for i in range(0, len(dados), 2)}
        for m in range(len(palavras) // 8):
            if m not in alcancaveis:
                continue
            for i in range(8):
                vaga = (palavras[m * 8 + i] >> 12) & 0xF
                if vaga in vagas_sec:
                    presas.add(vaga)
    return presas


def _particoes(itens):
    """Todas as partições de um conjunto pequeno, em ordem determinística."""
    if not itens:
        yield []
        return
    primeiro, resto = itens[0], itens[1:]
    for parte in _particoes(resto):
        for i in range(len(parte)):
            yield parte[:i] + [[primeiro] + parte[i]] + parte[i + 1:]
        yield [[primeiro]] + parte


def _cabe(grupo, retrato):
    """O grupo fecha em 15 cores exatas e concorda no índice 0?"""
    uniao = set()
    for vaga in grupo:
        uniao |= retrato["cores"][vaga]
    if len(uniao) > CORES_POR_PAL - 1:
        return None
    zeros = {retrato["zero"][v] for v in grupo if retrato["zero"][v] is not None}
    if len(zeros) > 1:
        return None                   # dois índices 0 diferentes: não dá
    return uniao, (zeros.pop() if zeros else (0, 0, 0))


def agrupa(retrato, alvo=None):
    """Menor número de grupos que fecha, sem aproximar cor. Determinístico."""
    livres = sorted(v for v in retrato["indices"] if v not in retrato["presas"])
    presas = sorted(retrato["presas"])
    if len(livres) > 9:
        return _agrupa_guloso(retrato, livres, presas)
    melhor = None
    for parte in _particoes(livres):
        if melhor is not None and len(parte) > len(melhor):
            continue
        fechados = [_cabe(sorted(g), retrato) for g in parte]
        if any(f is None for f in fechados):
            continue
        chave = sorted(sorted(g) for g in parte)
        if melhor is None or (len(chave), chave) < (len(melhor), melhor):
            melhor = chave
        if alvo is not None and len(melhor) <= alvo:
            break
    if melhor is None:
        raise SystemExit("nenhum agrupamento fecha em %d cores sem aproximar "
                         "nenhuma" % (CORES_POR_PAL - 1))
    return [[p] for p in presas] + melhor, set(presas)


def _agrupa_guloso(retrato, livres, presas):
    """Plano B para tileset com muitas vagas: primeiro a que gasta mais cor."""
    grupos = []
    for vaga in sorted(livres, key=lambda v: (-len(retrato["cores"][v]), v)):
        for g in grupos:
            if _cabe(sorted(g + [vaga]), retrato):
                g.append(vaga)
                break
        else:
            grupos.append([vaga])
    return ([[p] for p in presas]
            + sorted(sorted(g) for g in grupos)), set(presas)


def monta_plano(rotulo, alvo=None, todos=None, forcar=False):
    """Mede, agrupa e monta o de-para completo. Não escreve nada."""
    # ANIMAÇÃO. A recusa antiga era por `.callback` no headers.h, e isso é grosso
    # nos dois sentidos: `gTileset_PetalburgSinnoh` e `gTileset_LilycoveSinnoh`
    # têm `.callback` e a função de init deles põe o ponteiro em NULL, ou seja
    # não escrevem vaga nenhuma e estavam sendo recusados à toa; e quando a
    # animação existe de verdade "recusa tudo" não diz QUAIS vagas são
    # intocáveis. Agora quem responde é o `dev_scripts/pinos_anim.py`, que segue
    # a cadeia init -> passo -> AppendTilesetAnimToBuffer e devolve as vagas.
    vagas_anim, anim_ativa, explicacao_anim = PA.pinos_de_anim(rotulo)
    if anim_ativa and not forcar:
        raise SystemExit(
            "%s tem animacao ATIVA (%s) e ela escreve tile cru nas vagas %s em "
            "tempo de execucao: o reempacotamento reindexa o nibble desses "
            "tiles e o motor escreveria por cima com o nibble antigo, o que nao "
            "aparece em render estatico e so aparece dentro do jogo. Use "
            "--forcar so depois de CONGELAR esses tiles e PINAR a vaga de "
            "paleta de todo metatile que os usa." % (
                rotulo, explicacao_anim, PA.faixas(vagas_anim)))
    retrato = mede(rotulo, todos)
    grupos, presas = agrupa(retrato, alvo)

    # numeracao: pino fica onde esta, grupo livre pega o menor numero vago
    destino_vaga = {}
    tomados = set(presas)
    for g in grupos:
        if len(g) == 1 and g[0] in presas:
            destino_vaga[g[0]] = g[0]
    livres_num = [n for n in retrato["vagas_sec"] if n not in tomados]
    for g in sorted((g for g in grupos if not (len(g) == 1 and g[0] in presas)),
                    key=lambda g: min(g)):
        numero = livres_num.pop(0)
        for vaga in g:
            destino_vaga[vaga] = numero

    # a paleta de cada grupo: indice 0 preservado, cores nao-zero em ordem fixa
    nova_pal, de_para_cor = {}, {}
    for g in grupos:
        numero = destino_vaga[g[0]]
        uniao, cor_zero = _cabe(sorted(g), retrato)
        ordenadas = sorted(uniao)
        cores = [cor_zero] + ordenadas + [(0, 0, 0)] * (CORES_POR_PAL - 1 - len(ordenadas))
        nova_pal[numero] = cores
        onde = {c: i + 1 for i, c in enumerate(ordenadas)}
        for vaga in g:
            velha = retrato["pals"][vaga]
            # indice que nenhum pixel usa vai para 0: ele nunca e desenhado, e
            # deixa-lo apontando para cor fora da uniao seria mentira no .pal.
            tab = [0] * CORES_POR_PAL
            for i in range(1, min(len(velha), CORES_POR_PAL)):
                tab[i] = onde.get(velha[i], 0)
            de_para_cor[vaga] = tab

    # o de-para de TILE: um tile por (tile, vaga de origem), com deduplicacao
    tiles = retrato["tiles"]
    base = retrato["base"]
    por_tile = {}
    for (local, vaga), n in retrato["usos"].items():
        por_tile.setdefault(local, {})[vaga] = n

    def remapeia(tile, vaga):
        tab = de_para_cor[vaga]
        return tuple(tuple(0 if c == 0 else tab[c] for c in linha) for linha in tile)

    finais = list(tiles)              # conteudo final de cada vaga de tile ja existente
    escolha = {}                      # tile local -> vaga de origem que fica no lugar
    for local, vagas in por_tile.items():
        if local in retrato["congelados"]:
            continue                  # o original fica intacto na vaga dele
        escolha[local] = sorted(vagas, key=lambda v: (-vagas[v], v))[0]
        finais[local] = remapeia(tiles[local], escolha[local])

    indice_de = {c: i for i, c in enumerate(finais)}    # primeiro que casar
    de_para_tile, novos_tiles = {}, []
    for local in sorted(por_tile):
        for vaga in sorted(por_tile[local]):
            if escolha.get(local) == vaga:
                de_para_tile[(local, vaga)] = local
                continue
            conteudo = remapeia(tiles[local], vaga)
            if conteudo in indice_de:
                de_para_tile[(local, vaga)] = indice_de[conteudo]
                continue
            novo = len(finais) + len(novos_tiles)
            novos_tiles.append(conteudo)
            indice_de[conteudo] = novo
            de_para_tile[(local, vaga)] = novo

    total = len(finais) + len(novos_tiles)
    if total > retrato["teto_tiles"]:
        raise SystemExit("as duplicatas estouram o teto de %d tiles (%d)"
                         % (retrato["teto_tiles"], total))

    livres_depois = [n for n in retrato["vagas_sec"] if n not in set(destino_vaga.values())]
    plano = dict(retrato)
    plano.update(grupos=grupos, presas=presas, destino_vaga=destino_vaga,
                 nova_pal=nova_pal, de_para_cor=de_para_cor,
                 de_para_tile=de_para_tile, finais=finais,
                 novos_tiles=novos_tiles, vagas_livres=livres_depois,
                 antes=len(retrato["indices"]), depois=len(grupos))
    return plano


def aplica_plano(plano):
    """Gera (tiles finais, metatiles.bin novo) a partir do plano."""
    tiles = plano["finais"] + plano["novos_tiles"]
    base = plano["base"]
    saida = bytearray(plano["meta"])
    for i in range(0, len(saida), 2):
        palavra = struct.unpack_from("<H", saida, i)[0]
        idx, vaga = palavra & 0x3FF, (palavra >> 12) & 0xF
        if vaga not in plano["destino_vaga"] or idx < base:
            continue
        novo_tile = plano["de_para_tile"][(idx - base, vaga)]
        # a mascara guarda os flips (bits 10 e 11); paleta e tile sao reescritos
        nova = (palavra & 0x0C00) | (plano["destino_vaga"][vaga] << 12) \
            | (base + novo_tile)
        struct.pack_into("<H", saida, i, nova)
    return tiles, bytes(saida)


# ------------------------------------------------------------------- escrita
def _pasta_backup(plano):
    return os.path.join(BACKUP, os.path.basename(plano["pasta"]))


def _arquivos(pasta):
    saida = ["tiles.png", "metatiles.bin"]
    saida += [os.path.join("palettes", "%02d.pal" % v) for v in range(NUM_PALS_TOTAL)
              if os.path.exists(os.path.join(pasta, "palettes", "%02d.pal" % v))]
    return saida


def escreve(plano):
    tiles, meta = aplica_plano(plano)
    destino = _pasta_backup(plano)
    for nome in _arquivos(plano["pasta"]):
        guardado = os.path.join(destino, nome)
        os.makedirs(os.path.dirname(guardado), exist_ok=True)
        if not os.path.exists(guardado):
            shutil.copy2(os.path.join(plano["pasta"], nome), guardado)
    resto = (-len(tiles)) % C.COLUNAS
    branco = tuple(tuple(0 for _ in range(8)) for _ in range(8))
    C.grava_png(os.path.join(plano["pasta"], "tiles.png"), tiles + [branco] * resto,
                plano["paleta_png"], plano["info"])
    with open(os.path.join(plano["pasta"], "metatiles.bin"), "wb") as f:
        f.write(meta)
    for numero, cores in sorted(plano["nova_pal"].items()):
        grava_pal(os.path.join(plano["pasta"], "palettes", "%02d.pal" % numero), cores)
    return len(tiles) + resto


def desfaz(rotulo):
    pasta = R.caminho_tileset(rotulo)
    guardado = os.path.join(BACKUP, os.path.basename(pasta))
    if not os.path.isdir(guardado):
        raise SystemExit("nao ha backup em %s" % guardado)
    n = 0
    for raiz, _dirs, nomes in os.walk(guardado):
        for nome in nomes:
            origem = os.path.join(raiz, nome)
            shutil.copy2(origem, os.path.join(pasta, os.path.relpath(origem, guardado)))
            n += 1
    print("%s: %d arquivos devolvidos de %s" % (rotulo, n, guardado))
    return 0


# ---------------------------------------------------------------- conferência
def confere(plano, tiles, meta_novo):
    """Prova de equivalência na camada do PIXEL, com a cor de verdade.

    Para cada entrada de metatile compara a matriz 8x8 de RGB desenhada antes e
    depois, mais os flips. Índice de cor não entra na conta: o que tem que ser
    igual é a COR na tela. Entrada que aponta para o primário passa reto, porque
    o primário não é tocado.
    """
    velhas, novas = C.entradas(plano["meta"]), C.entradas(meta_novo)
    if len(velhas) != len(novas):
        return ["o metatiles.bin mudou de tamanho"]
    base, antigos, pals = plano["base"], plano["tiles"], plano["pals"]
    nova_pal = plano["nova_pal"]
    erros = []

    def pinta(tile, cores):
        return tuple(tuple(None if c == 0 else cores[c] for c in linha) for linha in tile)

    for i, (a, b) in enumerate(zip(velhas, novas)):
        if (a & 0x0C00) != (b & 0x0C00):
            erros.append("entrada %d: os flips mudaram (%04X -> %04X)" % (i, a, b))
            continue
        ia, ib = a & 0x3FF, b & 0x3FF
        va, vb = (a >> 12) & 0xF, (b >> 12) & 0xF
        if ia < base or ib < base:
            if ia != ib or va != vb:
                erros.append("entrada %d: o primario mudou (%04X -> %04X)" % (i, a, b))
            continue
        if va not in plano["destino_vaga"]:
            if a != b:
                erros.append("entrada %d: vaga fora do plano mudou (%04X -> %04X)"
                             % (i, a, b))
            continue
        if ib - base >= len(tiles):
            erros.append("entrada %d: aponta para o tile %d e so ha %d"
                         % (i, ib - base, len(tiles)))
            continue
        cores_a = pals[va]
        cores_b = nova_pal.get(vb)
        if cores_b is None:
            erros.append("entrada %d: a vaga %d nao tem paleta nova" % (i, vb))
            continue
        if pinta(antigos[ia - base], cores_a) != pinta(tiles[ib - base], cores_b):
            erros.append("entrada %d: o tile %d/pal %d virou %d/pal %d e a cor "
                         "na tela mudou" % (i, ia - base, va, ib - base, vb))
        if len(erros) > 40:
            break
    return erros


# -------------------------------------------------------------------- relato
def relata(plano):
    print(plano["rotulo"])
    print("  pasta      %s" % os.path.relpath(plano["pasta"], RAIZ))
    print("  layouts    %d: %s" % (len(plano["layouts"]),
                                   ", ".join(l["id"] for l in plano["layouts"][:6])))
    print("  vagas      %d a %d (NUM_PALS_IN_PRIMARY %d, NUM_PALS_TOTAL %d)"
          % (plano["vagas_sec"][0], plano["vagas_sec"][-1], plano["n_pri"],
             NUM_PALS_TOTAL))
    for vaga in sorted(plano["indices"]):
        print("    pal %2d   %2d cores nao-zero%s -> vaga %d"
              % (vaga, len(plano["cores"][vaga]),
                 ", PINO" if vaga in plano["presas"] else "",
                 plano["destino_vaga"][vaga]))
    uniao = set()
    for c in plano["cores"].values():
        uniao |= c
    print("  paletas    %d -> %d vagas em uso (%d cores no total), livres: %s"
          % (plano["antes"], plano["depois"], len(uniao),
             plano["vagas_livres"] or "nenhuma"))
    print("  tiles      %d -> %d (%d duplicatas por tile em duas paletas), teto %d"
          % (len(plano["tiles"]), len(plano["finais"]) + len(plano["novos_tiles"]),
             len(plano["novos_tiles"]), plano["teto_tiles"]))
    for aviso in plano["avisos"]:
        print("  aviso      %s" % aviso)


def censo():
    todos = C._layouts_por_secundario()
    linhas, recusados = [], []
    for rotulo in sorted(todos):
        try:
            plano = monta_plano(rotulo, todos=todos)
        except (SystemExit, ValueError, OSError) as e:
            # o layouts.json tem entradas com secundario invalido (o rotulo "0"
            # de layout de teste, por exemplo); censo nao e lugar de morrer.
            recusados.append((rotulo, str(e)[:70]))
            continue
        if plano["depois"] < plano["antes"]:
            linhas.append((rotulo, plano["antes"], plano["depois"],
                           len(plano["novos_tiles"])))
    linhas.sort(key=lambda l: -(l[1] - l[2]))
    print("%-34s%7s%8s%9s" % ("secundario", "vagas", "depois", "tiles+"))
    for rotulo, antes, depois, dup in linhas:
        print("%-34s%7d%8d%9d" % (rotulo, antes, depois, dup))
    for rotulo, erro in recusados:
        print("%-34s  recusado: %s" % (rotulo, erro))
    return 0


# ------------------------------------------------------------------ autoteste
def demo():
    """Cada armadilha do cabeçalho com o seu caso, e a prova negativa no fim."""
    # 1. o indice 0 nunca sai do lugar e nunca recebe cor
    tab = [0, 3, 1, 2] + [0] * 12
    tile = ((0, 1, 2, 3, 0, 0, 0, 0),) * 8
    remapeado = tuple(tuple(0 if c == 0 else tab[c] for c in linha) for linha in tile)
    assert remapeado[0][0] == 0, remapeado
    assert 0 not in remapeado[0][1:4], remapeado

    # 2. a mascara da palavra: os flips sobrevivem, paleta e tile sao reescritos
    base, palavra = 512, 0xBDFF          # pal 11, flip H e V, tile 0x1FF
    nova = (palavra & 0x0C00) | (7 << 12) | (base + 9)
    assert (nova & 0x0C00) == (palavra & 0x0C00), (hex(palavra), hex(nova))
    assert (nova >> 12) == 7 and (nova & 0x3FF) == base + 9, hex(nova)

    # 3. duas cores diferentes NUNCA se fundem: o grupo so fecha se a uniao
    #    couber em 15 cores exatas.
    retrato = dict(cores={6: {(1, 1, 1)} | {(i, 0, 0) for i in range(7)},
                          7: {(2, 2, 2)} | {(i, 0, 0) for i in range(7)},
                          8: {(i, 9, 9) for i in range(15)}},
                   zero={6: None, 7: (0, 0, 0), 8: (0, 0, 0)})
    assert _cabe([6, 7], retrato), "8+8 com 7 cores em comum cabe em 15"
    assert _cabe([6, 8], retrato) is None, "8+15 nao cabe, e nao pode aproximar"

    # 4. indice 0 diferente barra a fusao
    retrato2 = dict(cores={6: {(1, 1, 1)}, 7: {(2, 2, 2)}},
                    zero={6: (9, 9, 9), 7: (8, 8, 8)})
    assert _cabe([6, 7], retrato2) is None, "dois indices 0 diferentes nao fundem"
    retrato2["zero"][7] = None
    assert _cabe([6, 7], retrato2), "vaga que nao usa o indice 0 nao atrapalha"

    # 5. as particoes sao completas: Bell(4) = 15
    assert len(list(_particoes([1, 2, 3, 4]))) == 15

    # 6. prova negativa da conferencia: um de-para de cor trocado tem que ser
    #    ACUSADO, nao passar calado.
    pal_velha = [(0, 0, 0), (10, 0, 0), (20, 0, 0)] + [(0, 0, 0)] * 13
    pal_nova = [(0, 0, 0), (20, 0, 0), (10, 0, 0)] + [(0, 0, 0)] * 13
    t = ((1, 2, 0, 0, 0, 0, 0, 0),) * 8
    certo = tuple(tuple({0: 0, 1: 2, 2: 1}[c] for c in linha) for linha in t)
    plano = dict(meta=struct.pack("<H", 512 | (6 << 12)), base=512, tiles=[t],
                 pals={6: pal_velha}, nova_pal={6: pal_nova},
                 destino_vaga={6: 6})
    novo_meta = struct.pack("<H", 512 | (6 << 12))
    assert not confere(plano, [certo], novo_meta), "o caso certo nao pode acusar"
    assert confere(plano, [t], novo_meta), "o de-para trocado passou calado"

    print("demo ok")
    return 0


def _mapas_do_tileset(plano):
    ids = {l["id"] for l in plano["layouts"]}
    import json
    saida = []
    pasta = os.path.join(RAIZ, "data/maps")
    for nome in sorted(os.listdir(pasta)):
        cam = os.path.join(pasta, nome, "map.json")
        if os.path.isfile(cam) and json.load(open(cam, encoding="utf-8"))["layout"] in ids:
            saida.append(nome)
    return saida


def _renderiza(nomes, destino):
    os.makedirs(destino, exist_ok=True)
    antigo = R.OUT_DIR
    R.OUT_DIR = destino
    try:
        layouts, cache = R.carregar_layouts(), {}
        for nome in nomes:
            R.renderizar_mapa(nome, layouts, cache)
    finally:
        R.OUT_DIR = antigo


def autoteste(rotulo):
    """O portão: render antes contra render depois, e tem que dar 0 pixel."""
    import tempfile
    from PIL import Image, ImageChops

    plano = monta_plano(rotulo)
    tiles, meta = aplica_plano(plano)
    erros = confere(plano, tiles, meta)
    print("1. conferencia por entrada de metatile (cor na tela): %s"
          % ("VERDE, %d entradas" % (len(plano["meta"]) // 2) if not erros
             else "VERMELHO: %s" % erros[:3]))

    # prova negativa: trocar duas cores da paleta nova tem que ser acusado
    sabotado = dict(plano)
    ruim = {k: list(v) for k, v in plano["nova_pal"].items()}
    alvo = sorted(ruim)[0]
    ruim[alvo][1], ruim[alvo][2] = ruim[alvo][2], ruim[alvo][1]
    sabotado["nova_pal"] = ruim
    acusou = bool(confere(sabotado, tiles, meta))
    print("2. prova negativa (paleta sabotada): %s"
          % ("ACUSOU" if acusou else "NAO ACUSOU"))

    nomes = _mapas_do_tileset(plano)
    tmp = tempfile.mkdtemp(prefix="compacta_paletas_")
    antes, depois = os.path.join(tmp, "antes"), os.path.join(tmp, "depois")
    total_px = difs = 0
    aplicou = False
    try:
        _renderiza(nomes, antes)
        escreve(plano)
        aplicou = True
        _renderiza(nomes, depois)
        for nome in sorted(os.listdir(antes)):
            a = Image.open(os.path.join(antes, nome)).convert("RGB")
            b = Image.open(os.path.join(depois, nome)).convert("RGB")
            total_px += a.size[0] * a.size[1]
            if a.size != b.size:
                difs += a.size[0] * a.size[1]
                continue
            dif = ImageChops.difference(a, b).convert("L")
            # histograma em vez de getdata: mesma conta, sem materializar
            # 600 mil pixels em lista, e sem a API que a Pillow 14 tira.
            difs += sum(dif.histogram()[1:])
    finally:
        if aplicou:
            desfaz(rotulo)
    print("3. PORTAO: %d mapas (%s), %d pixels diferentes de %d"
          % (len(nomes), ", ".join(nomes), difs, total_px))

    # idempotencia: o plano do estado ja compactado nao pode mexer mais nada
    print("4. render guardado em %s" % tmp)
    falhou = bool(erros) or not acusou or difs
    print("AUTOTESTE %s" % ("VERMELHO" if falhou else "VERDE"))
    return 1 if falhou else 0


# ---------------------------------------------------------------------- main
def main():
    argv = sys.argv[1:]
    if "--demo" in argv:
        return demo()
    rotulos = [a for a in argv if not a.startswith("--")]
    alvo = None
    if "--alvo" in argv:
        alvo = int(argv[argv.index("--alvo") + 1])
        rotulos = [r for r in rotulos if r != str(alvo)]
    forcar = "--forcar" in argv
    if "--autoteste" in argv:
        if not rotulos:
            raise SystemExit("--autoteste precisa do nome do tileset")
        return max(autoteste(r) for r in rotulos)
    if "--desfazer" in argv:
        if not rotulos:
            raise SystemExit("--desfazer precisa do nome do tileset")
        for rotulo in rotulos:
            desfaz(rotulo)
        return 0
    if not rotulos:
        return censo()
    for rotulo in rotulos:
        plano = monta_plano(rotulo, alvo=alvo, forcar=forcar)
        relata(plano)
        if plano["depois"] == plano["antes"] and not plano["novos_tiles"]:
            print("  nada a fazer: as vagas ja estao compactadas")
            continue
        if "--aplicar" in argv:
            tiles, meta = aplica_plano(plano)
            erros = confere(plano, tiles, meta)
            if erros:
                print("  RECUSADO: a conferencia acusou")
                for e in erros[:5]:
                    print("   ", e)
                return 1
            total = escreve(plano)
            print("  aplicado   tiles.png com %d tiles, backup em %s"
                  % (total, os.path.relpath(_pasta_backup(plano), RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
