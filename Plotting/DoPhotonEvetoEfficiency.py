
from RooFitBase import fit_model_to_data, draw_fitted_results, SetHistContentBins
from SampleManager import SampleManager
from SampleManager import Sample
from uncertainties import ufloat
import uuid
import ROOT
import os
import pickle
import collections
from array import array

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

p.add_argument('--outputDir',default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')

options = p.parse_args()

if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
else :
    ROOT.gROOT.SetBatch(False)

_photon_hist_eta_pt_bins = ( [0, 1.44, 1.57, 2.5], [15,20,25,30,40,50,70,100] )

uncert_base = '%s/SinglePhotonResults/SigmaIEIEFits/JetSinglePhotonFakeNomIso' %options.outputDir
_photon_jet_fake_uncert_files = { 'mmg_passpsv' : { 
                                   ('EB', '15', '20')  : uncert_base+'/results__muzpeak_eff_passpsv__EB__pt_15-20.pickle',
                                   ('EB', '20', '25')  : uncert_base+'/results__muzpeak_eff_passpsv__EB__pt_20-25.pickle',
                                   ('EB', '25', '30')  : uncert_base+'/results__muzpeak_eff_passpsv__EB__pt_25-30.pickle',
                                   ('EB', '30', '40')  : uncert_base+'/results__muzpeak_eff_passpsv__EB__pt_30-40.pickle',
                                   ('EB', '40', '50')  : uncert_base+'/results__muzpeak_eff_passpsv__EB__pt_40-50.pickle',
                                   ('EB', '50', '70')  : uncert_base+'/results__muzpeak_eff_passpsv__EB__pt_50-70.pickle',
                                   ('EB', '70', 'max') : uncert_base+'/results__muzpeak_eff_passpsv__EB__pt_70-max.pickle',
                                   ('EE', '15', '20')  : uncert_base+'/results__muzpeak_eff_passpsv__EE__pt_15-20.pickle',
                                   ('EE', '20', '25')  : uncert_base+'/results__muzpeak_eff_passpsv__EE__pt_20-25.pickle',
                                   ('EE', '25', '30')  : uncert_base+'/results__muzpeak_eff_passpsv__EE__pt_25-30.pickle',
                                   ('EE', '30', '40')  : uncert_base+'/results__muzpeak_eff_passpsv__EE__pt_30-40.pickle',
                                   ('EE', '40', '50')  : uncert_base+'/results__muzpeak_eff_passpsv__EE__pt_40-50.pickle',
                                   ('EE', '50', '70')  : uncert_base+'/results__muzpeak_eff_passpsv__EE__pt_50-70.pickle',
                                   ('EE', '70', 'max') : uncert_base+'/results__muzpeak_eff_passpsv__EE__pt_70-max.pickle',
                                 },
                                  'mg_passpsv_highpt' : {
                                   ('EB', '15', '20')  : uncert_base+'/results__muw_eff_passpsv__EB__pt_15-20.pickle',
                                   ('EB', '20', '25')  : uncert_base+'/results__muw_eff_passpsv__EB__pt_20-25.pickle',
                                   ('EB', '25', '30')  : uncert_base+'/results__muw_eff_passpsv__EB__pt_25-30.pickle',
                                   ('EB', '30', '40')  : uncert_base+'/results__muw_eff_passpsv__EB__pt_30-40.pickle',
                                   ('EB', '40', '50')  : uncert_base+'/results__muw_eff_passpsv__EB__pt_40-50.pickle',
                                   ('EB', '50', '70')  : uncert_base+'/results__muw_eff_passpsv__EB__pt_50-70.pickle',
                                   ('EB', '70', 'max') : uncert_base+'/results__muw_eff_passpsv__EB__pt_70-max.pickle',
                                   ('EE', '15', '20')  : uncert_base+'/results__muw_eff_passpsv__EE__pt_15-20.pickle',
                                   ('EE', '20', '25')  : uncert_base+'/results__muw_eff_passpsv__EE__pt_20-25.pickle',
                                   ('EE', '25', '30')  : uncert_base+'/results__muw_eff_passpsv__EE__pt_25-30.pickle',
                                   ('EE', '30', '40')  : uncert_base+'/results__muw_eff_passpsv__EE__pt_30-40.pickle',
                                   ('EE', '40', '50')  : uncert_base+'/results__muw_eff_passpsv__EE__pt_40-50.pickle',
                                   ('EE', '50', '70')  : uncert_base+'/results__muw_eff_passpsv__EE__pt_50-70.pickle',
                                   ('EE', '70', 'max') : uncert_base+'/results__muw_eff_passpsv__EE__pt_70-max.pickle',
                                  },

                                  'mmg_medium' : {
                                   ('EB', '15', '20')  : uncert_base+'/results__muzpeak_eff_medium__EB__pt_15-20.pickle',
                                   ('EB', '20', '25')  : uncert_base+'/results__muzpeak_eff_medium__EB__pt_20-25.pickle',
                                   ('EB', '25', '30')  : uncert_base+'/results__muzpeak_eff_medium__EB__pt_25-30.pickle',
                                   ('EB', '30', '40')  : uncert_base+'/results__muzpeak_eff_medium__EB__pt_30-40.pickle',
                                   ('EB', '40', '50')  : uncert_base+'/results__muzpeak_eff_medium__EB__pt_40-50.pickle',
                                   ('EB', '50', '70')  : uncert_base+'/results__muzpeak_eff_medium__EB__pt_50-70.pickle',
                                   ('EB', '70', 'max') : uncert_base+'/results__muzpeak_eff_medium__EB__pt_70-max.pickle',
                                   ('EE', '15', '20')  : uncert_base+'/results__muzpeak_eff_medium__EE__pt_15-20.pickle',
                                   ('EE', '20', '25')  : uncert_base+'/results__muzpeak_eff_medium__EE__pt_20-25.pickle',
                                   ('EE', '25', '30')  : uncert_base+'/results__muzpeak_eff_medium__EE__pt_25-30.pickle',
                                   ('EE', '30', '40')  : uncert_base+'/results__muzpeak_eff_medium__EE__pt_30-40.pickle',
                                   ('EE', '40', '50')  : uncert_base+'/results__muzpeak_eff_medium__EE__pt_40-50.pickle',
                                   ('EE', '50', '70')  : uncert_base+'/results__muzpeak_eff_medium__EE__pt_50-70.pickle',
                                   ('EE', '70', 'max') : uncert_base+'/results__muzpeak_eff_medium__EE__pt_70-max.pickle',
                                  },
                                  'mg_medium_highpt' : {
                                   ('EB', '15', '20')  : uncert_base+'/results__muw_eff_medium__EB__pt_15-20.pickle',
                                   ('EB', '20', '25')  : uncert_base+'/results__muw_eff_medium__EB__pt_20-25.pickle',
                                   ('EB', '25', '30')  : uncert_base+'/results__muw_eff_medium__EB__pt_25-30.pickle',
                                   ('EB', '30', '40')  : uncert_base+'/results__muw_eff_medium__EB__pt_30-40.pickle',
                                   ('EB', '40', '50')  : uncert_base+'/results__muw_eff_medium__EB__pt_40-50.pickle',
                                   ('EB', '50', '70')  : uncert_base+'/results__muw_eff_medium__EB__pt_50-70.pickle',
                                   ('EB', '70', 'max') : uncert_base+'/results__muw_eff_medium__EB__pt_70-max.pickle',
                                   ('EE', '15', '20')  : uncert_base+'/results__muw_eff_medium__EE__pt_15-20.pickle',
                                   ('EE', '20', '25')  : uncert_base+'/results__muw_eff_medium__EE__pt_20-25.pickle',
                                   ('EE', '25', '30')  : uncert_base+'/results__muw_eff_medium__EE__pt_25-30.pickle',
                                   ('EE', '30', '40')  : uncert_base+'/results__muw_eff_medium__EE__pt_30-40.pickle',
                                   ('EE', '40', '50')  : uncert_base+'/results__muw_eff_medium__EE__pt_40-50.pickle',
                                   ('EE', '50', '70')  : uncert_base+'/results__muw_eff_medium__EE__pt_50-70.pickle',
                                   ('EE', '70', 'max') : uncert_base+'/results__muw_eff_medium__EE__pt_70-max.pickle',
                                  },

}


def get_default_draw_commands( ch ) :

    if ch=='mmg_medium' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_mediumNoEleVeto_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15 && m_leplep < 80'
    elif ch=='mmg_passpsv' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_mediumPassPSV_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15 && m_leplep < 80'
    elif ch=='mg_medium_highpt' :
        return 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoEleVeto_n==1 && dr_ph1_leadLep>0.4 && mt_lep_met > 60'
    elif ch=='mg_passpsv_highpt' :
        return 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumPassPSV_n==1 && dr_ph1_leadLep>0.4 && mt_lep_met > 60'
    else :
        return None
def get_phvar( ch ) :

    if ch=='mmg_medium' :
        return 'ptSorted_ph_mediumNoEleVeto_idx'
    elif ch=='mmg_passpsv' :
        return 'ptSorted_ph_mediumPassPSV_idx'
    elif ch=='mg_medium_highpt' :
        return 'ptSorted_ph_mediumNoEleVeto_idx'
    elif ch=='mg_passpsv_highpt' :
        return 'ptSorted_ph_mediumPassPSV_idx'
    else :
        return None

def get_background_draw_commands( ch ) :

    if   ch=='mmg_medium' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_mediumNoEleVeto_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 81 && m_leplep < 101'
    elif ch=='mmg_passpsv' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_mediumPassPSV_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 81 && m_leplep < 101'
    else :
        return None

def get_normalization_draw_commands_in( ch ) :

    if   ch=='mmg_medium' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 81 && m_leplep < 101'
    elif ch=='mmg_passpsv' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && ph_hasPixSeed[0]==0 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 81 && m_leplep < 101'
    else :
        return None

def get_normalization_draw_commands_out( ch ) :

    if   ch=='mmg_medium' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep < 80 && m_leplep > 15 && m_leplepph > 76 && m_leplepph < 106'
    elif ch=='mmg_passpsv' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && ph_hasPixSeed[0]==0 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep < 80 && m_leplep > 15 && m_leplepph > 76 && m_leplepph < 106'
    else :
        return None

def main() :


    global sampManMMG
    global sampManMG

    base_dir_mmg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_10_01'
    base_dir_mg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'
    xsFile = 'cross_sections/wgamgam.py'
    lumi = 19400

    sampManMMG = SampleManager(base_dir_mmg, treeName=treename,filename=filename, xsFile=xsFile, lumi=lumi)
    sampManMG = SampleManager(base_dir_mg, treeName=treename,filename=filename, xsFile=xsFile, lumi=lumi)

    samplesConf = 'Modules/TAndPSampleConf.py'

    sampManMMG.ReadSamples( samplesConf )
    sampManMG.ReadSamples( samplesConf )

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )
        

        subdir = 'PhotonEfficiencies'
        outputDir = options.outputDir + '/' + subdir

        pt_bins = [15, 20, 25, 30, 40, 50, 70, 1000000]

        #eff_medium_data = GetPhotonEfficiencies( data_sample='Muon'  , numerator = 'mmg_medium', denominator='mmg_loose' , pt_bins=pt_bins, bkg_sample='DYJetsToLLPhOlap', outputDir=outputDir+'/DataLLCut' )
        eff_passpsv_data  = GetPhotonEfficiencies( data_sample='Muon'  , numerator = 'mmg_passpsv' , denominator='mmg_medium', pt_bins=pt_bins, bkg_sample='DYJetsToLLPhOlap', outputDir=outputDir+'/DataLLCut' )
        #eff_medium_mc   = GetPhotonEfficiencies( data_sample='Zgamma', numerator = 'mmg_medium', denominator='mmg_loose' , pt_bins=pt_bins, bkg_sample=None, outputDir=outputDir+'/MCLLCut' )
        eff_passpsv_mc    = GetPhotonEfficiencies( data_sample='Zgamma', numerator = 'mmg_passpsv' , denominator='mmg_medium', pt_bins=pt_bins, bkg_sample=None, outputDir=outputDir+'/MCLLCut' )

        pt_bins_high = [15, 20, 25, 30, 40, 50, 70, 1000000]

        #eff_medium_data = GetPhotonEfficienciesHighPt( data_sample='Muon'  , numerator='mmg_medium', denominator='mmg_loose' , pt_min=pt_min_high, outputDir=outputDir+'/DataLLCut' )
        eff_passpsv_data_highpt  = GetPhotonEfficienciesHighPt( data_sample='Muon'  , numerator='mg_passpsv_highpt' , denominator='mg_medium_highpt', ptbins=pt_bins_high, useBkgEstimate=True, outputDir=outputDir+'/DataLLCut' )
        #eff_medium_mc   = GetPhotonEfficienciesHighPt( data_sample='Zgamma', numerator='mmg_medium', denominator='mmg_loose' , pt_min=pt_min_high, outputDir=outputDir+'/MCLLCut' )
        eff_passpsv_mc_highpt    = GetPhotonEfficienciesHighPt( data_sample='Wgamma', numerator='mg_passpsv_highpt' , denominator='mg_medium_highpt', ptbins=pt_bins_high, useBkgEstimate=False, outputDir=outputDir+'/MCLLCut' )

        # --------------------------
        # Put back to save as one
        # output
        # --------------------------
        #for bin, eff in eff_passpsv_data_highpt.iteritems() :
        #    eff_passpsv_data[bin] = eff
        #for bin, eff in eff_passpsv_mc_highpt.iteritems() :
        #    eff_passpsv_mc[bin] = eff

        #print 'Eveto data '
        #for bin, eff in eff_passpsv_data.iteritems() :
        #    print 'Bin = %s, eff = %s' %(bin, eff)

        #print 'Eveto MC '
        #for bin, eff in eff_passpsv_mc.iteritems() :
        #    print 'Bin = %s, eff = %s' %(bin, eff)

        #MakeScaleFactor( eff_medium_data, eff_medium_mc, tag='sf_medium_nom' , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        MakeScaleFactor( eff_passpsv_data , eff_passpsv_mc , tag='sf_passpsv_nom'  , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        MakeScaleFactor( eff_passpsv_data_highpt , eff_passpsv_mc_highpt , tag='sf_passpsv_highpt'  , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        #MakeScaleFactor( eff_medium_data_llcut, eff_medium_mc_llcut, tag='sf_medium_llcut' , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        #MakeScaleFactor( eff_passpsv_data_llcut , eff_passpsv_mc_llcut , tag='sf_passpsv_llcut'  , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )

