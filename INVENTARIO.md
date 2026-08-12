# Inventário por região, medido contra a fonte

Gerado por `python3 dev_scripts/inventario.py`. **Não edite à mão**:
todo número aqui sai de um arquivo da fonte, e o caminho do arquivo
está na própria linha, para poder ser conferido abrindo ele.

Toda coluna aparece como `aqui / fonte`. Onde a fonte não tem par para o
mapa, a linha sai com `--` e nunca com zero: não saber é um resultado.

**Existe não é ter conteúdo.** É a lição que fez `completude.py` dar 98%
para Unova sendo maquete de colisão. Por isso `pessoas` e `com fala` são
colunas diferentes, e `placas` e `com texto` também. Um NPC pode existir,
ocupar índice de save e não dizer uma palavra.

Pokémon de overworld do hns (1390 objetos) fora da régua por decisão de 12/08: dívida de feature inexistente não é fila de trabalho.

## Resumo por região

| região | fonte | mapas aqui / fonte | objetos | pessoas | com fala | treinadores | placas | com texto | encontros |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Kanto | pokefirered | 417 / 425 | 1650 / 1648 | 1240 / 1238 | 1060 / 1058 | 253 / 253 | 519 / 519 | 514 / 515 | 124 / 124 |
| Johto | hns | 236 / 243 | 2231 / 2374 | 782 / 944 | 532 / 746 | 238 / 270 | 486 / 506 | 293 / 300 | 87 / 87 |
| Hoenn | pokeemerald | 518 / 518 | 2778 / 2776 | 2276 / 2274 | 1545 / 1559 | 533 / 537 | 533 / 533 | 392 / 395 | 116 / 116 |
| Sinnoh | pokeplatinum | 433 / 594 | 1693 / 2730 | 1689 / 1739 | 1285 / 1369 | 395 / 393 | 598 / 565 | 505 / 516 | 128 / 128 |
| Unova | bw3g | 291 / 309 | 1395 / 1357 | 945 / 915 | 888 / 811 | 360 / 348 | 363 / 355 | 217 / 173 | 87 / 65 |

Leitura das colunas:

- **mapas aqui / fonte**: quantos mapas nossos casaram com a fonte, contra
  o total que a fonte tem daquela região (casados mais ausentes).
- **pessoas**: `object_event` que é gente. Item ball, árvore de Cut, pedra
  de Strength, caminhão e boneco de quarto secreto não entram, dos dois
  lados, senão a conta compara mobília com gente.
- **com fala**: dessas pessoas, quantas têm script que chega a pôr texto na
  tela. É a coluna de CONTEÚDO; a anterior é só de presença.
- **treinadores**: aqui é constante citada por `trainerbattle` E com bloco
  `=== TRAINER_X ===` num `.party` compilado (`trainers.party` e
  `trainers_frlg.party`; os `.party` de Johto e Sinnoh são acervo e não
  entram na ROM). Na fonte é o treinador que a fonte declara no mapa.
- **placas / com texto**: `bg_event` com script, e quantas dessas têm texto
  próprio em vez de rótulo genérico compartilhado.
- **encontros**: mapas com tabela de Pokémon selvagem.

## Kanto (fonte: `fontes-mapas/pokefirered`)

417 mapas nossos, 417 com par na fonte, 0 sem par, 8 mapas da fonte ausentes aqui.

### Os dois totais, lado a lado

| medida | existe | tem conteúdo | fonte |
|---|---:|---:|---:|
| pessoas | 1240 | 1060 com fala | 1238 (1058 com fala) |
| placas | 519 | 514 com texto | 519 (515 com texto) |
| treinadores | 253 citados por trainerbattle | 253 com time | 253 |
| mapas | 417 | 293 com pelo menos um NPC que fala | 425 |
| encontros | 124 | -- | 124 |

Dos 1240 que existem, **180 não falam**: 41 sem script nenhum (`script: "0"`) e 139 com rótulo que não tem comando de texto (parte é balconista e enfermeira, que chamam loja e cura direto, e parte é NPC pela metade). A fonte tem 180 mudos nos mesmos mapas, então a dívida real é **1**, somada mapa a mapa (o excesso de um mapa não paga a falta de outro).

Objetos que NÃO são gente (item ball, árvore, pedra, mobília): **410 aqui contra 410 na fonte**. Esta linha importa porque `completude.py` conta objeto e não gente: quando o total de objetos bate com a fonte e o de pessoas não, o que aconteceu foi troca de sprite, não falta de objeto. É o caso de Johto, onde o importador pôs `OBJ_EVENT_GFX_ITEM_BALL` com `script: "0"` na coordenada exata de cada NPC da fonte (conferido à mão em `EcruteakCity`, 49 objetos dos dois lados e 49 item balls aqui).

### Mapa a mapa (só os que divergem da fonte)

Toda coluna de lacuna é medida CONTRA A FONTE, nunca contra o ideal. Mapa igual à fonte não aparece aqui, mesmo cheio de NPC mudo: o pokeemerald vanilla também tem, e reprovar o jogo original é a lição 4.10 do `ESTADO.md`.

| mapa | objetos | pessoas | falta | excesso | mudo a mais | treinador | placa genérica a mais | encontro | arquivo da fonte |
|---|---:|---:|---:|---:|---:|---:|---:|:-:|---|
| `VermilionCity_Frlg` | 10 / 8 | 9 / 7 |  | 2 | 1 | 0 / 0 |  | ok | `fontes-mapas/pokefirered/data/maps/VermilionCity/map.json` |
| `PalletTown_PlayersHouse_2F_Frlg` | 0 / 0 | 0 / 0 |  |  |  | 0 / 0 | 1 | ok | `fontes-mapas/pokefirered/data/maps/PalletTown_PlayersHouse_2F/map.json` |

<details><summary>8 mapas que a fonte tem e nós não</summary>

- `Prototype_SeviiIsle_6`
- `Prototype_SeviiIsle_7`
- `Prototype_SeviiIsle_8`
- `Prototype_SeviiIsle_9`
- `Route19_UnusedHouse`
- `Route23_UnusedHouse`
- `Route6_UnusedHouse`
- `SevenIsland_UnusedHouse`

</details>

## Johto (fonte: `fontes-mapas/hns`)

236 mapas nossos, 233 com par na fonte, 3 sem par, 10 mapas da fonte ausentes aqui.

### Os dois totais, lado a lado

| medida | existe | tem conteúdo | fonte |
|---|---:|---:|---:|
| pessoas | 782 | 532 com fala | 944 (746 com fala) |
| placas | 486 | 293 com texto | 506 (300 com texto) |
| treinadores | 238 citados por trainerbattle | 238 com time | 270 |
| mapas | 236 | 146 com pelo menos um NPC que fala | 243 |
| encontros | 87 | -- | 87 |

Dos 782 que existem, **250 não falam**: 244 sem script nenhum (`script: "0"`) e 6 com rótulo que não tem comando de texto (parte é balconista e enfermeira, que chamam loja e cura direto, e parte é NPC pela metade). A fonte tem 198 mudos nos mesmos mapas, então a dívida real é **97**, somada mapa a mapa (o excesso de um mapa não paga a falta de outro).

Objetos que NÃO são gente (item ball, árvore, pedra, mobília): **1449 aqui contra 1430 na fonte**. Esta linha importa porque `completude.py` conta objeto e não gente: quando o total de objetos bate com a fonte e o de pessoas não, o que aconteceu foi troca de sprite, não falta de objeto. É o caso de Johto, onde o importador pôs `OBJ_EVENT_GFX_ITEM_BALL` com `script: "0"` na coordenada exata de cada NPC da fonte (conferido à mão em `EcruteakCity`, 49 objetos dos dois lados e 49 item balls aqui).

### Mapa a mapa (só os que divergem da fonte)

Toda coluna de lacuna é medida CONTRA A FONTE, nunca contra o ideal. Mapa igual à fonte não aparece aqui, mesmo cheio de NPC mudo: o pokeemerald vanilla também tem, e reprovar o jogo original é a lição 4.10 do `ESTADO.md`.

