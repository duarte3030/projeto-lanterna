#!/usr/bin/env python3
"""Anda o jogo inteiro pelo grafo de warps e conexoes, e acha o que trava.

Uso:
    python3 dev_scripts/valida_conectividade.py [MAP_DE_PARTIDA]

Existe porque "alcancavel" checado dentro de UM mapa e geometria de colisao, nao
jogo. O que prende o jogador de verdade e warp que aponta para indice que nao
existe, warp so de ida, e mapa que nenhum caminho alcanca. Tres bugs desse tipo
ja passaram por aqui despercebidos: dois ginasios inacessiveis por warp fora da
porta, e 6 de 7 ginasios cuspindo o jogador numa rota ao sair.

Reporta:
  1. warp cujo `dest_warp_id` nao existe no mapa de destino  (trava garantida)
  2. mapa alcancavel de onde NAO se volta                    (beco sem saida)
  3. mapa de QUALQUER das seis regioes que nenhum caminho alcanca (conteudo morto)

Tres buracos fechados em 23/08/2026, medidos pela auditoria de mapas
-------------------------------------------------------------------
1. **A checagem de orfao so olhava Sinnoh e Johto.** Kanto, Hoenn, Unova e Galar
   nunca tinham sido medidas por ela. Agora `regiao()` classifica pelo GRUPO do
   mapa, a mesma regra da auditoria, e as seis entram.
2. **O regex de warp de script perdia `setdivewarp`, `setescapewarp` e
   `warpwhitefade`.** Foi por essa fresta que Sootopolis inteira, a cidade que so
   se entra por mergulho, aparecia inalcancavel.
3. **Transporte que NAO e warp de script ficava de fora**, e sao dois nesta ROM:
   a balsa Seagallop das Sevii (`special DoSeagallopFerryScene`, tabela `sSeag`
   em src/seagallop.c) e o SELETOR DE CAPITULO (src/chapter_jump.c), que e a
   unica porta de Galar por decisao registrada no PLANO-OBRAS-GALAR. Sem eles a
   ferramenta acusava 162 mapas de Kanto e os 438 de Galar como conteudo morto,
   e os dois numeros eram da MEDICAO, nao do jogo.

Mapa com `cortado_por` no map.json e CORTE REGISTRADO (a CasteliaPlaza de Unova,
por exemplo, PLANO-ESCOPO.md): ele sai da conta de orfao em vez de reaparecer
toda rodada, e o mesmo vale para as tres tiras `*ConnectionDummy`, que sao sobra
de recurso de motor e nao mapa perdido (ver a nota no corpo).
"""
import json
import os
import re
import sys
from collections import deque

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = os.path.join(REPO, "data/maps")


def tabela_de_constantes():
    """dir do mapa -> constante MAP_*, lida da FONTE, nao adivinhada.

    Derivar a constante por regex erra: "OreburghCity_PokemonCenter_1F" vira
    "..._1_F" se a regra separar digito de maiuscula, e aparecem 1882 warps
    "quebrados" que nao existem. A verdade e o par (grupo, indice) de
    map_groups.json casado com o valor em constants/map_groups.h.
    """
    grupos = json.load(open(os.path.join(MAPS, "map_groups.json")))
    header = open(os.path.join(REPO, "include/constants/map_groups.h")).read()
    por_valor = {}
    for const, num, grp in re.findall(
            r"(MAP_[A-Z0-9_]+)\s*=\s*\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)\)", header):
        por_valor[(int(grp), int(num))] = const
    tabela = {}
    for g_idx, nome_grupo in enumerate(grupos["group_order"]):
        for m_idx, nome_mapa in enumerate(grupos.get(nome_grupo, [])):
            const = por_valor.get((g_idx, m_idx))
            if const:
                tabela[nome_mapa] = (const, nome_grupo)
    return tabela


