def config_samples(samples) :

    import ROOT

    samples.AddSample('WW'    , path='job_summer12_WW_2l2nu'  , scale=1.0, plotColor=ROOT.kBlue )
    #samples.AddSample('WWg'   , path='job_summer12_WWg'    ,  scale=2.26, plotColor=ROOT.kRed )
    samples.AddSample('WWg'   , path='job_summer12_WWg'    ,  scale=1.0, plotColor=ROOT.kRed )
    samples.AddSample('TT1L'    , path='job_summer12_ttjets_1l'  , scale=1.0, plotColor=ROOT.kBlue )
    samples.AddSample('TT2L'    , path='job_summer12_ttjets_2l'  , scale=1.0, plotColor=ROOT.kBlue )
    #samples.AddSample('TTg'   , path='job_summer12_ttg'    ,  scale=2.32, plotColor=ROOT.kRed )
    samples.AddSample('TTg'   , path='job_summer12_ttg'    ,  scale=1.0, plotColor=ROOT.kRed )



