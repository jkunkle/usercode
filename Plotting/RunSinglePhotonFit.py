"""
Plot 
"""
import sys
import os
import re
import math
import uuid
import copy
import imp
from array import array
import random
import collections
import pickle
import time

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('--fitPath',     default=None,  type=str ,        dest='fitPath',         help='Path to ntuples having the data to be fit')
p.add_argument('--fileName',     default='ntuple.root',  dest='fileName',        help='( Default ntuple.root ) Name of files')
p.add_argument('--treeName',     default='events'     ,  dest='treeName',        help='( Default events ) Name tree in root file')
p.add_argument('--samplesConf',  default=None,           dest='samplesConf',     help=('Use alternate sample configuration. '
                                                                                       'Must be a python file that implements the configuration '
                                                                                       'in the same manner as in the main() of this script.  If only '
                                                                                       'the file name is given it is assumed to be in the same directory '
                                                                                       'as this script, if a path is given, use that path' ) )

                                                                                       
p.add_argument('--xsFile',     default=None,  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')
p.add_argument('--syst_file',     default=None,  type=str ,        dest='syst_file',         help='Location of systematics file')
p.add_argument('--fitvar',     default='sigmaIEIE',  type=str ,        dest='fitvar',         help='Variable to use in the fit')
p.add_argument('--pid',     default='Medium',  type=str ,        dest='pid',         help='PID to use (Medium, Tight)')
p.add_argument('--ptbins',     default='15,25,40,70,1000000',  type=str ,        dest='ptbins',         help='list of pt bins')

p.add_argument('--channel', default='mu',  dest='channel', help='run this channel' )

options = p.parse_args()

import ROOT
from uncertainties import ufloat
from uncertainties import unumpy
from SampleManager import SampleManager
from SampleManager import Sample
from RunMatrixFit import draw_template


if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
else :
    ROOT.gROOT.SetBatch(False)

sampMan = None
sampManFit = None

def get_real_template_draw_commands( ch='mu') :

    return 'mu_passtrig25_n>0 && mu_n==1 &&  ph_HoverE12[0] < 0.05 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25  '

def get_fake_template_draw_commands( ch='mu' ) :

    return 'mu_passtrig25_n>0 && mu_n==2 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 '

def get_fake_window_template_draw_commands( ch='mu' ) :
    if ch.count('mu') :
         return 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] ',
    else :
         return 'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] ',
#'realwin' :'mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] ',

def get_default_draw_commands(ch='mu' ) :

    gg_cmds = {}
    if ch=='mu' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4  && el_n==0 && m_leplep>60 && m_leplepph > 105' }
    elif ch=='murealcr' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && el_n==0 && m_leplep>60 && m_leplepph > 81 && m_leplepph < 101' }
    elif ch == 'el' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==2 && leadPhot_leadLepDR>0.4 && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && mu_n==0 && m_leplep>60 && m_leplepph > 105',}
    elif ch == 'elrealcr' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==2 && leadPhot_leadLepDR>0.4 && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && mu_n==0 && m_leplep>60 && m_leplepph > 81 && m_leplepph < 101',}
    elif ch=='muw' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 &&  ph_HoverE12[0] < 0.05 && el_n==0 && mt_trigmu_met > 40',}
    elif ch=='muwtight' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 &&  ph_HoverE12[0] < 0.05 && el_n==0 && mt_trigmu_met > 80',}
    elif ch=='muwlowmt' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 &&  ph_HoverE12[0] < 0.05 && el_n==0 && mt_trigmu_met < 40',}
    elif ch=='muw_tp_medium' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && leadPhot_leadLepDR>0.4 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_lep_met > 60',}
    elif ch=='muw_tp_eveto' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && ph_hasPixSeed[0] == 0 && leadPhot_leadLepDR>0.4 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_lep_met > 60',}
    elif ch=='muzpeak_tp_eveto' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && ph_hasPixSeed[0]==0 && leadPhot_leadLepDR>0.4 && leadPhot_sublLepDR>0.4 && ph_HoverE12[0] < 0.05 && m_leplep>81 && m_leplep < 101',}
    elif ch=='muzpeak_tp_medium' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && leadPhot_leadLepDR>0.4 && leadPhot_sublLepDR>0.4 && ph_HoverE12[0] < 0.05 && m_leplep>81 && m_leplep < 101',}
    elif ch=='elw' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==0  && mt_trigel_met > 60',}
    elif ch=='elwsr' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==0  && mt_trigel_met > 40 && !( m_trigelph1 > 76 && m_trigelph1 < 106 )',}
    elif ch=='elwsrtight' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==0  && mt_trigel_met > 80 && !( m_trigelph1 > 76 && m_trigelph1 < 106 )',}
    elif ch=='elwsrlowmt' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==0  && mt_trigel_met < 40 && !( m_trigelph1 > 76 && m_trigelph1 < 106 )',}
    elif ch == 'elwzcr' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==0  && m_trigelph1 > 76 && m_trigelph1 < 106 ',}
    elif ch == 'elwzcrloose' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==0  && m_trigelph1 > 50 && m_trigelph1 < 106 ',}
    elif ch == 'elwinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==1  && mt_trigel_met > 60 ',}
    elif ch == 'elwzcrinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==1  && m_trigelph1 > 76 && m_trigelph1 < 106 ',}
    elif ch == 'elwzcrlooseinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==1  && m_trigelph1 > 50 && m_trigelph1 < 106 ',}
    elif ch=='elwsrinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==1  && mt_trigel_met > 40 && !( m_trigelph1 > 76 && m_trigelph1 < 106 )',}
    elif ch=='elwsrtightinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==1  && mt_trigel_met > 80 && !( m_trigelph1 > 76 && m_trigelph1 < 106 )',}
    elif ch=='elwsrlowmtinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && mu_n==0 && ph_hasPixSeed[0]==1  && mt_trigel_met < 40 && !( m_trigelph1 > 76 && m_trigelph1 < 106 )',}
    elif ch=='muwjj_lowmjj' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && leadPhot_leadLepDR>0.4 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_lep_met > 30 && jet_n>1 && m_j_j > 200 && m_j_j < 400',}
    elif ch=='muwjj_highmjj' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && leadPhot_leadLepDR>0.4 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_lep_met > 30 && jet_n>1 && m_j_j > 400 ',}
    elif ch=='muzjj_highmjj' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && leadPhot_leadLepDR>0.4 && leadPhot_sublLepDR>0.4 && ph_HoverE12[0] < 0.05 && el_n==0 && m_leplep>70 && m_leplep < 110  && jet_n>1 && m_j_j > 400 ',}
    elif ch=='muzjj_lowmjj' :                                                      
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && mu_pt[0] > 20 && mu_pt[1] > 20 && ph_n==1 && ph_pt[0] > 25 && ph_IsEB[0] && m_leplep>70 && m_leplep<120 && dr_ph1_leadLep>0.5 && dr_ph1_sublLep>0.5 && m_j_j > 150 && m_j_j < 400',}

    return gg_cmds

