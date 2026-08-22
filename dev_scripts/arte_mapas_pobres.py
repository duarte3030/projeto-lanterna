#!/usr/bin/env python3
"""Decora os mapas POBRES (arte < 10) de Johto e de Unova, escrevendo SÓ o id de
metatile do `map.bin`.

Contexto (22/08/2026, pedido do Gui "melhorar as artes pobres todas das 5
primeiras regiões"). A régua de arte do `dev_scripts/completude.py` conta
metatiles distintos por mapa e marca abaixo de 10 como "pobre": abaixo disso o
mapa não é desenho, é máscara de colisão em duas cores. Nas cinco primeiras
regiões restavam 26 pobres, e eles se separam em dois montes:

  - **HOENN, 21 mapas, TODOS VANILLA e por isso INTOCADOS.** Medido com
    `git log --follow` em cada `map.bin`: o último commit dos 21 é de upstream
    (`f61810a8f9` "Dump maps" de 2018, `89d35e82a2`, `2237d0748f`, `75b0c9d7a9`),
    nenhum do hack. São 14 quadrados do Battle Pyramid (moldes 8x8 que o motor
    SORTEIA e monta em tempo de execução, `GenerateBattlePyramidFloorLayout`) e
    7 layouts natimortos de 1x1 (`Route104_Prototype`, `UnusedContestHall1..6`,
    UMA célula cada). Sala minúscula do Emerald é decisão da Game Freak, não
    defeito nosso, e molde de Pirâmide redesenhado à mão quebraria o sorteio.
    A lista sai de `vanilla()` abaixo, e o `--demo` reconfere que ninguém a
    tocou.
  - **JOHTO (3) e UNOVA (1), nossos, e são estes que o gerador decora.** O
    quinto, o `Unova_VirbankComplexElevator`, foi MEDIDO, DESENHADO e
    DESCARTADO: ver `NAO_MEXER` abaixo.

O vocabulário é o do tileset que cada mapa JÁ carrega; o desenho é aprendido de
mapa NOSSO/vanilla que usa o MESMO par de tilesets e tem arte de verdade:

    MahoganyHideout_B1F/B2F/B3F  (General+Facility)  <- AquaHideout_1F/B1F/B2F
       esconderijo de vilão aprendendo com esconderijo de vilão, mesmo tileset
    Unova_FloccesyRanchBarn  (Building+UnovaTraditionalHouse) <- casas de Unova
    Unova_VirbankComplexElevator (Building+UnovaMart) <- lojas de Nimbasa

Como funciona, e por que não pode quebrar nada (as três primeiras regras são as
do `arte_ginasios_sinnoh.py`, de onde este script importa o motor; a quarta é
mais apertada que a de lá):

1. A célula do `map.bin` é u16: **10 bits de baixo são o METATILE**, os 6 de
   cima são COLISÃO e ELEVAÇÃO. Escreve-se `(antigo & 0xFC00) | novo`, então os
   6 bits de cima nunca são tocados e a máscara sai byte a byte idêntica.
2. Andabilidade não muda porque colisão e elevação não mudam. O que ainda podia
   mudar é o ATRIBUTO do metatile (gelo, esteira, porta, tapete, mato), então só
   entram células cujo metatile tem comportamento `MB_NORMAL` (0) e o
   substituto também tem 0. Isso congela sozinho porta, escada, tapete e
   qualquer `MB_TALL_GRASS`: nenhum é criado e nenhum é removido.
3. Chão vira chão e parede vira parede: a assinatura de vizinhança é indexada
   pelo bit de colisão, então enfeite de parede só cai em parede.
4. **Célula com evento fica congelada inteira, e a ORLA de 4 vizinhos em volta
   dela não recebe ENFEITE.** A orla existe porque o esconderijo de Mahogany tem
   22 `coord_events` (as armadilhas de piso do Team Rocket) e 8 placas: um
   enfeite carimbado colado numa delas leria como parte da armadilha ou taparia
   a leitura da placa.
   **A orla NÃO barra o passo estrutural, e isso foi medido antes de decidir**:
   com ela barrando tudo, 125 das 540 células do B1F (23% do mapa) ficavam
   com o metatile velho, e como o metatile velho de parede ali é PRETO PURO
   (0x201), o resultado eram 125 buracos pretos no meio das paredes novas.
   O passo estrutural não pode estragar evento nenhum, e isso não é opinião: ele
   troca parede por parede e chão por chão (regra 3), com colisão, elevação e
   comportamento provados idênticos célula a célula contra o `git show HEAD:`
   no `--demo`. Quem podia atrapalhar era o enfeite, e é o enfeite que a orla
   barra. Nenhum `map.json` é lido para escrita e nenhum é tocado.

Uso:
    python3 dev_scripts/arte_mapas_pobres.py             # mede, não escreve
    python3 dev_scripts/arte_mapas_pobres.py --dry-run   # idem, explícito
    python3 dev_scripts/arte_mapas_pobres.py --aplicar   # escreve os map.bin
    python3 dev_scripts/arte_mapas_pobres.py --demo      # auto-teste

Idempotente: as escolhas dependem só de colisão, evento e comportamento, que o
script nunca muda. Rodar duas vezes dá o mesmo byte (o `--demo` prova).
"""
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
import arte_ginasios_sinnoh as G   # noqa: E402  (motor: aprende/assinatura/enfeite)

