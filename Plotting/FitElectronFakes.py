"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('--baseDir',      default=None,           dest='baseDir',         help='Path to base directory')
p.add_argument('--dirNom',       default=None,           dest='dirNom',         help='directory containing all ntuples with inverted selection')
p.add_argument('--dirInv',       default=None,           dest='dirInv',         help='directory containing all ntuples with nominal selection')
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

p.add_argument('--bw_cms_fine'       ,     default=False, action='store_true',  dest='bw_cms_fine', help='Fit Signal Breit wigner convoluted with crysal ball and background CMS shape, fine eta bins')
p.add_argument('--bw_cms_coarse'     ,     default=False, action='store_true',  dest='bw_cms_coarse', help='Fit Signal Breit wigner convoluted with crysal ball and background CMS shape, coarse eta bins')

p.add_argument('--bw_exp_fine'       ,     default=False, action='store_true',  dest='bw_exp_fine', help='Fit Signal Breit wigner convoluted with crysal ball and background exp shape, fine eta bins')
p.add_argument('--bw_exp_coarse'     ,     default=False, action='store_true',  dest='bw_exp_coarse', help='Fit Signal Breit wigner convoluted with crysal ball and background exp shape, coarse eta bins')

p.add_argument('--ndkeys_cms_fine'   ,     default=False, action='store_true',  dest='ndkeys_cms_fine', help='Fit Signal MC Gaussian smeared and background CMS shape, fine eta bins')
p.add_argument('--ndkeys_cms_coarse' ,     default=False, action='store_true',  dest='ndkeys_cms_coarse', help='Fit Signal MC Gaussian smeared and background CMS shape, coarse eta bins')
p.add_argument('--ndkeys_exp_fine'   ,     default=False, action='store_true',  dest='ndkeys_exp_fine', help='Fit Signal MC Gaussian smeared and background Exponential shape, fine eta bins')
p.add_argument('--ndkeys_exp_coarse' ,     default=False, action='store_true',  dest='ndkeys_exp_coarse', help='Fit Signal MC Gaussian smeared and background Exponential shape, coarse eta bins')
p.add_argument('--mc_cms_fine'       ,     default=False, action='store_true',  dest='mc_cms_fine', help='Fit Signal MC and background CMS shape, fine eta bins')
p.add_argument('--mc_cms_coarse'     ,     default=False, action='store_true',  dest='mc_cms_coarse', help='Fit Signal MC and background CMS shape, coarse eta bins')
p.add_argument('--mc_exp_fine'       ,     default=False, action='store_true',  dest='mc_exp_fine', help='Fit Signal MC and background Exponential shape, fine eta bins')
p.add_argument('--mc_exp_coarse'     ,     default=False, action='store_true',  dest='mc_exp_coarse', help='Fit Signal MC and background Exponential shape, coarse eta bins')
p.add_argument('--mc_mc_fine'       ,     default=False, action='store_true',  dest='mc_mc_fine', help='Fit Signal MC and Background MC shape, fine eta bins')
p.add_argument('--mc_mc_coarse'       ,     default=False, action='store_true',  dest='mc_mc_coarse', help='Fit Signal MC and Background MC shape, coarse eta bins')
p.add_argument('--ndkeys_ndkeys_fine'       ,     default=False, action='store_true'  ,  dest='ndkeys_ndkeys_fine', help='Fit Signal MC and Background MC shape, fine eta bins')
p.add_argument('--ndkeys_ndkeys_coarse'       ,     default=False, action='store_true',  dest='ndkeys_ndkeys_coarse', help='Fit Signal MC and Background MC shape, coarse eta bins')
p.add_argument('--useCsev',     default=False, action='store_true',  dest='useCsev', help='Use conversion save electron veto instead of pixel seed veto')
p.add_argument('--useTAndP',     default=False, action='store_true',  dest='useTAndP', help='Use tag and probe ntuples')
p.add_argument('--mc',     default=False, action='store_true',  dest='mc', help='Use counting method on the MC')



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
import FitDefs


if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
else :
    ROOT.gROOT.SetBatch(False)

sampMan = None

global_hists={}

def get_default_draw_commands( ) :

    #return { 'FF' :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==1 && ph_elMinDR[0]>0.2 && ph_elMinDR[1]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_sceta[0])<2.5 && fabs(ph_sceta[1]) < 2.5' , 
    #         'RF'  :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && ph_elMinDR[0]>0.2  && ph_elMinDR[1]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_sceta[0])<2.5 && fabs(ph_sceta[1]) < 2.5',
    #         'FR'  :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && ph_elMinDR[0]>0.2 && ph_elMinDR[1]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_sceta[0])<2.5 && fabs(ph_sceta[1]) < 2.5',
    #         'RR' :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_elMinDR[0]>0.2  && ph_elMinDR[1]>0.2  && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_sceta[0])<2.5 && fabs(ph_sceta[1]) < 2.5',
    #       }

    return { 'FF' :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==1 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_sceta[0])<2.5 && fabs(ph_sceta[1]) < 2.5' , 
             'RF'  :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && ph_elMinDR[0]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_sceta[0])<2.5 && fabs(ph_sceta[1]) < 2.5',
             'FR'  :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && ph_elMinDR[1]>0.2 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_sceta[0])<2.5 && fabs(ph_sceta[1]) < 2.5',
             'RR' :'ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_phDR>0.3 && ph_pt[0]>15 && ph_pt[1]>15 && fabs(ph_sceta[0])<2.5 && fabs(ph_sceta[1]) < 2.5',
           }

def get_photon_vars( fittype, useCsev=False ) :

    if fittype == 'nom' :
        if useCsev :
            return ('ph_mediumPassCSEV_n', 'ptSorted_ph_mediumPassCSEV_idx' )
        else :
            return ('ph_mediumPassPSV_n' , 'ptSorted_ph_mediumPassPSV_idx' )
    if fittype == 'inv' :
        if useCsev :
            return ('ph_mediumFailCSEV_n', 'ptSorted_ph_mediumFailCSEV_idx' )
        else :
            return ('ph_mediumFailPSV_n' , 'ptSorted_ph_mediumFailPSV_idx' )


