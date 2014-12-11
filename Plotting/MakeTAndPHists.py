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
from FitTagAndProbe import pair_pt_eta_bins

ROOT.gROOT.SetBatch(False)

samplesWgg = None
samplesWg = None
samplesLLG = None
samplesPhOlap= None

analysis_bins_mgg = [0, 5, 10, 15, 25, 40, 70, 200 ] 
analysis_bins_egg = [0, 5, 10, 15, 25, 40, 70, 200 ] 

lead_dr_cut = 0.4
subl_dr_cut = 0.4
phot_dr_cut = 0.3

_baseline_cuts_mgg = ' mu_passtrig25_n>0 && mu_n==1 && ph_medium_n>1 && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && dr_ph1_ph2>%.1f && m_ph1_ph2>15 && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f '%(phot_dr_cut, lead_dr_cut, subl_dr_cut)
_baseline_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_medium_n>1 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && dr_ph1_ph2>%.1f && m_ph1_ph2>15 && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f '%(phot_dr_cut, lead_dr_cut, subl_dr_cut)
_zrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_medium_n>1 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && dr_ph1_ph2>%.1f && m_ph1_ph2>15 && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f  && !(fabs(m_leadLep_ph1_ph2-91.2) < 5) && !(fabs(m_leadLep_ph1-91.2) < 5)  && !(fabs(m_leadLep_ph2-91.2) < 5) ' %(phot_dr_cut, lead_dr_cut, subl_dr_cut)
_zcr_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_medium_n>1 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && dr_ph1_ph2>%.1f && m_ph1_ph2>15 && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f && ( (fabs(m_leadLep_ph1_ph2-91.2) < 5) || (fabs(m_leadLep_ph1-91.2) < 5)  || (fabs(m_leadLep_ph2-91.2) < 5) ) ' %(phot_dr_cut, lead_dr_cut, subl_dr_cut)

invPixLead_cuts_egg         = ' el_passtrig_n>0 && el_n==1 && ph_medium_n>1 && mu_n==0 && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && dr_ph1_ph2>%.1f && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f '%(phot_dr_cut, lead_dr_cut, subl_dr_cut)
invPixSubl_cuts_egg         = ' el_passtrig_n>0 && el_n==1 && ph_medium_n>1 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && dr_ph1_ph2>%.1f && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f '%(phot_dr_cut, lead_dr_cut, subl_dr_cut)

invPixLead_zrej_cuts_egg    = ' el_passtrig_n>0 && el_n==1 && ph_medium_n>1 && mu_n==0 && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && dr_ph1_ph2>%.1f && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f && !(fabs(m_leadLep_ph1_ph2-91.2) < 5) && !(fabs(m_leadLep_ph1-91.2) < 5)  && !(fabs(m_leadLep_ph2-91.2) < 5) ' %(phot_dr_cut, lead_dr_cut, subl_dr_cut)
invPixSubl_zrej_cuts_egg    = ' el_passtrig_n>0 && el_n==1 && ph_medium_n>1 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && dr_ph1_ph2>%.1f && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f && !(fabs(m_leadLep_ph1_ph2-91.2) < 5) && !(fabs(m_leadLep_ph1-91.2) < 5)  && !(fabs(m_leadLep_ph2-91.2) < 5) ' %(phot_dr_cut, lead_dr_cut, subl_dr_cut)

invPixLead_invzrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_medium_n>1 && mu_n==0 && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && dr_ph1_ph2>%.1f && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f && ((fabs(m_leadLep_ph1_ph2-91.2) < 5) || (fabs(m_leadLep_ph1-91.2) < 5) || (fabs(m_leadLep_ph2-91.2) < 5) ) ' %(phot_dr_cut, lead_dr_cut, subl_dr_cut)
invPixSubl_invzrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_medium_n>1 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && dr_ph1_ph2>%.1f && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f && ((fabs(m_leadLep_ph1_ph2-91.2) < 5) || (fabs(m_leadLep_ph1-91.2) < 5) || (fabs(m_leadLep_ph2-91.2) < 5) ) ' %(phot_dr_cut, lead_dr_cut, subl_dr_cut)

