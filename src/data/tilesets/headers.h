#include "fieldmap.h"

// Whether a palette has a night version, located at ((x + 9) % 16).pal
#define SWAP_PAL(x) ((x) < NUM_PALS_IN_PRIMARY ? 1 << (x) : 1 << ((x) - NUM_PALS_IN_PRIMARY))

const struct Tileset gTileset_SecretBase =
{
    .isCompressed = FALSE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_SecretBase,
    .palettes = gTilesetPalettes_SecretBase,
    .metatiles = gMetatiles_SecretBasePrimary,
    .metatileAttributes = gMetatileAttributes_SecretBasePrimary,
    .callback = NULL,
};

const struct Tileset gTileset_SecretBaseRedCave =
{
    .isCompressed = FALSE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SecretBaseRedCave,
    .palettes = gTilesetPalettes_SecretBaseRedCave,
    .metatiles = gMetatiles_SecretBaseSecondary,
    .metatileAttributes = gMetatileAttributes_SecretBaseSecondary,
    .callback = NULL,
};

const struct Tileset *const gTilesetPointer_SecretBase = &gTileset_SecretBase;
const struct Tileset *const gTilesetPointer_SecretBaseRedCave = &gTileset_SecretBaseRedCave;

// Kanto so aparece se os dois conjuntos de tileset forem compilados.

const struct Tileset gTileset_General =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_General,
    .palettes = gTilesetPalettes_General,
    .metatiles = gMetatiles_General,
    .metatileAttributes = gMetatileAttributes_General,
    .callback = InitTilesetAnim_General,
};

const struct Tileset gTileset_GeneralSinnoh =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_GeneralSinnoh,
    .palettes = gTilesetPalettes_GeneralSinnoh,
    .metatiles = gMetatiles_GeneralSinnoh,
    .metatileAttributes = gMetatileAttributes_GeneralSinnoh,
    .callback = InitTilesetAnim_General,
};
// gTileset_SinnohWest removido: nunca teve tiles, paletas, metatiles nem pasta em
// data/tilesets/, e nenhum layout apontava para ele. Só quebrava o link.

const struct Tileset gTileset_Petalburg =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Petalburg,
    .palettes = gTilesetPalettes_Petalburg,
    .metatiles = gMetatiles_Petalburg,
    .metatileAttributes = gMetatileAttributes_Petalburg,
    .callback = InitTilesetAnim_Petalburg,
};

const struct Tileset gTileset_PetalburgSinnoh =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PetalburgSinnoh,
    .palettes = gTilesetPalettes_PetalburgSinnoh,
    .metatiles = gMetatiles_PetalburgSinnoh,
    .metatileAttributes = gMetatileAttributes_PetalburgSinnoh,
    .callback = InitTilesetAnim_Petalburg,
};

const struct Tileset gTileset_Rustboro =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Rustboro,
    .palettes = gTilesetPalettes_Rustboro,
    .metatiles = gMetatiles_Rustboro,
    .metatileAttributes = gMetatileAttributes_Rustboro,
    .callback = InitTilesetAnim_Rustboro,
};

const struct Tileset gTileset_RustboroSinnoh =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_RustboroSinnoh,
    .palettes = gTilesetPalettes_RustboroSinnoh,
    .metatiles = gMetatiles_RustboroSinnoh,
    .metatileAttributes = gMetatileAttributes_RustboroSinnoh,
    .callback = InitTilesetAnim_Rustboro,
};

const struct Tileset gTileset_Dewford =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Dewford,
    .palettes = gTilesetPalettes_Dewford,
    .metatiles = gMetatiles_Dewford,
    .metatileAttributes = gMetatileAttributes_Dewford,
    .callback = InitTilesetAnim_Dewford,
};

const struct Tileset gTileset_Slateport =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Slateport,
    .palettes = gTilesetPalettes_Slateport,
    .metatiles = gMetatiles_Slateport,
    .metatileAttributes = gMetatileAttributes_Slateport,
    .callback = InitTilesetAnim_Slateport,
};

const struct Tileset gTileset_Mauville =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Mauville,
    .palettes = gTilesetPalettes_Mauville,
    .metatiles = gMetatiles_Mauville,
    .metatileAttributes = gMetatileAttributes_Mauville,
    .callback = InitTilesetAnim_Mauville,
};

const struct Tileset gTileset_MauvilleSinnoh =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MauvilleSinnoh,
    .palettes = gTilesetPalettes_MauvilleSinnoh,
    .metatiles = gMetatiles_MauvilleSinnoh,
    .metatileAttributes = gMetatileAttributes_MauvilleSinnoh,
    .callback = InitTilesetAnim_Mauville,
};

const struct Tileset gTileset_Lavaridge =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Lavaridge,
    .palettes = gTilesetPalettes_Lavaridge,
    .metatiles = gMetatiles_Lavaridge,
    .metatileAttributes = gMetatileAttributes_Lavaridge,
    .callback = InitTilesetAnim_Lavaridge,
};

const struct Tileset gTileset_LavaridgeSinnoh =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LavaridgeSinnoh,
    .palettes = gTilesetPalettes_LavaridgeSinnoh,
    .metatiles = gMetatiles_LavaridgeSinnoh,
    .metatileAttributes = gMetatileAttributes_LavaridgeSinnoh,
    .callback = InitTilesetAnim_Lavaridge,
};

const struct Tileset gTileset_Fallarbor =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Fallarbor,
    .palettes = gTilesetPalettes_Fallarbor,
    .metatiles = gMetatiles_Fallarbor,
    .metatileAttributes = gMetatileAttributes_Fallarbor,
    .callback = InitTilesetAnim_Fallarbor,
};

const struct Tileset gTileset_Fortree =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Fortree,
    .palettes = gTilesetPalettes_Fortree,
    .metatiles = gMetatiles_Fortree,
    .metatileAttributes = gMetatileAttributes_Fortree,
    .callback = InitTilesetAnim_Fortree,
};

const struct Tileset gTileset_Lilycove =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Lilycove,
    .palettes = gTilesetPalettes_Lilycove,
    .metatiles = gMetatiles_Lilycove,
    .metatileAttributes = gMetatileAttributes_Lilycove,
    .callback = InitTilesetAnim_Lilycove,
};

const struct Tileset gTileset_LilycoveSinnoh =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LilycoveSinnoh,
    .palettes = gTilesetPalettes_LilycoveSinnoh,
    .metatiles = gMetatiles_LilycoveSinnoh,
    .metatileAttributes = gMetatileAttributes_LilycoveSinnoh,
    .callback = InitTilesetAnim_Lilycove,
};

const struct Tileset gTileset_Mossdeep =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Mossdeep,
    .palettes = gTilesetPalettes_Mossdeep,
    .metatiles = gMetatiles_Mossdeep,
    .metatileAttributes = gMetatileAttributes_Mossdeep,
    .callback = InitTilesetAnim_Mossdeep,
};

const struct Tileset gTileset_EverGrande =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_EverGrande,
    .palettes = gTilesetPalettes_EverGrande,
    .metatiles = gMetatiles_EverGrande,
    .metatileAttributes = gMetatileAttributes_EverGrande,
    .callback = InitTilesetAnim_EverGrande,
};

const struct Tileset gTileset_EverGrandeSinnoh =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_EverGrandeSinnoh,
    .palettes = gTilesetPalettes_EverGrandeSinnoh,
    .metatiles = gMetatiles_EverGrandeSinnoh,
    .metatileAttributes = gMetatileAttributes_EverGrandeSinnoh,
    .callback = InitTilesetAnim_EverGrande,
};

const struct Tileset gTileset_Pacifidlog =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Pacifidlog,
    .palettes = gTilesetPalettes_Pacifidlog,
    .metatiles = gMetatiles_Pacifidlog,
    .metatileAttributes = gMetatileAttributes_Pacifidlog,
    .callback = InitTilesetAnim_Pacifidlog,
};

const struct Tileset gTileset_Sootopolis =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Sootopolis,
    .palettes = gTilesetPalettes_Sootopolis,
    .metatiles = gMetatiles_Sootopolis,
    .metatileAttributes = gMetatileAttributes_Sootopolis,
    .callback = InitTilesetAnim_Sootopolis,
};

const struct Tileset gTileset_BattleFrontierOutsideWest =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFrontierOutsideWest,
    .palettes = gTilesetPalettes_BattleFrontierOutsideWest,
    .metatiles = gMetatiles_BattleFrontierOutsideWest,
    .metatileAttributes = gMetatileAttributes_BattleFrontierOutsideWest,
    .callback = InitTilesetAnim_BattleFrontierOutsideWest,
};

const struct Tileset gTileset_BattleFrontierOutsideEast =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFrontierOutsideEast,
    .palettes = gTilesetPalettes_BattleFrontierOutsideEast,
    .metatiles = gMetatiles_BattleFrontierOutsideEast,
    .metatileAttributes = gMetatileAttributes_BattleFrontierOutsideEast,
    .callback = InitTilesetAnim_BattleFrontierOutsideEast,
};

const struct Tileset gTileset_Building =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_InsideBuilding,
    .palettes = gTilesetPalettes_InsideBuilding,
    .metatiles = gMetatiles_InsideBuilding,
    .metatileAttributes = gMetatileAttributes_InsideBuilding,
    .callback = InitTilesetAnim_Building,
};

const struct Tileset gTileset_Shop =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Shop,
    .palettes = gTilesetPalettes_Shop,
    .metatiles = gMetatiles_Shop,
    .metatileAttributes = gMetatileAttributes_Shop,
    .callback = NULL,
};

const struct Tileset gTileset_ShopSinnoh =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_ShopSinnoh,
    .palettes = gTilesetPalettes_ShopSinnoh,
    .metatiles = gMetatiles_ShopSinnoh,
    .metatileAttributes = gMetatileAttributes_ShopSinnoh,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonCenter =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonCenter,
    .palettes = gTilesetPalettes_PokemonCenter,
    .metatiles = gMetatiles_PokemonCenter,
    .metatileAttributes = gMetatileAttributes_PokemonCenter,
    .callback = NULL,
};

const struct Tileset gTileset_Cave =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Cave,
    .palettes = gTilesetPalettes_Cave,
    .metatiles = gMetatiles_Cave,
    .metatileAttributes = gMetatileAttributes_Cave,
    .callback = InitTilesetAnim_Cave,
};

const struct Tileset gTileset_CaveSinnoh =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CaveSinnoh,
    .palettes = gTilesetPalettes_CaveSinnoh,
    .metatiles = gMetatiles_CaveSinnoh,
    .metatileAttributes = gMetatileAttributes_CaveSinnoh,
    .callback = InitTilesetAnim_Cave,
};

const struct Tileset gTileset_PokemonSchool =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonSchool,
    .palettes = gTilesetPalettes_PokemonSchool,
    .metatiles = gMetatiles_PokemonSchool,
    .metatileAttributes = gMetatileAttributes_PokemonSchool,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonFanClub =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonFanClub,
    .palettes = gTilesetPalettes_PokemonFanClub,
    .metatiles = gMetatiles_PokemonFanClub,
    .metatileAttributes = gMetatileAttributes_PokemonFanClub,
    .callback = NULL,
};

const struct Tileset gTileset_Unused1 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Unused1,
    .palettes = gTilesetPalettes_Unused1,
    .metatiles = gMetatiles_Unused1,
    .metatileAttributes = gMetatileAttributes_Unused1,
    .callback = NULL,
};

const struct Tileset gTileset_MeteorFalls =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MeteorFalls,
    .palettes = gTilesetPalettes_MeteorFalls,
    .metatiles = gMetatiles_MeteorFalls,
    .metatileAttributes = gMetatileAttributes_MeteorFalls,
    .callback = NULL,
};

const struct Tileset gTileset_OceanicMuseum =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_OceanicMuseum,
    .palettes = gTilesetPalettes_OceanicMuseum,
    .metatiles = gMetatiles_OceanicMuseum,
    .metatileAttributes = gMetatileAttributes_OceanicMuseum,
    .callback = NULL,
};

const struct Tileset gTileset_CableClub =
{
    .isCompressed = FALSE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CableClub,
    .palettes = gTilesetPalettes_CableClub,
    .metatiles = gMetatiles_CableClub,
    .metatileAttributes = gMetatileAttributes_CableClub,
    .callback = NULL,
};

