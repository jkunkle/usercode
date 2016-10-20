from core import Filter
import os
import sys

def get_remove_filter() :

    return ['.*']

def get_keep_filter() :

    #return ['Evt.*', 'MET.*', 'GPdf.*', 'GPhotPt', 'GPhotEta', 'GPhotPhi', 'GPhotE' ,'GPhotSt', 'GPhotMotherId']
    return ['Evt.*', 'GPdf.*', 'GPhot.*']

def config_analysis( alg_list, args ) :

    alg_list.append( Filter( 'BuildMuon' ) )

    alg_list.append( build_electron( do_cutflow=False, do_hists=False, evalPID=None, applyCorrections=False ) )

    alg_list.append( build_muon( do_cutflow=False, do_hists=False, evalPID=None, applyCorrections=False ) )

    alg_list.append( build_photon( do_cutflow=False, do_hists=False, evalPID=None, doEVeto=False, applyCorrections=False ) )

    alg_list.append( build_jet( do_cutflow=False, do_hists=False ) )

    alg_list.append( Filter('BuildMET') )

    alg_list.append( Filter('BuildTruth') )

    alg_list.append( weight_event(args) )

    alg_list.append( Filter( 'BuildTriggerBits' ) )

    gph_filt = Filter( 'FilterGenPhoton' )
    gph_filt.cut_pt = ' > 0.1 '
    alg_list.append(gph_filt)

    #trig_filt = Filter('FilterTrigger')
    ##trig_filt.cut_trigger = ' ==48 ' #HLT_Photon36_CaloId10_Iso50_Photon22_CaloId10_Iso50_v 
    #trig_filt.cut_trigger = '==17 | == 18 | == 19 | == 13 | == 14 | == 9 | == 22 ' # HLT_Ele27_WP80 || HLT_IsoMu24_eta2p1 || HLT_IsoMu24 || HLT_Mu17_TkMu8 || HLT_Mu17_Mu8 || HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL || HLT_Ele17_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_Ele8_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL

    #alg_list.append(trig_filt)

def build_muon( do_cutflow=False, do_hists=False, evalPID=None, applyCorrections=False ) :

    filt = Filter('BuildMuon')

    filt.do_cutflow = do_cutflow

    filt.cut_pt         = ' > 10 '

    filt.cut_isGlobal   = ' == True '
    filt.cut_isPF       = ' == True '
    filt.cut_abseta     = ' < 2.4'
    filt.cut_chi2       = ' < 10'
    filt.cut_nMuonHits  = ' > 0 ' 
    filt.cut_nTrkLayers = ' > 5 ' 
    filt.cut_nStations  = ' > 1'
    filt.cut_nPixelHits = ' > 0'
    filt.cut_d0         = ' < 0.2'
    filt.cut_z0         = ' < 0.5'
    filt.cut_corriso    = ' < 0.25'

    filt.cut_trkiso     = ' < 0.05 '

    if evalPID is not None :
        filt.add_var( 'evalPID', evalPID )

    if applyCorrections :
        filt.add_var( 'applyCorrections', 'true' )

        workarea = os.getenv('WorkArea')
        filt.add_var( 'path', '%s/TreeFilter/RecoWgg/data/MuScleFitCorrector_v4_3/MuScleFit_2012_MC_53X_smearReReco.txt' %workarea )

    if do_hists :
        filt.add_hist( 'cut_pt', 100, 0, 500 )
        filt.add_hist( 'cut_abseta', 50, 0, 5 )
        filt.add_hist( 'cut_chi2', 50, 0, 50 )
        filt.add_hist( 'cut_nTrkLayers', 20, 0, 20 )
        filt.add_hist( 'cut_nStations', 5, 0, 5 )
        filt.add_hist( 'cut_nPixelHits', 20, 0, 20 )
        filt.add_hist( 'cut_d0', 100, -0.05, 0.05 )
        filt.add_hist( 'cut_z0', 100, -0.05, 0.05 )
        filt.add_hist( 'cut_trkiso', 50, 0, 0.5 )
        filt.add_hist( 'cut_corriso', 50, 0, 0.5 )

    return filt