def GetPhotonEfficienciesHighPt( data_sample, numerator, denominator, ptbins=[], useBkgEstimate=False,  outputDir=None ) :

    eta_reg = ['EB', 'EE']

    data_samp = sampManMMG.get_samples(name=data_sample )
    mass_binning = (40, 0, 200 )

    results = {}

    for reg in eta_reg :

        if reg == 'EB' :
            etamin = 0.0
            etamax = 1.44
        if reg == 'EE' :
            etamin = 1.57
            etamax = 2.50

        data_samp = sampManMG.get_samples(name=data_sample )

        draw_base_num = get_default_draw_commands( numerator )
        draw_base_den = get_default_draw_commands( denominator )

        phvar_num = get_phvar( numerator )
        phvar_den = get_phvar( denominator )

        draw_full_num = '%s && ph_Is%s[%s[0]] ' %( draw_base_num, reg, phvar_num )
        draw_full_den = '%s && ph_Is%s[%s[0]] ' %( draw_base_den, reg, phvar_den )

        draw_var_num = 'ph_pt[%s[0]] ' %( phvar_num ) #y:x
        draw_var_den = 'ph_pt[%s[0]] ' %( phvar_den ) #y:x

        hist_data_num = clone_sample_and_draw( sampManMG, data_samp[0], draw_var_num, 'PUWeight * ( %s )' %draw_full_num, mass_binning )
        hist_data_num.SetName( numerator+'_data' )
        hist_data_den = clone_sample_and_draw( sampManMG, data_samp[0], draw_var_den, 'PUWeight * ( %s )' %draw_full_den, mass_binning )
        hist_data_den.SetName( denominator+'_data' )

        eff_num = GetEfficiencyIntegralsHighPt(  hist_data_num, draw_tag=numerator   , eta_reg=reg,ptbins=ptbins, useBkgEstimate=useBkgEstimate)
        eff_den = GetEfficiencyIntegralsHighPt(  hist_data_den, draw_tag=denominator ,eta_reg=reg ,ptbins=ptbins, useBkgEstimate=useBkgEstimate)

        for res_bin, res_num in eff_num.iteritems() :

            res_den = eff_den[res_bin]

            ptmaxstr = str(res_bin[1])
            if res_bin[1] == ptbins[-1] :
                ptmaxstr = 'max'

            out_bin = ( str(etamin), str(etamax), str(res_bin[0]), ptmaxstr )

            # ----------------------------
            # Numerator
            # ----------------------------


            results[out_bin] = {}
            results[out_bin]['num'] = res_num
            results[out_bin]['den'] = res_den
            results[out_bin]['eff'] = res_num['result']/res_den['result']

    return results


