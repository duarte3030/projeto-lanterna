#!/usr/bin/env python3
"""Lê `metatile_attributes.bin` no formato CERTO do layout, e normaliza os dois.

POR QUE ESTE ARQUIVO EXISTE, e o defeito que ele fecha
------------------------------------------------------
Toda ferramenta desta árvore lia atributo de metatile como `u16`, com
comportamento na máscara `0x00FF` e `layerType` na `0xF000`. Isso está certo no
layout `emerald` (Hoenn, Sinnoh) e no `johto`, e está ERRADO no `frlg`, que é
**Kanto inteiro**, porque ali o arquivo guarda **4 bytes por metatile** e as
máscaras são outras. O motor sabe disso e a árvore não sabia: em
`src/fieldmap.c`, `GetAttributeByMetatileIdAndMapLayout` desvia para
`GetAttributeByMetatileIdAndMapLayoutFrlg` quando `mapLayout->isFrlg`, e lá o
ponteiro é lido como `const u32 *` em vez de `const u16 *`.

As máscaras, de `include/global.fieldmap.h`:

    2 bytes  METATILE_ATTR_BEHAVIOR_MASK      0x00FF       bits 0 a 7
             METATILE_ATTR_LAYER_MASK         0xF000       bits 12 a 15
    4 bytes  METATILE_ATTR_BEHAVIOR_MASK_FRLG 0x000001FF   bits 0 a 8
             METATILE_ATTR_LAYER_MASK_FRLG    0x60000000   bits 29 e 30

O estrago de ler Kanto como `u16` seria CALADO e duplo. O arquivo de
`general_frlg` tem 2.560 bytes; lido de dois em dois ele vira 1.280 "metatiles"
para 640 que existem, e cada palavra lida é METADE de um atributo de verdade.
Um portão que compara `(behavior, layerType)` célula a célula estaria comparando
lixo com lixo, e diria VERDE com a mesma cara de quem conferiu.

O QUE ELE FAZ
-------------
Devolve o atributo já **normalizado no formato do Emerald**:
`comportamento | (layerType << 12)`. Isso é seguro, e não é conveniência
preguiçosa: medido nesta árvore em 09/09/2026, os 61 tilesets `frlg` somam
10.386 metatiles com comportamento **máximo 238** (cabe nos 8 bits) e
`layerType` só 0, 1 e 2 (cabe nos 4). A normalização é conferida em tempo de
execução e levanta erro se algum dia um valor não couber, em vez de truncar
calado.

Assim toda ferramenta que já sabia mascarar `0x00FF` e `0xF000` continua valendo
sem mudar uma linha da lógica dela, e passa a estar certa nas quatro regiões.

O QUE ELE NÃO FAZ, dito na cara
-------------------------------
- Não lê os outros campos do atributo (terreno, encounter, porta, escada). Só
  comportamento e `layerType`, que são os dois que o REFINO precisa preservar.
  Medido: no `frlg` sobram bits fora dessas duas máscaras em 1.702 dos 10.386
  metatiles (`0x1000000` em 1.263, `0x2000400` em 401 e mais quatro padrões
  raros), e eles passam INTACTOS quando alguém regrava o arquivo, porque quem
  regrava deve escrever a palavra inteira e não a normalizada.
- Não escreve arquivo. Quem escreve atributo de metatile em tileset `frlg` tem
  que escrever `u32`, e usar `empacota()` daqui para montar a palavra.
- Não sabe de `bigPrimary` fora do `layouts.json`: a versão vem do
  `layout_version` do layout, que é o que o `tools/mapjson/mapjson.cpp` traduz
  em `isFrlg` e `bigPrimary`.

CUIDADO QUE FICA REGISTRADO, e que este arquivo NÃO conserta:
`dev_scripts/arte_ginasios_sinnoh.comportamento` mascara o comportamento de
2 bytes com `0x1FF` em vez de `0x00FF`, ou seja, engole o bit 8, que ali não é
comportamento. Medido: isso muda a leitura em 218 metatiles de 44.026, todos em
dois tilesets de interior de Johto (`gTileset_Lighthouse`, 144, e
`gTileset_BurnedTower`, 74). Nenhuma cidade de exterior é afetada. Não foi
consertado aqui porque aquela função é usada por vinte scripts das frentes de
Sinnoh e de Johto, que estavam rodando neste mesmo dia, e trocar a máscara
delas no meio do trabalho alheio é pior do que registrar.

Uso:
    python3 dev_scripts/atributos_metatile.py --demo
    python3 dev_scripts/atributos_metatile.py gTileset_General_Frlg
"""
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# largura em bytes, primeiro índice de metatile do secundário, paletas do
# primário, máscara e deslocamento do comportamento, máscara e deslocamento do
# layerType. Os números de 640 e 7 são `NUM_METATILES_IN_PRIMARY_FRLG` e
# `NUM_PALS_IN_PRIMARY_FRLG` de `include/fieldmap.h`.
FORMATOS = {
    "emerald": dict(largura=2, corte=512, n_pal_pri=6,
                    mask_beh=0x00FF, shift_beh=0, mask_lay=0xF000, shift_lay=12),
    "johto":   dict(largura=2, corte=640, n_pal_pri=7,
                    mask_beh=0x00FF, shift_beh=0, mask_lay=0xF000, shift_lay=12),
    "frlg":    dict(largura=4, corte=640, n_pal_pri=7,
                    mask_beh=0x01FF, shift_beh=0, mask_lay=0x60000000, shift_lay=29),
}

