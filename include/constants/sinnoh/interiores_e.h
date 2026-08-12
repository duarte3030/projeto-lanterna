// ponytail: ids de evento de Sinnoh, grupo "interiores_e".

// Twinleaf_Town_RivalsHouse_F2
#define LOCALID_RIVALSHOUSEF2_SISTER 1

// TwinleafTown_Haouse1
#define LOCALID_HAOUSE1_EXPERT 1
#define LOCALID_HAOUSE1_TWIN 2

// TwinleafTown_House2 (sprite GUITARIST inexistente, usado MAN_3 como no mapa de referencia TwinleafTown)
#define LOCALID_HOUSE2_GUITARIST 1

// SandgemTown_RivalHouse_F1
#define LOCALID_RIVALHOUSEF1_TWIN 1

// SandgemTown_House1 voltou a ser casa comum em 05/08/2026, quando o
// laboratorio ganhou mapa proprio (SandgemTown_RowanLab). Ate entao as duas
// portas de Sandgem entravam no MESMO interior.
#define LOCALID_HOUSE1_BREEDER_M 1
#define LOCALID_HOUSE1_BREEDER_F 2

// SandgemTown_RowanLab e o LABORATORIO DE POKEMON DO PROFESSOR ROWAN.
// Mapa proprio desde 05/08/2026, no FIM de gMapGroup_IndoorSandgem (mapa novo no
// meio de um grupo desloca os indices que a save guarda; ver guarda_save.py).
// Reusa LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB, o interior de laboratorio
// que ja existe no repo: nenhuma arte nova, nenhum blockdata novo.
// Sprites: ROWAN nao existe no GBA, usado PROF_BIRCH; BARRY nao existe,
// usado RICH_BOY (mesma troca que SandgemTown ja fazia).
#define LOCALID_ROWAN_LAB_ROWAN 1
#define LOCALID_ROWAN_LAB_ASSISTANT 2
#define LOCALID_ROWAN_LAB_RIVAL 3
#define LOCALID_ROWAN_LAB_BALL_TURTWIG 4
#define LOCALID_ROWAN_LAB_BALL_CHIMCHAR 5
#define LOCALID_ROWAN_LAB_BALL_PIPLUP 6

// SandgemTown_PokemonCenter_1F
#define LOCALID_SANDGEM_POKECENTER1F_NURSE 1

// SandgemTown_PokemonCenter_2F
#define LOCALID_SANDGEM_POKECENTER2F_TEALA1 1
#define LOCALID_SANDGEM_POKECENTER2F_TEALA2 2

// SandgemTown_Mart (sprites CASHIER_F e POKEMON_BREEDER_M inexistentes; usados MART_EMPLOYEE e POKEFAN_M)
#define LOCALID_SANDGEM_MART_CLERK 1

// JubilifeCity_PokemonSchool (sem dado de origem; NPCs inventados, sprites TEACHER/SCHOOL_KID_F inexistentes, usados WOMAN_2/LASS/YOUNGSTER)
#define LOCALID_SCHOOL_TEACHER 1
#define LOCALID_SCHOOL_KID_1 2
#define LOCALID_SCHOOL_KID_3 3

// JubilifeCity_JubilifeTV_F1 (sprites GYM_GUIDE/MIDDLE_AGED_MAN/ACE_TRAINER_SNOW_F/ACE_TRAINER_M inexistentes;
// usados GYM_GUY/MAN_4/WOMAN_3/COOLTRAINER_M. Lottery Corner vira NPC de flavor, sistema de sorteio nao ligado.)
#define LOCALID_TVF1_PRESIDENT 1
#define LOCALID_TVF1_LOTTERY 2

// JubilifeCity_JubilifeTV_F2 (LOCALID_REPORTER pulado, flag de historia;
// sprites IDOL/ROUGHNECK inexistentes, usados WOMAN_5/BIKER; GYM_GUIDE reusa GYM_GUY)
#define LOCALID_TVF2_IDOL 1
#define LOCALID_TVF2_DESKMAN 2

// JubilifeCity_JubilifeTV_F3 (GYM_GUIDE reusa sprite GYM_GUY, ja usado em F1/F2)

