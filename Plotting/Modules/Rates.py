def config_samples(samples) :

    import ROOT

    samples.AddSample('HLTPhysics0'                       , path='HLTPhysics0/HLTRates80X_v1'    ,  isActive=False)
    samples.AddSample('HLTPhysics1'                       , path='HLTPhysics1/HLTRates80X_v1'    ,  isActive=False)
    samples.AddSample('HLTPhysics2'                       , path='HLTPhysics2/HLTRates80X_v1'    ,  isActive=False)
    samples.AddSample('HLTPhysics3'                       , path='HLTPhysics3/HLTRates80X_v1'    ,  isActive=False)

    samples.AddSample('QCD_Pt-120to170_EMEnriched', path='QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2', isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt-15to20_EMEnriched'  , path='QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2'  , isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt-20to30_EMEnriched'  , path='QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2'  , isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt-30to50_EMEnriched'  , path='QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2'  , isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt-50to80_EMEnriched'  , path='QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2'  , isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt-80to120_EMEnriched' , path='QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2' , isActive=False, useXSFile=True )

    samples.AddSample('QCD_Pt_15to30', path='QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2', isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt_30to50', path='QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2', isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt_50to80', path='QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2', isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt_80to120', path='QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2', isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt_120to170', path='QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2', isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt_170to300', path='QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2', isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt_300to470', path='QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2', isActive=False, useXSFile=True )
    samples.AddSample('QCD_Pt_470to600', path='QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/HLTRates92X_v2', isActive=False, useXSFile=True )


    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             'HLTPhysics0',
                                             'HLTPhysics1',
                                             'HLTPhysics2',
                                             'HLTPhysics3',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )

def print_examples() :
    pass

