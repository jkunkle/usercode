from core import Filter
import os
import sys

def get_remove_filter() :

    return ['.*']

def get_keep_filter() :

    return ['pfMET.*', 'recoPfMET.*', 'pfType01MET.*', 'nVtxBS', 'nMC', 'mcPID', 'mcParentage', 'mcStatus', 'mcMomPID', 'mcGMomPID', 'mcPt', 'mcEta', 'mcPhi', 'mcE', 'nPU', 'puTrue', 'nVtx', 'nVtxBS', 'rho2012', 'isData', 'run', 'event', 'lumis', 'LHE.*', 'pdf']

def config_analysis( alg_list, args ) :

    alg_list.append( build_electron( do_cutflow=False, do_hists=False, evalPID=None, applyCorrections=False ) )

    alg_list.append( build_muon( do_cutflow=False, do_hists=False, evalPID=None, applyCorrections=False ) )

    alg_list.append( build_photon( do_cutflow=False, do_hists=False, evalPID=None, doEVeto=False, applyCorrections=False ) )

    alg_list.append( build_jet( do_cutflow=False, do_hists=False ) )

    # just for pileup reweighting
    alg_list.append( weight_event(args) )

    alg_list.append( Filter( 'BuildTriggerBits' ) )

    trig_filt = Filter('FilterTrigger')
    #trig_filt.cut_trigger = ' ==48 ' #HLT_Photon36_CaloId10_Iso50_Photon22_CaloId10_Iso50_v 
    trig_filt.cut_trigger = '==17 | == 18 | == 19 | == 13 | == 14 | == 9 | == 22 ' # HLT_Ele27_WP80 || HLT_IsoMu24_eta2p1 || HLT_IsoMu24 || HLT_Mu17_TkMu8 || HLT_Mu17_Mu8 || HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL || HLT_Ele17_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_Ele8_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL

    alg_list.append(trig_filt)

