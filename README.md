# Pokémon Claude

ROM hack de Geração III com múltiplas regiões jogáveis numa campanha só.

Projeto novo, separado do [Pokémon Crystal Harry](https://github.com/duarte3030/pokemon-crystal-harry),
que é Gen II e continua tocando por conta própria.

## Situação

Levantamento feito, base ainda não instalada. Nada foi compilado.

## Base escolhida: pokeemerald-expansion

[rh-hideout/pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion),
que é decompilação de fonte real do Pokémon Emerald com centenas de recursos das
gerações seguintes já portados.

Foi descartada a base do Pokémon Radical Red, que roda em CFRU (Complete FireRed
Upgrade) mais DPE. O CFRU é injeção binária de C no FireRed: herda mecânica de
batalha moderna de graça, mas não entrega código-fonte de verdade. Como o
trabalho pesado deste projeto é mapa em escala industrial, o que importa é ter
build system, refatoração e histórico em git. Por isso, decomp.

## Orçamento de espaço

O teto é conhecido e confortável: uma ROM de GBA expande de 16 MB para 32 MB, e
o FireRed expandido fica com cerca de 24 MB livres.

O custo por região é **estimativa derivada, não medição**. Foi obtida escalando
números medidos de verdade no Crystal Harry, cujo `.map` de linker dá o tamanho
exato de cada seção:

| componente | Gen II medido (Johto + Kanto, 607 mapas) |
|---|---|
| layout de blocos | 58,7 KB |
| scripts e dados de mapa | 23,4 KB |
| texto | 64,7 KB |
| encontros selvagens | 14,3 KB |
| tilesets | 159,6 KB |

Cerca de 320 KB para as duas regiões, ou aproximadamente 160 KB por região em
Gen II. Aplicando os multiplicadores do Gen III (tile de 4bpp em vez de 2bpp,
mapas maiores, muito mais texto, paleta por mapa) mais folga para sprites de
overworld e de treinador, chega-se a **1 a 2 MB por região**.

Quatro regiões custariam algo entre 4 e 8 MB dos 24 MB livres. Mesmo errando por
três vezes para mais, ainda cabe. **Espaço não é o gargalo deste projeto.**

O gargalo é mão de obra: quatro regiões são algo como 600 a 800 telas de mapa
para desenhar, conectar, popular e scriptar. Para comparação, o Crystal Harry
tem 607 mapas e é fruto de anos de trabalho de várias pessoas.

Quando a base estiver compilando, o custo real deixa de ser estimativa: o `.map`
do linker mede seção por seção, do mesmo jeito que foi feito no Crystal Harry.

## Regiões

Sugestão: **Kanto, Johto, Hoenn e Sinnoh**. Todas nasceram em grade 2D com câmera
fixa, então o demake é tradução direta em vez de redesenho.

A dificuldade não é uniforme, e a razão é estrutural:

| região | viabilidade |
|---|---|
| Kanto, Johto, Hoenn | nativas de Gen III ou anteriores, grade 2D |
| Sinnoh | grade 2D, e existe demake de GBA para estudar |
| Unova, Kalos | 3D mas ainda em grade, demake trabalhoso porém possível |
| Alola | quebra a grade |
| Galar | área aberta |
| Paldea | mundo aberto, exigiria redesenhar a região inteira à mão |

### Trabalho anterior encontrado

Levantado por pesquisa, quase tudo vindo de sites agregadores e **não confirmado
em fonte primária**. Vale checar no PokéCommunity antes de apostar em qualquer um.

- **Pokémon Crossroads** (março de 2026): três regiões conectadas, Kanto, Sevii e
  Hoenn, com Johto anunciado. É a prova de conceito mais próxima deste projeto.
- **Pokémon FireEmerald**: Kanto mais Hoenn mais Sevii numa campanha contínua.
- **Pokémon Sinnoh Legacy**: demake de Platinum em engine GBA, 649 Pokémon.
- **Pokémon Fire XY**: uma das poucas com Kalos, em português, inacabada.
- **Pokémon Emerald Crest**: traz as formas regionais de Hisui, Galar e Alola.
  Formas regionais, não as regiões.

Não foi encontrado nenhum hack de Gen III cobrindo Alola, Galar ou Paldea, nem
nenhum cobrindo as quatro primeiras regiões de uma vez.

## Decisões em aberto

1. Confirmar a base pokeemerald-expansion antes de clonar.
2. Fechar quais regiões entram, e em que ordem de produção.
3. Definir se a campanha é contínua com nível escalando entre regiões, ou se cada
   região reinicia a curva.
4. Arrumar a ROM base de Emerald, que a decomp exige para compilar e que precisa
   ser fornecida por você.
