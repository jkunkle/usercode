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

options = p.parse_args()

import sys
import os
import re
import math
import uuid
import copy
import imp
import ROOT

from SampleManager import SampleManager

ROOT.gROOT.SetBatch(False)

samples = None

def main() :

    global samples

    if not options.baseDir.count('/eos/') and not os.path.isdir( options.baseDir ) :
        print 'baseDir not found!'
        return

    samples = SampleManager(options.baseDir, options.treeName, mcweight=options.mcweight, treeNameModel=options.treeNameModel, filename=options.fileName, base_path_model=options.baseDirModel, xsFile=options.xsFile, lumi=options.lumi, readHists=options.readHists)


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
def SaveStack( filename, canname=None  ) :
    """ Save current plot to filename.  Must supply --outputDir  """

    global samples

    if options.outputDir is None :
        print 'No output directory provided.  Will not save.'
    else :

        if not os.path.isdir( options.outputDir ) :
            print 'Creating directory %s' %options.outputDir
            os.mkdir(options.outputDir)

        #histnamepdf = options.outputDir + '/' + filename.split('.')[0]+'.pdf'
        #histnameeps = options.outputDir + '/' + filename.split('.')[0]+'.eps'
        histnamepdf = options.outputDir + '/' + filename+'.pdf'
        histnameeps = options.outputDir + '/' + filename+'.eps'

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

def MakeTAndPHists( outputfile ) :

    global samples

    print 'FIXFIXFIX'
    samples.DoTAndP( 'probe_pt', 'probe_isPhoton && probe_pt > 15', '!probe_isPhoton && probe_pt > 15', 'Zgammastar', [15, 5000 ], colors=[ROOT.kBlack], normalize=0 )
    hist_norm = samples.get_samples(isRatio=True)[0].hist.Clone('norm')

    samples.DoTAndP( 'probe_eta', 'probe_isPhoton && probe_pt > 15', '!probe_isPhoton && probe_pt > 15', 'Zgammastar', [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.900000, -1.800000, -1.700000, -1.566000, -1.479000, -1.400000, -1.300000, -1.200000, -1.100000, -1.000000, -0.800000, -0.600000, -0.400000, -0.200000, 0.000000, 0.200000, 0.400000, 0.600000, 0.800000, 1.000000, 1.100000, 1.200000, 1.300000, 1.400000, 1.479000, 1.566000, 1.700000, 1.800000, 1.900000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5], colors=[ROOT.kBlack], normalize=1 )
    hist_eta = samples.get_samples(isRatio=True)[0].hist.Clone('eta')

    samples.DoTAndP( 'probe_pt', 'probe_isPhoton && probe_pt > 15', '!probe_isPhoton && probe_pt > 15', 'Zgammastar', [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 150, 200, 500 ], colors=[ROOT.kBlack], normalize=1 )
    hist_pt = samples.get_samples(isRatio=True)[0].hist.Clone('pt')


    file = ROOT.TFile.Open( outputfile, 'RECREATE' )

    hist_eta.Write()
    hist_pt.Write()
    hist_norm.Write()

    file.Close()


#---------------------------------------
def MakeTAndPPlots( ) :

    if options.outputDir is None :
        print 'Must provide an output directory via --outputDir.  Will not make plots'
        return
    
    DoTAndP( 'probe_pt', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==0 && passcut_mll )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll )',  ['DataMCSubtracted', 'Z + Jets'], (60, 0, 300, 250 ), xlabel='Electron p_{T} [GeV]', ylabel='Electron to photon fake factor', ymin=0.01, ymax=0.022, label='unconverted photons' )
    SaveStack('probe_pt_electron_to_photon_ff_mcsub_0conv', 'ratiocan')

    DoTAndP( 'probe_pt', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==2 && passcut_mll )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll )',  ['DataMCSubtracted', 'Z + Jets'], (60, 0, 300, 250 ), xlabel='Electron p_{T} [GeV]', ylabel='Electron to photon fake factor', ymin=0.006, ymax=0.018, label='2 track conversion photons' )
    SaveStack('probe_pt_electron_to_photon_ff_mcsub_2conv', 'ratiocan')
    
    DoTAndP( 'probe_eta', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==0 && passcut_mll )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll )',  ['DataMCSubtracted', 'Z + Jets'], (50, -2.5, 2.5 ), xlabel='Electron #eta', ylabel='Electron to photon fake factor', ymin=0.005, ymax=0.042, label='unconverted photons' )
    SaveStack('probe_eta_electron_to_photon_ff_mcsub_0conv', 'ratiocan')

    DoTAndP( 'probe_eta', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==2 && passcut_mll )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll )',  ['DataMCSubtracted', 'Z + Jets'], (50, -2.5, 2.5 ), xlabel='Electron #eta', ylabel='Electron to photon fake factor', label='2 track conversion photons' )
    SaveStack('probe_eta_electron_to_photon_ff_mcsub_2conv', 'ratiocan')


    DoTAndP( 'probe_pt', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==0 && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50  )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll  && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50)',  ['DataMCSubtracted', 'Z + Jets'], (60, 0, 300, 250 ), xlabel='Electron p_{T} [GeV]', ylabel='Electron to photon fake factor', ymin=0.01, ymax=0.022, label='unconverted photons' )
    SaveStack('probe_pt_electron_to_photon_ff_mtcut_mcsub_0conv', 'ratiocan')

    DoTAndP( 'probe_pt', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==2 && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )',  ['DataMCSubtracted', 'Z + Jets'], (60, 0, 300, 250 ), xlabel='Electron p_{T} [GeV]', ylabel='Electron to photon fake factor', ymin=0.006, ymax=0.018, label='2 track conversion photons' )
    SaveStack('probe_pt_electron_to_photon_ff_mtcut_mcsub_2conv', 'ratiocan')
    
    DoTAndP( 'probe_eta', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==0 && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )',  ['DataMCSubtracted', 'Z + Jets'], (50, -2.5, 2.5 ), xlabel='Electron #eta', ylabel='Electron to photon fake factor', ymin=0.005, ymax=0.042, label='unconverted photons' )
    SaveStack('probe_eta_electron_to_photon_ff_mtcut_mcsub_0conv', 'ratiocan')

    DoTAndP( 'probe_eta', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==2 && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )',  ['DataMCSubtracted', 'Z + Jets'], (50, -2.5, 2.5 ), xlabel='Electron #eta', ylabel='Electron to photon fake factor', label='2 track conversion photons' )
    SaveStack('probe_eta_electron_to_photon_ff_mtcut_mcsub_2conv', 'ratiocan')



