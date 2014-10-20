"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

                                                                                       
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',  required=False,       help='Input directory base')
p.add_argument('--baseDirSingle',     default=None,  type=str ,        dest='baseDirSingle',  required=False,       help='Input directory base for single photon results')
p.add_argument('--ptbins',     default='15,25,40,80,1000000',  type=str ,        dest='ptbins',  required=False,       help='PT bins to use')

options = p.parse_args()

import sys
import os
import re
import math
import uuid
import copy
import pickle
import imp
import ROOT
from array import array
from uncertainties import ufloat

from SampleManager import SampleManager

ROOT.gROOT.SetBatch(True)

samplesWgg = None

ph_cuts = ''
lead_dr_cut = 0.4
subl_dr_cut = 0.4
phot_dr_cut = 0.3

el_cuts = {'elfull' : 
           {'invlead' : 'el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
            'invsubl' : 'el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           },
           'elzcr' :
           {'invlead' : 'el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0  && ( (fabs(m_lepphph-91.2) < 5) || (fabs(m_lepph1-91.2) < 5) || (fabs(m_lepph2-91.2) < 5) ) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
            'invsubl' : ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1  && ( (fabs(m_lepphph-91.2) < 5) || (fabs(m_lepph1-91.2) < 5)  || (fabs(m_lepph2-91.2) < 5) ) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           },
           'elbase' : 
           {'invlead' : 'el_passtrig_n>0 && el_n==1 && ph_n==2  && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && ph_phDR>0.3 && leadPhot_leadLepDR>%.1f && sublPhot_leadLepDR>%.1f && mu_n==0 && m_phph>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts),
            'invsubl' : 'el_passtrig_n>0 && el_n==1 && ph_n==2  && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && ph_phDR>0.3 && leadPhot_leadLepDR>%.1f && sublPhot_leadLepDR>%.1f && mu_n==0 && m_phph>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts) 
          },
           'singleelzcr' : 'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_hasPixSeed[0]==1 && leadPhot_leadLepDR > %.1f && mu_n==0 && m_lepph1 > 76 && m_lepph1 < 106 ' %( lead_dr_cut ),
           'singleel' : 'el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_hasPixSeed[0]==1 && leadPhot_leadLepDR > %.1f && mu_n==0 ' %( lead_dr_cut ),
}


def main() :

    global samplesWgg
    global samplesWg

    baseDirWgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGamma_2014_10_12/'
    baseDirWg  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfWgg = 'Modules/Wgamgam.py'

    samplesWgg = SampleManager(baseDirWgg, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWg  = SampleManager(baseDirWg,  treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesWgg.ReadSamples( sampleConfWgg )
    samplesWg .ReadSamples( sampleConfWgg )

    bins = options.ptbins.split(',')

    file_bin_map = {'ElectronFakeFitsRatioMCTemplateNDKeys' : [(bins[0], bins[1]), (bins[1], bins[2]), (bins[2], bins[3]) ], 'ElectronFakeFitsRatio' : [(bins[3], 'max')] }
    file_bin_map_syst = {'ElectronFakeFitsRatioExpBkg' : [(bins[0], bins[1]), (bins[1], bins[2]), (bins[2], bins[3]),(bins[3], 'max') ] }

    if options.baseDir is not None :
        base_dir_ele = options.baseDir
        base_dir_jet = '%s/JetFakeResultsSyst'%options.baseDir
        outputDir='%s/BackgroundEstimates'%options.baseDir
        #MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, el_selection='elfull', outputDir=outputDir )
        #MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, el_selection='elzcr', outputDir=outputDir, namePostfix='__zcr' )

        #MakeJetBkgEstimate( base_dir_jet, outputDir )

        MakeBkgEstimatePlots( outputDir )

    if options.baseDirSingle is not None :

        base_dir_ele_single = options.baseDirSingle
        base_dir_jet_single = '%s/SinglePhotonResults' %options.baseDirSingle
        outputDirSingle='%s/SinglePhotonBackgroundEstimates' %options.baseDirSingle

        #MakeSingleEleBkgEstimate( base_dir_ele_single, base_dir_jet_single, file_bin_map, file_bin_map_syst, outputDir=outputDirSingle )
        #MakeSingleEleBkgEstimate( base_dir_ele_single, base_dir_jet_single, file_bin_map, file_bin_map_syst, el_selection='elzcr', outputDir=outputDirSingle, namePostfix='__zcr' )
        MakeSingleJetBkgEstimate( base_dir_jet_single, outputDirSingle )

def MakeJetBkgEstimate( base_dir_jet, outputDir=None ) :

    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB'), ('EE', 'EE')]
    pt_bins = [int(x) for x in options.ptbins.split(',')]

    file_key_mu = 'results__mu__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elfull = 'results__elfull__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elzcr  = 'results__elzcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'

    # jet fake results with systematic
    # uncertainties propagated
    file_key_mu_syst     = 'results__syst__mu__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elfull_syst = 'results__syst__elfull__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_el_syst     = 'results__syst__elzcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'

    jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )


    jet_files_mu     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu     )
    jet_files_elfull = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull )
    jet_files_elzcr  = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elzcr  )

    jet_files_mu_syst     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu_syst     )
    jet_files_elfull_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull_syst )
    jet_files_el_syst     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_el_syst     )

    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')

    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

    if jet_files_mu.values()[0] :
        subl_ptbins = [ ( '70', 'max', '15', '40' ), ( '70', 'max', '40', 'max' ) ]
        subl_ptbins = [ ]
        pred_mu     = get_jet_fake_results( jet_files_mu    , jet_files_mu_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet, pt_bins_subl=subl_ptbins ) 
        print 'muons'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['stat']['rf'][bin], pred_mu['stat']['fr'][bin], pred_mu['stat']['ff'][bin], (  pred_mu['stat']['rf'][bin]+ pred_mu['stat']['fr'][bin]+ pred_mu['stat']['ff'][bin] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['syst']['rf'][bin], pred_mu['syst']['fr'][bin], pred_mu['syst']['ff'][bin], (  pred_mu['syst']['rf'][bin]+ pred_mu['syst']['fr'][bin]+ pred_mu['syst']['ff'][bin] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['stat+syst']['rf'][bin], pred_mu['stat+syst']['fr'][bin], pred_mu['stat+syst']['ff'][bin], (  pred_mu['stat+syst']['rf'][bin]+ pred_mu['stat+syst']['fr'][bin]+ pred_mu['stat+syst']['ff'][bin] ) )

        file_muon = open( outputDir + '/jet_fake_results__mgg.pickle', 'w' )
        pickle.dump( pred_mu, file_muon )
        file_muon.close()

    if jet_files_elfull.values()[0] :
        pred_elfull = get_jet_fake_results( jet_files_elfull, jet_files_elfull_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print 'Electrons'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['stat']['rf'][bin], pred_elfull['stat']['fr'][bin], pred_elfull['stat']['ff'][bin], (  pred_elfull['stat']['rf'][bin]+ pred_elfull['stat']['fr'][bin]+ pred_elfull['stat']['ff'][bin] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['syst']['rf'][bin], pred_elfull['syst']['fr'][bin], pred_elfull['syst']['ff'][bin], (  pred_elfull['syst']['rf'][bin]+ pred_elfull['syst']['fr'][bin]+ pred_elfull['syst']['ff'][bin] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['stat+syst']['rf'][bin], pred_elfull['stat+syst']['fr'][bin], pred_elfull['stat+syst']['ff'][bin], (  pred_elfull['stat+syst']['rf'][bin]+ pred_elfull['stat+syst']['fr'][bin]+ pred_elfull['stat+syst']['ff'][bin] ) )

        file_elfull = open( outputDir + '/jet_fake_results__egg_allZRejCuts.pickle', 'w' )
        pickle.dump( pred_elfull, file_elfull )
        file_elfull.close()

    if jet_files_elzcr.values()[0] :
        pred_elzcr  = get_jet_fake_results( jet_files_elzcr , jet_files_el_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print 'Electrons Z CR'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)

                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['stat']['rf'][bin], pred_elzcr['stat']['fr'][bin], pred_elzcr['stat']['ff'][bin], (  pred_elzcr['stat']['rf'][bin]+ pred_elzcr['stat']['fr'][bin]+ pred_elzcr['stat']['ff'][bin] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['syst']['rf'][bin], pred_elzcr['syst']['fr'][bin], pred_elzcr['syst']['ff'][bin], (  pred_elzcr['syst']['rf'][bin]+ pred_elzcr['syst']['fr'][bin]+ pred_elzcr['syst']['ff'][bin] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['stat+syst']['rf'][bin], pred_elzcr['stat+syst']['fr'][bin], pred_elzcr['stat+syst']['ff'][bin], (  pred_elzcr['stat+syst']['rf'][bin]+ pred_elzcr['stat+syst']['fr'][bin]+ pred_elzcr['stat+syst']['ff'][bin] ) )


        file_elzcr = open( outputDir + '/jet_fake_results__egg_ZCR.pickle', 'w' )
        pickle.dump( pred_elzcr, file_elzcr)
        file_elzcr.close()

def MakeSingleJetBkgEstimate( base_dir_jet, outputDir=None ) :

    regions = ['EB', 'EE']
    pt_bins = [int(x) for x in options.ptbins.split(',')]

    file_key_mu = 'results__mu__(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_elfull = 'results__el__(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_elzcr  = 'results__elzcr__(EB|EE)__pt_(\d+)-(\d+|max).pickle'

    # jet fake results with systematic
    # uncertainties propagated
    file_key_mu_syst     = 'results__syst__mu__(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_elfull_syst = 'results__syst__el__(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_el_syst     = 'results__syst__elzcr__(EB|EE)__pt_(\d+)-(\d+|max).pickle'

    jet_dirs_key = 'JetSinglePhotonFakeNomIso'
    #jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    print jet_dir_key_map

    jet_files_mu     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu     )
    jet_files_elfull = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull )
    jet_files_elzcr  = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elzcr  )

    jet_files_mu_syst     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu_syst     )
    jet_files_elfull_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull_syst )
    jet_files_el_syst     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_el_syst     )

    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')


    pred_mu     = get_jet_single_fake_results( jet_files_mu    , jet_files_mu_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 
    pred_elfull = get_jet_single_fake_results( jet_files_elfull, jet_files_elfull_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 
    #pred_elzcr  = get_jet_single_fake_results( jet_files_elzcr , jet_files_el_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

    print 'muons'
    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
            ptmax = pt_bins_jetfile[idx+1]

            bin = (r1,ptmin,ptmax)

            print 'Region %s, pt %s-%s' %( r1,ptmin,ptmax)
            print 'Predicted Stat r = %s, predicted f = %s' %( pred_mu['stat']['r'][bin], pred_mu['stat']['f'][bin] ) 
            print 'Predicted Syst r = %s, predicted f = %s' %( pred_mu['syst']['r'][bin], pred_mu['syst']['f'][bin] )
            print 'Predicted Stat+Syst r = %s, predicted f = %s' %( pred_mu['stat+syst']['r'][bin], pred_mu['stat+syst']['f'][bin] )

    #print 'Electrons Z CR'
    #for r1 in regions :

    #    for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
    #        ptmax = pt_bins_jetfile[idx+1]

    #        bin = (r1,ptmin,ptmax)

    #        print 'Region %s, pt %s-%s' %( r1,ptmin,ptmax)

    #        print 'Predicted Stat r = %s, predicted f = %s' %( pred_elzcr['stat']['r'][bin], pred_elzcr['stat']['f'][bin] )
    #        print 'Predicted Syst r = %s, predicted f = %s' %( pred_elzcr['syst']['r'][bin], pred_elzcr['syst']['f'][bin] )
    #        print 'Predicted Stat+Syst r = %s, predicted f = %s' %( pred_elzcr['stat+syst']['r'][bin], pred_elzcr['stat+syst']['f'][bin])

    print 'Electrons'
    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
            ptmax = pt_bins_jetfile[idx+1]

            bin = (r1,ptmin,ptmax)

            print 'Region %s, pt %s-%s' %( r1,ptmin,ptmax)
            print 'Predicted Stat r = %s, predicted f = %s' %( pred_elfull['stat']['r'][bin], pred_elfull['stat']['f'][bin] )
            print 'Predicted Syst r = %s, predicted f = %s' %( pred_elfull['syst']['r'][bin], pred_elfull['syst']['f'][bin] )
            print 'Predicted Stat+Syst r = %s, predicted f = %s' %( pred_elfull['stat+syst']['r'][bin], pred_elfull['stat+syst']['f'][bin] )


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

    file_muon = open( outputDir + '/jet_fake_results__mg.pickle', 'w' )
    pickle.dump( pred_mu, file_muon )
    file_muon.close()

    file_elfull = open( outputDir + '/jet_fake_results__eg.pickle', 'w' )
    pickle.dump( pred_elfull, file_elfull )
    file_elfull.close()

    #file_elzcr = open( outputDir + '/jet_fake_results__eg_ZCR.pickle', 'w' )
    #pickle.dump( pred_elzcr, file_elzcr)
    #file_elzcr.close()

def MakeBkgEstimatePlots( baseDir ) :

    # first make the nominal estimates

    regions = [('EB', 'EB'), ('EB' ,'EE'), ('EE', 'EB')]

    for reg in regions :
    
        samplesWgg.activate_sample('AllBkg')
        samplesWgg.Draw( 'pt_leadph12', 'PUWeight * (mu_passtrig_n==1 && mu_n==1 && ph_medium_n>1 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.3 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && ph_Is%s[0] && ph_Is%s[1] ) ' %(reg[0],reg[1]), [0,5,10,15,25,40,70,200] )

        hist_data_mgg = samplesWgg.get_samples(name='Data')[0].hist.Clone('pt_leadph12_mgg_%s-%s'%(reg[0],reg[1]))
        save_hist( '%s/Plots/Data/hist.root' %baseDir, hist_data_mgg )

        hist_sig_mgg  = samplesWgg.get_samples(name='Wgg')[0].hist.Clone('pt_leadph12_mgg_%s-%s'%(reg[0],reg[1]))
        save_hist( '%s/Plots/Wgg/hist.root' %baseDir, hist_sig_mgg )

        hist_bkg_mgg  = samplesWgg.get_samples(name='AllBkg')[0].hist.Clone('pt_leadph12_mgg_%s-%s'%(reg[0],reg[1]))
        save_hist( '%s/Plots/MCBkg/hist.root' %baseDir, hist_bkg_mgg )

        samplesWgg.Draw( 'pt_leadph12', 'PUWeight * (el_passtrig_n==1 && el_n==1 && ph_medium_n>1 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.3 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && !(fabs(m_leadLep_ph1_ph2-91.2)<5) && !(fabs(m_leadLep_ph1-91.2)<5) && !(fabs(m_leadLep_ph2-91.2)<5) && ph_Is%s[0] && ph_Is%s[1] ) ' %(reg[0], reg[1]), [0,5,10,15,25,40,70,200] )

        hist_data_egg = samplesWgg.get_samples(name='Data')[0].hist.Clone('pt_leadph12_egg_%s-%s'%(reg[0],reg[1]))
        save_hist( '%s/Plots/Data/hist.root' %baseDir, hist_data_egg )

        hist_sig_egg  = samplesWgg.get_samples(name='Wgg')[0].hist.Clone('pt_leadph12_egg_%s-%s'%(reg[0],reg[1]))
        save_hist( '%s/Plots/Wgg/hist.root' %baseDir, hist_sig_egg )

        hist_bkg_egg  = samplesWgg.get_samples(name='AllBkg')[0].hist.Clone('pt_leadph12_egg_%s-%s'%(reg[0],reg[1]))
        save_hist( '%s/Plots/MCBkg/hist.root' %baseDir, hist_bkg_egg )

    # get jet fake background estimate
    file_jet_elfull = open( baseDir + '/jet_fake_results__egg_allZRejCuts.pickle', 'r' )
    file_jet_mu     = open( baseDir + '/jet_fake_results__mgg.pickle', 'r' )

    file_el = open(baseDir + '/electron_fake_results.pickle' )
    file_el_syst = open(baseDir + '/electron_fake_results_syst.pickle' )

    dic_jet_elfull = pickle.load(file_jet_elfull)
    dic_jet_mu     = pickle.load(file_jet_mu    )
    dic_el         = pickle.load( file_el )
    dic_el_syst    = pickle.load( file_el_syst )

    file_jet_elfull.close()
    file_jet_mu    .close()
    file_el        .close()
    file_el_syst   .close()

    samp_list = samplesWgg.get_samples()
    for reg in regions :
        hist_jet_elfull = None
        hist_jet_mu     = None
        hist_el         = None
        for s in samp_list :
            if s.hist is not None :
                hist_jet_elfull = s.hist.Clone( 'pt_leadph12_egg_%s-%s' %(reg[0], reg[1] ) )
                hist_jet_mu     = s.hist.Clone( 'pt_leadph12_mgg_%s-%s' %(reg[0], reg[1] ) )
                hist_el         = s.hist.Clone( 'pt_leadph12_egg_%s-%s' %(reg[0], reg[1] ) )
                break

        for ptbin in range( 1, hist_jet_mu.GetNbinsX()+1 ) :
            min = int(hist_jet_mu.GetXaxis().GetBinLowEdge(ptbin))
            print min
            max = int(hist_jet_mu.GetXaxis().GetBinUpEdge(ptbin))
            print max

            if max <= 15 :
                continue

            maxval = str(max)
            if max > 100 :
                maxval = 'max'

            databin = ( reg[0] ,reg[1], str( min), maxval )

            print databin

            hist_jet_mu.SetBinContent( ptbin, dic_jet_mu['stat+syst']['sum'][databin].n )
            hist_jet_mu.SetBinError( ptbin, dic_jet_mu['stat+syst']['sum'][databin].s )

            hist_jet_elfull.SetBinContent( ptbin, dic_jet_elfull['stat+syst']['sum'][databin].n )
            hist_jet_elfull.SetBinError( ptbin, dic_jet_elfull['stat+syst']['sum'][databin].s )

            hist_el.SetBinContent( ptbin, dic_el[databin].n )
            hist_el.SetBinError( ptbin, dic_el[databin].s )

        save_hist( '%s/Plots/JetFake/hist.root' %baseDir, hist_jet_mu )
        save_hist( '%s/Plots/JetFake/hist.root' %baseDir, hist_jet_elfull )
        save_hist( '%s/Plots/EleFake/hist.root' %baseDir, hist_el )
        

def save_hist( file, hist) :

    dirname = os.path.split( file)[0] 
    if not os.path.isdir( dirname ) :
        os.makedirs( dirname) 
    ofile = ROOT.TFile.Open( file, 'UPDATE' )

    hist.Write()

    ofile.Close()




    




def get_mapped_directory( base_dir_jet, jet_dirs_key ) :
    
    jet_dir_key_map = {}

    for dir in os.listdir( base_dir_jet ) :
        res = re.match( jet_dirs_key, dir )
        if res is not None :
            if len(res.groups() ) == 3 :
                jet_dir_key_map[ ( int(res.group(1)), int(res.group(2)), int(res.group(3)) ) ]  = dir
            elif len(res.groups()) == 0 :
                jet_dir_key_map[ ( 0,0,0 ) ]  = dir


    return jet_dir_key_map

def get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key ) :

    jet_files = {}
    for dir in os.listdir( base_dir_jet ) :
        res = re.match( jet_dirs_key, dir )
        if res is not None :
            iso_key = None
            if len(res.groups() ) == 3 :
                iso_key = ( int(res.group(1)), int(res.group(2)), int(res.group(3)) )
            elif len(res.groups() ) == 0 :
                iso_key = ( 0,0,0 )

            jet_files[iso_key] = {}

            for file in os.listdir( base_dir_jet+'/'+dir  ) :
                fresl = re.match(file_key, file )
                if fresl is not None :
                    if len(fresl.groups()) == 4 :
                        jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4))] = file
                    elif len(fresl.groups()) == 7 :
                        # if the gropus exist, but they're both none, then treat it like there are 4 groups
                        if fresl.group(6) is None and  fresl.group(7) is None :
                            jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4))] = file
                        else :
                            jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4), fresl.group(6), fresl.group(7))] = file
                    elif len(fresl.groups()) == 3 :
                        jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3))] = file

    return jet_files


