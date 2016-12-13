"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

                                                                                       
p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')

p.add_argument('--save'          , default=False, action='store_true',   dest='save'        , help='save plots ( must provide outputDir )')
p.add_argument('--detailLevel'   , default=100, type=int, dest='detailLevel'      , help='make only plots at this detail level (make all plots by default)')
p.add_argument('--makeAll'       , default=False, action='store_true',   dest='makeAll'     , help='make all plots')
p.add_argument('--makePhotonComp'     , default=False, action='store_true',   dest='makeEvent'   , help='make Wgg event plots')

options = p.parse_args()

import sys
import os
import re
import math
import uuid
import copy
import imp
import ROOT
from array import array

from SampleManager import SampleManager

ROOT.gROOT.SetBatch(False)

def main() :

    global samplesPhoton

    baseDirPhoton  = '/data/users/jkunkle/RecoPhoton/Photon_2015_11_23'

    treename = 'tupel/EventTree'
    filename = 'tree.root'

    sampleConfPhoton = 'Modules/SinglePhoton15.py'
    xsfile = 'cross_sections/photon15.py'

    lumi=2093.

    samplesPhoton   = SampleManager(baseDirPhoton, treename, filename=filename, xsFile=xsfile, lumi=lumi, quiet=options.quiet)

    samplesPhoton    .ReadSamples( sampleConfPhoton )

    if options.save :
        ROOT.gROOT.SetBatch(True)

    if options.outputDir is not None :
        samplesPhoton.start_command_collection()

    if options.makeAll or options.makePhotonComp :
        MakePhotonCompPlots( save=options.save, detail=options.detailLevel )

    samplesPhoton.run_commands(nFilesPerJob=1, treeName=treename)

#---------------------------------------
def MakePhotonCompPlots( save=False, detail=100, ph_cuts='', dirPostfix='', activate_data=False ) :

    subdir='PhotonCompPlots%s' %dirPostfix


    if save and options.outputDir is None :
        print 'Must provide an outputDir to save plots'
        save=False

    pt_bins = [(15,20), (20,30), (30,40), (40,50), (50,60), (60,80), (80, 100), (100, None ) ]
    regions = ['EB', 'EE']

    fitvars = ['ph_sigmaIEIE', 'ph_chIsoCorr', 'ph_phoIsoCorr']
    countvars = ['ph_mediumNoSIEIENoEleVeto_n', 'ph_mediumNoChIsoNoEleVeto_n', 'ph_mediumNoPhoIsoNoEleVeto_n']
    idxvars = ['ptSorted_ph_mediumNoSIEIENoEleVeto_idx', 'ptSorted_ph_mediumNoChIsoNoEleVeto_idx', 'ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx']
    binnings = { 'EB' : {
                         'ph_sigmaIEIE' : ( 30, 0, 0.03), 'ph_chIsoCorr' : (40, 0, 52.4), 'ph_phoIsoCorr' : (30, 0, 39.9),
                        },
                 'EE' : {
                          'ph_sigmaIEIE' : ( 30, 0, 0.0801), 'ph_chIsoCorr' : (40, 0, 50), 'ph_phoIsoCorr' : (50, 0, 51),
                        }
                 }

    ylabels = { 'EB' : {
                         'ph_sigmaIEIE' : 'Normalized Events / 0.001', 'ph_chIsoCorr' : 'Normalized Events / 1.31', 'ph_phoIsoCorr' : 'Normalized Events / 1.33',
                        },
                 'EE' : {
                          'ph_sigmaIEIE' : 'Normalized Events / 0.00267', 'ph_chIsoCorr' : 'Normalized Events / 1.25', 'ph_phoIsoCorr' : 'Normalized Events / 1.02',
                        }
                 }

    loose_cuts = { 'EB' : {
                         'ph_sigmaIEIE' : 0.014,  'ph_chIsoCorr' : 5.24, 'ph_phoIsoCorr' : 5.32,
                        },
                   'EE' : {
                          'ph_sigmaIEIE' : 0.1068, 'ph_chIsoCorr' : 5, 'ph_phoIsoCorr' : 4.08,
                          }
                 }


    labels = ['#sigma i#eta i#eta', 'charged had. Iso', 'photon Iso']

    for reg in regions :

        for ptmin, ptmax in pt_bins :

            for fitv, countv, idxv, label in zip( fitvars, countvars, idxvars, labels ) :

                if ptmax is None :
                    pt_sel = 'ph_pt[%s[0]] > %d ' %(idxv, ptmin )
                    ptstr = 'pt_%d-max' %ptmin
                else :
                    pt_sel = 'ph_pt[%s[0]] > %d && ph_pt[%s[0]] < %d ' %(idxv, ptmin, idxv, ptmax )
                    ptstr = 'pt_%d-%d' %(ptmin,ptmax)

                reg_sel = 'ph_Is%s[%s[0]] ' %( reg, idxv )

                str_qcd = '%s==1 && !( ph_truthMatch_ph[%s[0]] && abs(ph_truthMatchMotherPID_ph[%s[0]]) < 25 ) && %s && %s '%( countv, idxv, idxv, pt_sel, reg_sel )

                str_ll = 'mu_n==2 && %s' %str_qcd
                str_lv = 'mu_n==1 && %s' %str_qcd
    
                varstr = '%s[%s[0]]' %( fitv, idxv )

                ylabel = ylabels[reg][fitv]

                samplesPhoton.CompareSelections( varstr , [str_qcd, str_ll, str_lv],  ['QCD', 'DYJetsToLL', 'WJetsToLNu'], binnings[reg][fitv], hist_config={'colors' : [ROOT.kBlack, ROOT.kRed, ROOT.kGreen], 'normalize' : True, 'ymin' : 0, 'ymax' : 0.6, 'xlabel' : label, 'ylabel' : ylabel, 'doratio':1 } )


                if save :
                    name = 'phComp__%s__%s__%s' %( fitv, reg, ptstr )
                    samplesPhoton.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
                else :
                    raw_input('continue')

                loose_cut = '%s[%s[0]] < %f ' %( fitv, idxv, loose_cuts[reg][fitv] )

                str_qcd_loose = str_qcd + ' && %s' %loose_cut
                str_ll_loose = str_ll + ' && %s' %loose_cut
                str_lv_loose = str_lv + ' && %s' %loose_cut

                samplesPhoton.CompareSelections( varstr , [str_qcd_loose, str_ll_loose, str_lv_loose],  ['QCD', 'DYJetsToLL', 'WJetsToLNu'], binnings[reg][fitv], hist_config={'colors' : [ROOT.kBlack, ROOT.kRed, ROOT.kGreen], 'normalize' : True, 'ymin' : 0, 'ymax' : 0.6, 'xlabel' : label, 'ylabel' : ylabel, 'doratio':1 } )

                if save :
                    name = 'phCompLooseCut__%s__%s__%s' %( fitv, reg, ptstr )
                    samplesPhoton.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
                else :
                    raw_input('continue')

main()
