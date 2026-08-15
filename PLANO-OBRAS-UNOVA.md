# Plano das obras de Unova (máquina de setscene + tradutor de changeblock)

Documento de referência único das duas obras do bloco B6 de Unova aprovadas
pela condutora em 15/08/2026. Os executores consomem os defines de
`include/constants/vars.h` (bloco `B6 Unova, as 27 vars...`) e
`include/constants/flags.h` (blocos `B6 Unova, EVENT_*...`) e as tabelas
abaixo como fonte única de valor. Ninguém inventa número de scene nem de
EVENT_: se um valor não está nas tabelas, ele não existe ainda, e o certo é
voltar aqui, não adivinhar.

Escrito varrendo `fontes-mapas/bw3g/maps/*.asm` com `dev_scripts/fila_b6.py`
(a mesma travessia que já segue fallthrough e `jumpstd`, ver o cabeçalho
daquele arquivo). Nenhum número aqui foi digitado de memória.

## Ordem de execução

**Obra 2 (changeblock) roda ANTES da Obra 1 (setscene)**, decisão 6 da
condutora. Motivo: várias cenas de setscene fazem `applymovement` sobre
metatiles que só existem depois do changeblock (ex.: o jogador atravessando
VillageBridge depois da ponte baixar). Rodar a máquina de scene antes deixaria
o executor escrevendo script contra um chão que ainda não existe.

## Obra 1 — vars das 27 cenas de setscene

### Contagem contra o desenho de 15/08/2026

| | desenho | esta varredura | bate? |
|---|---|---|---|
| vars (mapas com setscene) | 26 | **27** | não — ver divergência abaixo |
| flags EVENT_ das 59 cenas | 21 | **21** | sim |
| flags EVENT_ do changeblock | 20 | **20** | sim |

**Divergência de 1 var, explicada:** a varredura de `coord_events` tipo
`setscene` achou **25** mapas com `scene_script` próprio (não 24), mais os
3 alvos remotos = 28, menos `ShoppingMallNine` (descartada, ver decisão 5) =
**27**. O mapa extra é **`PWT_OUTSIDE`** (Pokémon World Tournament): o
`coord_event` de (8,13) é uma cena real — despedida do CHEREN/BIANCA,
`clearevent EVENT_ASPERTIA_CITY_BLOCKER`, `setscene SCENE_FINISHED` — o mapa
já está importado (`data/maps/Unova_PWTOutside` existe) e não há nenhuma
decisão registrada excluindo-o. Não achei motivo para descartar, e descartar
por conta própria sem decisão explícita seria inventar escopo, não
materializar o que foi aprovado. Mantive a var (`VAR_UNOVA_PWT_FORA_CENA`,
`VAR_UNUSED_0x416F`); se a intenção era mesmo excluir PWT inteiro (o torneio
em si continua fora de escopo, só esta despedida foi incluída), é decisão do
Gui, não minha.

`HALL_OF_FAME` tem 2 `scene_script` na fonte mas **não entra**: nada dentro do
próprio `HallOfFame.asm` faz `checkscene`, então o valor gravado nunca é lido
por ninguém; a var seria morta.

### Tabela mapa → var → valores (fonte única)

Ordem: os 24 mapas locais (coord_event próprio, minus `ShoppingMallNine`),
depois os 3 alvos remotos. "Local" = a própria cena que dispara `setscene`
mora no mapa. "Remoto" = o mapa só recebe `setmapscene` de fora, nunca tem
`coord_event` próprio que grave seu scene.

