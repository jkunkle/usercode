

def config_samples(samples) :

    import ROOT
    samples.AddSample('_WWLONom'     , path='WWLONomFilt'        ,  isActive=True, useXSFile=True, plotColor=ROOT.kBlack, isSignal=True, XSName='WWLONom' )
    samples.AddSample('WWLONomM500'   , path='WWLONomM500'        ,  isActive=True, useXSFile=True, plotColor=ROOT.kGray, isSignal=True )
    samples.AddSample('WWLO_CWWW_2'   , path='WWLO_CWWW_2'    ,  isActive=False, useXSFile=True )
    samples.AddSample('WWLO_CWWW_5'   , path='WWLO_CWWW_5'    ,  isActive=False, useXSFile=True )
    samples.AddSample('WWLO_CWWW_10'  , path='WWLO_CWWW_10'   ,  isActive=False, useXSFile=True )
    samples.AddSample('WWLO_CWWW_20'  , path='WWLO_CWWW_20'   ,  isActive=False, useXSFile=True )
    samples.AddSample('WWLO_CWWW_50'  , path='WWLO_CWWW_50'   ,  isActive=False, useXSFile=True )

    samples.AddSampleGroup( 'WWLONom', legend_name = 'WW (SM)',
                           input_samples = ['_WWLONom', 'WWLONomM500'],
                           plotColor=ROOT.kBlack,
                           isSignal=True,
                          )

    samples.AddSampleGroup( 'WW_CWWW_2', legend_name = 'C_{WWW} = 2 TeV^{-2}',
                           input_samples = ['WWLONom', 'WWLO_CWWW_2'],
                           #input_samples = ['WWLO_CWWW_2'],
                           plotColor=ROOT.kRed,
                           isSignal=True,
                          )

    samples.AddSampleGroup( 'WW_CWWW_5', legend_name = 'C_{WWW} = 5 TeV^{-2}',
                           input_samples = ['WWLONom', 'WWLO_CWWW_5'],
                           #input_samples = ['WWLO_CWWW_5'],
                           plotColor=ROOT.kBlue,
                           isSignal=True,
                          )

    samples.AddSampleGroup( 'WW_CWWW_10', legend_name = 'C_{WWW} = 10 TeV^{-2}',
                           input_samples = ['WWLONom', 'WWLO_CWWW_10'],
                           #input_samples = ['WWLO_CWWW_10'],
                           plotColor=ROOT.kGreen,
                           isSignal=True,
                          )

    samples.AddSampleGroup( 'WW_CWWW_20', legend_name = 'C_{WWW} = 20 TeV^{-2}',
                           input_samples = ['WWLONom', 'WWLO_CWWW_20'],
                           #input_samples = [ 'WWLO_CWWW_20'],
                           plotColor=ROOT.kMagenta,
                           isSignal=True,
                          )

    samples.AddSampleGroup( 'WW_CWWW_50', legend_name = 'C_{WWW} = 50 TeV^{-2}',
                           input_samples = ['WWLONom', 'WWLO_CWWW_50'],
                           #input_samples = [ 'WWLO_CWWW_50'],
                           plotColor=ROOT.kOrange,
                           isSignal=True,
                          )



def print_examples() :
    pass
