def config_samples(samples) :

    import ROOT

    samples.AddSample('NoTrig'   , path='job_summer12_DYJetsToLLNoTrig/', scale=1.0, plotColor=ROOT.kBlue )
    samples.AddSample('WithTrig'   , path='job_summer12_DYJetsToLLWithTrig/'    ,  scale=1.0, plotColor=ROOT.kRed )



