#export GCC_LIB=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/gcc/5.3.0/lib64
#export BOOST_LIB=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/boost/1.57.0-ikhhed/lib
#export PYTHONDIR=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/python/2.7.11-ikhhed
##export GCC_LIB=/afs/cern.ch/sw/lcg/contrib/gcc/4.6/x86_64-slc6-gcc46-opt/lib64
##export BOOST_LIB=/afs/cern.ch/sw/lcg/external/Boost/1.50.0_python2.7/x86_64-slc5-gcc43-opt/lib
##export PYTHONDIR=/afs/cern.ch/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc47-opt
#export ROOTSYS=/afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.07_python2.7/x86_64-slc6-gcc46-opt/root
## source ROOT environment
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.07_python2.7/x86_64-slc6-gcc46-opt/root/bin/thisroot.sh
## set library paths
#export LD_LIBRARY_PATH=$GCC_LIB:$BOOST_LIB:$PYTHON_DIR/lib:$LD_LIBRARY_PATH
## add python to path
export PATH=$PYTHONDIR/bin:$PATH
# add python includes
#export PYTHONPATH=$ROOTSYS/lib:$PYTHONDIR/lib:$HOME/.python:$PYTHONPATH:$HOME/Programs/python:$HOME/Programs/python/numpy-1.8.1/build/lib.linux-x86_64-2.7/
# add paths within this package
export WorkArea=$PWD/Analysis
export PYTHONPATH=$PYTHONPATH:${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting
