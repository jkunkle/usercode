"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('--baseDir',      default=None,           dest='baseDir',         help='Path to base directory containing all ntuples')
p.add_argument('--baseDirModel',      default=None,           dest='baseDirModel', help='Path to base directory containing all ntuples for the model')
p.add_argument('--fileName',     default='ntuple.root',  dest='fileName',        help='( Default ntuple.root ) Name of files')
p.add_argument('--treeName',     default='events'     ,  dest='treeName',        help='( Default events ) Name tree in root file')
p.add_argument('--treeNameModel',     default='photons'     ,  dest='treeNameModel',help='( Default photons ) Name tree in root file')
p.add_argument('--samplesConf',  default=None,           dest='samplesConf',     help=('Use alternate sample configuration. '
                                                                                       'Must be a python file that implements the configuration '
                                                                                       'in the same manner as in the main() of this script.  If only '
                                                                                       'the file name is given it is assumed to be in the same directory '
                                                                                       'as this script, if a path is given, use that path' ) )

                                                                                       
p.add_argument('--xsFile',     default=None,  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--mcweight',     default=None,  type=float ,        dest='mcweight',         help='Weight to apply to MC samples')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--readHists',     default=False,action='store_true',   dest='readHists',         help='read histograms from root files instead of trees')

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

ROOT.gROOT.SetBatch(False)

samples = None

def main() :

    global samples

    if not options.baseDir.count('/eos/') and not os.path.isdir( options.baseDir ) :
        print 'baseDir not found!'
        return

    samples = SampleManager(options.baseDir, options.treeName, mcweight=options.mcweight, treeNameModel=options.treeNameModel, filename=options.fileName, base_path_model=options.baseDirModel, xsFile=options.xsFile, lumi=options.lumi, readHists=options.readHists, quiet=options.quiet)


    if options.samplesConf is not None :

        samples.ReadSamples( options.samplesConf )

        print 'Samples ready.\n'  

        print 'The draw syntax follows that of TTree.Draw.  Examples : '
        
        print 'samples.Draw(\'met_et\', \'EventWeight && passcut_ee==1\', \'(300, 0, 300)\'\n'

        print 'The first argument is a branch in the tree to draw'
        print 'The second argument is a set of cuts and/or weights to apply'
        print 'The third argument are the bin limits to use \n'

        print 'To see all available branches do ListBranches()'


#---------------------------------------
def ListBranches( key=None ) :
    """ List all available branches.  If key is provided only show those that match the key """

    global samples

    # grab list from 0th sample.  This may not work in some cases
    for br in samples.samples[0].chain.GetListOfBranches() :
        if key is None :
            print br.GetName()
        else :
            if br.GetName().count(key) :
                print br.GetName()


#---------------------------------------
def SaveStack( filename, canname=None, inDirs=''  ) :
    """ Save current plot to filename.  Must supply --outputDir  """

    global samples

    if options.outputDir is None :
        print 'No output directory provided.  Will not save.'
    else :

        outDir = options.outputDir + '/' + inDirs
        if not os.path.isdir( outDir ) :
            print 'Creating directory %s' %outDir
            os.makedirs(outDir)

        histnamepdf = outDir + '/' + filename+'.pdf'
        histnameeps = outDir + '/' + filename+'.eps'

        if len( samples.curr_canvases ) == 0 :
            print 'No canvases to save'
        elif len( samples.curr_canvases ) == 1  :
            samples.curr_canvases.values()[0].SaveAs(histnamepdf)
            samples.curr_canvases.values()[0].SaveAs(histnameeps)
        else :
            if canname is not None :
                if canname not in samples.curr_canvases :
                    print 'provided can name does not exist'
                else :
                    samples.curr_canvases[canname].SaveAs(histnamepdf)
                    samples.curr_canvases[canname].SaveAs(histnameeps)
                    return

            print 'Multiple canvases available.  Select which to save'
            keys = samples.curr_canvases.keys() 
            for idx, key in enumerate(keys) :
                print '%s (%d)' %(key, idx)
            selidx = int(raw_input('enter number 0 - %d' %( len(keys)-1 )))
            selkey = keys[selidx]
            samples.curr_canvases[selkey].SaveAs(histnamepdf)
            samples.curr_canvases[selkey].SaveAs(histnameeps)

#---------------------------------------
def DumpStack( txtname=None ) :

    global samples

    stack_entries = {}
    signal_entries = {}

    samp_list = samples.get_samples(name=samples.stack_order) + samples.get_samples(isData=True) + samples.get_samples(isSignal=True)

    for samp in samp_list :
        if samp.hist == None :
            continue
        err = ROOT.Double()
        integral = samp.hist.IntegralAndError( 1, samp.hist.GetNbinsX(), err )
        if samp.isSignal : 
            signal_entries[samp.name] = (integral, err*err)
        else :
            stack_entries[samp.name] = (integral, err*err )
    
    order = list(samples.stack_order)
    if 'Data' in stack_entries :
        order.insert(0, 'Data')

    bkg_sum = 0.0
    bkg_err = 0.9
    for name, vals in stack_entries.iteritems() :
        if name != 'Data' :
            bkg_sum += vals[0]
            bkg_err += vals[1]


    lines = []
    for nm in order :
        lines.append('%s : \t %f +- %f' %( nm, stack_entries[nm][0], math.sqrt(stack_entries[nm][1]) ))

    for sig in signal_entries :
        lines.append('%s : \t %f +- %f' %( sig, signal_entries[sig][0], math.sqrt(signal_entries[sig][1]) ))

    lines.append('MC Sum : \t %f +- %f' %(bkg_sum, math.sqrt(bkg_err)))

    for sig in signal_entries :
        lines.append('S/sqrt(S+B) (%s/All Bkg) : %f' %( sig, signal_entries[sig][0]/math.sqrt(signal_entries[sig][0] + bkg_sum ) ))

    for sig in signal_entries :
        for st in stack_entries :
            den = math.sqrt(signal_entries[sig][0] + stack_entries[st][0] )
            if den != 0 :
                lines.append('S/sqrt(S+B) (%s/%s) : %f' %( sig, st,  signal_entries[sig][0]/ den ))
            else :
                lines.append('S/sqrt(S+B) (%s/%s) : NAN' %( sig, st  ))

    for line in lines :
        print line

    if txtname is not None and options.outputDir is not None  :

        if txtname.count('.txt') == 0 :
            txtname += '.txt'
        txtfile = open( options.outputDir + '/' + txtname, 'w')
        for line in lines :
            txtfile.write( line + '\n' )
        txtfile.close()

    return

