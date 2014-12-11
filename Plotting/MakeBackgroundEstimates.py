"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
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
samplesWggInvSubl = None
samplesWggInvLead = None

ph_cuts = ''
lead_dr_cut = 0.4
subl_dr_cut = 0.4
phot_dr_cut = 0.4

el_cuts = {'elfull' : 
           {'invlead' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep >%f && dr_ph2_leadLep>%f && mu_n==0 && !(fabs(m_leadLep_ph1_ph2-91.2) < 5) && !(fabs(m_leadLep_ph1-91.2) < 5)  && !(fabs(m_leadLep_ph2-91.2) < 5) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
            'invsubl' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%f && dr_ph2_leadLep>%f && mu_n==0 && !(fabs(m_leadLep_ph1_ph2-91.2) < 5) && !(fabs(m_leadLep_ph1-91.2) < 5)  && !(fabs(m_leadLep_ph2-91.2) < 5) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           },
           'elzcr' :
           {
            #'invlead' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%f && dr_ph2_leadLep>%f && mu_n==0 && ( (fabs(m_leadLep_ph1_ph2-91.2) < 5) || (fabs(m_leadLep_ph1-91.2) < 5) || (fabs(m_leadLep_ph2-91.2) < 5) ) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           # 'invsubl' : ' el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%f && dr_ph2_leadLep>%f && mu_n==0 && ( (fabs(m_leadLep_ph1_ph2-91.2) < 5) || (fabs(m_leadLep_ph1-91.2) < 5)  || (fabs(m_leadLep_ph2-91.2) < 5) ) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           'invlead' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%f && dr_ph2_leadLep>%f && mu_n==0 && (fabs(m_leadLep_ph1_ph2-91.2) < 5) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
            'invsubl' : ' el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%f && dr_ph2_leadLep>%f && mu_n==0 && (fabs(m_leadLep_ph1_ph2-91.2) < 5) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           },
           'elbase' : 
           {'invlead' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f && mu_n==0 && m_ph1_ph2>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts),
            'invsubl' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f && mu_n==0 && m_ph1_ph2>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts) 
          },
}

_asym_iso_syst = { (0, 0, 0) : 0.05, (5,3,3) : 0.05, (8,5,5) : 0.10, (10, 7, 7) : 0.15, (12, 9, 9) : 0.2, (15,11,11) : 0.25, (20, 16, 16) : 0.35 }

def main() :

    p = ArgumentParser()
    
                                                                                           
    p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
    p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',  required=False,       help='Input directory base')
    p.add_argument('--plotDir',     default='Plots',  type=str ,        dest='plotDir',  required=False,       help='Directory where plots are written')
    p.add_argument('--ptbins',     default='15,25,40,70,1000000',  type=str ,        dest='ptbins',  required=False,       help='PT bins to use')
    
    options = p.parse_args()

    global samplesWgg
    global samplesWggInvLead
    global samplesWggInvSubl
    global samplesWg

    baseDirWgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNomUnblindLowPt_2014_12_08'
    #baseDirWgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNomUnblindEleZCR_2014_12_08'
    #baseDirWgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNomUnblindEle_2014_12_08'
    baseDirWg  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2014_12_08'
    baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvPixSeedLead_2014_12_08'
    baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvPixSeedSubl_2014_12_08'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfWgg = 'Modules/Wgamgam.py'

    samplesWgg = SampleManager(baseDirWgg, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWggInvLead = SampleManager(baseDirWggInvLead, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWggInvSubl = SampleManager(baseDirWggInvSubl, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWg  = SampleManager(baseDirWg,  treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesWgg.ReadSamples( sampleConfWgg )
    samplesWggInvLead.ReadSamples( sampleConfWgg )
    samplesWggInvSubl.ReadSamples( sampleConfWgg )
    samplesWg .ReadSamples( sampleConfWgg )

    bins = options.ptbins.split(',')


    file_bin_map = {'ElectronFakeFitsRatio' : [(bins[0], bins[1]), (bins[1], bins[2]), (bins[3], 'max')], 'ElectronFakeFitsRatioMCTemplateNDKeys': [(bins[2], bins[3]) ] }
    file_bin_map_coarse = {'ElectronFakeFitsRatioCoarseEta' : [(bins[0], bins[1]), (bins[1], bins[2]), (bins[3], 'max')], 'ElectronFakeFitsRatioMCTemplateNDKeysCoarseEta': [(bins[2], bins[3]) ] }
    file_bin_map_syst = {'ElectronFakeFitsRatioMCTemplateNDKeys' : [(bins[0], bins[1]), (bins[1], bins[2]), (bins[3], 'max')], 'ElectronFakeFitsRatio': [(bins[2], bins[3]) ] }
    file_bin_map_coarse_syst = {'ElectronFakeFitsRatioMCTemplateNDKeysCoarseEta' : [(bins[0], bins[1]), (bins[1], bins[2]), (bins[3], 'max')], 'ElectronFakeFitsRatioCoarseEta': [(bins[2], bins[3]) ] }

    ele_eta_bins = {'EB': [0.0, 0.1, 0.5, 1.0, 1.44 ], 'EE' : [1.57, 2.1, 2.2, 2.3, 2.4, 2.5] }
    ele_eta_bins_coarse = {'EB': [0.0, 1.44 ], 'EE' : [1.57, 2.5] }

    pt_bins = [int(x) for x in options.ptbins.split(',')]

    if options.baseDir is not None :
        base_dir_ele = options.baseDir
        base_dir_jet = '%s/JetFakeResultsSyst'%options.baseDir
        outputDir='%s/BackgroundEstimates'%options.baseDir
        MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, eta_bins=ele_eta_bins, pt_bins=pt_bins, el_selection='elfull', outputDir=outputDir )
        MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, eta_bins=ele_eta_bins, pt_bins=pt_bins, el_selection='elzcr', outputDir=outputDir, namePostfix='__zcr' )
        MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map_coarse, file_bin_map_coarse_syst, eta_bins=ele_eta_bins_coarse, pt_bins=pt_bins, el_selection='elfull', outputDir=outputDir, namePostfix='__coarse' )
        MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map_coarse, file_bin_map_coarse_syst, eta_bins=ele_eta_bins_coarse, pt_bins=pt_bins, el_selection='elzcr', outputDir=outputDir, namePostfix='__coarse__zcr' )

        MakeJetBkgEstimate( base_dir_jet, pt_bins, outputDir )

        MakeBkgEstimatePlots( outputDir, options.plotDir )

    print '^_^ FINSISHED ^_^'
    print 'It is safe to kill the program if it is hanging'

