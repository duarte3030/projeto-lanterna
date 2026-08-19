#!/usr/bin/env python3
"""B6 Sinnoh, bloco S1: a máquina de vars, flags e gatilhos de `PLANO-OBRAS-SINNOH.md`.

    python3 dev_scripts/maquina_sinnoh.py            # só o censo, não grava
    python3 dev_scripts/maquina_sinnoh.py --demo     # autoteste, não grava
    python3 dev_scripts/maquina_sinnoh.py --gravar   # escreve vars.h, flags.h,
                                                     # map.json, scripts.inc e o censo

## O que este arquivo faz, e o que ele NÃO faz

Faz: apelida as 49 vars da tabela do plano, apelida as flags dos grupos de
`hidden_flag` que sobram depois das decisões 3 a 6, planta os `coord_events`
dos gatilhos portáveis nos `map.json` (span expandido, decisão 7) e um
ESQUELETO de rótulo no `scripts.inc` de cada mapa que recebeu gatilho, e grava
o censo em `dev_scripts/maquina_sinnoh.json`.

Não faz: cena. O esqueleto é `@ TODO S<leva>` + `end`, e a fila continua
cobrando a cena até o executor da leva escrever o corpo (é o que o plano diz em
"A máquina (bloco S1)"). Também não põe objeto de `hidden_flag` no mapa: isso é
trabalho das levas S3 a S7, que já vão achar a flag pronta aqui.

**Nenhum número deste arquivo foi digitado de memória.** As tabelas literais
vêm de `PLANO-OBRAS-SINNOH.md`; o resto sai de varredura sobre
`dev_scripts/fila_b6.json`, `../fontes-mapas/pokeplatinum` e o próprio repo.
Conserto de arquivo gerado mora aqui, nunca no arquivo gerado (lição Kiyo).

## Três coisas que a varredura de 17/08/2026 achou, e que mudam o plano

1. **O orçamento de flags do plano morreu.** A consolidação de Kanto
   (commit 652776174a) alocou 245 de 245 endereços da faixa `0x190B` a
   `0x19FF` que o plano tinha reservado para Sinnoh (prova:
   `FLAG_HIDE_ROUTE24_TM45` = `FLAG_UNUSED_0x191A`), e ainda comeu até
   `0x1A4B`. A faixa desta obra passa a ser o TRANSBORDO que o próprio plano
   já apontava, `0x1B00+`, medido livre por `dev_scripts/flags_livres.py`
   (contíguo livre de `0x1A4C` a `0x2025`). `0x1B00` em vez de `0x1A4C`
   porque `0x1A00` a `0x1AFF` é reserva de Unova, e invadir reserva alheia foi
   exatamente o que doeu aqui.
2. **`hidden_flag` da fonte nem sempre é flag.** 34 dos 247 grupos de Sinnoh
   têm `hidden_flag` valendo `MAP_HEADER_*`. Não é flag escondida: são objetos
   CLONE (`clone_id` preenchido, ex.: a placa da creche em
   `events_route_210_south.json`), e o campo guarda o mapa de ORIGEM do clone.
   Clone não ganha flag, e nunca ganhou: sai do orçamento inteiro.
3. **`VAR_MAP_LOCAL_0x0F` do Villa empilha 4 gatilhos no mesmo tile.** A
   conversão de coordenada é proporcional (mapa da fonte é maior que o nosso),
   então span expandido de mapas grandes colapsa. Os 4 do Villa têm valores
   diferentes (6, 8, 10, 12), então um só dispara por vez e o mundo não trava;
   já `TwinleafTown_MainHouse_2F` empilha DOIS com o mesmo valor 0 e scripts
   diferentes, e ali só o primeiro dispara. Está no censo em
   `tiles_empilhados`, para o executor da leva desempatar na hora da cena.

## As decisões do plano, e como elas viram código aqui

- Decisão 1: `VAR_MAP_LOCAL_0xNN` vira `VAR_TEMP_N` (`temp_da_local`), sem
  alias novo. A obrigação de conferir o mapa de destino está dentro de
  `censo()`: se o `scripts.inc` do destino já cita aquele `VAR_TEMP_`, o
  gatilho NÃO é plantado e o motivo vai para o censo. Medido em 17/08/2026:
  zero colisão nos 16 mapas que usam temp. O `<leva>` desses esqueletos sai
  `S?` de propósito: o plano não atribui arco a var local de mapa, e chutar
  um seria invenção de executor.
- Decisão 2: `var_value` é o `value` da fonte, literal, sem renumerar.
- Decisões 3, 4 e 5: `FORA_DE_ESCOPO` lista as 12 vars que não viram alias nem
  gatilho (5 descartadas, Amity, 6 de acompanhante). Amity vira warp comum numa
  onda futura, não é trabalho desta máquina.
- Decisão 6: `POKECENTER_MART` tira os 41 grupos repetidos do orçamento.
- Decisão 7: span vira N `coord_events` de 1 tile, com dedupe DEPOIS da
  conversão (dois tiles da fonte podem cair no mesmo tile nosso; dois
  `coord_events` idênticos no mesmo tile seriam lixo, não fidelidade).
- Decisão 8: índice `script: N` é o N-ésimo `ScriptEntry`, 1-based. O `--demo`
  prova isso nos dois mapas de prova do plano antes de qualquer escrita.
- Decisão 9: nome `FLAG_SINNOH_ESCONDE_<resto>`, e reuso tem precedência. O
  reuso aqui é por PROVA, em duas formas, e as duas mecânicas:
  (a) a flag da fonte já existe com o MESMO nome em `flags.h` (só
  `FLAG_HIDE_BATTLE_TOWER_REPORTER`, que é do Emerald de fábrica);
  (b) a fila marcou o grupo como "sem bloqueio", ou seja, provou que o objeto
  já plantado no nosso `map.json` carrega uma flag que existe em `flags.h`.
  Empate (dois candidatos, ou candidato já reivindicado por outro grupo da
  fonte) NÃO vira fusão: fica `ambiguo` no censo e volta para a condutora,
  que é o que a decisão 9 manda.
- Decisão 10: o censo é artefato. Não editar `maquina_sinnoh.json` à mão.

## Colisão de onda (17/08/2026)

O bloco S2 está escrevendo AGORA nos 8 mapas dos grupos "sem bloqueio". Esta
máquina não encosta nos `map.json`/`scripts.inc` deles nesta rodada:
`COLISAO_ONDA` abaixo. Os gatilhos desses mapas ficam no censo como
`adiado_colisao_onda` e entram na onda seguinte. `flags.h` e `vars.h` não são
disputados: eles são do S1.
"""
import collections
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import fila_b6 as F                      # noqa: E402  mapas_casados_sinnoh
import importa_npcs_sinnoh as S          # noqa: E402  PLAT/conversor_de_coordenada

MEDIDO_EM = "17/08/2026"
CENSO = os.path.join(REPO, "dev_scripts/maquina_sinnoh.json")
VARS_H = os.path.join(REPO, "include/constants/vars.h")
FLAGS_H = os.path.join(REPO, "include/constants/flags.h")

