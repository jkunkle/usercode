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

ROOT.gROOT.ProcessLine( '.L /afs/cern.ch/user/v/volper/public/EtoGammaFR/forYurii/etogammaFR_eg/RooCMSShape.cc+' )

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

def get_ratio_draw_commands( isConv=None ) :

    if isConv==False :

        return { 
                 'nom'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && !ph_isConv[0]',
                 'inv'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && !ph_isConv[0]',
               }
    elif isConv==True :

        return { 
                 'nom'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && ph_isConv[0]',
                 'inv'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && ph_isConv[0]',
               }
    else :

        return { 
                 'nom'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==0 ',
                 'inv'  :'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==1 ',
               }


def get_fit_defaults( histname, useGaussSig=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False ) :

    defaults = {}

    bkg='cmsshape'

    sig='bw'
    if useGaussSig :
        sig='Gauss'

    if usePolyBkg :
        bkg = 'poly'
    if useExpBkg :
        bkg = 'exp'
    if useChebyBkg:
        bkg = 'cheby'
    if useBernsteinBkg:
        bkg = 'bernstein'

    defaults['bw_cmsshape'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 40, 'fit_max' : 160 }
    defaults['Gauss_cmsshape'] = { 'mean' : 0, 'sigma' : 2.495, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 40, 'fit_max' : 180 }

    #defaults['bw_poly'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'poly_linear' : -0.008, 'poly_quadratic' : -0.00002, 'poly_cubic' : 0.0000002,  'poly_quartic' : 0.001, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 160 }
    defaults['bw_poly'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'poly_linear' : 10, 'poly_quadratic' : -0.05, 'poly_cubic' : -0.00001,  'poly_quartic' : 0.0000001, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 160 }
    defaults['Gauss_poly'] = { 'mean' : 0, 'sigma' : 2.495, 'poly_linear' : 1, 'poly_quadratic' : 4, 'poly_cubic' : 3, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 160  }

    defaults['bw_exp'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'exp_width' : 0.05, 'exp_start' : 80, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
    defaults['Gauss_exp'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : 0.05, 'exp_start' : 80, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }

    defaults['bw_cheby'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'a0' : -0.05, 'a1' : -0.05, 'a2' : 0.5, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
    defaults['Gauss_cheby'] = { 'mean' : 0, 'sigma' : 2.495, 'a0' : 0.01, 'a1' : -0.1, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }

    defaults['bw_bernstein'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'b0' : 1, 'b1' : 1, 'b2' : 2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
    defaults['Gauss_bernstein'] = { 'mean' : 0, 'sigma' : 2.495, 'b0' : 1, 'b1' : 1, 'b2' : 1, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }

    alts = {'bw_cmsshape' : {}, 'Gauss_cmsshape' : {}, 'bw_poly' : {}, 'Gauss_poly' : {}, 'bw_exp' : {}, 'Gauss_exp' : {}, 'bw_cheby' : {} , 'Gauss_cheby' : { }, 'bw_bernstein' : {}, 'Gauss_bernstein' : {} }

    alts['bw_cmsshape']['fit_nom_eta_2.10-2.40_pt_80-max'] = { 'Bias' : 1.76, 'Width' : 1.7 , 'Cut' : -0.57, 'Power' : 8, 'cms_alpha' : 200, 'cms_beta' : 0.006, 'cms_gamma' : 0.0002, 'cms_peak' : 88.7, 'nsig' : 80, 'nbkg' : 400, 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_0.10-1.48_pt_80-max'] = { 'Bias' : 1.45, 'Width' : 2.9 , 'Cut' : -2.5, 'Power' : 20, 'cms_alpha' : 200, 'cms_beta' : 0.02, 'cms_gamma' : 0.06, 'cms_peak' : 88, 'nsig' : 400, 'nbkg' : 200, 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_1.00-1.48_pt_80-max'] = { 'Bias' : 1.45, 'Width' : 2.9 , 'Cut' : -2.5, 'Power' : 20, 'cms_alpha' : 200, 'cms_beta' : 0.02, 'cms_gamma' : 0.06, 'cms_peak' : 88, 'nsig' : 400, 'nbkg' : 200, 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_2.40-2.50_pt_25-40'] = { 'Bias' : 0.38, 'Width' : 3.4 , 'Cut' : -3.7, 'Power' : 30, 'cms_alpha' : 100, 'cms_beta' : 0.1, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_nom_eta_0.00-0.10_pt_80-max'] = { 'Bias' : -0.8, 'Width' : 1 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 100, 'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 60, 'nbkg' : 130, 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_0.50-1.00_pt_80-max'] = { 'Bias' : -0.7, 'Width' : 2 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 180, 'cms_beta' : 0.02, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 130, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 160 }
    alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_80-max'] = { 'Bias' : -0.7, 'Width' : 2 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 180, 'cms_beta' : 0.02, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 40, 'nbkg' : 40, 'fit_min': 40, 'fit_max' : 160 }

    alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_15-25'] = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_25-40'] = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 'cms_beta' : 0.04, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.48_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 150, 'cms_beta' : 0.03, 'cms_gamma' : 0.12, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 80, 'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 50000, 'nbkg' : 1000, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_40-80']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 120, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.10-0.50_pt_40-80'] = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 100, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_40-80'] = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 180, 'cms_beta' : 0.02, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.48_pt_40-80'] = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 100, 'cms_beta' : 0.03, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 1000, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_40-80'] = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_40-80'] = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_40-80'] = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.30_pt_40-80'] = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.30_pt_40-80'] = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.30-2.40_pt_40-80'] = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.30-2.40_pt_40-80'] = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_40-80'] = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_40-80'] = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_0.10-0.50_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.10-0.50_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_0.50-1.00_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.48_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.48_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.10_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.40_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.40_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }
    alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_80-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 'fit_min': 40, 'fit_max' : 180 }


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
        
    #DoElectronFakeSimpleClosure( outputDir=options.outputDir )



    #CompTrigNoTrig( outputDir = options.outputDir )

    #DoElectronFakeFit( outputDir=options.outputDir,useHist='.EleFit3dAbsEtaWithEleVeto' )
    #DoElectronFakeFit( outputDir=options.outputDir )

    #DoElectronFakeRatioClosure(  outputDir=options.outputDir )

    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=False, doNDKeys=False, usePolyBkg=True, useExpBkg=False)
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=False, doNDKeys=False, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False)
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=True, doNDKeys=False, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False)
    #--------------------------
    # Use MC template for syst. studies
    #--------------------------
    #DoElectronFakeFitRatio( outputDir=options.outputDir, sample='Data', useHist='.EleFit3dRatioAbsEtaWithEleVetoConv', useMCTemplate=False, useCoarseEta=True )

    #DoElectronFakeFitRatio( outputDir=options.outputDir, sample='Data', isConv=True, useHist='.EleFit3dRatioAbsEtaWithEleVetoMCConv', useMCTemplate=True )

    ##--------------------------
    ## Use bw x cb with cms shape bkg
    ##--------------------------
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=False, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False)

    ##--------------------------
    ## Use MC template with cms shape bkg
    ##--------------------------
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=True, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False)

    #--------------------------
    # Use MC template with NDKeys smearing with cms shape bkg
    #--------------------------
    DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=True, doNDKeys=True, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False)

    ##--------------------------
    ## Use MC template with exponential bkg
    ##--------------------------
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=True, doNDKeys=True, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False)

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
    #eta_bins = [-2.5, -2.1, -1.57, -1.48, -0.1, 0.1, 1.48, 1.57, 2.1, 2.5]
    eta_bins = [0.0, 0.1, 1.48, 1.57, 2.1, 2.5]
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

