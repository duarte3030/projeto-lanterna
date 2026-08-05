# Fontes de região: o que existe, o que serve, e como se prova

Levantado na madrugada de 04 para 05/08/2026. Este documento existe porque o
projeto já perdeu tempo duas vezes com fonte errada: a pipeline que raspava a ROM
de DS e trazia biblioteca de Wi-Fi em vez de tileset, e os 47 mapas de Unova que
eram Petalburg com nome trocado.

**Regra que saiu de tudo isso: região só entra no hack a partir de fonte com dado
2D legível. Nunca a partir de screenshot, promessa de release, ou "esse hack tem".**

Ferramenta para decidir: `dev_scripts/avalia_rom_gba.py rom.gba`. Ela roda três
testes independentes numa ROM de GBA (nomes de lugar no texto, tabela contígua de
nomes, e quantidade e tamanho real dos mapas) e diz se é região implementada ou
troca de nome.

---

## Placar das fontes

| Região | Fonte | Formato | Estado | Serve? |
|---|---|---|---|---|
| Sinnoh | `fontes-mapas/sinnoh` | pokeemerald | port GBA pronto | **sim, já usado** |
| Sinnoh | `fontes-mapas/pokeplatinum` | decomp de DS | texto decodificado, grade 2D | **sim, já usado** |
| Johto | `fontes-mapas/hns` (Heart n Soul) | pokeemerald | demake GBA | **sim, já usado** |
| Johto/Kanto | `pret/pokecrystal` | disassembly gen 2 | 254 mapas em `.blk` | **sim, conversor pronto** |
| Galar | hacks de SwSh em GBA (abaixo) | ROM compilada | região real, 44 bancos | **tecnicamente sim** |
| Unova | nenhuma | — | não existe port nem decomp | **não** |
| Paldea | nenhuma | — | — | **não** |
| Kalos | nenhuma | — | os hacks avaliados sao Hoenn ou Johto renomeados | **nao** |

---

## Galar: é possível, e está provado

Duas ROMs de GBA foram medidas com `avalia_rom_gba.py`:

- `sword-shield-gba-2020-11-25.gba` — base FireRed, 32 MB, **485 mapas em 44 bancos**
- `PKM SwSh ULTIMATE+.gba` — base FireRed, 32 MB, **437 mapas em 44 bancos**

São o mesmo trabalho base; o ULTIMATE+ é fork. As duas passam nos três testes:

1. **14 de 14 nomes de Galar** presentes, com 168 a 192 ocorrências.
2. **Tabela contígua de 8 nomes** no binário, ou seja, região registrada no motor
   e não fala solta. No `sword-shield`, em `0x3EED16`:
   `POSTWICK, Wedgehurst, Motostoke, Turffield, Hulbury, Stow On Side,
   Hammmelock, Ballonlea, Circhester, Wyndon, Spikemuth`, seguido das rotas.
3. **Mapas de tamanho real**: 87 a 94 mapas acima de 1500 tiles, com picos de
   100x47, 90x41 e 82x46. Não é casca.

O hack é em português. Há também nomes de Kanto no texto (Celadon, Saffron), que
são resto do FireRed de base, não conteúdo ativo.

### Como seria a extração, se for feita

Muito mais simples que DS, porque é o mesmo motor: a estrutura de mapa do GBA é a
mesma família do pokeemerald.

- Ponteiro da tabela de bancos do FireRed em `0x5524C`.
- Cada banco é uma lista de ponteiros para cabeçalho de mapa.
- Cabeçalho `+0` aponta o layout; o layout começa com `u32 largura, u32 altura`,
  depois ponteiros de borda, de blocos e dos dois tilesets.
- Os blocos são `u16` por metatile, igual ao `map.bin` do pokeemerald: 10 bits de
  metatile, 2 de colisão, 4 de elevação.

`avalia_rom_gba.py` já lê tudo isso; falta só gravar o `map.bin` e o tileset.

