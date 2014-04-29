

def config_samples(samples) :
    import ROOT

    samples.AddSample('DYJetsToLL', path='job_summer12_DYJetsToLL', useXSFile=True, plotColor=ROOT.kCyan, legend_name='Z+jets')
    samples.AddSample('DYJetsToLLPhOlap'             , path='job_summer12_DYJetsToLLPhOlap'        ,  legend_name='Z+jets, overlap removed', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=True)
    samples.AddSample('Zg'             , path='job_summer12_ZgPhOlap'        ,  legend_name='Z#gamma', plotColor=ROOT.kOrange, useXSFile=True, isActive=True)

    samples.AddSampleGroup( 'SumAfterOlapRm', legend_name='Z#gamma + Z+jets, overlap removed', 
                            input_samples = [
                                             'DYJetsToLLPhOlap',
                                             'Zg',
                                            ],
                           plotColor=ROOT.kPink,
                          )

    samples.AddSampleGroup( 'SumBeforeOlapRm', legend_name='Z#gamma + Z+jets, not overlap removed', 
                            input_samples = [
                                             'DYJetsToLL',
                                             'Zg',
                                            ],
                           plotColor=ROOT.kPink,
                          )



def print_examples() :
    pass
