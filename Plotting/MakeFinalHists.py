"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

                                                                                       
p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',         help='base directory for histograms')
p.add_argument('--baseDirComb',     default=None,  type=str ,        dest='baseDirComb',         help='base directory for combined histograms')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')
p.add_argument('--savePostfix',     default='',   dest='savePostfix',         help='Save plots in this form (eg .png)')
p.add_argument('--doRatio',     default=False,action='store_true',   dest='doRatio',         help='Make ratio plots')

p.add_argument('--muon',         default=False,  action='store_true' ,        dest='muon',         help='make muon channel plots')
p.add_argument('--electron',     default=False,  action='store_true' ,        dest='electron',         help='make electron channel plots')
p.add_argument('--combined',     default=False,  action='store_true' ,        dest='combined',         help='make combined plots')
p.add_argument('--zgg',          default=False,  action='store_true' ,        dest='zgg',             help='make zgg plots')

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

samplesWgg = None

def main() :

    global samplesWgg
    global samplesZgg
    global samplesWggComb
    global samplesWggBkgSub

    sampleConfWgg = 'Modules/WggFinal.py'
    if options.zgg :
        sampleConfWgg = 'Modules/ZggFinal.py'
    sampleConfWggBkgSub = 'Modules/WggFinalBkgSub.py'

    samplesWgg       = SampleManager(options.baseDir, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)
    #samplesWggComb   = SampleManager(options.baseDirComb, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)
    #samplesWggBkgSub = SampleManager(options.baseDirComb, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)

    samplesWgg        .ReadSamples( sampleConfWgg )
    #samplesWggComb    .ReadSamples( sampleConfWgg )
    #samplesWggBkgSub  .ReadSamples( sampleConfWggBkgSub )

    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)

    dumpStack=True
    samplesWgg.activate_sample( 'AllBkg')
    samplesWgg.activate_sample( 'ZggNoSyst')
    samplesWgg.activate_sample( 'AllBkgPlusSig')

    if options.zgg : 
        MakeZggPlots( options.outputDir, selection='muZgg', var='pt_leadph12', suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack )
        MakeZggPlots( options.outputDir, selection='elZgg', var='pt_leadph12', suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack )
        #MakeZggPlots( options.outputDir, selection='muZgg', var='m_ph1_ph2'  , suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack )
        #MakeZggPlots( options.outputDir, selection='muZgg', var='pt_ph1_ph2' , suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack )
        #MakeZggPlots( options.outputDir, selection='elZgg', var='m_ph1_ph2'  , suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack )
        #MakeZggPlots( options.outputDir, selection='elZgg', var='pt_ph1_ph2' , suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack )
    if options.electron :
        MakeElectronPlots(options.outputDir, selection='elfullhighmt', var='pt_leadph12', suffix='', ylabel='Events / bin',label_style='fancy', dumpStack=dumpStack  )
        #MakeElectronPlots(options.outputDir, selection='elfullhighmt', var='m_ph1_ph2'  , suffix='', ylabel='Events / bin',label_style='fancy', dumpStack=dumpStack  )
        #MakeElectronPlots(options.outputDir, selection='elfullhighmt', var='pt_ph1_ph2' , suffix='', ylabel='Events / bin',label_style='fancy', dumpStack=dumpStack  )
    if options.muon :
        MakeMuonPlots(options.outputDir, selection='muhighmt', var='pt_leadph12', suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack  )
        #MakeMuonPlots(options.outputDir, selection='muhighmt', var='m_ph1_ph2'  , suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack  )
        #MakeMuonPlots(options.outputDir, selection='muhighmt', var='pt_ph1_ph2' , suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack  )
    if options.combined :
        MakeCombinedPlots( options.outputDir, dumpStack=dumpStack )

    dumpStack=False
    samplesWgg.deactivate_sample( 'AllBkg' )
    samplesWgg.deactivate_sample( 'ZggNoSyst')
    samplesWgg.deactivate_sample( 'AllBkgPlusSig')
    xlabel_ptg = 'p_{T}^{lead #gamma} [GeV]'
    xlabel_ptgg = 'p_{T}^{#gamma #gamma} [GeV]'
    xlabel_mgg = 'M_{#gamma #gamma} [GeV]'
    xlabel_mee = 'M_{ee} [GeV]'
    xlabel_mmm = 'M_{#mu#mu} [GeV]'
    xlabel_meegg = 'M_{ee#gamma#gamma} [GeV]'
    xlabel_mmmgg = 'M_{#mu#mu#gamma#gamma} [GeV]'


    selections_wgg_mu = [ 
        {'selection' : 'muhighmt'     , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 80, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        {'selection' : 'mulowmt'      , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 60, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },

        #{'selection' : 'muhighmt'     , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 60, 'ymax_pergev' : 5  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'muhighmt'     , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 45, 'ymax_pergev' : 7  , 'ymin_logy' : 0.5, 'ymax_logy' :30   },
        #{'selection' : 'mulowmt'      , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 40, 'ymax_pergev' : 4  , 'ymin_logy' : 0.01, 'ymax_logy' :20   },
        #{'selection' : 'mulowmt'      , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 45, 'ymax_pergev' : 7  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
    ]

    selections_wgg_el = [ 
        {'selection' : 'elfullhighmt' , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 50, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        {'selection' : 'elfulllowmt'  , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 50, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        {'selection' : 'ellooselowmt' , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 80, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        {'selection' : 'elzcrhighmt'  , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 40, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },

        #{'selection' : 'elfullhighmt' , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 30, 'ymax_pergev' : 2.5, 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'elfullhighmt' , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 30, 'ymax_pergev' : 5  , 'ymin_logy' : 0.5, 'ymax_logy' :30   },
        #{'selection' : 'elfulllowmt'  , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 30, 'ymax_pergev' : 3  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'elfulllowmt'  , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 30, 'ymax_pergev' : 5  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'ellooselowmt' , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 50, 'ymax_pergev' : 5  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'ellooselowmt' , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 50, 'ymax_pergev' : 7  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'elzcrhighmt'  , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 30, 'ymax_pergev' : 5  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'elzcrhighmt'  , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 20, 'ymax_pergev' : 7  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
    ]

    selections_zgg = [
        {'selection' : 'elZgg'        , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 60, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        {'selection' : 'muZgg'        , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 60, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },

        #{'selection' : 'elZgg'        , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg   , 'ymax' : 40, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :30   },
        #{'selection' : 'elZgg'        , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg  , 'ymax' : 50, 'ymax_pergev' : 13, 'ymin_logy' : 0.1, 'ymax_logy' :30   },
        #{'selection' : 'elZgg'        , 'var' : 'm_leplepphph', 'xlabel' : xlabel_meegg , 'ymax' : 50, 'ymax_pergev' : 4 , 'ymin_logy' : 0.1, 'ymax_logy' :10   },
        #{'selection' : 'elZgg'        , 'var' : 'm_elel'      , 'xlabel' : xlabel_mee   , 'ymax' : 50, 'ymax_pergev' : 12 , 'ymin_logy' : 0.1, 'ymax_logy' :30   },
        #{'selection' : 'muZgg'        , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg   , 'ymax' : 50, 'ymax_pergev' : 12 , 'ymin_logy' : 0.1, 'ymax_logy' :30  },
        #{'selection' : 'muZgg'        , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg  , 'ymax' : 60, 'ymax_pergev' : 12 , 'ymin_logy' : 0.1, 'ymax_logy' :30   },
        #{'selection' : 'muZgg'        , 'var' : 'm_leplepphph', 'xlabel' : xlabel_mmmgg , 'ymax' : 60, 'ymax_pergev' : 5 , 'ymin_logy' : 0.1, 'ymax_logy' :10   },
        #{'selection' : 'muZgg'        , 'var' : 'm_mumu'      , 'xlabel' : xlabel_mmm   , 'ymax' : 60, 'ymax_pergev' : 12 , 'ymin_logy' : 0.1, 'ymax_logy' :30   },
    ]

    conf_wgg_mu =  make_full_configs( selections_wgg_mu, options.outputDir, dumpStack )
    conf_wgg_el =  make_full_configs( selections_wgg_el, options.outputDir, dumpStack )
    conf_zgg    =  make_full_configs( selections_zgg   , options.outputDir, dumpStack )


    if options.zgg : 
        for conf in conf_zgg :
            MakeZggPlots( **conf )
    if options.electron :
        for conf in conf_wgg_el :
            MakeElectronPlots( **conf )
    if options.muon:
        for conf in conf_wgg_mu :
            MakeMuonPlots( **conf )


    #if options.zgg : 
    #    MakeZggPlots( options.outputDir, var='pt_leadph12', suffix='', ylabel=ylabel_perbin, xlabel=xlabel_ptg   , label_style='fancy', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='m_ph1_ph2'  , suffix='', ylabel=ylabel_perbin, xlabel=xlabel_mgg    , label_style='fancy', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='pt_ph1_ph2' , suffix='', ylabel=ylabel_perbin, xlabel=xlabel_ptgg, label_style='fancy', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='pt_leadph12', suffix='', name_suffix='_prelim', ylabel=ylabel_perbin, xlabel=xlabel_ptg   , label_style='fancyprelim', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='m_ph1_ph2'  , suffix='', name_suffix='_prelim', ylabel=ylabel_perbin, xlabel=xlabel_mgg    , label_style='fancyprelim', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='pt_ph1_ph2' , suffix='', name_suffix='_prelim', ylabel=ylabel_perbin, xlabel=xlabel_ptgg, label_style='fancyprelim', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='pt_leadph12', suffix='_perGeV', name_suffix='_perGeV', ylabel=ylabel_pergev, xlabel=xlabel_ptg   , label_style='fancy', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='m_ph1_ph2'  , suffix='_perGeV', name_suffix='_perGeV', ylabel=ylabel_pergev, xlabel=xlabel_mgg    , label_style='fancy', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='pt_ph1_ph2' , suffix='_perGeV', name_suffix='_perGeV', ylabel=ylabel_pergev, xlabel=xlabel_ptgg, label_style='fancy', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='pt_leadph12', suffix='_perGeV', name_suffix='_perGeV_prelim', ylabel=ylabel_pergev, xlabel=xlabel_ptg   , label_style='fancyprelim', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='m_ph1_ph2'  , suffix='_perGeV', name_suffix='_perGeV_prelim', ylabel=ylabel_pergev, xlabel=xlabel_mgg    , label_style='fancyprelim', dumpStack=dumpStack )
    #    MakeZggPlots( options.outputDir, var='pt_ph1_ph2' , suffix='_perGeV', name_suffix='_perGeV_prelim', ylabel=ylabel_pergev, xlabel=xlabel_ptgg, label_style='fancyprelim', dumpStack=dumpStack )
    #if options.electron :
    #    MakeElectronPlots(options.outputDir, var='pt_leadph12', suffix='', ylabel=ylabel_perbin, xlabel=xlabel_ptg   ,label_style='fancy', dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='m_ph1_ph2'  , suffix='', ylabel=ylabel_perbin, xlabel=xlabel_mgg    ,label_style='fancy', dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='pt_ph1_ph2' , suffix='', ylabel=ylabel_perbin, xlabel=xlabel_ptgg,label_style='fancy', dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='pt_leadph12', suffix='', name_suffix='_prelim', ylabel=ylabel_perbin, xlabel=xlabel_ptg   ,label_style='fancyprelim', dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='m_ph1_ph2'  , suffix='', name_suffix='_prelim', ylabel=ylabel_perbin, xlabel=xlabel_mgg    ,label_style='fancyprelim', dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='pt_ph1_ph2' , suffix='', name_suffix='_prelim', ylabel=ylabel_perbin, xlabel=xlabel_ptgg,label_style='fancyprelim', dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='pt_leadph12', suffix='_perGeV', name_suffix='_perGeV', ylabel = ylabel_pergev, xlabel=xlabel_ptg   , logy=0, dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='m_ph1_ph2'  , suffix='_perGeV', name_suffix='_perGeV', ylabel = ylabel_pergev, xlabel=xlabel_mgg    , logy=0, dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='pt_ph1_ph2' , suffix='_perGeV', name_suffix='_perGeV', ylabel = ylabel_pergev, xlabel=xlabel_ptgg, logy=0, dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='pt_leadph12', suffix='_perGeV', name_suffix='_perGeV_prelim', ylabel = ylabel_pergev, xlabel=xlabel_ptg   ,label_style='fancyprelim', logy=0, dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='m_ph1_ph2'  , suffix='_perGeV', name_suffix='_perGeV_prelim', ylabel = ylabel_pergev, xlabel=xlabel_mgg    ,label_style='fancyprelim', logy=0, dumpStack=dumpStack  )
    #    MakeElectronPlots(options.outputDir, var='pt_ph1_ph2' , suffix='_perGeV', name_suffix='_perGeV_prelim', ylabel = ylabel_pergev, xlabel=xlabel_ptgg,label_style='fancyprelim', logy=0, dumpStack=dumpStack  )
    #if options.muon :
    #    MakeMuonPlots(options.outputDir, var='pt_leadph12', suffix='', ylabel=ylabel_perbin, xlabel=xlabel_ptg   , label_style='fancy', dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='m_ph1_ph2'  , suffix='', ylabel=ylabel_perbin, xlabel=xlabel_mgg    , label_style='fancy', dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='pt_ph1_ph2' , suffix='', ylabel=ylabel_perbin, xlabel=xlabel_ptgg, label_style='fancy', dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='pt_leadph12', suffix='', name_suffix='_prelim', ylabel=ylabel_perbin, xlabel=xlabel_ptg   , label_style='fancyprelim', dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='m_ph1_ph2'  , suffix='', name_suffix='_prelim', ylabel=ylabel_perbin, xlabel=xlabel_mgg    , label_style='fancyprelim', dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='pt_ph1_ph2' , suffix='', name_suffix='_prelim', ylabel=ylabel_perbin, xlabel=xlabel_ptgg, label_style='fancyprelim', dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='pt_leadph12', suffix='_perGeV', name_suffix='_perGeV',ylabel =ylabel_pergev, xlabel=xlabel_ptg   ,logy=0, dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='m_ph1_ph2'  , suffix='_perGeV', name_suffix='_perGeV',ylabel =ylabel_pergev, xlabel=xlabel_mgg    ,logy=0, dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='pt_ph1_ph2' , suffix='_perGeV', name_suffix='_perGeV',ylabel =ylabel_pergev, xlabel=xlabel_ptgg,logy=0, dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='pt_leadph12', suffix='_perGeV', name_suffix='_perGeV_prelim', ylabel=ylabel_pergev, xlabel=xlabel_ptg   , label_style='fancyprelim',logy=0, dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='m_ph1_ph2'  , suffix='_perGeV', name_suffix='_perGeV_prelim', ylabel=ylabel_pergev, xlabel=xlabel_mgg    , label_style='fancyprelim',logy=0, dumpStack=dumpStack  )
    #    MakeMuonPlots(options.outputDir, var='pt_ph1_ph2' , suffix='_perGeV', name_suffix='_perGeV_prelim', ylabel=ylabel_pergev, xlabel=xlabel_ptgg, label_style='fancyprelim',logy=0, dumpStack=dumpStack  )
    #if options.combined :
    #    MakeCombinedPlots( options.outputDir, dumpStack=dumpStack )

    print '^.^ FINSHED ^.^'


#---------------------------------------
def make_full_configs( selections, outputDir, dumpStack ) :

    ylabel_perbin = 'Events / bin'
    ylabel_pergev = 'Events / 5 GeV'

    out_configs = []

    for sel in selections :

        moddic = dict( sel )
        ymax_pergev = moddic.pop( 'ymax_pergev', None )
        ymin_logy = moddic.pop( 'ymin_logy', None )
        ymax_logy = moddic.pop( 'ymax_logy', None )
        ymax        = moddic.pop( 'ymax'       , None )

        info_nom        = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : ''       , 'name_suffix' : ''              , 'ylabel' : ylabel_perbin, 'ymax' : ymax,'label_style' : 'fancy' }
        info_nom_prelim = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : ''       , 'name_suffix' : '_prelim'       , 'ylabel' : ylabel_perbin, 'ymax' : ymax,'label_style' : 'fancyprelim' }
        info_gev        = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : '_perGeV', 'name_suffix' : '_perGeV'       , 'ylabel' : ylabel_pergev, 'ymax' : ymax_pergev,'label_style' : 'fancy' }
        info_gev_prelim = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : '_perGeV', 'name_suffix' : '_perGeV_prelim', 'ylabel' : ylabel_pergev, 'ymax' : ymax_pergev,'label_style' : 'fancyprelim' }
        info_gev_logy        = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : '_perGeV', 'name_suffix' : '_perGeV_logy'       , 'ylabel' : ylabel_pergev, 'ymin' : ymin_logy, 'ymax' : ymax_logy,'label_style' : 'fancy', 'logy' : 1 }
        info_gev_prelim_logy = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : '_perGeV', 'name_suffix' : '_perGeV_logy_prelim', 'ylabel' : ylabel_pergev, 'ymin' : ymin_logy, 'ymax' : ymax_logy,'label_style' : 'fancyprelim', 'logy' : 1 }

        info_nom             .update( moddic )
        info_nom_prelim      .update( moddic )
        info_gev             .update( moddic )
        info_gev_prelim      .update( moddic )
        info_gev_logy        .update( moddic )
        info_gev_prelim_logy .update( moddic )


        out_configs.append( info_nom             )
        out_configs.append( info_nom_prelim      )
        out_configs.append( info_gev             )
        out_configs.append( info_gev_prelim      )
        out_configs.append( info_gev_logy        )
        out_configs.append( info_gev_prelim_logy )

    return out_configs


