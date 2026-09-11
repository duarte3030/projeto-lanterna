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

### Mapas inteiros do Pokémon Liquid Crystal (áreas do Safari de Johto)

Este bloco não é kit de tile solto: são **mapas inteiros copiados**, com a planta e o par
de tilesets do autor, na composição que ele desenhou. Fonte: **Pokémon Liquid Crystal**,
de **Linkandzelda**, hack de base **Pokémon FireRed** (código `BPRE`). Md5 da cópia
privada de trabalho: `3e72e2d767ed9e689c48692f2f00de7a`. A ROM **não entra neste
repositório**, nem em parte nem em dump: o que está versionado é o asset já convertido
(PNG indexado, JASC-PAL, `metatiles.bin`, `metatile_attributes.bin`, `map.bin` e
`border.bin`) e a ferramenta que o converte, `dev_scripts/copia_mapa_rom.py`.

O que foi copiado, e só isto:

| nosso mapa | fonte no hack | tamanho |
|---|---|---|
| `LcSafariMountain` | `g5m113`, área de montanha da Safari Town | 58x50 |
| `LcSafariForest` | `g5m115`, área de floresta da Safari Town | 69x56 |
| `LcSafariWater` | `g5m116`, área de água da Safari Town | 70x50 |

Mais os dois tilesets que as três usam: `gTileset_LcOutdoor` (primário, 640 tiles, do
`0x2D4A94` do hack) e `gTileset_LcSafari` (secundário, 312 tiles, do `0x2D4B54`).

**Nada do JOGO do autor entra**: nenhum warp, NPC, gatilho, placa, item, treinador,
encontro, script, flag, var, música ou espécie do Liquid Crystal foi importado. O enredo
dele (o Team Nexus) fica de fora por decisão do Gui. Os eventos destes mapas são
escritos do zero neste repositório. As Ilhas Laranja, de onde a Safari Town vem no jogo
original, **não** foram importadas.

A arte de base é da Nintendo/Game Freak; o crédito acima cobre a edição feita pelo autor
do hack. Projeto privado e não monetizado.

### O TEMPLE OF ROCK, mapa inteiro copiado do Liquid Crystal

Em 11/09/2026 o mapa `g2m32` do **Pokémon Liquid Crystal** (Linkandzelda, com
Zeikku nos gráficos, Jambo51 no asm e Magnius na música; ROM privada de md5
`3e72e2d767ed9e689c48692f2f00de7a`, base FireRed) entrou em Johto como
`LcTempleOfRock`. O que veio do hack é **só a arte**: a planta (`map.bin`, 851
blocos, 23x37), a borda (`border.bin`) e os dois tilesets, o primário
`0x2D4BB4` como `gTileset_LcIndoor` e o secundário `0x2D5034` como
`gTileset_LcTemple`, copiados byte a byte por `dev_scripts/copia_mapa_rom.py`
(prova de render: 0 de 217.856 pixels diferentes).

**Nada do jogo do hack entrou**: warps, NPCs, treinadores, itens, placas e
encontros são nossos, escritos do zero. O enredo do Liquid Crystal (o Team
Nexus deles) ficou de fora inteiro, e as onze entidades de evento que o mapa
original tinha foram descartadas.

A ROM do hack não está neste repositório e nunca vai estar; só o asset
convertido.

### A UNDERSEA CAVERN, nove mapas inteiros copiados do Liquid Crystal

Em 11/09/2026 entrou em Johto a área inteira do mapsec 178 do **Pokémon Liquid
Crystal** (**LinkandZelda**, com **Zeikku** nos gráficos, **Jambo51** no asm e
**Magnius** na música), hack de base **Pokémon FireRed** (código `BPRE`). Md5 da
cópia privada de trabalho: `3e72e2d767ed9e689c48692f2f00de7a`. A ROM **não entra
neste repositório**, nem em parte nem em dump: o que está versionado é o asset já
convertido, copiado byte a byte por `dev_scripts/copia_mapa_rom.py`.

