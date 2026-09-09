## Conteúdo de terceiros usado neste hack

### Unova: saiu do cartucho 1 em 07/09/2026

A região de Unova foi portada de **Black and White 3: Genesis**, o projeto
pokecrystal de **Azure_Keys** (github.com/AzureKeys/BW3G), com arte de tiles
creditada pelo autor a **Rangi**, **PiaCarrot**, **Bloodless**, **Bees**,
**JaceDeane**, **Morlock** e **Luna**. Ela **não faz parte deste cartucho**: o
PRD-CARTUCHO-1.md tirou Unova e Galar em 07/09/2026, e nenhum mapa, tileset,
script, texto ou treinador delas ficou nesta ROM. O crédito completo continua
vivo na branch `cartucho-2` e na tag `pre-remocao-unova-galar`, que é onde a
região é jogável.

### Johto: a região inteira, e as portas da rodada 14

Johto veio de **Pokémon Heart & Soul (HnS)**, o demake de HGSS em Modern Emerald
decomp, aberto pelo autor como base para outros hacks. De lá saíram a planta, a
colisão, os warps, os objetos e o texto dos mapas de Johto que este hack traz.
A pasta de trabalho é privada e nunca sai desta máquina.

Em 07/09/2026, para responder à pergunta das 31 portas decorativas de Johto,
outras quatro fontes foram MEDIDAS (nenhum byte de arte ou de mapa foi copiado
delas; o que entrou no hack foi o veredito "esta porta abre em fonte X, aquela
não abre em fonte nenhuma", e as plantas de interior reaproveitadas são as que
este repositório já tinha, vindas do HnS):

- **GS Chronicles**, de Overlord Kaktus / G0LD, pelo decomp público
  `G0LD/GS-Chronicles-Decomp`. O autor credita a Rom Hacking Hideout (RHH) e o
  próprio pokemonHnS. Motor com base no CFRU, que proíbe qualquer monetização.
- **Pokémon Liquid Crystal**, de Linkandzelda, com Zeikku (gráficos),
  Jambo51 (asm) e Magnius (música).
- **Pokémon FireGold** (autoria não confirmada pela ROM; o material local aponta
  TheSnowPeople ou tzx211).
- **Pokémon Scorched Silver**.

O que cada uma disse está registrado, fonte por fonte, no cabeçalho de
`dev_scripts/abre_portas_johto.py` e na seção "As 31 portas de Johto ganham interior" do `ESTADO.md`.

### O cais de CanalaveCity, arte importada do Golden Glazed

Em 06/09/2026, na onda 1 do REFINO, a beira do canal de **CanalaveCity** ganhou
cais de verdade: cabeços de amarração com cabo, boia salva-vidas e estacas. Essa
arte foi extraída da ROM de **Pokémon Golden Glazed** v2.6, o tileset secundário
`0x3DF74C` (a cidade portuária do hack), e são 9 tiles de 8x8 e uma paleta de 16
cores, copiados sem alterar um pixel nem aproximar uma cor.

- **Golden Glazed**, do hacker que assina como *Golden*, derivado do **Pokémon
  Glazed**, de **redriders180** (com **Lucbui** no port decomp público
  `TrainerX493/pokeglazed`). O Glazed original credita a comunidade de
  hackers de tiles do fórum de onde a arte dele veio, e não declara licença.
- A ROM é cópia privada de trabalho e nunca sai desta máquina: o que entrou aqui
  é o **asset convertido**, como manda a regra 1 da seção 4 do `PRD-REFINO.md`.
- O que cada peça é, de onde ela veio e por que ela cabe está no cabeçalho de
  `dev_scripts/porto_canalave_arte.py`, e a medição que escolheu a fonte está em
  `amostras-tileset/refino/novidade-porto.tsv`, fora deste repositório.

O porto anterior da mesma cidade (o bote, o poste e os tambores, de
`dev_scripts/porto_canalave.py`) não veio de hack nenhum: é arte de Hoenn que
este repositório já tinha, do `gTileset_Slateport`.

A arte de base é da Nintendo e da Game Freak. "Livre para usar com crédito" dito
por um hacker cobre a edição dele, não o material original. Nada que descenda de
hack com motor CFRU pode ser monetizado, nem por doação opcional.