def GetPhotonEfficiencies( data_sample, numerator, denominator, pt_bins=[], bkg_sample=None,  outputDir=None ) :

    eta_reg = ['EB', 'EE']

    data_samp = sampManMMG.get_samples(name=data_sample )

    results = {}

    for reg in eta_reg :

        if reg == 'EB' :
            etamin = 0.0
            etamax = 1.44
        if reg == 'EE' :
            etamin = 1.57
            etamax = 2.50

        data_samp = sampManMMG.get_samples(name=data_sample )

        mass_binning = (40, 0, 200, 200, 0, 200 )

        draw_base_num = get_default_draw_commands( numerator )
        phvar_num     = get_phvar( numerator )
        draw_full_num = '%s && ph_Is%s[%s[0]] ' %( draw_base_num, reg, phvar_num )

        draw_base_den = get_default_draw_commands( denominator )
        phvar_den     = get_phvar( denominator )
        draw_full_den = '%s && ph_Is%s[%s[0]] ' %( draw_base_den, reg, phvar_den )

        draw_var_num = 'm_leplepph:ph_pt[%s[0]] ' %( phvar_num ) #y:x
        draw_var_den = 'm_leplepph:ph_pt[%s[0]] ' %( phvar_den ) #y:x

        hist_data_num = clone_sample_and_draw( sampManMMG, data_samp[0], draw_var_num, 'PUWeight * ( %s )' %draw_full_num, mass_binning )
        hist_data_num.SetName( numerator+'_data' )

        hist_data_den = clone_sample_and_draw( sampManMMG, data_samp[0], draw_var_den, 'PUWeight * ( %s )' %draw_full_den, mass_binning )
        hist_data_den.SetName( denominator+'_data' )

        hist_bkg_in_num    = None
        hist_loose_in_num  = None
        hist_loose_out_num = None

        hist_bkg_in_den    = None
        hist_loose_in_den  = None
        hist_loose_out_den = None
        if bkg_sample is not None :

            bkg_samp = sampManMMG.get_samples( name=bkg_sample )

            draw_base_bkg_in_num = get_background_draw_commands( numerator )
            draw_base_bkg_in_den = get_background_draw_commands( denominator )

            draw_full_bkg_in_num = '%s && ph_Is%s[%s[0]] ' %( draw_base_bkg_in_num, reg, phvar_num )
            draw_full_bkg_in_den = '%s && ph_Is%s[%s[0]] ' %( draw_base_bkg_in_den, reg, phvar_den )

            hist_bkg_in_num = clone_sample_and_draw( sampManMMG, bkg_samp[0], draw_var_num, 'PUWeight * ( %s )' %draw_full_bkg_in_num, mass_binning )
            hist_bkg_in_num.SetName( numerator+'_bkgIN' )
            hist_bkg_in_den = clone_sample_and_draw( sampManMMG, bkg_samp[0], draw_var_den, 'PUWeight * ( %s )' %draw_full_bkg_in_den, mass_binning )
            hist_bkg_in_den.SetName( denominator+'_bkgIN' )

            #IN
            draw_base_loose_in_num = get_normalization_draw_commands_in( numerator )
            draw_base_loose_in_den = get_normalization_draw_commands_in( denominator )
            draw_full_loose_in_num = '%s && ph_Is%s[%s[0]] ' %( draw_base_loose_in_num, reg, phvar_num )
            draw_full_loose_in_den = '%s && ph_Is%s[%s[0]] ' %( draw_base_loose_in_den, reg, phvar_den )

            hist_loose_in_num = clone_sample_and_draw( sampManMMG, bkg_samp[0], draw_var_num, 'PUWeight * ( %s )' %draw_full_loose_in_num, mass_binning )
            hist_loose_in_num.SetName( numerator+'_looseIN' )
            hist_loose_in_den = clone_sample_and_draw( sampManMMG, bkg_samp[0], draw_var_den, 'PUWeight * ( %s )' %draw_full_loose_in_den, mass_binning )
            hist_loose_in_den.SetName( denominator+'_looseIN' )

            #OUT
            draw_base_loose_out_num = get_normalization_draw_commands_out( numerator)
            draw_base_loose_out_den = get_normalization_draw_commands_out( denominator )

            draw_full_loose_out_num = '%s && ph_Is%s[%s[0]] ' %( draw_base_loose_out_num, reg, phvar_num )
            draw_full_loose_out_den = '%s && ph_Is%s[%s[0]] ' %( draw_base_loose_out_den, reg, phvar_den )

            hist_loose_out_num = clone_sample_and_draw( sampManMMG, bkg_samp[0], draw_var_num , 'PUWeight * ( %s )' %draw_full_loose_out_num, mass_binning )
            hist_loose_out_num.SetName( numerator+ '_looseOUT' )
            hist_loose_out_den = clone_sample_and_draw( sampManMMG, bkg_samp[0], draw_var_den , 'PUWeight * ( %s )' %draw_full_loose_out_den, mass_binning )
            hist_loose_out_den.SetName( denominator+ '_looseOUT' )

            num_hists = {'data' : hist_data_num, 'bkg_in' : hist_bkg_in_num, 'loose_in' : hist_loose_in_num, 'loose_out' : hist_loose_out_num }
            den_hists = {'data' : hist_data_den, 'bkg_in' : hist_bkg_in_den, 'loose_in' : hist_loose_in_den, 'loose_out' : hist_loose_out_den }

            eff_num = GetEfficiencyIntegrals( num_hists, reg,pt_bins, numerator)
            eff_den = GetEfficiencyIntegrals( den_hists, reg, pt_bins, numerator)


            for (ptmin, ptmax), res_num in eff_num.iteritems() :

                res_den = eff_den[(ptmin,ptmax)]

                ptmaxstr = str( ptmax )
                if ptmax == pt_bins[-1] :
                    ptmaxstr = 'max'

                
                out_bin = ( str(etamin), str(etamax), str( ptmin ), ptmaxstr )
                res_bin = ( ptmin, ptmax )

                results[out_bin] = {}
                results[out_bin]['num'] = res_num
                results[out_bin]['den'] = res_den
                results[out_bin]['eff'] = res_num['result']/res_den['result']

        return results


