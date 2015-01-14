"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

                                                                                       
p.add_argument('--xsFile',     default=None,  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',         help='base directory for histograms')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')

p.add_argument('--muon',         default=False,  action='store_true' ,        dest='muon',         help='make muon channel plots')
p.add_argument('--electron',     default=False,  action='store_true' ,        dest='electron',         help='make electron channel plots')

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

    sampleConfWgg = 'Modules/WggFinal.py'

    samplesWgg     = SampleManager(options.baseDir, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)

    samplesWgg    .ReadSamples( sampleConfWgg )

    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)

    if options.electron :
        MakeElectronPlots(options.outputDir  )
    if options.muon :
        MakeMuonPlots(options.outputDir  )
#---------------------------------------
def MakeMuonPlots( outputDir ) :

    save = ( outputDir is not None )

    samplesWgg.DrawHist( 'pt_leadph12_mgg_EB-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.60, 0.45) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=1 )

    if save :
        name = 'pt_leadph12_mgg_EB-EB'
        samplesWgg.SaveStack( name, outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=True, details=True )
    else :
        samplesWgg.DumpStack(doRatio=True, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_mgg_EE-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.60, 0.45) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=1 )

    if save :
        name = 'pt_leadph12_mgg_EE-EB'
        samplesWgg.SaveStack( name, outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=True, details=True )
    else :
        samplesWgg.DumpStack(doRatio=True, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_mgg_EB-EE', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.60, 0.45) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=1 )

    if save :
        name = 'pt_leadph12_mgg_EB-EE'
        samplesWgg.SaveStack( name, outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=True, details=True )
    else :
        samplesWgg.DumpStack(doRatio=True, details=True )
        raw_input('continue')

#---------------------------------------
def MakeElectronPlots( outputDir ) :

    save = ( outputDir is not None )

    samplesWgg.DrawHist( 'pt_leadph12_egg_EB-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.60, 0.45) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=1 )

    if save :
        name = 'pt_leadph12_egg_EB-EB'
        samplesWgg.SaveStack( name, outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=True, details=True )
    else :
        samplesWgg.DumpStack(doRatio=True, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_egg_EE-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.60, 0.45) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=1 )

    if save :
        name = 'pt_leadph12_egg_EE-EB'
        samplesWgg.SaveStack( name, outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=True, details=True )
    else :
        samplesWgg.DumpStack(doRatio=True, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_egg_EB-EE', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.60, 0.45) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=1 )

    if save :
        name = 'pt_leadph12_egg_EB-EE'
        samplesWgg.SaveStack( name, outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=True, details=True )
    else :
        samplesWgg.DumpStack(doRatio=True, details=True )
        raw_input('continue')


main()
