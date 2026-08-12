# PRD: terminar a ROM inteira

Documento de trabalho para o objetivo "acabar o hack". Escrito em 11/08/2026 e
redirigido ao Fable em 12/08/2026, sobre o commit `268514a116`. Tudo que está
aqui como número foi **medido nesta árvore**, e cada bloco diz com qual comando
remedir. Número sem comando ao lado é suspeito e deve ser remedido antes de
virar plano.

Leia `ESTADO.md` antes deste arquivo. Ele é o ponto de entrada e tem as
armadilhas; este aqui é só o plano.

---

## 0. Para o Fable: você é o arquiteto, e este documento é réu

**Este PRD foi escrito por agentes Opus e Sonnet, e o projeto inteiro também.**
Milhares de mapas, dezenas de ferramentas, cinco regiões, tudo produzido por
sessões que se sucederam sem memória uma da outra. O Gui te chamou porque a
decisão daqui pra frente é de arquitetura, tem trade-off caro em quase toda
escolha, e ele quer alguém julgando a estratégia antes de mais alguém executá-la.

**Seu papel, na ordem:**

1. **Revisar este PRD contra a árvore, não aceitar.** Trate cada número aqui
   como afirmação de terceiro, porque é. O histórico deste projeto justifica a
   desconfiança, e não é hipérbole:
   - O `ESTADO.md` afirmou teto de treinador errado (3000, real 2500) e duas
     frentes de trabalho receberam faixa de id inválida no mesmo dia.
   - O `ESTADO.md` afirmou a janela de save aberta e fechada em dois parágrafos
     do mesmo arquivo, por seis dias.
   - `completude.py` deu 94 a 98% para Unova, que é **maquete de colisão em duas
     cores**. Ninguém percebeu até o Gui jogar e desconfiar. Ver a seção 4.
   - `guarda_save.py`, o guarda que protege a save do usuário, deu
     "SAVE COMPATIVEL" em 12/08 para uma mudança que crescia o SaveBlock1 em 187
     bytes. Foi consertado no mesmo dia, e o conserto está no docstring dele.
   O padrão que se repete: **métrica que mede existência dá verde em trabalho
   oco.** Quando você for revisar aceite de bloco, pergunte sempre o que a
   métrica NÃO vê.

2. **Julgar a estratégia, que é onde estão os trade-offs.** A seção 10 lista os
   que já conheço, com a conta de cada um. Se algum estiver mal resolvido, é
   melhor descobrir antes de gastar agente. Você pode reescrever bloco,
   reordenar, fundir, matar. O documento é seu depois desta leitura.

3. **Delegar o que você conferiu**, pelo skill `fable-distribuido`: você escreve
   prompt e julga resultado, os agentes leem repositório e escrevem código.
   Executor padrão `opus`; `sonnet` para varredura e conversão mecânica.
   Não delegue bloco cuja abordagem você ainda não validou: aqui, agente com
   abordagem errada produz mil arquivos errados, e já produziu.

4. **Ser o pai de todo mundo.** Nenhum agente decide teto, ordem de região,
   política de conteúdo, ou o que entra na ROM. Dúvida de agente sobe pra você;
   dúvida que envolve dinheiro, gosto, prioridade ou ação irreversível sobe pro
   Gui, no formato da REGRA ZERO (resposta curta primeiro, bloco
   `**Preciso de voce:**` no fim, numeração contínua, hoje na pergunta 14).

**O que já está decidido pelo Gui e você NÃO reabre** (pode discordar e dizer,
mas não mude sozinho): passar de 32 MB é permitido e é o plano; a save de hoje é
descartável e a da entrega de hoje não; teto de treinador em 4000; a política de
conteúdo da seção 2; a ordem da arte de Unova (Castelia, Nimbasa, Driftveil,
Opelucid).

**Como economizar você mesmo:** não leia mapa, `scripts.inc` nem blockdata. Todo
número deste PRD tem comando ao lado; mande um agente `sonnet` rodar e voltar só
com o número. Se você estiver lendo arquivo grande, a divisão de trabalho falhou.

---

## 1. Objetivo

Um cartucho de GBA com **cinco regiões jogáveis do começo ao fim**, cada uma tão
completa quanto o jogo de onde veio: mapas, NPCs com fala, treinadores
batalháveis, ginásios populados, história, itens e encontros selvagens.

**Pronto** significa, para cada região, as cinco linhas abaixo verdes ao mesmo
tempo. Nenhuma delas é opinião:

| # | critério | como se mede |
|---|---|---|
| P1 | Mapas, objetos, warps e placas em 100% da fonte, ou com motivo nomeado para cada ausência | `completude.py`, e a lista de exceções neste PRD |
| P2 | Todo treinador da fonte existe aqui, é batalhável e tem time próprio | bloco B4 |
| P3 | Todo NPC fala o que fala na fonte | bloco B2 |
| P4 | A história roda do início ao Hall da Fama sem bloqueio | bloco B6 e B11 |
| P5 | Encontro selvagem em todo mapa que tem na fonte | bloco B7 |