def get_default_samples(ch='mu' ) :

    if ch.count('mu') :
        return { 'real' : {'Data' : 'Wgamma'}, 'fake' : {'Data' : 'Muon', 'Background' : 'RealPhotonsZg'}, 'target' : 'Muon' }
    elif ch.count('el') :
        return { 'real' : {'Data' : 'Wgamma'}, 'fake' : {'Data' : 'Muon', 'Background' : 'RealPhotonsZg'}, 'target' : 'Electron' }

def get_default_binning(var='sigmaIEIE') :

    if var == 'sigmaIEIE' :
        return { 'EB' : (30, 0, 0.03), 'EE' : (30, 0, 0.099) }
    elif var == 'chIsoCorr' :
        return { 'EB' : (30, 0, 45), 'EE' : (35, 0, 42) }
    elif var == 'neuIsoCorr' :
        return { 'EB' : (40, -2, 38), 'EE' : (30, -2, 43) }
    elif var == 'phoIsoCorr' :
        return { 'EB' : (53, -2.1, 35), 'EE' : (42, -2, 40) }

_sieie_cuts  = { 'Medium' : { 'EB' : 0.011, 'EE' : 0.033 },  'Tight' : { 'EB' : 0.011, 'EE' : 0.031 } }
_chIso_cuts  = { 'Medium' : { 'EB' : 1.5, 'EE' : 1.2 }    ,  'Tight' : { 'EB' : 0.7, 'EE' : 0.5 }     }
_neuIso_cuts = { 'Medium' : { 'EB' : 1.0, 'EE' : 1.5 }    ,  'Tight' : { 'EB' : 0.4, 'EE' : 1.5 }     }
_phoIso_cuts = { 'Medium' : { 'EB' : 0.7, 'EE' : 1.0 }    ,  'Tight' : { 'EB' : 0.5, 'EE' : 1.0 }     }

def get_default_cuts(var='sigmaIEIE', pid='Medium') :

    if var == 'sigmaIEIE' :

        return { 'EB' : { 'tight' : ( 0, _sieie_cuts[pid]['EB']-0.0001  ), 'loose' : ( _sieie_cuts[pid]['EB']+0.0001, 0.0299 ) },
                 'EE' : { 'tight' : ( 0, _sieie_cuts[pid]['EE']-0.0001 ), 'loose' : (  _sieie_cuts[pid]['EE']+0.0001, 0.066 ) } 
               }
    elif var == 'chIsoCorr' :
        return { 'EB' : { 'tight' : ( 0, _chIso_cuts[pid]['EB']-0.01 ), 'loose' : ( _chIso_cuts[pid]['EB']+0.01, 45 ) },
                 'EE' : { 'tight' : ( 0, _chIso_cuts[pid]['EE']-0.01 ), 'loose' : ( _chIso_cuts[pid]['EE']+0.01, 42 ) } 
               }
    elif var == 'neuIsoCorr' :
        return { 'EB' : { 'tight' : ( -2,_neuIso_cuts[pid]['EB']-0.01   ), 'loose' : ( _neuIso_cuts[pid]['EB']+0.01 , 40 ) },
                 'EE' : { 'tight' : ( -2,_neuIso_cuts[pid]['EE']-0.01   ), 'loose' : ( _neuIso_cuts[pid]['EE']+0.01 , 45 ) } 
               }
    elif var == 'phoIsoCorr' :
        return { 'EB' : { 'tight' : ( -2.1,_phoIso_cuts[pid]['EB']-0.001   ), 'loose' : (_phoIso_cuts[pid]['EB']+0.001  , 35 ) },
                 'EE' : { 'tight' : ( -2  ,_phoIso_cuts[pid]['EE']-0.001   ), 'loose' : (_phoIso_cuts[pid]['EE']+0.001  , 50 ) } 
               }


syst_uncertainties={}
def get_syst_uncertainty( type, reg, ptrange, real_fake, tight_loose ) :

    # Put these in by hand, may be necessary to load later
    if type.count( 'Background' ) :
        #use a flat 15% uncertainty for now
        return 0.15

    if not syst_uncertainties :
        print 'Systematics not loaded!  Use --syst_file to provide systematics file'
        return 0.0

    type_data = syst_uncertainties.get( type, None )
    if type_data is None :
        print 'no systematics available for %s' %type
        raw_input('con')
        return 0.0

    reg_data = type_data.get( reg, None )

    if reg_data is None :
        print 'No systematics available for region %s' %reg
        raw_input('con')
        return 0.0

    syst_ptrange = ( str(ptrange[0]), str(ptrange[1]) )
    if ptrange[0] is None :
        syst_ptrange = (None,None)
    elif ptrange[1] is None :
        syst_ptrange = (str(ptrange[0]), 'max')

    pt_data = reg_data.get(syst_ptrange, None)
    if pt_data is None :
        print 'No systematics available for pt range ', syst_ptrange
        raw_input('con')
        return 0.0

    return reg_data[syst_ptrange]

             
