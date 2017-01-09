from core import Filter
import inspect
import sys

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['.*']

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['Evt.*', 'GPdf.*', 'el_n', 'mu_n', 'ph_n', 'el_pt', 'el_phi', 'el_eta', 'el_e', 'mu_pt', 'mu_phi', 'mu_eta', 'mu_e', 'ph.*', 'met_pt', 'met_phi', 'jet_n', 'jet_pt', 'jet_eta', 'jet_phi', 'jet_e', 'trueph_.*']

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    # run on the function provided through
    # the args
    for s in inspect.getmembers(sys.modules[__name__]) :
        if s[0] == args['function'] :
            print '*********************************'
            print 'RUN %s' %( args['function'] )
            print '*********************************'
            s[1]( alg_list, args )

def make_final_mumu( alg_list, args) :

    mu_pt = args.get( 'mu_pt', ' > 25 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( mu_pt ) )
    alg_list.append( filter_electron( ) )
    alg_list.append( filter_photon( ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_mu_n = ' == 2 '
    filter_event.cut_trig_Mu27_IsoORIsoTk = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )

def make_final_elel( alg_list, args) :

    el_pt = args.get( 'el_pt', ' > 25 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( ) )
    alg_list.append( filter_electron( el_pt ) )
    alg_list.append( filter_photon( ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_el_n = ' == 2 '
    # reenable with new DYJets sample
    #filter_event.cut_trig_Ele27_eta2p1_tight = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )

def make_final_mu( alg_list, args) :

    mu_pt = args.get( 'mu_pt', ' > 25 ' )
    ph_id_cut = args.get( 'ph_id_cut', 'medium' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( mu_pt ) )
    alg_list.append( filter_electron( ) )
    alg_list.append( filter_photon( id_cut=ph_id_cut ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_mu_n = ' == 1 '
    filter_event.cut_trig_Mu27_IsoORIsoTk = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )

def make_final_el( alg_list, args) :

    el_pt = args.get( 'el_pt', ' > 25 ' )
    ph_id_cut = args.get( 'ph_id_cut', 'medium' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( ) )
    alg_list.append( filter_electron( el_pt ) )
    alg_list.append( filter_photon( id_cut=ph_id_cut ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_el_n = ' == 1 '
    filter_event.cut_trig_Ele27_eta2p1_tight = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )

def make_final_elg( alg_list, args) :

    el_pt = args.get( 'el_pt', ' > 25 ' )
    ph_pt = args.get( 'ph_pt', ' > 15 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( ) )
    alg_list.append( filter_electron(el_pt ) )
    alg_list.append( filter_photon( ph_pt ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_el_n = ' == 1 '
    filter_event.cut_mu_n = ' == 0 '
    filter_event.cut_el_pt30_n = ' == 1 '
    filter_event.cut_ph_n = ' == 1 '
    filter_event.cut_trig_Ele27_eta2p1_tight = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )

    filter_blind = Filter( 'FilterBlind' )
    filter_blind.cut_ph_pt_lead = ' < 50 ' 

    filter_blind.add_var( 'isData', args.get('isData', ' == False' ) )
    alg_list.append( filter_blind )

def make_final_mug( alg_list, args) :

    mu_pt = args.get( 'mu_pt', ' > 25 ' )
    ph_pt = args.get( 'ph_pt', ' > 15 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( mu_pt ) )
    alg_list.append( filter_electron( ph_pt ) )
    alg_list.append( filter_photon( ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_mu_n = ' == 1 '
    filter_event.cut_el_n = ' == 0 '
    filter_event.cut_mu_pt30_n = ' == 1 '
    filter_event.cut_ph_n = ' == 1 '
    filter_event.cut_trig_Mu27_IsoORIsoTk = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )

    filter_blind = Filter( 'FilterBlind' )
    filter_blind.cut_ph_pt_lead = ' < 50 ' 

    filter_blind.add_var( 'isData', args.get('isData', ' == False' ) )
    alg_list.append( filter_blind )

def make_final_elgjj( alg_list, args) :

    el_pt = args.get( 'el_pt', ' > 25 ' )
    ph_pt = args.get( 'ph_pt', ' > 15 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( ) )
    alg_list.append( filter_electron(el_pt ) )
    alg_list.append( filter_photon( ph_pt ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_el_n = ' == 1 '
    filter_event.cut_ph_n = ' == 1 '
    filter_event.cut_jet_n = ' > 1 '
    filter_event.cut_trig_Ele27_eta2p1_tight = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )

    filter_blind = Filter( 'FilterBlind' )
    filter_blind.cut_abs_dijet_m_from_z = ' < 15 ' 

    filter_blind.add_var( 'isData', args.get('isData', ' == False' ) )
    alg_list.append( filter_blind )

def make_final_mugjj( alg_list, args) :

    mu_pt = args.get( 'mu_pt', ' > 25 ' )
    ph_pt = args.get( 'ph_pt', ' > 15 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( mu_pt ) )
    alg_list.append( filter_electron( ph_pt ) )
    alg_list.append( filter_photon( ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_mu_n  = ' == 1 '
    filter_event.cut_ph_n  = ' == 1 '
    filter_event.cut_jet_n = ' > 1 '
    filter_event.cut_trig_Mu27_IsoORIsoTk = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )

    filter_blind = Filter( 'FilterBlind' )
    filter_blind.cut_abs_dijet_m_from_z = ' < 15 ' 

    filter_blind.add_var( 'isData', args.get('isData', ' == False' ) )
    alg_list.append( filter_blind )

def filter_muon( mu_pt = ' > 25 ', do_cutflow=False, do_hists=False ) :

    filt = Filter('FilterMuon')

    filt.cut_pt           = mu_pt
    filt.cut_eta       = ' < 2.5'
    filt.cut_tight       = ' == True '

    return filt

def filter_electron( el_pt = ' > 25 ', do_cutflow=False, do_hists=False ) :

    filt = Filter('FilterElectron')

    filt.cut_pt           = el_pt
    filt.cut_eta       = ' < 2.5'
    filt.cut_tight       = ' == True '
    filt.cut_muon_dr    = ' > 0.4 '

    return filt

def filter_photon( ph_pt = ' > 15 ', id_cut='medium', do_cutflow=False, do_hists=False ) :

    filt = Filter('FilterPhoton')

    filt.cut_pt           = ph_pt
    filt.cut_eta       = ' < 2.5'
    filt.cut_muon_dr    = ' > 0.4 '
    filt.cut_electron_dr    = ' > 0.4 '

    if( id_cut is not None ) :
        setattr( filt, 'cut_%s' %id_cut, ' == True ' )
    return filt

def filter_jet( jet_pt = ' > 30 ' ) :

    filt = Filter( 'FilterJet' )

    filt.cut_pt = jet_pt
    filt.cut_muon_dr    = ' > 0.4 '
    filt.cut_electron_dr    = ' > 0.4 '
    filt.cut_photon_dr    = ' > 0.4 '

    return filt