def DoElectronFakeFitRatio( outputDir=None, sample='Data', isConv=None, useHist=None, useCoarseEta=False, useMCTemplate=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, doNDKeys=False) :

    subdir = 'ElectronFakeFitsRatio'
    if sample != 'Data' :
        subdir += sample
    if useMCTemplate :
        subdir += 'MCTemplate'
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
    if useCoarseEta :
        subdir += 'CoarseEta'


    if outputDir is not None :
        outputDir = outputDir + '/' + subdir

    pt_bins = [ 15, 25, 40, 80]
    pt_bins_80 = [ 80, 1000000 ]
    #eta_bins = [-2.5, -2.1, -1.57, -1.48, -0.1, 0.1, 1.48, 1.57, 2.1, 2.5]
    eta_bins = [0.0, 0.1, 0.5, 1.0, 1.48, 1.57, 2.1, 2.2, 2.3, 2.4, 2.5]
    eta_bins_80 = [0.0, 0.1, 0.5, 1.0, 1.48, 1.57, 2.1, 2.4, 2.5]
    #eta_bins = [2.1, 2.5]
    mass_binning = (100, 0, 200)

    if useCoarseEta :
        eta_bins = [0.0, 1.48, 1.57, 2.5]
        eta_bins_80 = [0.0, 1.48, 1.57, 2.5]

    pt_eta_bins = {}
    for idx, ptmin in enumerate(pt_bins[:-1]) :
        ptmax = pt_bins[idx+1]
        pt_eta_bins[(ptmin, ptmax)] = eta_bins
        
    for idx, ptmin in enumerate(pt_bins_80[:-1]) :
        ptmax = pt_bins_80[idx+1]
        pt_eta_bins[(ptmin, ptmax)] = eta_bins_80
        


    draw_cmds = get_ratio_draw_commands(isConv=isConv )
    selection_nom = draw_cmds['nom'] 
    selection_inv = draw_cmds['inv'] 

    hists = get_3d_mass_ratio_histograms( selection_nom, selection_inv, sample, mass_binning, useHist=useHist, useAbsEta=True )

    if useMCTemplate :
        
        if doNDKeys :
            results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, ndKeysSample='DYJetsToLLPhOlap', ndKeysSelection=selection_nom, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, outputDir =outputDir, namePrefix='_nom' )
            results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, ndKeysSample='DYJetsToLLPhOlap', ndKeysSelection=selection_inv, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, outputDir =outputDir, namePrefix='_inv' )
        else :
            template_hist = get_3d_mass_ratio_histograms( selection_nom, selection_inv, 'DYJetsToLLPhOlap', mass_binning, useHist=None, useAbsEta=True )

            results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, mcTemplate=template_hist['nom'], usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, outputDir =outputDir, namePrefix='_nom' )
            results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, mcTemplate=template_hist['inv'], usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, outputDir =outputDir, namePrefix='_inv' )
    else :
        results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, outputDir =outputDir, namePrefix='_nom' )
        results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, outputDir =outputDir, namePrefix='_inv' )

    write_output( results_nom, results_inv, outputDir )

