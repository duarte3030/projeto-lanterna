#!/usr/bin/env python3
"""B1.c: abre os EXTERIORES folha de Sinnoh que um warp da fonte alcanca.

    python3 dev_scripts/abre_exteriores_folha_sinnoh.py            # so relata
    python3 dev_scripts/abre_exteriores_folha_sinnoh.py --aplicar  # escreve
    python3 dev_scripts/abre_exteriores_folha_sinnoh.py --demo     # autoteste

Diferenca para `abre_exteriores_sinnoh.py`
------------------------------------------
Aquele tem uma lista de QUATRO exteriores escrita a mao, escolhida porque cada um
destravava masmorra convertida. Aqui a fila sai do GRAFO DE WARP da fonte, em
laco ate parar de render, e o criterio de entrada e o do PRD: exterior que falta
e cujo pai ja esta na ROM. O metodo de dentro e o mesmo, e de proposito: planta
provisoria reaproveitada do repo, campo `origem` dizendo isso, ida e volta
provadas por comportamento de tile.

Por que a planta continua provisoria
------------------------------------
Decisao ja registrada no ESTADO: exterior de gen 4 tem cenario DESENHADO que a
grade 2D nao carrega. Medido nesta leva, para nao repetir de cabeca: a grade da
Amity Square tem 2212 tiles com colisao em 64x64, a do Battle Frontier 7505 em
96x96, e a do Great Marsh 17286 em 128x160. Convertidas com o motor de caverna
isso vira praca murada de pedra. Entao a planta e a antecamara `Route226_Access`
(13x9) que Sinnoh ja usa como passagem, com o `origem` marcando "passagem
provisoria" e o layout COMPARTILHADO com ela, igual ao precedente de 06/08.

Sem NPC, placa nem texto, pelo mesmo motivo de sempre: coordenada de exterior no
Platinum e GLOBAL da matriz de Sinnoh e nao ha offset que alinhe (decisao 5 de
`importa_npcs_sinnoh.py`); dentro de uma sala de 13x9 o NPC cairia em qualquer
lugar.

Por que a fila da OITO e nao vinte e oito
-----------------------------------------
Faltam 32 mapas de fora em Sinnoh, e so 8 tem pai na ROM. **O motivo nao e
buraco de ferramenta: e que exterior de gen 4 se liga por MATRIZ, nao por warp.**
Medido na fonte: `FUEGO_IRONWORKS_OUTSIDE` so e destino de warp do proprio
`FUEGO_IRONWORKS_BUILDING`, que por sua vez so e destino de warp do
`FUEGO_IRONWORKS_OUTSIDE` (par fechado, entra-se nele andando pela Route 205 na
matriz); `HALL_OF_ORIGIN`, `ETERNA_FOREST_OUTSIDE`, `SEABREAK_PATH` e
`FLOWER_PARADISE` nao sao destino de warp de NINGUEM; `FULLMOON_ISLAND` e
`NEWMOON_ISLAND` so saem do barco scriptado; e `GREAT_MARSH_1` a `5` sao
sorteadas, igual as salas da Turnback Cave. Alcancar o resto e trabalho de
CONEXAO de mapa (o `connections` do GBA), nao de warp, e e outro bloco.

A porta no pai
--------------
Tres caminhos, nesta ordem, e todos ja existiam no repo:
1. porta ORFA que o pai ja tem (`fecha_portas_sinnoh.portas_livres`);
2. pai convertido da grade 2D: a coordenada da fonte vale tile a tile
   (`abre_exteriores_sinnoh.boca_na_grade`);
3. desenhar, com o teste de parede de `abre_bocas_cavernas_sinnoh.candidatos`.

No caminho 3 a palavra de 16 bits ganhou uma fonte a mais que o precedente, e ela
foi precisa: `gTileset_Pasos` (o das portarias e da propria antecamara) **nao tem
metatile de porta nenhum**, so as quatro setas de warp, entao
`abre_portas_teimosas_sinnoh.palavra_ampla` devolvia None e Great Marsh 6 e
Spring Path ficavam de fora. A saida nao e inventar tile: e ler a tabela de
ATRIBUTOS do tileset, a mesma que o motor usa, e pegar a seta que casa com o lado
de onde o jogador chega. O teste de parede so aceita tile com chao andavel LOGO
ABAIXO, ou seja o jogador chega andando para o NORTE, entao a seta e
`MB_NORTH_ARROW_WARP`. Colisao e elevacao sao COPIADAS do chao de baixo, senao a
porta nasce em outra camada e o jogador nao a alcanca.

Compatibilidade de save: mapa novo no FIM de um grupo que ja existe e tem vaga,
warp novo no FIM da lista do pai, layout novo so quando o pai compartilha planta
e a porta precisa ser desenhada. Nenhum indice antigo anda.
"""
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import abre_bocas_cavernas_sinnoh as B      # noqa: E402
import abre_exteriores_sinnoh as E          # noqa: E402
import abre_portas_extras_sinnoh as A       # noqa: E402
import abre_portas_teimosas_sinnoh as T     # noqa: E402
import converte_cavernas_sinnoh as C        # noqa: E402
import converte_interiores_sinnoh as X      # noqa: E402
import fecha_portas_sinnoh as F             # noqa: E402
import importa_npcs_sinnoh as I             # noqa: E402
import valida_warp_tile as W                # noqa: E402

