/*
 * gba_runner: roda uma ROM de GBA headless via libmgba, aplica um roteiro de
 * botoes, salva um PNG do framebuffer final (240x160) e LE A MEMORIA do jogo.
 *
 * ESTA e a fonte de verdade do runner; ele vive no repo porque e a base de
 * todos os testes de dev_scripts/testa_critico.py, e ficar fora de controle de
 * versao ja quase custou a ferramenta. Compilar com:
 *
 *   cc -O2 -o dev_scripts/gba_runner dev_scripts/gba_runner.c \
 *      -I/opt/homebrew/include -L/opt/homebrew/lib \
 *      $(pkg-config --cflags --libs libpng) -lmgba
 *
 * Uso:
 *   gba_runner <rom.gba> <frames> <roteiro> <saida.png> [opcoes]
 *
 * Roteiro: lista separada por virgula de "N:BOTAO" ou "N:BOTAO*K".
 *   N     = quantos quadros rodar segurando esse botao (0 = so espera)
 *   BOTAO = A,B,SELECT,START,RIGHT,LEFT,UP,DOWN,R,L ou NONE (nenhum botao)
 *   *K    = repete o passo K vezes (opcional)
 *   sufixo "!" = segura o botao o passo inteiro (ex.: "30:R+START!")
 *   "N:FLAG=0x2A0" = acende a flag 0x2A0 direto na memoria e roda N quadros
 *   "N:VAR=0x4001=7" = grava 7 na var 0x4001 e roda N quadros
 *   "N:OPT=32" = grava 32 no byte das opcoes do modo de teste (precisa de
 *                --opcoes) e roda N quadros
 * Exemplo: "120:START,60:A,30:DOWN*10"
 * Roteiro vazio ("") so roda os N quadros iniciais sem apertar nada.
 *
 * Opcoes:
 *   --dump-estado         imprime o estado lido da EWRAM depois de cada passo
 *   --flag N              inclui a flag N (decimal ou 0x..) no dump
 *   --var N               inclui a var N (0x4000+) no dump
 *   --sb1ptr 0x030051cc   endereco de gSaveBlock1Ptr (vem do pokeemerald.map)
 *   --inimigo 0x02024xxx  endereco de gParties (vem do pokeemerald.map)
 *   --nivel-offset N      bytes de gParties ate o .level do 1o mon do inimigo
 *                         (medido pelo probe do testa_critico.py, nunca chutado)
 *   --nivel-passo N       sizeof(struct Pokemon): faz o dump imprimir tambem
 *                         nivelinimigo1..5, ou seja o time INTEIRO do adversario
 *   --timeinimigo P,O,S,T,L  offsets de personality, otId, secure, o tamanho de
 *                         um substruct e o offset de level dentro de struct
 *                         Pokemon: DECIFRA o time do inimigo e imprime
 *                         especie0..5, tera0..5 e item0..5
 *   --bolsa OFF,N,KEY     offset da BOLSA (struct Bag) dentro do SaveBlock1, o
 *                         numero total de slots dos cinco bolsos e o offset de
 *                         encryptionKey dentro do SaveBlock2 (todos medidos
 *                         pelo probe do testa_critico.py). Com --item, imprime
 *                         item_0xNNN=<quantidade decifrada>, ou -1 se ninguem
 *                         passou --bolsa (nunca 0, que se confundiria com
 *                         "nao tem")
 *   --item N              inclui o item N (decimal ou 0x..) no dump da bolsa
 *   --hp HP,MAXHP         offsets de hp e maxHP dentro de struct Pokemon
 *                         (medidos pelo probe do testa_critico.py): imprime
 *                         hp0..hp5 e hpmax0..hpmax5 do time decifrado, e
 *                         habilita o passo de roteiro "N:HP=slot=valor"
 *   --opcoes A,N          gSaveBlock2Ptr e o offset de filler_90: imprime
 *                         opcoes=<byte das opcoes do modo de teste>
 *   --batalhamons A,T,E,N,G  gBattleMons, sizeof(struct BattlePokemon) e os
 *                         offsets de species/level/moves: imprime bespecie,
 *                         bnivel e bgolpe0..3 do adversario ativo
 *   --gimmick A,N         gBattleStruct e o offset do u16 de
 *                         opponentMonCanTera/opponentMonCanDynamax
 *   --partycount 0x02031c38  endereco de gPartiesCount
 *   --oponente 0x02000928 endereco de gTrainerBattleParameter
 *   --offsets a,b,c,d,e,f,g  offsets dentro de SaveBlock1, medidos da fonte
 *   --sem-png             nao grava PNG nenhum (teste que so olha memoria)
 *
 * POR QUE LER MEMORIA: teste que infere estado da tela e palpite. Dois crashes
 * da sessao de 05/08/2026 passaram por seis agentes porque todo teste olhava so
 * pixel. "flag acesa" e "time com 1 Pokemon" sao fato quando vem da EWRAM.
 */
