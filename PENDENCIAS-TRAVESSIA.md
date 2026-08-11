# Pendências da travessia entre regiões (barco)

Estado em 11/08/2026. Verificado estaticamente **não é** verificado: este arquivo
existe para separar as duas coisas.

**As 20 rotas dirigidas estão provadas na ROM**, cada uma com o par
`(mapGroup, mapNum)` lido da EWRAM depois da travessia. As 12 que faltavam
fecharam em 11/08/2026, em `dev_scripts/testes_criticos/86_travessias_diagonais.json`
(casos `T86.1` a `T86.12`), sem gastar flag, var, id de treinador, mapa, warp nem
objeto: são só casos de teste. Detalhe na seção 1.

---

## 0. Olivine ↔ Vermilion passa por dentro do S.S. Aqua (05/08/2026)

Das 20 rotas dirigidas, **duas deixaram de ser teleporte**: o marinheiro de
Olivine e o de Vermilion agora embarcam o jogador em `MAP_SSAQUA_1F`, e quem
desembarca do outro lado é o marinheiro da porta, dentro do navio. Os pontos de
desembarque continuam os mesmos de antes (`MAP_VERMILION_CITY` 15,10 e
`MAP_OLIVINE_CITY_PORT_INSIDE` 8,17), de propósito: os roteiros já provados não
precisaram ser re-derivados, só ganharam o trecho de bordo no fim.

Quem manda o sentido é `FLAG_SSAQUA_RUMO_KANTO`, posta no embarque. A porta do
cais em (29,1) é `MAP_DYNAMIC` e o `setdynamicwarp` do porto a aponta de volta
para o próprio porto; hoje ela é inalcançável a pé, porque o marinheiro da porta
fica em (29,2) e tranca o único acesso, então ela é seguro, não caminho.

Provado na ROM: **T4.2** (Kanto → navio → Johto), **T10.3** (Johto → navio →
Kanto, com a descida ao convés) e **T10.4** (11 tiles de convés e entrada na
cabine do jogador). `dev_scripts/valida_barco.py` ganhou a regra dos dois saltos
e reprova se o `setflag`/`clearflag` do sentido ou o `setdynamicwarp` sumirem.

As outras 18 rotas continuam teleporte direto, e está certo: o S.S. Aqua liga
Johto a Kanto, não os outros portos.

---

## 1. As 20 rotas dirigidas, e o que cada prova vale

Os cinco portos formam **20 rotas dirigidas** (5 portos x 4 destinos cada), e
todas as 20 estão provadas na ROM. A cadeia cronológica nos dois sentidos são as
8 primeiras, provadas em 05/08/2026:

| rota | caso |
|---|---|
| Kanto → Johto | T4.2 (cadeia inteira: campeão, passe, embarque) |
| Johto → Kanto | T10.3 |
| Johto → Hoenn | T6.2 |
| Hoenn → Johto | T8.2 |
| Hoenn → Sinnoh | T8.3 |
| Sinnoh → Hoenn | T8.5 |
| Sinnoh → Unova | T10.1 |
| Unova → Sinnoh | T10.2 (ida e volta) |

### As 12 diagonais, provadas em 11/08/2026

Até 11/08/2026 elas só tinham passado pelo `dev_scripts/valida_barco.py`, que lê
a fonte e afirma que o `case` do porto aponta para o script que dá `warpsilent`
no mapa que o nome do item promete, e que todo `warpsilent` tem `waitstate`.
Isso pega lista fora de ordem e `case` trocado, e **não** pega marinheiro
inalcançável, tile de desembarque ruim nem colisão, que foram exatamente os três
bugs achados nas 8 anteriores.

Agora cada uma tem o par `(mapGroup, mapNum)` lido da EWRAM no fim da travessia,
e a posição de chegada bate com a coordenada do `warpsilent` da fonte:

