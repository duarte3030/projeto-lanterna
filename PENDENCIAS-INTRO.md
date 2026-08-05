# Pendências da abertura de Sinnoh

Escrito pela sessão que montou o começo do jogo (Twinleaf → Rota 201 → Sandgem →
laboratório do Rowan → escolha do inicial). Tudo aqui é coisa que **não** podia
ser feita nesta tarefa porque o arquivo estava com outro agente, ou porque exigia
flag/var nova. Quem orquestra registra.

Nada nesta lista bloqueia o build ou a jogabilidade: a abertura funciona sem
nenhum destes itens.

## 1. O laboratório do Rowan está morando dentro de `SandgemTown_House1`

Sinnoh não tem mapa próprio de laboratório. Criar um exigiria uma entrada nova em
`data/layouts/layouts.json` e outra em `data/maps/map_groups.json`, e os dois
estavam proibidos nesta tarefa. Solução: `MAP_SANDGEM_TOWN_HOUSE1` (a casa comum
de Sandgem, 10x9) virou o laboratório, com Rowan, a assistente Roseanne, Barry e
as três Poké Bolas.

Consequência visível, e é a única feia da entrega: **as duas portas de Sandgem
que davam em casas levam agora ao mesmo laboratório.** O warp 0 (o prédio grande
em 9,8, que é o laboratório de verdade) e o warp 3 (a casinha em 7,20) apontam
ambos para `MAP_SANDGEM_TOWN_HOUSE1`, warp 0. Sair do laboratório sempre devolve
o jogador à porta do laboratório.

Conserto, quando `layouts.json` e `map_groups.json` liberarem:

1. criar `data/maps/SandgemTown_RowanLab/` com layout próprio (o layout de
   laboratório mais parecido que já existe no repo é
   `LAYOUT_NEW_BARK_TOWN_LAB`, 40x14, ou `LAYOUT_PALLET_TOWN_LAB`, 32x28);
2. registrar o mapa em `gMapGroup_IndoorSandgem`;
3. mover para lá, sem mudar uma linha, o conteúdo de
   `data/maps/SandgemTown_House1/scripts.inc` e os seis `object_events` do
   `map.json` (só trocar o prefixo dos rótulos e os `LOCALID_ROWAN_LAB_*`);
4. apontar o warp 0 de `SandgemTown/map.json` para o mapa novo e devolver o warp
   3 (7,20) para `MAP_SANDGEM_TOWN_HOUSE1` com `dest_warp_id` 3, que é como
   estava antes;
5. devolver a `SandgemTown_House1` os dois criadores de Pokémon que moravam lá
   (`LOCALID_HOUSE1_BREEDER_M` e `_F`, textos no histórico do git).

O antigo warp de Sandgem apontava para `MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB`
(o laboratório do Birch, em Hoenn). Isso estava quebrado: entrar por Sandgem e
sair jogava o jogador em Littleroot, e os scripts daquele mapa são a introdução
de Hoenn inteira, incluindo o upgrade da Pokédex de Johto. Foi por isso que ele
não foi reaproveitado.

## 2. Flags que não foram criadas (e por que não fizeram falta)

`include/constants/flags.h` estava com outro agente, então nenhuma flag nova foi
criada. Nenhuma foi necessária:

| O que precisava de memória | O que foi usado no lugar |
|---|---|
| esconder as três Poké Bolas depois da escolha | `FLAG_SYS_POKEMON_GET` no campo `flag` dos três `object_events` (o objeto nem nasce com a flag ligada) |
| Rowan, Barry e a mãe mudarem de fala depois do inicial | `goto_if_set FLAG_SYS_POKEMON_GET` |
| a mãe só dar os Tênis de Corrida uma vez | `FLAG_SYS_B_DASH`, que é a própria flag dos tênis |
| ter Pokédex | `FLAG_SYS_POKEDEX_GET` |

**Zero var gasta.** As ~22 vars que sobram no jogo continuam intactas.

Se um dia alguém quiser a cena completa do Platinum (Barry sobe até o quarto, os
dois são parados pelo Rowan na Rota 201, a maleta cai no Lago Verity), aí sim
vai precisar de **uma** var de estado, no molde de `VAR_BIRCH_LAB_STATE`.
Sugestão de nome: `VAR_ROWAN_INTRO_STATE`. Não foi gasta agora porque a versão
enxuta (escolher no laboratório) não precisa dela.

## 3. Cena do Platinum que ficou de fora

No jogo original a escolha do inicial acontece **na Rota 201**, com a maleta do
Rowan, depois de Barry tentar atravessar a grama sem Pokémon. Aqui o jogador
escolhe **dentro do laboratório**, em Sandgem, que é o que a tarefa pedia.

`data/maps/Route201/` não estava sob esta tarefa, então a rota continua com os
três NPCs de sempre e nenhuma cena. O texto original da cena existe pronto em
`fontes-mapas/pokeplatinum/res/text/route_201.json` para quem for montá-la; as
falas do Rowan que hoje estão no laboratório vieram exatamente de lá.

Também ficaram de fora, por serem de arquivos de outros agentes ou por exigirem
personagem novo: Lucas/Dawn (o assistente do professor que guia o jogador por
Sandgem), o Journal, e a TM Return que o Rowan dá na saída.

## 4. Nada obriga o jogador a pegar o inicial

