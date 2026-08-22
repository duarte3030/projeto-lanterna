# Fase F: os times de chefe

Pedido do Gui, 21/08/2026, literal: *"Dá pra você trabalhar nos times de todos os
líderes de ginásio, rivais, Elite Four e Champion, mantendo lv 5. Faz times tops e
difíceis aí, com inspiração no Pokémon Radical Red, modo insano. Lendários pra todos
(acima do lv 40). Mega evolução, Z-move etc. Dynamax é o que eu menos gosto, deixa
pouco disso. Tera não sei se tem, se tiver bota alguns, mas também não gosto."*

Fonte da verdade: `dev_scripts/fase_f_chefes.json`. Quem escreve
`src/data/trainers.party` a partir dela: `dev_scripts/fase_f_chefes.py`, que é
**idempotente** (substitui o time inteiro da batalha; rodar duas vezes dá diff zero).
`dev_scripts/gens69_treinadores.py` deixou de valer para chefe, e o cabeçalho dele
já diz isso.

## O que a medição disse (não é memória, é o repositório de hoje)

- **Os quatro gimmicks existem e três não custam nada para ligar.**
  - **Mega**: puro item. `CanMegaEvolve` (`src/battle_util.c:8418`) só olha a pedra
    segurada; nenhuma flag. A tabela de pedras vem de
    `src/data/pokemon/form_change_tables.h`: **96 formas Mega**, incluindo Megas
    de fã que o upstream não tem (Meganium, Feraligatr, Skarmory, Staraptor,
    Heatran, Darkrai, Zeraora, Emboar, Excadrill, Magearna, Baxcalibur).
  - **Z-move**: puro item, 35 cristais em `include/constants/items.h`.
  - **Dynamax**: já ligado, por `B_FLAG_DYNAMAX_BATTLE = FLAG_B8_DYNAMAX_LIBERADO`
    (`include/config/battle.h:263`).
  - **Terastal: JÁ FUNCIONA para treinador, e ligar não custa nada, porque não há
    nada para ligar.** `src/battle_terastal.c:78` deixa o lado do ADVERSÁRIO pular
    todas as checagens de Tera Orb; `B_FLAG_TERA_ORB_CHARGED` só existe para o
    jogador. Basta o mon ter `Tera Type` no `.party`. **`include/config/battle.h`
    não foi tocado.**
- **Flags de IA**: 34 individuais em `include/constants/battle_ai.h`, mais os
  compostos `AI_FLAG_SMART_TRAINER` (básico + onisciente + troca inteligente +
  anti-stall de PP + tera inteligente), `AI_FLAG_PREDICTION` e `AI_FLAG_ASSUMPTIONS`.
  O campo `aiFlags` é u64, então cabem todos.
- **Ability declarada é asserção, não sugestão**: `src/battle_main.c:1941` tem
  `assertf(abilityNum < maxAbilityNum, "illegal ability ...")`. Toda habilidade da
  tabela foi conferida contra `.abilities` em `src/data/pokemon/species_info/*.h`;
  onde o `species_info` vem de macro e não dá para ler (Gengar, Genesect), a linha
  `Ability:` simplesmente não é escrita, e o motor cai no slot 0.
- **Curva por região, medida nos times de hoje** (ace mínimo e máximo dos chefes):
  Kanto 3-50, Johto 45-100, Hoenn 97-150, Sinnoh 149-200, Unova 204-255.
  **Nenhum nível foi mudado**: o ace de cada batalha ficou no nível que já tinha, e
  o resto do time entra até 4 níveis abaixo dele.

## Contagem: 144 batalhas de chefe (líder, rival, E4, campeão)

Os **40 chefes de equipe vilã** entraram depois, em 22/08/2026, e têm seção
própria mais abaixo; com eles a tabela foi a **184 batalhas e 970 Pokémon**. Na
rodada seguinte do mesmo dia entraram as **6 batalhas que a fonte tinha e este
repo não** (três de Silver, a `RYOKU1`, o N e o Hugh), e a tabela fechou em
**190 batalhas e 1.006 Pokémon**; a leva 2 do mesmo dia trouxe Bianca, Cheren 2 e
as seis variantes de Nate/Rosa, e a tabela fechou em **198 batalhas e 1.054
Pokémon**.

| região | batalhas | líder | rival | E4 | campeão | lendários distintos | mega | Z | dmax | tera |
|---|---|---|---|---|---|---|---|---|---|---|
| Kanto  | 43 | 8 | 21 | 8 | 6 | 6  | 22 | 2 | 0 | 1 |
| Johto  | 13 | 8 |  4 | 0 | 1 | 10 |  8 | 1 | 2 | 0 |
| Hoenn  | 44 | 8 | 30 | 4 | 2 | 16 | 22 | 1 | 1 | 2 |
| Sinnoh | 28 | 8 | 15 | 4 | 1 | 15 | 17 | 2 | 1 | 2 |
| Unova  | 16 | 8 |  0 | 4 | 4 | 14 | 11 | 3 | 1 | 1 |

