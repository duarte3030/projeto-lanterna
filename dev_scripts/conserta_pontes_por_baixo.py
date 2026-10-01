#!/usr/bin/env python3
"""Conserta a ponte desenhada por baixo: quem passa por baixo some, quem passa por cima fica por cima.

O DEFEITO (playtest do Gui, 30/09/2026)
--------------------------------------
"Logo fora do Pokémon Center tinha uns viadutos de bicicleta e estava tudo
bugado: eu andava e subia no viaduto." Era a Cycling Road da Route 206, ao sul
de Eterna. O motor estava certo: as 271 células do tabuleiro sobre o vale são
elevação 15 (`ELEVATION_MULTI_LEVEL`), o idioma de ponte do Emerald, por onde
o jogador do chão (3) passa por BAIXO e o de bicicleta (4) passa por CIMA. O
desenho é que estava pela metade: o tabuleiro inteiro vinha na camada de BAIXO
dos metatiles 680, 681, 682, 688 e 689 do `gTileset_Sunnyshore`, com a de cima
vazia. A camada de baixo de um metatile NORMAL vai para o Bg2, abaixo de todo
sprite, e o jogador de elevação 3 aparecia de pé em cima da ciclovia.

A regra E5 do `mapas_qa.py` (`pontes_por_baixo`) acha a mesma coisa em toda
célula de cruzamento que dois andares pisam e cujo metatile não cobre quem
passa por baixo: 0 no vanilla, 503 no master de 30/09/2026, todas em Sinnoh
(Route 206, 207, 208, 210 Norte, 212 Sul, 215, Sunyshore) e 3 no ginásio de
Goldenrod. O idioma certo, o das Routes 110, 119 e 120 do vanilla, é o
tabuleiro na camada de CIMA de um metatile NORMAL: ela vai para o Bg1
(prioridade 1); o andador de elevação 3 tem sprite de prioridade 2 e some
debaixo da ponte; o de elevação 4 tem prioridade 1 e, empatado com o Bg1, é
desenhado por cima.

O CONSERTO, em quatro passos, nenhum com coordenada cravada além da tabela
`ELEVACAO_PAR`:

  1. Ponte com tabuleiro em elevação ÍMPAR não tem conserto de desenho: o
     sprite de elevação 5 também tem prioridade 2 e sumiria junto. A Route 210
     Norte tem o planalto inteiro em 5; ele vira 6 (prioridade 1). Troca de
     rótulo, não de caminho: o mapa não tem nenhuma célula 6, nenhum evento em
     5 e nenhuma célula 5 encosta na borda de uma conexão, e a ferramenta
     recusa se qualquer uma dessas três coisas deixar de ser verdade.
  2. Para cada metatile acusado, uma de duas cirurgias:
       COVERED com o tabuleiro em cima -> o tipo vira NORMAL;
       NORMAL com a camada de cima vazia -> o tabuleiro sobe para a de cima e a
       de baixo recebe o chão mais comum em volta (o tabuleiro tem os 256 px
       opacos, então o chão nunca aparece; ele existe para a célula não virar
       o "bloco preto" do E3, que é camada de cima cheia sobre baixo vazia).
  3. A cirurgia é feita NO PRÓPRIO metatile quando nenhuma outra célula que o
     usa, em nenhum layout, é pisada por um andar de prioridade 2 (ela também
     passaria a cobrir esse andador). Quando alguma é, o metatile é CLONADO
     numa vaga provada livre do mesmo tileset (nenhum layout, borda ou rótulo
     METATILE_ a usa, e as 16 entradas são zero) e só as células acusadas
     passam a apontar para o clone.
  4. Objeto parado numa célula de cruzamento com elevação de molde de
     prioridade 2 está NO TABULEIRO (os ciclistas da Route 206, o Hiker da 208
     e o Black Belt da 215): o molde passa para o andar de cima, senão ele
     sumiria debaixo da própria ponte (`ObjectEventUpdateElevation` não mexe na
     elevação em cima de célula 15, e a prioridade do sprite sai da elevação
     anterior, que é a do molde). Objeto que uma cena move (`applymovement`
     com o local_id dele) fica como está e sai no relatório: o Rival de
     Sunyshore em (26,10) entra correndo POR BAIXO da passarela, de propósito.

USO
---
    python3 dev_scripts/conserta_pontes_por_baixo.py             # relatório, não grava
    python3 dev_scripts/conserta_pontes_por_baixo.py --aplica    # grava
    python3 dev_scripts/conserta_pontes_por_baixo.py --verifica  # exit 1 se sobrar E5
    python3 dev_scripts/conserta_pontes_por_baixo.py --demo      # autoteste
"""
import json
import os
import re
import struct
import sys
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "qa"))
import mapas_qa as Q  # noqa: E402

