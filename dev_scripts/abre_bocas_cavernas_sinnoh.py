#!/usr/bin/env python3
"""Desenha a BOCA das cavernas que ja estao convertidas e nao tinham entrada.

    python3 dev_scripts/abre_bocas_cavernas_sinnoh.py            # so relata
    python3 dev_scripts/abre_bocas_cavernas_sinnoh.py --aplicar  # escreve
    python3 dev_scripts/abre_bocas_cavernas_sinnoh.py --demo     # autoteste

O buraco que ele fecha
----------------------
`converte_cavernas_sinnoh.py` converte a geometria de 16 cavernas do Platinum e
so poe na ROM as que tem um tile de porta ORFA no mapa pai. Sobraram 16 destinos
com a planta pronta e sem entrada, e caverna sem entrada nao entra.

Este script nao cria mapa nenhum: ele so abre o tile de entrada no PAI. Depois
dele, `converte_cavernas_sinnoh.py --aplicar` acha a porta e cria as cavernas
pelo caminho que ja existia. Duas ferramentas, cada uma com um trabalho.

Onde a boca pode nascer
-----------------------
Dois casos, e a diferenca esta no dado, nao no gosto:

1. **O pai tambem saiu da grade 2D do Platinum** (`origem` do map.json diz
   "convertida"). Ai a coordenada da fonte vale AQUI, tile a tile, porque os
   dois lados sao a mesma grade. A escada entra na coordenada exata do warp
   deles, conferida andavel. Vale para Mt. Coronet 2F, Wayward Cave 1F,
   Snowpoint Temple 1F e Victory Road 1F Room 3.

2. **O pai e mapa nosso, de outra geometria** (rota, cidade, floresta, margem de
   lago). Coordenada de rua no Platinum e global da matriz de Sinnoh e nao
   existe offset que alinhe (mesma armadilha da decisao 5 do importador de NPC).
   Entao a posicao sai por ANCORA: o mesmo mapa ja tem warp para destino que o
   Platinum tambem tem (Route214 -> Ruin Maniac Cave Short, Solaceon -> a
   creche), e o delta entre os dois pares da a translacao local. A boca vai no
   candidato valido mais perto da estimativa.

Um tile so vira boca se, medido no nosso `map.bin`:

- ele esta BLOQUEADO hoje (nao se rouba chao andavel do jogador),
- tem chao andavel logo ABAIXO, que e por onde se entra numa porta,
- os vizinhos de cima, de esquerda e de direita tambem estao bloqueados, ou
  seja, e o meio de uma parede e nao a quina de uma arvore solta,
- a mancha bloqueada dele tem area >= 8.

Mancha que contem `MB_MOUNTAIN_TOP` ganha das outras: e penhasco, o lugar certo
de uma boca de caverna. Em floresta nao ha penhasco nenhum, e ai a boca sai no
meio do macico de arvore, que e onde o Platinum poe o Old Chateau.

E a palavra que se escreve?
---------------------------
A mesma regra de `abre_portas_extras_sinnoh.py`: **a palavra de 16 bits e
COPIADA de outro warp do mesmo mapa**, entao desenho, colisao, elevacao e
comportamento ja sao os de uma porta que o motor aceita. Nada de metatile
escolhido de cabeca. Quando o mapa nao tem nenhum warp em tile de porta de
verdade (a margem de Acuity tem UM warp, e ele esta em cima de areia, warp morto
que nunca disparou), cai no 0x00A7, que e a palavra medida da entrada da Ruin
Maniac Cave em Route214, no mesmo tileset primario `gTileset_GeneralSinnoh`.

Layout compartilhado
--------------------
`SpearPillar` usa `LAYOUT_SKY_PILLAR_TOP`, que e o Sky Pillar de HOENN. Desenhar
nele mudaria Hoenn. Ai o layout e CLONADO (entrada nova no fim de layouts.json,
copia de map.bin e border.bin) e so a copia e furada.

Compatibilidade de save: layout novo no FIM de layouts.json, warp novo no FIM da
lista do mapa. Nenhum indice antigo anda; o warp em si quem cria e o
`converte_cavernas_sinnoh.py`.
"""
import json
import os
import shutil
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import abre_portas_extras_sinnoh as A   # noqa: E402
import converte_cavernas_sinnoh as C    # noqa: E402
import fecha_portas_sinnoh as F         # noqa: E402
import importa_npcs_sinnoh as I         # noqa: E402
import valida_warp_tile as W            # noqa: E402

APLICAR = "--aplicar" in sys.argv

