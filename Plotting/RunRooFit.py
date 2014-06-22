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
import random

from SampleManager import SampleManager
from SampleManager import Sample

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

    #DoPhJetFakeSIEIETemplateFit()
    #DoDiPhotonSIEIETemplateFit( outputDir=options.outputDir )
    #DoDiPhotonSIEIETemplateFit(  )
    DoDiPhotonSIEIETemplateFitSimple( outputDir=options.outputDir )
    #DoDiPhoton2DSIEIETemplateFit()

def DoPhJetFakeSIEIETemplateFit() :

    #iso_cuts = 'ph_passSIEIEMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    iso_cuts = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    #iso_cuts = 'ph_chIsoCorr[0]< 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 '
    #iso_cuts = 'ph_chIsoCorr[0] > -99999'

    #signal_base = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4'
    #signal_sample = 'Data'
    signal_base = 'mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 ' %iso_cuts
    signal_sample = 'Wgamma'

    #bkg_base =  ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 '
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < m 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_phoIsoCorr[0] > 2 && ph_phoIsoCorr[0] < 4   '
    bkg_base = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %iso_cuts
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_passChIsoCorrMedium[0] '
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && ph_passChIsoCorrMedium[0] '
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && !( ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25) '

    bkg_sample = 'DataRealPhotonZgSub'
    #bkg_sample = 'Zgammastar'

    #target_base = ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && mt_lep_met > 60 )'
    iso_cuts_subl = iso_cuts.replace('[0]', '[1]')
    iso_cuts_tot = iso_cuts + ' && ' + iso_cuts_subl
    target_bases = [
                    'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && ph_phDR>0.3 && !ph_passSIEIEMedium[1] ' %iso_cuts_tot,
                    #'el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && ph_phDR>1.0 && !ph_passSIEIEMedium[1] ' %iso_cuts_tot,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_chIsoCorr[1]< 5 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3  ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3  ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_chIsoCorr[1]< 5 && ph_phoIsoCorr[1] < 3  ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_chIsoCorr[1]< 5 && ph_neuIsoCorr[1] < 3  ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && %s && ph_phDR>0.3 ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_passPhoIsoCorrMedium[1] ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_passNeuIsoCorrMedium[1] ' %iso_cuts,
                    #'mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_passChIsoCorrMedium[1]  ' %iso_cuts,
                    #' mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s ' %iso_cuts
                   ]
    #target_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s ' %iso_cuts
    #target_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_chIsoCorr[1]< 5 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3  ' %iso_cuts
    #target_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3  ' %iso_cuts
    target_sample = 'Data'
    #target_sample = 'WjetsWgamma'

    #binning = [0.0, 0.003, 0.005, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013 , 0.015, 0.03]

    etacuts = ['ph_IsEB[0] ' , 'ph_IsEE[0]']

    manual_signal_cuts = [ ( 0.008, 0.011 ), (0.02, 0.035) ]
    manual_bkg_cuts = [ (0.015, 0.03), ( 0.045, 0.06 ) ]
    fit_ranges = [( 0.008, 0.018 ), (0.015, 0.05) ]
    binning = [(30, 0, 0.03), (20, 0, 0.1)]

    #manual_signal_cuts = [ ( 0.00, 1.5 ), ( 0.0, 1.2 ) ]
    #manual_bkg_cuts = [ ( 3, 50 ), ( 3, 50 ) ]
    #fit_ranges = [( 0.0, 10), (0.0, 10) ]
    #binning = [(50, 0, 50), (50, 0, 50)]

    
    var='ph_sigmaIEIE[0]'
    #var = 'ph_chIsoCorr[0]'

    for tb in target_bases :
        for ec, binn, sig_cuts, bkg_cuts, fit_range in zip(etacuts, binning, manual_signal_cuts, manual_bkg_cuts, fit_ranges ) :
            signal_selection = ' PUWeight * ( %s && %s ) ' %( signal_base, ec ) 
            bkg_selection    = ' PUWeight * ( %s && %s ) ' %( bkg_base   , ec ) 
            target_selection = ' PUWeight * ( %s && %s ) ' %( tb, ec ) 
            get_hists_and_fit( var, signal_selection, bkg_selection, target_selection, signal_sample, bkg_sample, target_sample, binn, fit_range, sig_cuts, bkg_cuts )

    #for idx, min in enumerate( ptcuts[0:-1] ) :
    #    max = ptcuts[idx+1]
    #    for ec, binn, sig_cuts, bkg_cuts, fit_range in zip(etacuts, binning, manual_signal_cuts, manual_bkg_cuts, fit_ranges ) :
    #        signal_selection = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( signal_base, min, max, ec ) 
    #        bkg_selection    = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( bkg_base   , min, max, ec ) 
    #        target_selection = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( target_base, min, max, ec ) 

    #        get_hists_and_fit( var, signal_selection, bkg_selection, target_selection, signal_sample, bkg_sample, target_sample, binn, fit_range, sig_cuts, bkg_cuts )

def DoDiPhotonSIEIETemplateFitSimple( outputDir=None) :

    #iso_cuts_lead = '&& ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    #iso_cuts_lead = '&& ph_passChIsoCorrMedium[0] && ph_pfChIsoWorst[0] < 3'
    #iso_cuts_lead = '&& ph_chIsoCorr[0]< 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 '
    iso_cuts_lead = ''
    #iso_cuts_subl = ''
    iso_cuts_subl = ' && ph_chIsoCorr[1]< 5 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3 '
    #iso_cuts_subl = ' && ' +  iso_cuts_lead.replace('[0]', '[1]' ) 
    #iso_cuts_lead += ' && ph_pt[0]>20 '
    #iso_cuts_subl += ' && ph_pt[1]>20 '

    #iso_cuts_single = iso_cuts_lead
    iso_cuts_single = iso_cuts_subl.replace('[1]','[0]')

    #signal_base = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 %s && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4' %iso_cuts_single
    #signal_sample = 'Data'
    signal_base = 'mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 %s && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 ' % iso_cuts_single
    signal_sample = 'Wgamma'

    bkg_base = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %iso_cuts_single
    #bkg_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 %s && leadPhot_leadLepDR>1 ' %iso_cuts_single
    #bkg_base = ' ph_n==2 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && ph_eleVeto[1]==0 && ph_HoverE12[1] < 0.05 %s %s  ' %(iso_cuts_lead, iso_cuts_subl)

    #bkg_sample = 'jetmon'
    bkg_sample = 'DataRealPhotonZgSub'
    #bkg_sample = 'DataRealPhotonWgSub'
    #bkg_sample = 'Zgammastar'

    target_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 %s && ph_HoverE12[1] < 0.05 %s' %(iso_cuts_lead, iso_cuts_subl )

    xf_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 %s && ph_HoverE12[1] < 0.05 %s ' %(iso_cuts_lead, iso_cuts_subl)

    fx_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 %s && ph_HoverE12[1] < 0.05 %s ' %(iso_cuts_lead, iso_cuts_subl)

    fr_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 %s && ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 %s ' %(iso_cuts_lead, iso_cuts_subl )

    rf_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 %s && ph_passSIEIEMedium[0] && !ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 %s ' %(iso_cuts_lead, iso_cuts_subl)

    #ff_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 %s && !ph_passSIEIEMedium[1] && !ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 %s ' %(iso_cuts_lead, iso_cuts_subl )
    ff_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 %s &&  ph_HoverE12[1] < 0.05 %s ' %(iso_cuts_lead, iso_cuts_subl )
    target_sample = 'Data'
    #target_sample = 'WjetsWgamma'

    binning_eb = (30, 0, 0.03)
    binning_ee = (20, 0, 0.1)
    binning_eb_ee = ( 50, 0, 0.1 )
    binning_var_eb = [0, 0.011, 0.013, 0.03]
    #binning_var_eb = [0, 0.011, 0.03]
    binning_var_ee = [0, 0.033, 0.04, 0.1]
    binning_var_eb_ee = [0, 0.011, 0.013, 0.03]

    sig_cuts_eb    = [(0    , 0.011 )]*2
    bkg_cuts_eb    = [(0.01301, 0.299   )]*2
    #bkg_cuts_eb    = [(0.01401, 0.299   )]*2
    #bkg_cuts_eb    = [(0.01101, 0.299   )]*2
    sig_cuts_ee    = [(0    , 0.033 )]*2
    bkg_cuts_ee    = [(0.045 , 0.1   )]*2
    sig_cuts_eb_ee = [( 0, 0.033     ), (0    , 0.011 )]
    bkg_cuts_eb_ee = [(0.04, 0.1 ), (0.013, 0.3   )]

    mult_bkg_cuts_eb  = [ [(0.01101, 0.299   )]*2, [(0.01201, 0.299   )]*2, [(0.01301, 0.299   )]*2, [(0.01401, 0.299   )]*2, [(0.01501, 0.299   )]*2 ]

    sig_bins_eb=[1, 1]
    bkg_bins_eb=[3, 3]
    sig_bins_ee=[1, 1]
    bkg_bins_ee=[3, 3]
    sig_bins_eb_ee=[1, 1]
    bkg_bins_eb_ee=[3, 3]

    outputDirVarBins = None
    if outputDir is not None :
        outputDirVarBins = outputDir+'VarBins'

    #for bkg_cut in mult_bkg_cuts_eb :
    #    fit_diphoton_simple( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_eb, ['EB','EB'], sig_cut=sig_cuts_eb, bkg_cut=bkg_cut, outputDir=outputDir )

    fit_diphoton_simple( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_eb, ['EB','EB'], sig_cut=sig_cuts_eb, bkg_cut=bkg_cuts_eb, outputDir=outputDir )
    #fit_diphoton_simple( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_var_eb, ['EB', 'EB'], sig_bins=sig_bins_eb, bkg_bins=bkg_bins_eb, outputDir=outputDirVarBins)
    #fit_diphoton_simple( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_eb_ee, ['EB','EE'], sig_cut=sig_cuts_eb_ee, bkg_cut=bkg_cuts_eb_ee, outputDir=outputDir )
    #fit_diphoton_simple( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_var_eb_ee, ['EB', 'EE'], sig_bins=sig_bins_eb_ee, bkg_bins=bkg_bins_eb_ee, outputDir=outputDirVarBins)
    fit_diphoton_simple( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_ee, ['EE','EE'], sig_cut=sig_cuts_ee, bkg_cut=bkg_cuts_ee, outputDir=outputDir )
    #fit_diphoton_simple( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_var_ee, ['EE', 'EE'], sig_bins=sig_bins_ee, bkg_bins=bkg_bins_ee, outputDir=outputDirVarBins)

def DoDiPhotonSIEIETemplateFit( outputDir=None) :

    #iso_cuts_lead = '!ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    iso_cuts_lead = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    #iso_cuts_lead = 'ph_chIsoCorr[0]< 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 '
    iso_cuts_subl = iso_cuts_lead.replace('[0]', '[1]' ) 
    #iso_cuts_lead += ' && ph_pt[0]>40 '

    #signal_base = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4' %iso_cuts_lead
    #signal_sample = 'Data'
    signal_base = 'mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 ' % iso_cuts_lead
    signal_sample = 'Wgamma'

    bkg_base = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %iso_cuts_lead
    #bkg_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s && leadPhot_leadLepDR>1 ' %iso_cuts_lead

    bkg_sample = 'DataRealPhotonZgSub'
    #bkg_sample = 'DataRealPhotonWgSub'
    #bkg_sample = 'Zgammastar'

    target_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && ph_HoverE12[1] < 0.05 && %s' %(iso_cuts_lead, iso_cuts_subl )

    xf_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl)

    fx_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl)

    fr_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[0] && ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl )

    rf_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && ph_passSIEIEMedium[0] && !ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl)

    ff_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[1] && !ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl )
    target_sample = 'Data'
    #target_sample = 'WjetsWgamma'

    #binning = [0.0, 0.003, 0.005, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013 , 0.015, 0.03]


    #samples.CompareSelections( 'ph_sigmaIEIE[0]', [signal_selection, bkg_selection, target_selection], [signal_sample, bkg_sample, target_sample], binning, normalize=1 )
    #raw_input('continue')

    #x = ROOT.RooRealVar('x','x',-10,10) ;
    #mean_bkg  = ROOT.RooRealVar  ('mean_bkg','mean',0,-10,10) ; 
    #sigma_bkg = ROOT.RooRealVar  ('sigma_bkg','sigma',2,0.,10.) ;
    #fpeak = ROOT.RooRealVar ('fpeak','peaking background fraction',0.1,0.,1.) ; 
    #bkg_peak = ROOT.RooGaussian ('bkg_peak','peaking bkg p.d.f.',x,mean_bkg,sigma_bkg) 
    #bkg_peak2 = ROOT.RooGaussian ('bkg_peak2','peaking bkg p.d.f.',x,mean_bkg,sigma_bkg) 
    #sigpeak = ROOT.RooAddPdf('sigpeak','sig + peak',ROOT.RooArgList(bkg_peak,bkg_peak2),ROOT.RooArgList(fpeak)) ; 
    #sigpeak.Print()

    ptcuts = [15, 20, 25, 30, 40, 60, 90, 1000000]
    #sieiecuts = ' && ( (ph_sigmaIEIE[0] > 0.008 && ph_sigmaIEIE[0] < 0.011 ) ||( ph_sigmaIEIE[0] > 0.015  && ph_sigmaIEIE[0] < 0.03 ) ) '
    etacuts = ['ph_IsEB[0] ' , 'ph_IsEE[0]']
    fit_ranges = [( 0.008, 0.018 ), (0.02, 0.04) ]
    #binning = [(30, 0, 0.03), (20, 0, 0.1)]
    binning_eb = (60, -0.03, 0.03)
    binning_ee = (39,  -0.099, 0.099)
    binning_eb_ee = ( 100, -0.1, 0.1 )
    binning_var_eb = [-0.03, -0.013, -0.011,0, 0.011, 0.013, 0.03]
    #binning_var_eb = [-0.03,  -0.011,0, 0.011, 0.03]
    binning_var_ee = [-0.1, -0.04, -0.033, 0, 0.033, 0.04, 0.1]
    binning_var_eb_ee = [-0.1, -0.04, -0.033, 0, 0.011, 0.013, 0.03]

    sig_cuts_eb    = [( -0.011, 0     ), (0    , 0.011 )]
    bkg_cuts_eb    = [( -0.299  , -0.01301), (0.01301, 0.299   )]
    #bkg_cuts_eb    = [( -0.299  , -0.01401), (0.01401, 0.299   )]
    #bkg_cuts_eb    = [( -0.299  , -0.01101), (0.01101, 0.299   )]
    sig_cuts_ee    = [( -0.033, 0     ), (0    , 0.033 )]
    bkg_cuts_ee    = [( -0.1  , -0.04 ), (0.04 , 0.1   )]
    sig_cuts_eb_ee = [( -0.033, 0     ), (0    , 0.011 )]
    bkg_cuts_eb_ee = [( -0.1  , -0.04 ), (0.013, 0.3   )]

    sig_bins_eb=[3, 4]
    bkg_bins_eb=[1, 6]
    #sig_bins_eb=[2, 3]
    #bkg_bins_eb=[1, 4]
    sig_bins_ee=[3, 4]
    bkg_bins_ee=[1, 6]
    sig_bins_eb_ee=[3, 4]
    bkg_bins_eb_ee=[1, 6]

    outputDirVarBins = None
    if outputDir is not None :
        outputDirVarBins = outputDir+'VarBins'
    fit_diphoton( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_eb, ['EB','EB'], sig_cut=sig_cuts_eb, bkg_cut=bkg_cuts_eb, outputDir=outputDir )
    #fit_diphoton( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_var_eb, ['EB', 'EB'], sig_bins=sig_bins_eb, bkg_bins=bkg_bins_eb, outputDir=outputDirVarBins)
    #fit_diphoton( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_eb_ee, ['EB','EE'], sig_cut=sig_cuts_eb_ee, bkg_cut=bkg_cuts_eb_ee, outputDir=outputDir )
    #fit_diphoton( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_var_eb_ee, ['EB', 'EE'], sig_bins=sig_bins_eb_ee, bkg_bins=bkg_bins_eb_ee, outputDir=outputDirVarBins)
    fit_diphoton( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_ee, ['EE','EE'], sig_cut=sig_cuts_ee, bkg_cut=bkg_cuts_ee, outputDir=outputDir )
    fit_diphoton( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_var_ee, ['EE', 'EE'], sig_bins=sig_bins_ee, bkg_bins=bkg_bins_ee, outputDir=outputDirVarBins)


    #for idx, min in enumerate( ptcuts[0:-1] ) :
    #    max = ptcuts[idx+1]
    #    for ec, binn, sig_cuts, bkg_cuts, fit_range in zip(etacuts, binning, manual_signal_cuts, manual_bkg_cuts, fit_ranges ) :
    #        signal_selection = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( signal_base, min, max, ec ) 
    #        bkg_selection    = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( bkg_base   , min, max, ec ) 
    #        target_selection = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( target_base, min, max, ec ) 

    #        fit_diphoton( signal_selection, bkg_selection, target_selection, signal_sample, bkg_sample, target_sample, binn, fit_range, sig_cuts, bkg_cuts )