| mapa (MAP_CONST) | var | endereço | valores (0, 1, 2...) |
|---|---|---|---|
| CASTELIA_CITY_STREETS | `VAR_UNOVA_CASTELIA_RUAS_CENA` | 0x4161 | 0=SCENE_DEFAULT, 1=SCENE_CASTELIA_CHEREN, 2=SCENE_CASTELIA_NOTHING |
| CHAMPIONS_ROOM_ENTRANCE | `VAR_UNOVA_SALA_CAMPEAO_ENTRADA_CENA` | 0x4162 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| DRAGONSPIRAL_TOWER_6F | `VAR_UNOVA_DRAGONSPIRAL_6F_CENA` | 0x4163 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| DRAGONSPIRAL_TOWER_ROOF | `VAR_UNOVA_DRAGONSPIRAL_TOPO_CENA` | 0x4164 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| DRIFTVEIL_BRIDGE_GATE | `VAR_UNOVA_DRIFTVEIL_PORTAO_PONTE_CENA` | 0x4165 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| FLOCCESY_TOWN | `VAR_UNOVA_FLOCCESY_CENA` | 0x4166 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| GIANT_CHASM_1F | `VAR_UNOVA_GIANT_CHASM_CENA` | 0x4167 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| LOSTLORN_FOREST | `VAR_UNOVA_LOSTLORN_FOREST_CENA` | 0x4168 | 0=SCENE_LOSTLORN_GRUNTS, 1=SCENE_LOSTLORN_INFER, 2=SCENE_LOSTLORN_NOTHING |
| NACRENE_CITY | `VAR_UNOVA_NACRENE_CENA` | 0x4169 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| NIMBASA_PARK_BASEMENT | `VAR_UNOVA_NIMBASA_PARK_PORAO_CENA` | 0x416A | 0=SCENE_NIMBASA_PARK_BASEMENT_INFER, 1=SCENE_NIMBASA_PARK_BASEMENT_PLASMA, 2=SCENE_NIMBASA_PARK_BASEMENT_NOTHING |
| NUVEMA_LAB | `VAR_UNOVA_NUVEMA_LAB_CENA` | 0x416B | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| OPELUCID_CITY | `VAR_UNOVA_OPELUCID_CENA` | 0x416C | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| P2_LAB | `VAR_UNOVA_P2_LAB_CENA` | 0x416D | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| P2_LAB_ENTRANCE | `VAR_UNOVA_P2_LAB_ENTRADA_CENA` | 0x416E | 0=SCENE_P2_LAB_ENTRANCE_DEFAULT, 1=SCENE_P2_LAB_ENTRANCE_AFTER, 2=SCENE_P2_LAB_ENTRANCE_NOTHING |
| PWT_OUTSIDE | `VAR_UNOVA_PWT_FORA_CENA` | 0x416F | 0=SCENE_DEFAULT, 1=SCENE_FINISHED (ver divergência acima) |
| PKMN_LEAGUE_ENTRANCE | `VAR_UNOVA_LIGA_ENTRADA_CENA` | 0x4170 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| PLAYERS_HOUSE_1F | `VAR_UNOVA_CASA_JOGADOR_1F_CENA` | 0x4171 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| R_12 | `VAR_UNOVA_R12_CENA` | 0x4172 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| R_23_EAST | `VAR_UNOVA_R23_LESTE_CENA` | 0x4173 | 0=SCENE_R23_SHOWED_NONE, 1=SCENE_R23_SHOWED_SPOOKY, 2=SCENE_R23_SHOWED_INSECT, 3=SCENE_R23_SHOWED_TOXIC, 4=SCENE_R23_SHOWED_BASIC, 5=SCENE_R23_SHOWED_GARNISH, 6=SCENE_R23_SHOWED_JET |
| R_23_GATE | `VAR_UNOVA_R23_PORTAO_CENA` | 0x4174 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| R_23_WEST | `VAR_UNOVA_R23_OESTE_CENA` | 0x4175 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| R_5_BRIDGE_GATE | `VAR_UNOVA_R5_PORTAO_PONTE_CENA` | 0x4176 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| SEASIDE_CAVE_CHAMBER | `VAR_UNOVA_SEASIDE_CAVE_CAMARA_CENA` | 0x4177 | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| UNDELLA_TOWN | `VAR_UNOVA_UNDELLA_CENA` | 0x4178 | 0=SCENE_DEFAULT, 1=SCENE_UNDELLA_TOWN_CANT_LEAVE, 2=SCENE_UNDELLA_TOWN_NOTHING |
| **NIMBASA_PARK_OUTSIDE** (remoto) | `VAR_UNOVA_NIMBASA_PARK_FORA_CENA` | 0x4179 | 0=SCENE_DEFAULT, 1=SCENE_NIMBASA_PARK_OUTSIDE_CHEREN, 2=SCENE_NIMBASA_PARK_OUTSIDE_AFTER, 3=SCENE_NIMBASA_PARK_OUTSIDE_NOTHING |
| **R_12_VILLAGE_BRIDGE_GATE** (remoto) | `VAR_UNOVA_R12_VILLAGE_BRIDGE_PORTAO_CENA` | 0x417A | 0=SCENE_DEFAULT, 1=SCENE_FINISHED |
| **PKMN_LEAGUE_MAIN** (remoto) | `VAR_UNOVA_LIGA_SALAO_CENA` | 0x417B | 0=SCENE_ELITE_FOUR_ROOM_ENTER, 1=SCENE_ELITE_FOUR_ROOM_NOTHING, 2=SCENE_ELITE_FOUR_ROOM_FINISHED |