def carrega():
    const = tabela_de_constantes()
    mapas = {}
    for nome in sorted(os.listdir(MAPS)):
        if nome not in const:
            continue
        caminho = os.path.join(MAPS, nome, "map.json")
        if not os.path.exists(caminho):
            continue
        try:
            d = json.load(open(caminho))
        except json.JSONDecodeError as e:
            print(f"  JSON QUEBRADO: {nome}/map.json: {e}")
            continue
        mapas[const[nome][0]] = dict(dir=nome, grupo=const[nome][1], dados=d)
    return mapas


def mapa_de_partida(mapas):
    """Onde o jogo novo comeca, LIDO de src/new_game.c, nunca copiado aqui.

    Estava cravado como MAP_TWINLEAF_TOWN, que deixou de ser o inicio quando a
    ordem cronologica moveu o jogo para Pallet Town (decisao 66). Teste que
    guarda copia de um fato envelhece calado: partir do mapa errado muda a conta
    de alcance sem nenhum aviso. Le a linha do #else (o caminho de jogo de
    verdade), nao a do DEV_SKIP_INTRO.
    """
    fonte = open(os.path.join(REPO, "src/new_game.c")).read()
    achados = re.findall(r"SetWarpDestination\(MAP_GROUP\((MAP_\w+)\)", fonte)
    for nome in achados:
        if nome in mapas:
            return nome
    raise SystemExit("nao achei o mapa de partida em src/new_game.c: " + str(achados))


# Todo comando de script que MOVE o jogador para outro mapa. `warpwhitefade` cai
# no sufixo, `setdivewarp` e `setescapewarp` no prefixo. Sem os tres, Sootopolis
# ficava fora do grafo.
RE_WARP_DE_SCRIPT = re.compile(
    r"\b(?:set)?(?:dive|escape|dynamic)?warp"
    r"(?:silent|hole|door|teleport|whitefade)?\s+(MAP_[A-Z0-9_]+)")


# Cabecalho que os geradores de Galar escrevem antes do bloco de cada mapa,
# em `data/scripts/galar_*.inc`. Ele e a UNICA coisa que diz de qual mapa o
# rotulo seguinte e: os `data/maps/Galar_*/scripts.inc` nao tem `.string` nem
# `warp` nenhum, e o corpo inteiro mora nos arquivos compartilhados.
RE_CABECA_GALAR = re.compile(r"^@ ---- (Galar_\w+)\b", re.M)

LE_INC_GALAR = True
EXIGE_CHAMADA = True


