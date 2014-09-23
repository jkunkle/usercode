from core import Filter

def get_remove_filter() :

    return ['.*']

def get_keep_filter() :

    return []

def config_analysis( alg_list ) :

    build_lep = Filter('BuildLepton')
    #build_lep.cut_incTau = 'False'
    build_lep.cut_incTauMother = 'True'
    build_lep.cut_incWMother = 'True'
    build_lep.cut_incZMother = 'True'

    #build_lep.cut_pt = '> 25'
    #build_lep.cut_abseta = '< 2.5'

    alg_list.append( build_lep )

    build_phot = Filter( 'BuildPhoton' )
    build_phot.cut_motherPID = ' < 25 '
    #build_phot.cut_pt  = ' > 15'
    #build_phot.cut_abseta = ' < 2.5'

    alg_list.append( build_phot )

    build_nu = Filter('BuildNeutrino') 
    build_nu.cut_incWMother = 'True'
    build_nu.cut_incZMother = 'True'

    alg_list.append(build_nu)

    alg_list.append( Filter('BuildWboson') )
    alg_list.append( Filter('BuildEvent'   ) )