#include <mgba/core/core.h>
#include <mgba/core/config.h>
#include <mgba/core/blip_buf.h>
#include <mgba/internal/gba/input.h>
#include <mgba-util/vfs.h>
#include <png.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ---------------------------------------------------------------------------
 * Mapa da memoria do pokeemerald-expansion deste repo.
 *
 * Os DOIS enderecos abaixo mudam a cada link e por isso podem vir por argv
 * (o testa_critico.py le eles do pokeemerald.map). Os OFFSETS dentro da
 * struct so mudam se include/global.h mudar, e foram MEDIDOS, nao copiados do
 * comentario do header (o comentario dizia vars em 0x139C e o valor real e
 * 0x13E0, porque NUM_FLAG_BYTES cresceu de 0x12C para 0x16F na expansion).
 *
 * Receita da medicao, se global.h mudar:
 *   printf '#include "global.h"\nconst unsigned gP[]={offsetof(struct SaveBlock1,vars)};\n' > /tmp/p.c
 *   arm-none-eabi-gcc -c -iquote include -DMODERN=1 -DTESTING=0 -DEMERALD \
 *       -std=gnu17 -mthumb -mabi=apcs-gnu -march=armv4t -O0 -o /tmp/p.o /tmp/p.c
 *   arm-none-eabi-objdump -s -j .rodata /tmp/p.o
 * ------------------------------------------------------------------------- */
#define SB1_POS_X         0x000   /* struct Coords16: s16 x, s16 y */
#define SB1_POS_Y         0x002
#define VARS_START        0x4000

/* Os offsets abaixo sao os da build de 05/08/2026 e servem de padrao, mas
   PODEM E DEVEM vir por argv (--offsets loc,layout,party,flags,vars,nflags).
   Motivo medido: se global.h mover flags[] e o leitor continuar lendo o offset
   antigo, o leitor le o byte errado e AINDA ASSIM parece certo, porque a save
   antiga tem o valor velho naquele lugar. Foi exatamente isso que fez o teste
   T11 passar contra uma ROM propositalmente incompativel. Leitor com offset
   chumbado nao e testemunha, e adivinho. */
static uint32_t SB1_LOCATION    = 0x004;  /* WarpData: mapGroup em +0, mapNum em +1 */
static uint32_t SB1_MAPLAYOUTID = 0x032;  /* so muda quando o mapa REALMENTE carrega */
static uint32_t SB1_PARTYCOUNT  = 0x234;
static uint32_t SB1_FLAGS       = 0x1270;
static uint32_t SB1_VARS        = 0x13E0;
static int      FLAGS_COUNT     = 2936;
static int      VARS_COUNT      = 256;

static uint32_t g_sb1ptr = 0x030051cc;      /* gSaveBlock1Ptr */
static uint32_t g_partycount = 0x02031c38;  /* gPartiesCount, indice 0 = jogador */

/* gTrainerBattleParameter. O campo opponentA e um u16 em +2 (medido com o
   mesmo probe dos offsets de SaveBlock1). Existe para provar CONTRA QUEM a
   batalha comecou, e nao so que uma batalha comecou: em Kanto, 623 constantes
   de treinador sao apelidos de outro treinador, entao "abriu batalha no ginasio
   de Pewter" e verdade mesmo quando quem aparece e um montanhista de Hoenn. */
static uint32_t g_oponente = 0x02000928;
#define OPONENTE_A_OFFSET 2

/* gParties, e o deslocamento em bytes dali ate gParties[B_TRAINER_OPPONENT_A][0]
   .level. Existe para o bloco B8: a curva do selvagem so e provavel se der para
   ler o NIVEL do bicho que apareceu, e "abriu batalha" nao prova faixa nenhuma.
   O deslocamento NAO e chumbado aqui: quem mede e o probe de offsets_da_fonte()
   no testa_critico.py, compilando contra o global.h da propria build, porque
   sizeof(struct Pokemon) muda com a versao do expansion. Zero = nao pedido. */
static uint32_t g_inimigo = 0;
static uint32_t g_nivel_offset = 0;
/* Passo em bytes de um mon para o proximo dentro do time do inimigo, ou seja
   sizeof(struct Pokemon). Com ele o dump imprime o nivel dos SEIS slots e nao
   so o do primeiro, que e o que separa "o lider veio no nivel 5" de "o primeiro
   bicho dele veio no nivel 5": o ACE, que e quem carrega o gimmick, e o ULTIMO
   do time. Medido pelo probe do testa_critico.py, nunca chutado. */
static uint32_t g_nivel_passo = 0;

/* ESPECIE, TERA e ITEM dos SEIS slots do time do inimigo, DECIFRADOS.
   O comentario do g_bmons abaixo dizia que gParties guarda especie e item
   "dentro dos substructs cifrados", e por isso ate 21/08/2026 o runner so lia
   NIVEL do time e especie do batalhador ATIVO. Isso deixava um buraco de
   prova: com o modo LV.5 ligado os seis niveis viram 5, e entao o time inteiro
   passa a ser indistinguivel de qualquer outro time de seis. Quem carrega o
   Mega e o ACE, que e o ULTIMO slot e nunca o ativo, e a pedra dele e
   justamente um ITEM.
   A decifra e a mesma de src/pokemon.c: cada u32 de `secure.raw` guarda
   valor ^ otId ^ personality, e qual dos quatro substructs e o 0 sai da
   tabela sSubstructOffsets[SUBSTRUCT_TYPE_0][personality % 24], copiada
   literal abaixo. O primeiro u32 do substruct 0 carrega os tres campos de bits
   que interessam (include/pokemon.h): species:11, teraType:5, heldItem:10.
   Nenhum offset e chumbado: todos vem do probe do testa_critico.py. */
static uint32_t g_time_pers = 0, g_time_otid = 0, g_time_sec = 0,
                g_time_sub = 0, g_time_niv = 0;
static int g_tem_time = 0;