742 Pokémon no total. **111 batalhas têm lendário** (as de ace acima de 40) e
**33 não têm** (as de ace 40 ou menos: os 8 líderes de Kanto, os 4 primeiros E4 de
Kanto e as 21 batalhas de rival de Kanto). Os 8 líderes de Kanto e os 4 E4 da
primeira volta PERDERAM as lendas que o B8 tinha dado (Cosmog no Brock de nível 9,
Chi-Yu no Blaine de 31): a regra do Gui é "acima do lv 40".

## As regras, e onde o guarda as cobra (`fase_f_chefes.py --demo`)

1. **6 Pokémon** em todo chefe; menos só nas primeiras batalhas de rival, onde a
   contagem segue a fonte (1, 2, 3...). Quando a fonte tem menos vagas do que o
   lendário exige, o time sobe para 2.
2. **Um lendário por batalha com ace acima de 40, nenhum abaixo**, sempre coerente
   com o tipo do chefe, e **sem repetir dentro da mesma região entre pessoas
   diferentes** (Silver carrega o mesmo Lugia nas quatro batalhas dele porque é a
   mesma pessoa). Mewtwo, Arceus e Rayquaza foram reservados: Mewtwo é do Blue da
   revanche, Rayquaza é do Steven, Arceus não foi usado.
3. **Um gimmick por chefe**, nunca dois, porque o motor só deixa o treinador usar um
   por batalha. Mega é o padrão (80 chefes). Z entra onde o sabor ganha do Mega
   (9: Bruno-2, Lorelei-2, Morty com Marshadium, Juan, Fantina, Flint, Roxie, Skyla,
   Marshal). **Dynamax em 5 no jogo inteiro** (Whitney, Chuck, Norman, Roark, Cheren),
   **Terastal em 6** (Lance-2, Drake, Steven, Lucian, Cynthia, Genesis).
   Chefe com ace abaixo de 20 não ganha gimmick: Brock, Misty, Lt. Surge e as cinco
   primeiras batalhas de rival de Kanto lutam limpo.
4. **IV 31 em tudo, EV competitivo 252/252/4, natureza, habilidade e item de segurar
   em TODOS**, quatro golpes com cobertura, setup, hazard ou pivot.
5. **IA**: `AI_FLAG_SMART_TRAINER / HP_AWARE / TRY_TO_2HKO / POWERFUL_STATUS /
   PREDICTION / ASSUMPTIONS / KNOW_OPPONENT_PARTY / ACE_POKEMON` em todo chefe
   (em batalha dupla o ACE sai e entra `DOUBLE_BATTLE`).

Os **7 chefes que a 0.h achou sem gimmick nenhum** entraram na regra: Genesis ganhou
Terastal, os três Juniper ganharam Mega, e Colress, Elesa e Marshal ganharam Mega,
Mega e Z.

## Os 61 lendários, por chefe

- **Kanto**: Lorelei-2 Articuno, Bruno-2 Terrakion, Agatha-2 Spectrier, Lance-2 Latios, Blue Zapdos (primeira) e Mewtwo (revanche).
- **Johto**: Falkner Tornadus-T, Bugsy Genesect, Whitney Regigigas, Morty Marshadow, Chuck Cobalion, Jasmine Registeel, Pryce Regice, Clair Latias, Silver Lugia, Red Ho-Oh.
- **Hoenn**: Roxanne Regirock, Brawly Urshifu-Rapid, Wattson Thundurus-T, Flannery Heatran, Norman Regigigas, Winona Ho-Oh, Tate&Liza Cresselia, Juan Suicune, Sidney Darkrai, Phoebe Giratina-Origin, Glacia Glastrier, Drake Regidrago, **Wallace Palkia**, Steven Rayquaza, **Brendan Latios**, May Latias.
  (Wallace e Brendan trocaram em 22/08/2026 para o Archie e o Maxie ficarem com
  Kyogre e Groudon; a razão está na seção dos chefes de equipe vilã.)
