# Glossário de Galar: português do demake -> inglês do cartucho 2

Escrito em 06/09/2026 pelo executor do lote D da onda 1 da Frente A, na branch
`cartucho-2`, para atender a **decisão 32 do Gui** (`PRD-CARTUCHO-2.md`):
tradução **fiel** do português do demake para o inglês, sem reescrita autoral,
com glossário fixo dos termos do motor.

**Uma grafia por termo.** Se a coluna "inglês" tem uma forma, ela é a única que
pode aparecer em `dev_scripts/traducao_galar.json` e em qualquer texto novo de
Galar. O demake escreve o mesmo lugar de cinco jeitos (`Hammerlock`,
`Haammelock`, `hammelock`, `hammerlocke`, `Hammerlocke`); a tradução escreve
`Hammerlocke` sempre.

**Como cada linha foi levantada.** A coluna "como aparece no demake" saiu de
`grep -ohiE` nos cinco arquivos que guardam TODO o texto de Galar
(`data/scripts/galar_fala.inc`, `galar_treinadores.inc`, `galar_objetos.inc`,
`galar_placas.inc`, `galar_cenas.inc`), com a contagem ao lado; não saiu de
memória. A coluna "inglês" prefere, nesta ordem: (1) a forma que **o motor
deste repo** já usa, com o arquivo citado; (2) a forma oficial de Espada e
Escudo quando o motor não tem o termo.

**Onde o texto de Galar mora, e é uma correção de mapa mental:** não é em
`data/maps/Galar_*/scripts.inc`. Os 438 `scripts.inc` de Galar têm **zero**
`.string` (`grep -l '.string' data/maps/Galar_*/scripts.inc | wc -l` -> 0). Os
1.120 blocos de texto da região estão nos cinco `.inc` de `data/scripts/`
listados acima.

---

## 1. Lugares de Galar

**O motor já tem todos**, na tabela de letreiro `src/data/map_popup_names.h`,
que a rodada 13 escreveu. Ela grava em CAIXA ALTA porque é letreiro; em fala, a
grafia é a normal da coluna da direita.

| como aparece no demake | inglês (uma grafia) | fonte |
|---|---|---|
| Postwick | Postwick | `map_popup_names.h:sPopupNome_Postwick` |
| Wedgehurst | Wedgehurst | `map_popup_names.h:sPopupNome_Wedgehurst` |
| Motostoke, MOTOSTOKE | Motostoke | `map_popup_names.h:sPopupNome_Motostoke` |
| Turffield, turffield | Turffield | `map_popup_names.h:sPopupNome_Turffield` |
| Hulbury, HULBURY | Hulbury | `map_popup_names.h:sPopupNome_Hulbury` |
| Hammerlock, Hammerlocke, hammerlock, hammelock, Haammelock | **Hammerlocke** | `map_popup_names.h:sPopupNome_Hammerlocke` |
| Ston-on-side, stow-on-side | **Stow-on-Side** | `map_popup_names.h:sPopupNome_StowOnSide` |
| Ballonlea | Ballonlea | `map_popup_names.h:sPopupNome_Ballonlea` |
| Circhester, Chicerster, chichester | **Circhester** | `map_popup_names.h:sPopupNome_Circhester` |
| Spikemuth, Spikemurth, spikemuth | **Spikemuth** | `map_popup_names.h:sPopupNome_Spikemuth` |
| Wyndon | Wyndon | `map_popup_names.h:sPopupNome_Wyndon` |
| wild area, Wild area, Wild Area | **Wild Area** | `map_popup_names.h:sPopupNome_WildArea` |
| glimwood tangle, Glimwood | **Glimwood Tangle** | `map_popup_names.h:sPopupNome_GlimwoodTangle` |
| galar mine | **Galar Mine** | `map_popup_names.h:sPopupNome_GalarMine` |
| coroa tundra, Crown Tundra | **Crown Tundra** | `map_popup_names.h:sPopupNome_CrownTundra` |
| (não aparece em fala) | Isle of Armor | `map_popup_names.h:sPopupNome_IsleOfArmor` |
| (não aparece em fala) | Slumbering Weald | `map_popup_names.h:sPopupNome_SlumberingWeald` |
| cofre (de Hammerlocke) | **the Vault** | oficial SwSh (Hammerlocke Vault) |
| Rose Tower, torre | Rose Tower | `map_popup_names.h:sPopupNome_RoseTower` |
| Motostoke Stadium, estádio | Motostoke Stadium / Wyndon Stadium | oficial SwSh, e `sPopupNome_*` por cidade |
| galar, Galar, galr a | **Galar** | nome da região |
| jotho | **Johto** | região do motor |
| kalos | **Kalos** | região |
| rota N, Rota N | **Route N** | `map_popup_names.h:sPopupNome_RouteN` |

