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

if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
else :
    ROOT.gROOT.SetBatch(False)

sampMan = None

def get_default_draw_commands( ) :

    return { 'real' :'mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 ' , 
             'fake' :'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ',
             #'fake' :'ph_n==2 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && ph_phDR>0.3  ',
             'xf_cr' : ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && m_phph>15 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 ',
             'fx_cr' : ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && m_phph>15 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 ',
             'ff_cr' : ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && m_phph>15 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 ',
           }

    #real_base = ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 %s && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4' %iso_cuts_single
    #fake_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 %s && leadPhot_leadLepDR>1 ' %iso_cuts_single
def get_default_samples( ) :

    return { 'real' : 'Wgamma', 'fake' : 'DataRealPhotonZgSub', 'target' : 'Data' }
    #return { 'real' : 'Wgamma', 'fake' : 'jetmon', 'target' : 'Data' }

    #real_sample = 'Data'
    #fake_sample = 'jetmon'
    #fake_sample = 'DataRealPhotonWgSub'
    #fake_sample = 'Zgammastar'

def get_default_binning() :

    return { 'EB' : (30, 0, 0.03), 'EE' : (20, 0, 0.1) }

def get_default_cuts() :

    #return { ('EB','EB') : { 'tight' : [(0    , 0.011 )]*2, 'loose' : [(0.01301, 0.299   )]*2 },
    #         ('EE','EE') : { 'tight' : [(0    , 0.033 )]*2, 'loose' : [(0.035 , 0.1   )]*2} ,
    #         ('EB','EE') : { 'tight' : [(0    , 0.011 ), (0    , 0.033 )], 'loose' : [(0.01301, 0.299   ),(0.035 , 0.1   )]} ,
    #         ('EE','EB') : { 'tight' : [(0    , 0.033 ), (0    , 0.011 )], 'loose' : [(0.035 , 0.1   ),(0.01301, 0.299   )]} ,
    #        }
             
    return { ('EB','EB') : { 'tight' : [(0    , 0.011 )]*2, 'loose' : [(0.01101, 0.299   )]*2 },
             ('EE','EE') : { 'tight' : [(0    , 0.033 )]*2, 'loose' : [(0.0331 , 0.99   )]*2} ,
             ('EB','EE') : { 'tight' : [(0    , 0.011 ), (0    , 0.033 )], 'loose' : [(0.01101, 0.299   ),(0.0331 , 0.99   )]} ,
             ('EE','EB') : { 'tight' : [(0    , 0.033 ), (0    , 0.011 )], 'loose' : [(0.0331 , 0.99   ),(0.01101, 0.299   )]} ,
            }
             

def main() :

    global sampMan

    if not options.baseDir.count('/eos/') and not os.path.isdir( options.baseDir ) :
        print 'baseDir not found!'
        return

    sampMan = SampleManager(options.baseDir, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)


    if options.samplesConf is not None :

        sampMan.ReadSamples( options.samplesConf )

        print 'Samples ready.\n'  

        print 'The draw syntax follows that of TTree.Draw.  Examples : '
        
        print 'sampMan.Draw(\'met_et\', \'EventWeight && passcut_ee==1\', \'(300, 0, 300)\'\n'

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

    #real_base = ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4'
    #signal_sample = 'Data'
    real_base = 'mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 ' %iso_cuts
    signal_sample = 'Wgamma'

    #fake_base =  ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 '
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < m 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_phoIsoCorr[0] > 2 && ph_phoIsoCorr[0] < 4   '
    fake_base = ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %iso_cuts
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_passChIsoCorrMedium[0] '
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && ph_passChIsoCorrMedium[0] '
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && !( ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25) '

    bkg_sample = 'DataRealPhotonZgSub'
    #bkg_sample = 'Zgammastar'

    #target_base = ' PUWeight * ( mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && mt_lep_met > 60 )'
    iso_cuts_subl = iso_cuts.replace('[0]', '[1]')
    iso_cuts_tot = iso_cuts + ' && ' + iso_cuts_subl
    target_bases = [
                    'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && ph_phDR>0.3 && !ph_passSIEIEMedium[1] ' %iso_cuts_tot,
                    #'el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && ph_phDR>1.0 && !ph_passSIEIEMedium[1] ' %iso_cuts_tot,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_chIsoCorr[1]< 5 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3  ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3  ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_chIsoCorr[1]< 5 && ph_phoIsoCorr[1] < 3  ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_chIsoCorr[1]< 5 && ph_neuIsoCorr[1] < 3  ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && %s && ph_phDR>0.3 ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_passPhoIsoCorrMedium[1] ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_passNeuIsoCorrMedium[1] ' %iso_cuts,
                    #'mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_passChIsoCorrMedium[1]  ' %iso_cuts,
                    #' mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s ' %iso_cuts
                   ]
    #target_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s ' %iso_cuts
    #target_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_chIsoCorr[1]< 5 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3  ' %iso_cuts
    #target_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_phDR>0.3 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3  ' %iso_cuts
    target_sample = 'Data'
    #target_sample = 'WjetsWgamma'

    #binning = [0.0, 0.003, 0.005, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013 , 0.015, 0.03]

    etacuts = ['ph_IsEB[0] ' , 'ph_IsEE[0]']

    manual_tight_cuts = [ ( 0.008, 0.011 ), (0.02, 0.035) ]
    manual_loose_cuts = [ (0.015, 0.03), ( 0.045, 0.06 ) ]
    fit_ranges = [( 0.008, 0.018 ), (0.015, 0.05) ]
    binning = [(30, 0, 0.03), (20, 0, 0.1)]

    #manual_tight_cuts = [ ( 0.00, 1.5 ), ( 0.0, 1.2 ) ]
    #manual_loose_cuts = [ ( 3, 50 ), ( 3, 50 ) ]
    #fit_ranges = [( 0.0, 10), (0.0, 10) ]
    #binning = [(50, 0, 50), (50, 0, 50)]

    
    var='ph_sigmaIEIE[0]'
    #var = 'ph_chIsoCorr[0]'

    for tb in target_bases :
        for ec, binn, tight_cuts, loose_cuts, fit_range in zip(etacuts, binning, manual_tight_cuts, manual_loose_cuts, fit_ranges ) :
            signal_selection = ' PUWeight * ( %s && %s ) ' %( real_base, ec ) 
            bkg_selection    = ' PUWeight * ( %s && %s ) ' %( fake_base   , ec ) 
            target_selection = ' PUWeight * ( %s && %s ) ' %( tb, ec ) 
            get_hists_and_fit( var, signal_selection, bkg_selection, target_selection, signal_sample, bkg_sample, target_sample, binn, fit_range, tight_cuts, loose_cuts )

    #for idx, min in enumerate( ptcuts[0:-1] ) :
    #    max = ptcuts[idx+1]
    #    for ec, binn, tight_cuts, loose_cuts, fit_range in zip(etacuts, binning, manual_tight_cuts, manual_loose_cuts, fit_ranges ) :
    #        signal_selection = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( real_base, min, max, ec ) 
    #        bkg_selection    = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( fake_base   , min, max, ec ) 
    #        target_selection = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( target_base, min, max, ec ) 

    #        get_hists_and_fit( var, signal_selection, bkg_selection, target_selection, signal_sample, bkg_sample, target_sample, binn, fit_range, tight_cuts, loose_cuts )

def DoDiPhotonSIEIETemplateFitSimple( outputDir=None) :

    outputDirNom = None
    outputDirAsym = None
    outputDirAsymVL = None
    outputDirAsymL = None
    outputDirLooseAsym = None
    outputDirLoose=None
    if outputDir is not None :
        outputDirNom = outputDir +'/JetFakeTemplateFitPlotsNomIsoInvChFakeTemp'
        outputDirLoose = outputDir +'/JetFakeTemplateFitPlotsLooseIso'
        outputDirAsym = outputDir +'/JetFakeTemplateFitPlotsAsymIso'
        outputDirAsymVL = outputDir +'/JetFakeTemplateFitPlotsAsymIsoVLoose'
        outputDirAsymL = outputDir +'/JetFakeTemplateFitPlotsAsymIsoLoose'
        outputDirLooseAsym = outputDir +'/JetFakeTemplateFitPlotsLooseAsymIso'
        #outputDir = outputDir +'/JetFakeTemplateFitPlotsLooseSublIsoNoLeadIso'

    #bins_coarse = [15, 25, 40, 80, 1000000 ] 
    bins_coarse = [ 15, 25 ] 
    #bins_coarse = [ 25, 40 ] 
    #bins_coarse = [ 40, 80 ] 
    #bins_coarse = [80, 1000000 ] 
    regions = [('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB'), ('EE', 'EE')]
    ##regions = [('EE', 'EB'), ('EE', 'EE')]

    #---------------------------------------
    # Nom iso
    #---------------------------------------
    #iso_cuts_nom = ' && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    #iso_cuts_real = iso_cuts_nom
    #iso_cuts_fake= ' && ph_passPhoIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 '
    ##iso_cuts_fake= iso_cuts_nom
    #iso_cuts_nom = iso_cuts_nom + iso_cuts_nom.replace('[0]', '[1]')

    ##config_nominal_fitting( iso_cuts_nom, iso_cuts_real, iso_cuts_fake, regions, outputDir=outputDirNom )
    #config_nomptbin_fitting( iso_cuts_nom, iso_cuts_real, iso_cuts_fake, regions, ptbinning=bins_coarse, outputDir=outputDirNom+'/CoarseBins' )

    ##---------------------------------------
    ## Loose iso
    ##---------------------------------------
    #iso_cuts_loose = ' && ph_chIsoCorr[0]< 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 '
    #iso_cuts_loose_real = iso_cuts_loose
    #iso_cuts_loose_fake= iso_cuts_loose
    #iso_cuts_loose = iso_cuts_loose + iso_cuts_loose.replace('[0]', '[1]')

    ##config_nominal_fitting( iso_cuts_loose, iso_cuts_loose_real, iso_cuts_loose_fake, regions, outputDir=outputDirLoose )
    #config_nomptbin_fitting( iso_cuts_loose, iso_cuts_loose_real, iso_cuts_loose_fake, regions, ptbinning=bins_coarse, outputDir=outputDirLoose+'/CoarseBins' )

    ##---------------------------------------
    ## AsymIso, NoIso
    ##---------------------------------------

    #iso_cuts_iso = ' && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    #iso_cuts_noiso = ' '
    #
    #config_asymiso_fitting( iso_str=iso_cuts_iso, noiso_str=iso_cuts_noiso, regions=regions, outputDir=outputDirAsym )

    ##config_asymisoptbin_fitting( iso_str=iso_cuts_iso, noiso_str=iso_cuts_noiso, ptbinning=bins_coarse, regions=regions, outputDir=outputDirAsym+'/CoarseBins' )

    #---------------------------------------
    # AsymIso, Loose2 Iso (nominal)
    #---------------------------------------

    iso_cuts_iso = ' && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    iso_cuts_noiso = ' && ph_chIsoCorr[0]< 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 '
    #iso_cuts_noiso = ' && ph_chIsoCorr[0]< 10 && ph_neuIsoCorr[0] < 6 && ph_phoIsoCorr[0] < 6 '
    
    #config_asymiso_fitting( iso_str=iso_cuts_iso, noiso_str=iso_cuts_noiso, regions=regions, outputDir=outputDirAsymL )
    config_asymisoptbin_fitting( iso_str=iso_cuts_iso, noiso_str=iso_cuts_noiso, ptbinning=bins_coarse, regions=regions, outputDir=outputDirAsymL+'/CoarseBins' )

    #---------------------------------------
    # Loose AsymIso, Loose Iso
    #---------------------------------------

    #iso_cuts_iso = ' && ph_chIsoCorr[0]< 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 '
    #iso_cuts_noiso = ' '
    #
    #config_asymiso_fitting( iso_str=iso_cuts_iso, noiso_str=iso_cuts_noiso, regions=regions, outputDir=outputDirLooseAsym )
    #config_asymisoptbin_fitting( iso_str=iso_cuts_iso, noiso_str=iso_cuts_noiso, ptbinning=bins_coarse, regions=regions, outputDir=outputDirLooseAsym+'/CoarseBins' )

def config_nominal_fitting( iso_cuts_nom, iso_cuts_real, iso_cuts_fake, regions, outputDir ) :

    draw_base = get_default_draw_commands()
    samples = get_default_samples()

    real_base = draw_base['real'] + iso_cuts_real
    fake_base = draw_base['fake'] + iso_cuts_fake
    xf_cr_base = draw_base['xf_cr'] + iso_cuts_nom
    fx_cr_base = draw_base['fx_cr'] + iso_cuts_nom
    ff_cr_base = draw_base['ff_cr'] + iso_cuts_nom


    plotbinning = get_default_binning()
    cuts = get_default_cuts()

    templates = get_single_photon_templates( real_base, fake_base, samples['real'], samples['fake'], plotbinning['EB'], plotbinning['EE'], outputDir=outputDir )

    # determine efficiency of signal cut in background template
    #print_template_efficiencies( templates, cuts[('EB', 'EB')]['tight'], cuts[('EB', 'EB')]['loose'], cuts[('EE', 'EE')]['tight'], cuts[('EE', 'EE')]['loose'] )


    for (r1, r2) in regions :

        templates_mod={}
        templates_mod['fake']={}
        templates_mod['real']={}

        templates_mod['fake']['lead'] = templates['fake'][r1]
        templates_mod['real']['lead'] = templates['real'][r1]
        templates_mod['fake']['subl'] = templates['fake'][r2]
        templates_mod['real']['subl'] = templates['real'][r2]

        namePostfix = '_%s-%s' %( r1, r2)

        results_reg = fit_diphoton_simple( templates_mod, xf_cr_base, fx_cr_base, ff_cr_base, samples['target'], [plotbinning[r1], plotbinning[r2]], [r1,r2], tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix=namePostfix )

        DumpStandardTables( results_reg, outputDir=outputDir, namePostfix=namePostfix )


def config_nomptbin_fitting( iso_cuts_nom, iso_cuts_real, iso_cuts_fake, regions, ptbinning, outputDir ) :

    draw_base = get_default_draw_commands()
    samples = get_default_samples()
    plotbinning = get_default_binning()
    cuts = get_default_cuts()

    real_base = draw_base['real'] + iso_cuts_real
    fake_base = draw_base['fake'] + iso_cuts_fake
    xf_cr_base = draw_base['xf_cr'] + iso_cuts_nom
    fx_cr_base = draw_base['fx_cr'] + iso_cuts_nom
    ff_cr_base = draw_base['ff_cr'] + iso_cuts_nom

    templates_nopt = get_single_photon_templates( real_base, fake_base, samples['real'], samples['fake'], plotbinning['EB'], plotbinning['EE'], outputDir=outputDir )
    for idx, min in enumerate( ptbinning[:-1] ) :
        max = ptbinning[idx+1]

        print 'ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)

        real_base_pt  = real_base  + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        fake_base_pt  = fake_base  + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        xf_cr_base_pt = xf_cr_base + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        fx_cr_base_pt = fx_cr_base + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        ff_cr_base_pt = ff_cr_base + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)

        namePostfix = '_pt_%d_%d' %(  min, max)

        templates = get_single_photon_templates( real_base_pt, fake_base_pt, samples['real'], samples['fake'], plotbinning['EB'], plotbinning['EE'], outputDir=outputDir, namePostfix=namePostfix )

        for (r1, r2) in regions :

            namePostfix = '_%s-%s_pt_%d_%d' %( r1, r2, min, max)

            templates_mod={}
            templates_mod['fake']={}
            templates_mod['real']={}
            templates_mod['fake']['lead'] = templates['fake'][r1]
            templates_mod['real']['lead'] = templates['real'][r1]
            templates_mod['fake']['subl'] = templates_nopt['fake'][r2]
            templates_mod['real']['subl'] = templates_nopt['real'][r2]

            results = fit_diphoton_simple( templates_mod, xf_cr_base_pt, fx_cr_base_pt, ff_cr_base_pt, samples['target'], [plotbinning[r1],plotbinning[r2]], [r1,r2], tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix=namePostfix )

            DumpStandardTables( results, outputDir=outputDir, namePostfix=namePostfix )

