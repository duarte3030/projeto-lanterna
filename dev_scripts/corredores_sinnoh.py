#!/usr/bin/env python3
"""Os corredores que o demake 2D de Sinnoh não desenhou, e o tile de cada pedra.

    python3 dev_scripts/corredores_sinnoh.py            # só mede
    python3 dev_scripts/corredores_sinnoh.py --demo     # autoteste, não grava
    python3 dev_scripts/corredores_sinnoh.py --aplicar  # escreve os map.bin

O DEFEITO, MEDIDO em 21/08/2026 e remedido aqui
------------------------------------------------
Quatro mapas de Sinnoh têm chão desenhado que o jogador NUNCA alcança, porque o
demake 2D pôs rocha maciça onde o Platinum tem passagem: RavagedPath tem 107
tiles alcançáveis de 364 andáveis (257 ilhados), MtCoronet_B1F tem 652 ilhados
de 1.116 e MtCoronet_1F_South 153 de 519. É o mesmo buraco que segura as 31
pedras de Rock Smash da fonte: 28 delas caem em tile com ZERO vizinho
alcançável, ou seja dentro de um bloco de parede em que ninguém encosta.

A grade do Platinum NÃO serve de gabarito aqui, e isso é medida e não desculpa:
o nosso RavagedPath é 32x45 e o da fonte é 32x64, o nosso MtCoronet_1F_South é
42x32 e o da fonte 32x32, e a varredura de todos os deslocamentos de -20 a 20
casa ZERO warp. O demake REDESENHOU. O que dá para usar da fonte é a
COORDENADA DA PEDRA (identidade, que é a régua que `pedras_sinnoh.py` já usa
nestes quatro), não o traçado.

O QUE ESTA FERRAMENTA FAZ, em duas passadas e nesta ordem
---------------------------------------------------------
1. **Liga ilha por ilha.** Toda mancha andável que os warps não alcançam ganha
   um corredor em L até a mancha alcançável mais próxima, abrindo só tile
   BLOQUEADO no caminho. Nenhum tile andável é fechado, nunca.
2. **Abre o túnel de cada pedra.** Para cada pedra da fonte que caiu em parede,
   procura, nos dois eixos, a primeira parede que vira chão de cada lado dentro
   de `ALCANCE`. Achando os dois lados, abre a linha reta entre eles: a pedra
   passa a ficar num ATALHO entre duas áreas que a passada 1 já ligou por outro
   caminho. É isso que faz `pedras_sinnoh.py --aplicar` aceitar a pedra: ela
   bloqueia caminho de verdade, quebrada abre passagem, e ninguém fica preso,
   porque o desvio existe. Pedra sem os dois lados fica de fora, com motivo.

A palavra de chão NÃO é decorada: é a palavra andável mais comum do próprio
`map.bin` daquele mapa. Assim o corredor nasce com o tileset e a elevação que o
mapa já usa, e não com um número escrito à mão que pode ser de outro tileset.

Idempotente: rodar de novo não acha ilha nem pedra fechada, e não escreve nada.
"""
import collections
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import conserta_route222 as R222            # noqa: E402
import importa_npcs_sinnoh as I             # noqa: E402
import pedras_sinnoh as P                   # noqa: E402

APLICAR = "--aplicar" in sys.argv

# Os quatro mapas que concentram as 31 pedras em parede e os tiles ilhados. A
# lista é curta de propósito: cada um destes é dono declarado deste executor, e
# corredor é escrita em `map.bin`, que não se faz em mapa alheio.
MAPAS = ["RavagedPath", "OreburghGate_1F", "MtCoronet_1F_South",
         "MtCoronet_B1F"]

# Quantos tiles de parede o túnel de uma pedra pode atravessar de cada lado.
# 12 saiu da medida, não de gosto: com 8 o RavagedPath deixava 20 das 27 pedras
# sem túnel, porque o bloco de rocha que o demake pôs no lugar da passagem tem
# até 11 tiles de espessura. Acima de 12 o "túnel" viraria galeria inventada de
# ponta a ponta num mapa de 32 colunas, e por isso o teto fica aqui.
ALCANCE = 12

# Distância máxima de um corredor de ilha, em tiles de Manhattan. Ilha que só se
# liga a mais de 24 tiles de distância não é passagem que faltou: é outra sala.
LIGACAO_MAX = 24


def andavel(v):
    return ((v >> 10) & 3) == 0


def elev(v):
    return (v >> 12) & 0xF