# Palavra da entrada da Ruin Maniac Cave em Route214, medida do map.bin: mt 167
# do tileset primario `gTileset_GeneralSinnoh`, MB_NON_ANIMATED_DOOR. Serve de
# ultimo recurso quando o pai nao tem nenhum warp em tile de porta de verdade.
BOCA_PADRAO = 0x00A7
MOUNTAIN = W._MB["MB_MOUNTAIN_TOP"]


# ------------------------------------------------------------------ leitura
def alvos_pendentes():
    """[(pai, header_do_filho, [(x,z) da fonte])] das cavernas sem entrada."""
    heads = I.headers_do_platinum()
    saida = []
    for pai, filho in C.alvos():
        larg, alt, grade = C.grade_do_header(filho)
        if not grade:
            continue
        if C.chao_de_caverna(grade) < 8:
            continue                      # nao e caverna de verdade
        d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        ph = header_do_mapa(pai, d, heads)
        coords = []
        if ph:
            pe = os.path.join(C.PLAT, "res/field/events", heads[ph][0] + ".json")
            if os.path.exists(pe):
                coords = [(int(w["x"]), int(w["z"]))
                          for w in json.load(open(pe)).get("warp_events", [])
                          if w["dest_header_id"] == filho]
        saida.append((pai, filho, coords, d))
    return saida


def header_do_mapa(pasta, d, heads):
    """MAP_HEADER_* do Platinum que casa com um mapa nosso, ou None."""
    alvo = d.get("id")
    for h in heads:
        if F.const_do_header(h) == alvo:
            return h
    por_chave = {I.chave(h): h for h in heads}
    return I.APELIDOS.get(pasta) or por_chave.get(I.chave(pasta))


def convertido_do_ds(d):
    return "convertida" in (d.get("origem") or "")


# ------------------------------------------------------------- candidatos
def manchas(w, h, pal, comp):
    """indice do tile -> (area da mancha bloqueada, tem penhasco)."""
    col = [((p >> 10) & 3) != 0 for p in pal]
    saida = {}
    visto = bytearray(w * h)
    for i0 in range(w * h):
        if visto[i0] or not col[i0]:
            continue
        pilha, corpo, penhasco = [i0], [], False
        visto[i0] = 1
        while pilha:
            i = pilha.pop()
            corpo.append(i)
            if comp(pal[i]) == MOUNTAIN:
                penhasco = True
            x, y = i % w, i // w
            for j, ok in ((i - 1, x > 0), (i + 1, x + 1 < w),
                          (i - w, y > 0), (i + w, y + 1 < h)):
                if ok and not visto[j] and col[j]:
                    visto[j] = 1
                    pilha.append(j)
        for i in corpo:
            saida[i] = (len(corpo), penhasco)
    return saida


def candidatos(mapa):
    """[(x, y, penhasco, area)] onde uma boca de caverna pode nascer."""
    d, _lay, w, h, pal, comp = A._grade(mapa)
    col = lambda i: ((pal[i] >> 10) & 3) != 0                 # noqa: E731
    porta = lambda i: comp(pal[i]) in W.COMPORTA_WARP          # noqa: E731
    ja = {(e["x"], e["y"]) for e in (d.get("warp_events") or [])}
    mm = manchas(w, h, pal, comp)
    saida = []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            i = y * w + x
            if not col(i) or porta(i) or (x, y) in ja:
                continue
            if col(i + w) or porta(i + w):
                continue                  # sem chao andavel logo abaixo
            if not (col(i - w) and col(i - 1) and col(i + 1)):
                continue                  # nao e o meio de uma parede
            area, penhasco = mm.get(i, (0, False))
            if area < 8:
                continue
            saida.append((x, y, penhasco, area))
    return saida


def ancoras(mapa, d, heads):
    """[(plat_x, plat_z, nosso_x, nosso_y)] de destinos que os dois lados tem."""
    ph = header_do_mapa(mapa, d, heads)
    if not ph:
        return []
    pe = os.path.join(C.PLAT, "res/field/events", heads[ph][0] + ".json")
    if not os.path.exists(pe):
        return []
    deles = {}
    for wp in json.load(open(pe)).get("warp_events", []):
        deles.setdefault(wp["dest_header_id"], (int(wp["x"]), int(wp["z"])))
    saida = []
    for wp in d.get("warp_events") or []:
        for header, (px, pz) in deles.items():
            if F.const_do_header(header) == wp["dest_map"]:
                saida.append((px, pz, wp["x"], wp["y"]))
                break
    return saida