def MakeSingleEleBkgEstimate(base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, outputDir=None, el_selection='el', namePostfix='') :

    el_acc = ['el', 'elzcr']
    if el_selection not in el_acc :
        print 'Input region not recognized, must be %s' %(','.join(el_acc) )
        return

    samplesWgg.deactivate_all_samples()
    samplesWgg.activate_sample('Data')

    eta_bins = {'EB': [0.0, 0.1, 0.5, 1.0, 1.48 ], 'EE' : [1.57, 2.1, 2.2, 2.3, 2.4, 2.5] }
    regions = ['EB','EE']
    pt_bins = [int(x) for x in options.ptbins.split(',')]

    results_nom = get_ele_single_fakefactors( base_dir_ele, file_bin_map, regions, eta_bins, el_selection )
    results_syst = get_ele_single_fakefactors( base_dir_ele, file_bin_map_syst, regions, eta_bins, el_selection )


    file_key_lead = 'results__%sinvpixlead__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_lead_syst = 'results__syst__%sinvpixlead__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    jet_dir_key_map = {}
    #jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'
    jet_dirs_key = 'JetSinglePhotonFakeNomIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    jet_files_lead      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead      )
    jet_files_lead_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead_syst )

    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')
    pred_lead = get_jet_single_fake_results( jet_files_lead, jet_files_lead_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

    # get fake factors and binning from file
    rfile_coarse = ROOT.TFile.Open( '%s/ElectronFakeFitsRatioCoarseEta/results.root' %base_dir_ele )
    rhist_coarse = rfile_coarse.Get( 'ff') 

    scaled_f = {}
    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]

            ff_lead = -1
            bin_eb = rhist_coarse.GetYaxis().FindBin( 1.0 )
            bin_ee = rhist_coarse.GetYaxis().FindBin( 2.0 )
            bin_pt = rhist_coarse.GetXaxis().FindBin( int(ptmin ) )
            if r1 == 'EB' :
                ff_lead = rhist_coarse.GetBinContent( bin_pt, bin_eb )
                print 'ptmin = %s, ptmax = %s, histptmin = %d, histptmax = %d'  %( ptmin, ptmax, rhist_coarse.GetXaxis().GetBinLowEdge( bin_pt ), rhist_coarse.GetXaxis().GetBinUpEdge( bin_pt ) )
                print 'reg = EB, histetamin = %f, histetamax = %f'  %( rhist_coarse.GetYaxis().GetBinLowEdge( bin_eb ), rhist_coarse.GetYaxis().GetBinUpEdge( bin_eb ) )
            if r1 == 'EE' :
                ff_lead = rhist_coarse.GetBinContent( bin_pt, bin_ee )
                print 'reg = EE, histetamin = %f, histetamax = %f'  %(  rhist_coarse.GetYaxis().GetBinLowEdge( bin_ee ), rhist_coarse.GetYaxis().GetBinUpEdge( bin_ee ) )

            scaled_f[ (r1,ptmin,ptmax) ] = pred_lead['stat+syst']['f'][( r1,ptmin,ptmax)]*ff_lead

    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]
            print '%s, pt %s-%s' %( r1, ptmin, ptmax)
    
            print 'Pred f = %s, scaled f = %s' %( pred_lead['stat+syst']['f'][(r1,ptmin,ptmax)], scaled_f[(r1,ptmin,ptmax)] )


    results_subtracted = {}
    for (r1, ptmin, ptmax), val in results_nom.iteritems() :
            print 'Ele pred Final %s pt %s-%s = %s' %( r1, ptmin, ptmax, val-scaled_f[ (r1,ptmin,ptmax) ]  )
            results_subtracted[(r1,ptmin, ptmax)] = val-scaled_f[ (r1,ptmin,ptmax) ] 


    results_syst_subtracted = {}
    for (r1, ptmin, ptmax), val in results_syst.iteritems() :
            results_syst_subtracted[(r1, ptmin, ptmax)] = val-scaled_f[ (r1,ptmin,ptmax) ] 


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

        file_raw = open( outputDir + '/electron_fake_results%s__noJetFakeSubtraction.pickle' %namePostfix, 'w' )
        pickle.dump( results_nom, file_raw )
        file_raw.close()

        file_sub = open( outputDir + '/electron_fake_results%s.pickle' %namePostfix, 'w' )
        pickle.dump( results_subtracted, file_sub )
        file_sub.close()

        file_sub_syst = open( outputDir + '/electron_fake_results_syst%s.pickle' %namePostfix, 'w' )
        pickle.dump( results_syst_subtracted, file_sub_syst )
        file_sub_syst.close()