APLICAR = "--aplicar" in sys.argv
PLANTA = "Route226_Access"
GRUPO_BASE = "gMapGroup_IndoorSinnohPortas"
TIPOS_DE_FORA = ("MAP_TYPE_OUTDOORS", "MAP_TYPE_TOWN_CITY",
                 "MAP_TYPE_UNDERGROUND")

# Mapa de fora que esta ferramenta NAO cria, com o motivo escrito.
NAO_CRIAR = {
    # 480x480 e 156 mil tiles com colisao: e o subterraneo inteiro do Platinum,
    # que la e um sistema proprio (cavar, base secreta, radar). Uma sala de 13x9
    # chamada "Underground" mente mais do que a porta fechada.
    "MAP_HEADER_UNDERGROUND": "sistema proprio do DS, nao e mapa de andar",
}


# ------------------------------------------------------------------- fila
def fila():
    """[(pai, header)] dos exteriores que faltam e tem pai na ROM."""
    heads = I.headers_do_platinum()
    casados = X._casados(heads)
    temos = set(casados) | F.JA_TEMOS
    pastas, consts = X._consts_existentes()
    H = C.headers()

    def serve(d):
        if d in temos or d in NAO_CRIAR:
            return False
        if H.get(d, {}).get("mapType") not in TIPOS_DE_FORA:
            return False
        return (F.nome_de_pasta(d) not in pastas
                and F.const_do_header(d) not in consts)

    saida, vistos = [], set()
    for header, meu in sorted(casados.items(), key=lambda kv: kv[1]):
        if meu in A.NAO_FURAR:
            continue
        for wp in X.destinos(header, heads):
            d = wp["dest_header_id"]
            if d in vistos or not serve(d):
                continue
            vistos.add(d)
            saida.append((meu, d))
    mudou = True
    while mudou:
        mudou = False
        for _pai, header in list(saida):
            for wp in X.destinos(header, heads):
                d = wp["dest_header_id"]
                if d in vistos or not serve(d):
                    continue
                vistos.add(d)
                saida.append((F.nome_de_pasta(header), d))
                mudou = True
    return saida


# ------------------------------------------------------------------ porta
# `_corte`, `comportamento` e `palavra_do_tileset` moram no conversor de
# interiores: os dois precisam do mesmo ultimo recurso de porta, e duas copias
# viram duas verdades.
_corte = X._corte
comportamento = X.comportamento
palavra_do_tileset = X.palavra_do_tileset


def abre_porta(pai, header, heads, usados):
    """((x, y), como) da porta no pai, desenhando uma se preciso."""
    d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
    ja = usados.setdefault(pai, set())
    livres = [p for p in F.portas_livres(pai, d) if p not in ja]
    if livres:
        ja.add(livres[0])
        return livres[0], "porta orfa"

    if B.convertido_do_ds(d):
        xy = E.boca_na_grade(pai, d, header, heads)
        if xy and xy not in ja:
            if len(A.mapas_do_layout(d["layout"])) > 1:
                B.clona_layout(pai, d)
                d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
            A.libera_tile(pai, xy[0], xy[1])
            A.grava_tile(d["layout"], xy[0], xy[1], C.ESCADA)
            ja.add(xy)
            return xy, "grade do DS"

    cands = [(x, y) for x, y, _p, _a in B.candidatos(pai) if (x, y) not in ja]
    if not cands:
        return None, "nenhum tile passa no teste de parede"
    x, y = cands[0]
    palavra = T.palavra_ampla(pai) or palavra_do_tileset(pai, x, y)
    if palavra is None:
        return None, "tileset do pai nao tem porta nem seta de warp"
    if len(A.mapas_do_layout(d["layout"])) > 1:
        B.clona_layout(pai, d)
        d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
    A.libera_tile(pai, x, y)
    A.grava_tile(d["layout"], x, y, palavra)
    ja.add((x, y))
    return (x, y), "parede desenhada"


