# Estado do hack, e como trabalhar nele

Ponto de entrada. Leia este arquivo antes de qualquer coisa; ele diz onde o
projeto está, o que já foi decidido, e as armadilhas que já custaram sessões
inteiras. Detalhe fica nos documentos apontados no fim.

Última medição: 05/08/2026.

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
| ROM | **94,71% de 32 MB** (93 KB de margem) |
| EWRAM / IWRAM | 85,56% / 86,62% |
| SaveBlock1 | **13496 de 15872 B (85,0%)** |
| mapas | **1616** |
| treinadores com time próprio | **2346** |
| grupos de mapa que carregam | **101 de 101** |
| suíte de testes | **106 de 107** (o pulado precisa de duas builds) |
| teto de treinador | `MAX_TRAINERS_COUNT_EMERALD` = 3000 |

### Completude contra a fonte de cada região

100% = tão completo quanto o jogo de onde a região veio. Rode
`python3 dev_scripts/completude.py`.

| região | mapas | objetos | warps | placas |
|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100,0% | 100,0% |
| Johto | 63,6% | 93,9% | 100,0% | **6,8%** |
| Hoenn | 100,0% | 100,1% | 100,0% | 100,0% |
| Sinnoh | 25,6% | 88,0% | 61,8% | 107,6% |
| Unova | 85,4% | 98,5% | 98,8% | 76,0% |

Hoenn dando exatamente 100% é o **controle**: nossa Hoenn é o vanilla intocado,
então tem que dar 100. Se der outra coisa, a ferramenta está errada.

Sinnoh caiu de "100% / fonte 0" para estes números em 05/08/2026, e **isso é
bom**: a régua mudou, não o jogo. Antes era medida contra `fontes-mapas/sinnoh`,
que tem os mapas mas ZERO NPC de Sinnoh. Agora é contra o `pokeplatinum`, que
cobre muito mais mapa do que importamos. Os objetos foram de 528 para **1119**
de verdade; o 25,6% é a medida honesta aparecendo pela primeira vez.

### Warps que disparam de verdade

`python3 dev_scripts/valida_warp_tile.py --piso 60`

| Hoenn | Johto | Sinnoh | Unova | Kanto |
|---|---|---|---|---|
| 93,2% | 90,9% | 86,0% | 78,6% | 69,9% |

**Nunca chega a 100%, e não deve.** Warp só dispara se o tile embaixo tiver
comportamento de porta; muita porta é trocada por `setmetatile` em tempo de
execução, e muito warp é usado só por barco ou cutscene. Hoenn é a régua.

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

---

## 8. O que falta, em ordem de tamanho

1. **Johto, placas em 6,8%.** Letreiros e avisos nunca foram importados do
   `hns`. Maior buraco do painel e o mais barato de fechar.
2. **Sinnoh, o resto dos NPCs.** 1119 objetos hoje. Ficaram de fora 230 com
   `hidden_flag` (NPC de história: sem o script que os remove, viram bloqueio
   permanente, como as 39 pedras de Strength de Unova), 84 `coord_events` e 71
   sem sprite honesto (Cynthia, Cyrus, Looker, os lendários de lago). Ver
   `PENDENCIAS-NPC-SINNOH.md`. As 425 placas importadas dizem todas
   "The lettering has faded with age."; o texto de verdade exige portar os
   bancos de mensagem de Sinnoh.
3. **Unova, 14,6% dos mapas e 24% das placas**, mais 209 cenas de enredo e 264
   NPCs mudos. Ver `PLANO-UNOVA.md`.
4. **~530 flags de Kanto valem `0`**, então todo objeto escondido por flag nasce
   sempre: Pokébolas do laboratório reaparecem, fósseis, Rockets, Bill.
5. **ROM em 94,71%, com 93 KB de margem.** É o limite mais próximo hoje. Antes
   de mandar mais conteúdo entrar, medir onde dá para cortar.
6. **12 diagonais de barco** não jogadas em ROM. Ver `PENDENCIAS-TRAVESSIA.md`.
7. **Ninguém jogou do começo ao fim.** Tudo aqui é build, dado estático e
   emulador em ponto específico.

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
