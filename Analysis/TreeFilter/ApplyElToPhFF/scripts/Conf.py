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

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    filt = Filter('AddEventWeight')
    filt.cut_elpasstrig_n = ' > 0 '
    filt.cut_el_n = ' == 1 '
    filt.cut_ph_n = ' == 2 '

    if args['DoLeadWeight'] == True :
        filt.cut_ph_leadPixSeed = ' == 1 '
    if args['DoLeadWeight'] == False :
        filt.cut_ph_leadPixSeed = ' == 0 '
    if args['DoSublWeight'] == True :
        filt.cut_ph_leadPixSeed = ' == 1 '
    if args['DoSublWeight'] == False :
        filt.cut_ph_leadPixSeed = ' == 0 '

    
    filt.add_var( 'root_file', '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_08_18/ElectronFakeFitsRatio/results.root' )
    filt.add_var( 'hist_name', 'ff')

    alg_list.append(filt)
    