def MakeEleBkgEstimate(base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, outputDir=None, el_selection='elfull', namePostfix='') :

    el_acc = ['elfull', 'elzcr']
    if el_selection not in el_acc :
        print 'Input region not recognized, must be %s' %(','.join(el_acc) )
        return

    samplesWgg.deactivate_all_samples()
    samplesWgg.activate_sample('Data')

    eta_bins = {'EB': [0.0, 0.1, 0.5, 1.0, 1.48 ], 'EE' : [1.57, 2.1, 2.2, 2.3, 2.4, 2.5] }
    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB'), ('EE', 'EE')]
    pt_bins = [int(x) for x in options.ptbins.split(',')]

    results_nom = get_ele_fakefactors( base_dir_ele, file_bin_map, regions, eta_bins, el_selection )
    results_syst = get_ele_fakefactors( base_dir_ele, file_bin_map_syst, regions, eta_bins, el_selection )

    file_key_lead = 'results__%sinvpixlead__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_subl = 'results__%sinvpixsubl__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_lead_syst = 'results__syst__%sinvpixlead__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_subl_syst = 'results__syst__%sinvpixsubl__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    jet_dir_key_map = {}
    jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    jet_files_lead      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead      )
    jet_files_subl      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_subl      )
    jet_files_lead_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead_syst )
    jet_files_subl_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_subl_syst )

    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')
    #subl_ptbins = [ ( '70', 'max', '15', '25' ), ( '70', 'max', '25', 'max' ) ]
    subl_ptbins = [  ]
    pred_lead = get_jet_fake_results( jet_files_lead, jet_files_lead_syst, regions, pt_bins_jetfile, jet_dir_key_map, base_dir_jet,  pt_bins_subl=subl_ptbins ) 
    pred_subl = get_jet_fake_results( jet_files_subl, jet_files_subl_syst, regions, pt_bins_jetfile, jet_dir_key_map, base_dir_jet,  pt_bins_subl=subl_ptbins ) 

    # get fake factors and binning from file
    rfile_coarse = ROOT.TFile.Open( '%s/ElectronFakeFitsRatioCoarseEta/results.root' %base_dir_ele )
    rhist_coarse = rfile_coarse.Get( 'ff') 

    scaled_rf = {}
    scaled_fr = {}
    scaled_ff = {}
    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]

            ff_lead = -1
            ff_subl = -1
            bin_eb = rhist_coarse.GetYaxis().FindBin( 1.0 )
            bin_ee = rhist_coarse.GetYaxis().FindBin( 2.0 )
            bin_pt = rhist_coarse.GetXaxis().FindBin( int(ptmin ) )
            if r1 == 'EB' :
                ff_lead = rhist_coarse.GetBinContent( bin_pt, bin_eb )
                print 'ptmin = %s, ptmax = %s, histptmin = %d, histptmax = %d'  %( ptmin, ptmax, rhist_coarse.GetXaxis().GetBinLowEdge( bin_pt ), rhist_coarse.GetXaxis().GetBinUpEdge( bin_pt ) )
                print 'reg = EB, histetamin = %f, histetamax = %f'  %( rhist_coarse.GetYaxis().GetBinLowEdge( bin_eb ), rhist_coarse.GetYaxis().GetBinUpEdge( bin_eb ) )
            if r1 == 'EE' :
                ff_lead = rhist_coarse.GetBinContent( bin_pt, bin_ee )
                print 'reg = EE, histetamin = %f, histetamax = %f'  %(  rhist_coarse.GetYaxis().GetBinLowEdge( bin_ee ), rhist_coarse.GetYaxis().GetBinUpEdge( bin_ee ) )

            if r2 == 'EB' :
                ff_subl = rhist_coarse.GetBinContent( bin_pt, bin_eb )
            if r2 == 'EE' :
                ff_subl = rhist_coarse.GetBinContent( bin_pt, bin_ee )


            scaled_rf[ (r1,r2,ptmin,ptmax) ] = pred_lead['stat+syst']['rf'][( r1,r2,ptmin,ptmax)]*ff_lead + pred_subl['stat+syst']['rf'][( r1,r2,ptmin,ptmax)]*ff_subl
            scaled_fr[ (r1,r2,ptmin,ptmax) ] = pred_lead['stat+syst']['fr'][( r1,r2,ptmin,ptmax)]*ff_lead + pred_subl['stat+syst']['fr'][( r1,r2,ptmin,ptmax)]*ff_subl
            scaled_ff[ (r1,r2,ptmin,ptmax) ] = pred_lead['stat+syst']['ff'][( r1,r2,ptmin,ptmax)]*ff_lead + pred_subl['stat+syst']['ff'][( r1,r2,ptmin,ptmax)]*ff_subl

            #scaled_rf[ (r1,r2,ptmin,ptmax) ] = pred_lead['rf'][( r1,r2,ptmin,ptmax)] + pred_subl['rf'][( r1,r2,ptmin,ptmax)]
            #scaled_fr[ (r1,r2,ptmin,ptmax) ] = pred_lead['fr'][( r1,r2,ptmin,ptmax)] + pred_subl['fr'][( r1,r2,ptmin,ptmax)]
            #scaled_ff[ (r1,r2,ptmin,ptmax) ] = pred_lead['ff'][( r1,r2,ptmin,ptmax)] + pred_subl['ff'][( r1,r2,ptmin,ptmax)]

    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]
            print '%s-%s, pt %s-%s' %( r1, r2, ptmin, ptmax)
    
            print 'Pred rf = %s, scaled rf = %s' %( pred_lead['stat+syst']['rf'][(r1,r2,ptmin,ptmax)]+pred_subl['stat+syst']['rf'][(r1,r2,ptmin,ptmax)], scaled_rf[(r1,r2,ptmin,ptmax)] )
            print 'Pred fr = %s, scaled fr = %s' %( pred_lead['stat+syst']['fr'][(r1,r2,ptmin,ptmax)]+pred_subl['stat+syst']['fr'][(r1,r2,ptmin,ptmax)], scaled_fr[(r1,r2,ptmin,ptmax)] )
            print 'Pred ff = %s, scaled ff = %s' %( pred_lead['stat+syst']['ff'][(r1,r2,ptmin,ptmax)]+pred_subl['stat+syst']['ff'][(r1,r2,ptmin,ptmax)], scaled_ff[(r1,r2,ptmin,ptmax)] )


    results_subtracted = {}
    for (r1,r2, ptmin, ptmax), val in results_nom.iteritems() :
            print 'Ele pred Final %s-%s pt %s-%s = %s' %( r1, r2, ptmin, ptmax, val-scaled_rf[ (r1,r2,ptmin,ptmax) ] + scaled_fr[ (r1,r2,ptmin,ptmax) ] + scaled_ff[ (r1,r2,ptmin,ptmax) ] )
            results_subtracted[(r1,r2, ptmin, ptmax)] = val-scaled_rf[ (r1,r2,ptmin,ptmax) ] + scaled_fr[ (r1,r2,ptmin,ptmax) ] + scaled_ff[ (r1,r2,ptmin,ptmax) ] 


    results_syst_subtracted = {}
    for (r1,r2, ptmin, ptmax), val in results_syst.iteritems() :
            results_syst_subtracted[(r1,r2, ptmin, ptmax)] = val-scaled_rf[ (r1,r2,ptmin,ptmax) ] + scaled_fr[ (r1,r2,ptmin,ptmax) ] + scaled_ff[ (r1,r2,ptmin,ptmax) ] 


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

        file_raw = open( outputDir + '/electron_fake_results%s__noJetFakeSubtraction.pickle' %namePostfix, 'w' )
        pickle.dump( results_nom, file_raw )
        file_raw.close()

        file_sub = open( outputDir + '/electron_fake_results%s.pickle' %namePostfix, 'w' )
        pickle.dump( results_subtracted, file_sub )
        file_sub.close()

        file_sub_syst = open( outputDir + '/electron_fake_results_syst%s.pickle' %namePostfix, 'w' )
        pickle.dump( results_syst_subtracted, file_sub_syst )
        file_sub_syst.close()