- **Sinnoh**: Roark Terrakion, Gardenia Shaymin-Céu, Fantina Pecharunt, Maylene Keldeo, Wake Suicune, Byron Heatran, Candice Calyrex-Gelo, Volkner Raikou, Aaron Genesect, Bertha Landorus-T, Flint Volcanion, Lucian Azelf, Cynthia Giratina-Origin, Barry Palkia (e Dialga na Liga).
- **Unova**: Marlon Kyogre, Shauntal Hoopa-Solto, Burgh Pheromosa, Roxie Eternatus, Cheren Regigigas, Cilan Virizion, Skyla Yveltal, Drayden Zygarde-50, Grimsley Darkrai, Marshal Urshifu-Single, Elesa Zeraora, Colress Magearna, Genesis Kyurem-Preto, Juniper Reshiram.

Lendário repetido entre REGIÕES é de propósito: são jornadas separadas.

## Simplificação assumida, medida e dita

Os movesets vêm de uma biblioteca de sets por espécie, um set por espécie, e não
de um set por espécie POR CHEFE. O preço disso está medido: **16 dos 144 times
repetem um hazard** (20 Stealth Rock, 3 Spikes, 2 Toxic Spikes), o que gasta
**25 dos 742 slots de golpe, 3%**. Não é bug: com `AI_FLAG_CHECK_BAD_MOVE` a IA
não repõe hazard que já está no campo, e ter dois setters em time monotipo é
redundância legítima quando o primeiro cai antes de agir. Se um dia isso
incomodar, o conserto é uma tabela de golpe alternativo por espécie no autor da
`fase_f_chefes.json`, não lógica nova no gerador.

## O elenco de rival: nada ficou de fora, o buraco é do IMPORT

Conferido pelo fechador em 21/08/2026, porque a tabela chama a atenção: Johto tem
4 batalhas de rival e **Unova tem ZERO**. Medido contra `src/data/trainers.party`
e `include/constants/opponents.h`, e não contra a memória das fontes:

- **Johto**: eram **quatro** entradas de Silver com time próprio,
  `TRAINER_JOHTO_RIVAL_SILVER_1` a `_4`. O HGSS enfrenta o Silver sete vezes, e as
  outras três **foram importadas em 22/08/2026** (`_5`, `_6` e `_7`, ids 2523 a
  2525). Johto passa a ter **sete** batalhas de rival, e o buraco de importação
  fechou.
- **Unova**: o espaço `TRAINER_UNOVA_*` tinha 403 constantes e **nenhuma de
  rival**, e a leitura de então ("o BW3G não trouxe rival nenhum") estava errada
  por não ter aberto a fonte: o que não tinha rival era o IMPORT, não o BW3G. Os
  `TRAINER_BIANCA`, `TRAINER_HUGH` e `TRAINER_NATE` do `.party` seguem sendo NPCs
  de HOENN (Route 111, Route 119 e o ginásio de Mossdeep), homônimos. Em
  22/08/2026 entraram **dois** rivais de verdade: `TRAINER_UNOVA_N` (2527) e
  `TRAINER_UNOVA_HUGH_TEPIG` (2528). O Cheren de lá continua líder de ginásio
  (`TRAINER_UNOVA_LEADER_CHEREN`), como em BW2.
- Varredura fechada: **zero** treinadores com `RIVAL` no nome e time próprio
  ficaram fora da tabela de chefes.

Esse item de fila foi cumprido em 22/08/2026: as três batalhas de Silver e dois
rivais do BW3G entraram, e o time delas foi escrito pelo mesmo gerador. O que
ficou para trás está na tabela da seção "A FONTE FOI MEDIDA", com o motivo.

## Os chefes de equipe vilã: 40 batalhas, 228 Pokémon (22/08/2026)

Entraram na MESMA tabela e no MESMO gerador, com `papel: "vilao"`. Nível da curva
intocado: cada batalha ficou no ace que já tinha, e o resto do time entra até 4
níveis abaixo dele, como no resto da Fase F.

| região | equipe | batalhas | pessoas | ace | lendários | Mega | Z |
|---|---|---|---|---|---|---|---|
| Kanto | Rocket | 4 | 3 | 20-36 | **nenhum** | 4 | 0 |
| Johto | Rocket | 8 | 5 | 59-114 | Naganadel, Nihilego, Yveltal, Darkrai, Ting-Lu | 8 | 0 |
| Hoenn | Magma | 6 | 2 | 109-124 | **Groudon**, Chi-Yu | 6 | 0 |
| Hoenn | Aqua | 4 | 3 | 114-124 | **Kyogre**, Guzzlord, Tapu Fini | 4 | 0 |
| Sinnoh | Galáctica | 9 | 4 | 157-186 | Mesprit, Uxie, Cobalion, Darkrai | 9 | 0 |
| Unova | Plasma | 9 | 5 | 219-245 | Zekrom, Victini, Suicune, Wo-Chien, Chien-Pao | 8 | 1 |

