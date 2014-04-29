from core import Filter

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['nVtxBS', 'vtx_n', 'pfMET', 'pfMETPhi', 'PUWeight']

def config_analysis( alg_list ) :
    """ Configure analysis modules. Order is preserved """

    build_photon = Filter('BuildPhoton')
    #build_photon.cut_truth_match = ' == False'
    build_photon.cut_truth_match = ' == True'
    build_photon.cut_truth_match_ptdiff = ' < 5'

    alg_list.append( build_photon )


