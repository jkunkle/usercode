def config_samples(samples) :

    import ROOT

    samples.AddSample('Wkk'    , path='Wkk'  , plotColor=ROOT.kBlue, isSignal=True, useXSFile=True )
    samples.AddSample('Wgg'    , path='Wgg'  , plotColor=ROOT.kRed-2, isSignal=False, useXSFile=True )


