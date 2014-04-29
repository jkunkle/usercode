from filter import Filter

def get_remove_filter() :

    return ['.*']

def get_keep_filter() :

    return []

def config_analysis( alg_list ) :

    filt_event = Filter('FilterTauEvent')
    filt_event.cut_nTau = '== 1'
    filt_event.cut_tauStatus = ' == 3'

    alg_list.append(filt_event)

