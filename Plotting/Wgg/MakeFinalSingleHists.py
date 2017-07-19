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
p.add_argument('--suffix',     default='',   dest='suffix',         help='Suffix for plot names')
p.add_argument('--doRatio',     default=False,action='store_true',   dest='doRatio',         help='do ratio')

p.add_argument('--wcr',  default=False,action='store_true',   dest='wcr',         help='make W CR plots')
p.add_argument('--zcr',  default=False,action='store_true',   dest='zcr',         help='make W CR plots')
p.add_argument('--evalid',  default=False,action='store_true',   dest='evalid',         help='make ele fake validation plots')
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

samplesWg = None

def main() :

    global samplesWg

    sampleConfWg = 'Modules/WgFinal.py'

    samplesWg       = SampleManager(options.baseDir, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)

    samplesWg        .ReadSamples( sampleConfWg )

    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)

    if options.wcr :
        MakeWCRPlots(options.outputDir, suffix=options.suffix)
    if options.zcr :
        MakeZCRPlots(options.outputDir, suffix=options.suffix)
    if options.evalid: 
        MakeEleValidationPlots(  options.outputDir, suffix=options.suffix) 

    print '^.^ FINSHED ^.^'
    os._exit

#---------------------------------------
def MakeWCRPlots( outputDir, suffix='', ylabel='Events / bin', logy=0 ) :

    save = ( outputDir is not None )

    samplesWg.DrawHist( 'pt_leadph12_muw_EB', xlabel='p_{T}^{#gamma} [GeV]',ylabel= ylabel, label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Barrel Photon}', 'extra_label_loc' : (0.61, 0.54) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=False )

    if save :
        name = 'pt_leadph12_muw_EB%s' %suffix
        samplesWg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWg.DrawHist( 'pt_leadph12_muw_EE', xlabel='p_{T}^{#gamma} [GeV]',ylabel= ylabel, label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Endcap Photon}', 'extra_label_loc' : (0.61, 0.54) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=False )

    if save :
        name = 'pt_leadph12_muw_EE%s' %suffix
        samplesWg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


#---------------------------------------
def MakeZCRPlots( outputDir, suffix='', ylabel='Events / bin', logy=0 ) :

    save = ( outputDir is not None )

    samplesWg.DrawHist( 'pt_leadph12_mu_EB', xlabel='p_{T}^{#gamma} [GeV]',ylabel= ylabel, label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Barrel Photon}', 'extra_label_loc' : (0.61, 0.54) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=False )

    if save :
        name = 'pt_leadph12_mu_EB%s' %suffix
        samplesWg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWg.DrawHist( 'pt_leadph12_mu_EE', xlabel='p_{T}^{#gamma} [GeV]',ylabel= ylabel, label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Endcap Photon}', 'extra_label_loc' : (0.61, 0.54) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=False )

    if save :
        name = 'pt_leadph12_mu_EE%s' %suffix
        samplesWg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

def MakeEleValidationPlots(  outputDir, suffix='', ylabel='Events / bin', logy=0 ) :

    save = ( outputDir is not None )

    samplesWg.DrawHist( 'pt_leadph12_elwzcr_EB', xlabel='p_{T}^{#gamma} [GeV]',ylabel= ylabel, label_config={'labelStyle' : 'fancynostats', 'extra_label' : 'Barrel Photons', 'extra_label_loc' : (0.61, 0.48) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=True, rmin = 0.68, rmax=1.32, logy=False )

    if save :
        name = 'pt_leadph12_elwzcr_EB%s' %suffix
        samplesWg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWg.DrawHist( 'pt_leadph12_elwzcr_EE', xlabel='p_{T}^{#gamma} [GeV]',ylabel= ylabel, label_config={'labelStyle' : 'fancynostats', 'extra_label' : 'Endcap Photons', 'extra_label_loc' : (0.61, 0.48) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=True, rmin = 0.68, rmax=1.32, logy=False )

    if save :
        name = 'pt_leadph12_elwzcr_EE%s' %suffix
        samplesWg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')



    samplesWg.DrawHist( 'pt_leadph12_elwzcr_EB', xlabel='p_{T}^{#gamma} [GeV]',ylabel= ylabel, label_config={'labelStyle' : 'fancyprelimnostats', 'extra_label' : 'Barrel Photons', 'extra_label_loc' : (0.61, 0.48) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=True, rmin = 0.68, rmax=1.32, logy=False )

    if save :
        name = 'pt_leadph12_elwzcr_EB%s_prelim' %suffix
        samplesWg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWg.DrawHist( 'pt_leadph12_elwzcr_EE', xlabel='p_{T}^{#gamma} [GeV]',ylabel= ylabel, label_config={'labelStyle' : 'fancyprelimnostats', 'extra_label' : 'Endcap Photons', 'extra_label_loc' : (0.61, 0.48) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=True, rmin = 0.68, rmax=1.32, logy=False )

    if save :
        name = 'pt_leadph12_elwzcr_EE%s_prelim' %suffix
        samplesWg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')



main()
