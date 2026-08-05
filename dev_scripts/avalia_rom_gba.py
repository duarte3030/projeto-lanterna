#!/usr/bin/env python3
"""Diz se um hack de GBA tem uma REGIÃO de verdade ou só troca de nome.

Uso:
    python3 dev_scripts/avalia_rom_gba.py rom.gba [rom2.gba ...]

Por que existe: apareceram vários hacks prometendo região nova, e olhar screenshot
não distingue "Paldea implementada" de "Kanto com os NPCs dizendo Paldea". Este
script decide por evidência, em três testes independentes:

  1. Nomes de lugar no texto. Região de verdade tem os nomes das cidades dela em
     quantidade; hack de fachada tem só o nome da região solto em fala.
  2. Tabela de nomes de lugar. Se os nomes aparecem CONTÍGUOS no binário, é a
     tabela de MAPSEC, ou seja, região registrada no motor.
  3. Quantidade e TAMANHO dos mapas. Ler a tabela de bancos e medir largura e
     altura de cada layout separa região nova de mapa reaproveitado.

Caso real que motivou: um hack de "Scarlet/Violet" tinha 43 bancos, exatamente os
do FireRed, zero nomes de cidade de Paldea, e "PALDEA" só aparecia em fala do
tipo "hai salvato PALDEA". Era Kanto. Outro, de Sword/Shield, tinha as 10 cidades
de Galar contíguas numa tabela e mapas de até 100x47. Esse era real.
"""
import os
import statistics
import struct
import sys

REGIOES = {
    "Galar": ["POSTWICK", "WEDGEHURST", "MOTOSTOKE", "TURFFIELD", "HULBURY",
              "HAMMERLOCKE", "HAMMMELOCK", "STOW ON SIDE", "BALLONLEA",
              "CIRCHESTER", "SPIKEMUTH", "WYNDON", "GLIMWOOD", "WILD AREA"],
    "Paldea": ["MESAGOZA", "CORTONDO", "ARTAZON", "LEVINCIA", "CASCARRAFA",
               "MEDALI", "MONTENEVERA", "ALFORNADA", "GLASEADO", "ZAPAPICO",
               "PORTO MARINADA", "LOS PLATOS", "AREA ZERO"],
    "Sinnoh": ["TWINLEAF", "SANDGEM", "JUBILIFE", "OREBURGH", "FLOAROMA",
               "ETERNA", "HEARTHOME", "VEILSTONE", "PASTORIA", "CANALAVE",
               "SNOWPOINT", "SUNYSHORE", "SOLACEON", "CELESTIC"],
    "Johto": ["NEW BARK", "CHERRYGROVE", "VIOLET", "AZALEA", "GOLDENROD",
              "ECRUTEAK", "OLIVINE", "CIANWOOD", "MAHOGANY", "BLACKTHORN"],
    "Unova": ["NUVEMA", "ACCUMULA", "STRIATON", "NACRENE", "CASTELIA",
              "NIMBASA", "DRIFTVEIL", "MISTRALTON", "ICIRRUS", "OPELUCID"],
    "Kalos": ["VANIVILLE", "AQUACORDE", "SANTALUNE", "LUMIOSE", "CAMPHRIER",
              "CYLLAGE", "AMBRETTE", "GEOSENGE", "SHALOUR", "COUMARINE",
              "LAVERRE", "DENDEMILLE", "ANISTAR", "COURIWAY", "SNOWBELLE",
              "KILOUDE"],
    "Kanto (controle)": ["PALLET", "VIRIDIAN", "PEWTER", "CERULEAN", "LAVENDER",
                         "CELADON", "FUCHSIA", "SAFFRON", "CINNABAR"],
    "Hoenn (controle)": ["LITTLEROOT", "OLDALE", "PETALBURG", "RUSTBORO",
                         "DEWFORD", "SLATEPORT", "MAUVILLE", "LILYCOVE"],
}

BASES = {"BPRE": "FireRed", "BPEE": "Emerald", "BPGE": "LeafGreen",
         "AXVE": "Ruby", "AXPE": "Sapphire"}
# ponteiro da tabela de bancos de mapa, por base
TABELA_BANCOS = {"FireRed": 0x5524C, "LeafGreen": 0x5524C, "Emerald": 0x84AA4,
                 "Ruby": 0x53324, "Sapphire": 0x53324}


