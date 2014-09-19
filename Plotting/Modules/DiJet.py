

def config_samples(samples) :

    import ROOT
    samples.AddSample('muon_2012a_Jan22rereco'       , path='job_muon_2012a_Jan22rerecoTightBlind'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012b_Jan22rereco'       , path='job_muon_2012b_Jan22rerecoTightBlind'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012c_Jan22rereco'       , path='job_muon_2012c_Jan22rerecoTightBlind'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012d_Jan22rereco'       , path='job_muon_2012d_Jan22rerecoTightBlind'        ,  isActive=False, scale=1.0 )
    samples.AddSample('ttjets_1l'                    , path='job_summer12_ttjets_1lPhOlap'            ,  isActive=False, useXSFile=True )
    samples.AddSample('ttjets_2l'                    , path='job_summer12_ttjets_2lPhOlap'            ,  isActive=False, useXSFile=True )
    samples.AddSample('Wg'                           , path='job_summer12_Wg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('Wjets'                        , path='job_summer12_Wjets'               ,  isActive=False, useXSFile=True )
    samples.AddSample('WjetsPhOlap'                        , path='job_summer12_WjetsPhOlap'       ,  isActive=False, useXSFile=True, XSName='Wjets' )
    samples.AddSample('WW_2l2nu'                     , path='job_summer12_WW_2l2nu'             ,  isActive=False, useXSFile=True )
    samples.AddSample('WWg'                          , path='job_summer12_WWg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WWW'                          , path='job_summer12_WWW'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WWZ'                          , path='job_summer12_WWZ'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WZ_3lnu'                      , path='job_summer12_WZ_3lnu'              ,  isActive=False, useXSFile=True )
    samples.AddSample('WZZ'                          , path='job_summer12_WZZ'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('Zg'                           , path='job_summer12_Zg'                   ,  isActive=False, useXSFile=True )
    samples.AddSample('diphoton_box_10to25'          , path='job_summer12_diphoton_box_10to25'  ,  isActive=False, useXSFile=True )
    samples.AddSample('diphoton_box_250toInf'        , path='job_summer12_diphoton_box_250toInf',  isActive=False, useXSFile=True )
    samples.AddSample('diphoton_box_25to250'         , path='job_summer12_diphoton_box_25to250' ,  isActive=False, useXSFile=True )

    samples.AddSample( 'jetmon', path='job_jetmon_2012c_Jan22rereco', isActive=True )

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

    
    samples.AddSampleGroup( 'DiPhoton', legend_name='DiPhoton', 
                           input_samples = [
                                           'diphoton_box_10to25'                     ,
                                           'diphoton_box_25to250'                     ,
                                           'diphoton_box_250toInf'                     ,
                           ],
                           plotColor=ROOT.kYellow-3,
                          )

    #samples.AddSampleGroup( 'Wgammagamma', legend_name='W#gamma#gamma', 
    #                        input_samples = [
    #                                         'WAA_ISR',
    #                                         'Wgg_FSR',
    #                                        ],
    #                       plotColor=ROOT.kGray+2,
    #                       isSignal=False,
    #                      )
    samples.AddSample('DYJetsToLL'                   , path='job_summer12_DYJetsToLL' ,  legend_name='Z/#gamma *'   ,  plotColor=ROOT.kCyan, useXSFile=True, isActive=False )
    samples.AddSample('DYJetsToLLPhOlap'             , path='job_summer12_DYJetsToLLPhOlap'        ,  legend_name='Z/#gamma *', plotColor=ROOT.kCyan, useXSFile=True, XSName='DYJetsToLL', isActive=False)

    samples.AddSampleGroup( 'RealPhotonsZg', legend_name='Fake photons', 
                        input_samples = [
                            'Zg',
                        ],
                           plotColor=ROOT.kYellow,
                           scale=-1,
                          )

    samples.AddSampleGroup( 'RealPhotonsWg', legend_name='Fake photons', 
                        input_samples = [
                            'Wg',
                        ],
                           plotColor=ROOT.kYellow,
                           scale=-1,
                          )

    samples.AddSampleGroup( 'DataRealPhotonZgSub', legend_name='Fake photons', 
                        input_samples = [
                            'Data',
                            'RealPhotonsZg',
                        ],
                           plotColor=ROOT.kYellow,
                          )

    samples.AddSampleGroup( 'DataRealPhotonWgSub', legend_name='Fake photons', 
                        input_samples = [
                            'Data',
                            'RealPhotonsWg',
                            'RealPhotonsZg',
                        ],
                           plotColor=ROOT.kYellow,
                          )

    samples.AddSampleGroup( 'WjetsWgamma', legend_name = 'W+jets + W#gamma',
                           input_samples=[
                           'Wg', 
                           'WjetsPhOlap',
                           ],
                           plotColor=ROOT.kGray,
                          )


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
                           plotColor=ROOT.kBlue-10,
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
    
    samples.AddSampleGroup( 'WjetsZjets', legend_name = 'W+jets + Z+jets',
                           input_samples=[
                           'DYJetsToLLPhOlap', 
                           'WjetsPhOlap',
                           ],
                           plotColor=ROOT.kSpring,
                           isActive=False,
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