---

## 2. Política de conteúdo, decidida pelo Gui em 11/08/2026

**Pode remover tudo que não faz parte da história original.** NPC inventado por
sessão anterior, fala escrita à mão que não existe na fonte, treinador duplicado
criado fora da fonte: sai, e sai sem pedir autorização caso a caso.

**Não pode remover história inteira de outro jogo.** O hack é "um pedaço de
cada": o que veio de `pokefirered`, `hns`, `pokeemerald`, `pokeplatinum` e
`BW3G` é conteúdo legítimo e fica. A régua é a **fonte**, não a origem do
commit.

Regra operacional que sai disso, e vale para todo bloco:

1. Se existe na fonte, fica, e tem que estar igual à fonte.
2. Se não existe na fonte e é enfeite inventado aqui, sai.
3. Se não existe na fonte mas tapa um buraco de sistema que a ROM precisa
   (curador de loja, enfermeira, marinheiro da travessia entre regiões), fica, e
   entra na lista de exceções deliberadas no fim deste documento.
4. **Remover é esconder atrás de flag, não apagar objeto**, enquanto a save do
   Gui estiver viva (ver seção 3). Apagar move índice.

---

## 3. Restrições duras

Estas quatro não se negociam sem decisão explícita do Gui, e três delas mudaram
de valor em 11/08 porque o `ESTADO.md` estava errado. **Meça, não copie daqui.**

| recurso | livre hoje | onde medir | o que acontece se estourar |
|---|---|---|---|
| ROM | **1,53 MB** de 32 MB (95,23% usado) | fim do `make` | não builda, **e tudo bem: ver a regra abaixo** |
| flags | **40** | `flags_livres.py` | crescer `FLAGS_COUNT` quebra save antiga |
| ids de treinador | **59** (2441 a 2499) | ler `include/constants/opponents.h` | subir `MAX_TRAINERS_COUNT_EMERALD` (2500) desloca `SYSTEM_FLAGS`, que deriva de `TRAINER_FLAGS_END`, e quebra save antiga |
| vars | ~30 no jogo inteiro | `vars.h` | idem flags |
| grupos de mapa | 126 de 128, e 128 mapas por grupo | `map_groups.json` | mapa de índice 128 **reseta o jogo** |

### PASSAR DE 32 MB É PERMITIDO, E É O PLANO

Decidido pelo Gui em 12/08/2026, e esta é a regra que manda quando qualquer
outra frase deste documento parecer dizer o contrário:

> O que ele mais quer é **desenvolver todos os assets de todas as regiões**, e
> depois decidir o que cabe na ROM.

Consequências operacionais, obrigatórias:

1. **Nenhum bloco pode se cortar por medo de espaço.** Fazer tudo, inclusive
   sabendo que não cabe.
2. Asset que não couber **não é apagado**: ele vira arquivo no repositório e
   fica fora da build por `#if` / entrada comentada em `graphics_file_rules.mk`,
   com o motivo escrito. O trabalho fica feito e reversível.
3. Build vermelha por estouro de ROM **não é falha do bloco**; é entrada no
   bloco B10 dizendo quanto passou e qual asset é o mais caro.
4. **O que continua sendo linha vermelha de verdade** é o que não é questão de
   tamanho: EWRAM (85,6%), IWRAM (86,6%), o teto de 128 mapas por grupo e o de
   128 grupos. Esses reiniciam o jogo ou impedem o link, e nenhum "corta depois"
   resolve.

### A save: a janela está ABERTA hoje, e fecha na próxima ROM

Decidido pelo Gui em 12/08/2026, e **muda a restrição mais cara deste projeto**:

> A save atual dele **pode ser descartada** no trabalho de hoje. Da **próxima**
> save em diante é que precisa aguentar edição futura sem perder progresso.

O que isso libera, e **só vale enquanto durar a revisão de hoje**:

- Subir `MAX_TRAINERS_COUNT_EMERALD` acima de 2500 (o portão da seção 7 que
  podia travar o B4 inteiro).
- Crescer `FLAGS_COUNT` e o pool de vars.
- Inserir mapa no meio de grupo, objeto no meio de mapa, campo no meio de
  struct de save: tudo que hoje é proibido por mover índice.
- **Apagar** conteúdo inventado de verdade, em vez de esconder atrás de flag
  (regra 4 da seção 2 fica suspensa hoje).

**Como a janela fecha, e isto é entrega obrigatória do dia:** a última coisa
antes de entregar a ROM nova é rodar `guarda_save.py --gravar` sobre ela, para
congelar a impressão nova. Da ROM seguinte em diante, `guarda_save.py` volta a
ser portão vermelho e desfazer volta a ser a resposta padrão.

**Faça o alargamento de teto CEDO no dia, não tarde.** Toda quebra de save tem
que estar dentro da mesma janela; um bloco que descobre às 23h que precisa de
mais 300 ids não pode reabrir a janela sozinho.

---