def get_ele_fakefactors( base_dir_ele, file_bin_map, regions, eta_bins, el_selection ) :

    results_lead = {}
    results_subl = {}
    for file, ptbins in file_bin_map.iteritems() :

        # get root file
        if not os.path.isfile( '%s/%s/results.root'%(base_dir_ele, file ) ) :
            return {}

        rfile = ROOT.TFile.Open( '%s/%s/results.root'%(base_dir_ele, file ) )
        rhist = rfile.Get('ff')

        nxbins = rhist.GetXaxis().GetNbins()
        nybins = rhist.GetYaxis().GetNbins()
        xmin = rhist.GetXaxis().GetBinLowEdge(1)
        xmax = rhist.GetXaxis().GetBinUpEdge(nxbins)
        ymin = rhist.GetYaxis().GetBinLowEdge(1)
        ymax = rhist.GetYaxis().GetBinUpEdge(nybins)

        data_samp = samplesWgg.get_samples( name='Data' )[0]
        # get data counts from inverted pixel seed 
        for r1, r2 in regions :
            #invert lead, draw lead
            samplesWgg.create_hist(data_samp, 'fabs(ph_eta[0]):ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] )' %(el_cuts[el_selection]['invlead'], r1, r2), (nxbins, xmin, xmax, nybins, ymin, ymax) )

            hist_lead = data_samp.hist.Clone('hist_lead__%s-%s' %(r1,r2))

            for ptmin, ptmax in ptbins :
                results_lead[(r1, r2, ptmin, ptmax)] = 0
                for eidx, etamin in enumerate( eta_bins[r1][:-1] ) :
                    etamax = eta_bins[r1][eidx+1]


                    # get the bins.  For the max bin subtract 1 because
                    # you get the bin above the value
                    ptbinmin = hist_lead.GetXaxis().FindBin( int(ptmin) )
                    if ptmax == 'max' :
                        ptbinmax = hist_lead.GetNbinsX()
                    else :
                        ptbinmax = hist_lead.GetXaxis().FindBin( int(ptmax) )-1

                    etabinmin = hist_lead.GetYaxis().FindBin( etamin )
                    etabinmax = hist_lead.GetYaxis().FindBin( etamax )-1

                    nData = hist_lead.Integral( ptbinmin, ptbinmax, etabinmin, etabinmax )
                    ff = rhist.GetBinContent( ptbinmin, etabinmin )

                    print 'ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptbinmax = %d, etabinmin = %d, etabinmax = %d' %( ptmin, ptmax, etamin, etamax, ptbinmin, ptbinmax, etabinmin, etabinmax )
                    print 'GetBinContent in %f < pt < %f, %f < eta < %f ' %( rhist.GetXaxis().GetBinLowEdge(ptbinmin), rhist.GetXaxis().GetBinUpEdge(ptbinmax), rhist.GetYaxis().GetBinLowEdge(etabinmin), rhist.GetYaxis().GetBinUpEdge(etabinmin) )

                    results_lead[(r1, r2, ptmin, ptmax)]  = results_lead[(r1,r2, ptmin, ptmax)] + nData*ff
                    #results_lead[(r1, r2, ptmin, ptmax)]  = results_lead[(r1,r2, ptmin, ptmax)] + nData

            #invert subl, draw subl
            samplesWgg.create_hist(data_samp, 'fabs(ph_eta[1]):ph_pt[1]', ' PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] )' %(el_cuts[el_selection]['invsubl'], r1, r2), (nxbins, xmin, xmax, nybins, ymin, ymax) )

            hist_subl = data_samp.hist.Clone('hist_subl__%s-%s' %(r1,r2))

            for ptmin, ptmax in ptbins :
                results_subl[(r1, r2, ptmin, ptmax)] = 0
                for eidx, etamin in enumerate( eta_bins[r2][:-1] ) :
                    etamax = eta_bins[r2][eidx+1]

                    ptbinmin = hist_subl.GetXaxis().FindBin( int(ptmin) )
                    if ptmax == 'max' :
                        ptbinmax = hist_subl.GetNbinsX()
                    else :
                        ptbinmax = hist_subl.GetXaxis().FindBin( int(ptmax) )-1

                    etabinmin = hist_subl.GetYaxis().FindBin( etamin )
                    etabinmax = hist_subl.GetYaxis().FindBin( etamax )-1

                    nData = hist_subl.Integral( ptbinmin, ptbinmax, etabinmin, etabinmax )
                    ff = rhist.GetBinContent( ptbinmin, etabinmin )

                    results_subl[(r1, r2, ptmin, ptmax)]  = results_subl[(r1,r2, ptmin, ptmax)] + nData*ff
                    #results_subl[(r1, r2, ptmin, ptmax)]  = results_subl[(r1,r2, ptmin, ptmax)] + nData

        rfile.Close()

    results_full= {}
    for bin, val in results_lead.iteritems() : 
        results_full[bin] = val
    for bin, val in results_subl.iteritems() : 
        results_full[bin] = results_full[bin] + val

    return results_full

