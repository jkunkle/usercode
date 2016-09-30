from core import Filter

def get_remove_filter() :

    return []

def get_keep_filter() :

    #return ['mc.*', 'nMC']
    return ['el_passtrig_n', 'el_n', 'ph_n', 'ph_mediumPassCSEV_n', 'ph_mediumFailCSEV_n', 'ph_mediumPassPSV_n', 'ph_mediumFailPSV_n', 'ptSorted_ph_mediumPassCSEV_idx', 'ptSorted_ph_mediumFailCSEV_idx', 'ptSorted_ph_mediumPassPSV_idx', 'ptSorted_ph_mediumFailPSV_idx', 'ph_eta', 'ph_pt', 'ph_hasPixSeed', 'ph_eleVeto', 'dr_ph1_trigEle', 'ph_truthMatch_el']

def config_analysis( alg_list ) :

    return alg_list