Faixa usada: `VAR_UNUSED_0x4161`–`0x417B` (27 endereços). Livres na faixa
reservada (`0x4161`–`0x41BF`): **68** (`0x417C`–`0x41BF`).

`HALL_OF_FAME` continua em `VAR_UNOVA_LIGA_CENA` (0x4160, já existia).

## Obra 1 — flags dos EVENT_ das 59 cenas de setscene

21 `EVENT_*` distintos, alcançados pela mesma varredura (coord_events tipo
`setscene`, das 59 cenas pendentes — a 60ª, em `Unova_CasteliaGym`, já está
`feita`). Bate exatamente com os 21 do desenho.

| EVENT_ da fonte | FLAG_ | endereço |
|---|---|---|
| EVENT_ASPERTIA_CITY_BLOCKER | `FLAG_UNOVA_ASPERTIA_BLOQUEIO` | 0x1A0E |
| EVENT_DRAGONSPIRAL_TOWER_6F_INFER | `FLAG_UNOVA_DRAGONSPIRAL_6F_INFER` | 0x1A0F |
| EVENT_DRAGONSPIRAL_TOWER_SAGES | `FLAG_UNOVA_DRAGONSPIRAL_SABIOS` | 0x1A10 |
| EVENT_DRAYDENS_HOUSE_DRAGON_FANG | `FLAG_UNOVA_DRAYDEN_CASA_PRESA_DRAGAO` | 0x1A11 |
| EVENT_DRAYDENS_HOUSE_IRIS | `FLAG_UNOVA_DRAYDEN_CASA_IRIS` | 0x1A12 |
| EVENT_DRIFTVEIL_BLOCKER | `FLAG_UNOVA_DRIFTVEIL_BLOQUEIO` | 0x1A13 |
| EVENT_FINISHED_DRAGONSPIRAL_TOWER | `FLAG_UNOVA_DRAGONSPIRAL_CONCLUIDA` | 0x1A14 |
| EVENT_GOT_DRAGON_FANG | `FLAG_UNOVA_RECEBEU_PRESA_DRAGAO` | 0x1A15 |
| EVENT_GOT_OSHAWOTT | `FLAG_UNOVA_ESCOLHEU_OSHAWOTT` | 0x1A16 |
| EVENT_GOT_SNIVY | `FLAG_UNOVA_ESCOLHEU_SNIVY` | 0x1A17 |
| EVENT_NIMBASA_PARK_GRUNTS | `FLAG_UNOVA_NIMBASA_PARK_GRUNTS` | 0x1A18 |
| EVENT_NIMBASA_PARK_HIDDEN_GRUNT | `FLAG_UNOVA_NIMBASA_PARK_GRUNT_ESCONDIDO` | 0x1A19 |
| EVENT_NIMBASA_PARK_OUTSIDE_CHEREN | `FLAG_UNOVA_NIMBASA_PARK_FORA_CHEREN` | 0x1A1A |
| EVENT_OPELUCID_CITY_IRIS | `FLAG_UNOVA_OPELUCID_IRIS` | 0x1A1B |
| EVENT_PKMN_LEAGUE_ENTRANCE_INFER | `FLAG_UNOVA_LIGA_ENTRADA_INFER` | 0x1A1C |
| EVENT_PLAYERS_HOUSE_1F_NEIGHBOR | `FLAG_UNOVA_CASA_JOGADOR_VIZINHO` | 0x1A1D |
| EVENT_PLAYERS_HOUSE_MOM_1 | `FLAG_UNOVA_CASA_JOGADOR_MAE_1` | 0x1A1E |
| EVENT_PLAYERS_HOUSE_MOM_2 | `FLAG_UNOVA_CASA_JOGADOR_MAE_2` | 0x1A1F |
| EVENT_PLAYERS_NEIGHBORS_HOUSE_NEIGHBOR | `FLAG_UNOVA_CASA_DO_VIZINHO_NPC` | 0x1A20 |
| EVENT_TEMPORARY_UNTIL_MAP_RELOAD_1 | `FLAG_UNOVA_TEMP_ATE_RECARGA_1` | 0x1A21 |
| EVENT_TEMPORARY_UNTIL_MAP_RELOAD_2 | `FLAG_UNOVA_TEMP_ATE_RECARGA_2` | 0x1A22 |