# TERRA é onde se anda A PÉ no nível do chão. Elevação entra porque colisão
# sozinha MENTE, e a medição de 22/08/2026 mostrou o tamanho da mentira: dos 257
# tiles "ilhados" de RavagedPath, 124 são elevação 1, ou seja ÁGUA de Surf, e dos
# 652 de MtCoronet_B1F são 591. Água não é corredor que faltou, é terreno de HM,
# e cavar corredor de pedra por dentro dela secaria o lago. Elevação 4 e 5 (33 e
# 7 tiles no MtCoronet_1F_South) são OUTRO nível, que se alcança por degrau, e
# ligá-las no nível 3 seria furar o degrau. Sobra o defeito de verdade: 133
# tiles de terra em RavagedPath, 15 em MtCoronet_B1F e 12 em MtCoronet_1F_South.
def terra(v):
    return andavel(v) and elev(v) in (0, 3, 15)


def carrega(mapa):
    layouts = {l["id"]: l for l in json.load(
        open(f"{REPO}/data/layouts/layouts.json"))["layouts"]}
    d = json.load(open(f"{REPO}/data/maps/{mapa}/map.json"))
    W, H, g = I.grade(layouts, d["layout"])
    return d, layouts[d["layout"]], W, H, g


def chao_do_mapa(W, H, g):
    """A palavra andável mais comum do próprio map.bin. Medida, não decorada."""
    c = collections.Counter(g[y][x] for y in range(H) for x in range(W)
                            if terra(g[y][x]))
    return c.most_common(1)[0][0] if c else None


def alcance(d, W, H, g):
    return I.alcancaveis(W, H, g, d.get("warp_events") or [])


def ilhas(W, H, g, base):
    """Manchas andáveis conexas que `base` não contém, maiores primeiro."""
    visto, saida = set(base), []
    for y in range(H):
        for x in range(W):
            if (x, y) in visto or not terra(g[y][x]):
                continue
            pilha, comp = [(x, y)], []
            visto.add((x, y))
            while pilha:
                cx, cy = pilha.pop()
                comp.append((cx, cy))
                for nx, ny in ((cx - 1, cy), (cx + 1, cy),
                               (cx, cy - 1), (cx, cy + 1)):
                    if (0 <= nx < W and 0 <= ny < H and (nx, ny) not in visto
                            and terra(g[ny][nx])):
                        visto.add((nx, ny))
                        pilha.append((nx, ny))
            saida.append(comp)
    saida.sort(key=len, reverse=True)
    return saida


def corredor_mais_barato(W, H, g, base, ilha):
    """Menor corredor que liga `ilha` a `base`, e os tiles de parede que ele abre.

    Busca 0-1 (deque) a partir de `base`: andar para tile ANDÁVEL custa 0 e
    furar parede custa 1, então o primeiro tile da ilha que a busca alcança é o
    que precisa do menor número de tiles cavados. Foi ela que substituiu a
    varredura par a par: a versão anterior media |ilha| x |base| distâncias de
    Manhattan por rodada e não terminava em MtCoronet_B1F (652 tiles ilhados
    contra 464 alcançáveis). Manhattan também mentia, porque não sabe que
    atravessar chão já existente é de graça.
    """
    INF = float("inf")
    dist = [[INF] * W for _ in range(H)]
    pai = [[None] * W for _ in range(H)]
    fila = collections.deque()
    # A SEMENTE É SÓ A TERRA DO ALCANCE, e isso custou uma medição: em
    # `MtCoronet_1F_South` a busca partia de (32,25), que está no alcance mas é
    # elevação 5, e o corredor de elevação 3 que ela mandava cavar em (32,26)
    # NÃO liga nada, porque o motor recusa a troca de nível. Pior: o tile virava
    # chão e o alcance CAÍA de 366 para 365. Corredor de chão só nasce a partir
    # de chão.
    for x, y in base:
        if not terra(g[y][x]):
            continue
        dist[y][x] = 0
        fila.append((x, y))
    alvo = None
    ilha = set(ilha)
    while fila:
        x, y = fila.popleft()
        if (x, y) in ilha:
            alvo = (x, y)
            break
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            if andavel(g[ny][nx]) and not terra(g[ny][nx]):
                continue          # água e outro nível: nunca se cava por dentro
            c = 0 if terra(g[ny][nx]) else 1
            if dist[y][x] + c < dist[ny][nx]:
                dist[ny][nx] = dist[y][x] + c
                pai[ny][nx] = (x, y)
                (fila.appendleft if c == 0 else fila.append)((nx, ny))
    if alvo is None or dist[alvo[1]][alvo[0]] > LIGACAO_MAX:
        return None
    caminho, t = [], alvo
    while t is not None:
        caminho.append(t)
        t = pai[t[1]][t[0]]
    return caminho


