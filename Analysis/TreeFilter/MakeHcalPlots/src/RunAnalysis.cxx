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
    
    avg_adc_event_HBHE = new TH1F( "avg_adc_event_HBHE", "avg_adc_event_HBHE", nevt, 0, nevt );
    avg_adc_event_HF   = new TH1F( "avg_adc_event_HF", "avg_adc_event_HF", nevt, 0, nevt );
    avg_adc_HBHE = new TH1F( "avg_adc_HBHE", "avg_adc_HBHE", 500, 0, 500 );
    avg_adc_HF   = new TH1F( "avg_adc_HF", "avg_adc_HF", 100, 0, 100 );
    adc_depth_highadc = new TH2F( "adc_depth_highadc", "adc_depth_highadc", 82, -41, 41, 73, 0, 73 );
    adc_depth = new TH2F( "adc_depth", "adc_depth", 82, -41, 41, 73, 0, 73 );
    adc_HBHE = new TH1F( "adc_HBHE", "adc_HBHE", 128, 0, 1280 );
    adc_HF = new TH1F( "adc_HF", "adc_HF", 200, 0, 800 );
    bx_HBHE_highadc = new TH1F( "bx_HBHE_highadc", "bx_HBHE_highadc", 3600, 0, 3600 );
    bx_HF_highadc = new TH1F( "bx_HF_highadc", "bx_HF_highadc", 3600, 0, 3600 );
    
    _outfile = outfile;

    _evn = 0;
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

    if( config.GetName() == "PlotHBHE" ) {
        PlotHBHE( config );
    }
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

void RunModule::PlotHBHE( ModuleConfig & config ) {

    unsigned nch = IN::HBHEDigiIEta->size();
    unsigned nts = IN::HBHEDigiADC->at(0).size();

    int adc_sum = 0;
    for( unsigned ich = 0; ich < nch; ich++ ) {

        int ieta = IN::HBHEDigiIEta->at(ich);
        int iphi = IN::HBHEDigiIPhi->at(ich);
        int depth = IN::HBHEDigiDepth->at(ich);

        if( depth > 1  ) {
            continue;
        }

        std::pair<int, int> ch_id = std::make_pair( ieta, iphi );

        std::map<std::pair<int,int>, TH1F >::const_iterator itr = ch_adc_map.find( ch_id );
        std::map<std::pair<int,int>, TH1F >::const_iterator hitr = ch_highadc_map.find( ch_id );
        if( itr == ch_adc_map.end() ) {
            std::stringstream name;
            name  << "hist_" << ieta << "_" << iphi;
            ch_adc_map[ch_id] = TH1F( name.str().c_str(),name.str().c_str(), 100, 0, 1280 ) ;
        }
        if( hitr == ch_highadc_map.end() ) {
            std::stringstream name;
            name  << "histhighadc_" << ieta << "_" << iphi;
            ch_highadc_map[ch_id] = TH1F( name.str().c_str(),name.str().c_str(), 100, 0, 1280 ) ;
        }


        int ch_sum = 0;
        for( unsigned its = 0; its < nts; its++ ) {

            ch_sum += IN::HBHEDigiADC->at(ich)[its];

        }

        ch_adc_map[ch_id].Fill( ch_sum );
        adc_HBHE->Fill( ch_sum );
        adc_sum += ch_sum;

        if( ch_sum > 100 ) {
            ch_highadc_map[ch_id].Fill( ch_sum );
        }

    }

    avg_adc_event_HBHE->SetBinContent( _evn, float(adc_sum)/nch );
    avg_adc_HBHE->Fill( float(adc_sum)/nch );
    if( float(adc_sum)/nch > 100 ) {
        bx_HBHE_highadc->Fill( IN::bx );
    }


    for( std::map<std::pair<int, int>, TH1F>::const_iterator mitr = ch_adc_map.begin(); mitr != ch_adc_map.end(); ++mitr ) {

        float val = mitr->second.GetMean();

        int bin = adc_depth->FindBin( mitr->first.first, mitr->first.second);

        adc_depth->SetBinContent( bin, val );
    }

    for( std::map<std::pair<int, int>, TH1F >::const_iterator mitr = ch_highadc_map.begin(); mitr != ch_highadc_map.end(); ++mitr ) {

        float val = mitr->second.GetMean();

        int bin = adc_depth_highadc->FindBin( mitr->first.first, mitr->first.second);

        adc_depth_highadc->SetBinContent( bin, val );
    }

}