Cuidado com `rota 10` e afins: em Galar o demake usa a numeração de Galar
(Route 1 a Route 10), que colide de nome com a de Kanto/Sinnoh no mesmo repo.
Traduzir é só `Route 10`; **não** renumerar.

Sobra de FireRed que o demake deixou dentro dos grupos de Galar e que **já está
em inglês, não se traduz e não se "conserta"**: `Celadon Mansion`,
`Manager's Suite`, `Silph Co. Head Office`, `Mt. Moon`, `Tunnel Entrance`,
`Underground Path`, `Cerulean City`, `Vermilion City`, `Rest House`,
`Center Area`, `Area 1/2/3`.

## 2. Personagens

Nome próprio não se traduz; ele só se **corrige** para a grafia oficial. A
coluna do meio existe porque o demake erra caixa e letra.

| como aparece no demake | inglês (uma grafia) | quem é |
|---|---|---|
| Hop | Hop | rival |
| Leon | Leon | campeão |
| Sonia | Sonia | assistente da Magnolia |
| (não aparece em fala) | Magnolia | professora |
| Rose, presidente Rose, PRESIDENTE, Mr. Rose, Sr.Rose | **Chairman Rose** (1ª menção) / **Rose** | presidente da Macro Cosmos; `Chairman` é o título oficial |
| Oleana | Oleana | secretária do Rose |
| (não aparece em fala) | Bede | rival |
| Marnie | Marnie | rival |
| Piers | Piers | líder de Spikemuth |
| team Yell, team yell, Team yell, Team Yell | **Team Yell** | torcida da Marnie |
| Milo, milo | **Milo** | líder de Turffield, grama |
| Nessa | Nessa | líder de Hulbury, água |
| Kabu | Kabu | líder de Motostoke, fogo |
| Bea, bea | **Bea** | líder de Stow-on-Side, lutador |
| Allister, Allister1 | **Allister** | líder de Stow-on-Side, fantasma |
| Opal | Opal | líder de Ballonlea, fada |
| Gordie | Gordie | líder de Circhester, pedra |
| Melony | Melony | líder de Circhester, gelo |
| Raihan | Raihan | líder de Hammerlocke, dragão |
| MUSTARD, Mustard, Dojo Master Mustard | **Mustard** | mestre do Master Dojo |
| Klara | Klara | rival da Isle of Armor |
| (não aparece em fala) | Avery | rival da Isle of Armor |
| Peony | Peony | explorador da Crown Tundra |
| Eternatus | Eternatus | lendário |
| BallGuy | **Ball Guy** | mascote da liga (duas palavras, oficial) |

**Elenco próprio do demake** (autores e amigos que se puseram no jogo). Nome
fica como está, byte a byte; só a fala em volta é traduzida: `Pcl.g`,
`Felipe Mx`, `Sasukezin69`, `Planeta P.`, `Clayton Santos`, `Martha Santos`,
`Eurico`, `Isadora`, `Jon`, `Tommy`, `Lucas`, `Celina`, `Ruan`, `Juan`, `Hyde`,
`Lord`, `Coronel.Phene`, `Cloves`, `hanna`, `Nya`, `Frank`, `Bolt`, `Speary`.

## 3. Mecânica de Galar

