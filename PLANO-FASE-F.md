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
própria mais abaixo; com eles a tabela vai a **184 batalhas e 970 Pokémon**.

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

- **Johto**: existem exatamente **quatro** entradas de Silver com time próprio,
  `TRAINER_JOHTO_RIVAL_SILVER_1` a `_4`, e **as quatro estão na Fase F**. O
  HGSS enfrenta o Silver sete vezes; as outras três nunca foram importadas. Ou
  seja o que falta é **importação de Johto**, não elenco da Fase F.
- **Unova**: o espaço `TRAINER_UNOVA_*` tem 403 constantes e **nenhuma de
  rival**. O BW3G não trouxe rival nenhum: os `TRAINER_BIANCA`, `TRAINER_HUGH` e
  `TRAINER_NATE` que existem no `.party` são NPCs de HOENN (Route 111, Route 119
  e o ginásio de Mossdeep), homônimos e não os rivais de Unova. O Cheren de lá é
  líder de ginásio (`TRAINER_UNOVA_LEADER_CHEREN`), como em BW2.
- Varredura fechada: **zero** treinadores com `RIVAL` no nome e time próprio
  ficaram fora da tabela de chefes.

Portanto o item de fila é **importar as três batalhas de Silver que faltam e os
rivais do BW3G**, e só depois dar time a eles com o mesmo gerador.

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

**Nem Groudon nem Kyogre ganharam o orbe de Primal**: seguem com `ITEM_LEFTOVERS`
e `ITEM_CHOICE_SPECS`, os itens que já carregavam com Brendan e Wallace. A Primal
Reversion é gimmick à parte do Mega e entraria POR CIMA da Mega Camerupt do Maxie
e da Mega Sharpedo do Archie, quebrando o "um gimmick por chefe" sem que o guarda
visse, porque ele só conhece pedra de Mega e cristal Z.

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
2. **Bloco pendente: IMPORTAR as batalhas que não existem** (adiado pelo Gui em
   22/08/2026, depois da rodada dos vilões). São as três batalhas de Silver, a
   `RYOKU1`, os rivais do BW3G e, do lado vilão, **Ghetsis, N, o Shadow Triad,
   Courtney e Charon**. Medido aqui: nenhuma delas existe em
   `src/data/trainers.party` nem em `include/constants/opponents.h`, e "GHETSIS"
   só aparece como TEXTO em três `scripts.inc` de Unova.
   **Este bloco depende de a FONTE ter essas batalhas, e ninguém mediu isso
   ainda**: o BW3G pode simplesmente não trazer o Ghetsis nem o N como treinador,
   do mesmo jeito que não trouxe rival nenhum, e o HGSS pode não ter a `RYOKU1`.
   **Quem executar MEDE a fonte primeiro** e só depois promete elenco; enquanto
   isso, Kyurem para o Ghetsis e Reshiram/Zekrom para o N não são decisão tomada,
   são hipótese. O Zekrom, hoje, está com o Giallo, e o Kyurem-Preto com o
   Genesis.
3. **Rematches de líder de Hoenn** (`ROXANNE_2` a `JUAN_5`, 40 batalhas) e os
   `KAREN_1..5`: fora do escopo porque são o sistema de revanche por Match Call,
   não a linha principal.
4. **Os grunts de equipe vilã** (78 blocos só de Rocket, mais os de Magma, Aqua,
   Galáctica e Plasma) seguem sendo treinador comum, e a `TRAINER_JOHTO_ROCKET_ETO`
   com eles: só os executivos e os chefes entraram.
5. **Galar** não tem treinador nenhum; a Liga de Galar é fase futura nomeada na 0.h.