São nove mapas, 24.012 blocos, 48.024 B de blockdata:

| nosso mapa | fonte no hack | tamanho | par de tilesets |
|---|---|---|---|
| `LcUnderseaEntrance` | `g4m114` | 24x36 | `LcOutdoor` + `LcCaveSand` |
| `LcUnderseaCavern` | `g4m47` | 55x40 | `LcOutdoor` + `LcCaveRed` |
| `LcUnderseaSprings` | `g4m50` | 52x46 | `LcOutdoor` + `LcCaveRed` |
| `LcUnderseaGallery` | `g4m49` | 49x60 | `LcOutdoor` + `LcCaveRed` |
| `LcUnderseaDepths` | `g4m48` | 49x140 | `LcOutdoor` + `LcCaveRed` |
| `LcUnderseaChasm` | `g4m51` | 110x46 | `LcOutdoor` + `LcCaveRed` |
| `LcUnderseaGlacier` | `g4m103` | 48x34 | `LcOutdoor` + `LcCaveIce` |
| `LcUnderseaShrine` | `g4m5` | 48x30 | `LcIndoor` + `LcCaveSand` |
| `LcUnderseaAlcove` | `g4m116` | 24x26 | `LcOutdoor` + `LcCaveRed` |

Os dois primários já estavam aqui, do Safari e do Temple of Rock, e foram
REUSADOS: `gTileset_LcOutdoor` (do `0x2D4A94` do hack) e `gTileset_LcIndoor` (do
`0x2D4BB4`). Entraram três secundários novos, com nome genérico de propósito,
porque a arte deles serve a qualquer caverna do hack e não só a esta área:

- `gTileset_LcCaveRed`, do `0x2D4FEC`: rocha rosada com coral vermelho, chão de
  musgo, poça e escada de madeira. O mesmo secundário é a câmara grande do
  Cinnabar Volcano do hack (`g5m45`).
- `gTileset_LcCaveSand`, do `0x2D4BFC`: caverna de chão de areia ocre com
  pedregulhos. O mesmo secundário é a Hollow Cave inteira do hack (`g2m102` a
  `g2m104`) e a antessala do Cinnabar Volcano (`g5m44`).
- `gTileset_LcCaveIce`, do `0x2D4E24`: câmaras de gelo de parede azul-clara.

Prova de fidelidade: `copia_mapa_rom.py --prova-render` deu **0 de 6.147.072
pixels diferentes** somando os nove mapas.

**Nada do JOGO do autor entrou**: os 71 warps, os 52 objetos de evento, os
scripts, os itens, os treinadores e os encontros do hack foram todos descartados,
e os 58 warps, 35 objetos, 9 placas, 13 treinadores e 9 tabelas de encontro que a
área tem hoje foram escritos do zero aqui. O enredo do Liquid Crystal (o Team
Nexus deles) fica inteiro de fora, e a entrada, que no hack é um warp em Cianwood
City, aqui é mergulho de verdade pela água funda da Route 41.

A arte de base é da Nintendo/Game Freak; o crédito acima cobre a edição feita
pelo autor do hack. Projeto privado e não monetizado.

### A OUTSKIRT ISLAND, mapa inteiro copiado do Liquid Crystal

Em 11/09/2026 o mapa `g3m50` do **Pokémon Liquid Crystal** (Linkandzelda, com
Zeikku nos gráficos, Jambo51 no asm e Magnius na música; ROM privada de md5
`3e72e2d767ed9e689c48692f2f00de7a`, base FireRed) entrou em Kanto como
`LcOutskirtIsland`. O que veio do hack é **só a arte**: a planta (`map.bin`,
7.200 blocos, 60x120, 14.400 bytes), a borda (`border.bin`) e o tileset
secundário `0x2D507C`, importado como `gTileset_LcOutskirt` (384 tiles de 8x8,
384 metatiles, 16 paletas, 84 KB em disco). O primário `0x2D4A94` NÃO foi
reimportado: ele já estava aqui como `gTileset_LcOutdoor`, das três áreas do
Safari, e é reusado. Tudo copiado
byte a byte por `dev_scripts/copia_mapa_rom.py` (prova de render: 0 de 1.843.200
pixels diferentes).