def GetEfficiencyIntegrals( hists, eta_reg, pt_bins, draw_tag ) :

    mass_min = 76
    mass_max = 106

    for idx,ptmin in enumerate( pt_bins[:-1] ) :
        ptmax = pt_bins[idx+1]

        results = {}

        result_bin = (ptmin,ptmax)

        results[result_bin] = {}

        hist_data = hists['data']

        ptbinmin = hists['data'].GetXaxis().FindBin(ptmin)
        ptbinmax = hists['data'].GetXaxis().FindBin(ptmax) - 1

        massbinmin = hists['data'].GetYaxis().FindBin( mass_min ) 
        massbinmax = hists['data'].GetYaxis().FindBin( mass_max ) - 1

        err_data = ROOT.Double()
        int_data = hists['data'].IntegralAndError( ptbinmin, ptbinmax, massbinmin, massbinmax, err_data )

        if hists['bkg_in'] is not None :

            err_bkg_in = ROOT.Double()
            int_bkg_in = hists['bkg_in'].IntegralAndError( ptbinmin, ptbinmax, massbinmin, massbinmax, err_bkg_in )

            # get background estimate from
            # data driven jet fake
            dd_file = _photon_jet_fake_uncert_files[draw_tag][(eta_reg, str(ptmin), str(ptmax))]

            dd_ofile = open( dd_file, 'r')
            dd_data = pickle.load( dd_ofile )
            dd_val = dd_data['Npred_F_T']

            # now get the integrals from the in and out regions with loose photon selection
            #IN
            err_loose_in = ROOT.Double()
            int_loose_in = hists['loose_in'].IntegralAndError( ptbinmin, ptbinmax, massbinmin, massbinmax, err_loose_in )

            #OUT
            err_loose_out = ROOT.Double()
            int_loose_out = hists['loose_out'].IntegralAndError(ptbinmin, ptbinmax, massbinmin, massbinmax , err_loose_out )

            # now make the ufloats and do the division
            val_loose_in  = ufloat( int_loose_in, err_loose_in )
            val_loose_out = ufloat( int_loose_out, err_loose_out )
            val_bkg_in    = ufloat( int_bkg_in, err_bkg_in )
            val_data      = ufloat( int_data, err_data )

            results[result_bin]['loose_in' ] = val_loose_in
            results[result_bin]['loose_out'] = val_loose_out
            results[result_bin]['bkg_in' ] = val_bkg_in
            results[result_bin]['Data' ] = val_data
            results[result_bin]['JetFakeBkg' ] = dd_val


            loose_in_out_ratio = (val_loose_out/val_loose_in)
            dd_extrap_bkg      = dd_val*loose_in_out_ratio

            results[result_bin]['loose_in_out_ratio'] = loose_in_out_ratio
            results[result_bin]['Bkg_pred'] = dd_extrap_bkg
            results[result_bin]['result'] = val_data - dd_extrap_bkg

            return results

        else :

            # just take the number from data
            val_data = ufloat( int_data, err_data )
            results[result_bin]['result'] = val_data
            return results

