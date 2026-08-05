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
# Ele guarda as mudancas nao commitadas, builda o HEAD limpo, roda os
# validadores e o teste de emulador, e devolve as mudancas no fim, sempre,
# inclusive se algo falhar.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export DEVKITARM="${DEVKITARM:-$HOME/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64-arm-none-eabi}"
LOG=/tmp/antes_de_empurrar.log
FALHAS=0

guardou=0
if [ -n "$(git status --porcelain)" ]; then
    git stash -q -u && guardou=1
    echo "mudancas nao commitadas guardadas no stash"
fi

devolve() {
    [ "$guardou" = 1 ] && git stash pop -q 2>/dev/null && echo "stash devolvido"
}
trap devolve EXIT

passo() {  # passo "nome" "comando"
    # ponytail: `eval` aqui engolia as aspas simples de um grep por "'sprite': 0"
    # e o passo falhava com o jogo inteiro certo. Validador com falso positivo e
    # pior que validador nenhum: ensina a ignorar a saida. Use bash -c.
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

passo "build do HEAD limpo"        "make -j8"
passo "guarda de save"             "python3 dev_scripts/guarda_save.py"
passo "o declarado entrou na ROM"  "python3 dev_scripts/valida_rom.py"
passo "conectividade"              "python3 dev_scripts/valida_conectividade.py 2>&1 | grep -q 'warps quebrados: 0'"
passo "sprites e objetos"          "python3 dev_scripts/valida_mapas_sinnoh.py 2>&1 | grep -qE \"'sprite': 0\""

if [ -x dev_scripts/testa_critico.py ] || [ -f dev_scripts/testa_critico.py ]; then
    passo "treinador sem time"     "python3 dev_scripts/testa_critico.py --treinadores"
fi
if [ -f dev_scripts/testa_percurso.py ]; then
    passo "percurso no emulador"   "python3 dev_scripts/testa_percurso.py"
fi

echo
if [ "$FALHAS" = 0 ]; then
    grep -E 'EWRAM|IWRAM|ROM:' "$LOG" 2>/dev/null | tail -3
    echo "VERDE: pode empurrar."
    exit 0
fi
echo "$FALHAS passo(s) falharam. NAO empurre."
exit 1
