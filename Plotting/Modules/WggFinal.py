

def config_samples(samples) :

    import ROOT
    samples.AddSample('Data'          , path='Data'          ,legend_name='Data'                       ,isActive=True, plotColor=ROOT.kBlack, isData=True )
    samples.AddSample('Wgg'           , path='Wgg'           ,legend_name='W#gamma#gamma'       ,isActive=True, plotColor=ROOT.kRed-3, scale=1.0, isSignal=False )
    #samples.AddSample('Zgg'           , path='Zgg'           ,legend_name='Z#gamma#gamma'              ,isActive=True, plotColor=ROOT.kOrange-2, displayErrBand=True)
    samples.AddSample('ZggPlusOtherDiPhoton' , path='ZggPlusOtherDiPhoton' ,legend_name='Prompt diphoton'            ,isActive=True, plotColor=ROOT.kOrange-2, displayErrBand=True )
    #samples.AddSample('OtherDiPhoton' , path='OtherDiPhoton' ,legend_name='Prompt diphoton'            ,isActive=True, plotColor=ROOT.kGray, displayErrBand=True )
    samples.AddSample('Top'           , path='Top'           ,legend_name='Top'                        ,isActive=True, plotColor=ROOT.kGreen, displayErrBand=True )
    samples.AddSample('MultiBoson'    , path='MultiBoson'    ,legend_name='Multi Boson'                ,isActive=True, plotColor=ROOT.kBlue, displayErrBand=True )
    #samples.AddSample('EleFake'       , path='EleFake'       ,legend_name='e#rightarrow#gamma fakes'   ,isActive=True, plotColor=ROOT.kGreen+1, displayErrBand=True )
    #samples.AddSample('JetFake'       , path='JetFake'       ,legend_name='jet#rightarrow#gamma fakes' ,isActive=True, plotColor=ROOT.kBlue-7, displayErrBand=True)
    samples.AddSample('EleFake'       , path='EleFake'       ,legend_name='Misidentified electrons'   ,isActive=True, plotColor=ROOT.kGreen+1, displayErrBand=True )
    samples.AddSample('JetFake'       , path='JetFake'       ,legend_name='Misidentified jets' ,isActive=True, plotColor=ROOT.kBlue-7, displayErrBand=True)
    samples.AddSample('WAAQGCLT'      , path='WggAQGCLT50'   ,legend_name='W#gamma#gamma, #frac{L_{t0}}{#Lambda^{4}} = 50 TeV^{-4}'      ,isActive=False, plotColor=ROOT.kMagenta+2, required=False, useXSFile=True, isSignal=True )
    #samples.AddSample('MCBkg'        , path='MCBkg'         ,legend_name='MC background',   isActive=True, isSignal=True, plotColor=ROOT.kGray+2 )

    samples.AddSample('ZggNoSyst'     , path='ZggNoSyst'     ,legend_name='Z#gamma#gamma'              ,isActive=False, plotColor=ROOT.kOrange-2, displayErrBand=False)
    samples.AddSample('OtherDiPhotonNoSyst'     , path='OtherDiPhotonNoSyst'        ,isActive=False, plotColor=ROOT.kOrange-2, displayErrBand=False)
    samples.AddSample('DiTopDiPhoton', path='DiTopDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSample('SingleTopDiPhoton', path='SingleTopDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSample('TriBosonDiPhoton', path='TriBosonDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSample('TTVDiPhoton', path='TTVDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSample('WWDiPhoton', path='WWDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSample('WZlvjjDiPhoton', path='WZlvjjDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSample('WZlvllDiPhoton', path='WZlvllDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSample('WZjjllDiPhoton', path='WZjjllDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSample('WZlvvvDiPhoton', path='WZlvvvDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSample('ZZDiPhoton', path='ZZDiPhoton', isActive=False, displayErrBand=False)
    samples.AddSampleGroup('AllBkg' , legend_name = 'AllBkg' ,input_samples = ['Zgg', 'OtherDiPhoton', 'EleFake', 'JetFake'],   isActive=False, plotColor=ROOT.kBlue-7, displayErrBand=False)
    samples.AddSampleGroup('AllBkgPlusSig' , legend_name = 'AllBkg' ,input_samples = ['Zgg', 'OtherDiPhoton', 'EleFake', 'JetFake', 'Wgg'],   isActive=False, plotColor=ROOT.kBlue-7, displayErrBand=False)
    #samples.AddSampleGroup('AllBkgPlusQGC' , legend_name = 'Expected, #frac{f_{T0}}{#Lambda^{4}} = 50 TeV^{-4}' ,input_samples = ['Zgg', 'OtherDiPhoton', 'EleFake', 'JetFake', 'WAAQGCLT'], isActive=False, isSignal=True, plotColor=ROOT.kMagenta+2)
    samples.AddSampleGroup('AllBkgPlusQGC' , legend_name = 'Expected, #frac{f_{T0}}{#Lambda^{4}} = 50 TeV^{-4}' ,input_samples = ['ZggPlusOtherDiPhoton', 'EleFake', 'JetFake', 'WAAQGCLT'], isActive=False, isSignal=True, plotColor=ROOT.kMagenta+2)


def print_examples() :
    pass
