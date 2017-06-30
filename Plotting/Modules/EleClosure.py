

def config_samples(samples) :

    import ROOT

    samples.AddSample('DYJetsToLLNOOlapDup'             , path='job_summer12_DYJetsToLL_s10_olapDup'       ,  isActive=True, plotColor=ROOT.kBlack)
    samples.AddSample('DYJetsToLLFullOlap'             , path='job_summer12_DYJetsToLL_s10_withOlap'     ,  isActive=True, plotColor=ROOT.kBlue)
    samples.AddSample('ZgFullOlap'                         , path='job_summer12_Zg_s10_withOlap'     ,  isActive=True, plotColor=ROOT.kBlue)
    samples.AddSample('ZgNoOlapDupInvPSVLead'                         , path='job_summer12_Zg_s10_olapDupInvLead'     ,  isActive=True, plotColor=ROOT.kBlue)
    samples.AddSample('ZgNoOlapDupInvPSVSubl'                         , path='job_summer12_Zg_s10_olapDupInvSubl'     ,  isActive=True, plotColor=ROOT.kBlue)



def print_examples() :
    pass
