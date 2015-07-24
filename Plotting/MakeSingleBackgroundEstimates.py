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
           'singleelwzcr' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==1 && ph_hasPixSeed[0]==1 && dr_ph1_leadLep > %.1f && mu_n==0 && m_leadLep_ph1 > 76 && m_leadLep_ph1 < 106 ' %( lead_dr_cut ),
           'singleelw' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==1 && ph_hasPixSeed[0]==1 && dr_ph1_leadLep > %.1f && mu_n==0 && mt_lep_met > 80  ' %( lead_dr_cut ),
           'elwzcr' : 'el_passtrig_n>0 && el_n==1 && ph_medium_n==1 && leadPhot_leadLepDR > %.1f && m_lepph1 > 76 && m_lepph1 < 106 ' %( lead_dr_cut ),
           'muw' : ' mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && leadPhot_leadLepDR>0.4 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_lep_met > 80 ',
           'el' : 'el_passtrig_n>0 && el_n==2 && ph_medium_n==1 && leadPhot_leadLepDR>%.1f && leadPhot_sublLepDR>%.1f && m_leplep>60 && m_leplepph > 105' %( lead_dr_cut, lead_dr_cut ) ,
           'mu' : 'mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoEleVeto_n==1 && leadPhot_leadLepDR>%.1f  && leadPhot_sublLepDR>%.1f && el_n==0 && m_leplep>60 && m_leplepph > 105' %( lead_dr_cut, lead_dr_cut ) ,
           'elrealcr' : 'el_passtrig_n>0 && el_n==2 && ph_medium_n==1 && leadPhot_leadLepDR>%.1f && leadPhot_sublLepDR>%.1f && m_leplep>60 && m_leplepph >81 && m_leplepph < 101' %( lead_dr_cut, lead_dr_cut ) ,
           'murealcr' : 'mu_passtrig25_n>0 && mu_n==2 && ph_medium_n==1 && leadPhot_leadLepDR>%.1f  && leadPhot_sublLepDR>%.1f && el_n==0 && m_leplep>60 && m_leplepph >81 && m_leplepph < 101' %( lead_dr_cut, lead_dr_cut ) ,
}

