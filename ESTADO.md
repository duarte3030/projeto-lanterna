# Estado do hack, e como trabalhar nele

Ponto de entrada. Leia este arquivo antes de qualquer coisa; ele diz onde o
projeto está, o que já foi decidido, e as armadilhas que já custaram sessões
inteiras. Detalhe fica nos documentos apontados no fim.

Última medição: 11/08/2026, na build do commit `8f4013c807`.

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
| teto de treinador | `MAX_TRAINERS_COUNT_EMERALD` = **2500** (`include/constants/opponents.h:2020`, lido em 11/08/2026; este documento dizia 3000). Maior id declarado: **2440**. Livres: **2441 a 2499, ou seja 59**, e **subir o teto agora quebra a save do Gui**, porque `SYSTEM_FLAGS` deriva de `TRAINER_FLAGS_END` |

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

**A janela de quebrar save está FECHADA** desde 05/08/2026 (ver a decisão 14 na
seção 3). Este parágrafo dizia que ela "fecha quando o Gui receber a primeira
build", no presente, mesmo depois de ela já ter fechado, e as duas frases
conviveram no mesmo documento por seis dias.

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
| **2441-2499** | **livre: 59 ids, e é tudo que existe** |

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
| `curva_de_nivel.py` | Mede e remapeia nível por região |
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
