

def config_samples(samples) :

    import ROOT
    samples.AddSample('Data'          , path='Data'          ,legend_name='Data'                       ,isActive=True, plotColor=ROOT.kBlack, isData=True )
    samples.AddSample('Wgg'           , path='Wgg'           ,legend_name='W#gamma#gamma Signal'       ,isActive=True, plotColor=ROOT.kRed-3, scale=1.0, isSignal=False )
    samples.AddSample('Zgg'           , path='Zgg'           ,legend_name='Z#gamma#gamma'              ,isActive=True, plotColor=ROOT.kOrange-2, displayErrBand=True)
    samples.AddSample('OtherDiPhoton' , path='OtherDiPhoton' ,legend_name='Other di-photon'            ,isActive=True, plotColor=ROOT.kGray, displayErrBand=True )
    samples.AddSample('Top'           , path='Top'           ,legend_name='Top'                        ,isActive=True, plotColor=ROOT.kGreen, displayErrBand=True )
    samples.AddSample('MultiBoson'    , path='MultiBoson'    ,legend_name='Multi Boson'                ,isActive=True, plotColor=ROOT.kBlue, displayErrBand=True )
    samples.AddSample('EleFake'       , path='EleFake'       ,legend_name='e#rightarrow#gamma fakes'   ,isActive=True, plotColor=ROOT.kGreen+1, displayErrBand=True )
    samples.AddSample('JetFake'       , path='JetFake'       ,legend_name='jet#rightarrow#gamma fakes' ,isActive=True, plotColor=ROOT.kBlue-7, displayErrBand=True)
    samples.AddSample('WAAQGCLT'      , path='WggAQGCLT50'   ,legend_name='W#gamma#gamma, LT0=50'      ,isActive=False, plotColor=ROOT.kBlue, required=False, useXSFile=True, isSignal=True )
    #samples.AddSample('MCBkg'        , path='MCBkg'         ,legend_name='MC background',   isActive=True, isSignal=True, plotColor=ROOT.kGray+2 )

    samples.AddSample('ZggNoSyst'     , path='ZggNoSyst'     ,legend_name='Z#gamma#gamma'              ,isActive=True, plotColor=ROOT.kOrange-2, displayErrBand=True)
    samples.AddSampleGroup('AllBkg' , legend_name = 'AllBkg' ,input_samples = ['Zgg', 'OtherDiPhoton', 'EleFake', 'JetFake'],   isActive=True, plotColor=ROOT.kBlue-7, displayErrBand=False)
    samples.AddSampleGroup('AllBkgPlusSig' , legend_name = 'AllBkg' ,input_samples = ['Zgg', 'OtherDiPhoton', 'EleFake', 'JetFake', 'Wgg'],   isActive=False, plotColor=ROOT.kBlue-7, displayErrBand=False)
    samples.AddSampleGroup('AllBkgPlusQGC' , legend_name = 'Expected, LT0 = 50 TeV^{-4}' ,input_samples = ['Zgg', 'OtherDiPhoton', 'EleFake', 'JetFake', 'WAAQGCLT'], isActive=False, isSignal=True, plotColor=ROOT.kBlue-7)


def print_examples() :
    pass
