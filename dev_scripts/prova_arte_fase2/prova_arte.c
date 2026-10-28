// SÓ PARA A ROM DE PROVA da arte da fase 2 (dev_scripts/prova_arte_fase2.sh).
// Nunca entra na ROM de verdade: o script copia este arquivo para src/, troca o callback
// inicial em main.c, builda, captura e desfaz tudo.
//
// Cinco cenas, oito retratos novos (TRAINER_PIC_*) cada, sobre o fundo de batalha GALAR_FIELD:
//   0 Kalos, 1 Alola, 2 Paldea, 3 extras (Sinnoh, Unova, Galar, Hisui), 4 os cinco retratos retocados à mão.
// Os retratos usam os slots de OBJ 8 a 15, um por retrato (cada retrato tem paleta própria de 16 cores).
// Apertar A passa para a cena seguinte.
#include "global.h"
#include "bg.h"
#include "battle_environment.h"
#include "constants/battle.h"
#include "constants/trainers.h"
#include "decompress.h"
#include "gba/types.h"
#include "gpu_regs.h"
#include "constants/rgb.h"
#include "main.h"
#include "malloc.h"
#include "palette.h"
#include "scanline_effect.h"
#include "sprite.h"
#include "task.h"
#include "trainer_pokemon_sprites.h"

#define NCENAS 5
static u8 sCena;

static const u16 sRetratos[NCENAS][8] =
{
    { TRAINER_PIC_KALOS_DIANTHA, TRAINER_PIC_KALOS_SERENA, TRAINER_PIC_KALOS_CALEM, TRAINER_PIC_KALOS_LYSANDRE,
      TRAINER_PIC_KALOS_CLEMONT, TRAINER_PIC_KALOS_VIOLA, TRAINER_PIC_KALOS_KORRINA, TRAINER_PIC_KALOS_SYCAMORE },
    { TRAINER_PIC_ALOLA_HAU, TRAINER_PIC_ALOLA_LILLIE, TRAINER_PIC_ALOLA_GLADION, TRAINER_PIC_ALOLA_KUKUI,
      TRAINER_PIC_ALOLA_ACEROLA, TRAINER_PIC_ALOLA_MALLOW, TRAINER_PIC_ALOLA_GUZMA, TRAINER_PIC_ALOLA_LUSAMINE },
    { TRAINER_PIC_PALDEA_NEMONA_V, TRAINER_PIC_PALDEA_ARVEN_V, TRAINER_PIC_PALDEA_PENNY, TRAINER_PIC_PALDEA_KIERAN,
      TRAINER_PIC_PALDEA_IONO, TRAINER_PIC_PALDEA_GEETA, TRAINER_PIC_PALDEA_CARMINE, TRAINER_PIC_PALDEA_RYME },
    { TRAINER_PIC_SINNOH_CYNTHIA, TRAINER_PIC_UNOVA_HILBERT, TRAINER_PIC_UNOVA_JUNIPER, TRAINER_PIC_GALAR_MAGNOLIA,
      TRAINER_PIC_GALAR_SONIA, TRAINER_PIC_GALAR_SORDWARD, TRAINER_PIC_HISUI_KAMADO, TRAINER_PIC_UNOVA_LENORA },
    { TRAINER_PIC_KALOS_SCIENTISTF, TRAINER_PIC_KALOS_TRIATHLETESWIMMER, TRAINER_PIC_PALDEA_KIERAN_FESTIVAL,
      TRAINER_PIC_PALDEA_PENNY, TRAINER_PIC_GALAR_POKEMONBREEDER, TRAINER_PIC_KALOS_SCIENTIST,
      TRAINER_PIC_KALOS_SWIMMER, TRAINER_PIC_PALDEA_KIERAN },
};

static void VBlankCB_Prova(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static const struct BgTemplate sBgProva[] =
{
    { .bg = 3, .charBaseIndex = 2, .mapBaseIndex = 26, .screenSize = 1, .paletteMode = 0, .priority = 3, .baseTile = 0 },
};

static void CarregaFundo(enum BattleEnvironments env)
{
    DecompressDataWithHeaderVram(gBattleEnvironmentInfo[env].background.tileset, (void *)(BG_CHAR_ADDR(2)));
    DecompressDataWithHeaderVram(gBattleEnvironmentInfo[env].background.tilemap, (void *)(BG_SCREEN_ADDR(26)));
    LoadPalette(gBattleEnvironmentInfo[env].palette, BG_PLTT_ID(2), 3 * PLTT_SIZE_4BPP);
}

static void MontaCena(void)
{
    u32 i;

    SetVBlankCallback(NULL);
    DmaFill16(3, 0, VRAM, VRAM_SIZE);
    DmaFill32(3, 0, OAM, OAM_SIZE);
    DmaFill16(3, 0, PLTT, PLTT_SIZE);
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetAllPicSprites();
    ResetPaletteFade();
    ResetTasks();
    ScanlineEffect_Stop();
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgProva, ARRAY_COUNT(sBgProva));

    CarregaFundo(BATTLE_ENVIRONMENT_GALAR_FIELD);
    ShowBg(3);
    for (i = 0; i < 8; i++)
        CreateTrainerPicSprite(sRetratos[sCena][i], TRUE, 34 + (i % 4) * 60, 40 + (i / 4) * 66, 8 + i, TAG_NONE);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_BG3_ON | DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    SetVBlankCallback(VBlankCB_Prova);
}

static void CB2_Prova(void)
{
    if (gMain.newKeys & A_BUTTON)
    {
        sCena = (sCena + 1) % NCENAS;
        MontaCena();
    }
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

void CB2_ProvaArte(void)
{
    sCena = 0;
    MontaCena();
    SetMainCallback2(CB2_Prova);
}
