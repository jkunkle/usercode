

def config_samples(samples) :

    import ROOT
    samples.AddSample('Data'    , path='Data'    ,legend_name='Data',   isActive=True, plotColor=ROOT.kBlack, isData=True )
    samples.AddSample('Zgg'     , path='Zgg'     ,legend_name='Z#gamma#gamma',   isActive=True, plotColor=ROOT.kOrange-2, displayErrBand=True )
    #samples.AddSample('Zg'     , path='Zg'     ,legend_name='Z#gamma',   isActive=True, plotColor=ROOT.kOrange+2, displayErrBand=True )
    samples.AddSample('EleFake' , path='EleFake' ,legend_name='e#rightarrow#gamma fakes',   isActive=True, plotColor=ROOT.kGreen+1 )
    samples.AddSample('JetFake' , path='JetFake' ,legend_name='jet#rightarrow#gamma fakes',   isActive=True, plotColor=ROOT.kBlue-7, displayErrBand=True)
    #samples.AddSample('MCBkg'   , path='MCBkg'   ,legend_name='MC background',   isActive=True, isSignal=True, plotColor=ROOT.kGray+2 )

    samples.AddSampleGroup('AllBkg' , legend_name = 'All Bkg' ,input_samples = ['Zgg', 'OtherDiPhoton', 'EleFake', 'JetFake'],   isActive=False, plotColor=ROOT.kBlue-7, displayErrBand=False)


def print_examples() :
    pass
