// GERADO por `python3 dev_scripts/tileset_gen2.py --usados --gravar`.
// Nao editar a mao: a proxima rodada sobrescreve o arquivo inteiro.
//
// Porte da animacao de tileset do BW3G (gen 2). No gen 2 cada linha de
// `engine/tilesets/tileset_anims.asm` roda num quadro do ciclo e escreve 16
// bytes num tile de VRAM; aqui os quadros ja vem prontos em 4bpp e quem os
// despeja e a fila do V-blank do proprio pokeemerald
// (`AppendTilesetAnimToBuffer` / `TransferTilesetAnimsBuffer`), a mesma que
// General, Rustboro e Sootopolis usam. Nenhum mecanismo novo.
//
// Custo de CPU: `TilesetAnim_Unova` so enfileira a animacao de indice
// `timer % 16`, entao no maximo UMA transferencia de 32 bytes por quadro, como
// no gen 2, onde cada linha da tabela tambem rodava num quadro so.

static const u16 sUnovaAnimGfx_castelia_fountain_1_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_1/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_1_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_1/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_1_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_1/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_1_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_1/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_1_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_1/04.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_castelia_fountain_1[] =
{
    sUnovaAnimGfx_castelia_fountain_1_00,
    sUnovaAnimGfx_castelia_fountain_1_01,
    sUnovaAnimGfx_castelia_fountain_1_02,
    sUnovaAnimGfx_castelia_fountain_1_03,
    sUnovaAnimGfx_castelia_fountain_1_04
};

static const u16 sUnovaAnimGfx_castelia_fountain_2_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_2/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_2_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_2/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_2_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_2/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_2_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_2/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_2_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_2/04.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_castelia_fountain_2[] =
{
    sUnovaAnimGfx_castelia_fountain_2_00,
    sUnovaAnimGfx_castelia_fountain_2_01,
    sUnovaAnimGfx_castelia_fountain_2_02,
    sUnovaAnimGfx_castelia_fountain_2_03,
    sUnovaAnimGfx_castelia_fountain_2_04
};

static const u16 sUnovaAnimGfx_castelia_fountain_3_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_3/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_3_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_3/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_3_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_3/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_3_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_3/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_3_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_3/04.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_castelia_fountain_3[] =
{
    sUnovaAnimGfx_castelia_fountain_3_00,
    sUnovaAnimGfx_castelia_fountain_3_01,
    sUnovaAnimGfx_castelia_fountain_3_02,
    sUnovaAnimGfx_castelia_fountain_3_03,
    sUnovaAnimGfx_castelia_fountain_3_04
};

static const u16 sUnovaAnimGfx_castelia_fountain_4_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_4/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_4_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_4/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_4_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_4/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_4_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_4/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_4_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_4/04.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_castelia_fountain_4[] =
{
    sUnovaAnimGfx_castelia_fountain_4_00,
    sUnovaAnimGfx_castelia_fountain_4_01,
    sUnovaAnimGfx_castelia_fountain_4_02,
    sUnovaAnimGfx_castelia_fountain_4_03,
    sUnovaAnimGfx_castelia_fountain_4_04
};

static const u16 sUnovaAnimGfx_castelia_fountain_5_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_5/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_5_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_5/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_5_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_5/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_5_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_5/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_5_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_5/04.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_castelia_fountain_5[] =
{
    sUnovaAnimGfx_castelia_fountain_5_00,
    sUnovaAnimGfx_castelia_fountain_5_01,
    sUnovaAnimGfx_castelia_fountain_5_02,
    sUnovaAnimGfx_castelia_fountain_5_03,
    sUnovaAnimGfx_castelia_fountain_5_04
};

static const u16 sUnovaAnimGfx_castelia_fountain_6_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_6/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_6_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_6/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_6_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_6/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_6_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_6/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_castelia_fountain_6_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/castelia_fountain_6/04.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_castelia_fountain_6[] =
{
    sUnovaAnimGfx_castelia_fountain_6_00,
    sUnovaAnimGfx_castelia_fountain_6_01,
    sUnovaAnimGfx_castelia_fountain_6_02,
    sUnovaAnimGfx_castelia_fountain_6_03,
    sUnovaAnimGfx_castelia_fountain_6_04
};

static const u16 sUnovaAnimGfx_cave_r14_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r14/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r14_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r14/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r14_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r14/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r14_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r14/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r14_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r14/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r14_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r14/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r14_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r14/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r14_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r14/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_cave_r14[] =
{
    sUnovaAnimGfx_cave_r14_00,
    sUnovaAnimGfx_cave_r14_01,
    sUnovaAnimGfx_cave_r14_02,
    sUnovaAnimGfx_cave_r14_03,
    sUnovaAnimGfx_cave_r14_04,
    sUnovaAnimGfx_cave_r14_05,
    sUnovaAnimGfx_cave_r14_06,
    sUnovaAnimGfx_cave_r14_07
};

static const u16 sUnovaAnimGfx_cave_r40_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r40/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r40_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r40/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r40_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r40/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r40_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r40/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r40_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r40/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r40_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r40/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r40_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r40/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_r40_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_r40/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_cave_r40[] =
{
    sUnovaAnimGfx_cave_r40_00,
    sUnovaAnimGfx_cave_r40_01,
    sUnovaAnimGfx_cave_r40_02,
    sUnovaAnimGfx_cave_r40_03,
    sUnovaAnimGfx_cave_r40_04,
    sUnovaAnimGfx_cave_r40_05,
    sUnovaAnimGfx_cave_r40_06,
    sUnovaAnimGfx_cave_r40_07
};

