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
p.add_argument('--zgg',          default=False,  action='store_true' ,        dest='zgg',             help='make zgg plots')

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
    global samplesZgg
    global samplesWggComb
    global samplesWggBkgSub

    sampleConfWgg = 'Modules/WggFinal.py'
    if options.zgg :
        sampleConfWgg = 'Modules/ZggFinal.py'
    sampleConfWggBkgSub = 'Modules/WggFinalBkgSub.py'

    samplesWgg       = SampleManager(options.baseDir, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)
    #samplesWggComb   = SampleManager(options.baseDirComb, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)
    #samplesWggBkgSub = SampleManager(options.baseDirComb, filename='hist.root', xsFile='cross_sections/wgamgam.py', lumi=19400, readHists=True)

    samplesWgg        .ReadSamples( sampleConfWgg )
    #samplesWggComb    .ReadSamples( sampleConfWgg )
    #samplesWggBkgSub  .ReadSamples( sampleConfWggBkgSub )

    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)

    dumpStack=True
    samplesWgg.activate_sample( 'AllBkg')
    samplesWgg.activate_sample( 'ZggNoSyst')
    samplesWgg.activate_sample( 'AllBkgPlusSig')

    if options.zgg : 
        MakeZggPlots( options.outputDir, suffix='', ylabel='Events/bin', label_style='fancyprelim', dumpStack=dumpStack )
    if options.electron :
        MakeElectronPlots(options.outputDir, suffix='', ylabel='Events / bin',label_style='fancy', dumpStack=dumpStack  )
        MakeElectronPlots(options.outputDir, suffix='', name_suffix='_prelim', ylabel='Events / bin',label_style='fancyprelim', dumpStack=dumpStack  )
        #MakeElectronPlots(options.outputDir, suffix='_perGeV', name_suffix='_perGeV', ylabel = 'Events / 5 GeV', logy=1  )
    if options.muon :
        MakeMuonPlots(options.outputDir, suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack  )
        MakeMuonPlots(options.outputDir, suffix='', name_suffix='_prelim', ylabel='Events / bin', label_style='fancyprelim', dumpStack=dumpStack  )
        #MakeMuonPlots(options.outputDir, suffix='_perGeV', ylabel = 'Events / 5 GeV',logy=1  )
    if options.combined :
        MakeCombinedPlots( options.outputDir, dumpStack=dumpStack )

    dumpStack=False
    samplesWgg.deactivate_sample( 'AllBkg')
    samplesWgg.deactivate_sample( 'ZggNoSyst')

    if options.zgg : 
        MakeZggPlots( options.outputDir, suffix='', ylabel='Events/bin', label_style='fancyprelim', dumpStack=dumpStack )
    if options.electron :
        MakeElectronPlots(options.outputDir, suffix='', ylabel='Events / bin',label_style='fancy', dumpStack=dumpStack  )
        MakeElectronPlots(options.outputDir, suffix='', name_suffix='_prelim', ylabel='Events / bin',label_style='fancyprelim', dumpStack=dumpStack  )
        #MakeElectronPlots(options.outputDir, suffix='_perGeV', name_suffix='_perGeV', ylabel = 'Events / 5 GeV', logy=1  )
    if options.muon :
        MakeMuonPlots(options.outputDir, suffix='', ylabel='Events / bin', label_style='fancy', dumpStack=dumpStack  )
        MakeMuonPlots(options.outputDir, suffix='', name_suffix='_prelim', ylabel='Events / bin', label_style='fancyprelim', dumpStack=dumpStack  )
        #MakeMuonPlots(options.outputDir, suffix='_perGeV', ylabel = 'Events / 5 GeV',logy=1  )
    if options.combined :
        MakeCombinedPlots( options.outputDir, dumpStack=dumpStack )

    print '^.^ FINSHED ^.^'

#---------------------------------------
def MakeMuonPlots( outputDir, suffix='', name_suffix='', ylabel='Events / bin',label_style='fancy', logy=0, dumpStack=True ) :

    save = ( outputDir is not None )
    xlabel = 'p_{T}^{lead #gamma} [GeV]'

    #ymax = 200
    ymax = 60

    samplesWgg.DrawHist( 'pt_leadph12_muhighmt%s' %suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Muon Channel', 'extra_label_loc' : (0.66, 0.62) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045}, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax )

    if save :
        name = 'pt_leadph12_muhighmt%s' %name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_muhighmt_EB-EB%s' %suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_muhighmt_EB-EB%s' %name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_muhighmt_EE-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_muhighmt_EE-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_muhighmt_EB-EE%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_muhighmt_EB-EE%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_mulowmt%s' %suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Muon Channel', 'extra_label_loc' : (0.66, 0.62) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045}, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax-20 )

    if save :
        name = 'pt_leadph12_mulowmt%s' %name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_mulowmt_EB-EB%s' %suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_mulowmt_EB-EB%s' %name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_mulowmt_EE-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_mulowmt_EE-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_mulowmt_EB-EE%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_mulowmt_EB-EE%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