/* HP e maxHP dentro de struct Pokemon (--hp). Nasceram em 22/08/2026 para o
   caso adversarial do `special HealPlayerParty` de Galar: ate aqui o runner
   sabia dizer QUAL Pokemon estava no slot e em que nivel, e nao sabia dizer se
   ele estava machucado. Sem isso, cena de enfermeira e indistinguivel de cena
   que so imprime texto, que e exatamente o modo como um `special` traduzido
   para o indice ERRADO passaria verde.
   Os dois offsets vem do probe do testa_critico.py, nunca chumbados: hp e
   maxHP ficam FORA do bloco cifrado (struct Pokemon, depois de box), entao a
   leitura e direta e nao passa pela decifra do substruct. */
static uint32_t g_hp_off = 0, g_hpmax_off = 0;
static int g_tem_hp = 0;

/* Base do time decifrado (gParties do lado pedido), ou 0 se ninguem pediu. */
static uint32_t base_do_time(void) {
    if (!g_inimigo || !g_nivel_passo || !g_tem_time) return 0;
    return g_inimigo + g_nivel_offset - g_time_niv;
}

/* gSaveBlock2Ptr e o offset de filler_90 dentro do SaveBlock2. O byte
   filler_90[0] e onde moram as seis opcoes do modo de teste (include/global.h,
   TEST_OPT_*). Ler ele e o unico jeito de provar por FATO que o menu OPTION
   gravou a opcao, em vez de deduzir do efeito. */
static uint32_t g_sb2ptr = 0;
static uint32_t g_opcoes_offset = 0;

/* gBattleMons e o recorte da struct BattlePokemon. Ao contrario do time em
   gParties, que guarda especie e golpes DENTRO dos substructs cifrados, o
   gBattleMons e a copia decifrada do batalhador ativo: especie, nivel e os
   quatro golpes sao campos simples. E a camada certa para provar que baixar o
   nivel para 5 nao trocou o Pokemon nem regerou o moveset. O indice 1 e
   B_POSITION_OPPONENT_LEFT. */
static uint32_t g_bmons = 0, g_bmons_tam = 0, g_bmons_esp = 0,
                g_bmons_niv = 0, g_bmons_gol = 0;

/* gBattleStruct (um PONTEIRO em EWRAM) e o offset do u16 que carrega os dois
   campos de bits opponentMonCanTera:6 e opponentMonCanDynamax:6
   (include/battle.h). Sao eles que autorizam o adversario a usar o gimmick
   (src/battle_gimmick.c). Le-se o u16 INTEIRO de proposito: comparar o mesmo
   valor com a opcao LV.5 ligada e desligada prova que a queda de nivel nao
   apaga gimmick nenhum, e nao depende de saber em que bit cada um mora. */
static uint32_t g_bstruct = 0, g_gimmick_offset = 0;

/* enderecos pedidos no dump */
#define MAX_PEDIDOS 64
static int g_flags_pedidas[MAX_PEDIDOS], g_n_flags = 0;
static int g_vars_pedidas[MAX_PEDIDOS], g_n_vars = 0;
/* --palobj 0xXXXX: reporta se a cor de 15 bits esta em alguma palette OBJ
   carregada (PLTT 0x05000200-0x050003FF). E a prova de que a palette de um
   sprite foi registrada de verdade: o caso dos NPCs verdes de Kanto passou
   por toda a suite porque nenhum teste olhava isso. */
static int g_palobj_pedidas[MAX_PEDIDOS], g_n_palobj = 0;
/* --bolsa OFF,N,KEY + --item 0xNNN: quantidade do item NA BOLSA (os cinco bolsos).
   `struct ItemSlot` e {u16 itemId; u16 quantity} e a QUANTIDADE e cifrada com
   os 16 bits baixos de gSaveBlock2Ptr->encryptionKey (src/item.c). Ler o time
   nao prova a bolsa: o NPC da Dex entrega NOVE itens de troca de forma (cinco
   sao POCKET_KEY_ITEMS e os quatro nectares de Alola sao POCKET_ITEMS), e
   nenhum deles entra em gPlayerParty. Por isso a varredura e do struct Bag
   INTEIRO, cujos cinco bolsos sao `struct ItemSlot` contiguos: a pergunta e
   "esta na bolsa?", e responder isso nao devia exigir saber de bolso. */
static uint32_t g_bolsa_off = 0, g_bolsa_n = 0, g_chave_off = 0;
static int g_itens_pedidos[MAX_PEDIDOS], g_n_itens = 0;
static int g_dump_estado = 0;
static int g_sem_png = 0;

/* "0x02031928,140,0" -> vetor de n numeros. strtoul com base 0 de proposito:
   os enderecos chegam em hexadecimal do pokeemerald.map e sscanf("%u") os leria
   como zero, calado. */
static int le_lista(const char *s, uint32_t *v, int n) {
    char *fim = (char *)s;
    for (int i = 0; i < n; i++) {
        if (i && *fim == ',') fim++;
        else if (i) return 0;
        v[i] = (uint32_t)strtoul(fim, &fim, 0);
    }
    return *fim == '\0';
}

static uint32_t sb1(struct mCore *core) {
    return core->busRead32(core, g_sb1ptr);
}

static int le_flag(struct mCore *core, int id) {
    uint32_t base = sb1(core);
    if (!base || id < 0 || id >= FLAGS_COUNT) return -1;
    uint32_t byte = core->busRead8(core, base + SB1_FLAGS + (id / 8));
    return (byte >> (id & 7)) & 1;
}