Dá para sair de Twinleaf, atravessar a Rota 201 e chegar a Jubilife sem falar com
o Rowan. Não trava nem quebra nada (ver item 5), o jogo só fica sem graça.

No Platinum quem segura é a cena da Rota 201. Quando ela existir (item 3), o
bloqueio vem junto de graça.

## 5. Guarda de segurança posta em `src/wild_encounter.c`

`StandardWildEncounter()` ganhou três linhas:

```c
if (gPartiesCount[B_TRAINER_PLAYER] == 0)
    return FALSE;
```

Motivo: em Hoenn o jogador nunca pisa na grama antes do inicial, porque a
história não deixa. Em Sinnoh a Rota 201 fica **entre** a casa do jogador e o
laboratório, e a grama está lá, alcançável a pé, antes de existir qualquer
Pokémon no time. Sem a guarda, pisar nela iniciava uma batalha com time vazio.

O arquivo não estava na lista de proibidos (o proibido era
`src/data/wild_encounters.json`, que não foi tocado). A guarda é única e fica no
ponto por onde todo encontro aleatório passa, em vez de espalhada por mapa.

## 6. A tela de nome e gênero ainda é a do Emerald

`DEV_SKIP_INTRO FALSE` devolve a tela de introdução do Emerald, que é onde o
jogador escolhe gênero e digita o nome. Nenhuma UI nova foi escrita, como pedido.

O que mudou: `data/text/birch_speech.inc` teve o **texto** trocado pelas falas do
Rowan em Platinum (`res/text/rowan_intro.json`). Os símbolos continuam
`gText_Birch_*` porque `src/main_menu.c` os chama por nome, e renomear obrigaria
a mexer em `include/strings.h`, que não é desta tarefa.

O que **não** mudou, e é o que ainda destoa:

- o retrato do professor na tela é o do Birch (`graphics/birch_speech/`). Rowan
  não tem retrato no repo;
- o Pokémon que aparece na fala é um Lotad, não um Starly;
- o Platinum pergunta também o nome do rival, e essa tela não existe no Emerald.
  Barry aparece sem nome escolhido pelo jogador.

## 7. Ponto de cura inicial

`NewGameInitData()` agora chama `SetLastHealLocationWarp(HEAL_LOCATION_SANDGEM_TOWN)`,
que é o Centro Pokémon de Sandgem, o primeiro que o jogador alcança. No Platinum
o ponto inicial é a casa da mãe em Twinleaf; para copiar isso seria preciso uma
entrada nova em `src/data/heal_locations.json`
(`HEAL_LOCATION_TWINLEAF_TOWN_MAIN_HOUSE_1F`), que não foi criada.

## RESOLVIDO: o laboratorio do Rowan ganhou mapa proprio (05/08/2026, bloco 6)

`MAP_SANDGEM_TOWN_ROWAN_LAB` existe, e o item 1 desta pagina esta fechado.

| o que era | o que e |
|---|---|
| laboratorio dentro de `SandgemTown_House1`, layout de casa 10x9 | mapa proprio `SandgemTown_RowanLab`, `LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB` (13x13) |
| as duas portas de Sandgem entravam no MESMO interior | warp 0 vai ao laboratorio, warp 3 vai a casa |
| a casa nao existia mais | os dois criadores voltaram, com os textos do commit f97a18dc82 |

Decisoes, e o porque de cada uma:

- **Layout emprestado de Hoenn, nao desenhado.** O interior do laboratorio do
  Birch ja esta na ROM, ja tem bancada, estante e maquina, e nao custa nem um
  byte de blockdata novo. Desenhar um laboratorio de Sinnoh do zero seria arte
  inventada para um problema que arte existente resolve.
- **Mapa novo no FIM de `gMapGroup_IndoorSandgem`**, depois de `SandgemTown_Mart`.
  A save guarda `(mapGroup, mapNum)`, que sao INDICES: inserir no meio empurraria
  o Mart e os dois andares do Centro Pokemon para outro numero.
  `guarda_save.py` diz SAVE COMPATIVEL depois da mudanca.
- **Nenhuma flag e nenhuma var novas.** O script mudou de arquivo e de rotulo
  (`SandgemTown_House1_*` virou `SandgemTown_RowanLab_*`), mais nada: continua
  usando `FLAG_INICIAL_SINNOH`, `FLAG_SYS_POKEDEX_GET` e `VAR_STARTER_MON`.

Posicoes novas, no layout do laboratorio: Rowan (6,4), Barry (7,4), Roseanne
(9,8), as tres Poke Bolas em (5,8), (6,8) e (7,8), as duas portas em (6,12) e
(7,12), as duas estantes em (3,1) e (4,1).

Provado na ROM, lendo a EWRAM (`dev_scripts/testes_criticos/70_polimento.json`):

- **T40.3**: o mapa carrega e o layout lido da memoria e o do laboratorio.
- **T40.4**: prova NEGATIVA. Entrar em `SandgemTown_House1`, andar ate o meio da
  sala e martelar A deixa o time em 0 e `FLAG_INICIAL_SINNOH` apagada, ou seja,
  o laboratorio realmente saiu de la.
- **T20.3**, o caso do bloco 4, continua passando com o mapa novo: a bola do meio
  entrega CHIMCHAR e escreve `VAR_STARTER_MON = 1`.

Continua de fora, e nao bloqueia nada: a cena da Rota 201 (item 3), o Lucas/Dawn,
o Journal e a TM Return.