LAYER_NORMAL, LAYER_COVERED, LAYER_SPLIT = 0, 1, 2


def _layouts(_c={}):
    if not _c:
        d = json.load(open(os.path.join(RAIZ, "data/layouts/layouts.json"),
                           encoding="utf-8"))
        _c["l"] = d["layouts"]
    return _c["l"]


def versao_do_primario(pri, _c={}):
    """`layout_version` dos layouts que carregam este primário.

    A consulta é pelo PRIMÁRIO porque, medido nesta árvore em 09/09/2026,
    nenhum dos 2.189 layouts tem primário aparecendo com duas versões: são zero
    primários mistos e zero pares (primário, secundário) mistos. Se um dia
    tiver, esta função levanta erro em vez de escolher sozinha.
    """
    if not _c:
        for l in _layouts():
            _c.setdefault(l.get("primary_tileset"), set()).add(
                l.get("layout_version") or "emerald")
    versoes = _c.get(pri)
    if not versoes:
        return "emerald"
    if len(versoes) > 1:
        raise SystemExit("o primario %s aparece com as versoes %s; escolher uma "
                         "aqui seria chute" % (pri, sorted(versoes)))
    return next(iter(versoes))


def versao_do_tileset(label, _c={}):
    """A mesma coisa da `versao_do_primario`, mas aceitando rótulo de SECUNDÁRIO.

    Quem tem só o rótulo de um tileset (e não o layout) precisa disto para saber
    a largura do atributo dele. Medido em 09/09/2026: nenhum dos 228 pares
    (primário, secundário) desta árvore mistura versão, e nenhum tileset
    aparece dos dois lados com versões diferentes.
    """
    if not _c:
        for l in _layouts():
            v = l.get("layout_version") or "emerald"
            for campo in ("primary_tileset", "secondary_tileset"):
                if l.get(campo):
                    _c.setdefault(l[campo], set()).add(v)
    versoes = _c.get(label)
    if not versoes:
        return "emerald"
    if len(versoes) > 1:
        raise SystemExit("o tileset %s aparece com as versoes %s; escolher uma "
                         "aqui seria chute" % (label, sorted(versoes)))
    return next(iter(versoes))


