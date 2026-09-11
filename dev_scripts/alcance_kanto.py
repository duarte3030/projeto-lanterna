#!/usr/bin/env python3
"""Prova de ALCANCE de Kanto: porta, NPC e saída de conexão no mesmo pedaço de chão.

Uso:
    python3 dev_scripts/alcance_kanto.py                        # relatório da árvore de agora
    python3 dev_scripts/alcance_kanto.py --raiz /outra/arvore    # a mesma medida noutra árvore
    python3 dev_scripts/alcance_kanto.py --contra /outra/arvore  # diferença contra a outra
    python3 dev_scripts/alcance_kanto.py --mapa PalletTown_Frlg  # só um mapa, detalhado
    python3 dev_scripts/alcance_kanto.py --tsv saida.tsv         # a lista crua
    python3 dev_scripts/alcance_kanto.py --demo                  # autoteste, exit 1 se cair

POR QUE ESTE ARQUIVO EXISTE
---------------------------
Em 11/09/2026 a arte de Kanto inteira trocou pelo "Ikarus' Tileset Patch v3.2":
o primário `gTileset_General_Frlg`, 24 secundários e os `map.bin` dos mapas
externos. Warps, `object_event`, gatilhos e conexões NÃO foram tocados, e é
exatamente por isso que a troca é perigosa: o desenho embaixo deles mudou, e o
ponto de evento continua na mesma célula. Se o Ikarus pôs uma cerca, uma árvore
ou um penhasco onde antes era grama, a porta continua existindo, o NPC continua
existindo, e o jogador não chega em nenhum dos dois. Nada quebra no build, nada
quebra no `valida_conectividade.py` (que confere ÍNDICE de warp, não chão), e
nada quebra no `valida_warp_tile.py` (que confere o metatile DEBAIXO do warp,
não o caminho até ele). O defeito seria calado e só apareceria jogando.

`portao_planta.py` NÃO serve aqui, e isso está escrito na seção 5 do
METODO-COPIA-CIDADES.md: a planta MUDA de propósito nesta troca, então comparar
célula a célula com o desenho velho acusaria os mapas inteiros. O que tem de
continuar valendo não é o desenho, é a TOPOLOGIA: quem era alcançável a pé
continua alcançável a pé.

O QUE ELE MEDE
--------------
Para cada mapa, uma busca em largura sobre o chão andável, com a regra do motor:

- colisão dos bits 10 e 11 do `map.bin` (`MAPGRID_COLLISION_MASK`): célula com
  colisão não é pisada, ponto.
- elevação dos bits 12 a 15: duas elevações diferentes e ambas não-nulas não se
  ligam (`IsElevationMismatchAt` em `src/event_object_movement.c`). Sem isso a
  busca sobe penhasco e atravessa canal.
- ÁGUA É PAREDE. Água tem colisão 0 (quem barra é a elevação, e quem atravessa
  é o Surf), então uma busca que só olha colisão atravessa o mar e diz que a
  praia do outro lado está ligada. A lista de comportamentos de água sai do
  `include/constants/metatile_behaviors.h`, não da memória.

O comportamento do metatile segue a régua do `atributos_metatile.py`, que é
quem sabe que Kanto guarda o atributo em **4 bytes** com a máscara
`METATILE_ATTR_BEHAVIOR_MASK_FRLG` `0x1ff` (e o `layerType` na `0x60000000`), e
que o secundário começa no metatile **640** e não no 512. Ler Kanto com as
máscaras do Emerald dá lixo CALADO: o arquivo de `general_frlg` viraria 1.280
"metatiles" para 640 que existem, e cada palavra lida seria metade de um
atributo de verdade. Uma busca de alcance alimentada com isso diria VERDE com a
mesma cara de quem conferiu.

OS PONTOS QUE TÊM DE SE ALCANÇAR
--------------------------------
1. **warp**: o acesso é a própria célula do warp, se ela for andável, mais a
   célula ao SUL dela. As duas importam. Porta ANIMADA (`MB_ANIMATED_DOOR`) é
   SÓLIDA de propósito em centenas de mapas legítimos: o motor olha o tile da
   FRENTE quando o jogador anda para o norte (`TryDoorWarp` em
   `src/field_control_avatar.c`), e quem é pisado é a célula de baixo. Warp que
   não tem nenhuma das duas andável é porta inalcançável.
2. **object_event**: o NPC ocupa a célula dele e é sólido para o jogador, então
   o acesso são os quatro vizinhos andáveis, mais a própria célula (item no
   chão e bola de Pokémon são pisados, não falados). Sem nenhum, NPC ilhado.
3. **saída de conexão**: a fileira ou coluna da borda do lado que tem conexão.
   O acesso são as células andáveis dessa borda. Conexão sem nenhuma célula
   andável na borda é saída murada.

Depois, a pergunta que dá o nome ao arquivo: TODOS esses acessos caem no mesmo
componente conexo? O componente que guarda mais pontos é o PRINCIPAL; ponto que
cai fora dele é ACHADO, com a célula.

POR QUE O `--contra` É OBRIGATÓRIO NA PRÁTICA
---------------------------------------------
Mapa de verdade tem ilha legítima: praia que só se alcança surfando, área atrás
de árvore de Cut, pedra de Strength, Pokémon estático em cima d'água, a rota que
só abre depois da HM. Medido nesta árvore em 11/09/2026, Kanto tem 352 desses
ANTES da troca de arte. Uma lista crua seria ruído puro e ninguém leria.

Então o portão não é "zero achados": é "nenhum achado NOVO". `--contra` roda a
mesma medida na árvore de referência (um `git archive origin/master`, por
exemplo) e imprime só o que entrou e o que saiu. A identidade de um achado é
`(mapa, tipo, índice, x, y)`, que é estável porque os `map.json` não foram
tocados nesta troca.

O QUE ELE NÃO FAZ, dito na cara
-------------------------------
- Não sabe de HM: Cut, Rock Smash, Strength e Surf são parede para ele. Por isso
  a comparação com a árvore de referência, e não um número absoluto.
- Não sabe de `setmetatile`: mapa que abre caminho por script (muita porta de
  Hoenn, o Snorlax da Route 12) aparece fechado nas duas árvores e se cancela no
  diff.
- Não conserta nada. Achado de desenho se conserta célula a célula no `map.bin`,
  e quem decide isso é o condutor.
"""
import argparse
import collections
import json
import os
import re
import struct
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
N4 = ((0, -1), (0, 1), (-1, 0), (1, 0))

