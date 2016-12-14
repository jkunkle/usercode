setenv WorkArea ${PWD}/Analysis
if( $?PYTHONPATH == 0 ) then
   setenv PYTHONPATH ${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting
else 
   setenv PYTHONPATH ${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting:$PYTHONPATH
endif

if(`echo $HOSTNAME | awk -F "-" '{print $1}'` == "hepcms") then
    if( $?LD_LIBRARY_PATH == 0 ) then 
        setenv LD_LIBRARY_PATH /cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/boost/1.57.0-cms/lib
    else 
        setenv LD_LIBRARY_PATH /cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/boost/1.57.0-cms/lib:$LD_LIBRARY_PATH
endif