def get_ele_single_fakefactors( base_dir_ele, file_bin_map, regions, eta_bins, el_selection ) :

    results_lead = {}
    results_subl = {}
    for file, ptbins in file_bin_map.iteritems() :

        # get root file
        rfile = ROOT.TFile.Open( '%s/%s/results.root'%(base_dir_ele, file ) )
        rhist = rfile.Get('ff')

        nxbins = rhist.GetXaxis().GetNbins()
        nybins = rhist.GetYaxis().GetNbins()
        xmin = rhist.GetXaxis().GetBinLowEdge(1)
        xmax = rhist.GetXaxis().GetBinUpEdge(nxbins)
        ymin = rhist.GetYaxis().GetBinLowEdge(1)
        ymax = rhist.GetYaxis().GetBinUpEdge(nybins)

        data_samp = samplesWg.get_samples( name='Electron' )[0]
        # get data counts from inverted pixel seed 
        for r1 in regions :
            #invert lead, draw lead
            samplesWg.create_hist(data_samp, 'fabs(ph_eta[0]):ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[0] && mt_lep_met > 80 )' %(el_cuts['single'+el_selection], r1, ), (nxbins, xmin, xmax, nybins, ymin, ymax) )

            hist_lead = data_samp.hist.Clone('hist_lead__%s' %(r1))

            for ptmin, ptmax in ptbins :
                results_lead[(r1, ptmin, ptmax)] = 0
                for eidx, etamin in enumerate( eta_bins[r1][:-1] ) :
                    etamax = eta_bins[r1][eidx+1]

                    # get the bins.  For the max bin subtract 1 because
                    # you get the bin above the value
                    ptbinmin = hist_lead.GetXaxis().FindBin( int(ptmin) )
                    if ptmax == 'max' :
                        ptbinmax = hist_lead.GetNbinsX()
                    else :
                        ptbinmax = hist_lead.GetXaxis().FindBin( int(ptmax) )-1

                    etabinmin = hist_lead.GetYaxis().FindBin( etamin )
                    etabinmax = hist_lead.GetYaxis().FindBin( etamax )-1

                    nData = hist_lead.Integral( ptbinmin, ptbinmax, etabinmin, etabinmax )
                    ff = rhist.GetBinContent( ptbinmin, etabinmin )

                    print 'ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptbinmax = %d, etabinmin = %d, etabinmax = %d' %( ptmin, ptmax, etamin, etamax, ptbinmin, ptbinmax, etabinmin, etabinmax )
                    print 'GetBinContent in %f < pt < %f, %f < eta < %f ' %( rhist.GetXaxis().GetBinLowEdge(ptbinmin), rhist.GetXaxis().GetBinUpEdge(ptbinmax), rhist.GetYaxis().GetBinLowEdge(etabinmin), rhist.GetYaxis().GetBinUpEdge(etabinmin) )

                    results_lead[(r1, ptmin, ptmax)]  = results_lead[(r1, ptmin, ptmax)] + nData*ff

    return results_lead

