#include "global.h"
#include "event_data.h"
#include "field_move.h"
#include "fldeff.h"
#include "fldeff_misc.h"
#include "party_menu.h"
#include "constants/field_move.h"
#include "constants/moves.h"
#include "constants/party_menu.h"
#include "insignias.h"

// TRAVA DE MEDALHA DOS GOLPES DE CAMPO: VALE A MEDALHA EQUIVALENTE DE QUALQUER
// REGIÃO (fila de bugs 3, 30/09/2026).
//
// O que estava errado, medido e não suposto: `IS_FRLG` é constante de compilação
// e vale 0 nesta ROM, então os ramos FRLG daqui eram código morto e as oito
// travas pediam as FLAG_BADGE01..08_GET na ORDEM DO EMERALD. Só que essas oito
// flags, no hack, são as insígnias de KANTO (os ginásios _Frlg as acendem), e os
// ginásios de Johto, Hoenn e Sinnoh acendem só FLAG_INSIGNIA_*, que nenhuma trava
// lia. Resultado no jogo: o Fly em Cerulean pedia a insígnia da Sabrina (6ª) em
// vez da Thunder (3ª, a do FRLG), o Cut pedia a Boulder em vez da Cascade, e
// quem jogava Johto, Hoenn ou Sinnoh nunca destravava golpe de campo nenhum.
//
// Agora cada golpe destrava com a insígnia que o destrava no jogo ORIGINAL de
// cada região, e basta UMA delas (mesma lógica da obediência decidida pelo Gui
// em 30/09/2026: vale insígnia de qualquer região). Fontes das tabelas:
//   Kanto  (FRLG):     os ramos IS_FRLG que estavam aqui, iguais ao pokefirered.
//   Hoenn  (Emerald):  os ramos Emerald que estavam aqui, só que lidos nas
//                      FLAG_INSIGNIA_HOENN_1..8 (as oito originais; as 9..16 do
//                      Hoenn EX não destravam golpe).
//   Johto  (HGSS):     Zephyr Rock Smash, Hive Cut, Plain Strength, Fog Surf,
//                      Storm Fly, Rising Waterfall (o Heart and Soul em
//                      fontes-mapas/hns confere todos menos o Fly, que ele moveu
//                      para a 5ª; aqui fica a Storm, 6ª, a do HGSS).
//   Sinnoh (Platinum): pokeplatinum/src/field_move_tasks.c: Coal Rock Smash,
//                      Forest Cut, Cobble Fly, Fen Surf, Mine Strength, Beacon
//                      Waterfall.
// Onde o jogo original não tem o golpe ou não pede insígnia, a escolha é nossa e
// fica escrita: Flash é a 1ª em Johto (Zephyr, a do GSC) e em Sinnoh (no
// Platinum ele é TM livre); Dive é a 7ª em toda região (a do Emerald; em Kanto
// já era assim antes, e o T272.8 mergulha na Route 41 com as insígnias de Kanto).
//
// Custo de save ZERO: só LÊ flags que já existem.
// As regiões e as flags de cada insígnia vêm de src/insignias.c, a mesma tabela
// que a obediência, a penalidade de captura e o cartão do treinador usam
// (unificado no fechamento da fila de bugs 3, 01/10/2026).
// Número da insígnia (1 a 8) que destrava o golpe em cada região; 0 é "esta
// região não destrava".
static const u8 sInsigniaDoGolpe[][REGIAO_INSIGNIA_COUNT] =
{
    //                         Kanto Johto Hoenn Sinnoh
    [FIELD_MOVE_CUT]        = { 2,    2,    1,    2 },
    [FIELD_MOVE_FLASH]      = { 1,    1,    2,    1 },
    [FIELD_MOVE_ROCK_SMASH] = { 6,    1,    3,    1 },
    [FIELD_MOVE_STRENGTH]   = { 4,    3,    4,    6 },
    [FIELD_MOVE_SURF]       = { 5,    4,    5,    4 },
    [FIELD_MOVE_FLY]        = { 3,    6,    6,    3 },
    [FIELD_MOVE_DIVE]       = { 7,    7,    7,    7 },
    [FIELD_MOVE_WATERFALL]  = { 7,    8,    8,    8 },
};

