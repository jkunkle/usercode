from core import Filter

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['el_mva_trig', 'el_mva_nontrig', 'el_d0pv', 'el_z0pv', 'el_sigmaIEIE',
           'mu_isGlobal', 'mu_isPF', 'mu_chi2', 'mu_nHits', 'mu_nMuStations', 'mu_nPixHits',
           'mu_nTrkLayers', 'mu_d0', 'mu_z0', 'mu_pfIso_ch', 'mu_pfIso_nh', 'mu_pfIso_pho', 
            'mu_pfIso_pu', 'mu_trkIso', 
            'ph_sigmaIEIP', 'ph_r9', 'ph_E1x3', 'ph_E2x2', 'ph_E5x5', 'ph_E2x5Max', 'ph_SCetaWidth',
            'ph_SCphiWidth', 'ph_ESEffSigmaRR', 'ph_hcalIsoDR03', 'ph_trkIsoHollowDR03',
            'ph_chgpfIsoDR02', 'ph_pfChIsoWorst', 'ph_chIso', 'ph_neuIso', 'ph_phoIso', 
            'ph_SCRChIso', 'ph_SCRPhoIso', 'ph_SCRNeuIso', 'ph_SCRChIso04', 'ph_SCRPhoIso04',
            'ph_SCRNeuIso04', 'ph_RandConeChIso', 'ph_RandConePhoIso', 'ph_RandConeNeuIso',
            'ph_RandConeChIso04', 'ph_RandConePhoIso04', 'ph_RandConeNeuIso04', 'ph_drToTrk',
            'ph_conv_nTrk', 'ph_conv_vtx_x', 'ph_conv_vtx_y', 'ph_conv_vtx_z', 
            'ph_conv_ptin1', 'ph_conv_ptin2', 'ph_conv_ptout1', 'ph_conv_ptout2', 'ph_hasSLConv',
           'ph_pass_mva_presel', 'ph_mvascore',
           'jet_NCH', 'jet_Nconstitutents', 'jet_NEF', 'jet_CEF', 'jet_CHF', 'jet_NHF']

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['el_n', 'mu_n', 'ph_n', 'el_pt.*', 'el_eta.*', 'el_phi.*', 'el_e.*', 'mu_pt.*', 'mu_eta.*', 'mu_ph.*i', 'mu_e.*', 'el_pfiso40', 'el_triggerMatch', 'el_passMvaTrig', 'el_passMvaNonTrig', 'mu_corrIso', 'mu_passTightNoIso', 'mu_passTight', 'pfMET']

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    #----------------------------------------
    # Get the isData flag from the args
    # so it isnt used in the args below
    #----------------------------------------
    isData = args.pop('isData', 'False')

    #----------------------------------------
    # lepton and photon filters must be run 
    # before the jet filter
    # to properly handle the overlap removal
    #----------------------------------------

    
    #----------------------------------------
    # Nominal muon filter
    #----------------------------------------
    print 'MUON PT CUT = 10'
    alg_list.append( get_muon_filter( id='Tight',  ptcut=10, etacut=2.4 ) )
    #alg_list.append( get_muon_filter( id='Tight',  ptcut=5, etacut=2.4 ) )

    #----------------------------------------
    # Loose muon filter
    #----------------------------------------
    #print '****************LOOSE MUON ID*************************'
    #alg_list.append( get_muon_filter( id='TightNoIsoNoD0',  ptcut=10 ) )

    #----------------------------------------
    # Nominal electron filter
    #----------------------------------------
    #print '************************************NO ELE ID**********************'
    print 'ELECTRON PT CUT = 10'
    #alg_list.append( get_electron_filter( None, ptcut=10 ) )
    alg_list.append( get_electron_filter( 'mvaNonTrig', ptcut=10, doPhOlapRm=False) )
    #alg_list.append( get_electron_filter( 'loose', ptcut=10, doPhOlapRm=False ) )
    #alg_list.append( get_electron_filter( 'mvaNonTrig', ptcut=5 ) )
    print 'SAVING MVA ELECTRONS'

    #----------------------------------------
    # Other electron filters
    #----------------------------------------
    #alg_list.append( get_electron_filter( 'tightTrig' ) )
    #alg_list.append( get_electron_filter( None ) )

    #----------------------------------------
    # Nominal photon filter with no photon ID
    #----------------------------------------
    print 'PHOTON PT CUT = 15'
    #alg_list.append( get_photon_filter( id=None, eVeto='hasPixSeed', ptcut=15, sort_by_id=True, doElOlapRm=False, doTrigElOlapRm=False, doMuOlapRm=False, doPhOlapRm=False) )
    alg_list.append( get_photon_filter( id=None, eVeto=None, ptcut=15, sort_by_id=True, doElOlapRm=True, doTrigElOlapRm=True) )
    #alg_list.append( get_photon_filter( id='medium', eVeto=None, ptcut=15, sort_by_id=True, doElOlapRm=True, doTrigElOlapRm=True, doMuOlapRm=True, doPhOlapRm=True, olapDR=0.1) )
    print 'SAVING NOID WITH EVETO  PHOTONS, WITH OLAP REMOVAL'

    #----------------------------------------
    # Other photon filters
    #----------------------------------------
    #alg_list.append( get_photon_filter( 'looseNoSIEIE', ptcut=15 ) )
    #alg_list.append( get_photon_filter( id='medium', eVeto=None, ptcut=15, sort_by_id=True ) )
    #alg_list.append( get_photon_filter( id=None, eVeto='hasPixSeed', ptcut=15 ) )
    #alg_list.append( get_photon_filter( id='medium', eVeto='hasPixSeed', ptcut=15, sort_by_id=True) )
    #alg_list.append( get_photon_filter( id=None, eVeto=None, ptcut=15, sort_by_id=True, doElOlapRm=True ) )

    #----------------------------------------
    # Nominal jet filter
    #----------------------------------------
    alg_list.append( get_jet_filter(do_hists=False) )

    #----------------------------------------
    # Calculate event level variables
    #----------------------------------------
    alg_list.append( Filter( 'CalcEventVars' ) )

    #----------------------------------------
    # Calculate truth level variables
    #----------------------------------------
    alg_list.append( Filter( 'BuildTruth' ) )

    #----------------------------------------
    # Set event level cuts that are passed
    # from the scheduler
    #----------------------------------------
    filter_event = Filter('FilterEvent')
    for cut, val in args.iteritems() :
        setattr(filter_event, cut, val)

    alg_list.append( filter_event )

    ##----------------------------------------
    ## Apply blinding
    ## DISABLED
    ##----------------------------------------
    ## Apply blinding
    #filter_blind = Filter( 'FilterBlind' )
    #filter_blind.cut_ph_pt_lead = ' < 40 '
    ##filter_blind.cut_nPhPassMedium = ' < 2 '
    ##filter_blind.cut_m_lepphph= ' > 86.2 & < 96.2  '
    ##filter_blind.cut_m_lepph1= ' > 86.2 & < 96.2  '
    ##filter_blind.cut_m_lepph2= ' > 86.2 & < 96.2  '
    #filter_blind.add_var( 'isData', isData )
    ##alg_list.append(filter_blind)