def get_ratio_draw_commands( isConv=None, useCsev=False, useTAndP=False, mc=False ) :

    phcutnom,phidxnom = get_photon_vars( 'nom', useCsev )
    phcutinv,phidxinv = get_photon_vars( 'inv', useCsev )

    if isConv==False :

        return { 
                 'nom'  :'passTrig_ele27WP80 && el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && !ph_isConv[0]',
                 'inv'  :'passTrig_ele27WP80 && el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && !ph_isConv[0]',
               }
    elif isConv==True :

        return { 
                 'nom'  :'passTrig_ele27WP80 && el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && ph_isConv[0]',
                 'inv'  :'passTrig_ele27WP80 && el_passtrig_n>0 && el_n==1 && ph_n==1 && leadPhot_leadLepDR>0.4 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && ph_isConv[0]',
               }
    elif useCsev :

        if useTAndP :
            return { 
                     'nom'  :'probe_isPhoton && probe_eleVeto == 0 ',
                     'inv'  :'probe_isPhoton && probe_eleVeto == 1 ',
                   }
        else :

            nom = 'el_passtrig_n==1 && el_n==1 && ph_mediumPassCSEV_n==1  && ph_eleVeto[ptSorted_ph_mediumPassCSEV_idx[0]]==0 && dr_ph1_trigEle > 0.4'
            inv = 'el_passtrig_n==1 && el_n==1 && ph_mediumFailCSEV_n==1  && ph_eleVeto[ptSorted_ph_mediumFailCSEV_idx[0]]==1 && dr_ph1_trigEle > 0.4 '

            if mc : 
                return { 'nom' : nom + ' && ph_truthMatch_el[%s[0]] ' %phidxnom, 'inv' : inv +  ' && ph_truthMatch_el[%s[0]]' %phidxinv}
            else :
                return { 'nom'  : nom, 'inv'  : inv,}

    else :
        if useTAndP:
            return { 
                     'nom'  :'probe_hasPixSeed == 0 ',
                     'inv'  :'probe_hasPixSeed == 1 ',
                   }
        else :

            nom = 'el_passtrig_n>0 && el_n==1 && %s==1  && ph_hasPixSeed[%s[0]]==0 && dr_ph1_trigEle > 0.4' %( phcutnom, phidxnom )
            #inv = 'el_passtrig_n>0 && el_n>0 && %s==1  && ph_hasPixSeed[%s[0]]==1 && dr_ph1_trigEle > 0.4 '%( phcutinv, phidxinv )
            inv = 'el_passtrig_n>0 && el_n>0 && ph_n==1 '

            if mc : 
                return { 'nom' : nom + ' && ph_truthMatch_el[%s[0]] ' %phidxnom, 'inv' : inv +  ' && ph_truthMatch_el[%s[0]]'%phidxinv }
            else :
                return { 'nom'  : nom, 'inv'  : inv,}


def get_fit_defaults( histname, useGaussSig=False, useLandauSig=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useMCBkg=False, useTAndP=False ) :


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
    if useBernsteinBkg:
        bkg = 'mc'

    if useTAndP :
        bkg += '_tandp'

    defname = '%s_%s' %( sig, bkg)
    print defname
    if histname in FitDefs.alts[defname] :
        return FitDefs.alts[defname][histname]
    else :
        return FitDefs.defaults[defname]

def main() :

    global sampManNom
    global sampManInv

    if not options.baseDir.count('/eos/') and not os.path.isdir( options.baseDir ) :
        print 'baseDir not found!'
        return

    sampManNom = SampleManager('%s/%s'%( options.baseDir, options.dirNom ), options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    sampManInv = SampleManager('%s/%s'%( options.baseDir, options.dirInv ), options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)


    if options.samplesConf is not None :

        sampManInv.ReadSamples( options.samplesConf )
        sampManNom.ReadSamples( options.samplesConf )

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
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=False, useMCTemplate=True, useMCTemplateBackground=False, doNDKeys=True, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, extra_bkg_sample=extra_bkg_sample, useCsev=options.useCsev, useTAndP=options.useTAndP)
    if options.ndkeys_cms_coarse :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=True, useMCTemplate=True, doNDKeys=True, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    #--------------------------
    # Use MC signal and backgrond template with NDKeys smearing
    # For nominal fits
    #--------------------------
    extra_bkg_sample = 'FakeBackgroundSamples'
    #extra_bkg_sample = None
    if options.ndkeys_ndkeys_fine :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=False, useMCTemplate=True, useMCTemplateBackground=True, doNDKeys=True, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, extra_bkg_sample=extra_bkg_sample, useCsev=options.useCsev, useTAndP=options.useTAndP)
    if options.ndkeys_ndkeys_coarse:
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=True, useMCTemplate=True, useMCTemplateBackground=True, doNDKeys=True, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

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

    #--------------------------
    # Use MC template with NDKeys smearing with cms shape bkg
    # For nominal fits
    #--------------------------
    #extra_bkg_sample = 'Zgamma'
    extra_bkg_sample = None
    if options.mc_cms_fine :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=False, useMCTemplate=True, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, extra_bkg_sample=extra_bkg_sample, useCsev=options.useCsev, useTAndP=options.useTAndP)
    if options.mc_cms_coarse :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=True, useMCTemplate=True, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    #--------------------------
    # Use MC template with exponential bkg
    # For syst variations
    #--------------------------
    if options.mc_exp_fine :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=False, useMCTemplate=True, doNDKeys=False, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)
    if options.mc_exp_coarse :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=True, useMCTemplate=True, doNDKeys=False, usePolyBkg=False, useExpBkg=True, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    if options.mc_mc_fine :
        extra_bkg_sample = 'FakeBackgroundSamples'
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=False, useMCTemplate=True, useMCTemplateBackground=True, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP, extra_bkg_sample=extra_bkg_sample)
    if options.mc_mc_coarse :
        DoElectronFakeFitRatio( outputDir=options.outputDir,useHist=useHist, useCoarseEta=True, useMCTemplate=True, useMCTemplateBackground=True, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    ##--------------------------
    ## Use Landau Sig with cmsshap bkg
    ##--------------------------
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=False, doNDKeys=False, useLandauSig=True, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    ##--------------------------
    ## Use MC template with cms shape bkg
    ##--------------------------
    #DoElectronFakeFitRatio( outputDir=options.outputDir,useHist='.EleFitData', useCoarseEta=False, useMCTemplate=True, doNDKeys=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCsev=options.useCsev, useTAndP=options.useTAndP)

    if options.mc :
        DoElectronFakeCountRatio( outputDir=options.outputDir, sample='ZjetsZgamma', mode='truth_window' )
        DoElectronFakeCountRatio( outputDir=options.outputDir, sample='ZjetsZgamma', mode='reco_window' )

def DoElectronFakeCountRatio( outputDir, sample, mode='reco_window' ) :


    subDir = 'ElectronFakeCountsMC'

    draw_cmds = get_ratio_draw_commands( )

    selection_nom = draw_cmds['nom'] 
    selection_inv = draw_cmds['inv'] 

    mass_binning = (100, 0, 200)

    if mode == 'reco_window' :
        ff_tests = {'central' : 'fabs( m_lepph1-91.2 ) < 10', 'full' : '' }
    elif mode == 'truth_window' :
        ff_tests = {'central' : 'fabs( true_m_leplep - m_lepph1 ) < 10', 'full' : '' }

    # ----------------------------------------------
    # define binning
    # ----------------------------------------------
    pt_bins = [(15,25), (25,40), (40,70)]
    pt_bins_80 = [ (70, 1000000) ]

    eta_bins    = [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44), (1.57, 2.1), (2.1, 2.2), (2.2, 2.4), (2.4, 2.5) ]
    eta_bins_80 = [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44), (1.57, 2.1), (2.1, 2.4), (2.4, 2.5) ]

    pt_eta_bins = {}
    for pts in pt_bins :
        pt_eta_bins[pts] = eta_bins
        
    for pts in pt_bins_80 :
        pt_eta_bins[pts] = eta_bins_80

    # ----------------------------------------------

    results = {}

    for ff_tag, ff_test in ff_tests.iteritems() :
        results[ff_tag] = {}
        if ff_test :
            selection_nom = selection_nom + ' & %s' %ff_test
            selection_inv = selection_inv + ' & %s' %ff_test

        hists = get_3d_mass_ratio_histograms( selection_nom, selection_inv, sample, mass_binning, useAbsEta=True )


        last_pt = max( [x[1] for x in pt_eta_bins.keys() ] )
        for (ptmin, ptmax), eta_bins in pt_eta_bins.iteritems()  :

            if options.ptmin > 0 and options.ptmin != ptmin :
                continue

            # If FindBin is given a value on the boundary it returns
            # the bin above the boundary
            # Therefore the max bin is 1 less than what is returned

            for etaidx, (etamin, etamax) in enumerate( eta_bins ) :

                if options.etabinmin >= 0 and options.etabinmin != etaidx :
                    continue


                result_bin = ( str( ptmin ), str(ptmax), '%.2f' %etamin, '%.2f' %etamax )
                results[ff_tag][result_bin] = {}


                for hist_tag, hist in hists.iteritems() :

                    pt_bin_min = hist.GetYaxis().FindBin( ptmin )
                    pt_bin_max = hist.GetYaxis().FindBin( ptmax ) - 1 

                    eta_bin_min = hist.GetXaxis().FindBin( etamin )
                    eta_bin_max = hist.GetXaxis().FindBin( etamax ) - 1

                    print 'ptmin = %d, ptmax = %d, etamin = %f, etamax = %f ' %(ptmin, ptmax, etamin, etamax )
                    print 'BIN : ptmin = %d, ptmax = %d, etamin = %d, etamax = %d ' %(pt_bin_min, pt_bin_max, eta_bin_min, eta_bin_max )

                    if ptmax == last_pt :
                        histname = 'hist%s%s_eta_%.2f-%.2f_pt_%d-max' %(ff_tag, hist_tag, etamin, etamax, ptmin)
                    else :
                        histname = 'hist%s%s_eta_%.2f-%.2f_pt_%d-%d' %(ff_tag, hist_tag, etamin, etamax, ptmin, ptmax)

                    hist_proj = hist.ProjectionZ(histname, eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )

                    err = ROOT.Double()
                    int = hist_proj.IntegralAndError(1, hist_proj.GetNbinsX(), err)
                    results[ff_tag][result_bin][hist_tag] = ufloat( int, err )

        
                results[ff_tag][result_bin]['fake_factor'] = 0.0
                if results[ff_tag][result_bin]['inv'] != 0 :
                    results[ff_tag][result_bin]['fake_factor'] = results[ff_tag][result_bin]['nom']/results[ff_tag][result_bin]['inv']

    for tag, ffres in results.iteritems() :
        for bin, binres in ffres.iteritems() :
            print 'Test = %s, bin = %s, fake factor = %s' %( tag, bin, binres['fake_factor'] )

                    
    print results
    full_dir = '%s/%s' %(outputDir, subDir)
    if not os.path.isdir( full_dir ) :
        os.makedirs( full_dir )
    ofile = open( '%s/results_%s.pickle' %(full_dir, mode ), 'w' )
    pickle.dump( results, ofile )
    ofile.close()



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