| mapa | objetos | pessoas | falta | excesso | mudo a mais | treinador | placa genérica a mais | encontro | arquivo da fonte |
|---|---:|---:|---:|---:|---:|---:|---:|:-:|---|
| `EcruteakCity_Theater` | 12 / 12 | 0 / 11 | 11 |  |  | 0 / 6 |  | ok | `fontes-mapas/hns/data/maps/EcruteakCity_Theater/map.json` |
| `Route41` | 63 / 63 | 28 / 40 | 12 |  |  | 10 / 10 |  | ok | `fontes-mapas/hns/data/maps/Route41/map.json` |
| `GoldenrodCity` | 41 / 40 | 9 / 19 | 10 |  |  | 1 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity/map.json` |
| `AzaleaTown` | 6 / 19 | 6 / 12 | 6 |  |  | 1 / 3 |  | ok | `fontes-mapas/hns/data/maps/AzaleaTown/map.json` |
| `DragonsDen_Cavern` | 35 / 35 | 10 / 18 | 8 |  |  | 3 / 3 |  | ok | `fontes-mapas/hns/data/maps/DragonsDen_Cavern/map.json` |
| `GoldenrodCity_RadioTower_4F` | 2 / 7 | 2 / 6 | 4 |  |  | 1 / 4 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_4F/map.json` |
| `WhirlIslands_LugiaChamber` | 8 / 8 | 0 / 7 | 7 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/WhirlIslands_LugiaChamber/map.json` |
| `GoldenrodCity_RadioTower_2F` | 4 / 9 | 4 / 8 | 4 |  |  | 2 / 4 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_2F/map.json` |
| `TinTower_RoofDay` | 6 / 8 | 0 / 6 | 6 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/TinTower_RoofDay/map.json` |
| `GoldenrodCity_RadioTower_3F` | 3 / 6 | 3 / 6 | 3 |  |  | 2 / 4 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_3F/map.json` |
| `LakeOfRage` | 17 / 17 | 8 / 11 | 3 |  | 2 | 4 / 4 |  | ok | `fontes-mapas/hns/data/maps/LakeOfRage/map.json` |
| `OlivineCity_PortInside` | 1 / 7 | 1 / 6 | 5 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/OlivineCity_PortInside/map.json` |
| `SlowpokeWell_B1F` | 6 / 22 | 5 / 10 | 5 |  |  | 4 / 4 |  | ok | `fontes-mapas/hns/data/maps/SlowpokeWell_B1F/map.json` |
| `TrainerHill_Courtyard` | 29 / 29 | 8 / 8 |  |  | 5 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/TrainerHill_Courtyard/map.json` |
| `BurnedTower_1F` | 5 / 14 | 3 / 5 | 2 |  |  | 3 / 5 |  | ok | `fontes-mapas/hns/data/maps/BurnedTower_1F/map.json` |
| `CherrygroveCity` | 14 / 14 | 4 / 5 | 1 |  | 1 | 1 / 3 |  | ok | `fontes-mapas/hns/data/maps/CherrygroveCity/map.json` |
| `GoldenrodCity_UndergroundSwitches` | 10 / 10 | 6 / 7 | 1 |  |  | 6 / 9 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_UndergroundSwitches/map.json` |
| `IlexForest` | 38 / 38 | 4 / 8 | 4 |  |  | 1 / 1 |  | ok | `fontes-mapas/hns/data/maps/IlexForest/map.json` |
| `AzaleaTown_KurtsHouse` | 4 / 4 | 1 / 3 | 2 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/AzaleaTown_KurtsHouse/map.json` |
| `BlackthornCity` | 25 / 25 | 7 / 7 |  |  | 3 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/BlackthornCity/map.json` |
| `CianwoodCity` | 21 / 21 | 4 / 6 | 2 |  |  | 0 / 1 |  | ok | `fontes-mapas/hns/data/maps/CianwoodCity/map.json` |
| `EcruteakCity` | 49 / 49 | 7 / 9 | 2 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/EcruteakCity/map.json` |
| `Gate_GoldenrodCity_Route35` | 3 / 4 | 3 / 4 | 1 |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Gate_GoldenrodCity_Route35/map.json` |
| `Gate_Route43` | 3 / 3 | 0 / 3 | 3 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Gate_Route43/map.json` |
| `GoldenrodCity_DepartmentStoreBasement` | 13 / 13 | 3 / 3 |  |  | 3 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_DepartmentStoreBasement/map.json` |
| `GoldenrodCity_FlowerShop` | 4 / 4 | 3 / 4 | 1 |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_FlowerShop/map.json` |
| `GoldenrodCity_UndergroundTunnel` | 12 / 12 | 6 / 8 | 2 |  | 1 | 4 / 4 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_UndergroundTunnel/map.json` |
| `Mahoganytown` | 9 / 9 | 3 / 4 | 1 |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Mahoganytown/map.json` |
| `OlivineCity` | 34 / 35 | 5 / 7 | 2 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/OlivineCity/map.json` |
| `OlivineCity_PortOutside` | 0 / 3 | 0 / 3 | 3 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/OlivineCity_PortOutside/map.json` |
| `ReceptionGate` | 4 / 4 | 1 / 4 | 3 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/ReceptionGate/map.json` |
| `Route26` | 10 / 16 | 2 / 4 | 2 |  |  | 4 / 5 |  | ok | `fontes-mapas/hns/data/maps/Route26/map.json` |
| `Route29` | 17 / 17 | 6 / 6 |  |  | 3 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route29/map.json` |
| `Route30_MrPokemonsHouse` | 3 / 3 | 0 / 3 | 3 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route30_MrPokemonsHouse/map.json` |
| `Route36` | 20 / 21 | 5 / 5 |  |  | 3 | 2 / 2 |  | ok | `fontes-mapas/hns/data/maps/Route36/map.json` |
| `TinTower_1F` | 4 / 4 | 4 / 4 |  |  | 3 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/TinTower_1F/map.json` |
| `AzaleaTown_House1` | 3 / 3 | 0 / 2 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/AzaleaTown_House1/map.json` |
| `BlackthornCity_House3` | 2 / 2 | 2 / 2 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/BlackthornCity_House3/map.json` |
| `CianwoodGym` | 5 / 10 | 5 / 5 |  |  |  | 5 / 7 |  | ok | `fontes-mapas/hns/data/maps/CianwoodGym/map.json` |
| `CliffEdgeGate` | 5 / 5 | 1 / 3 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/CliffEdgeGate/map.json` |
| `EcruteakCity_PokemonCenter` | 6 / 6 | 5 / 6 | 1 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/EcruteakCity_PokemonCenter/map.json` |
| `EcruteakCity_SageOffice1` | 3 / 3 | 3 / 3 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/EcruteakCity_SageOffice1/map.json` |
| `Gate_NationalPark` | 8 / 8 | 8 / 8 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Gate_NationalPark/map.json` |
| `GoldenrodCity_BillsHouse` | 3 / 3 | 2 / 3 | 1 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_BillsHouse/map.json` |
| `GoldenrodCity_DepartmentStore_6F` | 4 / 4 | 3 / 4 | 1 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_DepartmentStore_6F/map.json` |
| `GoldenrodCity_RadioTower_1F` | 4 / 6 | 4 / 6 | 2 |  |  | 1 / 1 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_1F/map.json` |
| `GoldenrodCity_RadioTower_5F` | 4 / 6 | 4 / 6 | 2 |  |  | 3 / 3 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_5F/map.json` |
| `GoldenrodCity_UndergroundEntrance` | 2 / 2 | 0 / 2 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_UndergroundEntrance/map.json` |
| `MahoganyTown_Gym` | 7 / 8 | 7 / 7 |  |  |  | 6 / 8 |  | ok | `fontes-mapas/hns/data/maps/MahoganyTown_Gym/map.json` |
| `MtMortar_B1F` | 11 / 11 | 1 / 1 |  |  | 1 | 0 / 1 |  | ok | `fontes-mapas/hns/data/maps/MtMortar_B1F/map.json` |
| `MtSilver_SummitDay` | 1 / 1 | 0 / 1 | 1 |  |  | 0 / 1 |  | ok | `fontes-mapas/hns/data/maps/MtSilver_SummitDay/map.json` |
| `NationalPark_BugContest` | 39 / 53 | 5 / 6 | 1 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/NationalPark_BugContest/map.json` |
| `NewBarkTown` | 9 / 9 | 3 / 3 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/NewBarkTown/map.json` |
| `NewBarkTown_Lab` | 7 / 7 | 2 / 4 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/NewBarkTown_Lab/map.json` |
| `NewBarkTown_PlayersHouse_1F` | 2 / 2 | 1 / 2 | 1 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/NewBarkTown_PlayersHouse_1F/map.json` |
| `OlivineCity_Cafe` | 4 / 4 | 3 / 4 | 1 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/OlivineCity_Cafe/map.json` |
| `OlivineCity_Gym` | 4 / 4 | 4 / 4 |  |  |  | 1 / 3 |  | ok | `fontes-mapas/hns/data/maps/OlivineCity_Gym/map.json` |
| `Route30` | 24 / 24 | 5 / 6 | 1 |  | 1 | 3 / 3 |  | ok | `fontes-mapas/hns/data/maps/Route30/map.json` |
| `Route32` | 35 / 37 | 13 / 13 |  |  | 2 | 8 / 8 |  | ok | `fontes-mapas/hns/data/maps/Route32/map.json` |
| `Route32_PokemonCenter` | 4 / 4 | 4 / 4 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route32_PokemonCenter/map.json` |
| `Route34_DayCare` | 4 / 4 | 2 / 2 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route34_DayCare/map.json` |
| `Route39_Barn` | 7 / 7 | 2 / 2 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route39_Barn/map.json` |
| `Route39_FarmHouse` | 2 / 2 | 2 / 2 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route39_FarmHouse/map.json` |
| `SafariZoneGate` | 17 / 17 | 7 / 7 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/SafariZoneGate/map.json` |
| `SproutTower_3F` | 6 / 11 | 4 / 6 | 2 |  |  | 4 / 4 |  | ok | `fontes-mapas/hns/data/maps/SproutTower_3F/map.json` |
| `TohjoFalls_GiovanniRoom` | 8 / 8 | 0 / 1 | 1 |  |  | 0 / 1 |  | ok | `fontes-mapas/hns/data/maps/TohjoFalls_GiovanniRoom/map.json` |
| `VioletCity` | 56 / 56 | 4 / 6 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/VioletCity/map.json` |
| `VioletCity_PokemonCenter` | 7 / 7 | 6 / 7 | 1 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/VioletCity_PokemonCenter/map.json` |
| `AzaleaTown_PokemonCenter` | 5 / 5 | 5 / 5 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/AzaleaTown_PokemonCenter/map.json` |
| `BellchimeTrail` | 64 / 64 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/BellchimeTrail/map.json` |
| `BlackthornCity_House2` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/BlackthornCity_House2/map.json` |
| `BlackthornCity_PokemonCenter` | 4 / 4 | 4 / 4 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/BlackthornCity_PokemonCenter/map.json` |
| `BurnedTower_B1F` | 3 / 11 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/BurnedTower_B1F/map.json` |
| `CherrygroveCity_House2` | 1 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/CherrygroveCity_House2/map.json` |
| `CherrygroveCity_PokemonCenter` | 5 / 5 | 5 / 5 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/CherrygroveCity_PokemonCenter/map.json` |
| `CianwoodHouse1` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/CianwoodHouse1/map.json` |
| `CianwoodHouse3` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/CianwoodHouse3/map.json` |
| `DarkCave_NorthSide` | 10 / 10 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/DarkCave_NorthSide/map.json` |
| `DiglettsCave_EntranceNorth` | 1 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/DiglettsCave_EntranceNorth/map.json` |
| `DragonsDen_Shrine` | 4 / 4 | 3 / 4 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/DragonsDen_Shrine/map.json` |
| `Gate_MahoganyTown_Route43` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Gate_MahoganyTown_Route43/map.json` |
| `Gate_Route40_TrainerHill_Courtyard` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Gate_Route40_TrainerHill_Courtyard/map.json` |
| `GoldenrodCity_BikeShop` | 2 / 2 | 2 / 2 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_BikeShop/map.json` |
| `GoldenrodCity_GameCorner` | 11 / 11 | 11 / 11 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_GameCorner/map.json` |
| `GoldenrodCity_House1` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_House1/map.json` |
| `GoldenrodCity_PokemonCenter` | 6 / 6 | 6 / 6 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_PokemonCenter/map.json` |
| `GoldenrodCity_TrainStation` | 9 / 9 | 8 / 9 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_TrainStation/map.json` |
| `GoldenrodCity_UndergroundStorage` | 7 / 7 | 4 / 4 |  |  | 1 | 3 / 3 |  | ok | `fontes-mapas/hns/data/maps/GoldenrodCity_UndergroundStorage/map.json` |
| `IcePath_1F` | 11 / 11 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/IcePath_1F/map.json` |
| `LakeOfRage_House1` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/LakeOfRage_House1/map.json` |
| `LakeOfRage_House2` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/LakeOfRage_House2/map.json` |
| `MahoganyTown_PokemonCenter` | 5 / 5 | 5 / 5 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/MahoganyTown_PokemonCenter/map.json` |
| `MahoganyTown_Shop` | 2 / 4 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/MahoganyTown_Shop/map.json` |
| `MtSilver_PokemonCenter` | 3 / 3 | 3 / 3 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/MtSilver_PokemonCenter/map.json` |
| `NationalPark_Normal` | 49 / 49 | 9 / 9 |  |  | 1 | 4 / 4 |  | ok | `fontes-mapas/hns/data/maps/NationalPark_Normal/map.json` |
| `NewBarkTown_House1` | 2 / 2 | 1 / 2 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/NewBarkTown_House1/map.json` |
| `OlivineCity_House1` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/OlivineCity_House1/map.json` |
| `OlivineCity_House3` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/OlivineCity_House3/map.json` |
| `OlivineCity_Lighthouse` | 15 / 18 | 11 / 12 | 1 |  |  | 9 / 9 |  | ok | `fontes-mapas/hns/data/maps/OlivineCity_Lighthouse/map.json` |
| `OlivineCity_PokemonCenter` | 4 / 4 | 4 / 4 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/OlivineCity_PokemonCenter/map.json` |
| `Route26North` | 7 / 7 | 3 / 3 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route26North/map.json` |
| `Route27_House` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route27_House/map.json` |
| `Route28_House` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route28_House/map.json` |
| `Route30_House` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/Route30_House/map.json` |
| `Route31` | 20 / 22 | 4 / 4 |  |  | 1 | 1 / 1 |  | ok | `fontes-mapas/hns/data/maps/Route31/map.json` |
| `Route34` | 33 / 33 | 10 / 10 |  |  | 1 | 9 / 9 |  | ok | `fontes-mapas/hns/data/maps/Route34/map.json` |
| `Route37` | 18 / 18 | 4 / 4 |  |  | 1 | 2 / 2 |  | ok | `fontes-mapas/hns/data/maps/Route37/map.json` |
| `Route39` | 20 / 20 | 6 / 7 | 1 |  |  | 5 / 5 |  | ok | `fontes-mapas/hns/data/maps/Route39/map.json` |
| `Route40` | 20 / 20 | 7 / 7 |  |  | 1 | 4 / 4 |  | ok | `fontes-mapas/hns/data/maps/Route40/map.json` |
| `Route42` | 18 / 19 | 3 / 4 | 1 |  |  | 3 / 3 |  | ok | `fontes-mapas/hns/data/maps/Route42/map.json` |
| `Route47` | 33 / 33 | 6 / 7 | 1 |  |  | 4 / 4 |  | ok | `fontes-mapas/hns/data/maps/Route47/map.json` |
| `RuinsOfAlph_Lab` | 6 / 6 | 3 / 3 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/RuinsOfAlph_Lab/map.json` |
| `RuinsOfAlph_PuzzleAndRewardChambers` | 17 / 17 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/RuinsOfAlph_PuzzleAndRewardChambers/map.json` |
| `SafariZoneGate_PokemonCenter` | 5 / 5 | 5 / 5 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/SafariZoneGate_PokemonCenter/map.json` |
| `SafariZoneGate_SafariZoneEntrance` | 10 / 10 | 10 / 10 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/SafariZoneGate_SafariZoneEntrance/map.json` |
| `SproutTower_1F` | 6 / 9 | 5 / 6 | 1 |  |  | 1 / 1 |  | ok | `fontes-mapas/hns/data/maps/SproutTower_1F/map.json` |
| `SproutTower_2F` | 3 / 7 | 2 / 3 | 1 |  |  | 2 / 2 |  | ok | `fontes-mapas/hns/data/maps/SproutTower_2F/map.json` |
| `UnionCave_B2F` | 12 / 12 | 3 / 4 | 1 |  |  | 3 / 3 |  | ok | `fontes-mapas/hns/data/maps/UnionCave_B2F/map.json` |
| `VioletCity_House1` | 2 / 2 | 2 / 2 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/VioletCity_House1/map.json` |
| `VioletCity_TrainerSchool` | 7 / 7 | 6 / 7 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/hns/data/maps/VioletCity_TrainerSchool/map.json` |

