#include "global.h"
#include "decompress.h"
#include "graphics.h"
#include "malloc.h"
#include "mail.h"
#include "palette.h"
#include "pokemon_sprite_visualizer.h"
#include "pokemon_icon.h"
#include "sprite.h"
#include "data.h"
#include "constants/pokemon_icon.h"

// Os ícones são 32x32 4bpp com dois quadros de animação, guardados comprimidos
// (.smol) na ROM. Cada sprite de ícone aloca os 32 tiles dos DOIS quadros e o
// ícone é descomprimido direto para a VRAM na criação; animar passa a ser só
// mover o tileNum, sem cópia por quadro.
#define MON_ICON_FRAME_TILES  16
#define MON_ICON_TILES        (MON_ICON_FRAME_TILES * 2)

struct MonIconSpriteTemplate
{
    const struct OamData *oam;
    const u32 *image;
    const union AnimCmd *const *anims;
    const union AffineAnimCmd *const *affineAnims;
    void (*callback)(struct Sprite *);
    u16 paletteTag;
};

static u8 CreateMonIconSprite(struct MonIconSpriteTemplate *, s16, s16, u8);
static void FreeAndDestroyMonIconSprite_(struct Sprite *sprite);

const struct SpritePalette gMonIconPaletteTable[] =
{
    { gMonIconPalettes[0], POKE_ICON_BASE_PAL_TAG + 0 },
    { gMonIconPalettes[1], POKE_ICON_BASE_PAL_TAG + 1 },
    { gMonIconPalettes[2], POKE_ICON_BASE_PAL_TAG + 2 },
    { gMonIconPalettes[3], POKE_ICON_BASE_PAL_TAG + 3 },
    { gMonIconPalettes[4], POKE_ICON_BASE_PAL_TAG + 4 },
    { gMonIconPalettes[5], POKE_ICON_BASE_PAL_TAG + 5 },
};

static const struct OamData sMonIconOamData =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(32x32),
    .x = 0,
    .size = SPRITE_SIZE(32x32),
    .tileNum = 0,
    .priority = 1,
    .paletteNum = 0,
};

// fastest to slowest

static const union AnimCmd sAnim_0[] =
{
    ANIMCMD_FRAME(0, 6),
    ANIMCMD_FRAME(1, 6),
    ANIMCMD_JUMP(0),
};

static const union AnimCmd sAnim_1[] =
{
    ANIMCMD_FRAME(0, 8),
    ANIMCMD_FRAME(1, 8),
    ANIMCMD_JUMP(0),
};

static const union AnimCmd sAnim_2[] =
{
    ANIMCMD_FRAME(0, 14),
    ANIMCMD_FRAME(1, 14),
    ANIMCMD_JUMP(0),
};

static const union AnimCmd sAnim_3[] =
{
    ANIMCMD_FRAME(0, 22),
    ANIMCMD_FRAME(1, 22),
    ANIMCMD_JUMP(0),
};

static const union AnimCmd sAnim_4[] =
{
    ANIMCMD_FRAME(0, 29),
    ANIMCMD_FRAME(0, 29), // frame 0 is repeated
    ANIMCMD_JUMP(0),
};

static const union AnimCmd *const sMonIconAnims[] =
{
    sAnim_0,
    sAnim_1,
    sAnim_2,
    sAnim_3,
    sAnim_4,
};

static const union AffineAnimCmd sAffineAnim_0[] =
{
    AFFINEANIMCMD_FRAME(0, 0, 0, 10),
    AFFINEANIMCMD_END,
};

static const union AffineAnimCmd sAffineAnim_1[] =
{
    AFFINEANIMCMD_FRAME(-2, -2, 0, 122),
    AFFINEANIMCMD_END,
};

static const union AffineAnimCmd *const sMonIconAffineAnims[] =
{
    sAffineAnim_0,
    sAffineAnim_1,
};

// Estático de propósito: o sprite guarda esse ponteiro a vida inteira e
// DestroySprite lê o `.size` dele para devolver os tiles. Um temporário de pilha
// (o que o código fazia antes) só sobrevive porque todo mundo passa por
// FreeAndDestroyMonIconSprite; com o estático, DestroySprite direto também acerta.
static const struct SpriteFrameImage sMonIconImage = { NULL, MON_ICON_TILES * TILE_SIZE_4BPP };

