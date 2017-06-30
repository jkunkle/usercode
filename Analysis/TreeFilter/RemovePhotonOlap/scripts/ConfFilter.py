from core import Filter
import inspect
import sys

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

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    RemoveOlap = Filter( 'RemoveOlap' )

    RemoveOlap.cut_el_ph_dr = ' > 0.4'
    RemoveOlap.cut_trigel_ph_dr = ' > 0.4'

    alg_list.append( RemoveOlap )

    FilterEvent = Filter( 'FilterEvent' )

    FilterEvent.cut_n_ph = ' > 0 '

    alg_list.append( FilterEvent )

