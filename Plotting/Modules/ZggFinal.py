

def config_samples(samples) :

    import ROOT
    samples.AddSample('Data'    , path='Data'    ,legend_name='Data',   isActive=True, plotColor=ROOT.kBlack, isData=True )
    samples.AddSample('Zgg'     , path='Zgg'     ,legend_name='Z#gamma#gamma',   isActive=True, plotColor=ROOT.kOrange-2, displayErrBand=True )
    #samples.AddSample('OtherDiPhoton' , path='OtherDiPhoton' ,legend_name='Prompt diphoton'            ,isActive=True, plotColor=ROOT.kGray, displayErrBand=True )
    #samples.AddSample('Zg'     , path='Zg'     ,legend_name='Z#gamma',   isActive=True, plotColor=ROOT.kOrange+2, displayErrBand=True )
    samples.AddSample('EleFake' , path='EleFake' ,legend_name='Misidentified electrons',   isActive=True, plotColor=ROOT.kGreen+1 )
    samples.AddSample('JetFake' , path='JetFake' ,legend_name='Misidentified jets',   isActive=True, plotColor=ROOT.kBlue-7, displayErrBand=True)
    #samples.AddSample('MCBkg'   , path='MCBkg'   ,legend_name='MC background',   isActive=True, isSignal=True, plotColor=ROOT.kGray+2 )

    samples.AddSample('OtherDiPhotonNoSyst'     , path='OtherDiPhotonNoSyst'        ,isActive=False, plotColor=ROOT.kOrange-2, displayErrBand=False)
    samples.AddSample('SingleTopDiPhoton' , path='SingleTopDiPhoton', isActive=True, displayErrBand=False)
    samples.AddSample('TriBosonDiPhoton'  , path='TriBosonDiPhoton' , isActive=True, displayErrBand=False)
    samples.AddSample('TTVDiPhoton'       , path='TTVDiPhoton'      , isActive=True, displayErrBand=False)
    samples.AddSample('WWDiPhoton'        , path='WWDiPhoton'       , isActive=True, displayErrBand=False)
    samples.AddSample('WZlvjjDiPhoton'    , path='WZlvjjDiPhoton'   , isActive=True, displayErrBand=False)
    samples.AddSample('WZlvllDiPhoton'    , path='WZlvllDiPhoton'   , isActive=True, displayErrBand=False)
    samples.AddSample('WZjjllDiPhoton'    , path='WZjjllDiPhoton'   , isActive=True, displayErrBand=False)
    samples.AddSample('WZlvvvDiPhoton'    , path='WZlvvvDiPhoton'   , isActive=True, displayErrBand=False)
    samples.AddSample('ZZDiPhoton'        , path='ZZDiPhoton'       , isActive=True, displayErrBand=False)
    samples.AddSample('DiTopDiPhoton'     , path='DiTopDiPhoton'    , isActive=True, displayErrBand=False)

    samples.AddSampleGroup('AllBkg' , legend_name = 'All Bkg' ,input_samples = ['Zgg', 'OtherDiPhoton', 'EleFake', 'JetFake'],   isActive=False, plotColor=ROOT.kBlue-7, displayErrBand=False)
    samples.AddSampleGroup('AllBkgPlusSig' , legend_name = 'AllBkgPlusSig' ,input_samples = ['Zgg', 'OtherDiPhoton', 'JetFake'],   isActive=False, plotColor=ROOT.kBlue-7, displayErrBand=False)


def print_examples() :
    pass
