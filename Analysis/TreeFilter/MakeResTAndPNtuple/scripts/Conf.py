from core import Filter
import sys
import inspect

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
    # run on the function provided through
    # the args
    for s in inspect.getmembers(sys.modules[__name__]) :
        if s[0] == args['function'] :
            print '*********************************'
            print 'RUN %s' %( args['function'] )
            print '*********************************'
            s[1]( alg_list, args )


def makeMCMuon( alg_list, args) :

    filter_evt = Filter( 'FilterEvent' )
    filter_evt.cut_isWMuDecay = ' == True '

    alg_list.append(filter_evt )

    alg_list.append( Filter('BuildMCCommon' ) )
    alg_list.append( Filter('BuildMCMuon' ) )

def makeMCElectron( alg_list, args) :

    filter_evt = Filter( 'FilterEvent' )
    filter_evt.cut_isWElDecay = ' == True '

    alg_list.append(filter_evt )

    alg_list.append( Filter('BuildMCCommon' ) )
    alg_list.append( Filter('BuildMCElectron' ) )


def makeMCPhoton( alg_list, args) :

    useWMu = args.get( 'useWMu', False )
    useWEl = args.get( 'useWEl', False )

    if useWMu == 'False' :
        useWMu = False
    if useWEl == 'False' :
        useWEl = False

    filter_evt = Filter( 'FilterEvent' )

    if useWMu  :
        filter_evt.cut_isWMuDecay = ' == True '
    if useWEl :
        filter_evt.cut_isWElDecay = ' == True '

    alg_list.append(filter_evt )

    alg_list.append( Filter('BuildMCCommon' ) )
    alg_list.append( Filter('BuildMCPhoton' ) )


