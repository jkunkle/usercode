#include "include/RunAnalysis.h"

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <numeric>
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

    int nevt = chain->GetEntries();
    
    TDCTimevsIPhiHFM = new TH2F( "TDCTimevsIPhiHFM", "TDC time vs IPhi, HFM", 150, 0, 75, 8, 1, 9 );
    TDCTimevsIPhiHFP = new TH2F( "TDCTimevsIPhiHFP", "TDC time vs IPhi, HFP", 150, 0, 75, 8, 1, 9 );
    
    //_outfile = outfile;
    //
    std::string HFemap = "/afs/cern.ch/user/j/jkunkle/usercode/Analysis/TreeFilter/MakeHFPlots/data/ngHF2018LMap_20171215_K.txt";

    std::ifstream file(HFemap);
    std::string line;

    if( file.is_open() ) {

        while( getline(file, line) ) {

            std::string valid_line = line;

            std::vector<std::string> module_split = Tokenize( line, " " );

            if( valid_line.substr(0, 1) == "#" ) continue;

            int side;
            std::stringstream side_ss( module_split[0] );
            side_ss >> side;

            int abseta;
            std::stringstream abseta_ss( module_split[1] );
            abseta_ss >> abseta;

            int iphi;
            std::stringstream iphi_ss( module_split[2] );
            iphi_ss >> iphi;

            int depth;
            std::stringstream depth_ss( module_split[4] );
            depth_ss >> depth;

            std::string rbx_name = module_split[6];

            int rbx;
            std::stringstream rbx_ss(rbx_name.substr(3, 2));
            std::cout << "RBX ss = " << rbx_ss.str() << std::endl;
            rbx_ss >> rbx;

            rbx_map[EtaPhiDepth(side*abseta, iphi, depth)] = rbx;
        }
    }

     
}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    _evn++;

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        save_event &= ApplyModule( mod_conf );
    }

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) {

    bool keep_evt = true;

    if( config.GetName() == "PlotHF" ) {
        PlotHF( config );
    }
    return false;

}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//
// Examples :

void RunModule::PlotHF( ModuleConfig & config ) {

    unsigned nch = IN::QIE10DigiIEta->size();
    unsigned nts = IN::QIE10DigiADC->at(0).size();

    for( unsigned ich = 0; ich < nch; ich++ ) {

        int ieta = IN::QIE10DigiIEta->at(ich);
        int iphi = IN::QIE10DigiIPhi->at(ich);
        int depth = IN::QIE10DigiDepth->at(ich);

        int rbx = rbx_map[EtaPhiDepth( ieta, iphi, depth)];

        float tdc_time = 0;
        for( unsigned its = 0; its < nts; ++its ) {

            int tdc = IN::QIE10DigiLETDC->at(ich)[its];

            if( tdc <= 50 ) {
                tdc_time += tdc;
                break;
            }
            else {
                tdc_time += 50;
            }
        }
        tdc_time = tdc_time /2.;

        if( ieta < 0 ) {
            TDCTimevsIPhiHFM->Fill( tdc_time, rbx);
        }
        else {
            TDCTimevsIPhiHFP->Fill( tdc_time, rbx);
        }
        
    }

}

void RunModule::finalize() {

    TDCTimevsIPhiHFM->Write();
    TDCTimevsIPhiHFP->Write();
}

EtaPhiDepth::EtaPhiDepth( int _ieta, int _iphi, int _depth ) {

    ieta = _ieta;
    iphi = _iphi;
    depth = _depth;

}

bool EtaPhiDepth::operator<( const EtaPhiDepth &r ) const {
    if( ieta == r.ieta ) {
        if( iphi == r.iphi ) {
            return depth < r.depth;
        }
        else {
            return iphi < r.iphi;
        }
    }
    else {
        return ieta < r.ieta;
    }
}