| caso | rota | DOWN no menu | EWRAM `location` no fim | pos |
|---|---|---|---|---|
| T86.1 | Kanto → Hoenn | 1 (SLATEPORT) | (9,9) = `MAP_SLATEPORT_CITY_HARBOR`, layout 88 | (8,14) |
| T86.2 | Kanto → Sinnoh | 4 (CANALAVE) | (75,11) = `MAP_CANALAVE_CITY`, layout 787 | (17,49) |
| T86.3 | Kanto → Unova | 3 (VIRBANK) | (112,7) = `MAP_UNOVA_VIRBANK_PORT`, layout 1347 | (4,6) |
| T86.4 | Johto → Sinnoh | 4 (CANALAVE) | (75,11) = `MAP_CANALAVE_CITY`, layout 787 | (17,49) |
| T86.5 | Johto → Unova | 3 (VIRBANK) | (112,7) = `MAP_UNOVA_VIRBANK_PORT`, layout 1347 | (4,6) |
| T86.6 | Hoenn → Kanto | 2 (VERMILION) | (37,5) = `MAP_VERMILION_CITY`, layout 486 | (15,10) |
| T86.7 | Hoenn → Unova | 3 (VIRBANK) | (112,7) = `MAP_UNOVA_VIRBANK_PORT`, layout 1347 | (4,6) |
| T86.8 | Sinnoh → Kanto | 2 (VERMILION) | (37,5) = `MAP_VERMILION_CITY`, layout 486 | (15,10) |
| T86.9 | Sinnoh → Johto | 0 (OLIVINE, zero DOWN) | (91,8) = `MAP_OLIVINE_CITY_PORT_INSIDE`, layout 1031 | (8,17) |
| T86.10 | Unova → Kanto | 2 (VERMILION) | (37,5) = `MAP_VERMILION_CITY`, layout 486 | (15,10) |
| T86.11 | Unova → Johto | 0 (OLIVINE, zero DOWN) | (91,8) = `MAP_OLIVINE_CITY_PORT_INSIDE`, layout 1031 | (8,17) |
| T86.12 | Unova → Hoenn | 1 (SLATEPORT) | (9,9) = `MAP_SLATEPORT_CITY_HARBOR`, layout 88 | (8,14) |

ROM usada: a build de 06/08/2026 01:15 que estava na árvore, com `include/`
congelado ao lado dela para o `--src`, porque três outros agentes escrevem no
repo ao mesmo tempo e `map_groups.h` deslocado descreveria outro jogo.

**Re-rodar os 20 casos na primeira build depois desta.** Não é ritual: enquanto
estes casos eram escritos, a frente de Sinnoh estava dando script de fala a dez
NPCs de `data/maps/CanalaveCity/map.json`, e cinco dos casos novos (`T86.8` a
`T86.12`) atravessam Canalave a pé, como já faziam `T8.5`, `T10.1` e `T10.2`.
Posição nenhuma mudou nesse diff, então a expectativa é verde; expectativa não é
medida.

**As 12 passaram na primeira tentativa, e é por isso que quatro mutantes foram
rodados**: resultado limpo demais é verificação quebrada até que se explique por
que é real (ESTADO.md, portão 4). Cada mutante caiu exatamente onde a mutação
prevê, e nenhum caiu em "passou assim mesmo":

- `T86.2` com **3 DOWN** em vez de 4 desembarca em `MAP_UNOVA_VIRBANK_PORT`
  (112,7), não em Canalave: o índice do menu é lido de verdade.
- `T86.9` com **1 DOWN** onde o certo é zero desembarca em
  `MAP_SLATEPORT_CITY_HARBOR` (9,9), não em Olivine.
- `T86.10` com **1 DOWN na segunda perna** desembarca em Slateport (9,9), e não
  em Vermilion.

Esse mutante sozinho **não** prova que o menu da segunda perna é o de Virbank e
não o de Canalave: 1 DOWN dá SLATEPORT nas duas listas, e 0 e 2 também coincidem.
Quem prova é a sequência de `location` lida ao longo da corrida inteira, e não só
o estado final. Medida, para os três casos que saem de Virbank:

```
T86.10  (75,11) CANALAVE_CITY -> (112,7) UNOVA_VIRBANK_PORT -> (37,5)  VERMILION_CITY
T86.11  (75,11) CANALAVE_CITY -> (112,7) UNOVA_VIRBANK_PORT -> (91,8)  OLIVINE_CITY_PORT_INSIDE
T86.12  (75,11) CANALAVE_CITY -> (112,7) UNOVA_VIRBANK_PORT -> (9,9)   SLATEPORT_CITY_HARBOR
```

