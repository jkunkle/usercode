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

p.add_argument('--save'          , default=False, action='store_true',   dest='save'        , help='save plots ( must provide outputDir )')
p.add_argument('--detailLevel'   , default=100, type=int, dest='detailLevel'      , help='make only plots at this detail level (make all plots by default)')
p.add_argument('--makeAll'       , default=False, action='store_true',   dest='makeAll'     , help='make all plots')
p.add_argument('--makeEvent'     , default=False, action='store_true',   dest='makeEvent'   , help='make Wgg event plots')
p.add_argument('--makeMva'       , default=False, action='store_true',   dest='makeMva'     , help='make electron veto mva plots')
p.add_argument('--makeEleVeto'   , default=False, action='store_true',   dest='makeEleVeto' , help='make electron veto comparison plots')
p.add_argument('--makeEleFake'   , default=False, action='store_true',   dest='makeEleFake' , help='make electron fake factor plots')
p.add_argument('--makeEleCR'     , default=False, action='store_true',   dest='makeEleCR' , help='make electron fake factor application control region plots')
p.add_argument('--makeLepLepGamma' , default=False, action='store_true',   dest='makeLepLepGamma'  , help='make dilepton + photon')
p.add_argument('--makeLepGamma' , default=False, action='store_true',   dest='makeLepGamma'  , help='make single lepton + photon plots')
p.add_argument('--makeJetFakeTemplate' , default=False, action='store_true',   dest='makeJetFakeTemplate' , help='make jet fake plots, template method')
p.add_argument('--makeJetFakeSyst' , default=False, action='store_true',   dest='makeJetFakeSyst' , help='make jet fake plots used for syst uncertainties')
p.add_argument('--makeJetFakeFactor' , default=False, action='store_true',   dest='makeJetFakeFactor' , help='make jet fake plots, fake factor method')
p.add_argument('--makeSpecial' , default=False, action='store_true',   dest='makeSpecial' , help='make overlap removal plots')

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

analysis_bins_mgg = [0, 5, 10, 15, 25, 40, 70, 150 ] 
analysis_bins_egg = [0, 5, 10, 15, 25, 40, 70, 150 ] 
#analysis_bins_mgg = [0, 5, 10, 15, 35, 40, 70, 150 ] 
#analysis_bins_egg = [0, 5, 10, 15, 35, 40, 70, 150 ] 

eveto_bins = [15, 20, 25, 30, 40, 50, 70, 1000000]

lead_dr_cut = 0.4
subl_dr_cut = 0.4
phot_dr_cut = 0.4
m_ph1_ph2_cut = 0

_z_mass_cut = 10

_baseline_cuts_mgg = ' mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==2 && el_n==0 && dr_ph1_ph2>%(drgg).1f && dr_ph1_leadLep>%(drg1l).1f && dr_ph2_leadLep>%(drg2l).1f '%{'drgg' : phot_dr_cut, 'drg1l' : lead_dr_cut, 'drg2l' : subl_dr_cut}
_baseline_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_mediumPassPSV_n==2 && mu_n==0 && dr_ph1_ph2>%(drgg).1f && dr_ph1_leadLep>%(drg1l).1f && dr_ph2_leadLep>%(drg2l).1f '%{'drgg' : phot_dr_cut, 'drg1l' : lead_dr_cut, 'drg2l' : subl_dr_cut}
_zrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_mediumPassPSV_n==2 && mu_n==0 && dr_ph1_ph2>%(drgg).1f && dr_ph1_leadLep>%(drg1l).1f && dr_ph2_leadLep>%(drg2l).1f  && !(fabs(m_leadLep_ph1_ph2-91.2) < %(zcut)d) && !(fabs(m_leadLep_ph1-91.2) < %(zcut)d)  && !(fabs(m_leadLep_ph2-91.2) < %(zcut)d) ' %{'drgg' : phot_dr_cut, 'drg1l' : lead_dr_cut, 'drg2l' : subl_dr_cut, 'zcut' : _z_mass_cut}
_zcr_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_mediumPassPSV_n==2 && mu_n==0 && dr_ph1_ph2>%(drgg).1f && dr_ph1_leadLep>%(drg1l).1f && dr_ph2_leadLep>%(drg2l).1f && ( (fabs(m_leadLep_ph1_ph2-91.2) < %(zcut)d) || (fabs(m_leadLep_ph1-91.2) < %(zcut)d)  || (fabs(m_leadLep_ph2-91.2) < %(zcut)d) ) '  %{'drgg' : phot_dr_cut, 'drg1l' : lead_dr_cut, 'drg2l' : subl_dr_cut, 'zcut' : _z_mass_cut}

invPixLead_cuts_egg         = ' el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && mu_n==0 && ph_eleVeto[0]==1 && ph_eleVeto[1]==0 && dr_ph1_ph2>%.1f && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f '%(phot_dr_cut, lead_dr_cut, subl_dr_cut)
invPixSubl_cuts_egg         = ' el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && mu_n==0 && ph_eleVeto[0]==0 && ph_eleVeto[1]==1 && dr_ph1_ph2>%.1f && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f '%(phot_dr_cut, lead_dr_cut, subl_dr_cut)



#------------------------------
# basic photon cuts
#------------------------------
_photon_cuts_nopix_nosieie  = ' ph_mediumNoSIEIENoEleVeto_n==1 '
_photon_cuts_nopix_nochiso  = ' ph_mediumNoChIsoNoEleVeto_n==1 '
_photon_cuts_nopix_noneuiso = ' ph_mediumNoNeuIsoNoEleVeto_n==1 '
_photon_cuts_nopix_nophoiso = ' ph_mediumNoPhoIsoNoEleVeto_n==1 '

_photon_idx_nopix_nosieie  = ' ptSorted_ph_mediumNoSIEIENoEleVeto_idx '
_photon_idx_nopix_nochiso  = ' ptSorted_ph_mediumNoChIsoNoEleVeto_idx '
_photon_idx_nopix_noneuiso = ' ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx '
_photon_idx_nopix_nophoiso = ' ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx'

#------------------------------
# single photon cuts
#------------------------------
baseline_cuts_mg = ' mu_passtrig25_n>0  && ph_mediumNoEleVeto_n==1  && leadPhot_leadLepDR>%.1f '%(lead_dr_cut)
baseline_cuts_mg_psv = ' mu_passtrig25_n>0  && ph_mediumPassCSEV_n==1  && leadPhot_leadLepDR>%.1f '%(lead_dr_cut)
baseline_cuts_eg = ' el_passtrig_n>0 && ph_mediumPassCSEV_n==1  && leadPhot_leadLepDR>%.1f '%(lead_dr_cut)
baseline_cuts_eg_noPixVeto = ' el_passtrig_n>0 && ph_mediumNoEleVeto_n==1 && leadPhot_leadLepDR>%.1f  '%(lead_dr_cut)
zcr_cuts_eg      = ' el_passtrig_n>0 && ph_mediumPassCSEV_n==1 && leadPhot_leadLepDR>%.1f && m_lepph1 > 76 && m_lepph1 < 106 '%(lead_dr_cut)

baseline_cuts_mmg = ' mu_passtrig25_n>0 && mu_n>1 && ph_mediumNoEleVeto_n==1  && leadPhot_leadLepDR>%.1f && leadPhot_sublLepDR>%.1f '%(lead_dr_cut, lead_dr_cut)
baseline_cuts_mmg_psv = ' mu_passtrig25_n>0 && mu_n>1 && ph_mediumPassCSEV_n==1  && leadPhot_leadLepDR>%.1f && leadPhot_sublLepDR>%.1f '%(lead_dr_cut, lead_dr_cut)
baseline_cuts_eeg = ' el_passtrig_n>0 && el_n>1 && ph_mediumPassCSEV_n==1 && leadPhot_leadLepDR>%.1f && leadPhot_sublLepDR>%.1f '%(lead_dr_cut, lead_dr_cut)