def build_muon( do_cutflow=False, do_hists=False, evalPID=None, applyCorrections=False ) :

    filt = Filter('BuildMuon')

    filt.do_cutflow = do_cutflow

    filt.cut_pt         = ' > 5 '

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
    filt.cut_corriso    = ' < 0.12'

    ##filt.cut_trkiso     = ' < 0.1 '

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

    filt.cut_pt = ' > 5'
    filt.cut_abssceta       = ' <2.5 '
    #filt.cut_abssceta       = ' <1.479 '
    #filt.cut_abssceta       = ' >= 1.479 & < 2.5'
    # no crack for now
    #filt.cut_abssceta_crack = ' > 1.4442 & < 1.566 '
    #filt.invert('cut_abssceta_crack')
    #filt.invert('cut_abssceta')

    filt.cut_absdEtaIn_barrel_tight       = ' < 0.004 '
    filt.cut_absdPhiIn_barrel_tight       = ' < 0.03 '
    filt.cut_sigmaIEIE_barrel_tight       = ' < 0.01 '
    filt.cut_hovere_barrel_tight          = ' < 0.12 '
    filt.cut_d0_barrel_tight              = ' < 0.02 '
    filt.cut_z0_barrel_tight              = ' < 0.1 '
    filt.cut_epdiff_barrel_tight          = ' < 0.05 '
    filt.cut_pfIsoCorr30_barrel_tight         = ' < 0.1 '
    filt.cut_convfit_barrel_tight         = ' == 0 '
    filt.cut_misshits_barrel_tight        = ' == 0 '

    filt.cut_absdEtaIn_barrel_medium      = ' < 0.004 '
    filt.cut_absdPhiIn_barrel_medium      = ' < 0.06 '
    filt.cut_sigmaIEIE_barrel_medium      = ' < 0.01 '
    filt.cut_hovere_barrel_medium         = ' < 0.12 '
    filt.cut_d0_barrel_medium             = ' < 0.02 '
    filt.cut_z0_barrel_medium             = ' < 0.1 '
    filt.cut_epdiff_barrel_medium         = ' < 0.05 '
    filt.cut_pfIsoCorr30_barrel_medium        = ' < 0.15 '
    filt.cut_convfit_barrel_medium        = ' == 0 '
    filt.cut_misshits_barrel_medium       = ' <= 1 '

    filt.cut_absdEtaIn_barrel_loose       = ' < 0.007 '
    filt.cut_absdPhiIn_barrel_loose       = ' < 0.15 '
    filt.cut_sigmaIEIE_barrel_loose       = ' < 0.01 '
    filt.cut_hovere_barrel_loose          = ' < 0.12 '
    filt.cut_d0_barrel_loose              = ' < 0.02 '
    filt.cut_z0_barrel_loose              = ' < 0.2 '
    filt.cut_epdiff_barrel_loose          = ' < 0.05 '
    filt.cut_pfIsoCorr30_barrel_loose         = ' < 0.15 '
    filt.cut_convfit_barrel_loose         = ' == 0 '
    filt.cut_misshits_barrel_loose        = ' <= 1 '

    filt.cut_absdEtaIn_barrel_veryloose   = ' < 0.007 '
    filt.cut_absdPhiIn_barrel_veryloose   = ' < 0.8 '
    filt.cut_sigmaIEIE_barrel_veryloose   = ' < 0.01 '
    filt.cut_hovere_barrel_veryloose      = ' < 0.15 '
    filt.cut_d0_barrel_veryloose          = ' < 0.04 '
    filt.cut_z0_barrel_veryloose          = ' < 0.2 '
    #filt.cut_epdiff_barrel_veryloose     = ' < 0.05 ' #no cut
    filt.cut_pfIsoCorr30_barrel_veryloose     = ' < 0.1 '
    #filt.cut_convfit_barrel_veryloose    = ' == 0 ' #no cut
    #filt.cut_misshits_barrel_veryloose   = ' == 0 ' #no cut

    filt.cut_absdEtaIn_barrel_tightTrig   = ' < 0.007 '
    filt.cut_absdPhiIn_barrel_tightTrig   = ' < 0.15 '
    filt.cut_sigmaIEIE_barrel_tightTrig   = ' < 0.01 '
    filt.cut_hovere_barrel_tightTrig      = ' < 0.12 '
    filt.cut_ecalIso30_barrel_tightTrig   = ' < 0.2 '
    filt.cut_hcalIso30_barrel_tightTrig   = ' < 0.2 '
    filt.cut_trkIso30_barrel_tightTrig    = ' < 0.2 '

    filt.cut_absdEtaIn_endcap_tight       = ' < 0.005 '
    filt.cut_absdPhiIn_endcap_tight       = ' < 0.02 '
    filt.cut_sigmaIEIE_endcap_tight       = ' < 0.03 '
    filt.cut_hovere_endcap_tight          = ' < 0.1 '
    filt.cut_d0_endcap_tight              = ' < 0.02 '
    filt.cut_z0_endcap_tight              = ' < 0.1 '
    filt.cut_epdiff_endcap_tight          = ' < 0.05 '
    filt.cut_pfIsoCorr30_endcap_lowPt_tight   = ' < 0.07 '
    filt.cut_pfIsoCorr30_endcap_highPt_tight  = ' < 0.10 '
    filt.cut_convfit_endcap_tight         = ' == 0 '
    filt.cut_misshits_endcap_tight        = ' == 0 '

    filt.cut_absdEtaIn_endcap_medium      = ' < 0.007 '
    filt.cut_absdPhiIn_endcap_medium      = ' < 0.03 '
    filt.cut_sigmaIEIE_endcap_medium      = ' < 0.03 '
    filt.cut_hovere_endcap_medium         = ' < 0.1 '
    filt.cut_d0_endcap_medium             = ' < 0.02 '
    filt.cut_z0_endcap_medium             = ' < 0.1 '
    filt.cut_epdiff_endcap_medium         = ' < 0.05 '
    filt.cut_pfIsoCorr30_endcap_lowPt_medium  = ' < 0.1 '
    filt.cut_pfIsoCorr30_endcap_highPt_medium = ' < 0.15 '
    filt.cut_convfit_endcap_medium        = ' == 0 '
    filt.cut_misshits_endcap_medium       = ' <= 1 '

    filt.cut_absdEtaIn_endcap_loose       = ' < 0.009 '
    filt.cut_absdPhiIn_endcap_loose       = ' < 0.1 '
    filt.cut_sigmaIEIE_endcap_loose       = ' < 0.03 '
    filt.cut_hovere_endcap_loose          = ' < 0.1 '
    filt.cut_d0_endcap_loose              = ' < 0.02 '
    filt.cut_z0_endcap_loose              = ' < 0.2 '
    filt.cut_epdiff_endcap_loose          = ' < 0.05 '
    filt.cut_pfIsoCorr30_endcap_lowPt_loose   = ' < 0.10 '
    filt.cut_pfIsoCorr30_endcap_highPt_loose  = ' < 0.15 '
    filt.cut_convfit_endcap_loose         = ' == 0 '
    filt.cut_misshits_endcap_loose        = ' <= 1 '

    filt.cut_absdEtaIn_endcap_veryloose   = ' < 0.01 '
    filt.cut_absdPhiIn_endcap_veryloose   = ' < 0.7 '
    filt.cut_sigmaIEIE_endcap_veryloose   = ' < 0.03 '
    #filt.cut_hovere_endcap_veryloose      = ' < 0.15 ' #no cut
    filt.cut_d0_endcap_veryloose          = ' < 0.04 '
    filt.cut_z0_endcap_veryloose          = ' < 0.2 '
    #filt.cut_epdiff_endcap_veryloose     = ' < 0.05 ' #no cut
    filt.cut_pfIsoCorr30_endcap_veryloose     = ' < 0.15 '
    #filt.cut_convfit_endcap_veryloose    = ' == 0 ' #no cut
    #filt.cut_misshits_endcap_veryloose   = ' == 0 ' #no cut

    filt.cut_absdEtaIn_endcap_tightTrig    = ' < 0.009 '
    filt.cut_absdPhiIn_endcap_tightTrig    = ' < 0.10 '
    filt.cut_sigmaIEIE_endcap_tightTrig    = ' < 0.03 '
    filt.cut_hovere_endcap_tightTrig       = ' < 0.1 '
    filt.cut_ecalIso30_endcap_tightTrig    = ' < 0.2 '
    filt.cut_hcalIso30_endcap_tightTrig    = ' < 0.2 '
    filt.cut_trkIso30_endcap_tightTrig     = ' < 0.2 '

    filt.cut_mva_central_lowpt_mvatrig     = ' > 0.0 '
    filt.cut_mva_crack_lowpt_mvatrig       = ' > 0.1 '
    filt.cut_mva_endcap_lowpt_mvatrig      = ' > 0.62 '
    filt.cut_mva_central_highpt_mvatrig    = ' > 0.94 '
    filt.cut_mva_crack_highpt_mvatrig      = ' > 0.85 '
    filt.cut_mva_endcap_highpt_mvatrig     = ' > 0.92 '
    
    filt.cut_relpfiso_mvatrig              = ' < 0.15 '
    filt.cut_misshits_mvatrig              = ' == 0 '
    filt.cut_convfit_mvatrig               = ' == 0 ' 

    filt.cut_mva_central_lowpt_mvanontrig  = ' > 0.47 '
    filt.cut_mva_crack_lowpt_mvanontrig    = ' > 0.004 '
    filt.cut_mva_endcap_lowpt_mvanontrig   = ' > 0.295 '
    filt.cut_mva_central_highpt_mvanontrig = ' > -0.34 '
    filt.cut_mva_crack_highpt_mvanontrig   = ' > -0.65 '
    filt.cut_mva_endcap_highpt_mvanontrig  = ' > 0.6 '
    
    filt.cut_relpfiso_mvanontrig           = ' < 0.4 '
    filt.cut_misshits_mvanontrig           = ' < 2 '
    filt.cut_sip_mvanontrig                = ' < 4' 

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
        filt.add_hist( 'cut_epdiff_barrel_tight', 100, 0, 1 )
        filt.add_hist( 'cut_pfIso30_barrel_tight', 100, 0, 10 )
        filt.add_hist( 'cut_convfit_barrel_tight', 2, 0, 2 )
        filt.add_hist( 'cut_misshits_barrel_tight', 10, 0, 10 )

        filt.add_hist( 'cut_mva_central_lowpt_mvatrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_crack_lowpt_mvatrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_endcap_lowpt_mvatrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_central_highpt_mvatrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_crack_highpt_mvatrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_endcap_highpt_mvatrig', 50, -1, 1 )
        
        filt.add_hist( 'cut_relpfiso_mvatrig', 50, 0, 5 )
        filt.add_hist( 'cut_misshits_mvatrig', 10, 0, 10 )
        filt.add_hist( 'cut_convfit_mvatrig', 2, 0, 1 )

        filt.add_hist( 'cut_mva_central_lowpt_mvanontrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_crack_lowpt_mvanontrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_endcap_lowpt_mvanontrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_central_highpt_mvanontrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_crack_highpt_mvanontrig', 50, -1, 1 )
        filt.add_hist( 'cut_mva_endcap_highpt_mvanontrig', 50, -1, 1 )
        
        filt.add_hist( 'cut_relpfiso_mvanontrig', 50, 0, 5 )
        filt.add_hist( 'cut_misshits_mvanontrig', 10, 0, 10 )
        filt.add_hist( 'cut_sip_mvanontrig', 50, 0, 10 )

    return filt