const struct Tileset gTileset_SeashoreHouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SeashoreHouse,
    .palettes = gTilesetPalettes_SeashoreHouse,
    .metatiles = gMetatiles_SeashoreHouse,
    .metatileAttributes = gMetatileAttributes_SeashoreHouse,
    .callback = NULL,
};

const struct Tileset gTileset_PrettyPetalFlowerShop =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PrettyPetalFlowerShop,
    .palettes = gTilesetPalettes_PrettyPetalFlowerShop,
    .metatiles = gMetatiles_PrettyPetalFlowerShop,
    .metatileAttributes = gMetatileAttributes_PrettyPetalFlowerShop,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonDayCare =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonDayCare,
    .palettes = gTilesetPalettes_PokemonDayCare,
    .metatiles = gMetatiles_PokemonDayCare,
    .metatileAttributes = gMetatileAttributes_PokemonDayCare,
    .callback = NULL,
};

const struct Tileset gTileset_Facility =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Facility,
    .palettes = gTilesetPalettes_Facility,
    .metatiles = gMetatiles_Facility,
    .metatileAttributes = gMetatileAttributes_Facility,
    .callback = NULL,
};

const struct Tileset gTileset_BikeShop =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BikeShop,
    .palettes = gTilesetPalettes_BikeShop,
    .metatiles = gMetatiles_BikeShop,
    .metatileAttributes = gMetatileAttributes_BikeShop,
    .callback = InitTilesetAnim_BikeShop,
};

const struct Tileset gTileset_RusturfTunnel =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_RusturfTunnel,
    .palettes = gTilesetPalettes_RusturfTunnel,
    .metatiles = gMetatiles_RusturfTunnel,
    .metatileAttributes = gMetatileAttributes_RusturfTunnel,
    .callback = NULL,
};

const struct Tileset gTileset_SecretBaseBrownCave =
{
    .isCompressed = FALSE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SecretBaseBrownCave,
    .palettes = gTilesetPalettes_SecretBaseBrownCave,
    .metatiles = gMetatiles_SecretBaseSecondary,
    .metatileAttributes = gMetatileAttributes_SecretBaseSecondary,
    .callback = NULL,
};

const struct Tileset gTileset_SecretBaseTree =
{
    .isCompressed = FALSE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SecretBaseTree,
    .palettes = gTilesetPalettes_SecretBaseTree,
    .metatiles = gMetatiles_SecretBaseSecondary,
    .metatileAttributes = gMetatileAttributes_SecretBaseSecondary,
    .callback = NULL,
};

const struct Tileset gTileset_SecretBaseShrub =
{
    .isCompressed = FALSE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SecretBaseShrub,
    .palettes = gTilesetPalettes_SecretBaseShrub,
    .metatiles = gMetatiles_SecretBaseSecondary,
    .metatileAttributes = gMetatileAttributes_SecretBaseSecondary,
    .callback = NULL,
};

const struct Tileset gTileset_SecretBaseBlueCave =
{
    .isCompressed = FALSE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SecretBaseBlueCave,
    .palettes = gTilesetPalettes_SecretBaseBlueCave,
    .metatiles = gMetatiles_SecretBaseSecondary,
    .metatileAttributes = gMetatileAttributes_SecretBaseSecondary,
    .callback = NULL,
};

const struct Tileset gTileset_SecretBaseYellowCave =
{
    .isCompressed = FALSE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SecretBaseYellowCave,
    .palettes = gTilesetPalettes_SecretBaseYellowCave,
    .metatiles = gMetatiles_SecretBaseSecondary,
    .metatileAttributes = gMetatileAttributes_SecretBaseSecondary,
    .callback = NULL,
};

const struct Tileset gTileset_InsideOfTruck =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_InsideOfTruck,
    .palettes = gTilesetPalettes_InsideOfTruck,
    .metatiles = gMetatiles_InsideOfTruck,
    .metatileAttributes = gMetatileAttributes_InsideOfTruck,
    .callback = NULL,
};

const struct Tileset gTileset_Unused2 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Unused2,
    .palettes = gTilesetPalettes_Unused2,
    .metatiles = gMetatiles_Unused2,
    .metatileAttributes = gMetatileAttributes_Unused2,
    .callback = NULL,
};

const struct Tileset gTileset_Contest =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Contest,
    .palettes = gTilesetPalettes_Contest,
    .metatiles = gMetatiles_Contest,
    .metatileAttributes = gMetatileAttributes_Contest,
    .callback = NULL,
};

const struct Tileset gTileset_LilycoveMuseum =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LilycoveMuseum,
    .palettes = gTilesetPalettes_LilycoveMuseum,
    .metatiles = gMetatiles_LilycoveMuseum,
    .metatileAttributes = gMetatileAttributes_LilycoveMuseum,
    .callback = NULL,
};

const struct Tileset gTileset_BrendansMaysHouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BrendansMaysHouse,
    .palettes = gTilesetPalettes_BrendansMaysHouse,
    .metatiles = gMetatiles_BrendansMaysHouse,
    .metatileAttributes = gMetatileAttributes_BrendansMaysHouse,
    .callback = NULL,
};

const struct Tileset gTileset_Lab =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Lab,
    .palettes = gTilesetPalettes_Lab,
    .metatiles = gMetatiles_Lab,
    .metatileAttributes = gMetatileAttributes_Lab,
    .callback = NULL,
};

const struct Tileset gTileset_Underwater =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Underwater,
    .palettes = gTilesetPalettes_Underwater,
    .metatiles = gMetatiles_Underwater,
    .metatileAttributes = gMetatileAttributes_Underwater,
    .callback = InitTilesetAnim_Underwater,
};

const struct Tileset gTileset_PetalburgGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PetalburgGym,
    .palettes = gTilesetPalettes_PetalburgGym,
    .metatiles = gMetatiles_PetalburgGym,
    .metatileAttributes = gMetatileAttributes_PetalburgGym,
    .callback = NULL,
};

const struct Tileset gTileset_SootopolisGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SootopolisGym,
    .palettes = gTilesetPalettes_SootopolisGym,
    .metatiles = gMetatiles_SootopolisGym,
    .metatileAttributes = gMetatileAttributes_SootopolisGym,
    .callback = InitTilesetAnim_SootopolisGym,
};

const struct Tileset gTileset_GenericBuilding =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GenericBuilding,
    .palettes = gTilesetPalettes_GenericBuilding,
    .metatiles = gMetatiles_GenericBuilding,
    .metatileAttributes = gMetatileAttributes_GenericBuilding,
    .callback = NULL,
};

const struct Tileset gTileset_MauvilleGameCorner =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MauvilleGameCorner,
    .palettes = gTilesetPalettes_MauvilleGameCorner,
    .metatiles = gMetatiles_MauvilleGameCorner,
    .metatileAttributes = gMetatileAttributes_MauvilleGameCorner,
    .callback = NULL,
};

const struct Tileset gTileset_RustboroGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_RustboroGym,
    .palettes = gTilesetPalettes_RustboroGym,
    .metatiles = gMetatiles_RustboroGym,
    .metatileAttributes = gMetatileAttributes_RustboroGym,
    .callback = NULL,
};

const struct Tileset gTileset_DewfordGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_DewfordGym,
    .palettes = gTilesetPalettes_DewfordGym,
    .metatiles = gMetatiles_DewfordGym,
    .metatileAttributes = gMetatileAttributes_DewfordGym,
    .callback = NULL,
};

const struct Tileset gTileset_MauvilleGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MauvilleGym,
    .palettes = gTilesetPalettes_MauvilleGym,
    .metatiles = gMetatiles_MauvilleGym,
    .metatileAttributes = gMetatileAttributes_MauvilleGym,
    .callback = InitTilesetAnim_MauvilleGym,
};

const struct Tileset gTileset_LavaridgeGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LavaridgeGym,
    .palettes = gTilesetPalettes_LavaridgeGym,
    .metatiles = gMetatiles_LavaridgeGym,
    .metatileAttributes = gMetatileAttributes_LavaridgeGym,
    .callback = NULL,
};

const struct Tileset gTileset_TrickHousePuzzle =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_TrickHousePuzzle,
    .palettes = gTilesetPalettes_TrickHousePuzzle,
    .metatiles = gMetatiles_TrickHousePuzzle,
    .metatileAttributes = gMetatileAttributes_TrickHousePuzzle,
    .callback = NULL,
};

const struct Tileset gTileset_FortreeGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_FortreeGym,
    .palettes = gTilesetPalettes_FortreeGym,
    .metatiles = gMetatiles_FortreeGym,
    .metatileAttributes = gMetatileAttributes_FortreeGym,
    .callback = NULL,
};

const struct Tileset gTileset_MossdeepGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MossdeepGym,
    .palettes = gTilesetPalettes_MossdeepGym,
    .metatiles = gMetatiles_MossdeepGym,
    .metatileAttributes = gMetatileAttributes_MossdeepGym,
    .callback = NULL,
};

const struct Tileset gTileset_InsideShip =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_InsideShip,
    .palettes = gTilesetPalettes_InsideShip,
    .metatiles = gMetatiles_InsideShip,
    .metatileAttributes = gMetatileAttributes_InsideShip,
    .callback = NULL,
};

const struct Tileset gTileset_EliteFour =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_EliteFour,
    .palettes = gTilesetPalettes_EliteFour,
    .metatiles = gMetatiles_EliteFour,
    .metatileAttributes = gMetatileAttributes_EliteFour,
    .callback = InitTilesetAnim_EliteFour,
};

const struct Tileset gTileset_BattleFrontier =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFrontier,
    .palettes = gTilesetPalettes_BattleFrontier,
    .metatiles = gMetatiles_BattleFrontier,
    .metatileAttributes = gMetatileAttributes_BattleFrontier,
    .callback = NULL,
};

const struct Tileset gTileset_BattlePalace =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattlePalace,
    .palettes = gTilesetPalettes_BattlePalace,
    .metatiles = gMetatiles_BattlePalace,
    .metatileAttributes = gMetatileAttributes_BattlePalace,
    .callback = NULL,
};

const struct Tileset gTileset_BattleDome =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleDome,
    .palettes = gTilesetPalettes_BattleDome,
    .metatiles = gMetatiles_BattleDome,
    .metatileAttributes = gMetatileAttributes_BattleDome,
    .callback = InitTilesetAnim_BattleDome,
};

const struct Tileset gTileset_BattleFactory =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFactory,
    .palettes = gTilesetPalettes_BattleFactory,
    .metatiles = gMetatiles_BattleFactory,
    .metatileAttributes = gMetatileAttributes_BattleFactory,
    .callback = NULL,
};

const struct Tileset gTileset_BattlePike =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattlePike,
    .palettes = gTilesetPalettes_BattlePike,
    .metatiles = gMetatiles_BattlePike,
    .metatileAttributes = gMetatileAttributes_BattlePike,
    .callback = NULL,
};

const struct Tileset gTileset_BattleArena =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleArena,
    .palettes = gTilesetPalettes_BattleArena,
    .metatiles = gMetatiles_BattleArena,
    .metatileAttributes = gMetatileAttributes_BattleArena,
    .callback = NULL,
};

const struct Tileset gTileset_BattlePyramid =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattlePyramid,
    .palettes = gTilesetPalettes_BattlePyramid,
    .metatiles = gMetatiles_BattlePyramid,
    .metatileAttributes = gMetatileAttributes_BattlePyramid,
    .callback = InitTilesetAnim_BattlePyramid,
};

const struct Tileset gTileset_MirageTower =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MirageTower,
    .palettes = gTilesetPalettes_MirageTower,
    .metatiles = gMetatiles_MirageTower,
    .metatileAttributes = gMetatileAttributes_MirageTower,
    .callback = NULL,
};

const struct Tileset gTileset_MossdeepGameCorner =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MossdeepGameCorner,
    .palettes = gTilesetPalettes_MossdeepGameCorner,
    .metatiles = gMetatiles_MossdeepGameCorner,
    .metatileAttributes = gMetatileAttributes_MossdeepGameCorner,
    .callback = NULL,
};