def write_output( results_nom, results_inv, outputDir=None ) :

    sel_strs = []
    results_all = {}
    results_all['fake_ratio'] = {}
    results_all['fake_ratio_peak'] = {}
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

            for binx in range(ffhist.GetNbinsX() ) :
                for biny in range(ffhist.GetNbinsY() ) :
                    xcenter = ffhist.GetXaxis().GetBinCenter(binx+1) 
                    ycenter = ffhist.GetYaxis().GetBinCenter(biny+1) 
                    if xcenter > ptmin and xcenter < ptmax and ycenter > etamin and ycenter < etamax :
                        ffhist.SetBinContent( binx+1, biny+1 , ff.n )
                        ffhist.SetBinError( binx+1, biny+1 , ff.s )
        ffhist.Write()
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
    
def get_3d_mass_ratio_histograms( selection_nom, selection_inv, sample,  mass_binning, useHist=None ,useAbsEta=False ) :

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
        var_lead = 'm_lepph1:ph_pt[0]:fabs(ph_eta[0])' #z:y:x
        eta_nbin = 250
        eta_min = 0
        eta_max = 2.5
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


def fit_pt_eta_bins( hist, pt_eta_bins, mcTemplate=None, ndKeysSample=None, ndKeysSelection=None, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, outputDir=None, namePrefix='' ) :

    results_pt_eta = {}
    last_pt = max( [x[1] for x in pt_eta_bins.keys() ] )
    for (ptmin, ptmax), eta_bins in pt_eta_bins.iteritems()  :

        if options.ptmin > 0 and options.ptmin != ptmin :
            continue

        pt_bin_min = hist.GetYaxis().FindBin( ptmin )
        pt_bin_max = hist.GetYaxis().FindBin( ptmax )

        for etaidx, etamin in enumerate( eta_bins[:-1] ) :
            etamax = eta_bins[etaidx+1]

            eta_bin_min = hist.GetXaxis().FindBin( etamin )
            eta_bin_max = hist.GetXaxis().FindBin( etamax )

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

                pt_eta_selection = ndKeysSelection + ' && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f && ph_pt[0] > %d && ph_pt[0] < %d' %( etamin, etamax, ptmin, ptmax )

                orig_tree = sampMan.get_samples( name=ndKeysSample )[0].chain
                orig_tree.SetBranchStatus('*', 1)
                tmpfile = ROOT.TFile.Open( '/tmp/jkunkle/tmp.root', 'RECREATE' )
                new_tree = orig_tree.CopyTree( pt_eta_selection )

                #new_tree = sampMan.get_samples( name=ndKeysSample )[0].chain.CopyTree( pt_eta_selection )

                m_lepph1 = ROOT.RooRealVar( 'm_lepph1', 'm_lepph1', 40, 200 )
                ph_passMedium = ROOT.RooRealVar( 'ph_passMedium[0]', 'ph_passMedium[0]', 0, 1 )
                el_passtrig_n = ROOT.RooRealVar( 'el_passtrig_n', 'el_passtrig_n', 0, 10 )
                el_n = ROOT.RooRealVar( 'el_n', 'el_n', 0, 10 )
                ph_n = ROOT.RooRealVar( 'ph_n', 'ph_n', 0, 10 )
                ph_hasPixSeed = ROOT.RooRealVar( 'ph_hasPixSeed[0]', 'ph_hasPixSeed[0]', 0, 10 )
                ph_eta = ROOT.RooRealVar( 'ph_eta[0]', 'ph_eta[0]', -5., 5. )
                ph_pt = ROOT.RooRealVar( 'ph_pt[0]', 'ph_pt[0]', 0, 1000. )
                print pt_eta_selection
                data_set = ROOT.RooDataSet( 'dataset_%.2f_%.2f_%d_%d' %(etamin, etamax, ptmin, ptmax ), '', new_tree,ROOT.RooArgSet( m_lepph1))
                results = fit_hist_ndkeys( hist_proj, data_set, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, label=hist_proj.GetName(), outputName=output_name )
                tmpfile.Close()
            else :
                results = fit_hist_nominal( hist_proj, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, label=hist_proj.GetName(), outputName=output_name )

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

