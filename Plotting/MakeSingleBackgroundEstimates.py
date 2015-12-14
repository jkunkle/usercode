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
from array import array
from uncertainties import ufloat
from FakeFactorManager import FakeFactorManager


p = ArgumentParser()

p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',  required=True,       help='Input directory base')
p.add_argument('--plotDir',     default='Plots',  type=str ,        dest='plotDir',  required=False,       help='Directory where plots are written')
p.add_argument('--ptbins',     default='15,25,40,70,200',  type=str ,        dest='ptbins',  required=False,       help='PT bins to use')
p.add_argument('--zcr',     default=False,  action='store_true', dest='zcr',   help='Make background estimate to Z control region')
p.add_argument('--wcr',     default=False,  action='store_true', dest='wcr',   help='Make background estimate to W control region')

options = p.parse_args()

import ROOT
from SampleManager import SampleManager
from MakeBackgroundEstimates import get_dirs_and_files, get_mapped_directory, save_hist, add_syst_to_hist
ROOT.gROOT.SetBatch(True)

samplesLLG = None
samplesLG = None

_ptbins = [int(x) for x in options.ptbins.split(',')]

lead_dr_cut = 0.4

el_cuts = {
           'muw'               : 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_trigmu_met > 40 ',
           'muwtight'          : 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_trigmu_met > 80 ',
           'muwlowmt'          : 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_trigmu_met < 40 ',
           'muwlowmet'         : 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && el_n==0 && pfType01MET < 30 ',
           'muwlowmettightmu'  : 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && el_n==0 && pfType01MET < 30 && fabs(mu_d0[0]) < 0.015 && (mu_corrIso[0]/mu_pt[0]) < 0.12  ',
           'muwhighmet'        : 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && el_n==0 && pfType01MET > 30 ',
           'muwlowmtnolepveto' : 'mu_passtrig25_n>0 && ph_mediumNoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && mt_trigmu_met < 40 ',
           'muwlowmttightmu'   : 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_trigmu_met < 40 && fabs(mu_d0[0]) < 0.015 && (mu_corrIso[0]/mu_pt[0]) < 0.12 && mu_pt[0] < 40 ',
           'muwlowmttightmuhighpt'   : 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_trigmu_met < 40 && fabs(mu_d0[0]) < 0.015 && (mu_corrIso[0]/mu_pt[0]) < 0.12 && mu_pt[0] > 80 ',
           'singleelwzcr'      : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumFailPSV_n==1 && ph_hasPixSeed[0]==1 && m_trigelph1 > 76 && m_trigelph1 < 106 ' ,
           'singleelwzcrloose' : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumFailPSV_n==1 && ph_hasPixSeed[0]==1 && m_trigelph1 > 50 && m_trigelph1 < 106 ',
           'singleelw'         : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumFailPSV_n==1 && ph_hasPixSeed[0]==1 && mt_trigel_met > 60  ',
           'singleelwsr'       : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumFailPSV_n==1 && ph_hasPixSeed[0]==1 && mt_trigel_met > 40 && !( m_trigelph1 > 76 && m_trigelph1 < 106 ) ',
           'singleelwsrtight'  : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumFailEleVeto_n==1 && ph_hasPixSeed[0]==1 && mt_trigel_met > 80 && !( m_trigelph1 > 76 && m_trigelph1 < 106 ) ',
           'singleelwsrlowmt'  : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumFailEleVeto_n==1 && ph_hasPixSeed[0]==1 && mt_trigel_met < 40 && !( m_trigelph1 > 76 && m_trigelph1 < 106 ) ',
           'elw'               : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumPassPSV_n==1 && mu_n==0 && mt_trigel_met > 60  ',
           'elwsr'             : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumPassPSV_n==1 && mt_trigel_met > 40 && !( m_trigelph1 > 76 && m_trigelph1 < 106 ) ',
           'elwsrtight'        : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumPassPSV_n==1 && mt_trigel_met > 80 && !( m_trigelph1 > 76 && m_trigelph1 < 106 ) ',
           'elwsrlowmt'        : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumPassPSV_n==1 && mt_trigel_met < 40 && !( m_trigelph1 > 76 && m_trigelph1 < 106 ) ',
           'elwzcr'            : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumPassPSV_n==1 && ph_hasPixSeed[0]==0 && m_trigelph1 > 76 && m_trigelph1 < 106 ',
           'elwzcrloose'       : 'el_passtrig_n>0 && el_n==1  && mu_n==0 && ph_mediumPassPSV_n==1 && ph_hasPixSeed[0]==0 && m_trigelph1 > 50 && m_trigelph1 < 106 ',

           'elz'                : 'el_passtrig_n>0 && el_n==2 && ph_mediumNoEleVeto_n==1 && leadPhot_leadLepDR>%.1f && leadPhot_sublLepDR>%.1f && m_leplep>60 && m_leplepph > 105' %( lead_dr_cut, lead_dr_cut ) ,
           'muz'                : 'mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoEleVeto_n==1 && leadPhot_leadLepDR>%.1f  && leadPhot_sublLepDR>%.1f && m_leplep>60 && m_leplepph > 105' %( lead_dr_cut, lead_dr_cut ) ,
           'elrealcr'          : 'el_passtrig_n>0   && el_n==2 && ph_mediumPassPSV_n==1 && leadPhot_leadLepDR>%.1f && leadPhot_sublLepDR>%.1f && m_leplep>60 && m_leplepph >81 && m_leplepph < 101' %( lead_dr_cut, lead_dr_cut ) ,
           'murealcr'          : 'mu_passtrig25_n>0 && mu_n==2 && ph_mediumPassPSV_n==1 && leadPhot_leadLepDR>%.1f  && leadPhot_sublLepDR>%.1f && el_n==0 && m_leplep>60 && m_leplepph >81 && m_leplepph < 101' %( lead_dr_cut, lead_dr_cut ) ,
}

