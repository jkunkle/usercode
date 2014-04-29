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

    filt = Filter('AddEventWeight')
    filt.cut_elpasstrig_n = ' > 0 '
    filt.cut_el_n = ' > 1 '
    filt.cut_el_biased_pt = ' > 27 '
    filt.cut_el_biased_triggerMatch = ' == True '
    filt.cut_el_biased_passMvaTrig = ' == True '
    #filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/ApplyElToPhFF/data/ElToPhFF.root' )
    #filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/ApplyElToPhFF/data/ElToPhFFNoMassCut.root' )
    #filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/ApplyElToPhFF/data/ElToPhFFNoMassCut2Conv.root' )
    #filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/ApplyElToPhFF/data/ElToPhFFNoMassCut0Conv.root' )
    #filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/ApplyElToPhFF/data/ElToLoosePhFFNewEtaBinMassCut.root' )
    filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/ApplyElToPhFF/data/ElToLoosePhFFNewEtaBin.root' )
    #filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/ApplyElToPhFF/data/ElToLoosePhFFSimpleTEST.root' )
    #filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/ApplyElToPhFF/data/ElToLoosePhFFLowPtTrigMatch.root' )
    #filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/ApplyElToPhFF/data/ElToPhFFOneBin.root' )
    filt.add_var( 'hist_name_norm', 'norm')
    #filt.add_var( 'hist_name_pt', 'pt')
    filt.add_var( 'hist_name_eta', 'eta')
    #filt.add_var( 'hist_name_pteta', 'pteta')
    filt.add_var( 'sample_key', 'DYJetsToLL' )
    #filt.add_var( 'nconv', '0' )

    alg_list.append(filt)
    