def get_jet_fake_results( jet_files, jet_files_syst, regions, pt_bins,  jet_dir_key_map, base_dir_jet, pt_bins_subl=[] ) :
    """ Get the fake results for all pt and eta regions 
    
        Check if the data counts that were input to the 
        fit are non-zero.  If so, move to a looser isolation.
        If the values are never set, ie even in the loosest
        case there are no data counts, then use the 
        original with zero values
    """

    results = {'stat' : {}, 'syst' : {}, 'stat+syst' : {} }
    for val in results.values() :
       val['rf'] = {}
       val['fr'] = {}
       val['ff'] = {}
       val['sum'] = {}


    sorted_jet_dirs = jet_files.keys()
    sorted_jet_dirs.sort()

    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins[:-1]) :
            ptmax = pt_bins[idx+1]

            reg_bin = (r1, r2, ptmin, ptmax) 

            make_background_estimate( base_dir_jet, jet_files, jet_files_syst, jet_dir_key_map, sorted_jet_dirs, reg_bin, results )

        for ptlmin, ptlmax, ptsmin, ptsmax in pt_bins_subl :

            reg_bin = (r1, r2, ptlmin, ptlmax, ptsmin, ptsmax )

            make_background_estimate( base_dir_jet, jet_files, jet_files_syst, jet_dir_key_map, sorted_jet_dirs, reg_bin, results )

    return results