## Obra 2 — flags dos EVENT_ do changeblock (12 mapas da fila)

Os 12 mapas confirmam `ESTADO.md` linha 350 ("107 de changeblock em 12
mapas"; a varredura atual, com fallthrough, dá 108 cenas nos mesmos 12
mapas). 20 `EVENT_*` distintos, dois por mapa quando há um pré-requisito de
Strength/Twist Mountain antes da troca de bloco em si, um só nos demais.
Bate exatamente com os 20 do desenho.

| mapa (12 da fila) | EVENT_ da fonte | FLAG_ | endereço | papel |
|---|---|---|---|---|
| DragonspiralTower2F | EVENT_DRAGONSPIRAL_TOWER_UPPER_LEVEL | `FLAG_UNOVA_DRAGONSPIRAL_2F_ANDAR_SUPERIOR` | 0x1A23 | estado do andar |
| DragonspiralTower2F | EVENT_DRAGONSPIRAL_TOWER_2F_BOULDER | `FLAG_UNOVA_DRAGONSPIRAL_2F_PEDRA` | 0x1A24 | pré-requisito (pedra) |
| Dreamyard | EVENT_DREAMYARD_UPPER_LEVEL | `FLAG_UNOVA_DREAMYARD_ANDAR_SUPERIOR` | 0x1A25 | estado do andar |
| Dreamyard | EVENT_DREAMYARD_BOULDER | `FLAG_UNOVA_DREAMYARD_PEDRA` | 0x1A26 | pré-requisito (pedra) |
| IcirrusCitySouth | EVENT_ICIRRUS_CITY_UPPER_FLOOR | `FLAG_UNOVA_ICIRRUS_ANDAR_SUPERIOR` | 0x1A27 | estado do andar |
| IcirrusCitySouth | EVENT_OPENED_TWIST_MOUNTAIN | `FLAG_UNOVA_TWIST_MOUNTAIN_ABERTO` | 0x1A28 | pré-requisito |
| Rt11 | EVENT_R11_LOWER_FLOOR | `FLAG_UNOVA_R11_ANDAR_INFERIOR` | 0x1A29 | estado do andar |
| Rt18 | EVENT_R_18_LOWER | `FLAG_UNOVA_R18_ANDAR_INFERIOR` | 0x1A2A | estado do andar |
| SeasideCave1F | EVENT_SEASIDE_CAVE_LOWER_FLOOR | `FLAG_UNOVA_SEASIDE_CAVE_ANDAR_INFERIOR` | 0x1A2B | estado do andar |
| VictoryRoadCave1F | EVENT_VICTORY_ROAD_CAVE_LOWER | `FLAG_UNOVA_VICTORY_ROAD_ANDAR_INFERIOR` | 0x1A2C | estado do andar |
| VictoryRoadCave1F | EVENT_VICTORY_ROAD_RUINS_BOULDER_1 | `FLAG_UNOVA_VICTORY_ROAD_PEDRA_1` | 0x1A2D | pré-requisito (pedra 1) |
| VictoryRoadCave1F | EVENT_VICTORY_ROAD_RUINS_BOULDER_2 | `FLAG_UNOVA_VICTORY_ROAD_PEDRA_2` | 0x1A2E | pré-requisito (pedra 2) |
| VillageBridge | EVENT_VILLAGE_BRIDGE_LOWER | `FLAG_UNOVA_VILLAGE_BRIDGE_ANDAR_INFERIOR` | 0x1A2F | estado do andar |
| VirbankCity | EVENT_VIRBANK_CITY_LOWER_FLOOR | `FLAG_UNOVA_VIRBANK_CITY_ANDAR_INFERIOR` | 0x1A30 | estado do andar |
| VirbankComplexB1F | EVENT_OPENED_VIRBANK_COMPLEX_DOOR | `FLAG_UNOVA_VIRBANK_COMPLEX_PORTA` | 0x1A31 | estado da porta (MAPCALLBACK_TILES) |
| VirbankComplexB2F | EVENT_VIRBANK_COMPLEX_B2F_SWITCH1 | `FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_1` | 0x1A32 | interruptor 1/4 |
| VirbankComplexB2F | EVENT_VIRBANK_COMPLEX_B2F_SWITCH2 | `FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2` | 0x1A33 | interruptor 2/4 |
| VirbankComplexB2F | EVENT_VIRBANK_COMPLEX_B2F_SWITCH3 | `FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3` | 0x1A34 | interruptor 3/4 |
| VirbankComplexB2F | EVENT_VIRBANK_COMPLEX_B2F_SWITCH4 | `FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4` | 0x1A35 | interruptor 4/4 |
| VirbankComplexOutside | EVENT_VIRBANK_COMPLEX_UPPER_FLOOR | `FLAG_UNOVA_VIRBANK_COMPLEX_ANDAR_SUPERIOR` | 0x1A36 | estado do andar |

