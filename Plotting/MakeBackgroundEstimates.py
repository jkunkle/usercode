"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
import sys
import os
import re
import math
import uuid
import copy
import pickle
import imp
import ROOT
from array import array
from uncertainties import ufloat
import blue

import collections

from SampleManager import SampleManager
from FakeFactorManager import FakeFactorManager

samplesWelgg = None
samplesWmugg = None
samplesWggInvSubl = None
samplesWggInvLead = None

ROOT.gROOT.SetBatch(True)

ph_cuts = ''
lead_dr_cut = 0.4
subl_dr_cut = 0.4
phot_dr_cut = 0.4
_mgg_cut = 0

_asym_iso_syst = { (0, 0, 0) : 0.0, (5,3,3) : 0.10, (8,5,5) : 0.15, (10, 7, 7) : 0.20, (12, 9, 9) : 0.25, (15,11,11) : 0.30, (20, 16, 16) : 0.5 }

#_ele_eta_bins        = {'EB': [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44) ], 'EE' : [(1.57, 2.1), (2.1, 2.2), (2.2, 2.4), (2.4, 2.5)] }
#_ele_eta_bins_highpt = {'EB': [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44) ], 'EE' : [(1.57, 2.1), (2.1, 2.2), (2.2, 2.4), (2.4, 2.5)] }

_ele_eta_bins_coarse = {'EB': [(0.0, 1.44) ], 'EE' : [(1.57, 2.5)] }

_ele_eta_bins = _ele_eta_bins_coarse
_ele_eta_bins_highpt = _ele_eta_bins_coarse

_fakefactor_closure_syst = 0.1

_eta_pt_bin_map = { }
_eta_pt_bin_map_coarse = { }

def main() :

    p = ArgumentParser()
    
    p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
    p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',  required=False,       help='Input directory base')
    p.add_argument('--plotDir',     default='Plots',  type=str ,        dest='plotDir',  required=False,       help='Directory where plots are written')
    p.add_argument('--ptbins',     default='15,25,40,70,1000000',  type=str ,        dest='ptbins',  required=False,       help='PT bins to use')
    p.add_argument('--sublptbins',     default=None,  type=str ,        dest='sublptbins',  required=False,       help='subl PT bins to use')
    p.add_argument('--zgg',        default=False,  action='store_true' ,        dest='zgg',  required=False,       help='do Zgg')
    
    options = p.parse_args()

    ptmin = int(options.ptbins.split(',')[0])

   # print '**************************LOOSE ELE INV CUTS************************'
    global el_cuts
    #el_base = 'el_passtrig_n==1 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_trigEle>%f && dr_ph2_trigEle>%f && m_ph1_ph2>%.1f && pt_leadph12 > %d && pt_sublph12 > %d %s ' %(lead_dr_cut, subl_dr_cut, _mgg_cut, ptmin, ptmin, ph_cuts)
    el_base = 'el_passtrig_n>0 && el_n==1 && mu_n==0 && dr_ph1_ph2>0.4 && m_ph1_ph2>%.1f && dr_ph1_trigEle>%f && dr_ph2_trigEle>%f && pt_leadph12 > %d && pt_sublph12 > %d %s ' %(_mgg_cut, lead_dr_cut, subl_dr_cut, ptmin, ptmin, ph_cuts)
    #el_base_inv = 'el_passtrig_n>0 && el_n==2 && mu_n==0 && dr_ph1_ph2>0.4 && m_ph1_ph2>%.1f  && dr_ph1_trigEle>%f && dr_ph2_trigEle>%f && pt_leadph12 > %d && pt_sublph12 > %d %s ' %(_mgg_cut, lead_dr_cut, subl_dr_cut, ptmin, ptmin, ph_cuts)
    el_base_inv = el_base
    #el_base = 'pt_leadph12 > %d && pt_sublph12 > %d %s ' %(ptmin, ptmin, ph_cuts)

    zmasscut = 5
    el_cuts = {'elfull' : 
                el_base + ' && !(fabs(m_trigelphph-91.2) < %d) && !(fabs(m_trigelph1-91.2) < %d)  && !(fabs(m_trigelph2-91.2) < %d) ' %(zmasscut,zmasscut,zmasscut),
               'elloose' :
                el_base,
               'elzcr' :
                el_base + ' && (fabs(m_trigelphph-91.2) < %d) ' %zmasscut,
               'elph1zcr' :
                el_base + ' && (fabs(m_trigelph1-91.2) < %d) '%zmasscut,
               'elph2zcr' :
                el_base + ' && (fabs(m_trigelph2-91.2) < %d) '%zmasscut,

    }

    el_cuts_inv = {'elfull' : 
                    el_base_inv + ' && !(fabs(m_trigelphph-91.2) < %d) && !(fabs(m_trigelph1-91.2) < %d)  && !(fabs(m_trigelph2-91.2) < %d) ' %(zmasscut,zmasscut,zmasscut),
                   'elloose' :
                    el_base_inv,
                   'elzcr' :
                    el_base_inv + ' && (fabs(m_trigelphph-91.2) < %d) ' %zmasscut,
                   'elph1zcr' :
                    el_base_inv + ' && (fabs(m_trigelph1-91.2) < %d) '%zmasscut,
                   'elph2zcr' :
                    el_base_inv + ' && (fabs(m_trigelph2-91.2) < %d) '%zmasscut,

    }

    # add mT cuts 
    el_keys = el_cuts.keys()
    for key in el_keys :
        el_cuts[key+'lowmt']  = el_cuts[key] + ' && mt_trigel_met < 40 '
        el_cuts[key+'highmt'] = el_cuts[key] + ' && mt_trigel_met > 40 '
        el_cuts_inv[key+'lowmt']  = el_cuts_inv[key] + ' && mt_trigel_met < 40 '
        el_cuts_inv[key+'highmt'] = el_cuts_inv[key] + ' && mt_trigel_met > 40 '

    # add inverted cuts
    el_keys = el_cuts.keys()
    print '**************************USE PSV**************************'
    for key in el_keys :
        el_cuts[key+'invlead']  = el_cuts[key] + ' && ph_mediumNoEleVeto_n==2 && hasPixSeed_leadph12 == 1 && hasPixSeed_sublph12 == 0 '
        el_cuts[key+'invsubl']  = el_cuts[key] + ' && ph_mediumNoEleVeto_n==2 && hasPixSeed_leadph12 == 0 && hasPixSeed_sublph12 == 1 '
        el_cuts[key+'vetoboth'] = el_cuts[key] + ' && ph_mediumPassPSV_n==2 ' 

    #for key in el_keys :
    #    el_cuts[key+'invlead']  = el_cuts_inv[key] + ' && ph_mediumNoEleVeto_n==2 '
    #    el_cuts[key+'invsubl']  = el_cuts_inv[key] + ' && ph_mediumNoEleVeto_n==2 '
    #    el_cuts[key+'vetoboth'] = el_cuts[key] + ' && ph_mediumPassCSEV_n==2 ' 

    el_cuts['elZgg'] = 'el_n>1'
    el_cuts['elZggvetoboth'] = 'el_n>1'

    global mu_cuts
    mu_cuts = {}
    mu_cuts['mu']  = 'mu_passtrig25_n>0 && el_n==0 && mu_n==1 && mt_trigmu_met > 40 '
    mu_cuts['muhighmt']  = 'mu_passtrig25_n>0 && el_n==0 && mu_n==1 && mt_trigmu_met > 40 '
    mu_cuts['mulowmt']  = 'mu_passtrig25_n>0 && el_n==0 && mu_n==1 && mt_trigmu_met < 40 '

    mu_cuts['muZgg'] = 'mu_n>1'

    global samplesWelgg
    global samplesWelggCR
    global samplesWmugg
    global samplesWggInvLead
    global samplesWggInvSubl

    #baseDirWmugg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAll_2015_10_01'
    #baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElUnblindAll_2015_10_01'

    baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElUnblindAllNoZCutNoMtCut_2015_11_11'
    baseDirWmugg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAllNoMtCut_2015_11_11'
    baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElNoZCutNoMtCutInvPixLead_2015_11_11'
    baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElNoZCutNoMtCutInvPixSubl_2015_11_11'

    #baseDirWmugg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAllNoMtCut_2015_11_11'
    #baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElCSEVUnblindAllNoZCutNoMtCut_2015_11_11'
    #baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElCSEVNoZCutNoMtCutInvPixLead_2015_11_11'
    #baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElCSEVNoZCutNoMtCutInvPixSubl_2015_11_11'
    ##baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElCSEVNoEleOlapRMWithDRNoZCutNoMtCutInvPixLead_2015_11_11'
    ##baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElCSEVNoEleOlapRMWithDRNoZCutNoMtCutInvPixSubl_2015_11_11'

    if options.sublptbins  is not None :
        #baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElCSEVUnblindAllNoZCutNoMtCutPt15_2015_11_11'
        #baseDirWmugg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAllNoMtCutPt15_2015_11_11'
        #baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElCSEVNoZCutNoMtCutInvPixLeadPt15_2015_11_11'
        #baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElCSEVNoZCutNoMtCutInvPixSublPt15_2015_11_11'
        baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElUnblindAllNoZCutNoMtCutPt15_2015_11_11'
        baseDirWmugg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAllNoMtCutPt15_2015_11_11'
        baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElNoZCutNoMtCutInvPixLeadPt15_2015_11_11'
        baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalElNoZCutNoMtCutInvPixSublPt15_2015_11_11'

    if options.zgg :
        baseDirWmugg      = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaGammaFinalMuMuUnblindAll_2015_12_12'
        baseDirWelgg      = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaGammaFinalElElUnblindAll_2015_12_12'
        baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaGammaFinalElElUnblindAll_2015_12_12'
        baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaGammaFinalElElUnblindAll_2015_12_12'

    #baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaWithEleOlapFinalElUnblindAllNoZMassLowMt_2015_09_03'
    #baseDirWmugg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaWithEleOlapFinalMuUnblindAllLowMt_2015_09_03'
    #baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaWithEleOlapFinalElNoZCutInvPixLead_2015_09_03'
    #baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaWithEleOlapFinalElNoZCutInvPixSubl_2015_09_03'


    #baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoEleVetoFinalElUnblindAllNoZMassLowMt_2015_08_31'
    #baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaGammaFinalElZCR_2015_08_01'
    #baseDirWmugg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAllLowMt_2015_08_01'
    #baseDirWelggCR = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAllLowMt_2015_08_01'
    #baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaGammaFinalElElUnblindAll_2015_08_01'

    #baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvCSEVLead_2014_12_23'
    #baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvCSEVSubl_2014_12_23'

    #baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaGammaNoPhIDTrigEleOlapInvPixSeedLead_2015_01_02'
    #baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaGammaNoPhIDTrigEleOlapInvPixSeedSubl_2015_01_02'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfWgg = 'Modules/WgamgamForBkg.py'
    if options.zgg :
        sampleConfWgg = 'Modules/ZgamgamForBkg.py'

    samplesWelgg = SampleManager(baseDirWelgg, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWmugg = SampleManager(baseDirWmugg, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWggInvLead = SampleManager(baseDirWggInvLead, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWggInvSubl = SampleManager(baseDirWggInvSubl, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    #samplesWelggCR = SampleManager(baseDirWelggCR, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesWelgg.ReadSamples( sampleConfWgg )
    samplesWmugg.ReadSamples( sampleConfWgg )
    samplesWggInvLead.ReadSamples( sampleConfWgg )
    samplesWggInvSubl.ReadSamples( sampleConfWgg )
    #samplesWelggCR.ReadSamples( sampleConfWgg )

    bins = options.ptbins.split(',')

    # get paths to different fit results
    suffix = ''
    #suffix = 'TAndP'

    print '***************************USE PSV************************'

    path_nom           = 'ElectronFakeFitsRatio%s' %suffix 
    path_nom_coarse    = 'ElectronFakeFitsRatio%sCoarseEta' %suffix 
    path_mctempnd        = 'ElectronFakeFitsRatio%sMCTemplateNDKeys' %suffix
    path_mctempnd_coarse = 'ElectronFakeFitsRatio%sMCTemplateNDKeysCoarseEta' %suffix
    #path_mctempnd        = 'ElectronFakeFitsRatioCSEV%sMCTemplateNDKeys' %suffix
    #path_mctempnd_coarse = 'ElectronFakeFitsRatioCSEV%sMCTemplateNDKeysCoarseEta' %suffix
    #path_mctempnd        = 'ElectronFakeFitsRatioMIXReqEleCSEVMCTemplateNDKeys' 
    #path_mctempnd_coarse = 'ElectronFakeFitsRatioMIXReqEleCSEVMCTemplateNDKeys'
    #path_mctemp        = 'ElectronFakeFitsRatio%sMCTemplate' %suffix
    #path_mctemp_coarse = 'ElectronFakeFitsRatio%sMCTemplate' %suffix
    path_mctempmctempnd        = 'ElectronFakeFitsRatio%sMCTemplateBkgNDKeys' %suffix
    path_mctempmctempnd_coarse = 'ElectronFakeFitsRatio%sMCTemplateBkgNDKeys' %suffix
    path_manual = 'ElectronFakeManual'
    #path_manual = 'ElectronFakeManualWithOlap2'
    path_manualL = 'ElectronFakeManualLoose'

    # SET TO CORRECT DIRECTORY!
    ele_fake_dir = path_mctempnd

    # use orderedDict to keep things in pT order
    file_bin_map             = collections.OrderedDict()
    file_bin_map_coarse      = collections.OrderedDict()
    file_bin_map_syst        = collections.OrderedDict()
    file_bin_map_coarse_syst = collections.OrderedDict()

    # define the map between pt bins and
    # the fit results we want to use

    # go up to the second-to-last bin
    for bidx in range( 0, len( bins ) - 2 ) :
        #file_bin_map            [(bins[bidx], bins[bidx+1])] = path_mctempmctempnd
        #file_bin_map_syst       [(bins[bidx], bins[bidx+1])] = path_mctempmctempnd
        #file_bin_map            [(bins[bidx], bins[bidx+1])] = path_mctemp
        #file_bin_map_syst       [(bins[bidx], bins[bidx+1])] = path_mctemp
        #file_bin_map            [(bins[bidx], bins[bidx+1])] = path_manual
        #file_bin_map_syst       [(bins[bidx], bins[bidx+1])] = path_manual
        #file_bin_map            [(bins[bidx], bins[bidx+1])] = path_manualL
        #file_bin_map_syst       [(bins[bidx], bins[bidx+1])] = path_manualL
        #file_bin_map            [(bins[bidx], bins[bidx+1])] = path_nom
        #file_bin_map_syst       [(bins[bidx], bins[bidx+1])] = path_nom
        file_bin_map            [(bins[bidx], bins[bidx+1])] = path_mctempnd
        file_bin_map_syst       [(bins[bidx], bins[bidx+1])] = path_mctempnd

    # do the last bin
    #file_bin_map[(bins[-2], 'max')] = path_nom
    #file_bin_map_syst[(bins[-2], 'max')  ] = path_nom
    file_bin_map[(bins[-2], 'max')] = path_mctempnd
    file_bin_map_syst[(bins[-2], 'max')  ] = path_mctempnd
    #file_bin_map[(bins[-2], 'max')] = path_mctempmctempnd
    #file_bin_map_syst[(bins[-2], 'max')  ] = path_mctempmctempnd
    #file_bin_map[(bins[-2], 'max')] = path_mctemp
    #file_bin_map_syst[(bins[-2], 'max')  ] = path_mctemp
    #file_bin_map[(bins[-3], bins[-2])] = path_manual
    #file_bin_map_syst[(bins[-2], 'max')  ] = path_manual
    #file_bin_map[(bins[-2], 'max')] = path_manual
    #file_bin_map_syst[(bins[-2], 'max')  ] = path_manual
    #file_bin_map[(bins[-2], 'max')] = path_manualL
    #file_bin_map_syst[(bins[-2], 'max')  ] = path_manualL

    pt_bins = [int(x) for x in options.ptbins.split(',')]

    #kinevars_common = {'m_ph1_ph2'    : [(0, 40), (40, 60), (60, 100), (100, 1000000)], 
    #                   'pt_ph1_ph2'   : [(0,40), (40,80), (80,120), (120,1000000)],
    #                  }
    kinevars_common = {'m_ph1_ph2'    : [(0, 60), (60, 120), (120, 240), (240, 1000000)], 
                       'pt_ph1_ph2'   : [(0,20), (20,40), (40,60), (60,80), (80,1000000)],
                      }

    kinevars_ch_el  = { 'mt_trigel_met'  : [(40, 60), (60, 80), (80, 120), (120,1000000)] }
    kinevars_ch_mu  = { 'mt_trigmu_met'  : [(40, 60), (60, 80), (80, 120), (120,1000000)] }

    if options.zgg :
        kinevars_common = {
                           #'m_ph1_ph2'    : [(0, 20), (20, 40), (40, 60), (60, 80), (80, 100), (100,160), (160, 1000000)], 
                           'm_ph1_ph2'    : [(0, 20), (20, 40), (40, 60), (60, 100), (100,160), (160, 1000000)], 
                           'pt_ph1_ph2'   : [(0,20), (20,40), (40,60), (60,80), (80,1000000)],
                           'm_leplepphph' : [(80,100), (100,150), (150,200), (200,250), (250,300), (300,1000000)],
                          }
        kinevars_ch_el = {'m_elel'   : [(40,60), (60,80), (80, 100), (100, 1000000)] }
        kinevars_ch_mu = {'m_mumu'   : [(40,60), (60,80), (80, 100), (100, 1000000)] }

    kinevars_el = dict( kinevars_common )
    kinevars_el.update( kinevars_ch_el )

    kinevars_mu = dict( kinevars_common )
    kinevars_mu.update( kinevars_ch_mu  )

    # disable kinematic variables if 
    # binning in pT is requested
    if len( pt_bins ) > 2 :
        kinevars_el = {}
        kinevars_mu = {}


    for idx, ptmin in enumerate( pt_bins[:-1] )  :

        ptmax = pt_bins[idx+1]

        if ptmax == pt_bins[-1] :
            ptmaxstr = 'max'
        else :
            ptmaxstr = str( pt_bins[idx+1] )
        ptminstr = str( ptmin )

        _eta_pt_bin_map[(ptminstr,ptmaxstr)] = _ele_eta_bins
        _eta_pt_bin_map_coarse[(ptminstr,ptmaxstr)] = _ele_eta_bins_coarse

    subl_pt_bins = None
    if options.sublptbins is not None :
        binsplit = options.sublptbins.split(',')
        subl_pt_bins = ( int(binsplit[0]), int(binsplit[1]) )

    if options.baseDir is not None :
        outputDirBase='%s/BackgroundEstimates/' %(options.baseDir )
        base_dir_ele = options.baseDir
        resultDir = '%s/%s' %( outputDirBase, options.plotDir )
        base_dir_jet = resultDir
       
        MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='muZgg', addtlVars=kinevars_mu, outputDir=resultDir)
        MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elZgg', addtlVars=kinevars_el, outputDir=resultDir)

        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='muhighmt'              , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_mu, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elfullhighmt'          , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elfullhighmtinvpixlead', subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elfullhighmtinvpixsubl', subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )

        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elfulllowmt'           , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elfulllowmtinvpixlead' , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elfulllowmtinvpixsubl' , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )

        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='mulowmt'               , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_mu, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='ellooselowmt'          , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='ellooselowmtinvpixlead', subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='ellooselowmtinvpixsubl', subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )

        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elzcrhighmt'           , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elzcrhighmtinvpixlead' , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elzcrhighmtinvpixsubl' , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )

        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elzcr'                 , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elzcrinvpixlead'       , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )
        #MakeJetBkgEstimateNew( '%s/JetFakeResultsSyst'%options.baseDir, pt_bins, channel='elzcrinvpixsubl'       , subl_pt_bins=subl_pt_bins, addtlVars=kinevars_el, outputDir=resultDir )

        #ele_selections = ['elfullhighmt', 'elfulllowmt', 'elzcrhighmt', 'elzcr', 'ellooselowmt' ]
        #ele_selections = ['elfullhighmt', 'elfulllowmt']
        #ele_selections = ['elfullhighmt' ]
        ele_selections = []

        for sel in ele_selections :
            MakeEleBkgEstimateNew( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, pt_bins=pt_bins, subl_pt_bins=subl_pt_bins, el_selection=sel, fakeDir=ele_fake_dir, outputDir=resultDir )

            for var, cuts in kinevars_el.iteritems() :
                for cut in cuts :
                    MakeEleBkgEstimateNew( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, pt_bins=pt_bins, subl_pt_bins=subl_pt_bins, el_selection=sel, addtlVar=var, addtlVarCuts=cut, fakeDir=ele_fake_dir, outputDir=resultDir )


        plot_binning = pt_bins
        # last bin should be at 100
        plot_binning[-1] = 100
        #plot_binning = [25,100]

        channels_el = [
                        #'elfullhighmt', 
                        #'elfulllowmt', 
                        #'elzcrhighmt',
                        #'elzcr',
                        #'ellooselowmt',
                        'elZgg'
                      ]
        channels_mu = [
                        #'muhighmt',
                        #'mulowmt',
                        'muZgg'
                      ]

        for mu in channels_mu :
            MakeBkgEstimatePlots( resultDir, plot_binning, channelmu=mu, channelel=None, minpt=pt_bins[0], subl_pt_bins=subl_pt_bins )
            for var, cuts in kinevars_mu.iteritems() :
                binning = []
                varstrs = []
                for cut in cuts :
                    binning.append( cut[0] )
                    varstrs.append( '__cut_%s_%d-%d' %( var, cut[0], cut[1] ) )
                # make the last bin end above the last one by the previous bin boundary
                binning.append( cuts[-1][0] + cuts[-2][0] )
                MakeBkgEstimatePlots( resultDir, binning, channelmu=mu, channelel=None, minpt=pt_bins[0], subl_pt_bins=subl_pt_bins, varname=var, varstrs=varstrs  )

        for el in channels_el :
            MakeBkgEstimatePlots( resultDir, plot_binning, channelmu=None, channelel=el, minpt=pt_bins[0], subl_pt_bins=subl_pt_bins )
            for var, cuts in kinevars_el.iteritems() :
                binning = []
                varstrs = []
                for cut in cuts :
                    binning.append( cut[0] )
                    varstrs.append( '__cut_%s_%d-%d' %( var, cut[0], cut[1] ) )
                # make the last bin end above the last one by the previous bin boundary
                binning.append( cuts[-1][0] + cuts[-2][0] )
                MakeBkgEstimatePlots( resultDir, binning, channelmu=None, channelel=el, minpt=pt_bins[0], subl_pt_bins=subl_pt_bins, varname=var, varstrs=varstrs  )

        ##plot_binning_zgg = [15,25,40,100]
        ##plot_binning_zgg = [25,100]
        #MakeBkgEstimatePlots( resultDir, plot_binning_zgg, channelmu='muZgg', channelel='elZgg', minpt=pt_bins[0] )

 
    print '^_^ FINSISHED ^_^'
    print 'It is safe to kill the program if it is hanging'


def make_fake_factor( numerator, denominator, min, max ) :


    bin_min = numerator.FindBin( min )
    bin_max = numerator.FindBin( max ) - 1
    num_err = ROOT.Double()
    num_int = numerator.IntegralAndError( bin_min, bin_max, num_err )

    num_val = ufloat( num_int, num_err )

    den_err = ROOT.Double()
    den_int = denominator.IntegralAndError( bin_min, bin_max, den_err )

    den_val = ufloat( den_int, den_err )

    if den_int != 0 :
        ratio = num_val / den_val
    else :
        ratio = ufloat(0, 0)

    return { 'numerator' : num_val, 'denominator' : den_val, 'fake_factor' : ratio, 'min' : min, 'max' : max, 'min_bin' : bin_min, 'max_bin' : bin_max}



def MakeJetBkgEstimateNew( base_dir_jet, pt_bins, channel, subl_pt_bins=None, addtlVars={}, outputDir=None ) :

    print '--------------------------------------'
    print 'START JET FAKE ESTIMATE FOR CHANNEL %s' %channel
    print '--------------------------------------'

    #uncertainties = {'systTemp' : True, 'systBkg' : True, 'statTemp' : False, 'statData' : False}
    uncertainties = {'systTemp' : False, 'systBkg' : True, 'statTempTight' : True, 'statTempLoose' : True, 'statTempFF' : False, 'statDataSB' : False, 'statDataSR' : False, 'fakefake' : False, 'crossCorr' : True}
    #uncertainties = {'systTemp' : False, 'systBkg' : False, 'statTempTight' : False, 'statTempLoose' : False, 'statData' : False}
    #vars = ['SigmaIEIEFits', 'PhoIsoFits', 'ChHadIsoFits']
    vars = ['ChHadIsoFits']
    #vars = ['SigmaIEIEFits']

    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB')]

    result_dic = {'stat' : {}, 'syst' : {}, 'stat+syst' : {}}
    for key in result_dic.keys() :
        result_dic[key] = {'rf' : {}, 'fr' : {}, 'ff' : {}, 'sum' : {} }

    result_dic_vars = {}
    for v, cuts in addtlVars.iteritems() :
        for cut in cuts :
            varcut = '__cut_%s_%d-%d' %(v, cut[0], cut[1] )
            result_dic_vars[varcut] = { 'stat' : {'rf' : {}, 'fr' : {}, 'ff' : {}, 'sum' : {} },
                                        'syst' : {'rf' : {}, 'fr' : {}, 'ff' : {}, 'sum' : {} },
                                        'stat+syst' : {'rf' : {}, 'fr' : {}, 'ff' : {}, 'sum' : {} },
                                      }

    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')

    if subl_pt_bins is None :
        strsublptmin = pt_bins_jetfile[0]
        strsublptmax = 'max'
    else :
        strsublptmin = str( subl_pt_bins[0] )
        strsublptmax = str( subl_pt_bins[1] )

    for idx, strptmin in enumerate(pt_bins_jetfile[:-1]) :
        strptmax = pt_bins_jetfile[idx+1]

        for r1, r2 in regions :


            result_bin = ( r1, r2, strptmin, strptmax )

            get_jet_results_with_uncerts( result_dic, vars, channel, result_bin, base_dir_jet, uncertainties, strsublptmin, strsublptmax )

            for varcut, dic in result_dic_vars.iteritems() :
                get_jet_results_with_uncerts( dic, vars, channel, result_bin, base_dir_jet, uncertainties, strsublptmin, strsublptmax, addtl_var_cut=varcut )


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )
        file = open( outputDir + '/jet_fake_results__%s.pickle' %channel, 'w' )
        pickle.dump( result_dic, file)
        file.close()

        for varcut, dic in result_dic_vars.iteritems() :
            file = open( outputDir + '/jet_fake_results__%s%s.pickle' %(channel,varcut), 'w' )
            pickle.dump( dic, file )
            file.close()


    return

