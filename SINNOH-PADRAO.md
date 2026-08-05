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
