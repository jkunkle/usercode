###############################################################################
# 
# Makefile 
#
# Author : Josh Kunkle jkunkle@cern.ch
#
# Compile the local package and link to the Core package
#
# Tasks : CLEANUP
################################################################################


EXE_DIR = ./
OBJ_DIR = obj/
SRC_DIR = src/
INC_DIR = ${PWD}

WORK_AREA = ${WorkArea}

ROOTCONFIG   = root-config

ROOTCXXFLAGS = $(shell $(ROOTCONFIG) --cflags)
ROOTLIBS     = $(shell $(ROOTCONFIG) --libs) -lTreePlayer -lTMVA

BOOSTFLAGS   = -I/afs/cern.ch/sw/lcg/external/Boost/1.50.0_python2.7/x86_64-slc5-gcc43-opt/include/boost-1_50 -L/afs/cern.ch/sw/lcg/external/Boost/1.50.0_python2.7/x86_64-slc5-gcc43-opt/lib

COREINC = -I$(WORK_AREA)/TreeFilter/Core/
COREOBJ = $(WORK_AREA)/TreeFilter/Core/obj/AnalysisBase.o $(WORK_AREA)/TreeFilter/Core/obj/Util.o

# we need to link against an additional library if using root>5.24
NEWROOTVERSION  = $(shell $(ROOTCONFIG) --version | grep -c "5.24" )
ifeq ($(NEWROOTVERSION),1)
	ROOTLIBS +=  -lRIO
endif

LIBS         = $(ROOTLIBS) $(BOOSTFLAGS) -lboost_filesystem-gcc43-mt-1_50 -lboost_system-gcc43-mt-1_50 
DEBUG        = false
INCLUDE      = $(ROOTCXXFLAGS) $(BOOSTFLAGS) $(COREINC)

# do something like 
#  make DEBUG=true
# to activate the debug options
ifeq ($(DEBUG),true)
	CXXFLAGS     = -O0 -Wall -ggdb -fPIC -I$(INC_DIR) $(INCLUDE)
	LDFLAGS      = -O0 -Wall -ggdb -I$(INC_DIR) $(INCLUDE) 
else
	CXXFLAGS     = -O2 -Wall -fPIC -I$(INC_DIR) $(INCLUDE)
	LDFLAGS      = -O2 -I$(INC_DIR) $(INCLUDE) 
endif

OBJECT_ANA = $(OBJ_DIR)/RunAnalysis.o 
BRANCH_INIT = $(OBJ_DIR)/BranchInit.o
LINKDEF = $(OBJ_DIR)/cintLib.so

EXE = $(EXE_DIR)/RunAnalysis

# Main targets

all:   $(EXE) 

$(SRC_DIR)/Dict.cxx: $(INC_DIR)/include/LinkDef.h
	rootcint -f $@ -c $(CXXFLAGS) -p $^

$(LINKDEF):  $(SRC_DIR)/Dict.cxx
	g++ -shared -o$@ `root-config --ldflags` $(CXXFLAGS) -I$(ROOTSYS)/include $^

$(OBJ_DIR)/%.o : $(SRC_DIR)/%.cxx
	g++ $(CXXFLAGS) -c $^ -o $@ -I../$(INC_DIR)

$(EXE): $(OBJECT_ANA) $(BRANCH_INIT) $(LINKDEF) 
	g++ $(CXXFLAGS) -o $@ -g $^ $(COREOBJ) $(LIBS) -I../$(INC_DIR)
clean:
	@echo -e "\n\n===> cleaning directories"
	rm -f $(OBJ_DIR)/*.o 
