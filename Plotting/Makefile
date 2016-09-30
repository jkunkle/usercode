#CHANNELS=mu elzcr elfull elzcrinvpixsubl elzcrinvpixlead elfullinvpixsubl elfullinvpixlead
#CHANNELS=mu elfull elfullinvpixlead elfullinvpixsubl
#CHANNELS=elzcr elfull elzcrinvpixsubl elzcrinvpixlead elfullinvpixsubl elfullinvpixlead
CHANNELS=mu
#CHANNELS=muZgg
#CHANNELS=elfull 
#CHANNELS=elzcr
#CHANNELS=elfullinvpixlead
#CHANNELS=elfullinvpixsubl
#CHANNELS=elzcrinvpixlead
#CHANNELS=elzcrinvpixsubl
#CHANNELS=elzcr elfull
#CHANNELS=elph1zcr elph2zcr
#CHANNELS=elzcrinvpixsubl elzcrinvpixlead 
#CHANNELS=elfullinvpixlead elfullinvpixsubl
#CHANNELS=elph1zcrinvpixsubl elph1zcrinvpixlead 
#CHANNELS=elph2zcrinvpixsubl elph2zcrinvpixlead 
#CHANNELS=elph2zcrinvpixlead elph1zcrinvpixlead 
#CHANNELS=elzcrinvpixsubl elzcrinvpixlead elfullinvpixsubl elfullinvpixlead
#CHANNELS=mu elzcr elfull elzcrinvpixsubl
#CHANNELS=elzcrinvpixlead elzcrinvpixsubl elfullinvpixsubl elfullinvpixlead

#OUTPUTMAIN=~/Plots/ZggPlots_2015_12_01
#OUTPUTMAIN=~/Plots/ZggPlotsOneBin_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsSublPt20_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsSublPt30_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsSublPt35_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsSublPt40_2015_12_01
OUTPUTMAIN=~/Plots/WggPlotsPSVTightMass_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsPSVTightMassSublPtCR_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsPSVTightMassZScaleSublPtCR_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsPSVTightMassIncRealTempSublPtCR_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsPSVTightMassSIEIECorrSublPtCR_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsPSVTightMassSublPtCRLooseCh_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsPSVTightMassOneBin_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsOneBin_2016_02_04
#OUTPUTMAIN=~/Plots/WggPlotsOneBin_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsSublPtCR_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsNewEleOneBin_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlots_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsSinglePhFineBinning_2015_12_01
#OUTPUTMAIN=~/Plots/WggPlotsSinglePh_2015_12_01
OUTPUTJET=$(OUTPUTMAIN)/JetFakeResultsSyst
SYSTFILE=$(OUTPUTMAIN)/JetFakeTemplatePlots/systematics.pickle
PLOTDIR=PlotsUnblind

JETFITVARS=sigmaIEIE chIsoCorr
#JETFITVARS=chIsoCorr
#JETFITVARS=sigmaIEIE
#JETFFCORRINPUTS=nom veryloose loose tight None
JETFFCORRINPUTS=veryloose
MODULE=Modules/JetFakeFit.py
all : plots syst jet ele background evetosf
	@echo "^_^ FINISHED ^_^"

#-----------------------------
# Jet fake estimate ZggOneBin
#PTBINSJET=15,1000000
#SUBLSTR=

#-----------------------------
# Jet fake estimate WggOneBin
PTBINSJET=25,1000000
SUBLSTR=

#-----------------------------
# Jet fake estimate Wgg
#PTBINSJET=,70,1000000
#SUBLSTR=--sublptbins 40,None

#-----------------------------
# Jet fake estimate Zgg
#PTBINSJET=15,25,40,1000000
#SUBLSTR=

#-----------------------------
# Jet fake estimate WggSublPtCR
#PTBINSJET=15,25,40,1000000
#SUBLSTR=--sublptbins 15,25