# --------------------------------------------------------------------------
# TABELA DE VARS: transcrição LITERAL da seção "Tabela de vars" de
# PLANO-OBRAS-SINNOH.md (fonte -> alias -> endereço). Não recalcular, não
# reordenar: o endereço é contrato, e quem muda contrato é o plano.
VARS = [
    ("VAR_ACUITY_LAKEFRONT_STATE", "VAR_SINNOH_ACUITY_BEIRA_ESTADO", 0x4130),
    ("VAR_CANALAVE_CITY_STATE", "VAR_SINNOH_CANALAVE_ESTADO", 0x4131),
    ("VAR_CELESTIC_TOWN_ELDER_STATE", "VAR_SINNOH_CELESTIC_ANCIA_ESTADO", 0x4132),
    ("VAR_ETERNA_CITY_BLOCK_EXITS_STATE", "VAR_SINNOH_ETERNA_BLOQUEIO_SAIDAS", 0x4133),
    ("VAR_ETERNA_CITY_STATE", "VAR_SINNOH_ETERNA_ESTADO", 0x4134),
    ("VAR_GALACTIC_HQ_4F_STATE", "VAR_SINNOH_QG_4F_ESTADO", 0x4135),
    ("VAR_GALACTIC_HQ_CONTROL_ROOM_STATE", "VAR_SINNOH_QG_SALA_CONTROLE_ESTADO", 0x4136),
    ("VAR_GALACTIC_HQ_HALL_STATE", "VAR_SINNOH_QG_HALL_ESTADO", 0x4137),
    ("VAR_HALL_OF_ORIGIN_STATE", "VAR_SINNOH_SALAO_ORIGEM_ESTADO", 0x4138),
    ("VAR_HEARTHOME_CITY_STATE", "VAR_SINNOH_HEARTHOME_ESTADO", 0x4139),
    ("VAR_JUBILIFE_CITY_STATE", "VAR_SINNOH_JUBILIFE_ESTADO", 0x413A),
    ("VAR_JUBILIFE_LOOKER_PAL_PAD_STATE", "VAR_SINNOH_JUBILIFE_LOOKER_ESTADO", 0x413B),
    ("VAR_MT_CORONET_1F_SOUTH_STATE", "VAR_SINNOH_CORONET_1F_SUL_ESTADO", 0x413C),
    ("VAR_MT_CORONET_2F_STATE", "VAR_SINNOH_CORONET_2F_ESTADO", 0x413D),
    ("VAR_OREBURGH_CITY_STATE", "VAR_SINNOH_OREBURGH_ESTADO", 0x413E),
    ("VAR_OREBURGH_GATE_1F_HIKER_STATE", "VAR_SINNOH_OREBURGH_PORTAO_ANDARILHO", 0x413F),
    ("VAR_PASTORIA_CITY_CROAGUNK_SCENE_STATE", "VAR_SINNOH_PASTORIA_CROAGUNK_CENA", 0x4140),
    ("VAR_PASTORIA_CITY_OBSERVATORY_GATE_1F_STATE", "VAR_SINNOH_PASTORIA_OBSERVATORIO_ESTADO", 0x4141),
    ("VAR_PASTORIA_CITY_STATE", "VAR_SINNOH_PASTORIA_ESTADO", 0x4142),
    ("VAR_PLAYER_HOUSE_RIVAL_STATE", "VAR_SINNOH_CASA_JOGADOR_RIVAL_ESTADO", 0x4143),
    ("VAR_PLAYER_HOUSE_STATE", "VAR_SINNOH_CASA_JOGADOR_ESTADO", 0x4144),
    ("VAR_POKEMON_MANSION_OFFICE_BLOCK_STATUE_STATE", "VAR_SINNOH_MANSAO_ESTATUA_ESTADO", 0x4145),
    ("VAR_RESORT_AREA_STATE", "VAR_SINNOH_RESORT_ESTADO", 0x4146),
    ("VAR_RIVAL_BEAT_SUNYSHORE_GYM", "VAR_SINNOH_RIVAL_VENCEU_SUNYSHORE", 0x4147),
    ("VAR_ROUTE_202_STATE", "VAR_SINNOH_R202_ESTADO", 0x4148),
    ("VAR_ROUTE_203_RIVAL_STATE", "VAR_SINNOH_R203_RIVAL_ESTADO", 0x4149),
    ("VAR_ROUTE_207_COUNTERPART_TRIGGER_STATE", "VAR_SINNOH_R207_COMPANHEIRO_ESTADO", 0x414A),
    ("VAR_ROUTE_209_GATE_TO_HEARTHOME_CITY_STATE", "VAR_SINNOH_R209_PORTAO_HEARTHOME", 0x414B),
    ("VAR_ROUTE_217_STATE", "VAR_SINNOH_R217_ESTADO", 0x414C),
    ("VAR_ROUTE_218_GATE_TO_CANALAVE_CITY_STATE", "VAR_SINNOH_R218_PORTAO_CANALAVE", 0x414D),
    ("VAR_ROUTE_224_STATE", "VAR_SINNOH_R224_ESTADO", 0x414E),
    ("VAR_ROUTE_227_BUCK_STATE", "VAR_SINNOH_R227_BUCK_ESTADO", 0x414F),
    ("VAR_ROUTE_227_WAKE_RIVAL_STATE", "VAR_SINNOH_R227_WAKE_RIVAL_ESTADO", 0x4150),
    ("VAR_SANDGEM_TOWN_STATE", "VAR_SINNOH_SANDGEM_ESTADO", 0x4151),
    ("VAR_SNOWPOINT_CITY_STATE", "VAR_SINNOH_SNOWPOINT_ESTADO", 0x4152),
    ("VAR_SOLACEON_TOWN_STATE", "VAR_SINNOH_SOLACEON_ESTADO", 0x4153),
    ("VAR_SPEAR_PILLAR_STATE", "VAR_SINNOH_SPEAR_PILLAR_ESTADO", 0x4154),
    ("VAR_STARK_MOUNTAIN_OUTSIDE_STATE", "VAR_SINNOH_STARK_FORA_ESTADO", 0x4155),
    ("VAR_SUNYSHORE_CITY_STATE", "VAR_SINNOH_SUNYSHORE_ESTADO", 0x4156),
    ("VAR_TWINLEAF_TOWN_GUITARIST_TRIGGER_STATE", "VAR_SINNOH_TWINLEAF_GUITARRISTA", 0x4157),
    ("VAR_TWINLEAF_TOWN_RIVAL_TRIGGER_STATE", "VAR_SINNOH_TWINLEAF_RIVAL", 0x4158),
    ("VAR_VALLEY_WINDWORKS_STATE", "VAR_SINNOH_WINDWORKS_ESTADO", 0x4159),
    ("VAR_VALLEY_WINDWORKS_TEAM_GALACTIC_STATE", "VAR_SINNOH_WINDWORKS_GALACTICA_ESTADO", 0x415A),
    ("VAR_VALOR_LAKEFRONT_BLOCK_SUNYSHORE_STATE", "VAR_SINNOH_VALOR_BLOQUEIO_SUNYSHORE", 0x415B),
    ("VAR_VEILSTONE_CITY_CRASHER_WAKE_STATE", "VAR_SINNOH_VEILSTONE_WAKE_ESTADO", 0x415C),
    ("VAR_VEILSTONE_CITY_GALACTIC_WAREHOUSE_STATE", "VAR_SINNOH_VEILSTONE_ARMAZEM_ESTADO", 0x415D),
    ("VAR_VEILSTONE_WAREHOUSE_GUARDS_FIGHTABLE", "VAR_SINNOH_VEILSTONE_GUARDAS_DUELAVEIS", 0x415E),
    ("VAR_VERITY_LAKEFRONT_STATE", "VAR_SINNOH_VERITY_BEIRA_ESTADO", 0x415F),
    ("VAR_VILLA_STATE", "VAR_SINNOH_VILLA_ESTADO", 0x41C2),
]
ALIAS_DA_VAR = {f: a for f, a, _ in VARS}
ENDERECO_DA_VAR = {f: e for f, _, e in VARS}

# LEVA de cada var, transcrita da seção "Plano de blocos executáveis" do plano
# (S3 a S7). É o `<leva>` do comentário `@ TODO S<leva>` do esqueleto.
LEVA = {}
for _leva, _vs in {
    "S3": """VAR_TWINLEAF_TOWN_GUITARIST_TRIGGER_STATE VAR_TWINLEAF_TOWN_RIVAL_TRIGGER_STATE
             VAR_PLAYER_HOUSE_STATE VAR_PLAYER_HOUSE_RIVAL_STATE VAR_VERITY_LAKEFRONT_STATE
             VAR_SANDGEM_TOWN_STATE VAR_ROUTE_202_STATE""",
    "S4": """VAR_JUBILIFE_CITY_STATE VAR_JUBILIFE_LOOKER_PAL_PAD_STATE VAR_OREBURGH_CITY_STATE
             VAR_OREBURGH_GATE_1F_HIKER_STATE VAR_ROUTE_203_RIVAL_STATE
             VAR_ROUTE_207_COUNTERPART_TRIGGER_STATE VAR_ETERNA_CITY_STATE
             VAR_ETERNA_CITY_BLOCK_EXITS_STATE VAR_VALLEY_WINDWORKS_STATE
             VAR_VALLEY_WINDWORKS_TEAM_GALACTIC_STATE""",
    "S5": """VAR_HEARTHOME_CITY_STATE VAR_ROUTE_209_GATE_TO_HEARTHOME_CITY_STATE
             VAR_SOLACEON_TOWN_STATE VAR_VEILSTONE_CITY_CRASHER_WAKE_STATE
             VAR_VEILSTONE_CITY_GALACTIC_WAREHOUSE_STATE
             VAR_VEILSTONE_WAREHOUSE_GUARDS_FIGHTABLE VAR_PASTORIA_CITY_STATE
             VAR_PASTORIA_CITY_CROAGUNK_SCENE_STATE VAR_PASTORIA_CITY_OBSERVATORY_GATE_1F_STATE
             VAR_CELESTIC_TOWN_ELDER_STATE""",
    "S6": """VAR_GALACTIC_HQ_4F_STATE VAR_GALACTIC_HQ_CONTROL_ROOM_STATE VAR_GALACTIC_HQ_HALL_STATE
             VAR_MT_CORONET_1F_SOUTH_STATE VAR_MT_CORONET_2F_STATE VAR_ACUITY_LAKEFRONT_STATE
             VAR_SNOWPOINT_CITY_STATE VAR_ROUTE_217_STATE VAR_SPEAR_PILLAR_STATE
             VAR_HALL_OF_ORIGIN_STATE VAR_CANALAVE_CITY_STATE
             VAR_ROUTE_218_GATE_TO_CANALAVE_CITY_STATE""",
    "S7": """VAR_SUNYSHORE_CITY_STATE VAR_VALOR_LAKEFRONT_BLOCK_SUNYSHORE_STATE VAR_ROUTE_224_STATE
             VAR_ROUTE_227_BUCK_STATE VAR_ROUTE_227_WAKE_RIVAL_STATE
             VAR_STARK_MOUNTAIN_OUTSIDE_STATE VAR_RESORT_AREA_STATE VAR_VILLA_STATE
             VAR_POKEMON_MANSION_OFFICE_BLOCK_STATUE_STATE VAR_RIVAL_BEAT_SUNYSHORE_GYM""",
}.items():
    for _v in _vs.split():
        if _v in ALIAS_DA_VAR:
            LEVA[_v] = _leva