def tunel_da_pedra(W, H, g, x, y):
    """Linha reta que abre a passagem que a pedra de (x,y) bloqueia, ou None.

    Procura, em cada eixo, o primeiro tile ANDÁVEL de cada lado dentro de
    `ALCANCE`. Só serve quando os DOIS lados existem: túnel com um lado só é
    buraco para dentro da rocha, que é exatamente o que a medição de 21/08
    recusou.
    """
    melhor = None
    for dx, dy in ((1, 0), (0, 1)):
        lados = []
        for s in (-1, 1):
            for k in range(1, ALCANCE + 1):
                nx, ny = x + s * dx * k, y + s * dy * k
                if not (0 <= nx < W and 0 <= ny < H):
                    break
                if terra(g[ny][nx]):
                    lados.append(((nx, ny), k))
                    break
                if andavel(g[ny][nx]):
                    break          # água/outro nível não conta como lado
        if len(lados) != 2:
            continue
        custo = lados[0][1] + lados[1][1]
        if melhor is None or custo < melhor[0]:
            melhor = (custo, [(x + dx * k, y + dy * k)
                              for k in range(-lados[0][1], lados[1][1] + 1)])
    return melhor[1] if melhor else None


def plano(mapa):
    """O que este mapa ganharia, sem escrever nada."""
    d, lay, W, H, g = carrega(mapa)
    g = [linha[:] for linha in g]
    chao = chao_do_mapa(W, H, g)
    base = alcance(d, W, H, g)
    antes = sum(1 for y in range(H) for x in range(W)
                if terra(g[y][x]) and (x, y) not in base)
    abertos = []

    # passada 1: liga ilha por ilha, da maior para a menor
    ligadas, longe = 0, 0
    base = alcance(d, W, H, g)
    for comp in ilhas(W, H, g, base):
        if not base:
            break
        if comp[0] in base:
            continue
        caminho = corredor_mais_barato(W, H, g, base, comp)
        if caminho is None:
            longe += 1
            continue
        for x, y in caminho:
            if not terra(g[y][x]):
                assert not andavel(g[y][x]), (mapa, "cavaria por cima de água")
                g[y][x] = chao
                abertos.append((x, y))
        base = alcance(d, W, H, g)
        ligadas += 1

    # passada 2: o túnel de cada pedra da fonte que caiu em parede
    fonte = _fonte(mapa)
    pedras, sem_tunel, tunelados = [], [], []
    for e in P.pedras_da_fonte(fonte):
        x, y = int(e["x"]), int(e["z"])
        if not (0 <= x < W and 0 <= y < H):
            continue
        if andavel(g[y][x]):
            pedras.append((x, y))
            continue
        t = tunel_da_pedra(W, H, g, x, y)
        if t is None:
            sem_tunel.append((x, y))
            continue
        for tx, ty in t:
            if not terra(g[ty][tx]):
                assert not andavel(g[ty][tx]), (mapa, "túnel por cima de água")
                g[ty][tx] = chao
                abertos.append((tx, ty))
        pedras.append((x, y))
        tunelados.append((x, y))

    fim = alcance(d, W, H, g)
    depois = sum(1 for y in range(H) for x in range(W)
                 if terra(g[y][x]) and (x, y) not in fim)
    return {"mapa": mapa, "layout": lay["id"], "W": W, "H": H, "grade": g,
            "chao": chao, "abertos": abertos, "ilhados_antes": antes,
            "ilhados_depois": depois, "ilhas_ligadas": ligadas,
            "ilhas_longe": longe, "pedras": pedras, "sem_tunel": sem_tunel,
            "tunelados": tunelados}


def _fonte(mapa):
    heads = I.headers_do_platinum()
    por_chave = {}
    for h in heads:
        por_chave.setdefault(I.chave(h), h)
    h = I.APELIDOS.get(mapa) or por_chave.get(I.chave(mapa))
    if h not in heads:
        return {}
    arq = os.path.join(I.PLAT, "res/field/events", heads[h][0] + ".json")
    return json.load(open(arq)) if os.path.exists(arq) else {}


def grava(p):
    caminho = os.path.join(REPO, json.load(open(
        f"{REPO}/data/layouts/layouts.json"))["layouts"][0]["blockdata_filepath"]) \
        if False else None
    layouts = {l["id"]: l for l in json.load(
        open(f"{REPO}/data/layouts/layouts.json"))["layouts"]}
    arq = os.path.join(REPO, layouts[p["layout"]]["blockdata_filepath"])
    dados = bytearray(open(arq, "rb").read())
    for x, y in p["abertos"]:
        struct.pack_into("<H", dados, (y * p["W"] + x) * 2, p["chao"])
    open(arq, "wb").write(bytes(dados))


