"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

                                                                                       
p.add_argument('--xsFile',     default=None,  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')

p.add_argument('--save'        , default=False, action='store_true',   dest='save'        , help='save plots ( must provide outputDir )')
p.add_argument('--detailLevel' , default=100, type=int, dest='detailLevel'      , help='make only plots at this detail level (make all plots by default)')
p.add_argument('--makeAll'     , default=False, action='store_true',   dest='makeAll'     , help='make all plots')
p.add_argument('--makeEvent'   , default=False, action='store_true',   dest='makeEvent'   , help='make Wgg event plots')
p.add_argument('--makeMva'     , default=False, action='store_true',   dest='makeMva'     , help='make electron veto mva plots')
p.add_argument('--makeEleVeto' , default=False, action='store_true',   dest='makeEleVeto' , help='make electron veto comparison plots')
p.add_argument('--makeEleFake' , default=False, action='store_true',   dest='makeEleFake' , help='make electron fake factor plots')
p.add_argument('--makePhComp'  , default=False, action='store_true',   dest='makePhComp'  , help='make photon ID vars comparison plots')
p.add_argument('--makeJetFakeTemplate' , default=False, action='store_true',   dest='makeJetFakeTemplate' , help='make jet fake plots, template method')
p.add_argument('--makeJetFakeFactor' , default=False, action='store_true',   dest='makeJetFakeFactor' , help='make jet fake plots, fake factor method')

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
samplesWg = None
samplesEF = None

#analysis_bins_mgg = [0, 5, 10, 15, 20, 25, 30, 40, 50, 100, 200 ] 
#analysis_bins_egg = [0, 5, 10, 15, 20, 25, 30, 40, 50, 100, 200 ] 
analysis_bins_mgg = [0, 5, 10, 15, 25, 40, 80, 200 ] 
analysis_bins_egg = [0, 5, 10, 15, 25, 40, 80, 200 ] 

ph_cuts = ''
lead_dr_cut = 0.4
subl_dr_cut = 0.4
phot_dr_cut = 0.3

baseline_cuts_mgg = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2  && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_phDR>0.3 && leadPhot_leadLepDR>%.1f && sublPhot_leadLepDR>%.1f && el_n==0 && m_phph>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts)
baseline_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2  && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_phDR>0.3 && leadPhot_leadLepDR>%.1f && sublPhot_leadLepDR>%.1f && mu_n==0 && m_phph>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts)
zrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts)

invPixLead_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2  && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && ph_phDR>0.3 && leadPhot_leadLepDR>%.1f && sublPhot_leadLepDR>%.1f && mu_n==0 && m_phph>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixSubl_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2  && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && ph_phDR>0.3 && leadPhot_leadLepDR>%.1f && sublPhot_leadLepDR>%.1f && mu_n==0 && m_phph>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixLead_zrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixSubl_zrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixLead_invzrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0  && ( (fabs(m_lepphph-91.2) < 5) || (fabs(m_lepph1-91.2) < 5) || (fabs(m_lepph2-91.2) < 5) ) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixSubl_invzrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1  && ( (fabs(m_lepphph-91.2) < 5) || (fabs(m_lepph1-91.2) < 5)  || (fabs(m_lepph2-91.2) < 5) ) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts)