def get_jet_results_with_uncerts( result_dic, vars, channel, result_bin, base_dir_jet, uncertainties, sublptmin,sublptmax, addtl_var_cut='' ) :

    r1 = result_bin[0]
    r2 = result_bin[1]
    strptmin = result_bin[2]
    strptmax = result_bin[3]

    found_result_dirs = {}
    ff_var_systs = {}
    for var in vars :

        print 'var : %s, ptmin = %s, ptmax = %s, r1 = %s, r2 = %s ' %( var, strptmin, strptmax, r1, r2)

        file_key_generic = 'results__statDataSB__ffcorr_nom__%s__%s-%s__pt_%s-%s__subpt_%s-%s%s.pickle' %(  channel, r1, r2, strptmin, strptmax, sublptmin, sublptmax, addtl_var_cut )
        #file_key_generic = 'results__statData__ffcorr_nom__%s__%s-%s__pt_%s-%s.pickle' %(  channel, r1, r2, strptmin, strptmax )
        result_dir = select_result_dir( '%s/%s' %( base_dir_jet, var), channel, file_key_generic )

        found_result_dirs[var] = result_dir

        # get the ff template variation
        # uncertainties.  The uncertainty
        # is a difference in the central values
        # so any of the uncertainty files can be used
        file_key_ffvar = 'results__%s__ffcorr_(?P<ffvar>\w+)__%s__%s-%s__pt_%s-%s__subpt_%s-%s%s.pickle' %( 'statDataSB', channel, r1, r2, strptmin, strptmax, sublptmin, sublptmax,addtl_var_cut  )
        #file_key_ffvar = 'results__%s__ffcorr_(?P<ffvar>\w+)__%s__%s-%s__pt_%s-%s.pickle' %( uncertainties.keys()[0], channel, r1, r2, strptmin, strptmax )
        ff_var_unc = get_ff_var_uncertainties( '%s/%s/%s' %(base_dir_jet, var, result_dir), channel, file_key_ffvar )
        ff_var_systs[var] = ff_var_unc


    # key to match all other uncertainty variations
    file_key = 'results__(?P<uncertainty>\w+)__ffcorr_nom__%s__%s-%s__pt_%s-%s__subpt_%s-%s%s.pickle' %(  channel, r1, r2, strptmin, strptmax, sublptmin, sublptmax, addtl_var_cut  )
    #file_key = 'results__(?P<uncertainty>\w+)__%s__%s-%s__pt_%s-%s.pickle' %(  channel, r1, r2, strptmin, strptmax )

    results = get_jet_fake_results_new( base_dir_jet, file_key, channel, uncertainties, found_result_dirs, ff_var_systs )

    print 'addtl_var_cut = %s, comb_result = %s' %( addtl_var_cut, results['comb'])

    result_dic['stat+syst']['sum'][result_bin] = {}
    result_dic['stat+syst']['sum'][result_bin]['result'] = resolve_negatives( results['comb'] )

    for unc, val in results.iteritems() :
        if unc == 'comb' :
            continue
        result_dic.setdefault( 'individual', {} )
        result_dic['individual'].setdefault( unc , {} )
        result_dic['individual'][unc].setdefault( 'sum' , {} )
        result_dic['individual'][unc]['sum'][result_bin] = {'result' : val } 

def resolve_negatives( inval ) :

    # if the result is negative, but consistent
    # with 0, then set the value to zero with 
    # the proper uncertanty.
    # if not, take the full difference as the
    # uncertainty
    if inval.n < 0 :
        if math.fabs( inval.n ) < inval.s :
            return ufloat( 0.0, inval.s )
        else :
            return ufloat( 0.0, math.fabs(inval.n) )
    else :
        return inval


