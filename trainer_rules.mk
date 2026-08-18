# party files are run through trainerproc, which is a tool that converts party data to an output file
# matching the current trainer .h formatting

AUTO_GEN_TARGETS += src/data/trainers.h
AUTO_GEN_TARGETS += src/data/trainers_frlg.h
AUTO_GEN_TARGETS += src/data/battle_partners.h
AUTO_GEN_TARGETS += test/battle/trainer_control.h
AUTO_GEN_TARGETS += test/battle/partner_control.h
AUTO_GEN_TARGETS += src/data/debug_trainers.h
AUTO_GEN_TARGETS += include/constants/trainers_dense.h
AUTO_GEN_TARGETS += src/data/trainers_index.h

%.h: %.party $(TRAINERPROC)
	$(CPP) $(CPPFLAGS) -traditional-cpp - < $< | $(TRAINERPROC) -o $@ -i $< -

# ponytail: só o .party de Emerald ganha a indireção densa (-d/-x, ver D1 do PRD).
# FRLG tem 144 vagas vazias e os .party de teste/parceiro têm um punhado: nenhum
# deles paga a tabela de índice de 8 KB, então continuam indexados pelo id cru.
#
# Uma passada do gerador escreve os TRÊS arquivos, mas cada um precisa da própria
# regra: com receita vazia, apagar só um deles não o traz de volta (make acha que
# está pronto porque o irmão está). Encadeados de propósito, para que -j nunca
# rode duas passadas ao mesmo tempo escrevendo os mesmos arquivos.
define trainerproc_emerald
$(CPP) $(CPPFLAGS) -traditional-cpp - < src/data/trainers.party | $(TRAINERPROC) \
	-o src/data/trainers.h -i src/data/trainers.party \
	-d include/constants/trainers_dense.h -x src/data/trainers_index.h -
endef

src/data/trainers.h: src/data/trainers.party $(TRAINERPROC)
	$(trainerproc_emerald)

include/constants/trainers_dense.h: src/data/trainers.h
	$(trainerproc_emerald)

src/data/trainers_index.h: include/constants/trainers_dense.h
	$(trainerproc_emerald)