def main() :

    global samplesWgg
    global samplesWg
    global samplesEF

    baseDirWg  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/'
    baseDirWgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNom_2014_06_16/'
    baseDirEF  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/GammaGammaMediumNoEleVetoNoEleIDOlapWithTrig_2014_07_31/'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfWgg = 'Modules/Wgamgam.py'
    sampleConfWg  = 'Modules/Wgamgam.py'
    sampleConfEF  = 'Modules/Wgamgam.py'

    samplesWgg = SampleManager(baseDirWgg, treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    samplesWg  = SampleManager(baseDirWg , treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    samplesEF  = SampleManager(baseDirEF , treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)

    samplesWgg.ReadSamples( sampleConfWgg )
    samplesWg .ReadSamples( sampleConfWg )
    samplesEF .ReadSamples( sampleConfEF )

    if options.save :
        ROOT.gROOT.SetBatch(True)

    if options.makeAll or options.makeEvent :
        MakeWggEventPlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeMva:
        MakeWggMvaPlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeEleVeto:
        MakeWggEleVetoCompPlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeEleFake:
        MakeWggEleFakePlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makePhComp:
        MakePhotonCompPlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeJetFakeTemplate:
        MakePhotonJetFakePlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeJetFakeFactor:
        MakeJetFakeFactorPlots(save=options.save, detail=options.detailLevel) 

#---------------------------------------
# User functions
#---------------------------------------

#---------------------------------------
def MakeWggEventPlots( save=False, detail=100 ) :

    subdir='WggEventPlots'

    if save and options.outputDir is None :
        print 'Must provide an outputDir to save plots'
        save=False


    #ph_cuts = ' && ph_IsEB[0] && ph_IsEB[1]'

    samplesWgg.deactivate_sample( 'Data')
    print 'DISABLE DATA'

    samplesWgg.activate_sample( 'ISR')
    samplesWgg.activate_sample( 'FSR')
    samplesWgg.deactivate_sample( 'Wgg')

    samplesWgg.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && el_n==0 %s )' %ph_cuts, (25, 0, 5 ) , ymin=0.1, ymax=10000, logy=1, xlabel='#Delta R( l, lead #gamma)', ylabel='Events / 0.2', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87), legendConfig=samplesWgg.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double' ) )

    if save :
        name = 'leadPhot_leadLepDR__mgg__noLepPhDRCuts__splitWggISRFSR'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('sublPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && el_n==0  %s )' %ph_cuts, (25, 0, 5 ) , ymin=0.1, ymax=10000, logy=1, xlabel='#Delta R( l, sublead #gamma)', ylabel='Events / 0.2', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87), legendConfig=samplesWgg.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double'  ) )

    if save :
        name = 'sublPhot_leadLepDR__mgg__noLepPhDRCuts__splitWggISRFSR'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('sublPhot_leadLepDR', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && mu_n==0  %s )' %ph_cuts, (25, 0, 5 ) , ymin=0.1, ymax=50000, logy=1, xlabel='#Delta R( l, sublead #gamma)', ylabel='Events / 0.2', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.7, 0.87), legendConfig=samplesWgg.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double'  )  )

    if save :
        name = 'sublPhot_leadLepDR__egg__noLepPhDRCuts__splitWggISRFSR'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('leadPhot_leadLepDR', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && mu_n==0  %s )' %ph_cuts, (25, 0, 5 ) , ymin=0.1, ymax=80000, logy=1, xlabel='#Delta R( l, lead #gamma)', ylabel='Events / 0.2', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.7, 0.87), legendConfig=samplesWgg.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double'  )  )

    if save :
        name = 'leadPhot_leadLepDR__egg__noLepPhDRCuts__splitWggISRFSR'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')


    samplesWgg.deactivate_sample( 'ISR')
    samplesWgg.deactivate_sample( 'FSR')
    samplesWgg.activate_sample( 'Wgg')

    samplesWgg.Draw('m_lepphph', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts), (60, 0, 300 ) , logy=0,  xlabel='M_{l,#gamma,#gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.3, ) )

    if save :
        name = 'm_lepphph__egg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('m_lepphph', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %(lead_dr_cut, subl_dr_cut,ph_cuts), (60, 0, 300 ) , logy=0,  xlabel='M_{l,#gamma,#gamma} [GeV]', labelStyle='fancy', extra_label='Muon Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.3, ) )


    if save :
        name = 'm_lepphph__mgg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('m_lepph1', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts), (40, 0, 200 ) , logy=0,  xlabel='M_{l, lead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.3, legendTranslateX=0.05 , ) )

    if save :
        name = 'm_lepph1__egg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('m_lepph1', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts), (40, 0, 200 ) , logy=0,  xlabel='M_{l, lead #gamma} [GeV]', labelStyle='fancy', extra_label='Muon Channel',   extra_label_loc=(0.3, 0.86) , ymin=0, ymax=55, legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.3, ) )


    if save :
        name = 'm_lepph1__mgg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('m_lepph2', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %( lead_dr_cut, subl_dr_cut,ph_cuts), (40, 0, 200 ) , logy=0,  xlabel='M_{l, sublead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.3, ) )

    if save :
        name = 'm_lepph2__egg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('m_lepph2', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %( lead_dr_cut, subl_dr_cut, ph_cuts), (40, 0, 200 ) , logy=0,  xlabel='M_{l, sublead #gamma} [GeV]', labelStyle='fancy', extra_label='Muon Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.3, ) )


    if save :
        name = 'm_lepph2__mgg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('m_phph', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts), (50, 0, 200 ) , logy=1,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2,  legendWiden=1.2, ) )

    if save :
        name = 'm_phph__egg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWgg.Draw('m_phph', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %( lead_dr_cut, subl_dr_cut, ph_cuts), (50, 0, 200 ) , logy=1,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Muon Channel',  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2,  legendWiden=1.2 , ) )

    if save :
        name = 'm_phph__mgg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')


    samplesWgg.Draw('m_lepph1', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5)  %s)' %( lead_dr_cut, subl_dr_cut, ph_cuts), (40, 0, 200 ) , logy=0,  xlabel='M_{l, lead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.3, ) )
    if save :
        name = 'm_lepph1__egg__Cut_m_lepphph_10gevWindow'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')


    samplesWgg.Draw('m_lepph2', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5)  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts), (40, 0, 200 ) , logy=0,  xlabel='M_{l, sublead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.3, ) )

    if save :
        name = 'm_lepph2__egg__Cut_m_lepphph_10gevWindow'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    samplesWgg.Draw('m_lepph2', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts), (40, 0, 200 ) , logy=0,  xlabel='M_{l, sublead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.4, ) )
    if save :
        name = 'm_lepph2__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')


    samplesWgg.Draw('m_lepph2', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5)  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts), (40, 0, 200 ) , logy=0,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samplesWgg.config_legend(legendWiden=1.3,legendCompress=1.4, ) )

    if save :
        name = 'm_lepph2__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow__Cut_m_lepph2_10gevWindow'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    samplesWgg.Draw('m_phph', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5)  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts), (50, 0, 200 ) , logy=1,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    if save :
        name = 'm_phph__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow__Cut_m_lepph2_10gevWindow'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')


    samplesWgg.Draw('m_phph', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) && m_phph>15  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts), (50, 0, 200 ) , logy=1,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    if save :
        name = 'm_phph__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow__Cut_m_lepph2_10gevWindow__Cut_m_phph_15'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    samplesWgg.MakeRocCurve( ['m_phph', 'm_phph'], ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && (fabs(m_lepphph-91.2) > 5) && (fabs(m_lepph1-91.2) > 5)  && (fabs(m_lepph2-91.2) > 5) %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts) ]*2, ['Wgg', 'Wgg'], ['AllBkg', 'Zgamma'], [(50, 0, 200 )]*2, doSoverB=1, less_than=[0,0], colors=[ROOT.kRed, ROOT.kBlue], legend_entries=['B = All MC backgrounds', 'B = Zjets + Z#gamma'], ymin=0.5, ymax=4.5, legendConfig=samplesWgg.config_legend( legendWiden=1.3, legendCompress=1.4, legendTranslateX=-0.4 ) )

    if save :
        name = 'm_phph__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow__Cut_m_lepph2_10gevWindow__RocCurve'
        samplesWgg.DumpRoc(name, inDirs=subdir)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpRoc()
        raw_input('continue')

    samplesWgg.MakeRocCurve( ['m_phph', 'm_phph'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %(lead_dr_cut, subl_dr_cut, ph_cuts)]*2, ['Wgg', 'Wgg'], ['AllBkg', 'ZjetsZgamma'], [(50, 0, 200 )]*2, doSoverB=1, debug=1, less_than=[0,0], colors=[ROOT.kRed, ROOT.kBlue], legend_entries=['B = All MC backgrounds', 'B = Zjets + Z#gamma'] )

    if save :
        name = 'm_phph__mgg__baselineCuts__RocCurve'
        samplesWgg.DumpRoc(name, inDirs=subdir)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpRoc()
        raw_input('continue')



    # --------------------------------------
    # muon channel , photon pT
    # --------------------------------------
    samplesWgg.Draw('ph_pt[0]', 'PUWeight * ( %s ) ' %baseline_cuts_mgg, (40, 0, 200 ) , logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Muon Channel',  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2,  legendWiden=1.2 , ) )

    if save :
        name = 'ph_pt_lead__mgg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    samplesWgg.Draw('ph_pt[0]', 'PUWeight * ( %s ) ' %baseline_cuts_mgg, (analysis_bins_mgg[-1]/5, 0, analysis_bins_mgg[-1], analysis_bins_mgg ) , logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Muon Channel',  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2,  legendWiden=1.2 , ) )

    if save :
        name = 'ph_pt_lead__mgg__baselineCuts__varBins'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')


    samplesWgg.Draw('ph_pt[1]', 'PUWeight * ( %s ) ' %baseline_cuts_mgg, (40, 0, 200 ) , logy=1,  xlabel='sublead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Muon Channel',  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2,  legendWiden=1.2 , ) )

    if save :
        name = 'ph_pt_subl__mgg__baselineCuts'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    samplesWgg.Draw('ph_pt[1]', 'PUWeight * ( %s ) ' %baseline_cuts_mgg, (analysis_bins_mgg[-1]/5, 0, analysis_bins_mgg[-1], analysis_bins_mgg )   , logy=1,  xlabel='sublead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Muon Channel',  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2, legendWiden=1.2 , ) )

    if save :
        name = 'ph_pt_subl__mgg__baselineCuts__varBins'
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    #----------------------------------------
    # Make eta-pt dependent results
    #----------------------------------------

    eta_cuts = [['EB', 'EB'],['EB', 'EE'],['EE', 'EB'],['EE', 'EE']]
    eta_labels = ['Barrel photons', 'Lead photon in Barrel, sublead in Endcap','Lead photon in Endcap, sublead in Barrel', 'Endcap photons']

    analysis_bins_mgg_mod = list( analysis_bins_mgg )
    analysis_bins_mgg_mod[-1] = 1000000

    for ec, lab in zip(eta_cuts, eta_labels) :

        for idx, min in enumerate(analysis_bins_mgg_mod[:-1]) :
            if min < 15 : 
                continue
            max = analysis_bins_mgg_mod[idx+1]


            samplesWgg.Draw('ph_pt[0]', 'PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] && ph_pt[0] > %d && ph_pt[0] < %d )' %(baseline_cuts_mgg, ec[0], ec[1], min, max), (analysis_bins_mgg[-1]/5, 0, analysis_bins_mgg[-1] )   , logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='#splitline{Muon Channel}{%s}' %lab,  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2, legendWiden=1.2 , ) )

            if save :
                if idx+2 == len(analysis_bins_mgg_mod) :
                    name = 'ph_pt_lead__mgg__%s-%s__baselineCuts__ptbins_%d-max' %(ec[0], ec[1], min)
                else :
                    name = 'ph_pt_lead__mgg__%s-%s__baselineCuts__ptbins_%d-%d' %(ec[0], ec[1],min, max)
                samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
            else :
                samplesWgg.DumpStack( )
                raw_input('continue')

            samplesWgg.Draw('ph_pt[1]', 'PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] && ph_pt[0] > %d && ph_pt[0] < %d )' %(baseline_cuts_mgg, ec[0], ec[1], min, max), (analysis_bins_mgg[-1]/5, 0, analysis_bins_mgg[-1] )   , logy=1,  xlabel='sublead photon p_{T} [GeV]', labelStyle='fancy', extra_label='#splitline{Muon Channel}{%s}' %lab,  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2, legendWiden=1.2 , ) )

            if save :
                if idx+2 == len(analysis_bins_mgg_mod) :
                    name = 'ph_pt_subl__mgg__%s-%s__baselineCuts__ptbins_%d-max' %(ec[0], ec[1], min)
                else :
                    name = 'ph_pt_subl__mgg__%s-%s__baselineCuts__ptbins_%d-%d' %(ec[0], ec[1],min, max)
                samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
            else :
                samplesWgg.DumpStack( )
                raw_input('continue')

    #----------------------------------------
    # Make eta dependent results also 
    #----------------------------------------

    for ec, lab in zip(eta_cuts, eta_labels) :

        samplesWgg.Draw('ph_pt[0]', 'PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] )' %(baseline_cuts_mgg, ec[0], ec[1]), (analysis_bins_mgg[-1]/5, 0, analysis_bins_mgg[-1] )   , logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='#splitline{Muon Channel}{%s}' %lab,  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2, legendWiden=1.2 , ) ) 

        if save :
            name = 'ph_pt_lead__mgg__%s-%s__baselineCuts'%(ec[0],ec[1])
            samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        else :
            samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
            raw_input('continue')

        samplesWgg.Draw('ph_pt[0]', 'PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] ) ' %(baseline_cuts_mgg, ec[0], ec[1]), (analysis_bins_mgg[-1]/5, 0, analysis_bins_mgg[-1], analysis_bins_mgg ) , logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Muon Channel',  extra_label_loc=(0.3, 0.86), ymin=0.1, ymax=1000 , legendConfig=samplesWgg.config_legend(legendLoc=None,legendCompress=1.2,  legendWiden=1.2 , ) )

        if save :
            name = 'ph_pt_lead__mgg__%s-%s__baselineCuts__varBins'%(ec[0],ec[1])
            samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        else :
            samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
            raw_input('continue')

    # --------------------------------------
    # electron channel , photon pT
    # --------------------------------------

    samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s ) ' %zrej_cuts_egg, (analysis_bins_egg[-1]/5, 0, analysis_bins_egg[-1], analysis_bins_egg ) , logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    if save :
        name = 'ph_pt_lead__egg__allZRejCuts'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s ) ' %zrej_cuts_egg, (analysis_bins_egg[-1]/5, 0, analysis_bins_egg[-1], analysis_bins_egg ), logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    if save :
        name = 'ph_pt_lead__egg__allZRejCuts__varBins'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')


    samplesWgg.Draw('ph_pt[1]', ' PUWeight * ( %s ) ' %zrej_cuts_egg ,(analysis_bins_egg[-1]/5, 0, analysis_bins_egg[-1], analysis_bins_egg ),  logy=1,  xlabel='sublead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    if save :
        name = 'ph_pt_subl__egg__allZRejCuts'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    samplesWgg.Draw('ph_pt[1]', ' PUWeight * ( %s ) ' %zrej_cuts_egg, (analysis_bins_egg[-1]/5, 0, analysis_bins_egg[-1], analysis_bins_egg ) , logy=1,  xlabel='sublead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    if save :
        name = 'ph_pt_subl__egg__allZRejCuts__varBins'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    #-------------------------------------
    # make eta-pt dependent cuts
    #-------------------------------------

    cuts = [baseline_cuts_egg, zrej_cuts_egg ]
    labels = ['baselineCuts', 'allZrejCuts']

    for cut, label in zip( cuts, labels ) :

        eta_cuts = [['EB', 'EB'],['EB', 'EE'],['EE', 'EB'],['EE', 'EE']]
        eta_labels = ['Barrel photons', 'Lead photon in Barrel, sublead in Endcap','Lead photon in Endcap, sublead in Barrel', 'Endcap photons']

        analysis_bins_egg_mod = list( analysis_bins_egg )
        analysis_bins_egg_mod[-1] = 1000000

        for ec, lab in zip(eta_cuts, eta_labels) :

            for idx, min in enumerate(analysis_bins_egg_mod[:-1]) :
                if min < 15 : 
                    continue
                max = analysis_bins_egg_mod[idx+1]

                samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] && ph_pt[0]>%d && ph_pt[0]<%d )' %(cut, ec[0], ec[1], min, max), (40, 0, 200 ) , logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='#splitline{Electron Channel}{%s}'%lab, extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

                if save :
                    if idx+2 == len(analysis_bins_egg_mod) :
                        name = 'ph_pt_lead__egg__%s-%s__%s__ptbins_%d-max' %(ec[0], ec[1], label, min)
                    else :
                        name = 'ph_pt_lead__egg__%s-%s__%s__ptbins_%d-%d' %(ec[0], ec[1], label, min, max)
                    samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
                    samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
                else :
                    samplesWgg.DumpStack( )
                    raw_input('continue')

                samplesWgg.Draw('ph_pt[1]', ' PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] && ph_pt[0]>%d && ph_pt[0]<%d )' %(cut, ec[0], ec[1], min, max), (40, 0, 200 ) , logy=1,  xlabel='sublead photon p_{T} [GeV]', labelStyle='fancy', extra_label='#splitline{Electron Channel}{%s}'%lab, extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

                if save :
                    if idx+2 == len(analysis_bins_egg_mod) :
                        name = 'ph_pt_subl__egg__%s-%s__%s__ptbins_%d-max' %(ec[0], ec[1], label,min)
                    else :
                        name = 'ph_pt_subl__egg__%s-%s__%s__ptbins_%d-%d' %(ec[0], ec[1],label, min, max)
                    samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
                    samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
                else :
                    samplesWgg.DumpStack( )
                    raw_input('continue')

        #-------------------------------------
        # make eta dependent cuts also
        #-------------------------------------
        for ec, lab in zip(eta_cuts, eta_labels) :
            samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] )' %(cut, ec[0], ec[1]), (40, 0, 200 ) , logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='#splitline{Electron Channel}{%s}'%lab, extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

            if save :
                name = 'ph_pt_lead__egg__%s-%s__%s'%(ec[0], ec[1], label)
                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
                samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesWgg.DumpStack()
                raw_input('continue')

            samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] ) ' %(cut, ec[0], ec[1]), (analysis_bins_egg[-1]/5, 0, analysis_bins_egg[-1], analysis_bins_egg ) , logy=1,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
            if save :
                name = 'ph_pt_lead__egg__%s-%s__%s__varBins'%(ec[0], ec[1], label)
                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
                samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesWgg.DumpStack()
                raw_input('continue')

    
