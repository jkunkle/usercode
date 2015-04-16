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
p.add_argument('--doRatio',     default=False,action='store_true',   dest='doRatio',         help='Make ratio plots')

p.add_argument('--muon',         default=False,  action='store_true' ,        dest='muon',         help='make muon channel plots')
p.add_argument('--electron',     default=False,  action='store_true' ,        dest='electron',         help='make electron channel plots')
p.add_argument('--combined',     default=False,  action='store_true' ,        dest='combined',         help='make combined plots')

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
    global samplesWggComb
    global samplesWggBkgSub

    sampleConfWgg = 'Modules/WggFinal.py'
    sampleConfWggBkgSub = 'Modules/WggFinalBkgSub.py'

    samplesWgg       = SampleManager(options.baseDir, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)
    samplesWggComb   = SampleManager(options.baseDirComb, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)
    samplesWggBkgSub = SampleManager(options.baseDirComb, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)

    samplesWgg        .ReadSamples( sampleConfWgg )
    samplesWggComb    .ReadSamples( sampleConfWgg )
    samplesWggBkgSub  .ReadSamples( sampleConfWggBkgSub )

    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)

    if options.electron :
        MakeElectronPlots(options.outputDir  )
    if options.muon :
        MakeMuonPlots(options.outputDir  )
    if options.combined :
        MakeCombinedPlots( options.outputDir )

#---------------------------------------
def MakeMuonPlots( outputDir ) :

    save = ( outputDir is not None )

    samplesWgg.DrawHist( 'pt_leadph12_mgg', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : 'Muon Channel', 'extra_label_loc' : (0.61, 0.6) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_mgg'
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_mgg_EB-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.60) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_mgg_EB-EB'
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_mgg_EE-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.60) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_mgg_EE-EB'
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_mgg_EB-EE', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Muon Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.60) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_mgg_EB-EE'
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

#---------------------------------------
def MakeElectronPlots( outputDir ) :

    save = ( outputDir is not None )

    samplesWgg.DrawHist( 'pt_leadph12_egg', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_egg'
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWgg.DrawHist( 'pt_leadph12_egg_EB-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_egg_EB-EB'
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_egg_EE-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_egg_EE-EB'
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_egg_EB-EE', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_egg_EB-EE'
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


#---------------------------------------
def MakeCombinedPlots( outputDir ) :

    save = ( outputDir is not None )

    samplesWggComb.DrawHist( 'pt_leadph12_lgg', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : 'Combined', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_lgg'
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWggComb.DrawHist( 'pt_leadph12_lgg_EB-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Combined}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_lgg_EB-EB'
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWggComb.DrawHist( 'pt_leadph12_lgg_EE-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Combined}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_lgg_EE-EB'
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWggComb.DrawHist( 'pt_leadph12_lgg_EB-EE', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancy', 'extra_label' : '#splitline{Combined}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_lgg_EB-EE'
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWggBkgSub.DrawHist( 'pt_leadph12_lgg', subtract_bkg=True, xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Background Subtracted Events / bin', label_config={'labelStyle' : 'fancy'}, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=False, ymin=-50, ymax=200 )

    if save :
        name = 'pt_leadph12_lgg_bkgSub'
        samplesWggBkgSub.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    else :
        raw_input('continue')



main()