def get_jet_fake_results_new( base_dir, file_key, channel, uncertainties, result_dirs, ff_var_systs ) :

    central_values = {}
    std_devs = {}
    for unc in uncertainties.keys() :
        std_devs[unc] = {}

    data_values = {}
    for var, dir in result_dirs.iteritems() :

        # get the prediction and each systematic
        matches = get_matching_regex( os.listdir( '%s/%s/%s/%s' %(base_dir,var,dir, channel)), file_key )

        first = True
        for match_file, match_value in matches :

            if match_value['uncertainty'] in uncertainties.keys() :

                ofile = open( '%s/%s/%s/%s/%s' %( base_dir,var,dir, channel,match_file), 'r')

                this_result = pickle.load( ofile )

                ofile.close()

                bkg_sum = this_result['Npred_RF_TT'] + this_result['Npred_FR_TT'] + this_result['Npred_FF_TT']

                if var not in data_values :
                    data_values[var] = {}
                    data_values[var]['Ndata_TT'] = this_result['Ndata_TT']
                    data_values[var]['Ndata_TL'] = this_result['Ndata_TL']
                    data_values[var]['Ndata_LT'] = this_result['Ndata_LT']
                    data_values[var]['Ndata_LL'] = this_result['Ndata_LL']

                if first :
                    central_values[var] = bkg_sum
                    first = False

                std_devs[match_value['uncertainty']][var] = bkg_sum

        # do ff var systs
        std_devs['fakefake'][var] = ufloat( central_values[var].n, ff_var_systs[var] )

        # do cross correlation systs
        resdirres = re.match( 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso', result_dirs[var] )
        if resdirres is None :
            if result_dirs[var].count('No SIEIE') :
                std_devs['crossCorr'][var] = ufloat( central_values[var].n, _asym_iso_syst[(5, 3, 3)] )
            print 'WARNING, could not parse iso values from directory'
        else :

            iso1 = int(resdirres.group(1) )
            iso2 = int(resdirres.group(2) )
            iso3 = int(resdirres.group(3) )
            std_devs['crossCorr'][var] = ufloat( central_values[var].n, _asym_iso_syst[(iso1,iso2,iso3)] )

    for var, val in data_values.iteritems() :
        print '%s, NTT = %s, NTL = %s, NLT = %s, NLL = %s'  %( var, val['Ndata_TT'], val['Ndata_TL'], val['Ndata_LT'], val['Ndata_LL'] )

    results = {}


    comb_std_devs = {}
    for key, uncert in std_devs.iteritems() :
        for var, val in uncert.iteritems() :
            comb_std_devs.setdefault( var, 0.0 ) 
            comb_std_devs[var] = comb_std_devs[var] + val.s*val.s

            results.setdefault( var, {} )
            results[var][key] = val

    # get a stable variable ordering
    variable_order = list( result_dirs.keys() )

    if len( variable_order ) > 1 :
        # now do blue
        calc_comb = blue.Calculator() 


        meas_values = [central_values[v].n for v in variable_order]

        print 'Measured values :  ' + ', '.join( ['%s : %f +- %f' %( v, central_values[v].n, math.sqrt( comb_std_devs[v])) for v in variable_order ] )

        calc_comb.SetMeasurementValues( meas_values )

        # make BLUE calculators for each separate uncertainty
        calc_indiv = {}
        for unc in std_devs.keys() :
            calc_indiv[unc] = blue.Calculator()
            calc_indiv[unc].SetMeasurementValues( meas_values )

        n_var = len( variable_order )
        for unc, is_corr in uncertainties.iteritems() :

            matrix = [ ]
            for i in range(0, n_var) :
                list_i = [0]*n_var
                for j in range(0,n_var) :

                    entry = std_devs[unc][variable_order[i]].s*std_devs[unc][variable_order[j]].s
                    if i != j and not is_corr :
                        entry = 0

                    list_i[j] = entry

                matrix.append( list_i )

            calc_comb.AddErrorMatrix( matrix )
            if unc in calc_indiv :
                calc_indiv[unc].AddErrorMatrix( matrix)

            print 'Error matrix : '
            print matrix

        central_value = calc_comb.CalculateCombinedValue()
        combined_unc  = calc_comb.CalculateCombinedUncertainty()

        # get the weights from the combined BLUE calculation
        # and give them to the individual calculators
        combined_alphas = calc_comb.GetAlphas()
        for icalc in calc_indiv.values() :
            icalc.SetAlphas( combined_alphas )
        
        # get the individual uncertainties and save them to a file
        for unc, icalc in calc_indiv.iteritems() :

            value = icalc.CalculateCombinedValue()
            uncert= icalc.CalculateCombinedUncertainty()

            results[unc] = ufloat( value, uncert )

        max_diffs = []
        for v1, m1 in central_values.iteritems() :
            for v2,m2 in central_values.iteritems() :
                #if comb_std_devs[v1] > 5*m1.n or comb_std_devs[v2] > 5*m2.n :
                #    continue
                max_diffs.append( math.fabs( m2.n - m1.n) )

        max_diff = max( max_diffs )

        diff_unc = 0.5 * max_diff
        final_unc = math.sqrt( diff_unc*diff_unc + combined_unc*combined_unc)

        results['diff'] = ufloat( central_value, diff_unc )

        #print 'Result = %f +- %f' %( central_value, 0.5*max_diff )
        print 'Diff unc = %f, Combined unc = %f' %( diff_unc, combined_unc )
        print 'Result = %f +- %f' %( central_value, final_unc ) 
        print calc_comb.alpha_array
        print calc_comb.err_matrix

        print '***********************FIX********************'
        #results['comb'] = ufloat(central_value, final_unc )
        results['comb'] = ufloat(central_value, combined_unc )

    else :

        var = variable_order[0]
        results['diff'] = ufloat( central_values[var].n, 0.0 )
        sum_sq = 0
        print std_devs
        print results
        for unc in std_devs.keys() :
            results[unc] = std_devs[unc][var]
            sum_sq += std_devs[unc][var].s * std_devs[unc][var].s
        results['comb'] = ufloat( central_values[var].n, math.sqrt(sum_sq) )

    return results

                
def get_ff_var_uncertainties( result_dir,  channel, file_key_ffvar) :

    matches = get_matching_regex( os.listdir( '%s/%s' %(result_dir, channel) ), file_key_ffvar ) 

    bkg_sum = {}
    for match in matches :

        file = '%s/%s/%s' %( result_dir, channel, match[0] )

        ofile = open( file, 'r')
        
        results = pickle.load( ofile )
        ofile.close()

        bkg_sum[match[1]['ffvar']] = results['Npred_RF_TT']+results['Npred_FR_TT'] + results['Npred_FF_TT']

    central_value = bkg_sum['nom'].n

    diffs = []
    for match, val in bkg_sum.iteritems() :
        print 'ff type = %s, result = %s ' %( match, val ) 
        if match != 'None' :
            diffs.append( math.fabs( val.n-central_value ) )

    max_diff = max(diffs)

    return max_diff



def select_result_dir( base_dir, channel, file_name ) :

    jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'
    jet_dirs_key_nom = 'JetFakeTemplateFitPlotsNomIso'

    jet_dir_key_map = get_mapped_directory( base_dir, jet_dirs_key )
    jet_dir_key_map[(0,0,0)] = 'JetFakeTemplateFitPlotsCorrNo SIEIEAsymIso'
    #jet_dir_key_map[(0,0,0)] = jet_dirs_key_nom

    sorted_jet_dirs = jet_dir_key_map.keys()
    sorted_jet_dirs.sort()

    print '****************************FIX********************************'
    print 'USING NO SIEIE DIRECTORY'
    return jet_dir_key_map[(0,0,0)]

    selected_dir = None
    results_store = {}
    for syst_type in sorted_jet_dirs[1:] :

        result_file = '%s/%s/%s/%s' % (base_dir, jet_dir_key_map[syst_type], channel, file_name ) 

        ofile = open( result_file, 'r')

        results = pickle.load( ofile )

        ofile.close()

        Ndata_tt = results['Ndata_TT']
        Ndata_tl = results['Ndata_TL']
        Ndata_lt = results['Ndata_LT']
        Ndata_ll = results['Ndata_LL']

        results_store[jet_dir_key_map[syst_type]] = {'Ndata_TT' : Ndata_tt, 'Ndata_TL' : Ndata_tl, 'Ndata_LT' : Ndata_lt, 'Ndata_LL' : Ndata_ll }

        if  Ndata_tl == 0 or Ndata_lt == 0 or Ndata_ll == 0 :
            continue

        selected_dir = jet_dir_key_map[syst_type]
        print '************************************'
        print 'USE RESULT DIR %s ' %jet_dir_key_map[syst_type]
        print '************************************'

        break

    if selected_dir is None :
        print '*************************************'
        print 'DID NOT FIND NON-ZERO ENTRY'
        print '*************************************'
        print results_store
        selected_dir = jet_dir_key_map[sorted_jet_dirs[1]]

    return selected_dir

def get_matching_regex( full_list, match ) :
    
    matches = []

    for obj in full_list :
        res = re.match( match, obj )

        if res is not None :
            matches.append( ( obj, res.groupdict() ) )

    return matches

def MakeJetBkgEstimate( base_dir_jet, pt_bins, channel, outputDir=None ) :

    print '--------------------------------------'
    print 'START JET FAKE ESTIMATE'
    print '--------------------------------------'


    file_key_mu        = 'results__mu__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elfull    = 'results__elfull__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elzcr     = 'results__elzcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elph1zcr  = 'results__elph1zcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elph2zcr  = 'results__elph2zcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'

    # jet fake results with systematic
    # uncertainties propagated
    file_key_mu_syst       = 'results__syst__mu__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elfull_syst   = 'results__syst__elfull__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elzcr_syst    = 'results__syst__elzcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elph1zcr_syst = 'results__syst__elph1zcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elph2zcr_syst = 'results__syst__elph2zcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'

    jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'
    jet_dirs_key_nom = 'JetFakeTemplateFitPlotsNomIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )
    jet_dir_key_map[(0,0,0)] = 'JetFakeTemplateFitPlotsNomIso'

    jet_files_mu       = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu     )
    jet_files_elfull   = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull )
    jet_files_elzcr    = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elzcr  )
    jet_files_elph1zcr = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elph1zcr  )
    jet_files_elph2zcr = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elph1zcr  )

    jet_files_mu_nom   = get_dirs_and_files( base_dir_jet, jet_dirs_key_nom, file_key_mu     )
    jet_files_mu.update( jet_files_mu_nom )

    jet_files_mu_syst       = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu_syst     )
    jet_files_elfull_syst   = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull_syst )
    jet_files_elzcr_syst    = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elzcr_syst     )
    jet_files_elph1zcr_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elph1zcr_syst     )
    jet_files_elph2zcr_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elph2zcr_syst     )

    jet_files_mu_nom_syst  = get_dirs_and_files( base_dir_jet, jet_dirs_key_nom, file_key_mu_syst )
    jet_files_mu_syst.update( jet_files_mu_nom_syst )



    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

    print '---------------------------------------------'
    print 'START JET FAKE, MUON CHANNEL'
    print '---------------------------------------------'
    if jet_files_mu.values()[0] :
        subl_ptbins = [ ( '70', 'max', '15', '40' ), ( '70', 'max', '40', 'max' ) ]
        subl_ptbins = [ ]
        pred_mu     = get_jet_fake_results( jet_files_mu    , jet_files_mu_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet, pt_bins_subl=subl_ptbins ) 
        print '---------------------------------------------'
        print 'JET FAKE RESULTS, MUON CHANNEL'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['stat']['rf'][bin]['result'], pred_mu['stat']['fr'][bin]['result'], pred_mu['stat']['ff'][bin]['result'], (  pred_mu['stat']['rf'][bin]['result']+ pred_mu['stat']['fr'][bin]['result']+ pred_mu['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['syst']['rf'][bin]['result'], pred_mu['syst']['fr'][bin]['result'], pred_mu['syst']['ff'][bin]['result'], (  pred_mu['syst']['rf'][bin]['result']+ pred_mu['syst']['fr'][bin]['result']+ pred_mu['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['stat+syst']['rf'][bin]['result'], pred_mu['stat+syst']['fr'][bin]['result'], pred_mu['stat+syst']['ff'][bin]['result'], (  pred_mu['stat+syst']['rf'][bin]['result']+ pred_mu['stat+syst']['fr'][bin]['result']+ pred_mu['stat+syst']['ff'][bin]['result'] ) )

        file_muon = open( outputDir + '/jet_fake_results__mgg.pickle', 'w' )
        pickle.dump( pred_mu, file_muon )
        file_muon.close()

    print '---------------------------------------------'
    print 'START JET FAKE, ELECTRON CHANNEL WITH Z REJ CUTS'
    print '---------------------------------------------'
    if jet_files_elfull.values()[0] :
        pred_elfull = get_jet_fake_results( jet_files_elfull, jet_files_elfull_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print '---------------------------------------------'
        print 'JET FAKE RESULTS, ELECTRON CHANNEL WITH Z REJ CUTS'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['stat']['rf'][bin]['result'], pred_elfull['stat']['fr'][bin]['result'], pred_elfull['stat']['ff'][bin]['result'], (  pred_elfull['stat']['rf'][bin]['result']+ pred_elfull['stat']['fr'][bin]['result']+ pred_elfull['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['syst']['rf'][bin]['result'], pred_elfull['syst']['fr'][bin]['result'], pred_elfull['syst']['ff'][bin]['result'], (  pred_elfull['syst']['rf'][bin]['result']+ pred_elfull['syst']['fr'][bin]['result']+ pred_elfull['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['stat+syst']['rf'][bin]['result'], pred_elfull['stat+syst']['fr'][bin]['result'], pred_elfull['stat+syst']['ff'][bin]['result'], (  pred_elfull['stat+syst']['rf'][bin]['result']+ pred_elfull['stat+syst']['fr'][bin]['result']+ pred_elfull['stat+syst']['ff'][bin]['result'] ) )

        file_elfull = open( outputDir + '/jet_fake_results__egg_allZRejCuts.pickle', 'w' )
        pickle.dump( pred_elfull, file_elfull )
        file_elfull.close()

    print '---------------------------------------------'
    print 'START JET FAKE, ELECTRON CHANNEL IN Mlgg Z CR'
    print '---------------------------------------------'
    if jet_files_elzcr.values()[0] :
        pred_elzcr  = get_jet_fake_results( jet_files_elzcr , jet_files_elzcr_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print '---------------------------------------------'
        print 'JET FAKE RESULTS, ELECTRON CHANNEL IN Mlgg Z CR'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)

                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['stat']['rf'][bin]['result'], pred_elzcr['stat']['fr'][bin]['result'], pred_elzcr['stat']['ff'][bin]['result'], (  pred_elzcr['stat']['rf'][bin]['result']+ pred_elzcr['stat']['fr'][bin]['result']+ pred_elzcr['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['syst']['rf'][bin]['result'], pred_elzcr['syst']['fr'][bin]['result'], pred_elzcr['syst']['ff'][bin]['result'], (  pred_elzcr['syst']['rf'][bin]['result']+ pred_elzcr['syst']['fr'][bin]['result']+ pred_elzcr['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['stat+syst']['rf'][bin]['result'], pred_elzcr['stat+syst']['fr'][bin]['result'], pred_elzcr['stat+syst']['ff'][bin]['result'], (  pred_elzcr['stat+syst']['rf'][bin]['result']+ pred_elzcr['stat+syst']['fr'][bin]['result'] + pred_elzcr['stat+syst']['ff'][bin]['result'] ) )


        file_elzcr = open( outputDir + '/jet_fake_results__egg_ZCR.pickle', 'w' )
        pickle.dump( pred_elzcr, file_elzcr)
        file_elzcr.close()

    # Remove other control regions for now
    #if jet_files_elph1zcr.values()[0] :
    #    pred_elph1zcr  = get_jet_fake_results( jet_files_elph1zcr , jet_files_elph1zcr_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

    #    print '---------------------------------------------'
    #    print 'JET FAKE RESULTS, ELECTRON CHANNEL IN Mlg1 Z CR'
    #    print '---------------------------------------------'
    #    for r1, r2 in regions :

    #        for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
    #            ptmax = pt_bins_jetfile[idx+1]

    #            bin = (r1,r2,ptmin,ptmax)

    #            print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)

    #            print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph1zcr['stat']['rf'][bin]['result'], pred_elph1zcr['stat']['fr'][bin]['result'], pred_elph1zcr['stat']['ff'][bin]['result'], (  pred_elph1zcr['stat']['rf'][bin]['result']+ pred_elph1zcr['stat']['fr'][bin]['result']+ pred_elph1zcr['stat']['ff'][bin]['result'] ) )
    #            print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph1zcr['syst']['rf'][bin]['result'], pred_elph1zcr['syst']['fr'][bin]['result'], pred_elph1zcr['syst']['ff'][bin]['result'], (  pred_elph1zcr['syst']['rf'][bin]['result']+ pred_elph1zcr['syst']['fr'][bin]['result']+ pred_elph1zcr['syst']['ff'][bin]['result'] ) )
    #            print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph1zcr['stat+syst']['rf'][bin]['result'], pred_elph1zcr['stat+syst']['fr'][bin]['result'], pred_elph1zcr['stat+syst']['ff'][bin]['result'], (  pred_elph1zcr['stat+syst']['rf'][bin]['result']+ pred_elph1zcr['stat+syst']['fr'][bin]['result'] + pred_elph1zcr['stat+syst']['ff'][bin]['result'] ) )


    #    file_elph1zcr = open( outputDir + '/jet_fake_results__egg_ZCRPh1.pickle', 'w' )
    #    pickle.dump( pred_elph1zcr, file_elph1zcr)
    #    file_elph1zcr.close()

    #if jet_files_elph2zcr.values()[0] :
    #    pred_elph2zcr  = get_jet_fake_results( jet_files_elph2zcr , jet_files_elph2zcr_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

    #    print '---------------------------------------------'
    #    print 'JET FAKE RESULTS, ELECTRON CHANNEL IN Mlg2 Z CR'
    #    print '---------------------------------------------'
    #    for r1, r2 in regions :

    #        for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
    #            ptmax = pt_bins_jetfile[idx+1]

    #            bin = (r1,r2,ptmin,ptmax)

    #            print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)

    #            print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph2zcr['stat']['rf'][bin]['result'], pred_elph2zcr['stat']['fr'][bin]['result'], pred_elph2zcr['stat']['ff'][bin]['result'], (  pred_elph2zcr['stat']['rf'][bin]['result']+ pred_elph2zcr['stat']['fr'][bin]['result']+ pred_elph2zcr['stat']['ff'][bin]['result'] ) )
    #            print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph2zcr['syst']['rf'][bin]['result'], pred_elph2zcr['syst']['fr'][bin]['result'], pred_elph2zcr['syst']['ff'][bin]['result'], (  pred_elph2zcr['syst']['rf'][bin]['result']+ pred_elph2zcr['syst']['fr'][bin]['result']+ pred_elph2zcr['syst']['ff'][bin]['result'] ) )
    #            print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph2zcr['stat+syst']['rf'][bin]['result'], pred_elph2zcr['stat+syst']['fr'][bin]['result'], pred_elph2zcr['stat+syst']['ff'][bin]['result'], (  pred_elph2zcr['stat+syst']['rf'][bin]['result']+ pred_elph2zcr['stat+syst']['fr'][bin]['result'] + pred_elph2zcr['stat+syst']['ff'][bin]['result'] ) )


    #    file_elph2zcr = open( outputDir + '/jet_fake_results__egg_ZCRPh2.pickle', 'w' )
    #    pickle.dump( pred_elph2zcr, file_elph2zcr)
    #    file_elph2zcr.close()

def MakeBkgEstimatePlots( result_dir, plot_binning, channelmu='mu', channelel='elfull', minpt=15, subl_pt_bins = None, varname='pt_leadph12', varstrs=[] ) :

    # first make the nominal estimates

    regions = [('EB', 'EB'), ('EB' ,'EE'), ('EE', 'EB')]


    for reg in regions + [(None, None)] :

        if reg[0] is not None :
            reg_str = ' is%s_leadph12 && is%s_sublph12 ' %(reg[0],reg[1])
            reg_tag = '_%s-%s' %( reg[0], reg[1]) 
        else :
            reg_str = ' !(isEE_leadph12 && isEE_sublph12 )'
            reg_tag = ''

        weight_str = 'mu_idSF * mu_trigSF * mu_isoSF * el_trigSF * ph_idSF * '
        event_weight = ' ( 1.0 * ( LHEWeight_weights[0] > 0 ) - 1.0 * ( LHEWeight_weights[0] < 0 ) ) * '
        weight_aqgc_lm50 = 'LHEWeight_weights[8] * 58791 * '


        if subl_pt_bins is None :
            subl_str = 'pt_sublph12 > %d ' %(minpt)
        else :
            subl_str = 'pt_sublph12 > %d && pt_sublph12 < %d ' %(subl_pt_bins[0], subl_pt_bins[1])

    
        if channelmu is not None :
            mu_base = mu_cuts[channelmu]
            draw_str_mu = 'PUWeight * ( %s && pt_leadph12 > %d && %s &&  %s )' %(mu_base, minpt, subl_str, reg_str)
            hist_tag_mu = '%s%s' %( channelmu, reg_tag )
            save_muon_hists( draw_str_mu    , weight_str, event_weight, weight_aqgc_lm50, plot_binning, result_dir, reg_tag, channelmu,varname    )


        if channelel is not None :
            draw_str_el = 'PUWeight * ( %s && pt_leadph12 > %d && %s &&  %s )' %(el_cuts[channelel+'vetoboth'], minpt, subl_str, reg_str)
            hist_tag_el = '%s%s' %( channelel, reg_tag )
            save_electron_hists( draw_str_el    , weight_str, event_weight, weight_aqgc_lm50, plot_binning, result_dir, reg_tag, channelel,varname    )

    jet_dir_mu = '%s/jet_fake_results__%s.pickle'%(result_dir, channelmu)
    jet_dir_el = '%s/jet_fake_results__%s.pickle'%(result_dir,channelel)
    ele_dir_el = '%s/electron_fake_results__%s.pickle'%(result_dir,channelel)

    if varstrs : 
        jet_dir_mu = [ '%s/jet_fake_results__%s%s.pickle'%(result_dir, channelmu, v) for v in varstrs ]
        jet_dir_el = [ '%s/jet_fake_results__%s%s.pickle'%(result_dir,channelel, v) for v in varstrs ]
        ele_dir_el = [ '%s/electron_fake_results__%s%s.pickle'%(result_dir,channelel, v) for v in varstrs ]

    if channelmu is not None :
        make_hist_from_pickle( samplesWmugg, jet_dir_mu, '%s/JetFake/hist.root' %(result_dir), tag=channelmu, regions=regions, plot_binning=plot_binning, varname=varname )
        make_hist_from_pickle( samplesWmugg, jet_dir_mu, '%s/Muon/JetFake/hist.root' %(result_dir), tag='lgg', regions=regions, plot_binning=plot_binning, varname=varname  )

    if channelel is not None :
        make_hist_from_pickle( samplesWelgg, jet_dir_el, '%s/JetFake/hist.root' %(result_dir), tag=channelel, regions=regions, plot_binning=plot_binning, varname=varname  )
        make_hist_from_pickle( samplesWelgg, jet_dir_el, '%s/Electron/JetFake/hist.root' %(result_dir), tag='lgg', regions=regions, plot_binning=plot_binning, varname=varname  )

        if not channelel.count('Zgg') :
            make_hist_from_pickle( samplesWelgg, ele_dir_el, '%s/EleFake/hist.root' %(result_dir), tag=channelel, regions=regions, plot_binning=plot_binning, varname=varname   )
            make_hist_from_pickle( samplesWelgg, ele_dir_el, '%s/Electron/EleFake/hist.root' %(result_dir), tag='lgg', regions=regions, plot_binning=plot_binning, varname=varname   )

    # using summed hists
    if channelmu is not None :
        make_hist_from_pickle( samplesWmugg, '%s/jet_fake_results__%s.pickle'%(result_dir, channelmu), '%s/Muon/JetFake/hist.root' %(result_dir), tag='lgg', regions=regions, plot_binning=plot_binning )
    if channelel is not None :
        make_hist_from_pickle( samplesWelgg, '%s/jet_fake_results__%s.pickle'%(result_dir, channelel), '%s/Electron/JetFake/hist.root' %(result_dir), tag=channelel, regions=regions, plot_binning=plot_binning )
        if not channelel.count('Zgg') :
            make_hist_from_pickle( samplesWelgg, '%s/electron_fake_results__%s.pickle'%(result_dir,channelel), '%s/Electron/EleFake/hist.root' %(result_dir), tag=channelel, regions=regions, plot_binning=plot_binning  )


    # combine the electron and muon
    # directories into the Summed directory
    summed_dir = '%s/Summed' %(result_dir) 
    if not os.path.isdir( summed_dir ) :
        os.makedirs( summed_dir )
    if os.path.isdir( '%s/Electron' %(result_dir) ) :
        for dir in os.listdir( '%s/Electron' %(result_dir)  ) :
            if not os.path.isdir( '%s/%s' %( summed_dir, dir ) ) :
                os.makedirs( '%s/%s' %( summed_dir, dir ) )
            os.system( 'hadd -f %s/%s/hist.root %s/Electron/%s/hist.root %s/Muon/%s/hist.root' %( summed_dir, dir, result_dir,dir, result_dir, dir)  )
            os.system( 'cp %s/Electron/EleFake/hist.root %s/EleFake/hist.root ' %( result_dir, summed_dir ) )

def save_muon_hists( draw_str, weight_str, event_weight, aqgc_weight,  plot_binning, plot_dir, reg_tag, channel_tag, varname ) :

    hist_tag = '%s%s' %(channel_tag, reg_tag)

    # Draw without weight
    samplesWmugg.create_hist( 'Muon', varname, draw_str, plot_binning )

    #----------------------------
    # Data mgg
    #----------------------------
    hist_data_mgg = samplesWmugg.get_samples(name='Muon')[0].hist.Clone('%s_%s'%(varname, hist_tag))
    save_hist( '%s/Data/hist.root' %(plot_dir), hist_data_mgg )

    hist_data_mgg_pergev = hist_data_mgg.Clone( hist_data_mgg.GetName() + '_perGeV' )
    make_pergev_hist( hist_data_mgg, hist_data_mgg_pergev)
    save_hist( '%s/Data/hist.root' %(plot_dir), hist_data_mgg_pergev )

    #----------------------------
    # Data lgg
    #----------------------------
    hist_data_lgg = samplesWmugg.get_samples(name='Muon')[0].hist.Clone('%s_lgg%s'%(varname, reg_tag))
    save_hist( '%s/Muon/Data/hist.root' %(plot_dir), hist_data_lgg )

    hist_data_lgg_pergev = hist_data_lgg.Clone( hist_data_lgg.GetName() + '_perGeV' )
    make_pergev_hist( hist_data_lgg, hist_data_lgg_pergev)
    save_hist( '%s/Muon/Data/hist.root' %(plot_dir), hist_data_lgg_pergev )

    # Draw with weight
    #----------------------------
    # Wgg mgg
    #----------------------------
    success = samplesWmugg.create_hist( 'Wgg', varname, weight_str+event_weight+draw_str , plot_binning )
    if success : 
        hist_sig_mgg  = samplesWmugg.get_samples(name='Wgg')[0].hist.Clone('%s_%s'%(varname, hist_tag))
        save_hist( '%s/Wgg/hist.root' %(plot_dir), hist_sig_mgg )

        hist_sig_mgg_pergev = hist_sig_mgg.Clone( hist_sig_mgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_sig_mgg, hist_sig_mgg_pergev)
        save_hist( '%s/Wgg/hist.root' %(plot_dir), hist_sig_mgg_pergev )

        #----------------------------
        # Wgg lgg
        #----------------------------
        hist_sig_lgg  = samplesWmugg.get_samples(name='Wgg')[0].hist.Clone('%s_lgg%s'%(varname, reg_tag))
        save_hist( '%s/Muon/Wgg/hist.root' %(plot_dir), hist_sig_lgg )

        hist_sig_lgg_pergev = hist_sig_lgg.Clone( hist_sig_lgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_sig_lgg, hist_sig_lgg_pergev)
        save_hist( '%s/Muon/Wgg/hist.root' %(plot_dir), hist_sig_lgg_pergev )

    # Draw with weight
    #----------------------------
    # Wgg aQGC mgg
    #----------------------------
    success = samplesWmugg.create_hist( 'WAAQGCLT', varname, weight_str+aqgc_weight+draw_str , plot_binning )
    if success : 
        hist_sig_mgg  = samplesWmugg.get_samples(name='WAAQGCLT')[0].hist.Clone('%s_%s'%(varname, hist_tag))
        save_hist( '%s/WggAQGCLT50/hist.root' %(plot_dir), hist_sig_mgg )

        hist_sig_mgg_pergev = hist_sig_mgg.Clone( hist_sig_mgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_sig_mgg, hist_sig_mgg_pergev)
        save_hist( '%s/WggAQGCLT50/hist.root' %(plot_dir), hist_sig_mgg_pergev )

        #----------------------------
        # Wgg lgg
        #----------------------------
        hist_sig_lgg  = samplesWmugg.get_samples(name='WAAQGCLT')[0].hist.Clone('%s_lgg%s'%(varname, reg_tag))
        save_hist( '%s/Muon/WggAQGCLT50/hist.root' %(plot_dir), hist_sig_lgg )

        hist_sig_lgg_pergev = hist_sig_lgg.Clone( hist_sig_lgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_sig_lgg, hist_sig_lgg_pergev)
        save_hist( '%s/Muon/WggAQGCLT50/hist.root' %(plot_dir), hist_sig_lgg_pergev )

    #----------------------------
    # Zgg mgg
    #----------------------------
    # Draw with weight
    success = samplesWmugg.create_hist( 'Zgammagamma', varname, weight_str+event_weight+draw_str , plot_binning )

    if success : 
        hist_ZggFSR_mgg  = samplesWmugg.get_samples(name='Zgammagamma')[0].hist.Clone('%s_%s'%(varname, hist_tag))
        hist_ZggFSR_mgg_nosyst=hist_ZggFSR_mgg.Clone( '%s_%s'%(varname,hist_tag) )
        save_hist( '%s/ZggNoSyst/hist.root' %(plot_dir), hist_ZggFSR_mgg_nosyst )
        add_syst_to_hist( hist_ZggFSR_mgg, 0.1 )
        save_hist( '%s/Zgg/hist.root' %(plot_dir), hist_ZggFSR_mgg )

        hist_ZggFSR_mgg_pergev = hist_ZggFSR_mgg.Clone( hist_ZggFSR_mgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_ZggFSR_mgg, hist_ZggFSR_mgg_pergev)
        save_hist( '%s/Zgg/hist.root' %(plot_dir), hist_ZggFSR_mgg_pergev )
        #----------------------------
        # Zgg lgg
        #----------------------------
        hist_ZggFSR_lgg  = samplesWmugg.get_samples(name='Zgammagamma')[0].hist.Clone('%s_lgg%s'%(varname,reg_tag))
        hist_ZggFSR_lgg_nosyst = hist_ZggFSR_lgg.Clone( '%s_lgg%s'%(varname,reg_tag) )
        save_hist( '%s/Muon/ZggNoSyst/hist.root' %(plot_dir), hist_ZggFSR_lgg_nosyst )
        add_syst_to_hist( hist_ZggFSR_lgg, 0.1 )
        save_hist( '%s/Muon/Zgg/hist.root' %(plot_dir), hist_ZggFSR_lgg )

        hist_ZggFSR_lgg_pergev = hist_ZggFSR_lgg.Clone( hist_ZggFSR_lgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_ZggFSR_lgg, hist_ZggFSR_lgg_pergev)
        save_hist( '%s/Muon/Zgg/hist.root' %(plot_dir), hist_ZggFSR_lgg_pergev )

    #----------------------------
    # Other Di Photon mgg
    #----------------------------
    success = samplesWmugg.create_hist( 'OtherDiPhoton', varname, weight_str+draw_str , plot_binning )
    if success :
        hist_dip_mgg  = samplesWmugg.get_samples(name='OtherDiPhoton')[0].hist.Clone('%s_%s'%(varname,hist_tag))
        save_hist( '%s/OtherDiPhoton/hist.root' %(plot_dir), hist_dip_mgg )

        hist_dip_mgg_pergev = hist_dip_mgg.Clone( hist_dip_mgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_dip_mgg, hist_dip_mgg_pergev)
        save_hist( '%s/OtherDiPhoton/hist.root' %(plot_dir), hist_dip_mgg_pergev )
        #----------------------------
        # Other Di Photon lgg
        #----------------------------
        hist_dip_lgg  = samplesWmugg.get_samples(name='OtherDiPhoton')[0].hist.Clone('%s_lgg%s'%(varname,reg_tag))
        save_hist( '%s/Muon/OtherDiPhoton/hist.root' %(plot_dir), hist_dip_lgg )

        hist_dip_lgg_pergev = hist_dip_lgg.Clone( hist_dip_lgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_dip_lgg, hist_dip_lgg_pergev)
        save_hist( '%s/Muon/OtherDiPhoton/hist.root' %(plot_dir), hist_dip_lgg_pergev )
        #hist_Zgg_mgg     = samplesWmugg.get_samples(name='Zgg')[0].hist.Clone('%s_mgg%s'%(varname, reg_tag))
        #hist_Zgg_mgg.Add(hist_ZggFSR_mgg)
        #add_syst_to_hist( hist_Zgg_mgg, 0.15 )
        #save_hist( '%s/%s/Zgg/hist.root' %(baseDir, plotDir), hist_Zgg_mgg )


def save_electron_hists( draw_str, weight_str, event_weight, aqgc_weight,  plot_binning, plot_dir, reg_tag, channel_tag, varname ) :


    hist_tag = '%s%s' %(channel_tag, reg_tag)
    
    # draw without weight
    samplesWelgg.create_hist( 'Electron', varname, draw_str, plot_binning )

    #---------------------------
    # Data egg
    #---------------------------
    hist_data_egg = samplesWelgg.get_samples(name='Electron')[0].hist.Clone('%s_%s'%(varname,hist_tag))
    save_hist( '%s/Data/hist.root' %(plot_dir), hist_data_egg )

    hist_data_egg_pergev = hist_data_egg.Clone( hist_data_egg.GetName() + '_perGeV' )
    make_pergev_hist( hist_data_egg, hist_data_egg_pergev)
    save_hist( '%s/Data/hist.root' %(plot_dir), hist_data_egg_pergev )

    hist_data_lgg = samplesWelgg.get_samples(name='Electron')[0].hist.Clone('%s_lgg%s'%(varname,reg_tag))
    save_hist( '%s/Electron/Data/hist.root' %(plot_dir), hist_data_lgg )

    hist_data_lgg_pergev = hist_data_lgg.Clone( hist_data_lgg.GetName() + '_perGeV' )
    make_pergev_hist( hist_data_lgg, hist_data_lgg_pergev)
    save_hist( '%s/Data/hist.root' %(plot_dir), hist_data_lgg_pergev )

    #---------------------------
    # Wgg egg
    #---------------------------
    # draw with weight
    success = samplesWelgg.create_hist( 'Wgg', varname, weight_str+event_weight+draw_str, plot_binning )
    if success :
        hist_sig_egg  = samplesWelgg.get_samples(name='Wgg')[0].hist.Clone('%s_%s'%(varname, hist_tag))
        save_hist( '%s/Wgg/hist.root' %(plot_dir), hist_sig_egg )

        hist_sig_egg_pergev = hist_sig_egg.Clone( hist_sig_egg.GetName() + '_perGeV' )
        make_pergev_hist( hist_sig_egg, hist_sig_egg_pergev)
        save_hist( '%s/Wgg/hist.root' %(plot_dir), hist_sig_egg_pergev )

        hist_sig_lgg  = samplesWelgg.get_samples(name='Wgg')[0].hist.Clone('%s_lgg%s'%(varname, reg_tag))
        save_hist( '%s/Electron/Wgg/hist.root' %(plot_dir), hist_sig_lgg )

        hist_sig_lgg_pergev = hist_sig_lgg.Clone( hist_sig_lgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_sig_lgg, hist_sig_lgg_pergev)
        save_hist( '%s/Electron/Wgg/hist.root' %(plot_dir), hist_sig_lgg_pergev )

    #---------------------------
    # Wgg aQGC egg
    #---------------------------
    # draw with weight
    success = samplesWelgg.create_hist( 'WAAQGCLT', varname,  aqgc_weight+weight_str+draw_str, plot_binning )
    if success :
        hist_sig_egg  = samplesWelgg.get_samples(name='WAAQGCLT')[0].hist.Clone('%s_%s'%(varname,hist_tag))
        save_hist( '%s/WggAQGCLT50/hist.root' %(plot_dir), hist_sig_egg )

        hist_sig_egg_pergev = hist_sig_egg.Clone( hist_sig_egg.GetName() + '_perGeV' )
        make_pergev_hist( hist_sig_egg, hist_sig_egg_pergev)
        save_hist( '%s/WggAQGCLT50/hist.root' %(plot_dir), hist_sig_egg_pergev )

        hist_sig_lgg  = samplesWelgg.get_samples(name='WAAQGCLT')[0].hist.Clone('%s_lgg%s'%(varname,reg_tag))
        save_hist( '%s/Electron/WggAQGCLT50/hist.root' %(plot_dir), hist_sig_lgg )

        hist_sig_lgg_pergev = hist_sig_lgg.Clone( hist_sig_lgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_sig_lgg, hist_sig_lgg_pergev)
        save_hist( '%s/Electron/WggAQGCLT50/hist.root' %(plot_dir), hist_sig_lgg_pergev )

    #---------------------------
    # Zgg egg
    #---------------------------
    success = samplesWelgg.create_hist( 'Zgammagamma', varname, weight_str+event_weight+draw_str, plot_binning )

    if success :
        hist_Zgg_egg  = samplesWelgg.get_samples(name='Zgammagamma')[0].hist.Clone('%s_%s'%(varname, hist_tag))
        hist_Zgg_egg_nosyst= hist_Zgg_egg.Clone('%s_%s'%(varname, hist_tag) ) 

        save_hist( '%s/ZggNoSyst/hist.root' %(plot_dir), hist_Zgg_egg_nosyst )
        add_syst_to_hist( hist_Zgg_egg, 0.10 )
        save_hist( '%s/Zgg/hist.root' %(plot_dir), hist_Zgg_egg )

        hist_Zgg_egg_pergev = hist_Zgg_egg.Clone( hist_Zgg_egg.GetName() + '_perGeV' )
        make_pergev_hist( hist_Zgg_egg, hist_Zgg_egg_pergev)
        save_hist( '%s/Zgg/hist.root' %(plot_dir), hist_Zgg_egg_pergev )


        hist_Zgg_lgg  = samplesWelgg.get_samples(name='Zgammagamma')[0].hist.Clone('%s_lgg%s'%(varname,reg_tag))
        hist_Zgg_lgg_nosyst= hist_Zgg_lgg.Clone('%s_%s'%(varname, hist_tag) ) 

        save_hist( '%s/Electron/ZggNoSyst/hist.root' %(plot_dir), hist_Zgg_lgg_nosyst )
        add_syst_to_hist( hist_Zgg_lgg, 0.10 )
        save_hist( '%s/Electron/Zgg/hist.root' %(plot_dir), hist_Zgg_lgg )

        hist_Zgg_lgg_pergev = hist_Zgg_lgg.Clone( hist_Zgg_lgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_Zgg_lgg, hist_Zgg_lgg_pergev)
        save_hist( '%s/Electron/Zgg/hist.root' %(plot_dir), hist_Zgg_lgg_pergev )


    #---------------------------
    # OtherDiPhoton egg
    #---------------------------
    success = samplesWelgg.create_hist( 'OtherDiPhoton', varname, weight_str+draw_str, plot_binning )
    if success :
        hist_dip_egg  = samplesWelgg.get_samples(name='OtherDiPhoton')[0].hist.Clone('%s_%s'%(varname, hist_tag))
        save_hist( '%s/OtherDiPhoton/hist.root' %(plot_dir), hist_dip_egg )

        hist_dip_egg_pergev = hist_dip_egg.Clone( hist_dip_egg.GetName() + '_perGeV' )
        make_pergev_hist( hist_dip_egg, hist_dip_egg_pergev)
        save_hist( '%s/OtherDiPhoton/hist.root' %(plot_dir), hist_dip_egg_pergev )

        hist_dip_lgg  = samplesWelgg.get_samples(name='OtherDiPhoton')[0].hist.Clone('%s_lgg%s'%(varname, reg_tag))
        save_hist( '%s/Electron/OtherDiPhoton/hist.root' %(plot_dir), hist_dip_lgg )

        hist_dip_lgg_pergev = hist_dip_lgg.Clone( hist_dip_lgg.GetName() + '_perGeV' )
        make_pergev_hist( hist_dip_lgg, hist_dip_lgg_pergev)
        save_hist( '%s/Electron/OtherDiPhoton/hist.root' %(plot_dir), hist_dip_lgg_pergev )

def add_syst_to_hist( hist, syst, err_bin=[] ) :

    if not isinstance( err_bin, list ) :
        err_bin = [err_bin]

    bins = range( 1, hist.GetNbinsX() +1 )
    if err_bin :
        bins = err_bin

    for bin in bins :
        curr_err = hist.GetBinError( bin )
        curr_val = hist.GetBinContent( bin )
        new_err = math.sqrt( curr_err*curr_err + curr_val*syst*curr_val*syst )

        hist.SetBinError( bin, new_err )

def make_hist_from_pickle( sampMan, input_files, output_hist, tag, regions, plot_binning, varname='pt_leadph12', syst=None, sum_syst={} ) :

    if not isinstance( input_files, list ) :
        input_files = [input_files]

    datas = []
    for input_file in input_files :
        if not os.path.isfile( input_file) :
            print 'Could not find input file %s' %input_file
            continue
        ofile = open( input_file, 'r' )
        datas.append(pickle.load(ofile) )
        ofile.close()

    samp_list = sampMan.get_samples()
    sum_hist = None
    sum_data = {}
    for reg in regions :
        hist_binning = array('f', plot_binning)
        histname = '%s_%s_%s-%s' %(varname, tag, reg[0], reg[1] )
        hist = ROOT.TH1F( histname, histname, len(plot_binning)-1, hist_binning )
        sum_hist = hist.Clone( '%s_%s' %(varname, tag ) )

        # handle the case where the
        # histogram is the lead photon pT
        # assume this happens when only one file is passed
        if len( datas ) == 1 :
            data = datas[0]

            for ptbin in range( 1, hist.GetNbinsX()+1 ) :
                min = int(hist.GetXaxis().GetBinLowEdge(ptbin))
                max = int(hist.GetXaxis().GetBinUpEdge(ptbin))
                sum_data.setdefault(ptbin, ufloat(0, 0) )

                if max <= 15 :
                    continue

                maxval = str(max)
                if max >= 100 :
                    maxval = 'max'

                databin = ( reg[0] ,reg[1], str( min), maxval )

                if databin not in data['stat+syst']['sum'] :
                    print 'Skipping bin %s that does not exist' %(str(databin))
                    continue 

                hist.SetBinContent( ptbin, data['stat+syst']['sum'][databin]['result'].n )
                hist.SetBinError( ptbin, data['stat+syst']['sum'][databin]['result'].s )

                sum_data[ptbin] = sum_data[ptbin] + data['stat+syst']['sum'][databin]['result']

        elif len(datas) > 1 :

            # there should only be one pt bin
            testbin = datas[0]['stat+syst']['sum'].keys()[0]
            ptbin = (testbin[2], testbin[3])

            for idx, data in enumerate( datas ) :
                sum_data.setdefault(idx+1, ufloat(0, 0) )

                databin = ( reg[0], reg[1], ptbin[0], ptbin[1] )

                dataval = data['stat+syst']['sum'][databin]['result']
                hist.SetBinContent(idx+1, dataval.n )
                hist.SetBinError(idx+1, dataval.n )

                sum_data[idx+1] = sum_data[idx+1] + dataval

        save_hist( output_hist, hist )

        hist_pergev = hist.Clone( hist.GetName() + '_perGeV' )
        make_pergev_hist( hist, hist_pergev )

        save_hist( output_hist, hist_pergev)

    for ptbin in range( 1, hist.GetNbinsX()+1 ) :
        sum_hist.SetBinContent( ptbin, sum_data[ptbin].n )
        sum_hist.SetBinError( ptbin, sum_data[ptbin].s )


    if sum_syst :
        for bin, syst in sum_syst.iteritems() :
            new_syst = math.sqrt( syst*syst + sum_hist.GetBinError(bin)*sum_hist.GetBinError( bin ) )
            sum_hist.SetBinError( bin, new_syst )

    save_hist( output_hist, sum_hist )

    sum_hist_pergev = sum_hist.Clone( sum_hist.GetName() + '_perGeV' )
    make_pergev_hist( sum_hist, sum_hist_pergev )

    save_hist( output_hist, sum_hist_pergev )
    

def make_pergev_hist( hist, hist_pergev ) :

    hist_pergev.GetYaxis().SetTitle( 'Events / 5 GeV' )

    for ptbin in range( 1, hist_pergev.GetNbinsX()+1 ) :
        min = int(hist.GetXaxis().GetBinLowEdge(ptbin))
        max = int(hist.GetXaxis().GetBinUpEdge(ptbin))
        if max <= 15 :
            continue

        n_5gev = ( max - min ) / 5
        
        val_orig = hist.GetBinContent( ptbin )
        err_orig = hist.GetBinError( ptbin )

        val_new = val_orig/n_5gev
        err_new = err_orig/n_5gev

        hist_pergev.SetBinContent( ptbin, val_new )
        hist_pergev.SetBinError( ptbin, err_new )


def save_hist( file, hist) :

    dirname = os.path.split( file)[0] 
    if not os.path.isdir( dirname ) :
        os.makedirs( dirname ) 
    ofile = ROOT.TFile.Open( file, 'UPDATE' )

    hist.Write()

    ofile.Close()


def get_mapped_directory( base_dir_jet, jet_dirs_key ) :
    
    jet_dir_key_map = {}

    for dir in os.listdir( base_dir_jet ) :
        res = re.match( jet_dirs_key, dir )
        if res is not None :
            if len(res.groups() ) == 3 :
                jet_dir_key_map[ ( int(res.group(1)), int(res.group(2)), int(res.group(3)) ) ]  = dir
            elif len(res.groups()) == 0 :
                jet_dir_key_map[ ( 0,0,0 ) ]  = dir


    return jet_dir_key_map

def get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key ) :

    jet_files = {}
    for dir in os.listdir( base_dir_jet ) :
        res = re.match( jet_dirs_key, dir )
        if res is not None :
            iso_key = None
            if len(res.groups() ) == 3 :
                iso_key = ( int(res.group(1)), int(res.group(2)), int(res.group(3)) )
            elif len(res.groups() ) == 0 :
                iso_key = ( 0,0,0 )

            jet_files[iso_key] = {}

            for file in os.listdir( base_dir_jet+'/'+dir  ) :
                fresl = re.match(file_key, file )
                if fresl is not None :
                    if len(fresl.groups()) == 4 :
                        jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4))] = file
                    elif len(fresl.groups()) == 7 :
                        # if the gropus exist, but they're both none, then treat it like there are 4 groups
                        if fresl.group(6) is None and  fresl.group(7) is None :
                            jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4))] = file
                        else :
                            jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4), fresl.group(6), fresl.group(7))] = file
                    elif len(fresl.groups()) == 3 :
                        jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3))] = file

    return jet_files