# alvo -> referência(s) com o MESMO par de tilesets e arte de verdade.
PARES = {
    # Johto. O par General+Facility é o do esconderijo da Aqua em Hoenn:
    # esconderijo de vilão aprendendo com esconderijo de vilão.
    #
    # É UM mapa de referência só, e a escolha foi feita OLHANDO O PNG, não pelo
    # número. Somar os três AquaHideout dá 132+103+100 de vocabulário e sobe a
    # régua de 36 para 43 metatiles distintos, mas o `AquaHideout_1F` é a BOCA
    # da caverna: ele traz terra e rocha marrom, e a votação punha manchas de
    # rocha ao ar livre no meio de um porão de concreto do Team Rocket. Número
    # de arte mais alto com desenho pior é exatamente o que a régua não vê.
    # O `AquaHideout_B1F` sozinho (51x24, 132 distintos) é interior puro e tem
    # assinatura de sobra para os 540 blocos de cada andar de Mahogany.
    "MahoganyHideout_B1F": ("AquaHideout_B1F",),
    "MahoganyHideout_B2F": ("AquaHideout_B1F",),
    "MahoganyHideout_B3F": ("AquaHideout_B1F",),
    # Unova. Casas de Unova do mesmo tileset, todas de porte de casa (8x8 a
    # 28x14): mesa, tapete, prateleira e parede com quadro.
    "Unova_FloccesyRanchBarn": ("Unova_StrangeHouse1F", "Unova_AldersHouse",
                                "Unova_LentimasHouse", "Unova_OpelucidCuriosityShop",
                                "Unova_LentimasCoinHouse", "Unova_CelestialTower1F"),
}

# Meta desta rodada: 15 metatiles distintos (o piso da régua do `completude.py`
# é 10; 15 é o mesmo alvo do `arte_ginasios_sinnoh.py`).
META = 15

# Distância mínima (Chebyshev) entre dois enfeites. O 4 do gerador de ginásio é
# de mapa grande; num celeiro 8x8 ele só acha 3 lugares e a arte para em 13,
# abaixo da meta. Medido: com 2 o mesmo celeiro fecha em 16.
ESPACO_GRANDE, ESPACO_MIUDO, MIUDO = 4, 2, 400

# O pobre que este gerador SABE decorar e mesmo assim NÃO decora, com o motivo
# medido. Está aqui, e não numa nota de rodapé, porque a próxima pessoa a olhar
# a régua vai ver o mapa ainda abaixo de 10 e vai querer "consertar".
NAO_MEXER = {
    "Unova_VirbankComplexElevator": """4x4 = 16 células, e o teto honesto é 6 ou 7.
    Três razões, todas medidas em 22/08/2026 e nenhuma de gosto:
    (a) TAMANHO. Sobram 7 células livres depois de congelar as 3 de evento (a
        placa e as duas folhas da porta, estas com comportamento 96) e as 3 de
        parede de fundo. Os elevadores VANILLA do Emerald têm 15 e 16 distintos
        em 35 e 30 células (`BattleFrontier_BattleTowerElevator` 5x7 = 15,
        `LilycoveCity_DepartmentStoreElevator` 5x6 = 16): densidade ~0,45 por
        célula, que em 16 células dá 7. Pedir 15 aqui é pedir que quase toda
        célula seja um metatile diferente, o que é ruído e não desenho.
    (b) FIDELIDADE. O `.ablk` do BW3G que ele compartilha
        (`DeptStoreElevator.ablk`) tem 4 blocos distintos, e a conversão é fiel
        byte a byte (medido na 0.h do ESTADO). Ele é o equivalente Unova do
        "vanilla fica como o jogo fez".
    (c) O DESENHO SAI PIOR, e isso foi olhado no PNG, não deduzido. O único
        vocabulário de `gTileset_UnovaMart` com arte são as 4 lojas de Nimbasa e
        Icirrus, então a votação troca o piso amarelo por piso verde de loja e a
        parede de vidro azul (que é justamente o que faz aquilo parecer um
        elevador) por PRATELEIRA DE MERCADO. Sai um mercadinho de 4x4.
    O `completude.py` já prevê o caso no comentário do `PISO_ARTE` ("mapa
    minúsculo legítimo cai aqui de vez em quando"), então este mapa CONTINUA na
    conta dos pobres da régua, de propósito e por escrito.""",
}