## 4. Linha de base medida em 11/08/2026

| região | mapas | objetos | warps | placas | fonte |
|---|---|---|---|---|---|
| Kanto | 98,1% | 100,1% | 100,0% | 100,0% | `pokefirered` |
| Johto | 95,9% | 94,0% | 100,0% | 96,0% | `hns` |
| Hoenn | 100,0% | 100,1% | 100,0% | 100,0% | `pokeemerald` |
| Sinnoh | **72,7%** | **77,2%** | 99,2% | **81,2%** | `pokeplatinum` + `fontes-mapas/sinnoh` |
| Unova | 94,2% | 98,5% | 98,9% | 98,0% | `BW3G` |

Outros números da árvore: 1895 mapas, 2369 blocos de time em `trainers.party`,
1790 constantes citadas por `trainerbattle` (todas com time), 609 mapas com
encontro selvagem, suíte de emulador 162/163.

### O que essa tabela NÃO mede, e por que Unova aparece verde estando cru

O Gui desconfiou em 12/08 de que Unova fosse maquete. **Está certo, e a tabela
acima não é capaz de mostrar isso**, porque `completude.py` conta *presença* de
mapa, objeto, warp e placa. Ele nunca abre o `blockdata`. Um mapa com as portas e
os NPCs certos, desenhado como caixa vazia, passa com 98%.

Medida nova, feita nesta árvore, contando **metatiles distintos por mapa** (a
variedade do desenho, não a existência dele):

| região | mediana de metatiles distintos | máximo na região | mapas com 3 ou menos |
|---|---|---|---|
| Kanto | 52 | 319 | 0 |
| Hoenn | 39 | 545 | 11 |
| Sinnoh | 39 | 303 | 0 |
| **Unova** | **3** | **5** | **155 de 291** |

Máximo **5** em 291 mapas. Não é mapa: é **máscara de colisão em duas cores**,
chão e parede, mais o metatile de porta. Aspertia City são 1232 células com 4
valores; o prédio é um retângulo do metatile "bloqueado". Nenhum telhado, árvore,
água, degrau, cerca ou móvel existe em Unova.

Segunda medida, o outro lado do mesmo buraco, lendo `layouts.json`: **Unova não
tem um tileset próprio sequer.** Os 291 mapas usam tileset de Hoenn e de Sinnoh:

| tileset usado | mapas de Unova |
|---|---|
| `Building + GenericBuilding` | 138 |
| `GeneralSinnoh + PetalburgSinnoh` | 75 (todo exterior de cidade e rota) |
| `GeneralSinnoh + CaveSinnoh` | 32 |
| `Building + RustboroGym`, `PokemonCenter`, `Shop` | 46 |

**O que está pronto de verdade em Unova** (medido, e é bastante, por isso a
região não é lixo): 291 mapas registrados com dimensão exata da fonte, 1396 NPCs,
1060 warps, 497 placas, **6234 linhas de texto de verdade do BW3G**, 360
treinadores únicos **todos com time em `trainers.party`**, e 87 mapas com
encontro selvagem.

**Diagnóstico:** Unova está com **conteúdo pronto e arte zerada**. É o inverso
exato de Sinnoh, que tem arte real e 164 mapas faltando. A conversão leu o
`.ablk` certo (`AspertiaCity.ablk` tem 308 bytes = 14x22 blocos de gen 2 = os
28x44 metatiles do nosso layout, casamento exato) e **parou na tradução de bloco
para metatile**, chutando andável/bloqueado.

**A fonte tem a arte**, e isso é o que torna o conserto viável em vez de
artesanal: `../fontes-mapas/bw3g` é código-fonte, não binário raspado. Tem 240
`.ablk`, 309 `.asm` de mapa e **60 PNG de tileset de Unova de verdade**
(`castelia.png`, `desert.png`, `bridge.png`, `chargestone.pal`,
`dragonspiral_tower`, `celestial_tower`, `champions_room`...). O trabalho é
converter tileset de gen 2 para GBA e reescrever a tabela bloco→metatile, não
desenhar Unova à mão.

---

## 5. Blocos de trabalho

Cada bloco é uma frente que um agente consegue tocar sozinha. A ordem importa só
onde está escrito que importa.

### B0. Inventário por região (faça primeiro, é barato e todo o resto depende)

O projeto já errou várias vezes por confiar em número de documento. Antes de
qualquer bloco, produza `INVENTARIO.md` com, por região e por mapa:

- pessoas na fonte contra pessoas aqui (o excesso e a falta, separados);
- treinadores na fonte contra treinadores batalháveis aqui;
- NPCs com fala contra NPCs mudos;
- placas com texto próprio contra placas genéricas;
- mapas da fonte ausentes aqui;
- encontros selvagens na fonte contra tabelas aqui.

**Aceite:** o inventário roda por script (`dev_scripts/inventario.py`, com
`--demo`), é reprodutível, e cada linha aponta o arquivo da fonte que a
sustenta. Nada de número escrito à mão.

