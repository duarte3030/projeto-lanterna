#!/usr/bin/env python3
"""O portão de PLANTA da onda 2 do REFINO, escrito FORA do script que desenha.

Por que existe, e por que ele não podia morar dentro do gerador de cada cidade.
Cada frente desta onda escreve o próprio script de desenho e o próprio
auto-teste, e o auto-teste de um gerador é, no fundo, o gerador se olhando no
espelho: ele mede o que planejou, com o mesmo código que planejou. O portão 4 do
método manda verificar NA CAMADA DA AFIRMAÇÃO, e a afirmação desta onda é sobre
o `map.bin` em disco contra o `map.bin` do commit de referência, não sobre o
plano em memória. Este script só olha para os dois arquivos e para os atributos
dos dois tilesets, e não sabe nada sobre bolha, mancha, trilha nem catálogo.

O QUE ELE COBRA, e cada item é uma regra dura escrita no briefing da onda:

  1. TAMANHO. O `map.bin` tem que ter o mesmo número de células. Tamanho
     diferente é planta mudada, e é o pior defeito possível aqui.
  2. ELEVAÇÃO intacta em 100% das palavras. Nenhuma exceção, nunca.
  3. COLISÃO 1 -> 0 em ZERO células. O caminho não pode ganhar passagem nova.
     Colisão 0 -> 1 é permitida e sai contada, célula a célula.
  4. (BEHAVIOR, LAYERTYPE) idêntico em toda célula que continua ANDÁVEL. É o que
     garante que grama alta continua grama alta, que a areia continua areia e
     que a porta continua porta. Célula que virou sólida sai da conta, porque
     ninguém pisa nela, mas ela paga o item 6.
  5. LAYERTYPE da célula solidificada tem que ser COVERED (0x1000). Com
     `NORMAL`, a camada de cima vai para o BG1 e desenha ACIMA do boneco, que é
     o defeito E3 do `mapas_qa.py`: o jogador anda por dentro do cenário.
  6. ALCANCE A PÉ, pelos DOIS portões, e o segundo não é enfeite:
       (a) busca em largura a partir de todo warp e todo object_event,
           respeitando elevação: o alcance depois tem que ser exatamente o
           alcance antes menos as células que a decoração ocupou.
       (b) COMPONENTES conexos do chão andável: nenhum pedaço pode se partir em
           dois nem se juntar a outro. Em Snowpoint o portão (a) passou VERDE
           numa sabotagem que fechava um corredor de duas células, porque havia
           warp dos dois lados: ninguém saía do alcance e mesmo assim o jogador
           deixava de chegar nas casas do norte.
  7. CÉLULA DE EVENTO. Nenhum warp, object_event, bg_event ou coord_event pode
     ter virado sólido embaixo de si.

COMO ELE PODE ERRAR, dito na cara:

  - A busca em largura usa a regra de elevação do `arte_mapas_pobres.py` e do
    `enfeita_cidades.py` desta árvore (elevação 0 é curinga e casa com
    qualquer vizinho, e o resto exige igualdade), que é uma aproximação do
    `MapGridGetElevationAt` do motor. Ela é a MESMA dos dois lados da
    comparação, então serve para comparar antes com depois, e não serve para
    afirmar que o mapa é jogável.
  - Ele lê o `map.json` da árvore de HOJE para achar warp e evento. Se a frente
    tivesse mexido no `map.json`, a comparação usaria eventos diferentes dos
    dois lados; por isso ele EXIGE que o `map.json` esteja igual ao da
    referência e reprova se não estiver, em vez de seguir calado.
  - Água tem colisão 0 no Emerald e entra na busca como chão. Isso infla os dois
    lados igualmente e não muda o veredito, mas explica número grande de células
    alcançáveis em cidade com canal.

Uso:
    python3 dev_scripts/portao_planta.py CelesticTown SolaceonTown --ref a0e54260a2
    python3 dev_scripts/portao_planta.py --demo
"""
import collections
import json
import os
import struct
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
os.environ.setdefault("REPO_MAPAS", RAIZ)
import render_maps as R      # noqa: E402
import atributos_metatile as AM      # noqa: E402

