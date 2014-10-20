#CHANNELS=elzcrinvpixsubl
#CHANNELS=elzcrinvpixlead elfullinvpixsubl elfullinvpixlead
CHANNELS=mu elzcr elfull elzcrinvpixsubl elzcrinvpixlead elfullinvpixsubl elfullinvpixlead
#CHANNELS=mu elzcr elfull elzcrinvpixsubl
#CHANNELS=elzcrinvpixlead elfullinvpixsubl elfullinvpixlead

#CHANNELS=mu
#CHANNELS=elzcr
#CHANNELS=elfull
#CHANNELS=elzcrinvpixlead
#CHANNELS=elzcrinvpixsubl
#CHANNELS=elfullinvpixlead elfullinvpixsubl
#CHANNELS=elfullinvpixsubl
SYSTFILE=~/Plots/WggPlots_2014_10_16/JetFakeTemplatePlots/systematics.pickle
#SYSTFILE=~/Plots/WggPlots_2014_09_24/JetFakeTemplatePlots/systematics.pickle
OUTPUT=~/Plots/WggPlots_2014_10_16/JetFakeResultsSyst
PTBINS=15,25,40,70,1000000
SINGLEOUTPUT=~/Plots/WggPlots_2014_10_06/
all :
	@echo "Choose jet or syst or plots"
jet : 
	for item in $(CHANNELS) ; do \
	    #python RunMatrixFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUT) --nom --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	    python RunMatrixFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUT) --asymcorr533 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS);  \
	    #python RunMatrixFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUT) --asymcorr855 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	    #python RunMatrixFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUT) --asymcorr1077 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS);  \
	    #python RunMatrixFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUT) --asymcorr1299 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	    #python RunMatrixFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUT) --asymcorr151111 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	    #python RunMatrixFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --outputDir $(OUTPUT) --asymcorr201616 --channel $$item --syst_file $(SYSTFILE) --ptbins $(PTBINS); \
	done

ele :
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir ~/Plots/WggPlots_2014_10_02_last70

syst :
	#python CollectSystUncertanities.py --baseDir ~/Plots/WggPlots_2014_09_24  --save
	python CollectSystUncertanities.py --baseDir ~/Plots/WggPlots_2014_10_16 --save

plots :
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEleFake --makeJetFakeTemplate  --makeEvent --lumi 19400 --outputDir ~/Plots/WggPlots_2014_10_02_last70  --save
	python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --makeSinglePhoton --makeEleFake --makeJetFakeTemplate  --lumi 19400 --outputDir ~/Plots/WggPlots_2014_10_16  --save
	#python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --lumi 19400 --outputDir ~/Plots/WggPlots_2014_09_24  --save

background :
	python MakeBackgroundEstimates.py --baseDir ~/Plots/WggPlots_2014_10_02_last70 --ptbins 15,25,40,70,1000000

singlephjet : 
	#python RunSinglePhotonFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel elzcrinvpixlead --outputDir $(SINGLEOUTPUT) 
	#python RunSinglePhotonFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel elinvpixlead --outputDir  $(SINGLEOUTPUT)
	python RunSinglePhotonFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel el --outputDir $(SINGLEOUTPUT)
	#python RunSinglePhotonFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel elzcr --outputDir $(SINGLEOUTPUT) 
	python RunSinglePhotonFit.py --baseDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoEleVetoNewVar_2014_05_02/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --nom --channel mu --outputDir $(SINGLEOUTPUT)