| como aparece no demake | inglês (uma grafia) | fonte |
|---|---|---|
| Dynamax, Dynamaxed, Dynamaxing | Dynamax / Dynamaxed / Dynamaxing | oficial SwSh |
| gigantamax, Gigantamax | **Gigantamax** | oficial SwSh |
| max geyser | **Max Geyser** | oficial SwSh (movimento Max) |
| Gym Challenge | Gym Challenge | oficial SwSh, e o demake já escreve assim |
| Copa dos Campeoes | **Champion Cup** | oficial SwSh |
| desafiante, Desafiante | **Gym Challenger** (no contexto do desafio) / **challenger** | oficial SwSh |
| ginasio, ginásio, Ginasio, Gym | **Gym** | oficial |
| lider de ginasio, líder de ginásio, Lider de Ginásio | **Gym Leader** | oficial |
| campeão, campeao, Campeoes | **Champion** / **Champions** | oficial |
| insignia, insiguina, insiguia | **Badge** | oficial; `Gym Badge` quando a frase precisa |
| Centro Pokémon | **Pokémon Center** | oficial; o `é` sai do charmap deste repo |
| fly taxi | **Flying Taxi** | oficial SwSh |
| curry | **curry** | oficial SwSh (Curry Dex) |
| Cenouras da Neve | **Iceroot Carrot** | oficial Crown Tundra (a que chama Glastrier) |
| Cenouras Negras | **Shaderoot Carrot** | oficial Crown Tundra (a que chama Spectrier) |
| sementes (guia de sementes) | **Carrot Seeds** | oficial Crown Tundra |
| montaria do rei, pokémon cavalo do rei | **the King's steed** | descrição do Calyrex; o demake não nomeia |
| usina (subterrânea) | **(underground) Power Plant** | oficial SwSh |
| Dojo Master | **Dojo Master** (a pessoa) / **Master Dojo** (o prédio) | oficial Isle of Armor |
| Macro Cosmos | Macro Cosmos | oficial SwSh |
| Rotom Phone | Rotom Phone | oficial SwSh |
| mini game, minigame (do ginásio) | **Gym mission** | oficial SwSh chama a prova de ginásio de Gym mission |

## 4. Termos do motor (item, golpe, habilidade, classe)

Aqui a fonte é o código deste repo, não a Bulbapedia.

| demake | inglês | fonte no motor |
|---|---|---|
| Luxury Ball | Luxury Ball | `src/data/items.h:405` |
| POÇÕES, poção | **Potions / Potion** | `src/data/items.h:634` |
| Poké Ball | Poké Ball | `src/data/items.h:197` |
| Berries, Berry, BERRY | **Berries / Berry** | `src/data/items.h` (`ITEM_PLURAL_NAME`) |
| Aguav Berries | **Aguav Berries** | `src/data/items.h:11171-11172` |
| Mail | Mail | item do motor |
| Sand-Attack | **Sand Attack** (sem hífen) | `src/data/moves_info.h:766` |
| Dream Eater | Dream Eater | `src/data/moves_info.h:3758` |
| Clear Body | Clear Body | `src/data/abilities.h:228` |
| Pickup | Pickup | `src/data/abilities.h:408` |
| Flame Body | Flame Body | `src/data/abilities.h:378` |
| Magma Armor | Magma Armor | `src/data/abilities.h:311` |
| Pokédex, pokedex | **Pokédex** | nome do motor |
| pokémon, Pokémon, Pokemon, pokemons, Pokémons | **Pokémon** (invariável no plural) | `src/data/pokemon/species_info/` |
| tipo Ground / Poison / dark / fada / lutador / insetos / gelo / fantasma | **Ground-type / Poison-type / Dark-type / Fairy-type / Fighting-type / Bug-type / Ice-type / Ghost-type** | tipos do motor |
| estatisticas | **stats** | vocabulário do motor |
| habilidade | **Ability** | vocabulário do motor |
| movimentos, técnicas | **moves** | vocabulário do motor |
| nivel | **level** | vocabulário do motor |
| HP | HP | vocabulário do motor |
| item retido | **held item** | vocabulário do motor |
| PC, rede de PC | **PC / PC network** | vocabulário do motor |
| Sala da União | **Union Room** | vocabulário do motor |
| fita (de concurso) | **Ribbon** | `src/data/text/ribbon_descriptions.h` |
| hall da fama | **Hall of Fame** | vocabulário do motor |

**Espécies citadas em fala** (grafia do motor, conferida em
`src/data/pokemon/species_info/`): Wooloo, Corviknight, Duraludon, Impidimp,
Morpeko, Applin, Rookidee, Coalossal, Eternatus, Mr. Rime, Marowak, Combee,
Togepi, Chansey, Pidgey, Pidgeot, Croconaw, Spearow, Zigzagoon, Eevee, Dratini,
Charmander, Abra, Mew, Dragonite, Raikou, Pikachu. O demake escreve
`wooloos`, `Woolo`, `Duraludons`, `Pidey`, `pikachu`; a tradução escreve o nome
do motor, e o plural em inglês é o próprio nome (`Wooloo`, não `Wooloos`).

