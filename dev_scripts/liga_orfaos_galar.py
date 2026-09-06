#!/usr/bin/env python3
"""Warps dos órfãos de Galar: o que a FONTE sustenta, e só isso.

Uso:
    python3 dev_scripts/liga_orfaos_galar.py            # grava
    python3 dev_scripts/liga_orfaos_galar.py --seco     # só relata
    python3 dev_scripts/liga_orfaos_galar.py --censo    # a medição do diagnóstico
    python3 dev_scripts/liga_orfaos_galar.py --demo     # autoteste, sai 1 se cair

O QUE FOI MEDIDO, 06/09/2026 (lote AB da onda 1 da Frente A)
============================================================
`dev_scripts/valida_conectividade.py` acusa 246 mapas de Galar que nenhum
caminho alcança. O plano da onda supunha três causas: (1) a porta existe no
exterior mas aponta para id velho, (2) a porta do exterior se perdeu na
extração, (3) o interior é multi-andar e só o 1F tem porta. **As três medem
perto de zero.** A causa de verdade é uma quarta, e ela muda o que dá para
fazer aqui.

1. A extração é FIEL. A fonte tem 706 arestas de warp limpas entre os 438
   mapas; nós escrevemos 680 delas (96,3%). As 26 que faltam não são id velho
   nem porta perdida: em todas, o mapa de DESTINO não tem warp de chegada com
   aquele índice, porque a tabela de warps dele saiu vazia ou curta da
   extração. Das 176 conexões de rota da fonte, escrevemos **176**, nenhuma
   falta.
2. Dos 246 órfãos, **193 têm tabela de warp limpa na fonte**: eles SAEM sem
   problema. O que não existe é a porta de entrada. Na fonte:
      140 não são apontados por NINGUÉM (zero warp de entrada em toda a ROM
          do demake, dentro dos 438);
       58 só são apontados por mapa que também é órfão;
        5 são apontados por mapa vivo, mas com índice de chegada que não
          existe.
   Esses quatro números são sobre os 246 de ANTES do carimbo do B4. Rodar
   `--censo` depois dele dá 167/50/7/5 sobre os 229 que sobraram, porque as 16
   sobras saem da lista de órfãos e passam a contar como "mapa vivo" na
   classificação; é a mesma medida, com o denominador de hoje.
3. As portas do demake são COMPARTILHADAS. Os 58 `Galar_TurffieldIndoor*`
   saem, os 58, pelo MESMO warp: `Galar_Turffield04` warp 1. `Motostoke11` e
   `Motostoke01` saem os dois pela mesma porta da cidade (10,11), e a porta só
   leva a um dos dois. É a mesma família dos 4 `portas_de_mao_unica` que
   `mundo_galar.py` já tinha carimbado como "sujeira da fonte".
4. **136 órfãos têm blockdata duplicado** de outro mapa, e 77 deles são cópia
   byte a byte de um mapa VIVO (o mesmo interior de Pokécenter repetido seis
   vezes, a mesma casa genérica repetida cinquenta). São as salas de reserva
   que o autor do demake deixou na ROM sem ligar.

Conclusão medida: **ligar os 153 órfãos de campanha não é transcrever a fonte,
é INVENTAR porta** (decidir qual prédio de qual cidade leva a qual cópia da
casa genérica). Isso é desenho de conteúdo, não extração, e por isso este
script NÃO faz. Ele faz as três coisas que a fonte sustenta sozinha, e a
decisão de desenho ficou registrada no relatório do lote.

O QUE ESTE SCRIPT FAZ
=====================
B4. Carimba `cortado_por` nos 16 mapas que são SOBRA DE FIRERED dentro dos
    grupos de Galar (Lost Cave 01 a 13, Tanoby Key, câmara Liptoo e câmara
    Scufib: são as Sevii Islands do jogo base, que o demake não redesenhou e
    deixou no grupo). Decisão da condutora, 06/09/2026: ligá-las inventa mundo
    que a fonte não tem, e apagá-las mexe em índice de save. O carimbo é o
    MESMO campo que `remove_mapas_cortados.py` escreve e que
    `valida_conectividade.py` lê, e não esvazia o mapa: id, warps e objetos
    ficam onde estão, só a régua de conectividade para de cobrá-los.
    `Galar_RixyChamber01` é da mesma família e NÃO é carimbado, porque ele é
    alcançável hoje: carimbar mapa vivo seria esconder conteúdo bom.

    RESSALVA MEDIDA, e ela é do tamanho de uma decisão: as 16 NÃO são inertes.
    `Galar_TanobyKey01`, `Galar_LiptooChamber01` e `Galar_ScufibChamber01`
    carregam as portas de `Galar_CrownTundra10` a `14`, e `Galar_LostCave01` e
    `Galar_LostCave04` carregam as de `Galar_IsleOfArmor29` e `32`. São 8 portas
    boas, escritas e com índice de chegada certo, para 7 mapas distintos
    (`CrownTundra10` recebe duas), todas apontando para dentro da Crown Tundra
    e da Isle of Armor. O demake reaproveitou os slots de caverna das Sevii
    para desenhar caverna de DLC. O carimbo NÃO apaga essas portas (nada aqui
    esvazia mapa), mas tira as 16 da régua de conectividade, e com elas some da
    conta o fato de que 7 mapas de DLC dependem delas. Se a
    condutora quiser reverter, o carimbo é um campo só no `map.json` e este
    script mostra tudo com `--seco`.

R3. Liga a única porta inerte de exterior VIVO que exatamente um órfão reclama
    e ninguém mais: `Galar_WildArea20` warp 0, em (46,7). O warp 0 de
    `Galar_WildAreaIndoor01`, em (6,12), sai justo ali; hoje o warp da Wild
    Area aponta para si mesmo (porta morta) e o interior fica sem entrada.
    Apontá-lo de volta ao interior fecha ida e volta de verdade, com o par de
    índices que a própria fonte casou. É a ÚNICA porta em Galar que passa nos
    quatro filtros: exterior vivo, warp inerte hoje, reclamado por um só
    órfão, e nenhum mapa vivo disputando aquele índice de chegada.

O QUE ESTE SCRIPT NÃO FAZ, E POR QUÊ
====================================
- **Não mexe nas 4 `pendencias_warp` do tipo "chegada inexistente" que teriam
  conserto** (`Ballonlea02` warps 1 e 2, `Spikemuth05` warps 0 e 2). Elas não
  resgatam órfão nenhum (as duas pontas já estão vivas), e transformar warp
  inerte em warp vivo muda o comportamento de mapa que o jogador já pisa, em
  cima de tile que este lote não tem como validar (o `valida_mapa.py` que o
  plano cita não existe nesta árvore). Ganho zero, risco de porta sólida:
  ficam para quem tiver o validador de tile.
- **Não inventa porta.** Nenhuma linha aqui escreve warp que a fonte não case
  índice a índice.
"""
import argparse
import collections
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPAS = os.path.join(RAIZ, "data/maps")
CENSO = os.path.join(RAIZ, "dev_scripts/galar_mundo.json")

