# O que fica de fora do porte, e por quê

Decisão do Gui em **21/08/2026**. A **régua** é `CORTES_DO_GUI` em
`dev_scripts/completude.py` (`--detalhe <região>` diz o que cada grupo tirou) e
a **cobrança** é o status `cortada` de `dev_scripts/fila_b6.json`. Se este texto
e a tabela discordarem, a **tabela** está certa: é ela que é medida.

| região | mapas | objetos | warps | placas |
|---|---|---|---|---|
| Sinnoh antes | 90,8% | 76,2% | 97,7% | 81,3% |
| Sinnoh depois | **95,4%** | **81,9%** | **100,7%** | **86,3%** |
| Unova antes | 97,3% | 99,5% | 99,3% | 98,0% |
| Unova depois | **99,0%** | 99,5% | **100,0%** | **99,6%** |

Fila do B6: **193 pendentes antes, 165 depois**, 28 viradas `cortada`. Kanto,
Johto, Hoenn e Galar não têm corte nenhum. **Sinnoh em `warps` passou de 100 e é
medido:** o corte tirou do denominador os mapas com déficit de warp, e o saldo
dos que ficam é +7, quase todo do `GalacticHQ_B1F`, 25 warps contra 2 da fonte.

## Fora do escopo

Sinnoh: **Battle Zone inteira** (Fight, Survival e Resort Area, rotas 225 a 230,
Stark Mountain, Villa, Battle Frontier de gen 4 e as cinco instalações, Battle
Tower, Ribbon Syndicate 2F e os 4 `UNUSED_*` que moram dentro dela, Battle Park
e mart do Resort: 48 mapas nossos e 11 da fonte, ilha que só abre
depois da Liga, e a ROM já tem o Frontier de Hoenn); **Pokémon Mansion e Trophy
Garden**; **Turnback Cave, Sendoff Spring e Spring Path** (23 mapas, labirinto
por RNG de pós-jogo); **Great Marsh**, os 5 da fonte mais o `GreatMarsh6`
(Safari de gen 4; o de Hoenn fica); **Amity Square** e os dois portões
(`OW_FOLLOWERS_ENABLED` é `FALSE`); **Pal Park, Underground, GTS e Pokétch
Company** (mecânica de DS, decisões 3 e 6 do plano de Sinnoh); **2º andar dos
Pokécenters** (11), **Union Room, Wi-Fi, Record Mixing** e **elevadores da
Liga**; **mapas de Mystery Gift** (Fullmoon, Newmoon, Flower Paradise, Hall of
Origin, Seabreak Path); **palco de Contest** e **Game Corner de Veilstone**.

Unova: **Battle Tower do BW3G** (5 da fonte), **Cable Club** (Trade Center, Time Capsule, Colosseum), **caça-níquel de Castelia** (5) e o **2F do Pokécenter**.

## O que FICA, dito porque quase saiu

- **Distortion World**, com gravidade normal. Ele caía no balde de "sobra de
  tabela" da régua (9 dos 10 andares apontam para `events_empty` no Platinum) e
  virou exceção nomeada. **Medido: nenhum mapa dele existe no repo.**
- **Os 8 ginásios de Sinnoh** (arte é de outro executor), o **Bug Contest** de
  Johto, **3 dos 7 `UNUSED_*` com conteúdo** (os outros 4 saíram com a Battle
  Zone), o **Snowpoint Temple** e o **trem-bala de Unova**.
- **O `Restaurant`**: o inventário o juntou ao Game Corner como "fachada", e
  medido ele é o Seven Stars do **Valor Lakefront**, com 9 duplas de treinador
  (os dois warps dele vão para lá). O Gui cortou só o Game Corner.
- **Dos 12 moldes de portão, 8 saíram** nos grupos acima; o item da fila cobra
  só `IronIsland`, `MtCoronetOutsideNorth/South` e `Route204North`.

## Lendários: o lar foi cortado, o Pokémon não

**Medido em 21/08/2026, e derruba a premissa de "realocar": NENHUM lendário de
Sinnoh está colocado hoje**, zero em `src/data/wild_encounters.json` e zero
batalha estática em `data/maps/*/scripts.inc`. Há o que **colocar**, não mover, e
quem coloca é OUTRO EXECUTOR; a tabela diz onde não pode ser:

| Pokémon | lar na fonte | situação |
|---|---|---|
| Giratina | Turnback Cave (cortado) | vai para o Distortion World, que fica; falta importar os mapas |
| Heatran | Stark Mountain (cortado) | sem lar, escolher um |
| Cresselia | Fullmoon Island (cortado) | sem lar, escolher um |
| Darkrai | Newmoon Island (cortado) | sem lar, escolher um |
| Shaymin | Flower Paradise (cortado) | sem lar; era Mystery Gift na fonte |
| Arceus | Hall of Origin (cortado) | sem lar; era Mystery Gift na fonte |
| Regigigas | Snowpoint Temple (**FICA**) | não é realocação: o templo está no repo, com placa, sem trava de pós-jogo, e o B5F vazio. Falta só pôr o encontro; a trava do Platinum é ter os três Regis no time, e Hoenn está 100% |
| Manaphy e Phione | nenhum (ovo de Ranger) | o Manaphy nunca teve mapa e precisa de lar inventado; o Phione sai dele no Day Care (`src/daycare.c:1047`) e resolve-se sozinho depois |

A fila tem o status `realocar` e a tabela `LENDARIO_NO_ID` que o dispara, e
**hoje ele fica em zero linhas**, porque a fila do B6 é de `hidden_flag` e de
gatilho. A cobrança mora neste arquivo.

## Obra futura, separada: tirar os mapas cortados da ROM

Nada foi apagado: os mapas cortados continuam compilando, ocupando ROM e
alcançáveis por warp, e o que mudou é só que a régua parou de cobrá-los e a fila
parou de pedir trabalho neles. Remover a geometria mexe em `data/`, em
`map_groups.json` e nos warps de lá, então pede build e suíte; com a ROM em
98,69% de 32 MB (ESTADO 0.i), é a economia mais óbvia que existe.