static void acende_flag(struct mCore *core, int id) {
    uint32_t base = sb1(core);
    if (!base || id < 0 || id >= FLAGS_COUNT) {
        fprintf(stderr, "acende_flag: SaveBlock1 ainda nao existe ou flag %d fora de faixa\n", id);
        return;
    }
    uint32_t end = base + SB1_FLAGS + (id / 8);
    uint32_t byte = core->busRead8(core, end);
    core->busWrite8(core, end, (uint8_t)(byte | (1u << (id & 7))));
}

static int le_var(struct mCore *core, int id) {
    uint32_t base = sb1(core);
    int i = id - VARS_START;
    if (!base || i < 0 || i >= VARS_COUNT) return -1;
    return (int)core->busRead16(core, base + SB1_VARS + i * 2);
}

/* Grava o byte das opcoes do modo de teste (SaveBlock2.filler_90[0]).
   Existe porque em 19/08/2026 a opcao LV.5 passou a NASCER LIGADA no jogo novo
   (src/new_game.c), e os casos que medem a curva NATURAL de nivel precisam
   declarar que querem ela desligada. Fazer isso pelo menu OPTION custaria ~700
   quadros de navegacao por caso e amarraria a prova da curva ao layout do menu;
   escrever o byte e o mesmo efeito do TestOptionSet e nao depende de menu. */
static void grava_opcoes(struct mCore *core, int valor) {
    if (!g_sb2ptr) {
        fprintf(stderr, "OPT=: --opcoes nao foi passado, sem endereco de gSaveBlock2Ptr\n");
        return;
    }
    uint32_t sb2 = core->busRead32(core, g_sb2ptr);
    if (!sb2) {
        fprintf(stderr, "OPT=: SaveBlock2 ainda nao existe\n");
        return;
    }
    core->busWrite8(core, sb2 + g_opcoes_offset, (uint8_t)valor);
}

static void grava_var(struct mCore *core, int id, int valor) {
    uint32_t base = sb1(core);
    int i = id - VARS_START;
    if (!base || i < 0 || i >= VARS_COUNT) {
        fprintf(stderr, "grava_var: SaveBlock1 nao existe ou var 0x%X fora de faixa\n", id);
        return;
    }
    core->busWrite16(core, base + SB1_VARS + i * 2, (uint16_t)valor);
}

/* Uma linha por dump, formato chave=valor para o Python parsear sem regex feia.
   sb1=0 significa que o jogo ainda nao criou o save block (tela de titulo,
   ou reset). Isso sozinho ja e prova de reset depois do jogo ter comecado. */
