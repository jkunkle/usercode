from core import Filter

def get_remove_filter() :

    return []

def get_keep_filter() :

    #return ['mc.*', 'nMC']
    return ['el_n', 'mu_n', 'ph_n', 'el_pt', 'el_eta', 'el_phi', 'el_e', 'mu_pt', 'mu_eta', 'mu_phi', 'mu_e.*', 'el_pfiso40', 'el_triggerMatch', 'el_passMvaTrig', 'el_passMvaNonTrig', 'el_mva.*', 'mu_corrIso', 'mu_passTightNoIso', 'mu_passTight', 'mu_triggerMatch', 'pfMET', 'mu_truthMatch', 'el_truthMatch_el']

def config_analysis( alg_list ) :

    return alg_list