def MakeEleBkgEstimateNew(base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, pt_bins, subl_pt_bins=None, fakeDir=None, outputDir=None, el_selection='elfull', addtlVar=None, addtlVarCuts=None, coarse=False) :

    print '-----------------------------------'
    print 'START NEW ELECTRON FAKE ESTMATE FOR %s' %el_selection
    print '-----------------------------------'

    el_acc = ['elfull', 'elzcr', 'elph1zcr', 'elph2zcr', 'elloose', 'elfulllowmt', 'elfullhighmt', 'elzcrlowmt', 'elzcrhighmt', 'ellooselowmt']
    if el_selection not in el_acc :
        raise NameError( 'Input region not recognized, must be %s' %(','.join(el_acc) ) )

    # Just use data samples
    samplesWggInvLead.deactivate_all_samples()
    samplesWggInvLead.activate_sample('Electron')
    samplesWggInvSubl.deactivate_all_samples()
    samplesWggInvSubl.activate_sample('Electron')

    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB')]

    addtl_cuts = ''
    addtl_str = ''
    if addtlVar is not None and addtlVarCuts is not None :
        addtl_cuts = ' && %s > %d && %s < %d ' %( addtlVar, addtlVarCuts[0], addtlVar, addtlVarCuts[1] )
        addtl_str = '__cut_%s_%d-%d' %( addtlVar, addtlVarCuts[0], addtlVarCuts[1] )

    # get fake factors from nominal fits
    results_nom = get_ele_fakefactors( base_dir_ele, file_bin_map, regions, el_selection, subl_pt_bins=subl_pt_bins, addtl_cuts=addtl_cuts, coarse=coarse )
    # disable alternate fits
    # get fake factors from systematic fits
    #results_syst = get_ele_fakefactors( base_dir_ele, file_bin_map_syst, regions, el_selection, addtl_cuts=addtl_cuts, coarse=coarse )

    results_comb = {'stat' : { 'lead' : {}, 'subl' : {}}, 'syst' : { 'lead' : {}, 'subl' : {}} , 'details' : { 'lead' : {}, 'subl' : {}} }
    for bin, res in results_nom['lead'].iteritems() :
        results_comb['stat']['lead'][bin] = res['pred']
        results_comb['details']['lead'][bin] = res
        ## Calculate the systematic uncertainty 
        ## as the difference between the nominal
        ## and syst fake factor predictions
        #if res['pred'] == 0 :
        #    results_comb['syst']['lead'][bin] = ufloat( res['pred'].n, res['pred'].n)
        #else :
        #    results_comb['syst']['lead'][bin] = ufloat( res['pred'].n, math.fabs( (res['pred'].n - results_syst['lead'][bin]['pred'].n))/res['pred'].n)
        results_comb['syst']['lead'][bin] = ufloat( res['pred'].n, _fakefactor_closure_syst*res['pred'].n )


    for bin, res in results_nom['subl'].iteritems() :
        results_comb['stat']['subl'][bin] = res['pred']
        results_comb['details']['subl'][bin] = res
        ## Calculate the systematic uncertainty 
        ## as the difference between the nominal
        ## and syst fake factor predictions
        #if res['pred'] == 0 :
        #    results_comb['syst']['subl'][bin] = ufloat( res['pred'].n, res['pred'].n)
        #else :
        #    results_comb['syst']['subl'][bin] = ufloat( res['pred'].n, math.fabs( (res['pred'].n - results_syst['subl'][bin]['pred'].n))/res['pred'].n)

        results_comb['syst']['subl'][bin] = ufloat( res['pred'].n, _fakefactor_closure_syst*res['pred'].n)

    file_jet_invlead = '%s/jet_fake_results__%sinvpixlead%s.pickle' %( base_dir_jet, el_selection, addtl_str )
    file_jet_invsubl = '%s/jet_fake_results__%sinvpixsubl%s.pickle' %( base_dir_jet, el_selection, addtl_str )

    print 'open invlead ', file_jet_invlead
    print 'open invsubl ', file_jet_invsubl

    ofile_lead = open( file_jet_invlead )
    results_jet_invlead = pickle.load( ofile_lead )
    ofile_lead.close()

    ofile_subl = open( file_jet_invsubl )
    results_jet_invsubl = pickle.load( ofile_subl )
    ofile_subl.close()

    # get fake factors and binning from file
    ff_man_coarse = FakeFactorManager( '%s/%s/results.pickle' %(base_dir_ele,fakeDir), ['fake_ratio'] )

    pt_bins_jetfile = []
    for idx, ptmin in enumerate(pt_bins[:-1]) :
        strptmin = str(ptmin)
        strptmax = str( pt_bins[idx+1] ) 
        if pt_bins[idx+1] == pt_bins[-1] :
            strptmax = 'max'
        pt_bins_jetfile.append( (strptmin, strptmax ) )

    jet_scaled = {'stat' : {}, 'syst' : {} }
    for r1, r2 in regions :

        for ptmin, ptmax in pt_bins_jetfile :

            if subl_pt_bins is not None :
                sublptmin = subl_pt_bins[0]
                sublptmax = subl_pt_bins[1]
            else :
                sublptmin = ptmin
                sublptmax = pt_bins_jetfile[-1][1]


            ff_lead = -1
            ff_subl = -1
            if r1 == 'EB' :
                ff_lead = ff_man_coarse.get_pt_eta_ff( ptmin, ptmax, 0.0, 1.44 )
            if r1 == 'EE' :
                ff_lead = ff_man_coarse.get_pt_eta_ff( ptmin, ptmax, 1.57, 2.5 )

            if r2 == 'EB' :
                ff_subl = ff_man_coarse.get_pt_eta_ff( sublptmin, sublptmax, 0.0, 1.44 )
            if r2 == 'EE' :
                ff_subl = ff_man_coarse.get_pt_eta_ff( sublptmin, sublptmax, 1.57, 2.50 )

            print 'Jet Fakes -- Region : %s-%s, Lead pt range : %s-%s, Subl pt range : %s-%s, fflead = %s, ffsubl = %s ' %( r1,r2,ptmin, ptmax, sublptmin, sublptmax, ff_lead, ff_subl )

            bin = (r1,r2,ptmin,ptmax)

            jet_scaled[bin] = {} 
             
            jet_scaled[bin]['pred_lead'] = results_jet_invlead['stat+syst']['sum'][bin]['result']
            jet_scaled[bin]['pred_subl'] = results_jet_invsubl['stat+syst']['sum'][bin]['result']

            jet_scaled[bin]['ff_lead'] = ff_lead

            jet_scaled[bin]['ff_subl'] = ff_subl

            jet_scaled[bin]['total'] = jet_scaled[bin]['pred_lead']*jet_scaled[bin]['ff_lead'] + jet_scaled[bin]['pred_subl']*jet_scaled[bin]['ff_subl']


    for r1, r2 in regions :

        for ptmin, ptmax in pt_bins_jetfile :
            print '%s-%s, pt %s-%s' %( r1, r2, ptmin, ptmax)

            bin = (r1,r2,ptmin,ptmax)

            print 'Jet fake, lead CR = %s ' %( jet_scaled[bin]['pred_lead'] )
            print 'Jet fake, subl CR = %s ' %( jet_scaled[bin]['pred_subl'] )

            print 'N jet fake lead*ff = %s' %(jet_scaled[bin]['pred_lead']*jet_scaled[bin]['ff_lead'])
            print 'N jet fake subl*ff = %s' %(jet_scaled[bin]['pred_subl']*jet_scaled[bin]['ff_subl'])

            print 'N data lead*ff = %s' %results_comb['stat']['lead'][bin]
            print 'N data subl*ff = %s' %results_comb['stat']['subl'][bin]
    
    results_subtracted = {'stat' : {'sum' : {}}, 'elesyst' : {'sum' : {}}, 'jetsyst' : {'sum' : {}}, 'stat+syst' : {'sum' : {}}, 'details' : {}}
    results_subtracted['details'] = results_comb['details']

    for bin, info_stat_lead in results_comb['stat']['lead'].iteritems() :
        info_stat_subl = results_comb['stat']['subl'][bin]
        info_syst_lead = results_comb['syst']['lead'][bin]
        info_syst_subl = results_comb['syst']['subl'][bin]

        results_subtracted['stat']['sum'][bin] = {}
        results_subtracted['elesyst']['sum'][bin] = {}
        results_subtracted['jetsyst']['sum'][bin] = {}
        results_subtracted['stat+syst']['sum'][bin] = {}

        # add some additional information to the
        # stat+syst entries
        results_subtracted['stat+syst']['sum'][bin]['jet_info'] = jet_scaled[bin]
        results_subtracted['stat+syst']['sum'][bin]['lead'] = info_stat_lead
        results_subtracted['stat+syst']['sum'][bin]['subl'] = info_stat_subl

        # stat uncertainty is just the 
        # difference in the stat entries
        results_subtracted['stat']['sum'][bin]['result'] = info_stat_lead +info_stat_subl - ( jet_scaled[bin]['total'] )

        # for elesyst set jet uncertainties to zero
        results_subtracted['elesyst']['sum'][bin]['result'] = info_syst_lead +info_syst_subl - ufloat( jet_scaled[bin]['total'].n, 0.0 )

        # for jetsyst set ele uncertainties to zero
        results_subtracted['jetsyst']['sum'][bin]['result'] = ufloat( (info_stat_lead +info_stat_subl).n, 0.0) - ( jet_scaled[bin]['total'] )

        # for comb, set ele and jet values to zero but keep their uncertainties
        elesyst_to_add = ufloat( 0, results_subtracted['elesyst']['sum'][bin]['result'].s )
        jetsyst_to_add = ufloat( 0, results_subtracted['jetsyst']['sum'][bin]['result'].s )
        final_result =  results_subtracted['stat']['sum'][bin]['result'] + elesyst_to_add + jetsyst_to_add
        results_subtracted['stat+syst']['sum'][bin]['result']    = resolve_negatives( final_result )

        print 'Ele pred Final %s-%s pt %s-%s = %s' %( bin[0], bin[1], bin[2], bin[3], results_subtracted['stat+syst']['sum'][bin]['result'] )


    #results_syst_subtracted = {}
    #results_syst_subtracted['stat+syst'] = {}
    #results_syst_subtracted['stat+syst']['sum'] = {}
    #for (r1,r2, ptmin, ptmax), val in results_syst.iteritems() :

    #    results_syst_subtracted['stat+syst']['sum'][bin] = {}

    #    results_syst_subtracted['stat+syst']['sum'][bin]['lead'] = info_lead
    #    results_syst_subtracted['stat+syst']['sum'][bin]['subl'] = info_subl
    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_rf'] = jet_scaled[bin]['rf']
    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_fr'] = jet_scaled[bin]['fr']
    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_ff'] = jet_scaled[bin]['ff']
    #    results_syst_subtracted['stat+syst']['sum'][bin]['result'] = info_lead['pred'] +info_subl['pred'] - ( jet_scaled[bin]['rf']['total'] + jet_scaled[bin]['fr']['total'] + jet_scaled[bin]['ff']['total'] )

    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

        file_raw = open( outputDir + '/electron_fake_results__%s__noJetFakeSubtraction%s.pickle' %(el_selection, addtl_str), 'w' )
        pickle.dump( results_nom, file_raw )
        file_raw.close()

        file_sub = open( outputDir + '/electron_fake_results__%s%s.pickle' %(el_selection, addtl_str), 'w' )
        pickle.dump( results_subtracted, file_sub )
        file_sub.close()

        #file_sub_syst = open( outputDir + '/electron_fake_results_syst%s.pickle' %channel, 'w' )
        #pickle.dump( results_syst_subtracted, file_sub_syst )
        #file_sub_syst.close()