def charmap():
    cm = {0x00: " ", 0xAD: ".", 0xAE: "-", 0xB8: ",", 0xBA: "/",
          0xAB: "!", 0xAC: "?", 0xFF: "\n"}
    for i in range(10):
        cm[0xA1 + i] = str(i)
    for i in range(26):
        cm[0xBB + i] = chr(ord("A") + i)
    for i in range(26):
        cm[0xD5 + i] = chr(ord("a") + i)
    return cm


def texto_da_rom(b):
    cm = charmap()
    return "".join(cm.get(c, "\x00") for c in b).upper()


def mapas(b, base):
    """(qtd_bancos, qtd_mapas, lista de (largura, altura))."""
    off = TABELA_BANCOS.get(base)
    if off is None:
        return 0, 0, []
    N = len(b)

    def ptr(o):
        if o + 4 > N:
            return None
        v = struct.unpack_from("<I", b, o)[0]
        return v - 0x08000000 if 0x08000000 <= v < 0x08000000 + N else None

    p = ptr(off)
    if p is None:
        return 0, 0, []
    bancos = []
    for i in range(200):
        v = ptr(p + i * 4)
        if v is None:
            break
        bancos.append(v)
    dims, total = [], 0
    for i, ini in enumerate(bancos):
        fim = bancos[i + 1] if i + 1 < len(bancos) else ini + 4 * 250
        for j in range((fim - ini) // 4):
            mh = ptr(ini + j * 4)
            if mh is None:
                break
            total += 1
            lay = ptr(mh)
            if lay is None or lay + 8 > N:
                continue
            w, h = struct.unpack_from("<II", b, lay)
            if 1 <= w <= 500 and 1 <= h <= 500:
                dims.append((w, h))
    return len(bancos), total, dims


def contigua(t, nomes):
    """Os nomes aparecem juntos num trecho curto? Isso é tabela de MAPSEC."""
    pos = [t.find(n) for n in nomes]
    pos = sorted(p for p in pos if p >= 0)
    if len(pos) < 4:
        return False, 0
    # a maior sequência dentro de uma janela de 2 KB
    melhor = 1
    for i in range(len(pos)):
        j = i
        while j + 1 < len(pos) and pos[j + 1] - pos[i] < 2048:
            j += 1
        melhor = max(melhor, j - i + 1)
    return melhor >= 4, melhor


def avalia(caminho):
    b = open(caminho, "rb").read()
    cod = b[0xAC:0xB0].decode("ascii", "replace")
    base = BASES.get(cod, "?")
    print(f"\n{'='*70}\n{os.path.basename(caminho)}")
    print(f"  base {base} ({cod}), {len(b)/1048576:.0f} MB")
    t = texto_da_rom(b)

    print("  nomes de lugar encontrados:")
    for reg, nomes in REGIOES.items():
        achados = [(n, t.count(n)) for n in nomes if t.count(n)]
        if not achados:
            continue
        junto, seq = contigua(t, nomes)
        marca = f"  TABELA CONTIGUA de {seq} nomes" if junto else ""
        print(f"    {reg:<18} {len(achados)}/{len(nomes)} nomes, "
              f"{sum(n for _, n in achados)} ocorrencias{marca}")

    nb, nm, dims = mapas(b, base)
    if dims:
        areas = sorted(w * h for w, h in dims)
        grandes = [d for d in dims if d[0] * d[1] > 1500]
        print(f"  mapas: {nm} em {nb} bancos; medidos {len(dims)}, "
              f"area mediana {statistics.median(areas):.0f} tiles, "
              f"maior {max(areas)}, {len(grandes)} acima de 1500 tiles")
        print(f"    referencia: FireRed original tem ~418 mapas em 43 bancos")
    else:
        print(f"  mapas: nao consegui ler a tabela de bancos desta base")


def demo():
    if len(sys.argv) < 2:
        print(__doc__)
        # autoteste do que nao depende de arquivo
        t = "AAAMESAGOZA" + "x" * 100 + "CORTONDO" + "x" * 100 + "ARTAZON" + "x" * 50 + "MEDALI"
        junto, seq = contigua(t, REGIOES["Paldea"])
        assert junto and seq >= 4, "deteccao de tabela contigua quebrada"
        assert not contigua("MESAGOZA" + "x" * 9000 + "CORTONDO", REGIOES["Paldea"])[0]
        print("autoteste passou")
        return
    for c in sys.argv[1:]:
        avalia(c)


if __name__ == "__main__":
    demo()