def main() :


    global samplesLLG
    global samplesLG

    baseDirLLG  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_11_09'
    baseDirLG   = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09'
    #baseDirLG   = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22'
    #baseDirLG   = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaJJNoPhID_2015_05_05'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfLLG = 'Modules/WgamgamForBkg.py'

    samplesLLG  = SampleManager(baseDirLLG,  treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesLG   = SampleManager(baseDirLG ,  treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesLLG .ReadSamples( sampleConfLLG )
    samplesLG  .ReadSamples( sampleConfLLG )

    if options.wcr :

        #suffix = 'TAndP'
        suffix = ''
        path_manual   = 'ElectronFakeManual' 
        path_manualL  = 'ElectronFakeManualLoose' 
        path_nom      = 'ElectronFakeFitsRatio%s' %suffix 
        path_mctempnd = 'ElectronFakeFitsRatio%sMCTemplateNDKeys' %suffix
        #path_mctempnd = 'ElectronFakeFitsRatioTruthMatchMCTemplateNDKeys'
        path_mctemp   = 'ElectronFakeFitsRatio%sMCTemplate' %suffix
        path_subtract = 'ElectronFakeFitsRatioMCTemplateNDKeysSubtractZgamma'

        file_bin_map = {}
        file_bin_map_syst = {}

        # -----------------
        # Set the path here so it is picked up for jet background
        # -----------------
        #path_used = path_mctempnd
        #path_used = path_manual
        #path_used = path_subtract
        path_used = path_nom

        # go up to the second-to-last bin
        for bidx in range( 0, len( _ptbins ) - 2 ) :
            #file_bin_map.setdefault(path_subtract, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            #file_bin_map_syst.setdefault(path_subtract, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            #file_bin_map.setdefault(path_mctempnd, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            #file_bin_map_syst.setdefault(path_mctempnd, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            file_bin_map.setdefault(path_nom, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            file_bin_map_syst.setdefault(path_nom, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            #file_bin_map.setdefault(path_mctemp, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            #file_bin_map_syst.setdefault(path_mctemp, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            #file_bin_map.setdefault(path_manual, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            #file_bin_map_syst.setdefault(path_manual, []).append((_ptbins[bidx], _ptbins[bidx+1]))

        # do the last bin
        file_bin_map[path_nom].append((_ptbins[-2], 'max') )
        file_bin_map_syst[path_nom].append((_ptbins[-2], 'max') )
        #file_bin_map[path_mctemp].append((_ptbins[-2], 'max') )
        #file_bin_map_syst[path_mctemp].append((_ptbins[-2], 'max') )
        #file_bin_map[path_manual].append((_ptbins[-2], 'max'))
        #file_bin_map_syst[path_manual].append((_ptbins[-2], 'max'))
        #file_bin_map[path_mctempnd].append ((_ptbins[-2], 'max'))
        #file_bin_map_syst[path_mctempnd].append((_ptbins[-2], 'max'))
        #file_bin_map[path_subtract].append ((_ptbins[-2], 'max'))
        #file_bin_map_syst[path_subtract].append((_ptbins[-2], 'max'))

        #eta_bins = {'EB' : [(0.00, 0.10), (0.10, 0.50), (0.50, 1.00), (1.00, 1.44)],
        #            'EE' : [(1.57, 2.10), (2.10, 2.20), (2.20, 2.40), (2.40, 2.50)]}

        #eta_bins_plot = eta_bins

        eta_bins = {'EB' : [(0.00, 1.44)], 'EE' : [(1.57, 2.50)]}
        eta_bins_plot = {'EB' : [], 'EE' : []}

        for typedir in os.listdir( '%s/SinglePhotonResults'%options.baseDir ) :
            if typedir != 'ChHadIsoFits' :
                continue
            base_dir_ele_single = options.baseDir
            base_dir_jet_single = '%s/SinglePhotonResults/%s' %(options.baseDir, typedir)
            outputDirSingle='%s/SinglePhotonWCRBackgroundEstimates/%s' %(options.baseDir, typedir)

            channels = []
            channelsel = []

            #channelsel = ['elw', 'elwsr', 'elwsrtight', 'elwzcr' ]
            #channelsel = ['elwzcr' ]
            for elch in channelsel :
                channels.append( elch )
                channels.append( elch+'invpixlead' )

            #channelsmu = ['muwlowmtnolepveto']
            channelsmu = ['muw', 'muwtight']
            channels += channelsmu
            

            MakeSingleJetBkgEstimate( base_dir_jet_single, channels=channels,eta_bins=eta_bins, outputDir=outputDirSingle )

            for ch in channelsel :
                MakeSingleEleBkgEstimate( base_dir_ele_single, base_dir_jet_single, file_bin_map, file_bin_map_syst,eta_bins=eta_bins, elffdir=path_used, el_selection=ch, outputDir=outputDirSingle )

            #MakeSingleJetBkgEstimate( base_dir_jet_single, channels=['muw'],outputDir=outputDirSingle )


            MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=channelsmu+channelsel,eta_bins=eta_bins_plot )

            #MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=['elwzcr'],eta_bins=eta_bins_plot )
            #MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=['elwzcrloose'],eta_bins=eta_bins_plot )
            #MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=['muw'] )

    if options.zcr :

        for typedir in os.listdir( '%s/SinglePhotonResults'%options.baseDir ) :

            base_dir_jet_single = '%s/SinglePhotonResults/%s' %(options.baseDir, typedir )
            outputDirSingle='%s/SinglePhotonZCRBackgroundEstimates/%s' %(options.baseDir, typedir)

            eta_bins = {'EB' : [(0.00, 1.44)], 'EE' : [(1.57, 2.50)]}
            eta_bins_plot = {'EB' : [], 'EE' : []}
            MakeSingleJetBkgEstimate( base_dir_jet_single, channels=['muz', 'elz'], eta_bins=eta_bins, outputDir=outputDirSingle )
            MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=['muz', 'elz'], eta_bins=eta_bins_plot, makeEleFake=False )
            #MakeSingleJetBkgEstimate( base_dir_jet_single, channels=['mu'], outputDir=outputDirSingle )
            #MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=['mu'], makeEleFake=False )

    print '^_^ FINSISHED ^_^'
    print 'It is safe to kill the program if it is hanging'