**Isto substitui a seção 8 do `ESTADO.md` como fila de trabalho.**

### B1. Sinnoh: os 164 mapas que faltam

Divisão medida em 11/08:

| quanto | o quê | por que não saiu ainda |
|---|---|---|
| 46 | Turnback Cave e os `UNKNOWN_533` a `557` | zero pais no grafo de warp: a sala é sorteada por script |
| 10 | Distortion World | zero pais, e a grade dá de 0 a 31 tiles de chão |
| ~40 | Battle Frontier/Tower, ginásio DP de Hearthome, elevadores da Liga, Vista Lighthouse | interiores com mobília desenhada: a grade 2D não basta |
| ~15 | Amity Square, Trophy Garden, Great Marsh 1 a 6, Pal Park, Spring Path, Route 204 North, Fullmoon/Newmoon, Fuego, Hall of Origin | `MAP_TYPE_OUTDOORS`, folhas do grafo |

Três frentes técnicas distintas, e **nenhuma é mais conversão de chão**:

- **B1.a Conversor de mobília.** O conversor atual só entende chão de masmorra.
  Interior de gen 4 tem mobília desenhada no mapa, e é isso que falta traduzir
  para metatile do GBA. Maior item do PRD inteiro.
- **B1.b Salas sorteadas por script.** Turnback Cave e Distortion World não têm
  warp estático. Custa o script de sorteio, não conversão.
- **B1.c Exteriores folha.** Os ~15 que hoje virariam sala vazia de 13x9. Só
  entram junto com B1.a, senão são régua e não mapa (lição 4.10).

**Aceite:** mapa entra só se for **alcançável a pé** a partir de Pallet, provado
por `valida_conectividade.py` e por caso de emulador para cada tipo novo.

### B2. NPCs e falas de Sinnoh

559 mudos hoje, com a divisão medida:

- **344 são treinador** → resolvido pelo bloco B4, não aqui.
- **108 apontam para Wi-Fi e Union Room**, que não existem nesta ROM. Decisão
  necessária: fala substituta de sistema inexistente, ou esconder o NPC. Ver
  seção 7.
- **68 são balconista, enfermeira e vendedor**: o rótulo não tem comando de
  texto, chama a rotina de loja ou cura direto. Provavelmente já corretos.
- **19 têm buffer ou caractere fora do charmap** (`{SIZE}`, `{COLOR}`, `♫`).
- **8 estão em mapa reprovado pelo alinhamento** (`OreburghMine_B2F`,
  `Route205_North`): conserte o alinhamento por coordenada, como
  `itens_escondidos_sinnoh.py` já faz.

Mais: **230 objetos com `hidden_flag` e 84 `coord_events`** que nunca vieram.
Esses só entram **junto com a cena que os apaga** (bloco B6); sozinhos viram
parede permanente, que é a armadilha das 39 pedras de Strength de Unova.

### B3. Limpeza do conteúdo inventado

Autorizado pelo Gui em 11/08. Escopo medido: **+102 pessoas de excesso em 37
mapas de rota de Sinnoh** (311 na fonte contra 413 visíveis), mais o que o
inventário B0 achar nas outras regiões.

Método, o mesmo que já fechou 8 casos com prova:

1. cobertura do mapa fechada contra a fonte (todo mundo da fonte está aqui);
2. o excedente é nativo, sem par na fonte;
3. o script dele **só fala**, e o `local_id` não é citado por script nenhum;
4. some atrás de `FLAG_SINNOH_NPC_DUPLICADO`, **não é apagado**.

Falhou qualquer uma das quatro, fica de pé e entra em relatório. A decisão de
inverter par continua sendo humana e mora em tabela escrita à mão.

**Exceção obrigatória:** NPC de sistema (loja, cura, marinheiro da travessia)
fica mesmo sem par na fonte. Ver seção 7.

### B4. Todo treinador batalhável, nas cinco regiões

Estado: 1790 constantes citadas por `trainerbattle` e todas com time. O que não
se sabe é **quantos da fonte ficaram de fora**, por região. B0 responde.

Já medido em Sinnoh: 417 treinadores na fonte, 150 ligados em 11/08, e as
ausências nomeadas são treinador com `hidden_flag` (depende de B6) e treinador
com nome próprio sem sprite (depende de B9).

**Cuidado de recurso:** só existem **59 ids livres**. Se o inventário disser que
falta mais que isso, **pare no bloco B10**: subir o teto quebra a save do Gui, e
a saída é decisão dele.

**Aceite:** para cada região, treinador da fonte = treinador aqui, com time da
fonte, `trainer_type` certo, raio de visão da fonte, e fala portada (em gen 4 a
fala mora junto com o time, em `TRMSG_*`, não no banco de texto do mapa).

### B5. Ginásios populados nas cinco regiões

Medido: os oito de Sinnoh tinham **só o líder** até 11/08; os treinadores de
dentro entraram agora. Falta conferir o mesmo em Kanto, Johto, Hoenn e Unova, e
falta o **quebra-cabeça** de cada ginásio, que é o que os torna distintos e é
onde var costuma ser gasta.