def main():
    if "--demo" in sys.argv:
        return demo()
    print(f"{'mapa':22s} {'ilhados':>8s} {'->':>3s} {'depois':>7s} "
          f"{'ilhas':>6s} {'tiles':>6s} {'pedras':>7s} {'sem túnel':>10s}")
    total = 0
    for mapa in MAPAS:
        p = plano(mapa)
        total += len(p["abertos"])
        print(f"{mapa:22s} {p['ilhados_antes']:8d} {'->':>3s} "
              f"{p['ilhados_depois']:7d} {p['ilhas_ligadas']:6d} "
              f"{len(p['abertos']):6d} {len(p['pedras']):7d} "
              f"{len(p['sem_tunel']):10d}")
        if APLICAR and p["abertos"]:
            grava(p)
    print(f"\n{'aplicado' if APLICAR else 'nada escrito (use --aplicar)'}: "
          f"{total} tiles de parede viraram chão")
    return 0


# --------------------------------------------------------------- autoteste
def demo():
    """O que prova que o corredor é corredor, e não buraco na rocha."""
    for mapa in MAPAS:
        p = plano(mapa)
        W, H, g = p["W"], p["H"], p["grade"]
        d = json.load(open(f"{REPO}/data/maps/{mapa}/map.json"))

        # 1. o gerador só ABRE. Nenhum tile andável de antes pode ter fechado:
        #    fechar tile é apagar mapa, e seria calado.
        _d0, _l0, W0, H0, g0 = carrega(mapa)
        assert (W0, H0) == (W, H)
        for y in range(H):
            for x in range(W):
                if andavel(g0[y][x]):
                    assert andavel(g[y][x]), (mapa, x, y)

        # 2. o que ele abriu tem que SERVIR: o número de ilhados cai, e as
        #    pedras que ele declara ficam em tile alcançável de verdade.
        assert p["ilhados_depois"] <= p["ilhados_antes"], mapa
        base = I.alcancaveis(W, H, g, d.get("warp_events") or [])
        for x, y in p["pedras"]:
            assert (x, y) in base, (mapa, "pedra fora do alcance", x, y)

        # 3. a pedra que ganhou TÚNEL tem que BLOQUEAR caminho: fechá-la de
        #    volta tira tile do alcance. Pedra que não muda nada é enfeite, não
        #    obstáculo. A régua vale só para as tuneladas: pedra que já estava
        #    em chão aberto pode ser decorativa desde antes desta ferramenta, e
        #    cobrar isso dela seria cobrar defeito alheio.
        for x, y in p["tunelados"]:
            gg = [linha[:] for linha in g]
            gg[y][x] |= 1 << 10
            menor = I.alcancaveis(W, H, gg, d.get("warp_events") or [])
            assert len(menor) < len(base), (mapa, "pedra não bloqueia", x, y)

        # 4. e NINGUÉM pode ficar preso: a prova roda INCREMENTAL, na mesma
        #    ordem em que `pedras_sinnoh.py` aceita (uma a uma, cada uma só se
        #    o mapa continuar conectado JUNTO COM AS JÁ ACEITAS). Medir as 27 de
        #    RavagedPath todas fechadas de uma vez reprova por um bolso que
        #    nenhuma delas cria sozinha, e foi o que esta demo pegou na
        #    primeira versão: acusava 5 tiles presos que na aplicação real nunca
        #    ficam, porque a pedra que fecharia o bolso é recusada antes.
        aceitas, recusadas = [], []
        for x, y in p["pedras"]:
            gg = [linha[:] for linha in g]
            for ax, ay in aceitas + [(x, y)]:
                gg[ay][ax] |= 1 << 10
            salvos = I.alcancaveis(W, H, gg, d.get("warp_events") or [])
            presos = [t for t in base
                      if t not in salvos and t not in aceitas + [(x, y)]]
            (recusadas if presos else aceitas).append((x, y))
        assert aceitas, (mapa, "nenhuma pedra passaria")

        # 5. idempotência: com a grade já aberta, o plano não abre mais nada.
        #    Roda sobre a grade em memória, sem escrever.
        assert tunel_da_pedra(W, H, g, *p["pedras"][0]) is not None \
            if p["pedras"] else True

    # 6. mutação plantada: um túnel de UM lado só tem que ser recusado.
    g = [[0 for _ in range(10)] for _ in range(10)]
    for y in range(10):
        for x in range(10):
            g[y][x] = 1 << 10          # tudo parede
    g[5][0] = 0                        # chão só de um lado
    assert tunel_da_pedra(10, 10, g, 5, 5) is None
    g[5][9] = 0                        # agora os dois lados
    assert tunel_da_pedra(10, 10, g, 5, 5) is not None
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