def InvDoElectronFakeFit( outputDir=None, useHist=None) :

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

def DoElectronFakeFitRatio( outputDir=None, sample='Data', isConv=None, useCsev=False, useTAndP=False, useHist=None, useCoarseEta=False, useMCTemplate=False, useMCTemplateBackground=False, useLandauSig=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, doNDKeys=False, extra_bkg_sample=None) :

    print '**********************************************FIX*******************************************'
    #subdir = 'ElectronFakeFitsRatioDupInvMatchEleNewFixEta'
    subdir = 'ElectronFakeFitsRatioDupInvMatchEleNewFixEta24'

    if useCsev :
        subdir += 'CSEV'
    if useTAndP :
        subdir += 'TAndP'
    if sample != 'Data' :
        subdir += sample
    if useMCTemplate :
        subdir += 'MCTemplate'
    if useMCTemplateBackground :
        subdir += 'Bkg'
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

    #dy_sample_inv ='job_summer12_DYJetsToLL_s10PhOlapRepeat'
    dy_sample_nom ='job_summer12_DYJetsToLL_s10PhOlap'
    dy_sample_inv ='job_summer12_DYJetsToLL_s10PhOlap'

    useCmsShapeBkg=True
    if usePolyBkg or useExpBkg or useChebyBkg or useBernsteinBkg or useMCTemplateBackground   :
        useCmsShapeBkg = False

    if outputDir is not None :
        outputDir = outputDir + '/' + subdir

    #pt_bins = [(15,25), (25,40), (40,70), (15, 40), (15, 70), (15, 1000000) ]
    #pt_bins = [(15,20),(20,25),(25,30),(30,35),(35,40),(40,45),(45,50),(50,60),(60,70),(70,1000000) ]
    pt_bins = [(15,25),(25,30), (30,35), (35,40),(40,45),(45,50), (50,60), (60,70),(70,1000000) ]
    #pt_bins = [(40,50), (50,60), (60,70),(70,1000000) ]
    #pt_bins = [(70,1000000) ]
    #pt_bins_80 = [ (70, 1000000) ]

    subl_pt_bins = { (15, 40) : [ (15, 25), (25, 30), (30, 35), (35, 40) ], 
                     (25, 40) : [(25, 30), (30, 35), (35, 40) ],
                     (40, 70) : [(40,45), (45,50), (50,60), (60,70) ],
                     (15, 70) : [ (15, 25), (25, 30), (30, 35), (35, 40), (40,45), (45,50), (50,60), (60,70)],
                     (15, 1000000) : [ (15, 25), (25, 30), (30, 35), (35, 40), (40,45), (45,50), (50,60), (60,70), (70, 1000000)],
                     (25, 1000000) : [ (25, 30), (30, 35), (35, 40), (40,45), (45,50), (50,60), (60,70), (70, 1000000)],
                     (40, 1000000) : [ (40,45), (45,50), (50,60), (60,70), (70, 1000000)],
                   }
    #subl_pt_bins = { (15, 40) : [(15,20),(20,25),(25,30),(30,35),(35,40) ], 
    #                (15, 70) : pt_bins[:-1] ,
    #                 (15, 1000000) : pt_bins,
    #               }

    print '**********************************************FIX*******************************************'
    raw_input('cont')

    #coarse_eta_bins = { ('0.00', '1.44') : [ ('0.00', '0.10'), ('0.10', '0.50'), ('0.50', '1.00'), ('1.00', '1.44') ], 
    #                    ('1.57', '2.50') : [ ('1.57', '2.10'), ('2.10', '2.20'), ('2.20', '2.40'), ('2.40', '2.50')],
    #                  }

    coarse_eta_bins = { ('0.00', '1.44') : [ ('0.00', '0.10'), ('0.10', '0.50'), ('0.50', '1.00'), ('1.00', '1.44') ], 
                        ('1.57', '2.50') : [ ('1.57', '2.10'), ('2.10', '2.20'), ('2.20', '2.40')],
                      }

    eta_bins = [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44), (1.57, 2.1), (2.1, 2.2), (2.2, 2.4), (2.4, 2.5) ]
    #eta_bins = [(0.0, 1.44), (1.57, 2.5) ]
    #eta_bins_80 = [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44), (1.57, 2.1), (2.1, 2.4), (2.4, 2.5) ]
    mass_binning = (50, 0, 200)

    if useCoarseEta :
        eta_bins = [(0.0, 1.44), (1.57, 2.5)]
        #eta_bins_80 = [(0.0, 1.44), (1.57, 2.5)]

    pt_eta_bins = {}
    for pts in pt_bins :
        pt_eta_bins[pts] = eta_bins
        
    #for pts in pt_bins_80 :
    #    pt_eta_bins[pts] = eta_bins_80
        

    draw_cmds = get_ratio_draw_commands(isConv=isConv, useCsev=useCsev, useTAndP=useTAndP )
    selection_nom = draw_cmds['nom'] 
    selection_inv = draw_cmds['inv'] 
    
    phidxnom = get_photon_vars( 'nom', useCsev=useCsev ) [1]
    phidxinv = get_photon_vars( 'inv', useCsev=useCsev ) [1]

    hists = get_3d_mass_ratio_histograms( selection_nom, selection_inv, sample, mass_binning, useHist=useHist, useAbsEta=True, useTAndP=useTAndP )

    if useMCTemplate :
        hists_extra={'nom' : None, 'inv' : None }
        if extra_bkg_sample is not None :
            hists_extra = get_3d_mass_ratio_histograms( selection_nom, selection_inv, extra_bkg_sample, mass_binning, useHist=useHist, useAbsEta=True, useTAndP=useTAndP )
        
        if doNDKeys :
            draw_cmds_mc = get_ratio_draw_commands(isConv=isConv, useCsev=useCsev, useTAndP=useTAndP, mc=False )
            selection_mc_nom = draw_cmds_mc['nom'] 
            selection_mc_inv = draw_cmds_mc['inv'] 

            selection_mc_nom +=  ' && fabs( ph_sceta[%s[0]]) '%phidxnom + '> %(etamin)f' 
            selection_mc_nom +=  ' && fabs(ph_sceta[%s[0]]) '%phidxnom + ' < %(etamin)f'
            selection_mc_nom +=  ' && ph_pt[%s[0]] '%phidxnom + '> %(ptmin)d'
            selection_mc_nom +=  ' && ph_pt[%s[0]] '%phidxnom + '< %(ptmax)d'  

            selection_mc_inv +=  ' && fabs( ph_sceta[%s[0]]) '%phidxinv + '> %(etamin)f' 
            selection_mc_inv +=  ' && fabs(ph_sceta[%s[0]]) '%phidxinv + ' < %(etamin)f'
            selection_mc_inv +=  ' && ph_pt[%s[0]] '%phidxinv + '> %(ptmin)d'
            selection_mc_inv +=  ' && ph_pt[%s[0]] '%phidxinv + '< %(ptmax)d'  

            if useMCTemplateBackground :
                bkg_str = '1.0/EffectiveLumi * '
                results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, ndKeysSample=dy_sample_nom, ndKeysSampleBkg=extra_bkg_sample, ndKeysSelection=selection_mc_nom, ndKeysSelectionBkg=bkg_str, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, extraBkgHist=hists_extra['nom'], useTAndP=options.useTAndP, outputDir =outputDir, selType='nom' )
                results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, ndKeysSample=dy_sample_inv, ndKeysSampleBkg=extra_bkg_sample, ndKeysSelection=selection_mc_inv, ndKeysSelectionBkg=bkg_str, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, extraBkgHist=hists_extra['inv'], useTAndP=options.useTAndP, outputDir =outputDir, selType='inv' )
            else :
                results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, ndKeysSample=dy_sample_inv, ndKeysSelection=selection_mc_inv, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, extraBkgHist=hists_extra['inv'], useTAndP=options.useTAndP, outputDir =outputDir, selType='inv' )
                results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, ndKeysSample=dy_sample_nom, ndKeysSelection=selection_mc_nom, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, extraBkgHist=hists_extra['nom'], useTAndP=options.useTAndP, outputDir =outputDir, selType='nom' )
        else :
            template_hist = get_3d_mass_ratio_histograms( selection_nom, selection_inv, dy_sample_nom, mass_binning, useHist=None, useAbsEta=True, useTAndP=useTAndP )
            template_hist_bkg_nom = None
            template_hist_bkg_inv = None
            if useMCTemplateBackground :
                template_hist_bkg = get_3d_mass_ratio_histograms( selection_nom, selection_inv, 'FakeBackgroundSamples', mass_binning, useHist=None, useAbsEta=True, useTAndP=useTAndP )
                template_hist_bkg_nom = template_hist_bkg['nom']
                template_hist_bkg_inv = template_hist_bkg['inv']

            results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, mcTemplate=template_hist['nom'], mcTemplateBkg=template_hist_bkg_nom, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, useTAndP=useTAndP, outputDir =outputDir, selType='nom' )
            results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, mcTemplate=template_hist['inv'], mcTemplateBkg=template_hist_bkg_inv, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, useTAndP=useTAndP, outputDir =outputDir, selType='inv' )
    else :
        results_nom = fit_pt_eta_bins( hists['nom'], pt_eta_bins, useLandauSig=useLandauSig, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, useTAndP=useTAndP, outputDir =outputDir, selType='nom' )
        results_inv = fit_pt_eta_bins( hists['inv'], pt_eta_bins, useLandauSig=useLandauSig, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, useTAndP=useTAndP, outputDir =outputDir, selType='inv' )

    write_output( results_nom, results_inv, subl_pt_bins, coarse_eta_bins, useTAndP=useTAndP, outputDir=outputDir )