# B4: as 16 sobras de FireRed dentro dos grupos de Galar.
SOBRAS_FIRERED = (
    ["Galar_LostCave%02d" % i for i in range(1, 14)]
    + ["Galar_TanobyKey01", "Galar_LiptooChamber01", "Galar_ScufibChamber01"]
)
CARIMBO = ("sobra_firered_no_grupo_galar: Lost Cave, Tanoby Key e as camaras "
           "Liptoo e Scufib sao as Sevii Islands do FireRed base, que o demake "
           "deixou dentro dos grupos de Galar. Nao sao mapa de Galar; liga-las "
           "inventaria mundo que a fonte nao tem e apaga-las mexeria em indice "
           "de save. Decisao da condutora da Frente A, 06/09/2026, lote AB da "
           "onda 1.")

CARIMBO_DUP = ("reserva_duplicada_do_demake: o blockdata deste mapa é cópia "
               "BYTE A BYTE do de um mapa vivo, ninguém aponta warp para ele a "
               "partir de mapa que não seja órfão, nenhum script do demake o "
               "abre e ele não é ponto de cura. É uma das salas de reserva que "
               "o autor do demake deixou na ROM sem ligar (a mesma casa "
               "genérica repetida dezenas de vezes). Medido pelo lote AB2 da "
               "onda 1 da Frente A, 06/09/2026, com "
               "dev_scripts/anda_scripts_galar.py. O carimbo NÃO esvazia o mapa: "
               "id, warps e objetos ficam; só a régua de conectividade para de "
               "cobrá-los. Para reverter, apagar este campo do map.json.")