void RunModule::PlotHF( ModuleConfig & config ) {

    unsigned nch = IN::QIE10DigiIEta->size();
    unsigned nts = IN::QIE10DigiADC->at(0).size();

    int adc_sum = 0;
    for( unsigned ich = 0; ich < nch; ich++ ) {

        int ieta = IN::QIE10DigiIEta->at(ich);
        int iphi = IN::QIE10DigiIPhi->at(ich);
        int depth = IN::QIE10DigiDepth->at(ich);

        if( depth > 1  ) {
            continue;
        }

        std::pair<int, int> ch_id = std::make_pair( ieta, iphi );

        std::map<std::pair<int,int>, TH1F >::const_iterator itr = ch_adc_map.find( ch_id );
        std::map<std::pair<int,int>, TH1F >::const_iterator hitr = ch_highadc_map.find( ch_id );
        if( itr == ch_adc_map.end() ) {
            std::stringstream name;
            name  << "hist_" << ieta << "_" << iphi;
            ch_adc_map[ch_id] = TH1F( name.str().c_str(),name.str().c_str(), 100, 0, 1280 ) ;
        }
        if( hitr == ch_highadc_map.end() ) {
            std::stringstream name;
            name  << "histhighadc_" << ieta << "_" << iphi;
            ch_highadc_map[ch_id] = TH1F( name.str().c_str(),name.str().c_str(), 100, 0, 1280 ) ;
        }


        int ch_sum = 0;
        for( unsigned its = 0; its < nts; its++ ) {

            ch_sum += IN::QIE10DigiADC->at(ich)[its];

        }

        ch_adc_map[ch_id].Fill( ch_sum );
        adc_HF->Fill( ch_sum );
        adc_sum += ch_sum;

        if( ch_sum > 100 ) {
            ch_highadc_map[ch_id].Fill( ch_sum );
        }

    }

    avg_adc_event_HF->SetBinContent( _evn, float(adc_sum)/nch );
    avg_adc_HF->Fill( float(adc_sum)/nch );
    if( float(adc_sum)/nch > 20 ) {
        bx_HF_highadc->Fill( IN::bx );
    }

    for( std::map<std::pair<int, int>, TH1F>::const_iterator mitr = ch_adc_map.begin(); mitr != ch_adc_map.end(); ++mitr ) {

        float val = mitr->second.GetMean();

        int bin = adc_depth->FindBin( mitr->first.first, mitr->first.second);

        adc_depth->SetBinContent( bin, val );
    }

    for( std::map<std::pair<int, int>, TH1F>::const_iterator mitr = ch_highadc_map.begin(); mitr != ch_highadc_map.end(); ++mitr ) {

        float val = mitr->second.GetMean();

        int bin = adc_depth_highadc->FindBin( mitr->first.first, mitr->first.second);

        adc_depth_highadc->SetBinContent( bin, val );
    }


}

void RunModule::finalize() {

    _outfile->cd();

    avg_adc_event_HBHE->Write();
    avg_adc_event_HF->Write();
    avg_adc_HBHE->Write();
    avg_adc_HF->Write();
    adc_depth_highadc->Write();
    adc_depth->Write();
    adc_HBHE->Write();
    adc_HF->Write();
    bx_HF_highadc->Write();
    bx_HBHE_highadc->Write();

}


