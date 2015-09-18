

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
    samples.AddSample('DYJetsToLL'                   , path='job_summer12_DYJetsToLL'         ,  isActive=False, useXSFile=True )

    samples.AddSample('DYJetsToLLPhOlap'             , path='job_summer12_DYJetsToLLPhOlapWithSF'     ,  isActive=False, useXSFile=True, XSName='DYJetsToLL')
    samples.AddSample('diphoton_box_10to25'          , path='job_summer12_diphoton_box_10to25'  ,  isActive=False, useXSFile=True )
    samples.AddSample('diphoton_box_250toInf'        , path='job_summer12_diphoton_box_250toInf',  isActive=False, useXSFile=True )
    samples.AddSample('diphoton_box_25to250'         , path='job_summer12_diphoton_box_25to250' ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_s'                       , path='job_summer12_tbar_s'               ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_t'                       , path='job_summer12_tbar_t'               ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_tW'                      , path='job_summer12_tbar_tW'              ,  isActive=False, useXSFile=True )
    samples.AddSample('t_s'                          , path='job_summer12_t_s'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('t_t'                          , path='job_summer12_t_t'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('ttg'                          , path='job_summer12_ttg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('ttjets_1l'                    , path='job_summer12_ttjets_1l'            ,  isActive=False, useXSFile=True )
    samples.AddSample('ttjets_2l'                    , path='job_summer12_ttjets_2l'            ,  isActive=False, useXSFile=True )
    #samples.AddSample('ttjets_1l'                    , path='job_summer12_ttjets_1lPhOlap'            ,  isActive=False, useXSFile=True )
    #samples.AddSample('ttjets_2l'                    , path='job_summer12_ttjets_2lPhOlap'            ,  isActive=False, useXSFile=True )
    samples.AddSample('t_tW'                         , path='job_summer12_t_tW'                 ,  isActive=False, useXSFile=True )
    samples.AddSample('WAA_ISR'                      , path='job_summer12_WAA_ISR'              ,  isActive=False, useXSFile=True )
    samples.AddSample('Wgg_FSR'                      , path='job_summer12_Wgg_FSR'              ,  isActive=False, useXSFile=True )
    samples.AddSample('NLO_WAA_ISR'                  , path='job_NLO_WAA_ISR'              ,  isActive=False, useXSFile=True )
    samples.AddSample('NLO_WAA_FSR'                  , path='job_NLO_WAA_FSR'              ,  isActive=False, useXSFile=True )
    #samples.AddSample('WAA_ISR'                      , path='job_summer12_WAA_ISR'              ,  isActive=False, useXSFile=False, scale=1.0 )
    #samples.AddSample('Wgg_FSR'                      , path='job_summer12_Wgg_FSR'              ,  isActive=False, useXSFile=False, scale=1.0 )
    samples.AddSample('Wg'                           , path='job_summer12_Wg'                  ,  isActive=False, useXSFile=True )
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
    samples.AddSample('Zgg'                          , path='llaa_nlo_part1_ggNtuple'           ,  isActive=False, useXSFile=True, XSName='ZggNLO' )
    #samples.AddSample('Zg'                           , path='job_summer12_ZgOnePhot'                   ,  isActive=False, useXSFile=True )
    samples.AddSample('Zg'                           , path='job_summer12_ZgWithSF'             ,  isActive=False, useXSFile=True, XSName='Zg' )
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
    samples.AddSample('ggZZ_2l2l2PhFilt'                , path='job_summer12_ggZZ_2l2l2PhFilt'        , isActive=True, useXSFile=True, XSName='ggZZ_2l2l' )
    samples.AddSample('ggZZ_4l2PhFilt'                  , path='job_summer12_ggZZ_4l2PhFilt'          , isActive=True, useXSFile=True, XSName='ggZZ_4l' )
    #samples.AddSample('ttg2PhFilt'                      , path='job_summer12_ttg2PhFilt'              , isActive=True, useXSFile=True, XSName='ttg' )
    ##samples.AddSample('WW_2l2nu2PhFilt'                 , path='job_summer12_WW_2l2nu2PhFilt'         , isActive=True, useXSFile=True, XSName='WW_2l2nu' )
    #samples.AddSample('WWg2PhFilt'                      , path='job_summer12_WWg2PhFilt'              , isActive=True, useXSFile=True, XSName='WWg' )
    #samples.AddSample('WWW2PhFilt'                      , path='job_summer12_WWW2PhFilt'              , isActive=True, useXSFile=True, XSName='WWW' )
    #samples.AddSample('WWZ2PhFilt'                      , path='job_summer12_WWZ2PhFilt'              , isActive=True, useXSFile=True, XSName='WWZ' )
    ##samples.AddSample('WZ_3lnu2PhFilt'                  , path='job_summer12_WZ_3lnu2PhFilt'          , isActive=True, useXSFile=True, XSName='WZ_3lnu' )
    #samples.AddSample('WZZ2PhFilt'                      , path='job_summer12_WZZ2PhFilt'              , isActive=True, useXSFile=True, XSName='WZZ' )
    ##samples.AddSample('Zgg'                          , path='job_summer12_Zgg'                  , isActive=False, useXSFile=True, XSName='Zg' )
    #samples.AddSample('ZZ_2e2mu2PhFilt'                 , path='job_summer12_ZZ_2e2mu2PhFilt'         , isActive=True, useXSFile=True, XSName='ZZ_2e2mu' )
    #samples.AddSample('ZZ_2e2tau2PhFilt'                , path='job_summer12_ZZ_2e2tau2PhFilt'        , isActive=True, useXSFile=True, XSName='ZZ_2e2tau' )
    #samples.AddSample('ZZ_2l2nu2PhFilt'                 , path='job_summer12_ZZ_2l2nu2PhFilt'         , isActive=True, useXSFile=True, XSName='ZZ_2l2nu' )
    #samples.AddSample('ZZ_2l2q2PhFilt'                  , path='job_summer12_ZZ_2l2q2PhFilt'          , isActive=True, useXSFile=True, XSName='ZZ_2l2q' )
    #samples.AddSample('ZZ_2mu2tau2PhFilt'               , path='job_summer12_ZZ_2mu2tau2PhFilt'       , isActive=True, useXSFile=True, XSName='ZZ_2mu2tau' )
    #samples.AddSample('ZZ_2q2nu2PhFilt'                 , path='job_summer12_ZZ_2q2nu2PhFilt'         , isActive=True, useXSFile=True, XSName='ZZ_2q2nu' )
    #samples.AddSample('ZZ_4e2PhFilt'                    , path='job_summer12_ZZ_4e2PhFilt'            , isActive=True, useXSFile=True, XSName='ZZ_4e' )
    #samples.AddSample('ZZ_4mu2PhFilt'                   , path='job_summer12_ZZ_4mu2PhFilt'           , isActive=True, useXSFile=True, XSName='ZZ_4mu' )
    #samples.AddSample('ZZ_4tau2PhFilt'                  , path='job_summer12_ZZ_4tau2PhFilt'          , isActive=True, useXSFile=True, XSName='ZZ_4tau' )
    #samples.AddSample('ZZZ2PhFilt'                      , path='job_summer12_ZZZ2PhFilt'              , isActive=True, useXSFile=True, XSName='ZZZ' )
    samples.AddSample('Wgg_aQGC'                        , path='job_LNuAA_LM0123_Reweight'            , isActive=True, useXSFile=True, XSName='Wgg', isSignal=True, plotColor=ROOT.kRed )


    #samples.AddSample('MultiJet', path='job_MultiJet_2012a_Jan22rereco', isActive=True )

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             #'electron_2012a_Jan22rereco',
                                             #'electron_2012b_Jan22rereco',
                                             #'electron_2012c_Jan2012rereco',
                                             #'electron_2012d_Jan22rereco',
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
                                             'NLO_WAA_ISR',
                                             'NLO_WAA_FSR',
                                            ],
                           plotColor=ROOT.kRed,
                           isSignal=False,
                           isActive=False
                          )


    #samples.AddSampleGroup( 'Single Photon', legend_name='Single photon', 
    #                    input_samples = [
    #                                       'gjet_pt20to40_doubleEM'  ,
    #                                       'gjet_pt40_doubleEM'      ,
    #                    ],
    #                       plotColor=ROOT.kYellow,
    #                      )


    samples.AddSampleGroup( 'Zgammastar', legend_name='Z/#gamma * ', 
                            input_samples = [
                                             'DYJetsToLLPhOlap'
                                             #'DYJetsToLL'
                                             #'Zg',
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
                          )
    samples.AddSampleGroup( 'Zgammagamma', legend_name='Z#gamma#gamma', 
                           input_samples = [
                                            'Zgg',
                           ],
                           plotColor=ROOT.kOrange+2,
                           isActive=True,
                          )

    samples.AddSampleGroup( 'Wjets', legend_name='W+jets', 
                            input_samples = [
                                             '_Wjets',
                                            ],
                           plotColor=ROOT.kRed-7,
                           isActive=True,
                          )

    samples.AddSampleGroup( 'Wgamma', legend_name='W#gamma', 
                           input_samples = [
                                            'Wg',
                           ],
                           plotColor=ROOT.kBlue-6,
                           isSignal=False,
                           isActive=True,
                          )

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

    #samples.AddSampleGroup( 'OtherDiPhoton', legend_name='other real diphoton', 
    #                       input_samples = [
    #                                        'ggZZ_2l2lgFSR',
    #                                        'ggZZ_4lgFSR',
    #                                        'ttggFSR',
    #                                        'WW_2l2nugFSR',
    #                                        'WWggFSR',
    #                                        'WWWgFSR',
    #                                        'WWZgFSR',
    #                                        'WZ_3lnugFSR',
    #                                        'WZZgFSR',
    #                                        #'ZggFSR',
    #                                        'ZZ_2e2mugFSR',
    #                                        'ZZ_2e2taugFSR',
    #                                        'ZZ_2l2nugFSR',
    #                                        'ZZ_2l2qgFSR',
    #                                        'ZZ_2mu2taugFSR',
    #                                        'ZZ_2q2nugFSR',
    #                                        'ZZ_4egFSR',
    #                                        'ZZ_4mugFSR',
    #                                        'ZZ_4taugFSR',
    #                                        'ZZZgFSR',
    #                       ],
    #                           plotColor=ROOT.kBlue,
    #                           isActive=True,
    #                       )
    samples.AddSampleGroup( 'DiPhoton', legend_name='DiPhoton', 
                           input_samples = [
                                           'diphoton_box_10to25'                     ,
                                           'diphoton_box_25to250'                     ,
                                           'diphoton_box_250toInf'                     ,
                           ],
                           plotColor=ROOT.kYellow-3,
                           isActive=False,
                          )

    samples.AddSampleGroup( 'VH', legend_name='WH/ZH, m_{H} = 125 GeV', 
                           input_samples = [
                                           'WH_ZH_125'                     ,
                           ],
                           plotColor=ROOT.kRed+2,
                          )
    #samples.AddSampleGroup( 'DiBoson', legend_name='WW/WZ/ZZ', 
    #                       input_samples = [
    #                                       'WW_2l2nu'                ,
    #                                       'WZ_2l2q'                 ,
    #                                       'WZ_3lnu'                 ,
    #                                       'ZZ_2e2mu'                ,
    #                                       'ZZ_2e2tau'               ,
    #                                       'ZZ_2l2q'                 ,
    #                                       'ZZ_2q2nu'                ,
    #                                       'ZZ_2l2nu'                ,
    #                                       'ZZ_2mu2tau'              ,
    #                                       'ZZ_4e'                   ,
    #                                       'ZZ_4mu'                  ,
    #                                       'ZZ_4tau'                 ,
    #                      ],
    #                       plotColor=ROOT.kRed-3,
    #                      )
    samples.AddSampleGroup( 'WW', legend_name='WW', 
                           input_samples = [
                                           'WW_2l2nu'                ,
                          ],
                           plotColor=ROOT.kRed-3,
                          )
    samples.AddSampleGroup( 'WZ', legend_name='WZ', 
                           input_samples = [
                                           'WZ_2l2q'                 ,
                                           'WZ_3lnu'                 ,
                          ],
                           plotColor=ROOT.kBlue-3,
                          )
    samples.AddSampleGroup( 'ZZ', legend_name='ZZ', 
                           input_samples = [
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
                           plotColor=ROOT.kGreen-3,
                          )
    samples.AddSampleGroup( 'TriBoson', legend_name='Other Triboson', 
                           input_samples = [
                                           'WWg'                     ,
                                           'WWW'                     ,
                                           'WWZ'                     ,
                                           'WZZ'                     ,
                                           'ZZZ'                     ,
                           ],
                           plotColor=ROOT.kBlue-10,
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
                                           'ttg'                     ,
                                           'ttjets_1l'               ,
                                           'ttjets_2l'               ,
                           ],
                           plotColor=ROOT.kGreen-3,
                           isActive=False,
                          )

    #samples.AddSampleGroup( 'MultiBoson', legend_name='Other Multiboson', 
    #                       input_samples = [
    #                                       'WWg'                     ,
    #                                       'WWW'                     ,
    #                                       'WWZ'                     ,
    #                                       'WZZ'                     ,
    #                                       'ZZZ'                     ,
    #                                       'WW_2l2nu'                ,
    #                                       'WZ_2l2q'                 ,
    #                                       'WZ_3lnu'                 ,
    #                                       'ZZ_2e2mu'                ,
    #                                       'ZZ_2e2tau'               ,
    #                                       'ZZ_2l2q'                 ,
    #                                       'ZZ_2q2nu'                ,
    #                                       'ZZ_2l2nu'                ,
    #                                       'ZZ_2mu2tau'              ,
    #                                       'ZZ_4e'                   ,
    #                                       'ZZ_4mu'                  ,
    #                                       'ZZ_4tau'                 ,
    #                       ],
    #                       plotColor=ROOT.kBlue-10,
    #                      )


    samples.AddSampleGroup( 'ttgamma', legend_name='tt #gamma', 
                           input_samples = [
                                           'ttg'               ,
                           ],
                           plotColor=ROOT.kGreen+4,
                          )
    samples.AddSampleGroup( 'Top1l', legend_name='tt #rightarrow l#nu jj + X', 
                           input_samples = [
                                           'ttjets_1l'               ,
                           ],
                           plotColor=ROOT.kGreen,
                          )
    samples.AddSampleGroup( 'Top2l', legend_name='tt #rightarrow l#nu l#nu + X', 
                           input_samples = [
                                           'ttjets_2l'               ,
                           ],
                           plotColor=ROOT.kGreen-3,
                          )

#    samples.AddSampleGroup( 'MCBkg', legend_name='MCBkg', isActive=False,
#                            input_samples = [
#                                             #'DYJetsToLL',
#                                             'Inclusive W',
#                                             'Wgamma',
#                                             'DiBoson',
#                                             'TriBoson',
#                                             'Top',
#                                             'VH',
#                                        
#                           ],
#                           plotColor=ROOT.kGreen,
#                           scale=-1,
#                          )
#
#    samples.AddSampleGroup( 'DataMCSubtracted', legend_name='Data, bkg subtracted', isActive=False,
#                            input_samples = ['Data', 'MCBkg'],
#                            plotColor=ROOT.kGreen,isSignal=True
#                          )
#                                            
#
    #samples.AddSampleGroup( 'Data', legend_name='Data (generated)', 
    #                        input_samples = [
    #                                        'Zgammastar',
    #                                        'Zgamma',
    #                                        'Inclusive W',
    #                                        'Wgamma',
    #                                        'Wgammagamma',
    #                                        'DiBoson',
    #                                        'TriBoson',
    #                                        'Top',
    #                                        'VH',
    #                                        ],
    #                       plotColor=ROOT.kBlack,
    #                       isData=True,
    #                      )

    samples.AddSampleGroup( 'WjetsWgamma', legend_name = 'W+jets + W#gamma',
                           input_samples=[
                           'Wgamma', 
                           'Inclusive W',
                           ],
                           plotColor=ROOT.kGray,
                           isActive=False,
                          )
    samples.AddSampleGroup( 'ZjetsZgamma', legend_name = 'Z+jets + Z#gamma',
                           input_samples=[
                           'DYJetsToLLPhOlap', 
                           'Zgamma',
                           ],
                           plotColor=ROOT.kSpring,
                           isActive=False,
                          )

    samples.AddSampleGroup( 'WjetsZjets', legend_name = 'W+jets + Z+jets',
                           input_samples=[
                           'DYJetsToLLPhOlap', 
                           'WjetsPhOlap',
                           ],
                           plotColor=ROOT.kSpring,
                           isActive=False,
                          )

    samples.AddSampleGroup( 'RealPhotons', legend_name='Real photons', 
                        input_samples = [
                            'Zg',
                        ],
                           plotColor=ROOT.kYellow,
                           scale=-1,
                           isActive=False
                          )

    samples.AddSampleGroup( 'DataRealPhotonSub', legend_name='Fake photons', 
                        input_samples = [
                            'Data',
                            'RealPhotons',
                        ],
                           plotColor=ROOT.kYellow,
                           isActive=False,
                          )

    samples.AddSampleGroup( 'ElectronRealPhotonSub', legend_name='Fake photons', 
                        input_samples = [
                            'Electron',
                            'RealPhotons',
                        ],
                           plotColor=ROOT.kYellow,
                           isActive=False,
                          )

    samples.AddSampleGroup( 'MuonRealPhotonSub', legend_name='Fake photons', 
                        input_samples = [
                            'Muon',
                            'RealPhotons',
                        ],
                           plotColor=ROOT.kYellow,
                           isActive=False,
                          )

    samples.AddSampleGroup( 'AllBkg', legend_name='allBkg', 
                        input_samples = [
                            'Zgammastar',
                            'Zgamma',
                            'Wjets',
                            'Wgamma',
                            'MultiBoson',
                            'Top',
                            'DiPhoton',
                            'VH',
                        ],
                           plotColor=ROOT.kYellow,
                           isActive=False,
                          )



def print_examples() :
    pass