def MakeSingleEleBkgEstimate(base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, eta_bins, elffdir, el_selection='elw', outputDir=None) :

    el_acc = ['elw', 'elwzcr', 'elwzcrloose', 'elwsr', 'elwsrlowmt']
    if el_selection not in el_acc :
        print 'Input region not recognized, must be %s' %(','.join(el_acc) )
        return

    samplesLLG.deactivate_all_samples()
    samplesLLG.activate_sample('Data')

    regions = ['EB','EE']

    results_nom = get_ele_single_fakefactors( base_dir_ele, file_bin_map, regions, eta_bins, el_selection )
    # prevent killing from drawing too many plots
    #results_syst = get_ele_single_fakefactors( base_dir_ele, file_bin_map_syst, regions, eta_bins, el_selection )

    file_key_lead_eta = 'results__%sinvpixlead__(\d\.\d\d-\d\.\d\d)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_lead_syst_eta = 'results__syst__%sinvpixlead__(\d\.\d\d-\d\.\d\d)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_lead = 'results__%sinvpixlead__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_lead_syst = 'results__syst__%sinvpixlead__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    #jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'
    jet_dirs_key = 'JetSinglePhotonFakeNomIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    jet_files_lead_eta      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead_eta      )
    jet_files_lead_syst_eta = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead_syst_eta )
    jet_files_lead      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead      )
    jet_files_lead_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead_syst )

    update_jet_files_dict( jet_files_lead, jet_files_lead_eta )
    update_jet_files_dict( jet_files_lead_syst, jet_files_lead_syst_eta )

    print 'jet_files_lead'
    print jet_files_lead

    pt_bins_jetfile = [str(x) for x in _ptbins[:-1]]
    pt_bins_jetfile.append( 'max')
    pred_lead = get_jet_single_fake_results( jet_files_lead, jet_files_lead_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet, eta_bins=eta_bins) 

    # get fake factors and binning from file
    ff_man_coarse = FakeFactorManager( '%s/%s/results.pickle' %(base_dir_ele, elffdir), ['fake_ratio'] )
    #ff_man_coarse = FakeFactorManager( '%s/ElectronFakeFitsRatio/results.pickle' %base_dir_ele, ['fake_ratio'] )
    #ff_man_coarse = FakeFactorManager( '%s/ElectronFakeFitsRatioTAndPMCTemplate/results.pickle' %base_dir_ele, ['fake_ratio'] )
    #ff_man_coarse = FakeFactorManager( '%s/ElectronFakeManualWithOlap2/results.pickle' %base_dir_ele, ['fake_ratio'] )

    # determine number of eta bins used
    # if only one eta bin is requested
    # per region, some different behavior occurrs

    eta_lens = []
    for reg in regions :
        eta_lens.append( len(eta_bins[reg] ) )

    eta_lens = list(set(eta_lens))

    single_eta_bin = False
    if len(eta_lens) == 1 and eta_lens[0]==1 :
        single_eta_bin = True


    scaled_f = {}
    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]

            if r1 == 'EB' :
                ff_lead = ff_man_coarse.get_pt_eta_ff( ptmin, ptmax, 0.0, 1.44 )
            if r1 == 'EE' :
                ff_lead = ff_man_coarse.get_pt_eta_ff( ptmin, ptmax, 1.57, 2.5 )

            scaled_f[ (r1,ptmin,ptmax) ] = pred_lead['stat+syst']['f'][( r1,ptmin,ptmax)]*ff_lead

            
            if not single_eta_bin :
                for etamin, etamax in eta_bins[r1] :
                    ff_lead = ff_man_coarse.get_pt_eta_ff( ptmin, ptmax, etamin, etamax)
                    etabin = '%.2f-%.2f' %( etamin, etamax) 
                    scaled_f [(etabin, ptmin, ptmax) ] =pred_lead['stat+syst']['f'][( etabin,ptmin,ptmax)]*ff_lead


    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]
            print '%s, pt %s-%s' %( r1, ptmin, ptmax)
    
            print 'Pred f = %s, scaled f = %s' %( pred_lead['stat+syst']['f'][(r1,ptmin,ptmax)], scaled_f[(r1,ptmin,ptmax)] )

            if not single_eta_bin :
            #if eta_bins :
                for etamin, etamax in eta_bins[r1] :
                    etabin = '%.2f-%.2f' %( etamin, etamax) 
                    print '%s, pt %s-%s' %( etabin, ptmin, ptmax)
    
                    print 'Pred f = %s, scaled f = %s' %( pred_lead['stat+syst']['f'][(etabin,ptmin,ptmax)], scaled_f[(etabin,ptmin,ptmax)] )

    results_subtracted = {}
    results_subtracted['stat+syst'] = {}
    results_subtracted['stat+syst']['result'] = {}


    for reg_bin, val in results_nom['stat+syst']['result'].iteritems() :
        r1 = reg_bin[0]
        ptmin = reg_bin[1]
        ptmax = reg_bin[2]
        if reg_bin not in scaled_f :
            continue
        print 'Reg = %s, pt %s-%s, N Pix CR* ff = %s, N Jet Pix CR * ff = %s, pred = %s' %( r1, ptmin, ptmax, val, scaled_f[reg_bin], val- scaled_f[reg_bin] )
        results_subtracted['stat+syst']['result'][reg_bin] = val-scaled_f[ reg_bin ] 
    if not single_eta_bin :
        for r1 in regions :
            for etamin, etamax in eta_bins[r1] :
                etabin = '%.2f-%.2f' %( etamin, etamax) 
                print 'Reg = %s, pt %s-%s, N Pix CR* ff = %s, N Jet Pix CR * ff = %s, pred = %s' %( etabin, ptmin, ptmax, val, scaled_f[(etabin, ptmin, ptmax)], val- scaled_f[(etabin, ptmin, ptmax)] )
                results_subtracted['stat+syst']['result'][(etabin, ptmin, ptmax)] = val-scaled_f[ (etabin,ptmin,ptmax) ] 


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

        file_raw = open( outputDir + '/electron_fake_results%s__noJetFakeSubtraction.pickle' %el_selection, 'w' )
        pickle.dump( results_nom, file_raw )
        file_raw.close()

        file_sub = open( outputDir + '/electron_fake_results%s.pickle' %el_selection, 'w' )
        pickle.dump( results_subtracted, file_sub )
        file_sub.close()

        #file_sub_syst = open( outputDir + '/electron_fake_results_syst%s.pickle' %el_selection , 'w' )
        #pickle.dump( results_syst_subtracted, file_sub_syst )
        #file_sub_syst.close()

