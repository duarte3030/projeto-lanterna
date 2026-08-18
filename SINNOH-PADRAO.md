# Padrão de recursos: vars consumidas pelo conteúdo novo

Arquivo criado em 06/08/2026 porque a instrução da tarefa do rival de Johto
mandava registrar aqui cada var gasta, e o arquivo ainda não existia no repo.
Se outra sessão já tinha uma versão deste documento, junte as duas tabelas em
vez de sobrescrever.

## Por que este arquivo existe

`include/constants/vars.h` tem cerca de **21 vars livres no jogo inteiro** (os
`VAR_UNUSED_0x40xx` sem dono), para **quatro regiões**. Var é o recurso mais
escasso do projeto. Flag não é: a faixa `0x270` em diante tem dezenas livres, e
o motor grava de graça a flag de cada treinador derrotado.

## Tabela de vars consumidas

| Var | Onde | Quem gastou | Por que flag não resolvia |
|---|---|---|---|
| `VAR_BLACKTHORN_GYM_STATE` (`VAR_UNUSED_0x404E`) | ginásio de Blackthorn | 05/08/2026 | quebra-cabeça de 4 pontes com 5 estados cumulativos (0 a 4). Uma flag guarda 1 bit; o ginásio precisa saber *quantas* pontes já acenderam, não *se* alguma acendeu |

**Total: 1 var.** Restam ~20.

## O que NÃO gastou var (e como)

O rival de Johto (SILVER, 6 encontros) e as cenas que faltavam no esconderijo de
Mahogany (22 armadilhas de piso, 5 câmeras, 6 ELECTRODE) entraram em 06/08/2026
com **zero var**. O orçamento era de 4. As três técnicas que substituíram var,
em ordem de utilidade:

1. **`coord_event` com gatilho `VAR_TEMP_0` e valor 0.** O motor zera os
   `VAR_TEMP_*` a cada entrada de mapa (`ClearTempFieldEventData`), então o
   gatilho está sempre valendo e o `coord_event` dispara sempre. Quem lembra que
   a cena já aconteceu vai para dentro do script, numa **flag**. Isso derruba a
   crença de que "coord_event exige uma var", que fez as sessões anteriores
   cortarem cena por cena. O padrão já estava em uso no repo, em
   `data/maps/AzaleaTown_Gym/events.inc`.
   Detalhe do motor, para quem quiser ir mais longe: `ShouldTriggerScriptRun` em
   `src/field_control_avatar.c` chama `GetVarPointer(trigger)` e, se voltar
   `NULL` (ou seja, se o número for **menor que 0x4000**, que é o caso de toda
   flag), cai em `FlagGet(trigger) == index`. Ou seja, dá para pôr uma FLAG
   direto no campo `var` do `coord_event`. Não usei porque `VAR_TEMP_0` já
   resolvia e tem precedente neste repo, mas fica registrado.