static const u16 sUnovaAnimGfx_cave_ruins_r14_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_ruins_r14/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_ruins_r14_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_ruins_r14/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_ruins_r14_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_ruins_r14/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_ruins_r14_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_ruins_r14/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_ruins_r14_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_ruins_r14/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_ruins_r14_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_ruins_r14/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_ruins_r14_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_ruins_r14/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_cave_ruins_r14_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/cave_ruins_r14/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_cave_ruins_r14[] =
{
    sUnovaAnimGfx_cave_ruins_r14_00,
    sUnovaAnimGfx_cave_ruins_r14_01,
    sUnovaAnimGfx_cave_ruins_r14_02,
    sUnovaAnimGfx_cave_ruins_r14_03,
    sUnovaAnimGfx_cave_ruins_r14_04,
    sUnovaAnimGfx_cave_ruins_r14_05,
    sUnovaAnimGfx_cave_ruins_r14_06,
    sUnovaAnimGfx_cave_ruins_r14_07
};

static const u16 sUnovaAnimGfx_computer_1_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/computer_1/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_computer_1_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/computer_1/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_computer_1_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/computer_1/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_computer_1_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/computer_1/03.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_computer_1[] =
{
    sUnovaAnimGfx_computer_1_00,
    sUnovaAnimGfx_computer_1_01,
    sUnovaAnimGfx_computer_1_02,
    sUnovaAnimGfx_computer_1_03
};

static const u16 sUnovaAnimGfx_computer_2_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/computer_2/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_computer_2_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/computer_2/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_computer_2_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/computer_2/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_computer_2_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/computer_2/03.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_computer_2[] =
{
    sUnovaAnimGfx_computer_2_00,
    sUnovaAnimGfx_computer_2_01,
    sUnovaAnimGfx_computer_2_02,
    sUnovaAnimGfx_computer_2_03
};

static const u16 sUnovaAnimGfx_dreamyard_r6f_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/dreamyard_r6f/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_dreamyard_r6f_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/dreamyard_r6f/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_dreamyard_r6f_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/dreamyard_r6f/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_dreamyard_r6f_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/dreamyard_r6f/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_dreamyard_r6f_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/dreamyard_r6f/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_dreamyard_r6f_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/dreamyard_r6f/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_dreamyard_r6f_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/dreamyard_r6f/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_dreamyard_r6f_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/dreamyard_r6f/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_dreamyard_r6f[] =
{
    sUnovaAnimGfx_dreamyard_r6f_00,
    sUnovaAnimGfx_dreamyard_r6f_01,
    sUnovaAnimGfx_dreamyard_r6f_02,
    sUnovaAnimGfx_dreamyard_r6f_03,
    sUnovaAnimGfx_dreamyard_r6f_04,
    sUnovaAnimGfx_dreamyard_r6f_05,
    sUnovaAnimGfx_dreamyard_r6f_06,
    sUnovaAnimGfx_dreamyard_r6f_07
};

static const u16 sUnovaAnimGfx_elite_four_room_r57_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/elite_four_room_r57/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_elite_four_room_r57_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/elite_four_room_r57/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_elite_four_room_r57_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/elite_four_room_r57/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_elite_four_room_r57_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/elite_four_room_r57/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_elite_four_room_r57_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/elite_four_room_r57/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_elite_four_room_r57_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/elite_four_room_r57/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_elite_four_room_r57_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/elite_four_room_r57/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_elite_four_room_r57_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/elite_four_room_r57/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_elite_four_room_r57[] =
{
    sUnovaAnimGfx_elite_four_room_r57_00,
    sUnovaAnimGfx_elite_four_room_r57_01,
    sUnovaAnimGfx_elite_four_room_r57_02,
    sUnovaAnimGfx_elite_four_room_r57_03,
    sUnovaAnimGfx_elite_four_room_r57_04,
    sUnovaAnimGfx_elite_four_room_r57_05,
    sUnovaAnimGfx_elite_four_room_r57_06,
    sUnovaAnimGfx_elite_four_room_r57_07
};

static const u16 sUnovaAnimGfx_fan_1_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/fan_1/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_fan_1_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/fan_1/01.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_fan_1[] =
{
    sUnovaAnimGfx_fan_1_00,
    sUnovaAnimGfx_fan_1_01
};

static const u16 sUnovaAnimGfx_fan_2_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/fan_2/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_fan_2_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/fan_2/01.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_fan_2[] =
{
    sUnovaAnimGfx_fan_2_00,
    sUnovaAnimGfx_fan_2_01
};

static const u16 sUnovaAnimGfx_fan_3_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/fan_3/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_fan_3_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/fan_3/01.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_fan_3[] =
{
    sUnovaAnimGfx_fan_3_00,
    sUnovaAnimGfx_fan_3_01
};

static const u16 sUnovaAnimGfx_fan_4_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/fan_4/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_fan_4_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/fan_4/01.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_fan_4[] =
{
    sUnovaAnimGfx_fan_4_00,
    sUnovaAnimGfx_fan_4_01
};

static const u16 sUnovaAnimGfx_flower_cgb_1_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/flower_cgb_1/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_flower_cgb_1_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/flower_cgb_1/01.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_flower_cgb_1[] =
{
    sUnovaAnimGfx_flower_cgb_1_00,
    sUnovaAnimGfx_flower_cgb_1_01
};

