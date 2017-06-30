def config_samples(samples) :

    import ROOT

    samples.AddSample('ResonanceMass200_width0'  , path='MadGraphChargedResonance_WGToLNu_M200_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGreen , legend_name = 'W#gamma resonance, M = 200 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass300_width0'  , path='MadGraphChargedResonance_WGToLNu_M300_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kCyan  , legend_name = 'W#gamma resonance, M = 300 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass400_width0'  , path='MadGraphChargedResonance_WGToLNu_M400_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kViolet, legend_name = 'W#gamma resonance, M = 400 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass500_width0'  , path='MadGraphChargedResonance_WGToLNu_M500_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kOrange, legend_name = 'W#gamma resonance, M = 500 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass600_width0'  , path='MadGraphChargedResonance_WGToLNu_M600_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 600 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass700_width0'  , path='MadGraphChargedResonance_WGToLNu_M700_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 700 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass800_width0'  , path='MadGraphChargedResonance_WGToLNu_M800_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 800 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass1000_width0'  , path='MadGraphChargedResonance_WGToLNu_M1000_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 1000 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass1200_width0'  , path='MadGraphChargedResonance_WGToLNu_M1200_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 1200 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass2000_width0'  , path='MadGraphChargedResonance_WGToLNu_M2000_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 2000 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass3000_width0'  , path='MadGraphChargedResonance_WGToLNu_M3000_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 3000 GeV, width = 0.01%' )
    samples.AddSample('ResonanceMass4000_width0'  , path='MadGraphChargedResonance_WGToLNu_M4000_width0p01' , isActive=True,isSignal=True, useXSFile=True, plotColor=ROOT.kGray  , legend_name = 'W#gamma resonance, M = 4000 GeV, width = 0.01%' )

    samples.AddSampleGroup(  'Comb', legend_name='Comb',
                           input_samples = [
                                            'ResonanceMass200',
                                            'ResonanceMass300',
                                            'ResonanceMass400',
                                            'ResonanceMass500',
                                            'ResonanceMass600',
                                            'ResonanceMass700',
                                            'ResonanceMass800',
                                            'ResonanceMass1000',
                                            'ResonanceMass1200',
                                            'ResonanceMass2000',
                                            'ResonanceMass3000',
                                            'ResonanceMass4000',
                           ],
                           plotColor = ROOT.kBlue-2,
                          )