bool32 FieldMove_TemInsigniaQueDestrava(enum FieldMove fieldMove)
{
    u32 regiao;

    if (fieldMove >= ARRAY_COUNT(sInsigniaDoGolpe))
        return TRUE;
    for (regiao = 0; regiao < REGIAO_INSIGNIA_COUNT; regiao++)
    {
        u32 numero = sInsigniaDoGolpe[fieldMove][regiao];

        if (numero != 0 && FlagGet(FlagDaInsignia(regiao, numero - 1)))
            return TRUE;
    }
    return FALSE;
}

static bool32 IsFieldMoveUnlocked_Cut(void)
{
    return FieldMove_TemInsigniaQueDestrava(FIELD_MOVE_CUT);
}

static bool32 IsFieldMoveUnlocked_Flash(void)
{
    return FieldMove_TemInsigniaQueDestrava(FIELD_MOVE_FLASH);
}

static bool32 IsFieldMoveUnlocked_RockSmash(void)
{
    return FieldMove_TemInsigniaQueDestrava(FIELD_MOVE_ROCK_SMASH);
}

static bool32 IsFieldMoveUnlocked_Strength(void)
{
    return FieldMove_TemInsigniaQueDestrava(FIELD_MOVE_STRENGTH);
}

static bool32 IsFieldMoveUnlocked_Surf(void)
{
    return FieldMove_TemInsigniaQueDestrava(FIELD_MOVE_SURF);
}

static bool32 IsFieldMoveUnlocked_Fly(void)
{
    return FieldMove_TemInsigniaQueDestrava(FIELD_MOVE_FLY);
}

static bool32 IsFieldMoveUnlocked_Dive(void)
{
    return FieldMove_TemInsigniaQueDestrava(FIELD_MOVE_DIVE);
}

static bool32 IsFieldMoveUnlocked_Waterfall(void)
{
    return FieldMove_TemInsigniaQueDestrava(FIELD_MOVE_WATERFALL);
}

static bool32 IsFieldMoveUnlocked_RockClimb(void)
{
    return OW_ROCK_CLIMB_FIELD_MOVE;
}

static bool32 IsFieldMoveUnlocked_Teleport(void)
{
    return TRUE;
}

static bool32 IsFieldMoveUnlocked_Dig(void)
{
    return TRUE;
}

static bool32 IsFieldMoveUnlocked_SecretPower(void)
{
    return TRUE;
}

static bool32 IsFieldMoveUnlocked_MilkDrink(void)
{
    return TRUE;
}

static bool32 IsFieldMoveUnlocked_SoftBoiled(void)
{
    return TRUE;
}

static bool32 IsFieldMoveUnlocked_SweetScent(void)
{
    return TRUE;
}

static bool32 IsFieldMoveUnlocked_Defog(void)
{
    return OW_DEFOG_FIELD_MOVE;
}