def DoDiPhoton2DSIEIETemplateFit() :

    #signal_base = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4'
    #signal_sample = 'Data'
    signal_base = 'mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25'
    signal_sample = 'Wgamma'

    #bkg_base =  ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 '
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < m 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_phoIsoCorr[0] > 2 && ph_phoIsoCorr[0] < 4   '
    bkg_base = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 '
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_passChIsoCorrMedium[0] '
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && ph_passChIsoCorrMedium[0] '
    #bkg_base =  ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && !( ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25) '

    bkg_sample = 'DataRealPhotonSub'
    #bkg_sample = 'Zgammastar'

    sig_template_hist = None
    bkg_template_hist = None

    signal_selection = ' PUWeight * ( %s && ph_IsEB[0] ) ' %( signal_base ) 
    bkg_selection    = ' PUWeight * ( %s && ph_IsEB[0]) ' %( bkg_base    ) 

    binning = (30, 0, 0.03)
    binning2d = ( 30, 0, 0.03, 30, 0, 0.03 )
    #binning2d = ( [0, 0.011, 0.03], [0, 0.011, 0.03] )

    sig_template_samp = samples.get_samples(name=signal_sample )
    sig_list = []
    bkg_list = []
    templateff1d = None

    if sig_template_samp :
        sig_list = samples.get_list_from_tree( 'ph_sigmaIEIE[0]', signal_selection, sig_template_samp[0] )

    bkg_template_samp = samples.get_samples(name=bkg_sample)
    if bkg_template_samp :
        bkg_list = samples.get_list_from_tree( 'ph_sigmaIEIE[0]', bkg_selection , bkg_template_samp[0] )
        newFF1DSamp    = samples.clone_sample( oldname=bkg_template_samp[0].name, newname='FF1d', temporary=True)
        samples.create_hist(newFF1DSamp, 'ph_sigmaIEIE[0]',bkg_selection, binning  )
        templateff1d = newFF1DSamp.hist

    rr_2dlist = []
    ff_2dlist = []
    rf_2dlist = []
    fr_2dlist = []
    for ent in sig_list :
        rndm_sig_idx = random.randrange( 0, len( sig_list) )
        rndm_bkg_idx = random.randrange( 0, len( bkg_list) )
        rr_2dlist.append( (ent[0], sig_list[rndm_sig_idx][0], ent[1]* sig_list[rndm_sig_idx][1]) )
        rf_2dlist.append( (ent[0], bkg_list[rndm_bkg_idx][0], ent[1]*bkg_list[rndm_bkg_idx][1]) )
    for ent in bkg_list :
        rndm_sig_idx = random.randrange( 0, len( sig_list) )
        rndm_bkg_idx = random.randrange( 0, len( bkg_list) )
        ff_2dlist.append( (ent[0], bkg_list[rndm_bkg_idx][0], ent[1]*bkg_list[rndm_bkg_idx][1]) )
        fr_2dlist.append( (ent[0], sig_list[rndm_sig_idx][0], ent[1]*sig_list[rndm_sig_idx][1]) )

    c1 = ROOT.TCanvas( 'c1', 'c1' )
    if len( binning2d ) == 6 :
        templaterr = ROOT.TH2F( 'templaterr', '', binning2d[0], binning2d[1], binning2d[2], binning2d[3], binning2d[4], binning2d[5] )
    else :
        templaterr = ROOT.TH2F( 'templaterr', '', len(binning2d[0])-1, array('f', binning2d[0]), len(binning2d[1])-1, array('f', binning2d[1])  )
    for ph1, ph2, wt in rr_2dlist :
        templaterr.Fill( ph1, ph2, wt)

    templaterr.Draw('colz')

    c2 = ROOT.TCanvas( 'c2', 'c2' )
    if len( binning2d ) == 6 :
        templateff = ROOT.TH2F( 'templateff', '', binning2d[0], binning2d[1], binning2d[2], binning2d[3], binning2d[4], binning2d[5] )
    else :
        templateff = ROOT.TH2F( 'templateff', '', len(binning2d[0])-1, array('f', binning2d[0]), len(binning2d[1])-1, array('f', binning2d[1])  )
    for ph1, ph2, wt in ff_2dlist :
        templateff.Fill( ph1, ph2, wt)

    templateff.Draw('colz')

    c3 = ROOT.TCanvas( 'c3', 'c3' )
    if len( binning2d ) == 6 :
        templaterf = ROOT.TH2F( 'templaterf', '', binning2d[0], binning2d[1], binning2d[2], binning2d[3], binning2d[4], binning2d[5] )
    else :
        templaterf = ROOT.TH2F( 'templaterf', '', len(binning2d[0])-1, array('f', binning2d[0]), len(binning2d[1])-1, array('f', binning2d[1])  )
    for ph1, ph2, wt in rf_2dlist :
        templaterf.Fill( ph1, ph2, wt)

    templaterf.Draw('colz')

    c4 = ROOT.TCanvas( 'c4', 'c4' )
    if len( binning2d ) == 6 :
        templatefr = ROOT.TH2F( 'templatefr', '', binning2d[0], binning2d[1], binning2d[2], binning2d[3], binning2d[4], binning2d[5] )
    else :
        templatefr = ROOT.TH2F( 'templatefr', '', len(binning2d[0])-1, array('f', binning2d[0]), len(binning2d[1])-1, array('f', binning2d[1])  )
    for ph1, ph2, wt in fr_2dlist :
        templatefr.Fill( ph1, ph2, wt)

    templatefr.Draw('colz')

    
    raw_input('continue')

    
    #target_base = ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && mt_lep_met > 60 )'
    target_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    #rf_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    #fr_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    rf_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && !ph_passSIEIEMedium[1] && ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    fr_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && !ph_passSIEIEMedium[0] && ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    ff_cr_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && !ph_passSIEIEMedium[1] && !ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    target_sample = 'Data'
    #target_sample = 'WjetsWgamma'

    target_selection = ' PUWeight * ( %s && ph_IsEB[0] && ph_IsEB[1]) ' %( target_base ) 
    rf_cr_selection  = ' PUWeight * ( %s && ph_IsEB[0] && ph_IsEB[1]) ' %( rf_cr_base ) 
    fr_cr_selection  = ' PUWeight * ( %s && ph_IsEB[0] && ph_IsEB[1]) ' %( fr_cr_base ) 
    ff_cr_selection  = ' PUWeight * ( %s && ph_IsEB[0] && ph_IsEB[1]) ' %( ff_cr_base ) 

    target_hist = None
    rf_cr_hist = None
    fr_cr_hist = None
    ff_cr_hist = None
    ff_cr_hist1d = None

    target_samp = samples.get_samples(name=target_sample)
    if target_samp :
        newTargetSamp    = samples.clone_sample( oldname=target_samp[0].name, newname='DataTarget', temporary=True)
        samples.create_hist(newTargetSamp , 'ph_sigmaIEIE[1]:ph_sigmaIEIE[0]',target_selection , binning2d  )
        target_hist = newTargetSamp.hist

        newRFCRSamp    = samples.clone_sample( oldname=target_samp[0].name, newname='DataRFCR', temporary=True)
        samples.create_hist(newRFCRSamp , 'ph_sigmaIEIE[1]:ph_sigmaIEIE[0]', rf_cr_selection, binning2d  )
        rf_cr_hist = newRFCRSamp.hist

        newFRCRSamp    = samples.clone_sample( oldname=target_samp[0].name, newname='DataFRCR', temporary=True)
        samples.create_hist(newFRCRSamp , 'ph_sigmaIEIE[1]:ph_sigmaIEIE[0]', fr_cr_selection, binning2d  )
        fr_cr_hist = newFRCRSamp.hist

        newFFCRSamp    = samples.clone_sample( oldname=target_samp[0].name, newname='DataFFCR', temporary=True)
        samples.create_hist(newFFCRSamp , 'ph_sigmaIEIE[1]:ph_sigmaIEIE[0]', ff_cr_selection, binning2d  )
        ff_cr_hist = newFFCRSamp.hist
        newFFCRSamp1d    = samples.clone_sample( oldname=target_samp[0].name, newname='DataFFCR1d', temporary=True)
        samples.create_hist(newFFCRSamp1d , 'ph_sigmaIEIE[0]', ff_cr_selection, binning  )
        ff_cr_hist1d = newFFCRSamp1d.hist

    c1.cd()
    target_hist.Draw('colz')
    c2.cd()
    rf_cr_hist.Draw('colz')
    c3.cd()
    fr_cr_hist.Draw('colz')
    c4.cd()
    ff_cr_hist.Draw('colz')

    raw_input('continue')

    xbinmin = target_hist.GetXaxis().FindBin( 0.011 )
    xbinmax = target_hist.GetXaxis().FindBin( 0.03  )
    ybinmin = target_hist.GetYaxis().FindBin( 0.011 )
    ybinmax = target_hist.GetYaxis().FindBin( 0.03  )

    print 'BIN CHECK'
    print target_hist.GetXaxis().FindBin( 0.011  )
    print target_hist.GetXaxis().FindBin( 0.01099999  )
    print target_hist.GetXaxis().FindBin( 0.01100001  )

    print 'ff template bins'
    print '1,1, = %f' %( templateff.GetBinContent(xbinmin, ybinmin) )
    print '1,2, = %f' %( templateff.GetBinContent(xbinmin, ybinmin) )
    print '2,1, = %f' %( templateff.GetBinContent(xbinmin, ybinmin) )
    print '2,2, = %f' %( templateff.GetBinContent(xbinmin, ybinmin) )

    print 'ff CR bins'
    print '1,1, = %f' %( ff_cr_hist.GetBinContent(1, 1) )
    print '1,2, = %f' %( ff_cr_hist.GetBinContent(1, 2) )
    print '2,1, = %f' %( ff_cr_hist.GetBinContent(2, 1) )
    print '2,2, = %f' %( ff_cr_hist.GetBinContent(2, 2) )

    print 'fr template bins'
    print '1,1, = %f' %( templatefr.GetBinContent(1, 1) )
    print '1,2, = %f' %( templatefr.GetBinContent(1, 2) )
    print '2,1, = %f' %( templatefr.GetBinContent(2, 1) )
    print '2,2, = %f' %( templatefr.GetBinContent(2, 2) )

    print 'fr CR bins'
    print '1,1, = %f' %( fr_cr_hist.GetBinContent(1, 1) )
    print '1,2, = %f' %( fr_cr_hist.GetBinContent(1, 2) )
    print '2,1, = %f' %( fr_cr_hist.GetBinContent(2, 1) )
    print '2,2, = %f' %( fr_cr_hist.GetBinContent(2, 2) )

    print 'rf template bins'
    print '1,1, = %f' %( templaterf.GetBinContent(1, 1) )
    print '1,2, = %f' %( templaterf.GetBinContent(1, 2) )
    print '2,1, = %f' %( templaterf.GetBinContent(2, 1) )
    print '2,2, = %f' %( templaterf.GetBinContent(2, 2) )

    print 'rf CR bins'
    print '1,1, = %f' %( rf_cr_hist.GetBinContent(1, 1) )
    print '1,2, = %f' %( rf_cr_hist.GetBinContent(1, 2) )
    print '2,1, = %f' %( rf_cr_hist.GetBinContent(2, 1) )
    print '2,2, = %f' %( rf_cr_hist.GetBinContent(2, 2) )

    ff_fit = [(templateff, 1)] 
    ff_norm = do_manual_fit( ff_cr_hist, ff_fit, xrange=(0.011, 0.03), yrange=(0.011, 0.03) )
    #ff_norm = do_manual_fit( ff_cr_hist, ff_fit, xrange=2, yrange=2 )

    rf_fit = [(templaterf, 1), (templateff, -1*ff_norm) ]
    rf_norm = do_manual_fit( rf_cr_hist, rf_fit, xrange=(0.0, 0.011), yrange=(0.011, 0.03) )
    #rf_norm = do_manual_fit( rf_cr_hist, rf_fit, xrange=1, yrange=2) 

    fr_fit = [(templatefr, 1), (templateff, -1*ff_norm) ]
    fr_norm = do_manual_fit( fr_cr_hist, fr_fit, xrange=(0.011, 0.03), yrange=(0.0, 0.011) )
    #fr_norm = do_manual_fit( fr_cr_hist, fr_fit, xrange=2, yrange=1 )



    print 'ff_norm = %f' %( ff_norm )
    print 'rf_norm = %f' %( rf_norm )
    print 'fr_norm = %f' %( fr_norm )


    templateff.Scale( ff_norm );
    templaterf.Scale( rf_norm );
    templatefr.Scale( fr_norm );

    print 'predicted ff = %f' %( templateff.Integral( templateff.GetXaxis().FindBin( 0.0 ),  templateff.GetXaxis().FindBin( 0.011 ),templateff.GetYaxis().FindBin( 0.0 ),  templateff.GetYaxis().FindBin( 0.011 ) ) )
    print 'predicted rf = %f' %( templaterf.Integral( templaterf.GetXaxis().FindBin( 0.0 ),  templaterf.GetXaxis().FindBin( 0.011 ),templaterf.GetYaxis().FindBin( 0.0 ),  templaterf.GetYaxis().FindBin( 0.011 ) ) )
    print 'predicted fr = %f' %( templatefr.Integral( templatefr.GetXaxis().FindBin( 0.0 ),  templatefr.GetXaxis().FindBin( 0.011 ),templatefr.GetYaxis().FindBin( 0.0 ),  templatefr.GetYaxis().FindBin( 0.011 ) ) )

    templatesum = templateff.Clone( 'templatesum' )
    templatesum.Add( templaterf )
    templatesum.Add( templatefr )

    templateff_px = templateff.ProjectionX('tempffpx')
    templateff_py = templateff.ProjectionY('tempffpy')

    c1.cd()
    templateff1d.DrawNormalized()
    templateff_px.DrawNormalized('same')
    raw_input('1d check')
    templateff_px_ff = templateff.ProjectionX('tempffpxff', ybinmin, ybinmax)
    templateff_py_ff = templateff.ProjectionY('tempffpyff', xbinmin, xbinmax)
    templateff_px_rf = templateff.ProjectionX('tempffpxrf', 0, ybinmin)
    templateff_py_rf = templateff.ProjectionY('tempffpyrf', xbinmin, xbinmax)
    templateff_px_fr = templateff.ProjectionX('tempffpxfr', ybinmin, ybinmax)
    templateff_py_fr = templateff.ProjectionY('tempffpyfr', 0, xbinmin)
    templateff_px_rr = templateff.ProjectionX('tempffpxrr', 0, ybinmin)
    templateff_py_rr = templateff.ProjectionY('tempffpyrr', 0, xbinmin)

    templaterf_px_ff = templaterf.ProjectionX('temprfpxff', ybinmin, ybinmax)
    templaterf_py_ff = templaterf.ProjectionY('temprfpyff', xbinmin, xbinmax)
    templaterf_px_rf = templaterf.ProjectionX('temprfpxrf', ybinmin, ybinmax)
    templaterf_py_rf = templaterf.ProjectionY('temprfpyrf', 0, xbinmin)
    templaterf_px_fr = templaterf.ProjectionX('temprfpxrf', ybinmin, ybinmax)
    templaterf_py_fr = templaterf.ProjectionY('temprfpyrf', 0, xbinmin)
    templaterf_px_rr = templaterf.ProjectionX('temprfpxrr', 0, ybinmin)
    templaterf_py_rr = templaterf.ProjectionY('temprfpyrr', 0, xbinmin)

    templatefr_px_ff = templatefr.ProjectionX('temprfpxfr', ybinmin, ybinmax)
    templatefr_py_ff = templatefr.ProjectionY('temprfpyfr', xbinmin, xbinmax)
    templatefr_px_rf = templatefr.ProjectionX('temprfpxfr', 0, ybinmin)
    templatefr_py_rf = templatefr.ProjectionY('temprfpyfr', xbinmin, xbinmax)
    templatefr_px_fr = templatefr.ProjectionX('temprfpxfr', ybinmin, ybinmax)
    templatefr_py_fr = templatefr.ProjectionY('temprfpyfr', 0, xbinmin)
    templatefr_px_rr = templatefr.ProjectionX('temprfpxfr', 0, ybinmin)
    templatefr_py_rr = templatefr.ProjectionY('temprfpyfr', 0, xbinmin)

    #templaterf_px = templaterf.ProjectionX('temprfpx')
    #templaterf_py = templaterf.ProjectionY('temprfpy')
    #templatefr_px = templatefr.ProjectionX('tempfrpx')
    #templatefr_py = templatefr.ProjectionY('tempfrpy')

    target_px = target_hist.ProjectionX( 'targetpx' )
    target_py = target_hist.ProjectionY( 'targetpy' )

    rf_cr_px = rf_cr_hist.ProjectionX( 'rfcrpx', ybinmin, ybinmax )
    rf_cr_py = rf_cr_hist.ProjectionY( 'rfcrpy', 0, xbinmin )
    fr_cr_px = fr_cr_hist.ProjectionX( 'frcrpx', ybinmin, ybinmax)
    fr_cr_py = fr_cr_hist.ProjectionY( 'frcrpy', 0, xbinmin )

    ff_cr_px = ff_cr_hist.ProjectionX( 'ffcrpx', ybinmin, ybinmax )
    ff_cr_py = ff_cr_hist.ProjectionY( 'ffcrpy', xbinmin, xbinmax )

    templateff.SetLineColor( ROOT.kRed )
    templateff.SetLineStyle( ROOT.kDashed )
    templateff.SetLineWidth( 2 )
    templaterf.SetLineColor( ROOT.kMagenta )
    templaterf.SetLineStyle( ROOT.kDashed )
    templaterf.SetLineWidth( 2 )
    templatefr.SetLineColor( ROOT.kGreen )
    templatefr.SetLineStyle( ROOT.kDashed )
    templatefr.SetLineWidth( 2 )

    #templateff_px.SetLineColor( ROOT.kRed )
    #templateff_px.SetLineStyle( ROOT.kDashed )
    #templateff_px.SetLineWidth( 2 )
    #templateff_py.SetLineColor( ROOT.kRed )
    #templateff_py.SetLineStyle( ROOT.kDashed )
    #templateff_py.SetLineWidth( 2 )

    #templaterf_px.SetLineColor( ROOT.kMagenta )
    #templaterf_px.SetLineStyle( ROOT.kDashed )
    #templaterf_px.SetLineWidth( 2 )
    #templaterf_py.SetLineColor( ROOT.kMagenta )
    #templaterf_py.SetLineStyle( ROOT.kDashed )
    #templaterf_py.SetLineWidth( 2 )

    #templatefr_px.SetLineColor( ROOT.kGreen )
    #templatefr_px.SetLineStyle( ROOT.kDashed )
    #templatefr_px.SetLineWidth( 2 )
    #templatefr_py.SetLineColor( ROOT.kGreen )
    #templatefr_py.SetLineStyle( ROOT.kDashed )
    #templatefr_py.SetLineWidth( 2 )

    sum_px = templatesum.ProjectionX( 'sum_px' )
    sum_py = templatesum.ProjectionY( 'sum_py' )

    sum_px.SetLineWidth( 3 )
    sum_px.SetLineStyle( ROOT.kSolid )
    sum_py.SetLineColor( ROOT.kBlue )
    sum_py.SetLineWidth( 3 )
    sum_py.SetLineStyle( ROOT.kSolid )

    c0 = ROOT.TCanvas( 'c0', 'c0' )

    #c0.cd()
    #ff_cr_py.Draw()
    #templateff_py_ff.Draw('samehist')

    c0.cd()
    ff_cr_px.Draw()
    templateff_px_ff.Draw('samehist')

    c1.cd()
    rf_cr_px.Draw()
    templateff_px_rf.SetLineColor(ROOT.kRed)
    templaterf_px_rf.SetLineColor(ROOT.kBlue)
    templateff_px_rf.Draw('samehist')
    templaterf_px_rf.Draw('samehist')

    c2.cd()
    rf_cr_py.Draw()
    templateff_py_rf.SetLineColor(ROOT.kRed)
    templaterf_py_rf.SetLineColor(ROOT.kBlue)
    templateff_py_rf.Draw('samehist')
    templaterf_py_rf.Draw('samehist')


    print 'X projection'
    c3.cd()

    #target_px.Draw()
    #sum_px.Draw('samehist')
    #templateff_px.Draw('samehist')
    #templaterf_px.Draw('samehist')
    #templatefr_px.Draw('samehist')

    #print 'Y projection'
    #c4.cd()

    #target_py.Draw()
    #sum_py.Draw('samehist')
    #templateff_py.Draw('samehist')
    #templaterf_py.Draw('samehist')
    #templatefr_py.Draw('samehist')


    raw_input('continue')