def main() :

    global sampManLG
    global sampManLLG
    global sampManFit

    base_dir_lg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_09_09/'
    base_dir_llg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_09_09/'
    fit_dir  = options.fitPath
    print fit_dir

    sampManLG    = SampleManager(base_dir_lg, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    sampManLLG   = SampleManager(base_dir_llg, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    sampManFit = SampleManager(fit_dir, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)


    if options.samplesConf is not None :

        sampManLG.ReadSamples( options.samplesConf )
        sampManLLG.ReadSamples( options.samplesConf )
        sampManFit.ReadSamples( options.samplesConf )

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

    #RunClosureFitting( outputDir = None )

    if options.syst_file is not None :
        load_syst_file( options.syst_file )

    RunNomFitting( outputDir = options.outputDir, ch=options.channel, fitvar=options.fitvar, pid=options.pid)

def load_syst_file( file ) :

    global syst_uncertainties

    ofile = open( file ) 
    syst_uncertainties = pickle.load(ofile)

    ofile.close()

def RunNomFitting( outputDir = None, ch='mu', fitvar=None, pid='Medium') :

    outputDirNom = None
    if outputDir is not None :
        if fitvar == 'sigmaIEIE' :
            outputDirNom = outputDir + '/SinglePhotonResults/SigmaIEIEFits/JetSinglePhotonFakeNomIso'
        elif fitvar == 'chIsoCorr' :
            outputDirNom = outputDir + '/SinglePhotonResults/ChHadIsoFits/JetSinglePhotonFakeNomIso'
        elif fitvar == 'neuIsoCorr' :
            outputDirNom = outputDir + '/SinglePhotonResults/NeuHadIsoFits/JetSinglePhotonFakeNomIso'
        elif fitvar == 'phoIsoCorr' :
            outputDirNom = outputDir + '/SinglePhotonResults/PhoIsoFits/JetSinglePhotonFakeNomIso'

    ptbins = [float(x) for x in options.ptbins.split(',') ]
    #eta_bins = {'EB' : [(0.00, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44)],
    #            'EE' : [(1.57, 2.10), (2.10, 2.20), (2.20, 2.40), (2.40, 2.50 ) ] }

    eta_bins = {'EB' : [(0.00, 1.44)],
                'EE' : [(1.57, 2.50 ) ] }


    if ch.count('mu') or ch =='elwzcrinvpixlead' :
        if fitvar == 'sigmaIEIE' :
            #iso_cuts_full = 'ph_n==1 && ph_passChIsoCorr%s[0] && ph_passNeuIsoCorr%s[0] && ph_passPhoIsoCorr%s[0] '%(pid,pid,pid)
            #iso_cuts_full = 'ph_n>0 && ph_passChIsoCorr%s[0] && ph_passNeuIsoCorr%s[0] && ph_passPhoIsoCorr%s[0] '%(pid,pid,pid)
            iso_cuts_full = 'ph_mediumNoSIEIENoEleVeto_n == 1 '
            #iso_cuts_full = 'ph_mediumNoSIEIE_n == 1 '
        elif fitvar == 'chIsoCorr' :
            #iso_cuts_full = 'ph_n==1 && ph_passSIEIE%s[0] && ph_passNeuIsoCorr%s[0] && ph_passPhoIsoCorr%s[0] '%(pid,pid,pid)
            iso_cuts_full = 'ph_mediumNoChIsoNoEleVeto_n == 1 '
        elif fitvar == 'neuIsoCorr' :
            #iso_cuts_full = 'ph_n==1 && ph_passChIsoCorr%s[0] && ph_passSIEIE%s[0] && ph_passPhoIsoCorr%s[0] '%(pid,pid,pid)
            iso_cuts_full = 'ph_mediumNoNeuIsoNoEleVeto_n == 1 '
        elif fitvar == 'phoIsoCorr' :
            #iso_cuts_full = 'ph_n==1 && ph_passChIsoCorr%s[0] && ph_passNeuIsoCorr%s[0] && ph_passSIEIE%s[0] '%(pid,pid,pid)
            iso_cuts_full = 'ph_mediumNoPhoIsoNoEleVeto_n == 1 '
    else :
        if fitvar == 'sigmaIEIE' :
            iso_cuts_full = 'ph_mediumNoSIEIE_n == 1 '
        elif fitvar == 'chIsoCorr' :
            iso_cuts_full = 'ph_mediumNoChIso_n == 1 '
        elif fitvar == 'neuIsoCorr' :
            iso_cuts_full = 'ph_mediumNoNeuIso_n == 1 '
        elif fitvar == 'phoIsoCorr' :
            iso_cuts_full = 'ph_mediumNoPhoIso_n == 1 '

    do_nominal_fit( iso_cuts_full, ptbins=ptbins, etabins=eta_bins, fitvar=fitvar, ch=ch,pid=pid, outputDir = outputDirNom, systematics='Nom')

    #iso_cuts = 'ph_chIsoCorr[0] < 8 && ph_neuIsoCorr[0] < 5 && ph_phoIsoCorr[0] < 5'
    #asym_cuts = [(5,3,3), (8,5,5), (10,7,7), (12,9,9), (15,11,11), (20, 16, 16) ]
    #for cuts in asym_cuts :
    #    iso_cuts = 'ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d' %cuts
    #    outputDirAsym=None
    #    if outputDir is not None :
    #        outputDirAsym = outputDir + '/SinglePhotonResults/JetSinglePhotonFakeAsymIso%d-%d-%d' %cuts

    #    do_nominal_fit( iso_cuts, ptbins=ptbins, ch=ch, outputDir = outputDirAsym, systematics='Nom', iso_cuts_data=iso_cuts)


def do_nominal_fit( iso_cuts, ptbins=[], subl_ptrange=(None,None), etabins={}, fitvar='sigmaIEIE', ch='mu', pid='Medium', outputDir=None, systematics=None, iso_cuts_data=None ) :

    binning = get_default_binning(var=fitvar)
    samples = get_default_samples(ch)

    eta_binning = {'EB' : ( 144, 0, 1.44), 'EE' : ( 93, 1.57, 2.50 ) }

    # generate templates for both EB and EE
    real_template_str = get_real_template_draw_commands(ch ) + ' && %s' %iso_cuts
    #fake_template_str = get_fake_window_template_draw_commands(ch )
    fake_template_str = get_fake_template_draw_commands(ch )  + ' && %s' %iso_cuts

    templates_reg = {}
    templates_reg['EB'] = {}
    templates_reg['EE'] = {}
    templates_reg['EB']['real'] = get_single_photon_template(real_template_str, binning['EB'], samples['real'], 'EB', sampMan=sampManLG , fitvar=fitvar)
    templates_reg['EE']['real'] = get_single_photon_template(real_template_str, binning['EE'], samples['real'], 'EE', sampMan=sampManLG , fitvar=fitvar)
    templates_reg['EB']['fake'] = get_single_photon_template(fake_template_str, binning['EB'], samples['fake'], 'EB', sampMan=sampManLLG, fitvar=fitvar)
    templates_reg['EE']['fake'] = get_single_photon_template(fake_template_str, binning['EE'], samples['fake'], 'EE', sampMan=sampManLLG, fitvar=fitvar)

    #---------------------------------------
    # make finer binned templates in eta
    #---------------------------------------
    templates_eta = {}
    for reg, bins in etabins.iteritems() :
        for etamin, etamax in bins :
            etabin = ('%.2f' %etamin, '%.2f'%etamax)
            templates_eta.setdefault( etabin, {} )
            real_template_str_eta = real_template_str + ' && fabs(ph_eta[0]) > %f && fabs(ph_eta[0] ) < %f ' %( etamin, etamax )
            fake_template_str_eta = fake_template_str + ' && fabs(ph_eta[0]) > %f && fabs(ph_eta[0] ) < %f ' %( etamin, etamax )

            templates_eta[etabin]['real'] = get_single_photon_template( real_template_str_eta, binning[reg], samples['real'], reg, sampMan=sampManLG, fitvar=fitvar )
            templates_eta[etabin]['fake'] = get_single_photon_template( fake_template_str_eta, binning[reg], samples['fake'], reg, sampMan=sampManLLG, fitvar=fitvar )


    regions = [ 'EB', 'EE' ]
    for reg in regions :

        # convert from regions to lead/subl
        templates = {}
        templates['lead'] = {}
        templates['lead']['real'] = templates_reg[reg]['real']
        templates['lead']['fake'] = templates_reg[reg]['fake']

        # add regions onto the selection
        gg_selection = get_default_draw_commands(ch)['gg'] + ' && %s && ph_Is%s[0]' %( iso_cuts, reg)
        #gg_selection = get_default_draw_commands(ch)['gg'] + ' && ph_n > 0 && ph_Is%s[0]' %( reg)
        #if iso_cuts_data is not None :
        #    gg_selection = gg_selection + ' && %s ' %( iso_cuts_data )
        #elif iso_cuts is not None :
        #    gg_selection = gg_selection + ' && %s ' %( iso_cuts )

        # parse out the x and y binning
        varbinn = binning[reg]

        # variable given to TTree.Draw
        var = 'fabs(ph_eta[0]):ph_pt[0]:ph_%s[0]'%fitvar #z:y:x

        # get sample
        target_samp = sampManFit.get_samples(name=samples['target'])

        # draw and get back the hist
        gg_hist = clone_sample_and_draw( target_samp[0], var, gg_selection, ( varbinn[0], varbinn[1], varbinn[2], 40, 0, 200, eta_binning[reg][0], eta_binning[reg][1], eta_binning[reg][2]), sampMan=sampManFit )

        # -----------------------
        # inclusive result
        # -----------------------

        # project data hist
        gg_hist_inclusive = gg_hist.ProjectionX( 'px' )

        templates_inclusive = get_projected_templates( templates, lead_ptrange =(None,None) )

        (results_inclusive_stat, results_inclusive_syst) = run_photon_fit(templates_inclusive, gg_hist_inclusive, reg, fitvar=fitvar, pid=pid, lead_ptrange=(None,None), outputDir=outputDir, outputPrefix='__%s'%ch, systematics=systematics )

        namePostfix = '__%s__%s' %( ch, reg )
        save_templates( templates_inclusive, outputDir, lead_ptrange=(None,None), namePostfix=namePostfix )
        save_results( results_inclusive_stat, outputDir, namePostfix )

        namePostfix_syst = '__syst%s' %namePostfix
        save_results( results_inclusive_syst, outputDir, namePostfix_syst )

        # -----------------------
        # pt binned results
        # -----------------------
        for idx, ptmin in enumerate(ptbins[:-1] ) :
            ptmax = ptbins[idx+1]

            # put lead range together (expected by following code)
            if ptmax == ptbins[-1] : 
                # if we're in the last bin, move the min pt down one
                lead_ptrange_templates = ( ptbins[idx-1], None )
                lead_ptrange = ( ptmin, None )
            else :
                lead_ptrange = ( ptmin, ptmax )
                lead_ptrange_templates = ( ptmin, ptmax )

            print 'ptmin = %d, ptmax = %d, Min Z bin = %d, max Z bin = %d' %( ptmin, ptmax, gg_hist.GetZaxis().FindBin( ptmin), gg_hist.GetZaxis().FindBin( ptmax )-1 )

            # project data hist
            gg_hist_pt = gg_hist.ProjectionX( 'px_%d_%d' %( ptmin, ptmax), gg_hist.GetYaxis().FindBin( ptmin), gg_hist.GetYaxis().FindBin( ptmax )-1, 0, -1 )
                
            # get templates
            # if in the last pt bin, use the 
            # second to last template
            templates_pt = get_projected_templates( templates, lead_ptrange=lead_ptrange_templates ) 

            #if ptmax == ptbins[-1] :
            #    templates_pt_prev = get_projected_templates( templates, lead_ptrange=(ptbins[idx-1], ptbins[idx] ) )
            #    for key, val in templates_pt_prev['lead']['fake'].iteritems() :
            #        templates_pt['lead']['fake'][key] = val

            # get results
            (results_pt_stat, results_pt_syst) = run_photon_fit(templates_pt, gg_hist_pt, reg, fitvar=fitvar, pid=pid, lead_ptrange=lead_ptrange, outputDir=outputDir, outputPrefix='__%s' %ch, systematics=systematics )

            namePostfix = '__%s__%s' %( ch, reg )
            if lead_ptrange[0] is not None :
                if lead_ptrange[1] is None :
                    namePostfix += '__pt_%d-max' %lead_ptrange[0]
                else :
                    namePostfix += '__pt_%d-%d' %(lead_ptrange[0], lead_ptrange[1] )

            save_templates( templates_pt, outputDir, lead_ptrange=lead_ptrange, namePostfix=namePostfix )
            save_results( results_pt_stat, outputDir, namePostfix )

            namePostfix_syst = '__syst%s' %namePostfix

            save_results( results_pt_syst, outputDir, namePostfix_syst )

            # -----------------------
            # eta binned results
            # -----------------------
            for etamin, etamax in etabins[reg] :
                etabin = ('%.2f' %etamin, '%.2f'%etamax)

                templates_etabin = {}
                templates_etabin['lead'] = {}
                templates_etabin['lead']['real'] = templates_eta[etabin]['real']
                templates_etabin['lead']['fake'] = templates_eta[etabin]['fake']

                gg_hist_pt_eta = gg_hist.ProjectionX( 'px_%d_%d' %( ptmin, ptmax), gg_hist.GetYaxis().FindBin( ptmin), gg_hist.GetYaxis().FindBin( ptmax )-1, 
                                                                                   gg_hist.GetZaxis().FindBin( etamin), gg_hist.GetZaxis().FindBin( etamax )-1 )

                templates_pt_eta = get_projected_templates( templates_etabin, lead_ptrange=lead_ptrange_templates ) 

                (results_pt_eta_stat, results_pt_eta_syst) = run_photon_fit(templates_pt_eta, gg_hist_pt_eta, reg, fitvar=fitvar, pid=pid, lead_ptrange=lead_ptrange, outputDir=outputDir, outputPrefix='__%s' %ch, systematics=systematics )

                namePostfix = '__%s__%s-%s' %( ch, etabin[0], etabin[1] )
                if lead_ptrange[0] is not None :
                    if lead_ptrange[1] is None :
                        namePostfix += '__pt_%d-max' %lead_ptrange[0]
                    else :
                        namePostfix += '__pt_%d-%d' %(lead_ptrange[0], lead_ptrange[1] )

                save_templates( templates_pt_eta, outputDir, lead_ptrange=lead_ptrange, namePostfix=namePostfix )
                save_results( results_pt_eta_stat, outputDir, namePostfix )

                namePostfix_syst = '__syst%s' %namePostfix

                save_results( results_pt_eta_syst, outputDir, namePostfix_syst )

def get_projected_templates( templates, lead_ptrange=(None,None) ) :

    templates_proj = {}
    templates_proj['lead'] = {}

    # project in a range
    if lead_ptrange[0] is not None :
        for rf, hist_entries in templates['lead'].iteritems() :
            templates_proj['lead'][rf] = {}
            for hist_type, hist in hist_entries.iteritems() : 
                if hist is None :
                    templates_proj['lead'][rf][hist_type] = None
                else :
                    if lead_ptrange[1] is None :
                        templates_proj['lead'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_%d-max' %( lead_ptrange[0] ), hist.GetYaxis().FindBin( lead_ptrange[0] ) )
                    else :
                        templates_proj['lead'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_%d-%d' %( lead_ptrange[0], lead_ptrange[1] ), hist.GetYaxis().FindBin( lead_ptrange[0] ), hist.GetYaxis().FindBin( lead_ptrange[1] )-1 )

    else : # project inclusive
        for rf, hist_entries in templates['lead'].iteritems() :
            templates_proj['lead'][rf] = {}
            for hist_type, hist in hist_entries.iteritems() : 
                if hist is not None :
                    templates_proj['lead'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_inclusive' )
                else :
                    templates_proj['lead'][rf][hist_type] = None

    return templates_proj


def run_photon_fit( templates, gg_hist, lead_reg, fitvar='sigmaIEIE', pid='Medium', lead_ptrange=(None,None), outputDir=None, outputPrefix='', systematics=None ) :

    accept_reg = ['EB', 'EE']
    if lead_reg not in accept_reg :
        print 'Lead region does not make sense'
        return

    # get the defaults
    samples = get_default_samples()
    plotbinning = get_default_binning(var=fitvar)
    cuts = get_default_cuts(var=fitvar, pid=pid)

    # Find the bins corresponding to the cuts
    # lead photon on X axis, subl on Y axis
    bins_lead_tight = ( gg_hist.GetXaxis().FindBin( cuts[lead_reg]['tight'][0] ), gg_hist.GetXaxis().FindBin( cuts[lead_reg]['tight'][1] ) )
    bins_lead_loose = ( gg_hist.GetXaxis().FindBin( cuts[lead_reg]['loose'][0] ), gg_hist.GetXaxis().FindBin( cuts[lead_reg]['loose'][1] ) )

    print 'cuts, bins lead, tight = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['tight'][0], cuts[lead_reg]['tight'][1], bins_lead_tight[0], bins_lead_tight[1] )
    print 'cuts, bins lead, loose = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['loose'][0], cuts[lead_reg]['loose'][1], bins_lead_loose[0], bins_lead_loose[1] )

    # Integrate to the the data in the four regions
    Ndata_T = gg_hist.Integral( bins_lead_tight[0], bins_lead_tight[1])
    Ndata_L = gg_hist.Integral( bins_lead_loose[0], bins_lead_loose[1])

    # ufloat it!
    Ndata = {}
    Ndata['T'] = ufloat( Ndata_T, math.sqrt(Ndata_T ), 'Ndata_T' )
    Ndata['L'] = ufloat( Ndata_L, math.sqrt(Ndata_L ), 'Ndata_L' )

    print 'N data T = ', Ndata['T']
    print 'N data L = ', Ndata['L']

    # arragnge the cuts by 
    eff_cuts = {}
    eff_cuts['lead'] = {}
    eff_cuts['lead']['tight'] = cuts[lead_reg]['tight']
    eff_cuts['lead']['loose'] = cuts[lead_reg]['loose']

    # get 2-d efficiencies from 1-d inputs
    (eff_1d_stat, eff_1d_syst) =generate_1d_efficiencies( templates, eff_cuts, lead_reg, lead_ptrange,  systematics=systematics )

    print 'eff_1d'
    print eff_1d_stat

    results_stat = run_fit( {'T': Ndata['T'], 'L' : Ndata['L']}, eff_1d_stat )
    results_syst = run_fit( {'T': Ndata['T'], 'L' : Ndata['L']}, eff_1d_syst )

    print 'Real Norm = ', results_stat.item(0)
    print 'Fake Norm = ', results_stat.item(1)

    hist_temp_lead_real = templates['lead']['real']['Data'].Clone( 'hist_temp_lead_real' )
    hist_temp_lead_fake = templates['lead']['fake']['Data'].Clone( 'hist_temp_lead_fake' )

    if templates['lead']['real']['Background'] is not None :
        hist_temp_lead_real.Add( templates['lead']['real']['Background'] )
    if templates['lead']['fake']['Background'] is not None :
        hist_temp_lead_fake.Add( templates['lead']['fake']['Background'] )

    p_R_T = results_stat.item(0)*eff_1d_stat['eff_R_T_lead']
    p_R_L = results_stat.item(0)*eff_1d_stat['eff_R_L_lead']
    p_F_T = results_stat.item(1)*eff_1d_stat['eff_F_T_lead']
    p_F_L = results_stat.item(1)*eff_1d_stat['eff_F_L_lead']

    print 'nPred Real Tight = ', p_R_T
    print 'nPred Real Loose = ', p_R_L
    print 'nPred Fake Tight = ', p_F_T
    print 'nPred Fake Loose = ', p_F_L
    
    #normalize lead real template according to fit
    hist_temp_lead_real.Scale( ( p_R_T+p_R_L ).n/ hist_temp_lead_real.Integral() )
    hist_temp_lead_fake.Scale( ( p_F_T+p_F_L ).n/ hist_temp_lead_fake.Integral() )

    hist_temp_lead_real.SetLineColor(ROOT.kMagenta)
    hist_temp_lead_real.SetMarkerColor(ROOT.kMagenta)
    hist_temp_lead_real.SetLineWidth(2)

    hist_temp_lead_fake.SetLineColor(ROOT.kRed)
    hist_temp_lead_fake.SetMarkerColor(ROOT.kRed)
    hist_temp_lead_fake.SetLineWidth(2)

    hist_temp_lead_real.SetStats(0)
    hist_temp_lead_fake.SetStats(0)

    can_proj_lead = ROOT.TCanvas('proj_lead', '')

    namePostfix = '__%s' %( lead_reg )
    if lead_ptrange[0] is not None :
        if lead_ptrange[1] is None :
            namePostfix += '__pt_%d-max' %( lead_ptrange[0])
        else :
            namePostfix += '__pt_%d-%d' %( lead_ptrange[0], lead_ptrange[1])

    outputNamePL=None
    if outputDir is not None :
        outputNamePL = outputDir + '/fit_with_data_projlead%s%s.pdf' %(outputPrefix, namePostfix)

    if lead_reg == 'EE' :
        gg_hist.Rebin(10)
        hist_temp_lead_real.Rebin(10)
        hist_temp_lead_fake.Rebin(10)

    draw_template(can_proj_lead, [gg_hist, hist_temp_lead_real, hist_temp_lead_fake], sampManFit, normalize=False, first_hist_is_data=True, legend_entries=['Data', 'real+fake prediction', 'fake+fake prediction' ], outputName=outputNamePL )

    text_results_stat = collect_results( results_stat, Ndata, eff_1d_stat, templates, bins_lead_loose, bins_lead_tight )
    text_results_syst = collect_results( results_syst, Ndata, eff_1d_stat, templates, bins_lead_loose, bins_lead_tight )

    return text_results_stat, text_results_syst
    
def run_fit( data, efficiencies ) :

    # make the matrix
    matrix = generate_eff_matrix( efficiencies )
    print matrix

    #do the fit!  Invert the matrix and multiply the by counts vectors
    results = solve_matrix_eq( matrix, [data['T'], data['L']] )

    return results 

def collect_results( results, data, efficiencies, templates, bins_lead_loose, bins_lead_tight ) :

    text_results = collections.OrderedDict()

    for key, val in efficiencies.iteritems() :
        text_results[key] = val

    text_results['Ndata_T'] = data['T']
    text_results['Ndata_L'] = data['L']

    text_results['alpha_R'] = results.item(0)
    text_results['alpha_F'] = results.item(1)

    text_results['Npred_R_T'] = text_results['alpha_R']*text_results['eff_R_T_lead']
    text_results['Npred_R_L'] = text_results['alpha_R']*text_results['eff_R_L_lead']

    text_results['Npred_F_T'] = text_results['alpha_F']*text_results['eff_F_T_lead']
    text_results['Npred_F_L'] = text_results['alpha_F']*text_results['eff_F_L_lead']

    int_lead_real_loose = get_integral_and_error(templates['lead']['real']['Data'], bins_lead_loose )
    int_lead_real_tight = get_integral_and_error(templates['lead']['real']['Data'], bins_lead_tight )
    int_lead_fake_loose = get_integral_and_error(templates['lead']['fake']['Data'], bins_lead_loose )
    int_lead_fake_tight = get_integral_and_error(templates['lead']['fake']['Data'], bins_lead_tight )


    if templates['lead']['real']['Background'] is not None :
        int_lead_real_loose = int_lead_real_loose +  get_integral_and_error(templates['lead']['real']['Background'], bins_lead_loose )
    if templates['lead']['real']['Background'] is not None :
        int_lead_real_tight = int_lead_real_tight +  get_integral_and_error(templates['lead']['real']['Background'], bins_lead_tight )
    if templates['lead']['fake']['Background'] is not None :
        int_lead_fake_loose = int_lead_fake_loose +  get_integral_and_error(templates['lead']['fake']['Background'], bins_lead_loose )
    if templates['lead']['fake']['Background'] is not None :
        int_lead_fake_tight = int_lead_fake_tight +  get_integral_and_error(templates['lead']['fake']['Background'], bins_lead_tight )

    text_results['template_int_lead_real_loose'] = int_lead_real_loose
    text_results['template_int_lead_real_tight'] = int_lead_real_tight
    text_results['template_int_lead_fake_loose'] = int_lead_fake_loose
    text_results['template_int_lead_fake_tight'] = int_lead_fake_tight

    return text_results


def generate_1d_efficiencies( templates, cuts, lead_reg, lead_ptrange, systematics=None ) :

    (int_stat, int_syst) = get_template_integrals( templates, cuts, lead_reg, lead_ptrange, systematics=systematics )

    print 'Template integral'
    print int_stat

    (eff_1d_stat, eff_1d_syst) = get_1d_loose_efficiencies( int_stat, int_syst, lead_reg, lead_ptrange, systematics=systematics )

    return eff_1d_stat, eff_1d_syst

def get_1d_loose_efficiencies( int_stat, int_syst, lead_reg, lead_ptrange, systematics=None) :

    eff_stat = {}
    eff_syst = {}

    if int_stat['lead']['real']['loose'].n == 0 :
        eff_stat['eff_R_T_lead'] = ufloat( 1.0, int_stat['lead']['real']['tight'].s/int_stat['lead']['real']['tight'].n )
    else :
        eff_stat['eff_R_T_lead'] = int_stat['lead']['real']['tight'] / (int_stat['lead']['real']['tight']+int_stat['lead']['real']['loose'])
    eff_stat['eff_F_T_lead'] = int_stat['lead']['fake']['tight'] / (int_stat['lead']['fake']['tight']+int_stat['lead']['fake']['loose'])
    eff_stat['eff_R_L_lead'] = int_stat['lead']['real']['loose'] / (int_stat['lead']['real']['tight']+int_stat['lead']['real']['loose'])
    eff_stat['eff_F_L_lead'] = int_stat['lead']['fake']['loose'] / (int_stat['lead']['fake']['tight']+int_stat['lead']['fake']['loose'])

    eff_syst['eff_R_T_lead'] = int_syst['lead']['real']['tight'] / (int_syst['lead']['real']['tight']+int_syst['lead']['real']['loose'])
    eff_syst['eff_F_T_lead'] = int_syst['lead']['fake']['tight'] / (int_syst['lead']['fake']['tight']+int_syst['lead']['fake']['loose'])
    eff_syst['eff_R_L_lead'] = int_syst['lead']['real']['loose'] / (int_syst['lead']['real']['tight']+int_syst['lead']['real']['loose'])
    eff_syst['eff_F_L_lead'] = int_syst['lead']['fake']['loose'] / (int_syst['lead']['fake']['tight']+int_syst['lead']['fake']['loose'])


    # Do systematics
    # the integrals may already have some systematics
    # that are propagated to the eff_*
    # therefore, don't overwrite the existing 
    # systematics, but make a ufloat with a
    # zero value, and non-zero syst
    eff_syst['eff_R_L_lead'] = eff_syst['eff_R_L_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_R_L_lead'].n)*get_syst_uncertainty( 'RealTemplateNom', lead_reg, lead_ptrange, 'real', 'loose' ), 'Template_lead_real_loose')
    eff_syst['eff_F_L_lead'] = eff_syst['eff_F_L_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_F_L_lead'].n)*get_syst_uncertainty( 'FakeTemplate%s'%systematics, lead_reg, lead_ptrange, 'fake', 'loose' ), 'Template_lead_fake_loose' )
    eff_syst['eff_R_T_lead'] = eff_syst['eff_R_T_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_R_T_lead'].n)*get_syst_uncertainty( 'RealTemplateNom', lead_reg, lead_ptrange, 'real', 'loose' ), 'Template_lead_real_loose')
    eff_syst['eff_F_T_lead'] = eff_syst['eff_F_T_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_F_T_lead'].n)*get_syst_uncertainty( 'FakeTemplate%s'%systematics, lead_reg, lead_ptrange, 'fake', 'loose' ), 'Template_lead_fake_loose' )

    return eff_stat, eff_syst