# Vars da fonte que NÃO viram alias nem gatilho: decisões 3 (descarte por
# mecânica inexistente), 4 (Amity vira warp comum) e 5 (acompanhantes adiados).
FORA_DE_ESCOPO = {
    "VAR_GTS_ACCESS_STATE": "decisao 3: GTS nao existe aqui",
    "VAR_POKETCH_CAMPAIGN_STATE": "decisao 3: Poketch nao existe",
    "VAR_PAL_PARK_STATE": "decisao 3: migracao de gen 3 nao existe",
    "VAR_BATTLE_FRONTIER_DUMMY_STATE": "decisao 3: dummy declarado na propria fonte",
    "VAR_FOLLOWER_MON_ACTIVE": "decisao 3: OW_FOLLOWERS_ENABLED e FALSE",
    "VAR_AMITY_SQUARE_STATE": "decisao 4: Amity vira praca aberta, warp comum de onda futura",
    "VAR_FOLLOWER_RIVAL_STATE": "decisao 5: mecanica de parceiro sem desenho",
    "VAR_ETERNA_FOREST_FOLLOWER_CHERYL_STATE": "decisao 5: mecanica de parceiro sem desenho",
    "VAR_IRON_ISLAND_B2F_LEFT_ROOM_FOLLOWER_RILEY_STATE": "decisao 5: mecanica de parceiro sem desenho",
    "VAR_STARK_MOUNTAIN_ROOM_2_FOLLOWER_BUCK_STATE": "decisao 5: mecanica de parceiro sem desenho",
    "VAR_VICTORY_ROAD_1F_ROOM_2_FOLLOWER_MARLEY_STATE": "decisao 5: mecanica de parceiro sem desenho",
    "VAR_WAYWARD_CAVE_1F_FOLLOWER_MIRA_STATE": "decisao 5: mecanica de parceiro sem desenho",
}

# Decisão 6: mecânica diária / Mystery Gift, fora do orçamento de flags.
POKECENTER_MART = re.compile(
    r"POKECENTER_DAILY_TRAINER|MART_MYSTERY_GIFT_DELIVERYMAN")

# Os 8 mapas que o bloco S2 está editando nesta mesma onda.
COLISAO_ONDA = {
    "EternaCity", "GalacticHQ_2F", "GalacticHQ_3F", "GalacticHQ_B2F",
    "MtCoronet1FTunnelRoom", "SpearPillar", "TeamGalacticEternaBuilding_3F",
    "VeilstoneCity",
}

# Flags de infraestrutura: existem em objeto de Sinnoh mas não são cena de
# grupo nenhum (NPC duplicado, Wi-Fi de Pokécenter, escolha de inicial).
# Nunca servem de candidato a reuso.
FLAGS_INFRA = {"FLAG_SINNOH_NPC_DUPLICADO", "FLAG_SINNOH_WIFI_ESCONDIDO",
               "FLAG_INICIAL_SINNOH"}

# Faixa desta obra em flags.h. 0x190B-0x19FF (a do plano) foi INTEIRA para a
# consolidação de Kanto em 17/08/2026; 0x1A00-0x1AFF é reserva de Unova. Este
# é o transbordo que o próprio plano apontava.
FLAG_BASE = 0x1B00
FLAG_TETO = 0x1BFF

ABRE_V = "// >>> B6 Sinnoh, as 49 vars da maquina de cenas (dev_scripts/maquina_sinnoh.py) >>>"
FECHA_V = "// <<< B6 Sinnoh, as 49 vars da maquina de cenas <<<"
ABRE_F = "// >>> B6 Sinnoh, flags dos grupos de hidden_flag (dev_scripts/maquina_sinnoh.py) >>>"
FECHA_F = "// <<< B6 Sinnoh, flags dos grupos de hidden_flag <<<"
ABRE_I = "@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>"
FECHA_I = "@ <<< B6 Sinnoh S1: esqueletos de cena <<<"


# ------------------------------------------------------------------ leitura

def texto(p):
    return open(p, encoding="utf-8").read()


def defines(caminho, prefixo):
    """`{nome: alvo}` de todo `#define <prefixo>X <alvo>` do arquivo."""
    return {m.group(1): m.group(2) for m in re.finditer(
        rf"^#define\s+({prefixo}\w+)\s+(\S+)", texto(caminho), re.M)}


def pool_livre(caminho, prefixo):
    """Endereços do pool `<prefixo>UNUSED_0xNNN` que NÃO têm apelido apontando
    para eles, nem uso cru em data/ ou src/. Mesma régua de flags_livres.py:
    contar `UNUSED` conta o pool inteiro, ocupadas junto."""
    d = defines(caminho, prefixo)
    existe = {int(n, 16) for n in re.findall(
        rf"^#define\s+{prefixo}UNUSED_0x([0-9A-Fa-f]+)\s", texto(caminho), re.M)}
    apelidada = {int(m, 16) for alvo in d.values()
                 for m in re.findall(rf"^{prefixo}UNUSED_0x([0-9A-Fa-f]+)$", alvo)}
    return existe, apelidada


def fila():
    return json.load(open(os.path.join(REPO, "dev_scripts/fila_b6.json"),
                          encoding="utf-8"))


def entradas_da_fila(tipo):
    """Todas as linhas de Sinnoh daquele tipo, SEM olhar o `status`.

    Era `entradas_pendentes`, e olhava `status == "pendente"`. Isso funcionou
    enquanto a fila era a de 15/08/2026, em que os 164 gatilhos e os 247 grupos
    estavam TODOS pendentes; virou bomba-relógio no dia em que a fila aprendeu
    a marcar `feita`, `descartada` e `adiada` (fechamento de 18/08/2026): o
    censo encolheu de 164 para 56 e o `--demo` ficou vermelho em três contagens
    de uma vez, sem que nada da FONTE tivesse mudado.

    O que esta máquina precisa da fila não é "o que falta fazer", é "quais
    `coord_events` e grupos da fonte existem e casam com mapa importado". Isso
    não muda quando um executor escreve uma cena, e por isso o status sai da
    conta. O que NÃO deve ser portado continua fora por `FORA_DE_ESCOPO` e
    `POKECENTER_MART`, que são as decisões do plano lidas aqui dentro, não por
    efeito colateral do status de outra ferramenta.
    """
    return [e for e in fila() if e["regiao"] == "sinnoh" and e["tipo"] == tipo]


def script_entries(arq_eventos):
    """A lista de `ScriptEntry` do `scripts_<mapa>.s` da fonte, na ordem. O
    índice `script: N` do `coord_event` é 1-based nela (decisão 8)."""
    p = os.path.join(S.PLAT, "res/field/scripts",
                     arq_eventos.replace("events_", "scripts_") + ".s")
    if not os.path.exists(p):
        return []
    return re.findall(r"^\s*ScriptEntry\s+(\w+)\s*$", texto(p), re.M)


def rotulo_curto(entradas, nome):
    """`TwinleafTown_CoordEvent_RivalThud` -> `CoordEvent_RivalThud`.

    Tira só o PRIMEIRO componente, e só quando ele é o mesmo em TODAS as
    entradas do arquivo (é o nome do mapa na fonte). Sem isso o rótulo daqui
    ficaria `TwinleafTown_EventScript_TwinleafTown_CoordEvent_RivalThud`.
    Cortar mais que um componente arriscaria comer `CoordEvent` num arquivo de
    duas entradas, e aí dois rótulos diferentes poderiam virar o mesmo nome.
    """
    cabecas = {e.split("_", 1)[0] for e in entradas}
    if len(cabecas) == 1 and "_" in nome:
        return nome.split("_", 1)[1]
    return nome