**Nada do jogo do hack entrou**: os cinco objetos de evento que o mapa original
tinha foram descartados, e warps, NPCs, treinadores, itens, placas e encontros
são nossos, escritos do zero. O enredo do Liquid Crystal (o Team Nexus deles)
ficou de fora inteiro. A ilha do hack não tem warp nenhum; a ligação com Kanto
(o barco do marinheiro de Pallet Town) é invenção nossa.

A ROM do hack não está neste repositório e nunca vai estar; só o asset
convertido.

### A NEW ISLAND, cinco mapas inteiros copiados do Liquid Crystal

Em 11/09/2026 os mapas `g3m70`, `g4m30`, `g4m31`, `g4m33` e `g4m34` do
**Pokémon Liquid Crystal** (Linkandzelda, com Zeikku nos gráficos, Jambo51 no
asm e Magnius na música; ROM privada de md5
`3e72e2d767ed9e689c48692f2f00de7a`, base FireRed) entraram em Kanto como
`LcNewIsland` (exterior 65x35), `LcNewIslandEntrance` (12x10),
`LcNewIslandHall` (65x22), `LcNewIslandLab` (24x26) e `LcNewIslandCourtyard`
(24x46). O que veio do hack é **só a arte**: as cinco plantas (11.106 bytes de
`map.bin` somados), as bordas e dois tilesets secundários, o `0x2D5064` como
`gTileset_LcNewIslandOut` e o `0x2D501C` como `gTileset_LcNewIslandIn` (384
tiles de 8x8, 384 metatiles e 16 paletas cada). Os primários `0x2D4A94` e
`0x2D4BB4` NÃO foram reimportados: já estavam aqui como `gTileset_LcOutdoor` e
`gTileset_LcIndoor`. Tudo copiado byte a byte por
`dev_scripts/copia_mapa_rom.py` (prova de render: 0 de 1.421.568 pixels
diferentes nos cinco mapas).

**Nada do jogo do hack entrou**: os sete objetos de evento e os 33 warps que os
cinco mapas tinham foram descartados, e warps, NPCs, treinadores, itens,
placas, encontros e o MEW estático do pátio são nossos, escritos do zero. O
enredo do Liquid Crystal (o Team Nexus deles) ficou de fora inteiro. As
COORDENADAS das portas seguem os metatiles de porta, escada e seta que o autor
desenhou na planta, porque são arte; o destino de cada uma é decisão nossa.

A ROM do hack não está neste repositório e nunca vai estar; só o asset
convertido.

### A SILVER CAVE, cinco mapas inteiros copiados do Liquid Crystal