def main() :

    global samplesWggSp
    global samplesWggMu
    global samplesWggEl
    global samplesWg
    global samplesLLG
    global samplesLGG
    global samplesPhOlap

    baseDirWg  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09'
    #baseDirWggSp = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNomUnblindAllNoEleVeto_2015_07_16'
    baseDirWggSp = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhID_2015_11_09'
    baseDirWggMu = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAllNoMtCutPt15_2015_11_11'
    baseDirWggEl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElUnblindAllNoZCutNoMtCutPt15_2015_11_11'
    baseDirLLG = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_11_09'
    baseDirLGG = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhID_2015_11_09'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfWgg = 'Modules/PlotWgamgam.py'
    sampleConfWg  = 'Modules/WgamgamForBkg.py'
    sampleConfLLG = 'Modules/WgamgamForBkg.py'
    sampleConfLGG = 'Modules/WgamgamForBkg.py'
    sampleConfPhOlap = 'Modules/PhOlapComp.py'

    samplesWggSp   = SampleManager(baseDirWggSp, treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    samplesWggMu   = SampleManager(baseDirWggMu, treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    samplesWggEl   = SampleManager(baseDirWggEl, treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    samplesWg      = SampleManager(baseDirWg , treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    samplesLLG     = SampleManager(baseDirLLG , treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    samplesLGG     = SampleManager(baseDirLGG , treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    samplesPhOlap  = SampleManager(baseDirLLG , treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)

    samplesWggSp    .ReadSamples( sampleConfWgg )
    samplesWggMu    .ReadSamples( sampleConfWgg )
    samplesWggEl    .ReadSamples( sampleConfWgg )
    samplesWg     .ReadSamples( sampleConfWg )
    samplesLLG    .ReadSamples( sampleConfLLG )
    samplesLGG    .ReadSamples( sampleConfLGG )
    samplesPhOlap .ReadSamples( sampleConfPhOlap )

    if options.save :
        ROOT.gROOT.SetBatch(True)

    if options.outputDir is not None :
        samplesWg.start_command_collection()
        samplesWggMu.start_command_collection()
        samplesWggEl.start_command_collection()
        samplesLLG.start_command_collection()
        samplesLGG.start_command_collection()

    if options.makeAll or options.makeEvent :
        MakeWggEventPlots( save=options.save, detail=options.detailLevel )
        #MakeWggEventPlots( save=options.save, detail=options.detailLevel, ph_cuts=' && pt_leadph12 < 40', dirPostfix='UnblindLowPt', activate_data=True)

    if options.makeAll or options.makeSpecial :
        MakeSpecialWggPlots( save=options.save, detail=options.detailLevel )

    # depricated
    #if options.makeAll or options.makeMva:
    #    MakeWggMvaPlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeEleVeto:
        MakeWggEleVetoCompPlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeEleFake:
        MakeEleFakePlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeEleCR:
        MakeWggEleCRPlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeLepLepGamma :
        MakeLepLepGammaPlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeLepGamma :
        MakeLepGammaPlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeJetFakeTemplate:
        MakePhotonJetFakePlots( save=options.save, detail=options.detailLevel )

    if options.makeAll or options.makeJetFakeFactor:
        MakeJetFakeFactorPlots(save=options.save, detail=options.detailLevel) 

    if options.makeAll or options.makeJetFakeSyst:
        MakeJetFakeSystPlots() 

    print 'run samplesWg'
    samplesWg.run_commands(nFilesPerJob=1)
    print 'run samplesWggMu'
    samplesWggMu.run_commands(nFilesPerJob=5)
    print 'run samplesWggEl'
    samplesWggEl.run_commands(nFilesPerJob=5)
    print 'run samplesLLG'
    samplesLLG.run_commands(nFilesPerJob=1)
    print 'run samplesLGG'
    samplesLGG.run_commands(nFilesPerJob=1)
    print '^_^ Finished ^_^'
    print 'You can kill the program if it is hanging'
#---------------------------------------
# User functions
#---------------------------------------

#---------------------------------------
def MakeWggEventPlots( save=False, detail=100, ph_cuts='', dirPostfix='', activate_data=False ) :

    subdir='WggEventPlots%s' %dirPostfix


    if save and options.outputDir is None :
        print 'Must provide an outputDir to save plots'
        save=False

    label_loc_d_mu = (0.73, 0.87)
    label_loc_d_el = (0.7, 0.87)

    # legend config can come from any SampleManager
    legend_conf_d = samplesWggSp.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double' )

    baseline_cuts_mgg = _baseline_cuts_mgg + ph_cuts
    baseline_cuts_egg = _baseline_cuts_egg + ph_cuts
    zrej_cuts_egg     = _zrej_cuts_egg     + ph_cuts
    zcr_cuts_egg      = _zcr_cuts_egg      + ph_cuts

    #-----------------------------------
    # Make baseline plots
    #-----------------------------------
    MakeEventPlotSuite( channel='egg', sampMan=samplesWggEl, cuts=baseline_cuts_egg, nom_label_loc=(0.2, 0.86), double_label_loc=label_loc_d_el, suffix='__baselineCuts', subdir=subdir, outputDir=options.outputDir, save=save )
    MakeEventPlotSuite( channel='mgg', sampMan=samplesWggMu, cuts=baseline_cuts_mgg, nom_label_loc=(0.2, 0.86), double_label_loc=label_loc_d_mu, suffix='__baselineCuts', subdir=subdir, outputDir=options.outputDir, save=save )

    mass_met_cuts = ' && m_ph1_ph2 > %d && mt_lep_met > 40 ' %( m_ph1_ph2_cut )

    MakeEventPlotSuite( channel='egg', sampMan=samplesWggEl, cuts=baseline_cuts_egg+mass_met_cuts, nom_label_loc=(0.2, 0.86), double_label_loc=label_loc_d_el, suffix='__massMetCuts', subdir=subdir, outputDir=options.outputDir, save=save  )
    MakeEventPlotSuite( channel='mgg', sampMan=samplesWggMu, cuts=baseline_cuts_mgg+mass_met_cuts, nom_label_loc=(0.2, 0.86), double_label_loc=label_loc_d_mu, suffix='__massMetCuts', subdir=subdir, outputDir=options.outputDir, save=save  )

    MakeEventPlotSuite( channel='egg', sampMan=samplesWggEl, cuts=zrej_cuts_egg, nom_label_loc=(0.2, 0.86), double_label_loc=label_loc_d_el, suffix='__ZRejCuts', subdir=subdir, outputDir=options.outputDir, save=save  )
    MakeEventPlotSuite( channel='egg', sampMan=samplesWggEl, cuts=zrej_cuts_egg+mass_met_cuts, nom_label_loc=(0.2, 0.86), double_label_loc=label_loc_d_el, suffix='__massMetZRejCuts', subdir=subdir, outputDir=options.outputDir, save=save  )

    #-----------------------------------
    # 2 object  mass (lep-lead)
    # electron + some Z rej cuts
    #-----------------------------------
    samplesWggEl.Draw('m_leadLep_ph1', 'PUWeight * (  %s  && !(fabs(m_leadLep_ph1_ph2-91.2) < %d) )' %( baseline_cuts_egg, _z_mass_cut ), (40, 0, 200 ) , hist_config={'logy':0,  'ymin' : 0, 'ymax' : 80, 'xlabel':'M_{e, lead #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'Electron Channel',   'extra_label_loc':label_loc_d_el }, legend_config=legend_conf_d )
    if save :
        name = 'm_leadLep_ph1__egg__Cut_m_leadLep_ph1_ph2_20gevWindow'
        samplesWggEl.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWggEl.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWggEl.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')


    samplesWggEl.Draw('m_leadLep_ph2', 'PUWeight * ( %s && !(fabs(m_lepphph-91.2) < %d) )' %( baseline_cuts_egg, _z_mass_cut), (40, 0, 200 ) , hist_config={'logy':0,  'ymin' : 0, 'ymax' : 100, 'xlabel':'M_{e, sublead #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'Electron Channel',   'extra_label_loc':(0.2, 0.86) }, legend_config=samplesWggEl.config_legend(legendWiden=1.3,legendCompress=1.3, ) )

    if save :
        name = 'm_leadLep_ph2__egg__Cut_m_leadLep_ph1_ph2_20gevWindow'
        samplesWggEl.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWggEl.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWggEl.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

    samplesWggEl.Draw('m_leadLep_ph2', 'PUWeight * ( %s && !(fabs(m_leadLep_ph1_ph2-91.2) < %d) && !(fabs(m_leadLep_ph1-91.2) < %d) )' %(baseline_cuts_egg, _z_mass_cut, _z_mass_cut), (40, 0, 200 ) , hist_config={'logy':0,  'xlabel':'M_{e, sublead #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'Electron Channel',   'extra_label_loc':(0.2, 0.86) }, legend_config=samplesWggEl.config_legend(legendWiden=1.3,legendCompress=1.3, ) )
    if save :
        name = 'm_leadLep_ph2__egg__Cut_m_leadLep_ph1_ph2_20gevWindow__Cut_m_leadLep_ph1_20gevWindow'
        samplesWggEl.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWggEl.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWggEl.DumpStack(options.outputDir+'/'+subdir, )
        raw_input('continue')

def MakeSpecialWggPlots(save=False, detail=100, ph_cuts='', dirPostfix='', activate_data=False ) : 

    subdir='WggEventPlots%s' %dirPostfix


    if save and options.outputDir is None :
        print 'Must provide an outputDir to save plots'
        save=False

    label_loc_d_mu = (0.73, 0.87)
    label_loc_d_el = (0.7, 0.87)

    # legend config can come from any SampleManager
    legend_conf_d = samplesWggSp.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double' )

    samplesWggSp.activate_sample( 'ISR')
    samplesWggSp.activate_sample( 'FSR')
    samplesWggSp.deactivate_sample( 'Wgg')

    #------------------------------------
    # Make some plots with the 
    # lepton/photon cuts, but not 
    # the full baseline cuts
    #------------------------------------
    samplesWggSp.Draw('dr_ph1_leadLep', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n>1 && dr_ph1_ph2>%.1f && el_n==0 %s )' %(phot_dr_cut, ph_cuts), (25, 0, 5 ) , 
                      hist_config={'ymin': 0.1, 'ymax':100000, 'logy':1, 'xlabel':'#Delta R( #mu, lead #gamma)', 'ylabel':'Events / 0.2',}, 
                      label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':label_loc_d_mu}, 
                      legend_config=legend_conf_d )

    if save :
        name = 'dr_ph1_leadLep__mgg__noLepPhDRCuts__splitWggISRFSR'
        samplesWggSp.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWggSp.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWggSp.Draw('dr_ph1_leadLep', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_mediumPassPSV_n>1 && dr_ph1_ph2>%.1f && mu_n==0  %s )' %(phot_dr_cut, ph_cuts), (25, 0, 5 ) , hist_config={'ymin':0.1, 'ymax':80000, 'logy':1, 'xlabel':'#Delta R(e, lead #gamma)', 'ylabel':'Events / 0.2'}, label_config={'labelStyle':'fancy', 'extra_label':'Electron Channel', 'extra_label_loc':label_loc_d_el}, legend_config=legend_conf_d  )

    if save :
        name = 'dr_ph1_leadLep__egg__noLepPhDRCuts__splitWggISRFSR'
        samplesWggSp.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWggSp.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWggSp.Draw('dr_ph2_leadLep', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n>1 && dr_ph1_ph2>%.1f  && el_n==0  %s )' %(phot_dr_cut, ph_cuts), (25, 0, 5 ) , hist_config={'ymin':0.1, 'ymax':10000, 'logy':1, 'xlabel':'#Delta R(#mu, sublead #gamma)', 'ylabel':'Events / 0.2'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':label_loc_d_mu}, legend_config=legend_conf_d )

    if save :
        name = 'dr_ph2_leadLep__mgg__noLepPhDRCuts__splitWggISRFSR'
        samplesWggSp.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWggSp.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    samplesWggSp.Draw('dr_ph2_leadLep', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_mediumPassPSV_n>1 && dr_ph1_ph2>%.1f  && mu_n==0  %s )' %(phot_dr_cut, ph_cuts), (25, 0, 5 ) , hist_config={'ymin':0.1, 'ymax':50000, 'logy':1, 'xlabel':'#Delta R(e, sublead #gamma)', 'ylabel':'Events / 0.2' }, label_config={'labelStyle':'fancy', 'extra_label':'Electron Channel', 'extra_label_loc':label_loc_d_el}, legend_config=legend_conf_d  )

    if save :
        name = 'dr_ph2_leadLep__egg__noLepPhDRCuts__splitWggISRFSR'
        samplesWggSp.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        samplesWggSp.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        raw_input('continue')


    samplesWggSp.deactivate_sample( 'ISR')
    samplesWggSp.deactivate_sample( 'FSR')
    samplesWggSp.activate_sample( 'Wgg')

    #------------------------------------
    # make plots for overlap removal 
    #------------------------------------

    samplesPhOlap.Draw( 'm_leplepph', ' PUWeight * (mu_passtrig25_n>0 && mu_n == 2 && ph_mediumNoEleVeto_n>0 )', ( 100, 0, 200 ), hist_config={'xlabel' : 'M_{#mu #mu #gamma} [GeV]' }, label_config = {'labelStyle' : 'fancy' }, legend_config=samplesPhOlap.config_legend(legendCompress=2.0, legend_widen=1.5 ) )

    if save :
        name = 'm_leplepph_mmg__phOlap' 
        samplesPhOlap.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        raw_input('continue')

    samplesPhOlap.Draw( 'leadPhot_sublLepDR', ' PUWeight * (mu_passtrig25_n>0 && mu_n == 2 && ph_mediumNoEleVeto_n>0 )', ( 50, 0, 5 ), hist_config={'xlabel' : '#Delta R(sublead #mu, #gamma)','ylabel' : 'Events / 0.1' }, label_config = {'labelStyle' : 'fancy' }, legend_config=samplesPhOlap.config_legend(legendCompress=2.0, legend_widen=1.5 ) )

    if save :
        name = 'leadPhot_sublLepDR_mmg__phOlap' 
        samplesPhOlap.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        raw_input('continue')

def MakeEventPlotSuite( channel, sampMan, cuts, nom_label_loc, double_label_loc, suffix='', subdir='', outputDir=None, save=False ) :

    legend_conf_d = sampMan.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double' )
    legend_conf   = sampMan.config_legend( legendWiden=1.3,legendCompress=1.3 )

    if channel == 'egg' :
        channel_label = 'Electron Channel'
    if channel == 'mgg' :
        channel_label = 'Muon Channel'

    #-----------------------------------
    # lepton pT
    #-----------------------------------
    if channel == 'egg' : 
        pt_str = 'el_pt'
        label_str = 'p_{T}^{e} [GeV]'
    if channel == 'mgg' : 
        pt_str = 'mu_pt'
        label_str = 'p_{T}^{#mu} [GeV]'

    sampMan.Draw(pt_str+'[0]', 'PUWeight * ( %s )' %(cuts), (60, 0, 300 ) , hist_config={'logy':1,  'ymin' : 0.1, 'ymax' : 1000, 'xlabel':label_str}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':nom_label_loc}, legend_config=legend_conf )

    if save :
        name = '%s__%s%s' %( pt_str, channel, suffix )
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # lepton eta
    #-----------------------------------
    if channel == 'egg' : 
        eta_str = 'el_eta'
        label_str = '#eta^{e} '
    if channel == 'mgg' : 
        eta_str = 'mu_eta'
        label_str = '#eta^{#mu} '

    ymax = 80
    if channel == 'egg' and suffix == '__baselineCuts' :
        ymax = 100

    sampMan.Draw(eta_str+'[0]', 'PUWeight * ( %s )' %(cuts), (25, -2.5, 2.5 ) , hist_config={'logy':0,  'ymin' : 0, 'ymax' : ymax, 'xlabel':label_str, 'ylabel' : 'Events / 0.2'} , label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = '%s__%s%s' %( eta_str, channel, suffix )
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # MET
    #-----------------------------------
    sampMan.Draw('pfType01MET', 'PUWeight * ( %s )' %(cuts), (40, 0, 200 ) , 
                 hist_config={'logy':1, 'ymin':0.1, 'ymax':5000, 'xlabel':'E_{T}^{miss} [GeV]'} , 
                 label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':double_label_loc}, 
                 legend_config=legend_conf_d )

    if save :
        name = 'pfType01MET__%s%s' %( channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # transverse mass
    #-----------------------------------
    sampMan.Draw('mt_lep_met', 'PUWeight * ( %s )' %(cuts), (40, 0, 200 ) , hist_config={'logy':1, 'ymin':0.1, 'ymax':5000,  'xlabel':'m_{T} (l, E_{T}^{miss}) [GeV]'} , label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'mt_lep_met__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    sampMan.Draw('mt_lepph1_met', 'PUWeight * ( %s )' %(cuts), (40, 0, 200 ) , hist_config={'logy':1, 'ymin':0.1, 'ymax':5000,  'xlabel':'m_{T} (l+lead #gamma, E_{T}^{miss}) [GeV]'} , label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'mt_lepph1_met__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    sampMan.Draw('mt_lepph2_met', 'PUWeight * ( %s )' %(cuts), (40, 0, 200 ) , hist_config={'logy':1, 'ymin':0.1, 'ymax':5000,  'xlabel':'m_{T} (l+sublead #gamma, E_{T}^{miss}) [GeV]'} , label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'mt_lepph2_met__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    sampMan.Draw('mt_lepphph_met', 'PUWeight * ( %s )' %(cuts), (40, 0, 200 ) , hist_config={'logy':1, 'ymin':0.1, 'ymax':5000,  'xlabel':'m_{T} (l+lead #gamma+sublead #gamma, E_{T}^{miss}) [GeV]'} , label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'mt_lepphph_met__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # 3 object  mass
    #-----------------------------------
    sampMan.Draw('m_leadLep_ph1_ph2', 'PUWeight * ( %s )' %(cuts), (60, 0, 300 ) , hist_config={'logy':0,  'xlabel':'M_{e,#gamma,#gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':nom_label_loc}, legend_config=legend_conf )

    if save :
        name = 'm_leadLep_ph1_ph2__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')


    #-----------------------------------
    # 2 object  mass (lep-lead)
    #-----------------------------------
    ymax = 100
    if channel=='egg' and suffix=='__baselineCuts' :
        ymax = 160

    sampMan.Draw('m_leadLep_ph1', 'PUWeight * ( %s )' %(cuts), (40, 0, 200 ) , hist_config={'logy':0,  'ymin' : 0, 'ymax' : ymax, 'xlabel':'M_{e, lead #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'm_leadLep_ph1__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # 2 object  mass (lep-subl)
    #-----------------------------------
    sampMan.Draw('m_leadLep_ph2', 'PUWeight * ( %s )' %( cuts ), (40, 0, 200 ) , hist_config={'logy':0,  'xlabel':'M_{e, sublead #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,   'extra_label_loc':nom_label_loc }, legend_config=legend_conf )

    if save :
        name = 'm_leadLep_ph2__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # 2 object  mass (photons)
    #-----------------------------------
    sampMan.Draw('m_ph1_ph2', 'PUWeight * ( %s )' %(cuts), (40, 0, 200 ) , hist_config={'logy':1, 'ymin':0.1, 'ymax':4000 ,  'xlabel':'M_{#gamma, #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,  'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'm_ph1_ph2__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # object separation
    #-----------------------------------
    #-----------------------------------
    # DR(gg)
    #-----------------------------------

    sampMan.Draw('dr_ph1_ph2', 'PUWeight * ( %s )' %(cuts), (25, 0, 5 ) , hist_config={'logy':0, 'ymin':0.1, 'ymax':120 ,  'xlabel':'(#Delta R(#gamma, #gamma)', 'ylabel' : 'Events / 0.2'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,  'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'dr_ph1_ph2__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # DPhi(gg)
    #-----------------------------------

    sampMan.Draw('fabs(dphi_ph1_ph2)', 'PUWeight * ( %s )' %(cuts), (32, 0, 3.2 ) , hist_config={'logy':0, 'ymin':0, 'ymax':70 ,  'xlabel':'(#Delta #phi(#gamma, #gamma)', 'ylabel' : 'Events / 0.1'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,  'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'dphi_ph1_ph2__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # DR(l, lead)
    #-----------------------------------
    ymax=100
    if channel == 'egg' and suffix=='__baselineCuts' :
        ymax = 160

    sampMan.Draw('dr_ph1_leadLep', 'PUWeight * ( %s )' %(cuts), (25, 0, 5 ) , hist_config={'logy':0, 'ymin':0, 'ymax':ymax ,  'xlabel':'(#Delta R(e, lead #gamma)', 'ylabel' : 'Events / 0.2'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,  'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'dr_ph1_leadLep__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # DPhi(l, lead )
    #-----------------------------------
    ymax = 50
    if channel == 'egg' and suffix=='__baselineCuts' :
        ymax = 120

    sampMan.Draw('fabs(dphi_ph1_leadLep)', 'PUWeight * ( %s )' %(cuts), (32, 0, 3.2 ) , hist_config={'logy':0, 'ymin':0, 'ymax':ymax ,  'xlabel':'(#Delta #phi(e, lead #gamma)', 'ylabel' : 'Events / 0.1'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,  'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'dphi_ph1_leadLep__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    #-----------------------------------
    # DR(l, subl)
    #-----------------------------------
    ymax = 120
    if channel == 'egg' and suffix=='__baselineCuts' :
        ymax = 200

    sampMan.Draw('dr_ph2_leadLep', 'PUWeight * ( %s )' %(cuts), (25, 0, 5 ) , hist_config={'logy':0, 'ymin':0, 'ymax':ymax ,  'xlabel':'(#Delta R(e, sublead #gamma)', 'ylabel' : 'Events / 0.2'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,  'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'dr_ph2_leadLep__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')


    #-----------------------------------
    # DPhi(l, subl )
    #-----------------------------------
    ymax = 60
    if channel == 'egg' and suffix=='__baselineCuts' :
        ymax = 140

    sampMan.Draw('fabs(dphi_ph2_leadLep)', 'PUWeight * ( %s )' %(cuts), (32, 0, 3.2 ) , hist_config={'logy':0, 'ymin':0, 'ymax':ymax ,  'xlabel':'(#Delta #phi(e, sublead #gamma)', 'ylabel' : 'Events / 0.1'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label,  'extra_label_loc':double_label_loc}, legend_config=legend_conf_d )

    if save :
        name = 'dphi_ph2_leadLep__%s%s' %(channel, suffix)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
    else :
        raw_input('continue')

    # --------------------------------------
    # electron channel , photon pT
    # --------------------------------------
    if channel=='egg' :
        analysis_bins = analysis_bins_egg
    if channel=='mgg' :
        analysis_bins = analysis_bins_mgg

    sampMan.Draw('pt_leadph12', ' PUWeight * ( %s ) ' %cuts, (20, 0, 200 ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':1000,  'xlabel':'lead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label, 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )
    if save :
        name = 'ph_pt_lead__%s%s' %(channel, suffix)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
    else :
        sampMan.DumpStack(outputDir+'/'+subdir, )
        raw_input('continue')

    sampMan.Draw('pt_leadph12', ' PUWeight * ( %s ) ' %cuts, (analysis_bins[-1]/5, 0, analysis_bins[-1], analysis_bins ), hist_config={'logy':1, 'ymin':0.5, 'ymax':1000,  'xlabel':'lead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label, 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )
    if save :
        name = 'ph_pt_lead__%s%s__varBins'%( channel, suffix)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
    else :
        sampMan.DumpStack(outputDir+'/'+subdir, )
        raw_input('continue')


    sampMan.Draw('pt_sublph12', ' PUWeight * ( %s ) ' %cuts ,(20, 0, 200 ),  hist_config={'logy':1, 'ymin':0.5, 'ymax':1000,  'xlabel':'sublead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label, 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )
    if save :
        name = 'ph_pt_subl__%s%s'%( channel, suffix)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
    else :
        sampMan.DumpStack(outputDir+'/'+subdir, )
        raw_input('continue')

    sampMan.Draw('pt_sublph12', ' PUWeight * ( %s ) ' %cuts, (analysis_bins[-1]/5, 0, analysis_bins[-1], analysis_bins ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':1000,  'xlabel':'sublead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label, 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )
    if save :
        name = 'ph_pt_subl__%s%s__varBins'%( channel, suffix)
        sampMan.DumpStack(outputDir+'/'+subdir, name)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
    else :
        sampMan.DumpStack(outputDir+'/'+subdir, )
        raw_input('continue')

    #----------------------
    # Subleading pt for
    # lead pt > 40 GeV
    #----------------------
    sampMan.Draw('pt_sublph12', ' PUWeight * ( %s && pt_leadph12 > %d ) ' %(cuts, analysis_bins[-3]), (20, 0, 200 ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':500,  'xlabel':'sublead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label, 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )
    if save :
        name = 'ph_pt_subl__%s%s__leadPt%d'%( channel, suffix, analysis_bins[-3])
        sampMan.DumpStack(outputDir+'/'+subdir, name)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
    else :
        sampMan.DumpStack(outputDir+'/'+subdir, )
        raw_input('continue')

    sampMan.Draw('pt_sublph12', ' PUWeight * ( %s && pt_leadph12 > %d ) ' %(cuts, analysis_bins[-3]), (analysis_bins[-1]/5, 0, analysis_bins[-1], analysis_bins ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':500,  'xlabel':'sublead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label, 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )
    if save :
        name = 'ph_pt_subl__%s%s__leadPt%d__varBins'%( channel, suffix, analysis_bins[-3])
        sampMan.DumpStack(outputDir+'/'+subdir, name)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
    else :
        sampMan.DumpStack(outputDir+'/'+subdir, )
        raw_input('continue')

    #----------------------
    # Subleading pt for
    # lead pt > 70 GeV
    #----------------------
    sampMan.Draw('pt_sublph12', ' PUWeight * ( %s && pt_leadph12 > %d ) ' %(cuts, analysis_bins[-2]), (20, 0, 200 ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':500,  'xlabel':'sublead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label, 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )
    if save :
        name = 'ph_pt_subl__%s%s__leadPt%d'%( channel, suffix, analysis_bins[-2])
        sampMan.DumpStack(outputDir+'/'+subdir, name)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
    else :
        sampMan.DumpStack(outputDir+'/'+subdir, )
        raw_input('continue')

    sampMan.Draw('pt_sublph12', ' PUWeight * ( %s && pt_leadph12 > %d ) ' %(cuts, analysis_bins[-2]), (analysis_bins[-1]/5, 0, analysis_bins[-1], analysis_bins ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':500,  'xlabel':'sublead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label, 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )
    if save :
        name = 'ph_pt_subl__%s%s__leadPt%d__varBins'%( channel, suffix, analysis_bins[-2])
        sampMan.DumpStack(outputDir+'/'+subdir, name)
        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
    else :
        sampMan.DumpStack(outputDir+'/'+subdir, )
        raw_input('continue')

    #-------------------------------------
    # make eta-pt dependent cuts
    #-------------------------------------

    eta_cuts = [['EB', 'EB'],['EB', 'EE'],['EE', 'EB'],['EE', 'EE']]
    eta_labels = ['Barrel photons', 'Lead photon in Barrel, sublead in Endcap','Lead photon in Endcap, sublead in Barrel', 'Endcap photons']

    binning_mod = list( analysis_bins )
    binning_mod[-1] = 1000000

    for ec, lab in zip(eta_cuts, eta_labels) :

        for idx, min in enumerate(binning_mod[:-1]) :
            if min < 15 : 
                continue
            max = binning_mod[idx+1]

            sampMan.Draw('pt_leadph12', ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %d && pt_leadph12 < %d )' %(cuts, ec[0], ec[1], min, max), (40, 0, 200 ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':100,  'xlabel':'lead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{%s}{%s}'%(channel_label, lab), 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )

            if save :
                if idx+2 == len(binning_mod) :
                    name = 'ph_pt_lead__%s__%s-%s%s__ptbins_%d-max' %(channel, ec[0], ec[1], suffix, min)
                else :
                    name = 'ph_pt_lead__%s__%s-%s%s__ptbins_%d-%d' %(channel, ec[0], ec[1], suffix, min, max)
                sampMan.DumpStack(outputDir+'/'+subdir, name)
                sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
            else :
                sampMan.DumpStack( )
                raw_input('continue')

            sampMan.Draw('pt_sublph12', ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %d && pt_leadph12 < %d )' %(cuts, ec[0], ec[1], min, max), (40, 0, 200 ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':100,  'xlabel':'sublead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{%s}{%s}'%(channel_label, lab), 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )

            if save :
                if idx+2 == len(binning_mod) :
                    name = 'ph_pt_subl__%s__%s-%s%s__ptbins_%d-max' %(channel, ec[0], ec[1], suffix,min)
                else :
                    name = 'ph_pt_subl__%s__%s-%s%s__ptbins_%d-%d' %(channel, ec[0], ec[1],suffix, min, max)
                sampMan.DumpStack(outputDir+'/'+subdir, name)
                sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
            else :
                sampMan.DumpStack( )
                raw_input('continue')

        # put back in for subl_bins

        #for minl, maxl, mins, maxs in subl_bins :

        #    sampMan.Draw('pt_leadph12', ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %d && pt_leadph12 < %d && pt_sublph12 > %d && pt_sublph12 < %d )' %(cuts, ec[0], ec[1], minl, maxl, mins, maxs), (40, 0, 200 ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':100,  'xlabel':'lead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{%s}{%s}'%(channel_label,lab), 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )

        #    if save :
        #        if maxs == analysis_bins_mgg_mod[-1] :
        #            name = 'ph_pt_lead__%s__%s-%s__baselineCuts__ptbins_%d-max__subpt_%d-max%s' %(channel, ec[0], ec[1], minl, mins, suffix)
        #        else :
        #            name = 'ph_pt_lead__%s__%s-%s__baselineCuts__ptbins_%d-max__subpt_%d-%d%s' %(channel, ec[0], ec[1],minl, mins, max, suffix)
        #        sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        #        sampMan.DumpStack(outputDir+'/'+subdir, name)
        #    else :
        #        sampMan.DumpStack( )
        #        raw_input('continue')

    #-------------------------------------
    # make eta dependent cuts also
    #-------------------------------------
    for ec, lab in zip(eta_cuts, eta_labels) :
        sampMan.Draw('pt_leadph12', ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 )' %(cuts, ec[0], ec[1]), (40, 0, 200 ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':100,  'xlabel':'lead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{%s}{%s}'%(channel_label,lab), 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )


        if save :
            name = 'ph_pt_lead__%s__%s-%s%s'%(channel, ec[0], ec[1], suffix)
            sampMan.DumpStack(outputDir+'/'+subdir, name)
            sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        else :
            sampMan.DumpStack()
            raw_input('continue')

        sampMan.Draw('pt_leadph12', ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 ) ' %(cuts, ec[0], ec[1]), (analysis_bins[-1]/5, 0, analysis_bins[-1], analysis_bins ) , hist_config={'logy':1, 'ymin':0.5, 'ymax':100,  'xlabel':'lead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':channel_label, 'extra_label_loc':nom_label_loc},   legend_config=legend_conf )
        if save :
            name = 'ph_pt_lead__%s__%s-%s%s__varBins'%(channel, ec[0], ec[1], suffix)
            sampMan.DumpStack(outputDir+'/'+subdir, name)
            sampMan.SaveStack( name, outputDir +'/' +subdir, 'base', write_command=True)
        else :
            sampMan.DumpStack()
            raw_input('continue')

    
#---------------------------------------
def MakeEleFakePlots( save=False, detail=100 ) :

    global samplesWg

    subdir = 'EleFakePlots'

    samplesWg.activate_sample( 'Data')

    # ---------------------------------
    # Draw FF derivation control regions
    # ---------------------------------
    draw_base_nom = 'el_passtrig_n>0 && el_n==1 && ph_mediumPassCSEV_n==1 && leadPhot_leadLepDR>0.4 '
    draw_base_inv = 'el_passtrig_n>0 && el_n==1 && ph_mediumFailCSEV_n==1 && leadPhot_leadLepDR>0.4 '

    pt_bins = analysis_bins_egg[3:-1]
    eta_bins = [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44), (1.44, 1.57), (1.57, 2.1), (2.1, 2.2), (2.2, 2.4), (2.4, 2.5), (0.0, 1.44), (1.44, 1.57), (1.57,2.50) ]
    eta_bins_coarse = [(0.0, 1.44), (1.44, 1.57), (1.57,2.50) ]
    pt_bins_last = [analysis_bins_egg[-2], 1000000]
    eta_bins_last = [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44), (1.44, 1.57), (1.57, 2.1), (2.1, 2.4), (2.4, 2.5), (0.0, 1.44), (1.44, 1.57), (1.57,2.50)]
    eta_bins_last_coarse = [(0.0, 1.44), (1.44, 1.57), (1.57,2.50)]

    pt_eta_bins = {}
    for ptidx, ptmin in enumerate(pt_bins[:-1] ) :
        ptmax = pt_bins[ptidx+1]
        pt_eta_bins[(ptmin,ptmax)] = eta_bins + eta_bins_coarse
    for ptidx, ptmin in enumerate(pt_bins_last[:-1] ) :
        ptmax = pt_bins_last[ptidx+1]
        pt_eta_bins[(ptmin,ptmax)] = eta_bins_last + eta_bins_last_coarse
    
    last_pt_bin = max ([x[1] for x in pt_eta_bins.keys() ] )
    for (ptmin, ptmax), etabins in pt_eta_bins.iteritems() :
        for etamin, etamax in etabins :

            # binning should match that used when fitting
            mass_binning = ( 80, 40, 200)
            if ptmax == last_pt_bin :
                mass_binning = ( 40, 40, 200 )


            if ptmin < 15 :
                continue

            samplesWg.Draw( 'm_lepph1', 'PUWeight * ( %s && fabs(ph_eta[ptSorted_ph_mediumPassCSEV_idx[0]]) > %f && fabs(ph_eta[ptSorted_ph_mediumPassCSEV_idx[0]]) < %f && ph_pt[ptSorted_ph_mediumPassCSEV_idx[0]] > %d && ph_pt[ptSorted_ph_mediumPassCSEV_idx[0]] < %d && m_lepph1 > 40 )' %( draw_base_nom, etamin, etamax, ptmin, ptmax ), mass_binning , hist_config={'logy':1, 'xlabel':'M_{e, #gamma} [GeV]'}, legend_config=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, ), )

            if save :
                if ptmax == last_pt_bin :
                    name = 'm_lepph1__eg__passCSEV__eta_%.2f-%.2f__pt_%d-max'%(etamin, etamax, ptmin)
                else :
                    name = 'm_lepph1__eg__passCSEV__eta_%.2f-%.2f__pt_%d-%d'%(etamin, etamax, ptmin, ptmax)
                samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                samplesWg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesWg.DumpStack()
                raw_input('continue')

            samplesWg.Draw( 'm_lepph1', 'PUWeight * ( %s && fabs(ph_eta[ptSorted_ph_mediumFailCSEV_idx[0]]) > %f && fabs(ph_eta[ptSorted_ph_mediumFailCSEV_idx[0]]) < %f && ph_pt[ptSorted_ph_mediumFailCSEV_idx[0]] > %d && ph_pt[ptSorted_ph_mediumFailCSEV_idx[0]] < %d && m_lepph1 > 40)' %( draw_base_inv, etamin, etamax, ptmin, ptmax ), mass_binning, hist_config={'logy':1, 'xlabel':'M_{e, #gamma} [GeV]'}, legend_config=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, ), )

            if save :
                if ptmax == last_pt_bin :
                    name = 'm_lepph1__eg__failCSEV__eta_%.2f-%.2f__pt_%d-max'%(etamin, etamax, ptmin)
                else :
                    name = 'm_lepph1__eg__failCSEV__eta_%.2f-%.2f__pt_%d-%d'%(etamin, etamax, ptmin, ptmax)
                samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                samplesWg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesWg.DumpStack()
                raw_input('continue')

#---------------------------------------
def MakeWggEleCRPlots( save=False, detail=100 ) :

    subdir = 'EleFakePlots'

    # ---------------------------------
    # Draw FF application control regions
    # ---------------------------------
    samplesWgg.Draw('m_lepphph', ' PUWeight * ( %s )' %(invPixLead_cuts_egg), (40, 0, 200 ) , hist_config={'xlabel':'M_{l,#gamma,#gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'{Invert Pix Seed Veto, lead photon}', 'extra_label_loc':(0.3, 0.86)}, legend_config=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepphph__egg__baselineCuts__invPixSeed_lead'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('m_lepphph', ' PUWeight * ( %s )' %(invPixSubl_cuts_egg), (40, 0, 200 ) ,  hist_config={'xlabel':'M_{l,#gamma,#gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'{Invert Pix Seed Veto, sublead photon}', 'extra_label_loc':(0.3, 0.86)}, legend_config=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepphph__egg__baselineCuts__invPixSeed_subl'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('m_lepph1', ' PUWeight * ( %s )' %(invPixLead_cuts_egg), (40, 0, 200 ) , hist_config={'xlabel':'M_{l,lead #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'{Invert Pix Seed Veto, lead photon}', 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepph1__egg__baselineCuts__invPixSeed_lead'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('m_lepph1', ' PUWeight * ( %s )' %(invPixSubl_cuts_egg), (40, 0, 200 ) ,  hist_config={'xlabel':'M_{l,lead #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'{Invert Pix Seed Veto, sublead photon}', 'extra_label_loc':(0.3, 0.86)}, legend_config=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepph1__egg__baselineCuts__invPixSeed_subl'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')


    samplesWgg.Draw('m_lepph2', ' PUWeight * ( %s )' %(invPixLead_cuts_egg), (40, 0, 200 ) , hist_config={'xlabel':'M_{l,sublead #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'{Invert Pix Seed Veto, lead photon}', 'extra_label_loc':(0.3, 0.86)}, legend_config=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepph2__egg__baselineCuts__invPixSeed_lead'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('m_lepph2', ' PUWeight * ( %s )' %(invPixSubl_cuts_egg), (40, 0, 200 ) , hist_config={'xlabel':'M_{l,sublead #gamma} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'{Invert Pix Seed Veto, sublead photon}', 'extra_label_loc':(0.3, 0.86)},  legend_config=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'm_lepph2__egg__baselineCuts__invPixSeed_subl'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('pt_leadph12', ' PUWeight * ( %s )' %(invPixLead_cuts_egg), (analysis_bins_egg[-1]/5, 0, analysis_bins_egg[-1], analysis_bins_egg ) ,  hist_config={'xlabel':'lead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'{Invert Pix Seed Veto, lead photon}', 'extra_label_loc':(0.3, 0.86)}, legend_config=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'ph_pt_lead__egg__baselineCuts__invPixSeed_lead'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

    samplesWgg.Draw('pt_leadph12', ' PUWeight * ( %s )' %(invPixSubl_cuts_egg), (analysis_bins_egg[-1]/5, 0, analysis_bins_egg[-1], analysis_bins_egg ) ,  hist_config={'xlabel':'sublead photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'{Invert Pix Seed Veto, sublead photon}', 'extra_label_loc':(0.3, 0.86)}, legend_config=samplesWgg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

    if save :
        name = 'ph_pt_subl__egg__baselineCuts__invPixSeed_subl'
        samplesWgg.DumpStack(options.outputDir+'/'+subdir, name)
        samplesWgg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
    else :
        samplesWgg.DumpStack( )
        raw_input('continue')

#---------------------------------------
# Depricated
#---------------------------------------
#def MakeWggMvaPlots( save=False, detail=100 ) :
#
#    global samplesWgg
#
#    subdir = 'WggMvaPlots'
#
#    selection = 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && dr_ph1_ph2>0.4 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && m_phph>15  )'
#    binning = ( 40, -0.3, 0.5)
#
#    samplesWgg.MakeRocCurve( ['zrej_mvascore']*2, [ selection ]*2, ['Wgg', 'Wgg'], ['AllBkg', 'ZjetsZgamma'], [binning]*2, doSoverB=1, debug=1, less_than=[0,0], colors=[ROOT.kRed, ROOT.kBlue], legend_entries=['B = All MC backgrounds', 'B = Zjets + Z#gamma'], ymin=0, ymax=6, legend_config=samplesWgg.config_legend( legendWiden=1.4, legendCompress=1.4, legendTranslateX=-0.35 ) )
#
#    if save :
#        name = 'zrej_mvascore__egg__baselineCuts__RocCurve1EleVetoData'
#        DumpRoc(name, inDirs=subdir)
#        SaveStack( name, 'base', inDirs=subdir )
#    else :
#        DumpRoc()
#        raw_input('continue')
#
#    samplesWgg.Draw( 'zrej_mvascore', selection, binning, xlabel='BDT score', ylabel='Events / 0.2', legend_config=samplesWgg.config_legend( legendWiden=1.1, legendCompress=1.2 ), labelStyle='fancy'  )
#
#    if save :
#        name = 'zrej_mvascore__egg__baselineCuts__1EleVetoData'
#        DumpRoc(name, inDirs=subdir)
#        SaveStack( name, 'base', inDirs=subdir )
#    else :
#        DumpRoc()
#        raw_input('continue')

#---------------------------------------
def MakeWggEleVetoCompPlots( save=False, detail=100 ) :

    global samplesWgg

    subdir = 'WggEleVetoCompPlots'

    selection = ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_mediumPassPSV_n==2 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && dr_ph1_ph2>0.4 && m_phph>15 ) '] +  ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && ( (ph_hasPixSeed[ptSorted_ph_mediumNoEleVeto_idx[0]]==1 && ph_hasPixSeed[ptSorted_ph_mediumNoEleVeto_idx[1]]==0 ) || ( ph_hasPixSeed[ptSorted_ph_mediumNoEleVeto_idx[0]]==0 && ph_hasPixSeed[ptSorted_ph_mediumNoEleVeto_idx[1]]==1 ) ) && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && dr_ph1_ph2>0.4 && m_phph>15 )']*2

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

    samplesWgg.CompareSelections( 'dr_ph1_ph2', selection , sample_names , (20, 0, 5 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='#Delta R( #gamma, #gamma)', ylabel='Normalized Events / 0.25', ymin=0, ymax=0.3  )

    if save :
        name = 'ph_phDr__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samplesWgg.Draw( 'dr_ph1_ph2', selection[2], (20, 0, 5 ), xlabel='#Delta R( #gamma, #gamma)', ylabel='Events / 0.25')

    if save :
        name = 'ph_phDr__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')


#---------------------------------------
def MakeLepGammaPlots( save=False, detail=100) :

    subdir = 'LepGammaPlots'

    #-------------------------------------
    # make eta-pt dependent cuts
    #-------------------------------------

    binnings = [analysis_bins_mgg, analysis_bins_egg, eveto_bins, analysis_bins_mgg, analysis_bins_egg, analysis_bins_egg]
    cuts = [baseline_cuts_mg, baseline_cuts_eg_noPixVeto, baseline_cuts_eg+' && m_lepph1 > 105 ', baseline_cuts_mg+' && mt_lep_met > 60 ', baseline_cuts_mg_psv+' && mt_lep_met > 60 ', baseline_cuts_eg+' && mt_lep_met > 60  && m_lepph1 > 105', zcr_cuts_eg ]
    ph_vars = ['ptSorted_ph_mediumNoEleVeto_idx[0]', 'ptSorted_ph_mediumNoEleVeto_idx[0]', 'ptSorted_ph_mediumPassCSEV_idx[0]', 'ptSorted_ph_mediumNoEleVeto_idx[0]', 'ptSorted_ph_mediumPassCSEV_idx[0]', 'ptSorted_ph_mediumPassCSEV_idx[0]', 'ptSorted_ph_mediumPassCSEV_idx[0]']
    channels  =['Muon', 'Electron', 'Electron', 'Muon', 'Muon', 'Electron', 'Electron']
    tags = ['mg', 'eg', 'eg', 'mg', 'mg', 'eg', 'eg']
    labels = ['baselineCuts', 'baselineCutsNoMassCut', 'baselineCuts', 'mtCut', 'mtCutCSEV', 'mtCut',  'ZCR']
    eta_cuts = ['EB', 'EE']
    eta_labels = ['Barrel photon', 'Endcap photon']

    for cut, binning, tag, label, channel, phvar in zip( cuts, binnings, tags, labels, channels, ph_vars ) :

        binning_mod = list( binning )
        binning_mod[-1] = 1000000

        for ec, lab in zip(eta_cuts, eta_labels) :

            #------------------------
            # pT inclusive
            #------------------------
            samplesWg.Draw('ph_pt[%s]'%phvar, ' PUWeight * ( %s && ph_Is%s[%s] )' %(cut, ec, phvar), (40, 0, 200 ) , hist_config={'logy':1, 'xlabel':'photon p_{T} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{%s Channel}{%s}'%(channel, lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
            if save :
                name = 'ph_pt__%s__%s__%s' %( tag, ec, label )
                samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                samplesWg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesWg.DumpStack( )
                raw_input('continue')

            samplesWg.Draw('mt_lep_met', ' PUWeight * ( %s && ph_Is%s[%s] )' %(cut, ec, phvar), (40, 0, 200 ) , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 100000, 'xlabel':'m_{T} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{%s Channel}{%s}'%(channel, lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
            if save :
                name = 'mt_lep_met__%s__%s__%s' %( tag, ec, label )
                samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                samplesWg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesWg.DumpStack( )
                raw_input('continue')

            samplesWg.Draw('pfType01MET', ' PUWeight * ( %s && ph_Is%s[%s] )' %(cut, ec, phvar), (40, 0, 200 ) , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 100000,  'xlabel':'E_{T}^{miss} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{%s Channel}{%s}'%(channel, lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
            if save :
                name = 'pfType01MET__%s__%s__%s' %( tag, ec, label )
                samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                samplesWg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesWg.DumpStack( )
                raw_input('continue')

            for idx, min in enumerate(binning_mod[:-1]) :
 
                if min < 15 : 
                    continue
                max = binning_mod[idx+1]

                samplesWg.Draw('mt_lep_met', ' PUWeight * ( %s && ph_Is%s[%s] && ph_pt[%s]>%d && ph_pt[%s]<%d )' %(cut, ec,phvar, phvar, min, phvar, max), (80, 0, 400 ) , hist_config={'logy':1,  'xlabel':'photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{%s Channel}{%s}'%(channel, lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

                if save :
                    if idx+2 == len(binning_mod) :
                        name = 'mt_lep_met__%s__%s__%s__ptbins_%d-max' %(tag, ec, label, min)
                    else :
                        name = 'mt_lep_met__%s__%s__%s__ptbins_%d-%d' %(tag, ec, label, min, max)
                    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                    samplesWg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
                else :
                    samplesWg.DumpStack( )
                    raw_input('continue')

                samplesWg.Draw('m_lepph1', ' PUWeight * ( %s && ph_Is%s[%s] && ph_pt[%s]>%d && ph_pt[%s]<%d )' %(cut, ec,phvar, phvar, min, phvar, max), (80, 0, 400 ) , hist_config={'logy':1,  'xlabel':'photon p_{T} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{%s Channel}{%s}'%(channel, lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesWg.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

                if save :
                    if idx+2 == len(binning_mod) :
                        name = 'm_lepph1__%s__%s__%s__ptbins_%d-max' %(tag, ec, label, min)
                    else :
                        name = 'm_lepph1__%s__%s__%s__ptbins_%d-%d' %(tag, ec, label, min, max)
                    samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                    samplesWg.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
                else :
                    samplesWg.DumpStack( )
                    raw_input('continue')

#---------------------------------------
def MakeLepLepGammaPlots( save=False, detail=100) :

    subdir = 'LepLepGammaPlots'

    #-------------------------------------
    # make eta-pt dependent cuts
    #-------------------------------------

    eta_cuts = ['EB', 'EE']
    eta_labels = ['Barrel photon', 'Endcap photon']

    binning_mod = list( analysis_bins_mgg)
    binning_mod[-1] = 1000000

    for ec, lab in zip(eta_cuts, eta_labels) :

        #------------------------
        # pT inclusive
        #------------------------
        samplesLLG.Draw('ph_pt[ptSorted_ph_mediumNoEleVeto_idx[0]]', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumNoEleVeto_idx[0]] && m_leplep>60 )' %(baseline_cuts_mmg, ec), (40, 0, 200 ) , hist_config={'logy':1,  'xlabel':'photon p_{T} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Muon Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

        if save :
            name = 'ph_pt__mmg__%s__baselineCuts' %(ec)
            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
            samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        else :
            samplesLLG.DumpStack( )
            raw_input('continue')

        samplesLLG.Draw('m_leplep', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumNoEleVeto_idx[0]] )' %(baseline_cuts_mmg, ec), (40, 0, 200 ) , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 50000, 'xlabel':'M_{#mu#mu} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Muon Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

        if save :
            name = 'm_leplep__mmg__%s__baselineCuts' %(ec)
            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
            samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        else :
            samplesLLG.DumpStack( )
            raw_input('continue')

        samplesLLG.Draw('m_leplepph', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumNoEleVeto_idx[0]] && m_leplep>60 )' %(baseline_cuts_mmg, ec), (60, 0, 300 ) , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 50000,  'xlabel':'M_{#mu#mu#gamma} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Muon Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

        if save :
            name = 'm_leplepph__mmg__%s__baselineCuts' %(ec)
            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
            samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        else :
            samplesLLG.DumpStack( )
            raw_input('continue')

        #---------------------
        # Plots for photon eveto scale factor
        #---------------------
        for idx, ptmin in enumerate( eveto_bins[:-1] ) :
            ptmax = eveto_bins[idx+1]

            samplesLLG.Draw('m_leplepph', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumNoEleVeto_idx[0]] && ph_pt[ptSorted_ph_mediumNoEleVeto_idx[0]] > %d && ph_pt[ptSorted_ph_mediumNoEleVeto_idx[0]] < %d && m_leplep > 15 && m_leplep < 80 )' %(baseline_cuts_mmg, ec, ptmin, ptmax), (60, 0, 300 ) , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 50000,  'xlabel':'M_{#mu#mu#gamma} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Muon Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

            if save :
                name = 'm_leplepph__FSRmedium__mmg__%s__pt_%d-%d' %(ec, ptmin, ptmax)
                samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
                samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesLLG.DumpStack( )
                raw_input('continue')

            samplesLLG.Draw('m_leplepph', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumPassCSEV_idx[0]] && ph_pt[ptSorted_ph_mediumPassCSEV_idx[0]] > %d && ph_pt[ptSorted_ph_mediumPassCSEV_idx[0]] < %d && m_leplep > 15 && m_leplep < 80 )' %(baseline_cuts_mmg_psv, ec, ptmin, ptmax), (60, 0, 300 ) , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 50000,  'xlabel':'M_{#mu#mu#gamma} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Muon Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

            if save :
                name = 'm_leplepph__FSReveto__mmg__%s__pt_%s-%s' %(ec, ptmin, ptmax)
                samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
                samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesLLG.DumpStack( )
                raw_input('continue')

        samplesLLG.Draw('ph_pt[ptSorted_ph_mediumPassCSEV_idx[0]]', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumPassCSEV_idx[0]] && m_leplep>60)' %(baseline_cuts_eeg, ec), (40, 0, 200 ) , hist_config={'logy':1,  'xlabel':'photon p_{T} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Electron Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

        if save :
            name = 'ph_pt__eeg__%s__baselineCuts' %(ec)
            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
            samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        else :
            samplesLLG.DumpStack( )
            raw_input('continue')

        samplesLLG.Draw('m_leplep', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumPassCSEV_idx[0]] )' %(baseline_cuts_eeg, ec), (40, 0, 200 ) , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 50000,  'xlabel':'M_{e e} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Electron Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

        if save :
            name = 'm_leplep__eeg__%s__baselineCuts' %(ec)
            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
            samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        else :
            samplesLLG.DumpStack( )
            raw_input('continue')

        samplesLLG.Draw('m_leplepph', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumPassCSEV_idx[0]] && m_leplep>60)' %(baseline_cuts_eeg, ec), (60, 0, 300 ) , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 50000,  'xlabel':'M_{e e #gamma} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Electron Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

        if save :
            name = 'm_leplepph__eeg__%s__baselineCuts' %(ec)
            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
            samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        else :
            samplesLLG.DumpStack( )
            raw_input('continue')

        samplesLLG.Draw('ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumNoEleVeto_idx[0]] && m_leplep>60 && m_leplepph > 76 && m_leplepph < 106)' %(baseline_cuts_mmg, ec), [15,25,40,70,100] , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 50000,  'xlabel':'M_{#mu #mu #gamma} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Muon Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

        if save :
            name = 'ph_pt__mmg__%s__m_leplepphwindow__varBins' %(ec)
            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
            samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        else :
            samplesLLG.DumpStack( )
            raw_input('continue')

        samplesLLG.Draw('ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumPassCSEV_idx[0]] && m_leplep>60 && m_leplepph > 76 && m_leplepph < 106)' %(baseline_cuts_eeg, ec), [15,25,40,70,100] , hist_config={'logy':1,  'ymin' : 1, 'ymax' : 50000,  'xlabel':'M_{e e #gamma} [GeV]', 'doratio':1}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Electron Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

        if save :
            name = 'ph_pt__eeg__%s__m_leplepphwindow__varBins' %(ec)
            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
            samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
        else :
            samplesLLG.DumpStack( )
            raw_input('continue')

        for idx, min in enumerate(binning_mod[:-1]) :
            if min < 15 : 
                continue
            max = binning_mod[idx+1]

            samplesLLG.Draw('ph_pt[ptSorted_ph_mediumNoEleVeto_idx[0]]', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumNoEleVeto_idx[0]] && ph_pt[ptSorted_ph_mediumNoEleVeto_idx[0]]>%d && ph_pt[ptSorted_ph_mediumNoEleVeto_idx[0]]<%d  && m_leplep>60)' %(baseline_cuts_mmg, ec, min, max), (40, 0, 200 ) , hist_config={'logy':1,  'xlabel':'photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Muon Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

            if save :
                if idx+2 == len(binning_mod) :
                    name = 'ph_pt__mmg__baselineCuts__%s__ptbins_%d-max' %(ec, min)
                else :
                    name = 'ph_pt__mmg__baselineCuts__%s__ptbins_%d-%d' %(ec, min, max)
                samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
                samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesLLG.DumpStack( )
                raw_input('continue')

            samplesLLG.Draw('ph_pt[ptSorted_ph_mediumPassCSEV_idx[0]]', ' PUWeight * ( %s && ph_Is%s[ptSorted_ph_mediumPassCSEV_idx[0]] && ph_pt[ptSorted_ph_mediumPassCSEV_idx[0]]>%d && ph_pt[ptSorted_ph_mediumPassCSEV_idx[0]]<%d && m_leplep>60 )' %(baseline_cuts_eeg, ec, min, max), (40, 0, 200 ) , hist_config={'logy':1,  'xlabel':'photon p_{T} [GeV]'}, label_config={'labelStyle':'fancy', 'extra_label':'#splitline{Electron Channel}{%s}'%( lab), 'extra_label_loc':(0.3, 0.86)},   legend_config=samplesLLG.config_legend(legendCompress=1.2,legendWiden=1.2, ) )

            if save :
                if idx+2 == len(binning_mod) :
                    name = 'ph_pt__eeg__baselineCuts__%s__ptbins_%d-max' %(ec, min)
                else :
                    name = 'ph_pt__eeg__baselineCuts__%s__ptbins_%d-%d' %(ec, min, max)
                samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
                samplesLLG.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)
            else :
                samplesLLG.DumpStack( )
                raw_input('continue')


def MakePhotonJetFakePlots(save=False, detail=100 ) :

    subdir = 'JetFakeTemplatePlots'

    fsr_cut = 'leadPhot_sublLepDR > 0.4 && ( leadPhot_sublLepDR < 1.0 || leadPhot_leadLepDR < 1.0 ) '
    fsr_lab = 'Cut_leadPhot_sublLepDR_04_10'

    bins_eb = (10, 0, 0.03)
    bins_ee = (10, 0, 0.1)

    if not samplesLLG.collect_commands :
        samplesLLG.deactivate_sample('Data')
        samplesLLG.activate_sample('Muon')

    #------------------------------
    #------------------------------
    # signal template -- motivate event cuts
    #------------------------------
    #------------------------------
    samplesLLG.Draw('leadPhot_sublLepDR', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s ) ' %_photon_cuts_nopix_nosieie, (50, 0, 5), hist_config={'xlabel':'#Delta R(sublead #mu, #gamma)', 'ylabel':'Events / 0.1', 'labelStyle':'fancy'}, legend_config=samplesLLG.config_legend( legendWiden=1.3, legendCompress=1.3) )

    if save :
        name = 'leadPhot_sublLepDR__mmg'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')

    samplesLLG.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s )' %_photon_cuts_nopix_nosieie, (50, 0, 5), hist_config={'xlabel':'#Delta R(lead #mu, #gamma)', 'ylabel':'Events / 0.1'}, )

    if save :
        name = 'leadPhot_leadLepDR__mmg'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')

    #------------------------------
    # Make a cut to remove FSR photons
    #------------------------------


    samplesLLG.Draw('m_leplepph', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2  && %s && %s) ' %(_photon_cuts_nopix_nosieie, fsr_cut), (100, 0, 500), hist_config={'xlabel':'M_{#mu#mu#gamma} [GeV]', 'logy':1, 'ymin':1, 'ymax':1000000})

    if save :
        name = 'm_leplepph__mmg__%s'%fsr_lab
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    samplesLLG.Draw('m_leplepph+m_leplep', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s  && %s ) ' %(_photon_cuts_nopix_nosieie, fsr_cut), (100, 0, 500), hist_config={'xlabel':'M_{#mu#mu}+M_{#mu#mu#gamma} [GeV]', 'logy':1, 'ymin':1, 'ymax':1000000}  )

    if save :
        name = 'm_leplepph+m_leplep__mmg__%s'%fsr_lab
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    samplesLLG.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && ( m_leplepph+m_leplep ) < 185  ) ' %(_photon_cuts_nopix_nosieie, fsr_cut), (50, 0, 5), hist_config={'xlabel':'#Delta R(lead #mu, #gamma)', 'ylabel':'Events / 0.1'} )

    if save :
        name = 'leadPhot_leadLepDR__mmg__Cut_m_leplepph+m_leplep_185__%s'%fsr_lab
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')

    samplesLLG.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && fabs( m_leplepph-91.2 ) < 5  ) ' %(_photon_cuts_nopix_nosieie, fsr_cut), (50, 0, 5), hist_config={'xlabel':'#Delta R(lead #mu, #gamma)', 'ylabel':'Events / 0.1' })

    if save :
        name = 'leadPhot_leadLepDR__mmg__Cut_m_leplepph_10gevWindow__%s'%fsr_lab
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    #-------------------------
    # Add the leading fsr cut as well
    #-------------------------

    fsr_cut += ' && leadPhot_leadLepDR > 0.3'
    fsr_lab += '__Cut_leadPhot_leadLepDR_04'

    samplesLLG.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && fabs( m_leplepph-91.2 ) < 5 && ph_IsEB[0] )' %(_photon_cuts_nopix_nosieie, fsr_cut), ( 60, 0, 0.03), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0005', 'logy':1} )

    if save :
        name = 'ph_sigmaIEIE__mmg__EB__Cut_m_leplepph_10gevWindow__Cut_%s' %fsr_lab
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    samplesLLG.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && fabs( m_leplepph-91.2 ) < 5 && ph_IsEE[0] )' %(_photon_cuts_nopix_nosieie, fsr_cut), ( 50, 0, 0.1), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.002', 'logy':1}  )

    if save :
        name = 'ph_sigmaIEIE__mmg__EE__Cut_m_leplepph_10gevWindow__Cut_%s' %fsr_lab
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')

    samplesLLG.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && ( m_leplepph+m_leplep ) < 185 && ph_IsEB[0] )' %(_photon_cuts_nopix_nosieie, fsr_cut), ( 60, 0, 0.03), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0005', 'logy':1} )

    if save :
        name = 'ph_sigmaIEIE__mmg__EB__Cut_m_leplepph+m_leplep_185__Cut_%s' %fsr_lab
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    samplesLLG.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && ( m_leplepph+m_leplep ) < 185 && ph_IsEE[0] )' %(_photon_cuts_nopix_nosieie, fsr_cut), ( 50, 0, 0.1), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.002', 'logy':1 } )

    if save :
        name = 'ph_sigmaIEIE__mmg__EE__Cut_m_leplepph+m_leplep_185__Cut_%s' %fsr_lab
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')

    #---------------------------------------
    # We have two possible event cuts, look 
    # at how each cut affects sigmaIEIE
    #---------------------------------------

    samplesLLG.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && fabs( m_leplepph-91.2 ) < 5 && ph_IsEB[0] ) '%(_photon_cuts_nopix_nosieie, fsr_cut), 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && ( m_leplepph+m_leplep ) < 185 && ph_IsEB[0]  ) ' %(_photon_cuts_nopix_nosieie, fsr_cut)], ['Data']*2, (60, 0, 0.03), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0005', 'colors':[ROOT.kBlue, ROOT.kRed]}, legend_config={'legend_entries':[ '|M_{#mu#mu#gamma} - M_{Z}| < 5', 'M_{#mu#mu} + M_{#mu#mu#gamma} < 185 ']})

    if save :
        name = 'ph_sigmaIEIE__mmg__EB__CompMassCuts'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    samplesLLG.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && fabs( m_leplepph-91.2 ) < 5 && ph_IsEE[0] ) ' %(_photon_cuts_nopix_nosieie, fsr_cut), 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && %s && ( m_leplepph+m_leplep ) < 185 && ph_IsEE[0]  ) ' %(_photon_cuts_nopix_nosieie, fsr_cut)], ['Data']*2, (50, 0, 0.1), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.002', 'colors':[ROOT.kBlue, ROOT.kRed]}, legend_config={'legend_entries':[ '|M_{#mu#mu#gamma} - M_{Z}| < 5', 'M_{#mu#mu} + M_{#mu#mu#gamma} < 185 ']})

    if save :
        name = 'ph_sigmaIEIE__mmg__EE__CompMassCuts'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    print '*************************************FIX******************************'
    #samplesLLG.CompareSelections( 'ph_pt[%s[0]]'%(_photon_idx_nopix_nosieie), ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && fabs( m_leplepph-91.2 ) < 5 && leadPhot_leadLepDR>0.3 && leadPhot_sublLepDR > 0.3 && (leadPhot_leadLepDR < 1.0 || leadPhot_sublLepDR < 1.0 )  &&  %s)'%(_photon_cuts_nopix_nosieie)]*2 + ['PUWeight * (mu_passtrig25_n>0 && mu_n==2 && ph_truthMatch_ph[%s[0]] && abs(ph_truthMatchMotherPID_ph[%s[0]]) <25 && leadPhot_leadLepDR>0.4 && %s )' %(_photon_idx_nopix_nosieie, _photon_idx_nopix_nosieie, _photon_cuts_nopix_nosieie)], ['Data', 'Zgamma', 'Zgamma'], (50,0,200), hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], 'doratio':1, 'xlabel':'photon p_{T} [GeV]', 'ylabel':'Normalized Events', 'rlabel':'MC / Data', 'ymin':0.00001, 'ymax':5, 'logy':1, 'rmin':0.2, 'rmax':1.8}, legend_config={'legend_entries':['Data, FSR photons', 'Z#gamma, FSR photons', 'Z#gamma, truth matched photons'] }, label_config={'labelStyle' : 'fancy', } )
    ##samplesWg.CompareSelections( 'ph_pt[0]', ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && fabs( m_leplepph-91.2 ) < 5 && leadPhot_leadLepDR>0.3 && leadPhot_sublLepDR > 0.3 && (leadPhot_leadLepDR < 1.0 || leadPhot_sublLepDR < 1.0 ) &&  %s  )'%_photon_cuts_nopix_nosieie]*2 + ['PUWeight * ( %s && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25 )' %_photon_cuts_nopix_nosieie], ['Data', 'Zgamma', 'Wgamma'], (50, 0, 200 ), hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], 'doratio':1, 'xlabel':'photon p_{T} [GeV]', 'rlabel':'MC / Data', 'ymin':0.00001, 'ymax':5, 'logy':1, 'rmin':0.2, 'rmax':1.8}, legend_config=samplesWg.config_legend(legendWiden=1.5, legend_entries=['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'] ) )

    #if save :
    #    name = 'ph_pt__CompDataRealPhotonMCTruthMatchPhoton'
    #    #samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #    samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    #else :
    #    raw_input('continue')

    #------------------------------
    #------------------------------
    # background template -- motivate event cuts
    #------------------------------
    #------------------------------

    samplesLLG.Draw( 'leadPhot_sublLepDR', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplep-91.2 ) < 5 )'%_photon_cuts_nopix_nosieie, (50, 0, 5), hist_config={'xlabel':'#Delta R( #gamma, sublead lepton)'}, legend_config=samplesLLG.config_legend(legendWiden=1.5) )

    if save :
        name = 'leadPhot_sublLepDR__mmg__Cut_m_leplep_10GeVWindow'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')

    samplesLLG.Draw( 'leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplep-91.2 ) < 5 )'%_photon_cuts_nopix_nosieie, (50, 0, 5), hist_config={'xlabel':'#Delta R( #gamma, sublead lepton)'}, legend_config=samplesLLG.config_legend(legendWiden=1.5) )

    if save :
        name = 'leadPhot_leadLepDR__mmg__Cut_m_leplep_10GeVWindow'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    samplesLLG.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEB[0] )'%_photon_cuts_nopix_nosieie, (60, 0, 0.03), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0005'}, legend_config=samplesLLG.config_legend(legendWiden=1.5) )

    if save :
        name = 'ph_sigmaIEIE__EB__mmg__ZJetsCR'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    samplesLLG.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEE[0] )'%_photon_cuts_nopix_nosieie, (40, 0, 0.1), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0025'}, legend_config=samplesLLG.config_legend(legendWiden=1.5) )

    if save :
        name = 'ph_sigmaIEIE__EE__mmg__ZJetsCR'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')

    # Inv ChIso
    samplesLLG.Draw( 'ph_sigmaIEIE[ptSorted_ph_noSIEIEiso1077_idx[0]]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_noSIEIEiso1077_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEB[ptSorted_ph_noSIEIEiso1077_idx[0]] && ph_passNeuIsoCorrMedium[ptSorted_ph_noSIEIEiso1077_idx[0]] && ph_passPhoIsoCorrMedium[ptSorted_ph_noSIEIEiso1077_idx[0]] && ph_chIsoCorr[ptSorted_ph_noSIEIEiso1077_idx[0]] > 5 && ph_chIsoCorr[ptSorted_ph_noSIEIEiso1077_idx[0]] < 10 )', (60, 0, 0.03), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0005'}, legend_config=samplesLLG.config_legend(legendWiden=1.5) )

    if save :
        name = 'ph_sigmaIEIE__EB__mmg__chIso_5_10__ZJetsCR'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    samplesLLG.Draw( 'ph_sigmaIEIE[ptSorted_ph_noSIEIEiso1077_idx[0]]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_noSIEIEiso1077_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEE[ptSorted_ph_noSIEIEiso1077_idx[0]] && ph_passNeuIsoCorrMedium[ptSorted_ph_noSIEIEiso1077_idx[0]] && ph_passPhoIsoCorrMedium[ptSorted_ph_noSIEIEiso1077_idx[0]] && ph_chIsoCorr[ptSorted_ph_noSIEIEiso1077_idx[0]] > 5 && ph_chIsoCorr[ptSorted_ph_noSIEIEiso1077_idx[0]] < 10 )', (40, 0, 0.1), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0025'}, legend_config=samplesLLG.config_legend(legendWiden=1.5) )

    if save :
        name = 'ph_sigmaIEIE__EE__mmg__chIso_5_10__ZJetsCR'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')

    # Inv ChIso
    samplesLLG.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEB[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 )', (60, 0, 0.03), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0005'}, legend_config=samplesLLG.config_legend(legendWiden=1.5) )

    if save :
        name = 'ph_sigmaIEIE__EB__mmg__chIso_5_20__ZJetsCR'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    samplesLLG.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_IsEE[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 )', (40, 0, 0.1), hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0025'}, legend_config=samplesLLG.config_legend(legendWiden=1.5) )

    if save :
        name = 'ph_sigmaIEIE__EE__mmg__chIso_5_20__ZJetsCR'
        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
    else :
        raw_input('continue')


    binning = {'EB': (60, 0, 0.03), 'EE':  (40, 0, 0.1), 'EB__varBins' : [0, 0.011, 0.03], 'EE__varBins' : [0, 0.033, 0.1] }

    asym_isos = [(5,3,3), (8,5,5), (10,7,7), (12,9,9), (15,11,11), (20,16,16)]

    for reg in ['EB', 'EE']  :
        for iso in asym_isos :

            name = 'ph_pt__%s__mmg__iso%d-%d-%d__ZJetsCR' %(reg, iso[0], iso[1], iso[2])
            samplesLLG.CompareSelections( 'ph_pt[0]', ['PUWeight*(mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_sigmaIEIE[0]>0.011 && ph_Is%s[0] && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 )' %(reg), 'PUWeight * (mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_sigmaIEIE[0]>%f && ph_Is%s[0] && ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 )'%(binning[reg+'__varBins'][1], reg, iso[0], iso[1], iso[2])], ['DataRealPhotonSub']*2, (analysis_bins_mgg[-1]/5, 0, analysis_bins_mgg[-1], analysis_bins_mgg ) , hist_config={'doratio':2, 'colors':[ROOT.kBlack, ROOT.kRed], 'xlabel' : 'photon p_{T} [GeV]', 'ylabel' : 'Events / 5 GeV', 'logy' : 1, 'rmin' : 0, 'rmax' : 1.5, 'rlabel' : 'Nom / Loose'}, legend_config={'legend_entries' : ['Nominal iso', 'Loosened iso, %d-%d-%d'%(iso[0],iso[1],iso[2])]} )

            if save :
                samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                samplesLLG.DumpStack(options.outputDir+'/'+subdir, name )
            else :
                raw_input('continue')

    for reg in ['EB', 'EE'] :
        for bin_type in ['', '__varBins'] :

            for idx, min in enumerate( analysis_bins_mgg[:-2] ) :
                min1 = min
                max1 = analysis_bins_mgg[idx+1]
                min2 = analysis_bins_mgg[idx+1]
                max2 = analysis_bins_mgg[idx+2]

                leglab1 = '%d < p_{T} < %d' %( min1, max1 )
                leglab2 = '%d < p_{T} < %d' %( min2, max2 )

                ptlab = '__comp_pt_%d-%d-%d-%d' %( min1, max1, min2, max2)
                if max2 == analysis_bins_mgg[-1] :
                    max2=1000000
                    label2 = 'p_{T} > %d' %min2
                    ptlab = '__comp_pt_%d-%d-%d-max' %( min1, max1, min2 )

                if min1 < 15 :
                    continue

                    
                for iso in asym_isos :

                    name = 'ph_sigmaIEIE__%s__mmg__iso%d-%d-%d%s__ZJetsCR%s' %(reg, iso[0], iso[1], iso[2], ptlab, bin_type)

                    samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d )'%(iso[0], iso[1], iso[2], reg, min1, max1),'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d )'%(iso[0], iso[1], iso[2], reg, min2, max2)], ['DataRealPhotonSub']*2, binning[reg+bin_type], hist_config={'normalize':1, 'ymin' : 0.0, 'ymax' : 0.8, 'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0025', 'colors':[ROOT.kBlack,ROOT.kRed]}, legend_config=samplesLLG.config_legend(legendWiden=1.5, legend_entries=[leglab1, leglab2]) )

                    if save :
                        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                        samplesLLG.DumpStack(options.outputDir+'/'+subdir, name )

                    else :
                        raw_input('continue')

                #------------------------
                # Nominal - EB
                #------------------------
                name = 'ph_sigmaIEIE__%s__mmg%s__ZJetsCR%s' %(reg, ptlab, bin_type )
                samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d )'%(_photon_cuts_nopix_nosieie, reg, min1, max1),'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[0] && ph_pt[0]> %d && ph_pt[0] < %d)'%(_photon_cuts_nopix_nosieie, reg, min2, max2)], ['DataRealPhotonSub']*2, binning[reg+bin_type], hist_config={'normalize':1, 'ymin' : 0.0, 'ymax' : 0.5, 'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0005', 'colors':[ROOT.kBlack,ROOT.kRed]}, legend_config=samplesLLG.config_legend(legendWiden=1.5, legend_entries=[leglab1, leglab2]) )

                if save :
                    samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                    samplesLLG.DumpStack(options.outputDir+'/'+subdir, name )
                else :
                    raw_input('continue')

                #------------------------
                # ChIso window 5-10 
                #------------------------
                name = 'ph_sigmaIEIE__%s__mmg__chIso_5_10%s__ZJetsCR%s' %(reg, ptlab, bin_type )
                samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 && ph_pt[0] > %d && ph_pt[0] < %d )' %(reg,min1,max1),'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 && ph_pt[0] >  %d && ph_pt[0] < %d)'%(reg, min2, max2)], ['DataRealPhotonSub']*2, binning[reg+bin_type], hist_config={'normalize':1, 'ymin' : 0.0, 'ymax' : 0.5, 'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0005', 'colors':[ROOT.kBlack,ROOT.kRed]}, legend_config=samplesLLG.config_legend(legendWiden=1.5, legend_entries=[leglab1, leglab2]) )

                if save :
                    samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                    samplesLLG.DumpStack(options.outputDir+'/'+subdir, name )
                else :
                    raw_input('continue')

                #------------------------
                # ChIso window 5-20 
                #------------------------
                name = 'ph_sigmaIEIE__%s__mmg__chIso_5_20%s__ZJetsCR%s' %(reg, ptlab, bin_type)
                samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 && ph_pt[0] > %d && ph_pt[0] < %d )'%(reg, min1,max1),'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 && ph_pt[0] >  %d && ph_pt[0] < %d)' %(reg, min2,max2)], ['DataRealPhotonSub']*2, binning[reg+bin_type], hist_config={'normalize':1, 'ymin' : 0.0, 'ymax' : 0.5, 'xlabel':'#sigma i#etai#eta', 'ylabel':'Events / 0.0005', 'colors':[ROOT.kBlack,ROOT.kRed]}, legend_config=samplesLLG.config_legend(legendWiden=1.5, legend_entries=[leglab1, leglab2]) )

                if save :
                    samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                    samplesLLG.DumpStack(options.outputDir+'/'+subdir, name )
                else :
                    raw_input('continue')


def MakeJetFakeSystPlots(save=True ) :

    subdir = 'JetFakeTemplatePlots'
    bins_eb = (10, 0, 0.03)
    bins_ee = (10, 0, 0.1)

    fsr_cut = 'leadPhot_sublLepDR > 0.3 && ( leadPhot_sublLepDR < 1.0 || leadPhot_leadLepDR < 1.0 ) '
    #--------------------------------------
    #--------------------------------------
    # Study the effect of inverting an isolation variable on sigmaIEIE
    #--------------------------------------
    #--------------------------------------

    #--------------------------------------
    # Charged Iso
    #--------------------------------------
    draw_samples = ['Zgammastar', 'MuonRealPhotonSub']
    for samp in draw_samples :

            # NEED : ph_mediumNoSIEIENoNeuIso_n
            cutname = 'ph_chIsoCorr'
            common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
            samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 2 && %s[0] < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 5 && %s[0] < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 5 )' %( common_selection, cutname)], [samp]*6, bins_eb, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5']})
            if save :
                samplesLLG.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            else :
                raw_input('continue')
            
            common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
            samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 2 && %s[0] < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 5 && %s[0] < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 5 )' %( common_selection, cutname)], [samp]*6, bins_ee, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5']})
            if save :
                samplesLLG.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            else :
                raw_input('continue')
            
            #-------------------------------------------------
            # Not using SCRChIso
            #-------------------------------------------------
            #cutname = 'ph_SCRChIso'
            #common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
            #samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 2 && %s[0] < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 5 && %s[0] < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 5 )' %( common_selection, cutname)], [samp]*6, bins_eb, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5']})
            #if save :
            #    samplesLLG.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            #else :
            #    raw_input('continue')

            #common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
            #samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 2 && %s[0] < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 5 && %s[0] < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 5 )' %( common_selection, cutname)], [samp]*6, bins_ee, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5']})
            #if save :
            #    samplesLLG.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            #else :
            #    raw_input('continue')

            #--------------------------------------
            # Neutral Iso
            #--------------------------------------
            # NEED : ph_mediumNoSIEIENoNeuIso_n

            cutname = 'ph_neuIsoCorr'
            common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
            samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 1 && %s[0] < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 && %s[0] < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 )' %( common_selection, cutname)], [samp]*6, bins_eb, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1']})
            if save :
                samplesLLG.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            else :
                raw_input('continue')

            common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
            samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 1 && %s[0] < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 && %s[0] < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 )' %( common_selection, cutname)], [samp]*6, bins_ee, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1']})
            if save :
                samplesLLG.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            else :
                raw_input('continue')
            
            #-------------------------------------------------
            # Not using SCRNeuIso
            #-------------------------------------------------
            #cutname = 'ph_SCRNeuIso'
            #common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
            #samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 1 && %s[0] < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 && %s[0] < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 )' %( common_selection, cutname)], [samp]*6, bins_eb, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1']})
            #if save :
            #    samplesLLG.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            #else :
            #    raw_input('continue')

            #common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
            #samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 1 && %s[0] < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 && %s[0] < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 )' %( common_selection, cutname)], [samp]*6, bins_ee, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1']})
            #if save :
            #    samplesLLG.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            #else :
            #    raw_input('continue')

            #--------------------------------------
            # Photon Iso
            #--------------------------------------
            # NEED : ph_mediumNoSIEIENoPhoIso_n

            cutname = 'ph_phoIsoCorr'
            common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
            samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passPhoIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 1 && %s[0] < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 && %s[0] < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 )' %( common_selection, cutname)], [samp]*6, bins_eb, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1']})
            if save :
                samplesLLG.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            else :
                raw_input('continue')
            
            common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
            samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passPhoIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 1 && %s[0] < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 && %s[0] < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 )' %( common_selection, cutname)], [samp]*6, bins_ee, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1']}) 
            if save :
                samplesLLG.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            else :
                raw_input('continue')
            
            #-------------------------------------------------
            # Not using SCRPhoIso
            #-------------------------------------------------
            #cutname = 'ph_SCRPhoIso'
            #common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
            #samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 1 && %s[0] < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 && %s[0] < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 )' %( common_selection, cutname)], [samp]*6, bins_eb, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1']})
            #if save :
            #    samplesLLG.SaveStack('ph_sigmaIEIE__EB__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            #else :
            #    raw_input('continue')

            #common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
            #samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 1 && %s[0] < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 2 && %s[0] < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 && %s[0] < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s[0] > 2 )' %( common_selection, cutname)], [samp]*6, bins_ee, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':'Normalized Events / 0.002', 'rlabel':'Inverted Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.8}, legend_config={'legend_entries':['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1']})
            #if save :
            #    samplesLLG.SaveStack('ph_sigmaIEIE__EE__mmg__%s__Comp%scuts' %(samp, cutname), options.outputDir+'/'+subdir, 'base')
            #else :
            #    raw_input('continue')

            #--------------------------------------
            # Mult Iso
            #--------------------------------------

            binning = {'EB': (30, 0, 0.03), 'EE':  (20, 0, 0.1), 'EB__varBins' : [0, 0.011, 0.03], 'EE__varBins' : [0, 0.033, 0.1] }

            asym_isos = [(5,3,3), (8,5,5), (10,7,7), (12,9,9), (15,11,11), (20,16,16)]

            pt_bins = [(None, None)]
            for idx, min in enumerate( analysis_bins_mgg[:-1] ) :
                max = analysis_bins_mgg[idx+1]
                if min < 15 :
                    continue
                if max == analysis_bins_mgg[-1] :
                    pt_bins.append( (min, None) )
                    if min > analysis_bins_mgg[3] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[3], None) )
                    if min > analysis_bins_mgg[4] :
                        pt_bins.append( ( analysis_bins_mgg[4] , None ) )
                    if min > analysis_bins_mgg[5] :
                        pt_bins.append( (analysis_bins_mgg[5] , None ) )
                else :
                    pt_bins.append( (min, max) )
                    if min > analysis_bins_mgg[3] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[3], max) )
                    if min > analysis_bins_mgg[4] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[4], max) )
                    if min > analysis_bins_mgg[5] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[5], max) )


            for reg in ['EB', 'EE'] :
                for bin_type in ['', '__varBins'] :
                    for ptmin, ptmax in pt_bins :
                        pt_str = ''
                        pt_name = ''
                        if ptmin is not None :
                            pt_str = ' && ph_pt[0] > %d ' %ptmin
                            pt_name = '__pt_%d-max'%ptmin
                        if ptmax is not None :
                            pt_str += ' && ph_pt[0] < %d ' %ptmax
                            pt_name = '__pt_%d-%d'%(ptmin, ptmax)

                        ylab = 'Normalzied Events'
                        if isinstance( binning[reg+bin_type], tuple ) :
                            ylab = 'Normalized Events / %.4f ' %(binning[reg+bin_type][2]/binning[reg+bin_type][0])

                        common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_Is%s[0] %s'%(reg, pt_str)
                        samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', 
                                                    ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] )' %common_selection, 
                                                     'PUWeight * ( %s && ph_chIsoCorr[0] < 5  && ph_neuIsoCorr[0] < 3  && ph_phoIsoCorr[0] < 3  )' %( common_selection), 
                                                     'PUWeight * ( %s && ph_chIsoCorr[0] < 8  && ph_neuIsoCorr[0] < 5  && ph_phoIsoCorr[0] < 5  )' %( common_selection), 
                                                     'PUWeight * ( %s && ph_chIsoCorr[0] < 10 && ph_neuIsoCorr[0] < 7  && ph_phoIsoCorr[0] < 7  )' %( common_selection),
                                                     'PUWeight * ( %s && ph_chIsoCorr[0] < 12 && ph_neuIsoCorr[0] < 9  && ph_phoIsoCorr[0] < 9  )' %( common_selection), 
                                                     'PUWeight * ( %s && ph_chIsoCorr[0] < 15 && ph_neuIsoCorr[0] < 11 && ph_phoIsoCorr[0] < 11 )' %( common_selection),
                                                     'PUWeight * ( %s && ph_chIsoCorr[0] < 20 && ph_neuIsoCorr[0] < 16 && ph_phoIsoCorr[0] < 16 )' %( common_selection)
                                                    ], 
                                     [samp]*7, binning[reg+bin_type], hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta, ROOT.kYellow-2] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':ylab, 'rlabel':'Loose Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.5}, legend_config={'legend_entries':['Nominal Iso cuts', '5,3,3 (ch,neu,pho)', '8,5,5 (ch,neu,pho)', '10,7,7 (ch,neu,pho)', '12,9,9 (ch,neu,pho)', '15,11,11(ch,neu,pho)', '20,16,16 (ch,neu,pho)' ]})
                        if save :
                            name = 'ph_sigmaIEIE__%s__mmg__%s%s__CompLoosenedIsoCuts%s' %(reg,samp,pt_name, bin_type)
                            samplesLLG.SaveStack(name, options.outputDir+'/'+subdir, 'base')
                            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
                        else :
                            raw_input('continue')
           
    var_bins_ee = [0, 0.033, 0.1] 
    var_bins_eb = [0, 0.011, 0.03] 
    binning = {'EB': (30, 0, 0.03), 'EE':  (20, 0, 0.1), 'EB__varBins' : [0, 0.011, 0.03], 'EE__varBins' : [0, 0.033, 0.1] }

    pt_bins = [(None, None)]
    for idx, ptmin in enumerate(analysis_bins_mgg[:-1]) :
        if ptmin < 15 :
            continue
        ptmax = analysis_bins_mgg[idx+1]
        if ptmax == analysis_bins_mgg[-1] :
            pt_bins.append( (ptmin, None ) )
            if ptmin > analysis_bins_mgg[3] : # for sublead photon pt range
                pt_bins.append( ( analysis_bins_mgg[3], None ) )
            if ptmin > analysis_bins_mgg[4] : # for sublead photon pt range
                pt_bins.append( ( analysis_bins_mgg[4], None ) )
            if ptmin > analysis_bins_mgg[5] : # for sublead photon pt range
                pt_bins.append( ( analysis_bins_mgg[5], None ) )
        else :
            pt_bins.append( (ptmin, ptmax ) )
            if ptmin > analysis_bins_mgg[3] : # for sublead photon pt range
                pt_bins.append( ( analysis_bins_mgg[3], ptmax ) )
            if ptmin > analysis_bins_mgg[4] : # for sublead photon pt range
                pt_bins.append( ( analysis_bins_mgg[4], ptmax ) )
            if ptmin > analysis_bins_mgg[5] : # for sublead photon pt range
                pt_bins.append( (analysis_bins_mgg[5] , ptmax ) )

    draw_samples = ['Zgammastar', 'MuonRealPhotonSub']
    for samp in draw_samples :
        for reg in ['EB', 'EE'] :
            for bin_type in ['', '__varBins'] :
                for ptmin, ptmax in pt_bins :

                    pt_draw = ''
                    pt_name = ''
                    if ptmin is not None :
                        pt_draw += ' && ph_pt[0] > %d ' %ptmin
                        pt_name = '__pt_%d-max' %ptmin
                    if ptmax is not None :
                        pt_draw += ' && ph_pt[0] < %d ' %ptmax
                        pt_name = '__pt_%d-%s' %(ptmin, ptmax)


                    ylab = 'Normalzied Events'
                    if isinstance( binning[reg+bin_type], tuple ) :
                        ylab = 'Normalized Events / %.4f ' %(binning[reg+bin_type][2]/binning[reg+bin_type][0])

                    cutname = 'ph_chIsoCorr'
                    common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_Is%s[0] %s' %(reg,pt_draw)
                    samplesLLG.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > 2 && %s[0] < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s[0] > 5 && %s[0] < 20 )' %( common_selection, cutname, cutname)], [samp]*4, binning[reg+bin_type], hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange] ,'doratio':2, 'xlabel':'#sigma i#eta i#eta', 'ylabel':ylab}, legend_config={'legend_entries':['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20']})
                    if save :
                        name = 'ph_sigmaIEIE__%s__mmg__%s__Comp%scuts%s%s' %(reg,samp, cutname, pt_name, bin_type)
                        samplesLLG.SaveStack(name , options.outputDir+'/'+subdir, 'base')
                        samplesLLG.DumpStack(options.outputDir+'/'+subdir, name )
                    else :
                        raw_input('continue')
            
                    sieie_cut_nom = {'EB': 0.011, 'EE' : 0.033 }
                    sieie_cut_max1 = {'EB': 0.014, 'EE' : 0.04 }
                    sieie_cut_max2 = {'EB': 0.017, 'EE' : 0.05 }
                    for var in ['ph_chIsoCorr', 'ph_neuIsoCorr', 'ph_phoIsoCorr'] :
                        cutname = 'ph_sigmaIEIE'
                        common_selection = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_Is%s[0] %s' %(reg,pt_draw)
                        samplesLLG.CompareSelections( '%s[0]'%var, ['PUWeight * ( %s && ph_passSIEIEMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s[0] > %f && %s[0] < %f )' %( common_selection, cutname, sieie_cut_nom[reg], cutname, sieie_cut_max1[reg]), 'PUWeight * ( %s && %s[0] > %d && %s[0] < %s )' %( common_selection, cutname, sieie_cut_nom[reg], cutname, sieie_cut_max2[reg]), 'PUWeight * ( %s && %s[0] > %f )' %( common_selection, cutname, sieie_cut_nom[reg])], [samp]*4, binning[reg+bin_type], hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange] ,'doratio':2, 'xlabel':var, 'ylabel':ylab}, legend_config={'legend_entries':['Nominal #sigma i#etai#eta cut', ' %.3f < #sigma i#etai#eta < %.3f' %( sieie_cut_nom[reg], sieie_cut_max1[reg] ), ' %.3f < #sigma i#etai#eta < %.3f'%( sieie_cut_nom[reg], sieie_cut_max2[reg] ), '#sigma i#etai#eta > %0.3f '%( sieie_cut_nom[reg] )]})
                        if save :
                            name = '%s__%s__mmg__%s__Comp%scuts%s%s' %(var, reg,samp, cutname, pt_name, bin_type)
                            samplesLLG.SaveStack(name , options.outputDir+'/'+subdir, 'base')
                            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name )
                        else :
                            raw_input('continue')
            

    # ---------------------------------
    # Make ZCR fake template plots
    # ---------------------------------

    vars = ['sigmaIEIE', 'chIsoCorr', 'neuIsoCorr', 'phoIsoCorr']
    regions = ['EB', 'EE']
    asym_isos = { 'sigmaIEIE'  : [('5','3','3'), ('8','5','5'), ('10','7','7'), ('12','9','9'), ('15','11','11'), ('20','16','16')],
                  'chIsoCorr'  : [('NoSIEIE','3','3'),('None','3','3'), ('None','5','5'), ('None','7','7'), ('None','9','9'), ('None','11','11'), ('None','16','16')   ],
                  'neuIsoCorr' : [('5','NoSIEIE','3'),('5','None','3'), ('8','None','5'), ('10','None','7'), ('12','None','9'), ('15','None','11'), ('20','None','16')],
                  'phoIsoCorr' : [('5','3','NoSIEIE'),('5','3','None'), ('8','5','None'), ('10','7','None'), ('12','9','None'), ('15','11','None'), ('20','16','None')],
                }
    binning = { 'sigmaIEIE'  : { 'EB' : (30, 0, 0.03), 'EE' : (200, 0, 0.1), 'EB__varBins' : [0, 0.011, 0.03], 'EE__varBins' : [0, 0.033, 0.1] },
                'chIsoCorr'  : { 'EB' : (30, 0, 45)  , 'EE' : (35, 0, 42)  , 'EB__varBins' : [0, 1.5, 5.0]   , 'EE__varBins' : [0, 1.2, 5.0] },
                'neuIsoCorr' : { 'EB' : (40, -2, 38) , 'EE' : (30, -2, 43) , 'EB__varBins' : [-2, 1.0, 5.0]   , 'EE__varBins' : [-2, 1.5, 5.0] },
                'phoIsoCorr' : { 'EB' : (53, -2.1, 35)  , 'EE' : (42, -2, 40)  , 'EB__varBins' : [-2.1, 0.7, 35.0]   , 'EE__varBins' : [-2, 1.0, 5.0] }
              }
    ylabels = { 'sigmaIEIE' :  { 'EB' : 'Events/0.0005', 'EE' : 'Events /0.0025' },
                'chIsoCorr' :  { 'EB' : 'Events/1.5', 'EE' : 'Events/1.2' },
                'neuIsoCorr' : { 'EB' : 'Events/1.0', 'EE' : 'Events/1.5' },
                'phoIsoCorr' : { 'EB' : 'Events/0.7', 'EE' : 'Events/1.0' }
              }

    reglabels = { 'EB' : 'Barrel Photons' , 'EE' : 'Endcap Photons' }

    xlabels = { 'sigmaIEIE'  : '#sigma i#etai#eta', 
                'chIsoCorr'  : 'Charged Hadron Isolation', 
                'neuIsoCorr' : 'Neutral Hadron Isolation', 
                'phoIsoCorr' : 'Neutral EM Isolation' }
    base_colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta, ROOT.kYellow-2]
    for var in vars :
        for reg in regions :
    
            pt_bins = []
            for idx, min in enumerate( analysis_bins_mgg[:-1] ) :
                max = analysis_bins_mgg[idx+1]
                if min < 15 : 
                    continue

                if max == analysis_bins_mgg[-1] :
                    pt_bins.append( (min, None) )
                    if min > analysis_bins_mgg[3] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[3] , None) )
                    if min > analysis_bins_mgg[4] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[4], None) )
                    if min > analysis_bins_mgg[5] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[5], None) )
                else :
                    pt_bins.append( (min, max) )
                    if min > analysis_bins_mgg[3] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[3], max) )
                    if min > analysis_bins_mgg[4] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[4], max) )
                    if min > analysis_bins_mgg[5] : # for sublead photon pt range
                        pt_bins.append( (analysis_bins_mgg[5], max) )

                
            for ptmin, ptmax in pt_bins :

                if ptmin < 15 :
                    continue


                # to get the full set of cuts for when
                # no variables are loosned
                cuts_full = None
                phvar = None    
                if var == 'sigmaIEIE' :
                    cuts_full = _photon_cuts_nopix_nosieie
                    phvar = 'ptSorted_ph_mediumNoSIEIENoEleVeto_idx[0]'
                if var == 'chIsoCorr' :
                    cuts_full = _photon_cuts_nopix_nochiso
                    phvar = 'ptSorted_ph_mediumNoChIsoNoEleVeto_idx[0]'
                if var == 'neuIsoCorr' :
                    cuts_full = _photon_cuts_nopix_noneuiso
                    phvar = 'ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx[0]'
                if var == 'phoIsoCorr' :
                    cuts_full = _photon_cuts_nopix_nophoiso
                    phvar = 'ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx[0]'

                pt_str  = ''
                pt_str_def  = ''
                pt_name = ''
                pt_lab  = ''
                if ptmin is not None :
                    pt_str = ' ph_pt[%s] > %d ' %(phvar,ptmin)
                    pt_str_def = ' ph_pt[0] > %d ' %(ptmin)
                    pt_name = '__pt_%d-max'%ptmin
                    pt_lab = ' p_{T} > %d ' %ptmin
                if ptmax is not None :
                    pt_str = ' ph_pt[%s] > %d && ph_pt[%s] < %d  ' %(phvar,ptmin,phvar,ptmax)
                    pt_str_def = ' ph_pt[0] > %d && ph_pt[0] < %d  ' %(ptmin,ptmax)
                    pt_name = '__pt_%d-%d'%(ptmin, ptmax)
                    pt_lab = ' %d < p_{T} < %d ' %(ptmin,ptmax)

                for bin_type in ['', '__varBins'] :
                    
                    #-----------------------------
                    # Fake photon template plots
                    # nominal cuts
                    #-----------------------------

                    name = 'ph_%s__%s__mmg%s__ZJetsCR%s' %(var, reg, pt_name, bin_type)

                    samplesLLG.Draw( 'ph_%s[%s]'%(var,phvar), 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[%s] && %s)'%(cuts_full, reg, phvar, pt_str) , binning[var][reg+bin_type], hist_config={'xlabel':xlabels[var], 'ylabel':ylabels[var][reg]}, legend_config=samplesLLG.config_legend(legendWiden=1.5), label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{%s}{%s}' %(reglabels[reg],pt_lab), 'extra_label_loc':(0.2, 0.86)} )

                    if save :
                        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                    else :
                        raw_input('continue')

                    #-----------------------------
                    # Real photon template plots
                    # nominal cuts
                    # Must use Wg samples because
                    # comparison is done with Wgamma sample
                    #-----------------------------

                    print '************************************FIX***************************'
                    #samplesWg.CompareSelections( 'ph_%s[%s]'%(var,phvar), ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplepph-91.2 ) < 5  && %s && ph_Is%s[%s] && %s)'%(cuts_full, fsr_cut, reg, phvar, pt_str)]*2 + ['PUWeight * (mu_passtrig25_n>0 && mu_n==1 && %s && ph_truthMatch_ph[%s] && abs(ph_truthMatchMotherPID_ph[%s]) <25 && ph_Is%s[%s] && leadPhot_leadLepDR>0.4 && %s )' %(cuts_full, phvar, phvar, reg, phvar, pt_str)], ['Data', 'Zgamma', 'Wgamma'], binning[var][reg+bin_type], hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], 'doratio':1, 'xlabel':xlabels[var], 'ylabel':'Normalized Events', 'rlabel':'MC / Data', 'ymin':0.00001, 'ymax':5, 'logy':1, 'rmin':0.2, 'rmax':1.8}, legend_config={'legend_entries':['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'] }, label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{%s}{%s}' %(reglabels[reg],pt_lab), 'extra_label_loc':(0.2, 0.86)} )
                    # for comparing to Zg
                    samplesLLG.CompareSelections( 'ph_%s[%s]'%(var,phvar), ['PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplepph-91.2 ) < 5  && %s && ph_Is%s[%s] && %s)'%(cuts_full, fsr_cut, reg, phvar, pt_str)]*2 + ['PUWeight * (mu_passtrig25_n>0 && mu_n==2 && %s && ph_truthMatch_ph[%s] && abs(ph_truthMatchMotherPID_ph[%s]) <25 && ph_Is%s[%s] && leadPhot_leadLepDR>0.4 && %s )' %(cuts_full, phvar, phvar, reg, phvar, pt_str)], ['Data', 'Zgamma', 'Zgamma'], binning[var][reg+bin_type], hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], 'doratio':1, 'xlabel':xlabels[var], 'ylabel':'Normalized Events', 'rlabel':'MC / Data', 'ymin':0.00001, 'ymax':5, 'logy':1, 'rmin':0.2, 'rmax':1.8}, legend_config={'legend_entries':['Data, FSR photons', 'Z#gamma, FSR photons', 'Z#gamma, truth matched photons'] }, label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{%s}{%s}' %(reglabels[reg],pt_lab), 'extra_label_loc':(0.2, 0.86)} )

                    if save :
                        name = 'ph_%s__%s%s__CompDataRealPhotonMCTruthMatchPhoton%s'%(var, reg,pt_name, bin_type)
                        #samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                        #samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                        samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                        samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
                    else :
                        raw_input('continue')

                    if var =='sigmaIEIE' :
                        #-----------------------------
                        # Fake photon template plots
                        # with loosened chHadIso
                        # Not used in the analysis, kept for reference
                        #-----------------------------
                        name = 'ph_sigmaIEIE__%s__mmg%s__chIso_5_10__ZJetsCR%s' %(reg, pt_name, bin_type)
                        samplesLLG.Draw( 'ph_sigmaIEIE[ptSorted_ph_noSIEIEiso1077_idx[0]]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_noSIEIEiso1077_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[ptSorted_ph_noSIEIEiso1077_idx[0]] && %s && ph_passNeuIsoCorrMedium[ptSorted_ph_noSIEIEiso1077_idx[0]] && ph_passPhoIsoCorrMedium[ptSorted_ph_noSIEIEiso1077_idx[0]] && ph_chIsoCorr[ptSorted_ph_noSIEIEiso1077_idx[0]] > 5 && ph_chIsoCorr[ptSorted_ph_noSIEIEiso1077_idx[0]] < 10)'%(reg, pt_str_def) , binning[var][reg+bin_type], hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':ylabels[var][reg]}, legend_config=samplesLLG.config_legend(legendWiden=1.5), label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{#splitline{%s}{5 < chIso < 10}}{%s}' %(reglabels[reg], pt_lab), 'extra_label_loc':(0.2, 0.75) } )

                        if save :
                            samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                        else :
                            raw_input('continue')


                        name = 'ph_sigmaIEIE__%s__mmg%s__chIso_5_20__ZJetsCR%s' %(reg, pt_name, bin_type)
                        samplesLLG.Draw( 'ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[0] && %s && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20)'%(reg, pt_str_def) , binning[var][reg+bin_type], hist_config={'xlabel':'#sigma i#etai#eta', 'ylabel':ylabels[var][reg]}, legend_config=samplesLLG.config_legend(legendWiden=1.5), label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{#splitline{%s}{5 < chIso < 20}}{%s}' %(reglabels[reg], pt_lab), 'extra_label_loc':(0.2, 0.75)}  )

                        if save :
                            samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                        else :
                            raw_input('continue')


                    draw_samples = ['Zgammastar', 'MuonRealPhotonSub']
                    for samp in draw_samples :
                        #-----------------------------
                        # Comparison of loosened isolation
                        # on ID/iso vars
                        #-----------------------------
                        name = 'ph_%s__%s__mmg__%s%s__CompLoosenedIsoCuts%s' %(var,reg,samp,pt_name, bin_type)
                        common_selection = 'mu_passtrig25_n>0 && mu_n==2 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_Is%s[0] && %s'%(reg, pt_str)
                        iso_cut_strs = ['PUWeight * ( %s && %s)' %(cuts_full, common_selection)]
                        iso_lab_strs = ['Nominal Iso cuts']

                        for iso in asym_isos[var] :

                            if var == 'sigmaIEIE' :
                                iso_cut = 'ph_noSIEIEiso%s%s%s_n==1' %( iso[0], iso[1], iso[2] )
                                phvar = 'ptSorted_ph_noSIEIEiso%s%s%s_idx[0]' %( iso[0], iso[1], iso[2] )
                            else :
                                if 'NoSIEIE' in iso :
                                    if var == 'chIsoCorr' :
                                        iso_cut = 'ph_mediumNoSIEIENoChIso_n==1 '
                                        phvar = 'ptSorted_ph_mediumNoSIEIENoChIso_idx[0] ' 
                                    if var == 'neuIsoCorr' :
                                        iso_cut = 'ph_mediumNoSIEIENoNeuIso_n==1 '
                                        phvar = 'ptSorted_ph_mediumNoSIEIENoNeuIso_idx[0] ' 
                                    if var == 'phoIsoCorr' :
                                        iso_cut = 'ph_mediumNoSIEIENoPhoIso_n==1 '
                                        phvar = 'ptSorted_ph_mediumNoSIEIENoPhoIso_idx[0] ' 
                                else :
                                    iso_cut = 'ph_passSIEIEiso%s%s%s_n==1' %( iso[0], iso[1], iso[2] )
                                    phvar = 'ptSorted_ph_passSIEIEiso%s%s%s_idx[0]' %( iso[0], iso[1], iso[2] )

                            pt_str  = ''
                            pt_str_def  = ''
                            pt_name = ''
                            pt_lab  = ''
                            if ptmin is not None :
                                pt_str = ' ph_pt[%s] > %d ' %(phvar,ptmin)
                                pt_str_def = ' ph_pt[0] > %d ' %(ptmin)
                                pt_name = '__pt_%d-max'%ptmin
                                pt_lab = ' p_{T} > %d ' %ptmin
                            if ptmax is not None :
                                pt_str = ' ph_pt[%s] > %d && ph_pt[%s] < %d  ' %(phvar,ptmin,phvar,ptmax)
                                pt_str_def = ' ph_pt[0] > %d && ph_pt[0] < %d  ' %(ptmin,ptmax)
                                pt_name = '__pt_%d-%d'%(ptmin, ptmax)
                                pt_lab = ' %d < p_{T} < %d ' %(ptmin,ptmax)

                            common_selection = 'mu_passtrig25_n>0 && mu_n==2 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_Is%s[%s] && %s'%(reg, phvar, pt_str)

                            iso_cut_strs.append( 'PUWeight * ( %s && %s )' %(iso_cut, common_selection) )
                            isostr0 = str( iso[0] )
                            isostr1 = str( iso[1] )
                            isostr2 = str( iso[2] )
                            if iso[0] == 'None' : 
                                isostr0 = 'No Cut'
                            if iso[1] == 'None' : 
                                isostr1 = 'No Cut'
                            if iso[2] == 'None'  : 
                                isostr2 = 'No Cut'
                            iso_lab = '%s,%s,%s (ch,neu,pho)' %( isostr0, isostr1, isostr2)
                            if 'NoSIEIE' in iso :
                                iso_lab = 'No SIEIE'
                            iso_lab_strs.append( iso_lab )

                        n_plots = len( asym_isos[var]) + 1
                        colors = list(base_colors)

                        if len( colors ) < n_plots :
                            colors.append(ROOT.kGray)

                        samplesLLG.CompareSelections( 'ph_%s[0]' %(var ), iso_cut_strs, 
                                     [samp]*(n_plots), binning[var][reg+bin_type], hist_config={'normalize':1, 'colors':colors ,'doratio':2, 'xlabel':xlabels[var], 'ylabel':ylabels[var][reg], 'rlabel':'Loose Cut / Nominal cut', 'rmin':0.6, 'rmax':1.4, 'ymin':0, 'ymax':0.5}, legend_config={'legend_entries':iso_lab_strs})
                        if save :
                            samplesLLG.SaveStack(name, options.outputDir+'/'+subdir, 'base')
                            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
                        else :
                            raw_input('continue')
            
                    for iso in asym_isos[var] :

                        isostr0 = str( iso[0] )
                        isostr1 = str( iso[1] )
                        isostr2 = str( iso[2] )
                        if iso[0] == 'None' : 
                            isostr0 = 'No Cut'
                        if iso[1] == 'None' : 
                            isostr1 = 'No Cut'
                        if iso[2] == 'None' : 
                            isostr2 = 'No Cut'
                        iso_lab = 'Loose Iso (%s,%s,%s) ' %(isostr0, isostr1, isostr2)
                        if 'NoSIEIE' in iso :
                            iso_lab = 'No SIEIE'
                    
                        if var == 'sigmaIEIE' :
                            iso_cut = 'ph_noSIEIEiso%s%s%s_n==1' %( iso[0], iso[1], iso[2] )
                            phvar = 'ptSorted_ph_noSIEIEiso%s%s%s_idx[0]' %( iso[0], iso[1], iso[2] )
                        else :
                            if 'NoSIEIE' in iso :
                                if var == 'chIsoCorr' :
                                    iso_cut = 'ph_mediumNoSIEIENoChIso_n==1 '
                                    phvar = 'ptSorted_ph_mediumNoSIEIENoChIso_idx[0] ' 
                                if var == 'neuIsoCorr' :
                                    iso_cut = 'ph_mediumNoSIEIENoNeuIso_n==1 '
                                    phvar = 'ptSorted_ph_mediumNoSIEIENoNeuIso_idx[0] ' 
                                if var == 'phoIsoCorr' :
                                    iso_cut = 'ph_mediumNoSIEIENoPhoIso_n==1 '
                                    phvar = 'ptSorted_ph_mediumNoSIEIENoPhoIso_idx[0] ' 
                            else :
                                iso_cut = 'ph_passSIEIEiso%s%s%s_n==1' %( iso[0], iso[1], iso[2] )
                                phvar = 'ptSorted_ph_passSIEIEiso%s%s%s_idx[0]' %( iso[0], iso[1], iso[2] )

                        pt_str  = ''
                        pt_str_def  = ''
                        pt_name = ''
                        pt_lab  = ''
                        if ptmin is not None :
                            pt_str = ' ph_pt[%s] > %d ' %(phvar,ptmin)
                            pt_str_def = ' ph_pt[0] > %d ' %(ptmin)
                            pt_name = '__pt_%d-max'%ptmin
                            pt_lab = ' p_{T} > %d ' %ptmin
                        if ptmax is not None :
                            pt_str = ' ph_pt[%s] > %d && ph_pt[%s] < %d  ' %(phvar,ptmin,phvar,ptmax)
                            pt_str_def = ' ph_pt[0] > %d && ph_pt[0] < %d  ' %(ptmin,ptmax)
                            pt_name = '__pt_%d-%d'%(ptmin, ptmax)
                            pt_lab = ' %d < p_{T} < %d ' %(ptmin,ptmax)
                        #-----------------------------
                        # Fake photon template selections
                        # all vars, pt
                        #-----------------------------
                        name = 'ph_%s__%s__mmg%s__iso%s-%s-%s__ZJetsCR%s' %(var, reg, pt_name , iso[0], iso[1], iso[2], bin_type)
                        samplesLLG.Draw( 'ph_%s[%s]'%(var,phvar), 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR>1.0 && leadPhot_leadLepDR>1.0 && ph_Is%s[%s] && %s )'%(iso_cut, reg, phvar, pt_str) , binning[var][reg+bin_type], hist_config={'xlabel':xlabels[var], 'ylabel':ylabels[var][reg]}, legend_config=samplesLLG.config_legend(legendWiden=1.5), label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{#splitline{%s}{%s}}{%s}' %(reglabels[reg], iso_lab, pt_lab), 'extra_label_loc':(0.2, 0.75) } )

                        if save :
                            samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
                        else :
                            raw_input('continue')

                        #-----------------------------
                        # Real photon template selections
                        # all vars, pt
                        #-----------------------------
                        print '***************************FIX*******************************'
                        name = 'ph_%s__%s__iso%s-%s-%s%s__CompDataRealPhotonMCTruthMatchPhoton%s'%(var,reg,iso[0], iso[1], iso[2],pt_name, bin_type)
                        #samplesWg.CompareSelections( 'ph_%s[%s]'%(var,phvar), 
                        #                            ['PUWeight * (mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplepph-91.2 ) < 5  && %s && ph_Is%s[%s] && %s )'%(iso_cut, fsr_cut, reg, phvar, pt_str)]*2 
                        #                          + ['PUWeight * (mu_passtrig25_n>0 && mu_n==1 && %s && ph_truthMatch_ph[%s] && abs(ph_truthMatchMotherPID_ph[%s]) <25 && ph_Is%s[%s] && leadPhot_leadLepDR>0.4 && %s )' %(iso_cut, phvar, phvar, reg, phvar, pt_str)], 
                        #                            ['Data', 'Zgamma', 'Wgamma'], binning[var][reg+bin_type], hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], 'doratio':1, 'xlabel':xlabels[var], 'ylabel':'Normalized Events', 'rlabel':'MC / Data', 'ymin':0.00001, 'ymax':5, 'logy':1, 'rmin':0.2, 'rmax':1.8}, legend_config={'legend_entries':['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'] }, label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{#splitline{%s}{%s}}{%s}' %(reglabels[reg], iso_lab, pt_lab), 'extra_label_loc':(0.2, 0.75) } )
                        # for comparing to zg
                        samplesLLG.CompareSelections( 'ph_%s[%s]'%(var,phvar), 
                                                    ['PUWeight * (mu_passtrig25_n>0 && mu_n==2 && %s && fabs( m_leplepph-91.2 ) < 5  && %s && ph_Is%s[%s] && %s )'%(iso_cut, fsr_cut, reg, phvar, pt_str)]*2 
                                                  + ['PUWeight * (mu_passtrig25_n>0 && mu_n==2 && %s && ph_truthMatch_ph[%s] && abs(ph_truthMatchMotherPID_ph[%s]) <25 && ph_Is%s[%s] && leadPhot_leadLepDR>0.4 && %s )' %(iso_cut, phvar, phvar, reg, phvar, pt_str)], 
                                                    ['Data', 'Zgamma', 'Zgamma'], binning[var][reg+bin_type], hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], 'doratio':1, 'xlabel':xlabels[var], 'ylabel':'Normalized Events', 'rlabel':'MC / Data', 'ymin':0.00001, 'ymax':5, 'logy':1, 'rmin':0.2, 'rmax':1.8}, legend_config={'legend_entries':['Data, FSR photons', 'Z#gamma, FSR photons', 'Z#gamma, truth matched photons'] }, label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{#splitline{%s}{%s}}{%s}' %(reglabels[reg], iso_lab, pt_lab), 'extra_label_loc':(0.2, 0.75) } )
        
                        if save :
                            #samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                            #samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
                            samplesLLG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                            samplesLLG.DumpStack(options.outputDir+'/'+subdir, name)
                        else :
                            raw_input('continue')
        
    #-----------------------------------
    #-----------------------------------
    # Look at diphotons using loosened iso
    #-----------------------------------
    #-----------------------------------

    photon_cuts_looseiso = 'mu_passtrig25_n>0 && mu_n==1 && ph_noSIEIEiso533_n==2 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && dr_ph1_ph2 >0.3 && m_ph1_ph2 > %d ' %(m_ph1_ph2_cut )

    samplesWg.Draw( 'sieie_leadph12', 'PUWeight * ( %s && isEB_leadph12 && isEB_sublph12 )' %photon_cuts_looseiso, (60, 0, 0.03), hist_config={'xlabel' : 'Lead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0005'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_lead__mgg__EB_EB__loosenedIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')

    samplesWg.Draw( 'sieie_sublph12', 'PUWeight * ( %s && isEB_leadph12 && isEB_sublph12 )' %photon_cuts_looseiso, (60, 0, 0.03), hist_config={'xlabel' : 'Sublead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0005'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)})
                
    if save :
        name = 'ph_sigmaIEIE_subl__mgg__EB_EB__loosenedIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')


    samplesWg.Draw( 'sieie_leadph12', 'PUWeight * ( %s && isEB_leadph12 && isEE_sublph12 )' %photon_cuts_looseiso, (60, 0, 0.03), hist_config={'xlabel' : 'Lead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0005'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_lead__mgg__EB_EE__loosenedIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')

    samplesWg.Draw( 'sieie_sublph12', 'PUWeight * ( %s && isEB_leadph12 && isEE_sublph12 )' %photon_cuts_looseiso, (40, 0, 0.1), hist_config={'xlabel' : 'Sublead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0025'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_subl__mgg__EB_EE__loosenedIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')


    samplesWg.Draw( 'sieie_leadph12', 'PUWeight * ( %s && isEE_leadph12 && isEB_sublph12 )' %photon_cuts_looseiso, (40, 0, 0.1), hist_config={'xlabel' : 'Lead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0025'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_lead__mgg__EE_EB__loosenedIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')

    samplesWg.Draw( 'sieie_sublph12', 'PUWeight * ( %s && isEE_leadph12 && isEB_sublph12 )' %photon_cuts_looseiso, (60, 0, 0.03), hist_config={'xlabel' : 'Sublead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0005'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87) } )
                
    if save :
        name = 'ph_sigmaIEIE_subl__mgg__EE_EB__loosenedIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')


    samplesWg.Draw( 'sieie_leadph12', 'PUWeight * ( %s && isEE_leadph12 && isEE_sublph12 )' %photon_cuts_looseiso, (40, 0, 0.1), hist_config={'xlabel' : 'Lead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0025'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_lead__mgg__EE_EE__loosenedIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')

    samplesWg.Draw( 'sieie_sublph12', 'PUWeight * ( %s && isEE_leadph12 && isEE_sublph12  )' %photon_cuts_looseiso, (40, 0, 0.1), hist_config={'xlabel' : 'Sublead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0025'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87) })
                
    if save :
        name = 'ph_sigmaIEIE_subl__mgg__EE_EE__loosenedIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')


    #-----------------------------------
    #-----------------------------------
    # Look at diphotons using full iso
    #-----------------------------------
    #-----------------------------------

    photon_cuts_fulliso = 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoSIEIENoEleVeto_n==2 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && dr_ph1_ph2 >0.3 && m_ph1_ph2 > %d ' %(m_ph1_ph2_cut)

    samplesWg.Draw( 'sieie_leadph12', 'PUWeight * ( %s  && isEB_leadph12 && isEB_sublph12 )' %photon_cuts_fulliso, (60, 0, 0.03), hist_config={'xlabel' : 'Lead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0005'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_lead__mgg__EB_EB__fullIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')

    samplesWg.Draw( 'sieie_sublph12', 'PUWeight * ( %s && isEB_leadph12 && isEB_sublph12 )' %photon_cuts_fulliso, (60, 0, 0.03), hist_config={'xlabel' : 'Sublead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0005'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_subl__mgg__EB_EB__fullIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')


    samplesWg.Draw( 'sieie_leadph12', 'PUWeight * ( %s && isEB_leadph12 && isEE_sublph12 )' %photon_cuts_fulliso, (60, 0, 0.03), hist_config={'xlabel' : 'Lead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0005'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_lead__mgg__EB_EE__fullIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')

    samplesWg.Draw( 'sieie_sublph12', 'PUWeight * ( %s && isEB_leadph12 && isEE_sublph12 )' %photon_cuts_fulliso, (40, 0, 0.1), hist_config={'xlabel' : 'Sublead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0025'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_subl__mgg__EB_EE__fullIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')


    samplesWg.Draw( 'sieie_leadph12', 'PUWeight * ( %s && isEE_leadph12 && isEB_sublph12 )' %photon_cuts_fulliso, (40, 0, 0.1), hist_config={'xlabel' : 'Lead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0025'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_lead__mgg__EE_EB__fullIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')

    samplesWg.Draw( 'sieie_sublph12', 'PUWeight * ( %s && isEE_leadph12 && isEB_sublph12 )' %photon_cuts_fulliso, (60, 0, 0.03), hist_config={'xlabel' : 'Sublead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0005'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_subl__mgg__EE_EB__fullIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')


    samplesWg.Draw( 'sieie_leadph12', 'PUWeight * ( %s && isEE_leadph12 && isEE_sublph12 )' %photon_cuts_fulliso, (40, 0, 0.1), hist_config={'xlabel' : 'Lead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0025'}, label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_lead__mgg__EE_EE__fullIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')

    samplesWg.Draw( 'sieie_sublph12', 'PUWeight * ( %s && isEE_leadph12 && isEE_sublph12 )' %photon_cuts_fulliso, (40, 0, 0.1), hist_config={'xlabel' : 'Sublead photon #sigmai#etai#eta', 'ylabel':'Events / 0.0025'},label_config={'labelStyle':'fancy', 'extra_label':'Muon Channel', 'extra_label_loc':(0.73, 0.87)} )
                
    if save :
        name = 'ph_sigmaIEIE_subl__mgg__EE_EE__fullIso__baselineCuts'
        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base')
        samplesWg.DumpStack(options.outputDir+'/'+subdir, name)
    else :
        samplesWg.DumpStack()
        raw_input('continue')

    #------------------------------------------
    # Compare sigmaIEIE on one photon
    # and vary isolation cuts on the other photon
    # when the other photon fails sigmaIEIE
    #------------------------------------------

    phph_base = 'mu_passtrig25_n>0 && mu_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > %d && dr_ph2_leadLep > 0.4 && dr_ph1_leadLep > 0.4  ' %(m_ph1_ph2_cut)


    sample ='Muon'

    regions = [('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB')]

    for r1, r2 in regions :

        for var, iso_vals in asym_isos.iteritems() :


            binn_lead_coarse = binning[var][r1+'__varBins']
            binn_subl_coarse = binning[var][r2+'__varBins']

            binn_lead = binning[var][r1]
            binn_subl = binning[var][r2]

            for iso_val in iso_vals :

                if var == 'sigmaIEIE' :

                    ph_cuts = 'ph_noSIEIEiso%s%s%s_n==2' %( str(iso_val[0]), str(iso_val[1]), str(iso_val[2]) )
                    phvar = 'ptSorted_ph_noSIEIEiso%s%s%s_idx' %( str(iso_val[0]), str(iso_val[1]), str(iso_val[2]) )

                    tightiso_subl = 'ph_passChIsoCorrMedium[%s[1]] && ph_passNeuIsoCorrMedium[%s[1]] && ph_passPhoIsoCorrMedium[%s[1]]'%(phvar, phvar, phvar)
                    tightiso_lead = 'ph_passChIsoCorrMedium[%s[0]] && ph_passNeuIsoCorrMedium[%s[0]] && ph_passPhoIsoCorrMedium[%s[0]]'%(phvar, phvar, phvar)

                    sieie_loose_subl = {'EB' : ' ph_sigmaIEIE[%s[1]] > 0.011 && ph_sigmaIEIE[%s[1]] < 0.3 ' %(phvar,phvar), 'EE'  : ' ph_sigmaIEIE[%s[1]] > 0.033 && ph_sigmaIEIE[%s[1]] < 0.1 '%(phvar,phvar) }
                    sieie_loose_lead = {'EB' : ' ph_sigmaIEIE[%s[0]] > 0.011 && ph_sigmaIEIE[%s[0]] < 0.3 '%(phvar,phvar), 'EE'  : ' ph_sigmaIEIE[%s[0]] > 0.033 && ph_sigmaIEIE[%s[0]] < 0.1 '%(phvar,phvar) }

                    thisiso_lead = 'ph_chIsoCorr[%s[0]] < %s && ph_neuIsoCorr[%s[0]] < %s && ph_phoIsoCorr[%s[0]] < %s'%(phvar, iso_val[0],phvar,iso_val[1],phvar,iso_val[2])
                    thisiso_subl = 'ph_chIsoCorr[%s[1]] < %s && ph_neuIsoCorr[%s[1]] < %s && ph_phoIsoCorr[%s[1]] < %s'%(phvar, iso_val[0],phvar,iso_val[1],phvar,iso_val[2])

                    selection_lead_iso_subl_tight = 'PUWeight * (  %s && %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, sieie_loose_subl[r2], tightiso_lead, tightiso_subl, r1, phvar, r2, phvar)
                    selection_lead_iso_subl_loose = 'PUWeight * (  %s && %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, sieie_loose_subl[r2], tightiso_lead, thisiso_subl, r1, phvar,r2, phvar)
                    selection_subl_iso_lead_tight = 'PUWeight * (  %s && %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, sieie_loose_lead[r1], tightiso_subl, tightiso_lead, r1, phvar, r2, phvar)
                    selection_subl_iso_lead_loose = 'PUWeight * (  %s && %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, sieie_loose_lead[r1], tightiso_subl, thisiso_lead, r1, phvar, r2, phvar)

                elif var == 'chIsoCorr'  :

                    ph_cuts = 'ph_failSIEIEisoNone%s%s_n==2' %( str(iso_val[1]), str(iso_val[2]) )
                    phvar = 'ptSorted_ph_failSIEIEisoNone%s%s_idx' %( str(iso_val[1]), str(iso_val[2]) )

                    tightiso_subl = 'ph_passNeuIsoCorrMedium[%s[1]] && ph_passPhoIsoCorrMedium[%s[1]]'%(phvar, phvar)
                    tightiso_lead = 'ph_passNeuIsoCorrMedium[%s[0]] && ph_passPhoIsoCorrMedium[%s[0]]'%(phvar, phvar)

                    thisiso_lead = ' ph_neuIsoCorr[%s[0]] < %s && ph_phoIsoCorr[%s[0]] < %s'%(phvar,iso_val[1],phvar,iso_val[2])
                    thisiso_subl = ' ph_neuIsoCorr[%s[1]] < %s && ph_phoIsoCorr[%s[1]] < %s'%(phvar,iso_val[1],phvar,iso_val[2])

                    selection_lead_iso_subl_tight = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_lead, tightiso_subl, r1, phvar, r2, phvar)
                    selection_lead_iso_subl_loose = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_lead, thisiso_subl, r1, phvar,r2, phvar)
                    selection_subl_iso_lead_tight = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_subl, tightiso_lead, r1, phvar, r2, phvar)
                    selection_subl_iso_lead_loose = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_subl, thisiso_lead, r1, phvar, r2, phvar)

                elif var == 'phoIsoCorr'  :

                    ph_cuts = 'ph_failSIEIEiso%s%sNone_n==2' %( str(iso_val[0]), str(iso_val[1]) )
                    phvar = 'ptSorted_ph_failSIEIEiso%s%sNone_idx' %( str(iso_val[0]), str(iso_val[1]) )

                    tightiso_subl = 'ph_passChIsoCorrMedium[%s[1]] && ph_passNeuIsoCorrMedium[%s[1]] '%(phvar, phvar)
                    tightiso_lead = 'ph_passChIsoCorrMedium[%s[0]] && ph_passNeuIsoCorrMedium[%s[0]] '%(phvar, phvar)

                    thisiso_lead = ' ph_chIsoCorr[%s[0]] < %s && ph_neuIsoCorr[%s[0]] < %s'%(phvar,iso_val[0],phvar,iso_val[1])
                    thisiso_subl = ' ph_chIsoCorr[%s[1]] < %s && ph_neuIsoCorr[%s[1]] < %s'%(phvar,iso_val[0],phvar,iso_val[1])

                    selection_lead_iso_subl_tight = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_lead, tightiso_subl, r1, phvar, r2, phvar)
                    selection_lead_iso_subl_loose = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_lead, thisiso_subl, r1, phvar,r2, phvar)
                    selection_subl_iso_lead_tight = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_subl, tightiso_lead, r1, phvar, r2, phvar)
                    selection_subl_iso_lead_loose = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_subl, thisiso_lead, r1, phvar, r2, phvar)

                elif var == 'neuIsoCorr'  :

                    ph_cuts = 'ph_failSIEIEiso%sNone%s_n==2' %( str(iso_val[0]), str(iso_val[2]) )
                    phvar = 'ptSorted_ph_failSIEIEiso%sNone%s_idx' %( str(iso_val[0]), str(iso_val[2]) )

                    tightiso_subl = 'ph_passChIsoCorrMedium[%s[1]] && ph_passPhoIsoCorrMedium[%s[1]]'%(phvar, phvar)
                    tightiso_lead = 'ph_passChIsoCorrMedium[%s[0]] && ph_passPhoIsoCorrMedium[%s[0]]'%(phvar, phvar)

                    thisiso_lead = ' ph_chIsoCorr[%s[0]] < %s && ph_phoIsoCorr[%s[0]] < %s'%(phvar,iso_val[0],phvar,iso_val[2])
                    thisiso_subl = ' ph_chIsoCorr[%s[1]] < %s && ph_phoIsoCorr[%s[1]] < %s'%(phvar,iso_val[0],phvar,iso_val[2])

                    selection_lead_iso_subl_tight = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_lead, tightiso_subl, r1, phvar, r2, phvar)
                    selection_lead_iso_subl_loose = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_lead, thisiso_subl, r1, phvar,r2, phvar)
                    selection_subl_iso_lead_tight = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_subl, tightiso_lead, r1, phvar, r2, phvar)
                    selection_subl_iso_lead_loose = 'PUWeight * (  %s && %s && %s && %s && ph_Is%s[%s[0]] && ph_Is%s[%s[1]] )' %( phph_base, ph_cuts, tightiso_subl, thisiso_lead, r1, phvar, r2, phvar)

                if r1 == 'EB' :
                    ymax_lead = 0.8
                if r1 == 'EE' :
                    ymax_lead = 0.5
                if r2 == 'EB' : 
                    ymax_subl = 0.8
                if r2 == 'EE' : 
                    ymax_subl = 0.5

                samplesLGG.CompareSelections('ph_%s[%s[0]]'%(var,phvar), [selection_lead_iso_subl_tight, selection_lead_iso_subl_loose], [sample, sample], binn_lead_coarse, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed ], 'doratio':1, 'ylabel':'Normalized Events / 0.0001', 'xlabel':'#sigma i#etai#eta', 'ymin':0, 'ymax':0.8, 'rmin':0.5, 'rmax':1.5}, legend_config={'legend_entries':['Tight iso lead, tight iso subl', 'tightiso lead, loose(%s,%s,%s) iso subl' %(iso_val[0], iso_val[1], iso_val[2])], 'legendWiden' : 1.5, 'legendCompress' : 1.4} )

                if save :
                    name = 'ph_%s_lead__mgg__%s-%s__baselineCuts__comp_sieie_lead_tight_subl_tight_to_%s-%s-%s_varBins' %( var,r1,r2, iso_val[0], iso_val[1], iso_val[2])
                    samplesLGG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                    samplesLGG.DumpStack(options.outputDir+'/'+subdir, name )
                else :
                    raw_input('continue')

                samplesLGG.CompareSelections('ph_%s[%s[1]]'%(var,phvar), [selection_subl_iso_lead_tight, selection_subl_iso_lead_loose], [sample, sample], binn_subl_coarse, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed ], 'doratio':1, 'ylabel':'Normalized Events / 0.0001', 'xlabel':'#sigma i#etai#eta', 'ymin':0, 'ymax':0.8, 'rmin':0.5, 'rmax':1.5}, legend_config={'legendWiden' : 1.5, 'legendCompress' : 1.4, 'legend_entries':['Tight iso lead, tight iso subl', 'tightiso subl, loose(%s,%s,%s) iso lead' %(iso_val[0], iso_val[1], iso_val[2])]} )

                if save :
                    name = 'ph_%s_subl__mgg__%s-%s__baselineCuts__comp_sieie_subl_tight_lead_tight_to_%s-%s-%s_varBins' %( var,r1,r2, iso_val[0], iso_val[1], iso_val[2])
                    samplesLGG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                    samplesLGG.DumpStack(options.outputDir+'/'+subdir, name )
                else :
                    raw_input('continue')

                samplesLGG.CompareSelections('ph_%s[%s[0]]'%(var,phvar), [selection_lead_iso_subl_tight,selection_lead_iso_subl_loose], [sample, sample], binn_lead, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed ], 'doratio':1, 'ylabel':'Normalized Events / 0.0001', 'xlabel':'#sigma i#etai#eta', 'ymin':0, 'ymax':ymax_lead, 'rmin':0, 'rmax':4}, legend_config={'legend_entries':['Tight iso lead, tight iso subl', 'tightiso lead, loose(%s,%s,%s) iso subl' %(iso_val[0], iso_val[1], iso_val[2])], 'legendWiden' : 1.5, 'legendCompress' : 1.4} )

                if save :
                    name = 'ph_%s_lead__mgg__%s-%s__baselineCuts__comp_sieie_lead_tight_subl_tight_to_%s-%s-%s' %( var,r1,r2, iso_val[0], iso_val[1], iso_val[2])
                    samplesLGG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                    samplesLGG.DumpStack(options.outputDir+'/'+subdir, name )
                else :
                    raw_input('continue')

                samplesLGG.CompareSelections('ph_%s[%s[1]]'%(var,phvar), [selection_subl_iso_lead_tight, selection_subl_iso_lead_loose], [sample, sample], binn_subl, hist_config={'normalize':1, 'colors':[ROOT.kBlack, ROOT.kRed ], 'doratio':1, 'ylabel':'Normalized Events / 0.0001', 'xlabel':'#sigma i#etai#eta', 'ymin':0, 'ymax':ymax_subl, 'rmin':0, 'rmax':4}, legend_config={'legendWiden' : 1.5, 'legendCompress' : 1.4, 'legend_entries':['Tight iso lead, tight iso subl', 'tightiso subl, loose(%s,%s,%s) iso lead' %(iso_val[0], iso_val[1], iso_val[2])]} )

                if save :
                    name = 'ph_%s_subl__mgg__%s-%s__baselineCuts__comp_sieie_subl_tight_lead_tight_to_%s-%s-%s' %( var,r1,r2, iso_val[0], iso_val[1], iso_val[2])
                    samplesLGG.SaveStack( name, options.outputDir+'/'+subdir, 'base')
                    samplesLGG.DumpStack(options.outputDir+'/'+subdir, name )
                else :
                    raw_input('continue')

#------------------------------------------
# DEPRICATED
#------------------------------------------
#def MakeJetFakeFactorPlots(save=False, detail=100) :
#
#    subdir = 'JetFakeFactorPlots'
#
#    cut_invsieie_eb = 0.013
#    cut_invsieie_ee = 0.035
#
#    #var_bins = (40, 0, 200, [0, 5, 10, 15, 20, 25, 30, 40, 60, 100, 200] )
#    var_bins = (40, 0, 200, [0, 5, 10, 15, 20, 25, 30, 40, 60,  200] )
#    bins = (40, 0, 200)
#
#    base_cuts = 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0]<0.05 && ph_hasPixSeed[0]==0 '
#    fake_cr_cuts = 'fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 '
#
#    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0]  && ph_IsEE[0] && %s)' %( base_cuts, fake_cr_cuts) ,bins , xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Endcap photons', logy=1 )
#
#    #if save :
#    #    name = 'ph_pt__mmg__EE__Cut_passphoIso_passneuIso_chIsoWindow5-20_passSIEIE__ZjetsFakeCR'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEE[0] && %s )' %( base_cuts, cut_invsieie_ee, fake_cr_cuts ) , bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Endcap photons', logy=1  )
#
#    #if save :
#    #    name = 'ph_pt__mmg__EE__Cut_invphoIso_invneuIso_chIsoWindow5-20_invSIEIE__ZjetsFakeCR'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0]  && ph_IsEB[0] && %s)' %( base_cuts, fake_cr_cuts) , bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Barrel photons', logy=1 )
#
#    #if save :
#    #    name = 'ph_pt__mmg__EB__Cut_passphoIso_passneuIso_chIsoWindow5-20_passSIEIE__ZjetsFakeCR'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEB[0] && %s )' %( base_cuts, cut_invsieie_eb, fake_cr_cuts ) , bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Barrel photons', logy=1  )
#
#    #if save :
#    #    name = 'ph_pt__mmg__EB__Cut_invphoIso_invneuIso_chIsoWindow5-20_invSIEIE__ZjetsFakeCR'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0]  && ph_IsEE[0] && %s)' %( base_cuts, fake_cr_cuts) ,var_bins , xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Endcap photons', logy=1 )
#
#    #if save :
#    #    name = 'ph_pt__mmg__EE__Cut_passphoIso_passneuIso_chIsoWindow5-20_passSIEIE__ZjetsFakeCR__varBins'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEE[0] && %s )' %( base_cuts, cut_invsieie_ee, fake_cr_cuts ) , var_bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Endcap photons', logy=1  )
#
#    #if save :
#    #    name = 'ph_pt__mmg__EE__Cut_invphoIso_invneuIso_chIsoWindow5-20_invSIEIE__ZjetsFakeCR__varBins'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0]  && ph_IsEB[0] && %s)' %( base_cuts, fake_cr_cuts) , var_bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Barrel photons', logy=1 )
#
#    #if save :
#    #    name = 'ph_pt__mmg__EB__Cut_passphoIso_passneuIso_chIsoWindow5-20_passSIEIE__ZjetsFakeCR__varBins'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw( 'ph_pt[0]', 'PUWeight * ( %s && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEB[0] && %s )' %( base_cuts, cut_invsieie_eb, fake_cr_cuts ) , var_bins, xlabel='photon p_{T} [GeV]', labelStyle='fancy', extra_label='Barrel photons', logy=1  )
#
#    #if save :
#    #    name = 'ph_pt__mmg__EB__Cut_invphoIso_invneuIso_chIsoWindow5-20_invSIEIE__ZjetsFakeCR__varBins'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #if detail < 1 :
#    #    return
#    #-------------------------
#    #-------------------------
#    # Look at chIso to determine window size
#    #-------------------------
#    #-------------------------
#
#    samplesWg.Draw( 'ph_chIsoCorr[0]', 'PUWeight * ( %s && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEB[0] && %s )' %( base_cuts, cut_invsieie_eb, fake_cr_cuts ) , (50, 0, 50), xlabel='Charged Hadron iso [GeV]', labelStyle='fancy', extra_label='Barrel photons', extra_label_loc=(0.45, 0.87), logy=1, ymax=5e4, legend_config=samplesWg.config_legend(legendLoc='Double')  )
#
#    if save :
#        name = 'ph_chIsoCorr__mmg__EB__Cut_invNeuPhoIso_invSIEIE__ZjetsFakeCR'
#        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    else :
#        raw_input('continue')
#
#
#    samplesWg.Draw( 'ph_chIsoCorr[0]', 'PUWeight * ( %s && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && ph_sigmaIEIE[0] > %f  && ph_IsEE[0] && %s )' %( base_cuts, cut_invsieie_ee, fake_cr_cuts ) , (50, 0, 50), xlabel='Charged Hadron iso [GeV]', labelStyle='fancy', extra_label='Endcap photons', extra_label_loc=(0.6, 0.87), logy=1, legend_config=samplesWg.config_legend(legendLoc='Double')   )
#
#    if save :
#        name = 'ph_chIsoCorr__mmg__EE__Cut_invNeuPhoIso_invSIEIE__ZjetsFakeCR'
#        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    else :
#        raw_input('continue')
#
#    samplesWg.Draw( 'ph_chIsoCorr[0]', 'PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0] && ph_IsEB[0] && %s )' %( base_cuts, fake_cr_cuts ) , (50, 0, 50), xlabel='Charged Hadron iso [GeV]', labelStyle='fancy', extra_label='Barrel photons', extra_label_loc=(0.6, 0.87), logy=0 )
#
#    if save :
#        name = 'ph_chIsoCorr__mmg__EB__Cut_passNeuPhoIso_passSIEIE__ZjetsFakeCR'
#        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    else :
#        raw_input('continue')
#
#    samplesWg.Draw( 'ph_chIsoCorr[0]', 'PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0] && ph_IsEE[0] && %s )' %( base_cuts, fake_cr_cuts ) , (50, 0, 50), xlabel='Charged Hadron iso [GeV]', labelStyle='fancy', extra_label='Endcap photons', extra_label_loc=(0.6, 0.87), logy=0, legend_config=samplesWg.config_legend() )
#
#    if save :
#        name = 'ph_chIsoCorr__mmg__EE__Cut_passNeuPhoIso_passSIEIE__ZjetsFakeCR'
#        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    else :
#        raw_input('continue')
#
#    print detail
#
#    if detail < 2 :
#        print 'RETURN'
#        return
#
#    #-------------------------
#    #-------------------------
#    # Motivate choice of loose selection
#    #-------------------------
#    #-------------------------
#
#    base_cuts = 'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && dr_ph1_ph2>0.4 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 '
#
#
#    #-------------------------
#    # Full Iso -- EB EB
#    #-------------------------
#
#    ph_iso_cuts = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1]'
#
#    ## fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ##real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ##fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ##-------------------------
#    ## Full Iso -- EE EE
#    ##-------------------------
#
#    ##fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##-------------------------
#    ## Full Iso -- EB EE
#    ##-------------------------
#
#
#    ## fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##-------------------------
#    ## Full Iso -- EE EB
#    ##-------------------------
#
#
#    ## fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passAllIso_passSIEIE_lead__Cut_passAllIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passAllIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#
#    #-------------------------
#    # Inv Iso -- EB EB
#    #-------------------------
#
#    ph_iso_cuts_ff = '!ph_passChIsoCorrMedium[0] && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && !ph_passChIsoCorrMedium[1] && !ph_passNeuIsoCorrMedium[1] && !ph_passPhoIsoCorrMedium[1]'
#    ph_iso_cuts_fr = '!ph_passChIsoCorrMedium[0] && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1]'
#    ph_iso_cuts_rf = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && !ph_passChIsoCorrMedium[1] && !ph_passNeuIsoCorrMedium[1] && !ph_passPhoIsoCorrMedium[1]'
#
#    ## fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ##real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ##fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ##-------------------------
#    ## Inv Iso -- EE EE
#    ##-------------------------
#
#    ##fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##-------------------------
#    ## Inv Iso -- EB EE
#    ##-------------------------
#
#
#    ## fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##-------------------------
#    ## Inv Iso -- EE EB
#    ##-------------------------
#
#
#    ## fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_invIso_invSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passAllIso_passSIEIE_lead__Cut_invIso_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )
#
#    if save :
#        name = 'ph_pt_subl__mgg__EE_EB__Cut_invIso_invSIEIE_lead__Cut_passAllIso_passSIEIE_subl'
#        samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    else :
#        raw_input('continue')
#
#
#    ##-------------------------
#    ## Inv Iso, Ch iso window -- EB EB
#    ##-------------------------
#
#    #ph_iso_cuts_ff = '!ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && !ph_passNeuIsoCorrMedium[1] && !ph_passPhoIsoCorrMedium[1] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 && ph_chIsoCorr[1] > 5 && ph_chIsoCorr[1] < 20'
#    #ph_iso_cuts_fr = '!ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && ph_passNeuIsoCorrMedium[1]  && ph_passPhoIsoCorrMedium[1]  && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 && ph_chIsoCorr[1] > 5 && ph_chIsoCorr[1] < 20'
#    #ph_iso_cuts_rf = 'ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]    && !ph_passNeuIsoCorrMedium[1] && !ph_passPhoIsoCorrMedium[1] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 20 && ph_chIsoCorr[1] > 5 && ph_chIsoCorr[1] < 20'
#
#    ## fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ##real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ##fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEB[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ##-------------------------
#    ## Inv Iso, Ch iso window -- EE EE
#    ##-------------------------
#
#    ##fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_ee, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#
#    ##-------------------------
#    ## Inv Iso, Ch iso window -- EB EE
#    ##-------------------------
#
#
#    ## fake fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_ff, cut_invsieie_eb, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EB_EE__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## real fake
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0] && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EB_EE__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEB[0] && ph_IsEE[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_ee ), (50, 0, 200) )
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[0]  && ph_sigmaIEIE[1] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_rf, cut_invsieie_eb ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_lead__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    ## fake real
#
#    #samplesWg.Draw('ph_pt[0]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1] && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_lead__mgg__EE_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')
#
#    #samplesWg.Draw('ph_pt[1]', 'PUWeight * ( %s && %s && ph_passSIEIEMedium[1]  && ph_sigmaIEIE[0] > %f && ph_IsEE[0] && ph_IsEB[1] )' %( base_cuts, ph_iso_cuts_fr, cut_invsieie_ee ), (50, 0, 200) )
#
#    #if save :
#    #    name = 'ph_pt_subl__mgg__EE_EB__Cut_invNeuPhoIso_chIsoWindow_invSIEIE_lead__Cut_passNeuPhoIso_chIsoWindow_passSIEIE_subl'
#    #    samplesWg.SaveStack( name, options.outputDir+'/'+subdir, 'base', write_command=True)
#    #else :
#    #    raw_input('continue')

main()