def make_background_estimate( base_dir_jet, jet_files, jet_files_syst, jet_dir_key_map, sorted_jet_dirs, reg_bin, results ) :

    for val in results.values() :
        val['rf'][reg_bin] = None
        val['fr'][reg_bin] = None
        val['ff'][reg_bin] = None
        val['sum'][reg_bin] = None

    for dir_key in sorted_jet_dirs :
        
        fentries = jet_files[dir_key]
        fentries_syst = jet_files_syst[dir_key]

        if reg_bin not in fentries :
            print 'Bin not found', reg_bin
            continue

        # get the file 
        sub_dir_jet = jet_dir_key_map[dir_key]

        file_loc = base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin]

        if not os.path.isfile( file_loc ) :
            continue

        ofile = open(file_loc)
        predictions = pickle.load(ofile)
        ofile.close()

        file_loc_syst = base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin]
        ofile = open(file_loc_syst)
        predictions_syst = pickle.load(ofile)
        ofile.close()

        # get the data
        Ndata_tl = predictions['Ndata_TL']
        Ndata_lt = predictions['Ndata_LT']
        Ndata_ll = predictions['Ndata_LL']

        if Ndata_tl == 0 or Ndata_lt == 0 or Ndata_ll == 0 :
            print 'No data entries for AsymIso %d-%d-%d, region %s-%s, pt %s-%s ' %( dir_key[0], dir_key[1], dir_key[2], reg_bin[0], reg_bin[1], reg_bin[2], reg_bin[3])
            print 'Ndata_tl = %s, Ndata_lt = %s, Ndata_ll = %s' %( Ndata_tl, Ndata_lt, Ndata_ll)
            continue

        Npred_rf = predictions['Npred_RF_TT']
        Npred_fr = predictions['Npred_FR_TT']
        Npred_ff = predictions['Npred_FF_TT']

        Npred_rf_syst = predictions_syst['Npred_RF_TT']
        Npred_fr_syst = predictions_syst['Npred_FR_TT']
        Npred_ff_syst = predictions_syst['Npred_FF_TT']

        results['stat']['rf'][reg_bin] = Npred_rf
        results['stat']['fr'][reg_bin] = Npred_fr
        results['stat']['ff'][reg_bin] = Npred_ff
        results['stat']['sum'][reg_bin] = Npred_ff+Npred_rf+Npred_fr

        results['syst']['rf'][reg_bin] = Npred_rf_syst
        results['syst']['fr'][reg_bin] = Npred_fr_syst
        results['syst']['ff'][reg_bin] = Npred_ff_syst
        results['syst']['sum'][reg_bin] = Npred_rf_syst+Npred_fr_syst+Npred_ff_syst

        Npred_rf_tot = Npred_rf
        Npred_fr_tot = Npred_fr
        Npred_ff_tot = Npred_ff

        Npred_rf_syst_zero =ufloat( 0, Npred_rf_syst.s )
        Npred_fr_syst_zero =ufloat( 0, Npred_fr_syst.s )
        Npred_ff_syst_zero =ufloat( 0, Npred_ff_syst.s )

        Npred_rf_tot += Npred_rf_syst_zero
        Npred_fr_tot += Npred_fr_syst_zero
        Npred_ff_tot += Npred_ff_syst_zero
        
        results['stat+syst']['rf'][reg_bin] = Npred_rf_tot
        results['stat+syst']['fr'][reg_bin] = Npred_fr_tot
        results['stat+syst']['ff'][reg_bin] = Npred_ff_tot
        results['stat+syst']['sum'][reg_bin] = Npred_rf_tot+Npred_fr_tot+Npred_ff_tot

        break

    # if results weren't set in any cases above, 
    # get the results from the first entry
    if results['stat']['rf'][reg_bin] is None or results['stat']['fr'][reg_bin] is None or results['stat']['ff'][reg_bin] is None :

        dir_key = sorted_jet_dirs[0]

        fentries = jet_files[dir_key]

        sub_dir_jet = jet_dir_key_map[dir_key]

        file_loc = base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin]
        if not os.path.isfile( file_loc ) :
            print 'Could not locate file ', file_loc
            return
        ofile = open(file_loc)
        predictions = pickle.load(ofile)
        ofile.close()

        ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin])
        predictions_syst = pickle.load(ofile)
        ofile.close()

        Npred_rf = predictions['Npred_RF_TT']
        Npred_fr = predictions['Npred_FR_TT']
        Npred_ff = predictions['Npred_FF_TT']

        Npred_rf_syst = predictions_syst['Npred_RF_TT']
        Npred_fr_syst = predictions_syst['Npred_FR_TT']
        Npred_ff_syst = predictions_syst['Npred_FF_TT']

        results['stat']['rf'][reg_bin] = Npred_rf
        results['stat']['fr'][reg_bin] = Npred_fr
        results['stat']['ff'][reg_bin] = Npred_ff
        results['stat']['sum'][reg_bin] = Npred_ff+Npred_rf+Npred_fr

        results['syst']['rf'][reg_bin] = Npred_rf_syst
        results['syst']['fr'][reg_bin] = Npred_fr_syst
        results['syst']['ff'][reg_bin] = Npred_ff_syst
        results['syst']['sum'][reg_bin] = Npred_rf_syst+Npred_fr_syst+Npred_ff_syst

        Npred_rf_tot = Npred_rf
        Npred_fr_tot = Npred_fr
        Npred_ff_tot = Npred_ff

        Npred_rf_syst_zero =ufloat( 0, Npred_rf_syst.s )
        Npred_fr_syst_zero =ufloat( 0, Npred_fr_syst.s )
        Npred_ff_syst_zero =ufloat( 0, Npred_ff_syst.s )

        Npred_rf_tot += Npred_rf_syst_zero
        Npred_fr_tot += Npred_fr_syst_zero
        Npred_ff_tot += Npred_ff_syst_zero
        
        results['stat+syst']['rf'][reg_bin] = Npred_rf_tot
        results['stat+syst']['fr'][reg_bin] = Npred_fr_tot
        results['stat+syst']['ff'][reg_bin] = Npred_ff_tot
        results['stat+syst']['sum'][reg_bin] = Npred_rf_tot+Npred_fr_tot+Npred_ff_tot