def GetEfficiencyIntegralsHighPt( data_hist, draw_tag, eta_reg, ptbins, useBkgEstimate=False ) :

    results = {}
    for idx, ptmin in enumerate( ptbins[:-1] ) :
        ptmax = ptbins[idx+1]

        ptbinmin   = data_hist.GetXaxis().FindBin(ptmin)
        ptbinmax   = data_hist.GetXaxis().FindBin(ptmax) - 1

        err_data = ROOT.Double()
        int_data = data_hist.IntegralAndError(  ptbinmin, ptbinmax, err_data )

        res_bin = ( ptmin, ptmax )

        results[res_bin] = {}

        if useBkgEstimate :

            ptmaxstr = str(ptmax)
            if ptmax == ptbins[-1] :
                ptmaxstr = 'max'

            bkg_bin = ( eta_reg, str(ptmin), ptmaxstr)

            # get background estimate from
            # data driven jet fake
            dd_file = _photon_jet_fake_uncert_files[draw_tag][bkg_bin]

            dd_ofile = open( dd_file, 'r')
            dd_data = pickle.load( dd_ofile )
            dd_val = dd_data['Npred_F_T']

            val_data = ufloat( int_data, err_data )

            results[res_bin]['Data' ] = val_data
            results[res_bin]['JetFakeBkg' ] = dd_val
            results[res_bin]['result'] = val_data - dd_val

            print results

            return results

        else :

            # just take the number from data
            val_data = ufloat( int_data, err_data )
            results[res_bin]['result'] = val_data
            return results