**Classe de treinador.** A tabela do motor é `gTrainerClasses`
(`src/battle_main.c:302`) e ela grava em CAIXA ALTA (`COOLTRAINER`,
`BLACK BELT`, `SCHOOL KID`), porque é a caixa de batalha do RSE. **Isso vale
para a tabela, não para a fala**: dentro de um `.string`, classe de treinador é
substantivo comum e vai em caixa normal (`a Bug Catcher`, `the Gym Leader`). O
de-para de classe da fonte para classe do motor já existe e não se refaz aqui:
`CLASSES_NOVAS_GALAR.md`, na raiz.

## 5. Decisões de tradução que valem para o arquivo inteiro

Fielmente quer dizer **mesmo sentido e mesma quantidade de informação**. Não é
licença para melhorar o texto.

1. **Erro de digitação e de gramática do demake NÃO é reproduzido em inglês.**
   `dificeis`, `otima`, `incrivel`, `Perder fede!\nNo é nada legal.` viram
   inglês correto. Reproduzir o erro seria reescrita autoral ao contrário, e o
   PRD pede tradução, não paródia. O erro fica registrado no `pt` da entrada do
   JSON, que guarda o original exato.
2. **Piada e gíria brasileira viram o equivalente natural em inglês**, sem
   trocar a piada por outra: `5000 pilas` -> `5,000 bucks`, `Que merda...` ->
   `Damn it...`, `Toca aí!` -> `High five!`.
3. **Quebra da quarta parede fica.** As falas que citam a ROM, o save state, o
   Nintendo Switch e os autores são conteúdo do demake e são traduzidas como
   estão, não apagadas.
4. **Token de controle é intocável**: `{PLAYER}`, `{COLOR ...}`, `\n`, `\l`,
   `\p`, o `$` final. Eles saem da tradução na mesma ordem e na mesma
   quantidade em que entraram; só o ponto onde `\n` e `\l` caem pode mudar,
   porque a requebra por pixel é que decide isso.
5. **A largura manda na quebra, não o gosto.** Toda tradução passa pelo
   requebrador de `dev_scripts/texto_placas_sinnoh.py` (`requebra`,
   `largura_px`), 208 px por linha, duas linhas por caixa, a mesma régua do
   `dev_scripts/qa/checa_texto.py`.
6. **Texto que já está em inglês não é retraduzido** nem "melhorado", só tem a
   grafia de lugar e de personagem conferida contra as seções 1 e 2.

## 6. O que ficou de fora do de-para, e por quê

`dev_scripts/traducao_galar.json` tem **849 entradas** (530 textos distintos)
dos 1.120 blocos de Galar. Os 271 que não entraram, por motivo:

| motivo | blocos | exemplo |
|---|---|---|
| já está em inglês | 28 | `GalarObj_G02M10_o1_Text0` = `Please come again!` |
| não tem idioma (grito, reticências, nome, letreiro em inglês) | 241 | `...`, `Boom!`, `Zzz...`, `Rest House`, `Mt. Moon\nTunnel Entrance` |
| **mojibake, precisa de decisão** | 2 | ver abaixo |

Os dois blocos de mojibake **não foram traduzidos de propósito**, porque
traduzir esconderia um defeito de dado:

1. `data/scripts/galar_fala.inc`, rótulo `GalarFala_G09M10_o14_Text`:
   `Você ja viu o ginasio de\nhammelock?ゅ Você ja viu o ginasio de\nhammelock?`
   A frase está duplicada e colada por um `ゅ` que não é do charmap latino. É a
   ÚNICA das 310 falas de português de Galar que sobra sem tradução, e por isso
   o T07 de Galar cai de 310 para **1**, não para 0, quando o aplicador rodar.
2. `data/scripts/galar_fala.inc`, rótulo com o corpo `ÍÔ ゅぞャËÌÉフÁ`: é tabela
   de caractere errada aplicada a texto japonês, e não há o que traduzir.

Um terceiro caso ficou traduzido mas merece o olho do revisor:
`You can’t become a goAgora você vai ter que ir!` (índice 519 do levantamento) é
uma frase em inglês truncada colada numa frase em português. A tradução manteve
a colagem, porque consertar seria inventar a metade que o demake perdeu.

**Apóstrofo:** o demake escreve `’` (U+2019) e a tradução escreve `'` (U+0027).
Os dois viram o **mesmo byte 180** no `charmap.txt` deste repo, então não há
diferença nenhuma na tela; não é divergência a corrigir.