#---------------------------------------
def MakeWggEleFakePlots( save=False, detail=100 ) :

    global samplesWg

    subdir = 'EleFakePlots'

    samplesWg.activate_sample( 'Data')

    # ---------------------------------
    # Draw FF derivation control regions
    # ---------------------------------
    draw_base_nom = 'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==0 '
    draw_base_inv = 'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==1 '

    pt_bins = analysis_bins_egg[3:-2]
    eta_bins = [0.0, 0.1, 0.5, 1.0, 1.48, 1.57, 2.1, 2.2, 2.3, 2.4, 2.5]
    pt_bins_last = [analysis_bins_egg[-2], 1000000]
    eta_bins_last = [0.0, 0.1, 0.5, 1.0, 1.48, 1.57, 2.1, 2.4, 2.5]

    samplesWg.deactivate_sample('Data')
    samplesWg.activate_sample('Electron')
    pt_eta_bins = {}
    for ptidx, ptmin in enumerate(pt_bins[:-1] ) :
        ptmax = pt_bins[ptidx+1]
        pt_eta_bins[(ptmin,ptmax)] = eta_bins
    for ptidx, ptmin in enumerate(pt_bins_last[:-1] ) :
        ptmax = pt_bins_last[ptidx+1]
        pt_eta_bins[(ptmin,ptmax)] = eta_bins_last

    for bin in  samplesWg.Draw3DProjections( 'm_lepph1:fabs(ph_eta[0]):ph_pt[0]', 'PUWeight * ( %s )' %( draw_base_nom ), ( 40, 0, 200, 250, 0, 2.5, 100, 0, 200 ), pt_eta_bins, logy=0, xlabel='M_{e, #gamma} [GeV]', legendConfig=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, )  ) :
        print 'Got bin ', bin
        raw_input('continue')
    
    last_pt_bin = max ([x[1] for x in pt_eta_bins.keys() ] )
    for (ptmin, ptmax), etabins in pt_eta_bins.iteritems() :
        for etaidx, etamin in enumerate(etabins[:-1] ) :
            etamax = eta_bins[etaidx+1]

            if ptmin < 15 :
                continue

            samplesWg.Draw( 'm_lepph1', 'PUWeight * ( %s && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f && ph_pt[0] > %d && ph_pt[0] < %d )' %( draw_base_nom, etamin, etamax, ptmin, ptmax ), ( 100, 0, 200), logy=1, xlabel='M_{e, #gamma} [GeV]', legendConfig=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, ), )

            if save :
                if ptmax == last_pt_bin :
                    name = 'm_lepph1__eg__passPixSeed__eta_%.2f-%.2f__pt_%d-max'%(etamin, etamax, ptmin)
                else :
                    name = 'm_lepph1__eg__passPixSeed__eta_%.2f-%.2f__pt_%d-%d'%(etamin, etamax, ptmin, ptmax)
                samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                samplesWg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesWg.DumpStack()
                raw_input('continue')

            samplesWg.Draw( 'm_lepph1', 'PUWeight * ( %s && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f && ph_pt[0] > %d && ph_pt[0] < %d )' %( draw_base_inv, etamin, etamax, ptmin, ptmax ), ( 100, 0, 200), logy=1, xlabel='M_{e, #gamma} [GeV]', legendConfig=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, ), )

            if save :
                if ptmax == last_pt_bin :
                    name = 'm_lepph1__eg__failPixSeed__eta_%.2f-%.2f__pt_%d-max'%(etamin, etamax, ptmin)
                else :
                    name = 'm_lepph1__eg__failPixSeed__eta_%.2f-%.2f__pt_%d-%d'%(etamin, etamax, ptmin, ptmax)
                samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                samplesWg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesWg.DumpStack()
                raw_input('continue')

    # ---------------------------------
    # Draw FF application control regions
    # ---------------------------------
    samplesWgg.Draw('m_lepphph', ' PUWeight * ( %s )' %(invPixLead_cuts_egg), (40, 0, 200 ) , xlabel='M_{l,#gamma,#gamma} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, lead photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepphph__egg__baselineCuts__invPixSeed_lead'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('m_lepphph', ' PUWeight * ( %s )' %(invPixSubl_cuts_egg), (40, 0, 200 ) ,  xlabel='M_{l,#gamma,#gamma} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, sublead photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepphph__egg__baselineCuts__invPixSeed_subl'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('m_lepph1', ' PUWeight * ( %s )' %(invPixLead_cuts_egg), (40, 0, 200 ) , xlabel='M_{l,lead #gamma} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, lead photon}', extra_label_loc=(0.3, 0.86),   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepph1__egg__baselineCuts__invPixSeed_lead'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('m_lepph1', ' PUWeight * ( %s )' %(invPixSubl_cuts_egg), (40, 0, 200 ) ,  xlabel='M_{l,lead #gamma} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, sublead photon}', extra_label_loc=(0.3, 0.86),   legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepph1__egg__baselineCuts__invPixSeed_subl'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')


    samplesWgg.Draw('m_lepph2', ' PUWeight * ( %s )' %(invPixLead_cuts_egg), (40, 0, 200 ) , xlabel='M_{l,sublead #gamma} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, lead photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepph2__egg__baselineCuts__invPixSeed_lead'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('m_lepph2', ' PUWeight * ( %s )' %(invPixSubl_cuts_egg), (40, 0, 200 ) , xlabel='M_{l,sublead #gamma} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, sublead photon}', extra_label_loc=(0.3, 0.86),  legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepph2__egg__baselineCuts__invPixSeed_subl'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s )' %(invPixLead_cuts_egg), (analysis_bins_egg[-1]/5, 0, analysis_bins_egg[-1], analysis_bins_egg ) ,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, lead photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'ph_pt_lead__egg__baselineCuts__invPixSeed_lead'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s )' %(invPixSubl_cuts_egg), (analysis_bins_egg[-1]/5, 0, analysis_bins_egg[-1], analysis_bins_egg ) ,  xlabel='sublead photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, sublead photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'ph_pt_subl__egg__baselineCuts__invPixSeed_subl'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    #---------------------------------------------
    # Dump data counts for each pt, eta bin and region
    # DSIABLED -- Do this in MakeBackgroundEstimate.py
    #---------------------------------------------
    #samplesWgg.deactivate_all_samples()
    #samplesWgg.activate_sample('Data')
    #pt_bins = [ 15, 25, 40, 80, 1000000 ]
    #eta_bins = [0.0, 0.1, 0.5, 1.0, 1.48, 1.57, 2.1, 2.2, 2.3, 2.4, 2.5]

    #for idx, ptmin in enumerate( pt_bins[:-1] ) :
    #    ptmax = pt_bins[idx+1]

    #    for idx, etamin in enumerate( eta_bins[:-1] ) :
    #        etamax = eta_bins[idx+1]

    #        if etamin >= 0 and etamin < 1.48 and etamax > 0 and etamax <= 1.48 :
    #            #lead in barrel subl in barrel
    #            samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f && ph_IsEB[0] && ph_IsEB[1] )' %(invPixLead_cuts_egg, ptmin, ptmax, etamin, etamax), (1, 0, 200 ) ,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, lead photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    #            if save :
    #                name = 'ph_pt_lead__egg__baselineCuts__invPixSeed_lead__EB-EB__pt_%d-%d__eta_%.2f-%.2f' %( ptmin, ptmax, etamin, etamax)
    #                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    #            else :
    #                samplesWgg.DumpStack()

    #            #lead in barrel subl in endcap
    #            samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f && ph_IsEB[0] && ph_IsEE[1] )' %(invPixLead_cuts_egg, ptmin, ptmax, etamin, etamax), (1, 0, 200 ) ,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, lead photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    #            if save :
    #                name = 'ph_pt_lead__egg__baselineCuts__invPixSeed_lead__EB-EE__pt_%d-%d__eta_%.2f-%.2f' %( ptmin, ptmax, etamin, etamax)
    #                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    #            else :
    #                samplesWgg.DumpStack()

    #            #subl in barrel, lead in barrel
    #            samplesWgg.Draw('ph_pt[1]', ' PUWeight * ( %s && ph_pt[1] > %d && ph_pt[1] < %d && fabs(ph_eta[1]) > %f && fabs(ph_eta[1]) < %f && ph_IsEB[1] && ph_IsEB[0] )' %(invPixSubl_cuts_egg, ptmin, ptmax, etamin, etamax), (1, 0, 200 ) ,  xlabel='subl photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, subl photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    #            if save :
    #                name = 'ph_pt_subl__egg__baselineCuts__invPixSeed_subl__EB-EB__pt_%d-%d__eta_%.2f-%.2f' %( ptmin, ptmax, etamin, etamax)
    #                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    #            else :
    #                samplesWgg.DumpStack()

    #            #subl in barrel, lead in endcap
    #            samplesWgg.Draw('ph_pt[1]', ' PUWeight * ( %s && ph_pt[1] > %d && ph_pt[1] < %d && fabs(ph_eta[1]) > %f && fabs(ph_eta[1]) < %f && ph_IsEB[1] && ph_IsEE[0] )' %(invPixSubl_cuts_egg, ptmin, ptmax, etamin, etamax), (1, 0, 200 ) ,  xlabel='subl photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, subl photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    #            if save :
    #                name = 'ph_pt_subl__egg__baselineCuts__invPixSeed_subl__EE-EB__pt_%d-%d__eta_%.2f-%.2f' %( ptmin, ptmax, etamin, etamax)
    #                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    #            else :
    #                samplesWgg.DumpStack()

    #        elif etamin >= 1.57 and etamin < 2.5 and etamax > 1.57 and etamax <= 2.5 :

    #            #lead in endcap subl in barrel
    #            samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f && ph_IsEE[0] && ph_IsEB[1] )' %(invPixLead_cuts_egg, ptmin, ptmax, etamin, etamax), (1, 0, 200 ) ,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, lead photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    #            if save :
    #                name = 'ph_pt_lead__egg__baselineCuts__invPixSeed_lead__EE-EB__pt_%d-%d__eta_%.2f-%.2f' %( ptmin, ptmax, etamin, etamax)
    #                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    #            else :
    #                samplesWgg.DumpStack()

    #            #lead in endcap subl in endcap
    #            samplesWgg.Draw('ph_pt[0]', ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f && ph_IsEE[0] && ph_IsEE[1] )' %(invPixLead_cuts_egg, ptmin, ptmax, etamin, etamax), (1, 0, 200 ) ,  xlabel='lead photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, lead photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    #            if save :
    #                name = 'ph_pt_lead__egg__baselineCuts__invPixSeed_lead__EE-EE__pt_%d-%d__eta_%.2f-%.2f' %( ptmin, ptmax, etamin, etamax)
    #                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    #            else :
    #                samplesWgg.DumpStack()

    #            #subl in endcap, lead in barrel
    #            samplesWgg.Draw('ph_pt[1]', ' PUWeight * ( %s && ph_pt[1] > %d && ph_pt[1] < %d && fabs(ph_eta[1]) > %f && fabs(ph_eta[1]) < %f && ph_IsEE[1] && ph_IsEB[0] )' %(invPixSubl_cuts_egg, ptmin, ptmax, etamin, etamax), (1, 0, 200 ) ,  xlabel='subl photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, subl photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    #            if save :
    #                name = 'ph_pt_subl__egg__baselineCuts__invPixSeed_subl__EB-EE__pt_%d-%d__eta_%.2f-%.2f' %( ptmin, ptmax, etamin, etamax)
    #                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    #            else :
    #                samplesWgg.DumpStack()

    #            #subl in endcap, lead in endcap
    #            samplesWgg.Draw('ph_pt[1]', ' PUWeight * ( %s && ph_pt[1] > %d && ph_pt[1] < %d && fabs(ph_eta[1]) > %f && fabs(ph_eta[1]) < %f && ph_IsEE[1] && ph_IsEE[0] )' %(invPixSubl_cuts_egg, ptmin, ptmax, etamin, etamax), (1, 0, 200 ) ,  xlabel='subl photon p_{T} [GeV]', labelStyle='fancy', extra_label='{Invert Pix Seed Veto, subl photon}', extra_label_loc=(0.3, 0.86), legendConfig=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    #            if save :
    #                name = 'ph_pt_subl__egg__baselineCuts__invPixSeed_subl__EE-EE__pt_%d-%d__eta_%.2f-%.2f' %( ptmin, ptmax, etamin, etamax)
    #                samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
    #            else :
    #                samplesWgg.DumpStack()

#---------------------------------------
def MakeWggMvaPlots( save=False, detail=100 ) :

    global samplesWgg

    subdir = 'WggMvaPlots'

    selection = 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && m_phph>15  )'
    binning = ( 40, -0.3, 0.5)

    samplesWgg.MakeRocCurve( ['zrej_mvascore']*2, [ selection ]*2, ['Wgg', 'Wgg'], ['AllBkg', 'ZjetsZgamma'], [binning]*2, doSoverB=1, debug=1, less_than=[0,0], colors=[ROOT.kRed, ROOT.kBlue], legend_entries=['B = All MC backgrounds', 'B = Zjets + Z#gamma'], ymin=0, ymax=6, legendConfig=samplesWgg.config_legend( legendWiden=1.4, legendCompress=1.4, legendTranslateX=-0.35 ) )

    if save :
        name = 'zrej_mvascore__egg__baselineCuts__RocCurve1EleVetoData'
        DumpRoc(name, inDirs=subdir)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpRoc()
        raw_input('continue')

    samplesWgg.Draw( 'zrej_mvascore', selection, binning, xlabel='BDT score', ylabel='Events / 0.2', legendConfig=samplesWgg.config_legend( legendWiden=1.1, legendCompress=1.2 ), labelStyle='fancy'  )

    if save :
        name = 'zrej_mvascore__egg__baselineCuts__1EleVetoData'
        DumpRoc(name, inDirs=subdir)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpRoc()
        raw_input('continue')


#---------------------------------------
def MakeWggMvaPlots( save=False, detail=100 ) :

    global samplesWgg

    subdir = 'WggMvaPlots'

    selection = 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && m_phph>15  )'
    binning = ( 40, -0.3, 0.5)

    samplesWgg.MakeRocCurve( ['zrej_mvascore']*2, [ selection ]*2, ['Wgg', 'Wgg'], ['AllBkg', 'ZjetsZgamma'], [binning]*2, doSoverB=1, debug=1, less_than=[0,0], colors=[ROOT.kRed, ROOT.kBlue], legend_entries=['B = All MC backgrounds', 'B = Zjets + Z#gamma'], ymin=0, ymax=6, legendConfig=samplesWgg.config_legend( legendWiden=1.4, legendCompress=1.4, legendTranslateX=-0.35 ) )

    if save :
        name = 'zrej_mvascore__egg__baselineCuts__RocCurve1EleVetoData'
        DumpRoc(name, inDirs=subdir)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpRoc()
        raw_input('continue')

    samplesWgg.Draw( 'zrej_mvascore', selection, binning, xlabel='BDT score', ylabel='Events / 0.2', legendConfig=samplesWgg.config_legend( legendWiden=1.1, legendCompress=1.2 ), labelStyle='fancy'  )

    if save :
        name = 'zrej_mvascore__egg__baselineCuts__1EleVetoData'
        DumpRoc(name, inDirs=subdir)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpRoc()
        raw_input('continue')

#---------------------------------------
def MakeWggEleVetoCompPlots( save=False, detail=100 ) :

    global samplesWgg

    subdir = 'WggEleVetoCompPlots'

    selection = ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && ph_phDR>0.3 && m_phph>15 ) '] +  ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ( (ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 ) || ( ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 ) ) && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && ph_phDR>0.3 && m_phph>15 )']*2
    #jselection = ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && ph_phDR>0.3 && m_phph>15 ) '] +  ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ( ( ph_passMedium[0] && ph_hasPixSeed[0]==1 ) || ( !ph_passMedium[0] ) ) && && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && ph_phDR>0.3 && m_phph>15 )']*2

    sample_names = ['ZjetsZgamma', 'ZjetsZgamma', 'Data']
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue]
    legend_entries = ['Z MC -- 2 eleVeto photons', 'Z MC -- 1 eleVeto photon', 'Data -- 1 eleVeto photon']

    samplesWgg.CompareSelections( 'm_phph', selection , sample_names , (20, 0, 200 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='M_{#gamma #gamma} [GeV]', ymin=0, ymax=0.3 )

    if save :
        name = 'm_phph__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.Draw('m_phph', selection[2], ( 20, 0, 200 ), xlabel='M_{#gamma #gamma} [GeV]' )

    if save :
        name = 'm_phph__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.CompareSelections( 'm_lepphph', selection , sample_names ,(40, 0, 400 ) ,  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='M_{l #gamma #gamma} [GeV]', ymin=0, ymax=0.3  )
    if save :
        name = 'm_lepphph__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.Draw( 'm_lepphph', selection[2],(40, 0, 400 ), xlabel='M_{l #gamma #gamma} [GeV]'  )

    if save :
        name = 'm_lepphph__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')


    samplesWgg.CompareSelections( 'm_lepph1', selection , sample_names , (20, 0, 200 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='M_{l lead #gamma} [GeV]', ymin=0, ymax=0.3   )

    if save :
        name = 'm_lepph1__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.Draw( 'm_lepph1', selection[2], (20, 0, 200 ), xlabel='M_{l lead #gamma} [GeV]')

    if save :
        name = 'm_lepph1__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.CompareSelections( 'm_lepph2', selection , sample_names , (20, 0, 200 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='M_{l sublead #gamma} [GeV]', ymin=0, ymax=0.3  )

    if save :
        name = 'm_lepph2__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.Draw( 'm_lepph2', selection[2], (20, 0, 200 ), xlabel='M_{l sublead #gamma} [GeV]' )

    if save :
        name = 'm_lepph2__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.CompareSelections( 'leadPhot_leadLepDR', selection , sample_names , (20, 0, 5 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='#Delta R( l, lead #gamma) ', ylabel='Normalized Events / 0.25', ymin=0, ymax=0.3   )

    if save :
        name = 'leadPhot_leadLepDR__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.Draw( 'leadPhot_leadLepDR', selection[2], (20, 0, 5 ), xlabel='#Delta R( l, lead #gamma) ', ylabel='Events / 0.25' )

    if save :
        name = 'leadPhot_leadLepDR__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.CompareSelections( 'sublPhot_leadLepDR', selection , sample_names , (20, 0, 5 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='#Delta R( l, sublead #gamma)', ylabel='Normalized Events / 0.25', ymin=0, ymax=0.3   )

    if save :
        name = 'sublPhot_leadLepDR__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.Draw( 'sublPhot_leadLepDR', selection[2], (20, 0, 5 ), xlabel='#Delta R( l, sublead #gamma)', ylabel='Events / 0.25' )

    if save :
        name = 'sublPhot_leadLepDR__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.CompareSelections( 'ph_phDR', selection , sample_names , (20, 0, 5 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='#Delta R( #gamma, #gamma)', ylabel='Normalized Events / 0.25', ymin=0, ymax=0.3  )

    if save :
        name = 'ph_phDr__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.Draw( 'ph_phDR', selection[2], (20, 0, 5 ), xlabel='#Delta R( #gamma, #gamma)', ylabel='Events / 0.25')

    if save :
        name = 'ph_phDr__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')


#---------------------------------------
def MakePhotonCompPlots( save=False, detail=100) :

    samplesWg.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2 , ['Wgamma','Inclusive W'], (100, 0, 0.1), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.00001, ymax = 0.5, logy=1, xlabel='#sigma i#eta i#eta', extra_label='Endcap photons', ylabel='Normalized Events / 0.001'  )
    SaveStack('ph_sigmaIEIE_EE_comp_wg_wjets', 'base')

    samplesWg.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2 , ['Wgamma','Inclusive W'], (100, 0, 0.03), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.00001, ymax = 0.8, logy=1, xlabel='#sigma i#eta i#eta', extra_label='Barrel photons', ylabel='Normalized Events / 0.0003'  ) 
    SaveStack('ph_sigmaIEIE_EB_comp_wg_wjets', 'base')

    samplesWg.CompareSelections('ph_chIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2 , ['Wgamma','Inclusive W'], (100, 0, 100), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected charged hadron isolation [GeV]', extra_label='Barrel photons', ylabel='Normalized Events / GeV'  )
    SaveStack('ph_chIsoCorr_EB_comp_wg_wjets', 'base')

    samplesWg.CompareSelections('ph_chIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2 , ['Wgamma','Inclusive W'], (100, 0, 100), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected charged hadron isolation [GeV]', extra_label='Endcap photons', ylabel='Normalized Events / GeV'  )
    SaveStack('ph_chIsoCorr_EE_comp_wg_wjets', 'base')

    samplesWg.CompareSelections('ph_neuIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2 , ['Wgamma', 'Inclusive W'], (80, -20, 20), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected neutral hadron isolation [GeV]', extra_label='Endcap photons', ylabel='Normalized Events / 0.5 GeV'  )
    SaveStack('ph_neuIsoCorr_EE_comp_wg_wjets', 'base')

    samplesWg.CompareSelections('ph_neuIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2 , ['Wgamma', 'Inclusive W'], (80, -20, 20), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected neutral hadron isolation [GeV]', extra_label='Barrel photons', ylabel='Normalized Events / 0.5 GeV'  )
    SaveStack('ph_neuIsoCorr_EB_comp_wg_wjets', 'base')

    samplesWg.CompareSelections('ph_phoIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2 , ['Wgamma', 'Inclusive W'], (100, -5, 45), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected photon isolation [GeV]', extra_label='Endcap photons', ylabel='Normalized Events / 0.5 GeV'  )
    SaveStack('ph_phoIsoCorr_EE_comp_wg_wjets', 'base')

    samplesWg.CompareSelections('ph_phoIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2 , ['Wgamma', 'Inclusive W'], (100, -5, 45), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected photon isolation [GeV]', extra_label='Barrel photons', ylabel='Normalized Events / 0.5 GeV'  )
    SaveStack('ph_phoIsoCorr_EB_comp_wg_wjets', 'base')

    samplesWg.MakeRocCurve(['ph_sigmaIEIE[0]', 'ph_passSIEIEMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, 0, 0.1), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['#sigma i#eta i#eta ROC curve', 'Medium working point'], extra_label='Endcap Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_sigmaIEIE_EE_roc_comp_medium', 'base')
    samplesWg.MakeRocCurve(['ph_sigmaIEIE[0]', 'ph_passSIEIEMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, 0, 0.03), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['#sigma i#eta i#eta ROC curve', 'Medium working point'], extra_label='Barrel Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_sigmaIEIE_EB_roc_comp_medium', 'base')

    samplesWg.MakeRocCurve(['ph_chIsoCorr[0]', 'ph_passChIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, 0, 100), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr ch iso ROC curve', 'Medium working point'], extra_label='Endcap Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_chIsoCorr_EE_roc_comp_medium', 'base')
    samplesWg.MakeRocCurve(['ph_chIsoCorr[0]', 'ph_passChIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, 0, 100), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr ch iso ROC curve', 'Medium working point'], extra_label='Barrel Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_chIsoCorr_EB_roc_comp_medium', 'base')

    samplesWg.MakeRocCurve(['ph_neuIsoCorr[0]', 'ph_passNeuIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, -20, 20), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr neu iso ROC curve', 'Medium working point'], extra_label='Endcap Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_neuIsoCorr_EE_roc_comp_medium', 'base')
    samplesWg.MakeRocCurve(['ph_neuIsoCorr[0]', 'ph_passNeuIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, -20, 20), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr neu iso ROC curve', 'Medium working point'], extra_label='Barrel Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_neuIsoCorr_EB_roc_comp_medium', 'base')

    samplesWg.MakeRocCurve(['ph_phoIsoCorr[0]', 'ph_passPhoIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, -5, 45), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr pho iso ROC curve', 'Medium working point'], extra_label='Endcap Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_phoIsoCorr_EE_roc_comp_medium', 'base')
    samplesWg.MakeRocCurve(['ph_phoIsoCorr[0]', 'ph_passPhoIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, -5, 45), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr pho iso ROC curve', 'Medium working point'], extra_label='Barrel Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_phoIsoCorr_EB_roc_comp_medium', 'base')

def MakePhotonJetFakePlots(save=False, detail=100 ) :

    subdir = 'JetFakeTemplatePlots'

    photon_cuts = 'ph_hasPixSeed[0]==0 && ph_HoverE12[0]<0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    fsr_cut = 'leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR < 1.0 '
    fsr_lab = 'Cut_leadPhot_sublLepDR_04_10'

    bins_eb = (10, 0, 0.03)
    bins_ee = (10, 0, 0.1)

    ##------------------------------
    ##------------------------------
    ## signal template -- motivate event cuts
    ##------------------------------
    ##------------------------------
    #samplesWg.Draw('leadPhot_sublLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s ) ' %photon_cuts, (50, 0, 5), xlabel='#Delta R(sublead #mu, #gamma)', ylabel='Events / 0.1', labelStyle='fancy', legendConfig=samplesWg.config_legend( legendWiden=1.3, legendCompress=1.3) )

    #if save :
    #    name = 'leadPhot_sublLepDR__mmg'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s )' %photon_cuts, (50, 0, 5), xlabel='#Delta R(lead #mu, #gamma)', ylabel='Events / 0.1', )

    #if save :
    #    name = 'leadPhot_leadLepDR__mmg'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ##------------------------------
    ## Make a cut to remove FSR photons
    ##------------------------------


    #samplesWg.Draw('m_leplepph', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s  && %s) ' %(photon_cuts, fsr_cut), (100, 0, 500), xlabel='M_{#mu#mu#gamma} [GeV]', logy=1, ymin=1, ymax=1000000)

    #if save :
    #    name = 'm_leplepph__mmg__%s'%fsr_lab
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #samplesWg.Draw('m_leplepph+m_leplep', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s  && %s ) ' %(photon_cuts, fsr_cut), (100, 0, 500), xlabel='M_{#mu#mu}+M_{#mu#mu#gamma} [GeV]', logy=1, ymin=1, ymax=1000000  )

    #if save :
    #    name = 'm_leplepph+m_leplep__mmg__%s'%fsr_lab
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #samplesWg.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && ( m_leplepph+m_leplep ) < 185  ) ' %(photon_cuts, fsr_cut), (50, 0, 5), xlabel='#Delta R(lead #mu, #gamma)', ylabel='Events / 0.1' )

    #if save :
    #    name = 'leadPhot_leadLepDR__mmg__Cut_m_leplepph+m_leplep_185__%s'%fsr_lab
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && fabs( m_leplepph-91.2 ) < 5  ) ' %(photon_cuts, fsr_cut), (50, 0, 5), xlabel='#Delta R(lead #mu, #gamma)', ylabel='Events / 0.1' )

    #if save :
    #    name = 'leadPhot_leadLepDR__mmg__Cut_m_leplepph_10gevWindow__%s'%fsr_lab
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    ##-------------------------
    ## Add the leading fsr cut as well
    ##-------------------------

    #fsr_cut += ' && leadPhot_leadLepDR > 0.4'
    #fsr_lab += '__Cut_leadPhot_leadLepDR_04'

    #samplesWg.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && fabs( m_leplepph-91.2 ) < 5 && ph_IsEB[0] )' %(photon_cuts, fsr_cut), ( 60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', logy=1 )

    #if save :
    #    name = 'ph_sigmaIEIE__mmg__EB__Cut_m_leplepph_10gevWindow__Cut_%s' %fsr_lab
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #samplesWg.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && fabs( m_leplepph-91.2 ) < 5 && ph_IsEE[0] )' %(photon_cuts, fsr_cut), ( 50, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.002', logy=1  )

    #if save :
    #    name = 'ph_sigmaIEIE__mmg__EE__Cut_m_leplepph_10gevWindow__Cut_%s' %fsr_lab
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && ( m_leplepph+m_leplep ) < 185 && ph_IsEB[0] )' %(photon_cuts, fsr_cut), ( 60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', logy=1 )

    #if save :
    #    name = 'ph_sigmaIEIE__mmg__EB__Cut_m_leplepph+m_leplep_185__Cut_%s' %fsr_lab
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #samplesWg.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && ( m_leplepph+m_leplep ) < 185 && ph_IsEE[0] )' %(photon_cuts, fsr_cut), ( 50, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.002', logy=1  )

    #if save :
    #    name = 'ph_sigmaIEIE__mmg__EE__Cut_m_leplepph+m_leplep_185__Cut_%s' %fsr_lab
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ##---------------------------------------
    ## We have two possible event cuts, look 
    ## at how each cut affects sigmaIEIE
    ##---------------------------------------

    #samplesWg.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && fabs( m_leplepph-91.2 ) < 5 && ph_IsEB[0] ) '%(photon_cuts, fsr_cut), 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && ( m_leplepph+m_leplep ) < 185 && ph_IsEB[0]  ) ' %(photon_cuts, fsr_cut)], ['Data']*2, (60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', colors=[ROOT.kBlue, ROOT.kRed], legend_entries=[ '|M_{#mu#mu#gamma} - M_{Z}| < 5', 'M_{#mu#mu} + M_{#mu#mu#gamma} < 185 '])

    #if save :
    #    name = 'ph_sigmaIEIE__mmg__EB__CompMassCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #samplesWg.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && fabs( m_leplepph-91.2 ) < 5 && ph_IsEE[0] ) ' %(photon_cuts, fsr_cut), 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && %s && ( m_leplepph+m_leplep ) < 185 && ph_IsEE[0]  ) ' %(photon_cuts, fsr_cut)], ['Data']*2, (50, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.002', colors=[ROOT.kBlue, ROOT.kRed], legend_entries=[ '|M_{#mu#mu#gamma} - M_{Z}| < 5', 'M_{#mu#mu} + M_{#mu#mu#gamma} < 185 '])

    #if save :
    #    name = 'ph_sigmaIEIE__mmg__EE__CompMassCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #bins = [(None, None)]
    #for idx, min in enumerate( analysis_bins_mgg[:-1] ) :
    #    max = analysis_bins_mgg[idx+1]
    #    if min < 15 : 
    #        continue
    #    bins.append( (min, max) )

    #bins[-1] = ( bins[-1][0], None )

    ##bins = bins[3:]

    #for ptmin, ptmax in bins :

    #    cut_str = ''
    #    name_str = ''

    #    if ptmin is not None :
    #        cut_str += ' && ph_pt[0] > %d' %ptmin
    #        name_str = '__pt_%d-max' %ptmin
    #    if ptmax is not None :
    #        cut_str += ' && ph_pt[0] < %d' %ptmax
    #        name_str = '__pt_%d-%d' %(ptmin, ptmax)


    #    samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplepph-91.2 ) < 5 && %s && ph_IsEE[0] %s)'%(photon_cuts, fsr_cut, cut_str)]*2 + ['PUWeight * (mu_passtrig_n>0 && mu_n==1 && ph_n==1 && %s && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25 && ph_IsEE[0] && leadPhot_leadLepDR>0.4 %s )' %(photon_cuts, cut_str)], ['Data', 'Zgamma', 'Wgamma'], (50, 0, 0.1 ), normalize=1, colors=[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], doratio=1, xlabel='#sigma i#etai#eta', ylabel='Normalized Events / 0.002', rlabel='MC / Data', legend_entries=['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'], ymin=0.00001, ymax=5, logy=1, rmin=0.2, rmax=1.8 )

    #    if save :
    #        name = 'ph_sigmaIEIE__EE%s__CompDataRealPhotonMCTruthMatchPhoton'%name_str
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')


    #    samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplepph-91.2 ) < 5 && %s && ph_IsEB[0] %s)' %(photon_cuts, fsr_cut, cut_str)]*2 + ['PUWeight * (mu_passtrig_n>0 && mu_n==1 && ph_n==1 && %s && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25 && ph_IsEB[0] && leadPhot_leadLepDR>0.4 %s )' %(photon_cuts, cut_str)], ['Data', 'Zgamma', 'Wgamma'], (60, 0, 0.03 ), normalize=1, colors=[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], doratio=1, xlabel='#sigma i#etai#eta', ylabel='Normalized Events / 0.0005', rlabel='MC / Data', legend_entries=['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'], ymin=0.00001, ymax=5, logy=1, rmin=0.2, rmax=1.8 )

    #    if save :
    #        name = 'ph_sigmaIEIE__EB%s__CompDataRealPhotonMCTruthMatchPhoton'%name_str
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')

    #    samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplepph-91.2 ) < 5 && %s && ph_IsEE[0] %s)'%(photon_cuts, fsr_cut, cut_str)]*2 + ['PUWeight * (mu_passtrig_n>0 && mu_n==1 && ph_n==1 && %s && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25 && ph_IsEE[0] && leadPhot_leadLepDR>0.4 %s )' %(photon_cuts, cut_str)], ['Data', 'Zgamma', 'Wgamma'], [0, 0.033, 0.1], normalize=1, colors=[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], doratio=1, xlabel='#sigma i#etai#eta', ylabel='Normalized Events / 0.002', rlabel='MC / Data', legend_entries=['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'], ymin=0.00001, ymax=5, logy=1, rmin=0.2, rmax=1.8 )

    #    if save :
    #        name = 'ph_sigmaIEIE__EE%s__CompDataRealPhotonMCTruthMatchPhoton_twoBin'%name_str
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')


    #    samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplepph-91.2 ) < 5 && %s && ph_IsEB[0] %s)' %(photon_cuts, fsr_cut, cut_str)]*2 + ['PUWeight * (mu_passtrig_n>0 && mu_n==1 && ph_n==1 && %s && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25 && ph_IsEB[0] && leadPhot_leadLepDR>0.4 %s)' %(photon_cuts, cut_str)], ['Data', 'Zgamma', 'Wgamma'], [0, 0.011, 0.03], normalize=1, colors=[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], doratio=1, xlabel='#sigma i#etai#eta', ylabel='Normalized Events / 0.0005', rlabel='MC / Data', legend_entries=['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'], ymin=0.00001, ymax=5, logy=1, rmin=0.2, rmax=1.8 )

    #    if save :
    #        name = 'ph_sigmaIEIE__EB%s__CompDataRealPhotonMCTruthMatchPhoton_twoBin'%name_str
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')

  
    #samplesWg.CompareSelections( 'ph_pt[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4 )'%photon_cuts]*2 + ['PUWeight * (ph_n==1 && %s && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25 )' %photon_cuts], ['Data', 'Zgamma', 'Wgamma'], (50, 0, 200 ), normalize=1, colors=[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], doratio=1, xlabel='photon p_{T} [GeV]', rlabel='MC / Data', legend_entries=['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'], ymin=0.00001, ymax=5, logy=1, rmin=0.2, rmax=1.8, legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #if save :
    #    name = 'ph_pt__CompDataRealPhotonMCTruthMatchPhoton'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ##------------------------------
    ##------------------------------
    ## background template -- motivate event cuts
    ##------------------------------
    ##------------------------------

    #samplesWg.Draw( 'leadPhot_sublLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplep-91.2 ) < 5 )'%photon_cuts, (50, 0, 5), xlabel='#Delta R( #gamma, sublead lepton)', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #if save :
    #    name = 'leadPhot_sublLepDR__mmg__Cut_m_leplep_10GeVWindow'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    #samplesWg.Draw( 'leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplep-91.2 ) < 5 )'%photon_cuts, (50, 0, 5), xlabel='#Delta R( #gamma, sublead lepton)', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #if save :
    #    name = 'leadPhot_leadLepDR__mmg__Cut_m_leplep_10GeVWindow'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEB[0] )'%photon_cuts, (60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #if save :
    #    name = 'ph_sigmaIEIE__EB__mmg__ZJetsCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEE[0] )'%photon_cuts, (40, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0025', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #if save :
    #    name = 'ph_sigmaIEIE__EE__mmg__ZJetsCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ## Inv ChIso
    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEB[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 )', (60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #if save :
    #    name = 'ph_sigmaIEIE__EB__mmg__chIso_5_10__ZJetsCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEE[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 )', (40, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0025', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #if save :
    #    name = 'ph_sigmaIEIE__EE__mmg__chIso_5_10__ZJetsCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ## Inv ChIso
    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEB[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 )', (60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #if save :
    #    name = 'ph_sigmaIEIE__EB__mmg__chIso_5_20__ZJetsCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEE[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 )', (40, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0025', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #if save :
    #    name = 'ph_sigmaIEIE__EE__mmg__chIso_5_20__ZJetsCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    #for idx, min in enumerate( analysis_bins_mgg[:-1] ) :
    #    max = analysis_bins_mgg[idx+1]
    #    if min < 15 : 
    #        continue

    #    samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEB[0] && ph_pt[0] > %f && ph_pt[0] < %f)'%(photon_cuts,min, max) , (60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #    if save :
    #        minname = str(min)
    #        maxname = str(max)
    #        if max == analysis_bins_mgg[-1] :
    #            maxname = 'max'
    #        name = 'ph_sigmaIEIE__EB__mmg__ptbins_%s-%s__ZJetsCR' %(minname, maxname )
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')


    #    samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEE[0] && ph_pt[0] > %f && ph_pt[0] < %f )'%(photon_cuts, min, max), (40, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0025', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #    if save :
    #        minname = str(min)
    #        maxname = str(max)
    #        if max == analysis_bins_mgg[-1] :
    #            maxname = 'max'
    #        name = 'ph_sigmaIEIE__EE__mmg__ptbins_%s-%s__ZJetsCR' %(minname, maxname )
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')

    #    samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEB[0] && ph_pt[0] > %f && ph_pt[0] < %f && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10)'%(min, max) , (60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #    if save :
    #        minname = str(min)
    #        maxname = str(max)
    #        if max == analysis_bins_mgg[-1] :
    #            maxname = 'max'
    #        name = 'ph_sigmaIEIE__EB__mmg__ptbins_%s-%s__chIso_5_10__ZJetsCR' %(minname, maxname )
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')


    #    samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEE[0] && ph_pt[0] > %f && ph_pt[0] < %f && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 )'%(min, max), (40, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0025', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #    if save :
    #        minname = str(min)
    #        maxname = str(max)
    #        if max == analysis_bins_mgg[-1] :
    #            maxname = 'max'
    #        name = 'ph_sigmaIEIE__EE__mmg__ptbins_%s-%s__chIso_5_10__ZJetsCR' %(minname, maxname )
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')

    #    samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEB[0] && ph_pt[0] > %f && ph_pt[0] < %f && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20)'%(min, max) , (60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #    if save :
    #        minname = str(min)
    #        maxname = str(max)
    #        if max == analysis_bins_mgg[-1] :
    #            maxname = 'max'
    #        name = 'ph_sigmaIEIE__EB__mmg__ptbins_%s-%s__chIso_5_20__ZJetsCR' %(minname, maxname )
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')


    #    samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEE[0] && ph_pt[0] > %f && ph_pt[0] < %f && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 )'%(min, max), (40, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0025', legendConfig=samplesWg.config_legend(legendWiden=1.5) )

    #    if save :
    #        minname = str(min)
    #        maxname = str(max)
    #        if max == analysis_bins_mgg[-1] :
    #            maxname = 'max'
    #        name = 'ph_sigmaIEIE__EE__mmg__ptbins_%s-%s__chIso_5_20__ZJetsCR' %(minname, maxname )
    #        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    else :
    #        raw_input('continue')
    ##--------------------------------------
    ##--------------------------------------
    ## Study the effect of inverting an isolation variable on sigmaIEIE
    ##--------------------------------------
    ##--------------------------------------

    ##--------------------------------------
    ## Charged Iso
    ##--------------------------------------
    #draw_samples = ['Zgammastar', 'MuonRealPhotonSub']
    #for samp in draw_samples :

    #        cutname = 'ph_chIsoCorr'
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], [samp]*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')
    #        
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], [samp]*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')
    #        
    #        cutname = 'ph_SCRChIso'
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], [samp]*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')

    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], [samp]*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')

    #        #--------------------------------------
    #        # Neutral Iso
    #        #--------------------------------------

    #        cutname = 'ph_neuIsoCorr'
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')

    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')
    #        
    #        cutname = 'ph_SCRNeuIso'
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')

    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')

    #        #--------------------------------------
    #        # Photon Iso
    #        #--------------------------------------

    #        cutname = 'ph_phoIsoCorr'
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passPhoIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')
    #        
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passPhoIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')
    #        
    #        cutname = 'ph_SCRPhoIso'
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')

    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')

    #        #--------------------------------------
    #        # Mult Iso
    #        #--------------------------------------

    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s && ph_chIsoCorr[0] < 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 )' %( common_selection), 'PUWeight * ( %s && ph_chIsoCorr[0] < 8 && ph_neuIsoCorr[0] < 5 && ph_phoIsoCorr[0] < 5  )' %( common_selection ), 'PUWeight * ( %s && ph_chIsoCorr[0] < 10 && ph_neuIsoCorr[0] < 7 && ph_phoIsoCorr[0] < 7 )' %( common_selection),'PUWeight * ( %s && ph_chIsoCorr[0] < 12 && ph_neuIsoCorr[0] < 9 && ph_phoIsoCorr[0] < 9   )' %( common_selection)], [samp]*5, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Iso cuts', '5,3,3 (ch,neu,pho)', '8,5,5 (ch,neu,pho)', '10,7,7 (ch,neu,pho)', '12,9,9 (ch,neu,pho)' ], rlabel='Loose Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EB__mmg__%s__CompLoosenedIsoCuts' %(samp), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')
    #        
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s && ph_chIsoCorr[0] < 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 )' %( common_selection), 'PUWeight * ( %s && ph_chIsoCorr[0] < 8 && ph_neuIsoCorr[0] < 5 && ph_phoIsoCorr[0] < 5  )' %( common_selection ), 'PUWeight * ( %s && ph_chIsoCorr[0] < 10 && ph_neuIsoCorr[0] < 7 && ph_phoIsoCorr[0] < 7 )' %( common_selection),'PUWeight * ( %s && ph_chIsoCorr[0] < 12 && ph_neuIsoCorr[0] < 9 && ph_phoIsoCorr[0] < 9   )' %( common_selection)], [samp]*5, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Iso cuts', '5,3,3 (ch,neu,pho)', '8,5,5 (ch,neu,pho)', '10,7,7 (ch,neu,pho)', '12,9,9 (ch,neu,pho)'], rlabel='Loose Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EE__mmg__%s__CompLoosenedIsoCuts' %(samp), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')
    #        
    #        cutname = 'ph_SCRPhoIso'
    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')

    #        common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    #        samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], [samp]*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
    #        if save :
    #            samplesWg.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
    #        else :
    #            raw_input('continue')

    var_bins_eb = [0, 0.011, 0.03]
    var_bins_ee = [0, 0.033, 0.1] 
    pt_cuts = [(None, None), (15, 25), (25, 40), (40, 80), (80, None)]
    draw_samples = ['Zgammastar', 'MuonRealPhotonSub']
    for samp in draw_samples :
        for ptmin, ptmax in pt_cuts :

            pt_draw = ''
            pt_name = ''
            if ptmin is not None :
                pt_draw += ' && ph_pt[0] > %d ' %ptmin
                pt_name = '__pt_%d-max' %ptmin
            if ptmax is not None :
                pt_draw += ' && ph_pt[0] < %d ' %ptmax
                pt_name = '__pt_%d-%s' %(ptmin, ptmax)


            cutname = 'ph_chIsoCorr'
            common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0] %s' %pt_draw
            #samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], [samp]*6, var_bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
            samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname)], [samp]*4, var_bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
            if save :
                samplesWg.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts%s__varBins' %(samp, cutname, pt_name), options.outputDir+'/'+subdir, 'base')
            else :
                raw_input('continue')
            
            common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0] %s' %pt_draw
            #samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], [samp]*6, var_bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
            samplesWg.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname)], [samp]*4, var_bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.8)
            if save :
                samplesWg.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts%s__varBins' %(samp, cutname, pt_name), options.outputDir+'/'+subdir, 'base')
            else :
                raw_input('continue')
            

    ##-----------------------------------
    ##-----------------------------------
    ## Look at diphotons using loosened iso
    ##-----------------------------------
    ##-----------------------------------

    #photon_cuts_looseiso = 'ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_chIsoCorr[0]< 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 && ph_chIsoCorr[1]< 5 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3'

    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEB[0] && ph_IsEB[1] )' %photon_cuts_looseiso, (60, 0, 0.03), xlabel = 'Lead photon #sigmai#etai#eta', ylabel='Events / 0.0005', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EB__loosenedIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_sigmaIEIE[1]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEB[0] && ph_IsEB[1] )' %photon_cuts_looseiso, (60, 0, 0.03), xlabel = 'Sublead photon #sigmai#etai#eta', ylabel='Events / 0.0005', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EB_EB__loosenedIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEB[0] && ph_IsEE[1] )' %photon_cuts_looseiso, (60, 0, 0.03), xlabel = 'Lead photon #sigmai#etai#eta', ylabel='Events / 0.0005', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EE__loosenedIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_sigmaIEIE[1]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEB[0] && ph_IsEE[1] )' %photon_cuts_looseiso, (40, 0, 0.1), xlabel = 'Sublead photon #sigmai#etai#eta', ylabel='Events / 0.0025', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EB_EE__loosenedIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEE[0] && ph_IsEB[1] )' %photon_cuts_looseiso, (40, 0, 0.1), xlabel = 'Lead photon #sigmai#etai#eta', ylabel='Events / 0.0025', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EE_EB__loosenedIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_sigmaIEIE[1]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEE[0] && ph_IsEB[1] )' %photon_cuts_looseiso, (60, 0, 0.03), xlabel = 'Sublead photon #sigmai#etai#eta', ylabel='Events / 0.0005', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EE_EB__loosenedIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEE[0] && ph_IsEE[1] )' %photon_cuts_looseiso, (40, 0, 0.1), xlabel = 'Lead photon #sigmai#etai#eta', ylabel='Events / 0.0025', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EE_EE__loosenedIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_sigmaIEIE[1]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEE[0] && ph_IsEE[1] )' %photon_cuts_looseiso, (40, 0, 0.1), xlabel = 'Sublead photon #sigmai#etai#eta', ylabel='Events / 0.0025', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EE_EE__loosenedIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')


    ##-----------------------------------
    ##-----------------------------------
    ## Look at diphotons using full iso
    ##-----------------------------------
    ##-----------------------------------

    #photon_cuts_fulliso = 'ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1]'

    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEB[0] && ph_IsEB[1] )' %photon_cuts_fulliso, (60, 0, 0.03), xlabel = 'Lead photon #sigmai#etai#eta', ylabel='Events / 0.0005', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EB__fullIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_sigmaIEIE[1]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEB[0] && ph_IsEB[1] )' %photon_cuts_fulliso, (60, 0, 0.03), xlabel = 'Sublead photon #sigmai#etai#eta', ylabel='Events / 0.0005', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EB_EB__fullIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEB[0] && ph_IsEE[1] )' %photon_cuts_fulliso, (60, 0, 0.03), xlabel = 'Lead photon #sigmai#etai#eta', ylabel='Events / 0.0005', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EE__fullIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_sigmaIEIE[1]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEB[0] && ph_IsEE[1] )' %photon_cuts_fulliso, (40, 0, 0.1), xlabel = 'Sublead photon #sigmai#etai#eta', ylabel='Events / 0.0025', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EB_EE__fullIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEE[0] && ph_IsEB[1] )' %photon_cuts_fulliso, (40, 0, 0.1), xlabel = 'Lead photon #sigmai#etai#eta', ylabel='Events / 0.0025', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EE_EB__fullIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_sigmaIEIE[1]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEE[0] && ph_IsEB[1] )' %photon_cuts_fulliso, (60, 0, 0.03), xlabel = 'Sublead photon #sigmai#etai#eta', ylabel='Events / 0.0005', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EE_EB__fullIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')


    #samplesWg.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEE[0] && ph_IsEE[1] )' %photon_cuts_fulliso, (40, 0, 0.1), xlabel = 'Lead photon #sigmai#etai#eta', ylabel='Events / 0.0025', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EE_EE__fullIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_sigmaIEIE[1]', 'PUWeight * ( mu_passtrig_n==0 && mu_n==1 && %s && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_phDR>0.3 && ph_IsEE[0] && ph_IsEE[1] )' %photon_cuts_fulliso, (40, 0, 0.1), xlabel = 'Sublead photon #sigmai#etai#eta', ylabel='Events / 0.0025', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87) )
    #            
    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EE_EE__fullIso__baselineCuts'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    #else :
    #    samplesWg.DumpStack()
    #    raw_input('continue')

    ##------------------------------------------
    ## Compare sigmaIEIE on one photon
    ## and vary isolation cuts on the other photon
    ## when the other photon fails sigmaIEIE
    ##------------------------------------------

    #phph_base = 'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && m_phph>15 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && ph_IsEB[0] && ph_IsEB[1]'

    #loose_subl = ' ph_sigmaIEIE[1] > 0.013010 && ph_sigmaIEIE[1] < 0.299000 '
    #loose_lead = ' ph_sigmaIEIE[0] > 0.013010 && ph_sigmaIEIE[0] < 0.299000 '

    #looseiso_subl = 'ph_chIsoCorr[1] < 5 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] <3'
    #looseiso_lead = 'ph_chIsoCorr[0] < 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] <3'

    #morelooseiso_subl = 'ph_chIsoCorr[1] < 10 && ph_neuIsoCorr[1] < 6 && ph_phoIsoCorr[1] <6'
    #morelooseiso_lead = 'ph_chIsoCorr[0] < 10 && ph_neuIsoCorr[0] < 6 && ph_phoIsoCorr[0] <6'

    #tightiso_subl = 'ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1]'
    #tightiso_lead = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'

    #sample ='Muon'

    ## Lead loose, sublead, loose to none
    #samplesWg.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * (  %s && %s && %s  && %s  )' %( phph_base, loose_subl, looseiso_subl, looseiso_lead ), 'PUWeight * (  %s && %s && %s )' %(phph_base, loose_subl, looseiso_lead ) ], [sample, sample], (30, 0, 0.03), normalize=1, colors=[ROOT.kBlack, ROOT.kRed ], doratio=1, legend_entries=['Loose iso lead, loose iso subl', 'loose iso lead, no iso subl'], ylabel='Normalized Events / 0.0001', xlabel='#sigma i#etai#eta', ymin=0, ymax=0.5, rmin=0, rmax=4, legendConfig={'legendWiden' : 1.5, 'legendCompress' : 1.4} )

    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EB__baselineCuts__comp_sieie_lead_loose_subl_loose_to_none'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ## Subl loose, lead, loose to none
    #samplesWg.CompareSelections('ph_sigmaIEIE[1]', ['PUWeight * (  %s && %s && %s && %s  )' %( phph_base, loose_lead, looseiso_lead, looseiso_subl ), 'PUWeight * (  %s && %s && %s )' %(phph_base, loose_lead, looseiso_subl ) ], [sample, sample], (30, 0, 0.03), normalize=1, colors=[ROOT.kBlack, ROOT.kRed ], doratio=1, legend_entries=['Loose iso subl, loose iso lead', 'Loose iso lead, no iso subl'], ylabel='Normalized Events / 0.0001', xlabel='#sigma i#etai#eta', ymin=0, ymax=0.5, rmin=0, rmax=4, legendConfig={'legendWiden' : 1.5, 'legendCompress' : 1.4} )

    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EB_EB__baselineCuts__comp_sieie_subl_loose_lead_loose_to_none'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ## Lead tight, sublead, tight to loose 
    #samplesWg.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * (  %s && %s && %s  && %s  )' %( phph_base, loose_subl, tightiso_subl, tightiso_lead ), 'PUWeight * (  %s && %s && %s && %s )' %(phph_base, loose_subl, tightiso_lead, looseiso_subl ) ], [sample, sample], (30, 0, 0.03), normalize=1, colors=[ROOT.kBlack, ROOT.kRed ], doratio=1, legend_entries=['Tight iso lead, Tight iso subl', 'Tight iso lead, Loose iso subl'], ylabel='Normalized Events / 0.0001', xlabel='#sigma i#etai#eta', ymin=0, ymax=0.5, rmin=0, rmax=4, legendConfig={'legendWiden' : 1.5, 'legendCompress' : 1.4} )

    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EB__baselineCuts__comp_sieie_lead_tight_subl_tight_to_loose'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ## subl tight, lead, tight to loose 
    #samplesWg.CompareSelections('ph_sigmaIEIE[1]', ['PUWeight * (  %s && %s && %s && %s  )' %( phph_base, loose_lead, tightiso_lead, tightiso_subl ), 'PUWeight * (  %s && %s && %s && %s )' %(phph_base, loose_lead, tightiso_subl, looseiso_lead) ], [sample, sample], (30, 0, 0.03), normalize=1, colors=[ROOT.kBlack, ROOT.kRed ], doratio=1, legend_entries=['Tight iso subl, Tight iso lead', 'Tight iso subl, Loose iso lead'], ylabel='Normalized Events / 0.0001', xlabel='#sigma i#etai#eta', ymin=0, ymax=0.5, rmin=0, rmax=4, legendConfig={'legendWiden' : 1.5, 'legendCompress' : 1.4} )

    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EB__baselineCuts__comp_sieie_subl_tight_lead_tight_to_loose'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ## Lead tight, sublead, tight to more loose 
    #samplesWg.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * (  %s && %s && %s  && %s  )' %( phph_base, loose_subl, tightiso_subl, tightiso_lead ), 'PUWeight * (  %s && %s && %s && %s )' %(phph_base, loose_subl, tightiso_lead, morelooseiso_subl ) ], [sample, sample], (30, 0, 0.03), normalize=1, colors=[ROOT.kBlack, ROOT.kRed ], doratio=1, legend_entries=['Tight iso lead, Tight iso subl', 'Tight iso lead, More Loose iso subl'], ylabel='Normalized Events / 0.0001', xlabel='#sigma i#etai#eta', ymin=0, ymax=0.5, rmin=0, rmax=4, legendConfig={'legendWiden' : 1.5, 'legendCompress' : 1.4} )

    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EB__baselineCuts__comp_sieie_lead_tight_subl_tight_to_moreloose'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ## subl tight, lead, tight to more loose 
    #samplesWg.CompareSelections('ph_sigmaIEIE[1]', ['PUWeight * (  %s && %s && %s && %s  )' %( phph_base, loose_lead, tightiso_lead, tightiso_subl ), 'PUWeight * (  %s && %s && %s && %s )' %(phph_base, loose_lead, tightiso_subl, morelooseiso_lead) ], [sample, sample], (30, 0, 0.03), normalize=1, colors=[ROOT.kBlack, ROOT.kRed ], doratio=1, legend_entries=['Tight iso subl, Tight iso lead', 'Tight iso subl, More Loose iso lead'], ylabel='Normalized Events / 0.0001', xlabel='#sigma i#etai#eta', ymin=0, ymax=0.5, rmin=0, rmax=4, legendConfig={'legendWiden' : 1.5, 'legendCompress' : 1.4} )

    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EB__baselineCuts__comp_sieie_subl_tight_lead_tight_to_moreloose'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ## Lead tight, sublead, tight to none
    #samplesWg.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * (  %s && %s && %s  && %s  )' %( phph_base, loose_subl, tightiso_subl, tightiso_lead ), 'PUWeight * (  %s && %s && %s )' %(phph_base, loose_subl, tightiso_lead ) ], [sample, sample], (30, 0, 0.03), normalize=1, colors=[ROOT.kBlack, ROOT.kRed ], doratio=1, legend_entries=['Tight iso lead, tight iso subl', 'Tight iso lead'], ylabel='Normalized Events / 0.0001', xlabel='#sigma i#etai#eta', ymin=0, ymax=0.5, rmin=0, rmax=4, legendConfig={'legendWiden' : 1.5, 'legendCompress' : 1.4} )

    #if save :
    #    name = 'ph_sigmaIEIE_lead__mgg__EB_EB__baselineCuts__comp_sieie_lead_tight_subl_tight_to_none'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    ## subl tight, lead, tight to none
    #samplesWg.CompareSelections('ph_sigmaIEIE[1]', ['PUWeight * (  %s && %s && %s && %s  )' %( phph_base, loose_lead, tightiso_lead, tightiso_subl ), 'PUWeight * (  %s && %s && %s )' %(phph_base, loose_lead, tightiso_subl) ], [sample, sample], (30, 0, 0.03), normalize=1, colors=[ROOT.kBlack, ROOT.kRed ], doratio=1, legend_entries=['Tight iso subl, tight iso lead', 'Tight iso subl'], ylabel='Normalized Events / 0.0001', xlabel='#sigma i#etai#eta', ymin=0, ymax=0.5, rmin=0, rmax=4, legendConfig={'legendWiden' : 1.5, 'legendCompress' : 1.4} )

    #if save :
    #    name = 'ph_sigmaIEIE_subl__mgg__EB_EB__baselineCuts__comp_sieie_subl_tight_lead_tight_to_none'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