**Zero coincidência entre os 21 EVENT_ da Obra 1 e os 20 da Obra 2** — nomes
checados um a um, nenhum repete. Não houve caso de "uma flag só, comentário
duplo" para aplicar.

Faixa usada: `FLAG_UNUSED_0x1A0E`–`0x1A36` (41 endereços: 21 + 20,
sequenciais, sem buraco). Livres na faixa reservada (`0x1A0E`–`0x1AFF`):
**201** (`0x1A37`–`0x1AFF`).

`EVENT_BEAT_VIRBANK_COMPLEX_BRONIUS` e `EVENT_ASPERTIA_CITY_BLOCKER` aparecem
dentro do fecho de `VirbankComplexB1F` (batalha do BRONIUS) mas **não**
entraram na Obra 2: são efeito colateral da cena de batalha, não gravam nem
condicionam o `changeblock` da porta — quem faz isso é só
`EVENT_OPENED_VIRBANK_COMPLEX_DOOR`. `EVENT_ASPERTIA_CITY_BLOCKER` já está
coberto pela Obra 1 (`FLAG_UNOVA_ASPERTIA_BLOQUEIO`); `EVENT_BEAT_VIRBANK_
COMPLEX_BRONIUS` não faz parte de nenhuma das duas obras (é flag de batalha
de treinador, fora do escopo de vars/flags desta frente).