def config_asymiso_fitting(iso_str, noiso_str, regions, outputDir  ) :

    draw_base = get_default_draw_commands()
    samples = get_default_samples()
    binning = get_default_binning()
    cuts = get_default_cuts()

    real_base_iso = draw_base['real'] + iso_str
    fake_base_iso = draw_base['fake'] + iso_str
    templates_iso = get_single_photon_templates( real_base_iso, fake_base_iso, samples['real'], samples['fake'], binning['EB'], binning['EE'], outputDir=outputDir, namePostfix='_iso' )

    real_base_noiso = draw_base['real'] + noiso_str
    fake_base_noiso = draw_base['fake'] + noiso_str
    templates_noiso = get_single_photon_templates( real_base_noiso, fake_base_noiso, samples['real'], samples['fake'], binning['EB'], binning['EE'], outputDir=outputDir, namePostfix='_noiso' )

    lead_iso_cuts = iso_str.replace('[1]', '[0]') + noiso_str.replace( '[0]', '[1]' )
    subl_iso_cuts = iso_str.replace('[0]', '[1]') + noiso_str.replace( '[1]', '[0]' )

    xf_cr_base_leadiso = draw_base['xf_cr'] + lead_iso_cuts
    fx_cr_base_leadiso = draw_base['fx_cr'] + lead_iso_cuts
    ff_cr_base_leadiso = draw_base['ff_cr'] + lead_iso_cuts

    xf_cr_base_subliso = draw_base['xf_cr'] + subl_iso_cuts
    fx_cr_base_subliso = draw_base['fx_cr'] + subl_iso_cuts
    ff_cr_base_subliso = draw_base['ff_cr'] + subl_iso_cuts


    for (r1, r2) in regions:

        pos_str = '_%s-%s' %( r1, r2 )


        templates_mod_iso={}
        templates_mod_iso['fake']={}
        templates_mod_iso['real']={}
        templates_mod_iso['fake']['lead']= templates_iso['fake'][r1]
        templates_mod_iso['real']['lead']= templates_iso['real'][r1]
        templates_mod_iso['fake']['subl']= templates_iso['fake'][r2]
        templates_mod_iso['real']['subl']= templates_iso['real'][r2]

        templates_mod_noiso={}
        templates_mod_noiso['fake']={}
        templates_mod_noiso['real']={}
        templates_mod_noiso['fake']['lead']= templates_noiso['fake'][r1]
        templates_mod_noiso['real']['lead']= templates_noiso['real'][r1]
        templates_mod_noiso['fake']['subl']= templates_noiso['fake'][r2]
        templates_mod_noiso['real']['subl']= templates_noiso['real'][r2]

        DumpTemplateEfficiencies( templates_mod_iso,   tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix='_tempeff_iso'+pos_str )
        DumpTemplateEfficiencies( templates_mod_noiso, tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix='_tempeff_noiso'+pos_str )

        templates_mod_leadiso = {}
        templates_mod_leadiso['fake'] = {}
        templates_mod_leadiso['real'] = {}
        templates_mod_leadiso['fake']['lead']= templates_iso['fake'][r1]
        templates_mod_leadiso['real']['lead']= templates_iso['real'][r1]
        templates_mod_leadiso['fake']['subl']= templates_noiso['fake'][r2]
        templates_mod_leadiso['real']['subl']= templates_noiso['real'][r2]

        templates_mod_subliso = {}
        templates_mod_subliso['fake'] = {}
        templates_mod_subliso['real'] = {}
        templates_mod_subliso['fake']['lead']= templates_noiso['fake'][r1]
        templates_mod_subliso['real']['lead']= templates_noiso['real'][r1]
        templates_mod_subliso['fake']['subl']= templates_iso['fake'][r2]
        templates_mod_subliso['real']['subl']= templates_iso['real'][r2]

        results_lead_iso = fit_diphoton_simple( templates_mod_leadiso, xf_cr_base_leadiso, fx_cr_base_leadiso, ff_cr_base_leadiso, samples['target'], [binning[r1], binning[r2]], [r1,r2], tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix='_leadIsosublNoIso%s' %pos_str )

        results_subl_iso = fit_diphoton_simple( templates_mod_subliso, xf_cr_base_subliso, fx_cr_base_subliso, ff_cr_base_subliso, samples['target'], [binning[r1], binning[r2]], [r1,r2], tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix='_sublIsoleadNoIso%s' %pos_str )


        print 'results_lead_iso ' 
        for k, val in results_lead_iso['lead'].iteritems() :
            print '%s : %s' %(k, val[0].__str__())
        print 'results_subl_iso ' 
        for k, val in results_subl_iso['subl'].iteritems() :
            print '%s : %s' %(k, val[0].__str__())
        results_comb = collections.OrderedDict()
        results_comb['lead']=results_lead_iso['lead']
        results_comb['subl']=results_subl_iso['subl']

        num_str_eb = 'PUWeight * ( %s && ph_IsEB[0] && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f) ' %(( draw_base['fake']+iso_str), cuts[(r1,r2)]['loose'][0][0], cuts[(r1,r2)]['loose'][0][1] )
        den_str_eb = 'PUWeight * ( %s && ph_IsEB[0] && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f) ' %(( draw_base['fake']+noiso_str), cuts[(r1,r2)]['loose'][0][0], cuts[(r1,r2)]['loose'][0][1] )
                                                                                                                                          
        num_str_ee = 'PUWeight * ( %s && ph_IsEE[0] && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f) ' %(( draw_base['fake']+iso_str), cuts[(r1,r2)]['loose'][0][0], cuts[(r1,r2)]['loose'][0][1] )
        den_str_ee = 'PUWeight * ( %s && ph_IsEE[0] && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f) ' %(( draw_base['fake']+noiso_str), cuts[(r1,r2)]['loose'][0][0], cuts[(r1,r2)]['loose'][0][1] )

        eff_lead = 0.0
        eff_subl = 0.0
        if r1 == 'EB' :
            eff_lead = get_loose_iso_eff( samples['fake'], num=num_str_eb, den= den_str_eb, binning=binning['EB'] )
        else :
            eff_lead = get_loose_iso_eff( samples['fake'], num=num_str_ee, den= den_str_ee, binning=binning['EE'] )
        if r2 == 'EB' :
            eff_subl = get_loose_iso_eff( samples['fake'], num=num_str_eb, den= den_str_eb, binning=binning['EB'] )
        else :
            eff_subl = get_loose_iso_eff( samples['fake'], num=num_str_ee, den= den_str_ee, binning=binning['EE'] )

        results_comb['lead']['Iso eff'] = [eff_lead]
        results_comb['subl']['Iso eff'] = [eff_subl]

        results_comb['lead']['N predicted r+f in t+t with eff'] = [results_comb['lead']['N predicted r+f in t+t'][0]*eff_subl]
        results_comb['subl']['N predicted f+r in t+t with eff'] = [results_comb['subl']['N predicted f+r in t+t'][0]*eff_lead]

        namePostfix='_%s-%s' %(r1, r2)

        DumpAsymIsoTables( results_comb, outputDir=outputDir, namePostfix=namePostfix )

        DumpToPickle( results_lead_iso, outputDir, namePostfix=namePostfix+'_leadIsosublNoIso' )
        DumpToPickle( results_subl_iso, outputDir, namePostfix=namePostfix+'_sublIsoleadNoIso' )


def config_asymisoptbin_fitting(iso_str, noiso_str, ptbinning, regions, outputDir  ) :

    draw_base = get_default_draw_commands()
    samples = get_default_samples()
    binning = get_default_binning()
    cuts = get_default_cuts()

    real_base = draw_base['real'] + iso_str
    fake_base = draw_base['fake'] + iso_str

    lead_iso_cuts = iso_str.replace('[1]', '[0]') + noiso_str.replace( '[0]', '[1]' )
    subl_iso_cuts = iso_str.replace('[0]', '[1]') + noiso_str.replace( '[1]', '[0]' )

    xf_cr_base_leadiso = draw_base['xf_cr'] + lead_iso_cuts
    fx_cr_base_leadiso = draw_base['fx_cr'] + lead_iso_cuts
    ff_cr_base_leadiso = draw_base['ff_cr'] + lead_iso_cuts

    xf_cr_base_subliso = draw_base['xf_cr'] + subl_iso_cuts
    fx_cr_base_subliso = draw_base['fx_cr'] + subl_iso_cuts
    ff_cr_base_subliso = draw_base['ff_cr'] + subl_iso_cuts

    templates_nopt = get_single_photon_templates( real_base_pt, fake_base_pt, samples['real'], samples['fake'], binning['EB'], binning['EE'], outputDir=outputDir )
    for idx, min in enumerate(ptbinning[:-1]) :
        max = ptbinning[idx+1]

        xf_cr_base_leadiso_pt = xf_cr_base_leadiso + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        fx_cr_base_leadiso_pt = fx_cr_base_leadiso + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        ff_cr_base_leadiso_pt = ff_cr_base_leadiso + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)

        xf_cr_base_subliso_pt = xf_cr_base_subliso + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        fx_cr_base_subliso_pt = fx_cr_base_subliso + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        ff_cr_base_subliso_pt = ff_cr_base_subliso + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)

        real_base_pt  = real_base  + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        fake_base_pt  = fake_base  + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)

        templates = get_single_photon_templates( real_base_pt, fake_base_pt, samples['real'], samples['fake'], binning['EB'], binning['EE'], outputDir=outputDir, namePostfix=namePostfix )
        for (r1, r2) in regions :

            namePostfix = '_%s-%s_pt_%d_%d' %( r1, r2, min, max)

            templates_mod={}
            templates_mod['fake']={}
            templates_mod['real']={}
            templates_mod['fake']['lead']= templates['fake'][r1]
            templates_mod['real']['lead']= templates['real'][r1]
            templates_mod['fake']['subl']= templates_nopt['fake'][r2]
            templates_mod['real']['subl']= templates_nopt['real'][r2]


            results_lead_iso = fit_diphoton_simple( templates_mod, xf_cr_base_leadiso_pt, fx_cr_base_leadiso_pt, ff_cr_base_leadiso_pt, samples['target'], [binning[r1],binning[r2]], [r1,r2], tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix=namePostfix+'_leadIsosublNoIso' )

            results_subl_iso = fit_diphoton_simple( templates_mod, xf_cr_base_subliso_pt, fx_cr_base_subliso_pt, ff_cr_base_subliso_pt, samples['target'], [binning[r1],binning[r2]], [r1,r2], tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix=namePostfix+'_sublIsoleadNoIso' )

            results_comb = collections.OrderedDict()
            results_comb['lead']=results_lead_iso['lead']
            results_comb['subl']=results_subl_iso['subl']

            num_str_eb = 'PUWeight * ( %s && ph_IsEB[0] && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_pt[0] > %d && ph_pt[0] < %d) ' %(( draw_base['fake']+iso_str), cuts[('EB','EB')]['loose'][0][0], cuts[('EB','EB')]['loose'][0][1], min, max )
            den_str_eb = 'PUWeight * ( %s && ph_IsEB[0] && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_pt[0] > %d && ph_pt[0] < %d) ' %(( draw_base['fake']+noiso_str), cuts[('EB','EB')]['loose'][0][0], cuts[('EB','EB')]['loose'][0][1], min, max )

            num_str_ee = 'PUWeight * ( %s && ph_IsEE[0] && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_pt[0] > %d && ph_pt[0] < %d) ' %(( draw_base['fake']+iso_str), cuts[('EB','EB')]['loose'][0][0], cuts[('EB','EB')]['loose'][0][1], min, max )
            den_str_ee = 'PUWeight * ( %s && ph_IsEE[0] && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_pt[0] > %d && ph_pt[0] < %d) ' %(( draw_base['fake']+noiso_str), cuts[('EB','EB')]['loose'][0][0], cuts[('EB','EB')]['loose'][0][1], min, max )

            eff_lead = 0.0
            eff_subl = 0.0
            if r1 == 'EB' :
                eff_lead = get_loose_iso_eff( samples['fake'], num=num_str_eb, den= den_str_eb, binning=binning['EB'] )
            else :
                eff_lead = get_loose_iso_eff( samples['fake'], num=num_str_ee, den= den_str_ee, binning=binning['EE'] )
            if r2 == 'EB' :
                eff_subl = get_loose_iso_eff( samples['fake'], num=num_str_eb, den= den_str_eb, binning=binning['EB'] )
            else :
                eff_subl = get_loose_iso_eff( samples['fake'], num=num_str_ee, den= den_str_ee, binning=binning['EE'] )


            results_comb['lead']['Iso eff'] = [eff_lead]
            results_comb['subl']['Iso eff'] = [eff_subl]

            results_comb['lead']['N predicted r+f in t+t with eff'] = [results_comb['lead']['N predicted r+f in t+t'][0]*eff_subl]
            results_comb['subl']['N predicted f+r in t+t with eff'] = [results_comb['subl']['N predicted f+r in t+t'][0]*eff_lead]

            DumpToPickle( results_lead_iso, outputDir, namePostfix=namePostfix+'_leadIsosublNoIso' )
            DumpToPickle( results_subl_iso, outputDir, namePostfix=namePostfix+'_sublIsoleadNoIso' )

            DumpAsymIsoTables( results_comb, outputDir=outputDir, namePostfix=namePostfix )


def run_oneptbin_fits( real_base, fake_base, real_sample, fake_sample, xf_cr_base, fx_cr_base, ff_cr_base, target_sample, outputDir ) : 

    plotbinning = get_default_binning()
    cuts = get_default_cuts()

    templates = get_single_photon_templates( real_base, fake_base, real_sample, fake_sample, plotbinning['EB'], plotbinning['EE'], outputDir=outputDir )

    templates_mod={}
    templates_mod['fake']={}
    templates_mod['real']={}
    templates_mod['fake']['lead']= templates['fake'][position[0]]
    templates_mod['real']['lead']= templates['real'][position[0]]
    templates_mod['fake']['subl']= templates['fake'][position[1]]
    templates_mod['real']['subl']= templates['real'][position[1]]


    # determine efficiency of signal cut in background template
    #print_template_efficiencies( templates, cuts[('EB', 'EB')]['tight'], cuts[('EB', 'EB')]['loose'], cuts[('EE', 'EE')]['tight'], cuts[('EE', 'EE')]['loose'] )

    regions = [('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB'), ('EE', 'EE') ]
    for (r1, r2) in regions :

        namePostfix = '_%s-%s'%(r1,r2)
                           
        results = fit_diphoton_simple( templates_mod, xf_cr_base, fx_cr_base, ff_cr_base, target_sample, [plotbinning[r1], plotbinning[r2]], [r1,r2], tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix=namePostfix )

        DumpStandardTables( results, outputDir=outputDir, namePostfix=namePostfix )


def run_multptbin_fits( bins, subdir, real_base, fake_base, real_sample, fake_sample, xf_cr_base, fx_cr_base, ff_cr_base, target_sample, outputDir  ) :

    if outputDir is not None :
        outputDir = outputDir +'/'+subdir

    binning = get_default_binning()
    cuts = get_default_cuts()

    templates_nopt = get_single_photon_templates( real_base, fake_base, real_sample, fake_sample, binning['EB'], binning['EE'], outputDir=outputDir )

    for idx, min in enumerate(bins[:-1]) :
        max = bins[idx+1]

        real_base_pt  = real_base  + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        fake_base_pt  = fake_base  + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        xf_cr_base_pt = xf_cr_base + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        fx_cr_base_pt = fx_cr_base + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)
        ff_cr_base_pt = ff_cr_base + ' && ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)

        namePostfix='_pt_%d_%d' %( min, max)
        
        templates = get_single_photon_templates( real_base_pt, fake_base_pt, real_sample, fake_sample, binning['EB'], binning['EE'], outputDir=outputDir, namePostfix=namePostfix )

        print 'ph_pt[0] > %d && ph_pt[0] < %d' %( min, max)

        regions = [('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB'), ('EE', 'EE') ]
        for (r1, r2) in regions :

            namePostfix = namePostfix+'_%s-%s'%(r1,r2)

            templates_mod={}
            templates_mod['fake']={}
            templates_mod['real']={}
            templates_mod['fake']['lead']= templates['fake'][r1]
            templates_mod['real']['lead']= templates['real'][r1]
            templates_mod['fake']['subl']= templates_nopt['fake'][r2]
            templates_mod['real']['subl']= templates_nopt['real'][r2]

            results = fit_diphoton_simple( templates_mod, xf_cr_base_pt, fx_cr_base_pt, ff_cr_base_pt, target_sample, [binning[r1], binning[r2]], [r1,r2], tight_cut=cuts[(r1,r2)]['tight'], loose_cut=cuts[(r1,r2)]['loose'], outputDir=outputDir, namePostfix=namePostfix )
            DumpStandardTables( results, outputDir=outputDir, namePostfix=namePostfix )