REPO = os.path.dirname(AQUI)

# mapa -> (elevação de hoje, elevação nova). Ver o passo 1 do cabeçalho.
ELEVACAO_PAR = {"Route210_North": (5, 6)}

PRIO = Q.PRIO_DA_ELEVACAO
TIPO_NORMAL, TIPO_COVERED = 0, 1


def palavra(m, c, e):
    return (m & 0x3FF) | ((c & 3) << 10) | ((e & 0xF) << 12)


class Obra:
    """O estado em memória: grades, metatiles e atributos, gravados no fim."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.A = Q.Arvore(raiz)
        self.grades = {}           # lid -> [linhas] mutáveis
        self.meta = {}             # ts -> bytearray
        self.attr = {}             # ts -> bytearray
        self.mapas = {}            # nome -> (caminho, json)
        for n in sorted(os.listdir(os.path.join(raiz, "data/maps"))):
            p = os.path.join(raiz, "data/maps", n, "map.json")
            if os.path.exists(p):
                self.mapas[n] = (p, json.load(open(p, encoding="utf-8")))
        self.objetos_mudados = set()
        self.log = []

    # -- leitura ----------------------------------------------------------
    def grade(self, lid):
        if lid not in self.grades:
            g = self.A.grade(lid)
            if not g:
                return None
            self.grades[lid] = [list(l) for l in g[2]]
        return self.grades[lid]

    def dims(self, lid):
        L = self.A.layouts[lid]
        return L["width"], L["height"]

    def corte(self, lid):
        return self.A.grade(lid)[3]

    def ts_do(self, lid, mt):
        L = self.A.layouts[lid]
        c = self.corte(lid)
        return (L["primary_tileset"], mt) if mt < c else (L["secondary_tileset"], mt - c)

    def bins(self, ts):
        if ts not in self.meta:
            d = self.A.pastas()[ts]
            self.meta[ts] = bytearray(open(os.path.join(d, "metatiles.bin"), "rb").read())
            self.attr[ts] = bytearray(open(os.path.join(d, "metatile_attributes.bin"), "rb").read())
            assert len(self.attr[ts]) * 8 == len(self.meta[ts]), \
                f"{ts}: só o atributo de 2 bytes (Emerald) é tratado aqui"
        return self.meta[ts], self.attr[ts]

    def entradas(self, ts, idx):
        m, _ = self.bins(ts)
        return list(struct.unpack_from("<8H", m, idx * 16))

    def tipo(self, ts, idx):
        _, a = self.bins(ts)
        return struct.unpack_from("<H", a, idx * 2)[0] >> 12

    def opacos(self, ts_pri, ts_sec, entradas4, corte):
        tp = self.A.tiles_opacos(ts_pri), self.A.tiles_opacos(ts_sec)
        n = 0
        for v in entradas4:
            it = v & 0x3FF
            lista, j = (tp[0], it) if it < corte else (tp[1], it - corte)
            n += lista[j] if 0 <= j < len(lista) else 0
        return n

    def desenho(self, lid, mt):
        """Como `Arvore.desenho_do_metatile`, mas lendo os bins EM MEMÓRIA."""
        L = self.A.layouts[lid]
        ts, idx = self.ts_do(lid, mt)
        if ts not in self.A.pastas() or idx >= len(self.bins(ts)[0]) // 16:
            return None            # tileset sem pasta ou id fora do teto: é o E1
        e = self.entradas(ts, idx)
        c = self.corte(lid)
        pb = self.opacos(L["primary_tileset"], L["secondary_tileset"], e[:4], c)
        pc = self.opacos(L["primary_tileset"], L["secondary_tileset"], e[4:], c)
        iguais = sum(1 for q in range(4) if e[q] == e[4 + q])
        return (pb, pc, iguais, self.tipo(ts, idx))

    def layouts_do_tileset(self, ts):
        return [lid for lid, L in self.A.layouts.items()
                if ts in (L.get("primary_tileset"), L.get("secondary_tileset"))
                and self.A.grade(lid)]

    def mapas_do_layout(self, lid):
        return [n for n, (_, d) in self.mapas.items() if d.get("layout") == lid]

    # -- E5 em memória -----------------------------------------------------
    def acusados(self, lid):
        lin = self.grade(lid)
        if lin is None:
            return {}
        W, H = self.dims(lid)
        r = {}
        for (x, y), es in Q.cruzamentos(W, H, lin).items():
            if Q.ponte_nao_cobre(self.desenho(lid, lin[y][x] & 0x3FF)):
                r[(x, y)] = es
        return r


# ------------------------------------------------------------------ passo 1
def troca_elevacao(ob, nome, de, para):
    caminho, d = ob.mapas[nome]
    lid = d["layout"]
    lin = ob.grade(lid)
    W, H = ob.dims(lid)
    if any(Q.elev(v) == para for row in lin for v in row):
        raise SystemExit(f"{nome}: já existe célula de elevação {para}; a troca juntaria andares")
    for k in ("object_events", "coord_events", "bg_events", "warp_events"):
        for e in d.get(k) or []:
            if str(e.get("elevation")) in (str(de), str(para)):
                raise SystemExit(f"{nome}: {k} em ({e.get('x')},{e.get('y')}) tem elevação "
                                 f"{e.get('elevation')}; decidir à mão antes")
    bordas = {"up": lambda x, y: y == 0, "down": lambda x, y: y == H - 1,
              "left": lambda x, y: x == 0, "right": lambda x, y: x == W - 1}
    n = 0
    for y in range(H):
        for x in range(W):
            v = lin[y][x]
            if Q.elev(v) != de:
                continue
            for c in d.get("connections") or []:
                if Q.andavel(v) and bordas[c["direction"]](x, y):
                    raise SystemExit(f"{nome}: ({x},{y}) em {de} encosta na conexão com "
                                     f"{c['map']}; o vizinho continuaria em {de}")
            lin[y][x] = palavra(v & 0x3FF, (v >> 10) & 3, para)
            n += 1
    ob.log.append(f"{nome}: {n} células de elevação {de} viram {para} (troca de rótulo)")
    return n


# ------------------------------------------------------------------ passo 2/3
def andar_dos_vizinhos(lin, W, H, andares, x, y):
    r = set()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H:
            r |= {e for e in andares.get((nx, ny), ()) if e not in (0, 15)}
    return r


def perigos(ob, ts, idx, acusadas):
    """Células que NÃO são cruzamento acusado e passariam a cobrir um andador."""
    r = []
    for lid in ob.layouts_do_tileset(ts):
        lin = ob.grade(lid)
        W, H = ob.dims(lid)
        c = ob.corte(lid)
        L = ob.A.layouts[lid]
        alvo = idx if ts == L["primary_tileset"] and idx < c else None
        if ts == L["secondary_tileset"]:
            alvo = idx + c
        if alvo is None:
            continue
        andares = None
        for y in range(H):
            for x in range(W):
                if lin[y][x] & 0x3FF != alvo or (lid, x, y) in acusadas:
                    continue
                if andares is None:
                    andares = Q.andares_por_celula(W, H, lin)
                es = {e for e in andares.get((x, y), ()) if e != 0}
                if Q.elev(lin[y][x]) == 0:
                    es |= andar_dos_vizinhos(lin, W, H, andares, x, y)
                if any(PRIO[e] == 2 for e in es):
                    r.append((L.get("name"), x, y, sorted(es)))
    return r


def rotulos_metatile(raiz):
    p = os.path.join(raiz, "include/constants/metatile_labels.h")
    return open(p).read() if os.path.exists(p) else ""


def vaga_livre(ob, ts, ja_usadas):
    usados = set()
    for lid in ob.layouts_do_tileset(ts):
        L = ob.A.layouts[lid]
        c = ob.corte(lid)
        sec = ts == L["secondary_tileset"]
        palavras = [v for row in ob.grade(lid) for v in row]
        bp = os.path.join(ob.raiz, L.get("border_filepath", ""))
        if os.path.isfile(bp):
            b = open(bp, "rb").read()
            palavras += [struct.unpack_from("<H", b, i)[0] for i in range(0, len(b), 2)]
        for v in palavras:
            mt = v & 0x3FF
            if sec and mt >= c:
                usados.add(mt - c)
            elif not sec and mt < c:
                usados.add(mt)
    # O rótulo METATILE_<Tileset>_* cita o id GLOBAL: o do primário é o próprio
    # índice, o do secundário soma o corte (512 no Emerald, 640 no FRLG).
    rot = rotulos_metatile(ob.raiz)
    nome_ts = ts.replace("gTileset_", "")
    citados = {int(v, 0) for v in re.findall(
        r"#define\s+METATILE_%s_\w+\s+(0x[0-9A-Fa-f]+|\d+)" % re.escape(nome_ts), rot)}
    # `setmetatile x, y, 809` com número cru também é uso; conservador: qualquer
    # script do repo que cite o id global tira a vaga.
    for raiz_inc, _, arqs in os.walk(os.path.join(ob.raiz, "data")):
        for a in arqs:
            if a.endswith(".inc"):
                txt = open(os.path.join(raiz_inc, a), encoding="utf-8", errors="replace").read()
                citados |= {int(v, 0) for v in re.findall(
                    r"setmetatile\s+[^,\n]+,\s*[^,\n]+,\s*(0x[0-9A-Fa-f]+|\d+)\b", txt)}
    m, _ = ob.bins(ts)
    livres = [i for i in range(1, len(m) // 16)
              if i not in usados and i not in ja_usadas
              and not ({i, i + 512, i + 640} & citados)]
    # Vaga de 16 entradas zero primeiro (nada a perder); se não houver, a
    # primeira sem uso nenhum, que é o "reuso provado" da 0.ap.
    for i in livres:
        if not any(ob.entradas(ts, i)):
            return i
    if livres:
        return livres[0]
    raise SystemExit(f"{ts}: nenhuma vaga provada livre para clonar")


def chao_em_volta(ob, lid, celulas, andar_baixo):
    lin = ob.grade(lid)
    W, H = ob.dims(lid)
    cont = Counter()
    for (x, y) in celulas:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H:
                v = lin[ny][nx]
                if Q.andavel(v) and Q.elev(v) in andar_baixo:
                    cont[v & 0x3FF] += 1
    for mt, _ in cont.most_common():
        ts, idx = ob.ts_do(lid, mt)
        if ob.tipo(ts, idx) == TIPO_NORMAL:
            return mt, ob.entradas(ts, idx)[:4]
    raise SystemExit(f"{lid}: sem chão comum em volta de {sorted(celulas)[:3]}")


def nova_definicao(ob, lid, ts, idx, celulas, andar_baixo):
    """(8 entradas, tipo) da versão que cobre quem passa por baixo."""
    e = ob.entradas(ts, idx)
    t = ob.tipo(ts, idx)
    d = ob.desenho(lid, ts_global(ob, lid, ts, idx))
    if t == TIPO_COVERED:
        return e, TIPO_NORMAL, "COVERED vira NORMAL (o tabuleiro já está na camada de cima)"
    assert d[1] == 0, f"{ts}#{idx}: NORMAL com camada de cima não vazia não é acusado"
    mt_chao, baixo = chao_em_volta(ob, lid, celulas, andar_baixo)
    return baixo + e[:4], t, f"tabuleiro sobe para a camada de cima; embaixo o chão do metatile {mt_chao}"


def ts_global(ob, lid, ts, idx):
    L = ob.A.layouts[lid]
    return idx if ts == L["primary_tileset"] and idx < ob.corte(lid) else idx + ob.corte(lid)


def grava_metatile(ob, ts, idx, entradas8, tipo):
    m, a = ob.bins(ts)
    struct.pack_into("<8H", m, idx * 16, *entradas8)
    v = struct.unpack_from("<H", a, idx * 2)[0]
    struct.pack_into("<H", a, idx * 2, (v & 0x0FFF) | (tipo << 12))


def planeja_e_aplica(ob):
    for nome, (de, para) in ELEVACAO_PAR.items():
        troca_elevacao(ob, nome, de, para)

    # quem é acusado, agrupado por metatile do tileset
    por_mt = defaultdict(list)          # (ts, idx) -> [(lid, x, y, andares)]
    acusadas = set()
    sem_conserto = []
    for lid in sorted(ob.A.layouts):
        for (x, y), es in sorted(ob.acusados(lid).items()):
            # Conserto de desenho só existe se há quem passe por CIMA
            # (prioridade 1) e quem passe por BAIXO (prioridade 2).
            if not (any(PRIO[e] == 1 for e in es) and any(PRIO[e] == 2 for e in es)):
                sem_conserto.append((ob.A.layouts[lid].get("name"), x, y, sorted(es)))
                continue
            mt = ob.grade(lid)[y][x] & 0x3FF
            por_mt[ob.ts_do(lid, mt)].append((lid, x, y, es))
            acusadas.add((lid, x, y))
    if sem_conserto:
        raise SystemExit("cruzamento sem conserto de desenho (andar de cima com prioridade 2): "
                         + str(sem_conserto[:6]))

    vagas = defaultdict(set)
    for (ts, idx), cels in sorted(por_mt.items()):
        lid0 = cels[0][0]
        baixo = {e for _, _, _, es in cels for e in es if PRIO[e] == 2}
        # O chão em volta é medido na PONTE inteira do layout (o miolo do
        # tabuleiro não encosta em chão nenhum).
        celulas = [(x, y) for (l, x, y) in acusadas if l == lid0]
        entradas8, tipo, como = nova_definicao(ob, lid0, ts, idx, celulas, baixo)
        risco = perigos(ob, ts, idx, acusadas)
        if not risco:
            grava_metatile(ob, ts, idx, entradas8, tipo)
            ob.log.append(f"{ts} #{idx}: no lugar, {len(cels)} células; {como}")
            continue
        novo = vaga_livre(ob, ts, vagas[ts])
        vagas[ts].add(novo)
        m, a = ob.bins(ts)
        a_orig = struct.unpack_from("<H", a, idx * 2)[0]
        struct.pack_into("<H", a, novo * 2, a_orig)
        grava_metatile(ob, ts, novo, entradas8, tipo)
        for lid, x, y, _ in cels:
            lin = ob.grade(lid)
            v = lin[y][x]
            novo_global = novo + (ob.corte(lid) if ts == ob.A.layouts[lid]["secondary_tileset"] else 0)
            lin[y][x] = palavra(novo_global, (v >> 10) & 3, Q.elev(v))
        ob.log.append(f"{ts} #{idx}: CLONE em #{novo} para {len(cels)} células ({como}); "
                      f"no lugar cobriria {len(risco)} célula(s) de andar de prioridade 2, "
                      f"ex. {risco[0]}")

    # passo 4: treinador no tabuleiro
    andares_de = {(lid, x, y): es for cels in por_mt.values() for lid, x, y, es in cels}
    for lid in sorted({l for l, _, _ in andares_de}):
        for nome in ob.mapas_do_layout(lid):
            caminho, d = ob.mapas[nome]
            for o in d.get("object_events") or []:
                es = andares_de.get((lid, o.get("x"), o.get("y")))
                if not es:
                    continue
                p = (o.get("x"), o.get("y"))
                e_molde = int(o.get("elevation", 0))
                if PRIO[e_molde] == 1:
                    continue
                cima = max(e for e in es if PRIO[e] == 1)
                sc = os.path.join(os.path.dirname(caminho), "scripts.inc")
                cena = (o.get("local_id") and os.path.exists(sc) and re.search(
                    r"applymovement\s+%s\b" % re.escape(o["local_id"]),
                    open(sc, encoding="utf-8").read()))
                if not cena:
                    o["elevation"] = cima
                    ob.objetos_mudados.add(nome)
                    ob.log.append(f"{nome}: {o.get('graphics_id')} em {p} sobe do molde "
                                  f"{e_molde} para {cima} (parado no tabuleiro)")
                else:
                    ob.log.append(f"{nome}: {o.get('graphics_id')} em {p} fica com o molde "
                                  f"{e_molde} (anda por cena; decidir pela cena, não pela célula)")


def grava(ob):
    for lid, lin in ob.grades.items():
        L = ob.A.layouts[lid]
        orig = ob.A.grade(lid)[2]
        if lin == orig:
            continue
        p = os.path.join(ob.raiz, L["blockdata_filepath"])
        open(p, "wb").write(b"".join(struct.pack(f"<{len(r)}H", *r) for r in lin))
    for ts in ob.meta:
        d = ob.A.pastas()[ts]
        open(os.path.join(d, "metatiles.bin"), "wb").write(bytes(ob.meta[ts]))
        open(os.path.join(d, "metatile_attributes.bin"), "wb").write(bytes(ob.attr[ts]))
    for nome in sorted(ob.objetos_mudados):
        caminho, d = ob.mapas[nome]
        txt = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
        open(caminho, "w", encoding="utf-8").write(txt)


def restantes(raiz):
    A = Q.Arvore(raiz)
    r = []
    for lid in sorted(A.layouts):
        for x, y, mt, es in Q.pontes_por_baixo(A, lid):
            r.append((A.layouts[lid].get("name"), x, y, mt, es))
    return r


# ---------------------------------------------------------------------- demo
def demo():
    # (1) célula 15 entre chão 3 e tabuleiro 4 é cruzamento; com um andar só, não
    e3, e4, e15 = 3 << 12, 4 << 12, 15 << 12
    linhas = [[e3, e15, e3],
              [e4, e15, e4]]
    cz = Q.cruzamentos(3, 2, linhas)
    assert set(cz) == {(1, 0), (1, 1)} and cz[(1, 0)] == {3, 4}, cz
    assert Q.cruzamentos(3, 1, [[e3, e15, e3]]) == {}, "um andar só não é ponte"
    # (2) a célula 0 zera a elevação: depois dela qualquer andar entra
    e0 = 0
    assert Q.andares_por_celula(3, 1, [[e3, e0, e4]])[(2, 0)] == {4, 0} or \
        4 in Q.andares_por_celula(3, 1, [[e3, e0, e4]])[(2, 0)]
    # (3) o critério de "não cobre": COVERED sempre; NORMAL só com cima vazia
    assert Q.ponte_nao_cobre((256, 256, 0, 1))
    assert Q.ponte_nao_cobre((256, 0, 0, 0))
    assert not Q.ponte_nao_cobre((0, 256, 0, 0)), "o tabuleiro da Route 110 cobre"
    assert not Q.ponte_nao_cobre((256, 80, 0, 0)), "cima parcial não é acusada"
    # (4) a tabela de prioridade é a do motor (src/event_object_movement.c)
    fonte = open(os.path.join(REPO, "src/event_object_movement.c")).read()
    m = re.search(r"sElevationToPriority\[\]\s*=\s*\{([^}]*)\}", fonte)
    assert tuple(int(v) for v in m.group(1).replace("\n", "").split(",") if v.strip()) == PRIO
    # (5) a palavra do map.bin: metatile 10 bits, colisão 2, elevação 4
    v = palavra(681, 0, 15)
    assert v & 0x3FF == 681 and (v >> 10) & 3 == 0 and v >> 12 == 15
    print("demo ok")
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    if "--verifica" in sys.argv:
        r = restantes(REPO)
        print(f"E5 restantes: {len(r)}")
        for it in r[:20]:
            print("  ", it)
        return 1 if r else 0
    antes = restantes(REPO)
    print(f"E5 antes: {len(antes)} células em "
          f"{len({n for n, *_ in antes})} layouts")
    ob = Obra(REPO)
    planeja_e_aplica(ob)
    for l in ob.log:
        print("  " + l)
    if "--aplica" not in sys.argv:
        print("\n(relatório; nada gravado. --aplica grava)")
        return 0
    grava(ob)
    depois = restantes(REPO)
    print(f"\nE5 depois: {len(depois)}")
    for it in depois[:20]:
        print("  ", it)
    return 1 if depois else 0


if __name__ == "__main__":
    sys.exit(main() or 0)
