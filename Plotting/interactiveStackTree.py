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

def MakeTAndPHists( outputfile, tagprobe_min=0, tagprobe_max=1e9, normalize=1 ) :

    global samples
    vals_norm = [15, 5000]
    ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 150, 200, 500 ]
    ptvals_2d = [15, 20, 25, 30, 35, 40, 45, 50, 500 ]
    etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.900000, -1.800000, -1.700000, -1.566000, -1.479000, -1.400000, -1.300000, -1.200000, -1.100000, -1.000000, -0.800000, -0.600000, -0.400000, -0.200000, 0.000000, 0.200000, 0.400000, 0.600000, 0.800000, 1.000000, 1.100000, 1.200000, 1.300000, 1.400000, 1.479000, 1.566000, 1.700000, 1.800000, 1.900000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    etavals_2d = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, -1.200000, -0.800000, -0.200000, 0.000000, 0.200000, 0.800000, 1.200000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    #etavals_2d = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, 0.000000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]

    samples.DoTAndP( 'probe_pt', 'probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), '!probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), 'DYJetsToLL', vals_norm, colors=[ROOT.kBlack], normalize=0 )
    hist_norm = samples.get_samples(isRatio=True)[0].hist.Clone('norm')

    samples.DoTAndP( 'probe_eta', 'probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), '!probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), 'DYJetsToLL',etavals , colors=[ROOT.kBlack], normalize=normalize )
    hist_eta = samples.get_samples(isRatio=True)[0].hist.Clone('eta')

    samples.DoTAndP( 'probe_pt', 'probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), '!probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), 'DYJetsToLL', ptvals, colors=[ROOT.kBlack], normalize=normalize )
    hist_pt = samples.get_samples(isRatio=True)[0].hist.Clone('pt')

    samples.DoTAndP( 'probe_pt:probe_eta', 'probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), '!probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), 'DYJetsToLL', (etavals_2d,ptvals_2d), colors=[ROOT.kBlack], normalize=0 )
    hist_pt_eta = samples.get_samples(isRatio=True)[0].hist.Clone('pteta')

    file = ROOT.TFile.Open( outputfile, 'RECREATE' )

    hist_eta.Write()
    hist_pt.Write()
    hist_norm.Write()
    hist_pt_eta.Write()

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

#--- ------------------------------------
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


def MakeTAndPCompPlots( ) :
    global samples
    #ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 150, 500 ]
    #etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.900000, -1.800000, -1.700000, -1.566000, -1.479000, -1.400000, -1.300000, -1.200000, -1.100000, -1.000000, -0.800000, -0.600000, -0.400000, -0.200000, 0.000000, 0.200000, 0.400000, 0.600000, 0.800000, 1.000000, 1.100000, 1.200000, 1.300000, 1.400000, 1.479000, 1.566000, 1.700000, 1.800000, 1.900000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 500 ]
    #etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, 0.000000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, -1.200000, -0.800000, -0.200000, 0.000000, 0.200000, 0.800000, 1.200000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    for pidx, pmin in enumerate(ptvals[:-1]) :
        pmax = ptvals[pidx+1]
        for eidx, emin in enumerate(etavals[:-1]) :
            emax = etavals[eidx+1]
            eta_precision = 1
            eta_precisionm = 1
            if math.fabs(int(emin*10)-emin) != 0 : 
                eta_precision = 3
            if math.fabs(int(emax*10)-emax) != 0 :
                eta_precisionm=3
            samples.CompareSelections('m_tagprobe', ['!probe_isPhoton && probe_pt > %d && probe_pt < %d && probe_eta > %f && probe_eta < %f ' %( pmin, pmax, emin, emax), 'probe_isPhoton && probe_pt > %d && probe_pt < %d && probe_eta > %f && probe_eta < %f ' %( pmin, pmax, emin, emax)], ['DYJetsToLL', 'DYJetsToLL'], (100, 0, 500), colors=[ROOT.kBlack, ROOT.kRed], doratio=0, logy=1, legend_entries=['Probe electrons', 'Probe photons'], ymax_scale=10, xlabel='M_{tag, probe} [GeV]', extra_label='#splitline{%d < p_{T} < %d}{%.*f < #eta < %.*f}' %( pmin, pmax, eta_precision, emin, eta_precisionm, emax ) )
            SaveStack( 'm_tagprobe_pt_%d_%d_eta_%f_%f' %( pmin, pmax, emin, emax), 'base' )
          
