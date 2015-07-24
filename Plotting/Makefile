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

#OUTPUTMAIN=~/Plots/WggPlotsNoMggSublPt30_2015_07_19
OUTPUTMAIN=~/Plots/ZggPlots_2015_07_20
#OUTPUTMAIN=~/Plots/WggPlots_2015_06_05
OUTPUTJET=$(OUTPUTMAIN)/JetFakeResultsSyst
SYSTFILE=$(OUTPUTMAIN)/JetFakeTemplatePlots/systematics.pickle
PLOTDIR=PlotsUnblind

JETFITVARS=sigmaIEIE phoIsoCorr chIsoCorr
#JETFFCORRINPUTS=nom veryloose loose tight None
JETFFCORRINPUTS=veryloose
PTBINS=15,25,40,70,1000000
#PTBINS=15,1000000
SINGLEOUTPUT=~/Plots/WggPlotsNoMgg_2015_07_05/
MODULE=Modules/JetFakeFit.py
all : plots syst jet ele background evetosf
	@echo "^_^ FINISHED ^_^"
jet : 
	for item in $(CHANNELS) ; do \
	    for var in $(JETFITVARS) ; do \
	        for ffinput in $(JETFFCORRINPUTS) ; do \
	            #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --nom --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS) --fitvar $$var --ffcorr $$ffinput --quiet ; \
	            python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr533 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS) --fitvar $$var --ffcorr $$ffinput  --quiet;  \
	            #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr855 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS) --fitvar $$var --ffcorr $$ffinput  --quiet; \
	            #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr1077 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS) --fitvar $$var --ffcorr $$ffinput  --quiet;  \
	            #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr1299 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS) --fitvar $$var --ffcorr $$ffinput  --quiet; \
	            #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr151111 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS) --fitvar $$var --ffcorr $$ffinput  --quiet; \
	            #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr201616 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS) --fitvar $$var --ffcorr $$ffinput  --quiet; \
		done \
	    done \
	done

newjet :
	#python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE)
	python RunMatrixFit.py  --samplesConf Modules/JetFakeFit.py --samplesConfGG Modules/JetFakeFitZgg.py --fileName tree.root --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE)



ele :
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_07_16/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_cms_fine 
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_07_16/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_cms_coarse
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_07_16/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_exp_fine 
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_07_16/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_exp_coarse 
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_07_16/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_fine 
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_07_16/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_coarse

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
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --lumi 19400 --outputDir $(OUTPUTMAIN)  --save

background :
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,70,1000000 --plotDir $(PLOTDIR) --mtcut " > 40 "
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 30,40,70,1000000 --plotDir $(PLOTDIR) --mtcut " > 40 "
	python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,1000000 --plotDir $(PLOTDIR) --mtcut " > -100 "
	#python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN)LowMt --ptbins 15,25,40,70,1000000 --plotDir $(PLOTDIR) --mtcut " < 40 "

singlebackground :
	#python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir Plots --ptbins 15,20,25,30,35,40,45,50,60,70,150 --zcr
	python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir Plots --ptbins 15,20,25,30,35,40,45,50,60,70,150 --wcr

finalplots :
	python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR) --baseDirComb $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)Summed --outputDir $(OUTPUTMAIN)/FinalPlots --muon --electron 
	#python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)LowMt/BackgroundEstimates/$(PLOTDIR) --baseDirComb $(OUTPUTMAIN)LowMt/BackgroundEstimates/$(PLOTDIR)Summed --outputDir $(OUTPUTMAIN)LowMt/FinalPlots --muon --electron 

finalplotssingle :
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/SigmaIEIEFits/Plots  --outputDir $(OUTPUTMAIN)/FinalPlotsWCR --doRatio --suffix SigmaIEIE --wcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/ChHadIsoFits/Plots   --outputDir $(OUTPUTMAIN)/FinalPlotsWCR --doRatio --suffix ChHadIso --wcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/PhoIsoFits/Plots     --outputDir $(OUTPUTMAIN)/FinalPlotsWCR --doRatio --suffix PhoIso --wcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonZCRBackgroundEstimates/SigmaIEIEFits/Plots  --outputDir $(OUTPUTMAIN)/FinalPlotsZCR --doRatio --suffix SigmaIEIE --zcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonZCRBackgroundEstimates/ChHadIsoFits/Plots   --outputDir $(OUTPUTMAIN)/FinalPlotsZCR --doRatio --suffix ChHadIso --zcr 
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonZCRBackgroundEstimates/PhoIsoFits/Plots     --outputDir $(OUTPUTMAIN)/FinalPlotsZCR --doRatio --suffix PhoIso --zcr 

singlephjet : 
	for var in $(JETFITVARS) ; do \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elw --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwinvpixlead --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcrinvpixlead --ptbins 15,20,25,30,35,40,45,50,60,70,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elwzcr --ptbins 15,20,25,30,35,40,45,50,60,70,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel mu --ptbins 15,20,25,30,35,40,45,50,60,70,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw --ptbins 15,20,25,30,35,40,45,50,60,70,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel el --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel murealcr --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel elrealcr --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel mu_tp_eveto --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel mu_tp_eveto_loose --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muzpeak_tp_eveto  --ptbins 15,20,25,30,40,50,70,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muzpeak_tp_medium --ptbins 15,20,25,30,40,50,70,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel mu_tp_medium_loose --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    ##python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel mu_tp_medium_tight --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw_tp_medium --ptbins 15,20,25,30,40,50,70,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_06_29/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muw_tp_eveto --ptbins 15,20,25,30,40,50,70,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaJJNoPhID_2015_05_05/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muzjj_lowmjj  --pid Tight --ptbins 25,62.5,1000000 --outputDir $(SINGLEOUTPUT) --fitvar $$var; \
	done


	


