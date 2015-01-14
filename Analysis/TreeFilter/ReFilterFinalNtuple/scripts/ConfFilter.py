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

    
    # for complicated configurations, define a function
    # that returns the Filter object and append it to the
    # alg list.  Otherwise you can directly append 
    # a Filter object to the list
    # There is no restriction on the naming or inputs to these funtions
    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_medium = ' == True '
    #filter_photon.cut_ph_mediumNoSIEIE = ' == True '
    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' > 1 '
    #filter_event.cut_hasPixSeed_leadph12 = ' == False '
    #filter_event.cut_hasPixSeed_sublph12 = ' == True '
    #filter_event.cut_csev_leadph12 = ' == False '
    #filter_event.cut_csev_sublph12 = ' == False '

    alg_list.append( filter_event )

    isData = args.pop('isData', 'False')
    filter_blind = Filter( 'FilterBlind' )
    filter_blind.cut_ph_pt_lead = ' < 40 '
    #filter_blind.cut_m_lepphph= ' > 86.2 & < 96.2  '
    #filter_blind.cut_m_lepph1= ' > 86.2 & < 96.2  '
    #filter_blind.cut_m_lepph2= ' > 86.2 & < 96.2  '

    #filter_blind.cut_m_lepphph= ' > 81.2 & < 101.2  '
    #filter_blind.cut_m_lepph1= ' > 81.2 & < 101.2  '
    #filter_blind.cut_m_lepph2= ' > 81.2 & < 101.2  '

    filter_blind.add_var( 'isData', isData )

    alg_list.append(filter_blind)