# Comportamentos que exigem Surf. Lidos do enum do repo, nunca cravados: o enum
# já cresceu nesta árvore e número copiado envelhece calado. `MB_PUDDLE` e
# `MB_SHALLOW_WATER` são água de ANDAR e ficam de fora de propósito.
NOMES_AGUA = (
    "MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_WATERFALL",
    "MB_SOOTOPOLIS_DEEP_WATER", "MB_OCEAN_WATER",
    "MB_UNUSED_SOOTOPOLIS_DEEP_WATER", "MB_NO_SURFACING",
    "MB_UNUSED_SOOTOPOLIS_DEEP_WATER_2", "MB_SEAWEED",
    "MB_SEAWEED_NO_SURFACING", "MB_FAST_WATER", "MB_CYCLING_ROAD_WATER",
)


class Arvore:
    """Tudo que a medida precisa ler de UMA árvore do repo.

    Existe como classe, e não como um punhado de funções com cache global,
    porque este script precisa ter DUAS árvores abertas ao mesmo tempo (a de
    agora e a de referência do `--contra`). Cache global aqui faria a segunda
    árvore responder com os dados da primeira, calada.
    """

    def __init__(self, raiz):
        self.raiz = os.path.abspath(raiz)
        self.layouts = {l["id"]: l for l in json.load(open(
            f"{self.raiz}/data/layouts/layouts.json", encoding="utf-8"))["layouts"]}
        self.grupos = json.load(open(f"{self.raiz}/data/maps/map_groups.json",
                                     encoding="utf-8"))
        self._mb = self._enum_comportamentos()
        self.agua = {self._mb[n] for n in NOMES_AGUA if n in self._mb}
        self._pastas = None
        self._attrs = {}
        self._mapas = {}

    # ------------------------------------------------------------- leitura crua
    def _enum_comportamentos(self):
        texto = open(f"{self.raiz}/include/constants/metatile_behaviors.h").read()
        corpo = texto[texto.index("{") + 1:texto.rindex("}")]
        valor, tabela = 0, {}
        for item in corpo.split(","):
            item = re.sub(r"/\*.*?\*/", "", re.sub(r"//.*", "", item), flags=re.S).strip()
            if not item:
                continue
            if "=" in item:
                nome, _, bruto = item.partition("=")
                nome, valor = nome.strip(), int(bruto.strip(), 0)
            else:
                nome = item
            tabela[nome] = valor
            valor += 1
        return tabela

    def pasta_do_tileset(self, tileset):
        """gTileset_X -> caminho da pasta de dados, ou None.

        Sai do INCBIN de `src/data/tilesets/metatiles.h`, que é o mesmo dado que
        o build usa, e NÃO de CamelCase -> snake_case: `gTileset_Route38Farmland`
        mora em `secondary/route38_farmland`, e adivinhar o nome descartava
        mapas inteiros calado. Resolve também o `ASSET_ALIAS` que o
        `dedupe_assets.py` deixa no lugar do INCBIN do tileset repetido.
        """
        if not tileset or tileset == "0":
            return ""
        if self._pastas is None:
            mt = open(f"{self.raiz}/src/data/tilesets/metatiles.h").read()
            sym = dict(re.findall(
                r'gMetatiles_(\w+)\[\]\s*=\s*INCBIN_U16\("(data/tilesets/\w+/\w+)/metatiles\.bin"\)',
                mt))
            for apelido, canon in re.findall(
                    r'gMetatiles_(\w+)\[[^\]]*\]\s*ASSET_ALIAS\(gMetatiles_(\w+)\)', mt):
                sym.setdefault(apelido, canon)
            for _ in range(len(sym)):
                mudou = False
                for k, v in sym.items():
                    if not v.startswith("data/") and v in sym:
                        sym[k], mudou = sym[v], True
                if not mudou:
                    break
            hdr = open(f"{self.raiz}/src/data/tilesets/headers.h").read()
            self._pastas = {}
            for nome, corpo in re.findall(
                    r'const struct Tileset gTileset_(\w+)\s*=\s*\{(.*?)\};', hdr, re.S):
                m = re.search(r'\.metatiles\s*=\s*gMetatiles_(\w+)', corpo)
                if m and m.group(1) in sym:
                    self._pastas["gTileset_" + nome] = f"{self.raiz}/{sym[m.group(1)]}"
        return self._pastas.get(tileset)

    def comportamentos(self, tileset):
        """Lista comportamento[i] do tileset, ou None se a pasta não existe.

        A LARGURA do atributo é deduzida do tamanho dos dois arquivos, não
        chutada: `metatiles.bin` gasta 16 bytes por metatile, então a divisão
        dá 2 no Emerald e 4 no FRLG. As máscaras seguem a largura:
        `METATILE_ATTR_BEHAVIOR_MASK` 0x00FF nos 2 bytes,
        `METATILE_ATTR_BEHAVIOR_MASK_FRLG` 0x01FF nos 4.
        """
        if tileset in self._attrs:
            return self._attrs[tileset]
        d = self.pasta_do_tileset(tileset)
        if d == "":
            self._attrs[tileset] = []
            return []
        if not d:
            self._attrs[tileset] = None
            return None
        pa, pm = f"{d}/metatile_attributes.bin", f"{d}/metatiles.bin"
        if not (os.path.exists(pa) and os.path.exists(pm)):
            self._attrs[tileset] = None
            return None
        n = os.path.getsize(pm) // 16
        if not n:
            self._attrs[tileset] = []
            return []
        b = open(pa, "rb").read()
        largura = len(b) // n
        if largura >= 4:
            vals = [struct.unpack_from("<I", b, i * 4)[0] & 0x1FF for i in range(n)]
        else:
            vals = [struct.unpack_from("<H", b, i * 2)[0] & 0x00FF for i in range(n)]
        self._attrs[tileset] = vals
        return vals

    def mapa(self, nome):
        if nome not in self._mapas:
            p = f"{self.raiz}/data/maps/{nome}/map.json"
            self._mapas[nome] = json.load(open(p, encoding="utf-8")) \
                if os.path.exists(p) else None
        return self._mapas[nome]

    # -------------------------------------------------------------- a geometria
    def grade(self, nome):
        """(d, L, W, H, blocos, f_comportamento) ou None se o mapa não dá para ler."""
        d = self.mapa(nome)
        if not d:
            return None
        L = self.layouts.get(d.get("layout"))
        if not L:
            return None
        bp = f"{self.raiz}/{L.get('blockdata_filepath', '')}"
        if not os.path.exists(bp):
            return None
        W, H = L["width"], L["height"]
        b = open(bp, "rb").read()
        if len(b) < W * H * 2:
            return None
        v = list(struct.unpack_from("<%dH" % (W * H), b, 0))
        pri = self.comportamentos(L.get("primary_tileset"))
        sec = self.comportamentos(L.get("secondary_tileset"))
        if pri is None or sec is None:
            return None
        # O corte primário/secundário é a CONSTANTE do motor
        # (`GetNumMetatilesInPrimary`, src/fieldmap.c), 640 no ramo grande
        # (FRLG e Johto) e 512 no Emerald, e NÃO o tamanho do arquivo do
        # primário. `gTileset_Building` tem 8 metatiles no arquivo e é primário
        # de quase todo interior; deduzir o corte do arquivo trocava o índice de
        # centenas de metatiles calado.
        corte = 640 if L.get("layout_version") in ("frlg", "johto") else 512

        def beh(mt):
            t, i = (pri, mt) if mt < corte else (sec, mt - corte)
            return t[i] if 0 <= i < len(t) else 0

        return d, L, W, H, v, beh