def MakeTAndPCompPlotsFull( ) :
    global samples

    #ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 150, 500 ]
    #etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.900000, -1.800000, -1.700000, -1.566000, -1.479000, -1.400000, -1.300000, -1.200000, -1.100000, -1.000000, -0.800000, -0.600000, -0.400000, -0.200000, 0.000000, 0.200000, 0.400000, 0.600000, 0.800000, 1.000000, 1.100000, 1.200000, 1.300000, 1.400000, 1.479000, 1.566000, 1.700000, 1.800000, 1.900000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 500 ]
    #ptvals = [25, 30, 35, 40, 45, 50, 500 ]
    etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, -1.200000, -0.800000, -0.200000, 0.000000, 0.200000, 0.800000, 1.200000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]

    for pidx, pmin in enumerate(ptvals[:-1]) :
        pmax = ptvals[pidx+1]
        for eidx, emin in enumerate(etavals[:-1]) :
            emax = etavals[eidx+1]
            eta_precision = 1
            eta_precisionm = 1
            if math.fabs(int(emin*10)-emin) != 0 : 
                eta_precision = 3
            if math.fabs(int(emax*10)-emax) != 0 :
                eta_precisionm=3

            samples.Draw('m_tagprobe', '!probe_isPhoton && probe_pt > %d && probe_pt < %d && probe_eta > %f && probe_eta < %f ' %( pmin, pmax, emin, emax),  (100, 0, 200), ymin=10, ymax_scale=10, xlabel='M_{tag, probe} [GeV]', extra_label='#splitline{Probe Electrons}{#splitline{%d < p_{T} < %d}{%.*f < #eta < %.*f}}' %( pmin, pmax, eta_precision, emin, eta_precisionm, emax), extra_label_loc='TopLeft', logy=1, noAtlasLabel=True  )
            SaveStack( 'm_tagprobe_probeEl_pt_%d_%d_eta_%f_%f' %( pmin, pmax, emin, emax), 'base' )

            samples.Draw('m_tagprobe', 'probe_isPhoton && probe_pt > %d && probe_pt < %d && probe_eta > %f && probe_eta < %f ' %( pmin, pmax, emin, emax),  (100, 0, 200), ymin=10, ymax_scale=10, xlabel='M_{tag, probe} [GeV]', extra_label='#splitline{Probe Photons}{#splitline{%d < p_{T} < %d}{%.*f < #eta < %.*f}}' %( pmin, pmax, eta_precision, emin, eta_precisionm, emax ), extra_label_loc='TopLeft', logy=1, noAtlasLabel=True )
            SaveStack( 'm_tagprobe_probePh_pt_%d_%d_eta_%f_%f' %( pmin, pmax, emin, emax), 'base' )
          
def FitTAndPComp( ) :
    global samples

    #ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 500 ]
    ptvals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, -1.200000, -0.800000, -0.200000, 0.000000, 0.200000, 0.800000, 1.200000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    meanhist = ROOT.TH1F( 'mean', '', len(ptvals)-1, array('f', ptvals))
    widthhist = ROOT.TH1F( 'width', '', len(ptvals)-1, array('f', ptvals))
    for pidx, pmin in enumerate(ptvals[:-1]) :
        pmax = ptvals[pidx+1]

        #samples.CompareSelections('m_lepph1', ['EventWeight * (el_n==1 && ph_n==1 && ph_pt[0] > %d && ph_pt[0] < %d)' %(pmin, pmax)]*2, ['DYJetsToLL', 'DYJetsToLLFF'], (500, 0, 500), doratio=0 )
        samples.CompareSelections('m_lepph1', ['EventWeight * (el_n==1 && ph_n==1 && ph_eta[0] > %f && ph_eta[0] < %f)' %(pmin, pmax)]*2, ['DYJetsToLL', 'DYJetsToLLFF'], (500, 0, 500), doratio=0 )

        hist_lg = samples.get_samples(name='DYJetsToLL0')[0].hist
        hist_ff = samples.get_samples(name='DYJetsToLLFF1')[0].hist

        func = ROOT.TF1( 'gaus', 'gaus(0)', 86, 96 )
        func.SetParameter(0, hist_lg.GetBinContent( hist_lg.FindBin( 91) ) )
        func.SetParameter(1, 91)
        func.SetParameter(2, 3)

        hist_lg.Fit( func, 'R')
        mean_lg = func.GetParameter(1)
        width_lg = func.GetParameter(2)

        func.SetParameter(0, hist_ff.GetBinContent( hist_ff.FindBin( 91) ) )
        func.SetParameter(1, 91)
        func.SetParameter(2, 3)
        hist_ff.Fit( func, 'R' )
        mean_ff = func.GetParameter(1)
        width_ff = func.GetParameter(2)

        meanhist.SetBinContent( pidx+1, mean_lg - mean_ff )
        widthhist.SetBinContent( pidx+1, width_lg - width_ff )

        print 'Pt range = %d - %d' %( pmin, pmax )
        print 'Delta mean = %f' %(mean_lg - mean_ff)
        print 'Delta width = %f' %(width_lg - width_ff)

    meanhist.Draw()
    raw_input('continue')
    widthhist.Draw()
    raw_input('continue')



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
