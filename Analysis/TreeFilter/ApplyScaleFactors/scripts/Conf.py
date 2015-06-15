from core import Filter
import os

_workarea = os.getenv( 'WorkArea' )

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

    return ['.*']

def config_analysis( alg_list, options ) :
    """ Configure analysis modules. Order is preserved """

    # for complicated configurations, define a function
    # that returns the Filter object and append it to the
    # alg list.  Otherwise you can directly append 
    # a Filter object to the list
    # There is no restriction on the naming or inputs to these funtions

    alg_list.append( get_muon_sf() ) 
    alg_list.append( get_electron_sf() ) 
    alg_list.append( get_photon_sf() ) 
    #alg_list.append( get_pileup_sf(options) )
    alg_list.append( Filter ( 'AddMETUncert' ) )

def get_muon_sf() :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea


    muon_sf = Filter( 'AddMuonSF' )
    muon_sf.add_var( 'FilePathTrig', '%s/SingleMuonTriggerEfficiencies_eta2p1_Run2012ABCD_v5trees.root' %base_path )
    muon_sf.add_var( 'FilePathIso', '%s/MuonEfficiencies_ISO_Run_2012ReReco_53X.root' %base_path )
    muon_sf.add_var( 'FilePathId', '%s/MuonEfficiencies_Run2012ReReco_53X.root' %base_path )

    return muon_sf

def get_electron_sf() :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    electron_sf = Filter( 'AddElectronSF' )

    electron_sf.add_var( 'FilePathTrig', '%s/electrons_scale_factors.root' %base_path )

    return electron_sf

def get_photon_sf() :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    photon_sf = Filter( 'AddPhotonSF' )

    photon_sf.add_var( 'FilePathId', '%s/Photon_ID_CSEV_SF_Jan22rereco_Full2012_S10_MC_V01.root' %base_path )
    photon_sf.add_var( 'FilePathEveto', '%s/hist_sf_eveto_nom.root' %base_path )
    photon_sf.add_var( 'FilePathEvetoHighPt', '%s/hist_sf_eveto_highpt.root' %base_path )
    
    return photon_sf

def get_pileup_sf(options) :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    pileup_sf = Filter( 'AddPileupSF' )
    pileup_sf.add_var( 'DataFilePath', '%s/Data_Pileup_2012_ReReco-600bins.root' % base_path)
    pileup_sf.add_var( 'MCFilePath', options['PUDistMCFile'] )

    return pileup_sf