def temp_da_local(var):
    """`VAR_MAP_LOCAL_0x0F` -> `VAR_TEMP_F` (decisão 1)."""
    return "VAR_TEMP_" + var.rsplit("_", 1)[1][-1].upper()


# ------------------------------------------------- andabilidade do tile plantado

# Raio máximo, em tiles, da busca por casa andável quando a conversão
# proporcional joga um gatilho em cima de parede. 8 é o tamanho do maior span
# da fonte (Twinleaf, width 8): passar disso deixaria de ser "reposicionamento
# fiel" e viraria invenção de coordenada.
RAIO_REALOCACAO = 8

_MAPBIN = {}


def mapbin(layout):
    """`(bytes, largura, altura)` do `map.bin` do layout, lido uma vez só."""
    if layout["id"] not in _MAPBIN:
        _MAPBIN[layout["id"]] = (
            open(os.path.join(REPO, layout["blockdata_filepath"]), "rb").read(),
            layout["width"], layout["height"])
    return _MAPBIN[layout["id"]]


def andavel(layout, x, y):
    """O tile (x, y) do layout é pisável?

    Bits 10-11 do `map.bin` são `MAPGRID_COLLISION_MASK`
    (`include/global.fieldmap.h`), zero = passa. Mesma leitura de
    `dev_scripts/changeblock_gen2.py` e `gatilhos_setscene_unova.py`. Fora do
    layout também é "não andável": gatilho fora do mapa é gatilho morto.
    """
    b, w, h = mapbin(layout)
    if not (0 <= x < w and 0 <= y < h):
        return False
    return ((struct.unpack_from("<H", b, (y * w + x) * 2)[0] >> 10) & 3) == 0


def tiles_bloqueados(d):
    """Tiles do `map.json` onde um gatilho é inútil mesmo sendo andável:

    - casa de `warp_events`: pisar nela troca de mapa ANTES de a cena rodar
      (foi o defeito do rival de Oreburgh, em cima da porta do portão);
    - casa de `object_events` SEM flag de esconder (`flag` = "0"): o NPC está
      sempre ali, o jogador nunca pisa no tile. Objeto COM flag não entra:
      ele pode estar removido na hora da cena, e bloquear por causa dele
      moveria gatilho que funciona.
    """
    fora = {(int(w.get("x", 0)), int(w.get("y", 0)))
            for w in (d.get("warp_events") or [])}
    fora |= {(int(o.get("x", 0)), int(o.get("y", 0)))
             for o in (d.get("object_events") or [])
             if str(o.get("flag", "0")) == "0"}
    return fora


def realoca_tiles(layout, d, pts, width, length):
    """Move para casa andável cada tile plantado que caiu em parede.

    Régua (decisão do plano, item de QA de 17/08/2026): o tile anda pela
    LINHA ou pela COLUNA dele, nunca na diagonal, e o eixo do span da fonte é
    tentado primeiro (span horizontal procura primeiro na linha, vertical
    primeiro na coluna). Distância crescente, e a cada distância o sentido
    negativo antes do positivo, para a saída não depender da ordem de leitura.
    Não pode cair em tile já usado pelo mesmo gatilho, nem em tile bloqueado
    (`tiles_bloqueados`). Sem candidato dentro de `RAIO_REALOCACAO`, o tile é
    REPORTADO e não plantado, em vez de virar gatilho morto em parede.

    Devolve `(tiles_finais, movidos, perdidos)`.
    """
    if width == 1 and length > 1:
        eixos = ("y", "x")
    elif length == 1 and width > 1:
        eixos = ("x", "y")
    else:                                  # 1x1 ou retângulo: sem eixo único
        eixos = ("x", "y")
    bloq = tiles_bloqueados(d)
    ruim = lambda t: (not andavel(layout, *t)) or t in bloq   # noqa: E731

    ocupados = set(pts)
    finais, movidos, perdidos = [], [], []
    for t in pts:
        if not ruim(t):
            finais.append(t)
            continue
        alvo = None
        for dist in range(1, RAIO_REALOCACAO + 1):
            for eixo in eixos:
                for s in (-1, 1):
                    c = ((t[0], t[1] + s * dist) if eixo == "y"
                         else (t[0] + s * dist, t[1]))
                    if c in ocupados or ruim(c):
                        continue
                    alvo = c
                    break
                if alvo:
                    break
            if alvo:
                break
        if alvo is None:
            perdidos.append(list(t))
            continue
        ocupados.add(alvo)
        finais.append(alvo)
        movidos.append([list(t), list(alvo)])
    return sorted(finais), movidos, perdidos


# ------------------------------------------------------------------- censo

def censo():
    """Tudo que esta máquina sabe, sem escrever nada. Estrutura:

    `vars`      um item por var da tabela do plano (todas, com ou sem gatilho);
    `flags`     um item por NOME de flag da fonte que sobrou das decisões 3-6;
    `gatilhos`  um item por `coord_event` da fonte que vira gatilho aqui, já
                com os tiles expandidos e o rótulo do esqueleto;
    `adiados`   um item por `coord_event`/grupo que NÃO entra nesta rodada, com
                o motivo escrito.
    """
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json"),
             encoding="utf-8"))["layouts"]}
    flags_reais = set(re.findall(r"#define\s+(FLAG_\w+)", texto(FLAGS_H)))

    pend_gat = {(e["mapa_destino"], e["id"].split(":")[2], e["id"].split(":")[3])
                for e in entradas_da_fila("coord_event")}
    gatilhos, adiados = [], []
    tiles = collections.defaultdict(list)
    total_fonte = span_bruto = 0

    for meu, header, arq, matriz in F.mapas_casados_sinnoh():
        p = os.path.join(S.PLAT, "res/field/events", arq + ".json")
        if not os.path.exists(p):
            continue
        fonte = json.load(open(p, encoding="utf-8"))
        seus = [c for c in (fonte.get("coord_events") or [])
                if (meu, str(c.get("var")), str(c.get("script"))) in pend_gat]
        if not seus:
            continue
        total_fonte += len(seus)
        entradas = script_entries(arq)
        d = json.load(open(os.path.join(REPO, "data/maps", meu, "map.json"),
                           encoding="utf-8"))
        L = layouts[d["layout"]]
        conv = S.conversor_de_coordenada(fonte, L["width"], L["height"],
                                         header, matriz, d)
        inc = texto(os.path.join(REPO, "data/maps", meu, "scripts.inc"))

        for c in seus:
            v, n = str(c["var"]), int(c["script"])
            base = dict(mapa=meu, var_fonte=v, script_fonte=n,
                        fonte_x=c["x"], fonte_z=c["z"],
                        width=int(c.get("width", 1) or 1),
                        length=int(c.get("length", 1) or 1))
            span_bruto += base["width"] * base["length"]

            if v in FORA_DE_ESCOPO:
                adiados.append(dict(base, motivo=FORA_DE_ESCOPO[v]))
                continue
            if v.startswith("VAR_MAP_LOCAL_"):
                nossa, novo = temp_da_local(v), False
                # A conferência da decisão 1 é contra USO ALHEIO do temp. Se o
                # mapa já tem coord_event NOSSO naquele temp, o que o
                # `scripts.inc` cita é a cena que esta máquina plantou, e ler
                # isso como colisão faria o gerador se auto-envenenar depois da
                # primeira gravação (foi o que tirou Route206_North/South do
                # censo e deixou os gatilhos deles em parede).
                nosso = any(
                    x.get("var") == nossa
                    and str(x.get("script", "")).startswith(meu + "_EventScript_")
                    for x in (d.get("coord_events") or []))
                if not nosso and re.search(rf"\b{nossa}\b", inc):
                    adiados.append(dict(base, motivo=(
                        f"decisao 1: {nossa} ja e usado por outra coisa em "
                        f"{meu}/scripts.inc; volta ao plano")))
                    continue
            elif v in ALIAS_DA_VAR:
                nossa, novo = ALIAS_DA_VAR[v], True
            else:
                adiados.append(dict(base, motivo=(
                    "var da fonte fora da tabela do plano; volta ao plano")))
                continue
            if meu in COLISAO_ONDA:
                adiados.append(dict(base, motivo=(
                    "adiado por colisao de onda: o bloco S2 edita este mapa "
                    "em 17/08/2026")))
                continue
            if not 1 <= n <= len(entradas):
                adiados.append(dict(base, motivo=(
                    f"script {n} fora da lista de ScriptEntry ({len(entradas)} "
                    f"entradas): e indice de script global do narc, sem rotulo "
                    f"na fonte; volta ao plano")))
                continue
            if conv is None:
                adiados.append(dict(base, motivo=(
                    "mapa da fonte sem object/bg_event: nao ha ancora para "
                    "converter coordenada")))
                continue

            pts = sorted({conv({"x": c["x"] + dx, "z": c["z"] + dz})
                          for dx in range(base["width"])
                          for dz in range(base["length"])})
            pts, movidos, perdidos = realoca_tiles(
                L, d, pts, base["width"], base["length"])
            rot = rotulo_curto(entradas, entradas[n - 1])
            if not pts:
                adiados.append(dict(base, motivo=(
                    f"todos os {len(perdidos)} tiles convertidos caem em "
                    f"parede/warp e nao ha casa andavel na linha nem na coluna "
                    f"dentro de {RAIO_REALOCACAO} tiles; volta ao plano"),
                    tiles_perdidos=perdidos))
                continue
            item = dict(base, var=nossa, var_alias=novo,
                        var_value=str(c.get("value", 0)),
                        rotulo_fonte=entradas[n - 1],
                        script=f"{meu}_EventScript_{rot}",
                        leva=LEVA.get(v, "S?"), tiles=[list(t) for t in pts],
                        tiles_movidos=movidos, tiles_perdidos=perdidos)
            gatilhos.append(item)
            for t in pts:
                tiles[(meu, t)].append(item["script"])

    empilhados = [dict(mapa=m, x=t[0], y=t[1], scripts=sorted(set(ss)))
                  for (m, t), ss in sorted(tiles.items()) if len(ss) > 1]

    return dict(medido_em=MEDIDO_EM,
                vars=censo_vars(),
                flags=censo_flags(flags_reais),
                gatilhos=gatilhos, adiados=adiados,
                tiles_empilhados=empilhados,
                resumo=dict(coord_events_da_fonte=total_fonte,
                            span_bruto=span_bruto,
                            tiles_plantados=sum(len(g["tiles"]) for g in gatilhos),
                            tiles_movidos=sum(len(g["tiles_movidos"]) for g in gatilhos),
                            tiles_perdidos=sum(len(g["tiles_perdidos"]) for g in gatilhos),
                            gatilhos=len(gatilhos), adiados=len(adiados),
                            mapas_com_gatilho=len({g["mapa"] for g in gatilhos})))


