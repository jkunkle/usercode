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

    return []

def config_analysis( alg_list ) :
    """ Configure analysis modules. Order is preserved """

    
    # for complicated configurations, define a function
    # that returns the Filter object and append it to the
    # alg list.  Otherwise you can directly append 
    # a Filter object to the list
    # There is no restriction on the naming or inputs to these funtions
    filter_event = Filter('FilterEvent')
    filter_event.cut_n_ph = ' == 2 '
    #filter_event.cut_n_el_passtrig = ' > 0 '

    alg_list.append( filter_event )

    make_ntuple = Filter( 'MakeGGNtuple' )
    #make_ntuple.cut_tag_pt = ' > 27 '
    #make_ntuple.cut_tag_triggerMatch = ' == True '

    alg_list.append( make_ntuple )