def get_single_photon_templates( real_sel_base, fake_sel_base, real_sample, fake_sample, binning_eb, binning_ee, outputDir, namePostfix='' ) :

    results = {}

    real_selection = {}
    fake_selection = {}

    var = 'ph_sigmaIEIE[0]'

    real_selection['EB'] = ' PUWeight * ( %s && ph_IsEB[0] ) '    %( real_sel_base ) 
    real_selection['EE'] = ' PUWeight * ( %s && ph_IsEE[0] ) '    %( real_sel_base ) 
    fake_selection['EB'] = ' PUWeight * ( %s && ph_IsEB[0] ) '    %( fake_sel_base ) 
    fake_selection['EE'] = ' PUWeight * ( %s && ph_IsEE[0] ) '    %( fake_sel_base ) 

    real_template_hist = {}
    fake_template_hist = {}

    real_template_samp = sampMan.get_samples(name=real_sample )
    fake_template_samp = sampMan.get_samples(name=fake_sample )
    
    #real template
    if real_template_samp :
        real_template_hist['EB'] = clone_sample_and_draw( real_template_samp[0], var, real_selection['EB'], binning_eb ) 
        real_template_hist['EE'] = clone_sample_and_draw( real_template_samp[0], var, real_selection['EE'], binning_ee ) 

    #fake template
    if fake_template_samp :
        fake_template_hist['EB'] = clone_sample_and_draw( fake_template_samp[0], var, fake_selection['EB'], binning_eb ) 
        fake_template_hist['EE'] = clone_sample_and_draw( fake_template_samp[0], var, fake_selection['EE'], binning_ee ) 

    fake_template_hist['EB'].SetLineColor(ROOT.kRed)
    real_template_hist['EB'].SetLineColor(ROOT.kBlue-2)
    fake_template_hist['EE'].SetLineColor(ROOT.kRed)
    real_template_hist['EE'].SetLineColor(ROOT.kBlue-2)

    fake_temp_name_eb = None
    real_temp_name_eb = None
    fake_temp_name_ee = None
    real_temp_name_ee = None

    if outputDir is not None :
        fake_temp_name_eb = outputDir+'/fake_template_eb%s.pdf'%namePostfix
        fake_temp_name_ee = outputDir+'/fake_template_ee%s.pdf'%namePostfix
        real_temp_name_eb = outputDir+'/real_template_eb%s.pdf'%namePostfix
        real_temp_name_ee = outputDir+'/real_template_ee%s.pdf'%namePostfix

    faketemp_eb = ROOT.TCanvas('faketemp_eb', 'faketemp_eb')
    faketemp_ee = ROOT.TCanvas('faketemp_ee', 'faketemp_ee')
    realtemp_eb = ROOT.TCanvas('realtemp_eb', 'realtemp_eb')
    realtemp_ee = ROOT.TCanvas('realtemp_ee', 'realtemp_ee')

    draw_template(faketemp_eb, fake_template_hist['EB'], normalize=1, outputName=fake_temp_name_eb)
    draw_template(faketemp_ee, fake_template_hist['EE'], normalize=1, outputName=fake_temp_name_ee)
    draw_template(realtemp_eb, real_template_hist['EB'], normalize=1, outputName=real_temp_name_eb)
    draw_template(realtemp_ee, real_template_hist['EE'], normalize=1, outputName=real_temp_name_ee)

    results['real'] = real_template_hist
    results['fake'] = fake_template_hist

    return results

def get_loose_iso_eff( fake_samp, num, den, binning) :

    fake_template_samp = sampMan.get_samples(name=fake_samp )
    
    #real template
    if fake_template_samp :
        num_hist = clone_sample_and_draw( fake_template_samp[0], 'ph_sigmaIEIE[0]', num, binning ) 
        den_hist = clone_sample_and_draw( fake_template_samp[0], 'ph_sigmaIEIE[0]', den, binning ) 

        num_err = ROOT.Double()
        num_val = num_hist.IntegralAndError( 1, num_hist.GetNbinsX(), num_err )
        den_err = ROOT.Double()
        den_val = den_hist.IntegralAndError( 1, den_hist.GetNbinsX(), den_err )

        num_res = ufloat( num_val, num_err )
        den_res = ufloat( den_val, den_err )

        return (num_res/den_res)
    else :
        print 'Did not get the fake samples'
        return None


def DoDiPhotonSIEIETemplateFit( outputDir=None) :

    #iso_cuts_lead = '!ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    iso_cuts_lead = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    #iso_cuts_lead = 'ph_chIsoCorr[0]< 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 '
    iso_cuts_subl = iso_cuts_lead.replace('[0]', '[1]' ) 
    #iso_cuts_lead += ' && ph_pt[0]>40 '

    #real_base = ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4' %iso_cuts_lead
    #signal_sample = 'Data'
    real_base = 'mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 ' % iso_cuts_lead
    signal_sample = 'Wgamma'

    fake_base = ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %iso_cuts_lead
    #fake_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0] < 0.05 && %s && leadPhot_leadLepDR>1 ' %iso_cuts_lead

    bkg_sample = 'DataRealPhotonZgSub'
    #bkg_sample = 'DataRealPhotonWgSub'
    #bkg_sample = 'Zgammastar'

    target_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && ph_HoverE12[1] < 0.05 && %s' %(iso_cuts_lead, iso_cuts_subl )

    xf_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl)

    fx_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl)

    fr_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[0] && ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl )

    rf_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && ph_passSIEIEMedium[0] && !ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl)

    ff_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && %s && !ph_passSIEIEMedium[1] && !ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && %s ' %(iso_cuts_lead, iso_cuts_subl )
    target_sample = 'Data'
    #target_sample = 'WjetsWgamma'

    #binning = [0.0, 0.003, 0.005, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013 , 0.015, 0.03]


    #sampMan.CompareSelections( 'ph_sigmaIEIE[0]', [signal_selection, bkg_selection, target_selection], [signal_sample, bkg_sample, target_sample], binning, normalize=1 )
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

    tight_cuts_eb    = [( -0.011, 0     ), (0    , 0.011 )]
    loose_cuts_eb    = [( -0.299  , -0.01301), (0.01301, 0.299   )]
    #loose_cuts_eb    = [( -0.299  , -0.01401), (0.01401, 0.299   )]
    #loose_cuts_eb    = [( -0.299  , -0.01101), (0.01101, 0.299   )]
    tight_cuts_ee    = [( -0.033, 0     ), (0    , 0.033 )]
    loose_cuts_ee    = [( -0.1  , -0.04 ), (0.04 , 0.1   )]
    tight_cuts_eb_ee = [( -0.033, 0     ), (0    , 0.011 )]
    loose_cuts_eb_ee = [( -0.1  , -0.04 ), (0.013, 0.3   )]

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
    fit_diphoton( real_base, fake_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_eb, ['EB','EB'], tight_cut=tight_cuts_eb, loose_cut=loose_cuts_eb, outputDir=outputDir )
    #fit_diphoton( real_base, fake_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_var_eb, ['EB', 'EB'], sig_bins=sig_bins_eb, bkg_bins=bkg_bins_eb, outputDir=outputDirVarBins)
    #fit_diphoton( real_base, fake_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_eb_ee, ['EB','EE'], tight_cut=tight_cuts_eb_ee, loose_cut=loose_cuts_eb_ee, outputDir=outputDir )
    #fit_diphoton( real_base, fake_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_var_eb_ee, ['EB', 'EE'], sig_bins=sig_bins_eb_ee, bkg_bins=bkg_bins_eb_ee, outputDir=outputDirVarBins)
    fit_diphoton( real_base, fake_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_ee, ['EE','EE'], tight_cut=tight_cuts_ee, loose_cut=loose_cuts_ee, outputDir=outputDir )
    fit_diphoton( real_base, fake_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning_var_ee, ['EE', 'EE'], sig_bins=sig_bins_ee, bkg_bins=bkg_bins_ee, outputDir=outputDirVarBins)


    #for idx, min in enumerate( ptcuts[0:-1] ) :
    #    max = ptcuts[idx+1]
    #    for ec, binn, tight_cuts, loose_cuts, fit_range in zip(etacuts, binning, manual_tight_cuts, manual_loose_cuts, fit_ranges ) :
    #        signal_selection = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( real_base, min, max, ec ) 
    #        bkg_selection    = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( fake_base   , min, max, ec ) 
    #        target_selection = ' PUWeight * ( %s && ph_pt[0] > %d && ph_pt[0] < %d && %s ) ' %( target_base, min, max, ec ) 

    #        fit_diphoton( signal_selection, bkg_selection, target_selection, signal_sample, bkg_sample, target_sample, binn, fit_range, tight_cuts, loose_cuts )

def DoDiPhoton2DSIEIETemplateFit() :

    #real_base = ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4'
    #signal_sample = 'Data'
    real_base = 'mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25'
    signal_sample = 'Wgamma'

    #fake_base =  ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 '
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < m 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_phoIsoCorr[0] > 2 && ph_phoIsoCorr[0] < 4   '
    fake_base = ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 '
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_passChIsoCorrMedium[0] '
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]  && ph_passChIsoCorrMedium[0] '
    #fake_base =  ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && !( ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25) '

    bkg_sample = 'DataRealPhotonSub'
    #bkg_sample = 'Zgammastar'

    sig_template_hist = None
    bkg_template_hist = None

    signal_selection = ' PUWeight * ( %s && ph_IsEB[0] ) ' %( real_base ) 
    bkg_selection    = ' PUWeight * ( %s && ph_IsEB[0]) ' %( fake_base    ) 

    binning = (30, 0, 0.03)
    binning2d = ( 30, 0, 0.03, 30, 0, 0.03 )
    #binning2d = ( [0, 0.011, 0.03], [0, 0.011, 0.03] )

    sig_template_samp = sampMan.get_samples(name=signal_sample )
    sig_list = []
    bkg_list = []
    templateff1d = None

    if sig_template_samp :
        sig_list = sampMan.get_list_from_tree( 'ph_sigmaIEIE[0]', signal_selection, sig_template_samp[0] )

    bkg_template_samp = sampMan.get_samples(name=bkg_sample)
    if bkg_template_samp :
        bkg_list = sampMan.get_list_from_tree( 'ph_sigmaIEIE[0]', bkg_selection , bkg_template_samp[0] )
        newFF1DSamp    = sampMan.clone_sample( oldname=bkg_template_samp[0].name, newname='FF1d', temporary=True)
        sampMan.create_hist(newFF1DSamp, 'ph_sigmaIEIE[0]',bkg_selection, binning  )
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

    
    #target_base = ' PUWeight * ( mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && mt_lep_met > 60 )'
    target_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    #rf_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    #fr_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    rf_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && !ph_passSIEIEMedium[1] && ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    fr_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && !ph_passSIEIEMedium[0] && ph_passSIEIEMedium[1] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    ff_cr_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && ph_phDR > 0.3 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && !ph_passSIEIEMedium[1] && !ph_passSIEIEMedium[0] && ph_HoverE12[1] < 0.05 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
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

    target_samp = sampMan.get_samples(name=target_sample)
    if target_samp :
        newTargetSamp    = sampMan.clone_sample( oldname=target_samp[0].name, newname='DataTarget', temporary=True)
        sampMan.create_hist(newTargetSamp , 'ph_sigmaIEIE[1]:ph_sigmaIEIE[0]',target_selection , binning2d  )
        target_hist = newTargetSamp.hist

        newRFCRSamp    = sampMan.clone_sample( oldname=target_samp[0].name, newname='DataRFCR', temporary=True)
        sampMan.create_hist(newRFCRSamp , 'ph_sigmaIEIE[1]:ph_sigmaIEIE[0]', rf_cr_selection, binning2d  )
        rf_cr_hist = newRFCRSamp.hist

        newFRCRSamp    = sampMan.clone_sample( oldname=target_samp[0].name, newname='DataFRCR', temporary=True)
        sampMan.create_hist(newFRCRSamp , 'ph_sigmaIEIE[1]:ph_sigmaIEIE[0]', fr_cr_selection, binning2d  )
        fr_cr_hist = newFRCRSamp.hist

        newFFCRSamp    = sampMan.clone_sample( oldname=target_samp[0].name, newname='DataFFCR', temporary=True)
        sampMan.create_hist(newFFCRSamp , 'ph_sigmaIEIE[1]:ph_sigmaIEIE[0]', ff_cr_selection, binning2d  )
        ff_cr_hist = newFFCRSamp.hist
        newFFCRSamp1d    = sampMan.clone_sample( oldname=target_samp[0].name, newname='DataFFCR1d', temporary=True)
        sampMan.create_hist(newFFCRSamp1d , 'ph_sigmaIEIE[0]', ff_cr_selection, binning  )
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
        
def draw_template_with_axis(can, hists, normalize=False, first_hist_is_data=False, legend_entries=[], outputName=None) :

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
        global sampMan
        leg = sampMan.create_standard_legend( len(hists) )
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

    
def draw_template(can, hists, normalize=False, first_hist_is_data=False, legend_entries=[], outputName=None ) :

    if not isinstance(hists, list) :
        hists = [hists]

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
        global sampMan
        sampMan.legendTranslateX = -0.1
        leg = sampMan.create_standard_legend( len(hists) )
        if added_sum_hist :
            legend_entries.append( 'Template sum' )

        for ent, hist in zip( legend_entries, hists ) :
            leg.AddEntry( hist, ent )

        leg.Draw()
        
    if outputName is None :
        raw_input('continue')

    if outputName is not None :
        if not os.path.isdir( os.path.dirname(outputName) ) :
            os.makedirs( os.path.dirname(outputName) )

        can.SaveAs( outputName )

    