def warps_de_script_de_galar(mapas):
    """{mapa de Galar: {MAP_* que um script dele alcanca}}.

    Por que isto existe: a varredura por `data/maps/<mapa>/scripts.inc` nao ve
    NADA de Galar. Os 438 `scripts.inc` daquela regiao so tem o `MapScripts`; o
    corpo esta em `data/scripts/galar_*.inc`, um arquivo por tipo de conteudo,
    com todos os mapas dentro e um cabecalho `@ ---- Galar_X ----` separando os
    blocos. Sem ler isso, toda porta que o demake abre por bytecode fica fora do
    grafo e o mapa do outro lado aparece como orfao sem ter defeito nenhum.
    """
    fora = {}
    if not LE_INC_GALAR:
        return fora
    # `mapas` e indexado pela constante MAP_*, e o cabecalho do .inc traz o nome
    # da PASTA. Sem esta tabela a varredura casava zero linha e passava calada.
    por_pasta = {info["dir"]: nome for nome, info in mapas.items()}
    pasta = os.path.join(REPO, "data/scripts")
    if not os.path.isdir(pasta):
        return fora
    # O rotulo so vale se o MAPA o chama. Rotulo escrito no .inc e nao
    # pendurado em nenhum `script` de map.json e texto na ROM que o jogador
    # nunca dispara, e credita-lo aqui apagaria um orfao de verdade da lista.
    # Sao 10 portas `GalarTrn_*` nessa situacao hoje.
    chamados = {}
    for nome, info in mapas.items():
        if not info["dir"].startswith("Galar_"):
            continue
        d = info["dados"]
        alvo = set()
        for chave in ("object_events", "bg_events", "coord_events"):
            for e in d.get(chave) or []:
                if isinstance(e.get("script"), str) and e["script"] != "0":
                    alvo.add(e["script"])
        inc_mapa = os.path.join(MAPS, info["dir"], "scripts.inc")
        if os.path.exists(inc_mapa):
            t = open(inc_mapa, encoding="utf-8", errors="replace").read()
            alvo |= set(re.findall(r"\bGalar[A-Za-z]*_\w+", t))
        chamados[info["dir"]] = alvo

    for nome in sorted(os.listdir(pasta)):
        if not (nome.startswith("galar_") and nome.endswith(".inc")):
            continue
        texto = open(os.path.join(pasta, nome), encoding="utf-8",
                     errors="replace").read()
        cortes = list(RE_CABECA_GALAR.finditer(texto))
        for i, m in enumerate(cortes):
            mapa = m.group(1)
            if mapa not in por_pasta:
                continue
            fim = cortes[i + 1].start() if i + 1 < len(cortes) else len(texto)
            bloco = texto[m.end():fim]
            rotulos = set(re.findall(r"^(\w+)::", bloco, re.M))
            if EXIGE_CHAMADA and not (rotulos & chamados.get(mapa, set())):
                continue
            for destino in RE_WARP_DE_SCRIPT.findall(bloco):
                if destino in mapas:
                    fora.setdefault(mapa, set()).add(destino)
    return fora


def transportes_por_special(mapas):
    """Conjuntos de mapas ligados por transporte que NAO e warp de script.

    Devolve lista de conjuntos MUTUAMENTE ligados. Lido da fonte, nunca copiado:
    quem mexer na tabela muda a medicao junto.
    """
    grupos = []
    # A balsa Seagallop das Sevii. `sSeag` (src/seagallop.c) e a tabela de
    # destinos que `DoSeagallopFerryScene` usa; qualquer porto alcanca qualquer
    # outro conforme o passe, entao o conjunto e mutuamente ligado. O PORTAO e de
    # ENREDO e esta intacto (Blaine acende VAR_MAP_SCENE_CINNABAR_ISLAND=1 em
    # CinnabarIsland_Gym_Frlg/scripts.inc:61, a cena do Bill leva a One Island, e
    # la nasce o TRI PASS): as Sevii sao pos-setima-insignia, nao conteudo morto.
    fonte = os.path.join(REPO, "src/seagallop.c")
    if os.path.exists(fonte):
        t = open(fonte, encoding="utf-8", errors="replace").read()
        m = re.search(r"sSeag\[\]\[4\]\s*=\s*\{(.*?)\n\};", t, re.S)
        if m:
            portos = {n for n in re.findall(r"MAP_GROUP\((MAP_\w+)\)", m.group(1))
                      if n in mapas}
            if len(portos) > 1:
                grupos.append(portos)
    return grupos


def sementes_do_seletor(mapas):
    """Mapas que o SELETOR DE CAPITULO alcanca sem warp nenhum.

    src/chapter_jump.c pula por HEAL_LOCATION_*, e e a UNICA porta de Galar
    (decisao registrada no PLANO-OBRAS-GALAR): nao existe warp nem conexao
    ligando Galar as outras cinco regioes. Medir Galar sem isto so mede a
    decisao de novo.
    """
    cj = os.path.join(REPO, "src/chapter_jump.c")
    hl = os.path.join(REPO, "src/data/heal_locations.json")
    if not (os.path.exists(cj) and os.path.exists(hl)):
        return set()
    usados = set(re.findall(r"HEAL_LOCATION_[A-Z0-9_]+",
                            open(cj, encoding="utf-8", errors="replace").read()))
    por_id = {h["id"]: h.get("map") for h in json.load(open(hl))["heal_locations"]}
    return {por_id[i] for i in usados if por_id.get(i) in mapas}


