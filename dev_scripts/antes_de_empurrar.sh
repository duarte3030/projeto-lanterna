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

# -j4 e nao -j8: o Mac de 16 GB travou em 28/10/2026 com builds e agentes
# demais ao mesmo tempo. MAKE_JOBS sobrescreve, se a maquina aguentar.
passo "build do HEAD limpo"        "${MAKE_PREFIXO:-}make -j${MAKE_JOBS:-4}"
passo "guarda de save"             "python3 dev_scripts/guarda_save.py"
passo "o declarado entrou na ROM"  "python3 dev_scripts/valida_rom.py"
# `struct WarpData` guardava mapGroup e mapNum como s8 (include/global.h): o mapa
# de indice 128 de um grupo virava -128 dentro do warp e o jogo RESETAVA ao entrar
# nele. Custou 26 mapas mortos no grupo de portas de Sinnoh, todos com warp que
# o validador estatico dava por bom.
# Em 12/08/2026 os dois campos viraram u8, dentro da janela de quebra de save, e
# o teto de GRUPO subiu para 255 (o indice 255 fica reservado para MAP_UNDEFINED).
# O teto de MAPAS POR GRUPO continua cobrado em 128 aqui de proposito: o codigo
# aguenta 255, mas ninguem provou indice acima de 127 no emulador ainda. Quem
# precisar, meça primeiro e so entao suba este numero.
# K1 (28/10/2026, PRD de assets, anexo F 3.4): o teto de 128 deixava nascer o
# mapa de indice 127 no grupo de indice 127, e (127,127) e MAP_DYNAMIC
# (include/constants/maps.h): o warp para ele vira "volta para onde voce
# estava". No cartucho 2 o grupo 127 e Galar, com 94 mapas. Por isso o grupo
# de indice 127 tem teto proprio de 127 mapas (indices 0 a 126).
passo "grupo abaixo do teto" "python3 -c \"import json,sys; g=json.load(open('data/maps/map_groups.json')); go=g['group_order']; ruins=[(k,len(g[k])) for k in go if len(g[k])>128]; k1=[(go[127],len(g[go[127]]))] if len(go)>127 and len(g[go[127]])>127 else []; print('grupos:',len(go),'de 255; grupos com mais de 128 mapas:',ruins,'; grupo 127 com o mapa 127 (MAP_DYNAMIC):',k1); sys.exit(1 if ruins or k1 or len(go)>255 else 0)\""
# Os 11 portoes de mapa da trilha F (C1 a F3), com linha de base versionada:
# so reprova achado NOVO. Ver o cabecalho de dev_scripts/qa/valida_mapa.py.
passo "portoes de mapa (valida_mapa)" "python3 dev_scripts/qa/valida_mapa.py"
# Paletas de OBJ por tela (c2-galar-ui): nenhum mapa pode pedir mais tags de
# paleta de NPC numa mesma janela de criação do que os 16 slots menos os do
# campo (clima, jogador, efeitos, reflexo). Acima disso o NPC sai com a cor de
# outro, sem erro. Ver o cabeçalho de dev_scripts/qa/lente_paletas_obj.py.
passo "paletas de OBJ por tela"   "python3 dev_scripts/qa/lente_paletas_obj.py && python3 dev_scripts/qa/lente_paletas_obj.py --demo"
passo "conectividade"              "python3 dev_scripts/valida_conectividade.py 2>&1 | grep -q 'warps quebrados: 0'"
passo "sprites e objetos"          "python3 dev_scripts/valida_mapas_sinnoh.py 2>&1 | grep -qE \"'sprite': 0\""

# --piso, e nao o total: o numero nunca chega a 100%, porque existe warp
# legitimo em tile que nao e porta (o motor tambem entra por script, e muita
# porta de Hoenn e trocada por setmetatile em tempo de execucao). Exigir 100%
# deixava este passo vermelho para sempre, que e o mesmo que nao ter passo. O
# que interessa e catastrofe por regiao: Johto passou a madrugada em 1,6%.
# Curva de nível da campanha de Galar e Unova (cartucho 2, decisão 130): nenhum
# treinador de campanha acima de 100; Unova dentro do trecho da ordem do BW3G
# (dev_scripts/progressao_unova_bw3g.json), líder no nível do ginásio de mesmo
# número do Black 2 e mato na curva do mapa; Galar a até 10 níveis dos casados
# vizinhos. Achado fora de dev_scripts/prova_curva_c2_base.json reprova.
[ -f dev_scripts/prova_curva_c2.py ] && \
    passo "curva de nivel da campanha" "python3 dev_scripts/prova_curva_c2.py && python3 dev_scripts/prova_curva_c2.py --demo && python3 dev_scripts/curva_c2.py --demo && python3 dev_scripts/ordem_bw3g_c2.py --demo"
# Voo de Unova e Galar (c2-lacunas): toda cidade com Pokécenter tem pouso
# passável e flag de voo, e src/data/region_map/voo_c2.h é o que o gerador dá hoje.
[ -f dev_scripts/voo_c2.py ] && \
    passo "destinos de voo"          "python3 dev_scripts/voo_c2.py --demo"
# Fundos de Galar: todo líder de ginásio de Galar tem estádio e a tabela gerada
# (src/data/battle_environment_galar.h) é a que o script dá hoje.
[ -f dev_scripts/fundos_galar.py ] && \
    passo "fundos de Galar"          "python3 dev_scripts/fundos_galar.py --demo"
# Música de Galar e Unova (c2-musica): todo mapa de Galar e Unova toca o que a regra
# de dev_scripts/musica_c2.py pede, e toda MUS_GALAR_* e MUS_UNOVA_* citada existe.
[ -f dev_scripts/musica_c2.py ] && \
    passo "música de Galar e Unova"   "python3 dev_scripts/musica_c2.py --demo"
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

# TODO (para o B1/B2, achado em 12/08/2026 medindo o teto de grupo): a escada do
# OreburghCity_PokemonCenter_1F para o B1F, em (13,6), e INALCANCAVEL a pe. Os
# tiles (13,6) e (13,7) formam um bolsao isolado no map.bin (elevacao 4 e 3 sem
# vizinho andavel; (12,6), (12,7) e (13,8) sao colisao 1). O warp existe e o
# conserto de MAP_DYNAMIC em src/field_control_avatar.c ja fez o destino ficar
# certo, mas ninguem consegue pisar nele ate a colisao ser aberta. Enquanto isso
# nao acontecer, esse conserto nao tem como ser provado no emulador.