const struct Tileset gTileset_IslandHarbor =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_IslandHarbor,
    .palettes = gTilesetPalettes_IslandHarbor,
    .metatiles = gMetatiles_IslandHarbor,
    .metatileAttributes = gMetatileAttributes_IslandHarbor,
    .callback = NULL,
};

const struct Tileset gTileset_TrainerHill =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_TrainerHill,
    .palettes = gTilesetPalettes_TrainerHill,
    .metatiles = gMetatiles_TrainerHill,
    .metatileAttributes = gMetatileAttributes_TrainerHill,
    .callback = NULL,
};

const struct Tileset gTileset_NavelRock =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_NavelRock,
    .palettes = gTilesetPalettes_NavelRock,
    .metatiles = gMetatiles_NavelRock,
    .metatileAttributes = gMetatileAttributes_NavelRock,
    .callback = NULL,
};

const struct Tileset gTileset_BattleFrontierRankingHall =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFrontierRankingHall,
    .palettes = gTilesetPalettes_BattleFrontierRankingHall,
    .metatiles = gMetatiles_BattleFrontierRankingHall,
    .metatileAttributes = gMetatileAttributes_BattleFrontierRankingHall,
    .callback = NULL,
};

const struct Tileset gTileset_BattleTent =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleTent,
    .palettes = gTilesetPalettes_BattleTent,
    .metatiles = gMetatiles_BattleTent,
    .metatileAttributes = gMetatileAttributes_BattleTent,
    .callback = NULL,
};

const struct Tileset gTileset_MysteryEventsHouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MysteryEventsHouse,
    .palettes = gTilesetPalettes_MysteryEventsHouse,
    .metatiles = gMetatiles_MysteryEventsHouse,
    .metatileAttributes = gMetatileAttributes_MysteryEventsHouse,
    .callback = NULL,
};

const struct Tileset gTileset_UnionRoom =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnionRoom,
    .palettes = gTilesetPalettes_UnionRoom,
    .metatiles = gMetatiles_UnionRoom,
    .metatileAttributes = gMetatileAttributes_UnionRoom,
    .callback = NULL,
};


// Tilesets de Sinnoh, importados de LiderMorti00/Sinnoh-pokeemerald-expansion.
const struct Tileset gTileset_Jubilife =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Jubilife,
    .palettes = gTilesetPalettes_Jubilife,
    .metatiles = gMetatiles_Jubilife,
    .metatileAttributes = gMetatileAttributes_Jubilife,
    .callback = NULL,
};

const struct Tileset gTileset_Hearthome =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Hearthome,
    .palettes = gTilesetPalettes_Hearthome,
    .metatiles = gMetatiles_Hearthome,
    .metatileAttributes = gMetatileAttributes_Hearthome,
    .callback = NULL,
};

const struct Tileset gTileset_Celestic =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Celestic,
    .palettes = gTilesetPalettes_Celestic,
    .metatiles = gMetatiles_Celestic,
    .metatileAttributes = gMetatileAttributes_Celestic,
    .callback = NULL,
};

const struct Tileset gTileset_Veilstone =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Veilstone,
    .palettes = gTilesetPalettes_Veilstone,
    .metatiles = gMetatiles_Veilstone,
    .metatileAttributes = gMetatileAttributes_Veilstone,
    .callback = NULL,
};

const struct Tileset gTileset_Canalave =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Canalave,
    .palettes = gTilesetPalettes_Canalave,
    .metatiles = gMetatiles_Canalave,
    .metatileAttributes = gMetatileAttributes_Canalave,
    .callback = NULL,
};

const struct Tileset gTileset_Snowpoint =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Snowpoint,
    .palettes = gTilesetPalettes_Snowpoint,
    .metatiles = gMetatiles_Snowpoint,
    .metatileAttributes = gMetatileAttributes_Snowpoint,
    .callback = NULL,
};

const struct Tileset gTileset_Sunnyshore =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Sunnyshore,
    .palettes = gTilesetPalettes_Sunnyshore,
    .metatiles = gMetatiles_Sunnyshore,
    .metatileAttributes = gMetatileAttributes_Sunnyshore,
    .callback = NULL,
};

const struct Tileset gTileset_Valor =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Valor,
    .palettes = gTilesetPalettes_Valor,
    .metatiles = gMetatiles_Valor,
    .metatileAttributes = gMetatileAttributes_Valor,
    .callback = NULL,
};

const struct Tileset gTileset_Pasos =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Pasos,
    .palettes = gTilesetPalettes_Pasos,
    .metatiles = gMetatiles_Pasos,
    .metatileAttributes = gMetatileAttributes_Pasos,
    .callback = NULL,
};
// (antes: #else de #if !IS_FRLG, que deixava os tilesets de FRLG fora)

// FRLG tilesets
const struct Tileset gTileset_BuildingFrlg =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_Building_Frlg,
    .palettes = gTilesetPalettes_Building_Frlg,
    .metatiles = gMetatiles_Building_Frlg,
    .metatileAttributes = gMetatileAttributes_Building_Frlg,
    .callback = NULL,
};

const struct Tileset gTileset_General_Frlg =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_General_Frlg,
    .palettes = gTilesetPalettes_General_Frlg,
    .metatiles = gMetatiles_General_Frlg,
    .metatileAttributes = gMetatileAttributes_General_Frlg,
    .callback = InitTilesetAnim_General_Frlg,
};

const struct Tileset gTileset_PalletTown =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PalletTown,
    .palettes = gTilesetPalettes_PalletTown,
    .metatiles = gMetatiles_PalletTown,
    .metatileAttributes = gMetatileAttributes_PalletTown,
    .callback = NULL,
};

const struct Tileset gTileset_ViridianCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_ViridianCity,
    .palettes = gTilesetPalettes_ViridianCity,
    .metatiles = gMetatiles_ViridianCity,
    .metatileAttributes = gMetatileAttributes_ViridianCity,
    .callback = NULL,
};

const struct Tileset gTileset_PewterCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PewterCity,
    .palettes = gTilesetPalettes_PewterCity,
    .metatiles = gMetatiles_PewterCity,
    .metatileAttributes = gMetatileAttributes_PewterCity,
    .callback = NULL,
};

const struct Tileset gTileset_CeruleanCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CeruleanCity,
    .palettes = gTilesetPalettes_CeruleanCity,
    .metatiles = gMetatiles_CeruleanCity,
    .metatileAttributes = gMetatileAttributes_CeruleanCity,
    .callback = NULL,
};

const struct Tileset gTileset_LavenderTown =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LavenderTown,
    .palettes = gTilesetPalettes_LavenderTown,
    .metatiles = gMetatiles_LavenderTown,
    .metatileAttributes = gMetatileAttributes_LavenderTown,
    .callback = NULL,
};

const struct Tileset gTileset_VermilionCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_VermilionCity,
    .palettes = gTilesetPalettes_VermilionCity,
    .metatiles = gMetatiles_VermilionCity,
    .metatileAttributes = gMetatileAttributes_VermilionCity,
    .callback = NULL,
};

const struct Tileset gTileset_CeladonCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CeladonCity,
    .palettes = gTilesetPalettes_CeladonCity,
    .metatiles = gMetatiles_CeladonCity,
    .metatileAttributes = gMetatileAttributes_CeladonCity,
    .callback = InitTilesetAnim_CeladonCity,
};

const struct Tileset gTileset_FuchsiaCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_FuchsiaCity,
    .palettes = gTilesetPalettes_FuchsiaCity,
    .metatiles = gMetatiles_FuchsiaCity,
    .metatileAttributes = gMetatileAttributes_FuchsiaCity,
    .callback = NULL,
};

const struct Tileset gTileset_CinnabarIsland =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CinnabarIsland,
    .palettes = gTilesetPalettes_CinnabarIsland,
    .metatiles = gMetatiles_CinnabarIsland,
    .metatileAttributes = gMetatileAttributes_CinnabarIsland,
    .callback = NULL,
};

const struct Tileset gTileset_IndigoPlateau =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_IndigoPlateau,
    .palettes = gTilesetPalettes_IndigoPlateau,
    .metatiles = gMetatiles_IndigoPlateau,
    .metatileAttributes = gMetatileAttributes_IndigoPlateau,
    .callback = NULL,
};

const struct Tileset gTileset_SaffronCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SaffronCity,
    .palettes = gTilesetPalettes_SaffronCity,
    .metatiles = gMetatiles_SaffronCity,
    .metatileAttributes = gMetatileAttributes_SaffronCity,
    .callback = NULL,
};

const struct Tileset gTileset_Mart =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Mart,
    .palettes = gTilesetPalettes_Mart,
    .metatiles = gMetatiles_Mart,
    .metatileAttributes = gMetatileAttributes_Mart,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonCenterFrlg =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonCenter_Frlg,
    .palettes = gTilesetPalettes_PokemonCenter_Frlg,
    .metatiles = gMetatiles_PokemonCenter_Frlg,
    .metatileAttributes = gMetatileAttributes_PokemonCenter_Frlg,
    .callback = NULL,
};

const struct Tileset gTileset_Cave_Frlg =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Cave_Frlg,
    .palettes = gTilesetPalettes_Cave_Frlg,
    .metatiles = gMetatiles_Cave_Frlg,
    .metatileAttributes = gMetatileAttributes_Cave_Frlg,
    .callback = NULL,
};

const struct Tileset gTileset_Museum =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Museum,
    .palettes = gTilesetPalettes_Museum,
    .metatiles = gMetatiles_Museum,
    .metatileAttributes = gMetatileAttributes_Museum,
    .callback = NULL,
};

const struct Tileset gTileset_CableClub_Frlg =
{
    .isCompressed = FALSE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CableClub_Frlg,
    .palettes = gTilesetPalettes_CableClub_Frlg,
    .metatiles = gMetatiles_CableClub_Frlg,
    .metatileAttributes = gMetatileAttributes_CableClub_Frlg,
    .callback = NULL,
};

const struct Tileset gTileset_BikeShop_Frlg =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BikeShop_Frlg,
    .palettes = gTilesetPalettes_BikeShop_Frlg,
    .metatiles = gMetatiles_BikeShop_Frlg,
    .metatileAttributes = gMetatileAttributes_BikeShop_Frlg,
    .callback = NULL,
};

const struct Tileset gTileset_GenericBuilding1 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GenericBuilding1,
    .palettes = gTilesetPalettes_GenericBuilding1,
    .metatiles = gMetatiles_GenericBuilding1,
    .metatileAttributes = gMetatileAttributes_GenericBuilding1,
    .callback = NULL,
};

const struct Tileset gTileset_Lab_Frlg =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Lab_Frlg,
    .palettes = gTilesetPalettes_Lab_Frlg,
    .metatiles = gMetatiles_Lab_Frlg,
    .metatileAttributes = gMetatileAttributes_Lab_Frlg,
    .callback = NULL,
};

const struct Tileset gTileset_FuchsiaGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_FuchsiaGym,
    .palettes = gTilesetPalettes_FuchsiaGym,
    .metatiles = gMetatiles_FuchsiaGym,
    .metatileAttributes = gMetatileAttributes_FuchsiaGym,
    .callback = NULL,
};

const struct Tileset gTileset_ViridianGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_ViridianGym,
    .palettes = gTilesetPalettes_ViridianGym,
    .metatiles = gMetatiles_ViridianGym,
    .metatileAttributes = gMetatileAttributes_ViridianGym,
    .callback = NULL,
};

const struct Tileset gTileset_HoennBuilding =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_HoennBuilding,
    .palettes = gTilesetPalettes_HoennBuilding,
    .metatiles = gMetatiles_HoennBuilding,
    .metatileAttributes = gMetatileAttributes_HoennBuilding,
    .callback = NULL,
};

const struct Tileset gTileset_GameCorner =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GameCorner,
    .palettes = gTilesetPalettes_GameCorner,
    .metatiles = gMetatiles_GameCorner,
    .metatileAttributes = gMetatileAttributes_GameCorner,
    .callback = NULL,
};

const struct Tileset gTileset_PewterGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PewterGym,
    .palettes = gTilesetPalettes_PewterGym,
    .metatiles = gMetatiles_PewterGym,
    .metatileAttributes = gMetatileAttributes_PewterGym,
    .callback = NULL,
};

const struct Tileset gTileset_CeruleanGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CeruleanGym,
    .palettes = gTilesetPalettes_CeruleanGym,
    .metatiles = gMetatiles_CeruleanGym,
    .metatileAttributes = gMetatileAttributes_CeruleanGym,
    .callback = NULL,
};

