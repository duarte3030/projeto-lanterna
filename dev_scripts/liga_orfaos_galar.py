#!/usr/bin/env python3
"""Warps dos órfãos de Galar: o que a FONTE sustenta, e só isso.

Uso:
    python3 dev_scripts/liga_orfaos_galar.py            # grava
    python3 dev_scripts/liga_orfaos_galar.py --seco     # só relata
    python3 dev_scripts/liga_orfaos_galar.py --censo    # a medição do diagnóstico
    python3 dev_scripts/liga_orfaos_galar.py --demo     # autoteste, sai 1 se cair
    python3 dev_scripts/liga_orfaos_galar.py --pendentes  # so a marcacao dos sem fonte

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

P1. Marca os mapas que a fonte deixou SEM ENTRADA NENHUMA como pendentes de
    fonte, em `dev_scripts/orfaos_galar_pendente_fonte.json`. Decisão do Gui,
    06/09/2026 (resposta 40): eles NÃO são cortados e NÃO ganham porta
    inventada; ficam marcados para serem desenvolvidos depois, e a busca por
    fonte continua (`fontes-mapas/galar-swsh/FONTES-ORFAOS.md`).

    A marcação é DOCUMENTO, não corte: ela não escreve `cortado_por`, não
    toca em `map.json` nenhum e não tira ninguém do denominador. A régua de
    órfãos de Galar de `valida_conectividade.py` continua contando os mesmos
    mapas de antes; a linha nova ("pendentes de fonte") só EXPLICA parte
    deles. Quem quiser conferir: rode o validador antes e depois, a contagem
    de Galar não muda.

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


# ------------------------------------------------- os pendentes de fonte --

# Decisao do Gui, 06/09/2026 (resposta 40): os mapas de Galar que a fonte
# deixou sem entrada nenhuma NAO sao cortados e NAO ganham porta inventada.
# Eles ficam MARCADOS como pendentes de fonte, para serem desenvolvidos
# depois, e a busca por fonte continua. Este bloco escreve a marcacao.
#
# O que a marcacao NAO faz, de proposito: ela nao escreve `cortado_por` em
# mapa nenhum, nao mexe em `map.json` e nao tira ninguem do denominador. A
# regua de orfaos de Galar continua contando os mesmos 132 de
# `valida_conectividade.py`; a linha nova so EXPLICA 42 deles.
MOTIVO_PENDENTE = "sem_entrada_na_fonte"
DATA_PENDENTE = "2026-09-06"
PENDENTE_FONTE = os.path.join(RAIZ, "dev_scripts/orfaos_galar_pendente_fonte.json")

# O palpite do que cada mapa e em Sword/Shield. E INFERENCIA, marcada [P] no
# documento de fontes (fontes-mapas/galar-swsh/FONTES-ORFAOS.md), e sai daqui:
# do tileset, do tamanho, da secao da fonte, dos objetos e de para onde o mapa
# SAI. Nao e leitura de documento do autor do demake, e por isso nao decide
# nada sozinho: quem for desenhar a porta confere antes.
PALPITE = {
    "Galar_GalarMine04": "galeria curta e reta da Galar Mine; sai na Galar Mine 02, que e viva",
    "Galar_GalarMine05": "camara larga da Galar Mine com tres NPCs; sai duas vezes na Galar Mine 02, que e viva",
    "Galar_IsleOfArmor15": "casca de 1x1 sem tile, sem warp e sem objeto: slot vazio que o autor reservou na Isle of Armor",
    "Galar_Motostoke21": "interior generico de casa de cidade, copia byte a byte de Wedgehurst14 e Wedgehurst15; sai na porta compartilhada de Wedgehurst04",
    "Galar_Postwick06": "sala grande de predio com 17 NPCs, tileset dos interiores de Turffield; o unico warp aponta para si mesmo",
    "Galar_Postwick07": "copia byte a byte de Postwick06, mesmo warp morto",
    "Galar_Postwick11": "sala pequena de caverna com dois warps mortos e dois itens escondidos",
    "Galar_Postwick111": "andar de caverna com 20 NPCs, copia byte a byte de Postwick03, Postwick112 e Postwick113; warp morto",
    "Galar_Postwick112": "copia byte a byte de Postwick111",
    "Galar_Postwick113": "copia byte a byte de Postwick111",
    "Galar_Postwick172": "variante 68% igual a Postwick06 e Postwick07, mesmo warp morto",
    "Galar_Postwick23": "casca de 1x1, blockdata igual ao de outras cascas vazias",
    "Galar_Postwick24": "casca de 1x1 unica, sem gemeo",
    "Galar_Postwick26": "lasca de rota 70x30, 98% igual ao Slumbering Weald 02, sem warp e sem objeto",
    "Galar_Postwick31": "predio alto e estreito, 20x100, com tres warps que saem todos no mesmo warp 2 de Wedgehurst12",
    "Galar_Postwick34": "casca de 1x1",
    "Galar_Postwick37": "casca de 2x2, igual a Hammerlocke24",
    "Galar_Postwick38": "casca de 1x1, do mesmo molde de Postwick23",
    "Galar_Postwick40": "lasca de exterior 48x48 com seis NPCs e zero warp",
    "Galar_Postwick45": "casca de 1x1",
    "Galar_Postwick46": "interior enorme, 55x63, tileset que so Hulbury01 usa; sai em Hulbury01 e na porta compartilhada de Wedgehurst04",
    "Galar_Postwick47": "lasca da Wild Area 48x47 com sete NPCs e dois warps mortos; na fonte, e ela que aponta para Postwick50",
    "Galar_Postwick49": "lasca da Wild Area 48x48 com um warp morto",
    "Galar_Postwick50": "lasca da Wild Area 48x48 com 63 warps, TODOS apontando para si mesmos: a laje de covis que o autor nunca ligou",
    "Galar_Postwick53": "lasca de rota 58x19 com quatro NPCs e zero warp",
    "Galar_Postwick58": "interior 25x17 com doze NPCs e zero warp",
    "Galar_Route0204": "trecho grande da Rota 2, 90x60, com as duas conexoes da fonte escritas (Rota 2 02 a direita, Rota 1 01 embaixo); os vizinhos e que nao conectam de volta",
    "Galar_StowOnSide03": "interior 11x29 com seis NPCs, copia byte a byte de StowOnSide02, e zero warp",
    "Galar_Wedgehurst13": "interior 95% igual ao de Motostoke01, que e Centro Pokemon; sai em Wedgehurst03, Wedgehurst05 e Wedgehurst04",
    "Galar_Wedgehurst14": "copia byte a byte de Motostoke21 e Wedgehurst15; sai na porta compartilhada de Wedgehurst04",
    "Galar_Wedgehurst15": "copia byte a byte de Motostoke21 e Wedgehurst14; sai na porta compartilhada de Wedgehurst04",
    "Galar_WildArea01": "laje da Wild Area 60x70 com 22 NPCs, 96% igual a WildArea22; sai no warp 2 de Hammerlocke04, que e vivo",
    "Galar_WildArea02": "laje da Wild Area 26x126, 99% igual a WildArea21 e a WildArea12; a conexao para Wyndon01 esta escrita, Wyndon01 e que nao conecta de volta",
    "Galar_WildArea12": "laje da Wild Area 26x126, blockdata praticamente igual ao de WildArea21, sem warp e sem conexao",
    "Galar_WildArea18": "laje da Wild Area 29x83 que faz par com WildAreaCave01; HOJE ja e alcancada por script, ver o campo alcancado_hoje",
    "Galar_WildArea23": "laje da Wild Area 49x65 com sete NPCs; sai no warp 0 de WildArea10, que e vivo",
    "Galar_WildArea25": "clareira 25x25 do tileset de Ballonlea, warp morto",
    "Galar_WildArea26": "clareira 25x25 do mesmo molde, 94% igual a WildArea25, warp morto",
    "Galar_WildArea27": "laje da Wild Area 48x47 com nove NPCs, zero warp e um item escondido",
    "Galar_WildArea28": "clareira 25x25, copia byte a byte de WildArea29, warp morto",
    "Galar_WildArea29": "clareira 25x25, copia byte a byte de WildArea28, warp morto",
    "Galar_WildAreaCave01": "caverna 58x50 que faz par com WildArea18; HOJE ja e alcancada, ver o campo alcancado_hoje",
}

CLASSES = {
    "porta_no_exterior": (
        "o mapa SAI para um mapa vivo, com indice de chegada valido: sabemos "
        "exatamente em que exterior a porta entra. O que falta e o tile de "
        "warp no exterior, porque o indice que a fonte usou ja e de outro "
        "mapa vivo (as portas do demake sao compartilhadas)."),
    "conexao_de_borda_de_mao_unica": (
        "a conexao de borda da fonte esta escrita neste mapa, mas o vizinho "
        "nao conecta de volta. Falta a conexao reciproca no vizinho."),
    "warp_morto_aponta_para_si": (
        "o mapa tem tile de warp, e o warp aponta para o proprio mapa. A "
        "fonte nunca escreveu o par: falta a escada ou a porta dos DOIS "
        "lados, e nada diz onde ela entra."),
    "sobra_vazia": (
        "casca de 1x1 ou 2x2, zero warp, zero objeto: slot que o autor "
        "reservou na ROM e nunca desenhou. Sem correspondente em SwSh."),
    "sobra_sem_porta": (
        "o mapa tem blockdata e as vezes NPC, mas zero warp e zero conexao "
        "em qualquer direcao. A fonte nao tem porta para dar."),
    "ja_alcancado": (
        "estava nesta lista quando ela foi gerada, mas HOJE a regua de "
        "`valida_conectividade.py` ja o alcanca. Fica marcado para nao sumir "
        "calado, e nao conta como pendencia de desenho."),
}


def _dados_do_mapa(nome, cen):
    """Tudo que da para MEDIR de um mapa de Galar, sem inferir nada."""
    v = next(x for x in cen["de_para"].values() if x["nome"] == nome)
    doc = le(nome)
    return v, doc


def pendentes_de_fonte(gravar):
    """Monta a marcacao dos mapas sem entrada na fonte. Devolve o documento.

    Le a lista de `orfaos_galar_sem_saida.txt` (que este mesmo script gera) e,
    para cada mapa, mede: o que ele e pelo blockdata e pelo tamanho, quantos
    objetos tem, para onde ele SAI, que conexoes de borda tem escritas, e de
    que outros mapas ele e copia (exata pelo md5, parcial pela fracao de
    metatiles iguais entre mapas do MESMO tamanho).
    """
    import hashlib
    cen = json.load(open(CENSO, encoding="utf-8"))
    dp = cen["de_para"]
    pasta = {v["mapa"]: v["nome"] for v in dp.values()}
    # `orfaos_hoje()` fala em MAP_*, e o resto deste bloco fala em nome de
    # pasta. Sem esta tabela a comparação sai sempre falsa e TODO mapa
    # apareceria como já alcançado, que foi o primeiro jeito errado disto.
    id_de = {v["nome"]: v["mapa"] for v in dp.values()}
    secao = {int(k): v for k, v in cen["secoes"].items()}

    lista = []
    for linha in open(SEM_SAIDA, encoding="utf-8"):
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            lista.append(linha.split()[0])

    # Estado de cada mapa HOJE, pela mesma regra da regua.
    # Aqui vale a regua PUBLICA, a mesma que `valida_conectividade.py` mostra:
    # a marcacao existe para explicar o numero que o Gui ve, e explicar um
    # numero com outra regua seria mentir de boa fe. Ver orfaos_hoje().
    orfaos_agora = set(orfaos_hoje(com_scripts_de_galar=True))
    cortados = set()
    for m, n in pasta.items():
        arq = os.path.join(MAPAS, n, "map.json")
        if os.path.exists(arq) and le(n).get("cortado_por"):
            cortados.add(n)

    def estado(n):
        if n in cortados:
            return "cortado"
        return "orfao" if id_de.get(n) in orfaos_agora else "vivo"

    # Blockdata de todo mundo, uma vez so.
    corpo, digest = {}, {}
    for v in dp.values():
        b = os.path.join(RAIZ, "data/layouts", v["nome"], "map.bin")
        if os.path.exists(b):
            corpo[v["nome"]] = open(b, "rb").read()
            digest[v["nome"]] = hashlib.md5(corpo[v["nome"]]).hexdigest()
    por_digest = collections.defaultdict(list)
    for n, h in digest.items():
        por_digest[h].append(n)

    def copias(nome):
        b = corpo.get(nome)
        if b is None:
            return [], []
        exatas = sorted(x for x in por_digest[digest[nome]] if x != nome)
        parciais = []
        if len(b) >= 32:
            for outro, b2 in corpo.items():
                if outro == nome or outro in exatas or len(b2) != len(b):
                    continue
                iguais = sum(1 for i in range(0, len(b), 2)
                             if b[i:i + 2] == b2[i:i + 2])
                pct = round(100.0 * iguais / (len(b) // 2))
                if pct >= 60:
                    parciais.append({"mapa": outro, "metatiles_iguais_pct": pct})
            parciais.sort(key=lambda x: (-x["metatiles_iguais_pct"], x["mapa"]))
        return exatas, parciais[:3]

    itens = []
    for nome in lista:
        v, doc = _dados_do_mapa(nome, cen)
        warps = doc.get("warp_events") or []
        mortos, saidas = [], []
        for i, w in enumerate(warps):
            alvo = w.get("dest_map", "")
            if alvo == doc["id"]:
                mortos.append({"warp": i, "x": w.get("x"), "y": w.get("y")})
                continue
            if alvo in pasta:
                saidas.append({"warp": i, "x": w.get("x"), "y": w.get("y"),
                               "sai_em": pasta[alvo], "sai_em_id": alvo,
                               "warp_de_chegada": str(w.get("dest_warp_id")),
                               "estado_do_destino": estado(pasta[alvo])})
        conexoes = [{"direcao": c.get("direction"),
                     "vizinho": pasta.get(c.get("map"), c.get("map")),
                     "estado_do_vizinho": estado(pasta.get(c.get("map"), ""))
                     if c.get("map") in pasta else "?"}
                    for c in (doc.get("connections") or [])]
        exatas, parciais = copias(nome)
        vivas = [s for s in saidas if s["estado_do_destino"] == "vivo"]

        eh_orfao = id_de[nome] in orfaos_agora
        if not eh_orfao:
            classe = "ja_alcancado"
        elif vivas:
            classe = "porta_no_exterior"
        elif any(c["estado_do_vizinho"] == "vivo" for c in conexoes):
            classe = "conexao_de_borda_de_mao_unica"
        elif mortos:
            classe = "warp_morto_aponta_para_si"
        elif v["w"] * v["h"] <= 4 and not warps and not (doc.get("object_events") or []):
            classe = "sobra_vazia"
        else:
            classe = "sobra_sem_porta"

        if classe == "porta_no_exterior":
            n_w = len(vivas)
            custo = ("%s no exterior %s"
                     % ("porta de 1 warp" if n_w == 1 else "porta de %d warps" % n_w,
                        ", ".join(sorted({s["sai_em"] for s in vivas}))))
        elif classe == "conexao_de_borda_de_mao_unica":
            custo = ("conexao de borda reciproca em %s"
                     % ", ".join(c["vizinho"] for c in conexoes
                                 if c["estado_do_vizinho"] == "vivo"))
        elif classe == "warp_morto_aponta_para_si":
            custo = ("escada ou porta dos dois lados: %s aqui, e o par que a "
                     "fonte nunca escreveu"
                     % ("1 warp morto" if len(mortos) == 1
                        else "%d warps mortos" % len(mortos)))
        elif classe == "sobra_vazia":
            custo = "sem correspondente em SwSh: casca vazia, sobra do autor"
        elif classe == "ja_alcancado":
            custo = "nenhum: a regua de hoje ja alcanca este mapa"
        else:
            custo = "sem correspondente em SwSh: sobra do autor, sem porta na fonte"

        sec = secao.get(v["secao_fonte"]) or {}
        itens.append({
            "pasta": nome,
            "mapa": v["mapa"],
            "mapsec": v["region_map_section"],
            "mapsec_real": sec.get("mapsec_real"),
            "lugar_na_fonte": sec.get("slug"),
            "fonte": "g%02dm%02d" % (v["fonte_grupo"], v["fonte_indice"]),
            "nome_antes_do_g3": v["nome_no_g2"],
            "map_type": doc.get("map_type"),
            "largura": v["w"], "altura": v["h"], "area_em_tiles": v["w"] * v["h"],
            "warps": len(warps),
            "warps_mortos": mortos,
            "saidas": saidas,
            "conexoes": conexoes,
            "objetos": len(doc.get("object_events") or []),
            "bg_events": len(doc.get("bg_events") or []),
            "tileset_primario": v["primary_tileset"],
            "tileset_secundario": v["secondary_tileset"],
            "musica": v["music"],
            "copia_exata_de": exatas,
            "copia_parcial_de": parciais,
            "orfao_hoje": eh_orfao,
            "classe": classe,
            "custo_estimado": custo,
            "o_que_e_palpite": PALPITE.get(nome, ""),
            "motivo": MOTIVO_PENDENTE,
            "data": DATA_PENDENTE,
        })

    resumo = collections.Counter(i["classe"] for i in itens)
    doc = {
        "gerado_por": "dev_scripts/liga_orfaos_galar.py --pendentes",
        "data": DATA_PENDENTE,
        "decisao": (
            "Gui, 06/09/2026, resposta 40: os mapas de Galar que a fonte deixou "
            "sem entrada nenhuma NAO sao cortados e NAO ganham porta inventada. "
            "Ficam marcados como pendentes de fonte, para serem desenvolvidos "
            "depois, e a busca por fonte continua."),
        "o_que_esta_marcacao_nao_faz": (
            "nao escreve cortado_por, nao mexe em map.json e nao tira ninguem do "
            "denominador. A regua de orfaos de Galar de valida_conectividade.py "
            "continua contando os mesmos mapas; esta lista so EXPLICA parte deles."),
        "motivo": MOTIVO_PENDENTE,
        "fonte_da_lista": os.path.relpath(SEM_SAIDA, RAIZ),
        "busca_de_fonte": "fontes-mapas/galar-swsh/FONTES-ORFAOS.md",
        "classes": CLASSES,
        "total": len(itens),
        "ainda_orfaos": sum(1 for i in itens if i["orfao_hoje"]),
        "resumo_por_classe": dict(sorted(resumo.items())),
        "mapas": itens,
    }
    if gravar:
        with open(PENDENTE_FONTE, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")
    return doc


def le_pendentes():
    """(total, ainda orfaos, {MAP_*}) da marcacao. ({}, se ela nao existe.)

    E por aqui que `valida_conectividade.py` le a lista: ele nunca recalcula
    nada daqui, so mostra numa linha propria quantos dos orfaos de Galar ja
    tem motivo conhecido. Se o arquivo nao existir, devolve zeros e a regua
    segue igual, sem quebrar.
    """
    if not os.path.exists(PENDENTE_FONTE):
        return 0, 0, set()
    try:
        d = json.load(open(PENDENTE_FONTE, encoding="utf-8"))
    except (ValueError, OSError):
        return 0, 0, set()
    ids = {m.get("mapa") for m in d.get("mapas") or [] if m.get("mapa")}
    return d.get("total", len(ids)), d.get("ainda_orfaos", 0), ids

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


def orfaos_hoje(com_scripts_de_galar=False):
    """Os orfaos de Galar. Duas reguas, e a diferenca entre elas importa.

    `com_scripts_de_galar=False` (o padrao, e o que o B5 usa desde o lote AB2)
    NAO le `data/scripts/galar_*.inc`. E a regra ESTRITA: um mapa so conta
    como alcancado por caminho que o proprio `map.json` ou o `scripts.inc` da
    pasta dele declara. Ela e de proposito mais dura que a regua publica,
    porque carimbar mapa como reserva do autor com base em cena de script e
    justamente o erro que aquele lote nao quis cometer.

    `com_scripts_de_galar=True` e a regra PUBLICA, identica a de
    `valida_conectividade.py`: soma os warps que os `data/scripts/galar_*.inc`
    abrem. E a que o Gui ve no numero de orfaos de Galar, e por isso e a que
    a marcacao de pendentes de fonte usa para dizer quem ainda esta na conta.
    Medido em 06/09/2026: a estrita acha 141 e a publica acha 132; os 9 de
    diferenca sao alcancados por cena.
    """
    if os.path.join(RAIZ, "dev_scripts") not in sys.path:
        sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
    import re
    from collections import deque
    import valida_conectividade as VC
    mapas = VC.carrega()
    de_galar = VC.warps_de_script_de_galar(mapas) if com_scripts_de_galar else {}
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
        if com_scripts_de_galar:
            for d in de_galar.get(info["dir"], ()):
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
    # P1, a marcação dos pendentes de fonte. O que precisa estar de pé:
    # ela cobre a lista inteira, classifica TODO mundo, não inventa mapa que
    # não existe, e sobretudo NÃO carimba nada (marcação é documento, não
    # corte: se um `cortado_por` vazasse daqui, a régua de órfãos encolheria
    # sozinha e o Gui perderia de vista o trabalho que sobrou).
    lista_txt = [l.split()[0] for l in open(SEM_SAIDA, encoding="utf-8")
                 if l.strip() and not l.startswith("#")]
    pend = pendentes_de_fonte(False)
    confere("P1 cobre a lista de sem-saída inteira",
            pend["total"], len(lista_txt))
    confere("P1 tem a mesma ordem e os mesmos mapas",
            [m["pasta"] for m in pend["mapas"]] == lista_txt, True)
    # As duas reguas de orfaos_hoje() nao podem colapsar numa so: a publica
    # tem que enxergar MENOS orfao que a estrita, senao ler os
    # `data/scripts/galar_*.inc` deixou de valer alguma coisa.
    estrita, publica = len(orfaos_hoje()), len(orfaos_hoje(True))
    confere("a regua publica de orfaos e mais frouxa que a estrita",
            estrita > publica, True)
    confere("P1 classifica todo mundo",
            sorted({m["classe"] for m in pend["mapas"]} - set(CLASSES)), [])
    confere("P1 dá custo estimado a todo mundo",
            [m["pasta"] for m in pend["mapas"] if not m["custo_estimado"]], [])
    confere("P1 dá motivo único a todo mundo",
            sorted({m["motivo"] for m in pend["mapas"]}), [MOTIVO_PENDENTE])
    confere("P1 não carimba cortado_por em ninguém",
            [m["pasta"] for m in pend["mapas"]
             if le(m["pasta"]).get("cortado_por")], [])
    # A trava que importa para a régua: todo pendente que ainda é órfão tem
    # que ESTAR na lista de órfãos de valida_conectividade.py, senão a linha
    # nova estaria explicando mapa que a régua nem cobra.
    confere("P1 soma bate com o resumo por classe",
            sum(pend["resumo_por_classe"].values()), pend["total"])
    confere("P1 conta certo quem ainda é órfão",
            sum(1 for m in pend["mapas"] if m["orfao_hoje"]),
            pend["ainda_orfaos"])
    # E o que le_pendentes() devolve tem que ser o que o arquivo em disco diz;
    # é essa função que valida_conectividade.py chama.
    if os.path.exists(PENDENTE_FONTE):
        tot, orf, ids = le_pendentes()
        disco = json.load(open(PENDENTE_FONTE, encoding="utf-8"))
        confere("le_pendentes bate com o arquivo em disco",
                (tot, orf, len(ids)),
                (disco["total"], disco["ainda_orfaos"], len(disco["mapas"])))
    else:
        print("  %-56s %s" % ("le_pendentes: arquivo ainda não gerado",
                              "rode --pendentes"))

    print("\n%s" % ("autoteste: tudo de pé" if not falhou
                    else "autoteste: %d caiu" % len(falhou)))
    return 1 if falhou else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seco", action="store_true", help="nao escreve nada")
    ap.add_argument("--censo", action="store_true", help="so a medicao do diagnostico")
    ap.add_argument("--demo", action="store_true", help="autoteste")
    ap.add_argument("--pendentes", action="store_true",
                    help="so a marcacao dos mapas sem entrada na fonte")
    ap.add_argument("--autoteste", action="store_true", help="autoteste")
    args = ap.parse_args()
    if args.demo or args.autoteste:
        return autoteste()
    if args.censo:
        return censo()
    if args.pendentes:
        d = pendentes_de_fonte(True)
        print("pendentes de fonte: %d (%d ainda órfãos hoje)"
              % (d["total"], d["ainda_orfaos"]))
        for classe, n in sorted(d["resumo_por_classe"].items()):
            print("  %4d  %s" % (n, classe))
        print("  lista em %s" % os.path.relpath(PENDENTE_FONTE, RAIZ))
        return 0

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

    # P1. A marcação dos que a fonte deixou sem entrada. Vem DEPOIS do B5 de
    # propósito: ela lê `orfaos_galar_sem_saida.txt`, que o B5 acabou de
    # reescrever, e assim a marcação nunca fica falando de uma lista velha.
    d = pendentes_de_fonte(gravar)
    print("P1 pendentes de fonte: %d (%d ainda órfãos hoje), %s"
          % (d["total"], d["ainda_orfaos"],
             os.path.relpath(PENDENTE_FONTE, RAIZ)))
    for classe, n in sorted(d["resumo_por_classe"].items()):
        print("   %4d  %s" % (n, classe))
    return 0


if __name__ == "__main__":
    sys.exit(main())