def MakeScaleFactor( numerator, denominator, tag, binning, outputDir=None ) :
    

    # numerator is data, denominator is MC
    scale_factors = {}
    for bin, res_num in numerator.iteritems() :

        if bin not in denominator :
            print 'Bin not found in denominator', bin
            print numerator
            print denominator
            continue

        res_den = denominator[bin]

        if res_den == 0 :
            print 'SF denominator is zero!'
            scale_factors[bin] = 1000000
        else :
            scale_factors[bin] = res_num['eff'] / res_den['eff']


    hist_sf = ROOT.TH2F( 'hist_%s' %tag, 'hist_%s' %tag, len(binning[0])-1, array( 'f', binning[0]), len(binning[1])-1, array('f', binning[1]) )

    print 'GOt Scale factor'
    print scale_factors

    for bin, sf in scale_factors.iteritems() : 

        etamin = float( bin[0] )
        etamax = float( bin[1] )
        ptmin  = float( bin[2] )
        if bin[3] == 'max' : 
            ptmax = hist_sf.GetYaxis().GetBinUpEdge( hist_sf.GetNbinsY() )
        else :
            ptmax  = float( bin[3] )

        SetHistContentBins( hist_sf, sf, etamin, etamax, ptmin, ptmax )


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )
        file_sf = ROOT.TFile.Open( '%s/hist_%s.root' %( outputDir, tag ), 'RECREATE' )
        print 'Write root file ', file_sf.GetName()
        hist_sf.Write()
        file_sf.Close()

        file_pick = open( '%s/results_%s.pickle' %(outputDir, tag), 'w' )
        pickle.dump( scale_factors, file_pick )
        file_pick.close()

        file_num = open( '%s/details_data_%s.pickle' %(outputDir, tag), 'w' )
        pickle.dump( numerator, file_num )
        file_num.close()

        file_den = open( '%s/details_mc_%s.pickle' %(outputDir, tag), 'w' )
        pickle.dump( denominator, file_den )
        file_den.close()

def pair_pt_eta_bins( bin_list ) :

    paired_bins = {}

    for ptbins, etabins in bin_list :
        paired_eta = []
        for etaidx, etamin in enumerate(etabins[:-1]) :
            etamax = etabins[etaidx+1]
            paired_eta.append( ( etamin, etamax ) )

        for ptidx, ptmin in enumerate(ptbins[:-1]) :
            ptmax = ptbins[ptidx+1]
            paired_bins[ (ptmin, ptmax) ] = paired_eta

    return paired_bins


def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :
        newSamp = sampMan.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
        sampMan.create_hist( newSamp, var, sel, binning )
        return newSamp.hist
                                       
if __name__ == '__main__' :
    main()
