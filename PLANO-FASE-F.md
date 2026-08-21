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

## Contagem: 144 batalhas de chefe

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
- **Hoenn**: Roxanne Regirock, Brawly Urshifu-Rapid, Wattson Thundurus-T, Flannery Heatran, Norman Regigigas, Winona Ho-Oh, Tate&Liza Cresselia, Juan Suicune, Sidney Darkrai, Phoebe Giratina-Origin, Glacia Glastrier, Drake Regidrago, Wallace Kyogre, Steven Rayquaza, Brendan Groudon, May Latias.
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

## O que fica para o próximo bloco

1. **Chefes de equipe vilã** (Rocket, Magma/Aqua, Galáctica, Plasma): não entraram
   nesta rodada por decisão do condutor. São o próximo alvo natural, com a mesma
   tabela e o mesmo gerador.
2. **Treinador comum**: intocado. Se o Gui quiser subir o piso, o corte é
   `gens69_treinadores.py` parte 2, que continua válido para eles.
3. **Rematches de líder de Hoenn** (`ROXANNE_2` a `JUAN_5`, 40 batalhas) e os
   `KAREN_1..5`: fora do escopo porque são o sistema de revanche por Match Call,
   não a linha principal.
4. **Galar** não tem treinador nenhum; a Liga de Galar é fase futura nomeada na 0.h.
