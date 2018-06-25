
#************************************************************************************
#
# filter.py
#
# Author : Josh Kunkle  (jkunkle@cern.ch)
#
# This script is called to run the analysis.  All of the heavy lifting
# is in the core package, so just import it, parse the options, and run
# The only work that is done here is to determine the package path
# so that the generated c++ files go into the correct place
# Example
# python scripts/filter.py --filesDir /store/user/jkunkle/MinimumBias/HCALLaser_v1/170630_081709/0000/ --outputDir /data/users/jkunkle/HCAL/LaserHists_2017_07_15 --outputFile hists.root --module scripts/ConfTemplate.py --treeName hcalTupleTree/tree --nFilesPerJob 1 --condor

import os
import core

options = core.ParseArgs()

#*************************************
# get the path of this script
#*************************************
script_path = os.path.realpath(__file__)
package_name = script_path.split('/')[-3]

# run it!
core.config_and_run( options, package_name )