## As 6 decisões da condutora (15/08/2026)

1. **Elevação explícita no `setmetatileinrange`.** Os 91 quadrantes que
   trocam para/de água usam elevação EXPLÍCITA, nunca o valor default.
   Armadilha verificada em `src/scrcmd.c` (`NativeFunc_SetMetatileInRange`,
   linhas ~2760–2789): o parâmetro `elevation` só é aplicado quando
   `elevation < 15` — passar `0xFF` como "não mexe" na verdade PULA a
   atribuição e a elevação fica em 0 (chão), não na elevação atual do tile.
   E `hasCollision = TRUE` grava `MAPGRID_COLLISION_MASK` (`0x0C00`, bits
   10-11 setados = colisão 3), então marcar "tem colisão" sem querer bloqueia
   o quadrante de vez.
2. **`changeblock` vira macro `changeblock_gen2`** que expande em 4
   `setmetatile` (um por quadrante 2×2 do bloco de gen 2, que é 16×16 contra
   os 8×8 dos metatiles daqui).
3. **Escopo desta fase: os 12 mapas da fila** (tabela da Obra 2 acima).
   A ferramenta de tradução já está pronta para os 40 arquivos que citam
   `changeblock` em algum lugar (ver cabeçalho de `fila_b6.py`), mas só estes
   12 têm changeblock alcançado por `coord_event` de fato jogável nesta leva.
4. **`setmetatile` de cena vai em `MAP_SCRIPT_ON_LOAD`, nunca em
   `ON_TRANSITION`.** `InitMapLayoutData` roda DEPOIS do `ON_TRANSITION` e
   ANTES do `ON_LOAD` (`src/fieldmap.c`, `InitMap()`, linhas ~134-138: chama
   `InitMapLayoutData` e só depois `RunOnLoadMapScript`). Um `setmetatile`
   feito em `ON_TRANSITION` é sobrescrito pela releitura do layout antes do
   jogador ver a tela; feito em `ON_LOAD` ele fica.
5. **`ShoppingMallNine` descartada.** A fonte cita `SHOPPING_MALL_NINE` em
   `data/maps/scenes.asm` (var reservada) e algum gatilho a referencia, mas
   `ShoppingMallNine.asm` tem **zero** `scene_script` (`db 0 ; scene
   scripts`, nenhuma linha depois) — o gatilho não tem máquina de estados
   para acionar na fonte. Não dá para portar o que não existe.
   **Nota para a próxima regeneração de `dev_scripts/fila_b6.json`:** o JSON
   é gerado, não editado à mão, então esta exceção não foi marcada nele.
   Quando `fila_b6.py --gravar` rodar de novo, o item de `ShoppingMallNine`
   do tipo `setscene` (hoje 1 cena, `Unova_ShoppingMallNine`, status
   `pendente`) deve ser tratado como **descartado por decisão de 15/08/2026**
   (0 `scene_script` na fonte), não como pendência de executor.
6. **Obra 2 (changeblock) antes da Obra 1 (setscene)** na ordem de execução
   — ver seção "Ordem de execução" acima.

## Plano de blocos executáveis

Construído agora, a partir das tabelas acima, para dar ao executor uma
sequência com risco crescente dentro de cada obra. Ordem geral: B (Obra 2)
primeiro, A (Obra 1) depois, decisão 6.

### Obra 2 — changeblock (B1-B5)

- **B1 — pré-requisitos de pedra/Twist Mountain.** `DragonspiralTower2F`,
  `Dreamyard`, `VictoryRoadCave1F` (2 pedras), `IcirrusCitySouth` (Twist
  Mountain). Padrão comum: flag de pré-requisito + flag de andar, 2
  `changeblock_gen2` por mapa. Fazer primeiro porque é o padrão mais repetido
  (4 dos 12 mapas) e estabelece o molde para os outros.