u8 CreateMonIcon(enum Species species, void (*callback)(struct Sprite *), s16 x, s16 y, u8 subpriority, u32 personality)
{
    return CreateMonIconIsEgg(species, callback, x, y, subpriority, personality, FALSE);
}

u8 CreateMonIconIsEgg(enum Species species, void (*callback)(struct Sprite *), s16 x, s16 y, u8 subpriority, u32 personality, bool32 isEgg)
{
    u8 spriteId;
    struct MonIconSpriteTemplate iconTemplate =
    {
        .oam = &sMonIconOamData,
        .image = GetMonIconPtrIsEgg(species, personality, isEgg),
        .anims = sMonIconAnims,
        .affineAnims = sMonIconAffineAnims,
        .callback = callback,
        .paletteTag = POKE_ICON_BASE_PAL_TAG + gSpeciesInfo[species].iconPalIndex,
    };
    species = SanitizeSpeciesId(species);

    if (isEgg)
    {
        if (gSpeciesInfo[species].eggId != EGG_ID_NONE)
            iconTemplate.paletteTag = POKE_ICON_BASE_PAL_TAG + gEggDatas[gSpeciesInfo[species].eggId].eggIconPalIndex;
        else
            iconTemplate.paletteTag = POKE_ICON_BASE_PAL_TAG + gSpeciesInfo[SPECIES_EGG].iconPalIndex;
    }
    else if (species > NUM_SPECIES)
    {
        iconTemplate.paletteTag = POKE_ICON_BASE_PAL_TAG;
    }
#if P_GENDER_DIFFERENCES
    else if (gSpeciesInfo[species].iconSpriteFemale != NULL && IsPersonalityFemale(species, personality))
    {
        iconTemplate.paletteTag = POKE_ICON_BASE_PAL_TAG + gSpeciesInfo[species].iconPalIndexFemale;
    }
#endif

    spriteId = CreateMonIconSprite(&iconTemplate, x, y, subpriority);
    if (spriteId < MAX_SPRITES)
        UpdateMonIconFrame(&gSprites[spriteId]);

    return spriteId;
}


u8 CreateMonIconNoPersonality(enum Species species, void (*callback)(struct Sprite *), s16 x, s16 y, u8 subpriority)
{
    return CreateMonIconNoPersonalityIsEgg(species, callback, x, y, subpriority, FALSE);
}
u8 CreateMonIconNoPersonalityIsEgg(enum Species species, void (*callback)(struct Sprite *), s16 x, s16 y, u8 subpriority, bool32 isEgg)
{
    u8 spriteId;
    struct MonIconSpriteTemplate iconTemplate =
    {
        .oam = &sMonIconOamData,
        .image = NULL,
        .anims = sMonIconAnims,
        .affineAnims = sMonIconAffineAnims,
        .callback = callback,
        .paletteTag = POKE_ICON_BASE_PAL_TAG + gSpeciesInfo[species].iconPalIndex,
    };

    iconTemplate.image = GetMonIconTilesIsEgg(species, 0, isEgg);
    spriteId = CreateMonIconSprite(&iconTemplate, x, y, subpriority);
    if (spriteId < MAX_SPRITES)
        UpdateMonIconFrame(&gSprites[spriteId]);

    return spriteId;
}

enum Species GetIconSpecies(enum Species species, u32 personality)
{
    species = SanitizeSpeciesId(species);
    if (species == SPECIES_UNOWN)
        species = GetUnownSpeciesId(personality);
    return species;
}

u16 GetUnownLetterByPersonality(u32 personality)
{
    if (!personality)
        return 0;
    else
        return GET_UNOWN_LETTER(personality);
}

enum Species GetIconSpeciesNoPersonality(enum Species species)
{
    species = SanitizeSpeciesId(species);

    if (MailSpeciesToSpecies(species, &species) == SPECIES_UNOWN)
        return species += SPECIES_UNOWN_B; // TODO
    return GetIconSpecies(species, 0);
}

// Para quem precisa dos pixels do ícone na CPU (BG, blit em janela, folha de
// sprite) e não do caminho de sprite acima. Devolve os 1024 B dos dois quadros
// num buffer do heap; o chamador libera com Free. NULL se o heap estiver cheio.
u8 *AllocDecompressedMonIcon(const u32 *icon)
{
    u8 *buffer = Alloc(MON_ICON_TILES * TILE_SIZE_4BPP);

    if (buffer != NULL)
        DecompressDataWithHeaderWram(icon, buffer);
    return buffer;
}