static const u16 sUnovaAnimGfx_forest_tree_1_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/forest_tree_1/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_forest_tree_1_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/forest_tree_1/01.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_forest_tree_1[] =
{
    sUnovaAnimGfx_forest_tree_1_00,
    sUnovaAnimGfx_forest_tree_1_01
};

static const u16 sUnovaAnimGfx_forest_tree_3_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/forest_tree_3/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_forest_tree_3_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/forest_tree_3/01.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_forest_tree_3[] =
{
    sUnovaAnimGfx_forest_tree_3_00,
    sUnovaAnimGfx_forest_tree_3_01
};

static const u16 sUnovaAnimGfx_icirrus_r08_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r08/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r08_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r08/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r08_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r08/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r08_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r08/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r08_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r08/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r08_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r08/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r08_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r08/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r08_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r08/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_icirrus_r08[] =
{
    sUnovaAnimGfx_icirrus_r08_00,
    sUnovaAnimGfx_icirrus_r08_01,
    sUnovaAnimGfx_icirrus_r08_02,
    sUnovaAnimGfx_icirrus_r08_03,
    sUnovaAnimGfx_icirrus_r08_04,
    sUnovaAnimGfx_icirrus_r08_05,
    sUnovaAnimGfx_icirrus_r08_06,
    sUnovaAnimGfx_icirrus_r08_07
};

static const u16 sUnovaAnimGfx_icirrus_r09_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r09/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r09_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r09/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r09_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r09/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r09_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r09/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r09_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r09/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r09_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r09/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r09_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r09/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r09_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r09/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_icirrus_r09[] =
{
    sUnovaAnimGfx_icirrus_r09_00,
    sUnovaAnimGfx_icirrus_r09_01,
    sUnovaAnimGfx_icirrus_r09_02,
    sUnovaAnimGfx_icirrus_r09_03,
    sUnovaAnimGfx_icirrus_r09_04,
    sUnovaAnimGfx_icirrus_r09_05,
    sUnovaAnimGfx_icirrus_r09_06,
    sUnovaAnimGfx_icirrus_r09_07
};

static const u16 sUnovaAnimGfx_icirrus_r18_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r18/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r18_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r18/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r18_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r18/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r18_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r18/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r18_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r18/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r18_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r18/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r18_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r18/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r18_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r18/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_icirrus_r18[] =
{
    sUnovaAnimGfx_icirrus_r18_00,
    sUnovaAnimGfx_icirrus_r18_01,
    sUnovaAnimGfx_icirrus_r18_02,
    sUnovaAnimGfx_icirrus_r18_03,
    sUnovaAnimGfx_icirrus_r18_04,
    sUnovaAnimGfx_icirrus_r18_05,
    sUnovaAnimGfx_icirrus_r18_06,
    sUnovaAnimGfx_icirrus_r18_07
};

static const u16 sUnovaAnimGfx_icirrus_r19_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r19/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r19_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r19/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r19_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r19/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r19_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r19/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r19_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r19/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r19_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r19/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r19_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r19/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_icirrus_r19_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/icirrus_r19/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_icirrus_r19[] =
{
    sUnovaAnimGfx_icirrus_r19_00,
    sUnovaAnimGfx_icirrus_r19_01,
    sUnovaAnimGfx_icirrus_r19_02,
    sUnovaAnimGfx_icirrus_r19_03,
    sUnovaAnimGfx_icirrus_r19_04,
    sUnovaAnimGfx_icirrus_r19_05,
    sUnovaAnimGfx_icirrus_r19_06,
    sUnovaAnimGfx_icirrus_r19_07
};

static const u16 sUnovaAnimGfx_opelucid_r1d_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r1d/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r1d_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r1d/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r1d_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r1d/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r1d_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r1d/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r1d_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r1d/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r1d_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r1d/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r1d_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r1d/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r1d_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r1d/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_opelucid_r1d[] =
{
    sUnovaAnimGfx_opelucid_r1d_00,
    sUnovaAnimGfx_opelucid_r1d_01,
    sUnovaAnimGfx_opelucid_r1d_02,
    sUnovaAnimGfx_opelucid_r1d_03,
    sUnovaAnimGfx_opelucid_r1d_04,
    sUnovaAnimGfx_opelucid_r1d_05,
    sUnovaAnimGfx_opelucid_r1d_06,
    sUnovaAnimGfx_opelucid_r1d_07
};

static const u16 sUnovaAnimGfx_opelucid_r4d_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r4d/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r4d_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r4d/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r4d_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r4d/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r4d_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r4d/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r4d_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r4d/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r4d_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r4d/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r4d_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r4d/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r4d_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r4d/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_opelucid_r4d[] =
{
    sUnovaAnimGfx_opelucid_r4d_00,
    sUnovaAnimGfx_opelucid_r4d_01,
    sUnovaAnimGfx_opelucid_r4d_02,
    sUnovaAnimGfx_opelucid_r4d_03,
    sUnovaAnimGfx_opelucid_r4d_04,
    sUnovaAnimGfx_opelucid_r4d_05,
    sUnovaAnimGfx_opelucid_r4d_06,
    sUnovaAnimGfx_opelucid_r4d_07
};

