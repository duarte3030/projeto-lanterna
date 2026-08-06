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
