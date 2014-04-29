def config_samples(samples) :

    import ROOT

    samples.AddSample('DYJetsToLL'                   , path='job_summer12_DYJetsToLL'           ,  scale=1.0, )
    #samples.AddSample('DYJetsToLLFF'                   , path='job_summer12_DYJetsToLLFFUpdatePtEta2DnewBinMassCut'           ,  scale=1.0 )
    samples.AddSample('DYJetsToLLFF'                   , path='job_summer12_DYJetsToLLFFUpdate2DNewBin'           ,  scale=1.0 )
    #samples.AddSample('DYJetsToLLFF'                   , path='job_summer12_DYJetsToLLFFUpdatePtEta1D'           ,  scale=1.0 )
    #samples.AddSample('DYJetsToLLFF'                   , path='job_summer12_DYJetsToLLFFUpdatePt1D'           ,  scale=1.0 )
    #samples.AddSample('DYJetsToLLFF'                   , path='job_summer12_DYJetsToLLFFUpdate1DPtSimple'           ,  scale=1.0 )
    #samples.AddSample('DYJetsToLLFF'                   , path='job_summer12_DYJetsToLLFFUpdatePt1DLooseLowPtSimple'           ,  scale=1.0 )
    #samples.AddSample('DYJetsToLLFF'                   , path='job_summer12_DYJetsToLLFFUpdatePt1DLooseLowPtSimpleTestBiasFilter'           ,  scale=1.0 )
    #samples.AddSample('DYJetsToLLFF'                   , path='job_summer12_DYJetsToLLFFUpdatePt1DLooseLowPtSimpleBiasFilterNoOlap'           ,  scale=1.0 )

def print_examples() :
    pass

