
from RooFitBase import fit_model_to_data, draw_fitted_results, SetHistContentBins
from SampleManager import SampleManager
from SampleManager import Sample
from uncertainties import ufloat
import uuid
import ROOT
import os
import pickle
import collections

_lepton_hist_eta_pt_bins = ( 25, 0.0, 2.5, 401, 0, 401 )
_photon_hist_eta_pt_bins = ( 250, 0.0, 2.5, 401, 0, 401 )

uncert_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_12_08/SinglePhotonResults/JetSinglePhotonFakeNomIso'
_photon_jet_fake_uncert_files = { 'mmg_eveto_llcut' : { 
                                   ('EB', '70', 'max') : uncert_base+'/results__mu_tp_eveto__EB__pt_70-max.pickle',
                                   ('EE', '70', 'max') : uncert_base+'/results__mu_tp_eveto__EE__pt_70-max.pickle',
                                 },
                                  'mmg_medium_llcut' : {
                                   ('EB', '70', 'max') : uncert_base+'/results__mu_tp_medium__EB__pt_70-max.pickle',
                                   ('EE', '70', 'max') : uncert_base+'/results__mu_tp_medium__EE__pt_70-max.pickle',
                                  },
}


def get_default_draw_commands( ch ) :

    if ch=='mmg_loose' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15'
    elif ch=='mmg_medium' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && ph_passMedium[0] && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15 '
    elif ch=='mmg_eveto' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0] == 0 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15 '
    elif ch=='mmg_loose_llcut' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15 && m_leplep < 80'
    elif ch=='mmg_medium_llcut' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && ph_passMedium[0] && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15 && m_leplep < 80'
    elif ch=='mmg_eveto_llcut' :
        return 'mu_passtrig25_n>0 && mu_n>1 && ph_n==1 && ph_passMedium[0] && ph_hasPixSeed[0] == 0 && dr_ph1_leadLep>0.4 && dr_ph1_sublLep>0.4 && m_leplep > 15 && m_leplep < 80'
    elif ch=='mm_loose' :
        return ' muprobe_pt > 0 '
    elif ch=='mm_tight' :
        return ' muprobe_passTight==1 '
    elif ch=='mm_trig' :
        return ' muprobe_triggerMatch ==1 && muprobe_passTight == 1 '
    elif ch=='ee_loose' :
        return 'elprobe_isPh==1 '
    elif ch=='ee_obj' :
        return 'elprobe_isEl==1 && elprobe_isPh==1 '
    elif ch=='ee_tight' :
        return 'elprobe_isEl==1 && elprobe_isPh==0  && elprobe_passMVANonTrig'
    elif ch=='ee_trig' :
        return 'elprobe_isEl==1 && elprobe_isPh==0  && elprobe_passMVATrig && elprobe_triggerMatch'
    else :
        return None

