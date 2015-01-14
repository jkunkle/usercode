

def config_samples(samples) :

    import ROOT
    samples.AddSample('Data'    , path='Data'    ,legend_name='Data',   isActive=True, plotColor=ROOT.kBlack, isData=True )
    samples.AddSample('Wgg'     , path='Wgg'     ,legend_name='W#gamma#gamma Signal',   isActive=True, plotColor=ROOT.kRed-3 )
    samples.AddSample('ZggFSR'     , path='ZggFSR'     ,legend_name='Z#gamma#gamma FSR',   isActive=True, plotColor=ROOT.kOrange-2, displayErrBand=True )
    #samples.AddSample('Zg'     , path='Zg'     ,legend_name='Z#gamma',   isActive=True, plotColor=ROOT.kOrange+2, displayErrBand=True )
    samples.AddSample('Top'     , path='Top'     ,legend_name='Top',   isActive=True, plotColor=ROOT.kGreen, displayErrBand=True )
    samples.AddSample('MultiBoson'     , path='MultiBoson'     ,legend_name='Multi Boson',   isActive=True, plotColor=ROOT.kBlue, displayErrBand=True )
    samples.AddSample('EleFake' , path='EleFake' ,legend_name='Electron fake estimate',   isActive=True, plotColor=ROOT.kGreen+1 )
    samples.AddSample('JetFake' , path='JetFake' ,legend_name='Jet fake estimate',   isActive=True, plotColor=ROOT.kBlue-7, displayErrBand=True )
    #samples.AddSample('MCBkg'   , path='MCBkg'   ,legend_name='MC background',   isActive=True, isSignal=True, plotColor=ROOT.kGray+2 )

def print_examples() :
    pass