def vanilla_hoenn():
    """Os 21 pobres de Hoenn, com o commit de upstream que os escreveu.

    A regra do Gui: vanilla fica como o jogo fez, só relata. A prova é o
    `git log --follow` do `map.bin`, conferida no `--demo`.
    """
    return (["BattleFrontier_BattlePyramidFloor"]
            + [f"BattlePyramidSquare{n:02d}" for n in (2, 4, 5, 6, 7, 8, 9, 10,
                                                       12, 13, 14, 15, 16)]
            + ["Route104_Prototype"]
            + [f"UnusedContestHall{n}" for n in range(1, 7)])


AUTORES_UPSTREAM = ("Marcus Huderle", "GriffinR", "PikalaxALT", "Diegoisawesome",
                    "DizzyEggg", "ProjectRevoTPP", "Phlosioneer")


def eventos(d):
    return {(o["x"], o["y"])
            for k in ("object_events", "warp_events", "bg_events", "coord_events")
            for o in (d.get(k) or [])}


def orla(d):
    """Célula de evento e os 4 vizinhos: sem ENFEITE (ver regra 4 no topo)."""
    ev = eventos(d)
    fora = set(ev)
    for x, y in ev:
        for dx, dy in G.N4:
            fora.add((x + dx, y + dy))
    return fora


def decora(alvo):
    """Devolve (layout, W, H, antes, depois, quantos enfeites)."""
    tab, enfeites = G.aprende(PARES[alvo])
    d, L, W, H, v = G.grade(alvo)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    fora = eventos(d)          # nem re-pele estrutural, nem enfeite
    sem_enfeite = orla(d)
    mask = G._mascara(v)
    out = list(v)

    def livre(x, y):
        return (x, y) not in fora and beh(v[y * W + x] & 0x3FF) == 0

    for y in range(H):
        for x in range(W):
            if not livre(x, y):
                continue
            i = y * W + x
            m = mask[i]
            novo = G._escolhe(tab, [(m, 8, G._assin(mask, W, H, x, y, G.N8)),
                                    (m, 4, G._assin(mask, W, H, x, y, G.N4)),
                                    (m,)])
            if novo is not None:
                out[i] = (v[i] & 0xFC00) | novo

    postos, n = [], 0
    meta = META
    espaco = ESPACO_MIUDO if W * H < MIUDO else ESPACO_GRANDE
    basta = lambda: (n >= G.ENFEITES_MAX and G.distintos(out) >= meta) or n >= G.ENFEITES_TETO

    def cabe(e, x, y):
        if any(max(abs(x - px), abs(y - py)) < espaco for px, py in postos):
            return False
        return all(mask[(y + dy) * W + x + dx] == m and livre(x + dx, y + dy)
                   and (x + dx, y + dy) not in sem_enfeite and beh(mt) == 0
                   for dx, dy, mt, m in e["cel"])

    for _ in range(3):
        if basta():
            break
        for e in enfeites:
            if basta():
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