#Use MakeEleBkgEstimateNew
#def MakeEleBkgEstimate(base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, pt_bins, outputDir=None, el_selection='elfull', namePostfix='', coarse=False) :
#
#    print '-----------------------------------'
#    print 'START ELECTRON FAKE ESTMATE FOR %s' %el_selection
#    print '-----------------------------------'
#
#    el_acc = ['elfull', 'elzcr', 'elph1zcr', 'elph2zcr']
#    if el_selection not in el_acc :
#        print 'Input region not recognized, must be %s' %(','.join(el_acc) )
#        return
#
#    # Just use data samples
#    samplesWggInvLead.deactivate_all_samples()
#    samplesWggInvLead.activate_sample('Electron')
#    samplesWggInvSubl.deactivate_all_samples()
#    samplesWggInvSubl.activate_sample('Electron')
#
#    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB')]
#
#    # get fake factors from nominal fits
#    results_nom = get_ele_fakefactors( base_dir_ele, file_bin_map, regions, el_selection, coarse=coarse )
#    # get fake factors from systematic fits
#    results_syst = get_ele_fakefactors( base_dir_ele, file_bin_map_syst, regions, el_selection, coarse=coarse )
#
#    results_comb = {'stat' : { 'lead' : {}, 'subl' : {}}, 'syst' : { 'lead' : {}, 'subl' : {}} , 'details' : { 'lead' : {}, 'subl' : {}} }
#    for bin, res in results_nom['lead'].iteritems() :
#        results_comb['stat']['lead'][bin] = res['pred']
#        results_comb['details']['lead'][bin] = res
#        # Calculate the systematic uncertainty 
#        # as the difference between the nominal
#        # and syst fake factor predictions
#        if res['pred'] == 0 :
#            results_comb['syst']['lead'][bin] = ufloat( res['pred'].n, res['pred'].n)
#        else :
#            results_comb['syst']['lead'][bin] = ufloat( res['pred'].n, math.fabs( (res['pred'].n - results_syst['lead'][bin]['pred'].n))/res['pred'].n)
#
#    for bin, res in results_nom['subl'].iteritems() :
#        results_comb['stat']['subl'][bin] = res['pred']
#        results_comb['details']['subl'][bin] = res
#        # Calculate the systematic uncertainty 
#        # as the difference between the nominal
#        # and syst fake factor predictions
#        if res['pred'] == 0 :
#            results_comb['syst']['subl'][bin] = ufloat( res['pred'].n, res['pred'].n)
#        else :
#            results_comb['syst']['subl'][bin] = ufloat( res['pred'].n, math.fabs( (res['pred'].n - results_syst['subl'][bin]['pred'].n))/res['pred'].n)
#
#    file_key_lead = 'results__%sinvpixlead__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
#    file_key_subl = 'results__%sinvpixsubl__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
#    file_key_lead_syst = 'results__syst__%sinvpixlead__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
#    file_key_subl_syst = 'results__syst__%sinvpixsubl__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
#    jet_dir_key_map = {}
#    jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'
#
#    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )
#
#    jet_files_lead      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead      )
#    jet_files_subl      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_subl      )
#    jet_files_lead_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead_syst )
#    jet_files_subl_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_subl_syst )
#
#    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
#    pt_bins_jetfile.append( 'max')
#    #subl_ptbins = [ ( '70', 'max', '15', '25' ), ( '70', 'max', '25', 'max' ) ]
#    subl_ptbins = [  ]
#    pred_lead = get_jet_fake_results( jet_files_lead, jet_files_lead_syst, regions, pt_bins_jetfile, jet_dir_key_map, base_dir_jet,  pt_bins_subl=subl_ptbins ) 
#    pred_subl = get_jet_fake_results( jet_files_subl, jet_files_subl_syst, regions, pt_bins_jetfile, jet_dir_key_map, base_dir_jet,  pt_bins_subl=subl_ptbins ) 
#
#    # get fake factors and binning from file
#    ff_man_coarse = FakeFactorManager( '%s/ElectronFakeFitsRatioCoarseEta/results.pickle' %base_dir_ele, ['fake_ratio'] )
#
#    jet_scaled = {'stat' : {}, 'syst' : {} }
#    for r1, r2 in regions :
#
#        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
#            ptmax = pt_bins_jetfile[idx+1]
#
#
#            ff_lead = -1
#            ff_subl = -1
#            if r1 == 'EB' :
#                ff_lead = ff_man_coarse.get_pt_eta_ff( ptmin, ptmax, 0.0, 1.44 )
#            if r1 == 'EE' :
#                ff_lead = ff_man_coarse.get_pt_eta_ff( ptmin, ptmax, 1.57, 2.5 )
#
#            if r2 == 'EB' :
#                ff_subl = ff_man_coarse.get_pt_eta_ff( 15, ptmax, 0.0, 1.44 )
#            if r2 == 'EE' :
#                ff_subl = ff_man_coarse.get_pt_eta_ff( 15, ptmax, 1.57, 2.50 )
#
#
#            bin = (r1,r2,ptmin,ptmax)
#            jet_scaled['stat'][bin] = {'rf' : {}, 'fr' : {}, 'ff' : {} }
#            jet_scaled['syst'][bin] = {'rf' : {}, 'fr' : {}, 'ff' : {} }
#
#             
#            jet_scaled['stat'][ bin ]['rf']['pred_lead'] = pred_lead['stat']['rf'][bin]['result']
#            jet_scaled['stat'][ bin ]['fr']['pred_lead'] = pred_lead['stat']['fr'][bin]['result']
#            jet_scaled['stat'][ bin ]['ff']['pred_lead'] = pred_lead['stat']['ff'][bin]['result']
#
#            jet_scaled['stat'][ bin ]['rf']['pred_subl'] = pred_subl['stat']['rf'][bin]['result']
#            jet_scaled['stat'][ bin ]['fr']['pred_subl'] = pred_subl['stat']['fr'][bin]['result']
#            jet_scaled['stat'][ bin ]['ff']['pred_subl'] = pred_subl['stat']['ff'][bin]['result']
#
#            jet_scaled['syst'][ bin ]['rf']['pred_lead'] = pred_lead['syst']['rf'][bin]['result']
#            jet_scaled['syst'][ bin ]['fr']['pred_lead'] = pred_lead['syst']['fr'][bin]['result']
#            jet_scaled['syst'][ bin ]['ff']['pred_lead'] = pred_lead['syst']['ff'][bin]['result']
#
#            jet_scaled['syst'][ bin ]['rf']['pred_subl'] = pred_subl['syst']['rf'][bin]['result']
#            jet_scaled['syst'][ bin ]['fr']['pred_subl'] = pred_subl['syst']['fr'][bin]['result']
#            jet_scaled['syst'][ bin ]['ff']['pred_subl'] = pred_subl['syst']['ff'][bin]['result']
#
#            jet_scaled['stat'][ bin ]['rf']['ff_lead'] = ff_lead
#            jet_scaled['stat'][ bin ]['fr']['ff_lead'] = ff_lead
#            jet_scaled['stat'][ bin ]['ff']['ff_lead'] = ff_lead
#
#            jet_scaled['stat'][ bin ]['rf']['ff_subl'] = ff_subl
#            jet_scaled['stat'][ bin ]['fr']['ff_subl'] = ff_subl
#            jet_scaled['stat'][ bin ]['ff']['ff_subl'] = ff_subl
#
#            # no additional FF syst at this point
#            jet_scaled['syst'][ bin ]['rf']['ff_lead'] = ff_lead
#            jet_scaled['syst'][ bin ]['fr']['ff_lead'] = ff_lead
#            jet_scaled['syst'][ bin ]['ff']['ff_lead'] = ff_lead
#
#            jet_scaled['syst'][ bin ]['rf']['ff_subl'] = ff_subl
#            jet_scaled['syst'][ bin ]['fr']['ff_subl'] = ff_subl
#            jet_scaled['syst'][ bin ]['ff']['ff_subl'] = ff_subl
#
#            jet_scaled['stat'][ bin ]['rf']['total'] = jet_scaled['stat'][ bin ]['rf']['pred_lead']*jet_scaled['stat'][ bin ]['rf']['ff_lead'] + jet_scaled['stat'][ bin ]['rf']['pred_subl']*jet_scaled['stat'][ bin ]['rf']['ff_subl']
#            jet_scaled['stat'][ bin ]['fr']['total'] = jet_scaled['stat'][ bin ]['fr']['pred_lead']*jet_scaled['stat'][ bin ]['fr']['ff_lead'] + jet_scaled['stat'][ bin ]['fr']['pred_subl']*jet_scaled['stat'][ bin ]['fr']['ff_subl']
#            jet_scaled['stat'][ bin ]['ff']['total'] = jet_scaled['stat'][ bin ]['ff']['pred_lead']*jet_scaled['stat'][ bin ]['ff']['ff_lead'] + jet_scaled['stat'][ bin ]['ff']['pred_subl']*jet_scaled['stat'][ bin ]['ff']['ff_subl']
#
#
#            jet_scaled['syst'][ bin ]['rf']['total'] = jet_scaled['syst'][ bin ]['rf']['pred_lead']*jet_scaled['syst'][ bin ]['rf']['ff_lead'] + jet_scaled['syst'][ bin ]['rf']['pred_subl']*jet_scaled['syst'][ bin ]['rf']['ff_subl']
#            jet_scaled['syst'][ bin ]['fr']['total'] = jet_scaled['syst'][ bin ]['fr']['pred_lead']*jet_scaled['syst'][ bin ]['fr']['ff_lead'] + jet_scaled['syst'][ bin ]['fr']['pred_subl']*jet_scaled['syst'][ bin ]['fr']['ff_subl']
#            jet_scaled['syst'][ bin ]['ff']['total'] = jet_scaled['syst'][ bin ]['ff']['pred_lead']*jet_scaled['syst'][ bin ]['ff']['ff_lead'] + jet_scaled['syst'][ bin ]['ff']['pred_subl']*jet_scaled['syst'][ bin ]['ff']['ff_subl']
#
#
#    for r1, r2 in regions :
#
#        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
#            ptmax = pt_bins_jetfile[idx+1]
#            print '%s-%s, pt %s-%s' %( r1, r2, ptmin, ptmax)
#
#            bin = (r1,r2,ptmin,ptmax)
#
#            print 'Jet fake, lead CR : rf = %s, fr = %s, ff = %s, sum = %s ' %( jet_scaled['stat'][bin]['rf']['pred_lead'], jet_scaled['stat'][bin]['fr']['pred_lead'], jet_scaled['stat'][bin]['ff']['pred_lead'], jet_scaled['stat'][bin]['rf']['pred_lead']+jet_scaled['stat'][bin]['fr']['pred_lead']+jet_scaled['stat'][bin]['ff']['pred_lead'])
#            print 'Jet fake, subl CR : rf = %s, fr = %s, ff = %s, sum = %s ' %( jet_scaled['stat'][bin]['rf']['pred_subl'], jet_scaled['stat'][bin]['fr']['pred_subl'], jet_scaled['stat'][bin]['ff']['pred_subl'], jet_scaled['stat'][bin]['rf']['pred_subl']+jet_scaled['stat'][bin]['fr']['pred_subl']+jet_scaled['stat'][bin]['ff']['pred_subl'])
#
#            print 'N jet fake lead*ff = %s' %((jet_scaled['stat'][bin]['rf']['pred_lead']+jet_scaled['stat'][bin]['fr']['pred_lead']+jet_scaled['stat'][bin]['ff']['pred_lead']) * ff_lead )
#            print 'N jet fake subl*ff = %s' %((jet_scaled['stat'][bin]['rf']['pred_subl']+jet_scaled['stat'][bin]['fr']['pred_subl']+jet_scaled['stat'][bin]['ff']['pred_subl']) * ff_subl )
#            print 'N data lead*ff = %s' %results_comb['stat']['lead'][bin]
#            print 'N data subl*ff = %s' %results_comb['stat']['subl'][bin]
#    
#    results_subtracted = {'stat' : {'sum' : {}}, 'elesyst' : {'sum' : {}}, 'jetsyst' : {'sum' : {}}, 'stat+syst' : {'sum' : {}}, 'details' : {}}
#    results_subtracted['details'] = results_comb['details']
#    for bin, info_stat_lead in results_comb['stat']['lead'].iteritems() :
#        info_stat_subl = results_comb['stat']['subl'][bin]
#        info_syst_lead = results_comb['syst']['lead'][bin]
#        info_syst_subl = results_comb['syst']['subl'][bin]
#
#        results_subtracted['stat']['sum'][bin] = {}
#        results_subtracted['elesyst']['sum'][bin] = {}
#        results_subtracted['jetsyst']['sum'][bin] = {}
#        results_subtracted['stat+syst']['sum'][bin] = {}
#
#        # add some additional information to the
#        # stat+syst entries
#        results_subtracted['stat+syst']['sum'][bin]['lead'] = info_stat_lead
#        results_subtracted['stat+syst']['sum'][bin]['subl'] = info_stat_subl
#        results_subtracted['stat+syst']['sum'][bin]['jet_rf'] = jet_scaled['stat'][bin]['rf']
#        results_subtracted['stat+syst']['sum'][bin]['jet_fr'] = jet_scaled['stat'][bin]['fr']
#        results_subtracted['stat+syst']['sum'][bin]['jet_ff'] = jet_scaled['stat'][bin]['ff']
#
#        # stat uncertainty is just the 
#        # difference in the stat entries
#        results_subtracted['stat']['sum'][bin]['result'] = info_stat_lead +info_stat_subl - ( jet_scaled['stat'][bin]['rf']['total'] + jet_scaled['stat'][bin]['fr']['total'] + jet_scaled['stat'][bin]['ff']['total'] )
#
#        # for elesyst set jet uncertainties to zero
#        results_subtracted['elesyst']['sum'][bin]['result'] = info_syst_lead +info_syst_subl - ufloat( (jet_scaled['stat'][bin]['rf']['total'] + jet_scaled['stat'][bin]['fr']['total'] + jet_scaled['stat'][bin]['ff']['total']).n, 0.0 )
#
#        # for jetsyst set ele uncertainties to zero
#        results_subtracted['jetsyst']['sum'][bin]['result'] = ufloat( (info_stat_lead +info_stat_subl).n, 0.0) - ( jet_scaled['syst'][bin]['rf']['total'] + jet_scaled['syst'][bin]['fr']['total'] + jet_scaled['syst'][bin]['ff']['total'] )
#
#        # for comb, set ele and jet values to zero but keep their uncertainties
#        elesyst_to_add = ufloat( 0, results_subtracted['elesyst']['sum'][bin]['result'].s )
#        jetsyst_to_add = ufloat( 0, results_subtracted['jetsyst']['sum'][bin]['result'].s )
#        results_subtracted['stat+syst']['sum'][bin]['result']    = results_subtracted['stat']['sum'][bin]['result'] + elesyst_to_add + jetsyst_to_add
#
#        print 'Ele pred Final %s-%s pt %s-%s = %s' %( bin[0], bin[1], bin[2], bin[3], results_subtracted['stat+syst']['sum'][bin]['result'] )
#
#
#
#    #results_syst_subtracted = {}
#    #results_syst_subtracted['stat+syst'] = {}
#    #results_syst_subtracted['stat+syst']['sum'] = {}
#    #for (r1,r2, ptmin, ptmax), val in results_syst.iteritems() :
#
#    #    results_syst_subtracted['stat+syst']['sum'][bin] = {}
#
#    #    results_syst_subtracted['stat+syst']['sum'][bin]['lead'] = info_lead
#    #    results_syst_subtracted['stat+syst']['sum'][bin]['subl'] = info_subl
#    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_rf'] = jet_scaled[bin]['rf']
#    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_fr'] = jet_scaled[bin]['fr']
#    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_ff'] = jet_scaled[bin]['ff']
#    #    results_syst_subtracted['stat+syst']['sum'][bin]['result'] = info_lead['pred'] +info_subl['pred'] - ( jet_scaled[bin]['rf']['total'] + jet_scaled[bin]['fr']['total'] + jet_scaled[bin]['ff']['total'] )
#
#    if outputDir is not None :
#        if not os.path.isdir( outputDir ) :
#            os.makedirs( outputDir )
#
#        file_raw = open( outputDir + '/electron_fake_results%s__noJetFakeSubtraction.pickle' %namePostfix, 'w' )
#        pickle.dump( results_nom, file_raw )
#        file_raw.close()
#
#        file_sub = open( outputDir + '/electron_fake_results%s.pickle' %namePostfix, 'w' )
#        pickle.dump( results_subtracted, file_sub )
#        file_sub.close()
#
#        #file_sub_syst = open( outputDir + '/electron_fake_results_syst%s.pickle' %namePostfix, 'w' )
#        #pickle.dump( results_syst_subtracted, file_sub_syst )
#        #file_sub_syst.close()