const struct Tileset gTileset_VermilionGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_VermilionGym,
    .palettes = gTilesetPalettes_VermilionGym,
    .metatiles = gMetatiles_VermilionGym,
    .metatileAttributes = gMetatileAttributes_VermilionGym,
    .callback = InitTilesetAnim_VermilionGym,
};

const struct Tileset gTileset_CeladonGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CeladonGym,
    .palettes = gTilesetPalettes_CeladonGym,
    .metatiles = gMetatiles_CeladonGym,
    .metatileAttributes = gMetatileAttributes_CeladonGym,
    .callback = InitTilesetAnim_CeladonGym,
};

const struct Tileset gTileset_SaffronGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SaffronGym,
    .palettes = gTilesetPalettes_SaffronGym,
    .metatiles = gMetatiles_SaffronGym,
    .metatileAttributes = gMetatileAttributes_SaffronGym,
    .callback = NULL,
};

const struct Tileset gTileset_CinnabarGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CinnabarGym,
    .palettes = gTilesetPalettes_CinnabarGym,
    .metatiles = gMetatiles_CinnabarGym,
    .metatileAttributes = gMetatileAttributes_CinnabarGym,
    .callback = NULL,
};

const struct Tileset gTileset_SSAnne =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SSAnne,
    .palettes = gTilesetPalettes_SSAnne,
    .metatiles = gMetatiles_SSAnne,
    .metatileAttributes = gMetatileAttributes_SSAnne,
    .callback = NULL,
};

const struct Tileset gTileset_ViridianForest =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_ViridianForest,
    .palettes = gTilesetPalettes_ViridianForest,
    .metatiles = gMetatiles_ViridianForest,
    .metatileAttributes = gMetatileAttributes_ViridianForest,
    .callback = NULL,
};

const struct Tileset gTileset_UnusedGatehouse1 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnusedGatehouse1,
    .palettes = gTilesetPalettes_UnusedGatehouse1,
    .metatiles = gMetatiles_UnusedGatehouse1,
    .metatileAttributes = gMetatileAttributes_UnusedGatehouse1,
    .callback = NULL,
};

const struct Tileset gTileset_RockTunnel =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_RockTunnel,
    .palettes = gTilesetPalettes_RockTunnel,
    .metatiles = gMetatiles_RockTunnel,
    .metatileAttributes = gMetatileAttributes_RockTunnel,
    .callback = NULL,
};

const struct Tileset gTileset_DiglettsCave =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_DiglettsCave,
    .palettes = gTilesetPalettes_DiglettsCave,
    .metatiles = gMetatiles_DiglettsCave,
    .metatileAttributes = gMetatileAttributes_DiglettsCave,
    .callback = NULL,
};

const struct Tileset gTileset_SeafoamIslands =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SeafoamIslands,
    .palettes = gTilesetPalettes_SeafoamIslands,
    .metatiles = gMetatiles_SeafoamIslands,
    .metatileAttributes = gMetatileAttributes_SeafoamIslands,
    .callback = NULL,
};

const struct Tileset gTileset_UnusedGatehouse2 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnusedGatehouse2,
    .palettes = gTilesetPalettes_UnusedGatehouse2,
    .metatiles = gMetatiles_UnusedGatehouse2,
    .metatileAttributes = gMetatileAttributes_UnusedGatehouse2,
    .callback = NULL,
};

const struct Tileset gTileset_CeruleanCave =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CeruleanCave,
    .palettes = gTilesetPalettes_CeruleanCave,
    .metatiles = gMetatiles_CeruleanCave,
    .metatileAttributes = gMetatileAttributes_CeruleanCave,
    .callback = NULL,
};

const struct Tileset gTileset_DepartmentStore =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_DepartmentStore,
    .palettes = gTilesetPalettes_DepartmentStore,
    .metatiles = gMetatiles_DepartmentStore,
    .metatileAttributes = gMetatileAttributes_DepartmentStore,
    .callback = NULL,
};

const struct Tileset gTileset_GenericBuilding2 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GenericBuilding2,
    .palettes = gTilesetPalettes_GenericBuilding2,
    .metatiles = gMetatiles_GenericBuilding2,
    .metatileAttributes = gMetatileAttributes_GenericBuilding2,
    .callback = NULL,
};

const struct Tileset gTileset_PowerPlant =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PowerPlant,
    .palettes = gTilesetPalettes_PowerPlant,
    .metatiles = gMetatiles_PowerPlant,
    .metatileAttributes = gMetatileAttributes_PowerPlant,
    .callback = NULL,
};

const struct Tileset gTileset_SeaCottage =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SeaCottage,
    .palettes = gTilesetPalettes_SeaCottage,
    .metatiles = gMetatiles_SeaCottage,
    .metatileAttributes = gMetatileAttributes_SeaCottage,
    .callback = NULL,
};

const struct Tileset gTileset_SilphCo =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Condominiums,
    .palettes = gTilesetPalettes_Condominiums,
    .metatiles = gMetatiles_SilphCo,
    .metatileAttributes = gMetatileAttributes_SilphCo,
    .callback = InitTilesetAnim_SilphCo,
};

const struct Tileset gTileset_UndergroundPath =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UndergroundPath,
    .palettes = gTilesetPalettes_UndergroundPath,
    .metatiles = gMetatiles_UndergroundPath,
    .metatileAttributes = gMetatileAttributes_UndergroundPath,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonTower =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonTower,
    .palettes = gTilesetPalettes_PokemonTower,
    .metatiles = gMetatiles_PokemonTower,
    .metatileAttributes = gMetatileAttributes_PokemonTower,
    .callback = NULL,
};

const struct Tileset gTileset_SafariZoneBuilding =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SafariZoneBuilding,
    .palettes = gTilesetPalettes_SafariZoneBuilding,
    .metatiles = gMetatiles_SafariZoneBuilding,
    .metatileAttributes = gMetatileAttributes_SafariZoneBuilding,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonMansion =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonMansion,
    .palettes = gTilesetPalettes_PokemonMansion,
    .metatiles = gMetatiles_PokemonMansion,
    .metatileAttributes = gMetatileAttributes_PokemonMansion,
    .callback = NULL,
};

const struct Tileset gTileset_RestaurantHotel =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_RestaurantHotel,
    .palettes = gTilesetPalettes_RestaurantHotel,
    .metatiles = gMetatiles_RestaurantHotel,
    .metatileAttributes = gMetatileAttributes_RestaurantHotel,
    .callback = NULL,
};

const struct Tileset gTileset_School =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_School,
    .palettes = gTilesetPalettes_School,
    .metatiles = gMetatiles_School,
    .metatileAttributes = gMetatileAttributes_School,
    .callback = NULL,
};

const struct Tileset gTileset_FanClubDaycare =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_FanClubDaycare,
    .palettes = gTilesetPalettes_FanClubDaycare,
    .metatiles = gMetatiles_FanClubDaycare,
    .metatileAttributes = gMetatileAttributes_FanClubDaycare,
    .callback = NULL,
};

const struct Tileset gTileset_Condominiums =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Condominiums,
    .palettes = gTilesetPalettes_Condominiums,
    .metatiles = gMetatiles_Condominiums,
    .metatileAttributes = gMetatileAttributes_Condominiums,
    .callback = NULL,
};

const struct Tileset gTileset_BurgledHouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BurgledHouse,
    .palettes = gTilesetPalettes_BurgledHouse,
    .metatiles = gMetatiles_BurgledHouse,
    .metatileAttributes = gMetatileAttributes_BurgledHouse,
    .callback = NULL,
};

const struct Tileset gTileset_MtEmber =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MtEmber,
    .palettes = gTilesetPalettes_MtEmber,
    .metatiles = gMetatiles_MtEmber,
    .metatileAttributes = gMetatileAttributes_MtEmber,
    .callback = InitTilesetAnim_MtEmber,
};

const struct Tileset gTileset_BerryForest =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BerryForest,
    .palettes = gTilesetPalettes_BerryForest,
    .metatiles = gMetatiles_BerryForest,
    .metatileAttributes = gMetatileAttributes_BerryForest,
    .callback = NULL,
};

const struct Tileset gTileset_NavelRock_Frlg =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_NavelRock_Frlg,
    .palettes = gTilesetPalettes_NavelRock_Frlg,
    .metatiles = gMetatiles_NavelRock_Frlg,
    .metatileAttributes = gMetatileAttributes_NavelRock_Frlg,
    .callback = NULL,
};

const struct Tileset gTileset_TanobyRuins =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_TanobyRuins,
    .palettes = gTilesetPalettes_TanobyRuins,
    .metatiles = gMetatiles_TanobyRuins,
    .metatileAttributes = gMetatileAttributes_TanobyRuins,
    .callback = NULL,
};

const struct Tileset gTileset_SeviiIslands123 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SeviiIslands123,
    .palettes = gTilesetPalettes_SeviiIslands123,
    .metatiles = gMetatiles_SeviiIslands123,
    .metatileAttributes = gMetatileAttributes_SeviiIslands123,
    .callback = NULL,
};

const struct Tileset gTileset_SeviiIslands45 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SeviiIslands45,
    .palettes = gTilesetPalettes_SeviiIslands45,
    .metatiles = gMetatiles_SeviiIslands45,
    .metatileAttributes = gMetatileAttributes_SeviiIslands45,
    .callback = NULL,
};

const struct Tileset gTileset_SeviiIslands67 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SeviiIslands67,
    .palettes = gTilesetPalettes_SeviiIslands67,
    .metatiles = gMetatiles_SeviiIslands67,
    .metatileAttributes = gMetatileAttributes_SeviiIslands67,
    .callback = NULL,
};

const struct Tileset gTileset_TrainerTower =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_TrainerTower,
    .palettes = gTilesetPalettes_TrainerTower,
    .metatiles = gMetatiles_TrainerTower,
    .metatileAttributes = gMetatileAttributes_TrainerTower,
    .callback = NULL,
};

const struct Tileset gTileset_IslandHarbor_Frlg =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_IslandHarbor_Frlg,
    .palettes = gTilesetPalettes_IslandHarbor_Frlg,
    .metatiles = gMetatiles_IslandHarbor_Frlg,
    .metatileAttributes = gMetatileAttributes_IslandHarbor_Frlg,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonLeague =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonLeague,
    .palettes = gTilesetPalettes_PokemonLeague,
    .metatiles = gMetatiles_PokemonLeague,
    .metatileAttributes = gMetatileAttributes_PokemonLeague,
    .callback = NULL,
};

const struct Tileset gTileset_HallOfFame =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_HallOfFame,
    .palettes = gTilesetPalettes_HallOfFame,
    .metatiles = gMetatiles_HallOfFame,
    .metatileAttributes = gMetatileAttributes_HallOfFame,
    .callback = NULL,
};

// (antes: #endif de #if !IS_FRLG)

// ---- tilesets de Johto (dev_scripts/importa_tilesets_johto.py) ----
const struct Tileset gTileset_AzaleaTown =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_AzaleaTown,
    .palettes = gTilesetPalettes_AzaleaTown,
    .metatiles = gMetatiles_AzaleaTown,
    .metatileAttributes = gMetatileAttributes_AzaleaTown,
    .callback = NULL,
};

const struct Tileset gTileset_AzaleaTownGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_AzaleaTownGym,
    .palettes = gTilesetPalettes_AzaleaTownGym,
    .metatiles = gMetatiles_AzaleaTownGym,
    .metatileAttributes = gMetatileAttributes_AzaleaTownGym,
    .callback = NULL,
};

const struct Tileset gTileset_Barn =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Barn,
    .palettes = gTilesetPalettes_Barn,
    .metatiles = gMetatiles_Barn,
    .metatileAttributes = gMetatileAttributes_Barn,
    .callback = NULL,
};

const struct Tileset gTileset_BattleTowerOuter =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleTowerOuter,
    .palettes = gTilesetPalettes_BattleTowerOuter,
    .metatiles = gMetatiles_BattleTowerOuter,
    .metatileAttributes = gMetatileAttributes_BattleTowerOuter,
    .callback = NULL,
};