Em 11/09/2026 os mapas `g3m75`, `g4m95`, `g4m98`, `g4m96` e `g4m97` do
**Pokémon Liquid Crystal** (Linkandzelda, com Zeikku nos gráficos, Jambo51 no
asm e Magnius na música; ROM privada de md5
`3e72e2d767ed9e689c48692f2f00de7a`, base FireRed) entraram em Johto como
`LcSilverCaveOutside` (o vale, 44x48), `LcSilverCavePokemonCenter` (16x10),
`LcSilverCaveEntrance` (primeiro nível, 45x58), `LcSilverCaveMain` (segundo
nível, 50x58) e `LcSilverCaveDepths` (terceiro nível, 60x50). O que veio do
hack é **só a arte**: as cinco plantas (21.564 bytes de `map.bin` somados,
10.782 blocos), as bordas e dois tilesets secundários, o `0x2D4BE4` como
`gTileset_LcSilverIndoor` (384 tiles de 8x8, 384 metatiles, 16 paletas) e o
`0x2D4DF4` como `gTileset_LcSilverCave` (336 tiles de 8x8, 384 metatiles, 16
paletas), 84 KB em disco cada. Os primários `0x2D4A94` e `0x2D4BB4` NÃO foram
reimportados: já estavam aqui como `gTileset_LcOutdoor` e `gTileset_LcIndoor`.
O secundário `0x2D4AC4`, do vale, também NÃO entrou: a planta dele e a borda
dele não citam UM metatile do secundário (maior id 632 e borda 113, os dois
abaixo do corte de 640 do `frlg`), então o mapa declara um secundário que já
existe e a fidelidade continua exata. Tudo copiado byte a byte por
`dev_scripts/copia_mapa_rom.py` (prova de render: **0 de 2.760.192 pixels
diferentes** nos cinco mapas).

**Nada do jogo do hack entrou**: os 22 objetos de evento e os 15 warps que os
cinco mapas tinham foram descartados, e warps, NPCs, treinadores, itens,
placas e encontros são nossos, escritos do zero. O enredo do Liquid Crystal (o
Team Nexus deles) ficou de fora inteiro, e o Mt. Silver que este cartucho já
tinha ficou intacto: a Silver Cave é uma área A MAIS, ao lado dele. As
COORDENADAS das portas seguem os metatiles de porta, escada e seta que o autor
desenhou na planta, porque são arte; o destino de cada uma é decisão nossa, e
a ligação com o nosso mundo (o guia do Mt. Silver) é invenção nossa.

A ROM do hack não está neste repositório e nunca vai estar; só o asset
convertido.

### A ROUTE 100, dois mapas inteiros copiados do Liquid Crystal

Em 11/09/2026 os mapas `g3m94` e `g3m40` do **Pokémon Liquid Crystal**
(Linkandzelda, com Zeikku nos gráficos, Jambo51 no asm e Magnius na música; ROM
privada de md5 `3e72e2d767ed9e689c48692f2f00de7a`, base FireRed) entraram em
Johto como `LcRoute100Coast` (a orla de penhasco e mata, 104x34) e
`LcRoute100Open` (o mar aberto de recife com a ilha da estação, 132x54). O que
veio do hack é **só a arte**: as duas plantas (21.328 bytes de `map.bin`
somados, 10.664 blocos), as bordas e dois tilesets secundários, o `0x2D4AAC`
como `gTileset_LcSeaCliff` (384 tiles de 8x8, 384 metatiles, 16 paletas) e o
`0x2D4B6C` como `gTileset_LcOpenOcean` (128 tiles de 8x8, 384 metatiles, 16
paletas), 80 KB em disco cada. O primário `0x2D4A94` NÃO foi reimportado: já
estava aqui como `gTileset_LcOutdoor`. Tudo copiado byte a byte por
`dev_scripts/copia_mapa_rom.py` (prova de render: **0 de 2.729.984 pixels
diferentes** nos dois mapas).

**Nada do jogo do hack entrou**: os seis objetos de evento e os sete warps que
os dois mapas tinham foram descartados, e NPCs, treinadores, itens, placas e
encontros são nossos, escritos do zero. O enredo do Liquid Crystal (o Team
Nexus deles) ficou de fora inteiro. A **UNDERSEA EXPRESS**, a empresa de trem
submarino que no hack leva às Ilhas Laranja, ficou FECHADA: os onze interiores
dela (mapsec 136) não vieram, os três warps da ilha da estação não entraram e
cada um ganhou placa em inglês dizendo que a linha está fora de serviço, no
molde das portas fechadas de Johto. Nenhum prédio novo foi desenhado e nenhum
trem existe. A conexão entre os dois mapas é a mesma do hack (`right`/`left`,
offset 0); a ligação com o nosso mundo (o barco do marinheiro da Route 27) é
invenção nossa.

