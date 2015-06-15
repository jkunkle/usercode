

def config_samples(samples) :

    import ROOT
    samples.AddSample('electron_2012a_Jan22rereco'   , path='job_electron_2012a_Jan22rereco'    ,  isActive=False, required=True, scale=1.0 )
    samples.AddSample('electron_2012b_Jan22rereco'   , path='job_electron_2012b_Jan22rereco'    ,  isActive=False, required=True, scale=1.0 )
    samples.AddSample('electron_2012c_Jan2012rereco' , path='job_electron_2012c_Jan2012rereco'  ,  isActive=False, required=True, scale=1.0 )
    samples.AddSample('electron_2012d_Jan22rereco'   , path='job_electron_2012d_Jan22rereco'    ,  isActive=False, required=True, scale=1.0 )
    samples.AddSample('muon_2012a_Jan22rereco'       , path='job_muon_2012a_Jan22rereco'        ,  isActive=False, required=True, scale=1.0 )
    samples.AddSample('muon_2012b_Jan22rereco'       , path='job_muon_2012b_Jan22rereco'        ,  isActive=False, required=True, scale=1.0 )
    samples.AddSample('muon_2012c_Jan22rereco'       , path='job_muon_2012c_Jan22rereco'        ,  isActive=False, required=True, scale=1.0 )
    samples.AddSample('muon_2012d_Jan22rereco'       , path='job_muon_2012d_Jan22rereco'        ,  isActive=False, required=True, scale=1.0 )
    samples.AddSample('DYJetsToLL'                   , path='job_summer12_DYJetsToLL'         ,  isActive=False, useXSFile=True )

    samples.AddSample('DYJetsToLLPhOlap'             , path='job_summer12_DYJetsToLLPhOlap'     ,  isActive=False, required=True, useXSFile=True, XSName='DYJetsToLL')
    samples.AddSample('diphoton_box_10to25'          , path='job_summer12_diphoton_box_10to25'  ,  isActive=False, useXSFile=True )
    samples.AddSample('diphoton_box_250toInf'        , path='job_summer12_diphoton_box_250toInf',  isActive=False, useXSFile=True )
    samples.AddSample('diphoton_box_25to250'         , path='job_summer12_diphoton_box_25to250' ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_s'                       , path='job_summer12_tbar_s'               ,  isActive=False, required=True, useXSFile=True )
    samples.AddSample('tbar_t'                       , path='job_summer12_tbar_t'               ,  isActive=False, required=True, useXSFile=True )
    samples.AddSample('tbar_tW'                      , path='job_summer12_tbar_tW'              ,  isActive=False, required=True, useXSFile=True )
    samples.AddSample('t_s'                          , path='job_summer12_t_s'                  ,  isActive=False, required=True, useXSFile=True )
    samples.AddSample('t_t'                          , path='job_summer12_t_t'                  ,  isActive=False, required=True, useXSFile=True )
    samples.AddSample('ttg'                          , path='job_summer12_ttg'                  ,  isActive=False, required=True, useXSFile=True )
    samples.AddSample('ttjets_1lPhOlap'              , path='job_summer12_ttjets_1lPhOlap'      ,  isActive=False, required=True, useXSFile=True, XSName='ttjets_1l' )
    samples.AddSample('ttjets_2lPhOlap'              , path='job_summer12_ttjets_2lPhOlap'      ,  isActive=False, required=True, useXSFile=True, XSName='ttjets_2l' )
    samples.AddSample('t_tW'                         , path='job_summer12_t_tW'                 ,  isActive=False, required=True, useXSFile=True )
    samples.AddSample('WAA_ISR'                      , path='job_summer12_WAA_ISR'              ,  isActive=False, required=True, useXSFile=True )
    samples.AddSample('Wgg_FSR'                      , path='job_summer12_Wgg_FSR'              ,  isActive=False, required=True, useXSFile=True )
    #samples.AddSample('WAA_ISR'                      , path='job_summer12_WAA_ISR'              ,  isActive=False, useXSFile=False, scale=1.0 )
    #samples.AddSample('Wgg_FSR'                      , path='job_summer12_Wgg_FSR'              ,  isActive=False, useXSFile=False, scale=1.0 )
    samples.AddSample('Wg'                           , path='job_summer12_Wg'                   ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPhOlap'                     , path='job_summer12_WgPhOlap'             ,  isActive=False, required=True, useXSFile=True, XSName='Wg' )
    samples.AddSample('WH_ZH_125'                    , path='job_summer12_WH_ZH_125'            ,  isActive=False, useXSFile=True )
    samples.AddSample('_Wjets'                        , path='job_summer12_Wjets'               ,  isActive=False, useXSFile=True, XSName='Wjets' )
    samples.AddSample('WjetsPhOlap'                  , path='job_summer12_WjetsPhOlap'          ,  isActive=False, required=True, useXSFile=True, XSName='Wjets' )
    samples.AddSample('WW_2l2nu'                     , path='job_summer12_WW_2l2nu'             ,  isActive=False, useXSFile=True )
    samples.AddSample('WWg'                          , path='job_summer12_WWg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WWW'                          , path='job_summer12_WWW'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WWZ'                          , path='job_summer12_WWZ'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WZ_2l2q'                      , path='job_summer12_WZ_2l2q'              ,  isActive=False, useXSFile=True )
    samples.AddSample('WZ_3lnu'                      , path='job_summer12_WZ_3lnu'              ,  isActive=False, useXSFile=True )
    samples.AddSample('WZZ'                          , path='job_summer12_WZZ'                  ,  isActive=False, useXSFile=True )
    #samples.AddSample('Zgg'                          , path='job_summer12_ZgTwoPhot'                  ,  isActive=False, useXSFile=True, XSName='Zg' )
    #samples.AddSample('Zg'                           , path='job_summer12_ZgOnePhot'                   ,  isActive=False, useXSFile=True )
    samples.AddSample('Zg'                           , path='job_summer12_Zg'                   ,  isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('Zg2PhFilt'                    , path='job_summer12_Zg2PhFilt'            ,  isActive=False, required=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('Zgg'                          , path='job_summer12_Zgg'                  ,  isActive=False, useXSFile=True )
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
    samples.AddSample('ZgElToPh'                     , path='job_summer12_ZgElToPh'             ,  isActive=False, useXSFile=True, XSName='Zg' )

    samples.AddSample('jfaulkne_WZA2PhFilt'          , path='job_jfaulkne_WZA2PhFilt'           , isActive=False, useXSFile=True, XSName='WZA' )
    samples.AddSample('tbar_s2PhFilt'                , path='job_summer12_tbar_s2PhFilt'        , isActive=False, useXSFile=True, XSName='tbar_s')
    samples.AddSample('tbar_t2PhFilt'                , path='job_summer12_tbar_t2PhFilt'        , isActive=False, useXSFile=True, XSName='tbar_t')
    samples.AddSample('tbar_tW2PhFilt'               , path='job_summer12_tbar_tW2PhFilt'       , isActive=False, useXSFile=True, XSName='tbar_tW')
    samples.AddSample('t_s2PhFilt'                   , path='job_summer12_t_s2PhFilt'           , isActive=False, useXSFile=True, XSName='t_s')
    samples.AddSample('t_t2PhFilt'                   , path='job_summer12_t_t2PhFilt'           , isActive=False, useXSFile=True, XSName='t_t')
    samples.AddSample('ttg2PhFilt'                   , path='job_summer12_ttg2PhFilt'           , isActive=False, useXSFile=True, XSName='ttg')
    samples.AddSample('ttW2PhFilt'                   , path='job_summer12_ttW2PhFilt'           , isActive=False, useXSFile=True, XSName='ttW')
    samples.AddSample('t_tW2PhFilt'                  , path='job_summer12_t_tW2PhFilt'          , isActive=False, useXSFile=True, XSName='t_tW')
    samples.AddSample('ttZ2PhFilt'                   , path='job_summer12_ttZ2PhFilt'           , isActive=False, useXSFile=True, XSName='ttZ')
    samples.AddSample('WWg2PhFilt'                   , path='job_summer12_WWg2PhFilt'           , isActive=False, useXSFile=True, XSName='WWg')
    samples.AddSample('WWW2PhFilt'                   , path='job_summer12_WWW2PhFilt'           , isActive=False, useXSFile=True, XSName='WWW')
    samples.AddSample('WWZ2PhFilt'                   , path='job_summer12_WWZ2PhFilt'           , isActive=False, useXSFile=True, XSName='WWZ')
    samples.AddSample('WZZ2PhFilt'                   , path='job_summer12_WZZ2PhFilt'           , isActive=False, useXSFile=True, XSName='WZZ')
    samples.AddSample('Zg2PhFilt'                    , path='job_summer12_Zg2PhFilt'            , isActive=False, useXSFile=True, XSName='Zg')
    samples.AddSample('ZZ_2e2mu2PhFilt'              , path='job_summer12_ZZ_2e2mu2PhFilt'      , isActive=False, useXSFile=True, XSName='ZZ_2e2mu')
    samples.AddSample('ZZ_2e2tau2PhFilt'             , path='job_summer12_ZZ_2e2tau2PhFilt'     , isActive=False, useXSFile=True, XSName='ZZ_2e2tau')
    samples.AddSample('ZZ_2l2nu2PhFilt'              , path='job_summer12_ZZ_2l2nu2PhFilt'      , isActive=False, useXSFile=True, XSName='ZZ_2l2nu')
    samples.AddSample('ZZ_2l2q2PhFilt'               , path='job_summer12_ZZ_2l2q2PhFilt'       , isActive=False, useXSFile=True, XSName='ZZ_2l2q')
    samples.AddSample('ZZ_2mu2tau2PhFilt'            , path='job_summer12_ZZ_2mu2tau2PhFilt'    , isActive=False, useXSFile=True, XSName='ZZ_2mu2tau')
    samples.AddSample('ZZ_2q2nu2PhFilt'              , path='job_summer12_ZZ_2q2nu2PhFilt'      , isActive=False, useXSFile=True, XSName='ZZ_2q2nu')
    samples.AddSample('ZZ_4e2PhFilt'                 , path='job_summer12_ZZ_4e2PhFilt'         , isActive=False, useXSFile=True, XSName='ZZ_4e')
    samples.AddSample('ZZ_4mu2PhFilt'                , path='job_summer12_ZZ_4mu2PhFilt'        , isActive=False, useXSFile=True, XSName='ZZ_4mu')
    samples.AddSample('ZZ_4tau2PhFilt'               , path='job_summer12_ZZ_4tau2PhFilt'       , isActive=False, useXSFile=True, XSName='ZZ_4tau')
    samples.AddSample('ZZZ2PhFilt'                   , path='job_summer12_ZZZ2PhFilt'           , isActive=False, useXSFile=True, XSName='ZZZ')

    #samples.AddSample('MultiJet', path='job_MultiJet_2012a_Jan22rereco', isActive=True )

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             'electron_2012a_Jan22rereco',
                                             'electron_2012b_Jan22rereco',
                                             'electron_2012c_Jan2012rereco',
                                             'electron_2012d_Jan22rereco',
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
    samples.AddSampleGroup( 'Electron', legend_name='Data', 
                            input_samples = [
                                             'electron_2012a_Jan22rereco',
                                             'electron_2012b_Jan22rereco',
                                             'electron_2012c_Jan2012rereco',
                                             'electron_2012d_Jan22rereco',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                           isActive=False,
                          )

    samples.AddSampleGroup( 'Wgg', legend_name='W#gamma#gamma', 
                            input_samples = [
                                             'WAA_ISR',
                                             'Wgg_FSR',
                                            ],
                           plotColor=ROOT.kRed,
                           isSignal=True,
                          )


    #samples.AddSampleGroup( 'Single Photon', legend_name='Single photon', 
    #                    input_samples = [
    #                                       'gjet_pt20to40_doubleEM'  ,
    #                                       'gjet_pt40_doubleEM'      ,
    #                    ],
    #                       plotColor=ROOT.kYellow,
    #                      )



    samples.AddSampleGroup( 'ISR', legend_name='W#gamma#gamma -- ISR', 
                            input_samples = [
                                             'WAA_ISR',
                                            ],
                           plotColor=ROOT.kRed,
                           isSignal=True,
                           isActive=False,
                          )

    samples.AddSampleGroup( 'FSR', legend_name='W#gamma#gamma -- FSR', 
                            input_samples = [
                                             'Wgg_FSR',
                                            ],
                           plotColor=ROOT.kViolet,
                           isSignal=True,
                           isActive=False,
                          )
    samples.AddSampleGroup( 'Zgammagamma', legend_name='Z#gamma#gamma', 
                           input_samples = [
                                            'Zg2PhFilt',
                           ],
                           plotColor=ROOT.kOrange+2,
                           isActive=True,
                          )

    samples.AddSampleGroup( 'OtherDiPhoton', legend_name='other real diphoton', 
                           input_samples = [
                                            'ggZZ_2l2l2PhFilt',
                                            'ggZZ_4l2PhFilt',
                                            'ttg2PhFilt',
                                            't_t2PhFilt',
                                            't_s2PhFilt',
                                            't_tW2PhFilt',
                                            'tbar_t2PhFilt',
                                            'tbar_s2PhFilt',
                                            'tbar_tW2PhFilt',
                                            'WW_2l2nu2PhFilt',
                                            'WWg2PhFilt',
                                            'WWW2PhFilt',
                                            'WWZ2PhFilt',
                                            'jfaulkne_WZA2PhFilt',
                                            'WZZ2PhFilt',
                                            'ZZ_2e2mu2PhFilt',
                                            'ZZ_2e2tau2PhFilt',
                                            'ZZ_2l2nu2PhFilt',
                                            'ZZ_2l2q2PhFilt',
                                            'ZZ_2mu2tau2PhFilt',
                                            'ZZ_2q2nu2PhFilt',
                                            'ZZ_4e2PhFilt',
                                            'ZZ_4mu2PhFilt',
                                            'ZZ_4tau2PhFilt',
                                            'ZZZ2PhFilt',
                           ],
                               plotColor=ROOT.kBlue,
                               isActive=True,
                           )

    samples.AddSampleGroup( 'DiPhoton', legend_name='DiPhoton', 
                           input_samples = [
                                           'diphoton_box_10to25'                     ,
                                           'diphoton_box_25to250'                     ,
                                           'diphoton_box_250toInf'                     ,
                           ],
                           plotColor=ROOT.kYellow-3,
                           isActive=True,
                          )

    samples.AddSampleGroup( 'VH', legend_name='WH/ZH, m_{H} = 125 GeV', 
                           input_samples = [
                                           'WH_ZH_125'                     ,
                           ],
                           plotColor=ROOT.kRed+2,
                           isActive=False,
                          )


def print_examples() :
    pass
