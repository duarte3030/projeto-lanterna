# Unova entra na mesma ROM, com o tileset de Sinnoh

Decisão do Gui em 05/08/2026. Reverte a remoção de Unova feita horas antes, mas
por um motivo diferente: o que foi apagado eram **47 retângulos falsos apontando
para o `map.bin` de Petalburg**. O que entra agora é geometria real.

## Por que cabe (a conta que eu tinha errado)

Eu estimei antes que uma região não caberia, mas assumi tileset novo. O Gui
apontou que dá para reusar o tileset de Sinnoh e que **Black e White não tem
mecânica que o expansion já não tenha**. Está certo, e muda tudo:

| item | custo medido |
|---|---|
| blockdata de uma região | ~350 KB (Sinnoh 372, Johto 317) |
| scripts e texto | 200 a 400 KB |
| treinadores e encontros | dezenas de KB |
| **tileset novo (evitado)** | 90 a 190 KB **por tileset**, e seriam vários |

**Total sem tileset novo: 600 a 800 KB.** A ROM está em 84,25% de 32 MB, com
~3,7 MB livres. Cabe com folga.

Cuidado que aperta antes do cartucho: **EWRAM em 86,46% (29 KB livres) e IWRAM em
86,62% (4 KB livres)**. Se algum dia der erro de link sem motivo aparente, olhar
RAM antes de ROM.

## Fonte

`Pokemon BW Genesis (v1.2).gbc`, demake de Black e White em Game Boy Color, 2 MB
sobre o Crystal. Provado real: 17 de 20 nomes de Unova (Castelia 42x, Nimbasa
27x, Driftveil 23x), Johto praticamente ausente (Violet 2x, Goldenrod 1x), e o
texto dos mapas citando Undella, Lacunosa, Skyarrow Bridge, Castelia Game Plaza,
Team Plasma e Virbank City. Detalhe em `RECURSOS-REGIOES.md`.

**É gen 2**, o mesmo formato que `dev_scripts/demake_gen2.py` já converte, provado
hoje no esconderijo de Mahogany, que saiu com geometria e posições de warp
exatas, sem reposicionar nada.

## O que falta resolver, em ordem

1. **Procurar fonte pública do BW Genesis antes de raspar o binário.** Se existir,
   vem `.blk` com dimensão declarada, mais script e texto organizados. O binário
   dá mapa e nada mais. Mesma consideração de autoria do demake de Galar: se
   entrar, creditar o autor.
2. **Se não houver fonte, achar as tabelas de cabeçalho de mapa dentro do `.gbc`.**
   Primeira tentativa saiu desalinhada (li com passo de 9 bytes e as dimensões
   vieram absurdas, tipo 4x21). É engenharia reversa de verdade, não uma tarde.
   O `pokecrystal` serve de gabarito: mesma engine, estrutura documentada.
3. **Converter com `demake_gen2.py`**, ajustando a paleta de metatiles para o
   tileset de Sinnoh, como o agente do esconderijo fez com `gTileset_Facility`.
4. **Registrar** em `layouts.json`, `map_groups.json` e `event_scripts.s`, e
   **agrupar MAPSEC**: MAPSEC é `u8` e está quase cheia, então Unova usa
   `UNOVA_WEST/EAST/NORTH` como Sinnoh e Johto já fazem. Isso já existiu e foi
   removido junto com a Unova falsa; recriar.
5. **Ligar por barco**, como Johto: o marinheiro de Canalave já tem menu com
   Olivine, Slateport e Vermilion. Acrescentar Unova ali e criar a volta.

## O que aceitar de cara

**Castelia vai ficar estranha.** É metrópole de arranha-céu desenhada com tileset
rural. Rota e cidade pequena portam bem; cidade grande, mal. É o mesmo
compromisso dos interiores de ginásio de Sinnoh, que hoje são de Hoenn.

A diferença que importa: a geometria é **real**. A Unova apagada não era feia,
era mentira, e por isso saiu.

Se depois sobrar espaço, dá para somar tileset próprio **um por vez**, começando
pelas cidades grandes. Mapa primeiro, arte quando couber.

## O que NÃO entra

**Galar fica fora desta ROM.** A ROM do autor já usa 30,2 de 32 MB só com Galar,
e lá o custo real é arte, não mapa. Se um dia entrar, é ROM separada, e o caminho
certo é falar com o Phantonomy antes.

---

## Estado em 05/08/2026: a região entrou

Feito por `dev_scripts/importa_unova.py` (roda de novo e regenera tudo do zero,
é determinístico). Medido nesta sessão, não estimado:

| item | número | como conferi |
|---|---|---|
| mapas | **291** | `ls data/maps/Unova_* \| wc -l` |
| geometria e colisão | **152.388 metatiles, 0 errados** | releitura do `map.bin` gravado contra o `.ablk` da fonte |
| warps | 1067, **0 quebrados** | `valida_conectividade.py` |
| placas, NPCs, textos | 175, 1061, 944 | saída do import |
| Pokecenters que curam, lojas | 18, 18 | `jumpstd pokecenternurse` e `scalingmart` |
| tabelas de selvagem | 87 | `wild_encounters.json` |
| ROM | 85,62% (era 84,25%) | saída do `make`, +452 KB |
| flags gastas | **0** | ver `SEM_FLAG` no import |
| save | compatível | `guarda_save.py` |

### O que ficou de fora, e por quê