# ------------------------------------------------------------------------ demo
def demo():
    """As regras que este script não pode quebrar, medidas e não afirmadas."""
    import subprocess
    for alvo in PARES:
        L, W, H, antes, depois, n = decora(alvo)
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        base = G.do_git(L["blockdata_filepath"])
        assert base is not None, f"{alvo}: sem git, e sem git não há prova"

        # 1. colisão e elevação byte a byte, contra o disco E contra o HEAD
        assert not G.confere(antes, depois), f"{alvo}: colisão/elevação mudou"
        assert not G.confere(base, depois), f"{alvo}: colisão mudou contra o HEAD"

        # 2. comportamento de metatile idêntico célula a célula: andabilidade,
        #    porta, escada, tapete e MB_TALL_GRASS continuam o que eram
        maus = [i for i, (a, b) in enumerate(zip(base, depois))
                if beh(a & 0x3FF) != beh(b & 0x3FF)]
        assert not maus, f"{alvo}: comportamento mudou em {len(maus)} células"

        # 3. célula de evento intocada, e nenhum ENFEITE na orla dela. O enfeite
        #    é o que muda desenho de verdade; a re-pele estrutural é provada
        #    inofensiva pelos itens 1 e 2 (ver regra 4 no topo do arquivo).
        d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
        for x, y in eventos(d):
            if 0 <= x < W and 0 <= y < H:
                i = y * W + x
                assert base[i] == depois[i], f"{alvo}: mexeu na célula de evento ({x},{y})"

        # 4. a régua de arte SOBE, bate a meta e sai de pobre
        # contra o HEAD, e não contra o disco: depois de `--aplicar` o disco JÁ
        # é o desenho novo (o gerador é idempotente) e a comparação seria trivial
        assert G.distintos(depois) >= G.distintos(base), f"{alvo}: a arte caiu"
        assert G.distintos(depois) >= META, \
            f"{alvo}: {G.distintos(depois)} metatiles distintos, meta é {META}"

        # 5. mutação plantada: se o gerador escrevesse a célula inteira em vez
        #    dos 10 bits de baixo, a colisão viajaria junto e `confere` grita
        mutante = list(depois)
        mutante[len(mutante) // 2] ^= 0x0400
        assert G.confere(antes, mutante), f"{alvo}: mutação de colisão passou batido"

        print(f"OK  {alvo:30} {G.distintos(base):3} -> {G.distintos(depois):3} "
              f"metatiles (contra o HEAD), {n} enfeites")

    # 6. os 21 de Hoenn são vanilla: o último commit de cada map.bin é upstream
    lay = {l["id"]: l for l in json.load(
        open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"] if l.get("id")}
    for m in vanilla_hoenn():
        d = json.load(open(f"{RAIZ}/data/maps/{m}/map.json"))
        f = lay[d["layout"]]["blockdata_filepath"]
        r = subprocess.run(["git", "-C", RAIZ, "log", "--follow", "-1",
                            "--format=%an", "--", f], capture_output=True, text=True)
        autor = r.stdout.strip()
        assert autor in AUTORES_UPSTREAM, f"{m}: último autor é {autor!r}, não é upstream"
    print(f"OK  {len(vanilla_hoenn())} pobres de Hoenn são vanilla e ficam como estão")

    # 6b. o que está em NAO_MEXER continua byte a byte igual ao HEAD
    lay2 = {l["id"]: l for l in json.load(
        open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"] if l.get("id")}
    for m in NAO_MEXER:
        f = lay2[json.load(open(f"{RAIZ}/data/maps/{m}/map.json"))["layout"]]["blockdata_filepath"]
        assert open(f"{RAIZ}/{f}", "rb").read() == struct.pack(
            "<%dH" % len(G.do_git(f)), *G.do_git(f)), f"{m}: está em NAO_MEXER e mudou"
    print(f"OK  {len(NAO_MEXER)} mapa(s) em NAO_MEXER continuam byte a byte no HEAD")

    # 7. idempotência: só dá para medir escrevendo, então grava, roda de novo e
    #    volta ao estado original.
    origem = {a: G.grade(a)[4] for a in PARES}
    try:
        um = {}
        for alvo in PARES:
            L, W, H, _, depois, _ = decora(alvo)
            um[alvo] = depois
            G.grava(L, W, H, depois)
        for alvo in PARES:
            L, W, H, _, dois, _ = decora(alvo)
            assert dois == um[alvo], f"{alvo}: não é idempotente"
    finally:
        for alvo, v in origem.items():
            L = G._layouts()[json.load(
                open(f"{RAIZ}/data/maps/{alvo}/map.json"))["layout"]]
            G.grava(L, L["width"], L["height"], v)
    print("OK  idempotente, e o repo voltou ao estado de antes do demo")


def main():
    if "--demo" in sys.argv:
        return demo()
    aplicar = "--aplicar" in sys.argv
    for alvo in PARES:
        L, W, H, antes, depois, n = decora(alvo)
        maus = G.confere(antes, depois)
        if maus:
            sys.exit(f"ABORTA {alvo}: colisão/elevação mudaria em {len(maus)} células")
        print(f"{alvo:30} arte {G.distintos(antes):3} -> {G.distintos(depois):3}  "
              f"enfeites={n}  colisão idêntica")
        if aplicar:
            G.grava(L, W, H, depois)
    print(f"\nHoenn: {len(vanilla_hoenn())} pobres, TODOS vanilla, intocados por decisão.")
    for m in NAO_MEXER:
        print(f"{m}: intocado (ver NAO_MEXER).")
    if not aplicar:
        print("(nada escrito; use --aplicar)")


if __name__ == "__main__":
    main()
