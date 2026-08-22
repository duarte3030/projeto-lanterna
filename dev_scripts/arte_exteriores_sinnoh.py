#!/usr/bin/env python3
"""Decora os mapas POBRES de Sinnoh que NÃO vestem tileset de caverna.

ESCOPO, medido e não presumido (`--lista` refaz a conta a qualquer hora):
Sinnoh tem 376 mapas dentro da régua do `completude.py` e **76 abaixo do piso
de 10 metatiles distintos**. Desses 76, **72 vestem `gTileset_CaveSinnoh`** (são
as cavernas, e têm dono próprio nesta rodada) e os **4 restantes**
(`MtCoronetOutsideNorth`, `MtCoronetOutsideSouth`, `Route204North` e
`IronIsland`) são os moldes de portão que outra frente está mexendo. Ou seja:
pelo critério literal "abaixo de 10 e fora de caverna" esta lista seria VAZIA.

Então o alvo aqui é a META que a rodada pediu, e não o piso: **15 metatiles
distintos**. Os mapas de Sinnoh fora das cavernas abaixo de 15 são os 11
interiores de `gTileset_GenericBuilding` de `ALVOS`, todos entre 12 e 14: o
labirinto do ginásio D/P de Hearthome (duas salas de elevador, a sala da líder,
seis salas de treinador), a primeira sala de treinador do ginásio de Hearthome e
a casa da Iron Island. Nenhum dos 8 mapas `*_Gym` entra: aqueles já foram
decorados pelo `arte_ginasios_sinnoh.py` na rodada passada.

POR QUE SÓ O PASSO DE ENFEITE, e não o autotiling do gerador dos ginásios. O
motor do `arte_ginasios_sinnoh.py` tem dois passos: um ESTRUTURAL, que reescreve
parede e chão pela assinatura de vizinhança aprendida do doador, e um de
ENFEITE, que carimba os grupos de metatile raros (móvel, vaso, quadro). Aqui o
estrutural foi MEDIDO E DESCARTADO, não esquecido: nos ginásios de Sinnoh ele
era necessário porque a planta era mesmo uma máscara de duas cores, mas estas 11
salas já têm desenho legível (corredor claro, balcão de vidro, vão de porta) e
o número baixo é consequência de a planta ser um LABIRINTO, que por natureza
repete pouca peça. Rodado nelas, o estrutural trocava balcão e corredor por
retalho de parede de casa de Hoenn e o labirinto virava ruído amarelo onde
andável e bloqueado ficam iguais (imagem guardada na rodada). Enfeite sozinho
sobe a régua de 12 para 25-38 e não encosta na leitura da planta.

As "famílias" que o pedido descreve (exterior com árvore e cerca, interior com
tapete e estante, neve com monte) não viram `if` neste arquivo: quem escolhe o
vocabulário é o DOADOR, e doador de casa ensina móvel do mesmo jeito que doador
de rota ensinaria árvore. Como esta lista é 100% interior, os doadores são casas
de Hoenn do mesmo par de tilesets.

O que este script NÃO PODE quebrar, e cada regra tem prova no `--demo`:

1. Escreve só os 10 bits de baixo da célula (`(antigo & 0xFC00) | novo`).
   COLISÃO e ELEVAÇÃO saem byte a byte idênticas contra `git show HEAD:`.
2. Só entra e só sai metatile com comportamento 0 (`MB_NORMAL`). Isso congela
   sozinho porta, tapete, escada, esteira, gelo e **grama de encontro**: uma
   célula `MB_TALL_GRASS` nunca é criada nem removida porque nunca é tocada.
3. Célula com evento em cima (objeto, warp, placa, gatilho) **e os 4 vizinhos
   ortogonais dela** ficam congeladas. É a regra mais dura que este script tem
   sobre o gerador dos ginásios, e existe para que enfeite nenhum encoste no
   NPC, na porta ou na placa.
4. Enfeite só entra na região ALCANÇÁVEL a partir dos warps (mais a orla de uma
   célula). Sem isso o gerador punha vaso e poltrona na faixa morta fora das
   paredes da sala, que o jogador vê de longe e não faz sentido nenhum.
5. Nenhum `map.json`, script, tileset ou `flags.h` é lido para escrita. Só
   `map.bin`.

Uso:
    python3 dev_scripts/arte_exteriores_sinnoh.py --lista     # a lista e a conta
    python3 dev_scripts/arte_exteriores_sinnoh.py --dry-run   # mede, não escreve
    python3 dev_scripts/arte_exteriores_sinnoh.py --aplicar   # escreve os map.bin
    python3 dev_scripts/arte_exteriores_sinnoh.py --demo      # auto-teste
    python3 dev_scripts/arte_exteriores_sinnoh.py --imagens D # PNG antes/depois

Idempotente: a escolha de cada célula depende só de colisão, evento e
comportamento, e o script nunca muda nenhum dos três. O `--demo` prova rodando
duas vezes e devolvendo o repo ao estado de antes.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")

import arte_ginasios_sinnoh as G  # noqa: E402  (o motor, importado e não copiado)

# Casas de Hoenn do MESMO par (gTileset_Building, gTileset_GenericBuilding) que
# os 11 alvos vestem. Uma casa só não basta: as tabelas somam e `aprende()` já
# aceita tupla. Escolhidas por serem as mais ricas do par (64, 55 e 52 metatiles
# distintos) e por variarem o mobiliário: sala de estar, clube e salão.
DOADORES_CASA = (
    "VerdanturfTown_WandasHouse",
    "LilycoveCity_PokemonTrainerFanClub",
    "DewfordTown_Hall",
    "RustboroCity_House3",
    "OreburghCity_Flat1_F1",
)

ALVOS = {
    "HearthomeCityDpGymElevatorRoom1": DOADORES_CASA,
    "HearthomeCityDpGymElevatorRoom2": DOADORES_CASA,
    "HearthomeCityDpGymLeaderRoom":    DOADORES_CASA,
    "HearthomeCityDpGymTrainerRoom1":  DOADORES_CASA,
    "HearthomeCityDpGymTrainerRoom2":  DOADORES_CASA,
    "HearthomeCityDpGymTrainerRoom3":  DOADORES_CASA,
    "HearthomeCityDpGymTrainerRoom4":  DOADORES_CASA,
    "HearthomeCityDpGymTrainerRoom5":  DOADORES_CASA,
    "HearthomeCityDpGymTrainerRoom6":  DOADORES_CASA,
    "HearthomeCityGymTrainerRoom1":    DOADORES_CASA,
    "IronIslandHouse":                 DOADORES_CASA,
}

META_ARTE = 15    # o que a rodada pediu
PISO_ARTE = 10    # o piso do completude.py; nenhum alvo pode terminar abaixo
ESPACO = 3        # sala de 17x12 não comporta os 4 do gerador dos ginásios
DENSIDADE = 25    # uma peça de mobília a cada ~25 células jogáveis
ENFEITES_TETO = 24
VOLTAS = 4        # uma cópia de cada enfeite por volta, para variar o mobiliário


def congeladas(d, W, H):
    """Célula de evento MAIS os 4 vizinhos ortogonais dela."""
    fora = set()
    for k in ("object_events", "warp_events", "bg_events", "coord_events"):
        for o in (d.get(k) or []):
            x, y = o["x"], o["y"]
            for dx, dy in [(0, 0)] + G.N4:
                if 0 <= x + dx < W and 0 <= y + dy < H:
                    fora.add((x + dx, y + dy))
    return fora


def decora(alvo):
    """(layout, W, H, antes, depois, quantos enfeites)."""
    _, enfeites = G.aprende(ALVOS[alvo])
    d, L, W, H, v = G.grade(alvo)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    ev = congeladas(d, W, H)
    mask = G._mascara(v)
    perto = G._perto_do_jogavel(d, W, H, mask)
    out = list(v)

    def livre(x, y):
        return ((x, y) in perto and (x, y) not in ev
                and beh(v[y * W + x] & 0x3FF) == 0)

    teto = min(ENFEITES_TETO, max(4, len([p for p in perto
                                          if 0 <= p[0] < W and 0 <= p[1] < H])
                                  // DENSIDADE))
    postos, n = [], 0

    def cabe(e, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO for px, py in postos):
            return False
        return all(mask[(y + dy) * W + x + dx] == m and livre(x + dx, y + dy)
                   and beh(mt) == 0 for dx, dy, mt, m in e["cel"])

    # Uma cópia de cada enfeite por volta, e não N cópias do primeiro: senão o
    # teto se esgota carimbando sempre o mesmo vaso e a régua sobe pouco.
    for _ in range(VOLTAS):
        if n >= teto and G.distintos(out) >= META_ARTE:
            break
        for e in enfeites:
            if n >= teto and G.distintos(out) >= META_ARTE:
                break
            if n >= ENFEITES_TETO:
                break
            for y in range(H - e["h"] + 1):
                posto = False
                for x in range(W - e["w"] + 1):
                    if not cabe(e, x, y):
                        continue
                    for dx, dy, mt, _m in e["cel"]:
                        j = (y + dy) * W + x + dx
                        out[j] = (v[j] & 0xFC00) | mt
                    postos.append((x, y))
                    n += 1
                    posto = True
                    break
                if posto:
                    break
    return L, W, H, v, out, n


# --------------------------------------------------------------------- a lista
def lista():
    """Reimprime a conta que define o escopo, em vez de afirmá-la de cabeça."""
    import completude as C
    import importa_npcs_sinnoh as I
    lay = {l["id"]: l for l in json.load(
        open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"] if l.get("id")}
    fora = C._cortados_deficit()
    medidos, pobres, cav = 0, 0, 0
    for m in sorted(I.nossos_mapas_sinnoh()):
        p = f"{RAIZ}/data/maps/{m}/map.json"
        if not os.path.exists(p) or m in fora:
            continue
        l = lay.get(json.load(open(p)).get("layout"))
        if not l or not os.path.exists(f"{RAIZ}/{l['blockdata_filepath']}"):
            continue
        medidos += 1
        n = len(C._distintos(open(f"{RAIZ}/{l['blockdata_filepath']}", "rb").read()))
        caverna = "Cave" in l["secondary_tileset"]
        if n < C.PISO_ARTE:
            pobres += 1
            cav += caverna
        if n < META_ARTE and not caverna:
            print(f"  {m:34} {n:3}  {l['secondary_tileset']:26} "
                  f"{l['width']:>2}x{l['height']:<2}  "
                  f"{'ALVO' if m in ALVOS else 'outra frente'}")
    print(f"\nSinnoh: {medidos} mapas medidos, {pobres} abaixo do piso "
          f"{C.PISO_ARTE}, dos quais {cav} de caverna (frente vizinha) e "
          f"{pobres - cav} moldes de portão (outra frente).")
    print(f"Abaixo da meta {META_ARTE} e fora de caverna: os de cima; "
          f"{len(ALVOS)} são alvo desta frente.")


# ---------------------------------------------------------------------- demo
def demo():
    origem = {a: G.grade(a)[4] for a in ALVOS}
    um = {}
    for alvo in ALVOS:
        L, W, H, antes, depois, n = decora(alvo)
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        um[alvo] = depois

        # 1. colisão e elevação idênticas célula a célula, contra o HEAD do git,
        #    que é a linha de base que um `--aplicar` anterior não apaga.
        base = G.do_git(L["blockdata_filepath"])
        assert base is not None, f"{alvo}: sem git, e sem git não há prova"
        assert not G.confere(base, depois), f"{alvo}: colisão/elevação mudou"
        assert not G.confere(antes, depois), f"{alvo}: colisão/elevação mudou"

        # 2. comportamento de metatile idêntico: andabilidade, porta, tapete e
        #    grama de encontro continuam o que eram.
        maus = [i for i, (a, b) in enumerate(zip(base, depois))
                if beh(a & 0x3FF) != beh(b & 0x3FF)]
        assert not maus, f"{alvo}: comportamento mudou em {len(maus)} células"

        # 3. evento e os 4 vizinhos ortogonais dele intocados, byte a byte.
        d, _, W, H, _ = G.grade(alvo)
        for x, y in congeladas(d, W, H):
            assert base[y * W + x] == depois[y * W + x], \
                f"{alvo}: célula ({x},{y}), vizinha de evento, foi escrita"

        # 4. nada escrito fora da região alcançável a partir dos warps.
        perto = G._perto_do_jogavel(d, W, H, G._mascara(antes))
        for i, (a, b) in enumerate(zip(base, depois)):
            if a != b:
                assert (i % W, i // W) in perto, \
                    f"{alvo}: escreveu em ({i % W},{i // W}), fora do jogável"

        # 5. a régua sobe, passa da meta e ninguém termina abaixo do piso.
        # A régua sobe contra o HEAD do git, e não contra o disco: `antes` é o
        # disco, e depois de um `--aplicar` o disco JÁ está decorado, então
        # `depois == antes` e a comparação com o disco reprovava um gerador
        # idempotente e correto (medido em 22/08/2026, no fechamento da rodada
        # 7). `base` é a linha de base de verdade, a mesma que os passos 1 a 4
        # já usam, e é o que o `arte_mapas_pobres.py` faz.
        assert G.distintos(depois) > G.distintos(base), f"{alvo}: arte não subiu"
        assert G.distintos(depois) >= META_ARTE, \
            f"{alvo}: {G.distintos(depois)} metatiles, meta é {META_ARTE}"
        assert G.distintos(depois) >= PISO_ARTE

        # 6. a mutação plantada TEM que ser pega: se o gerador escrevesse a
        #    célula inteira, a colisão viajaria junto e `confere` é quem grita.
        mut = list(depois)
        mut[len(mut) // 2] ^= 0x0400
        assert G.confere(antes, mut), f"{alvo}: mutação de colisão passou batido"

        print(f"OK  {alvo:34} {G.distintos(base):3} -> {G.distintos(depois):3} "
              f"metatiles, {n} enfeites")

    # 7. idempotência: só dá para medir escrevendo. Grava, roda de novo, volta.
    try:
        for alvo in ALVOS:
            L, W, H, _, _, _ = decora(alvo)
            G.grava(L, W, H, um[alvo])
        for alvo in ALVOS:
            _, _, _, _, dois, _ = decora(alvo)
            assert dois == um[alvo], f"{alvo}: não é idempotente"
    finally:
        for alvo, v in origem.items():
            L = G._layouts()[json.load(
                open(f"{RAIZ}/data/maps/{alvo}/map.json"))["layout"]]
            G.grava(L, L["width"], L["height"], v)
    print("OK  idempotente, e o repo voltou ao estado de antes do demo")


# -------------------------------------------------------------------- imagens
def imagens(dest):
    import render_maps as RM
    lay = RM.carregar_layouts()
    cache = {}
    for sub in ("antes", "depois"):
        os.makedirs(f"{dest}/{sub}", exist_ok=True)
    origem = {a: G.grade(a)[4] for a in ALVOS}
    RM.OUT_DIR = f"{dest}/antes"
    for a in ALVOS:
        RM.renderizar_mapa(a, lay, cache)
    try:
        for a in ALVOS:
            L, W, H, _, depois, _ = decora(a)
            G.grava(L, W, H, depois)
        RM.OUT_DIR = f"{dest}/depois"
        for a in ALVOS:
            RM.renderizar_mapa(a, lay, cache)
    finally:
        for a, v in origem.items():
            L = G._layouts()[json.load(
                open(f"{RAIZ}/data/maps/{a}/map.json"))["layout"]]
            G.grava(L, L["width"], L["height"], v)
    contato(dest)
    print(f"imagens em {dest}")


def contato(dest):
    """Uma folha só, antes à esquerda e depois à direita, para olhar de uma vez."""
    from PIL import Image, ImageDraw
    linhas = []
    for a in ALVOS:
        pa, pd = f"{dest}/antes/{a}.png", f"{dest}/depois/{a}.png"
        if os.path.exists(pa) and os.path.exists(pd):
            linhas.append((a, Image.open(pa), Image.open(pd)))
    if not linhas:
        return
    esq = max(i.width for _, i, _ in linhas)
    dir_ = max(i.width for _, _, i in linhas)
    alt = sum(max(a.height, b.height) + 18 for _, a, b in linhas)
    folha = Image.new("RGB", (esq + dir_ + 24, alt), (24, 24, 24))
    dr = ImageDraw.Draw(folha)
    y = 0
    for nome, a, b in linhas:
        dr.text((4, y + 3), nome, fill=(255, 255, 255))
        folha.paste(a, (0, y + 18))
        folha.paste(b, (esq + 24, y + 18))
        y += max(a.height, b.height) + 18
    folha.save(f"{dest}/CONTATO.png")


def main():
    if "--demo" in sys.argv:
        return demo()
    if "--lista" in sys.argv:
        return lista()
    if "--imagens" in sys.argv:
        return imagens(sys.argv[sys.argv.index("--imagens") + 1])
    aplicar = "--aplicar" in sys.argv
    antes_n, ns = [], []
    for alvo in ALVOS:
        L, W, H, antes, depois, n = decora(alvo)
        maus = G.confere(antes, depois)
        if maus:
            sys.exit(f"ABORTA {alvo}: colisão/elevação mudaria em {len(maus)} células")
        antes_n.append(G.distintos(antes))
        ns.append(G.distintos(depois))
        print(f"{alvo:34} arte {G.distintos(antes):3} -> {G.distintos(depois):3}  "
              f"enfeites={n}  colisão idêntica")
        if aplicar:
            G.grava(L, W, H, depois)
    antes_n.sort()
    ns.sort()
    print(f"\nantes:  mediana {antes_n[len(antes_n) // 2]}, mínimo {antes_n[0]}")
    print(f"depois: mediana {ns[len(ns) // 2]}, mínimo {ns[0]}, "
          f"{sum(1 for x in ns if x < PISO_ARTE)} abaixo do piso {PISO_ARTE}, "
          f"{sum(1 for x in ns if x < META_ARTE)} abaixo da meta {META_ARTE}")
    if not aplicar:
        print("(nada escrito; use --aplicar)")


if __name__ == "__main__":
    main()
