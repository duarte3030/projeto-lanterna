#!/usr/bin/env python3
"""Quanto de cada regiao ja esta pronto, medido CONTRA A FONTE dela, MAPA A MAPA.

Uso:
    python3 dev_scripts/completude.py
    python3 dev_scripts/completude.py --detalhe Johto

Existe porque numero cru nao significa nada. "82% dos warps disparam" nao diz se
isso e bom: o proprio jogo original nunca chega a 100%, porque muita porta e
trocada por script em tempo de execucao e muito warp so e usado por barco ou
cutscene, sem ninguem pisar nele.

A regua certa e a FONTE. 100% quer dizer "tao completo quanto o jogo de onde a
regiao veio", nao "perfeito".

    Hoenn  -> pret/pokeemerald   (nossa Hoenn e o vanilla; deve dar ~100%)
    Kanto  -> pret/pokefirered
    Johto  -> fontes-mapas/hns
    Sinnoh -> fontes-mapas/sinnoh
    Unova  -> BW3G (gen 2, formato incomparavel: sai como "sem fonte")

PRIMEIRA VERSAO ESTAVA ERRADA e vale registrar: ela casava por NOME DE GRUPO de
mapa. As fontes usam outros nomes de grupo, entao o denominador pegava um punhado
de mapas e Johto saiu com "833% dos mapas" e Hoenn com 270%. Numero acima de 100
era o unico motivo de eu ter olhado de novo; se tivesse dado 91% eu teria
acreditado. **Comparacao so vale se os dois lados falarem do mesmo conjunto**, e
o unico jeito de garantir isso e casar MAPA A MAPA pelo nome.

Regiao sem fonte em disco aparece como "sem fonte", nunca como 100%. Nao saber e
um resultado; fingir que sabe foi o erro que esta sessao cometeu a noite toda.
"""
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.dirname(RAIZ) + "/fontes-mapas"

REGIOES = {
    "Kanto":  {"grupo": "Frlg",           "fonte": f"{FONTES}/pokefirered"},
    "Johto":  {"grupo": "Johto",          "fonte": f"{FONTES}/hns"},
    "Hoenn":  {"grupo": "TownsAndRoutes", "fonte": f"{FONTES}/pokeemerald"},
    # Sinnoh saiu de fontes-mapas/sinnoh para o pokeplatinum em 05/08/2026. O
    # motivo esta na ARMADILHA da funcao p(): a fonte antiga tem ZERO NPC nos
    # mapas de Sinnoh, entao ela media "objetos" contra um denominador vazio e
    # imprimia "fonte 0". O pokeplatinum tem os 2278 objetos de verdade, so que
    # em outro formato (events_*.json ligados por MAP_HEADER). Ver le_plat().
    # Sinnoh passa de 100% em placas (105,1% em 05/08/2026) e isso esta CERTO:
    # o denominador e so o Platinum, mas a geometria de Sinnoh veio do
    # fontes-mapas/sinnoh, que ja trazia placa propria. Medido: 31 placas a mais
    # espalhadas por 24 mapas, no maximo 2 por mapa. Nao e conversao gerando
    # placa falsa, e soma de duas fontes.
    "Sinnoh": {"grupo": "Sinnoh",         "fonte": f"{FONTES}/pokeplatinum",
               "plat": True},
    # BW3G e pokecrystal (gen 2). O formato e outro, mas e legivel: cada mapa
    # tem um .asm com warp_event, bg_event e object_event em macro. Eu tinha
    # marcado "sem fonte" por nao ter escrito o leitor, o que e diferente de nao
    # dar para medir. Ver le_gen2().
    "Unova":  {"grupo": "Unova",          "fonte": "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/bw3g",
               "gen2": True},
    # Galar (18/08/2026). ARMADILHA que custou uma sessao em `valida_warp_tile.py`
    # e vale para qualquer ferramenta desta casa: **filtrar Galar por NOME DE
    # GRUPO nao funciona**. O alocador espalhou 344 dos 438 mapas em append
    # dentro de grupos alheios (gMapGroup_IndoorRoute116 e irmaos), entao um
    # filtro por grupo enxergaria 283 mapas e mediria a regiao errada. Quem sabe
    # quais mapas sao de Galar e o censo `dev_scripts/galar_mundo.json`, gerado
    # por `mundo_galar.py` a partir da ROM do demake; e quem sabe o que a FONTE
    # tinha de gente e placa e `dev_scripts/galar_gente.json`. A ROM nao e
    # reaberta aqui: os dois censos ja estao extraidos. Ver galar().
    "Galar":  {"censo": f"{RAIZ}/dev_scripts/galar_mundo.json",
               "gente": f"{RAIZ}/dev_scripts/galar_gente.json"},
}

CAMPOS = [("object_events", "objetos (NPC, item)"),
          ("warp_events", "warps"),
          ("bg_events", "placas e sinais")]