def get_jet_filter( do_hists = False ) :

    filt = Filter ( 'FilterJet' ) 

    filt.cut_jet_nhf = ' < 0.99 '
    filt.cut_jet_nef = ' < 0.99 '
    filt.cut_jet_chf = ' > 0 '
    filt.cut_jet_cef = ' < 0.99 '
    filt.cut_jet_n_constituents = ' > 1 '
    filt.cut_jet_nch = ' > 0 '

    # redo overlap rm with photons and muons
    filt.cut_jet_ele_dr = ' > 0.4 '
    filt.cut_jet_ph_dr = ' > 0.4 '
    filt.cut_jet_mu_dr = ' > 0.4 '

    filt.do_cutflow = False

    if do_hists :
        filt.add_hist('cut_jet_ele_dr', 50, 0, 5)
        filt.add_hist('cut_jet_ph_dr', 50, 0, 5)
        filt.add_hist('cut_jet_mu_dr', 50, 0, 5)

    return filt

def get_electron_filter ( id, ptcut=10, doPhOlapRm=False ) :

    filt = Filter( 'FilterElectron' )

    #filt.add_var( 'PtScaleDownBarrel', '0.994' )
    #filt.add_var( 'PtScaleDownEndcap', '0.986' )
    #filt.add_var( 'PtScaleUpBarrel', '1.006' )
    #filt.add_var( 'PtScaleUpEndcap', '1.014' )

    filt.cut_el_pt = ' > %d'  %ptcut
    #--------------------------------
    # remove electrons near a muon
    # NOTE -- the muon filter should be
    # run before the electron fitler
    # for the cut to work properly
    #--------------------------------
    filt.cut_mu_el_dr = ' > 0.4 '
    if doPhOlapRm :
        filt.cut_ph_el_dr = ' > 0.4 '

    if id is not None :
        setattr( filt, 'cut_el_%s' %id, ' == True' )

    return filt

