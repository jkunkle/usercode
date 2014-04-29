

def config_samples(samples) :
    import ROOT

    samples.AddSample('job_summer12_gjet_pt20to40_doubleEM', path='job_summer12_gjet_pt20to40_doubleEM',  isActive=False)
    samples.AddSample('job_summer12_gjet_pt40_doubleEM', path='job_summer12_gjet_pt40_doubleEM',  isActive=False)
    samples.AddSample('job_summer12_qcd_pt30to40_doubleEM', path='job_summer12_qcd_pt30to40_doubleEM',  isActive=False)
    samples.AddSample('job_summer12_qcd_pt40_doubleEM', path='job_summer12_qcd_pt40_doubleEM',  isActive=False)

    samples.AddSampleGroup( 'Photon', legend_name='Single photon', 
                            input_samples = [
                                            'job_summer12_gjet_pt20to40_doubleEM',
                                            'job_summer12_gjet_pt40_doubleEM',
                                            ],
                           plotColor=ROOT.kBlue,
                          )

    samples.AddSampleGroup( 'QCD', legend_name='Multi jet', 
                            input_samples = [
                                            'job_summer12_qcd_pt40_doubleEM',
                                            'job_summer12_qcd_pt30to40_doubleEM',
                                            ],
                           plotColor=ROOT.kRed,
                          )



def print_examples() :
    pass