def componentes(W, H, v, beh, agua):
    """Rotula cada célula andável com o número do seu pedaço de chão.

    Devolve (rótulo, tamanhos): `rotulo[(x, y)]` só existe para célula andável.
    Andável = colisão 0 e comportamento fora da água. A ligação entre duas
    células ainda exige a regra de elevação do motor.
    """
    def andavel(x, y):
        c = v[y * W + x]
        return not ((c >> 10) & 3) and beh(c & 0x3FF) not in agua

    rotulo, tamanhos, atual = {}, [], 0
    for y0 in range(H):
        for x0 in range(W):
            if (x0, y0) in rotulo or not andavel(x0, y0):
                continue
            fila = collections.deque([(x0, y0)])
            rotulo[(x0, y0)] = atual
            n = 0
            while fila:
                x, y = fila.popleft()
                n += 1
                ea = (v[y * W + x] >> 12) & 0xF
                for dx, dy in N4:
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in rotulo:
                        continue
                    if not andavel(nx, ny):
                        continue
                    eb = (v[ny * W + nx] >> 12) & 0xF
                    if ea and eb and ea != eb:
                        continue
                    rotulo[(nx, ny)] = atual
                    fila.append((nx, ny))
            tamanhos.append(n)
            atual += 1
    return rotulo, tamanhos