2. **`MAP_SCRIPT_ON_TRANSITION` ligando/desligando a flag de esconder do
   objeto.** O motor roda `RunOnTransitionMapScript()` **antes** de `InitMap()`,
   que é quem faz nascer os `object_events` (`src/overworld.c`). Então um
   roteiro de 5 linhas por mapa ("esconde por padrão; mostra só se o encontro
   anterior já caiu e este ainda não") faz o papel de uma var de estágio de
   história inteira. Precedente vanilla:
   `BattleFrontier_BattleTowerLobby_OnTransition`.

3. **Raio de visão de treinador no lugar de `coord_event` + cutscene.** O motor
   já faz exclamação, aproximação, batalha e gravação do "já perdeu" sozinho.
   Foi assim que as 5 câmeras do B1F viraram 5 guardas e que as 4 batalhas do
   rival dispensaram roteiro de movimento.

Quem for gastar var: tente as três acima primeiro, e escreva aqui o motivo de
não terem servido.

## NPC duplicado de Sinnoh: 1 flag para 382 pares (11/08/2026)

`FLAG_SINNOH_NPC_DUPLICADO` (`FLAG_UNUSED_0x8EA`), **zero var**. O importador do
pokeplatinum trouxe de novo gente que já tinha sido escrita à mão, e desde a leva
de texto de 11/08 os dois falam. Apagar objeto está proibido (a save guarda
índice de objeto), então o clone perdedor de cada par leva esta flag no campo
`flag` e não nasce (`src/event_object_movement.c:2882`: nasce quando
`!FlagGet(flagId)`). Uma flag só serve para todos porque nenhum par precisa de
bit próprio: ou o clone existe, ou não existe, para sempre. Acesa uma vez em
`EventScript_ResetAllMapFlags` (`data/scripts/new_game.inc`), junto com as outras
flags de esconder de jogo novo. Reversível: apagar a flag traz os 382 de volta.

## Travessia entre regiões: 3 flags já reservadas, zero nova (11/08/2026)

`FLAG_REGIAO_JOHTO_LIBERADA`, `FLAG_REGIAO_HOENN_LIBERADA` e
`FLAG_REGIAO_SINNOH_LIBERADA` existiam desde sempre e nenhum script as lia.
Agora o menu dos cinco portos é montado em `data/scripts/travessia_regioes.inc`
e esconde o destino da região ainda não liberada. **Zero var e zero flag nova**:
Unova entra atrás de `FLAG_ELITE_SINNOH_VENCIDA`, que a Cynthia já acendia.

A técnica que dispensou var: `dynmultipush NOME, ID` empilha uma opção com um
**id próprio**, e o `dynmultistack` devolve esse id em `VAR_RESULT`, não a linha
escolhida. Por isso o menu encolhe sem que nenhum `case` dos cinco portos mude.
Quem for montar outro menu variável use isto em vez de gastar var de estado.

## Flags tiradas do stub de FRLG (registro, para não colidir)

Flag de Kanto não é "livre por padrão": `include/constants/flags.h` só inclui
`flags_frlg.h` dentro de `#if IS_FRLG`, e nesta build `IS_FRLG` é 0. No ramo
`#else` as 532 flags de Kanto viram o literal **0**, e `GetFlagPointer(0)`
devolve `NULL`. Consequência medida: `setflag` é no-op, `FlagGet` é sempre
`FALSE`, e todo objeto de Kanto escondido por flag **nasce sempre**, às vezes em
cima do caminho do jogador.

Quem precisar de uma dessas flags tira ela do stub, uma a uma, apontando para um
`FLAG_UNUSED_*` sem dono, e **registra aqui**.

| Flag | Número | Quem tirou do stub | Por quê |
|---|---|---|---|
| `FLAG_HIDE_OAK_IN_HIS_LAB` | `FLAG_UNUSED_0x1DE` | abertura de Pallet, 05/08/2026 | o Oak tem que estar fora do laboratório até o jogador ser parado na saída norte |
| `FLAG_HIDE_OAK_IN_PALLET_TOWN` | `FLAG_UNUSED_0x1DF` | abertura de Pallet, 05/08/2026 | com a flag em 0 ele nascia em (10,8) e **trancava a fileira 8**, o único caminho da casa até a rota 1 |

Sobram `FLAG_UNUSED_0x1E0` a `0x1E3` nesse bloco. A abertura de Pallet gastou
**zero var**: `VAR_MAP_SCENE_PALLET_TOWN_OAK` e
`VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB` já existem em `vars_frlg.h`.

Cuidado que fica de aviso: essas duas vars de FRLG são `0x4050` e `0x4055`, que
em `vars.h` são `VAR_LITTLEROOT_TOWN_STATE` e `VAR_VERDANTURF_TOWN_STATE`. A
segunda está marcada como não usada, mas a **primeira é de Hoenn e é usada**: a
cena do Oak em Pallet Town e o estado de Littleroot escrevem no mesmo lugar.
Não atrapalha a abertura de Kanto, mas quem for ligar a chegada em Hoenn precisa
resolver isso antes.

## Flags gastas pelos itens escondidos de Sinnoh (11/08/2026)

**Vars gastas: zero.** Item escondido não usa var nenhuma: a flag mora dentro do
próprio `bg_event` (`hiddenItemId + FLAG_HIDDEN_ITEMS_START`), e é o motor que a
acende ao entregar o item.

Faixa reservada a esta frente: `0x8F0` a `0x91F`, 48 flags. **Gastas 46**, de
`FLAG_UNUSED_0x8F0` a `FLAG_UNUSED_0x91D`; sobram `0x91E` e `0x91F`. O bloco de
apelidos está no fim de `include/constants/flags.h`, todos com o prefixo
`FLAG_ITEM_SINNOH_`, e é **regenerado** a partir dos `map.json` por
`dev_scripts/itens_escondidos_sinnoh.py`: não editar à mão.

São 46 flags para **50** itens porque quatro deles aparecem em dois mapas
vizinhos com a mesma flag do Platinum (costura de mapa da fonte, ver o item 3 da
seção 8 do `ESTADO.md`). Dividir a flag entre os dois é o que o jogo original
faz.

Dois limites do motor que quem mexer nisso precisa respeitar, medidos e não
lembrados:

- `asm/macros/map.inc:107` aborta a montagem com flag abaixo de
  `FLAG_HIDDEN_ITEMS_START` (`0x1F4`);
- `hiddenItemId` é um campo de **13 bits** e `item` de **11 bits**
  (`include/global.fieldmap.h:194-201`), ou seja, a flag tem que ficar a menos
  de 8192 do início e o id do item abaixo de 2048.

## Flags gastas pelo trio de iniciais por região (05/08/2026)

**Vars gastas: zero.** `VAR_STARTER_MON` já existia e agora é escrita pelas
cinco regiões, cada uma com o índice dentro do PRÓPRIO trio (0=grama, 1=fogo,
2=água; Kanto é a exceção e mantém a numeração do FRLG, 0=Bulbasaur,
1=Squirtle, 2=Charmander, porque os scripts do rival de Kanto já a leem assim).
Como cada região escreve na chegada e só os scripts daquela região leem, uma var
só serve para as cinco.

| Flag | Onde | Por que uma por região |
|---|---|---|
| `FLAG_INICIAL_JOHTO` (`FLAG_UNUSED_0x054`) | laboratório do Elm | esconde as três Poké Bolas depois da escolha |
| `FLAG_INICIAL_SINNOH` (`FLAG_UNUSED_0x055`) | laboratório do Rowan | idem |
| `FLAG_INICIAL_UNOVA` (`FLAG_UNUSED_0x4EF`) | laboratório de Nuvema | idem |

`FLAG_SYS_POKEMON_GET` não serve como porteiro dessas três: com a ordem
cronológica (decisão 66) quem a acende é o Oak, em Kanto, e a partir dali as
bolas dos outros laboratórios não nasceriam mais. Kanto continua com ela porque
é a primeira região, e Hoenn continua com
`FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG`, que já é só dela.

**Nota de faixa:** a faixa reservada para este agente era
`FLAG_UNUSED_0x050` a `0x05F`, mas só **duas** dessas dezesseis existem livres
(`0x054` e `0x055`): `0x50` a `0x53` e `0x56` a `0x5F` são flags de Hoenn em
uso (`FLAG_RESCUED_BIRCH`, `FLAG_SET_WALL_CLOCK` e companhia). Como os três
laboratórios precisam de três bits independentes (um jogador pode pular o
laboratório de uma região e pegar o inicial da seguinte primeiro, então contador
de 2 bits não resolve), a terceira saiu de `FLAG_UNUSED_0x4EF`, o fim de um
bloco de 64 flags livres que nenhum agente encostou. Escrito aqui para que a
próxima faixa distribuída seja conferida contra o arquivo antes de ser
prometida.

## Cenas da Galáctica que faltavam na espinha (12/08/2026, bloco B6)

**Vars gastas: zero. Flags gastas: 4**, todas da faixa exclusiva daquela frente
(`FLAG_UNUSED_0x1900` a `0x19FF`); sobram 252. Ferramenta:
`dev_scripts/cena_galactica_sinnoh.py` (`--demo` e idempotente).

O que entrou: os **doze** treinadores que tinham constante, bloco em
`trainers.party` e fala traduzível e ainda assim **não estavam em mapa nenhum**,
mais um grunt mudo da mesma cena. Eles ficavam de fora porque
`importa_npcs_sinnoh.py` recusa, de propósito, todo objeto do Platinum com
`hidden_flag`: sem a cena que apaga a flag, o objeto vira parede permanente.

| Flag | Onde | Some quando |
|---|---|---|
| `FLAG_GALACTICA_MT_CORONET` (`0x1900`) | 8 objetos nos 5 andares de Mt. Coronet | o Cyrus cai no Spear Pillar |
| `FLAG_GALACTICA_QG_TOMADO` (`0x1901`) | Scientist Fredrick (QG 1F) e Darrius (QG 2F) | o Saturn cai na sala de controle |
| `FLAG_SINNOH_ROUTE210_WYATT_ESCONDIDO` (`0x1902`) | Jogger Wyatt, Rota 210 sul | não é de manhã |
| `FLAG_SINNOH_ROUTE212_DANNY_ESCONDIDO` (`0x1903`) | Policeman Danny, Rota 212 sul | não é de noite |

O Scientist Travon, do 3F do prédio de Eterna, **não gastou flag**: reusa
`FLAG_GALACTICA_ETERNA`, que existe desde 04/08/2026 e já é acesa pela derrota
da Jupiter. O que mudou é que o próprio 3F ganhou o `ON_TRANSITION`, para o
prédio esvaziar sem depender de o jogador voltar à rua de Eterna primeiro.

A técnica que dispensou var, de novo, é a 2 da lista acima:
`MAP_SCRIPT_ON_TRANSITION` + `call_if_defeated`. O marco de cada cena é a flag
de "já derrotei" que o motor grava sozinho para o treinador-gatilho, então
nenhuma var de estágio de história foi criada.

Duas armadilhas medidas escrevendo isto, para a próxima sessão não pagar de novo:

- **`enum` de C não existe para o montador.** `TIME_MORNING` e `TIME_NIGHT` são
  membros de `enum TimeOfDay` (`include/constants/rtc.h:98`), não `#define`;
  escrever o nome num `goto_if_eq` de `scripts.inc` não monta, mesmo com
  `constants/rtc.h` incluído em `data/event_scripts.s`. Vai o número cru (0 e 3)
  com o nome no comentário, precedente do `setmetatile 13, 11, 588` do
  SpearPillar.
- **`texto_sinnoh.resolve` devolve TUPLA**, `(texto, comandos de buffer)`, e
  `treinadores_masmorra_sinnoh.falas` repassa a tupla inteira. Quem escrever
  `.string "{intro}"` com isso grava o `repr` da tupla dentro das aspas. Custou
  37 linhas em dez `scripts.inc` na primeira rodada desta leva.

### Empréstimos de sprite desta leva

Nenhum empréstimo NOVO foi inventado: os cinco saem da tabela
`valida_mapas_sinnoh.TROCA_SPRITE`, que já existia. `GRUNT_M` →
`MAGMA_MEMBER_M`, `GRUNT_F` → `MAGMA_MEMBER_F`, `SCIENTIST_M` → `SCIENTIST_1`,
`JOGGER` → `RUNNING_TRIATHLETE_M`, `POLICEMAN` → `GENTLEMAN`.

Fora da tabela, uma troca de julgamento: **o Cyrus saiu de
`OBJ_EVENT_GFX_MAN_5` para `OBJ_EVENT_GFX_MAXIE`**, nos dois mapas em que ele
aparece (`SpearPillar` e `GalacticHQ_Hall`). É o precedente registrado em
`ARTE-PENDENTE.md` (chefe de equipe criminosa emprestando chefe de equipe
criminosa), e `MAN_5` é um senhor genérico. `graphics_id` não entra na save,
então a troca é reversível e não custa nada.

**Fica pendente, e é medida e não palpite:** `ARTE-PENDENTE.md` manda
Mars, Jupiter e Saturn usarem `OBJ_EVENT_GFX_MAGMA_ADMIN`, e esse sprite **não
existe nesta build** (conferido com `valida_mapas_sinnoh.sprites_utilizaveis`;
`COURTNEY` e `AQUA_ADMIN_F` também não). Os três seguem em
`MAGMA_MEMBER_F`/`MAGMA_MEMBER_M`, e a Cynthia segue em `OBJ_EVENT_GFX_BEAUTY`.

## História de Unova, bloco B6: 1 var e 12 flags (12/08/2026)

**Var gasta: 1.** `VAR_UNOVA_LIGA_CENA` (`VAR_UNUSED_0x4160`), faixa exclusiva
desta frente `0x4160` a `0x41BF`.

O BW3G tem `setscene`/`checkscene`, uma máquina de estados **por mapa** que o
motor do gen 2 guarda sozinho, e 47 das 209 cenas de Unova dependem dela. Aqui
não existe equivalente, então cada mapa da fonte que tem `scene_script` vira uma
var com os mesmos valores, na mesma ordem em que os `scene_script` aparecem no
`.asm`. `ChampionsRoom.asm` tem quatro, e as três técnicas que dispensam var não
serviram: são estados **sequenciais e excludentes** (0 a 3), não bits
independentes, e o `MAP_SCRIPT_ON_TRANSITION` precisa ler o estágio para decidir
quais dos sete objetos da sala nascem.

**Flags gastas: 12**, da faixa exclusiva `FLAG_UNUSED_0x1A00` a `0x1AFF`.
Nomeadas em `include/constants/flags.h`, logo depois de `FLAG_UNOVA_LIGA_ELENCO`.

| flag | serve para |
|---|---|
| `FLAG_UNOVA_CENA_ENTRADA_LIGA` | a emboscada das três sombras já rodou |
| `FLAG_UNOVA_CENA_JUNIPER`, `_SOMBRAS`, `_GENESECT_1`, `_GENESECT_2`, `_GENESIS` | esconder cada grupo de figurante da sala do Campeão. Eram um guarda-chuva só (`FLAG_UNOVA_LIGA_ELENCO`, do B5); a cena mostra e esconde cada grupo em momento diferente, então cada um virou um bit. **`_JUNIPER` extrapolou a sala do Campeão:** virou o bit compartilhado de esconder NPC de cena em **oito** mapas de Unova (o último trio entrou em 16/08/2026), cada um reescrevendo o bit no próprio `ON_TRANSITION`; contrato completo em `data/maps/Unova_ChampionsRoom/scripts.inc` |
| `FLAG_UNOVA_GENESIS_VENCIDO` | o `EVENT_BEAT_GENESIS_PROJECT` da fonte |
| `FLAG_UNOVA_LIGA_VENCIDA` | acesa pelo Hall da Fama; é ela que **solta** o selo da escada da Liga |
| `FLAG_UNOVA_LIGA_PORTAO` | "o jogador acabou de subir da entrada da Liga". Traduz o `setmapscene PKMN_LEAGUE_MAIN, SCENE_ELITE_FOUR_ROOM_ENTER` que a `PkmnLeagueEntrance` dispara no `MAPCALLBACK_NEWMAP`; sem ele a cena do terremoto rodaria também para quem volta de uma sala da Elite, e o `applymovement` de seis passos para o norte jogaria o jogador para fora do mapa |
| `FLAG_UNOVA_STRIATON_CHAVE_1`, `_2`, `_3` | os três interruptores que abrem a escada do CILAN |

`FLAG_UNOVA_LIGA_ELENCO`, que o B5 tinha gasto, **continua em uso** e passou a
ter dono de verdade: ela esconde os cinco figurantes da `ChampionsRoomEntrance`,
é apagada no início da emboscada e reacesa no fim. Isso não é enfeite: os
templates da JUNIPER e do METAGROSS ficam em (7,5), que é o **único** warp
daquele mapa.

**Técnica que evitou uma var a mais:** o selo da escada da Liga não tem
`setmetatile` de desfazer. O estado limpo é o do próprio `map.bin`, então basta a
cena **não rodar** quando `FLAG_UNOVA_LIGA_VENCIDA` está acesa. Bloqueio que se
desfaz sozinho ao deixar de ser reaplicado custa zero.

## As quatro cenas que fecharam a espinha (12/08/2026, bloco B6, segunda leva)

**Vars gastas: zero. Flags gastas: 6**, da mesma faixa exclusiva
(`FLAG_UNUSED_0x1900` a `0x19FF`); com as 4 da leva anterior são **10 de 256**.
**Ids de treinador: 5**, da faixa **2500 a 2519** liberada pelo condutor depois
que a frente de Johto largou `opponents.h` em 2461. Sobram **2505 a 2519**, e o
vão **2462 a 2499 fica vazio de propósito**, reservado para Johto retomar.

| cena | o bloqueio que cria | o marco que o desfaz |
|---|---|---|
| Celestic Town | o grunt da bomba em frente às ruínas | derrotá-lo (id 2500) |
| Rota 218 | o show ocupa a estrada (não a sela, ver abaixo) | a mesma `FLAG_GALACTICA_CELESTIC` |
| Lago Verity | a Mars e os 4 grunts na margem | derrotar a Mars (id 2501) |
| Lago Acuity | Jupiter e o rival no caminho da caverna | a cutscene rodar até o fim |
| Canalave | o rival cobra a revanche antes do Byron | derrotá-lo (2502, 2503 ou 2504) |

### Flags

| Flag | Nasce | Quem a vira |
|---|---|---|
| `FLAG_GALACTICA_CELESTIC` (`0x1904`) | apagada | a derrota do grunt de Celestic acende |
| `FLAG_CELESTIC_CYNTHIA_ESCONDIDA` (`0x1905`) | **ACESA**, em `EventScript_ResetAllMapFlags` | a mesma derrota apaga |
| `FLAG_GALACTICA_LAGO_VERITY` (`0x1906`) | apagada | a derrota da Mars acende |
| `FLAG_ESCONDE_LAGO_ACUITY` (`0x1907`) | **ACESA**, idem | o `ON_TRANSITION` do Lago Acuity apaga enquanto a janela da cena está aberta |
| `FLAG_GALACTICA_ACUITY_VISTO` (`0x1908`) | apagada | o fim da cutscene acende |
| `FLAG_GALACTICA_CANALAVE_RIVAL` (`0x1909`) | apagada | a derrota do rival acende |

**Duas nascem ACESAS, e isso é a regra e não a exceção:** flag de jogo novo
nasce apagada, e objeto com a flag apagada NASCE
(`src/event_object_movement.c:2882`). Quem só deve aparecer no MEIO da história
precisa começar escondido, então vai para `data/scripts/new_game.inc`. Sem essas
duas linhas a Cynthia estaria em Celestic desde o primeiro dia e a Jupiter
estaria no Lago Acuity antes de a Mars cair.

### Níveis: a curva foi MEDIDA do próprio arquivo, não deduzida

Os 5 times novos vieram do acervo `src/data/trainers_sinnoh.party`, que guarda os
níveis CRUS do Platinum. Convertê-los pedia a mesma regra que os 888 níveis de
Sinnoh já usam, e essa regra **não é uma fórmula que dê para reconstruir de
cabeça**: um ajuste linear pelos mínimos quadrados erra até 1 nível, e as três
tentativas de deduzir o deslocamento pelos comandantes deram 141, 142 e 139.

O que resolveu foi parear acervo e arquivo que compila, treinador a treinador:
saíram **888 pares (nível cru → nível escalado), e nenhum nível cru tem dois
destinos diferentes**. A conversão é uma tabela de consulta exata, medida na
hora, cobrindo 4 a 62 → 145 a 200. Foi ela que escreveu os 20 níveis novos, e
`curva_de_nivel.py` confirma depois: Sinnoh foi de 888 para 908 Pokémon com
mínimo 145 e máximo 200 intactos, ou seja a forma da curva não se mexeu.

Quem for acrescentar treinador de Sinnoh: refaça esse pareamento em vez de
copiar a tabela daqui. Tabela copiada envelhece calada (lição 4.11).

### O rival de Sinnoh tem TRÊS times, e o comentário do rival de Johto está velho

`data/maps/CherrygroveCity/scripts.inc` diz que o triângulo de tipos do rival é
impossível porque o laboratório não escreve `VAR_STARTER_MON`, e aponta para
`SandgemTown_House1`. **Medido em 12/08/2026: está errado nas duas metades.** O
laboratório do Rowan é `data/maps/SandgemTown_RowanLab/scripts.inc`, e ele
escreve `VAR_STARTER_MON` com 0, 1 e 2 desde 05/08/2026. Por isso o rival de
Canalave entrou com os três ids do Platinum e um `switch VAR_STARTER_MON`, e não
com um time fixo.

O nome de cada constante é o inicial **DO JOGADOR**, não o do rival: o ramo
`TURTWIG` (2502) é o que roda quando o jogador tem Turtwig, e o ace dele é
Infernape. Conferido bloco a bloco. Casos `T94.7` e `T94.8` provam os dois
extremos no emulador.

### O show da Rota 218 NÃO sela a estrada, e isso é medida

No Platinum os seis selam uma ponte de um tile, e a estrada para Canalave só abre
com a fala da Cynthia. **Aqui não:** medido com busca em largura sobre a grade de
colisão, selar a Rota 218 exigiria tapar as colunas 8, 9 e 10 inteiras das linhas
12 a 26; seis objetos não chegam perto, e sobram desvios pelas fileiras 16 a 21.

**Fechar o vão à mão está proibido, e o motivo é grave:** quem apaga a flag do
show é a cena de Celestic, e Celestic fica do outro lado do mapa. Bloqueio
inventado ali seria softlock. O `--demo` guarda a medida com uma busca em
largura e uma contraprova que tapa as três colunas e reprova.

### Empréstimos de sprite desta leva

Quatro personagens de nome próprio, nenhum com sprite nesta ROM. Eles não entram
em `valida_mapas_sinnoh.TROCA_SPRITE` de propósito (o comentário de lá proíbe
gente nomeada), então o empréstimo fica declarado na tabela `ROTEIRO`:

| quem | sprite emprestado | por quê |
|---|---|---|
| Comandante Mars | `OBJ_EVENT_GFX_MAGMA_MEMBER_F` | mesmo uniforme de equipe criminosa que Jupiter e Saturn já usam aqui |
| Comandante Jupiter | `OBJ_EVENT_GFX_MAGMA_MEMBER_F` | idem |
| Cynthia | `OBJ_EVENT_GFX_BEAUTY` | é o mesmo que ela já usa na sala do Campeão e no Spear Pillar distorcido |
| Cedric (o rival) | `OBJ_EVENT_GFX_RICH_BOY` | é a linha que `TROCA_SPRITE` já dá para `OBJ_EVENT_GFX_BARRY` |
| Guitarrista da Rota 218 | `OBJ_EVENT_GFX_MAN_3` | idem, `TROCA_SPRITE` |

`OBJ_EVENT_GFX_CLEFAIRY` e `OBJ_EVENT_GFX_PIKACHU` **existem** nesta build e
entraram sem empréstimo nenhum.

### Cortado de propósito, e o que custaria trazer

- **Old Charm.** `ITEM_OLD_CHARM` não existe nesta ROM, então o ancião fala o
  texto do Platinum inteiro mas nada muda de mão. Trazer custa um item novo.
- **Câmera livre da cutscene do Lago Acuity** (`AddFreeCamera`) e os dois ramos
  de `x=14`/`x=15` do original, que só existem porque lá o `coord_event` cobre
  dois tiles. O que a cena diz e faz é o mesmo.
- **Nome do rival por buffer.** O Platinum enche `{STRVAR_1 3, 0, 0}` com o nome
  que o jogador deu ao rival; aqui vai `CEDRIC` cravado, que é o nome do bloco de
  `trainers.party` (veio assim da própria fonte). O nome do JOGADOR continua
  dinâmico, com `{PLAYER}`.
- **Raio de visão no rival de Canalave.** O rival de Johto usa raio de visão, mas
  o script dele é um `trainerbattle_single` pelado. O de Canalave tem `lock`,
  `faceplayer` e um `switch` antes da batalha, e a aproximação automática do
  motor já fez as duas primeiras coisas: rodar o mesmo corpo pelos dois caminhos
  é pedir travamento num script que não dá para testar sem build. Ele não está em
  gargalo nenhum, então falar com ele basta.

### Extensão da mesma leva, mais tarde em 12/08/2026

**Zero var nova.** O que entrou depois:

- **A campeã JUNIPER**, três treinadores na faixa exclusiva **2520 a 2529** de
  `include/constants/opponents.h` (gastos 3, livres 2523 a 2529), com time em
  `src/data/trainers.party`. Os três são idênticos nos cinco primeiros Pokémon e
  mudam só no sexto (Serperior, Emboar, Samurott), como na fonte. A seleção usa
  `VAR_STARTER_MON`, que **já existia** e que o laboratório de Nuvema já escreve:
  zero var, zero flag. **Decidido em 12/08/2026, não relitigar:** ela fica com o
  inicial que *perde* para o do jogador, que é o que a fonte faz; o espelho foi
  considerado e recusado pela política de portar em vez de escrever enredo novo.
- **Os 18 pontos de cura de Unova**
  (`dev_scripts/heal_locations_unova.py`, idempotente, com `--demo` e mutação).
  Custo em var e flag: **zero**. Ponto de cura não usa nenhuma das duas: a save
  guarda `struct WarpData` em `lastHealLocation`, e o `respawn_npc` é um
  `LOCALID_*`, que é constante de montagem. Antes disto a região não tinha
  nenhum, e quem desmaiava em Unova voltava para outra região.
- **O conserto dos ledges** (`tileset_gen2.py` mais
  `blockdata_unova.alvos_de_pulo`): zero var, zero flag. É tabela de conversão,
  não estado de jogo.
