

def config_samples(samples) :

    import ROOT
    #samples.AddSample('electron_2012a_Jan22rereco'   , path='job_electron_2012a_Jan22rereco'    ,  isActive=False, scale=1.0 )
    #samples.AddSample('electron_2012b_Jan22rereco'   , path='job_electron_2012b_Jan22rereco'    ,  isActive=False, scale=1.0 )
    #samples.AddSample('electron_2012c_Jan2012rereco' , path='job_electron_2012c_Jan2012rereco'  ,  isActive=False, scale=1.0 )
    #samples.AddSample('electron_2012d_Jan22rereco'   , path='job_electron_2012d_Jan22rereco'    ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012a_Jan22rereco'       , path='job_2muon_2012a_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012b_Jan22rereco'       , path='job_2muon_2012b_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012c_Jan22rereco'       , path='job_2muon_2012c_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012d_Jan22rereco'       , path='job_2muon_2012d_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('DYJetsToLLPhOlap'             , path='job_summer12_DYJetsToLLPhOlap'     ,  isActive=False, useXSFile=True, XSName='DYJetsToLL')
    samples.AddSample('Zg'                           , path='job_summer12_Zg'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('ZgPhOlap'                           , path='job_summer12_ZgPhOlap'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('ZggFSR'                           , path='job_summer12_ZggFSR'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('ZggFSR2'                           , path='job_summer12_ZggFSR2'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('Zgg'                          , path='job_summer12_Zgg'                  ,  isActive=False, useXSFile=True )


    #samples.AddSample('MultiJet', path='job_MultiJet_2012a_Jan22rereco', isActive=True )

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             'muon_2012a_Jan22rereco',
                                             'muon_2012b_Jan22rereco',
                                             'muon_2012c_Jan22rereco',
                                             'muon_2012d_Jan22rereco',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )

    samples.AddSampleGroup( 'Muon', legend_name='Data', 
                            input_samples = [
                                             'muon_2012a_Jan22rereco',
                                             'muon_2012b_Jan22rereco',
                                             'muon_2012c_Jan22rereco',
                                             'muon_2012d_Jan22rereco',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                           isActive=False,
                          )

    samples.AddSampleGroup( 'Zgammastar', legend_name='Z/#gamma * ', 
                            input_samples = [
                                             'DYJetsToLLPhOlap'
                                            ],
                           plotColor=ROOT.kCyan,
                           scale=1.0,
                           #scale=1.4,
                          )

    samples.AddSampleGroup( 'Zgamma', legend_name='Z#gamma', 
                           input_samples = [
                                            'Zg',
                           ],
                           plotColor=ROOT.kOrange-4,
                           isSignal=False,
                           isActive=False,
                          )
    samples.AddSampleGroup( 'ZgammagammaFSR', legend_name='Z#gamma#gamma FSR', 
                           input_samples = [
                                            'ZggFSR2',
                           ],
                           plotColor=ROOT.kOrange-4,
                           isSignal=False,
                           isActive=True,
                          )
    samples.AddSampleGroup( 'Zgammagamma', legend_name='Z#gamma#gamma', 
                           input_samples = [
                                            'Zgg',
                           ],
                           plotColor=ROOT.kOrange+2,
                           isActive=False,
                          )


def print_examples() :
    pass