static const u16 sUnovaAnimGfx_opelucid_r6f_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r6f/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r6f_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r6f/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r6f_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r6f/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r6f_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r6f/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r6f_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r6f/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r6f_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r6f/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r6f_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r6f/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_opelucid_r6f_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/opelucid_r6f/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_opelucid_r6f[] =
{
    sUnovaAnimGfx_opelucid_r6f_00,
    sUnovaAnimGfx_opelucid_r6f_01,
    sUnovaAnimGfx_opelucid_r6f_02,
    sUnovaAnimGfx_opelucid_r6f_03,
    sUnovaAnimGfx_opelucid_r6f_04,
    sUnovaAnimGfx_opelucid_r6f_05,
    sUnovaAnimGfx_opelucid_r6f_06,
    sUnovaAnimGfx_opelucid_r6f_07
};

static const u16 sUnovaAnimGfx_sky_1_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_1/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_1_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_1/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_1_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_1/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_1_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_1/03.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_sky_1[] =
{
    sUnovaAnimGfx_sky_1_00,
    sUnovaAnimGfx_sky_1_01,
    sUnovaAnimGfx_sky_1_02,
    sUnovaAnimGfx_sky_1_03
};

static const u16 sUnovaAnimGfx_sky_2_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_2/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_2_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_2/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_2_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_2/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_2_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_2/03.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_sky_2[] =
{
    sUnovaAnimGfx_sky_2_00,
    sUnovaAnimGfx_sky_2_01,
    sUnovaAnimGfx_sky_2_02,
    sUnovaAnimGfx_sky_2_03
};

static const u16 sUnovaAnimGfx_sky_3_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_3/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_3_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_3/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_3_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_3/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_3_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_3/03.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_sky_3[] =
{
    sUnovaAnimGfx_sky_3_00,
    sUnovaAnimGfx_sky_3_01,
    sUnovaAnimGfx_sky_3_02,
    sUnovaAnimGfx_sky_3_03
};

static const u16 sUnovaAnimGfx_sky_4_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_4/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_4_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_4/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_4_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_4/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_sky_4_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/sky_4/03.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_sky_4[] =
{
    sUnovaAnimGfx_sky_4_00,
    sUnovaAnimGfx_sky_4_01,
    sUnovaAnimGfx_sky_4_02,
    sUnovaAnimGfx_sky_4_03
};

static const u16 sUnovaAnimGfx_stars_1_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_stars_1_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_stars_1_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_stars_1_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1/03.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_stars_1[] =
{
    sUnovaAnimGfx_stars_1_00,
    sUnovaAnimGfx_stars_1_01,
    sUnovaAnimGfx_stars_1_02,
    sUnovaAnimGfx_stars_1_03
};

static const u16 sUnovaAnimGfx_stars_1_f1_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1_f1/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_stars_1_f1_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1_f1/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_stars_1_f1_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1_f1/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_stars_1_f1_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1_f1/03.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_stars_1_f1[] =
{
    sUnovaAnimGfx_stars_1_f1_00,
    sUnovaAnimGfx_stars_1_f1_01,
    sUnovaAnimGfx_stars_1_f1_02,
    sUnovaAnimGfx_stars_1_f1_03
};

static const u16 sUnovaAnimGfx_stars_1_f2_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1_f2/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_stars_1_f2_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1_f2/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_stars_1_f2_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1_f2/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_stars_1_f2_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/stars_1_f2/03.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_stars_1_f2[] =
{
    sUnovaAnimGfx_stars_1_f2_00,
    sUnovaAnimGfx_stars_1_f2_01,
    sUnovaAnimGfx_stars_1_f2_02,
    sUnovaAnimGfx_stars_1_f2_03
};

static const u16 sUnovaAnimGfx_underground_r77_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/underground_r77/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_underground_r77_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/underground_r77/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_underground_r77_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/underground_r77/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_underground_r77_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/underground_r77/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_underground_r77_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/underground_r77/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_underground_r77_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/underground_r77/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_underground_r77_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/underground_r77/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_underground_r77_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/underground_r77/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_underground_r77[] =
{
    sUnovaAnimGfx_underground_r77_00,
    sUnovaAnimGfx_underground_r77_01,
    sUnovaAnimGfx_underground_r77_02,
    sUnovaAnimGfx_underground_r77_03,
    sUnovaAnimGfx_underground_r77_04,
    sUnovaAnimGfx_underground_r77_05,
    sUnovaAnimGfx_underground_r77_06,
    sUnovaAnimGfx_underground_r77_07
};

static const u16 sUnovaAnimGfx_unova_east_r60_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r60/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r60_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r60/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r60_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r60/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r60_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r60/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r60_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r60/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r60_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r60/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r60_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r60/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r60_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r60/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_unova_east_r60[] =
{
    sUnovaAnimGfx_unova_east_r60_00,
    sUnovaAnimGfx_unova_east_r60_01,
    sUnovaAnimGfx_unova_east_r60_02,
    sUnovaAnimGfx_unova_east_r60_03,
    sUnovaAnimGfx_unova_east_r60_04,
    sUnovaAnimGfx_unova_east_r60_05,
    sUnovaAnimGfx_unova_east_r60_06,
    sUnovaAnimGfx_unova_east_r60_07
};

static const u16 sUnovaAnimGfx_unova_east_r61_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r61/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r61_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r61/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r61_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r61/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r61_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r61/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r61_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r61/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r61_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r61/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r61_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r61/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r61_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r61/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_unova_east_r61[] =
{
    sUnovaAnimGfx_unova_east_r61_00,
    sUnovaAnimGfx_unova_east_r61_01,
    sUnovaAnimGfx_unova_east_r61_02,
    sUnovaAnimGfx_unova_east_r61_03,
    sUnovaAnimGfx_unova_east_r61_04,
    sUnovaAnimGfx_unova_east_r61_05,
    sUnovaAnimGfx_unova_east_r61_06,
    sUnovaAnimGfx_unova_east_r61_07
};

