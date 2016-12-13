

def config_samples(samples) :

    import ROOT


    samples.AddSample('DiPhoton_M40_80', path='DiPhotonJetsBox_M40_80-Sherpa', isActive=True, useXSFile=True, plotColor=ROOT.kYellow )
    samples.AddSample('DiPhoton_M80toInf', path='DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa', isActive=True, useXSFile=True, plotColor=ROOT.kRed-4)


def print_examples() :
    pass
