// Laboratório do Oak com 52 iniciais (pedido do Gui, 28/10/2026).
//
// O jogo começa em Pallet Town, e no laboratório do Oak a escolha deixou de ser
// entre três: são mesinhas de três Poké Balls com os iniciais das nove gerações
// (27) e mais 25 espécies, 52 bolas no total. O jogador continua levando UMA, no
// nível 5, como no FireRed.
//
// Como foi feito, e por quê:
//
//   - As três bolas de Kanto (8,4), (9,4) e (10,4) continuam OBJETOS, nas mesmas
//     posições, com o roteiro do FireRed intacto (rival, batalha de saída, times
//     do rival no resto do jogo por VAR_STARTER_MON).
//   - As outras 49 não podem ser objeto: a janela de objetos tem 16 vagas
//     (OBJECT_EVENTS_COUNT, include/constants/global.h, e ela mora dentro da
//     save). Cada uma é um metatile "mesa com Poké Ball" com um bg_event em cima.
//     Ao escolher, o metatile vira o tampo vazio e o índice vai para
//     VAR_LAB_INICIAL_ESCOLHIDO, que o MAP_SCRIPT_ON_LOAD relê para redesenhar a
//     mesa vazia sempre que o mapa carrega.
//   - O rival leva o inicial de Kanto que leva vantagem sobre o escolhido, pela
//     tabela de tipos do motor (LabIniciais_RivalPorTipo, regra documentada lá).
//     O resultado é o mesmo 0/1/2 de VAR_STARTER_MON do FireRed, e o rival anda
//     até a bola de Kanto correspondente com os movimentos que já existiam.
//
// ESTA TABELA É O ÚNICO PONTO DE DADO das 49 bolas novas: posição e espécie. O
// mapa (map.bin e os bg_events do map.json) é DERIVADO dela por
// dev_scripts/lab_iniciais.py, que também confere as duas coisas. Para trocar uma
// espécie, troque a linha aqui e recompile; para mover uma bola, troque aqui e
// rode o gerador.
#include "global.h"
#include "battle_util.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "lab_iniciais.h"
#include "pokemon.h"
#include "constants/species.h"
#include "constants/vars.h"

// Metatiles do tampo da mesa do laboratório (gTileset_Lab_Frlg). Os três
// primeiros são o tampo da mesa de Kanto, sem nada em cima. Os três últimos são
// o mesmo tampo com a Poké Ball desenhada: os pixels do sprite
// OBJ_EVENT_GFX_ITEM_BALL (graphics/object_events/pics/misc/ball_poke.png, na
// paleta npc_3) por cima do tampo, montados por dev_scripts/lab_iniciais.py.
#define METATILE_MESA_ESQ           0x2A8
#define METATILE_MESA_MEIO          0x2A9
#define METATILE_MESA_DIR           0x2AA
#define METATILE_MESA_BOLA_ESQ      0x32F
#define METATILE_MESA_BOLA_MEIO     0x330
#define METATILE_MESA_BOLA_DIR      0x331

struct BolaDoLab
{
    u8 x;
    u8 y;
    u16 especie;
};