def get_jet_single_fake_results( jet_files, jet_files_syst, regions, pt_bins,  jet_dir_key_map, base_dir_jet ) :
    """ Get the fake results for all pt and eta regions 
    
        Check if the data counts that were input to the 
        fit are non-zero.  If so, move to a looser isolation.
        If the values are never set, ie even in the loosest
        case there are no data counts, then use the 
        original with zero values
    """

    results = {'stat' : {}, 'syst' : {}, 'stat+syst' : {} }
    for val in results.values() :
       val['f'] = {}
       val['r'] = {}

    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins[:-1]) :
            ptmax = pt_bins[idx+1]

            reg_bin = (r1, ptmin, ptmax) 

            sorted_jet_dirs = jet_files.keys()
            sorted_jet_dirs.sort()

            for val in results.values() :
                val['r'][reg_bin] = None
                val['f'][reg_bin] = None

            for dir_key in sorted_jet_dirs :
                
                fentries = jet_files[dir_key]
                fentries_syst = jet_files_syst[dir_key]

                if reg_bin not in fentries :
                    continue

                sub_dir_jet = jet_dir_key_map[dir_key]

                ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin])
                predictions = pickle.load(ofile)
                ofile.close()

                ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin])
                predictions_syst = pickle.load(ofile)
                ofile.close()

                Ndata_t = predictions['Ndata_T']
                Ndata_l = predictions['Ndata_L']

                if Ndata_t == 0 or Ndata_l == 0 :
                    print 'No data entries for AsymIso %d-%d-%d, region %s-%s, pt %s-%s ' %( dir_key[0], dir_key[1], dir_key[2], r1, r2, ptmin, ptmax )
                    print 'Ndata_tl = %s, Ndata_lt = %s, Ndata_ll = %s' %( Ndata_tl, Ndata_lt, Ndata_ll)
                    continue

                Npred_f = predictions['Npred_F_T']
                Npred_r = predictions['Npred_R_T']

                Npred_f_syst = predictions_syst['Npred_R_T']
                Npred_r_syst = predictions_syst['Npred_F_T']

                results['stat']['r'][reg_bin] = Npred_r
                results['stat']['f'][reg_bin] = Npred_f

                results['syst']['r'][reg_bin] = Npred_r_syst
                results['syst']['f'][reg_bin] = Npred_f_syst

                Npred_r_tot = Npred_r
                Npred_f_tot = Npred_f

                Npred_r_syst_zero =ufloat( 0, Npred_r_syst.s )
                Npred_f_syst_zero =ufloat( 0, Npred_f_syst.s )

                Npred_r_tot += Npred_r_syst_zero
                Npred_f_tot += Npred_f_syst_zero
                
                results['stat+syst']['r'][reg_bin] = Npred_r_tot
                results['stat+syst']['f'][reg_bin] = Npred_f_tot

                break

            # if results weren't set in any cases above, 
            # get the results from the first entry
            if results['stat']['r'][reg_bin] is None or results['stat']['f'][reg_bin] is None :

                dir_key = sorted_jet_dirs[0]

                fentries = jet_files[dir_key]

                sub_dir_jet = jet_dir_key_map[dir_key]

                print fentries

                ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin])
                predictions = pickle.load(ofile)
                ofile.close()

                ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin])
                predictions_syst = pickle.load(ofile)
                ofile.close()

                Npred_r = predictions['Npred_R_T']
                Npred_f = predictions['Npred_F_T']

                Npred_r_syst = predictions_syst['Npred_R_T']
                Npred_f_syst = predictions_syst['Npred_F_T']

                results['stat']['r'][reg_bin] = Npred_r
                results['stat']['f'][reg_bin] = Npred_f

                results['syst']['r'][reg_bin] = Npred_r_syst
                results['syst']['f'][reg_bin] = Npred_f_syst

                Npred_r_tot = Npred_r
                Npred_f_tot = Npred_f

                Npred_r_syst_zero =ufloat( 0, Npred_r_syst.s )
                Npred_f_syst_zero =ufloat( 0, Npred_f_syst.s )

                Npred_r_tot += Npred_r_syst_zero
                Npred_f_tot += Npred_f_syst_zero
                
                results['stat+syst']['r'][reg_bin] = Npred_r_tot
                results['stat+syst']['f'][reg_bin] = Npred_f_tot

    return results

main()