def MakeJetBkgEstimate( base_dir_jet, pt_bins, outputDir=None ) :

    print '--------------------------------------'
    print 'START JET FAKE ESTIMATE'
    print '--------------------------------------'

    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB')]

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
        print '---------------------------------------------'
        print 'JET FAKE RESULTS, MUON CHANNEL'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['stat']['rf'][bin]['result'], pred_mu['stat']['fr'][bin]['result'], pred_mu['stat']['ff'][bin]['result'], (  pred_mu['stat']['rf'][bin]['result']+ pred_mu['stat']['fr'][bin]['result']+ pred_mu['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['syst']['rf'][bin]['result'], pred_mu['syst']['fr'][bin]['result'], pred_mu['syst']['ff'][bin]['result'], (  pred_mu['syst']['rf'][bin]['result']+ pred_mu['syst']['fr'][bin]['result']+ pred_mu['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['stat+syst']['rf'][bin]['result'], pred_mu['stat+syst']['fr'][bin]['result'], pred_mu['stat+syst']['ff'][bin]['result'], (  pred_mu['stat+syst']['rf'][bin]['result']+ pred_mu['stat+syst']['fr'][bin]['result']+ pred_mu['stat+syst']['ff'][bin]['result'] ) )

        file_muon = open( outputDir + '/jet_fake_results__mgg.pickle', 'w' )
        pickle.dump( pred_mu, file_muon )
        file_muon.close()

    if jet_files_elfull.values()[0] :
        pred_elfull = get_jet_fake_results( jet_files_elfull, jet_files_elfull_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print '---------------------------------------------'
        print 'JET FAKE RESULTS, ELECTRON CHANNEL WITH Z REJ CUTS'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['stat']['rf'][bin]['result'], pred_elfull['stat']['fr'][bin]['result'], pred_elfull['stat']['ff'][bin]['result'], (  pred_elfull['stat']['rf'][bin]['result']+ pred_elfull['stat']['fr'][bin]['result']+ pred_elfull['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['syst']['rf'][bin]['result'], pred_elfull['syst']['fr'][bin]['result'], pred_elfull['syst']['ff'][bin]['result'], (  pred_elfull['syst']['rf'][bin]['result']+ pred_elfull['syst']['fr'][bin]['result']+ pred_elfull['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['stat+syst']['rf'][bin]['result'], pred_elfull['stat+syst']['fr'][bin]['result'], pred_elfull['stat+syst']['ff'][bin]['result'], (  pred_elfull['stat+syst']['rf'][bin]['result']+ pred_elfull['stat+syst']['fr'][bin]['result']+ pred_elfull['stat+syst']['ff'][bin]['result'] ) )

        file_elfull = open( outputDir + '/jet_fake_results__egg_allZRejCuts.pickle', 'w' )
        pickle.dump( pred_elfull, file_elfull )
        file_elfull.close()

    if jet_files_elzcr.values()[0] :
        pred_elzcr  = get_jet_fake_results( jet_files_elzcr , jet_files_el_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print '---------------------------------------------'
        print 'JET FAKE RESULTS, ELECTRON CHANNEL IN Z CR'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)

                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['stat']['rf'][bin]['result'], pred_elzcr['stat']['fr'][bin]['result'], pred_elzcr['stat']['ff'][bin]['result'], (  pred_elzcr['stat']['rf'][bin]['result']+ pred_elzcr['stat']['fr'][bin]['result']+ pred_elzcr['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['syst']['rf'][bin]['result'], pred_elzcr['syst']['fr'][bin]['result'], pred_elzcr['syst']['ff'][bin]['result'], (  pred_elzcr['syst']['rf'][bin]['result']+ pred_elzcr['syst']['fr'][bin]['result']+ pred_elzcr['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['stat+syst']['rf'][bin]['result'], pred_elzcr['stat+syst']['fr'][bin]['result'], pred_elzcr['stat+syst']['ff'][bin]['result'], (  pred_elzcr['stat+syst']['rf'][bin]['result']+ pred_elzcr['stat+syst']['fr'][bin]['result'] + pred_elzcr['stat+syst']['ff'][bin]['result'] ) )


        file_elzcr = open( outputDir + '/jet_fake_results__egg_ZCR.pickle', 'w' )
        pickle.dump( pred_elzcr, file_elzcr)
        file_elzcr.close()

def MakeBkgEstimatePlots( baseDir, plotDir ) :

    # first make the nominal estimates

    regions = [('EB', 'EB'), ('EB' ,'EE'), ('EE', 'EB')]

    for reg in regions + [(None, None)] :

        if reg[0] is not None :
            reg_str = ' && is%s_leadph12 && is%s_sublph12 ' %(reg[0],reg[1])
            reg_tag = '_%s-%s' %( reg[0], reg[1]) 
        else :
            reg_str = ' && !(isEE_leadph12 && isEE_sublph12 )'
            reg_tag = ''
    
        samplesWgg.activate_sample('AllBkg')
        samplesWgg.Draw( 'pt_leadph12', 'PUWeight * (mu_passtrig25_n>0 && mu_n==1 && ph_medium_n==2 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.4 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 %s  ) ' %(reg_str), [0,5,10,15,25,40,70,200] )

        hist_data_mgg = samplesWgg.get_samples(name='Data')[0].hist.Clone('pt_leadph12_mgg%s'%(reg_tag))
        save_hist( '%s/%s/Data/hist.root' %(baseDir, plotDir), hist_data_mgg )

        hist_sig_mgg  = samplesWgg.get_samples(name='Wgg')[0].hist.Clone('pt_leadph12_mgg%s'%(reg_tag))
        save_hist( '%s/%s/Wgg/hist.root' %(baseDir, plotDir), hist_sig_mgg )

        hist_Zgg_mgg     = samplesWgg.get_samples(name='Zgg')[0].hist.Clone('pt_leadph12_mgg%s'%(reg_tag))
        hist_ZggFSR_mgg  = samplesWgg.get_samples(name='ZgammagammaFSR')[0].hist.Clone('pt_leadph12_mgg%s'%(reg_tag))
        #hist_Zgg_mgg.Add(hist_ZggFSR_mgg)
        add_syst_to_hist( hist_Zgg_mgg, 0.15 )
        add_syst_to_hist( hist_ZggFSR_mgg, 0.15 )

        save_hist( '%s/%s/ZggFSR/hist.root' %(baseDir, plotDir), hist_ZggFSR_mgg )
        save_hist( '%s/%s/Zgg/hist.root' %(baseDir, plotDir), hist_Zgg_mgg )

        hist_bkg_mgg  = samplesWgg.get_samples(name='AllBkg')[0].hist.Clone('pt_leadph12_mgg%s'%(reg_tag))
        save_hist( '%s/%s/MCBkg/hist.root' %(baseDir, plotDir), hist_bkg_mgg )

        samplesWgg.Draw( 'pt_leadph12', 'PUWeight * (el_passtrig_n>0 && el_n==1 && ph_medium_n==2 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.4 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && !(fabs(m_leadLep_ph1_ph2-91.2)<5) && !(fabs(m_leadLep_ph1-91.2)<5) && !(fabs(m_leadLep_ph2-91.2)<5) && is%s_leadph12 && is%s_sublph12 ) ' %(reg[0], reg[1]), [0,5,10,15,25,40,70,200] )

        hist_data_egg = samplesWgg.get_samples(name='Data')[0].hist.Clone('pt_leadph12_egg%s'%(reg_tag))
        save_hist( '%s/%s/Data/hist.root' %(baseDir, plotDir), hist_data_egg )

        hist_sig_egg  = samplesWgg.get_samples(name='Wgg')[0].hist.Clone('pt_leadph12_egg%s'%(reg_tag))
        save_hist( '%s/%s/Wgg/hist.root' %(baseDir, plotDir), hist_sig_egg )

        hist_Zgg_egg     = samplesWgg.get_samples(name='Zgg')[0].hist.Clone('pt_leadph12_egg%s'%(reg_tag))
        hist_ZggFSR_egg  = samplesWgg.get_samples(name='ZgammagammaFSR')[0].hist.Clone('pt_leadph12_egg%s'%(reg_tag))

        add_syst_to_hist( hist_Zgg_egg, 0.15 )
        add_syst_to_hist( hist_ZggFSR_egg, 0.15 )

        #hist_Zgg_egg.Add(hist_ZggFSR_egg)
        save_hist( '%s/%s/ZggFSR/hist.root' %(baseDir, plotDir), hist_ZggFSR_egg )
        save_hist( '%s/%s/Zgg/hist.root' %(baseDir, plotDir), hist_Zgg_egg )

        hist_bkg_egg  = samplesWgg.get_samples(name='AllBkg')[0].hist.Clone('pt_leadph12_egg%s'%(reg_tag))
        save_hist( '%s/%s/MCBkg/hist.root' %(baseDir, plotDir), hist_bkg_egg )

        #samplesWgg.Draw( 'pt_leadph12', 'PUWeight * (el_passtrig_n>0 && el_n==1 && ph_medium_n==2 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.4 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && ( (fabs(m_leadLep_ph1_ph2-91.2)<5) || (fabs(m_leadLep_ph1-91.2)<5) || (fabs(m_leadLep_ph2-91.2)<5) ) && is%s_leadph12 && is%s_sublph12 ) ' %(reg[0], reg[1]), [0,5,10,15,25,40,70,200] )
        samplesWgg.Draw( 'pt_leadph12', 'PUWeight * (el_passtrig_n>0 && el_n==1 && ph_medium_n==2 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.4 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && (fabs(m_leadLep_ph1_ph2-91.2)<5) && is%s_leadph12 && is%s_sublph12 ) ' %(reg[0], reg[1]), [0,5,10,15,25,40,70,200] )
   
        hist_data_egg_zcr = samplesWgg.get_samples(name='Data')[0].hist.Clone('pt_leadph12_egg_zcr%s'%(reg_tag))
        save_hist( '%s/%s/Data/hist.root' %(baseDir, plotDir), hist_data_egg_zcr )

        hist_sig_egg_zcr  = samplesWgg.get_samples(name='Wgg')[0].hist.Clone('pt_leadph12_egg_zcr%s'%(reg_tag))
        save_hist( '%s/%s/Wgg/hist.root' %(baseDir, plotDir), hist_sig_egg_zcr )

        hist_Zgg_egg_zcr     = samplesWgg.get_samples(name='Zgg')[0].hist.Clone('pt_leadph12_egg_zcr%s'%(reg_tag))
        hist_ZggFSR_egg_zcr  = samplesWgg.get_samples(name='ZgammagammaFSR')[0].hist.Clone('pt_leadph12_egg_zcr%s'%(reg_tag))

        add_syst_to_hist( hist_Zgg_egg_zcr, 0.15 )
        add_syst_to_hist( hist_ZggFSR_egg_zcr, 0.15 )

        #hist_Zgg_egg.Add(hist_ZggFSR_egg)
        save_hist( '%s/%s/ZggFSR/hist.root' %(baseDir, plotDir), hist_ZggFSR_egg_zcr )
        save_hist( '%s/%s/Zgg/hist.root' %(baseDir, plotDir), hist_Zgg_egg_zcr )

        hist_bkg_egg_zcr  = samplesWgg.get_samples(name='AllBkg')[0].hist.Clone('pt_leadph12_egg_zcr%s'%(reg_tag))
        save_hist( '%s/%s/MCBkg/hist.root' %(baseDir, plotDir), hist_bkg_egg_zcr )

    make_hist_from_pickle( samplesWgg, baseDir + '/jet_fake_results__mgg.pickle'            , '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag='mgg', regions=regions )
    make_hist_from_pickle( samplesWgg, baseDir + '/jet_fake_results__egg_allZRejCuts.pickle', '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag='egg', regions=regions )
    make_hist_from_pickle( samplesWgg, baseDir + '/electron_fake_results.pickle'            , '%s/%s/EleFake/hist.root' %(baseDir, plotDir), tag='egg', regions=regions, syst=baseDir + '/electron_fake_results_syst.pickle')

    make_hist_from_pickle( samplesWgg, baseDir + '/electron_fake_results__zcr.pickle'       , '%s/%s/EleFake/hist.root' %(baseDir, plotDir), tag='egg_zcr', regions=regions, syst=baseDir + '/electron_fake_results_syst.pickle')
    make_hist_from_pickle( samplesWgg, baseDir + '/jet_fake_results__egg_ZCR.pickle'        , '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag='egg_zcr', regions=regions )

def add_syst_to_hist( hist, syst ) :

    for bin in range( 1, hist.GetNbinsX() +1 ) :
        curr_err = hist.GetBinError( bin )
        curr_val = hist.GetBinContent( bin )
        new_err = math.sqrt( curr_err*curr_err + curr_val*syst*curr_val*syst )

        hist.SetBinError( bin, new_err )

def make_hist_from_pickle( sampMan, input_file, output_hist, tag, regions, syst=None ) :

    # get jet fake background estimate
    if not os.path.isfile( input_file) :
        print 'Could not find input file %s', input_file
        return

    ofile = open( input_file, 'r' )


    data = pickle.load(ofile)

    ofile.close()

    samp_list = sampMan.get_samples()
    sum_hist = None
    sum_data = {}
    for reg in regions :
        hist = None
        for s in samp_list :
            if s.hist is not None :
                hist = s.hist.Clone( 'pt_leadph12_%s_%s-%s' %(tag, reg[0], reg[1] ) )
                sum_hist = s.hist.Clone( 'pt_leadph12_%s' %(tag ) )
                break

        for ptbin in range( 1, hist.GetNbinsX()+1 ) :
            min = int(hist.GetXaxis().GetBinLowEdge(ptbin))
            max = int(hist.GetXaxis().GetBinUpEdge(ptbin))
            sum_data.setdefault(ptbin, ufloat(0, 0) )

            if max <= 15 :
                continue

            maxval = str(max)
            if max > 100 :
                maxval = 'max'

            databin = ( reg[0] ,reg[1], str( min), maxval )

            print databin

            print data
            print data['stat+syst']['sum'].keys()
            hist.SetBinContent( ptbin, data['stat+syst']['sum'][databin]['result'].n )
            hist.SetBinError( ptbin, data['stat+syst']['sum'][databin]['result'].s )

            sum_data[ptbin] = sum_data[ptbin] + data['stat+syst']['sum'][databin]['result']

        save_hist( output_hist, hist )

    for ptbin in range( 1, hist.GetNbinsX()+1 ) :
        sum_hist.SetBinContent( ptbin, sum_data[ptbin].n )
        sum_hist.SetBinError( ptbin, sum_data[ptbin].s )

    save_hist( output_hist, sum_hist )
    

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



def MakeEleBkgEstimate(base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, eta_bins, pt_bins, outputDir=None, el_selection='elfull', namePostfix='') :

    print '-----------------------------------'
    print 'START ELECTRON FAKE ESTMATE FOR %s' %el_selection
    print '-----------------------------------'

    el_acc = ['elfull', 'elzcr']
    if el_selection not in el_acc :
        print 'Input region not recognized, must be %s' %(','.join(el_acc) )
        return

    # Just use data samples
    samplesWggInvLead.deactivate_all_samples()
    samplesWggInvLead.activate_sample('Data')
    samplesWggInvSubl.deactivate_all_samples()
    samplesWggInvSubl.activate_sample('Data')

    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB')]

    # get fake factors from nominal fits
    results_nom = get_ele_fakefactors( base_dir_ele, file_bin_map, regions, eta_bins, el_selection )
    # get fake factors from systematic fits
    results_syst = get_ele_fakefactors( base_dir_ele, file_bin_map_syst, regions, eta_bins, el_selection )

    results_comb = {'stat' : { 'lead' : {}, 'subl' : {}}, 'syst' : { 'lead' : {}, 'subl' : {}} }
    for bin, res in results_nom['lead'].iteritems() :
        results_comb['stat']['lead'][bin] = res['pred']
        if res['pred'] == 0 :
            results_comb['syst']['lead'][bin] = ufloat( res['pred'].n, res['pred'].n)
        else :
            results_comb['syst']['lead'][bin] = ufloat( res['pred'].n, math.fabs( (res['pred'].n - results_syst['lead'][bin]['pred'].n))/res['pred'].n)

    for bin, res in results_nom['subl'].iteritems() :
        results_comb['stat']['subl'][bin] = res['pred']
        if res['pred'] == 0 :
            results_comb['syst']['subl'][bin] = ufloat( res['pred'].n, res['pred'].n)
        else :
            results_comb['syst']['subl'][bin] = ufloat( res['pred'].n, math.fabs( (res['pred'].n - results_syst['subl'][bin]['pred'].n))/res['pred'].n)

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

    print 'jet_files_lead'
    print jet_files_lead

    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')
    #subl_ptbins = [ ( '70', 'max', '15', '25' ), ( '70', 'max', '25', 'max' ) ]
    subl_ptbins = [  ]
    pred_lead = get_jet_fake_results( jet_files_lead, jet_files_lead_syst, regions, pt_bins_jetfile, jet_dir_key_map, base_dir_jet,  pt_bins_subl=subl_ptbins ) 
    pred_subl = get_jet_fake_results( jet_files_subl, jet_files_subl_syst, regions, pt_bins_jetfile, jet_dir_key_map, base_dir_jet,  pt_bins_subl=subl_ptbins ) 

    # get fake factors and binning from file
    rfile_coarse = ROOT.TFile.Open( '%s/ElectronFakeFitsRatioCoarseEta/results.root' %base_dir_ele )
    rhist_coarse = rfile_coarse.Get( 'ff') 

    jet_scaled = {'stat' : {}, 'syst' : {} }
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


            bin = (r1,r2,ptmin,ptmax)
            jet_scaled['stat'][bin] = {'rf' : {}, 'fr' : {}, 'ff' : {} }
            jet_scaled['syst'][bin] = {'rf' : {}, 'fr' : {}, 'ff' : {} }

             
            jet_scaled['stat'][ bin ]['rf']['pred_lead'] = pred_lead['stat']['rf'][bin]['result']
            jet_scaled['stat'][ bin ]['fr']['pred_lead'] = pred_lead['stat']['fr'][bin]['result']
            jet_scaled['stat'][ bin ]['ff']['pred_lead'] = pred_lead['stat']['ff'][bin]['result']

            jet_scaled['stat'][ bin ]['rf']['pred_subl'] = pred_subl['stat']['rf'][bin]['result']
            jet_scaled['stat'][ bin ]['fr']['pred_subl'] = pred_subl['stat']['fr'][bin]['result']
            jet_scaled['stat'][ bin ]['ff']['pred_subl'] = pred_subl['stat']['ff'][bin]['result']

            jet_scaled['syst'][ bin ]['rf']['pred_lead'] = pred_lead['syst']['rf'][bin]['result']
            jet_scaled['syst'][ bin ]['fr']['pred_lead'] = pred_lead['syst']['fr'][bin]['result']
            jet_scaled['syst'][ bin ]['ff']['pred_lead'] = pred_lead['syst']['ff'][bin]['result']

            jet_scaled['syst'][ bin ]['rf']['pred_subl'] = pred_subl['syst']['rf'][bin]['result']
            jet_scaled['syst'][ bin ]['fr']['pred_subl'] = pred_subl['syst']['fr'][bin]['result']
            jet_scaled['syst'][ bin ]['ff']['pred_subl'] = pred_subl['syst']['ff'][bin]['result']

            jet_scaled['stat'][ bin ]['rf']['ff_lead'] = ff_lead
            jet_scaled['stat'][ bin ]['fr']['ff_lead'] = ff_lead
            jet_scaled['stat'][ bin ]['ff']['ff_lead'] = ff_lead

            jet_scaled['stat'][ bin ]['rf']['ff_subl'] = ff_subl
            jet_scaled['stat'][ bin ]['fr']['ff_subl'] = ff_subl
            jet_scaled['stat'][ bin ]['ff']['ff_subl'] = ff_subl

            # no additional FF syst at this point
            jet_scaled['syst'][ bin ]['rf']['ff_lead'] = ff_lead
            jet_scaled['syst'][ bin ]['fr']['ff_lead'] = ff_lead
            jet_scaled['syst'][ bin ]['ff']['ff_lead'] = ff_lead

            jet_scaled['syst'][ bin ]['rf']['ff_subl'] = ff_subl
            jet_scaled['syst'][ bin ]['fr']['ff_subl'] = ff_subl
            jet_scaled['syst'][ bin ]['ff']['ff_subl'] = ff_subl

            jet_scaled['stat'][ bin ]['rf']['total'] = jet_scaled['stat'][ bin ]['rf']['pred_lead']*jet_scaled['stat'][ bin ]['rf']['ff_lead'] + jet_scaled['stat'][ bin ]['rf']['pred_subl']*jet_scaled['stat'][ bin ]['rf']['ff_subl']
            jet_scaled['stat'][ bin ]['fr']['total'] = jet_scaled['stat'][ bin ]['fr']['pred_lead']*jet_scaled['stat'][ bin ]['fr']['ff_lead'] + jet_scaled['stat'][ bin ]['fr']['pred_subl']*jet_scaled['stat'][ bin ]['fr']['ff_subl']
            jet_scaled['stat'][ bin ]['ff']['total'] = jet_scaled['stat'][ bin ]['ff']['pred_lead']*jet_scaled['stat'][ bin ]['ff']['ff_lead'] + jet_scaled['stat'][ bin ]['ff']['pred_subl']*jet_scaled['stat'][ bin ]['ff']['ff_subl']


            jet_scaled['syst'][ bin ]['rf']['total'] = jet_scaled['syst'][ bin ]['rf']['pred_lead']*jet_scaled['syst'][ bin ]['rf']['ff_lead'] + jet_scaled['syst'][ bin ]['rf']['pred_subl']*jet_scaled['syst'][ bin ]['rf']['ff_subl']
            jet_scaled['syst'][ bin ]['fr']['total'] = jet_scaled['syst'][ bin ]['fr']['pred_lead']*jet_scaled['syst'][ bin ]['fr']['ff_lead'] + jet_scaled['syst'][ bin ]['fr']['pred_subl']*jet_scaled['syst'][ bin ]['fr']['ff_subl']
            jet_scaled['syst'][ bin ]['ff']['total'] = jet_scaled['syst'][ bin ]['ff']['pred_lead']*jet_scaled['syst'][ bin ]['ff']['ff_lead'] + jet_scaled['syst'][ bin ]['ff']['pred_subl']*jet_scaled['syst'][ bin ]['ff']['ff_subl']


    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]
            print '%s-%s, pt %s-%s' %( r1, r2, ptmin, ptmax)

            bin = (r1,r2,ptmin,ptmax)
    
            print 'Pred rf = %s' %( jet_scaled['stat'][ bin ]['rf']['total'] )
            print 'Pred fr = %s' %( jet_scaled['stat'][ bin ]['fr']['total'] )
            print 'Pred ff = %s' %( jet_scaled['stat'][ bin ]['ff']['total'] )


    results_subtracted = {'stat' : {'sum' : {}}, 'elesyst' : {'sum' : {}}, 'jetsyst' : {'sum' : {}}, 'stat+syst' : {'sum' : {}}}
    for bin, info_stat_lead in results_comb['stat']['lead'].iteritems() :
        info_stat_subl = results_comb['stat']['subl'][bin]
        info_syst_lead = results_comb['syst']['lead'][bin]
        info_syst_subl = results_comb['syst']['subl'][bin]

        results_subtracted['stat']['sum'][bin] = {}
        results_subtracted['elesyst']['sum'][bin] = {}
        results_subtracted['jetsyst']['sum'][bin] = {}
        results_subtracted['stat+syst']['sum'][bin] = {}

        results_subtracted['stat+syst']['sum'][bin]['lead'] = info_stat_lead
        results_subtracted['stat+syst']['sum'][bin]['subl'] = info_stat_subl
        results_subtracted['stat+syst']['sum'][bin]['jet_rf'] = jet_scaled['stat'][bin]['rf']
        results_subtracted['stat+syst']['sum'][bin]['jet_fr'] = jet_scaled['stat'][bin]['fr']
        results_subtracted['stat+syst']['sum'][bin]['jet_ff'] = jet_scaled['stat'][bin]['ff']

        results_subtracted['stat']['sum'][bin]['result'] = info_stat_lead +info_stat_subl - ( jet_scaled['stat'][bin]['rf']['total'] + jet_scaled['stat'][bin]['fr']['total'] + jet_scaled['stat'][bin]['ff']['total'] )

        # for elesyst set jet uncertainties to zero
        results_subtracted['elesyst']['sum'][bin]['result'] = info_syst_lead +info_syst_subl - ufloat( (jet_scaled['stat'][bin]['rf']['total'] + jet_scaled['stat'][bin]['fr']['total'] + jet_scaled['stat'][bin]['ff']['total']).n, 0.0 )

        # for jetsyst set ele uncertainties to zero
        results_subtracted['jetsyst']['sum'][bin]['result'] = ufloat( (info_stat_lead +info_stat_subl).n, 0.0) - ( jet_scaled['syst'][bin]['rf']['total'] + jet_scaled['syst'][bin]['fr']['total'] + jet_scaled['syst'][bin]['ff']['total'] )

        # for comb, set ele and jet values to zero but keep their uncertainties
        elesyst_to_add = ufloat( 0, results_subtracted['elesyst']['sum'][bin]['result'].s )
        jetsyst_to_add = ufloat( 0, results_subtracted['jetsyst']['sum'][bin]['result'].s )
        results_subtracted['stat+syst']['sum'][bin]['result']    = results_subtracted['stat']['sum'][bin]['result'] + elesyst_to_add + jetsyst_to_add

        print 'Ele pred Final %s-%s pt %s-%s = %s' %( bin[0], bin[1], bin[2], bin[3], results_subtracted['stat+syst']['sum'][bin]['result'] )



    #results_syst_subtracted = {}
    #results_syst_subtracted['stat+syst'] = {}
    #results_syst_subtracted['stat+syst']['sum'] = {}
    #for (r1,r2, ptmin, ptmax), val in results_syst.iteritems() :

    #    results_syst_subtracted['stat+syst']['sum'][bin] = {}

    #    results_syst_subtracted['stat+syst']['sum'][bin]['lead'] = info_lead
    #    results_syst_subtracted['stat+syst']['sum'][bin]['subl'] = info_subl
    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_rf'] = jet_scaled[bin]['rf']
    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_fr'] = jet_scaled[bin]['fr']
    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_ff'] = jet_scaled[bin]['ff']
    #    results_syst_subtracted['stat+syst']['sum'][bin]['result'] = info_lead['pred'] +info_subl['pred'] - ( jet_scaled[bin]['rf']['total'] + jet_scaled[bin]['fr']['total'] + jet_scaled[bin]['ff']['total'] )

    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

        file_raw = open( outputDir + '/electron_fake_results%s__noJetFakeSubtraction.pickle' %namePostfix, 'w' )
        pickle.dump( results_nom, file_raw )
        file_raw.close()

        file_sub = open( outputDir + '/electron_fake_results%s.pickle' %namePostfix, 'w' )
        pickle.dump( results_subtracted, file_sub )
        file_sub.close()

        #file_sub_syst = open( outputDir + '/electron_fake_results_syst%s.pickle' %namePostfix, 'w' )
        #pickle.dump( results_syst_subtracted, file_sub_syst )
        #file_sub_syst.close()


def get_ele_fakefactors( base_dir_ele, file_bin_map, regions, eta_bins, el_selection ) :

    results = {}
    results['lead'] = {}
    results['subl'] = {}

    for file, lead_ptbins in file_bin_map.iteritems() :

        # get root file
        if not os.path.isfile( '%s/%s/results.root'%(base_dir_ele, file ) ) :
            print 'Fake factor file not found'
            return {}

        rfile = ROOT.TFile.Open( '%s/%s/results.root'%(base_dir_ele, file ) )
        rhist = rfile.Get('ff')

        nxbins = rhist.GetXaxis().GetNbins()
        nybins = rhist.GetYaxis().GetNbins()
        xmin = rhist.GetXaxis().GetBinLowEdge(1)
        xmax = rhist.GetXaxis().GetBinUpEdge(nxbins)
        ymin = rhist.GetYaxis().GetBinLowEdge(1)
        ymax = rhist.GetYaxis().GetBinUpEdge(nybins)

        data_samp_invlead = samplesWggInvLead.get_samples( name='Data' )[0]
        data_samp_invsubl = samplesWggInvSubl.get_samples( name='Data' )[0]
        # get data counts from inverted pixel seed 
        for r1, r2 in regions :
            #invert lead, draw lead
            #samplesWggInvLead.create_hist(data_samp_invlead, 'fabs(eta_leadph12):pt_leadph12', ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 )' %(el_cuts[el_selection]['invlead'], r1, r2), (nxbins, xmin, xmax, nybins, ymin, ymax) )

            #hist_lead = data_samp_invlead.hist.Clone('hist_lead__%s-%s' %(r1,r2))

            for ptmin, ptmax in lead_ptbins :

                if ptmax == 'max' :
                    draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %s)' %(el_cuts[el_selection]['invlead'], r1, r2, ptmin)
                else :
                    draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %s && pt_leadph12 < %s)' %(el_cuts[el_selection]['invlead'], r1, r2, ptmin, ptmax)
                samplesWggInvLead.create_hist(data_samp_invlead, 'fabs(eta_leadph12):pt_leadph12', draw_str, (nxbins, xmin, xmax, nybins, ymin, ymax) )

                hist_lead = data_samp_invlead.hist.Clone('hist_lead__%s-%s' %(r1,r2))

                bin = (r1, r2, ptmin, ptmax)
                results['lead'][bin] = {}
                results['lead'][bin]['pred'] = ufloat(0, 0)

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


                    dataerr = ROOT.Double()
                    nData = hist_lead.IntegralAndError( ptbinmin, ptbinmax, etabinmin, etabinmax, dataerr )
                    ff = rhist.GetBinContent( ptbinmin, etabinmin )
                    fferr = rhist.GetBinError( ptbinmin, etabinmin )

                    print 'LEAD : ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptminmax = %d, etabinmin = %d, etabinmax = %d data = %d, ff = %f, pred = %f ' %( ptmin, ptmax, etamin, etamax, ptbinmin, ptbinmax, etabinmin, etabinmax, nData, ff, nData*ff )

                    ff_bin = ( str(etamin), str(etamax), ptmin, ptmax )

                    results['lead'][bin][ff_bin] = {}
                    results['lead'][bin][ff_bin]['data'] = ufloat( nData, dataerr )
                    results['lead'][bin][ff_bin]['ff'] = ufloat( ff, fferr )
                    results['lead'][bin][ff_bin]['pred'] = results['lead'][bin][ff_bin]['data']*results['lead'][bin][ff_bin]['ff']

                    results['lead'][bin]['pred'] = results['lead'][bin]['pred'] + results['lead'][bin][ff_bin]['pred']

                if ptmax == 'max' :
                    draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %s)' %(el_cuts[el_selection]['invsubl'], r1, r2, ptmin)
                else :
                    draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %s && pt_leadph12 < %s)' %(el_cuts[el_selection]['invsubl'], r1, r2, ptmin, ptmax)
                samplesWggInvSubl.create_hist(data_samp_invsubl, 'fabs(eta_sublph12):pt_sublph12', draw_str,  (nxbins, xmin, xmax, nybins, ymin, ymax) )


                hist_subl = data_samp_invsubl.hist.Clone('hist_subl__%s-%s' %(r1,r2))

                bin = (r1, r2, ptmin, ptmax)
                results['subl'][bin] = {}
                results['subl'][bin]['pred'] = ufloat(0, 0)
                print 'SUBL Total : ', hist_subl.Integral()
                for eidx, etamin in enumerate( eta_bins[r2][:-1] ) :
                    etamax = eta_bins[r2][eidx+1]

                    sublptbinmin = hist_subl.GetXaxis().FindBin( 15 )
                    if ptmax == 'max' :
                        sublptbinmax = hist_subl.GetNbinsX()
                    else :
                        sublptbinmax = hist_subl.GetXaxis().FindBin( int(ptmax) )-1

                    etabinmin = hist_subl.GetYaxis().FindBin( etamin )
                    etabinmax = hist_subl.GetYaxis().FindBin( etamax )-1

                    for subl_hist_bin in range( 1, hist_subl.GetNbinsX() + 1 ) :

                        if subl_hist_bin >= sublptbinmin and subl_hist_bin <= sublptbinmax :
                            dataerr = ROOT.Double()
                            nData = hist_subl.IntegralAndError( subl_hist_bin, subl_hist_bin, etabinmin, etabinmax, dataerr )
                            ff = rhist.GetBinContent( sublptbinmin, etabinmin )
                            fferr = rhist.GetBinError( sublptbinmin, etabinmin )
                            print 'Sublead : ptmin = 15, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptminmax = %d, etabinmin = %d, etabinmax = %d hist_bin = %d, data = %d, ff= %f, pred = %f ' %(ptmax, etamin, etamax, sublptbinmin, sublptbinmax, etabinmin, etabinmax, subl_hist_bin, nData, ff, nData*ff )


                            ff_bin = ( str(etamin), str(etamax), str(hist_subl.GetXaxis().GetBinLowEdge(subl_hist_bin)), str(hist_subl.GetXaxis().GetBinUpEdge(subl_hist_bin)) )

                            results['subl'][bin][ff_bin] = {}
                            results['subl'][bin][ff_bin]['data'] = ufloat(nData, dataerr )
                            results['subl'][bin][ff_bin]['ff'] = ufloat( ff, fferr )
                            results['subl'][bin][ff_bin]['pred'] = results['subl'][bin][ff_bin]['data']*results['subl'][bin][ff_bin]['ff']

                            results['subl'][bin]['pred'] = results['subl'][bin]['pred'] +results['subl'][bin][ff_bin]['pred']

            hist_subl.Draw('colz')
            for bin, res in results['lead'].iteritems() :
                print 'LEAD bin : %s, info = %s' %( bin, res['pred'] )
            for bin, res in results['subl'].iteritems() :
                print 'SUBL bin : %s, info = %s' %( bin, res['pred'] )

        rfile.Close()

    return results


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
        val['rf'][reg_bin] = {}
        val['fr'][reg_bin] = {}
        val['ff'][reg_bin] = {}
        val['sum'][reg_bin] = {}

    for dir_key in sorted_jet_dirs :
        
        fentries = jet_files[dir_key]
        fentries_syst = jet_files_syst[dir_key]

        if reg_bin not in fentries :

            print 'Bin not found', reg_bin
            print fentries
            print jet_files
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

        results['stat']['rf'][reg_bin]['result'] = Npred_rf
        results['stat']['fr'][reg_bin]['result'] = Npred_fr
        results['stat']['ff'][reg_bin]['result'] = Npred_ff
        results['stat']['sum'][reg_bin]['result'] = Npred_ff+Npred_rf+Npred_fr

        syst_asym = _asym_iso_syst[(dir_key[0], dir_key[1], dir_key[2])]

        results['syst']['rf'][reg_bin]['result'] = Npred_rf_syst* ufloat( 1.0, syst_asym )
        results['syst']['fr'][reg_bin]['result'] = Npred_fr_syst* ufloat( 1.0, syst_asym )
        results['syst']['ff'][reg_bin]['result'] = Npred_ff_syst* ufloat( 1.0, syst_asym )
        results['syst']['sum'][reg_bin]['result'] = results['syst']['rf'][reg_bin]['result'] + results['syst']['fr'][reg_bin]['result'] + results['syst']['ff'][reg_bin]['result']

        Npred_rf_tot = Npred_rf
        Npred_fr_tot = Npred_fr
        Npred_ff_tot = Npred_ff

        Npred_rf_syst_zero =ufloat( 0, results['syst']['rf'][reg_bin]['result'].s )
        Npred_fr_syst_zero =ufloat( 0, results['syst']['fr'][reg_bin]['result'].s )
        Npred_ff_syst_zero =ufloat( 0, results['syst']['ff'][reg_bin]['result'].s )

        # do sum for stat+syst
        Npred_rf_tot += Npred_rf_syst_zero
        Npred_fr_tot += Npred_fr_syst_zero
        Npred_ff_tot += Npred_ff_syst_zero
        
        results['stat+syst']['rf'][reg_bin]['result'] = Npred_rf_tot
        results['stat+syst']['fr'][reg_bin]['result'] = Npred_fr_tot
        results['stat+syst']['ff'][reg_bin]['result'] = Npred_ff_tot
        results['stat+syst']['sum'][reg_bin]['result'] = results['stat+syst']['rf'][reg_bin]['result'] + results['stat+syst']['fr'][reg_bin]['result'] + results['stat+syst']['ff'][reg_bin]['result']

        break

    # if results weren't set in any cases above, 
    # get the results from the first entry
    if not results['stat']['rf'][reg_bin] or not results['stat']['fr'][reg_bin] or not results['stat']['ff'][reg_bin] :

        if reg_bin not in fentries :
            print 'Bin not found', reg_bin
            return

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

        syst_asym = _asym_iso_syst[(dir_key[0], dir_key[1], dir_key[2])]

        Npred_rf_syst = predictions_syst['Npred_RF_TT']
        Npred_fr_syst = predictions_syst['Npred_FR_TT']
        Npred_ff_syst = predictions_syst['Npred_FF_TT']

        results['stat']['rf'][reg_bin]['result'] = Npred_rf
        results['stat']['fr'][reg_bin]['result'] = Npred_fr
        results['stat']['ff'][reg_bin]['result'] = Npred_ff
        results['stat']['sum'][reg_bin]['result'] = Npred_ff+Npred_rf+Npred_fr

        results['syst']['rf'][reg_bin]['result'] = Npred_rf_syst* ufloat( 1.0, syst_asym )
        results['syst']['fr'][reg_bin]['result'] = Npred_fr_syst* ufloat( 1.0, syst_asym )
        results['syst']['ff'][reg_bin]['result'] = Npred_ff_syst* ufloat( 1.0, syst_asym )
        results['syst']['sum'][reg_bin]['result'] = results['syst']['rf'][reg_bin]['result'] + results['syst']['fr'][reg_bin]['result'] + results['syst']['ff'][reg_bin]['result']

        Npred_rf_tot = Npred_rf
        Npred_fr_tot = Npred_fr
        Npred_ff_tot = Npred_ff

        Npred_rf_syst_zero =ufloat( 0, results['syst']['rf'][reg_bin]['result'].s )
        Npred_fr_syst_zero =ufloat( 0, results['syst']['fr'][reg_bin]['result'].s )
        Npred_ff_syst_zero =ufloat( 0, results['syst']['ff'][reg_bin]['result'].s )

        Npred_rf_tot += Npred_rf_syst_zero
        Npred_fr_tot += Npred_fr_syst_zero
        Npred_ff_tot += Npred_ff_syst_zero
        
        results['stat+syst']['rf'][reg_bin]['result'] = Npred_rf_tot
        results['stat+syst']['fr'][reg_bin]['result'] = Npred_fr_tot
        results['stat+syst']['ff'][reg_bin]['result'] = Npred_ff_tot
        results['stat+syst']['sum'][reg_bin]['result'] = Npred_rf_tot+Npred_fr_tot+Npred_ff_tot

if __name__ == '__main__' :
    main()