# Piso de ARTE: abaixo disto o mapa nao e desenho, e mascara de colisao.
#
# Existe porque a tabela de cima nao enxerga arte, e isso deixou uma regiao
# inteira passar por 94% completa por SEIS DIAS. Unova tinha os 1396 NPCs, os
# 1060 warps e as 497 placas nos lugares certos, dentro de caixas com TRES
# metatiles distintos: chao, parede e porta. Presenca de evento nao e desenho.
#
# O piso e 10 e nao 3 porque 3 era o sintoma daquele bug especifico; 10 e o
# ponto onde um mapa deixa de ter mobilia. Mapa minusculo legitimo cai aqui de
# vez em quando (o elevador de Castelia tem 4 metatiles na FONTE tambem, medido
# em DeptStoreElevator.ablk), entao a coluna diz "mediana (quantos abaixo)": o
# numero entre parenteses e para investigar, nao para acusar.
PISO_ARTE = 10


def todos_os_mapas(raiz):
    p = f"{raiz}/data/maps/map_groups.json"
    if not os.path.exists(p):
        return {}
    g = json.load(open(p))
    return {m: grp for grp in g.get("group_order", []) for m in g.get(grp, [])}


def nossos_da_regiao(mapa_grupo, chave):
    if chave == "TownsAndRoutes":
        # Hoenn e "tudo que nao e das outras cinco". `galar` entrou em
        # 18/08/2026: os 438 mapas dela moram em grupos alheios, entao sem o
        # nome aqui eles caiam no balde de Hoenn. Nao mudava as tres colunas de
        # evento (nome de Galar nao casa com mapa do pokeemerald, e casados
        # descartava), mas envenenava a coluna de ARTE, que mede TODOS os
        # nossos mapas da regiao e nao so os casados.
        outras = ("frlg", "johto", "sinnoh", "unova", "galar")
        return [m for m, g in mapa_grupo.items()
                if not any(o in g.lower() or o in m.lower() for o in outras)]
    return [m for m, g in mapa_grupo.items()
            if chave.lower() in g.lower() or chave.lower() in m.lower()]


# Mapa que a FONTE tem e que JÁ ESTÁ na ROM com outro nome.
#
# Existe porque em 21/08/2026 a régua dizia que faltavam 10 mapas em Johto e 10
# em Unova que estão jogáveis desde sempre, só que com sufixo de outra região.
# `cidades_de_outra_fonte()` já desconta 732 mapas assim, mas ela casa pelo
# PREFIXO DE CIDADE (o pedaço antes do primeiro "_"), e o prefixo destes 20 não
# é nome de cidade nenhum: "CeruleanCave1", "OaksLab", "DayCare".
#
# A tabela é EXPLÍCITA de propósito. Heurística que casasse "OaksLab" com
# "PalletTown_ProfessorOaksLab_Frlg" seria solta o bastante para casar mapa
# diferente, e casamento errado não aparece como erro: aparece como completude
# alta. Cada linha abaixo traz a medida que provou o par.
APELIDOS_FONTE = {
    # --- Johto (fonte `hns`, que é hack de Johto E Kanto). A nossa versão
    # destes veio do pokefirered, com sufixo _Frlg.
    # Topologia: CeruleanCave1 warpa para 2 e para 3 (é o térreo), CeruleanCave3
    # só warpa de volta para o 1 (é o andar sem saída). Igual ao FRLG, onde o 1F
    # liga 2F e B1F. Os três layouts têm 39-40 x 23 nos dois lados.
    "CeruleanCave1": "CeruleanCave_1F_Frlg",
    "CeruleanCave2": "CeruleanCave_2F_Frlg",
    "CeruleanCave3": "CeruleanCave_B1F_Frlg",
    # Safári: casado por DIMENSÃO de layout, que bate exata nos três.
    # LAYOUT_SAFARI_ZONE1 é 51x36 como o nosso SAFARI_ZONE_CENTER; o 2 é 54x35
    # como o EAST; o 3 é 48x36 como o WEST.
    "SafariZone1": "SafariZone_Center_Frlg",
    "SafariZone2": "SafariZone_East_Frlg",
    "SafariZone3": "SafariZone_West_Frlg",
    # O "indoor" é 13x11 e o único warp dele volta para o SafariZone2, ou seja é
    # a casa de descanso da área LESTE.
    "SafariZoneIndoor": "SafariZone_East_RestHouse_Frlg",
    # Estrada da Vitória de Kanto: o hns conta os andares para BAIXO e o FRLG
    # para cima. O 1F dos dois abre na Route 23; o último andar dos dois (B2F lá,
    # 3F aqui) é o que sai no Planalto Índigo.
    "VictoryRoadKanto_1F": "VictoryRoad_1F_Frlg",
    "VictoryRoadKanto_B1F": "VictoryRoad_2F_Frlg",
    "VictoryRoadKanto_B2F": "VictoryRoad_3F_Frlg",
    # --- Unova (fonte `bw3g`, que é hack de gen 2 e carregou junto um punhado
    # de interiores de Johto e Kanto). Nenhum destes tem warp de entrada no
    # bw3g, porque o hack apagou o mapa externo que levava a eles; o conteúdo,
    # porém, está lá (a regra de sobra abaixo NÃO os pega, e nem deve).
    "CeladonGameCorner": "CeladonCity_GameCorner_Frlg",
    "CeladonGameCornerPrizeRoom": "CeladonCity_GameCorner_PrizeRoom_Frlg",
    "DayCare": "Route34_DayCare",              # o Day Care de gen 2 é o da Route 34
    "ElmsLab": "NewBarkTown_Lab",              # laboratório do Prof. Elm
    "GoldenrodGameCorner": "GoldenrodCity_GameCorner",
    "LancesRoom": "PokemonLeague_LancesRoom_Frlg",
    # O hns marca `BlackthornCity_House3` como a casa do Move Deleter (único
    # mapa de Blackthorn com `MoveDeletion` no scripts.inc dele).
    "MoveDeletersHouse": "BlackthornCity_House3",
    "NationalPark": "NationalPark_Normal",     # a variante de concurso é outro mapa
    "OaksLab": "PalletTown_ProfessorOaksLab_Frlg",
    "PokemonFanClub": "VermilionCity_PokemonFanClub_Frlg",  # o Fan Club de gen 2 é o de Vermilion
}


