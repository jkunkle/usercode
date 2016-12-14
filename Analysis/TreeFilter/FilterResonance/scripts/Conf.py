from core import Filter

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

    return ['Evt.*', 'GPdf.*', 'el_n', 'mu_n', 'ph_n', 'el_pt', 'el_phi', 'el_eta', 'el_e', 'mu_pt', 'mu_phi', 'mu_eta', 'mu_e', 'ph_pt', 'ph_phi', 'ph_eta', 'ph_e', 'met_pt', 'met_phi']

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    
    alg_list.append( filter_muon( ) )
    alg_list.append( filter_electron( ) )
    alg_list.append( filter_photon( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_el_n = ' == 0 '
    filter_event.cut_mu_n = ' == 1 '
    filter_event.cut_ph_n = ' == 1 '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )


def filter_muon( do_cutflow=False, do_hists=False ) :

    filt = Filter('filter_muon')

    filt.cut_pt           = ' > 25 '
    filt.cut_eta       = ' < 2.5'
    filt.cut_tight       = ' == True '

    return filt

def filter_electron( do_cutflow=False, do_hists=False ) :

    filt = Filter('filter_electron')

    filt.cut_pt           = ' > 25 '
    filt.cut_eta       = ' < 2.5'
    filt.cut_tight       = ' == True '

    return filt

def filter_photon( do_cutflow=False, do_hists=False ) :

    filt = Filter('filter_photon')

    filt.cut_pt           = ' > 25 '
    filt.cut_eta       = ' < 2.5'
    filt.cut_medium       = ' == True '

    return filt

