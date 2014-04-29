from core import Filter
import os
import sys

def get_remove_filter() :

    return ['.*']

def get_keep_filter() :

    return []

def config_analysis( alg_list, args ) :

    alg_list.append( build_photon( do_cutflow=False, do_hists=False, evalPID=None) )

    # just for pileup reweighting
    alg_list.append( weight_event(args) )

def build_photon( do_cutflow=False, do_hists=False, filtPID=None, evalPID=None ) :

    filt = Filter('BuildPhoton')

    filt.do_cutflow = do_cutflow

    filt.cut_pt           = ' > 15 '
    filt.cut_abseta       = ' < 2.5'
    filt.cut_abseta_crack = ' > 1.479 & < 1.566 '
    filt.invert('cut_abseta_crack')

    filt.cut_hovere       = ' < 0.05'
    filt.cut_eveto        = ' == False'

    filt.cut_sigmaIEIE_barrel_loose  = ' < 0.012 '
    filt.cut_chIsoCorr_barrel_loose  = ' < 2.6 '
    filt.cut_neuIsoCorr_barrel_loose = ' < 3.5 '
    filt.cut_phoIsoCorr_barrel_loose = ' < 1.3 '

    filt.cut_sigmaIEIE_endcap_loose  = ' < 0.034 '
    filt.cut_chIsoCorr_endcap_loose  = ' < 2.3 '
    filt.cut_neuIsoCorr_endcap_loose = ' < 2.9 '
    # no cut for loose
    #filt.cut_phoIsoCorr_endcap_loose = ' < 1.0 '

    filt.cut_sigmaIEIE_barrel_medium  = ' < 0.011 '
    filt.cut_chIsoCorr_barrel_medium  = ' < 1.5 '
    filt.cut_neuIsoCorr_barrel_medium = ' < 1.0 '
    filt.cut_phoIsoCorr_barrel_medium = ' < 0.7 '

    filt.cut_sigmaIEIE_endcap_medium  = ' < 0.033 '
    filt.cut_chIsoCorr_endcap_medium  = ' < 1.2 '
    filt.cut_neuIsoCorr_endcap_medium = ' < 1.5 '
    filt.cut_phoIsoCorr_endcap_medium = ' < 1.0 '

    filt.cut_sigmaIEIE_barrel_tight  = ' < 0.011 '
    filt.cut_chIsoCorr_barrel_tight  = ' < 0.7 '
    filt.cut_neuIsoCorr_barrel_tight = ' < 0.4 '
    filt.cut_phoIsoCorr_barrel_tight = ' < 0.5 '

    filt.cut_sigmaIEIE_endcap_tight  = ' < 0.031 '
    filt.cut_chIsoCorr_endcap_tight  = ' < 0.5 '
    filt.cut_neuIsoCorr_endcap_tight = ' < 1.5 '
    filt.cut_phoIsoCorr_endcap_tight = ' < 1.0 '

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

