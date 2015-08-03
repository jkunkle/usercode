

def config_samples(samples) :

    import ROOT
    samples.AddSample('electron_2012a_Jan22rereco'   , path='job_electron_2012a_Jan22rereco'    ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012b_Jan22rereco'   , path='job_electron_2012b_Jan22rereco'    ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012c_Jan2012rereco' , path='job_electron_2012c_Jan2012rereco'  ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012d_Jan22rereco'   , path='job_electron_2012d_Jan22rereco'    ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012a_Jan22rereco'       , path='job_muon_2012a_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012b_Jan22rereco'       , path='job_muon_2012b_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012c_Jan22rereco'       , path='job_muon_2012c_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012d_Jan22rereco'       , path='job_muon_2012d_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('Zg'                           , path='job_summer12_Zg'                   ,  isActive=False, useXSFile=True )


    samples.AddSampleGroup( 'Muon', legend_name='Muon Data', 
                            input_samples = [
                                             'muon_2012a_Jan22rereco',
                                             'muon_2012b_Jan22rereco',
                                             'muon_2012c_Jan22rereco',
                                             'muon_2012d_Jan22rereco',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )
    samples.AddSampleGroup( 'Electron', legend_name='Electron Data', 
                            input_samples = [
                                             'electron_2012a_Jan22rereco',
                                             'electron_2012b_Jan22rereco',
                                             'electron_2012c_Jan2012rereco',
                                             'electron_2012d_Jan22rereco',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )

    


    samples.AddSampleGroup( 'RealPhotonsZg', legend_name='Fake photons', 
                        input_samples = [
                            'Zg',
                        ],
                           plotColor=ROOT.kYellow,
                          )



def print_examples() :
    pass