def get_template_integrals( templates, cuts, lead_reg, lead_ptrange, systematics=None) :

    int_stat = {}
    int_stat['lead']={}
    int_stat['lead']['real']={}
    int_stat['lead']['fake']={}

    int_syst = {}
    int_syst['lead']={}
    int_syst['lead']['real']={}
    int_syst['lead']['fake']={}

    bins_lead_real_tight = ( templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][0] ), templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][1] ) )
    bins_lead_real_loose = ( templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][0] ), templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][1] ) )
    bins_lead_fake_tight = ( templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][0] ), templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][1] ) )
    bins_lead_fake_loose = ( templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][0] ), templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][1] ) )

    int_stat['lead']['real']['tight'] = get_integral_and_error( templates['lead']['real']['Data'], bins_lead_real_tight, 'Data_lead_real_tight' )
    int_stat['lead']['real']['loose'] = get_integral_and_error( templates['lead']['real']['Data'], bins_lead_real_loose, 'Data_lead_real_loose' )
    int_stat['lead']['fake']['tight'] = get_integral_and_error( templates['lead']['fake']['Data'], bins_lead_fake_tight, 'Data_lead_fake_tight' )
    int_stat['lead']['fake']['loose'] = get_integral_and_error( templates['lead']['fake']['Data'], bins_lead_fake_loose, 'Data_lead_fake_loose' )

    # If running with systematics, set the data systs to zero
    # May need to implement non-zero systematics for data in the future
    # The overall template systematics should not be set here
    int_syst['lead']['real']['tight'] = ufloat(int_stat['lead']['real']['tight'].n, 0.0 , 'Data_lead_real_tight' )
    int_syst['lead']['real']['loose'] = ufloat(int_stat['lead']['real']['loose'].n, 0.0 , 'Data_lead_real_loose' )
    int_syst['lead']['fake']['tight'] = ufloat(int_stat['lead']['fake']['tight'].n, 0.0 , 'Data_lead_fake_tight' )
    int_syst['lead']['fake']['loose'] = ufloat(int_stat['lead']['fake']['loose'].n, 0.0 , 'Data_lead_fake_loose' )

    # Subtract background

    if templates['lead']['real']['Background'] is not None :
        bkg_int_tight = get_integral_and_error( templates['lead']['real']['Background'], bins_lead_real_tight, 'Background_lead_real_tight' )
        bkg_int_loose = get_integral_and_error( templates['lead']['real']['Background'], bins_lead_real_loose, 'Background_lead_real_loose'  ) 

        syst_bkg_int_tight = ufloat( bkg_int_tight.n, math.fabs(bkg_int_tight.n)*get_syst_uncertainty('Background%s'%systematics , lead_reg, lead_ptrange, 'real', 'tight' ), 'Background_lead_real_tight' )
        syst_bkg_int_loose = ufloat( bkg_int_loose.n, math.fabs(bkg_int_loose.n)*get_syst_uncertainty( 'Background%s'%systematics, lead_reg , lead_ptrange, 'real', 'loose'), 'Background_lead_real_loose' )


        int_stat['lead']['real']['tight'] = int_stat['lead']['real']['tight'] + bkg_int_tight
        int_stat['lead']['real']['loose'] = int_stat['lead']['real']['loose'] + bkg_int_loose

        int_syst['lead']['real']['tight'] = int_syst['lead']['real']['tight'] + syst_bkg_int_tight
        int_syst['lead']['real']['loose'] = int_syst['lead']['real']['loose'] + syst_bkg_int_loose


    if templates['lead']['fake']['Background'] is not None :
        bkg_int_tight = get_integral_and_error( templates['lead']['fake']['Background'], bins_lead_fake_tight, 'Background_lead_fake_tight'  ) 
        bkg_int_loose = get_integral_and_error( templates['lead']['fake']['Background'], bins_lead_fake_loose, 'Background_lead_fake_loose'  ) 

        syst_bkg_int_tight = ufloat( bkg_int_tight.n, math.fabs(bkg_int_tight.n)*get_syst_uncertainty( 'Background%s'%systematics, lead_reg , lead_ptrange, 'fake', 'tight'), 'Background_lead_fake_tight' )
        syst_bkg_int_loose = ufloat( bkg_int_loose.n, math.fabs(bkg_int_loose.n)*get_syst_uncertainty( 'Background%s'%systematics, lead_reg , lead_ptrange, 'fake', 'loose'), 'Background_lead_fake_loose' )

        int_stat['lead']['fake']['tight'] = int_stat['lead']['fake']['tight'] + bkg_int_tight
        int_stat['lead']['fake']['loose'] = int_stat['lead']['fake']['loose'] + bkg_int_loose

        int_syst['lead']['fake']['tight'] = int_syst['lead']['fake']['tight'] + syst_bkg_int_tight
        int_syst['lead']['fake']['loose'] = int_syst['lead']['fake']['loose'] + syst_bkg_int_loose

    return int_stat, int_syst

