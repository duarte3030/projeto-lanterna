# Estado do hack, e como trabalhar nele

Ponto de entrada. Leia este arquivo antes de qualquer coisa; ele diz onde o
projeto está, o que já foi decidido, e as armadilhas que já custaram sessões
inteiras. Detalhe fica nos documentos apontados no fim.

Última medição: 06/09/2026, na build da rodada 13, os dois primeiros consertos do playtest do Gui (o
letreiro de mapa e a música de Johto). A seção 0.u abaixo é a passagem de bastão dela, e a 0.t é a da
rodada 12.

---

## 0.u O LETREIRO DE MAPA PARA DE DIZER "SINNOH WEST" E JOHTO PARA DE TOCAR CAVERNA: O NOME DO POPUP SAI DO MAPSEC, E O DE-PARA DE MÚSICA SAI DE PETALBURG WOODS, 05-06/09/2026 (rodada 13; os dois primeiros defeitos achados pelo Gui no playtest, um executor Opus cada)

O Gui jogou a ROM `23d` e trouxe o primeiro defeito do playtest: o letreiro que aparece ao entrar num
mapa dizia **"SINNOH WEST", "SINNOH EAST", "SINNOH NORTH", "UNOVA EAST", "GALAR NORTH"** em centenas de
mapas de quatro regiões. Não era dado errado, era o desenho: `MAPSEC` é `u8` e divide o espaço de
valores com `METLOC_SPECIAL_EGG` (0xFD), então Johto, Sinnoh, Unova e Galar **não têm uma seção por
cidade**, e cada lugar é APELIDO de um MAPSEC de GRUPO
(`src/data/region_map/region_map_sections.constants.json.txt`). Como `GetPopUpMapName` copiava
`gRegionMapEntries[mapsec].name`, o letreiro só sabia dizer o nome do grupo. Medido antes de tocar:
**398 mapas de Sinnoh carregavam o MAPSEC de grupo cru** no `region_map_section` e **172 mapas de Galar
estavam em `MAPSEC_GALAR_POSTWICK`**, que era o valor padrão errado de interiores de outras cidades
(Turffield, Wyndon, Wild Area, Isle of Armor).

### O mecanismo novo: o nome do letreiro deixa de ser o MAPSEC

MAPSEC continua `u8` e os apelidos continuam onde estavam. O "met location" do sumário do Pokémon
segue por GRUPO, e isso é aceito. O que mudou é só o letreiro, em quatro peças:

1. **Campo opcional `"map_name_popup"` no `map.json`**, com a string já no formato exibido
   ("SUNYSHORE CITY"). `tools/mapjson` lê o `map.json` por CHAVE (`generate_map_header_text`) e
   **ignora campo que não conhece**: conferido antes de escrever, e por isso o header do mapa não
   mudou um byte.
2. **`dev_scripts/nomes_popup.py`**, o gerador. Deriva o nome nesta ordem: (a) NOME DA PASTA por
   dicionário de radicais, que é a única fonte que sobrou em Sinnoh e em Galar; (b) o APELIDO do
   `region_map_section` transformado (`MAPSEC_UNOVA_R_11` -> "ROUTE 11", `MAPSEC_GALAR_ROUTE01` ->
   "ROUTE 1"), que é a fonte boa em Johto e Unova, onde o demake carregou o apelido certo em cada
   mapa; (c) o que sobra vai para `dev_scripts/qa/nomes_popup_revisao.csv` e **não recebe campo**,
   caindo no comportamento antigo. Interior herda o lugar da cidade, mapa TÚMULO (`MAPSEC_NONE`) fica
   fora, e Kanto e Hoenn ficam fora porque têm MAPSEC próprio. Ele é **idempotente** (rodar duas vezes
   dá 0 arquivos alterados na segunda) e tem `--demo` com 25 casos.
3. **`src/data/map_popup_names.h`, GERADO no build**, não versionado, como
   `region_map_entries.h` já é: um passo em `map_data_rules.mk` com todos os `map.json` como
   pré-requisito o refaz sozinho, e `$(C_BUILDDIR)/map_name_popup.o` depende dele. Um literal por nome
   distinto (**224** no total, compartilhados entre regiões: "ROUTE 5" e "VICTORY ROAD" servem Unova e
   Galar ao mesmo tempo), um array de ponteiros por grupo de mapa que tem nome (**55** grupos) e a tabela de grupos com o tamanho de cada um.
4. **`GetPopUpMapName` ganhou `mapGroup`/`mapNum`** e consulta a tabela antes de cair no MAPSEC. O
   par vem de `gSaveBlock1Ptr->location`, que é exatamente de onde `gMapHeader` é carregado
   (`src/overworld.c:674`), porque `struct MapHeader` não guarda grupo nem número. Celadon Dept.,
   andar e Battle Pyramid continuam como estavam, e o teste "Map names fit in popup" de `test/text.c`
   passou a medir também os nomes novos, agora que recebe o par.

### O que entrou, e o que ficou de fora

| região | mapas com nome | sem nome | nomes distintos |
|---|---|---|---|
| Johto | 220 | 0 | 54 |
| Sinnoh | 394 | 4 | 70 |
| Unova | 280 | 2 | 68 |
| Galar | 438 | 0 | 44 |

Dos 1.332, **317 mostram o letreiro hoje** (`show_map_name` verdadeiro): 66 em Johto, 56 em Sinnoh, 70
em Unova e 125 em Galar. Os outros 1.015 são interiores que hoje não mostram nada, e ganharam o campo
assim mesmo, para que ligar o letreiro num deles amanhã não precise passar por aqui de novo.

**1.332 mapas ganharam o campo** e o CSV de revisão tem **147 linhas**: 6 são "não resolveu" de
verdade (`Cafe`, `Restaurant`, `ForeignBuilding` e `UnusedGateBetweenEternaCityRoute206` em Sinnoh,
`Unova_MobileBattleRoom` e `Unova_MobileTradeRoom`, que são salas de link sem lugar no mundo) e as
outras 141 são **aviso de divergência**, onde a PASTA mandou e o apelido dizia outra coisa: são os
interiores de Galar presos no `MAPSEC_GALAR_POSTWICK`. O aviso fica no CSV de propósito, porque a
divergência é o retrato do defeito do `region_map_section` de Galar, que continua aberto.

### A régua de largura entrou no gerador

O teste `Map names fit in popup` cobra 80 px na `FONT_NARROWER`, e o buffer do letreiro tem 20
caracteres. O gerador mede o nome **mais o sufixo de andar** com a tabela real
(`gFontNarrowerLatinGlyphWidths` de `src/fonts.c` e o `charmap.txt`), e nome que não couber vai para o
CSV em vez de entrar. Medido: o mais largo é **"OLIVINE LIGHTHOUSE", 71 px de 80**, e nenhum dos mapas
nomeados tem andar. Foi essa régua que encurtou "POKEMON WORLD TOURNAMENT" (94 px) para
"WORLD TOURNAMENT".

### A prova está no framebuffer, e é um par antes/depois

Cinco warps pelo menu de debug, PNG por passo, abertos e olhados. Na ROM `23d`, o MESMO warp e a
MESMA rota: `SunyshoreCity` (grupo 75, mapa 13) escrevia **"SINNOH EAST"** e `Galar_Wyndon01`
(grupo 127, mapa 11) escrevia **"GALAR NORTH"**. Na build desta rodada os mesmos dois escrevem
**"SUNYSHORE CITY"** e **"WYNDON"**, e mais: `AzaleaTown` (84, 3) escreve "AZALEA TOWN" no lugar de
"SINNOH WEST", `Unova_NimbasaCity` (107, 0) escreve "NIMBASA CITY" no lugar de "UNOVA EAST", e
`PetalburgCity` (0, 0), que é o controle de Hoenn e não tem campo nenhum, continua escrevendo
"PETALBURG CITY".

### O que fica aberto

- **Porymap não conhece o campo.** `tools/mapjson` ignora chave desconhecida, mas um editor gráfico que
  reserialize o `map.json` inteiro pode deixar `map_name_popup` para trás. Se algum mapa perder o
  campo, `python3 dev_scripts/nomes_popup.py` o repõe sozinho, e o `make` refaz a tabela.
- **Os 172 mapas de Galar em `MAPSEC_GALAR_POSTWICK` continuam lá.** O letreiro deles já está certo,
  mas o `region_map_section` não, e é ele que o sumário do Pokémon e o mapa da região leem. As 141
  linhas de aviso do CSV são a lista exata do conserto, e ele é obra de dados de Galar, não deste
  mecanismo.
- **Seis mapas seguem sem nome próprio** e caem no comportamento antigo: quatro de Sinnoh
  (`Cafe`, `Restaurant`, `ForeignBuilding`, `UnusedGateBetweenEternaCityRoute206`) e as duas salas de
  link de Unova. Precisam de decisão de conteúdo, não de código.

### O segundo defeito do playtest: a música de Johto, 06/09/2026

O Gui trouxe "toda cidade de Johto toca música de caverna". Não era mapa e não era arte de som: era
**de-para de apelido**. Em `include/constants/songs.h`, **23 apelidos `MUS_HG_*`** apontavam para
`MUS_PETALBURG_WOODS`, que nesta build também era o destino de `MUS_CAVE`, `MUS_ROCK_TUNNEL` e
`MUS_SHOAL_CAVE`. Medido antes de tocar: **159 dos 236 mapas dos grupos `*_Johto`** resolviam na mesma
faixa 366, cidade, rota, ginásio, loja e caverna no mesmo som. Nenhuma outra região tinha o problema.

O conserto é troca de constante, **zero arte de som e zero byte de ROM** (32.360.228 B antes e
depois): as faixas de destino já estavam todas na ROM. Cada apelido passou a apontar para uma faixa
com **número próprio** em `songs.h` e `.s` em `sound/songs/midi/`, conferido um a um, porque
`MUS_RG_*` nem sempre entra em build baseada em Emerald.

| apelido | faixa | por quê |
|---|---|---|
| `MUS_HG_NEW_BARK` | `MUS_LITTLEROOT` | vila natal pequena |
| `MUS_HG_CHERRYGROVE` | `MUS_OLDALE` | vilarejo vizinho calmo |
| `MUS_HG_VIOLET` | `MUS_RG_FUCHSIA` | cidade tradicional serena |
| `MUS_HG_AZALEA` | `MUS_VERDANTURF` | vila tranquila |
| `MUS_HG_GOLDENROD` | `MUS_RG_CELADON` | metrópole com loja |
| `MUS_HG_ECRUTEAK` | `MUS_SOOTOPOLIS` | cidade mística tradicional |
| `MUS_HG_OLIVINE` (novo) | `MUS_RG_VERMILLION` | cidade portuária |
| `MUS_HG_CIANWOOD` | `MUS_DEWFORD` | ilha litorânea isolada |
| `MUS_HG_MAHOGANY` (novo) | `MUS_FALLARBOR` | vila serrana pequena |
| `MUS_HG_BLACKTHORN` (novo) | `MUS_EVER_GRANDE` | cidade de montanha |
| `MUS_HG_ROUTE29` | `MUS_ROUTE101` | primeira rota campestre |
| `MUS_HG_ROUTE30` | `MUS_RG_ROUTE1` | rota inicial arborizada |
| `MUS_HG_ROUTE34` | `MUS_ROUTE104` | rota larga litorânea |
| `MUS_HG_ROUTE26` | `MUS_ROUTE120` | rota final úmida |
| `MUS_HG_ROUTE42` | `MUS_ROUTE113` | rota de montanha |
| `MUS_HG_GYM` | `MUS_GYM` | ginásio, direto |
| `MUS_HG_POKE_MART` | `MUS_POKE_MART` | loja, direto |
| `MUS_HG_GAME_CORNER` | `MUS_GAME_CORNER` | cassino, direto |
| `MUS_HG_ELM_LAB` | `MUS_RG_OAK_LAB` | laboratório de professor |
| `MUS_HG_ROCKET_TAKEOVER` | `MUS_RG_ROCKET_HIDEOUT` | ocupação da Rocket |
| `MUS_HG_DANCE_THEATER` | `MUS_CONTEST_LOBBY` | casa de espetáculo |
| `MUS_HG_NATIONAL_PARK` | `MUS_SAFARI_ZONE` | parque natural |
| `MUS_HG_ICE_PATH` | `MUS_RG_MT_MOON` | caverna fria |
| `MUS_HG_DRAGONS_DEN` | `MUS_CAVE_OF_ORIGIN` | caverna mística |
| `MUS_HG_UNION_CAVE` | `MUS_RG_SEVII_CAVE` | caverna comum |
| `MUS_HG_ROCK_TUNNEL` | `MUS_RG_SEVII_DUNGEON` | túnel subterrâneo |

**As dez cidades de Johto têm dez faixas distintas**, conferido por contagem, e caverna só nas quatro
masmorras, cada uma com a sua. Os três apelidos mortos que criavam a armadilha (`MUS_CAVE`,
`MUS_ROCK_TUNNEL`, `MUS_SHOAL_CAVE`, **zero uso** em `map.json` e em código) saíram de Petalburg
Woods também, para que o próximo que os usar não recrie o defeito.

**Catorze `map.json` corrigidos**, que é a herança tosca do import: `OlivineCity` tocava a faixa de
Violet e as seis dependências dela a de Cherrygrove; `Mahoganytown` e `MahoganyTown_House1` tocavam a
de Cherrygrove; as quatro de `BlackthornCity` tocavam a de Azalea; e `MahoganyTown_Shop`, que é loja,
tocava a de Azalea e virou `MUS_HG_POKE_MART`.

**A prova é do emulador, e tem par antes/depois.** `dev_scripts/prova_musica_johto.py` warpa por
debug e lê DUAS camadas: `gMapHeader.music` (o header que o motor carregou) e
`gMPlayInfo_BGM.songHeader` (o ponteiro que o driver de som está tocando naquele quadro), este último
traduzido de volta para o número da faixa procurando o ponteiro em `gSongTable` dentro do binário. Os
dois endereços saem do `pokeemerald.map`. Na ROM `2026-09-05`, que é a que o Gui jogou, Goldenrod, New
Bark, Olivine, Blackthorn, a Rota 29, o ginásio de Violet, a loja de Cherrygrove e o Ice Path leem
**366 nos dois**, ou seja Petalburg Woods; nesta build leem **521, 405, 525, 422, 359, 364, 404 e
500**, cada um a sua. `PetalburgCity` é o controle de Hoenn e lê **362 nas duas ROMs**. O `gba_runner`
ganhou `--mem16` e `--mem32`, leitura crua de endereço, porque nenhuma das duas provas passa por
SaveBlock1.

### Os portões

**Suíte 1.002 de 1.003**, com o T11.3 contado à parte, e **T11 3/3** contra a ROM
`roms/pokemon-claude-2026-08-18.gba`, que é a última ANTES do `SAVE_LAYOUT_REVISION` de 19/08 (a fonte
dela é a worktree de `cf6786b2ae` em `/private/tmp/claude-501/t11-r13`). Build verde com o lock,
**ROM 96,44% de 32 MB** (32.360.228 B, **1.194.204 B livres**, 9.632 B a mais
que a 0.t, que é o custo inteiro da tabela e das strings), **EWRAM 86,16% e IWRAM 86,68%**, idênticos
aos da 0.t. **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%), 2.400 mapas, 2.252 ids de
treinador e 1.716 apelidos conferidos: não há mudança de struct, de índice nem de flag nesta rodada, e
o campo novo mora no `map.json`, que não entra na save. `valida_rom.py` com os 2.400 mapas declarados
dentro da ROM. `dev_scripts/qa/roda_qa.py --demo` verde nas quatro varreduras, e
`dev_scripts/nomes_popup.py --demo` com 25 casos.

**Os portões foram REFEITOS INTEIROS depois do conserto da música de Johto (06/09/2026), e deram os
MESMOS números**, o que é a prova de que a troca de constante não custou nada: build verde com o lock,
**ROM 32.360.228 B, byte a byte o mesmo tamanho**, EWRAM 86,16% e IWRAM 86,68% iguais, **suíte 1.002 de
1.003** com o T11.3 à parte, **T11 3/3** contra a mesma `roms/pokemon-claude-2026-08-18.gba`,
**SAVE COMPATIVEL** (música não mora na save), `valida_rom.py` com os 2.400 mapas dentro da ROM,
`roda_qa.py --demo` verde nas quatro varreduras e `prova_musica_johto.py` com **9 de 9** mapas certos
no header e no driver de som, contra **1 de 9** na ROM `2026-09-05`.

### Duas lições

1. **Pasta de `.sav` em `/tmp` é veredito falso esperando acontecer.** Seis casos de prova de save
   (T123.21, T123.22, T127.3, T127.4, T127.9, T127.10) abriram VERMELHOS na primeira passada, e o
   motivo não era o jogo: `/tmp/claude-501/fechador` e `/tmp/claude-501/frenteGalar` tinham sido
   limpos pelo sistema desde a rodada 12, e o `gba_runner` respondia "nao consegui abrir sav". O
   conserto ficou em `dev_scripts/testa_critico.py`, na função `roda`, que agora cria a pasta do
   `.sav` antes de chamar o runner; com ela, os dois blocos voltaram 25/25 e 10/10 sem tocar em mais
   nada.
2. **Campo de `map.json` que o `mapjson` não conhece é grátis, e a tabela tem que sair DELE, não da
   derivação.** A primeira versão do gerador montava o `.h` a partir do dicionário de radicais, e não do
   campo que ele mesmo tinha acabado de escrever: quem editasse `map_name_popup` à mão veria o
   `map.json` mudar e o letreiro continuar igual, sem uma linha de erro. Hoje `--tabela` lê SÓ o
   campo, e é esse passo que o `make` chama. Provado trocando o campo de `SunyshoreCity` por
   "PROVA DO CAMPO" e vendo o `.h` mudar sozinho.

### O defeito dos prédios que Hoenn e Johto dividem: entrar por Johto e sair na Rota 111, 06/09/2026

Relato do Gui: "entrei em Trainer Hill por Olivine City (Johto) e quando fui sair, saí na Rota 111, em
Hoenn". Medido antes de tocar: a praça `TrainerHill_Courtyard`, que é a praça de instalações que o
demake de HGSS põe ao norte da Route 40 (ligada a ela pela conexão e pelo
`MAP_GATE_ROUTE40_TRAINER_HILL_COURTYARD`) e que o item **F5 da 0.j** completou com a porta para a
Battle Frontier, tem cinco warps, e **quatro deles
entram em prédios COMPARTILHADOS com Hoenn**: `MAP_TRAINER_HILL_ENTRANCE` em (12,10) e os três lobbies
de Battle Tent, `FALLARBOR` em (27,19), `VERDANTURF` em (20,28) e `SLATEPORT` em (34,28). A saída dos
quatro era warp FIXO de Hoenn (`TrainerHill_Entrance` (9,16) e (10,16) para `MAP_ROUTE111` warp 4, e
cada lobby para a sua cidade), então **o mesmo defeito acontecia quatro vezes, e não uma**. O quinto
warp, (24,29) para o `BattleFrontier_OutsideWest` warp 11, foi conferido e está CERTO: os dois lados
são recíprocos e a volta é a seta ao sul, que o T126.3 já mede desde 21/08.

#### O mecanismo: o retorno é o `dynamicWarp`, e quem o grava é o motor

Nenhum mapa foi copiado e nenhum bit de save foi gasto. A saída dos quatro prédios virou
`MAP_DYNAMIC` / `WARP_ID_DYNAMIC`, que é o mesmo idioma dos elevadores e do `InsideOfTruck`, e quem
preenche o destino é o próprio motor: em `SetupWarp`
(`src/field_control_avatar.c:1131`), quando o warp em que o jogador vai POUSAR é dinâmico, ele chama
`SetDynamicWarp` com o mapa e o ÍNDICE do warp de onde o jogador veio. Ou seja, entrar já grava por
onde sair, com a mesma animação de porta e o mesmo tile de chegada de antes, porque o retorno guarda
`warpId` e não coordenada crua. `dynamicWarp` já existe no `SaveBlock1` desde o Emerald: **custo de
save ZERO**.

O que o motor NÃO faz é repor esse retorno depois que outra coisa reescreve o `dynamicWarp`, e dentro
das tendas isso acontece sempre: `InitFallarborTentChallenge` e as duas irmãs (`src/battle_tent.c:115,
178, 234`) apontam o `dynamicWarp` para o PRÓPRIO lobby, porque é dele que `SaveGameFrontier`
(`src/frontier_util.c:2534`) tira o ponto de "Continuar" de quem salva no meio do desafio. Sem
reposição, ao voltar da sala de batalha a porta do lobby devolveria o jogador para dentro do lobby, e
ele não sairia nunca mais. Por isso os quatro mapas de entrada ganharam `MAP_SCRIPT_ON_TRANSITION`
chamando o special novo `DefinirRetornoPredioCompartilhado` (`src/field_specials.c`), que **repõe o
retorno a partir do `escapeWarp`** quando ele aponta para mapa fechado. O `escapeWarp` é o registro
que o próprio motor faz da última entrada de mapa aberto para mapa fechado (`UpdateEscapeWarp`,
`src/overworld.c:774`): ele guarda o mapa de fora e o tile uma linha abaixo da porta, e nenhum passo
dado dentro do prédio o altera, porque lobby, corredor e sala de batalha são todos fechados.

Conferido e sem volta fixa para Hoenn em lugar nenhum: as saídas por elevador, derrota e desistência
do Trainer Hill (`data/scripts/trainer_hill.inc:40,52` e `TrainerHill_Elevator/scripts.inc:37`) voltam
todas ao `Entrance`, cuja porta é a dinâmica; as salas de batalha das três tendas voltam ao LOBBY, não
à cidade; e nenhum `HEAL_LOCATION` nem `setrespawn` aponta para esses prédios (a enfermeira do Trainer
Hill cura e não marca respawn).

#### A prova é do emulador, e o par negativo é a outra porta

`dev_scripts/testes_criticos/171_predios_compartilhados.json`, **10 casos, 10 verdes**, todos lendo
mapa e posição do `SaveBlock1`. **T171.1**: entra no Trainer Hill pela praça de Johto e sai em
`MAP_TRAINER_HILL_COURTYARD` (12,11). **T171.2**, o par negativo, é o MESMO prédio com o MESMO
roteiro entrando pela Route 111: sai em `MAP_ROUTE111` (31,114), que é a regressão zero de Hoenn.
**T171.3**: entra por Johto, vai ao `TRAINER_HILL_1F`, volta ao `Entrance` e só então sai; cai na
praça, o que prova que o retorno atravessa os andares de dentro. **T171.4**: o mesmo caminho menos os
últimos passos, o jogador entra e FICA no capacho (9,16), o que separa "a porta funciona" de
"qualquer tile devolve para a praça". **T171.5 a T171.8** fecham as três tendas: Verdanturf pela
praça (20,29) e por Verdanturf Town (3,8), Fallarbor pela praça (27,20) e Slateport pela praça
(34,29).

E os PNGs foram abertos, porque memória não desenha tela. No último quadro do T171.1 o jogador está de
pé embaixo do portal escuro do Trainer Hill, entre os dois postes acesos da praça, com o mato fechado
à esquerda e o paredão à direita; no do T171.2, o MESMO prédio, o cenário é a rocha roxa da Route 111,
sem poste nenhum. O T171.3 termina com o quadro idêntico ao do T171.1. No T171.5 o jogador está
embaixo da cúpula da Battle Tent com a fileira de postes e a grade d'água da praça atrás; no T171.6, a
MESMA cúpula, mas cercada pelo capim e pela cerca de Verdanturf Town, com dois NPCs da cidade. Dois
mapas diferentes, o mesmo prédio, a mesma porta.

O par **T171.9 e T171.10** é o adversarial, e existe porque os oito primeiros exercitam só o
automático do motor: se o special fosse um `return` vazio, os oito passariam igual. Quem suja o
`dynamicWarp` no jogo é o desafio da tenda, que este harness não joga até o fim, então o par usa um
sujador equivalente e alcançável, o **elevador da loja de Lilycove**, cujo
`setdynamicwarp MAP_LILYCOVE_CITY_DEPARTMENT_STORE_5F, 2, 1`
(`LilycoveCity_DepartmentStoreElevator/scripts.inc:98`) aponta o retorno para um mapa FECHADO do outro
lado do mundo. O **T171.9** é o controle: depois do elevador, sair pela porta dele cai mesmo em
`MAP_LILYCOVE_CITY_DEPARTMENT_STORE_5F` (2,2), ou seja o retorno está sujo de verdade. O **T171.10**
carrega esse mesmo estado para dentro do lobby da tenda e sai pela porta: cai na praça de Johto em
(20,29), e não na loja. Sem a reposição, ele cairia na loja.

#### O que fica aberto

- **Duas funções com a MESMA regra nasceram na mesma rodada.** A frente das lojas compartilhadas de
  Sinnoh (Veilstone e Oreburgh, que reaproveitam a loja e o museu de Lilycove) escreveu
  `DefinirSaidaPelaPortaDeEntrada` em `src/retorno_dinamico.c` com a mesma guarda. As duas devem virar
  UMA; quem consolidar não precisa reabrir a decisão, só escolher o nome.
- **O "Continuar" de quem salva no meio de um desafio de tenda muda de tile.** Depois que o
  `ON_TRANSITION` repõe o retorno, um `tent_save` feito DENTRO do lobby grava o ponto de continuação
  fora da tenda, e não no lobby como no Emerald original. O jogador reaparece na praça (ou na cidade)
  em frente à porta, com o desafio ainda pausado, e retoma entrando de novo. É diferença de tile, não
  de estado: nada trava e nada se perde.
- **O letreiro e o mapa da região continuam dizendo Hoenn dentro desses quatro prédios**, porque o
  `region_map_section` deles é o de Hoenn e é ele que essas telas leem. Quem entra pela praça de Johto
  vê "FALLARBOR TOWN" no lobby da tenda da esquerda. É dado de mapa, não deste mecanismo.

#### Os portões desta frente

Build verde numa worktree ISOLADA (`/private/tmp/claude-501/predios`, HEAD `fccccc0265` mais só este
conserto), porque a árvore compartilhada estava com outra frente no meio de uma obra e não linkava.
**ROM 32.360.292 B, 96,44% de 32 MB**, ou seja **+64 B** sobre os 32.360.228 B que a frente da música
mediu neste mesmo HEAD, e é esse o custo inteiro do conserto; **EWRAM 86,16% e IWRAM 86,68%**,
idênticos aos da 0.t e da 0.u. **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%), 2.400
mapas, 2.252 ids de treinador e 1.716 apelidos conferidos: nenhuma flag, var, item, mapa ou índice
novo. `valida_rom.py` com os 2.400 mapas declarados dentro da ROM. `valida_conectividade.py` com **0
warps quebrados** e os mesmos 4 / 12 / 1.966 de 2.289 que a MESMA ferramenta dá na árvore SEM o
conserto (medido numa worktree de `b7ef40f330`, o HEAD de antes da rodada): o campo
`destinos_dinamicos` dos quatro `map.json` mantém o grafo de alcance honesto, já que a ferramenta pula
`MAP_DYNAMIC` de propósito. `valida_warp_tile.py --piso 60` em 5.915 de 6.875 (86,0%), idêntico à
0.t. `guarda_colisao_vars` com 23 colisões herdadas, 0 novas e 0 stub. `dev_scripts/qa/roda_qa.py
--demo` verde nas quatro varreduras.


---

## 0.t A CAÇA A BUGS ANTES DO PLAYTEST: A RÉGUA PARA DE MEDIR PORCENTAGEM E PASSA A MEDIR DEFEITO, 23/08/2026 (rodada 12; condutor Opus, quatro executores Opus, fechador Opus)

Build verde, uma build só, e a primeira rodada em que **nenhuma coluna de completude era o alvo**: o
que a régua não mede é jogo travando, cena abrindo na pessoa errada, texto cortado e mapa alcançável
no papel e intransitável no cartucho. **A varredura de QA caiu de 39 travas para 22 e de 2.244
prováveis para 1.972**, e as quedas são obra e medição, não recalibragem de conveniência.

**ROM 96,41% de 32 MB** (32.350.596 B, **1.203.836 B livres**, 10.120 B a mais que a 0.s), **EWRAM
86,16% e IWRAM 86,68%**, idênticos aos da 0.s, **Dex obtenível 1.571 de 1.571 e ZERO inobtenível**.
**Suíte 1.002 de 1.003, ZERO reprovado**, com o T11.3 pulado na varredura (ele só prova algo com duas
ROMs); a varredura inteira foi REFEITA pelo fechador sobre a ROM `23d` e deu o mesmo 1.002/1.003, com
**T143.9 verde**, que antes já tinha sido rodado sozinho CINCO vezes e passado nas cinco. **T11 3/3**
contra a build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`). Blocos novos: **T163 4/4, T164 4/4, T165 10/10, T166 4/4, T167 5/5, T168 5/5** (dois do
Deoxys) e **T169 8/8**, o adversarial. **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B (94,3%),
**2.054 layouts e 2.400 mapas**, os 2.400 dentro da ROM, 2.252 ids de treinador e 1.716 apelidos
conferidos; `guarda_colisao_vars` com 23 colisões herdadas, **0 novas** e 0 stub;
`valida_conectividade` com **0 warps quebrados**; `valida_warp_tile --piso 60` em 5.915 de 6.875
(86,0%), nenhuma região abaixo do piso; `valida_mapas_sinnoh --so-sinnoh` com `'sprite': 0` e 0 mapas
com problema; os quinze `--demo` de ferramenta tocada verdes, mais `dev_scripts/qa/roda_qa.py --demo`
nas quatro varreduras. ROM oficial **`roms/pokemon-claude-2026-08-23d.gba`**
(md5 `b6cdb072b9fd904215c21a544df389d8`), com o `.map`, e o MESMO binário em
`roms/pokemon-claude-teste-2026-08-16.gba`.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 100,8% | 100,1% | 100,4% | -- | 55 (0) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 100% | 101,5% | 103,7% | 103,5% | -- | 39 (18) | 267 |
| Unova | 100% | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | 103,6% | 100% | 70,3% | 59,2% | 48 (32) | 0 |

### Três lentes, e a tabela de QA antes e depois

**(1) A varredura estática** (`dev_scripts/qa/`, quatro ferramentas, 8.746 achados no começo) lê a
árvore e acha CANDIDATO em escala. **(2) O emulador** (`testa_critico.py`) roda o jogo e lê a EWRAM, e
PROVA o fato. **(3) O olho no framebuffer**, o PNG que o `gba_runner` grava, aberto e olhado, a única
que responde "a caixa está desenhada e a linha cabe". Nenhuma substitui a próxima. Abaixo,
`roda_qa.py`, a MESMA ferramenta, em `010cc1dd67` e na árvore desta rodada:

| classe | Kanto | Johto | Hoenn | Sinnoh | Unova | Galar | comum | total |
|---|---|---|---|---|---|---|---|---|
| trava, antes | 5 | **19** | 2 | 0 | 0 | 0 | 13 | **39** |
| trava, depois | 5 | **2** | 2 | 0 | 0 | 0 | 13 | **22** |
| provável, antes | 373 | 108 | 811 | 130 | 141 | **264** | 417 | **2.244** |
| provável, depois | 359 | 104 | 759 | 121 | 137 | **76** | 416 | **1.972** |
| cosmético, antes | 718 | 449 | 1.538 | 2.085 | 1.154 | 475 | 42 | 6.461 |
| cosmético, depois | 718 | 444 | 1.538 | 1.929 | 1.154 | 474 | 42 | 6.299 |
| falso positivo | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 |
| falso positivo, depois | 11 | 0 | 48 | 0 | 0 | 0 | 2 | **61** |

As duas linhas que mais andaram dizem onde a obra foi: **Johto perdeu 17 das 19 travas** e **Galar
perdeu 188 prováveis**.

### As quatro frentes

**Galar.** Os 127 blocos `nointro` (`lock`/`faceplayer`/`goto_if_set`/`trainerbattle_no_intro`/`end`)
viraram `trainerbattle_single` + `msgbox GalarTrn_Depois_*` + `release`. **108 objetos dividiam id de
treinador** e por isso nasciam vencidos junto com o gêmeo; a numeração passou a ser por OBJETO, ids
publicados intactos e **60 ids novos em append, 3208 a 3267**. Alocadores de flag e var viraram
append-only com os 16 endereços repostos nos da 22f, e `guarda_save.py` ganhou guarda de apelido.

**Johto.** Sete travas de verdade na raiz, `release` e `waitstate` fora de ordem. Ho-Oh, Lugia e
Deoxys tinham UMA flag de esconder pendurando dois ou três objetos em regiões diferentes; cada mapa
ganhou apelido na faixa 0x1BB4, custo zero de var. Unown invisível em tile sólido, e três espécies da
Dex realocadas para mapa vivo.

**Sinnoh.** **203 textos requebrados por pixel**, contra a caixa de 208 px e não por contagem de
caractere. O rival do Pokecenter da Liga voltou **na posição 7 da lista**, e não no fim, porque
`local_id` sem nome é a POSIÇÃO mais um: com ele fora, o `addobject 7` da cena mirava a PICNICKER do
canto, que fazia o "!", andava até o jogador, lutava como BARRY e sumia do mapa para sempre. Três
NPCs ligados por `ON_TRANSITION`, `VerityLakefront` com `warp`/`waitstate`/`releaseall` na ordem
canônica, `GalacticHQ_Hall` de 34 para 15 objetos na janela e `Restaurant` de 19 para 15, e 69
túmulos repovoados limpos.

**Resto.** O seletor de capítulo passou a acender **FLAG_BADGE01..08_GET por ÍNDICE**: os oito golpes
de campo perguntam por elas e mais nada (`src/field_move.c`), e a coluna `flagInsignia` do seletor só
É a insígnia do motor em KANTO, então quem pulava para "Before CANDICE" ganhava um Pikachu com Surf,
Rock Smash e Strength que o motor RECUSAVA em cinco das seis regiões. Capítulo 0 continua sem insígnia
(T99 2/2). Twist Mountain portada no gerador, Driftveil por `ON_TRANSITION`, três `dual_connection` de
Unova consertadas (15 órfãos para 3), e a QA promovida para `dev_scripts/qa/`.

### Os falsos positivos PROVADOS (a régua não via o mecanismo)

**Azalea e Blackthorn**: quem tira o jogador dali é `applymovement`/`setmetatile`, e a régua procurava
`release`. **E4 de Kanto** (Lorelei, Bruno, Agatha): o warp 0 pousa em tile sólido, blockdata IDÊNTICO
ao `pokefirered`, e quem tira o jogador é o `ON_FRAME` com `Common_Movement_WalkUp5`, porque
`applymovement` de script não consulta colisão. **Sevii, 162 mapas fora do grafo de warp**: portão de
ENREDO intacto, a balsa é `special DoSeagallopFerryScene` e a corrente Blaine -> Bill -> TRI PASS está
inteira. **Hearthome e ThreeIsland**: o mapa TROCA DE LAYOUT no `ON_TRANSITION`, e não é
`setmetatile`, que foi o que a auditoria procurou e não achou.

### O Deoxys ganha caminho, e a porta é a que a ROM já tinha

`FLAG_HIDE_DEOXYS` nunca ser apagada é **falso positivo**: é idioma vanilla, o Deoxys entra por
`addobject` quando o triângulo é resolvido. A outra metade era verdade: o menu da balsa de Lilycove
cobra **BOLSA E FLAG** (`src/script_menu.c:853`), o Seagallop de Vermilion cobra o mesmo par, e o
único `giveitem ITEM_AURORA_TICKET` do repo mora **dentro do Mystery Gift, que este cartucho não
tem**: as duas Birth Island eram alcançáveis no grafo de warp e sem porta no jogo. O conserto segue a
regra que a pesquisa de lendários já tinha escrito ("não copiar o gate por Mystery Gift") e usa o
guarda-chuva que a ROM já usa para item-chave que ninguém entrega: o Aurora Ticket virou a **décima
linha de `chaves`** e sai pelo MESMO NPC do laboratório, com `setflag
FLAG_ENABLE_SHIP_BIRTH_ISLAND` colado no `additem`. **Nenhum mapa novo, nenhum estático movido, custo
ZERO de save**, e o portão de ENREDO fica de pé: a atendente só atende com `FLAG_SYS_GAME_CLEAR`,
então Deoxys continua pós-Liga. **T168.4 e T168.5.**

### Os cinco casos adversariais (T169, 8 casos)

1. **Galar, vencer e falar de novo.** Dito por inteiro: vencer de verdade no harness NÃO dá, o time
   de Galar é `Level: 255` e o Pikachu 20 do seletor não ganha; plantar a flag do id é o MESMO estado
   de save. O que este caso tem a mais que o T163.3 é a camada da afirmação: **o PNG foi aberto e a
   caixa de pós-batalha está desenhada, com texto dentro**, e depois dela o jogador anda.
2. **Johto, capítulo alto, Surf e Strength.** Liga de Johto, oito insígnias. Surf em
   `OlivineCity_PortOutside`, escolhido por varredura dos 236 mapas atrás de "warp cuja linha reta
   bate em água funda com corredor limpo e água terminando em PAREDE": a Route41, candidata óbvia,
   tem oito TILES DE WARP em fila na linha de caminhada. Strength no ginásio de Cianwood, o único
   lugar de Johto com bloco de Strength e script próprio. **Os dois com par negativo em "Start of
   region"**, que prova que quem destrava é o capítulo, e não o Pikachu.
3. **Sinnoh, o texto no framebuffer.** Das 433 linhas acrescentadas, a mais larga em mapa alcançável
   por rota curta tem **200 px de 208** e está em `VeilstoneCityNortheastHouse`. **PNG aberto: as duas
   linhas cabem, sem letra cortada e sem terceira linha.**
4. **Accumula, T143.9, cinco vezes seguidas: 5/5.**
5. **O gêmeo atravessa o desligamento.** T169.7 planta a flag do gêmeo PUBLICADO (0x10BE, id 3006) e
   SALVA sem falar com ninguém; T169.8 abre em CONTINUAR **sem acender flag à mão** e a batalha que
   abre é `TRAINER_GALAR_ISADORA_22_3`, id 3250.

### O que a caça achou DENTRO do próprio ferramental

Cinco vermelhos que ninguém via porque um `assert` anterior sempre caía primeiro. (a) **Três espécies
da Dex moradas em DOIS lugares**: a realocação de Johto pôs cópia nos mapas novos e deixou as
originais na órfã Diglett's Cave, e como `encontros_base()` desfaz a escrita pela coluna
`substituido`, o censo-base voltava a vê-las e o plano as dava por obtidas; os três slots voltaram a
`SPECIES_DIGLETT`. (b) **Um COMENTÁRIO entregava um item**: `RotomsRoom/scripts.inc:44` cita
`ITEM_ROTOM_CATALOG` dentro de um `@`, e a varredura era regex no texto cru, então o NPC parava de
dar o item e **as cinco formas do Rotom voltavam a inobteníveis sem uma linha de erro**. (c)
**`plano_congelado` cobrava o irreproduzível**: exigia o mesmo par espécie -> casa de cada estático, e
`decide_estaticos` escolhe casa por cota e por lotação, que leem a árvore; passou a cobrar o CONJUNTO
de linhas por balde, e foi essa cobrança que pegou o item (a). (d) **Tabela de encontro VAZIA não é
conteúdo**. (e) **O Masquerain tem estático próprio** desde 22/08 e a régua só aceitava evolução ou
mato: cobrava o caminho em vez do resultado.

E seis casos ficaram vermelhos pela troca de idioma de Galar, **sem defeito de jogo** (T153.1 a
T153.4, T154.5, T154.6): `trainerbattle_single` escreve `gTrainerBattleParameter` no SETUP, ANTES de o
`GetTrainerFlag` desviar para `gotopostbattlescript`, então **`oponente_faixa [0,0]` deixou de
significar "nenhuma batalha começou"** e quem responde isso agora é o time do adversário, carregado só
quando ela começa. E o caminho de quem ainda não venceu ganhou uma caixa: o `nointro` batia direto, o
`single` mostra o texto de entrada e espera botão, então a rota precisa de UM A a mais.

### Lições

1. **`UnlockPlayerFieldControls` é solta no FIM do script, e não pelo `release`.** O `frozen` que o
   `lock` põe é do OBJETO, não do jogador. Ler `lock` sem `release` e gritar "trava" errou 127 vezes
   numa rodada só; o que o `end` seco custava era outro, NPC congelado e zero fala.
2. **Alocador de flag e de var é APPEND-ONLY, sempre.** Reordenar endereço publicado invalida save em
   silêncio, e save inválida é o único defeito desta obra sem conserto.
3. **Túmulo fora do denominador.** Mapa sem warp, sem conexão e com `MAPSEC_NONE` não entra em alcance
   nem em completude; contá-lo faz a régua mentir dos dois lados.
4. **QA mora em `dev_scripts/qa/`**, com uma contagem só, um `--demo` só e os vereditos de calibração
   escritos DENTRO da ferramenta: auditoria fora do repo envelhece sem ninguém ver. E **falso positivo
   que volta todo mês custa mais que o bug**: os 61 reclassificados foram medidos contra o
   `pret/pokeemerald` intocado ou contra o mecanismo real, com arquivo e linha por escrito.

### O que fica aberto

- **Galar: 246 mapas órfãos**, e o retrato NÃO é o que se supunha. Medido nesta rodada: 58 interiores
  de Turffield, 49 da Isle of Armor, 27 de Postwick, 22 interiores de Wyndon, 20 da Crown Tundra, 13
  da Wild Area, 13 da Lost Cave e o resto pulverizado. O grosso é **interior sem porta**, e não DLC:
  86 dos 246 são de DLC. É o maior item da região, e é obra de warp, não de escopo.
- **22 travas e ~1.970 prováveis** ainda na varredura. Não é fila de conserto, é fila de VEREDITO, e
  cada um passa por medir, como os 61 desta rodada. Hoenn concentra 759 prováveis.
- **A fala de Galar é em PORTUGUÊS** (intro e pós-batalha, 308 textos), porque o demake de origem é
  brasileiro; as outras cinco regiões são em inglês. Decisão herdada, não regressão, mas o Gui vai ver
  a troca de idioma ao atravessar.
- **Galar** segue com 70 estáticos dos 1.088, 25 placas, 514 NPCs mudos e `fila_galar.json` em 1.198
  de 3.195; a **pergunta 18** segue sem resposta; **gens 6, 7 e 9** paradas por escopo. Os **90
  canteiros de berry**, as **8 bolas de neve** e os **141 objetos em 49 mapas** de Sinnoh continuam
  onde a 0.s os deixou.
- **Playthrough por região é a PRÓXIMA rodada.** Esta caçou defeito por lente; falta percorrer o
  enredo de ponta a ponta, uma região por vez, que é a única lente que pega ordem de cena e ritmo.

### A ROM `23d` é a candidata ao playtest do Gui

`roms/pokemon-claude-2026-08-23d.gba`, md5 `b6cdb072b9fd904215c21a544df389d8`, com o `.map` ao lado, e
o mesmo binário em `roms/pokemon-claude-teste-2026-08-16.gba`, que é o arquivo que o emulador dele já
aponta. Save antiga continua valendo: `SAVE_LAYOUT_REVISION` segue em 1 e `guarda_save.py` fechou
COMPATIVEL.

---

## 0.s SINNOH FECHA: O ENREDO ENTRA POR FLAG RECALCULADA, O GELO GANHA BATENTE, E A PORCENTAGEM PASSA A MEDIR O QUE VAI FICAR, 23/08/2026 (rodada 11; condutor Opus, três executores Opus, fechador Opus)

Build verde, uma build só, e a rodada em que **Sinnoh passa de 100% nas quatro colunas**: mapas 100%,
**objetos 93,3 → 101,6%**, warps 103,7% e **placas 98,1 → 103,4%**. **ROM 96,38% de 32 MB**
(32.340.476 B, **1.213.956 B livres**, 3.932 B a mais que a 0.r), **EWRAM 86,16% e IWRAM 86,68%**,
os dois idênticos aos da 0.r, Dex obtenível em 1.571 de 1.571. **Suíte 961 de 963**, com o T11.3
pulado na varredura porque ele só prova algo com duas ROMs e **um reprovado que é o T143.9, o
instável conhecido**: ele mora na Accumula Town, que tem quatro NPCs `MOVEMENT_TYPE_WANDER_AROUND`
no caminho da rota, e ele mesmo diz isso no par negativo T143.10. Foi **rodado sozinho três vezes
depois da varredura e passou nas três**; Unova não foi tocada nesta rodada. O bloco novo **T162 em
3/3**; **T11 3/3** contra a build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`).
**SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B, **2.054 layouts e 2.400 mapas**, os 2.400
declarados dentro da ROM, 2.192 ids de treinador conferidos e os 38 chefes de Galar da Fase F
conferidos um a um; `guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags, **0 novas
nos dois perfis** e 0 stub; `valida_conectividade` com **0 warps quebrados**; `valida_warp_tile
--piso 60` em **5.915 de 6.875 (86,0%)**, nenhuma região abaixo do piso; `valida_mapas_sinnoh
--so-sinnoh` com `'sprite': 0` e 0 mapas com problema; os nove `--demo` rodados, oito deles TOCADOS nesta rodada (`completude`,
`bolas_neve_sinnoh`, `cenas_sinnoh_b3`, `porta_morta`, `texto_placas_sinnoh`, `importa_npcs_sinnoh`,
`treinadores_galar`, `guarda_party`, `guarda_save`) verdes. ROM oficial
`roms/pokemon-claude-2026-08-23c.gba` (md5 `1924d5cf6d7c38c2310d1445382e648f`), com o `.map` ao lado, e o MESMO binário em
`roms/pokemon-claude-teste-2026-08-16.gba`.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 100,8% | 100,1% | 100,4% | -- | 55 (0) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 100% | **101,6%** | 103,7% | **103,4%** | -- | 39 (18) | 267 |
| Unova | 100% | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | 103,6% | 100% | 70,3% | 59,2% | 48 (32) | 0 |

### O enredo de Sinnoh entra por flag RECALCULADA, e não por estado inicial

`dev_scripts/cenas_sinnoh_b3.py` trouxe **30 objetos de cena** do Platinum para 18 mapas: 13 que
estão sempre visíveis, 13 de polaridade **"aparece"** e 4 de polaridade **"some"**. Custo de save:
**6 apelidos de flag e ZERO var**. O idioma é o que importa, e ele foi escolhido contra a alternativa
óbvia: pôr `setflag` em `EventScript_ResetAllMapFlags` só roda em JOGO NOVO, e save antiga veria o
ancião de Celestic plantado desde o primeiro dia. Aqui não há estado inicial nenhum para acertar,
porque o `MAP_SCRIPT_ON_TRANSITION` de cada mapa **reescreve a flag toda vez que o mapa carrega**:
acende sempre, e só apaga se o marco já caiu. Save velha e save nova se comportam igual, e nada
entrou em `new_game.inc`.

`dev_scripts/porta_morta.py` mediu mapa a mapa quem tem warp em cima de metatile de porta e achou
**um só em Sinnoh**: a **caverna de Celestic**, onde o pouso do warp alcançava UM tile de 108
andáveis, porque o primeiro passo ao norte pisava na porta e devolvia o jogador à cidade. A porta
virou chão, o tile de pouso virou `MB_SOUTH_ARROW_WARP` (0x208, o metatile que 86 bocas de Sinnoh do
mesmo par de tilesets já usam) e o warp desceu para (10,21). `texto_placas_sinnoh` liberou **39
placas** (7 com texto do próprio banco do Platinum; 3 ficaram de fora por não haver tile de leitura),
e o conserto de `teto_bg` no importador é o que deixou a coluna `placas` sair de 98,1% para 103,4%.
**T161 em 7/7.**

### O gelo: a bola de neve é BATENTE, e o teto real é o de SPRITE

A primeira tentativa trouxe as bolas como bloco de Strength, e a medida derrubou a ideia: o chão do
ginásio é `MB_ICE`, e em tile de gelo o motor entra em movimento forçado ANTES de chegar em
`TryPushBoulder`. Então elas entraram pelo que são: objeto sólido, sem script e sem flag, na
coordenada da fonte. `desliza()` foi **calibrada contra o emulador com 197 sondas** lidas da EWRAM, e
as duas regras que faltavam estão escritas no topo do arquivo. Das 19 bolas do Platinum, **11
entraram e 8 ficaram de fora**: 7 pelo teto de sprite e 1 por acesso. **T115 7/7, T125 12/12 e T157
11/11**, este último em duas passadas.

### A ordem de rodar virou GUARDA, e a guarda foi provada na árvore de verdade

A 0.r deixou escrito que `treinadores_galar.py --aplicar` APAGA a Fase F se rodado sozinho, e que
isso era "disciplina de quem roda". Deixou de ser: `bloco_party` passou a **preservar o AI e os
Pokémon dos 38 chefes** que moram dentro do bloco de Galar, e `dev_scripts/guarda_party.py`, chamado
por `guarda_save.py`, reprova chefe cru. A prova não é só de laboratório: `--aplicar` foi rodado
**na árvore real desta rodada, duas vezes**, e o `git diff` inteiro ficou com o MESMO md5
(`f4a8c6ad0f211bc8c02b5ea5642c15de`) antes e depois, com `opponents.h` e `trainers.party` byte a
byte iguais. Nada precisou de `git checkout`.

### O corte honesto: a régua contava MAPA, e o que faltava era REGISTRO

Ordem do Gui: "vamos completar Sinnoh" e "normalizar a porcentagem com base no que realmente vai
ficar". `CORTES_DO_GUI` tinha dois modos, e os dois eram de MAPA: `mapa_fonte` tira o que a fonte tem
e nós não, `deficit` zera o buraco de um mapa inteiro. Nenhum dos dois enxerga **um tipo de registro
dentro de mapa que fica**, e era exatamente aí que Sinnoh sangrava. Nasceu o terceiro modo,
**`objeto_fonte`**: regex contra o `graphics_id` de cada objeto da fonte, e quem casa sai do
denominador da coluna `objetos` na região inteira.

Os dois grupos, ambos datados de 23/08/2026 e impressos por `--detalhe Sinnoh`:

| grupo | registros | motivo |
|---|---|---|
| Mobiliário sem mecânica | **63** (55 `VENT` em 14 mapas, 8 `BOLLARD` em 3) | desenho com colisão, sem fala, sem item e sem gatilho; este motor não tem objeto decorativo sólido, e NPC de pé em cima de respiro de calçada faz o mapa mentir |
| Canteiros de berry | **90** `BERRY_SOIL` em 23 mapas | o canteiro é ESTADO, e o id da árvore mora na save; corte **com prazo**, cai na primeira janela de save aberta de propósito |

**A trava que torna isso honesto, e ela é medida, não jurada:** o gráfico cortado tem que ter ZERO
ocorrências nos NOSSOS `map.json` da região. Cortar do denominador o que nós usamos seria descontar
de um lado e contar do outro, e a coluna subiria sem obra nenhuma. `confere_cortes` cobra isso, e o
`--demo` tem a mutação plantada: cortar `OBJ_EVENT_GFX_ITEM_BALL`, que Sinnoh usa 167 vezes, reprova.

O **"teto da fonte"** foi MEDIDO e NÃO virou corte, de propósito: mapa em que já pusemos tanto objeto
quanto o Platinum tem déficit ZERO, então o registro dele já não pesa no denominador. A régua já o
tratava; inventar um corte para ele seria maquiagem.

Resultado: objetos de Sinnoh de **2.181 sobre 2.300 (94,8%)** para **2.181 sobre 2.147 (101,6%)**.
O excedente acima de 100 é o mesmo fenômeno de `warps` e `placas`: NPC e cena nossos que a fonte não
tem.

### O que AINDA falta em Sinnoh, nomeado

Depois do corte, **49 mapas ainda têm menos objeto que a fonte, 141 no total**, e `--detalhe Sinnoh`
imprime a lista mapa a mapa. Atribuindo o buraco de cada mapa aos gráficos da fonte que ele não tem
(heurística, e é declarada como tal), o retrato é: **71 obstáculos de HM** (34 `ROCK_SMASH`, 26
`STRENGTH_BOULDER`, 11 `CUT_TREE`), quase todos recusados pelo portão de TRANCA ou de BOLSO, que é o
portão provando que ninguém fica preso; **23 item balls**; **7 bolas de neve**, as recusadas por teto
de sprite; **6 portas animadas** de Elite e do QG, que aqui são warp e não objeto; e **34 pessoas**,
o balde de nome próprio sem sprite mais os 24 objetos de marco sem equivalente nesta ROM. Os piores
mapas são `SinnohVictoryRoad2F` (14 de 32) e `RavagedPath` (13 de 31), os dois de pedra quebrável.

### Lições

1. **O teto real de objeto por sala não é o do mapa, é o de SPRITE.** `gObjectEvents` tem 16 vagas e
   a 0 é do jogador, então sobram 15, e `TrySpawnObjectEvents` simplesmente NÃO acorda o resto quando
   elas acabam: sem erro, sem aviso. Objeto que não acordou não é sólido, e bola de neve que não é
   sólida não para escorregão nenhum. O ginásio de Snowpoint é a janela mais apertada de Sinnoh (20
   objetos: 11 bolas e 9 corpos, com câmera que enxerga as 15 vagas cheias), e o `--demo` agora liga
   o `VAGAS_DE_SPRITE` ao `OBJECT_EVENTS_COUNT` lido do `.h`: quem mexer no motor quebra ali.
2. **Os tiles 192 e 193 PARAM o deslize, e bloqueiam também a SAÍDA.** `MetatileBehavior_IsIce_2` só
   aceita `MB_ICE`, e `IsMetatileDirectionallyImpassable` olha o tile de ORIGEM e o de DESTINO. Sem a
   primeira regra são 12 divergências em 161 medidas; sem a segunda, 6.
3. **Porta de beco: warp em cima de metatile de porta come o primeiro passo.** O mapa fica alcançável
   pelo validador estático e intransitável no jogo. A busca vale a pena e é barata: `porta_morta.py`
   varreu Sinnoh inteira e achou um único caso.
4. **Censo que não reconhece o próprio trabalho mente para baixo.** Os "166 objetos de enredo" que a
   0.r listava eram 169, dos quais **12 já estavam no mapa**, 97 moravam em mapa já no teto da fonte
   e 122 eram mobiliário. Régua e fila envelhecem juntas, e remedir custa minutos.

### O que fica aberto

- **9 divergências residuais** do simulador de gelo contra o motor (o deslize foi encerrado a 7
  tiles, não fechado) e as **8 bolas** que ficaram de fora, 7 delas por teto de sprite: subir isso
  pede reduzir corpo no salão, não calibrar melhor.
- **141 objetos em 49 mapas de Sinnoh**, no retrato da seção acima, mais os **24 objetos de marco sem
  equivalente nesta ROM**, que só andam com a máquina de cenas de Sinnoh avançando.
- **Os 90 canteiros de berry** voltam ao denominador na primeira janela de save aberta de propósito,
  e quem a abrir sobe `SAVE_LAYOUT_REVISION` junto.
- **8 das 10 constantes `OBJ_EVENT_GFX_SINNOH_*` sem uso** continuam sem uso (BUCK, CHARON, CHERYL,
  CRASHER_WAKE, LOOKER, MARS, MAYLENE, PALMER); a leva b3 gastou BYRON e RILEY, uma vez cada.
- **Galar** com 70 estáticos dos 1.088, 25 placas, 514 NPCs mudos por motivo e `fila_galar.json` em
  1.198 de 3.195; **T143.9 continua instável**; a **pergunta 18** (sprites dos 26) segue sem resposta;
  e **gens 6, 7 e 9** seguem paradas por escopo, com o julgamento em `fontes-mapas/PLANO-GENS-6-9.md`.
- **FECHADO nesta rodada**, e a 0.r o listava aqui: `treinadores_galar.py --aplicar` não apaga mais a
  Fase F. Virou guarda, não disciplina, e a prova foi rodada na árvore de verdade.

### A próxima rodada é CAÇA A BUGS, antes de o Gui jogar

As seis regiões estão em cem por cento ou acima nas colunas que a régua mede, e a régua agora só
conta o que vai ficar. O que ela **não** mede é jogo travando, cena abrindo duas vezes, texto
cortado, NPC que fala pela pessoa errada, warp que leva ao lugar certo pelo lado errado. A rodada 12
é de **caça a bugs**, com a ROM na mão, antes do playtest do Gui: procurar defeito, não porcentagem.

---

## 0.r TRÊS CONSERTOS DE IDENTIDADE: O TIL DE GALAR, O ID DE TREINADOR E O SPRITE QUE FALAVA POR OUTRA PESSOA, 23/08/2026 (rodada 10; condutor Opus, um executor Opus, fechador Opus)

Build verde, uma build só, e uma rodada que **não custou um byte**: **ROM 96,37% de 32 MB**
(32.336.544 B, **1.217.888 B livres**), **EWRAM 86,16% e IWRAM 86,68%**, os três idênticos aos da
0.q, e a **régua de completude da 0.q intocada linha por linha**, Dex obtenível em 1.571 de 1.571.
Os três consertos são de NOME e de ÍNDICE, não de conteúdo. **Suíte 949 de 950**, ZERO reprovados,
com o T11.3 pulado na varredura porque ele só prova algo com duas ROMs, e o bloco novo **T160 em
8/8**; **T11 3/3** contra a build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`).
**SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B, **2.054 layouts e 2.400 mapas**, os 2.400
declarados dentro da ROM, e agora também **2.192 ids de treinador conferidos** contra o `e5224a3d67`;
`guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags, **0 novas nos dois perfis** e
0 stub; `valida_conectividade` com **0 warps quebrados**; `valida_warp_tile --piso 60` em **5.915 de
6.875 (86,0%)**, nenhuma região abaixo do piso; `valida_mapas_sinnoh --so-sinnoh` com `'sprite': 0` e
0 mapas com problema; os seis `--demo` tocados (`fala_galar`, `glifo_til`, `treinadores_galar`,
`guarda_save`, `importa_npcs_sinnoh`, `sprites_sinnoh`) verdes. ROM oficial
`roms/pokemon-claude-2026-08-23b.gba` (md5 `ec560cb869964788a5a4f1880179c325`), com o `.map` ao lado,
e o MESMO binário em `roms/pokemon-claude-teste-2026-08-16.gba`.

### O til: byte certo com glifo errado engana a ida e volta

A 0.q fechou dizendo que os `ä` de Galar eram "obra de fonte, não de script, porque o gerador tem ida
e volta byte a byte pelo charmap, então os BYTES estão certos". Estava certa pela metade. A fonte (o
demake `ultimate-plus-v1.2.1.2`, base FireRed) escreve "não" como `E2 F4 E3`, medido byte a byte em
`0x818376`, e REDESENHOU como til o glifo do `F4`, que no FireRed é o trema alemão `ä`. O nosso
`charmap.txt` ainda chamava `F4` de `ä`, então o tradutor decodificava `ä` e o assembler reencodava
`ä` no mesmo `F4`: **a ida e volta fechava, e o defeito nunca virou erro de build**, com o jogador
lendo "N-trema-o" em 315 lugares. A verificação media o BYTE; o errado era a LETRA.

O `charmap.txt` passou a chamar `F1 F2 F4 F5` de `Ã Õ ã õ`, e `dev_scripts/glifo_til.py` redesenhou
os quatro glifos nos **nove** `graphics/fonts/latin_*.png` sem inventar pixel: o til vem do `Ñ` e do
`ñ` do MESMO arquivo, sobreposto ao `A O a o` do MESMO arquivo, e tinta da letra nunca é apagada.
**`Ü` (`F3`) e `ü` (`F6`) continuam trema**, os únicos tremas vivos do repo, por causa do "JÜRGEN" de
`src/data/battle_frontier/apprentice.h`: conferido no fechamento, célula por célula nos nove PNG, que
**só `F1 F2 F4 F5` mudaram de desenho**. Varridos `data/`, `src/`, `include/` e `tools/` em UTF-8 e
em latin-1 atrás de trema fora de Galar, **nenhuma ocorrência**: nenhum texto de Kanto, Johto, Hoenn,
Sinnoh ou Unova usava `F4` como `ä` de verdade. Os quatro `.inc` regerados dão **0 trema, 317 til**,
e o `fala_galar --demo` ganhou quatro casos que medem a letra, com mutação plantada.

### O id de treinador é APPEND-ONLY, como o de mapa e o de layout

A 0.q registrou que `TRAINER_GALAR_LEON_736` e `_739` tinham ido de 3204/3205 para 3206/3207 com o
`guarda_save.py` dizendo SAVE COMPATIVEL, "certo pela régua dele e mudo sobre a vitória que mudava de
dono". A flag de "já venci este treinador" é `TRAINER_FLAGS_START + id` e mora na save: **id de
treinador é índice de save**, e vale a regra dos mapas e dos layouts, quem existe não se move e quem
entra entra no fim. O `numera()` de `treinadores_galar.py` passou a ler o de-para do próprio
`opponents.h` e só dá vaga nova a quem ainda não tem, os dois Leon voltaram a 3204/3205, e o
`guarda_save.py` ganhou `ids_de_treinador`, que compara o header de hoje com o do `e5224a3d67` (o da
ROM publicada) e reprova quem moveu, quem sumiu e quem entrou no meio, com a mutação real plantada no
`--demo`.

### O de-para por nome precisa olhar o SCRIPT

O de-para de sprite próprio casa pelo nome do objeto da fonte, e a fonte rotula como MARS o objeto de
CENA da comandante em `ValleyWindworksBuilding`: ela aparece, fala e some, e quem fica no mapa é o
pai da família, cujo script começa com "Papa:". O casamento com o objeto NOSSO era por vizinhança
pura, então a cara da Mars foi parar em quem fala como o pai, que é o mapa mentindo. `pode_vestir()`
virou o portão único dos DOIS pontos de `importa_npcs_sinnoh.py` que repintam objeto nosso: sprite
próprio só entra em objeto MUDO ou em objeto cujo script fala como a pessoa, seguindo os saltos de
rótulo, que é como a Candice de Snowpoint continua passando (o rótulo dela não diz o nome, o corpo
tem `TRAINER_SINNOH_LEADER_CANDICE`). A Mars saiu, o objeto voltou ao `OBJ_EVENT_GFX_SCIENTIST_1` que
já tinha, e ficam **20 colocações em 20 mapas, com 16 constantes**.

### Os casos adversariais desta rodada

`dev_scripts/testes_criticos/160_fechador_r10.json`, **8 casos, 8 verdes**, seis em PAR; o texto
inteiro de cada um está no JSON.

- **T160.1, T160.2 e T160.3, o id do Leon pelos dois lados.** O 3204 abre a batalha dele com o time
  da tabela; a flag `0x1184` (`0x500 + 3204`) plantada faz o `goto_if_set` disparar e a batalha não
  começa; e a `0x1186`, o id que ele TINHA fora do lugar e que hoje é da Wanda, **não** o segura. O
  terceiro mede o estrago: uma save de ontem acenderia a vitória da Wanda e mandaria brigar de novo
  com o Leon.
- **T160.4, a vitória gravada de verdade.** O Tammy de `Galar_RoseTower03` (id 3166) é DERROTADO e a
  flag `0x115E` acende com as duas VIZINHAS apagadas. O truque é o `10:HP=0=1` na janela medida entre
  a criação do time em `gParties` e a cópia dele para `gBattleMons`, seis passos de dez quadros:
  antes dela a escrita é desfeita, depois dela o HP volta a 21 no primeiro golpe.
- **T160.5 e T160.6, a Gardenia trava POR FALA.** O T158.7 já provava que ela é sólida, o que
  qualquer `graphics_id` daria; aqui o A roda a fala dela até o `trainerbattle_no_intro` e quem abre
  é `TRAINER_SINNOH_LEADER_GARDENIA`. O par sem o A não abre batalha nenhuma.
- **T160.7 e T160.8, o til lido na TELA.** O diário de `Galar_Route0803` é o único letreiro de Galar
  com til, e o tile dele é ANDÁVEL: o caso usa um toque de quatro quadros, que vira sem andar, porque
  a primeira versão usou dezesseis e atravessou o letreiro sem lê-lo. A medida de tela saiu do MESMO
  roteiro nas DUAS ROMs: os framebuffers finais diferem em **NOVE pixels**, todos no retângulo
  (116,124) a (121,125), o acento do único "a" com til da tela, dois pontos na velha e til na de
  hoje. **Nenhum outro pixel mudou.**

### O que fica aberto

- **13 bolas de neve** de Snowpoint, até o simulador de gelo ser calibrado contra o motor ao sul da
  linha 8 do ginásio; **Sinnoh em 93,3% de objetos**, que são 166 objetos de enredo do Platinum mais
  48 canteiros de berry cujo id mora na SAVE; e **Galar** com 70 estáticos dos 1.088, 25 placas, 514
  NPCs mudos por motivo e `fila_galar.json` em 1.198 de 3.195.
- **10 constantes `OBJ_EVENT_GFX_SINNOH_*` sem uso em mapa nenhum** (BUCK, BYRON, CHARON, CHERYL,
  CRASHER_WAKE, LOOKER, MARS, MAYLENE, PALMER, RILEY). Custam ROM e não aparecem; quem for usá-las
  passa pelo `pode_vestir()`.
- **`treinadores_galar.py --aplicar` APAGA a Fase F se rodado sozinho**, porque reescreve o
  `galar_treinadores.inc` inteiro e os chefes só voltam com `fase_f_chefes.py --aplicar` depois. Hoje
  é disciplina de quem roda, e não guarda: **vale um guarda**.
- **T143.9 continua instável** pelo motivo escrito na 0.q, o conserto da 0.p segue medido e refutado,
  a **pergunta 18** (sprites dos 26) segue sem resposta com a arte crua, e **gens 6, 7 e 9** seguem
  paradas por escopo, com o julgamento em `fontes-mapas/PLANO-GENS-6-9.md`.

---

## 0.q GALAR VOLTA A FALAR E OS ANTROS DE RAIDE VIRAM ENCONTRO, SINNOH ABRE OS TRÊS LAGOS E GANHA 26 SPRITES PRÓPRIOS, 23/08/2026 (rodada 9; condutor Opus, três executores Opus, fechador Opus)

Build verde, uma build só. **ROM 96,37% de 32 MB** (32.336.544 B, **1.217.888 B livres**, 1,16 MB;
era 96,06% e 1.320.436 B livres na 0.p, então a rodada gastou 102.548 B), **EWRAM 86,16% e IWRAM
86,68%, idênticos aos da 0.p e aos da 0.o**: nada desta rodada encostou em RAM. **Suíte 939 de 940**, ZERO reprovados,
com o T11.3 pulado na varredura porque ele só prova algo com duas ROMs, e os quatro blocos novos **T156 em 10/10, T157 em 8/8, T158 em 6/6 e T159 em
14/14**; **T11 3/3** contra a build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`).
**SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B, **2.054 layouts e 2.400 mapas**, os 2.400
declarados dentro da ROM, **nenhum grupo novo** (128 de 255, nenhum acima de 128 mapas);
`guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags e **0 novas nos dois perfis**,
0 stub nos dois; `valida_conectividade` com **0 warps quebrados**; `valida_warp_tile --piso 60` em
**5.915 de 6.875 (86,0%)**, nenhuma região abaixo do piso; `valida_mapas_sinnoh --so-sinnoh` com
`'sprite': 0` e 0 mapas com problema. ROM oficial `roms/pokemon-claude-2026-08-23.gba` (md5 6e3c177cbe61c5eabdd7759b3de3cfee),
com o `.map` ao lado, e o MESMO binário em `roms/pokemon-claude-teste-2026-08-16.gba`.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 100,8% | 100,1% | 100,4% | -- | 55 (0) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 100% | **93,3%** | 103,7% | 98,1% | -- | **39 (18)** | 267 |
| Unova | 100% | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | **103,6%** | 100% | **70,3%** | **59,2%** | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%**, intocada.

### Galar: seis specials nulos destravam 274 linhas, e as mesas de raide saem da recusa

O demake chama Quest Log e Help System do FireRed o tempo todo, 236 vezes em 178 linhas de script, e
enquanto o NOME não existisse aqui o tradutor recusava a CENA INTEIRA por um comando que não muda
nada observável. `src/field_specials.c` e `data/specials.inc` ganharam os seis com corpo NULO, e a
semântica nula é FIEL: `GetQuestLogState` devolve 0, que no FireRed quer dizer "não estou gravando
nem reproduzindo", e nesta ROM isso é sempre verdade. Resultado: **274 linhas destravadas e 168
frases novas**.

As **mesas de raide** eram, na 0.p, 200 linhas fora por "sorteio de N espécies no script".
`estaticos_galar.resolve_mesas` passou a escolher UM encontro por antro com regra determinística:
lendário pela regra 1, com **um lendário por antro e sem repetição**, e o resto por rotação no índice
do antro na fila, vetando espécie que já saiu em antro a até três mapas de distância. Medido na
árvore de hoje: **196 antros, 111 espécies distintas, 20 lendários em 20 antros, zero lendário
repetido em qualquer outro antro**. Em **três pares** de mapas vizinhos a espécie de raide ainda
repete (CrownTundra08/12, CrownTundra11/13, IsleOfArmor08/12), e isso é o SEGUNDO degrau da regra
funcionando como escrito: quando não há candidato que respeite vizinhança e lendário ao mesmo tempo,
a vizinhança cede, porque ela é a restrição mole.

Com o reposicionamento de 42 encontros a menos de três tiles, os estáticos vão de **795 para 1.018
dos 1.088** que a fonte oferece. Objetos 93,5 → **103,6%**, placas 65,8 → **70,3%**, script 55,6 →
**59,2%**, fila de 1.476 para **1.198**. Quatro defeitos de gerador consertados na raiz, e um deles ia
longe: o pool de flag escolhia por apelido e teria escrito por cima da Jasmine de Johto.

**A régua de Galar é HONESTA, e foi conferida aqui e não aceita de palavra.** O denominador de
`objetos` soma os 1.111 registros que o filtro G4 aprovou MAIS os **1.088 encontros estáticos que a
FONTE oferece** (`dev_scripts/galar_estaticos.json`); o numerador conta os `object_events` do
`map.json` de hoje, estáticos inclusive. O `da_fonte` NÃO se mexeu nesta rodada, só o `aceitos`
(795 → 1.018), e as recusas fecham a conta exata: 1.018 + 1 + 1 + 2 + 4 + 37 + 25 = 1.088. Os dois
lados contam os estáticos, e passar de 100% é o mesmo de Kanto (101,2%) e Unova (102,3%).

### Sinnoh: os três lagos abrem a pé, as bolas de neve são batente, e os objetos vão a 93,3%

Os três lagos drenados eram prisão: `LakeVerityLowWater`, `LakeAcuityLowWater` e `LakeValorDrained`
tinham a boca na elevação 3 e os ~800 tiles em volta na elevação 1, e `IsElevationMismatchAt`
recusava cada passo. A causa não era o mapa da fonte, era a REGRA de conversão, escrita para caverna
de pedra: `0x00` sem colisão virava rocha e `PUDDLE`/`SHALLOW_WATER` viravam água.
`dev_scripts/lagos_sinnoh.py` converte os três com a regra do lago, e `WATER_SEA` continua água de
propósito, porque no Platinum também é Surf que atravessa.

As **19 bolas de neve** do ginásio de Snowpoint entraram como OBJETO SÓLIDO, e não como bloco de
Strength, e isso foi MEDIDO e não escolhido: o chão do ginásio é `MB_ICE` inteiro, e em gelo o motor
entra em movimento forçado (`sForcedMovementFuncs`, `src/field_player_avatar.c:164`) ANTES de chegar
em `TryPushBoulder`, então o empurrão nunca acontece. **6 das 19 passaram** no portão, que exige que
todo NPC com script do ginásio continue alcançável pelo simulador de escorregão; as outras 13 ficam
ao sul da linha 8, onde o modelo ainda não bate com o motor.

Também entraram: os sub-baldes b1/b2/b3 do importador de NPC (b1 tem cena equivalente aqui e entra com
a NOSSA flag; b2 é sorteio diário da fonte e entra visível; b3 é flag MORTA na fonte), o corredor de
conversa reservado, as pedras com empurrão de até três tiles, a `RotomsRoom` com as sete formas como
cenário, e o `MOVE_STRENGTH` no `src/chapter_jump.c`. Objetos **87,0 → 93,3%**, **81 Pokémon no
overworld**, **19 NPCs com sprite próprio**. Três defeitos de idempotência consertados, que juntos
tinham deixado **284 cópias** de objeto no mapa.

### Sprites: 26 personagens de Sinnoh com desenho próprio, e nenhuma paleta nova

`dev_scripts/sprites_sinnoh.py` desenha 26 PNG de **144 por 32**, que são os nove quadros de 16 por 32
da tabela de animação padrão, lidos por `overworld_ascending_frames` (uma entrada só na pic table, com
`relativeFrames`). **Zero paleta nova**: os 26 reaproveitam `OBJ_EVENT_PAL_TAG_NPC_1` a `NPC_4`, porque
paleta de overworld é VRAM e estourar a janela de sprite de um mapa faz NPC sumir sem erro nenhum
aparecer. O preço é arte crua, e foi escolha. As constantes entram no FIM do enum de
`include/constants/event_objects.h`, única posição que não desloca id de sprite já gravado.

**Correção de número em relação ao que foi relatado:** as colocações são **21 objetos em 21 mapas,
com 17 constantes distintas**, e não 16; nove constantes (LOOKER, BUCK, MAYLENE, CRASHER_WAKE, CHARON,
BYRON, RILEY, PALMER, CHERYL) ainda não foram usadas em mapa nenhum.

### Os casos adversariais desta rodada

`dev_scripts/testes_criticos/159_fechador_r9.json`, **14 casos, 14 verdes**, sete deles em PAR, autor
de caso diferente do autor de cena em todos. O texto inteiro de cada um está no JSON; aqui vai o que
cada par mede.

- **T159.1 e T159.2, dois antros de raide VIZINHOS.** `Galar_WildArea05` dá `SPECIES_MIME_JR` (439) e
  `Galar_WildArea06`, vizinho direto no grafo de warps, dá `SPECIES_DARUMAKA_GALAR` (989), lidos de
  `gParties`. O par é a prova: um caso sozinho só diria que ALGUM bicho apareceu.
- **T159.3, T159.4 e T159.5, o Quest Log depois de SAVE E RECARGA.** O T159.3 salva dentro de
  `Galar_Hulbury06`; o T159.4 CONTINUA daquela save, fala com o mercador que chama
  `special GetQuestLogState` e fica TRAVADO pela caixa em (25,45); o T159.5, com um aperto a menos,
  anda até (20,45). Special que a tabela não registrasse derrubaria o script.
- **T159.6, o lago esvaziado atravessado de ponta a ponta E DE VOLTA.** 181 passos em 52 pernas dentro
  do leito do `LakeValorDrained`, parando no VIZINHO da boca, porque pisar nela provaria warp e não
  leito.
- **T159.7 e T159.8, a bola de neve contra o escorregão.** Do MESMO tile (12,3): para baixo o
  escorregão para em (12,7), quatro tiles, porque a bola de (12,8) segura; para a esquerda, na linha
  sem bola, ele corre ONZE tiles até (1,7).
- **T159.9 e T159.10, o sprite próprio lido no motor.** `graphics_id` que não resolve NÃO dá erro de
  build: dá objeto que não carrega, e objeto que não carrega deixa de ser sólido e de rodar script. A
  Mars trava o jogador em (9,4) com o A; sem o A ele desce até (9,7).
- **T159.11 e T159.12, o objeto b1 some depois da cena nossa.** Com `FLAG_GALACTICA_WINDWORKS` acesa o
  objeto de (3,7) some e o jogador anda até (3,6); com ela apagada ele não sai de (3,8).
- **T159.13 e T159.14, a cena do c3 acende a flag que o mapa REALMENTE lê.** É o caso do defeito
  achado no fechamento: o jogador joga a cena inteira, SAI E VOLTA pelo mesmo warp, e só então anda.
  Recarregar o mapa é o ponto, porque `removeobject` sozinho passaria num caso da mesma sessão.
- **O rodízio do Restaurante NÃO EXISTE, e a sonda é a resposta.** `data/maps/Restaurant/map.json` tem
  19 objetos, todos com `flag: "0"`, `Restaurant_MapScripts:: .byte 0`, e `GetDayOfWeek` não tem
  chamador nenhum no repo. A decisão está em `importa_npcs_sinnoh.py:250-278`: na fonte o critério é
  `GetRandom`, não dia da semana, e o balde b2 põe os NPCs visíveis de propósito. Não há caso a
  escrever.

### O que o fechador consertou

- **A cena nova do c3 acendia uma flag que NINGUÉM lê, e foi por pouco que ninguém viu.** O bloco c3
  (`cenas_galar.py`) alocava a PRÓPRIA flag de esconder por (mapa, flag da fonte),
  `FLAG_GALAR_ESCONDE_G09M11_230` na vaga 0x1C89, enquanto os objetos 1 e 2 do `Galar_Hammerlocke05`
  escondem por `FLAG_GALAR_ESCONDE_230`, vaga 0x1C81, que é a que o bloco c4b (`objetos_galar.py`)
  batizou para a MESMA flag da fonte e escreveu no `map.json`. A cena chamava `setflag` numa e
  `removeobject` nos objetos da outra: o sumiço valia só a sessão de mapa e os dois NPCs voltavam ao
  reentrar. O c3 passou a REUSAR o nome do c4b quando ele já existe no header, e o T159.13/T159.14 é a
  prova. Efeito colateral MEDIDO e querido: a flag do c4b é por FLAG DA FONTE e não por mapa, e a
  0x230 pendura seis objetos em três mapas de Hammerlocke, então a cena passa a sumir com os seis, que
  é o que a fonte faz.
- **`objetos_galar.py --demo` ficou VERMELHO nesta árvore, e a causa é a mesma família.** Ele planta
  duas flags na mesma vaga e cobra que o portão reprove; a vaga escolhida já tinha dono, o grupo
  acusado vinha com TRÊS nomes e a mutação reprovava por si mesma. Raiz: o filtro por PREFIXO. O c4b
  tirava da conta tudo que começasse com `FLAG_GALAR_ESCONDE_`, e o c3 usa o MESMO prefixo mais o nome
  do mapa. Não chegou a colidir por sorte de ordem, e teria colidido na próxima flag pedida. O
  reconhecimento passou a ser por FORMATO EXATO do nome, numa função só (`flags_com_dono`).
- **T141.5 e T141.6 ficaram VERMELHOS, e a culpa não era do jogo.** A partir desta rodada o
  `Galar_Hammerlocke05` tem cena de `ON_FRAME` própria, longa, que dispara ao entrar e come os apertos
  do roteiro em caixa de texto. Com `VAR_GALAR_G09M11_CENA` valendo 1 o mapa se comporta tile a tile
  como na ROM da 0.p, medido nos dois binários, então não há travamento: há cena nova. Os dois casos
  ganharam a var e voltaram a medir o que foram escritos para medir. **Custou meia hora acreditar que
  era trava**, e o que desfez a suspeita foi rodar a MESMA sonda contra a ROM `2026-08-22f`.
- **Semântica de aperto, medida e não suposta:** pressão de 16 quadros contígua anda um tile, mas a
  PRIMEIRA pressão do roteiro é engolida, e um `NADA` no meio faz a pressão seguinte virar só a
  virada. Quatro rotas do T159 nasceram erradas por isso, e foram medidas até baterem tile a tile.

### O que fica aberto

- **A cena longa nova de `Galar_Hammerlocke05`** tem três caixas com muitas páginas e roda ao ENTRAR
  no mapa. Ela é fiel à fonte, mas é a primeira cena de Galar que um jogador encontra sem pedir, e o
  Gui pode querer olhar o texto dela (ver o item do "ä" abaixo).
- **T143.9 continua INSTÁVEL, e o conserto que a 0.p propunha foi MEDIDO e REFUTADO.** Ele passou
  verde nas duas varreduras completas desta rodada, e rodado sozinho deu 2 de 3 numa vez e 1 de 3 na
  outra, na mesma ROM. A 0.p dizia que o conserto era dar um Pokémon ao jogador pelo `antes_do_warp`,
  como o T144.5 faz; isso foi feito e medido, e o caso passou a 1 de 3, ou seja PIOROU. Duas medidas
  do mesmo remédio com o resultado errado querem dizer que o diagnóstico está errado, então o
  `antes_do_warp` foi desfeito e o caso ficou como estava, com a medida nova escrita no próprio texto
  dele. Quem for mexer: meça POR QUE a batalha se fecha, em vez de supor que é falta de time.
- **13 bolas de neve** de Snowpoint até o simulador de gelo ser calibrado contra o motor ao sul da
  linha 8 do ginásio.
- **Sinnoh, objetos em 93,3%**: 166 objetos de enredo do Platinum e 48 canteiros de berry cujo id mora
  na SAVE.
- **Galar, 70 estáticos** dos 1.088 (mesa sem espécie com nome aqui e geometria recusada), **25
  placas**, **514 NPCs mudos** por motivo, `fila_galar.json` com 1.198 de 3.195.
- **Texto de Galar sem "ã".** Os arquivos de fala trazem **191 ocorrências de "ä" e ZERO de "ã"**
  ("Näo", "irmä"). Não é regressão desta rodada, veio com a onda de 20/08, e o gerador tem ida e volta
  byte a byte pelo charmap, então os BYTES estão certos: o que falta é o glifo. Conserto é obra de
  fonte, não de script.
- **`opponents.h` deslocou dois ids** (`TRAINER_GALAR_LEON_736` e `_739` foram de 3204/3205 para
  3206/3207) e `vars.h` remanejou seis apelidos de var de Galar. O `guarda_save.py` diz SAVE
  COMPATIVEL e está certo, porque ele mede TAMANHO (`FLAGS_COUNT`, `MAX_TRAINERS_COUNT`) e não
  atribuição; mas a flag de "já derrotei" de um treinador é indexada pelo id, então esses dois trocaram
  de vaga. Não morde hoje, porque Galar não tem treinador jogável, e é a última hora em que isso é de
  graça.
- **A Mars de `ValleyWindworksBuilding` fala como o pai da família.** O objeto 0 trocou de
  `OBJ_EVENT_GFX_SCIENTIST_1` para `OBJ_EVENT_GFX_SINNOH_MARS`, e o script dele
  (`ValleyWindworksBuilding_EventScript_Npc1`) é a fala portada que começa com "Papa:". Ou o sprite
  está errado, ou o script; não foi mexido de propósito, porque os sprites estão na pergunta 18, sem
  resposta do Gui.
- **Pergunta 18 (sprites dos 26 personagens) segue sem resposta.**
- **Gens 6, 7 e 9** seguem paradas por escopo, com o julgamento em `fontes-mapas/PLANO-GENS-6-9.md`.

---

## 0.p O B10 DERRUBA A ROM DE 99,28% PARA 96,06%, E O DISTORTION WORLD FICA SIMÉTRICO, 22/08/2026 (rodada 8; condutor Opus, dois executores Opus, fechador Opus)

Build verde, um build só. **ROM 96,06% de 32 MB** (32.233.996 B, **1.320.436 B livres**, 1,26 MB;
era 99,28% e 241.172 B livres na 0.o), **EWRAM 86,16% e IWRAM 86,68%, idênticos aos da 0.o**: o B10
é obra de ROM e não encostou em RAM. **Suíte 900 de 902**, com o T11.3 pulado e UM vermelho de
tempo no T143.9 (ver "o que fica aberto"), e o bloco novo **T155 em 6/6**; **T11 3/3** contra a
build `cf6786b2ae` (worktree em
`/private/tmp/claude-501/t11-antiga`). **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B,
**2.054 layouts sem nenhum movido** e **2.400 mapas**, os 2.400 declarados dentro da ROM;
`guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags e **0 novas nos dois
perfis**; `valida_conectividade` com **0 warps quebrados**; `valida_warp_tile --piso 60` em
**5.915 de 6.875 (86,0%)**, nenhuma região abaixo do piso; `valida_mapas_sinnoh` com 0 mapas com
problema; os três `--demo` tocados verdes, um deles depois de conserto. ROM oficial
`roms/pokemon-claude-2026-08-22f.gba` (md5 `fb239ede296088906761daece2e7d6d5`), com o `.map` ao
lado, e o MESMO binário em `roms/pokemon-claude-teste-2026-08-16.gba`.

**A régua de completude não se mexeu**, e isso é o critério de aceitação do B10, não um detalhe:

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 100,8% | 100,1% | 100,4% | -- | 55 (0) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 100% | 87,0% | 103,7% | 98,1% | -- | 39 (18) | 267 |
| Unova | 100% | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | 93,5% | 100% | 65,8% | 55,6% | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%**, intocada.

### O B10, fatia por fatia

| fatia | onde | B de volta |
|---|---|---|
| tabelas de fala de treinador, VAZIAS desde sempre | `src/trainer_slide.c` | **498.400** (448.056 + 50.400 viraram 56) |
| dificuldade colapsada: EASY e HARD de `gTrainers` | `include/constants/difficulty.h` | **277.160** |
| blockdata repetido virando referência, 2.373 de 4.108 blobs | `dev_scripts/dedupe_blockdata.py`, chamado pelo `map_data_rules.mk` | **264.080** |
| 20 famílias novas de asset, criadas pela entrada de Galar | `dev_scripts/dedupe_assets.json` | **38.700** |

Somadas dão 1.078.340 B previstos contra **1.079.264 B medidos no link**; a diferença é alinhamento
de seção, e vale o medido. `B_VAR_DIFFICULTY == 0` faz `GetCurrentDifficultyLevel()` devolver
`DIFFICULTY_NORMAL` sempre, então EASY e HARD eram zeros inalcançáveis e `[DIFFICULTY_NORMAL]` virou
`[0]` sozinho (dar um var a `B_VAR_DIFFICULTY` devolve as três na hora, e `TESTING` segue com as
três); as duas tabelas de fala nunca tiveram uma fala cadastrada; e o dedupe de layout só troca o
`.incbin` do repetido pelo símbolo do primeiro de conteúdo igual, sem tocar em `map.bin`, em
`layouts.json` nem no motor.

**Descartado, com número e não no olho:** a **indireção de tabela de treinador** renderia ~52 KB
líquidos, caro demais para o tamanho, e os **ícones já estão em `.smol` desde a Fase D**.

### Distortion World, a corrente ficou simétrica

O `cria_mapas_sinnoh.py` ganhou `simetriza`, e ele mora ali, e não numa ferramenta à parte, porque
o `--aplicar` não recria mapa que já existe: sem esse passo o defeito ficaria congelado para sempre.
Ele corrigiu **9 `dest_warp_id` em 8 `map.json`**, e o `pares` é simétrico POR CONSTRUÇÃO (o mesmo
`zip` produz A→B e B→A), o que o `--demo` cobra com mutação plantada. **Uma assimetria FICA, e é
honesta**: o warp 0 do `DistortionWorld1F` leva ao `MtCoronet6F`, que não tem escada de volta, então
essa porta é de mão única; está no T153.14, e é falta de degrau, não fiação errada.

### Os casos adversariais desta rodada

`dev_scripts/testes_criticos/155_fechador_r8.json`, **6 casos, 6 verdes**, autor de caso diferente
do autor de cena em todos.

- **T155.1, dificuldade no CHEFE.** O time de `TRAINER_SINNOH_LEADER_CANDICE` lido de `gParties`:
  seis espécies diferentes, seis níveis em escada (178 a 182) e o item do ace (`ITEM_ABOMASITE`). O
  "antes" foi RODADO, não argumentado: o mesmo caso passou verde contra a ROM da rodada anterior
  (`pokemon-claude-2026-08-22e.gba`), com os mesmos doze campos.
- **T155.2 e T155.3, blockdata aliasado com PLACA.** O `CanalaveLibrary2F` (layout aliasado) é
  cruzado de ponta a ponta e uma placa é lida; a prova é a posição, porque a caixa aberta ENGOLE a
  perna seguinte. O par negativo tira só o A e termina em (0,7) em vez de (13,7).
- **T155.4, Galar com o tileset inteiro aliasado.** No `gTileset_Galar19` metatiles, ATRIBUTOS e
  paletas viraram alias; o único mapa que o usa entra, SAI para o vizinho e VOLTA, para medir a
  segunda carga e não só a primeira.
- **T155.5, trainer slide no pior id.** `TRAINER_GALAR_LEON_739` é o id **3205**, o maior de
  `opponents.h` e o que ocupava a última linha da tabela que saiu; a batalha abre e entrega as seis
  espécies. Medido no caminho: batalha de Frontier **não** é desviada por `IsSpecialTrainer`
  (`include/data.h:275`), ela chega em `GetTrainerSlideArray`.
- **T155.6, o Distortion World inteiro.** Nove andares a pé numa sequência só, 27 pernas e ~345
  tiles, terminando no Spear Pillar em (14,12). É o único jeito de medir simetria: par torto põe o
  jogador no tile errado e a rota do andar seguinte quebra na hora.

### O que o fechador consertou

- **`dedupe_blockdata.py --demo` era verde VAZIO.** Ele lia o `layouts.inc` do DISCO, que já passou
  pelo próprio passo dentro do `make`, e imprimia "0 repetidos, 0 B de volta" com exit 0. Passou a
  rodar o `mapjson` num diretório temporário e medir A LINHA DE BASE: **4.108 blobs, 2.373 repetidos,
  264.080 B**, com `assert` que reprova se o número der zero. É a mesma armadilha dos dois `--demo`
  consertados na 0.o: autoteste tem de saber que o gerador já rodou.
- **`valida_warp_tile.py` ia CEGO em tileset aliasado.** A varredura de pastas só enxergava
  `INCBIN`, e o `dedupe_assets.py` troca o `INCBIN` do repetido por `ASSET_ALIAS`:
  `Galar_Motostoke03` e `GoldenrodCity_BikeShop` caíam em "sem pasta" e saíam da conta sem virar
  vermelho. Ele passou a seguir o alias até o canônico, e o total subiu de **6.873 para 6.875
  conferidos, com 5.915 vivos**; os dois escondidos são VIVOS. O defeito é anterior a esta rodada (o
  BikeShop já estava cego) e cresce a cada família nova de alias.
- **A primeira versão do T155.2 era prova vazia**: as duas histórias, com placa e sem placa,
  terminavam no MESMO tile. Foi redesenhada até o par discriminar, e só então o negativo entrou.

### O que fica aberto

- **Próximas fatias de ROM, não executadas:** **blockdata cru ~1,5 a 2 MB**, o maior prêmio que
  sobra, mas é obra de MOTOR (comprimir `map.bin` e descomprimir na carga do mapa) e não de script;
  **metatiles crus ~600 KB**, mesma natureza; **glifos japoneses 130 KB**, barato e sem risco, e é
  por onde começar se a próxima rodada precisar de pouco. Com 1,26 MB livres, nada é urgente.
- **Lagos `LakeVerityLowWater` e `LakeAcuityLowWater`** seguem na fila: a trava é de ELEVAÇÃO (boca
  em 3, os 799 tiles em volta em 1), e o conserto honesto é converter o leito drenado do Platinum.
- **Sinnoh, objetos em 87,0%**, e nenhum balde é ferramenta parada: 128 nomes próprios sem sprite,
  ~100 com `hidden_flag` que esta ROM não tem, 115 bolas e 59 obstáculos recusados por tile fora de
  alcance, 90 canteiros de berry (id mora na SAVE) e 63 VENT e BOLLARD.
- **Galar, objetos em 93,5% e `script` em 55,6%**, com os 200 encontros de raide fora por decisão e
  89 recusados por geometria. `fila_b6.json` com 157 pendentes, `fila_galar.json` com 1.476 de 3.195.
- **Gens 6, 7 e 9** seguem paradas por escopo, com o julgamento em `fontes-mapas/PLANO-GENS-6-9.md`.
- **T143.9 é INSTÁVEL, e isso não é regressão desta rodada.** Ele reprovou na varredura de fechamento
  e passou **3 de 3 rodado sozinho**, na MESMA ROM (md5 `fb239ede296088906761daece2e7d6d5`), e tinha
  passado na varredura anterior do mesmo binário. A causa está escrita no próprio caso: a janela de
  apertos dele é de UM aperto (com 10 A o diálogo ainda rola, com 12 A o jogador já perdeu), e o
  jogador de teste entra sem time, então o instante em que a batalha fica aberta depende de RNG.
  Quem for mexer: o conserto não é aumentar a cauda, é dar um Pokémon ao jogador pelo
  `antes_do_warp`, como o T144.5 faz, para a batalha parar de se resolver sozinha.

---

## 0.o AS SEIS REGIÕES FECHAM O QUE DAVA PARA FECHAR, E A ROM ENCOSTA NO TETO, 22/08/2026 (rodada 7; condutor Opus, sete executores Opus, fechador Opus)

Build verde. **ROM 99,28% de 32 MB** (33.313.260 B, **241.172 B livres**, 235,5 KB; era 98,50% na
0.n), EWRAM 86,16% e IWRAM 86,68%. **Suíte 886 de 887**: a varredura normal deu 865/866 com só o
T11.3 pulado, e o bloco novo T153 deu **21/21**. **T11 3 de 3** contra a build `cf6786b2ae`
(worktree em `/private/tmp/claude-501/t11-antiga`), que é o primeiro 3/3 desde que o T11.1 foi
calibrado. **SAVE COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B, **2.054 layouts numerados sem
nenhum movido** e **2.400 mapas** (eram 2.377); `valida_rom.py` com os 2.400 declarados dentro da
ROM; `guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags e **0 novas nos dois
perfis**; `valida_conectividade` com **0 warps quebrados** e nenhum mapa de Sinnoh ou Johto
inalcançável; `valida_warp_tile --piso 60` em 5.914 de 6.874 (86,0%, era 85,9%), nenhuma região
abaixo do piso; `valida_mapas_sinnoh --so-sinnoh` com **0 mapas com problema**. Os **26 `--demo`
de gerador tocados** rodaram verdes, dois deles depois de conserto (abaixo). ROM oficial
`roms/pokemon-claude-2026-08-22e.gba` (md5 `bba1d16835302015348c7bc374b66127`), com o `.map` ao
lado, e o MESMO binário na ROM de teste de nome fixo.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | **100%** | **100,8%** | **100,1%** | **100,4%** | -- | **55 (0)** | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | **100%** | **87,0%** | 103,7% | **98,1%** | -- | **39 (18)** | 267 |
| Unova | **100%** | 102,3% | 100% | 100,2% | -- | 30,5 (1) | 315 |
| Galar | 100% | 93,5% | 100% | **65,8%** | **55,6%** | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

### As decisões, e quem as tomou

Do **Gui**: "completa até ficar 100 em tudo", "agentes para melhorar as artes pobres das 5
primeiras regiões", **Galar travada em nível 255** e **seis regiões**, teto de pé.

Do **condutor**: **Galar fecha `objetos` em 93,5%** e os registros de "gráfico é cenário" ficam
sendo cenário, sem virar objeto; **a GS Ball sai** (não existe item nem cena que a use); o **trem
magnético de Saffron é corte declarado** (`SaffronMagnetTrainStation` entrou em `CORTES_DO_GUI`);
o **PWT é autorizado**; e os **nove andares novos do Distortion World FICAM**, com forma honesta e
arte chapada, com a decoração adiada para outra rodada.

### As sete frentes, com número

1. **Harness (T11).** O T11.1 contava o menu de START **de cima** e caía na tela de CARTÃO na ROM
   velha, porque `BuildNormalStartMenu` (`src/start_menu.c:332`) monta o TOPO conforme o estado do
   jogo e só o RABO é fixo: PLAYER, SAVE, OPTION, EXIT. Passou a contar **de baixo**, três UP a
   partir da linha 0, que `Menu_MoveCursor` (`src/menu.c:704`) faz dar a volta; junto veio
   `prova.sav_gravada`, que abre o `.sav` e cobra um slot inteiro escrito. T11 **3/3**.
2. **Galar, treinadores e placas.** `treinadores_galar.py`, `galar_fase_f.py` e `placas_galar.py`:
   **266 batalhas em 148 mapas** a nível 255, **38 chefes** com 17 lendários, 31 Mega e 7 Z, zero
   Dynamax e zero Tera; **206 times novos** em `trainers.party` (ids 3000 a 3205); placas de 44,1%
   para **65,8%** e `script` de 35,6% para **55,6%**; a fila de Galar caiu de 1.775 para **1.476
   de 3.195**. T147 **12/12**. Conserto de motor: **`trainerbattle_no_intro` NÃO consulta a flag de
   vitória**, então o gerador emite `goto_if_set TRAINER_FLAGS_START + id` antes dela, senão o
   treinador rebrigaria para sempre.
3. **Sinnoh, os 100% de mapa.** `converte_interiores_sinnoh.py`, `cria_mapas_sinnoh.py`,
   `corredores_sinnoh.py`, `bolas_sinnoh.py`, `pedras_sinnoh.py` e `importa_npcs_sinnoh.py`:
   **23 mapas novos** (90 KB), entre eles os 9 andares do Distortion World; mapas de 95,4% para
   **100%**; RavagedPath saiu de 133 tiles ilhados para **0**; objetos de 76,3% para **87,0%**;
   placas de 86,8% para **98,1%**; **166 bolas**, **51 obstáculos** e 30 clones removidos.
   T148 **9/9**.
4. **Johto e Unova, os 100%.** `completa_objetos_johto.py`, `completa_placas_johto.py`,
   `bolas_faltantes_johto.py`, `arco_farol_johto.py`, `cenas_pwt_unova.py` e
   `completa_placas_unova.py`, mais o **quebra-cabeça deslizante** como motor novo
   (`src/sliding_puzzle.c` e 13.476 B de arte comprimida), usado pelas quatro placas do
   `RuinsOfAlph_PuzzleAndRewardChambers`. Johto **100 / 100,8 / 100,1 / 100,4** e Unova
   **100 / 102,3 / 100 / 100,2**, com **2 vars novas** do PWT. T149 **14/14**.
5, 6 e 7. **Arte.** `arte_cavernas_sinnoh.py` em **70 mapas** (mediana de 8 para 21 metatiles
   distintos, T150 **6/6**), `arte_exteriores_sinnoh.py` em **11 salas** do ginásio D/P de
   Hearthome e na casa da Iron Island (de 12 para 27, T151 **6/6**) e `arte_mapas_pobres.py` em
   **4 mapas** de Johto e Unova (T152 **4/4**). Os **21 pobres de Hoenn são vanilla e ficam**, e o
   elevador de Virbank foi descartado no olho.

Nas três frentes de arte a regra é a mesma e está provada célula a célula no `--demo`: o gerador
escreve só os **10 bits de baixo** de cada célula do `map.bin`, então colisão, elevação e
comportamento saem byte a byte idênticos ao `git show HEAD:`.

### O que o fechador consertou

- **Os 12 casos que apertam SAVE** pelo menu do START passaram a contar **de baixo** (três UP) e
  ganharam `prova.sav_gravada`: T11.1, T120.9, T123.21, T127.3, T127.9, T136.1, T136.5, T139.3,
  T144.1, T145.3, T145.7 e T146.3. Dois apertavam três DOWN e dez apertavam dois, e a diferença era
  administrada à mão conforme o jogador tivesse ou não Pokémon.
- **Dois `--demo` vermelhos, os dois da mesma família: autoteste que não sabe que o gerador já
  rodou.** O `arte_exteriores_sinnoh.py` comparava a arte de DEPOIS com o DISCO (que já estava
  decorado) em vez do HEAD do git, e reprovava um gerador idempotente e correto; passou a usar
  `base`, como o `arte_mapas_pobres.py` já fazia. O `placas_galar.py` montava o plano só com o que
  ainda está `pendente`, e depois do `--aplicar` o plano fica VAZIO: ganhou `plano(incluir_feitas)`
  para o autoteste e um portão que soma o que já está no mapa.
- **Os lagos `LakeVerityLowWater` e `LakeAcuityLowWater` foram para a fila, com motivo**, e não
  consertados. Medido: o jogador chega pela boca e alcança **um tile, ele mesmo**, e a causa é
  ELEVAÇÃO, não colisão (a boca é elevação 3 e os 799 tiles em volta são elevação 1, água;
  `IsElevationMismatchAt`, `src/event_object_movement.c:10014`, barra 3 contra 1). Não é trava
  dura: a seta do warp devolve o jogador, e quem tem Surf entra na água. Corredor não resolve,
  porque as ilhas de chão de verdade são o metatile 0x201, preto puro de enchimento de caverna, e
  a passagem levaria ao vazio: o conserto honesto é **converter o leito do lago**, drenado no
  Platinum, e isso é obra de conversão.

### Os casos adversariais desta rodada

`dev_scripts/testes_criticos/153_fechador_r7.json`, **21 casos, 21 verdes**, autor de caso
diferente do autor de cena em todos.

- **T153.1 a T153.4, Galar.** O treinador comum vencido não rebriga depois de **sair do mapa e
  voltar** (`WARP=` no roteiro) nem depois de **salvar e recarregar**, e o par negativo prova que
  sem a flag a batalha começa (`TRAINER_GALAR_RUAN_POKE_372`, flag 0x500+3137 = 0x1141).
- **T153.5 a T153.10, arte.** Um mapa decorado de cada gerador, com rota longa e leitura de NPC:
  MtCoronet2F (o Looker fala e solta o jogador), Mahogany B2F (o Lance cura e solta) e a segunda
  sala de elevador de Hearthome, onde não existe NPC com script nos 11 mapas daquele gerador e o
  que se prova é o corpo no mesmo tile do HEAD.
- **T153.11 a T153.15, Sinnoh.** O corredor novo do RavagedPath é atravessado em **16 pernas e 69
  tiles**, dos quais **nove eram parede no HEAD**, até uma item ball nova, pega **uma vez**; e os
  **três warps** do andar novo `DistortionWorld1F` disparam, um caso cada.
- **T153.16 a T153.18, Johto.** O quebra-cabeça deslizante **abre e toma o controle** (seis DOWN
  são engolidos), **fecha com B e devolve o jogador** (a perna seguinte anda quatro tiles), e o par
  negativo prova que sem abrir nada os mesmos apertos andam.
- **T153.19 a T153.21, Unova.** A cena do PWT dispara **uma vez**, com **save no meio**, e o
  recepcionista volta ao posto de (7,3) no fim da coreografia.

### Lições desta rodada

- **Aperto de direção que o jogador NÃO está encarando só VIRA, não anda.** Passo solto pede dois
  apertos quando muda de direção. Quatro casos do T153 reprovaram exatamente por isso.
- **Porta empurra um tile ao sul na chegada.** Quem entra por `MB_NON_ANIMATED_DOOR` não nasce na
  coordenada do warp. O primeiro T153.7 andava de (3,14), pisava de novo no próprio warp no meio da
  perna e caía no B1F.
- **O menu de START se conta de baixo**, porque o topo depende do que o jogo já liberou, e
  **`trainerbattle_no_intro` não consulta a flag de vitória**: quem desvia é o `goto_if_set`.
- **Stride do CFRU é 8/16 B** nos times da fonte de Galar, e **`planta_provisoria` está morta
  desde os túmulos**: nenhum mapa de Sinnoh veste mais o molde.
- **Autoteste tem de saber que o gerador já rodou.** Linha de base é o `git show HEAD:`, nunca o
  disco.

### O que impede 100% onde não chegou

- **Sinnoh, objetos em 87,0%**, e nenhum dos baldes é trabalho de ferramenta parado: **128** são
  nome próprio sem sprite aqui (Cynthia, Cyrus, os oito líderes, os lendários), **~100** têm
  `hidden_flag` do Platinum que esta ROM não tem, **115 bolas e 59 obstáculos** foram recusados por
  tile fora de alcance, **90** são canteiros de berry (id de árvore de berry MORA NA SAVE, então é
  obra de janela), e **63** são VENT e BOLLARD, cenário sem mecânica nativa.
- **Galar, objetos em 93,5% e `script` em 55,6%.** Faltam os 200 encontros de raide (o script da
  fonte sorteia até 59 espécies, e escolher uma seria inventar) e 89 recusados por geometria; a
  coluna `script` conta só NPC, e o que falta lá é fala, não colocação. Galar segue com **Dex 0**
  na régua, porque estático não conta como entrada de Dex de região.
- **Fila:** `fila_b6.json` com **157 pendentes** (150 de Sinnoh, 6 de Unova, 1 de Johto) e
  `fila_galar.json` com **1.476 de 3.195**.
- **Assimetria medida e CONSERTADA na 0.p** (quando esta seção foi escrita ela ainda estava de pé,
  e a frase original dizia "não consertada"): os **17 warps dos 9 andares novos do Distortion World**
  subiam sempre para o índice 0 do andar de cima, que é o warp de subida DELE e não o par
  correspondente; ninguém ficava preso, mas o jogador reaparecia no tile errado. O `simetriza` do
  `cria_mapas_sinnoh.py` corrigiu **9 `dest_warp_id` em 8 `map.json`** em 22/08/2026, e o T155.6
  desce a corrente inteira de uma vez.
- **O ramo de SUCESSO do quebra-cabeça deslizante não virou caso de suíte**: `CheckForSolution`
  (`src/sliding_puzzle.c:972`) exige as 24 casas na ordem e em `ORIENTATION_0`, o que não sai de
  martelada de botão; é pendência de FERRAMENTA, como a vitória do estático único da 0.n.

### O teto de ROM, e o que ele custa a partir de agora

**A ROM está em 99,28% de 32 MB, com 241.172 B livres**, e esta rodada gastou 261.332 B: nesse
ritmo resta menos de uma rodada. **A próxima obra grande exige o B10** (compressão de ícones mais
indireção de tabela de treinador, ~1,1 MB estimados) **ou um corte novo declarado pelo Gui**; a
economia mais óbvia continua sendo tirar da ROM os mapas que o `PLANO-ESCOPO.md` já cortou e que
hoje ainda compilam.

**Para o Gui olhar**: as três folhas de contato da arte nova estão em
`scratchpad/arte/sinnoh-cavernas/CONTATO.png`, `scratchpad/arte/sinnoh-exteriores/CONTATO.png` e
`scratchpad/arte/johto-unova-hoenn/CONTATO.png`, e são a única coisa desta rodada que depende de
gosto e não de medida.

---

## 0.n GALAR GANHA OS 795 POKÉMON DO OVERWORLD, E A RÉGUA VOLTA A FECHAR, 22/08/2026 (rodada 6; condutor Opus, um executor Opus, fechador Opus)

Build verde. **ROM 98,50% de 32 MB** (33.051.928 B, 490,7 KB livres; era 98,43% na 0.m), EWRAM
86,16% e IWRAM 86,66% (iguais às de ontem), **suíte 814/815** (só o T11.3 pulado na rodada
normal), **T146 10/10** e o **T11 em 2 de 3** contra a build `cf6786b2ae`
(`/private/tmp/claude-501/t11-antiga`), com esse vermelho explicado no fim desta seção. **SAVE
COMPATIVEL**, SaveBlock1 em 14.964 de 15.872 B e 2.032 layouts sem nenhum movido;
`valida_rom.py` com os 2.378 mapas declarados dentro da ROM; `guarda_colisao_vars.py` com 23
colisões herdadas e **0 novas nos dois perfis**; `valida_conectividade` com **0 warps
quebrados**; `valida_warp_tile --piso 60` em 5.869 de 6.829 (85,9%, igual à 0.m); `--demo`
tocados verdes. ROM oficial `roms/pokemon-claude-2026-08-22d.gba` (md5
`17e5f891bfb0862e8443644ff73a3e74`), com o `.map` ao lado, e o MESMO binário na ROM de teste de
nome fixo.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 96,1% | 100,1% | 96,2% | -- | 55 (3) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 95,4% | 76,3% | 100,9% | 86,8% | -- | 39 (76) | 267 |
| Unova | 99,0% | 102,3% | 99,6% | 100,2% | -- | 30 (2) | 315 |
| Galar | 100% | **93,5%** | 100% | 44,1% | 35,6% | 48 (32) | 0 |

### O bloco c5: 795 Pokémon parados no mapa, como em Sword/Shield

Decisão do Gui: **o teto de seis regiões fica de pé, Galar fica, e o conteúdo próprio dela
entra.** Caiu com ela o descarte de 18/08 ("gráfico de Pokémon mentiria a espécie"), verdade
naquele dia e não mais: `OBJ_EVENT_GFX_SPECIES` existe nesta build e o `distribui_dex.py` já
punha 106 estáticos com ela. `dev_scripts/estaticos_galar.py`: **795 encontros em 68 mapas**
(791 comuns e 4 únicos), 79 espécies, 145 cenas no `.inc` e **4 flags** (0x1D0A a 0x1D0D,
apelidos de `FLAG_UNUSED`, save intocada); a fila de Galar caiu de 2.570 para **1.775 de
3.195**. A espécie sai da `gSpeciesNames` da PRÓPRIA ROM da fonte, achada por âncora, **por NOME
e nunca por id** (o 331 do demake é `Sharpedo`); nome repetido é forma e só entra com decisão
escrita uma a uma.

**Comum e único são medidos, não arbitrados.** Único é aquele cujo script da fonte acende a
própria flag de esconder: gasta flag e a acende só em vitória ou captura. Comum não gasta flag
NENHUMA, e é isso que o faz renascer quando o mapa recarrega. **De fora ficaram 293 linhas com
motivo contado**: 200 de raide (o script sorteia até 59 espécies, e escolher uma seria
inventar), 89 de geometria, 3 de forma e 1 de id fora da tabela da fonte; nenhuma caiu por teto
nem por janela.

**O 859 do plano era 1.092.** Remedido sobre a MESMA fonte: 1.092 linhas de `script_objeto`
carregam `setwildbattle`, e 1.088 são de objeto que o G4 não pôs no mapa. Nenhuma definição
testada devolve 859: cita-se 1.092, e a régua divide por 1.088, que é o recorte de objeto.

### Os dois defeitos de motor, que viram lição

1. **`VAR_LAST_TALKED` não guarda id entre a batalha e o fim do script**, porque
   `ProcessPlayerFieldInput` regrava essa var a cada quadro em que o jogador tem controle:
   `removeobject VAR_LAST_TALKED` depois de `dowildbattle` é aposta na ordem dos quadros. O
   gerador guarda o id em `VAR_TEMP_1` ANTES da batalha, e o **T146.7** martela LEFT na saída da
   batalha: passou **5 de 5 execuções seguidas**.
2. **Remover o objeto ANTES da batalha congela o jogador**: a ordem é a da fonte. E
   **`FLAG_SYS_CTRL_OBJ_DELETE` não é lida por ninguém neste fork**: fica no script do único
   porque é o idioma do vanilla, não porque faça efeito.

### A régua contava o mesmo objeto duas vezes, e o `--demo` dela dizia

Vermelho real da rodada. A primeira versão somava os **795 que NÓS gravamos** nos dois lados da
coluna `objetos` E mantinha esses mesmos 795 dentro de `obj_impossiveis`: as partes deixavam de
somar o todo (1.906 + 3.051 = 4.957 contra 4.162 da fonte) e o `completude.py --demo`
**reprovava**. Pior que a soma: denominador feito da própria resposta lê 100% para sempre, e os
293 que a fonte tem e nós não pusemos sumiam; o `--detalhe` ainda imprimia "sobram 1.111
colocáveis" com o divisor já em 1.906.

Conserto: o denominador sai do **lado da fonte**, por um censo que o próprio gerador escreve
(`dev_scripts/galar_estaticos.json`, `da_fonte: 1088`), e os 1.088 saem dos impossíveis e entram
nos colocáveis. Galar `objetos` vai a **93,5%** (2.055 de 2.199) no lugar dos 107,8% de antes, e
1.963 + 2.199 = 4.162 fecha. A coluna `script` conta **só NPC** (448 de 1.260, 35,6%): estático
já nasce com script, e misturá-lo levaria a coluna a 60,5% sem uma linha de fala nova.

### Os casos adversariais do fechador (autor de caso ≠ autor de cena)

`dev_scripts/testes_criticos/146_fechador_r6.json`, 10 casos, 10 verdes.

- **T146.1 e T146.2, o comum renasce sem passar pelo save.** Numa execução só: batalha, fuga, o
  Skwovet some, o jogador SAI para o `Galar_WildArea05` e VOLTA, e o corredor volta a barrar em
  (19,17); o par sem a ida e volta anda os 41 tiles até (7,17) e é quem isola a carga de mapa.
  Pediu ferramenta nova: `WARP=MAP_X[:id]` no roteiro (`expande_warps` em `testa_critico.py`),
  com o mapa resolvido pela tabela.
- **T146.3 e T146.4, o único que NÃO se apaga.** O T145.7 acende a flag na mão e passa nos dois
  mundos; aqui a batalha termina em FUGA, e a flag tem de seguir apagada e o Slowpoke sólido,
  inclusive depois do save.
- **T146.5, T146.8, T146.9 e T146.10: os cinco warps do mapa mais cheio.** O
  `Galar_CrownTundra08` tem 43 objetos de 64 (15 herdados, 28 do c5); somados ao T145.9, os
  cinco ficam provados com o mapa cheio. **T146.6**: no mesmo mapa o NPC de cena de (22,54)
  continua acordando, prova de que o herdado não perdeu a vez na janela de sprite, com os
  encontros no FIM da lista de templates.
- **A prova de que o recusado NÃO está no mapa é de SCRIPT**, porque tile não andável, ocupado e
  inalcançável são onde o jogador não chega, e andar por cima não separa "o objeto não existe"
  de "não consigo chegar lá". Virou o portão 9 do `--demo` do gerador: chave recusada não
  aparece em `map.json` nenhum, chave aceita aparece uma vez, e não há objeto nosso com chave
  que a fonte não tenha.

### O que fica aberto para o Gui

- **A curva de Galar (pergunta 16)**: o nível é o da fonte, cru, e a fonte é de pós-jogo, então
  Galar ainda nasce em nível alto. **Os 200 de raide e os 89 de geometria** seguem na fila. E
  **Galar continua com Dex 0 na régua**: estático não conta como entrada de Dex de região, e
  ligar isso é escopo.
- **Vencer o estático único não virou caso de suíte.** A vitória FOI medida à mão (a flag foi de
  0 para 1 e o objeto saiu do mapa), mas o Pokémon do menu de debug chega à batalha DORMINDO em
  parte das execuções, sem que o inimigo tenha golpe de sono: flaky por construção, e pendência
  de FERRAMENTA.
- **`lendarios_sinnoh.comportamento` não julga warp morto**: responde MB_NORMAL para os warps 1,
  3 e 4 do `Galar_CrownTundra08` e os três disparam. **T108.2 é flaky**: reprovou por "não andou"
  numa varredura, passou na outra e 3 de 3 isolado.
- **O T11 está 2 de 3, e o verde do T11.3 NÃO vale hoje.** O T11.1 passa, mas o menu de SAVE
  dele para na TELA DE CARTÃO na ROM velha (medido no framebuffer): a save nunca é escrita, e o
  T11.2, que é o controle, cai num menu principal SEM "CONTINUE". Com save inválida, o T11.3
  ("a ROM nova RECUSA a save velha") passa por não ter o que carregar: verde falso. Reprova
  igual com o `testa_critico.py` do HEAD, ou seja não é desta rodada; é calibração do roteiro
  do T11.1 contra a ROM velha.
- **Gens 6, 7 e 9 andaram FORA do repo**, em `fontes-mapas/`: scripts de XY extraídos, Alola com
  268 treinadores com lugar por guia e Paldea com 23 interiores. E seguem abertos os cinco itens
  da 0.m, do `valida_warp_tile` sem linha de base às duas salas do Mt. Coronet.

---

## 0.m O WARP DE OBJETO DE GALAR ANDA, E O ELENCO QUE FALTAVA ENTRA, 22/08/2026 (rodada 5; condutor Opus, dois executores Opus, fechador Opus)

Build verde. **ROM 98,43% de 32 MB** (33.026.864 B, 515,2 KB livres; era 98,38%
na 0.l), EWRAM 86,16% e IWRAM 86,66% (iguais às de ontem), **suíte 794/795**
(só o T11.3 pulado na rodada normal), **T11 3/3** à parte contra a build
`cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`), **SAVE
COMPATIVEL** com SaveBlock1 em 14.964 de 15.872 B e 2.032 layouts numerados sem
nenhum movido, `valida_rom.py` com os 2.378 mapas declarados dentro da ROM,
`guarda_colisao_vars.py` com 23 colisões herdadas em vars e 5 em flags e **0
novas nos dois perfis**, `valida_conectividade` com **0 warps quebrados e nenhum
órfão novo**, `valida_warp_tile --piso 60` com 5.869 de 6.829 warps disparando
(85,9%, igual à 0.l) e os cinco `--demo` de gerador tocados verdes. ROM oficial:
`roms/pokemon-claude-2026-08-22c.gba` (md5 `462fef1424fc2ae5b467346df11f518a`), com o `.map` ao
lado, e o MESMO binário na ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,2% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 96,1% | 100,1% | 96,2% | -- | 55 (3) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 95,4% | 76,3% | 100,9% | 86,8% | -- | 39 (76) | 267 |
| Unova | 99,0% | 102,3% | 99,6% | 100,2% | -- | 30 (2) | 315 |
| Galar | 100% | 113,4% | 100% | **44,1%** | **35,6%** | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.
### As decisões desta rodada

Do Gui: **"pode continuar isso aí tudo"**, que autorizou as duas frentes de uma
vez; **Primal para Maxie e Archie**; **importar o que a fonte tiver**, sem
inventar batalha nenhuma; e o **teto de seis regiões fica de pé**.

Do condutor: **no chefe de equipe vilã a lore vence** (herança da 0.l, e é ela
que põe o orbe na mão do vilão e não do herói). **Kalos, Alola e Paldea não entram no repo**: material e julgamento ficam em
`fontes-mapas/` (`PLANO-OBRAS-KALOS/ALOLA/PALDEA.md`,
`AUDITORIA-PRONTIDAO-2026-08-22.md`, `INFRA-GENS-6-9.md`).

### Frente 1: Galar, blocos c4e e c4f, e o warp que sempre esteve certo

`objetos_galar.py` e `cenas_galar.py`: **58 cenas de objeto em 34 mapas** (eram
31 em 15 na 0.l), com **7 flags de esconder** na faixa 0x1C80 (apelidos de
`FLAG_UNUSED`, save intocada), **5 vars de etapa do c4d** e as 5 do c3 reusadas.
A fila de Galar caiu de 2.597 para **2.570 de 3.195**, a coluna `script` subiu de
33,6% para **35,6%** e a de placas de 43,1% para **44,1%**. T142 4/4 e T130 10/10.

**O `warp` de objeto nunca esteve quebrado.** A 0.l deixou como pré-requisito do
c4e um "aviso grave" dizendo que `warp` de script de objeto traduz mas não troca
de mapa, e que `warp` seguido de `waitstate` prende o jogador para sempre. Está
errado, e a receita boa é justamente a proibida: **`warp` mais `waitstate`**. O
que estava quebrado era a SONDA: ela entrou pelo warp de debug num mapa SEM warp
nenhum (`Galar_StowOnSide02`, `Galar_Wedgehurst09`), pedindo um índice de warp
que não existe, e isso deixa o estado de warp do jogador sujo. A cena rodava e a
troca de mapa não acontecia, e o defeito era do banco de provas. O parágrafo
velho do `PLANO-CONTEUDO-GALAR.md` ficou marcado como vencido, para lembrar que
conclusão tirada de sonda montada errado custou uma rodada de bloco caro.

**O de-para de opcode: 214 contra 214.** A `gScriptCmdTable` do demake tem o
mesmo tamanho da do FireRed, ou seja **nenhum opcode novo**, e o c4e não pedia
motor. O buraco era do nosso lado: o parser de `fala_galar.py` só guardava o
PRIMEIRO ramo das macros de dois ramos (`.ifb \map`), e `applymovement_at` (0x50),
`waitmovement_at` (0x52), `removeobject_at` (0x54) e `addobject_at` (0x56) caíam
no balde de "opcode indecodificável". Conferido pelo fechador: a tabela responde
213 opcodes com tamanho, com os quatro `_at` dentro. E o bloco c4f resolve
`special` por NOME e não por índice (o do FireRed não é o nosso, e por número a
função errada entraria calada): **192 nomes em comum** (444 na tabela do FireRed
contra 623 na nossa, conferido pelo fechador), e de fora ficam **64 chamadas de
`GetQuestLogState`**, motor de Quest Log que não existe aqui.

### Frente 2: Fase F, o Primal, e as batalhas que a fonte tinha

**Primal em Maxie e Archie, sem gastar o gimmick.** O motor foi medido ANTES de a
tabela mudar: a Primal Reversion **não está no `enum Gimmick`**
(`include/battle_gimmick.h:4`), roda sozinha na entrada em campo
(`src/battle_switch_in.c:276`) e não passa por escolha de gimmick nenhuma. Ou
seja o Red Orb no Groudon do Maxie e o Blue Orb no Kyogre do Archie **convivem**
com a Mega Camerupt e a Mega Sharpedo dos aces, e a regra "um gimmick por chefe"
segue de pé. O guarda do gerador aprendeu orbe (`--demo` 10/10, com a mutação de
orbe em espécie sem Primal reprovando).

**Seis batalhas que a fonte tinha e este repo não**, mais oito de uma segunda
leva, todas importadas e nenhuma inventada: SILVER 5, 6 e 7 (ids 2523 a 2525,
fechando as sete batalhas de rival do HGSS), `RYOKU1` (2526), **N** (2527),
HUGH_TEPIG (2528), BIANCA (2529), CHEREN_2 (2530) e as **seis variantes de
Nate/Rosa** (2531 a 2536, gênero vezes inicial, times idênticos mon a mon como na
fonte). A Fase F fecha em **198 batalhas e 1.054 Pokémon**, com Dynamax em 5 (teto
5) e Terastal em 6 (teto 6), as cotas do Gui gastas e não estouradas. T143 22/22.

**O N mudou de tile de propósito**: ficou em (0,4) do `Unova_NsRoom`, o ÚNICO
tile de porta do mapa; quem sai da sala é quem venceu, e o `setflag
FLAG_HIDE_UNOVA_N` mais `removeobject` do fim da batalha é o que devolve a porta.

**Quem NÃO existe na fonte, e por isso não entrou**: Ghetsis, o Shadow Triad,
Courtney e Charon. Dos dois primeiros o BW3G tem texto e nome de música, e nem
constante nem time. Isso sai da fila como inexistente, não como pendência.

### Os casos adversariais do fechador (autor de caso ≠ autor de cena)

`dev_scripts/testes_criticos/144_fechador_r5.json`, 9 casos, 9 verdes.

- **T144.1 a T144.4, o warp de objeto com SAVE no meio.** O T130 prova a receita
  dentro de UMA execução, e execução única não responde se o `warp` de script
  grava `SaveBlock1.location` do jeito que o SAVE espera. Aqui o T144.1 dá
  `ITEM_GO_GOGGLES` pelo menu de debug, sai de `Galar_Underwater01` pelo objeto
  de (32,9) e SALVA já do outro lado; o **T144.2 carrega ESSA save** e faz a
  volta, que passa por `checkitem`, ou seja também prova que a bolsa sobreviveu.
  O T144.4 é o portão: sem os óculos a volta cai no texto de recusa e o jogador
  fica parado. De quebra ficou medido que a `Galar_WildArea17` tem `warp_events`
  VAZIO e o `warp` de script funciona nela do mesmo jeito.
- **T144.5 e T144.6, e eles pediram ferramenta nova**: a suíte sabia dizer QUAL
  Pokémon estava no slot e em que nível, e não sabia dizer se ele estava
  machucado, então cena de enfermeira e cena que só imprime texto eram
  indistinguíveis. O `gba_runner` ganhou **`--hp`** (hp0..hp5 e hpmax0..hpmax5,
  com os offsets medidos pelo probe, porque hp e maxHP ficam FORA do bloco
  cifrado) e o passo de roteiro **`HP=slot=valor`**, que existe porque não há
  caminho de jogo determinístico que machuque um time. Com o Bulbasaur em 1 de
  HP, a enfermeira de `Galar_Wedgehurst03` devolve o HP cheio; o par negativo
  refaz tudo sem apertar A e o HP fica em 1 cravado. **Achado do caso**: o
  `Party… > Set Party` do menu de debug NÃO serve para isto, porque
  `DebugAction_Party_SetParty` não atualiza `gPartiesCount` e `HealPlayerParty`
  itera até ele; com Set Party o time existe na memória e a cura não toca nele.
- **T144.7**: o N sai da porta. O T143.11 prova que a batalha abre e o T143.12
  que o jogador esbarra nele; nenhum dos dois chega ao DEPOIS. Com a
  `FLAG_HIDE_UNOVA_N` acesa (o estado de quem venceu), os MESMOS dois passos do
  T143.12 pisam em (0,4) e o jogador SAI da sala. NPC parado em cima da única
  porta é sala sem saída enquanto ele estiver lá, e agora isso tem caso.
- **T144.8**: o ramo de GÊNERO do Nate/Rosa. O T143.19, o T143.21 e o T143.22
  varrem os três valores do inicial e param todos do MESMO lado do primeiro teste,
  porque a abertura da suíte grava gênero masculino: as três ROSA eram código
  morto para a suíte. Com o `Player… > Toggle gender` do debug e mais nada
  mudando, o oponente passa a ser `TRAINER_UNOVA_ROSA_OSHAWOTT`.
- **T144.9**: os portões dos três Silvers novos não são apelidos um do outro.
  0xEDB e 0xEDC são vizinhas, e trocá-las daria um jogo em que vencer o Silver 5
  faz aparecer o Silver 7, sem erro de build e sem vermelho. Com só a 0xEDB
  acesa, o Centro Pokémon do Indigo Plateau tem que ficar vazio.

### O vermelho que o fechador achou, e o conserto é de uma função

`cenas_galar.py --demo` **nasceu vermelho** nesta árvore: "segunda passada ainda
mexeria em vars.h". Nenhuma letra de conteúdo mudava, só a ORDEM: `poe_bloco`
apagava o bloco marcado e colava o novo no FIM do arquivo, então dois geradores
que escrevem no MESMO header (o bloco c1 daqui e o c4d do `objetos_galar.py`, que
chama esta mesma função) ficavam trocando de última posição a cada rodada. Agora
o bloco é trocado NO LUGAR e o fim do arquivo só é usado quando o bloco é novo.
Os dois `--demo` ficaram verdes e o conteúdo dos headers não mudou uma linha.

### O que fica aberto para o Gui

- **Galar, o que sobrou do c4**: **340 chamadas de `special`** que dependem do
  Quest Log do FireRed, **1.398 linhas de objeto que não estão no mapa** (descarte
  do condutor de 21/08) e **859 encontros estáticos** da fonte medidos e parados,
  esperando decisão de sprite. Galar segue com **zero linha de encontro** e Dex 0.
- **A curva de Galar**: a fonte é de pós-jogo (mediana 70, 276 times no nível
  100). Importada crua, Galar inteira nasce em nível 100.
- **Fase F**: a moldura de torneio da Bianca **não foi portada** de propósito (na
  fonte ela é `scene_script` com `priorityjump`, `setmapscene` e `warpcheck` do
  PWT); só a batalha entrou.
- **Gens 6, 7 e 9**: assets e planos em `fontes-mapas/`, fora do repo, como acima.
- Seguem abertos, da 0.l: `valida_warp_tile` sem linha de base, as 19 bolas de
  neve de Snowpoint, as 31 pedras de Sinnoh, a alcançabilidade de `RavagedPath` e
  de duas salas do Mt. Coronet.

---

## 0.l A DEX FECHA EM 1.571, OS VILÕES ENTRAM E OS CORTADOS SAEM DA ROM, 22/08/2026 (rodada 4; condutor Opus, quatro executores Opus, fechador Opus)

Build verde. **ROM 98,38% de 32 MB** (33.011.952 B, 529,8 KB livres; era 98,85%
na 0.k, ou seja meio ponto e cerca de 150 KB devolvidos), EWRAM 86,16% e IWRAM
86,66% (iguais às de ontem), **suíte 757/758** (só o T11.3 pulado na
rodada normal), **T11 3/3** à parte contra a build `cf6786b2ae` (worktree em
`/private/tmp/claude-501/t11-antiga`), **SAVE COMPATIVEL** com SaveBlock1 em
14.964 de 15.872 B e agora com o **`mapLayoutId` coberto**, `valida_rom.py` com
os 2.378 mapas declarados dentro da ROM, `guarda_colisao_vars.py` com 23
colisões herdadas em vars e 5 em flags e **0 novas nos dois perfis**,
`valida_conectividade` com **0 warps quebrados e nenhum órfão novo**,
`valida_warp_tile --piso 60` com 5.869 de 6.829 warps disparando (85,9%), e os
oito `--demo` de gerador tocados verdes. ROM oficial:
`roms/pokemon-claude-2026-08-22b.gba` (md5 `470666cf982cec334a950db80987a4ea`), com o `.map` ao lado, e o
MESMO binário na ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | 101,0% | 100% | 100% | -- | 52 (0) | 290 |
| Johto | 100% | 96,1% | 100,1% | 96,2% | -- | 55 (3) | 305 |
| Hoenn | 100% | 100,7% | 100,1% | 100% | -- | 39 (21) | 297 |
| Sinnoh | 95,4% | **76,3%** | 100,9% | 86,8% | -- | 39 (**76**) | **267** |
| Unova | 99,0% | 102,3% | 99,6% | 100,2% | -- | 30 (2) | 315 |
| Galar | 100% | 113,4% | 100% | 43,1% | **33,6%** | 48 (32) | 0 |

**Dex obtenível: 1.571 de 1.571, 100%.** Os três números de Sinnoh que CAÍRAM
(objetos 82,7 → 76,3, arte pobre 102 → 76, Dex 295 → 267) não são regressão de
obra: são honestidade. Os 111 mapas cortados viraram túmulo e pararam de
emprestar objeto, arte e encontro a uma coluna que os contava.

### As decisões desta rodada

Do Gui: **"completa a dex, falta 5; pode continuar"**; os **ginásios ficam** como
estão (pergunta 3); e o **Giovanni de Tohjo Falls mantém os níveis 111 a 114**
(pergunta 6), com a palavra dele, *"a curva pode ter outliers coerentes"*.

Do condutor: **no chefe de equipe vilã a lore vence, e o herói é quem cede**
(Maxie fica com Groudon e Archie com Kyogre; Brendan cede para Latios e Wallace
para Palkia); a **`RockPeakRuins` entra no corte da Battle Zone**; e importar
Ghetsis, N e o Shadow Triad **depende de a fonte tê-los**, o que ninguém mediu
ainda, então segue hipótese e não promessa.

### Frente 1: a Dex fecha em 1.571, e o buraco era do CENSO

A 0.k dizia 1.566 e culpava mecânica de troca de forma. Estava errada, e o
conserto é de UMA função: `censo_dex.censo()` fechava um passo só de forma, e as
cinco que faltavam saem de correntes de DOIS e TRÊS passos (Deoxys-Defesa e
Deoxys-Velocidade vêm do Deoxys-Ataque, que vem do Normal; as três formas de
Zygarde saem umas das outras pelo Cube). Com o fecho em cadeia o repositório
responde sozinho, e nenhum estático novo foi preciso. A obra acrescentou os **nove
itens de troca de forma**, entregues pelo NPC do laboratório do Birch com
`checkitem` de guarda antes de cada `additem`. T137 2/2, mais sonda.

**O que o fechador consertou**: a remoção física apagou a tabela de mato da
`Route229`, **única casa de Surskit e Masquerain no jogo inteiro**, e o censo
voltou a 1.569. O conserto é pelo gerador, com a régua nomeada: nasceu
`REPOE_NA_REGIAO` em `distribui_dex.py`, a **única exceção à regra 3** (gen 1 a 5
vai para a região da geração), porque isto é REPOSIÇÃO de um lar que obra nossa
destruiu. O Surskit voltou para `MAP_CANALAVE_CITY`, `fishing_mons`, slot
duplicado 1, em Sinnoh; o **Masquerain não ganha linha e não precisa**, porque é
Bug/Flying, a regra 6 proíbe água para quem não é `TYPE_WATER`, e ele sai do
Surskit por `EVO_LEVEL`.

**O defeito que esse conserto revelou vale mais do que ele**: o `decide_selvagem`
não era estável contra árvore já mexida. Espécie nova no meio da lista empurrava
a escolha de todas as seguintes um slot adiante, e o `aplica_selvagem` deixava
ÓRFÃ a linha antiga que a tabela nova não mencionava mais. Medido: o
replanejamento mexia em NOVE linhas que ninguém pediu, uma delas deixando a
`SeafloorCavernRoom1` com um Salazzle-Totem no lugar do Zubat **para sempre**.
Agora quem já tem escolha gravada e ainda válida FICA ONDE ESTÁ, e o
replanejamento tocou **duas** linhas. Conferido contra o `git`: o
`wild_encounters.json` de hoje difere do de `852be4632a` em **2 slots**, zero
níveis e zero tabelas redimensionadas.

O `diff_do_mato` (T129.13) também estava vermelho e ninguém tinha rodado: exigia
o CONJUNTO de tabelas idêntico ao de `0cb8724099`, e 26 saíram legitimamente com
os cortados. Agora sumir só vale para mapa cortado e **nascer nunca vale**.

### Frente 2: os 40 chefes de equipe vilã

`fase_f_chefes.json` com `papel: "vilao"`, o mesmo gerador idempotente: **40
batalhas, 228 Pokémon, 18 lendários distintos, 39 Mega e 1 Z, e ZERO Dynamax e
Tera novos** (as cotas do Gui, 5 e 6, seguem gastas nos 144 chefes da primeira
leva). A Fase F vai a **184 batalhas e 970 Pokémon**, com a curva de nível
intocada. As quatro trocas de Hoenn foram feitas pelo gerador e não à mão, e **nem
Groudon nem Kyogre ganharam orbe de Primal**, de propósito: Primal entraria POR
CIMA da Mega Camerupt e da Mega Sharpedo e quebraria o "um gimmick por chefe" sem
que o guarda visse, porque ele só conhece pedra de Mega e cristal Z. Tabela e
razão de cada lendário em `PLANO-FASE-F.md`. T138 2/2.

### Frente 3: Galar, blocos c4b a c4d

`objetos_galar.py`: **31 cenas de objeto em 15 mapas e 30 cenas de mapa**, com **5
flags de esconder** (`FLAG_GALAR_ESCONDE_*`, 0x1C80 a 0x1C84, apelido de
`FLAG_UNUSED`, save intocada) em **10 objetos** e **5 vars de etapa**. A fila de
Galar caiu de 2.622 para **2.597** e a coluna `script` subiu de 31,7% para 33,6%.
T139 6/6.

**Diagnóstico pendente, e pré-requisito do c4e**: `warp` dentro de script de
OBJETO traduz e a cena roda, mas **não troca de mapa**; e `warp` seguido de
`waitstate` **prende o jogador para sempre**. Até isso ser entendido, nenhuma
cena portada pode usar `warp`.

### Frente 4: os 111 mapas cortados saíram da ROM, e nenhum id andou

`dev_scripts/remove_mapas_cortados.py`. **111 mapas viraram túmulo** (110 da
primeira medição mais a `RockPeakRuins`, acrescentada pelo fechador por decisão do
condutor: o único warp dela ia para a `Route228` e sem ela o mapa ficava sem
caminho nenhum; as irmãs `IronRuins` e `IcebergRuins` NÃO entram, e foi medido,
porque saem da `IronIslandB3F` e do `MtCoronet_1F_North_Room2`, dois mapas vivos).
**45 layouts exclusivos encolhidos para 1x1**, **26 tabelas de mato fora**, **29
portas fechadas em 23 mapas vivos** com **22 placas** (a 23ª foi embora com a
`RockPeakRuins`), e **24 casos de suíte** que morriam nos cortados removidos.

**Por que a entrada da tabela NÃO é apagada**, e este é o parágrafo que salva a
próxima pessoa: a save guarda **índices**, e são dois.
`SaveBlock1.location.mapGroup`/`mapNum` (0x04) é a POSIÇÃO do mapa dentro do
grupo, e os 111 cortados estão espalhados NO MEIO de nove grupos (o
`gMapGroup_IndoorSinnohPortas` perde 38 de 128, do índice 1 ao 123), então apagar
a entrada desloca todo mapa vivo que vem depois. E `SaveBlock1.mapLayoutId` (0x32)
é o ordinal do layout, e por isso o layout **encolhe** para 1x1 em vez de ser
apagado. Pelo mesmo motivo o warp que ia para túmulo vira **lápide**: a entrada
fica no MESMO índice e passa a repetir as coordenadas do warp vivo de menor índice
do mapa, porque `dest_warp_id` também é índice e a `HearthomeCity` sozinha
perderia os índices 7 e 8 de 16 e desalinharia 14 ponteiros de terceiros. Duas
entradas no mesmo tile: `GetWarpEventAtPosition` devolve a PRIMEIRA, então o
doador ganha e a lápide nunca dispara.

### A guarda nova: `mapLayoutId`, o ponto cego que a própria remoção denunciou

`guarda_save.py` agora cobre o `mapLayoutId`, e a régua **replica o gerador**
(`tools/mapjson/mapjson.cpp:895`) em vez de contar posições no JSON: o número do
layout é a posição contando SÓ os layouts cujo `border_filepath` existe no disco.
Medido: **2.167 entradas no `layouts.json` e 2.032 numeradas**, conferido contra o
`layouts.h` gerado, divergência zero. A consequência é a que assusta: **apagar um
`border.bin` desloca o id de todo layout seguinte**, sem mudar uma letra de
arquivo nenhum e sem erro de compilação, e a save parada lá carrega a geometria de
outro mapa. É por isso que a remoção encolhe o `border.bin` em vez de apagá-lo. O
lado velho vem de `852be4632a` por `git ls-tree` enquanto a impressão gravada não
tiver a chave. Rodado hoje: **2.032 layouts, nenhum movido**.

### Os casos adversariais do fechador (autor de caso ≠ autor de cena)

`dev_scripts/testes_criticos/141_fechador_r4.json`, 8 casos, 8 verdes, cada um
com o par negativo.

- **T141.1 e T141.2**: o T138 provou o Cyrus de Sinnoh e **nenhum caso chegava a
  um Maxie**, que é justamente onde a troca do Groudon foi feita. Agora o caso
  entra pelo warp 1 do `MagmaHideout_4F`, anda três tiles, abre a cena do
  despertar do Groudon e lê `gParties` decifrado: Groudon no slot 4 e Camerupt no
  ace com `ITEM_CAMERUPTITE`. Os números vieram do pré-processador (Groudon 383,
  Cameruptite 323) e não da saída do runner, senão a prova seria circular.
- **T141.3 e T141.4, e este NASCEU VERMELHO**: a suíte só sabia ler o TIME, e item
  de troca de forma não entra em `gPlayerParty` nenhum, ou seja os nove `additem`
  poderiam estar vazios sem um caso reclamar. O `gba_runner` ganhou `--bolsa` +
  `--item`, que varre a bolsa e DECIFRA a quantidade com os 16 bits baixos de
  `encryptionKey` (`src/item.c`), com os offsets medidos pelo probe e nunca
  chumbados. **O achado é do caso**: dos nove itens só CINCO são
  `POCKET_KEY_ITEMS`, e os quatro néctares de Alola são `POCKET_ITEMS`, ao
  contrário do que o comentário do gerador dizia. Por isso a varredura é do
  `struct Bag` inteiro.
- **T141.5 e T141.6**: o T139 prova a mecânica de esconder no `CrownTundra08`, que
  tem UM objeto com flag nova. O `Galar_Hammerlocke05` tem DOIS, e é nele que
  trocar as duas passaria calado; pior, a cena faz `removeobject 4` e
  `removeobject 5`, que são LOCAL IDs de base 1, ou seja os objetos de ÍNDICE 3 e
  4 do `map.json`, e errar a base por um apagaria o vizinho. Com a `BA7` acesa o
  jogador atravessa (16,10) e sai do mapa; com a `BA8`, a do outro NPC, para em
  (16,11).
- **T141.7 e T141.8**: a lápide no caso mais apertado que existe. No
  `CanalaveCityPokecenter1F` a escada do 2F virou uma SEGUNDA entrada em (6,8), o
  mesmo tile do warp 0 que sai para a cidade; pisar ali sai em `MAP_CANALAVE_CITY`
  (28,23), sem travar. Medido de quebra: (1,6), o tile da escada velha, é colisão
  sólida, então aquele warp **nunca disparava nem antes**.
- **T129.18, fora do emulador**: nenhuma das 234 linhas de mato aponta para tabela
  morta (o Burmy-Planta apontava, e o `--selvagem` morria com `SystemExit`), e o
  Surskit está em água de Sinnoh e deixou de ser inobtenível.
- **Passo 5 do `remove_mapas_cortados --demo`**: a pergunta do condutor, "dá para
  entrar num túmulo pelo seletor de capítulo?", foi respondida por medição. **Não,
  e nenhum capítulo precisou sair**: o seletor (`src/chapter_jump.c`) só oferece
  `HEAL_LOCATION` de cidade de ginásio e de Liga. O que faltava era a trava,
  porque o Chapter Jump é o único caminho do jogo que ignora warp: cortar uma
  cidade de ginásio um dia daria um capítulo que larga o jogador num mapa vazio
  SEM SAÍDA, e nem o build nem a suíte diriam nada.

### O que fica aberto para o Gui

- **`warp` em script de objeto de Galar**, o diagnóstico acima, e os blocos **c4e
  (390 indecisos)** e **c4f (282 de `special`)**, os dois caros.
- **A Dex de Galar**: 859 encontros estáticos da fonte medidos e parados,
  esperando decisão de sprite. Galar segue com zero linha de encontro.
- **Importar as batalhas que não existem**: as três de Silver, a `RYOKU1`, os
  rivais do BW3G e, do lado vilão, Ghetsis, N, o Shadow Triad, Courtney e Charon.
  **Ninguém mediu a fonte ainda**, e o BW3G pode não trazê-los, como não trouxe
  rival nenhum.
- **Primal para Maxie e Archie**, se o Gui quiser: custa trocar o gimmick deles.
- **`valida_warp_tile` sem linha de base**: os 85,9% de hoje não têm com o que ser
  comparados, e o portão só cobra piso de 60% por região.
- Seguem abertos, da 0.k e da 0.j: as 19 bolas de neve de Snowpoint, as 31 pedras
  de Sinnoh, a alcançabilidade de `RavagedPath` e de duas salas do Mt. Coronet, e
  a curva de Galar.

**Dívida quitada**: o `T93.6` e o `T85.1`, que desde a 0.i fixavam o molde do
`SendoffSpring` (cortado do escopo e portanto nunca convertido), foram embora com
os outros 22 casos de mapa cortado. A bomba plantada em 0.i saiu do mapa.

---
## 0.k A DEX COMPLETA NAS CINCO REGIÕES, 21-22/08/2026 (rodada 3; condutor Opus, executores Opus, fechador Opus)

Build verde. **ROM 98,85% de 32 MB** (+16 KB sobre a 0.j, 375 KB livres), EWRAM
86,16% e IWRAM 86,66% (iguais às de ontem), **suíte 757/758** (só o T11.3
pulado na rodada normal), **T11 3/3** à parte contra a build `cf6786b2ae`
(worktree em `/private/tmp/claude-501/t11-antiga`), **SAVE COMPATIVEL** com
SaveBlock1 em 14.964 de 15.872 B, `valida_rom.py` com os 2.378 mapas declarados
dentro da ROM, `guarda_colisao_vars.py` com as 23 colisões herdadas e **0 novas**,
e os sete `--demo` de gerador tocados (`distribui_dex`, `objetos_galar`,
`cenas_galar`, `fala_galar`, `fila_galar`, `arte_ginasios_sinnoh`,
`lendarios_sinnoh`) verdes. ROM oficial: `roms/pokemon-claude-2026-08-22.gba`
(md5 `3cd78228b0803ff6ef3ed67100c24fb9`), com o `.map` ao lado, e o MESMO binário na ROM de teste de nome
fixo.

| região | mapas | objetos | warps | placas | script | arte | Dex |
|---|---|---|---|---|---|---|---|
| Kanto | 100% | **101,0%** | 100% | 100% | -- | 52 (0) | **290** |
| Johto | 100% | **96,1%** | 100,1% | 96,2% | -- | 55 (3) | **305** |
| Hoenn | 100% | **100,7%** | 100,1% | 100% | -- | 39 (21) | **297** |
| Sinnoh | 95,4% | **82,7%** | 100,7% | 86,3% | -- | 39 (102) | **295** |
| Unova | 99,0% | **102,3%** | 100% | 99,6% | -- | 30 (3) | **315** |
| Galar | 100% | 113,4% | 100% | **43,1%** | **31,7%** | 48 (32) | 0 |

**Dex obtenível: 1.096 → 1.566 de 1.571 (69,8% → 99,7%).** É a obra que a 0.j
deixou planejada, feita em duas ondas.

### O censo, a régua e a pesquisa

O pedido supunha 1.200 a 1.300 entradas. O censo (`dev_scripts/censo_dex.py`,
importável, com `--demo`) mediu **1.571 entradas distintas de `gSpeciesInfo`**:
1.668 ids do enum menos 97 apelidos, 1.025 bases e 546 formas, porque mega,
gmax, regional, padrão de Vivillon, letra de Unown, sabor de Alcremie e prato de
Arceus são entrada própria. **Armadilha de 243 entradas**: o
`catalogo_especies.py` só enxerga `[SPECIES_X] = { ... }`, e dez famílias são
escritas por MACRO; `censo_dex.entradas_macro()` existe só para isso. **Achado
que vale por si: os iniciais de Hoenn não existiam neste jogo**, o
`SPECIES_TREECKO` só aparecia em `debug.inc` e o Birch entregava os de Johto; os
outros buracos de espécie comum são exatamente os exclusivos de versão, porque
quem importou pegou um lado só.

A decisão mora em `dev_scripts/dex_distribuicao.json`, uma linha por entrada
inobtenível; o executor é `dev_scripts/distribui_dex.py` e não decide nada. As
regras que mudam o resultado: **nível não se toca** (a linha nova herda o nível
do slot, o estático herda o da fonte); **"slot vazio" tem definição medida**, e
não é slot vazio nenhum, são os **5.622 slots duplicados** (48% dos 11.732) em
que a mesma espécie ocupa duas linhas da MESMA tabela, e a nova entra na segunda
ocorrência, de modo que nenhuma espécie da fonte sai e nenhum mapa nem tabela
nova foi preciso; **gen 1 a 5 vai para a região da geração**, sem exceção, e as
gens 6 a 9 vão por bioma tirado do PERFIL DE TIPOS da própria tabela, com empate
resolvido por cota; **água é água**; **lenda nunca vai para o mato**, é sempre
estático; e **nada de trava de pós-jogo**.

A pesquisa de lendários (`dev_scripts/lendarios_referencia.csv`, 117 linhas) leu
o que vanilla e sete rom hacks (Radical Red, Unbound, Renegade Platinum, Sacred
Gold, Blaze Black 2 Redux, Elite Redux, Liquid Crystal) fizeram com cada lenda
fora da região de origem, e decidiu: **lar canônico quando o mapa existe neste
repo, bioma quando não existe**. N's Castle, Abundant Shrine e Liberty Garden
NÃO existem aqui, e nesses casos vale o vizinho mais próximo. A régua sozinha põe
Xerneas em floresta de Johto, Yveltal em torre de Unova, Zacian e Zamazenta nas
Ruins of Alph, Koraidon e Miraidon no Mt. Coronet e Glastrier na neve de
Snowpoint.

### O que entrou, por caminho

| caminho | linhas | onde |
|---|---:|---|
| mato (slot duplicado) | **233** | Kanto 47, Johto 41, Hoenn 47, Sinnoh 54, Unova 44 |
| estático novo | **106** | Kanto 15, Johto 22, Hoenn 16, Sinnoh 14, Unova 39, em 29 mapas |
| presente por NPC | **22** | 3 iniciais de Hoenn por `dynmultichoice`, 19 sem sprite por `givemon` |
| evolução em cascata | **114** | sai de graça quando a base ou a forma entra |
| `EVO_ITEM` novo | **2** | Karrablast e Shelmet, com `ITEM_LINKING_CORD` (id 796, já existia) |

O motor ganhou 29 linhas em `include/regions.h`: **Johto sai por GRUPO DE MAPA**
(84 a 98) e não por mapsec, porque os 65 apelidos de MAPSEC de Johto são todos
`#define ... MAPSEC_SINNOH_WEST` e nenhuma comparação de `sectionId` separa as
duas; Sinnoh, Unova e Galar saem por faixa de mapsec. **Custo de save zero**: é
leitura de `location.mapGroup`, que o motor já gravava. As 106
`FLAG_HIDE_DEX_*` (0x31A0 a 0x3209) mais duas de presente (0x319E, 0x319F) são
apelido de `FLAG_UNUSED`, então `FLAGS_COUNT` não muda.

**Os 5 que faltam, e por quê**: `DEOXYS_DEFENSE`, `DEOXYS_SPEED`,
`ZYGARDE_10_POWER_CONSTRUCT`, `ZYGARDE_COMPLETE` e `ZYGARDE_MEGA`. Nenhum é
questão de lugar: os cinco dependem de **mecânica de troca de forma** que este
jogo não tem ligada (o meteorito das torres para o Deoxys, as células e o Cube
para o Zygarde). Pôr como estático seria mentir a forma.

### Os seis defeitos de gerador que a onda B achou

Todos vieram de rodar o gerador contra a árvore JÁ MEXIDA, que a onda A nunca
exercitou, e todos são de posicionamento silencioso: nenhum dá erro de compilação.

1. **Estático em cima de objeto que já existia**: a busca ignorava os objetos do
   `lendarios_sinnoh` e três caíram sobre o Shaymin, o Heatran e o Regigigas. A
   marca a ignorar virou parâmetro; as dos outros valem como parede.
2. **Estático em cima da CAMINHADA de um caso gerado** (T123.9, T123.10, T123.13,
   T123.14). Não ilhar tile nenhum não basta: caso de emulador é rota exata.
3. **A mesma coisa com caso escrito À MÃO** (T124.11, T124.13, T124.14, no
   Distortion World): nasceu o `corredor_de_casos`, que relê o roteiro de todo
   caso e refaz a caminhada sobre a grade de colisão.
4. **Estático órfão**: mudar um lendário de mapa deixava o objeto velho no mapa
   velho para sempre (SnowpointTempleB5F guardou um em (5,3)).
5. **Rota atravessando linha de visão de treinador** (MtPyre_Summit, quatorze
   tiles antes do lendário). O raio vai nas QUATRO direções, porque NPC anda.
6. **Parede não segura seta**: a perna de zerar escolheu DOWN sobre um
   `MB_SOUTH_ARROW_WARP` na Viridian Forest, o motor decide o warp ANTES da
   colisão, e o jogador foi parar na guarita, dois mapas adiante.

### A janela de 15 sprites, o defeito que não dá sintoma

`OBJECT_EVENTS_COUNT` é 16 e um slot é sempre o jogador, então sobram **15**.
`TrySpawnObjectEvents` acorda todo template dentro de uma janela em volta do
jogador que, refeita a partir de `MAP_OFFSET` 7, é de **20 por 17 tiles**
(`pos.x - 9 <= tile.x <= pos.x + 10`, `pos.y - 7 <= tile.y <= pos.y + 9`). Do 16º
em diante o motor desiste CALADO: o lendário existe no mapa, tem script, tem
flag, e não aparece. Distância de 5 tiles não basta (4 por 4 de 5 em 5 já são
16), e por isso o gerador tem portão de lotação por janela.

**Folga medida pelo fechador em 22/08, e que não estava escrita**: template de
`OBJ_EVENT_GFX_LIGHT_SPRITE` **não gasta slot de ObjectEvent** (o motor o manda
para `SpawnLightSprite`, no ramo de cima do `if`). O `lotacao()` conta as luzes,
então a régua é PESSIMISTA: no `RuinsOfAlph_Outside`, o mapa no teto (15 numa
janela só, ancorada em (8,8), ou seja jogador em (17,14) ou (17,15)), cinco
daqueles 15 são luz e o motor vê 10. **Não afrouxe a conta sem medir de novo**:
errar para esse lado custa um reposicionamento, para o outro custa um lendário
invisível.

**Os 17 quadros por toque não garantem o passo.** Os 202 casos da onda B usam
`17:` e não `16:` para o aperto não empatar com o passo do jogador, que dura 16
quadros; medido em 22/08 no ginásio de Eterna, uma subida reta de 23 tiles com
`17:UP*25` (24 de folga, contando o toque que só vira o boneco) para em (11,10),
treze tiles antes do alvo, e só fecha com `17:UP*40`. Regra: **perna longa e reta
usa contagem SATURANTE com folga larga**, nunca a exata.

### Eterna e Canalave, e o Galar c4a

A pergunta 14 da 0.j foi respondida com obra: os dois ginásios que o corte não
pegou ganharam tileset secundário próprio (`gTileset_FortreeGym` em Eterna,
`gTileset_Lab` em Canalave) pelo `arte_ginasios_sinnoh.py`, que subiu de 6 para 8
ginásios decorados. **Custo de ROM zero** (tilesets que já existiam) e **colisão
idêntica**, conferida byte a byte. T125 em 12/12.

Em Galar, `dev_scripts/objetos_galar.py` portou **8 cenas de objeto em 6 mapas**
(6 NPCs mudos e 2 placas que não existiam), a custo de 0 var e 0 flag; a fila caiu
de 2.630 para **2.622**. O que muda o plano é o tamanho: das 1.891 linhas de
objeto e placa, **1.398 são de objetos que o G4 não pôs no mapa**, então o teto
real do c4a é **79** e não 1.038. Dentro daquelas 1.398 estão os **859 scripts de
encontro estático de Galar**, insumo de uma Pokédex de Galar futura.
**AVISO GRAVE**: `warp` de script de objeto traduz e a cena roda, mas **não troca
de mapa**; e `warp` seguido de `waitstate` **prende o jogador para sempre**.

### Os casos adversariais do fechador (autor de caso ≠ autor de cena)

- **T136.1 e T136.2**: os 212 casos das ondas A e B acendem a `FLAG_HIDE_DEX_*`
  na EWRAM e leem o efeito no MESMO boot, o que prova o motor e não prova ONDE a
  flag mora; e a faixa nova (0x31A0) é OUTRA que a do `lendarios_sinnoh.py`
  (0x3220), a única provada em 21/08. Agora o jogo salva pelo menu, recarrega do
  zero e o tile do Ting-Lu continua vazio.
- **T136.3 e T136.4**: o T129.5 lê UMA espécie do time, então o NPC podia
  entregar seis vezes a mesma forma e passar. Agora os SEIS slots são lidos de
  `gPlayerParty` e cobrados contra a ordem dos `givemon` (1020, 1011, 1009, 1016,
  1019, 1014, que não é crescente nem contígua), com o par negativo que faltava.
- **T136.5 e T136.6**: a cena do c4a agora roda inteira depois de salvar e
  recarregar do zero, e o `release` devolve o jogador a (4,7).
- **T136.7 a T136.10**: Eterna e Canalave não tinham caso NENHUM, nem de chegada.
  Agora a Gardenia e o Byron abrem batalha de verdade, com par negativo cada. O de
  Canalave custou sete flags de derrotado, e a razão está medida: os sete
  treinadores do ginásio são `MOVEMENT_TYPE_LOOK_AROUND` e **não existe caminho do
  warp até o Byron sem atravessar linha de visão**.
- **T129.13, fora do emulador**: o mato conferido contra o GIT
  (`git show 0cb8724099:src/data/wild_encounters.json`), tabela a tabela e slot a
  slot. **1.005 tabelas intactas em número e tamanho, 233 slots trocados, ZERO
  espécies perdidas e ZERO níveis alterados.** O T129.2 comparava o arquivo de
  hoje com ele mesmo desfeito pela coluna `substituido`: se a tabela mentisse, os
  dois lados mentiriam junto.
- **T129.14 e T129.15, por sonda**, porque `GetCurrentRegion` não aparece na
  EWRAM e o teto de sprite não tem sintoma: os `_Static_assert` agora afirmam que
  a **Ilex Forest**, onde mora o Okidogi, cairia em `REGION_SINNOH` pelo mapsec e
  só o ramo do GRUPO a devolve como `REGION_JOHTO`, com `IF_REGION` vivo; e o
  `--demo` refaz `TETO_SPRITE` e `JANELA_SPRITE` a partir de
  `OBJECT_EVENTS_COUNT` e de `MAP_OFFSET` em vez de confiar no número escrito à
  mão. Mutação plantada reprovada nos dois.

**A circularidade do `--demo`**: ele reprovava, e não era defeito de dado. O
`corredor_de_casos` lia os arquivos 129 e 131 a 135, que são ESCRITOS a partir da
tabela depois de ela existir; na segunda rodada o `plano()` reservava corredores
que ele mesmo criara e mudava de decisão (Kanto de 15 estáticos para 16, Johto de
22 para 30), e o autoteste comparava a tabela gravada com um plano que nunca
poderia bater. Conserto: **arquivo derivado desta tabela não entra na conta dos
corredores**, e o `--demo` passa a provar a TABELA GRAVADA contra os mapas, com
um plano refeito do zero cobrando espécie para região e mapa, e não tile, porque
Great Tusk e Scream Tail tiveram o tile movido à mão por linha de visão.

### O que fica aberto para o Gui

- **A Dex de Galar**: 859 encontros estáticos da fonte medidos e parados,
  esperando decisão de sprite. Galar hoje tem zero linha de encontro.
- **Zygarde e Deoxys**: os 5 que faltam pedem mecânica de forma, não lugar.
- **Os chefes de equipe vilã** (Rocket, Magma/Aqua, Galáctica, Plasma) seguem
  fora da Fase F.
- **Galar c4b a c4f**, com o teto real medido e o aviso do `warp` escrito.
- **Remoção física dos mapas cortados**: nada foi apagado, e com a ROM em 98,85%
  de 32 MB é a economia mais óbvia que existe.
- Seguem abertos, da 0.j e da 0.i: as três batalhas de Silver e os rivais do BW3G
  a importar, as 19 bolas de neve de Snowpoint, as 31 pedras de Sinnoh, a
  alcançabilidade de `RavagedPath` e de duas salas do Mt. Coronet, e a curva de
  Galar.

**Dívida que continua plantada**: o `T93.6` e o `T85.1` seguem fixando o molde do
`SendoffSpring`, cortado do escopo e portanto nunca convertido.

---

## 0.j ESCOPO DECIDIDO, LENDÁRIOS, DISTORTION WORLD E FASE F DESTRAVADA, 21/08/2026 (rodada 2; condutor Opus, sete executores Opus, fechador Opus)

Build verde. **ROM 98,80% de 32 MB**, EWRAM 86,16%, IWRAM 86,66%, **suíte
524/525** (só o T11.3 pulado na rodada normal), **T11 3/3** à parte contra a
build `cf6786b2ae` (worktree em `/private/tmp/claude-501/t11-antiga`; `vars` em
0x1678 e 8248 flags do lado velho contra 0x18B8 e 12856 do novo), **SAVE
COMPATIVEL**, `valida_rom.py` dizendo que os 2.378 mapas declarados entraram, e
`guarda_colisao_vars.py` com 23 colisões herdadas e **0 novas**. ROM oficial:
`roms/pokemon-claude-2026-08-21b.gba` (md5
`8c01c21bdaad23f79e93f3b70f852471`), com o `.map` ao lado, e o MESMO binário
na ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

| região | mapas | objetos | warps | placas | script | arte (mediana, pobres) |
|---|---|---|---|---|---|---|
| Kanto | 100% | 100,1% | 100% | 100% | -- | 52 (0) |
| Johto | 100% | 95,2% | 100,1% | 96,2% | -- | 55 (3) |
| Hoenn | 100% | 100,1% | 100,1% | 100% | -- | 39 (21) |
| Sinnoh | **95,4%** | **82,2%** | **100,7%** | **86,3%** | -- | 39 (**102**) |
| Unova | **99,0%** | 99,5% | **100%** | **99,6%** | -- | 30 (3) |
| Galar | 100% | 113,4% | 100% | 42,1% | 31,3% | 48 (32) |

Kanto, Johto e Hoenn subiram para 100% **no commit `e905a87d3d`, de ontem**, por
conserto de régua e não por obra: quem quiser o antes/depois lê a mensagem dele.
O que esta rodada mexeu é Sinnoh e Unova, e por DUAS causas separadas: os cortes
de escopo (mapas, warps e placas) e obra de verdade (os objetos de Sinnoh saíram
de 81,9% para 82,2% com os 10 lendários, e a arte pobre caiu de 105 para 102 com
os ginásios decorados).

### As decisões do Gui, que é o que esta seção existe para gravar

- **Sai do porte**, em Sinnoh: Battle Zone inteira (três Areas, rotas 225 a 230,
  Stark Mountain, Villa, o Frontier de gen 4 e as cinco instalações), Pokémon
  Mansion e Trophy Garden, Turnback Cave / Sendoff Spring / Spring Path, Great
  Marsh, Amity Square, Pal Park, Underground, GTS, Pokétch Company, 2º andar dos
  Pokécenters, Union Room / Wi-Fi / Record Mixing, elevadores da Liga, mapas de
  Mystery Gift, palco de Contest e o Game Corner de Veilstone. Em Unova: Battle
  Tower do BW3G, Cable Club, caça-níquel de Castelia e o 2F do Pokécenter.
- **Fica**: o **Distortion World** (com gravidade normal), os 8 ginásios de
  Sinnoh, o Bug Contest de Johto, o Snowpoint Temple, o trem-bala de Unova e o
  `Restaurant`, que é o Seven Stars do Valor Lakefront com 9 duplas e não fachada
  de Game Corner como o inventário dizia.
- **Uma battle facility só na ROM**, a de Hoenn, alcançável a pé de Johto.
- **Lendário nunca é cortado**: o lar sai, o Pokémon fica, em lugar fácil.
- **A Fase F foi DESTRAVADA**, com regra própria: times no espírito do Radical Red
  modo insano em líder, rival, Elite Four e campeão; **nível da curva intocado**,
  porque quem rebaixa é o modo lv5; lendário em todo chefe de ace acima de 40;
  Mega e Z à vontade, **pouco Dynamax**, **pouco Tera**.
- **Planejada, executa na próxima onda**: Dex completa nas 5 regiões, censo em
  `scratchpad/dex/`.

A régua é `CORTES_DO_GUI` em `dev_scripts/completude.py` (`--detalhe <região>` diz
o que cada grupo tirou) e a cobrança é o status `cortada` de `fila_b6.json`. Texto
em `PLANO-ESCOPO.md`; se ele e a tabela discordarem, a **tabela** está certa.

### O que cada frente fez

- **F1, régua e fila**: 24 grupos de corte na `completude.py`, em dois modos
  (`mapa_fonte` para o que só a fonte tem, `deficit` para o que existe na ROM e
  ninguém vai terminar), com `--demo` cobrindo alvo inexistente e grupo repetido.
  Fila do B6 de **193 para 165 pendentes**, com **28 cortadas**.
- **F2, lendários de Sinnoh**: **10 encontros estáticos** (Uxie, Azelf e Mesprit
  nas cavernas dos lagos, Rotom no Old Chateau, Regigigas no B5F do Snowpoint
  Temple **sem trava de pós-jogo**, Heatran no `MtCoronet_B1F`, Shaymin em
  Floaroma, Darkrai e Cresselia no porto de Canalave, Arceus no Spear Pillar
  atrás de Dialga **e** Palkia), flags 0x3220-0x322A, apelido de `FLAG_UNUSED`.
- **F3, moldes, Distortion World e portas**: os **4 moldes de portão** do escopo
  viraram mapa (`IronIsland`, `MtCoronetOutsideNorth` e `South`, `Route204North`);
  o **Distortion World** nasceu com UM andar 32x32, o Giratina no fundo e portal
  novo no Spear Pillar; `porta_morta.py` mais um `valida_warp_tile.py` que agora
  olha COLISÃO destravaram **9 portas**.
- **F4, arte de ginásio**: 8 `map.bin` de Sinnoh redesenhados. Conferido pelo
  fechador byte a byte contra o HEAD: **colisão e elevação idênticas nos oito, e
  nenhum tile mudou de comportamento de metatile** (a primeira medição do
  fechador acusou 362 mudanças e estava ERRADA: cortava primário/secundário pelo
  tamanho do arquivo, a quarta armadilha do `valida_warp_tile.py`).
- **F5, Frontier por Johto**: porta em `TrainerHill_Courtyard` (24,29) para o cais
  do `BattleFrontier_OutsideWest` (20,68), volta por seta ao sul, UM metatile
  mudado no cais de Hoenn (2 bytes).
- **F6, cenas de Galar**: 16 cenas de map script e 3 `VAR_GALAR_*`; a fila de lá
  foi de 445 para **461 feitas** (3.195 linhas, 2.630 pendentes).
- **Fase F**: **144 batalhas, 742 Pokémon, 61 lendários distintos, 80 Mega, 9 Z,
  5 Dynamax e 6 Terastal**, escritas em `trainers.party` por gerador idempotente
  que só toca bloco de chefe.

### As premissas que a rodada derrubou

1. **Os 144 map_scripts de Galar NÃO são `ON_FRAME_TABLE`** (a 0.i diz isso e
   está errada). No FireRed, que é a fonte do demake, o tipo **3 é
   `ON_TRANSITION`** e o **2 é `ON_FRAME_TABLE`**: os 144 são bytecode solto, sem
   var e sem valor, e tabela de cena a fonte tem **19, em 17 mapas**. Ainda por
   cima **139 dos 144 não escrevem var nenhuma**, e 77 são só dois `setflag` de
   flags que nenhum script LÊ (0x90E tem 98 `setflag` e zero `checkflag`): quem
   as lia era código C do hack, que aqui não existe.
2. **O Distortion World não tem chão na fonte.** Os dez headers do Platinum
   juntos têm no máximo dez tiles andáveis, porque a geometria mora no modelo 3D
   de gravidade variável. O andar que entrou é **invenção declarada**.
3. **Nenhum lendário de Sinnoh existia na ROM**: zero em `wild_encounters.json`,
   zero batalha estática. Havia o que colocar, não o que realocar, e por isso o
   status `realocar` da fila segue em zero linhas (medido de novo hoje: nenhuma
   linha do B6 casa a tabela `LENDARIO_NO_ID`, porque a fila é de `hidden_flag` e
   de gatilho). O pedido do F2 ao dono da fila era, portanto, **um no-op**, e a
   cobrança da realocação mora no `PLANO-ESCOPO.md`.
4. **Vars de Galar: 3 bastaram, não 200.** A conta de 200 a 260 da 0.i vinha da
   premissa 1; com 19 tabelas na fonte, a fase cabe nos **147 que ainda sobram**.
5. **Porta sólida nunca dispara.** O `valida_warp_tile.py` julgava warp só pelo
   comportamento do metatile e dava por boas portas em tile de colisão 1, onde o
   jogador nunca pisa. Passou a olhar os dois.

### O bug que o caso adversarial achou: o Arceus infinito

O portão do Arceus rodava no `ON_TRANSITION` e, a cada entrada no Spear Pillar,
acendia `FLAG_HIDE_ARCEUS_SINNOH` e a apagava se `FLAG_CAUGHT_DIALGA` e
`FLAG_CAUGHT_PALKIA` estivessem acesas. Só que **capturar o Arceus acende essa
MESMA flag**: quem o pegava (o que exige os dois marcos) e saía da sala tinha a
flag apagada na volta, e o lendário nascia de novo, **quantas vezes quisesse**.
Uma flag não distingue "escondido porque o portão está fechado" de "escondido
porque o bicho já foi". Medido no emulador antes do conserto: (13,15), barrado
pelo Arceus, com a HIDE em 0. O conserto é na raiz, em
`dev_scripts/lendarios_sinnoh.py`: nasceu `FLAG_ARCEUS_SINNOH_RESOLVIDO`
(0x322A, apelido de `FLAG_UNUSED`), acesa na vitória e na captura, e ela é a
PRIMEIRA linha do portão. Caso **T123.25**.

### Os outros casos adversariais (autor de caso ≠ autor de cena)

- **T123.21 e T123.22**: os vinte casos do F2 acendem a HIDE na EWRAM e leem o
  efeito no MESMO boot, o que prova o motor e não prova ONDE a flag mora. Agora o
  jogo salva pelo menu e recarrega do zero, e o tile do Uxie continua vazio.
- **T123.23 e T123.24**: o portão do Arceus com UMA flag só. Com um
  `goto_if_unset` a menos os casos do F2 passariam e o Arceus nasceria só com o
  Dialga; as três combinações que fecham o portão agora estão medidas.
- **T124.19**: entrada e saída do Distortion World eram dois casos de mão única,
  cada um do seu warp de debug. O circuito ida-volta-ida corre numa sequência só.
- **T125.11 e T125.12**: a lição da 0.i aplicada. O T115.3 provava só que o
  jogador CHEGA em (11,3); agora ele aperta A e a batalha da Candice abre, no
  ginásio de gelo, o mais arriscado dos oito.
- **T126.9 e T126.10**: a razão escrita da porta nova é que largar o jogador na
  praça o deixaria sem o Frontier Pass PARA SEMPRE, e ninguém tinha medido que a
  cena do Scott dispara para quem vem de Johto: agora uma corrida só vai do warp
  10 da Route 40 até `FLAG_SYS_FRONTIER_PASS` acesa, e outra faz a volta inteira
  até `MAP_ROUTE40` (11,14). Medido e dito: dali até a Olivine City o caminho
  EXISTE (a varredura de colisão alcança a borda leste em (33,13) a (33,18)), mas
  este harness não o estabilizou, e o caso para no chão de Johto em vez de fingir
  que chega na cidade.
- **T127.9 e T127.10**: o T127.4 recarrega a save mas acorda DENTRO do mapa e
  nunca o recarrega, e é o carregamento que roda a tabela de cenas. Agora o
  jogador salva, o jogo recarrega do zero e ele ENTRA de novo: a cena não repete.
- **T128.5**: com LV.5 ligado os seis níveis viram 5, e a partir daí um time da
  Fase F é indistinguível de qualquer outro; pior, quem carrega o Mega é o ACE,
  que é o ÚLTIMO slot e nunca o ativo, e a Mega é um ITEM. O `gba_runner` ganhou
  `--timeinimigo`, que decifra o substruct 0 de `gParties` como `src/pokemon.c`
  faz, e imprime `especie0..5`, `item0..5` e `tera0..5`. As seis espécies do
  Byron e a `ITEM_HEATRANITE` no ace batem com o `fase_f_chefes.json`.

### O elenco de rival: nada ficou de fora, o buraco é do IMPORT

A tabela da Fase F chama a atenção com **4 batalhas de rival em Johto e ZERO em
Unova**. Medido contra `trainers.party` e `opponents.h`, e não contra a memória
das fontes: existem exatamente **quatro** Silver com time próprio
(`TRAINER_JOHTO_RIVAL_SILVER_1` a `_4`) e **os quatro estão na Fase F**; o HGSS
enfrenta o Silver sete vezes, e as outras três nunca foram importadas. Em Unova,
as 403 constantes de `TRAINER_UNOVA_*` **não têm rival nenhum**: os
`TRAINER_BIANCA`, `TRAINER_HUGH` e `TRAINER_NATE` que existem são NPCs de HOENN
(Route 111, Route 119 e o ginásio de Mossdeep), homônimos. Varredura fechada:
**zero** treinadores com `RIVAL` no nome e time próprio ficaram fora da tabela.
O item de fila é **importar** as três batalhas de Silver e os rivais do BW3G;
dar time a eles é depois, com o mesmo gerador.

### O que fica aberto para o Gui

- **A obra da Dex completa nas 5 regiões**, planejada aqui e por executar.
- **Os chefes de equipe vilã** (Rocket, Magma/Aqua, Galáctica, Plasma) não
  entraram na Fase F, por decisão do condutor; são o próximo alvo natural.
- **O bloco c4 de Galar por padrão**: 2.630 linhas pendentes e vars de sobra.
- **Remoção física dos mapas cortados**: nada foi apagado, e os mapas fora do
  escopo continuam compilando, ocupando ROM e alcançáveis por warp. Com a ROM em
  98,80% de 32 MB é a economia mais óbvia que existe; mexe em `data/`, em
  `map_groups.json` e nos warps de lá, então pede build e suíte.
- **Pergunta 14, ainda de pé**: o `BattleFrontier` de Sinnoh vira a praça do
  Platinum ou fica ligado ao Frontier de Hoenn que já existe? E os ginásios de
  **Eterna** e **Canalave**, cujos moldes o corte não pegou, ficam como estão?
- Seguem abertos, da 0.i: as 19 bolas de neve de Snowpoint, as 31 pedras de
  Sinnoh, a alcançabilidade de `RavagedPath` e de duas salas de Mt. Coronet, e a
  curva de Galar (mediana 70, 276 bichos no nível 100, e o struct de party do
  demake que NÃO é o do FireRed).

**Dívida que continua plantada**: o `T93.6` e o `T85.1` seguem fixando o molde
do `SendoffSpring`, que agora está **cortado do escopo** e portanto nunca será
convertido. A dívida da 0.i virou letra morta em vez de bomba, mas os dois casos
continuam medindo um mapa que o Gui decidiu não terminar; quem apagar os mapas
cortados reescreve os dois.

---

## 0.i CONTEÚDO DE GALAR, MOLDES DE SINNOH E PEDRAS, 21/08/2026 (condutor Opus, três executores Opus, fechador Opus)

Build verde. **ROM 98,69% de 32 MB**, EWRAM 86,16%, IWRAM 86,66%, **suíte
443/444** (só o T11.3 pulado na rodada normal, que é o caso de duas ROMs), **T11
3/3** à parte contra a build do commit `cf6786b2ae` (worktree próprio; `vars` em
0x1678 e 8248 flags do lado velho contra 0x18B8 e 12856 do novo), **SAVE
COMPATIVEL**, `valida_rom.py` dizendo que tudo que foi declarado entrou, e
`valida_mapas_sinnoh.py --so-sinnoh` fechando com `bloqueado: 0`. ROM oficial:
`roms/pokemon-claude-2026-08-21.gba` (md5 `c4452153949d42b8aef2f57a65c7678a`),
com o `.map` ao lado, e o MESMO binário na ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada.

| região | mapas | objetos | warps | placas | arte (mediana, pobres) |
|---|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100% | 100% | 52 (0) |
| Johto | 95,9% | 95,2% | 100% | 96% | 55 (3) |
| Hoenn | 100% | 100,1% | 100% | 100% | 39 (22) |
| Sinnoh | 80,1% | **75,9%** (era 75,8) | 97,7% | 81,3% | 39 (**105**, era 104) |
| Unova | 94,2% | 99,5% | 99,3% | 98% | 30 (3) |
| Galar | 100% | 26,7% | 100% | 15,4% | 48 (32) |

**A linha de Galar não se mexeu e isso é defeito de régua, não da onda.** O
`completude.py` lê Galar de censos congelados (`galar_gente.json`,
`objetos_gravados: 1204`, `itens_gravados: 33`) e a onda não os regerou. Medido
hoje no `map.json`: **1.260 objetos**, **394 com script** (era 1) e **85 bg
events** (eram 33). Regerar o censo é item de fila; até lá a linha de Galar diz o
mundo de anteontem.

### O que a rodada fez

- **Galar, onda 1 da fase de conteúdo** (`fala_galar.py`, novo): 337 NPCs mudos
  ganharam a fala da fonte, 52 placas passaram a existir (Galar não tinha
  nenhuma) e 56 bolas de item entraram com **flag própria por bola**, em
  0x1C21-0x1C58, todas apelido de `FLAG_UNUSED` e portanto a **custo zero de
  save**. A fila caiu de 3.257 para 3.195 linhas: 445 feitas, 104 descartadas com
  motivo, 2.646 pendentes.
- **Sinnoh, o 13º molde virou mapa** (`converte_moldes_sinnoh.py`, novo): o
  `OreburghGateB1F` deixou de vestir o molde de portão 13x9 e virou a caverna
  64x32 da grade 2D do Platinum, com 2 NPCs e 3 pedras. Os outros 12 seguem
  parados por decisão do Gui, com o `--dry-run` pronto.
- **Sinnoh, as pedras**: o validador passou a julgar por COMPORTAMENTO de
  metatile e por ALCANÇABILIDADE, não por colisão crua, e o seletor de capítulo
  passou a dar `MOVE_ROCK_SMASH` ao Pikachu (uma linha em `chapter_jump.c`, custo
  zero de save), o que destravou a primeira prova de SMASH da suíte.

### As três premissas que a medição derrubou

1. **As 31 pedras de Sinnoh NÃO são dívida da conversão.** A 0.g dizia que "a
   conversão do Platinum marca o tile da pedra como bloqueado". Errado: o nosso
   `map.bin` é **byte a byte** o do demake 2D em `OreburghGate_1F`,
   `MtCoronet_1F_South` e `MtCoronet_B1F`, e em `RavagedPath` difere em UM tile
   do mapa inteiro, a 20 tiles da pedra mais próxima. Quem não desenhou a
   passagem foi a FONTE. 28 das 31 caem em tile com ZERO vizinho alcançável.
   Deslocamento não salva: varrendo (dx,dz) de -20 a 20, o melhor põe 18 das 27
   pedras de RavagedPath em tile andável e casa ZERO warp. Pôr essas pedras é
   DESENHAR corredor, ou seja decisão de fase e não conversão.
2. **Eram 13 mapas de molde, não 12.** Há DOIS moldes no repo,
   `LAYOUT_ROUTE226_ACCESS` e `LAYOUT_ROUTE208_ACCESS`, e `planta_provisoria`
   sempre pegou os dois. Quem enxergava só 12 era a **lista escrita à mão** da
   fila, que escondia o `OreburghGateB1F`. A fila passou a tirar a lista da
   medição.
3. **O pool de flags é 5.711 e não 1.375.** O 1.375 da 0.h era o que o harness
   conseguia NOMEAR, não o que existe. Medido por `flags_livres.py`: **5.711
   livres**, 4.447 numa faixa contígua. Flag não é gargalo nesta fase.

### Vars de Galar: sobram 150, e a saída é uma var por MAPA

Dos 512 endereços 0x4000-0x41FF, 16 são `TEMP_VARS`, 346 têm dono declarado (318
citados de verdade, 28 recuperáveis um a um) e **150 estão livres**
(0x417E-0x41BF, 0x41D6-0x41FF, 0x4107-0x412F, 0x4100). A fase de conteúdo estima
200 a 260, ou seja **déficit de 50 a 110**, e crescer `VARS_COUNT` quebra a save.
**A saída recomendada é uma var por MAPA com o valor codificando a etapa**, que é
o que o FireRed faz com `VAR_MAP_SCENE_*`: cabe folgado, não abre janela de save,
e o preço é não ter duas cenas independentes no mesmo mapa. O bloco c3 (144
linhas de `ON_FRAME_TABLE` puro) é o teste dessa escolha: fazer 12 e MEDIR antes
de comprometer a faixa. **ERRADO, e corrigido na 0.j:** no FireRed o tipo 3 é
`ON_TRANSITION`, não `ON_FRAME_TABLE`; os 144 são bytecode solto, e tabela de
cena a fonte tem 19, em 17 mapas. Por isso 3 vars bastaram, e não 200. Rascunho em `PLANO-CONTEUDO-GALAR.md` (é rascunho de
executor, não decisão).

### O achado da rodada: dois Pokécenters de Sinnoh não curavam

`JubilifeCity_PokemonCenter_1F` e `SandgemTown_PokemonCenter_1F` tinham
enfermeira com sprite, script de cura e movimento certo, e mesmo assim **não
havia de onde falar com ela**. Medido no emulador contra a ROM de 19/08, com par
positivo e negativo: em Jubilife o jogador terminava em (3,4) COM e SEM o A; a
MESMA rota em Oreburgh travava em (7,4) com o A e andava até (5,4) sem ele.

**O conserto que a fila mandava fazer estava errado, e o número mostra por quê.**
Ela pedia `MB_COUNTER` no metatile de balcão, que é o 545 do
`gTileset_PokemonCenter`; ele aparece TRÊS vezes na linha do balcão de TODOS os
20 Pokécenters desse tileset, Hoenn incluída, então dar `MB_COUNTER` a ele
abriria conversa através da parede em 20 mapas para consertar 2. O defeito era a
COORDENADA: varridos os 67 mapas com enfermeira com script, **65 põem a moça em
cima da coluna que tem `MB_COUNTER`** (517 em Hoenn e no resto de Sinnoh, 664 em
Johto e no Mt. Silver, 577 em Unova, 774 no Trainer Hill) e só estes 2 caíam
fora. As duas foram para (7,2). Casos T122.1 a T122.4.

**Lição, de régua e não de mapa: "o NPC está lá" não é "dá para falar com ele".**
Entre o objeto e a conversa há um atributo de metatile, e nenhuma medida de
completude enxerga isso.

### Os casos adversariais (autor de caso ≠ autor de cena)

- **T120.9 e T120.10 (Galar)**: a bola é pega, o jogo SALVA pelo menu e a save é
  recarregada do zero. Os casos que já existiam acendiam a flag à mão na EWRAM, o
  que prova o motor e não prova ONDE a flag mora: se as 56 tivessem caído na
  faixa temporária ou acima de `SPECIAL_FLAGS_START`, todos passariam e o jogador
  ganharia o item de novo a cada boot. Passou: a flag sobrevive.
- **T112.5 (pedras)**: o par NEGATIVO do de cima. O jogador quebra a pedra, sai
  pelo B1F, volta e ela está lá, porque a memória do smash é `FLAG_TEMP_2` e
  `ClearTempFieldEventData` zera a faixa a cada carregamento de mapa. Era o que a
  0.g afirmava sem medir, e é dele que depende o custo zero de save das 478
  pedras.
- **T121.6 (Oreburgh)**: o T121.2 provava que a escada dispara e que o mapa é o
  certo, e parava aí; mapa certo não é tile certo. Agora a chegada é medida:
  subindo pela escada de verdade o jogador para no MESMO (7,5) em que o T112.2
  para saindo do mesmo tile por warp de debug.
- **T121.4 nasceu FLAKY e foi reescrito pelo fechador**: terminava um tile abaixo
  do ciclista `WANDER_AROUND` de (37,12), que o próprio T121.3 já tinha
  descartado como alvo. Três rodadas isoladas: OK, OK, FALHA. A perna final virou
  DOWN, saturando em (50,14), longe de tudo que se mexe. **Mesma família do
  T98.9 e do T108.2.**

### O que fica aberto para o Gui

- **Os 12 mapas de molde de Sinnoh**: a ferramenta não trava mais nada, falta
  gosto. A troca entrega forma honesta e desenho chapado: a arte cai de 46-48
  metatiles distintos para 5-9 e Sinnoh vai de 105 para 116 mapas abaixo do piso.
  O prêmio contado na fonte são 91 objetos e 36 placas, sendo 30 e 20 só no
  `BattleFrontier`. **Pergunta separada: o `BattleFrontier` de Sinnoh vira a
  praça do Platinum (a fonte) ou fica ligado ao Battle Frontier de Hoenn que já
  existe na ROM?**
- **A curva de Galar**: 278 ids de treinador citados pelos scripts, 774 Pokémon,
  **mediana 70 e 276 exatamente no nível 100**. A fonte é pós-jogo, não campanha;
  importada crua, Galar inteira nasce em 100. É a mesma decisão que congelou a
  Fase F. **Aviso: o struct de party do demake NÃO é o do FireRed** (só 165 dos
  741 times passam com o molde do FR); medir o stride antes de acreditar.
- **A Fase F continua congelada** por decisão dele de 19/08 (carta de trabalho na
  0.h). Seguem abertos as 19 bolas de neve de Snowpoint, os 8 ginásios de Sinnoh
  sem arte, as 31 pedras (agora com o motivo certo), a alcançabilidade de
  `RavagedPath` e de duas salas de Mt. Coronet (257, 652 e 153 tiles ilhados) e o
  censo de Galar por regerar.

### Dívida plantada: dois casos fixam um molde que vai morrer

**`T93.6` e `T85.1` VÃO QUEBRAR no dia em que o `SendoffSpring` for convertido, e
quem converter reescreve os dois na MESMA rodada.** O T93.6 prova
`layout: LAYOUT_SENDOFFSPRING`, o molde 13x9, e o id muda com a planta nova; o
T85.1 anda `16:RIGHT*11` dentro de um mapa de 13 colunas para chegar ao
`MAP_TURNBACK_CAVE_ENTRANCE`, e no 64x64 essa rota não chega a lugar nenhum.

**Régua para quem escrever rota**: andabilidade se mede por COLISÃO **e
ELEVAÇÃO** (o lago do `OreburghGateB1F` tem colisão zero e elevação 1); warp só
dispara sobre metatile com comportamento de porta ou escada (a primeira conversão
do B1F nasceu de mão única sobre chão comum); a primeira tecla de uma direção
nova só VIRA o boneco; e **aperto mandado durante a animação de escada é
COMIDO**, então perna logo depois de warp precisa de espera antes.

---

## 0.h ENCERRAMENTO DO PRD-GOAL, 19/08/2026 (condutor Opus, executores Opus)

**O goal `PRD-GOAL.md` está CUMPRIDO no escopo que ele define, com UMA fase
congelada por decisão do Gui.** Handoff da próxima sessão:
`/tmp/handoff-pokemon-claude-2026-08-19.md`; auditoria item a item:
`/tmp/fechamento-prd-2026-08-19.md`.

Build verde, **ROM 98,58%**, EWRAM 86,16%, IWRAM 86,66%. **Suíte 413/414**
(só T11.3 pulado na rodada normal, que é o caso de duas ROMs), **T11 3/3**
à parte, **SAVE COMPATIVEL**, `valida_rom.py` dizendo que tudo que foi
declarado entrou. ROM oficial: `roms/pokemon-claude-2026-08-19b.gba`
(md5 `8f90f12f1279e557dd0f41899fa7d057`), com o `.map` ao lado, e a mesma
build na ROM de teste de nome fixo, também com o `.map` casado.

### Critério do PRD, item a item

| critério | veredito |
|---|---|
| suíte verde completa | **cumprido** (413/414, zero vermelho) |
| T11 3/3 contra a ROM congelada | **cumprido**, com o T11.3 provando a RECUSA da save velha |
| fila sem pendente executável | **cumprido**: de 15 para **0**; os 192 que sobram têm bloqueio medido |
| Galar jogável | **cumprido no escopo da obra** (ver decisão abaixo) |
| ROM oficial + ROM de teste | cumprido, com `.map` ao lado das duas |
| ESTADO com seção de fechamento | esta seção |
| memória apontando o estado final | cumprido |
| handoff de encerramento | cumprido |

### Duas decisões de condução que ficam escritas, para ninguém reabrir

1. **"Galar jogável" vale pelo critério final, não pelo "Pronto quando" da
   Fase E.** O texto da Fase E pedia insígnias e Liga, mas a decisão 1 do
   próprio `PLANO-OBRAS-GALAR.md` mandou cena, treinador e ginásio para uma
   fase de conteúdo separada, e foi assim que a obra rodou. Galar hoje é a
   região inteira andável (149 mapas a pé pelo barco, com volta, provado
   nos casos T108.4 a T108.6), com 26,7% de objeto, zero cena e fila
   própria de 3.257 linhas. **A Liga de Galar é fase futura nomeada**, não
   pendência escondida deste goal.
2. **A Fase F está CONGELADA pelo Gui**, não esquecida: "nao quero mexer em
   times de lideres ainda nem curva de nivel, deixa todos lv 5, pra eu
   poder testar o rom" (19/08/2026). A medição dela foi feita e está na
   carta de trabalho abaixo, para quando ele destravar.

### O que a Fase F mediu antes de congelar (carta de trabalho)

- **7 chefes SEM GIMMICK NENHUM, e isso é defeito, não desenho**: os três
  campeões de Unova (`GENESIS`, `JUNIPER_*`) e os E4 `COLRESS`, `ELESA`,
  `MARSHAL`. Nasceram no B6, depois do B8, e o `gens69_treinadores.py`
  nunca rodou de novo. É o clímax do jogo sem mecânica.
- **26 blocos com Dynamax sem lenda** (eram 22 no B8; Sinnoh e Unova
  ganharam chefes depois). Dar lenda exige trocar o mais fraco do time, o
  que contraria "a fonte entra primeiro": decisão do Gui.
- **Curva: quatro regiões de cinco estão certas.** Johto tem 76 mons acima
  do teto, e **24 deles são a S.S. Aqua** (níveis 120 a 128, teto 100),
  importada depois da rodada de curva e nunca reescalada. O 25º é o RED do
  Mt. Silver, com 149, provavelmente proposital.
- **Os 41 grupos de Pokécenter**: 28 são executáveis (o motor tem
  `ClearDailyFlags`, sobram 52 flags no bloco diário e a faixa de id
  2523-3999 está livre); os 13 do Mart são Mystery Gift, que não existe
  neste motor, e devem sair do escopo.
- **Armadilha para quem executar**: `gens69_treinadores.py --aplicar` NÃO é
  idempotente. Rodar de novo hoje acrescentaria 580 Pokémon e 44 lendas,
  porque ele só olha "tem vaga". Consertar isso é parte do trabalho.

### O que a leva de encerramento consertou

- **Johto parou de mostrar bola de item onde não há bola**: 1171 objetos
  restaurados pelo que a fonte diz (775 Pokémon de overworld, 219 efeitos
  de luz, 49 pedras, 33 canteiros, 13 árvores de Cut). Custo zero de ROM
  nos Pokémon, porque o desenho vem de `gSpeciesInfo`. **61 tiles andáveis
  abriram**: efeito de luz é tratado antes de virar object event.
- **A fila passou a CALCULAR bloqueio** lendo `vars.h` e `flags.h`, em vez
  de confiar no campo escrito à mão. Bloqueio some sozinho quando a var
  nascer.
- Duas armadilhas silenciosas de ferramenta: o validador de Sinnoh
  contava Pokémon de overworld como sprite inexistente e, com
  `--corrigir`, trocaria 781 deles por boneco genérico; e o harness não
  conseguia nomear nenhuma das 1375 flags do pool novo, porque o regex
  exigia hexadecimal maiúsculo.

### O que fica aberto, dito

Fase F inteira (congelada), os 8 ginásios de Sinnoh sem arte (decisão de
desenho do Gui, com amostra pronta em `.../scratchpad/AMOSTRA_oreburgh_4_
caminhos.png`), as 19 bolas de neve de Snowpoint (mecânica), os 12 mapas
de Sinnoh que são molde de portão, as 31 pedras dentro de parede, a fase
de conteúdo de Galar (3.257 linhas) e as gens 6-9 paradas por decisão de
17/08. **ROM em 98,58%, com cerca de 460 KB livres.**

---

## 0.g ONDA DE JANELA ABERTA E A RODADA DE COMPLETUDE, 18-19/08/2026 (condutor Fable até o G5, depois Opus; executores Opus)

Build verde (**ROM 98,58% de 32 MB**, EWRAM 86,16%, IWRAM 86,66%), **suíte 399/400** na hora em que a seção foi escrita (hoje são 414 casos,
413/414; ver 0.h),
**T11 completo 3/3**, e **SAVE COMPATIVEL** depois da regravação da
impressão. ROM oficial: `roms/pokemon-claude-2026-08-19.gba`, com o
`.map` gravado ao lado (faltava, e o T11 precisa dele), e a mesma build na
ROM de teste de nome fixo. **Dex obtenível: 1.571 de 1.571, 100%**, intocada nesta rodada. Commits: `f23c4e4ab2`, `c68e11fc55`,
`3f922f893d`, `01b1874b83`, `fe8668803c`, `001ea8e056`.

### A JANELA DE SAVE ABRIU E FECHOU DE NOVO. A save antiga NÃO carrega mais

Decisão do Gui em 18/08/2026: pode quebrar a save, porque o Chapter Jump
repõe o progresso em minutos. A onda fez o que a janela fechada proibia e
**a janela está FECHADA outra vez** desde a regravação da impressão.

O pool de flags cresceu (`FLAGS_COUNT` 8248 para 12856, SaveBlock1 em
94,3% com 431 B de folga até o teto de 97%), as item balls de Johto
ganharam flag própria uma a uma, e 19 vars de cena de Kanto saíram de
cima do estado de Hoenn.

**O defeito que o adversarial achou é a lição da rodada: a save velha não
era recusada, era lida errada em silêncio.** O checksum batia por acidente
(o setor é zerado antes de gravar, e os bytes a mais somam zero), então
`GetSaveValidStatus` devolvia OK e o jogo carregava com todas as vars
deslocadas 288 posições, Pokédex embaralhada, creche com Pokémon de
espécie inválida e até 153 item balls nascendo como já pegas. **Carregar
lixo calado é pior do que perder a save.** `SAVE_LAYOUT_REVISION` entrou
na assinatura de setor: o menu agora abre só com NEW GAME (medido em
print, não deduzido), e o T11.3 foi reescrito para provar o comportamento
NOVO, ou seja a recusa.

Três camadas de trava, e a terceira nasceu porque as duas primeiras
dependiam de memória humana: o guarda detecta o deslocamento; a
amarração reprova deslocamento sem subida de revisão; e o `--gravar`, que
era escape hatch mudo, passa a RECUSAR gravação com quebra e revisão
parada (`--forcar` existe e exige decisão escrita).

### Portão de colisão: o que o pré-processador resolve, não o que o texto diz

Ferramenta nova, `dev_scripts/guarda_colisao_vars.py` (faz vars e flags,
`--flags`), lendo o valor que o `cpp` devolve. Achou o que ninguém sabia:

- **38 endereços de var com dois donos vivos**, sendo **19 a doença real**
  (cena de FRLG gravando sobre estado de Hoenn; medido: o `setvar` da
  Pallet Town escrevia em `VAR_LITTLEROOT_TOWN_STATE`). Os 19 foram para
  0x41C3-0x41D5. As outras 19 são utilitárias e ficam declaradas.
- **Duas flags de Johto em 0x4000 e 0x4001**, que são flags especiais do
  motor. Nasceram de um `#ifndef` de import que inventava endereço quando
  não achava o nome. O portão passou a reprovar `#ifndef` nesses headers:
  **mata a classe, não só o caso**.

Calibração medida: em vars, apelido é regra larga; em flags, tem que ser
a forma exata, senão faixa gerada por base mais deslocamento fica
invisível justo para o portão que existe para vigiá-la. E a ordem dos
headers segue a ordem do include, senão o portão grava o corpo de um
arquivo e o valor de outro (foi o falso positivo de 0x20).

### A régua enxerga arte, e Galar entrou na tabela

`completude.py` contava presença e nunca abria o desenho. Era por isso que
Unova aparecia com 94% sendo máscara de colisão em duas cores, e **o erro
só caiu porque o Gui olhou o jogo e desconfiou**. Coluna de arte nova
(mediana de metatile por mapa, piso 10), e Galar como sexta linha, pelos
censos e nunca por nome de grupo.

Dois documentos meus estavam mentindo e foram corrigidos com data: a arte
de Unova já tinha sido feita em 12/08 (mediana 30, não 3; 2 mapas abaixo
do piso, não 155), e a queda de objetos de Sinnoh não era regressão, era
denominador maior mais 270 NPCs inventados apagados de propósito.

### Sinnoh: o buraco era pedra, e a arte de ginásio não existe

- **Completude de objetos de Sinnoh: 60,2% para 75,8%.** Dos 594 objetos
  que faltavam, **447 eram pedra de Rock Smash**, não gente. Entraram 478
  em 28 mapas, **a custo ZERO de save**: o motor pede flag por pedra, mas
  da faixa temporária, então pedra quebrada volta ao sair e entrar, que é
  o comportamento do jogo original.
- **O portão de tranca recusou 14 pedras** que fechavam caminho, provado
  por BFS sem Rock Smash na mochila, nos dois estados. Ele foi consertado
  no meio: a primeira versão reprovava pedra por defeito que já existia
  (seis mapas de Sinnoh nascem com warp fora do alcance a pé, porque a
  fonte pede Surf ou Strength ali).
- **A fonte de Sinnoh não tem arte de ginásio.** O Platinum guarda esses
  mapas como modelo 3D; o 2D carrega só colisão e comportamento, de 2 a 6
  valores. Já emitíamos mais do que a fonte sabe dizer. Conferido na
  segunda fonte: o "Oreburgh Gym" do demake gen 3 é byte a byte o ginásio
  da Roxanne. **A prova pixel a pixel que vale para Unova é indefinida
  para Sinnoh**; a camada certa aqui é o comportamento.
- **`MB_ICE` é atributo, não arte**: 5 metatiles em append (92 B)
  devolveram os 497 tiles de gelo de Snowpoint e as passagens direcionais
  de Oreburgh. Hoenn não mudou um pixel (bytes antigos são prefixo exato
  dos novos).

### Lições novas

- **Com gelo, colisão livre não significa que dá para parar ali.**
  Snowpoint tem 531 tiles andáveis e 84 paradas. Régua de treinador tem
  que separar quem precisa de conversa (parada colada) de quem batalha por
  vista (basta pisar).
- **Em mapa de gelo, os apertos seguintes são comidos enquanto o jogador
  desliza.** Caso de suíte ali precisa de ~240 quadros entre pernas, não
  60.
- **Coordenada errada só aparece quando alguém tropeça.** Os NPCs dos oito
  ginásios de Sinnoh estavam 1 tile abaixo porque ginásio tem UM warp e a
  régua de translação não podia provar nada, então a identidade assumiu,
  cega ao recorte. Não é epidemia: medido nos 353 mapas com NPC
  importado, o desvio é só dos ginásios.
- **Pareamento por nome nosso esconde duplicata**; por evento da FONTE,
  não. Oreburgh tinha a mesma pessoa duas vezes, invisível enquanto as
  duas estavam desalinhadas.
- **`pgrep -f <script>` dentro de um laço que contém esse nome se
  enxerga.** Espera de processo casa por PID guardado. Um `pkill` por
  padrão de texto matou vigias de outra onda nesta rodada.
- **Flaky conhecidos, não regressão**: T98.9 (Unova, VirbankCity) e
  T108.2 (Galar, Circhester06), os dois por NPC que passeia sobre tile de
  gatilho. Rodar isolado 3 vezes antes de acusar.

### O que fica pendente, dito

- **Os 1211 objetos de Johto com sprite de item ball sem serem item
  ball** (a fonte diz efeito de luz, pedra, canteiro, NPC). É o maior
  defeito visível do repo hoje, está na fila com critério de aceite.
- **12 mapas de Sinnoh são o molde de portão 13x9, não mapa** (o Battle
  Frontier é o maior prêmio parado ali: 24 NPCs e 25 placas). Critério de
  detecção é medido, comparação de blockdata contra o molde, nunca nome.
- **31 pedras de Sinnoh caem dentro de parede**, porque a conversão do
  Platinum marca o tile da pedra como bloqueado. Dívida de geometria.
- **As 19 bolas de neve de Snowpoint** com a pergunta de mecânica em
  aberto (empurrável no GBA é bloco de Strength; o Platinum empurra sem
  HM). Enquanto não entrarem, **NÃO realinhar os 3 treinadores** que
  estão 1 tile fora de propósito.
- **Os 8 ginásios de Sinnoh continuam abaixo do piso de arte** e só saem
  de lá inventando desenho, que é decisão do Gui, ainda em aberto.
- `valida_warp_tile.py` não mede Galar (o filtro é por nome de grupo e o
  alocador espalhou 344 dos 438 mapas em grupos alheios).

---

## 0.f FECHAMENTO DA FASE E, GALAR ENTRA COMO SEXTA REGIÃO, 18/08/2026 (condutor Fable até o G5, depois Opus; executores Opus)

Build verde (**ROM 98,55% de 32 MB**, EWRAM 85,94%, IWRAM 86,66%), **suíte
372/373** (só T11.3 pulado, que é o caso de duas ROMs), **T11 completo 3/3 à
parte** contra `roms/pokemon-claude-2026-08-15c.gba`, e **SAVE COMPATIVEL**
(SaveBlock1 em 14388 B de 15872, 90,7%; os 438 mapas de Galar entraram todos
em append). ROM oficial: `roms/pokemon-claude-2026-08-18b.gba`, e a mesma
build sobrescreveu `roms/pokemon-claude-teste-2026-08-16.gba` (md5
`ac8ed5419ab69cacece45ad6479e6063` nas três).

Commits do dia, em ordem: `b61e3fbc12` (G4, gente e itens), `b25f786253`
(miúdas), `4c0368bea0` (Route 222), `3d867acdfc` (arte de Johto),
`2c82216fc0` (pendências de Sinnoh e Johto), `86deaf89c0` (G5),
`ebd8cb29a2` (plano da janela aberta).

### O que Galar é hoje, e o que ela não é

É **geometria inteira e conteúdo nenhum**: 438 mapas com tilesets provados
pixel a pixel, 1.473 warps, 1.203 NPCs mudos, 33 itens escondidos, 12 heal
locations e música traduzida por medição (id da fonte mais 212). Não tem
cena, treinador, encontro, ginásio nem Liga: isso está na fila gerada
`dev_scripts/fila_galar.json`, com **3.257 linhas** chaveadas pela FONTE e
não pelo nosso nome, porque o G3 renomeou 140 mapas.

O Gui entra em Galar pelo barco, em qualquer um dos cinco portos, atrás de
`FLAG_GALAR_QA_ANDAR` (apelido de UNUSED), com marinheiro de volta em
Wedgehurst: **149 mapas a pé, volta de 147**. O Chapter Jump ganhou Galar
como sexta região, e com ela a regra de que heal location zero significa
região sem Liga, senão o seletor ofereceria capítulo que não leva a lugar
nenhum.

### As duas premissas que a medição derrubou nesta fase

1. **Os "455 warps mortos de Galar" não eram herança do desvio MB_NORMAL do
   G1.** São 477 em 211 mapas, e **435 têm comportamento MB_NORMAL na
   própria fonte**: o demake também não dispara. Só 13 vinham do G1. Quem
   deriva "o comportamento certo a partir do contexto" recebe de volta
   `MB_NORMAL`, porque é o que a fonte diz. O resgate que entrou é estreito
   de propósito, aceita só byte baixo que dá PORTA, e ressuscitou 11 warps
   de Circhester. Lição: **hipótese de causa escrita num plano não é
   medição**, e o executor que mede tem o dever de contradizer o plano.
2. **A Route 222 não estava partida onde o plano dizia.** A coluna 91 não é
   a estrada, a entrega em Sunyshore é por warp de portão e sempre
   funcionou. O partido era a entrada norte vinda de Valor, um bolso de 4
   tiles onde elevação 3 contra 4 barrava o passo **sem aparecer na
   colisão**. Três tiles viraram `ELEVATION_TRANSITION`, diff de 3 palavras.

### O defeito de família que apareceu de graça

As 3 placas ilegíveis da Route 222 não eram defeito de mapa: o
`importa_npcs_sinnoh.py` converte coordenada **por escala** da caixa da
matriz do Platinum sobre o nosso layout, e a escala engolia até 4 tiles
onde o layout é redesenho 1 para 1. Duas das três placas não tinham nenhum
tile andável na frente, ou seja o jogador nunca poderia lê-las. O conserto
mora no gerador (`deslocamento_de_warp`, translação provada por dois warps,
mais a lista autorizada `REDESENHO_1PARA1`). **Outros 7 mapas de Sinnoh
seguem na conversão por escala, com 15 placas já gravadas**, e estão na
fila: mover placa já gravada é conteúdo, se mede uma a uma.

### Lições novas, para quem escrever caso ou esperar processo

- **`pgrep -f <nome do script>` dentro de um laço que contém esse nome se
  enxerga.** Um `pkill` disparado por esse padrão matou os vigias de outra
  onda (sem perder dado, porque a suíte dela já tinha terminado). Espera de
  processo casa por **PID guardado**, nunca por padrão de texto.
- **T98.9 (Unova, VirbankCity) é flaky conhecido, não regressão.** O objeto
  12 daquele mapa passeia numa caixa 2x2 que cobre os três tiles de gatilho
  do caso, então a semente do relógio às vezes fecha o caminho. Verde em 4
  de 4 rodadas isoladas. Conserto honesto é pinar RNG ou mexer no NPC, que
  é conteúdo de Unova.
- **O procedimento do T11 ficou mais caro do que estava registrado.** A
  worktree da ROM antiga agora precisa de `make generated` inteiro (não só
  `map_groups.h`: também `layouts.h`, `region_map_sections.h`,
  `heal_locations.h` e os `trainers.h`), com os binários de `tools/` da
  árvore principal copiados para lá.
- **A fala de 5 páginas custou 16 apertos de A, não 11.** Com 11 o `msgbox`
  ficava aberto na última página e o `setvar` nunca rodava: o caso
  reprovava por motivo que não era o gatilho.
- **`OBJECT_EVENTS_COUNT` 16 é teto de objetos SIMULTÂNEOS**, não de
  templates: a save guarda 64. Mapa com 17 objetos não é defeito (o máximo
  simultâneo medido no Lago da Fúria é 6).

### O que fica pendente, dito

- **A janela de save está autorizada a abrir** (decisão do Gui de
  18/08/2026, porque o Chapter Jump repõe o progresso). Nada do que foi
  commitado hoje abriu: a árvore ainda é SAVE COMPATIVEL. A onda tem plano
  próprio, `PLANO-JANELA-ABERTA.md`, e roda antes da Fase F.
- **A faixa de flag de Johto acabou** (192 de 192) e ganhou o transbordo
  `0x1D00`-`0x1D3F`, 62 vagas. **`P_FLAG_FORCE_SHINY` agora aponta para
  `FLAG_TEMP_7`**: acender essa flag em qualquer outro lugar faz todo
  selvagem nascer shiny.
- **`valida_warp_tile.py` não enxerga Galar de verdade**: o filtro é por
  nome de grupo e o alocador espalhou 344 dos 438 mapas em append dentro de
  grupos alheios, então `--regiao Galar` aferiria 283 de 1.473. Não entrou
  em `REGIOES` de propósito (lição 4.3). Quem mede Galar hoje é o censo do
  `mundo_galar`.
- **218 mapas de Galar seguem fora do grafo alcançável** (226 warps sem
  destino representável, 188 apontando para mapa vanilla do FireRed) e
  **4 portas de mão única**, as quatro sujeira da fonte. Estão na fila.
- **ROM em 98,55%, sobram cerca de 470 KB.** A fase de conteúdo de Galar não
  cabe nessa folga sem orçamento. Corte por espaço continua sendo portão da
  condutora com o Gui, nunca decisão de executor.
- Herdadas e sem mexida: mecânica de parceiro (desenho), Amity Square e
  Stark Mountain medidos e parados na fila (a saída da Stark é decisão
  pendente, a fonte não tem porta de volta), corrente da bomba de Pastoria
  nunca jogada de ponta a ponta por humano.

---

## 0.e FECHAMENTO DA OBRA DE SINNOH, 18/08/2026 (condutor Fable, executor Opus)

Build verde (ROM 97,68% de 32 MB, EWRAM 85,94%, IWRAM 86,66%), **suíte
322/323** (só T11.3 pulado, porque ele é o caso de duas ROMs), **T11 completo
3/3 à parte** (a save da `roms/pokemon-claude-2026-08-15c.gba` carrega na build
nova) e **SAVE COMPATIVEL** (a obra não criou item nenhum; SaveBlock1 em
14388 B de 15872, 90,7%). ROM: `roms/pokemon-claude-2026-08-18.gba`, e a mesma
build sobrescreveu `roms/pokemon-claude-teste-2026-08-16.gba` (md5 conferido,
`16426067c02ccb74e51275ad141e021d` nas três).

### O que a obra de Sinnoh foi, do começo ao fim

Cinco ondas mais a leva final, todas desenhadas por `PLANO-OBRAS-SINNOH.md` e
executadas contra `dev_scripts/maquina_sinnoh.json`, o censo que a máquina do
bloco S1 gera:

- **Onda 1 (S1+S2)**: a máquina de vars, flags e gatilhos. 49 alias de var no
  gap `0x4130`-`0x415F` (+`0x41C2`), 157 flags novas em `0x1B00`-`0x1B9C`, e os
  esqueletos de cena plantados nos `scripts.inc`; mais os 8 grupos de
  `hidden_flag` que já estavam sem bloqueio.
- **Onda 2 (S3)**: arco de abertura (Twinleaf, casa do jogador, Verity, Sandgem,
  Route 202).
- **Onda 3 (S4/S5)**: Jubilife/Oreburgh/Eterna e Hearthome/Veilstone/Pastoria.
- **Onda 4 (S6)**: arco da Galáctica, rivais de Pastoria e do portão 209,
  treinadores 2508-2513.
- **Onda 5 (S7)**: pós-liga, Cyrus do 4F (2514) e o fim das cenas por arco.
- **Leva final (S8)**: a bomba de Pastoria inteira, o Croagunk da placa, o rival
  do Pokécenter da Liga (2515-2517), e a FIAÇÃO que sobrou das ondas.

Casos de suíte da obra: **T100 a T104**, e os nove **T104** são desta leva.
Faixa de treinador de Sinnoh: 2500-2517 gastos, 2518-2519 livres.

### A fiação que a leva final fechou, e por que ela existia

Três correntes estavam escritas e **inalcançáveis**, cada uma porque o escritor
da var morava num arquivo que a onda dona da cena não tinha escopo para tocar.
As três foram ligadas aqui, com o desvio da fonte documentado valor a valor:

1. **Partida da corrente de Pastoria.** O único `SetVar VAR_PASTORIA_CITY_STATE,
   1` da fonte inteira mora na cutscene do armazém da Galáctica de Veilstone
   (`scripts_veilstone_city_galactic_warehouse.s:89`), cutscene que esta casa
   descartou ao redesenhar o armazém. O `setvar` entrou no ponto equivalente do
   fluxo NOSSO, colado na mesma fala (`..._Text_WeDidntLearnMuch`), com
   `call_if_eq ... 0` na frente para a corrente nunca ANDAR PARA TRÁS.
2. **Fecho pós-vitória do ginásio de Pastoria.** A fonte escreve 3 no ginásio e
   só chega a 4 na cutscene `PastoriaCity_OnFrame_ExitGym`, que não foi portada.
   O ginásio passou a escrever **4 direto** (o 3 é invisível: nada neste
   repositório o lê), mais os dois `setflag` que a fonte põe na mesma linha
   (esconder o Grunt_M, bloquear o evento do Croagunk).
3. **Atores da cena da bomba.** O S7 escreveu a coreografia supondo um fecho
   pós-ginásio que revelaria Crasher Wake e Rival; esse fecho não existia, e os
   `applymovement` mirariam objetos ausentes. A própria cena passou a revelá-los
   (`clearflag` + `setobjectxyperm` + `setobjectmovementtype` + `addobject`, o
   molde que o `RivalBattle` do mesmo arquivo já usava), nas coordenadas
   convertidas da fonte: Wake em (37,9) e Rival em (34,13). E o fecho ganhou o
   `setflag` que faltava antes do `removeobject` do Wake: sem ele a cutscene
   inteira ficava replayável pelo clique nele.

Entrou também o `ON_TRANSITION` de PastoriaCity, porte do
`PastoriaCity_OnTransition` da fonte. Ele zera `VAR_SINNOH_PASTORIA_CROAGUNK_CENA`
a cada entrada no mapa (sem isso o sorteio de 10% da placa acontece UMA vez na
vida do save, porque a própria cena escreve 1) e reposiciona o rival depois da
explosão (sem isso ele volta ao tile que o `setobjectxyperm` da batalha gravou
no SAVE, do outro lado da cidade).

### As duas ferramentas, consertadas na causa

- **`dev_scripts/maquina_sinnoh.py`**: o `--demo` era vermelho num ponto só, o
  `coord_event` do Buck da Route 227 gravado em (30,19), tile que uma rodada
  ANTERIOR escolheu e que hoje é ruim (o objeto do próprio Buck nasceu em cima
  dele). A realocação só sabia casar pela posição ORIGINAL da fonte, e a posição
  velha não batia com nada. Nasceu `plano_de_reparo`, que também casa por
  SCRIPT o que está gravado e ruim sem explicação, e o manda para o tile que o
  censo de hoje escolheu. Corrigido para (29,19), `--demo` verde, `--gravar`
  idempotente.
- **A idempotência custou uma tabela nova, e ela é a lição.** O primeiro
  `--gravar` verde **ressuscitou 8 `coord_events` que levas anteriores tinham
  APAGADO de propósito**: os três falso-gatilhos da onda 4 (CanalaveCity,
  GalacticHQ_Hall e MtCoronet_1F_South, todos com cena equivalente já existente)
  e o span do Collector do Valor, que a onda 5 escolheu tile a tile no
  `map.bin`. **Gerador que não sabe o que a mão decidiu desfaz a decisão
  calado.** `LEVA_DONA` lista os quatro, com commit e motivo, e a máquina não
  planta, não move e não apaga nenhum deles.
- **E a fila mexeu embaixo da máquina, que é o achado mais perigoso do dia.**
  `maquina_sinnoh.py` escolhia o que portar filtrando `status == "pendente"` no
  `fila_b6.json`, e a alocação de flag saía dessa mesma lista. Quando a fila
  aprendeu `feita`/`descartada`/`adiada`, o conjunto de entrada encolheu de 164
  para 56 e de 247 para 126: um `--gravar` inocente teria **reescrito o bloco de
  flags de Sinnoh com endereços diferentes**, embaixo das dezenas de cenas que
  já citam esses apelidos por nome. Duas travas entraram: a seleção passou a ser
  por REGIÃO e TIPO, sem olhar status (`entradas_da_fila`), e **endereço de flag
  já gravado virou HISTÓRIA** (`alias_ja_gravados` lê o bloco do `flags.h` e
  devolve nome e endereço; alocação nova só existe para nome que nunca saiu, e
  entra em append depois do maior endereço já apelidado da faixa, contando
  também os que a condutora autorizou à mão fora do bloco). Consumo depois
  disso: **158 flags** (as 157 de antes mais
  `FLAG_SINNOH_ESCONDE_VEILSTONE_CITY_GRUNT_M_STORAGE_KEY` em `0x1BA1`, que é a
  calibração do falso "feita" virando endereço reservado para quem escrever a
  cena). Conferido: a ROM recompilada depois dessa linha tem o MESMO md5, porque
  apelido que ninguém cita não muda binário.
- **`dev_scripts/fila_b6.py`**: aprendeu que **esqueleto não é cena**. Gatilho
  cujo rótulo só tem `@ TODO` + `end` deixou de contar como feito
  (`rotulos_com_cena`), e isso desmascarou **38 gatilhos** que a fila dava por
  prontos. E aprendeu as decisões DATADAS da obra: dois status novos,
  `descartada` e `adiada`, com o motivo escrito em cada linha.

### O placar da fila, antes e depois (`python3 dev_scripts/fila_b6.py`)

| tipo | antes: pend. / feitas | depois: pend. / feitas / descart. / adiadas |
|---|---|---|
| sinnoh `coord_event` | 73 / 91 | 56 / 51 / 39 / 18 |
| sinnoh `hidden_flag` | 206 / 70 | 126 / 69 / 35 / 46 |
| **pendentes do B6 inteiro** | **312** | **215** |

O que saiu de "pendente" por DECISÃO, e não por trabalho: os 34 clones (o campo
`hidden_flag` da fonte guardando `MAP_HEADER_*`), os 27 do Amity e os 5 de
mecânica inexistente (decisões 3 e 4), os 41 de Pokécenter/Mart (decisão 6), os
17 de acompanhante (decisão 5), os visitantes da Villa, e Amity e Stark exterior
como **descartados-por-mapa-provisório**. Mais três calibrações registradas: o
grunt da Storage Key de Veilstone, que era falso "feita"; os trainers do
`MtCoronet1FTunnelRoom`, que moram DE PROPÓSITO em outros mapas; e os
`coord_events` decorativos dos portões de molde 13x9.

### As lições de harness, consolidadas

Valem para quem escrever caso novo. Todas medidas, nenhuma deduzida:

1. **N+1 apertos por perna.** O runner segura o botão 6 quadros, e isso só VIRA
   o jogador quando a direção é nova e ele está parado: perna de N tiles em
   direção nova custa N+1 apertos.
2. **Depois de uma perna que SATURA contra parede, a direção nova não custa o
   aperto de virar.** Medido nesta leva, com traço de EWRAM: um `RIGHT` de dois
   apertos contado como um tile andou DOIS e pôs o caso na coluna errada. As
   duas regras juntas são o motivo de a régua boa ser "não conte tile".
3. **~2 apertos de A por página de `msgbox`.** Espera é de graça, aperto de A
   não é: A que sobra pode escolher coisa em menu.
4. **Porta de casa só desce**, e **porta é WARP mesmo com colisão 1**: subir
   para dentro dela tira o jogador do mapa. Foi assim que o par negativo da
   bomba terminou dentro do portão do observatório enquanto o positivo passava
   (a cena trancava o jogador antes de ele chegar na porta).
5. **Tapete de saída é seta sul**: precisa de pausa e de um aperto a mais.
6. **Elevação barra sem aparecer na colisão** (`IsElevationMismatchAt`); o bit
   de colisão do `map.bin` não mostra isso.
7. **Colisão não barra warp de seta**: a borda de conexão atravessa.
8. **Rota se mede no `map.bin`, e se confere no traço de EWRAM.** Sempre que
   der, use perna que SATURA: perna saturada não tem ambiguidade de um tile. Se
   nenhuma perna saturar no eixo que interessa, faça a rota SERPENTINA entre
   duas paredes, e **deixe o gatilho no MEIO da perna, não na ponta** (o
   `coord_event` dispara ao ENTRAR no tile).

### O que fica pendente, dito

- **Mecânica de parceiro que anda junto** (decisão 5): as 6 vars dos cinco stat
  trainers e do rival esperam desenho de mecânica.
- ~~**`MAP_ROUTE222` está partida no meio**: nenhuma entrada do lado de Valor
  alcança a borda de Sunyshore. Pendência de MAPA, não de cena.~~
  **RESOLVIDA EM 18/08/2026, e o diagnóstico acima estava mirando a costura
  errada.** A coluna x=91 nunca foi a estrada: a Route 222 entrega em Sunyshore
  por WARP, pelo portão `(89,23)` -> `Route222_Access` -> `(11,5)` ->
  `SunyshoreCity (4,48)`, e a coluna x=0 de `SunyshoreCity` é água ou parede em
  todas as linhas, então abrir a borda direita não levaria a lugar nenhum. O
  que estava partido era a ENTRADA NORTE de Valor, e era pior: com a estrada
  sul trancada de propósito pelo Collector (sem escritor para
  `VAR_SINNOH_VALOR_BLOQUEIO_SUNYSHORE` neste porte), a norte era a única, e
  ela caía num bolso de 4 tiles, `(0,3)` a `(3,3)`, porque a linha 3 estava em
  elevação 3 com a região grande em elevação 4 logo abaixo (lição 6 desta
  mesma seção: elevação barra sem aparecer na colisão). Sunyshore era
  inalcançável a pé vindo de Valor. Conserto em
  `dev_scripts/conserta_route222.py` (3 tiles viram `ELEVATION_TRANSITION`,
  metatile e colisão intactos, arquivo do mesmo tamanho), prova em **T107.1**
  (`dev_scripts/testes_criticos/107_pendencias.json`), que fica vermelho se os
  três tiles voltarem para elevação 3. Detalhe medido em
  `PLANO-OBRAS-SINNOH.md`, seção "CORREÇÃO DE ROUTE 222, 18/08/2026".
- **Amity Square e Stark Mountain exterior são provisórios**: as cenas existem e
  estão corretas, e voltam a existir quando os mapas reais do Platinum forem
  importados. **Medidos em 18/08/2026 e PARADOS por decisão da condutora**: vão
  para a fila de conteúdo, não para uma onda. Os dois são viáveis sem tileset
  nem tile novo (Amity 64x64 com matriz própria e coordenadas de evento já
  locais; Stark 32x32 com offset exato de (736,224)), e a Stark tem uma decisão
  pendente da condutora com o Gui antes de qualquer execução: a fonte não tem
  porta de volta para a Route 227, então ou se inventa a saída ou o mapa vira
  de mão única. Números, custos e a armadilha inteira em
  `PLANO-OBRAS-SINNOH.md`, seção "AMITY SQUARE E STARK MOUNTAIN OUTSIDE".
- **Visitantes da Villa**: a máquina de `VAR_RESORT_VILLA_VISITOR` não existe
  neste motor.
- **Pokécenter/Mart** (41 grupos): batalha diária e Mystery Gift, polimento de
  fim de projeto.
- **Biblioteca de Canalave**: continua sem escopo escrito (herdado do ESTADO 0).
- **Dialga/Palkia do Spear Pillar** e o clímax da explosão dos lagos: fora desta
  obra.
- **`Route210_North`**: mapa não importado.
- Da própria corrente de Pastoria: o valor 6, que a fonte põe em
  `scripts_valor_lakefront.s:364`, continua sem escritor aqui, de propósito.

---

## 0.d CONSOLIDAÇÃO DE 17/08/2026 (condutor Fable, executor Opus)

Build verde (ROM 97,60% de 32 MB, EWRAM 85,94%, IWRAM 86,66%), **suíte 255/256**
(só T11.3 pulado) mais os **2 casos novos T99** no mesmo binário, **T11 completo
3/3 à parte** (a save da 2026-08-15c carrega) e **SAVE COMPATIVEL** com a
impressão regravada por causa dos itens 877 a 879 (append puro, nada movido).
ROM: `roms/pokemon-claude-2026-08-17.gba`, e a mesma build sobrescreveu
`roms/pokemon-claude-teste-2026-08-16.gba`.

O que entrou: consertos de removeobject em quatro mapas de Unova (ON_LOAD roda
antes de os objetos nascerem; virou ON_TRANSITION com FLAG_UNOVA_CENA_JUNIPER,
contrato agora com oito mapas); validador de IS_FRLG de Sinnoh; modo de teste
com seis opções no menu de opções; itens INFINITE_CANDY, INFINITE_REPEL e
CHAPTER_JUMP; o seletor de capítulo, que substitui a introdução do professor
no jogo novo (nome RED, rival GREEN, masculino); e as 426 flags de Kanto que
valiam o literal 0 ganhando número (a cadeia Bill, S.S. Ticket e policial de
Cerulean religada; 178 item balls de Kanto com flag real).

**Dois defeitos reais achados pela consolidação, os dois medidos no emulador:**

1. **O seletor de capítulo travava o jogo, sempre.** `waitstate` depois de
   `dynmultistack` para o contexto uma SEGUNDA vez (o próprio comando já chama
   `ScriptContext_Stop`), e quem religa é a tarefa do menu, que já religou.
   New Game abria o seletor, o menu fechava na escolha e o jogador ficava sem
   andar, sem menu e sem R+START. Regra que fica: **`dynmultistack` NÃO leva
   `waitstate` atrás**; o modelo certo é `data/scripts/travessia_regioes.inc`.
2. **AUTO RUN muda a gramática de andar.** Correndo, mudar de direção LOGO
   DEPOIS de um passo gasta um aperto só para virar, e parado não gasta.
   Medido nas duas ROMs com o mesmo roteiro (T80.1): na build de 15/08 o
   `16:RIGHT` depois de dois `16:UP` anda; com AUTO RUN ligado ele só vira.
   Reprovou 15 casos de percurso. AUTO RUN passou a nascer DESLIGADO em
   `src/new_game.c`; a opção continua no menu, a um toque. TURBO A/B ficou
   ligado (dispara com 20 quadros de botão segurado, o gba_runner segura 6).

**Abertura da suíte remedida** (`ABERTURA` em `dev_scripts/testa_critico.py`):
4 A exatos até NEW GAME, esperas generosas, `20:DOWN*5` até START FROM
BEGINNING e 2 B de rede; caiu de ~10.700 para ~2.100 quadros. Regra nova:
**espera é de graça, aperto de A não é**, porque depois que o seletor abre
dois A escolhem região e capítulo e o caso acorda em outra região. A abertura
velha virou `intro_carvalho`, escolhida por `--abertura`, e é ela que o T11.1
usa contra a ROM antiga (que ainda tem a intro do Carvalho). Quatro roteiros
do quarto até a rua foram remedidos no framebuffer (o jogo novo nasce em
(6,6) no quarto; a porta do 1F em (4,8) só dispara descendo).

Casos novos: **T99.1 e T99.2** (`99_chapter_jump.json`), com par negativo,
provando o seletor por fato de memória (Planalto Índigo com as oito insígnias
acesas; Pallet Town com as oito apagadas).

Riscos abertos: LV.5 TRAINERS, batalha opcional e animação pós-KO sem prova
direta de suíte (nenhum caso joga batalha até o fim); T90.5 segue calibrado
sobre o defeito conhecido do Kiyo; a impressão do guarda usa espaço de índice
próprio em `dados/items` (itens novos aparecem como 920-922 lá; o id real é
877-879), anotado para não assustar auditoria futura.

## 0.c RODADA 3 DE 15/08/2026: AS DUAS OBRAS DE UNOVA (Fable condutor)

Build verde, **suíte 255/256** (T11.3 pulado na rodada normal) e **T11 completo
3/3 à parte** (save da 2026-08-15b carrega). ROM a 97,64% (+43 KB, na conta do
desenho). SAVE COMPATIVEL direto (zero item/contador novo nesta rodada).

**Obra 2 (changeblock) COMPLETA**: os 12 mapas de planta dupla de Unova
funcionam (7 de troca de nível, 3 de pedra de Strength, 2 de interruptor).
Pedra cai em buraco de verdade (MB_MT_PYRE_HOLE por atributo de metatile
exclusivo, censo-trava em `pedra_buraco_unova.py`; motor:
`HandleBoulderFallThroughHole` roda o coord_event do tile). Elevador do
Virbank Complex RELIGADO (warps em append, nada renumerado). O B2F dos 4
interruptores virou renderizador de estado provado nas 16 combinações
(`prova_b2f_interruptores.py`). Armadilha registrada: a marca `agua` do
gerador é relativa ao map.bin, então o caminho de VOLTA também precisa de
`setmetatileinrange` com elevação explícita (12 quadrantes na Victory Road
incluem 4 de borda que a marca não pega).

**Obra 1 (setscene) COMPLETA**: 71 gatilhos + 59 cenas nos 23 mapas (A2
gerador, A4 sem batalha, A5 arco INFER com 19 batalhas ids 2148-2168, A6
abertura/portões). Ramo por starter é INVERTIDO de propósito (o rótulo da
fonte nomeia o Pokémon DELA). Dois setmapscene remotos por setvar. NPCs de
cena escondidos por FLAG_TEMP_11/12 recalculadas no ON_TRANSITION (zero bit
de save; contrato documentado nos arquivos). Abertura da casa da mãe
protegida (barco desembarca em VIRBANK, casa fica em HUMILAU; cena roda uma
vez e nunca prende). PLANO-OBRAS-UNOVA.md agora carrega a tabela de
conversão e a decisão 7 (relógio do gen 2 descartado).

**Fila recalibrada: 444 pendentes** (era 633): Unova 29, Sinnoh 411, Johto 4.
Três consertos de régua: asserts de invariante (nunca fotografia), regra
"flag citada inexistente = bloqueado" (FightArea voltou a bloqueado), e
identidade por flag dispensa raio de posição (Sinnoh 84 objetos casados).

**Casos novos: 19 (T98.1-19, `98_unova_obras.json`)**, todos verdes, com o
par negativo onde a prova positiva passaria com o mundo quebrado. Limite de
harness documentado: nenhum caso joga batalha até o fim, então consequência
pós-vitória (ex.: var remota do porão de Nimbasa) fica sem prova direta.

Pendências vivas: cena do MARLON em Undella (priorityjump, fora do gerador
de gatilhos; chip de task criado); LIFT_KEY não portada (ninguém a entrega
em Unova; elevador ficou destrancado de propósito); Rt23East Lower/Upper
são changeblock FORA da fila dos 12 (stub documentado); os 29 pendentes de
Unova são portáveis-com-bloqueio residual + 2 changeblock + 2 batalhas + 1
setscene, ver fila_b6.json.

## 0.b RODADA 2 DE 15/08/2026 (Fable condutor, agentes executores)

Build verde, **suíte 236/237** (T11.3 pulado na rodada normal) e **T11 completo
3/3 rodado à parte** (save da ROM 2026-08-15 carrega na build nova, que criou
itens). ROM a 97,51%. **Impressão de save REGRAVADA** (`guarda_save.py
--gravar`): a varredura antiga contava 8 constantes que nunca foram item de
save (`ITEM_USE_*`, `ITEM_FIELD_ARROW`); a corrigida prova zero item real
movido e os 2 sinos no FIM. Regra: item novo é append no fim, e a impressão
se rebendiz depois, com a leitura de fantasma zero conferida.

O que entrou: **Johto leva 2** (ITEM_CLEAR_BELL 875 e ITEM_TIDAL_BELL 876;
arco dos sinos completo: Baoba na Route 39 com escolha GOLD/SILVER, cameo do
rival, 5 Kimono no teatro ids 2464-2466/2468-2469, Ho-Oh e Lugia nível 100;
RED no Mt. Silver id 2467 com OBJ_EVENT_GFX_RED_2 e palette própria 0x1134,
decisão 3; Lugia pousa na BEIRA (29,15) porque a metade norte da câmara é
água legítima da fonte); **Sinnoh leva 3** (9 grupos de hidden_flag da rota
principal: Spear Pillar, Mt. Coronet, Eterna 4F, Veilstone, QG 1F, Lago Valor,
Floaroma, Route 205; 1 flag nova FLAG_SINNOH_LAGO_VALOR_ESVAZIADO, 4
reusadas); **fundação de Unova** (PLANO-OBRAS-UNOVA.md com as 6 decisões de
15/08; 27 vars e 41 flags aliasadas; dev_scripts/changeblock_gen2.py com
--demo que reconstrói 39 mapas byte a byte e os 5 números do desenho
fechando exatos; macro changeblock_gen2 em asm/macros/event.inc); **17 casos
de teste novos** (T90.14, T91.7-11, T97.1-11). Consertos de raspão: cena do
KIYO batalhava o Kiyo VANILLA (regressão de gerador, consertada NO GERADOR;
já era a 2ª vez que um conserto manual era comido por --aplica); queda de
rótulo com portão novo no porta_cenas_johto.py.

Gasto da rodada: 2 itens, 5 flags (4 Johto + 1 Sinnoh), 3 vars de Johto,
27 vars e 41 flags de Unova (fundação, ainda sem consumidor), 6 ids.

Próximo da fila de Unova: executores B3/B4 (changeblock dos 12 mapas, a
ferramenta está pronta) e A2-A6 (setscene; A3 treinadores agora está livre
porque Johto devolveu opponents.h/trainers.party).

## 0.a LEVA DE 15/08/2026 (Fable condutor, agentes executores)

Build verde, **suíte 219/220** (só T11.3 pulado na rodada normal) e **T11
completo rodado à parte: 3/3, a save da ROM 2026-08-12b carrega na ROM nova**
(worktree do commit antigo + `--rom2`; os headers gerados do worktree vieram
copiados da árvore principal porque nenhum mapa novo entrou). ROM entregue:
`pokemon-claude-2026-08-15.gba` no workspace, 97,48% de 32 MB.

O que entrou: **B10/overworld** (220,8 KB de volta; 152 sprites `.smol`;
estouro de VRAM no Battle Dome achado por prova de emulador e desfeito ali;
ferramenta `comprime_overworld.py`); **B6 Johto** (duelos GIOVANNI e
EUSINE/SUICUNE, 4º duelo do rival no subterrâneo, choro da WHITNEY com a
insígnia via BRIDGET, raio de visão devolvido a 17 treinadores de torre/farol
que já existiam com ids 1340-1357; o "grunt do subterrâneo" da fila era
fantasma; OLIVINE adiada de propósito, gatilho da fonte inalcançável);
**B6 Sinnoh** (21 objetos em 2 levas nos mapas da Galáctica + LakeVerity +
FightArea conferido; os 20 grunts do Hall somem com FLAG_GALACTICA_QG_TOMADO
na queda do Saturn); **casos T90.8-13** (autor ≠ executor da cena); fila
`fila_b6.json` calibrada três vezes (conteúdo em vez de proxy, raio 4,
fallthrough). Gasto de recursos da leva inteira: 3 flags, 2 vars, 2 ids.

Pendências novas ou vivas: decisão do Gui sobre o sprite do RED_2 (duelo do
Mt. Silver); arco dos sinos bloqueado por ITEM_TIDAL_BELL/ITEM_CLEAR_BELL
inexistentes (criar item no fim da lista não quebra save, mas ninguém criou
ainda); as duas obras grandes de Unova (máquina de setscene, 59 cenas;
tradutor de changeblock, 108 cenas) precisam de desenho antes de executor;
B10 restante (ícones ~673 KB, indireção de treinador ~485 KB, ambos pedem
mudança de engine); `porta_ginasios_johto.py` continua com a landmine de
reescrever map.json inteiro (rodar `porta_cenas_johto.py --pokemon --aplica`
depois dele); os itens de FightArea na fila são falso "sem bloqueio" (flag
inexistente, corrigir na próxima regeneração).

## 0. PASSAGEM DE BASTÃO da sessão de 12/08/2026 (Fable condutor)

### Conserto da noite de 12/08: NPCs verdes de Kanto (palettes FRLG nunca registradas)

O Gui jogou a ROM de entrega e viu os NPCs do laboratório do Oak com as cores
estragadas (verdes). O defeito existia desde pelo menos 05/08 e passou por toda
a suíte porque a suíte só lia EWRAM. Causa: quando os gráficos FRLG foram
destravados para a build Emerald (guardas `#if IS_FRLG` removidas de
`object_event_graphics.h` e `object_event_graphics_info.h`), a TERCEIRA guarda
ficou: a tabela `sObjectEventSpritePalettes` em `src/event_object_movement.c`.
Os tags 0x1129 a 0x1133 (NPC_BLUE/PINK/GREEN/WHITE, METEORITE, SS_ANNE,
SEAGALLOP e os dois do player FRLG) existiam na ROM mas nunca eram registrados;
`LoadObjectEventPalette` devolvia 0xFF e o sprite desenhava com a palette de
outro dono. Conserto: guarda removida com o mesmo comentário `(antes: ...)` dos
outros dois arquivos. Lição: destravou gráfico condicionado, procure TODAS as
ocorrências da condição, `grep -rn IS_FRLG src/ include/`.

Para essa classe nunca mais passar: o `gba_runner` ganhou `--palobj 0xXXXX`
(diz se a cor de 15 bits está na PLTT OBJ, 0x05000200-0x050003FF, fato de
memória e não pixel), o `testa_critico.py` ganhou a prova `palobj_presentes`,
e o caso novo `T96.1` (`16_kanto_palettes.json`) warpa ao laboratório e cobra
uma cor de `npc_white.pal` e uma de `npc_green.pal`. Calibrado nos dois lados:
FALHA na ROM de entrega de 12/08 (0x0227 ausente; 0x32B9 sozinho não
discrimina, coincide com palette já carregada) e OK na build consertada.
`guarda_save.py` depois do conserto: SAVE COMPATIVEL, 1939 mapas, SaveBlock1
14388 B.

**Efeito colateral esperado: o T93.3 quebrou, e foi reescrito.** O roteiro
antigo entrava pela porta da entrada e decorava o caminho de UMA sala sorteada
(a 81); o sorteio (`random` do motor de script) muda com qualquer mudança de
consumo de RNG da build, e o conserto das palettes mudou. O caso novo parte da
SALA DO PILAR por warp de debug (determinístico), margeia a parede pela linha
y=2 e coluna x=3 (livres em todas as plantas, conferido em `mapas-png`) e sai
pela porta oeste (2,11); a prova continua sendo o contador somando na sala
seguinte. Regra que fica: **roteiro de suíte não pode decorar resultado de
sorteio.**

**RISCO FECHADO em 15/08/2026, medido nas duas ROMs: não existe regressão.**
Entrar numa sala do Turnback por porta custa 58 quadros de input travado em
`0e4571bfd5` E em `25f3976336` (N=3 cada, variância zero, lido de
`sLockFieldControls` na EWRAM); porta não animada de Unova, 60 nas duas. O
">480 engolidos" era o jogador contra a parede: todo warp dinâmico chega em
(11,1), a coluna x=11 é bloqueada em y=8 nas plantas PILLAR_ROOM e ROOM_5 e
livre em ROOM_1/ROOM_3, e a sala é sorteada com semente de relógio
(`SeedRngAndSetTrainerId`, `src/main.c:215`, timers de hardware amostrados na
confirmação do nome). Regra que fica: caso de suíte que entra por porta no
Turnback PINA o sorteio com `"vars": {"0x41C0": 3}` ou `{"0x41C1": 29}`, como
T93.4/T93.5. Colaterais registrados: as "portas" do Turnback são metatile de
comportamento 97 (`MB_LADDER`), não 96 (`MB_NON_ANIMATED_DOOR`), então a
guarda de `Task_ExitNonAnimDoor` é inerte lá; e
`testa_critico.offsets_da_fonte()` grava `probe.c/probe.o` em caminho cravado
(`/tmp/claude-501/frenteA/offsets`), colisão esperando duas sessões paralelas.

### B8 FEITO em 12/08/2026, DEPOIS da janela de save fechar (leia isto primeiro)

A janela de save estava FECHADA quando este bloco rodou, e ele terminou com
`guarda_save.py` dizendo **SAVE COMPATIVEL**. Nada aqui mexeu em `FLAGS_COUNT`,
`VARS_COUNT`, `MAX_TRAINERS_COUNT`, tamanho de struct ou id de mapa; as duas
flags que a mecânica nova consome saíram do pool de `FLAG_UNUSED` que já existe.

| medida | antes | depois |
|---|---|---|
| ROM | 98,07% de 32 MB | **98,14%** (+23 KB, 601 KB livres) |
| EWRAM / IWRAM | 85,94% / 86,65% | **85,94% / 86,65%** (iguais) |
| SaveBlock1 | 14388 B | **14388 B** (igual) |
| mediana do selvagem, K/J/H/S/U | 25 / 20 / 27 / 27 / 30 | **20 / 65 / 122 / 166 / 217** |
| espécies de gen 6-9 no jogo | **0** | **365 de 365** |
| espécies-base alcançáveis | 745 | **927 de 1010** |

**O teto de 255 é viável, e a auditoria achou TRÊS defeitos reais que ele mesmo
criou** (detalhe e prova em `PRD-ROM-COMPLETA.md`, bloco B8): `u8 nextLevel` que
virava 0 e gravava **nível 0** no Pokémon do teto (`src/pokemon.c`); `s16
moveDamage` que enrolava para negativo acima de 32767 e **curava o alvo**
(`include/battle.h`), porque o termo de nível do dano sai de 42 para 104; e três
leituras `gExperienceTables[...][level + 1]` fora do array. **Nível não está em
save**: `struct BoxPokemon` não tem campo de nível, ele é derivado de
`experience:26` (folga de 21% no nível 255) e o `u8 level` de `struct Pokemon` é
cache, com 255 sendo exatamente o máximo do tipo.

**Defeito de flag que estava escondido há tempo**: `B_FLAG_DYNAMAX_BATTLE` e
`B_FLAG_TERA_ORB_CHARGED` apontavam para `FLAG_UNUSED_0x020` e `0x021`, que
neste repo são **apelido de `FLAG_HIDE_ARTICUNO` e `FLAG_HIDE_BILL_CLEFAIRY`**.
Começar o jogo escondia os dois NPCs de Kanto, e entrar nos mapas deles
desligava as duas mecânicas para sempre. Lição: **antes de usar qualquer
`FLAG_UNUSED_*` que o upstream sugere, rode `dev_scripts/flags_livres.py`** —
ele já separava "definidas" de "realmente livres" e as duas estavam na coluna
das 359 OCUPADAS.

### Build de fechamento de 12/08/2026: VERDE, suíte 210/211, ROM a 98,07%

A sessão de fechamento pegou a build verde de 197/211 e foi atrás dos 13
vermelhos. **Nenhum deles era falha de roteiro sozinha e nenhum era o que o
relatório anterior dizia que era**; os três defeitos abaixo estão medidos no
emulador, com a coordenada lida da EWRAM, e consertados.

| medida | valor |
|---|---|
| ROM | **98,07% de 32 MB** (32.136,4 KB mapeados de 32.768; **631 KB livres**) |
| EWRAM / IWRAM | 85,94% / 86,65% |
| SaveBlock1 | 14388 de 15872 B (**90,7%**) |
| mapas na ROM | 1939 |

Toolchain `~/toolchains/arm-gnu-toolchain-15.2*` passada em `DEVKITARM=`; o gcc
do brew continua sem buildar.

**ROM de entrega**: `roms/pokemon-claude-2026-08-12.gba`, com o `.map` do linker
ao lado (é dele que o `testa_critico.py` tira os símbolos). **A janela de save
foi FECHADA**: `guarda_save.py --gravar` rodou sobre essa ROM depois de a suíte
fechar, e antes disso a rodada sem `--gravar` acusou exatamente as 3 quebras
esperadas e nenhuma a mais (vars `0x40FF`→`0x41FF`, SaveBlock1 13432→14388 B,
impressão anterior aos macros).

### Defeito 1: a porta de Unova, e o que ela era DE VERDADE

**A causa registrada pelas duas sessões anteriores estava errada nas duas
direções, e as duas erravam por um.** O relatório disse
`MB_NON_ANIMATED_DOOR` com o número `0x5F`; a conferência do condutor corrigiu o
número para `0x60` e trocou o nome para `MB_LADDER`. Neste repo,
**`0x60` é `MB_NON_ANIMATED_DOOR`** e `MB_LADDER` é `0x61` (o próprio
`valida_warp_tile.py` já avisava disso no comentário da tabela `NOME`). Ou seja:
o nome do primeiro relatório estava certo, o número do segundo estava certo, e
a conclusão dos dois estava errada. **A varredura de 1060 warps de Unova é
`MB_NON_ANIMATED_DOOR` em 1000 e `MB_LADDER` em 60**, e não o contrário.

**Medição no emulador, T20.4, `Unova_NuvemaLab` (12x12, warps em (2,11) e
(3,11), última linha):** o jogador entra, e a EWRAM mostra ele em **(2,12)**,
fora da grade. Ali ele não anda para lado nenhum; o primeiro UP o devolve a
(2,11), que é a própria porta, e o warp dispara de novo: **ele é cuspido para a
rua toda vez que tenta entrar.** O motor separa isso exatamente onde a história
do empurrão precisava: `SetUpWarpExitTask` (`src/field_screen_effect.c`) manda
`MB_NON_ANIMATED_DOOR` para `Task_ExitNonAnimDoor`, que dá um passo para o sul
com **movimento segurado**, que ignora colisão e limite de mapa.

**Conserto, no motor e não no dado** (`src/field_screen_effect.c`): a porta não
animada só usa a saída com empurrão quando o tile de baixo dá para pisar. Fora
da grade o bloco vale `MAPGRID_UNDEFINED` e `MapGridGetCollisionAt` devolve
verdadeiro, então o mesmo teste cobre os dois casos. Varredura do repo inteiro
antes de escrever: **265 warps em 137 mapas** caíam fora da grade e outros
**187** caíam dentro de parede, todos de Unova menos 9 interiores de Sinnoh;
os **1106** warps sadios têm colisão 0 embaixo, então a guarda é inerte para
tudo que já funcionava. Isso é o oposto de reconverter 57 tilesets, que era o
conserto proposto.

**Um pedaço do defeito é de DADO mesmo, e esse foi cirúrgico.** Porta não
animada dispara ao ser PISADA, então quando ela é a única ligação entre a sala
de chegada e o resto do mapa, atravessá-la é sair do prédio. Foi o que o T92.6
provou na `Unova_PkmnLeagueMain`: (13,19) e (14,19) são o único caminho entre a
sala de chegada e o salão da Elite, e **depois de ganhar a Liga o salão ficava
inalcançável**, porque a cena de entrada que carrega o jogador para dentro é
pulada quando `FLAG_UNOVA_LIGA_VENCIDA` está acesa. Os dois metatiles viraram
`MB_SOUTH_ARROW_WARP` (`dev_scripts/porta_de_saida_unova.py`), e o
`applymovement` da cena caiu de seis para cinco passos, porque a seta não
empurra e a partida subiu um tile.

**O tamanho do resto está medido e escrito, para a próxima leva não remedir**
(`porta_de_saida_unova.py --censo`): de 470 metatiles de porta usados por warp
no repo, **196 (558 warps)** têm o tile do norte andável em TODOS os seus usos,
que é a assinatura de "porta por onde se sai andando para o sul" e são
candidatos legítimos a seta sul; os outros **274 (1000 warps)** têm pelo menos
um uso com o norte bloqueado, ou seja são porta de ENTRADA, e seta sul
quebraria a entrada deles. Os dois papéis convivem no MESMO tileset: em
`gTileset_UnovaPkmnLeague`, 683 são as quatro salas da Elite (entrada) e 786/788
são a escada de volta (saída). Virar os 196 de uma vez é trabalho de leva com
rebuild e suíte inteira em cima, não de fechamento.

### Defeito 2: o Lago Acuity não era soft-lock, era um par de mapas ILHADO

O relatório anterior dizia que quem entra pela frente cai na água e alcança 1
tile. A parte da água é verdade; a conclusão não. Medido no disco:
**ninguém chegava lá.** O warp do outro lado, `AcuityLakefront` (32,40), está
sobre `MB_SAND`, e `IsWarpMetatileBehavior` não dispara em areia. A fiação
inteira, antes:

    AcuityLakefront (32,40) MB_SAND         -> LakeAcuity warp 0     MORTO
    AcuityLakefront (32,39) porta           -> LakeAcuityLowWater    vivo
    LakeAcuity      (24,24) MB_POND_WATER   -> AcuityLakefront       MORTO
    LakeAcuity      (23,29) porta           -> AcuityCavern          vivo
    AcuityCavern    (16,21) seta sul        -> LakeAcuity warp 1     vivo

`{LakeAcuity, AcuityCavern}` era uma **ilha do grafo de mapas**, alcançável só
pelo menu de debug, que é o que o T94.5 usa. Conserto em
`dev_scripts/conserta_lago_acuity.py`, copiando o padrão do Lago Verity, que
funciona: (32,40) vira `MB_NORTH_ARROW_WARP` e o `warp 0` do lago sai da água e
vai para (24,31), na plataforma da boca da caverna, com `MB_SOUTH_ARROW_WARP`.
Não é (23,31) porque ali mora o template do RIVAL e em (22,31) o da JUPITER.

**E o conserto acordou um defeito de verdade, que é o melhor argumento de que
ele estava certo.** Com o mapa alcançável, o T94.6 (par negativo) reprovou:
`LakeAcuity_EventScript_Jupiter` só olhava `FLAG_GALACTICA_ACUITY_VISTO` e não
o marco da Mars, então quem chegasse na boca da caverna antes da hora via as
seis caixas de texto **com ninguém na tela** e ainda queimava a flag, trancando
a cena de verdade para sempre. Ganhou um `goto_if_not_defeated` no começo.
Enquanto o warp largava o jogador dentro do lago, esse caso passava por não
conseguir chegar no gatilho: passar por impossibilidade é o mesmo que não ter
teste.

**O que fica aberto no Acuity, de propósito**: a geometria. Medido contra
`fontes-mapas/pokeplatinum/res/field/events/events_lake_acuity.json`, a fonte
entra por quatro tiles no bordo sul, e na nossa conversão a praia sul (42 tiles)
não se liga à plataforma da caverna (25 tiles), porque virou água um caminho que
na fonte é terra. Consertar é reconverter o `blockdata` a partir da grade de
permissão do pokeplatinum. Enquanto isso a entrada cai direto na boca da
caverna: ninguém fica preso, e a cena roda. Efeito colateral aceito e medido:
`LakeAcuityLowWater` perde a única entrada a pé, e aquele mapa tem ZERO objetos,
ZERO coord_events, ZERO bg_events e um `scripts.inc` de duas linhas.

### Defeito 3: onze roteiros escritos contra um mapa que não existia mais

Os casos de Unova foram escritos antes de o B12 trocar os tilesets, quando a
última linha dos interiores era chão comum. Com a porta funcionando, os onze
tiveram que ser re-derivados por busca em largura no `map.bin`. As regras que
saíram disso valem para todo caso novo e **foram medidas, não deduzidas**:

- **O jogador chega VIRADO PARA O SUL** em porta não animada
  (`GetAdjustedInitialDirection`), então a primeira tecla de qualquer outra
  direção só VIRA. Contagem de passo sem contar a virada erra por um.
- **Depois de um warp de PORTA, os primeiros apertos se perdem.** Com 300
  quadros de espera o jogador ficava parado o roteiro inteiro no ginásio de
  Aspertia; com 600 ele anda. Warp do menu de debug não precisa disso.
- **Pausa entre pernas do caminho não é enfeite**: sem `90:NADA` entre elas, os
  apertos da perna seguinte se perdem e o jogador para no meio (T92.6).
- **Caixa de texto aberta come tecla de direção.** O T89.1 ficava parado em
  (13,14) porque a cena de entrada termina com uma mensagem; os A vêm ANTES do
  movimento agora. Isso só apareceu olhando o framebuffer.
- **Número de A é TETO, não piso** (T92.7): com 70 a cena termina na sala do
  Campeão, com 75 o duelo já começa, e com 90 o jogador perde de time vazio e
  acorda em Pallet Town.
- **A prova `andou` precisa de duas posições amostradas DENTRO do mapa final.**
  Cena que move o jogador inteira dentro de um passo do roteiro dá uma amostra
  só, e o caso reprova dizendo que o jogo não respondeu (T92.4).
- **Andar de lado de uma porta para a porta vizinha sai do prédio**, enquanto o
  tile for porta não animada. Todo caminho novo desvia da linha da porta.

### Consertos de integração além dos dois da build

- `2e03d4b561`: o Karate King do Mt. Mortar chamava `TRAINER_KIYO` (181), que é
  o Kiyo da Rota 132 de Hoenn: os dois dividiam a flag de derrotado, e o
  `TRAINER_JOHTO_KIYO` (2461) criado no mesmo dia não era citado por script
  nenhum. Varri a faixa 2460 a 2530: era o único órfão.
- `7593233e5a`: a tabela de treinadores do `testa_critico.py` lia
  `^#define TRAINER_... (\d+)\s*$` e não enxergava as **12** constantes com
  comentário no fim da linha (os quatro duelos do Silver e os oito líderes de
  Unova). O sintoma era o caso reprovar dizendo "treinador da prova não existe",
  que é mentira de validador (lição 4.3).

### Armadilhas de roteiro MEDIDAS (para quem escrever caso novo)

- **Virar custa UM aperto**, e a exceção que estava escrita aqui NÃO EXISTE
  mais. A anotação dizia que virar não custava no primeiro movimento depois do
  warp de debug; medido em 12/08/2026, custa: o jogador chega virado para a
  direção que `GetAdjustedInitialDirection` escolhe pelo comportamento do tile
  (sul em porta não animada, norte em seta sul), e qualquer outra direção gasta
  um aperto para virar. Perna que termina em PAREDE (ou no próprio NPC, que é
  sólido) não depende disso, e continua sendo a forma robusta de escrever.
- `N:BOTAO*K` **anda K tiles**: cada repetição é um aperto separado, com o botão
  solto entre elas. A anotação antiga que dizia o contrário está errada.
- ~~**Warp de debug para interior cuja porta está na última linha não serve**~~:
  serve desde 12/08/2026. O jogador nascia fora da grade porque a porta não
  animada empurrava ele um tile para o sul; a guarda em `SetUpWarpExitTask`
  acabou com isso e ele nasce no próprio tile do warp. Entrar pela cidade, com
  `warp_id` na porta, continua sendo o caminho mais fiel, e cobra ~600 quadros
  de espera antes do primeiro aperto.
- **Cena longa cobra muito mais A do que parece**: o rival de Canalave precisou
  de 10 apertos e a cena do teatro de 20. Seis não bastavam, e o sintoma era
  `oponente=0`, igual ao de roteiro que nem chegou no NPC.
- **Falha que não repete não é defeito**: o T85.3 reprovou na primeira rodada e
  passa sozinho, porque NPC anda por conta própria e pode fechar o corredor.
  Rode o caso duas vezes antes de acusar o jogo.

---

**A sessão de 12/08 executou quase o PRD inteiro por agentes, em 6 commits
(`98685da1d6` a `5127978487`), e PAROU AQUI por crédito. Os números abaixo
desta seção estão VELHOS (são de 11/08); o que vale é isto:**

**FEITO em 12/08** (detalhe em `PRD-ROM-COMPLETA.md`, que registra cada bloco):
B0 inventário; B3 (270 NPCs apagados); B7 (542 mapas com encontro: Kanto
estava 100% fora da build por sufixo `_FireRed`); B4 e B5 nas 5 regiões
(insígnias de Hoenn separadas de Kanto); B12 completo (57 tilesets do BW3G,
mediana de Unova 3→30, animações, ledges com paridade 40/40, +369 KB);
B1 a+b+c (44 mapas, Sinnoh 80,1%, Battle Frontier aberto, Turnback via
MAP_DYNAMIC); B2 (mudos encontráveis 192→63, 21 lojas da fonte, 109 Wi-Fi
escondidos); B6 parcial (espinha da Galáctica de ponta a ponta, Teatro de
Ecruteak, fim de Unova com Juniper campeã, 18 heal locations de Unova).
Infra na janela de save: +2048 flags, +256 vars, teto de treinador 4000,
teto de grupos 128→255, s16 em coordenada de warp.

**NÃO FEITO, na ordem para a próxima sessão:**
1. ~~**BUILD DO CONDUTOR NUNCA RODOU depois da leva.**~~ **FEITO**, e o
   resultado está na seção "Build de 12/08/2026" logo acima: build verde depois
   de dois consertos mecânicos, suíte em 197 de 211, e os 13 vermelhos são os
   três defeitos reais descritos lá (porta de Unova, Liga de Unova, elevação em
   Sinnoh), nenhum deles falha de roteiro.
2. ~~**A JANELA DE SAVE ESTÁ ABERTA E NÃO FOI FECHADA.**~~ **FECHADA** em
   12/08/2026 pela sessão de fechamento: `guarda_save.py --gravar` rodou sobre
   a ROM de entrega depois da suíte, e antes disso a rodada sem `--gravar`
   acusou só as 3 quebras esperadas. A impressão gravada agora inclui o campo
   `macros`, que é o que fechava o buraco de `FLAGS_COUNT`. Save feita nesta
   ROM vale daqui para a frente; save de build anterior a ela não vale.
3. ~~**B8 NÃO COMEÇOU**~~ **B8 FEITO** em 12/08/2026, e o placar está no
   primeiro bloco desta seção. Sobra dele uma decisão do Gui: 22 blocos de
   líder/E4/campeão com time cheio (6 Pokémon) ficaram só com Dynamax e sem
   lenda, e entre eles estão a Cynthia de Sinnoh e os campeões de Unova.
4. **B6 restante, REMEDIDO em 15/08/2026. A fila canônica é
   `dev_scripts/fila_b6.json`, regenerável por `dev_scripts/fila_b6.py`; os
   números antigos desta linha (193/104/348/176) estavam errados e a
   explicação de cada erro está no cabeçalho do script.** São **652 cenas
   pendentes**: Unova 209 (107 de changeblock em **12 mapas**, 1226 chamadas;
   47 setscene; os "16 callasm" são 16 coord_events de UM mapa,
   IcirrusCitySouth, sobre 4 callasm literais; 15 batalhas; 31 portáveis com
   bloqueio; 6 portáveis; 3 special), Sinnoh 430 (276 cenas de hidden_flag
   cobrindo 371 objetos; 164 gatilhos de coord_event, 177 no total; nenhuma
   var do Platinum existe aqui ainda; mais a biblioteca de Canalave, sem
   escopo escrito), Johto 13 (arco dos sinos BLOQUEADO por ITEM_TIDAL_BELL e
   ITEM_CLEAR_BELL inexistentes; 4 duelos de cena; 4º duelo do rival com
   slot pronto; RED_2 esperando decisão de arte do Gui). **Os 18 treinadores
   de torre/farol de Johto estão DESBLOQUEADOS**: a seção 4.1 do
   `PENDENCIAS-JOHTO.md` ficou velha, a faixa 2462-2499 (38 ids) está livre
   e o teto 4000 aguenta sem tocar em save.
5. **B10/corte**: ROM estava a ~97,8% ANTES da leva final de B6; a build
   da próxima sessão diz o número real. Economias mapeadas na seção 11 do
   PRD (ícones 673 KB, indireção de treinador 485 KB, overworld 330 KB).
6. Caso de emulador do guarda da Liga de Hoenn (pendência do B5, opção c).

**Regiões novas (gens 6-9)**: 4 sessões separadas rodando com escopo "tudo"
(dados + demake). Staging em `../fontes-mapas/<gen>/` (que virou repo git
LOCAL, com datamine sem licença: NUNCA ganhar remote público). A integração
ao hack é da sessão condutora, em levas. Teto de grupos já aguenta (255).

**Lições novas de 12/08 (valem regra):** quem escreveu não pode ser quem
confere (escrita silenciosamente falhada só apareceu em grep de processo
separado); agente NUNCA restaura a árvore inteira de snapshot (reverte só os
próprios arquivos; custou reverts de trabalho alheio); faixa exclusiva de
flag/var/id por agente paralelo funciona (0x1840/0x1900/0x1A00, vars 0x41xx,
ids 2460+/2500+/2520+, vagas anotadas em `opponents.h`).

---

## 1. O que o hack é

Cinco regiões num cartucho de GBA, em ordem cronológica:

**Kanto → Johto → Hoenn → Sinnoh → Unova**

Base: `pokeemerald-expansion`. Nada de mapa foi desenhado do zero; tudo veio de
fonte, convertido. As fontes ficam em `../fontes-mapas/`.

| região | fonte |
|---|---|
| Kanto | `pret/pokefirered` |
| Johto | `hns` (hack de pokeemerald) |
| Hoenn | `pret/pokeemerald`, intocado |
| Sinnoh | `fontes-mapas/sinnoh` (geometria), `pokeplatinum` (NPCs) |
| Unova | `AzureKeys/BW3G` (pokecrystal, gen 2) |

---

## 2. Números de agora

| medida | valor |
|---|---|
| ROM | **95,23% de 32 MB** (1,53 MB livres), medido na build de 11/08/2026. Era 94,67% de manhã: cresceu com os 50 itens escondidos, as 9 trocas de Unova, os 790 textos de Sinnoh e os 150 treinadores |
| EWRAM / IWRAM | 85,57% / 86,62% |
| SaveBlock1 | **13432 de 15872 B (84,6%)** |
| flags livres no pool | **40** (medido por `flags_livres.py` em 11/08/2026, depois de a última flag da faixa de itens escondidos ir para o PP UP da Rota 222: estava em 88, 46 foram para os itens escondidos de Sinnoh (`itens_escondidos_sinnoh.py`) e 1 para `FLAG_SINNOH_NPC_DUPLICADO`, que esconde o clone perdedor dos 382 pares de NPC repetido) |
| mapas | **1878** |
| treinadores com time próprio | **2346** |
| grupos de mapa | **126** (teto duro de **128** grupos e **128 mapas por grupo**: `s8` em `struct WarpData`; passar disso mata o mapa) |
| suíte de testes | **162 de 163** em 11/08/2026, rodada em worktree isolada sobre o HEAD mais a leva de tradução dos portos, dos itens escondidos e da escada de MtCoronet2F (eram 161 de 162 antes do caso T88, que prova essa escada). O único pulado é o T11.3, que precisa de duas builds. Uma rodada intermediária desta mesma leva deu **154 de 163, e os 9 reprovados eram exatamente os 9 casos que atravessam porto**: é a lição 4.13, `\l` cobrando aperto de botão que o verificador não contava. Os "2 reprovados de Unova" que esta linha já anunciou foram consertados em `44cae4fa02` uma hora depois de a linha ser escrita, e ninguém a corrigiu por seis dias |
| teto de treinador | `MAX_TRAINERS_COUNT_EMERALD` = **4000**, subido em 12/08/2026 dentro da janela de save aberta daquele dia (era 2500, e este documento chegou a dizer 3000). Maior id declarado: **2440**. Livres: **2441 a 3999, ou seja 1559**. Custou **~486 KB de ROM**, porque `gTrainers` e `sTrainerSlides` sao dimensionados pelo teto e nao pelo uso: ~324 bytes por vaga VAZIA. So da para mexer neste numero com a janela aberta |

### Completude contra a fonte de cada região

100% = tão completo quanto o jogo de onde a região veio. Rode
`python3 dev_scripts/completude.py`.

**Medição de 18/08/2026** (a tabela anterior, de 11/08, está logo abaixo marcada
como SUPERADA; nada foi apagado, porque duas investigações já foram reabertas
por causa de número velho lido como número de hoje):

| região | mapas | objetos | warps | placas | arte |
|---|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100,0% | 100,0% | 52 (0) |
| Johto | 95,9% | 95,2% | 100,0% | 96,0% | 55 (3) |
| Hoenn | 100,0% | 100,1% | 100,0% | 100,0% | 39 (22) |
| Sinnoh | **80,1%** | **60,2%** | 97,7% | 77,4% | 39 (**104**) |
| Unova | 94,2% | 99,5% | 99,3% | 98,0% | **30** (3) |
| **Galar** | 100,0% | 26,7% | 100,0% | 15,4% | 48 (32) |

A coluna **arte** é nova (18/08/2026) e não é completude contra a fonte: é a
mediana de metatiles distintos por mapa, e entre parênteses quantos mapas ficam
abaixo de 10. Ela existe porque a régua velha deixou uma região inteira passar
por "94% completa" durante seis dias; ver "A régua não enxergava arte" adiante.

| SUPERADA em 18/08/2026, medição de 11/08 | mapas | objetos | warps | placas |
|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100,0% | 100,0% |
| Johto | 95,9% | 94,0% | 100,0% | 96,0% |
| Hoenn | 100,0% | 100,1% | 100,0% | 100,0% |
| Sinnoh | 72,7% | 77,2% | 99,2% | 81,2% |
| Unova | 94,2% | 98,5% | 98,9% | 98,0% |

**A linha de Sinnoh mudou muito e NADA disso é regressão.** Mapas subiram de
72,7% para 80,1% porque o bloco B1 pôs 44 mapas de Sinnoh na ROM. Os mesmos 44
mapas derrubaram a coluna de objetos, e é aritmética de denominador: eles
trazem 564 objetos da fonte contra 63 nossos, o que sozinho custa cerca de 12
pontos. A outra metade da queda é deliberada: o B3 apagou 270 NPCs inventados
(censo em `dev_scripts/limpa_clones_sinnoh.py`). Medido no MESMO conjunto de 432
mapas dos dois lados, a queda honesta é de 77,2% para 71,1% (1963 para 1808 de
2542), e o resto é o denominador novo. A obra de 17-18/08 só SUBIU o número
(57,7% para 60,2%), e entre `d9dbdea770` e o HEAD **zero** mapas de Sinnoh
perderam objeto, medido mapa a mapa nos 476 casados. O buraco de verdade são
**1235 objetos que a fonte tem em mapas que entraram vazios** (`BattleFrontier`
0 de 25, `StarkMountainRoom1` 0 de 17, `AmitySquare` 0 de 16, as sete salas de
`TurnbackCave*`, `Route204North`, `MtCoronetOutside*`, `RotomsRoom`,
`LakeVerityLowWater`): eles nunca tiveram gente, não perderam. **Uma frente de
povoamento está mexendo nesses mapas AGORA**, então a coluna de objetos de
Sinnoh vai subir de novo e este número é datado de 18/08/2026. O
`completude.py` foi auditado nesta data e **não** tem defeito de régua aqui.

#### A régua não enxergava arte, e por isso Unova passou seis dias mentindo

`completude.py` contava PRESENÇA de mapa, objeto, warp e placa e **nunca abria o
`blockdata`**, então caixa vazia com as portas e os NPCs certos passava com 98%.
O Gui olhou o jogo e desconfiou em 12/08/2026; a medição deu razão a ele. Desde
18/08/2026 a régua abre o `blockdata`: é a coluna **arte** da tabela acima, e o
conserto de régua é o que faltava para este erro não se repetir em outra região.

Metatiles distintos por mapa, **medição de 18/08/2026**:

| região | mediana | máximo | mapas abaixo de 10 |
|---|---|---|---|
| Kanto | 52 | 319 | 0 |
| Johto | 55 | 437 | 3 |
| Hoenn | 39 | 545 | 22 |
| Sinnoh | 39 | 303 | **104** |
| Unova | **30** | **283** | **3** |
| Galar | 48 | 401 | 32 |

| SUPERADA em 18/08/2026, medição de 12/08 | mediana | máximo | mapas com 3 ou menos |
|---|---|---|---|
| Kanto | 52 | 319 | 0 |
| Hoenn | 39 | 545 | 11 |
| Sinnoh | 39 | 303 | 0 |
| Unova | 3 | 5 | 155 de 291 |

**O parágrafo abaixo é a descrição do defeito, e ele está CONSERTADO. SUPERADO
em 18/08/2026, mantido porque explica a causa:** "Máximo 5 em 291 mapas: Unova é
máscara de colisão em duas cores, chão e parede mais o metatile de porta. E não
tem um tileset próprio sequer: os 291 mapas usam tileset de Hoenn e de Sinnoh
(138 em `Building + GenericBuilding`, 75 exteriores em `GeneralSinnoh +
PetalburgSinnoh`, 32 em `CaveSinnoh`). A conversão leu o `.ablk` certo
(`AspertiaCity.ablk`, 308 bytes = 14x22 blocos de gen 2 = os 28x44 metatiles do
nosso layout) e parou na tradução de bloco para metatile."

**O que Unova é HOJE, medido em 18/08/2026:** 291 mapas, **todos** com tileset
secundário próprio de Unova (46 tilesets do BW3G convertidos, registrados em
`include/tilesets.h` e todos com mapa; os outros 11 do BW3G são de Johto, de
Kanto e das salas de palavra das Ruins of Alph, que nenhum mapa nosso usa). O
primário continua sendo `Building` (184 mapas) ou `GeneralSinnoh` (107), e isso
é **de projeto**: o tileset do BW3G cabe inteiro no slot SECUNDÁRIO do GBA, e
gastar o primário seria pagar duas vezes pelo mesmo desenho. Mediana 30,
máximo 283 (`Unova_VillageBridge`), mínimo 4, **zero** mapas com 3 ou menos. Os
3 mapas abaixo de 10 são **fiéis à fonte**, conferido byte a byte:
`CasteliaPlazaElevator` e `VirbankComplexElevator` (4 metatiles; os dois
compartilham `DeptStoreElevator.ablk`, que tem 4 bytes e 4 blocos distintos) e
`FloccesyRanchBarn` (9; `Route39Barn.ablk`, 16 bytes e 8 blocos). Quem entrou:
o commit **`72820a01db`** (12/08/2026), pelos geradores
`dev_scripts/tileset_gen2.py` (tileset) e `dev_scripts/blockdata_unova.py`
(blockdata), os dois com `--demo` verde em 18/08/2026 e prova de fidelidade
pixel a pixel com mutação plantada. Rodar `blockdata_unova.py --arte-propria`
sem `--gravar` hoje devolve "antes" idêntico a "depois" nas quatro métricas: a
conversão é idempotente e a arte da árvore é a que o gerador produz.

O que **está** pronto em Unova, e é por isso que a região não é lixo: 1396 NPCs,
1060 warps, 497 placas, 6234 linhas de texto de verdade do BW3G, 360 treinadores
únicos todos com time, 87 mapas com encontro selvagem, e as dimensões exatas da
fonte. **Superado em 18/08: a frase "conteúdo cheio com arte zerada, o inverso
de Sinnoh" valeu até 12/08 e hoje está errada.** Unova é a região mais completa
depois de Kanto e Hoenn; o que sobra dela é conteúdo (as 209 cenas da fila
`fila_b6.json` e os 67 NPCs em tile bloqueado, medidos por
`blockdata_unova.py --medir`, item (d)), não arte.

**A coluna de arte já achou serviço nas outras regiões, e isso é o ponto dela:**
Sinnoh tem **104** mapas abaixo de 10, entre eles SETE ginásios (o de Hearthome
com 4 metatiles, e Canalave, Eterna, Pastoria, Snowpoint, Sunyshore e Veilstone
com 5), que são caixa vazia com piso e parede; Galar tem 32, sendo **11 com UM
único metatile** (`Galar_Postwick23`, `Galar_WildArea16` e irmãos). Nenhum dos
dois foi investigado nesta rodada: ficam anotados aqui como fila.

Detalhe de régua, para o número bater quando alguém repetir a medição: a linha de
Sinnoh é medida sobre os 477 mapas de `nossos_mapas_sinnoh()` (a mesma lista que
o resto da linha dela usa), e as outras regiões sobre a lista de grupo. Galar não
tem lista de grupo que preste e sai do censo `galar_mundo.json`; ver o comentário
em `REGIOES` do `completude.py`.

**As placas de Sinnoh caíram de 94,4% para 82,3% em 11/08/2026, e isso NÃO é
regressão.** Medido antes e depois com `completude.py`, na mesma árvore. As 146
bg_events que sumiram nunca foram placa: eram item escondido do Platinum que o
importador copiou como placa (ver o item 3 da seção 8). Cinquenta viraram item
escondido de verdade e 96 foram apagadas. Quem contar placa vai achar que
perdemos conteúdo; o que perdemos foi mentira, e a régua é que continua contando
item escondido da fonte como se fosse placa.

**Sinnoh subiu de 72,4% para 72,7% dos mapas em 11/08/2026 sem um mapa novo, e
isso é régua outra vez.** `importa_npcs_sinnoh.NAO_TOCAR` é uma trava de
ESCRITA ("mapa que outro agente está editando"), e ela estava sendo descontada
dentro de `nossos_mapas_sinnoh()`, que é a régua do `completude.py`:
`CanalaveCity_Gym` e `SandgemTown_House1` estão na ROM e no `map_groups.json` e
mesmo assim contavam como ausentes. É o mesmo defeito de medida que segurava as
seis salas da Elite dos Quatro por causa do nome, e a diferença é que aqui não
era o nome, era a lista de quem não pode ser escrito. As duas coisas foram
separadas: `nossos_mapas_sinnoh()` mede e `mapas_editaveis_sinnoh()` escreve,
e os cinco chamadores foram divididos entre as duas conforme o que cada um faz.
`SandgemTown_House1` ganhou apelido (`MAP_HEADER_SANDGEM_TOWN_HOUSE`) porque o
`1` no fim do nosso nome não casa sozinho, e as duas entradas que só existiam
para tapar o buraco saíram de `fecha_portas_sinnoh.JA_TEMOS`.

**A escada de `MtCoronet2F` em (7,23) apontava para si mesma, e o preço era o
3F inteiro.** Consertado em 11/08/2026. No Platinum ela é metade de um par
(warps 2 e 3 de `mt_coronet_2f`); a conversão trouxe só um lado, e o outro,
(7,12), ficou como chão comum. Medido na grade: as linhas 13 a 22 do mapa são
parede maciça de ponta a ponta, então esse par é o **único** caminho entre a
sala do sul, que vem do 1F, e a metade norte, onde fica a escada para o 3F. Com
o warp morto, `MtCoronet3F` era inalcançável a pé. **Nada foi renumerado**,
porque a save do Gui já está congelada: o degrau que faltava entrou como warp 3,
no FIM da lista, o warp 1 passou a apontar para ele, e o tile (7,12) recebeu a
palavra 0x323F **copiada do próprio (7,23) deste mapa** (metatile 575,
`MB_LADDER`), em cima de chão andável que já existia. Prova no emulador em
`T88.1`, e a contraprova é de graça: o mesmo caso rodado na ROM anterior ao
conserto para em `MAP_MT_CORONET_2F`.

Mudou em 06/08/2026, na sétima leva do dia: **Sinnoh foi de 69,5% para 72,1%
dos mapas**, com 15 mapas novos, e desta vez **nada é régua**: são 12 masmorras
com a geometria CONVERTIDA de verdade e 3 exteriores de planta REAPROVEITADA.
Objetos e placas caíram em porcentagem porque o denominador cresceu: os mapas
novos entram contando os NPCs e as placas que o Platinum tem neles.

A fila de `converte_cavernas_sinnoh.py` dava **zero** e não era falta de
masmorra: Turnback Cave, Iron Island e Stark Mountain já convertiam, e o que
faltava era o mapa **DE FORA** por onde se entra em cada uma, porque o conversor
só cria masmorra que é destino de warp de um mapa que já está na ROM. Exterior
de gen 4 tem cenário DESENHADO que a grade 2D não guarda, e convertê-lo com o
motor de caverna encheria a rua de parede de pedra; então os três exteriores
saíram por `dev_scripts/abre_exteriores_sinnoh.py`, com a planta da antecâmara
`Route226_Access` que o repo já tem (13x9). Cada `map.json` grava isso no campo
`origem`, com a palavra "passagem provisoria".

- **Convertido de verdade (12):** Turnback Cave Entrance; Iron Island 1F, B1F
  Left, B1F Right, B2F Left, B2F Right, B3F, Iron Island Iron Ruins e Iron
  Ruins (o Platinum tem os dois headers, matrizes 283 e 284, e o B3F leva aos
  dois); Stark Mountain Room 1, 2 e 3.
- **Reaproveitado (3):** Sendoff Spring (entra por Route214), Iron Island (por
  CanalaveCity) e Stark Mountain Outside (por Route227). Sem NPC, sem placa e
  sem texto de propósito: coordenada de exterior no Platinum é GLOBAL da matriz
  de Sinnoh e não há offset que alinhe, então NPC importado cairia em qualquer
  lugar dentro de uma sala de 13x9.
- **Régua: nada.** Nenhuma medida mudou nesta leva.

**As 21 salas de pilar da Turnback Cave não vêm, e isso não é defeito de
ferramenta.** Medido na fonte: no Platinum toda sala de pilar aponta só de volta
para a Entrance, e a Entrance aponta para si mesma. Qual sala se entra é
escolhido por SCRIPT, não por warp, então não há warp estático que crie nenhuma
delas. Elas custam o script de sorteio de sala, não conversão de mapa.

**O bug que este bloco quase repetiu, e a prova que o pegou:** a primeira versão
do `abre_exteriores_sinnoh.py` cravou a volta ao mundo em (6,4), que é onde a
`Route226_Access` original tem o warp dela. Medido depois de aplicar: aquele
tile é `MB_NORMAL`, warp MORTO que nunca disparou (a saída de lá é scriptada
pelo marinheiro). Os três exteriores nasceram com entrada boa e **sem saída**,
com validador estático verde: dava para entrar na masmorra e não dava para
voltar ao mundo, que é a lição 4.1 outra vez. Agora a volta sai de
`fecha_portas_sinnoh.portas_livres`, que lê o comportamento do tile no `map.bin`,
e o `--demo` exige duas portas na planta: uma para voltar, pelo menos uma para a
masmorra. Casos `T85.1` a `T85.8` provam no emulador as três idas, duas voltas
de masmorra e as três voltas ao mundo.

Armadilha de roteiro de teste medida aqui: `16:DOWN*3` **não** é o mesmo que
`16:DOWN,16:DOWN,16:DOWN`. O `*N` do `gba_runner` repete os quadros dentro do
mesmo passo, e a seta de warp (`TryArrowWarp`) só dispara com
`input->heldDirection` e o jogador já virado para o lado
(`src/field_control_avatar.c:204`). Roteiro que só soma tecla falha calado.

Nenhuma flag foi gasta (a faixa 0x8EA a 0x8FF continua intacta) e **nenhum grupo
novo foi criado**: seguem 126 dos 128.

Mudou em 06/08/2026, na sexta leva do dia: **Sinnoh foi de 66,7% para 69,5% dos
mapas e a taxa de warp que dispara de verdade foi de 95,8% para 97,0%**, com
oito mapas novos e, de novo, NENHUMA ferramenta nova. Pela terceira leva
seguida, o que travava era **regua errada dentro da ferramenta certa**.

- `converte_cavernas_sinnoh.chao_de_caverna` contava so
  `TILE_BEHAVIOR_CAVE_FLOOR` (0x08). Vizinhos dele no MESMO enum do pokeplatinum
  (`include/constants/field/map_tile_behaviors.h`) sao `OLD_CHATEAU_FLOOR`
  (0x0B) e `MOUNTAIN_FLOOR` (0x0C). Por isso os cinco andares da **Lost Tower da
  Route 209** (84 a 123 tiles de 0x0B cada) e a quinta sala do fundo do **Old
  Chateau** eram reprovados como "nao e caverna de verdade", com a planta
  inteira desenhada na grade do Platinum. O filtro por `mapType` errava dos dois
  lados no mesmo lugar: FLOAROMA_MEADOW esta marcado CAVE e e um prado, a Lost
  Tower esta marcada INDOORS e e masmorra. Quem decide agora e o chao na grade;
  so `MAP_TYPE_OUTDOORS` fica de fora, por decisao. Casa, ginasio de Hearthome,
  Vista Lighthouse, Celestic Cave e a sala de ranking da Jubilife TV continuam
  fora, todos com ZERO chao de masmorra, e sao eles que provam que abrir para
  INDOORS nao abriu a porteira.
- **Achado maior que a propria leva:** o conversor cravava `dest_warp_id` "0" em
  toda escada, porque no laco que escreve o mapa do outro lado ainda nao existe.
  So que o warp 0 de uma masmorra e a SAIDA dela: **descer um andar cuspia o
  jogador para fora do dungeon inteiro**, e eram **69 escadas assim**, incluindo
  a Victory Road de Sinnoh, que jogava o jogador na porta da Liga. Isso passou
  pela leva anterior com validador estatico verde: warp que existe, dispara, e
  leva ao lugar errado (licao 4.1 por inteiro). `casa_voltas()` aponta cada uma
  para o degrau que devolve, e o caso `T84.3` guarda a prova.
- Nove mapas que **ja estavam na ROM** sairam da lista de ausentes so por
  apelido de nome (`importa_npcs_sinnoh.APELIDOS`), entre eles as **seis salas
  da Elite dos Quatro de Sinnoh**, que aqui se chamam `SinnohLeague_*` e la
  `POKEMON_LEAGUE_*`. Isso e correcao de MEDIDA, nao mapa novo, e esta separado
  de proposito: dos 2,8 pontos da leva, 1,5 e regua e 1,3 e mapa.

O que a regua nova alcancou e **nao entrou**: as quatro salas de elevador da
Liga. Abri-las fura a parede das cinco salas da Elite dos Quatro para um quarto
que devolve o jogador de onde ele veio, e a Elite ja se liga sala a sala com o
bloqueio de vitoria. `abre_portas_extras_sinnoh.NAO_FURAR` registra o motivo.

Tres `--demo` guardavam copia de um fato e envelheceram calados, todos
reprovando o proprio conserto da leva anterior (licao 4.11): "CanalaveCity tem 4
predios sem porta" (as quatro portas foram abertas), "os 15 mapas do layout de
centro Pokemon" (sao 14) e "o predio da Galactica divide layout" (foi clonado).
Passaram a testar a forma, nao a contagem. **O portao nao roda `--demo` de
ferramenta**, e foi por isso que os tres ficaram vermelhos sem ninguem ver.

Armadilha de roteiro medida escrevendo o `T84.2`, que contradiz a da leva
anterior e vale mais que ela: **depois de um warp pelo menu de debug o jogador
NAO gasta tecla para virar**, cada toque anda um tile. "Virar custa uma tecla"
vale para quem ja estava andando no mapa.

Mudou em 06/08/2026, na quarta e na quinta leva do dia: **Sinnoh foi de 59,3%
para 66,7% dos mapas e de 96,9% para 99,0% dos warps**, com 44 mapas novos e
NENHUMA ferramenta nova. As duas levas cairam pelo mesmo motivo, e ele nao era
falta de ferramenta: era **regua errada dentro da ferramenta certa**.

- 30 salas de predio (estudios da Jubilife TV, salas dos ginasios de Hearthome e
  de Sunyshore, andares da loja de Veilstone, biblioteca de Canalave 2F e 3F,
  Global Terminal 2F e 3F, elevadores, o restaurante do Lago Valor) eram destino
  de warp de mapa que ja estava na ROM, e `fecha_portas_sinnoh.arquetipo_do_header`
  devolvia `None` para todas elas. So a tabela `NOMEADOS` cresceu, e a cadeia
  inteira veio junto, rodada em laco ate parar de render.
- 14 mapas de geometria CONVERTIDA: a Victory Road de Sinnoh (1F, 2F e B1F) e as
  11 salas sem saida das Solaceon Ruins. A Victory Road ficava de fora so por
  colisao de nome, porque `MAP_VICTORY_ROAD_1F` e `LAYOUT_VICTORY_ROAD_1F` ja sao
  de HOENN; entrou com prefixo de regiao e o par vai em `I.APELIDOS`. As 11 salas
  eram reprovadas por "menos de 30 tiles andaveis nao e caverna", regra que mede
  o TAMANHO da sala: sao camaras de 10 a 13 tiles de verdade. A regra agora conta
  `TILE_BEHAVIOR_CAVE_FLOOR`, e Floaroma Meadow (zero) continua de fora.

Dois warps mortos apareceram no caminho e foram consertados: `fecha_portas_sinnoh`
escrevia direto num grupo que ja estava com os 128 do teto (o mapa 129 nasceria
morto, o defeito que matou 26 mapas), e os dois guardas de insignia da entrada da
Liga estavam parados EXATAMENTE nos dois tiles por onde se entra nas duas portas
do norte, o que deixava a porta do centro Pokemon norte fechada desde sempre.
Prova a pe no emulador em `T80.1` a `T80.5` e `T81.1` a `T81.4`.

Duas armadilhas de roteiro de teste, medidas escrevendo esses casos: **virar
custa uma tecla** (roteiro com a distancia exata erra um tile a cada troca de
direcao) e **porta `MB_ANIMATED_DOOR` so dispara com o jogador vindo de BAIXO**.

**A Elite dos Quatro de Sinnoh e a Cynthia já estavam na ROM** desde `20ac2eaac4`
(04/08/2026), e o que faltava era prova de combate: os casos `T9.9` a `T9.14`
provavam que as sete salas carregam, e nenhum provava que a batalha começa contra
quem devia. Fechado em 06/08/2026 com `T82.1` a `T82.5`, um por membro, todos por
**faixa** de id (1258 a 1262) e nunca pelo nome da constante. Os cinco blocos de
`trainers.party` são times do Platinum, dentro da curva de Sinnoh: Aaron 188-192,
Bertha 188-194, Flint 190-196, Lucian 192-198, Cynthia 196-200. Sprite de
overworld dos cinco é **provisório**, emprestado de classe parecida
(Aaron `BUG_CATCHER`, Bertha `EXPERT_F`, Flint `MANIAC`, Lucian `PSYCHIC_M`,
Cynthia `BEAUTY`); nenhum é sprite próprio de Sinnoh, e todos existem em
`object_event_graphics_info_pointers.h`.

Mudou em 06/08/2026, mais tarde no mesmo dia: **grupo de mapa tem teto de 128**,
e 26 mapas de Sinnoh estavam MORTOS por causa dele. `struct WarpData` guarda
`s8 mapGroup` e `s8 mapNum` (`include/global.h`): o mapa de indice 128 vira -128
no warp e o jogo reseta ao entrar. Medido no emulador, indice a indice. O grupo
de portas foi partido em dois, `fecha_portas_sinnoh.grupo_com_vaga` passa a
escolher o grupo sozinha e `antes_de_empurrar.sh` recusa grupo estourado. **Sobram
2 grupos dos 128**: regiao nova precisa caber neles. Com o teto respeitado
entraram as 36 cavernas com boca desenhada (`abre_bocas_cavernas_sinnoh.py`) e as
11 portas teimosas (`abre_portas_teimosas_sinnoh.py`, com clone de layout onde a
planta e compartilhada), e **Sinnoh foi de 51,0% para 59,3% dos mapas**. Detalhe
nas secoes 11 e 12 de `PENDENCIAS-NPC-SINNOH.md`.

Mudou em 06/08/2026: **Sinnoh saiu de 25,6% para 51,0% dos mapas e de 61,8%
para 95,4% dos warps**, em tres levas. A primeira reaproveitou planta de
interior do repo e fechou 112 portas de cidade; a segunda desenhou a porta que
faltava, copiando a palavra de 16 bits de um warp do proprio mapa, e abriu mais
28 interiores, entre eles os 18 `POKECENTER_B1F`; a terceira converteu a
geometria DE VERDADE de 10 cavernas a partir da grade 2D do Platinum
(`converte_cavernas_sinnoh.py`), incluindo Wayward Cave 1F inteira em 96x64. A
taxa de warp de Sinnoh que dispara de verdade foi de 86,0% para **95,8%**.
Detalhe nas secoes 8, 9 e 10 de `PENDENCIAS-NPC-SINNOH.md`.

Mudou em 05/08/2026, mais tarde no mesmo dia: o **S.S. Aqua entrou na ROM**, os
11 mapas do navio importados do `hns` com texto, NPC e os 23 treinadores de
bordo, e Johto foi de 91,4% para 95,9% de mapas. A travessia Olivine ↔ Vermilion
deixou de ser teleporte e passa **por dentro do navio** nos dois sentidos (T4.2 e
T10.3), com a caminhada e as cabines provadas no T10.4.

Mudou em 05/08/2026: as placas de Johto saíram de 6,8% para 96,0% (448 placas
importadas do `hns` com script e texto), e Unova saiu de 85,4% para 94,2% de
mapas **sem um byte novo**, porque o buraco era o normalizador de nome: no BW3G
a rota é `R5NimbasaGate` e aqui ela entrou como `Rt5NimbasaGate`.

Hoenn dando exatamente 100% é o **controle**: nossa Hoenn é o vanilla intocado,
então tem que dar 100. Se der outra coisa, a ferramenta está errada.

Sinnoh caiu de "100% / fonte 0" para estes números em 05/08/2026, e **isso é
bom**: a régua mudou, não o jogo. Antes era medida contra `fontes-mapas/sinnoh`,
que tem os mapas mas ZERO NPC de Sinnoh. Agora é contra o `pokeplatinum`, que
cobre muito mais mapa do que importamos. Os objetos foram de 528 para **1119**
de verdade; o 25,6% de 05/08 é a medida honesta aparecendo pela primeira vez, e
o 51,0% de hoje é ela subindo com mapa novo, não com régua nova.

### Warps que disparam de verdade

`python3 dev_scripts/valida_warp_tile.py --piso 60`

| Hoenn | Johto | Sinnoh | Unova | Kanto |
|---|---|---|---|---|
| 93,2% | 91,2% | 97,1% | 78,6% | 79,4% |

**Nunca chega a 100%, e não deve.** Warp só dispara se o tile embaixo tiver
comportamento de porta; muita porta é trocada por `setmetatile` em tempo de
execução, e muito warp é usado só por barco ou cutscene. Hoenn é a régua.

Kanto subiu de 69,9% para 79,4% em 05/08/2026 **sem tocar em mapa nenhum**: a
ferramenta é que não conhecia as quatro escadas diagonais (`MB_UP_LEFT_STAIR_WARP`
e irmãs, 235 a 238), que ligam os andares do esconderijo Rocket, do Silph Co e da
Mansão de Cinnabar. Elas não passam por `IsWarpMetatileBehavior`: disparam por
`TryArrowWarp` (`src/field_control_avatar.c:955`). O caso T15.3 prova no emulador
que a escada funciona, então a régua nova é o jogo, não a minha leitura dele.

Os 20,6% que sobram em Kanto **não são defeito, e não devem ser consertados**:
saída de prédio no FireRed tem três tiles de largura, e só o do meio carrega
`MB_SOUTH_ARROW_WARP`; os dois das pontas são entrada de warp redundante em cima
de `MB_NORMAL`. Medido em `PewterCity_Museum_1F` (warps 0, 1 e 2 em (13,9),
(14,9) e (15,9)), em `PowerPlant` e em `PokemonMansion_1F`. Quem "consertar" isso
está mexendo no vanilla.

---

## 3. Decisões já tomadas pelo Gui

Não relitigar. Números são das perguntas numeradas da sessão.

| # | decisão |
|---|---|
| 66 | Começa em **Pallet Town**, ordem cronológica Kanto, Johto, Hoenn, Sinnoh, Unova |
| 67 | **Cynthia fecha Sinnoh, Alder fecha Unova** |
| 68 | **Cada região entrega seu trio de iniciais** ao chegar |
| 69 | **Portar** o texto do BW3G, não escrever enredo novo |
| 70 | **Só creditar** Azure_Keys e os artistas, não contatar |
| 71 | **Nível vai até 255**, não 100. O trabalho de expansão já existia |
| 73 | Importar os treinadores de rota de Johto do `hns` |
| 13 | ~~As 152 "placas" de Sinnoh que na verdade são item escondido **ficam como estão**~~. **Revogada em 11/08/2026 pelo Gui**: as 146 (contagem certa) foram resolvidas. 50 viraram item escondido de verdade, custando 46 flags, e 96 foram apagadas |
| 14 | **Primeiro a ROM na mão do Gui**, ele joga a primeira hora; só depois atacar os 455 mapas de Sinnoh que faltam |
| 2 (15/08/2026) | **Polir times de líder/E4/campeão fica pro FIM do desenvolvimento**, quando todos os assets estiverem validados. Os 22 blocos de time cheio que o B8 deixou sem lenda ficam como estão até lá; nenhuma sessão deve "melhorar" time de líder antes dessa etapa |
| 3 (15/08/2026) | **RED do Mt. Silver REUSA a arte do jogador RED com palette própria** (novo OBJ_EVENT_GFX, sem esperar sprite dedicado). Destrava o duelo RED_2 de Johto |

**A janela de quebrar save FECHOU em 05/08/2026**, com a entrega de
`roms/pokemon-claude-2026-08-05.gba` (commit `d9e5e7581e`). A partir daqui existe
partida do Gui para proteger: mapa novo só no fim do grupo, grupo novo só no fim
de `group_order`, objeto novo só no fim da lista do mapa, flag nova só do pool
que já cabe em `FLAGS_COUNT`, struct de save só recebe append. O `T11.3` foi
provado nessa build: save feita na ROM anterior carrega na recompilada.

**Curva de nível aplicada**, remapeamento linear preservando a forma de cada jogo:

| Kanto | Johto | Hoenn | Sinnoh | Unova |
|---|---|---|---|---|
| 3-50 | 45-100 | 95-150 | 145-200 | 195-255 |

~~**Galar fica fora desta ROM.**~~ **SUPERADO em 18/08/2026**: Galar entrou como
sexta região (seção 0.f), com 438 mapas de geometria e conteúdo nenhum. Ela
ainda **não tem faixa de nível**, porque não tem encontro nem treinador; quando
tiver, a faixa entra nesta tabela. Ver `RECURSOS-REGIOES.md`.

---

## 4. As lições que custaram caro

Todas foram pagas com sessão perdida. Não repetir.

### 4.1 Verificar na camada da afirmação

O fio que liga quase todo bug grave desta sessão. Em cada caso a ferramenta
dizia verde:

- **Kanto tinha 421 mapas no JSON e zero na ROM.** Oito camadas a descartavam em
  silêncio, e a pior gravava `.4byte NULL` na posição do layout, mantendo os
  índices alinhados.
- **Johto tinha 771 warps com índice válido e 12 que disparavam.**
- **Kanto tinha 624 nomes de treinador e 623 sem time**, caindo em cima de
  treinadores de Hoenn. O ginásio de Pewter entregava um montanhista.

"O mapa está no JSON" não é "o mapa está na ROM". "O warp existe" não é "o warp
funciona". "Carrega" não é "funciona".

### 4.2 Ferramenta que discorda do vanilla está errada

Três validadores meus acusaram mapas **originais do Emerald** antes de acertar.
Quando a medida diverge do jogo original, o suspeito é a medida.

### 4.3 Falso positivo é pior que validador nenhum

Portão que não pode ficar verde ensina todo mundo a ignorar a saída. Antes de
pôr regra no portão, meça o vanilla e calibre pelo excesso sobre ele.

Exemplo: a regra "todo warp tem que voltar" acusou 427 casos aqui e o vanilla
tem a mesma taxa (25,3 por 100 mapas contra 26,4). A regra útil é a estreita:
**interior com uma porta só tem que devolver para si mesmo**, que dá zero nos
dois lados e teria pego o bug dos 6 ginásios.

### 4.4 Medir antes de racionar

Eu mandei três frentes racionarem treinador porque "só havia 24 bytes de save".
Medindo o SaveBlock1 campo a campo, `secretBases[20]` ocupava **3200 bytes**
para uma feature de troca por link. Cortada para 4: 2560 bytes, 20.480 flags.

Ainda sobram `berryTrees` (1024 B) e os campos de concurso (736 B).

### 4.5 Constante existir não é o jogo desenhar

Sprite, flag e treinador têm a mesma armadilha: a constante existe, o dado não.

- **Sprite** sem gráfico **reinicia o jogo na tela de título**, sem erro de
  compilação. A lista do que a build desenha sai de
  `object_event_graphics_info_pointers.h`, não de `event_objects.h`.
- **Flag** ocupada continua existindo como `FLAG_UNUSED_0x030`; o que muda é
  alguém apelidar ela. `grep -c FLAG_UNUSED` conta o pool, não o dono. Use
  `dev_scripts/flags_livres.py`.
- **Treinador** sem bloco `=== TRAINER_X ===` cai em cima de quem já ocupa o id.

### 4.6 Prova por identidade não vale quando o apelido devolve a si mesmo

"O oponente é `TRAINER_CAMPER_LIAM`" era verdade com o jogo quebrado. A prova
correta é por **faixa** de id.

### 4.7 Dado corrompido varia, endereço errado não

`mapLayoutId` saindo 26651 **igual em todos** os 41 grupos de Kanto foi a pista
que entregou o caso. Valor absurdo idêntico em todo lugar aponta para busca no
endereço errado, não para dado ruim.

### 4.8 `git add -A` numa árvore com agentes escrevendo captura um instante

Quebrei o `master` duas vezes assim. Buildar antes de commitar não basta: o
build é de outro instante. Rode `dev_scripts/antes_de_empurrar.sh`, que builda o
HEAD numa **worktree isolada**.

A primeira versão desse script usava `git stash`, e **destruiu trabalho de
agente**: o stash de um levou os arquivos de outro.

### 4.9 Substring casa onde você não quer

Comparar `"VENT"` contra o nome inteiro do gráfico casa com
`OBJ_EVENT_GFX_ACE_TRAINER_F`, porque tem *e-VENT-o* dentro. Isso jogou **806
NPCs fora sem erro nenhum**, e só apareceu porque o total deu zero. Tire o
prefixo antes de comparar classe.

### 4.10 Régua tirada da cabeça reprova o jogo original

Levantei que 30 placas em cima de warp eram defeito. Medi: o vanilla tem 2,64%
e nós temos 1,26%, ou seja, **o dobro da nossa taxa**. Se eu tivesse mandado
consertar, teria tirado placa boa. Antes de chamar de bug, meça a fonte.

### 4.11 Teste que guarda cópia de um fato envelhece calado

Três casos desta sessão: teste com número de flag cravado (o número andou quando
o teto de treinador subiu), testador com cópia própria do roteiro de abertura
(o começo mudou de Twinleaf para Pallet), e teste dependendo de NPC que anda.
Leia o fato da fonte; não copie.

### 4.12 Existir não é ser único, e gerador de rótulo tem que ler o arquivo

11/08/2026: o `texto_sinnoh.py` escreveu 790 rótulos e a conferência disse que
todos existiam no `scripts.inc` do próprio mapa. **O assembler reprovou 134
deles em 50 mapas**, porque existência e unicidade são checagens diferentes:
rótulo duplicado existe duas vezes e passa na primeira.

A causa não foi colisão interna. Foi colisão com o que **já estava no arquivo**
de sessões anteriores: o gerador começava com o conjunto `usados` vazio em cada
mapa e renumerava do 1, reescrevendo o `Placa4` que o `texto_placas_sinnoh.py`
tinha escrito antes. Gerador de nome tem que semear `usados` lendo o arquivo.

A checagem certa é na **unidade de montagem**, não por arquivo: os 2018
`scripts.inc` entram num único `data/event_scripts.s`, então o nome precisa ser
único no conjunto inteiro (35.747 rótulos), e a checagem por arquivo deixaria
passar colisão entre mapas. Está em `texto_sinnoh.py --demo`, e ela ignora
`.if/.else` de propósito, senão o vanilla a reprova pelo motivo errado (4.3).

**Landmine registrado:** `fecha_portas_sinnoh.py`, `importa_unova.py` e
`importa_trocas_unova.py` usam o mesmo esquema `<Mapa>_EventScript_Npc<N>` e
**nenhum semeia `usados`**. Hoje não há duplicata, conferida nos 35.747. Quem
rodar um deles num mapa que já tem `Npc1` repete este build quebrado.

### 4.13 `\l` também cobra aperto de botão, e o verificador que só olhou `\p` deu verde

11/08/2026, traduzindo os cinco portos. O número de `A` de 24 roteiros de teste
está embutido no número de páginas de cada caixa, então antes de buildar foi
escrito um verificador que comparava, rótulo a rótulo contra o `HEAD`, quantos
`\p` cada `.string` tinha. Ele deu **zero divergência**, e a suíte reprovou
**9 casos**, todos de barco.

`\l` é `CHAR_PROMPT_SCROLL` e `\p` é `CHAR_PROMPT_CLEAR`. **Os dois são
PROMPT**: param e esperam o jogador apertar A. Só `\n` passa direto. Um texto de
três linhas com `\l` no meio cobra um aperto a mais que o de duas linhas que ele
substituiu, e cada roteiro parou um `A` antes, ainda no porto de origem.

A lição não é "lembre do `\l`". É a 4.4 outra vez, num lugar novo: **o
verificador foi escrito a partir da minha lembrança de como o motor trata `\l`,
em vez de do charmap.** Medir a coisa errada com precisão dá verde, e verde de
verificador quebrado é pior que verificador nenhum (4.3). O que salvou foi a
suíte, e o que fechou o diagnóstico foi o conjunto das falhas ser EXATAMENTE o
conjunto dos casos que atravessam porto, sem um caso de outro assunto sobrando.

---

## 5. Regras de trabalho

- **Nunca escrever mapa, time ou texto do zero quando a fonte tem.** Toda vez
  que alguém escreveu conteúdo nesta sessão, foi o caminho errado.
- **Nunca ler exit code atrás de pipe.** `make -j8 > /tmp/x.log 2>&1; echo $?`.
- **Empurrar só com `antes_de_empurrar.sh` VERDE.** Commitar pode sempre.
- **Agente paralelo recebe faixa de flag e de id exclusiva**, tirada do
  `flags_livres.py`. Já colidiram.
- **Vars são escassas** (30 no jogo inteiro), flags são baratas. Antes de gastar
  var, leia `SINNOH-PADRAO.md`, que tem três técnicas que dispensam.
- Build: `export DEVKITARM="$HOME/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64-arm-none-eabi"`.
- Commit como o Gui: `git -c user.name="Guilherme Duarte" -c user.email="gduarte3030@gmail.com" commit`.
  Português acentuado, sem em dash, sem trailer de IA.

### Compatibilidade de save

A save guarda **índices**: `(mapGroup, mapNum)`, índice de objeto, número de
flag. Todo índice é promessa permanente, e não há migração em pokeemerald.

- mapa novo só no **fim** do grupo
- grupo novo só no **fim** de `group_order`
- objeto novo só no **fim** da lista do mapa
- flag nova só do pool que já está dentro de `FLAGS_COUNT`

### Teto de 128, e a política de grupo (decidida em 05/08/2026)

`struct WarpData` guarda `s8 mapGroup` e `s8 mapNum` (`include/global.h:668`).
O mapa de índice **128** de um grupo vira -128 dentro do warp e **o jogo reseta
ao entrar nele**. Medido no emulador índice a índice: 127 entra, 128 derruba. O
mesmo teto vale para a quantidade de grupos. Custou 26 mapas mortos no grupo de
portas de Sinnoh, todos com warp que o validador estático dava por bom.

Estado medido: **126 dos 128 grupos em uso, e 14.302 vagas livres DENTRO dos
grupos existentes.** O que é escasso é grupo, não vaga.

**Política: não criar grupo novo.** Mapa novo entra no fim de um grupo que já
existe e tem vaga (`fecha_portas_sinnoh.grupo_com_vaga` escolhe sozinha). Criar
grupo só com autorização explícita do Gui, porque só restam 2 e não há como
devolver. O `antes_de_empurrar.sh` recusa grupo acima de 128.

`python3 dev_scripts/guarda_save.py` tem que dizer SAVE COMPATIVEL.

**A janela de quebrar save foi REABERTA pelo Gui em 12/08/2026, só para a
revisão deste dia.** Palavra dele: a save atual pode ser descartada; é da
**próxima** save em diante que precisa aguentar edição futura. Enquanto a janela
estiver aberta valem `MAX_TRAINERS_COUNT` maior, `FLAGS_COUNT` maior, mapa
inserido no meio de grupo, objeto no meio de mapa e apagar conteúdo inventado em
vez de escondê-lo atrás de flag.

**Quem fecha a janela é a entrega:** a última ação antes de mandar a ROM nova é
`python3 dev_scripts/guarda_save.py --gravar` sobre ela, congelando a impressão
nova. Da ROM seguinte em diante, tudo abaixo volta a valer como estava.

**Faça o alargamento de teto cedo.** Bloco que descobre tarde que precisa de mais
id não reabre a janela sozinho.

(Ela tinha FECHADO em 05/08/2026, com a decisão 14 da seção 3. Este parágrafo já
disse por seis dias que ela "fecha quando o Gui receber a primeira build", no
presente, depois de ela já ter fechado.)

Linha de base gravada em 11/08/2026 sobre a build `296474325a`
(`roms/pokemon-claude-2026-08-11.gba`, md5 `457f3b5211b75175a0af5b95e04616c7`),
que é a ROM que o Gui vai jogar. `dev_scripts/save_impressao.json` é a impressão
dela. Daqui em diante, quebra de save não é "aceitável se registrada": é
vermelho no portão, e desfazer é a resposta padrão.

**Cuidado que o guarda NÃO pega, porque não é quebra de save:** flag que só é
acesa em jogo novo (`EventScript_ResetAllMapFlags`) nasce apagada em save
antiga. É o caso de `FLAG_SINNOH_NPC_DUPLICADO` e das três `FLAG_REGIAO_*`: a
save de 05/08 carrega e funciona, mas com os 382 clones visíveis e os portos
fechados. Consertar isso exige `MAP_SCRIPT_ON_TRANSITION`, e é decisão do Gui.

---

## 6. Faixas de id de treinador em uso

| faixa | dono |
|---|---|
| 1367-1379 | Unova, chefes |
| 1400-1799 | Kanto |
| 1800-2147 | Unova, rota |
| 2200-2273 | Kanto, segunda leva |
| 2274-2440 | Johto, rota (vai até 2440, não até 2417) |
| **2441-3999** | **livre: 1559 ids, depois do teto subir para 4000 em 12/08/2026** |

Conferido id a id em 11/08/2026 lendo `opponents.h`, depois de duas frentes de
treinador receberem faixa inventada a partir desta tabela: a de rota recebeu
2418-2549, que colide com Johto embaixo e estoura o teto em cima, e a de masmorra
recebeu 2550-2749, **inteira acima do teto de 2500**. Nenhuma das duas chegou a
gastar id, porque as duas descobriram antes que os 425 `TRAINER_SINNOH_*` já
estavam declarados e já tinham time. Tabela errada em documento é faixa errada em
agente: confira aqui antes de prometer faixa a alguém.

---

## 7. Ferramentas

Todas em `dev_scripts/`. Cada uma tem `--demo` ou `--autoteste` e o motivo de
existir escrito no topo.

| ferramenta | o que faz |
|---|---|
| `antes_de_empurrar.sh` | Portão. Builda o HEAD em worktree isolada e roda tudo |
| `completude.py` | Quanto de cada região está pronto, contra a fonte dela |
| `valida_rom.py` | Compara o declarado com o que o build **emitiu** |
| `valida_warp_tile.py` | Warp que existe e nunca dispara |
| `valida_conectividade.py` | Warp quebrado, alcance, porta única que não devolve |
| `valida_mapas_sinnoh.py` | Sprite sem gráfico, objeto fora do mapa |
| `guarda_save.py` | Impede mudança que invalida save |
| `flags_livres.py` | Quais flags estão **realmente** livres |
| `curva_de_nivel.py` | Mede e remapeia nível do TREINADOR por região |
| `curva_selvagem.py` | Mede e remapeia nível do SELVAGEM, e põe gen 6-9 em slot duplicado |
| `gens69_treinadores.py` | Gen 6-9 nos times, lenda em líder e E4, Dynamax no ace |
| `catalogo_especies.py` | Tipo, stat, geração e lenda de cada espécie, lidos do `species_info` (o enum de `species.h` mistura base e forma, e classificar por faixa de id põe mega de gen 1 na gen 9) |
| `testa_critico.py` | Casos T1 a T30, prova lida da **EWRAM** |
| `gba_runner.c` | Emulador headless que lê memória do jogo (`--mem16`/`--mem32` leem endereço cru) |
| `prova_musica_johto.py` | Qual faixa cada mapa TOCA, lida do header e do driver de som |
| `demake_gen2.py` / `demake_ds.py` | Converte mapa de gen 2 e gen 4 |
| `fecha_portas_sinnoh.py` | Interior de cidade de Sinnoh com planta reaproveitada do repo |
| `abre_portas_extras_sinnoh.py` | Desenha a porta que falta, copiando um warp do proprio mapa |
| `converte_cavernas_sinnoh.py` | Caverna de Sinnoh com a planta CONVERTIDA da grade 2D do DS |
| `importa_placas_johto.py` | Traz placa do `hns` com script e texto, e recusa a que não funciona aqui |
| `texto_placas_sinnoh.py` | Segue índice → `ScriptEntry` → banco de texto do Platinum |
| `itens_escondidos_sinnoh.py` | Desfaz a placa falsa: converte em item escondido o que vale, apaga o resto |
| `liga_flags_kanto.py` | Tira do stub só a flag que algum script mexe |

As cinco fontes ficam em `../fontes-mapas/`: `pokeemerald`, `pokefirered`,
`hns` (Johto), `sinnoh` e `pokeplatinum` (Sinnoh), `bw3g` (Unova). O BW3G morava
em `/tmp` e foi movido em 05/08/2026, porque `/tmp` é limpo pelo sistema e seis
scripts liam de lá.

---

## 8. O que falta, em ordem de tamanho

1. **Sinnoh, mapas em 72,4%, e a fila barata acabou** (medido em 11/08/2026).
   As 12 cavernas de geometria convertida e os 11 interiores teimosos que este
   item listava **já entraram** nas levas de 06/08: hoje
   `abre_bocas_cavernas_sinnoh.py` dá 0 pendências e os outros dois abridores só
   apontam para pai que não é mapa de rua. Faltam **164 mapas**, e nenhum deles
   sai com a técnica atual:

   | quanto | o quê | motivo medido |
   |---|---|---|
   | 46 | Turnback Cave e os `UNKNOWN_533` a `557`, que são as mesmas salas duplicadas | **zero pais** no grafo de warp da fonte: a sala é sorteada por script, não há warp estático que a crie |
   | 10 | Distortion World | zero pais, e a grade dá de 0 a 31 tiles de chão, abaixo do piso de 8 em quase todos |
   | ~40 | Battle Frontier/Tower, salas do ginásio DP de Hearthome, elevadores da Liga, Vista Lighthouse | **zero chão de masmorra na grade**: interiores com mobília desenhada, o caso em que a grade 2D não basta |
   | ~15 | Amity Square, Trophy Garden, Great Marsh 1 a 6, Pal Park, Spring Path, Route 204 North, Fullmoon/Newmoon, Fuego, Hall of Origin | `MAP_TYPE_OUTDOORS`. **Deixados de fora de propósito:** são folhas do grafo e não destravam masmorra nenhuma, então virariam 15 salas vazias de 13x9 com nome de área, ou seja +2,5 pontos de régua e zero mapa (lição 4.10) |

   Passar disso exige converter mobília, não geometria de chão. Decisão do Gui.
   O `fontes-mapas/sinnoh`, que é GBA e seria barato, só tem 133 mapas próprios
   de Sinnoh e **todos os 133 já estão na ROM**: dessa fonte não sobra nada.
2. **Sinnoh, o resto dos NPCs.** Em 11/08/2026, **561 NPCs deixaram de ser mudos
   e 229 placas ganharam texto próprio**, todo o texto portado do pokeplatinum
   por `dev_scripts/texto_sinnoh.py` (o `texto_placas_sinnoh.py` dava 0 porque
   seguia só o comando `Message`, e a fonte usa também `NPCMessage`, 656 vezes,
   mais `EventMessage`, `ShowMapSign` e outros seis). Sobram **559 mudos**, e a
   divisão é medida na fonte: **344 são treinador do Platinum** (o `script` deles
   é constante `TRAINER_*`, não índice de texto: precisa de time e id, é outra
   frente), 108 apontam para Wi-Fi e Union Room, que **não existem nesta ROM**,
   68 são balconista/enfermeira/vendedor cujo rótulo não tem comando de texto,
   19 têm buffer ou caractere fora do charmap, 8 estão em mapa reprovado pelo
   alinhamento.

   **Os 230 `hidden_flag` e os 84 `coord_events` continuam de fora, e não é falta
   de flag.** Medido em `src/event_object_movement.c:2882`: o objeto nasce quando
   `!FlagGet(flagId)`, então flag nova que nenhum script acende deixa o objeto
   sempre visível, ou seja, idêntico a trazê-lo com `flag: "0"`, e ainda planta o
   bloqueio permanente das 39 pedras de Strength de Unova. A flag só vale junto
   com a cena que a acende. Faltam também 71 sem sprite honesto (Cynthia, Cyrus,
   Looker, os lendários de lago). Ver `PENDENCIAS-NPC-SINNOH.md`.
3. ~~146 "placas" de Sinnoh não são placa~~. **FEITO em 11/08/2026** por
   `dev_scripts/itens_escondidos_sinnoh.py`. A causa era o importador:
   `dev_scripts/importa_npcs_sinnoh.py:385` lê `fonte["bg_events"]` cru do
   Platinum, onde placa e item escondido moram no MESMO array e só se distinguem
   pela faixa do `script` (< 2500 = placa, 7000+ = item visível, **8000 a 8799 =
   item escondido**, `include/script_manager.h:90-98` da fonte). O jogador
   parava em cima de um item invisível e lia "the lettering has faded".

   **50 viraram item escondido de verdade** (`bg_events` do tipo `hidden_item`,
   a mesma mecânica de Hoenn: `mapjson` emite `bg_hidden_item_event` e o motor lê
   item, quantidade e flag do próprio evento, sem tabela para manter), em 34
   mapas, **custando 46 flags** da faixa `0x8F0` a `0x91D`. **96 foram
   apagadas**, 95 por serem lixo de rota (Stardust, Pearl, Shard, Poké Ball,
   poção comum) e uma porque `ITEM_SUITE_KEY` não existe nesta ROM.

   **46 flags para 50 itens**, e a diferença não é economia torta: quatro itens
   aparecem em DOIS mapas vizinhos com a MESMA flag do Platinum (Moon Stone em
   EternaCity e Route211_West, Thunderstone em Route229 e ResortArea, Zinc em
   Route219 e Route220, Rare Candy em Route226 e Route227). É costura de mapa da
   fonte, e no Platinum pegar de um lado apaga o do outro; dar uma flag nossa aos
   dois reproduz o jogo original.

   **Apagar `bg_event` não quebra save, e isso foi conferido, não presumido:**
   nada em SaveBlock1/2/3 guarda posição dentro de `bg_events` (o que a save
   guarda de evento é índice de `object_event`, em `objectEvents[]` e
   `objectEventTemplates[]`). Todo acesso do motor varre o array por COORDENADA
   dentro do mapa carregado: `src/field_control_avatar.c:1203`,
   `src/item_use.c:453` e `:483`, `src/secret_base.c:385`. A única identidade de
   item escondido que atravessa o save é a FLAG, e ela viaja dentro do próprio
   dado (`hiddenItemId + FLAG_HIDDEN_ITEMS_START`).

   **Armadilha medida, que continua valendo:** `script - 8000` **não** é a
   posição na tabela `gHiddenItems`, é a posição da flag dentro de
   `HIDDEN_ITEM_FLAGS_START` (`src/script_manager.c:534` da fonte); ler pela
   tabela resolve só 139 dos 146. Quem faz essa conta certo é
   `texto_sinnoh.tabela_de_itens()`, reusada em vez de reescrita.

   **FECHADO em 11/08/2026, mais tarde no mesmo dia.** O que este item chamava
   de "até 13 itens escondidos nos 8 mapas que o alinhamento reprova" eram
   **9, em 3 mapas**, e a estimativa velha errava por contar item escondido da
   fonte em mapa que **nunca importou item escondido nenhum**:
   `fecha_portas_sinnoh.py` e `converte_cavernas_sinnoh.py` já pulam
   `script >= 8000` na origem, então os interiores criados por eles
   (`ContestHallLobby`, `GalacticHq4F`, `GalacticHQ_Laboratory`,
   `PokemonMansionMaidsRoom`, `SandgemTown_RowanLab`) não tinham nada a
   consertar. Sobrava mesmo: 7 na Route222, 1 em GalacticHQ_2F e 1 em
   SinnohLeague_Entrance. Dois viraram item escondido (SKY PLATE e PP UP,
   custando **1 flag nova**, porque a do SKY PLATE já existia) e 7 foram
   apagados como lixo de rota.

   **Sobra exatamente UM, e ele fica**: o `script` 8075 de `GalacticHQ_2F` cai
   em (13,1) junto com outro evento da fonte depois da conversão de coordenada,
   e dois candidatos no mesmo tile não se distinguem. Escolher um seria o chute
   que esta ferramenta existe para evitar.

   **O alinhamento deixou de ser por ORDEM e passou a ser por COORDENADA**, e a
   troca não é gosto: a própria passada das 146 quebrou a régua velha. Apagar 96
   `bg_events` encurtou os nossos arrays e a contagem parou de bater em 40 mapas
   **já resolvidos**, ou seja, a ferramenta ficaria incapaz de rodar de novo.
   Coordenada sobrevive: `importa_npcs_sinnoh.conversor_de_coordenada()`
   (extraída do próprio importador, não reescrita) diz onde cada evento da fonte
   foi parar, e a conta é refeita em vez de adivinhada. Duas guardas seguram o
   chute: **um `bg_event` nosso em coordenada que a fonte não tem reprova o mapa
   inteiro**, e **coordenada com mais de um candidato fica de fora**.

   **Contraprova rodada antes de escrever qualquer coisa:** o alinhamento novo
   reproduz os **50 de 50** itens que a passada ordinal já tinha convertido, com
   o mesmo item e a mesma flag do Platinum, zero divergência. E a regra do órfão
   separa sozinha os 96 mapas de `importa_npcs_sinnoh.py` dos 38 dos outros dois
   conversores: ela concorda com o campo `origem` do `map.json` nos 134, sem
   nenhuma exceção.

   **Numeração de flag passou a ser append-only** no mesmo dia, e isso era
   quebra de save esperando acontecer: `flags_em_uso()` reatribuía a faixa
   inteira por ordem alfabética a cada passada, então um nome novo no meio do
   alfabeto empurraria os 46 apelidos que já estão na ROM do Gui uma casa cada.
   Agora quem já tem número fica com ele e o nome novo só ocupa vaga livre.
4. **Unova.** Este item também estava velho: as 117 placas entraram em
   `febde977c3` e 33 NPCs em `0508831d27`. Em 11/08/2026 entraram as **9 trocas
   de Pokémon** (`dev_scripts/importa_trocas_unova.py`; `trade NPC_TRADE_X` lê
   tabela, não script, e por isso o importador de NPC recusava essas casas):
   objetos mudos 114 → 106, custo de 9 flags, zero var.

   O que sobra são as **209 cenas de enredo**, classificadas uma a uma: 107 são
   `changeblock` (1225 chamadas, exigem traduzir id de bloco de gen 2 para
   metatile), 47 usam `setscene`, 27 abrem batalha, 21 `special`, 16 `callasm`
   (a máquina de estados da Plasma). Das 32 mecanicamente portáveis, **17 são
   bloqueio** que o enredo apaga na fonte e aqui nunca apagaria, virando parede
   permanente (a armadilha das 39 pedras de Strength). Ver `PLANO-UNOVA.md`.
5. **426 flags de Kanto seguem em `0`**, e isso está certo: elas não são mexidas
   por script nenhum, então dar número a elas não mudaria nada em jogo. As 104
   que importavam saíram do stub em 05/08/2026
   (`dev_scripts/liga_flags_kanto.py`).
6. **As 20 rotas dirigidas de barco estão provadas em ROM** (T4, T6, T8, T10 e
   T86.1 a T86.12, prova lida da EWRAM, com mutante para cada caso). O texto de
   jogo dos cinco portos **saiu do português em 11/08/2026** e está em inglês,
   como o resto do jogo; junto foram as quatro falas do assistente do PROF. OAK
   em Vermilion, o item "Sair" do menu do marinheiro (agora "EXIT") e a balsa
   interna de Sinnoh entre Snowpoint e a Battle Zone, que ninguém tinha visto e
   falava português pelo mesmo motivo. **Nenhuma caixa de texto mudou de número
   de páginas**: os `\p` foram conferidos rótulo a rótulo contra o HEAD antes de
   buildar, zero divergência, e por isso nenhum dos 24 roteiros de botão que
   atravessam porto precisou ser reescrito. Re-rodado na build seguinte. As três
   `FLAG_REGIAO_*_LIBERADA` **foram ligadas em 11/08/2026**: o menu do marinheiro
   passou a ser montado em `data/scripts/travessia_regioes.inc` e esconde o
   destino da região ainda não liberada (Kanto sempre aberto; Johto pelo campeão
   de Kanto; Hoenn pela 8ª insígnia de Johto, porque esta ROM não tem Elite dos
   Quatro de Johto; Sinnoh pelo Wallace; Unova por `FLAG_ELITE_SINNOH_VENCIDA`,
   que a Cynthia já acendia). Zero flag nova, zero var, e nenhum `case` de porto
   mudou, porque `dynmultipush` devolve o **id empilhado** e não a linha. **O
   portão está provado na ROM** pelos casos T87.1 a T87.5, e a prova tem
   contraprova: numa ROM mutante, com os `call_if_set` do menu virando `call`,
   os cinco falham no ponto que a mutação prevê. Ver `PENDENCIAS-TRAVESSIA.md`.
7. **Ninguém jogou do começo ao fim.** Tudo aqui é build, dado estático e
   emulador em ponto específico.

**O aperto de ROM que este documento anunciava não existia.** Os "93 KB de
margem" eram a distância até uma linha de 95% que eu mesmo inventei como aviso,
não até o teto de 32 MB. Livres na build de 11/08/2026: **1,56 MB** (a ROM está
em 95,11%). Unova completa cabe, o resto de Sinnoh cabe, as placas de Johto
couberam.

---

## 9. Onde está o resto

| documento | assunto |
|---|---|
| `PRD-ROM-COMPLETA.md` | **O plano para acabar o hack**, em blocos B0 a B11, com os limites medidos e os portões que exigem o Gui |
| `PRD-CINCO-REGIOES.md` | Plano por blocos, decisões, desenho dos testes |
| `HANDOFF-2026-08-05.md` | O caso Kanto em detalhe, as oito camadas |
| `PLANO-UNOVA.md` | Unova: o que entrou, o que falta, e por quê |
| `PENDENCIAS-TRAVESSIA.md` | Barco entre regiões, o que foi provado e o que não |
| `PENDENCIAS-JOHTO.md`, `PENDENCIAS-INTRO.md`, `PENDENCIAS-GALACTICA.md` | Pendências por frente |
| `SINNOH-PADRAO.md` | Padrões de script que economizam var |
| `RECURSOS-REGIOES.md` | Fontes avaliadas, com o veredito medido de cada |
| `DEMAKE-DS.md` | Formato de mapa de gen 4 e gen 5 |