// Posições em coordenada de mapa (sem MAP_OFFSET). Cada mesa tem três células
// de tampo, (x, y), (x+1, y) e (x+2, y); o jogador alcança a bola pela fileira
// de baixo (os pés da mesa, andáveis), pelos corredores entre as mesas ou pela
// fileira de cima.
static const struct BolaDoLab sBolasDoLab[] =
{
    // Fileira 1 (y = 4, na altura da mesa de Kanto): gerações 2 a 5.
    { 15,  4, SPECIES_CHIKORITA },
    { 16,  4, SPECIES_CYNDAQUIL },
    { 17,  4, SPECIES_TOTODILE },
    { 19,  4, SPECIES_TREECKO },
    { 20,  4, SPECIES_TORCHIC },
    { 21,  4, SPECIES_MUDKIP },
    { 23,  4, SPECIES_TURTWIG },
    { 24,  4, SPECIES_CHIMCHAR },
    { 25,  4, SPECIES_PIPLUP },
    { 27,  4, SPECIES_SNIVY },
    { 28,  4, SPECIES_TEPIG },
    { 29,  4, SPECIES_OSHAWOTT },
    // Fileira 2 (y = 7): gerações 6 a 9.
    { 15,  7, SPECIES_CHESPIN },
    { 16,  7, SPECIES_FENNEKIN },
    { 17,  7, SPECIES_FROAKIE },
    { 19,  7, SPECIES_ROWLET },
    { 20,  7, SPECIES_LITTEN },
    { 21,  7, SPECIES_POPPLIO },
    { 23,  7, SPECIES_GROOKEY },
    { 24,  7, SPECIES_SCORBUNNY },
    { 25,  7, SPECIES_SOBBLE },
    { 27,  7, SPECIES_SPRIGATITO },
    { 28,  7, SPECIES_FUECOCO },
    { 29,  7, SPECIES_QUAXLY },
    // Fileira 3 (y = 10): as outras espécies, na ordem do pedido.
    { 15, 10, SPECIES_DRATINI },
    { 16, 10, SPECIES_LARVITAR },
    { 17, 10, SPECIES_BELDUM },
    { 19, 10, SPECIES_GIBLE },
    { 20, 10, SPECIES_HONEDGE },
    { 21, 10, SPECIES_PORYGON },
    { 23, 10, SPECIES_TOGEPI },
    { 24, 10, SPECIES_GASTLY },
    { 25, 10, SPECIES_ABRA },
    { 27, 10, SPECIES_SMOOCHUM },
    { 28, 10, SPECIES_ELEKID },
    { 29, 10, SPECIES_MAGBY },
    // Fileira 4 (y = 13). Ralts, Riolu, Axew e Eevee são a resposta do Gui à
    // vaga "Ares" (28/10/2026); o Sandshrew de Alola ("AloLon Centro") também
    // foi confirmado por ele.
    { 15, 13, SPECIES_MUNCHLAX },
    { 16, 13, SPECIES_RALTS },
    { 17, 13, SPECIES_RIOLU },
    { 19, 13, SPECIES_AXEW },
    { 20, 13, SPECIES_EEVEE },
    { 21, 13, SPECIES_PONYTA },
    { 23, 13, SPECIES_DODUO },
    { 24, 13, SPECIES_BAGON },
    { 25, 13, SPECIES_VULPIX_ALOLA },
    { 27, 13, SPECIES_SANDSHREW_ALOLA },
    { 28, 13, SPECIES_GROWLITHE },
    { 29, 13, SPECIES_PIKACHU },
    // Fileira 5 (y = 16): a mesa do meio, sozinha, com a 52ª bola
    // (52 = 17 mesas de 3 + 1).
    { 22, 16, SPECIES_DEINO },
};

#define NUM_BOLAS_DO_LAB ARRAY_COUNT(sBolasDoLab)

// O registro de teste abaixo tem 64 bits; a var guarda índice + 1.
STATIC_ASSERT(NUM_BOLAS_DO_LAB == 49, LabIniciaisQuarentaENoveBolas);

// Só para teste (T364): um bit por bola que já RESPONDEU ao A do jogador nesta
// sessão. Não vai para a save. É como a suíte prova, num único passeio pelo
// laboratório, que as 49 bolas novas respondem.
EWRAM_DATA u16 gLabIniciaisBolasTocadas[4] = {0};

static s32 IndiceDaBolaEm(s32 x, s32 y)
{
    u32 i;

    for (i = 0; i < NUM_BOLAS_DO_LAB; i++)
    {
        if (sBolasDoLab[i].x == x && sBolasDoLab[i].y == y)
            return i;
    }
    return -1;
}