**Dynamax e Terastal: zero novos.** As cotas do Gui (5 e 6) já estavam gastas nos
144 chefes da primeira leva e continuam em 5 e 6; nenhum vilão ganhou nem um nem
outro. O Z é UM só, no Ryoku (Decidueye com `ITEM_DECIDIUM_Z`), e ele foi
escolhido porque o time de grama dele é o único onde **nenhuma das seis espécies
tem Mega** na `form_change_tables.h`: dar Mega ali exigiria trocar o elenco.

**Os quatro chefes de Kanto não têm lendário e isso é a regra, não esquecimento**:
Giovanni do Rocket Hideout (ace 20), do Silph Co. (27) e os dois Admin do
Rocket Warehouse de Five Island (36) estão todos em 40 ou abaixo, e a regra do Gui
é "lendário acima do lv 40".

### A lore vence para o chefe vilão: quem cede é o herói (decisão do Gui, 22/08/2026)

A primeira escrita desta rodada tinha dado Entei ao Maxie e Palkia ao Archie,
porque Groudon estava com o **Brendan** (rival) e Kyogre com o **Wallace**
(campeão), e a regra proíbe repetir lendário dentro da região. O Gui inverteu a
prioridade: **para chefe de equipe vilã a lore vence, e o herói é quem cede.**
Quatro trocas, todas em Hoenn, feitas pelo gerador e não à mão:

| pessoa | antes | depois | por quê |
|---|---|---|---|
| Maxie (3 batalhas) | Entei | **Groudon** | é o Pokémon que a Magma quer despertar |
| Archie (1 batalha) | Palkia | **Kyogre** | é o Pokémon que a Aqua quer despertar |
| Brendan (15 batalhas) | Groudon | **Latios** | Latias é da May, e Latios só estava em KANTO (Lance-2), então é o único do par livre em Hoenn |
| Wallace (1 batalha) | Kyogre | **Palkia** | é o Água/Dragão que o Archie acabou de liberar; Suicune não servia porque já é do Juan, na mesma região |

**O orbe de Primal ENTROU em 22/08/2026 (rodada 5), e a 0.l estava errada sobre o
motor.** O Groudon do Maxie passa a carregar `ITEM_RED_ORB` nas três batalhas e o
Kyogre do Archie passa a carregar `ITEM_BLUE_ORB`; **a Mega Camerupt e a Mega
Sharpedo FICAM**. A 0.l dizia que a Primal entraria "por cima" do Mega e quebraria
o "um gimmick por chefe"; medido no código de batalha, ela não entra por cima de
nada:

- a Primal **não está no `enum Gimmick`** (`include/battle_gimmick.h:4`, que só
  tem MEGA, ULTRA_BURST, Z_MOVE, DYNAMAX e TERA);
- ela roda **sozinha ao entrar em campo**, sem botão e sem escolha do treinador
  (`src/battle_switch_in.c:276` chama `TryPrimalReversion` dentro do
  `FIRST_EVENT_BLOCK_GENERAL_ABILITIES`);
- ela **nunca chama `SetActiveGimmick` nem `SetGimmickAsActivated`**: a varredura
  dos dois só acha `battle_z_move.c`, `battle_dynamax.c`, `battle_terastal.c`,
  `battle_ai_util.c` e as duas de Mega/Ultra Burst em `battle_util.c:8496` e
  `:8514`.

Logo `CanMegaEvolve` (`src/battle_util.c:8418`) continua devolvendo TRUE para o
ace com pedra depois de o Groudon reverter, porque nem
`HasTrainerUsedGimmick(GIMMICK_MEGA)` nem `GetActiveGimmick` enxergam a Primal.
`P_PRIMAL_REVERSIONS` é TRUE (`include/config/species_enabled.h:24`) e as duas
entradas de forma existem (`form_change_tables.h:739` e `:750`).

**O guarda aprendeu o orbe** (`orbes_do_motor` em `fase_f_chefes.py`): ele lê as
entradas `FORM_CHANGE_BATTLE_PRIMAL_REVERSION` do motor, reprova orbe em espécie
que não tem Primal, reprova a tabela inteira se alguém desligar
`P_PRIMAL_REVERSIONS`, e **não** conta o orbe contra o "um gimmick por chefe",
porque o motor não conta. O `--demo` foi de 9 para 10 mutações.

**Cyrus ficou como estava, e é decisão e não esquecimento**: o trio da criação
está todo com Barry (Palkia, Dialga) e Cynthia (Giratina-Origin), e Darkrai é o
pesadelo de Sinnoh, que é o que o Cyrus quer ser no Platinum. As outras escolhas
que a regra ditou seguem valendo: **Tabitha Chi-Yu**, **Matt Guzzlord**, **Shelly
Tapu Fini**, e os comandantes com o **trio dos lagos que a Galáctica sequestra na
história** (Mars Mesprit do Lago Verity, Jupiter Uxie do Lago Acuity, e Saturn com
**Cobalion** porque o Azelf do Lago Valor é do Lucian). **Giovanni de Johto ficou
com Ting-Lu** e não com Mewtwo: o Mewtwo segue reservado ao Blue da revanche.