def pontos(d, W, H):
    """Os pontos de evento do mapa e as células por onde se chega em cada um.

    Devolve lista de (tipo, índice, x, y, [células de acesso]).
    """
    fora = []
    for i, w in enumerate(d.get("warp_events") or []):
        x, y = w.get("x", 0), w.get("y", 0)
        # a própria célula (warp pisado) e a de baixo (porta animada, que é
        # sólida e larga o jogador uma casa ao sul)
        fora.append(("warp", i, x, y, [(x, y), (x, y + 1)]))
    for i, o in enumerate(d.get("object_events") or []):
        x, y = o.get("x", 0), o.get("y", 0)
        fora.append(("objeto", i, x, y,
                     [(x, y)] + [(x + dx, y + dy) for dx, dy in N4]))
    for i, c in enumerate(d.get("connections") or []):
        dirr = c.get("direction")
        if dirr == "up":
            cels = [(x, 0) for x in range(W)]
        elif dirr == "down":
            cels = [(x, H - 1) for x in range(W)]
        elif dirr == "left":
            cels = [(0, y) for y in range(H)]
        elif dirr == "right":
            cels = [(W - 1, y) for y in range(H)]
        else:
            continue                      # dive/emerge não se anda
        fora.append(("conexao:" + dirr, i, -1, -1, cels))
    return fora


