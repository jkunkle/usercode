from core import Filter

def get_remove_filter() :

    return []

def get_keep_filter() :

    return []

def config_analysis( alg_list ) :

    evt_filt = Filter('FilterBasicEvent' )
    evt_filt.cut_nPhot = '> 0'
    #evt_filt.cut_nPhotLepMom = '== 1'
    evt_filt.cut_nPhotWMom = '== 1'
    evt_filt.cut_nPhotQuarkMom = '== 1'
    alg_list.append(evt_filt)