<details><summary>3 mapas nossos sem par na fonte (nativo, renomeado ou de outra fonte)</summary>

- `MahoganyHideout_B1F` (7 pessoas, 7 com fala)
- `MahoganyHideout_B2F` (5 pessoas, 5 com fala)
- `MahoganyHideout_B3F` (8 pessoas, 8 com fala)

</details>

<details><summary>10 mapas que a fonte tem e nós não</summary>

- `CeruleanCave1`
- `CeruleanCave2`
- `CeruleanCave3`
- `SafariZone1`
- `SafariZone2`
- `SafariZone3`
- `SafariZoneIndoor`
- `VictoryRoadKanto_1F`
- `VictoryRoadKanto_B1F`
- `VictoryRoadKanto_B2F`

</details>

## Hoenn (fonte: `fontes-mapas/pokeemerald`)

518 mapas nossos, 518 com par na fonte, 0 sem par, 0 mapas da fonte ausentes aqui.

### Os dois totais, lado a lado

| medida | existe | tem conteúdo | fonte |
|---|---:|---:|---:|
| pessoas | 2276 | 1545 com fala | 2274 (1559 com fala) |
| placas | 533 | 392 com texto | 533 (395 com texto) |
| treinadores | 534 citados por trainerbattle | 533 com time | 537 |
| mapas | 518 | 319 com pelo menos um NPC que fala | 518 |
| encontros | 116 | -- | 116 |

Dos 2276 que existem, **731 não falam**: 569 sem script nenhum (`script: "0"`) e 162 com rótulo que não tem comando de texto (parte é balconista e enfermeira, que chamam loja e cura direto, e parte é NPC pela metade). A fonte tem 715 mudos nos mesmos mapas, então a dívida real é **16**, somada mapa a mapa (o excesso de um mapa não paga a falta de outro).

Objetos que NÃO são gente (item ball, árvore, pedra, mobília): **502 aqui contra 502 na fonte**. Esta linha importa porque `completude.py` conta objeto e não gente: quando o total de objetos bate com a fonte e o de pessoas não, o que aconteceu foi troca de sprite, não falta de objeto. É o caso de Johto, onde o importador pôs `OBJ_EVENT_GFX_ITEM_BALL` com `script: "0"` na coordenada exata de cada NPC da fonte (conferido à mão em `EcruteakCity`, 49 objetos dos dois lados e 49 item balls aqui).

### Mapa a mapa (só os que divergem da fonte)

Toda coluna de lacuna é medida CONTRA A FONTE, nunca contra o ideal. Mapa igual à fonte não aparece aqui, mesmo cheio de NPC mudo: o pokeemerald vanilla também tem, e reprovar o jogo original é a lição 4.10 do `ESTADO.md`.