static void dump_estado(struct mCore *core, const char *rotulo) {
    uint32_t base = sb1(core);
    printf("ESTADO %s sb1=0x%08x", rotulo, base);
    if (base) {
        /* location e escrito por SetWarpDestination ANTES do mapa carregar, entao
           sozinho ele NAO prova que o mapa carregou: medido em 05/08/2026, um
           warp para MAP_PEWTER_CITY deixou location=37.2 com a tela preta.
           layout so muda quando o mapa entra de verdade. */
        printf(" grupo=%d num=%d layout=%d x=%d y=%d timesb1=%d timevivo=%d",
               (int)core->busRead8(core, base + SB1_LOCATION),
               (int)core->busRead8(core, base + SB1_LOCATION + 1),
               (int)core->busRead16(core, base + SB1_MAPLAYOUTID),
               (int16_t)core->busRead16(core, base + SB1_POS_X),
               (int16_t)core->busRead16(core, base + SB1_POS_Y),
               (int)core->busRead8(core, base + SB1_PARTYCOUNT),
               (int)core->busRead8(core, g_partycount));
        printf(" oponente=%d",
               (int)core->busRead16(core, g_oponente + OPONENTE_A_OFFSET));
        if (g_inimigo) {
            printf(" nivelinimigo=%d",
                   (int)core->busRead8(core, g_inimigo + g_nivel_offset));
            for (int i = 1; g_nivel_passo && i < 6; i++)
                printf(" nivelinimigo%d=%d", i,
                       (int)core->busRead8(core, g_inimigo + g_nivel_offset
                                                 + (uint32_t)i * g_nivel_passo));
            if (g_tem_time && g_nivel_passo) {
                /* src/pokemon.c, sSubstructOffsets[SUBSTRUCT_TYPE_0] */
                static const uint8_t sub0[24] = {0, 0, 0, 0, 0, 0, 1, 1, 2, 3,
                                                 2, 3, 1, 1, 2, 3, 2, 3, 1, 1,
                                                 2, 3, 2, 3};
                uint32_t mon0 = g_inimigo + g_nivel_offset - g_time_niv;
                for (int i = 0; i < 6; i++) {
                    uint32_t mon = mon0 + (uint32_t)i * g_nivel_passo;
                    uint32_t pers = core->busRead32(core, mon + g_time_pers);
                    uint32_t otid = core->busRead32(core, mon + g_time_otid);
                    uint32_t w = core->busRead32(core, mon + g_time_sec
                                                 + (uint32_t)sub0[pers % 24]
                                                   * g_time_sub);
                    w ^= otid;
                    w ^= pers;
                    printf(" especie%d=%d tera%d=%d item%d=%d",
                           i, (int)(w & 0x7FF), i, (int)((w >> 11) & 0x1F),
                           i, (int)((w >> 16) & 0x3FF));
                }
            }
            if (g_tem_hp && base_do_time()) {
                uint32_t mon0 = base_do_time();
                for (int i = 0; i < 6; i++) {
                    uint32_t mon = mon0 + (uint32_t)i * g_nivel_passo;
                    printf(" hp%d=%d hpmax%d=%d",
                           i, (int)core->busRead16(core, mon + g_hp_off),
                           i, (int)core->busRead16(core, mon + g_hpmax_off));
                }
            }
        }
        if (g_sb2ptr) {
            uint32_t sb2 = core->busRead32(core, g_sb2ptr);
            printf(" opcoes=%d", sb2 ? (int)core->busRead8(core, sb2 + g_opcoes_offset) : -1);
        }
        if (g_bmons) {
            uint32_t m = g_bmons + g_bmons_tam;  /* battler 1: oponente da esquerda */
            printf(" bespecie=%d bnivel=%d",
                   (int)core->busRead16(core, m + g_bmons_esp),
                   (int)core->busRead8(core, m + g_bmons_niv));
            for (int i = 0; i < 4; i++)
                printf(" bgolpe%d=%d", i,
                       (int)core->busRead16(core, m + g_bmons_gol + (uint32_t)i * 2));
        }
        if (g_bstruct) {
            uint32_t bs = core->busRead32(core, g_bstruct);
            printf(" gimmick=%d", bs ? (int)core->busRead16(core, bs + g_gimmick_offset) : -1);
        }
        for (int i = 0; i < g_n_itens; i++) {
            int quantos = 0;
            if (g_bolsa_n && g_sb2ptr) {
                uint32_t sb2 = core->busRead32(core, g_sb2ptr);
                uint16_t chave = sb2 ? (uint16_t)core->busRead32(core, sb2 + g_chave_off) : 0;
                for (uint32_t s = 0; s < g_bolsa_n; s++) {
                    uint32_t slot = base + g_bolsa_off + s * 4;
                    if ((int)core->busRead16(core, slot) != g_itens_pedidos[i])
                        continue;
                    quantos = (int)(uint16_t)(core->busRead16(core, slot + 2) ^ chave);
                    break;
                }
            } else {
                quantos = -1;   /* sem --bolsa: dito, nunca fingido como zero */
            }
            printf(" item_0x%X=%d", g_itens_pedidos[i], quantos);
        }
        for (int i = 0; i < g_n_flags; i++)
            printf(" flag_0x%X=%d", g_flags_pedidas[i], le_flag(core, g_flags_pedidas[i]));
        for (int i = 0; i < g_n_vars; i++)
            printf(" var_0x%X=%d", g_vars_pedidas[i], le_var(core, g_vars_pedidas[i]));
    }
    for (int i = 0; i < g_n_palobj; i++) {
        int achou = 0;
        for (uint32_t a = 0x05000200; a < 0x05000400 && !achou; a += 2)
            if (core->busRead16(core, a) == (uint16_t)g_palobj_pedidas[i]) achou = 1;
        printf(" palobj_0x%04X=%d", g_palobj_pedidas[i], achou);
    }
    printf("\n");
    fflush(stdout);
}

static int botao_para_chave(const char *nome) {
    /* NADA = roda os quadros sem apertar nada; serve para esperar transicao */
    if (!strcmp(nome, "NADA")) return -1;
    if (!strcmp(nome, "A")) return GBA_KEY_A;
    if (!strcmp(nome, "B")) return GBA_KEY_B;
    if (!strcmp(nome, "SELECT")) return GBA_KEY_SELECT;
    if (!strcmp(nome, "START")) return GBA_KEY_START;
    if (!strcmp(nome, "RIGHT")) return GBA_KEY_RIGHT;
    if (!strcmp(nome, "LEFT")) return GBA_KEY_LEFT;
    if (!strcmp(nome, "UP")) return GBA_KEY_UP;
    if (!strcmp(nome, "DOWN")) return GBA_KEY_DOWN;
    if (!strcmp(nome, "R")) return GBA_KEY_R;
    if (!strcmp(nome, "L")) return GBA_KEY_L;
    if (!strcmp(nome, "NONE")) return -1;
    fprintf(stderr, "botao desconhecido no roteiro: %s\n", nome);
    exit(1);
}

/* Converte "R+START" numa mascara de bits. Combinacao existe porque o menu de
   debug do pokeemerald-expansion abre com R segurado + START, e sem ela nao da
   para varrer o jogo inteiro sem recompilar a ROM para cada lugar. */
static uint32_t mascara_de_botoes(const char *nome) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%s", nome);
    uint32_t m = 0;
    for (char *p = strtok(buf, "+"); p; p = strtok(NULL, "+")) {
        int t = botao_para_chave(p);
        if (t >= 0) m |= (1u << t);
    }
    return m;
}