const u32 *GetMonIconPtr(enum Species species, u32 personality)
{
    return GetMonIconPtrIsEgg(species, personality, FALSE);
}

const u32 *GetMonIconPtrIsEgg(enum Species species, u32 personality, bool32 isEgg)
{
    return GetMonIconTilesIsEgg(GetIconSpecies(species, personality), personality, isEgg);
}

void FreeAndDestroyMonIconSprite(struct Sprite *sprite)
{
    FreeAndDestroyMonIconSprite_(sprite);
}

void LoadMonIconPalettes(void)
{
    u8 i;
    for (i = 0; i < ARRAY_COUNT(gMonIconPaletteTable); i++)
        LoadSpritePalette(&gMonIconPaletteTable[i]);
}

// unused
void SafeLoadMonIconPalette(enum Species species)
{
    u8 palIndex;
    palIndex = gSpeciesInfo[SanitizeSpeciesId(species)].iconPalIndex;
    if (IndexOfSpritePaletteTag(gMonIconPaletteTable[palIndex].tag) == 0xFF)
        LoadSpritePalette(&gMonIconPaletteTable[palIndex]);
}

void LoadMonIconPalette(enum Species species)
{
    u8 palIndex = gSpeciesInfo[SanitizeSpeciesId(species)].iconPalIndex;
    if (IndexOfSpritePaletteTag(gMonIconPaletteTable[palIndex].tag) == 0xFF)
        LoadSpritePalette(&gMonIconPaletteTable[palIndex]);
}

void LoadMonIconPalettePersonality(enum Species species, u32 personality)
{
    u8 palIndex;
    species = SanitizeSpeciesId(species);
#if P_GENDER_DIFFERENCES
    if (gSpeciesInfo[species].iconSpriteFemale != NULL && IsPersonalityFemale(species, personality))
        palIndex = gSpeciesInfo[species].iconPalIndexFemale;
    else
#endif
        palIndex = gSpeciesInfo[species].iconPalIndex;
    if (IndexOfSpritePaletteTag(gMonIconPaletteTable[palIndex].tag) == 0xFF)
        LoadSpritePalette(&gMonIconPaletteTable[palIndex]);
}

void FreeMonIconPalettes(void)
{
    u8 i;
    for (i = 0; i < ARRAY_COUNT(gMonIconPaletteTable); i++)
        FreeSpritePaletteByTag(gMonIconPaletteTable[i].tag);
}

// unused
void SafeFreeMonIconPalette(enum Species species)
{
    u8 palIndex;
    palIndex = gSpeciesInfo[SanitizeSpeciesId(species)].iconPalIndex;
    FreeSpritePaletteByTag(gMonIconPaletteTable[palIndex].tag);
}

void FreeMonIconPalette(enum Species species)
{
    u8 palIndex;
    palIndex = gSpeciesInfo[SanitizeSpeciesId(species)].iconPalIndex;
    FreeSpritePaletteByTag(gMonIconPaletteTable[palIndex].tag);
}

void SpriteCB_MonIcon(struct Sprite *sprite)
{
    UpdateMonIconFrame(sprite);
}

const u32 *GetMonIconTiles(enum Species species, u32 personality)
{
    return GetMonIconTilesIsEgg(species, personality, FALSE);
}

const u32 *GetMonIconTilesIsEgg(enum Species species, u32 personality, bool32 isEgg)
{
    const u32 *iconSprite;

    if (species > NUM_SPECIES)
        species = SPECIES_NONE;

    if (isEgg)
    {
        if (gSpeciesInfo[species].eggId != EGG_ID_NONE)
            iconSprite = gEggDatas[gSpeciesInfo[species].eggId].eggIcon;
        else
            iconSprite = gSpeciesInfo[SPECIES_EGG].iconSprite;
    }
    else
    {
#if P_GENDER_DIFFERENCES
        if (gSpeciesInfo[species].iconSpriteFemale != NULL && IsPersonalityFemale(species, personality))
            iconSprite = gSpeciesInfo[species].iconSpriteFemale;
        else
#endif
        if (gSpeciesInfo[species].iconSprite != NULL)
            iconSprite = gSpeciesInfo[species].iconSprite;
        else
            iconSprite = gSpeciesInfo[SPECIES_NONE].iconSprite;
    }

    return iconSprite;
}

