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

    calib_tdc_vs_evt = new TH2F( "calib_tdc_vs_evt", "PIN diode TDC time vs event",160, 0, 160000, 300, 0, 150 );
     
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

    std::map<std::pair<int, int>, float> numerator_sum;
    std::map<std::pair<int, int>, float> denominator_sum;
    for( unsigned ich = 0; ich < nch; ich++ ) {

        int ieta = IN::QIE10DigiIEta->at(ich);
        int iphi = IN::QIE10DigiIPhi->at(ich);
        int depth = IN::QIE10DigiDepth->at(ich);
        int subdet = IN::QIE10DigiSubdet->at(ich);

        if( subdet == 4 ) {

            EtaPhiDepth channel( ieta, iphi, depth);

            if( charge_ratio_ts2_ts3.find( channel ) == charge_ratio_ts2_ts3.end() ) {

                std::stringstream name_1;
                std::stringstream name_2;
                std::stringstream name_3;
                std::stringstream title_1;
                std::stringstream title_2;
                std::stringstream title_3;
                name_1 << "charge_ratio_ts1_ts2_" << ieta << "_" << iphi << "_" << depth;
                name_2 << "charge_ratio_ts2_ts3_" << ieta << "_" << iphi << "_" << depth;
                name_3 << "tdc_time_vs_evt_" << ieta << "_" << iphi << "_" << depth;

                title_1 << "Charge ratio in TS1 and TS2, IEta=" << ieta << ", IPhi=" << iphi << ", Depth=" << depth;
                title_2 << "Charge ratio in TS2 and TS3, IEta=" << ieta << ", IPhi=" << iphi << ", Depth=" << depth;
                title_3 << "TDC time vs event, IEta=" << ieta << ", IPhi=" << iphi << ", Depth=" << depth;


                charge_ratio_ts1_ts2[channel] = new TH2F( name_1.str().c_str(), title_1.str().c_str(), 160, 0, 160000, 100, 0, 1 );
                charge_ratio_ts2_ts3[channel] = new TH2F( name_2.str().c_str(), title_2.str().c_str(), 160, 0, 160000, 100, 0, 1 );
                tdc_time_vs_evt[channel] = new TH2F( name_3.str().c_str(), title_3.str().c_str(), 160, 0, 160000, 300, 0, 150 );
                    
            }

            std::pair<int,int> ieta_iphi = std::make_pair(ieta, iphi);
            if( numerator_sum.find( ieta_iphi ) == numerator_sum.end() ) {
                numerator_sum[ieta_iphi] = 0;
                denominator_sum[ieta_iphi] = 0;
            }

            float fc_1 = IN::QIE10DigiFC->at(ich)[1];
            float fc_2 = IN::QIE10DigiFC->at(ich)[2];
            float fc_3 = IN::QIE10DigiFC->at(ich)[3];

            float ts_sum = 0;
            for( unsigned its = 0; its < nts; ++its ) {
                ts_sum += IN::QIE10DigiFC->at(ich)[its];
            }

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

            tdc_time_vs_evt[channel]->Fill( IN::event, tdc_time );

            charge_ratio_ts1_ts2[channel]->Fill( IN::event, (fc_1 + fc_2)/ts_sum );
            charge_ratio_ts2_ts3[channel]->Fill( IN::event, (fc_2 + fc_3)/ts_sum );

            denominator_sum[ieta_iphi] = denominator_sum[ieta_iphi] + ts_sum;
            numerator_sum[ieta_iphi] = numerator_sum[ieta_iphi] + fc_2 + fc_3;
            
        }

        if( subdet==7 && depth == 12 && ieta == -48 && iphi == 25  ) {

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

        calib_tdc_vs_evt->Fill( IN::event, tdc_time);
        }
        
    }

    for( std::map<std::pair<int, int>, float>::const_iterator itr = numerator_sum.begin();
            itr != numerator_sum.end(); ++itr ) {

        if( charge_ratio_ts2_ts3_sum.find( itr->first ) == charge_ratio_ts2_ts3_sum.end() ) {

            std::stringstream name;
            std::stringstream title;
            name << "charge_ratio_ts2_ts3_sum_" << itr->first.first << "_" << itr->first.second;
            title << "Charge ratio in TS2 and TS3, Depth sum, IEta=" << itr->first.first << ", IPhi=" << itr->first.second ;
            charge_ratio_ts2_ts3_sum[itr->first] = new TH2F( name.str().c_str(), title.str().c_str(), 160, 0, 160000, 100, 0, 1 );
        }

        charge_ratio_ts2_ts3_sum[itr->first]->Fill( IN::event, itr->second/(denominator_sum[itr->first]) );

    }
}

void RunModule::finalize() {

    calib_tdc_vs_evt->Write();

    for( std::map<EtaPhiDepth, TH2F*>::const_iterator itr = charge_ratio_ts1_ts2.begin(); itr != charge_ratio_ts1_ts2.end(); ++itr ) {
        itr->second->Write();
    }
    for( std::map<EtaPhiDepth, TH2F*>::const_iterator itr = charge_ratio_ts2_ts3.begin(); itr != charge_ratio_ts2_ts3.end(); ++itr ) {
        itr->second->Write();
    }
    for( std::map<EtaPhiDepth, TH2F*>::const_iterator itr = tdc_time_vs_evt.begin(); itr != tdc_time_vs_evt.end(); ++itr ) {
        itr->second->Write();
    }
    for( std::map<std::pair<int,int>, TH2F*>::const_iterator itr = charge_ratio_ts2_ts3_sum.begin(); itr != charge_ratio_ts2_ts3_sum.end(); ++itr ) {
        itr->second->Write();
    }
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



