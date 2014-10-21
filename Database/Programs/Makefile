EXE_DIR = ./
OBJ_DIR = obj/
SRC_DIR = src/
INC_DIR = include/

EXENAME=Test

EXE = $(EXE_DIR)/$(EXENAME)

OCCIPATH=/afs/cern.ch/sw/lcg/external/oracle/11.2.0.3.0/x86_64-slc5-gcc43-opt/
BOOSTINC=/afs/cern.ch/sw/lcg/external/Boost/1.50.0_python2.7/x86_64-slc5-gcc43-opt/include/boost-1_50
OCCILIBS=-libocci

$(EXE): $(SRC_DIR)/DatabaseExplorer.cc
	g++ $^ -o $@ -I$(OCCIPATH)/include -I$(BOOSTINC) -L$(OCCIPATH)/lib  -locci -lclntsh -lnnz11