def censo_vars():
    peso = collections.Counter(e["id"].split(":")[2]
                               for e in entradas_da_fila("coord_event"))
    return [dict(fonte=f, alias=a, endereco=f"0x{e:04X}",
                 leva=LEVA.get(f, "?"), gatilhos_na_fila=peso.get(f, 0))
            for f, a, e in VARS]


def alias_ja_gravados():
    """`FLAG_HIDE_* da fonte -> (alias daqui, endereco)` já dentro de flags.h.

    Existe porque ENDEREÇO DE FLAG GRAVADA É HISTÓRIA, não resultado de conta.
    A alocação desta máquina saía inteira da fila, e a fila mexe: no fechamento
    de 18/08/2026 ela aprendeu `feita`/`descartada`/`adiada`, o conjunto de
    entrada mudou, e um `--gravar` inocente teria REESCRITO o bloco de flags de
    Sinnoh com endereços diferentes, embaixo das dezenas de cenas que já citam
    esses apelidos por nome. O `--demo` só pegou isso porque a contagem também
    mudou; sem esta trava, o próximo executor teria descoberto pelo jogo.

    A partir daqui: nome da fonte que já saiu gravado uma vez fica com o alias
    e o endereço que ele tem, aconteça o que acontecer com a fila. Nome NOVO
    (fonte nova, mapa importado depois) entra em append, depois do maior
    endereço já usado, e é só isso que o gerador ainda decide.
    """
    t = texto(FLAGS_H)
    if ABRE_F not in t:
        return {}
    bloco = t[t.index(ABRE_F):t.index(FECHA_F)]
    return {fonte: (alias, ender) for alias, ender, fonte in re.findall(
        r"#define\s+(FLAG_SINNOH_ESCONDE_\w+)\s+FLAG_UNUSED_(0x[0-9A-Fa-f]{4})"
        r"\s*//\s*(FLAG_HIDE_\w+)", bloco)}


def censo_flags(flags_reais):
    """Um item por NOME de `FLAG_HIDE_*` da fonte que sobrou das decisões 3-6.

    A unidade é o NOME, não o par (mapa, nome): a mesma flag da fonte aparece
    em até 5 mapas (`FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC`), e na fonte ela é
    UMA flag só. Endereço sequencial a partir de FLAG_BASE, em ordem alfabética
    do nome da fonte, para a alocação não depender da ordem de varredura.
    """
    grupos = collections.defaultdict(list)
    for e in entradas_da_fila("hidden_flag"):
        nome = e["id"].split(":", 1)[1]
        grupos[nome].append(e)
    ja_alocado = alias_ja_gravados()

    # candidato a reuso: nos grupos que a fila deu como "sem bloqueio" (ela já
    # provou que existe cena), a flag que o objeto plantado carrega.
    por_mapa = {}
    saida, alocado, reivindicada = [], FLAG_BASE, {}
    # Endereço novo entra DEPOIS do maior já apelidado na faixa desta obra, e a
    # varredura é o arquivo inteiro, não só o bloco gerado: as flags que a
    # condutora autorizou à mão (0x1B9D a 0x1BA0, a corrente da bomba de
    # Pastoria) moram FORA do bloco, e alocar por cima delas seria dar o mesmo
    # bit para duas coisas.
    usados = [int(e, 16) for e in re.findall(
        r"#define\s+FLAG_\w+\s+FLAG_UNUSED_(0x[0-9A-Fa-f]{4})", texto(FLAGS_H))]
    usados = [e for e in usados if FLAG_BASE <= e <= FLAG_TETO]
    if usados:
        alocado = max(usados) + 1
    for nome in sorted(grupos):
        gs = grupos[nome]
        mapas = sorted({g["mapa_destino"] for g in gs})
        # HISTÓRIA MANDA. Nome da fonte que JÁ tem alias gravado em flags.h
        # mantém alias e endereço, e nem passa pela classificação. Ver
        # `alias_ja_gravados`: reclassificar isso reescreveria endereço de
        # flag que dezenas de cenas já citam.
        if nome in ja_alocado:
            flag, ender = ja_alocado[nome]
            saida.append(dict(fonte=nome, mapas=mapas, estado="nova",
                              flag=flag, endereco=ender))
            continue
        # Grupo sem nenhuma linha PENDENTE na fila e sem alias gravado é grupo
        # que já está no mapa carregando flag própria (ou que a fila descartou
        # / adiou por decisão datada). Não é trabalho desta máquina, e alocar
        # flag para ele gastaria endereço que nenhuma cena vai citar.
        if not any(g["status"] == "pendente" for g in gs):
            saida.append(dict(fonte=nome, mapas=mapas, estado="fora",
                              motivo=("nenhuma linha pendente na fila e nenhum "
                                      "alias gravado: feito, descartado ou "
                                      "adiado por decisao datada")))
            continue
        if nome.startswith("MAP_HEADER_"):
            saida.append(dict(fonte=nome, mapas=mapas, estado="clone",
                              motivo=("objeto clone da fonte: o campo "
                                      "hidden_flag guarda o MAP_HEADER de "
                                      "origem, nao e flag")))
            continue
        if POKECENTER_MART.search(nome):
            saida.append(dict(fonte=nome, mapas=mapas, estado="adiado",
                              motivo=("decisao 6: mecanica diaria/Mystery "
                                      "Gift, nao e cena de historia")))
            continue
        if nome in flags_reais:
            saida.append(dict(fonte=nome, mapas=mapas, estado="reusada",
                              flag=nome, prova="nome identico ja em flags.h"))
            continue
        cands = set()
        for g in gs:
            if g["bloqueio"] != "nenhum":
                continue
            m = g["mapa_destino"]
            if m not in por_mapa:
                d = json.load(open(os.path.join(REPO, "data/maps", m, "map.json"),
                                   encoding="utf-8"))
                por_mapa[m] = {str(o.get("flag", "0"))
                               for o in (d.get("object_events") or [])}
            cands |= {f for f in por_mapa[m]
                      if f in flags_reais and f not in FLAGS_INFRA}
        livres = cands - set(reivindicada)
        if len(cands) > 1 or (cands and not livres):
            saida.append(dict(
                fonte=nome, mapas=mapas, estado="ambiguo",
                candidatos=sorted(cands),
                motivo=("decisao 9: reuso com mais de um candidato, ou "
                        "candidato ja reivindicado por outro grupo da fonte; "
                        "fusao e decisao de condutora, nao do gerador")))
            continue
        if len(livres) == 1:
            f = livres.pop()
            reivindicada[f] = nome
            saida.append(dict(fonte=nome, mapas=mapas, estado="reusada", flag=f,
                              prova=("a fila deu o grupo como sem bloqueio e o "
                                     "objeto ja plantado carrega esta flag")))
            continue
        saida.append(dict(fonte=nome, mapas=mapas, estado="nova",
                          flag="FLAG_SINNOH_ESCONDE_"
                               + nome[len("FLAG_HIDE_"):],
                          endereco=f"0x{alocado:04X}"))
        alocado += 1
    if alocado - 1 > FLAG_TETO:
        raise SystemExit(f"faixa 0x{FLAG_BASE:04X}-0x{FLAG_TETO:04X} estourou "
                         f"em 0x{alocado:04X}: volte ao plano antes de gravar")
    return saida