def build_electron( do_cutflow=False, do_hists=False, filtPID=None, evalPID=None, applyCorrections=False ) :

    filt = Filter('BuildElectron')

    filt.do_cutflow = do_cutflow

    filt.cut_pt = ' > 10'
    filt.cut_abssceta       = ' <2.5 '
    #filt.cut_abssceta       = ' <1.479 '
    #filt.cut_abssceta       = ' >= 1.479 & < 2.5'
    # no crack for now
    #filt.cut_abssceta_crack = ' > 1.4442 & < 1.566 '
    #filt.invert('cut_abssceta_crack')
    #filt.invert('cut_abssceta')

    filt.cut_sigmaIEIE_barrel_tight        = ' < 0.0101 '
    filt.cut_absdEtaIn_barrel_tight        = ' < 0.00926 '
    filt.cut_absdPhiIn_barrel_tight        = ' < 0.0336 '
    filt.cut_hovere_barrel_tight           = ' < 0.0597 '
    filt.cut_isoRho_barrel_tight           = ' < 0.0354 '
    filt.cut_ooEmooP_barrel_tight          = ' < 0.012 '
    filt.cut_d0_barrel_tight               = ' < 0.0111 '
    filt.cut_z0_barrel_tight               = ' < 0.0466 '
    filt.cut_misshits_barrel_tight         = ' < 3 '
    filt.cut_passConvVeto_barrel_tight     = ' == 1 '

    filt.cut_sigmaIEIE_barrel_medium       = ' < 0.0101 '
    filt.cut_absdEtaIn_barrel_medium       = ' < 0.0103 '
    filt.cut_absdPhiIn_barrel_medium       = ' < 0.0336 '
    filt.cut_hovere_barrel_medium          = ' < 0.0876 '
    filt.cut_isoRho_barrel_medium          = ' < 0.0766 '
    filt.cut_ooEmooP_barrel_medium         = ' < 0.0174 '
    filt.cut_d0_barrel_medium              = ' < 0.0118 '
    filt.cut_z0_barrel_medium              = ' < 0.373 '
    filt.cut_misshits_barrel_medium        = ' < 3 '
    filt.cut_passConvVeto_barrel_medium    = ' == 1 '

    filt.cut_sigmaIEIE_barrel_loose        = ' < 0.0103 '
    filt.cut_absdEtaIn_barrel_loose        = ' < 0.0105 '
    filt.cut_absdPhiIn_barrel_loose        = ' < 0.115 '
    filt.cut_hovere_barrel_loose           = ' < 0.104 '
    filt.cut_isoRho_barrel_loose           = ' < 0.0893 '
    filt.cut_ooEmooP_barrel_loose          = ' < 0.102 '
    filt.cut_d0_barrel_loose               = ' < 0.0261 '
    filt.cut_z0_barrel_loose               = ' < 0.41 '
    filt.cut_misshits_barrel_loose         = ' < 3 '
    filt.cut_passConvVeto_barrel_loose     = ' == 1 '

    filt.cut_sigmaIEIE_barrel_veryloose    = ' < 0.0114 '
    filt.cut_absdEtaIn_barrel_veryloose    = ' < 0.0152 '
    filt.cut_absdPhiIn_barrel_veryloose    = ' < 0.216 '
    filt.cut_hovere_barrel_veryloose       = ' < 0.181 '
    filt.cut_isoRho_barrel_veryloose       = ' < 0.126 '
    filt.cut_ooEmooP_barrel_veryloose      = ' < 0.207 '
    filt.cut_d0_barrel_veryloose           = ' < 0.0564 '
    filt.cut_z0_barrel_veryloose           = ' < 0.472 '
    filt.cut_misshits_barrel_veryloose     = ' < 3 '
    filt.cut_passConvVeto_barrel_veryloose = ' == 1 '

    filt.cut_sigmaIEIE_endcap_tight        = ' < 0.0279 '
    filt.cut_absdEtaIn_endcap_tight        = ' < 0.00724 '
    filt.cut_absdPhiIn_endcap_tight        = ' < 0.0918 '
    filt.cut_hovere_endcap_tight           = ' < 0.0615 '
    filt.cut_isoRho_endcap_tight           = ' < 0.0646 '
    filt.cut_ooEmooP_endcap_tight          = ' < 0.00999 '
    filt.cut_d0_endcap_tight               = ' < 0.0351 '
    filt.cut_z0_endcap_tight               = ' < 0.417 '
    filt.cut_misshits_endcap_tight         = ' < 2 '
    filt.cut_passConvVeto_endcap_tight     = ' == 1 '

    filt.cut_sigmaIEIE_endcap_medium       = ' < 0.0283 '
    filt.cut_absdEtaIn_endcap_medium       = ' < 0.00733 '
    filt.cut_absdPhiIn_endcap_medium       = ' < 0.114 '
    filt.cut_hovere_endcap_medium          = ' < 0.0678 '
    filt.cut_isoRho_endcap_medium          = ' < 0.0678 '
    filt.cut_ooEmooP_endcap_medium         = ' < 0.0898 '
    filt.cut_d0_endcap_medium              = ' < 0.0739 '
    filt.cut_z0_endcap_medium              = ' < 0.602 '
    filt.cut_misshits_endcap_medium        = ' <  2 '
    filt.cut_passConvVeto_endcap_medium    = ' == 1 '

    filt.cut_sigmaIEIE_endcap_loose        = ' < 0.0301 '
    filt.cut_absdEtaIn_endcap_loose        = ' < 0.00814 '
    filt.cut_absdPhiIn_endcap_loose        = ' < 0.182 '
    filt.cut_hovere_endcap_loose           = ' < 0.0897 '
    filt.cut_isoRho_endcap_loose           = ' < 0.121 '
    filt.cut_ooEmooP_endcap_loose          = ' < 0.126 '
    filt.cut_d0_endcap_loose               = ' < 0.118 '
    filt.cut_z0_endcap_loose               = ' < 0.822 '
    filt.cut_misshits_endcap_loose         = ' <  2 '
    filt.cut_passConvVeto_endcap_loose     = ' == 1 '

    filt.cut_sigmaIEIE_endcap_veryloose    = ' < 0.0352 '
    filt.cut_absdEtaIn_endcap_veryloose    = ' < 0.0113 '
    filt.cut_absdPhiIn_endcap_veryloose    = ' < 0.237 '
    filt.cut_hovere_endcap_veryloose       = ' < 0.116 '
    filt.cut_isoRho_endcap_veryloose       = ' < 0.144 '
    filt.cut_ooEmooP_endcap_veryloose      = ' < 0.174 '
    filt.cut_d0_endcap_veryloose           = ' < 0.222 '
    filt.cut_z0_endcap_veryloose           = ' < 0.921 '
    filt.cut_misshits_endcap_veryloose     = ' < 4 '
    filt.cut_passConvVeto_endcap_veryloose = ' == 1 '


    if filtPID is not None :
        setattr(filt, 'cut_pid_%s' %filtPID, ' == True' )

    if evalPID is not None :
        filt.add_var( 'evalPID', evalPID )

    if applyCorrections :
        workarea = os.getenv('WorkArea')
        filt.add_var('applyCorrections', 'true' )
        filt.add_var('correctionFile', '%s/TreeFilter/RecoWgg/data/step2-invMass_SC-loose-Et_20-trigger-noPF-HggRunEtaR9.dat' %workarea )
        filt.add_var('smearingFile', '%s/TreeFilter/RecoWgg/data/outFile-step4-invMass_SC-loose-Et_20-trigger-noPF-HggRunEtaR9-smearEle.dat' %workarea )


    if do_hists :
        filt.add_hist( 'cut_pt', 100, 0, 500 )
        filt.add_hist( 'cut_abseta', 50, 0, 5 )
        filt.add_hist( 'cut_abseta_crack', 50, 0, 5 )
        filt.add_hist( 'cut_absdEtaIn_barrel_tight', 100, -0.1, 0.1 )
        filt.add_hist( 'cut_absdPhiIn_barrel_tight', 100, -0.1, 0.1 )
        filt.add_hist( 'cut_sigmaIEIE_barrel_tight', 100, 0, 0.05 )
        filt.add_hist( 'cut_hovere_barrel_tight', 100, -1, 1 )
        filt.add_hist( 'cut_d0_barrel_tight', 100, -1, 1 )
        filt.add_hist( 'cut_z0_barrel_tight', 100, -1, 1 )
        filt.add_hist( 'cut_ooEmooP_barrel_tight', 100, 0, 1 )
        filt.add_hist( 'cut_pfIso30_barrel_tight', 100, 0, 10 )
        filt.add_hist( 'cut_passConvVeto_barrel_tight', 2, 0, 2 )
        filt.add_hist( 'cut_misshits_barrel_tight', 10, 0, 10 )

    return filt