def get_integral_and_error( hist, bins=None, name='' ) :

    err = ROOT.Double()
    if bins is None :
        val = hist.IntegralAndError( 1, hist.GetNbinsX(), err )
    else :
        if bins[1] is None :
            val = hist.IntegralAndError( bins[0], hist.GetNbinsX(), err )
        else :
            val = hist.IntegralAndError( bins[0], bins[1], err )

    return ufloat( val, err, name )


def get_single_photon_template( selection, binning, sample, reg, sampMan, fitvar='sigmaIEIE') :

    if reg not in ['EB', 'EE'] :
        print 'Region not specified correctly'
        return None

    var = 'ph_pt[0]:ph_%s[0]' %fitvar#y:x

    selection = selection + ' && ph_Is%s[0] ' %( reg )

    data_samp_name = sample['Data']
    bkg_samp_name  = sample.get('Background', None)

    template_hists = {}

    data_samp = sampMan.get_samples(name=data_samp_name )

    if data_samp :
        template_hists['Data'] = clone_sample_and_draw( data_samp[0], var, selection, ( binning[0], binning[1], binning[2],100, 0, 500  ), sampMan=sampMan ) 
    else :
        print 'Data template sample not found!'
        
    if bkg_samp_name is not None :
        bkg_samp = sampMan.get_samples(name=bkg_samp_name )
        var_bkg = 'ph_pt[0]:ph_%s[0]'%fitvar #y:x

        if bkg_samp :
            template_hists['Background'] = clone_sample_and_draw( bkg_samp[0], var_bkg, selection, ( binning[0], binning[1], binning[2],100, 0, 500  ), sampMan=sampMan ) 
        else :
            print 'Background template sample not found!'
    else :
        template_hists['Background']=None

    return template_hists