const struct Tileset gTileset_BellchimeTrail =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BellchimeTrail,
    .palettes = gTilesetPalettes_BellchimeTrail,
    .metatiles = gMetatiles_BellchimeTrail,
    .metatileAttributes = gMetatileAttributes_BellchimeTrail,
    .callback = NULL,
};

const struct Tileset gTileset_BikeShopJohto =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BikeShopJohto,
    .palettes = gTilesetPalettes_BikeShopJohto,
    .metatiles = gMetatiles_BikeShopJohto,
    .metatileAttributes = gMetatileAttributes_BikeShopJohto,
    .callback = NULL,
};

const struct Tileset gTileset_Blackthorn =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Blackthorn,
    .palettes = gTilesetPalettes_Blackthorn,
    .metatiles = gMetatiles_Blackthorn,
    .metatileAttributes = gMetatileAttributes_Blackthorn,
    .callback = NULL,
};

const struct Tileset gTileset_BlackthornGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BlackthornGym,
    .palettes = gTilesetPalettes_BlackthornGym,
    .metatiles = gMetatiles_BlackthornGym,
    .metatileAttributes = gMetatileAttributes_BlackthornGym,
    .callback = NULL,
};

const struct Tileset gTileset_BurnedTower =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BurnedTower,
    .palettes = gTilesetPalettes_BurnedTower,
    .metatiles = gMetatiles_BurnedTower,
    .metatileAttributes = gMetatileAttributes_BurnedTower,
    .callback = NULL,
};

const struct Tileset gTileset_Cafe =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Cafe,
    .palettes = gTilesetPalettes_Cafe,
    .metatiles = gMetatiles_Cafe,
    .metatileAttributes = gMetatileAttributes_Cafe,
    .callback = NULL,
};

const struct Tileset gTileset_CaveDefault =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CaveDefault,
    .palettes = gTilesetPalettes_CaveDefault,
    .metatiles = gMetatiles_CaveDefault,
    .metatileAttributes = gMetatileAttributes_CaveDefault,
    .callback = NULL,
};

const struct Tileset gTileset_CaveDragonsDen =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CaveDragonsDen,
    .palettes = gTilesetPalettes_CaveDragonsDen,
    .metatiles = gMetatiles_CaveDragonsDen,
    .metatileAttributes = gMetatileAttributes_CaveDragonsDen,
    .callback = NULL,
};

const struct Tileset gTileset_CaveGray =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CaveGray,
    .palettes = gTilesetPalettes_CaveGray,
    .metatiles = gMetatiles_CaveGray,
    .metatileAttributes = gMetatileAttributes_CaveGray,
    .callback = NULL,
};

const struct Tileset gTileset_CaveIce =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CaveIce,
    .palettes = gTilesetPalettes_CaveIce,
    .metatiles = gMetatiles_CaveIce,
    .metatileAttributes = gMetatileAttributes_CaveIce,
    .callback = NULL,
};

const struct Tileset gTileset_CaveSandy =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CaveSandy,
    .palettes = gTilesetPalettes_CaveSandy,
    .metatiles = gMetatiles_CaveSandy,
    .metatileAttributes = gMetatileAttributes_CaveSandy,
    .callback = NULL,
};

const struct Tileset gTileset_CherrygroveCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CherrygroveCity,
    .palettes = gTilesetPalettes_CherrygroveCity,
    .metatiles = gMetatiles_CherrygroveCity,
    .metatileAttributes = gMetatileAttributes_CherrygroveCity,
    .callback = NULL,
};

const struct Tileset gTileset_CianwoodCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CianwoodCity,
    .palettes = gTilesetPalettes_CianwoodCity,
    .metatiles = gMetatiles_CianwoodCity,
    .metatileAttributes = gMetatileAttributes_CianwoodCity,
    .callback = NULL,
};

const struct Tileset gTileset_CianwoodCityGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_CianwoodCityGym,
    .palettes = gTilesetPalettes_CianwoodCityGym,
    .metatiles = gMetatiles_CianwoodCityGym,
    .metatileAttributes = gMetatileAttributes_CianwoodCityGym,
    .callback = NULL,
};

const struct Tileset gTileset_DepartmentStoreJohto =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_DepartmentStoreJohto,
    .palettes = gTilesetPalettes_DepartmentStoreJohto,
    .metatiles = gMetatiles_DepartmentStoreJohto,
    .metatileAttributes = gMetatileAttributes_DepartmentStoreJohto,
    .callback = NULL,
};

const struct Tileset gTileset_DragonsDenShrine =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_DragonsDenShrine,
    .palettes = gTilesetPalettes_DragonsDenShrine,
    .metatiles = gMetatiles_DragonsDenShrine,
    .metatileAttributes = gMetatileAttributes_DragonsDenShrine,
    .callback = NULL,
};

const struct Tileset gTileset_EcruteakCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_EcruteakCity,
    .palettes = gTilesetPalettes_EcruteakCity,
    .metatiles = gMetatiles_EcruteakCity,
    .metatileAttributes = gMetatileAttributes_EcruteakCity,
    .callback = NULL,
};

const struct Tileset gTileset_EcruteakCityGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_EcruteakCityGym,
    .palettes = gTilesetPalettes_EcruteakCityGym,
    .metatiles = gMetatiles_EcruteakCityGym,
    .metatileAttributes = gMetatileAttributes_EcruteakCityGym,
    .callback = NULL,
};

const struct Tileset gTileset_EcruteakTheater =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_EcruteakTheater,
    .palettes = gTilesetPalettes_EcruteakTheater,
    .metatiles = gMetatiles_EcruteakTheater,
    .metatileAttributes = gMetatileAttributes_EcruteakTheater,
    .callback = NULL,
};

const struct Tileset gTileset_GameCornerJohto =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GameCornerJohto,
    .palettes = gTilesetPalettes_GameCornerJohto,
    .metatiles = gMetatiles_GameCornerJohto,
    .metatileAttributes = gMetatileAttributes_GameCornerJohto,
    .callback = NULL,
};

const struct Tileset gTileset_GateStandard =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GateStandard,
    .palettes = gTilesetPalettes_GateStandard,
    .metatiles = gMetatiles_GateStandard,
    .metatileAttributes = gMetatileAttributes_GateStandard,
    .callback = NULL,
};

const struct Tileset gTileset_Goldenrod =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Goldenrod,
    .palettes = gTilesetPalettes_Goldenrod,
    .metatiles = gMetatiles_Goldenrod,
    .metatileAttributes = gMetatileAttributes_Goldenrod,
    .callback = NULL,
};

const struct Tileset gTileset_GoldenrodStation =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GoldenrodStation,
    .palettes = gTilesetPalettes_GoldenrodStation,
    .metatiles = gMetatiles_GoldenrodStation,
    .metatileAttributes = gMetatileAttributes_GoldenrodStation,
    .callback = NULL,
};

const struct Tileset gTileset_GoldenrodUndergroundRocket =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GoldenrodUndergroundRocket,
    .palettes = gTilesetPalettes_GoldenrodUndergroundRocket,
    .metatiles = gMetatiles_GoldenrodUndergroundRocket,
    .metatileAttributes = gMetatileAttributes_GoldenrodUndergroundRocket,
    .callback = NULL,
};

const struct Tileset gTileset_GoldenrodUndergroundStorage =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GoldenrodUndergroundStorage,
    .palettes = gTilesetPalettes_GoldenrodUndergroundStorage,
    .metatiles = gMetatiles_GoldenrodUndergroundStorage,
    .metatileAttributes = gMetatileAttributes_GoldenrodUndergroundStorage,
    .callback = NULL,
};

const struct Tileset gTileset_GoldenrodUndergroundTunnel =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_GoldenrodUndergroundTunnel,
    .palettes = gTilesetPalettes_GoldenrodUndergroundTunnel,
    .metatiles = gMetatiles_GoldenrodUndergroundTunnel,
    .metatileAttributes = gMetatileAttributes_GoldenrodUndergroundTunnel,
    .callback = NULL,
};

const struct Tileset gTileset_House2 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_House2,
    .palettes = gTilesetPalettes_House2,
    .metatiles = gMetatiles_House2,
    .metatileAttributes = gMetatileAttributes_House2,
    .callback = NULL,
};

const struct Tileset gTileset_HouseLab =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_HouseLab,
    .palettes = gTilesetPalettes_HouseLab,
    .metatiles = gMetatiles_HouseLab,
    .metatileAttributes = gMetatileAttributes_HouseLab,
    .callback = NULL,
};

const struct Tileset gTileset_IlexForest =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_IlexForest,
    .palettes = gTilesetPalettes_IlexForest,
    .metatiles = gMetatiles_IlexForest,
    .metatileAttributes = gMetatileAttributes_IlexForest,
    .callback = NULL,
};

const struct Tileset gTileset_JohtoBikeShop =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_JohtoBikeShop,
    .palettes = gTilesetPalettes_JohtoBikeShop,
    .metatiles = gMetatiles_JohtoBikeShop,
    .metatileAttributes = gMetatileAttributes_JohtoBikeShop,
    .callback = NULL,
};

const struct Tileset gTileset_JohtoBuilding =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_JohtoBuilding,
    .palettes = gTilesetPalettes_JohtoBuilding,
    .metatiles = gMetatiles_JohtoBuilding,
    .metatileAttributes = gMetatileAttributes_JohtoBuilding,
    .callback = NULL,
};

const struct Tileset gTileset_JohtoGeneral =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_JohtoGeneral,
    .palettes = gTilesetPalettes_JohtoGeneral,
    .metatiles = gMetatiles_JohtoGeneral,
    .metatileAttributes = gMetatileAttributes_JohtoGeneral,
    .callback = NULL,
};

const struct Tileset gTileset_JohtoMart =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_JohtoMart,
    .palettes = gTilesetPalettes_JohtoMart,
    .metatiles = gMetatiles_JohtoMart,
    .metatileAttributes = gMetatileAttributes_JohtoMart,
    .callback = NULL,
};

const struct Tileset gTileset_JohtoNorthEast =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_JohtoNorthEast,
    .palettes = gTilesetPalettes_JohtoNorthEast,
    .metatiles = gMetatiles_JohtoNorthEast,
    .metatileAttributes = gMetatileAttributes_JohtoNorthEast,
    .callback = NULL,
};

const struct Tileset gTileset_JohtoNorthWest =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_JohtoNorthWest,
    .palettes = gTilesetPalettes_JohtoNorthWest,
    .metatiles = gMetatiles_JohtoNorthWest,
    .metatileAttributes = gMetatileAttributes_JohtoNorthWest,
    .callback = NULL,
};

const struct Tileset gTileset_JohtoSouth =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_JohtoSouth,
    .palettes = gTilesetPalettes_JohtoSouth,
    .metatiles = gMetatiles_JohtoSouth,
    .metatileAttributes = gMetatileAttributes_JohtoSouth,
    .callback = NULL,
};

const struct Tileset gTileset_KantoGeneral =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_KantoGeneral,
    .palettes = gTilesetPalettes_KantoGeneral,
    .metatiles = gMetatiles_KantoGeneral,
    .metatileAttributes = gMetatileAttributes_KantoGeneral,
    .callback = NULL,
};

const struct Tileset gTileset_KantoPokemonCenter =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_KantoPokemonCenter,
    .palettes = gTilesetPalettes_KantoPokemonCenter,
    .metatiles = gMetatiles_KantoPokemonCenter,
    .metatileAttributes = gMetatileAttributes_KantoPokemonCenter,
    .callback = NULL,
};

const struct Tileset gTileset_KurtsHouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_KurtsHouse,
    .palettes = gTilesetPalettes_KurtsHouse,
    .metatiles = gMetatiles_KurtsHouse,
    .metatileAttributes = gMetatileAttributes_KurtsHouse,
    .callback = NULL,
};

const struct Tileset gTileset_Lighthouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Lighthouse,
    .palettes = gTilesetPalettes_Lighthouse,
    .metatiles = gMetatiles_Lighthouse,
    .metatileAttributes = gMetatileAttributes_Lighthouse,
    .callback = NULL,
};

const struct Tileset gTileset_MahoganyTown =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MahoganyTown,
    .palettes = gTilesetPalettes_MahoganyTown,
    .metatiles = gMetatiles_MahoganyTown,
    .metatileAttributes = gMetatileAttributes_MahoganyTown,
    .callback = NULL,
};

