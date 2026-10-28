#!/bin/bash
# Prova no emulador da arte da fase 1: monta uma ROM de PROVA (nunca a de verdade),
# captura três cenas com o gba_runner e desfaz tudo.
#
#   cena 0: 3 retratos novos + 3 NPCs novos
#   cena 1: fundo de batalha GALAR_FIELD + retrato + NPC
#   cena 2: fundo de batalha GALAR_STADIUM_RED + retrato
#
# Uso:  bash dev_scripts/prova_arte_fase1.sh DIRETORIO_DE_SAIDA
# Requer a árvore COMMITADA e limpa em src/main.c (o script o altera e o restaura com git checkout).
# O make roda com -j4. DYLD_LIBRARY_PATH é o do gba_runner (ffmpeg8-compat).
set -euo pipefail
cd "$(dirname "$0")/.."
SAIDA="${1:?diretório de saída}"
mkdir -p "$SAIDA"
export DEVKITARM="${DEVKITARM:-$HOME/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64-arm-none-eabi}"
export DYLD_LIBRARY_PATH="$HOME/toolchains/lib/ffmpeg8-compat${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
git diff --quiet -- src/main.c || { echo "src/main.c sujo; abortando"; exit 1; }

desfaz() {
    rm -f src/prova_arte.c
    git checkout -q -- src/main.c
}
trap desfaz EXIT

cp dev_scripts/prova_arte_fase1/prova_arte.c src/prova_arte.c
sed -i '' 's/^extern void gInitialMainCB2(void);/extern void gInitialMainCB2(void);\nextern void CB2_ProvaArte(void);/' src/main.c
sed -i '' 's/SetMainCallback2(gInitialMainCB2);/SetMainCallback2(CB2_ProvaArte);/' src/main.c
make -j4 > "$SAIDA/build-prova.log" 2>&1
cp pokeemerald.gba "$SAIDA/rom-prova-arte.gba"

R=dev_scripts/gba_runner
"$R" "$SAIDA/rom-prova-arte.gba" 200 "60:NONE" "$SAIDA/cena0.png"
"$R" "$SAIDA/rom-prova-arte.gba" 200 "60:NONE,3:A,60:NONE" "$SAIDA/cena1.png"
"$R" "$SAIDA/rom-prova-arte.gba" 200 "60:NONE,3:A,20:NONE,3:A,60:NONE" "$SAIDA/cena2.png"
echo "capturas em $SAIDA"
