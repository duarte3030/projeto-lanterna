# Estado do hack, e como trabalhar nele

Ponto de entrada. Leia este arquivo antes de qualquer coisa; ele diz onde o
projeto está, o que já foi decidido, e as armadilhas que já custaram sessões
inteiras. Detalhe fica nos documentos apontados no fim.

Última medição: 12/08/2026, na build de fechamento (sessão de fechamento do dia). A seção 0 abaixo é a passagem de bastão dela.

---

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

| região | mapas | objetos | warps | placas |
|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100,0% | 100,0% |
| Johto | **95,9%** | 94,0% | 100,0% | 96,0% |
| Hoenn | 100,0% | 100,1% | 100,0% | 100,0% |
| Sinnoh | **72,7%** | 77,2% | **99,2%** | **81,2%** |
| Unova | 94,2% | 98,5% | 98,9% | 98,0% |

**ATENÇÃO, a linha de Unova está tecnicamente certa e mesmo assim engana.**
`completude.py` conta PRESENÇA de mapa, objeto, warp e placa. Ele **nunca abre o
`blockdata`**, então caixa vazia com as portas e os NPCs certos passa com 98%. O
Gui olhou o jogo e desconfiou em 12/08/2026; a medição deu razão a ele.

Medindo **metatiles distintos por mapa**, que é a variedade do desenho:

| região | mediana | máximo | mapas com 3 ou menos |
|---|---|---|---|
| Kanto | 52 | 319 | 0 |
| Hoenn | 39 | 545 | 11 |
| Sinnoh | 39 | 303 | 0 |
| **Unova** | **3** | **5** | **155 de 291** |

Máximo 5 em 291 mapas: Unova é **máscara de colisão em duas cores**, chão e
parede mais o metatile de porta. E não tem **um tileset próprio sequer**: os 291
mapas usam tileset de Hoenn e de Sinnoh (138 em `Building + GenericBuilding`, 75
exteriores em `GeneralSinnoh + PetalburgSinnoh`, 32 em `CaveSinnoh`).

O que **está** pronto em Unova, e é por isso que a região não é lixo: 1396 NPCs,
1060 warps, 497 placas, 6234 linhas de texto de verdade do BW3G, 360 treinadores
únicos todos com time, 87 mapas com encontro selvagem, e as dimensões exatas da
fonte. Unova é **conteúdo cheio com arte zerada**, o inverso de Sinnoh.

A conversão leu o `.ablk` certo (`AspertiaCity.ablk`, 308 bytes = 14x22 blocos de
gen 2 = os 28x44 metatiles do nosso layout) e parou na tradução de bloco para
metatile. Conserto no bloco **B12** do `PRD-ROM-COMPLETA.md`: o mesmo `.ablk`
relido com tabela honesta troca o `blockdata` sem mexer em índice nenhum, e a
arte existe na fonte (`fontes-mapas/bw3g/gfx/tilesets`, 60 PNG com `.pal`).

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

**Galar fica fora desta ROM.** Ver `RECURSOS-REGIOES.md`.

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
| `gba_runner.c` | Emulador headless que lê memória do jogo |
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
