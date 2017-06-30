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

    # run on the function provided through
    # the args
    for s in inspect.getmembers(sys.modules[__name__]) :
        if s[0] == args['function'] :
            print '*********************************'
            print 'RUN %s' %( args['function'] )
            print '*********************************'
            s[1]( alg_list, args )



def make_ntuple_invPixLead( alg_list, args ) :

    make_ntuple = Filter( 'RunNtupleProcessing' )

    make_ntuple.cut_nph = ' > 1 '
    make_ntuple.cut_hasPixSeed_leadph12 = ' == True '
    make_ntuple.cut_hasPixSeed_sublph12 = ' == False '
    make_ntuple.cut_eleOlap_leadph12 = ' == True '
    make_ntuple.cut_eleOlap_sublph12 = ' == False '


    alg_list.append( make_ntuple )


def make_ntuple_invPixSubl( alg_list, args ) :

    make_ntuple = Filter( 'RunNtupleProcessing' )

    make_ntuple.cut_nph = ' > 1 '
    make_ntuple.cut_hasPixSeed_leadph12 = ' == False '
    make_ntuple.cut_hasPixSeed_sublph12 = ' == True '
    make_ntuple.cut_eleOlap_leadph12 = ' == False '
    make_ntuple.cut_eleOlap_sublph12 = ' == True '


    alg_list.append( make_ntuple )

def make_ntuple_invPixSinglePhot( alg_list, args ) :

    make_ntuple = Filter( 'RunNtupleProcessing' )

    make_ntuple.cut_nph = ' > 0 '
    make_ntuple.cut_hasPixSeed_singlePhot = ' == True '

    alg_list.append( make_ntuple )