### Ghetsis, N e o Shadow Triad NÃO EXISTEM nesta ROM

Medido em 22/08/2026 contra `src/data/trainers.party` e
`include/constants/opponents.h`, não contra a memória do BW2: **zero** ocorrência
de `GHETSIS`, `SHADOW_TRIAD` ou de um `TRAINER_N`. O nome "GHETSIS" aparece só
como TEXTO, em três `scripts.inc` de Unova (`ChampionsRoom`,
`ChampionsRoomEntrance`, `DragonspiralTowerRoof`), onde os Sete Sábios o citam.
Quem batalha pela Plasma são **Zinzolin e quatro dos Sete Sábios**: Gorm, Giallo,
Bronius e Ryoku, com duas batalhas cada menos o Ryoku, que só tem a `RYOKU2` (a
`RYOKU1` nunca foi importada, como as três batalhas de Silver). Colress e Marshal
já eram Elite Four e continuam lá. Portanto **Kyurem para o Ghetsis e
Reshiram/Zekrom para o N são item de IMPORTAÇÃO**, não de elenco; o Zekrom entrou
com o Giallo, que é o sábio de elétrico. **Courtney e Charon também não existem**
(a ausência da Courtney já estava escrita em `SINNOH-PADRAO.md`).

## A FONTE FOI MEDIDA (22/08/2026, rodada 5): quem existe, quem não existe

A 0.l e a seção acima diziam que Kyurem para o Ghetsis e Reshiram/Zekrom para o N
eram "hipótese e não promessa", porque **ninguém tinha aberto a fonte**. Agora
abriu. Medição contra os arquivos, com caminho e linha:

| pessoa | existe na fonte? | id da fonte | mapa da fonte | ace da fonte | cena portável? |
|---|---|---|---|---|---|
| Silver 5 | **sim** | `TRAINER_RIVAL_TOTODILE_5` | `VictoryRoadKanto_1F` | Tyranitar 48 | **não**: `applymovement2`, `OBJ_EVENT_ID_FOLLOWER`, três ramos de `getplayerxy` |
| Silver 6 | **sim** | `TRAINER_RIVAL_TOTODILE_6` | `MtMoon_Cave` | Tyranitar 64 | **não**: `MAP_SCRIPT_ON_FRAME_TABLE`, `applymovement2`, `clearflag` de outro mapa |
| Silver 7 | **sim** | `TRAINER_RIVAL_TOTODILE_7` | `IndigoPlateau_PokemonCenter` | Tyranitar 68 | **sim**, e é o único: só `lock`/`faceplayer`/`msgbox`/`trainerbattle_no_intro` |
| Ryoku 1 | **sim** | `RYOKU1` | `AccumulaTown` (`maps/AccumulaTown.asm:43`) | Amoonguss 40 | **não**: `checkcode VAR_FACING`, `FadeBlackQuickly`, 5 `disappear` + 4 `appear` |
| N | **sim** | `N1` (`parties.asm:4989`) | `NsRoom` (`maps/NsRoom.asm:29`) | Zoroark 73 | **sim**: `faceplayer` + texto + batalha |
| Hugh | **sim**, 3 variantes de inicial | `HUGH_SNIVY/_TEPIG/_OSHAWOTT` (`parties.asm:4875`) | `DriftveilShelter` (revanche em `:222-252`) | starter 73 | **sim** na revanche: só falas + batalha |
| Bianca | **sim**, 1 | `BIANCA1` (`parties.asm:4075`) | `PWTBattleRoom` | Musharna 45 | **não**: moldura de torneio (`scene_script`, `priorityjump`, `warpcheck`, `setmapscene`) |
| Nate / Rosa | **sim**, 3+3 variantes | `NATE_*`, `ROSA_*` | `NimbasaParkOutside` | starter 76 | médio, atrás de ramo de gênero **e** de inicial |
| Cheren 2 | **sim** | `CHEREN2` (`parties.asm:3731`) | `OpelucidBattleHouse` | Stoutland 68 | sim, mas é **revanche**, e revanche já estava fora de escopo |
| **Ghetsis** | **NÃO EXISTE** | — | só como texto em 5 mapas e como `MUSIC_GHETSIS_BATTLE` | — | — |
| **Shadow Triad** | **NÃO EXISTE como treinador** | só `SPRITE_SHADOW` em `OBJECTTYPE_SCRIPT` | — | — | — |
| **Courtney** | **NÃO EXISTE** | zero ocorrência em `fontes-mapas/pokeemerald` | — | — | — |
| **Charon** | **NÃO EXISTE como treinador** | é NPC de cena no `pokeplatinum`; a lista de 929 treinadores não tem nenhum | — | — | — |

