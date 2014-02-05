

def config_samples(samples) :

    import ROOT
    samples.AddSample('electron_2012a_Jan22rereco'   , path='job_electron_2012a_Jan22rereco'    ,  disableDraw=True, scale=1.0 )
    samples.AddSample('electron_2012b_Jan22rereco'   , path='job_electron_2012b_Jan22rereco'   ,  disableDraw=True, scale=1.0 )
    samples.AddSample('electron_2012c_Jan2012rereco' , path='job_electron_2012c_Jan2012rereco' ,  disableDraw=True, scale=1.0 )
    samples.AddSample('electron_2012d_Jan22rereco'   , path='job_electron_2012d_Jan22rereco'   ,  disableDraw=True, scale=1.0 )
    samples.AddSample('muon_2012a_Jan22rereco'       , path='job_muon_2012a_Jan22rereco'       ,  disableDraw=True, scale=1.0 )
    samples.AddSample('muon_2012b_Jan22rereco'       , path='job_muon_2012b_Jan22rereco'       ,  disableDraw=True, scale=1.0 )
    samples.AddSample('muon_2012c_Jan22rereco'       , path='job_muon_2012c_Jan22rereco'       ,  disableDraw=True, scale=1.0 )
    samples.AddSample('muon_2012d_Jan22rereco'       , path='job_muon_2012d_Jan22rereco'       ,  disableDraw=True, scale=1.0 )
    samples.AddSample('diphoton_box_10to25'          , path='job_summer12_diphoton_box_10to25'  ,  disableDraw=True, useXSFile=True )
    samples.AddSample('diphoton_box_250toInf'        , path='job_summer12_diphoton_box_250toInf',  disableDraw=True, useXSFile=True )
    samples.AddSample('diphoton_box_25to250'         , path='job_summer12_diphoton_box_25to250' ,  disableDraw=True, useXSFile=True )
    samples.AddSample('DYJetsToLL'                   , path='job_summer12_DYJetsToLL'           ,  disableDraw=True, useXSFile=True )
    #samples.AddSample('DYJetsToLL'                   , path='DYJetsToLLPhOlap'           ,  disableDraw=True, useXSFile=True )
    samples.AddSample('tbar_s'                       , path='job_summer12_tbar_s'               ,  disableDraw=True, useXSFile=True )
    samples.AddSample('tbar_t'                       , path='job_summer12_tbar_t'               ,  disableDraw=True, useXSFile=True )
    samples.AddSample('tbar_tW'                      , path='job_summer12_tbar_tW'              ,  disableDraw=True, useXSFile=True )
    samples.AddSample('t_s'                          , path='job_summer12_t_s'                  ,  disableDraw=True, useXSFile=True )
    samples.AddSample('t_t'                          , path='job_summer12_t_t'                  ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ttg'                          , path='job_summer12_ttg'                  ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ttjets_1l'                    , path='job_summer12_ttjets_1l'            ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ttjets_2l'                    , path='job_summer12_ttjets_2l'            ,  disableDraw=True, useXSFile=True )
    samples.AddSample('t_tW'                         , path='job_summer12_t_tW'                 ,  disableDraw=True, useXSFile=True )
    samples.AddSample('WAA_ISR'                      , path='job_summer12_WAA_ISR'              ,  disableDraw=True, useXSFile=True )
    samples.AddSample('Wg'                           , path='job_summer12_Wg'                   ,  disableDraw=True, useXSFile=True )
    #samples.AddSample('Wg'                           , path='WgPhOlap'                          ,  disableDraw=True, useXSFile=True )
    samples.AddSample('Wgg_FSR'                      , path='job_summer12_Wgg_FSR'              ,  disableDraw=True, useXSFile=True )
    samples.AddSample('WH_ZH_125'                    , path='job_summer12_WH_ZH_125'            ,  disableDraw=True, useXSFile=True )
    samples.AddSample('Wjets'                        , path='job_summer12_Wjets'                ,  disableDraw=True, useXSFile=True )
    #samples.AddSample('Wjets'                        , path='WjetsPhOlap'                       ,  disableDraw=True, useXSFile=True )
    samples.AddSample('WW_2l2nu'                     , path='job_summer12_WW_2l2nu'             ,  disableDraw=True, useXSFile=True )
    samples.AddSample('WWg'                          , path='job_summer12_WWg'                  ,  disableDraw=True, useXSFile=True )
    samples.AddSample('WWW'                          , path='job_summer12_WWW'                  ,  disableDraw=True, useXSFile=True )
    samples.AddSample('WWZ'                          , path='job_summer12_WWZ'                  ,  disableDraw=True, useXSFile=True )
    samples.AddSample('WZ_3lnu'                      , path='job_summer12_WZ_3lnu'              ,  disableDraw=True, useXSFile=True )
    samples.AddSample('WZZ'                          , path='job_summer12_WZZ'                  ,  disableDraw=True, useXSFile=True )
    samples.AddSample('Zg'                           , path='job_summer12_Zg'                   ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZ_2e2mu'                     , path='job_summer12_ZZ_2e2mu'             ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZ_2e2tau'                    , path='job_summer12_ZZ_2e2tau'            ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZ_2l2nu'                     , path='job_summer12_ZZ_2l2nu'             ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZ_2l2q'                      , path='job_summer12_ZZ_2l2q'              ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZ_2mu2tau'                   , path='job_summer12_ZZ_2mu2tau'           ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZ_2q2nu'                     , path='job_summer12_ZZ_2q2nu'             ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZ_4e'                        , path='job_summer12_ZZ_4e'                ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZ_4mu'                       , path='job_summer12_ZZ_4mu'               ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZ_4tau'                      , path='job_summer12_ZZ_4tau'              ,  disableDraw=True, useXSFile=True )
    samples.AddSample('ZZZ'                          , path='job_summer12_ZZZ'                  ,  disableDraw=True, useXSFile=True )

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

    #samples.AddSampleGroup( 'Single Photon', legend_name='Single photon', 
    #                    input_samples = [
    #                                       'gjet_pt20to40_doubleEM'  ,
    #                                       'gjet_pt40_doubleEM'      ,
    #                    ],
    #                       plotColor=ROOT.kYellow,
    #                      )
    samples.AddSampleGroup( 'Inclusive W', legend_name='W+jets', 
                            input_samples = [
                                             'Wjets',
                                            ],
                           plotColor=ROOT.kPink,
                          )

    samples.AddSampleGroup( 'Zgammastar', legend_name='Z/#gamma * ', 
                            input_samples = [
                                             'DYJetsToLL',
                                            ],
                           plotColor=ROOT.kCyan,
                           scale=1.0,
                          )

    samples.AddSampleGroup( 'Wgamma', legend_name='W#gamma', 
                           input_samples = [
                                            'Wg',
                           ],
                           plotColor=ROOT.kBlue,
                          )

    samples.AddSampleGroup( 'Zgamma', legend_name='Z#gamma', 
                           input_samples = [
                                            'Zg',
                           ],
                           plotColor=ROOT.kOrange,
                          )

    #samples.AddSampleGroup( 'WW', legend_name='WW', 
    #                       input_samples = [
    #                                       'WW_2l2nu'                ,
    #                      ],
    #                       plotColor=ROOT.kRed-3,
    #                      )
    #samples.AddSampleGroup( 'WZ', legend_name='WZ', 
    #                       input_samples = [
    #                                       'WZ_2l2q'                 ,
    #                                       'WZ_3lnu'                 ,
    #                      ],
    #                       plotColor=ROOT.kRed-1,
    #                      )
    #samples.AddSampleGroup( 'ZZ', legend_name='ZZ', 
    #                       input_samples = [
    #                                       'ZZ_2e2mu'                ,
    #                                       'ZZ_2e2tau'               ,
    #                                       'ZZ_2l2q'                 ,
    #                                       'ZZ_2mu2tau'              ,
    #                                       'ZZ_4e'                   ,
    #                                       'ZZ_4mu'                  ,
    #                                       'ZZ_4tau'                 ,
    #                      ],
    #                       plotColor=ROOT.kRed-5,
    #                      )
    samples.AddSampleGroup( 'Wgammagamma', legend_name='W#gamma#gamma', 
                            input_samples = [
                                             'WAA_ISR',
                                             'Wgg_FSR',
                                            ],
                           plotColor=ROOT.kRed,
                           isSignal=True,
                          )

    samples.AddSampleGroup( 'DiBoson', legend_name='WW/WZ/ZZ', 
                           input_samples = [
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
                           plotColor=ROOT.kRed-3,
                          )
    samples.AddSampleGroup( 'TriBoson', legend_name='Other Triboson', 
                           input_samples = [
                                           'WWg'                     ,
                                           'WWW'                     ,
                                           'WWZ'                     ,
                                           'WZZ'                     ,
                                           'ZZZ'                     ,
                           ],
                           plotColor=ROOT.kBlue-4,
                          )

    #samples.AddSampleGroup( 'Top1l', legend_name='tt #rightarrow l#nu jj + X', 
    #                       input_samples = [
    #                                       'ttjets_1l'               ,
    #                       ],
    #                       plotColor=ROOT.kGreen,
    #                      )
    #samples.AddSampleGroup( 'Top2l', legend_name='tt #rightarrow l#nu l#nu + X', 
    #                       input_samples = [
    #                                       'ttjets_2l'               ,
    #                       ],
    #                       plotColor=ROOT.kGreen-3,
    #                      )

    #samples.AddSampleGroup( 'Top2l', legend_name='tt #rightarrow l#nu l#nu + X', 
    #                       input_samples = [
    #                                       'ttjets_2l'               ,
    #                       ],
    #                       plotColor=ROOT.kGreen-3,
    #                      )

    samples.AddSampleGroup( 'Top', legend_name='Top', 
                           input_samples = [
                                           #'t_s'                     ,
                                           #'t_t'                     ,
                                           #'t_tW'                    ,
                                           #'tbar_s'                  ,
                                           #'tbar_t'                  ,
                                           #'tbar_tW'                 ,
                                           #'ttW'                     ,
                                           #'ttZ'                     ,
                                           #'ttg'                     ,
                                           'ttjets_1l'               ,
                                           'ttjets_2l'               ,
                           ],
                           plotColor=ROOT.kGreen,
                          )

    samples.AddSampleGroup( 'VH', legend_name='WH/ZH 125', 
                           input_samples = [
                                           'WH_ZH_125'                     ,
                           ],
                           plotColor=ROOT.kRed+2,
                          )
    #samples.AddSampleGroup( 'AllMC', legend_name='AllMC', disableDraw=True,
    #                        input_samples = [
    #                                         #'DYJetsToLL',
    #                                         'WJetsToLNu1',
    #                                         'WJetsToLNu2',
    #                                        'Wg',
    #                                        'Zg',
    #                                       'WW_2l2nu'                ,
    #                                       'WZ_2l2q'                 ,
    #                                       'WZ_3lnu'                 ,
    #                                       'ZZ_2e2mu'                ,
    #                                       'ZZ_2e2tau'               ,
    #                                       'ZZ_2l2q'                 ,
    #                                       'ZZ_2mu2tau'              ,
    #                                       'ZZ_4e'                   ,
    #                                       'ZZ_4mu'                  ,
    #                                       'ZZ_4tau'                 ,
    #                                       'ttjets_1l'               ,
    #                                       'ttjets_2l'               ,
    #                       ],
    #                       plotColor=ROOT.kGreen,
    #                       scale=-1,
    #                      )

    #samples.AddSampleGroup( 'DataMCSubtracted', legend_name='Data, bkg subtracted', disableDraw=True,
    #                        input_samples = ['Data', 'AllMC'],
    #                        plotColor=ROOT.kGreen,isSignal=True
    #                      )
                                             



def print_examples() :
    pass
