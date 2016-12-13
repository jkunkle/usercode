def config_samples(samples) :

    import ROOT
    samples.AddSample('Wg'                       , path='WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'    ,  isActive=False, useXSFile=True, plotColor=ROOT.kRed-2 )
    samples.AddSample('WgPt500'                       , path='WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'    ,  isActive=False, useXSFile=True, plotColor=ROOT.kRed )
    samples.AddSample('_Wjets'                    , path='WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'  ,  isActive=False, useXSFile=True, XSName='Wjets', plotColor=ROOT.kBlue-2)
    samples.AddSample('ResonanceMass400Width1'  , path='ChargedResonance_WGToLNu_M400_width1'            , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGreen, legend_name = 'W#gamma resonance, M = 400 GeV, width = 1%' )
    #samples.AddSample('ResonanceMass400Width1'   , path='ChargedResonance_WGToLNu_M400_width1'            , isActive=True,isSignal=True, plotColor=ROOT.kGreen )
    #samples.AddSample('ResonanceMass2000Width0p01'  , path='ChargedResonance_WGToLNu_M2000_width0p01'            , isActive=True,isSignal=True, plotColor=ROOT.kCyan )
    #samples.AddSample('ResonanceMass2000Width5'   , path='ChargedResonance_WGToLNu_M2000_width5'            , isActive=True,isSignal=True, plotColor=ROOT.kGray )
    samples.AddSample('ResonanceMass2000Width10'   , path='ChargedResonance_WGToLNu_M2000_width10'            , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kViolet, legend_name = 'W#gamma resonance, M = 2000 GeV, width = 10%' )
    #samples.AddSample('ResonanceMass2000Width20'   , path='ChargedResonance_WGToLNu_M2000_width20'            , isActive=True,isSignal=True, plotColor=ROOT.kOrange )

    samples.AddSampleGroup(  'Wgamma', legend_name='W#gamma',
                           input_samples = ['Wg', 'WgPt500'],
                           plotColor = ROOT.kRed-2,
                          )

    samples.AddSampleGroup(  'Wjets', legend_name='W+Jets',
                           input_samples = ['_Wjets'],
                           plotColor = ROOT.kBlue-2,
                          )


    samples.AddSampleGroup( 'MCBackground', legend_name='MC Background',
                           input_samples = ['Wgamma', 'Wjets'],
                           isActive=False,
                          )

def print_examples() :
    pass