def MakeSingleJetBkgEstimate( base_dir_jet, channels=[], eta_bins={}, outputDir=None ) :

    if not isinstance(channels, list ) :
        channels = [channels]

    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

    regions = ['EB', 'EE']

    # get the pt bins in the format expected
    # in the pickle files
    pt_bins_jetfile = [str(x) for x in _ptbins[:-1]]
    pt_bins_jetfile.append( 'max')

    # regex expression to match directories
    # where jet fake results should be found
    # if the Corr directories are used 
    # it will prioritize to the minimum values
    jet_dirs_key = 'JetSinglePhotonFakeNomIso'
    #jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'

    # get the directories mapped to the integer values matched
    # if no values are matched the directory is matched ot (0,0,0)
    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    for channel in channels :
        file_key_eta = 'results__%s__(\d\.\d\d-\d\.\d\d)__pt_(\d+)-(\d+|max).pickle' %channel
        file_key_eta_syst = 'results__syst__%s__(\d\.\d\d-\d\.\d\d)__pt_(\d+)-(\d+|max).pickle' %channel
        file_key = 'results__%s__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %channel
        file_key_syst = 'results__syst__%s__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %channel

        jet_files_eta      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_eta      )
        jet_files_eta_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_eta_syst )
        jet_files      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key      )
        jet_files_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_syst )

        update_jet_files_dict( jet_files, jet_files_eta )
        update_jet_files_dict( jet_files_syst, jet_files_eta_syst )

        jet_pred     = get_jet_single_fake_results( jet_files    , jet_files_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet, eta_bins=eta_bins) 

        print 'Predicted Jet fakes for channel %s' %channel

        for r1 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                single_eta_bin = False
                if not eta_bins :
                    single_eta_bin = True
                if len( eta_bins[r1] ) == 1 :
                    single_eta_bin = True

                if not single_eta_bin :
                    for etamin, etamax in eta_bins[r1] :

                        bin = ('%.2f-%.2f'%(etamin,etamax), ptmin, ptmax)

                        print 'Region %s, pt %s-%s' %( bin[0],ptmin,ptmax)
                        print 'Predicted Stat r = %s, predicted f = %s' %( jet_pred['stat']['r'][bin], jet_pred['stat']['f'][bin] ) 
                        print 'Predicted Syst r = %s, predicted f = %s' %( jet_pred['syst']['r'][bin], jet_pred['syst']['f'][bin] )
                        print 'Predicted Stat+Syst r = %s, predicted f = %s' %( jet_pred['stat+syst']['r'][bin], jet_pred['stat+syst']['f'][bin] )
                else :
                    bin = (r1,ptmin,ptmax)

                    print 'Region %s, pt %s-%s' %( r1,ptmin,ptmax)
                    print 'Predicted Stat r = %s, predicted f = %s' %( jet_pred['stat']['r'][bin], jet_pred['stat']['f'][bin] ) 
                    print 'Predicted Syst r = %s, predicted f = %s' %( jet_pred['syst']['r'][bin], jet_pred['syst']['f'][bin] )
                    print 'Predicted Stat+Syst r = %s, predicted f = %s' %( jet_pred['stat+syst']['r'][bin], jet_pred['stat+syst']['f'][bin] )


        file = open( outputDir + '/jet_fake_results__%s.pickle' %channel, 'w' )
        pickle.dump( jet_pred, file )
        file.close()


    #file_key_mu = 'results__mu__(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    #file_key_elfull = 'results__el__(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    #file_key_elzcr  = 'results__elzcr__(EB|EE)__pt_(\d+)-(\d+|max).pickle'

    ## jet fake results with systematic
    ## uncertainties propagated
    #file_key_mu_syst     = 'results__syst__mu__(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    #file_key_elfull_syst = 'results__syst__el__(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    #file_key_el_syst     = 'results__syst__elzcr__(EB|EE)__pt_(\d+)-(\d+|max).pickle'


    #jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    #jet_files_mu     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu     )
    #jet_files_elfull = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull )
    #jet_files_elzcr  = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elzcr  )

    #jet_files_mu_syst     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu_syst     )
    #jet_files_elfull_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull_syst )
    #jet_files_el_syst     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_el_syst     )



    #pred_mu     = get_jet_single_fake_results( jet_files_mu    , jet_files_mu_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 
    #pred_elfull = get_jet_single_fake_results( jet_files_elfull, jet_files_elfull_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 
    #pred_elzcr  = get_jet_single_fake_results( jet_files_elzcr , jet_files_el_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

    #print 'muons'
    #for r1 in regions :

    #    for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
    #        ptmax = pt_bins_jetfile[idx+1]

    #        bin = (r1,ptmin,ptmax)

    #        print 'Region %s, pt %s-%s' %( r1,ptmin,ptmax)
    #        print 'Predicted Stat r = %s, predicted f = %s' %( pred_mu['stat']['r'][bin], pred_mu['stat']['f'][bin] ) 
    #        print 'Predicted Syst r = %s, predicted f = %s' %( pred_mu['syst']['r'][bin], pred_mu['syst']['f'][bin] )
    #        print 'Predicted Stat+Syst r = %s, predicted f = %s' %( pred_mu['stat+syst']['r'][bin], pred_mu['stat+syst']['f'][bin] )

    #print 'Electrons Z CR'
    #for r1 in regions :

    #    for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
    #        ptmax = pt_bins_jetfile[idx+1]

    #        bin = (r1,ptmin,ptmax)

    #        print 'Region %s, pt %s-%s' %( r1,ptmin,ptmax)

    #        print 'Predicted Stat r = %s, predicted f = %s' %( pred_elzcr['stat']['r'][bin], pred_elzcr['stat']['f'][bin] )
    #        print 'Predicted Syst r = %s, predicted f = %s' %( pred_elzcr['syst']['r'][bin], pred_elzcr['syst']['f'][bin] )
    #        print 'Predicted Stat+Syst r = %s, predicted f = %s' %( pred_elzcr['stat+syst']['r'][bin], pred_elzcr['stat+syst']['f'][bin])

    #print 'Electrons'
    #for r1 in regions :

    #    for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
    #        ptmax = pt_bins_jetfile[idx+1]

    #        bin = (r1,ptmin,ptmax)

    #        print 'Region %s, pt %s-%s' %( r1,ptmin,ptmax)
    #        print 'Predicted Stat r = %s, predicted f = %s' %( pred_elfull['stat']['r'][bin], pred_elfull['stat']['f'][bin] )
    #        print 'Predicted Syst r = %s, predicted f = %s' %( pred_elfull['syst']['r'][bin], pred_elfull['syst']['f'][bin] )
    #        print 'Predicted Stat+Syst r = %s, predicted f = %s' %( pred_elfull['stat+syst']['r'][bin], pred_elfull['stat+syst']['f'][bin] )


    #if outputDir is not None :
    #    if not os.path.isdir( outputDir ) :
    #        os.makedirs( outputDir )

    #file_muon = open( outputDir + '/jet_fake_results__mg.pickle', 'w' )
    #pickle.dump( pred_mu, file_muon )
    #file_muon.close()

    #file_elfull = open( outputDir + '/jet_fake_results__eg.pickle', 'w' )
    #pickle.dump( pred_elfull, file_elfull )
    #file_elfull.close()

    #file_elzcr = open( outputDir + '/jet_fake_results__eg_zcr.pickle', 'w' )
    #pickle.dump( pred_elzcr, file_elzcr)
    #file_elzcr.close()