def fit_diphoton_simple( templates, xf_cr_base, fx_cr_base, ff_cr_base, target_sample, binning, position,  tight_cut=None, loose_cut=None, sig_bins=None, bkg_bins=None, outputDir=None, namePostfix='' ) :

    global sampMan

    sampMan.clear_hists()

    if not isinstance(binning, list ) :
        binning = [binning]*2

    sig_selection = []
    bkg_selection    = []
    xf_cr_selection  = []
    fx_cr_selection  = []
    ff_cr_selection  = []

    pos_string = None
    print 'POSITION'
    print position

    pos_string = 'ph_Is%s[0] && ph_Is%s[1]' %( position[0], position[1] )

    xf_cr_selection .append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[1] > %f  && ph_sigmaIEIE[1] < %f ) ' %( xf_cr_base , pos_string, loose_cut[1][0], loose_cut[1][1] ) ) )
    xf_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[1] > %f  && ph_sigmaIEIE[1] < %f ) ' %( xf_cr_base , pos_string, loose_cut[1][0], loose_cut[1][1] ) ) )
    fx_cr_selection .append( ( 'ph_sigmaIEIE[0]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f  && ph_sigmaIEIE[0] < %f ) ' %( fx_cr_base , pos_string, loose_cut[0][0], loose_cut[0][1] ) ) )
    fx_cr_selection .append( ( 'ph_sigmaIEIE[1]' , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f  && ph_sigmaIEIE[0] < %f ) ' %( fx_cr_base , pos_string, loose_cut[0][0], loose_cut[0][1] ) ) )
    ff_cr_selection .append( ( 'ph_sigmaIEIE[0]'    , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_sigmaIEIE[1] > %f && ph_sigmaIEIE[1] < %f  ) ' %( ff_cr_base , pos_string, loose_cut[1][0], loose_cut[1][1], loose_cut[0][0], loose_cut[0][1] ) ) )
    ff_cr_selection .append( ( 'ph_sigmaIEIE[1]'    , ' PUWeight * ( %s && %s && ph_sigmaIEIE[0] > %f && ph_sigmaIEIE[0] < %f && ph_sigmaIEIE[1] > %f && ph_sigmaIEIE[1] < %f  ) ' %( ff_cr_base , pos_string, loose_cut[1][0], loose_cut[1][1], loose_cut[0][0], loose_cut[0][1] ) ) )

    xf_cr_hists = None
    fx_cr_hists = None
    ff_cr_hists = None
    rf_cr_hists = None
    fr_cr_hists = None
    target_samp = sampMan.get_samples(name=target_sample)
    if target_samp :

        xf_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binn ) for binn, (var, sel) in zip(binning, xf_cr_selection)]

        fx_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binn ) for binn, (var, sel) in zip(binning, fx_cr_selection)]

        ff_cr_hists = [clone_sample_and_draw( target_samp[0], var, sel, binn ) for binn, (var, sel) in zip(binning, ff_cr_selection)]

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

    lead_fake_template = templates['fake']['lead']
    lead_real_template = templates['real']['lead']
    subl_fake_template = templates['fake']['subl']
    subl_real_template = templates['real']['subl']

    lead_fake_template.Scale(1.0/lead_fake_template.Integral())
    lead_real_template.Scale(1.0/lead_real_template.Integral())
    subl_fake_template.Scale(1.0/subl_fake_template.Integral())
    subl_real_template.Scale(1.0/subl_real_template.Integral())

    text_results = collections.OrderedDict()
    if loose_cut is not None and tight_cut is not None  :

        #tot/nTight = ( tot-nTight + nTight )/nTight = (tot-nTight)/nTight + 1 

        # get bins for doing integrals
        tight_bins_lead = ( xf_cr_hist_lead.FindBin( tight_cut[0][0] ) , xf_cr_hist_lead.FindBin( tight_cut[0][1] ) )
        tight_bins_subl = ( xf_cr_hist_subl.FindBin( tight_cut[1][0] ) , xf_cr_hist_subl.FindBin( tight_cut[1][1] ) )

        loose_bins_lead = ( xf_cr_hist_lead.FindBin( loose_cut[0][0] ) , xf_cr_hist_lead.FindBin( loose_cut[0][1] ) )
        loose_bins_subl = ( xf_cr_hist_subl.FindBin( loose_cut[1][0] ) , xf_cr_hist_subl.FindBin( loose_cut[1][1] ) )

        # integral of the fake template in the tight region
        integral_tight_ftemp_lead_err = ROOT.Double()
        integral_tight_ftemp_subl_err = ROOT.Double()
        integral_tight_ftemp_lead_val = lead_fake_template.IntegralAndError( tight_bins_lead[0], tight_bins_lead[1], integral_tight_ftemp_lead_err )
        integral_tight_ftemp_subl_val = subl_fake_template.IntegralAndError( tight_bins_subl[0], tight_bins_subl[1], integral_tight_ftemp_subl_err )

        n_tight_ftemp_lead  = ufloat( integral_tight_ftemp_lead_val, integral_tight_ftemp_lead_err )
        n_tight_ftemp_subl  = ufloat( integral_tight_ftemp_subl_val, integral_tight_ftemp_subl_err )

        # integral of the fake template in the loose region
        integral_loose_ftemp_lead_err = ROOT.Double()
        integral_loose_ftemp_subl_err = ROOT.Double()
        integral_loose_ftemp_lead_val = lead_fake_template.IntegralAndError( loose_bins_lead[0], loose_bins_lead[1], integral_loose_ftemp_lead_err )
        integral_loose_ftemp_subl_val = subl_fake_template.IntegralAndError( loose_bins_subl[0], loose_bins_subl[1], integral_loose_ftemp_subl_err )

        n_loose_ftemp_lead  = ufloat( integral_loose_ftemp_lead_val, integral_loose_ftemp_lead_err )
        n_loose_ftemp_subl  = ufloat( integral_loose_ftemp_subl_val, integral_loose_ftemp_subl_err )

        # integral of the real template in the tight region
        integral_tight_rtemp_lead_err = ROOT.Double()
        integral_tight_rtemp_subl_err = ROOT.Double()
        integral_tight_rtemp_lead_val = lead_real_template.IntegralAndError( tight_bins_lead[0], tight_bins_lead[1], integral_tight_rtemp_lead_err ) 
        integral_tight_rtemp_subl_val = subl_real_template.IntegralAndError( tight_bins_subl[0], tight_bins_subl[1], integral_tight_rtemp_subl_err )

        n_tight_rtemp_lead = ufloat( integral_tight_rtemp_lead_val, integral_tight_rtemp_lead_err )
        n_tight_rtemp_subl = ufloat( integral_tight_rtemp_subl_val, integral_tight_rtemp_subl_err )

        # integral of the real template in the loose region
        integral_loose_rtemp_lead_err = ROOT.Double()
        integral_loose_rtemp_subl_err = ROOT.Double()
        integral_loose_rtemp_lead_val = lead_real_template.IntegralAndError( loose_bins_lead[0], loose_bins_lead[1], integral_loose_rtemp_lead_err ) 
        integral_loose_rtemp_subl_val = subl_real_template.IntegralAndError( loose_bins_subl[0], loose_bins_subl[1], integral_loose_rtemp_subl_err )

        n_loose_rtemp_lead = ufloat( integral_loose_rtemp_lead_val, integral_loose_rtemp_lead_err )
        n_loose_rtemp_subl = ufloat( integral_loose_rtemp_subl_val, integral_loose_rtemp_subl_err )

        # get tight and loose cut efficiencies for the fake templates
        # we have to be careful with error propagation in this case
        # doing ( Ntot - NTight ) / NTight double counts stats because NTight is a subset of Ntot
        # instead do ( !nTight + nTight )/ nTight  = !nTight/nTight + 1

        # first get Ntot
        integral_tot_ftemp_lead_err = ROOT.Double()
        integral_tot_ftemp_subl_err = ROOT.Double()
        integral_tot_ftemp_lead_val = lead_fake_template.IntegralAndError(1, lead_fake_template.GetNbinsX(), integral_tot_ftemp_lead_err)
        integral_tot_ftemp_subl_val = subl_fake_template.IntegralAndError(1, subl_fake_template.GetNbinsX(), integral_tot_ftemp_subl_err)
        
        integral_tot_rtemp_lead_err = ROOT.Double()
        integral_tot_rtemp_subl_err = ROOT.Double()
        integral_tot_rtemp_lead_val = lead_real_template.IntegralAndError(1, lead_real_template.GetNbinsX(), integral_tot_rtemp_lead_err)
        integral_tot_rtemp_subl_val = subl_real_template.IntegralAndError(1, subl_real_template.GetNbinsX(), integral_tot_rtemp_subl_err)
        
        # !nTight is just the difference (no error propagation!)
        integral_nottight_ftemp_lead_val = integral_tot_ftemp_lead_val - n_tight_ftemp_lead.n
        integral_nottight_ftemp_subl_val = integral_tot_ftemp_subl_val - n_tight_ftemp_subl.n

        integral_nottight_rtemp_lead_val = integral_tot_rtemp_lead_val - n_tight_rtemp_lead.n
        integral_nottight_rtemp_subl_val = integral_tot_rtemp_subl_val - n_tight_rtemp_subl.n

        # calculate the error, but don't use error propagation because
        # this value should result from independent stats
        # instead, back out the original number of events
        # by taking a ratio of the square of the value to the square of the error
        # this method works regardless of overall normalziation factors applied to the templates
        alpha_ftemp_lead = integral_tot_ftemp_lead_err*integral_tot_ftemp_lead_err/integral_tot_ftemp_lead_val
        alpha_ftemp_subl = integral_tot_ftemp_subl_err*integral_tot_ftemp_subl_err/integral_tot_ftemp_subl_val

        alpha_rtemp_lead = integral_tot_rtemp_lead_err*integral_tot_rtemp_lead_err/integral_tot_rtemp_lead_val
        alpha_rtemp_subl = integral_tot_rtemp_subl_err*integral_tot_rtemp_subl_err/integral_tot_rtemp_subl_val

        
        integral_nottight_ftemp_lead_err = alpha_ftemp_lead * math.sqrt( integral_tot_ftemp_lead_err*integral_tot_ftemp_lead_err - integral_tight_ftemp_lead_err*integral_tight_ftemp_lead_err )
        integral_nottight_ftemp_subl_err = alpha_ftemp_subl * math.sqrt( integral_tot_ftemp_subl_err*integral_tot_ftemp_subl_err - integral_tight_ftemp_subl_err*integral_tight_ftemp_subl_err )

        integral_nottight_rtemp_lead_err = alpha_rtemp_lead * math.sqrt( integral_tot_rtemp_lead_err*integral_tot_rtemp_lead_err - integral_tight_rtemp_lead_err*integral_tight_rtemp_lead_err )
        integral_nottight_rtemp_subl_err = alpha_rtemp_subl * math.sqrt( integral_tot_rtemp_subl_err*integral_tot_rtemp_subl_err - integral_tight_rtemp_subl_err*integral_tight_rtemp_subl_err )

        # do the same four ops as above, but with loose
        integral_notloose_ftemp_lead_val = integral_tot_ftemp_lead_val - n_loose_ftemp_lead.n
        integral_notloose_ftemp_subl_val = integral_tot_ftemp_subl_val - n_loose_ftemp_subl.n

        integral_notloose_rtemp_lead_val = integral_tot_rtemp_lead_val - n_loose_rtemp_lead.n
        integral_notloose_rtemp_subl_val = integral_tot_rtemp_subl_val - n_loose_rtemp_subl.n

        integral_notloose_ftemp_lead_err = alpha_ftemp_lead * math.sqrt( integral_tot_ftemp_lead_err*integral_tot_ftemp_lead_err - integral_loose_ftemp_lead_err*integral_loose_ftemp_lead_err )
        integral_notloose_ftemp_subl_err = alpha_ftemp_subl * math.sqrt( integral_tot_ftemp_subl_err*integral_tot_ftemp_subl_err - integral_loose_ftemp_subl_err*integral_loose_ftemp_subl_err )

        integral_notloose_rtemp_lead_err = alpha_rtemp_lead * math.sqrt( integral_tot_rtemp_lead_err*integral_tot_rtemp_lead_err - integral_loose_rtemp_lead_err*integral_loose_rtemp_lead_err )
        integral_notloose_rtemp_subl_err = alpha_rtemp_subl * math.sqrt( integral_tot_rtemp_subl_err*integral_tot_rtemp_subl_err - integral_loose_rtemp_subl_err*integral_loose_rtemp_subl_err )


        # now we're ready to assign and the values
        n_nottight_ftemp_lead = ufloat( integral_nottight_ftemp_lead_val, integral_nottight_ftemp_lead_err )
        n_nottight_ftemp_subl = ufloat( integral_nottight_ftemp_subl_val, integral_nottight_ftemp_subl_err )

        n_notloose_ftemp_lead = ufloat( integral_notloose_ftemp_lead_val, integral_notloose_ftemp_lead_err )
        n_notloose_ftemp_subl = ufloat( integral_notloose_ftemp_subl_val, integral_notloose_ftemp_subl_err )

        n_nottight_rtemp_lead = ufloat( integral_nottight_rtemp_lead_val, integral_nottight_rtemp_lead_err )
        n_nottight_rtemp_subl = ufloat( integral_nottight_rtemp_subl_val, integral_nottight_rtemp_subl_err )

        n_notloose_rtemp_lead = ufloat( integral_notloose_rtemp_lead_val, integral_notloose_rtemp_lead_err )
        n_notloose_rtemp_subl = ufloat( integral_notloose_rtemp_subl_val, integral_notloose_rtemp_subl_err )

        # do ( !nTight + nTight )/ nTight  = !nTight/nTight + 1
        tight_eff_fake_lead = 1.0/( ( n_nottight_ftemp_lead )/( n_tight_ftemp_lead ) + 1 )
        tight_eff_fake_subl = 1.0/( ( n_nottight_ftemp_subl )/( n_tight_ftemp_subl ) + 1 )
        loose_eff_fake_lead = 1.0/( ( n_notloose_ftemp_lead )/( n_loose_ftemp_lead ) + 1 )
        loose_eff_fake_subl = 1.0/( ( n_notloose_ftemp_subl )/( n_loose_ftemp_subl ) + 1 )

        tight_eff_real_lead = 1.0/( ( n_nottight_rtemp_lead )/( n_tight_rtemp_lead ) + 1 )
        tight_eff_real_subl = 1.0/( ( n_nottight_rtemp_subl )/( n_tight_rtemp_subl ) + 1 )
        
        if n_loose_rtemp_lead.n != 0 :
            loose_eff_real_lead = 1.0/( ( n_notloose_rtemp_lead )/( n_loose_rtemp_lead ) + 1 )
        else :
            loose_eff_real_lead = ufloat( 0, 0, 0.0 )

        if n_loose_rtemp_subl.n != 0 :
            loose_eff_real_subl = 1.0/( ( n_notloose_rtemp_subl )/( n_loose_rtemp_subl ) + 1 )
        else :
            loose_eff_real_subl = ufloat(0, 0, 0.0)


        # integral of the data in the loose region
        integral_loose_data_lead      = xf_cr_hist_lead   .Integral(loose_bins_lead[0], loose_bins_lead[1] )
        integral_loose_data_subl      = fx_cr_hist_subl   .Integral(loose_bins_subl[0], loose_bins_subl[1] )

        n_loose_data_lead      = ufloat( integral_loose_data_lead      , math.sqrt( integral_loose_data_lead      ) )
        n_loose_data_subl      = ufloat( integral_loose_data_subl      , math.sqrt( integral_loose_data_subl      ) )

        # integral of the data (for debugging)
        integral_all_data_lead      = xf_cr_hist_lead   .Integral()
        integral_all_data_subl      = fx_cr_hist_subl   .Integral()

        n_all_data_lead      = ufloat( integral_all_data_lead      , math.sqrt( integral_all_data_lead      ) )
        n_all_data_subl      = ufloat( integral_all_data_subl      , math.sqrt( integral_all_data_subl      ) )

        # integral of the data in the tight region
        integral_tight_data_lead = xf_cr_hist_lead.Integral( tight_bins_lead[0], tight_bins_lead[1]) 
        integral_tight_data_subl = fx_cr_hist_subl.Integral( tight_bins_subl[0], tight_bins_subl[1]) 

        n_tight_data_lead = ufloat( integral_tight_data_lead, math.sqrt( integral_tight_data_lead ) )
        n_tight_data_subl = ufloat( integral_tight_data_subl, math.sqrt( integral_tight_data_subl ) )

        # integral of the ff data in the loose region
        integral_ff_data_lead = ff_cr_hist_lead.Integral( loose_bins_lead[0], loose_bins_lead[1] )
        integral_ff_data_subl = ff_cr_hist_subl.Integral( loose_bins_subl[0], loose_bins_subl[1] )

        n_ff_data_lead = ufloat( integral_ff_data_lead, math.sqrt( integral_ff_data_lead ) )
        n_ff_data_subl = ufloat( integral_ff_data_subl, math.sqrt( integral_ff_data_subl ) )
        

        # get normalization of fake template in the loose region
        # assume no real contribution (usually ~1%)
        lead_norm = n_loose_data_lead / n_loose_ftemp_lead
        subl_norm = n_loose_data_subl / n_loose_ftemp_subl

        
        # use above normalization to determine number of
        # fake events in tight region
        n_fake_tight_pred_lead = lead_norm*n_tight_ftemp_lead
        n_fake_tight_pred_subl = subl_norm*n_tight_ftemp_subl

        # get the number of expected real photon events in the tight region
        n_real_tight_pred_lead = n_tight_data_lead - n_fake_tight_pred_lead 
        n_real_tight_pred_subl = n_tight_data_subl - n_fake_tight_pred_subl

        #determine fake+real template normalization in tight region
        xf_lead_norm = n_real_tight_pred_lead / n_tight_rtemp_lead
        fx_subl_norm = n_real_tight_pred_subl / n_tight_rtemp_subl

        #above normalization gives the integral of the template of the other photon in the loose region
        #we want to know the integral of the other template in the tight region
        #first calculate a normalization of the fake template such that the integral
        #of the fake template in the loose region is equal to the 
        #to calculate this, just divide by the loose efficiency and multiply by the tight efficiency
        n_xf_tot_subl = (xf_lead_norm*n_tight_rtemp_lead) / loose_eff_fake_subl
        n_fx_tot_lead = (fx_subl_norm*n_tight_rtemp_subl) / loose_eff_fake_lead

        n_xf_tight_subl = n_xf_tot_subl*tight_eff_fake_subl
        n_fx_tight_lead = n_fx_tot_lead*tight_eff_fake_lead

        (n_real_tight_lead, n_real_loose_lead, n_fake_tight_lead, n_fake_loose_lead) = do_2bin_fit( nTight=n_tight_data_lead, nLoose=n_loose_data_lead, eff={'TeffF' : tight_eff_fake_lead, 'TeffR': tight_eff_real_lead, 'LeffF': loose_eff_fake_lead, 'LeffR' : loose_eff_real_lead} )
        (n_real_tight_subl, n_real_loose_subl, n_fake_tight_subl, n_fake_loose_subl) = do_2bin_fit( nTight=n_tight_data_subl, nLoose=n_loose_data_subl, eff={'TeffF' : tight_eff_fake_subl, 'TeffR': tight_eff_real_subl, 'LeffF': loose_eff_fake_subl, 'LeffR' : loose_eff_real_subl} )

        text_results['lead'] = collections.OrderedDict()
        text_results['subl'] = collections.OrderedDict()
        text_results['lead']['loose range'] = ['%.3f-%.3f' %(loose_cut[1][0]    , loose_cut[1][1]    ) ]
        text_results['lead']['loose bins']  = ['%d-%d'     %(loose_bins_lead[0] , loose_bins_lead[1] ) ]
        text_results['subl']['loose range'] = ['%.3f-%.3f' %(loose_cut[0][0]    , loose_cut[0][1]    ) ]
        text_results['subl']['loose bins']  = ['%d-%d'     %(loose_bins_subl[0] , loose_bins_subl[1] ) ]
        text_results['lead']['tight range'] = ['%.3f-%.3f' %(tight_cut[1][0]    , tight_cut[1][1]    ) ]
        text_results['lead']['tight bins']  = ['%d-%d'     %(tight_bins_lead[0] , tight_bins_lead[1] ) ]
        text_results['subl']['tight range'] = ['%.3f-%.3f' %(tight_cut[0][0]    , tight_cut[0][1]    ) ]
        text_results['subl']['tight bins']  = ['%d-%d'     %(tight_bins_subl[0] , tight_bins_subl[1] ) ]

        text_results['lead']['loose eff fake']                 = [loose_eff_fake_lead]
        text_results['subl']['loose eff fake']                 = [loose_eff_fake_subl]
        text_results['lead']['tight eff fake']                 = [tight_eff_fake_lead]
        text_results['subl']['tight eff fake']                 = [tight_eff_fake_subl]
        text_results['lead']['loose eff real']                 = [loose_eff_real_lead]
        text_results['subl']['loose eff real']                 = [loose_eff_real_subl]
        text_results['lead']['tight eff real']                 = [tight_eff_real_lead]
        text_results['subl']['tight eff real']                 = [tight_eff_real_subl]

        text_results['lead']['N data loose+loose']             = [n_loose_data_lead]
        text_results['subl']['N data loose+loose']             = [n_loose_data_subl]
        text_results['lead']['N data loose subl+tight']        = [n_tight_data_lead ]
        text_results['subl']['N data loose lead+tight']        = [n_tight_data_subl ]
        text_results['lead']['N data fake+fake']               = [(n_ff_data_lead)]
        text_results['subl']['N data fake+fake']               = [(n_ff_data_subl)]
        text_results['subl']['N data loose']                   = [n_all_data_lead]
        text_results['lead']['N data loose']                   = [n_all_data_subl]

        text_results['lead']['N fake template loose']          = [n_loose_ftemp_lead]
        text_results['subl']['N fake template loose']          = [n_loose_ftemp_subl]
        text_results['lead']['N fake template tight']          = [n_tight_ftemp_lead]
        text_results['subl']['N fake template tight']          = [n_tight_ftemp_subl]
        text_results['lead']['N real template tight']          = [n_tight_rtemp_lead]
        text_results['subl']['N real template tight']          = [n_tight_rtemp_subl]

        text_results['lead']['fake template loose norm']       = [lead_norm]
        text_results['subl']['fake template loose norm']       = [subl_norm]
        text_results['lead']['N ftemp normalized in loose']    = [(n_loose_ftemp_lead*lead_norm)]
        text_results['subl']['N ftemp normalized in loose']    = [(n_loose_ftemp_lead*subl_norm)]

        text_results['lead']['N predicted fake in tight']      = [n_fake_tight_pred_lead ]
        text_results['subl']['N predicted fake in tight']      = [n_fake_tight_pred_subl ]

        text_results['lead']['N predicted real in tight']      = [n_real_tight_pred_lead ]
        text_results['subl']['N predicted real in tight']      = [n_real_tight_pred_subl ]

        text_results['lead']['real template tight norm']       = [xf_lead_norm]
        text_results['subl']['real template tight norm']       = [fx_subl_norm]

        text_results['lead']['N rtemp normalized in tight']    = [(n_tight_rtemp_lead*xf_lead_norm)]
        text_results['subl']['N rtemp normalized in tight']    = [(n_tight_rtemp_subl*fx_subl_norm)]
    
        text_results['subl']['fake template ntot']             = [n_fx_tot_lead]
        text_results['lead']['fake template ntot']             = [n_xf_tot_subl]

        text_results['subl']['N predicted f+r in t+t']             = [n_fx_tight_lead]
        text_results['lead']['N predicted r+f in t+t']             = [n_xf_tight_subl]

        text_results['lead']['N predicted fake+fake in tight'] = [(n_ff_data_lead* ( tight_eff_fake_lead*tight_eff_fake_lead ) / ( loose_eff_fake_lead*loose_eff_fake_lead) )]
        text_results['subl']['N predicted fake+fake in tight'] = [(n_ff_data_subl* ( tight_eff_fake_subl*tight_eff_fake_subl ) / ( loose_eff_fake_subl*loose_eff_fake_subl) )]

        print 'LEAD'
        for key, val in text_results['lead'].iteritems() :
            print key, val[0]
        print 'SUBL'
        for key, val in text_results['subl'].iteritems() :
            print key, val[0]

        text_results['lead']['2d_nRT'] = [n_real_tight_lead]
        text_results['lead']['2d_nRL'] = [n_real_loose_lead]
        text_results['lead']['2d_nFT'] = [n_fake_tight_lead]
        text_results['lead']['2d_nFL'] = [n_fake_loose_lead]

        text_results['subl']['2d_nRT'] = [n_real_tight_subl]
        text_results['subl']['2d_nRL'] = [n_real_loose_subl]
        text_results['subl']['2d_nFT'] = [n_fake_tight_subl]
        text_results['subl']['2d_nFL'] = [n_fake_loose_subl]

        print '2d_results_lead : nRT = %s, nRL = %s, nFT = %s, nFL = %s'  % (n_real_tight_lead, n_real_loose_lead, n_fake_tight_lead, n_fake_loose_lead )
        print '2d_results_subl : nRT = %s, nRL = %s, nFT = %s, nFL = %s'  % (n_real_tight_subl, n_real_loose_subl, n_fake_tight_subl, n_fake_loose_subl )

        ### do a three bin fit

        # convert to ufloat for matrix manips
        eff_R_T_lead = tight_eff_real_lead
        eff_R_L_lead = loose_eff_real_lead
        eff_F_T_lead = tight_eff_fake_lead
        eff_F_L_lead = loose_eff_fake_lead
        
        eff_R_T_subl = tight_eff_real_subl
        eff_R_L_subl = loose_eff_real_subl
        eff_F_T_subl = tight_eff_fake_subl
        eff_F_L_subl = loose_eff_fake_subl
        
        print 'eff_R_T_lead'
        print eff_R_T_lead
        print 'eff_R_L_lead '
        print eff_R_L_lead 
        print 'eff_F_T_lead '
        print eff_F_T_lead 
        print 'eff_F_L_lead '
        print eff_F_L_lead 
        
        print 'eff_R_T_subl '
        print eff_R_T_subl 
        print 'eff_R_L_subl '
        print eff_R_L_subl 
        print 'eff_F_T_subl '
        print eff_F_T_subl 
        print 'eff_F_L_subl '
        print eff_F_L_subl 
        
        eff_RR_TT = eff_R_T_lead*eff_R_T_subl
        eff_RR_TL = eff_R_T_lead*eff_R_L_subl
        eff_RR_LT = eff_R_L_lead*eff_R_T_subl
        eff_RR_LL = eff_R_L_lead*eff_R_L_subl

        eff_RF_TT = eff_R_T_lead*eff_F_T_subl
        eff_RF_TL = eff_R_T_lead*eff_F_L_subl 
        eff_RF_LT = eff_R_L_lead*eff_F_T_subl
        eff_RF_LL = eff_R_L_lead*eff_F_L_subl

        eff_FR_TT = eff_F_T_lead*eff_R_T_subl
        eff_FR_TL = eff_F_T_lead*eff_R_L_subl
        eff_FR_LT = eff_F_L_lead*eff_R_T_subl
        eff_FR_LL = eff_F_L_lead*eff_R_L_subl

        eff_FF_TT = eff_F_T_lead*eff_F_T_subl
        eff_FF_TL = eff_F_T_lead*eff_F_L_subl
        eff_FF_LT = eff_F_L_lead*eff_F_T_subl
        eff_FF_LL = eff_F_L_lead*eff_F_L_subl


        text_results['eff_RR_TT'] = eff_RR_TT
        text_results['eff_RR_TL'] = eff_RR_TL
        text_results['eff_RR_LT'] = eff_RR_LT
        text_results['eff_RR_LL'] = eff_RR_LL

        text_results['eff_RF_TT'] = eff_RF_TT
        text_results['eff_RF_TL'] = eff_RF_TL
        text_results['eff_RF_LT'] = eff_RF_LT
        text_results['eff_RF_LL'] = eff_RF_LL

        text_results['eff_FR_TT'] = eff_FR_TT
        text_results['eff_FR_TL'] = eff_FR_TL
        text_results['eff_FR_LT'] = eff_FR_LT
        text_results['eff_FR_LL'] = eff_FR_LL

        text_results['eff_FF_TT'] = eff_FF_TT
        text_results['eff_FF_TL'] = eff_FF_TL
        text_results['eff_FF_LT'] = eff_FF_LT
        text_results['eff_FF_LL'] = eff_FF_LL


        big_matrix = unumpy.umatrix( [[ eff_RR_TT.n, eff_RF_TT.n, eff_FR_TT.n, eff_FF_TT.n ], [ eff_RR_TL.n, eff_RF_TL.n, eff_FR_TL.n, eff_FF_TL.n ], [eff_RR_LT.n, eff_RF_LT.n, eff_FR_LT.n, eff_FF_LT.n], [eff_RR_LL.n, eff_RF_LL.n, eff_FR_LL.n, eff_FF_LL.n]], 
                                     [[ eff_RR_TT.s, eff_RF_TT.s, eff_FR_TT.s, eff_FF_TT.s ], [ eff_RR_TL.s, eff_RF_TL.s, eff_FR_TL.s, eff_FF_TL.s ], [eff_RR_LT.s, eff_RF_LT.s, eff_FR_LT.s, eff_FF_LT.s], [eff_RR_LL.s, eff_RF_LL.s, eff_FR_LL.s, eff_FF_LL.s]] )


        eff_matrix = unumpy.umatrix( [[ eff_RF_TL.n, eff_FR_TL.n, eff_FF_TL.n ], [eff_RF_LT.n, eff_FR_LT.n, eff_FF_LT.n], [eff_RF_LL.n,eff_FR_LL.n, eff_FF_LL.n]], 
                                     [[ eff_RF_TL.s, eff_FR_TL.s, eff_FF_TL.s ], [eff_RF_LT.s, eff_FR_LT.s, eff_FF_LT.s], [eff_RF_LL.s,eff_FR_LL.s, eff_FF_LL.s]] )

        print 'big_matrix'
        print big_matrix

        print 'eff_matrix'
        print eff_matrix

        inv_matrix = eff_matrix.getI()
        print 'inv_matrix'
        print inv_matrix

        count_vector = unumpy.umatrix( [[n_tight_data_lead.n], [n_tight_data_subl.n], [n_loose_data_lead.n]],
                                                     [[n_tight_data_lead.s], [n_tight_data_subl.s], [n_loose_data_lead.s]] )

        print 'count_vector'
        print count_vector

        product = inv_matrix*count_vector
        print 'product'
        print product

        N_RF_TL = product.item(0)*eff_RF_TL
        N_RF_LT = product.item(0)*eff_RF_LT
        N_RF_LL = product.item(0)*eff_RF_LL
        N_RF_TT = product.item(0)*eff_RF_TT

        N_FR_TL = product.item(1)*eff_FR_TL
        N_FR_LT = product.item(1)*eff_FR_LT
        N_FR_LL = product.item(1)*eff_FR_LL
        N_FR_TT = product.item(1)*eff_FR_TT

        N_FF_TL = product.item(2)*eff_FF_TL
        N_FF_LT = product.item(2)*eff_FF_LT
        N_FF_LL = product.item(2)*eff_FF_LL
        N_FF_TT = product.item(2)*eff_FF_TT


        text_results['N_RF_TL'] = N_RF_TL
        text_results['N_RF_LT'] = N_RF_LT
        text_results['N_RF_LL'] = N_RF_LL
        text_results['N_RF_TT'] = N_RF_TT

        text_results['N_FR_TL'] = N_FR_TL
        text_results['N_FR_LT'] = N_FR_LT
        text_results['N_FR_LL'] = N_FR_LL
        text_results['N_FR_TT'] = N_FR_TT

        text_results['N_FF_TL'] = N_FF_TL
        text_results['N_FF_LT'] = N_FF_LT
        text_results['N_FF_LL'] = N_FF_LL
        text_results['N_FF_TT'] = N_FF_TT

        print 'Predicted in TT'
        print 'N_RF_TT = ', text_results['N_RF_TT'] 
        print 'N_FR_TT = ', text_results['N_FR_TT'] 
        print 'N_FF_TT = ', text_results['N_FF_TT'] 

        print 'Predicted in TL'
        print 'N_RF_TL = ', text_results['N_RF_TL'] 
        print 'N_FR_TL = ', text_results['N_FR_TL'] 
        print 'N_FF_TL = ', text_results['N_FF_TL'] 

        print 'Predicted in LT'
        print 'N_RF_LT = ', text_results['N_RF_LT'] 
        print 'N_FR_LT = ', text_results['N_FR_LT'] 
        print 'N_FF_LT = ', text_results['N_FF_LT'] 

        print 'Predicted in LL'
        print 'N_RF_LL = ', text_results['N_RF_LL'] 
        print 'N_FR_LL = ', text_results['N_FR_LL'] 
        print 'N_FF_LL = ', text_results['N_FF_LL'] 

        ###fit lead

        sigmavar = ROOT.RooRealVar('sigmavar', 'sigmavar', 0, 0.03 )
        sigfrac_lead  = ROOT.RooRealVar('sigfrac_lead', 'sigfrac_lead', 0.5, 0., 1.)
        sigfrac_subl  = ROOT.RooRealVar('sigfrac_subl', 'sigfrac_subl', 0.5, 0., 1.)

        sig_templatehist = ROOT.RooDataHist( 'sig_hist', 'sig_hist', ROOT.RooArgList(sigmavar), lead_real_template) 
        bkg_templatehist = ROOT.RooDataHist( 'bkg_hist', 'bkg_hist', ROOT.RooArgList(sigmavar), lead_fake_template) 

        sig_template = ROOT.RooHistPdf( 'sig_template', 'sig_template', ROOT.RooArgSet(sigmavar), sig_templatehist )
        bkg_template = ROOT.RooHistPdf( 'bkg_template', 'bkg_template', ROOT.RooArgSet(sigmavar), bkg_templatehist )

        model_lead = ROOT.RooAddPdf( 'model_lead', 'model_lead', ROOT.RooArgList(sig_template, bkg_template), ROOT.RooArgList(sigfrac_lead) )
        model_subl = ROOT.RooAddPdf( 'model_subl', 'model_subl', ROOT.RooArgList(sig_template, bkg_template), ROOT.RooArgList(sigfrac_subl) )

        target_template_lead = ROOT.RooDataHist( 'target_template_lead', 'target_template_lead', ROOT.RooArgList(sigmavar), xf_cr_hist_lead)
        target_template_subl = ROOT.RooDataHist( 'target_template_subl', 'target_template_subl', ROOT.RooArgList(sigmavar), xf_cr_hist_subl)

        print 'FIT LEAD'
        result_lead = model_lead.fitTo( target_template_lead, ROOT.RooFit.Range(0.0005, 0.025) )
        print 'FIT SUBL'
        result_subl = model_subl.fitTo( target_template_subl, ROOT.RooFit.Range(0.0005, 0.025) )
        print 'RESULT'
        ##result = model.fitTo( target_template )

        #target_template.plotOn( frame )
        #model.plotOn( frame )


    ff_template_hist_xfNew = lead_fake_template.Clone('ffhistxfnew')
    #ff_template_hist_xfNew.Scale( lead_norm.n)
    ff_template_hist_xfNew.Scale( ( product.item(2) * eff_FF_LL).n / ff_template_hist_xfNew.Integral(loose_bins_lead[0], loose_bins_lead[1]))
    ff_template_hist_fxNew = subl_fake_template.Clone('ffhistfxnew')
    #ff_template_hist_fxNew.Scale( subl_norm.n)
    ff_template_hist_fxNew.Scale( (product.item(2) * eff_FF_LL).n / ff_template_hist_fxNew.Integral(loose_bins_subl[0], loose_bins_subl[1]) )
    
    rf_template_histNew = lead_real_template.Clone('rfhistnew')
    #rf_template_histNew.Scale( xf_lead_norm.n)
    rf_template_histNew.Scale( (product.item(0)*eff_RF_TL).n/ rf_template_histNew.Integral(tight_bins_lead[0], tight_bins_lead[1]))

    fr_template_histNew = subl_real_template.Clone('frhistnew')
    #fr_template_histNew.Scale( fx_subl_norm.n)
    fr_template_histNew.Scale( (product.item(1)*eff_FR_LT).n / fr_template_histNew.Integral(tight_bins_subl[0], tight_bins_subl[1]) )

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

        rrtempName = outputDir + '/rr'+tempName
        rftempName = outputDir + '/rf'+tempName
        frtempName = outputDir + '/fr'+tempName
        fftempNamefx = outputDir + '/fffx'+tempName
        fftempNamexf = outputDir + '/ffxf'+tempName

        fftempNorm_llName = outputDir +'/ff_llregion_%s%s.pdf'%(tempNormName, namePostfix)
        rftempNorm_xlName = outputDir +'/rf_xlregion_%s%s.pdf'%(tempNormName, namePostfix)
        frtempNorm_lxName = outputDir +'/fr_lxregion_%s%s.pdf'%(tempNormName, namePostfix)
        fftempNorm_rfName = outputDir +'/ff_rfregion_%s%s.pdf'%(tempNormName, namePostfix)
        fftempNorm_frName = outputDir +'/ff_frregion_%s%s.pdf'%(tempNormName, namePostfix)

    xfcan = ROOT.TCanvas('xfcan', 'xfcan')
    draw_template(xfcan, [xf_cr_hist_lead, rf_template_histNew, ff_template_hist_xfNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=rftempNorm_xlName)

    #xfcan_subl = ROOT.TCanvas('xfcan_subl', 'xfcan_subl')
    #draw_template(xfcan_subl, [xf_cr_hist_subl, rf_template_histNew, ff_template_hist_xfNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=None)

    fxcan = ROOT.TCanvas('fxcan', 'fxcan')
    draw_template(fxcan, [fx_cr_hist_subl, fr_template_histNew, ff_template_hist_fxNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FR template', 'FF template'], outputName=frtempNorm_lxName)

    #fxcan_lead= ROOT.TCanvas('fxcan_lead', 'fxcan_lead')
    #draw_template(fxcan_lead, [fx_cr_hist_lead, fr_template_histNew, ff_template_hist_xfNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FR template', 'FR template'], outputName=None)

    return text_results

    #elif bkg_bins is not None and sig_bins is not None :


    #    print 'Normalize ff template in xf region in bin %d ' %bkg_bins[1]
    #    print 'Normalize ff template in fx region in bin %d'  %bkg_bins[0]
    #    
    #    print '%f events in subl LL region ' %fx_cr_hist_subl.GetBinContent( bkg_bins[0]) 
    #    print '%f events in lead LL region ' %xf_cr_hist_lead.GetBinContent( bkg_bins[1]) 
    #    print '%f events in fx signal region ' %fx_cr_hist_subl.GetBinContent( sig_bins[0]) 
    #    print '%f events in xf signal region ' %xf_cr_hist_lead.GetBinContent( sig_bins[1]) 
    #    print '%f events in fx ff template ' %subl_fake_template.GetBinContent( bkg_bins[0] )
    #    print '%f events in xf ff template ' %lead_fake_template.GetBinContent( bkg_bins[1] )

    #    print 'Normalize in xf region in bin %d ' %sig_bins[1]
    #    print 'Normalize in fx region in bin %d' %sig_bins[0]
    #    n_ll_target_lead = xf_cr_hist_lead.GetBinContent( bkg_bins[1] )
    #    n_ll_target_subl = fx_cr_hist_subl.GetBinContent( bkg_bins[0] )
    #    n_ll_ff_template_lead = lead_fake_template.GetBinContent(bkg_bins[1] )
    #    n_ll_ff_template_subl = subl_fake_template.GetBinContent(bkg_bins[0] )
    #    lead_norm = n_ll_target_lead / n_ll_ff_template_lead
    #    subl_norm = n_ll_target_subl / n_ll_ff_template_subl
    #    n_xf_target = xf_cr_hist_lead.GetBinContent( sig_bins[1]) - lead_norm*lead_fake_template.GetBinContent( sig_bins[1] ) 
    #    n_fx_target = fx_cr_hist_subl.GetBinContent( sig_bins[0]) - subl_norm*subl_fake_template.GetBinContent( sig_bins[0] )
    #    xf_lead_norm = n_xf_target / lead_real_template.GetBinContent( sig_bins[1] ) 
    #    fx_subl_norm = n_fx_target / subl_real_template.GetBinContent( sig_bins[0] )
    #    xf_subl_norm = xf_lead_norm * ( lead_real_template.Integral() / ( subl_fake_template.Integral() - subl_fake_template.GetBinContent( sig_bins[0] ) ) )
    #    fx_lead_norm = fx_subl_norm * ( subl_real_template.Integral() / ( lead_fake_template.Integral() - lead_fake_template.GetBinContent( sig_bins[1] ) ) )

    #    print 'N ff events in rf normalization region = ', lead_norm*lead_fake_template.GetBinContent( sig_bins[1] )
    #    print 'N ff events in fr normalization region = ', subl_norm*subl_fake_template.GetBinContent( sig_bins[0] )
    #    print 'N xf target = ', n_xf_target
    #    print 'N fx target = ', n_fx_target
    #    print 'rf norm = ', xf_lead_norm
    #    print 'fr norm = ', fx_lead_norm
    #    print 'N lead rf after norm = ',xf_lead_norm * ( lead_real_template.Integral() ) 
    #    print 'N subl fr after norm = ',fx_subl_norm * ( subl_real_template.Integral() ) 
    #    print 'N loose subl rf after norm = ', xf_subl_norm * ( subl_fake_template.Integral( ) - subl_fake_template.GetBinContent( sig_bins[0] ) )
    #    print 'N loose lead fr after norm = ', fx_lead_norm * ( lead_fake_template.Integral( ) - lead_fake_template.GetBinContent( sig_bins[1] ) )
    #    print 'N total subl rf after norm = ', xf_subl_norm * ( subl_fake_template.Integral( ) )
    #    print 'N total lead fr after norm = ', fx_lead_norm * ( lead_fake_template.Integral( ) )

    #    print 'Predict %f rf events in TT region' %( xf_subl_norm * subl_fake_template.GetBinContent( sig_bins[0] ) )
    #    print 'Predict %f fr events in TT region' %( fx_lead_norm * lead_fake_template.GetBinContent( sig_bins[1] ) )
    #    print '%d data events in LL region ' %ff_cr_hist_lead.GetBinContent( bkg_bins[1] )
    #    print 'Probability for f to be T = %f' %(tight_eff_fake)
    #    print 'Probability for f to be L = %f' %(loose_eff_fake)
    #    print 'Predict %f ff events in TT region' %( ff_cr_hist_lead.GetBinContent( bkg_bins[1] ) * ( tight_eff_fake*tight_eff_fake) / (loose_eff_fake*loose_eff_fake) )

def DumpStandardTables( text_results, outputDir, namePostfix='' ) :

    if outputDir is None :
        return

    latex_setup = collections.OrderedDict()
    latex_setup['']                  = ['Lead cuts', 'Sublead cuts']
    latex_setup['loose range']         = text_results['lead']['loose range']  +text_results['subl']['loose range']
    latex_setup['tight range']         = text_results['lead']['tight range']  +text_results['subl']['tight range']
    latex_setup['Fake $\epsilon_{L}$'] = text_results['lead']['loose eff fake']+text_results['subl']['loose eff fake']         
    latex_setup['Fake $\epsilon_{T}$'] = text_results['lead']['tight eff fake']+text_results['subl']['tight eff fake']           

    latex_results                      = collections.OrderedDict()
    latex_results[' ']                  = ['Subl is Loose', 'Lead is Loose']
    latex_results['Ndata Loose']       =  text_results['lead']['N data loose+loose']            + text_results['subl']['N data loose+loose']
    latex_results['Ndata Tight']       =  text_results['lead']['N data loose subl+tight']       + text_results['subl']['N data loose lead+tight']
    latex_results['Npred Tight fake']  =  text_results['lead']['N predicted fake in tight']     + text_results['subl']['N predicted fake in tight']
    latex_results['Npred Tight real']  =  text_results['lead']['N predicted real in tight']     + text_results['subl']['N predicted real in tight']
    latex_results['Npred RF in TT']    =  text_results['lead']['N predicted r+f in t+t']             + text_results['subl']['N predicted f+r in t+t']
    latex_results['Npred FF in TT']    =  text_results['lead']['N predicted fake+fake in tight']+ text_results['subl']['N predicted fake+fake in tight']

    latex_results_example              = collections.OrderedDict()
    latex_results_example['lab.'] = [' '] + latex_results[' '] + ['Eq.']
    latex_results_example['A']    = ['Ndata Loose'] + latex_results['Ndata Loose'] + ['-']
    latex_results_example['B']    = ['Ndata Tight'] + latex_results['Ndata Tight'] + ['-']
    latex_results_example['C']    = ['Fake $\epsilon_{L}$'] + latex_setup['Fake $\epsilon_{L}$'] + ['-']
    latex_results_example['D']    = ['Fake $\epsilon_{T}$'] + latex_setup['Fake $\epsilon_{T}$'] + ['-']
    latex_results_example['E']    = ['Npred Tight fake'] + latex_results['Npred Tight fake'] + ['A * D /C']
    latex_results_example['F']    = ['Npred Tight real'] + latex_results['Npred Tight real'] + ['B - E']
    latex_results_example['G']    = ['Npred RF in TT'] + latex_results['Npred RF in TT'] + ['F * D / C']
    latex_results_example['H']    = ['Npred FF in TT'] + latex_results['Npred FF in TT'] + ['A * DD/CC']

    latex_tab_setup = generate_latex_table( latex_setup )
    latex_tab_results = generate_latex_table( latex_results )
    latex_tab_results_example = generate_latex_table( latex_results_example )

    picfile = open( outputDir + '/results%s.pickle' %namePostfix, 'w' )
    pickle.dump( text_results, picfile )
    picfile.close()

    setuptexfile = open( outputDir + '/setup%s.tex' %namePostfix, 'w' )
    setuptexfile.write(latex_tab_setup)
    setuptexfile.close()

    resultstexfile = open( outputDir + '/results%s.tex' %namePostfix, 'w' )
    resultstexfile.write(latex_tab_results)
    resultstexfile.close()
    
    resultstexfileex = open( outputDir + '/results_example%s.tex' %namePostfix, 'w' )
    resultstexfileex.write(latex_tab_results_example)
    resultstexfileex.close()
        
def DumpAsymIsoTables( text_results, outputDir, namePostfix='' ) :

    latex_setup = collections.OrderedDict()
    latex_setup['']                  = ['Lead cuts', 'Sublead cuts']
    latex_setup['loose range']         = text_results['lead']['loose range']  +text_results['subl']['loose range']
    latex_setup['tight range']         = text_results['lead']['tight range']  +text_results['subl']['tight range']
    latex_setup['Fake $\epsilon_{L}$'] = text_results['lead']['loose eff fake']+text_results['subl']['loose eff fake']         
    latex_setup['Fake $\epsilon_{T}$'] = text_results['lead']['tight eff fake']+text_results['subl']['tight eff fake']           
    latex_setup['Iso efficiency']      = text_results['lead']['Iso eff']+text_results['subl']['Iso eff']           

    latex_results                            = collections.OrderedDict()
    latex_results[' ']                       = ['Subl is Loose', 'Lead is Loose']
    latex_results['Ndata Loose']             =  text_results['lead']['N data loose+loose']              + text_results['subl']['N data loose+loose']
    latex_results['Ndata Tight']             =  text_results['lead']['N data loose subl+tight']         + text_results['subl']['N data loose lead+tight']
    latex_results['Npred Tight fake']        =  text_results['lead']['N predicted fake in tight']       + text_results['subl']['N predicted fake in tight']
    latex_results['Npred Tight real']        =  text_results['lead']['N predicted real in tight']       + text_results['subl']['N predicted real in tight']
    latex_results['Npred RF in TT']          =  text_results['lead']['N predicted r+f in t+t']          + text_results['subl']['N predicted f+r in t+t']
    latex_results['Npred RF in TT with eff'] =  text_results['lead']['N predicted r+f in t+t with eff'] + text_results['subl']['N predicted f+r in t+t with eff']
    latex_results['Npred FF in TT ']         =  text_results['lead']['N predicted fake+fake in tight']  + text_results['subl']['N predicted fake+fake in tight']

    latex_tab_setup = generate_latex_table( latex_setup )
    latex_tab_results = generate_latex_table( latex_results )

    picfile = open( outputDir + '/results%s.pickle' %namePostfix, 'w' )
    pickle.dump( text_results, picfile )
    picfile.close()

    setuptexfile = open( outputDir + '/setup%s.tex' %namePostfix, 'w' )
    setuptexfile.write(latex_tab_setup)
    setuptexfile.close()

    resultstexfile = open( outputDir + '/results%s.tex' %namePostfix, 'w' )
    resultstexfile.write(latex_tab_results)
    resultstexfile.close()

def DumpToPickle( text_results, outputDir, namePostfix ) :

    picfile = open( outputDir + '/results%s.pickle' %namePostfix, 'w' )
    pickle.dump( text_results, picfile )
    picfile.close()

def DumpTemplateEfficiencies( templates, tight_cut, loose_cut, outputDir, namePostfix='' ) :

    lead_fake_template = templates['fake']['lead']
    lead_real_template = templates['real']['lead']
    subl_fake_template = templates['fake']['subl']
    subl_real_template = templates['real']['subl']

    # get bins for doing integrals
    tight_bins_lead = ( lead_fake_template.FindBin( tight_cut[0][0] ) , lead_fake_template.FindBin( tight_cut[0][1] ) )
    tight_bins_subl = ( subl_fake_template.FindBin( tight_cut[1][0] ) , subl_fake_template.FindBin( tight_cut[1][1] ) )

    loose_bins_lead = ( lead_fake_template.FindBin( loose_cut[0][0] ) , lead_fake_template.FindBin( loose_cut[0][1] ) )
    loose_bins_subl = ( subl_fake_template.FindBin( loose_cut[1][0] ) , subl_fake_template.FindBin( loose_cut[1][1] ) )

    # integral of the fake template in the tight region
    integral_tight_ftemp_lead_err = ROOT.Double()
    integral_tight_ftemp_subl_err = ROOT.Double()
    integral_tight_ftemp_lead_val = lead_fake_template.IntegralAndError( tight_bins_lead[0], tight_bins_lead[1], integral_tight_ftemp_lead_err )
    integral_tight_ftemp_subl_val = subl_fake_template.IntegralAndError( tight_bins_subl[0], tight_bins_subl[1], integral_tight_ftemp_subl_err )

    n_tight_ftemp_lead  = ufloat( integral_tight_ftemp_lead_val/lead_fake_template.Integral(), integral_tight_ftemp_lead_err/lead_fake_template.Integral() )
    n_tight_ftemp_subl  = ufloat( integral_tight_ftemp_subl_val/subl_fake_template.Integral() , integral_tight_ftemp_subl_err/subl_fake_template.Integral() )

    # integral of the fake template in the loose region
    integral_loose_ftemp_lead_err = ROOT.Double()
    integral_loose_ftemp_subl_err = ROOT.Double()
    integral_loose_ftemp_lead_val = lead_fake_template.IntegralAndError( loose_bins_lead[0], loose_bins_lead[1], integral_loose_ftemp_lead_err )
    integral_loose_ftemp_subl_val = subl_fake_template.IntegralAndError( loose_bins_subl[0], loose_bins_subl[1], integral_loose_ftemp_subl_err )

    n_loose_ftemp_lead  = ufloat( integral_loose_ftemp_lead_val/lead_fake_template.Integral(), integral_loose_ftemp_lead_err/lead_fake_template.Integral() )
    n_loose_ftemp_subl  = ufloat( integral_loose_ftemp_subl_val/subl_fake_template.Integral(), integral_loose_ftemp_subl_err/subl_fake_template.Integral() )

    # integral of the real template in the tight region
    integral_tight_rtemp_lead_err = ROOT.Double()
    integral_tight_rtemp_subl_err = ROOT.Double()
    integral_tight_rtemp_lead_val = lead_real_template.IntegralAndError( tight_bins_lead[0], tight_bins_lead[1], integral_tight_rtemp_lead_err ) 
    integral_tight_rtemp_subl_val = subl_real_template.IntegralAndError( tight_bins_subl[0], tight_bins_subl[1], integral_tight_rtemp_subl_err )

    n_tight_rtemp_lead = ufloat( integral_tight_rtemp_lead_val/lead_real_template.Integral(), integral_tight_rtemp_lead_err/lead_real_template.Integral() )
    n_tight_rtemp_subl = ufloat( integral_tight_rtemp_subl_val/subl_real_template.Integral(), integral_tight_rtemp_subl_err/subl_real_template.Integral() )

    # integral of the real template in the loose region
    integral_loose_rtemp_lead_err = ROOT.Double()
    integral_loose_rtemp_subl_err = ROOT.Double()
    integral_loose_rtemp_lead_val = lead_real_template.IntegralAndError( loose_bins_lead[0], loose_bins_lead[1], integral_loose_rtemp_lead_err ) 
    integral_loose_rtemp_subl_val = subl_real_template.IntegralAndError( loose_bins_subl[0], loose_bins_subl[1], integral_loose_rtemp_subl_err )

    n_loose_rtemp_lead = ufloat( integral_loose_rtemp_lead_val/lead_real_template.Integral(), integral_loose_rtemp_lead_err/lead_real_template.Integral() )
    n_loose_rtemp_subl = ufloat( integral_loose_rtemp_subl_val/subl_real_template.Integral(), integral_loose_rtemp_subl_err/subl_real_template.Integral() )

    text_results = {}
    text_results['lead'] = {}
    text_results['subl'] = {}

    text_results['lead']['eff_R_T'] = n_tight_rtemp_lead
    text_results['lead']['eff_R_L'] = n_loose_rtemp_lead
    text_results['lead']['eff_F_T'] = n_tight_ftemp_lead
    text_results['lead']['eff_F_L'] = n_loose_ftemp_lead

    text_results['subl']['eff_R_T'] = n_tight_rtemp_subl
    text_results['subl']['eff_R_L'] = n_loose_rtemp_subl
    text_results['subl']['eff_F_T'] = n_tight_ftemp_subl
    text_results['subl']['eff_F_L'] = n_loose_ftemp_subl

    DumpToPickle( text_results, outputDir, namePostfix )


def fit_diphoton( real_base, fake_base, target_base, xf_cr_base, fx_cr_base, ff_cr_base, rf_cr_base, fr_cr_base, signal_sample, bkg_sample, target_sample, binning, position,  tight_cut=None, loose_cut=None, sig_bins=None, bkg_bins=None, outputDir=None ) :

    global sampMan

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

        sig_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEB[0] ) '    %( real_base ) ) )
        sig_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) '    %( real_base ) ) )
        bkg_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEB[0] ) '    %( fake_base    ) ) )
        bkg_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) '    %( fake_base    ) ) )
        
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
        sig_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight *  ( %s && ph_IsEB[0] ) ' %( real_base ) ) )
        sig_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight *  ( %s && ph_IsEB[0] ) ' %( real_base ) ) )
        bkg_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight *  ( %s && ph_IsEB[0] ) ' %( fake_base    ) ) )
        bkg_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight *  ( %s && ph_IsEB[0] ) ' %( fake_base    ) ) )

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
        sig_selection.append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEE[0] ) ' %( real_base ) ) )
        sig_selection.append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) ' %( real_base ) ) )

        bkg_selection   .append( ( 'ph_sigmaIEIE[0]'   , ' PUWeight * ( %s && ph_IsEE[0] ) ' %( fake_base    ) ) )
        bkg_selection   .append( ( '-1*ph_sigmaIEIE[0]', ' PUWeight * ( %s && ph_IsEE[0] ) ' %( fake_base    ) ) )

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
    

    #generate histograms
    rr_template_hist = None
    rf_template_hist = None
    fr_template_hist = None
    ff_template_hist = None

    sig_template_hist = None
    sig_template_hist_neg = None

    bkg_template_hist = None
    bkg_template_hist_neg = None
    
    sig_template_samp = sampMan.get_samples(name=signal_sample )
    bkg_template_samp = sampMan.get_samples(name=bkg_sample)
    
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
    if tight_cut is not None :
        tight_eff_fake = bkg_hists[0].Integral( bkg_hists[0].FindBin(tight_cut[1][0]), bkg_hists[0].FindBin( tight_cut[1][1] ) ) / bkg_hists[0].Integral() 
        tight_eff_sig = sig_hists[0].Integral( sig_hists[0].FindBin(tight_cut[1][0]), sig_hists[0].FindBin( tight_cut[1][1] ) ) / sig_hists[0].Integral() 
    if sig_bins is not None :
        tight_eff_fake = bkg_hists[0].GetBinContent( sig_bins[1] ) / bkg_hists[0].Integral() 
        tight_eff_sig = sig_hists[0].GetBinContent( sig_bins[1] ) / sig_hists[0].Integral() 
    if loose_cut is not None :
        loose_eff_fake = bkg_hists[0].Integral( bkg_hists[0].FindBin(loose_cut[1][0]), bkg_hists[0].FindBin( loose_cut[1][1] ) ) / bkg_hists[0].Integral() 
        loose_eff_sig = sig_hists[0].Integral( sig_hists[0].FindBin(loose_cut[1][0]), sig_hists[0].FindBin( loose_cut[1][1] ) ) / sig_hists[0].Integral() 
    if bkg_bins is not None :
        loose_eff_fake = bkg_hists[0].GetBinContent( bkg_bins[1] ) / bkg_hists[0].Integral() 
        loose_eff_sig = sig_hists[0].GetBinContent( bkg_bins[1] ) / sig_hists[0].Integral() 

    print 'tight_eff_fake = ', tight_eff_fake
    print 'loose_eff_fake = ', loose_eff_fake
    print 'tight_eff_sig = ', tight_eff_sig
    print 'loose_eff_sig = ', loose_eff_sig


    ff_template_hist_xf = bkg_hists[0].Clone('ffhistxf')
    # normalize subl distribution to the lead distribution, but increase the sublead by 1/tight_eff_fake
    ff_template_hist_xf.Scale( tight_eff_fake*bkg_hists[1].Integral()/ff_template_hist_xf.Integral())
    ff_template_hist_xf.Add( bkg_hists[1] )

    ff_template_hist_fx = bkg_hists[0].Clone('ffhistfx')
    # normalize lead distribution to the sublead distribution, but increase the lead by 1/tight_eff_fake
    ff_template_hist_fx.Scale( bkg_hists[1].Integral()/( tight_eff_fake*ff_template_hist_fx.Integral()))
    ff_template_hist_fx.Add( bkg_hists[1] )

    rf_template_hist = sig_hists[0].Clone( 'rfhist' )
    # normalize subl distribution to the lead distribution, but increase the sublead by 1/tight_eff_fake
    rf_template_hist.Scale( tight_eff_fake*bkg_hists[1].Integral() / rf_template_hist.Integral() )
    rf_template_hist.Add( bkg_hists[1] )
    
    fr_template_hist = bkg_hists[0].Clone( 'frhist' )
    # normalize lead distribution to the sublead distribution, but increase the lead by 1/tight_eff_fake
    fr_template_hist.Scale( sig_hists[1].Integral() / ( tight_eff_fake*fr_template_hist.Integral() ) )
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
    #draw_template_with_axis(rrtemp, [rr_template_hist], normalize=1, outputName=rrtempName)
    rftemp = ROOT.TCanvas('rftemp', 'rftemp')
    draw_template_with_axis(rftemp, [fr_template_hist], normalize=1, outputName=rftempName)
    #frtemp = ROOT.TCanvas('frtemp', 'frtemp')
    #draw_template_with_axis(frtemp, [rf_template_hist], normalize=1, outputName=frtempName)
    #fftempfx = ROOT.TCanvas('fftempfx', 'fftempfx')
    #draw_template_with_axis(fftempfx, [ff_template_hist_fx], normalize=1, outputName=fftempNamefx)
    #fftempxf = ROOT.TCanvas('fftempxf', 'fftempxf')
    #draw_template_with_axis(fftempxf, [ff_template_hist_xf], normalize=1, outputName=fftempNamexf)


    target_hist = None
    xf_cr_hist = None
    fx_cr_hist = None
    ff_cr_hist = None
    rf_cr_hist = None
    fr_cr_hist = None
    target_samp = sampMan.get_samples(name=target_sample)
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

    if loose_cut is not None and tight_cut is not None  :

        tight_bins_lead = ( xf_cr_hist.FindBin( tight_cut[1][0] ) ,xf_cr_hist.FindBin( tight_cut[1][1] ) )
        tight_bins_subl = ( xf_cr_hist.FindBin( tight_cut[0][0] ) , xf_cr_hist.FindBin( tight_cut[0][1] ) )

        loose_bins_lead = ( xf_cr_hist.FindBin( loose_cut[1][0] ) , xf_cr_hist.FindBin( loose_cut[1][1] ) )
        loose_bins_subl = ( xf_cr_hist.FindBin( loose_cut[0][0] ) , xf_cr_hist.FindBin( loose_cut[0][1] ) )

        print 'Normalize in lead ff region betwen bins %d and %d ( %f and %f )' %(loose_bins_lead[0],loose_bins_lead[1], loose_cut[1][0], loose_cut[1][1])
        print 'Normalize in subl ff region betwen bins %d and %d ( %f and %f )' %(loose_bins_subl[0],loose_bins_subl[1], loose_cut[0][0], loose_cut[0][1])
        print 'Normalize in xf region betwen bins %d and %d ( %f and %f )' %(tight_bins_lead[0], tight_bins_lead[1], tight_cut[1][0], tight_cut[1][1] )
        print 'Normalize in fx region betwen bins %d and %d ( %f and %f )' %(tight_bins_subl[0], tight_bins_subl[1], tight_cut[0][0], tight_cut[0][1] )
        print 'Bin %d min=%f, center=%f, max=%f '%( loose_bins_lead[0], xf_cr_hist.GetXaxis().GetBinLowEdge( loose_bins_lead[0] ), xf_cr_hist.GetXaxis().GetBinCenter( loose_bins_lead[0] ), xf_cr_hist.GetXaxis().GetBinUpEdge( loose_bins_lead[0] ) )
        print 'Bin %d min=%f, center=%f, max=%f '%( loose_bins_subl[1], xf_cr_hist.GetXaxis().GetBinLowEdge( loose_bins_subl[1] ), xf_cr_hist.GetXaxis().GetBinCenter( loose_bins_subl[1] ), xf_cr_hist.GetXaxis().GetBinUpEdge( loose_bins_subl[1] ) )
        print 'ff_cr_hist.Integral( loose_bins_subl[0], loose_bins_subl[1] ) ', ff_cr_hist.Integral( loose_bins_subl[0], loose_bins_subl[1] ) 
        print 'ff_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] ) ', ff_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] )
        print 'xf_cr_hist.Integral( tight_bins_lead[0], tight_bins_lead[1])', xf_cr_hist.Integral( tight_bins_lead[0], tight_bins_lead[1])
        print 'fx_cr_hist.Integral( tight_bins_subl[0], tight_bins_subl[1])', fx_cr_hist.Integral( tight_bins_subl[0], tight_bins_subl[1])

        n_ll_target_lead = xf_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] )
        n_ll_target_subl = fx_cr_hist.Integral( loose_bins_subl[0], loose_bins_subl[1] )
        n_ll_ff_template_lead = bkg_hists[0].Integral(loose_bins_lead[0], loose_bins_lead[1] )
        n_ll_ff_template_subl = bkg_hists[1].Integral(loose_bins_subl[0], loose_bins_subl[1] )
        lead_norm = n_ll_target_lead / n_ll_ff_template_lead
        subl_norm = n_ll_target_subl / n_ll_ff_template_subl
        n_xf_target = xf_cr_hist.Integral( tight_bins_lead[0], tight_bins_lead[1]) - lead_norm*bkg_hists[0].Integral( tight_bins_lead[0], tight_bins_lead[1] ) 
        n_fx_target = fx_cr_hist.Integral( tight_bins_subl[0], tight_bins_subl[1]) - subl_norm*bkg_hists[1].Integral( tight_bins_subl[0], tight_bins_subl[1] )
        xf_lead_norm = n_xf_target / sig_hists[0].Integral( tight_bins_lead[0], tight_bins_lead[1] ) 
        fx_subl_norm = n_fx_target / sig_hists[1].Integral( tight_bins_subl[0], tight_bins_subl[1] )
        xf_subl_norm = xf_lead_norm * ( sig_hists[0].Integral() /( bkg_hists[1].Integral( ) - bkg_hists[1].Integral( tight_bins_subl[0], tight_bins_subl[1] ) ) )
        fx_lead_norm = fx_subl_norm * ( sig_hists[1].Integral() /( bkg_hists[0].Integral( ) - bkg_hists[0].Integral( tight_bins_lead[0], tight_bins_lead[1] ) ) )

        print 'N ff events in rf normalization region = ', lead_norm*bkg_hists[0].Integral( tight_bins_lead[0], tight_bins_lead[1] )
        print 'N ff events in fr normalization region = ', subl_norm*bkg_hists[1].Integral( tight_bins_subl[0], tight_bins_subl[1] )
        print 'N xf target = ', n_xf_target
        print 'N fx target = ', n_fx_target
        print 'rf norm = ', xf_lead_norm
        print 'fr norm = ', fx_lead_norm
        print 'N lead rf after norm = ',xf_lead_norm * ( sig_hists[0].Integral() ) 
        print 'N subl fr after norm = ',fx_subl_norm * ( sig_hists[1].Integral() ) 
        print 'N loose subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) - bkg_hists[1].Integral( tight_bins_subl[0], tight_bins_subl[1] ) )
        print 'N loose lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) - bkg_hists[0].Integral( tight_bins_lead[0], tight_bins_lead[1] ) )
        print 'N total subl rf after norm = ', xf_subl_norm * ( bkg_hists[1].Integral( ) )
        print 'N total lead fr after norm = ', fx_lead_norm * ( bkg_hists[0].Integral( ) )

        print 'Predict %f rf events in TT region' %( xf_subl_norm * bkg_hists[1].Integral( tight_bins_subl[0], tight_bins_subl[1] ) )
        print 'Predict %f fr events in TT region' %( fx_lead_norm * bkg_hists[0].Integral( tight_bins_lead[0], tight_bins_lead[1] ) )
        print '%d data events in LL region ' %ff_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] )
        print 'Probability for f to be T = %f' %(tight_eff_fake)
        print 'Probability for f to be L = %f' %(loose_eff_fake)
        print 'Probability for r to be T = %f' %(tight_eff_fake)
        print 'Probability for r to be L = %f' %(loose_eff_fake)
        print 'Predict %f ff events in TT region' %( ff_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] ) * ( tight_eff_fake*tight_eff_fake) / (loose_eff_fake*loose_eff_fake) )

        #n_ll_target_lead = ff_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] )
        #n_ll_target_subl = ff_cr_hist.Integral( loose_bins_subl[0], loose_bins_subl[1] )
        #n_ll_ff_template_lead = ff_template_hist_xf.Integral(loose_bins_lead[0], loose_bins_lead[1] )
        #n_ll_ff_template_subl = ff_template_hist_fx.Integral(loose_bins_subl[0], loose_bins_subl[1] )
        #lead_norm = n_ll_target_lead / n_ll_ff_template_lead
        #subl_norm = n_ll_target_subl / n_ll_ff_template_subl
        #n_xf_target = xf_cr_hist.Integral( tight_bins_lead[0], tight_bins_lead[1]) - lead_norm*ff_template_hist_xf.Integral( tight_bins_lead[0], tight_bins_lead[1] ) 
        #n_fx_target = fx_cr_hist.Integral( tight_bins_subl[0], tight_bins_subl[1]) - subl_norm*ff_template_hist_fx.Integral( tight_bins_subl[0], tight_bins_subl[1] )

        #print 'ff subl_norm = %f' %subl_norm
        #print 'ff lead_norm = %f' %lead_norm

        #print 'Normalize lead distribution to %f in xf region' %n_xf_target
        #print 'Normalize subl distribution to %f in fx region' %n_fx_target

        #xf_norm = n_xf_target / rf_template_hist.Integral( tight_bins_lead[0], tight_bins_lead[1] ) 
        #fx_norm = n_fx_target / fr_template_hist.Integral( tight_bins_subl[0], tight_bins_subl[1] )

        #print 'Predict %f rf events in TT region' %( xf_norm * rf_template_hist.Integral( tight_bins_subl[0], tight_bins_subl[1] ) )
        #print 'Predict %f fr events in TT region' %( fx_norm * fr_template_hist.Integral( tight_bins_lead[0], tight_bins_lead[1] ) )

        #print '%d data events in LL region ' %ff_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] )
        #print 'Probability for f to be T = %f' %(tight_eff_fake)
        #print 'Probability for f to be L = %f' %(loose_eff_fake)
        #print 'Predict %f ff events in TT region' %( ff_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] ) * ( tight_eff_fake*tight_eff_fake) / (loose_eff_fake*loose_eff_fake) )
        
        

        ##print 'Fraction of fr events where lead passes Tight = %f' %fx_leadpassT_frac
        ##print 'Fraction of rf events where subl passes Tight = %f' %xf_sublpassT_frac

        ###Ntot * (1-frac) = NBkg
        ###Ntot * frac = NSig
        ###NSig = NBkg * frac/(1-frac)
        ###NBkg = norm*Integral( Lregion )
        ###NSig = norm*Integral( Lregion ) * frac/(1-frac)

        ##nbkg_rf = xf_norm*( (rf_template_hist.Integral()/2.) - rf_template_hist.Integral( tight_bins_subl[0], tight_bins_subl[1] ) )
        ##nbkg_fr = fx_norm*( (fr_template_hist.Integral()/2.) - fr_template_hist.Integral( tight_bins_lead[0], tight_bins_lead[1] ) )

        ##print 'N Bkg rf = %f' %nbkg_rf
        ##print 'N Bkg fr = %f' %nbkg_fr

        ##print 'Total N rf = %f' %( nbkg_rf/( 1-xf_sublpassT_frac) )
        ##print 'Total N fr = %f' %( nbkg_fr/( 1-fx_leadpassT_frac) )

        ##print 'RF factor = %f, FR factor = %f' %( xf_norm, fx_norm )
        ###print 'Predict %f rf events in TT region' %(xf_norm*rf_template_hist.Integral( tight_bins_subl[0], tight_bins_subl[1] ))
        ###print 'Predict %f fr events in TT region' %(fx_norm*fr_template_hist.Integral( tight_bins_lead[0], tight_bins_lead[1] ))

        ##print 'Predict %f rf events in TT region' %(nbkg_rf * xf_sublpassT_frac / ( 1-xf_sublpassT_frac ) )
        ##print 'Predict %f fr events in TT region' %(nbkg_fr * fx_leadpassT_frac / ( 1-fx_leadpassT_frac ) )

        ##nff_tot_lead = avg_norm*ff_template_hist.Integral()/2.
        ##nff_pass_tight = avg_norm*ff_template_hist.Integral( tight_bins_lead[0], tight_bins_lead[1] )
        ##prob_pass = nff_pass_tight/nff_tot_lead
        ##prob_fail = 1-prob_pass

        ##print '%d data events in LL region ' %ff_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] )
        ##print 'Probability for f to be T = %f' %(prob_pass)
        ##print 'Predict %f ff events in TT region' %( ff_cr_hist.Integral( loose_bins_lead[0], loose_bins_lead[1] ) * ( prob_pass*prob_pass) / (prob_fail*prob_fail) )
        

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
        print 'Probability for f to be T = %f' %(tight_eff_fake)
        print 'Probability for f to be L = %f' %(loose_eff_fake)
        print 'Predict %f ff events in TT region' %( ff_cr_hist.GetBinContent( bkg_bins[1] ) * ( tight_eff_fake*tight_eff_fake) / (loose_eff_fake*loose_eff_fake) )


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
        #print 'Probability for f to be T = %f' %(tight_eff_fake)
        #print 'Probability for f to be L = %f' %(loose_eff_fake)
        #print 'Predict %f ff events in TT region' %( ff_cr_hist.GetBinContent( bkg_bins[1] ) * ( tight_eff_fake*tight_eff_fake) / (loose_eff_fake*loose_eff_fake ) )
        
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
        ##print 'Predict %f rf events in TT region' %(xf_norm*rf_template_hist.Integral( tight_bins_subl[0], tight_bins_subl[1] ))
        ##print 'Predict %f fr events in TT region' %(fx_norm*fr_template_hist.Integral( tight_bins_lead[0], tight_bins_lead[1] ))

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
    #draw_template_with_axis(ffcanxf, [ff_cr_hist, ff_template_hist_xf], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FF template'], outputName=fftempNorm_llName)
    #ffcanfx = ROOT.TCanvas('ffcanfx', 'ffcanfx')
    #draw_template_with_axis(ffcanfx, [ff_cr_hist, ff_template_hist_fx], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FF template'], outputName=fftempNorm_llName)
    #xfcan = ROOT.TCanvas('xfcan', 'xfcan')
    #draw_template_with_axis(xfcan, [xf_cr_hist, rf_template_hist, ff_template_hist_xf], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=rftempNorm_xlName)
    #fxcan = ROOT.TCanvas('fxcan', 'fxcan')
    #draw_template_with_axis(fxcan, [fx_cr_hist, fr_template_hist, ff_template_hist_fx], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FR template', 'FF template'], outputName=frtempNorm_lxName)

    xfcan = ROOT.TCanvas('xfcan', 'xfcan')
    draw_template_with_axis(xfcan, [xf_cr_hist, rf_template_histNew, ff_template_hist_xfNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=rftempNorm_xlName)
    fxcan = ROOT.TCanvas('fxcan', 'fxcan')
    draw_template_with_axis(fxcan, [fx_cr_hist, fr_template_histNew, ff_template_hist_fxNew], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'FR template', 'FF template'], outputName=frtempNorm_lxName)


    if loose_cut is not None and tight_cut is not None  :
        rf_fit_bins = ( rf_cr_hist.FindBin( loose_cut[0][0] ), rf_cr_hist.FindBin( loose_cut[0][1] ) )
        fr_fit_bins = ( rf_cr_hist.FindBin( loose_cut[1][0] ), rf_cr_hist.FindBin( loose_cut[1][1] ) )

        subl_sig_bins = ( rf_cr_hist.FindBin( tight_cut[0][0] ), rf_cr_hist.FindBin( tight_cut[0][1] ) )
        lead_sig_bins = ( rf_cr_hist.FindBin( tight_cut[1][0] ), rf_cr_hist.FindBin( tight_cut[1][1] ) )

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
    draw_template_with_axis(rfcan, [rf_cr_hist, rf_template_hist, ff_template_hist_xf], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=fftempNorm_rfName)
    frcan = ROOT.TCanvas('frcan', 'frcan')
    draw_template_with_axis(frcan, [fr_cr_hist, fr_template_hist, ff_template_hist_fx], normalize=False, first_hist_is_data=True, legend_entries=['Data', 'RF template', 'FF template'], outputName=fftempNorm_frName)

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
        global sampMan
        newSamp = sampMan.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
        sampMan.create_hist( newSamp, var, sel, binning )
        return newSamp.hist
                                       
