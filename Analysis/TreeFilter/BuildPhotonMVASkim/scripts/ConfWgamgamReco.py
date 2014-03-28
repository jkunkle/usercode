from core import Filter
import os
import sys

def get_remove_filter() :

    return ['.*']

def get_keep_filter() :

    return ['pfMET.*', 'recoPfMET.*', 'nVtxBS', 'nMC', 'mcPID', 'mcParentage', 'mcStatus', 'mcMomPID', 'mcGMomPID', 'mcPt', 'mcEta', 'mcPhi', 'mcE', 'nPU', 'puTrue', 'nVtx', 'nVtxBS']

def config_analysis( alg_list, args ) :

    alg_list.append( build_photon( do_cutflow=False, do_hists=False, evalPID=None) )

def build_photon( do_cutflow=False, do_hists=False, filtPID=None, evalPID=None ) :

    filt = Filter('BuildPhoton')

    filt.do_cutflow = do_cutflow

    filt.cut_hovere12_barrel_mva_presel_smallr9      = ' < 0.075 '
    filt.cut_hcalIsoEtCorr_barrel_mva_presel_smallr9 = ' < 4 '
    filt.cut_trkIsoEtCorr_barrel_mva_presel_smallr9  = ' < 4 '
    filt.cut_hovere12_barrel_mva_presel_larger9      = ' < 0.082 '
    filt.cut_hcalIsoEtCorr_barrel_mva_presel_larger9 = ' < 50 '
    filt.cut_trkIsoEtCorr_barrel_mva_presel_larger9  = ' < 50 '
    filt.cut_sigmaIEIE_barrel_mva_presel             = ' < 0.014 '
    filt.cut_chgpfIso_barrel_mva_presel              = ' < 4 '

    filt.cut_hovere12_endcap_mva_presel_smallr9      = ' < 0.075 '
    filt.cut_hcalIsoEtCorr_endcap_mva_presel_smallr9 = ' < 4 '
    filt.cut_trkIsoEtCorr_endcap_mva_presel_smallr9  = ' < 4 '
    filt.cut_hovere12_endcap_mva_presel_larger9      = ' < 0.075 '
    filt.cut_hcalIsoEtCorr_endcap_mva_presel_larger9 = ' < 50 '
    filt.cut_trkIsoEtCorr_endcap_mva_presel_larger9  = ' < 50 '
    filt.cut_sigmaIEIE_endcap_mva_presel             = ' < 0.034 '
    filt.cut_chgpfIso_endcap_mva_presel              = ' < 4 '

    if filtPID is not None :
        setattr(filt, 'cut_pid_%s' %filtPID, ' == True' )

    if evalPID is not None :
        filt.add_var( 'evalPID', evalPID )

    filt.add_var( 'TMVAWeightsFileEB', '/afs/cern.ch/user/r/rslu/public/photonIDMVA_2014/EB_BDT.weights.xml' )
    filt.add_var( 'TMVAWeightsFileEE', '/afs/cern.ch/user/r/rslu/public/photonIDMVA_2014/EE_BDT.weights.xml' )

    #filt.cut_ph_el_dr = ' > 0.2 '

    if do_hists :
        filt.add_hist( 'cut_pt', 100, 0, 500 )
        filt.add_hist( 'cut_abseta', 50, 0, 5 )
        filt.add_hist( 'cut_abseta_crack', 50, 0, 5 )
        filt.add_hist( 'cut_hovere', 50, 0, 0.1 )
        filt.add_hist( 'cut_eveto', 2, 0, 2 )
        filt.add_hist( 'cut_sigmaIEIE_barrel_medium', 50, 0, 0.05 )
        filt.add_hist( 'cut_chIsoCorr_barrel_medium', 50, 0, 5 )
        filt.add_hist( 'cut_neuIsoCorr_barrel_medium', 50, 0, 5 )
        filt.add_hist( 'cut_phoIsoCorr_barrel_medium', 50, 0, 5 )
        filt.add_hist( 'cut_sigmaIEIE_endcap_medium', 50, 0, 0.05 )
        filt.add_hist( 'cut_chIsoCorr_endcap_medium', 50, 0, 5 )
        filt.add_hist( 'cut_neuIsoCorr_endcap_medium', 50, 0, 5 )
        filt.add_hist( 'cut_phoIsoCorr_endcap_medium', 50, 0, 5 )

        filt.add_hist( 'cut_sigmaIEIE_barrel_loose', 50, 0, 0.05 )
        filt.add_hist( 'cut_chIsoCorr_barrel_loose', 50, 0, 5 )
        filt.add_hist( 'cut_neuIsoCorr_barrel_loose', 100, -5, 5 )
        filt.add_hist( 'cut_phoIsoCorr_barrel_loose', 50, 0, 5 )
        filt.add_hist( 'cut_sigmaIEIE_endcap_loose', 50, 0, 0.05 )
        filt.add_hist( 'cut_chIsoCorr_endcap_loose', 50, 0, 5 )
        filt.add_hist( 'cut_neuIsoCorr_endcap_loose', 100, -5, 5 )
        filt.add_hist( 'cut_phoIsoCorr_endcap_loose', 50, 0, 5 )

    return filt