def get_fit_defaults( histname, useMCBkg=False, useMCSig=False ) :

    type = 'bw_cmsshape'
    if useMCBkg :
        type = 'bw_mc'
    if useMCSig :
        type = 'mc_cmsshape'

    defaults = {}

    defaults['bw_mc'] = { 'mean' : 0, 'sigma' : 2.495,'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'nsig' : 5000, 'nbkg' : 1800, 'rho' : 1, 'nSigma' : 3, 'fit_min': 80, 'fit_max' : 160 }

    defaults['bw_cmsshape'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160 }

    defaults['mc_cmsshape'] = { 'mean' : 1, 'sigma' : 0.8, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160 }

    alts = {'bw_mc' : {} , 'bw_cmsshape' : {}, 'mc_cmsshape' : {}}

    #global_alts = {'bw_mc' : {} , 'bw_cmsshape' : {}, 'mc_cmsshape' : {}}
    #global_alts['bw_cmsshape']['hist_mm_\w+_\d\.\d\d-\d\.\d\d_25-30'] = defaults['bw_cmsshape']
    #global_alts['bw_cmsshape']['hist_mm_\w+_\d\.\d\d-\d\.\d\d_25-30']['fit_max'] = 140

    #global_alts['bw_cmsshape']['hist_mm_\w+_\d\.\d\d-\d\.\d\d_25-30'] = defaults['bw_cmsshape']
    #global_alts['bw_cmsshape']['hist_mm_\w+_\d\.\d\d-\d\.\d\d_25-30']['fit_max'] = 140



    # --------------------------------- 
    # mm trig
    # --------------------------------- 
    alts['bw_cmsshape']['hist_mm_trig_2.30-2.40_30-40'] = { 'Bias' : -0.5, 'Width' : 2.5 , 'Cut' : -4.5, 'Power' : 20, 'cms_alpha' : 97, 'cms_beta' : 0.09, 'cms_gamma' : 0.3, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_mm_trig_2.30-2.40_40-50'] = { 'Bias' : -0.5, 'Width' : 2.5 , 'Cut' : -4.5, 'Power' : 20, 'cms_alpha' : 97, 'cms_beta' : 0.09, 'cms_gamma' : 0.3, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_mm_trig_1.80-2.40_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_trig_1.60-1.80_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_trig_1.20-1.60_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_trig_0.80-1.20_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_trig_0.40-0.80_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_trig_0.30-0.40_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_trig_0.20-0.30_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_trig_0.10-0.20_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_trig_0.00-0.10_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}

    # --------------------------------- 
    # mm tight
    # --------------------------------- 
    alts['bw_cmsshape']['hist_mm_tight_2.30-2.40_30-40'] = { 'Bias' : -0.5, 'Width' : 2.5 , 'Cut' : -4.5, 'Power' : 20, 'cms_alpha' : 97, 'cms_beta' : 0.09, 'cms_gamma' : 0.3, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_tight_2.30-2.40_40-50'] = { 'Bias' : -0.5, 'Width' : 2.5 , 'Cut' : -4.5, 'Power' : 20, 'cms_alpha' : 97, 'cms_beta' : 0.09, 'cms_gamma' : 0.3, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}

    alts['bw_cmsshape']['hist_mm_tight_1.80-2.40_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_tight_1.60-1.80_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_tight_1.20-1.60_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_tight_0.80-1.20_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_tight_0.40-0.80_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_tight_0.30-0.40_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_tight_0.20-0.30_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_tight_0.10-0.20_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_mm_tight_0.00-0.10_200-1000000'] = { 'Bias' : 0.3, 'Width' : 2.5 , 'Cut' : -1, 'Power' : 30, 'cms_alpha' : 68, 'cms_beta' : 0.1, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}

    # --------------------------------- 
    # mm loose
    # --------------------------------- 
    alts['bw_cmsshape']['hist_mm_loose_1.60-1.80_200-1000000'] = { 'Bias' : 0.7, 'Width' : 2.5 , 'Cut' : -5, 'Power' : 5, 'cms_alpha' : 40, 'cms_beta' : 0.3, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}

    # --------------------------------- 
    # ee loose
    # --------------------------------- 
    alts['bw_cmsshape']['hist_ee_loose_0.00-0.10_10-15'] = { 'Bias' : 0.1, 'Width' : 3.1 , 'Cut' : -8.5, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.8, 'cms_gamma' : 0.06, 'cms_peak' : 85, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.10-0.20_10-15'] = { 'Bias' : 0.1, 'Width' : 3.1 , 'Cut' : -8.5, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.8, 'cms_gamma' : 0.06, 'cms_peak' : 85, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.20-0.30_10-15'] = { 'Bias' : -0.7, 'Width' : 3.5 , 'Cut' : -6.3, 'Power' : 30, 'cms_alpha' : 53, 'cms_beta' : 0.1, 'cms_gamma' : 0.06, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.30-0.40_10-15'] = { 'Bias' : -0.7, 'Width' : 3.3 , 'Cut' : -3.3, 'Power' : 15, 'cms_alpha' : 60, 'cms_beta' : 0.8, 'cms_gamma' : 0.06, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.40-0.80_10-15'] = { 'Bias' : -0.4, 'Width' : 2.9 , 'Cut' : -1.2, 'Power' : 20, 'cms_alpha' : 50, 'cms_beta' : 0.2, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.80-1.20_10-15'] = { 'Bias' : -0.4, 'Width' : 2.9 , 'Cut' : -1.2, 'Power' : 20, 'cms_alpha' : 50, 'cms_beta' : 0.2, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_1.20-1.60_10-15'] = { 'Bias' : -0.4, 'Width' : 2.9 , 'Cut' : -1.2, 'Power' : 20, 'cms_alpha' : 50, 'cms_beta' : 0.2, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_1.60-1.80_10-15'] = { 'Bias' : -0.4, 'Width' : 2.9 , 'Cut' : -1.2, 'Power' : 20, 'cms_alpha' : 50, 'cms_beta' : 0.2, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_1.80-2.10_10-15'] = { 'Bias' : -0.4, 'Width' : 2.9 , 'Cut' : -1.2, 'Power' : 20, 'cms_alpha' : 50, 'cms_beta' : 0.2, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_2.10-2.30_10-15'] = { 'Bias' : -0.8, 'Width' : 2.0 , 'Cut' : -5, 'Power' : 20, 'cms_alpha' : 50, 'cms_beta' : 0.2, 'cms_gamma' : 0.05, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_2.30-2.50_10-15'] = { 'Bias' : -0.8, 'Width' : 2.0 , 'Cut' : -5, 'Power' : 20, 'cms_alpha' : 50, 'cms_beta' : 0.2, 'cms_gamma' : 0.05, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}

    alts['bw_cmsshape']['hist_ee_loose_0.00-0.10_15-20'] = { 'Bias' : 0.01, 'Width' : 3.0 , 'Cut' : -4.0, 'Power' : 5, 'cms_alpha' : 55, 'cms_beta' : 0.05, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.10-0.20_15-20'] = { 'Bias' : 0.01, 'Width' : 3.0 , 'Cut' : -4.0, 'Power' : 5, 'cms_alpha' : 55, 'cms_beta' : 0.05, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.20-0.30_15-20'] = { 'Bias' : 0.01, 'Width' : 3.0 , 'Cut' : -4.0, 'Power' : 5, 'cms_alpha' : 55, 'cms_beta' : 0.05, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.30-0.40_15-20'] = { 'Bias' : 0.01, 'Width' : 3.0 , 'Cut' : -4.0, 'Power' : 5, 'cms_alpha' : 55, 'cms_beta' : 0.05, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.40-0.80_15-20'] = { 'Bias' : 0.01, 'Width' : 3.0 , 'Cut' : -4.0, 'Power' : 5, 'cms_alpha' : 55, 'cms_beta' : 0.05, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_0.80-1.20_15-20'] = { 'Bias' : -2.8, 'Width' : 3.0 , 'Cut' : -2.7, 'Power' : 10, 'cms_alpha' : 60, 'cms_beta' : 0.5, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_1.20-1.60_15-20'] = { 'Bias' : -2.8, 'Width' : 3.0 , 'Cut' : -2.7, 'Power' : 10, 'cms_alpha' : 60, 'cms_beta' : 0.5, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_1.60-1.80_15-20'] = { 'Bias' : -3, 'Width' : 3.4 , 'Cut' : -4.0, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.5, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_1.80-2.10_15-20'] = { 'Bias' : -1.6, 'Width' : 2.9 , 'Cut' : -4.8, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.5, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_2.10-2.30_15-20'] = { 'Bias' : -1.6, 'Width' : 2.9 , 'Cut' : -4.8, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.5, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_2.30-2.50_15-20'] = { 'Bias' : -1.6, 'Width' : 2.9 , 'Cut' : -4.8, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.5, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}

    alts['bw_cmsshape']['hist_ee_loose_0.00-0.10_20-25'] = { 'Bias' : 0.13, 'Width' : 2.7 , 'Cut' : -3.7, 'Power' : 6, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_loose_0.10-0.20_20-25'] = { 'Bias' : 0.13, 'Width' : 2.7 , 'Cut' : -3.7, 'Power' : 6, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_loose_0.20-0.30_20-25'] = { 'Bias' : 0.01, 'Width' : 2.7 , 'Cut' : -5.4, 'Power' : 30, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_loose_0.30-0.40_20-25'] = { 'Bias' : 0.01, 'Width' : 2.7 , 'Cut' : -4.3, 'Power' : 7, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_loose_0.40-0.80_20-25'] = { 'Bias' : -0.5, 'Width' : 2.7 , 'Cut' : -6, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_loose_0.80-1.20_20-25'] = { 'Bias' : -0.5, 'Width' : 2.7 , 'Cut' : -6, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_loose_1.20-1.60_20-25'] = { 'Bias' : -0.5, 'Width' : 2.7 , 'Cut' : -6, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_loose_1.60-1.80_20-25'] = { 'Bias' : -0.5, 'Width' : 2.7 , 'Cut' : -6, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_loose_1.80-2.10_20-25'] = { 'Bias' : -1.3, 'Width' : 3.3 , 'Cut' : -6, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_2.10-2.30_20-25'] = { 'Bias' : -1.3, 'Width' : 3.3 , 'Cut' : -6, 'Power' : 5, 'cms_alpha' : 60, 'cms_beta' : 0.07, 'cms_gamma' : 0.04, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_2.30-2.50_20-25'] = { 'Bias' : 0.1, 'Width' : 3.3 , 'Cut' : -6, 'Power' : 10, 'cms_alpha' : 60, 'cms_beta' : 0.1, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 140}

    alts['bw_cmsshape']['hist_ee_loose_0.30-0.40_100-200'] = { 'Bias' : 0.7, 'Width' : 1.5 , 'Cut' : -2.5, 'Power' : 20, 'cms_alpha' : 200, 'cms_beta' : 0.007, 'cms_gamma' : 0.01, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 140}

    alts['bw_cmsshape']['hist_ee_loose_1.60-1.80_200-1000000'] = { 'Bias' : 1.2, 'Width' : 2 , 'Cut' : -7, 'Power' : 28, 'cms_alpha' : 90, 'cms_beta' : 0.026, 'cms_gamma' : 0.01, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_loose_1.80-2.50_200-1000000'] = { 'Bias' : 1.2, 'Width' : 2 , 'Cut' : -7, 'Power' : 28, 'cms_alpha' : 90, 'cms_beta' : 0.026, 'cms_gamma' : 0.01, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 140}

    # --------------------------------- 
    # ee loose
    # --------------------------------- 
    alts['bw_cmsshape']['hist_ee_obj_0.00-0.10_10-15'] = { 'Bias' : -0.1, 'Width' : 2.8 , 'Cut' : -6.4, 'Power' : 20, 'cms_alpha' : 50, 'cms_beta' : 0.05, 'cms_gamma' : 0.06, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_obj_0.10-0.20_10-15'] = { 'Bias' : -0.1, 'Width' : 2.8 , 'Cut' : -6.4, 'Power' : 20, 'cms_alpha' : 50, 'cms_beta' : 0.05, 'cms_gamma' : 0.06, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_obj_0.40-0.80_10-15'] = { 'Bias' : -0.4, 'Width' : 3 , 'Cut' : -8.0, 'Power' : 30, 'cms_alpha' : 50, 'cms_beta' : 0.01, 'cms_gamma' : 0.06, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_obj_0.80-1.20_10-15'] = { 'Bias' : -0.4, 'Width' : 3 , 'Cut' : -8.0, 'Power' : 30, 'cms_alpha' : 50, 'cms_beta' : 0.01, 'cms_gamma' : 0.06, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_obj_1.20-1.60_10-15'] = { 'Bias' : -0.4, 'Width' : 3 , 'Cut' : -8.0, 'Power' : 30, 'cms_alpha' : 50, 'cms_beta' : 0.01, 'cms_gamma' : 0.06, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_obj_1.60-1.80_10-15'] = { 'Bias' : -0.4, 'Width' : 3 , 'Cut' : -8.0, 'Power' : 30, 'cms_alpha' : 50, 'cms_beta' : 0.01, 'cms_gamma' : 0.06, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' : 160}
    alts['bw_cmsshape']['hist_ee_obj_1.80-2.10_10-15'] = { 'Bias' : -2, 'Width' : 3 , 'Cut' : -1.5, 'Power' : 30, 'cms_alpha' : 30, 'cms_beta' : 0.2, 'cms_gamma' : 0.02, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_obj_2.10-2.30_10-15'] = { 'Bias' : -1, 'Width' : 3.5 , 'Cut' : -1.5, 'Power' : 30, 'cms_alpha' : 40, 'cms_beta' : 0.2, 'cms_gamma' : 0.02, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}
    alts['bw_cmsshape']['hist_ee_obj_2.30-2.50_10-15'] = { 'Bias' : -0.3, 'Width' : 3.5 , 'Cut' : -5, 'Power' : 10, 'cms_alpha' : 50, 'cms_beta' : 0.2, 'cms_gamma' : 0.02, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 140}

    if histname in alts[type] :
        return alts[type][histname]
    else :
        return defaults[type]


def main() :

    # Parse command-line options
    from argparse import ArgumentParser
    p = ArgumentParser()
    
    p.add_argument('--outputDir',default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
    p.add_argument('--photon',   default=False,  action='store_true' ,        dest='photon',         help='run photon SF')
    p.add_argument('--muon',     default=False,  action='store_true' ,        dest='muon',         help='run muon SF')
    p.add_argument('--electron', default=False,  action='store_true' ,        dest='electron',         help='run electron SF')
    
    options = p.parse_args()
    
    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)
    else :
        ROOT.gROOT.SetBatch(False)

    global sampManMMG
    global sampManMM
    global sampManEE

    base_dir_mmg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaNoPhID_2014_12_23'
    base_dir_mm  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPMuMu_2014_11_27'
    base_dir_ee  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPElEl_2014_11_27'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'
    xsFile = 'cross_sections/wgamgam.py'
    lumi = 19400

    sampManMMG = SampleManager(base_dir_mmg, treeName=treename,filename=filename, xsFile=xsFile, lumi=lumi)
    sampManMM = SampleManager(base_dir_mm, treeName=treename,filename=filename, xsFile=xsFile, lumi=lumi)
    sampManEE = SampleManager(base_dir_ee, treeName=treename,filename=filename, xsFile=xsFile, lumi=lumi)

    #samplesConf = 'Modules/Wgamgam.py'
    samplesConf = 'Modules/TAndPSampleConf.py'

    sampManMMG.ReadSamples( samplesConf )
    sampManMM.ReadSamples( samplesConf )
    sampManEE.ReadSamples( samplesConf )

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )
        
    if options.photon : 

        subdir = 'PhotonEfficiencies'
        outputDir = options.outputDir + '/' + subdir

        eff_medium_data, eff_medium_data_count = GetPhotonEfficiencies( data_sample='Muon'       , numerator='mmg_medium', denominator='mmg_loose', doNDKeys=True, outputDir=outputDir+'/Data' )
        eff_eveto_data , eff_eveto_data_count  = GetPhotonEfficiencies( data_sample='Muon'       , numerator='mmg_eveto', denominator='mmg_medium', doNDKeys=True, outputDir=outputDir+'/Data' )
        eff_medium_mc  , eff_medium_mc_count   = GetPhotonEfficiencies( data_sample='ZjetsZgamma', numerator='mmg_medium', denominator='mmg_loose', doNDKeys=True, outputDir=outputDir+'/MC' )
        eff_eveto_mc   , eff_eveto_mc_count    = GetPhotonEfficiencies( data_sample='ZjetsZgamma', numerator='mmg_eveto', denominator='mmg_medium', doNDKeys=True, outputDir=outputDir+'/MC' )

        eff_medium_data_llcut, eff_medium_data_llcut_count = GetPhotonEfficiencies( data_sample='Muon'       , numerator='mmg_medium_llcut', denominator='mmg_loose_llcut', doNDKeys=True, outputDir=outputDir+'/DataLLCut' )
        eff_eveto_data_llcut , eff_eveto_data_llcut_count  = GetPhotonEfficiencies( data_sample='Muon'       , numerator='mmg_eveto_llcut', denominator='mmg_medium_llcut', doNDKeys=True, outputDir=outputDir+'/DataLLCut' )
        eff_medium_mc_llcut  , eff_medium_mc_llcut_count   = GetPhotonEfficiencies( data_sample='ZjetsZgamma', numerator='mmg_medium_llcut', denominator='mmg_loose_llcut', doNDKeys=True, outputDir=outputDir+'/MCLLCut' )
        eff_eveto_mc_llcut   , eff_eveto_mc_llcut_count    = GetPhotonEfficiencies( data_sample='ZjetsZgamma', numerator='mmg_eveto_llcut', denominator='mmg_medium_llcut', doNDKeys=True, outputDir=outputDir+'/MCLLCut' )

        print 'Eveto data '
        for bin, eff in eff_eveto_data.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'Eveto data  count'
        for bin, eff in eff_eveto_data_count.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'medium data '
        for bin, eff in eff_medium_data.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'medium data  count'
        for bin, eff in eff_medium_data_count.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'Eveto MC '
        for bin, eff in eff_eveto_mc.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'Eveto MC  count'
        for bin, eff in eff_eveto_mc_count.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'medium MC '
        for bin, eff in eff_medium_mc.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'medium MC  count'
        for bin, eff in eff_medium_mc_count.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'Eveto data llcut'
        for bin, eff in eff_eveto_data_llcut.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'Eveto data llcut count'
        for bin, eff in eff_eveto_data_llcut_count.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'medium data llcut'
        for bin, eff in eff_medium_data_llcut.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'medium data llcut count'
        for bin, eff in eff_medium_data_llcut_count.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'Eveto MC llcut'
        for bin, eff in eff_eveto_mc_llcut.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'Eveto MC llcut count'
        for bin, eff in eff_eveto_mc_llcut_count.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'medium MC llcut'
        for bin, eff in eff_medium_mc_llcut.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        print 'medium MC llcut count'
        for bin, eff in eff_medium_mc_llcut_count.iteritems() :
            print 'Bin = %s, eff = %s' %(bin, eff)

        MakeScaleFactor( eff_medium_data, eff_medium_mc, tag='sf_medium_nom' , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        MakeScaleFactor( eff_eveto_data , eff_eveto_mc , tag='sf_eveto_nom'  , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        MakeScaleFactor( eff_medium_data_llcut, eff_medium_mc_llcut, tag='sf_medium_llcut' , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )
        MakeScaleFactor( eff_eveto_data_llcut , eff_eveto_mc_llcut , tag='sf_eveto_llcut'  , binning=_photon_hist_eta_pt_bins, outputDir=outputDir )

    if options.muon :
        subdir = 'MuonEfficiencies'
        outputDirData = None
        outputDirDataMCSig = None
        outputDirMC = None
        outputDirDY = None
        outptuDirBase = None
        if options.outputDir is not None :
            outputDirBase = options.outputDir + '/' + subdir
            outputDirData = options.outputDir + '/' + subdir + '/Data'
            outputDirDataMCSig = options.outputDir + '/' + subdir + '/DataMCSig'
            outputDirMC = options.outputDir + '/' + subdir + '/MC'
            outputDirDY = options.outputDir + '/' + subdir + '/DYJetsToLL'

        #res_tight_data, res_trig_data = GetMuonEfficiencies( data_sample='Muon', outputDir=outputDirData )
        #res_tight_mc  , res_trig_mc   = GetMuonEfficiencies( data_sample='AllBkg', outputDir=outputDirMC )
        #res_tight_dy  , res_trig_dy   = GetMuonEfficiencies( data_sample='DYJetsToLL', outputDir=outputDirDY, runFit=False )

        res_tight_mcsig, res_trig_mcsig = GetMuonEfficiencies( data_sample = 'Muon', sig_sample='DYJetsToLL', outputDir=outputDirDataMCSig )

        #MakeScaleFactor( res_tight_data, res_tight_mc, tag='sf_tight_nom' , binning=_lepton_hist_eta_pt_bins, outputDir=outputDirBase )
        #MakeScaleFactor( res_trig_data , res_trig_mc , tag='sf_trig_nom'  , binning=_lepton_hist_eta_pt_bins, outputDir=outputDirBase )
        ##MakeScaleFactor( res_tight_data, res_tight_dy, tag='sf_tight_dymc', binning=_lepton_hist_eta_pt_bins, outputDir=outputDirBase )
        ##MakeScaleFactor( res_trig_data , res_trig_dy , tag='sf_trig_dymc' , binning=_lepton_hist_eta_pt_bins, outputDir=outputDirBase )

    if options.electron :
        subdir = 'ElectronEfficiencies'
        outputDirData = None
        outputDirDataMCSig = None
        outputDirMC = None
        outputDirDY = None
        outputDirBase = None
        if options.outputDir is not None :
            outputDirBase = options.outputDir + '/' + subdir
            outputDirData = options.outputDir + '/' + subdir + '/Data'
            outputDirDataMCSig = options.outputDir + '/' + subdir + '/DataMCSig'
            outputDirMC = options.outputDir + '/' + subdir + '/MC'
            outputDirDY = options.outputDir + '/' + subdir + '/DYJetsToLL'



        #res_loose_data, res_tight_data, res_trig_data = GetElectronEfficiencies( data_sample = 'Electron', outputDir=outputDirData )
        #res_loose_mc  , res_tight_mc  , res_trig_mc   = GetElectronEfficiencies( data_sample = 'AllBkg', outputDir=outputDirMC )
        #res_loose_dy  , res_tight_dy  , res_trig_dy   = GetElectronEfficiencies( data_sample = 'DYJetsToLL', outputDir=outputDirDY, runFit=False )

        res_loose_mcsig, res_tight_mcsig, res_trig_mcsig = GetElectronEfficiencies( data_sample = 'Electron', sig_sample='DYJetsToLL', outputDir=outputDirDataMCSig )

        #MakeScaleFactor( res_loose_data, res_loose_mc, tag='sf_loose_nom', binning=_lepton_hist_eta_pt_bins, outputDir = outputDirBase )
        #MakeScaleFactor( res_tight_data, res_tight_mc, tag='sf_tight_nom', binning=_lepton_hist_eta_pt_bins, outputDir = outputDirBase )
        #MakeScaleFactor( res_trig_data , res_trig_mc , tag='sf_trig_nom' , binning=_lepton_hist_eta_pt_bins, outputDir = outputDirBase )

        ##MakeScaleFactor( res_loose_data, res_loose_dy, tag='sf_loose_dymc', binning=_lepton_hist_eta_pt_bins, outputDir = outputDirBase )
        ##MakeScaleFactor( res_tight_data, res_tight_dy, tag='sf_tight_dymc', binning=_lepton_hist_eta_pt_bins, outputDir = outputDirBase )
        ##MakeScaleFactor( res_trig_data , res_trig_dy, tag='sf_trig_dymc'  , binning=_lepton_hist_eta_pt_bins, outputDir = outputDirBase )
        

    print '^_^ Finished ^_^'
    print 'It is safe to kill the program if it is hanging'
    
def GetElectronEfficiencies( data_sample='Electron', sig_sample=None, outputDir=None, runFit=True ) :

    #eta_bins_lowpt  = [-2.4, -2.3, -2.1, -1.8, -1.6, -1.2, -0.8, -0.4, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.1, 2.3, 2.4]
    #eta_bins_highpt = [-2.4, -1.8, -1.6, -1.2, -0.8, -0.4, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.4]
    eta_bins_lowpt  = [0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.1, 2.3, 2.5]
    eta_bins_highpt = [0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.5]
    low_pt_bins_tight = range( 10, 30, 5) + [30, 40, 50 ] 
    low_pt_bins_trig = range( 24, 30, 2) + [30, 40, 50 ]
    high_pt_bins = [50, 100, 200, 1000000]

    pt_eta_bins_obj   = pair_pt_eta_bins( [ (low_pt_bins_tight, eta_bins_lowpt ), ( high_pt_bins, eta_bins_highpt ) ] )
    pt_eta_bins_tight = pair_pt_eta_bins( [ (low_pt_bins_tight, eta_bins_lowpt ), ( high_pt_bins, eta_bins_highpt ) ] )
    pt_eta_bins_trig  = pair_pt_eta_bins( [ (low_pt_bins_trig, eta_bins_lowpt ), ( high_pt_bins, eta_bins_highpt ) ] )


    drawvar = 'm_eltagprobe:elprobe_pt:fabs(elprobe_eta)'#z,y,x
    fitvar = 'm_eltagprobe'

    results_loose = GetLeptonEfficiency( data_sample, sampManEE, pt_eta_bins_tight, denominator='ee_loose', numerator='ee_obj', drawvar=drawvar, fitvar=fitvar, sig_sample=sig_sample, outputDir=outputDir, runFit=runFit )
    results_tight = GetLeptonEfficiency( data_sample, sampManEE, pt_eta_bins_tight, denominator='ee_obj', numerator='ee_tight', drawvar=drawvar, fitvar=fitvar, sig_sample=sig_sample, outputDir=outputDir, runFit=runFit )
    results_trigger = GetLeptonEfficiency( data_sample, sampManEE, pt_eta_bins_trig, denominator='ee_obj', numerator='ee_trig' , drawvar=drawvar, fitvar=fitvar, sig_sample=sig_sample, outputDir=outputDir, runFit=runFit )

    return results_loose, results_tight, results_trigger

def GetMuonEfficiencies( data_sample='Muon', sig_sample=None, outputDir=None, runFit=True ) :

    #eta_bins_lowpt  = [-2.4, -2.3, -2.1, -1.8, -1.6, -1.2, -0.8, -0.4, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.1, 2.3, 2.4]
    #eta_bins_highpt = [-2.4, -1.8, -1.6, -1.2, -0.8, -0.4, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.4]
    eta_bins_lowpt  = [0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.1, 2.3, 2.4]
    eta_bins_highpt = [0.0, 0.1, 0.2, 0.3, 0.4, 0.8, 1.2, 1.6, 1.8, 2.4]
    low_pt_bins_tight = range( 10, 30, 5) + [30, 40, 50 ] 
    low_pt_bins_trig = [25] + range( 26, 30, 2) + [30, 40, 50 ]
    high_pt_bins = [50, 100, 200, 1000000]

    pt_eta_bins_tight = pair_pt_eta_bins( [ (low_pt_bins_tight, eta_bins_lowpt ), ( high_pt_bins, eta_bins_highpt ) ] )
    pt_eta_bins_trig  = pair_pt_eta_bins( [ (low_pt_bins_trig, eta_bins_lowpt ), ( high_pt_bins, eta_bins_highpt ) ] )

    drawvar = 'm_mutagprobe:muprobe_pt:fabs(muprobe_eta)'#z,y,x
    fitvar  = 'm_mutagprobe'
    
    results_tight = GetLeptonEfficiency( data_sample, sampManMM, pt_eta_bins_tight, denominator='mm_loose', numerator='mm_tight', drawvar=drawvar, fitvar=fitvar, sig_sample=sig_sample, outputDir=outputDir, runFit=runFit )
    results_trigger = GetLeptonEfficiency( data_sample, sampManMM, pt_eta_bins_trig, denominator='mm_loose', numerator='mm_trig' , drawvar=drawvar, fitvar=fitvar, sig_sample=sig_sample, outputDir=outputDir, runFit=runFit)

    return results_tight, results_trigger

def GetLeptonEfficiency( data_sample, sampMan, pt_eta_bins, denominator, numerator, drawvar, fitvar, sig_sample=None, outputDir=None, runFit=True ) :


    m_leplep = ROOT.RooRealVar( fitvar, fitvar, 60, 160 )

    draw_base_den = get_default_draw_commands( denominator )
    draw_base_num = get_default_draw_commands( numerator )

    data_samp = sampMan.get_samples(name=data_sample )
    sig_samp = None
    if sig_sample is not None :
        sig_samp = sampMan.get_samples(name=sig_sample)

    mass_binning = (100, 0, 200 )
    #mass_binning = (5, 0, 200 )

    #eta_pt_bins = ( 12, -2.2, 2.2, 5, 0, 50 )
    hist_eta_pt_mass_bins = _lepton_hist_eta_pt_bins + ( mass_binning[0], mass_binning[1], mass_binning[2]  )

    hist_data_den = clone_sample_and_draw( sampMan, data_samp[0], drawvar, ' ( %s )' %draw_base_den, hist_eta_pt_mass_bins  )
    hist_data_num = clone_sample_and_draw( sampMan, data_samp[0], drawvar, ' ( %s )' %draw_base_num, hist_eta_pt_mass_bins  )

    hist_sig_den=None
    hist_sig_num=None
    if sig_samp is not None :
        hist_sig_den = clone_sample_and_draw( sampMan, sig_samp[0], drawvar, ' ( %s )' %draw_base_den, hist_eta_pt_mass_bins  )
        hist_sig_num = clone_sample_and_draw( sampMan, sig_samp[0], drawvar, ' ( %s )' %draw_base_num, hist_eta_pt_mass_bins  )


    #hist_data_test = clone_sample_and_draw( sampMan, data_samp[0], 'muprobe_pt:muprobe_eta', ' ( %s )' %draw_base_den, eta_pt_bins  )
    #hist_data_test2 = hist_data_den.Project3D( 'yx' )

    fits_den = {}
    fits_num = {}

    counts_num = {}
    counts_den = {}

    all_pt = []
    for ptmin, ptmax in pt_eta_bins.keys() :
        all_pt.append(ptmin)
        all_pt.append(ptmax)

    last_pt = max( all_pt )

    for (ptmin, ptmax), eta_bins in pt_eta_bins.iteritems() :

        # If FindBin is given a value on the boundary it returns
        # the bin above the boundary
        # Therefore the max bin is 1 less than what is returned
        pt_bin_min = hist_data_den.GetYaxis().FindBin( ptmin )
        pt_bin_max = hist_data_den.GetYaxis().FindBin( ptmax ) - 1 

        for etamin, etamax in eta_bins :

            eta_bin_min = hist_data_den.GetXaxis().FindBin( etamin+0.001 )
            eta_bin_max = hist_data_den.GetXaxis().FindBin( etamax+0.001 ) - 1

            print 'ptmin = %d, ptmax = %d, etamin = %f, etamax = %f ' %(ptmin, ptmax, etamin, etamax )
            print 'BIN : ptmin = %d, ptmax = %d, etamin = %d, etamax = %d ' %(pt_bin_min, pt_bin_max, eta_bin_min, eta_bin_max )

            bin = ( str(etamin), str(etamax), str(ptmin), str(ptmax) )

            label_den = 'hist_%s_%.2f-%.2f_%d-%d' %( denominator, etamin, etamax, ptmin, ptmax )
            label_num = 'hist_%s_%.2f-%.2f_%d-%d' %( numerator, etamin, etamax, ptmin, ptmax )

            
            if ptmax == last_pt :
                pt_bin_max = hist_data_den.GetNbinsY()

            hist_proj_den = hist_data_den.ProjectionZ( label_den+'_fit', eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )
            hist_proj_num = hist_data_num.ProjectionZ( label_num+'_fit', eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )

            hist_proj_sig_den = None
            hist_proj_sig_num = None
            if hist_sig_den is not None  :
                hist_proj_sig_den = hist_sig_den.ProjectionZ( label_den+'_sig', eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )
            if hist_sig_num is not None  :
                hist_proj_sig_num = hist_sig_num.ProjectionZ( label_num+'_sig', eta_bin_min, eta_bin_max, pt_bin_min, pt_bin_max )

            err_num = ROOT.Double()
            err_den = ROOT.Double()
            val_num = hist_proj_num.IntegralAndError( hist_proj_num.FindBin( m_leplep.getMin()) , hist_proj_num.FindBin(m_leplep.getMax()), err_num )
            val_den = hist_proj_den.IntegralAndError( hist_proj_den.FindBin( m_leplep.getMin()) , hist_proj_den.FindBin(m_leplep.getMax()), err_den )

            counts_num[bin] = ufloat( val_num, err_num )
            counts_den[bin] = ufloat( val_den, err_den )
            if runFit :

                chi2_den = run_fit( sampMan, hist_proj_den, m_leplep,  mass_binning, sig_hist=hist_proj_sig_den, name=label_den, doNDKeys=False)

                outputNameDen=None
                if outputDir is not None :
                    outputNameDen = outputDir +'/' + label_den
                draw_fitted_results( sampMan.fit_objs['model'], sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], 'Bkg', m_leplep, chi2_den, label_den, outputName=outputNameDen )

                fits_den[bin]= {}
                for name, obj in sampMan.fit_objs.iteritems() :
                    if isinstance( obj, ROOT.RooRealVar ) :
                        fits_den[bin][name] = ufloat( obj.getVal(), obj.getError() )

                chi2_num = run_fit( sampMan, hist_proj_num, m_leplep,  mass_binning, sig_hist=hist_proj_sig_num, name=label_num, doNDKeys=False)
                outputNameNum=None
                if outputDir is not None :
                    outputNameNum = outputDir +'/' + label_num
                draw_fitted_results( sampMan.fit_objs['model'], sampMan.fit_objs['target_data'], sampMan.fit_objs['sig_model'], 'Bkg', m_leplep, chi2_num, label_num, outputName=outputNameNum )

                fits_num[bin]= {}
                for name, obj in sampMan.fit_objs.iteritems() :
                    if isinstance( obj, ROOT.RooRealVar ) :
                        fits_num[bin][name] = ufloat( obj.getVal(), obj.getError() )

    if outputDir is not None :
        ofile = open( '%s/%s_fits_den.pickle' %( outputDir, denominator) , 'w' )
        pickle.dump( fits_den, ofile )
        ofile.close()
        ofile = open( '%s/%s_fits_num.pickle' %( outputDir, numerator) , 'w' )
        pickle.dump( fits_num, ofile )
        ofile.close()

    results_num = {}
    count_results_num = {}

    for bin, res_den in fits_den.iteritems() :
        res_num = fits_num[bin]

        results_num[bin] = res_num['nsig']/res_den['nsig']

    for bin, cres_den in counts_den.iteritems() :
        if cres_den.n != 0 :
            cres_num = counts_num[bin]
            count_results_num[bin] = cres_num/cres_den
        else :
            count_results_num[bin] = ufloat( 0.0, 0.0 )

    hist_eff   = ROOT.TH2F( 'hist_%s' %numerator, 'hist_%s' %numerator, *_lepton_hist_eta_pt_bins )
    hist_count = ROOT.TH2F( 'hist_count_%s' %numerator, 'hist_count_%s' %numerator, *_lepton_hist_eta_pt_bins )

    for (ptmin, ptmax), eta_bins in pt_eta_bins.iteritems() :

        for etamin, etamax in eta_bins :

            bin = ( str(etamin), str(etamax), str(ptmin), str(ptmax) )
            
            eff_num = results_num.get(bin, None )
            eff_count = count_results_num[bin]


            SetHistContentBins( hist_eff, eff_num, etamin, etamax, ptmin, ptmax )
            SetHistContentBins( hist_count, eff_count, etamin, etamax, ptmin, ptmax )


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )
        ofile = ROOT.TFile.Open ( outputDir + '/results_%s.root'%numerator, 'RECREATE' )
        hist_eff.Write()
        hist_count.Write()
        ofile.Close()


    return results_num

def GetPhotonEfficiencies( data_sample, numerator, denominator, doNDKeys=False, llcut=False, outputDir=None ) :

    mass_binning = (100, 0, 200 )
    pt_bins = [15, 25, 40, 70]
    eta_reg = ['EB', 'EE']

    var = 'm_leplepph'
    m_leplepph = ROOT.RooRealVar( var, var, 60, 120 )

    fits_num = {}
    fits_den = {}
    eff    = {}
    eff_count    = {}

    data_samp = sampManMMG.get_samples(name=data_sample )

    for reg in eta_reg :

        if reg == 'EB' :
            etamin = 0.0
            etamax = 1.44
        if reg == 'EE' :
            etamin = 1.57
            etamax = 2.50

        for idx, minpt in enumerate( pt_bins[:-1] ) :
            maxpt = pt_bins[idx+1]

            # bin for storing results
            bin = ( str(etamin), str(etamax), str( minpt), str(maxpt) )

            fits_num[bin] = {}
            fits_den[bin] = {}

            draw_base_num = get_default_draw_commands( numerator )
            draw_full_num = '%s && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d ' %( draw_base_num, reg, minpt, maxpt )
            # if in the last pt bin, use the background shape from the
            # previous bin
            if maxpt == pt_bins[-1] :
                draw_full_num_bkg = '%s && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d ' %( draw_base_num , reg, pt_bins[-3], pt_bins[-2] )
            else :
                draw_full_num_bkg = draw_full_num

            draw_base_den = get_default_draw_commands( denominator )
            draw_full_den = '%s && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d ' %( draw_base_den, reg, minpt, maxpt )
            if maxpt == pt_bins[-1] :
                draw_full_den_bkg = '%s && ph_Is%s[0] && ph_pt[0] > %d && ph_pt[0] < %d ' %( draw_base_den, reg, pt_bins[-3], pt_bins[-2] )
            else :
                draw_full_den_bkg = draw_full_den

            bkg_sample = 'DYJetsToLLPhOlap'

            label_num = 'hist_num_%s_%s_%d-%d' %( numerator, reg, minpt, maxpt )
            label_den = 'hist_den_%s_%s_%d-%d' %( denominator, reg, minpt, maxpt )

            # ----------------------------
            # Numerator
            # ----------------------------
            hist_data_num = clone_sample_and_draw( sampManMMG, data_samp[0], var, 'PUWeight * ( %s )' %draw_full_num, mass_binning )
            hist_data_num.SetName( label_num )

            integerr_num = ROOT.Double()
            integral_num = hist_data_num.IntegralAndError( hist_data_num.FindBin( 76 ), hist_data_num.FindBin( 106 ), integerr_num )

            chi2_num = run_fit( sampManMMG, hist_data_num, m_leplepph,  mass_binning, name=label_num, doNDKeys=doNDKeys, bkg_sample=bkg_sample, draw_base_bkg=draw_full_num_bkg )

            outputNameNum=None
            if outputDir is not None :
                outputNameNum = outputDir +'/' + label_num
                draw_fitted_results( sampManMMG.fit_objs['model'], sampManMMG.fit_objs['target_data'], sampManMMG.fit_objs['sig_model'], 'Bkg', m_leplepph, chi2_num, label_num, outputName=outputNameNum )

            for name, obj in sampManMMG.fit_objs.iteritems() :
                if isinstance( obj, ROOT.RooRealVar ) :
                    fits_num[bin][name] = ufloat( obj.getVal(), obj.getError() )

            hist_data_den = clone_sample_and_draw( sampManMMG, data_samp[0], var, 'PUWeight * ( %s )' %draw_full_den, mass_binning )
            hist_data_den.SetName( label_den )

            integerr_den = ROOT.Double()
            integral_den = hist_data_den.IntegralAndError( hist_data_den.FindBin( 76 ), hist_data_den.FindBin( 106 ), integerr_den )

            chi2_den = run_fit( sampManMMG, hist_data_den , m_leplepph, mass_binning, name=label_den, doNDKeys=doNDKeys, bkg_sample=bkg_sample, draw_base_bkg=draw_full_den_bkg )

            outputNameDen=None
            if outputDir is not None :
                outputNameDen= outputDir +'/' + label_den
            draw_fitted_results( sampManMMG.fit_objs['model'], sampManMMG.fit_objs['target_data'], sampManMMG.fit_objs['sig_model'], 'Bkg', m_leplepph, chi2_den, label_den, outputName=outputNameDen )

            for name, obj in sampManMMG.fit_objs.iteritems() :
                if isinstance( obj, ROOT.RooRealVar ) :
                    fits_den[bin][name] = ufloat( obj.getVal(), obj.getError() )

            print fits_den[bin]
            if fits_den[bin]['nsig'] == 0 :
                eff[bin] = 0
            else :
                eff[bin] = fits_num[bin]['nsig']/fits_den[bin]['nsig']

            eff_count[bin] = ufloat(integral_num, integerr_num)/ufloat(integral_den, integerr_den )

    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

        ofile = open( '%s/%s_fits_den.pickle' %( outputDir, denominator) , 'w' )
        pickle.dump( fits_den, ofile )
        ofile.close()
        ofile = open( '%s/%s_fits_num.pickle' %( outputDir, numerator) , 'w' )
        pickle.dump( fits_num, ofile )
        ofile.close()

        hist_eff = ROOT.TH2F( 'hist_%s' %numerator, 'hist_%s' %numerator, *_photon_hist_eta_pt_bins )

        for reg in eta_reg :

            if reg == 'EB' :
                etamin = 0.0
                etamax = 1.44
            if reg == 'EE' :
                etamin = 1.57
                etamax = 2.50

            for idx, minpt in enumerate( pt_bins[:-1] ) :
                maxpt = pt_bins[idx+1]

                # bin for storing results
                bin = ( str(etamin), str(etamax), str( minpt), str(maxpt) )

                val = eff[bin]

                print 'bin = %s, val = %s' %(bin, val )

                SetHistContentBins( hist_eff, val, etamin, etamax, minpt, maxpt )
        
            ofile = ROOT.TFile.Open ( outputDir + '/results_%s.root'%numerator, 'RECREATE' )
            hist_eff.Write()
            ofile.Close()

    return eff,eff_count


def run_fit( sampMan, hist_data, fit_var, mass_binning, name, doNDKeys=False, sig_hist =None, bkg_sample=None, draw_base_bkg=None ) :

    if sig_hist is not None :

        fit_defs = get_fit_defaults( hist_data.GetName(), useMCSig=True )

        return fit_model_to_data(fit_var, hist_data, fit_defs, sampMan, signal=[sig_hist], background=['cmsshape'], bkg_labels=['Bkg'] )
        

    if doNDKeys :

        orig_tree = sampMan.get_samples(name=bkg_sample )[0].chain
        orig_tree.SetBranchStatus('*', 1)
        tmpfile = ROOT.TFile.Open( '/tmp/jkunkle/tnptmp.root', 'RECREATE' )
        new_tree = orig_tree.CopyTree( draw_base_bkg )

        mu_passtrig25_n  = ROOT.RooRealVar( 'mu_passtrig25_n', 'mu_passtrig25_n', 0, 10 )
        mu_n           = ROOT.RooRealVar( 'mu_n', 'mu_n', 0, 10 )
        ph_n           = ROOT.RooRealVar( 'ph_n', 'ph_n', 0, 10 )
        ph_hasPixSeed  = ROOT.RooRealVar( 'ph_hasPixSeed[0]', 'ph_hasPixSeed[0]', 0, 1 )
        ph_IsEB        = ROOT.RooRealVar( 'ph_IsEB[0]', 'ph_IsEB[0]', 0, 1 )
        ph_IsEE        = ROOT.RooRealVar( 'ph_IsEE[0]', 'ph_IsEE[0]', 0, 1 )
        ph_pt          = ROOT.RooRealVar( 'ph_pt[0]', 'ph_pt[0]', 0, 1000000. )
        dr_ph1_leadLep = ROOT.RooRealVar( 'dr_ph1_leadLep', 'dr_ph1_leadLep', 0, 10 )
        dr_ph1_sublLep = ROOT.RooRealVar( 'dr_ph1_sublLep', 'dr_ph1_sublLep', 0, 10 )
        m_leplep       = ROOT.RooRealVar( 'm_leplep', 'm_leplep', 0, 1000000 )

        data_set = ROOT.RooDataSet( 'dataset_%s' %( name), '', new_tree,ROOT.RooArgSet( fit_var))

        sampMan.fit_objs = {}

        fit_defs = get_fit_defaults( hist_data.GetName(), useMCBkg=True )

        return fit_model_to_data( fit_var, hist_data, fit_defs, sampMan, signal=['bwxcb'], background=[data_set], bkg_labels=['Bkg'] )

    else :

        fit_defs = get_fit_defaults( hist_data.GetName() )

        return fit_model_to_data( fit_var, hist_data, fit_defs, sampMan, signal=['bwxcb'], background=['cmsshape'], bkg_labels=['Bkg'] )

def MakeScaleFactor( numerator, denominator, tag, binning, outputDir=None ) :

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
            scale_factors[bin] = res_num / res_den


    hist_sf = ROOT.TH2F( 'hist_%s' %tag, 'hist_%s' %tag, *binning )

    for bin, sf in scale_factors.iteritems() : 

        etamin = float( bin[0] )
        etamax = float( bin[1] )
        ptmin  = float( bin[2] )
        ptmax  = float( bin[3] )

        SetHistContentBins( hist_sf, sf, etamin, etamax, ptmin, ptmax )


    if outputDir is not None :
        file_sf = ROOT.TFile.Open( '%s/hist_%s.root' %( outputDir, tag ), 'RECREATE' )
        hist_sf.Write()
        file_sf.Close()

        file_pick = open( '%s/results_%s.pickle' %(outputDir, tag), 'w' )
        pickle.dump( scale_factors, file_pick )
        file_pick.close()

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