static const u16 sUnovaAnimGfx_unova_east_r62_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r62/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r62_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r62/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r62_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r62/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r62_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r62/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r62_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r62/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r62_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r62/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r62_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r62/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r62_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r62/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_unova_east_r62[] =
{
    sUnovaAnimGfx_unova_east_r62_00,
    sUnovaAnimGfx_unova_east_r62_01,
    sUnovaAnimGfx_unova_east_r62_02,
    sUnovaAnimGfx_unova_east_r62_03,
    sUnovaAnimGfx_unova_east_r62_04,
    sUnovaAnimGfx_unova_east_r62_05,
    sUnovaAnimGfx_unova_east_r62_06,
    sUnovaAnimGfx_unova_east_r62_07
};

static const u16 sUnovaAnimGfx_unova_east_r63_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r63/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r63_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r63/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r63_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r63/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r63_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r63/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r63_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r63/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r63_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r63/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r63_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r63/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_east_r63_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_east_r63/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_unova_east_r63[] =
{
    sUnovaAnimGfx_unova_east_r63_00,
    sUnovaAnimGfx_unova_east_r63_01,
    sUnovaAnimGfx_unova_east_r63_02,
    sUnovaAnimGfx_unova_east_r63_03,
    sUnovaAnimGfx_unova_east_r63_04,
    sUnovaAnimGfx_unova_east_r63_05,
    sUnovaAnimGfx_unova_east_r63_06,
    sUnovaAnimGfx_unova_east_r63_07
};

static const u16 sUnovaAnimGfx_unova_north_r60_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_north_r60/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_north_r60_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_north_r60/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_north_r60_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_north_r60/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_north_r60_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_north_r60/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_north_r60_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_north_r60/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_north_r60_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_north_r60/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_north_r60_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_north_r60/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_unova_north_r60_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/unova_north_r60/07.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_unova_north_r60[] =
{
    sUnovaAnimGfx_unova_north_r60_00,
    sUnovaAnimGfx_unova_north_r60_01,
    sUnovaAnimGfx_unova_north_r60_02,
    sUnovaAnimGfx_unova_north_r60_03,
    sUnovaAnimGfx_unova_north_r60_04,
    sUnovaAnimGfx_unova_north_r60_05,
    sUnovaAnimGfx_unova_north_r60_06,
    sUnovaAnimGfx_unova_north_r60_07
};