/* roda N quadros do core, segurando (ou nao) a tecla indicada */
static void roda_quadros_mascara(struct mCore *core, uint32_t mascara, int n, int segurar) {
    /* O jogo so reconhece um toque novo depois de ver o botao SOLTO por pelo
       menos um quadro. Segurar e soltar sem rodar quadro no meio faz o jogo
       enxergar um unico toque continuo, e o roteiro inteiro vira nada. Por isso
       aqui o botao fica pressionado por poucos quadros e solto pelo resto. */
    const int QUADROS_PRESSIONADO = 6;
    /* segurar = o botao fica apertado o passo inteiro. Necessario para combinacao
       tipo R+START do menu de debug, em que R precisa estar HELD quando START e
       NEW: soltar depois de 6 quadros faz o jogo nunca ver as duas condicoes. */
    int pressionado = segurar ? n
                     : (mascara && n > QUADROS_PRESSIONADO) ? QUADROS_PRESSIONADO : n;

    core->clearKeys(core, 0xFFFFFFFF);
    if (mascara) core->addKeys(core, mascara);
    for (int i = 0; i < pressionado; i++) core->runFrame(core);

    core->clearKeys(core, 0xFFFFFFFF);
    for (int i = pressionado; i < n; i++) core->runFrame(core);
}

/* compatibilidade: chamada antiga por tecla unica, -1 = nenhuma */
static void roda_quadros(struct mCore *core, int tecla, int n) {
    roda_quadros_mascara(core, tecla >= 0 ? (1u << tecla) : 0u, n, 0);
}

/* Salva um PNG por passo do roteiro, ao lado da saida final, com sufixo -NN.
   Sem isso o runner so mostra o quadro final: quando o roteiro erra, nao da para
   saber em QUAL passo errou, e cada tentativa custa um boot inteiro. */
static const uint32_t *g_framebuffer = NULL;
static unsigned g_largura = 0, g_altura = 0;
static const char *g_saida = NULL;
static void salva_png(const uint32_t *, int, int, const char *);

/* Cada passo do roteiro tambem despeja o ESTADO, nao so o PNG. Sem isto o
   runner so mostra o estado ANTES do roteiro e o do fim, e "o jogador andou"
   fica indemonstravel: a diferenca entre os dois inclui o warp. Com um dump por
   passo da para exigir duas posicoes distintas DENTRO do mapa final, que e a
   prova de que o jogo continua respondendo ao controle. */
static struct mCore *g_core = NULL;
static void dump_estado(struct mCore *core, const char *rotulo);

static void salva_passo(int indice) {
    if (g_dump_estado && g_core) {
        char rot[32];
        snprintf(rot, sizeof(rot), "passo%02d", indice);
        dump_estado(g_core, rot);
    }
    if (g_sem_png || !g_framebuffer || !g_saida) return;
    char caminho[1024];
    const char *ponto = strrchr(g_saida, '.');
    int base = ponto ? (int)(ponto - g_saida) : (int)strlen(g_saida);
    snprintf(caminho, sizeof(caminho), "%.*s-%02d.png", base, g_saida, indice);
    salva_png(g_framebuffer, g_largura, g_altura, caminho);
}

/* executa o roteiro completo, passo a passo */
static void executa_roteiro(struct mCore *core, char *roteiro) {
    if (!roteiro || !*roteiro) return;
    char *salvo = NULL;
    int indice = 0;
    char *passo = strtok_r(roteiro, ",", &salvo);
    while (passo) {
        int repeticoes = 1;
        char *asterisco = strchr(passo, '*');
        if (asterisco) {
            repeticoes = atoi(asterisco + 1);
            *asterisco = '\0';
        }
        char *dois_pontos = strchr(passo, ':');
        if (!dois_pontos) {
            fprintf(stderr, "passo invalido no roteiro: %s\n", passo);
            exit(1);
        }
        *dois_pontos = '\0';
        int quadros = atoi(passo);
        char *botoes = dois_pontos + 1;

        /* Passo que mexe na memoria em vez de apertar botao. Acender flag por
           escrita direta e o MESMO efeito de FlagSet (que so faz
           flags[id/8] |= 1<<(id%8)), e nao depende de descobrir navegacao de
           menu, que muda quando o menu de debug muda. */
        if (!strncmp(botoes, "FLAG=", 5)) {
            acende_flag(core, (int)strtol(botoes + 5, NULL, 0));
            roda_quadros_mascara(core, 0, quadros, 0);
            if (g_dump_estado) { char r[32]; snprintf(r, sizeof r, "passo%02d", indice + 1); dump_estado(core, r); }
            salva_passo(++indice);
            passo = strtok_r(NULL, ",", &salvo);
            continue;
        }
        if (!strncmp(botoes, "OPT=", 4)) {
            grava_opcoes(core, (int)strtol(botoes + 4, NULL, 0));
            roda_quadros_mascara(core, 0, quadros, 0);
            if (g_dump_estado) { char r[32]; snprintf(r, sizeof r, "passo%02d", indice + 1); dump_estado(core, r); }
            salva_passo(++indice);
            passo = strtok_r(NULL, ",", &salvo);
            continue;
        }
        /* "N:HP=slot=valor" grava HP direto no slot do time decifrado. Existe
           porque nao ha caminho de jogo que MACHUQUE o time de forma
           deterministica (batalha selvagem depende de sorteio), e sem um time
           machucado nao da para provar que uma cena de cura CUROU. */
        if (!strncmp(botoes, "HP=", 3)) {
            char *igual = strchr(botoes + 3, '=');
            if (!igual) { fprintf(stderr, "HP= precisa de slot=valor: %s\n", botoes); exit(1); }
            *igual = '\0';
            uint32_t mon0 = base_do_time();
            if (!mon0 || !g_tem_hp) {
                fprintf(stderr, "HP=: precisa de --inimigo, --timeinimigo e --hp\n");
                exit(1);
            }
            core->busWrite16(core,
                mon0 + (uint32_t)strtol(botoes + 3, NULL, 0) * g_nivel_passo + g_hp_off,
                (uint16_t)strtol(igual + 1, NULL, 0));
            roda_quadros_mascara(core, 0, quadros, 0);
            if (g_dump_estado) { char r[32]; snprintf(r, sizeof r, "passo%02d", indice + 1); dump_estado(core, r); }
            salva_passo(++indice);
            passo = strtok_r(NULL, ",", &salvo);
            continue;
        }
        if (!strncmp(botoes, "VAR=", 4)) {
            char *igual = strchr(botoes + 4, '=');
            if (!igual) { fprintf(stderr, "VAR= precisa de id=valor: %s\n", botoes); exit(1); }
            *igual = '\0';
            grava_var(core, (int)strtol(botoes + 4, NULL, 0), (int)strtol(igual + 1, NULL, 0));
            roda_quadros_mascara(core, 0, quadros, 0);
            if (g_dump_estado) { char r[32]; snprintf(r, sizeof r, "passo%02d", indice + 1); dump_estado(core, r); }
            salva_passo(++indice);
            passo = strtok_r(NULL, ",", &salvo);
            continue;
        }

        /* sufixo "!" = segura o botao o passo inteiro, ex.: "30:R+START!" */
        int segurar = 0;
        size_t tam = strlen(botoes);
        if (tam && botoes[tam - 1] == '!') { segurar = 1; botoes[tam - 1] = '\0'; }
        uint32_t mascara = mascara_de_botoes(botoes);
        for (int k = 0; k < repeticoes; k++)
            roda_quadros_mascara(core, mascara, quadros, segurar);
        if (g_dump_estado) { char r[32]; snprintf(r, sizeof r, "passo%02d", indice + 1); dump_estado(core, r); }
        salva_passo(++indice);
        passo = strtok_r(NULL, ",", &salvo);
    }
}