const struct Tileset gTileset_MtSilverSnow =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MtSilverSnow,
    .palettes = gTilesetPalettes_MtSilverSnow,
    .metatiles = gMetatiles_MtSilverSnow,
    .metatileAttributes = gMetatileAttributes_MtSilverSnow,
    .callback = NULL,
};

const struct Tileset gTileset_NationalPark =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_NationalPark,
    .palettes = gTilesetPalettes_NationalPark,
    .metatiles = gMetatiles_NationalPark,
    .metatileAttributes = gMetatileAttributes_NationalPark,
    .callback = NULL,
};

const struct Tileset gTileset_NewBarkTown =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_NewBarkTown,
    .palettes = gTilesetPalettes_NewBarkTown,
    .metatiles = gMetatiles_NewBarkTown,
    .metatileAttributes = gMetatileAttributes_NewBarkTown,
    .callback = NULL,
};

const struct Tileset gTileset_OlivineCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_OlivineCity,
    .palettes = gTilesetPalettes_OlivineCity,
    .metatiles = gMetatiles_OlivineCity,
    .metatileAttributes = gMetatileAttributes_OlivineCity,
    .callback = NULL,
};

const struct Tileset gTileset_PlayersHouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PlayersHouse,
    .palettes = gTilesetPalettes_PlayersHouse,
    .metatiles = gMetatiles_PlayersHouse,
    .metatileAttributes = gMetatileAttributes_PlayersHouse,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonCenterWhite =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonCenterWhite,
    .palettes = gTilesetPalettes_PokemonCenterWhite,
    .metatiles = gMetatiles_PokemonCenterWhite,
    .metatileAttributes = gMetatileAttributes_PokemonCenterWhite,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonDayCareJohto =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonDayCareJohto,
    .palettes = gTilesetPalettes_PokemonDayCareJohto,
    .metatiles = gMetatiles_PokemonDayCareJohto,
    .metatileAttributes = gMetatileAttributes_PokemonDayCareJohto,
    .callback = NULL,
};

const struct Tileset gTileset_PortIndoor =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PortIndoor,
    .palettes = gTilesetPalettes_PortIndoor,
    .metatiles = gMetatiles_PortIndoor,
    .metatileAttributes = gMetatileAttributes_PortIndoor,
    .callback = NULL,
};

const struct Tileset gTileset_PowerPlantGeneratorRoom =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PowerPlantGeneratorRoom,
    .palettes = gTilesetPalettes_PowerPlantGeneratorRoom,
    .metatiles = gMetatiles_PowerPlantGeneratorRoom,
    .metatileAttributes = gMetatileAttributes_PowerPlantGeneratorRoom,
    .callback = NULL,
};

const struct Tileset gTileset_Route32 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Route32,
    .palettes = gTilesetPalettes_Route32,
    .metatiles = gMetatiles_Route32,
    .metatileAttributes = gMetatileAttributes_Route32,
    .callback = NULL,
};

const struct Tileset gTileset_Route38Farmland =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Route38Farmland,
    .palettes = gTilesetPalettes_Route38Farmland,
    .metatiles = gMetatiles_Route38Farmland,
    .metatileAttributes = gMetatileAttributes_Route38Farmland,
    .callback = NULL,
};

const struct Tileset gTileset_RuinsOfAlphB1F =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_RuinsOfAlphB1F,
    .palettes = gTilesetPalettes_RuinsOfAlphB1F,
    .metatiles = gMetatiles_RuinsOfAlphB1F,
    .metatileAttributes = gMetatileAttributes_RuinsOfAlphB1F,
    .callback = NULL,
};

const struct Tileset gTileset_RuinsOfAlphOutside =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_RuinsOfAlphOutside,
    .palettes = gTilesetPalettes_RuinsOfAlphOutside,
    .metatiles = gMetatiles_RuinsOfAlphOutside,
    .metatileAttributes = gMetatileAttributes_RuinsOfAlphOutside,
    .callback = NULL,
};

const struct Tileset gTileset_RuinsOfAlphWriting =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_RuinsOfAlphWriting,
    .palettes = gTilesetPalettes_RuinsOfAlphWriting,
    .metatiles = gMetatiles_RuinsOfAlphWriting,
    .metatileAttributes = gMetatileAttributes_RuinsOfAlphWriting,
    .callback = NULL,
};

const struct Tileset gTileset_SafariZoneEntrance =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SafariZoneEntrance,
    .palettes = gTilesetPalettes_SafariZoneEntrance,
    .metatiles = gMetatiles_SafariZoneEntrance,
    .metatileAttributes = gMetatileAttributes_SafariZoneEntrance,
    .callback = NULL,
};

const struct Tileset gTileset_SafariZoneJohto =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SafariZoneJohto,
    .palettes = gTilesetPalettes_SafariZoneJohto,
    .metatiles = gMetatiles_SafariZoneJohto,
    .metatileAttributes = gMetatileAttributes_SafariZoneJohto,
    .callback = NULL,
};

const struct Tileset gTileset_ShopRooftop =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_ShopRooftop,
    .palettes = gTilesetPalettes_ShopRooftop,
    .metatiles = gMetatiles_ShopRooftop,
    .metatileAttributes = gMetatileAttributes_ShopRooftop,
    .callback = NULL,
};

const struct Tileset gTileset_SootopolisGymJohto =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SootopolisGymJohto,
    .palettes = gTilesetPalettes_SootopolisGymJohto,
    .metatiles = gMetatiles_SootopolisGymJohto,
    .metatileAttributes = gMetatileAttributes_SootopolisGymJohto,
    .callback = NULL,
};

const struct Tileset gTileset_Ssaqua =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Ssaqua,
    .palettes = gTilesetPalettes_Ssaqua,
    .metatiles = gMetatiles_Ssaqua,
    .metatileAttributes = gMetatileAttributes_Ssaqua,
    .callback = NULL,
};

const struct Tileset gTileset_TrainerSchool =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_TrainerSchool,
    .palettes = gTilesetPalettes_TrainerSchool,
    .metatiles = gMetatiles_TrainerSchool,
    .metatileAttributes = gMetatileAttributes_TrainerSchool,
    .callback = NULL,
};

const struct Tileset gTileset_VioletCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_VioletCity,
    .palettes = gTilesetPalettes_VioletCity,
    .metatiles = gMetatiles_VioletCity,
    .metatileAttributes = gMetatileAttributes_VioletCity,
    .callback = NULL,
};

const struct Tileset gTileset_ViridianCityJohto =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_ViridianCityJohto,
    .palettes = gTilesetPalettes_ViridianCityJohto,
    .metatiles = gMetatiles_ViridianCityJohto,
    .metatileAttributes = gMetatileAttributes_ViridianCityJohto,
    .callback = NULL,
};

const struct Tileset gTileset_WhirlIslands =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_WhirlIslands,
    .palettes = gTilesetPalettes_WhirlIslands,
    .metatiles = gMetatiles_WhirlIslands,
    .metatileAttributes = gMetatileAttributes_WhirlIslands,
    .callback = NULL,
};

// --- Unova (B12.a, tileset_gen2.py) ---

const struct Tileset gTileset_UnovaCastelia =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaCastelia,
    .palettes = gTilesetPalettes_UnovaCastelia,
    .metatiles = gMetatiles_UnovaCastelia,
    .metatileAttributes = gMetatileAttributes_UnovaCastelia,
    .callback = InitTilesetAnim_UnovaCastelia,
};

const struct Tileset gTileset_UnovaNimbasa =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaNimbasa,
    .palettes = gTilesetPalettes_UnovaNimbasa,
    .metatiles = gMetatiles_UnovaNimbasa,
    .metatileAttributes = gMetatileAttributes_UnovaNimbasa,
    .callback = InitTilesetAnim_UnovaNimbasa,
};

const struct Tileset gTileset_UnovaDriftveil =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaDriftveil,
    .palettes = gTilesetPalettes_UnovaDriftveil,
    .metatiles = gMetatiles_UnovaDriftveil,
    .metatileAttributes = gMetatileAttributes_UnovaDriftveil,
    .callback = InitTilesetAnim_UnovaDriftveil,
};

const struct Tileset gTileset_UnovaOpelucid =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaOpelucid,
    .palettes = gTilesetPalettes_UnovaOpelucid,
    .metatiles = gMetatiles_UnovaOpelucid,
    .metatileAttributes = gMetatileAttributes_UnovaOpelucid,
    .callback = InitTilesetAnim_UnovaOpelucid,
};

const struct Tileset gTileset_UnovaTower =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaTower,
    .palettes = gTilesetPalettes_UnovaTower,
    .metatiles = gMetatiles_UnovaTower,
    .metatileAttributes = gMetatileAttributes_UnovaTower,
    .callback = InitTilesetAnim_UnovaTower,
};

const struct Tileset gTileset_UnovaDesert =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaDesert,
    .palettes = gTilesetPalettes_UnovaDesert,
    .metatiles = gMetatiles_UnovaDesert,
    .metatileAttributes = gMetatileAttributes_UnovaDesert,
    .callback = InitTilesetAnim_UnovaDesert,
};

const struct Tileset gTileset_UnovaTraditionalHouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaTraditionalHouse,
    .palettes = gTilesetPalettes_UnovaTraditionalHouse,
    .metatiles = gMetatiles_UnovaTraditionalHouse,
    .metatileAttributes = gMetatileAttributes_UnovaTraditionalHouse,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaForest =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaForest,
    .palettes = gTilesetPalettes_UnovaForest,
    .metatiles = gMetatiles_UnovaForest,
    .metatileAttributes = gMetatileAttributes_UnovaForest,
    .callback = InitTilesetAnim_UnovaForest,
};

const struct Tileset gTileset_UnovaFacility =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaFacility,
    .palettes = gTilesetPalettes_UnovaFacility,
    .metatiles = gMetatiles_UnovaFacility,
    .metatileAttributes = gMetatileAttributes_UnovaFacility,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaComplex =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaComplex,
    .palettes = gTilesetPalettes_UnovaComplex,
    .metatiles = gMetatiles_UnovaComplex,
    .metatileAttributes = gMetatileAttributes_UnovaComplex,
    .callback = InitTilesetAnim_UnovaComplex,
};

const struct Tileset gTileset_UnovaHouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaHouse,
    .palettes = gTilesetPalettes_UnovaHouse,
    .metatiles = gMetatiles_UnovaHouse,
    .metatileAttributes = gMetatileAttributes_UnovaHouse,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaGate =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaGate,
    .palettes = gTilesetPalettes_UnovaGate,
    .metatiles = gMetatiles_UnovaGate,
    .metatileAttributes = gMetatileAttributes_UnovaGate,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaCave =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaCave,
    .palettes = gTilesetPalettes_UnovaCave,
    .metatiles = gMetatiles_UnovaCave,
    .metatileAttributes = gMetatileAttributes_UnovaCave,
    .callback = InitTilesetAnim_UnovaCave,
};

const struct Tileset gTileset_UnovaPokecenter =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaPokecenter,
    .palettes = gTilesetPalettes_UnovaPokecenter,
    .metatiles = gMetatiles_UnovaPokecenter,
    .metatileAttributes = gMetatileAttributes_UnovaPokecenter,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaMansion =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaMansion,
    .palettes = gTilesetPalettes_UnovaMansion,
    .metatiles = gMetatiles_UnovaMansion,
    .metatileAttributes = gMetatileAttributes_UnovaMansion,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaGameCorner =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaGameCorner,
    .palettes = gTilesetPalettes_UnovaGameCorner,
    .metatiles = gMetatiles_UnovaGameCorner,
    .metatileAttributes = gMetatileAttributes_UnovaGameCorner,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaMart =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaMart,
    .palettes = gTilesetPalettes_UnovaMart,
    .metatiles = gMetatiles_UnovaMart,
    .metatileAttributes = gMetatileAttributes_UnovaMart,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaUnovaBeach =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaUnovaBeach,
    .palettes = gTilesetPalettes_UnovaUnovaBeach,
    .metatiles = gMetatiles_UnovaUnovaBeach,
    .metatileAttributes = gMetatileAttributes_UnovaUnovaBeach,
    .callback = InitTilesetAnim_UnovaUnovaBeach,
};