Achado de quebra, e ele desmonta a hipótese da 0.l: a `MUSIC_GHETSIS_BATTLE` do
BW3G **não é do Ghetsis**. Em `engine/battle/start_battle.asm:135` ela pertence à
`trainerclass GENESIS`, o chefe original do hack, que já é o campeão de Unova
aqui. O slot narrativo do Ghetsis já está ocupado, e por isso **Ghetsis, Shadow
Triad, Courtney e Charon saem da fila como INEXISTENTES, não como pendentes.**

### O que foi importado, e por quê o resto não

Seis batalhas, por `dev_scripts/importa_chefes_faltantes.py` (idempotente,
`--demo` com três mutações plantadas), e depois vestidas pelo `fase_f_chefes.py`
como qualquer outro chefe. A Fase F vai a **190 batalhas e 1.006 Pokémon**; a leva 2 do mesmo dia trouxe Bianca, Cheren 2 e
as seis variantes de Nate/Rosa, e a tabela fechou em **198 batalhas e 1.054
Pokémon**.

| batalha | id | mapa deste repo | ace | gimmick | lendário |
|---|---|---|---|---|---|
| `TRAINER_JOHTO_RIVAL_SILVER_5` | 2523 | `VictoryRoad_1F_Frlg` (8,20) | 92 | Mega Tyranitar | Lugia |
| `TRAINER_JOHTO_RIVAL_SILVER_6` | 2524 | `MtMoon_1F_Frlg` (4,6) | 109 | Mega Tyranitar | Lugia |
| `TRAINER_JOHTO_RIVAL_SILVER_7` | 2525 | `IndigoPlateau_PokemonCenter_1F_Frlg` (11,13) | 113 | Mega Tyranitar | Lugia |
| `TRAINER_UNOVA_RYOKU1` | 2526 | `Unova_AccumulaTown`, NPC que já existia | 228 | Z Decidueye | Wo-Chien |
| `TRAINER_UNOVA_N` | 2527 | `Unova_NsRoom`, NPC que já existia | 255 | Z Zoroark | Kyurem-Branco |
| `TRAINER_UNOVA_HUGH_TEPIG` | 2528 | `Unova_DriftveilShelter`, NPC que já existia | 255 | Mega Emboar | Landorus-T |

- **As três de Silver foram REESCRITAS, não copiadas**, e isso é decisão: duas das
  três cenas da fonte são cinema (`ShakeCamera`, `setmetatile`, `warphole`,
  `applymovement2`, `OBJ_EVENT_ID_FOLLOWER`). O molde usado é o das QUATRO cenas de
  Silver que este repo já provou na ROM (`CherrygroveCity/scripts.inc`):
  `ON_TRANSITION` acende a flag de esconder, `goto_if_not_defeated` da batalha
  anterior e `goto_if_defeated` da própria abrem o NPC, e a cena é
  `trainerbattle_single` + `msgbox` + `removeobject`. **Os textos são os da
  fonte, verbatim.** A fonte tem três linhas de inicial e este repo segue com a
  do TOTODILE, como as quatro batalhas antigas.
- **As três de Unova não precisaram de objeto nem de flag**: o import de mapa já
  tinha posto o NPC no lugar certo, com o sprite e o texto da fonte, só falando.
  O `msgbox` virou `trainerbattle_single`.
- **O Hugh entra na variante TEPIG por MEDIÇÃO**: das três, só ela põe no slot de
  ace um Pokémon com Mega na `form_change_tables.h` (Emboar / `ITEM_EMBOARITE`).
  Com Snivy ou Oshawott o ace ficaria sem gimmick.
- **N e Ryoku 1 ganharam Z e não Mega** pelo mesmo motivo do Ryoku 2: nenhuma das
  seis espécies do time da fonte tem Mega.
- **Bianca, Nate/Rosa e Cheren 2 entraram na leva 2** (decisão do condutor,
  22/08/2026), com ids 2529 a 2536:

