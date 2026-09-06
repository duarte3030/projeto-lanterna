#!/usr/bin/env python3
"""Warps dos órfãos de Galar: o que a FONTE sustenta, e só isso.

Uso:
    python3 dev_scripts/liga_orfaos_galar.py            # grava
    python3 dev_scripts/liga_orfaos_galar.py --seco     # só relata
    python3 dev_scripts/liga_orfaos_galar.py --censo    # a medição do diagnóstico
    python3 dev_scripts/liga_orfaos_galar.py --demo     # autoteste, sai 1 se cair
    python3 dev_scripts/liga_orfaos_galar.py --pendentes  # so a marcacao dos sem fonte
    python3 dev_scripts/liga_orfaos_galar.py --escadas --seco     # so lista
    python3 dev_scripts/liga_orfaos_galar.py --escadas --aplicar  # grava os pares

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

N1. `--escadas` (onda 4, 06/09/2026). Procura o par das 14 marcadas
    `warp_morto_aponta_para_si`, pela regra de nome e geometria da condutora,
    com o tile conferido pelo comportamento do metatile. RESULTADO MEDIDO:
    liga zero. Nenhum dos 78 warps mortos delas está sobre escada ou porta, e
    em 11 dos 14 o mapa inteiro não tem tile que dispare warp. A regra está
    escrita por extenso no cabeçalho do próprio modo, junto com a medição que
    derrubou a premissa e com o que a FONTE de fato escreveu para cada uma.
    O modo não escreve `map.json` sem par válido; ele mede, recusa e registra
    a medição em `orfaos_galar_pendente_fonte.json`.

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
import re
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

    # A SOBRA SAI PELA REGUA PUBLICA, e o carimbo continua pela estrita.
    # ------------------------------------------------------------------
    # Decisao da condutora da onda 4, 06/09/2026 (lote N). Sao duas perguntas
    # diferentes e por isso duas reguas:
    #
    #   - CARIMBAR mapa como reserva do autor e irreversivel na pratica (some
    #     do denominador), entao continua na regua ESTRITA, que nao aceita cena
    #     de script como prova de alcance. E o cuidado que o lote AB2 escreveu.
    #   - A LISTA `orfaos_galar_sem_saida.txt` e documento: ela existe para
    #     explicar o numero de orfaos de Galar que o Gui LE em
    #     `valida_conectividade.py`, e esse numero sai da regua PUBLICA, que
    #     soma os `data/scripts/galar_*.inc`. Explicar um numero com outra
    #     regua e mentir de boa fe, e era o que fazia `Galar_WildArea18` e
    #     `Galar_WildAreaCave01` aparecerem como pendencia de desenho sendo que
    #     a regua publica ja os alcanca (a classe `ja_alcancado`).
    #
    # Nada aqui muda carimbo nenhum: so a lista, e por tabela quem entra na
    # marcacao de pendentes de fonte, que le esta lista.
    orfaos_pub = set(orfaos_hoje(com_scripts_de_galar=True))
    vivo_pub = {m for m in pasta if m not in orfaos_pub and m not in cortado}
    copia_de_vivo_pub = {}
    for iguais in md5.values():
        fontes = sorted(x for x in iguais if x in vivo_pub)
        if not fontes:
            continue
        for m in iguais:
            if m in orfaos_pub:
                copia_de_vivo_pub[m] = fontes
    apontado_por_vivo_pub = set()
    for f in dp:
        if id_de[f] in orfaos_pub:
            continue
        for w in src[f].get("warps") or []:
            d = "g%02dm%02d" % (w["grupo"], w["mapa"])
            if d in dp and id_de[d] != id_de[f]:
                apontado_por_vivo_pub.add(id_de[d])
    sobra_pub = [(pasta[m], m) for m in sorted(orfaos_pub)
                 if m not in alcancados and m not in apontado_por_vivo_pub
                 and m not in copia_de_vivo_pub and m not in curas]
    return mudados, prontos, None, sobra_pub


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
                "# CONTEÚDO, não extração: a fonte não tem porta para dar.\n"
                "#\n"
                "# A régua aqui é a PÚBLICA desde a onda 4 (06/09/2026): a mesma de\n"
                "# valida_conectividade.py, que soma os data/scripts/galar_*.inc.\n"
                "# Antes era a estrita, e por isso a lista trazia mapa que a régua\n"
                "# do dia já alcançava. O carimbo de reserva do B5 continua na\n"
                "# régua estrita, de propósito: são perguntas diferentes.\n#\n")
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
        "o mapa tem warp, e o warp aponta para o proprio mapa. CORRIGIDO pelo "
        "lote N da onda 4, 06/09/2026, que mediu tile a tile: o nome desta "
        "classe promete escada, e escada nao ha. Nenhum dos 78 warps mortos "
        "destes mapas esta sobre escada, escada rolante ou porta (73 em "
        "MB_NORMAL, 5 deles solidos; 2 em MB_CAVE), e em 11 dos 14 o mapa "
        "inteiro nao tem um unico tile que dispare warp. A fonte TAMBEM nao "
        "e omissa como se dizia: ela escreveu destino para 12 dos 17 warps "
        "mortos dos mapas de um warp so, mas o destino aponta para sobra de "
        "FireRed que nao importamos, ou para indice de chegada que nao "
        "existe. Ligar qualquer um exige DESENHAR tile de porta ou escada no "
        "blockdata, que e a decisao de desenho da resposta 40."),
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
            custo = ("desenhar tile de porta ou escada no blockdata: %s "
                     "aqui, e nenhum deles esta sobre tile que dispare "
                     "(medido pelo lote N da onda 4)"
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

    # ARMADILHA que este bloco tinha e o lote N da onda 4 fechou: esta funcao
    # REMONTA o documento do zero a cada rodada. Sem as tres linhas abaixo, a
    # proxima rodada em modo padrao apagaria calada tudo que o modo --escadas
    # anotou (a medicao de tile, o que a fonte diz e o par escrito), e o
    # arquivo voltaria a repetir a premissa que a medicao derrubou. O que a
    # onda 4 escreveu e MEDICAO, nao derivado: ele viaja junto.
    antes = {}
    if os.path.exists(PENDENTE_FONTE):
        try:
            _velho = json.load(open(PENDENTE_FONTE, encoding="utf-8"))
            antes = {m.get("pasta"): m for m in (_velho.get("mapas") or [])}
        except (ValueError, OSError):
            _velho, antes = {}, {}
    else:
        _velho = {}
    for i in itens:
        a = antes.get(i["pasta"]) or {}
        for campo in ("escadas_onda4", "ligado_na_onda_4"):
            if campo in a:
                i[campo] = a[campo]
        if a.get("classe") == CLASSE_LIGADO:
            i["classe"] = CLASSE_LIGADO

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
    if _velho.get("onda_4"):
        doc["onda_4"] = _velho["onda_4"]
    if CLASSE_LIGADO in (_velho.get("classes") or {}):
        doc["classes"] = dict(doc["classes"])
        doc["classes"][CLASSE_LIGADO] = _velho["classes"][CLASSE_LIGADO]
    if gravar:
        with open(PENDENTE_FONTE, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")
    return doc


# ----------------------------------------------------- as escadas da onda 4 --

# A REGRA DO MODO `--escadas`, escrita antes de qualquer linha de codigo, e a
# decisao da condutora da onda 4 da Frente A (06/09/2026):
#
#   As 14 marcadas `warp_morto_aponta_para_si` seriam interiores de varios
#   andares em que o tile de escada existe mas o warp aponta para o proprio
#   mapa, porque a fonte nunca escreveu o par. O par seria dedutivel pelo NOME
#   (andar N <-> N+1 da mesma familia) e pela GEOMETRIA (escada na mesma
#   coluna/linha, ou espelhada). Para cada warp morto, procurar o mapa irmao da
#   mesma familia com numero adjacente que tambem tenha escada livre, e ligar
#   os dois com ida e volta. Par ambiguo (dois candidatos) NAO se liga: fica
#   registrado com os candidatos.
#
# Duas travas, e a primeira decide quase tudo:
#
#   1. TILE. Ninguem e ligado sem que o tile embaixo do warp seja da familia de
#      escada ou porta pelo COMPORTAMENTO do metatile, e sem que ele DISPARE
#      (`valida_warp_tile.warp_morto`, a mesma tabela da `lente_portas`). Ligar
#      warp em cima de MB_NORMAL escreve um par que o motor nunca executa: o
#      mapa continua inalcancavel e a regua passa a mentir que ele foi ligado.
#   2. AMBIGUIDADE. Dois candidatos que passam na geometria e empate, e empate
#      nao se resolve no chute.
#
# O QUE A MEDICAO DESTE LOTE DISSE, e ela derruba a premissa (06/09/2026) [V]
# ------------------------------------------------------------------------
# Nenhuma das 14 tem escada embaixo do warp. Medido tile a tile com a Grade da
# `lente_portas`, os 17 warps mortos das 14 caem assim:
#
#     13 em MB_NORMAL (piso liso), 3 deles SOLIDO (colisao 1, o jogador nem
#        pisa: Postwick111, 112, 113 e os dois de Postwick47)
#      4 em MB_CAVE / MB_NORMAL de laje (Postwick11, Postwick49, Postwick50)
#      0 em MB_LADDER, MB_*_STAIR_WARP, MB_*_ESCALATOR ou porta
#
# Mais forte ainda: em 11 das 14, o mapa INTEIRO nao tem um unico tile que
# dispare warp. Nao e escada sem par; e mapa sem escada. So `Galar_Postwick11`
# (1 tile MB_LADDER em (11,7)) e `Galar_Postwick47` (2 escadas e 1 porta) tem
# tile de escada em algum lugar, e em nenhum dos dois o warp esta em cima dele.
#
# A leitura de tile nao esta quebrada: nos mesmos moldes, 993 dos 1.468 warps
# de Galar (67,6%) caem em tile que dispara, com 44 MB_LADDER e 28 escadas
# diagonais entre eles. Boa noticia suspeita conferida, e ela e real.
#
# E A FONTE TEM DESTINO, so que ele nao serve (medido em mapas.json) [V]
# ----------------------------------------------------------------------
# A classe dizia "a fonte nunca escreveu o par". Errado: a fonte escreveu
# destino para 12 dos 17 warps mortos. O que a fonte nao tem e destino
# UTILIZAVEL:
#
#   7 mapas apontam para mapa que NAO importamos, porque nao e de Galar:
#     Postwick06, 07 e 172 -> g0m0, secao "Celadon Dept."; Postwick111, 112 e
#     113 -> g3m58, "Outcast Island"; Postwick11 -> g1m115 e g1m119, "Dotted
#     Hole". Sao sobras de FireRed dentro da ROM do demake, a mesma familia do
#     carimbo B4. Ligar para elas era importar mapa de Kanto para dentro de
#     Galar.
#   4 apontam para `Galar_WildArea03` warp 13, e esse mapa tem 7 warps: o
#     indice de chegada nao existe (WildArea25, 26, 28 e 29).
#   2 tem tabela de warp LIXO na fonte, lida fora do fim do vetor (Postwick49 e
#     Postwick50, com coordenadas do tipo (-30648,-30624) e 225 warps).
#   Sobra 1 par que resolve dentro de Galar: Postwick47 -> Postwick50 warps 0 e
#     1. Mas os dois warps de chegada de Postwick50 estao em (0,0), em
#     MB_NORMAL, dentro dos 63 warps-lixo dele, e os dois de Postwick47 estao
#     em tile SOLIDO. Ligar isso e escrever par que nao dispara em nenhuma das
#     duas pontas.
#
# Conclusao medida: as 14 nao sao escada faltando. Sao mapa sem tile de escada,
# com destino que aponta para fora de Galar ou para indice que nao existe.
# Ligar qualquer uma delas exige DESENHAR tile de porta ou escada no blockdata,
# que e a mesma decisao de desenho que a resposta 40 do Gui adiou, e este modo
# nao faz. Ele mede, recusa e registra, que e o que a regra manda.
ESCADA_MB = ("MB_LADDER", "MB_UP_ESCALATOR", "MB_DOWN_ESCALATOR",
             "MB_UP_RIGHT_STAIR_WARP", "MB_UP_LEFT_STAIR_WARP",
             "MB_DOWN_RIGHT_STAIR_WARP", "MB_DOWN_LEFT_STAIR_WARP")
PORTA_MB = ("MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR", "MB_WATER_DOOR",
            "MB_DEEP_SOUTH_WARP")
CLASSE_ESCADA = "warp_morto_aponta_para_si"
CLASSE_LIGADO = "ligado_na_onda_4"
# Acima disto, a tabela da fonte ou a lista de warps mortos vira resumo.
TETO_FONTE = 8


def _familia(nome):
    """'Galar_Postwick111' -> ('Galar_Postwick', 111); (nome, None) sem numero."""
    m = re.match(r"^(.*?)(\d+)$", nome)
    if not m:
        return nome, None
    return m.group(1), int(m.group(2))


def _geometria_casa(a, b):
    """A escada de `b` cai na mesma coluna/linha de `a`, ou na espelhada.

    Espelhada de proposito: o 2F de um interior costuma ser desenhado como
    imagem espelhada do 1F, e cravar so 'mesma coluna' perderia esse caso.
    """
    razoes = []
    if a["x"] == b["x"]:
        razoes.append("mesma coluna x=%d" % a["x"])
    if a["y"] == b["y"]:
        razoes.append("mesma linha y=%d" % a["y"])
    if b["w"] and b["x"] == b["w"] - 1 - a["x"]:
        razoes.append("coluna espelhada %d<->%d" % (a["x"], b["x"]))
    if b["h"] and b["y"] == b["h"] - 1 - a["y"]:
        razoes.append("linha espelhada %d<->%d" % (a["y"], b["y"]))
    return razoes


def par_de_escada(alvo, candidatos):
    """A REGRA, pura: sem disco, sem json, testavel pelo --demo.

    `alvo` e `candidatos` sao registros medidos:
        nome, familia, numero, warp, x, y, w, h, comportamento, dispara, livre

    Devolve (escolhido, motivo, considerados). `motivo` e um de:
    'ligado', 'tile_nao_e_escada', 'sem_irmao', 'ambiguo'.
    """
    if not alvo.get("dispara"):
        return None, "tile_nao_e_escada", []
    vale = []
    for c in candidatos:
        if c["nome"] == alvo["nome"] or c["familia"] != alvo["familia"]:
            continue
        if alvo["numero"] is None or c["numero"] is None:
            continue
        if abs(c["numero"] - alvo["numero"]) != 1:
            continue
        if not c.get("dispara") or not c.get("livre"):
            continue
        razoes = _geometria_casa(alvo, c)
        if not razoes:
            continue
        c = dict(c, geometria=razoes)
        vale.append(c)
    if not vale:
        return None, "sem_irmao", []
    if len(vale) > 1:
        return None, "ambiguo", vale
    return vale[0], "ligado", vale


class _Tiles:
    """Comportamento+colisao de cada celula, com cache. Usa a Grade da lente."""

    def __init__(self):
        qa = os.path.join(RAIZ, "dev_scripts/qa")
        if qa not in sys.path:
            sys.path.insert(0, qa)
        if os.path.join(RAIZ, "dev_scripts") not in sys.path:
            sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
        import valida_warp_tile as vwt
        import lente_portas as lp
        self.vwt = vwt
        self.grade = lp.Grade(RAIZ)
        self.de_familia = {vwt._MB[n] for n in ESCADA_MB + PORTA_MB if n in vwt._MB}
        self.cache = {}

    def celulas(self, nome, doc):
        if nome not in self.cache:
            self.cache[nome] = self.grade.de(doc) or {}
        return self.cache[nome]

    def em(self, nome, doc, x, y):
        """(nome do comportamento, colisao, dispara_como_escada_ou_porta)."""
        c = self.celulas(nome, doc).get((x, y))
        if c is None:
            return "fora do mapa", None, False
        comp, col = c
        morto, _ = self.vwt.warp_morto(comp, col)
        nome_mb = self.vwt.NOME.get(comp, "comportamento %s" % comp)
        return nome_mb, col, (comp in self.de_familia and not morto)


def _destino_na_fonte(nome, cen, src, por_fonte):
    """O que a FONTE escreveu para cada warp deste mapa, resolvido no nosso mundo."""
    v = next((x for x in cen["de_para"].values() if x["nome"] == nome), None)
    if v is None:
        return []
    m = src.get((v["fonte_grupo"], v["fonte_indice"]))
    if m is None:
        return []
    # TABELA DE WARP LIXO: `Galar_Postwick49` e `Galar_Postwick50` tem 224 e 225
    # warps na fonte, com coordenadas do tipo (-30648,-30624). O extrator leu
    # fora do fim do vetor. Despejar as 449 entradas aqui enche o documento de
    # ruido e esconde as 12 linhas que sao evidencia de verdade, entao a tabela
    # que estoura o mapa vira resumo.
    brutos = m.get("warps") or []
    n_no_mapa = len(le(nome).get("warp_events") or [])
    if len(brutos) > max(n_no_mapa, TETO_FONTE):
        return [{"tabela_da_fonte": "LIXO",
                 "warps_na_fonte": len(brutos),
                 "warps_no_nosso_map_json": n_no_mapa,
                 "por_que_nao_serve": (
                     "a tabela de warps deste mapa foi lida fora do fim do "
                     "vetor na extracao: as coordenadas saem da faixa do mapa "
                     "(ex.: %s) e os destinos apontam para grupo que nao "
                     "existe. Nao ha destino que se possa usar."
                     % ", ".join("(%d,%d)" % (w["x"], w["y"])
                                 for w in brutos[:3]))}]
    fora = []
    for i, w in enumerate(brutos):
        alvo = por_fonte.get((w["grupo"], w["mapa"]))
        d = {"warp": i, "x": w["x"], "y": w["y"],
             "fonte_destino": "g%dm%d" % (w["grupo"], w["mapa"]),
             "warp_de_chegada": w["warp_id"],
             "nosso_destino": alvo["nome"] if alvo else None}
        if alvo is None:
            outro = src.get((w["grupo"], w["mapa"]))
            d["por_que_nao_serve"] = (
                "o destino nao foi importado para Galar (secao da fonte: %r)"
                % (outro or {}).get("nome_secao"))
        else:
            n = len(le(alvo["nome"]).get("warp_events") or [])
            if not 0 <= w["warp_id"] < n:
                d["por_que_nao_serve"] = (
                    "o indice de chegada %d nao existe em %s, que tem %d warps"
                    % (w["warp_id"], alvo["nome"], n))
        fora.append(d)
    return fora


def _resume_mortos(meus):
    """A medicao de tile, um por warp; resumo quando sao dezenas (Postwick50)."""
    linhas = [{"warp": r["warp"], "x": r["x"], "y": r["y"],
               "comportamento": r["comportamento"], "colisao": r["colisao"],
               "e_escada_ou_porta_que_dispara": r["dispara"]} for r in meus]
    if len(linhas) <= TETO_FONTE:
        return linhas
    tipos = collections.Counter(
        r["comportamento"] + (" SOLIDO" if r["colisao"] else "") for r in meus)
    return {"warps_mortos": len(linhas),
            "nenhum_em_escada_ou_porta": not any(r["dispara"] for r in meus),
            "por_comportamento": dict(tipos.most_common()),
            "primeiros": linhas[:TETO_FONTE]}


def escadas(gravar):
    """O modo `--escadas`. Devolve (ligados, ambiguos, sem_irmao, recusados).

    Idempotente: um par ja escrito nao entra em `ligados` de novo.
    """
    tiles = _Tiles()
    cen = json.load(open(CENSO, encoding="utf-8"))
    por_fonte = {(v["fonte_grupo"], v["fonte_indice"]): v
                 for v in cen["de_para"].values()}
    FONTE = os.path.join(os.path.dirname(RAIZ),
                         "fontes-mapas/galar-swsh/extraidos-ultimate")
    src = {}
    arq = os.path.join(FONTE, "mapas.json")
    if os.path.exists(arq):
        for g in json.load(open(arq, encoding="utf-8")):
            for i, m in enumerate(g["mapas"]):
                src[(g["grupo"], i)] = m

    d = le_pendentes_documento()
    alvos = [m for m in (d.get("mapas") or []) if m.get("classe") == CLASSE_ESCADA]

    # Todo warp de todo mapa de Galar que esta LIVRE (aponta para o proprio
    # mapa, ou para um indice que nao existe) e cujo tile e de escada/porta.
    # E daqui que saem os candidatos a irmao.
    livres = []
    for v in cen["de_para"].values():
        p = os.path.join(MAPAS, v["nome"], "map.json")
        if not os.path.exists(p):
            continue
        doc = le(v["nome"])
        fam, num = _familia(v["nome"])
        for i, w in enumerate(doc.get("warp_events") or []):
            proprio = w.get("dest_map") == doc.get("id")
            if not proprio:
                continue
            mb, col, dispara = tiles.em(v["nome"], doc, w["x"], w["y"])
            livres.append({"nome": v["nome"], "id": doc.get("id"),
                           "familia": fam, "numero": num, "warp": i,
                           "x": w["x"], "y": w["y"],
                           "w": v.get("w") or 0, "h": v.get("h") or 0,
                           "comportamento": mb, "colisao": col,
                           "dispara": dispara, "livre": True})

    ligados, ambiguos, sem_irmao, recusados = [], [], [], []
    escritos = set()
    for m in alvos:
        nome = m["pasta"]
        if not os.path.exists(os.path.join(MAPAS, nome, "map.json")):
            continue
        doc = le(nome)
        fam, num = _familia(nome)
        meus = [r for r in livres if r["nome"] == nome]
        m["escadas_onda4"] = {
            "regra": "liga_orfaos_galar.py --escadas, onda 4 da Frente A",
            "warps_mortos_medidos": _resume_mortos(meus),
            "destino_na_fonte": _destino_na_fonte(nome, cen, src, por_fonte),
            "resultado": [],
        }
        for alvo in meus:
            escolhido, motivo, considerados = par_de_escada(alvo, livres)
            reg = {"warp": alvo["warp"], "motivo": motivo,
                   "evidencia": "%s (%2d,%2d) tile %s%s" % (
                       nome, alvo["x"], alvo["y"], alvo["comportamento"],
                       " SOLIDO" if alvo["colisao"] else "")}
            if motivo == "ambiguo":
                reg["candidatos"] = ["%s warp %d (%d,%d) %s [%s]" % (
                    c["nome"], c["warp"], c["x"], c["y"], c["comportamento"],
                    "; ".join(c["geometria"])) for c in considerados]
                ambiguos.append((nome, alvo["warp"], reg["candidatos"]))
            elif motivo == "sem_irmao":
                sem_irmao.append((nome, alvo["warp"]))
            elif motivo == "tile_nao_e_escada":
                recusados.append((nome, alvo["warp"], alvo["comportamento"],
                                  bool(alvo["colisao"])))
            else:
                outro = le(escolhido["nome"])
                doc["warp_events"][alvo["warp"]]["dest_map"] = escolhido["id"]
                doc["warp_events"][alvo["warp"]]["dest_warp_id"] = str(escolhido["warp"])
                outro["warp_events"][escolhido["warp"]]["dest_map"] = doc["id"]
                outro["warp_events"][escolhido["warp"]]["dest_warp_id"] = str(alvo["warp"])
                if gravar:
                    grava(nome, doc)
                    grava(escolhido["nome"], outro)
                escritos.add(nome)
                escritos.add(escolhido["nome"])
                reg["par"] = "%s warp %d <-> %s warp %d" % (
                    nome, alvo["warp"], escolhido["nome"], escolhido["warp"])
                reg["geometria"] = escolhido["geometria"]
                ligados.append((nome, alvo["warp"], escolhido["nome"],
                                escolhido["warp"], escolhido["geometria"]))
                m["classe"] = CLASSE_LIGADO
                m["ligado_na_onda_4"] = reg["par"]
            m["escadas_onda4"]["resultado"].append(reg)
        # Mesma razao do resumo la de cima: 63 linhas iguais nao sao evidencia,
        # sao ruido. O que decide (o motivo) fica; a repeticao vira contagem.
        res = m["escadas_onda4"]["resultado"]
        if len(res) > TETO_FONTE:
            m["escadas_onda4"]["resultado"] = {
                "warps": len(res),
                "por_motivo": dict(collections.Counter(
                    r["motivo"] for r in res).most_common()),
                "primeiros": res[:TETO_FONTE]}
            motivos = {r["motivo"] for r in res}
        else:
            motivos = {r["motivo"] for r in res}
        if not ligados or m.get("classe") != CLASSE_LIGADO:
            m["escadas_onda4"]["conclusao"] = (
                "nao ligado nesta onda: " + ", ".join(sorted(motivos)))
    if gravar:
        _grava_pendentes(d)
    return ligados, ambiguos, sem_irmao, recusados


def le_pendentes_documento():
    """O JSON dos pendentes inteiro, para o modo --escadas mexer nele."""
    with open(PENDENTE_FONTE, encoding="utf-8") as f:
        return json.load(f)


def _grava_pendentes(d):
    """Regrava o JSON dos pendentes com o resumo por classe refeito."""
    resumo = collections.Counter(m.get("classe") for m in (d.get("mapas") or []))
    # Ordenado, igual ao que `pendentes_de_fonte` escreve. Sem o `sorted`, os
    # dois modos escreviam o mesmo conteudo com as chaves em ordem diferente e
    # o arquivo oscilava entre duas versoes a cada rodada, o que faz o `git
    # diff` mentir que algo mudou.
    d["resumo_por_classe"] = dict(sorted(resumo.items()))
    d["classes"][CLASSE_LIGADO] = (
        "estava marcado como escada faltando e a onda 4 ligou o par, com ida e "
        "volta e o tile conferido pelo comportamento do metatile.")
    d["onda_4"] = {
        "data": "2026-09-06",
        "modo": "dev_scripts/liga_orfaos_galar.py --escadas",
        "o_que_foi_medido": (
            "os 17 warps mortos das 14 marcadas como escada faltando foram "
            "medidos tile a tile: NENHUM esta sobre escada, escada rolante ou "
            "porta. 13 caem em MB_NORMAL (3 deles solidos), 4 em MB_CAVE ou "
            "piso de laje. Em 11 das 14 o mapa inteiro nao tem um unico tile "
            "que dispare warp. A fonte, ao contrario do que a classe dizia, "
            "ESCREVEU destino para 12 dos 17: 7 mapas apontam para sobra de "
            "FireRed que nao importamos (Celadon Dept., Outcast Island, Dotted "
            "Hole), 4 apontam para Galar_WildArea03 warp 13, que nao existe "
            "(ele tem 7 warps), e 2 tem tabela de warp lixo na fonte. Nenhuma "
            "foi ligada: ligar exige DESENHAR tile de escada ou porta no "
            "blockdata, que e a decisao de desenho que a resposta 40 do Gui "
            "adiou."),
        "leitura_de_tile_conferida": (
            "993 dos 1.468 warps de Galar (67,6%) caem em tile que dispara, "
            "com 44 MB_LADDER e 28 escadas diagonais: a leitura nao esta "
            "quebrada, o resultado e real."),
    }
    with open(PENDENTE_FONTE, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def demo_escadas():
    """Autoteste da REGRA, com caso sintetico. Devolve lista de falhas."""
    falhas = []

    def base(nome, warp, x, y, dispara=True, livre=True, w=20, h=20):
        fam, num = _familia(nome)
        return {"nome": nome, "id": "MAP_" + nome.upper(), "familia": fam,
                "numero": num, "warp": warp, "x": x, "y": y, "w": w, "h": h,
                "comportamento": "MB_LADDER" if dispara else "MB_NORMAL",
                "colisao": 0, "dispara": dispara, "livre": livre}

    # 1. andar 1 e andar 2 da mesma familia, escada na mesma coluna: liga.
    a1 = base("Demo_Torre01", 0, 5, 9)
    a2 = base("Demo_Torre02", 0, 5, 3)
    esc, mot, _ = par_de_escada(a1, [a1, a2])
    if mot != "ligado" or esc["nome"] != "Demo_Torre02":
        falhas.append("caso 1 (par obvio) deu %r" % mot)
    # 1b. e a geometria espelhada tambem casa.
    a2e = base("Demo_Torre02", 0, 14, 3)   # 20-1-5 = 14
    esc, mot, _ = par_de_escada(a1, [a1, a2e])
    if mot != "ligado":
        falhas.append("caso 1b (coluna espelhada) deu %r" % mot)
    # 2. dois candidatos adjacentes que passam: ambiguo, e NAO liga.
    a0 = base("Demo_Torre00", 0, 5, 15)
    esc, mot, cand = par_de_escada(a1, [a0, a1, a2])
    if mot != "ambiguo" or esc is not None or len(cand) != 2:
        falhas.append("caso 2 (ambiguo) deu %r com %d candidatos"
                      % (mot, len(cand)))
    # 3. tile que nao e escada: recusa antes de olhar irmao.
    ruim = base("Demo_Torre01", 0, 5, 9, dispara=False)
    esc, mot, _ = par_de_escada(ruim, [ruim, a2])
    if mot != "tile_nao_e_escada":
        falhas.append("caso 3 (tile de piso) deu %r" % mot)
    # 4. irmao com numero distante nao vale.
    longe = base("Demo_Torre05", 0, 5, 3)
    esc, mot, _ = par_de_escada(a1, [a1, longe])
    if mot != "sem_irmao":
        falhas.append("caso 4 (numero distante) deu %r" % mot)
    # 5. outra familia nao vale, nem com a geometria certa.
    outra = base("Demo_Farol02", 0, 5, 3)
    esc, mot, _ = par_de_escada(a1, [a1, outra])
    if mot != "sem_irmao":
        falhas.append("caso 5 (outra familia) deu %r" % mot)
    # 6. irmao com escada JA pareada (nao livre) nao vale.
    preso = base("Demo_Torre02", 0, 5, 3, livre=False)
    esc, mot, _ = par_de_escada(a1, [a1, preso])
    if mot != "sem_irmao":
        falhas.append("caso 6 (irmao ja pareado) deu %r" % mot)
    # 7. geometria que nao casa em nada nao vale.
    torto = base("Demo_Torre02", 0, 2, 7)
    esc, mot, _ = par_de_escada(a1, [a1, torto])
    if mot != "sem_irmao":
        falhas.append("caso 7 (geometria torta) deu %r" % mot)
    for o_que, ok in (("regra de escada, 7 casos sinteticos", not falhas),):
        print("  %-56s %s" % (o_que, "OK" if ok else "CAIU"))
    for f in falhas:
        print("     ! %s" % f)
    return falhas



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
    falhou.extend(demo_escadas())
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


def modo_escadas(gravar):
    """Imprime o que o modo --escadas achou. Sem --aplicar, nao escreve nada."""
    ligados, ambiguos, sem_irmao, recusados = escadas(gravar)
    print("--escadas%s: %d pares ligados, %d ambiguos, %d sem irmao, "
          "%d recusados pelo tile"
          % (" --aplicar" if gravar else " (seco, nao escreveu nada)",
             len(ligados), len(ambiguos), len(sem_irmao), len(recusados)))
    for a, wa, b, wb, geo in ligados:
        print("   + %s warp %d <-> %s warp %d  [%s]" % (a, wa, b, wb, "; ".join(geo)))
    for nome, w, cands in ambiguos:
        print("   ? %s warp %d: %d candidatos, nao se liga" % (nome, w, len(cands)))
        for c in cands:
            print("       %s" % c)
    for nome, w in sem_irmao:
        print("   - %s warp %d: nenhum irmao de numero adjacente com escada livre"
              % (nome, w))
    # Recusa se agrupa por mapa: Galar_Postwick50 sozinho tem 63 warps mortos,
    # e imprimir um por linha enterra os outros treze mapas.
    por_mapa = collections.OrderedDict()
    for nome, w, mb, solido in recusados:
        por_mapa.setdefault(nome, []).append((w, mb + (" SOLIDO" if solido else "")))
    for nome, itens in por_mapa.items():
        tipos = collections.Counter(mb for _, mb in itens)
        print("   ! %-22s %2d warp(s) morto(s), nenhum em escada ou porta: %s"
              % (nome, len(itens),
                 ", ".join("%dx %s" % (q, mb) for mb, q in tipos.most_common())))
    if recusados:
        print("   (%d mapas, %d warps: a premissa de escada nao se sustenta; "
              "ver o cabecalho do modo)" % (len(por_mapa), len(recusados)))
    if gravar:
        print("   marcacao regravada em %s" % os.path.relpath(PENDENTE_FONTE, RAIZ))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seco", action="store_true", help="nao escreve nada")
    ap.add_argument("--censo", action="store_true", help="so a medicao do diagnostico")
    ap.add_argument("--demo", action="store_true", help="autoteste")
    ap.add_argument("--pendentes", action="store_true",
                    help="so a marcacao dos mapas sem entrada na fonte")
    ap.add_argument("--autoteste", action="store_true", help="autoteste")
    ap.add_argument("--escadas", action="store_true",
                    help="o modo escada da onda 4: procura o par dos warps mortos")
    ap.add_argument("--aplicar", action="store_true",
                    help="com --escadas, grava os pares (sem ele, so relata)")
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

    if args.escadas:
        return modo_escadas(args.aplicar and not args.seco)

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