def normaliza(nome):
    """Nosso 'PalletTown_Frlg' e o 'PalletTown' da fonte sao o mesmo mapa."""
    nome = APELIDOS_FONTE.get(nome, nome)
    n = re.sub(r"_Frlg$", "", nome)
    n = re.sub(r"_johto$", "", n, flags=re.I)
    n = re.sub(r"^Unova_", "", n)          # Unova_AccumulaTown == AccumulaTown
    # No BW3G a rota e "R5NimbasaGate"; aqui ela virou "Rt5NimbasaGate". Sem
    # esta linha o painel dava 45 mapas de Unova como ausentes, sendo que a
    # maioria estava dentro da ROM com outro nome.
    n = re.sub(r"^R(?=\d)", "Rt", n)
    return n.lower().replace("_", "")


def le_gen2(caminho):
    """Conta eventos num mapa de pokecrystal (.asm com macros).

    O gen 2 guarda os eventos como linhas de macro no proprio .asm do mapa:
        warp_event  4, 6, R_2_ACCUMULA_GATE, 3
        bg_event   24, 14, BGEVENT_READ, AccumulaTownSign
        object_event 19, 9, SPRITE_POKEFAN_M, ...
    Contar linha de macro e a leitura certa aqui, e da o mesmo numero que o
    map.json de gen 3 daria depois de convertido.
    """
    if not os.path.exists(caminho):
        return None
    txt = open(caminho, errors="ignore").read()
    return {
        "warp_events": len(re.findall(r"^\s*warp_event\b", txt, re.M)),
        "bg_events": len(re.findall(r"^\s*bg_event\b", txt, re.M)),
        "object_events": len(re.findall(r"^\s*object_event\b", txt, re.M)),
    }


def cidades_de_outra_fonte(fonte_atual=""):
    """Prefixo de nome (a parte antes do primeiro '_') das cidades que vieram
    de OUTRA fonte. `CeladonCity_PokemonCenter` do hns e o
    `CeladonCity_PokemonCenter_1F` do pokefirered sao o mesmo lugar, mas o nome
    difere no sufixo, entao o desconto por nome inteiro nao pega. O que nao
    varia e a cidade. Sem isto, Johto saia com 63,6% dos mapas por causa de 92
    mapas de Kanto que ja estao no jogo, vindos do FireRed com outro nome."""
    cidades = set()
    for f in ("pokefirered", "pokeemerald"):
        # ARMADILHA que eu cai: sem esta linha, medir Kanto contra o
        # pokefirered descontava o pokefirered inteiro e Kanto dava 100,0% com
        # qualquer buraco. A fonte da propria regiao nunca entra no desconto.
        if f in fonte_atual:
            continue
        raiz = f"{FONTES}/{f}/data/maps"
        if os.path.isdir(raiz):
            cidades |= {m.split("_")[0].lower() for m in os.listdir(raiz)
                        if os.path.isdir(f"{raiz}/{m}")}
    return cidades


# Mapa que a fonte tem e que nao e conteudo: rascunho do autor do hack e
# variante de horario, que aqui nao existe como mapa separado.
LIXO = re.compile(r"^(NewMap|Trees|.*_Temp|Gate_)|(Day|Night)$", re.I)


def mapas_so_na_fonte(deles, nosso_mg, fonte=""):
    nossos = {normaliza(x) for x in nosso_mg}
    cidades = cidades_de_outra_fonte(fonte)
    return [m for k, m in deles.items()
            if k not in nossos
            and m.split("_")[0].lower() not in cidades
            and not LIXO.search(m)]


def _cru(n):
    """Chave crua de nome de mapa, para casar as DUAS grafias do mesmo lugar.

    A fonte escreve o destino de um warp como constante (`MAP_VICTORY_ROAD_KANTO_1F`,
    `MAP_HEADER_UNKNOWN_197`) e o mapa em si como diretório ou arquivo
    (`VictoryRoadKanto_1F`). Onde cai cada `_` varia entre os dois, então tirar
    TODOS eles é o único casamento que não depende de adivinhar a convenção.
    """
    return re.sub(r"^MAP(_HEADER)?_", "", n).replace("_", "").lower()


