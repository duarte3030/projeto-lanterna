#!/bin/bash
# Roda tudo que separa "commitei" de "funciona", e recusa se algo falhar.
#
# Existe porque eu quebrei o master duas vezes na mesma madrugada, do mesmo
# jeito: `git add -A` numa arvore onde agentes escrevem captura um INSTANTE, nao
# um estado coerente. Buildar antes de commitar nao basta, porque o build e de
# outro instante. A unica prova e buildar EXATAMENTE o que esta commitado.
#
# Uso:
#     bash dev_scripts/antes_de_empurrar.sh
#
# COMO ELE ISOLA O HEAD, e por que nao usa `git stash`
# ----------------------------------------------------
# A primeira versao guardava as mudancas com `git stash -u`, buildava e devolvia
# no fim. Isso destruiu trabalho de verdade em 05/08/2026: com varios agentes
# escrevendo na mesma arvore, o stash de um levou junto os arquivos de outro, e
# o `pop` caiu no `git add -A` de uma terceira sessao. O agente que perdeu os
# arquivos so descobriu conferindo byte a byte o que tinha ido parar no commit
# alheio.
#
# Agora ele cria uma WORKTREE descartavel no HEAD. A arvore de trabalho de
# ninguem e tocada, e o build e do commit, nao do instante.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
REPO=$(pwd)
export DEVKITARM="${DEVKITARM:-$HOME/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64-arm-none-eabi}"
# ponytail: caminho fixo aqui fez duas sessoes rodando o portao ao mesmo tempo
# sobrescreverem o log uma da outra, e o `tail` de uma mostrou a compilacao da
# outra em vez da causa da falha. $$ e o pid.
LOG=/tmp/antes_de_empurrar.$$.log
FALHAS=0

WT=$(mktemp -d /tmp/verifica-head.XXXXXX)
rm -rf "$WT"
if ! git worktree add --detach -q "$WT" HEAD 2>/dev/null; then
    echo "nao consegui criar worktree em $WT; abortando sem tocar na sua arvore"
    exit 1
fi
limpa() {
    cd "$REPO" || return
    git worktree remove --force "$WT" 2>/dev/null || rm -rf "$WT"
}
trap limpa EXIT

cd "$WT" || exit 1
echo "verificando o HEAD em worktree isolada (sua arvore nao foi tocada)"

passo() {  # passo "nome" "comando"
    # ponytail: `eval` engolia as aspas simples de um grep por "'sprite': 0" e o
    # passo falhava com o jogo inteiro certo. Validador com falso positivo e pior
    # que validador nenhum: ensina a ignorar a saida. Por isso bash -c.
    printf '%-34s' "$1"
    if bash -c "$2" > "$LOG" 2>&1; then
        echo "ok"
    else
        echo "FALHOU  (log em $LOG)"
        tail -6 "$LOG" | sed 's/^/    /'
        FALHAS=$((FALHAS+1))
    fi
}

# ponytail: arquivo duplicado com espaco no nome faz o make falhar sem imprimir
# nada. Custa nada limpar antes.
find . -name "* [2-9].*" -not -path "./.git/*" -delete 2>/dev/null

# ponytail: o binario do runner esta no gitignore (so o .c e versionado), entao
# em maquina nova o portao ficava vermelho no passo do emulador por FALTA DE
# FERRAMENTA, e nao por bug no jogo. Compila se faltar, e segue.
if [ ! -x "$REPO/dev_scripts/gba_runner" ]; then
    printf '%-34s' "compilando o gba_runner"
    if cc -O2 -o "$REPO/dev_scripts/gba_runner" "$REPO/dev_scripts/gba_runner.c" \
         -I/opt/homebrew/include -L/opt/homebrew/lib \
         $(pkg-config --cflags --libs libpng 2>/dev/null) -lmgba > "$LOG" 2>&1; then
        echo "ok"
    else
        echo "FALHOU  (log em $LOG; falta libmgba ou libpng?)"
    fi
fi

passo "build do HEAD limpo"        "make -j8"
passo "guarda de save"             "python3 dev_scripts/guarda_save.py"
passo "o declarado entrou na ROM"  "python3 dev_scripts/valida_rom.py"
passo "conectividade"              "python3 dev_scripts/valida_conectividade.py 2>&1 | grep -q 'warps quebrados: 0'"
passo "sprites e objetos"          "python3 dev_scripts/valida_mapas_sinnoh.py 2>&1 | grep -qE \"'sprite': 0\""

# --piso, e nao o total: o numero nunca chega a 100%, porque existe warp
# legitimo em tile que nao e porta (o motor tambem entra por script, e muita
# porta de Hoenn e trocada por setmetatile em tempo de execucao). Exigir 100%
# deixava este passo vermelho para sempre, que e o mesmo que nao ter passo. O
# que interessa e catastrofe por regiao: Johto passou a madrugada em 1,6%.
[ -f dev_scripts/valida_warp_tile.py ] && \
    passo "warp em tile que dispara" "python3 dev_scripts/valida_warp_tile.py --piso 60"
[ -f dev_scripts/testa_critico.py ] && \
    passo "treinador sem time"       "python3 dev_scripts/testa_critico.py --treinadores"
[ -f dev_scripts/testa_percurso.py ] && \
    passo "percurso no emulador"     "python3 dev_scripts/testa_percurso.py"

echo
if [ "$FALHAS" = 0 ]; then
    grep -E 'EWRAM|IWRAM|ROM:' "$LOG" 2>/dev/null | tail -3
    echo "VERDE: pode empurrar."
    exit 0
fi
echo "$FALHAS passo(s) falharam. NAO empurre."
exit 1