def main() :

    global samplesMuMu
    global samplesElEl

    baseDirMuMu = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPMuMu_2014_11_27'
    baseDirElEl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPElEl_2014_11_27'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConf = 'Modules/TAndPSampleConf.py'

    samplesMuMu = SampleManager(baseDirMuMu, treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    samplesElEl = SampleManager(baseDirElEl, treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)

    samplesMuMu .ReadSamples( sampleConf )
    samplesElEl .ReadSamples( sampleConf )

    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)

    samplesMuMu.start_command_collection()
    samplesElEl.start_command_collection()

    MakeMuMuPlots( )
    MakeElElPlots( )

    samplesMuMu.run_commands()
    samplesElEl.run_commands()
#---------------------------------------
# User functions
#---------------------------------------

#---------------------------------------
def MakeMuMuPlots( save=False, detail=100, ph_cuts='', dirPostfix='', activate_data=False ) :

    subdir='TAndPMuMuPlots'

    cmd_loose = ' muprobe_pt > 0 '
    cmd_tight = ' muprobe_passTight == 1 '
    cmd_trig  = ' muprobe_triggerMatch == 1 && muprobe_passTight==1 '

    eta_bins_lowpt  = [0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.1, 2.3, 2.4]
    eta_bins_highpt = [0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.4]
    low_pt_bins_tight = range( 10, 30, 5) 
    low_pt_bins_trig = range( 24, 30, 2)
    med_pt_bins = [30, 40, 50]
    high_pt_bins = [100, 200, 1000000]

    pt_eta_bins_tight = pair_pt_eta_bins( [ (low_pt_bins_tight, eta_bins_lowpt ), (med_pt_bins, eta_bins_lowpt), ( high_pt_bins, eta_bins_highpt ) ] )
    pt_eta_bins_trig  = pair_pt_eta_bins( [ (low_pt_bins_trig, eta_bins_lowpt ) , (med_pt_bins, eta_bins_lowpt), ( high_pt_bins, eta_bins_highpt ) ] )
    pt_eta_bins_comb = pair_pt_eta_bins( [(low_pt_bins_tight, eta_bins_lowpt), (low_pt_bins_trig, eta_bins_lowpt), (med_pt_bins, eta_bins_lowpt), ( high_pt_bins, eta_bins_highpt )  ]  )

    PTMAX = high_pt_bins[-1]

    #------------------------------------
    # Make plots in each pt and eta region
    # for loose muons
    # use combined bins because
    # loose is the denominator for both 
    # tight and trig
    #------------------------------------
    for (ptmin, ptmax), etabins in pt_eta_bins_comb.iteritems() :
        for etamin, etamax in etabins :

            samplesMuMu.Draw('m_mutagprobe', 'PUWeight * ( muprobe_pt > %d && muprobe_pt < %d && fabs( muprobe_eta ) > %f && fabs(muprobe_eta) < %f  )' %(ptmin, ptmax, etamin, etamax ), (50, 60, 160) , hist_config={'ymin': 0.1, 'ymax':10000, 'logy':1, 'xlabel':'M_{#mu probe, #mu tag}',}, label_config={'labelStyle':'fancy', 'extra_label':'Loose muons', 'extra_label_loc':(0.2, 0.87)}, legend_config=samplesMuMu.config_legend(  legendCompress=1.2, legendWiden=1.2 ) )

            if  ptmax >= PTMAX :
                name = 'm_mutagprobe__loose__eta_%.2f-%.2f__pt_%d-max' %(etamin, etamax, ptmin)
            else :
                name = 'm_mutagprobe__loose__eta_%.2f-%.2f__pt_%d-%d' %(etamin, etamax, ptmin, ptmax)
            samplesMuMu.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)


    #------------------------------------
    # Make plots in each pt and eta region
    # for tight muons
    #------------------------------------
    for (ptmin, ptmax), etabins in pt_eta_bins_tight.iteritems() :
        for etamin, etamax in etabins :

            samplesMuMu.Draw('m_mutagprobe', 'PUWeight * ( %s && muprobe_pt > %d && muprobe_pt < %d && fabs( muprobe_eta ) > %f && fabs(muprobe_eta) < %f  )' %(cmd_tight, ptmin, ptmax, etamin, etamax ), (50, 60, 160) , hist_config={'ymin': 0.1, 'ymax':10000, 'logy':1, 'xlabel':'M_{#mu probe, #mu tag}',}, label_config={'labelStyle':'fancy', 'extra_label':'Tight muons', 'extra_label_loc':(0.2, 0.87)}, legend_config=samplesMuMu.config_legend(  legendCompress=1.2, legendWiden=1.2 ) )

            if  ptmax >= PTMAX :
                name = 'm_mutagprobe__tight__eta_%.2f-%.2f__pt_%d-max' %(etamin, etamax, ptmin)
            else :
                name = 'm_mutagprobe__tight__eta_%.2f-%.2f__pt_%d-%d' %(etamin, etamax, ptmin, ptmax)
            samplesMuMu.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)

    #------------------------------------
    # Make plots in each pt and eta region
    # for trig muons
    #------------------------------------
    for (ptmin, ptmax), etabins in pt_eta_bins_trig.iteritems() :
        for etamin, etamax in etabins :

            samplesMuMu.Draw('m_mutagprobe', 'PUWeight * ( %s && muprobe_pt > %d && muprobe_pt < %d && fabs( muprobe_eta ) > %f && fabs(muprobe_eta) < %f  )' %(cmd_trig, ptmin, ptmax, etamin, etamax ), (50, 60, 160) , hist_config={'ymin': 0.1, 'ymax':10000, 'logy':1, 'xlabel':'M_{#mu probe, #mu tag}',}, label_config={'labelStyle':'fancy', 'extra_label':'Trigger muons', 'extra_label_loc':(0.2, 0.87)}, legend_config=samplesMuMu.config_legend(  legendCompress=1.2, legendWiden=1.2 ) )

            if  ptmax >= PTMAX :
                name = 'm_mutagprobe__trig__eta_%.2f-%.2f__pt_%d-max' %(etamin, etamax, ptmin)
            else :
                name = 'm_mutagprobe__trig__eta_%.2f-%.2f__pt_%d-%d' %(etamin, etamax, ptmin, ptmax)
            samplesMuMu.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)

