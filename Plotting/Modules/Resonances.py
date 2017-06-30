

def config_samples(samples) :

    import ROOT
    samples.AddSample('Wg'                           , path='job_summer12_Wg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('Wjets'                        , path='job_summer12_Wjets'               ,  isActive=False, useXSFile=True, XSName='Wjets' )
    samples.AddSample('ResonanceMass400Width10'      , path='job_LNuAA_LM0123_Reweight'            , isActive=True, useXSFile=True, XSName='Wgg', isSignal=True, plotColor=ROOT.kRed )



def print_examples() :
    pass
