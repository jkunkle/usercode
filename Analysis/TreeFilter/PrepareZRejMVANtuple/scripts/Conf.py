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

    
    # for complicated configurations, define a function
    # that returns the Filter object and append it to the
    # alg list.  Otherwise you can directly append 
    # a Filter object to the list

    #----------------------
    # For ISR sample
    #----------------------
    #Sample Zg : lumi_sample = 41403.726747, scale = 0.468557
    #Sample Wgg_FSR : lumi_sample = 545608.695652, scale = 0.035557
    #Sample DYJetsToLL : lumi_sample = 8693.344750, scale = 2.231592
    #Sample WAA_ISR : lumi_sample = 3135768.025078, scale = 0.006187

    weight = Filter('WeightEvent')
    #weight.add_var( 'Weight', '0.468557') #Zg
    #weight.add_var( 'Weight', '2.231592') #DYJetsToLL
    weight.add_var( 'Weight', '0.035557') #Wgg_FSR
    #weight.add_var( 'Weight', '0.006187') #WAA_ISR

    alg_list.append( weight )


    filt_phot = Filter( 'FilterPhoton' )
    filt_phot.cut_ph_pt = ' > 15 '
    filt_phot.cut_ph_medium = ' == True '
    #filt_phot.cut_ph_hasPixSeed = ' == False '

    #alg_list.append(filt_phot ) 

    alg_list.append( filter_event( nPhPassEleVeto=2 ) )

    alg_list.append(Filter('CalcVars') )


def filter_event ( nPhPassEleVeto=None ) :

    
    filt_event = Filter( 'FilterEvent' )
    filt_event.cut_el_passtrig_n = ' >0 '
    filt_event.cut_el_n = ' ==1 '
    filt_event.cut_mu_n = ' ==0 '
    filt_event.cut_ph_n = ' ==2 '
    filt_event.cut_ph_phDR = ' > 0.3 '
    filt_event.cut_leadPhot_leadLepDR = ' > 0.7 '
    filt_event.cut_sublPhot_leadLepDR = ' > 0.7 '

    if nPhPassEleVeto is not None :
        filt_event.cut_nPhPassEleVeto = ' == %d ' %nPhPassEleVeto

    return filt_event