def MakeElElPlots( ) :

    subdir = 'TAndPElElPlots'

    cmd_loose = 'elprobe_isPh==1'
    cmd_obj   = 'elprobe_isEl==1 && elprobe_isPh==1'
    cmd_tight = 'elprobe_isEl==1 && elprobe_isPh==0 && elprobe_passMVANonTrig==1'
    cmd_trig  = 'elprobe_isEl==1 && elprobe_isPh==0 && elprobe_passMVATrig==1 && elprobe_triggerMatch==1 '



    eta_bins_lowpt  = [0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.1, 2.3, 2.4]
    eta_bins_highpt = [0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.4]
    low_pt_bins_tight = range( 10, 30, 5) + [30, 40, 50 ] 
    low_pt_bins_trig = range( 24, 30, 2) + [30, 40, 50 ]
    high_pt_bins = [50, 100, 200, 1000000]

    pt_eta_bins_tight = pair_pt_eta_bins( [ (low_pt_bins_tight, eta_bins_lowpt ), ( high_pt_bins, eta_bins_highpt ) ] )
    pt_eta_bins_trig  = pair_pt_eta_bins( [ (low_pt_bins_trig, eta_bins_lowpt ), ( high_pt_bins, eta_bins_highpt ) ] )

    pt_eta_bins_tight = pair_pt_eta_bins( [ (low_pt_bins_tight, eta_bins_lowpt ), ( high_pt_bins, eta_bins_highpt ) ] )
    pt_eta_bins_trig  = pair_pt_eta_bins( [ (low_pt_bins_trig, eta_bins_lowpt ) , ( high_pt_bins, eta_bins_highpt ) ] )
    pt_eta_bins_comb = pair_pt_eta_bins( [(low_pt_bins_tight, eta_bins_lowpt), (low_pt_bins_trig, eta_bins_lowpt), ( high_pt_bins, eta_bins_highpt )  ]  )

    PTMAX = high_pt_bins[-1]

    #------------------------------------
    # Make plots in each pt and eta region
    # for loose electrons
    # use combined bins because
    #------------------------------------
    for (ptmin, ptmax), etabins in pt_eta_bins_tight.iteritems() :
        for etamin, etamax in etabins :

            samplesElEl.Draw('m_eltagprobe', 'PUWeight * ( %s && elprobe_pt > %d && elprobe_pt < %d && fabs( elprobe_eta ) > %f && fabs(elprobe_eta) < %f  )' %(cmd_loose, ptmin, ptmax, etamin, etamax ), (50, 60, 160) , hist_config={'ymin': 0.1, 'ymax':10000, 'logy':1, 'xlabel':'M_{e probe, e tag}',}, label_config={'labelStyle':'fancy', 'extra_label':'SC Electrons', 'extra_label_loc':(0.2, 0.87)}, legend_config=samplesElEl.config_legend( legendCompress=1.2, legendWiden=1.2 ) )

            if  ptmax >= PTMAX :
                name = 'm_eltagprobe__loose__eta_%.2f-%.2f__pt_%d-max' %(etamin, etamax, ptmin)
            else :
                name = 'm_eltagprobe__loose__eta_%.2f-%.2f__pt_%d-%d' %(etamin, etamax, ptmin, ptmax)
            samplesElEl.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)


    #------------------------------------
    # Make plots in each pt and eta region
    # for obj electrons
    # use combined bins because
    # obj is the denominator for both 
    # tight and trig
    #------------------------------------

    for (ptmin, ptmax), etabins in pt_eta_bins_comb.iteritems() :
        for etamin, etamax in etabins :

            samplesElEl.Draw('m_eltagprobe', 'PUWeight * ( %s && elprobe_pt > %d && elprobe_pt < %d && fabs( elprobe_eta ) > %f && fabs(elprobe_eta) < %f  )' %(cmd_obj, ptmin, ptmax, etamin, etamax ), (50, 60, 160) , hist_config={'ymin': 0.1, 'ymax':10000, 'logy':1, 'xlabel':'M_{e probe, e tag}',}, label_config={'labelStyle':'fancy', 'extra_label':'Reco Electrons', 'extra_label_loc':(0.2, 0.87)}, legend_config=samplesElEl.config_legend( legendCompress=1.2, legendWiden=1.2 ) )

            if  ptmax >= PTMAX :
                name = 'm_eltagprobe__obj__eta_%.2f-%.2f__pt_%d-max' %(etamin, etamax, ptmin)
            else :
                name = 'm_eltagprobe__obj__eta_%.2f-%.2f__pt_%d-%d' %(etamin, etamax, ptmin, ptmax)
            samplesElEl.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)

    #------------------------------------
    # Make plots in each pt and eta region
    # for tight electrons
    #------------------------------------

    for (ptmin, ptmax), etabins in pt_eta_bins_tight.iteritems() :
        for etamin, etamax in etabins :

            samplesElEl.Draw('m_eltagprobe', 'PUWeight * ( %s && elprobe_pt > %d && elprobe_pt < %d && fabs( elprobe_eta ) > %f && fabs(elprobe_eta) < %f  )' %(cmd_tight, ptmin, ptmax, etamin, etamax ), (50, 60, 160) , hist_config={'ymin': 0.1, 'ymax':10000, 'logy':1, 'xlabel':'M_{e probe, e tag}',}, label_config={'labelStyle':'fancy', 'extra_label':'MVA Electrons', 'extra_label_loc':(0.2, 0.87)}, legend_config=samplesElEl.config_legend( legendCompress=1.2, legendWiden=1.2 ) )

            if  ptmax >= PTMAX :
                name = 'm_eltagprobe__tight__eta_%.2f-%.2f__pt_%d-max' %(etamin, etamax, ptmin)
            else :
                name = 'm_eltagprobe__tight__eta_%.2f-%.2f__pt_%d-%d' %(etamin, etamax, ptmin, ptmax)
            samplesElEl.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)

    #------------------------------------
    # Make plots in each pt and eta region
    # for trig electrons
    #------------------------------------

    for (ptmin, ptmax), etabins in pt_eta_bins_trig.iteritems() :
        for etamin, etamax in etabins :

            samplesElEl.Draw('m_eltagprobe', 'PUWeight * ( %s && elprobe_pt > %d && elprobe_pt < %d && fabs( elprobe_eta ) > %f && fabs(elprobe_eta) < %f  )' %(cmd_trig, ptmin, ptmax, etamin, etamax ), (50, 60, 160) , hist_config={'ymin': 0.1, 'ymax':10000, 'logy':1, 'xlabel':'M_{e probe, e tag}',}, label_config={'labelStyle':'fancy', 'extra_label':'Trigger Electrons', 'extra_label_loc':(0.2, 0.87)}, legend_config=samplesElEl.config_legend( legendCompress=1.2, legendWiden=1.2 ) )

            if  ptmax >= PTMAX :
                name = 'm_eltagprobe__trig__eta_%.2f-%.2f__pt_%d-max' %(etamin, etamax, ptmin)
            else :
                name = 'm_eltagprobe__trig__eta_%.2f-%.2f__pt_%d-%d' %(etamin, etamax, ptmin, ptmax)
            samplesElEl.SaveStack( name, options.outputDir +'/' +subdir, 'base', write_command=True)

main()
