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
#include <boost/filesystem.hpp>

#include "include/BranchDefs.h"
#include "include/BranchInit.h"

#include "Core/Util.h"

#include "TMVA/Factory.h"
#include "TMVA/Tools.h"

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

    std::string treename;
    std::string outputFileName;
    std::string JobName;
    std::string EtaCut;
    std::vector<std::string> all_sig_files;
    std::vector<std::string> all_bkg_files;
    std::vector<std::string> variables;
    std::vector<std::string> weights;

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
    
        std::map<std::string, std::string>::const_iterator itr; 
        itr = mod_conf.GetInitData().find( "SignalFiles" );
        if( itr != mod_conf.GetInitData().end() ) {
            all_sig_files = Tokenize( itr->second, ",");
        }

        itr = mod_conf.GetInitData().find( "BackgroundFiles" );
        if( itr != mod_conf.GetInitData().end() ) {
            all_bkg_files = Tokenize( itr->second, ",");
        }

        itr = mod_conf.GetInitData().find( "TreeName" );
        if( itr != mod_conf.GetInitData().end() ) {
            treename = itr->second;
        }

        itr = mod_conf.GetInitData().find( "OutputFile" );
        if( itr != mod_conf.GetInitData().end() ) {
            outputFileName = itr->second;
        }

        itr = mod_conf.GetInitData().find( "Variables" );
        if( itr != mod_conf.GetInitData().end() ) {
            variables = Tokenize( itr->second, "," );
        }

        itr = mod_conf.GetInitData().find( "JobName" );
        if( itr != mod_conf.GetInitData().end() ) {
            JobName = itr->second;
        }

        itr = mod_conf.GetInitData().find( "EtaCut" );
        if( itr != mod_conf.GetInitData().end() ) {
            EtaCut = itr->second;
        }

        itr = mod_conf.GetInitData().find( "Weights" );
        if( itr != mod_conf.GetInitData().end() ) {
            weights = Tokenize(itr->second, ",");
        }

        std::cout << "Running MVA for " << JobName << std::endl;

        TFile * outputFile = TFile::Open( outputFileName.c_str(), "RECREATE" );

        std::vector<std::string> path_split = Tokenize( outputFileName, "/" );
        std::string outputDir = "/"+boost::algorithm::join(std::vector<std::string>( path_split.begin(), path_split.end()-1 ) ,  "/" );

        boost::filesystem::create_directories(outputDir.c_str());
                    
        TMVA::Factory *factory = new TMVA::Factory(JobName, outputFile, "!V:!Silent:Color:DrawProgressBar");

        TChain *sigTree = new TChain( treename.c_str() );
        TChain *bkgTree = new TChain( treename.c_str() );

        BOOST_FOREACH( const std::string & file, all_sig_files ) {
            sigTree->Add( file.c_str() );
        }
        BOOST_FOREACH( const std::string & file, all_bkg_files ) {
            bkgTree->Add( file.c_str() );
        }

        float sigWeight = 1.0;
        float bkgWeight = 1.0;
        
        factory->AddSignalTree( sigTree, sigWeight );
        factory->AddBackgroundTree( bkgTree, bkgWeight );

        BOOST_FOREACH( const std::string & wt, weights ) {
            factory->SetSignalWeightExpression( wt );
            factory->SetBackgroundWeightExpression( wt );
        }
            

        BOOST_FOREACH( const std::string & var, variables ) {
            factory->AddVariable( var, 'F');
        }

        TCut etacut(EtaCut.c_str());
        factory->PrepareTrainingAndTestTree(etacut, "");

        factory->BookMethod( TMVA::Types::kBDT, "BDT", "nCuts=40:DoBoostMonitor:MaxDepth=4" );
        factory->BookMethod( TMVA::Types::kKNN, "kNN", "" );
        //factory->BookMethod( TMVA::Types::kMLP, "MLP", "HiddenLayers=1" );

        factory->TrainAllMethods();
  
        factory->TestAllMethods();

        factory->EvaluateAllMethods();
    }


}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    return true;

}