def escolhe(cands, anc, alvo):
    """O candidato que a fonte pede, ou o melhor que existe.

    Com ancora, a posicao sai por translacao local (ver o topo). Sem ancora, ou
    sem coordenada de fonte, ganha penhasco, depois mancha maior: e o criterio
    honesto, porque nao ha de onde tirar a posicao.
    """
    if not cands:
        return None
    if alvo and anc:
        px, pz = alvo
        ax, az, ox, oy = min(anc, key=lambda a: (a[0] - px) ** 2 + (a[1] - pz) ** 2)
        nx, ny = ox + (px - ax), oy + (pz - az)
        return min(cands, key=lambda c: ((c[0] - nx) ** 2 + (c[1] - ny) ** 2,
                                         not c[2]))
    return max(cands, key=lambda c: (c[2], c[3], -c[1], -c[0]))


# ------------------------------------------------------------------ escrita
def clona_layout(mapa, d):
    """Copia o layout do mapa para uso exclusivo dele, e devolve o id novo.

    So faz sentido quando o layout e COMPARTILHADO: furar o original mudaria
    todo mapa que aponta para ele, e no caso do `SpearPillar` o outro usuario e
    o Sky Pillar de HOENN.
    """
    velho = F.layouts()[d["layout"]]
    novo_id = "LAYOUT_" + mapa.upper()
    pasta = f"data/layouts/{mapa}"
    # A pasta do layout velho pode ter EXATAMENTE este nome, e ai o copiador
    # reclamaria de copiar arquivo sobre ele mesmo. Medido em
    # `OreburghCity_Flat1_F2`, cujo layout ja se chama assim e e compartilhado
    # com o Flat2 vizinho.
    if novo_id == velho["id"] or f"{pasta}/map.bin" == velho["blockdata_filepath"]:
        novo_id += "_PROPRIO"
        pasta += "_Proprio"
    os.makedirs(f"{REPO}/{pasta}", exist_ok=True)
    shutil.copyfile(f"{REPO}/{velho['blockdata_filepath']}", f"{REPO}/{pasta}/map.bin")
    shutil.copyfile(f"{REPO}/{velho['border_filepath']}", f"{REPO}/{pasta}/border.bin")
    lay = dict(velho)
    # o nome sai da PASTA e nao do mapa: com o nome do mapa, o clone do
    # `OreburghCity_Flat1_F2` gerava `OreburghCity_Flat1_F2_Layout` duas vezes e
    # o montador parava em "symbol already defined".
    lay.update({"id": novo_id, "name": os.path.basename(pasta) + "_Layout",
                "blockdata_filepath": f"{pasta}/map.bin",
                "border_filepath": f"{pasta}/border.bin"})
    arq = f"{REPO}/data/layouts/layouts.json"
    todos = json.load(open(arq))
    todos["layouts"].append(lay)          # no FIM: nenhum indice antigo anda
    json.dump(todos, open(arq, "w"), indent=2, ensure_ascii=False)
    F.layouts()[novo_id] = lay
    d["layout"] = novo_id
    json.dump(d, open(f"{REPO}/data/maps/{mapa}/map.json", "w"),
              indent=2, ensure_ascii=False)
    return novo_id


def palavra(mapa, alvo):
    """Palavra de 16 bits da boca: porta de caverna, nao seta de portaria.

    `abre_portas_extras_sinnoh.palavra_de_porta` devolve a porta MAIS COMUM do
    mapa, que em cidade e a porta de casa e esta certo. Em rota a mais comum e a
    seta da portaria (`MB_NORTH_ARROW_WARP`, medido em Route214), e boca de
    caverna com desenho de escada de portaria mente o mapa. Entao aqui a
    preferencia e explicita: porta NAO animada do proprio mapa, que e o desenho
    de entrada de caverna, e so depois o resto.
    """
    _d, lay, w, h, pal, comp = A._grade(mapa)
    nao_anim = W._MB["MB_NON_ANIMATED_DOOR"]
    conta = {}
    for p in pal:
        if comp(p) == nao_anim:
            conta[p] = conta.get(p, 0) + 1
    if conta:
        return max(conta, key=conta.get)
    if lay.get("primary_tileset") == "gTileset_GeneralSinnoh":
        return BOCA_PADRAO
    p = A.palavra_de_porta(mapa, alvo)
    return BOCA_PADRAO if p is None else p