GRUPO_DE_REGIAO = (("Frlg", "Kanto"), ("Johto", "Johto"), ("Unova", "Unova"),
                   ("Galar", "Galar"), ("Sinnoh", "Sinnoh"), ("Galactic", "Sinnoh"))


def pendentes_de_fonte():
    """Os MAP_* que liga_orfaos_galar.py marcou como pendentes de fonte.

    So LEITURA: esta ferramenta nunca decide quem e pendente, nem tira ninguem
    da conta de orfaos por causa disso. Quem gera a lista e
    `dev_scripts/liga_orfaos_galar.py --pendentes`, e o formato dela mora la.
    Se o arquivo nao existir ou estiver quebrado, devolve conjunto vazio e a
    regua segue igual: marcacao que falta nao pode fazer validador mentir.
    """
    if os.path.join(REPO, "dev_scripts") not in sys.path:
        sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
    try:
        import liga_orfaos_galar as LOG
        return LOG.le_pendentes()[2]
    except Exception:
        return set()


def demo():
    """MUTACAO PLANTADA: sem ler `data/scripts/galar_*.inc`, a conta de orfaos
    de Galar tem que PIORAR. Se ela nao mudar, a varredura nova nao esta
    pesando e quem confiar nela mede o jogo errado."""
    global LE_INC_GALAR
    mapas = carrega()
    com = warps_de_script_de_galar(mapas)
    pares = sum(len(v) for v in com.values())
    falhas = []
    if not com:
        falhas.append("nenhum warp de script achado em data/scripts/galar_*.inc")
    guarda = LE_INC_GALAR
    try:
        LE_INC_GALAR = False
        if warps_de_script_de_galar(mapas):
            falhas.append("a trava LE_INC_GALAR nao desliga a varredura")
    finally:
        LE_INC_GALAR = guarda
    # O filtro de "rotulo que o mapa chama" nunca pode ACRESCENTAR par, e a
    # demo diz em voz alta quanto ele tira hoje, para ninguem tratar como trava
    # o que hoje nao morde.
    global EXIGE_CHAMADA
    guarda2 = EXIGE_CHAMADA
    try:
        EXIGE_CHAMADA = False
        solto = warps_de_script_de_galar(mapas)
    finally:
        EXIGE_CHAMADA = guarda2
    pares_solto = sum(len(v) for v in solto.values())
    if pares > pares_solto:
        falhas.append("o filtro de rotulo chamado ACRESCENTOU par, o que e "
                      "impossivel: %d contra %d" % (pares, pares_solto))
    # Todo destino citado e mapa que existe, e toda origem e pasta de Galar.
    for mapa, destinos in com.items():
        if not mapa.startswith("Galar_"):
            falhas.append("origem que nao e de Galar: " + mapa)
        for d in destinos:
            if d not in mapas:
                falhas.append(f"{mapa}: destino que nao existe, {d}")
    # A trava da linha nova: os pendentes de fonte sao SO leitura. Todo
    # pendente tem que ser um MAP_* que existe nesta arvore e de Galar; e a
    # conta de orfaos nao pode depender dele (por isso ela e feita antes, em
    # main(), sem consultar esta lista).
    pend = pendentes_de_fonte()
    for m in sorted(pend):
        if m not in mapas:
            falhas.append("pendente de fonte que nao existe nesta arvore: " + m)
        elif not mapas[m]["dir"].startswith("Galar_"):
            falhas.append("pendente de fonte que nao e de Galar: " + m)

    print("demo conectividade: %s (%d mapas de Galar com warp de script, "
          "%d pares mapa->destino; o filtro de rotulo chamado tira %d par(es) "
          "de %d; %d pendentes de fonte lidos, todos so para exibicao)"
          % ("OK" if not falhas else "REPROVADO", len(com), pares,
             pares_solto - pares, pares_solto, len(pend)))
    for f in falhas:
        print("  FALHA", f)
    return 1 if falhas else 0