def get_ele_single_fakefactors( base_dir_ele, file_bin_map, regions, eta_bins, el_selection ) :

    results_lead = { 'stat+syst' : {'result' : {} } }
    for file, ptbins in file_bin_map.iteritems() :

        # get root file
        print 'Get fake factors from ', '%s/%s/results.pickle' %(base_dir_ele, file)
        ff_man = FakeFactorManager( '%s/%s/results.pickle' %(base_dir_ele, file), ['fake_ratio'] )

        data_samp = samplesLG.get_samples( name='Electron' )[0]
        # get data counts from inverted pixel seed 
        for r1 in regions :
            #invert lead, draw lead
            samplesLG.create_hist(data_samp, 'fabs(ph_eta[0]):ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[0] )' %(el_cuts['single'+el_selection], r1, ), (20, 0, 100, 250, 0, 2.5) )

            hist_lead = data_samp.hist.Clone('hist_lead__%s' %(r1))

            for ptmin, ptmax in ptbins :
                results_lead['stat+syst']['result'][(r1, str(ptmin), str(ptmax))] = 0
                for etamin, etamax in eta_bins[r1] :

                    etabin = '%.2f-%.2f' %(etamin, etamax)

                    results_lead['stat+syst']['result'][(etabin, str(ptmin), str(ptmax))] = 0

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

                    ff = ff_man.get_pt_eta_ff( ptmin, ptmax, etamin, etamax )
                    
                    print 'etamin = %.2f, etamax = %.2f, ptmin = %s, ptmax = %s, nData = %d, ff = %s' %( etamin, etamax, ptmin, ptmax, nData, ff )

                    #print 'ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptbinmax = %d, etabinmin = %d, etabinmax = %d' %( ptmin, ptmax, etamin, etamax, ptbinmin, ptbinmax, etabinmin, etabinmax )
                    #print 'GetBinContent in %f < pt < %f, %f < eta < %f ' %( rhist.GetXaxis().GetBinLowEdge(ptbinmin), rhist.GetXaxis().GetBinUpEdge(ptbinmax), rhist.GetYaxis().GetBinLowEdge(etabinmin), rhist.GetYaxis().GetBinUpEdge(etabinmin) )

                    results_lead['stat+syst']['result'][(etabin, str(ptmin), str(ptmax))]  = nData*ff
                    results_lead['stat+syst']['result'][(r1, str(ptmin), str(ptmax))]  = results_lead['stat+syst']['result'][(r1, str(ptmin), str(ptmax))] + nData*ff

    return results_lead