def fit_hist_nominal( data_hist, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, label=None, outputName=None ) :

    sampMan.fit_objs = {}

    if label is None :
        label = data_hist.GetName()

    # independent var
    xmin = 40
    xmax = 200

    m_lepph1 = ROOT.RooRealVar( 'm_lepph1', 'm_lepph1', xmin, xmax )

    model = fit_model_to_data( data_hist.GetName(), m_lepph1, data_hist, MCSig=None, doNDKeys=False, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg)

    draw_fitted_results( model, sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], sampMan.fit_objs['bkg_model'], m_lepph1, label, outputName=outputName )

    return store_results( m_lepph1 )

def fit_hist_mc_template( data_hist, template_hist, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, label=None, outputName=None ) :

    sampMan.fit_objs = {}

    if label is None :
        label = data_hist.GetName()

    xmin = 40
    xmax = 200

    # independent var
    m_lepph1 = ROOT.RooRealVar( 'm_lepph1', 'm_lepph1', xmin,xmax)

    model = fit_model_to_data( data_hist.GetName(), m_lepph1, data_hist, MCSig=template_hist, doNDKeys=False, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg)

    draw_fitted_results( model, sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], sampMan.fit_objs['bkg_model'], m_lepph1, label, outputName=outputName )

    return store_results( m_lepph1 )

def fit_hist_ndkeys( data_hist, template_dataset, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, label=None, outputName=None ) :

    sampMan.fit_objs = {}

    if label is None :
        label = data_hist.GetName()

    xmin = 40
    xmax = 200

    # independent var
    m_lepph1 = ROOT.RooRealVar( 'm_lepph1', 'm_lepph1', xmin,xmax)

    model = fit_model_to_data( data_hist.GetName(), m_lepph1, data_hist, MCSig=template_dataset, doNDKeys=True, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg)
    
    draw_fitted_results( model, sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], sampMan.fit_objs['bkg_model'], m_lepph1, label, outputName=outputName )

    return store_results( m_lepph1 )