const struct Tileset gTileset_UnovaEliteFourRoom =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaEliteFourRoom,
    .palettes = gTilesetPalettes_UnovaEliteFourRoom,
    .metatiles = gMetatiles_UnovaEliteFourRoom,
    .metatileAttributes = gMetatileAttributes_UnovaEliteFourRoom,
    .callback = InitTilesetAnim_UnovaEliteFourRoom,
};

const struct Tileset gTileset_UnovaPkmnLeague =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaPkmnLeague,
    .palettes = gTilesetPalettes_UnovaPkmnLeague,
    .metatiles = gMetatiles_UnovaPkmnLeague,
    .metatileAttributes = gMetatileAttributes_UnovaPkmnLeague,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaUnovaEast =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaUnovaEast,
    .palettes = gTilesetPalettes_UnovaUnovaEast,
    .metatiles = gMetatiles_UnovaUnovaEast,
    .metatileAttributes = gMetatileAttributes_UnovaUnovaEast,
    .callback = InitTilesetAnim_UnovaUnovaEast,
};

const struct Tileset gTileset_UnovaAirport =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaAirport,
    .palettes = gTilesetPalettes_UnovaAirport,
    .metatiles = gMetatiles_UnovaAirport,
    .metatileAttributes = gMetatileAttributes_UnovaAirport,
    .callback = InitTilesetAnim_UnovaAirport,
};

const struct Tileset gTileset_UnovaIcirrus =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaIcirrus,
    .palettes = gTilesetPalettes_UnovaIcirrus,
    .metatiles = gMetatiles_UnovaIcirrus,
    .metatileAttributes = gMetatileAttributes_UnovaIcirrus,
    .callback = InitTilesetAnim_UnovaIcirrus,
};

const struct Tileset gTileset_UnovaPort =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaPort,
    .palettes = gTilesetPalettes_UnovaPort,
    .metatiles = gMetatiles_UnovaPort,
    .metatileAttributes = gMetatileAttributes_UnovaPort,
    .callback = InitTilesetAnim_UnovaPort,
};

const struct Tileset gTileset_UnovaBattleTower =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaBattleTower,
    .palettes = gTilesetPalettes_UnovaBattleTower,
    .metatiles = gMetatiles_UnovaBattleTower,
    .metatileAttributes = gMetatileAttributes_UnovaBattleTower,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaChampionsRoom =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaChampionsRoom,
    .palettes = gTilesetPalettes_UnovaChampionsRoom,
    .metatiles = gMetatiles_UnovaChampionsRoom,
    .metatileAttributes = gMetatileAttributes_UnovaChampionsRoom,
    .callback = InitTilesetAnim_UnovaChampionsRoom,
};

const struct Tileset gTileset_UnovaUnovaWest =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaUnovaWest,
    .palettes = gTilesetPalettes_UnovaUnovaWest,
    .metatiles = gMetatiles_UnovaUnovaWest,
    .metatileAttributes = gMetatileAttributes_UnovaUnovaWest,
    .callback = InitTilesetAnim_UnovaUnovaWest,
};

const struct Tileset gTileset_UnovaNacrene =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaNacrene,
    .palettes = gTilesetPalettes_UnovaNacrene,
    .metatiles = gMetatiles_UnovaNacrene,
    .metatileAttributes = gMetatileAttributes_UnovaNacrene,
    .callback = InitTilesetAnim_UnovaNacrene,
};

const struct Tileset gTileset_UnovaRadioTower =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaRadioTower,
    .palettes = gTilesetPalettes_UnovaRadioTower,
    .metatiles = gMetatiles_UnovaRadioTower,
    .metatileAttributes = gMetatileAttributes_UnovaRadioTower,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaCaveRuins =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaCaveRuins,
    .palettes = gTilesetPalettes_UnovaCaveRuins,
    .metatiles = gMetatiles_UnovaCaveRuins,
    .metatileAttributes = gMetatileAttributes_UnovaCaveRuins,
    .callback = InitTilesetAnim_UnovaCaveRuins,
};

const struct Tileset gTileset_UnovaDreamyard =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaDreamyard,
    .palettes = gTilesetPalettes_UnovaDreamyard,
    .metatiles = gMetatiles_UnovaDreamyard,
    .metatileAttributes = gMetatileAttributes_UnovaDreamyard,
    .callback = InitTilesetAnim_UnovaDreamyard,
};

const struct Tileset gTileset_UnovaLab =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaLab,
    .palettes = gTilesetPalettes_UnovaLab,
    .metatiles = gMetatiles_UnovaLab,
    .metatileAttributes = gMetatileAttributes_UnovaLab,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaMistralton =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaMistralton,
    .palettes = gTilesetPalettes_UnovaMistralton,
    .metatiles = gMetatiles_UnovaMistralton,
    .metatileAttributes = gMetatileAttributes_UnovaMistralton,
    .callback = InitTilesetAnim_UnovaMistralton,
};

const struct Tileset gTileset_UnovaStriaton =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaStriaton,
    .palettes = gTilesetPalettes_UnovaStriaton,
    .metatiles = gMetatiles_UnovaStriaton,
    .metatileAttributes = gMetatileAttributes_UnovaStriaton,
    .callback = InitTilesetAnim_UnovaStriaton,
};

const struct Tileset gTileset_UnovaTrainStation =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaTrainStation,
    .palettes = gTilesetPalettes_UnovaTrainStation,
    .metatiles = gMetatiles_UnovaTrainStation,
    .metatileAttributes = gMetatileAttributes_UnovaTrainStation,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaUnovaNorth =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaUnovaNorth,
    .palettes = gTilesetPalettes_UnovaUnovaNorth,
    .metatiles = gMetatiles_UnovaUnovaNorth,
    .metatileAttributes = gMetatileAttributes_UnovaUnovaNorth,
    .callback = InitTilesetAnim_UnovaUnovaNorth,
};

const struct Tileset gTileset_UnovaBridge =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaBridge,
    .palettes = gTilesetPalettes_UnovaBridge,
    .metatiles = gMetatiles_UnovaBridge,
    .metatileAttributes = gMetatileAttributes_UnovaBridge,
    .callback = InitTilesetAnim_UnovaBridge,
};

const struct Tileset gTileset_UnovaIcePath =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaIcePath,
    .palettes = gTilesetPalettes_UnovaIcePath,
    .metatiles = gMetatiles_UnovaIcePath,
    .metatileAttributes = gMetatileAttributes_UnovaIcePath,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaLentimas =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaLentimas,
    .palettes = gTilesetPalettes_UnovaLentimas,
    .metatiles = gMetatiles_UnovaLentimas,
    .metatileAttributes = gMetatileAttributes_UnovaLentimas,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaPlayersHouse =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaPlayersHouse,
    .palettes = gTilesetPalettes_UnovaPlayersHouse,
    .metatiles = gMetatiles_UnovaPlayersHouse,
    .metatileAttributes = gMetatileAttributes_UnovaPlayersHouse,
    .callback = InitTilesetAnim_UnovaPlayersHouse,
};

const struct Tileset gTileset_UnovaUnderground =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaUnderground,
    .palettes = gTilesetPalettes_UnovaUnderground,
    .metatiles = gMetatiles_UnovaUnderground,
    .metatileAttributes = gMetatileAttributes_UnovaUnderground,
    .callback = InitTilesetAnim_UnovaUnderground,
};

const struct Tileset gTileset_UnovaBattleTowerOutside =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaBattleTowerOutside,
    .palettes = gTilesetPalettes_UnovaBattleTowerOutside,
    .metatiles = gMetatiles_UnovaBattleTowerOutside,
    .metatileAttributes = gMetatileAttributes_UnovaBattleTowerOutside,
    .callback = InitTilesetAnim_UnovaBattleTowerOutside,
};

const struct Tileset gTileset_UnovaPark =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaPark,
    .palettes = gTilesetPalettes_UnovaPark,
    .metatiles = gMetatiles_UnovaPark,
    .metatileAttributes = gMetatileAttributes_UnovaPark,
    .callback = InitTilesetAnim_UnovaPark,
};

const struct Tileset gTileset_UnovaPlayersRoom =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaPlayersRoom,
    .palettes = gTilesetPalettes_UnovaPlayersRoom,
    .metatiles = gMetatiles_UnovaPlayersRoom,
    .metatileAttributes = gMetatileAttributes_UnovaPlayersRoom,
    .callback = NULL,
};

const struct Tileset gTileset_UnovaVillageBridge =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaVillageBridge,
    .palettes = gTilesetPalettes_UnovaVillageBridge,
    .metatiles = gMetatiles_UnovaVillageBridge,
    .metatileAttributes = gMetatileAttributes_UnovaVillageBridge,
    .callback = InitTilesetAnim_UnovaVillageBridge,
};

const struct Tileset gTileset_UnovaVirbank =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnovaVirbank,
    .palettes = gTilesetPalettes_UnovaVirbank,
    .metatiles = gMetatiles_UnovaVirbank,
    .metatileAttributes = gMetatileAttributes_UnovaVirbank,
    .callback = InitTilesetAnim_UnovaVirbank,
};

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaAerodactylWordRoom =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaAerodactylWordRoom,
//     .palettes = gTilesetPalettes_UnovaAerodactylWordRoom,
//     .metatiles = gMetatiles_UnovaAerodactylWordRoom,
//     .metatileAttributes = gMetatileAttributes_UnovaAerodactylWordRoom,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaBetaWordRoom =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaBetaWordRoom,
//     .palettes = gTilesetPalettes_UnovaBetaWordRoom,
//     .metatiles = gMetatiles_UnovaBetaWordRoom,
//     .metatileAttributes = gMetatileAttributes_UnovaBetaWordRoom,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaHoOhWordRoom =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaHoOhWordRoom,
//     .palettes = gTilesetPalettes_UnovaHoOhWordRoom,
//     .metatiles = gMetatiles_UnovaHoOhWordRoom,
//     .metatileAttributes = gMetatileAttributes_UnovaHoOhWordRoom,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaJohto =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaJohto,
//     .palettes = gTilesetPalettes_UnovaJohto,
//     .metatiles = gMetatiles_UnovaJohto,
//     .metatileAttributes = gMetatileAttributes_UnovaJohto,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaJohtoModern =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaJohtoModern,
//     .palettes = gTilesetPalettes_UnovaJohtoModern,
//     .metatiles = gMetatiles_UnovaJohtoModern,
//     .metatileAttributes = gMetatileAttributes_UnovaJohtoModern,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaKabutoWordRoom =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaKabutoWordRoom,
//     .palettes = gTilesetPalettes_UnovaKabutoWordRoom,
//     .metatiles = gMetatiles_UnovaKabutoWordRoom,
//     .metatileAttributes = gMetatileAttributes_UnovaKabutoWordRoom,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaKanto =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaKanto,
//     .palettes = gTilesetPalettes_UnovaKanto,
//     .metatiles = gMetatiles_UnovaKanto,
//     .metatileAttributes = gMetatileAttributes_UnovaKanto,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaLighthouse =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaLighthouse,
//     .palettes = gTilesetPalettes_UnovaLighthouse,
//     .metatiles = gMetatiles_UnovaLighthouse,
//     .metatileAttributes = gMetatileAttributes_UnovaLighthouse,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaOmanyteWordRoom =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaOmanyteWordRoom,
//     .palettes = gTilesetPalettes_UnovaOmanyteWordRoom,
//     .metatiles = gMetatiles_UnovaOmanyteWordRoom,
//     .metatileAttributes = gMetatileAttributes_UnovaOmanyteWordRoom,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaPokecomCenter =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaPokecomCenter,
//     .palettes = gTilesetPalettes_UnovaPokecomCenter,
//     .metatiles = gMetatiles_UnovaPokecomCenter,
//     .metatileAttributes = gMetatileAttributes_UnovaPokecomCenter,
//     .callback = NULL,
// };

// FORA DA BUILD: nenhum dos 291 mapas de Unova usa este tileset do BW3G (medido em maps.asm); convertido e guardado, fora da ROM
// const struct Tileset gTileset_UnovaRuinsOfAlph =
// {
//     .isCompressed = TRUE,
//     .isSecondary = TRUE,
//     .tiles = gTilesetTiles_UnovaRuinsOfAlph,
//     .palettes = gTilesetPalettes_UnovaRuinsOfAlph,
//     .metatiles = gMetatiles_UnovaRuinsOfAlph,
//     .metatileAttributes = gMetatileAttributes_UnovaRuinsOfAlph,
//     .callback = NULL,
// };

