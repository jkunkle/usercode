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
p.add_argument('--aqgc',     default=False,  action='store_true' ,        dest='aqgc',         help='make combined aqgc plots')
p.add_argument('--money',     default=False,  action='store_true' ,        dest='money',         help='make money plots')
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

    samplesWgg       = SampleManager(options.baseDir, filename='hist.root', readHists=True)
    samplesWggComb   = SampleManager(options.baseDirComb, filename='hist.root', readHists=True)
    #samplesWggBkgSub = SampleManager(options.baseDirComb, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)

    samplesWgg        .ReadSamples( sampleConfWgg )
    samplesWggComb    .ReadSamples( sampleConfWgg )
    #samplesWggBkgSub  .ReadSamples( sampleConfWggBkgSub )

    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)

    dumpStack=True
    samplesWgg.activate_sample( 'AllBkg')
    samplesWgg.activate_sample( 'ZggNoSyst')
    samplesWgg.activate_sample( 'OtherDiPhotonNoSyst')
    samplesWgg.activate_sample( 'AllBkgPlusSig')
    samplesWgg.activate_sample('DiTopDiPhoton')
    samplesWgg.activate_sample('SingleTopDiPhoton')
    samplesWgg.activate_sample('TriBosonDiPhoton')
    samplesWgg.activate_sample('TTVDiPhoton')
    samplesWgg.activate_sample('WWDiPhoton')
    samplesWgg.activate_sample('WZlvjjDiPhoton')
    samplesWgg.activate_sample('WZlvllDiPhoton')
    samplesWgg.activate_sample('WZjjllDiPhoton')
    samplesWgg.activate_sample('WZlvvvDiPhoton')
    samplesWgg.activate_sample('ZZDiPhoton')

    if options.zgg and not options.money : 
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

    dumpStack=False
    samplesWgg.deactivate_sample( 'AllBkg' )
    samplesWgg.deactivate_sample( 'ZggNoSyst')
    samplesWgg.deactivate_sample( 'OtherDiPhotonNoSyst')
    samplesWgg.deactivate_sample( 'AllBkgPlusSig')
    samplesWgg.deactivate_sample('DiTopDiPhoton')
    samplesWgg.deactivate_sample('SingleTopDiPhoton')
    samplesWgg.deactivate_sample('TriBosonDiPhoton')
    samplesWgg.deactivate_sample('TTVDiPhoton')
    samplesWgg.deactivate_sample('WWDiPhoton')
    samplesWgg.deactivate_sample('WZlvjjDiPhoton')
    samplesWgg.deactivate_sample('WZlvllDiPhoton')
    samplesWgg.deactivate_sample('WZjjllDiPhoton')
    samplesWgg.deactivate_sample('WZlvvvDiPhoton')
    samplesWgg.deactivate_sample('ZZDiPhoton')

    xlabel_ptg = 'p_{T}^{lead #gamma} [GeV]'
    xlabel_ptgg = 'p_{T}^{#gamma #gamma} [GeV]'
    xlabel_mgg = 'M_{#gamma #gamma} [GeV]'
    xlabel_mee = 'M_{ee} [GeV]'
    xlabel_mmm = 'M_{#mu#mu} [GeV]'
    xlabel_meegg = 'M_{ee#gamma#gamma} [GeV]'
    xlabel_mmmgg = 'M_{#mu#mu#gamma#gamma} [GeV]'


    selections_wgg_mu = [ 
        #------------------------------------
        # Subl pT bins
        #------------------------------------
        #{'selection' : 'muhighmt'     , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 200, 'ymax_pergev' : 100 , 'ymin_logy' : 0.1, 'ymax_logy':200   },
        #{'selection' : 'mulowmt'      , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 140, 'ymax_pergev' : 80 , 'ymin_logy' : 0.1, 'ymax_logy' :200   },

        #------------------------------------
        # Nominal pT bins
        #------------------------------------
        {'selection' : 'muhighmt'     , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 80, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'mulowmt'      , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 40, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },

        #------------------------------------
        # From OneBin 
        #------------------------------------
        #{'selection' : 'muhighmt'     , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 60, 'ymax_pergev' : 5  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'muhighmt'     , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 45, 'ymax_pergev' : 7  , 'ymin_logy' : 0.5, 'ymax_logy' :30   },
        #{'selection' : 'mulowmt'      , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 40, 'ymax_pergev' : 4  , 'ymin_logy' : 0.01, 'ymax_logy' :20   },
        #{'selection' : 'mulowmt'      , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 45, 'ymax_pergev' : 7  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
    ]

    selections_wgg_el = [ 
        #------------------------------------
        # Subl pT bins
        #------------------------------------
        #{'selection' : 'elfullhighmt' , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 140, 'ymax_pergev' : 50 , 'ymin_logy' : 0.1, 'ymax_logy' :100   },
        #{'selection' : 'elfulllowmt'  , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 100, 'ymax_pergev' : 30 , 'ymin_logy' : 0.1, 'ymax_logy' :100   },
        #{'selection' : 'ellooselowmt' , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 240, 'ymax_pergev' : 100 , 'ymin_logy' : 0.1, 'ymax_logy' :200   },
        ##{'selection' : 'elzcrhighmt'  , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 80, 'ymax_pergev' : 30 , 'ymin_logy' : 0.1, 'ymax_logy' :100   },

        #------------------------------------
        # Nominal pT bins
        #------------------------------------
        {'selection' : 'elfullhighmt' , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 50, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'elfulllowmt'  , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 50, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'ellooselowmt' , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 80, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        ##{'selection' : 'elzcrhighmt'  , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 40, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },

        #------------------------------------
        # From OneBin 
        #------------------------------------
        #{'selection' : 'elfullhighmt' , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 30, 'ymax_pergev' : 2.5, 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'elfullhighmt' , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 30, 'ymax_pergev' : 5  , 'ymin_logy' : 0.5, 'ymax_logy' :30   },
        #{'selection' : 'elfulllowmt'  , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 30, 'ymax_pergev' : 3  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'elfulllowmt'  , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 30, 'ymax_pergev' : 5  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'ellooselowmt' , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 50, 'ymax_pergev' : 5  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'ellooselowmt' , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 50, 'ymax_pergev' : 7  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        ##{'selection' : 'elzcrhighmt'  , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg  , 'ymax' : 30, 'ymax_pergev' : 5  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        ##{'selection' : 'elzcrhighmt'  , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg , 'ymax' : 20, 'ymax_pergev' : 7  , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
    ]

    selections_zgg = [
        #{'selection' : 'elZgg'        , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 60, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },
        #{'selection' : 'muZgg'        , 'var' : 'pt_leadph12' , 'xlabel' : xlabel_ptg  , 'ymax' : 60, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :20   },

        {'selection' : 'elZgg'        , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg   , 'ymax' : 40, 'ymax_pergev' : 10 , 'ymin_logy' : 0.1, 'ymax_logy' :30   },
        {'selection' : 'elZgg'        , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg  , 'ymax' : 50, 'ymax_pergev' : 13, 'ymin_logy' : 0.1, 'ymax_logy' :30   },
        {'selection' : 'elZgg'        , 'var' : 'm_leplepphph', 'xlabel' : xlabel_meegg , 'ymax' : 50, 'ymax_pergev' : 5 , 'ymin_logy' : 0.1, 'ymax_logy' :10   },
        {'selection' : 'elZgg'        , 'var' : 'm_elel'      , 'xlabel' : xlabel_mee   , 'ymax' : 50, 'ymax_pergev' : 12 , 'ymin_logy' : 0.1, 'ymax_logy' :30   },
        {'selection' : 'muZgg'        , 'var' : 'm_ph1_ph2'   , 'xlabel' : xlabel_mgg   , 'ymax' : 50, 'ymax_pergev' : 12 , 'ymin_logy' : 0.1, 'ymax_logy' :30  },
        {'selection' : 'muZgg'        , 'var' : 'pt_ph1_ph2'  , 'xlabel' : xlabel_ptgg  , 'ymax' : 60, 'ymax_pergev' : 15 , 'ymin_logy' : 0.1, 'ymax_logy' :30   },
        {'selection' : 'muZgg'        , 'var' : 'm_leplepphph', 'xlabel' : xlabel_mmmgg , 'ymax' : 60, 'ymax_pergev' : 6 , 'ymin_logy' : 0.1, 'ymax_logy' :10   },
        {'selection' : 'muZgg'        , 'var' : 'm_mumu'      , 'xlabel' : xlabel_mmm   , 'ymax' : 60, 'ymax_pergev' : 12 , 'ymin_logy' : 0.1, 'ymax_logy' :30   },
    ]

    conf_wgg_mu =  make_full_configs( selections_wgg_mu, options.outputDir, dumpStack )
    conf_wgg_el =  make_full_configs( selections_wgg_el, options.outputDir, dumpStack )
    conf_zgg    =  make_full_configs( selections_zgg   , options.outputDir, dumpStack )


    if options.aqgc :
        MakeCombinedAQGCPlots( options.outputDir, dumpStack=dumpStack )
        #MakeCombinedAQGCPlots( options.outputDir, var='m_ph1_ph2', dumpStack=dumpStack )
    elif options.money :
        if options.zgg :
            MakeCombinedMoneyPlots( options.outputDir, var='pt_ph1_ph2', dumpStack=dumpStack, zgg=options.zgg, ymax=30)
            MakeCombinedMoneyPlots( options.outputDir, var='m_ph1_ph2', dumpStack=dumpStack, zgg=options.zgg, ymax=20)
            MakeCombinedMoneyPlots( options.outputDir, var='m_leplepphph', dumpStack=dumpStack, zgg=options.zgg, ymax=130)
            #MakeCombinedMoneyPlots( options.outputDir, var='m_elel', dumpStack=dumpStack, zgg=options.zgg, ymax=130)
            #MakeCombinedMoneyPlots( options.outputDir, var='m_mumu', dumpStack=dumpStack, zgg=options.zgg, ymax=130)
        else :
            MakeCombinedMoneyPlots( options.outputDir, var='pt_ph1_ph2', dumpStack=dumpStack, zgg=options.zgg, ymax=13)
            MakeCombinedMoneyPlots( options.outputDir, var='m_ph1_ph2', dumpStack=dumpStack, zgg=options.zgg, ymax=8)

    elif options.zgg : 
        for conf in conf_zgg :
            MakeZggPlots( **conf )
    else :
        if options.electron :
            for conf in conf_wgg_el :
                MakeElectronPlots( **conf )
        if options.muon:
            for conf in conf_wgg_mu :
                MakeMuonPlots( **conf )

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
        info_nom_prelim_nostat = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : ''       , 'name_suffix' : '_prelim_nostat'       , 'ylabel' : ylabel_perbin, 'ymax' : ymax,'label_style' : 'fancyprelimnostats' }
        info_gev        = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : '_perGeV', 'name_suffix' : '_perGeV'       , 'ylabel' : ylabel_pergev, 'ymax' : ymax_pergev,'label_style' : 'fancy' }
        info_gev_prelim = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : '_perGeV', 'name_suffix' : '_perGeV_prelim', 'ylabel' : ylabel_pergev, 'ymax' : ymax_pergev,'label_style' : 'fancyprelim' }
        info_gev_logy        = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : '_perGeV', 'name_suffix' : '_perGeV_logy'       , 'ylabel' : ylabel_pergev, 'ymin' : ymin_logy, 'ymax' : ymax_logy,'label_style' : 'fancy', 'logy' : 1 }
        info_gev_prelim_logy = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : '_perGeV', 'name_suffix' : '_perGeV_logy_prelim', 'ylabel' : ylabel_pergev, 'ymin' : ymin_logy, 'ymax' : ymax_logy,'label_style' : 'fancyprelim', 'logy' : 1 }
        info_gev_prelim_nostat = {'outputDir' : outputDir, 'dumpStack' : dumpStack, 'suffix' : '_perGeV', 'name_suffix' : '_perGeV_prelim_nostats', 'ylabel' : ylabel_pergev, 'ymax' : ymax_pergev,'label_style' : 'fancyprelimnostats' }

        info_nom               .update( moddic )
        info_nom_prelim        .update( moddic )
        info_gev               .update( moddic )
        info_gev_prelim        .update( moddic )
        info_gev_logy          .update( moddic )
        info_gev_prelim_logy   .update( moddic )
        info_gev_prelim_nostat .update( moddic )
        info_nom_prelim_nostat .update( moddic )


        out_configs.append( info_nom               )
        out_configs.append( info_nom_prelim        )
        out_configs.append( info_gev               )
        out_configs.append( info_gev_prelim        )
        out_configs.append( info_gev_logy          )
        out_configs.append( info_gev_prelim_logy   )
        out_configs.append( info_gev_prelim_nostat )
        out_configs.append( info_nom_prelim_nostat )

    return out_configs


