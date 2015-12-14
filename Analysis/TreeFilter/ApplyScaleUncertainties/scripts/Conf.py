from core import Filter
import os
import sys
import inspect

_workarea = os.getenv( 'WorkArea' )

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

    return ['.*']

def config_analysis( alg_list, options ) :
    """ Configure analysis modules. Order is preserved """

    print options

    # run on the function provided through
    # the args
    for s in inspect.getmembers(sys.modules[__name__]) :
        if s[0] in options['functions'].split(',') :
            print '*********************************'
            print 'RUN %s' %( s[0] )
            print '*********************************'
            alg_list.append( s[1]( options['args'] ) )

    print alg_list

    #alg_list.append( get_muon_sf() ) 
    #alg_list.append( get_electron_sf() ) 
    #alg_list.append( get_photon_sf() ) 
    #alg_list.append( get_pileup_sf(options) )
    #alg_list.append( Filter ( 'AddMETUncert' ) )

def vary_egamma_scale_up (options) :
    egamma_vary = Filter( 'VaryEGammaScale' )
    egamma_vary.add_var( 'Direction', 'UP' )
    return egamma_vary

def vary_egamma_scale_dn(options) :
    egamma_vary = Filter( 'VaryEGammaScale' )
    egamma_vary.add_var( 'Direction', 'DN' )
    return egamma_vary

def vary_muon_scale_up (options) :
    muon_vary = Filter( 'VaryMuonScale' )
    muon_vary.add_var( 'Direction', 'UP' )
    return muon_vary

def vary_muon_scale_dn(options) :
    muon_vary = Filter( 'VaryMuonScale' )
    muon_vary.add_var( 'Direction', 'DN' )
    return muon_vary

def vary_met_uncert(options) :
    return Filter( 'AddMETUncert' )