def get_photon_filter( id=None, eVeto=None, ptcut=10, sort_by_id='false', doElOlapRm=True, doTrigElOlapRm=True, doMuOlapRm=True, doPhOlapRm=True, olapDR=0.4 ) :

    if sort_by_id == True :
        sort_by_id = 'true'
    if sort_by_id == False :
        sort_by_id = 'false'

    filt = Filter( 'FilterPhoton' )
    filt.cut_ph_pt = ' > %d ' %ptcut

    # reimplement eta cut here to be sure its correct
    # not needed after new Reco samples are made (2014-12-05)
    #filt.cut_ph_abseta       = ' < 2.5'
    #filt.cut_ph_abseta_crack = ' > 1.44 & < 1.57 '
    #filt.invert('cut_ph_abseta_crack')

    if doMuOlapRm :
        filt.cut_mu_ph_dr = ' > %f ' %olapDR
    if doPhOlapRm :
        filt.cut_ph_ph_dr = ' > %f ' %olapDR
    if doElOlapRm :
        filt.cut_el_ph_dr = ' > %f ' %olapDR
    if doTrigElOlapRm :
        filt.cut_trigel_ph_dr = ' > %f ' %olapDR

    #filt.add_var( 'PtScaleDownBarrel', '0.994' )
    #filt.add_var( 'PtScaleDownEndcap', '0.986' )
    #filt.add_var( 'PtScaleUpBarrel', '1.006' )
    #filt.add_var( 'PtScaleUpEndcap', '1.014' )

    if id is not None :
        setattr( filt, 'cut_ph_%s' %id, ' == True' )
    if eVeto is not None :
        setattr( filt, 'cut_ph_%s' %eVeto, ' == False ' )

    filt.sort_by_id = sort_by_id

    return filt


def get_muon_filter( id='Tight', ptcut=10, etacut=2.1 ) :

    filt = Filter( 'FilterMuon' )

    #filt.add_var( 'PtScaleDownBarrel', '0.94' )
    #filt.add_var( 'PtScaleDownEndcap', '0.985' )
    #filt.add_var( 'PtScaleUpBarrel', '1.06' )
    #filt.add_var( 'PtScaleUpEndcap', '1.015' )

    if id is not None :
        setattr(filt,  'cut_mu_pass%s' %id, ' == True' )
    filt.cut_mu_pt = ' > %d' %ptcut
    filt.cut_mu_eta = ' < %.1f '%etacut
    #filt.cut_mu_corriso = ' < 0.2  '

    
    return filt