**Aceite:** líder com time, insígnia, treinadores de dentro, e o puzzle
funcionando, provado no emulador (entrar, resolver, chegar ao líder).

**Cuidado:** puzzle é a maior fonte de gasto de var do projeto. Leia as três
técnicas de `SINNOH-PADRAO.md` antes de gastar uma. O ginásio de Blackthorn já
foi resolvido sem var, nascendo pronto num `MAP_SCRIPT_ON_LOAD`.

### B6. História completa, região por região

O maior bloco depois de B1.a, e o que mais depende de julgamento.

- **Unova: 209 cenas.** Classificação já feita: 107 `changeblock` (1225
  chamadas, exigem traduzir id de bloco de gen 2 para metatile), 47 `setscene`,
  27 abrem batalha, 21 `special`, 16 `callasm` (máquina de estados da Plasma).
  **17 das 32 mecanicamente portáveis são bloqueio** que o enredo apaga na fonte
  e aqui viraria parede permanente: essas só entram com a cena que as apaga.
- **Sinnoh: o resto da Galáctica**, mais os 230 `hidden_flag` do bloco B2.
- **Kanto, Johto, Hoenn:** B0 diz o que falta. Hoenn está intocado e em 100%,
  então é a régua de comparação.

**Aceite por cena:** a cena roda, muda o mundo, e **desfaz o bloqueio que criou**.
Cena que trava o jogador é pior que cena ausente.

### B7. Encontros selvagens e disponibilidade de espécie

609 mapas têm tabela hoje, sendo 87 de Unova e 30 de Sinnoh (de 94 mapas de
Sinnoh na ROM, e nem todo interior precisa). Gen 1 a 9 estão habilitadas em
`include/config/species_enabled.h`, então **espécie existe**; o que falta é
**onde ela aparece**.

**Aceite:** todo mapa que tem encontro na fonte tem tabela aqui, com espécie,
nível e taxa da fonte; e a Pokédex de cada região é completável sem depender de
troca, ou a exceção é nomeada.

### B8. Curva de nível entre regiões

Cinco regiões em ordem cronológica num save só: o nível dos treinadores de
Sinnoh veio remapeado, o de Unova não necessariamente. `curva_de_nivel.py` mede
e remapeia.

**Aceite:** a curva sobe de forma monótona por região na ordem
Kanto, Johto, Hoenn, Sinnoh, Unova, sem degrau que exija grind.

### B9. Sprite, arte e o que falta desenhar

71 NPCs de Sinnoh não vieram por não ter sprite honesto (Cynthia, Cyrus, Looker,
os lendários de lago). Ver `ARTE-PENDENTE.md`. Emprestar sprite de personagem
parecido é aceitável e já foi feito (Maxie para Cyrus); inventar não.

### B12. Unova: tileset de verdade e mapa que não seja máscara de colisão

**O maior bloco de arte do projeto, e ele existe porque o Gui olhou e desconfiou
em 12/08.** A medição está na seção 4: mediana de **3 metatiles distintos por
mapa**, máximo de 5 em 291 mapas, zero tileset próprio. Unova hoje é conteúdo
completo dentro de caixas vazias com tijolo de Petalburg.

Não se conserta mapa a mapa. Conserta-se na conversão, e por tileset:

#### O casamento gen 2 → gen 3, medido, que é o que torna o bloco viável

O Gui perguntou como o plano converte BW3G de gen 2 para gen 3. A resposta é que
os dois formatos **casam quase campo a campo**, e isso não é sorte: o gen 3 é o
gen 2 com o dobro de bits. Medido nas duas árvores:

| conceito | gen 2 (BW3G) | gen 3 (pokeemerald) | conversão |
|---|---|---|---|
| tile | 8x8, 2bpp, 4 cores | 8x8, 4bpp, 16 cores | expandir bits; sobra paleta |
| unidade de mapa | **bloco de 4x4 tiles** (32x32 px) | **metatile de 2x2 tiles** (16x16 px) | **1 bloco = 4 metatiles**, e é por isso que o `.ablk` de 14x22 vira layout de 28x44 |
| camada | 1 camada + bit de prioridade | 2 camadas por metatile (8 entradas) | camada de baixo recebe o tile; prioridade vira camada de cima |
| paleta por tile | `attributes.bin`, 3 bits (8 paletas) + flip | entrada de metatile, 4 bits (16) + flip | direto, e cabe |
| colisão | `_collision.asm`, **4 valores por bloco**, um por quadrante de 16x16 | 1 comportamento por metatile | **um para um**, sem perda |
| comportamento | `COLL_TALL_GRASS`, `COLL_WATER`, `COLL_ICE`, `COLL_WATERFALL`, `COLL_WHIRLPOOL`, `COLL_CUT_TREE`, ledge por direção | `MB_TALL_GRASS`, `MB_DEEP_WATER`, `MB_ICE`, `MB_WATERFALL`, `MB_...` | tabela de nomes, escrita à mão uma vez |