#---------------------------------------
def DumpRoc( txtname=None, inDirs='' ) :

    global samples

    output = []
    for title, entries in samples.transient_data.iteritems() :
        output.append( title )
        print output[-1]
        for entry in entries :
            output.append('Cutval=%(CutVal)f, nSig=%(nSig)f, nBkg=%(nBkg)f, sigEff=%(sigEff)f, bkgEff=%(bkgEff)f, S/sqrt(S+B)=%(SoverRootSplusB)f ' %entry )
            print output[-1]

    if txtname is not None and options.outputDir is not None  :

        outdir = options.outputDir + '/' + inDirs

        if not os.path.isdir( outdir ) :
            print 'Making directory : ', outdir
            os.makedirs( outdir )

        if txtname.count('.txt') == 0 :
            txtname += '.txt'

        txtfile = open( outdir + '/' + txtname, 'w' )
        for out in output :
            txtfile.write( out + '\n' )
        txtfile.close()

#---------------------------------------
# User functions
#---------------------------------------

#---------------------------------------
def DrawFormatted(varexp, selection, histpars=None ) :
    """ Example wrapper function.   Make a stack and then add some extra goodies """

    global samples

    print 'DrawFormatted histpars ', histpars
    samples.MakeStack(varexp, selection, histpars)

    statuslabel = ROOT.TLatex(0.4, 0.8, 'Atlas Internal')
    statuslabel.SetNDC()
    luminosity = ROOT.TLatex(0.4, 0.7, ' 10.0 fb^{-1}')
    luminosity.SetNDC()
    samples.add_decoration(statuslabel)
    samples.add_decoration(luminosity)

    samples.DrawCanvas()

    statuslabel.Draw()
    luminosity.Draw()

#---------------------------------------
def WriteCurrentHists( filename='hist.root') :
    """ write all histograms in samples to a root file """

    file = ROOT.TFile.Open( filename, 'RECREATE')

    for hist, samp in samples.samples.iteritems() :
        newhist = samp.hist.Clone(hist)
        file.cd()
        newhist.Write()

    file.Close()
        