#---------------------------------------
def MakeMuonPlots( outputDir=None, selection='', var='pt_leadph12', suffix='', name_suffix='', ylabel='Events / bin', xlabel='', label_style='fancy', logy=0, ymin=0, ymax=60, dumpStack=True ) :

    save = ( outputDir is not None )

    samplesWgg.DrawHist( '%s_%s%s' %(var,selection, suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Muon Channel', 'extra_label_loc' : (0.66, 0.57) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045}, doratio=options.doRatio, logy=logy, ymin=ymin, ymax=ymax )

    if save :
        name = '%s_%s%s' %(var,selection, name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( '%s_%s_EB-EB%s' %(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = '%s_%s_EB-EB%s' %(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        raw_input('continue')

    samplesWgg.DrawHist( '%s_%s_EE-EB%s'%(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = '%s_%s_EE-EB%s'%(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( '%s_%s_EB-EE%s'%(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = '%s_%s_EB-EE%s'%(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

#---------------------------------------
def MakeElectronPlots( outputDir=None, selection='', var='pt_leadph12', suffix='', name_suffix='', ylabel='Events / bin', xlabel='', label_style='fancy', logy=0, ymin=0, ymax=50, dumpStack=True  ) :

    save = ( outputDir is not None )

    samplesWgg.DrawHist( '%s_%s%s'%(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.66, 0.50) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045, }, doratio=options.doRatio, logy=logy, ymin=ymin, ymax=ymax )

    if save :
        name = '%s_%s%s'%(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWgg.DrawHist( '%s_%s_EB-EB%s'%(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = '%s_%s_EB-EB%s'%(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( '%s_%s_EE-EB%s'%(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = '%s_%s_EE-EB%s'%(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( '%s_%s_EB-EE%s'%(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = '%s_%s_EB-EE%s'%(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    #samplesWgg.DrawHist( '%s_elfulllowmt%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.66, 0.50) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045}, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax-10 )

    #if save :
    #    name = '%s_elfulllowmt%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')


    #samplesWgg.DrawHist( '%s_elfulllowmt_EB-EB%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_elfulllowmt_EB-EB%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_elfulllowmt_EE-EB%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_elfulllowmt_EE-EB%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_elfulllowmt_EB-EE%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_elfulllowmt_EB-EE%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_ellooselowmt%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.66, 0.50) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045}, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax )

    #if save :
    #    name = '%s_ellooselowmt%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')


    #samplesWgg.DrawHist( '%s_ellooselowmt_EB-EB%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_ellooselowmt_EB-EB%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_ellooselowmt_EE-EB%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_ellooselowmt_EE-EB%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_ellooselowmt_EB-EE%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_ellooselowmt_EB-EE%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_elzcrhighmt%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.66, 0.50) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045}, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax )

    #if save :
    #    name = '%s_elzcrhighmt%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')


    #samplesWgg.DrawHist( '%s_elzcrhighmt_EB-EB%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_elzcrhighmt_EB-EB%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_elzcrhighmt_EE-EB%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_elzcrhighmt_EE-EB%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_elzcrhighmt_EB-EE%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_elzcrhighmt_EB-EE%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')


#---------------------------------------
def MakeZggPlots( outputDir=None, selection='', var='', suffix='', name_suffix='', ylabel='Events / bin',xlabel='', label_style='fancy', logy=0, ymin=0, ymax=50, dumpStack=True  ) :

    save = ( outputDir is not None )

    chlabel = 'Muon Channel'
    if selection.count('el') :
        chlabel = 'Electron Channel'

    samplesWgg.DrawHist( '%s_%s%s' %(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : chlabel, 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.1}, doratio=options.doRatio, logy=logy, ymin=ymin, ymax=ymax )

    if save :
        name = '%s_%s%s' %(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( '%s_%s_EB-EB%s' %(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{%s}{Barrel-Barrel}'%chlabel, 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = '%s_%s_EB-EB%s' %(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( '%s_%s_EE-EB%s'%(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{%s}{Endcap-Barrel}'%chlabel, 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = '%s_%s_EE-EB%s'%(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( '%s_%s_EB-EE%s'%(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{%s}{Barrel-Endcap}'%chlabel, 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = '%s_%s_EB-EE%s'%(var,selection,name_suffix)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    #samplesWgg.DrawHist( '%s_elZgg%s' %(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.61, 0.58) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07}, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax )

    #if save :
    #    name = '%s_elZgg%s' %(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_elZgg_EB-EB%s' %(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_elZgg_EB-EB%s' %(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_elZgg_EE-EB%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_elZgg_EE-EB%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

    #samplesWgg.DrawHist( '%s_elZgg_EB-EE%s'%(var,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    #if save :
    #    name = '%s_elZgg_EB-EE%s'%(var,name_suffix)
    #    samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    #    if dumpStack : 
    #        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    #else :
    #    samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
    #    raw_input('continue')

#---------------------------------------
def MakeCombinedPlots( outputDir, var='pt_leadph12', dumpStack=True  ) :

    save = ( outputDir is not None )

    samplesWggComb.DrawHist( '%s_lgg'%(var), xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelim', 'extra_label' : 'Combined', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = '%s_lgg'%(var)
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWggComb.DrawHist( '%s_lgg_EB-EB'%(var), xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelim', 'extra_label' : '#splitline{Combined}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = '%s_lgg_EB-EB'%(var)
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWggComb.DrawHist( '%s_lgg_EE-EB'%(var), xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelim', 'extra_label' : '#splitline{Combined}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = '%s_lgg_EE-EB'%(var)
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWggComb.DrawHist( '%s_lgg_EB-EE'%(var), xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelim', 'extra_label' : '#splitline{Combined}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = '%s_lgg_EB-EE'%(var)
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWggBkgSub.DrawHist( '%s_lgg'%(var), subtract_bkg=True, xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Background Subtracted Events / bin', label_config={'labelStyle' : 'fancyprelim'}, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=False, ymin=-50, ymax=200 )

    if save :
        name = '%s_lgg_bkgSub'%(var)
        samplesWggBkgSub.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    else :
        raw_input('continue')



main()