A colisão do gen 2 ser **por quadrante de 16x16** é o detalhe que faz tudo
fechar: é exatamente a granularidade do metatile de GBA. Nada precisa ser
inventado nem arredondado.

**E cabe no orçamento de tileset do GBA, que era o risco real.** `fieldmap.h`
dá ao tileset secundário 512 tiles, 512 metatiles e 6 paletas. Um bloco de gen 2
vira 4 metatiles, e 253 blocos dariam 1012, o dobro do teto. Mas quadrante
repete muito (parede sólida, chão liso), e **deduplicando quadrantes idênticos**
o pior tileset dos 58 do BW3G dá **322 metatiles únicos**, mediana 162, e
**nenhum passa de 512**. Tiles: 224 a 256 por tileset, contra teto de 512.
Medido nos 58, não estimado. Conclusão: **cada tileset do BW3G vira um tileset
secundário do GBA, um para um, sem partir mapa.**

O que **não** casa e é decisão sua: gen 2 tem paleta de dia e de noite
(`*_nite.pal`), e o pokeemerald não tinge tileset por horário. Descartar a noite
é o caminho barato.

**B12.a Converter o tileset.** Escrever `dev_scripts/tileset_gen2.py`: PNG 2bpp
+ `.pal` viram `tiles.png` 4bpp, `palettes/*.pal` e `metatiles.bin` no formato do
pokeemerald, com a deduplicação de quadrante acima. Começar por **um** tileset de
exterior (`castelia` ou `desert`) e provar o ciclo inteiro antes de rodar nos 58.
Custo: 90 a 190 KB por tileset. **Isso estoura a ROM, e estourar é permitido**
(seção 3).

**B12.b A tabela bloco→metatile.** É aqui que a conversão original parou: ela
chutou andável/bloqueado em vez de emitir os 4 metatiles. O `.ablk` guarda o
índice do bloco de gen 2, e `AspertiaCity.ablk` (308 bytes = 14x22) casa exato
com o layout de 28x44 que já está na ROM. Então **a geometria não precisa ser
reimportada**: reler o mesmo `.ablk` com a tabela honesta substitui o
`blockdata` inteiro **sem mexer em warp, NPC, placa ou índice de mapa**. É o que
torna B12 barato em risco e caro só em bytes.

**B12.c Colisão e comportamento.** Hoje Unova só tem andável/bloqueado, o que
implica que **não existe grama alta em Unova** e as 87 tabelas de encontro
selvagem do B7 provavelmente nunca disparam. Confirmar isso é a primeira medição
do bloco, e o resultado muda o aceite do B7. O dado de origem existe:
`data/tilesets/*_collision.asm`, com os `COLL_*` da tabela acima.

**B12.d Interiores.** 138 mapas usam `Building + GenericBuilding` sem uma mesa
sequer. Mesma técnica do conversor de mobília do B1.a de Sinnoh; se B1.a ficar
pronto primeiro, reusar em vez de escrever outro.

**Aceite:** mediana de metatiles distintos por mapa de Unova na mesma ordem de
grandeza das outras regiões (dezenas, não 3), toda cidade e rota com tileset de
Unova, grama alta existindo onde a fonte tem encontro, e nenhum índice de mapa,
warp ou objeto deslocado (`guarda_save.py` verde, ou dentro da janela de hoje).

**Ordem sugerida:** B12.b antes de B12.a se der, porque a tabela feita com
tileset emprestado já melhora o mapa e prova o casamento sem gastar ROM.

### B10. Orçamento: o que estourou

Bloco de registro, não de execução. Toda vez que um bloco passar de qualquer
limite da seção 3, anote aqui: quanto passou, o que causou, e qual seria o corte
mais barato. **Nenhum agente corta sozinho.** No fim, o Gui decide.

Já se sabe que vai apertar: 1,53 MB de ROM e 59 ids de treinador não pagam B1.a
mais B4 completos.

### B11. Jogar do começo ao fim

Ninguém nunca jogou este hack inteiro. Dois caminhos, e os dois valem:

- **Emulador dirigido:** estender a suíte `testa_critico.py` até cobrir a
  espinha da história de cada região, com prova lida da EWRAM.
- **O Gui jogando**, com a save protegida pelo `guarda_save.py`, achando o que só
  humano acha: dificuldade, ritmo, fala sem sentido, NPC no lugar errado.

**Aceite final:** um save que sai de Pallet e chega ao Hall da Fama das cinco
regiões.

---

## 6. Ordem

