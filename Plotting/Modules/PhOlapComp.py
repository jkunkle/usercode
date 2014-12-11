

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
    samples.AddSample('muon_2012a_Jan22rerecoTightBlind'       , path='job_muon_2012a_Jan22rerecoTightBlind'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012b_Jan22rerecoTightBlind'       , path='job_muon_2012b_Jan22rerecoTightBlind'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012c_Jan22rerecoTightBlind'       , path='job_muon_2012c_Jan22rerecoTightBlind'        ,  isActive=False, scale=1.0 )
    samples.AddSample('muon_2012d_Jan22rerecoTightBlind'       , path='job_muon_2012d_Jan22rerecoTightBlind'        ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012a_Jan22rerecoTightBlind'   , path='job_electron_2012a_Jan22rerecoTightBlind'    ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012b_Jan22rerecoTightBlind'   , path='job_electron_2012b_Jan22rerecoTightBlind'    ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012c_Jan2012rerecoTightBlind' , path='job_electron_2012c_Jan2012rerecoTightBlind'  ,  isActive=False, scale=1.0 )
    samples.AddSample('electron_2012d_Jan22rerecoTightBlind'   , path='job_electron_2012d_Jan22rerecoTightBlind'    ,  isActive=False, scale=1.0 )
    samples.AddSample('DYJetsToLL'                   , path='job_summer12_DYJetsToLL'         ,  isActive=False, useXSFile=True )

    samples.AddSample('DYJetsToLLPhOlap'             , path='job_summer12_DYJetsToLLPhOlap'     ,  isActive=False, useXSFile=True, XSName='DYJetsToLL')
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
    samples.AddSample('Wg'                           , path='job_summer12_Wg'                  ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPhOlap'                           , path='job_summer12_WgPhOlap'          ,  isActive=False, useXSFile=True, XSName='Wg' )
    samples.AddSample('WgPt20-30'                   , path='job_summer12_WgPt20-30'          ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPt30-50'                   , path='job_summer12_WgPt30-50'          ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPt50-130'                   , path='job_summer12_WgPt50-130'          ,  isActive=False, useXSFile=True )
    samples.AddSample('WgPt130'                      , path='job_summer12_WgPt130'          ,  isActive=False, useXSFile=True )
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
    #samples.AddSample('Zgg'                          , path='job_summer12_ZgTwoPhot'                  ,  isActive=False, useXSFile=True, XSName='Zg' )
    #samples.AddSample('Zg'                           , path='job_summer12_ZgOnePhot'                   ,  isActive=False, useXSFile=True )
    samples.AddSample('Zg'                           , path='job_summer12_Zg'             ,  isActive=False, useXSFile=True, XSName='Zg' )
    #samples.AddSample('ZggFSR'                        , path='job_summer12_ZggFSR'              ,  isActive=False, useXSFile=True, XSName='Zg' )
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
    samples.AddSample('ggZZ_2l2lg'                   , path='job_summer12_ggZZ_2l2lg'           , isActive=False, useXSFile=True, XSName='ggZZ_2l2l' )
    samples.AddSample('ggZZ_4lg'                     , path='job_summer12_ggZZ_4lg'             , isActive=False, useXSFile=True, XSName='ggZZ_4l' )
    samples.AddSample('ttgg'                         , path='job_summer12_ttgg'                 , isActive=False, useXSFile=True, XSName='ttg' )
    samples.AddSample('WW_2l2nug'                    , path='job_summer12_WW_2l2nug'            , isActive=False, useXSFile=True, XSName='WW_2l2nu' )
    samples.AddSample('WWgg'                         , path='job_summer12_WWgg'                 , isActive=False, useXSFile=True, XSName='WWg' )
    samples.AddSample('WWWg'                         , path='job_summer12_WWWg'                 , isActive=False, useXSFile=True, XSName='WWW' )
    samples.AddSample('WWZg'                         , path='job_summer12_WWZg'                 , isActive=False, useXSFile=True, XSName='WWZ' )
    samples.AddSample('WZ_3lnug'                     , path='job_summer12_WZ_3lnug'             , isActive=False, useXSFile=True, XSName='WZ_3lnu' )
    samples.AddSample('WZZg'                         , path='job_summer12_WZZg'                 , isActive=False, useXSFile=True, XSName='WZZ' )
    #samples.AddSample('Zgg'                          , path='job_summer12_Zgg'                  , isActive=False, useXSFile=True, XSName='Zg' )
    samples.AddSample('ZZ_2e2mug'                    , path='job_summer12_ZZ_2e2mug'            , isActive=False, useXSFile=True, XSName='ZZ_2e2mu' )
    samples.AddSample('ZZ_2e2taug'                   , path='job_summer12_ZZ_2e2taug'           , isActive=False, useXSFile=True, XSName='ZZ_2e2tau' )
    samples.AddSample('ZZ_2l2nug'                    , path='job_summer12_ZZ_2l2nug'            , isActive=False, useXSFile=True, XSName='ZZ_2l2nu' )
    samples.AddSample('ZZ_2l2qg'                     , path='job_summer12_ZZ_2l2qg'             , isActive=False, useXSFile=True, XSName='ZZ_2l2q' )
    samples.AddSample('ZZ_2mu2taug'                  , path='job_summer12_ZZ_2mu2taug'          , isActive=False, useXSFile=True, XSName='ZZ_2mu2tau' )
    samples.AddSample('ZZ_2q2nug'                    , path='job_summer12_ZZ_2q2nug'            , isActive=False, useXSFile=True, XSName='ZZ_2q2nu' )
    samples.AddSample('ZZ_4eg'                       , path='job_summer12_ZZ_4eg'               , isActive=False, useXSFile=True, XSName='ZZ_4e' )
    samples.AddSample('ZZ_4mug'                      , path='job_summer12_ZZ_4mug'              , isActive=False, useXSFile=True, XSName='ZZ_4mu' )
    samples.AddSample('ZZ_4taug'                     , path='job_summer12_ZZ_4taug'             , isActive=False, useXSFile=True, XSName='ZZ_4tau' )
    samples.AddSample('ZZZg'                         , path='job_summer12_ZZZg'                 , isActive=False, useXSFile=True, XSName='ZZZ' )


    #samples.AddSample('MultiJet', path='job_MultiJet_2012a_Jan22rereco', isActive=True )

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             #'electron_2012a_Jan22rerecoTightBlind',
                                             #'electron_2012b_Jan22rerecoTightBlind',
                                             #'electron_2012c_Jan2012rerecoTightBlind',
                                             #'electron_2012d_Jan22rerecoTightBlind',
                                             #'muon_2012a_Jan22rerecoTightBlind',
                                             #'muon_2012b_Jan22rerecoTightBlind',
                                             #'muon_2012c_Jan22rerecoTightBlind',
                                             #'muon_2012d_Jan22rerecoTightBlind',
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


    samples.AddSampleGroup( 'Zgammastar', legend_name='Z/#gamma * ', 
                            input_samples = [
                                             'DYJetsToLLPhOlap'
                                             #'DYJetsToLL'
    #                                        #'Zg',
                                            ],
                           plotColor=ROOT.kCyan,
                           scale=1.0,
                           #scale=1.4,
                          )

    samples.AddSampleGroup( 'ZgammastarNoOlap', legend_name='No overlap removal', 
                            input_samples = [
                                             'DYJetsToLL',
                                             #'DYJetsToLL'
                                            'Zg',
                                            ],
                           plotColor=ROOT.kBlue,
                           scale=1.0,
                           isSignal=True
                           #scale=1.4,
                          )

    samples.AddSampleGroup( 'Zgamma', legend_name='Z#gamma', 
                           input_samples = [
                                            'Zg',
                           ],
                           plotColor=ROOT.kOrange-4,
                           isSignal=False,
                          )


def print_examples() :
    pass
