#!/bin/tcsh
source /afs/cern.ch/sw/lcg/external/gcc/4.3.2/x86_64-slc5/setup.csh
set ARGS=($_)
set THIS="`dirname ${ARGS[2]}`"
#setenv ROOTSYS "`(cd ${THIS}/..;pwd)`"
#setenv ROOTSYS "/afs/cern.ch/cms/slc5_amd64_gcc434/lcg/root/5.28.00b"
#setenv ROOTSYS "/afs/cern.ch/sw/lcg/app/releases/ROOT/5.28.00b/x86_64-slc5-gcc43-opt/root"

#setenv ROOTSYS "/afs/cern.ch/sw/lcg/app/releases/ROOT/5.30.04/x86_64-slc5-gcc43-opt/root"
setenv ROOTSYS "/afs/cern.ch/sw/lcg/app/releases/ROOT/5.30.02/x86_64-slc5-gcc43-opt/root"
if ($?MANPATH) then
# Nothing to do
else
   # Grab the default man path before setting the path to avoid duplicates 
   if ( -X manpath ) then
      set default_manpath = `manpath`
   else
      set default_manpath = `man -w`
   endif
endif

set path = ($ROOTSYS/bin $path)
if ($?LD_LIBRARY_PATH) then
   setenv LD_LIBRARY_PATH $ROOTSYS/lib:$LD_LIBRARY_PATH      # Linux, ELF HP-UX
else
   setenv LD_LIBRARY_PATH $ROOTSYS/lib
endif

if ($?PYTHONPATH) then
   setenv PYTHONPATH $ROOTSYS/lib:$PYTHONPATH
else
   setenv PYTHONPATH $ROOTSYS/lib
endif

if ($?MANPATH) then
   setenv MANPATH `dirname $ROOTSYS/man/man1`:$MANPATH
else
   setenv MANPATH `dirname $ROOTSYS/man/man1`:$default_manpath
endif