def perfil(versao):
    if versao not in FORMATOS:
        raise SystemExit("layout_version desconhecida: %r" % (versao,))
    return FORMATOS[versao]


def perfil_do_layout(layout):
    return perfil((layout.get("layout_version") if layout else None) or "emerald")


def palavras(dados, versao):
    """A lista de palavras CRUAS do arquivo, na largura certa da versão."""
    p = perfil(versao)
    if len(dados) % p["largura"]:
        raise SystemExit("metatile_attributes com %d bytes nao e multiplo de %d "
                         "(layout_version %s)" % (len(dados), p["largura"], versao))
    fmt = "<H" if p["largura"] == 2 else "<I"
    return [struct.unpack_from(fmt, dados, i * p["largura"])[0]
            for i in range(len(dados) // p["largura"])]


def par(palavra, versao):
    """(comportamento, layerType) de uma palavra crua."""
    p = perfil(versao)
    return ((palavra & p["mask_beh"]) >> p["shift_beh"],
            (palavra & p["mask_lay"]) >> p["shift_lay"])


def normaliza(palavra, versao):
    """A palavra reescrita no formato do Emerald: `comportamento | layerType << 12`.

    É isso que deixa toda ferramenta que já mascarava `0x00FF` e `0xF000`
    continuar valendo em Kanto sem mudar a lógica dela.
    """
    beh, lay = par(palavra, versao)
    if beh > 0xFF or lay > 0xF:
        raise SystemExit(
            "atributo %08X do layout %s tem comportamento %d e layerType %d, e "
            "nao cabe no formato normalizado de 16 bits; a normalizacao teria "
            "que truncar, e truncar calado e o defeito que este arquivo existe "
            "para evitar" % (palavra, versao, beh, lay))
    return beh | (lay << 12)


def empacota(beh, lay, versao):
    """A palavra CRUA, na largura da versão. O inverso de `par`."""
    p = perfil(versao)
    return ((beh << p["shift_beh"]) & p["mask_beh"]) | \
           ((lay << p["shift_lay"]) & p["mask_lay"])


def _le(caminho):
    with open(caminho, "rb") as f:
        return f.read()


def tabela(pasta_pri, pasta_sec, versao, cru_pri=None, cru_sec=None, corte=None):
    """{indice_de_metatile: palavra NORMALIZADA}, com o corte certo do layout.

    `cru_pri` e `cru_sec` deixam o chamador passar o conteúdo de outro commit
    (é o que o `portao_planta.py` faz para comparar antes com depois). `corte`
    deixa o chamador que JÁ TEM o layout na mão mandar o início do secundário
    dele; sem isso, quem passasse `layout_version` errada e corte certo (ou o
    contrário) receberia a tabela deslocada em silêncio.
    """
    p = perfil(versao)
    corte = p["corte"] if corte is None else corte
    attr = {}
    for base, pasta, cru in ((0, pasta_pri, cru_pri), (corte, pasta_sec, cru_sec)):
        dados = cru if cru is not None else _le(
            os.path.join(RAIZ, pasta, "metatile_attributes.bin"))
        for i, palavra in enumerate(palavras(dados, versao)):
            attr[base + i] = normaliza(palavra, versao)
    return attr


def _pasta_de(label):
    sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
    os.environ.setdefault("REPO_MAPAS", RAIZ)
    import render_maps as R
    return os.path.relpath(R.caminho_tileset(label), RAIZ)


def demo():
    """Autoteste, com os números pregados: se a árvore mudar, isto cai."""
    mau = []

    # 1. As três versões têm o perfil que `include/fieldmap.h` diz.
    if perfil("emerald")["largura"] != 2 or perfil("emerald")["corte"] != 512:
        mau.append("perfil emerald errado")
    if perfil("johto")["largura"] != 2 or perfil("johto")["corte"] != 640:
        mau.append("perfil johto errado")
    if perfil("frlg")["largura"] != 4 or perfil("frlg")["corte"] != 640:
        mau.append("perfil frlg errado")

    # 2. A versão sai do layouts.json, e não de chute.
    for pri, esperada in (("gTileset_General", "emerald"),
                          ("gTileset_General_Frlg", "frlg"),
                          ("gTileset_JohtoSouth", "johto")):
        if versao_do_primario(pri) != esperada:
            mau.append("versao de %s: %s, esperava %s"
                       % (pri, versao_do_primario(pri), esperada))

    # 3. O TAMANHO do arquivo prova a largura, e este é o caso que mais
    #    importa: 2.560 bytes para 640 metatiles só fecha com 4 bytes.
    for label, nmeta, largura in (("gTileset_General_Frlg", 640, 4),
                                  ("gTileset_General", 512, 2),
                                  ("gTileset_JohtoGeneral", 640, 2)):
        try:
            caminho = os.path.join(RAIZ, _pasta_de(label), "metatile_attributes.bin")
            b = _le(caminho)
        except Exception as e:                                   # noqa: BLE001
            mau.append("nao consegui ler %s: %s" % (label, e))
            continue
        if len(b) != nmeta * largura:
            mau.append("%s tem %d bytes e devia ter %d (%d metatiles x %d)"
                       % (label, len(b), nmeta * largura, nmeta, largura))

    # 4. PROVA NEGATIVA: ler o arquivo de Kanto com a largura do Emerald tem que
    #    dar resultado DIFERENTE do certo. Se desse igual, a distinção que este
    #    arquivo inteiro faz seria decorativa.
    try:
        b = _le(os.path.join(RAIZ, _pasta_de("gTileset_General_Frlg"),
                             "metatile_attributes.bin"))
        certo = [par(p, "frlg") for p in palavras(b, "frlg")]
        errado = [par(p, "emerald") for p in palavras(b, "emerald")][:len(certo)]
        if len(certo) != 640:
            mau.append("general_frlg deu %d metatiles lido como frlg" % len(certo))
        if certo == errado:
            mau.append("ler general_frlg como emerald deu o MESMO resultado; a "
                       "prova negativa nao morde")
    except Exception as e:                                       # noqa: BLE001
        mau.append("prova negativa falhou: %s" % e)

    # 5. `empacota` e `par` são inversos nas três versões.
    for versao in ("emerald", "johto", "frlg"):
        for beh, lay in ((0, 0), (105, 1), (238 if versao == "frlg" else 200, 2)):
            if par(empacota(beh, lay, versao), versao) != (beh, lay):
                mau.append("empacota/par nao fecham em %s para (%d,%d)"
                           % (versao, beh, lay))

    # 6. A normalização recusa o que não cabe, em vez de truncar.
    try:
        normaliza(0x1FF, "frlg")
        mau.append("normaliza aceitou comportamento 511, e devia recusar")
    except SystemExit:
        pass

    if mau:
        print("AUTOTESTE VERMELHO")
        for m in mau:
            print("  -", m)
        return 1
    print("atributos_metatile --demo: VERDE")
    return 0


def main():
    if "--demo" in sys.argv:
        sys.exit(demo())
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    label = sys.argv[1]
    versao = versao_do_primario(label)
    pasta = _pasta_de(label)
    b = _le(os.path.join(RAIZ, pasta, "metatile_attributes.bin"))
    ps = palavras(b, versao)
    pares = [par(p, versao) for p in ps]
    print("%s: %s, %s, %d bytes, %d metatiles de %d bytes cada"
          % (label, pasta, versao, len(b), len(ps), perfil(versao)["largura"]))
    print("  comportamento de %d a %d, layerTypes %s"
          % (min(p[0] for p in pares), max(p[0] for p in pares),
             sorted({p[1] for p in pares})))
    print("  corte do secundario %d, paletas do primario %d"
          % (perfil(versao)["corte"], perfil(versao)["n_pal_pri"]))


if __name__ == "__main__":
    main()