def MakeJetFakeFactorPlots(save=False, detail=100) :

    subdir = 'JetFakeFactorPlots'

    cut_invsieie_eb = 0.013
    cut_invsieie_ee = 0.035

    #var_bins = (40, 0, 200, [0, 5, 10, 15, 20, 25, 30, 40, 60, 100, 200] )
    var_bins = (40, 0, 200, [0, 5, 10, 15, 20, 25, 30, 40, 60,  200] )
    bins = (40, 0, 200)

    base_cuts = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0]<0.05 && ph_hasPixSeed[0]==0 '
    fake_cr_cuts = 'fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 '

    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0]  && ph_IsEE[0] && %s)' %( base_cuts, fake_cr_cuts) ,bins , xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Endcap photons', logy=1 )

    #if save :
    #    name = 'ph_pt__mmg__EE__Cut_passphoIso_passneuIso_chIsoWindow5-20_passSIEIE__ZjetsFakeCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEE[0] && %s )' %( base_cuts, cut_invsieie_ee, fake_cr_cuts ) , bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Endcap photons', logy=1  )

    #if save :
    #    name = 'ph_pt__mmg__EE__Cut_invphoIso_invneuIso_chIsoWindow5-20_invSIEIE__ZjetsFakeCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0]  && ph_IsEB[0] && %s)' %( base_cuts, fake_cr_cuts) , bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Barrel photons', logy=1 )

    #if save :
    #    name = 'ph_pt__mmg__EB__Cut_passphoIso_passneuIso_chIsoWindow5-20_passSIEIE__ZjetsFakeCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEB[0] && %s )' %( base_cuts, cut_invsieie_eb, fake_cr_cuts ) , bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Barrel photons', logy=1  )

    #if save :
    #    name = 'ph_pt__mmg__EB__Cut_invphoIso_invneuIso_chIsoWindow5-20_invSIEIE__ZjetsFakeCR'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0]  && ph_IsEE[0] && %s)' %( base_cuts, fake_cr_cuts) ,var_bins , xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Endcap photons', logy=1 )

    #if save :
    #    name = 'ph_pt__mmg__EE__Cut_passphoIso_passneuIso_chIsoWindow5-20_passSIEIE__ZjetsFakeCR__varBins'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEE[0] && %s )' %( base_cuts, cut_invsieie_ee, fake_cr_cuts ) , var_bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Endcap photons', logy=1  )

    #if save :
    #    name = 'ph_pt__mmg__EE__Cut_invphoIso_invneuIso_chIsoWindow5-20_invSIEIE__ZjetsFakeCR__varBins'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0]  && ph_IsEB[0] && %s)' %( base_cuts, fake_cr_cuts) , var_bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Barrel photons', logy=1 )

    #if save :
    #    name = 'ph_pt__mmg__EB__Cut_passphoIso_passneuIso_chIsoWindow5-20_passSIEIE__ZjetsFakeCR__varBins'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEB[0] && %s )' %( base_cuts, cut_invsieie_eb, fake_cr_cuts ) , var_bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Barrel photons', logy=1  )

    #if save :
    #    name = 'ph_pt__mmg__EB__Cut_invphoIso_invneuIso_chIsoWindow5-20_invSIEIE__ZjetsFakeCR__varBins'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #if detail < 1 :
    #    return
    #-------------------------
    #-------------------------
    # Look at chIso to determine window size
    #-------------------------
    #-------------------------

    samplesWg.Draw( 'ph_chIsoCorr[0]', 'PUWeight * ( %s && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEB[0] && %s )' %( base_cuts, cut_invsieie_eb, fake_cr_cuts ) , (50, 0, 50), xlabel='Charged Hadron iso [GeV]', labelStyle='fancy', extra_label='Barrel photons', extra_label_loc=(0.45, 0.87), logy=1, ymax=5e4, legendConfig=samplesWg.config_legend(legendLoc='Double')  )

    if save :
        name = 'ph_chIsoCorr__mmg__EB__Cut_invNeuPhoIso_invSIEIE__ZjetsFakeCR'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    else :
        raw_input('continue')


    samplesWg.Draw( 'ph_chIsoCorr[0]', 'PUWeight * ( %s && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEE[0] && %s )' %( base_cuts, cut_invsieie_ee, fake_cr_cuts ) , (50, 0, 50), xlabel='Charged Hadron iso [GeV]', labelStyle='fancy', extra_label='Endcap photons', extra_label_loc=(0.6, 0.87), logy=1, legendConfig=samplesWg.config_legend(legendLoc='Double')   )

    if save :
        name = 'ph_chIsoCorr__mmg__EE__Cut_invNeuPhoIso_invSIEIE__ZjetsFakeCR'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    else :
        raw_input('continue')

    samplesWg.Draw( 'ph_chIsoCorr[0]', 'PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0] && ph_IsEB[0] && %s )' %( base_cuts, fake_cr_cuts ) , (50, 0, 50), xlabel='Charged Hadron iso [GeV]', labelStyle='fancy', extra_label='Barrel photons', extra_label_loc=(0.6, 0.87), logy=0 )

    if save :
        name = 'ph_chIsoCorr__mmg__EB__Cut_passNeuPhoIso_passSIEIE__ZjetsFakeCR'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    else :
        raw_input('continue')

    samplesWg.Draw( 'ph_chIsoCorr[0]', 'PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0] && ph_IsEE[0] && %s )' %( base_cuts, fake_cr_cuts ) , (50, 0, 50), xlabel='Charged Hadron iso [GeV]', labelStyle='fancy', extra_label='Endcap photons', extra_label_loc=(0.6, 0.87), logy=0, legendConfig=samplesWg.config_legend() )

    if save :
        name = 'ph_chIsoCorr__mmg__EE__Cut_passNeuPhoIso_passSIEIE__ZjetsFakeCR'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    else :
        raw_input('continue')

    print detail

    if detail < 2 :
        print 'RETURN'
        return

    #-------------------------
    #-------------------------
    # Motivate choice of loose selection
    #-------------------------
    #-------------------------

    base_cuts = 'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 '


    #-------------------------
    # Full Iso -- EB EB
    #-------------------------

    ph_iso_cuts = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1]'

    ## fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ##real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ##fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ##-------------------------
    ## Full Iso -- EE EE
    ##-------------------------

    ##fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##-------------------------
    ## Full Iso -- EB EE
    ##-------------------------


    ## fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##-------------------------
    ## Full Iso -- EE EB
    ##-------------------------


    ## fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')



    #-------------------------
    # Inv Iso -- EB EB
    #-------------------------

    ph_iso_cuts_ff = '!ph_passChIsoCorrMedium[0] && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && !ph_passChIsoCorrMedium[1] && !ph_passNeuIsoCorrMedium[1] && !ph_passPhoIsoCorrMedium[1]'
    ph_iso_cuts_fr = '!ph_passChIsoCorrMedium[0] && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1]'
    ph_iso_cuts_rf = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && !ph_passChIsoCorrMedium[1] && !ph_passNeuIsoCorrMedium[1] && !ph_passPhoIsoCorrMedium[1]'

    ## fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ##real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ##fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ##-------------------------
    ## Inv Iso -- EE EE
    ##-------------------------

    ##fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##-------------------------
    ## Inv Iso -- EB EE
    ##-------------------------


    ## fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##-------------------------
    ## Inv Iso -- EE EB
    ##-------------------------


    ## fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )

    if save :
        name = 'ph_pt_subl__mgg__EE_EB__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    else :
        raw_input('continue')


    ##-------------------------
    ## Inv Iso, Ch iso window -- EB EB
    ##-------------------------

    #ph_iso_cuts_ff = '!ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && !ph_passNeuIsoCorrMedium[1] && !ph_passPhoIsoCorrMedium[1] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 && ph_chIsoCorr[1] > 5 && ph_chIsoCorr[1] < 20'
    #ph_iso_cuts_fr = '!ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && ph_passNeuIsoCorrMedium[1]  && ph_passPhoIsoCorrMedium[1]  && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 && ph_chIsoCorr[1] > 5 && ph_chIsoCorr[1] < 20'
    #ph_iso_cuts_rf = 'ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]    && !ph_passNeuIsoCorrMedium[1] && !ph_passPhoIsoCorrMedium[1] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 && ph_chIsoCorr[1] > 5 && ph_chIsoCorr[1] < 20'

    ## fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ##real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ##fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ##-------------------------
    ## Inv Iso, Ch iso window -- EE EE
    ##-------------------------

    ##fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')


    ##-------------------------
    ## Inv Iso, Ch iso window -- EB EE
    ##-------------------------


    ## fake fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## real fake

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )
    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    ## fake real

    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')

    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )

    #if save :
    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
    #else :
    #    raw_input('continue')



#
# The following is to get the history 
#
import atexit
historyPath = os.path.expanduser("~/.pyhistory")
try:
    import readline
except ImportError:
    print "Module readline not available."
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")
    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)


# -----------------------------------------------------------------
def save_history(historyPath=historyPath):
    try:
        import readline
    except ImportError:
        print "Module readline not available."
    else:
        readline.write_history_file(historyPath)

atexit.register(save_history)

main()