def main() :


    global samplesLLG
    global samplesLG

    baseDirLLG  = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29'
    baseDirLG   = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_06_29'
    #baseDirLG   = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaJJNoPhID_2015_05_05'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfLLG = 'Modules/Wgamgam.py'

    samplesLLG  = SampleManager(baseDirLLG,  treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesLG   = SampleManager(baseDirLG ,  treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesLLG .ReadSamples( sampleConfLLG )
    samplesLG  .ReadSamples( sampleConfLLG )


    #file_bin_map = {'ElectronFakeFitsRatio' : [(15,20), (20,25), (25,30), (30,40), (40,50), (50,70), (70, 'max')] }
    #file_bin_map_syst = {'ElectronFakeFitsRatioExpBkg' : [(15,20), (20,25), (25,30), (30,40), (40,50), (50,70), (70, 'max') ] }
    #file_bin_map = {'ElectronFakeFitsRatioMCTemplateNDKeys' : [(15,20), (20,25), (25,30), (30, 35), (35, 40), (40, 45), (45, 50), (50,60), (60,70), (70,100), (100,'max') ] }
    #file_bin_map = {'ElectronFakeFitsRatioExpBkg' : [(15,20), (20,25), (25,30), (30, 35), (35, 40), (40, 45), (45, 50), (50,60), (60,70), (70,100), (100,'max') ] }
    #file_bin_map_syst = {'ElectronFakeFitsRatioExpBkg' : [(15,20), (20,25), (25,30), (30, 35), (35, 40), (40, 45), (45, 50), (50,60), (60,70), (70,100), (100,'max')] }
    #file_bin_map = {'ElectronFakeFitsRatioMCTemplateNDKeys' : [(15,20), (20,25), (25,30), (30, 35), (35, 40), (40, 45), (45, 50), (50,60), (60,70), (70,100), (100,'max')] }
    #file_bin_map_syst = {'ElectronFakeFitsRatioMCTemplateNDKeys' : [(15,20), (20,25), (25,30), (30, 35), (35, 40), (40, 45), (45, 50), (50,60), (60,70), (70,100), (100,'max')] }
    #file_bin_map = {'ElectronFakeFitsRatio' : [(_ptbins[0], _ptbins[1]), (_ptbins[1], _ptbins[2]), (_ptbins[2], _ptbins[3]), (_ptbins[3], 'max')] }
    #file_bin_map_syst = {'ElectronFakeFitsRatioExpBkg' : [(_ptbins[0], _ptbins[1]), (_ptbins[1], _ptbins[2]), (_ptbins[2], _ptbins[3]),(_ptbins[3], 'max') ] }
    #file_bin_map = {'ElectronFakeFitsRatioMCTemplateNDKeys' : [(_ptbins[0], _ptbins[1]), (_ptbins[1], _ptbins[2]), (_ptbins[2], _ptbins[3]), (_ptbins[3], 'max')] }
    #file_bin_map = {'ElectronFakeFitsRatioMCTemplateNDKeysSubtractZgamma' : [(_ptbins[0], _ptbins[1]), (_ptbins[1], _ptbins[2]), (_ptbins[2], _ptbins[3]), (_ptbins[3], 'max')] }
    #file_bin_map_syst = {'ElectronFakeFitsRatioExpBkg' : [(_ptbins[0], _ptbins[1]), (_ptbins[1], _ptbins[2]), (_ptbins[2], _ptbins[3]),(_ptbins[3], 'max') ] }


    if options.wcr :

        suffix = ''
        path_nom           = 'ElectronFakeFitsRatio%s' %suffix 
        path_mctemp        = 'ElectronFakeFitsRatio%sMCTemplateNDKeys' %suffix

        file_bin_map = {}
        file_bin_map_syst = {}

        # go up to the second-to-last bin
        for bidx in range( 0, len( _ptbins ) - 2 ) :
            file_bin_map.setdefault(path_mctemp, []).append((_ptbins[bidx], _ptbins[bidx+1]))
            file_bin_map_syst.setdefault(path_mctemp, []).append((_ptbins[bidx], _ptbins[bidx+1]))

        # do the last bin
        file_bin_map[path_nom] = [(_ptbins[-2], 'max')]
        file_bin_map_syst[path_nom] = [(_ptbins[-2], 'max')  ]

        for typedir in os.listdir( '%s/SinglePhotonResults'%options.baseDir ) :
            base_dir_ele_single = options.baseDir
            base_dir_jet_single = '%s/SinglePhotonResults/%s' %(options.baseDir, typedir)
            outputDirSingle='%s/SinglePhotonWCRBackgroundEstimates/%s' %(options.baseDir, typedir)

            #MakeSingleJetBkgEstimate( base_dir_jet_single, channels=['elwzcr', 'elwzcrinvpixlead'],outputDir=outputDirSingle )
            #MakeSingleEleBkgEstimate( base_dir_ele_single, base_dir_jet_single, file_bin_map, file_bin_map_syst, el_selection='elw', outputDir=outputDirSingle )
            MakeSingleEleBkgEstimate( base_dir_ele_single, base_dir_jet_single, file_bin_map, file_bin_map_syst, el_selection='elwzcr', outputDir=outputDirSingle, namePostfix='__zcr' )
            #MakeSingleJetBkgEstimate( base_dir_jet_single, channels=['muw'],outputDir=outputDirSingle )

            MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=['elwzcr'] )
            #MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=['muw'] )

    if options.zcr :

        for typedir in os.listdir( '%s/SinglePhotonResults'%options.baseDir ) :

            base_dir_jet_single = '%s/SinglePhotonResults/%s' %(options.baseDir, typedir )
            outputDirSingle='%s/SinglePhotonZCRBackgroundEstimates/%s' %(options.baseDir, typedir)

            #MakeSingleJetBkgEstimate( base_dir_jet_single, channels=['mu', 'el', 'murealcr', 'elrealcr'], outputDir=outputDirSingle )
            #MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=['mu', 'el', 'murealcr', 'elrealcr'], makeEleFake=False )
            MakeSingleJetBkgEstimate( base_dir_jet_single, channels=['mu'], outputDir=outputDirSingle )
            MakeSingleBkgEstimatePlots( outputDirSingle, options.plotDir, channels=['mu'], makeEleFake=False )

    print '^_^ FINSISHED ^_^'
    print 'It is safe to kill the program if it is hanging'

def MakeSingleEleBkgEstimate(base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, outputDir=None, el_selection='el', namePostfix='') :

    el_acc = ['elw', 'elwzcr']
    if el_selection not in el_acc :
        print 'Input region not recognized, must be %s' %(','.join(el_acc) )
        return

    samplesLLG.deactivate_all_samples()
    samplesLLG.activate_sample('Data')

    eta_bins = {'EB': [0.0, 0.1, 0.5, 1.0, 1.44 ], 'EE' : [1.57, 2.1, 2.2, 2.3, 2.4, 2.5] }
    regions = ['EB','EE']

    results_nom = get_ele_single_fakefactors( base_dir_ele, file_bin_map, regions, eta_bins, el_selection )
    results_syst = get_ele_single_fakefactors( base_dir_ele, file_bin_map_syst, regions, eta_bins, el_selection )

    file_key_lead = 'results__%sinvpixlead__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_lead_syst = 'results__syst__%sinvpixlead__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    #jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'
    jet_dirs_key = 'JetSinglePhotonFakeNomIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    jet_files_lead      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead      )
    jet_files_lead_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead_syst )

    print 'jet_files_lead'
    print jet_files_lead

    pt_bins_jetfile = [str(x) for x in _ptbins[:-1]]
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
    results_subtracted['stat+syst'] = {}
    results_subtracted['stat+syst']['result'] = {}
    for (r1, ptmin, ptmax), val in results_nom['stat+syst']['result'].iteritems() :
        print 'Reg = %s, pt %s-%s, N Pix CR* ff = %s, N Jet Pix CR * ff = %s, pred = %s' %( r1, ptmin, ptmax, val, scaled_f[(r1, ptmin, ptmax)], val- scaled_f[(r1, ptmin, ptmax)] )
        results_subtracted['stat+syst']['result'][(r1, ptmin, ptmax)] = val-scaled_f[ (r1,ptmin,ptmax) ] 


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