1. **334 item balls e 133 itens escondidos.** Cada um exige uma flag própria
   (senão o item renasce a cada entrada no mapa). São 467 flags, e o pool
   `FLAG_UNUSED_*` inteiro tem 251. Criar número de flag novo cresce `flags[]`
   dentro do SaveBlock1 e invalida save. **Precisa de decisão do dono** sobre
   orçamento de flag antes de entrar.
2. **209 `coord_event`** (gatilhos de cena). Cada um é uma cutscene do enredo do
   BW3G; portar exige traduzir o bytecode de script de gen 2, que é trabalho
   diferente de geometria.
3. **361 treinadores** entraram como NPC que fala o texto de "ao ser visto", sem
   batalha. Batalha exige entrada em `trainers.party` e time montado.
4. **365 NPCs mudos**: script de gen 2 que não é `jumptextfaceplayer`, `writetext`
   nem `trainer` (troca, elevador, estante, estátua de ginásio).
5. **Elevadores**: 7 warps apagados de propósito. No gen 2 o elevador não tem
   warp de volta, quem decide o destino é o painel; convertido ao pé da letra o
   jogador entrava e não saía.

### Treinadores: o muro de save, e quem ficou de fora (decisão do dono, 05/08/2026)

O BW3G tem **357 objetos `OBJECTTYPE_TRAINER`** em 81 mapas. **Não cabem.**

`include/constants/flags.h:1344` amarra as duas coisas:

```c
#define TRAINER_FLAGS_END  (TRAINER_FLAGS_START + MAX_TRAINERS_COUNT - 1)
#define SYSTEM_FLAGS       (TRAINER_FLAGS_END + 1)
```

Cada vaga de treinador é uma flag dentro de `flags[]`, que mora no SaveBlock1.
Medido: subir `MAX_TRAINERS_COUNT_EMERALD` de 1400 para 1719 (o que caberia os
357) leva o SaveBlock1 a **15888 B contra o teto de 15872**, e o `make` continua
saindo **EXIT=0**. A save corrompe sem erro de compilação; quem acusa é o
`guarda_save.py`.

| | |
|---|---|
| SaveBlock1 com os itens de Unova dentro | 15848 de 15872 B |
| livre | **24 bytes = 192 flags** |
| teto máximo possível | 1592 |
| vagas que isso daria | 225, e gastaria **todo** o SaveBlock1 restante do jogo |

**Decisão do dono: opção (a), só as 33 vagas que já existem (1367 a 1399).** Os
24 bytes são o orçamento do jogo inteiro, não de Unova: ainda faltam a transição
Kanto para Johto, os iniciais por região e a curva de nível. O dono foi atrás de
espaço por outro caminho (esticar os setores da save em `include/save.h`); se
conseguir, sai faixa nova e o resto entra.

**Entrou:** os líderes de ginásio, e o Elite dos Quatro se coube nas 33.

**Ficou de fora: 327 treinadores de rota, caverna e prédio.** Os maiores focos,
para quem retomar priorizar: Celestial Tower (10), Rota 4 (10), Desert Resort
(9), Rota 20 (9), Rota 2 (9), Pinwheel Forest (8), Victory Road Outdoor 2F (8),
Rota 6 (8), Rota 23 Oeste (8), Castelia Sewers (7), Victory Road Cave 1F (7),
Rota 21 (7). Os objetos deles já estão no mapa, falando o texto de "ao ser
visto"; virar batalha é só acrescentar a entrada em `trainers.party` e trocar o
`trainer_type` quando houver vaga.

### Mobília: 120 objetos que não eram texto

39 pedras de Strength e 81 estantes usavam `jumpstd` no gen 2, não diálogo, e
por isso caíam na peneira de "NPC mudo". A pedra era a grave: convertida como
NPC mudo ela vira parede permanente e **tranca a caverna para sempre**, e isso
só apareceria depois de horas de jogo. Agora usam `EventScript_StrengthBoulder`
e `EventScript_BookShelf`, que já existiam no repo.

Ficaram de fora de propósito: 15 estátuas de ginásio (o texto do gen 2 é montado
em tempo de execução com o nome do líder e a contagem de vitórias; inventar um no
lugar seria escrever conteúdo, o que o dono vetou) e 11 escadas de prédio e
botões de elevador, que são comportamento e não texto.

### O campeão Genesis não ficou ligado (aceito pelo dono, 05/08/2026)

A sala do campeão do BW3G é cutscene: os objetos estão empilhados na mesma
posição e quem decide quem aparece é o script da cena, não o mapa. Convertida ao
pé da letra, a batalha não tem como ser disparada por um objeto sozinho.
`TRAINER_UNOVA_CHAMPION_GENESIS` (1379) existe, com time e texto, e está pronto
para ser chamado quando alguém portar a cutscene. Os 8 líderes e os 4 do Elite
estão ligados normalmente.

### Menu do barco: uma lista para os cinco portos (decisão do dono, 05/08/2026)

`MULTI_BOAT_DESTINATIONS` aponta para `MULTI_CINCO_REGIOES_BARCO`, com OLIVINE,
SLATEPORT, VERMILION, VIRBANK, CANALAVE e Sair. Cada marinheiro pula o próprio
destino omitindo o `case`. Não fazer uma lista por porto: é mais código para o
mesmo resultado. O bug de verdade, já consertado, era o `switch` em três casos
lendo um menu de duas entradas.