def fit_model_to_data( hist_name, var, data_hist, MCSig=None, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False) :

    global sampMan

    if not hasattr( sampMan, 'fit_objs' ) :
        sampMan.fit_objs = {}

    fit_defs = get_fit_defaults( hist_name, useGaussSig=(MCSig is not None), usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg )

    if MCSig is not None :

        sampMan.fit_objs['mean'] = ROOT.RooRealVar('mean', 'Gaussian Z mass', fit_defs['mean'], -5, 5,'GeV/c^{2}')
        sampMan.fit_objs['sigma'] = ROOT.RooRealVar('sigma', '#sigma', fit_defs['sigma'], 0.2,4.0,'GeV/c^{2}')

        sampMan.fit_objs['gauss'] = ROOT.RooGaussian('gaussian','Signal shape gaussian',var, sampMan.fit_objs['mean'], sampMan.fit_objs['sigma'])

        if doNDKeys :

            sampMan.fit_objs['sig_template'] = ROOT.RooNDKeysPdf( 'sig_template', 'sig_template', ROOT.RooArgList(var), MCSig )

            #  Convolution p.d.f. using numeric convolution operator based on Fourier Transforms
            sampMan.fit_objs['sig_model'] = ROOT.RooFFTConvPdf('sig_model','Convolution', var, sampMan.fit_objs['sig_template'], sampMan.fit_objs['gauss'])

        else :

            sampMan.fit_objs['sig_template_hist'] = ROOT.RooDataHist( 'template_hist', 'template_hist', ROOT.RooArgList( var ), MCSig )
            sampMan.fit_objs['sig_template'] = ROOT.RooHistPdf( 'sig_template', 'sig_template', ROOT.RooArgSet( var ), sampMan.fit_objs['sig_template_hist'] )

            #  Convolution p.d.f. using numeric convolution operator based on Fourier Transforms
            sampMan.fit_objs['sig_model'] = ROOT.RooFFTConvPdf('sig_model','Convolution', var, sampMan.fit_objs['sig_template'], sampMan.fit_objs['gauss'])

    else :
        #  Parameters for Crystal Ball Lineshape
        sampMan.fit_objs['m0']    = ROOT.RooRealVar('#Delta m_{0}', 'Bias' , fit_defs['Bias'] , -3.0 , 2.0,'GeV/c^{2}')
        sampMan.fit_objs['sigma'] = ROOT.RooRealVar('#sigma_{CB}' , 'Width', fit_defs['Width'], 0.5  , 3.5, 'GeV/c^{2}')
        sampMan.fit_objs['cut']   = ROOT.RooRealVar('#alpha'      , 'Cut'  , fit_defs['Cut']  , -10.0, 0. , ''  )
        sampMan.fit_objs['power'] = ROOT.RooRealVar('#gamma'      , 'Power', fit_defs['Power'], 5    , 30 , ''  )

        #  Parameters for Breit-Wigner Distribution
        sampMan.fit_objs['mRes'] = ROOT.RooRealVar('M_{Z^{0}}', 'Z0 Resonance  Mass', 91.188, 88.0, 94.0,'GeV/c^{2}')
        sampMan.fit_objs['Gamma'] = ROOT.RooRealVar('#Gamma', '#Gamma', 2.495, 1,4.0,'GeV/c^{2}')
        sampMan.fit_objs['mRes'].setConstant()
        sampMan.fit_objs['Gamma'].setConstant()

        sampMan.fit_objs['cb'] = ROOT.RooCBShape('cb', 'A  Crystal Ball Lineshape', var, sampMan.fit_objs['m0'], sampMan.fit_objs['sigma'], sampMan.fit_objs['cut'], sampMan.fit_objs['power'])
        #  Breit-Wigner Lineshape
        sampMan.fit_objs['bw'] = ROOT.RooBreitWigner('bw','A Breit-Wigner Distribution', var, sampMan.fit_objs['mRes'],sampMan.fit_objs['Gamma'])

        #  Convolution p.d.f. using numeric convolution operator based on Fourier Transforms
        sampMan.fit_objs['sig_model'] = ROOT.RooFFTConvPdf('sig_model','Convolution', var, sampMan.fit_objs['bw'], sampMan.fit_objs['cb'])


    if usePolyBkg :
        sampMan.fit_objs['poly_1'] = ROOT.RooRealVar( 'poly_1', 'linear term'   , fit_defs['poly_linear']   , -1000, 1000, '' )
        sampMan.fit_objs['poly_2'] = ROOT.RooRealVar( 'poly_2', 'quadratic term', fit_defs['poly_quadratic'], -1000, 0   , '' )
        sampMan.fit_objs['poly_3'] = ROOT.RooRealVar( 'poly_3', 'cubic term'    , fit_defs['poly_cubic']    , -100 , 100 , '' )
        sampMan.fit_objs['poly_4'] = ROOT.RooRealVar( 'poly_4', 'quartic term'  , fit_defs['poly_quartic']  , -100 , 100 , '' )

        sampMan.fit_objs['bkg_model'] = ROOT.RooPolynomial('bkg_model', 'Cubic polynomial', var, ROOT.RooArgList(sampMan.fit_objs['poly_1'], sampMan.fit_objs['poly_2'], sampMan.fit_objs['poly_3'], sampMan.fit_objs['poly_4']))
        

    elif useExpBkg :

        sampMan.fit_objs['width'] = ROOT.RooRealVar ('width', 'exponential width', fit_defs['exp_width'], -10, 10 )
        #sampMan.fit_objs['start'] = ROOT.RooRealVar ('start', 'exponential start', fit_defs['exp_start'], 0, 100 )
        #sampMan.fit_objs['start'].setConstant()

        #sampMan.fit_objs['bkg_model'] = ROOT.RooGenericPdf( 'bkg_model', 'Exponential', 'exp(width * (start - %s))' %var.GetName(), ROOT.RooArgList( var, sampMan.fit_objs['width'], sampMan.fit_objs['start']) )
        sampMan.fit_objs['bkg_model'] = ROOT.RooExponential( 'bkg_model', 'Exponential', var,  sampMan.fit_objs['width'] )

    elif useChebyBkg :

        sampMan.fit_objs['cheby_a0'] = ROOT.RooRealVar ('a0', 'chebychev 0', fit_defs['a0'], -10, 10 )
        sampMan.fit_objs['cheby_a1'] = ROOT.RooRealVar ('a1', 'chebychev 1', fit_defs['a1'], -10, 10 )
        sampMan.fit_objs['cheby_a2'] = ROOT.RooRealVar ('a2', 'chebychev 2', fit_defs['a2'], -10, 10 )

        sampMan.fit_objs['bkg_model'] = ROOT.RooChebychev( 'bkg_model', 'Chebychev',  var, ROOT.RooArgList( sampMan.fit_objs['cheby_a0'], sampMan.fit_objs['cheby_a1'], sampMan.fit_objs['cheby_a2']) )

    elif useBernsteinBkg:

        sampMan.fit_objs['bern_b0'] = ROOT.RooRealVar ('b0', 'bernstein 0', fit_defs['b0'], -10, 10 )
        sampMan.fit_objs['bern_b1'] = ROOT.RooRealVar ('b1', 'bernstien 1', fit_defs['b1'], -10, 10 )
        sampMan.fit_objs['bern_b2'] = ROOT.RooRealVar ('b2', 'bernstien 2', fit_defs['b2'], -10, 10 )

        sampMan.fit_objs['bkg_model'] = ROOT.RooBernstein( 'bkg_model', 'Bernstein',  var, ROOT.RooArgList( sampMan.fit_objs['bern_b0'], sampMan.fit_objs['bern_b1'], sampMan.fit_objs['bern_b2']) )

    else :
    
        # Generate ROOCMSShape
        sampMan.fit_objs['cms_alpha'] = ROOT.RooRealVar('cms_alpha', 'cms_alpha', fit_defs['cms_alpha'], 50, 200, '')
        sampMan.fit_objs['cms_beta']  = ROOT.RooRealVar('cms_beta' , 'cms_beta' , fit_defs['cms_beta'] , 0., 0.8  , '')
        sampMan.fit_objs['cms_gamma'] = ROOT.RooRealVar('cms_gamma', 'cms_gamma', fit_defs['cms_gamma'], 0 , 0.3, '')
        sampMan.fit_objs['cms_peak']  = ROOT.RooRealVar('cms_peak' , 'cms_peak' , fit_defs['cms_peak'] , 85, 95 , '')

        sampMan.fit_objs['bkg_model'] = ROOT.RooCMSShape('bkg_model', 'CMSShape', var, sampMan.fit_objs['cms_alpha'], sampMan.fit_objs['cms_beta'], sampMan.fit_objs['cms_gamma'], sampMan.fit_objs['cms_peak'])

    # fitted values
    sampMan.fit_objs['nsig'] = ROOT.RooRealVar('N_{S}', '#signal events'    , fit_defs['nsig'],0,1000000.)
    sampMan.fit_objs['nbkg'] = ROOT.RooRealVar('N_{B}', '#background events', fit_defs['nbkg'],0,1000000.)

    sampMan.fit_objs['model'] = ROOT.RooAddPdf('model', 'Di-photon Mass model', ROOT.RooArgList(sampMan.fit_objs['sig_model'], sampMan.fit_objs['bkg_model']), ROOT.RooArgList(sampMan.fit_objs['nsig'], sampMan.fit_objs['nbkg']))

    # data
    sampMan.fit_objs['target_data'] = ROOT.RooDataHist( 'target_data', 'target_data', ROOT.RooArgList(var), data_hist)

    sampMan.fit_objs['fit_result'] = sampMan.fit_objs['model'].fitTo(sampMan.fit_objs['target_data'],ROOT.RooFit.Range(fit_defs['fit_min'], fit_defs['fit_max']),ROOT.RooFit.SumW2Error(True),ROOT.RooFit.Save()) ;

    return sampMan.fit_objs['model']

