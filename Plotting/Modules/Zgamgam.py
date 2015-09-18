

def config_samples(samples) :

    import ROOT
    samples.AddSample('electron_2012a'   , path='job_2electron_2012a_Jan22rereco'    ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012b'   , path='job_2electron_2012b_Jan22rereco'    ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012c' , path='job_2electron_2012c_Jan22rereco'  ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012d'   , path='job_2electron_2012d_Jan22rereco'    ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012a'       , path='job_2muon_2012a_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012b'       , path='job_2muon_2012b_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012c'       , path='job_2muon_2012c_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012d'       , path='job_2muon_2012d_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('DYJetsToLLPhOlap'             , path='job_summer12_DYJetsToLLPhOlap'     ,  isActive=False, useXSFile=True, XSName='DYJetsToLL')
    samples.AddSample('Zg'                           , path='job_summer12_Zg'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('ZgPhOlap'                           , path='job_summer12_ZgPhOlap'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('ZggFSR'                           , path='job_summer12_ZggFSR'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('ZggFSR2'                           , path='job_summer12_ZggFSR2'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('Zg2PhFilt'                           , path='job_summer12_Zg2PhFilt'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('Zgg'                          , path='job_summer12_Zgg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('ZggNLO'                       , path='llaa_nlo_part1_ggNtupleWithSF'                  ,  isActive=False, useXSFile=True )

    samples.AddSample('ttjets_1l'                    , path='job_summer12_ttjets_1lPhOlap'            ,  isActive=False, useXSFile=True )
    samples.AddSample('ttjets_2l'                    , path='job_summer12_ttjets_2lPhOlap'            ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_s'                       , path='job_summer12_tbar_s'               ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_t'                       , path='job_summer12_tbar_t'               ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_tW'                      , path='job_summer12_tbar_tW'              ,  isActive=False, useXSFile=True )
    samples.AddSample('t_s'                          , path='job_summer12_t_s'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('t_t'                          , path='job_summer12_t_t'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('ttg'                          , path='job_summer12_ttg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('ttjets_1l'                    , path='job_summer12_ttjets_1lPhOlap'            ,  isActive=False, useXSFile=True )
    samples.AddSample('ttjets_2l'                    , path='job_summer12_ttjets_2lPhOlap'            ,  isActive=False, useXSFile=True )
    samples.AddSample('t_tW'                         , path='job_summer12_t_tW'                 ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPhOlap'                           , path='job_summer12_WgPhOlap'          ,  isActive=False, useXSFile=True, XSName='Wg' )
    samples.AddSample('WH_ZH_125'                    , path='job_summer12_WH_ZH_125'            ,  isActive=False, useXSFile=True )
    samples.AddSample('_Wjets'                        , path='job_summer12_Wjets'               ,  isActive=False, useXSFile=True, XSName='Wjets' )
    samples.AddSample('WjetsPhOlap'                  , path='job_summer12_WjetsPhOlap'       ,  isActive=False, useXSFile=True, XSName='Wjets' )
    samples.AddSample('WW_2l2nu'                     , path='job_summer12_WW_2l2nu'             ,  isActive=False, useXSFile=True )
    samples.AddSample('WWg'                          , path='job_summer12_WWg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WWW'                          , path='job_summer12_WWW'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WWZ'                          , path='job_summer12_WWZ'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WZ_2l2q'                      , path='job_summer12_WZ_2l2q'              ,  isActive=False, useXSFile=True )
    samples.AddSample('WZ_3lnu'                      , path='job_summer12_WZ_3lnu'              ,  isActive=False, useXSFile=True )
    samples.AddSample('WZZ'                          , path='job_summer12_WZZ'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ_2e2mu'                     , path='job_summer12_ZZ_2e2mu'             ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ_2e2tau'                    , path='job_summer12_ZZ_2e2tau'            ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ_2l2nu'                     , path='job_summer12_ZZ_2l2nu'             ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ_2l2q'                      , path='job_summer12_ZZ_2l2q'              ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ_2mu2tau'                   , path='job_summer12_ZZ_2mu2tau'           ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ_2q2nu'                     , path='job_summer12_ZZ_2q2nu'             ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ_4e'                        , path='job_summer12_ZZ_4e'                ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ_4mu'                       , path='job_summer12_ZZ_4mu'               ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ_4tau'                      , path='job_summer12_ZZ_4tau'              ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZZ'                          , path='job_summer12_ZZZ'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WZA'          , path='job_jfaulkne_WZA'           , isActive=False, useXSFile=True, XSName='WZA' )

    #samples.AddSample('MultiJet', path='job_MultiJet_2012a_Jan22rereco', isActive=True )

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             'muon_2012a',
                                             'muon_2012b',
                                             'muon_2012c',
                                             'muon_2012d',
                                             'electron_2012a',
                                             'electron_2012b',
                                             'electron_2012c',
                                             'electron_2012d',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )

    samples.AddSampleGroup( 'Muon', legend_name='Data', 
                            input_samples = [
                                             'muon_2012a',
                                             'muon_2012b',
                                             'muon_2012c',
                                             'muon_2012d',
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
                                            #'Zg2PhFilt',
                                            'Zg',
                           ],
                           plotColor=ROOT.kOrange-4,
                           isSignal=False,
                           isActive=True,
                          )
    samples.AddSampleGroup( 'Zgammagamma', legend_name='Z#gamma#gamma', 
                           input_samples = [
                                            'ZggNLO',
                           ],
                           plotColor=ROOT.kOrange+2,
                           isActive=True,
                          )
    samples.AddSampleGroup( 'Top', legend_name='Top', 
                           input_samples = [
                                           't_s'                     ,
                                           't_t'                     ,
                                           't_tW'                    ,
                                           'tbar_s'                  ,
                                           'tbar_t'                  ,
                                           'tbar_tW'                 ,
                                           'ttW'                     ,
                                           'ttZ'                     ,
                                           'ttjets_1l'               ,
                                           'ttjets_2l'               ,
                           ],
                           plotColor=ROOT.kGreen-3,
                           isActive=True,
                          )

    samples.AddSampleGroup( 'ttgamma', legend_name='tt #gamma', 
                           input_samples = [
                                           'ttg'               ,
                           ],
                           plotColor=ROOT.kGreen+4,
                          )

    samples.AddSampleGroup( 'WZ', legend_name='WZ', 
                           input_samples = [
                                           'WZA'                 ,
                           ],
                           plotColor=ROOT.kRed-10,
                          )

    samples.AddSampleGroup( 'VH', legend_name='WH/ZH, m_{H} = 125 GeV', 
                           input_samples = [
                                           'WH_ZH_125'                     ,
                           ],
                           plotColor=ROOT.kRed+2,
                          )
    samples.AddSampleGroup( 'MultiBoson', legend_name='Other Multiboson', 
                           input_samples = [
                                           'WWg'                     ,
                                           'WWW'                     ,
                                           'WWZ'                     ,
                                           'WZZ'                     ,
                                           'ZZZ'                     ,
                                           'WW_2l2nu'                ,
                                           'WZ_2l2q'                 ,
                                           'WZ_3lnu'                 ,
                                           'ZZ_2e2mu'                ,
                                           'ZZ_2e2tau'               ,
                                           'ZZ_2l2q'                 ,
                                           'ZZ_2q2nu'                ,
                                           'ZZ_2l2nu'                ,
                                           'ZZ_2mu2tau'              ,
                                           'ZZ_4e'                   ,
                                           'ZZ_4mu'                  ,
                                           'ZZ_4tau'                 ,
                           ],
                           plotColor=ROOT.kBlue-10,
                           isActive=True,
                          )





def print_examples() :
    pass