def mede(arv, nome):
    """Achados do mapa: lista de (tipo, índice, x, y, motivo).

    Dois motivos, e só dois:
      SEM ACESSO   nenhuma célula de acesso é andável
      ILHADO       o acesso existe, mas cai fora do componente PRINCIPAL, que é
                   o que guarda mais pontos de evento (empate desempatado pelo
                   componente maior em células)
    """
    g = arv.grade(nome)
    if not g:
        return None
    d, L, W, H, v, beh = g
    rot, tam = componentes(W, H, v, beh, arv.agua)
    pts = pontos(d, W, H)
    se_liga = []
    for tipo, i, x, y, cels in pts:
        comps = {rot[c] for c in cels
                 if 0 <= c[0] < W and 0 <= c[1] < H and c in rot}
        se_liga.append((tipo, i, x, y, comps))
    votos = collections.Counter()
    for _, _, _, _, comps in se_liga:
        for c in comps:
            votos[c] += 1
    principal = None
    if votos:
        principal = max(votos, key=lambda c: (votos[c], tam[c], -c))
    achados = []
    for tipo, i, x, y, comps in se_liga:
        if not comps:
            achados.append((tipo, i, x, y, "SEM ACESSO"))
        elif principal is not None and principal not in comps:
            achados.append((tipo, i, x, y, "ILHADO"))
    return dict(mapa=nome, W=W, H=H, pontos=len(pts), componentes=len(tam),
                principal=principal, achados=achados)


def alvos(arv, primarios, grupos_extra=()):
    """Os mapas a medir: os que carregam um dos primários pedidos.

    `grupos_extra` aceita pedaço de nome de grupo, para varrer também os
    interiores de Kanto, que têm primário próprio (`gTileset_BuildingFrlg` e
    parentes) mas grupo `*_Frlg`.
    """
    fora = []
    for g in arv.grupos["group_order"]:
        casa_grupo = any(t.lower() in g.lower() for t in grupos_extra)
        for m in arv.grupos.get(g, []):
            d = arv.mapa(m)
            if not d:
                continue
            L = arv.layouts.get(d.get("layout"))
            if not L:
                continue
            if L.get("primary_tileset") in primarios or casa_grupo:
                fora.append((g, m))
    return fora


def roda(raiz, primarios, grupos_extra, so=None):
    arv = Arvore(raiz)
    fora, mudos = {}, []
    for g, m in alvos(arv, primarios, grupos_extra):
        if so and m != so:
            continue
        r = mede(arv, m)
        if r is None:
            mudos.append(m)
            continue
        r["grupo"] = g
        fora[m] = r
    return fora, mudos


def chave(m, a):
    return (m, a[0], a[1], a[2], a[3])