# ------------------------------------------------------------------ escrita

def troca_bloco(caminho, abre, fecha, corpo):
    """Escreve o bloco entre as marcas, criando no fim do arquivo se não houver.
    Idempotente de propósito: rodar duas vezes tem que dar o mesmo arquivo."""
    t = texto(caminho)
    novo = f"{abre}\n{corpo}{fecha}\n"
    if abre in t:
        i, j = t.index(abre), t.index(fecha) + len(fecha) + 1
        t = t[:i] + novo + t[j:]
    else:
        t = t.rstrip("\n") + "\n\n" + novo
    open(caminho, "w", encoding="utf-8").write(t)


def grava_vars(c):
    corpo = (
        "// Faixa exclusiva desta frente, transcrita de PLANO-OBRAS-SINNOH.md:\n"
        "// VAR_UNUSED_0x4130 a 0x415F (o gap de 48) mais o transbordo\n"
        "// VAR_UNUSED_0x41C2. Alias 1:1 da var do Platinum, e os VALORES são os\n"
        "// da fonte, número a número (decisão 2 do plano). Apelidar var\n"
        "// existente não mexe em VARS_COUNT, ou seja, não invalida save.\n"
        "// Var interna de cena que aparecer no porte NÃO ganha endereço de\n"
        "// executor: volta ao plano, e o endereço sai do MAPA DE DONOS escrito\n"
        "// em include/constants/vars.h, medido antes com\n"
        "// `python3 dev_scripts/guarda_colisao_vars.py`. Esta linha já apontou\n"
        "// um número cravado (\"append em 0x41C3+\") e ele apodreceu no mesmo\n"
        "// dia: em 18/08/2026 o bloco J6 da janela aberta mudou as 19 vars de\n"
        "// cena de Kanto justamente para 0x41C3-0x41D5. Endereço livre é o que\n"
        "// a medição diz agora, nunca o que um comentário lembra.\n")
    larg = max(len(a) for _, a, _ in VARS) + 1
    for f, a, e in VARS:
        corpo += (f"#define {a:<{larg}} VAR_UNUSED_0x{e:04X}"
                  f"  // {f}, leva {LEVA.get(f, '?')}\n")
    troca_bloco(VARS_H, ABRE_V, FECHA_V, corpo)
    return len(VARS)


def grava_flags(c):
    novas = [f for f in c["flags"] if f["estado"] == "nova"]
    corpo = (
        f"// DONO DA FAIXA 0x{FLAG_BASE:04X} a 0x{FLAG_TETO:04X}: a obra de Sinnoh\n"
        f"// (PLANO-OBRAS-SINNOH.md, bloco S1). Uma flag por grupo de\n"
        f"// hidden_flag da fonte, nome mecânico da decisão 9.\n"
        f"//\n"
        f"// Por que NÃO é a faixa 0x190B-0x19FF que o plano reservou: em\n"
        f"// 17/08/2026 a consolidação de Kanto (652776174a) apelidou os 245\n"
        f"// endereços dela e seguiu até 0x1A4B (medido por\n"
        f"// dev_scripts/flags_livres.py). 0x1A00-0x1AFF é reserva de Unova,\n"
        f"// então esta obra desce para o transbordo 0x1B00+, que o próprio\n"
        f"// plano já apontava. Cabeça livre depois daqui: NÃO se lê deste\n"
        f"// comentário, mede-se com `python3 dev_scripts/flags_livres.py`. A\n"
        f"// frase que ficava aqui dizia \"até 0x2025\" e envelheceu em\n"
        f"// 18/08/2026, quando o bloco J1 da janela aberta subiu FLAGS_COUNT\n"
        f"// e loteou 0x2031 em diante entre item balls e reserva.\n")
    if novas:
        larg = max(len(f["flag"]) for f in novas) + 1
        for f in novas:
            corpo += (f"#define {f['flag']:<{larg}} "
                      f"FLAG_UNUSED_{f['endereco'].replace('0x', '0x')}"
                      f"  // {f['fonte']}\n")
    troca_bloco(FLAGS_H, ABRE_F, FECHA_F, corpo)
    return len(novas)


# --------------------------------------------------------- gatilhos da leva

# Gatilhos cujo `coord_event` no `map.json` pertence à LEVA que escreveu a
# cena, e não a esta máquina. Ela não planta, não move e não apaga nenhum
# deles. Cada linha tem decisão ESCRITA no `scripts.inc` do próprio mapa, e
# sem esta tabela um `--gravar` posterior desfazia calado o que a leva
# decidiu (medido em 18/08/2026 pelo S8: 8 `coord_events` ressuscitados).
#
# Duas formas de entrar aqui:
# (a) a leva REMOVEU o gatilho porque ele apontava para um rótulo morto (a
#     cena equivalente já existe por clique/raio de visão, e o gatilho
#     duplicaria a batalha ou custaria var só para lembrar que já rodou);
# (b) a leva ESCOLHEU os tiles à mão contra o `map.bin`, e a conta
#     proporcional desta máquina escolhe outros.
LEVA_DONA = {
    # (a), onda 4 (commit cfdb819d30), "três falso-gatilhos removidos com
    # prova de cena equivalente já existente":
    ("CanalaveCity", "CanalaveCity_EventScript_CoordEvent_Rival"):
        "duplicaria a batalha de CanalaveCity_EventScript_Rival (raio de visao)",
    ("GalacticHQ_Hall", "GalacticHQ_Hall_EventScript_CoordEvent_Speech"):
        "discurso roda por dialogo replay-avel do Cyrus/Looker, sem var",
    ("MtCoronet_1F_South", "MtCoronet_1F_South_EventScript_CoordEvent_Cyrus"):
        "monologo ja portado no clique do Cyrus, sem var",
    # (b), onda 5 (commit a7e7120d41 + PLANO-OBRAS-SINNOH.md, "Valor
    # Lakefront: o bloqueio do Collector fecha UMA das duas saidas"): o span
    # de 3 foi posto na seccao inteira da estrada sul, (45,57)/(45,58)/(45,59),
    # medido em busca em largura sobre LAYOUT_VALOR_LAKEFRONT.
    ("ValorLakefront", "ValorLakefront_EventScript_CoordEvent_BlockSunyshore"):
        "tiles escolhidos a mao no map.bin, span de 3 na estrada sul",
}