| mapa | objetos | pessoas | falta | excesso | mudo a mais | treinador | placa genérica a mais | encontro | arquivo da fonte |
|---|---:|---:|---:|---:|---:|---:|---:|:-:|---|
| `Route117` | 26 / 24 | 20 / 18 |  | 2 | 2 | 9 / 9 |  | ok | `fontes-mapas/pokeemerald/data/maps/Route117/map.json` |
| `LilycoveCity_ContestLobby` | 25 / 25 | 25 / 25 |  |  |  | 0 / 0 | 3 | ok | `fontes-mapas/pokeemerald/data/maps/LilycoveCity_ContestLobby/map.json` |
| `MossdeepCity_SpaceCenter_2F` | 9 / 9 | 9 / 9 |  |  |  | 3 / 5 |  | ok | `fontes-mapas/pokeemerald/data/maps/MossdeepCity_SpaceCenter_2F/map.json` |
| `BattleFrontier_BattlePyramidFloor` | 16 / 16 | 16 / 16 |  |  |  | 0 / 1 |  | ok | `fontes-mapas/pokeemerald/data/maps/BattleFrontier_BattlePyramidFloor/map.json` |
| `BattleFrontier_Lounge6` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/BattleFrontier_Lounge6/map.json` |
| `FallarborTown_Mart` | 5 / 5 | 5 / 5 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/FallarborTown_Mart/map.json` |
| `FortreeCity_House1` | 3 / 3 | 3 / 3 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/FortreeCity_House1/map.json` |
| `FortreeCity_House2` | 2 / 2 | 2 / 2 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/FortreeCity_House2/map.json` |
| `LavaridgeTown_Gym_1F` | 6 / 6 | 6 / 6 |  |  |  | 1 / 2 |  | ok | `fontes-mapas/pokeemerald/data/maps/LavaridgeTown_Gym_1F/map.json` |
| `LavaridgeTown_House` | 3 / 3 | 3 / 3 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/LavaridgeTown_House/map.json` |
| `LilycoveCity_DepartmentStoreRooftop` | 4 / 4 | 4 / 4 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/LilycoveCity_DepartmentStoreRooftop/map.json` |
| `MauvilleCity` | 11 / 11 | 10 / 10 |  |  | 1 | 1 / 1 |  | ok | `fontes-mapas/pokeemerald/data/maps/MauvilleCity/map.json` |
| `MossdeepCity` | 17 / 17 | 16 / 16 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/MossdeepCity/map.json` |
| `PacifidlogTown_House3` | 2 / 2 | 2 / 2 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/PacifidlogTown_House3/map.json` |
| `PacifidlogTown_PokemonCenter_1F` | 5 / 5 | 5 / 5 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/PacifidlogTown_PokemonCenter_1F/map.json` |
| `RustboroCity_House1` | 2 / 2 | 2 / 2 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/RustboroCity_House1/map.json` |
| `SlateportCity_PokemonFanClub` | 9 / 9 | 9 / 9 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/SlateportCity_PokemonFanClub/map.json` |
| `SootopolisCity_PokemonCenter_1F` | 4 / 4 | 4 / 4 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/SootopolisCity_PokemonCenter_1F/map.json` |
| `VerdanturfTown_PokemonCenter_1F` | 4 / 4 | 4 / 4 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeemerald/data/maps/VerdanturfTown_PokemonCenter_1F/map.json` |

## Sinnoh (fonte: `fontes-mapas/pokeplatinum`)

433 mapas nossos, 432 com par na fonte, 1 sem par, 162 mapas da fonte ausentes aqui.

### Os dois totais, lado a lado

| medida | existe | tem conteúdo | fonte |
|---|---:|---:|---:|
| pessoas | 1689 | 1285 com fala | 1739 (1369 com fala) |
| placas | 598 | 505 com texto | 565 (516 com texto) |
| treinadores | 395 citados por trainerbattle | 395 com time | 393 |
| mapas | 433 | 308 com pelo menos um NPC que fala | 594 |
| encontros | 128 | -- | 128 |

Dos 1689 que existem, **404 não falam**: 404 sem script nenhum (`script: "0"`) e 0 com rótulo que não tem comando de texto (parte é balconista e enfermeira, que chamam loja e cura direto, e parte é NPC pela metade). A fonte tem 370 mudos nos mesmos mapas, então a dívida real é **209**, somada mapa a mapa (o excesso de um mapa não paga a falta de outro).

Objetos que NÃO são gente (item ball, árvore, pedra, mobília): **4 aqui contra 991 na fonte**. Esta linha importa porque `completude.py` conta objeto e não gente: quando o total de objetos bate com a fonte e o de pessoas não, o que aconteceu foi troca de sprite, não falta de objeto. É o caso de Johto, onde o importador pôs `OBJ_EVENT_GFX_ITEM_BALL` com `script: "0"` na coordenada exata de cada NPC da fonte (conferido à mão em `EcruteakCity`, 49 objetos dos dois lados e 49 item balls aqui).

### Mapa a mapa (só os que divergem da fonte)

Toda coluna de lacuna é medida CONTRA A FONTE, nunca contra o ideal. Mapa igual à fonte não aparece aqui, mesmo cheio de NPC mudo: o pokeemerald vanilla também tem, e reprovar o jogo original é a lição 4.10 do `ESTADO.md`.

| mapa | objetos | pessoas | falta | excesso | mudo a mais | treinador | placa genérica a mais | encontro | arquivo da fonte |
|---|---:|---:|---:|---:|---:|---:|---:|:-:|---|
| `LakeValorDrained` | 3 / 30 | 3 / 29 | 26 |  | 3 | 0 / 3 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_lake_valor_drained.json` |
| `Route223` | 26 / 18 | 26 / 14 |  | 12 | 12 | 13 / 13 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_223.json` |
| `Route222` | 23 / 32 | 23 / 14 |  | 9 | 10 | 11 / 11 | 4 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_222.json` |
| `Restaurant` | 1 / 19 | 1 / 19 | 18 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_restaurant.json` |
| `Route206` | 19 / 24 | 19 / 10 |  | 9 | 9 | 9 / 9 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_206.json` |
| `Route210_North` | 21 / 26 | 21 / 12 |  | 9 | 9 | 10 / 10 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_210_north.json` |
| `Route214` | 18 / 28 | 18 / 9 |  | 9 | 9 | 9 / 9 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_214.json` |
| `Route216` | 18 / 17 | 18 / 9 |  | 9 | 9 | 9 / 9 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_216.json` |
| `EternaForest` | 20 / 25 | 20 / 11 |  | 9 | 7 | 8 / 8 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_eterna_forest.json` |
| `Route217` | 19 / 19 | 19 / 11 |  | 8 | 8 | 9 / 9 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_217.json` |
| `Route225` | 16 / 31 | 16 / 8 |  | 8 | 8 | 8 / 8 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_225.json` |
| `Route228` | 16 / 27 | 16 / 8 |  | 8 | 8 | 8 / 8 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_228.json` |
| `Villa` | 0 / 17 | 0 / 16 | 16 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_villa.json` |
| `Route213` | 21 / 34 | 21 / 14 |  | 7 | 8 | 9 / 9 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_213.json` |
| `CanalaveCity_Gym` | 1 / 9 | 1 / 9 | 8 |  |  | 1 / 7 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_canalave_city_gym.json` |
| `GameCorner` | 8 / 9 | 8 / 9 | 1 |  |  | 0 / 0 | 13 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_game_corner.json` |
| `Route208` | 15 / 24 | 15 / 8 |  | 7 | 7 | 7 / 7 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_208.json` |
| `Route220` | 14 / 10 | 14 / 7 |  | 7 | 7 | 7 / 7 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_220.json` |
| `GalacticHQ_Hall` | 6 / 36 | 6 / 18 | 12 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_galactic_hq_hall.json` |
| `JubilifeTv2FGallery` | 3 / 3 | 3 / 3 |  |  | 1 | 0 / 0 | 11 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_tv_2f_gallery.json` |
| `Route224` | 16 / 22 | 16 / 11 |  | 5 | 7 | 8 / 8 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_224.json` |
| `Route207` | 13 / 27 | 13 / 8 |  | 5 | 5 | 6 / 6 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_207.json` |
| `Route215` | 15 / 29 | 15 / 11 |  | 4 | 6 | 8 / 8 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_215.json` |
| `Route221` | 12 / 17 | 12 / 8 |  | 4 | 6 | 6 / 6 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_221.json` |
| `Route230` | 12 / 19 | 12 / 8 |  | 4 | 6 | 6 / 6 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_230.json` |
| `FightArea` | 12 / 32 | 12 / 21 | 9 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_fight_area.json` |
| `GalacticHQ_2F` | 5 / 7 | 4 / 4 |  |  |  | 3 / 4 | 8 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_galactic_hq_2f.json` |
| `GalacticHQ_Laboratory` | 2 / 3 | 2 / 2 |  |  |  | 0 / 0 | 9 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_galactic_hq_laboratory.json` |
| `Route205_North` | 10 / 12 | 10 / 4 |  | 6 | 3 | 3 / 3 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_205_north.json` |
| `Route210_South` | 11 / 31 | 11 / 19 | 8 |  |  | 8 / 9 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_210_south.json` |
| `StarkMountainRoom3` | 0 / 11 | 0 / 9 | 9 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_stark_mountain_room_3.json` |
| `ValleyWindworksBuilding` | 1 / 8 | 1 / 8 | 7 |  |  | 0 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_valley_windworks_building.json` |
| `ContestHallLobby` | 7 / 11 | 7 / 11 | 4 |  |  | 0 / 0 | 4 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_contest_hall_lobby.json` |
| `Route203` | 11 / 15 | 11 / 7 |  | 4 | 4 | 5 / 5 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_203.json` |
| `Route211_East` | 9 / 22 | 9 / 5 |  | 4 | 4 | 4 / 4 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_211_east.json` |
| `Route226` | 10 / 16 | 10 / 6 |  | 4 | 4 | 5 / 5 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_226.json` |
| `Route229` | 9 / 19 | 9 / 5 |  | 4 | 4 | 4 / 4 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_229.json` |
| `MtCoronet1FTunnelRoom` | 0 / 17 | 0 / 4 | 4 |  |  | 0 / 3 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_mt_coronet_1f_tunnel_room.json` |
| `OreburghMine_B2F` | 7 / 11 | 7 / 7 |  |  | 5 | 0 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_mine_b2f.json` |
| `Route209` | 16 / 33 | 16 / 14 |  | 2 | 5 | 8 / 8 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_209.json` |
| `JubilifeCity` | 15 / 33 | 15 / 21 | 6 |  |  | 2 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_city.json` |
| `LakeVerityLowWater` | 0 / 7 | 0 / 6 | 6 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_lake_verity_low_water.json` |
| `RotomsRoom` | 0 / 8 | 0 / 6 | 6 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_rotoms_room.json` |
| `Route218` | 8 / 21 | 8 / 10 | 2 |  | 4 | 4 / 4 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_218.json` |
| `StarkMountainOutside` | 0 / 8 | 0 / 5 | 5 |  |  | 0 / 1 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_stark_mountain_outside.json` |
| `AcuityLakefront` | 6 / 4 | 6 / 1 |  | 5 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_acuity_lakefront.json` |
| `Battleground` | 1 / 6 | 1 / 6 | 5 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_battleground.json` |
| `LakeValor` | 5 / 1 | 5 / 0 |  | 5 |  | 3 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_lake_valor.json` |
| `MtCoronet_1F_South` | 6 / 7 | 6 / 1 |  | 5 |  | 2 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_mt_coronet_1f_south.json` |
| `ResortArea` | 6 / 19 | 6 / 11 | 5 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_resort_area.json` |
| `SandgemTown_RowanLab` | 8 / 5 | 5 / 5 |  |  |  | 0 / 0 | 5 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sandgem_town_pokemon_research_lab.json` |
| `StarkMountainRoom1` | 0 / 17 | 0 / 5 | 5 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_stark_mountain_room_1.json` |
| `TeamGalacticEternaBuilding_1F` | 3 / 7 | 3 / 6 | 3 |  |  | 0 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_team_galactic_eterna_building_1f.json` |
| `CanalaveCity` | 8 / 19 | 8 / 12 | 4 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_canalave_city.json` |
| `HearthomeCity` | 19 / 36 | 19 / 23 | 4 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_hearthome_city.json` |
| `HotelGrandLake` | 7 / 3 | 7 / 3 |  | 4 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_grand_lake_route_213_lobby.json` |
| `MtCoronet3F` | 0 / 2 | 0 / 2 | 2 |  |  | 0 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_mt_coronet_3f.json` |
| `MtCoronet4FRooms1And2` | 0 / 10 | 0 / 2 | 2 |  |  | 0 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_mt_coronet_4f_rooms_1_and_2.json` |
| `MtCoronet5F` | 0 / 2 | 0 / 2 | 2 |  |  | 0 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_mt_coronet_5f.json` |
| `Route201` | 4 / 13 | 4 / 8 | 4 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_201.json` |
| `Route202` | 7 / 9 | 7 / 5 |  | 2 | 2 | 3 / 3 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_202.json` |
| `Route205_South` | 9 / 32 | 9 / 13 | 4 |  |  | 8 / 8 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_205_south.json` |
| `Route212_North` | 14 / 30 | 14 / 14 |  |  | 4 | 8 / 8 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_212_north.json` |
| `Route219` | 4 / 4 | 4 / 2 |  | 2 | 2 | 2 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_219.json` |
| `SinnohLeague_Entrance` | 4 / 2 | 4 / 0 |  | 4 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pokemon_league.json` |
| `ValorLakefront` | 4 / 12 | 4 / 8 | 4 |  |  | 1 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_valor_lakefront.json` |
| `VeilstoneCity` | 13 / 30 | 13 / 17 | 4 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_city.json` |
| `CanalaveLibrary3F` | 2 / 5 | 2 / 5 | 3 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_canalave_library_3f.json` |
| `CelesticTown` | 3 / 12 | 3 / 6 | 3 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_celestic_town.json` |
| `FloaromaTwon_PokemonCenter_2F` | 6 / 3 | 6 / 3 |  | 3 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_floaroma_town_pokecenter_2f.json` |
| `GalacticHQ_1F` | 9 / 11 | 9 / 7 |  | 2 |  | 1 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_galactic_hq_1f.json` |
| `GalacticHQ_ControlRoom` | 2 / 5 | 2 / 5 | 3 |  |  | 1 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_galactic_hq_control_room.json` |
| `HearthomeCity_Gym` | 2 / 1 | 2 / 1 |  | 1 |  | 1 / 0 | 2 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_hearthome_city_gym_entrance_room.json` |
| `IronIslandB2FLeftRoom` | 8 / 17 | 8 / 11 | 3 |  |  | 8 / 8 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_iron_island_b2f_left_room.json` |
| `JubilifeCity_PokemonCenter_2F` | 6 / 3 | 6 / 3 |  | 3 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_city_pokecenter_2f.json` |
| `MtCoronet_B1F` | 3 / 24 | 3 / 0 |  | 3 |  | 1 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_mt_coronet_b1f.json` |
| `OreburghCity` | 18 / 28 | 18 / 16 |  | 2 | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city.json` |
| `OreburghCity_Flat1_F2` | 7 / 4 | 7 / 4 |  | 3 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_northwest_house_2f.json` |
| `OreburghCity_Flat3_F2` | 6 / 3 | 6 / 3 |  | 3 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_east_house_2f.json` |
| `OreburghCity_Gym` | 5 / 4 | 5 / 4 |  | 1 |  | 3 / 2 | 2 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_gym.json` |
| `OreburghCity_PokemonCenter_2F` | 6 / 3 | 6 / 3 |  | 3 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_pokecenter_2f.json` |
| `PokmonLeague` | 3 / 2 | 3 / 0 |  | 3 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pokemon_league.json` |
| `RavagedPath` | 3 / 31 | 3 / 0 |  | 3 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_ravaged_path.json` |
| `Route212_South` | 14 / 44 | 14 / 16 | 2 |  |  | 11 / 12 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_212_south.json` |
| `Route227` | 8 / 13 | 8 / 7 |  | 1 | 2 | 4 / 4 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_227.json` |
| `SolaceonTown` | 8 / 21 | 8 / 11 | 3 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_solaceon_town.json` |
| `TeamGalacticEternaBuilding_3F` | 1 / 4 | 1 / 3 | 2 |  |  | 1 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_team_galactic_eterna_building_3f.json` |
| `TwinleafTown_Haouse1` | 3 / 1 | 3 / 1 |  | 2 | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_twinleaf_town_northeast_house.json` |
| `TwinleafTown_MainHouse_1F` | 2 / 2 | 2 / 2 |  |  | 1 | 0 / 0 | 2 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_twinleaf_town_player_house_1f.json` |
| `EternaCity` | 13 / 34 | 13 / 15 | 2 |  |  | 2 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_eterna_city.json` |
| `EternaCityPokecenter1F` | 5 / 7 | 5 / 7 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_eterna_city_pokecenter_1f.json` |
| `EternaCity_Gym` | 5 / 5 | 5 / 5 |  |  |  | 1 / 0 | 2 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_eterna_city_gym.json` |
| `FloaromaTown_House1` | 4 / 2 | 4 / 2 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_floaroma_town_southeast_house.json` |
| `GalacticHq4F` | 0 / 5 | 0 / 1 | 1 |  |  | 0 / 0 | 1 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_galactic_hq_4f.json` |
| `HearthomeCityPokemonFanClub` | 4 / 6 | 4 / 6 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_hearthome_city_pokemon_fan_club.json` |
| `IronIsland` | 0 / 2 | 0 / 2 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_iron_island.json` |
| `JubilifeCity_JubilifeTV_F1` | 7 / 5 | 7 / 5 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_tv_1f.json` |
| `JubilifeCity_JubilifeTV_F4` | 5 / 3 | 5 / 3 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_tv_4f.json` |
| `JubilifeCity_PokemonCenter_1F` | 5 / 7 | 5 / 7 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_city_pokecenter_1f.json` |
| `JubilifeCity_PokemonSchool` | 9 / 9 | 9 / 7 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_trainers_school.json` |
| `JubilifeCity_PoketchCompany_F1` | 3 / 5 | 3 / 5 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_poketch_co_1f.json` |
| `JubilifeTvElevator` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 | 1 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_tv_elevator.json` |
| `LakeVerity` | 6 / 9 | 6 / 8 | 2 |  |  | 4 / 4 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_lake_verity.json` |
| `MtCoronet6F` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 1 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_mt_coronet_6f.json` |
| `OreburghCity_Flat1_F1` | 5 / 3 | 5 / 3 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_northwest_house_1f.json` |
| `OreburghCity_Flat2_F1` | 5 / 3 | 5 / 3 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_north_house_1f.json` |
| `OreburghCity_Flat3_F1` | 5 / 3 | 5 / 3 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_east_house_1f.json` |
| `OreburghCity_House3` | 3 / 1 | 3 / 1 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_south_house.json` |
| `OreburghGate_1F` | 5 / 11 | 5 / 3 |  | 2 |  | 2 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_gate_1f.json` |
| `PalParkLobby` | 8 / 9 | 8 / 9 | 1 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pal_park_lobby.json` |
| `PastoriaCity` | 13 / 29 | 13 / 15 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pastoria_city.json` |
| `PastoriaCity_Gym` | 8 / 8 | 8 / 8 |  |  |  | 7 / 6 | 2 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pastoria_city_gym.json` |
| `PokemonMansion` | 5 / 7 | 5 / 7 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pokemon_mansion.json` |
| `PokemonMansionOffice` | 2 / 4 | 2 / 3 | 1 |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pokemon_mansion_office.json` |
| `ResortAreaRibbonSyndicate1F` | 6 / 6 | 6 / 6 |  |  | 2 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_resort_area_ribbon_syndicate_1f.json` |
| `Route204` | 7 / 10 | 7 / 5 |  | 2 |  | 5 / 3 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_204_south.json` |
| `Route212_Access` | 2 / 4 | 2 / 4 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_212_gate_to_hearthome_city.json` |
| `SandgemTown` | 5 / 15 | 5 / 7 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sandgem_town.json` |
| `SandgemTown_PokemonCenter_2F` | 6 / 4 | 6 / 4 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sandgem_town_pokecenter_2f.json` |
| `SandgemTown_RivalHouse_F1` | 3 / 2 | 3 / 2 |  | 1 | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sandgem_town_counterpart_house_1f.json` |
| `SinnohLeague_HallOfFame` | 0 / 2 | 0 / 2 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pokemon_league_hall_of_fame.json` |
| `SnowpointCity` | 7 / 12 | 7 / 9 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_snowpoint_city.json` |
| `SnowpointCityPokecenter1F` | 5 / 7 | 5 / 7 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_snowpoint_city_pokecenter_1f.json` |
| `SnowpointCity_Gym` | 8 / 27 | 8 / 8 |  |  |  | 7 / 6 | 2 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_snowpoint_city_gym.json` |
| `SpearPillar` | 4 / 6 | 4 / 6 | 2 |  |  | 3 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_spear_pillar.json` |
| `SpearPillar_Distorted` | 4 / 6 | 4 / 6 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_spear_pillar_distorted.json` |
| `SunyshoreMarket` | 6 / 5 | 6 / 5 |  | 1 | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sunyshore_market.json` |
| `SurvivalArea` | 4 / 12 | 4 / 6 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_survival_area.json` |
| `TeamGalacticEternaBuilding_2F` | 2 / 5 | 2 / 4 | 2 |  |  | 2 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_team_galactic_eterna_building_2f.json` |
| `TeamGalacticEternaBuilding_4F` | 2 / 7 | 2 / 4 | 2 |  |  | 1 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_team_galactic_eterna_building_4f.json` |
| `Twinleaf_Town_RivalsHouse_F1` | 2 / 1 | 2 / 1 |  | 1 | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_twinleaf_town_rival_house_1f.json` |
| `ValleyWindworks` | 5 / 8 | 5 / 3 |  | 2 |  | 3 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_valley_windworks_outside.json` |
| `ValorCavern` | 0 / 2 | 0 / 2 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_valor_cavern.json` |
| `VeilstoneCity_Gym` | 6 / 6 | 6 / 6 |  |  |  | 5 / 4 | 2 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_city_gym.json` |
| `VerityCavern` | 0 / 2 | 0 / 2 | 2 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_verity_cavern.json` |
| `VerityLakefront` | 2 / 1 | 2 / 0 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_verity_lakefront.json` |
| `AcuityCavern` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_acuity_cavern.json` |
| `CanalaveCityHarborInn` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_canalave_city_harbor_inn.json` |
| `CanalaveCityPokecenter1F` | 6 / 7 | 6 / 7 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_canalave_city_pokecenter_1f.json` |
| `CanalaveCitySailorEldritchHouse` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_canalave_city_sailor_eldritch_house.json` |
| `CanalaveCityWestHouse` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_canalave_city_west_house.json` |
| `CanalaveLibrary1F` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_canalave_library_1f.json` |
| `CanalaveLibrary2F` | 1 / 2 | 1 / 2 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_canalave_library_2f.json` |
| `CelesticTownNorthHouse` | 2 / 4 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_celestic_town_north_house.json` |
| `CelesticTownPokecenter1F` | 5 / 6 | 5 / 6 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_celestic_town_pokecenter_1f.json` |
| `CelesticTownSouthwestHouse` | 1 / 2 | 1 / 2 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_celestic_town_southwest_house.json` |
| `CycleShop` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_cycle_shop.json` |
| `EternaCityHerbShop` | 4 / 3 | 4 / 3 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_eterna_city_herb_shop.json` |
| `EternaCitySouthHouse` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_eterna_city_south_house.json` |
| `FightAreaPokecenter1F` | 5 / 6 | 5 / 6 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_fight_area_pokecenter_1f.json` |
| `FightAreaSouthHouse` | 3 / 4 | 3 / 4 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_fight_area_south_house.json` |
| `FloaromaTown` | 7 / 13 | 7 / 8 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_floaroma_town.json` |
| `FloaromaTown_House2` | 4 / 3 | 4 / 3 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_floaroma_town_middle_house.json` |
| `FloaromaTown_PokemonCenter_1F` | 5 / 6 | 5 / 6 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_floaroma_town_pokecenter_1f.json` |
| `FootstepHouse` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_footstep_house.json` |
| `GalacticHQ_B2F` | 3 / 9 | 3 / 4 | 1 |  |  | 2 / 2 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_galactic_hq_b2f.json` |
| `GlobalTerminal1F` | 14 / 14 | 14 / 14 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_global_terminal_1f.json` |
| `GrandLakeValorLakefrontEastHouse` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_grand_lake_valor_lakefront_east_house.json` |
| `GrandLakeValorLakefrontWestHouse` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_grand_lake_valor_lakefront_west_house.json` |
| `HearthomeCityEastGateToAmitySquare` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_hearthome_city_east_gate_to_amity_square.json` |
| `HearthomeCityGymLeaderRoom` | 0 / 3 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_hearthome_city_gym_leader_room.json` |
| `HearthomeCityPokecenter1F` | 5 / 6 | 5 / 6 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_hearthome_city_pokecenter_1f.json` |
| `HearthomeCitySoutheastHouse1F` | 3 / 4 | 3 / 4 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_hearthome_city_southeast_house_1f.json` |
| `HearthomeCityWestGateToAmitySquare` | 3 / 4 | 3 / 4 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_hearthome_city_west_gate_to_amity_square.json` |
| `JubilifeCity_Flat1_F1` | 4 / 4 | 4 / 4 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_city_condominiums_1f.json` |
| `JubilifeCity_Flat2_F1` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_city_south_house_1f.json` |
| `JubilifeCity_Flat2_F2` | 4 / 3 | 4 / 3 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_city_south_house_2f.json` |
| `JubilifeCity_Flat3_F1` | 4 / 3 | 4 / 3 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_city_southwest_house_1f.json` |
| `JubilifeCity_JubilifeTV_F2` | 5 / 4 | 5 / 4 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_tv_2f.json` |
| `JubilifeCity_PoketchCompany_F2` | 3 / 4 | 3 / 4 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_poketch_co_2f.json` |
| `JubilifeTv3FGroupRankingRoom` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_jubilife_tv_3f_group_ranking_room.json` |
| `LakeAcuityLowWater` | 0 / 2 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_lake_acuity_low_water.json` |
| `MtCoronet2F` | 0 / 9 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_mt_coronet_2f.json` |
| `MtCoronet_1F_North_Room1` | 4 / 19 | 4 / 3 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_mt_coronet_1f_north_room_1.json` |
| `OldChateauBackMiddleEastRoom` | 0 / 2 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_old_chateau_back_middle_east_room.json` |
| `OldChateauDiningArea` | 0 / 3 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_old_chateau_dining_area.json` |
| `OreburghCity_Flat2_F2` | 4 / 3 | 4 / 3 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_north_house_2f.json` |
| `OreburghCity_House1` | 3 / 2 | 3 / 2 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_middle_house.json` |
| `OreburghCity_PokemonCenter_1F` | 8 / 9 | 8 / 9 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_city_pokecenter_1f.json` |
| `OreburghMine_B1F` | 4 / 4 | 4 / 3 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_oreburgh_mine_b1f.json` |
| `PastoriaCityNortheastHouse` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pastoria_city_northeast_house.json` |
| `PastoriaCityPokecenter1F` | 4 / 5 | 4 / 5 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pastoria_city_pokecenter_1f.json` |
| `PoffinHouse` | 5 / 6 | 5 / 6 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_poffin_house.json` |
| `PokemonDayCare` | 1 / 2 | 1 / 2 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pokemon_day_care.json` |
| `PokemonLeagueSouthPokecenter1F` | 4 / 3 | 4 / 3 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_pokemon_league_south_pokecenter_1f.json` |
| `ResortAreaHouse` | 3 / 3 | 3 / 3 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_resort_area_house.json` |
| `ResortAreaPokecenter1F` | 4 / 5 | 4 / 5 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_resort_area_pokecenter_1f.json` |
| `ResortAreaRibbonSyndicateElevator` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_resort_area_ribbon_syndicate_elevator.json` |
| `Route206_North` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_206_cycling_road_north_gate.json` |
| `Route209_Access` | 1 / 2 | 1 / 2 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_209_gate_to_hearthome_city.json` |
| `Route214_Access` | 1 / 2 | 1 / 2 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_214_gate_to_veilstone_city.json` |
| `Route217NortheastHouse` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_217_northeast_house.json` |
| `Route218_West` | 1 / 2 | 1 / 2 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_218_gate_to_canalave_city.json` |
| `Route221House` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_221_house.json` |
| `Route228NorthHouse` | 1 / 1 | 1 / 1 |  |  |  | 0 / 0 | 1 | ok | `fontes-mapas/pokeplatinum/res/field/events/events_route_228_north_house.json` |
| `SendoffSpring` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sendoff_spring.json` |
| `SinnohVictoryRoad1F` | 6 / 12 | 6 / 7 | 1 |  |  | 6 / 6 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_victory_road_1f.json` |
| `SnowpointTempleB5F` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_snowpoint_temple_b5f.json` |
| `SolaceonTownNortheastHouse` | 2 / 2 | 2 / 2 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_solaceon_town_northeast_house.json` |
| `SolaceonTownPokecenter1F` | 5 / 6 | 5 / 6 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_solaceon_town_pokecenter_1f.json` |
| `StarkMountainRoom2` | 16 / 31 | 16 / 17 | 1 |  |  | 16 / 16 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_stark_mountain_room_2.json` |
| `SunyshoreCity` | 7 / 21 | 7 / 8 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sunyshore_city.json` |
| `SunyshoreCityGymRoom3` | 4 / 5 | 4 / 5 | 1 |  |  | 4 / 4 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sunyshore_city_gym_room_3.json` |
| `SunyshoreCityPokecenter1F` | 5 / 6 | 5 / 6 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sunyshore_city_pokecenter_1f.json` |
| `SunyshoreCity_Gym` | 3 / 2 | 3 / 2 |  | 1 |  | 2 / 1 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_sunyshore_city_gym_room_1.json` |
| `SurvivalAreaPokecenter1F` | 5 / 4 | 5 / 4 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_survival_area_pokecenter_1f.json` |
| `TwinleafTown` | 5 / 8 | 5 / 4 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_twinleaf_town.json` |
| `TwinleafTown_House2` | 3 / 2 | 3 / 2 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_twinleaf_town_southwest_house.json` |
| `TwinleafTown_MainHouse_2F` | 0 / 1 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_twinleaf_town_player_house_2f.json` |
| `UnusedJubilifeCityCondominiums4F` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_unused_jubilife_city_condominiums_4f.json` |
| `UnusedOreburghCityNorthwestHouse3F` | 2 / 2 | 2 / 2 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_unused_oreburgh_city_northwest_house_3f.json` |
| `VeilstoneCityNorthwestHouse` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_city_northwest_house.json` |
| `VeilstoneCityPokecenter1F` | 4 / 5 | 4 / 5 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_city_pokecenter_1f.json` |
| `VeilstoneCityPrizeExchange` | 4 / 3 | 4 / 3 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_city_prize_exchange.json` |
| `VeilstoneCitySouthwestHouse` | 2 / 3 | 2 / 3 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_city_southwest_house.json` |
| `VeilstoneStore1F` | 7 / 6 | 7 / 6 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_store_1f.json` |
| `VeilstoneStore2F` | 8 / 7 | 8 / 7 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_store_2f.json` |
| `VeilstoneStore3F` | 7 / 6 | 7 / 6 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_store_3f.json` |
| `VeilstoneStore4F` | 7 / 6 | 7 / 6 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_store_4f.json` |
| `VeilstoneStore5F` | 5 / 4 | 5 / 4 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_store_5f.json` |
| `VeilstoneStoreElevator` | 1 / 1 | 1 / 1 |  |  | 1 | 0 / 0 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_veilstone_store_elevator.json` |
| `VictoryRoad1FRoom2` | 14 / 29 | 14 / 15 | 1 |  |  | 14 / 14 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_victory_road_1f_room_2.json` |
| `WaywardCave1F` | 10 / 26 | 10 / 11 | 1 |  |  | 10 / 10 |  | ok | `fontes-mapas/pokeplatinum/res/field/events/events_wayward_cave_1f.json` |