def get_ele_fakefactors( base_dir_ele, file_bin_map, regions, el_selection, subl_pt_bins=None, addtl_cuts='', coarse=False ) :

    results = {}
    results['lead'] = {}
    results['subl'] = {}

    data_samp_invlead = samplesWggInvLead.get_samples( name='Electron' )[0]
    data_samp_invsubl = samplesWggInvSubl.get_samples( name='Electron' )[0]

    for r1, r2 in regions :

        # -----------------------------------
        # Lead CR draw string
        # draw once and make cuts
        # for all lead pt and eta
        # -----------------------------------
        draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 )' %(el_cuts[el_selection+'invlead'], r1, r2)

        if subl_pt_bins is not None :
            if subl_pt_bins[1] is not None :
                draw_str += ' && pt_sublph12 > %d && pt_sublph12 < %d ' %( subl_pt_bins )
            else :
                draw_str += ' && pt_sublph12 > %d ' %( subl_pt_bins[0] )

        if addtl_cuts :
            draw_str += addtl_cuts

        samplesWggInvLead.create_hist(data_samp_invlead, 'pt_leadph12:fabs(eta_leadph12)', draw_str, ( 250, 0, 2.5, 20, 0, 100) )

        hist_lead = data_samp_invlead.hist.Clone('hist_lead__%s-%s' %(r1,r2))

        # -----------------------------------------
        # Get data counts in each pt and eta region
        # and multiply by the fake factor
        # -----------------------------------------
        for (leadptmin, leadptmax), file in file_bin_map.iteritems() :

            fffile = '%s/%s/results.pickle' %(base_dir_ele, file)
            print 'Get fake factors from %s ' %fffile

            ff_man = FakeFactorManager( fffile, ['fake_ratio'] )

            bin = (r1, r2, leadptmin, leadptmax)

            results['lead'][bin] = {}
            results['lead'][bin]['pred'] = ufloat(0, 0)

            eta_map = _eta_pt_bin_map
            if coarse :
                eta_map = _eta_pt_bin_map_coarse
            

            for etamin, etamax in eta_map[(leadptmin,leadptmax)][r1]  :


                # get the bins.  For the max bin subtract 1 because
                # you get the bin above the value
                leadptbinmin = hist_lead.GetYaxis().FindBin( float(leadptmin) )
                if leadptmax == 'max' :
                    leadptbinmax = hist_lead.GetNbinsY()
                else :
                    leadptbinmax = hist_lead.GetYaxis().FindBin( float(leadptmax) ) - 1

                leadetabinmin = hist_lead.GetXaxis().FindBin( float(etamin) )
                leadetabinmax = hist_lead.GetXaxis().FindBin( float(etamax) ) - 1

                dataerr = ROOT.Double()
                nData = hist_lead.IntegralAndError( leadetabinmin, leadetabinmax, leadptbinmin, leadptbinmax, dataerr )

                data = ufloat( nData, dataerr )

                ff = ff_man.get_pt_eta_ff( leadptmin, leadptmax, etamin, etamax )

                print 'LEAD : ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptbinmax = %d, etabinmin = %d, etabinmax = %d, data = %s, ff = %s, pred = %s ' %( leadptmin, leadptmax, etamin, etamax, leadptbinmin, leadptbinmax, leadetabinmin, leadetabinmax, data, ff, data*ff )

                ff_bin = ( str(etamin), str(etamax), leadptmin, leadptmax )

                results['lead'][bin][ff_bin] = {}
                results['lead'][bin][ff_bin]['data'] = data
                results['lead'][bin][ff_bin]['ff'] = ff
                results['lead'][bin][ff_bin]['pred'] = results['lead'][bin][ff_bin]['data']*(results['lead'][bin][ff_bin]['ff'] )
                #results['lead'][bin][ff_bin]['pred'] = results['lead'][bin][ff_bin]['data']*(results['lead'][bin][ff_bin]['ff']/(1-results['lead'][bin][ff_bin]['ff']) )

                # sum the results
                results['lead'][bin]['pred'] = results['lead'][bin]['pred'] + results['lead'][bin][ff_bin]['pred']
            # -----------------------------------------
            # Subl control region
            # Get data counts in each pt and eta region
            # and multiply by the fake factor
            # the sublead pT range starts at 15
            # and goes to the maximum lead pt
            # -----------------------------------------
            bin = (r1, r2, leadptmin, leadptmax)
            results['subl'][bin] = {}
            results['subl'][bin]['pred'] = ufloat(0, 0)


            # -----------------------------------
            # Subl CR draw string
            # draw once for each lead pT bin and make cuts
            # for all sublead pt and eta
            # -----------------------------------

            if leadptmax == 'max' :
                # draw exactly what is in ntuple
                draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %s )' %(el_cuts[el_selection+'invsubl'], r1, r2, leadptmin)
            else :
                draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %s && pt_leadph12 < %s )' %(el_cuts[el_selection+'invsubl'], r1, r2, leadptmin, leadptmax)

            if addtl_cuts :
                draw_str += addtl_cuts
            samplesWggInvSubl.create_hist(data_samp_invsubl, 'pt_sublph12:fabs(eta_sublph12)', draw_str,  (250, 0, 2.5, 20, 0, 100) )

            hist_subl = data_samp_invsubl.hist.Clone('hist_subl__%s-%s_leadpt%s-%s' %(r1,r2, leadptmin, leadptmax))

            # if no sublead bin is given, 
            # the sublead bins should go from
            # the minimum lead bin to the max bin
            sublbins = []
            if subl_pt_bins is not None :
                sublbins.append( (str(subl_pt_bins[0]), str(subl_pt_bins[1]) ) )
            else :
                for (sublptmin, sublptmax) in file_bin_map.keys() :
                    if leadptmax == 'max' :
                        # this includes all subl bins
                        sublbins.append( (sublptmin, sublptmax) )
                    else :
                        # only include bins up the the max lead bin
                        # if sublptmax is max and lead is not then don't include it
                        if not sublptmax == 'max' :
                            if int(sublptmax) <= int(leadptmax) :
                                sublbins.append( (sublptmin, sublptmax) )


            for (sublptmin, sublptmax) in sublbins :

                for subletamin, subletamax in eta_map[(sublptmin,sublptmax)][r2] :


                    sublptbinmin = hist_subl.GetYaxis().FindBin( float(sublptmin) )
                    if sublptmax == 'max' :
                        sublptbinmax = hist_subl.GetNbinsY()
                    else :
                        sublptbinmax = hist_subl.GetYaxis().FindBin( float(sublptmax) ) - 1

                    subletabinmin = hist_subl.GetXaxis().FindBin( float(subletamin) )
                    subletabinmax = hist_subl.GetXaxis().FindBin( float(subletamax) ) - 1

                    dataerr = ROOT.Double()
                    nData = hist_subl.IntegralAndError( subletabinmin, subletabinmax, sublptbinmin, sublptbinmax, dataerr )

                    data = ufloat( nData, dataerr )

                    ff = ff_man.get_pt_eta_ff( sublptmin, sublptmax, subletamin, subletamax )

                    print 'SUBLEAD : leadptmin = %s, leadptmax = %s, ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptbinmax = %d, etabinmin = %d, etabinmax = %d, data = %s, ff= %s, pred = %s ' %(leadptmin, leadptmax, sublptmin, sublptmax, subletamin, subletamax, sublptbinmin, sublptbinmax, subletabinmin, subletabinmax, data, ff, data*ff )

                    ff_bin = ( str(subletamin), str(subletamax), str(sublptmin), str(sublptmax) )

                    results['subl'][bin][ff_bin] = {}
                    results['subl'][bin][ff_bin]['data'] = data
                    results['subl'][bin][ff_bin]['ff'] =  ff
                    results['subl'][bin][ff_bin]['pred'] = results['subl'][bin][ff_bin]['data']*results['subl'][bin][ff_bin]['ff']
                    #results['subl'][bin][ff_bin]['pred'] = results['subl'][bin][ff_bin]['data']*(results['subl'][bin][ff_bin]['ff']/(1-results['subl'][bin][ff_bin]['ff']) )

                    results['subl'][bin]['pred'] = results['subl'][bin]['pred'] +results['subl'][bin][ff_bin]['pred']

    for bin, res in results['lead'].iteritems() :
        print 'Invert LEAD bin : %s, predicted = %s' %( bin, res['pred'] )
    for bin, res in results['subl'].iteritems() :
        print 'Invert SUBL bin : %s, predicted = %s' %( bin, res['pred'] )

    return results