### O que pesar antes de fazer

Estas ROMs não são jogo oficial desmontado: são o trabalho de um hacker
específico, feito de graça, e distribuído compilado sem código-fonte. Portar do
`pokecrystal` ou do `pokeplatinum` é usar o jogo original; copiar daqui é usar o
trabalho de outra pessoa.

Isso não é impedimento técnico e a decisão é do dono do projeto. Mas se Galar
entrar, o mínimo é **creditar o autor** no README e nos créditos do jogo, como o
projeto já faz com o `hns` e o port de Sinnoh.

---

## O que NÃO serve, e por quê (para não se perder tempo de novo)

**`Pokémon Scarlet, Violet & Indigo [COMPLETE].gba`** — é Kanto com nome trocado.
Medido: 43 bancos, exatamente os do FireRed original, 468 mapas contra ~418, e
**zero** nomes de cidade de Paldea. "PALDEA" aparece só em fala, em italiano
("hai salvato PALDEA"), e como forma regional ("WOOPER di PALDEA"). O jogador
anda por Kanto enquanto os NPCs falam de Paldea.

**`x-y-emerald.gba`** — é Hoenn com três cidades renomeadas. Só 4 dos 16 nomes de
Kalos, contra 8 de 8 de Hoenn com 292 ocorrências, e 552 mapas em 34 bancos,
praticamente o Emerald original. A prova está em `0x5A0B95`, DENTRO da tabela de
nomes de Hoenn: `PETALBURG CITY, SLATEPORT CITY, SHALOUR CITY, FORTREE CITY,
LILYCOVE`. Colaram Shalour no lugar de uma cidade de Hoenn.

**`kalos-crystal-2019-04-29.gbc`** — é Johto com a Pokédex de Kalos. Game Boy
Color, 2 MB, exatamente o tamanho do Crystal original. **Zero** nomes de lugar de
Kalos; Johto inteira presente (Goldenrod 42x, Ecruteak 28x). Os 15 Pokémon de
Kalos que testei estão todos lá, e os iniciais de Johto sumiram: Chikorita,
Cyndaquil e Totodile viraram Chespin, Fennekin e Froakie. Mapa é Johto, que já
temos de fonte melhor.

**`monhacks/bwdemake`** — repositório de demake de Black e White. Clonado e
conferido: é pokeemerald puro, 519 mapas de Hoenn, **zero de Unova**.

**Pokémon Liquid Crystal** — tem o esconderijo da Rocket em Mahogany, mas é hack
de FireRed distribuído compilado, sem fonte. O `pokecrystal` tem o mesmo mapa em
`.blk` legível, com dimensão declarada em constante. Fonte melhor, e é o original.

**ROMs de DS (`platinum.nds`, `black.nds`)** — servem para gen 4, onde a decomp
`pokeplatinum` já entrega tudo mastigado, e **não compensam** para gen 5. Detalhe
completo em `DEMAKE-DS.md`: a grade 2D existe no Black 2, o bit de colisão foi
provado em interiores, mas no exterior a regra deixa só 8,7% dos tiles andáveis,
e o formato de altura continua desconhecido.

---

## Ferramentas escritas para isto

| Ferramenta | O que faz |
|---|---|
| `dev_scripts/avalia_rom_gba.py` | Diz se uma ROM de GBA tem região real ou troca de nome |
| `dev_scripts/demake_gen2.py` | Converte mapa do pokecrystal em `map.bin` do pokeemerald, colisão exata |
| `dev_scripts/demake_ds.py` | Converte grade 2D de gen 4 e gen 5 em `map.bin` |
| `dev_scripts/valida_conectividade.py` | Anda o jogo pelo grafo de warps e acha o que prende o jogador |
| `dev_scripts/valida_mapas_sinnoh.py` | Sprite que a build não desenha, NPC fora do mapa, script faltando |
