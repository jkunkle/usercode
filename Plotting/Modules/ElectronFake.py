def config_samples(samples) :

    import ROOT

    #samples.AddSample('DYJetsToLL'   , path='job_summer12_DYJetsToLL', plotColor=ROOT.kBlue )
    samples.AddSample('Zg'           , path='job_summer12_Zg_s10'    ,  plotColor=ROOT.kRed )
    samples.AddSample('Wg'           , path='job_summer12_Wg'    ,  plotColor=ROOT.kRed )
    samples.AddSample('DYJetsToLL' , path='job_summer12_DYJetsToLL_s10'    ,  plotColor=ROOT.kRed, isActive=False )
    samples.AddSample('DYJetsToLLPhOlap' , path='job_summer12_DYJetsToLL_s10PhOlap'    ,  plotColor=ROOT.kRed, isActive=False )
    samples.AddSample('ttjets_1l'                    , path='job_summer12_ttjets_1l'            ,  isActive=False, useXSFile=True )
    samples.AddSample('ttjets_2l'                    , path='job_summer12_ttjets_2l'            ,  isActive=False, useXSFile=True )
    samples.AddSample('Wjets'                        , path='job_summer12_Wjets'               ,  isActive=False, useXSFile=True, XSName='Wjets' )
    samples.AddSample('FakeBackgroundSamples'        , path='FakeBackgroundSamples'               ,  isActive=False, useXSFile=False)

    samples.AddSample('electron_2012a_Jan22rereco'   , path='job_electron_2012a_Jan22rereco'    ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012b_Jan22rereco'   , path='job_electron_2012b_Jan22rereco'    ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012c_Jan2012rereco' , path='job_electron_2012c_Jan2012rereco'  ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012d_Jan22rereco'   , path='job_electron_2012d_Jan22rereco'    ,  isActive=False, scale=1.0 )

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             'electron_2012a_Jan22rereco',
                                             'electron_2012b_Jan22rereco',
                                             'electron_2012c_Jan2012rereco',
                                             'electron_2012d_Jan22rereco',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )

    samples.AddSampleGroup( 'Electron', legend_name='Data', 
                            input_samples = [
                                             'electron_2012a_Jan22rereco',
                                             'electron_2012b_Jan22rereco',
                                             'electron_2012c_Jan2012rereco',
                                             'electron_2012d_Jan22rereco',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )

    
    samples.AddSampleGroup( 'ZjetsZgamma', legend_name='ZjetsZgamma', 
                            input_samples = [
                                             'DYJetsToLLPhOlap',
                                             'Zg',
                            ],
                           plotColor=ROOT.kBlue,
                           )


    samples.AddSampleGroup( 'Zgamma', legend_name='Zgamma', 
                            input_samples = [
                                             'Zg',
                            ],
                           plotColor=ROOT.kBlue,
                           )

    samples.AddSampleGroup( 'Wgamma', legend_name='Wgamma', 
                            input_samples = [
                                             'Wg',
                            ],
                           plotColor=ROOT.kBlue,
                           )