def get_jet_fake_results( jet_files, jet_files_syst, regions, pt_bins,  jet_dir_key_map, base_dir_jet, pt_bins_subl=[] ) :
    """ Get the fake results for all pt and eta regions 
    
        Check if the data counts that were input to the 
        fit are non-zero.  If so, move to a looser isolation.
        If the values are never set, ie even in the loosest
        case there are no data counts, then use the 
        original with zero values
    """

    results = {'stat' : {}, 'syst' : {}, 'stat+syst' : {} }
    for val in results.values() :
       val['rf'] = {}
       val['fr'] = {}
       val['ff'] = {}
       val['sum'] = {}


    sorted_jet_dirs = jet_files.keys()
    sorted_jet_dirs.sort()

    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins[:-1]) :
            ptmax = pt_bins[idx+1]

            reg_bin = (r1, r2, ptmin, ptmax) 

            make_background_estimate( base_dir_jet, jet_files, jet_files_syst, jet_dir_key_map, sorted_jet_dirs, reg_bin, results )

        for ptlmin, ptlmax, ptsmin, ptsmax in pt_bins_subl :

            reg_bin = (r1, r2, ptlmin, ptlmax, ptsmin, ptsmax )

            make_background_estimate( base_dir_jet, jet_files, jet_files_syst, jet_dir_key_map, sorted_jet_dirs, reg_bin, results )

    return results