/* converte o framebuffer BGR8 (uint32, 0x00BBGGRR) do mgba e grava PNG RGB */
static void salva_png(const uint32_t *pixels, int largura, int altura, const char *caminho) {
    FILE *f = fopen(caminho, "wb");
    if (!f) { perror("fopen"); exit(1); }

    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    png_infop info = png_create_info_struct(png);
    png_init_io(png, f);
    png_set_IHDR(png, info, largura, altura, 8, PNG_COLOR_TYPE_RGB,
                 PNG_INTERLACE_NONE, PNG_COMPRESSION_TYPE_DEFAULT, PNG_FILTER_TYPE_DEFAULT);
    png_write_info(png, info);

    png_bytep linha = malloc(largura * 3);
    for (int y = 0; y < altura; y++) {
        for (int x = 0; x < largura; x++) {
            uint32_t px = pixels[y * largura + x];
            linha[x * 3 + 0] = px & 0xFF;         /* R */
            linha[x * 3 + 1] = (px >> 8) & 0xFF;  /* G */
            linha[x * 3 + 2] = (px >> 16) & 0xFF; /* B */
        }
        png_write_row(png, linha);
    }
    free(linha);
    png_write_end(png, NULL);
    png_destroy_write_struct(&png, &info);
    fclose(f);
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "uso: %s <rom.gba> <frames> <roteiro> <saida.png> [opcoes]\n"
                        "opcoes: --dump-estado --flag N --var N --sav arq.sav\n"
                        "        --sb1ptr 0xADDR --partycount 0xADDR --sem-png\n", argv[0]);
        return 1;
    }
    const char *caminho_rom = argv[1];
    int quadros_iniciais = atoi(argv[2]);
    char *roteiro = argv[3];
    const char *caminho_png = argv[4];
    const char *caminho_sav = NULL;

    for (int i = 5; i < argc; i++) {
        if (!strcmp(argv[i], "--dump-estado")) g_dump_estado = 1;
        else if (!strcmp(argv[i], "--sem-png")) g_sem_png = 1;
        else if (!strcmp(argv[i], "--flag") && i + 1 < argc) {
            if (g_n_flags < MAX_PEDIDOS) g_flags_pedidas[g_n_flags++] = (int)strtol(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--var") && i + 1 < argc) {
            if (g_n_vars < MAX_PEDIDOS) g_vars_pedidas[g_n_vars++] = (int)strtol(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--item") && i + 1 < argc) {
            if (g_n_itens < MAX_PEDIDOS) g_itens_pedidos[g_n_itens++] = (int)strtol(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--bolsa") && i + 1 < argc) {
            uint32_t v[3];
            if (!le_lista(argv[++i], v, 3)) {
                fprintf(stderr, "--bolsa precisa de offset,nslots,chave\n");
                return 1;
            }
            g_bolsa_off = v[0]; g_bolsa_n = v[1]; g_chave_off = v[2];
        } else if (!strcmp(argv[i], "--palobj") && i + 1 < argc) {
            if (g_n_palobj < MAX_PEDIDOS) g_palobj_pedidas[g_n_palobj++] = (int)strtol(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--sav") && i + 1 < argc) {
            caminho_sav = argv[++i];
        } else if (!strcmp(argv[i], "--sb1ptr") && i + 1 < argc) {
            g_sb1ptr = (uint32_t)strtoul(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--partycount") && i + 1 < argc) {
            g_partycount = (uint32_t)strtoul(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--oponente") && i + 1 < argc) {
            g_oponente = (uint32_t)strtoul(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--inimigo") && i + 1 < argc) {
            g_inimigo = (uint32_t)strtoul(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--nivel-offset") && i + 1 < argc) {
            g_nivel_offset = (uint32_t)strtoul(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--nivel-passo") && i + 1 < argc) {
            g_nivel_passo = (uint32_t)strtoul(argv[++i], NULL, 0);
        } else if (!strcmp(argv[i], "--timeinimigo") && i + 1 < argc) {
            uint32_t v[5];
            if (!le_lista(argv[++i], v, 5)) {
                fprintf(stderr, "--timeinimigo precisa de "
                                "pers,otid,secure,tamsubstruct,nivel\n");
                return 1;
            }
            g_time_pers = v[0]; g_time_otid = v[1]; g_time_sec = v[2];
            g_time_sub = v[3]; g_time_niv = v[4]; g_tem_time = 1;
        } else if (!strcmp(argv[i], "--hp") && i + 1 < argc) {
            uint32_t v[2];
            if (!le_lista(argv[++i], v, 2)) {
                fprintf(stderr, "--hp precisa de offset_hp,offset_maxhp\n");
                return 1;
            }
            g_hp_off = v[0]; g_hpmax_off = v[1]; g_tem_hp = 1;
        } else if (!strcmp(argv[i], "--opcoes") && i + 1 < argc) {
            uint32_t v[2];
            if (!le_lista(argv[++i], v, 2)) {
                fprintf(stderr, "--opcoes precisa de addr,offset\n");
                return 1;
            }
            g_sb2ptr = v[0]; g_opcoes_offset = v[1];
        } else if (!strcmp(argv[i], "--batalhamons") && i + 1 < argc) {
            uint32_t v[5];
            if (!le_lista(argv[++i], v, 5)) {
                fprintf(stderr, "--batalhamons precisa de addr,tam,esp,niv,gol\n");
                return 1;
            }
            g_bmons = v[0]; g_bmons_tam = v[1]; g_bmons_esp = v[2];
            g_bmons_niv = v[3]; g_bmons_gol = v[4];
        } else if (!strcmp(argv[i], "--gimmick") && i + 1 < argc) {
            uint32_t v[2];
            if (!le_lista(argv[++i], v, 2)) {
                fprintf(stderr, "--gimmick precisa de addr,offset\n");
                return 1;
            }
            g_bstruct = v[0]; g_gimmick_offset = v[1];
        } else if (!strcmp(argv[i], "--offsets") && i + 1 < argc) {
            /* loc,layout,party,flags,vars,nflags,nvars, medidos da fonte da build */
            uint32_t v[7];
            if (sscanf(argv[++i], "%u,%u,%u,%u,%u,%u,%u",
                       &v[0], &v[1], &v[2], &v[3], &v[4], &v[5], &v[6]) != 7) {
                fprintf(stderr, "--offsets precisa de 7 numeros: "
                                "loc,layout,party,flags,vars,nflags,nvars\n");
                return 1;
            }
            SB1_LOCATION = v[0]; SB1_MAPLAYOUTID = v[1]; SB1_PARTYCOUNT = v[2];
            SB1_FLAGS = v[3]; SB1_VARS = v[4];
            FLAGS_COUNT = (int)v[5]; VARS_COUNT = (int)v[6];
        } else {
            fprintf(stderr, "opcao desconhecida: %s\n", argv[i]);
            return 1;
        }
    }

    struct mCore *core = mCoreFind(caminho_rom);
    if (!core) { fprintf(stderr, "mCoreFind falhou para %s\n", caminho_rom); return 1; }
    if (!core->init(core)) { fprintf(stderr, "core->init falhou\n"); return 1; }

    /* inicializa e aplica a config padrao interna do core (sem tocar arquivo do usuario) */
    mCoreInitConfig(core, "gba_runner");
    core->loadConfig(core, &core->config);

    unsigned largura, altura;
    core->desiredVideoDimensions(core, &largura, &altura);
    uint32_t *framebuffer = malloc(largura * altura * sizeof(uint32_t));
    core->setVideoBuffer(core, (color_t *)framebuffer, largura);

    g_framebuffer = framebuffer;
    g_largura = largura;
    g_altura = altura;
    g_saida = caminho_png;

    if (!mCoreLoadFile(core, caminho_rom)) { fprintf(stderr, "mCoreLoadFile falhou\n"); return 1; }

    /* Flash persistida em arquivo: sem isso a save do jogo morre com o processo
       e nao da para provar que uma .sav antiga continua valendo numa ROM nova
       (teste T11). O arquivo e criado se nao existir; se existir, o jogo enxerga
       "Continuar" na tela de titulo. */
    if (caminho_sav) {
        struct VFile *vf = VFileOpen(caminho_sav, O_CREAT | O_RDWR);
        if (!vf) { fprintf(stderr, "nao consegui abrir sav: %s\n", caminho_sav); return 1; }
        if (!core->loadSave(core, vf)) { fprintf(stderr, "loadSave falhou\n"); return 1; }
    }

    core->reset(core);

    g_core = core;
    roda_quadros(core, -1, quadros_iniciais);
    if (g_dump_estado) dump_estado(core, "passo00");
    executa_roteiro(core, roteiro);
    if (g_dump_estado) dump_estado(core, "final");

    if (!g_sem_png) salva_png(framebuffer, largura, altura, caminho_png);

    /* deinit descarrega a ROM, e e isso que faz o mgba despejar a flash no
       arquivo. Sem chamar, a .sav sai vazia. */
    core->deinit(core);
    free(framebuffer);
    return 0;
}