def generate_eff_matrix( eff_dic ) :

    eff_matrix = [ [ eff_dic['eff_R_T_lead'], eff_dic['eff_F_T_lead'] ],
                   [ eff_dic['eff_R_L_lead'], eff_dic['eff_F_L_lead'] ] ]
    
    return eff_matrix


def solve_matrix_eq( matrix_ntries, vector_entries ) :

    ms = []
    mn = []
    for row in matrix_ntries :
        ms_row = []
        mn_row = []
        for col in row :
            ms_row.append( col.s )
            mn_row.append( col.n )
        ms.append( ms_row )
        mn.append( mn_row )

    matrix = unumpy.umatrix( mn, ms )

    print matrix

    vs = []
    vn = []
    for row in vector_entries :
        vn.append( [ row.n ] )
        vs.append( [ row.s ] )

    vector = unumpy.umatrix( vn, vs )
    
    inv_matrix = None
    try :
        inv_matrix = matrix.getI()
    except :
        print 'Failed to invert matrix, aborting'
        return unumpy.umatrix( [0.0, 0.0], [0.0, 0.0] )

    print inv_matrix
    print vector

    return inv_matrix*vector

def clone_sample_and_draw( samp, var, sel, binning, sampMan ) :

    newSamp = sampMan.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

def save_templates( templates, outputDir, lead_ptrange=(None,None), namePostfix='' ) :

    if outputDir is None :
        return

    draw_templates = {'lead' : {}, 'subl' : {} }

    draw_templates['lead']['real'] = templates['lead']['real']['Data'].Clone( 'draw_%s' %templates['lead']['real']['Data'].GetName())
    draw_templates['lead']['fake'] = templates['lead']['fake']['Data'].Clone( 'draw_%s' %templates['lead']['fake']['Data'].GetName())

    if templates['lead']['real']['Background'] is not None :
        draw_templates['lead']['real'].Add( templates['lead']['real']['Background'])
    if templates['lead']['fake']['Background'] is not None :
        draw_templates['lead']['fake'].Add( templates['lead']['fake']['Background'])

    can_lead_real = ROOT.TCanvas('can_lead_real', '')
    can_lead_fake = ROOT.TCanvas('can_lead_fake', '')

    pt_label_lead = None
    if lead_ptrange[0] is not None :
        if lead_ptrange[1] == None :
            pt_label_lead = ' p_{T} > %d ' %( lead_ptrange[0] )
        else :
            pt_label_lead = ' %d < p_{T} < %d ' %( lead_ptrange[0], lead_ptrange[1] )

    draw_template( can_lead_real, draw_templates['lead']['real'], sampManFit, normalize=1, label=pt_label_lead, outputName = outputDir+'/template_lead_real%s.pdf' %namePostfix )
    draw_template( can_lead_fake, draw_templates['lead']['fake'], sampManFit, normalize=1, label=pt_label_lead, outputName = outputDir+'/template_lead_fake%s.pdf' %namePostfix )


def save_results( results, outputDir, namePostfix='' ) :

    if outputDir is None :
        return

    fname = outputDir + '/results%s.pickle' %namePostfix

    if not os.path.isdir( os.path.dirname( fname ) ) :
        os.makedirs( os.path.dirname( fname ) )
    file = open( fname, 'w' )
    pickle.dump( results, file )
    file.close()

main()
