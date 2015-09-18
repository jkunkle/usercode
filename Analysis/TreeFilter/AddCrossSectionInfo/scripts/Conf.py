from core import Filter
import sys
import os

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

    if 'xsFile' not in args :
        print 'A command line argument like --moduleArgs " { \'xsFile\' : \'/afs/cern.ch/user/j/jkunkle/usercode/Plotting/cross_sections/wgamgam.py\'} " is required'
        sys.exit(-1)
    if 'xsKey' not in args :
        print 'A command line argument like --moduleArgs " { \'xsKey\' : \'DYJetsToLL\'} " is required'
        sys.exit(-1)

    file = args['xsFile']
    if not os.path.isfile( file ) :
        print 'Could not locate cross section file.  No values will be loaded.'
        sys.exit(-1)

    ofile = open( file )
    xsdict = eval( ofile.read() )

    sample = args['xsKey']

    values = xsdict.get(sample, None)

    if values is None  :
        print 'Sample %s does not have an entry in the cross section file' %sample
        sys.exit(-1)

    lumi_sample_den = values['cross_section']*values['gen_eff']*values['k_factor']
    if lumi_sample_den == 0 :
        print 'Cannot calculate cross section for %s.' %sample
        sys.exit(-1)
    else :
        lumi_sample = values['n_evt']/float(lumi_sample_den)


    add_weight = Filter('AddWeight')

    print str( lumi_sample )

    add_weight.add_var( 'EffectiveLumi', str( lumi_sample ) )

    alg_list.append( add_weight )