def draw_fitted_results( model, target_data, sig_model, bkg_model, var, label, outputName=None ) :

    can = ROOT.TCanvas( str(uuid.uuid4()), '' )
    frame = var.frame()
    target_data.plotOn(frame)
    model.plotOn(frame)
    model.plotOn(frame, ROOT.RooFit.Components('sig_model'), ROOT.RooFit.LineStyle(ROOT.kDashed)) 
    model.plotOn(frame, ROOT.RooFit.Components('bkg_model'), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) ) 
    frame.SetTitle('')
    model.Print()


    frame.Draw()
    lab = ROOT.TLatex( 0.6, 0.85, label  )
    lab.SetNDC()
    lab.SetX(0.4)
    lab.SetY(0.91)
    lab.Draw()
    if outputName is None :
        model.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        raw_input('continue')
    else :
        name = outputName + '.pdf'
        name_log = outputName + '__logy.pdf'
        name_nopar = outputName + '__nopar.pdf'
        if not os.path.isdir( os.path.split( name )[0] ) :
            os.makedirs( os.path.split( name )[0] )
        can.SetLogy()
        can.SaveAs(name_nopar)
        model.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        lab.Draw()
        can.SetLogy(0)
        can.SaveAs(name)
        can.SetLogy()
        can.SaveAs(name_log)

