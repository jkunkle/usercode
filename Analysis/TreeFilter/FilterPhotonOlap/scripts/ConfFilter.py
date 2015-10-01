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

    return []

def config_analysis( alg_list ) :
    """ Configure analysis modules. Order is preserved """

    
    filter_event = Filter('FilterEvent')
    filter_event.cut_n_gen_photons = ' < 2 ' #for Wg, Zg
    #filter_event.cut_n_gen_photons = ' < 1 ' #for DYJets, WJets, top

    # for Zg FSR
    #filter_event.cut_n_gen_photons_pt10 = ' > 1 '

    #filter_event.add_hist( 'cut_n_gen_photons', 10, 0, 10 )

    filter_event.do_cutflow=True
    alg_list.append( filter_event )