def plano_de_reparo(gs, d, layout):
    """De-para dos `coord_events` JÁ gravados que precisam mudar de tile.

    Duas origens de tile ruim, e as duas saem daqui:

    1. o tile que ESTE censo acabou de realocar (`tiles_movidos`) ou de perder
       (`tiles_perdidos`). Casa pela posição ORIGINAL da fonte, que é a que
       `realoca_tiles` conhece;
    2. tile que uma rodada ANTERIOR gravou e que hoje é ruim sem bater com
       nenhuma das duas listas acima. Isso acontece quando o mapa muda embaixo
       do gatilho: o caso medido em 18/08/2026 é o Buck da Route227, gravado
       em (30,19) por uma rodada em que aquele tile ainda estava livre, e
       depois coberto pelo `object_event` do próprio Buck (objeto sem flag de
       esconder entra em `tiles_bloqueados`). A posição velha não está em
       `tiles_movidos` (que hoje diz (33,19) -> (29,19)), então o casamento
       aqui é por SCRIPT: o gatilho vai para um tile que o censo de HOJE
       escolheu e que ainda não está ocupado por outro gatilho do mesmo
       script. Sem alvo livre, ele é apagado, que é o mesmo destino de um
       tile perdido: gatilho em parede nunca dispara.

    Tile gravado que está ANDÁVEL não entra em nenhum dos dois caminhos, e é
    isso que preserva o que a leva mexeu à mão (o des-empilhamento de
    `TwinleafTown_MainHouse_2F`, por exemplo).

    Devolve `(mover, apagar)`: `mover` é `{(script, (x, y)): (x, y)}` e
    `apagar` é um conjunto de `(script, (x, y))`.
    """
    gs = [g for g in gs if (g["mapa"], g["script"]) not in LEVA_DONA]
    bloq = tiles_bloqueados(d)
    ruim = lambda t: (not andavel(layout, *t)) or t in bloq   # noqa: E731
    mover = {(g["script"], tuple(a)): tuple(b)
             for g in gs for a, b in g["tiles_movidos"]}
    apagar = {(g["script"], tuple(t))
              for g in gs for t in g["tiles_perdidos"]}
    alvos = {g["script"]: [tuple(t) for t in g["tiles"]] for g in gs}
    gravados = collections.defaultdict(list)
    for ce in (d.get("coord_events") or []):
        if ce.get("script") in alvos:
            gravados[ce["script"]].append(
                (int(ce.get("x", 0)), int(ce.get("y", 0))))
    for s, pts in sorted(gravados.items()):
        livres = [t for t in alvos[s] if t not in pts]
        for t in pts:
            if (s, t) in mover or (s, t) in apagar or not ruim(t):
                continue
            if livres:
                mover[(s, t)] = livres.pop(0)
            else:
                apagar.add((s, t))
    return mover, apagar


def grava_mapas(c):
    """Planta os `coord_events` e os esqueletos, um mapa por vez.

    Preserva o que já existe: um tile só recebe gatilho se o mapa ainda não
    tiver `coord_event` com a MESMA var naquele (x, y). Coordenada sozinha não
    serve de identidade aqui como serviu em Unova, porque a conversao de Sinnoh
    e proporcional e dois gatilhos de vars diferentes podem cair no mesmo tile.

    A CORREÇÃO DE ANDABILIDADE alcança o que já está gravado: gatilho nosso que
    hoje mora em parede/warp é MOVIDO para o destino que `realoca_tiles`
    calculou, e o que ficou sem destino é APAGADO (tile de parede nunca vai
    disparar). Quem decide isso é `plano_de_reparo`, que também alcança o tile
    gravado por rodada ANTERIOR cuja posição velha não está no censo de hoje.
    Tile andável que a leva mexeu à mão não é tocado: ele não entra no plano,
    e é isso que preserva o des-empilhamento de `TwinleafTown_MainHouse_2F`
    que a condutora mandou fazer.
    """
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json"),
             encoding="utf-8"))["layouts"]}
    por_mapa = collections.defaultdict(list)
    for g in c["gatilhos"]:
        por_mapa[g["mapa"]].append(g)
    n_ce = n_esq = n_mov = n_del = 0
    for meu, gs in sorted(por_mapa.items()):
        pj = os.path.join(REPO, "data/maps", meu, "map.json")
        d = json.load(open(pj, encoding="utf-8"))

        de_para, morto = plano_de_reparo(gs, d, layouts[d["layout"]])
        vivos, mexeu = [], False
        for ce in (d.get("coord_events") or []):
            chave = (ce.get("script"),
                     (int(ce.get("x", 0)), int(ce.get("y", 0))))
            if chave in morto:
                mexeu, n_del = True, n_del + 1
                continue
            if chave in de_para:
                ce["x"], ce["y"] = de_para[chave]
                mexeu, n_mov = True, n_mov + 1
            vivos.append(ce)
        if mexeu:
            d["coord_events"] = vivos

        ja = {(int(x.get("x", 0)), int(x.get("y", 0)), x.get("var"))
              for x in (d.get("coord_events") or [])}
        novos = []
        for g in gs:
            if (g["mapa"], g["script"]) in LEVA_DONA:
                continue
            for x, y in g["tiles"]:
                if (x, y, g["var"]) in ja:
                    continue
                ja.add((x, y, g["var"]))
                novos.append({"type": "trigger", "x": x, "y": y,
                              "elevation": 0, "var": g["var"],
                              "var_value": g["var_value"],
                              "script": g["script"]})
        if novos or mexeu:
            d.setdefault("coord_events", []).extend(novos)
            with open(pj, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2)
                f.write("\n")
            n_ce += len(novos)

        pi = os.path.join(REPO, "data/maps", meu, "scripts.inc")
        t = texto(pi)
        tem = set(re.findall(r"^(\w+)::", t, re.M))
        faltam = {}
        for g in gs:
            if g["script"] not in tem:
                faltam[g["script"]] = (g["leva"], g["rotulo_fonte"])
        if not faltam:
            continue
        blocos = "".join(
            f"{s}::\n\t@ TODO {leva}: cena da fonte, rotulo {rot}\n\tend\n\n"
            for s, (leva, rot) in sorted(faltam.items()))
        if ABRE_I in t:
            t = t.replace(FECHA_I, blocos + FECHA_I, 1)
        else:
            gancho = re.search(rf"^{re.escape(meu)}_MapScripts::\n(?:.*\n)*?\t\.byte 0\n",
                               t, re.M)
            if not gancho:
                raise SystemExit(f"{meu}: nao achei `{meu}_MapScripts::` em {pi}")
            i = gancho.end()
            t = t[:i] + f"\n{ABRE_I}\n{blocos}{FECHA_I}\n" + t[i:]
        open(pi, "w", encoding="utf-8").write(t)
        n_esq += len(faltam)
    return n_ce, n_esq, len(por_mapa), n_mov, n_del


# ------------------------------------------------------------------ autoteste