def get_jet_single_fake_results( jet_files, jet_files_syst, regions, pt_bins, jet_dir_key_map, base_dir_jet, eta_bins={} ) :
    """ Get the fake results for all pt and eta regions 
    
        Check if the data counts that were input to the 
        fit are non-zero.  If so, move to a looser isolation.
        If the values are never set, ie even in the loosest
        case there are no data counts, then use the 
        original with zero values
    """
    sorted_jet_dirs = jet_files.keys()
    sorted_jet_dirs.sort()

    results = {'stat' : {}, 'syst' : {}, 'stat+syst' : {} }
    for val in results.values() :
       val['f'] = {}
       val['r'] = {}
       val['result'] = {}

    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins[:-1]) :
            ptmax = pt_bins[idx+1]

            single_eta_bin = False
            if not eta_bins :
                single_eta_bin = True
            if len( eta_bins[r1] ) == 1 :
                single_eta_bin = True

            if not single_eta_bin :
                for etamin, etamax in eta_bins[r1] :
                    reg_bin = ('%.2f-%.2f' %(etamin,etamax), ptmin, ptmax)

                    get_jet_fake_results_from_file( results, reg_bin, base_dir_jet, sorted_jet_dirs, jet_dir_key_map, jet_files, jet_files_syst, region='%s_%s-%s' %(reg_bin[0], ptmin, ptmax))
                reg_bin = (r1, ptmin, ptmax) 

                get_jet_fake_results_from_file( results, reg_bin, base_dir_jet, sorted_jet_dirs, jet_dir_key_map, jet_files, jet_files_syst, region='%s_%s-%s' %(r1, ptmin, ptmax))
            else :

                reg_bin = (r1, ptmin, ptmax) 

                get_jet_fake_results_from_file( results, reg_bin, base_dir_jet, sorted_jet_dirs, jet_dir_key_map, jet_files, jet_files_syst, region='%s_%s-%s' %(r1, ptmin, ptmax))

    return results