A ROM do hack não está neste repositório e nunca vai estar; só o asset
convertido.

### O CINNABAR VOLCANO, dois mapas inteiros copiados do Liquid Crystal

Em 11/09/2026 os mapas `g5m45` e `g5m44` do **Pokémon Liquid Crystal**
(Linkandzelda, com Zeikku nos gráficos, Jambo51 no asm e Magnius na música; ROM
privada de md5 `3e72e2d767ed9e689c48692f2f00de7a`, base FireRed) entraram em
Kanto como `LcCinnabarVolcano` (a cratera, 68x48, 3.264 blocos, 6.528 bytes de
`map.bin`) e `LcCinnabarVolcanoVent` (a câmara de cinzas, 24x36, 864 blocos,
1.728 bytes). O que veio do hack é **só a arte**: as duas plantas, as duas
bordas e nada mais. **Nenhum tileset novo entrou**: os quatro de que estes
mapas dependem já estavam aqui, o primário `0x2D4A94` como `gTileset_LcOutdoor`
e os secundários `0x2D4FEC` e `0x2D4BFC` como `gTileset_LcCaveRed` e
`gTileset_LcCaveSand`, todos das áreas que entraram mais cedo nesta mesma onda.
Tudo copiado byte a byte por `dev_scripts/copia_mapa_rom.py` (prova de render:
0 de 835.584 pixels na cratera e 0 de 221.184 pixels na câmara, 0,0000% nos
dois).

**Nada do jogo do hack entrou**: os dezesseis objetos de evento e os dezoito
warps que os dois mapas tinham foram descartados, e warps, NPCs, treinadores,
itens, placas e encontros são nossos, escritos do zero. O enredo do Liquid
Crystal (o Team Nexus deles) ficou de fora inteiro, e também ficou de fora o
ponto de mergulho que o hack tinha na poça da cratera. As COORDENADAS das
portas seguem os metatiles de porta e de seta que o autor desenhou na planta,
porque são arte; o destino de cada uma é decisão nossa, e a ligação com Kanto
(os dois guias de Cinnabar Island) é invenção nossa.

A ROM do hack não está neste repositório e nunca vai estar; só o asset
convertido.

### A HOLLOW CAVE, três mapas inteiros copiados do Liquid Crystal

Em 11/09/2026 os mapas `g2m102`, `g2m103` e `g2m104` do **Pokémon Liquid
Crystal** (Linkandzelda, com Zeikku nos gráficos, Jambo51 no asm e Magnius na
música; ROM privada de md5 `3e72e2d767ed9e689c48692f2f00de7a`, base FireRed)
entraram em Johto como `LcHollowCave` (1º andar, 40x50, 2.000 blocos, 4.000
bytes de `map.bin`), `LcHollowCaveInner` (2º andar, 40x50, 4.000 bytes) e
`LcHollowCaveChamber` (a câmara do fundo, 20x18, 720 bytes). O que veio do hack
é **só a arte**: as três plantas e as três bordas. **Nenhum tileset novo
entrou**: o primário `0x2D4A94` e o secundário `0x2D4BFC` já estavam aqui como
`gTileset_LcOutdoor` e `gTileset_LcCaveSand`. Tudo copiado byte a byte por
`dev_scripts/copia_mapa_rom.py` (prova de render: 0 de 512.000, 0 de 512.000 e
0 de 92.160 pixels diferentes, 0,0000% nos três).

**Nada do jogo do hack entrou**: os sete objetos de evento e os 21 warps que os
três mapas tinham foram descartados, e warps, NPCs, treinadores, itens, placas
e encontros são nossos, escritos do zero. O enredo do Liquid Crystal (o Team
Nexus deles) ficou de fora inteiro. As COORDENADAS dos degraus e das setas
seguem os metatiles que o autor desenhou na planta, porque são arte; o destino
de cada um é decisão nossa, e as duas bocas na encosta da Route 45, que ligam a
caverna ao nosso mundo, foram abertas por nós, no nosso mapa, com um metatile
que a própria rota já usava.

