setenv WorkArea ${PWD}/Analysis
setenv PYTHONPATH ${PYTHONPATH}:${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python
#Set boost library path if on the UMD Cluster
if(`echo $HOSTNAME | cut -c0-13` == "interactive-0") then
    setenv LD_LIBRARY_PATH /cvmfs/cms.cern.ch/slc5_amd64_gcc481/external/boost/1.51.0-cms/lib:$LD_LIBRARY_PATH
endif