def make_background_estimate( base_dir_jet, jet_files, jet_files_syst, jet_dir_key_map, sorted_jet_dirs, reg_bin, results ) :

    for val in results.values() :
        val['rf'][reg_bin] = {}
        val['fr'][reg_bin] = {}
        val['ff'][reg_bin] = {}
        val['sum'][reg_bin] = {}

    for dir_key in sorted_jet_dirs :
        
        fentries = jet_files[dir_key]
        fentries_syst = jet_files_syst[dir_key]

        if reg_bin not in fentries :

            print 'Bin not found', reg_bin
            print fentries
            print jet_files
            continue

        # get the file 
        sub_dir_jet = jet_dir_key_map[dir_key]

        file_loc = base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin]

        if not os.path.isfile( file_loc ) :
            continue

        ofile = open(file_loc)
        predictions = pickle.load(ofile)
        ofile.close()

        file_loc_syst = base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin]
        ofile = open(file_loc_syst)
        predictions_syst = pickle.load(ofile)
        ofile.close()

        # get the data
        Ndata_tt = predictions['Ndata_TT']
        Ndata_tl = predictions['Ndata_TL']
        Ndata_lt = predictions['Ndata_LT']
        Ndata_ll = predictions['Ndata_LL']

        if Ndata_tl == 0 or Ndata_lt == 0 or Ndata_ll == 0 :
            print 'No data entries for AsymIso %d-%d-%d, region %s-%s, pt %s-%s ' %( dir_key[0], dir_key[1], dir_key[2], reg_bin[0], reg_bin[1], reg_bin[2], reg_bin[3])
            print 'Ndata_tl = %s, Ndata_lt = %s, Ndata_ll = %s' %( Ndata_tl, Ndata_lt, Ndata_ll)
            continue

        Npred_rf = predictions['Npred_RF_TT']
        Npred_fr = predictions['Npred_FR_TT']
        Npred_ff = predictions['Npred_FF_TT']

        Npred_rf_syst = predictions_syst['Npred_RF_TT']
        Npred_fr_syst = predictions_syst['Npred_FR_TT']
        Npred_ff_syst = predictions_syst['Npred_FF_TT']

        results['stat']['rf'][reg_bin]['result'] = Npred_rf
        results['stat']['fr'][reg_bin]['result'] = Npred_fr
        results['stat']['ff'][reg_bin]['result'] = Npred_ff

        syst_asym = _asym_iso_syst[(dir_key[0], dir_key[1], dir_key[2])]

        results['syst']['rf'][reg_bin]['result'] = Npred_rf_syst* ufloat( 1.0, syst_asym )
        results['syst']['fr'][reg_bin]['result'] = Npred_fr_syst* ufloat( 1.0, syst_asym )
        results['syst']['ff'][reg_bin]['result'] = Npred_ff_syst* ufloat( 1.0, syst_asym )

        pred_sum = Npred_ff+Npred_rf+Npred_fr
        pred_sum_syst = results['syst']['rf'][reg_bin]['result']+results['syst']['fr'][reg_bin]['result']+results['syst']['ff'][reg_bin]['result']

        if Ndata_tt > 0 and pred_sum.n > Ndata_tt.n :
            print 'Changing prediction from %s to %s' %( pred_sum, ufloat( Ndata_tt.n, (pred_sum.s/pred_sum.n)*Ndata_tt.n ) )
            pred_sum = ufloat( Ndata_tt.n, (pred_sum.s/pred_sum.n)*Ndata_tt.n )
            pred_sum_syst = ufloat( Ndata_tt.n, (pred_sum_syst.s/pred_sum_syst.n)*Ndata_tt.n )


        results['stat']['sum'][reg_bin]['result'] = pred_sum
        results['syst']['sum'][reg_bin]['result'] = pred_sum_syst

        Npred_rf_tot = Npred_rf
        Npred_fr_tot = Npred_fr
        Npred_ff_tot = Npred_ff

        Npred_rf_syst_zero =ufloat( 0, results['syst']['rf'][reg_bin]['result'].s )
        Npred_fr_syst_zero =ufloat( 0, results['syst']['fr'][reg_bin]['result'].s )
        Npred_ff_syst_zero =ufloat( 0, results['syst']['ff'][reg_bin]['result'].s )

        # do sum for stat+syst
        Npred_rf_tot += Npred_rf_syst_zero
        Npred_fr_tot += Npred_fr_syst_zero
        Npred_ff_tot += Npred_ff_syst_zero
        
        results['stat+syst']['rf'][reg_bin]['result'] = Npred_rf_tot
        results['stat+syst']['fr'][reg_bin]['result'] = Npred_fr_tot
        results['stat+syst']['ff'][reg_bin]['result'] = Npred_ff_tot
        results['stat+syst']['sum'][reg_bin]['result'] = results['stat+syst']['rf'][reg_bin]['result'] + results['stat+syst']['fr'][reg_bin]['result'] + results['stat+syst']['ff'][reg_bin]['result']

        break

    # if results weren't set in any cases above, 
    # get the results from the first entry
    if not results['stat']['rf'][reg_bin] or not results['stat']['fr'][reg_bin] or not results['stat']['ff'][reg_bin] :

        if reg_bin not in fentries :
            print 'Bin not found', reg_bin
            return

        dir_key = sorted_jet_dirs[0]

        fentries = jet_files[dir_key]

        sub_dir_jet = jet_dir_key_map[dir_key]
        file_loc = base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin]
        if not os.path.isfile( file_loc ) :
            print 'Could not locate file ', file_loc
            return
        ofile = open(file_loc)
        predictions = pickle.load(ofile)
        ofile.close()

        ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin])
        predictions_syst = pickle.load(ofile)
        ofile.close()

        Npred_rf = predictions['Npred_RF_TT']
        Npred_fr = predictions['Npred_FR_TT']
        Npred_ff = predictions['Npred_FF_TT']

        syst_asym = _asym_iso_syst[(dir_key[0], dir_key[1], dir_key[2])]

        Npred_rf_syst = predictions_syst['Npred_RF_TT']
        Npred_fr_syst = predictions_syst['Npred_FR_TT']
        Npred_ff_syst = predictions_syst['Npred_FF_TT']

        results['stat']['rf'][reg_bin]['result'] = Npred_rf
        results['stat']['fr'][reg_bin]['result'] = Npred_fr
        results['stat']['ff'][reg_bin]['result'] = Npred_ff
        results['stat']['sum'][reg_bin]['result'] = Npred_ff+Npred_rf+Npred_fr

        results['syst']['rf'][reg_bin]['result'] = Npred_rf_syst* ufloat( 1.0, syst_asym )
        results['syst']['fr'][reg_bin]['result'] = Npred_fr_syst* ufloat( 1.0, syst_asym )
        results['syst']['ff'][reg_bin]['result'] = Npred_ff_syst* ufloat( 1.0, syst_asym )
        results['syst']['sum']['raw_asym'] = syst_asym
        results['syst']['sum'][reg_bin]['result'] = results['syst']['rf'][reg_bin]['result'] + results['syst']['fr'][reg_bin]['result'] + results['syst']['ff'][reg_bin]['result']

        Npred_rf_tot = Npred_rf
        Npred_fr_tot = Npred_fr
        Npred_ff_tot = Npred_ff

        Npred_rf_syst_zero =ufloat( 0, results['syst']['rf'][reg_bin]['result'].s )
        Npred_fr_syst_zero =ufloat( 0, results['syst']['fr'][reg_bin]['result'].s )
        Npred_ff_syst_zero =ufloat( 0, results['syst']['ff'][reg_bin]['result'].s )

        Npred_rf_tot += Npred_rf_syst_zero
        Npred_fr_tot += Npred_fr_syst_zero
        Npred_ff_tot += Npred_ff_syst_zero
        
        results['stat+syst']['rf'][reg_bin]['result'] = Npred_rf_tot
        results['stat+syst']['fr'][reg_bin]['result'] = Npred_fr_tot
        results['stat+syst']['ff'][reg_bin]['result'] = Npred_ff_tot
        results['stat+syst']['sum'][reg_bin]['result'] = Npred_rf_tot+Npred_fr_tot+Npred_ff_tot

if __name__ == '__main__' :
    main()