def do_manual_fit( target, fit_inputs, xrange, yrange=None ) :

    n_target = 0
    n_primfit = 0
    n_bkgfit = 0

    if isinstance( xrange, tuple ) :
        xbinmin = target.GetXaxis().FindBin( xrange[0] )
        xbinmax = target.GetXaxis().FindBin( xrange[1] )
    else :
        xbinmin = xrange
        xbinmax = xrange
        
    print 'x bin min, max = %d, %d' %( xbinmin, xbinmax )
    if yrange is not None :
        if isinstance( yrange, tuple ) :
            ybinmin = target.GetYaxis().FindBin( yrange[0] )
            ybinmax = target.GetYaxis().FindBin( yrange[1] )
        else :
            ybinmin = yrange
            ybinmax = yrange
        print 'y bin min, max = %d, %d' %( ybinmin, ybinmax )

        n_target = target.Integral( xbinmin, xbinmax, ybinmin, ybinmax )
        #n_target_c = target.GetBinContent( xbinmin, ybinmin )
        n_primfit = fit_inputs[0][1]*fit_inputs[0][0].Integral( xbinmin, xbinmax, ybinmin, ybinmax  )
        #n_primfit_c = fit_inputs[0][1]*fit_inputs[0][0].GetBinContent( xbinmin, ybinmin  )
        n_bkgfit_c = 0
        for hist, scale in fit_inputs[1:] :
            n_bkgfit += scale*hist.Integral( xbinmin, xbinmax, ybinmin, ybinmax )
            n_bkgfit_c += scale*hist.GetBinContent( xbinmin, ybinmin )
        print 'n_target, n_primfit, n_bkgfit = %f, %f, %f' %( n_target, n_primfit, n_bkgfit )
        #print 'n_target, n_primfit, n_bkgfit = %f, %f, %f' %( n_target_c, n_primfit_c, n_bkgfit_c )
    else :
        n_target = target.Integral( xbinmin, xbinmax )
        n_primfit = fit_inputs[0][1]*fit_inputs[0][0].Integral( xbinmin, xbinmax  )
        for hist, scale in fit_inputs[1:] :
            n_bkgfit += scale*hist.Integral( xbinmin, xbinmax )

    return ( n_target + n_bkgfit )/n_primfit
        
def draw_template_with_axis(can, hists, normalize=False, first_hist_is_data=False, legend_entries=[], outputName=None, plot_lead_subl=True) :

    can.cd()

    added_sum_hist=False
    if len(hists) > 1 and not first_hist_is_data or len(hists)>2 and first_hist_is_data :
        if first_hist_is_data :
            hists_to_sum = hists[1:]
        else :
            hists_to_sum = hists

        sumhist = hists_to_sum[0].Clone( 'sumhist%s' %hists_to_sum[0].GetName)
        for h in hists_to_sum[1:] :
            sumhist.Add(h)

        sumhist.SetLineColor(ROOT.kBlue+1)
        sumhist.SetLineWidth(3)
        hists.append(sumhist)
        added_sum_hist=True

    #get y size
    maxbin = hists[0].GetBinContent(hists[0].GetMaximumBin())
    for h in hists[1: ] :
        if h.GetBinContent(h.GetMaximumBin() ) > maxbin :
            maxbin = h.GetBinContent(h.GetMaximumBin() )

    maxval_hist = maxbin * 1.25
    if normalize :
        maxval_axis = maxval_hist/hists[0].Integral()
    else :
        maxval_axis = maxval_hist
        
    for h in hists :        
        h.GetYaxis().SetRangeUser( 0, maxval_hist )

    drawcmd='A'
    if not first_hist_is_data :
        drawcmd += 'hist'

    if normalize :
        hists[0].DrawNormalized(drawcmd)
        drawcmd+='hist'
        for h in hists[1:] :
            h.DrawNormalized(drawcmd + 'same')
    else :
        hists[0].Draw(drawcmd)
        drawcmd+='hist'
        for h in hists[1:] :
            h.Draw(drawcmd + 'same')

    f1= ROOT.TF1('f1','-x',0,-1*hists[0].GetXaxis().GetXmin() );

    newxaxis_pos = ROOT.TGaxis(0 ,ROOT.gPad.GetUymin(), hists[0].GetXaxis().GetXmax() , ROOT.gPad.GetUymin(), 0,hists[0].GetXaxis().GetXmax() , 505, '+' )

    newxaxis_neg = ROOT.TGaxis(hists[0].GetXaxis().GetXmin()  , ROOT.gPad.GetUymin(),0, ROOT.gPad.GetUymin(), 'f1', 505, '+' )

    newxaxis_pos.SetTitle( '#sigma i#etai#eta ' )
    
    #newxaxis_neg.SetTitle( 'sublead photon #sigma i#etai#eta ' )

    newxaxis_pos.Draw()
    newxaxis_neg.Draw()


    #newyaxis = ROOT.TGaxis( 0,ROOT.gPad.GetUymin(),0, 1.0/hists[0].GetMaximum() , 0, hists[0].GetMaximum(), 520, '+-' )
    newyaxis = ROOT.TGaxis( 0,ROOT.gPad.GetUymin(),0  , maxval_axis,0, maxval_axis, 510, '+-' )
    newyaxis.SetTickSize(0.0)
    newyaxis.Draw()

    alabel =  'Events'
    axis_label_pos = 0.45
    if normalize :
        alabel = 'A.U.'
        axis_label_pos = 0.47

    subl_label = ROOT.TLatex( 0.0, 0.85, 'Sublead Photon' )
    lead_label = ROOT.TLatex( 0.7, 0.85, 'Lead Photon' )
    axis_label = ROOT.TLatex( 0.5, 0.92, alabel)
    lead_label.SetNDC()
    axis_label.SetNDC()
    subl_label.SetNDC()
    lead_label.SetX(0.7)
    lead_label.SetY(0.85)
    subl_label.SetX(0.12)
    subl_label.SetY(0.85)
    axis_label.SetX(axis_label_pos)
    axis_label.SetY(0.92)
    subl_label.Draw()
    lead_label.Draw()
    axis_label.Draw()

    leg=None
    if legend_entries :
        global samples
        leg = samples.create_standard_legend( len(hists) )
        if added_sum_hist :
            legend_entries.append( 'Template sum' )

        for ent, hist in zip( legend_entries, hists ) :
            leg.AddEntry( hist, ent )

        leg.Draw()
        
    raw_input('continue')

    if outputName is not None :
        if not os.path.isdir( os.path.dirname(outputName) ) :
            os.makedirs( os.path.dirname(outputName) )

        can.SaveAs( outputName )

    
def draw_template(can, hists, normalize=False, first_hist_is_data=False, legend_entries=[], outputName=None, plot_lead_subl=True) :

    can.cd()
    can.SetBottomMargin( 0.12 )
    can.SetLeftMargin( 0.12 )

    added_sum_hist=False
    if len(hists) > 1 and not first_hist_is_data or len(hists)>2 and first_hist_is_data :
        if first_hist_is_data :
            hists_to_sum = hists[1:]
        else :
            hists_to_sum = hists

        sumhist = hists_to_sum[0].Clone( 'sumhist%s' %hists_to_sum[0].GetName)
        for h in hists_to_sum[1:] :
            sumhist.Add(h)

        sumhist.SetLineColor(ROOT.kBlue+1)
        sumhist.SetLineWidth(3)
        hists.append(sumhist)
        added_sum_hist=True

    #get y size
    maxbin = hists[0].GetBinContent(hists[0].GetMaximumBin())
    for h in hists[1: ] :
        if h.GetBinContent(h.GetMaximumBin() ) > maxbin :
            maxbin = h.GetBinContent(h.GetMaximumBin() )

    maxval_hist = maxbin * 1.25
    if normalize :
        maxval_axis = maxval_hist/hists[0].Integral()
    else :
        maxval_axis = maxval_hist
        
    for h in hists :        
        h.GetYaxis().SetRangeUser( 0, maxval_hist )
        h.GetXaxis().SetTitleSize( 0.05 )
        h.GetXaxis().SetLabelSize( 0.05 )
        h.GetYaxis().SetTitleSize( 0.05 )
        h.GetYaxis().SetLabelSize( 0.05 )
        h.GetYaxis().SetTitleOffset( 1.15 )
        h.GetXaxis().SetTitle( '#sigma i#etai#eta' )
        h.SetLineWidth( 2 )
        bin_width = h.GetXaxis().GetBinWidth(1)

        if first_hist_is_data :
            h.GetYaxis().SetTitle( 'Events / %.3f ' %bin_width )
        else :
            h.GetYaxis().SetTitle( 'A.U. / %.3f ' %bin_width )

    drawcmd=''
    if not first_hist_is_data :
        drawcmd += 'hist'

    if normalize :
        hists[0].DrawNormalized(drawcmd)
        drawcmd+='hist'
        for h in hists[1:] :
            h.DrawNormalized(drawcmd + 'same')
    else :
        hists[0].Draw(drawcmd)
        drawcmd+='hist'
        for h in hists[1:] :
            h.Draw(drawcmd + 'same')

    leg=None
    if legend_entries :
        global samples
        samples.legendTranslateX = -0.1
        leg = samples.create_standard_legend( len(hists) )
        if added_sum_hist :
            legend_entries.append( 'Template sum' )

        for ent, hist in zip( legend_entries, hists ) :
            leg.AddEntry( hist, ent )

        leg.Draw()
        
    raw_input('continue')

    if outputName is not None :
        if not os.path.isdir( os.path.dirname(outputName) ) :
            os.makedirs( os.path.dirname(outputName) )

        can.SaveAs( outputName )

    