| batalha | id | mapa deste repo | ace | gimmick | lendário |
|---|---|---|---|---|---|
| `TRAINER_UNOVA_BIANCA` | 2529 | `Unova_PWTBattleRoom`, NPC que já existia mudo | 232 | Z Musharna | Cresselia |
| `TRAINER_UNOVA_CHEREN_2` | 2530 | `Unova_OpelucidBattleHouse` (4,2) | 253 | Z Stoutland | Regigigas |
| `TRAINER_UNOVA_{NATE,ROSA}_{SNIVY,TEPIG,OSHAWOTT}` | 2531-2536 | `Unova_NimbasaParkOutside` (6,9) | 255 | Mega Froslass | Meloetta |

  - **A moldura de torneio da Bianca NÃO foi portada, e isso é decisão**: na fonte
    ela é `scene_script` + `priorityjump` na entrada do mapa + `setmapscene` +
    `warpcheck` (`PWTBattleRoom.asm:8-16`, `:59-61`), e o diagnóstico aberto na
    0.l diz que `warp` dentro de script portado não troca de mapa. Entrou a
    BATALHA, pendurada no NPC que o import já tinha deixado com `script: "0"`,
    com os textos da fonte.
  - **As seis variantes de Nate/Rosa vieram inteiras**, com o ramo da fonte
    comando a comando (`NimbasaParkOutside.asm:127-156`): primeiro
    `checkplayergender`, depois `VAR_STARTER_MON`, e o inicial testa só DOIS
    valores porque o terceiro cai por fallthrough, exatamente como os dois
    `checkevent` de lá. O mapa inicial→rival é o da fonte e dá a vantagem de tipo
    ao JOGADOR (Snivy enfrenta a variante Oshawott), que é o mesmo mapa que o
    `Unova_ChampionsRoom` já usa para a Juniper.
  - **Cheren 2 leva o MESMO Regigigas do Cheren líder**, e é a regra e não
    descuido: a proibição de repetir lendário vale entre pessoas diferentes.
  - **Gimmick por medição, não por gosto**: Bianca e Cheren 2 ganharam Z porque
    nenhuma das espécies da fonte deles tem Mega; Nate/Rosa ganharam Mega no
    **Froslass**, a única das seis espécies da fonte com entrada na
    `form_change_tables.h`, e por isso o `gimmick_slot` deles é o 3 e não o ace.
    Dynamax e Terastal seguem em 5 e 6, intocados.
  - **Níveis pela mesma reta**: Bianca ace 45 da fonte → 232; Cheren 2 ace 68 →
    253; Nate/Rosa ace 76 → satura em 255.

**Os níveis não foram escolhidos a dedo.** Cada um saiu do MESMO ajuste linear que
os irmãos já obedecem, e a conta está em `NIVEL_MEDIDO`, no importador:

- Silver: os quatro aces daqui (45, 60, 68, 82) contra os quatro da fonte (5, 18,
  24, 40) dão `nível = 40,69 + 1,0601 × fonte`, resíduo máximo de 2. Nos aces 48,
  64 e 68 isso dá **92, 109 e 113**. Os dois últimos passam do teto de 100 da
  faixa de Johto de propósito: são batalhas de pós-jogo, e a
  `TRAINER_JOHTO_GIOVANNI` já está em 114 com a palavra do Gui.
- Plasma: Giallo 30→219, Bronius 36→224, Gorm 45→232 e Zinzolin 57→242 dão
  `nível = 192,5 + 0,885 × fonte`, que reproduz **os quatro exatamente**. O ace 40
  do Ryoku 1 cai em **228**.
- N e Hugh têm ace 73 na fonte e a mesma reta daria 257: os dois **saturam em
  255**, o MAX_LEVEL desta build.

### A sala do N era um beco, e foi consertada movendo o N

`Unova_NsRoom` tem UM warp, em (0,4), com comportamento `MB_NON_ANIMATED_DOOR`, e
porta larga o jogador UM tile ao sul, em **(0,5)**. O (0,5) faz fronteira só com
(1,5) e (0,6), que são parede, e com o próprio warp: para sair de lá o jogador
PISA no warp e volta para a Victory Road. Com o N na posição da fonte, (5,2), ele
era inalcançável, e a suíte provou isso antes de qualquer conserto.

**Mover o warp não servia, e isso é medição e não palpite**: a varredura do
comportamento dos metatiles do layout inteiro diz que **(0,4) é o ÚNICO tile do
mapa que dispara warp**. Warp em coordenada nova não dispararia, e o jogador
ficaria preso de vez, que é pior do que o beco.

O conserto foi o mais barato que existia: **o N foi para (0,4)**, a própria porta,
com `FLAG_HIDE_UNOVA_N`, e some depois da batalha, que é o que a fonte também faz
(`disappear NSROOM_N`, `maps/NsRoom.asm:43`). Ele bloqueia a saída até a batalha,
que é exatamente o papel dele na cena. Só posição de objeto mudou; nada de
geometria, nada de save. T143.11 prova que a batalha abre e T143.12 prova o
bloqueio: os mesmos dois UP que antes levavam o jogador para
`MAP_UNOVA_VICTORY_ROAD_CASTLE_OUTSIDE` agora param em (0,5).