O jogador **passou** pelo Porto de Virbank e saiu dele para três destinos
diferentes: é o marinheiro de Virbank que está sendo lido, e a lista dele tem os
quatro destinos certos.
- `T86.5` **sem o `20:DOWN*12`** que leva até o marinheiro fica em
  `MAP_OLIVINE_CITY_PORT_INSIDE` (91,8): os `A` do roteiro não abrem menu
  nenhum sozinhos, então "chegou no marinheiro" não é suposição.
- `T86.1` **sem `FLAG_SYS_GAME_CLEAR`** fica em `MAP_VERMILION_CITY` (37,5): o
  portão do PASSE TRI vale para as três diagonais de Vermilion, não só para a
  rota de Johto. (Os casos `T4.5` e `T4.6` já guardavam esse controle; o mutante
  só confirmou que ele cobre também as diagonais.)

### Receita para escrever esses casos

A lista `MULTI_CINCO_REGIOES_BARCO` é sempre a mesma:
`0 OLIVINE, 1 SLATEPORT, 2 VERMILION, 3 VIRBANK, 4 CANALAVE, 5 EXIT`
(o item de saída chamava `Sair` até 11/08/2026, quando o texto do barco
passou para inglês; o id 5 não mudou).
O cursor começa em 0 e o menu **não dá a volta**, então o número de `DOWN` é o
próprio índice do destino. Cada porto pula o próprio índice, e é por isso que
sair de Vermilion rumo a Canalave custa 4 DOWN mesmo Vermilion não tendo `case 2`.

Como chegar em cada marinheiro (medido, não chutado):

| porto | warp de debug | roteiro até o marinheiro |
|---|---|---|
| Vermilion | `MAP_VERMILION_CITY` warp 4 | `16:DOWN*4` (o marinheiro em (15,11) trava o passo) |
| Olivine | `MAP_OLIVINE_CITY_PORT_INSIDE` warp 0 | `16:DOWN*12` |
| Slateport | `MAP_SLATEPORT_CITY_HARBOR` warp 0 | `20:UP*2,20:LEFT*10` |
| Canalave | `MAP_CANALAVE_CITY` warp 1 | `20:DOWN*20,20:LEFT*20,20:RIGHT*4,20:UP*12` |
| Virbank | **não aceita warp de debug** | chegar de barco de Canalave, depois `16:RIGHT*5,16:UP` |

O Porto de Virbank não aceita warp de debug porque os três warps dele caem em
cima de outro warp ou fora do mapa 10x8: o warp 0 larga o jogador em (4,8),
abaixo do mapa, e o passo seguinte re-dispara o warp para Virbank City. Por isso
o T10.2 é ida e volta.

Depois de encostar no marinheiro, o diálogo é sempre:
`A` (fala) → `A` (fecha a caixa, o menu abre) → `DOWN` x N → `A` (escolhe) →
`A` (fecha o "Zarpando...") → o warp acontece. Em Vermilion entra antes a
conversa do assistente do Prof. Carvalho, que precisa de 4 `A` e depois `B` para
limpar o que sobrou sem re-disparar o NPC.

**Prioridade:** baixa em jogo (a progressão cronológica só usa as 8 da cadeia),
alta em teste de regressão: as 12 são o que quebra calado quando alguém
acrescentar um sexto destino no meio da lista, e agora existe caso de emulador
para cada uma.

### O que continua aberto

1. **O Porto de Virbank continua sem aceitar warp de debug**, e por isso três
   casos (`T86.10` a `T86.12`, além do `T10.2`) gastam uma travessia inteira de
   Canalave só para chegar lá. Os três warps do mapa 10x8 caem em cima de outro
   warp ou fora do mapa. Consertar é mexer em mapa de Unova, dono de outra
   frente; enquanto não for, o custo é ~4 s por caso, e nenhum resultado muda.