def store_results( var ) :

    results = {}

    xmin = var.getMin()
    xmax = var.getMax()

    print xmin
    print xmax

    hist_sig = sampMan.fit_objs['sig_model'].createHistogram('hist_sig_model', var, ROOT.RooFit.Binning( int((xmax-xmin)*10), xmin, xmax ) )
    hist_bkg = sampMan.fit_objs['bkg_model'].createHistogram('hist_bkg_model', var, ROOT.RooFit.Binning( int((xmax-xmin)*10), xmin, xmax ) )

    int_min = 91.2-10
    int_max = 91.2+10

    bin_min = hist_sig.FindBin( int_min )
    bin_max = hist_sig.FindBin( int_max )

    int_sig_err = ROOT.Double()
    int_bkg_err = ROOT.Double()
    int_sig = hist_sig.IntegralAndError( bin_min, bin_max, int_sig_err )
    int_bkg = hist_bkg.IntegralAndError( bin_min, bin_max, int_bkg_err )

    for name, obj in sampMan.fit_objs.iteritems() :

        if isinstance( obj, ROOT.RooRealVar ) :
            results[name] = ufloat( obj.getVal(), obj.getError() )

    results['nsig_peak'] = ufloat( int_sig, int_sig_err )
    results['nbkg_peak'] = ufloat( int_bkg, int_bkg_err )

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