#-----------------------------
# Single photon binning
SINGLEPTBINS = 15,25,40,70,1000000
#SINGLEPTBINS=15,20,25,30,35,45,55,65,75,85,95,120,1000000


jet :
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels muhighmt --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels mulowmt --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels ellooselowmt --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels ellooselowmtinvpixlead --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels ellooselowmtinvpixsubl --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullhighmt --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullinvpixleadhighmt --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullinvpixsublhighmt --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfulllowmt --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfulllowmtinvpixlead --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfulllowmtinvpixsubl --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrhighmt --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrhighmtinvpixlead --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrhighmtinvpixsubl --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcr --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrinvpixlead --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrinvpixsubl --ptbins $(PTBINSJET) $(SUBLSTR)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFitZgg.py --samplesConfWgg Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels muZgg --ptbins $(PTBINSJET) --zgg
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFitZgg.py --samplesConfWgg Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elZgg --ptbins $(PTBINSJET) --zgg

ele :
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --mc_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDWithOlapPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDWithOlapFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDWithOlapPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDWithOlapFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --mc_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaNoPhID_2015_11_09 --dirInv LepGammaNoPhID_2015_11_09  --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_fine --useCsev
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/ --dirNom LepGammaNoPhID_2015_11_09 --dirInv LepGammaNoPhIDNoElOlapRm_2016_02_05 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDWithOlap_2015_08_24  --dirInv LepGammaMediumPhIDWithOlap_2015_08_24 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_exp_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom TAndPGG_2015_09_14 --dirInv TAndPGG_2015_09_14 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_cms_fine  --useTAndP
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom TAndPGG_2015_09_14 --dirInv TAndPGG_2015_09_14 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_exp_fine  --useTAndP
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom TAndPGG_2015_09_14 --dirInv TAndPGG_2015_09_14 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --mc_cms_fine --useTAndP 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom TAndPGG_2015_09_14 --dirInv TAndPGG_2015_09_14 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_fine --useTAndP
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom TAndPGG_2015_09_14 --dirInv TAndPGG_2015_09_14 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --mc_mc_fine --useTAndP 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom TAndPGG_2015_09_14 --dirInv TAndPGG_2015_09_14 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_ndkeys_fine --useTAndP 

backupele :
	python MakeBackupEleBkgEstimate.py --baseDir $(OUTPUTMAIN)
tandp :
	#python FitTagAndProbe.py  --muon --outputDir ~/Plots/WggPlots_2014_11_20
	#python FitTagAndProbe.py  --electron --outputDir ~/Plots/WggPlots_2014_11_20
	#python FitTagAndProbe.py  --photon --outputDir ~/Plots/WggPlots_2015_01_10

evetosf :
	python DoPhotonEvetoEfficiency.py  --outputDir $(OUTPUTMAIN)

syst :
	python CollectSystUncertanities.py --baseDir $(OUTPUTMAIN) --save

plots :
	python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --makeEleFake --makeJetFakeTemplate --makeJetFakeSyst --makeLepGamma --makeLepLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --makeEleFake --makeJetFakeTemplate --makeLepGamma --makeLepLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeJetFakeSyst --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --makeEleFake --makeJetFakeTemplate --makeLepGamma --makeLepLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeLepLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --lumi 19400 --outputDir $(OUTPUTMAIN)  --save

background :
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,70,1000000 --plotDir $(PLOTDIR)
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,1000000 --plotDir $(PLOTDIR) --zgg
	python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,1000000 --plotDir $(PLOTDIR) --zgg
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 25,1000000 --plotDir $(PLOTDIR)
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 35,40,70,1000000 --sublptbins 35,1000000 --plotDir $(PLOTDIR)
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,1000000 --sublptbins 15,25 --plotDir $(PLOTDIR)
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,1000000 --sublptbins 15,25 --plotDir $(PLOTDIR)SIEIE --useSIEIE
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 25,1000000 --plotDir $(PLOTDIR)
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 25,1000000 --plotDir $(PLOTDIR)SIEIE --useSIEIE