- **B2 — andares simples, sem pré-requisito.** `Rt11`, `Rt18`,
  `SeasideCave1F`, `VillageBridge`, `VirbankCity`. Uma flag, um
  `changeblock_gen2`, aplica o molde de B1 sem a parte de pré-requisito.
- **B3 — Virbank Complex, andar e porta.** `VirbankComplexOutside` (andar) +
  `VirbankComplexB1F` (porta, via `MAPCALLBACK_TILES .CheckDoor` — não é
  `coord_event`, é callback de mapa, atenção ao portar).
- **B4 — Virbank Complex B2F, os 4 interruptores.** O caso mais complexo da
  obra (16 blocos de `changeblock`, lógica cruzada entre os 4
  `FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_*`); isolado em bloco próprio
  de propósito.
- **B5 — QA da Obra 2.** Rodar `dev_scripts/fila_b6.py --demo` (a trava de
  108 `changeblock` continua valendo), conferir os 12 mapas contra
  `data/maps/Unova_*/map.json` e regenerar `fila_b6.json`.

### Obra 1 — setscene (A1-A6)

- **A1 — arco do dragão.** `DragonspiralTower6F`, `DragonspiralTowerRoof`,
  mais as flags `FLAG_UNOVA_DRAGONSPIRAL_*`, `FLAG_UNOVA_DRAYDEN_*`,
  `FLAG_UNOVA_RECEBEU_PRESA_DRAGAO`. Depende de B1 (mesmo andar da torre já
  ter o `changeblock` certo).
- **A2 — parque de Nimbasa.** `NimbasaParkBasement` (local) +
  `NIMBASA_PARK_OUTSIDE` (remoto) + as flags de grunt/Plasma/CHEREN.
- **A3 — casa do jogador e vizinhança.** `PLAYERS_HOUSE_1F`, as flags
  `FLAG_UNOVA_CASA_JOGADOR_*` e `FLAG_UNOVA_CASA_DO_VIZINHO_NPC`.
- **A4 — cidades e rotas.** `CasteliaCityStreets`, `NacreneCity`,
  `OpelucidCity`, `FloccesyTown`, `UndellaTown`, `R_12`, `R_23_EAST/GATE/
  WEST`, `SeasideCaveChamber`, `GiantChasm1F`, `LostlornForest`, `P2_LAB` +
  `P2_LAB_ENTRANCE`, `PWT_OUTSIDE` (ver divergência). O bloco mais numeroso;
  cada mapa é independente dos outros, dá para paralelizar entre sessões.
- **A5 — Liga.** `ChampionsRoomEntrance`, `PkmnLeagueEntrance`,
  `PKMN_LEAGUE_MAIN` (remoto), `R_12_VILLAGE_BRIDGE_GATE` (remoto),
  `DriftveilBridgeGate`/`R_5_BRIDGE_GATE` (irmãos, mesma ponte). Por último
  porque é o clímax da história e depende de tudo que já rodou antes
  (insígnias, arco do dragão).
- **A6 — QA da Obra 1.** Rodar `dev_scripts/fila_b6.py --demo`, conferir as
  59 cenas `setscene` contra `coord_events` de `data/maps/Unova_*/map.json` e
  regenerar `fila_b6.json` (que também aplica a nota da decisão 5 sobre
  `ShoppingMallNine`).

## Treinadores de Unova (bloqueado nesta leva)

`trainerbattle` de Unova usa ids na faixa **1800-2199**, molde em
`dev_scripts/gera_treinadores_unova.py` (`BASE_ID = 1800`, `TETO_ID = 2199`).
Conferido agora: **52 ids livres** na faixa (348 já usados de 400).
`include/constants/opponents.h` está **bloqueado por Johto nesta leva** (o
agente de Johto está gravando lá agora) — quando o agente de treinadores de
Unova rodar, ele consome dessa mesma faixa pelo molde já pronto, sem precisar
de decisão nova aqui.