def demo():
    """Autoteste OBRIGATÓRIO antes de qualquer `--gravar`, e válido também
    DEPOIS: as contagens da FONTE e as provas de indexação não mudam de estado;
    as de pendência mudam, e por isso são conferidas contra o censo, não contra
    um número fixo de "quanto falta"."""
    # 1. a fila continua descrevendo os 164 gatilhos e os 247 grupos que o
    # plano mediu (os 247 do plano eram os PENDENTES de 15/08; 276 é o
    # total, que é o que não muda). É contagem da FONTE, não de pendência: ver
    # `entradas_da_fila`, que foi o que quebrou no fechamento de 18/08.
    pend = entradas_da_fila("coord_event")
    assert len(pend) == 164, f"gatilhos de Sinnoh na fila: {len(pend)} (esperado 164)"
    hid = entradas_da_fila("hidden_flag")
    assert len(hid) == 276, f"grupos de hidden_flag na fila: {len(hid)} (esperado 276)"

    # 2. decisão 8: ScriptEntry é 1-based, provado nos dois mapas do plano
    am = script_entries("events_amity_square")
    assert len(am) == 45, f"ScriptEntry em Amity: {len(am)} (esperado 45)"
    for i in range(27):
        esperado = f"AmitySquare_Warp{i + 1}"
        assert am[18 + i - 1] == esperado, \
            f"Amity script {18 + i} deu {am[18 + i - 1]}, esperado {esperado}"
    tw = script_entries("events_twinleaf_town")
    assert tw[2 - 1] == "TwinleafTown_CoordEvent_RivalThud", tw[:4]
    assert tw[4 - 1] == "TwinleafTown_CoordEvent_RivalWasLookingForYou", tw[:5]
    # e o corte de prefixo não pode comer o rótulo
    assert rotulo_curto(tw, tw[1]) == "CoordEvent_RivalThud"

    c = censo()

    # 3. colisão zero de endereço contra vars.h/flags.h ATUAIS
    v_existe, v_apelidada = pool_livre(VARS_H, "VAR_")
    alias_v = defines(VARS_H, "VAR_")
    meus_v = {v["alias"] for v in c["vars"]}
    for v in c["vars"]:
        e = int(v["endereco"], 16)
        assert e in v_existe, f"{v['alias']}: VAR_UNUSED_{v['endereco']} nao existe"
        assert e not in v_apelidada or v["alias"] in alias_v, \
            f"{v['alias']}: VAR_UNUSED_{v['endereco']} ja tem outro dono"
        assert v["alias"] not in alias_v or alias_v[v["alias"]] == \
            f"VAR_UNUSED_{v['endereco']}", f"{v['alias']} ja existe com outro valor"
    assert len(meus_v) == len(c["vars"]) == 49, "alias de var repetido ou faltando"

    f_existe, f_apelidada = pool_livre(FLAGS_H, "FLAG_")
    alias_f = defines(FLAGS_H, "FLAG_")
    cruas = set()
    for raiz in ("data", "src"):
        for dirpath, _, nomes in os.walk(os.path.join(REPO, raiz)):
            for n in nomes:
                if n.endswith((".json", ".inc", ".c", ".h", ".s")):
                    cruas |= {int(m, 16) for m in re.findall(
                        r"FLAG_UNUSED_0x([0-9A-Fa-f]+)",
                        texto(os.path.join(dirpath, n)))}
    novas = [f for f in c["flags"] if f["estado"] == "nova"]
    vistos = set()
    for f in novas:
        e = int(f["endereco"], 16)
        assert e in f_existe, f"{f['flag']}: FLAG_UNUSED_{f['endereco']} nao existe"
        assert e not in f_apelidada or alias_f.get(f["flag"]) == \
            f"FLAG_UNUSED_{f['endereco']}", \
            f"{f['flag']}: FLAG_UNUSED_{f['endereco']} ja tem outro dono"
        assert e not in cruas, \
            f"{f['flag']}: FLAG_UNUSED_{f['endereco']} tem uso cru em data/ ou src/"
        assert e not in vistos, f"endereco {f['endereco']} alocado duas vezes"
        vistos.add(e)
        assert FLAG_BASE <= e <= FLAG_TETO, f"{f['flag']} fora da faixa desta obra"
    assert len({f["flag"] for f in novas}) == len(novas), "nome de flag repetido"

    # 4. expansão de span: o total de tiles bate com a soma dos spans, menos o
    # que a conversão de coordenada colapsa, e NUNCA é menor que o número de
    # gatilhos (um gatilho sem tile seria gatilho mudo).
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json"),
             encoding="utf-8"))["layouts"]}
    for g in c["gatilhos"]:
        assert 1 <= len(g["tiles"]) <= g["width"] * g["length"], g
        assert len({tuple(t) for t in g["tiles"]}) == len(g["tiles"]), \
            f"{g['script']}: tile repetido dentro do proprio span"
    r = c["resumo"]
    assert r["coord_events_da_fonte"] == 177, \
        f"coord_events pendentes lidos da fonte: {r['coord_events_da_fonte']} (esperado 177)"
    assert r["span_bruto"] == 360, f"soma dos spans: {r['span_bruto']} (esperado 360)"
    assert r["gatilhos"] + r["adiados"] == r["coord_events_da_fonte"], \
        "gatilho perdido entre plantado e adiado"
    assert r["tiles_plantados"] >= r["gatilhos"], "gatilho sem tile"

    # 5. sobre o estado GRAVADO: todo script citado num coord_event nosso tem
    # rótulo de verdade no scripts.inc, e todo alias que já foi gravado
    # aponta para o endereço da tabela.
    conferidos = andados = 0
    pendentes = []
    for meu in sorted({g["mapa"] for g in c["gatilhos"]}):
        d = json.load(open(os.path.join(REPO, "data/maps", meu, "map.json"),
                           encoding="utf-8"))
        L = layouts[d["layout"]]
        bloq = tiles_bloqueados(d)
        rot = set(re.findall(r"^(\w+)::", texto(
            os.path.join(REPO, "data/maps", meu, "scripts.inc")), re.M))
        nossos = {g["script"] for g in c["gatilhos"] if g["mapa"] == meu}
        # 6. andabilidade: nenhum tile deste censo, nem nenhum coord_event
        # nosso JÁ gravado, pode estar em parede, fora do layout ou em cima de
        # warp/NPC fixo. É a checagem que o plano pediu ao QA em 17/08/2026.
        for g in c["gatilhos"]:
            if g["mapa"] != meu:
                continue
            for t in g["tiles"]:
                assert andavel(L, *t) and tuple(t) not in bloq, \
                    f"{meu}: {g['script']} plantaria em ({t[0]},{t[1]}), inandavel"
                andados += 1
        # O que --gravar já sabe consertar não reprova o autoteste: é reparo
        # PENDENTE, e sai listado. Tile ruim que o gerador NÃO explica é
        # invariante quebrada, e aí sim para.
        mover, apagar = plano_de_reparo(
            [g for g in c["gatilhos"] if g["mapa"] == meu], d, L)
        sabe_consertar = set(mover) | apagar
        for ce in (d.get("coord_events") or []):
            if ce.get("script") in nossos:
                assert ce["script"] in rot, \
                    f"{meu}: {ce['script']} em coord_event e sem rotulo em scripts.inc"
                x, y = int(ce.get("x", 0)), int(ce.get("y", 0))
                if not (andavel(L, x, y) and (x, y) not in bloq):
                    assert (ce["script"], (x, y)) in sabe_consertar, \
                        (f"{meu}: {ce['script']} gravado em ({x},{y}), tile "
                         f"inandavel que o gerador nao sabe realocar")
                    pendentes.append((meu, ce["script"], x, y))
                conferidos += 1

    print(f"demo ok ({MEDIDO_EM}):")
    print(f"  fila: {len(pend)} gatilhos e {len(hid)} grupos de Sinnoh")
    print(f"  decisao 8 provada em Amity (27 warps, 18-44) e Twinleaf (2 e 4)")
    print(f"  vars: 49 alias, zero colisao de endereco em vars.h")
    print(f"  flags: {len(novas)} novas em 0x{FLAG_BASE:04X}+, zero colisao "
          f"(apelido e uso cru conferidos)")
    print(f"  span: {r['coord_events_da_fonte']} coord_events da fonte, "
          f"{r['span_bruto']} tiles de span bruto, "
          f"{r['tiles_plantados']} tiles plantados em {r['gatilhos']} gatilhos")
    print(f"  andabilidade: {andados} tiles do censo andaveis e fora de "
          f"warp/NPC fixo; {conferidos} coord_events nossos ja gravados")
    print(f"  gravado: {conferidos} coord_events nossos com rotulo conferido")
    if pendentes:
        print(f"  PENDENTE de --gravar: {len(pendentes)} coord_events gravados "
              f"em tile inandavel, todos com realocacao ja calculada")
        for meu, s, x, y in pendentes:
            print(f"      {meu:28} {s.split('_EventScript_')[1]:38} ({x},{y})")


# --------------------------------------------------------------------- saida

def relatorio(c):
    r = c["resumo"]
    est = collections.Counter(f["estado"] for f in c["flags"])
    print(f"censo de {MEDIDO_EM}")
    print(f"  vars aliasadas ............ {len(c['vars'])}")
    print(f"  flags: novas {est['nova']}  reusadas {est['reusada']}  "
          f"ambiguas {est['ambiguo']}  adiadas {est['adiado']}  "
          f"clones {est['clone']}")
    print(f"  gatilhos plantaveis ....... {r['gatilhos']} em "
          f"{r['mapas_com_gatilho']} mapas, {r['tiles_plantados']} tiles")
    print(f"  adiados ................... {r['adiados']}")
    for motivo, n in collections.Counter(
            a["motivo"].split(";")[0] for a in c["adiados"]).most_common():
        print(f"      {n:3}  {motivo}")
    if c["tiles_empilhados"]:
        print(f"  tiles com mais de um gatilho: {len(c['tiles_empilhados'])} "
              f"(a leva desempata na cena)")
    print(f"  tiles realocados por inandabilidade  {r['tiles_movidos']}")
    for g in c["gatilhos"]:
        for a, b in g["tiles_movidos"]:
            print(f"      {g['mapa']:28} {g['script'].split('_EventScript_')[1]:38} "
                  f"({a[0]},{a[1]}) -> ({b[0]},{b[1]})")
    perdidos = [(g, t) for g in c["gatilhos"] for t in g["tiles_perdidos"]]
    if perdidos:
        print(f"  tiles NAO plantados (sem casa andavel no raio "
              f"{RAIO_REALOCACAO})  {len(perdidos)}")
        for g, t in perdidos:
            print(f"      {g['mapa']:28} {g['script'].split('_EventScript_')[1]:38} "
                  f"({t[0]},{t[1]})")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        c = censo()
        relatorio(c)
        if "--gravar" in sys.argv:
            nv = grava_vars(c)
            nf = grava_flags(c)
            nce, nesq, nmapas, nmov, ndel = grava_mapas(c)
            with open(CENSO, "w", encoding="utf-8") as f:
                json.dump(c, f, ensure_ascii=False, indent=1, sort_keys=True)
                f.write("\n")
            print(f"\ngravado: {nv} vars, {nf} flags novas, {nce} coord_events "
                  f"e {nesq} esqueletos em {nmapas} mapas, censo em "
                  f"{os.path.relpath(CENSO, REPO)}")
            print(f"         {nmov} coord_events ja gravados MOVIDOS para casa "
                  f"andavel e {ndel} apagados por nao haver casa andavel")
        else:
            print("\n(nada gravado; use --gravar depois de --demo verde)")