## Credits ✨


Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/en/reference/emoji-key/)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AgustinGDLV"><img src="https://avatars.githubusercontent.com/u/103095241?v=4?s=100" width="100px;" alt="AgustinGDLV"/><br /><sub><b>AgustinGDLV</b></sub></a><br /><a href="#maintenance-AgustinGDLV" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=AgustinGDLV" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AlexOn1ine"><img src="https://avatars.githubusercontent.com/u/93446519?v=4?s=100" width="100px;" alt="Alex"/><br /><sub><b>Alex</b></sub></a><br /><a href="#maintenance-AlexOn1ine" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=AlexOn1ine" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Bassoonian"><img src="https://avatars.githubusercontent.com/u/16993385?v=4?s=100" width="100px;" alt="Bassoonian"/><br /><sub><b>Bassoonian</b></sub></a><br /><a href="#maintenance-Bassoonian" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Bassoonian" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/DizzyEggg"><img src="https://avatars.githubusercontent.com/u/16259973?v=4?s=100" width="100px;" alt="DizzyEggg"/><br /><sub><b>DizzyEggg</b></sub></a><br /><a href="#maintenance-DizzyEggg" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=DizzyEggg" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ghoulslash"><img src="https://avatars.githubusercontent.com/u/41651341?v=4?s=100" width="100px;" alt="ghoulslash"/><br /><sub><b>ghoulslash</b></sub></a><br /><a href="#maintenance-ghoulslash" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=ghoulslash" title="Code">💻</a> <a href="#design-ghoulslash" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hedara90"><img src="https://avatars.githubusercontent.com/u/149414898?v=4?s=100" width="100px;" alt="hedara90"/><br /><sub><b>hedara90</b></sub></a><br /><a href="#maintenance-hedara90" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=hedara90" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.martin-griffin.com/"><img src="https://avatars.githubusercontent.com/u/838573?v=4?s=100" width="100px;" alt="Martin Griffin"/><br /><sub><b>Martin Griffin</b></sub></a><br /><a href="#maintenance-mrgriffin" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=mrgriffin" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Pawkkie"><img src="https://avatars.githubusercontent.com/u/61265402?v=4?s=100" width="100px;" alt="Pawkkie"/><br /><sub><b>Pawkkie</b></sub></a><br /><a href="#maintenance-Pawkkie" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Pawkkie" title="Code">💻</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Pawkkie" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SBird1337"><img src="https://avatars.githubusercontent.com/u/3799173?v=4?s=100" width="100px;" alt="Philipp AUER"/><br /><sub><b>Philipp AUER</b></sub></a><br /><a href="#maintenance-SBird1337" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=SBird1337" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tertu-m"><img src="https://avatars.githubusercontent.com/u/836640?v=4?s=100" width="100px;" alt="tertu"/><br /><sub><b>tertu</b></sub></a><br /><a href="#maintenance-tertu-m" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=tertu-m" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://linktr.ee/pkmnsnfrn"><img src="https://avatars.githubusercontent.com/u/77138753?v=4?s=100" width="100px;" alt="psf"/><br /><sub><b>psf</b></sub></a><br /><a href="#maintenance-pkmnsnfrn" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=pkmnsnfrn" title="Code">💻</a> <a href="#projectManagement-pkmnsnfrn" title="Project Management">📆</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/wiz1989"><img src="https://avatars.githubusercontent.com/u/80073265?v=4?s=100" width="100px;" alt="wiz1989"/><br /><sub><b>wiz1989</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=wiz1989" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/PCG06"><img src="https://avatars.githubusercontent.com/u/75729017?v=4?s=100" width="100px;" alt="PCG"/><br /><sub><b>PCG</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=PCG06" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/kittenchilly"><img src="https://avatars.githubusercontent.com/u/23617175?v=4?s=100" width="100px;" alt="kittenchilly"/><br /><sub><b>kittenchilly</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=kittenchilly" title="Code">💻</a> <a href="#research-kittenchilly" title="Research">🔬</a> <a href="#data-kittenchilly" title="Data">🔣</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ExpoSeed"><img src="https://avatars.githubusercontent.com/u/43502820?v=4?s=100" width="100px;" alt="ExpoSeed"/><br /><sub><b>ExpoSeed</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=ExpoSeed" title="Code">💻</a> <a href="#maintenance-ExpoSeed" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/pulls?q=is%3Apr+reviewed-by%3AExpoSeed" title="Reviewed Pull Requests">👀</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/LinathanZel"><img src="https://avatars.githubusercontent.com/u/35115312?v=4?s=100" width="100px;" alt="Linathan"/><br /><sub><b>Linathan</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=LinathanZel" title="Code">💻</a> <a href="#userTesting-LinathanZel" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AsparagusEduardo"><img src="https://avatars.githubusercontent.com/u/2904965?v=4?s=100" width="100px;" alt="Eduardo Quezada"/><br /><sub><b>Eduardo Quezada</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=AsparagusEduardo" title="Code">💻</a> <a href="#data-AsparagusEduardo" title="Data">🔣</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=AsparagusEduardo" title="Documentation">📖</a> <a href="#infra-AsparagusEduardo" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#maintenance-AsparagusEduardo" title="Maintenance">🚧</a> <a href="#projectManagement-AsparagusEduardo" title="Project Management">📆</a> <a href="#promotion-AsparagusEduardo" title="Promotion">📣</a> <a href="#research-AsparagusEduardo" title="Research">🔬</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/pulls?q=is%3Apr+reviewed-by%3AAsparagusEduardo" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=AsparagusEduardo" title="Tests">⚠️</a> <a href="#tutorial-AsparagusEduardo" title="Tutorials">✅</a> <a href="#userTesting-AsparagusEduardo" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/khbsd"><img src="https://avatars.githubusercontent.com/u/26092020?v=4?s=100" width="100px;" alt="khbsd"/><br /><sub><b>khbsd</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=khbsd" title="Documentation">📖</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=khbsd" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Cafeei"><img src="https://avatars.githubusercontent.com/u/46283144?v=4?s=100" width="100px;" alt="Cafe"/><br /><sub><b>Cafe</b></sub></a><br /><a href="#design-Cafeei" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/agsmgmaster64"><img src="https://avatars.githubusercontent.com/u/67435611?v=4?s=100" width="100px;" alt="agsmgmaster64"/><br /><sub><b>agsmgmaster64</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=agsmgmaster64" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/RubyRaven6"><img src="https://avatars.githubusercontent.com/u/178652077?v=4?s=100" width="100px;" alt="Ruby"/><br /><sub><b>Ruby</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=RubyRaven6" title="Code">💻</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=RubyRaven6" title="Documentation">📖</a> <a href="#tool-RubyRaven6" title="Tools">🔧</a> <a href="#tutorial-RubyRaven6" title="Tutorials">✅</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mudskipper13"><img src="https://avatars.githubusercontent.com/u/105766191?v=4?s=100" width="100px;" alt="mudskipper13"/><br /><sub><b>mudskipper13</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=mudskipper13" title="Code">💻</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=mudskipper13" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/surskitty"><img src="https://avatars.githubusercontent.com/u/1383512?v=4?s=100" width="100px;" alt="surskitty"/><br /><sub><b>surskitty</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=surskitty" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/grintoul1"><img src="https://avatars.githubusercontent.com/u/166724814?v=4?s=100" width="100px;" alt="grintoul"/><br /><sub><b>grintoul</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=grintoul1" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bassforte123"><img src="https://avatars.githubusercontent.com/u/130828119?v=4?s=100" width="100px;" alt="bassforte123"/><br /><sub><b>bassforte123</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=bassforte123" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/iriv24"><img src="https://avatars.githubusercontent.com/u/40581123?v=4?s=100" width="100px;" alt="iriv24"/><br /><sub><b>iriv24</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=iriv24" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Bivurnum"><img src="https://avatars.githubusercontent.com/u/147376167?v=4?s=100" width="100px;" alt="Bivurnum"/><br /><sub><b>Bivurnum</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Bivurnum" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Emiliasky"><img src="https://avatars.githubusercontent.com/u/48217459?v=4?s=100" width="100px;" alt="Emilia Daelman"/><br /><sub><b>Emilia Daelman</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Emiliasky" title="Code">💻</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Emiliasky" title="Tests">⚠️</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ravepossum"><img src="https://avatars.githubusercontent.com/u/145081120?v=4?s=100" width="100px;" alt="RavePossum"/><br /><sub><b>RavePossum</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=ravepossum" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fakuzatsu"><img src="https://avatars.githubusercontent.com/u/118256341?v=4?s=100" width="100px;" alt="Zatsu"/><br /><sub><b>Zatsu</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=fakuzatsu" title="Code">💻</a> <a href="#design-fakuzatsu" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/poetahto"><img src="https://avatars.githubusercontent.com/u/11669335?v=4?s=100" width="100px;" alt="poetahto"/><br /><sub><b>poetahto</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=poetahto" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lordraindance2"><img src="https://avatars.githubusercontent.com/u/47706100?v=4?s=100" width="100px;" alt="lordraindance2"/><br /><sub><b>lordraindance2</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=lordraindance2" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pablopenna"><img src="https://avatars.githubusercontent.com/u/11214682?v=4?s=100" width="100px;" alt="Pablo Pena"/><br /><sub><b>Pablo Pena</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=pablopenna" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://tustin2121.github.io/"><img src="https://avatars.githubusercontent.com/u/794812?v=4?s=100" width="100px;" alt="tustin2121"/><br /><sub><b>tustin2121</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=tustin2121" title="Documentation">📖</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=tustin2121" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Ddaretrogamer"><img src="https://avatars.githubusercontent.com/u/131238004?v=4?s=100" width="100px;" alt="Phantonomy"/><br /><sub><b>Phantonomy</b></sub></a><br /><a href="#design-Ddaretrogamer" title="Design">🎨</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://metin2.dev/index.php"><img src="https://avatars.githubusercontent.com/u/42327659?v=4?s=100" width="100px;" alt="Enrico Drago"/><br /><sub><b>Enrico Drago</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Syreldar" title="Documentation">📖</a> <a href="#userTesting-Syreldar" title="User Testing">📓</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Pyredrid"><img src="https://avatars.githubusercontent.com/u/8324784?v=4?s=100" width="100px;" alt="Pyredrid"/><br /><sub><b>Pyredrid</b></sub></a><br /><a href="#userTesting-Pyredrid" title="User Testing">📓</a> <a href="#maintenance-Pyredrid" title="Maintenance">🚧</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Pyredrid" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mvit"><img src="https://avatars.githubusercontent.com/u/128863?v=4?s=100" width="100px;" alt="mv"/><br /><sub><b>mv</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=mvit" title="Code">💻</a> <a href="#design-mvit" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Mother-Of-Dragons"><img src="https://avatars.githubusercontent.com/u/31101124?v=4?s=100" width="100px;" alt="Avara"/><br /><sub><b>Avara</b></sub></a><br /><a href="#data-Mother-Of-Dragons" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Doesnty"><img src="https://avatars.githubusercontent.com/u/6163136?v=4?s=100" width="100px;" alt="Doesnty"/><br /><sub><b>Doesnty</b></sub></a><br /><a href="#design-Doesnty" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/FosterProgramming"><img src="https://avatars.githubusercontent.com/u/178871164?v=4?s=100" width="100px;" alt="FosterProgramming"/><br /><sub><b>FosterProgramming</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=FosterProgramming" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Squeetz"><img src="https://avatars.githubusercontent.com/u/21145213?v=4?s=100" width="100px;" alt="Squeetz"/><br /><sub><b>Squeetz</b></sub></a><br /><a href="#maintenance-Squeetz" title="Maintenance">🚧</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ghostyboyy97"><img src="https://avatars.githubusercontent.com/u/106448956?v=4?s=100" width="100px;" alt="ghostyboyy97"/><br /><sub><b>ghostyboyy97</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=ghostyboyy97" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://hashtagmarky.github.io"><img src="https://avatars.githubusercontent.com/u/143505183?v=4?s=100" width="100px;" alt="Marky"/><br /><sub><b>Marky</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=HashtagMarky" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MandL27"><img src="https://avatars.githubusercontent.com/u/10366615?v=4?s=100" width="100px;" alt="MandL27"/><br /><sub><b>MandL27</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=MandL27" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cawtds"><img src="https://avatars.githubusercontent.com/u/38510667?v=4?s=100" width="100px;" alt="cawtds"/><br /><sub><b>cawtds</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=cawtds" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fdeblasio"><img src="https://avatars.githubusercontent.com/u/35279583?v=4?s=100" width="100px;" alt="Frank DeBlasio"/><br /><sub><b>Frank DeBlasio</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=fdeblasio" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://vriska.dev"><img src="https://avatars.githubusercontent.com/u/8355305?v=4?s=100" width="100px;" alt="leo60228"/><br /><sub><b>leo60228</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=leo60228" title="Documentation">📖</a> <a href="#data-leo60228" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/shachar700"><img src="https://avatars.githubusercontent.com/u/48739719?v=4?s=100" width="100px;" alt="shachar700"/><br /><sub><b>shachar700</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=shachar700" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://purrfectdoodle.com"><img src="https://avatars.githubusercontent.com/u/105788407?v=4?s=100" width="100px;" alt="Eva"/><br /><sub><b>Eva</b></sub></a><br /><a href="#design-purrfectdoodle" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/amiosi"><img src="https://avatars.githubusercontent.com/u/44352097?v=4?s=100" width="100px;" alt="amiosi"/><br /><sub><b>amiosi</b></sub></a><br /><a href="#data-amiosi" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mrdollsteak"><img src="https://avatars.githubusercontent.com/u/5975698?v=4?s=100" width="100px;" alt="mrdollsteak"/><br /><sub><b>mrdollsteak</b></sub></a><br /><a href="#data-mrdollsteak" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/TheXaman"><img src="https://avatars.githubusercontent.com/u/48356183?v=4?s=100" width="100px;" alt="TheXaman"/><br /><sub><b>TheXaman</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=TheXaman" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ZnogyroP"><img src="https://avatars.githubusercontent.com/u/20970593?v=4?s=100" width="100px;" alt="ZnogyroP"/><br /><sub><b>ZnogyroP</b></sub></a><br /><a href="#design-ZnogyroP" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/luckytyphlosion"><img src="https://avatars.githubusercontent.com/u/10688458?v=4?s=100" width="100px;" alt="luckytyphlosion"/><br /><sub><b>luckytyphlosion</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=luckytyphlosion" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ShinyDragonHunter"><img src="https://avatars.githubusercontent.com/u/32826900?v=4?s=100" width="100px;" alt="Josh"/><br /><sub><b>Josh</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=ShinyDragonHunter" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Gamer2020"><img src="https://avatars.githubusercontent.com/u/6243575?v=4?s=100" width="100px;" alt="Gamer2020"/><br /><sub><b>Gamer2020</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Gamer2020" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SonikkuA-DatH"><img src="https://avatars.githubusercontent.com/u/58025603?v=4?s=100" width="100px;" alt="SonikkuA-DatH"/><br /><sub><b>SonikkuA-DatH</b></sub></a><br /><a href="#design-SonikkuA-DatH" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://jaizu.moe"><img src="https://avatars.githubusercontent.com/u/18596778?v=4?s=100" width="100px;" alt="Jaizu"/><br /><sub><b>Jaizu</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Jaizu" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/miriamlefae"><img src="https://avatars.githubusercontent.com/u/206095739?v=4?s=100" width="100px;" alt="Miriam"/><br /><sub><b>Miriam</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=miriamlefae" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Skeli789"><img src="https://avatars.githubusercontent.com/u/17243618?v=4?s=100" width="100px;" alt="Skeli"/><br /><sub><b>Skeli</b></sub></a><br /><a href="#design-Skeli789" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://hufford.io"><img src="https://avatars.githubusercontent.com/u/8021794?v=4?s=100" width="100px;" alt="Josh Hufford"/><br /><sub><b>Josh Hufford</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=ostomachion" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Kasenn"><img src="https://avatars.githubusercontent.com/u/115586266?v=4?s=100" width="100px;" alt="Kasenn"/><br /><sub><b>Kasenn</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Kasenn" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SabataLunar"><img src="https://avatars.githubusercontent.com/u/26584469?v=4?s=100" width="100px;" alt="SabataLunar"/><br /><sub><b>SabataLunar</b></sub></a><br /><a href="#design-SabataLunar" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/PacFire"><img src="https://avatars.githubusercontent.com/u/108960850?v=4?s=100" width="100px;" alt="PacFire"/><br /><sub><b>PacFire</b></sub></a><br /><a href="#design-PacFire" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ChrispyChris27"><img src="https://avatars.githubusercontent.com/u/173648816?v=4?s=100" width="100px;" alt="ChrispyChris27"/><br /><sub><b>ChrispyChris27</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=ChrispyChris27" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/LogicalLlama"><img src="https://avatars.githubusercontent.com/u/248230900?v=4?s=100" width="100px;" alt="LogicalLlama"/><br /><sub><b>LogicalLlama</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/issues?q=author%3ALogicalLlama" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/KnightGallade"><img src="https://avatars.githubusercontent.com/u/189022270?v=4?s=100" width="100px;" alt="KnightGallade"/><br /><sub><b>KnightGallade</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/issues?q=author%3AKnightGallade" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/luuma"><img src="https://avatars.githubusercontent.com/u/31407427?v=4?s=100" width="100px;" alt="luuma"/><br /><sub><b>luuma</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=luuma" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/DragonScaledEmma"><img src="https://avatars.githubusercontent.com/u/220702264?v=4?s=100" width="100px;" alt="Emma"/><br /><sub><b>Emma</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/issues?q=author%3ADragonScaledEmma" title="Bug reports">🐛</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Gammel2013"><img src="https://avatars.githubusercontent.com/u/160730477?v=4?s=100" width="100px;" alt="gammel2013"/><br /><sub><b>gammel2013</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/issues?q=author%3Agammel2013" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/BluSunrize"><img src="https://avatars.githubusercontent.com/u/4106382?v=4?s=100" width="100px;" alt="blusunrize"/><br /><sub><b>blusunrize</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/issues?q=author%3Ablusunrize" title="Bug reports">🐛</a> <a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=blusunrize" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jtebbe"><img src="https://avatars.githubusercontent.com/u/15947257?v=4?s=100" width="100px;" alt="jtebbe"/><br /><sub><b>jtebbe</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=jtebbe" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Liamjd14"><img src="https://avatars.githubusercontent.com/u/175732139?v=4?s=100" width="100px;" alt="Liam"/><br /><sub><b>Liam</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Liamjd14" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Gastly92"><img src="https://avatars.githubusercontent.com/u/262681076?v=4?s=100" width="100px;" alt="Gastly92"/><br /><sub><b>Gastly92</b></sub></a><br /><a href="https://github.com/rh-hideout/pokeemerald-expansion/commits?author=Gastly92" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/montmoguri"><img src="https://avatars.githubusercontent.com/u/202215938?v=4?s=100" width="100px;" alt="Montblanc"/><br /><sub><b>Montblanc</b></sub></a><br /><a href="#design-montmoguri" title="Design">🎨</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
This project follows the [all-contributors](https://github.com/all-contributors/allcontributors.org) specification. Contributions of any kind welcome!

## Other Credits
### Mega Evolution Overworld Sprite Credits:
- [princess-phoenix](https://www.deviantart.com/princess-phoenix)
- [larryturbo](https://www.deviantart.com/larryturbo)
- [kidkatt](https://www.deviantart.com/kidkatt)

## Resources
- [Sugimori Palettes and Sprites](https://www.pokecommunity.com/showthread.php?t=336945)
- [DS Style Gen VI Sprites](https://www.pokecommunity.com/showthread.php?t=314422)
- [Gen VII and Beyond Sprites](https://www.pokecommunity.com/showthread.php?t=368703)
- Some icons ripped from [Pokemon Gaia](https://www.pokecommunity.com/showthread.php?t=326118)
- [Data Files](https://www.pokecommunity.com/showthread.php?t=417909)
- [Complete FireRed Upgrade](https://github.com/Skeli789/Complete-Fire-Red-Upgrade)
- [pokeemerald](https://github.com/pret/pokeemerald/)

### Trilha sonora de Johto (HGSS) e de Sinnoh (DPPt/Platinum), 06/09/2026

As 158 sequências `.mid`, os 83 voicegroups e as 324 amostras de som que fazem
Johto tocar música de HeartGold/SoulSilver e Sinnoh tocar música de
Diamond/Pearl/Platinum vieram do pacote de faixas de:

- **CyanSMP64**, autor do porte das sequências de DS para o motor m4a do GBA.
  Esse rearranjo faixa a faixa é o trabalho caro (a comunidade estima de 1 a 4
  horas por faixa) e é dele que todo mundo copia;
- **resetes12**, do **Modern Emerald**, que consolidou e numerou o pacote;
- **Lil Dill**, do **Pokémon Heart & Soul (HnS)**, que é a cópia de onde este
  hack importou de fato, e de onde também saíram as durações de cada jingle na
  tabela `sFanfares[]` de `src/sound.c`.

Os jingles de HGSS (subir de nível, item, item chave, insígnia, TM, evolução,
cura, avaliação da Pokédex) substituem os de Hoenn no jogo inteiro.

**Nenhuma dessas fontes declara licença, e a música é copyright de
Nintendo/Game Freak/Creatures.** Vale aqui a mesma regra de todo o ecossistema
pret e de todo o resto deste arquivo: **este projeto distribui patch, NUNCA
ROM.** Uma ROM montada contém o áudio original e não pode ser compartilhada,
publicada, vendida nem enviada a terceiros em nenhuma circunstância.

## Arte de mapa importada de ROM hacks

Este projeto é **privado e não monetizado**. A arte de base é da Nintendo/Game Freak; o
crédito abaixo cobre a edição feita por cada autor de ROM hack, e vale para todo asset
convertido que descende dela.

### Kit de neve de `SnowpointCity` (`gTileset_Snowpoint`, metatiles 680 a 690)

Os 14 tiles 8x8, a paleta 6 e os 11 metatiles de chão de neve (banco de neve, beirada,
crista, rastro e muda de pinheiro) vieram do secundário `0x3DF7AC` da cidade de neve do
**Pokémon Golden Glazed v2.6**, de **'Golden'**, que por sua vez é derivado do **Pokémon
Glazed**, de **redriders180** e **Lucbui** (port decomp público em
`github.com/TrainerX493/pokeglazed`). Nenhum id de flag, var, script ou música foi
importado: só arte.

### Segunda passada de `SnowpointCity`: pinheiros, boneco de neve e poste (`gTileset_Snowpoint`, metatiles 691 a 707)

Em 07/09/2026, na onda 1c do REFINO, `SnowpointCity` ganhou duas silhuetas novas de
pinheiro, um arbusto sob neve, um poste de ferro e um boneco de neve. São 35 tiles 8x8,
17 metatiles e a vaga de paleta 10 do secundário. A arte vem de **duas** ROM hacks
privadas, e o que entra neste repositório é sempre o **asset convertido**, nunca a ROM
(regra 1 da seção 4 do `PRD-REFINO.md`). Nenhum id de flag, var, script ou música foi
importado: só arte.

- Os pinheiros (metatiles 13, 14, 21, 22, 133 e 141), o arbusto sob neve (25) e o poste
  de ferro (159 e 230) saíram do secundário `0x3DF7AC` do **Pokémon Golden Glazed v2.6**
  (md5 `f602010e5769fc0454fca4cc8eb77a4b`), do hacker que assina como **'Golden'**, que
  por sua vez é derivado do **Pokémon Glazed**, de **redriders180** (com **Lucbui** no
  port decomp público `github.com/TrainerX493/pokeglazed`). O Glazed original não declara
  licença; o crédito segue a seção de créditos dele.
- O boneco de neve (metatiles 70, 71 e 78) saiu do secundário `0x4924B4` do **Pokémon
  Scorched Silver v1.3 Complete** (md5 `f7af51cecd3e170cc373fba01753053c`), de **Sloo**.
  Esse hack não declara licença própria e a base dele pede crédito à **Rom Hacking
  Hideout (RHH)**, pelo `pokeemerald-expansion`, que é o mesmo motor deste repositório.

A arte de base continua sendo da **Nintendo/Game Freak**: o crédito acima cobre a edição
feita por cada autor de ROM hack. Este projeto é privado, não monetizado, e distribui
patch, nunca ROM.

### Silhueta de porto de `CanalaveCity`: farol, veleiro e engradado (`gTileset_Canalave`, metatiles 832 a 890)

Esta seção é auto-contida e cobre a onda 1c do REFINO, frente CANALAVE.

Os 136 tiles 8x8 e as três paletas novas do `gTileset_Canalave` (vagas 10, 11 e 12,
liberadas pelo reempacotamento de paleta do `dev_scripts/compacta_paletas.py`) vieram
de duas ROM hacks, e nada além de ARTE foi importado: nenhum id de flag, var, script,
música, treinador ou espécie.

- O **veleiro** (16 células, 15 cores, vaga de paleta 10) e o **farol** (39 células,
  15 cores, vaga 11) vieram do tileset secundário `0x3DF92C` do **Pokémon Golden
  Glazed v2.6**, do hacker que assina como **'Golden'**, que por sua vez é derivado do
  **Pokémon Glazed**, de **redriders180** e **Lucbui** (port decomp público em
  `github.com/TrainerX493/pokeglazed`). Md5 da cópia privada de trabalho:
  `f602010e5769fc0454fca4cc8eb77a4b`.
- O **engradado** 2 por 2 (24 células, 5 cores, vaga 12) veio do tileset
  secundário `0x4929B4` do
  **Pokémon Scorched Silver v1.3 Complete**, de **Sloo**, construído sobre o
  **pokeemerald-expansion** da **RHH (Rom Hacking Hideout)**, a quem a base pede
  crédito. Md5 da cópia privada de trabalho: `f7af51cecd3e170cc373fba01753053c`.

Nenhuma das duas ROMs entra neste repositório, nem em parte nem em dump: o que está
versionado é o kit já CONVERTIDO, em
`dev_scripts/porto_canalave_silhueta_kit.json` (paleta em RGB e tile em nibble), e o
script que o instala. A arte de base é da Nintendo/Game Freak; o crédito acima cobre a
edição feita por cada autor de ROM hack. Projeto privado e não monetizado.

### Ruína de `CelesticTown` e campo de `SolaceonTown` (`gTileset_Celestic`, metatiles 774 a 832)

Esta seção é auto-contida e cobre a onda 2 do REFINO, frente CELESTIC e SOLACEON.

Os 100 tiles 8x8 e as duas vagas de paleta novas do `gTileset_Celestic` (a vaga 10, que
já estava livre, e a vaga 7, liberada pela fusão das cinco cores dela dentro dos dois
índices ociosos da vaga 9) vieram de UMA ROM hack, e nada além de ARTE foi importado:
nenhum id de flag, var, script, música, treinador ou espécie.

- **Pokémon Light Platinum**, de **WesleyFG** (versão Final de 2012, base Ruby/AXVE,
  md5 da cópia privada de trabalho `7fd2c08735459d99fa23fdaa9b755486`). O hack não
  declara licença formal; o tópico "WesleyFG Tile's" na PokéCommunity libera os tiles
  **com crédito**, e é isso que esta seção faz.
  - O tema de **ruína** de `CelesticTown` (laje solta, cascalho, pedra rachada,
    pedregulho, monte de pedra, árvore morta, muro caído e a laje do altar: 10 cores
    não-zero na vaga de paleta 10) saiu do tileset secundário `0x286F64`, o da montanha
    do templo, com o primário `0x286CF4`.
  - O tema de **campo** de `SolaceonTown` (broto de plantação, terra batida, tufo de
    capim, medão de feno, fardo de palha, fardo redondo em três tons, monte de palha,
    palheiro largo e duas árvores douradas: 15 cores não-zero na vaga de paleta 7) saiu
    do tileset secundário `0x286DE4`, o da vila verde, com o mesmo primário.

A ROM não entra neste repositório, nem em parte nem em dump: o que está versionado é o
kit já CONVERTIDO, em `dev_scripts/campo_celestic_kit.json` (paleta em RGB e tile em
nibble, já reindexado para a vaga nova), e o script que o instala,
`dev_scripts/campo_celestic.py`. A arte de base é rip de Diamond/Pearl/Platinum, ou
seja da **Nintendo/Game Freak**: o crédito acima cobre a edição feita pelo autor do
hack, não o material original. Projeto privado, não monetizado, que distribui patch e
nunca ROM.

### Pedreira de `OreburghCity` e mato de `EternaCity` (`gTileset_Jubilife`, metatiles 899 a 939)

Esta seção é auto-contida e cobre a onda 2 do REFINO, frente MINA + FLORESTA.

Os 82 tiles 8x8 novos do `gTileset_Jubilife` e as cores novas das vagas de paleta 7,
8 e 11 vieram de UMA ROM hack, e nada além de ARTE foi importado: nenhum id de flag,
var, script, música, treinador ou espécie, e o comportamento de todo metatile novo
entra ZERADO.

- O **chão de cascalho** de Oreburgh (nove variantes de piso), as **pedras**, os
  **pedregulhos**, as **pilhas de minério**, os **engradados**, as **vigas de
  madeira** e o **matação** 2 por 2 vieram do tileset secundário `0x286E8C` do
  **Pokémon Light Platinum**, de **WesleyFG**, sobre base **Pokémon Ruby (AXVE)**.
  É o par da pedreira a céu aberto do grupo 24 do hack (mapa de amostra g24m09,
  44 por 80). Md5 da cópia privada de trabalho:
  `7fd2c08735459d99fa23fdaa9b755486`.
- O **tronco caído** e o **galho caído** de Eterna vieram do tileset secundário
  `0x286FAC` da mesma ROM, o par da floresta densa (mapa de amostra g24m04).
- O resto do mato de Eterna (tufos, moitas, flores, pedras de mato, copa) NÃO é
  importado: são metatiles que o próprio `gTileset_GeneralSinnoh` deste repositório
  já tinha desenhados e que nenhum mapa usava.

O **Light Platinum** não declara licença própria. A arte de base é da
**Nintendo/Game Freak**; o crédito acima cobre a edição feita pelo autor da ROM hack.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está versionado
é o kit já CONVERTIDO, em `dev_scripts/mina_oreburgh_kit.json` (paleta em RGB e tile
em nibble), e o script que o instala. Projeto privado e não monetizado.

### Metrópole de `JubilifeCity` (`gTileset_RustboroSinnoh`, metatiles 872 a 908)

Esta seção é auto-contida e cobre a onda 2 do REFINO, frente METRÓPOLE.

Os 27 tiles 8x8 novos do `gTileset_RustboroSinnoh` e as cores novas das vagas de
paleta 7, 8 e 9 vieram de UMA ROM hack, e nada além de ARTE foi importado: nenhum id
de flag, var, script, música, treinador ou espécie, e o comportamento de todo metatile
novo entra ZERADO.

- O **calçamento de praça** (miolo de paralelepípedo, as quatro faixas de moldura e
  os quatro cantos), o **passeio liso**, o **hidrante** em três variantes, a **grade**,
  o **arbusto largo**, o **banco de praça** e o **vaso com arbusto** e **com pinheiro**
  vieram do tileset secundário `0x286DB4` do **Pokémon Light Platinum**, de
  **WesleyFG**, sobre base **Pokémon Ruby (AXVE)**. É o par da metrópole do grupo 0 do
  hack (mapa de amostra g00m10, 54 por 44). Md5 da cópia privada de trabalho:
  `7fd2c08735459d99fa23fdaa9b755486`.
- A montagem de cada peça foi lida do MAPA do hack e não do atlas: a moldura da praça
  saiu das contagens de par do g00m10, e o arbusto largo e os dois vasos saíram dos
  pares que o hack usa de verdade.

O **Light Platinum** não declara licença própria; o tópico "WesleyFG Tile's" na
PokéCommunity libera os tiles com crédito, e é isso que esta seção faz. A arte de base
é rip de Diamond/Pearl/Platinum, ou seja da **Nintendo/Game Freak**: o crédito acima
cobre a edição feita pelo autor da ROM hack, não o material original.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está versionado é
o kit já CONVERTIDO, em `dev_scripts/metropole_jubilife_kit.json` (paleta em RGB e tile
em nibble, já reindexado para a vaga nova), e o script que o instala,
`dev_scripts/metropole_jubilife.py`. Projeto privado e não monetizado, que distribui
patch e nunca ROM.

### Praia de `SandgemTown` e mato de `TwinleafTown` (`gTileset_PetalburgSinnoh`, metatiles 720 a 745)

Esta seção é auto-contida e cobre a onda 2 do REFINO, frente COSTA.

Os 38 tiles 8x8 novos do `gTileset_PetalburgSinnoh` e as cores novas das vagas de
paleta 6, 7 e 11 vieram de UMA ROM hack, e nada além de ARTE foi importado: nenhum
id de flag, var, script, música, treinador ou espécie, e o comportamento de todo
metatile novo entra ZERADO.

- As oito **variantes de areia** do caminho (areia ondulada, salpicada,
  pontilhada, marcada e as quatro dunas de canto), o **coqueiro** de duas por duas
  células, as **moitas**, os **arbustos**, o **capim baixo**, as **pedras** e a
  **flor azul** vieram do par de tilesets `0x286CF4` (primário de exterior) e
  `0x286D54` (secundário) do **Pokémon Light Platinum**, de **WesleyFG**, sobre
  base **Pokémon Ruby (AXVE)**. É o par da vila costeira do hack (mapas de amostra
  g00m01, 78 por 60, com praia e coqueiral, e g00m37, 40 por 40, a vila verde com
  caminho de areia). Md5 da cópia privada de trabalho:
  `7fd2c08735459d99fa23fdaa9b755486`.
- O **mato das duas cidades** (moita clara, tufo fundo, tufo claro, tufo torto,
  moita cerrada e os quatro espelhos horizontais deles) NÃO é importado: são
  metatiles que o próprio `gTileset_GeneralSinnoh` deste repositório já tinha
  desenhados sobre a grama do metatile 1, com o atributo idêntico ao dele, e que
  nenhuma das duas cidades usava. O mesmo vale para o arbusto de flor vermelha, os
  dois pedregulhos e a placa, que já estavam em COVERED com comportamento zerado.

O **Light Platinum** não declara licença própria. A arte de base é da
**Nintendo/Game Freak**; o crédito acima cobre a edição feita pelo autor da ROM hack.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está versionado
é o kit já CONVERTIDO, em `dev_scripts/costa_sandgem_kit.json` (paleta em RGB e tile
em nibble), e o script que o instala. Projeto privado e não monetizado.

### Praia e penhasco de `CianwoodCity` (`gTileset_CianwoodCity`, metatiles 880 a 932)

Esta seção é auto-contida e cobre a onda 3 do REFINO, frente JOHTO, cidade CIANWOOD.

Os 30 tiles 8x8 novos do `gTileset_CianwoodCity` e as cores novas das vagas de paleta
7 e 10 vieram de UMA ROM hack, e nada além de ARTE foi importado: nenhum id de flag,
var, script, música, treinador ou espécie, e o comportamento de todo metatile novo
entra ZERADO.

- O **coqueiro** (em duas alturas), a **areia molhada** da beira do mar, o
  **pedregulho de granito** (em três silhuetas) e o **poste de luz** vieram do par de
  tilesets `0x49240C` (primário de exterior) e `0x492AD4` (secundário) do **Pokémon
  Scorched Silver v1.3 Complete**, de **Sloo**, construído sobre o
  **pokeemerald-expansion** da **RHH (Rom Hacking Hideout)**, a quem a base pede
  crédito. É o par da vila de praia do hack (mapa de amostra g00m15, 60 por 50, com
  coqueiral, penhasco e areia). Md5 da cópia privada de trabalho:
  `f7af51cecd3e170cc373fba01753053c`.
- A **textura do penhasco** (as três rochas em quatro orientações cada), a **areia
  seca e a areia úmida** da vila e as dezesseis misturas de tom entre as duas NÃO são
  importadas: são metatiles que o próprio `gTileset_JohtoNorthEast` deste repositório
  já tinha desenhados, reassentados sobre a base do carimbo de cada família e girados
  pelos bits de espelho que a entrada de metatile já carrega. O mesmo vale para a
  **placa de madeira** e os dois **postes de madeira**, que saíram da camada de cima
  de metatiles nossos que nenhum dos cinco mapas do tileset usava.
- A rocha e a areia do hack foram MEDIDAS antes de serem descartadas como tapete: a
  rocha dele é rosada, (216,176,160) contra os (192,168,120) da nossa, e importá-la
  como mancha deixaria retalho de outro matiz no meio do penhasco.

O **Scorched Silver** não declara licença própria. A arte de base é da
**Nintendo/Game Freak**; o crédito acima cobre a edição feita pelo autor da ROM hack.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está versionado é
o kit já CONVERTIDO, em `dev_scripts/costa_cianwood_kit.json` (paleta em RGB e tile em
nibble, já reindexado para a vaga nova), e o script que o instala,
`dev_scripts/costa_cianwood.py`. Projeto privado e não monetizado, que distribui patch
e nunca ROM.

### Cratera de `BlackthornCity` (`gTileset_Blackthorn`, metatiles 791 a 805)

Esta seção é auto-contida e cobre a onda 3 do REFINO, frente JOHTO, cidade de
Blackthorn.

Os 52 tiles 8x8 novos do `gTileset_Blackthorn` e as 12 cores da vaga de paleta 7
vieram de UMA ROM hack, e nada além de ARTE foi importado: nenhum id de flag, var,
script, música, treinador ou espécie, e o comportamento de todo metatile novo entra
ZERADO.

- As **nove variantes de piso da cratera** (cascalho claro e escuro, terra batida,
  riscada e ondulada, seixo redondo e grande, laje solta e partida), o
  **pedregulho** cinza, os **dois montes de minério** e o **pilar de rocha** vieram
  do par de tilesets `0x492964` (primário) e `0x492784` (secundário) do **Pokémon
  Scorched Silver** v1.3 Complete, de **Sloo**, construído sobre o
  **pokeemerald-expansion** da **Rom Hacking Hideout (RHH)**, base **Pokémon
  Emerald (BPEE)**. É o par da caverna de rocha avermelhada do grupo 25 do hack
  (mapa de amostra g25m18, 9 por 15). Md5 da cópia privada de trabalho:
  `f7af51cecd3e170cc373fba01753053c`.
- A **tinta de chão das nove variantes de piso NÃO é a da fonte**: as quatro cores
  do chão da caverna do hack ((208,168,136), (176,136,112), (152,104,88) e
  (128,80,64), medidas nos dois metatiles de chão liso dele) foram trocadas, posto
  a posto por luminância, pelas quatro cores da areia do nosso metatile 217
  ((230,222,164), (213,197,131), (197,172,106) e (172,148,74)). O que veio da fonte
  com o RGB exato é só o detalhe: os quatro cinzas do cascalho e do pedregulho e os
  quatro ocres do minério.
- O **pedregulho**, os **montes de minério** e o **pilar** entram por MÁSCARA: o que
  se importa é a diferença entre o metatile da peça e o metatile de chão liso da
  própria fonte, e o fundo é o nosso metatile 217 entrada por entrada.
- O **restante do mobiliário NÃO é importado**: a rocha (metatiles 696 e 697), o
  galho e o tronco secos (688 e 689) e as duas pedras pontudas (680 e 681) já
  estavam desenhados no próprio `gTileset_Blackthorn` sobre a areia do 217, e
  nenhum dos quatro mapas do tileset os usava. O mesmo vale para o barro do chão
  (metatiles 178 e 179 do `gTileset_JohtoNorthEast`) e para as três variantes de
  rocha de montanha do platô (107, 109 e 187), que já existiam com o atributo
  idêntico ao do carimbo que substituem.

O **Scorched Silver** não declara licença própria; o pokeemerald-expansion da RHH é
aberto e pede crédito, e é isso que esta seção faz. A arte de base é rip e edição de
Pokémon Gold/Silver e Emerald, ou seja da **Nintendo/Game Freak**: o crédito acima
cobre a edição feita pelo autor da ROM hack, não o material original.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está versionado
é o kit já CONVERTIDO, em `dev_scripts/cratera_blackthorn_kit.json` (paleta em RGB e
tile em nibble, já reindexado para a vaga nova), e o script que o instala,
`dev_scripts/cratera_blackthorn.py`. Projeto privado e não monetizado, que distribui
patch e nunca ROM.

### Brejo de `PastoriaCity` (`gTileset_LilycoveSinnoh`, metatiles 904 a 930)

Esta seção é auto-contida e cobre a onda 2 do REFINO, frente BREJO.

Os 61 tiles 8x8 novos do `gTileset_LilycoveSinnoh` e as cores novas das vagas de
paleta 6, 7 e 10 vieram de UMA ROM hack, e nada além de ARTE foi importado: nenhum
id de flag, var, script, música, treinador ou espécie, e o comportamento de todo
metatile novo entra ZERADO.

- Os quatro **chãos de lama** (lama salpicada, lama batida, lama funda e lodo), os
  sete **chãos de poça** (poça rasa, poça larga, água parada, poça funda, filme de
  musgo, lodo na água e beira de poça), a **samambaia**, os dois **juncos
  rasteiros**, a **moita de musgo**, a **estaca de cerca** do safári, a **pedra de
  brejo**, o **junco alto** de duas células, a **raiz exposta** e o **tronco caído**
  vieram do par de tilesets `0x286CF4` (primário de exterior) e `0x286FAC`
  (secundário) do **Pokémon Light Platinum**, de **WesleyFG**, sobre base **Pokémon
  Ruby (AXVE)**. É o par do brejo do hack, o mapa de amostra g24m04 (46 por 94), uma
  rota de pântano com lodo, passarela de madeira, junco e tronco caído. Md5 da cópia
  privada de trabalho: `7fd2c08735459d99fa23fdaa9b755486`.
- Os **tufos de grama** (moita clara, tufo fundo, tufo claro, tufo torto, moita
  cerrada e os quatro espelhos horizontais deles) e o **pedregulho** NÃO são
  importados: são metatiles que o próprio `gTileset_GeneralSinnoh` deste repositório
  já tinha desenhados sobre a grama do metatile 1, com o atributo idêntico ao dele. A
  razão de não importar a grama do hack é COR e não economia: a grama do Light
  Platinum é (136,184,80) e a nossa é (115,197,164), 90 de distância RGB, e uma
  mancha dessas ao lado do carimbo vira remendo.

O que ficou de fora, e por quê:

- A **areia** e a **terra** do hack (metatiles 71 a 94 do secundário), por distância
  de cor: 82,4 da nossa clareira, sem nenhuma borda de transição desenhada.
- A **passarela de madeira** (metatiles 132 a 134 e 140 a 142) e a **cerca** inteira
  (109, 110, 124 a 126), porque as duas são estruturas LINEARES e o gerador desta
  onda cresce bolha, não linha. Sobreviveu ao corte só a estaca solta, o metatile
  125, que é peça de uma célula.
- O **pedregulho** do hack (metatile 31 do secundário), porque ele pinta com a paleta
  3 do hack, que é uma paleta do primário dele: importá-la pediria uma quarta vaga e
  as três que sobravam já estavam pagas. No lugar dele entra o nosso metatile 224.
- A **moita de brejo** (o par 100/99), porque a arte dela mora quase toda na camada de
  baixo e com a regra desta passada ela chegaria como uma lasca de 48 pixels.

O **Light Platinum** não declara licença própria. A arte de base é da
**Nintendo/Game Freak**; o crédito acima cobre a edição feita pelo autor da ROM hack.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está versionado
é o kit já CONVERTIDO, em `dev_scripts/brejo_pastoria_kit.json` (paleta em RGB e tile
em nibble, já reindexado para a vaga nova), e o script que o instala,
`dev_scripts/brejo_pastoria.py`. Projeto privado e não monetizado, que distribui patch
e nunca ROM.

### Orla de `SunyshoreCity` (`gTileset_Sunnyshore`, metatiles 730 a 756)

Esta seção é auto-contida e cobre a onda 2 do REFINO, frente ORLA.

Os 38 tiles 8x8 novos do `gTileset_Sunnyshore` e as cores novas das vagas de paleta
6, 7 e 8 vieram de UMA ROM hack, e nada além de ARTE foi importado: nenhum id de
flag, var, script, música, treinador ou espécie, e o comportamento de todo metatile
novo de móvel entra ZERADO, com `layerType` COVERED.

- O **vocabulário de cais** (boia salva-vidas, cabo de amarração laranja e azul,
  poste de amarração, pilar de corrimão, tambor de cais, balde do pescador,
  guarda-sol fechado, quadro de avisos, poste do cais e o **poste de luz** de duas
  células) veio do par `0x286CF4` (primário de exterior) e `0x286D54` (secundário
  costeiro) do **Pokémon Light Platinum**, de **WesleyFG**, sobre base **Pokémon
  Ruby (AXVE)**. É o mesmo par que a frente COSTA usou para a praia de Sandgem, e
  as peças são outras: aqui entrou só o que Sunyshore pedia e o demake não tinha.
  Md5 da cópia privada de trabalho: `7fd2c08735459d99fa23fdaa9b755486`.
- Os **quatro tiles de terra moteada** com que as sete variantes de chão de terra
  são montadas vieram do MESMO hack e do MESMO primário, mas de outro secundário
  dele, o `0x286E8C` (o par aparece em 31 mapas do hack). São quatro tiles 8x8 e uma
  paleta; as sete silhuetas saem de arranjos e espelhos deles.
- As **seis variantes de chão da passarela** (prancha larga, prancha e junta, junta
  e prancha, prancha alternada e a inversa, chapa pontilhada) NÃO são importadas:
  são arranjos de tiles que os NOSSOS dois tilesets deste mapa já tinham desenhados
  (a prancha estreita `0x293` do próprio carimbo, a prancha larga `0xE3` e a chapa
  pontilhada `0x116` e `0x2ED` do `gTileset_GeneralSinnoh`). Custam zero tile e zero
  cor. O motivo de não serem importadas está medido no docstring do
  `dev_scripts/orla_sunyshore.py`: entre as 17 ROM hacks da pasta privada não há UM
  chão que case com a prancha branca desta cidade, e todos os que casam de cor são
  tileset de NEVE.

O **Light Platinum** não declara licença própria. A arte de base é da
**Nintendo/Game Freak**; o crédito acima cobre a edição feita pelo autor da ROM hack.

O que ficou de fora, e por quê: a **palmeira** e o **guarda-sol aberto** do hack
(Sunyshore é a cidade do farol no leste frio de Sinnoh, e o demake desenhou pinheiro
na borda oeste do mapa), e os **botes** e o **cais sobre água** (pediriam solidificar
célula de água, que é a superfície de Surf que liga a cidade à Route 223, e isso pede
um portão de alcance da água que esta passada não escreveu).

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está versionado
é o kit já CONVERTIDO, em `dev_scripts/orla_sunyshore_kit.json` (paleta em RGB e tile
em nibble, já reindexado para a vaga nova), e o script que o instala,
`dev_scripts/orla_sunyshore.py`. Projeto privado e não monetizado, que distribui
patch e nunca ROM.

### Calçada de `GoldenrodCity` (`gTileset_Goldenrod`, metatiles 640, 651, 680 e 681)

Esta seção é auto-contida e cobre a onda 3 do REFINO (Johto), frente Goldenrod.

Os 8 tiles 8x8 novos do `gTileset_Goldenrod` vieram de UMA ROM hack, e nada além de
ARTE foi importado: nenhum id de flag, var, script, música, treinador ou espécie.
**Nenhuma cor entrou.** Esta é a diferença desta seção para todas as outras deste
arquivo: o `gTileset_Goldenrod` tem ZERO orçamento de paleta (medido cor a cor, a
menor união de um par de vagas em uso é 25 cores e uma vaga cabe 15, então nenhum par
cabe junto e a repactuação é impossível), e por isso **as dezesseis paletas do
secundário saem byte a byte idênticas** e a arte importada foi reindexada para cores
que o cartucho já tinha.

- O **calçamento em losango** e o **bueiro** vieram do par `0x49240C` (primário) e
  `0x492484` (secundário da metrópole densa) do **Pokémon Scorched Silver** v1.3
  Complete, de **Sloo**, sobre base **Pokémon Emerald (BPEE)**, split 512/512/6. O
  losango é o metatile local 105 daquele secundário, inteiro; o bueiro é o local 119,
  tirado por MÁSCARA contra o piso liso 108 da própria fonte, ou seja só a tampa
  redonda entra e o fundo é a nossa calçada. Md5 da cópia privada de trabalho:
  `f7af51cecd3e170cc373fba01753053c`. O autor do hack credita a **RHH**
  (`pokeemerald-expansion`).
- A TINTA É NOSSA, e é assim que a importação cabe sem gastar cor. Os quatro tons do
  losango da fonte foram trocados posto a posto, por luminância, pelos quatro bege da
  **paleta 5 do nosso primário `gTileset_JohtoGeneral`**, que é a paleta em que o
  próprio calçamento 363 da cidade já pinta:

      (240,192,96) -> (230,222,164)      (200,144,80) -> (197,172,106)
      (224,168,48) -> (213,197,131)      (192,128,56) -> (172,148,74)

  O quarto tom, `(172,148,74)`, já estava na paleta 5 e nenhum pixel da cidade o
  usava; é ele que dá a junta do losango. Os dois cinzas da tampa do bueiro caem na
  mesma paleta 5, e um deles cai EXATO: `(96,96,120) -> (88,88,112)` e
  `(64,72,104) -> (64,72,104)`.
- As **três direções do calçamento** (losango, losango espelhado e losango deitado)
  são a MESMA peça importada, escrita com os bits 10 e 11 de espelho das entradas de
  metatile: custam ZERO tile a mais. A distância RGB média entre elas foi medida e
  vale 26,5, 26,6 e 42,2, contra o piso de 8,0 da onda.
- O **mobiliário urbano** (canteiro de flores, arbusto, duas lixeiras, máquina de
  rua, bicicleta e placa) **NÃO é importado**: são os metatiles 828, 831, 1003, 1004,
  1005, 1006 e 829, que já estavam compilados dentro do `gTileset_Goldenrod`, já
  desenhados sobre a calçada bege e já com `layerType` COVERED, e que a cidade usava
  no máximo três vezes cada um. Custam zero byte, zero tile e zero cor.

O **Scorched Silver** não declara licença própria. A arte de base é da
**Nintendo/Game Freak**; o crédito acima cobre a edição feita pelo autor da ROM hack.

O que ficou de fora, e por quê, porque olhar e recusar também é resultado: a **praça
de laje cinza** da fonte (locais 99 a 117) foi montada, repintada na paleta 1 do nosso
primário e desenhada dentro de um tapete de calçada, e lê como JANELA e não como
praça, porque a moldura clara em volta de um cinza chapado vira buraco no chão; o
**gradil de aço** (locais 48 a 66) some no recorte, dá borrão de cinza solto de 60 a
170 pixels, e a cidade já tem guarda-corpo próprio; e o tileset `0x492ABC`, que o
briefing chamava de "metrópole em grade", foi renderizado em atlas antes de gastar
vaga e é fachada de tijolo rosa e sebe verde, sem piso de calçada e sem par de paleta
no nosso.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está versionado
é o kit já CONVERTIDO, em `dev_scripts/calcada_goldenrod_kit.json` (tile em ÍNDICE da
nossa paleta, já repintado e já composto sobre a nossa calçada), e o script que o
instala, `dev_scripts/calcada_goldenrod.py`. Projeto privado e não monetizado, que
distribui patch e nunca ROM.

### Cidade de pedra de `EcruteakCity` (`gTileset_EcruteakCity`, 27 vagas mortas entre 640 e 782)

Esta seção é auto-contida e cobre a onda 3 do REFINO, frente JOHTO, cidade de
Ecruteak.

Desta passada, só DUAS peças são importadas, e elas custam os 8 tiles 8x8 novos do
`gTileset_EcruteakCity`. Nenhuma cor nova entrou: o tileset tem ZERO vaga de paleta
(as seis vagas do secundário aparecem em metatile vivo, a menor união de um par em
uso é 23 cores e a vaga cabe 15, e das 96 entradas das seis vagas só UMA está morta),
então toda a arte que chega é reindexada para cor que já existe, sem aproximar
nenhuma. Nada além de ARTE foi importado: nenhum id de flag, var, script, música,
treinador ou espécie.

- Os **dois marcos de pedra** (o par de pilares de topo chanfrado que agora alinha a
  beira da rua, e a variante gasta dele) vieram dos metatiles 693 e 706 do secundário
  `0x2D4B3C`, com o primário `0x2D4A94`, do **Pokémon GS Chronicles** build 2.7.6
  (19/06/2024), de **Overlord Kaktus / G0LD**, sobre base **Pokémon FireRed (BPRE)**
  com motor fork do CFRU e split de VRAM estilo Emerald (512/512/6). É o par da
  Ecruteak redesenhada do hack, mapa de amostra do grupo 3, mapa 6 (68 por 46). Md5
  da cópia privada de trabalho: `d50d50b2ed8e462882aa5f30cb056a41`.
- A extração dos dois **não é por diferença** contra o chão liso da fonte, e sim por
  **máscara de COR**: naquele trecho o chão do hack é areia com borda de grama, e a
  diferença traria tufo verde junto com o pilar. Entram só os cinco tons do objeto,
  ((192,192,184), (144,144,136), (104,104,96), (56,64,72) e (40,48,56)), e todo o
  resto do quadrado é o NOSSO calçamento, pixel a pixel. Os cinco caem por
  luminância em cinco cores que a vaga 9 já tinha, com o RGB intacto:
  (192,192,192), (160,160,160), (96,104,120) e (64,72,104), esta última recebendo os
  dois tons mais escuros.
- O **atributo de metatile do GS Chronicles tem QUATRO bytes e o nosso tem DOIS**, ou
  seja a importação perde comportamento. Ele foi reescrito à mão: os dois marcos
  entram com `0x1000`, comportamento `MB_NORMAL` e `layerType` COVERED, que é o mesmo
  atributo do metatile 724 que eles substituem e o que a regra da onda exige de
  célula solidificada. Comportamento zerado é a escolha certa porque o pilar não é
  água, não é grama alta, não é porta e não dispara script: é cenário sólido, e quem
  o torna intransponível é a COLISÃO.
- **Todo o resto NÃO é importado.** Os onze arranjos novos de calçamento saem dos
  treze tiles de laje cinza que o próprio `gTileset_EcruteakCity` já tinha (os locais
  96 a 108), recombinados quadrante a quadrante, e custam zero tile e zero cor. As
  outras doze peças de mobiliário (canteiro de flores, urna dourada, pedestal de
  pedra, banco de pedra, bebedouro, quadro de avisos, placa de madeira e o arbusto de
  duas células, cada um na versão de rua e as quatro primeiras também na de lote) são
  a camada de CIMA de metatiles que este repositório já tinha desenhados e que os
  dois mapas do tileset não usavam (767, 749, 956, 960, 963, 943 e 942 do próprio
  secundário, e 26 e 27 do primário `gTileset_JohtoNorthWest`), remontada sobre o
  nosso calçamento.

O que ficou de fora, e por quê:

- A **família de laje retangular** da Ecruteak do GS Chronicles (metatiles 725, 607,
  566, 567, 574, 575, 582, 583, 591 e 599), que reindexa muito bem para os nossos
  cinzas: as linhas dela não são textura, são borda de plataforma, e espalhadas se
  cruzam em ângulo reto e viram um labirinto de riscos que não fecham. Peça de chão
  de fora só serve espalhada se for isotrópica, e essa não é.
- O **medalhão redondo** e as **lajes lavradas** do secundário de praça do mesmo hack
  (`0x2D4B54`, metatiles 512, 514, 520, 521 e 522). Sozinhos ficam bons; espalhados
  de um em um sobre o nosso calçamento leem como símbolo solto, e não como pedra
  lavrada. Acento geométrico só funciona em área contínua.
- A **lanterna suspensa** dos metatiles 750 e 751, que o repositório já tinha: ela é
  `layerType` NORMAL, e usá-la numa célula de rua que continua andável trocaria o
  `layerType` de uma célula andável, que é o que a regra 3 da onda proíbe.

O **GS Chronicles** não declara licença própria nos dois repositórios públicos do
autor; o README dele pede crédito à **Rom Hacking Hideout (RHH)** e ao
**pokemonHnS**, e é isso que esta seção faz, e repete a cláusula anti-monetização do
CFRU, que este projeto respeita. A arte de base é rip e edição de Pokémon
Gold/Silver e FireRed, ou seja da **Nintendo/Game Freak**: o crédito acima cobre a
edição feita pelo autor da ROM hack, não o material original.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está versionado
é o kit já CONVERTIDO, em `dev_scripts/pedra_ecruteak_kit.json` (máscara em índice da
nossa paleta, com -1 onde o pixel é nosso), e o script que o instala,
`dev_scripts/pedra_ecruteak.py`. Projeto privado e não monetizado, que distribui
patch e nunca ROM.

### Porto de `OlivineCity` (`gTileset_OlivineCity`, 20 vagas mortas entre 640 e 979)

Esta seção é auto-contida e cobre a onda 3 do REFINO, frente JOHTO, cidade de
Olivine, a do porto e do farol da Jasmine.

**Nada foi importado nesta passada, e isso é o resultado da medição, não
economia de esforço.** Antes de desenhar, o atlas de metatiles
(`dev_scripts/atlas_metatiles.py`) foi rodado nos dois lados do par de tilesets
de Olivine, e ele mostrou 478 metatiles do primário `gTileset_JohtoGeneral` e
127 do secundário `gTileset_OlivineCity` que a cidade NÃO usa. Dentro deles
estavam dois guarda-sóis inteiros, um painel de toldo amarelo, pernas, balizas,
bueiro e a trama espelhada, tudo já desenhado e nunca escrito em `map.bin`
nenhum. Com esse acervo em mãos, abrir uma ROM de terceiro seria gastar
orçamento de tile e de cor por arte que o cartucho já carrega. Por isso a pasta
`fontes-mapas/romhacks/` NÃO foi aberta nesta rodada, nenhum arquivo de ROM foi
lido, e não há md5 de cópia privada de trabalho a declarar: não houve cópia.

O orçamento, medido nesta árvore:

- **tiles 8x8 novos: ZERO.** O `tiles.png` do `gTileset_OlivineCity` continua com
  os mesmos 240 tiles de 384 e os mesmos 3.217 bytes, e não foi sequer aberto
  para escrita.
- **cores novas: ZERO.** Toda peça aponta para tile e para vaga de paleta que já
  estavam compilados (as vagas 0, 1, 7 e 8).
- **bytes de ROM: ZERO.** As 20 peças novas de metatile ocupam vaga MORTA do
  secundário, então `metatiles.bin` continua com 5.440 bytes e
  `metatile_attributes.bin` com 680. O `map.bin` de `OlivineCity` continua com
  7.488. A `pokeemerald.gba` tem os mesmos 33.554.432 bytes de antes.

De onde saiu cada peça, toda ela deste repositório:

- **Cais de pedra** (calçamento de tijolo da orla, andável): mesma arte do
  metatile 827 do `gTileset_OlivineCity`, quatro vezes o tile local 61 na vaga 8
  de paleta, escrita numa vaga nova com atributo `0x0000` em vez de `0x1000`
  porque a trama que ela substitui é `NORMAL` e a regra da onda exige
  `(comportamento, layerType)` idêntico em célula que continua andável. Com a
  camada de cima vazia, `COVERED` e `NORMAL` desenham o mesmo pixel.
- **Bueiro do cais**: o tile local 60 do mesmo secundário, aquele disco escuro
  que o tileset trazia e que nenhum dos dois mapas usava.
- **Guarda-sol amarelo e guarda-sol azul**: metatiles 876 a 880, 882 e 884 a 887
  do `gTileset_OlivineCity`, todos sem uso nos dois mapas do tileset. A copa
  alta (tiles locais 6 a 9 do amarelo e 23 a 26 do azul, na vaga 7 de paleta) e
  a copa baixa (locais 10 a 13 e 27 a 29) foram remontadas sobre a trama; o pé
  (metatiles 880 e 882, tiles locais 52 e 53) ficou como estava, porque ele já
  nasce sobre o tijolo e o cais novo é de tijolo.
- **Painel do porto**: os metatiles 864 a 866 e 872 a 874 (toldo amarelo em cima
  e laranja embaixo, três células de largura, tiles locais 40 a 51 na vaga 7),
  remontados sobre a trama, com as pernas 893 e 892 usadas como vêm, porque elas
  já nascem sobre o tijolo do cais.
- **Balizas de amarração**: metatile 944 do próprio secundário, que a cidade já
  usava, replicado em mais seis pontos.
- **Arbustos**: a camada de cima dos metatiles 26 e 27 do primário
  `gTileset_JohtoGeneral` (tiles 38, 39, 54 e 55 da vaga 0), o mesmo par que
  Ecruteak usou, remontada sobre a trama.
- **Avenida em espinha de peixe**: a própria trama do metatile 905, espelhada na
  horizontal (594H e 593H em cima, 610H e 609H embaixo). Não é rearranjo de
  quadrante: é o metatile inteiro virado, o que inverte a diagonal sem quebrar
  linha nenhuma. Essa orientação já existia no tileset, nos metatiles 660 a 663,
  668 e 669, todos vivos no mapa.

O que ficou de fora, e por quê:

- O **deque de tábuas** do primário (metatiles 354 a 372, atributo `0x0000`, ou
  seja andável), que daria um belo pátio de carga: as peças de BORDA dele têm a
  grama pintada dentro do tile, então encostadas no calçamento mostram franja
  verde. Só o miolo é limpo, e miolo sem borda encosta em ângulo reto, que é o
  defeito de retalho que esta onda já pagou uma vez.
- As **lajes de variante por rearranjo de quadrante**, que foram o truque de
  Ecruteak: a trama de Olivine é contínua e de período 16, e qualquer troca de
  quadrante rompe a diagonal no meio da célula.
- O **canteiro de grama** na esplanada: o anel de transição (metatiles 441, 443,
  444, 448, 450, 451, 452 e 457) é todo `COVERED`, e um canteiro decente pede um
  anel de 6 por 5 células. Caberia com oito cópias de atributo, mas comeria a
  esplanada inteira e deixaria o cais sem lugar.
- A **troca de metade das células de 905 pelo metatile 449 do primário**, que é
  byte a byte a mesma coisa e derrubaria a régua para 11% sem mudar um pixel.
  Isso é comprar nota com duplicata, e está recusado por escrito no cabeçalho de
  `dev_scripts/porto_olivine.py`; é também o motivo de a conferência daquele
  script medir o carimbo por FAMÍLIA VISUAL além de por id.

**Licença e autoria.** Como nada veio de fora, não há licença de terceiro a
declarar nesta seção. A arte de base é a do `pokeemerald` e a do demake de Johto
já creditados nas seções acima, ou seja **Nintendo / Game Freak / Creatures**
para o material original, e os créditos de conversão que este arquivo já
registra para Johto. Nenhuma ROM entra neste repositório: o que está versionado é
o script que monta as peças, `dev_scripts/porto_olivine.py`, e o plano que ele
grava, `dev_scripts/porto_olivine.json`. Projeto privado e não monetizado, que
distribui patch e nunca ROM.

### Praça de `HearthomeCity` (`gTileset_Hearthome`, metatiles 805 a 834)

Esta seção é auto-contida e cobre a onda 2 do REFINO, frente PRAÇA.

Os 11 tiles 8x8 novos do `gTileset_Hearthome` e as 14 cores novas da vaga de
paleta 6 são de DUAS origens, e a maior parte NÃO veio de fora. Nada além de
ARTE foi importado: nenhum id de flag, var, script, música, treinador ou espécie,
e o comportamento de todo metatile novo de móvel entra ZERADO, com `layerType`
COVERED.

DITO EM VOZ ALTA, PORQUE A PROVA DAS CIDADES ANTERIORES NÃO EXISTE AQUI: o
`gTileset_Hearthome` é secundário de UM layout só e de UM mapa só, o próprio
`HearthomeCity` (medido nesta árvore lendo `data/layouts/layouts.json` e todo
`data/maps/*/map.json`). Pastoria e Sunyshore puderam fechar com "zero pixel de
diferença no mapa irmão"; aqui não há mapa irmão, e fabricar uma prova vazia por
construção seria pior do que não ter prova. O que existe no lugar dela são duas
contas diretas, impressas por `python3 dev_scripts/praca_hearthome.py --medir`:
nenhuma cor foi escrita num índice de paleta que algum pixel VIVO deste tileset
use, e nenhum tile foi escrito numa vaga que alguma entrada de algum dos 512
metatiles do `metatiles.bin` peça.

- O **calçamento inteiro é NOSSO**, e isso é medida e não economia. As quatorze
  variantes de chão (três de junta espelhada do tijolo, três de junta espelhada
  da laje e oito de meio-fio de granito, que são as mesmas oito peças que
  desenham o medalhão do centro da praça) saem de três operações sobre o que o
  repositório já desenhava: ESPELHO dos tiles do tijolo 521 e da laje 545 (o
  bit de espelho custa zero tile e zero cor, e a mudança é real: 37,4 de
  distância RGB média no espelho horizontal do tijolo, 24,0 no da laje, contra o
  piso de 8,0 do `varia_carimbo.py`); MOSAICO, que é misturar quadrantes de duas
  famílias no mesmo metatile, de graça porque cada entrada carrega a própria vaga
  de paleta; e GRANITO, os quatro tiles da nossa laje escurecidos pelo fator
  0,62, que dá (117,117,117), (132,132,132) e (158,158,158). O granito é a única
  arte nova de chão: 4 tiles e 3 cores, todas derivadas das nossas.
- O **banco de praça** (metatiles 24 e 25 do hack) e as duas **grades** (9 e 21)
  vieram do par `0x286CF4` (primário de exterior) e `0x286DB4` (secundário de
  metrópole) do **Pokémon Light Platinum**, de **WesleyFG**, sobre base **Pokémon
  Ruby (AXVE)**. É o mesmo par que a frente METRÓPOLE usou em Jubilife, e as
  peças são as que Hearthome não tinha desenhadas. A cor foi medida ANTES de
  escolher: a cor mais distante do banco está a 15,8 da cor mais próxima que os
  nossos dois tilesets já têm, e a da grade a 24,0. É a mesma família
  cinza-azulada da catedral e dos prédios da cidade. Md5 da cópia privada de
  trabalho: `7fd2c08735459d99fa23fdaa9b755486`.
- O **arbusto redondo**, a **moita larga** e a **moita** NÃO são importados: são
  a camada de CIMA de metatiles que os nossos tilesets já desenham (o 539 do
  `gTileset_Hearthome` e o par 30 e 31 mais o 14 do `gTileset_GeneralSinnoh`),
  levantada para cima do calçamento novo. Custam zero tile e zero cor, e são os
  canteiros de arbusto do tema, com o verde que a cidade já usa.

O que ficou de fora, e por quê:

- O **calçamento de praça** do hack (metatiles 30, 31, 38, 46, 47, 54, 55, 62 e
  63 do `0x286DB4`), que é o único desenhado em sistema nas três folhas de
  contato triadas, por DISTÂNCIA DE COR: ele é cinza azulado ((136,152,184),
  (112,136,160), (104,128,152), (80,88,120), (168,192,216)) e o chão de
  Hearthome não é dessa família. A peça mais próxima dele fica a 78,0 da média
  do nosso tijolo 521, que é (213,180,106), e a 83,4 da média da nossa laje 545,
  que é (236,236,236), contra o critério duro de 50 desta onda. Em Jubilife o
  mesmo calçamento entrou porque LÁ a cidade já era cinza-azulada; aqui ele
  entraria como remendo.
- O **hidrante** (26, 27 e 28), por ser o móvel de cor mais estranha à cidade: a
  cor mais distante dele está a 43,8 do que os nossos tilesets já têm, contra
  15,8 do banco e 24,0 da grade. Hidrante também é mobiliário de RUA, e o tema
  desta passada é praça.
- O **canteiro de madeira** do hack (40 e 41), que seria o canteiro de flor do
  tema: ele é peça de UMA camada e traz o calçamento cinza-azulado do hack
  assado dentro do próprio tile, o mesmo calçamento que a conta de cor acabou de
  reprovar.
- O **vaso** (294) e as **copas** (68, 104 e 295): o vaso pinta com DUAS paletas
  do hack ao mesmo tempo (a 2 e a 10) e a copa com a 2, que sozinha pede 9
  cores; com o banco e a grade já na vaga 6, não sobrava vaga para uma terceira
  paleta do hack. Copa sem vaso é meia peça, que é a armadilha que a topiária de
  Jubilife já pagou.
- A **flor vermelha** do nosso próprio primário (metatile 4), que seria o
  canteiro de flor: a camada de cima dela cobre a célula INTEIRA, com a grama
  assada junto, então plantada no calçamento ela viraria um quadrado de grama
  com flor em cima.

O **Light Platinum** não declara licença própria. A arte de base é da
**Nintendo/Game Freak**; o crédito acima cobre a edição feita pelo autor da ROM
hack.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está
versionado é o kit já CONVERTIDO, em `dev_scripts/praca_hearthome_kit.json`
(paleta em RGB e tile em nibble, já reindexado para a vaga nova), e o script que
o instala, `dev_scripts/praca_hearthome.py`. Projeto privado e não monetizado,
que distribui patch e nunca ROM.

### Pedra talhada de `VeilstoneCity` (`gTileset_Veilstone`, metatiles 760 a 795)

Esta seção é auto-contida e cobre a onda 2 do REFINO, frente PEDRA.

Os 26 tiles 8x8 novos do `gTileset_Veilstone` e as cores novas das vagas de
paleta 6 e 8 vieram de UMA ROM hack, e nada além de ARTE foi importado: nenhum
id de flag, var, script, música, treinador ou espécie, e o comportamento de todo
metatile novo de móvel entra ZERADO, com `layerType` COVERED.

Um aviso que esta seção dá em voz alta, porque a alternativa seria fabricar uma
prova vazia: o `gTileset_Veilstone` é usado por UM mapa só, o próprio
`VeilstoneCity`. Por isso **não existe**, aqui, a prova de "zero pixel de
diferença em mapa irmão" que as seções de Pastoria, Sunyshore e Oreburgh puderam
dar. No lugar dela ficam o portão de planta (`dev_scripts/portao_planta.py`,
verde contra o commit de referência) e a lente de carimbo
(`dev_scripts/qa/lente_carimbo.py`), que compara os 33 mapas carimbados e acusou
mudança em `VeilstoneCity` e em nenhum outro.

- O **matação** de duas por duas células (e o espelho horizontal dele) e o
  **pedregulho** vieram do par de tilesets `0x286E44` (primário) e `0x2870FC`
  (secundário) do **Pokémon Light Platinum**, de **WesleyFG**, sobre base
  **Pokémon Ruby (AXVE)**. É o par do desfiladeiro de pedra do grupo 8 do hack
  (mapa de amostra g08m01, 48 por 43). Md5 da cópia privada de trabalho:
  `7fd2c08735459d99fa23fdaa9b755486`. A montagem do matação foi lida do MAPA do
  hack e não do atlas: naquele mapa o par vertical (77, 85) aparece 21 vezes, o
  (78, 86) outras 21 e o par horizontal (85, 86) aparece 27, e é assim que a
  peça foi remontada aqui, com a linha de cima ANDÁVEL (a arte mora na camada de
  cima e o jogador passa atrás) e a de baixo sólida.
- O **poste de rua** de duas células veio do par `0x286CF4` (primário) e
  `0x286EEC` (secundário) da MESMA ROM, a cidade de calçada do grupo 0 (mapa de
  amostra g00m14, 40 por 30). São seis cores, de (48,56,88) a (184,208,224), nos
  índices vagos da nossa vaga de paleta 8.
- A escolha da rocha do `0x2870FC` foi por COR MEDIDA e não por gosto: ela é
  cinza-azulada, (176,184,200), (152,160,176), (128,128,144), (104,112,120),
  (96,96,96) e (80,80,88), a mesma família fria do calçamento desta cidade, que
  é (216,224,224), (192,200,208) e (168,184,200). Do tom claro da rocha para o
  tom médio da nossa calçada são 24,0 de distância RGB. A pedreira que
  `OreburghCity` usou nesta mesma onda (o `0x286E8C`) foi descartada aqui pela
  mesma conta: a rocha dela é quente, (184,136,128)/(152,104,96)/(128,80,72), e
  dá 102 de distância contra este cinza.
- As **21 variantes de calçamento** NÃO são importadas, e a razão também é cor
  medida: o calçamento de pedra do `0x286EEC`, que casaria de desenho, tem
  (168,176,176), (136,152,152) e (88,96,104), e a distância entre as cores
  médias dos dois metatiles de piso é **85,6**, muito acima do piso de ~50 que a
  lição da areia de Pastoria e da terra de Sandgem deixou. Sem borda de
  transição desenhada, uma mancha dessas vira remendo escuro no meio da praça.
  No lugar dela, as 21 variantes são ARRANJO e ESPELHO de tiles que os nossos
  dois tilesets já tinham desenhados: o tecido diagonal do próprio carimbo (694,
  695, 710 e 711), a laje com junta (758, 759, 760, 761, 774 e 790) e o liso
  salpicado do segundo carimbo (262 e 278). Custam zero tile e zero cor.
- A **pedra do demake** (e o espelho dela) e a **moita florida** também NÃO são
  importadas: são a arte da camada de cima dos metatiles 404 e 4 do próprio
  `gTileset_GeneralSinnoh` deste repositório, que nenhum mapa desta cidade
  usava, remontadas sobre o nosso calçamento com comportamento zerado.

O que ficou de fora, e por quê:

- A **coluna** e a **bacia** de pedra do `0x2870FC` (metatiles locais 110 e
  113). Elas foram plantadas, renderizadas e OLHADAS antes do corte, não
  descartadas no papel. As duas pintam com a paleta 5 do primário do hack, que é
  cinza QUENTE: (200,192,176), (176,176,160), (168,152,136), (152,136,136),
  (128,120,120) e (88,88,88). Contra o cinza frio desta cidade a conta é dura
  ((168,152,136) para o nosso (168,184,200) dá 71,6), e no render a coluna saiu
  como uma barra bege listrada que lê como poste de MADEIRA numa praça de pedra,
  e a bacia como um banco marrom. Cortadas as duas, sobram nove índices livres
  na vaga de paleta 6 para quem vier depois.
- A **pedra miúda** do mesmo tileset (local 70), por cor: ela é a rocha quente
  daquele par, (200,152,104)/(184,136,104)/(160,120,88), e dá 114,8 de distância
  do nosso calçamento. Sete cores para plantar uma pedra marrom numa praça
  cinza.
- O **seixo** (local 93), porque na fonte ele tem colisão 0, ou seja é respingo
  de chão e não móvel; importá-lo como sólido poria uma pedrinha de oito pixels
  barrando o passo, que lê como bug e não como enfeite.
- A **escadaria** e o **degrau** de pedra (locais 137 e 138), porque degrau é
  promessa de mudança de nível e esta passada tem elevação INTACTA em 100% das
  palavras como regra dura; degrau desenhado sem elevação atrás dele é armadilha
  visual.
- A **laje lisa** (locais 104 e 112), porque como peça solta ela é um quadrado
  cinza sem silhueta: no meio da praça não lê como móvel, lê como buraco.
- O **bueiro** e a **grade** do `0x286EEC` (local 261), porque são arte de CHÃO
  com a cor do calçamento da fonte, e caem na mesma conta de 85,6.

O **Light Platinum** não declara licença própria; o tópico "WesleyFG Tile's" na
PokéCommunity libera os tiles **com crédito**, e é isso que esta seção faz. A
arte de base é rip de Diamond/Pearl/Platinum, ou seja da **Nintendo/Game
Freak**: o crédito acima cobre a edição feita pelo autor da ROM hack, não o
material original.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está
versionado é o kit já CONVERTIDO, em `dev_scripts/pedra_veilstone_kit.json`
(paleta em RGB e tile em nibble, já reindexado para a vaga nova), e o script que
o instala, `dev_scripts/pedra_veilstone.py`. Projeto privado e não monetizado,
que distribui patch e nunca ROM.

### Praia de `DewfordTown` (`gTileset_Dewford`, metatiles 891 a 921)

Esta seção é auto-contida e cobre a onda 4 do REFINO (Kanto e Hoenn), frente
DewfordTown.

Os 16 tiles 8x8 novos do `gTileset_Dewford` e as cores novas das vagas de paleta
6 e 7 vieram de UMA ROM hack, e nada além de ARTE foi importado: nenhum id de
flag, var, script, música, treinador ou espécie, e o comportamento de todo
metatile novo de móvel entra ZERADO, com `layerType` COVERED.

- O **vocabulário de pescador** (boia no suporte, boia deitada na areia, tambor
  de cais, balde do pescador, poste do cais e quadro de avisos) veio do par
  `0x286CF4` (primário de exterior) e `0x286D54` (secundário costeiro) do
  **Pokémon Light Platinum**, de **WesleyFG**, sobre base **Pokémon Ruby
  (AXVE)**. É o mesmo par que as frentes COSTA (Sandgem) e ORLA (Sunyshore)
  usaram, e a razão de voltar a ele está medida: no atlas dos 379 metatiles do
  `gTileset_Dewford` e nos 512 do `gTileset_General` não existe uma boia, um
  tambor, um balde nem um quadro de avisos, e Dewford é a vila de pescador do
  Brawly. Md5 da cópia privada de trabalho:
  `7fd2c08735459d99fa23fdaa9b755486`.
- As **dezesseis variantes de chão de areia** e a **moita redonda andável** NÃO
  são importadas: saem de tiles que os NOSSOS dois tilesets deste mapa já têm
  desenhados. O `gTileset_General` tem 35 tiles 8x8 pintados só com os quatro
  índices de areia da paleta 5, e as variantes são espelhos e misturas de
  quadrante de SEIS deles (`0x02` e `0x03`, a areia grossa manchada; `0x81`, o
  cascalho claro; `0xD5`, o sulco horizontal da maré; `0x1F0` e `0x1F2`, as duas
  faixas de transição), somados aos dois tiles do próprio carimbo 292 (`0x108`,
  a areia chapada, e `0x118`, a mesma com nove pixels de salpico); a moita
  redonda é a camada de cima do nosso metatile 514, levantada para cima da areia
  com o atributo do carimbo 569. Custam zero tile e zero cor.

O **Light Platinum** não declara licença própria; o tópico "WesleyFG Tile's" na
PokéCommunity libera os tiles **com crédito**, e é isso que esta seção faz. A
arte de base é da **Nintendo/Game Freak**; o crédito acima cobre a edição feita
pelo autor da ROM hack.

O que ficou de fora, e por quê:

- O **resort de praia do Scorched Silver** (secundário `0x492AD4`, o mapa
  g00m15, 60x50), que é a peça mais bonita da triagem inteira, com coqueiro,
  guarda-sol aberto em três cores e espreguiçadeira, e ainda por cima em base
  Emerald, ou seja com a MESMA paleta de areia que a nossa. O coqueiro dele é um
  bloco 2x2 e o topo tem atributo `0x0021`; o nosso carimbo é `0x1021`. Para a
  linha de cima continuar ANDÁVEL ela teria que herdar o `0x1021`, e aí a copa
  desenharia ABAIXO do boneco (`METATILE_LAYER_TYPE_COVERED` manda as duas
  camadas para BG3 e BG2), ou seja o jogador andaria NA FRENTE da folhagem. A
  saída seria solidificar as QUATRO células, e numa cidade de 212 células
  andáveis cada coqueiro custaria 4 do denominador da régua por cópia. O
  guarda-sol e a espreguiçadeira saíram junto, por tema: Dewford é a ilha do
  ginásio de luta e da Granite Cave, não uma estação balneária.
- O **cabo de amarração** do Light Platinum (local 375), que chegou a ser
  importado, plantado e renderizado: é ferragem de convés, e solto na areia lê
  como uma estrela azul no chão. Cortado depois do render, como o guarda-sol de
  Sandgem.
- O **calçadão bege** da fonte, sempre. A camada de baixo dos seis móveis é o
  piso do hack, achado por EVIDÊNCIA e não por constante (todo padrão de camada
  de baixo que aparece em 4 ou mais metatiles diferentes da fonte é piso dela), e
  cada móvel recebe o NOSSO chão de areia entrada por entrada.

Nenhuma ROM entra neste repositório, nem em parte nem em dump: o que está
versionado é o kit já CONVERTIDO, em `dev_scripts/praia_dewford_kit.json`
(paleta em RGB e tile em nibble, já reindexado para a vaga nova), e o script que
o instala, `dev_scripts/praia_dewford.py`. Projeto privado e não monetizado, que
distribui patch e nunca ROM.
