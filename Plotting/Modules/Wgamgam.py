

def config_samples(samples) :

    import ROOT
    #samples.AddSample('electron_2012a_Jan22rereco'   , path='job_electron_2012a_Jan22rereco'    ,  isActive=False, scale=1.0 )
    #samples.AddSample('electron_2012b_Jan22rereco'   , path='job_electron_2012b_Jan22rereco'    ,  isActive=False, scale=1.0 )
    #samples.AddSample('electron_2012c_Jan2012rereco' , path='job_electron_2012c_Jan2012rereco'  ,  isActive=False, scale=1.0 )
    #samples.AddSample('electron_2012d_Jan22rereco'   , path='job_electron_2012d_Jan22rereco'    ,  isActive=False, scale=1.0 )
    #samples.AddSample('muon_2012a_Jan22rereco'       , path='job_muon_2012a_Jan22rereco'        ,  isActive=False, scale=1.0 )
    #samples.AddSample('muon_2012b_Jan22rereco'       , path='job_muon_2012b_Jan22rereco'        ,  isActive=False, scale=1.0 )
    #samples.AddSample('muon_2012c_Jan22rereco'       , path='job_muon_2012c_Jan22rereco'        ,  isActive=False, scale=1.0 )
    #samples.AddSample('muon_2012d_Jan22rereco'       , path='job_muon_2012d_Jan22rereco'        ,  isActive=False, scale=1.0 )
    samples.AddSample('diphoton_box_10to25'          , path='job_summer12_diphoton_box_10to25'  ,  isActive=False, useXSFile=True )
    samples.AddSample('diphoton_box_250toInf'        , path='job_summer12_diphoton_box_250toInf',  isActive=False, useXSFile=True )
    samples.AddSample('diphoton_box_25to250'         , path='job_summer12_diphoton_box_25to250' ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_s'                       , path='job_summer12_tbar_s'               ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_t'                       , path='job_summer12_tbar_t'               ,  isActive=False, useXSFile=True )
    samples.AddSample('tbar_tW'                      , path='job_summer12_tbar_tW'              ,  isActive=False, useXSFile=True )
    samples.AddSample('t_s'                          , path='job_summer12_t_s'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('t_t'                          , path='job_summer12_t_t'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('ttg'                          , path='job_summer12_ttg'                  ,  isActive=False, useXSFile=True )
    #samples.AddSample('ttjets_1l'                    , path='job_summer12_ttjets_1l'            ,  isActive=False, useXSFile=True )
    #samples.AddSample('ttjets_2l'                    , path='job_summer12_ttjets_2l'            ,  isActive=False, useXSFile=True )
    samples.AddSample('ttjets_1l'                    , path='job_summer12_ttjets_1lPhOlap'            ,  isActive=False, useXSFile=True )
    samples.AddSample('ttjets_2l'                    , path='job_summer12_ttjets_2lPhOlap'            ,  isActive=False, useXSFile=True )
    samples.AddSample('t_tW'                         , path='job_summer12_t_tW'                 ,  isActive=False, useXSFile=True )
    samples.AddSample('WAA_ISR'                      , path='job_summer12_WAA_ISR'              ,  isActive=False, useXSFile=True )
    samples.AddSample('Wgg_FSR'                      , path='job_summer12_Wgg_FSR'              ,  isActive=False, useXSFile=True )
    #samples.AddSample('WAA_ISR'                      , path='job_summer12_WAA_ISR'              ,  isActive=False, useXSFile=False, scale=1.0 )
    #samples.AddSample('Wgg_FSR'                      , path='job_summer12_Wgg_FSR'              ,  isActive=False, useXSFile=False, scale=1.0 )
    #samples.AddSample('Wg'                           , path='job_summer12_Wg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('Wg'                           , path='job_summer12_WgPhOlap'          ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPt20-30'                   , path='job_summer12_WgPt20-30PhOlap'          ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPt30-50'                   , path='job_summer12_WgPt30-50PhOlap'          ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPt50-130'                   , path='job_summer12_WgPt50-130PhOlap'          ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPt130'                   , path='job_summer12_WgPt130PhOlap'          ,  isActive=False, useXSFile=True )
    samples.AddSample('WH_ZH_125'                    , path='job_summer12_WH_ZH_125'            ,  isActive=False, useXSFile=True )
    #samples.AddSample('Wjets'                        , path='job_summer12_Wjets'               ,  isActive=False, useXSFile=True )
    samples.AddSample('Wjets'                        , path='job_summer12_WjetsPhOlap'       ,  isActive=False, useXSFile=True )
    samples.AddSample('WW_2l2nu'                     , path='job_summer12_WW_2l2nu'             ,  isActive=False, useXSFile=True )
    samples.AddSample('WWg'                          , path='job_summer12_WWg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WWW'                          , path='job_summer12_WWW'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WWZ'                          , path='job_summer12_WWZ'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WZ_3lnu'                      , path='job_summer12_WZ_3lnu'              ,  isActive=False, useXSFile=True )
    samples.AddSample('WZZ'                          , path='job_summer12_WZZ'                  ,  isActive=False, useXSFile=True )
    #samples.AddSample('Zgg'                          , path='job_summer12_ZgTwoPhot'                  ,  isActive=False, useXSFile=True, XSName='Zg' )
    #samples.AddSample('Zg'                           , path='job_summer12_ZgOnePhot'                   ,  isActive=False, useXSFile=True )
    samples.AddSample('Zg'                           , path='job_summer12_Zg'                   ,  isActive=False, useXSFile=True )
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

    #samples.AddSampleGroup( 'Wgammagamma', legend_name='W#gamma#gamma', 
    #                        input_samples = [
    #                                         'WAA_ISR',
    #                                         'Wgg_FSR',
    #                                        ],
    #                       plotColor=ROOT.kGray+2,
    #                       isSignal=False,
    #                      )
    samples.AddSample('DYJetsToLL'                   , path='job_summer12_DYJetsToLL' ,  legend_name='Z/#gamma *'   ,  plotColor=ROOT.kCyan, useXSFile=True, isActive=False )
    samples.AddSample('DYJetsToLLNoCorr'                   , path='job_summer12_DYJetsToLLNoCorr' ,  legend_name='Z/#gamma *'   ,  plotColor=ROOT.kCyan, useXSFile=True, isActive=False )
    samples.AddSample('DYJetsToLLPhOlap'             , path='job_summer12_DYJetsToLLPhOlap'        ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False)
    samples.AddSample('DYJetsToLLPhOlapOnlyQCD'      , path='job_summer12_DYJetsToLLPhOlapOnlyQCD' ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False )
    samples.AddSample('DYJetsToLLPhOlapNew'      , path='job_summer12_DYJetsToLLPhOlapNew2' ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False )
    samples.AddSample('DYJetsToLLPhOlapFix'      , path='job_summer12_DYJetsToLLPhOlapFix3' ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False )
    samples.AddSample('DYJetsToLLPhOlapTestGen'      , path='job_summer12_DYJetsToLLPhOlapTestJustGen' ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False )
    samples.AddSample('DYJetsToLLPhOlapTestGenMother'      , path='job_summer12_DYJetsToLLPhOlapTestGenAndMother' ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False )
    samples.AddSample('DYJetsToLLPhOlapWithBits'      , path='job_summer12_DYJetsToLLPhOlapTestWithBits' ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False )
    samples.AddSample('DYJetsToLLPhOlapTestBasic'      , path='job_summer12_DYJetsToLLPhOlapTestBasic' ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False )
    samples.AddSample('DYJetsToLLPhOlapNoPion'      , path='job_summer12_DYJetsToLLPhOlapNoPion' ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False )
    samples.AddSample('DYJetsToLLPhOlapMotherCheck'      , path='job_summer12_DYJetsToLLPhOlapMotherCheck' ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False )

    samples.AddSampleGroup( 'Zgammastar', legend_name='Z/#gamma * ', 
                            input_samples = [
                                             #'DYJetsToLLPhOlapWithBits'
                                            #'DYJetsToLLPhOlapMotherCheck'
                                             'DYJetsToLLPhOlap'
    #                                        'Zg',
                                            ],
                           plotColor=ROOT.kCyan,
                           scale=1.0,
                           #scale=1.4,
                          )

    samples.AddSampleGroup( 'Zgamma', legend_name='Z#gamma', 
                           input_samples = [
                                            'Zg',
                           ],
                           plotColor=ROOT.kOrange,
                           isSignal=False,
                          )
    samples.AddSampleGroup( 'Zgammagamma', legend_name='Z#gamma#gamma', 
                           input_samples = [
                                            'Zgg',
                           ],
                           plotColor=ROOT.kOrange+2,
                          )

    samples.AddSampleGroup( 'Inclusive W', legend_name='W+jets', 
                            input_samples = [
                                             'Wjets',
                                            ],
                           plotColor=ROOT.kPink,
                          )

    samples.AddSampleGroup( 'Wgamma', legend_name='W#gamma', 
                           input_samples = [
                                            'Wg',
                                            #'WgPt20-30',
                                            #'WgPt30-50',
                                            #'WgPt50-130',
                                            #'WgPt130',
                           ],
                           plotColor=ROOT.kBlue,
                           isSignal=False,
                          )

    #samples.AddSampleGroup( 'WgammaComb', legend_name='W#gamma Comb', 
    #                       input_samples = [
    #                                        #'Wg',
    #                                        'WgPt20-30',
    #                                        'WgPt30-50',
    #                                        'WgPt50-130',
    #                                        'WgPt130',
    #                       ],
    #                       plotColor=ROOT.kBlue,
    #                       isSignal=False,
    #                      )


    samples.AddSampleGroup( 'Wgg', legend_name='W#gamma#gamma', 
                            input_samples = [
                                             'WAA_ISR',
                                             'Wgg_FSR',
                                            ],
                           plotColor=ROOT.kRed,
                           isSignal=True,
                          )

    #samples.AddSampleGroup( 'ISR', legend_name='ISR', 
    #                        input_samples = [
    #                                         'WAA_ISR',
    #                                        ],
    #                       plotColor=ROOT.kRed,
    #                       isSignal=True,
    #                      )

    #samples.AddSampleGroup( 'FSR', legend_name='FSR', 
    #                        input_samples = [
    #                                         'Wgg_FSR',
    #                                        ],
    #                       plotColor=ROOT.kRed,
    #                       isSignal=True,
    #                      )

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

    samples.AddSampleGroup( 'Topgamma', legend_name='Top + #gamma', 
                           input_samples = [
                                           'ttg',
                           ],
                           plotColor=ROOT.kGreen+4,
                          )

    samples.AddSampleGroup( 'DiPhoton', legend_name='DiPhoton', 
                           input_samples = [
                                           'diphoton_box_10to25'                     ,
                                           'diphoton_box_25to250'                     ,
                                           'diphoton_box_250toInf'                     ,
                           ],
                           plotColor=ROOT.kYellow-3,
                          )

    samples.AddSampleGroup( 'VH', legend_name='WH/ZH, m_{H} = 125 GeV', 
                           input_samples = [
                                           'WH_ZH_125'                     ,
                           ],
                           plotColor=ROOT.kRed+2,
                          )
    samples.AddSampleGroup( 'MCBkg', legend_name='MCBkg', isActive=False,
                            input_samples = [
                                             #'DYJetsToLL',
                                             'Inclusive W',
                                             'Wgamma',
                                             'DiBoson',
                                             'TriBoson',
                                             'Top',
                                             'VH',
                                        
                           ],
                           plotColor=ROOT.kGreen,
                           scale=-1,
                          )

    samples.AddSampleGroup( 'DataMCSubtracted', legend_name='Data, bkg subtracted', isActive=False,
                            input_samples = ['Data', 'MCBkg'],
                            plotColor=ROOT.kGreen,isSignal=True
                          )
                                            

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



def print_examples() :
    pass
