from core import Filter
import os
import sys
import inspect

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

    print options

    # run on the function provided through
    # the args
    for s in inspect.getmembers(sys.modules[__name__]) :
        if s[0] in options['functions'].split(',') :
            print '*********************************'
            print 'RUN %s' %( s[0] )
            print '*********************************'
            alg_list.append( s[1]( options['args'] ) )

    print alg_list

    #alg_list.append( get_muon_sf() ) 
    #alg_list.append( get_electron_sf() ) 
    #alg_list.append( get_photon_sf() ) 
    #alg_list.append( get_pileup_sf(options) )
    #alg_list.append( Filter ( 'AddMETUncert' ) )

def get_muon_sf(options) :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    muon_sf = Filter( 'AddMuonSF' )


    muon_sf.add_var( 'FilePathTrig', '%s/SingleMuonTriggerEfficiencies_eta2p1_Run2012ABCD_v5trees.root' %base_path )
    muon_sf.add_var( 'FilePathDiTrig', '%s/triggerSummary_mumu_rereco198fb.root' %base_path )

    muon_sf.add_var( 'FilePathIso', '%s/MuonEfficiencies_ISO_Run_2012ReReco_53X.root' %base_path )
    muon_sf.add_var( 'FilePathId', '%s/MuonEfficiencies_Run2012ReReco_53X.root' %base_path )

    return muon_sf

def get_electron_sf(options) :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    electron_sf = Filter( 'AddElectronSF' )

    electron_sf.add_var( 'FilePathID', '%s/electrons_scale_factors.root' %base_path )
    electron_sf.add_var( 'FilePathDiTrig', '%s/triggerSummary_ee_rereco198fb.root' %base_path )
    electron_sf.add_var( 'FilePathCutID', '%s/CutBasedIdScaleFactors.root' %base_path )

    return electron_sf

def get_photon_sf(options) :

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

def vary_egamma_scale_up (options) :
    print 'GOTHERE'
    egamma_vary = Filter( 'VaryEGammaScale' )
    egamma_vary.add_var( 'Direction', 'UP' )
    return egamma_vary

def vary_egamma_scale_dn(options) :
    egamma_vary = Filter( 'VaryEGammaScale' )
    egamma_vary.add_var( 'Direction', 'DN' )
    return egamma_vary

def vary_muon_scale_up (options) :
    muon_vary = Filter( 'VaryMuonScale' )
    muon_vary.add_var( 'Direction', 'UP' )
    return muon_vary

def vary_muon_scale_dn(options) :
    muon_vary = Filter( 'VaryMuonScale' )
    muon_vary.add_var( 'Direction', 'DN' )
    return muon_vary

def vary_met_uncert(options) :
    return Filter( 'AddMETUncert' )