2. ~~**Todo o texto de jogo do barco está em português**, nos cinco portos:
   `VermilionCity_Text_WhereTo` ("Bem-vindo ao Porto de Vermilion City em
   Kanto!"), `VermilionCity_Text_FerrySemPasse`, os quatro
   `..._Text_SettingSailTo*` / `..._Text_Zarpar*` de cada porto e os
   `Text_ParaOnde` / `Text_Volte` de Canalave e de Virbank. A regra do projeto é
   texto de jogo em **inglês**; documentação e comentário é que são em
   português. **Não foi consertado nesta leva de propósito**, por dois motivos:
   dois dos cinco arquivos são mapa de Sinnoh (`CanalaveCity`) e de Unova
   (`Unova_VirbankPort`), de outras frentes; e o número de páginas de cada caixa
   (`\p`) está embutido na contagem de `A` de 20 roteiros de teste já provados,
   então reescrever texto sem re-rodar os 20 casos quebra a suíte calada.
   Quem for traduzir: mantenha uma página por caixa e re-rode `T4`, `T6`, `T8`,
   `T10` e `T86` na build seguinte.~~

   **FECHADO em 11/08/2026, mais tarde no mesmo dia.** Os cinco portos falam
   inglês. Foram junto, porque eram o mesmo defeito e ninguém os tinha listado:
   as quatro falas do assistente do PROF. OAK em Vermilion (`FerrySemPasse`,
   `AssistenteAindaNao`, `AssistenteEntrega`, `AssistenteJaEntregou`), o item
   `Sair` do menu do marinheiro, que virou `EXIT` como todo multichoice do
   pokeemerald (`gText_Exit`, `src/strings.c:532`), e a **balsa interna de
   Sinnoh** entre Snowpoint e a Battle Zone (`SnowpointCity_Text_Sailor*` e
   `FightArea_Text_Sailor*`), que não é uma das cinco travessias entre regiões e
   por isso não estava nesta lista.

   **A contagem de `A` dos 20 roteiros custou uma build para ficar certa, e a
   história vale mais que o resultado.** A primeira versão da tradução usou três
   linhas nos cinco `Text_WhereTo` (`...\n...\l...`) e uma no texto do assistente,
   convencida de que só `\p` cobra aperto de botão e que `\l` apenas rola a
   linha. Um verificador foi escrito antes de buildar, comparou o número de `\p`
   de cada `.string` contra o `HEAD` rótulo a rótulo, e deu **zero divergência**:
   verde, e errado. **`\l` é `CHAR_PROMPT_SCROLL` e `\p` é `CHAR_PROMPT_CLEAR`;
   os dois são PROMPT e os dois param esperando A.** Só `\n` passa direto.

   Quem pegou foi a suíte, na build: **9 casos reprovados, e exatamente os 9 que
   atravessam porto** (T4.2, T6.2, T8.2, T8.3, T8.5, T10.1 a T10.4), cada um
   parando um `A` antes, no porto de origem. O conjunto das falhas ser
   exatamente o conjunto dos casos de barco é o que fecha o diagnóstico: não
   sobrou um caso de outro assunto para explicar.

   Consertado tirando o `\l` dos seis textos (as duas linhas ficaram
   "Welcome to VERMILION CITY, KANTO!" e "Where would you like to sail?"), e o
   verificador passou a contar **`\p` E `\l`**, que é a pergunta que ele devia
   estar fazendo desde o começo. As linhas ficaram em no máximo 34 caracteres,
   medido contra a régua do vanilla de Hoenn (p95 de 38, máximo 45), pela lição
   4.2: quem discorda do jogo original é a régua.

   O que dois dos cinco arquivos serem de outra frente (`CanalaveCity` de Sinnoh
   e `Unova_VirbankPort` de Unova) impedia era mexer em `object_events` do
   `map.json` deles, e não no `scripts.inc`, que é onde o texto mora.
3. ~~As três `FLAG_REGIAO_*_LIBERADA` estão reservadas e NÃO estão ligadas em
   lugar nenhum.~~ **FECHADO em 11/08/2026, mais tarde no mesmo dia.** O menu
   dos cinco portos deixou de ser a lista estática `MULTI_CINCO_REGIOES_BARCO` e
   passou a ser montado em `data/scripts/travessia_regioes.inc`, escondendo o
   destino da região que ainda não foi liberada. **Zero flag nova e zero var:**

   | destino | porteiro | quem acende |
   |---|---|---|
   | VERMILION (Kanto) | nenhum, é a região inicial | — |
   | OLIVINE (Johto) | `FLAG_REGIAO_JOHTO_LIBERADA` | campeão de Kanto, `PokemonLeague_ChampionsRoom_Frlg` |
   | SLATEPORT (Hoenn) | `FLAG_REGIAO_HOENN_LIBERADA` | Clair, 8ª insígnia de Johto, `BlackthornCity_Gym` |
   | CANALAVE (Sinnoh) | `FLAG_REGIAO_SINNOH_LIBERADA` | Wallace, campeão de Hoenn, `EverGrandeCity_ChampionsRoom` |
   | VIRBANK (Unova) | `FLAG_ELITE_SINNOH_VENCIDA` | Cynthia, que já acendia essa flag |

   **Johto é a exceção declarada, e não é descuido:** esta ROM não tem uma Elite
   dos Quatro de Johto (a Liga de gen 2 é o mesmo Planalto Índigo de Kanto, que
   aqui são os mapas `PokemonLeague_*_Frlg`). O fim de Johto que existe de
   verdade é a oitava insígnia, então é ela que abre Hoenn.

   **Nenhum `case` dos cinco portos mudou.** `dynmultipush NOME, ID` empilha a
   opção com um id PRÓPRIO, e o `dynmultistack` devolve esse id em `VAR_RESULT`,
   não a linha escolhida (`src/scrcmd.c:1884` grava `item.id`;
   `Task_HandleScrollingMultichoiceInput` em `src/script_menu.c` grava
   `gSpecialVar_Result = input`, que é o id). Os ids seguem sendo 0 OLIVINE,
   1 SLATEPORT, 2 VERMILION, 3 VIRBANK, 4 CANALAVE, 5 Sair.

   **O que MUDA é a contagem de `DOWN`**, porque a lista encolhe: o número de
   DOWN passa a ser a posição do destino DENTRO da lista já filtrada. Os 24 casos
   de emulador que atravessam porto (T4.2, T4.4, T4.5, T4.6, T6.2, T8.2, T8.3,
   T8.5, T10.1 a T10.4 e T86.1 a T86.12) ganharam as quatro flags de liberação no
   campo `flags`, o que devolve o menu cheio de seis itens e mantém válido cada
   roteiro já provado. **Nenhum roteiro de botão foi reescrito.**

   `dev_scripts/valida_barco.py` foi reescrito para ler o menu novo: confere os
   ids empilhados, o porteiro de cada destino e que cada flag é acesa por alguém.
   Três mutantes rodados, três reprovações no ponto previsto (id de CANALAVE
   trocado para 3; porteiro de Canalave removido; `setflag` da Clair removido).

   **O portão ganhou prova de emulador em 11/08/2026**, em
   `dev_scripts/testes_criticos/87_portao_regioes.json`, rodada na ROM do commit
   `6a796d4ad3`. Os 24 casos acima acendem as quatro flags de propósito, então
   eles provam a ROTA e não o portão: um portão que ignorasse a flag passaria
   inteiro neles. Os cinco casos novos fecham isso:

   | caso | estado das flags | roteiro | `location` no fim |
   |---|---|---|---|
   | T87.1 | jogo novo, nada escrito | — | `FLAG_SINNOH_NPC_DUPLICADO` acesa, as três `FLAG_REGIAO_*` apagadas |
   | T87.2 | só `FLAG_SYS_GAME_CLEAR` | o do T86.2, **4 DOWN** | fica em `MAP_VERMILION_CITY`, e ANDOU dentro dele |
   | T87.3 | só Sinnoh liberada | **1 DOWN** | `MAP_CANALAVE_CITY` (com as quatro flags, esse mesmo 1 DOWN é SLATEPORT: T86.1) |
   | T87.4 | só Sinnoh liberada | **3 DOWN**, o índice de VIRBANK | fica em `MAP_VERMILION_CITY` |
   | T87.5 | só Johto liberada | o do T6.2, **1 DOWN** | `MAP_SSAQUA_1F` (com as quatro flags, esse mesmo 1 DOWN é SLATEPORT: T6.2) |

   O T87.3 e o T87.5 são o que separa "filtra por flag" de "esconde tudo": mesmo
   porto, mesmo aperto de botão, mapa final diferente conforme a flag. O T87.4 é
   o bug original em forma de teste (Kanto direto para Unova no começo).

   **Os cinco passaram de primeira, então foram rodados contra uma ROM mutante**,
   buildada numa worktree isolada com duas mutações somadas: os quatro
   `call_if_set` do menu viraram `call` (o menu ignora as flags) e o `setflag
   FLAG_SINNOH_NPC_DUPLICADO` saiu do jogo novo. **0 de 5 passaram, cada um
   falhando exatamente onde a mutação prevê:** T87.2 desembarcou em Canalave,
   T87.3 em Slateport, T87.4 em `MAP_UNOVA_VIRBANK_PORT` (o bug original vivo na
   tela), T87.5 em Slateport, e o T87.1 leu a flag do clone apagada.

   **O que continua sem prova de emulador, e por quê:** os três `setflag` que
   ACENDEM as flags (campeão de Kanto, Clair, Wallace). Todos os três só rodam
   depois de uma batalha vencida, e isso está fora do alcance deste banco de
   teste: medido em 11/08/2026 com uma sonda descartável, depois da abertura o
   jogador tem **zero Pokémon**, então o caso teria que escolher inicial, montar
   um time capaz de derrubar um campeão na curva da região e ganhar um 6x6 no
   braço, às cegas. Batalha decidida a marteladas de `A` é teste instável, e a
   lição 4.3 diz que falso positivo é pior que validador nenhum. O substituto,
   declarado e não calado, está em `valida_barco.py`: ele exige que cada
   `setflag` exista E que apareça **depois** da batalha âncora daquele mapa
   (`TRAINER_WALLACE`, `TRAINER_JOHTO_LEADER_CLAIR`,
   `PokemonLeague_ChampionsRoom_EventScript_Battle`). Mutante rodado: movendo o
   `setflag` do Wallace para antes do `trainerbattle`, o validador reprova.

A travessia continua não gastando var nenhuma, e os 12 casos novos são só JSON
de teste: sem flag, var, id de treinador, mapa, warp ou objeto novo. A faixa
0x881 a 0x887, reservada para esta frente, **voltou inteira**.

---

## 2. O canal de Canalave é caminhável, e o cais é uma ilha

Achado em 05/08/2026 ao provar Hoenn → Sinnoh. **Não consertei de propósito: é
`data/layouts/CanalaveCity/map.bin`, arquivo do import de Sinnoh, não meu.**

O barco desembarca em (17,49) e o marinheiro Eldritch fica em (17,48). Os dois
estão **dentro do canal**: os tiles x=16..20 são desenhados como água e têm
`colisão 0`, com a mesma `elevação 1` do chão que o jogador anda no resto da
cidade. Resultado na tela: o jogador e o NPC ficam em pé sobre a água.

```
     x=12    13      14      15      16      17      18      19      20     21
y=46 c0e3   c0e3    c0e3    c0e3  | c0e1    c0e1    c0e1    c0e1 |  c1e0   c0e3
y=47 c0e3   c0e3    c0e3    c0e3  | c0e1    c0e1    c0e1    c0e1 |  c1e0   c0e3
y=48 c0e3   c1e0    c0e1    c0e1  | c0e1   [NPC]   c0e1    c0e1  |  c1e0   c0e3
y=49 c0e3   c1e0    c0e1    c0e1  | c0e1  [barco]  c0e1    c0e1  |  c1e0   c0e3
                                    ^--------- o canal ---------^
```

O cais de verdade é o retângulo de **elevação 3** em (13..15, 46..47), ligado à
margem oeste. Mas ele é **isolado por elevação** do chão `e1` onde o jogador
anda: mover o marinheiro para o cais tornaria o porto inalcançável, porque não
existe tile de transição (elevação 0 ou 15) entre `e1` e `e3` ali. Por isso o
marinheiro fica onde está.

**Conserto, no dono do layout:** dar `colisão 1` aos tiles do canal
(x=16..20 em toda a faixa y=40..55) e abrir uma transição de elevação no cais,
depois mover o marinheiro para (15,47) e o desembarque para (14,47). Os
roteiros de T8.3, T8.5, T10.1 e T10.2 precisam ser re-derivados junto, porque
todos hoje atravessam o canal a pé.