def write_output( results_nom, results_inv, subl_pt_bins={}, coarse_eta_bins={}, useTAndP=False, outputDir=None ) :

    #---------------------------------------
    # Combine into the coarser subleding bins
    #---------------------------------------
    sum_base = {'nsig' : 0, 'nsig_peak' : 0, 'extra_bkg' : 0 }
    summed_results_nom = { }
    summed_results_inv = { }
    for bin, sub_bins in subl_pt_bins.iteritems() :

        for ptmin, ptmax in sub_bins :

            for res_bin, res_nom in results_nom.iteritems() :

                res_inv = results_inv[res_bin]

                res_ptmin = res_bin[0]
                res_ptmax = res_bin[1]

                if str(res_ptmin) == str(ptmin) and str(res_ptmax) == str(ptmax)  :

                    print 'Add results for subl bin %s-%s from lead bin %s-%s ' %( bin[0], bin[1], res_ptmin, res_ptmax)

                    res_etamin = res_bin[2]
                    res_etamax = res_bin[3]

                    summed_bin = ( str(bin[0]), str(bin[1]), res_etamin, res_etamax )
                    print 'summed_bin = ', summed_bin

                    if summed_bin not in summed_results_nom :
                        summed_results_nom[summed_bin] = dict( sum_base )
                        summed_results_inv[summed_bin] = dict( sum_base )


                    summed_results_nom[summed_bin]['nsig'] = summed_results_nom[summed_bin]['nsig'] + res_nom['nsig']
                    summed_results_inv[summed_bin]['nsig'] = summed_results_inv[summed_bin]['nsig'] + res_inv['nsig']

                    summed_results_nom[summed_bin]['nsig_peak'] = summed_results_nom[summed_bin]['nsig_peak'] + res_nom['nsig_peak']
                    summed_results_inv[summed_bin]['nsig_peak'] = summed_results_inv[summed_bin]['nsig_peak'] + res_inv['nsig_peak']

                    if 'extra_bkg' in res_nom :
                        summed_results_nom[summed_bin]['extra_bkg'] = summed_results_nom[summed_bin]['extra_bkg'] + res_nom['extra_bkg']
                        summed_results_inv[summed_bin]['extra_bkg'] = summed_results_inv[summed_bin]['extra_bkg'] + res_inv['extra_bkg']

    print 'sumemd results' 
    print summed_results_nom
    results_nom.update( summed_results_nom )
    results_inv.update( summed_results_inv )
            
    #---------------------------------------
    # Combine into the coarser eta bins
    #---------------------------------------
    print results_nom.keys()

    summed_results_nom = { }
    summed_results_inv = { }
    for bin, sub_bins in coarse_eta_bins.iteritems() :

        for etamin, etamax in sub_bins :

            for res_bin, res_nom in results_nom.iteritems() :

                res_inv = results_inv[res_bin]

                res_etamin = res_bin[2]
                res_etamax = res_bin[3]

                if str(res_etamin) == str(etamin) and str(res_etamax) == str(etamax)  :

                    print 'Add results for pt %s-%s, subl bin %s-%s from lead bin %s-%s ' %( res_bin[0], res_bin[1], bin[0], bin[1], res_etamin, res_etamax)

                    res_ptmin = res_bin[0]
                    res_ptmax = res_bin[1]

                    summed_bin = ( str(res_ptmin), str(res_ptmax), bin[0], bin[1] )

                    if summed_bin not in summed_results_nom :
                        summed_results_nom[summed_bin] = dict( sum_base )
                        summed_results_inv[summed_bin] = dict( sum_base )


                    summed_results_nom[summed_bin]['nsig'] = summed_results_nom[summed_bin]['nsig'] + res_nom['nsig']
                    summed_results_inv[summed_bin]['nsig'] = summed_results_inv[summed_bin]['nsig'] + res_inv['nsig']

                    summed_results_nom[summed_bin]['nsig_peak'] = summed_results_nom[summed_bin]['nsig_peak'] + res_nom['nsig_peak']
                    summed_results_inv[summed_bin]['nsig_peak'] = summed_results_inv[summed_bin]['nsig_peak'] + res_inv['nsig_peak']

                    if 'extra_bkg' in res_nom :
                        summed_results_nom[summed_bin]['extra_bkg'] = summed_results_nom[summed_bin]['extra_bkg'] + res_nom['extra_bkg']
                        summed_results_inv[summed_bin]['extra_bkg'] = summed_results_inv[summed_bin]['extra_bkg'] + res_inv['extra_bkg']

    print 'summed results nom'
    print summed_results_nom.keys()

    results_nom.update( summed_results_nom )
    results_inv.update( summed_results_inv )
    
    print 'results_nom'
    print results_nom.keys()


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

        ff = res_nom['nsig']/res_inv['nsig']

        print ' pt %s - %s, eta %s - %s nom = %s, inv = %s, ratio = %s ' %( ptmin, ptmax, etamin, etamax, res_nom['nsig'], res_inv['nsig'], ff )

        results_all['fake_ratio'][bin] = ff

        results_all['fake_ratio_peak'][bin] = (res_nom['nsig']*res_nom['nsig_peak']/(res_inv['nsig']*res_inv['nsig_peak']))

        if 'extra_bkg' in res_nom :
            results_all['fake_ratio_subtract'][bin] = (res_nom['nsig']-res_nom['extra_bkg'])/(res_inv['nsig']-res_inv['extra_bkg'])


    if outputDir is not None :
        fname = '%s/results.pickle' %outputDir
        file_res = open( fname , 'w' )
        pickle.dump( results_all, file_res )
        file_res.close()
        print 'Wrote file ', fname

    
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

    target_samp_nom = sampManNom.get_samples(name='DYJetsToLL')
    target_samp_inv = sampManInv.get_samples(name='DYJetsToLL')

    #hist_nom = clone_sample_and_draw( target_samp[0], 'm_trigelph1', selection_0fake, mass_binning )

    
    selection_inv = ' el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_elMinDR[0]>0.2 && ph_passMedium[0] && ph_hasPixSeed[0]==1 '
    selection_nom = ' el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_elMinDR[0]>0.2 && ph_passMedium[0] && ph_hasPixSeed[0]==0 '

    #selection_inv_weight = ' + '.join( ['( ph_pt[0] > %s && ph_pt[0] < %s ) * ( %f ) '%( min, max, ff.n) for (min, max), ff in ffresults_trig['pt'].iteritems()] )
    #selection_inv = '( %f ) * ( %s )' %( ffresults_trig['norm_pt'].values()[0].n, selection_inv )

    hist_inv = clone_sample_and_draw( target_samp_inv[0], 'm_trigelph1', selection_inv, mass_binning )
    hist_nom = clone_sample_and_draw( target_samp_nom[0], 'm_trigelph1', selection_nom, mass_binning )

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

    target_samp_nom = sampManNom.get_samples(name='ZjetsZgamma')
    target_samp_inv = sampManInv.get_samples(name='ZjetsZgamma')

    selection_inv = ' el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==1 && m_trigelph1 > 86 && m_trigelph1 < 106'
    selection_nom = ' el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0]==0 && m_trigelph1 > 86 && m_trigelph1 < 106'
    
    hist_inv_pt = clone_sample_and_draw( target_samp_inv[0], 'ph_pt[0]', selection_inv, pt_bins )
    hist_nom_pt = clone_sample_and_draw( target_samp_nom[0], 'ph_pt[0]', selection_nom, pt_bins )

    hist_nom_pt.Divide(hist_inv_pt)

    hist_inv_eta = clone_sample_and_draw( target_samp_inv[0], 'ph_sceta[0]', selection_inv, eta_bins )
    hist_nom_eta = clone_sample_and_draw( target_samp_nom[0], 'ph_sceta[0]', selection_nom, eta_bins )

    hist_nom_eta.Divide(hist_inv_eta)


    fake_factors = {}
    for idx, min in enumerate(pt_bins[:-1] ) :
        max = pt_bins[idx+1]

        fake_factors[(min, max)] = hist_nom_pt.GetBinContent( idx+1 )

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
    ee_eta_lead = clone_sample_and_draw( target_samp[0], 'm_phph:ph_sceta[0]', selection_2fake_tagsubl, (500, -2.5, 2.5, mass_binning[0], mass_binning[1], mass_binning[2]) )
    ee_eta_subl = clone_sample_and_draw( target_samp[0], 'm_phph:ph_sceta[1]', selection_2fake_taglead, (500, -2.5, 2.5, mass_binning[0], mass_binning[1], mass_binning[2]) )

    eg_eta_lead = clone_sample_and_draw( target_samp[0], 'm_phph:ph_sceta[0]', selection_1fake_tagsubl, (500, -2.5, 2.5, mass_binning[0], mass_binning[1], mass_binning[2]))
    eg_eta_subl = clone_sample_and_draw( target_samp[0], 'm_phph:ph_sceta[1]', selection_1fake_taglead, (500, -2.5, 2.5, mass_binning[0], mass_binning[1], mass_binning[2]))

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

    target_samp_inv = sampManInv.get_samples(name=sample)
    target_samp_nom = sampManNom.get_samples(name=sample)

    if useAbsEta :
        if useTAndP :
            var_lead = 'm_tagprobe:probe_pt:fabs(probe_eta)'
        else :
            var_lead = 'm_trigelph1:ph_pt[0]:fabs(ph_sceta[0])' #z:y:x
        eta_nbin = 250
        eta_min = 0
        eta_max = 2.5
    else :
        if useTAndP :
            var_lead = 'm_tagprobe:probe_pt:probe_eta'
        else :
            var_lead = 'm_trigelph1:ph_pt[0]:ph_sceta[0]' #z:y:x
        eta_nbin = 500
        eta_min = -2.5
        eta_max = 2.5

    # pt hists
    hist_nom = clone_sample_and_draw( target_samp_nom[0], var_lead, selection_nom, (eta_nbin, eta_min, eta_max, 40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]), sampMan=sampManNom )
    hist_inv = clone_sample_and_draw( target_samp_inv[0], var_lead, selection_inv, (eta_nbin, eta_min, eta_max, 40, 0, 200, mass_binning[0], mass_binning[1], mass_binning[2]), sampMan=sampManInv  )

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
        var_lead = 'm_phph:ph_pt[0]:fabs(ph_sceta[0])' #z:y:x
        var_subl = 'm_phph:ph_pt[1]:fabs(ph_sceta[1])' #z:y:x
        eta_nbin = 250
        eta_min = 0
        eta_max = 2.5
    else :
        var_lead = 'm_phph:ph_pt[0]:ph_sceta[0]' #z:y:x
        var_subl = 'm_phph:ph_pt[1]:ph_sceta[1]' #z:y:x
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


