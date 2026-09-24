#!/usr/bin/env python3
"""Corta o FIM VAZIO dos arquivos de metatile dos pares de tileset copiados dos
ROM hacks (`*_copia_pri` e `*_copia_sec`), sem mudar um pixel.

POR QUE EXISTE
--------------
A `copia_cidade.py` grava o primário inteiro (640 metatiles, 10.240 B de
`metatiles.bin` e 1.280 B de atributo) e o secundário inteiro (384, 6.144 B e
768 B), mesmo quando o mapa usa 30 deles. O resto é zero, e ocupa ROM: uma
clareira de 38 metatiles custava ~22 KB. Aprovado pelo Fable em 23/09/2026 como
passo separado, depois do merge do pacote GS Chronicles (ESTADO 0.an).

POR QUE CORTAR O FIM É SEGURO, e o que obriga a guardar
--------------------------------------------------------
O motor não copia `metatiles.bin` para a VRAM: ele lê `gMetatiles_*[i]` e
`gMetatileAttributes_*[i]` pelo ponteiro, só para o índice i que alguma célula
pede. Índice que ninguém pede nunca é lido. Por isso o corte guarda TODO índice
que pode ser pedido, e não só os do `map.bin`:

  1. todo índice de todo layout que usa o tileset (e a borda dele);
  2. todo índice de todo mapa LIGADO por conexão a um mapa que usa o tileset:
     o motor desenha a faixa do vizinho com os tilesets do mapa ATUAL
     (METODO-COPIA-CIDADES 3), então o índice do vizinho é lido aqui;
  3. todo número de `setmetatile` nos scripts dos mapas que usam o tileset.

O arquivo fica com (maior índice pedido + 1) metatiles, e nunca com zero.

Uso:
    python3 dev_scripts/corta_metatiles_vazios.py            # só mede
    python3 dev_scripts/corta_metatiles_vazios.py --aplicar
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N_PRI = 640   # layout_version "johto": bigPrimary


def pasta(rotulo):
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", rotulo.replace("gTileset_", "")).lower()
    s = re.sub(r"[^a-z0-9_]", "_", s)
    for lado in ("primary", "secondary"):
        p = os.path.join(REPO, "data/tilesets", lado, s)
        if os.path.isdir(p):
            return p
    raise SystemExit("ERRO: pasta de %s não achada" % rotulo)


def indices(caminho):
    d = open(os.path.join(REPO, caminho), "rb").read()
    return {struct.unpack_from("<H", d, i)[0] & 0x3FF for i in range(0, len(d) - 1, 2)}


def main():
    aplicar = "--aplicar" in sys.argv
    layouts = [l for l in json.load(open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]
               if l.get("id")]
    por_id = {l["id"]: l for l in layouts}
    mapas = {}
    for n in os.listdir(os.path.join(REPO, "data/maps")):
        p = os.path.join(REPO, "data/maps", n, "map.json")
        if os.path.isfile(p):
            mapas[n] = json.load(open(p, encoding="utf-8"))
    por_const = {m["id"]: n for n, m in mapas.items()}
    alvos = sorted({l[k] for l in layouts for k in ("primary_tileset", "secondary_tileset")
                    if "Copia" in l[k]})
    total_antes = total_depois = 0
    for t in alvos:
        secundario = t.endswith("Sec")
        lays = [l for l in layouts if t in (l["primary_tileset"], l["secondary_tileset"])]
        if any(l.get("layout_version") != "johto" for l in lays):
            raise SystemExit("ERRO: %s é usado por layout que não é 'johto'" % t)
        pedidos = set()
        for l in lays:
            pedidos |= indices(l["blockdata_filepath"]) | indices(l["border_filepath"])
        usam = [n for n, m in mapas.items() if m.get("layout") in {l["id"] for l in lays}]
        for n in usam:
            for c in (mapas[n].get("connections") or []):
                viz = por_const.get(c["map"])
                if viz:
                    lv = por_id[mapas[viz]["layout"]]
                    pedidos |= indices(lv["blockdata_filepath"])
            sc = os.path.join(REPO, "data/maps", n, "scripts.inc")
            if os.path.isfile(sc):
                for num in re.findall(r"setmetatile\s+\d+\s*,\s*\d+\s*,\s*(\w+)", open(sc).read()):
                    try:
                        pedidos.add(int(num, 0))
                    except ValueError:
                        raise SystemExit("ERRO: setmetatile com constante em %s: %s" % (n, num))
        if secundario:
            locais = [i - N_PRI for i in pedidos if i >= N_PRI]
        else:
            locais = [i for i in pedidos if i < N_PRI]
        n_quer = max(locais) + 1 if locais else 1
        p = pasta(t)
        meta = open(os.path.join(p, "metatiles.bin"), "rb").read()
        attr = open(os.path.join(p, "metatile_attributes.bin"), "rb").read()
        n_tem = len(meta) // 16
        if len(attr) // 2 != n_tem:
            raise SystemExit("ERRO: %s tem %d metatiles e %d atributos" % (t, n_tem, len(attr) // 2))
        n_final = min(n_tem, n_quer)
        if any(meta[n_final * 16:]) and n_final < n_tem:
            # não corta desenho: o que sai tem de ser zero (e o atributo também)
            raise SystemExit("ERRO: %s tem metatile NÃO vazio depois do %d" % (t, n_final))
        antes = len(meta) + len(attr)
        depois = n_final * 18
        total_antes += antes
        total_depois += depois
        print("%-52s %4d -> %4d metatiles  %6d -> %6d B" % (t, n_tem, n_final, antes, depois))
        if aplicar and n_final < n_tem:
            open(os.path.join(p, "metatiles.bin"), "wb").write(meta[:n_final * 16])
            open(os.path.join(p, "metatile_attributes.bin"), "wb").write(attr[:n_final * 2])
    print("total: %d -> %d B (%d B a menos nos arquivos)" % (total_antes, total_depois, total_antes - total_depois))
    return 0


if __name__ == "__main__":
    sys.exit(main())