# ------------------------------------------------------------------- main
def main():
    if "--demo" in sys.argv:
        return demo()

    heads = I.headers_do_platinum()
    pend = fila()
    print(f"exteriores folha alcancaveis que faltam: {len(pend)}")
    for pai, header in pend:
        try:
            larg, alt, g = C.grade_do_header(header)
            bl = sum(1 for v in g if v & 0x8000)
            grade = f"{larg}x{alt}, {bl} com colisao"
        except Exception:
            grade = "matriz com pedaco vazio"
        print(f"   {header.replace('MAP_HEADER_', ''):32} <- {pai:34} "
              f"grade da fonte {grade}")
    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        return 0

    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    base = json.load(open(f"{REPO}/data/maps/{PLANTA}/map.json"))
    volta = E.volta_ao_mundo(PLANTA)
    incs, usados, feitos = [], {}, []
    for pai, header in pend:
        if not os.path.exists(f"{REPO}/data/maps/{pai}/map.json"):
            print(f"   PULADO {header.replace('MAP_HEADER_', '')}: "
                  f"pai {pai} nao existe")
            continue
        porta, como = abre_porta(pai, header, heads, usados)
        if porta is None:
            print(f"   PULADO {header.replace('MAP_HEADER_', '')}: {pai}: {como}")
            continue
        pasta = F.nome_de_pasta(header)
        d_pai = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        d = dict(base)
        d.pop("connections", None)
        d["id"] = F.const_do_header(header)
        d["name"] = pasta
        d["region_map_section"] = d_pai.get("region_map_section",
                                            base["region_map_section"])
        d["object_events"] = []
        d["coord_events"] = []
        d["bg_events"] = []
        # warp 0 e a volta ao mundo, convencao que `casa_voltas` do conversor de
        # caverna usa. As outras portas da planta ficam orfas de proposito.
        d["warp_events"] = [{
            "x": volta[0], "y": volta[1], "elevation": 0,
            "dest_map": d_pai["id"],
            "dest_warp_id": str(len(d_pai.get("warp_events") or []))}]
        d["origem"] = E.ORIGEM.format(planta=PLANTA)
        os.makedirs(f"{REPO}/data/maps/{pasta}", exist_ok=True)
        json.dump(d, open(f"{REPO}/data/maps/{pasta}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        open(f"{REPO}/data/maps/{pasta}/scripts.inc", "w").write(
            f"{pasta}_MapScripts::\n\t.byte 0\n")
        grupos[F.grupo_com_vaga(grupos, GRUPO_BASE)].append(pasta)
        incs.append(f'\t.include "data/maps/{pasta}/scripts.inc"\n')

        d_pai.setdefault("warp_events", []).append(
            {"x": porta[0], "y": porta[1], "elevation": 0,
             "dest_map": d["id"], "dest_warp_id": "0"})
        json.dump(d_pai, open(f"{REPO}/data/maps/{pai}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        feitos.append((pasta, pai, porta, como))

    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    with open(f"{REPO}/data/event_scripts.s", "a") as f:
        f.writelines(incs)
    for pasta, pai, porta, como in feitos:
        print(f"   {pasta:28} entra por {pai} em {porta} ({como})")
    print(f"\naplicado: {len(feitos)} exteriores provisorios")
    return 0


# --------------------------------------------------------------- autoteste
def demo():
    """O que precisa ser verdade para uma passagem provisoria valer alguma coisa."""
    # 1. a planta tem que ter porta SOBRANDO depois da volta ao mundo, senao o
    #    exterior novo nasce sem para onde crescer. Duas orfas, medidas do
    #    map.bin da Route226_Access.
    livres = F.portas_livres(PLANTA)
    assert len(livres) >= 2, livres
    assert E.volta_ao_mundo(PLANTA) == livres[0]

    # 2. a volta ao mundo tem que ser tile que DISPARA, lido da tabela do motor.
    #    A primeira versao do precedente cravou a coordenada do warp que a planta
    #    ja tinha, e ele estava em cima de `MB_NORMAL`: dava para entrar e nao
    #    dava para voltar, com validador estatico verde (licao 4.1).
    lay = F.layouts()[json.load(
        open(f"{REPO}/data/maps/{PLANTA}/map.json"))["layout"]]
    blk = open(f"{REPO}/{lay['blockdata_filepath']}", "rb").read()

    def comp(palavra):
        return comportamento(lay, palavra)
    p = struct.unpack_from("<H", blk,
                           (livres[0][1] * lay["width"] + livres[0][0]) * 2)[0]
    assert comp(p) in W.COMPORTA_WARP, (livres[0], comp(p))

    # 3. a seta do tileset e o ULTIMO recurso, e ela tem que existir e disparar
    #    no par de tilesets das portarias, que e onde `palavra_ampla` falha.
    #    Sem isto, Great Marsh 6 e Spring Path ficam de fora calados.
    assert T.palavra_ampla("SendoffSpring") is None, (
        "se um mapa passou a ter porta neste tileset, o ultimo recurso ficou "
        "sem caso de teste")
    cands = B.candidatos("SendoffSpring")
    assert cands, "SendoffSpring sem parede onde desenhar"
    x, y = cands[0][0], cands[0][1]
    palavra = palavra_do_tileset("SendoffSpring", x, y)
    assert palavra is not None
    assert comp(palavra) == W._MB["MB_NORTH_ARROW_WARP"], comp(palavra)
    assert (palavra >> 10) & 3 == 0, "porta desenhada tem que ser andavel"
    #    e a elevacao tem que ser a do chao de baixo, nao um numero escolhido
    d_ss = json.load(open(f"{REPO}/data/maps/SendoffSpring/map.json"))
    l_ss = F.layouts()[d_ss["layout"]]
    b_ss = open(f"{REPO}/{l_ss['blockdata_filepath']}", "rb").read()
    abaixo = struct.unpack_from("<H", b_ss,
                                ((y + 1) * l_ss["width"] + x) * 2)[0]
    assert (palavra & 0xF000) == (abaixo & 0xF000), (hex(palavra), hex(abaixo))

    # 4. o nome da pasta tem que cair na mesma chave do header, senao o mapa
    #    entra na ROM e `completude.py` continua contando ele como ausente.
    for _pai, header in fila():
        pasta = F.nome_de_pasta(header)
        assert (I.chave(pasta) == I.chave(header)
                or I.APELIDOS.get(pasta) == header), header

    # 5. IDEMPOTENCIA: o que ja esta na ROM nao volta para a fila.
    pend = fila()
    assert len(set(h for _p, h in pend)) == len(pend), "fila repete header"
    heads = I.headers_do_platinum()
    assert not (set(h for _p, h in pend) & set(X._casados(heads))), "fila repete mapa"

    # 6. depois de aplicado: ida e volta de verdade. O warp 0 do mapa novo cai no
    #    warp do pai que aponta de volta para ele, nos dois sentidos, e o tile de
    #    cada ponta DISPARA. Warp que existe e nao dispara ja custou uma leva
    #    inteira aqui.
    conferidos = 0
    for pasta in sorted(os.listdir(f"{REPO}/data/maps")):
        arq = f"{REPO}/data/maps/{pasta}/map.json"
        if not os.path.exists(arq):
            continue
        d = json.load(open(arq))
        if "passagem provisoria" not in (d.get("origem") or ""):
            continue
        volta = d["warp_events"][0]
        alvo = None
        for outro in os.listdir(f"{REPO}/data/maps"):
            f2 = f"{REPO}/data/maps/{outro}/map.json"
            if os.path.exists(f2):
                dd = json.load(open(f2))
                if dd["id"] == volta["dest_map"]:
                    alvo = (outro, dd)
                    break
        assert alvo, pasta
        i = int(volta["dest_warp_id"])
        assert i < len(alvo[1]["warp_events"]), (pasta, i)
        assert alvo[1]["warp_events"][i]["dest_map"] == d["id"], (pasta, i)
        for mapa, x, y in ((pasta, volta["x"], volta["y"]),
                           (alvo[0], alvo[1]["warp_events"][i]["x"],
                            alvo[1]["warp_events"][i]["y"])):
            _d, l2, w2, _h2, pal2, c2 = A._grade(mapa)
            assert c2(pal2[y * w2 + x]) in W.COMPORTA_WARP, (mapa, x, y)
        conferidos += 1
    assert conferidos >= 3, conferidos
    print(f"demo ok ({conferidos} passagens provisorias conferidas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
