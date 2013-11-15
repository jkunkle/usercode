

def config_samples(samples) :

    import ROOT

    samples.AddSample('1electron_2012b_Jul13rereco_run1' , path='job_1electron_2012b_Jul13rereco_run1' , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('1electron_2012b_Jul13rereco_run2' , path='job_1electron_2012b_Jul13rereco_run2' , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('1electron_2012c_Aug24rereco'      , path='job_1electron_2012c_Aug24rereco'      , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('1electron_2012c_Dec11rereco'      , path='job_1electron_2012c_Dec11rereco'      , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('1electron_2012c_PRv2_part1'       , path='job_1electron_2012c_PRv2_part1'       , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('1electron_2012c_PRv2_part2'       , path='job_1electron_2012c_PRv2_part2'       , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('1electron_2012c_PRv2_part3'       , path='job_1electron_2012c_PRv2_part3'       , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('1electron_2012d_PRv1_part1'       , path='job_1electron_2012d_PRv1_part1'       , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('1electron_2012d_PRv1_part2'       , path='job_1electron_2012d_PRv1_part2'       , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('electron_2012a_Aug6rereco'        , path='job_electron_2012a_Aug6rereco'        , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('electron_2012a_Jul13rereco'       , path='job_electron_2012a_Jul13rereco'       , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('muon_2012a_Aug6rereco'            , path='job_muon_2012a_Aug6rereco'            , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('muon_2012a_Jul13rereco'           , path='job_muon_2012a_Jul13rereco'           , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('muon_2012b_Jul13rereco'           , path='job_muon_2012b_Jul13rereco'           , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('muon_2012c_Aug24rereco'           , path='job_muon_2012c_Aug24rereco'           , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('muon_2012c_Dec11rereco'           , path='job_muon_2012c_Dec11rereco'           , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('muon_2012c_PRv2'                  , path='job_muon_2012c_PRv2'                  , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('muon_2012c_PRv21'                 , path='job_muon_2012c_PRv21'                 , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('muon_2012d_PRv1'                  , path='job_muon_2012d_PRv1'                  , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('muon_2012d_PRv11'                 , path='job_muon_2012d_PRv11'                 , filekey='tree.root', disableDraw=True, scale=1.0 );
    samples.AddSample('DYJetsToLL'              , path='job_summer12_DYJetsToLL'              , filekey='tree.root', disableDraw=True, useXSFile=True );
    #samples.AddSample('Zgammastar'              , path='job_summer12_DYJetsToLL'              , filekey='tree.root', disableDraw=False, useXSFile=True );
    samples.AddSample('LNuGG_FSR'               , path='job_summer12_LNuGG_FSR'               , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('LNuGG_ISR'               , path='job_summer12_LNuGG_ISR'               , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('WJetsToLNu1'             , path='job_summer12_WJetsToLNu1'             , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('Wg'                      , path='job_summer12_Wg'                      , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('WJetsToLNu2'             , path='job_summer12_WJetsToLNu2'             , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('WWW'                     , path='job_summer12_WWW'                     , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('WWZ'                     , path='job_summer12_WWZ'                     , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('WW_2l2nu'                , path='job_summer12_WW_2l2nu'                , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('WZZ'                     , path='job_summer12_WZZ'                     , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('WZ_2l2q'                 , path='job_summer12_WZ_2l2q'                 , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('WZ_3lnu'                 , path='job_summer12_WZ_3lnu'                 , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ZZZ'                     , path='job_summer12_ZZZ'                     , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ZZ_2e2mu'                , path='job_summer12_ZZ_2e2mu'                , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ZZ_2e2tau'               , path='job_summer12_ZZ_2e2tau'               , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ZZ_2l2q'                 , path='job_summer12_ZZ_2l2q'                 , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ZZ_2mu2tau'              , path='job_summer12_ZZ_2mu2tau'              , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ZZ_4e'                   , path='job_summer12_ZZ_4e'                   , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ZZ_4mu'                  , path='job_summer12_ZZ_4mu'                  , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ZZ_4tau'                 , path='job_summer12_ZZ_4tau'                 , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('Zg'                      , path='job_summer12_Zg'                      , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('gjet_pt20to40_doubleEM'  , path='job_summer12_gjet_pt20to40_doubleEM'  , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('gjet_pt40_doubleEM'      , path='job_summer12_gjet_pt40_doubleEM'      , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('t_s'                     , path='job_summer12_t_s'                     , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('t_t'                     , path='job_summer12_t_t'                     , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('t_tW'                    , path='job_summer12_t_tW'                    , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('tbar_s'                  , path='job_summer12_tbar_s'                  , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('tbar_t'                  , path='job_summer12_tbar_t'                  , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('tbar_tW'                 , path='job_summer12_tbar_tW'                 , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ttW'                     , path='job_summer12_ttW'                     , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ttZ'                     , path='job_summer12_ttZ'                     , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ttg'                     , path='job_summer12_ttg'                     , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ttjets_1l'               , path='job_summer12_ttjets_1l'               , filekey='tree.root', disableDraw=True, useXSFile=True );
    samples.AddSample('ttjets_2l'               , path='job_summer12_ttjets_2l'               , filekey='tree.root', disableDraw=True, useXSFile=True );

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                              '1electron_2012b_Jul13rereco_run1' ,
                                              '1electron_2012b_Jul13rereco_run2' ,
                                              '1electron_2012c_Aug24rereco'      ,
                                              '1electron_2012c_Dec11rereco'      ,
                                              '1electron_2012c_PRv2_part1'       ,
                                              '1electron_2012c_PRv2_part2'       ,
                                              '1electron_2012c_PRv2_part3'       ,
                                              '1electron_2012d_PRv1_part1'       ,
                                              '1electron_2012d_PRv1_part2'       ,
                                              'electron_2012a_Aug6rereco'        ,
                                              'electron_2012a_Jul13rereco'       ,
                                              'muon_2012a_Aug6rereco'            ,
                                              'muon_2012a_Jul13rereco'           ,
                                              'muon_2012b_Jul13rereco'           ,
                                              'muon_2012c_Aug24rereco'           ,
                                              'muon_2012c_Dec11rereco'           ,
                                              'muon_2012c_PRv2'                  ,
                                              'muon_2012c_PRv21'                 ,
                                              'muon_2012d_PRv1'                  ,
                                              'muon_2012d_PRv11'                 ,
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
    #samples.AddSampleGroup( 'Inclusive W', legend_name='Inclusive W', 
    #                        input_samples = [
    #                                         'WJetsToLNu1',
    #                                         'WJetsToLNu2',
    #                                        ],
    #                       plotColor=ROOT.kPink,
    #                      )

    samples.AddSampleGroup( 'Zgammastar', legend_name='Z/#gamma * ', 
                            input_samples = [
                                             'DYJetsToLL',
                                            ],
                           plotColor=ROOT.kCyan,
                           scale=0.887,
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
                                             'LNuGG_FSR',
                                             'LNuGG_ISR',
                                            ],
                           plotColor=ROOT.kRed,
                           isSignal=True
                          )

    samples.AddSampleGroup( 'DiBoson', legend_name='WW/WZ/ZZ', 
                           input_samples = [
                                           'WW_2l2nu'                ,
                                           'WZ_2l2q'                 ,
                                           'WZ_3lnu'                 ,
                                           'ZZ_2e2mu'                ,
                                           'ZZ_2e2tau'               ,
                                           'ZZ_2l2q'                 ,
                                           'ZZ_2mu2tau'              ,
                                           'ZZ_4e'                   ,
                                           'ZZ_4mu'                  ,
                                           'ZZ_4tau'                 ,
                          ],
                           plotColor=ROOT.kRed-3,
                          )
    #samples.AddSampleGroup( 'TriBoson', legend_name='WWW/WWZ/WZZ/ZZZ', 
    #                       input_samples = [
    #                                       'WWW'                     ,
    #                                       'WWZ'                     ,
    #                                       'WZZ'                     ,
    #                                       'ZZZ'                     ,
    #                       ],
    #                       plotColor=ROOT.kBlue-4,
    #                      )

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

    #samples.AddSampleGroup( 'DataMCSubtracted', legend_name='Data, bkg subtracted', disableDraw=False,
    #                        input_samples = ['Data', 'AllMC'],
    #                        plotColor=ROOT.kGreen,isSignal=True
    #                      )
    #                                         



def print_examples() :
    pass
