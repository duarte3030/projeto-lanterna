// SÓ PARA A ROM DE PROVA da arte da fase 1 (dev_scripts/prova_arte_fase1.sh).
// Nunca entra na ROM de verdade: o script copia este arquivo para src/, troca o callback
// inicial em main.c, builda, captura e desfaz tudo.
//
// Cena 0: três retratos novos (TRAINER_PIC_*) em cima e três NPCs novos (OBJ_EVENT_GFX_*) embaixo.
// Cena 1: fundo de batalha GALAR_FIELD, com um retrato e um NPC.
// Cena 2: fundo de batalha GALAR_STADIUM_RED, com um retrato.
// Apertar A passa para a cena seguinte.
#include "global.h"
#include "bg.h"
#include "battle_environment.h"
#include "constants/battle.h"
#include "constants/trainers.h"
#include "constants/event_objects.h"
#include "decompress.h"
#include "event_object_movement.h"
#include "gpu_regs.h"
#include "main.h"
#include "malloc.h"
#include "palette.h"
#include "scanline_effect.h"
#include "sprite.h"
#include "task.h"
#include "trainer_pokemon_sprites.h"

static u8 sCena;

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

    if (sCena == 0)
    {
        gPlttBufferUnfaded[0] = gPlttBufferFaded[0] = RGB(20, 20, 20);
        CreateTrainerPicSprite(TRAINER_PIC_GALAR_LEON, TRUE, 44, 50, 0, TAG_NONE);
        CreateTrainerPicSprite(TRAINER_PIC_GALAR_NESSA, TRUE, 120, 50, 1, TAG_NONE);
        CreateTrainerPicSprite(TRAINER_PIC_UNOVA_ELESA, TRUE, 196, 50, 2, TAG_NONE);
        CreateObjectGraphicsSprite(OBJ_EVENT_GFX_GALAR_LEON, SpriteCallbackDummy, 44, 124, 0);
        CreateObjectGraphicsSprite(OBJ_EVENT_GFX_GALAR_NESSA, SpriteCallbackDummy, 120, 124, 0);
        CreateObjectGraphicsSprite(OBJ_EVENT_GFX_UNOVA_ELESA, SpriteCallbackDummy, 196, 124, 0);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    }
    else
    {
        CarregaFundo(sCena == 1 ? BATTLE_ENVIRONMENT_GALAR_FIELD : BATTLE_ENVIRONMENT_GALAR_STADIUM_RED);
        ShowBg(3);
        CreateTrainerPicSprite(sCena == 1 ? TRAINER_PIC_GALAR_HOP : TRAINER_PIC_UNOVA_ELESA, TRUE, 176, 60, 0, TAG_NONE);
        if (sCena == 1)
            CreateObjectGraphicsSprite(OBJ_EVENT_GFX_GALAR_MARNIE, SpriteCallbackDummy, 70, 110, 0);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_BG3_ON | DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    }
    SetVBlankCallback(VBlankCB_Prova);
}

static void CB2_Prova(void)
{
    if (gMain.newKeys & A_BUTTON)
    {
        sCena = (sCena + 1) % 3;
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