<details><summary>1 mapas nossos sem par na fonte (nativo, renomeado ou de outra fonte)</summary>

- `JubilifeCity_Flat3_F3` (2 pessoas, 2 com fala)

</details>

<details><summary>162 mapas que a fonte tem e nós não</summary>

- `MAP_HEADER_AMITY_SQUARE`
- `MAP_HEADER_BATTLE_ARCADE`
- `MAP_HEADER_BATTLE_CASTLE`
- `MAP_HEADER_BATTLE_FACTORY`
- `MAP_HEADER_BATTLE_FRONTIER`
- `MAP_HEADER_BATTLE_HALL`
- `MAP_HEADER_BATTLE_TOWER`
- `MAP_HEADER_BATTLE_TOWER_BATTLE_ROOM`
- `MAP_HEADER_BATTLE_TOWER_BATTLE_SALON`
- `MAP_HEADER_BATTLE_TOWER_CORRIDOR`
- `MAP_HEADER_BATTLE_TOWER_CORRIDOR_MULTI`
- `MAP_HEADER_BATTLE_TOWER_ELEVATOR`
- `MAP_HEADER_BATTLE_TOWER_MULTI_BATTLE_ROOM`
- `MAP_HEADER_CELESTIC_TOWN_CAVE`
- `MAP_HEADER_COMMUNICATION_CLUB_COLOSSEUM_2P`
- `MAP_HEADER_COMMUNICATION_CLUB_COLOSSEUM_4P`
- `MAP_HEADER_CONTEST_HALL_STAGE_ONGOING_CONTEST`
- `MAP_HEADER_DISTORTION_WORLD_1F`
- `MAP_HEADER_DISTORTION_WORLD_B1F`
- `MAP_HEADER_DISTORTION_WORLD_B2F`
- `MAP_HEADER_DISTORTION_WORLD_B3F`
- `MAP_HEADER_DISTORTION_WORLD_B4F`
- `MAP_HEADER_DISTORTION_WORLD_B5F`
- `MAP_HEADER_DISTORTION_WORLD_B6F`
- `MAP_HEADER_DISTORTION_WORLD_B7F`
- `MAP_HEADER_DISTORTION_WORLD_GIRATINA_ROOM`
- `MAP_HEADER_DISTORTION_WORLD_TURNBACK_CAVE_ROOM`
- `MAP_HEADER_ETERNA_CITY_DP_GYM`
- `MAP_HEADER_ETERNA_FOREST_OUTSIDE`
- `MAP_HEADER_EVERYWHERE`
- `MAP_HEADER_FLOAROMA_MEADOW`
- `MAP_HEADER_FLOAROMA_MEADOW_HOUSE`
- `MAP_HEADER_FLOWER_PARADISE`
- `MAP_HEADER_FUEGO_IRONWORKS_BUILDING`
- `MAP_HEADER_FUEGO_IRONWORKS_OUTSIDE`
- `MAP_HEADER_FULLMOON_ISLAND`
- `MAP_HEADER_FULLMOON_ISLAND_FOREST`
- `MAP_HEADER_GREAT_MARSH_1`
- `MAP_HEADER_GREAT_MARSH_2`
- `MAP_HEADER_GREAT_MARSH_3`
- `MAP_HEADER_GREAT_MARSH_4`
- `MAP_HEADER_GREAT_MARSH_5`
- `MAP_HEADER_GREAT_MARSH_6`
- `MAP_HEADER_HALL_OF_ORIGIN`
- `MAP_HEADER_HEARTHOME_CITY_DP_GYM_ELEVATOR_ROOM_1`
- `MAP_HEADER_HEARTHOME_CITY_DP_GYM_ELEVATOR_ROOM_2`
- `MAP_HEADER_HEARTHOME_CITY_DP_GYM_LEADER_ROOM`
- `MAP_HEADER_HEARTHOME_CITY_DP_GYM_TRAINER_ROOM_1`
- `MAP_HEADER_HEARTHOME_CITY_DP_GYM_TRAINER_ROOM_2`
- `MAP_HEADER_HEARTHOME_CITY_DP_GYM_TRAINER_ROOM_3`
- `MAP_HEADER_HEARTHOME_CITY_DP_GYM_TRAINER_ROOM_4`
- `MAP_HEADER_HEARTHOME_CITY_DP_GYM_TRAINER_ROOM_5`
- `MAP_HEADER_HEARTHOME_CITY_DP_GYM_TRAINER_ROOM_6`
- `MAP_HEADER_HEARTHOME_CITY_GYM_TRAINER_ROOM_1`
- `MAP_HEADER_HEARTHOME_CITY_NORTHEAST_HOUSE_2F`
- `MAP_HEADER_HEARTHOME_CITY_SOUTHEAST_HOUSE_2F`
- `MAP_HEADER_IRON_ISLAND_HOUSE`
- `MAP_HEADER_JUBILIFE_TV_3F_GLOBAL_RANKING_ROOM`
- `MAP_HEADER_MT_CORONET_OUTSIDE_NORTH`
- `MAP_HEADER_NEWMOON_ISLAND`
- `MAP_HEADER_NEWMOON_ISLAND_FOREST`
- `MAP_HEADER_NOTHING`
- `MAP_HEADER_PAL_PARK`
- `MAP_HEADER_PASTORIA_CITY_DP_GREAT_MARSH`
- `MAP_HEADER_POKEMON_LEAGUE_ELEVATOR_TO_BERTHA_ROOM`
- `MAP_HEADER_POKEMON_LEAGUE_ELEVATOR_TO_CHAMPION_ROOM`
- `MAP_HEADER_POKEMON_LEAGUE_ELEVATOR_TO_FLINT_ROOM`
- `MAP_HEADER_POKEMON_LEAGUE_ELEVATOR_TO_LUCIAN_ROOM`
- `MAP_HEADER_POKEMON_LEAGUE_HALLWAY_TO_HALL_OF_FAME`
- `MAP_HEADER_RECORD_MIXING_ROOM`
- `MAP_HEADER_RESORT_AREA_RIBBON_SYNDICATE_2F`
- `MAP_HEADER_ROUTE_204_NORTH`
- `MAP_HEADER_SEABREAK_PATH`
- `MAP_HEADER_SPRING_PATH`
- `MAP_HEADER_TROPHY_GARDEN`
- `MAP_HEADER_TURNBACK_CAVE_GIRATINA_ROOM`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_1_ROOM_1`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_1_ROOM_2`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_1_ROOM_3`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_1_ROOM_4`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_1_ROOM_5`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_1_ROOM_6`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_2_ROOM_1`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_2_ROOM_2`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_2_ROOM_3`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_2_ROOM_4`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_2_ROOM_5`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_2_ROOM_6`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_3_ROOM_1`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_3_ROOM_2`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_3_ROOM_3`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_3_ROOM_4`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_3_ROOM_5`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_3_ROOM_6`
- `MAP_HEADER_TURNBACK_CAVE_PILLAR_ROOM`
- `MAP_HEADER_UNDERGROUND`
- `MAP_HEADER_UNION_ROOM`
- `MAP_HEADER_UNKNOWN_197`
- `MAP_HEADER_UNKNOWN_206`
- `MAP_HEADER_UNKNOWN_222`
- `MAP_HEADER_UNKNOWN_224`
- `MAP_HEADER_UNKNOWN_243`
- `MAP_HEADER_UNKNOWN_250`
- `MAP_HEADER_UNKNOWN_252`
- `MAP_HEADER_UNKNOWN_255`
- `MAP_HEADER_UNKNOWN_266`
- `MAP_HEADER_UNKNOWN_275`
- `MAP_HEADER_UNKNOWN_276`
- `MAP_HEADER_UNKNOWN_277`
- `MAP_HEADER_UNKNOWN_304`
- `MAP_HEADER_UNKNOWN_324`
- `MAP_HEADER_UNKNOWN_325`
- `MAP_HEADER_UNKNOWN_401`
- `MAP_HEADER_UNKNOWN_402`
- `MAP_HEADER_UNKNOWN_404`
- `MAP_HEADER_UNKNOWN_405`
- `MAP_HEADER_UNKNOWN_408`
- `MAP_HEADER_UNKNOWN_409`
- `MAP_HEADER_UNKNOWN_470`
- `MAP_HEADER_UNKNOWN_473`
- `MAP_HEADER_UNKNOWN_511`
- `MAP_HEADER_UNKNOWN_533`
- `MAP_HEADER_UNKNOWN_534`
- `MAP_HEADER_UNKNOWN_535`
- `MAP_HEADER_UNKNOWN_536`
- `MAP_HEADER_UNKNOWN_537`
- `MAP_HEADER_UNKNOWN_538`
- `MAP_HEADER_UNKNOWN_539`
- `MAP_HEADER_UNKNOWN_540`
- `MAP_HEADER_UNKNOWN_541`
- `MAP_HEADER_UNKNOWN_542`
- `MAP_HEADER_UNKNOWN_543`
- `MAP_HEADER_UNKNOWN_544`
- `MAP_HEADER_UNKNOWN_545`
- `MAP_HEADER_UNKNOWN_546`
- `MAP_HEADER_UNKNOWN_547`
- `MAP_HEADER_UNKNOWN_548`
- `MAP_HEADER_UNKNOWN_549`
- `MAP_HEADER_UNKNOWN_550`
- `MAP_HEADER_UNKNOWN_551`
- `MAP_HEADER_UNKNOWN_552`
- `MAP_HEADER_UNKNOWN_553`
- `MAP_HEADER_UNKNOWN_554`
- `MAP_HEADER_UNKNOWN_555`
- `MAP_HEADER_UNKNOWN_556`
- `MAP_HEADER_UNKNOWN_557`
- `MAP_HEADER_UNKNOWN_561`
- `MAP_HEADER_UNKNOWN_570`
- `MAP_HEADER_UNKNOWN_572`
- `MAP_HEADER_UNKNOWN_578`
- `MAP_HEADER_UNUSED_BATTLE_PARK`
- `MAP_HEADER_UNUSED_BATTLE_PARK_EXCHANGE_SERVICE_CORNER`
- `MAP_HEADER_UNUSED_BATTLE_PARK_GATE_TO_FIGHT_AREA`
- `MAP_HEADER_UNUSED_ETERNA_CITY_HOUSE`
- `MAP_HEADER_UNUSED_FIGHT_AREA_HOUSE`
- `MAP_HEADER_UNUSED_GATE_BETWEEN_ETERNA_CITY_ROUTE_206`
- `MAP_HEADER_UNUSED_JUBILIFE_CITY_HOUSE_1`
- `MAP_HEADER_UNUSED_JUBILIFE_CITY_HOUSE_2`
- `MAP_HEADER_UNUSED_RESORT_AREA_MART`
- `MAP_HEADER_UNUSED_VERITY_LAKEFRONT_HOUSE`
- `MAP_HEADER_VISTA_LIGHTHOUSE`
- `MAP_HEADER_WIFI_PLAZA_ENTRANCE`

