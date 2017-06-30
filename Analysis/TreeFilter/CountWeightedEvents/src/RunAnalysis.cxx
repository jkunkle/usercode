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
    chain->SetBranchStatus("*", 0);
    chain->SetBranchStatus("EvtWeights", 1);
    n_total = 0;
    n_weighted = 0;
    
}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    n_total++;

    if( IN::EvtWeights->at(0) < 0 ) {
        n_weighted--;
    }
    else {
        n_weighted++;
    }


}

void RunModule::finalize() {

    std::cout << "Total events = " << n_total << " Weighted events = " << n_weighted << std::endl;


}

