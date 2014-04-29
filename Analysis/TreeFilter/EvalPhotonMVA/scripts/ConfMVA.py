from core import Filter
import os
import sys

def get_remove_filter() :

    return ['.*']

def get_keep_filter() :

    return []

def config_analysis( alg_list, args ) :

    alg_list.append( build_photon( do_cutflow=False, do_hists=False, evalPID=None) )

def build_photon( do_cutflow=False, do_hists=False, filtPID=None, evalPID=None ) :

    filt = Filter('BuildPhoton')

    filt.add_var( 'TMVAWeightsFileEB11W', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/TrainPhotonMVA/weights/photonMVAWtrainEB_BDT.weights.xml' )
    filt.add_var( 'TMVAWeightsFileEE11W', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/TrainPhotonMVA/weights/photonMVAWtrainEE_BDT.weights.xml' )
    #filt.add_var( 'TMVAWeightsFileEB5', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/TrainPhotonMVA/weights/photonMVAEB_BDT.weights.xml' )
    #filt.add_var( 'TMVAWeightsFileEE5', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/TrainPhotonMVA/weights/photonMVAEE_BDT.weights.xml' )
    #filt.add_var( 'TMVAWeightsFileEB6', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/TrainPhotonMVA/weights_6var_v1/photonMVAEB_BDT.weights.xml' )
    #filt.add_var( 'TMVAWeightsFileEE6', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/TrainPhotonMVA/weights_6var_v1/photonMVAEE_BDT.weights.xml' )
    #filt.add_var( 'TMVAWeightsFileEB11', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/TrainPhotonMVA/weights_11var_v1/photonMVAEB_BDT.weights.xml' )
    #filt.add_var( 'TMVAWeightsFileEE11', '/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/TrainPhotonMVA/weights_11var_v1/photonMVAEE_BDT.weights.xml' )

    return filt

