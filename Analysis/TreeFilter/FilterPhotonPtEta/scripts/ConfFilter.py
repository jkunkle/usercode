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

    nom_inv = args['type']

    filter_photon = Filter('FilterPhoton')

    if nom_inv == 'inv' :
        setattr( filter_photon, 'cut_ph_%s' %args['eveto'] , True )
    elif nom_inv == 'nom' :
        setattr( filter_photon, 'cut_ph_%s' %args['eveto'] , False )

    alg_list.append(filter_photon)

    filter_event = Filter('FilterEvent')

    filter_event.add_var( 'eveto', args['eveto'] )
    filter_event.add_var( 'type', args['type'] )

    filter_event.cut_Nph = args['nph']
    filter_event.cut_ph_pt = ' > %s & < %s ' %( args['ptmin'],  args['ptmax'] )
    filter_event.cut_abs_ph_eta = ' > %s & < %s ' %( args['etamin'],  args['etamax'] )
    filter_event.cut_save_max = ' < 15000 '

    alg_list.append( filter_event )


