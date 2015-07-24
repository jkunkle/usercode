
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
#
# Example:
# python scripts/filter.py --files root://eoscms//eos/cms/store/user/cranelli/WGamGam/NLO_ggNtuples/job_NLO_WAA_ISR.root --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/WAANLOTruth_2015_07_14/job_NLO_WAA_ISR --module scripts/ConfTruthFilter.py --treeName ggNtuplizer/EventTree

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


