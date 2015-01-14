"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('--baseDir',      default=None,           dest='baseDir',         help='Path to base directory containing all ntuples')
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
p.add_argument('--readHists',     default=False,action='store_true',   dest='readHists',         help='read histograms from root files instead of trees')
p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')
p.add_argument('--ptmin',     default=0, type=int,   dest='ptmin',         help='Only use the pt bin starting at ptmin')
p.add_argument('--etabinmin',     default=-1, type=int,   dest='etabinmin',         help='Only use the eta bin starting at etabinmin')

p.add_argument('--bw_cms_fine',     default=False, action='store_true',  dest='bw_cms_fine', help='Fit Signal Breit wigner convoluted with crysal ball and background CMS shape, fine eta bins')
p.add_argument('--bw_cms_coarse',     default=False, action='store_true',  dest='bw_cms_coarse', help='Fit Signal Breit wigner convoluted with crysal ball and background CMS shape, coarse eta bins')

p.add_argument('--bw_exp_fine',     default=False, action='store_true',  dest='bw_exp_fine', help='Fit Signal Breit wigner convoluted with crysal ball and background exp shape, fine eta bins')
p.add_argument('--bw_exp_coarse',     default=False, action='store_true',  dest='bw_exp_coarse', help='Fit Signal Breit wigner convoluted with crysal ball and background exp shape, coarse eta bins')

p.add_argument('--ndkeys_cms_fine',     default=False, action='store_true',  dest='ndkeys_cms_fine', help='Fit Signal MC Gaussian smeared and background CMS shape, fine eta bins')
p.add_argument('--ndkeys_cms_coarse',     default=False, action='store_true',  dest='ndkeys_cms_coarse', help='Fit Signal MC Gaussian smeared and background CMS shape, coarse eta bins')
p.add_argument('--ndkeys_exp_fine',     default=False, action='store_true',  dest='ndkeys_exp_fine', help='Fit Signal MC Gaussian smeared and background Exponential shape, fine eta bins')
p.add_argument('--ndkeys_exp_coarse',     default=False, action='store_true',  dest='ndkeys_exp_coarse', help='Fit Signal MC Gaussian smeared and background Exponential shape, coarse eta bins')
p.add_argument('--useCsev',     default=False, action='store_true',  dest='useCsev', help='Use conversion save electron veto instead of pixel seed veto')
p.add_argument('--useTAndP',     default=False, action='store_true',  dest='useTAndP', help='Use tag and probe ntuples')



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
import random
import collections
import pickle
from uncertainties import ufloat
from uncertainties import unumpy

from SampleManager import SampleManager
from SampleManager import Sample
from data_pair import data_pair
from RooFitBase import fit_model_to_data, draw_fitted_results, SetHistContentBins


if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
else :
    ROOT.gROOT.SetBatch(False)

sampMan = None

global_hists={}

def get_default_draw_commands( ) :

    #return { 'FF' :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==1 && ph_elMinDR[0]>0.2 && ph_elMinDR[1]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_eta[0])<2.5 && fabs(ph_eta[1]) < 2.5' , 
    #         'RF'  :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && ph_elMinDR[0]>0.2  && ph_elMinDR[1]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_eta[0])<2.5 && fabs(ph_eta[1]) < 2.5',
    #         'FR'  :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && ph_elMinDR[0]>0.2 && ph_elMinDR[1]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_eta[0])<2.5 && fabs(ph_eta[1]) < 2.5',
    #         'RR' :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_elMinDR[0]>0.2  && ph_elMinDR[1]>0.2  && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_eta[0])<2.5 && fabs(ph_eta[1]) < 2.5',
    #       }

    return { 'FF' :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==1 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_eta[0])<2.5 && fabs(ph_eta[1]) < 2.5' , 
             'RF'  :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && ph_elMinDR[0]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_eta[0])<2.5 && fabs(ph_eta[1]) < 2.5',
             'FR'  :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && ph_elMinDR[1]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_eta[0])<2.5 && fabs(ph_eta[1]) < 2.5',
             'RR' :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_eta[0])<2.5 && fabs(ph_eta[1]) < 2.5',
           }

def get_ratio_draw_commands( isConv=None, useCsev=False, useTAndP=False ) :

    if isConv==False :

        return { 
                 'nom'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && !ph_isConv[0]',
                 'inv'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && !ph_isConv[0]',
               }
    elif isConv==True :

        return { 
                 'nom'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && ph_isConv[0]',
                 'inv'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && ph_isConv[0]',
               }
    elif useCsev :

        if useTAndP :
            return { 
                     'nom'  :'probe_isPhoton && probe_eleVeto == 0 ',
                     'inv'  :'probe_isPhoton && probe_eleVeto == 1 ',
                   }
        else :
            return { 
                     'nom'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_eleVeto[0]==0 ',
                     'inv'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_eleVeto[0]==1 ',
                   }
    else :
        if useTAndP:
            return { 
                     'nom'  :'probe_isPhoton && probe_hasPixSeed == 0 ',
                     'inv'  :'probe_isPhoton && probe_hasPixSeed == 1 ',
                   }
        else :

            return { 
                     'nom'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==0 ',
                     'inv'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==1 ',
                     #'inv'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] ',
                   }