def _sobra_gen3(fonte):
    dest, ev = set(), {}
    for m in todos_os_mapas(fonte):
        d = json.load(open(f"{fonte}/data/maps/{m}/map.json"))
        ev[m] = sum(len(d.get(c) or []) for c in
                    ("object_events", "warp_events", "bg_events", "coord_events"))
        dest |= {_cru(w["dest_map"]) for w in d.get("warp_events") or []}
        dest |= {_cru(c["map"]) for c in d.get("connections") or []}
    return {m: (n, _cru(m) in dest) for m, n in ev.items()}


def _sobra_gen2(fonte):
    dest, ev = set(), {}
    for f in glob.glob(f"{fonte}/maps/*.asm"):
        txt = open(f, errors="ignore").read()
        ev[os.path.basename(f)[:-4]] = len(re.findall(
            r"^\s*(?:warp|bg|object|coord)_event\b", txt, re.M))
        dest |= {_cru(x) for x in re.findall(
            r"^\s*warp_event\s+[^,]+,[^,]+,\s*([A-Z0-9_]+)\s*,", txt, re.M)}
    return {m: (n, _cru(m) in dest) for m, n in ev.items()}


def _sobra_plat(fonte, heads):
    dest, ev = set(), {}
    for h, arq in heads.items():
        p = f"{fonte}/res/field/events/{arq[0]}.json"
        if not os.path.exists(p):
            ev[h] = 0
            continue
        d = json.load(open(p))
        ev[h] = sum(len(d.get(c) or []) for c in
                    ("object_events", "warp_events", "bg_events", "coord_events"))
        dest |= {_cru(w["dest_header_id"]) for w in d.get("warp_events") or []}
    return {h: (n, _cru(h) in dest) for h, n in ev.items()}


def julga_sobra(medido):
    """As DUAS condições, e só elas. Julgamento separado da leitura de disco
    para poder ser testado com medição plantada em `--demo`."""
    return {m for m, (eventos, tem_entrada) in medido.items()
            if not eventos and not tem_entrada}


def sobra_de_tabela(fonte, cfg, heads=None, _cache={}):
    """Registro da fonte que NÃO É LUGAR: sobra de tabela do motor dela.

    Existe porque a coluna `mapas` estava dividindo por um denominador que tem
    53 headers `UNKNOWN_*` do Platinum, 8 mapas do FireRed que o próprio
    FireRed nunca ligou a lugar nenhum, e as sentinelas `EVERYWHERE` e
    `NOTHING`, que são valor de enum e não mapa.

    A REGRA É MEDIDA, não é lista de nome: sai do denominador o header que tem
    **zero evento na fonte E nenhum warp (ou conexão) de entrada vindo de outro
    mapa da fonte**. As duas condições juntas, sempre: mapa sem warp de entrada
    mas COM conteúdo fica (é o caso dos 10 interiores de Johto/Kanto que o bw3g
    carregou sem o mapa externo), e mapa sem conteúdo mas COM porta fica
    também (alguém entra nele).

    ARMADILHA, e por isso `--detalhe` imprime a lista inteira: a regra corta por
    AUSÊNCIA DE DADO, então ela também pega header cujo conteúdo a fonte
    simplesmente não traz. Medido em 21/08/2026: os 9 andares do Distortion
    World do Platinum apontam para `events_empty` e caem aqui, e o Distortion
    World é conteúdo de verdade. Ninguém pode esconder corte de escopo atrás
    desta regra: o corte de escopo é decisão do Gui, e a lista impressa é o
    lugar onde ele o vê.
    """
    if fonte not in _cache:
        _cache[fonte] = julga_sobra(
            _sobra_plat(fonte, heads) if cfg.get("plat") else
            _sobra_gen2(fonte) if cfg.get("gen2") else
            _sobra_gen3(fonte))
    return _cache[fonte]


def le_plat(fonte, header):
    """Conta eventos num mapa do pokeplatinum (formato de DS).

    O mapa la nao guarda os eventos: guarda o NOME do arquivo de eventos, em
    include/data/map_headers.h. Placa de rua no Platinum e object_event com
    grafico de SIGNBOARD, nao bg_event, entao ela e contada como placa aqui,
    senao o denominador de "placas" fica quase zero e a coluna mente para cima.
    """
    import importa_npcs_sinnoh as I
    arq = I.headers_do_platinum().get(header)
    if not arq:
        return None
    p = f"{fonte}/res/field/events/{arq[0]}.json"
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    objs = d.get("object_events") or []
    placas = [o for o in objs
              if any(t in o.get("graphics_id", "") for t in I.GRAFICOS_PLACA)]
    return {"object_events": len(objs) - len(placas),
            "warp_events": len(d.get("warp_events") or []),
            "bg_events": len(d.get("bg_events") or []) + len(placas)}