A ROM do hack não está neste repositório e nunca vai estar; só o asset
convertido.

### Sinnoh: as cidades copiadas do Pokémon Retro Platinum (11/09/2026)

As cidades abaixo foram copiadas INTEIRAS, arte por arte, do **Pokémon Retro
Platinum**, de **blloop**, um projeto decomp público em
`github.com/sinnoh-remakes/pokeemerald-platinum`, clonado no commit
`caece4fb104cf6285607465696df54294e47a7f6` do `master`. O hack não declara
licença; o Gui resolveu direto com o autor, que é amigo dele, e a permissão está
dada (resposta 73, de 11/09/2026).

O que veio de lá, por cidade:

- **TwinleafTown**: o `map.bin` e o `border.bin` do `TwinleafTown_Layout` dele
  (planta 22x34), a arte do secundário novo `gTileset_TwinleafRetroSec` (273
  tiles, 122 metatiles, 7 paletas), e o comportamento de metatile que veio junto.
  A cidade continua no nosso primário `gTileset_GeneralSinnoh`, então a faixa de
  8 tiles da borda conectada com a Route 201 é arte NOSSA, de propósito.
- **FloaromaTown**: o `map.bin` e o `border.bin` dele recortados em `0,0,34,38`
  (planta 34x38), o par próprio `gTileset_FloaromaRetroPrim` +
  `gTileset_FloaromaRetroSec` (481 tiles, 238 metatiles, 13 paletas), e **a
  animação de flor do tileset dele** (`data/tilesets/primary/outdoor_floaroma/
  anim/flowers`, 4 quadros), que virou `InitTilesetAnim_FloaromaRetro` e anima
  512 células do mapa.
- **SandgemTown**: o `map.bin` e o `border.bin` do `SandgemTown_Layout` dele
  (planta 34x34, sem recorte), o par próprio `gTileset_SandgemRetroPrim` +
  `gTileset_SandgemRetroSec` (584 tiles, 236 metatiles, 13 paletas) e o
  comportamento de metatile que veio junto. O desenho fica a 100,00% do dele: o
  render da cópia e o render da fonte são o mesmo arquivo. O tileset dele não
  anima nada nesta cidade (os dois `.callback` são `NULL` na fonte), então não
  veio animação.
- **OreburghCity**: os DOIS mapas dele, `OreburghCityNorth_Layout` (72x32) e
  `OreburghCitySouth_Layout` (58x44), fundidos num só `map.bin` de 72x76, com o
  `border.bin`, o par próprio `gTileset_OreburghRetroPrim` +
  `gTileset_OreburghRetroSec` (1.023 tiles, 427 metatiles, 13 paletas) e o
  comportamento de metatile que veio junto. A cidade inteira dele entrou, sem
  corte de desenho; a animação de carvão do `gTileset_OreburghSouth` NÃO veio, e
  as esteiras do pátio ficam paradas.
- **JubilifeCity**: o `map.bin` e o `border.bin` do `JubilifeCity_Layout` dele
  (planta 74x66, sem recorte), o par próprio `gTileset_JubilifeRetroPrim` +
  `gTileset_JubilifeRetroSec` (584 tiles, 329 metatiles, 13 paletas) e o
  comportamento de metatile que veio junto. O desenho fica a 99,63% do dele, e
  as 36 células que diferem são NOSSAS de propósito: 20 do prédio encaixado (o
  portão da Route 218, montado com metatiles do próprio autor), 2 das portas
  abertas na fachada do Global Terminal dele e 14 de quantização de cor.