def get_fit_defaults( histname, useGaussSig=False, useLandauSig=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False ) :

    defaults = {}

    bkg='cmsshape'

    sig='bw'
    if useGaussSig :
        sig='Gauss'
    if useLandauSig :
        sig='Landau'

    if usePolyBkg :
        bkg = 'poly'
    if useExpBkg :
        bkg = 'exp'
    if useChebyBkg:
        bkg = 'cheby'
    if useBernsteinBkg:
        bkg = 'bernstein'

    defaults['bw_cmsshape'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 40, 'fit_max' : 160 }
    defaults['Gauss_cmsshape'] = { 'mean' : 0, 'sigma' : 2.495, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3  }
    defaults['Landau_cmsshape'] = { 'mean' : 90, 'sigma' : 10, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 40, 'fit_max' : 180 }

    #defaults['bw_poly'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'poly_linear' : -0.008, 'poly_quadratic' : -0.00002, 'poly_cubic' : 0.0000002,  'poly_quartic' : 0.001, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 160 }
    defaults['bw_poly'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'poly_linear' : 10, 'poly_quadratic' : -0.05, 'poly_cubic' : -0.00001,  'poly_quartic' : 0.0000001, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 160 }
    defaults['Gauss_poly'] = { 'mean' : 0, 'sigma' : 2.495, 'poly_linear' : 1, 'poly_quadratic' : 4, 'poly_cubic' : 3, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3  }

    defaults['bw_exp'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'exp_width' : 0.05, 'exp_start' : 80, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
    defaults['Gauss_exp'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : 0.05, 'exp_start' : 80, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }

    defaults['bw_cheby'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'a0' : -0.05, 'a1' : -0.05, 'a2' : 0.5, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
    defaults['Gauss_cheby'] = { 'mean' : 0, 'sigma' : 2.495, 'a0' : 0.01, 'a1' : -0.1, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }

    defaults['bw_bernstein'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'b0' : 1, 'b1' : 1, 'b2' : 2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
    defaults['Gauss_bernstein'] = { 'mean' : 0, 'sigma' : 2.495, 'b0' : 1, 'b1' : 1, 'b2' : 1, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }

    alts = {'bw_cmsshape' : {}, 'Gauss_cmsshape' : {}, 'bw_poly' : {}, 'Gauss_poly' : {}, 'bw_exp' : {}, 'Gauss_exp' : {}, 'bw_cheby' : {} , 'Gauss_cheby' : { }, 'bw_bernstein' : {}, 'Gauss_bernstein' : {}, 'Landau_cmsshape' : {} }

    alts['bw_cmsshape']['fit_inv_eta_1.57-2.50_pt_25-40']     = { 'Bias' : -1.0, 'Width' : 3.0 , 'Cut' : -8, 'Power' : 30, 'cms_alpha' : 100, 
                                                                 'cms_beta' : 0.08, 'cms_gamma' : 0.3, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                                 'fit_min': 40, 'fit_max' : 160 }

    alts['bw_cmsshape']['fit_inv_eta_2.40-2.50_pt_25-40']     = { 'Bias' : 0.38, 'Width' : 3.4 , 'Cut' : -3.7, 'Power' : 30, 'cms_alpha' : 100, 
                                                                 'cms_beta' : 0.1, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                                 'fit_min': 40, 'fit_max' : 160 }

    alts['bw_cmsshape']['fit_nom_eta_0.00-0.10_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 110, 
                                                                  'cms_beta' : 0.027, 'cms_gamma' : 0.029, 'cms_peak' : 91, 'nsig' : 6500, 'nbkg' : 1000, 
                                                                   'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.19, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 100, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_nom_eta_0.10-0.50_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 110, 
                                                                 'cms_beta' : 0.027, 'cms_gamma' : 0.034, 'cms_peak' : 88, 'nsig' : 17000, 'nbkg' : 3700, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_inv_eta_0.10-0.50_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.1, 'Power' : 30, 'cms_alpha' : 114, 
                                                                 'cms_beta' : 0.034, 'cms_gamma' : 0.043, 'cms_peak' : 88, 'nsig' : 18000, 'nbkg' : 700, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_nom_eta_0.50-1.00_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.3, 'Power' : 30, 'cms_alpha' : 99, 
                                                                 'cms_beta' : 0.03, 'cms_gamma' : 0.03, 'cms_peak' : 87, 'nsig' : 18000, 'nbkg' : 4400, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_inv_eta_0.50-1.00_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.1, 'Power' : 30, 'cms_alpha' : 113, 
                                                                 'cms_beta' : 0.023, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 23000, 'nbkg' : 500, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_inv_eta_1.00-1.44_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 110, 
                                                                 'cms_beta' : 0.03, 'cms_gamma' : 0.04, 'cms_peak' : 89, 'nsig' : 30000, 'nbkg' : 1400, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_nom_eta_1.57-2.10_pt_40-70']     = { 'Bias' : 1.4, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 98, 
                                                                 'cms_beta' : 0.027, 'cms_gamma' : 0.022, 'cms_peak' : 88, 'nsig' : 13000, 'nbkg' : 2800, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_inv_eta_1.57-2.10_pt_40-70']     = { 'Bias' : 1.4, 'Width' : 3.0 , 'Cut' : -3, 'Power' : 10, 'cms_alpha' : 99, 
                                                                 'cms_beta' : 0.048, 'cms_gamma' : 0.031, 'cms_peak' : 88, 'nsig' : 7700, 'nbkg' : 400, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_inv_eta_2.10-2.20_pt_40-70']     = { 'Bias' : 1.4, 'Width' : 3.0 , 'Cut' : -3, 'Power' : 10, 'cms_alpha' : 99, 
                                                                 'cms_beta' : 0.048, 'cms_gamma' : 0.031, 'cms_peak' : 88, 'nsig' : 7700, 'nbkg' : 400, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_nom_eta_2.10-2.20_pt_40-70']     = { 'Bias' : 1.5, 'Width' : 2.9 , 'Cut' : -3.6, 'Power' : 10, 'cms_alpha' : 150, 
                                                                 'cms_beta' : 0.022, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 2600, 'nbkg' : 400, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_inv_eta_2.20-2.30_pt_40-70']     = { 'Bias' : 1.8, 'Width' : 2.7 , 'Cut' : -3.3, 'Power' : 30, 'cms_alpha' : 200, 
                                                                 'cms_beta' : 0.022, 'cms_gamma' : 0.09, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_inv_eta_2.30-2.40_pt_40-70']     = { 'Bias' : 2.0, 'Width' : 2.8 , 'Cut' : -1.06, 'Power' : 30, 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.037, 'cms_gamma' : 0.015, 'cms_peak' : 88, 'nsig' : 11000, 'nbkg' : 500, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_nom_eta_2.30-2.40_pt_40-70']     = { 'Bias' : 2.0, 'Width' : 2.8 , 'Cut' : -1.06, 'Power' : 30, 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.037, 'cms_gamma' : 0.015, 'cms_peak' : 88, 'nsig' : 11000, 'nbkg' : 500, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    alts['bw_cmsshape']['fit_inv_eta_2.40-2.50_pt_40-70']     = { 'Bias' : 2, 'Width' : 2.8 , 'Cut' : -1.2, 'Power' : 30, 'cms_alpha' : 143, 
                                                                 'cms_beta' : 0.0234, 'cms_gamma' : 0.044, 'cms_peak' : 88, 'nsig' : 12000, 'nbkg' : 670, 
                                                                 'fit_min': 40, 'fit_max' : 180 }
    #alts['bw_cmsshape']['fit_nom_eta_2.40-2.50_pt_40-70']    = { 'Bias' : 2.0, 'Width' : 2.8 , 'Cut' : -1.06, 'Power' : 30, 'cms_alpha' : 100, 
    #                                                             'cms_beta' : 0.024, 'cms_gamma' : 0.014, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 620, 
    #                                                             'fit_min': 40, 'fit_max' : 180 }

    alts['bw_cmsshape']['fit_nom_eta_0.00-0.10_pt_70-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.26, 'Power' : 30, 'cms_alpha' : 172, 
                                                                 'cms_beta' : 0.023, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 60, 'nbkg' : 130, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_70-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                                 'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :50 , 'nbkg' : 10, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_0.10-0.50_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :200 , 'nbkg' : 150, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_nom_eta_0.10-0.50_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :200 , 'nbkg' : 150, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_0.00-1.44_pt_70-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 172, 
                                                                 'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :150 , 'nbkg' : 70, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_0.50-1.00_pt_70-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 172, 
                                                                 'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :150 , 'nbkg' : 70, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_70-max']    = { 'Bias' : -0.7, 'Width' : 2 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 180, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 40, 'nbkg' : 40, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_0.10-0.50_pt_70-max']    = { 'Bias' : -0.05, 'Width' : 2 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 180, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 40, 'nbkg' : 40, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_1.00-1.44_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_1.57-2.10_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_nom_eta_2.10-2.40_pt_70-max']    = { 'Bias' : 1.76, 'Width' : 1.7 , 'Cut' : -0.57, 'Power' : 8, 'cms_alpha' : 200, 
                                                                 'cms_beta' : 0.006, 'cms_gamma' : 0.0002, 'cms_peak' : 88.7, 'nsig' : 80, 'nbkg' : 400, 
                                                                 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_2.10-2.40_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 160 }

    alts['Gauss_cmsshape']['fit_nom_eta_0.00-0.10_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                                 'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                                 'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 46, 
                                                                 'cms_beta' : 0.09, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_15-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                                 'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_15-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                                 'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_15-25']  = { 'mean' : 0.8, 'sigma' : 1.6 , 'cms_alpha' : 50, 
                                                                 'cms_beta' : 0.09, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_15-25']  = { 'mean' : 1.6, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                                 'cms_beta' : 0.1, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }

    alts['Gauss_cmsshape']['fit_nom_eta_0.00-1.44_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 70, 
                                                                 'cms_beta' : 0.05, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                                 'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.50_pt_25-40']  = { 'mean' : 1.2, 'sigma' : 1.7 , 'cms_alpha' : 70, 
                                                                 'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                                 'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.04, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 150, 
                                                                 'cms_beta' : 0.03, 'cms_gamma' : 0.12, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 50000, 'nbkg' : 1000, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }

    alts['Gauss_cmsshape']['fit_inv_eta_0.00-1.44_pt_40-70']  = { 'mean' : 0.33, 'sigma' : 0.4 , 'cms_alpha' : 100, 
                                                                 'cms_beta' : 0.03, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                                 'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 120, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.10-0.50_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 100, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_40-70']  = { 'mean' : 1.1, 'sigma' : 0.8 , 'cms_alpha' : 112, 
                                                                 'cms_beta' : 0.023, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 23000, 'nbkg' : 470, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 100, 
                                                                 'cms_beta' : 0.03, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 1000, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 120, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.30_pt_40-70']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 100, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.090, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.30_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.40_pt_40-70']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 100, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.090, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.40_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.30-2.40_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.30-2.40_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_40-70']  = { 'mean' : 2, 'sigma' : 1.9 , 'cms_alpha' : 90, 
                                                                 'cms_beta' : 0.03, 'cms_gamma' : 0.02, 'cms_peak' : 88, 'nsig' : 12000, 'nbkg' : 670, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }


    alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
    alts['Gauss_cmsshape']['fit_nom_eta_0.10-0.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.10-0.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.00-1.44_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
    alts['Gauss_cmsshape']['fit_nom_eta_0.50-1.00_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
    alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.2, 'nSigma' : 0.5 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
    alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.40_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.3, 'nSigma' : 1 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.40_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.4, 'nSigma' : 0.6 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                                 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                                 'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }

    alts['Gauss_exp']['fit_inv_eta_0.10-0.50_pt_40-70'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : 0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_0.00-0.10_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_1.00-1.44_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 75, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_1.57-2.10_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 75, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_2.10-2.20_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_2.20-2.30_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_2.30-2.40_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_2.40-2.50_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_nom_eta_0.00-0.10_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.01, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 70, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_0.00-0.10_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.01, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 80, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_0.10-0.50_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.05, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 85, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_nom_eta_1.00-1.44_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.05, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_1.00-1.44_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.05, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_nom_eta_1.57-2.10_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.0, 'exp_width' : -0.05, 'nsig' : 10000, 'nbkg' : 30000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_1.57-2.10_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_nom_eta_2.10-2.20_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_2.10-2.20_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_nom_eta_2.20-2.30_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_2.20-2.30_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_nom_eta_2.30-2.40_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_2.30-2.40_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_nom_eta_2.40-2.50_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
    alts['Gauss_exp']['fit_inv_eta_2.40-2.50_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }

    alts['bw_exp']['fit_inv_eta_0.00-0.10_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 140 }
    alts['bw_exp']['fit_nom_eta_1.00-1.44_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :160 }
    alts['bw_exp']['fit_inv_eta_1.00-1.44_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :200 }
    alts['bw_exp']['fit_nom_eta_1.57-2.10_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :160 }
    alts['bw_exp']['fit_inv_eta_1.57-2.10_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.1, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :160 }

    alts['bw_exp']['fit_nom_eta_0.00-0.10_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
    alts['bw_exp']['fit_inv_eta_0.00-0.10_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :140 }
    alts['bw_exp']['fit_nom_eta_0.10-0.50_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
    alts['bw_exp']['fit_inv_eta_0.10-0.50_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :140 }
    alts['bw_exp']['fit_nom_eta_0.50-1.00_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
    alts['bw_exp']['fit_inv_eta_0.50-1.00_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :140 }
    alts['bw_exp']['fit_nom_eta_1.00-1.44_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
    alts['bw_exp']['fit_inv_eta_1.00-1.44_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :140 }
    alts['bw_exp']['fit_nom_eta_1.57-2.10_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
    alts['bw_exp']['fit_inv_eta_1.57-2.10_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
    alts['bw_exp']['fit_nom_eta_2.10-2.20_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
    alts['bw_exp']['fit_inv_eta_2.10-2.20_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }
    alts['bw_exp']['fit_nom_eta_2.20-2.30_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
    alts['bw_exp']['fit_inv_eta_2.20-2.30_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }
    alts['bw_exp']['fit_nom_eta_2.30-2.40_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
    alts['bw_exp']['fit_inv_eta_2.30-2.40_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }
    alts['bw_exp']['fit_nom_eta_2.40-2.50_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
    alts['bw_exp']['fit_inv_eta_2.40-2.50_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }

    alts['bw_exp']['fit_nom_eta_2.10-2.40_pt_70-max'] = { 'Bias' : -0.3, 'Width' : 0.5 , 'Cut' : -0.1, 'Power' : 30, 'exp_width' : 0.015, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }
    if histname in alts[sig+'_'+bkg] :
        return alts[sig+'_'+bkg][histname]
    else :
        return defaults[sig+'_'+bkg]

def main() :

    global sampMan

    if not options.baseDir.count('/eos/') and not os.path.isdir( options.baseDir ) :
        print 'baseDir not found!'
        return

    sampMan = SampleManager(options.baseDir, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)


    if options.samplesConf is not None :

        sampMan.ReadSamples( options.samplesConf )

        print 'Samples ready.\n'  

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

    #useHist = '.EleFitData'
    useHist = None
        
    #DoElectronFakeSimpleClosure( outputDir=options.outputDir )



    #CompTrigNoTrig( outputDir = options.outputDir )

    #DoElectronFakeFit( outputDir=options.outputDir,useHist='.EleFit3dAbsEtaWithEleVeto' )
    #DoElectronFakeFit( outputDir=options.outputDir )

    #DoElectronFakeRatioClosure(  outputDir=options.outputDir )

    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=False, doNDKeys=False, usePolyBkg=True, useExpBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=False, doNDKeys=False, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=True, doNDKeys=False, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)
    #--------------------------
    # Use MC template for syst. studies
    #--------------------------
    #DoElectronFakeFitRatio( outputDir=options.outputDir, sample='Data', useHist='.EleFit3dRatioAbsEtaWithEleVetoConv', useMCTemplate=False, useCoarseEta=True, useCsev=options.useCsev, useTAndP=options.useTAndP )

    #DoElectronFakeFitRatio( outputDir=options.outputDir, sample='Data', isConv=True, useHist='.EleFit3dRatioAbsEtaWithEleVetoMCConv', useMCTemplate=True, useCsev=options.useCsev, useTAndP=options.useTAndP )

    #--------------------------
    # Use bw x cb with cms shape bkg
    # For nominal fits at high pt
    #--------------------------
    if options.bw_cms_fine :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=False, useMCTemplate=False, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)
    if options.bw_cms_coarse :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=True, useMCTemplate=False, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)


    #--------------------------
    # Use MC template with NDKeys smearing with cms shape bkg
    # For nominal fits
    #--------------------------
    #extra_bkg_sample = 'Zgamma'
    extra_bkg_sample = None
    if options.ndkeys_cms_fine :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=False, useMCTemplate=True, doNDKeys=True, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, extra_bkg_sample=extra_bkg_sample, useCsev=options.useCsev, useTAndP=options.useTAndP)
    if options.ndkeys_cms_coarse :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=True, useMCTemplate=True, doNDKeys=True, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    #--------------------------
    # Use MC template with exponential bkg
    # For syst variations
    #--------------------------
    if options.ndkeys_exp_fine :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=False, useMCTemplate=True, doNDKeys=True, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)
    if options.ndkeys_exp_coarse :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=True, useMCTemplate=True, doNDKeys=True, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    #--------------------------
    # Use bw x cb with exponential bkg
    # For syst variations
    #--------------------------
    if options.bw_exp_fine :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=False, useMCTemplate=False, doNDKeys=False, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)
    if options.bw_exp_coarse :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=True, useMCTemplate=False, doNDKeys=False, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    ##--------------------------
    ## Use Landau Sig with cmsshap bkg
    ##--------------------------
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=False, doNDKeys=False, useLandauSig=True, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    ##--------------------------
    ## Use MC template with cms shape bkg
    ##--------------------------
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=True, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

def CompTrigNoTrig( outputDir=None ) :

    subdir = 'CompTrigNoTrigMC'

    pt_bins = [15, 20, 25, 30, 40, 50, 60, 80, 100, 200 ] 
    eta_bins = [-2.5, -2.3, -2.1, -1.9, -1.7, -1.5, -1.3, -1.1, -0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]

    mass_binning = (100, 0, 200)

    draw_commands = get_default_draw_commands()

    plots_notrig = get_mass_histograms(draw_commands['FF'], draw_commands['FF'], draw_commands['FR'], draw_commands['RF'], 'NoTrig', mass_binning )
    plots_withtrig = get_mass_histograms(draw_commands['FF'], draw_commands['FF'], draw_commands['FR'], draw_commands['RF'], 'WithTrig', mass_binning )

    ff_notrig   = get_fake_factors_counts( plots_notrig, pt_bins, eta_bins, (81, 106) )
    ff_withtrig = get_fake_factors_counts( plots_withtrig, pt_bins, eta_bins, (81, 106) )

    ffhist_withtrig_eta = bin_map_to_hist( ff_withtrig['eta'], 'ffhist_withtrig_eta' )
    ffhist_withtrig_pt  = bin_map_to_hist( ff_withtrig['pt'],  'ffhist_withtrig_pt' )

    ffhist_notrig_eta = bin_map_to_hist( ff_notrig['eta'], 'ffhist_notrig_eta' )
    ffhist_notrig_pt  = bin_map_to_hist( ff_notrig['pt'],  'ffhist_notrig_pt' )

    ffhist_notrig_eta.SetLineColor(ROOT.kRed)
    ffhist_notrig_eta.SetMarkerColor(ROOT.kRed)
    ffhist_notrig_pt.SetLineColor(ROOT.kRed)
    ffhist_notrig_pt.SetMarkerColor(ROOT.kRed)


    ffhist_withtrig_pt.Draw()
    ffhist_notrig_pt.Draw('same')
    raw_input('continue')

    ffhist_withtrig_eta.Draw()
    ffhist_notrig_eta.Draw('same')
    raw_input('continue')


def DoElectronFakeFit( outputDir=None, useHist=None) :

    subdir = 'ElectronFakeFits'
    if outputDir is not None :
        outputDir = outputDir + '/' + subdir

    pt_bins = [ 15, 25, 40, 80, 1000000 ]
    #pt_bins = [ 80, 1000000 ]
    #eta_bins = [-2.5, -2.1, -1.57, -1.44, -0.1, 0.1, 1.44, 1.57, 2.1, 2.5]
    eta_bins = [0.0, 0.1, 1.44, 1.57, 2.1, 2.5]
    mass_binning = (50, 0, 200)

    draw_cmds = get_default_draw_commands( )
    selection_2fake_trig_taglead = draw_cmds['FF'] + ' && ph_trigMatch_el[0] == 1 && ph_pt[0]>30'
    selection_2fake_trig_tagsubl = draw_cmds['FF'] + ' && ph_trigMatch_el[1] == 1 && ph_pt[1]>30 '
    selection_1fake_trig_taglead = draw_cmds['FR'] + ' && ph_trigMatch_el[0] == 1 && ph_pt[0]>30 '
    selection_1fake_trig_tagsubl = draw_cmds['RF'] + ' && ph_trigMatch_el[1] == 1 && ph_pt[1]>30 '

    #plots = get_mass_histograms(selection_2fake, selection_2fake, selection_1fake_tagsubl, selection_1fake_taglead, 'NoTrig', mass_binning )
    plots = get_3d_mass_histograms(selection_2fake_trig_taglead, selection_2fake_trig_tagsubl, selection_1fake_trig_tagsubl, selection_1fake_trig_taglead, 'Data', mass_binning, useHist=useHist, useAbsEta=True )


    ffresults = get_fake_factors_3d_fit( plots, pt_bins, eta_bins, outputDir=outputDir )

    print ffresults

def DoElectronFakeFitRatio( outputDir=None, sample='Data', isConv=None, useCsev=False, useTAndP=False, useHist=None, useCoarseEta=False, useMCTemplate=False, useLandauSig=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, doNDKeys=False, extra_bkg_sample=None) :

    subdir = 'ElectronFakeFitsRatio'
    if useCsev :
        subdir += 'CSEV'
    if useTAndP :
        subdir += 'TAndP'
    if sample != 'Data' :
        subdir += sample
    if useMCTemplate :
        subdir += 'MCTemplate'
    if useLandauSig:
        subdir += 'LandauSig'
    if doNDKeys :
        subdir += 'NDKeys'
    if usePolyBkg :
        subdir += 'PolyBkg'
    if useExpBkg:
        subdir += 'ExpBkg'
    if useChebyBkg:
        subdir += 'ChebyBkg'
    if useBernsteinBkg:
        subdir += 'BernsteinBkg'
    if isConv == False :
        subdir += 'NoConv'
    if isConv == True :
        subdir += 'Conv'
    if extra_bkg_sample is not None :
        subdir += 'Subtract%s' %extra_bkg_sample
    if useCoarseEta :
        subdir += 'CoarseEta'

    useCmsShapeBkg=True
    if usePolyBkg or useExpBkg or useChebyBkg or useBernsteinBkg :
        useCmsShapeBkg = False

    if outputDir is not None :
        outputDir = outputDir + '/' + subdir

    #pt_bins = [ 15, 20,25,30, 35, 40,45, 50, 60, 70]
    #pt_bins_80 = [ 70, 100, 1000000 ]

    pt_bins = [(15,25), (25,40), (40,70), (15, 40), (15, 70), (15, 1000000) ]
    pt_bins_80 = [ (70, 1000000) ]

    #eta_bins = [-2.5, -2.1, -1.57, -1.44, -0.1, 0.1, 1.44, 1.57, 2.1, 2.5]
    eta_bins = [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44), (1.57, 2.1), (2.1, 2.2), (2.2, 2.4), (2.4, 2.5) ]
    eta_bins_80 = [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44), (1.57, 2.1), (2.1, 2.4), (2.4, 2.5) ]
    #eta_bins = [2.1, 2.5]
    mass_binning = (100, 0, 200)

    if useCoarseEta :
        eta_bins = [(0.0, 1.44), (1.57, 2.5)]
        eta_bins_80 = [(0.0, 1.44), (1.57, 2.5)]

    pt_eta_bins = {}
    for pts in pt_bins :
        pt_eta_bins[pts] = eta_bins
        
    for pts in pt_bins_80 :
        pt_eta_bins[pts] = eta_bins_80
        

    draw_cmds = get_ratio_draw_commands(isConv=isConv, useCsev=useCsev, useTAndP=useTAndP )
    selection_nom = draw_cmds['nom'] 
    selection_inv = draw_cmds['inv'] 

    hists = get_3d_mass_ratio_histograms( selection_nom, selection_inv, sample, mass_binning, useHist=useHist, useAbsEta=True, useTAndP=useTAndP )

    if useMCTemplate :
        hists_extra={'nom' : None, 'inv' : None }
        if extra_bkg_sample is not None :
            hists_extra = get_3d_mass_ratio_histograms( selection_nom, selection_inv, extra_bkg_sample, mass_binning, useHist=useHist, useAbsEta=True, useTAndP=useTAndP )
        
        if doNDKeys :
            results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, ndKeysSample='DYJetsToLLPhOlap', ndKeysSelection=selection_nom, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, extraBkgHist=hists_extra['nom'], useTAndP=options.useTAndP, outputDir =outputDir, namePrefix='_nom' )
            results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, ndKeysSample='DYJetsToLLPhOlap', ndKeysSelection=selection_inv, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, extraBkgHist=hists_extra['inv'], useTAndP=options.useTAndP, outputDir =outputDir, namePrefix='_inv' )
        else :
            template_hist = get_3d_mass_ratio_histograms( selection_nom, selection_inv, 'DYJetsToLLPhOlap', mass_binning, useHist=None, useAbsEta=True, useTAndP=useTAndP )

            results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, mcTemplate=template_hist['nom'], usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, outputDir =outputDir, namePrefix='_nom' )
            results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, mcTemplate=template_hist['inv'], usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, outputDir =outputDir, namePrefix='_inv' )
    else :
        results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, useLandauSig=useLandauSig, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, outputDir =outputDir, namePrefix='_nom' )
        results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, useLandauSig=useLandauSig, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, outputDir =outputDir, namePrefix='_inv' )

    write_output( results_nom, results_inv, outputDir )

def write_output( results_nom, results_inv, outputDir=None ) :

    sel_strs = []
    results_all = {}
    results_all['fake_ratio'] = {}
    results_all['fake_ratio_peak'] = {}
    results_all['fake_ratio_subtract'] = {}
    results_all['bins'] = {}
    results_all['pass_veto'] = results_nom
    results_all['fail_veto'] = results_inv

    for bin, res_nom in results_nom.iteritems() :

        res_inv = results_inv[bin]

        ptmin = bin[0]
        ptmax = bin[1]

        etamin = bin[2]
        etamax = bin[3]

        print ' pt %s - %s, eta %s - %s nom = %s, inv = %s, ratio = %s ' %( ptmin, ptmax, etamin, etamax, res_nom['nsig'], res_inv['nsig'], res_nom['nsig']/res_inv['nsig'] )

        sel_strs.append(' ( ph_pt[0] > %s && ph_pt[0] < %s && fabs(ph_eta) > %s && fabs(ph_eta) < %s ) * %f ' %( ptmin, ptmax, etamin, etamax, (res_nom['nsig']/res_inv['nsig']).n ) )
        results_all['fake_ratio'][bin] = (res_nom['nsig']/res_inv['nsig'])

        results_all['fake_ratio_peak'][bin] = (res_nom['nsig']*res_nom['nsig_peak']/(res_inv['nsig']*res_inv['nsig_peak']))

        if 'extra_bkg' in res_nom :
            results_all['fake_ratio_subtract'][bin] = (res_nom['nsig']-res_nom['extra_bkg'])/(res_inv['nsig']-res_inv['extra_bkg'])


    print ' + '.join( sel_strs )


    if outputDir is not None :
        file_res = open( '%s/results.pickle' %outputDir , 'w' )
        pickle.dump( results_all, file_res )
        file_res.close()

    
        root_file = ROOT.TFile.Open( '%s/results.root' %outputDir, 'RECREATE' )
        # write a th2 as well
        ffhist = ROOT.TH2F('ff', '', 40, 0, 200, 250, 0, 2.5 )

        for bin, ff in results_all['fake_ratio'].iteritems() :
            ptmin  = int( bin[0] ) 
            ptmax  = int( bin[1] ) 
            etamin = float( bin[2] ) 
            etamax = float( bin[3] ) 

            SetHistContentBins( ffhist, ff, ptmin, ptmax, etamin, etamax )

        ffpeak = ROOT.TH2F('ffpeak', '', 40, 0, 200, 250, 0, 2.5 )

        for bin, ff in results_all['fake_ratio_peak'].iteritems() :
            ptmin  = int( bin[0] ) 
            ptmax  = int( bin[1] ) 
            etamin = float( bin[2] ) 
            etamax = float( bin[3] ) 

            SetHistContentBins( ffpeak, ff, ptmin, ptmax, etamin, etamax )

        ffsubtract = ROOT.TH2F('ffsubtract', '', 40, 0, 200, 250, 0, 2.5 )
        if 'fake_ratio_subtract' in results_all :

            for bin, ff in results_all['fake_ratio_subtract'].iteritems() :
                ptmin  = int( bin[0] ) 
                ptmax  = int( bin[1] ) 
                etamin = float( bin[2] ) 
                etamax = float( bin[3] ) 

                SetHistContentBins( ffsubtract, ff, ptmin, ptmax, etamin, etamax )

        ffhist.Write()
        ffpeak.Write()
        ffsubtract.Write()
        root_file.Close()


def DoElectronFakeSimpleClosure( outputDir=None) :

    #pt_bins = [15, 20, 25, 30, 40, 50, 60, 80, 100, 10000000 ] 
    pt_bins = [15, 20, 25, 30, 40, 50, 60, 80, 100, 200 ] 
    #pt_bins = [15, 200]
    eta_bins = [-2.5, -2.3, -2.1, -1.9, -1.7, -1.5, -1.3, -1.1, -0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]
    #bins_coarse = [80, 1000000 ] 
    mass_binning = (100, 0, 200)

    draw_cmds = get_default_draw_commands( )
    selection_2fake_taglead = draw_cmds['FF']# + ' && ph_trigMatch_el[0] == 1 && ph_pt[0]>30'
    selection_2fake_tagsubl = draw_cmds['FF']# + ' && ph_trigMatch_el[1] == 1 && ph_pt[1]>30 '
    selection_1fake_taglead = draw_cmds['FR']# + ' && ph_trigMatch_el[0] == 1 && ph_pt[0]>30 '
    selection_1fake_tagsubl = draw_cmds['RF']# + ' && ph_trigMatch_el[1] == 1 && ph_pt[1]>30 '
    selection_0fake         = draw_cmds['RR']

    #results_with_trig = get_mass_histograms(selection_2fake_taglead, selection_2fake_tagsubl, selection_1fake_tagsubl, selection_1fake_taglead, 'DYJetsToLL', mass_binning )

    #ffresults_trig = get_fake_factors_counts( results_with_trig, pt_bins, eta_bins, (92-5, 92+5), normalize=False)

    #ffhist_trig = bin_map_to_hist( ffresults_trig['pt'], 'ffhist_trig' )

    #ffhist_trig.SetMarkerColor(ROOT.kRed)
    #ffhist_trig.SetLineColor(ROOT.kRed)

    #ffhist_trig.Draw()
    #raw_input('continue')

    target_samp = sampMan.get_samples(name='DYJetsToLL')

    #hist_nom = clone_sample_and_draw( target_samp[0], 'm_lepph1', selection_0fake, mass_binning )

    selection_inv = ' el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_elMinDR[0]>0.2 && ph_passMedium[0] && ph_hasPixSeed[0]==1 '
    selection_nom = ' el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_elMinDR[0]>0.2 && ph_passMedium[0] && ph_hasPixSeed[0]==0 '

    #selection_inv_weight = ' + '.join( ['( ph_pt[0] > %s && ph_pt[0] < %s ) * ( %f ) '%( min, max, ff.n) for (min, max), ff in ffresults_trig['pt'].iteritems()] )
    #selection_inv = '( %f ) * ( %s )' %( ffresults_trig['norm_pt'].values()[0].n, selection_inv )

    hist_inv = clone_sample_and_draw( target_samp[0], 'm_lepph1', selection_inv, mass_binning )
    hist_nom = clone_sample_and_draw( target_samp[0], 'm_lepph1', selection_nom, mass_binning )

    hist_nom.SetLineColor(ROOT.kBlack )
    hist_nom.SetMarkerColor(ROOT.kBlack )
    hist_inv.SetLineColor(ROOT.kRed )
    hist_inv.SetMarkerColor(ROOT.kRed )

    hist_nom.Draw()
    hist_inv.Draw('same')
    raw_input('continue')

    #selection_2fake_tagsubl_weight = ' + '.join( ['( ph_pt[1] > %s && ph_pt[1] < %s ) * ( %f ) '%( min, max, ff.n) for (min, max), ff in ffresults_trig['pt'].iteritems()] )
    #selection_2fake_tagsubl = '( %s ) * ( %s ) ' %(selection_2fake_tagsubl_weight, selection_2fake_tagsubl)

    #selection_2fake_taglead_weight = ' + '.join( ['( ph_pt[0] > %s && ph_pt[0] < %s ) * ( %f ) '%( min, max, ff.n) for (min, max), ff in ffresults_trig['pt'].iteritems()] )
    #selection_2fake_taglead = '( %s ) * ( %s ) ' %(selection_2fake_taglead_weight, selection_2fake_taglead)

    #hist_fake_lead = clone_sample_and_draw( target_samp[0], 'm_lepph1', selection_2fake_taglead, mass_binning )
    #hist_fake_subl = clone_sample_and_draw( target_samp[0], 'm_lepph1', selection_2fake_tagsubl, mass_binning )

    #hist_fake_lead.Add(hist_fake_subl)
    #hist_actual         = clone_sample_and_draw( target_samp[0], 'm_lepph1', selection_1fake_taglead, mass_binning )
    #hist_actual_tagsubl = clone_sample_and_draw( target_samp[0], 'm_lepph1', selection_1fake_tagsubl, mass_binning )

    #hist_actual.Add( hist_actual_tagsubl )

    #hist_actual.SetLineColor(ROOT.kBlack)
    #hist_actual.SetMarkerColor(ROOT.kBlack)
    #hist_actual.Draw()

    #hist_fake_lead.SetLineColor(ROOT.kRed)
    #hist_fake_lead.SetMarkerColor(ROOT.kRed)
    #hist_fake_lead.Draw('same')
    #raw_input('continue')

def DoElectronFakeRatioClosure( outputDir=None) :

    subdir = 'ElectronFakeClosure'

    #pt_bins = [15, 20, 25, 30, 40, 50, 60, 80, 100, 10000000 ] 
    pt_bins = [15, 20, 25, 30, 40, 50, 60, 80, 100, 200 ] 
    #pt_bins = [15, 200]
    #eta_bins = [-2.5, -2.3, -2.1, -1.9, -1.7, -1.5, -1.3, -1.1, -0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]
    eta_bins = [-2.5, -2.4, -2.3, -2.2, -2.1, -2.0,  -1.9, -1.8, -1.7, -1.5, -1.3, -1.1, -0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
    #bins_coarse = [80, 1000000 ] 
    mass_binning = (100, 0, 200)

    target_samp = sampMan.get_samples(name='ZjetsZgamma')

    selection_inv = ' el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && m_lepph1 > 86 && m_lepph1 < 106'
    selection_nom = ' el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && m_lepph1 > 86 && m_lepph1 < 106'
    
    hist_inv_pt = clone_sample_and_draw( target_samp[0], 'ph_pt[0]', selection_inv, pt_bins )
    hist_nom_pt = clone_sample_and_draw( target_samp[0], 'ph_pt[0]', selection_nom, pt_bins )

    hist_nom_pt.Divide(hist_inv_pt)

    hist_inv_eta = clone_sample_and_draw( target_samp[0], 'ph_eta[0]', selection_inv, eta_bins )
    hist_nom_eta = clone_sample_and_draw( target_samp[0], 'ph_eta[0]', selection_nom, eta_bins )

    hist_nom_eta.Divide(hist_inv_eta)


    fake_factors = {}
    for idx, min in enumerate(pt_bins[:-1] ) :
        max = pt_bins[idx+1]

        fake_factors[(min, max)] = hist_nom_pt.GetBinContent( idx+1 )

    print fake_factors

    selection_weight_lead = ' + '.join( ['( ph_pt[0] > %s && ph_pt[0] < %s ) * ( %f ) '%( min, max,ff) for (min, max), ff in fake_factors.iteritems()] )
    selection_weight_subl = ' + '.join( ['( ph_pt[1] > %s && ph_pt[1] < %s ) * ( %f ) '%( min, max,ff) for (min, max), ff in fake_factors.iteritems()] )

    #rej_cuts = '&& !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) ' 
    rej_cuts = '' 
    selection_egg =      ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && ph_passMedium[1] && ph_hasPixSeed[1]==0 && ph_phDR>0.3 %s'  %rej_cuts
    #selection_inv_lead = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && ph_passMedium[1] && ph_hasPixSeed[1]==0 && ph_phDR>0.3 && ph_truthMatch_ph[1] && ph_truthMatch_el[0]' 
    #selection_inv_subl = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && ph_passMedium[1] && ph_hasPixSeed[1]==1 && ph_phDR>0.3 && ph_truthMatch_ph[0] && ph_truthMatch_el[1]' 
    selection_inv_lead = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && ph_passMedium[1] && ph_hasPixSeed[1]==0 && ph_phDR>0.3 %s'  %rej_cuts
    selection_inv_subl = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && ph_passMedium[1] && ph_hasPixSeed[1]==1 && ph_phDR>0.3 %s'  %rej_cuts

    selection_inv_lead = '( %s ) * ( %s )' %( selection_weight_lead, selection_inv_lead )
    selection_inv_subl = '( %s ) * ( %s )' %( selection_weight_subl, selection_inv_subl )

    mass_binning = ( 50, 0, 200 )
    for var in ['m_lepph1', 'm_lepph2', 'm_lepphph'] :
        hist_egg = clone_sample_and_draw( target_samp[0], var, selection_egg, mass_binning)
        hist_inv_lead = clone_sample_and_draw( target_samp[0], var, selection_inv_lead, mass_binning)
        hist_inv_subl = clone_sample_and_draw( target_samp[0], var, selection_inv_subl, mass_binning)

        hist_egg.SetMarkerColor(ROOT.kBlack)
        hist_inv_lead.SetMarkerColor(ROOT.kRed)
        hist_inv_subl.SetMarkerColor(ROOT.kBlue)
        hist_inv_lead.SetMarkerStyle(20)
        hist_inv_subl.SetMarkerStyle(20)

        hist_egg.SetLineColor(ROOT.kBlack)
        hist_inv_lead.SetLineColor(ROOT.kRed)
        hist_inv_subl.SetLineColor(ROOT.kBlue)

        hist_inv_lead.Add(hist_inv_subl)

        can = ROOT.TCanvas( 'can', '')
        hist_egg.Draw()
        
        hist_inv_lead.Draw('same')
        #hist_inv_subl.Draw('same')

        if outputDir is not None :
            can.SaveAs( '%s/%s/closure_%s.pdf' %( outputDir, subdir, var ) )
        else :
            raw_input('continue')



def get_mass_histograms( selection_2fake_taglead, selection_2fake_tagsubl, selection_1fake_tagsubl, selection_1fake_taglead, sample,  mass_binning ) :

    results = {}
    results['pt'] = {}
    results['eta'] = {}

    target_samp = sampMan.get_samples(name=sample)

    # pt hists
    ee_pt_lead = clone_sample_and_draw( target_samp[0], 'm_phph:ph_pt[0]', selection_2fake_tagsubl, (40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]) )
    ee_pt_subl = clone_sample_and_draw( target_samp[0], 'm_phph:ph_pt[1]', selection_2fake_taglead, (40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]) )

    eg_pt_lead = clone_sample_and_draw( target_samp[0], 'm_phph:ph_pt[0]', selection_1fake_tagsubl, (40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]))
    eg_pt_subl = clone_sample_and_draw( target_samp[0], 'm_phph:ph_pt[1]', selection_1fake_taglead, (40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]))

    eg_pt_lead.Add(eg_pt_subl)
    ee_pt_lead.Add(ee_pt_subl)

    results['pt']['ee'] = ee_pt_lead
    results['pt']['eg'] = eg_pt_lead

    # eta hists
    ee_eta_lead = clone_sample_and_draw( target_samp[0], 'm_phph:ph_eta[0]', selection_2fake_tagsubl, (500, -2.5, 2.5, mass_binning[0], mass_binning[1], mass_binning[2]) )
    ee_eta_subl = clone_sample_and_draw( target_samp[0], 'm_phph:ph_eta[1]', selection_2fake_taglead, (500, -2.5, 2.5, mass_binning[0], mass_binning[1], mass_binning[2]) )

    eg_eta_lead = clone_sample_and_draw( target_samp[0], 'm_phph:ph_eta[0]', selection_1fake_tagsubl, (500, -2.5, 2.5, mass_binning[0], mass_binning[1], mass_binning[2]))
    eg_eta_subl = clone_sample_and_draw( target_samp[0], 'm_phph:ph_eta[1]', selection_1fake_taglead, (500, -2.5, 2.5, mass_binning[0], mass_binning[1], mass_binning[2]))

    eg_eta_lead.Add(eg_eta_subl)
    ee_eta_lead.Add(ee_eta_subl)

    results['eta']['ee'] = ee_eta_lead
    results['eta']['eg'] = eg_eta_lead

    return results
    
def get_3d_mass_ratio_histograms( selection_nom, selection_inv, sample,  mass_binning, useHist=None ,useAbsEta=False, useTAndP=False ) :

    results = {}

    if useHist is not None :
        fname = '%s.root' %useHist
        if os.path.isfile( fname ) :
            ofile = ROOT.TFile.Open( fname, 'READ')
            results['nom'] = ofile.Get('nom').Clone( 'hist_nom')
            results['inv'] = ofile.Get('inv').Clone( 'hist_inv')
            sampMan.curr_decorations.append (results['nom'] )
            sampMan.curr_decorations.append (results['inv'] )
            # it gets pissed if you close the file
            sampMan.curr_decorations.append (ofile )

            return results

    target_samp = sampMan.get_samples(name=sample)

    if useAbsEta :
        if useTAndP :
            var_lead = 'm_tagprobe:probe_pt:fabs(probe_eta)'
        else :
            var_lead = 'm_lepph1:ph_pt[0]:fabs(ph_eta[0])' #z:y:x
        eta_nbin = 250
        eta_min = 0
        eta_max = 2.5
    else :
        if useTAndP :
            var_lead = 'm_tagprobe:probe_pt:probe_eta'
        else :
            var_lead = 'm_lepph1:ph_pt[0]:ph_eta[0]' #z:y:x
        eta_nbin = 500
        eta_min = -2.5
        eta_max = 2.5

    # pt hists
    hist_nom = clone_sample_and_draw( target_samp[0], var_lead, selection_nom, (eta_nbin, eta_min, eta_max, 40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]) )
    hist_inv = clone_sample_and_draw( target_samp[0], var_lead, selection_inv, (eta_nbin, eta_min, eta_max, 40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]) )

    results['nom'] = hist_nom
    results['inv'] = hist_inv

    # if we've gotten here, useHist was set but the file does
    # not exsit.  Create it and save it
    if useHist is not None :
        ofile = ROOT.TFile.Open( '%s.root' %useHist, 'RECREATE')
        hist_nom = results['nom'].Clone('nom')
        hist_inv = results['inv'].Clone('inv')
        hist_nom.SetName('nom')
        hist_inv.SetName('inv')
        hist_nom.Write()
        hist_inv.Write()
        ofile.Close()

    return results


def get_3d_mass_histograms( selection_2fake_taglead, selection_2fake_tagsubl, selection_1fake_tagsubl, selection_1fake_taglead, sample,  mass_binning, useHist=None ,useAbsEta=False ) :

    results = {}

    if useHist is not None :
        fname = '%s.root' %useHist
        if os.path.isfile( fname ) :
            ofile = ROOT.TFile.Open( fname, 'READ')
            results['ee'] = ofile.Get('ee').Clone( 'hist_ee')
            results['eg'] = ofile.Get('eg').Clone( 'hist_eg')
            sampMan.curr_decorations.append (results['ee'] )
            sampMan.curr_decorations.append (results['eg'] )
            sampMan.curr_decorations.append (ofile )

            return results

    target_samp = sampMan.get_samples(name=sample)

    if useAbsEta :
        var_lead = 'm_phph:ph_pt[0]:fabs(ph_eta[0])' #z:y:x
        var_subl = 'm_phph:ph_pt[1]:fabs(ph_eta[1])' #z:y:x
        eta_nbin = 250
        eta_min = 0
        eta_max = 2.5
    else :
        var_lead = 'm_phph:ph_pt[0]:ph_eta[0]' #z:y:x
        var_subl = 'm_phph:ph_pt[1]:ph_eta[1]' #z:y:x
        eta_nbin = 500
        eta_min = -2.5
        eta_max = 2.5

    # pt hists
    ee_lead = clone_sample_and_draw( target_samp[0], var_lead, selection_2fake_tagsubl, (eta_nbin, eta_min, eta_max, 40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]) )
    ee_subl = clone_sample_and_draw( target_samp[0], var_subl, selection_2fake_taglead, (eta_nbin, eta_min, eta_max, 40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]) )

    eg_lead = clone_sample_and_draw( target_samp[0], var_lead, selection_1fake_tagsubl, (eta_nbin, eta_min, eta_max, 40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]))
    eg_subl = clone_sample_and_draw( target_samp[0], var_subl, selection_1fake_taglead, (eta_nbin, eta_min, eta_max, 40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]))

    eg_lead.Add(eg_subl)
    ee_lead.Add(ee_subl)

    results['ee'] = ee_lead
    results['eg'] = eg_lead

    # if we've gotten here, useHist was set but the file does
    # not exsit.  Create it and save it
    if useHist is not None :
        ofile = ROOT.TFile.Open( '%s.root' %useHist, 'RECREATE')
        hist_ee = results['ee'].Clone('ee')
        hist_eg = results['eg'].Clone('eg')
        hist_ee.SetName('ee')
        hist_eg.SetName('eg')
        hist_ee.Write()
        hist_eg.Write()
        ofile.Close()

    return results
    
def get_fake_factors_counts( hists, pt_bins, eta_bins, mass_cuts, normalize=True ) :

    fake_factors = {}
    fake_factors['norm_pt'] = {}
    fake_factors['norm_eta'] = {}
    fake_factors['pt'] = {}
    fake_factors['eta'] = {}

    mass_bin_min = hists['pt']['ee'].GetYaxis().FindBin( mass_cuts[0] )
    mass_bin_max = hists['pt']['ee'].GetYaxis().FindBin( mass_cuts[1] )

    pt_bin_first = hists['pt']['ee'].GetXaxis().FindBin( pt_bins[0] )
    pt_bin_last  = hists['pt']['ee'].GetXaxis().FindBin( pt_bins[-1] ) 

    eta_bin_first = hists['eta']['ee'].GetXaxis().FindBin( eta_bins[0] )
    eta_bin_last  = hists['eta']['ee'].GetXaxis().FindBin( eta_bins[-1] ) 
    
    err_ee_pt_tot = ROOT.Double()
    err_eg_pt_tot = ROOT.Double()
    int_ee_pt_tot = hists['pt']['ee'].IntegralAndError( pt_bin_first, pt_bin_last, mass_bin_min, mass_bin_max, err_ee_pt_tot)
    int_eg_pt_tot = hists['pt']['eg'].IntegralAndError( pt_bin_first, pt_bin_last, mass_bin_min, mass_bin_max, err_eg_pt_tot)

    err_ee_eta_tot = ROOT.Double()
    err_eg_eta_tot = ROOT.Double()
    int_ee_eta_tot = hists['eta']['ee'].IntegralAndError( eta_bin_first, eta_bin_last, mass_bin_min, mass_bin_max, err_ee_eta_tot)
    int_eg_eta_tot = hists['eta']['eg'].IntegralAndError( eta_bin_first, eta_bin_last, mass_bin_min, mass_bin_max, err_eg_eta_tot)

    val_ee_pt_tot = ufloat( int_ee_pt_tot, err_ee_pt_tot)
    val_eg_pt_tot = ufloat( int_eg_pt_tot, err_eg_pt_tot)

    val_ee_eta_tot = ufloat( int_ee_eta_tot, err_ee_eta_tot)
    val_eg_eta_tot = ufloat( int_eg_eta_tot, err_eg_eta_tot)

    fake_factors['norm_pt'][(pt_bins[0], pt_bins[-1])] = val_eg_pt_tot/( val_eg_pt_tot + val_ee_pt_tot )
    fake_factors['norm_eta'][(eta_bins[0], eta_bins[-1])] = val_eg_eta_tot/( val_eg_eta_tot + val_ee_eta_tot )

    for idx, min in enumerate(pt_bins[:-1]) :
        max = pt_bins[idx+1]

        pt_bin_min = hists['pt']['ee'].GetXaxis().FindBin( min )
        pt_bin_max = hists['pt']['ee'].GetXaxis().FindBin( max ) 

        pt_bin_max -=1

        err_ee = ROOT.Double()
        err_eg = ROOT.Double()
        int_ee = hists['pt']['ee'].IntegralAndError( pt_bin_min, pt_bin_max, mass_bin_min, mass_bin_max, err_ee )
        int_eg = hists['pt']['eg'].IntegralAndError( pt_bin_min, pt_bin_max, mass_bin_min, mass_bin_max, err_eg )


        # convert to val+-err
        val_ee = ufloat( int_ee, err_ee )
        val_eg = ufloat( int_eg, err_eg )

        if normalize :
            # normalize values if requested
            val_num = val_eg/int_eg_pt_tot
            val_den = (val_ee + val_eg)/( int_eg_pt_tot+int_ee_pt_tot)

            fake_factor = val_num/val_den
        else :

            fake_factor = val_eg/( val_ee + val_eg )

        fake_factors['pt'][(min, max)] = fake_factor

        print 'Pt min, max = %d, %d -- bins = %d, %d -- FF = %s' %( min, max, pt_bin_min, pt_bin_max, fake_factor)

    for idx, min in enumerate(eta_bins[:-1]) :
        max = eta_bins[idx+1]

        eta_bin_min = hists['eta']['ee'].GetXaxis().FindBin( min )
        eta_bin_max = hists['eta']['ee'].GetXaxis().FindBin( max ) 

        eta_bin_max -=1

        err_ee = ROOT.Double()
        err_eg = ROOT.Double()
        int_ee = hists['eta']['ee'].IntegralAndError( eta_bin_min, eta_bin_max, mass_bin_min, mass_bin_max, err_ee )
        int_eg = hists['eta']['eg'].IntegralAndError( eta_bin_min, eta_bin_max, mass_bin_min, mass_bin_max, err_eg )


        # convert to val+-err
        val_ee = ufloat( int_ee, err_ee )
        val_eg = ufloat( int_eg, err_eg )

        normalize=True
        if normalize :
            # normalize values if requested
            val_num = val_eg/int_eg_eta_tot
            val_den = (val_ee + val_eg)/( int_eg_eta_tot+int_ee_eta_tot)

            fake_factor = val_num/val_den
        else :

            fake_factor = val_eg/( val_ee + val_eg )

        fake_factors['eta'][(min, max)] = fake_factor

        print 'Eta min, max = %f, %f -- bins = %d, %d -- FF = %s' %( min, max, eta_bin_min, eta_bin_max, fake_factor)

    return fake_factors

def get_fake_factors_fit( hists, pt_bins, eta_bins) :

    fake_factors = {}
    fake_factors['norm_pt'] = {}
    fake_factors['norm_eta'] = {}
    fake_factors['pt'] = {}
    fake_factors['eta'] = {}

    hist_ee_pt_tot = hists['pt']['ee'].ProjectionY('hist_ee_pt_tot')
    hist_eg_pt_tot = hists['pt']['eg'].ProjectionY('hist_eg_pt_tot')

    for idx, min in enumerate(eta_bins[:-1]) :
        max = eta_bins[idx+1]

        eta_bin_min = hists['eta']['ee'].GetXaxis().FindBin( min )
        eta_bin_max = hists['eta']['ee'].GetXaxis().FindBin( max ) 

        hist_ee_pt = hists['eta']['ee'].ProjectionY('hist_ee_eta_%f_%f' %(min, max), eta_bin_min, eta_bin_max )
        hist_eg_pt = hists['eta']['eg'].ProjectionY('hist_eg_eta_%f_%f' %(min, max), eta_bin_min, eta_bin_max )

        fit_hist_nominal( hist_ee_pt )

    for idx, min in enumerate(pt_bins[:-1]) :
        max = pt_bins[idx+1]

        pt_bin_min = hists['pt']['ee'].GetXaxis().FindBin( min )
        pt_bin_max = hists['pt']['ee'].GetXaxis().FindBin( max ) 

        hist_ee_pt = hists['pt']['ee'].ProjectionY('hist_ee_pt_%d_%d' %(min, max), pt_bin_min, pt_bin_max )
        hist_eg_pt = hists['pt']['eg'].ProjectionY('hist_eg_pt_%d_%d' %(min, max), pt_bin_min, pt_bin_max )

        fit_hist_nominal( hist_ee_pt )


def fit_pt_eta_bins( hist, pt_eta_bins, mcTemplate=None, useLandauSig=False, ndKeysSample=None, ndKeysSelection=None, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCmsShapeBkg=False, extraBkgHist=None, useTAndP=False, outputDir=None, namePrefix='' ) :

    results_pt_eta = {}
    last_pt = max( [x[1] for x in pt_eta_bins.keys() ] )
    for (ptmin, ptmax), eta_bins in pt_eta_bins.iteritems()  :

        if options.ptmin > 0 and options.ptmin != ptmin :
            continue

        # If FindBin is given a value on the boundary it returns
        # the bin above the boundary
        # Therefore the max bin is 1 less than what is returned
        pt_bin_min = hist.GetYaxis().FindBin( ptmin )
        pt_bin_max = hist.GetYaxis().FindBin( ptmax ) - 1 

        for etaidx, (etamin, etamax) in enumerate( eta_bins ) :

            if options.etabinmin >= 0 and options.etabinmin != etaidx :
                continue

            eta_bin_min = hist.GetXaxis().FindBin( etamin )
            eta_bin_max = hist.GetXaxis().FindBin( etamax ) - 1

            print 'ptmin = %d, ptmax = %d, etamin = %f, etamax = %f ' %(ptmin, ptmax, etamin, etamax )
            print 'BIN : ptmin = %d, ptmax = %d, etamin = %d, etamax = %d ' %(pt_bin_min, pt_bin_max, eta_bin_min, eta_bin_max )

            if ptmax == last_pt :
                fitname = 'fit%s_eta_%.2f-%.2f_pt_%d-max' %(namePrefix, etamin, etamax, ptmin)
            else :
                fitname = 'fit%s_eta_%.2f-%.2f_pt_%d-%d' %(namePrefix, etamin, etamax, ptmin, ptmax)

            hist_proj = hist.ProjectionZ(fitname, eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )

            if ptmax == last_pt:
                hist_proj.Rebin(2)

            output_name = None
            if outputDir is not None :
                output_name = outputDir + '/' + hist_proj.GetName()

            if mcTemplate is not None :
                template_proj = mcTemplate.ProjectionZ(fitname+'_fit', eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )
                results = fit_hist_mc_template( hist_proj, template_proj, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, label=hist_proj.GetName(), outputName=output_name )

            elif ndKeysSample is not None :

                if useTAndP :
                    pt_eta_selection = ndKeysSelection + ' && fabs(probe_eta) > %f && fabs(probe_eta) < %f && probe_pt > %d && probe_pt < %d ' %( etamin, etamax, ptmin, ptmax )
                else :
                    pt_eta_selection = ndKeysSelection + ' && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f && ph_pt[0] > %d && ph_pt[0] < %d ' %( etamin, etamax, ptmin, ptmax )

                orig_tree = sampMan.get_samples( name=ndKeysSample )[0].chain
                orig_tree.SetBranchStatus('*', 1)
                tmpfile = ROOT.TFile.Open( '/tmp/jkunkle/tmp.root', 'RECREATE' )
                new_tree = orig_tree.CopyTree( pt_eta_selection )


                if useTAndP :
                    m_tagprobe       = ROOT.RooRealVar( 'm_tagprobe', 'm_tagprobe', 40, 200 )
                    probe_pt         = ROOT.RooRealVar( 'probe_pt', 'probe_pt', 0, 1000 )
                    probe_eta        = ROOT.RooRealVar( 'probe_eta', 'probe_eta', -5, 5)
                    probe_hasPixSeed = ROOT.RooRealVar( 'probe_hasPixSeed', 'probe_hasPixSeed', 0, 1)
                    probe_eleVeto    = ROOT.RooRealVar( 'probe_eleVeto', 'probe_eleVeto', 0, 1)
                    probe_isPhoton   = ROOT.RooRealVar( 'probe_isPhoton', 'probe_isPhoton', 0, 1)

                    data_set = ROOT.RooDataSet( 'dataset_%.2f_%.2f_%d_%d' %(etamin, etamax, ptmin, ptmax ), '', new_tree,ROOT.RooArgSet( m_tagprobe ))

                    results = fit_hist_ndkeys( hist_proj, signal_dataset=data_set, varname='m_tagprobe', bkg_dataset=None, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, label=hist_proj.GetName(), outputName=output_name )
                else :

                    m_lepph1         = ROOT.RooRealVar( 'm_lepph1', 'm_lepph1', 40, 200 )
                    ph_passMedium    = ROOT.RooRealVar( 'ph_passMedium[0]', 'ph_passMedium[0]', 0, 1 )
                    el_passtrig_n    = ROOT.RooRealVar( 'el_passtrig_n', 'el_passtrig_n', 0, 10 )
                    el_n             = ROOT.RooRealVar( 'el_n', 'el_n', 0, 10 )
                    ph_n             = ROOT.RooRealVar( 'ph_n', 'ph_n', 0, 10 )
                    ph_hasPixSeed    = ROOT.RooRealVar( 'ph_hasPixSeed[0]', 'ph_hasPixSeed[0]', 0, 10 )
                    ph_eta           = ROOT.RooRealVar( 'ph_eta[0]', 'ph_eta[0]', -5., 5. )
                    ph_pt            = ROOT.RooRealVar( 'ph_pt[0]', 'ph_pt[0]', 0, 1000. )
                    ph_truthMatch_ph = ROOT.RooRealVar( 'ph_truthMatch_ph[0]', 'ph_truthMatch_ph[0]', 0, 1. )

                    data_set = ROOT.RooDataSet( 'dataset_%.2f_%.2f_%d_%d' %(etamin, etamax, ptmin, ptmax ), '', new_tree,ROOT.RooArgSet( m_lepph1))

                    results = fit_hist_ndkeys( hist_proj, signal_dataset=data_set, varname='m_lepph1', bkg_dataset=None, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, label=hist_proj.GetName(), outputName=output_name )
                tmpfile.Close()
            else :
                results = fit_hist_nominal( hist_proj, useLandauSig=useLandauSig, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, label=hist_proj.GetName(), outputName=output_name )

            if extraBkgHist is not None :
                histname = 'bkg%s_eta_%.2f-%.2f_pt_%d-%d' %(namePrefix, etamin, etamax, ptmin, ptmax) 
                bkg_hist_proj = extraBkgHist.ProjectionZ(histname, eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )
                results['extra_bkg'] = bkg_hist_proj.Integral()

            results_pt_eta[(str(ptmin), str(ptmax), '%.2f'%etamin, '%.2f'%etamax)] = results

    return results_pt_eta


def get_fake_factors_3d_fit( hists, pt_bins, eta_bins, outputDir=None) :

    fake_factors = {}
    fake_factors['norm_pt'] = {}
    fake_factors['norm_eta'] = {}
    fake_factors['pt'] = {}
    fake_factors['eta'] = {}

    for ptidx, ptmin in enumerate( pt_bins[:-1] )  :
        ptmax = pt_bins[ptidx+1]

        pt_bin_min = hists['ee'].GetYaxis().FindBin( ptmin )
        pt_bin_max = hists['ee'].GetYaxis().FindBin( ptmax )
        for etaidx, etamin in enumerate( eta_bins[:-1] ) :
            etamax = eta_bins[etaidx+1]

            eta_bin_min = hists['ee'].GetXaxis().FindBin( etamin )
            eta_bin_max = hists['ee'].GetXaxis().FindBin( etamax )

            if ptmax == pt_bins[-1] :
                fitname_ee = 'fit_ee_eta_%.2f-%.2f_pt_%d-max' %(etamin, etamax, ptmin)
                fitname_eg = 'fit_eg_eta_%.2f-%.2f_pt_%d-max' %(etamin, etamax, ptmin)
            else :
                fitname_ee = 'fit_ee_eta_%.2f-%.2f_pt_%d-%d' %(etamin, etamax, ptmin, ptmax)
                fitname_eg = 'fit_eg_eta_%.2f-%.2f_pt_%d-%d' %(etamin, etamax, ptmin, ptmax)

            hist_ee = hists['ee'].ProjectionZ(fitname_ee, eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )
            hist_eg = hists['eg'].ProjectionZ(fitname_eg, eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )

            output_name_eg = None
            output_name_ee = None
            if outputDir is not None :
                output_name_eg = outputDir + '/' + hist_eg.GetName()
                output_name_ee = outputDir + '/' + hist_ee.GetName()

            fit_hist_nominal( hist_ee, hist_ee.GetName(), output_name_ee )
            fit_hist_nominal( hist_eg, hist_eg.GetName(), output_name_eg )

def fit_hist_nominal( data_hist, useLandauSig=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, label=None, outputName=None ) :

    sampMan.fit_objs = {}

    if label is None :
        label = data_hist.GetName()

    # independent var
    xmin = 40
    xmax = 200

    m_lepph1 = ROOT.RooRealVar( 'm_lepph1', 'm_lepph1', xmin, xmax )

    signal = []
    if useLandauSig :
        signal.append('landau')
    else :
        signal.append( 'bwxcb' )

    background = []
    if usePolyBkg :
        background.append( 'poly' )
    elif useExpBkg :
        background.append( 'exp' )
    elif useChebyBkg :
        background.append( 'cheby' )
    elif useBernsteinBkg:
        background.append( 'bernstein' )
    else :
        background.append('cmsshape')

    fit_defs = get_fit_defaults( data_hist.GetName(), useGaussSig=None, useLandauSig=useLandauSig, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg )
    chi2 = fit_model_to_data(m_lepph1, data_hist, fit_defs, sampMan, signal=signal, background=background, bkg_labels=['Bkg'])

    draw_fitted_results( sampMan.fit_objs['model'], sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], 'Bkg', m_lepph1, chi2, label, outputName=outputName )

    return store_results( m_lepph1, 'Bkg' )

def fit_hist_mc_template( data_hist, template_hist, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, label=None, outputName=None ) :

    sampMan.fit_objs = {}

    if label is None :
        label = data_hist.GetName()

    xmin = 40
    xmax = 200

    # independent var
    m_lepph1 = ROOT.RooRealVar( 'm_lepph1', 'm_lepph1', xmin,xmax)

    fit_defs = get_fit_defaults( data_hist.GetName(), useGaussSig=(template_dataset is not None), useLandauSig=False, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg )
    chi2 = fit_model_to_data(m_lepph1, data_hist, fit_defs, sampMan, MCSig=template_hist, doNDKeys=False, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg)

    draw_fitted_results( sampMan.fit_objs['model'], sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], sampMan.fit_objs['bkg_model'], m_lepph1, chi2, label, outputName=outputName )

    return store_results( m_lepph1 )

def fit_hist_ndkeys( data_hist, signal_dataset=None, bkg_dataset=None, varname='m_lepph1', usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCmsShapeBkg=False, label=None, outputName=None ) :

    sampMan.fit_objs = {}

    if label is None :
        label = data_hist.GetName()

    xmin = 40
    xmax = 200

    # independent var
    m_lepph1 = ROOT.RooRealVar( varname, varname, xmin,xmax)

    signals = [signal_dataset]
    if bkg_dataset is not None :
        backgrounds = [bkg_dataset]
    else :
        backgrounds= []

    if usePolyBkg :
        backgrounds.append( 'poly' )
    if useExpBkg :
        backgrounds.append( 'exp' )
    if useChebyBkg :
        backgrounds.append( 'cheby' )
    if useBernsteinBkg :
        backgrounds.append( 'bernstein' )
    if useCmsShapeBkg:
        backgrounds.append( 'cmsshape' )

    bkg_labels = ['Bkg']

    fit_defs = get_fit_defaults( data_hist.GetName(), useGaussSig=(signal_dataset is not None), useLandauSig=False, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg )
    #chi2 = fit_model_to_data( m_lepph1, data_hist, fit_defs, sampMan, MCSig=template_dataset, doNDKeys=True, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg)
    chi2 = fit_model_to_data( m_lepph1, data_hist, fit_defs, sampMan, signal=signals, background=backgrounds, bkg_labels=bkg_labels)

    print sampMan.fit_objs.keys()

    draw_fitted_results( sampMan.fit_objs['model'], sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], bkg_labels, m_lepph1, chi2, label, outputName=outputName )

    return store_results( m_lepph1, backgrounds=bkg_labels )

def store_results( var, backgrounds=['bkg_model'] ) :

    if not isinstance( backgrounds, list) :
        backgrounds = [backgrounds]

    results = {}

    xmin = var.getMin()
    xmax = var.getMax()

    print xmin
    print xmax

    hist_sig = sampMan.fit_objs['sig_model'].createHistogram('hist_sig_model', var, ROOT.RooFit.Binning( int((xmax-xmin)*10), xmin, xmax ) )
    hist_bkg = sampMan.fit_objs[backgrounds[0]].createHistogram('hist_bkg_model', var, ROOT.RooFit.Binning( int((xmax-xmin)*10), xmin, xmax ) )

    int_min = 91.2-10
    int_max = 91.2+10

    int_min_tight = 91.2-5
    int_max_tight = 91.2+5

    bin_min = hist_sig.FindBin( int_min )
    bin_max = hist_sig.FindBin( int_max )
    
    bin_min_tight = hist_sig.FindBin( int_min_tight )
    bin_max_tight = hist_sig.FindBin( int_max_tight )

    int_sig_err = ROOT.Double()
    int_bkg_err = ROOT.Double()
    int_sig = hist_sig.IntegralAndError( bin_min, bin_max, int_sig_err )
    int_bkg = hist_bkg.IntegralAndError( bin_min, bin_max, int_bkg_err )

    int_sig_err_tight = ROOT.Double()
    int_bkg_err_tight = ROOT.Double()
    int_sig_tight = hist_sig.IntegralAndError( bin_min_tight, bin_max_tight, int_sig_err_tight )
    int_bkg_tight = hist_bkg.IntegralAndError( bin_min_tight, bin_max_tight, int_bkg_err_tight )

    for name, obj in sampMan.fit_objs.iteritems() :
        if isinstance( obj, ROOT.RooRealVar ) :
            results[name] = ufloat( obj.getVal(), obj.getError() )

    results['nsig_peak'] = ufloat( int_sig, int_sig_err )
    results['nbkg_peak'] = ufloat( int_bkg, int_bkg_err )
    results['nsig_peak_tight'] = ufloat( int_sig_tight, int_sig_err_tight )
    results['nbkg_peak_tight'] = ufloat( int_bkg_tight, int_bkg_err_tight )

    return results


def clone_sample_and_draw( samp, var, sel, binning ) :
    global sampMan
    newSamp = sampMan.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist
                                       
def generate_latex_table( entries ) :

    max_len = 0
    for val in entries.values() :
        if len(val) > max_len :
            max_len = len(val)

    latex_text = r'\begin{tabular} {| l | ' + ' | '.join( ['c']*max_len ) + ' | } \n'

    first = True
    for key, val in entries.iteritems() :

        txtval = []
        for v in val :
            if isinstance(v, data_pair) :
                txtval.append(v.Print())
            else :
                txtval.append(v)

        print txtval


        latex_text += key + ' & ' + ' & '.join( txtval ) + r' \\ '
        if first :
            latex_text += r' \hline  '
            first = False

        latex_text += '\n'

    latex_text += r'\end{tabular}' + ' \n'


    return latex_text

def bin_map_to_hist( map, name ) :

    #first get the binning
    binning = []
    for min, max in map.keys() :
        binning.append(min)

    binning.sort()
    print binning

    for min, max in map.keys() :
        if max > binning[-1]  :
            binning.append(max)

    print binning 

    hist = ROOT.TH1F( name, name, len(binning)-1, array('f', binning) )

    for idx, min in enumerate(binning[:-1]) :
        max = binning[idx+1]

        val = map[(min, max)]

        hist.SetBinContent( idx+1, val.n )
        hist.SetBinError( idx+1, val.s )

    global_hists[name]=hist

    return hist



    

main() 
