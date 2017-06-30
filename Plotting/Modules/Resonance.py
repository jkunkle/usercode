def config_samples(samples) :

    import ROOT

    samples.AddSample('SingleMuon'                       , path='SingleMuon'    ,  isActive=False)
    samples.AddSample('SingleElectron'                       , path='SingleElectron'    ,  isActive=False)

    samples.AddSample('DYJetsToLL_M-50'               , path='DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'          , isActive=False, useXSFile=True )
    samples.AddSample('TTJets_DiLept'                 , path='TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'            , isActive=False, useXSFile=True )
    samples.AddSample('TTJets_SingleLeptFromTbar'     , path='TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', isActive=False, useXSFile=True )
    samples.AddSample('TTJets_SingleLeptFromT'        , path='TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , isActive=False, useXSFile=True )
    samples.AddSample('WGToLNuG_PtG-130-amcatnloFXFX' , path='WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        , isActive=False, useXSFile=True )
    samples.AddSample('WGToLNuG-amcatnloFXFX'         , path='WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                , isActive=False, useXSFile=True )
    samples.AddSample('WJetsToLNu'                    , path='WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'               , isActive=False, useXSFile=True )
    samples.AddSample('WWG'                           , path='WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                         , isActive=False, useXSFile=True )

    samples.AddSample('ResonanceMass200'  , path='MadGraphChargedResonance_WGToLNu_M200_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGreen , legend_name = 'W#gamma resonance, M = 200 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass300'  , path='MadGraphChargedResonance_WGToLNu_M300_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kCyan  , legend_name = 'W#gamma resonance, M = 300 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass400'  , path='MadGraphChargedResonance_WGToLNu_M400_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kViolet, legend_name = 'W#gamma resonance, M = 400 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass500'  , path='MadGraphChargedResonance_WGToLNu_M500_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kOrange, legend_name = 'W#gamma resonance, M = 500 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass600'  , path='MadGraphChargedResonance_WGToLNu_M600_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 600 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass700'  , path='MadGraphChargedResonance_WGToLNu_M700_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 700 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass800'  , path='MadGraphChargedResonance_WGToLNu_M800_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 800 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass1000'  , path='MadGraphChargedResonance_WGToLNu_M1000_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 1000 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass1200'  , path='MadGraphChargedResonance_WGToLNu_M1200_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 1200 GeV, width = 0.01%' )

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             'SingleMuon',
                                             'SingleElectron',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )

    samples.AddSampleGroup(  'Wjets', legend_name='W+Jets',
                           input_samples = ['WJetsToLNu'],
                           plotColor = ROOT.kBlue-2,
                          )

    samples.AddSampleGroup(  'Z+jets', legend_name='Z+Jets',
                           input_samples = ['DYJetsToLL_M-50'],
                           plotColor = ROOT.kCyan-2,
                          )

    samples.AddSampleGroup(  'Wgamma', legend_name='W#gamma',
                           input_samples = ['WGToLNuG-amcatnloFXFX'],
                           plotColor = ROOT.kRed-2,
                          )

    samples.AddSampleGroup( 'TTbar_DiLep', legend_name='t#bar{t} dileptonic',
                           input_samples = ['TTJets_DiLept'],
                           plotColor = ROOT.kMagenta+2,
                          )

    samples.AddSampleGroup( 'TTbar_SingleLep', legend_name='t#bar{t} semileptonic',
                           input_samples = ['TTJets_SingleLeptFromTbar', 'TTJets_SingleLeptFromT'],
                           plotColor = ROOT.kGreen+2,
                          )

    samples.AddSampleGroup( 'WWgamma', legend_name='WW#gamma',
                           input_samples = ['WWG'],
                           plotColor = ROOT.kOrange,
                          )

    samples.AddSampleGroup( 'MCBackground', legend_name='MC Background',
                           input_samples = ['Wgamma', 'Wjets'],
                           isActive=False,
                          )

def print_examples() :
    pass