def fit_pt_eta_bins( hist, pt_eta_bins, mcTemplate=None, mcTemplateBkg=None, useLandauSig=False, ndKeysSample=None, ndKeysSampleBkg=None, ndKeysSelection=None, ndKeysSelectionBkg=None, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCmsShapeBkg=False, extraBkgHist=None, useTAndP=False, outputDir=None, selType='' ) :

    sampMan = None
    if   selType == 'nom' :
        sampMan = sampManNom
    elif selType == 'inv' :
        sampMan = sampManInv
    else :
        print 'Expect to get nom or inv'


    results_pt_eta = {}
    last_pt = max( [x[1] for x in pt_eta_bins.keys() ] )
    nextlast_pt = max( [x[0] for x in pt_eta_bins.keys() ] )
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

            print 'type = %s, ptmin = %d, ptmax = %d, etamin = %f, etamax = %f ' %(selType, ptmin, ptmax, etamin, etamax )
            print 'BIN : ptmin = %d, ptmax = %d, etamin = %d, etamax = %d ' %(pt_bin_min, pt_bin_max, eta_bin_min, eta_bin_max )

            if ptmax == last_pt :
                fitname = 'fit_%s_eta_%.2f-%.2f_pt_%d-max' %(selType, etamin, etamax, ptmin)
            else :
                fitname = 'fit_%s_eta_%.2f-%.2f_pt_%d-%d' %(selType, etamin, etamax, ptmin, ptmax)

            hist_proj = hist.ProjectionZ(fitname, eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )
            ROOT.SetOwnership( hist_proj, False )

            # don't rebin for high pt
            #if ptmax == last_pt and ptmin == nextlast_pt:
            #    hist_proj.Rebin(2)

            output_name = None
            if outputDir is not None :
                output_name = outputDir + '/' + hist_proj.GetName()

            if mcTemplate is not None :
                template_proj = mcTemplate.ProjectionZ(fitname+'_fit', eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )
                ROOT.SetOwnership( template_proj, False )
                if mcTemplateBkg is not None :
                    template_proj_bkg = mcTemplateBkg.ProjectionZ(fitname+'_fitbkg', eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )
                    results = fit_hist_mc_template( hist_proj, template_proj, mcTemplateBkg=template_proj_bkg, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useTAndP=useTAndP, label=hist_proj.GetName(), outputName=output_name, sampMan=sampMan )
                else :
                    results = fit_hist_mc_template( hist_proj, template_proj, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useTAndP=useTAndP, label=hist_proj.GetName(), outputName=output_name, sampMan=sampMan )

            elif ndKeysSample is not None :

                if selType == 'nom' :
                    #file_path = '%s/%s_filt_pt_%d-%d_eta_%.2f-%.2f/Job_0000/tree.root' %(sampMan.base_path, ndKeysSample, ptmin, ptmax, etamin, etamax  )
                    file_path = '%s/%s_filt_pt_%d-%d_eta_%.2f-%.2f/Job_0000/tree.root' %(sampMan.base_path, ndKeysSample, ptmin, ptmax, etamin, etamax  )
                if selType == 'inv' :
                    file_path = '%s/%s_filt_pt_%d-%d_eta_%.2f-%.2f/Job_0000/tree.root' %(sampMan.base_path, ndKeysSample, ptmin, ptmax, etamin, etamax  )
                open_file = ROOT.TFile.Open( file_path, 'READ') 

                new_tree = open_file.Get( 'ggNtuplizer/EventTree' )
                print 'Tree has entries ', new_tree.GetEntries()

                #if useTAndP :
                #    #pt_eta_selection = ndKeysSelection + ' && fabs(probe_eta) > %f && fabs(probe_eta) < %f && probe_pt > %d && probe_pt < %d ' %( etamin, etamax, ptmin, ptmax )
                #    pt_eta_selection = ndKeysSelection %{'etamin' : etamin, 'etamax' : etamax,'ptmin' : ptmin, 'ptmax' : ptmax }
                #    pt_eta_selection_bkg = '%s ( %s ) ' %( ndKeysSelectionBkg, pt_eta_selection )
                #else :
                #    #pt_eta_selection = ndKeysSelection + ' && fabs(ph_sceta[0]) > %f && fabs(ph_sceta[0]) < %f && ph_pt[0] > %d && ph_pt[0] < %d ' %( etamin, etamax, ptmin, ptmax )
                #    pt_eta_selection = ndKeysSelection %{'etamin' : etamin, 'etamax' : etamax, 'ptmin' : ptmin, 'ptmax' : ptmax }
                #    pt_eta_selection_bkg = '%s ( %s ) ' %( ndKeysSelectionBkg, pt_eta_selection )

                #orig_path = '%s/%s/Job_0000/tree.root' %(sampMan.base_path, ndKeysSample )
                #orig_file = ROOT.TFile.Open( orig_path, 'READ' )
                #orig_tree = orig_file.Get('ggNtuplizer/EventTree')
                #ROOT.SetOwnership( orig_tree, False )
                #orig_tree.SetBranchStatus('*', 1)
                #tmpfile = ROOT.TFile.Open( '/tmp/jkunkle/tmp.root', 'RECREATE' )

                ## start with a filter factor of 5
                #filter_factor = 5
                #new_tree = orig_tree.CopyTree( pt_eta_selection + ' && Entry$%' + '%d == 0 ' %filter_factor )
                #new_tree.SetName( 'new_tree' )
                #ROOT.SetOwnership( new_tree, False )
                #nentries = new_tree.GetEntries()

                ## determine a new scaling factor
                ## if it is too small or too large
                ## remake the sample with a new scaling factor
                #new_factor = nentries/10000.
                #print 'Factor with scaling of 5 = %f' %new_factor
                #if new_factor < 1 or new_factor > 2 :
                #    new_factor *= filter_factor
                #    new_factor = math.floor( new_factor )
                #    if new_factor == 0 :
                #        new_factor = 1

                #    print 'New factor = ', new_factor
                #    new_tree = orig_tree.CopyTree( pt_eta_selection+ ' && Entry$%' + '%d == 0 ' %new_factor )

                #ROOT.SetOwnership( new_tree, False )
                #nentries = new_tree.GetEntries()
                #if nentries < 5 :
                #    print 'WARNING : MC Sample has too few entries'
                #    continue

                ##if nentries > 10000 :
                ##    filter_factor = int(math.floor(nentries/10000.))
                ##    print 'Tree has too many entries will copy with fewer'
                ##    print filter_factor
                ##    new_tree = orig_tree.CopyTree( pt_eta_selection + ' && Entry$%' + '%d == 0 ' %filter_factor )

                if ndKeysSampleBkg is not None :
                    orig_tree_bkg = sampMan.get_samples( name=ndKeysSampleBkg )[0].chain
                    orig_tree_bkg.SetBranchStatus('*', 1)
                    tmpfile_bkg = ROOT.TFile.Open( '/tmp/jkunkle/tmpbkg.root', 'RECREATE' )

                    new_tree_bkg = orig_tree_bkg.CopyTree( pt_eta_selection)
                    nentries = new_tree_bkg.GetEntries()
                    if nentries > 10000 :
                        filter_factor = int(math.floor(nentries/10000.))
                        print 'Background Tree has too many entries will copy with fewer'
                        print filter_factor
                        new_tree_bkg = orig_tree_bkg.CopyTree( pt_eta_selection + ' && Entry$%' + '%d == 0 ' %filter_factor )

                    print 'Tree has %d entries ' %new_tree.GetEntries()
                    print 'Background Tree has %d entries ' %new_tree_bkg.GetEntries()

                if useTAndP :
                    m_tagprobe       = ROOT.RooRealVar( 'm_tagprobe', 'm_tagprobe', 40, 200 )
                    probe_pt         = ROOT.RooRealVar( 'probe_pt', 'probe_pt', 0, 1000 )
                    probe_eta        = ROOT.RooRealVar( 'probe_eta', 'probe_eta', -5, 5)
                    probe_hasPixSeed = ROOT.RooRealVar( 'probe_hasPixSeed', 'probe_hasPixSeed', 0, 1)
                    probe_eleVeto    = ROOT.RooRealVar( 'probe_eleVeto', 'probe_eleVeto', 0, 1)
                    probe_isPhoton   = ROOT.RooRealVar( 'probe_isPhoton', 'probe_isPhoton', 0, 1)

                    data_set = ROOT.RooDataSet( 'dataset_%.2f_%.2f_%d_%d' %(etamin, etamax, ptmin, ptmax ), '', new_tree,ROOT.RooArgSet( m_tagprobe ))

                    data_set_bkg = None
                    if ndKeysSampleBkg is not None :
                        data_set_bkg = ROOT.RooDataSet( 'dataset_%.2f_%.2f_%d_%d' %(etamin, etamax, ptmin, ptmax ), ndKeysSampleBkg, new_tree_bkg,ROOT.RooArgSet( m_tagprobe ))

                    results = fit_hist_ndkeys( hist_proj, signal_dataset=data_set, varname='m_tagprobe', bkg_dataset=data_set_bkg, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, useTAndP=useTAndP, label=hist_proj.GetName(), outputName=output_name, sampMan=sampMan )
                    data_set.IsA().Destructor( data_set )
                else :

                    m_trigelph1      = ROOT.RooRealVar( 'm_trigelph1', 'm_trigelph1', 40, 200 )
                    ph_passMedium    = ROOT.RooRealVar( 'ph_passMedium[0]', 'ph_passMedium[0]', 0, 1 )
                    el_passtrig_n    = ROOT.RooRealVar( 'el_passtrig_n', 'el_passtrig_n', 0, 10 )
                    el_n             = ROOT.RooRealVar( 'el_n', 'el_n', 0, 10 )
                    ph_n             = ROOT.RooRealVar( 'ph_n', 'ph_n', 0, 10 )
                    ph_hasPixSeed    = ROOT.RooRealVar( 'ph_hasPixSeed[0]', 'ph_hasPixSeed[0]', 0, 10 )
                    ph_eleVeto       = ROOT.RooRealVar( 'ph_eleVeto[0]', 'ph_eleVeto[0]', 0, 10 )
                    ph_eta           = ROOT.RooRealVar( 'ph_sceta[0]', 'ph_sceta[0]', -5., 5. )
                    ph_pt            = ROOT.RooRealVar( 'ph_pt[0]', 'ph_pt[0]', 0, 1000. )
                    ph_truthMatch_ph = ROOT.RooRealVar( 'ph_truthMatch_ph[0]', 'ph_truthMatch_ph[0]', 0, 1. )

                    data_set = ROOT.RooDataSet( 'dataset_%.2f_%.2f_%d_%d' %(etamin, etamax, ptmin, ptmax ), '', new_tree,ROOT.RooArgSet( m_trigelph1))
                    ROOT.SetOwnership( data_set, False )


                    results = fit_hist_ndkeys( hist_proj, signal_dataset=data_set, varname='m_trigelph1', bkg_dataset=None, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useCmsShapeBkg=useCmsShapeBkg, useTAndP=useTAndP, label=hist_proj.GetName(), outputName=output_name, sampMan=sampMan )
                    data_set.IsA().Destructor( data_set )

                open_file.Close()
            else :
                results = fit_hist_nominal( hist_proj, useLandauSig=useLandauSig, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useTAndP=useTAndP, label=hist_proj.GetName(), outputName=output_name, sampMan=sampMan )

            if extraBkgHist is not None :
                histname = 'bkg_%s_eta_%.2f-%.2f_pt_%d-%d' %(selType, etamin, etamax, ptmin, ptmax) 
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

