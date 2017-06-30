import inspect
import sys
import os
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

    return ['passTrig.*']

def config_analysis( alg_list, options ) :
    """ Configure analysis modules. Order is preserved """

    # run on the function provided through
    # the args
    for s in inspect.getmembers(sys.modules[__name__]) :
        if s[0] in options['functions'].split(',') :
            print '*********************************'
            print 'RUN %s' %( s[0] )
            print '*********************************'
            addtl_args = options.get( 'args', {} )
            func_algs = s[1]( addtl_args )
            if not isinstance( func_algs, list ) :
                func_algs = [func_algs]
            alg_list += func_algs

    print alg_list
    

def MakeGJNtuple(options) :

    alg_list = []

    filter_event = Filter('FilterEvent')
    filter_event.cut_ph_n = ' > 1'
    filter_event.cut_ph_medium_n = ' > 0 '

    alg_list.append( filter_event )

    make_ntuple = Filter( 'MakeGJNtuple' )
    alg_list.append( make_ntuple )

    return alg_list

def MakeZmumuNtuple( options ) :

    alg_list = []

    filter_event = Filter('FilterEvent')
    filter_event.cut_ph_n = ' > 0 '
    filter_event.cut_mu_n = ' == 2 '

    alg_list.append( filter_event )

    make_ntuple = Filter( 'MakeZmumuNtuple' )
    alg_list.append( make_ntuple )

    return alg_list


def MakeWmunuNtuple( options ) :

    alg_list = []

    filter_event = Filter('FilterEvent')
    filter_event.cut_ph_n = ' > 0 '
    filter_event.cut_mu_n = ' == 1 '

    alg_list.append( filter_event )

    make_ntuple = Filter( 'MakeWmunuNtuple' )
    alg_list.append( make_ntuple )

    return alg_list


def MakeQCDNtuple( options ) :

    alg_list = []

    filter_event = Filter('FilterEvent')
    filter_event.cut_ph_n = ' > 0 '

    alg_list.append( filter_event )

    make_ntuple = Filter( 'MakeQCDNtuple' )
    alg_list.append( make_ntuple )

    return alg_list