```
B0  inventário          ── obrigatório antes de tudo
 ├─ B3  limpeza          ── independente, barato, autorizado
 ├─ B4  treinadores      ── depende de B0; para em B10 se faltar id
 ├─ B5  ginásios         ── depende de B4
 ├─ B7  selvagens        ── independente
 ├─ B8  curva            ── depende de B4 e B7
 ├─ B2  NPCs e falas     ── parte depende de B6
 ├─ B6  história         ── depende de B2 para os hidden_flag
 ├─ B9  sprite           ── destrava parte de B2 e B4
 ├─ B1  mapas de Sinnoh  ── B1.b e B1.c dependem de B1.a
 └─ B12 arte de Unova    ── B12.c antes do aceite de B7; B12.d reusa B1.a
B10 orçamento           ── contínuo
B11 jogar               ── contínuo, e é o aceite final
```

Paralelizar B3, B4, B7 e B9 é seguro: chaves diferentes do `map.json` e arquivos
diferentes. B1.a é solo, porque mexe no conversor, e B12.a e B12.b também são:
os três escrevem `blockdata` e `layouts.json`, e não podem rodar juntos.

**Alargar teto vem antes de todos**, hoje, enquanto a janela de save está aberta
(seção 3): decidir e aplicar `MAX_TRAINERS_COUNT`, `FLAGS_COUNT` e vars antes de
qualquer bloco pedir.

---

## 7. Portões que exigem decisão do Gui

Não são perguntas de execução; são escolhas que mudam o jogo.

1. ~~**Teto de treinador.**~~ **RESOLVIDO em 12/08:** a save de hoje é
   descartável, então o teto sobe dentro da janela. Decidir **de quanto** ainda
   é dele, e a conta é do B0: subir para 4000 custa RAM de save e ROM, e não dá
   para subir de novo depois sem quebrar de novo. **Subir com folga agora sai de
   graça; subir amanhã sai caro.**
2. **Os 108 NPCs de Wi-Fi e Union Room.** Fala substituta, ou esconder.
3. ~~**Estouro de ROM.**~~ **RESOLVIDO em 12/08:** pode passar de 32 MB, fazer
   tudo, cortar depois. Ver a regra na seção 3. B10 vira só registro de custo.
4. ~~**Save antiga da build de 05/08.**~~ **RESOLVIDO em 12/08:** ele começa
   partida nova na ROM de hoje; nada de `MAP_SCRIPT_ON_TRANSITION`.
5. **Os ~15 exteriores folha de Sinnoh.** Entram como sala vazia agora, ou
   esperam o conversor de mobília?
6. **Quanto de Unova desenhar (B12).** Converter os 60 tilesets do BW3G é o
   maior gasto de ROM do projeto inteiro, e sozinho pode dobrar o estouro. Ele
   já disse "fazer tudo"; o que fica em aberto é a **ordem**, ou seja, quais
   cidades ganham arte primeiro se o corte vier depois. Sugestão: Castelia,
   Nimbasa, Driftveil e Opelucid, que são as que ficam mais absurdas com tijolo
   de Petalburg.

---

## 8. Regras para quem executar

Valem para todo bloco, e cada uma nasceu de um erro que já custou uma sessão.

**Como o Fable delega** (skill `fable-distribuido`; ele escreve prompt e julga
resultado, não digita código):

| bloco | executor sugerido | por quê |
|---|---|---|
| B0 inventário | `sonnet`, um agente por região, em paralelo | varredura mecânica, retorno é tabela |
| B1.a conversor de mobília, B12.a e B12.b | `opus`, **um de cada vez** | os três escrevem `blockdata` e `layouts.json`; errar aqui estraga mapa em massa |
| B3 limpeza | `opus` | decide o que é inventado, e decidir errado apaga conteúdo legítimo |
| B4 treinadores, B5 ginásios | `opus`, faixa de id exclusiva medida na hora | |
| B2 falas, B6 história | `opus` | julgamento de texto contra fonte |
| B7 selvagens, B8 curva | `sonnet` | tabela contra tabela |
| B9 sprite | `opus` | "emprestar sprite parecido" é julgamento |
| conferência mecânica (build, suíte, `guarda_save.py`) | `sonnet` ou Bash direto | barato, e pega a maior parte |

Todo prompt de executor carrega o protocolo de dúvida do skill: **não chute
decisão que muda o resultado**, termine o que dá sem ela e volte com bloco
`DÚVIDA:` (pergunta, opções, recomendação). O Fable responde continuando o
**mesmo** agente por `SendMessage`, nunca abrindo agente novo.

- **Meça antes de escrever.** Duas frentes de treinador receberam faixa de id
  inválida vinda de tabela do `ESTADO.md` no mesmo dia; as duas só não quebraram
  nada porque foram conferir na fonte primeiro.
- **Nunca escreva conteúdo do zero quando a fonte tem.** Toda vez que alguém
  escreveu, foi o caminho errado.
- **Agente não compila.** `make` concorrente já encheu este repo de arquivos
  `arquivo 2.c`. Build só em worktree isolada, e quem builda na árvore é o
  condutor, uma vez, no fim.
- **Agente não commita** e nunca roda `git add`.
- **Agente paralelo recebe chave exclusiva do `map.json`** (um em
  `object_events`, outro em `bg_events`, outro em `warp_events`) e faixa
  exclusiva de flag e de id, **medida na hora**, não copiada de documento.