// Multiplicador do tipo `tipo` atacando `alvo`, pela tabela do motor
// (GetTypeModifier, src/battle_util.c), com os dois tipos do alvo.
static uq4_12_t MultiplicadorContra(enum Type tipo, u32 alvo)
{
    enum Type t0 = GetSpeciesType(alvo, 0);
    enum Type t1 = GetSpeciesType(alvo, 1);
    uq4_12_t mult = GetTypeModifier(tipo, t0);

    if (t1 != t0)
        mult = uq4_12_multiply(mult, GetTypeModifier(tipo, t1));
    return mult;
}

// O melhor dos tipos de `atacante` contra `alvo`.
static uq4_12_t MelhorAtaque(u32 atacante, u32 alvo)
{
    uq4_12_t a = MultiplicadorContra(GetSpeciesType(atacante, 0), alvo);
    uq4_12_t b = MultiplicadorContra(GetSpeciesType(atacante, 1), alvo);

    return a > b ? a : b;
}

// Qual inicial de Kanto o rival leva, como o valor de VAR_STARTER_MON do FireRed:
// 0 = rival com CHARMANDER, 1 = rival com BULBASAUR, 2 = rival com SQUIRTLE (é o
// que o resto do jogo lê para montar o time dele).
//
// Regra, aplicada em ordem, cada passo só desempata o anterior:
//   1. ELEMENTO: o tipo principal do inicial de Kanto (Fire, Grass, Water, o
//      triângulo) contra os dois tipos do escolhido. Maior vence. É o passo que
//      faz o Sprigatito (Grass) dar CHARMANDER ao rival, como no FireRed.
//   2. ATAQUE: o melhor dos tipos do inicial de Kanto (o Poison do Bulbasaur
//      conta aqui) contra o escolhido. Maior vence. O Dratini (Dragon) resiste aos
//      três elementos por igual, e o Poison neutro faz o rival levar BULBASAUR.
//   3. DEFESA: o melhor dos tipos do escolhido contra o inicial de Kanto. Menor
//      vence (o rival prefere quem apanha menos).
//   4. ORDEM FIXA: CHARMANDER, BULBASAUR, SQUIRTLE (o próprio 0, 1, 2).
// E nunca o mesmo que o jogador levou: se o escolhido for um dos três de Kanto,
// ele sai da disputa. Para os três de Kanto a regra devolve exatamente o
// mapeamento do FireRed (BULBASAUR 0, SQUIRTLE 1, CHARMANDER 2).
u32 LabIniciais_RivalPorTipo(u32 especie)
{
    static const u16 sDoRival[3] = { SPECIES_CHARMANDER, SPECIES_BULBASAUR, SPECIES_SQUIRTLE };
    s32 melhor = -1;
    uq4_12_t melhorElemento = 0, melhorAtaque = 0, melhorDefesa = 0;
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sDoRival); i++)
    {
        uq4_12_t elemento, ataque, defesa;

        if (sDoRival[i] == especie)
            continue;
        elemento = MultiplicadorContra(GetSpeciesType(sDoRival[i], 0), especie);
        ataque = MelhorAtaque(sDoRival[i], especie);
        defesa = MelhorAtaque(especie, sDoRival[i]);
        if (melhor < 0
         || elemento > melhorElemento
         || (elemento == melhorElemento && ataque > melhorAtaque)
         || (elemento == melhorElemento && ataque == melhorAtaque && defesa < melhorDefesa))
        {
            melhor = i;
            melhorElemento = elemento;
            melhorAtaque = ataque;
            melhorDefesa = defesa;
        }
    }
    return melhor;
}

