#include "include/RunAnalysis.h"

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <boost/foreach.hpp>
#include <boost/algorithm/string.hpp>
#include <sys/types.h>
#include <sys/stat.h>
#include <math.h>
#include <stdlib.h>

#include "include/BranchDefs.h"
#include "include/BranchInit.h"

#include "Core/Util.h"

#include "TFile.h"

int main(int argc, char **argv)
{

    //TH1::AddDirectory(kFALSE);
    CmdOptions options = ParseOptions( argc, argv );

    // Parse the text file and form the configuration object
    AnaConfig ana_config = ParseConfig( options.config_file, options );
    std::cout << "Configured " << ana_config.size() << " analysis modules " << std::endl;

    RunModule runmod;
    ana_config.Run(runmod, options);

    std::cout << "^_^ Finished ^_^" << std::endl;


}

void RunModule::initialize( TChain * chain, TTree * outtree, TFile *outfile,
                            const CmdOptions & options, std::vector<ModuleConfig> &configs ) {

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Set defaults for added output variables
    // *************************
    //OUT::ph_mvascore_5var              = 0;
    //OUT::ph_mvascore_6var              = 0;
    OUT::ph_mvascore_11varW              = 0;
    //OUT::ph_mvascore_11var              = 0;

    // *************************
    // Declare Branches
    // *************************

    // Examples :
    //outtree->Branch("ph_mvascore_6var" , &OUT::ph_mvascore_6var                                      );
    //outtree->Branch("ph_mvascore_11var"     , &OUT::ph_mvascore_11var);
    outtree->Branch("ph_mvascore_11varW"     , &OUT::ph_mvascore_11varW);
    //outtree->Branch("ph_mvascore_5var"     , &OUT::ph_mvascore_5var);

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {

        if( mod_conf.GetName() == "BuildPhoton" ) { 
            std::map<std::string, std::string>::const_iterator citr;
            //citr = mod_conf.GetInitData().find( "TMVAWeightsFileEB11" );
            //if( citr != mod_conf.GetInitData().end() ) {
            //    std::string mva_weights = citr->second;  
            //    TMVAReaderEB11 = new TMVA::Reader( "!Color:!Silent:Error" );
            //    TMVAReaderEB11->SetVerbose(true);

            //    TMVAReaderEB11->AddVariable("phoR9", &MVAVars::phoR9);
            //    TMVAReaderEB11->AddVariable("phoSigmaIEtaIEta", &MVAVars::phoSigmaIEtaIEta  );
            //    TMVAReaderEB11->AddVariable("phoSigmaIEtaIPhi", &MVAVars::phoSigmaIEtaIPhi );
            //    TMVAReaderEB11->AddVariable("phoE2x2/phoE5x5", &MVAVars::s4ratio );
            //    TMVAReaderEB11->AddVariable("phoE1x3/phoE5x5", &MVAVars::s13 );
            //    TMVAReaderEB11->AddVariable("phoE2x5Max/phoE5x5", &MVAVars::s25 );
            //    //TMVAReaderEB11->AddVariable("s13", &MVAVars::s13 );
            //    //TMVAReaderEB11->AddVariable("s4ratio", &MVAVars::s4ratio );
            //    //TMVAReaderEB11->AddVariable("s25", &MVAVars::s25 );
            //    TMVAReaderEB11->AddVariable("phoSCEtaWidth", &MVAVars::phoSCEtaWidth );
            //    TMVAReaderEB11->AddVariable("phoSCPhiWidth", &MVAVars::phoSCPhiWidth );
            //    TMVAReaderEB11->AddVariable("phoPFPhoIso", &MVAVars::phoPFPhoIso );
            //    TMVAReaderEB11->AddVariable("phoPFChIso", &MVAVars::phoPFChIso );
            //    TMVAReaderEB11->AddVariable("phoPFChIsoWorst", &MVAVars::phoPFChIsoWorst );
            //    //TMVAReaderEB11->AddSpectator("phoEt", &MVAVars::phoEt);
            //    //TMVAReaderEB11->AddSpectator("phoEta", &MVAVars::phoEta);

            //    TMVAReaderEB11->BookMVA("BDT", mva_weights);


            //}
            citr = mod_conf.GetInitData().find( "TMVAWeightsFileEB11W" );
            if( citr != mod_conf.GetInitData().end() ) {
                std::string mva_weights = citr->second;  
                TMVAReaderEB11W = new TMVA::Reader( "!Color:!Silent:Error" );
                TMVAReaderEB11W->SetVerbose(true);


                TMVAReaderEB11W->AddVariable("ph_r9", &MVAVars::ph_r9);
                TMVAReaderEB11W->AddVariable("ph_sigmaIEIE", &MVAVars::ph_sigmaIEIE);
                TMVAReaderEB11W->AddVariable("ph_sigmaIEIP", &MVAVars::ph_sigmaIEIP);
                TMVAReaderEB11W->AddVariable("ph_s4ratio", &MVAVars::ph_s4ratio);
                TMVAReaderEB11W->AddVariable("ph_s13", &MVAVars::ph_s13);
                TMVAReaderEB11W->AddVariable("ph_s25", &MVAVars::ph_s25);
                TMVAReaderEB11W->AddVariable("ph_SCetaWidth", &MVAVars::ph_SCetaWidth);
                TMVAReaderEB11W->AddVariable("ph_SCphiWidth", &MVAVars::ph_SCphiWidth);
                TMVAReaderEB11W->AddVariable("ph_phoIsoCorr", &MVAVars::ph_phoIsoCorr);
                TMVAReaderEB11W->AddVariable("ph_chIsoCorr", &MVAVars::ph_chIsoCorr);
                TMVAReaderEB11W->AddVariable("ph_pfChIsoWorst", &MVAVars::ph_pfChIsoWorst);
                TMVAReaderEB11W->BookMVA("BDT", mva_weights);


            }

            //citr = mod_conf.GetInitData().find( "TMVAWeightsFileEE11" );
            //if( citr != mod_conf.GetInitData().end() ) {
            //    std::string mva_weights = citr->second;  
            //    TMVAReaderEE11 = new TMVA::Reader( "!Color:!Silent:Error" );
            //    TMVAReaderEE11->SetVerbose(true);

            //    TMVAReaderEE11->AddVariable("phoR9", &MVAVars::phoR9 );
            //    TMVAReaderEE11->AddVariable("phoSigmaIEtaIEta", &MVAVars::phoSigmaIEtaIEta );
            //    TMVAReaderEE11->AddVariable("phoSigmaIEtaIPhi", &MVAVars::phoSigmaIEtaIPhi );
            //    TMVAReaderEE11->AddVariable("s13", &MVAVars::s13 );
            //    TMVAReaderEE11->AddVariable("s4ratio", &MVAVars::s4ratio );
            //    TMVAReaderEE11->AddVariable("s25", &MVAVars::s25 );
            //    TMVAReaderEE11->AddVariable("phoSCEtaWidth", &MVAVars::phoSCEtaWidth );
            //    TMVAReaderEE11->AddVariable("phoSCPhiWidth", &MVAVars::phoSCPhiWidth );
            //    TMVAReaderEE11->AddVariable("phoPFPhoIso", &MVAVars::phoPFPhoIso );
            //    TMVAReaderEE11->AddVariable("phoPFChIso", &MVAVars::phoPFChIso );
            //    TMVAReaderEE11->AddVariable("phoPFChIsoWorst", &MVAVars::phoPFChIsoWorst );

            //    //TMVAReaderEE11->AddSpectator("phoEt", &MVAVars::phoEt);
            //    //TMVAReaderEE11->AddSpectator("phoEta", &MVAVars::phoEta);
            //    
            //    TMVAReaderEE11->BookMVA("BDT", mva_weights);
            //}
            
            citr = mod_conf.GetInitData().find( "TMVAWeightsFileEE11W" );
            if( citr != mod_conf.GetInitData().end() ) {
                std::string mva_weights = citr->second;  
                TMVAReaderEE11W = new TMVA::Reader( "!Color:!Silent:Error" );
                TMVAReaderEE11W->SetVerbose(true);

                TMVAReaderEE11W->AddVariable("ph_r9", &MVAVars::ph_r9);
                TMVAReaderEE11W->AddVariable("ph_sigmaIEIE", &MVAVars::ph_sigmaIEIE);
                TMVAReaderEE11W->AddVariable("ph_sigmaIEIP", &MVAVars::ph_sigmaIEIP);
                TMVAReaderEE11W->AddVariable("ph_s4ratio", &MVAVars::ph_s4ratio);
                TMVAReaderEE11W->AddVariable("ph_s13", &MVAVars::ph_s13);
                TMVAReaderEE11W->AddVariable("ph_s25", &MVAVars::ph_s25);
                TMVAReaderEE11W->AddVariable("ph_SCetaWidth", &MVAVars::ph_SCetaWidth);
                TMVAReaderEE11W->AddVariable("ph_SCphiWidth", &MVAVars::ph_SCphiWidth);
                TMVAReaderEE11W->AddVariable("ph_phoIsoCorr", &MVAVars::ph_phoIsoCorr);
                TMVAReaderEE11W->AddVariable("ph_chIsoCorr", &MVAVars::ph_chIsoCorr);
                TMVAReaderEE11W->AddVariable("ph_pfChIsoWorst", &MVAVars::ph_pfChIsoWorst);
                TMVAReaderEE11W->BookMVA("BDT", mva_weights);
            }
            //citr = mod_conf.GetInitData().find( "TMVAWeightsFileEB6" );
            //if( citr != mod_conf.GetInitData().end() ) {
            //    std::string mva_weights = citr->second;  
            //    TMVAReaderEB6 = new TMVA::Reader( "!Color:!Silent:Error" );
            //    TMVAReaderEB6->SetVerbose(true);

            //    TMVAReaderEB6->AddVariable("phoR9", &MVAVars::phoR9);
            //    TMVAReaderEB6->AddVariable("phoSigmaIEtaIEta", &MVAVars::phoSigmaIEtaIEta  );
            //    TMVAReaderEB6->AddVariable("phoSigmaIEtaIPhi", &MVAVars::phoSigmaIEtaIPhi );
            //    TMVAReaderEB6->AddVariable("phoPFPhoIso", &MVAVars::phoPFPhoIso );
            //    TMVAReaderEB6->AddVariable("phoPFChIso", &MVAVars::phoPFChIso );
            //    TMVAReaderEB6->AddVariable("phoPFChIsoWorst", &MVAVars::phoPFChIsoWorst );

            //    TMVAReaderEB6->BookMVA("BDT", mva_weights);


            //}
            //citr = mod_conf.GetInitData().find( "TMVAWeightsFileEE6" );
            //if( citr != mod_conf.GetInitData().end() ) {
            //    std::string mva_weights = citr->second;  
            //    TMVAReaderEE6 = new TMVA::Reader( "!Color:!Silent:Error" );
            //    TMVAReaderEE6->SetVerbose(true);

            //    TMVAReaderEE6->AddVariable("phoR9", &MVAVars::phoR9 );
            //    TMVAReaderEE6->AddVariable("phoSigmaIEtaIEta", &MVAVars::phoSigmaIEtaIEta );
            //    TMVAReaderEE6->AddVariable("phoSigmaIEtaIPhi", &MVAVars::phoSigmaIEtaIPhi );
            //    TMVAReaderEE6->AddVariable("phoPFPhoIso", &MVAVars::phoPFPhoIso );
            //    TMVAReaderEE6->AddVariable("phoPFChIso", &MVAVars::phoPFChIso );
            //    TMVAReaderEE6->AddVariable("phoPFChIsoWorst", &MVAVars::phoPFChIsoWorst );

            //    TMVAReaderEE6->BookMVA("BDT", mva_weights);
            //}
            //citr = mod_conf.GetInitData().find( "TMVAWeightsFileEB5" );
            //if( citr != mod_conf.GetInitData().end() ) {
            //    std::string mva_weights = citr->second;  
            //    TMVAReaderEB5 = new TMVA::Reader( "!Color:!Silent:Error" );
            //    TMVAReaderEB5->SetVerbose(true);

            //    TMVAReaderEB5->AddVariable("phoHoverE12", &MVAVars::phoHoverE12  );
            //    TMVAReaderEB5->AddVariable("phoSigmaIEtaIEta", &MVAVars::phoSigmaIEtaIEta  );
            //    TMVAReaderEB5->AddVariable("phoPFChIsoPtRhoCorr", &MVAVars::phoPFChIsoPtRhoCorr );
            //    TMVAReaderEB5->AddVariable("phoPFNeuIsoPtRhoCorr", &MVAVars::phoPFNeuIsoPtRhoCorr );
            //    TMVAReaderEB5->AddVariable("phoPFPhoIsoPtRhoCorr", &MVAVars::phoPFPhoIsoPtRhoCorr );

            //    TMVAReaderEB5->BookMVA("BDT", mva_weights);


            //}
            //citr = mod_conf.GetInitData().find( "TMVAWeightsFileEE5" );
            //if( citr != mod_conf.GetInitData().end() ) {
            //    std::string mva_weights = citr->second;  
            //    TMVAReaderEE5 = new TMVA::Reader( "!Color:!Silent:Error" );
            //    TMVAReaderEE5->SetVerbose(true);

            //    TMVAReaderEE5->AddVariable("phoHoverE12", &MVAVars::phoHoverE12  );
            //    TMVAReaderEE5->AddVariable("phoSigmaIEtaIEta", &MVAVars::phoSigmaIEtaIEta  );
            //    TMVAReaderEE5->AddVariable("phoPFChIsoPtRhoCorr", &MVAVars::phoPFChIsoPtRhoCorr );
            //    TMVAReaderEE5->AddVariable("phoPFNeuIsoPtRhoCorr", &MVAVars::phoPFNeuIsoPtRhoCorr );
            //    TMVAReaderEE5->AddVariable("phoPFPhoIsoPtRhoCorr", &MVAVars::phoPFPhoIsoPtRhoCorr );

            //    TMVAReaderEE5->BookMVA("BDT", mva_weights);
            //}
        }
    }
}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    CopyInputVarsToOutput();

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        save_event &= ApplyModule( mod_conf );
    }

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    // This bool is used for filtering
    // If a module implements an event filter
    // update this variable and return it
    // to apply the filter
    bool keep_evt = true;

    // This part is a bit hacked.  For each module that
    // you write below, you have to put a call to that
    // function with a matching name here.
    // The name is used to match the name used
    // in the python configuration.
    // There are fancy ways to do this, but it
    // would require the code to be much more complicated
    //
    // Example :
    if( config.GetName() == "BuildPhoton" ) {
        BuildPhoton( config );
    }

    // If the module applies a filter the filter decision
    // is passed back to here.  There is no requirement
    // that a function returns a bool, but
    // if you want the filter to work you need to do this
    //
    // Example :

    return keep_evt;

}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//
// Examples :

