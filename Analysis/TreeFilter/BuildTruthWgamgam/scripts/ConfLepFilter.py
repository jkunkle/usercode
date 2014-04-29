from filter import Filter

def get_remove_filter() :

    return ['.*']

def get_keep_filter() :

    return []

def config_analysis( alg_list ) :

    build_lep = Filter('BuildLepton')
    build_lep.cut_incTau = 'False'
    build_lep.cut_incTauMother = 'False'

    alg_list.append(build_lep)

    filt_event = Filter('FilterEvent')
    filt_event.cut_nLep = '> 0'

    alg_list.append(filt_event)

