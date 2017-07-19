import ROOT
from SampleManager import SampleManager

ROOT.gROOT.SetBatch(False)

baseDir  = 'root://eoscms//eos/cms/store/user/jkunkle/Wgamgam/RecoOutput_2015_04_05'

treename = 'ggNtuplizer/EventTree'
filename = 'tree.root'
sampleConf= '/afs/cern.ch/user/j/jkunkle/usercode/Plotting/Modules/LepLep.py'

samples = SampleManager( baseDir, treename, filename=filename, xsFile='/afs/cern.ch/user/j/jkunkle/usercode/Plotting/cross_sections/wgamgam.py', lumi=19400. )

samples.ReadSamples( sampleConf )

samples.start_command_collection()

samples.Draw( 'el_pfiso40[0]/el_pt[0]', 'el_n==1 && el_triggerMatch[0] && el_pt[0] > 30', (100, 0, 5) )
samples.SaveStack( 'el_relpfiso', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )

samples.Draw( 'el_pfiso40[0]/el_pt[0]', 'el_n==1 && el_triggerMatch[0] && el_pt[0] > 30', [0, 1.5, 5] )
samples.SaveStack( 'el_relpfiso__varBins', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )
samples.DumpStack( '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' ,'el_relpfiso__varBins' )

samples.Draw( 'mu_corrIso[0]/mu_pt[0]', 'mu_n==1 && mu_triggerMatch[0] && mu_passTightNoIso[0] && mu_pt[0] > 25', (100, 0, 5) )
samples.SaveStack( 'mu_relpfiso', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )

samples.Draw( 'mu_corrIso[0]/mu_pt[0]', 'mu_n==1 && mu_triggerMatch[0] && mu_passTightNoIso[0] && mu_pt[0] > 25', [0, 2, 5] )
samples.SaveStack( 'mu_relpfiso__varBins', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )
samples.DumpStack( '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' ,'mu_relpfiso__varBins' )

samples.Draw( 'pfMET', 'mu_n==1 && mu_triggerMatch[0] && mu_pt[0] > 25 && mu_passTightNoIso[0] ', (100, 0, 500) )
samples.SaveStack( 'pfMET_mu', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )

samples.Draw( 'pfMET', 'el_n==1 && el_triggerMatch[0] && el_pt[0] > 30', (100, 0, 500) )
samples.SaveStack( 'pfMET_el', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )

samples.Draw( 'el_pfiso40[0]/el_pt[0]', 'el_n==1 && el_triggerMatch[0] && el_pt[0] > 30 && pfMET < 40', (100, 0, 5) )
samples.SaveStack( 'el_relpfiso_MetCut', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )

samples.Draw( 'el_pfiso40[0]/el_pt[0]', 'el_n==1 && el_triggerMatch[0] && el_pt[0] > 30 && pfMET < 40', [0, 1.5, 5])
samples.SaveStack( 'el_relpfiso_MetCut__varBins', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )
samples.DumpStack( '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' ,'el_relpfiso_MetCut__varBins' )

samples.Draw( 'mu_corrIso[0]/mu_pt[0]', 'mu_n==1 && mu_triggerMatch[0] && mu_passTightNoIso[0]  && mu_pt[0] > 25 && pfMET < 40', (100, 0, 5) )
samples.SaveStack( 'mu_relpfiso_MetCut', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )

samples.Draw( 'mu_corrIso[0]/mu_pt[0]', 'mu_n==1 && mu_triggerMatch[0] && mu_passTightNoIso[0]  && mu_pt[0] > 25 && pfMET < 40', [0, 2, 5] )
samples.SaveStack( 'mu_relpfiso_MetCut__varBins', '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' )
samples.DumpStack( '/afs/cern.ch/work/j/jkunkle/private/CMS/Plots/TEST' ,'mu_relpfiso_MetCut__varBins' )

samples.run_commands()