def build_photon( do_cutflow=False, do_hists=False, filtPID=None, evalPID=None, doEVeto=True, applyCorrections=False ) :

    filt = Filter('BuildPhoton')

    filt.do_cutflow = do_cutflow

    filt.cut_pt           = ' > 10 '
    filt.cut_abseta       = ' < 2.5'
    filt.cut_abseta_crack = ' > 1.44 & < 1.57 '
    filt.invert('cut_abseta_crack')

    filt.cut_sigmaIEIE_barrel_loose  = ' < 0.0103 '
    filt.cut_chIsoCorr_barrel_loose  = ' < 2.44 '
    filt.cut_neuIsoCorr_barrel_loose = ' < 2.57 '
    filt.cut_phoIsoCorr_barrel_loose = ' < 1.92 '
    filt.cut_hovere_barrel_loose = ' < 0.05 '

    filt.cut_sigmaIEIE_endcap_loose  = ' < 0.0277 '
    filt.cut_chIsoCorr_endcap_loose  = ' < 1.84 '
    filt.cut_neuIsoCorr_endcap_loose = ' < 4.00 '
    filt.cut_phoIsoCorr_endcap_loose = ' < 2.15  '
    filt.cut_hovere_endcap_loose = ' < 0.05 '

    filt.cut_sigmaIEIE_barrel_medium  = ' < 0.010 '
    filt.cut_chIsoCorr_barrel_medium  = ' < 1.31 '
    filt.cut_neuIsoCorr_barrel_medium = ' < 0.60 '
    filt.cut_phoIsoCorr_barrel_medium = ' < 1.33 '
    filt.cut_hovere_barrel_medium = ' < 0.05 '

    filt.cut_sigmaIEIE_endcap_medium  = ' < 0.0267 '
    filt.cut_chIsoCorr_endcap_medium  = ' < 1.25 '
    filt.cut_neuIsoCorr_endcap_medium = ' < 1.65 '
    filt.cut_phoIsoCorr_endcap_medium = ' < 1.02 '
    filt.cut_hovere_endcap_medium = ' < 0.05 '

    filt.cut_sigmaIEIE_barrel_tight  = ' < 0.010 '
    filt.cut_chIsoCorr_barrel_tight  = ' < 0.91 '
    filt.cut_neuIsoCorr_barrel_tight = ' < 0.33 '
    filt.cut_phoIsoCorr_barrel_tight = ' < 0.61 '
    filt.cut_hovere_barrel_tight = ' < 0.05 '

    filt.cut_sigmaIEIE_endcap_tight  = ' < 0.0267 '
    filt.cut_chIsoCorr_endcap_tight  = ' < 0.55 '
    filt.cut_neuIsoCorr_endcap_tight = ' < 0.93 '
    filt.cut_phoIsoCorr_endcap_tight = ' < 0.54 '
    filt.cut_hovere_endcap_tight = ' < 0.05 '

    if filtPID is not None :
        setattr(filt, 'cut_pid_%s' %filtPID, ' == True' )

    if evalPID is not None :
        filt.add_var( 'evalPID', evalPID )

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

def build_jet( do_cutflow=False, do_hists=False ) :

    filt = Filter('BuildJet')
    filt.do_cutflow = do_cutflow

    filt.cut_pt = ' > 30 '
    filt.cut_abseta = ' < 4.5 '

    #filt.cut_jet_el_dr = ' > 0.4 '
    #filt.cut_jet_ph_dr = ' > 0.4 '

    if do_hists :
        filt.add_hist( 'cut_pt', 100, 0, 500 )
        filt.add_hist( 'cut_abseta', 50, 0, 5 )

    return filt

def weight_event( args ) :

    filt = Filter( 'WeightEvent' )

    filt_str = args.get( 'ApplyNLOWeight', 'false' )

    filt.add_var( 'ApplyNLOWeight', filt_str )

    return filt

