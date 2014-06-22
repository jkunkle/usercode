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
    // Examples :
    OUT::zrej_mvascore             = 0;

    // *************************
    // Declare Branches
    // *************************

    // Examples :
    outtree->Branch("zrej_mvascore"             , &OUT::zrej_mvascore, "zrej_mvascore/F" );                 

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {

        if( mod_conf.GetName() == "EvalMVA" ) { 
            std::map<std::string, std::string>::const_iterator citr;
            citr = mod_conf.GetInitData().find( "TMVAWeightsFileEl" );
            if( citr != mod_conf.GetInitData().end() ) {
                std::string mva_weights = citr->second;  
                TMVAReaderEl = new TMVA::Reader( "!Color:!Silent:Error" );
                TMVAReaderEl->SetVerbose(true);

                TMVAReaderEl->AddVariable("m_lepphph", &MVAVars::m_lepphph);
                TMVAReaderEl->AddVariable("m_lepph1", &MVAVars::m_lepph1);
                TMVAReaderEl->AddVariable("m_lepph2", &MVAVars::m_lepph2);
                TMVAReaderEl->AddVariable("m_phph", &MVAVars::m_phph );
                TMVAReaderEl->AddVariable("leadPhot_leadLepDR", &MVAVars::leadPhot_leadLepDR);
                TMVAReaderEl->AddVariable("sublPhot_leadLepDR", &MVAVars::sublPhot_leadLepDR );
                TMVAReaderEl->AddVariable("ph_phDR", &MVAVars::ph_phDR);
                ///TMVAReaderEl->AddVariable("dphi_met_lep1", &MVAVars::dphi_met_lep1);
                ///TMVAReaderEl->AddVariable("dphi_met_ph1",  &MVAVars::dphi_met_ph1);
                ///TMVAReaderEl->AddVariable("dphi_met_ph2",  &MVAVars::dphi_met_ph2);

                TMVAReaderEl->BookMVA("BDT", mva_weights);
            }
            citr = mod_conf.GetInitData().find( "TMVAWeightsFileMu" );
            if( citr != mod_conf.GetInitData().end() ) {
                std::string mva_weights = citr->second;  
                TMVAReaderMu = new TMVA::Reader( "!Color:!Silent:Error" );
                TMVAReaderMu->SetVerbose(true);

                TMVAReaderMu->AddVariable("m_lepphph", &MVAVars::m_lepphph);
                TMVAReaderMu->AddVariable("m_lepph1", &MVAVars::m_lepph1);
                TMVAReaderMu->AddVariable("m_lepph2", &MVAVars::m_lepph2);
                TMVAReaderMu->AddVariable("m_phph", &MVAVars::m_phph );
                TMVAReaderMu->AddVariable("leadPhot_leadLepDR", &MVAVars::leadPhot_leadLepDR);
                TMVAReaderMu->AddVariable("sublPhot_leadLepDR", &MVAVars::sublPhot_leadLepDR );
                TMVAReaderMu->AddVariable("ph_phDR", &MVAVars::ph_phDR);
                //TMVAReaderMu->AddVariable("dphi_met_lep1", &MVAVars::dphi_met_lep1);
                //TMVAReaderMu->AddVariable("dphi_met_ph1",  &MVAVars::dphi_met_ph1);
                //TMVAReaderMu->AddVariable("dphi_met_ph2",  &MVAVars::dphi_met_ph2);

                TMVAReaderMu->BookMVA("BDT", mva_weights);
            }
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
    if( config.GetName() == "EvalMVA" ) {
        EvalMVA( config );
    }

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

// This is an example of a module that applies an
// event filter.  Note that it returns a bool instead
// of a void.  In principle the modules can return any
// type of variable, you just have to handle it
// in the ApplyModule function

void RunModule::EvalMVA( ModuleConfig & config ) const {

    OUT::zrej_mvascore = -99;

    if( IN::ph_n==2 && IN::leadPhot_pt>15 && IN::sublPhot_pt>15 && IN::ph_passMedium ) {

        MVAVars::m_lepphph = IN::m_lepphph;
        MVAVars::m_lepph1 = IN::m_lepph1;
        MVAVars::m_lepph2 = IN::m_lepph2;
        MVAVars::m_phph  = IN::m_phph ;
        MVAVars::leadPhot_leadLepDR = IN::leadPhot_leadLepDR;
        MVAVars::sublPhot_leadLepDR  = IN::sublPhot_leadLepDR ;
        MVAVars::ph_phDR = IN::ph_phDR;
        //MVAVars::dphi_met_lep1 = IN::dphi_met_lep1 ;
        //MVAVars::dphi_met_ph1 = IN::dphi_met_ph1 ;
        //MVAVars::dphi_met_ph2 = IN::dphi_met_ph2 ;


        if( IN::el_passtrig_n>0 && IN::el_n==1 && TMVAReaderEl ) {
            OUT::zrej_mvascore = TMVAReaderEl->EvaluateMVA("BDT");
        }
        //if( IN::mu_passtrig_n>0 && IN::mu_n==1 && TMVAReaderMu ) {
        //    OUT::zrej_mvascore = TMVAReaderMu->EvaluateMVA("BDT");
        //}
    }
    
}

