# projeto-lanterna

Projeto pessoal de estudo: ferramentas de build, conversao de dados de mapa e
testes automatizados para uma engine 2D de console portatil.

O que tem aqui de meu, e o motivo do repositorio existir:

| pasta | o que e |
|---|---|
| `dev_scripts/` | as ferramentas: conversores de formato de mapa, validadores, um portao de pre-push e um runner headless que roda a build num emulador e le a memoria dela |
| `data/` | dados de mapa e de evento em JSON e em assembly |
| `test/` | testes da engine |

O ponto tecnico interessante nao e o conteudo, sao as ferramentas de
verificacao. A mais util e o `dev_scripts/gba_runner.c`, que builda, roda num
emulador sem tela e **le a memoria do programa** para afirmar coisas como "esta
posicao mudou" ou "esta flag acendeu", em vez de comparar pixel. Junto com ele,
`dev_scripts/antes_de_empurrar.sh` builda o HEAD limpo numa worktree isolada e
recusa o push se qualquer validador reprovar.

Documentacao interna do estado do projeto: [ESTADO.md](ESTADO.md).

Este repositorio nao distribui binario de fabrica de ninguem. Os tres arquivos
de multiboot que vinham na base foram substituidos por stub de zeros e ficam
fora do controle de versao (ver `.gitignore`).

## Base

Construido sobre o `pokeemerald-expansion` da RHH (Rom Hacking Hideout), que por
sua vez e construido sobre o projeto de descompilacao `pret/pokeemerald`.
Creditos completos da base em [CREDITS.md](CREDITS.md) e o README original da
base em [README-upstream.md](README-upstream.md).

## Créditos a terceiros

Parte da geometria de mapa deste projeto foi derivada de trabalho fan-made de
outras pessoas. O crédito é obrigatório e vem antes de qualquer uso.

### Galar: demake "Sword and Shield Ultimate Plus"

| item | valor |
|---|---|
| obra | Pokémon Sword and Shield Ultimate Plus, versão em inglês |
| versão usada | v1.2.1.2 |
| base | Pokémon FireRed (GBA), revisões 1.0 e 1.1 |
| autoria | **PCLG** (criação original em 2020 e o overhaul "Ultimate Plus"), **Jeanstars** (remasterização "SwSh Ultimate", 2023) e **Phantonomy** (tradução para inglês e implementação de recursos) |
| créditos adicionais declarados pelos autores | KingTapir (tiles), hyo (sprite do Victor), Chronoyevsky (WikiGen), LibertyTwins, Shiny Miner, Compumaxx e ansh860 (patches de menu), LibertyTwins (MIDIs de GBA), Zake (tradução do verificador de EV/IV), Skeli e equipe (CFRU), Rycule (suporte a RetroAchievements) |
| distribuição oficial | repositório de patches `Ddaretrogamer/Sword-and-Shield-Ultimate-Plus` no GitHub e a thread de lançamento no PokéCommunity (`threads/526384`) |
| licença | **não declarada** pelos autores. Não existe LICENSE no repositório de patches |

O que foi usado aqui: a geometria dos mapas de Galar (blockdata, tilesets,
colisão e eventos), extraída da ROM aplicada localmente. O material de origem
mora fora deste repositório, em `fontes-mapas/galar-swsh/`, que não tem remote e
nunca é publicado.

**Regras de uso, e elas não são negociáveis:**

- **Uso privado.** Nada derivado desse demake é distribuído por este projeto.
- **Nenhuma ROM sai daqui**, nem a de origem, nem a construída.
- **Nunca publicar sem crédito e sem permissão.** Como a licença não é
  declarada, publicar qualquer peça derivada exige autorização escrita dos
  autores acima, pedida antes e não depois.
- Este repositório distribui **código e dados de origem**, nunca binário de
  fábrica de ninguém.

**Pendência registrada:** a tela de créditos DENTRO do jogo, com esses mesmos
nomes, é obra da fase de montagem do cartucho e ainda não existe. Enquanto ela
não existir, este bloco é o único crédito, e ele é suficiente só porque nada
saiu daqui.