Nada do JOGO dele entrou: warp, NPC, gatilho, placa, script, conexão, encontro e
treinador são todos nossos, nos mesmos ids de antes. A arte de base é da
Nintendo/Game Freak; o crédito acima cobre a edição feita pelo autor do hack.
Nenhuma ROM nem patch entra neste repositório: o que está versionado é o asset já
convertido. Projeto privado e não monetizado.

### Kanto inteira: `Ikarus' Tileset Patch FR (V3.2)`

Em 10/09/2026, por decisão do Gui, **Kanto inteira** (cidades, rotas, cavernas e as
ilhas Sevii) trocou a arte vanilla da FireRed pela arte de gen 4 do **Ikarus' Tileset
Patch FR (V3.2)**. É uma troca de região inteira, na forma da seção 3 do
`METODO-COPIA-CIDADES.md`: o primário `gTileset_General_Frlg` e 24 secundários saem
juntos, e com eles vêm os 109 `map.bin` e `border.bin` que o autor redesenhou dentro da
planta oficial, que não muda de tamanho em mapa nenhum.

O download oficial do autor traz um `#README.txt` com a licença em uma linha, *"If you
use this patch, please give credit"*, e a lista de quem creditar. Ela vai inteira:

- **Ikarus** (base: Ikarus Lost Property v2.4)
- **LibertyTwins** (correções da v3.2)
- Gráficos: **Alucus**, **ChaoticCherryCake**, **Cilerba**, **TheEnglishKiwi**,
  **Falsefate**, **Gallanty**, **Gigatom**, **Jesse [TB pro]**, **Klnothincomin**,
  **Kyledove**, **Lightbulb15**, **Magicscarf**, **Midnitez-REMIX**, **Newtiteuf**,
  **NickC**, **Prince Legendario**, **Rayquazadot**, **Scarex3wer**, **Spaceemotion**,
  **Speeddialga**, **Sylver1984**, **Thunderdove**, **William GF**, **WesleyFG**,
  **Zetavares852**, **674521**, **Heavy-Metal-Lover**