MASCARA_BEHAVIOR = 0x00FF
MASCARA_LAYER = 0xF000
LAYER_COVERED = 0x1000


def _git(ref, caminho):
    """Conteúdo de um arquivo num commit. None quando ele não existe lá."""
    try:
        return subprocess.check_output(["git", "-C", RAIZ, "show", f"{ref}:{caminho}"],
                                       stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None


def _celulas(dados):
    return [struct.unpack_from("<H", dados, i)[0] for i in range(0, len(dados), 2)]


def base_do_secundario(layout):
    """Onde comeca o indice de metatile do SECUNDARIO: 512 no layout `emerald`,
    640 no `johto` e no `frlg`.

    Ate 09/09/2026 este arquivo cravava 512, e isso era um defeito CALADO em
    Johto, medido em `CianwoodCity` antes de qualquer executor tocar no mapa:
    o dicionario saia com chaves de 0 a 751, o mapa usa metatiles de 0 a 849, e
    entao (a) treze metatiles que a cidade USA nao tinham atributo nenhum e
    caiam no `.get(..., 0)`, e (b) os que tinham liam o atributo de OUTRO
    metatile, porque o secundario era escrito por cima da faixa 512 a 639 do
    primario. O metatile 641 do mapa, cujo atributo de verdade e 0x0000, era
    lido como 0x1017.

    O estrago disso e dos dois tipos ao mesmo tempo. Celula solidificada cujo
    metatile cai fora do dicionario le atributo 0, e 0 nao e COVERED, entao o
    item 5 REPROVA um trabalho certo; celula solidificada que le o atributo
    trocado de outro metatile pode ler COVERED sem ser, e ai o item 5 APROVA
    um trabalho errado. O item 4 sofre igual: enquanto a celula fica com o mesmo
    metatile os dois lados leem a mesma coisa errada e a comparacao passa, mas
    trocar o metatile de uma celula andavel, que e exatamente o que esta onda
    faz, compara lixo com lixo.

    O 640 nao e numero decorado: e `NUM_TILES_IN_PRIMARY_FRLG` de
    `include/fieldmap.h`, e quem escolhe entre um e outro e o `layout_version`
    do layout, que o `tools/mapjson/mapjson.cpp` traduz em `bigPrimary`. A mesma
    conta ja estava escrita em `dev_scripts/compacta_tileset.py`.
    """
    versao = (layout.get("layout_version") if layout else None) or "emerald"
    return 640 if versao in ("johto", "frlg") else 512


def _atributos(pasta_pri, pasta_sec, meta_pri=None, meta_sec=None, base_sec=512,
               versao="emerald"):
    """attr[indice_de_metatile] -> a palavra NORMALIZADA (`beh | layerType << 12`).

    `base_sec` vem de `base_do_secundario(layout)` e `versao` do
    `layout_version` do layout. O padrao dos dois e o do `emerald`, que e o de
    Sinnoh e o de Hoenn.

    Ate 09/09/2026 esta funcao lia SEMPRE `u16`, e isso e um defeito CALADO em
    KANTO, onde o layout e `frlg` e o arquivo guarda **4 bytes por metatile**
    (`GetAttributeByMetatileIdAndMapLayoutFrlg` em `src/fieldmap.c` le o
    ponteiro como `const u32 *`). O arquivo de `general_frlg` tem 2.560 bytes:
    lido de dois em dois ele virava 1.280 "metatiles" para 640 que existem, e
    cada palavra lida era METADE de um atributo de verdade. Os itens 4 e 5 deste
    portao, que sao justamente os que garantem que enfeitar nao muda caminho,
    estariam comparando lixo com lixo e dizendo VERDE com cara de quem conferiu.

    Quem sabe a largura, as mascaras e o corte de cada layout e
    `dev_scripts/atributos_metatile.py`, e e de la que vem a normalizacao para o
    formato do Emerald, que deixa o resto deste arquivo mascarar `0x00FF` e
    `0xF000` sem mudar uma linha.
    """
    return AM.tabela(pasta_pri, pasta_sec, versao, meta_pri, meta_sec, corte=base_sec)


def _vizinhos(x, y, w, h):
    if x > 0:
        yield x - 1, y
    if x + 1 < w:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y + 1 < h:
        yield x, y + 1


def alcance(celulas, w, h, partidas):
    """Células alcançáveis a pé a partir de `partidas`, respeitando elevação."""
    def andavel(i):
        return ((celulas[i] >> 10) & 0x3) == 0

    def elev(i):
        return (celulas[i] >> 12) & 0xF

    vistos = set()
    fila = collections.deque()
    for (x, y) in partidas:
        if 0 <= x < w and 0 <= y < h:
            i = y * w + x
            if andavel(i) and i not in vistos:
                vistos.add(i)
                fila.append(i)
    while fila:
        i = fila.popleft()
        x, y = i % w, i // w
        for (nx, ny) in _vizinhos(x, y, w, h):
            j = ny * w + nx
            if j in vistos or not andavel(j):
                continue
            ea, eb = elev(i), elev(j)
            if ea and eb and ea != eb:
                continue
            vistos.add(j)
            fila.append(j)
    return vistos


def componentes(celulas, w, h, com_rotulo=False):
    """Pedaços conexos de chão andável: tamanhos, e o rótulo de cada célula."""
    def andavel(i):
        return ((celulas[i] >> 10) & 0x3) == 0

    def elev(i):
        return (celulas[i] >> 12) & 0xF

    rotulo = [-1] * len(celulas)
    tamanhos = []
    for inicio in range(len(celulas)):
        if rotulo[inicio] >= 0 or not andavel(inicio):
            continue
        atual = len(tamanhos)
        rotulo[inicio] = atual
        fila = collections.deque([inicio])
        n = 0
        while fila:
            i = fila.popleft()
            n += 1
            x, y = i % w, i // w
            for (nx, ny) in _vizinhos(x, y, w, h):
                j = ny * w + nx
                if rotulo[j] >= 0 or not andavel(j):
                    continue
                ea, eb = elev(i), elev(j)
                if ea and eb and ea != eb:
                    continue
                rotulo[j] = atual
                fila.append(j)
        tamanhos.append(n)
    if com_rotulo:
        return tamanhos, rotulo
    return sorted(tamanhos, reverse=True)


def parte_ou_junta(antes, depois, w, h):
    """Casa os pedacos de chao dos dois lados, celula a celula.

    Contar pedaco antes e depois NAO serve: um bolso de uma celula coberto
    inteiro pela decoracao derruba a contagem sem partir nada. O que a regra
    proibe e um pedaco virar dois (o jogador deixa de atravessar) ou dois
    virarem um (apareceu passagem nova).

    Devolve (tamanhos_antes, tamanhos_depois, partidos, juntados, sumidos).
    """
    comp_antes, rot_antes = componentes(antes, w, h, com_rotulo=True)
    comp_depois, rot_depois = componentes(depois, w, h, com_rotulo=True)
    de_para = collections.defaultdict(set)
    para_de = collections.defaultdict(set)
    for i in range(len(antes)):
        ra, rd = rot_antes[i], rot_depois[i]
        if ra < 0 or rd < 0:
            continue
        de_para[ra].add(rd)
        para_de[rd].add(ra)
    partidos = {ra: ds for ra, ds in de_para.items() if len(ds) > 1}
    juntados = {rd: a for rd, a in para_de.items() if len(a) > 1}
    sumidos = [comp_antes[ra] for ra in range(len(comp_antes)) if ra not in de_para]
    return comp_antes, comp_depois, partidos, juntados, sumidos


def confere_mapa(nome, ref, layouts=None, ref_eventos=None):
    """Roda os sete itens num mapa. Devolve (erros, retrato)."""
    layouts = layouts if layouts is not None else R.carregar_layouts()
    # O `carregar_layouts` indexa por ID (LAYOUT_CELESTIC_TOWN), e o que chega
    # aqui e o nome do MAPA. Procurar pelos dois, e pelo campo `name`.
    layout = layouts.get(nome) or layouts.get(nome + "_Layout")
    if layout is None:
        for l in layouts.values():
            if l.get("name") in (nome + "_Layout", nome):
                layout = l
                break
    if layout is None:
        # A FONTE DA VERDADE do layout de um mapa e o campo `layout` do
        # `map.json` dele, e nao o nome. Kanto e a familia em que os dois nao
        # batem: o mapa se chama `PalletTown_Frlg`, o layout dele se chama
        # `PalletTown_Layout`, e nenhuma das tres tentativas acima acha isso.
        # Medido em 09/09/2026: as 14 cidades de Kanto saiam VERMELHAS com
        # "layout nao encontrado", ou seja, o portao recusava o mapa em vez de
        # conferi-lo, e a onda de refino de Kanto ficava sem portao de planta.
        caminho_mapa = os.path.join(RAIZ, "data/maps/%s/map.json" % nome)
        if os.path.exists(caminho_mapa):
            with open(caminho_mapa, encoding="utf-8") as f:
                layout = layouts.get(json.load(f).get("layout"))
    if layout is None:
        return ["%s: layout nao encontrado" % nome], {}
    erros = []
    caminho_bin = layout["blockdata_filepath"]
    caminho_json = "data/maps/%s/map.json" % nome

    antes_cru = _git(ref, caminho_bin)
    if antes_cru is None:
        return ["%s: %s nao existe em %s" % (nome, caminho_bin, ref)], {}
    depois_cru = open(os.path.join(RAIZ, caminho_bin), "rb").read()

    # item 7 comeca aqui: o map.json tem que estar igual, senao a comparacao
    # usaria eventos diferentes dos dois lados e nao valeria nada.
    # O map.json tem referencia PROPRIA. O `ref` do map.bin e o commit em que a
    # frente de arte nasceu; o map.json pode ter mudado depois, e legitimamente,
    # por outra frente (a quebra de save mexeu em id de treinador e em flag de
    # objeto). O que esta onda proibe e a FRENTE DE ARTE encostar nele, entao a
    # comparacao certa e contra o ramo de onde ela partiu para valer, e nao
    # contra o commit do map.bin.
    json_antes = _git(ref_eventos or ref, caminho_json)
    json_depois = open(os.path.join(RAIZ, caminho_json), "rb").read()
    if json_antes is not None and json_antes != json_depois:
        erros.append("%s: o map.json MUDOU entre %s e agora; a onda proibe "
                     "encostar em warp, objeto, placa e gatilho"
                     % (nome, ref_eventos or ref))

    antes, depois = _celulas(antes_cru), _celulas(depois_cru)
    if len(antes) != len(depois):
        erros.append("%s: o map.bin tem %d celulas e tinha %d: a PLANTA mudou"
                     % (nome, len(depois), len(antes)))
        return erros, {}

    w, h = layout["width"], layout["height"]
    if w * h != len(depois):
        erros.append("%s: o layout diz %dx%d e o map.bin tem %d celulas"
                     % (nome, w, h, len(depois)))
        return erros, {}

    # atributos dos dois lados, cada um com o tileset do seu commit
    pri, sec = layout["primary_tileset"], layout["secondary_tileset"]
    pasta_pri = os.path.relpath(R.caminho_tileset(pri), RAIZ)
    pasta_sec = os.path.relpath(R.caminho_tileset(sec), RAIZ)
    base_sec = base_do_secundario(layout)
    versao = (layout.get("layout_version") or "emerald")
    attr_depois = _atributos(pasta_pri, pasta_sec, base_sec=base_sec, versao=versao)
    attr_antes = _atributos(
        pasta_pri, pasta_sec,
        _git(ref, os.path.join(pasta_pri, "metatile_attributes.bin")),
        _git(ref, os.path.join(pasta_sec, "metatile_attributes.bin")),
        base_sec=base_sec, versao=versao)
    # Portao de LEITURA, antes de qualquer veredito: metatile que o mapa usa e o
    # dicionario nao conhece vira atributo 0 no `.get`, e atributo 0 nao e
    # COVERED. Sem esta linha o portao reprova (ou aprova) por nao saber ler, e
    # diz "VERDE" ou "VERMELHO" com a mesma cara de quem sabe.
    orfaos = sorted({(c & 0x3FF) for c in antes + depois} - set(attr_depois))
    if orfaos:
        erros.append("%s: %d metatiles usados pelo mapa nao tem atributo no par "
                     "de tilesets (o primeiro e o %d, base do secundario %d): o "
                     "portao nao sabe ler este mapa e nao pode dar veredito"
                     % (nome, len(orfaos), orfaos[0], base_sec))

    solidificadas, soltas, elevacao, comportamento, sem_covered = [], [], [], [], []
    for i, (a, b) in enumerate(zip(antes, depois)):
        ca, cb = (a >> 10) & 0x3, (b >> 10) & 0x3
        ea, eb = (a >> 12) & 0xF, (b >> 12) & 0xF
        if ea != eb:
            elevacao.append(i)
        if ca == 0 and cb != 0:
            solidificadas.append(i)
            attr = attr_depois.get(b & 0x3FF, 0)
            if (attr & MASCARA_LAYER) != LAYER_COVERED:
                sem_covered.append((i, attr))
        elif ca != 0 and cb == 0:
            soltas.append(i)
        if cb == 0:
            pa = attr_antes.get(a & 0x3FF, 0)
            pb = attr_depois.get(b & 0x3FF, 0)
            if (pa & (MASCARA_BEHAVIOR | MASCARA_LAYER)) != (pb & (MASCARA_BEHAVIOR | MASCARA_LAYER)):
                comportamento.append((i, pa, pb))

    if elevacao:
        erros.append("%s: elevacao mudou em %d celulas (a primeira e (%d,%d))"
                     % (nome, len(elevacao), elevacao[0] % w, elevacao[0] // w))
    if soltas:
        erros.append("%s: colisao 1 -> 0 em %d celulas, e a onda proibe (a "
                     "primeira e (%d,%d))" % (nome, len(soltas), soltas[0] % w, soltas[0] // w))
    if comportamento:
        i, pa, pb = comportamento[0]
        erros.append("%s: (behavior, layerType) mudou em %d celulas ANDAVEIS "
                     "(a primeira e (%d,%d), %04X -> %04X)"
                     % (nome, len(comportamento), i % w, i // w, pa, pb))
    if sem_covered:
        i, attr = sem_covered[0]
        erros.append("%s: %d celulas viraram solidas com layerType != COVERED "
                     "(a primeira e (%d,%d), attr %04X): com NORMAL a camada de "
                     "cima cobre o boneco" % (nome, len(sem_covered), i % w, i // w, attr))

    # eventos: nada pode ter virado solido embaixo de um
    eventos = []
    dados_json = json.loads(json_depois)
    for chave in ("warp_events", "object_events", "bg_events", "coord_events"):
        for e in dados_json.get(chave) or []:
            eventos.append((chave, int(e["x"]), int(e["y"])))
    pisados = [(k, x, y) for (k, x, y) in eventos
               if 0 <= x < w and 0 <= y < h and (y * w + x) in set(solidificadas)]
    if pisados:
        erros.append("%s: %d eventos ficaram embaixo de decoracao solida (%s)"
                     % (nome, len(pisados), pisados[:3]))

    # alcance a pe, os dois portoes
    partidas = [(x, y) for (k, x, y) in eventos if k in ("warp_events", "object_events")]
    al_antes = alcance(antes, w, h, partidas)
    al_depois = alcance(depois, w, h, partidas)
    perdidas = al_antes - al_depois
    ganhas = al_depois - al_antes
    esperadas = set(solidificadas) & al_antes
    if ganhas:
        erros.append("%s: %d celulas ENTRARAM no alcance a pe, e nenhuma podia"
                     % (nome, len(ganhas)))
    if perdidas != esperadas:
        so_perdidas = sorted(perdidas - esperadas)[:3]
        erros.append("%s: o alcance a pe perdeu %d celulas e a decoracao ocupou "
                     "%d; sobram %d celulas perdidas sem decoracao em cima (%s)"
                     % (nome, len(perdidas), len(esperadas),
                        len(perdidas - esperadas),
                        [(i % w, i // w) for i in so_perdidas]))
    # PARTIR e JUNTAR, e nao "mudou de numero". Contar pedaco antes e depois nao
    # serve: um bolso de UMA celula que a decoracao cobriu inteiro derruba a
    # contagem sem partir nada, e foi exatamente o que aconteceu em
    # `OreburghCity` (11 -> 10, e o que sumiu foi um bolso de 1 celula). O que a
    # regra proibe e um pedaco virar dois (o jogador deixa de atravessar) ou
    # dois virarem um (apareceu passagem nova). Isso se mede casando os rotulos
    # celula a celula, nas celulas que continuam andaveis dos DOIS lados.
    comp_antes, comp_depois, partidos, juntados, sumidos = parte_ou_junta(
        antes, depois, w, h)
    if partidos:
        ra = sorted(partidos)[0]
        erros.append("%s: %d pedacos de chao se PARTIRAM (o de %d celulas virou "
                     "%d pedacos)" % (nome, len(partidos), comp_antes[ra],
                                      len(partidos[ra])))
    if juntados:
        rd = sorted(juntados)[0]
        erros.append("%s: %d pedacos de chao se JUNTARAM (o de %d celulas veio de "
                     "%d pedacos)" % (nome, len(juntados), comp_depois[rd],
                                      len(juntados[rd])))


    retrato = dict(mapa=nome, celulas=len(depois), largura=w, altura=h,
                   solidificadas=len(solidificadas), soltas=len(soltas),
                   elevacao=len(elevacao), comportamento=len(comportamento),
                   alcance_antes=len(al_antes), alcance_depois=len(al_depois),
                   pedacos_antes=len(comp_antes), pedacos_depois=len(comp_depois),
                   pedacos_sumidos=sumidos, pedacos_partidos=len(partidos),
                   pedacos_juntados=len(juntados),
                   mudadas=sum(1 for a, b in zip(antes, depois) if a != b))
    return erros, retrato


def demo():
    """Auto-teste: o portão tem que REPROVAR cada sabotagem, uma por item."""
    erros = []
    w = h = 8
    base = []
    for y in range(h):
        for x in range(w):
            solido = 1 if (x == 0 or y == 0 or x == w - 1 or y == h - 1) else 0
            base.append((solido << 10) | (3 << 12) | 5)

    def bfs(cel, partidas):
        return alcance(cel, w, h, partidas)

    # caso 1: um mapa igual a ele mesmo tem alcance e pedaços iguais.
    a = list(base)
    if bfs(a, [(3, 3)]) != bfs(list(base), [(3, 3)]):
        erros.append("caso 1: o mesmo mapa deu alcance diferente de si mesmo")
    if componentes(a, w, h) != componentes(list(base), w, h):
        erros.append("caso 1: o mesmo mapa deu pedacos diferentes de si mesmo")

    # caso 2, prova negativa do portão (b): fechar um corredor com warp dos DOIS
    # lados não tira ninguém do alcance, e mesmo assim parte o chão em dois. É a
    # sabotagem exata que passou verde em Snowpoint.
    corredor = []
    for y in range(h):
        for x in range(w):
            solido = 1 if (x == 0 or y == 0 or x == w - 1 or y == h - 1) else 0
            if y == 4 and 1 <= x <= w - 2 and x != 3:
                solido = 1
            corredor.append((solido << 10) | (3 << 12) | 5)
    fechado = list(corredor)
    fechado[4 * w + 3] = (1 << 10) | (3 << 12) | 5
    partidas = [(3, 2), (3, 6)]
    if len(bfs(corredor, partidas)) - 1 != len(bfs(fechado, partidas)):
        erros.append("caso 2: fechar o corredor devia tirar do alcance so a "
                     "celula ocupada, e o portao (a) sozinho passaria")
    if len(componentes(corredor, w, h)) != 1:
        erros.append("caso 2: o corredor aberto devia ser UM pedaco so")
    if len(componentes(fechado, w, h)) != 2:
        erros.append("caso 2: o corredor fechado devia partir o chao em DOIS, e "
                     "o portao (b) e o unico que ve isso")

    # caso 3, prova negativa: elevação diferente separa vizinhos.
    degrau = list(base)
    for x in range(1, w - 1):
        degrau[4 * w + x] = (0 << 10) | (7 << 12) | 5
    if len(bfs(degrau, [(3, 2)])) >= len(bfs(base, [(3, 2)])):
        erros.append("caso 3: elevacao diferente devia barrar a passagem")

    # caso 4, prova negativa: elevação 0 é curinga e NÃO barra.
    curinga = list(base)
    for x in range(1, w - 1):
        curinga[4 * w + x] = (0 << 10) | (0 << 12) | 5
    if len(bfs(curinga, [(3, 2)])) != len(bfs(base, [(3, 2)])):
        erros.append("caso 4: elevacao 0 e curinga e nao podia barrar nada")

    # caso 5, o casamento de pedacos: fechar o corredor tem que sair como
    # PARTIDO, e cobrir um bolso inteiro NAO pode sair como partido nem juntado.
    _, _, partidos, juntados, sumidos = parte_ou_junta(corredor, fechado, w, h)
    if len(partidos) != 1 or juntados:
        erros.append("caso 5: o corredor fechado devia sair como 1 pedaco PARTIDO "
                     "e 0 juntados, e deu %d e %d" % (len(partidos), len(juntados)))
    _, _, partidos, juntados, sumidos = parte_ou_junta(fechado, corredor, w, h)
    if len(juntados) != 1 or partidos:
        erros.append("caso 5: abrir o corredor devia sair como 1 pedaco JUNTADO, "
                     "e deu %d juntados e %d partidos" % (len(juntados), len(partidos)))

    # caso 6: bolso de UMA celula coberto inteiro. Foi o caso real de
    # OreburghCity (11 pedacos -> 10) e ele nao pode reprovar.
    bolso = list(base)
    bolso[2 * w + 2] = (1 << 10) | (3 << 12) | 5
    bolso[2 * w + 4] = (1 << 10) | (3 << 12) | 5
    bolso[1 * w + 3] = (1 << 10) | (3 << 12) | 5
    bolso[3 * w + 3] = (1 << 10) | (3 << 12) | 5
    coberto = list(bolso)
    coberto[2 * w + 3] = (1 << 10) | (3 << 12) | 5
    ca, cb, partidos, juntados, sumidos = parte_ou_junta(bolso, coberto, w, h)
    if len(ca) != len(cb) + 1:
        erros.append("caso 6: o bolso devia existir antes e sumir depois (%d -> %d)"
                     % (len(ca), len(cb)))
    if partidos or juntados:
        erros.append("caso 6: cobrir um bolso inteiro nao pode contar como "
                     "partido (%d) nem juntado (%d)" % (len(partidos), len(juntados)))
    if sumidos != [1]:
        erros.append("caso 6: o pedaco coberto tinha 1 celula e saiu como %s" % sumidos)

    # caso 7, a base do secundario, e ele nao e sintetico: le os tilesets de
    # verdade. Ate 09/09/2026 o `_atributos` cravava 512, e em Johto (layout
    # `johto`, bigPrimary) isso deixava metatiles USADOS pelo mapa sem atributo
    # nenhum e fazia os outros lerem o atributo de OUTRO metatile. O portao
    # continuava imprimindo VERDE, porque ele so olha celula que MUDOU e no
    # master nenhuma mudou: o defeito so apareceria no primeiro trabalho de
    # verdade, ja tarde. Este caso le o par de tilesets de um mapa de cada
    # versao de layout e cobra tres coisas.
    try:
        layouts = R.carregar_layouts()
    except Exception as e:                                   # pragma: no cover
        erros.append("caso 7: nao consegui carregar os layouts (%s)" % e)
        layouts = {}
    esperado = {"CianwoodCity": ("johto", 640), "GoldenrodCity": ("johto", 640),
                "SnowpointCity": ("emerald", 512)}
    for nome, (versao_esperada, base_esperada) in esperado.items():
        alvo = None
        for l in layouts.values():
            if (l.get("blockdata_filepath") or "").endswith("/%s/map.bin" % nome):
                alvo = l
                break
        if alvo is None:
            erros.append("caso 7: layout de %s nao achado" % nome)
            continue
        versao = alvo.get("layout_version") or "emerald"
        base = base_do_secundario(alvo)
        if (versao, base) != (versao_esperada, base_esperada):
            erros.append("caso 7: %s devia ser (%s, %d) e deu (%s, %d)"
                         % (nome, versao_esperada, base_esperada, versao, base))
            continue
        pri = os.path.relpath(R.caminho_tileset(alvo["primary_tileset"]), RAIZ)
        sec = os.path.relpath(R.caminho_tileset(alvo["secondary_tileset"]), RAIZ)
        attr = _atributos(pri, sec, base_sec=base)
        celulas = _celulas(open(os.path.join(RAIZ, alvo["blockdata_filepath"]), "rb").read())
        orfaos = {(c & 0x3FF) for c in celulas} - set(attr)
        if orfaos:
            erros.append("caso 7: %s usa %d metatiles sem atributo no dicionario "
                         "(o primeiro e o %d)" % (nome, len(orfaos), min(orfaos)))
        # o primeiro metatile do secundario tem que ler o atributo do indice
        # LOCAL 1 daquele arquivo, e nao o de um vizinho
        cru = open(os.path.join(RAIZ, sec, "metatile_attributes.bin"), "rb").read()
        alvo_attr = struct.unpack_from("<H", cru, 2)[0]
        if attr.get(base + 1) != alvo_attr:
            erros.append("caso 7: %s: o metatile %d devia ler %04X e leu %s"
                         % (nome, base + 1, alvo_attr, attr.get(base + 1)))
        # PAR NEGATIVO: com a base errada, o mesmo mapa tem que dar defeito. Sem
        # isto o caso 7 nao prova que sabe reprovar.
        if base != 512:
            errado = _atributos(pri, sec, base_sec=512)
            orfaos_errados = {(c & 0x3FF) for c in celulas} - set(errado)
            if not orfaos_errados and errado.get(base + 1) == alvo_attr:
                erros.append("caso 7: %s com a base ERRADA (512) nao acusou nada, "
                             "entao o caso nao sabe reprovar" % nome)

    for erro in erros:
        print("  VERMELHO", erro)
    print("portao_planta --demo:", "VERDE" if not erros else "VERMELHO (%d)" % len(erros))
    return 1 if erros else 0


def main():
    argv = sys.argv[1:]
    if "--demo" in argv or "--autoteste" in argv:
        return demo()
    ref = argv[argv.index("--ref") + 1] if "--ref" in argv else "master"
    ref_eventos = argv[argv.index("--ref-eventos") + 1] if "--ref-eventos" in argv else "master"
    nomes = [a for a in argv if not a.startswith("--") and a not in (ref, ref_eventos)]
    if not nomes:
        print(__doc__)
        return 2
    layouts = R.carregar_layouts()
    total = 0
    for nome in nomes:
        erros, retrato = confere_mapa(nome, ref, layouts, ref_eventos)
        if retrato:
            print("%-16s %d celulas mudadas de %d | solidificadas %d | colisao 1->0 %d | "
                  "elevacao %d | behavior %d | alcance %d -> %d | pedacos %d -> %d"
                  % (retrato["mapa"], retrato["mudadas"], retrato["celulas"],
                     retrato["solidificadas"], retrato["soltas"], retrato["elevacao"],
                     retrato["comportamento"], retrato["alcance_antes"],
                     retrato["alcance_depois"], retrato["pedacos_antes"],
                     retrato["pedacos_depois"])
                  + ("" if not retrato["pedacos_sumidos"] else
                     " | pedacos cobertos inteiros: %s" % retrato["pedacos_sumidos"]))
        for e in erros:
            print("   VERMELHO", e)
        total += len(erros)
    print("portao_planta contra %s: %s" % (ref, "VERDE" if not total else
                                           "VERMELHO (%d achados)" % total))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