void RunModule::BuildPhoton( ModuleConfig & config ) const {

    OUT::ph_mvascore_11varW  -> clear();
    //OUT::ph_mvascore_6var  -> clear();
    //OUT::ph_mvascore_5var  -> clear();

    for( int idx = 0; idx < IN::ph_n; ++idx ) {
        //float sigmaIEIE    = IN::ph_sigmaIEIE->at(idx);
        //float sigmaIEIP    = IN::ph_sigmaIEIP->at(idx);
        //float r9           = IN::ph_r9->at(idx);
        //float E1x3         = IN::ph_E1x3->at(idx);
        //float E2x2         = IN::ph_E2x2->at(idx);
        //float E5x5         = IN::ph_E5x5->at(idx);
        //float E2x5Max      = IN::ph_E2x5Max->at(idx);
        //float SCetaWidth   = IN::ph_SCetaWidth->at(idx);
        //float SCphiWidth   = IN::ph_SCphiWidth->at(idx);
        //float pfChIsoWorst = IN::ph_pfChIsoWorst->at(idx);
        //float phoIso       = IN::ph_phoIso->at(idx);
        //float chIso        = IN::ph_chIso->at(idx);
        //float sceta        = IN::ph_sceta->at(idx);
        //float hoverE12     = IN::ph_HoverE->at(idx);
        //float pfPhoIsoCorr = IN::ph_phoIsoCorr->at(idx);
        //float pfChIsoCorr  = IN::ph_chIsoCorr->at(idx);
        //float pfNeuIsoCorr = IN::ph_neuIsoCorr->at(idx);

        //float r9Corr = r9;
        //if( fabs(sceta) < 1.479 ) {
        //    r9Corr = 0.000740 + 1.00139*r9;
        //}
        //else {
        //    r9Corr = -0.000399 + 1.00016*r9;
        //}

        //bool pass_mva_presel        = IN::ph_pass_mva_presel->at(idx);
        
        MVAVars::ph_r9           = IN::ph_r9           ->at(idx);
        MVAVars::ph_sigmaIEIE    = IN::ph_sigmaIEIE    ->at(idx);
        MVAVars::ph_sigmaIEIP    = IN::ph_sigmaIEIP    ->at(idx);
        MVAVars::ph_s4ratio      = IN::ph_E2x2->at(idx)/IN::ph_E5x5->at(idx);
        MVAVars::ph_s13          = IN::ph_E1x3->at(idx)/IN::ph_E5x5->at(idx);
        MVAVars::ph_s25          = IN::ph_E2x5Max->at(idx)/IN::ph_E5x5->at(idx);
        MVAVars::ph_SCetaWidth   = IN::ph_SCetaWidth   ->at(idx);
        MVAVars::ph_SCphiWidth   = IN::ph_SCphiWidth   ->at(idx);
        MVAVars::ph_phoIsoCorr   = IN::ph_phoIsoCorr   ->at(idx);
        MVAVars::ph_chIsoCorr    = IN::ph_chIsoCorr    ->at(idx);
        MVAVars::ph_pfChIsoWorst = IN::ph_pfChIsoWorst ->at(idx);
        
        

        bool iseb                   = IN::ph_IsEB->at(idx);
        bool isee                   = IN::ph_IsEE->at(idx);


        ////MVAVars::phoPhi           = phi;
        //MVAVars::phoR9            = r9Corr;
        //MVAVars::phoSigmaIEtaIEta = sigmaIEIE;
        //MVAVars::phoSigmaIEtaIPhi = sigmaIEIP;
        //MVAVars::s4ratio          = E2x2/E5x5;
        //MVAVars::s13              = E1x3/E5x5;
        //MVAVars::s25              = E2x5Max/E5x5;
        ////MVAVars::phoSCEta         = sceta;
        ////MVAVars::phoSCRawE        = SCRawE;
        //MVAVars::phoSCEtaWidth    = SCetaWidth;
        //MVAVars::phoSCPhiWidth    = SCphiWidth;
        ////MVAVars::rho2012          = rho;
        //MVAVars::phoPFPhoIso      = phoIso;
        //MVAVars::phoPFChIso       = chIso;
        //MVAVars::phoPFChIsoWorst  = pfChIsoWorst;
        //MVAVars::phoPFChIsoPtRhoCorr = pfChIsoCorr;
        //MVAVars::phoPFNeuIsoPtRhoCorr = pfNeuIsoCorr;
        //MVAVars::phoPFPhoIsoPtRhoCorr = pfPhoIsoCorr;
        //MVAVars::phoHoverE12          = hoverE12;
        ////MVAVars::phoESEnToRawE    = esE/SCRawE;
        ////MVAVars::phoESEffSigmaRR  = ESEffSigmaRR;

        bool pass_mva_presel=true;
        if( pass_mva_presel ) {
            if( iseb ) {
                //OUT::ph_mvascore_5var->push_back(TMVAReaderEB5->EvaluateMVA("BDT"));
                //OUT::ph_mvascore_6var->push_back(TMVAReaderEB6->EvaluateMVA("BDT"));
                //OUT::ph_mvascore_11var->push_back(TMVAReaderEB11->EvaluateMVA("BDT"));
                OUT::ph_mvascore_11varW->push_back(TMVAReaderEB11W->EvaluateMVA("BDT"));
            }
            else if( isee ){
                //OUT::ph_mvascore_5var->push_back(TMVAReaderEE5->EvaluateMVA("BDT"));
                //OUT::ph_mvascore_6var->push_back(TMVAReaderEE6->EvaluateMVA("BDT"));
                //OUT::ph_mvascore_11var->push_back(TMVAReaderEE11->EvaluateMVA("BDT"));
                OUT::ph_mvascore_11varW->push_back(TMVAReaderEE11W->EvaluateMVA("BDT"));
            }
            else {
                //OUT::ph_mvascore_5var->push_back(-99);
                //OUT::ph_mvascore_6var->push_back(-99);
                //OUT::ph_mvascore_11var->push_back(-99);
                OUT::ph_mvascore_11varW->push_back(-99);
            }
        }
        else {
            //OUT::ph_mvascore_5var->push_back(-99);
            //OUT::ph_mvascore_6var->push_back(-99);
            //OUT::ph_mvascore_11var->push_back(-99);
            OUT::ph_mvascore_11varW->push_back(-99);
        }

    }

}