static const u16 sUnovaAnimGfx_whirlpool_1_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/07.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_08[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/08.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_09[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/09.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_1_10[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_1/10.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_whirlpool_1[] =
{
    sUnovaAnimGfx_whirlpool_1_00,
    sUnovaAnimGfx_whirlpool_1_01,
    sUnovaAnimGfx_whirlpool_1_02,
    sUnovaAnimGfx_whirlpool_1_03,
    sUnovaAnimGfx_whirlpool_1_04,
    sUnovaAnimGfx_whirlpool_1_05,
    sUnovaAnimGfx_whirlpool_1_06,
    sUnovaAnimGfx_whirlpool_1_07,
    sUnovaAnimGfx_whirlpool_1_08,
    sUnovaAnimGfx_whirlpool_1_09,
    sUnovaAnimGfx_whirlpool_1_10
};

static const u16 sUnovaAnimGfx_whirlpool_2_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/07.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_08[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/08.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_09[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/09.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_2_10[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_2/10.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_whirlpool_2[] =
{
    sUnovaAnimGfx_whirlpool_2_00,
    sUnovaAnimGfx_whirlpool_2_01,
    sUnovaAnimGfx_whirlpool_2_02,
    sUnovaAnimGfx_whirlpool_2_03,
    sUnovaAnimGfx_whirlpool_2_04,
    sUnovaAnimGfx_whirlpool_2_05,
    sUnovaAnimGfx_whirlpool_2_06,
    sUnovaAnimGfx_whirlpool_2_07,
    sUnovaAnimGfx_whirlpool_2_08,
    sUnovaAnimGfx_whirlpool_2_09,
    sUnovaAnimGfx_whirlpool_2_10
};

static const u16 sUnovaAnimGfx_whirlpool_3_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/07.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_08[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/08.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_09[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/09.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_3_10[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_3/10.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_whirlpool_3[] =
{
    sUnovaAnimGfx_whirlpool_3_00,
    sUnovaAnimGfx_whirlpool_3_01,
    sUnovaAnimGfx_whirlpool_3_02,
    sUnovaAnimGfx_whirlpool_3_03,
    sUnovaAnimGfx_whirlpool_3_04,
    sUnovaAnimGfx_whirlpool_3_05,
    sUnovaAnimGfx_whirlpool_3_06,
    sUnovaAnimGfx_whirlpool_3_07,
    sUnovaAnimGfx_whirlpool_3_08,
    sUnovaAnimGfx_whirlpool_3_09,
    sUnovaAnimGfx_whirlpool_3_10
};

static const u16 sUnovaAnimGfx_whirlpool_4_00[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/00.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_01[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/01.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_02[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/02.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_03[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/03.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_04[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/04.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_05[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/05.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_06[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/06.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_07[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/07.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_08[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/08.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_09[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/09.png", ".4bpp");
static const u16 sUnovaAnimGfx_whirlpool_4_10[] = INCGFX_U16("data/tilesets/secondary/unova_anim/whirlpool_4/10.png", ".4bpp");

static const u16 *const sUnovaAnimFrames_whirlpool_4[] =
{
    sUnovaAnimGfx_whirlpool_4_00,
    sUnovaAnimGfx_whirlpool_4_01,
    sUnovaAnimGfx_whirlpool_4_02,
    sUnovaAnimGfx_whirlpool_4_03,
    sUnovaAnimGfx_whirlpool_4_04,
    sUnovaAnimGfx_whirlpool_4_05,
    sUnovaAnimGfx_whirlpool_4_06,
    sUnovaAnimGfx_whirlpool_4_07,
    sUnovaAnimGfx_whirlpool_4_08,
    sUnovaAnimGfx_whirlpool_4_09,
    sUnovaAnimGfx_whirlpool_4_10
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaCave[] =
{
    { sUnovaAnimFrames_cave_r14, ARRAY_COUNT(sUnovaAnimFrames_cave_r14), 12 },
    { sUnovaAnimFrames_cave_r40, ARRAY_COUNT(sUnovaAnimFrames_cave_r40), 45 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaUnovaBeach[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 79 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 80 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 91 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 92 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 4 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaDesert[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 110 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 111 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 126 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 127 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaEliteFourRoom[] =
{
    { sUnovaAnimFrames_elite_four_room_r57, ARRAY_COUNT(sUnovaAnimFrames_elite_four_room_r57), 77 },
    { sUnovaAnimFrames_fan_1, ARRAY_COUNT(sUnovaAnimFrames_fan_1), 85 },
    { sUnovaAnimFrames_fan_2, ARRAY_COUNT(sUnovaAnimFrames_fan_2), 86 },
    { sUnovaAnimFrames_fan_3, ARRAY_COUNT(sUnovaAnimFrames_fan_3), 101 },
    { sUnovaAnimFrames_fan_4, ARRAY_COUNT(sUnovaAnimFrames_fan_4), 102 },
    { sUnovaAnimFrames_computer_1, ARRAY_COUNT(sUnovaAnimFrames_computer_1), 60 },
    { sUnovaAnimFrames_computer_2, ARRAY_COUNT(sUnovaAnimFrames_computer_2), 61 },
    { sUnovaAnimFrames_computer_1, ARRAY_COUNT(sUnovaAnimFrames_computer_1), 75 },
    { sUnovaAnimFrames_computer_2, ARRAY_COUNT(sUnovaAnimFrames_computer_2), 76 },
    { sUnovaAnimFrames_computer_1, ARRAY_COUNT(sUnovaAnimFrames_computer_1), 65 },
    { sUnovaAnimFrames_computer_2, ARRAY_COUNT(sUnovaAnimFrames_computer_2), 66 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaTower[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 31 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 32 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 45 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 46 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaUnovaEast[] =
{
    { sUnovaAnimFrames_unova_east_r60, ARRAY_COUNT(sUnovaAnimFrames_unova_east_r60), 66 },
    { sUnovaAnimFrames_unova_east_r61, ARRAY_COUNT(sUnovaAnimFrames_unova_east_r61), 67 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 4 },
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 79 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 80 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 94 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 95 },
    { sUnovaAnimFrames_unova_east_r62, ARRAY_COUNT(sUnovaAnimFrames_unova_east_r62), 68 },
    { sUnovaAnimFrames_unova_east_r63, ARRAY_COUNT(sUnovaAnimFrames_unova_east_r63), 69 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaAirport[] =
{
    { sUnovaAnimFrames_sky_1, ARRAY_COUNT(sUnovaAnimFrames_sky_1), 4 },
    { sUnovaAnimFrames_sky_1, ARRAY_COUNT(sUnovaAnimFrames_sky_1), 5 },
    { sUnovaAnimFrames_sky_1, ARRAY_COUNT(sUnovaAnimFrames_sky_1), 6 },
    { sUnovaAnimFrames_sky_1, ARRAY_COUNT(sUnovaAnimFrames_sky_1), 7 },
    { sUnovaAnimFrames_sky_2, ARRAY_COUNT(sUnovaAnimFrames_sky_2), 19 },
    { sUnovaAnimFrames_sky_2, ARRAY_COUNT(sUnovaAnimFrames_sky_2), 20 },
    { sUnovaAnimFrames_sky_2, ARRAY_COUNT(sUnovaAnimFrames_sky_2), 21 },
    { sUnovaAnimFrames_sky_2, ARRAY_COUNT(sUnovaAnimFrames_sky_2), 22 },
    { sUnovaAnimFrames_sky_3, ARRAY_COUNT(sUnovaAnimFrames_sky_3), 34 },
    { sUnovaAnimFrames_sky_3, ARRAY_COUNT(sUnovaAnimFrames_sky_3), 35 },
    { sUnovaAnimFrames_sky_3, ARRAY_COUNT(sUnovaAnimFrames_sky_3), 36 },
    { sUnovaAnimFrames_sky_3, ARRAY_COUNT(sUnovaAnimFrames_sky_3), 37 },
    { sUnovaAnimFrames_sky_4, ARRAY_COUNT(sUnovaAnimFrames_sky_4), 48 },
    { sUnovaAnimFrames_sky_4, ARRAY_COUNT(sUnovaAnimFrames_sky_4), 49 },
    { sUnovaAnimFrames_sky_4, ARRAY_COUNT(sUnovaAnimFrames_sky_4), 50 },
    { sUnovaAnimFrames_sky_4, ARRAY_COUNT(sUnovaAnimFrames_sky_4), 51 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaIcirrus[] =
{
    { sUnovaAnimFrames_icirrus_r08, ARRAY_COUNT(sUnovaAnimFrames_icirrus_r08), 8 },
    { sUnovaAnimFrames_icirrus_r09, ARRAY_COUNT(sUnovaAnimFrames_icirrus_r09), 9 },
    { sUnovaAnimFrames_icirrus_r18, ARRAY_COUNT(sUnovaAnimFrames_icirrus_r18), 24 },
    { sUnovaAnimFrames_icirrus_r19, ARRAY_COUNT(sUnovaAnimFrames_icirrus_r19), 25 },
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 101 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 102 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 117 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 118 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 4 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaPort[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 70 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 71 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 72 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 73 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaChampionsRoom[] =
{
    { sUnovaAnimFrames_stars_1, ARRAY_COUNT(sUnovaAnimFrames_stars_1), 95 },
    { sUnovaAnimFrames_stars_1_f1, ARRAY_COUNT(sUnovaAnimFrames_stars_1_f1), 96 },
    { sUnovaAnimFrames_stars_1_f2, ARRAY_COUNT(sUnovaAnimFrames_stars_1_f2), 94 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaUnovaWest[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 100 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 101 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 113 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 114 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 2 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaNacrene[] =
{
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 2 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaCastelia[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 87 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 88 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 103 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 104 },
    { sUnovaAnimFrames_castelia_fountain_1, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_1), 36 },
    { sUnovaAnimFrames_castelia_fountain_2, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_2), 46 },
    { sUnovaAnimFrames_castelia_fountain_3, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_3), 38 },
    { sUnovaAnimFrames_castelia_fountain_4, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_4), 37 },
    { sUnovaAnimFrames_castelia_fountain_5, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_5), 47 },
    { sUnovaAnimFrames_castelia_fountain_6, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_6), 48 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaCaveRuins[] =
{
    { sUnovaAnimFrames_cave_ruins_r14, ARRAY_COUNT(sUnovaAnimFrames_cave_ruins_r14), 19 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaDreamyard[] =
{
    { sUnovaAnimFrames_dreamyard_r6f, ARRAY_COUNT(sUnovaAnimFrames_dreamyard_r6f), 112 },
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 110 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 111 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 126 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 127 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaForest[] =
{
    { sUnovaAnimFrames_forest_tree_1, ARRAY_COUNT(sUnovaAnimFrames_forest_tree_1), 11 },
    { sUnovaAnimFrames_forest_tree_3, ARRAY_COUNT(sUnovaAnimFrames_forest_tree_3), 14 },
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 82 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 83 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 90 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 91 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 3 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaMistralton[] =
{
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 4 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaNimbasa[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 85 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 86 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 100 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 101 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 4 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaStriaton[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 103 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 104 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 118 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 119 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 4 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaUnovaNorth[] =
{
    { sUnovaAnimFrames_unova_north_r60, ARRAY_COUNT(sUnovaAnimFrames_unova_north_r60), 96 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 4 },
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 107 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 108 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 120 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 121 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaBridge[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 101 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 102 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 116 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 117 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaOpelucid[] =
{
    { sUnovaAnimFrames_opelucid_r6f, ARRAY_COUNT(sUnovaAnimFrames_opelucid_r6f), 103 },
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 101 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 102 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 108 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 109 },
    { sUnovaAnimFrames_opelucid_r4d, ARRAY_COUNT(sUnovaAnimFrames_opelucid_r4d), 73 },
    { sUnovaAnimFrames_castelia_fountain_1, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_1), 43 },
    { sUnovaAnimFrames_castelia_fountain_2, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_2), 57 },
    { sUnovaAnimFrames_castelia_fountain_3, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_3), 45 },
    { sUnovaAnimFrames_castelia_fountain_4, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_4), 44 },
    { sUnovaAnimFrames_castelia_fountain_5, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_5), 58 },
    { sUnovaAnimFrames_castelia_fountain_6, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_6), 59 },
    { sUnovaAnimFrames_opelucid_r1d, ARRAY_COUNT(sUnovaAnimFrames_opelucid_r1d), 29 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaPlayersHouse[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 101 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 102 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 105 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 106 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaUnderground[] =
{
    { sUnovaAnimFrames_underground_r77, ARRAY_COUNT(sUnovaAnimFrames_underground_r77), 98 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaBattleTowerOutside[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 101 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 102 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 117 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 118 },
    { sUnovaAnimFrames_castelia_fountain_1, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_1), 40 },
    { sUnovaAnimFrames_castelia_fountain_2, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_2), 53 },
    { sUnovaAnimFrames_castelia_fountain_3, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_3), 42 },
    { sUnovaAnimFrames_castelia_fountain_4, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_4), 41 },
    { sUnovaAnimFrames_castelia_fountain_5, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_5), 54 },
    { sUnovaAnimFrames_castelia_fountain_6, ARRAY_COUNT(sUnovaAnimFrames_castelia_fountain_6), 55 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaComplex[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 79 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 80 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 92 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 93 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaDriftveil[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 102 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 103 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 118 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 119 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 4 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaPark[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 60 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 61 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 63 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 64 },
    { sUnovaAnimFrames_flower_cgb_1, ARRAY_COUNT(sUnovaAnimFrames_flower_cgb_1), 2 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaVillageBridge[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 84 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 85 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 96 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 97 },
};

static const struct UnovaTilesetAnim sUnovaAnim_UnovaVirbank[] =
{
    { sUnovaAnimFrames_whirlpool_1, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_1), 106 },
    { sUnovaAnimFrames_whirlpool_2, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_2), 107 },
    { sUnovaAnimFrames_whirlpool_3, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_3), 120 },
    { sUnovaAnimFrames_whirlpool_4, ARRAY_COUNT(sUnovaAnimFrames_whirlpool_4), 121 },
};

void InitTilesetAnim_UnovaCave(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaCave, ARRAY_COUNT(sUnovaAnim_UnovaCave));
}

void InitTilesetAnim_UnovaUnovaBeach(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaUnovaBeach, ARRAY_COUNT(sUnovaAnim_UnovaUnovaBeach));
}

void InitTilesetAnim_UnovaDesert(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaDesert, ARRAY_COUNT(sUnovaAnim_UnovaDesert));
}

void InitTilesetAnim_UnovaEliteFourRoom(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaEliteFourRoom, ARRAY_COUNT(sUnovaAnim_UnovaEliteFourRoom));
}

void InitTilesetAnim_UnovaTower(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaTower, ARRAY_COUNT(sUnovaAnim_UnovaTower));
}

void InitTilesetAnim_UnovaUnovaEast(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaUnovaEast, ARRAY_COUNT(sUnovaAnim_UnovaUnovaEast));
}

void InitTilesetAnim_UnovaAirport(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaAirport, ARRAY_COUNT(sUnovaAnim_UnovaAirport));
}

void InitTilesetAnim_UnovaIcirrus(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaIcirrus, ARRAY_COUNT(sUnovaAnim_UnovaIcirrus));
}

void InitTilesetAnim_UnovaPort(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaPort, ARRAY_COUNT(sUnovaAnim_UnovaPort));
}

void InitTilesetAnim_UnovaChampionsRoom(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaChampionsRoom, ARRAY_COUNT(sUnovaAnim_UnovaChampionsRoom));
}

void InitTilesetAnim_UnovaUnovaWest(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaUnovaWest, ARRAY_COUNT(sUnovaAnim_UnovaUnovaWest));
}

void InitTilesetAnim_UnovaNacrene(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaNacrene, ARRAY_COUNT(sUnovaAnim_UnovaNacrene));
}

void InitTilesetAnim_UnovaCastelia(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaCastelia, ARRAY_COUNT(sUnovaAnim_UnovaCastelia));
}

void InitTilesetAnim_UnovaCaveRuins(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaCaveRuins, ARRAY_COUNT(sUnovaAnim_UnovaCaveRuins));
}

void InitTilesetAnim_UnovaDreamyard(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaDreamyard, ARRAY_COUNT(sUnovaAnim_UnovaDreamyard));
}

void InitTilesetAnim_UnovaForest(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaForest, ARRAY_COUNT(sUnovaAnim_UnovaForest));
}

void InitTilesetAnim_UnovaMistralton(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaMistralton, ARRAY_COUNT(sUnovaAnim_UnovaMistralton));
}

void InitTilesetAnim_UnovaNimbasa(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaNimbasa, ARRAY_COUNT(sUnovaAnim_UnovaNimbasa));
}

void InitTilesetAnim_UnovaStriaton(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaStriaton, ARRAY_COUNT(sUnovaAnim_UnovaStriaton));
}

void InitTilesetAnim_UnovaUnovaNorth(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaUnovaNorth, ARRAY_COUNT(sUnovaAnim_UnovaUnovaNorth));
}

void InitTilesetAnim_UnovaBridge(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaBridge, ARRAY_COUNT(sUnovaAnim_UnovaBridge));
}

void InitTilesetAnim_UnovaOpelucid(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaOpelucid, ARRAY_COUNT(sUnovaAnim_UnovaOpelucid));
}

void InitTilesetAnim_UnovaPlayersHouse(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaPlayersHouse, ARRAY_COUNT(sUnovaAnim_UnovaPlayersHouse));
}

void InitTilesetAnim_UnovaUnderground(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaUnderground, ARRAY_COUNT(sUnovaAnim_UnovaUnderground));
}

void InitTilesetAnim_UnovaBattleTowerOutside(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaBattleTowerOutside, ARRAY_COUNT(sUnovaAnim_UnovaBattleTowerOutside));
}

void InitTilesetAnim_UnovaComplex(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaComplex, ARRAY_COUNT(sUnovaAnim_UnovaComplex));
}

void InitTilesetAnim_UnovaDriftveil(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaDriftveil, ARRAY_COUNT(sUnovaAnim_UnovaDriftveil));
}

void InitTilesetAnim_UnovaPark(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaPark, ARRAY_COUNT(sUnovaAnim_UnovaPark));
}

void InitTilesetAnim_UnovaVillageBridge(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaVillageBridge, ARRAY_COUNT(sUnovaAnim_UnovaVillageBridge));
}

void InitTilesetAnim_UnovaVirbank(void)
{
    InitUnovaTilesetAnim(sUnovaAnim_UnovaVirbank, ARRAY_COUNT(sUnovaAnim_UnovaVirbank));
}
