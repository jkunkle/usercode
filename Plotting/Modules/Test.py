def config_samples(samples) :

    import ROOT

    samples.AddSample('DYJetsToLL'   , path='job_summer12_DYJetsToLL'    ,   scale=1.0, plotColor=ROOT.kBlue )
    samples.AddSample('Zg'   , path='job_summer12_Zg'    ,  scale=1.0, plotColor=ROOT.kRed )