</details>

## Unova (fonte: `fontes-mapas/bw3g`)

291 mapas nossos, 290 com par na fonte, 1 sem par, 19 mapas da fonte ausentes aqui.

### Os dois totais, lado a lado

| medida | existe | tem conteúdo | fonte |
|---|---:|---:|---:|
| pessoas | 945 | 888 com fala | 915 (811 com fala) |
| placas | 363 | 217 com texto | 355 (173 com texto) |
| treinadores | 360 citados por trainerbattle | 360 com time | 348 |
| mapas | 291 | 246 com pelo menos um NPC que fala | 309 |
| encontros | 87 | -- | 65 |

Dos 945 que existem, **57 não falam**: 57 sem script nenhum (`script: "0"`) e 0 com rótulo que não tem comando de texto (parte é balconista e enfermeira, que chamam loja e cura direto, e parte é NPC pela metade). A fonte tem 104 mudos nos mesmos mapas, então a dívida real é **1**, somada mapa a mapa (o excesso de um mapa não paga a falta de outro).

Objetos que NÃO são gente (item ball, árvore, pedra, mobília): **450 aqui contra 442 na fonte**. Esta linha importa porque `completude.py` conta objeto e não gente: quando o total de objetos bate com a fonte e o de pessoas não, o que aconteceu foi troca de sprite, não falta de objeto. É o caso de Johto, onde o importador pôs `OBJ_EVENT_GFX_ITEM_BALL` com `script: "0"` na coordenada exata de cada NPC da fonte (conferido à mão em `EcruteakCity`, 49 objetos dos dois lados e 49 item balls aqui).

