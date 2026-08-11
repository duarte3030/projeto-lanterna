#!/usr/bin/env python3
"""Abre os tres EXTERIORES que travam ~32 interiores de masmorra de Sinnoh.

    python3 dev_scripts/abre_exteriores_sinnoh.py            # so relata
    python3 dev_scripts/abre_exteriores_sinnoh.py --aplicar  # escreve
    python3 dev_scripts/abre_exteriores_sinnoh.py --demo     # autoteste

O buraco que ele fecha
----------------------
`converte_cavernas_sinnoh.py` so cria uma masmorra quando ela e destino de warp
de um mapa que JA esta na ROM. Medido em 06/08/2026: Turnback Cave (22 salas),
Iron Island (7) e Stark Mountain (3) tem chao de masmorra de verdade na grade 2D
do Platinum e convertem hoje, e o que falta nao e a masmorra: e o mapa DE FORA
por onde se entra em cada uma. Sem ele a fila do conversor da zero.

Por que a planta e REAPROVEITADA e nao convertida
-------------------------------------------------
Decisao ja registrada no ESTADO: exterior de gen 4 tem cenario DESENHADO que a
grade 2D nao carrega, e converter exterior com o motor de caverna enche a rua de
parede de pedra ao ar livre. Entao aqui a planta sai do proprio repo: a mesma
antecamara `Route226_Access` que Sinnoh ja usa como passagem, 13x9. O PRIMEIRO
tile de porta orfa dela devolve o jogador ao mundo e os que sobram ficam orfaos
de proposito, que e exatamente o que `fecha_portas_sinnoh.portas_livres` procura
e o que faz o conversor de caverna achar entrada.

Qual tile devolve ao mundo sai medido, nunca de gosto
-----------------------------------------------------
A primeira versao deste script cravou (6,4), que e onde a `Route226_Access`
original tem o warp dela de volta para a Route226. Medido depois de aplicar:
aquele tile e `MB_NORMAL`, warp MORTO que nunca disparou (a saida de la e
scriptada pelo marinheiro). Os tres exteriores nasceram com entrada boa e SEM
saida: dava para entrar na masmorra e nao dava para voltar ao mundo, que e a
licao 4.1 do ESTADO outra vez, com validador estatico verde. Agora a volta sai
de `F.portas_livres(planta)`, que le o comportamento do tile no `map.bin`, e o
`--demo` exige duas portas: uma para voltar, pelo menos uma para a masmorra.

A `Route226_Access` tem exatamente duas (`MB_WEST_ARROW_WARP` em (1,5) e
`MB_EAST_ARROW_WARP` em (11,5)), entao cada exterior abre UMA masmorra. Isso
custa o atalho direto IronIsland -> Iron Island B3F que o Platinum tem; nao
custa mapa nenhum, porque o B3F tambem se alcanca por B1F Right -> B2F Left,
conferido na fonte.

Cada `map.json` novo grava isso no campo `origem`. Nao ha NPC, placa nem texto:
coordenada de exterior no Platinum e GLOBAL da matriz de Sinnoh e nao ha offset
que alinhe (decisao 5 de `importa_npcs_sinnoh.py`), entao NPC importado cairia
em qualquer lugar dentro de uma sala de 13x9. O que importa e chegar no lugar,
entrar na masmorra, sair dela e voltar ao mundo.

A boca no mapa pai
------------------
Route214, CanalaveCity e Route227 nao tem porta orfa nenhuma. A boca sai pela
mesma regra ja medida em `abre_bocas_cavernas_sinnoh.py`: tile bloqueado, com
chao andavel logo abaixo, no meio de uma parede, em mancha de area >= 8, e a
palavra de 16 bits e COPIADA de uma porta nao animada do proprio mapa. Nenhum
dos tres pais tem warp para o exterior na fonte, entao a posicao cai no criterio
de desempate honesto de `escolhe`: penhasco primeiro, mancha maior depois.

Compatibilidade de save: mapa novo no FIM de um grupo que JA existe e tem vaga,
warp novo no FIM da lista do pai, nenhum layout novo. Nenhum indice antigo anda.
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import abre_bocas_cavernas_sinnoh as B   # noqa: E402
import abre_portas_extras_sinnoh as A    # noqa: E402
import converte_cavernas_sinnoh as C     # noqa: E402
import fecha_portas_sinnoh as F          # noqa: E402
import importa_npcs_sinnoh as I          # noqa: E402

APLICAR = "--aplicar" in sys.argv

# Grupo que ja existe e tem vaga. O de cavernas fica reservado para as masmorras
# que estes tres exteriores destravam, que sao ~32.
GRUPO_BASE = "gMapGroup_IndoorSinnohPortas"

ORIGEM = ("passagem provisoria: planta reaproveitada de {planta} do repo, "
          "so para dar entrada e saida na masmorra. Exterior do Platinum nao e "
          "convertido, ver o topo de abre_exteriores_sinnoh.py")

# (header do Platinum, pai nosso, planta do repo)
EXTERIORES = [
    ("MAP_HEADER_SENDOFF_SPRING",           "Route214",     "Route226_Access"),
    ("MAP_HEADER_IRON_ISLAND",              "CanalaveCity", "Route226_Access"),
    ("MAP_HEADER_STARK_MOUNTAIN_OUTSIDE",   "Route227",     "Route226_Access"),
    # O pai aqui e caverna CONVERTIDA da grade 2D, nao rua: a boca sai pela
    # coordenada da fonte (ver `boca_na_grade`), nao pelo teste de parede. Este
    # exterior destrava `MT_CORONET_4F_ROOMS_1_AND_2`, 323 tiles de chao de
    # masmorra na grade do Platinum, que e filho SO dos dois Mt. Coronet Outside
    # e por isso nunca apareceu na fila do conversor.
    ("MAP_HEADER_MT_CORONET_OUTSIDE_SOUTH", "MtCoronet3F",  "Route226_Access"),
]


def volta_ao_mundo(planta):
    """O tile da planta que devolve o jogador, medido do `map.bin`.

    E a primeira porta ORFA. Cravar a coordenada do warp que a planta ja tem
    seria errado: na `Route226_Access` aquele warp esta em cima de `MB_NORMAL` e
    nunca disparou.
    """
    livres = F.portas_livres(planta)
    if len(livres) < 2:
        raise SystemExit(f"{planta}: precisa de 2 portas orfas, tem {len(livres)}")
    return livres[0]


def pendentes():
    """Os exteriores que ainda nao estao na ROM."""
    pastas = set(os.listdir(f"{REPO}/data/maps"))
    return [e for e in EXTERIORES if F.nome_de_pasta(e[0]) not in pastas]


def boca_na_grade(pai, d_pai, header, heads):
    """(x, y) da escada quando o PAI tambem saiu da grade 2D do Platinum.

    E o caso 1 de `abre_bocas_cavernas_sinnoh`: os dois lados sao a mesma grade,
    entao a coordenada da fonte vale aqui tile a tile e nao ha por que cacar
    parede. O teste de parede so existe porque coordenada de RUA no Platinum e
    global da matriz de Sinnoh e nao tem offset que alinhe; dentro de caverna
    convertida esse problema nao existe.

    Devolve None, e ai o chamador cai no teste de parede, se a coordenada da
    fonte nao servir. Tres motivos, e cada um ja custou um mapa antes:

    - fora do mapa: matriz do DS maior que a nossa;
    - ja ocupada por outro warp deste mapa (medido em `MtCoronet4FRoom3`, onde a
      saida da fonte para o Outside North e justamente o tile que o conversor
      gastou como volta para o 5F);
    - fora do corpo andavel principal: a boca da gen 4 costuma ser um bolsao
      solto na grade 2D, e o jogador chegaria preso numa fresta (medido em
      `MtCoronet1FTunnelRoom`, cujo (2,58) nao encosta nos 305 tiles do corpo).
    """
    ph = B.header_do_mapa(pai, d_pai, heads)
    pe = (os.path.join(C.PLAT, "res/field/events", heads[ph][0] + ".json")
          if ph else None)
    if not pe or not os.path.exists(pe):
        return None
    _d, _l, w, h, pal, _c = A._grade(pai)
    regiao = C.regiao_principal(pal, w, h)
    ja = {(e["x"], e["y"]) for e in (d_pai.get("warp_events") or [])}
    for wp in json.load(open(pe)).get("warp_events", []):
        if wp["dest_header_id"] != header:
            continue
        x, z = int(wp["x"]), int(wp["z"])
        if not (0 <= x < w and 0 <= z < h) or (x, z) in ja:
            continue
        if z * w + x in regiao:
            return x, z
    return None


def main():
    if "--demo" in sys.argv:
        return demo()

    heads = I.headers_do_platinum()
    planos = []
    usados = {}
    for header, pai, planta in pendentes():
        d_pai = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        na_grade = (boca_na_grade(pai, d_pai, header, heads)
                    if B.convertido_do_ds(d_pai) else None)
        if na_grade and na_grade not in set(usados.get(pai, [])):
            # tile ja andavel: a palavra e a ESCADA de caverna do conversor, e
            # nao a porta de casa do tileset geral que `B.palavra` devolveria
            # aqui. Escada dispara ao pisar; a boca de caverna (519) e
            # MB_SOUTH_ARROW_WARP e so dispara com o jogador VINDO DE CIMA, que
            # nao e o caso de um tile no meio do chao.
            escolha, forcada, como = (na_grade[0], na_grade[1], False, 0), \
                C.ESCADA, "grade do DS"
        else:
            cands = [c for c in B.candidatos(pai)
                     if (c[0], c[1]) not in set(usados.get(pai, []))]
            escolha = B.escolhe(cands, B.ancoras(pai, d_pai, heads), None)
            if escolha is None:
                print(f"   {pai}: nenhum tile passa no teste de boca")
                continue
            forcada, como = None, "penhasco" if escolha[2] else "parede"
        usados.setdefault(pai, []).append((escolha[0], escolha[1]))
        planos.append((header, pai, planta, volta_ao_mundo(planta), escolha,
                       forcada, como))

    print(f"exteriores que faltam: {len(pendentes())}")
    for header, pai, planta, _v, esc, _f, como in planos:
        print(f"   {F.nome_de_pasta(header):24} planta {planta:16} "
              f"entra por {pai} ({esc[0]},{esc[1]}) {como}")
    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        return 0

    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    incs = []
    for header, pai, planta, volta, esc, forcada, _como in planos:
        pasta = F.nome_de_pasta(header)
        d_pai = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        # a boca vai no map.bin do PAI. Layout exclusivo dele, conferido: sem
        # isso, desenhar aqui mudaria todo mapa que compartilha a planta.
        assert len(A.mapas_do_layout(d_pai["layout"])) == 1, pai
        A.grava_tile(d_pai["layout"], esc[0], esc[1],
                     forcada or B.palavra(pai, None))

        base = json.load(open(f"{REPO}/data/maps/{planta}/map.json"))
        d = dict(base)
        d.pop("connections", None)
        d["id"] = F.const_do_header(header)
        d["name"] = pasta
        d["region_map_section"] = d_pai.get("region_map_section",
                                            base["region_map_section"])
        d["object_events"] = []
        d["coord_events"] = []
        d["bg_events"] = []
        # warp 0 e a volta ao mundo, que e a convencao que o conversor de
        # caverna usa (`casa_voltas`). As outras portas da planta ficam orfas.
        d["warp_events"] = [{"x": volta[0], "y": volta[1], "elevation": 0,
                             "dest_map": d_pai["id"],
                             "dest_warp_id": str(len(d_pai.get("warp_events") or []))}]
        d["origem"] = ORIGEM.format(planta=planta)
        os.makedirs(f"{REPO}/data/maps/{pasta}", exist_ok=True)
        json.dump(d, open(f"{REPO}/data/maps/{pasta}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        open(f"{REPO}/data/maps/{pasta}/scripts.inc", "w").write(
            f"{pasta}_MapScripts::\n\t.byte 0\n")
        grupos[F.grupo_com_vaga(grupos, GRUPO_BASE)].append(pasta)
        incs.append(f'\t.include "data/maps/{pasta}/scripts.inc"\n')

        d_pai.setdefault("warp_events", []).append(
            {"x": esc[0], "y": esc[1], "elevation": 0,
             "dest_map": d["id"], "dest_warp_id": "0"})
        json.dump(d_pai, open(f"{REPO}/data/maps/{pai}/map.json", "w"),
                  indent=2, ensure_ascii=False)

    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    with open(f"{REPO}/data/event_scripts.s", "a") as f:
        f.writelines(incs)
    print(f"\naplicado: {len(planos)} exteriores provisorios, "
          f"{len(planos)} bocas abertas no pai")
    return 0


def demo():
    """O que precisa ser verdade para os tres exteriores servirem de entrada."""
    # 1. a planta reaproveitada tem que ter porta SOBRANDO depois da volta ao
    #    mundo, senao o conversor de caverna nao acha entrada e o exterior nasce
    #    inutil. Duas orfas em Route226_Access, medidas do map.bin.
    for _h, _p, planta in EXTERIORES:
        livres = F.portas_livres(planta)
        assert len(livres) >= 2, (planta, livres)
        assert volta_ao_mundo(planta) == livres[0], planta
    # 2. o pai tem que ter layout EXCLUSIVO: a boca e escrita no map.bin, que e
    #    do layout e nao do mapa.
    for _h, pai, _pl in EXTERIORES:
        d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        assert A.mapas_do_layout(d["layout"]) == [pai], pai
    # 3. o pai tem que ter ONDE por a boca, por um dos dois caminhos. Sem isso o
    #    exterior nao teria como ser alcancado a pe.
    #    Nao exigir `B.candidatos` de todo pai: em caverna convertida a boca sai
    #    da coordenada da fonte, e cacar parede la seria trocar dado por
    #    heuristica.
    heads = I.headers_do_platinum()
    for header, pai, _pl in EXTERIORES:
        d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        assert (B.candidatos(pai)
                or boca_na_grade(pai, d, header, heads)), pai
    # 3b. no pai convertido da grade 2D, a coordenada da fonte tem que cair em
    #     chao ANDAVEL e dentro do corpo principal, senao a escada entrega o
    #     jogador preso numa fresta, e a palavra escrita tem que ter
    #     comportamento de warp de verdade, lida da mesma tabela do motor.
    #     A boca de caverna (519) NAO serve aqui: e MB_SOUTH_ARROW_WARP, so
    #     dispara com o jogador vindo de cima. A ESCADA dispara ao pisar.
    prim, _ = F._atributos("gTileset_GeneralSinnoh")
    seg, _ = F._atributos("gTileset_CaveSinnoh")
    mt = C.ESCADA & 0x3FF
    tab, rel = (prim, mt) if mt < 512 else (seg, mt - 512)
    assert tab[rel] in B.W.COMPORTA_WARP, (hex(C.ESCADA), tab[rel])
    #     O fato e lido do DADO nos dois estados, nunca de uma copia: enquanto o
    #     exterior esta pendente vale a coordenada da fonte, e depois de aplicado
    #     vale o warp que ficou no pai. Assim o teste nao reprova o proprio
    #     conserto quando a fila zera (licao 4.11 do ESTADO).
    for header, pai, _pl in EXTERIORES:
        d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        if not B.convertido_do_ds(d):
            continue
        _dd, _l, w, h, pal, _c = A._grade(pai)
        const = F.const_do_header(header)
        pontos = [(e["x"], e["y"]) for e in (d.get("warp_events") or [])
                  if e["dest_map"] == const]
        if not pontos:
            xy = boca_na_grade(pai, d, header, heads)
            assert xy, (pai, header)
            pontos = [xy]
        regiao = C.regiao_principal(pal, w, h)
        for x, y in pontos:
            assert not ((pal[y * w + x] >> 10) & 3), (pai, (x, y))
            assert y * w + x in regiao, (pai, (x, y))
    # 4. o nome da pasta tem que cair na mesma chave do header, senao o mapa
    #    entra na ROM e `completude.py` continua contando ele como ausente, e
    #    pior: o conversor de caverna nao reconhece o pai e nao cria nada.
    for header, _p, _pl in EXTERIORES:
        pasta = F.nome_de_pasta(header)
        assert (I.chave(pasta) == I.chave(header)
                or I.APELIDOS.get(pasta) == header), header
    # 5. cada exterior tem que ser, na fonte, o pai de masmorra de verdade. Se
    #    nao for, este script esta abrindo passagem para nada.
    for header, _p, _pl in EXTERIORES:
        pe = os.path.join(C.PLAT, "res/field/events", heads[header][0] + ".json")
        filhos = [w["dest_header_id"]
                  for w in json.load(open(pe)).get("warp_events", [])]
        masmorras = 0
        for f in set(filhos):
            try:
                _l, _a, g = C.grade_do_header(f)
            except ValueError:
                continue                  # matriz com pedaco NONE: exterior
            if C.chao_de_caverna(g) >= 8:
                masmorras += 1
        assert masmorras >= 1, (header, filhos)
    # 6. depois de aplicado, o mapa novo tem que ter porta orfa de verdade e o
    #    warp 0 tem que devolver ao pai. E o que o conversor de caverna consome.
    for header, pai, _pl in EXTERIORES:
        pasta = F.nome_de_pasta(header)
        arq = f"{REPO}/data/maps/{pasta}/map.json"
        if not os.path.exists(arq):
            continue
        d = json.load(open(arq))
        d_pai = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        assert d["warp_events"][0]["dest_map"] == d_pai["id"], pasta
        i = int(d["warp_events"][0]["dest_warp_id"])
        assert d_pai["warp_events"][i]["dest_map"] == d["id"], (pasta, i)
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