def fit_diphoton_simple( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning, position,  sig_cut=None, bkg_cut=None, sig_bins=None, bkg_bins=None, outputDir=None ) :

    global samples

    sig_selection = []
    bkg_selection    = []
    target_selection = []
    xf_cr_selection  = []
    fx_cr_selection  = []
    fr_cr_selection  = []
    rf_cr_selection  = []
    ff_cr_selection  = []

    if position[0] is not position[1] : #EB+EE
        print 'Doing EB+EE'

        sig_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEB[0] ) '    %( signal_base ) ) )
        sig_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) '    %( signal_base ) ) )
        bkg_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEB[0] ) '    %( bkg_base    ) ) )
        bkg_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) '    %( bkg_base    ) ) )
        
        #target_selection.append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( target_base ) ) )
        #target_selection.append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( target_base ) ) )
        #xf_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( xf_cr_base  ) ) ) 
        #xf_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( xf_cr_base  ) ) ) 
        #fx_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( fx_cr_base  ) ) ) 
        #fx_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( fx_cr_base  ) ) ) 
        #fr_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( fr_cr_base  ) ) ) 
        #fr_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( fr_cr_base  ) ) ) 
        #rf_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( rf_cr_base  ) ) ) 
        #rf_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( rf_cr_base  ) ) ) 
        #ff_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( ff_cr_base  ) ) ) 
        #ff_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( ff_cr_base  ) ) ) 

        #target_selection.append( ( 'ph_sigmaIEIE[0]   ', ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( target_base ) ) )
        #target_selection.append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( target_base ) ) )
        #xf_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( xf_cr_base  ) ) ) 
        #xf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( xf_cr_base  ) ) ) 
        #fx_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( fx_cr_base  ) ) ) 
        #fx_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( fx_cr_base  ) ) ) 
        #fr_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( fr_cr_base  ) ) ) 
        #fr_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( fr_cr_base  ) ) ) 
        #rf_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( rf_cr_base  ) ) ) 
        #rf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( rf_cr_base  ) ) ) 
        #ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( ff_cr_base  ) ) ) 
        #ff_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( ff_cr_base  ) ) ) 

        target_selection.append( ( 'ph_sigmaIEIE[0]   ', ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( target_base ) ) )
        #target_selection.append( ( 'ph_sigmaIEIE[1]   ', ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( target_base ) ) )
        #target_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( target_base ) ) )
        target_selection.append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( target_base ) ) )
        xf_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( xf_cr_base  ) ) ) 
        #xf_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( xf_cr_base  ) ) ) 
        #xf_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( xf_cr_base  ) ) ) 
        xf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( xf_cr_base  ) ) ) 
        fx_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( fx_cr_base  ) ) ) 
        #fx_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( fx_cr_base  ) ) ) 
        #fx_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( fx_cr_base  ) ) ) 
        fx_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( fx_cr_base  ) ) ) 
        fr_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( fr_cr_base  ) ) ) 
        #fr_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( fr_cr_base  ) ) ) 
        #fr_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( fr_cr_base  ) ) ) 
        fr_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( fr_cr_base  ) ) ) 
        rf_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( rf_cr_base  ) ) ) 
        #rf_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( rf_cr_base  ) ) ) 
        #rf_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( rf_cr_base  ) ) ) 
        rf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( rf_cr_base  ) ) ) 
        ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( ff_cr_base  ) ) ) 
        #ff_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( ff_cr_base  ) ) ) 
        #ff_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( ff_cr_base  ) ) ) 
        ff_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( ff_cr_base  ) ) ) 

    elif position[0] is 'EB' and position[1] is 'EB' :
        sig_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEB[0] ) ' %( signal_base ) ) )
        bkg_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEB[0] ) ' %( bkg_base    ) ) )

        pos_string = 'ph_IsEB[0] && ph_IsEB[1]'

        target_selection.append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s) ' %( target_base, pos_string ) ) )
        target_selection.append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( target_base, pos_string ) ) )
        xf_cr_selection .append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[1] > %f  && ph_sigmaIEIE[1] < %f ) ' %( xf_cr_base , pos_string, bkg_cut[1][0], bkg_cut[1][1] ) ) )
        xf_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[1] > %f  && ph_sigmaIEIE[1] < %f ) ' %( xf_cr_base , pos_string, bkg_cut[1][0], bkg_cut[1][1] ) ) )
        fx_cr_selection .append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f  && ph_sigmaIEIE[0] < %f ) ' %( fx_cr_base , pos_string, bkg_cut[0][0], bkg_cut[0][1] ) ) )
        fx_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f  && ph_sigmaIEIE[0] < %f ) ' %( fx_cr_base , pos_string, bkg_cut[0][0], bkg_cut[0][1] ) ) )
        #fr_cr_selection .append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s) ' %( fr_cr_base , pos_string ) ) )
        #fr_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( fr_cr_base , pos_string ) ) )
        #rf_cr_selection .append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s) ' %( rf_cr_base , pos_string ) ) )
        #rf_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( rf_cr_base , pos_string ) ) )
        ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_sigmaIEIE[1] > %f && ph_sigmaIEIE[1] < %f  ) ' %( ff_cr_base , pos_string, bkg_cut[1][0], bkg_cut[1][1], bkg_cut[0][0], bkg_cut[0][1] ) ) )
        ff_cr_selection .append( ( 'ph_sigmaIEIE[1]'    , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_sigmaIEIE[1] > %f && ph_sigmaIEIE[1] < %f  ) ' %( ff_cr_base , pos_string, bkg_cut[1][0], bkg_cut[1][1], bkg_cut[0][0], bkg_cut[0][1] ) ) )
    
    elif position[0] is 'EE' and position[1] is 'EE' :
        sig_selection.append( ( 'ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) ' %( signal_base ) ) )
        sig_selection.append( ( 'ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) ' %( signal_base ) ) )
        bkg_selection.append( ( 'ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) ' %( bkg_base    ) ) )
        bkg_selection.append( ( 'ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) ' %( bkg_base    ) ) )

        pos_string = 'ph_IsEE[0] && ph_IsEE[1] '

        target_selection.append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s) ' %( target_base, pos_string ) ) ) 
        target_selection.append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( target_base, pos_string ) ) ) 
        xf_cr_selection .append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[1] > %f  && ph_sigmaIEIE[1] < %f ) ' %( xf_cr_base , pos_string, bkg_cut[1][0], bkg_cut[1][1] ) ) ) 
        xf_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[1] > %f  && ph_sigmaIEIE[1] < %f ) ' %( xf_cr_base , pos_string, bkg_cut[1][0], bkg_cut[1][1] ) ) ) 
        fx_cr_selection .append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f  && ph_sigmaIEIE[0] < %f ) ' %( fx_cr_base , pos_string, bkg_cut[0][0], bkg_cut[0][1] ) ) ) 
        fx_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f  && ph_sigmaIEIE[0] < %f ) ' %( fx_cr_base , pos_string, bkg_cut[0][0], bkg_cut[0][1] ) ) ) 
        #fr_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( fr_cr_base , pos_string ) ) ) 
        #fr_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( fr_cr_base , pos_string ) ) ) 
        #rf_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( rf_cr_base , pos_string ) ) ) 
        #rf_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( rf_cr_base , pos_string ) ) ) 
        #ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( ff_cr_base , pos_string ) ) ) 
        #ff_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( ff_cr_base , pos_string ) ) ) 
        ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_sigmaIEIE[1] > %f && ph_sigmaIEIE[1] < %f  ) ' %( ff_cr_base , pos_string, bkg_cut[1][0], bkg_cut[1][1], bkg_cut[0][0], bkg_cut[0][1] ) ) )
        ff_cr_selection .append( ( 'ph_sigmaIEIE[1]'    , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_sigmaIEIE[1] > %f && ph_sigmaIEIE[1] < %f  ) ' %( ff_cr_base , pos_string, bkg_cut[1][0], bkg_cut[1][1], bkg_cut[0][0], bkg_cut[0][1] ) ) )
    

    plot_lead_subl=True
    if position[0] is not position[1] :
        plot_lead_subl=False


    sig_template_hist = None
    sig_template_hist_neg = None

    bkg_template_hist = None
    bkg_template_hist_neg = None
    
    sig_template_samp = samples.get_samples(name=signal_sample )
    bkg_template_samp = samples.get_samples(name=bkg_sample)
    
    sig_hists=[]
    bkg_hists=[]
                                
    #background template
    if bkg_template_samp :
        bkg_hists = [clone_sample_and_draw( bkg_template_samp[0], var, sel, binning ) for (var, sel) in bkg_selection ]

    if sig_template_samp :
        sig_hists = [clone_sample_and_draw( sig_template_samp[0], var, sel, binning ) for (var, sel) in sig_selection ]

    bkg_hists.append(bkg_hists[0])
    sig_hists.append(sig_hists[0])
    

    # determine efficiency of signal cut in background template
    if sig_cut is not None :
        tight_eff_bkg = bkg_hists[0].Integral( bkg_hists[0].FindBin(sig_cut[1][0]), bkg_hists[0].FindBin( sig_cut[1][1] ) ) / bkg_hists[0].Integral() 
        tight_eff_sig = sig_hists[0].Integral( sig_hists[0].FindBin(sig_cut[1][0]), sig_hists[0].FindBin( sig_cut[1][1] ) ) / sig_hists[0].Integral() 
    if sig_bins is not None :
        tight_eff_bkg = bkg_hists[0].GetBinContent( sig_bins[1] ) / bkg_hists[0].Integral() 
        tight_eff_sig = sig_hists[0].GetBinContent( sig_bins[1] ) / sig_hists[0].Integral() 
    if bkg_cut is not None :
        loose_eff_bkg = bkg_hists[0].Integral( bkg_hists[0].FindBin(bkg_cut[1][0]), bkg_hists[0].FindBin( bkg_cut[1][1] ) ) / bkg_hists[0].Integral() 
        loose_eff_sig = sig_hists[0].Integral( sig_hists[0].FindBin(bkg_cut[1][0]), sig_hists[0].FindBin( bkg_cut[1][1] ) ) / sig_hists[0].Integral() 
    if bkg_bins is not None :
        loose_eff_bkg = bkg_hists[0].GetBinContent( bkg_bins[1] ) / bkg_hists[0].Integral() 
        loose_eff_sig = sig_hists[0].GetBinContent( bkg_bins[1] ) / sig_hists[0].Integral() 

    print 'tight_eff_bkg = ', tight_eff_bkg
    print 'loose_eff_bkg = ', loose_eff_bkg
    print 'tight_eff_sig = ', tight_eff_sig
    print 'loose_eff_sig = ', loose_eff_sig

    bkg_hists[0].SetLineColor(ROOT.kRed)
    sig_hists[0].SetLineColor(ROOT.kBlue-2)
    bkg_hists[1].SetLineColor(ROOT.kRed)
    sig_hists[1].SetLineColor(ROOT.kBlue-2)
    bkgtemp = ROOT.TCanvas('bkgtemp', 'bkgtemp')
    draw_template(bkgtemp, [bkg_hists[0]], normalize=1, outputName=None )
    sigtemp = ROOT.TCanvas('sigtemp', 'sigtemp')
    draw_template(sigtemp, [sig_hists[0]], normalize=1, outputName=None )

    target_hists = None
    xf_cr_hists = None
    fx_cr_hists = None
    ff_cr_hists = None
    rf_cr_hists = None
    fr_cr_hists = None
    target_samp = samples.get_samples(name=target_sample)
    if target_samp :

        xf_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in xf_cr_selection]

        fx_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in fx_cr_selection]

        ff_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in ff_cr_selection]

        #rf_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in rf_cr_selection]

        #fr_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in fr_cr_selection]

    xf_cr_hist_lead = xf_cr_hists[0]
    xf_cr_hist_subl = xf_cr_hists[1]
    fx_cr_hist_lead = fx_cr_hists[0]
    fx_cr_hist_subl = fx_cr_hists[1]
    ff_cr_hist_lead = ff_cr_hists[0]
    ff_cr_hist_subl = ff_cr_hists[1]

    # determine rf normalization factor
    subl_norm=-1
    lead_norm=-1
    avg_norm=-1
    xf_norm=-1
    fx_norm=-1

    if bkg_cut is not None and sig_cut is not None  :

        leadsig_fit_bins = ( xf_cr_hist_lead.FindBin( sig_cut[1][0] ) , xf_cr_hist_lead.FindBin( sig_cut[1][1] ) )
        sublsig_fit_bins = ( xf_cr_hist_subl.FindBin( sig_cut[0][0] ) , xf_cr_hist_subl.FindBin( sig_cut[0][1] ) )

        ff_fit_bins_lead = ( xf_cr_hist_lead.FindBin( bkg_cut[1][0] ) , xf_cr_hist_lead.FindBin( bkg_cut[1][1] ) )
        ff_fit_bins_subl = ( xf_cr_hist_subl.FindBin( bkg_cut[0][0] ) , xf_cr_hist_subl.FindBin( bkg_cut[0][1] ) )

        print 'Normalize in lead ff region betwen bins %d and %d ( %f and %f )' %(ff_fit_bins_lead[0],ff_fit_bins_lead[1], bkg_cut[1][0], bkg_cut[1][1])
        print 'Normalize in subl ff region betwen bins %d and %d ( %f and %f )' %(ff_fit_bins_subl[0],ff_fit_bins_subl[1], bkg_cut[0][0], bkg_cut[0][1])
        print 'Normalize in xf region betwen bins %d and %d ( %f and %f )' %(leadsig_fit_bins[0], leadsig_fit_bins[1], sig_cut[1][0], sig_cut[1][1] )
        print 'Normalize in fx region betwen bins %d and %d ( %f and %f )' %(sublsig_fit_bins[0], sublsig_fit_bins[1], sig_cut[0][0], sig_cut[0][1] )
        print 'Bin %d min=%f, center=%f, max=%f '%( ff_fit_bins_lead[0], xf_cr_hist_lead.GetXaxis().GetBinLowEdge( ff_fit_bins_lead[0] ), xf_cr_hist_lead.GetXaxis().GetBinCenter( ff_fit_bins_lead[0] ), xf_cr_hist_lead.GetXaxis().GetBinUpEdge( ff_fit_bins_lead[0] ) )
        print 'Bin %d min=%f, center=%f, max=%f '%( ff_fit_bins_subl[1], xf_cr_hist_subl.GetXaxis().GetBinLowEdge( ff_fit_bins_subl[1] ), xf_cr_hist_subl.GetXaxis().GetBinCenter( ff_fit_bins_subl[1] ), xf_cr_hist_subl.GetXaxis().GetBinUpEdge( ff_fit_bins_subl[1] ) )
        print 'ff_cr_hist.Integral( ff_fit_bins_subl[0], ff_fit_bins_subl[1] ) ', ff_cr_hist_subl.Integral( ff_fit_bins_subl[0], ff_fit_bins_subl[1] ) 
        print 'ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] ) ', ff_cr_hist_lead.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        print 'xf_cr_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1])', xf_cr_hist_lead.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1])
        print 'fx_cr_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1])', fx_cr_hist_subl.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1])

        n_ll_target_lead = xf_cr_hist_lead.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        n_ll_target_subl = fx_cr_hist_subl.Integral( ff_fit_bins_subl[0], ff_fit_bins_subl[1] )
        n_ll_ff_template_lead = bkg_hists[0].Integral(ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        n_ll_ff_template_subl = bkg_hists[1].Integral(ff_fit_bins_subl[0], ff_fit_bins_subl[1] )
        lead_norm = n_ll_target_lead / n_ll_ff_template_lead
        subl_norm = n_ll_target_subl / n_ll_ff_template_subl
        n_xf_target = xf_cr_hist_lead.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1]) - lead_norm*bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) 
        n_fx_target = fx_cr_hist_subl.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1]) - subl_norm*bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] )
        xf_lead_norm = n_xf_target / sig_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) 
        fx_subl_norm = n_fx_target / sig_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] )
        xf_subl_norm = xf_lead_norm * ( sig_hists[0].Integral() /( bkg_hists[1].Integral( ) - bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ) ) )
        fx_lead_norm = fx_subl_norm * ( sig_hists[1].Integral() /( bkg_hists[0].Integral( ) - bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) ) )

        print 'N ff events in rf normalization region = ', lead_norm*bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] )
        print 'N ff events in fr normalization region = ', subl_norm*bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] )
        print 'N xf target = ', n_xf_target
        print 'N fx target = ', n_fx_target
        print 'rf norm = ', xf_lead_norm
        print 'fr norm = ', fx_lead_norm
        print 'N lead rf after norm = ',xf_lead_norm * ( sig_hists[0].Integral() ) 
        print 'N subl fr after norm = ',fx_subl_norm * ( sig_hists[1].Integral() ) 
        print 'N loose subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) - bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ) )
        print 'N loose lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) - bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) )
        print 'N total subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) )
        print 'N total lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) )
        print 'Fraction of signal in subl loose region = %f' %( fx_subl_norm*sig_hists[1].Integral( ff_fit_bins_subl[0],ff_fit_bins_subl[1] )/ ( subl_norm*bkg_hists[1].Integral( ff_fit_bins_subl[0], ff_fit_bins_subl[1] ) ) )
        print 'Fraction of signal in lead loose region = %f' %( xf_lead_norm*sig_hists[0].Integral( ff_fit_bins_lead[0],ff_fit_bins_lead[1] )/ ( lead_norm*bkg_hists[0].Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] ) )  )

        print 'Predict %f rf events in TT region' %( xf_subl_norm * bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ) )
        print 'Predict %f fr events in TT region' %( fx_lead_norm * bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) )
        #print '%d data events in LL region ' %ff_cr_hist_lead.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        print '%d data events in LL region ' %ff_cr_hist_lead.Integral( )
        print 'Probability for f to be T = %f' %(tight_eff_bkg)
        print 'Probability for f to be L = %f' %(loose_eff_bkg)
        #print 'Predict %f ff events in TT region' %( ff_cr_hist_lead.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] ) * ( tight_eff_bkg*tight_eff_bkg) / (loose_eff_bkg*loose_eff_bkg) )
        print 'Predict %f ff events in TT region' %( ff_cr_hist_lead.Integral( ) * ( tight_eff_bkg*tight_eff_bkg) / (loose_eff_bkg*loose_eff_bkg) )

    elif bkg_bins is not None and sig_bins is not None :


        print 'Normalize ff template in xf region in bin %d ' %bkg_bins[1]
        print 'Normalize ff template in fx region in bin %d'  %bkg_bins[0]
        
        print '%f events in subl LL region ' %fx_cr_hist_subl.GetBinContent( bkg_bins[0]) 
        print '%f events in lead LL region ' %xf_cr_hist_lead.GetBinContent( bkg_bins[1]) 
        print '%f events in fx signal region ' %fx_cr_hist_subl.GetBinContent( sig_bins[0]) 
        print '%f events in xf signal region ' %xf_cr_hist_lead.GetBinContent( sig_bins[1]) 
        print '%f events in fx ff template ' %bkg_hists[1].GetBinContent( bkg_bins[0] )
        print '%f events in xf ff template ' %bkg_hists[0].GetBinContent( bkg_bins[1] )

        print 'Normalize in xf region in bin %d ' %sig_bins[1]
        print 'Normalize in fx region in bin %d' %sig_bins[0]
        n_ll_target_lead = xf_cr_hist_lead.GetBinContent( bkg_bins[1] )
        n_ll_target_subl = fx_cr_hist_subl.GetBinContent( bkg_bins[0] )
        n_ll_ff_template_lead = bkg_hists[0].GetBinContent(bkg_bins[1] )
        n_ll_ff_template_subl = bkg_hists[1].GetBinContent(bkg_bins[0] )
        lead_norm = n_ll_target_lead / n_ll_ff_template_lead
        subl_norm = n_ll_target_subl / n_ll_ff_template_subl
        n_xf_target = xf_cr_hist_lead.GetBinContent( sig_bins[1]) - lead_norm*bkg_hists[0].GetBinContent( sig_bins[1] ) 
        n_fx_target = fx_cr_hist_subl.GetBinContent( sig_bins[0]) - subl_norm*bkg_hists[1].GetBinContent( sig_bins[0] )
        xf_lead_norm = n_xf_target / sig_hists[0].GetBinContent( sig_bins[1] ) 
        fx_subl_norm = n_fx_target / sig_hists[1].GetBinContent( sig_bins[0] )
        xf_subl_norm = xf_lead_norm * ( sig_hists[0].Integral() / ( bkg_hists[1].Integral() - bkg_hists[1].GetBinContent( sig_bins[0] ) ) )
        fx_lead_norm = fx_subl_norm * ( sig_hists[1].Integral() / ( bkg_hists[0].Integral() - bkg_hists[0].GetBinContent( sig_bins[1] ) ) )

        print 'N ff events in rf normalization region = ', lead_norm*bkg_hists[0].GetBinContent( sig_bins[1] )
        print 'N ff events in fr normalization region = ', subl_norm*bkg_hists[1].GetBinContent( sig_bins[0] )
        print 'N xf target = ', n_xf_target
        print 'N fx target = ', n_fx_target
        print 'rf norm = ', xf_lead_norm
        print 'fr norm = ', fx_lead_norm
        print 'N lead rf after norm = ',xf_lead_norm * ( sig_hists[0].Integral() ) 
        print 'N subl fr after norm = ',fx_subl_norm * ( sig_hists[1].Integral() ) 
        print 'N loose subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) - bkg_hists[1].GetBinContent( sig_bins[0] ) )
        print 'N loose lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) - bkg_hists[0].GetBinContent( sig_bins[1] ) )
        print 'N total subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) )
        print 'N total lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) )

        print 'Predict %f rf events in TT region' %( xf_subl_norm * bkg_hists[1].GetBinContent( sig_bins[0] ) )
        print 'Predict %f fr events in TT region' %( fx_lead_norm * bkg_hists[0].GetBinContent( sig_bins[1] ) )
        print '%d data events in LL region ' %ff_cr_hist_lead.GetBinContent( bkg_bins[1] )
        print 'Probability for f to be T = %f' %(tight_eff_bkg)
        print 'Probability for f to be L = %f' %(loose_eff_bkg)
        print 'Predict %f ff events in TT region' %( ff_cr_hist_lead.GetBinContent( bkg_bins[1] ) * ( tight_eff_bkg*tight_eff_bkg) / (loose_eff_bkg*loose_eff_bkg) )


    print 'subl FF factor = %f, lead FF factor = %f, average = %f' %( subl_norm, lead_norm, avg_norm )

    ff_template_hist_xfNew = bkg_hists[0].Clone('ffhistxfnew')
    ff_template_hist_xfNew.Scale( lead_norm )
    ff_template_hist_fxNew = bkg_hists[1].Clone('ffhistfxnew')
    ff_template_hist_fxNew.Scale( subl_norm )
    
    rf_template_histNew = sig_hists[0].Clone('rfhistnew')
    rf_template_histNew.Scale( xf_lead_norm )

    fr_template_histNew = sig_hists[1].Clone('frhistnew')
    fr_template_histNew.Scale( fx_subl_norm )

    ff_template_hist_fxNew.SetLineColor(ROOT.kRed)
    ff_template_hist_xfNew.SetLineColor(ROOT.kRed)
    rf_template_histNew.SetLineColor(ROOT.kMagenta+1)
    fr_template_histNew.SetLineColor(ROOT.kCyan+1)
    ff_template_hist_fxNew.SetMarkerColor(ROOT.kRed)
    ff_template_hist_xfNew.SetMarkerColor(ROOT.kRed)
    rf_template_histNew.SetMarkerColor(ROOT.kMagenta+1)
    fr_template_histNew.SetMarkerColor(ROOT.kCyan+1)

    ff_template_hist_fxNew.SetLineWidth(2)
    ff_template_hist_xfNew.SetLineWidth(2)
    rf_template_histNew.SetLineWidth(2)
    fr_template_histNew.SetLineWidth(2)

    ff_template_hist_fxNew.SetMarkerSize(0)
    ff_template_hist_xfNew.SetMarkerSize(0)
    rf_template_histNew.SetMarkerSize(0)
    fr_template_histNew.SetMarkerSize(0)

    ff_template_hist_fxNew.SetLineStyle(ROOT.kSolid)
    ff_template_hist_xfNew.SetLineStyle(ROOT.kSolid)
    rf_template_histNew.SetLineStyle(ROOT.kSolid)
    fr_template_histNew.SetLineStyle(ROOT.kSolid)

    rrtempName = None
    rftempName = None
    frtempName = None
    fftempNamefx = None
    fftempNamexf = None
    fftempNorm_llName = None
    rftempNorm_xlName = None
    frtempNorm_lxName = None
    fftempNorm_rfName = None
    fftempNorm_frName = None

    if outputDir is not None :
        tempName = 'template_'
        tempNormName = 'templateNorm_'
        if position[0]=='EB' :
            tempName+='eb_'
            tempNormName += 'eb_'
        if position[0]=='EE' :
            tempName+='ee_'
            tempNormName += 'ee_'
        if position[1]=='EB' :
            tempName+='eb.pdf'
            tempNormName += 'eb.pdf'
        if position[1]=='EE' :
            tempName+='ee.pdf'
            tempNormName += 'ee.pdf'

        rrtempName = outputDir + '/rr'+tempName
        rftempName = outputDir + '/rf'+tempName
        frtempName = outputDir + '/fr'+tempName
        fftempNamefx = outputDir + '/fffx'+tempName
        fftempNamexf = outputDir + '/ffxf'+tempName

        fftempNorm_llName = outputDir +'/ff_llregion_'+tempNormName
        rftempNorm_xlName = outputDir +'/rf_xlregion_'+tempNormName
        frtempNorm_lxName = outputDir +'/fr_lxregion_'+tempNormName
        fftempNorm_rfName = outputDir +'/ff_rfregion_'+tempNormName
        fftempNorm_frName = outputDir +'/ff_frregion_'+tempNormName


    xfcan = ROOT.TCanvas('xfcan', 'xfcan')
    draw_template(xfcan, [xf_cr_hist_lead, rf_template_histNew, ff_template_hist_xfNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=rftempNorm_xlName, plot_lead_subl=plot_lead_subl)

    xfcan_subl = ROOT.TCanvas('xfcan_subl', 'xfcan_subl')
    draw_template(xfcan_subl, [xf_cr_hist_subl, rf_template_histNew, ff_template_hist_xfNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=None, plot_lead_subl=plot_lead_subl)

    fxcan = ROOT.TCanvas('fxcan', 'fxcan')
    draw_template(fxcan, [fx_cr_hist_subl, fr_template_histNew, ff_template_hist_fxNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FR template', 'FF template'], outputName=frtempNorm_lxName, plot_lead_subl=plot_lead_subl)

    fxcan_lead= ROOT.TCanvas('fxcan_lead', 'fxcan_lead')
    draw_template(fxcan_lead, [fx_cr_hist_lead, fr_template_histNew, ff_template_hist_xfNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FR template', 'FR template'], outputName=None, plot_lead_subl=plot_lead_subl)

    #if bkg_cut is not None and sig_cut is not None  :
    #    rf_fit_bins = ( rf_cr_hist.FindBin( bkg_cut[0][0] ), rf_cr_hist.FindBin( bkg_cut[0][1] ) )
    #    fr_fit_bins = ( rf_cr_hist.FindBin( bkg_cut[1][0] ), rf_cr_hist.FindBin( bkg_cut[1][1] ) )

    #    subl_sig_bins = ( rf_cr_hist.FindBin( sig_cut[0][0] ), rf_cr_hist.FindBin( sig_cut[0][1] ) )
    #    lead_sig_bins = ( rf_cr_hist.FindBin( sig_cut[1][0] ), rf_cr_hist.FindBin( sig_cut[1][1] ) )

    #    print 'Normalize in xf region betwen bins %d and %d' %rf_fit_bins
    #    print 'Normalize in fx region betwen bins %d and %d' %fr_fit_bins
    #    subl_ff_norm = ( rf_cr_hist.Integral( rf_fit_bins[0], rf_fit_bins[1]) - rf_template_hist.Integral( rf_fit_bins[0], rf_fit_bins[1] ) ) / ff_template_hist_xf.Integral( rf_fit_bins[0], rf_fit_bins[1] ) 
    #    lead_ff_norm = ( fr_cr_hist.Integral( fr_fit_bins[0], fr_fit_bins[1]) - fr_template_hist.Integral( fr_fit_bins[0], fr_fit_bins[1] ) ) / ff_template_hist_fx.Integral( fr_fit_bins[0], fr_fit_bins[1] ) 

    #    print 'Predict %f ff events in TT region using subl fit' %(subl_ff_norm*ff_template_hist_xf.Integral( subl_sig_bins[0], subl_sig_bins[1] ))
    #    print 'Predict %f ff events in TT region using lead fit' %(lead_ff_norm*ff_template_hist_fx.Integral( lead_sig_bins[0], lead_sig_bins[1] ))

    #elif bkg_bins is not None and sig_bins is not None :

    #    print 'Normalize in xf region in bin %d ' %sig_bins[1]
    #    print 'Normalize in fx region in bin %d' %sig_bins[0]
    #    subl_ff_norm = ( rf_cr_hist.GetBinContent( bkg_bins[0] ) - rf_template_hist.GetBinContent( bkg_bins[0] ) ) / ff_template_hist_xf.GetBinContent( bkg_bins[0] ) 
    #    lead_ff_norm = ( fr_cr_hist.GetBinContent( bkg_bins[1] ) - fr_template_hist.GetBinContent( bkg_bins[1] ) ) / ff_template_hist_fx.GetBinContent( bkg_bins[1] ) 

    #    print 'Predict %f ff events in TT region using subl fit' %(subl_ff_norm*ff_template_hist_xf.GetBinContent( sig_bins[0] ))
    #    print 'Predict %f ff events in TT region using lead fit' %(lead_ff_norm*ff_template_hist_fx.GetBinContent( sig_bins[1] ))

    #print 'Normalization ff in rf region = %f' %subl_ff_norm
    #print 'Normalization ff in fr region = %f' %lead_ff_norm

    #ff_template_hist_xf.Scale( subl_ff_norm )
    #ff_template_hist_fx.Scale( lead_ff_norm )
    #rfcan = ROOT.TCanvas('rfcan', 'rfcan')
    #draw_template_with_axis(rfcan, [rf_cr_hist, rf_template_hist, ff_template_hist_xf], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=fftempNorm_rfName, plot_lead_subl=plot_lead_subl)
    #frcan = ROOT.TCanvas('frcan', 'frcan')
    #draw_template_with_axis(frcan, [fr_cr_hist, fr_template_hist, ff_template_hist_fx], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=fftempNorm_frName, plot_lead_subl=plot_lead_subl)

def fit_diphoton( signal_base, bkg_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning, position,  sig_cut=None, bkg_cut=None, sig_bins=None, bkg_bins=None, outputDir=None ) :

    global samples

    sig_selection = []
    bkg_selection    = []
    target_selection = []
    xf_cr_selection  = []
    fx_cr_selection  = []
    fr_cr_selection  = []
    rf_cr_selection  = []
    ff_cr_selection  = []

    if position[0] is not position[1] : #EB+EE
        print 'Doing EB+EE'

        sig_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEB[0] ) '    %( signal_base ) ) )
        sig_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) '    %( signal_base ) ) )
        bkg_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEB[0] ) '    %( bkg_base    ) ) )
        bkg_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) '    %( bkg_base    ) ) )
        
        #target_selection.append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( target_base ) ) )
        #target_selection.append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( target_base ) ) )
        #xf_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( xf_cr_base  ) ) ) 
        #xf_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( xf_cr_base  ) ) ) 
        #fx_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( fx_cr_base  ) ) ) 
        #fx_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( fx_cr_base  ) ) ) 
        #fr_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( fr_cr_base  ) ) ) 
        #fr_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( fr_cr_base  ) ) ) 
        #rf_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( rf_cr_base  ) ) ) 
        #rf_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( rf_cr_base  ) ) ) 
        #ff_cr_selection .append( ( 'ph_sigmaIEIE'   , ' PUWeight * ( %s && ( ph_IsEB[0] || ph_IsEB[1] ) ) ' %( ff_cr_base  ) ) ) 
        #ff_cr_selection .append( ( '-1*ph_sigmaIEIE', ' PUWeight * ( %s && ( ph_IsEE[0] || ph_IsEE[1] ) ) ' %( ff_cr_base  ) ) ) 

        #target_selection.append( ( 'ph_sigmaIEIE[0]   ', ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( target_base ) ) )
        #target_selection.append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( target_base ) ) )
        #xf_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( xf_cr_base  ) ) ) 
        #xf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( xf_cr_base  ) ) ) 
        #fx_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( fx_cr_base  ) ) ) 
        #fx_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( fx_cr_base  ) ) ) 
        #fr_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( fr_cr_base  ) ) ) 
        #fr_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( fr_cr_base  ) ) ) 
        #rf_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( rf_cr_base  ) ) ) 
        #rf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( rf_cr_base  ) ) ) 
        #ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( ff_cr_base  ) ) ) 
        #ff_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( ff_cr_base  ) ) ) 

        target_selection.append( ( 'ph_sigmaIEIE[0]   ', ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( target_base ) ) )
        #target_selection.append( ( 'ph_sigmaIEIE[1]   ', ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( target_base ) ) )
        #target_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( target_base ) ) )
        target_selection.append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( target_base ) ) )
        xf_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( xf_cr_base  ) ) ) 
        #xf_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( xf_cr_base  ) ) ) 
        #xf_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( xf_cr_base  ) ) ) 
        xf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( xf_cr_base  ) ) ) 
        fx_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( fx_cr_base  ) ) ) 
        #fx_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( fx_cr_base  ) ) ) 
        #fx_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( fx_cr_base  ) ) ) 
        fx_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( fx_cr_base  ) ) ) 
        fr_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( fr_cr_base  ) ) ) 
        #fr_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( fr_cr_base  ) ) ) 
        #fr_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( fr_cr_base  ) ) ) 
        fr_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( fr_cr_base  ) ) ) 
        rf_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( rf_cr_base  ) ) ) 
        #rf_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( rf_cr_base  ) ) ) 
        #rf_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( rf_cr_base  ) ) ) 
        rf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( rf_cr_base  ) ) ) 
        ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ( ph_IsEB[0] && ph_IsEE[1] ) ) ' %( ff_cr_base  ) ) ) 
        #ff_cr_selection .append( ( 'ph_sigmaIEIE[1]'   , ' PUWeight * ( %s && ( ph_IsEB[1] && ph_IsEE[0] ) ) ' %( ff_cr_base  ) ) ) 
        #ff_cr_selection .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ( ph_IsEE[0] && ph_IsEB[1] ) ) ' %( ff_cr_base  ) ) ) 
        ff_cr_selection .append( ( '-1*ph_sigmaIEIE[1]', ' PUWeight * ( %s && ( ph_IsEE[1] && ph_IsEB[0] ) ) ' %( ff_cr_base  ) ) ) 

    elif position[0] is 'EB' and position[1] is 'EB' :
        sig_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight *  ( %s && ph_IsEB[0] ) ' %( signal_base ) ) )
        sig_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight *  ( %s && ph_IsEB[0] ) ' %( signal_base ) ) )
        bkg_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight *  ( %s && ph_IsEB[0] ) ' %( bkg_base    ) ) )
        bkg_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight *  ( %s && ph_IsEB[0] ) ' %( bkg_base    ) ) )

        pos_string = 'ph_IsEB[0] && ph_IsEB[1]'

        target_selection.append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( target_base, pos_string ) ) )
        target_selection.append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( target_base, pos_string ) ) )
        xf_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( xf_cr_base , pos_string ) ) )
        xf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( xf_cr_base , pos_string ) ) )
        fx_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( fx_cr_base , pos_string ) ) )
        fx_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( fx_cr_base , pos_string ) ) )
        fr_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( fr_cr_base , pos_string ) ) )
        fr_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( fr_cr_base , pos_string ) ) )
        rf_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( rf_cr_base , pos_string ) ) )
        rf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( rf_cr_base , pos_string ) ) )
        ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( ff_cr_base , pos_string ) ) )
        ff_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( ff_cr_base , pos_string ) ) )
    
    elif position[0] is 'EE' and position[1] is 'EE' :
        sig_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEE[0] ) ' %( signal_base ) ) )
        sig_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) ' %( signal_base ) ) )

        bkg_selection   .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEE[0] ) ' %( bkg_base    ) ) )
        bkg_selection   .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) ' %( bkg_base    ) ) )

        pos_string = 'ph_IsEE[0] && ph_IsEE[1] '

        target_selection.append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( target_base, pos_string ) ) ) 
        target_selection.append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( target_base, pos_string ) ) ) 
        xf_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( xf_cr_base , pos_string ) ) ) 
        xf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( xf_cr_base , pos_string ) ) ) 
        fx_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( fx_cr_base , pos_string ) ) ) 
        fx_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( fx_cr_base , pos_string ) ) ) 
        fr_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( fr_cr_base , pos_string ) ) ) 
        fr_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( fr_cr_base , pos_string ) ) ) 
        rf_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( rf_cr_base , pos_string ) ) ) 
        rf_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( rf_cr_base , pos_string ) ) ) 
        ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s) ' %( ff_cr_base , pos_string ) ) ) 
        ff_cr_selection .append( ( '-1*ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s) ' %( ff_cr_base , pos_string ) ) ) 
    

    plot_lead_subl=True
    if position[0] is not position[1] :
        plot_lead_subl=False


    #generate histograms
    rr_template_hist = None
    rf_template_hist = None
    fr_template_hist = None
    ff_template_hist = None

    sig_template_hist = None
    sig_template_hist_neg = None

    bkg_template_hist = None
    bkg_template_hist_neg = None
    
    sig_template_samp = samples.get_samples(name=signal_sample )
    bkg_template_samp = samples.get_samples(name=bkg_sample)
    
    sig_hists=[]
    bkg_hists=[]
                                
    #background template
    if bkg_template_samp :
        bkg_hists = [clone_sample_and_draw( bkg_template_samp[0], var, sel, binning ) for (var, sel) in bkg_selection ]

    if sig_template_samp :
        sig_hists = [clone_sample_and_draw( sig_template_samp[0], var, sel, binning ) for (var, sel) in sig_selection ]

    rr_template_hist = sig_hists[0].Clone('rrhist')
    rr_template_hist.Scale( sig_hists[1].Integral()/rr_template_hist.Integral())
    rr_template_hist.Add( sig_hists[1] )

    # determine efficiency of signal cut in background template
    if sig_cut is not None :
        tight_eff_bkg = bkg_hists[0].Integral( bkg_hists[0].FindBin(sig_cut[1][0]), bkg_hists[0].FindBin( sig_cut[1][1] ) ) / bkg_hists[0].Integral() 
        tight_eff_sig = sig_hists[0].Integral( sig_hists[0].FindBin(sig_cut[1][0]), sig_hists[0].FindBin( sig_cut[1][1] ) ) / sig_hists[0].Integral() 
    if sig_bins is not None :
        tight_eff_bkg = bkg_hists[0].GetBinContent( sig_bins[1] ) / bkg_hists[0].Integral() 
        tight_eff_sig = sig_hists[0].GetBinContent( sig_bins[1] ) / sig_hists[0].Integral() 
    if bkg_cut is not None :
        loose_eff_bkg = bkg_hists[0].Integral( bkg_hists[0].FindBin(bkg_cut[1][0]), bkg_hists[0].FindBin( bkg_cut[1][1] ) ) / bkg_hists[0].Integral() 
        loose_eff_sig = sig_hists[0].Integral( sig_hists[0].FindBin(bkg_cut[1][0]), sig_hists[0].FindBin( bkg_cut[1][1] ) ) / sig_hists[0].Integral() 
    if bkg_bins is not None :
        loose_eff_bkg = bkg_hists[0].GetBinContent( bkg_bins[1] ) / bkg_hists[0].Integral() 
        loose_eff_sig = sig_hists[0].GetBinContent( bkg_bins[1] ) / sig_hists[0].Integral() 


    print 'tight_eff_bkg = ', tight_eff_bkg
    print 'loose_eff_bkg = ', loose_eff_bkg
    print 'tight_eff_sig = ', tight_eff_sig
    print 'loose_eff_sig = ', loose_eff_sig


    ff_template_hist_xf = bkg_hists[0].Clone('ffhistxf')
    # normalize subl distribution to the lead distribution, but increase the sublead by 1/tight_eff_bkg
    ff_template_hist_xf.Scale( tight_eff_bkg*bkg_hists[1].Integral()/ff_template_hist_xf.Integral())
    ff_template_hist_xf.Add( bkg_hists[1] )

    ff_template_hist_fx = bkg_hists[0].Clone('ffhistfx')
    # normalize lead distribution to the sublead distribution, but increase the lead by 1/tight_eff_bkg
    ff_template_hist_fx.Scale( bkg_hists[1].Integral()/( tight_eff_bkg*ff_template_hist_fx.Integral()))
    ff_template_hist_fx.Add( bkg_hists[1] )

    rf_template_hist = sig_hists[0].Clone( 'rfhist' )
    # normalize subl distribution to the lead distribution, but increase the sublead by 1/tight_eff_bkg
    rf_template_hist.Scale( tight_eff_bkg*bkg_hists[1].Integral() / rf_template_hist.Integral() )
    rf_template_hist.Add( bkg_hists[1] )
    
    fr_template_hist = bkg_hists[0].Clone( 'frhist' )
    # normalize lead distribution to the sublead distribution, but increase the lead by 1/tight_eff_bkg
    fr_template_hist.Scale( sig_hists[1].Integral() / ( tight_eff_bkg*fr_template_hist.Integral() ) )
    fr_template_hist.Add( sig_hists[1] )
    
    
    rr_template_hist.SetLineColor(ROOT.kGreen+1)
    ff_template_hist_fx.SetLineColor(ROOT.kRed)
    ff_template_hist_xf.SetLineColor(ROOT.kRed)
    rf_template_hist.SetLineColor(ROOT.kMagenta+1)
    fr_template_hist.SetLineColor(ROOT.kCyan+1)
    rr_template_hist.SetMarkerColor(ROOT.kGreen+1)
    ff_template_hist_fx.SetMarkerColor(ROOT.kRed)
    ff_template_hist_xf.SetMarkerColor(ROOT.kRed)
    rf_template_hist.SetMarkerColor(ROOT.kMagenta+1)
    fr_template_hist.SetMarkerColor(ROOT.kCyan+1)

    rr_template_hist.SetLineWidth(2)
    ff_template_hist_fx.SetLineWidth(2)
    ff_template_hist_xf.SetLineWidth(2)
    rf_template_hist.SetLineWidth(2)
    fr_template_hist.SetLineWidth(2)

    rr_template_hist.SetMarkerSize(0)
    ff_template_hist_fx.SetMarkerSize(0)
    ff_template_hist_xf.SetMarkerSize(0)
    rf_template_hist.SetMarkerSize(0)
    fr_template_hist.SetMarkerSize(0)

    rr_template_hist.SetLineStyle(ROOT.kSolid)
    ff_template_hist_fx.SetLineStyle(ROOT.kSolid)
    ff_template_hist_xf.SetLineStyle(ROOT.kSolid)
    rf_template_hist.SetLineStyle(ROOT.kSolid)
    fr_template_hist.SetLineStyle(ROOT.kSolid)

    rrtempName = None
    rftempName = None
    frtempName = None
    fftempNamefx = None
    fftempNamexf = None
    fftempNorm_llName = None
    rftempNorm_xlName = None
    frtempNorm_lxName = None
    fftempNorm_rfName = None
    fftempNorm_frName = None

    if outputDir is not None :
        tempName = 'template_'
        tempNormName = 'templateNorm_'
        if position[0]=='EB' :
            tempName+='eb_'
            tempNormName += 'eb_'
        if position[0]=='EE' :
            tempName+='ee_'
            tempNormName += 'ee_'
        if position[1]=='EB' :
            tempName+='eb.pdf'
            tempNormName += 'eb.pdf'
        if position[1]=='EE' :
            tempName+='ee.pdf'
            tempNormName += 'ee.pdf'

        rrtempName = outputDir + '/rr'+tempName
        rftempName = outputDir + '/rf'+tempName
        frtempName = outputDir + '/fr'+tempName
        fftempNamefx = outputDir + '/fffx'+tempName
        fftempNamexf = outputDir + '/ffxf'+tempName

        fftempNorm_llName = outputDir +'/ff_llregion_'+tempNormName
        rftempNorm_xlName = outputDir +'/rf_xlregion_'+tempNormName
        frtempNorm_lxName = outputDir +'/fr_lxregion_'+tempNormName
        fftempNorm_rfName = outputDir +'/ff_rfregion_'+tempNormName
        fftempNorm_frName = outputDir +'/ff_frregion_'+tempNormName

    
    #rrtemp = ROOT.TCanvas('rrtemp', 'rrtemp')
    #draw_template_with_axis(rrtemp, [rr_template_hist], normalize=1, outputName=rrtempName, plot_lead_subl=plot_lead_subl )
    rftemp = ROOT.TCanvas('rftemp', 'rftemp')
    draw_template_with_axis(rftemp, [fr_template_hist], normalize=1, outputName=rftempName, plot_lead_subl=plot_lead_subl )
    #frtemp = ROOT.TCanvas('frtemp', 'frtemp')
    #draw_template_with_axis(frtemp, [rf_template_hist], normalize=1, outputName=frtempName, plot_lead_subl=plot_lead_subl )
    #fftempfx = ROOT.TCanvas('fftempfx', 'fftempfx')
    #draw_template_with_axis(fftempfx, [ff_template_hist_fx], normalize=1, outputName=fftempNamefx, plot_lead_subl=plot_lead_subl )
    #fftempxf = ROOT.TCanvas('fftempxf', 'fftempxf')
    #draw_template_with_axis(fftempxf, [ff_template_hist_xf], normalize=1, outputName=fftempNamexf, plot_lead_subl=plot_lead_subl )


    target_hist = None
    xf_cr_hist = None
    fx_cr_hist = None
    ff_cr_hist = None
    rf_cr_hist = None
    fr_cr_hist = None
    target_samp = samples.get_samples(name=target_sample)
    if target_samp :
        #target_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in target_selection]
        #target_hist = target_hists[0]
        #[target_hist.Add( h ) for h in target_hists[1:] ]

        xf_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in xf_cr_selection]
        xf_cr_hist = xf_cr_hists[0]
        [xf_cr_hist.Add( h ) for h in xf_cr_hists[1:] ]

        fx_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in fx_cr_selection]
        fx_cr_hist = fx_cr_hists[0]
        [fx_cr_hist.Add( h ) for h in fx_cr_hists[1:] ]

        ff_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in ff_cr_selection]
        ff_cr_hist = ff_cr_hists[0]
        [ff_cr_hist.Add( h ) for h in ff_cr_hists[1:] ]

        rf_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in rf_cr_selection]
        rf_cr_hist = rf_cr_hists[0]
        [rf_cr_hist.Add( h ) for h in rf_cr_hists[1:] ]

        fr_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binning ) for (var, sel) in fr_cr_selection]
        fr_cr_hist = fr_cr_hists[0]
        [fr_cr_hist.Add( h ) for h in fr_cr_hists[1:] ]


    # determine rf normalization factor
    subl_norm=-1
    lead_norm=-1
    avg_norm=-1
    xf_norm=-1
    fx_norm=-1

    if bkg_cut is not None and sig_cut is not None  :

        leadsig_fit_bins = ( xf_cr_hist.FindBin( sig_cut[1][0] ) ,xf_cr_hist.FindBin( sig_cut[1][1] ) )
        sublsig_fit_bins = ( xf_cr_hist.FindBin( sig_cut[0][0] ) , xf_cr_hist.FindBin( sig_cut[0][1] ) )

        ff_fit_bins_lead = ( xf_cr_hist.FindBin( bkg_cut[1][0] ) , xf_cr_hist.FindBin( bkg_cut[1][1] ) )
        ff_fit_bins_subl = ( xf_cr_hist.FindBin( bkg_cut[0][0] ) , xf_cr_hist.FindBin( bkg_cut[0][1] ) )

        print 'Normalize in lead ff region betwen bins %d and %d ( %f and %f )' %(ff_fit_bins_lead[0],ff_fit_bins_lead[1], bkg_cut[1][0], bkg_cut[1][1])
        print 'Normalize in subl ff region betwen bins %d and %d ( %f and %f )' %(ff_fit_bins_subl[0],ff_fit_bins_subl[1], bkg_cut[0][0], bkg_cut[0][1])
        print 'Normalize in xf region betwen bins %d and %d ( %f and %f )' %(leadsig_fit_bins[0], leadsig_fit_bins[1], sig_cut[1][0], sig_cut[1][1] )
        print 'Normalize in fx region betwen bins %d and %d ( %f and %f )' %(sublsig_fit_bins[0], sublsig_fit_bins[1], sig_cut[0][0], sig_cut[0][1] )
        print 'Bin %d min=%f, center=%f, max=%f '%( ff_fit_bins_lead[0], xf_cr_hist.GetXaxis().GetBinLowEdge( ff_fit_bins_lead[0] ), xf_cr_hist.GetXaxis().GetBinCenter( ff_fit_bins_lead[0] ), xf_cr_hist.GetXaxis().GetBinUpEdge( ff_fit_bins_lead[0] ) )
        print 'Bin %d min=%f, center=%f, max=%f '%( ff_fit_bins_subl[1], xf_cr_hist.GetXaxis().GetBinLowEdge( ff_fit_bins_subl[1] ), xf_cr_hist.GetXaxis().GetBinCenter( ff_fit_bins_subl[1] ), xf_cr_hist.GetXaxis().GetBinUpEdge( ff_fit_bins_subl[1] ) )
        print 'ff_cr_hist.Integral( ff_fit_bins_subl[0], ff_fit_bins_subl[1] ) ', ff_cr_hist.Integral( ff_fit_bins_subl[0], ff_fit_bins_subl[1] ) 
        print 'ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] ) ', ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        print 'xf_cr_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1])', xf_cr_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1])
        print 'fx_cr_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1])', fx_cr_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1])

        n_ll_target_lead = xf_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        n_ll_target_subl = fx_cr_hist.Integral( ff_fit_bins_subl[0], ff_fit_bins_subl[1] )
        n_ll_ff_template_lead = bkg_hists[0].Integral(ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        n_ll_ff_template_subl = bkg_hists[1].Integral(ff_fit_bins_subl[0], ff_fit_bins_subl[1] )
        lead_norm = n_ll_target_lead / n_ll_ff_template_lead
        subl_norm = n_ll_target_subl / n_ll_ff_template_subl
        n_xf_target = xf_cr_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1]) - lead_norm*bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) 
        n_fx_target = fx_cr_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1]) - subl_norm*bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] )
        xf_lead_norm = n_xf_target / sig_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) 
        fx_subl_norm = n_fx_target / sig_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] )
        xf_subl_norm = xf_lead_norm * ( sig_hists[0].Integral() /( bkg_hists[1].Integral( ) - bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ) ) )
        fx_lead_norm = fx_subl_norm * ( sig_hists[1].Integral() /( bkg_hists[0].Integral( ) - bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) ) )

        print 'N ff events in rf normalization region = ', lead_norm*bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] )
        print 'N ff events in fr normalization region = ', subl_norm*bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] )
        print 'N xf target = ', n_xf_target
        print 'N fx target = ', n_fx_target
        print 'rf norm = ', xf_lead_norm
        print 'fr norm = ', fx_lead_norm
        print 'N lead rf after norm = ',xf_lead_norm * ( sig_hists[0].Integral() ) 
        print 'N subl fr after norm = ',fx_subl_norm * ( sig_hists[1].Integral() ) 
        print 'N loose subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) - bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ) )
        print 'N loose lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) - bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) )
        print 'N total subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) )
        print 'N total lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) )

        print 'Predict %f rf events in TT region' %( xf_subl_norm * bkg_hists[1].Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ) )
        print 'Predict %f fr events in TT region' %( fx_lead_norm * bkg_hists[0].Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) )
        print '%d data events in LL region ' %ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        print 'Probability for f to be T = %f' %(tight_eff_bkg)
        print 'Probability for f to be L = %f' %(loose_eff_bkg)
        print 'Probability for r to be T = %f' %(tight_eff_bkg)
        print 'Probability for r to be L = %f' %(loose_eff_bkg)
        print 'Predict %f ff events in TT region' %( ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] ) * ( tight_eff_bkg*tight_eff_bkg) / (loose_eff_bkg*loose_eff_bkg) )

        #n_ll_target_lead = ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        #n_ll_target_subl = ff_cr_hist.Integral( ff_fit_bins_subl[0], ff_fit_bins_subl[1] )
        #n_ll_ff_template_lead = ff_template_hist_xf.Integral(ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        #n_ll_ff_template_subl = ff_template_hist_fx.Integral(ff_fit_bins_subl[0], ff_fit_bins_subl[1] )
        #lead_norm = n_ll_target_lead / n_ll_ff_template_lead
        #subl_norm = n_ll_target_subl / n_ll_ff_template_subl
        #n_xf_target = xf_cr_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1]) - lead_norm*ff_template_hist_xf.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) 
        #n_fx_target = fx_cr_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1]) - subl_norm*ff_template_hist_fx.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] )

        #print 'ff subl_norm = %f' %subl_norm
        #print 'ff lead_norm = %f' %lead_norm

        #print 'Normalize lead distribution to %f in xf region' %n_xf_target
        #print 'Normalize subl distribution to %f in fx region' %n_fx_target

        #xf_norm = n_xf_target / rf_template_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) 
        #fx_norm = n_fx_target / fr_template_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] )

        #print 'Predict %f rf events in TT region' %( xf_norm * rf_template_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ) )
        #print 'Predict %f fr events in TT region' %( fx_norm * fr_template_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) )

        #print '%d data events in LL region ' %ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        #print 'Probability for f to be T = %f' %(tight_eff_bkg)
        #print 'Probability for f to be L = %f' %(loose_eff_bkg)
        #print 'Predict %f ff events in TT region' %( ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] ) * ( tight_eff_bkg*tight_eff_bkg) / (loose_eff_bkg*loose_eff_bkg) )
        
        

        ##print 'Fraction of fr events where lead passes Tight = %f' %fx_leadpassT_frac
        ##print 'Fraction of rf events where subl passes Tight = %f' %xf_sublpassT_frac

        ###Ntot * (1-frac) = NBkg
        ###Ntot * frac = NSig
        ###NSig = NBkg * frac/(1-frac)
        ###NBkg = norm*Integral( Lregion )
        ###NSig = norm*Integral( Lregion ) * frac/(1-frac)

        ##nbkg_rf = xf_norm*( (rf_template_hist.Integral()/2.) - rf_template_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ) )
        ##nbkg_fr = fx_norm*( (fr_template_hist.Integral()/2.) - fr_template_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ) )

        ##print 'N Bkg rf = %f' %nbkg_rf
        ##print 'N Bkg fr = %f' %nbkg_fr

        ##print 'Total N rf = %f' %( nbkg_rf/( 1-xf_sublpassT_frac) )
        ##print 'Total N fr = %f' %( nbkg_fr/( 1-fx_leadpassT_frac) )

        ##print 'RF factor = %f, FR factor = %f' %( xf_norm, fx_norm )
        ###print 'Predict %f rf events in TT region' %(xf_norm*rf_template_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ))
        ###print 'Predict %f fr events in TT region' %(fx_norm*fr_template_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ))

        ##print 'Predict %f rf events in TT region' %(nbkg_rf * xf_sublpassT_frac / ( 1-xf_sublpassT_frac ) )
        ##print 'Predict %f fr events in TT region' %(nbkg_fr * fx_leadpassT_frac / ( 1-fx_leadpassT_frac ) )

        ##nff_tot_lead = avg_norm*ff_template_hist.Integral()/2.
        ##nff_pass_tight = avg_norm*ff_template_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] )
        ##prob_pass = nff_pass_tight/nff_tot_lead
        ##prob_fail = 1-prob_pass

        ##print '%d data events in LL region ' %ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] )
        ##print 'Probability for f to be T = %f' %(prob_pass)
        ##print 'Predict %f ff events in TT region' %( ff_cr_hist.Integral( ff_fit_bins_lead[0], ff_fit_bins_lead[1] ) * ( prob_pass*prob_pass) / (prob_fail*prob_fail) )
        

    elif bkg_bins is not None and sig_bins is not None :


        print 'Normalize ff template in xf region in bin %d ' %bkg_bins[1]
        print 'Normalize ff template in fx region in bin %d'  %bkg_bins[0]
        
        #subl_norm = ff_cr_hist.GetBinContent( bkg_bins[0]) / ff_template_hist_fx.GetBinContent( bkg_bins[0] )
        #lead_norm = ff_cr_hist.GetBinContent( bkg_bins[1]) / ff_template_hist_xf.GetBinContent( bkg_bins[1] )
        #subl_norm = fx_cr_hist.GetBinContent( bkg_bins[0]) / ff_template_hist_fx.GetBinContent( bkg_bins[0] )
        #lead_norm = xf_cr_hist.GetBinContent( bkg_bins[1]) / ff_template_hist_xf.GetBinContent( bkg_bins[1] )

        print '%f events in subl LL region ' %fx_cr_hist.GetBinContent( bkg_bins[0]) 
        print '%f events in lead LL region ' %xf_cr_hist.GetBinContent( bkg_bins[1]) 
        print '%f events in fx signal region ' %fx_cr_hist.GetBinContent( sig_bins[0]) 
        print '%f events in xf signal region ' %xf_cr_hist.GetBinContent( sig_bins[1]) 
        print '%f events in fx ff template ' %ff_template_hist_fx.GetBinContent( bkg_bins[0] )
        print '%f events in xf ff template ' %ff_template_hist_xf.GetBinContent( bkg_bins[1] )

        print 'Normalize in xf region in bin %d ' %sig_bins[1]
        print 'Normalize in fx region in bin %d' %sig_bins[0]
        n_ll_target_lead = xf_cr_hist.GetBinContent( bkg_bins[1] )
        n_ll_target_subl = fx_cr_hist.GetBinContent( bkg_bins[0] )
        n_ll_ff_template_lead = bkg_hists[0].GetBinContent(bkg_bins[1] )
        n_ll_ff_template_subl = bkg_hists[1].GetBinContent(bkg_bins[0] )
        lead_norm = n_ll_target_lead / n_ll_ff_template_lead
        subl_norm = n_ll_target_subl / n_ll_ff_template_subl
        n_xf_target = xf_cr_hist.GetBinContent( sig_bins[1]) - lead_norm*bkg_hists[0].GetBinContent( sig_bins[1] ) 
        n_fx_target = fx_cr_hist.GetBinContent( sig_bins[0]) - subl_norm*bkg_hists[1].GetBinContent( sig_bins[0] )
        xf_lead_norm = n_xf_target / sig_hists[0].GetBinContent( sig_bins[1] ) 
        fx_subl_norm = n_fx_target / sig_hists[1].GetBinContent( sig_bins[0] )
        xf_subl_norm = xf_lead_norm * ( sig_hists[0].Integral() / ( bkg_hists[1].Integral() - bkg_hists[1].GetBinContent( sig_bins[0] ) ) )
        fx_lead_norm = fx_subl_norm * ( sig_hists[1].Integral() / ( bkg_hists[0].Integral() - bkg_hists[0].GetBinContent( sig_bins[1] ) ) )

        print 'N ff events in rf normalization region = ', lead_norm*bkg_hists[0].GetBinContent( sig_bins[1] )
        print 'N ff events in fr normalization region = ', subl_norm*bkg_hists[1].GetBinContent( sig_bins[0] )
        print 'N xf target = ', n_xf_target
        print 'N fx target = ', n_fx_target
        print 'rf norm = ', xf_lead_norm
        print 'fr norm = ', fx_lead_norm
        print 'N lead rf after norm = ',xf_lead_norm * ( sig_hists[0].Integral() ) 
        print 'N subl fr after norm = ',fx_subl_norm * ( sig_hists[1].Integral() ) 
        print 'N loose subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) - bkg_hists[1].GetBinContent( sig_bins[0] ) )
        print 'N loose lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) - bkg_hists[0].GetBinContent( sig_bins[1] ) )
        print 'N total subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) )
        print 'N total lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) )

        print 'Predict %f rf events in TT region' %( xf_subl_norm * bkg_hists[1].GetBinContent( sig_bins[0] ) )
        print 'Predict %f fr events in TT region' %( fx_lead_norm * bkg_hists[0].GetBinContent( sig_bins[1] ) )
        print '%d data events in LL region ' %ff_cr_hist.GetBinContent( bkg_bins[1] )
        print 'Probability for f to be T = %f' %(tight_eff_bkg)
        print 'Probability for f to be L = %f' %(loose_eff_bkg)
        print 'Predict %f ff events in TT region' %( ff_cr_hist.GetBinContent( bkg_bins[1] ) * ( tight_eff_bkg*tight_eff_bkg) / (loose_eff_bkg*loose_eff_bkg) )


        #n_ll_target_lead = xf_cr_hist.GetBinContent( bkg_bins[1] )
        #n_ll_target_subl = fx_cr_hist.GetBinContent( bkg_bins[0] )
        #n_ll_ff_template_lead = ff_template_hist_xf.GetBinContent( bkg_bins[1] )
        #n_ll_ff_template_subl = ff_template_hist_fx.GetBinContent( bkg_bins[0] )
        #lead_norm = n_ll_target_lead / n_ll_ff_template_lead
        #subl_norm = n_ll_target_subl / n_ll_ff_template_subl

        #print 'ff subl_norm = %f' %subl_norm
        #print 'ff lead_norm = %f' %lead_norm
        #

        #n_xf_target = xf_cr_hist.GetBinContent( sig_bins[1] ) - lead_norm*ff_template_hist_xf.GetBinContent( sig_bins[1] ) 
        #n_fx_target = fx_cr_hist.GetBinContent( sig_bins[0] ) - subl_norm*ff_template_hist_fx.GetBinContent( sig_bins[0] )  

        #print 'Normalize lead distribution to %f in xf region' %n_xf_target
        #print 'Normalize subl distribution to %f in fx region' %n_fx_target

        #xf_norm = n_xf_target / rf_template_hist.GetBinContent( sig_bins[1] ) 
        #fx_norm = n_fx_target / fr_template_hist.GetBinContent( sig_bins[0] ) 

        #print 'Predict %f rf events in TT region' %( xf_norm * rf_template_hist.GetBinContent( sig_bins[0] ) )
        #print 'Predict %f fr events in TT region' %( fx_norm * fr_template_hist.GetBinContent( sig_bins[1] ) )

        #print '%d data events in LL region ' %ff_cr_hist.GetBinContent( bkg_bins[1] )
        #print 'Probability for f to be T = %f' %(tight_eff_bkg)
        #print 'Probability for f to be L = %f' %(loose_eff_bkg)
        #print 'Predict %f ff events in TT region' %( ff_cr_hist.GetBinContent( bkg_bins[1] ) * ( tight_eff_bkg*tight_eff_bkg) / (loose_eff_bkg*loose_eff_bkg ) )
        
        #xf_sublpassT_frac = rf_template_hist.GetBinContent( sig_bins[0] ) / (rf_template_hist.Integral()/2.)
        #fx_leadpassT_frac = fr_template_hist.GetBinContent( sig_bins[1] ) / (fr_template_hist.Integral()/2.)

        #print 'Fraction of fr events where lead passes Tight = %f' %fx_leadpassT_frac
        #print 'Fraction of rf events where subl passes Tight = %f' %xf_sublpassT_frac

        ##Ntot * (1-frac) = NBkg
        ##Ntot * frac = NSig
        ##NSig = NBkg * frac/(1-frac)
        ##NBkg = norm*Integral( Lregion )
        ##NSig = norm*Integral( Lregion ) * frac/(1-frac)

        #nbkg_rf = xf_norm*( (rf_template_hist.Integral()/2.) - rf_template_hist.GetBinContent( sig_bins[0] ) )
        #nbkg_fr = fx_norm*( (fr_template_hist.Integral()/2.) - fr_template_hist.GetBinContent( sig_bins[1] ) )

        #total_rf = nbkg_rf/( 1-xf_sublpassT_frac)
        #total_fr = nbkg_fr/( 1-fx_leadpassT_frac) 

        #print 'N Bkg rf = %f' %nbkg_rf
        #print 'N Bkg fr = %f' %nbkg_fr

        #print 'Total N rf = %f' %( total_rf )
        #print 'Total N fr = %f' %( total_fr )

        #print 'RF factor = %f, FR factor = %f' %( xf_norm, fx_norm )
        ##print 'Predict %f rf events in TT region' %(xf_norm*rf_template_hist.Integral( sublsig_fit_bins[0], sublsig_fit_bins[1] ))
        ##print 'Predict %f fr events in TT region' %(fx_norm*fr_template_hist.Integral( leadsig_fit_bins[0], leadsig_fit_bins[1] ))

        #print 'Predict %f rf events in TT region' %(total_rf * xf_sublpassT_frac )
        #print 'Predict %f fr events in TT region' %(total_fr * fx_leadpassT_frac )

        #print 'RF factor = %f, FR factor = %f' %( xf_norm, fx_norm )
        #print 'Predict %f rf events in TT region' %( xf_norm*rf_template_hist.GetBinContent( sig_bins[0] ) )
        #print 'Predict %f fr events in TT region' %( fx_norm*fr_template_hist.GetBinContent( sig_bins[1] ) )
        #
        ## calculate probability of getting TT from ff

        #nff_tot_lead = avg_norm*ff_template_hist.Integral()/2.
        #nff_pass_tight = avg_norm*ff_template_hist.GetBinContent(sig_bins[1])
        #prob_pass = nff_pass_tight/nff_tot_lead
        #prob_fail = 1-prob_pass

        #print '%d data events in LL region ' %ff_cr_hist.GetBinContent( bkg_bins[0])
        #print 'Probability for f to be T = %f' %(prob_pass)
        #print 'Predict %f ff events in TT region' %( ff_cr_hist.GetBinContent( bkg_bins[0]) * ( prob_pass*prob_pass) / (prob_fail*prob_fail) )
        

    print 'subl FF factor = %f, lead FF factor = %f, average = %f' %( subl_norm, lead_norm, avg_norm )

    ff_template_hist_xfNew = bkg_hists[0].Clone('ffhistxfnew')
    ff_template_hist_xfNew.Scale( lead_norm )
    ff_template_hist_fxNew = bkg_hists[1].Clone('ffhistfxnew')
    ff_template_hist_fxNew.Scale( subl_norm )
    
    rf_template_histNew = sig_hists[0].Clone('rfhistnew')
    rf_template_histNew.Scale( xf_lead_norm )

    fr_template_histNew = sig_hists[1].Clone('frhistnew')
    fr_template_histNew.Scale( fx_subl_norm )

    ff_template_hist_fxNew.SetLineColor(ROOT.kRed)
    ff_template_hist_xfNew.SetLineColor(ROOT.kRed)
    rf_template_histNew.SetLineColor(ROOT.kMagenta+1)
    fr_template_histNew.SetLineColor(ROOT.kCyan+1)
    ff_template_hist_fxNew.SetMarkerColor(ROOT.kRed)
    ff_template_hist_xfNew.SetMarkerColor(ROOT.kRed)
    rf_template_histNew.SetMarkerColor(ROOT.kMagenta+1)
    fr_template_histNew.SetMarkerColor(ROOT.kCyan+1)

    ff_template_hist_fxNew.SetLineWidth(2)
    ff_template_hist_xfNew.SetLineWidth(2)
    rf_template_histNew.SetLineWidth(2)
    fr_template_histNew.SetLineWidth(2)

    ff_template_hist_fxNew.SetMarkerSize(0)
    ff_template_hist_xfNew.SetMarkerSize(0)
    rf_template_histNew.SetMarkerSize(0)
    fr_template_histNew.SetMarkerSize(0)

    ff_template_hist_fxNew.SetLineStyle(ROOT.kSolid)
    ff_template_hist_xfNew.SetLineStyle(ROOT.kSolid)
    rf_template_histNew.SetLineStyle(ROOT.kSolid)
    fr_template_histNew.SetLineStyle(ROOT.kSolid)

    rf_template_hist.Scale( xf_norm )
    fr_template_hist.Scale( fx_norm )
    ff_template_hist_xf.Scale( lead_norm)
    ff_template_hist_fx.Scale( subl_norm )

    ff_template_hist_xf.SetMarkerSize(0)
    ff_template_hist_xf.SetMarkerColor(ROOT.kBlack)
    ff_template_hist_fx.SetMarkerSize(0)
    ff_template_hist_fx.SetMarkerColor(ROOT.kBlack)
    #ffcanxf = ROOT.TCanvas('ffcanxf', 'ffcanxf')
    #draw_template_with_axis(ffcanxf, [ff_cr_hist, ff_template_hist_xf], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FF template'], outputName=fftempNorm_llName, plot_lead_subl=plot_lead_subl )
    #ffcanfx = ROOT.TCanvas('ffcanfx', 'ffcanfx')
    #draw_template_with_axis(ffcanfx, [ff_cr_hist, ff_template_hist_fx], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FF template'], outputName=fftempNorm_llName, plot_lead_subl=plot_lead_subl )
    #xfcan = ROOT.TCanvas('xfcan', 'xfcan')
    #draw_template_with_axis(xfcan, [xf_cr_hist, rf_template_hist, ff_template_hist_xf], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=rftempNorm_xlName, plot_lead_subl=plot_lead_subl)
    #fxcan = ROOT.TCanvas('fxcan', 'fxcan')
    #draw_template_with_axis(fxcan, [fx_cr_hist, fr_template_hist, ff_template_hist_fx], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FR template', 'FF template'], outputName=frtempNorm_lxName, plot_lead_subl=plot_lead_subl)

    xfcan = ROOT.TCanvas('xfcan', 'xfcan')
    draw_template_with_axis(xfcan, [xf_cr_hist, rf_template_histNew, ff_template_hist_xfNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=rftempNorm_xlName, plot_lead_subl=plot_lead_subl)
    fxcan = ROOT.TCanvas('fxcan', 'fxcan')
    draw_template_with_axis(fxcan, [fx_cr_hist, fr_template_histNew, ff_template_hist_fxNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FR template', 'FF template'], outputName=frtempNorm_lxName, plot_lead_subl=plot_lead_subl)


    if bkg_cut is not None and sig_cut is not None  :
        rf_fit_bins = ( rf_cr_hist.FindBin( bkg_cut[0][0] ), rf_cr_hist.FindBin( bkg_cut[0][1] ) )
        fr_fit_bins = ( rf_cr_hist.FindBin( bkg_cut[1][0] ), rf_cr_hist.FindBin( bkg_cut[1][1] ) )

        subl_sig_bins = ( rf_cr_hist.FindBin( sig_cut[0][0] ), rf_cr_hist.FindBin( sig_cut[0][1] ) )
        lead_sig_bins = ( rf_cr_hist.FindBin( sig_cut[1][0] ), rf_cr_hist.FindBin( sig_cut[1][1] ) )

        print 'Normalize in xf region betwen bins %d and %d' %rf_fit_bins
        print 'Normalize in fx region betwen bins %d and %d' %fr_fit_bins
        subl_ff_norm = ( rf_cr_hist.Integral( rf_fit_bins[0], rf_fit_bins[1]) - rf_template_hist.Integral( rf_fit_bins[0], rf_fit_bins[1] ) ) / ff_template_hist_xf.Integral( rf_fit_bins[0], rf_fit_bins[1] ) 
        lead_ff_norm = ( fr_cr_hist.Integral( fr_fit_bins[0], fr_fit_bins[1]) - fr_template_hist.Integral( fr_fit_bins[0], fr_fit_bins[1] ) ) / ff_template_hist_fx.Integral( fr_fit_bins[0], fr_fit_bins[1] ) 

        print 'Predict %f ff events in TT region using subl fit' %(subl_ff_norm*ff_template_hist_xf.Integral( subl_sig_bins[0], subl_sig_bins[1] ))
        print 'Predict %f ff events in TT region using lead fit' %(lead_ff_norm*ff_template_hist_fx.Integral( lead_sig_bins[0], lead_sig_bins[1] ))

    elif bkg_bins is not None and sig_bins is not None :

        print 'Normalize in xf region in bin %d ' %sig_bins[1]
        print 'Normalize in fx region in bin %d' %sig_bins[0]
        subl_ff_norm = ( rf_cr_hist.GetBinContent( bkg_bins[0] ) - rf_template_hist.GetBinContent( bkg_bins[0] ) ) / ff_template_hist_xf.GetBinContent( bkg_bins[0] ) 
        lead_ff_norm = ( fr_cr_hist.GetBinContent( bkg_bins[1] ) - fr_template_hist.GetBinContent( bkg_bins[1] ) ) / ff_template_hist_fx.GetBinContent( bkg_bins[1] ) 

        print 'Predict %f ff events in TT region using subl fit' %(subl_ff_norm*ff_template_hist_xf.GetBinContent( sig_bins[0] ))
        print 'Predict %f ff events in TT region using lead fit' %(lead_ff_norm*ff_template_hist_fx.GetBinContent( sig_bins[1] ))

    print 'Normalization ff in rf region = %f' %subl_ff_norm
    print 'Normalization ff in fr region = %f' %lead_ff_norm

    ff_template_hist_xf.Scale( subl_ff_norm )
    ff_template_hist_fx.Scale( lead_ff_norm )
    rfcan = ROOT.TCanvas('rfcan', 'rfcan')
    draw_template_with_axis(rfcan, [rf_cr_hist, rf_template_hist, ff_template_hist_xf], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=fftempNorm_rfName, plot_lead_subl=plot_lead_subl)
    frcan = ROOT.TCanvas('frcan', 'frcan')
    draw_template_with_axis(frcan, [fr_cr_hist, fr_template_hist, ff_template_hist_fx], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=fftempNorm_frName, plot_lead_subl=plot_lead_subl)

    #print "ff_cr_hist.Draw()"
    #ff_cr_hist.Draw()
    #ff_template_hist.Draw('samehist')
    #raw_input('continue')

    #print "xf_cr_hist.Draw()"
    #xf_cr_hist.Draw()
    #rf_template_hist.Draw('samehist')
    ##fr_template_hist.Draw('samehist')
    #ff_template_hist.Draw('samehist')
    #xfsum = rf_template_hist.Clone('xfsum')
    #xfsum.Add( ff_template_hist )
    #xfsum.SetLineColor( ROOT.kBlack )
    #xfsum.SetLineWidth( 3 )
    #xfsum.Draw('samehist')
    #raw_input('continue')

    #print "fx_cr_hist.Draw()"
    #fx_cr_hist.Draw()
    ##rf_template_hist.Draw('samehist')
    #fr_template_hist.Draw('samehist')
    #ff_template_hist.Draw('samehist')
    #fxsum = fr_template_hist.Clone( 'fxsum' )
    #fxsum.Add( ff_template_hist )
    #fxsum.SetLineColor( ROOT.kBlack )
    #fxsum.SetLineWidth( 3 )
    #fxsum.Draw('samehist')
    #raw_input('continue')

    #print "fr_cr_hist.Draw()"
    #fr_cr_hist.Draw()
    ##rf_template_hist.Draw('samehist')
    #fr_template_hist.Draw('samehist')
    #ff_template_hist.Draw('samehist')
    #frsum = fr_template_hist.Clone( 'frsum' )
    #frsum.Add( ff_template_hist )
    #frsum.SetLineColor( ROOT.kBlack )
    #frsum.SetLineWidth( 3 )
    #frsum.Draw('samehist')
    #raw_input('continue')

    #print "rf_cr_hist.Draw()"
    #rf_cr_hist.Draw()
    ##rf_template_hist.Draw('samehist')
    #rf_template_hist.Draw('samehist')
    #ff_template_hist.Draw('samehist')
    #rfsum = rf_template_hist.Clone( 'rfsum' )
    #rfsum.Add( ff_template_hist )
    #rfsum.SetLineColor( ROOT.kBlack )
    #rfsum.SetLineWidth( 3 )
    #rfsum.Draw('samehist')
    #raw_input('continue')

    #print "target_hist.Draw()"
    #target_hist.Draw()
    #rf_template_hist.Draw('samehist')
    #fr_template_hist.Draw('samehist')
    #ff_template_hist.Draw('samehist')
    #sum_hist = rf_template_hist.Clone('sum_hist')
    #sum_hist.Add(fr_template_hist)
    #sum_hist.Add(ff_template_hist)
    #sum_hist.SetLineWidth(3)
    #sum_hist.SetLineColor(ROOT.kBlack)
    #sum_hist.Draw('samehist')
    #raw_input('continue')

    #pmvar   = ROOT.RooRealVar('pmvar', 'pmvar', -0.03, 0.03 )
    #leadvar = ROOT.RooRealVar('leadvar', 'leadvar', 0., 0.03 )
    #sublvar = ROOT.RooRealVar('sublvar', 'sublvar', 0., 0.03 )

    #sigfrac  = ROOT.RooRealVar('sigfrac', 'sigfrac', 0.5, 0., 1.)
    #sigfrac2  = ROOT.RooRealVar('sigfrac2', 'sigfrac2', 0.5, 0., 1.)

    #leadsig_datahist = ROOT.RooDataHist( 'leadsig_hist', 'leadsig_hist', ROOT.RooArgList(leadvar), sig_template_hist) 
    #sublsig_datahist = ROOT.RooDataHist( 'sublsig_hist', 'sublsig_hist', ROOT.RooArgList(leadvar), sig_template_hist) 
    #leadbkg_datahist = ROOT.RooDataHist( 'leadbkg_hist', 'leadbkg_hist', ROOT.RooArgList(leadvar), bkg_template_hist ) 
    #sublbkg_datahist = ROOT.RooDataHist( 'sublbkg_hist', 'sublbkg_hist', ROOT.RooArgList(leadvar), bkg_template_hist ) 



    #leadsig_template = ROOT.RooHistPdf( 'leadsig_pdf', 'leadsig_pdf', ROOT.RooArgSet(leadvar), leadsig_datahist) 
    #sublsig_template = ROOT.RooHistPdf( 'sublsig_pdf', 'sublsig_pdf', ROOT.RooArgSet(leadvar), sublsig_datahist) 
    #leadbkg_template = ROOT.RooHistPdf( 'leadbkg_pdf', 'leadbkg_pdf', ROOT.RooArgSet(leadvar), leadbkg_datahist ) 
    #sublbkg_template = ROOT.RooHistPdf( 'sublbkg_pdf', 'sublbkg_pdf', ROOT.RooArgSet(leadvar), sublbkg_datahist ) 

    ##rf_template = ROOT.RooAddPdf( 'rf_template', 'rf_template', ROOT.RooArgList( leadsig_template, sublbkg_template ), 1.0 )
    ##ff_template = ROOT.RooAddPdf( 'ff_template', 'ff_template', ROOT.RooArgList( leadbkg_template, sublbkg_template ), 1.0 )
    ##rf_template = ROOT.RooAddPdf( 'rf_template', 'rf_template', leadsig_template, sublbkg_template , ROOT.RooFit.RooConst(1.0) )
    ##ff_template = ROOT.RooAddPdf( 'ff_template', 'ff_template', leadbkg_template, sublbkg_template , ROOT.RooFit.RooConst(1.0) )


    ##rf_template = ROOT.RooHistPdf( 'rf_template', 'rf_template', ROOT.RooArgSet(leadvar, sublvar), ROOT.RooArgList(leadsig_templatehist, sublbkg_templatehist ), 0 )
    ##fr_template = ROOT.RooHistPdf( 'fr_template', 'fr_template', ROOT.RooArgSet(leadvar, sublvar), ROOT.RooArgList(leadbkg_templatehist, sublsig_templatehist ), 0 )
    ##ff_template = ROOT.RooHistPdf( 'ff_template', 'ff_template', ROOT.RooArgSet(leadvar, sublvar), ROOT.RooArgList(leadbkg_templatehist, sublbkg_templatehist ), 0 )

    ##--------------------------------
    ## Use visualization histos
    ##--------------------------------

    #pmvar.setRange('low', -0.02, -0.012 )
    #pmvar.setRange('high', 0.012, 0.02 )

    #rf_data_hist = ROOT.RooDataHist( 'rf_data_hist', 'rf_data_hist', ROOT.RooArgList(pmvar), rf_template_hist )
    #fr_data_hist = ROOT.RooDataHist( 'fr_data_hist', 'fr_data_hist', ROOT.RooArgList(pmvar), fr_template_hist )
    #ff_data_hist = ROOT.RooDataHist( 'ff_data_hist', 'ff_data_hist', ROOT.RooArgList(pmvar), ff_template_hist )

    #rf_pdf = ROOT.RooHistPdf( 'rf_pdf', 'rf_pdf', ROOT.RooArgSet(pmvar), rf_data_hist)
    #fr_pdf = ROOT.RooHistPdf( 'fr_pdf', 'fr_pdf', ROOT.RooArgSet(pmvar), fr_data_hist)
    #ff_pdf = ROOT.RooHistPdf( 'ff_pdf', 'ff_pdf', ROOT.RooArgSet(pmvar), ff_data_hist)

    #target_datahist = ROOT.RooDataHist( 'target_datahist', 'target_datahist', ROOT.RooArgList( pmvar), target_hist )
    ##rf_cr_datahist = ROOT.RooDataHist( 'rf_cr_datahist', 'rf_cr_datahist', ROOT.RooArgList( pmvar), rf_cr_hist )

    #fffrac  = ROOT.RooRealVar('fffrac', 'fffrac', 0.5, 0., 1.)
    #rffrac  = ROOT.RooRealVar('rffrac2', 'rffrac2', 0.2, 0., 1.)
    #
    #model = ROOT.RooAddPdf( 'model', 'model', ROOT.RooArgList(ff_pdf, rf_pdf, fr_pdf), ROOT.RooArgList(fffrac, rffrac) )

    #frame = pmvar.frame()
    #target_datahist.plotOn( frame )
    #model.plotOn( frame )
    #model.plotOn( frame , ROOT.RooFit.Components('rf_pdf'), ROOT.RooFit.LineStyle(ROOT.kDashed))
    #model.plotOn( frame , ROOT.RooFit.Components('rf_pdf'), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kGreen ) )
    #model.plotOn( frame , ROOT.RooFit.Components('ff_pdf'), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) )

    #frame.Draw()

    #raw_input('continue')

    #crCat = ROOT.RooCategory( 'crCat', 'rf, fr, ff' )
    #crCat.defineType('rf')
    #crCat.defineType('fr')
    #crCat.defineType('ff')

    #fffrac_rf  = ROOT.RooRealVar('fffrac_rf', 'fffrac_rf', 0.5, 0., 1.)
    #fffrac_fr  = ROOT.RooRealVar('fffrac_fr', 'fffrac_fr', 0.5, 0., 1.)
    #rf_model = ROOT.RooAddPdf( 'rf_model', 'rf_model', ROOT.RooArgList(ff_pdf, rf_pdf), ROOT.RooArgList(fffrac_rf) )
    #fr_model = ROOT.RooAddPdf( 'fr_model', 'fr_model', ROOT.RooArgList(ff_pdf, fr_pdf), ROOT.RooArgList(fffrac_fr) )
    #ff_model = ROOT.RooAddPdf( 'ff_model', 'ff_model', ROOT.RooArgList( ff_pdf, rf_pdf, fr_pdf ), ROOT.RooArgList( fffrac, rffrac ) )

    #simModel = ROOT.RooSimultaneous( 'simModel', 'simModel', crCat )
    #simModel.addPdf( rf_model , 'rf' )
    #simModel.addPdf( fr_model, 'fr' )
    #simModel.addPdf( ff_model, 'ff' )

    #data_model = ROOT.RooDataHist( 'combData', 'combData', ROOT.RooArgList(pmvar), ROOT.RooFit.Index( crCat ), ROOT.RooFit.Import( 'rf', rf_cr_hist ), ROOT.RooFit.Import( 'fr', fr_cr_hist ), ROOT.RooFit.Import( 'ff', ff_cr_hist ) )

    #result = simModel.fitTo( data_model )
    #print result
    #if result != None :
    #    result.Print()


    ###result = model.fitTo( target_datahist )
    ##result = model.fitTo( target_datahist, ROOT.RooFit.Range('low,high') )
    ##if result != None :
    ##    result.Print()

    #frame_rf = pmvar.frame()
    #rf_data_hist.plotOn( frame_rf )
    #simModel.plotOn( frame_rf , ROOT.RooFit.Components( 'rf' ), ROOT.RooFit.LineColor(ROOT.kBlack) )
    #rf_model.plotOn( frame_rf , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kMagenta))
    #fr_model.plotOn( frame_rf , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kGreen ) )
    #ff_model.plotOn( frame_rf , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) )

    #frame_rf.Draw()

    #raw_input('continue')

    #frame_fr = pmvar.frame()

    #fr_data_hist.plotOn( frame_fr )
    #simModel.plotOn( frame_fr , ROOT.RooFit.Components( 'fr' ), ROOT.RooFit.LineColor(ROOT.kBlack) )
    #rf_model.plotOn( frame_fr , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kMagenta))
    #fr_model.plotOn( frame_fr , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kGreen ) )
    #ff_model.plotOn( frame_fr , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) )

    #frame_fr.Draw()

    #raw_input('continue')

    #frame_ff = pmvar.frame()

    #ff_data_hist.plotOn( frame_ff )
    #simModel.plotOn( frame_ff , ROOT.RooFit.Components( 'ff' ), ROOT.RooFit.LineColor(ROOT.kBlack) )
    #rf_model.plotOn( frame_ff , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kMagenta))
    #fr_model.plotOn( frame_ff , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kGreen ) )
    #ff_model.plotOn( frame_ff , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) )

    #frame_ff.Draw()

    #raw_input('continue')

    #frame = pmvar.frame()
    #target_datahist.plotOn( frame )
    ##simModel.plotOn( frame , ROOT.RooFit.LineColor(ROOT.kBlack) )
    #rf_model.plotOn( frame , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kMagenta))
    #fr_model.plotOn( frame , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kGreen ) )
    #ff_model.plotOn( frame , ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) )

    #frame.Draw()

    #raw_input('continue')


    ###--------------------------------
    ### Try RooSimultaneous
    ###--------------------------------

    ##lead_model = ROOT.RooAddPdf( 'lead_model', 'lead_model', leadsig_template, leadbkg_template, sigfrac )
    ##subl_model = ROOT.RooAddPdf( 'subl_model', 'subl_model', sublsig_template, sublbkg_template, sigfrac )

    ##phCat = ROOT.RooCategory( 'phCat', 'Leading or subleading' )
    ##phCat.defineType('lead')
    ##phCat.defineType('subl')

    ##data_model = ROOT.RooDataHist( 'combData', 'combData', ROOT.RooArgList(leadvar), ROOT.RooFit.Index( phCat ), ROOT.RooFit.Import( 'lead', rf_cr_hist_lead ), ROOT.RooFit.Import( 'subl', rf_cr_hist_subl ) )


    ##simModel = ROOT.RooSimultaneous( 'simModel', 'simModel', phCat )
    ##simModel.addPdf( lead_model, 'lead' )
    ##simModel.addPdf( subl_model, 'subl' )

    ##result = simModel.fitTo(data_model)
    ##result.Print()

    ##--------------------------------
    ## original
    ##--------------------------------

    ##model = ROOT.RooAddPdf( 'model', 'model', ROOT.RooArgList(rf_template, ff_template), ROOT.RooArgList(sigfrac) )

    ##target_lead_hist = ROOT.RooDataHist( 'target_lead_hist', 'target_lead_hist', ROOT.RooArgList( leadvar ), rf_cr_hist_lead )
    ##target_subl_hist = ROOT.RooDataHist( 'target_subl_hist', 'target_subl_hist', ROOT.RooArgList( sublvar ), rf_cr_hist_subl )

    ##target_lead_pdf = ROOT.RooHistPdf( 'target_lead_pdf', 'target_lead_pdf', ROOT.RooArgSet( leadvar ), target_lead_hist )
    ##target_subl_pdf = ROOT.RooHistPdf( 'target_subl_pdf', 'target_subl_pdf', ROOT.RooArgSet( sublvar ), target_subl_hist )

    ##target_template = ROOT.RooAddPdf( 'target_template', 'target_template', target_lead_pdf, target_subl_pdf, ROOT.RooFit.RooConst(1.0))

    ##result = model.fitTo( target_template )
    ##result.Print()

def clone_sample_and_draw( samp, var, sel, binning ) :
        global samples
        newSamp = samples.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
        samples.create_hist( newSamp, var, sel, binning )
        return newSamp.hist
                                       
def get_hists_and_fit( var, signal_selection, bkg_selection, target_selection, signal_sample, bkg_sample, target_sample, binning, fit_range, manual_sig_cut, manual_bkg_cut ) :
    
    global samples

    print signal_selection
    print bkg_selection
    print target_selection

    #generate histograms
    sig_template_hist = None
    bkg_template_hist = None

    sig_template_samp = samples.get_samples(name=signal_sample )
    if sig_template_samp :
        newEBSigsamp = samples.clone_sample( oldname=sig_template_samp[0].name, newname='DataSigTemplateEB', temporary=True )
        samples.create_hist( newEBSigsamp, var, signal_selection, binning )
        sig_template_hist = newEBSigsamp.hist

    #background template
    bkg_template_samp = samples.get_samples(name=bkg_sample)
    if bkg_template_samp :
        newEBBkgsamp = samples.clone_sample( oldname=bkg_template_samp[0].name, newname='DataMCSubBkgTemplateEB', temporary=True )
        samples.create_hist( newEBBkgsamp, var, bkg_selection , binning )
        bkg_template_hist = newEBBkgsamp.hist

    target_hist = None
    target_samp = samples.get_samples(name=target_sample)
    if target_samp :
        newEBTargetSamp = samples.clone_sample( oldname=target_samp[0].name, newname='DataTargetEB', temporary=True)
        samples.create_hist(newEBTargetSamp , var,target_selection , binning  )
        target_hist = newEBTargetSamp.hist

    sigmavar = ROOT.RooRealVar('sigmavar', 'sigmavar', binning[1], binning[2] )
    sigfrac  = ROOT.RooRealVar('sigfrac', 'sigfrac', 0.5, 0., 1.)

    sig_templatehist = ROOT.RooDataHist( 'sig_hist', 'sig_hist', ROOT.RooArgList(sigmavar), sig_template_hist ) 
    bkg_templatehist = ROOT.RooDataHist( 'bkg_hist', 'bkg_hist', ROOT.RooArgList(sigmavar), bkg_template_hist ) 

    sig_template = ROOT.RooHistPdf( 'sig_template', 'sig_template', ROOT.RooArgSet(sigmavar), sig_templatehist, 0 )
    bkg_template = ROOT.RooHistPdf( 'bkg_template', 'bkg_template', ROOT.RooArgSet(sigmavar), bkg_templatehist, 0 )

    model = ROOT.RooAddPdf( 'model', 'model', ROOT.RooArgList(sig_template, bkg_template), ROOT.RooArgList(sigfrac) )

    target_template = ROOT.RooDataHist( 'target_template', 'target_template', ROOT.RooArgList(sigmavar), target_hist)

    # do a manual fit before running the fitting
    bkg_bin_min = target_hist.FindBin( manual_bkg_cut[0] )
    bkg_bin_max = target_hist.FindBin( manual_bkg_cut[1] )
    sig_bin_min = target_hist.FindBin( manual_sig_cut[0] )
    sig_bin_max = target_hist.FindBin( manual_sig_cut[1] )

    n_target_bkg_pure = target_hist.Integral( bkg_bin_min, bkg_bin_max )
    n_bkg_bkg_pure = bkg_template_hist.Integral( bkg_bin_min, bkg_bin_max )

    bkg_norm = n_target_bkg_pure/n_bkg_bkg_pure
    print 'In bkg region between %f and %f ( %d and %d ), Ndata = %d, Nbkg = %f, norm= %f' %( manual_bkg_cut[0], manual_bkg_cut[1], bkg_bin_min, bkg_bin_max, n_target_bkg_pure, n_bkg_bkg_pure, bkg_norm )
    
    n_target_sig_pure = target_hist.Integral( sig_bin_min, sig_bin_max )
    n_bkg_sig_pure = bkg_template_hist.Integral( sig_bin_min, sig_bin_max )
    n_sig_sig_pure = sig_template_hist.Integral( sig_bin_min, sig_bin_max )

    sig_norm = ( n_target_sig_pure - n_bkg_sig_pure*bkg_norm ) / n_sig_sig_pure

    print 'In sig region between %f and %f ( %d and %d ), Ndata = %d, Nsig=%f, Nbkg = %f, norm= %f' %( manual_sig_cut[0], manual_sig_cut[1], sig_bin_min, sig_bin_max, n_target_sig_pure, n_sig_sig_pure, bkg_norm*n_bkg_bkg_pure, sig_norm )

    print 'Signal Fraction from manual fit =  %f ' %((sig_template_hist.Integral() * sig_norm ) / target_hist.Integral() )
    print 'Background Fraction from manual fit =  %f ' %((bkg_template_hist.Integral() * bkg_norm ) / target_hist.Integral() )
    print 'Signal fraction in background pure region = %f ' %((sig_template_hist.Integral( bkg_bin_min, bkg_bin_max ) * sig_norm ) / target_hist.Integral(bkg_bin_min, bkg_bin_max ) ) 


    #frame = sigmavar.frame()
    #result = model.fitTo( target_template, ROOT.RooFit.Range(fit_range[0], fit_range[1]) )
    ##result = model.fitTo( target_template )

    #target_template.plotOn( frame )
    #model.plotOn( frame )
    #model.plotOn( frame , ROOT.RooFit.Components('sig_template'), ROOT.RooFit.LineStyle(ROOT.kDashed))
    #model.plotOn( frame , ROOT.RooFit.Components('bkg_template'), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) )

    #frame.Draw()
    #chi2 = model.createChi2

    #frac = sigfrac.getVal()
    #ntot = target_hist.Integral()
    #nbkg_bkg = ntot * (1-frac) * ( bkg_template_hist.Integral( bkg_bin_min, bkg_bin_max )/ bkg_template_hist.Integral() )
    #nsig_sig = ntot * frac * ( sig_template_hist.Integral( sig_bin_min, sig_bin_max )/ sig_template_hist.Integral() )
    #nbkg_sig = ntot * (1-frac) * ( bkg_template_hist.Integral( sig_bin_min, sig_bin_max )/ bkg_template_hist.Integral() )
    #print 'With roofit, nbkg in bkg = %f, nbkg in sig = %f, nsig in sig = %f' %( nbkg_bkg, nbkg_sig, nsig_sig )
    #sigfrac.Print()
    #sig_template.Print()
    #bkg_template.Print()
    #target_template.Print()
    #model.Print()
    
    #bkg_template_hist_forscale = bkg_template_hist.Clone( 'bkg_template_hist_forscale' )
    #sig_template_hist_forscale = sig_template_hist.Clone( 'sig_template_hist_forscale' )

    #bkg_template_hist_forscale.Scale(  (1-frac) / bkg_template_hist_forscale.Integral() )
    #sig_template_hist_forscale.Scale(  frac / sig_template_hist_forscale.Integral() )

    #sig_template_hist_forscale.Add( bkg_template_hist_forscale )
    #print 'Fit chi2 = ', sig_template_hist_forscale.Chi2Test( target_hist, 'WWCHI2/NDF' )

    
    samples.create_top_canvas_for_ratio('can')
    samples.curr_canvases['can'].cd()
    target_hist.GetYaxis().SetTitle( 'Events / %.3f' %( (binning[2]-binning[1])/binning[0] ) )
    target_hist.Draw()
    bkg_template_hist.Scale( bkg_norm )
    sig_template_hist.Scale( sig_norm )

    bkg_template_hist.SetMarkerSize(0)
    sig_template_hist.SetMarkerSize(0)
    bkg_template_hist.SetLineColor( ROOT.kRed )
    sig_template_hist.SetLineColor( ROOT.kGreen-2 )
    bkg_template_hist.SetMarkerColor( ROOT.kRed )
    sig_template_hist.SetMarkerColor( ROOT.kGreen-2 )
    bkg_template_hist.SetLineWidth( 2 )
    sig_template_hist.SetLineWidth( 2 )

    bkg_template_hist.Draw('samehist')
    sig_template_hist.Draw('samehist')
    sumhist = sig_template_hist.Clone( 'sumhist' )
    sumhist.Add(bkg_template_hist )
    sumhist.SetLineColor( ROOT.kBlue-2)
    sumhist.SetLineWidth( 2 )
    sumhist.Draw('samehist')

    samples.create_standard_ratio_canvas()
    samples.set_canvas_default_formatting( samples.curr_canvases['can'], doratio=True, logy=False )

    samples.curr_canvases['top'].cd()
    samples.curr_canvases['can'].DrawClonePad()
    samples.curr_canvases['can'].SetLogy(1)
    leg = samples.create_standard_legend( 3, doratio=True )
    leg.AddEntry( target_hist, 'Data' )
    leg.AddEntry( bkg_template_hist, 'Fake template' )
    leg.AddEntry( sig_template_hist, 'Real template' )
    leg.AddEntry( sumhist, 'Template sum' )
    leg.Draw()

    samples.curr_canvases['bottom'].cd()
    ratiohist = target_hist.Clone('ratio')
    ratiohist.Divide( sumhist )

    tmpSamp = Sample('tmpSAmp')
    tmpSamp.hist = ratiohist
    samples.set_ratio_default_formatting( samples.curr_canvases['bottom'], [tmpSamp], doratio=True, rlabel='Data/Template' )

    ratiohist.GetXaxis().SetTitle( '#sigma i#eta i#eta' )
    ratiohist.Draw()

    
    print ' Chi square = ', sumhist.Chi2Test( target_hist, 'WWCHI2' )
    print ' Chi square/NDF = ', sumhist.Chi2Test( target_hist, 'WWCHI2/NDF' )

    samples.curr_canvases['top'].cd()

    chi2 = ROOT.TLatex( 0.8, 0.6, '#chi^{2}/NDF = %.2f' % sumhist.Chi2Test( target_hist, 'WWCHI2/NDF' ) )
    chi2.SetNDC()
    chi2.SetX(0.7)
    chi2.SetY(0.6)
    chi2.Draw()


    raw_input('continue')
    


main() 
