# PRD: terminar a ROM inteira

Documento de trabalho para o objetivo "acabar o hack". Escrito em 11/08/2026,
sobre o commit `9f0c020299`. Tudo que está aqui como número foi **medido nesta
árvore**, e cada bloco diz com qual comando remedir. Número sem comando ao lado
é suspeito e deve ser remedido antes de virar plano.

Leia `ESTADO.md` antes deste arquivo. Ele é o ponto de entrada e tem as
armadilhas; este aqui é só o plano.

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
| ROM | **1,53 MB** de 32 MB (95,23% usado) | fim do `make` | não builda |
| flags | **40** | `flags_livres.py` | crescer `FLAGS_COUNT` **quebra a save** |
| ids de treinador | **59** (2441 a 2499) | ler `include/constants/opponents.h` | subir `MAX_TRAINERS_COUNT_EMERALD` (2500) desloca `SYSTEM_FLAGS`, que deriva de `TRAINER_FLAGS_END`, e **quebra a save** |
| vars | ~30 no jogo inteiro | `vars.h` | idem flags |
| grupos de mapa | 126 de 128, e 128 mapas por grupo | `map_groups.json` | mapa de índice 128 **reseta o jogo** |

**A save do Gui está viva.** Impressão congelada em
`dev_scripts/save_impressao.json`, sobre `roms/pokemon-claude-2026-08-11b.gba`.
`guarda_save.py` tem que dizer SAVE COMPATIVEL ao fim de todo bloco, e **desfazer
é a resposta padrão** para quebra, não registrar a quebra.

**Sobre estourar a ROM:** o Gui decidiu em 11/08 que prefere **fazer tudo e
cortar depois**. Então bloco que não couber **não deve ser cortado sozinho**:
faça, meça o custo, e registre no bloco B10 quanto passou. A decisão de o que
tirar é dele.

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
 └─ B1  mapas de Sinnoh  ── B1.b e B1.c dependem de B1.a
B10 orçamento           ── contínuo
B11 jogar               ── contínuo, e é o aceite final
```

Paralelizar B3, B4, B7 e B9 é seguro: chaves diferentes do `map.json` e arquivos
diferentes. B1.a é solo, porque mexe no conversor.

---

## 7. Portões que exigem decisão do Gui

Não são perguntas de execução; são escolhas que mudam o jogo.

1. **Teto de treinador.** Se faltar mais que 59 ids, subir `MAX_TRAINERS_COUNT`
   quebra a save dele. Alternativas: save nova, ou menos treinador.
2. **Os 108 NPCs de Wi-Fi e Union Room.** Fala substituta, ou esconder.
3. **Estouro de ROM.** Ele já disse: fazer tudo e cortar depois. B10 lista o que
   cortar quando chegar a hora.
4. **Save antiga da build de 05/08.** As flags de esconder e de região só nascem
   em jogo novo; consertar save antiga exige `MAP_SCRIPT_ON_TRANSITION`.
5. **Os ~15 exteriores folha de Sinnoh.** Entram como sala vazia agora, ou
   esperam o conversor de mobília?

---

## 8. Regras para quem executar

Valem para todo bloco, e cada uma nasceu de um erro que já custou uma sessão.

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