POR_SCRIPT = os.path.join(RAIZ, "dev_scripts/orfaos_galar_por_script.json")
CARIMBADOS = os.path.join(RAIZ, "dev_scripts/orfaos_galar_carimbados.txt")
SEM_SAIDA = os.path.join(RAIZ, "dev_scripts/orfaos_galar_sem_saida.txt")

# R3: (exterior vivo, indice do warp inerte, interior orfao, warp de chegada).
# Cada campo foi medido; ver o cabecalho.
PORTAS = [
    {
        "exterior": "Galar_WildArea20", "warp": 0,
        "interior": "Galar_WildAreaIndoor01", "warp_interior": 0,
        "medida": ("o warp 0 de Galar_WildAreaIndoor01, em (6,12), aponta para o "
                   "warp 0 de Galar_WildArea20, em (46,7); esse warp aponta hoje "
                   "para si mesmo e nenhum outro mapa reclama o indice"),
    },
]


def le(pasta):
    with open(os.path.join(MAPAS, pasta, "map.json"), encoding="utf-8") as f:
        return json.load(f)


def grava(pasta, doc):
    with open(os.path.join(MAPAS, pasta, "map.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")


def pasta_de_id(censo=None):
    censo = censo or json.load(open(CENSO, encoding="utf-8"))
    return {v["mapa"]: v["nome"] for v in censo["de_para"].values()}


def carimba(gravar):
    """B4. Devolve (mudados, ja_carimbados, sem_pasta)."""
    mudados, prontos, sem = [], [], []
    for pasta in SOBRAS_FIRERED:
        if not os.path.exists(os.path.join(MAPAS, pasta, "map.json")):
            sem.append(pasta)
            continue
        doc = le(pasta)
        if doc.get("cortado_por") == CARIMBO:
            prontos.append(pasta)
            continue
        doc["cortado_por"] = CARIMBO
        if gravar:
            grava(pasta, doc)
        mudados.append(pasta)
    return mudados, prontos, sem


def liga(gravar):
    """R3. Devolve (mudados, ja_ligadas, recusadas)."""
    mudados, prontos, recusadas = [], [], []
    for p in PORTAS:
        ext, dentro = le(p["exterior"]), le(p["interior"])
        we = ext.get("warp_events") or []
        wi = dentro.get("warp_events") or []
        if not (0 <= p["warp"] < len(we)) or not (0 <= p["warp_interior"] < len(wi)):
            recusadas.append((p, "indice fora da lista"))
            continue
        # A prova antes de escrever: o warp do interior tem que apontar para
        # ESTE warp do exterior. Sem isto, a porta nao e a que a fonte casou.
        volta = wi[p["warp_interior"]]
        if (volta.get("dest_map") != ext["id"]
                or str(volta.get("dest_warp_id")) != str(p["warp"])):
            recusadas.append((p, "o warp do interior nao devolve a este warp do exterior"))
            continue
        alvo = we[p["warp"]]
        if alvo.get("dest_map") == dentro["id"] and str(alvo.get("dest_warp_id")) == str(p["warp_interior"]):
            prontos.append(p)
            continue
        if alvo.get("dest_map") != ext["id"]:
            recusadas.append((p, "o warp do exterior ja leva a %s: nao e porta morta"
                              % alvo.get("dest_map")))
            continue
        alvo["dest_map"] = dentro["id"]
        alvo["dest_warp_id"] = str(p["warp_interior"])
        if gravar:
            grava(p["exterior"], ext)
        mudados.append(p)
    return mudados, prontos, recusadas


def duplicadas(gravar):
    """B5. As reservas duplicadas do demake. Devolve (mudados, prontos, motivo).

    Devolve (mudados, prontos, motivo_de_nao_rodar, sobra), em que `sobra` são
    os órfãos que NÃO são reserva e não têm entrada nenhuma: nem warp de mapa
    não órfão, nem script do demake, nem blockdata igual ao de mapa vivo. Ligar
    esses é desenho de conteúdo, não extração.

    Um órfão entra no carimbo só quando as QUATRO coisas valem ao mesmo tempo:

      1. o blockdata dele é cópia byte a byte (md5 de data/layouts/<mapa>/map.bin)
         do de pelo menos um mapa VIVO, isto é, um mapa que hoje é alcançável e
         que não está carimbado;
      2. nenhum mapa NÃO ÓRFÃO aponta warp para ele NA FONTE (não só no que
         escrevemos: se o demake tinha a porta e nós a perdemos, ele não é
         reserva, é conserto, e não pode ser carimbado). Mapa já cortado conta
         como apontador aqui, de propósito; ver o comentário abaixo;
      3. nenhum script do demake o abre, nem de mapa vivo nem de mapa órfão,
         pela medição de dev_scripts/anda_scripts_galar.py;
      4. ele não é destino de HEAL_LOCATION nenhum. Esta quarta trava é o
         conserto de um erro real desta mesma sessão: os Centros Pokémon de
         Galar são cópia byte a byte uns dos outros, e o de
         MAP_GALAR_ISLE_OF_ARMOR_04 chegou a ser carimbado como reserva
         enquanto o seletor de capítulo ainda não oferecia a heal location da
         ilha. Mapa que o motor usa como ponto de cura NUNCA é reserva, esteja
         ou não alcançável hoje.

    O item 3 depende do JSON daquele script. Sem ele, esta função NÃO carimba
    nada e diz por quê: carimbar sem a medição de script esconderia mapa que o
    demake abre por cena.
    """
    if not os.path.exists(POR_SCRIPT):
        return [], [], ("falta %s: rode dev_scripts/anda_scripts_galar.py antes"
                        % os.path.relpath(POR_SCRIPT, RAIZ))
    import hashlib
    FONTE = os.path.join(os.path.dirname(RAIZ),
                         "fontes-mapas/galar-swsh/extraidos-ultimate")
    cen = json.load(open(CENSO, encoding="utf-8"))
    dp = cen["de_para"]
    id_de = {k: v["mapa"] for k, v in dp.items()}
    pasta = {v["mapa"]: v["nome"] for v in dp.values()}
    mapas = json.load(open(os.path.join(FONTE, "mapas.json"), encoding="utf-8"))
    src = {}
    for g in mapas:
        for i, m in enumerate(g["mapas"]):
            src["g%02dm%02d" % (g["grupo"], i)] = m

    orfaos = set(orfaos_hoje())
    alcancados = set(json.load(open(POR_SCRIPT, encoding="utf-8"))["orfaos"])
    # "vivo" aqui é mapa alcançável E sem carimbo: mapa cortado não promove
    # ninguém a alcançável, senão um carimbo puxaria o próximo em cascata.
    cortado = {m for m, n in pasta.items()
               if os.path.exists(os.path.join(MAPAS, n, "map.json"))
               and le(n).get("cortado_por")}
    vivo = {m for m in pasta if m not in orfaos and m not in cortado}

    # Quem DESQUALIFICA o carimbo é todo mapa que não é órfão, e isso inclui
    # de propósito os mapas já CORTADOS: as sobras de FireRed do B4 carregam 8
    # portas boas para dentro da DLC, e um órfão que só depende delas não é
    # reserva do autor, é consequência daquele corte. Ele fica de fora daqui
    # para continuar visível na ressalva do B4, em vez de sumir com um motivo
    # errado. Sem esta linha, Galar_IsleOfArmor32 (porta em Galar_LostCave04)
    # entraria como reserva, e não é.
    apontado_por_vivo = set()
    for f in dp:
        if id_de[f] in orfaos:
            continue
        for w in src[f].get("warps") or []:
            d = "g%02dm%02d" % (w["grupo"], w["mapa"])
            if d in dp and id_de[d] != id_de[f]:
                apontado_por_vivo.add(id_de[d])

    hl = os.path.join(RAIZ, "src/data/heal_locations.json")
    curas = set()
    if os.path.exists(hl):
        for h in json.load(open(hl, encoding="utf-8"))["heal_locations"]:
            curas.add(h.get("map"))
            curas.add(h.get("respawn_map"))

    md5 = collections.defaultdict(list)
    for m, n in pasta.items():
        b = os.path.join(RAIZ, "data/layouts", n, "map.bin")
        if os.path.exists(b):
            md5[hashlib.md5(open(b, "rb").read()).hexdigest()].append(m)
    copia_de_vivo = {}
    for iguais in md5.values():
        fontes = sorted(x for x in iguais if x in vivo)
        if not fontes:
            continue
        for m in iguais:
            if m in orfaos:
                copia_de_vivo[m] = fontes

    # Mapa que JA leva este carimbo some da lista de orfaos e por isso nao passa
    # mais pelo laco abaixo. Se o texto do carimbo mudar (ele e documentacao, e
    # documentacao envelhece), a atualizacao tem que acontecer aqui, senao a
    # arvore fica com duas redacoes do mesmo motivo.
    prefixo = CARIMBO_DUP.split(":")[0]
    atualizados = []
    for m, n in sorted(pasta.items()):
        if not os.path.exists(os.path.join(MAPAS, n, "map.json")):
            continue
        doc = le(n)
        c = doc.get("cortado_por")
        if c and c.startswith(prefixo) and c != CARIMBO_DUP:
            doc["cortado_por"] = CARIMBO_DUP
            if gravar:
                grava(n, doc)
            atualizados.append(n)

    mudados, prontos, sobra = [], [], []
    for m in sorted(orfaos):
        if (m not in copia_de_vivo or m in alcancados
                or m in apontado_por_vivo or m in curas):
            # O que não é reserva e não tem entrada nenhuma é o trabalho de
            # desenho que sobra: ninguém aponta warp para ele, nenhum script o
            # abre, e o mapa não é cópia de nada vivo.
            if (m not in alcancados and m not in apontado_por_vivo
                    and m not in copia_de_vivo):
                sobra.append((pasta[m], m))
            continue
        n = pasta[m]
        doc = le(n)
        if doc.get("cortado_por"):
            prontos.append((n, m, copia_de_vivo[m]))
            continue
        doc["cortado_por"] = CARIMBO_DUP
        if gravar:
            grava(n, doc)
        mudados.append((n, m, copia_de_vivo[m]))
    if atualizados:
        print("B5: texto do carimbo atualizado em %d mapas" % len(atualizados))
    return mudados, prontos, None, sobra


def escreve_carimbados(mudados):
    """A lista do que ficou carimbado em Galar, por motivo. Lê do disco."""
    cen = json.load(open(CENSO, encoding="utf-8"))
    linhas = ["# Mapas de Galar com `cortado_por` no map.json, lidos do disco.",
              "# Gerado por dev_scripts/liga_orfaos_galar.py. O carimbo tira o",
              "# mapa da régua de conectividade e NÃO esvazia nada: id, warps e",
              "# objetos continuam onde estão.", ""]
    por_motivo = collections.defaultdict(list)
    for v in sorted(cen["de_para"].values(), key=lambda x: x["nome"]):
        arq = os.path.join(MAPAS, v["nome"], "map.json")
        if not os.path.exists(arq):
            continue
        c = le(v["nome"]).get("cortado_por")
        if c:
            por_motivo[c.split(":")[0]].append((v["nome"], v["mapa"]))
    for motivo in sorted(por_motivo):
        linhas.append("%s  (%d)" % (motivo, len(por_motivo[motivo])))
        for n, m in por_motivo[motivo]:
            linhas.append("  %-34s %s" % (n, m))
        linhas.append("")
    with open(CARIMBADOS, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    return sum(len(v) for v in por_motivo.values())


def escreve_sem_saida(sobra):
    """A lista do desenho que sobra. Ver o docstring de duplicadas()."""
    with open(SEM_SAIDA, "w", encoding="utf-8") as f:
        f.write("# Órfãos de Galar que sobram DE VERDADE, gerado por\n"
                "# dev_scripts/liga_orfaos_galar.py. Critério: nenhum mapa NÃO\n"
                "# ÓRFÃO aponta warp para eles na fonte, nenhum script do demake os\n"
                "# abre (dev_scripts/anda_scripts_galar.py) e o blockdata deles não\n"
                "# é cópia byte a byte de mapa vivo. Ligar estes é DESENHO DE\n"
                "# CONTEÚDO, não extração: a fonte não tem porta para dar.\n#\n")
        f.write("# %d mapas.\n\n" % len(sobra))
        for n, m in sobra:
            f.write("%-34s %s\n" % (n, m))
    return len(sobra)


# ------------------------------------------------------------------ o censo --

def censo():
    """A medição do cabeçalho, refeita da fonte. Não escreve nada."""
    FONTE = os.path.join(os.path.dirname(RAIZ),
                         "fontes-mapas/galar-swsh/extraidos-ultimate")
    cen = json.load(open(CENSO, encoding="utf-8"))
    dp = cen["de_para"]
    id_de = {k: v["mapa"] for k, v in dp.items()}
    f_de_id = {v["mapa"]: k for k, v in dp.items()}
    mapas = json.load(open(os.path.join(FONTE, "mapas.json"), encoding="utf-8"))
    comp = json.load(open(os.path.join(FONTE, "complemento.json"), encoding="utf-8"))
    src = {}
    for g in mapas:
        for i, m in enumerate(g["mapas"]):
            src["g%02dm%02d" % (g["grupo"], i)] = m
    suj = json.load(open(os.path.join(FONTE, "galar_sujeira.json"), encoding="utf-8"))
    sujos = collections.defaultdict(set)
    for r in suj["reprovados"]:
        if r["tipo"] == "warps":
            sujos[r["mapa"]].add(r["i"])
    limpos = {n: [j for j in range(len(src[n].get("warps") or []))
                  if j not in sujos[n]] for n in dp}
    pos = {n: {j: p for p, j in enumerate(limpos[n])} for n in limpos}
    doc = {v["mapa"]: le(v["nome"]) for v in dp.values()}

    orfaos = orfaos_hoje()
    print("orfaos de Galar hoje: %d" % len(orfaos))

    # 1. fidelidade da extracao
    arestas_fonte, escritas = set(), set()
    for n in dp:
        for i, w in enumerate(src[n].get("warps") or []):
            if i in sujos[n]:
                continue
            d = "g%02dm%02d" % (w["grupo"], w["mapa"])
            if d in dp:
                arestas_fonte.add((n, d))
        for w in doc[id_de[n]].get("warp_events") or []:
            if w.get("dest_map") in f_de_id:
                escritas.add((n, f_de_id[w["dest_map"]]))
    print("arestas de warp limpas na fonte: %d; escritas por nos: %d; perdidas: %d"
          % (len(arestas_fonte), len(arestas_fonte & escritas),
             len(arestas_fonte - escritas)))
    cx_fonte = cx_escritas = 0
    DIR = {1: "down", 2: "up", 3: "left", 4: "right"}
    for n in dp:
        nossas = {(c["direction"], c["map"])
                  for c in (doc[id_de[n]].get("connections") or [])}
        for c in ((comp.get(n) or {}).get("conexoes") or []):
            d = "g%02dm%02d" % (c["grupo"], c["mapa"])
            if d in dp and c["direcao"] in DIR:
                cx_fonte += 1
                cx_escritas += (DIR[c["direcao"]], id_de[d]) in nossas
    print("conexoes da fonte: %d; escritas: %d" % (cx_fonte, cx_escritas))

    # 2. por que cada orfao esta sem entrada
    entra = collections.defaultdict(list)
    for P in dp:
        for i, w in enumerate(src[P].get("warps") or []):
            d = "g%02dm%02d" % (w["grupo"], w["mapa"])
            if d in dp:
                entra[d].append((P, i, w["warp_id"], i in sujos[P]))
    classe = collections.Counter()
    for oid in orfaos:
        o = f_de_id.get(oid)
        if o is None:
            classe["fora dos 438"] += 1
            continue
        vivas = [x for x in entra[o] if not x[3]]
        de_vivo = [x for x in vivas if id_de[x[0]] not in orfaos]
        if any(x[2] not in pos[o] for x in de_vivo):
            classe["apontado por mapa vivo, mas o indice de chegada nao existe"] += 1
        elif de_vivo:
            classe["apontado por mapa vivo com porta viva"] += 1
        elif vivas:
            classe["so apontado por mapa que tambem e orfao"] += 1
        else:
            classe["NINGUEM aponta para ele na fonte"] += 1
    for k, v in classe.most_common():
        print("  %4d  %s" % (v, k))

    # 3. blockdata duplicado
    import hashlib
    h = collections.defaultdict(list)
    for v in dp.values():
        p = os.path.join(RAIZ, "data/layouts", v["nome"], "map.bin")
        if os.path.exists(p):
            h[hashlib.md5(open(p, "rb").read()).hexdigest()].append(v["mapa"])
    dup = {k: v for k, v in h.items() if len(v) > 1}
    orf_dup = [m for v in dup.values() for m in v if m in orfaos]
    orf_dup_vivo = [m for v in dup.values() for m in v
                    if m in orfaos and any(x not in orfaos for x in v)]
    print("orfaos com blockdata duplicado: %d, dos quais copia de mapa VIVO: %d"
          % (len(orf_dup), len(orf_dup_vivo)))
    return 0


def orfaos_hoje():
    """Os orfaos de Galar, pela MESMA regra de valida_conectividade.py."""
    if os.path.join(RAIZ, "dev_scripts") not in sys.path:
        sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
    import re
    from collections import deque
    import valida_conectividade as VC
    mapas = VC.carrega()
    saidas = {}
    for origem, info in mapas.items():
        viz = set()
        for w in info["dados"].get("warp_events") or []:
            d = w.get("dest_map", "")
            if d in ("MAP_NONE", "MAP_DYNAMIC", "") or d not in mapas:
                continue
            n = len(mapas[d]["dados"].get("warp_events") or [])
            try:
                alvo = int(w.get("dest_warp_id", 0))
            except (TypeError, ValueError):
                continue
            if 0 <= alvo < n:
                viz.add(d)
        for c in info["dados"].get("connections") or []:
            if c.get("map") in mapas:
                viz.add(c["map"])
        for d in info["dados"].get("destinos_dinamicos") or []:
            if d in mapas:
                viz.add(d)
        inc = os.path.join(VC.MAPS, info["dir"], "scripts.inc")
        if os.path.exists(inc):
            t = open(inc, encoding="utf-8", errors="replace").read()
            for d in VC.RE_WARP_DE_SCRIPT.findall(t):
                if d in mapas:
                    viz.add(d)
        saidas[origem] = viz
    for conj in VC.transportes_por_special(mapas):
        for a in conj:
            saidas.setdefault(a, set()).update(conj - {a})
    sementes = {VC.mapa_de_partida(mapas)} | VC.sementes_do_seletor(mapas)
    vis = set(sementes)
    fila = deque(sorted(sementes))
    while fila:
        a = fila.popleft()
        for v in saidas.get(a, ()):
            if v not in vis:
                vis.add(v)
                fila.append(v)
    return sorted(m for m, i in mapas.items()
                  if i["dir"].startswith("Galar_")
                  and not i["dados"].get("cortado_por")
                  and not i["dir"].endswith("ConnectionDummy")
                  and m not in vis)


def autoteste():
    falhou = []

    def confere(o_que, deu, esperado):
        ok = deu == esperado
        print("  %-56s %s  (%s)" % (o_que, "OK" if ok else "CAIU", deu))
        if not ok:
            falhou.append(o_que)

    confere("sobras de FireRed na lista", len(SOBRAS_FIRERED), 16)
    confere("sobras que existem em disco",
            sum(1 for p in SOBRAS_FIRERED
                if os.path.exists(os.path.join(MAPAS, p, "map.json"))), 16)
    # RixyChamber e da mesma familia e NAO pode estar carimbado: ele e alcancavel.
    confere("Galar_RixyChamber01 fora da lista",
            "Galar_RixyChamber01" in SOBRAS_FIRERED, False)
    confere("Galar_RixyChamber01 sem carimbo",
            bool(le("Galar_RixyChamber01").get("cortado_por")), False)
    m, p, s = carimba(False)
    confere("sobras sem pasta", s, [])
    confere("sobras carimbadas depois de rodar", len(m) + len(p), 16)
    mu, pr, re_ = liga(False)
    confere("portas recusadas", [(x[0]["exterior"], x[1]) for x in re_], [])
    confere("portas no plano", len(mu) + len(pr), len(PORTAS))
    # A ressalva do B4, travada: as 5 sobras abaixo carregam 8 portas boas para
    # dentro da DLC (7 mapas distintos; CrownTundra10 recebe duas). Se este
    # numero mudar, a ressalva do cabecalho envelheceu.
    portadoras = ("Galar_TanobyKey01", "Galar_LiptooChamber01",
                  "Galar_ScufibChamber01", "Galar_LostCave01", "Galar_LostCave04")
    boas = 0
    for p in portadoras:
        d = le(p)
        for w in d.get("warp_events") or []:
            alvo = w.get("dest_map", "")
            if ("CROWN_TUNDRA" in alvo or "ISLE_OF_ARMOR" in alvo) and alvo != d["id"]:
                boas += 1
    confere("portas das sobras para dentro da DLC", boas, 8)
    du, dpr, falta, sobra = duplicadas(False)
    confere("B5 tem a medição de script para rodar", falta, None)
    if falta is None:
        # Toda candidata do B5 tem que ser copia de mapa vivo E estar fora da
        # lista de alcancados por script. Se alguma nao for, a regra vazou.
        alc = set(json.load(open(POR_SCRIPT, encoding="utf-8"))["orfaos"])
        confere("nenhuma candidata do B5 é alcançada por script",
                sorted(m for _, m, _ in du if m in alc), [])
        confere("toda candidata do B5 tem mapa vivo de origem",
                sorted(m for _, m, f in du if not f), [])
        hl = os.path.join(RAIZ, "src/data/heal_locations.json")
        curas = {h.get("map") for h in json.load(open(hl, encoding="utf-8"))["heal_locations"]}
        confere("nenhuma candidata do B5 é ponto de cura",
                sorted(m for _, m, _ in du if m in curas), [])
    print("\n%s" % ("autoteste: tudo de pé" if not falhou
                    else "autoteste: %d caiu" % len(falhou)))
    return 1 if falhou else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seco", action="store_true", help="nao escreve nada")
    ap.add_argument("--censo", action="store_true", help="so a medicao do diagnostico")
    ap.add_argument("--demo", action="store_true", help="autoteste")
    ap.add_argument("--autoteste", action="store_true", help="autoteste")
    args = ap.parse_args()
    if args.demo or args.autoteste:
        return autoteste()
    if args.censo:
        return censo()

    gravar = not args.seco
    m, p, s = carimba(gravar)
    print("B4 sobras de FireRed: %d carimbadas agora, %d ja estavam, %d sem pasta"
          % (len(m), len(p), len(s)))
    for x in m:
        print("   +", x)
    mu, pr, re_ = liga(gravar)
    print("R3 portas: %d ligadas agora, %d ja estavam, %d recusadas"
          % (len(mu), len(pr), len(re_)))
    for x in mu:
        print("   + %s warp %d -> %s warp %d"
              % (x["exterior"], x["warp"], x["interior"], x["warp_interior"]))
    for x, motivo in re_:
        print("   ! %s warp %d: %s" % (x["exterior"], x["warp"], motivo))

    du, dp_, falta, sobra = duplicadas(gravar)
    if falta:
        print("B5 reservas duplicadas: NÃO rodou (%s)" % falta)
    else:
        print("B5 reservas duplicadas: %d carimbadas agora, %d ja estavam"
              % (len(du), len(dp_)))
        for n, m, fontes in du:
            print("   + %-34s cópia de %s" % (n, ", ".join(fontes[:2])))
        if gravar:
            n = escreve_carimbados(du)
            print("   lista com %d mapas em %s"
                  % (n, os.path.relpath(CARIMBADOS, RAIZ)))
            escreve_sem_saida(sobra)
        print("órfãos que sobram DE VERDADE (sem warp, sem script, sem "
              "duplicata): %d" % len(sobra))
    return 0


if __name__ == "__main__":
    sys.exit(main())