def redesenha():
    """Refaz a palavra das bocas ja abertas, sem mexer em warp nenhum.

    Existe porque a regra de escolha da palavra mudou depois da primeira leva:
    Route214, Eterna Forest e a margem de Verity tinham ganhado a SETA de
    portaria, que e o desenho de escada de predio e nunca foi boca de caverna.

    Tres guardas, e cada uma tem um motivo medido:

    - so troca tile de SETA. Porta, animada ou nao, ja e desenho de entrada e
      fica como esta (a de Route228 e a das ruinas de pedra).
    - nao entra em mapa de caverna (`gTileset_CaveSinnoh`): la o 519 que o
      conversor escreve JA e a boca de caverna daquele tileset, e o 167 do
      tileset geral apareceria como porta de casa dentro da pedra.
    - nao entra em pai convertido do DS: la a palavra e escada de caverna.

    Sem a segunda e a terceira guarda esta funcao repintava a entrada de
    Mt. Coronet 1F South e a de Snowpoint City, que sao da leva anterior e
    estao certas.
    """
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    cavernas = {f"MAP_{p.upper()}" for p in grupos.get(C.GRUPO, [])}
    cavernas |= {json.load(open(f"{REPO}/data/maps/{p}/map.json"))["id"]
                 for p in grupos.get(C.GRUPO, [])}
    mexidos = 0
    for pasta in sorted(os.listdir(f"{REPO}/data/maps")):
        arq = f"{REPO}/data/maps/{pasta}/map.json"
        if not os.path.exists(arq):
            continue
        d = json.load(open(arq))
        if convertido_do_ds(d) or pasta in grupos.get(C.GRUPO, []):
            continue
        alvos = [(e["x"], e["y"]) for e in (d.get("warp_events") or [])
                 if e["dest_map"] in cavernas]
        if not alvos:
            continue
        _d, lay, w, _h, pal, comp = A._grade(pasta)
        if lay.get("secondary_tileset") == "gTileset_CaveSinnoh":
            continue
        nova = palavra(pasta, alvos[0])
        for x, y in alvos:
            if pal[y * w + x] == nova:
                continue
            if "ARROW_WARP" not in W.NOME.get(comp(pal[y * w + x]), ""):
                continue
            print(f"   {pasta:28} ({x:3},{y:3}) 0x{pal[y*w+x]:04X} -> 0x{nova:04X}")
            if APLICAR:
                A.grava_tile(d["layout"], x, y, nova)
            mexidos += 1
    print(f"bocas com a palavra refeita: {mexidos}")
    return 0