#---------------------------------------
def MakeZHCutFlowTables( channel='EE' ) :

    global samples

    cut_flow = ['']
    if channel == 'EE' :
        cut_base = 'EventWeight * ( passtrig_electron %s)'
        cut_flow.append('IsEE')
    if channel == 'MM' :
        cut_base = 'EventWeight * ( passtrig_muon %s)'
        cut_flow.append('IsMM')

    cut_flow += ['passcut_os', 'passcut_thirdlepveto', 'passcut_mll', 'passcut_met', 'passcut_dphill', 'passcut_ll_dphi_met', 'passcut_fracdiff', 'passcut_met_dphi_trackmet', 'passcut_jetveto']

    cut_selections = []
    for idx in range(1, len(cut_flow)+1 ) :
        cut_selections.append( cut_base%( ' && '.join(cut_flow[0:idx]) ) )

    print cut_selections
    print len(cut_selections)
    cut_labels = ['Trigger', 'DiLep', 'OS', 'ThirdLep', 'Mll', 'Met', 'DPhill', 'ZMetDphi', 'FracDiff', 'MetTrkDPhi', 'JetVeto']

    samples.MakeCutflowTable('met_et', cut_selections, cut_labels, (50, 0, 5000))
    
#---------------------------------------
def MakeQCDCRPlots() :

    global samples
    if options.outputDir is None :
        print 'Must provide an output directory via --outputDir.  Will not make plots'
        return

    #samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( !ph_pass_eratio && !ph_pass_fside && !ph_pass_deltae ) ) ', ( 64, -2, 30 ), xlabel='Calorimeter Isolation [GeV]', ylabel='Events / 0.5 GeV', noAtlasLabel=True, doratio=0, logy=True, ymax=1e12, ymin=1 )
    #SaveStack('ph_corriso_30_invertall', 'base')

    samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( !ph_pass_eratio || !ph_pass_fside || !ph_pass_deltae ) ) ', ( 64, -2, 30 ), xlabel='Calorimeter Isolation [GeV]', ylabel='Events / 0.5 GeV', noAtlasLabel=True, doratio=0, logy=True, ymax=1e13, ymin=1 )
    SaveStack('ph_corriso_30_invertany', 'base')

    samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( ( !ph_pass_eratio && !ph_pass_fside ) || ( !ph_pass_eratio && !ph_pass_deltae ) || ( !ph_pass_fside && !ph_pass_deltae ) ) )', ( 64, -2, 30 ), xlabel='Calorimeter Isolation [GeV]', ylabel='Events / 0.5 GeV', noAtlasLabel=True, doratio=0, logy=True, ymax=5e12, ymin=1 )
    SaveStack('ph_corriso_30_invertmaj', 'base')

    samples.Draw('ph_pt', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_corriso_30 > 10000 && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( !ph_pass_eratio && !ph_pass_fside && !ph_pass_deltae ) ) ', ( 100, 0, 500, 25 ), xlabel='p_{T} [GeV]', noAtlasLabel=True, doratio=0, logy=True, ymax=1e9, ymin=0.01 )
    SaveStack('ph_pt_invertall_noniso', 'base')

    samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0 && ph_corriso_30 > 10000  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( !ph_pass_eratio || !ph_pass_fside || !ph_pass_deltae ) ) ', ( 100, 0, 500, 25 ), xlabel='p_{T} [GeV]', noAtlasLabel=True, doratio=0, logy=True, ymax=1e9, ymin=0.01 )
    SaveStack('ph_pt_invertany_noniso', 'base')

    samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0 && ph_corriso_30 > 10000  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( ( !ph_pass_eratio && !ph_pass_fside ) || ( !ph_pass_eratio && !ph_pass_deltae ) || ( !ph_pass_fside && !ph_pass_deltae ) ) )', ( 100, 0, 500, 25 ), xlabel='p_{T} [GeV]', noAtlasLabel=True, doratio=0, logy=True, ymax=1e9, ymin=0.01 )
    SaveStack('ph_pt_invertmaj_noniso', 'base')

    #samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_pass_tight ) ', ( 64, -2, 30 ), xlabel='Photon Calorimeter Isolation [GeV]', ylabel='Events / 0.5 GeV', noAtlasLabel=True, doratio=0, logy=True, ymax=1e13, ymin=100 )
    #SaveStack('ph_corriso_30_tightnoiso', 'base')


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