def fit_hist_nominal( data_hist, useLandauSig=False, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useTAndP=False, label=None, outputName=None, sampMan=None ) :

    sampMan.fit_objs = {}

    if label is None :
        label = data_hist.GetName()

    # independent var
    xmin = 40
    xmax = 200

    m_lepph1 = ROOT.RooRealVar( 'm_trigelph1', 'm_trigelph1', xmin, xmax )

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

    fit_defs = get_fit_defaults( data_hist.GetName(), useGaussSig=None, useLandauSig=useLandauSig, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useTAndP=useTAndP )
    chi2 = fit_model_to_data(m_lepph1, data_hist, fit_defs, sampMan, signal=signal, background=background, bkg_labels=['Bkg'])

    draw_fitted_results( sampMan.fit_objs['model'], sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], 'Bkg', m_lepph1, chi2, label, outputName=outputName )

    return store_results( m_lepph1, 'Bkg', sampMan )

def fit_hist_mc_template( data_hist, template_hist, mcTemplateBkg=None, usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useTAndP=False, label=None, selType='', outputName=None, sampMan=None ) :

    sampMan.fit_objs = {}

    if label is None :
        label = data_hist.GetName()

    xmin = 40
    xmax = 180

    signals = [template_hist]

    backgrounds= []

    if mcTemplateBkg :
        backgrounds.append( mcTemplateBkg )
    elif usePolyBkg :
        backgrounds.append( 'poly' )
    elif useExpBkg :
        backgrounds.append( 'exp' )
    elif useChebyBkg :
        backgrounds.append( 'cheby' )
    elif useBernsteinBkg :
        backgrounds.append( 'bernstein' )
    else :
        backgrounds.append( 'cmsshape' )

    bkg_labels = ['Bkg']


    # independent var
    m_lepph1 = ROOT.RooRealVar( 'm_trigelph1', 'm_trigelph1', xmin,xmax)


    fit_defs = get_fit_defaults( data_hist.GetName(), useGaussSig=(template_hist is not None), useLandauSig=False, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useTAndP=useTAndP )
    chi2 = fit_model_to_data(m_lepph1, data_hist, fit_defs, sampMan, signal=signals, background=backgrounds, bkg_labels=bkg_labels)

    draw_fitted_results( sampMan.fit_objs['model'], sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], bkg_labels, m_lepph1, chi2, label, outputName=outputName )

    return store_results( m_lepph1, backgrounds=bkg_labels, sampMan=sampMan )