### Mapa a mapa (só os que divergem da fonte)

Toda coluna de lacuna é medida CONTRA A FONTE, nunca contra o ideal. Mapa igual à fonte não aparece aqui, mesmo cheio de NPC mudo: o pokeemerald vanilla também tem, e reprovar o jogo original é a lição 4.10 do `ESTADO.md`.

| mapa | objetos | pessoas | falta | excesso | mudo a mais | treinador | placa genérica a mais | encontro | arquivo da fonte |
|---|---:|---:|---:|---:|---:|---:|---:|:-:|---|
| `Unova_Rt6Lab` | 2 / 0 | 2 / 0 |  | 2 |  | 0 / 0 | 4 | ok | `fontes-mapas/bw3g/maps/R6Lab.asm` |
| `Unova_MistraltonGym1F` | 9 / 9 | 5 / 9 | 4 |  |  | 4 / 3 |  | ok | `fontes-mapas/bw3g/maps/MistraltonGym1F.asm` |
| `Unova_Rt18House` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 | 2 | ok | `fontes-mapas/bw3g/maps/R18House.asm` |
| `Unova_Rt23House` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 | 2 | ok | `fontes-mapas/bw3g/maps/R23House.asm` |
| `Unova_Rt3DayCare` | 2 / 0 | 2 / 0 |  | 2 | 1 | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R3DayCare.asm` |
| `Unova_Rt4House` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 | 2 | ok | `fontes-mapas/bw3g/maps/R4House.asm` |
| `Unova_Rt4NimbasaGate` | 3 / 0 | 3 / 0 |  | 3 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R4NimbasaGate.asm` |
| `Unova_Rt6House` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 | 2 | ok | `fontes-mapas/bw3g/maps/R6House.asm` |
| `Unova_Rt7House` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 | 2 | ok | `fontes-mapas/bw3g/maps/R7House.asm` |
| `Unova_Rt7TradeHouse` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 | 2 | ok | `fontes-mapas/bw3g/maps/R7TradeHouse.asm` |
| `Unova_MistraltonGym2F` | 4 / 4 | 2 / 4 | 2 |  |  | 2 / 2 |  | ok | `fontes-mapas/bw3g/maps/MistraltonGym2F.asm` |
| `Unova_Rt13UndellaGate` | 2 / 0 | 2 / 0 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R13UndellaGate.asm` |
| `Unova_Rt16LostlornGate` | 2 / 0 | 2 / 0 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R16LostlornGate.asm` |
| `Unova_Rt16NimbasaGate` | 2 / 0 | 2 / 0 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R16NimbasaGate.asm` |
| `Unova_Rt19AspertiaGate` | 2 / 0 | 2 / 0 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R19AspertiaGate.asm` |
| `Unova_Rt4CasteliaGate` | 2 / 0 | 2 / 0 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R4CasteliaGate.asm` |
| `Unova_Rt4DesertGate` | 2 / 0 | 2 / 0 |  | 2 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R4DesertGate.asm` |
| `Unova_OpelucidCity` | 7 / 7 | 5 / 6 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/OpelucidCity.asm` |
| `Unova_PlayersHouse2F` | 4 / 4 | 0 / 1 | 1 |  |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/PlayersHouse2F.asm` |
| `Unova_Rt11OpelucidGate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R11OpelucidGate.asm` |
| `Unova_Rt11Truck` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R11Truck.asm` |
| `Unova_Rt11VillageBridgeGate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R11VillageBridgeGate.asm` |
| `Unova_Rt12VillageBridgeGate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R12VillageBridgeGate.asm` |
| `Unova_Rt20VirbankGate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R20VirbankGate.asm` |
| `Unova_Rt23Gate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R23Gate.asm` |
| `Unova_Rt2AccumulaGate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R2AccumulaGate.asm` |
| `Unova_Rt3NacreneGate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R3NacreneGate.asm` |
| `Unova_Rt5BridgeGate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R5BridgeGate.asm` |
| `Unova_Rt5NimbasaGate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R5NimbasaGate.asm` |
| `Unova_Rt5Truck` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R5Truck.asm` |
| `Unova_Rt9OpelucidGate` | 1 / 0 | 1 / 0 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/R9OpelucidGate.asm` |
| `Unova_VirbankPort` | 2 / 1 | 2 / 1 |  | 1 |  | 0 / 0 |  | ok | `fontes-mapas/bw3g/maps/VirbankPort.asm` |

<details><summary>1 mapas nossos sem par na fonte (nativo, renomeado ou de outra fonte)</summary>

- `Unova_Rt1Rt17Gate` (1 pessoas, 1 com fala)

</details>

<details><summary>19 mapas que a fonte tem e nós não</summary>

- `BattleTower1F`
- `BattleTowerBattleRoom`
- `BattleTowerElevator`
- `BattleTowerHallway`
- `BattleTowerOutside`
- `CeladonGameCorner`
- `CeladonGameCornerPrizeRoom`
- `DayCare`
- `ElmsLab`
- `GoldenrodGameCorner`
- `GoldenrodMagnetTrainStation`
- `LancesRoom`
- `MoveDeletersHouse`
- `NationalPark`
- `NationalParkBugContest`
- `OaksLab`
- `PokemonFanClub`
- `R1R17Gate`
- `SaffronMagnetTrainStation`

</details>

## Fila de trabalho

**Isto substitui a seção 8 do `ESTADO.md` como fila.** A ordem é o tamanho
medido da lacuna, não a opinião de ninguém. Item que some do inventário na
próxima rodada é item resolvido; item que cresce é regressão.

| # | tamanho | região | lacuna | por onde se fecha |
|---:|---:|---|---|---|
| 1 | 316 | Sinnoh | pessoas que a fonte tem e aqui não | completar object_events dos mapas com falta |
| 2 | 266 | Sinnoh | pessoas a mais que a fonte (conteúdo inventado) | bloco B3: esconder atrás de flag depois das quatro provas |
| 3 | 209 | Sinnoh | NPC mudo a mais que a fonte (existe e não fala) | bloco B2: trazer a fala da fonte |
| 4 | 162 | Sinnoh | mapa da fonte ausente aqui | bloco B1 (Sinnoh) ou conversão nova |
| 5 | 162 | Johto | pessoas que a fonte tem e aqui não | completar object_events dos mapas com falta |
| 6 | 97 | Johto | NPC mudo a mais que a fonte (existe e não fala) | bloco B2: trazer a fala da fonte |
| 7 | 71 | Sinnoh | placa genérica a mais que a fonte | trazer o texto da placa da fonte |
| 8 | 38 | Unova | pessoas a mais que a fonte (conteúdo inventado) | bloco B3: esconder atrás de flag depois das quatro provas |
| 9 | 33 | Johto | treinador da fonte sem par batalhável aqui | bloco B4: ligar trainerbattle e declarar time |
| 10 | 31 | Sinnoh | treinador da fonte sem par batalhável aqui | bloco B4: ligar trainerbattle e declarar time |
| 11 | 19 | Unova | mapa da fonte ausente aqui | bloco B1 (Sinnoh) ou conversão nova |
| 12 | 16 | Unova | placa genérica a mais que a fonte | trazer o texto da placa da fonte |
| 13 | 16 | Hoenn | NPC mudo a mais que a fonte (existe e não fala) | bloco B2: trazer a fala da fonte |
| 14 | 10 | Johto | mapa da fonte ausente aqui | bloco B1 (Sinnoh) ou conversão nova |
| 15 | 8 | Unova | pessoas que a fonte tem e aqui não | completar object_events dos mapas com falta |
| 16 | 8 | Kanto | mapa da fonte ausente aqui | bloco B1 (Sinnoh) ou conversão nova |
| 17 | 4 | Hoenn | treinador da fonte sem par batalhável aqui | bloco B4: ligar trainerbattle e declarar time |
| 18 | 3 | Hoenn | placa genérica a mais que a fonte | trazer o texto da placa da fonte |
| 19 | 2 | Kanto | pessoas a mais que a fonte (conteúdo inventado) | bloco B3: esconder atrás de flag depois das quatro provas |
| 20 | 2 | Hoenn | pessoas a mais que a fonte (conteúdo inventado) | bloco B3: esconder atrás de flag depois das quatro provas |
| 21 | 1 | Unova | NPC mudo a mais que a fonte (existe e não fala) | bloco B2: trazer a fala da fonte |
| 22 | 1 | Kanto | placa genérica a mais que a fonte | trazer o texto da placa da fonte |
| 23 | 1 | Kanto | NPC mudo a mais que a fonte (existe e não fala) | bloco B2: trazer a fala da fonte |

### Por região, a maior lacuna de cada uma

- **Sinnoh**: pessoas que a fonte tem e aqui não, 316. completar object_events dos mapas com falta.
- **Johto**: pessoas que a fonte tem e aqui não, 162. completar object_events dos mapas com falta.
- **Unova**: pessoas a mais que a fonte (conteúdo inventado), 38. bloco B3: esconder atrás de flag depois das quatro provas.
- **Hoenn**: NPC mudo a mais que a fonte (existe e não fala), 16. bloco B2: trazer a fala da fonte.
- **Kanto**: mapa da fonte ausente aqui, 8. bloco B1 (Sinnoh) ou conversão nova.