### As regras próprias do papel `vilao`

1. **Tema por equipe, cobrado pelo guarda**: Rocket veneno/sombrio/normal, Magma
   fogo/terra, Aqua água/sombrio, Galáctica psíquico/sombrio/aço e, na Plasma,
   **o tipo do próprio sábio na fonte** (Zinzolin gelo, Gorm água, Giallo
   elétrico, Bronius fogo, Ryoku grama), porque a Plasma não tem tipo único. Cada
   linha declara `tema`, e o `--demo` reprova tanto vilão SEM tema quanto vilão
   cujo time caiu fora do tema que ele mesmo declarou. Os tipos saem do
   `species_info` pelo `catalogo_especies`; espécie escrita por macro (Genesect,
   Darmanitan, Sawsbuck) não tem tipo legível e conta como FORA, que é o lado
   seguro.
2. **6 Pokémon, menos na PRIMEIRA batalha de cada equipe por região**, onde a
   contagem segue a fonte + 1, pelo mesmo motivo das primeiras batalhas de rival:
   Giovanni do Hideout 5, Proton do Slowpoke Well 4, Tabitha do Mt. Chimney 5,
   Shelly do Weather Institute 3, Mars do Valley Windworks 3 e Giallo do Nimbasa
   Park 4. Da segunda em diante, 6.
3. Mega em todo chefe que tenha Pokémon com Mega (39 dos 40), IV 31, EV
   252/252/4, natureza, habilidade, item e quatro golpes em todos, e as mesmas
   oito flags de IA do resto da Fase F (batalha de vilão é toda simples, então o
   `ACE_POKEMON` fica).

### O caso T138

`dev_scripts/testes_criticos/138_viloes.json`. O **T138.1** herda a rota já medida
do T103.1 até o Cyrus do Galactic HQ, com LV.5 ligado, e lê as SEIS espécies e os
itens dos slots 4 e 5 direto de `gParties` pelo `--timeinimigo`, como o T128.5:
`ITEM_METAGROSSITE` no ace é o único campo da suíte que reclamaria se a pedra
caísse do time, e mutação plantada (`item5` esperado 855) reprovou. O **T138.2** é
o par negativo: MESMA rota até a última tecla de caminhada, sem nenhum `A` para
avançar as falas, e então a batalha não abre, o oponente fica em 0 e o `especie5`
fica em 0. Sem ele o T138.1 não separaria "a batalha carregou o time" de "a
leitura pegou lixo que já estava na EWRAM desde o boot".

## O que fica para o próximo bloco

1. **Treinador comum**: intocado. Se o Gui quiser subir o piso, o corte é
   `gens69_treinadores.py` parte 2, que continua válido para eles.
2. **Bloco cumprido em 22/08/2026: as batalhas que não existiam.** A fonte foi
   medida (tabela na seção "A FONTE FOI MEDIDA"). Entraram **seis**: as três de
   Silver, a `RYOKU1`, o N e o Hugh. **Ghetsis, Shadow Triad, Courtney e Charon
   saíram da fila como INEXISTENTES**, e não como pendentes: nenhum dos quatro é
   treinador com time em fonte nenhuma. Kyurem para o Ghetsis e Reshiram/Zekrom
   para o N deixaram de ser hipótese: o N ficou com **Kyurem-Branco**, porque
   Reshiram é da Juniper e Zekrom é do Giallo, na mesma região. Ficaram de fora,
   e existem na fonte: **Bianca** (moldura de torneio do PWT), **Nate/Rosa**
   (seis variantes atrás de ramo de gênero e de inicial) e **Cheren 2**
   (revanche). **Os três entraram na leva 2 do mesmo dia**, por decisão do
   condutor, e com eles a fila de importação de batalha de chefe fica VAZIA:
   não sobrou treinador com time em fonte nenhuma que este repo não tenha.
3. **Rematches de líder de Hoenn** (`ROXANNE_2` a `JUAN_5`, 40 batalhas) e os
   `KAREN_1..5`: fora do escopo porque são o sistema de revanche por Match Call,
   não a linha principal.
4. **Os grunts de equipe vilã** (78 blocos só de Rocket, mais os de Magma, Aqua,
   Galáctica e Plasma) seguem sendo treinador comum, e a `TRAINER_JOHTO_ROCKET_ETO`
   com eles: só os executivos e os chefes entraram.
5. **Galar** não tem treinador nenhum; a Liga de Galar é fase futura nomeada na 0.h.