#---------------------------------------
def MakeMuonPlots( outputDir=None, selection='', var='pt_leadph12', suffix='', name_suffix='', ylabel='Events / bin', xlabel='', label_style='fancy', logy=0, ymin=0, ymax=60, dumpStack=True ) :

    print var
    print suffix

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
    #samplesWgg.DrawHist( '%s_%s%s'%(var,selection,suffix), xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.16, 0.50) }, legend_config={'legendLoc' : 'Double','legendWiden' : 1.0, 'legendCompress' : 0.7, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045, }, doratio=options.doRatio, logy=logy, ymin=ymin, ymax=ymax )

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
def MakeCombinedAQGCPlots( outputDir, var='pt_leadph12', dumpStack=True  ) :

    samplesWggComb.deactivate_sample( 'AllBkg' )
    samplesWggComb.deactivate_sample( 'ZggNoSyst')
    samplesWggComb.deactivate_sample( 'OtherDiPhotonNoSyst')
    samplesWggComb.deactivate_sample( 'AllBkgPlusSig')
    #samplesWggComb.activate_sample( 'WAAQGCLT')
    samplesWggComb.activate_sample( 'AllBkgPlusQGC')


    save = ( outputDir is not None )

    samplesWggComb.DrawHist( '%s_lgg'%(var), xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelimnostats', 'extra_label' : 'Electron + Muon Channels', 'extra_label_loc' : (0.38, 0.6) }, legend_config={'legendLoc' : 'Double', 'legendWiden' : 1.1, 'legendCompress' : 1.2, 'legendTranslateX' : 0.22, 'legendTranslateY' : 0.06 }, doratio=options.doRatio, ymin = 0, ymax = 130 )
    #samplesWggComb.DrawHist( '%s_lgg'%(var), xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelimnostats', 'extra_label' : 'Electron + Muon Channels', 'extra_label_loc' : (0.38, 0.6) }, legend_config={'legendLoc' : 'Double', 'legendWiden' : 1.1, 'legendCompress' : 1.2, 'legendTranslateX' : 0.22, 'legendTranslateY' : 0.06 }, doratio=options.doRatio, ymin = 0, ymax = 60 )
    #samplesWggComb.DrawHist( '%s_lgg'%(var), xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelimnostats', 'extra_label' : 'Muon Channel', 'extra_label_loc' : (0.65, 0.57) }, legend_config={ 'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.035  }, doratio=options.doRatio, ymin = 0, ymax = 100 )

    if save :
        name = '%s_lgg'%(var)
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')



#---------------------------------------
def MakeCombinedMoneyPlots( outputDir, var='pt_ph1_ph2', dumpStack=True, zgg=False, ymax=10  ) :

    save = ( outputDir is not None )

    addtl_label = 'wgg'
    entry_width = 0.06
    if zgg :
        addtl_label = 'zgg'
        entry_width = 0.08

    samplesWgg.DrawHist( '%s_lgg_perGeV'%(var), xlabel='p_{T}^{#gamma #gamma} [GeV]',ylabel= 'Events / 5 GeV', label_config={'labelStyle' : 'fancypapernostats', 'extra_label' : '#splitline{combined muon and}{electron channels}', 'extra_label_loc' : (0.18, 0.8) }, legend_config={'legendWiden' : 1.1, 'entryWidth' : entry_width }, doratio=options.doRatio, ymin = 0, ymax = ymax )

    if save :
        name = '%s_lgg_%s'%(var, addtl_label)
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

main()