# --------------------------------------------------------------------- main
def main():
    if "--demo" in sys.argv:
        return demo()
    if "--redesenha" in sys.argv:
        return redesenha()
    heads = I.headers_do_platinum()
    pend = alvos_pendentes()
    usados, planos, fora = {}, [], []
    for pai, filho, coords, d in pend:
        if F.portas_livres(pai, d):
            continue                       # ja tem entrada, nao e caso deste
        if convertido_do_ds(d):
            _d, _l, w, h, pal, _c = A._grade(pai)
            ja = {(e["x"], e["y"]) for e in (d.get("warp_events") or [])}
            ja |= set(usados.get(pai, []))
            escolha = next((
                (x, z) for x, z in coords
                if 0 <= x < w and 0 <= z < h and not ((pal[z * w + x] >> 10) & 3)
                and (x, z) not in ja), None)
            if escolha is None and coords:
                # A fonte poe a escada em cima de um tile que ja virou warp
                # aqui. Medido em Victory Road 1F Room 3: a unica warp da grade
                # dela aponta para a Room 2, e por isso mesmo o conversor a
                # gastou como saida para Route224, senao a sala nao devolveria o
                # jogador. Entao a escada anda para o chao livre mais proximo,
                # que mantem o lado certo da sala.
                regiao = C.regiao_principal(pal, w, h) - {
                    yy * w + xx for xx, yy in ja}
                if regiao:
                    x0, z0 = coords[0]
                    i = min(regiao, key=lambda j: (j % w - x0) ** 2
                            + (j // w - z0) ** 2)
                    escolha = (i % w, i // w)
            if escolha is None:
                fora.append((filho, f"{pai}: nenhuma coordenada da fonte esta "
                                    "livre e andavel"))
                continue
            planos.append((pai, filho, escolha, C.ESCADA, "grade do DS"))
        else:
            cands = [c for c in candidatos(pai)
                     if (c[0], c[1]) not in set(usados.get(pai, []))]
            escolha = escolhe(cands, ancoras(pai, d, heads),
                              coords[0] if coords else None)
            if escolha is None:
                fora.append((filho, f"{pai}: nenhum tile passa no teste de boca"))
                continue
            x, y = escolha[0], escolha[1]
            planos.append((pai, filho, (x, y), None,
                           "penhasco" if escolha[2] else "parede"))
        usados.setdefault(pai, []).append(planos[-1][2])

    print(f"cavernas convertidas e sem entrada: {len(pend)}")
    print(f"bocas que da para abrir: {len(planos)}")
    for filho, m in fora:
        print(f"   {filho.replace('MAP_HEADER_', '')}: {m}")
    for pai, filho, (x, y), _p, como in planos:
        print(f"   {pai:28} ({x:3},{y:3}) {como:12} -> "
              f"{filho.replace('MAP_HEADER_', '')}")
    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        return 0

    for pai, _filho, (x, y), forcada, _como in planos:
        d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        if len(A.mapas_do_layout(d["layout"])) > 1:
            clona_layout(pai, d)
            d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        A.libera_tile(pai, x, y)
        A.grava_tile(d["layout"], x, y, forcada or palavra(pai, (x, y)))
    print(f"\naplicado: {len(planos)} bocas abertas. Agora rode "
          "`converte_cavernas_sinnoh.py --aplicar` para criar as cavernas.")
    return 0


def demo():
    """O que prova que a boca nasce no lugar certo, e nao em cima do jogador."""
    heads = I.headers_do_platinum()
    # 1. o tile escolhido tem que estar bloqueado HOJE e ter chao logo abaixo.
    #    Sem as duas contas a boca rouba chao ou nasce dentro da parede.
    for mapa in ("Route214", "Route228", "SolaceonTown"):
        _d, _l, w, h, pal, _c = A._grade(mapa)
        cs = candidatos(mapa)
        assert cs, mapa
        for x, y, _p, _a in cs[:50]:
            assert (pal[y * w + x] >> 10) & 3, (mapa, x, y)
            assert not ((pal[(y + 1) * w + x] >> 10) & 3), (mapa, x, y)
    # 2. Route214 e Route228 sao penhasco: a boca tem que cair numa mancha com
    #    MB_MOUNTAIN_TOP, senao a heuristica pegou cerca ou arvore.
    for mapa in ("Route214", "Route228"):
        assert any(c[2] for c in candidatos(mapa)), mapa
    # 3. a palavra escrita tem que ter comportamento de warp de verdade, lida da
    #    mesma tabela que o motor usa. Sem isso a porta existe e nunca dispara.
    prim, _ = F._atributos("gTileset_GeneralSinnoh")
    assert prim[BOCA_PADRAO & 0x3FF] in W.COMPORTA_WARP
    for mapa in ("Route214", "SolaceonTown", "EternaForest"):
        p = palavra(mapa, candidatos(mapa)[0][:2])
        _d, lay, _w, _h, _pal, comp = A._grade(mapa)
        assert comp(p) in W.COMPORTA_WARP, (mapa, hex(p))
    # 4. no pai convertido do DS a coordenada da fonte vale tile a tile: se ela
    #    caisse em rocha, a leitura da grade estaria invertida.
    #    A versao anterior contava as pendencias ("achou >= 3") e envelheceu
    #    calada: as pendencias sao justamente o que esta ferramenta consome, e
    #    quando a fila zerou o teste passou a reprovar o proprio conserto
    #    (licao 4.11 do ESTADO). O fato permanente e outro: nos mapas que JA
    #    foram convertidos do DS, o warp da fonte cai em chao andavel aqui.
    for pai, _filho, coords, d in alvos_pendentes():
        if not convertido_do_ds(d) or not coords:
            continue
        _dd, _l, w, h, pal, _c = A._grade(pai)
        assert any(0 <= x < w and 0 <= z < h and not ((pal[z * w + x] >> 10) & 3)
                   for x, z in coords), pai
    conferidos = 0
    for pasta in sorted(os.listdir(f"{REPO}/data/maps")):
        arq = f"{REPO}/data/maps/{pasta}/map.json"
        if not os.path.exists(arq):
            continue
        d = json.load(open(arq))
        if not convertido_do_ds(d):
            continue
        h4 = header_do_mapa(pasta, d, heads)
        pe = os.path.join(C.PLAT, "res/field/events",
                          heads[h4][0] + ".json") if h4 else None
        if not pe or not os.path.exists(pe):
            continue
        _dd, _l, w, h, pal, _c = A._grade(pasta)
        for wv in json.load(open(pe)).get("warp_events", []):
            x, z = int(wv["x"]), int(wv["z"])
            if not (0 <= x < w and 0 <= z < h):
                continue
            assert not ((pal[z * w + x] >> 10) & 3), (pasta, x, z)
            conferidos += 1
    assert conferidos >= 20, conferidos
    # 5. ancora: Route214 tem warp para a Ruin Maniac Cave dos dois lados, entao
    #    a translacao local existe. Sem ela a posicao seria chute puro.
    d = json.load(open(f"{REPO}/data/maps/Route214/map.json"))
    assert ancoras("Route214", d, heads), "Route214 sem ancora"
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