static void EsvaziaMesaDaBola(u32 i)
{
    s32 x = sBolasDoLab[i].x + MAP_OFFSET;
    s32 y = sBolasDoLab[i].y + MAP_OFFSET;
    u32 vazio;

    switch (MapGridGetMetatileIdAt(x, y))
    {
    case METATILE_MESA_BOLA_ESQ:
        vazio = METATILE_MESA_ESQ;
        break;
    case METATILE_MESA_BOLA_MEIO:
        vazio = METATILE_MESA_MEIO;
        break;
    case METATILE_MESA_BOLA_DIR:
        vazio = METATILE_MESA_DIR;
        break;
    default:
        return; // já vazia, ou a célula não é tampo de mesa: nada a fazer
    }
    MapGridSetMetatileIdAt(x, y, vazio | PACK_COLLISION(MapGridGetCollisionAt(x, y)));
}

// special, chamado pelo bg_event de cada bola nova. Olha a célula em frente ao
// jogador e responde em VAR_RESULT:
//   0 = não há bola ali (a mesa da bola que o jogador já levou);
//   1 = bola: VAR_TEMP_1 recebe o 0/1/2 do rival, VAR_TEMP_2 a espécie, e
//       VAR_0x8004 o índice, que LabIniciais_EsvaziaMesa usa.
void LabIniciais_BolaDaFrente(void)
{
    s16 x, y;
    s32 i;

    gSpecialVar_Result = 0;
    GetXYCoordsOneStepInFrontOfPlayer(&x, &y);
    i = IndiceDaBolaEm(x - MAP_OFFSET, y - MAP_OFFSET);
    if (i < 0 || VarGet(VAR_LAB_INICIAL_ESCOLHIDO) == i + 1)
        return;

    gLabIniciaisBolasTocadas[i / 16] |= 1 << (i % 16);
    gSpecialVar_0x8004 = i;
    VarSet(VAR_TEMP_1, LabIniciais_RivalPorTipo(sBolasDoLab[i].especie));
    VarSet(VAR_TEMP_2, sBolasDoLab[i].especie);
    gSpecialVar_Result = 1;
}

// special, depois do "sim": grava a escolha na save e troca o tampo para o vazio.
// O script chama DrawWholeMapView em seguida.
void LabIniciais_EsvaziaMesa(void)
{
    u32 i = gSpecialVar_0x8004;

    if (i >= NUM_BOLAS_DO_LAB)
        return;
    VarSet(VAR_LAB_INICIAL_ESCOLHIDO, i + 1);
    EsvaziaMesaDaBola(i);
}

// special do MAP_SCRIPT_ON_LOAD do laboratório.
//
// Primeiro, devolve ao mapa qualquer célula que tenha chegado INDEFINIDA. Isso só
// acontece num caso: a save foi gravada DENTRO do laboratório numa ROM anterior a
// esta, em que ele media 13x14. Ao continuar, LoadSavedMapView (src/fieldmap.c)
// cola por cima do mapa a vista 15x14 guardada na save, e as células que caíam
// FORA do laboratório velho chegam como MAPGRID_UNDEFINED, que o jogo trata como
// borda: um muro preto onde agora é a ala nova, até o jogador sair e voltar. Em
// warp normal não há célula indefinida e o laço não toca em nada.
//
// Depois, esvazia a mesa da bola que o jogador levou, se foi uma das 49.
void LabIniciais_AoCarregar(void)
{
    const struct MapLayout *layout = gMapHeader.mapLayout;
    s32 x, y;
    u32 escolhida = VarGet(VAR_LAB_INICIAL_ESCOLHIDO);

    for (y = 0; y < layout->height; y++)
    {
        for (x = 0; x < layout->width; x++)
        {
            u16 *celula = &gBackupMapLayout.map[(x + MAP_OFFSET) + (y + MAP_OFFSET) * gBackupMapLayout.width];

            if (UNPACK_METATILE(*celula) == MAPGRID_UNDEFINED)
                *celula = layout->map[x + y * layout->width];
        }
    }

    if (escolhida >= 1 && escolhida <= NUM_BOLAS_DO_LAB)
        EsvaziaMesaDaBola(escolhida - 1);
}