#---------------------------------------
#graveyard.py
#def MakeTAndPHists( outputfile, tagprobe_min=0, tagprobe_max=1e9, normalize=1 ) :
#def MakeTAndPPlots( ) :
#---------------------------------------
def MakeWggEventPlots( save=False ) :

    subdir='WggEventPlots'

    if save and options.outputDir is None :
        print 'Must provide an outputDir to save plots'
        save=False

    #ph_cuts = ' && ph_IsEB[0] && ph_IsEB[1]'
    ph_cuts = ''

    samples.activate_sample( 'ISR')
    samples.activate_sample( 'FSR')
    samples.deactivate_sample( 'Wgg')

    samples.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && el_n==0 %s )' %ph_cuts, (25, 0, 5 ) , ymin=0.1, ymax=10000, logy=1, xlabel='#Delta R( l, lead #gamma)', ylabel='Events / 0.2', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87), legendConfig=samples.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double' ) )

    if save :
        name = 'leadPhot_leadLepDR__mgg__noLepPhDRCuts__splitWggISRFSR'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('sublPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && el_n==0  %s )' %ph_cuts, (25, 0, 5 ) , ymin=0.1, ymax=10000, logy=1, xlabel='#Delta R( l, sublead #gamma)', ylabel='Events / 0.2', labelStyle='fancy', extra_label='Muon Channel', extra_label_loc=(0.73, 0.87), legendConfig=samples.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double'  ) )

    if save :
        name = 'sublPhot_leadLepDR__mgg__noLepPhDRCuts__splitWggISRFSR'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('sublPhot_leadLepDR', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && mu_n==0  %s )' %ph_cuts, (25, 0, 5 ) , ymin=0.1, ymax=50000, logy=1, xlabel='#Delta R( l, sublead #gamma)', ylabel='Events / 0.2', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.7, 0.87), legendConfig=samples.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double'  )  )

    if save :
        name = 'sublPhot_leadLepDR__egg__noLepPhDRCuts__splitWggISRFSR'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('leadPhot_leadLepDR', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && mu_n==0  %s )' %ph_cuts, (25, 0, 5 ) , ymin=0.1, ymax=80000, logy=1, xlabel='#Delta R( l, lead #gamma)', ylabel='Events / 0.2', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.7, 0.87), legendConfig=samples.config_legend( legendCompress=0.8, legendTranslateX=0.05, legendTranslateY=0.05, legendLoc='Double'  )  )

    if save :
        name = 'leadPhot_leadLepDR__egg__noLepPhDRCuts__splitWggISRFSR'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')


    samples.deactivate_sample( 'ISR')
    samples.deactivate_sample( 'FSR')
    samples.activate_sample( 'Wgg')

    samples.Draw('m_lepphph', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %ph_cuts, (60, 0, 300 ) , logy=0,  xlabel='M_{l,#gamma,#gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86), legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.3, ) )

    if save :
        name = 'm_lepphph__egg__baselineCuts'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('m_lepphph', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %ph_cuts, (60, 0, 300 ) , logy=0,  xlabel='M_{l,#gamma,#gamma} [GeV]', labelStyle='fancy', extra_label='Muon Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.3, ) )


    if save :
        name = 'm_lepphph__mgg__baselineCuts'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('m_lepph1', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %ph_cuts, (40, 0, 200 ) , logy=0,  xlabel='M_{l, lead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86), legendTranslateX=0.05 , legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.3, ) )

    if save :
        name = 'm_lepph1__egg__baselineCuts'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('m_lepph1', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %ph_cuts, (40, 0, 200 ) , logy=0,  xlabel='M_{l, lead #gamma} [GeV]', labelStyle='fancy', extra_label='Muon Channel',   extra_label_loc=(0.3, 0.86) , ymin=0, ymax=55, legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.3, ) )


    if save :
        name = 'm_lepph1__mgg__baselineCuts'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('m_lepph2', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %ph_cuts, (40, 0, 200 ) , logy=0,  xlabel='M_{l, sublead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.3, ) )

    if save :
        name = 'm_lepph2__egg__baselineCuts'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('m_lepph2', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %ph_cuts, (40, 0, 200 ) , logy=0,  xlabel='M_{l, sublead #gamma} [GeV]', labelStyle='fancy', extra_label='Muon Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.3, ) )


    if save :
        name = 'm_lepph2__mgg__baselineCuts'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('m_phph', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %ph_cuts, (50, 0, 200 ) , logy=1,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',  extra_label_loc=(0.3, 0.86),  legendWiden=1.2, ymin=0.1, ymax=1000 , legendConfig=samples.config_legend(legendLoc=None,legendCompress=1.2, ) )

    if save :
        name = 'm_phph__egg__baselineCuts'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')

    samples.Draw('m_phph', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %ph_cuts, (50, 0, 200 ) , logy=1,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Muon Channel',  extra_label_loc=(0.3, 0.86),  legendWiden=1.2 , ymin=0.1, ymax=1000 , legendConfig=samples.config_legend(legendLoc=None,legendCompress=1.2, ) )

    if save :
        name = 'm_phph__mgg__baselineCuts'
        SaveStack( name, 'base', inDirs=subdir )
        DumpStack(name)
    else :
        raw_input('continue')


    samples.Draw('m_lepph1', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5)  %s)' %ph_cuts, (40, 0, 200 ) , logy=0,  xlabel='M_{l, lead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.3, ) )
    if save :
        name = 'm_lepph1__egg__Cut_m_lepphph_10gevWindow'
        DumpStack(name)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpStack()
        raw_input('continue')


    samples.Draw('m_lepph2', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5)  %s)' %ph_cuts, (40, 0, 200 ) , logy=0,  xlabel='M_{l, sublead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.3, ) )

    if save :
        name = 'm_lepph2__egg__Cut_m_lepphph_10gevWindow'
        DumpStack(name)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpStack()
        raw_input('continue')

    samples.Draw('m_lepph2', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  %s)' %ph_cuts, (40, 0, 200 ) , logy=0,  xlabel='M_{l, sublead #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.4, ) )
    if save :
        name = 'm_lepph2__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow'
        DumpStack(name)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpStack()
        raw_input('continue')


    samples.Draw('m_lepph2', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5)  %s)' %ph_cuts, (40, 0, 200 ) , logy=0,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel',   extra_label_loc=(0.3, 0.86) , legendConfig=samples.config_legend(legendWiden=1.3,legendCompress=1.4, ) )

    if save :
        name = 'm_lepph2__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow__Cut_m_lepph2_10gevWindow'
        DumpStack(name)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpStack()
        raw_input('continue')

    samples.Draw('m_phph', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5)  %s)' %ph_cuts, (50, 0, 200 ) , logy=1,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samples.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    if save :
        name = 'm_phph__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow__Cut_m_lepph2_10gevWindow'
        DumpStack(name)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpStack()
        raw_input('continue')


    samples.Draw('m_phph', 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) && m_phph>15  %s)' %ph_cuts, (50, 0, 200 ) , logy=1,  xlabel='M_{#gamma, #gamma} [GeV]', labelStyle='fancy', extra_label='Electron Channel', extra_label_loc=(0.3, 0.86), ymin=0.5, ymax=100,   legendConfig=samples.config_legend(legendCompress=1.2,legendWiden=1.2, ) )
    if save :
        name = 'm_phph__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow__Cut_m_lepph2_10gevWindow__Cut_m_phph_15'
        DumpStack(name)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpStack()
        raw_input('continue')

    samples.MakeRocCurve( ['m_phph', 'm_phph'], ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  && (fabs(m_lepphph-91.2) > 5) && (fabs(m_lepph1-91.2) > 5)  && (fabs(m_lepph2-91.2) > 5))']*2, ['Wgg', 'Wgg'], ['AllBkg', 'Zgamma'], [(50, 0, 200 )]*2, doSoverB=1, less_than=[0,0], colors=[ROOT.kRed, ROOT.kBlue], legend_entries=['B = All MC backgrounds', 'B = Zjets + Z#gamma'], ymin=0.5, ymax=4.5, legendConfig=samples.config_legend( legendWiden=1.3, legendCompress=1.4, legendTranslateX=-0.4 ) )

    if save :
        name = 'm_phph__egg__Cut_m_lepphph_10gevWindow__Cut_m_lepph1_10gevWindow__Cut_m_lepph2_10gevWindow__RocCurve'
        DumpRoc(name, inDirs=subdir)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpRoc()
        raw_input('continue')

    #samples.MakeRocCurve( ['m_phph', 'm_phph'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && el_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  %s)' %ph_cuts]*2, ['Wgg', 'Wgg'], ['AllBkg', 'ZjetsZgamma'], [(50, 0, 200 )]*2, doSoverB=1, debug=1, less_than=[0,0], colors=[ROOT.kRed, ROOT.kBlue], legend_entries=['B = All MC backgrounds', 'B = Zjets + Z#gamma'] )

    #raw_input('continue')


#---------------------------------------
def MakeWggMvaPlots( save=False ) :

    global samples

    subdir = 'WggMvaPlots'

    selection = 'PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && m_phph>15  )'
    binning = ( 40, -0.3, 0.5)

    samples.MakeRocCurve( ['zrej_mvascore']*2, [ selection ]*2, ['Wgg', 'Wgg'], ['AllBkg', 'ZjetsZgamma'], [binning]*2, doSoverB=1, debug=1, less_than=[0,0], colors=[ROOT.kRed, ROOT.kBlue], legend_entries=['B = All MC backgrounds', 'B = Zjets + Z#gamma'], ymin=0, ymax=6, legendConfig=samples.config_legend( legendWiden=1.4, legendCompress=1.4, legendTranslateX=-0.35 ) )

    if save :
        name = 'zrej_mvascore__egg__baselineCuts__RocCurve1EleVetoData'
        DumpRoc(name, inDirs=subdir)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpRoc()
        raw_input('continue')

    samples.Draw( 'zrej_mvascore', selection, binning, xlabel='BDT score', ylabel='Events / 0.2', legendConfig=samples.config_legend( legendWiden=1.1, legendCompress=1.2 ), labelStyle='fancy'  )

    if save :
        name = 'zrej_mvascore__egg__baselineCuts__1EleVetoData'
        DumpRoc(name, inDirs=subdir)
        SaveStack( name, 'base', inDirs=subdir )
    else :
        DumpRoc()
        raw_input('continue')

#---------------------------------------
def MakeWggEleVetoCompPlots( save=False ) :

    global samples

    subdir = 'WggEleVetoCompPlots'

    selection = ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && ph_phDR>0.3 && m_phph>15 ) '] +  ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ( (ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 ) || ( ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 ) ) && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && ph_phDR>0.3 && m_phph>15 )']*2
    #jselection = ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_passMedium[0] && ph_passMedium[1] && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && ph_phDR>0.3 && m_phph>15 ) '] +  ['PUWeight * ( el_passtrig_n>0 && el_n==1 && ph_n==2 && ( ( ph_passMedium[0] && ph_hasPixSeed[0]==1 ) || ( !ph_passMedium[0] ) ) && && leadPhot_leadLepDR>0.7 && sublPhot_leadLepDR>0.7 && ph_phDR>0.3 && m_phph>15 )']*2

    sample_names = ['ZjetsZgamma', 'ZjetsZgamma', 'Data']
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue]
    legend_entries = ['Z MC -- 2 eleVeto photons', 'Z MC -- 1 eleVeto photon', 'Data -- 1 eleVeto photon']

    samples.CompareSelections( 'm_phph', selection , sample_names , (20, 0, 200 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='M_{#gamma #gamma} [GeV]', ymin=0, ymax=0.3 )

    if save :
        name = 'm_phph__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.Draw('m_phph', selection[2], ( 20, 0, 200 ), xlabel='M_{#gamma #gamma} [GeV]' )

    if save :
        name = 'm_phph__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.CompareSelections( 'm_lepphph', selection , sample_names ,(40, 0, 400 ) ,  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='M_{l #gamma #gamma} [GeV]', ymin=0, ymax=0.3  )
    if save :
        name = 'm_lepphph__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.Draw( 'm_lepphph', selection[2],(40, 0, 400 ), xlabel='M_{l #gamma #gamma} [GeV]'  )

    if save :
        name = 'm_lepphph__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')


    samples.CompareSelections( 'm_lepph1', selection , sample_names , (20, 0, 200 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='M_{l lead #gamma} [GeV]', ymin=0, ymax=0.3   )

    if save :
        name = 'm_lepph1__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.Draw( 'm_lepph1', selection[2], (20, 0, 200 ), xlabel='M_{l lead #gamma} [GeV]')

    if save :
        name = 'm_lepph1__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.CompareSelections( 'm_lepph2', selection , sample_names , (20, 0, 200 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='M_{l sublead #gamma} [GeV]', ymin=0, ymax=0.3  )

    if save :
        name = 'm_lepph2__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.Draw( 'm_lepph2', selection[2], (20, 0, 200 ), xlabel='M_{l sublead #gamma} [GeV]' )

    if save :
        name = 'm_lepph2__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.CompareSelections( 'leadPhot_leadLepDR', selection , sample_names , (20, 0, 5 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='#Delta R( l, lead #gamma) ', ylabel='Normalized Events / 0.25', ymin=0, ymax=0.3   )

    if save :
        name = 'leadPhot_leadLepDR__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.Draw( 'leadPhot_leadLepDR', selection[2], (20, 0, 5 ), xlabel='#Delta R( l, lead #gamma) ', ylabel='Events / 0.25' )

    if save :
        name = 'leadPhot_leadLepDR__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.CompareSelections( 'sublPhot_leadLepDR', selection , sample_names , (20, 0, 5 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='#Delta R( l, sublead #gamma)', ylabel='Normalized Events / 0.25', ymin=0, ymax=0.3   )

    if save :
        name = 'sublPhot_leadLepDR__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.Draw( 'sublPhot_leadLepDR', selection[2], (20, 0, 5 ), xlabel='#Delta R( l, sublead #gamma)', ylabel='Events / 0.25' )

    if save :
        name = 'sublPhot_leadLepDR__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.CompareSelections( 'ph_phDR', selection , sample_names , (20, 0, 5 ),  colors=colors, normalize=1, doratio=1, legend_entries=legend_entries, xlabel='#Delta R( #gamma, #gamma)', ylabel='Normalized Events / 0.25', ymin=0, ymax=0.3  )

    if save :
        name = 'ph_phDr__egg__nPhPassEleVetoComp'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')

    samples.Draw( 'ph_phDR', selection[2], (20, 0, 5 ), xlabel='#Delta R( #gamma, #gamma)', ylabel='Events / 0.25')

    if save :
        name = 'ph_phDr__egg__Cut_invertEleVeto1Ph'
        SaveStack( name, 'base', inDirs=subdir )
    else :
        raw_input('continue')


#---------------------------------------
def MakePhotonCompPlots( ) :

    global samples

    samples.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2 , ['Wgamma','Inclusive W'], (100, 0, 0.1), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.00001, ymax = 0.5, logy=1, xlabel='#sigma i#eta i#eta', extra_label='Endcap photons', ylabel='Normalized Events / 0.001'  )
    SaveStack('ph_sigmaIEIE_EE_comp_wg_wjets', 'base')

    samples.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2 , ['Wgamma','Inclusive W'], (100, 0, 0.03), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.00001, ymax = 0.8, logy=1, xlabel='#sigma i#eta i#eta', extra_label='Barrel photons', ylabel='Normalized Events / 0.0003'  ) 
    SaveStack('ph_sigmaIEIE_EB_comp_wg_wjets', 'base')

    samples.CompareSelections('ph_chIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2 , ['Wgamma','Inclusive W'], (100, 0, 100), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected charged hadron isolation [GeV]', extra_label='Barrel photons', ylabel='Normalized Events / GeV'  )
    SaveStack('ph_chIsoCorr_EB_comp_wg_wjets', 'base')

    samples.CompareSelections('ph_chIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2 , ['Wgamma','Inclusive W'], (100, 0, 100), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected charged hadron isolation [GeV]', extra_label='Endcap photons', ylabel='Normalized Events / GeV'  )
    SaveStack('ph_chIsoCorr_EE_comp_wg_wjets', 'base')

    samples.CompareSelections('ph_neuIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2 , ['Wgamma', 'Inclusive W'], (80, -20, 20), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected neutral hadron isolation [GeV]', extra_label='Endcap photons', ylabel='Normalized Events / 0.5 GeV'  )
    SaveStack('ph_neuIsoCorr_EE_comp_wg_wjets', 'base')

    samples.CompareSelections('ph_neuIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2 , ['Wgamma', 'Inclusive W'], (80, -20, 20), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected neutral hadron isolation [GeV]', extra_label='Barrel photons', ylabel='Normalized Events / 0.5 GeV'  )
    SaveStack('ph_neuIsoCorr_EB_comp_wg_wjets', 'base')

    samples.CompareSelections('ph_phoIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2 , ['Wgamma', 'Inclusive W'], (100, -5, 45), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected photon isolation [GeV]', extra_label='Endcap photons', ylabel='Normalized Events / 0.5 GeV'  )
    SaveStack('ph_phoIsoCorr_EE_comp_wg_wjets', 'base')

    samples.CompareSelections('ph_phoIsoCorr[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2 , ['Wgamma', 'Inclusive W'], (100, -5, 45), colors=[ROOT.kRed, ROOT.kBlack],normalize=1, ymin=0.0001, ymax = 0.8, logy=1, xlabel='p_{T}, #rho corrected photon isolation [GeV]', extra_label='Barrel photons', ylabel='Normalized Events / 0.5 GeV'  )
    SaveStack('ph_phoIsoCorr_EB_comp_wg_wjets', 'base')

    samples.MakeRocCurve(['ph_sigmaIEIE[0]', 'ph_passSIEIEMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, 0, 0.1), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['#sigma i#eta i#eta ROC curve', 'Medium working point'], extra_label='Endcap Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_sigmaIEIE_EE_roc_comp_medium', 'base')
    samples.MakeRocCurve(['ph_sigmaIEIE[0]', 'ph_passSIEIEMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, 0, 0.03), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['#sigma i#eta i#eta ROC curve', 'Medium working point'], extra_label='Barrel Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_sigmaIEIE_EB_roc_comp_medium', 'base')

    samples.MakeRocCurve(['ph_chIsoCorr[0]', 'ph_passChIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, 0, 100), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr ch iso ROC curve', 'Medium working point'], extra_label='Endcap Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_chIsoCorr_EE_roc_comp_medium', 'base')
    samples.MakeRocCurve(['ph_chIsoCorr[0]', 'ph_passChIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, 0, 100), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr ch iso ROC curve', 'Medium working point'], extra_label='Barrel Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_chIsoCorr_EB_roc_comp_medium', 'base')

    samples.MakeRocCurve(['ph_neuIsoCorr[0]', 'ph_passNeuIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, -20, 20), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr neu iso ROC curve', 'Medium working point'], extra_label='Endcap Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_neuIsoCorr_EE_roc_comp_medium', 'base')
    samples.MakeRocCurve(['ph_neuIsoCorr[0]', 'ph_passNeuIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, -20, 20), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr neu iso ROC curve', 'Medium working point'], extra_label='Barrel Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_neuIsoCorr_EB_roc_comp_medium', 'base')

    samples.MakeRocCurve(['ph_phoIsoCorr[0]', 'ph_passPhoIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEE[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, -5, 45), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr pho iso ROC curve', 'Medium working point'], extra_label='Endcap Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_phoIsoCorr_EE_roc_comp_medium', 'base')
    samples.MakeRocCurve(['ph_phoIsoCorr[0]', 'ph_passPhoIsoCorrMedium[0]'], ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_pt[0]>15 && ph_IsEB[0] )']*2, ['Wgamma']*2, ['Inclusive W']*2, [(100, -5, 45), (2, 0, 2)], less_than=[1,0], markers=[3, 21], colors=[ROOT.kRed, ROOT.kBlack], debug=1, legend_entries=['p_{T}, #rho corr pho iso ROC curve', 'Medium working point'], extra_label='Barrel Photons', extra_label_loc="BottomLeft" )
    SaveStack('ph_phoIsoCorr_EB_roc_comp_medium', 'base')

def MakePhotonJetFakePlots(save=False ) :

    #------------------------------
    # signal template
    #------------------------------
    #samples.Draw('leadPhot_sublLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] ) ', (50, 0, 5), xlabel='#Delta R(sublead #mu, #gamma)', ylabel='Events / 0.1' )
    #raw_input('continue')
    #samples.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] ) ', (50, 0, 5), xlabel='#Delta R(lead #mu, #gamma)', ylabel='Events / 0.1', legendLoc='TopLeft' )
    #raw_input('continue')
    #samples.Draw('m_leplepph', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && leadPhot_sublLepDR>0.4 ) ', (100, 0, 500), xlabel='M_{#mu#mu#gamma} [GeV]', logy=1, ymin=1, ymax=1000000, legendCompress=0.8 )
    #raw_input('continue')
    #samples.Draw('m_leplepph+m_leplep', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && leadPhot_sublLepDR>0.4 ) ', (100, 0, 500), xlabel='M_{#mu#mu}+M_{#mu#mu#gamma} [GeV]', logy=1, ymin=1, ymax=1000000, legendCompress=0.8  )
    #raw_input('continue')
    ##samples.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_sublLepDR>0.4 && ( m_leplepph+m_leplep ) < 185  ) ', (50, 0, 5), xlabel='#Delta R(lead #mu, #gamma)', ylabel='Events / 0.1' )
    ##raw_input('continue')
    #samples.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_sublLepDR>0.4 && fabs( m_leplepph-91.2 ) < 5 && ph_IsEB[0] ) ', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_sublLepDR>0.4 && ( m_leplepph+m_leplep ) < 185 && ph_IsEB[0]  ) '], ['Data']*2, (60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', colors=[ROOT.kBlue, ROOT.kRed], legend_entries=[ '|M_{#mu#mu#gamma} - M_{Z}| < 5', 'M_{#mu#mu} + M_{#mu#mu#gamma} < 185 '])
    #raw_input('continue')
    #samples.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_sublLepDR>0.4 && fabs( m_leplepph-91.2 ) < 5 && ph_IsEE[0] ) ', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_sublLepDR>0.4 && ( m_leplepph+m_leplep ) < 185 && ph_IsEE[0]  ) '], ['Data']*2, (50, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.002', colors=[ROOT.kBlue, ROOT.kRed], legend_entries=[ '|M_{#mu#mu#gamma} - M_{Z}| < 5', 'M_{#mu#mu} + M_{#mu#mu#gamma} < 185 '])
    #raw_input('continue')
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_sublLepDR>0.4 && fabs( m_leplepph-91.2 ) < 5 && ph_IsEB[0] )', ( 60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005', logy=1 )
    #raw_input('continue')
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_sublLepDR>0.4 && fabs( m_leplepph-91.2 ) < 5 && ph_IsEE[0] )', ( 50, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.002', logy=1  )
    #raw_input('continue')
    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4 && ph_IsEE[0])']*2 + ['PUWeight * (ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25 && ph_IsEE[0] )'], ['Data', 'Zgamma', 'Wgamma'], (50, 0, 0.1 ), normalize=1, colors=[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], doratio=1, xlabel='#sigma i#etai#eta', ylabel='Normalized Events / 0.002', rlabel='MC / Data', legend_entries=['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'], ymin=0.00001, ymax=5, logy=1, rmin=0.2, rmax=1.8 )
    #raw_input('continue')
    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4 && ph_IsEB[0])']*2 + ['PUWeight * (ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25 && ph_IsEB[0] )'], ['Data', 'Zgamma', 'Wgamma'], (60, 0, 0.03 ), normalize=1, colors=[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], doratio=1, xlabel='#sigma i#etai#eta', ylabel='Normalized Events / 0.0005', rlabel='MC / Data', legend_entries=['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'], ymin=0.00001, ymax=5, logy=1, rmin=0.2, rmax=1.8 )
    #raw_input('continue')
    #samples.CompareSelections( 'ph_pt[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4 )']*2 + ['PUWeight * (ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25 )'], ['Data', 'Zgamma', 'Wgamma'], (50, 0, 200 ), normalize=1, colors=[ROOT.kBlack, ROOT.kRed+2, ROOT.kBlue-3], doratio=1, xlabel='photon p_{T} [GeV]', rlabel='MC / Data', legend_entries=['Data, FSR photons', 'Z#gamma, FSR photons', 'W#gamma, truth matched photons'], ymin=0.00001, ymax=5, logy=1, rmin=0.2, rmax=1.8, legendWiden=1.5 )
    #raw_input('continue')

    #samples.Draw('leadPhot_sublLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 ) ' , (50, 0, 5), xlabel='#Delta R(sublead #mu, #gamma)', ylabel='Events / 0.1', legendCompress=0.8 )
    #raw_input('continue')

    #samples.Draw('leadPhot_leadLepDR', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 )', ( 50, 0, 5), xlabel='#Delta R(lead #mu, #gamma)', ylabel='Events / 0.1', legendLoc='TopLeft', legendCompress=0.8 )
    #raw_input('continue')
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR > 1 && ph_IsEB[0])', ( 60, 0, 0.03), xlabel='#sigma i#etai#eta', ylabel='Events / 0.0005' )
    #raw_input('continue')
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0] )', ( 50, 0, 0.1), xlabel='#sigma i#etai#eta', ylabel='Events / 0.002')
    #raw_input('continue')

    #samples.Draw('ph_SCRChIso[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ) ', (50, 0, 50), xlabel='ch Had Iso (footprint subtracted) [GeV]', logy=1  )
    #raw_input('continue')
    #samples.Draw('ph_SCRNeuIso[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ) ', (50, 0, 50), xlabel='neu Had Iso (footprint subtracted) [GeV]', logy=1  )
    #raw_input('continue')
    #samples.Draw('ph_SCRNeuIso[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ) ', (40, 0, 20), xlabel='neu Had Iso (footprint subtracted) [GeV]', logy=1  )
    #raw_input('continue')
    #samples.Draw('ph_neuIsoCorr[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ) ', (40, 0, 20), xlabel='neu Had Iso (p_{T}, #rho corr) [GeV]', logy=1  )
    #raw_input('continue')
    #samples.Draw('ph_phoIsoCorr[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ) ', (40, 0, 20), xlabel='Pho Iso (p_{T}, #rho corr) [GeV]', logy=1  )
    #raw_input('continue')
    #samples.Draw('ph_phoIsoCorr[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ) ', (40, 0, 20), xlabel='Pho Iso (p_{T}, #rho corr) [GeV]', logy=1  )
    #raw_input('continue')
    #samples.Draw('ph_SCRPhoIso[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ) ', (40, 0, 20), xlabel='Pho Iso (footprint subtracted) [GeV]', logy=1  )
    #raw_input('continue')

    #--------------------------------------
    # Charged Iso
    #--------------------------------------

    bins_eb = (10, 0, 0.03)
    bins_ee = (10, 0, 0.1)

    cutname = 'ph_chIsoCorr'
    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_eb_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')
    
    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_ee_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')
    
    cutname = 'ph_SCRChIso'
    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_eb_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')

    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passChIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 2 && %s < 5 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 10 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 5 && %s < 20 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 && %s < 30 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 5 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Ch Iso cut', ' 2 < Iso < 5', '5 < Iso < 10', '5 < Iso < 20', '5 < Iso < 30', 'Iso > 5'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_ee_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')

    #--------------------------------------
    # Neutral Iso
    #--------------------------------------

    cutname = 'ph_neuIsoCorr'
    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_eb_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')
    
    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_ee_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')
    
    cutname = 'ph_SCRNeuIso'
    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_eb_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')

    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_ee_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')

    #--------------------------------------
    # Photon Iso
    #--------------------------------------

    cutname = 'ph_phoIsoCorr'
    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passPhoIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_eb_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')
    
    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passPhoIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_ee_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')
    
    cutname = 'ph_SCRPhoIso'
    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEB[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_eb, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_eb_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')

    common_selection = 'mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_IsEE[0]'
    samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( %s && ph_passNeuIsoCorrMedium[0] )' %common_selection, 'PUWeight * ( %s &&  %s > 1 && %s < 2 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 4 )' %( common_selection, cutname, cutname), 'PUWeight * ( %s && %s > 2 && %s < 6 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 && %s < 10 )' %( common_selection, cutname, cutname),'PUWeight * ( %s && %s > 2 )' %( common_selection, cutname)], ['Zgammastar']*6, bins_ee, normalize=1, colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kMagenta] ,doratio=2, xlabel='#sigma i#eta i#eta', ylabel='Normalized Events / 0.002', legend_entries=['Nominal Neu Iso cut', ' 1 < Iso < 2', '2 < Iso < 4', '2 < Iso < 6', '2 < Iso < 10', 'Iso > 1'], rlabel='Inverted Cut / Nominal cut', rmin=0.6, rmax=1.4, ymin=0, ymax=0.4)
    if save :
        SaveStack('sieie_ee_mmg_comp%scuts' %cutname, 'base')
    else :
        raw_input('continue')


    #samples.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * (mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_leadLepDR>0.4 && ph_IsEB[0] && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25)', ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] && ph_passChIsoCorrMedium[0] )', ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] )', ], ['Wgamma', 'DataRealPhotonSub', 'Data'], (60, 0, 0.03), normalize=1, legend_entries=['Real photon template', 'Fake photon template', 'Target, #mu + #gamma '], colors=[ROOT.kBlue-3, ROOT.kRed+2, ROOT.kBlack], drawHist=[0, 0, 0], logy=1, ymin=0.00001, ymax=3 )
    ##samples.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * (mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_leadLepDR>0.4 && ph_IsEB[0] && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) <25)', ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] && ph_passChIsoCorrMedium[0] )', ], ['Wgamma', 'DataRealPhotonSub'], (60, 0, 0.03), normalize=1, legend_entries=['Real photon template', 'Fake photon template'], colors=[ROOT.kBlue-3, ROOT.kRed+2], drawHist=[1, 1], logy=1, ymin=0.00001, ymax=3 )
    #if save :
    #    SaveStack('sieie_eb_comp_templates_mcsigtemp', 'base')
    #else :
    #    raw_input('continue')

    ##samples.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * (mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4 && ph_IsEB[0] )', ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] && ph_passChIsoCorrMedium[0] )', ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] )', ], ['Data', 'DataRealPhotonSub', 'Data'], (60, 0, 0.03), normalize=1, legend_entries=['Real photon template', 'Fake photon template', 'Target, #mu + #gamma '], colors=[ROOT.kBlue-3, ROOT.kRed+2, ROOT.kBlack], drawHist=[1, 1, 0], logy=1, ymin=0.00001, ymax=3 )
    #samples.CompareSelections('ph_sigmaIEIE[0]', ['PUWeight * (mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4 && ph_IsEB[0] )', ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] && ph_passChIsoCorrMedium[0] )'], ['Data', 'DataRealPhotonSub'], (60, 0, 0.03), normalize=1, legend_entries=['Real photon template', 'Fake photon template'], colors=[ROOT.kBlue-3, ROOT.kRed+2], drawHist=[1, 1], logy=1, ymin=0.00001, ymax=3 )
    #if save :
    #    SaveStack('sieie_eb_comp_templates_datasigtemp', 'base')
    #else :
    #    raw_input('continue')

    #selection_base = 'mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12<0.05 && ph_IsEB[0] && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    #selections = [
    #              'PUWeight * ( %s )' %selection_base, 
    #              'PUWeight * ( %s && ph_pt[0]<20 )' %selection_base , 
    #              'PUWeight * ( %s && ph_pt[0]<25 && ph_pt[0]>20 )' %selection_base , 
    #              'PUWeight * ( %s && ph_pt[0]>25 && ph_pt[0]<30 )' %selection_base , 
    #              'PUWeight * ( %s && ph_pt[0]>30 && ph_pt[0]<40 )' %selection_base , 
    #              'PUWeight * ( %s && ph_pt[0]>40 && ph_pt[0]<60 )' %selection_base , 
    #              'PUWeight * ( %s && ph_pt[0]>60 && ph_pt[0]<90 )' %selection_base , 
    #              'PUWeight * ( %s && ph_pt[0]>90 )'%selection_base
    #             ]
    #samples.CompareSelections('ph_sigmaIEIE[0]', selections , ['Wgamma']*8, (15, 0, 0.03), xlabel='#sigma i#eta i#eta', ylabel = 'Events / %f' %(0.03/15), normalize=1 , colors=[ROOT.kBlack, ROOT.kOrange+5, ROOT.kBlue, ROOT.kRed, ROOT.kMagenta, ROOT.kGreen, ROOT.kGray, ROOT.kOrange], legend_entries=['Inclusive', '15 < p_{T} < 20', '20 < p_{T} < 25', '25 < p_{T} < 30', '30 < p_{T} < 40', '40 < p_{T} < 60', '60 < p_{T} < 90', 'p_{T} > 90'], doratio=2 )
    #raw_input('continue')
    #selection_base = 'mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12<0.05 && ph_IsEB[0] && !(ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25) && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    #samples.CompareSelections('ph_sigmaIEIE[0]', selections , ['Wjets']*8, (15, 0, 0.03), xlabel='#sigma i#eta i#eta', ylabel = 'Events / %f' %(0.03/15), normalize=1 , colors=[ROOT.kBlack, ROOT.kOrange+5, ROOT.kBlue, ROOT.kRed, ROOT.kMagenta, ROOT.kGreen, ROOT.kGray, ROOT.kOrange], legend_entries=['Inclusive', '15 < p_{T} < 20', '20 < p_{T} < 25', '25 < p_{T} < 30', '30 < p_{T} < 40', '40 < p_{T} < 60', '60 < p_{T} < 90', 'p_{T} > 90'], doratio=2 )



#graveyard.py
#def MakeDiPhotonTemplatePlots() :
#def MakeZHCutFlowTables( channel='EE' ) :
    
#def MakeQCDCRPlots() :

#def MakeTAndPCompPlots( ) :
#def MakeTAndPCompPlotsFull( ) :
#def FitTAndPComp( ) :

#
# The following is to get the history 
#
import atexit
historyPath = os.path.expanduser("~/.pyhistory")
try:
    import readline
except ImportError:
    print "Module readline not available."
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")
    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)


# -----------------------------------------------------------------
def save_history(historyPath=historyPath):
    try:
        import readline
    except ImportError:
        print "Module readline not available."
    else:
        readline.write_history_file(historyPath)

atexit.register(save_history)

main()
