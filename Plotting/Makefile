#CHANNELS=mu elzcr elfull elzcrinvpixsubl elzcrinvpixlead elfullinvpixsubl elfullinvpixlead
#CHANNELS=mu
#CHANNELS=elzcr elfull elzcrinvpixsubl elzcrinvpixlead elfullinvpixsubl elfullinvpixlead
#CHANNELS=muZgg
#CHANNELS=elfull 
#CHANNELS=elzcr elfull
#CHANNELS=elph1zcr elph2zcr
#CHANNELS=elzcrinvpixsubl elzcrinvpixlead 
#CHANNELS=elph1zcrinvpixsubl elph1zcrinvpixlead 
#CHANNELS=elph2zcrinvpixsubl elph2zcrinvpixlead 
CHANNELS=elph2zcrinvpixlead elph1zcrinvpixlead 
#CHANNELS=elfullinvpixsubl elfullinvpixlead
#CHANNELS=elzcrinvpixlead
#CHANNELS=elzcrinvpixsubl elzcrinvpixlead elfullinvpixsubl elfullinvpixlead
#CHANNELS=mu elzcr elfull elzcrinvpixsubl
#CHANNELS=elzcrinvpixlead elzcrinvpixsubl elfullinvpixsubl elfullinvpixlead

#CHANNELS=muZgg
#CHANNELS=elzcr
#CHANNELS=elfull
#CHANNELS=elzcrinvpixlead
#CHANNELS=elzcrinvpixsubl
#CHANNELS=elfullinvpixlead
#CHANNELS=elfullinvpixsubl
#SYSTFILE=~/Plots/WggPlots_2014_09_24/JetFakeTemplatePlots/systematics.pickle
#OUTPUT=~/Plots/WggPlots_2014_12_08/JetFakeResultsSyst
OUTPUTMAIN=~/Plots/WggPlots_2015_01_20
OUTPUTJET=$(OUTPUTMAIN)/JetFakeResultsSyst
SYSTFILE=$(OUTPUTMAIN)/JetFakeTemplatePlots/systematics.pickle

PTBINS=15,25,40,70,1000000
#PTBINS=15,1000000
SINGLEOUTPUT=~/Plots/WggPlots_2015_01_10/
MODULE=Modules/JetFakeFit.py
all : plots syst jet ele background evetosf
	@echo "^_^ FINISHED ^_^"
jet : 
	for item in $(CHANNELS) ; do \
	    #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --nom --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	    #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr533 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS);  \
	    #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr855 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	    #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr1077 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS);  \
	    #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr1299 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	    #python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr151111 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	    python RunMatrixFit.py --samplesConf $(MODULE) --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUTJET) --asymcorr201616 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	done

ele :
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2014_12_23/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_cms_fine 
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2014_12_23/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_cms_coarse
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2014_12_23/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_exp_fine 
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2014_12_23/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --bw_exp_coarse 
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2014_12_23/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_fine 
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2014_12_23/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_coarse

	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPElFF_2015_01_01/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir ~/Plots/WggPlots_2014_12_23 --bw_cms_fine --useTAndP
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPElFF_2015_01_01/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir ~/Plots/WggPlots_2014_12_23 --bw_cms_coarse --useTAndP
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPElFF_2015_01_01/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir ~/Plots/WggPlots_2014_12_23 --bw_exp_fine --useTAndP
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPElFF_2015_01_01/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir ~/Plots/WggPlots_2014_12_23 --bw_exp_coarse --useTAndP
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPElFF_2015_01_01/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir ~/Plots/WggPlots_2014_12_23 --ndkeys_cms_fine --useTAndP
	#python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/TAndPElFF_2015_01_01/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir ~/Plots/WggPlots_2014_12_23 --ndkeys_cms_coarse --useTAndP

tandp :
	#python FitTagAndProbe.py  --muon --outputDir ~/Plots/WggPlots_2014_11_20
	#python FitTagAndProbe.py  --electron --outputDir ~/Plots/WggPlots_2014_11_20
	#python FitTagAndProbe.py  --photon --outputDir ~/Plots/WggPlots_2015_01_10

evetosf :
	python DoPhotonEvetoEfficiency.py  --outputDir $(OUTPUTMAIN)

syst :
	python CollectSystUncertanities.py --baseDir $(OUTPUTMAIN) --save

plots :
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEleFake --makeJetFakeTemplate  --makeEvent --lumi 19400 --outputDir ~/Plots/WggPlots_2014_10_02_last70  --save
	python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --makeEleFake --makeJetFakeTemplate --makeLooseDiPhoton --makeLepGamma --makeLepLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --lumi 19400 --outputDir ~/Plots/WggPlots_2014_09_24  --save

background :
	python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,25,40,70,1000000


singlephjet : 
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel elw --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel elwinvpixlead --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel elwzcrinvpixlead --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel elwzcr --outputDir $(SINGLEOUTPUT) 
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel mu --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel el --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel murealcr --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel elrealcr --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel mu_tp_eveto --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel mu_tp_eveto_loose --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel mu_tp_eveto_tight --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel mu_tp_medium --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel mu_tp_medium_loose --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel mu_tp_medium_tight --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel muw --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel muw_tp_medium --outputDir $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel muw_tp_eveto --outputDir $(SINGLEOUTPUT)