def build_photon( do_cutflow=False, do_hists=False, filtPID=None, evalPID=None, doEVeto=True, applyCorrections=False ) :

    filt = Filter('BuildPhoton')

    filt.do_cutflow = do_cutflow

    filt.cut_pt           = ' > 10 '
    filt.cut_abseta       = ' < 2.5'
    filt.cut_abseta_crack = ' > 1.44 & < 1.57 '
    filt.invert('cut_abseta_crack')

    #filt.cut_hovere       = ' < 0.05'
    if doEVeto :
        filt.cut_eveto        = ' == False'

    filt.cut_sigmaIEIE_barrel_loose  = ' < 0.012 '
    filt.cut_chIsoCorr_barrel_loose  = ' < 2.6 '
    filt.cut_neuIsoCorr_barrel_loose = ' < 3.5 '
    filt.cut_phoIsoCorr_barrel_loose = ' < 1.3 '
    filt.cut_hovere_barrel_loose = ' < 0.05 '

    filt.cut_sigmaIEIE_endcap_loose  = ' < 0.034 '
    filt.cut_chIsoCorr_endcap_loose  = ' < 2.3 '
    filt.cut_neuIsoCorr_endcap_loose = ' < 2.9 '
    # no cut for loose
    #filt.cut_phoIsoCorr_endcap_loose = ' < 1.0 '
    filt.cut_hovere_endcap_loose = ' < 0.05 '

    filt.cut_sigmaIEIE_barrel_medium  = ' < 0.011 '
    filt.cut_chIsoCorr_barrel_medium  = ' < 1.5 '
    filt.cut_neuIsoCorr_barrel_medium = ' < 1.0 '
    filt.cut_phoIsoCorr_barrel_medium = ' < 0.7 '
    filt.cut_hovere_barrel_medium = ' < 0.05 '

    filt.cut_sigmaIEIE_endcap_medium  = ' < 0.033 '
    filt.cut_chIsoCorr_endcap_medium  = ' < 1.2 '
    filt.cut_neuIsoCorr_endcap_medium = ' < 1.5 '
    filt.cut_phoIsoCorr_endcap_medium = ' < 1.0 '
    filt.cut_hovere_endcap_medium = ' < 0.05 '

    filt.cut_sigmaIEIE_barrel_tight  = ' < 0.011 '
    filt.cut_chIsoCorr_barrel_tight  = ' < 0.7 '
    filt.cut_neuIsoCorr_barrel_tight = ' < 0.4 '
    filt.cut_phoIsoCorr_barrel_tight = ' < 0.5 '
    filt.cut_hovere_barrel_tight = ' < 0.05 '

    filt.cut_sigmaIEIE_endcap_tight  = ' < 0.031 '
    filt.cut_chIsoCorr_endcap_tight  = ' < 0.5 '
    filt.cut_neuIsoCorr_endcap_tight = ' < 1.5 '
    filt.cut_phoIsoCorr_endcap_tight = ' < 1.0 '
    filt.cut_hovere_endcap_tight = ' < 0.05 '

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

    if applyCorrections :
        workarea = os.getenv('WorkArea')
        filt.add_var('applyCorrections', 'true' )
        filt.add_var('correctionFile', '%s/TreeFilter/RecoWgg/data/step2-invMass_SC-loose-Et_20-trigger-noPF-HggRunEtaR9.dat' %workarea )
        filt.add_var('smearingFile', '%s/TreeFilter/RecoWgg/data/outFile-step4-invMass_SC-loose-Et_20-trigger-noPF-HggRunEtaR9-smearEle.dat' %workarea )

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

