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

// Tilesets de Sinnoh, importados de LiderMorti00/Sinnoh-pokeemerald-expansion.

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

// (antes: #endif de #if !IS_FRLG)

// ---- tilesets de Johto (dev_scripts/importa_tilesets_johto.py) ----

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

// Secundario so de LAYOUT_MAHOGANYTOWN: copia do gTileset_MahoganyTown com as
// paletas 7, 8 e 9 viradas em neve e 158 metatiles nevados. Existe separado
// porque o gTileset_MahoganyTown e compartilhado com Route 42, Route 43,
// Lago da Furia e Mt. Silver Outside, que continuam sem neve.

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
