# Estado do hack, e como trabalhar nele

Ponto de entrada. Leia este arquivo antes de qualquer coisa; ele diz onde o
projeto está, o que já foi decidido, e as armadilhas que já custaram sessões
inteiras. Detalhe fica nos documentos apontados no fim.

Última medição: 06/08/2026.

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
| ROM | **94,43% de 32 MB** (1,78 MB livres) |
| EWRAM / IWRAM | 85,57% / 86,62% |
| SaveBlock1 | **13432 de 15872 B (84,6%)** |
| flags livres no pool | **184** (eram 288 antes de ligar as de Kanto) |
| mapas | **1870** |
| treinadores com time próprio | **2346** |
| grupos de mapa | **126** (teto duro de **128** grupos e **128 mapas por grupo**: `s8` em `struct WarpData`; passar disso mata o mapa) |
| suíte de testes | **107 de 110** (1 pulado precisa de duas builds; 2 reprovados são de Unova) |
| teto de treinador | `MAX_TRAINERS_COUNT_EMERALD` = 3000 |

### Completude contra a fonte de cada região

100% = tão completo quanto o jogo de onde a região veio. Rode
`python3 dev_scripts/completude.py`.

| região | mapas | objetos | warps | placas |
|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100,0% | 100,0% |
| Johto | **95,9%** | 94,0% | 100,0% | 96,0% |
| Hoenn | 100,0% | 100,1% | 100,0% | 100,0% |
| Sinnoh | **66,7%** | 80,3% | **99,0%** | 98,3% |
| Unova | 94,2% | 98,3% | 98,9% | 98,0% |

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
| 93,2% | 91,2% | 95,8% | 78,6% | 79,4% |

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
| 13 | As 152 "placas" de Sinnoh que na verdade são item escondido **ficam como estão**: não viram item nem são apagadas agora. Não gastar o pool de flags nisso |
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

**A janela de quebrar save de graça fecha quando o Gui receber a primeira build
que ele vá jogar de verdade.** Até lá, quebra é aceitável se for deliberada e
registrada. Quatro já foram feitas nesta sessão.

---

## 6. Faixas de id de treinador em uso

| faixa | dono |
|---|---|
| 1367-1379 | Unova, chefes |
| 1400-1799 | Kanto |
| 1800-2147 | Unova, rota |
| 2200-2273 | Kanto, segunda leva |
| 2274-2417 | Johto, rota |
| **2418-2999** | **livre** |

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
| `liga_flags_kanto.py` | Tira do stub só a flag que algum script mexe |

As cinco fontes ficam em `../fontes-mapas/`: `pokeemerald`, `pokefirered`,
`hns` (Johto), `sinnoh` e `pokeplatinum` (Sinnoh), `bw3g` (Unova). O BW3G morava
em `/tmp` e foi movido em 05/08/2026, porque `/tmp` é limpo pelo sistema e seis
scripts liam de lá.

---

## 8. O que falta, em ordem de tamanho

1. **Sinnoh, mapas em 51,0%.** Continua o maior buraco, mas o caminho agora está
   medido. O que falta se divide em tres: (a) 12 cavernas com a geometria JÁ
   convertida e conferida, paradas só por falta de tile de porta órfã no mapa
   pai (Old Chateau, Solaceon Ruins, Rock Peak Ruins, Maniac Tunnel, Mt. Coronet
   6F, as duas Low Water de lago); (b) 11 interiores de cidade, sendo 4 deles
   presos a layout compartilhado que precisa ser clonado; (c) o resto do mapa de
   DS que ainda nem foi tocado (Great Marsh, Distortion World, Turnback Cave,
   Battle Frontier, andares de hotel e de loja), que tem mobília desenhada e por
   isso a grade 2D não basta. Ver secoes 8 a 10 de `PENDENCIAS-NPC-SINNOH.md`.
   O `fontes-mapas/sinnoh`, que é GBA e seria barato, só tem 133 mapas próprios
   de Sinnoh e **todos os 133 já estão na ROM**: dessa fonte não sobra nada.
2. **Sinnoh, o resto dos NPCs.** 1119 objetos hoje. Ficaram de fora 230 com
   `hidden_flag` (NPC de história: sem o script que os remove, viram bloqueio
   permanente, como as 39 pedras de Strength de Unova), 84 `coord_events` e 71
   sem sprite honesto (Cynthia, Cyrus, Looker, os lendários de lago). Ver
   `PENDENCIAS-NPC-SINNOH.md`.
3. **152 "placas" de Sinnoh não são placa: são item escondido.** O `script`
   delas no Platinum é 8000 ou mais, que é a faixa `SCRIPT_ID_OFFSET_HIDDEN_ITEMS`
   (`include/script_manager.h:96`); a tabela com item, quantidade e raio está em
   `include/data/field/hidden_items.h`. Hoje o jogador lê "the lettering has
   faded" em cima de um item invisível. Virar item de verdade custa **uma flag
   por item, 152 das 184 livres**: é gasto do pool inteiro e precisa da decisão
   do Gui.
4. **Unova, 23% das placas** (117, sendo 55 delas máquinas do Game Corner),
   209 cenas de enredo e 264 NPCs mudos. Ver `PLANO-UNOVA.md`.
5. **426 flags de Kanto seguem em `0`**, e isso está certo: elas não são mexidas
   por script nenhum, então dar número a elas não mudaria nada em jogo. As 104
   que importavam saíram do stub em 05/08/2026
   (`dev_scripts/liga_flags_kanto.py`).
6. **12 diagonais de barco** não jogadas em ROM. Ver `PENDENCIAS-TRAVESSIA.md`.
7. **Ninguém jogou do começo ao fim.** Tudo aqui é build, dado estático e
   emulador em ponto específico.

**O aperto de ROM que este documento anunciava não existia.** Os "93 KB de
margem" eram a distância até uma linha de 95% que eu mesmo inventei como aviso,
não até o teto de 32 MB. Livres de verdade: **1,98 MB**. Unova completa cabe, o
resto de Sinnoh cabe, as placas de Johto couberam.

---

## 9. Onde está o resto

| documento | assunto |
|---|---|
| `PRD-CINCO-REGIOES.md` | Plano por blocos, decisões, desenho dos testes |
| `HANDOFF-2026-08-05.md` | O caso Kanto em detalhe, as oito camadas |
| `PLANO-UNOVA.md` | Unova: o que entrou, o que falta, e por quê |
| `PENDENCIAS-TRAVESSIA.md` | Barco entre regiões, o que foi provado e o que não |
| `PENDENCIAS-JOHTO.md`, `PENDENCIAS-INTRO.md`, `PENDENCIAS-GALACTICA.md` | Pendências por frente |
| `SINNOH-PADRAO.md` | Padrões de script que economizam var |
| `RECURSOS-REGIOES.md` | Fontes avaliadas, com o veredito medido de cada |
| `DEMAKE-DS.md` | Formato de mapa de gen 4 e gen 5 |
