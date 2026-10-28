#!/bin/bash
# Prova no emulador dos retratos da fase 2. Duas partes, nenhuma toca a ROM de verdade:
#
#   A) ROM de PROVA com 5 cenas de 8 retratos (Kalos, Alola, Paldea, extras, os 5 retocados à mão),
#      sobre o fundo GALAR_FIELD (dev_scripts/prova_arte_fase2/prova_arte.c).
#   B) BATALHA FORÇADA de verdade: cópia da ROM construída com o retrato do campeão Genesis trocado
#      (dev_scripts/prova_arte_fase2_batalha.py), rodando o duelo T116.5 pelo emulador.
#
# Uso:  bash dev_scripts/prova_arte_fase2.sh DIRETORIO_DE_SAIDA
# Requer a árvore COMMITADA e limpa em src/main.c (o script o altera e o restaura com git checkout)
# e a ROM de verdade já construída (pokeemerald.gba). O make roda com -j4 sob o lock de build.
set -euo pipefail
cd "$(dirname "$0")/.."
SAIDA="${1:?diretório de saída}"
mkdir -p "$SAIDA"
export DEVKITARM="${DEVKITARM:-$HOME/toolchains/arm-gnu-toolchain-15.2.rel1-darwin-arm64-arm-none-eabi}"
export DYLD_LIBRARY_PATH="$HOME/toolchains/lib/ffmpeg8-compat${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
git diff --quiet -- src/main.c || { echo "src/main.c sujo; abortando"; exit 1; }
[ -f pokeemerald.gba ] || { echo "falta a ROM de verdade (make -j4 antes)"; exit 1; }
cp pokeemerald.gba "$SAIDA/rom-verdadeira.gba"
cp pokeemerald.map "$SAIDA/rom-verdadeira.map"

# ---- B) batalha forçada, sobre a ROM de verdade (antes de a ROM de prova sobrescrevê-la)
python3 dev_scripts/prova_arte_fase2_batalha.py "$SAIDA/rom-verdadeira.gba" "$SAIDA/batalha" \
    KALOS_DIANTHA ALOLA_HAU PALDEA_NEMONA_V > "$SAIDA/batalha.log" 2>&1 || true

# ---- A) cenas
desfaz() {
    rm -f src/prova_arte.c
    git checkout -q -- src/main.c
}
trap desfaz EXIT
cp dev_scripts/prova_arte_fase2/prova_arte.c src/prova_arte.c
sed -i '' 's/^extern void gInitialMainCB2(void);/extern void gInitialMainCB2(void);\nextern void CB2_ProvaArte(void);/' src/main.c
sed -i '' 's/SetMainCallback2(gInitialMainCB2);/SetMainCallback2(CB2_ProvaArte);/' src/main.c
lockf /tmp/pokemon-claude-build.lock make -j4 > "$SAIDA/build-prova.log" 2>&1
cp pokeemerald.gba "$SAIDA/rom-prova-arte.gba"
R=dev_scripts/gba_runner
P="60:NONE"
for i in 0 1 2 3 4; do
    "$R" "$SAIDA/rom-prova-arte.gba" 200 "$P" "$SAIDA/cena$i.png"
    P="$P,3:A,60:NONE"
done
echo "capturas em $SAIDA"