def get_hists_and_fit( var, signal_selection, bkg_selection, target_selection, signal_sample, bkg_sample, target_sample, binning, fit_range, manual_tight_cut, manual_loose_cut ) :
    
    global sampMan

    print signal_selection
    print bkg_selection
    print target_selection

    #generate histograms
    sig_template_hist = None
    bkg_template_hist = None

    sig_template_samp = sampMan.get_samples(name=signal_sample )
    if sig_template_samp :
        newEBSigsamp = sampMan.clone_sample( oldname=sig_template_samp[0].name, newname='DataSigTemplateEB', temporary=True )
        sampMan.create_hist( newEBSigsamp, var, signal_selection, binning )
        sig_template_hist = newEBSigsamp.hist

    #background template
    bkg_template_samp = sampMan.get_samples(name=bkg_sample)
    if bkg_template_samp :
        newEBBkgsamp = sampMan.clone_sample( oldname=bkg_template_samp[0].name, newname='DataMCSubBkgTemplateEB', temporary=True )
        sampMan.create_hist( newEBBkgsamp, var, bkg_selection , binning )
        bkg_template_hist = newEBBkgsamp.hist

    target_hist = None
    target_samp = sampMan.get_samples(name=target_sample)
    if target_samp :
        newEBTargetSamp = sampMan.clone_sample( oldname=target_samp[0].name, newname='DataTargetEB', temporary=True)
        sampMan.create_hist(newEBTargetSamp , var,target_selection , binning  )
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
    bkg_bin_min = target_hist.FindBin( manual_loose_cut[0] )
    bkg_bin_max = target_hist.FindBin( manual_loose_cut[1] )
    sig_bin_min = target_hist.FindBin( manual_tight_cut[0] )
    sig_bin_max = target_hist.FindBin( manual_tight_cut[1] )

    n_target_bkg_pure = target_hist.Integral( bkg_bin_min, bkg_bin_max )
    n_bkg_bkg_pure = bkg_template_hist.Integral( bkg_bin_min, bkg_bin_max )

    bkg_norm = n_target_bkg_pure/n_bkg_bkg_pure
    print 'In bkg region between %f and %f ( %d and %d ), Ndata = %d, Nbkg = %f, norm= %f' %( manual_loose_cut[0], manual_loose_cut[1], bkg_bin_min, bkg_bin_max, n_target_bkg_pure, n_bkg_bkg_pure, bkg_norm )
    
    n_target_sig_pure = target_hist.Integral( sig_bin_min, sig_bin_max )
    n_bkg_sig_pure = bkg_template_hist.Integral( sig_bin_min, sig_bin_max )
    n_sig_sig_pure = sig_template_hist.Integral( sig_bin_min, sig_bin_max )

    sig_norm = ( n_target_sig_pure - n_bkg_sig_pure*bkg_norm ) / n_sig_sig_pure

    print 'In sig region between %f and %f ( %d and %d ), Ndata = %d, Nsig=%f, Nbkg = %f, norm= %f' %( manual_tight_cut[0], manual_tight_cut[1], sig_bin_min, sig_bin_max, n_target_sig_pure, n_sig_sig_pure, bkg_norm*n_bkg_bkg_pure, sig_norm )

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

    
    sampMan.create_top_canvas_for_ratio('can')
    sampMan.curr_canvases['can'].cd()
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

    sampMan.create_standard_ratio_canvas()
    sampMan.set_canvas_default_formatting( sampMan.curr_canvases['can'], doratio=True, logy=False )

    sampMan.curr_canvases['top'].cd()
    sampMan.curr_canvases['can'].DrawClonePad()
    sampMan.curr_canvases['can'].SetLogy(1)
    leg = sampMan.create_standard_legend( 3, doratio=True )
    leg.AddEntry( target_hist, 'Data' )
    leg.AddEntry( bkg_template_hist, 'Fake template' )
    leg.AddEntry( sig_template_hist, 'Real template' )
    leg.AddEntry( sumhist, 'Template sum' )
    leg.Draw()

    sampMan.curr_canvases['bottom'].cd()
    ratiohist = target_hist.Clone('ratio')
    ratiohist.Divide( sumhist )

    tmpSamp = Sample('tmpSAmp')
    tmpSamp.hist = ratiohist
    sampMan.set_ratio_default_formatting( sampMan.curr_canvases['bottom'], [tmpSamp], doratio=True, rlabel='Data/Template' )

    ratiohist.GetXaxis().SetTitle( '#sigma i#eta i#eta' )
    ratiohist.Draw()

    
    print ' Chi square = ', sumhist.Chi2Test( target_hist, 'WWCHI2' )
    print ' Chi square/NDF = ', sumhist.Chi2Test( target_hist, 'WWCHI2/NDF' )

    sampMan.curr_canvases['top'].cd()

    chi2 = ROOT.TLatex( 0.8, 0.6, '#chi^{2}/NDF = %.2f' % sumhist.Chi2Test( target_hist, 'WWCHI2/NDF' ) )
    chi2.SetNDC()
    chi2.SetX(0.7)
    chi2.SetY(0.6)
    chi2.Draw()


    raw_input('continue')
    

