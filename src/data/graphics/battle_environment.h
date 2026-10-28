const u32 gBattleEnvironmentTiles_TallGrass[] = INCGFX_U32("graphics/battle_environment/tall_grass/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_TallGrass[] = INCGFX_U16("graphics/battle_environment/tall_grass/palette.pal", ".gbapal");
// dedupe_assets.py: compartilhado por 7 consumidores (lista em dev_scripts/dedupe_assets.json); editar este arquivo muda TODOS.
const u32 gBattleEnvironmentTilemap_TallGrass[] = INCGFX_U32("graphics/battle_environment/tall_grass/map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_LongGrass[] = INCGFX_U32("graphics/battle_environment/long_grass/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_LongGrass[] = INCGFX_U16("graphics/battle_environment/long_grass/palette.pal", ".gbapal");
extern const u32 gBattleEnvironmentTilemap_LongGrass[ARRAY_COUNT(gBattleEnvironmentTilemap_TallGrass)] ASSET_ALIAS(gBattleEnvironmentTilemap_TallGrass); // dedupe_assets.py: mesmos 116 B (md5 850248c7)

const u32 gBattleEnvironmentTiles_Sand[] = INCGFX_U32("graphics/battle_environment/sand/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_Sand[] = INCGFX_U16("graphics/battle_environment/sand/palette.pal", ".gbapal");
// dedupe_assets.py: compartilhado por 4 consumidores (lista em dev_scripts/dedupe_assets.json); editar este arquivo muda TODOS.
const u32 gBattleEnvironmentTilemap_Sand[] = INCGFX_U32("graphics/battle_environment/sand/map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_Underwater[] = INCGFX_U32("graphics/battle_environment/underwater/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_Underwater[] = INCGFX_U16("graphics/battle_environment/underwater/palette.pal", ".gbapal");
extern const u32 gBattleEnvironmentTilemap_Underwater[ARRAY_COUNT(gBattleEnvironmentTilemap_TallGrass)] ASSET_ALIAS(gBattleEnvironmentTilemap_TallGrass); // dedupe_assets.py: mesmos 116 B (md5 850248c7)

const u32 gBattleEnvironmentTiles_Water[] = INCGFX_U32("graphics/battle_environment/water/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_Water[] = INCGFX_U16("graphics/battle_environment/water/palette.pal", ".gbapal");
extern const u32 gBattleEnvironmentTilemap_Water[ARRAY_COUNT(gBattleEnvironmentTilemap_TallGrass)] ASSET_ALIAS(gBattleEnvironmentTilemap_TallGrass); // dedupe_assets.py: mesmos 116 B (md5 850248c7)

const u32 gBattleEnvironmentTiles_PondWater[] = INCGFX_U32("graphics/battle_environment/pond_water/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_PondWater[] = INCGFX_U16("graphics/battle_environment/pond_water/palette.pal", ".gbapal");
extern const u32 gBattleEnvironmentTilemap_PondWater[ARRAY_COUNT(gBattleEnvironmentTilemap_TallGrass)] ASSET_ALIAS(gBattleEnvironmentTilemap_TallGrass); // dedupe_assets.py: mesmos 116 B (md5 850248c7)

const u32 gBattleEnvironmentTiles_Rock[] = INCGFX_U32("graphics/battle_environment/rock/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_Rock[] = INCGFX_U16("graphics/battle_environment/rock/palette.pal", ".gbapal");
extern const u32 gBattleEnvironmentTilemap_Rock[ARRAY_COUNT(gBattleEnvironmentTilemap_TallGrass)] ASSET_ALIAS(gBattleEnvironmentTilemap_TallGrass); // dedupe_assets.py: mesmos 116 B (md5 850248c7)

const u32 gBattleEnvironmentTiles_Cave[] = INCGFX_U32("graphics/battle_environment/cave/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_Cave[] = INCGFX_U16("graphics/battle_environment/cave/palette.pal", ".gbapal");
extern const u32 gBattleEnvironmentTilemap_Cave[ARRAY_COUNT(gBattleEnvironmentTilemap_TallGrass)] ASSET_ALIAS(gBattleEnvironmentTilemap_TallGrass); // dedupe_assets.py: mesmos 116 B (md5 850248c7)

const u32 gBattleEnvironmentTiles_Building[] = INCGFX_U32("graphics/battle_environment/building/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_Building[] = INCGFX_U16("graphics/battle_environment/building/palette.pal", ".gbapal");
extern const u32 gBattleEnvironmentTilemap_Building[ARRAY_COUNT(gBattleEnvironmentTilemap_Sand)] ASSET_ALIAS(gBattleEnvironmentTilemap_Sand); // dedupe_assets.py: mesmos 116 B (md5 250e7775)

const u16 gBattleEnvironmentPalette_BuildingGym[] = INCGFX_U16("graphics/battle_environment/building/gym.pal", ".gbapal");
const u16 gBattleEnvironmentPalette_BuildingLeader[] = INCGFX_U16("graphics/battle_environment/building/leader.pal", ".gbapal");
const u16 gBattleEnvironmentPalette_Plain[] = INCGFX_U16("graphics/battle_environment/plain/palette.pal", ".gbapal");

const u32 gBattleEnvironmentTiles_Stadium[] = INCGFX_U32("graphics/battle_environment/stadium/tiles.png", ".4bpp.smol");
extern const u32 gBattleEnvironmentTilemap_Stadium[ARRAY_COUNT(gBattleEnvironmentTilemap_Sand)] ASSET_ALIAS(gBattleEnvironmentTilemap_Sand); // dedupe_assets.py: mesmos 116 B (md5 250e7775)

const u16 gBattleEnvironmentPalette_Frontier[] = INCGFX_U16("graphics/battle_environment/stadium/battle_frontier.pal", ".gbapal"); // this is also used for link battles
const u16 gBattleEnvironmentPalette_StadiumAqua[] = INCGFX_U16("graphics/battle_environment/stadium/aqua.pal", ".gbapal");
const u16 gBattleEnvironmentPalette_StadiumMagma[] = INCGFX_U16("graphics/battle_environment/stadium/magma.pal", ".gbapal");
const u16 gBattleEnvironmentPalette_StadiumSidney[] = INCGFX_U16("graphics/battle_environment/stadium/sidney.pal", ".gbapal");
const u16 gBattleEnvironmentPalette_StadiumPhoebe[] = INCGFX_U16("graphics/battle_environment/stadium/phoebe.pal", ".gbapal");
const u16 gBattleEnvironmentPalette_StadiumGlacia[] = INCGFX_U16("graphics/battle_environment/stadium/glacia.pal", ".gbapal");
const u16 gBattleEnvironmentPalette_StadiumDrake[] = INCGFX_U16("graphics/battle_environment/stadium/drake.pal", ".gbapal");
const u16 gBattleEnvironmentPalette_StadiumWallace[] = INCGFX_U16("graphics/battle_environment/stadium/wallace.pal", ".gbapal");

const u16 gBattleEnvironmentPalette_Kyogre[] = INCGFX_U16("graphics/battle_environment/water/kyogre.pal", ".gbapal");
const u16 gBattleEnvironmentPalette_Groudon[] = INCGFX_U16("graphics/battle_environment/cave/groudon.pal", ".gbapal");

const u32 gBattleEnvironmentTiles_Rayquaza[] = INCGFX_U32("graphics/battle_environment/sky/tiles.png", ".4bpp.smol");
const u16 gBattleEnvironmentPalette_Rayquaza[] = INCGFX_U16("graphics/battle_environment/sky/palette.pal", ".gbapal");
extern const u32 gBattleEnvironmentTilemap_Rayquaza[ARRAY_COUNT(gBattleEnvironmentTilemap_Sand)] ASSET_ALIAS(gBattleEnvironmentTilemap_Sand); // dedupe_assets.py: mesmos 116 B (md5 250e7775)

const u32 gBattleEnvironmentAnimTiles_TallGrass[] = INCGFX_U32("graphics/battle_environment/tall_grass/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_TallGrass[] = INCGFX_U32("graphics/battle_environment/tall_grass/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentAnimTiles_LongGrass[] = INCGFX_U32("graphics/battle_environment/long_grass/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_LongGrass[] = INCGFX_U32("graphics/battle_environment/long_grass/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentAnimTiles_Sand[] = INCGFX_U32("graphics/battle_environment/sand/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_Sand[] = INCGFX_U32("graphics/battle_environment/sand/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentAnimTiles_Underwater[] = INCGFX_U32("graphics/battle_environment/underwater/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_Underwater[] = INCGFX_U32("graphics/battle_environment/underwater/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentAnimTiles_Water[] = INCGFX_U32("graphics/battle_environment/water/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_Water[] = INCGFX_U32("graphics/battle_environment/water/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentAnimTiles_PondWater[] = INCGFX_U32("graphics/battle_environment/pond_water/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_PondWater[] = INCGFX_U32("graphics/battle_environment/pond_water/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentAnimTiles_Rock[] = INCGFX_U32("graphics/battle_environment/rock/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_Rock[] = INCGFX_U32("graphics/battle_environment/rock/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentAnimTiles_Cave[] = INCGFX_U32("graphics/battle_environment/cave/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_Cave[] = INCGFX_U32("graphics/battle_environment/cave/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentAnimTiles_Building[] = INCGFX_U32("graphics/battle_environment/building/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_Building[] = INCGFX_U32("graphics/battle_environment/building/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentAnimTiles_Rayquaza[] = INCGFX_U32("graphics/battle_environment/sky/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_Rayquaza[] = INCGFX_U32("graphics/battle_environment/sky/anim_map.bin", ".smolTM");

// >>> arte fase 1
const u32 gBattleEnvironmentTiles_GalarWater[] = INCGFX_U32("graphics/battle_environment/galar_water/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarWater[] = INCGFX_U32("graphics/battle_environment/galar_water/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarWater[] = INCGFX_U16("graphics/battle_environment/galar_water/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarWater[] = INCGFX_U32("graphics/battle_environment/galar_water/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarWater[] = INCGFX_U32("graphics/battle_environment/galar_water/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarField[] = INCGFX_U32("graphics/battle_environment/galar_field/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarField[] = INCGFX_U32("graphics/battle_environment/galar_field/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarField[] = INCGFX_U16("graphics/battle_environment/galar_field/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarField[] = INCGFX_U32("graphics/battle_environment/galar_field/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarField[] = INCGFX_U32("graphics/battle_environment/galar_field/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarCaveA[] = INCGFX_U32("graphics/battle_environment/galar_cave_a/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarCaveA[] = INCGFX_U32("graphics/battle_environment/galar_cave_a/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarCaveA[] = INCGFX_U16("graphics/battle_environment/galar_cave_a/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarCaveA[] = INCGFX_U32("graphics/battle_environment/galar_cave_a/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarCaveA[] = INCGFX_U32("graphics/battle_environment/galar_cave_a/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarCaveB[] = INCGFX_U32("graphics/battle_environment/galar_cave_b/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarCaveB[] = INCGFX_U32("graphics/battle_environment/galar_cave_b/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarCaveB[] = INCGFX_U16("graphics/battle_environment/galar_cave_b/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarCaveB[] = INCGFX_U32("graphics/battle_environment/galar_cave_b/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarCaveB[] = INCGFX_U32("graphics/battle_environment/galar_cave_b/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarDesert[] = INCGFX_U32("graphics/battle_environment/galar_desert/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarDesert[] = INCGFX_U32("graphics/battle_environment/galar_desert/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarDesert[] = INCGFX_U16("graphics/battle_environment/galar_desert/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarDesert[] = INCGFX_U32("graphics/battle_environment/galar_desert/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarDesert[] = INCGFX_U32("graphics/battle_environment/galar_desert/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarStadiumIce[] = INCGFX_U32("graphics/battle_environment/galar_stadium_ice/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarStadiumIce[] = INCGFX_U32("graphics/battle_environment/galar_stadium_ice/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarStadiumIce[] = INCGFX_U16("graphics/battle_environment/galar_stadium_ice/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarStadiumIce[] = INCGFX_U32("graphics/battle_environment/galar_stadium_ice/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarStadiumIce[] = INCGFX_U32("graphics/battle_environment/galar_stadium_ice/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarStadiumGrass[] = INCGFX_U32("graphics/battle_environment/galar_stadium_grass/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarStadiumGrass[] = INCGFX_U32("graphics/battle_environment/galar_stadium_grass/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarStadiumGrass[] = INCGFX_U16("graphics/battle_environment/galar_stadium_grass/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarStadiumGrass[] = INCGFX_U32("graphics/battle_environment/galar_stadium_grass/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarStadiumGrass[] = INCGFX_U32("graphics/battle_environment/galar_stadium_grass/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarStadiumOrange[] = INCGFX_U32("graphics/battle_environment/galar_stadium_orange/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarStadiumOrange[] = INCGFX_U32("graphics/battle_environment/galar_stadium_orange/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarStadiumOrange[] = INCGFX_U16("graphics/battle_environment/galar_stadium_orange/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarStadiumOrange[] = INCGFX_U32("graphics/battle_environment/galar_stadium_orange/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarStadiumOrange[] = INCGFX_U32("graphics/battle_environment/galar_stadium_orange/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarStadiumPokeball[] = INCGFX_U32("graphics/battle_environment/galar_stadium_pokeball/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarStadiumPokeball[] = INCGFX_U32("graphics/battle_environment/galar_stadium_pokeball/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarStadiumPokeball[] = INCGFX_U16("graphics/battle_environment/galar_stadium_pokeball/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarStadiumPokeball[] = INCGFX_U32("graphics/battle_environment/galar_stadium_pokeball/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarStadiumPokeball[] = INCGFX_U32("graphics/battle_environment/galar_stadium_pokeball/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarStadiumRed[] = INCGFX_U32("graphics/battle_environment/galar_stadium_red/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarStadiumRed[] = INCGFX_U32("graphics/battle_environment/galar_stadium_red/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarStadiumRed[] = INCGFX_U16("graphics/battle_environment/galar_stadium_red/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarStadiumRed[] = INCGFX_U32("graphics/battle_environment/galar_stadium_red/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarStadiumRed[] = INCGFX_U32("graphics/battle_environment/galar_stadium_red/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarTallGrass[] = INCGFX_U32("graphics/battle_environment/galar_tall_grass/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarTallGrass[] = INCGFX_U32("graphics/battle_environment/galar_tall_grass/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarTallGrass[] = INCGFX_U16("graphics/battle_environment/galar_tall_grass/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarTallGrass[] = INCGFX_U32("graphics/battle_environment/galar_tall_grass/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarTallGrass[] = INCGFX_U32("graphics/battle_environment/galar_tall_grass/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarUnderwater[] = INCGFX_U32("graphics/battle_environment/galar_underwater/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarUnderwater[] = INCGFX_U32("graphics/battle_environment/galar_underwater/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarUnderwater[] = INCGFX_U16("graphics/battle_environment/galar_underwater/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarUnderwater[] = INCGFX_U32("graphics/battle_environment/galar_underwater/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarUnderwater[] = INCGFX_U32("graphics/battle_environment/galar_underwater/anim_map.bin", ".smolTM");

const u32 gBattleEnvironmentTiles_GalarPurpleScreen[] = INCGFX_U32("graphics/battle_environment/galar_purple_screen/tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentTilemap_GalarPurpleScreen[] = INCGFX_U32("graphics/battle_environment/galar_purple_screen/map.bin", ".smolTM");
const u16 gBattleEnvironmentPalette_GalarPurpleScreen[] = INCGFX_U16("graphics/battle_environment/galar_purple_screen/palette.pal", ".gbapal");
const u32 gBattleEnvironmentAnimTiles_GalarPurpleScreen[] = INCGFX_U32("graphics/battle_environment/galar_purple_screen/anim_tiles.png", ".4bpp.smol");
const u32 gBattleEnvironmentAnimTilemap_GalarPurpleScreen[] = INCGFX_U32("graphics/battle_environment/galar_purple_screen/anim_map.bin", ".smolTM");
// <<< fim da arte fase 1