#---------------------------------------
def MakeElectronPlots( outputDir, suffix='', name_suffix='', ylabel='Events / bin', label_style='fancy', logy=0, dumpStack=True  ) :

    save = ( outputDir is not None )

    xlabel = 'p_{T}^{lead #gamma} [GeV]'

    #ymax = 150
    ymax = 50

    samplesWgg.DrawHist( 'pt_leadph12_elfullhighmt%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.66, 0.55) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045, }, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax )

    if save :
        name = 'pt_leadph12_elfullhighmt%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWgg.DrawHist( 'pt_leadph12_elfullhighmt_EB-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elfullhighmt_EB-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elfullhighmt_EE-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elfullhighmt_EE-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elfullhighmt_EB-EE%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elfullhighmt_EB-EE%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elfulllowmt%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.66, 0.55) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045}, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax-10 )

    if save :
        name = 'pt_leadph12_elfulllowmt%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWgg.DrawHist( 'pt_leadph12_elfulllowmt_EB-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elfulllowmt_EB-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elfulllowmt_EE-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elfulllowmt_EE-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elfulllowmt_EB-EE%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elfulllowmt_EB-EE%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_ellooselowmt%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.66, 0.55) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045}, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax )

    if save :
        name = 'pt_leadph12_ellooselowmt%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWgg.DrawHist( 'pt_leadph12_ellooselowmt_EB-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_ellooselowmt_EB-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_ellooselowmt_EE-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_ellooselowmt_EE-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_ellooselowmt_EB-EE%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_ellooselowmt_EB-EE%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elzcrhighmt%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.66, 0.55) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07, 'legendTranslateX' : 0.045}, doratio=options.doRatio, logy=logy, ymin=0, ymax=ymax )

    if save :
        name = 'pt_leadph12_elzcrhighmt%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWgg.DrawHist( 'pt_leadph12_elzcrhighmt_EB-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elzcrhighmt_EB-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elzcrhighmt_EE-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elzcrhighmt_EE-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elzcrhighmt_EB-EE%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.44) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.3}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elzcrhighmt_EB-EE%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


#---------------------------------------
def MakeZggPlots( outputDir, suffix='', name_suffix='', ylabel='Events / bin',label_style='fancy', logy=0, dumpStack=True  ) :

    save = ( outputDir is not None )
    xlabel = 'p_{T}^{lead #gamma} [GeV]'

    samplesWgg.DrawHist( 'pt_leadph12_muZgg%s' %suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Muon Channel', 'extra_label_loc' : (0.61, 0.58) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07}, doratio=options.doRatio, logy=logy, ymin=0, ymax=80 )

    if save :
        name = 'pt_leadph12_muZgg%s' %name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_muZgg_EB-EB%s' %suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_muZgg_EB-EB%s' %name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_muZgg_EE-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_muZgg_EE-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_muZgg_EB-EE%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Muon Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_muZgg_EB-EE%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elZgg%s' %suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : 'Electron Channel', 'extra_label_loc' : (0.61, 0.58) }, legend_config={'legendWiden' : 1.2, 'entryWidth' : 0.07}, doratio=options.doRatio, logy=logy, ymin=0, ymax=80 )

    if save :
        name = 'pt_leadph12_elZgg%s' %name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elZgg_EB-EB%s' %suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elZgg_EB-EB%s' %name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elZgg_EE-EB%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elZgg_EE-EB%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWgg.DrawHist( 'pt_leadph12_elZgg_EB-EE%s'%suffix, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : label_style, 'extra_label' : '#splitline{Electron Channel}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.52) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio, logy=logy )

    if save :
        name = 'pt_leadph12_elZgg_EB-EE%s'%name_suffix
        samplesWgg.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWgg.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWgg.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

#---------------------------------------
def MakeCombinedPlots( outputDir, dumpStack=True  ) :

    save = ( outputDir is not None )

    samplesWggComb.DrawHist( 'pt_leadph12_lgg', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelim', 'extra_label' : 'Combined', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_lgg'
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')


    samplesWggComb.DrawHist( 'pt_leadph12_lgg_EB-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelim', 'extra_label' : '#splitline{Combined}{Barrel-Barrel}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_lgg_EB-EB'
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWggComb.DrawHist( 'pt_leadph12_lgg_EE-EB', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelim', 'extra_label' : '#splitline{Combined}{Endcap-Barrel}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_lgg_EE-EB'
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWggComb.DrawHist( 'pt_leadph12_lgg_EB-EE', xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Events / bin', label_config={'labelStyle' : 'fancyprelim', 'extra_label' : '#splitline{Combined}{Barrel-Endcap}', 'extra_label_loc' : (0.61, 0.53) }, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=options.doRatio )

    if save :
        name = 'pt_leadph12_lgg_EB-EE'
        samplesWggComb.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
        if dumpStack : 
            samplesWggComb.DumpStack( outputDir, name, doRatio=options.doRatio, details=True )
    else :
        samplesWggComb.DumpStack(doRatio=options.doRatio, details=True )
        raw_input('continue')

    samplesWggBkgSub.DrawHist( 'pt_leadph12_lgg', subtract_bkg=True, xlabel='p_{T}^{lead #gamma} [GeV]',ylabel= 'Background Subtracted Events / bin', label_config={'labelStyle' : 'fancyprelim'}, legend_config={'legendWiden' : 1.2, 'legendCompress' : 1.5}, doratio=False, ymin=-50, ymax=200 )

    if save :
        name = 'pt_leadph12_lgg_bkgSub'
        samplesWggBkgSub.SaveStack( '%s%s' %(name,options.savePostfix), outputDir, 'base' )
    else :
        raw_input('continue')



main()