const struct FieldMoveInfo gFieldMoveInfo[FIELD_MOVES_COUNT] =
{
    [FIELD_MOVE_CUT] =
    {
        .fieldMoveFunc = SetUpFieldMove_Cut,
        .isUnlockedFunc = IsFieldMoveUnlocked_Cut,
        .moveID = MOVE_CUT,
        .partyMsgID = PARTY_MSG_NOTHING_TO_CUT,
    },

    [FIELD_MOVE_FLASH] =
    {
        .fieldMoveFunc = SetUpFieldMove_Flash,
        .isUnlockedFunc = IsFieldMoveUnlocked_Flash,
        .moveID = MOVE_FLASH,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },

    [FIELD_MOVE_ROCK_SMASH] =
    {
        .fieldMoveFunc = SetUpFieldMove_RockSmash,
        .isUnlockedFunc = IsFieldMoveUnlocked_RockSmash,
        .moveID = MOVE_ROCK_SMASH,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },

    [FIELD_MOVE_STRENGTH] =
    {
        .fieldMoveFunc = SetUpFieldMove_Strength,
        .isUnlockedFunc = IsFieldMoveUnlocked_Strength,
        .moveID = MOVE_STRENGTH,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },

    [FIELD_MOVE_SURF] =
    {
        .fieldMoveFunc = SetUpFieldMove_Surf,
        .isUnlockedFunc = IsFieldMoveUnlocked_Surf,
        .moveID = MOVE_SURF,
        .partyMsgID = PARTY_MSG_CANT_SURF_HERE,
    },

    [FIELD_MOVE_FLY] =
    {
        .fieldMoveFunc = SetUpFieldMove_Fly,
        .isUnlockedFunc = IsFieldMoveUnlocked_Fly,
        .moveID = MOVE_FLY,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },

    [FIELD_MOVE_DIVE] =
    {
        .fieldMoveFunc = SetUpFieldMove_Dive,
        .isUnlockedFunc = IsFieldMoveUnlocked_Dive,
        .moveID = MOVE_DIVE,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },

    [FIELD_MOVE_WATERFALL] =
    {
        .fieldMoveFunc = SetUpFieldMove_Waterfall,
        .isUnlockedFunc = IsFieldMoveUnlocked_Waterfall,
        .moveID = MOVE_WATERFALL,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },

    [FIELD_MOVE_TELEPORT] =
    {
        .fieldMoveFunc = SetUpFieldMove_Teleport,
        .isUnlockedFunc = IsFieldMoveUnlocked_Teleport,
        .moveID = MOVE_TELEPORT,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },

    [FIELD_MOVE_DIG] =
    {
        .fieldMoveFunc = SetUpFieldMove_Dig,
        .isUnlockedFunc = IsFieldMoveUnlocked_Dig,
        .moveID = MOVE_DIG,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },

    [FIELD_MOVE_SECRET_POWER] =
    {
        .fieldMoveFunc = SetUpFieldMove_SecretPower,
        .isUnlockedFunc = IsFieldMoveUnlocked_SecretPower,
        .moveID = MOVE_SECRET_POWER,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },

    [FIELD_MOVE_MILK_DRINK] =
    {
        .fieldMoveFunc = SetUpFieldMove_SoftBoiled,
        .isUnlockedFunc = IsFieldMoveUnlocked_MilkDrink,
        .moveID = MOVE_MILK_DRINK,
        .partyMsgID = PARTY_MSG_NOT_ENOUGH_HP,
    },

    [FIELD_MOVE_SOFT_BOILED] =
    {
        .fieldMoveFunc = SetUpFieldMove_SoftBoiled,
        .isUnlockedFunc = IsFieldMoveUnlocked_SoftBoiled,
        .moveID = MOVE_SOFT_BOILED,
        .partyMsgID = PARTY_MSG_NOT_ENOUGH_HP,
    },

    [FIELD_MOVE_SWEET_SCENT] =
    {
        .fieldMoveFunc = SetUpFieldMove_SweetScent,
        .isUnlockedFunc = IsFieldMoveUnlocked_SweetScent,
        .moveID = MOVE_SWEET_SCENT,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },
    [FIELD_MOVE_ROCK_CLIMB] =
    {
        .fieldMoveFunc = SetUpFieldMove_RockClimb,
        .isUnlockedFunc = IsFieldMoveUnlocked_RockClimb,
        .moveID = MOVE_ROCK_CLIMB,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },
    [FIELD_MOVE_DEFOG] =
    {
        .fieldMoveFunc = SetUpFieldMove_Defog,
        .isUnlockedFunc = IsFieldMoveUnlocked_Defog,
        .moveID = MOVE_DEFOG,
        .partyMsgID = PARTY_MSG_CANT_USE_HERE,
    },
};