def get_jet_fake_results_from_file( results, reg_bin, base_dir_jet, sorted_jet_dirs, jet_dir_key_map, jet_files, jet_files_syst, region='' ) :

    for val in results.values() :
        val['r'][reg_bin] = None
        val['f'][reg_bin] = None
        val['result'][reg_bin] = None

    for dir_key in sorted_jet_dirs :
        
        fentries = jet_files[dir_key]
        fentries_syst = jet_files_syst[dir_key]

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
            print 'No data entries for AsymIso %d-%d-%d, region %s ' %( dir_key[0], dir_key[1], dir_key[2], region  )
            print 'Ndata_t = %s, Ndata_l = %s' %( Ndata_t, Ndata_l)
            continue

        Npred_f = predictions['Npred_F_T']
        Npred_r = predictions['Npred_R_T']

        Npred_r_syst = predictions_syst['Npred_R_T']
        Npred_f_syst = predictions_syst['Npred_F_T']

        results['stat']['r'][reg_bin] = Npred_r
        results['stat']['f'][reg_bin] = Npred_f
        results['stat']['result'][reg_bin] = Npred_f

        results['syst']['r'][reg_bin] = Npred_r_syst
        results['syst']['f'][reg_bin] = Npred_f_syst
        results['syst']['result'][reg_bin] = Npred_f_syst

        Npred_r_tot = Npred_r
        Npred_f_tot = Npred_f

        Npred_r_syst_zero =ufloat( 0, Npred_r_syst.s )
        Npred_f_syst_zero =ufloat( 0, Npred_f_syst.s )
        results['stat+syst']['r'][reg_bin] = Npred_r_tot
        results['stat+syst']['f'][reg_bin] = Npred_f_tot
        results['stat+syst']['result'][reg_bin] = Npred_f_tot

        break

    # if results weren't set in any cases above, 
    # get the results from the first entry
    if results['stat']['r'][reg_bin] is None or results['stat']['f'][reg_bin] is None :

        dir_key = sorted_jet_dirs[0]

        fentries = jet_files[dir_key]

        sub_dir_jet = jet_dir_key_map[dir_key]

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
        results['stat']['result'][reg_bin] = Npred_f

        results['syst']['r'][reg_bin] = Npred_r_syst
        results['syst']['f'][reg_bin] = Npred_f_syst
        results['syst']['result'][reg_bin] = Npred_f_syst

        Npred_r_tot = Npred_r
        Npred_f_tot = Npred_f

        Npred_r_syst_zero =ufloat( 0, Npred_r_syst.s )
        Npred_f_syst_zero =ufloat( 0, Npred_f_syst.s )

        Npred_r_tot += Npred_r_syst_zero
        Npred_f_tot += Npred_f_syst_zero
        
        results['stat+syst']['r'][reg_bin] = Npred_r_tot
        results['stat+syst']['f'][reg_bin] = Npred_f_tot
        results['stat+syst']['result'][reg_bin] = Npred_f_tot