- **Releia o arquivo do disco antes de cada escrita.** Já salvou trabalho de
  outro agente neste repo.
- **Verifique na camada da afirmação.** "Rodou" não é verificação; "existe" não é
  "é único" (134 rótulos duplicados passaram por uma checagem de existência e
  quebraram o build); exit code atrás de pipe mente.
- **Boa notícia é suspeita.** Cinco de cinco casos passando de primeira pede
  contraprova: rode a mutação e veja o teste falhar.
- **Toda ferramenta tem `--demo` com assert e é idempotente.**
- Texto de jogo em inglês; documentação e comentário em português acentuado, sem
  em dash.

---

## 9. Exceções deliberadas

Lista viva. Conteúdo que **não está na fonte e fica assim mesmo**, cada um com o
motivo. Quem acrescentar item aqui, escreva o porquê na mesma linha.

| o quê | por que fica |
|---|---|
| Marinheiro da travessia entre regiões, nos cinco portos | a fonte não tem viagem entre regiões; sem ele o hack não existe |
| `MAP_SINNOH_LEAGUE_HALL_OF_FAME` | Sinnoh precisa de Hall da Fama próprio, e o de Hoenn liga a história inteira de Hoenn |
| `SetGameClearHealLocation` | sem ele, o "Continue" pós-créditos joga todo mundo em Littleroot |
| Storage Key de Veilstone reusando o item de Hoenn | mesmo nome, mesmo bolso, mesma função, e economiza um item |
| Passagem provisória dos três exteriores de Sinnoh | destravam masmorra convertida de verdade; saem quando B1.a existir |
| Ausência de Elite dos Quatro de Johto | a liga de gen 2 é o mesmo Planalto Índigo de Kanto; quem libera Hoenn é a oitava insígnia |

---

## 10. Os trade-offs, para o Fable julgar antes de delegar

Cada um destes já tem conta feita e nenhum tem resposta óbvia. É por causa desta
lista que o Gui chamou um arquiteto em vez de mais um executor.

**T1. Vaga vazia de treinador é o gasto mais burro da ROM, e já foi pago.**
`opponents.h` mede **~324 bytes de ROM por vaga**, porque `gTrainers`,
`sTrainerSlides` e `sTestTrainerSlides` são dimensionados pelo teto, não pelo
uso. Subir 2500 → 4000 custou **~486 KB** de 1,53 MB livres, em slot vazio, que
não vira conteúdo e não dá para cortar seletivo depois. Foi decisão do Gui,
sabendo o número, porque **o teto só muda em dia de janela de save aberta** e
hoje é esse dia. O trade-off que sobra pra você: se o B0 mostrar que a
necessidade real é 3000, valeu a pena? Não dá para desfazer amanhã.

**T2. Arte de Unova contra tudo o mais que precisa de ROM.** 58 tilesets a 90 a
190 KB dão 5 a 11 MB, sozinhos maiores que a ROM livre. A ordem do Gui é
Castelia, Nimbasa, Driftveil, Opelucid. Decisão sua: converter os 4 e medir o
custo real antes de liberar os outros 54, ou converter todos e deixar o corte
para o B10? O primeiro é reversível e barato; o segundo é o que ele pediu ao
dizer "faça tudo".

**T3. Sinnoh tem arte e não tem mapa; Unova tem mapa e não tem arte.** São 164
mapas de Sinnoh (B1) contra 291 mapas crus de Unova (B12), e as duas frentes
disputam o mesmo conversor de mobília e o mesmo espaço. Ordem errada faz uma
delas ser reescrita. B12.d diz para reusar B1.a; confirme que é o mesmo problema
antes de fazer alguém escrever dois conversores.

**T4. Apagar contra esconder, hoje.** Enquanto a janela de save está aberta,
apagar conteúdo inventado é mais limpo e devolve índice. Depois de fechada, só
esconder atrás de flag, e cada flag sai de um pool de 40. Se o B3 vai apagar,
tem que ser **hoje**; se for depois, custa flag para sempre.

**T5. `completude.py` não é aceite suficiente e o projeto acreditou nele.** Ele
mede presença. Foi o que deixou Unova passar com 98% sendo maquete. Antes de
fechar qualquer bloco por métrica, decida qual medida enxerga o buraco daquele
bloco. Precisa existir um `completude.py --geometria`, e não existe.

**T6. Ninguém jogou este hack inteiro.** A suíte de emulador tem 163 casos e
prova trecho, não jornada. O aceite final (B11) depende do Gui jogando, o que é
lento, ou de estender a suíte, o que é caro. Escolher qual dos dois carrega o
peso muda o tamanho de todos os outros blocos.

**T7. A ROM que ele joga sai de commit local.** Nada foi empurrado; o `git push`
é dele. Se a entrega de hoje sair, o `guarda_save.py --gravar` sobre ela é
irreversível na prática: congela a impressão que rege todas as edições futuras.
Não deixe isso acontecer por acidente no fim de um bloco.