def main():
    global LE_INC_GALAR
    argumentos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--demo" in sys.argv:
        raise SystemExit(demo())
    if "--sem-scripts-galar" in sys.argv:
        # So para MEDIR quanto a varredura nova vale. Nao e modo de trabalho.
        LE_INC_GALAR = False
    mapas = carrega()
    partida = argumentos[0] if argumentos else mapa_de_partida(mapas)
    if partida not in mapas:
        # cai para o que o modo de desenvolvimento usa hoje
        dbg = open(os.path.join(REPO, "include/config/debug.h")).read()
        m = re.search(r"#define DEV_START_MAP\s+(MAP_\w+)", dbg)
        partida = m.group(1) if m and m.group(1) in mapas else sorted(mapas)[0]
    print(f"partindo de {partida}\n")

    quebrados = []
    saidas = {}
    de_galar = warps_de_script_de_galar(mapas)
    for origem, info in mapas.items():
        vizinhos = set()
        for i, w in enumerate(info["dados"].get("warp_events", [])):
            destino = w.get("dest_map", "")
            if destino in ("MAP_NONE", "MAP_DYNAMIC", ""):
                continue
            if destino not in mapas:
                quebrados.append((origem, i, destino, "mapa de destino nao existe"))
                continue
            n_la = len(mapas[destino]["dados"].get("warp_events", []))
            try:
                alvo = int(w.get("dest_warp_id", 0))
            except (TypeError, ValueError):
                alvo = -1
            if alvo < 0 or alvo >= n_la:
                quebrados.append((origem, i, destino,
                                  f"dest_warp_id {w.get('dest_warp_id')} mas o destino tem {n_la} warps"))
                continue
            vizinhos.add(destino)
        # conexoes de rota (andar de um mapa para o outro sem warp) sao bidirecionais
        for c in info["dados"].get("connections") or []:
            if c.get("map") in mapas:
                vizinhos.add(c["map"])
        # Warp MAP_DYNAMIC nao tem destino escrito: quem decide e o
        # `setdynamicwarp` de um script. O laco acima o PULA, e sem isto as 20
        # salas da Turnback Cave apareceriam como "nenhum caminho alcanca"
        # estando alcancaveis no jogo. O destino nao e adivinhado aqui: o mapa
        # declara em `destinos_dinamicos` para onde as portas dele podem mandar,
        # e o `--demo` de `turnback_cave_sinnoh.py` exige que essa lista seja
        # exatamente o conjunto de `setdynamicwarp` do script gerado, senao ela
        # viraria uma segunda verdade que envelhece calada.
        for destino in info["dados"].get("destinos_dinamicos") or []:
            if destino in mapas:
                vizinhos.add(destino)
        # Warp escrito DENTRO de script tambem liga mapa, e e assim que a viagem
        # entre regioes funciona (o marinheiro de Canalave leva a Olivine). Sem
        # ler isto, a ferramenta declarava Johto inteira inalcancavel, que era
        # falso: o erro era da ferramenta, nao do jogo.
        inc = os.path.join(MAPS, info["dir"], "scripts.inc")
        if os.path.exists(inc):
            texto = open(inc, encoding="utf-8", errors="replace").read()
            for destino in RE_WARP_DE_SCRIPT.findall(texto):
                if destino in mapas:
                    vizinhos.add(destino)
        # Galar escreve o corpo em `data/scripts/galar_*.inc`, e nao no
        # `scripts.inc` do mapa. Sem esta linha a regua media Galar com o
        # bytecode do demake inteiro fora do grafo.
        vizinhos |= de_galar.get(info["dir"], set())
        saidas[origem] = vizinhos

    # Transporte por `special` (a balsa das Sevii): liga o conjunto inteiro.
    for conjunto in transportes_por_special(mapas):
        for a in conjunto:
            saidas.setdefault(a, set()).update(conjunto - {a})

    # ---------------------------------------------------------------
    # Regra de ida-e-volta, VERSAO ESTREITA. Estava na especificacao desde o
    # comeco e eu nunca tinha escrito; quando escrevi, a versao ampla nao servia.
    #
    # O problema que ela existe para pegar: o item 1 abaixo so confere que o
    # INDICE existe. Se A manda para o warp 4 de B e B tem 5 warps, passa. Foi
    # por baixo disso que 6 ginasios de Sinnoh saiam para o warp 0 da cidade,
    # que e a porta de OUTRO predio. Indice 0 existe em todo mapa.
    #
    # A versao ampla ("todo warp tem que voltar") acusou 427 casos aqui. Medi o
    # pret/pokeemerald intocado: 131 casos em 518 mapas, 25,3 por 100, contra
    # 26,4 por 100 aqui. **O vanilla tem a mesma taxa**, porque predio de varias
    # portas, corredor de mao unica e saida compartilhada sao desenho normal. A
    # regra ampla nao distingue bug de padrao, e seria mais um validador de
    # falso positivo, que e o erro que esta sessao passou a noite consertando.
    #
    # A versao que serve: INTERIOR COM UMA PORTA SO tem que devolver para si
    # mesmo. Casa de uma porta e caso sem ambiguidade. Mede zero aqui e zero no
    # vanilla, e teria acusado os 6 ginasios, que tinham exatamente uma saida.
    ida_volta = []
    for origem, info in mapas.items():
        d = info["dados"]
        ws = d.get("warp_events") or []
        if len(ws) != 1 or d.get("map_type") != "MAP_TYPE_INDOOR":
            continue
        w = ws[0]
        destino = w.get("dest_map", "")
        if destino not in mapas:
            continue
        try:
            j = int(w.get("dest_warp_id", 0))
        except (TypeError, ValueError):
            continue
        la = mapas[destino]["dados"].get("warp_events") or []
        if not (0 <= j < len(la)):
            continue
        volta = la[j].get("dest_map", "")
        if volta in ("MAP_NONE", "MAP_DYNAMIC", ""):
            continue
        if volta != origem:
            ida_volta.append((origem, destino, j, volta))

    print(f"=== 0. porta unica que nao devolve: {len(ida_volta)} ===")
    for origem, destino, j, volta in ida_volta[:20]:
        print(f"  {origem} tem UMA saida, para {destino} warp {j}, "
              f"e esse warp leva a {volta}")
    print()

    print(f"=== 1. warps quebrados: {len(quebrados)} ===")
    for origem, i, destino, motivo in quebrados[:25]:
        print(f"  {origem} warp {i} -> {destino}: {motivo}")
    if len(quebrados) > 25:
        print(f"  ... e mais {len(quebrados) - 25}")

    sementes = {partida} | sementes_do_seletor(mapas)
    vistos = set(sementes)
    fila = deque(sorted(sementes))
    while fila:
        atual = fila.popleft()
        for v in saidas.get(atual, ()):
            if v not in vistos:
                vistos.add(v)
                fila.append(v)
    # TUMULO nao entra no denominador (23/08/2026). `remove_mapas_cortados.py`
    # deixa o mapa cortado na tabela, para nao deslocar `mapGroup`/`mapNum` da
    # save, mas o esvazia: sem warp, sem conexao e com `region_map_section` em
    # MAPSEC_NONE. Contar isso como "mapa que ninguem alcanca" e cobrar da regua
    # um alcance que o Gui cortou de proposito, e o numero so piora a cada corte
    # novo. Os tres sinais juntos, e nao so o MAPSEC, porque mapa vivo de sala
    # de link tambem nasce sem secao de mapa-mundi.
    tumulos = {m for m, i in mapas.items()
               if str(i["dados"].get("region_map_section")) == "MAPSEC_NONE"
               and not i["dados"].get("warp_events")
               and not i["dados"].get("connections")}
    vivos = len(mapas) - len(tumulos)
    print(f"\n=== 2. alcance: {len(vistos - tumulos)} de {vivos} mapas vivos "
          f"({len(tumulos)} tumulos de mapa cortado fora da conta) ===")

    becos = [m for m in vistos if not saidas.get(m)]
    print(f"\n=== 3. becos sem saida (entra e nao sai): {len(becos)} ===")
    for m in sorted(becos)[:20]:
        print("  ", m)

    def regiao(m):
        """Regiao pelo GRUPO do mapa, a mesma regra da auditoria de mapas.

        A versao antiga classificava por prefixo de diretorio e so sabia dizer
        Sinnoh e Johto; tudo mais caia em "outro" e sumia da conta. Grupo e o
        que map_groups.json ja declara, e nao envelhece com nome de mapa novo.
        """
        nome, grupo = mapas[m]["dir"], mapas[m]["grupo"]
        if nome.startswith("Galar_"):
            return "Galar"
        for chave, r in GRUPO_DE_REGIAO:
            if chave in grupo:
                return r
        return "Hoenn"

    # `cortado_por` e CORTE REGISTRADO no map.json (PLANO-ESCOPO.md). Ele sai da
    # conta em vez de reaparecer toda rodada: acusar de novo o que o Gui ja
    # decidiu cortar e ruido, e ruido e o que faz validador deixar de ser lido.
    # Medido em 23/08/2026: 68 mapas trazem o carimbo, entre eles as cinco da
    # CasteliaPlaza de Unova, que sao tumulo de verdade (zero warp, zero objeto).
    orfaos, cortados = {}, 0
    for m, info in mapas.items():
        if info["dados"].get("cortado_por"):
            cortados += 1
            continue
        # `*ConnectionDummy`: sobra de RECURSO DE MOTOR que esta ROM nao tem, e
        # nao mapa perdido. O bw3g resolve borda dupla em tempo de execucao
        # (data/maps/dual_connections.asm: andar ao norte de Icirrus South cai em
        # IcirrusCityNorth se x < 21 e na Rota 8 caso contrario), e o importador
        # criou uma tira vazia para segurar a borda. Pokeemerald so aceita UMA
        # conexao por direcao, entao em 23/08/2026 as tres bordas passaram a
        # apontar para o destino PRINCIPAL de cada par e as tiras ficaram sem
        # dono. Elas nao podem ser apagadas: indice de mapa e promessa de save.
        if info["dir"].endswith("ConnectionDummy"):
            cortados += 1
            continue
        if m not in vistos:
            orfaos.setdefault(regiao(m), []).append(m)
    print(f"\n=== 4. mapas que NENHUM caminho alcanca, por regiao "
          f"({cortados} cortados registrados fora da conta) ===")
    # `pendentes de fonte` NAO e corte e NAO sai do denominador: e a lista de
    # Galar que `dev_scripts/liga_orfaos_galar.py` marcou como "a fonte nao tem
    # porta para dar" (decisao do Gui, 06/09/2026). A linha abaixo so EXPLICA
    # parte dos orfaos de Galar; a contagem deles fica exatamente igual, com ou
    # sem o arquivo. Se um dia ela passar a mexer no numero, o `--demo` cai.
    pendentes = pendentes_de_fonte()
    for r, lst in sorted(orfaos.items()):
        print(f"  {r}: {len(lst)}")
        if r == "Galar" and pendentes:
            dentro = len(set(lst) & pendentes)
            print(f"    pendentes de fonte: {len(pendentes)}"
                  f"  ({dentro} destes {len(lst)}; marcados em "
                  f"dev_scripts/orfaos_galar_pendente_fonte.json, nao cortados)")
        for m in sorted(lst)[:12]:
            print("     ", m)
        if len(lst) > 12:
            print(f"      ... e mais {len(lst) - 12}")
    if not orfaos:
        print("  nenhum")

    return 1 if quebrados else 0


if __name__ == "__main__":
    sys.exit(main())