def print_template_efficiencies( templates, tight_cuts_eb, loose_cuts_eb, tight_cuts_ee, loose_cuts_ee ) :

    tight_eff_fake_eb = templates['fake']['EB'].Integral( templates['fake']['EB'].FindBin( tight_cuts_eb[0][0] ),templates['fake']['EB'].FindBin( tight_cuts_eb[0][1] )) / templates['fake']['EB'].Integral() 
    tight_eff_fake_ee = templates['fake']['EE'].Integral( templates['fake']['EE'].FindBin( tight_cuts_ee[0][0] ),templates['fake']['EE'].FindBin( tight_cuts_ee[0][1] )) / templates['fake']['EE'].Integral() 
    loose_eff_fake_eb = templates['fake']['EB'].Integral( templates['fake']['EB'].FindBin( loose_cuts_eb[0][0] ),templates['fake']['EB'].FindBin( loose_cuts_eb[0][1] )) / templates['fake']['EB'].Integral() 
    loose_eff_fake_ee = templates['fake']['EE'].Integral( templates['fake']['EE'].FindBin( loose_cuts_ee[0][0] ),templates['fake']['EE'].FindBin( loose_cuts_ee[0][1] )) / templates['fake']['EE'].Integral() 

    tight_eff_real_eb = templates['real']['EB'].Integral( templates['real']['EB'].FindBin( tight_cuts_eb[0][0] ),templates['real']['EB'].FindBin( tight_cuts_eb[0][1] )) / templates['real']['EB'].Integral() 
    tight_eff_real_ee = templates['real']['EE'].Integral( templates['real']['EE'].FindBin( tight_cuts_ee[0][0] ),templates['real']['EE'].FindBin( tight_cuts_ee[0][1] )) / templates['real']['EE'].Integral() 
    loose_eff_real_eb = templates['real']['EB'].Integral( templates['real']['EB'].FindBin( loose_cuts_eb[0][0] ),templates['real']['EB'].FindBin( loose_cuts_eb[0][1] )) / templates['real']['EB'].Integral() 
    loose_eff_real_ee = templates['real']['EE'].Integral( templates['real']['EE'].FindBin( loose_cuts_ee[0][0] ),templates['real']['EE'].FindBin( loose_cuts_ee[0][1] )) / templates['real']['EE'].Integral() 

    print 'tight_eff_fake_eb = ', tight_eff_fake_eb 
    print 'tight_eff_fake_ee = ', tight_eff_fake_ee 
    print 'loose_eff_fake_eb = ', loose_eff_fake_eb 
    print 'loose_eff_fake_ee = ', loose_eff_fake_ee 
    print 'tight_eff_real_eb = ', tight_eff_real_eb 
    print 'tight_eff_real_ee = ', tight_eff_real_ee 
    print 'loose_eff_real_eb = ', loose_eff_real_eb 
    print 'loose_eff_real_ee = ', loose_eff_real_ee 

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
            txtval.append( '%s' %v)

        print txtval


        latex_text += key + ' & ' + ' & '.join( txtval ) + r' \\ '
        if first :
            latex_text += r' \hline  '
            first = False

        latex_text += '\n'

    latex_text += r'\end{tabular}' + ' \n'


    return latex_text

def do_2bin_fit( nTight, nLoose, eff) :

    if eff['LeffF'] == 0 or eff['TeffR'] == 0 :
        print 'Denominator is zero!'
        return (None, None,None, None)

    alpha_R = ( nTight - ( eff['TeffF'] / eff['LeffF'] ) * nLoose ) / ( eff['TeffR'] - ( ( eff['LeffR']*eff['TeffF'] )/eff['LeffF'] ) ) 

    alpha_F = ( nLoose - ( eff['LeffR'] / eff['TeffR'] ) * nTight ) / ( eff['LeffF'] - ( ( eff['LeffR']*eff['TeffF'] )/eff['TeffR'] ) ) 


    n_real_tight = alpha_R*eff['TeffR']
    n_fake_tight = alpha_F*eff['TeffF']
    n_real_loose = alpha_R*eff['LeffR']
    n_fake_loose = alpha_F*eff['LeffF']

    return n_real_tight, n_real_loose, n_fake_tight, n_fake_loose





main() 