const u32 *GetMonIconTilesByIconType(enum Species species, enum SpeciesIconType iconType)
{
    if (iconType == EGG_ICON)
        return gEggDatas[gSpeciesInfo[species].eggId].eggIcon;
    if (iconType == FEMALE_ICON)
        return gSpeciesInfo[species].iconSpriteFemale;
    return gSpeciesInfo[species].iconSprite;
}

void TryLoadAllMonIconPalettesAtOffset(u16 offset)
{
    s32 i;
    if (offset <= BG_PLTT_ID(16 - ARRAY_COUNT(gMonIconPaletteTable)))
    {
        for (i = 0; i < (int)ARRAY_COUNT(gMonIconPaletteTable); i++)
        {
            LoadPalette(gMonIconPaletteTable[i].data, offset, PLTT_SIZE_4BPP);
            offset += 16;
        }
    }
}

u8 GetValidMonIconPalIndex(enum Species species)
{
    return gSpeciesInfo[SanitizeSpeciesId(species)].iconPalIndex;
}

u8 GetMonIconPaletteIndexFromSpecies(enum Species species)
{
    return gSpeciesInfo[SanitizeSpeciesId(species)].iconPalIndex;
}

const u16 *GetValidMonIconPalettePtr(enum Species species)
{
    return gMonIconPaletteTable[gSpeciesInfo[SanitizeSpeciesId(species)].iconPalIndex].data;
}

u8 UpdateMonIconFrame(struct Sprite *sprite)
{
    u8 result = 0;

    if (sprite->animDelayCounter == 0)
    {
        s16 frame = sprite->anims[sprite->animNum][sprite->animCmdIndex].frame.imageValue;

        switch (frame)
        {
        case -1:
            break;
        case -2:
            sprite->animCmdIndex = 0;
            break;
        default:
            // Os dois quadros já estão na VRAM do próprio sprite (sheetTileStart
            // guarda a base alocada), então trocar de quadro é só mover o tileNum.
            sprite->oam.tileNum = sprite->sheetTileStart + (frame * MON_ICON_FRAME_TILES);
            sprite->animDelayCounter = sprite->anims[sprite->animNum][sprite->animCmdIndex].frame.duration & 0xFF;
            sprite->animCmdIndex++;
            result = sprite->animCmdIndex;
            break;
        }
    }
    else
    {
        sprite->animDelayCounter--;
    }
    return result;
}

static u8 CreateMonIconSprite(struct MonIconSpriteTemplate *iconTemplate, s16 x, s16 y, u8 subpriority)
{
    u8 spriteId;

    struct SpriteTemplate spriteTemplate =
    {
        .tileTag = TAG_NONE,
        .paletteTag = iconTemplate->paletteTag,
        .oam = iconTemplate->oam,
        .anims = iconTemplate->anims,
        .images = &sMonIconImage,
        .affineAnims = iconTemplate->affineAnims,
        .callback = iconTemplate->callback,
    };

    spriteId = CreateSprite(&spriteTemplate, x, y, subpriority);
    if (spriteId >= MAX_SPRITES) // sem tiles livres na OBJ VRAM
        return spriteId;

    gSprites[spriteId].animPaused = TRUE;
    gSprites[spriteId].animBeginning = FALSE;
    gSprites[spriteId].sheetTileStart = gSprites[spriteId].oam.tileNum;
    DecompressDataWithHeaderVram(iconTemplate->image,
                                 (void *)(OBJ_VRAM0 + gSprites[spriteId].oam.tileNum * TILE_SIZE_4BPP));
    return spriteId;
}

static void FreeAndDestroyMonIconSprite_(struct Sprite *sprite)
{
    // O tileNum pode estar no segundo quadro; DestroySprite devolve os tiles a
    // partir dele, então volta para a base antes de destruir.
    sprite->oam.tileNum = sprite->sheetTileStart;
    DestroySprite(sprite);
}

void SetPartyHPBarSprite(struct Sprite *sprite, u8 animNum)
{
    sprite->animNum = animNum;
    sprite->animDelayCounter = 0;
    sprite->animCmdIndex = 0;
}