def _distintos(blob):
    """Metatiles distintos num `map.bin`.

    Cada celula do layout e um u16: os 10 bits de baixo sao o METATILE e os 6 de
    cima sao colisao e elevacao. Sem a mascara, dois pedacos do mesmo desenho com
    elevacao diferente contariam como desenho diferente e a coluna mentiria para
    cima. Ver `include/fieldmap.h` (MAPGRID_METATILE_ID_MASK = 0x03FF).
    """
    return {(blob[i] | (blob[i + 1] << 8)) & 0x3FF for i in range(0, len(blob), 2)}


def _layouts(_cache={}):
    if not _cache:
        d = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
        _cache.update({l["id"]: l["blockdata_filepath"] for l in d["layouts"]
                       if l.get("id")})
    return _cache


def arte(nossos):
    """(mediana de metatiles distintos por mapa, quantos abaixo do piso, n)."""
    n = []
    for m in nossos:
        p = f"{RAIZ}/data/maps/{m}/map.json"
        if not os.path.exists(p):
            continue
        arq = _layouts().get(json.load(open(p)).get("layout"))
        if arq and os.path.exists(f"{RAIZ}/{arq}"):
            n.append(len(_distintos(open(f"{RAIZ}/{arq}", "rb").read())))
    if not n:
        return None
    n.sort()
    meio = n[len(n) // 2] if len(n) % 2 else (n[len(n) // 2 - 1] + n[len(n) // 2]) / 2
    return meio, sum(1 for x in n if x < PISO_ARTE), len(n)


def fmt_arte(a):
    if not a:
        return "  --  "
    meio, abaixo, _ = a
    return f"{meio:g} ({abaixo})"


def galar(cfg):
    """Galar medida no `map.json` de hoje, como toda região, com denominador filtrado.

    ARMADILHA CONSERTADA EM 21/08/2026, e ela custou uma rodada inteira: esta
    função lia o NUMERADOR do censo `galar_gente.json`, que é um arquivo
    CONGELADO, gerado antes da fase de conteúdo. A onda de 20/08 pôs 337 falas,
    52 placas e 56 bolas de item na região e a linha da tabela NÃO SE MEXEU,
    porque o censo não foi regerado. Número que não se mexe depois de trabalho
    feito não é região parada: é régua quebrada. Agora o numerador sai do
    `data/maps/<mapa>/map.json`, medido na hora, igual ao das outras cinco.

    O DENOMINADOR é que vem do censo, e só a parte dele que é COLOCÁVEL:
      objetos -> os 1.111 que o filtro G4 aprovou ("entrou mudo"). Os outros
                 3.051 registros da fonte nunca podem virar NPC (gráfico de
                 Pokémon, tile não andável, cenário de script, em cima de warp);
                 contar com eles dava 26,7% e media a fonte, não a obra.
      placas  -> 202, que são os 214 bg da fonte menos os 12 sem item traduzível.
    A contagem do que ficou de fora sai em `--detalhe`, para o corte ser visível.

    Devolve (nossos_mapas, {campo: (nosso, denominador)}, extras).
    """
    cen = json.load(open(cfg["censo"]))
    gente = json.load(open(cfg["gente"]))
    nossos = [v["nome"] for v in cen["de_para"].values()]
    obj = [l for l in gente["linhas"] if l["tipo"] == "objeto"]
    bg = [l for l in gente["linhas"] if l["tipo"] == "bg"]
    # "NPC de obra" é o marinheiro da travessia, que não veio da fonte: ele não
    # entra em nenhum dos dois lados, senão inventa numerador sem denominador.
    fonte_obj = [l for l in obj if "nao vem da fonte" not in l["motivo"]]
    colocaveis = [l for l in fonte_obj if l["motivo"] == "entrou mudo"]
    # "lixo de leitura" são os kinds 5 e 6, que não existem em nenhum dos dois
    # motores: não são placa que faltou, são bytes que não queriam dizer nada.
    fonte_bg = [l for l in bg if "lixo de leitura" not in l["motivo"]]
    placaveis = [l for l in fonte_bg if "sem item traduzivel" not in l["motivo"]]

    n_obj = n_bg = n_script = 0
    for m in nossos:
        d = json.load(open(f"{RAIZ}/data/maps/{m}/map.json"))
        oe = d.get("object_events") or []
        n_obj += len(oe)
        n_script += sum(1 for o in oe if str(o.get("script") or "0") not in ("0", ""))
        n_bg += len(d.get("bg_events") or [])
    extras = {"script": (n_script, n_obj),
              "obj_impossiveis": len(fonte_obj) - len(colocaveis),
              "obj_fonte": len(fonte_obj),
              "bg_sem_traducao": len(fonte_bg) - len(placaveis),
              "bg_fonte": len(fonte_bg)}
    return nossos, {
        "object_events": (n_obj, len(colocaveis)),
        "warp_events": (cen["warps_gravados"], cen["warps_gravados"]),
        "bg_events": (n_bg, len(placaveis)),
    }, extras


def confere_apelidos(tabela=None):
    """Problemas na tabela de apelidos. Lista vazia = tabela sã.

    Apelido errado não aparece como erro em lugar nenhum: aparece como
    completude ALTA, que é o jeito mais caro de errar nesta casa. Então a
    tabela é conferida, e não apenas escrita:
      1. o destino tem que EXISTIR em `data/maps` (senão o mapa não está na ROM
         e o "já está na ROM com outro nome" é mentira);
      2. dois mapas da fonte não podem apontar para o MESMO mapa nosso (sinal de
         chute: 1F, 2F e B1F todos casados com o mesmo andar);
      3. a chave não pode ser nome de um mapa NOSSO, senão `normaliza` passaria
         a reescrever o nosso próprio mapa e o casamento inverteria.
    """
    tabela = APELIDOS_FONTE if tabela is None else tabela
    nossos = set(todos_os_mapas(RAIZ))
    ruim = []
    vistos = {}
    for fonte, meu in tabela.items():
        if not os.path.exists(f"{RAIZ}/data/maps/{meu}/map.json"):
            ruim.append(f"{fonte}: o alvo {meu} não existe em data/maps")
        if meu in vistos:
            ruim.append(f"{fonte} e {vistos[meu]} apontam para o mesmo {meu}")
        vistos[meu] = fonte
        if fonte in nossos:
            ruim.append(f"{fonte} também é nome de mapa NOSSO")
    return ruim


def eventos(raiz, mapa):
    p = f"{raiz}/data/maps/{mapa}/map.json"
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return {c: len(d.get(c) or []) for c, _ in CAMPOS}


def main():
    alvo = None
    if "--detalhe" in sys.argv:
        alvo = sys.argv[sys.argv.index("--detalhe") + 1]

    nosso_mg = todos_os_mapas(RAIZ)
    print("Completude por região, normalizada pela FONTE, mapa a mapa.")
    print("100% = tão completo quanto o jogo de onde a região veio.\n")
    print("A coluna ARTE não é completude contra a fonte: é a variedade do "
          "desenho, mediana de\nmetatiles distintos por mapa, com quantos mapas "
          f"abaixo de {PISO_ARTE} entre parênteses.\n")
    print("A coluna SCRIPT só existe para Galar, e de propósito: lá a colocação "
          "está feita e o que\nfalta é fala. Nas outras cinco a colocação é que "
          "está em jogo, e a coluna não diria nada.\n")
    print(f"{'região':8} {'mapas':>11} {'objetos':>11} {'warps':>11} "
          f"{'placas':>11} {'script':>11} {'arte':>11}")

    faltando_total = {}
    sobras = {}
    galar_extras = None
    for nome, cfg in REGIOES.items():
        if alvo and alvo.lower() != nome.lower():
            continue
        if cfg.get("censo"):
            nossos, pares, galar_extras = galar(cfg)
            def q(c, pares=pares):
                a, b = pares[c]
                return f"{100*a/b:5.1f}%" if b else "  --  "
            a, b = galar_extras["script"]
            print(f"{nome:8} {100.0:10.1f}% {q('object_events'):>11} "
                  f"{q('warp_events'):>11} {q('bg_events'):>11} "
                  f"{100*a/b:9.1f}%  {fmt_arte(arte(nossos)):>11}")
            faltando_total[nome] = ([], [])
            continue
        fonte = cfg["fonte"]
        if not (fonte and os.path.isdir(fonte)):
            nossos = nossos_da_regiao(nosso_mg, cfg["grupo"])
            print(f"{nome:8} {len(nossos):>8} sem fonte" + " " * 30)
            continue

        gen2, plat = cfg.get("gen2"), cfg.get("plat")
        if plat:
            sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
            import importa_npcs_sinnoh as I
            heads = I.headers_do_platinum()
            deles = {}
            for h in heads:
                deles.setdefault(I.chave(h), h)
            nossos = I.nossos_mapas_sinnoh()
            casados = [(m, I.APELIDOS.get(m) or deles.get(I.chave(m)))
                       for m in nossos]
            casados = [(m, h) for m, h in casados if h in heads]
            casadas_norm = {I.chave(h) for _, h in casados}
            so_na_fonte = [h for k, h in deles.items() if k not in casadas_norm]
            sobra = sobra_de_tabela(fonte, cfg, heads)
        else:
            if gen2:
                deles = {normaliza(os.path.basename(f)[:-4]): os.path.basename(f)[:-4]
                         for f in glob.glob(f"{fonte}/maps/*.asm")}
            else:
                deles = {normaliza(m): m for m in todos_os_mapas(fonte)}
            nossos = nossos_da_regiao(nosso_mg, cfg["grupo"])
            casados = [(m, deles[normaliza(m)]) for m in nossos if normaliza(m) in deles]
            so_na_fonte = mapas_so_na_fonte(deles, nosso_mg, fonte)
            sobra = sobra_de_tabela(fonte, cfg)
        # A sobra de tabela da fonte sai do DENOMINADOR (ver `sobra_de_tabela`),
        # e o que saiu vai impresso em `--detalhe`.
        sobras[nome] = sorted(m for m in so_na_fonte if m in sobra)
        so_na_fonte = [m for m in so_na_fonte if m not in sobra]
        # Mapas que a FONTE tem e nos nao.
        #
        # ARMADILHA: o denominador tem que descontar o que ja veio por OUTRA
        # fonte. O hns e um hack de Johto E Kanto, entao ele tem PalletTown,
        # ViridianCity e mais 730. Comparando so contra os nossos mapas de
        # Johto, esses 732 apareciam como "faltando" e Johto saia com 23,3% dos
        # mapas, quando o que falta de verdade e outra coisa. Nos importamos
        # Kanto do pokefirered, entao eles JA ESTAO no jogo.
        # Por isso o desconto e contra TODOS os nossos mapas, nao so os da regiao.

        soma_n = {c: 0 for c, _ in CAMPOS}
        soma_f = {c: 0 for c, _ in CAMPOS}
        piores = []
        for meu, seu in casados:
            a = eventos(RAIZ, meu)
            b = (le_plat(fonte, seu) if plat else
                 le_gen2(f"{fonte}/maps/{seu}.asm") if gen2 else
                 eventos(fonte, seu))
            if not a or not b:
                continue
            for c, _ in CAMPOS:
                soma_n[c] += a[c]
                soma_f[c] += b[c]
            if b["object_events"] >= 5:
                r = a["object_events"] / b["object_events"]
                if r < 0.75:
                    piores.append((r, meu, a["object_events"], b["object_events"]))

        def p(c):
            # ARMADILHA: denominador zero nao e "nao da para medir", e um FATO
            # sobre a fonte. A fonte de Sinnoh tem 2778 objetos no total e ZERO
            # nos 69 mapas de cidade de Sinnoh: os objetos dela sao todos de
            # Hoenn. Ou seja, nao ha NPC de Sinnoh para importar dali, e quem
            # quiser fechar essa lacuna tem que ir no pokeplatinum.
            # Imprimir "n/a" escondia isso; agora diz que a fonte esta vazia.
            if not soma_f[c]:
                return "fonte 0" if soma_n[c] else "  --  "
            return f"{100*soma_n[c]/soma_f[c]:5.1f}%"
        # mapas: o denominador e o que a fonte tem daquela regiao, e para as
        # fontes que sao o jogo inteiro isso e o total delas
        pm = 100.0 * len(casados) / max(1, len(casados) + len(so_na_fonte))
        print(f"{nome:8} {pm:10.1f}% {p('object_events'):>11} "
              f"{p('warp_events'):>11} {p('bg_events'):>11} "
              f"{'--':>10}  {fmt_arte(arte(nossos)):>11}")
        faltando_total[nome] = (so_na_fonte, sorted(piores)[:6])

    if not alvo or alvo.lower() == "galar":
        print("\nGalar é GEOMETRIA INTEIRA e conteúdo em obra. Os 438 mapas "
              "estão com tileset provado\npixel a pixel, 1.473 warps e 1.260 "
              "objetos colocados; a fase de conteúdo começou em\n20/08/2026 e "
              "hoje 394 desses objetos falam. Sem treinador, encontro, ginásio "
              "nem Liga:\na fila está em `dev_scripts/fila_galar.json`. As "
              "colunas `objetos` e `placas` dividem pelo\nque é COLOCÁVEL, não "
              "pelo total da fonte (ver `--detalhe Galar`), porque 3.051 "
              "registros\nda fonte nunca podem virar NPC. `objetos` passa de "
              "100% porque a obra pôs coisa que a\nfonte não tinha nesse "
              "formato: 52 placas e 56 bolas de item com flag própria.")

    if alvo:
        for nome, (falta, piores) in faltando_total.items():
            print(f"\n=== {nome}: {len(falta)} mapas que a fonte tem e nós não ===")
            for m in falta[:15]:
                print(f"   {m}")
            if piores:
                print(f"\n=== {nome}: mapas mais vazios que o original ===")
                for r, m, a, b in piores:
                    print(f"   {100*r:5.1f}%  {m:42} {a} de {b} objetos")
        for nome, fora in sobras.items():
            if not fora:
                continue
            print(f"\n=== {nome}: {len(fora)} registros da fonte FORA do "
                  f"denominador ===")
            print("   critério MEDIDO: zero evento na fonte E nenhum warp ou "
                  "conexão de entrada.")
            print("   não é corte de escopo; se algo aqui for lugar de "
                  "verdade, a fonte é que não trouxe o dado.")
            for m in fora:
                print(f"   {m}")
        if galar_extras:
            g = galar_extras
            print("\n=== Galar: o que ficou FORA do denominador ===")
            print(f"   objetos: {g['obj_impossiveis']} dos {g['obj_fonte']} "
                  "registros da fonte não podem virar NPC")
            print("      (gráfico de Pokémon, tile não andável, cenário de "
                  "script, em cima de warp). Sobram")
            print(f"      {g['obj_fonte'] - g['obj_impossiveis']} colocáveis, "
                  "que são o denominador da coluna `objetos`.")
            print(f"   placas: {g['bg_sem_traducao']} dos {g['bg_fonte']} bg da "
                  "fonte são item sem tradução neste motor.")
            print(f"      Sobram {g['bg_fonte'] - g['bg_sem_traducao']}, que são "
                  "o denominador da coluna `placas`.")
            a, b = g["script"]
            print(f"   objetos COM script hoje: {a} de {b} ({100*a/b:.1f}%). "
                  "É aqui que mora o trabalho.")
    else:
        print("\nuse --detalhe <região> para ver o que falta em cada uma")
    return 0


def demo():
    """Duas regras que a primeira versao quebrou, mais a coluna de arte."""
    # 1. mapa da fonte com sufixo nosso e o MESMO mapa
    assert normaliza("PalletTown_Frlg") == normaliza("PalletTown")
    assert normaliza("Route3_Frlg") == normaliza("Route3")
    # 2. nomes diferentes continuam diferentes
    assert normaliza("Route3_Frlg") != normaliza("Route4")
    # 3. arte conta METATILE, e metatile e so os 10 bits de baixo. A celula
    #    0xF001 e o mesmo desenho da 0x0001 com outra colisao e elevacao.
    assert _distintos(b"\x00\x00\x01\x04") == {0, 1}
    assert _distintos(b"\x01\x00\x01\xF0") == {1}
    assert _distintos(b"\xFF\xFF") == {0x3FF}
    # 4. a mutacao tem que ser pega: trocar um metatile muda a conta
    assert _distintos(b"\x01\x00\x01\x00") != _distintos(b"\x01\x00\x02\x00")
    # 5. Galar sai do censo para o DENOMINADOR e do map.json para o NUMERADOR.
    #    O censo é congelado; se o numerador voltar a sair dele, a linha para de
    #    se mexer quando a obra anda, que foi o defeito consertado em 21/08/2026.
    nossos, pares, extras = galar(REGIOES["Galar"])
    assert len(nossos) == 438, len(nossos)
    assert pares["warp_events"][0] == pares["warp_events"][1] == 1473
    gente = json.load(open(REGIOES["Galar"]["gente"]))
    assert pares["object_events"][0] != gente["objetos_gravados"], (
        "numerador de Galar voltou a sair do censo congelado")
    assert extras["script"][0] <= extras["script"][1] == pares["object_events"][0]
    # o denominador é o COLOCÁVEL, não o total da fonte
    assert pares["object_events"][1] + extras["obj_impossiveis"] == extras["obj_fonte"]
    assert pares["bg_events"][1] + extras["bg_sem_traducao"] == extras["bg_fonte"]

    # 6. a tabela de apelidos tem que estar sã, e apelido errado tem que REPROVAR
    assert confere_apelidos() == [], confere_apelidos()
    assert normaliza("OaksLab") == normaliza("PalletTown_ProfessorOaksLab_Frlg")
    assert normaliza("CeruleanCave3") == normaliza("CeruleanCave_B1F_Frlg")
    # ...e continuar separando o que é separado: o 1F não pode virar o B1F
    assert normaliza("CeruleanCave1") != normaliza("CeruleanCave_B1F_Frlg")
    # mutação plantada 1: alvo que não existe na ROM
    assert confere_apelidos({"Xyz": "MapaQueNaoExiste"})
    # mutação plantada 2: dois andares da fonte casados com o mesmo mapa nosso
    assert confere_apelidos({"CeruleanCave1": "CeruleanCave_1F_Frlg",
                             "CeruleanCave2": "CeruleanCave_1F_Frlg"})

    # 7. a sobra de tabela sai por MEDIDA, e as duas condições valem juntas.
    #    mutação plantada 3: um mapa COM evento na fonte, e com cara de sobra no
    #    nome, jogado no balde. Quem trocar a regra medida por lista de nome
    #    reprova aqui.
    plantado = {"MAP_HEADER_UNKNOWN_999": (7, False),   # tem evento: FICA
                "MAP_HEADER_UNUSED_CASA": (0, True),    # tem porta: FICA
                "MAP_HEADER_SOBRA_DE_VERDADE": (0, False)}
    assert julga_sobra(plantado) == {"MAP_HEADER_SOBRA_DE_VERDADE"}, julga_sobra(plantado)
    # e na fonte de verdade: os 8 do FireRed são sobra, e nenhum deles tem evento
    med = _sobra_gen3(REGIOES["Kanto"]["fonte"])
    assert all(med[m] == (0, False) for m in julga_sobra(med))
    assert med["Prototype_SeviiIsle_6"] == (0, False)
    # os 10 interiores que o bw3g carregou sem o mapa externo NÃO são sobra:
    # não têm warp de entrada, mas têm conteúdo.
    med2 = _sobra_gen2(REGIOES["Unova"]["fonte"])
    assert med2["ElmsLab"][0] > 0 and med2["ElmsLab"][1] is False
    assert "ElmsLab" not in julga_sobra(med2)

    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