def demo():
    """Autoteste da régua, com mutação plantada numa grade sintética.

    Não toca no repositório: monta um `map.bin` de mentira e cobra que cada uma
    das três regras do motor separe o chão do jeito certo. Uma busca que só
    olhasse colisão passaria nos três casos e mesmo assim mentiria em Kanto.
    """
    W = H = 5

    def grade(paredes=(), elev=None, agua=()):
        v = []
        for y in range(H):
            for x in range(W):
                c = 1 if (x, y) in agua else 0
                col = 1 if (x, y) in paredes else 0
                e = (elev or {}).get((x, y), 3)
                v.append(c | (col << 10) | (e << 12))
        return v

    def beh(mt):
        return 21 if mt == 1 else 0          # 21 é MB_OCEAN_WATER na régua abaixo

    ag = {21}
    # 1. sem parede nenhuma, o chão inteiro é um pedaço só
    rot, tam = componentes(W, H, grade(), beh, ag)
    assert len(tam) == 1 and tam[0] == 25, (tam,)
    # 2. COLISÃO parte o mapa em dois
    parede = {(2, y) for y in range(H)}
    rot, tam = componentes(W, H, grade(paredes=parede), beh, ag)
    assert sorted(tam) == [10, 10], (tam,)
    # 3. ELEVAÇÃO diferente e não-nula também parte, sem nenhuma colisão
    elev = {(x, y): (3 if x < 2 else 5) for y in range(H) for x in range(W)}
    rot, tam = componentes(W, H, grade(elev=elev), beh, ag)
    assert sorted(tam) == [10, 15], (tam,)
    # 4. ÁGUA é parede: sem isso a busca atravessa o mar e diz que a praia do
    #    outro lado está ligada. É o caso que custou cinco NPCs em Cianwood.
    mar = {(2, y) for y in range(H)}
    rot, tam = componentes(W, H, grade(agua=mar), beh, ag)
    assert sorted(tam) == [10, 10], (tam,)
    # 5. o warp de porta ANIMADA é sólido de propósito, e quem é pisado é o
    #    tile ao sul: os dois entram como acesso
    d = dict(warp_events=[dict(x=1, y=1)], object_events=[], connections=[])
    pts = pontos(d, W, H)
    assert pts[0][4] == [(1, 1), (1, 2)], pts
    # 6. o NPC é sólido para o jogador: o acesso são os quatro vizinhos
    d = dict(warp_events=[], object_events=[dict(x=2, y=2)], connections=[])
    assert set(pontos(d, W, H)[0][4]) == {(2, 2), (2, 1), (2, 3), (1, 2), (3, 2)}
    print("demo ok")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--raiz", default=os.path.dirname(AQUI))
    p.add_argument("--contra", default=None,
                   help="árvore de referência; imprime só a DIFERENÇA")
    p.add_argument("--mapa", default=None)
    p.add_argument("--primario", action="append", default=None)
    p.add_argument("--grupo", action="append", default=None,
                   help="pedaço de nome de grupo a varrer inteiro")
    p.add_argument("--tsv", default=None)
    p.add_argument("--demo", action="store_true")
    a = p.parse_args()
    if a.demo:
        return demo()

    primarios = set(a.primario or ["gTileset_General_Frlg"])
    grupos = tuple(a.grupo or [])

    atual, mudos = roda(a.raiz, primarios, grupos, a.mapa)
    print("árvore  %s" % a.raiz)
    print("mapas   %d medidos, %d mudos (sem layout ou sem blockdata)"
          % (len(atual), len(mudos)))
    if mudos:
        print("        mudos: %s" % ", ".join(sorted(mudos)[:10]))
    total = sum(len(r["achados"]) for r in atual.values())
    print("achados %d em %d mapas"
          % (total, sum(1 for r in atual.values() if r["achados"])))

    if a.tsv:
        with open(a.tsv, "w", encoding="utf-8") as f:
            f.write("mapa\ttipo\tindice\tx\ty\tmotivo\n")
            for m in sorted(atual):
                for t, i, x, y, mot in atual[m]["achados"]:
                    f.write("%s\t%s\t%d\t%d\t%d\t%s\n" % (m, t, i, x, y, mot))
        print("tsv     %s" % a.tsv)

    if a.contra:
        ref, _ = roda(a.contra, primarios, grupos, a.mapa)
        agora = {chave(m, x): x[4] for m in atual for x in atual[m]["achados"]}
        antes = {chave(m, x): x[4] for m in ref for x in ref[m]["achados"]}
        novos = sorted(k for k in agora if k not in antes)
        sumidos = sorted(k for k in antes if k not in agora)
        mudou = sorted(k for k in agora if k in antes and agora[k] != antes[k])
        print("\nCONTRA  %s" % a.contra)
        print("  antes %d achados, agora %d" % (len(antes), len(agora)))
        print("  NOVOS %d" % len(novos))
        for k in novos:
            print("    %-34s %-16s #%d (%d,%d)  %s"
                  % (k[0], k[1], k[2], k[3], k[4], agora[k]))
        print("  sumidos %d" % len(sumidos))
        for k in sumidos:
            print("    %-34s %-16s #%d (%d,%d)  %s"
                  % (k[0], k[1], k[2], k[3], k[4], antes[k]))
        if mudou:
            print("  mudaram de motivo %d" % len(mudou))
            for k in mudou:
                print("    %-34s %-16s #%d (%d,%d)  %s -> %s"
                      % (k[0], k[1], k[2], k[3], k[4], antes[k], agora[k]))
        return 1 if novos else 0

    if a.mapa:
        for m in sorted(atual):
            r = atual[m]
            print("\n%s  %dx%d  %d pontos  %d componentes"
                  % (m, r["W"], r["H"], r["pontos"], r["componentes"]))
            for t, i, x, y, mot in r["achados"]:
                print("    %-16s #%d (%d,%d)  %s" % (t, i, x, y, mot))
    else:
        for m in sorted(atual):
            for t, i, x, y, mot in atual[m]["achados"]:
                print("  %-34s %-16s #%d (%d,%d)  %s" % (m, t, i, x, y, mot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
