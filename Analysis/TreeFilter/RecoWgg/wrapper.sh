#. /afs/cern.ch/sw/lcg/external/gcc/4.6/x86_64-slc6/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.07_python2.7/x86_64-slc6-gcc46-opt/root/bin/thisroot.sh
export LD_LIBRARY_PATH=/afs/cern.ch/sw/lcg/contrib/gcc/4.6/x86_64-slc6-gcc46-opt/lib64:$LD_LIBRARY_PATH
#export ROOTSYS=/afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.07_python2.7/x86_64-slc6-gcc46-opt/root

/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/RecoWgg/RunAnalysisTEST.exe --conf_file /afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/RecoWgg/job_muon_2012a_Jan22rereco.txt