def MakeSingleJetBkgEstimate( base_dir_jet, channels=[], outputDir=None ) :

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
        file_key = 'results__%s__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %channel
        file_key_syst = 'results__syst__%s__(EB|EE)__pt_(\d+)-(\d+|max).pickle' %channel

        jet_files      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key      )
        jet_files_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_syst )

        jet_pred     = get_jet_single_fake_results( jet_files    , jet_files_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print 'Predicted Jet fakes for channel %s' %channel

        for r1 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

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
        rfile = ROOT.TFile.Open( '%s/%s/results.root'%(base_dir_ele, file ) )
        rhist = rfile.Get('ff')

        nxbins = rhist.GetXaxis().GetNbins()
        nybins = rhist.GetYaxis().GetNbins()
        xmin = rhist.GetXaxis().GetBinLowEdge(1)
        xmax = rhist.GetXaxis().GetBinUpEdge(nxbins)
        ymin = rhist.GetYaxis().GetBinLowEdge(1)
        ymax = rhist.GetYaxis().GetBinUpEdge(nybins)

        data_samp = samplesLG.get_samples( name='Electron' )[0]
        # get data counts from inverted pixel seed 
        for r1 in regions :
            #invert lead, draw lead
            samplesLG.create_hist(data_samp, 'fabs(ph_eta[0]):ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[0] )' %(el_cuts['single'+el_selection], r1, ), (nxbins, xmin, xmax, nybins, ymin, ymax) )

            hist_lead = data_samp.hist.Clone('hist_lead__%s' %(r1))

            for ptmin, ptmax in ptbins :
                results_lead['stat+syst']['result'][(r1, str(ptmin), str(ptmax))] = 0
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
                    
                    print 'Region = %s, ptmin = %s, ptmax = %s, nData = %d, ff = %f' %( r1, ptmin, ptmax, nData, ff )

                    #print 'ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptbinmax = %d, etabinmin = %d, etabinmax = %d' %( ptmin, ptmax, etamin, etamax, ptbinmin, ptbinmax, etabinmin, etabinmax )
                    #print 'GetBinContent in %f < pt < %f, %f < eta < %f ' %( rhist.GetXaxis().GetBinLowEdge(ptbinmin), rhist.GetXaxis().GetBinUpEdge(ptbinmax), rhist.GetYaxis().GetBinLowEdge(etabinmin), rhist.GetYaxis().GetBinUpEdge(etabinmin) )

                    results_lead['stat+syst']['result'][(r1, str(ptmin), str(ptmax))]  = results_lead['stat+syst']['result'][(r1, str(ptmin), str(ptmax))] + nData*ff

    return results_lead

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
       val['result'] = {}

    for r1 in regions :

        for idx, ptmin in enumerate(pt_bins[:-1]) :
            ptmax = pt_bins[idx+1]

            reg_bin = (r1, ptmin, ptmax) 

            sorted_jet_dirs = jet_files.keys()
            sorted_jet_dirs.sort()

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
                    print 'No data entries for AsymIso %d-%d-%d, region %s, pt %s-%s ' %( dir_key[0], dir_key[1], dir_key[2], r1,  ptmin, ptmax )
                    print 'Ndata_t = %s, Ndata_l = %s' %( Ndata_t, Ndata_l)
                    continue

                Npred_f = predictions['Npred_F_T']
                Npred_r = predictions['Npred_R_T']

                Npred_f_syst = predictions_syst['Npred_R_T']
                Npred_r_syst = predictions_syst['Npred_F_T']

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

    return results

def MakeSingleBkgEstimatePlots( baseDir, plotDir, channels=[], makeEleFake=True ) :

    # first make the nominal estimates

    regions = ['EB','EE']

    for ch in channels :
        for reg in regions :

            samplesLG.deactivate_all_samples()
            samplesLG.activate_sample( 'Wgamma' )
            samplesLG.activate_sample( 'Zgamma' )
            samplesLG.activate_sample( 'DYJetsToLLPhOlap' )

            data_sample = None
            if ch.count('mu') :
                data_sample = 'Muon'
            if ch.count('el') :
                data_sample = 'Electron'
    
            samplesLG.activate_sample( data_sample )
            samplesLG.Draw( 'ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[0]  ) ' %(el_cuts[ch], reg), _ptbins)

            hist_data_mg = samplesLG.get_samples(name=data_sample)[0].hist.Clone('pt_leadph12_%s_%s'%(ch,reg))
            save_hist( '%s/%s/Data/hist.root' %(baseDir, plotDir), hist_data_mg )

            hist_wg_mg  = samplesLG.get_samples(name='Wgamma')[0].hist.Clone('pt_leadph12_%s_%s'%(ch,reg))
            save_hist( '%s/%s/Wg/hist.root' %(baseDir, plotDir), hist_wg_mg )

            hist_zg_mg  = samplesLG.get_samples(name='Zgamma')[0].hist.Clone('pt_leadph12_%s_%s'%(ch,reg))
            save_hist( '%s/%s/Zg/hist.root' %(baseDir, plotDir), hist_zg_mg )

            hist_zjets_mg  = samplesLG.get_samples(name='DYJetsToLLPhOlap')[0].hist.Clone('pt_leadph12_%s_%s'%(ch,reg))
            save_hist( '%s/%s/ZJets/hist.root' %(baseDir, plotDir), hist_zjets_mg )

        make_hist_from_pickle( samplesLG, baseDir + '/jet_fake_results__%s.pickle'%ch            , '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag=ch, regions=regions )

    if makeEleFake :
        make_hist_from_pickle( samplesLG, baseDir + '/electron_fake_results__zcr.pickle'       , '%s/%s/EleFake/hist.root' %(baseDir, plotDir), tag='elwzcr', regions=regions)
        make_hist_from_pickle( samplesLG, baseDir + '/electron_fake_results.pickle'            , '%s/%s/EleFake/hist.root' %(baseDir, plotDir), tag='elw', regions=regions)

def make_hist_from_pickle( sampMan, input_file, output_hist, tag, regions ) :

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

        for ptbin in range( 1, hist.GetNbinsX()+1 ) :
            min = int(hist.GetXaxis().GetBinLowEdge(ptbin))
            max = int(hist.GetXaxis().GetBinUpEdge(ptbin))

            if max <= 15 :
                continue

            maxval = str(max)
            if ptbin == hist.GetNbinsX() :
                maxval = 'max'

            databin = ( reg, str( min), maxval )

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




if __name__ == '__main__' :
    main()