def fit_hist_ndkeys( data_hist, signal_dataset=None, bkg_dataset=None, varname='m_lepph1', usePolyBkg=False, useExpBkg=False, useChebyBkg=False, useBernsteinBkg=False, useCmsShapeBkg=False, useTAndP=False, label=None, outputName=None, sampMan=None ) :

    sampMan.fit_objs = {}
    bkg_labels = []

    if label is None :
        label = data_hist.GetName()

    xmin = 40
    xmax = 200

    # independent var
    m_lepph1 = ROOT.RooRealVar( varname, varname, xmin,xmax)

    signals = [signal_dataset]
    print 'bkg_dataset = ', bkg_dataset
    if bkg_dataset is not None :
        backgrounds = [bkg_dataset]
        bkg_labels.append( bkg_dataset.GetTitle() )
    else :
        backgrounds= []

    if usePolyBkg :
        backgrounds.append( 'poly' )
        bkg_labels.append('Bkg')
    if useExpBkg :
        backgrounds.append( 'exp' )
        bkg_labels.append('Bkg')
    if useChebyBkg :
        backgrounds.append( 'cheby' )
        bkg_labels.append('Bkg')
    if useBernsteinBkg :
        backgrounds.append( 'bernstein' )
        bkg_labels.append('Bkg')
    if useCmsShapeBkg:
        backgrounds.append( 'cmsshape' )
        bkg_labels.append('Bkg')

    print backgrounds

    use_mc_bkg = (bkg_dataset is not None)

    fit_defs = get_fit_defaults( data_hist.GetName(), useGaussSig=(signal_dataset is not None), useLandauSig=False, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg, useMCBkg=use_mc_bkg, useTAndP=useTAndP )
    #chi2 = fit_model_to_data( m_lepph1, data_hist, fit_defs, sampMan, MCSig=template_dataset, doNDKeys=True, usePolyBkg=usePolyBkg, useExpBkg=useExpBkg, useChebyBkg=useChebyBkg, useBernsteinBkg=useBernsteinBkg)
    chi2 = fit_model_to_data( m_lepph1, data_hist, fit_defs, sampMan, signal=signals, background=backgrounds, bkg_labels=bkg_labels)

    print sampMan.fit_objs.keys()

    draw_fitted_results( sampMan.fit_objs['model'], sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], bkg_labels, m_lepph1, chi2, label, outputName=outputName )

    return store_results( m_lepph1, backgrounds=bkg_labels, sampMan=sampMan )

def store_results( var, backgrounds=['bkg_model'], sampMan=None ) :

    if not isinstance( backgrounds, list) :
        backgrounds = [backgrounds]

    results = {}

    xmin = var.getMin()
    xmax = var.getMax()

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


def clone_sample_and_draw( samp, var, sel, binning, sampMan=None ) :

    if sampMan is None :
        sampMan = sampManInv

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