singlebackground :
	#python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir Plots --ptbins 15,20,25,30,35,45,55,65,75,85,95,120,200 --wcr
	#python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir Plots --ptbins 15,20,25,30,35,40,45,50,60,70,150 --zcr
	#python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir PlotsCheck --ptbins 15,25,30,35,40,45,50,55,60,70,150 --wcr
	##python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir PlotsMCND --ptbins 15,25,30,35,40,45,50,60,70,150 --wcr
	python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir PlotsNom --ptbins 15,25,40,70,150 --wcr
	#python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir PlotsNomChHadIso --ptbins 15,25,40,70,150 --zcr
	#python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir Plots --ptbins 15,25,40,70,100 --zcr

finalplots :
	python MakeFinalHists.py  --baseDirComb $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)/Muon --outputDir $(OUTPUTMAIN)/FinalPlotsOneBinMuon  --aqgc
	#python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR) --outputDir $(OUTPUTMAIN)/FinalPlotsOneBin  --muon --electron 
	#python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)LowMt/BackgroundEstimates/$(PLOTDIR) --baseDirComb $(OUTPUTMAIN)LowMt/BackgroundEstimates/$(PLOTDIR)Summed --outputDir $(OUTPUTMAIN)LowMt/FinalPlots --muon --electron 
	#python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)  --outputDir $(OUTPUTMAIN)/FinalPlotsOneBin --zgg
	#python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)/Summed  --outputDir $(OUTPUTMAIN)/MoneyPlots --money
	#python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)/Summed  --outputDir $(OUTPUTMAIN)/MoneyPlots --money --zgg

finalplotssingle :
	#python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/SigmaIEIEFits/Plots  --outputDir $(OUTPUTMAIN)/FinalPlotsWCR --doRatio --suffix SigmaIEIE --wcr 
	#python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/ChHadIsoFits/Plots   --outputDir $(OUTPUTMAIN)/FinalPlotsWCR --doRatio --suffix ChHadIso --wcr 
	#python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/PhoIsoFits/Plots     --outputDir $(OUTPUTMAIN)/FinalPlotsWCR --doRatio --suffix PhoIso --wcr 
	#python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonZCRBackgroundEstimates/SigmaIEIEFits/Plots  --outputDir $(OUTPUTMAIN)/FinalPlotsZCR --doRatio --suffix SigmaIEIE --zcr 
	#python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonZCRBackgroundEstimates/ChHadIsoFits/Plots   --outputDir $(OUTPUTMAIN)/FinalPlotsZCR --doRatio --suffix ChHadIso --zcr 
	#python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonZCRBackgroundEstimates/PhoIsoFits/Plots     --outputDir $(OUTPUTMAIN)/FinalPlotsZCR --doRatio --suffix PhoIso --zcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/SigmaIEIEFits/PlotsMCNDCoarse     --outputDir $(OUTPUTMAIN)/FinalPlotsEValid --doRatio  --evalid

singlephjet : 
	for var in $(JETFITVARS) ; do \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muz --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN)  --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muztest --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN)  --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwtight --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muz --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muztest --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwtight --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elz --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmt --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsr --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrinvpixlead --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elw --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwinvpixlead  --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcrinvpixlead  --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var ; \
	    python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcr  --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var ;\
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrtight  --ptbins $(SINGLEPTBINS)  --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrtightinvpixlead  --ptbins $(SINGLEPTBINS)  --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmtnolepveto --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmttightmuhighpt --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmttightmu --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmtinvd0inviso --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmtinvd0passiso --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmtpassd0inviso --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwhighmet --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmet --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmettightmu --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrlowmt --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrlowmtinvpixlead --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcrlooseinvpixlead --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcrloose --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw_eff_medium --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw_eff_passpsv --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muzpeak_eff_passpsv  --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muzpeak_eff_medium --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	done


	