def MakeSingleBkgEstimatePlots( baseDir, plotDir, channels=[], eta_bins={}, makeEleFake=True ) :

    # first make the nominal estimates

    regions = ['EB','EE']


    for ch in channels :
        data_sample = None
        if ch.count('mu') :
            data_sample = 'Muon'
        if ch.count('el') :
            data_sample = 'Electron'
    
        samplesLG.deactivate_all_samples()
        samplesLG.activate_sample( 'Wgamma' )
        samplesLG.activate_sample( 'Zgamma' )
        samplesLG.activate_sample( 'DYJetsToLLPhOlap' )
        samplesLG.activate_sample( data_sample )

        for reg in regions :

            var = 'ph_pt[0]'
            selection = ' PUWeight * ( %s && ph_Is%s[0]  ) ' %(el_cuts[ch], reg)
            hist_name = 'pt_leadph12_%s_%s'%(ch,reg)

            draw_singleph_hists( var, selection, _ptbins, data_sample, baseDir, plotDir, hist_name )

            if eta_bins :
                for etamin, etamax in eta_bins[reg] :
                    
                    selection = ' PUWeight * ( %s && ph_Is%s[0] && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f  ) ' %(el_cuts[ch], reg, etamin, etamax)
                    hist_name = 'pt_leadph12_%s_%.2f-%.2f'%(ch,etamin, etamax)

                    draw_singleph_hists( var, selection, _ptbins, data_sample, baseDir, plotDir, hist_name )
        #if eta_bins :
        #    all_eta_bins = []
        #    for reg_bins in eta_bins.values() :
        #         for rbin in reg_bins :
        #             all_eta_bins.append( rbin )
        #        
        #    #selection = ' PUWeight * ( %s && ph_Is%s[0] && fabs(ph_eta[0]) > %f && fabs(ph_eta[0]) < %f  ) ' %(el_cuts[ch], reg, etamin, etamax)
        #    selection = ' PUWeight * ( %s ) ' %(el_cuts[ch])
        #    hist_name = 'pt_leadph12_%s'%(ch)

        #    var2d = 'ph_pt[0]:fabs(ph_eta[0])' # y:x
        #    bins_2d = ( 250, 0, 2.5, 40, 0, 200)

        #    draw_singleph_hists_proj( var2d, selection, bins_2d, data_sample, baseDir, plotDir, hist_name, all_eta_bins )


        make_hist_from_pickle( samplesLG, baseDir + '/jet_fake_results__%s.pickle'%ch            , '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag=ch, regions=regions, eta_bins=eta_bins )

    if makeEleFake :
        make_hist_from_pickle( samplesLG, baseDir + '/electron_fake_results%s.pickle'%ch            , '%s/%s/EleFake/hist.root' %(baseDir, plotDir), tag=ch, regions=regions, eta_bins=eta_bins)

def draw_singleph_hists( var, selection, bins, data_sample, baseDir, plotDir, hist_name ) :

    samplesLG.Draw( var, selection, bins)

    hist_data_mg = samplesLG.get_samples(name=data_sample)[0].hist.Clone(hist_name)
    save_hist( '%s/%s/Data/hist.root' %(baseDir, plotDir), hist_data_mg )

    hist_wg_mg  = samplesLG.get_samples(name='Wgamma')[0].hist.Clone(hist_name)
    save_hist( '%s/%s/Wg/hist.root' %(baseDir, plotDir), hist_wg_mg )

    hist_zg_mg  = samplesLG.get_samples(name='Zgamma')[0].hist.Clone(hist_name)
    save_hist( '%s/%s/Zg/hist.root' %(baseDir, plotDir), hist_zg_mg )

    #hist_zjets_mg  = samplesLG.get_samples(name='DYJetsToLLPhOlap')[0].hist.Clone(hist_name)
    #save_hist( '%s/%s/ZJets/hist.root' %(baseDir, plotDir), hist_zjets_mg )

def draw_singleph_hists_proj( var, selection, bins, data_sample, baseDir, plotDir, hist_name, eta_bins ) :

    #samplesLG.Draw( var, selection, bins)

    #hist_data_inc = samplesLG.get_samples( name=data_sample )[0].hist
    #hist_wg_inc   = samplesLG.get_samples( name='Wgamma'    )[0].hist
    #hist_zg_inc   = samplesLG.get_samples( name='Zgamma'    )[0].hist

    data_samp = samplesLG.get_samples( name=data_sample )[0]
    wg_samp   = samplesLG.get_samples( name='Wgamma')[0]
    zg_samp   = samplesLG.get_samples( name='Zgamma')[0]

    samplesLG.create_hist(data_samp, var, selection, bins )
    samplesLG.create_hist(wg_samp, var, selection, bins )
    samplesLG.create_hist(zg_samp, var, selection, bins )

    hist_data_inc = data_samp.hist.Clone( '%s_inc' %data_sample )
    hist_wg_inc   = wg_samp.hist.Clone( 'Wgamma_inc' )
    hist_zg_inc   = zg_samp.hist.Clone( 'Zgamma_inc' )

    for etamin, etamax in eta_bins :

        full_hist_name = '%s_%.2f-%.2f' %( hist_name, etamin, etamax )

        etabinmin = hist_data_inc.GetXaxis().FindBin( etamin )
        etabinmax = hist_data_inc.GetXaxis().FindBin( etamax ) - 1

        hist_data_mg = hist_data_inc.ProjectionY( full_hist_name, etabinmin, etabinmax );
        hist_wg_mg   = hist_wg_inc  .ProjectionY( full_hist_name, etabinmin, etabinmax );
        hist_zg_mg   = hist_zg_inc  .ProjectionY( full_hist_name, etabinmin, etabinmax );

        save_hist( '%s/%s/Data/hist.root' %(baseDir, plotDir), hist_data_mg )

        save_hist( '%s/%s/Wg/hist.root' %(baseDir, plotDir), hist_wg_mg )

        save_hist( '%s/%s/Zg/hist.root' %(baseDir, plotDir), hist_zg_mg )

    #hist_zjets_mg  = samplesLG.get_samples(name='DYJetsToLLPhOlap')[0].hist.Clone(hist_name)
    #save_hist( '%s/%s/ZJets/hist.root' %(baseDir, plotDir), hist_zjets_mg )

def make_hist_from_pickle( sampMan, input_file, output_hist, tag, regions, eta_bins={} ) :

    # get jet fake background estimate
    if not os.path.isfile( input_file) :
        print 'Could not find input file ', input_file
        return

    ofile = open( input_file, 'r' )

    data = pickle.load(ofile)

    ofile.close()

    samp_list = sampMan.get_samples()
    for reg in regions :
        hist = None
        for s in samp_list :
            if s.hist is not None :
                hist = s.hist.Clone( 'pt_leadph12_%s_%s' %(tag, reg) )
                break

        make_hist( data, hist, reg, output_hist )

        if eta_bins :
            for etamin, etamax in eta_bins[reg] :
                eta_bin = '%.2f-%.2f' %(etamin, etamax)
                hist_eta_bin = hist.Clone( 'pt_leadph12_%s_%s' %(tag, eta_bin) )
                make_hist( data, hist_eta_bin, eta_bin, output_hist )

def make_hist( data, hist, reg_bin, output_hist ) :

    for ptbin in range( 1, hist.GetNbinsX()+1 ) :
        min = int(hist.GetXaxis().GetBinLowEdge(ptbin))
        max = int(hist.GetXaxis().GetBinUpEdge(ptbin))

        if max <= 15 :
            continue

        maxval = str(max)
        if ptbin == hist.GetNbinsX() :
            maxval = 'max'

        databin = ( reg_bin, str( min), maxval )

        print data['stat+syst']['result'].keys()
        hist.SetBinContent( ptbin, data['stat+syst']['result'][databin].n )
        hist.SetBinError( ptbin, data['stat+syst']['result'][databin].s )

    save_hist( output_hist, hist )

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

def update_jet_files_dict( dict_to, dict_from ) :
    for key in dict_to.keys() :
        for etakey, etaval in dict_from[key].iteritems() :
            dict_to[key][etakey] = etaval






if __name__ == '__main__' :
    main()
