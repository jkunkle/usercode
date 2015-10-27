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

OUTPUTMAIN=~/Plots/WggPlots_2015_10_19
#OUTPUTMAIN=~/Plots/WggPlotsWithEleOlap_2015_09_03
OUTPUTJET=$(OUTPUTMAIN)/JetFakeResultsSyst
SYSTFILE=$(OUTPUTMAIN)/JetFakeTemplatePlots/systematics.pickle
PLOTDIR=PlotsUnblind

#JETFITVARS=sigmaIEIE phoIsoCorr chIsoCorr
#JETFITVARS=chIsoCorr
JETFITVARS=sigmaIEIE
#JETFFCORRINPUTS=nom veryloose loose tight None
JETFFCORRINPUTS=veryloose
SINGLEOUTPUT=~/Plots/WggPlots_2015_08_24/
MODULE=Modules/JetFakeFit.py
all : plots syst jet ele background evetosf
	@echo "^_^ FINISHED ^_^"

PTBINSJET=15,25,40,70,1000000
jet :
	##python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE)
	##python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN)
	##python RunMatrixFit.py  --samplesConf Modules/JetFakeFit.py --samplesConfGG Modules/JetFakeFitZgg.py --fileName tree.root --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE)
	##python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN)LowMt --syst_file   $(SYSTFILE)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels muhighmt --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels mulowmt --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels ellooselowmt --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels ellooselowmtinvpixlead --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels ellooselowmtinvpixsubl --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullhighmt --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullhighmtinvpixlead --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullhighmtinvpixsubl --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfulllowmt --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfulllowmtinvpixlead --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfulllowmtinvpixsubl --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrhighmt --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrhighmtinvpixlead --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrhighmtinvpixsubl --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcr --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrinvpixlead --ptbins $(PTBINSJET)
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elzcrinvpixsubl --ptbins $(PTBINSJET)

	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFitZgg.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elZgg,muZgg --ptbins $(PTBINSJET)

ele :
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --mc_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDWithOlapPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDWithOlapFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_cms_fine 
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDWithOlapPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDWithOlapFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --mc_cms_fine 
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/ --dirNom LepGammaMediumPhIDWithOlapPassPixSeed_2015_10_01 --dirInv LepGammaMediumPhIDWithOlapFailPixSeed_2015_10_01 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_fine 
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
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --makeEleFake --makeJetFakeTemplate --makeJetFakeSyst --makeLepGamma --makeLepLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --makeEleFake --makeJetFakeTemplate --makeLepGamma --makeLepLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeJetFakeSyst --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeLepLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --lumi 19400 --outputDir $(OUTPUTMAIN)  --save

background :
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,70,1000000 --plotDir $(PLOTDIR)ManualWithPhoWithCorrNoDiffUnc
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,70,1000000 --plotDir $(PLOTDIR)ZCR 
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,1000000 --plotDir $(PLOTDIR)Zgg 
	python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 25,40,70,1000000 --plotDir $(PLOTDIR)ManualWithPhoWithCorrNoDiffUnc

singlebackground :
	#python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir Plots --ptbins 15,20,25,30,35,40,45,50,60,70,150 --zcr
	#python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir PlotsCheck --ptbins 15,25,30,35,40,45,50,55,60,70,150 --wcr
	python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir PlotsMCND --ptbins 15,25,30,35,40,45,50,60,70,150 --wcr
	#python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir Plots --ptbins 15,25,40,70,100 --zcr

finalplots :
	python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)ManualWithPhoWithCorrNoDiffUnc --outputDir $(OUTPUTMAIN)/FinalPlotsManualWithPhoWithCorrNoDiffUnc  --muon --electron 
	#python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)TAndP7 --baseDirComb $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)ModSummed --outputDir $(OUTPUTMAIN)/FinalPlots --muon --electron 
	#python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)LowMt/BackgroundEstimates/$(PLOTDIR) --baseDirComb $(OUTPUTMAIN)LowMt/BackgroundEstimates/$(PLOTDIR)Summed --outputDir $(OUTPUTMAIN)LowMt/FinalPlots --muon --electron 
	#python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)Zgg  --outputDir $(OUTPUTMAIN)/FinalPlots --zgg

finalplotssingle :
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/SigmaIEIEFits/Plots  --outputDir $(OUTPUTMAIN)/FinalPlotsWCR --doRatio --suffix SigmaIEIE --wcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/ChHadIsoFits/Plots   --outputDir $(OUTPUTMAIN)/FinalPlotsWCR --doRatio --suffix ChHadIso --wcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/PhoIsoFits/Plots     --outputDir $(OUTPUTMAIN)/FinalPlotsWCR --doRatio --suffix PhoIso --wcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonZCRBackgroundEstimates/SigmaIEIEFits/Plots  --outputDir $(OUTPUTMAIN)/FinalPlotsZCR --doRatio --suffix SigmaIEIE --zcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonZCRBackgroundEstimates/ChHadIsoFits/Plots   --outputDir $(OUTPUTMAIN)/FinalPlotsZCR --doRatio --suffix ChHadIso --zcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonZCRBackgroundEstimates/PhoIsoFits/Plots     --outputDir $(OUTPUTMAIN)/FinalPlotsZCR --doRatio --suffix PhoIso --zcr 

singlephjet : 
	for var in $(JETFITVARS) ; do \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muz --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elz --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwtight --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmt --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsr --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrinvpixlead --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elw --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwinvpixlead  --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcrinvpixlead  --ptbins 15,25,30,35,40,45,50,60,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcr  --ptbins 15,25,30,35,40,45,50,60,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrtight  --ptbins 15,25,40,70,1000000  --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrtightinvpixlead  --ptbins 15,25,40,70,1000000  --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmtnolepveto --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmttightmuhighpt --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmttightmu --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmtinvd0inviso --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmtinvd0passiso --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmtpassd0inviso --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwhighmet --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmet --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhIDLooseMuonID_2015_09_22/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muwlowmettightmu --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrlowmt --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhIDWithOlap_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwsrlowmtinvpixlead --ptbins 15,25,40,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcrlooseinvpixlead --ptbins 15,25,30,35,40,45,50,55,60,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcrloose --ptbins 15,25,30,35,40,45,50,55,60,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw_eff_medium --ptbins 15,20,25,30,40,50,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw_eff_passpsv --ptbins 15,20,25,30,40,50,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muzpeak_eff_passpsv  --ptbins 15,20,25,30,40,50,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muzpeak_eff_medium --ptbins 15,20,25,30,40,50,70,1000000 --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	done
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel mu_eff_passpsv --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel mu_eff_passpsv_loose --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel mu_eff_medium_loose --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel mu_eff_medium_tight --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaJJNoPhID_2015_05_05/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muzjj_lowmjj  --pid Tight --ptbins 25,62.5,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \


	


