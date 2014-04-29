from core import Filter

def get_remove_filter() :

    return ['.*']

def get_keep_filter() :

    return []

def config_analysis( alg_list ) :

    build_lep = Filter('BuildLepton')
    build_lep.cut_incTau = 'False'
    build_lep.cut_incTauMother = 'True'

    #build_lep.cut_pt = '> 25'
    #build_lep.cut_abseta = '< 2.5'

    alg_list.append( build_lep )

    build_phot = Filter( 'BuildPhoton' )
    #build_phot.cut_pt  = ' > 15'
    #build_phot.cut_abseta = ' < 2.5'

    alg_list.append( build_phot )

    alg_list.append( Filter('BuildNeutrino') )
    alg_list.append( Filter('BuildWboson') )

    alg_list.append( Filter('BuildEvent'   ) )