def build_jet( do_cutflow=False, do_hists=False ) :

    filt = Filter('BuildJet')
    filt.do_cutflow = do_cutflow

    filt.cut_pt = ' > 25 '
    filt.cut_abseta = ' < 4.5 '

    #filt.cut_jet_el_dr = ' > 0.4 '
    #filt.cut_jet_ph_dr = ' > 0.4 '

    if do_hists :
        filt.add_hist( 'cut_pt', 100, 0, 500 )
        filt.add_hist( 'cut_abseta', 50, 0, 5 )

    return filt

def weight_event( args ) :

    filt = Filter( 'WeightEvent' )

    if 'sampleFile' not in args :
        print 'weight_event requires as a command line argument like --moduleArgs " { \'sampleFile\' : \'/path/histograms.root\'} "'
        sys.exit(-1)

    sample_hist = 'ggNtuplizer/hPUTrue'
    if 'sample_hist' in args :
        sample_hist = args['sampleHist']
    
    workarea = os.getenv('WorkArea')

    filt.add_var('sample_file', args['sampleFile'])
    filt.add_var('data_file', '%s/TreeFilter/RecoWgg/data/run2012ABCD_pileup_true.root' %workarea )
    filt.add_var('sample_hist', sample_hist)
    filt.add_var('data_hist', 'pileup')

    return filt

