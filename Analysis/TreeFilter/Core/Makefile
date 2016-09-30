###############################################################################
#
# 
# Makefile       (RPB2010088)
#
# Targets: 
# - main executables  
# - library (which can be loaded within root: gSystem->Load("lib/hwwLib.so") )
# 
#
################################################################################


CERNLOC=CERN
UMDLOC=UMD

HOSTNAME := $(shell hostname)
ifneq (,$(findstring lxplus,$(HOSTNAME))) #find lxplus in host, if found result is non-empty
	LOCATION=$(CERNLOC)
else 
	LOCATION=$(UMDLOC)
endif 

CXX     = g++
LD      = g++

BIN_DIR = ./
OBJ_DIR = obj/
SRC_DIR = src/
INC_DIR = Core

#ROOTCINT     = $(ROOTSYS)/bin/rootcint
#ROOTCONFIG   = $(ROOTSYS)/bin/root-config
ROOTCINT     = rootcint
ROOTCONFIG   = root-config
ROOTCXXFLAGS = $(shell $(ROOTCONFIG) --cflags)
ROOTLIBS     = $(shell $(ROOTCONFIG) --libs) -lTreePlayer -lTMVA #-lBoost

ifeq ($(LOCATION), $(CERNLOC))
	BOOSTFLAGS   = -I/afs/cern.ch/sw/lcg/external/Boost/1.50.0_python2.7/x86_64-slc5-gcc43-opt/include/boost-1_50

endif

ifeq ($(LOCATION), $(UMDLOC))
	BOOSTFLAGS   = -I/cvmfs/cms.cern.ch/slc5_amd64_gcc481/external/boost/1.51.0-cms/include
endif

# we need to link against an additional library if using root>5.24
NEWROOTVERSION  = $(shell $(ROOTCONFIG) --version | grep -c "5.24" )
ifeq ($(NEWROOTVERSION),1)
	ROOTLIBS +=  -lRIO
endif
LIBS         = $(ROOTLIBS) $(BOOSTFLAGS)
DEBUG        = false
INCLUDE      = $(ROOTCXXFLAGS) $(BOOSTFLAGS)


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

OBJECT_BASE = $(OBJ_DIR)/AnalysisBase.o $(OBJ_DIR)/Util.o

# Main targets
#
all : $(OBJECT_BASE)

$(OBJ_DIR)/%.o : $(SRC_DIR)/%.cxx
	$(CXX) $(CXXFLAGS) -c $^ -o $@ -I../Core

clean:
	@echo -e "\n\n===> cleaning directories"
	rm -f $(OBJ_DIR)/*.o 
