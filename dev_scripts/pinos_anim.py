#!/usr/bin/env python3
"""Diz QUAIS vagas de tile do secundário a animação sobrescreve em tempo de execução.

Por que existe, e o defeito que ele evita. O `compacta_tileset.py` renumera as
vagas de tile de um secundário e o `compacta_paletas.py` reindexa os nibbles de
pixel. Os dois são seguros contra tudo que está DENTRO dos arquivos do tileset,
porque tudo que está dentro é remapeado junto. Só que o `src/tileset_anims.c`
escreve tile CRU direto na VRAM, numa vaga FIXA calculada como
`NUM_TILES_IN_PRIMARY + N`, e ele não sabe que a numeração mudou. Renumerar por
baixo dele não quebra o build, não muda um pixel do render estático e só aparece
DENTRO do jogo, quando a fonte de Jubilife começa a piscar com o desenho errado.
É exatamente a classe de erro do risco 1 da seção 6 do `PRD-REFINO.md`: falha em
silêncio, devolvendo dado plausível e errado.

Por isso os dois compactadores recusavam qualquer tileset com `.callback`, o que
é grosso demais nos dois sentidos. Grosso para MENOS: `gTileset_PetalburgSinnoh`
e `gTileset_LilycoveSinnoh` TÊM `.callback`, mas a função de init deles põe
`sSecondaryTilesetAnimCallback = NULL`, ou seja não escrevem vaga nenhuma, e
estavam sendo recusados à toa. Grosso para MAIS: quando a animação existe de
verdade, "recusa tudo" não diz ao próximo agente QUAIS vagas são intocáveis, e
ele fica sem saber onde pode instalar o kit de arte.

O QUE ELE FAZ. Lê o `src/data/tilesets/headers.h` para achar o `.callback` do
tileset, lê o `src/tileset_anims.c` e segue a cadeia:

    InitTilesetAnim_X  ->  sSecondaryTilesetAnimCallback = TilesetAnim_X (ou NULL)
    TilesetAnim_X      ->  as funções QueueAnimTiles_* que ele chama
    QueueAnimTiles_*   ->  os AppendTilesetAnimToBuffer(origem, destino, tamanho)

e de cada `AppendTilesetAnimToBuffer` tira o par (vaga inicial, número de tiles).
O destino aparece de duas formas, e as duas são tratadas:

  - literal:  `(u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + 448))`
  - por array: `gTilesetAnims_Rustboro_WindyWater_VDests[modulo]`, e aí o array
    é lido inteiro, porque o índice é o timer e em algum quadro ele passa por
    todas as entradas.

O tamanho vem do terceiro argumento, `K * TILE_SIZE_4BPP`, que dá K vagas
seguidas a partir da inicial.

COMO ELE PODE ERRAR, e o que fazer com isso:

  - Ele lê C com expressão regular, não com compilador. Uma animação escrita de
    outro jeito (destino calculado em variável, laço, ponteiro passado adiante)
    sai como ZERO pinos e o tileset passaria a ser compactado como se fosse
    seguro. Por isso o `--demo` prega os dois casos conhecidos do repositório
    (Rustboro e Mauville) com o número na mão: se o parser deixar de achá-los,
    o auto-teste fica vermelho antes de alguém confiar nele.
  - Ele só cobre animação de TILE. `BlendAnimPalette_*` (Battle Dome) mexe em
    PALETA em tempo de execução e não entra nesta conta; nenhum tileset de
    exterior de Sinnoh usa isso, e o `--todos` imprime o aviso quando encontra.
  - `NUM_TILES_IN_PRIMARY` é a fronteira do layout `emerald` (512). Tileset de
    layout `frlg` ou `johto` usa outra fronteira, mas o número que este script
    devolve é sempre LOCAL ao secundário (a vaga dentro do `tiles.png`), que é
    a unidade com que os dois compactadores trabalham, então a fronteira não
    entra na conta.

Uso:
    python3 dev_scripts/pinos_anim.py gTileset_RustboroSinnoh
    python3 dev_scripts/pinos_anim.py --todos      # varre o headers.h inteiro
    python3 dev_scripts/pinos_anim.py --demo       # auto-teste
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADERS = os.path.join(RAIZ, "src", "data", "tilesets", "headers.h")
ANIMS = os.path.join(RAIZ, "src", "tileset_anims.c")

# Os dois casos conhecidos do repositório, medidos na mão em 08/09/2026 lendo o
# `src/tileset_anims.c`. Servem de gabarito para o `--demo`; se o parser deixar
# de reproduzir estes números, ele está quebrado e o auto-teste acusa.
GABARITO = {
    "gTileset_Rustboro": set(range(128, 160)) | set(range(448, 452)),
    "gTileset_RustboroSinnoh": set(range(128, 160)) | set(range(448, 452)),
    "gTileset_Mauville": set(range(96, 160)),
    "gTileset_MauvilleSinnoh": set(range(96, 160)),
    "gTileset_PetalburgSinnoh": set(),
    "gTileset_LilycoveSinnoh": set(),
    "gTileset_Celestic": set(),
    "gTileset_Jubilife": set(),
}


def _texto(caminho):
    return open(caminho, encoding="utf-8").read()


def callback_do_tileset(rotulo, headers=None):
    """Devolve o nome da função de `.callback`, ou None se for NULL/ausente."""
    texto = headers if headers is not None else _texto(HEADERS)
    marca = "const struct Tileset %s =" % rotulo
    i = texto.find(marca)
    if i < 0:
        return None
    corpo = texto[i:texto.find("};", i)]
    achado = re.search(r"\.callback\s*=\s*(\w+)", corpo)
    if not achado:
        return None
    nome = achado.group(1)
    return None if nome == "NULL" else nome


def _corpo_da_funcao(texto, nome):
    """Corpo de `nome`, achado por contagem de chave. None se não existir."""
    achado = re.search(r"\b%s\s*\([^)]*\)\s*\{" % re.escape(nome), texto)
    if not achado:
        return None
    i = achado.end() - 1
    nivel = 0
    for j in range(i, len(texto)):
        if texto[j] == "{":
            nivel += 1
        elif texto[j] == "}":
            nivel -= 1
            if nivel == 0:
                return texto[i + 1:j]
    return None


def _vagas_do_array(texto, nome, primario=False):
    """Vagas de destino declaradas num array VDests.

    No secundario o destino e escrito `NUM_TILES_IN_PRIMARY + N` e N ja e a vaga
    LOCAL. No primario ele e um literal, `TILE_OFFSET_4BPP(496)`, e a vaga local
    e o proprio literal.
    """
    achado = re.search(r"\b%s\s*\[\s*\]\s*=\s*\{(.*?)\};" % re.escape(nome),
                       texto, re.S)
    if not achado:
        return []
    corpo = achado.group(1)
    if primario:
        return [int(n) for n in re.findall(
            r"TILE_OFFSET_4BPP\s*\(\s*(\d+)\s*\)", corpo)]
    return [int(n) for n in re.findall(r"NUM_TILES_IN_PRIMARY\s*\+\s*(\d+)",
                                       corpo)]


def _appends(corpo, texto, primario=False):
    """Pares (vaga_inicial, n_tiles) de cada AppendTilesetAnimToBuffer do corpo."""
    pares = []
    for chamada in re.finditer(
            r"AppendTilesetAnimToBuffer\s*\((.*?)\)\s*;", corpo, re.S):
        args = chamada.group(1)
        tamanho = re.search(r"(\d+)\s*\*\s*TILE_SIZE_4BPP", args)
        n = int(tamanho.group(1)) if tamanho else 1
        if primario:
            literais = [v for v in re.findall(
                r"TILE_OFFSET_4BPP\s*\(\s*(\d+)\s*\)", args)]
        else:
            literais = re.findall(r"NUM_TILES_IN_PRIMARY\s*\+\s*(\d+)", args)
        if literais:
            pares += [(int(v), n) for v in literais]
            continue
        for nome_array in re.findall(r"\b(\w*VDests)\s*\[", args):
            pares += [(v, n) for v in _vagas_do_array(texto, nome_array, primario)]
    return pares


def pinos_de_anim(rotulo, headers=None, anims=None):
    """(vagas_pinadas, ativa, explicacao) para um tileset.

    `vagas_pinadas` são LOCAIS ao secundário: a vaga dentro do `tiles.png`.
    `ativa` é False quando não há `.callback` ou quando a função de init põe
    `sSecondaryTilesetAnimCallback = NULL`, que é o caso de Petalburg e Lilycove.
    """
    texto_h = headers if headers is not None else _texto(HEADERS)
    texto_c = anims if anims is not None else _texto(ANIMS)

    init = callback_do_tileset(rotulo, texto_h)
    if init is None:
        return set(), False, "sem .callback no headers.h"

    corpo_init = _corpo_da_funcao(texto_c, init)
    if corpo_init is None:
        return set(), False, "%s declarado no headers.h e nao achado no tileset_anims.c" % init

    # O mesmo init serve para primário e secundário, e o campo que ele preenche
    # é o que diz de qual dos dois o tileset é. Ler os dois: um primário cujo
    # init só mexe no ponteiro secundário existe (Petalburg, Lilycove) e é
    # justamente o caso "tem .callback e não anima nada".
    atribui = re.search(r"s(Primary|Secondary)TilesetAnimCallback\s*=\s*(\w+)\s*;",
                        corpo_init)
    if not atribui or atribui.group(2) == "NULL":
        campo = ("s%sTilesetAnimCallback" % atribui.group(1)) if atribui \
            else "sSecondaryTilesetAnimCallback"
        return set(), False, ("%s poe %s = NULL: nao escreve vaga nenhuma em "
                              "tempo de execucao" % (init, campo))

    primario = atribui.group(1) == "Primary"
    passo = atribui.group(2)
    corpo_passo = _corpo_da_funcao(texto_c, passo)
    if corpo_passo is None:
        return set(), True, "%s nao achado no tileset_anims.c" % passo

    pares = list(_appends(corpo_passo, texto_c, primario))
    chamadas = set(re.findall(r"\b(QueueAnimTiles_\w+|BlendAnimPalette_\w+)\s*\(",
                              corpo_passo))
    avisos = []
    for chamada in sorted(chamadas):
        if chamada.startswith("BlendAnimPalette"):
            avisos.append("%s mexe em PALETA em tempo de execucao e esta conta "
                          "so cobre TILE" % chamada)
            continue
        corpo_fila = _corpo_da_funcao(texto_c, chamada)
        if corpo_fila is None:
            avisos.append("%s nao achado" % chamada)
            continue
        pares += _appends(corpo_fila, texto_c, primario)

    vagas = set()
    for inicio, n in pares:
        vagas |= set(range(inicio, inicio + n))

    explicacao = "%s -> %s (%s), %d destinos, %d vagas" % (
        init, passo, "primario" if primario else "secundario", len(pares), len(vagas))
    if avisos:
        explicacao += "; AVISO: " + "; ".join(avisos)
    return vagas, True, explicacao


def faixas(vagas):
    """'128-159, 448-451', para caber numa linha de relatório."""
    if not vagas:
        return "nenhuma"
    saida, comeco, anterior = [], None, None
    for v in sorted(vagas):
        if comeco is None:
            comeco = anterior = v
        elif v == anterior + 1:
            anterior = v
        else:
            saida.append("%d-%d" % (comeco, anterior) if comeco != anterior else str(comeco))
            comeco = anterior = v
    saida.append("%d-%d" % (comeco, anterior) if comeco != anterior else str(comeco))
    return ", ".join(saida)


def todos_os_rotulos(headers=None):
    texto = headers if headers is not None else _texto(HEADERS)
    return re.findall(r"const struct Tileset (gTileset_\w+) =", texto)


def demo():
    """Auto-teste: o parser tem que reproduzir o gabarito medido na mão."""
    texto_h, texto_c = _texto(HEADERS), _texto(ANIMS)
    erros = []

    for rotulo, esperado in sorted(GABARITO.items()):
        if "const struct Tileset %s =" % rotulo not in texto_h:
            erros.append("caso 1: %s nao existe no headers.h" % rotulo)
            continue
        vagas, ativa, _ = pinos_de_anim(rotulo, texto_h, texto_c)
        if vagas != esperado:
            erros.append("caso 1: %s deu %s e o gabarito diz %s"
                         % (rotulo, faixas(vagas), faixas(esperado)))
        if bool(esperado) != ativa:
            erros.append("caso 1: %s tem anim ativa=%s e o gabarito esperava %s"
                         % (rotulo, ativa, bool(esperado)))

    # caso 2, prova negativa: com o array de destinos apagado, Rustboro tem que
    # PERDER as 32 vagas de agua. Sem isso "achou as vagas certas" nao vale,
    # porque um parser que devolvesse a faixa fixa passaria no caso 1.
    sabotado = re.sub(r"u16 \*const gTilesetAnims_Rustboro_WindyWater_VDests\[\] = \{.*?\};",
                      "u16 *const gTilesetAnims_Rustboro_WindyWater_VDests[] = {};",
                      texto_c, flags=re.S)
    if sabotado == texto_c:
        erros.append("caso 2: a sabotagem nao encontrou o array; o teste nao vale")
    else:
        vagas, _, _ = pinos_de_anim("gTileset_RustboroSinnoh", texto_h, sabotado)
        if vagas & set(range(128, 160)):
            erros.append("caso 2: com o array de destinos vazio o parser ainda "
                         "devolveu as vagas 128-159: ele nao esta lendo o array")
        if not (vagas & set(range(448, 452))):
            erros.append("caso 2: a sabotagem no array levou junto a fonte, que "
                         "e literal e devia continuar aparecendo")

    # caso 3, prova negativa: init que poe NULL nao pode devolver pino nenhum.
    trocado = texto_c.replace("sSecondaryTilesetAnimCallback = TilesetAnim_Rustboro;",
                              "sSecondaryTilesetAnimCallback = NULL;")
    if trocado == texto_c:
        erros.append("caso 3: a sabotagem nao encontrou a atribuicao")
    else:
        vagas, ativa, _ = pinos_de_anim("gTileset_RustboroSinnoh", texto_h, trocado)
        if vagas or ativa:
            erros.append("caso 3: com o callback em NULL o parser ainda devolveu "
                         "%s (ativa=%s)" % (faixas(vagas), ativa))

    for erro in erros:
        print("  VERMELHO", erro)
    print("pinos_anim --demo:", "VERDE" if not erros else "VERMELHO (%d)" % len(erros))
    return 1 if erros else 0


def main():
    argv = sys.argv[1:]
    if "--demo" in argv or "--autoteste" in argv:
        return demo()
    if "--todos" in argv:
        rotulos = todos_os_rotulos()
    else:
        rotulos = [a for a in argv if not a.startswith("--")]
    if not rotulos:
        print(__doc__)
        return 2
    texto_h, texto_c = _texto(HEADERS), _texto(ANIMS)
    for rotulo in rotulos:
        vagas, ativa, explicacao = pinos_de_anim(rotulo, texto_h, texto_c)
        if not ativa and "--todos" in argv and not vagas:
            continue
        print("%-32s anim=%-5s vagas de tile pinadas: %s"
              % (rotulo, "SIM" if ativa else "nao", faixas(vagas)))
        print("%-32s %s" % ("", explicacao))
    return 0


if __name__ == "__main__":
    sys.exit(main())
