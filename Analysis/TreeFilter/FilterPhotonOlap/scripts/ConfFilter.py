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
    filter_event.cut_n_gen_photons = ' < 2 ' #for Wg
    #filter_event.cut_n_gen_photons = ' < 1 ' #for DYJets, WJets, top
    #filter_event.cut_n_gen_photons = ' > 1 ' # to make Zgg
    #filter_event.cut_n_gen_photons = ' > 0 ' # to make Wg backgrounds

    filter_event.add_hist( 'cut_n_gen_photons', 10, 0, 10 )

    filter_event.do_cutflow=True
    alg_list.append( filter_event )

    #filter = Filter('FilterPhotonsMother')
    ##filter.cut_n_ewklepqcd_photons = ' < 2 '
    #filter.cut_n_ewklepqcd_photons_pt15 = ' < 2 '
    #filter.add_hist( 'cut_n_ewklepqcd_photons', 10, 0, 10 )
    #filter.do_cutflow=True

    #alg_list.append(filter)

