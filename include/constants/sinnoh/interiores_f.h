// ponytail: ids de evento de Sinnoh, grupo "interiores_f".
// Arquivo proprio por grupo: varios agentes escrevem em paralelo, e um arquivo
// unico virava corrida de escrita. Padrao: LOCALID_<MAPA>_<QUEM>, de 1 em diante
// dentro de cada mapa.

// JubilifeCity_JubilifeTV_F4 (sprites MIDDLE_AGED_MAN/RECEPTIONIST/POKEMON_BREEDER_F
// inexistentes; usados MAN_4/UNION_ROOM_RECEPTIONIST/WOMAN_3, mesmos substitutos
// ja usados em JubilifeTV_F1-F3)
#define LOCALID_TVF4_PRESIDENT 1
#define LOCALID_TVF4_RECEPTIONIST 2
#define LOCALID_TVF4_BREEDER 3

// JubilifeCity_PoketchCompany_F1 (LOCALID_REPORTER e LOCALID_POKETCH_CO_PRESIDENT
// pulados, presos a flag de historia FLAG_HIDE_*; sprite RECEPTIONIST inexistente,
// usado UNION_ROOM_RECEPTIONIST)
#define LOCALID_POKETCHF1_SCIENTIST 1
#define LOCALID_POKETCHF1_RECEPTIONIST 2
#define LOCALID_POKETCHF1_LASS 3

// JubilifeCity_PoketchCompany_F2 (LOCALID_PACHIRISU pulado, sem sprite de Pachirisu
// disponivel)
#define LOCALID_POKETCHF2_POKEFAN_M 1
#define LOCALID_POKETCHF2_OLDMAN 2
#define LOCALID_POKETCHF2_CLEFAIRY 3

// JubilifeCity_PoketchCompany_F3
#define LOCALID_POKETCHF3_NINJA_BOY 1
#define LOCALID_POKETCHF3_POKEFAN_F 2
#define LOCALID_POKETCHF3_EXPERT_F 3

// JubilifeCity_Flat1_F1 (jubilife_city_condominiums_1f; LOCALID_PACHIRISU pulado,
// sem sprite disponivel)
#define LOCALID_FLAT1F1_EXPERT_F 1
#define LOCALID_FLAT1F1_PIKACHU 2
#define LOCALID_FLAT1F1_BEAUTY 3

// JubilifeCity_Flat1_F2 (jubilife_city_condominiums_2f; sprite POKEMON_BREEDER_M
// inexistente, usado POKEFAN_M, mesmo substituto ja usado em SandgemTown_House1)
#define LOCALID_FLAT1F2_BUG_CATCHER 1
#define LOCALID_FLAT1F2_BREEDER_M 2

// JubilifeCity_Flat1_F3 (unused_jubilife_city_condominiums_3f; sprite COLLECTOR
// inexistente, usado MAN_5)
#define LOCALID_FLAT1F3_LASS 1
#define LOCALID_FLAT1F3_COLLECTOR 2

// JubilifeCity_Flat2_F1 (jubilife_city_south_house_1f; sprite ACE_TRAINER_M
// inexistente, usado COOLTRAINER_M; LOCALID_PACHIRISU pulado)
#define LOCALID_FLAT2F1_ACE_TRAINER_M 1
#define LOCALID_FLAT2F1_LASS 2

// JubilifeCity_Flat2_F2 (jubilife_city_south_house_2f; sprite POKEMON_BREEDER_F
// inexistente, usado WOMAN_3)
#define LOCALID_FLAT2F2_YOUNGSTER 1
#define LOCALID_FLAT2F2_POKEFAN_F 2
#define LOCALID_FLAT2F2_BREEDER_F 3

// JubilifeCity_Flat2_F3 (unused_jubilife_city_south_house_3f)
#define LOCALID_FLAT2F3_POKEFAN_M 1

// JubilifeCity_Flat3_F1 (jubilife_city_southwest_house_1f; sprite
// POKETCH_CO_PRESIDENT/MIDDLE_AGED_MAN inexistente, usado MAN_4)
#define LOCALID_FLAT3F1_YOUNGSTER 1
#define LOCALID_FLAT3F1_PIKACHU 2
#define LOCALID_FLAT3F1_PRESIDENT 3

// JubilifeCity_Flat3_F2 (jubilife_city_southwest_house_2f; sprite ACE_TRAINER_M
// inexistente, usado COOLTRAINER_M; LOCALID_COLLECTOR do dado de origem cortado,
// apartamento aceita no maximo 3 NPCs e o dado trazia 4)
#define LOCALID_FLAT3F2_ACE_TRAINER_M 1
#define LOCALID_FLAT3F2_BEAUTY 2
#define LOCALID_FLAT3F2_LASS 3

// JubilifeCity_Flat3_F3 (sem dado de origem; NPCs inventados no tom do predio)
#define LOCALID_FLAT3F3_YOUNGSTER 1
#define LOCALID_FLAT3F3_OLD_MAN 2
