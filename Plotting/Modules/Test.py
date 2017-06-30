def config_samples(samples) :

    import ROOT

    samples.AddSample('WJetsToLNu'                    , path='WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'               , isActive=True, isSignal=True, plotColor=1, useXSFile=True )
    samples.AddSample('WJetsToLNu_HT-100To200'         , path='WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , isActive=True, isSignal=True, plotColor=2, useXSFile=True )
    samples.AddSample('WJetsToLNu_HT-200To400'         , path='WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , isActive=True, isSignal=True, plotColor=3, useXSFile=True )
    samples.AddSample('WJetsToLNu_HT-400To600'         , path='WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , isActive=True, isSignal=True, plotColor=4, useXSFile=True )
    samples.AddSample('WJetsToLNu_HT-600To800'         , path='WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , isActive=True, isSignal=True, plotColor=5, useXSFile=True )
    samples.AddSample('WJetsToLNu_HT-800To1200'        , path='WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'  , isActive=True, isSignal=True, plotColor=6, useXSFile=True )
    samples.AddSample('WJetsToLNu_HT-1200To2500'        , path='WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', isActive=True, isSignal=True, plotColor=7, useXSFile=True )
    samples.AddSample('WJetsToLNu_HT-2500ToInf'         , path='WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'  , isActive=True, isSignal=True, plotColor=8, useXSFile=True )