// --- Galar (G1, tileset_galar.py) ---

const struct Tileset gTileset_Galar00 =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_Galar00,
    .palettes = gTilesetPalettes_Galar00,
    .metatiles = gMetatiles_Galar00,
    .metatileAttributes = gMetatileAttributes_Galar00,
    .callback = NULL,
};

const struct Tileset gTileset_Galar01 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar01,
    .palettes = gTilesetPalettes_Galar01,
    .metatiles = gMetatiles_Galar01,
    .metatileAttributes = gMetatileAttributes_Galar01,
    .callback = NULL,
};

const struct Tileset gTileset_Galar02 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar02,
    .palettes = gTilesetPalettes_Galar02,
    .metatiles = gMetatiles_Galar02,
    .metatileAttributes = gMetatileAttributes_Galar02,
    .callback = NULL,
};

const struct Tileset gTileset_Galar03 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar03,
    .palettes = gTilesetPalettes_Galar03,
    .metatiles = gMetatiles_Galar03,
    .metatileAttributes = gMetatileAttributes_Galar03,
    .callback = NULL,
};

const struct Tileset gTileset_Galar04 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar04,
    .palettes = gTilesetPalettes_Galar04,
    .metatiles = gMetatiles_Galar04,
    .metatileAttributes = gMetatileAttributes_Galar04,
    .callback = NULL,
};

const struct Tileset gTileset_Galar05 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar05,
    .palettes = gTilesetPalettes_Galar05,
    .metatiles = gMetatiles_Galar05,
    .metatileAttributes = gMetatileAttributes_Galar05,
    .callback = NULL,
};

const struct Tileset gTileset_Galar06 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar06,
    .palettes = gTilesetPalettes_Galar06,
    .metatiles = gMetatiles_Galar06,
    .metatileAttributes = gMetatileAttributes_Galar06,
    .callback = NULL,
};

const struct Tileset gTileset_Galar07 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar07,
    .palettes = gTilesetPalettes_Galar07,
    .metatiles = gMetatiles_Galar07,
    .metatileAttributes = gMetatileAttributes_Galar07,
    .callback = NULL,
};

const struct Tileset gTileset_Galar08 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar08,
    .palettes = gTilesetPalettes_Galar08,
    .metatiles = gMetatiles_Galar08,
    .metatileAttributes = gMetatileAttributes_Galar08,
    .callback = NULL,
};

const struct Tileset gTileset_Galar09 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar09,
    .palettes = gTilesetPalettes_Galar09,
    .metatiles = gMetatiles_Galar09,
    .metatileAttributes = gMetatileAttributes_Galar09,
    .callback = NULL,
};

const struct Tileset gTileset_Galar10 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar10,
    .palettes = gTilesetPalettes_Galar10,
    .metatiles = gMetatiles_Galar10,
    .metatileAttributes = gMetatileAttributes_Galar10,
    .callback = NULL,
};

const struct Tileset gTileset_Galar11 =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_Galar11,
    .palettes = gTilesetPalettes_Galar11,
    .metatiles = gMetatiles_Galar11,
    .metatileAttributes = gMetatileAttributes_Galar11,
    .callback = NULL,
};

const struct Tileset gTileset_Galar12 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar12,
    .palettes = gTilesetPalettes_Galar12,
    .metatiles = gMetatiles_Galar12,
    .metatileAttributes = gMetatileAttributes_Galar12,
    .callback = NULL,
};

const struct Tileset gTileset_Galar13 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar13,
    .palettes = gTilesetPalettes_Galar13,
    .metatiles = gMetatiles_Galar13,
    .metatileAttributes = gMetatileAttributes_Galar13,
    .callback = NULL,
};

const struct Tileset gTileset_Galar14 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar14,
    .palettes = gTilesetPalettes_Galar14,
    .metatiles = gMetatiles_Galar14,
    .metatileAttributes = gMetatileAttributes_Galar14,
    .callback = NULL,
};

const struct Tileset gTileset_Galar15 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar15,
    .palettes = gTilesetPalettes_Galar15,
    .metatiles = gMetatiles_Galar15,
    .metatileAttributes = gMetatileAttributes_Galar15,
    .callback = NULL,
};

const struct Tileset gTileset_Galar16 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar16,
    .palettes = gTilesetPalettes_Galar16,
    .metatiles = gMetatiles_Galar16,
    .metatileAttributes = gMetatileAttributes_Galar16,
    .callback = NULL,
};

const struct Tileset gTileset_Galar17 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar17,
    .palettes = gTilesetPalettes_Galar17,
    .metatiles = gMetatiles_Galar17,
    .metatileAttributes = gMetatileAttributes_Galar17,
    .callback = NULL,
};

const struct Tileset gTileset_Galar18 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar18,
    .palettes = gTilesetPalettes_Galar18,
    .metatiles = gMetatiles_Galar18,
    .metatileAttributes = gMetatileAttributes_Galar18,
    .callback = NULL,
};

const struct Tileset gTileset_Galar19 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar19,
    .palettes = gTilesetPalettes_Galar19,
    .metatiles = gMetatiles_Galar19,
    .metatileAttributes = gMetatileAttributes_Galar19,
    .callback = NULL,
};

const struct Tileset gTileset_Galar20 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar20,
    .palettes = gTilesetPalettes_Galar20,
    .metatiles = gMetatiles_Galar20,
    .metatileAttributes = gMetatileAttributes_Galar20,
    .callback = NULL,
};

const struct Tileset gTileset_Galar21 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar21,
    .palettes = gTilesetPalettes_Galar21,
    .metatiles = gMetatiles_Galar21,
    .metatileAttributes = gMetatileAttributes_Galar21,
    .callback = NULL,
};

const struct Tileset gTileset_Galar22 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar22,
    .palettes = gTilesetPalettes_Galar22,
    .metatiles = gMetatiles_Galar22,
    .metatileAttributes = gMetatileAttributes_Galar22,
    .callback = NULL,
};

const struct Tileset gTileset_Galar23 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar23,
    .palettes = gTilesetPalettes_Galar23,
    .metatiles = gMetatiles_Galar23,
    .metatileAttributes = gMetatileAttributes_Galar23,
    .callback = NULL,
};

const struct Tileset gTileset_Galar24 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar24,
    .palettes = gTilesetPalettes_Galar24,
    .metatiles = gMetatiles_Galar24,
    .metatileAttributes = gMetatileAttributes_Galar24,
    .callback = NULL,
};

const struct Tileset gTileset_Galar25 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar25,
    .palettes = gTilesetPalettes_Galar25,
    .metatiles = gMetatiles_Galar25,
    .metatileAttributes = gMetatileAttributes_Galar25,
    .callback = NULL,
};

const struct Tileset gTileset_Galar26 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar26,
    .palettes = gTilesetPalettes_Galar26,
    .metatiles = gMetatiles_Galar26,
    .metatileAttributes = gMetatileAttributes_Galar26,
    .callback = NULL,
};

const struct Tileset gTileset_Galar27 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar27,
    .palettes = gTilesetPalettes_Galar27,
    .metatiles = gMetatiles_Galar27,
    .metatileAttributes = gMetatileAttributes_Galar27,
    .callback = NULL,
};

const struct Tileset gTileset_Galar28 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar28,
    .palettes = gTilesetPalettes_Galar28,
    .metatiles = gMetatiles_Galar28,
    .metatileAttributes = gMetatileAttributes_Galar28,
    .callback = NULL,
};

const struct Tileset gTileset_Galar29 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar29,
    .palettes = gTilesetPalettes_Galar29,
    .metatiles = gMetatiles_Galar29,
    .metatileAttributes = gMetatileAttributes_Galar29,
    .callback = NULL,
};

const struct Tileset gTileset_Galar30 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar30,
    .palettes = gTilesetPalettes_Galar30,
    .metatiles = gMetatiles_Galar30,
    .metatileAttributes = gMetatileAttributes_Galar30,
    .callback = NULL,
};

const struct Tileset gTileset_Galar31 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar31,
    .palettes = gTilesetPalettes_Galar31,
    .metatiles = gMetatiles_Galar31,
    .metatileAttributes = gMetatileAttributes_Galar31,
    .callback = NULL,
};

const struct Tileset gTileset_Galar32 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar32,
    .palettes = gTilesetPalettes_Galar32,
    .metatiles = gMetatiles_Galar32,
    .metatileAttributes = gMetatileAttributes_Galar32,
    .callback = NULL,
};

const struct Tileset gTileset_Galar33 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar33,
    .palettes = gTilesetPalettes_Galar33,
    .metatiles = gMetatiles_Galar33,
    .metatileAttributes = gMetatileAttributes_Galar33,
    .callback = NULL,
};

const struct Tileset gTileset_Galar34 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar34,
    .palettes = gTilesetPalettes_Galar34,
    .metatiles = gMetatiles_Galar34,
    .metatileAttributes = gMetatileAttributes_Galar34,
    .callback = NULL,
};

const struct Tileset gTileset_Galar35 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar35,
    .palettes = gTilesetPalettes_Galar35,
    .metatiles = gMetatiles_Galar35,
    .metatileAttributes = gMetatileAttributes_Galar35,
    .callback = NULL,
};

const struct Tileset gTileset_Galar36 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar36,
    .palettes = gTilesetPalettes_Galar36,
    .metatiles = gMetatiles_Galar36,
    .metatileAttributes = gMetatileAttributes_Galar36,
    .callback = NULL,
};

const struct Tileset gTileset_Galar37 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar37,
    .palettes = gTilesetPalettes_Galar37,
    .metatiles = gMetatiles_Galar37,
    .metatileAttributes = gMetatileAttributes_Galar37,
    .callback = NULL,
};

const struct Tileset gTileset_Galar38 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar38,
    .palettes = gTilesetPalettes_Galar38,
    .metatiles = gMetatiles_Galar38,
    .metatileAttributes = gMetatileAttributes_Galar38,
    .callback = NULL,
};

const struct Tileset gTileset_Galar39 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar39,
    .palettes = gTilesetPalettes_Galar39,
    .metatiles = gMetatiles_Galar39,
    .metatileAttributes = gMetatileAttributes_Galar39,
    .callback = NULL,
};

const struct Tileset gTileset_Galar41 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar41,
    .palettes = gTilesetPalettes_Galar41,
    .metatiles = gMetatiles_Galar41,
    .metatileAttributes = gMetatileAttributes_Galar41,
    .callback = NULL,
};

const struct Tileset gTileset_Galar42 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar42,
    .palettes = gTilesetPalettes_Galar42,
    .metatiles = gMetatiles_Galar42,
    .metatileAttributes = gMetatileAttributes_Galar42,
    .callback = NULL,
};

const struct Tileset gTileset_Galar43 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar43,
    .palettes = gTilesetPalettes_Galar43,
    .metatiles = gMetatiles_Galar43,
    .metatileAttributes = gMetatileAttributes_Galar43,
    .callback = NULL,
};

const struct Tileset gTileset_Galar44 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar44,
    .palettes = gTilesetPalettes_Galar44,
    .metatiles = gMetatiles_Galar44,
    .metatileAttributes = gMetatileAttributes_Galar44,
    .callback = NULL,
};

const struct Tileset gTileset_Galar45 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar45,
    .palettes = gTilesetPalettes_Galar45,
    .metatiles = gMetatiles_Galar45,
    .metatileAttributes = gMetatileAttributes_Galar45,
    .callback = NULL,
};

const struct Tileset gTileset_Galar46 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar46,
    .palettes = gTilesetPalettes_Galar46,
    .metatiles = gMetatiles_Galar46,
    .metatileAttributes = gMetatileAttributes_Galar46,
    .callback = NULL,
};

const struct Tileset gTileset_Galar47 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Galar47,
    .palettes = gTilesetPalettes_Galar47,
    .metatiles = gMetatiles_Galar47,
    .metatileAttributes = gMetatileAttributes_Galar47,
    .callback = NULL,
};
