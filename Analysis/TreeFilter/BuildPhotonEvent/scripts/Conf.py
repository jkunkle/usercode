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

    #----------------------------------------
    # Get the isData flag from the args
    # so it isnt used in the args below
    #----------------------------------------
    isData = args.pop('isData', 'False')

    #----------------------------------------
    # lepton and photon filters must be run 
    # before the jet filter
    # to properly handle the overlap removal
    #----------------------------------------

    
    #----------------------------------------
    # Nominal muon filter
    #----------------------------------------
    alg_list.append( get_muon_filter( id='Tight',  ptcut=10, etacut=2.4 ) )

    #----------------------------------------
    # Nominal electron filter
    #----------------------------------------
    alg_list.append( get_electron_filter( 'medium', ptcut=10, doPhOlapRm=False) )

    #----------------------------------------
    # Nominal photon filter with no photon ID
    #----------------------------------------
    alg_list.append( get_photon_filter( id=None, eVeto=None, ptcut=15, sort_by_id=True, doElOlapRm=True, doTrigElOlapRm=False ) )

    #----------------------------------------
    # Nominal jet filter
    #----------------------------------------
    #alg_list.append( get_jet_filter(do_hists=False) )

    #----------------------------------------
    # Calculate event level variables
    #----------------------------------------
    alg_list.append( Filter( 'CalcEventVars' ) )

    #----------------------------------------
    # Calculate truth level variables
    ##----------------------------------------
    #alg_list.append( Filter( 'BuildTruth' ) )

    #----------------------------------------
    # Set event level cuts that are passed
    # from the scheduler
    #----------------------------------------
    filter_event = Filter('FilterEvent')
    for cut, val in args.iteritems() :
        setattr(filter_event, cut, val)

    alg_list.append( filter_event )

    # Apply blinding
    apply_blinding = args.get('applyBlinding', False)
    print apply_blinding
    if apply_blinding :
        filter_blind = Filter( 'FilterBlind' )
        filter_blind.cut_nPhPassMediumPt50 = ' == 0 '
        alg_list.append(filter_blind)




def get_jet_filter( do_hists = False ) :

    filt = Filter ( 'FilterJet' ) 

    filt.cut_jet_nhf = ' < 0.99 '
    filt.cut_jet_nef = ' < 0.99 '
    filt.cut_jet_chf = ' > 0 '
    filt.cut_jet_cef = ' < 0.99 '
    filt.cut_jet_n_constituents = ' > 1 '
    filt.cut_jet_nch = ' > 0 '

    # redo overlap rm with photons and muons
    filt.cut_jet_ele_dr = ' > 0.4 '
    filt.cut_jet_ph_dr = ' > 0.4 '
    filt.cut_jet_mu_dr = ' > 0.4 '

    filt.do_cutflow = False

    if do_hists :
        filt.add_hist('cut_jet_ele_dr', 50, 0, 5)
        filt.add_hist('cut_jet_ph_dr', 50, 0, 5)
        filt.add_hist('cut_jet_mu_dr', 50, 0, 5)

    return filt

def get_electron_filter ( id, ptcut=10, doPhOlapRm=False ) :

    filt = Filter( 'FilterElectron' )

    filt.cut_el_pt = ' > %d'  %ptcut
    #--------------------------------
    # remove electrons near a muon
    # NOTE -- the muon filter should be
    # run before the electron fitler
    # for the cut to work properly
    #--------------------------------
    filt.cut_mu_el_dr = ' > 0.4 '
    if doPhOlapRm :
        filt.cut_ph_el_dr = ' > 0.4 '

    if id is not None :
        setattr( filt, 'cut_el_%s' %id, ' == True' )

    return filt

def get_photon_filter( id=None, eVeto=None, eVetoVal='False', ptcut=10, sort_by_id='false', doElOlapRm=True, doTrigElOlapRm=True, doMuOlapRm=True, doPhOlapRm=True, olapDR=0.4 ) :

    if id is None :
        print 'NO PHOTON ID'
    else :
        print 'FILTER %s PHOTONS' %id
    if eVeto is None :
        print 'NO PHOTON EVETO'
    else :
        if eVetoVal == 'False' :
            print 'REMOVE PHOTONS FAILING ELECTRON VETO, %s' %eVeto
        else :
            print 'REMOVE PHOTONS PASSING ELECTRON VETO, %s' %eVeto

    if doElOlapRm : 
        print 'FILER PHOTONS FROM ALL ELECTRONS, dR > %.2f' %olapDR
    if doTrigElOlapRm : 
        print 'FILER PHOTONS FROM LEADING TRIGGERED ELECTRON, dR > %.2f' %olapDR
    if doMuOlapRm : 
        print 'FILER PHOTONS FROM ALL MUONS, dR > %.2f' %olapDR
    if doPhOlapRm : 
        print 'FILER PHOTONS FROM OVERLAPPING PHOTONS OF HIGHER PT, dR > %.2f' %olapDR

    #if sort_by_id == True :
    #    sort_by_id = 'true'
    #if sort_by_id == False :
    #    sort_by_id = 'false'

    filt = Filter( 'FilterPhoton' )
    filt.cut_ph_pt = ' > %d ' %ptcut

    if doMuOlapRm :
        filt.cut_mu_ph_dr = ' > %f ' %olapDR
    if doPhOlapRm :
        filt.cut_ph_ph_dr = ' > %f ' %olapDR
    if doElOlapRm :
        filt.cut_el_ph_dr = ' > %f ' %olapDR
    if doTrigElOlapRm :
        filt.cut_trigel_ph_dr = ' > %f ' %olapDR

    if id is not None :
        setattr( filt, 'cut_ph_%s' %id, ' == True' )
    if eVeto is not None :
        setattr( filt, 'cut_ph_%s' %eVeto, ' == %s ' %eVetoVal )

    #filt.sort_by_id = sort_by_id

    return filt


def get_muon_filter( id='Tight', ptcut=10, etacut=2.1 ) :

    filt = Filter( 'FilterMuon' )

    if id is not None :
        setattr(filt,  'cut_mu_pass%s' %id, ' == True' )
    filt.cut_mu_pt = ' > %d' %ptcut
    filt.cut_mu_eta = ' < %.1f '%etacut

    
    return filt