Versão: **V3.2 (Fixed Version)**. Patch IPS do autor, md5 do zip baixado
`bd991a02a1403ebf97d0da2e399aa842`; a cópia privada patchada, gerada aqui sobre a
FireRed 1.0 compilada do `pret/pokefirered` (sha1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`),
tem md5 `958ecefa1bb999e3f95d0890f380fffe`. Nem o patch nem a ROM entram neste
repositório: só o asset convertido, como manda a seção 6 do `METODO-COPIA-CIDADES.md`.

O que entrou: `tiles.png`, paletas, `metatiles.bin` e `metatile_attributes.bin` de
`general_frlg`, `pallet_town_frlg`, `viridian_city_frlg`, `pewter_city_frlg`,
`cerulean_city_frlg`, `lavender_town_frlg`, `vermilion_city_frlg`, `celadon_city_frlg`,
`fuchsia_city_frlg`, `cinnabar_island_frlg`, `indigo_plateau_frlg`, `saffron_city_frlg`,
`cave_frlg`, `viridian_forest_frlg`, `seafoam_islands_frlg`, `cerulean_cave_frlg`,
`mt_ember_frlg`, `berry_forest_frlg`, `navel_rock_frlg`, `sevii_islands_123_frlg`,
`sevii_islands_45_frlg`, `sevii_islands_67_frlg`, `ss_anne_frlg`, `island_harbor_frlg` e
`rock_tunnel_frlg`, mais o desenho de 109 layouts. **Nenhum script, texto, evento,
treinador, flag, var ou música do Ikarus entrou.**

### Hoenn inteira repintada: `Pokémon Blazing Emerald v1.6`, de Struedel (11/09/2026)

Decisão do Gui em 11/09/2026 (resposta 71): "copia Blazing Emerald" inteiro em Hoenn. O
que entrou foi **só arte de tileset**. Nenhum `map.bin`, warp, NPC, gatilho, placa,
script, conexão, encontro, treinador, flag, var ou música do hack foi importado: a planta
e o jogo continuam nossos, célula a célula.

- **Hack**: Pokémon Blazing Emerald v1.6, de **Struedel**, base Emerald binário (BPEE),
  32 MB, md5 da cópia privada de trabalho `5f9943a48a55ec85c2d1c8f05dca2aeb`. Sem licença
  formal declarada; o crédito ao autor é obrigatório em qualquer asset derivado.
- **Primário `gTileset_General`** (offset `0x3DF704` na ROM deles): `tiles.png` (512
  tiles), as paletas 00 a 05 e o `metatiles.bin` (80 dos 512 metatiles mudaram). Esse
  primário é compartilhado por **243 mapas** nossos, então a repintura alcança as
  dezesseis cidades, as rotas, as cavernas e, fora de Hoenn, `ValorLakefront`, os doze
  mapas do Time Galáctico e os três andares do esconderijo de Mahogany.
- **Doze secundários de cidade** (offsets `0x3DF71C` a `0x3DF83C`): `tiles.png`, as
  paletas 06 a 12 e o `metatiles.bin` de `petalburg`, `rustboro`, `dewford`, `slateport`,
  `mauville`, `lavaridge`, `fortree`, `lilycove`, `mossdeep`, `ever_grande`, `pacifidlog`
  e `sootopolis`. **O secundário de `fallarbor` NÃO entrou**: ele é dividido com quatro
  rotas, e a cidade recebeu a planta do Run & Bun por cima do NOSSO tileset (seção
  abaixo).
- **O que NÃO veio do hack**: o `metatile_attributes.bin` de todos eles continua o nosso
  (comportamento e layerType nossos, célula a célula); cinco metatiles do hack foram
  recusados por apontarem para índice de tile fora do tileset deles (petalburg 74 e 75,
  slateport 253 e 367, mauville 0); e, em `dewford`, **50 metatiles continuam os nossos**,
  porque o autor do hack reordenou a tabela e copiá-los inteiros quebrava o significado
  dos metatiles de `BirthIsland_Exterior` e `NavelRock_Exterior`, que dividem o mesmo
  tileset. Os 26 quadros de animação do `general` (água, beirada de areia, beirada de
  terra, cachoeira e flor) são **byte a byte iguais** aos da ROM deles, então nenhum
  precisou ser copiado: a água nova do Blazing é paleta, não tile.

A ROM do hack não entra neste repositório, nem em parte nem em dump: ela mora fora dele,
em `fontes-mapas/romhacks/blazing-emerald/`. A arte de base é da **Nintendo/Game Freak**;
o crédito acima cobre a edição feita pelo autor do hack. Projeto privado e não
monetizado, que distribui patch e nunca ROM.

### Fallarbor Town, Hoenn: a PLANTA veio do Pokémon Run & Bun (11/09/2026)

O `data/layouts/FallarborTown/map.bin` da cidade é o do **Pokémon Run & Bun v1.07**
(março de 2023), de **dekzeh**, construído sobre o decomp **pokeemerald** de Emerald.
Cópia direta 20x20 do mapa `g0m13` (blockdata `0x4B6080`), 34 das 400 células
diferentes da nossa planta anterior. O hack não declara licença e não tem fonte
pública; a arte de base continua sendo da Nintendo e da Game Freak, e o crédito acima
cobre a EDIÇÃO de planta feita pelo autor.

Nada além da planta entrou: nenhum tile, metatile, paleta, script, NPC, warp, flag,
var, música, treinador ou espécie. O tileset secundário de Fallarbor continua sendo o
nosso, e os warps, os objetos e os scripts da cidade são os de sempre, na mesma ordem
e com os mesmos índices. A ROM não entra neste repositório, nem em parte nem em dump.
Md5 da cópia privada de trabalho: `52e902cf2c124ef90c6b610e959b7035`.
