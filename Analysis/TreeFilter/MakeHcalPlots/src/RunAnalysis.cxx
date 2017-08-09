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
    
    laser_user_word = new TH1F( "laser_user_word", "laser_user_word", 20, 0, 20 );
    avg_adc_HBHE = new TH1F( "avg_adc_HBHE", "avg_adc_HBHE", 500, 0, 500 );
    avg_adc_HF   = new TH1F( "avg_adc_HF", "avg_adc_HF", 300, 0, 300 );
    avg_adc_HBHE_vs_umnqie1 = new TH2F( "avg_adc_HBHE_vs_umnqie1", "avg_adc_HBHE_vs_umnqie1", 100, 0, 500, 50, 0, 500 );
    avg_adc_HF_vs_umnqie1   = new TH2F( "avg_adc_HF_vs_umnqie1", "avg_adc_HF_vs_umnqie1", 50, 0, 300, 50, 0, 500 );
    avg_adc_HBHE_vs_umnqie2 = new TH2F( "avg_adc_HBHE_vs_umnqie2", "avg_adc_HBHE_vs_umnqie2", 100, 0, 500, 50, 0, 500 );
    avg_adc_HF_vs_umnqie2   = new TH2F( "avg_adc_HF_vs_umnqie2", "avg_adc_HF_vs_umnqie2", 50, 0, 300, 50, 0, 500 );
    avg_adc_umnqie1_vs_umnqie2   = new TH2F( "avg_adc_umnqie1_vs_umnqie2", "avg_adc_umnqie1_vs_umnqie2", 50, 0, 500, 50, 0, 500 );
    adc_umnqie1_vs_umnqie2_laserHBHE= new TH2F( "adc_umnqie1_vs_umnqie2_laserHBHE", "adc_umnqie1_vs_umnqie2_laserHBHE", 50, 0, 500, 50, 0, 500 );
    adc_umnqie1_vs_umnqie2_laserHF= new TH2F( "adc_umnqie1_vs_umnqie2_laserHF", "adc_umnqie1_vs_umnqie2_laserHF", 50, 0, 500, 50, 0, 500 );
    adc_depth_highadc = new TH2F( "adc_depth_highadc", "adc_depth_highadc", 82, -41, 41, 73, 0, 73 );
    adc_depth_bxadc = new TH2F( "adc_depth_bxadc", "adc_depth_bxadc", 82, -41, 41, 73, 0, 73 );
    adc_depth = new TH2F( "adc_depth", "adc_depth", 82, -41, 41, 73, 0, 73 );
    adc_HBHE = new TH1F( "adc_HBHE", "adc_HBHE", 128, 0, 1280 );
    adc_HF = new TH1F( "adc_HF", "adc_HF", 200, 0, 800 );
    adc_umnqie1 = new TH1F( "adc_umnqie1", "adc_umnqie1", 128, 0, 500 );
    adc_umnqie2 = new TH1F( "adc_umnqie2", "adc_umnqie2", 128, 0, 500 );
    bx_HBHE_highadc = new TH1F( "bx_HBHE_highadc", "bx_HBHE_highadc", 3600, 0, 3600 );
    bx_HF_highadc = new TH1F( "bx_HF_highadc", "bx_HF_highadc", 3600, 0, 3600 );

    totdiff_HBHE = new TH1F( "totdiff_HBHE", "totdiff_HBHE", 35640, 0, 356400 );
    totdiff_HF = new TH1F( "totdiff_HF", "totdiff_HF", 35640, 0, 356400 );

    n_fires_orn_hf = new TH1F( "n_fires_orn_hf", "n_fires_orn_hf", 300000, 0, 300000);
    n_fires_orn_hbhe = new TH1F( "n_fires_orn_hbhe", "n_fires_orn_hbhe", 100, 0, 100 );
    

    
    _outfile = outfile;

    _evn = 0;
    _lastLS = 0;
    _lastORN = 0;
    _lastBX = 0;

    match_list_hbhe.push_back(std::make_pair(296593, 70317338) );
    match_list_hbhe.push_back(std::make_pair(296593, 70317338) );
    match_list_hbhe.push_back(std::make_pair(296593, 70285976) );
    match_list_hbhe.push_back(std::make_pair(296593, 71551580) );
    match_list_hf.push_back(std::make_pair(296608, 13481597) );
    match_list_hf.push_back(std::make_pair(296608, 14010238) );
    match_list_hf.push_back(std::make_pair(296608, 14010238) );
    match_list_hf.push_back(std::make_pair(296608, 13976637) );
    match_list_hf.push_back(std::make_pair(296608, 13929597) );
    match_list_hf.push_back(std::make_pair(296608, 14252156) );
    match_list_hbhe.push_back(std::make_pair(296609, 5774) );
    match_list_hbhe.push_back(std::make_pair(296609, 5774) );
    match_list_hbhe.push_back(std::make_pair(296609, 279042) );
    match_list_hbhe.push_back(std::make_pair(296609, 279042) );
    match_list_hbhe.push_back(std::make_pair(296609, 5488559) );
    match_list_hbhe.push_back(std::make_pair(296609, 5488559) );
    match_list_hf.push_back(std::make_pair(296623, 42831539) );
    match_list_hf.push_back(std::make_pair(296623, 42990576) );
    match_list_hf.push_back(std::make_pair(296623, 42990576) );
    match_list_hf.push_back(std::make_pair(296623, 43057803) );
    match_list_hf.push_back(std::make_pair(296623, 43245940) );
    match_list_hf.push_back(std::make_pair(296623, 43151855) );
    match_list_hf.push_back(std::make_pair(296623, 43499065) );
    match_list_hf.push_back(std::make_pair(296623, 43508016) );
    match_list_hf.push_back(std::make_pair(296623, 43521455) );
    match_list_hf.push_back(std::make_pair(296623, 43543855) );
    match_list_hf.push_back(std::make_pair(296623, 43543855) );
    match_list_hf.push_back(std::make_pair(296623, 43604334) );
    match_list_hf.push_back(std::make_pair(296623, 43667069) );
    match_list_hf.push_back(std::make_pair(296623, 43541613) );
    match_list_hf.push_back(std::make_pair(296623, 43709628) );
    match_list_hf.push_back(std::make_pair(296623, 43516976) );
    match_list_hf.push_back(std::make_pair(296625, 19899249) );
    match_list_hf.push_back(std::make_pair(296625, 20418360) );
    match_list_hf.push_back(std::make_pair(296625, 20418360) );

    for( unsigned i =0; i < match_list_hbhe.size(); ++i ) {
        std::stringstream name;
        name << "bxhist_run_" << match_list_hbhe[i].first << "_orn_" << match_list_hbhe[i].second;
        runorn_bx_hists_hbhe[match_list_hbhe[i]] = TH1F( name.str().c_str(), name.str().c_str(), 3564, 0, 3564 );
    }
     
    for( unsigned i =0; i < match_list_hf.size(); ++i ) {
        std::stringstream name;
        name << "bxhist_run_" << match_list_hf[i].first << "_orn_" << match_list_hf[i].second;
        runorn_bx_hists_hf[match_list_hf[i]] = TH1F( name.str().c_str(), name.str().c_str(), 3564, 0, 3564 );
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

    if( config.GetName() == "PlotHBHE" ) {
        PlotHBHE( config );
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

    if( IN::run == 296578 ) return;

    laser_user_word->Fill(IN::LaserUserWord);

    unsigned nch = IN::QIE10DigiIEta->size();
    unsigned nts = IN::QIE10DigiADC->at(0).size();

    int adc_sum = 0;
    int adc_sum_umnqie1 = 0;
    int adc_sum_umnqie2 = 0;
    int counted_ch = 0;
    for( unsigned ich = 0; ich < nch; ich++ ) {

        int ieta = IN::QIE10DigiIEta->at(ich);
        int iphi = IN::QIE10DigiIPhi->at(ich);
        int depth = IN::QIE10DigiDepth->at(ich);

        if( depth == 5 ) {

            int ch_sum = 0;
            for( unsigned its = 0; its < nts; its++ ) {

                ch_sum += IN::QIE10DigiADC->at(ich)[its];

                if( ieta < 0 ) {
                    adc_umnqie1->Fill( ch_sum );
                    adc_sum_umnqie1 = ch_sum;
                }
                else {
                    adc_umnqie2->Fill( ch_sum );
                    adc_sum_umnqie2 = ch_sum;
                }
            }
        }

        if( depth > 1  ) {
            continue;
        }

        counted_ch++;

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

    avg_adc_HF->Fill( float(adc_sum)/counted_ch );
    avg_adc_HF_vs_umnqie1->Fill( float(adc_sum)/counted_ch, adc_sum_umnqie1 );
    avg_adc_HF_vs_umnqie2->Fill( float(adc_sum)/counted_ch, adc_sum_umnqie2 );
    avg_adc_umnqie1_vs_umnqie2->Fill( adc_sum_umnqie1, adc_sum_umnqie2 );
    if( float(adc_sum)/counted_ch > 50 ) {

        adc_umnqie1_vs_umnqie2_laserHF->Fill( adc_sum_umnqie1, adc_sum_umnqie2 );

        int bx = IN::bx;

        std::map<int, TH1F>::const_iterator itr = orn_ls_run296609_HF.find( IN::run );
        if( itr == orn_ls_run296609_HF.end() ) {
            std::stringstream name;
            name << "LaserORNHF_Run_" << IN::run;
            TH1F thishist( name.str().c_str(), name.str().c_str(), 100000000, 0, 100000000 );
            orn_ls_run296609_HF[IN::run] = thishist;
        }

        orn_ls_run296609_HF[IN::run].Fill( IN::orbit );
                

        std::vector<std::pair<unsigned, unsigned> >::const_iterator vitr = std::find( match_list_hf.begin(), match_list_hf.end(), std::make_pair( IN::run, IN::orbit ) );

        if( vitr != match_list_hf.end() ) {
            runorn_bx_hists_hf[std::make_pair( IN::run, IN::orbit )].Fill( IN::bx );
        }




        bx_HF_highadc->Fill( bx );

        if( bx < 425 || bx > 440 ) {
            std::stringstream name;
            name << "RunHF_" << IN::run << "_LS_" << IN::ls << "_EVENT_" << IN::event << "_ORN_" << IN::orbit << "_BX_" << bx;
            TH2F thishist( name.str().c_str(), name.str().c_str(), 82, -41, 41, 73, 0, 73 );
            std::stringstream nameumn;
            nameumn << "uMNqieHF_" << IN::run << "_LS_" << IN::ls << "_EVENT_" << IN::event << "_ORN_" << IN::orbit << "_BX_" << bx;
            TH2F thishistqie( nameumn.str().c_str(), nameumn.str().c_str(), 50, 0, 500, 50, 0, 500);

            if( _lastLS == IN::ls ) {

                int orn_diff = IN::orbit - _lastORN;
                int bx_diff = bx - _lastBX;
                
                int tot_diff = orn_diff * 3564 + bx_diff;

                totdiff_HF->Fill( tot_diff );

            }

            thishistqie.Fill( adc_sum_umnqie1, adc_sum_umnqie2 );

            umnqie_highadc_outbx_list.push_back( thishistqie );

            for( unsigned ich = 0; ich < nch; ich++ ) {

                int ieta = IN::QIE10DigiIEta->at(ich);
                int iphi = IN::QIE10DigiIPhi->at(ich);
                int depth = IN::QIE10DigiDepth->at(ich);

                if( depth > 1  ) {
                    continue;
                }

                int ch_sum = 0;
                for( unsigned its = 0; its < nts; its++ ) {

                    ch_sum += IN::QIE10DigiADC->at(ich)[its];

                }
                int binid = thishist.FindBin( ieta, iphi);
                thishist.SetBinContent( binid, ch_sum );
            }
            adc_depth_highadc_outbx_list.push_back( thishist);
        }
        else {

            for( unsigned ich = 0; ich < nch; ich++ ) {

                int ieta  = IN::QIE10DigiIEta->at(ich);
                int iphi  = IN::QIE10DigiIPhi->at(ich);
                int depth = IN::QIE10DigiDepth->at(ich);

                if( depth > 1  ) {
                    continue;
                }

                int ch_sum = 0;
                for( unsigned its = 0; its < nts; its++ ) {

                    ch_sum += IN::QIE10DigiADC->at(ich)[its];

                }

                std::pair<int, int> ch_id = std::make_pair( ieta, iphi );
                std::map<std::pair<int,int>, TH1F >::const_iterator bitr = ch_bxadc_map.find( ch_id );

                if( bitr == ch_bxadc_map.end() ) {

                    std::stringstream name;
                    name  << "histbx_" << ieta << "_" << iphi;
                    ch_bxadc_map[ch_id] = TH1F( name.str().c_str(),name.str().c_str(), 100, 0, 800 ) ;
                }

                ch_bxadc_map[ch_id].Fill( ch_sum );
            }
        }
        _lastLS = IN::ls;
        _lastORN = IN::orbit;
        _lastBX = IN::bx;
    }


    nch = IN::HBHEDigiIEta->size();
    nts = IN::HBHEDigiADC->at(0).size();


    adc_sum = 0;
    int tot_ch = 4128;
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

    avg_adc_HBHE->Fill( float(adc_sum)/tot_ch);

    avg_adc_HBHE_vs_umnqie1->Fill( float(adc_sum)/tot_ch, adc_sum_umnqie1 );
    avg_adc_HBHE_vs_umnqie2->Fill( float(adc_sum)/tot_ch, adc_sum_umnqie2 );
    if( float(adc_sum)/tot_ch > 60 ) {

        adc_umnqie1_vs_umnqie2_laserHBHE->Fill( adc_sum_umnqie1, adc_sum_umnqie2 );

        std::map<int, TH1F>::const_iterator itr = orn_ls_run296609_HBHE.find( IN::run );
        if( itr == orn_ls_run296609_HBHE.end() ) {
            std::stringstream name;
            name << "LaserORNHBHE_Run_" << IN::run;
            TH1F thishist( name.str().c_str(), name.str().c_str(), 100000000, 0, 100000000 );
            orn_ls_run296609_HBHE[IN::run] = thishist;
        }

        orn_ls_run296609_HBHE[IN::run].Fill( IN::orbit );

        std::vector<std::pair<unsigned,unsigned> >::const_iterator vitr = std::find( match_list_hbhe.begin(), match_list_hbhe.end(), std::make_pair( IN::run, IN::orbit ) );

        if( vitr != match_list_hbhe.end() ) {
            runorn_bx_hists_hbhe[std::make_pair( IN::run, IN::orbit )].Fill( IN::bx );
        }


        int bx = IN::bx;
        bx_HBHE_highadc->Fill( bx );

        if( bx < 425 || bx > 440 ) {
            std::stringstream name;
            name << "RunHBHE_" << IN::run << "_LS_" << IN::ls << "_EVENT_" << IN::event << "_ORN_" << IN::orbit << "_BX_" << bx;
            TH2F thishist( name.str().c_str(), name.str().c_str(), 82, -41, 41, 73, 0, 73 );
            std::stringstream nameumn;
            nameumn << "uMNqieHBHE_" << IN::run << "_LS_" << IN::ls << "_EVENT_" << IN::event << "_ORN_" << IN::orbit << "_BX_" << bx;
            TH2F thishistqie( nameumn.str().c_str(), nameumn.str().c_str(), 50, 0, 500, 50, 0, 500);

            if( _lastLS == IN::ls ) {

                int orn_diff = IN::orbit - _lastORN;
                int bx_diff = bx - _lastBX;
                
                int tot_diff = orn_diff * 3564 + bx_diff;
                totdiff_HBHE->Fill( tot_diff );

                        
            }

            thishistqie.Fill( adc_sum_umnqie1, adc_sum_umnqie2 );

            umnqie_highadc_outbx_list.push_back( thishistqie );

            for( unsigned ich = 0; ich < nch; ich++ ) {

                int ieta = IN::HBHEDigiIEta->at(ich);
                int iphi = IN::HBHEDigiIPhi->at(ich);
                int depth = IN::HBHEDigiDepth->at(ich);

                if( depth > 1  ) {
                    continue;
                }

                int ch_sum = 0;
                for( unsigned its = 0; its < nts; its++ ) {

                    ch_sum += IN::HBHEDigiADC->at(ich)[its];

                }
                int binid = thishist.FindBin( ieta, iphi);
                thishist.SetBinContent( binid, ch_sum );
            }
            adc_depth_highadc_outbx_list.push_back( thishist);
        }
        else {

            for( unsigned ich = 0; ich < nch; ich++ ) {

                int ieta = IN::HBHEDigiIEta->at(ich);
                int iphi = IN::HBHEDigiIPhi->at(ich);
                int depth = IN::HBHEDigiDepth->at(ich);

                if( depth > 1  ) {
                    continue;
                }

                int ch_sum = 0;
                for( unsigned its = 0; its < nts; its++ ) {

                    ch_sum += IN::HBHEDigiADC->at(ich)[its];

                }

                std::pair<int, int> ch_id = std::make_pair( ieta, iphi );
                std::map<std::pair<int,int>, TH1F >::const_iterator bitr = ch_bxadc_map.find( ch_id );

                if( bitr == ch_bxadc_map.end() ) {

                    std::stringstream name;
                    name  << "histbx_" << ieta << "_" << iphi;
                    ch_bxadc_map[ch_id] = TH1F( name.str().c_str(),name.str().c_str(), 100, 0, 1280 ) ;
                }

                ch_bxadc_map[ch_id].Fill( ch_sum );
            }
        }
        _lastLS = IN::ls;
        _lastORN = IN::orbit;
        _lastBX = IN::bx;

    }

}

void RunModule::finalize() {

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

    for( std::map<std::pair<int, int>, TH1F>::const_iterator mitr = ch_bxadc_map.begin(); mitr != ch_bxadc_map.end(); ++mitr ) {

        float val = mitr->second.GetMean();

        int bin = adc_depth_bxadc->FindBin( mitr->first.first, mitr->first.second);

        adc_depth_bxadc->SetBinContent( bin, val );
    }


    _outfile->cd();

    avg_adc_HBHE->Write();
    avg_adc_HF->Write();
    laser_user_word->Write();
    avg_adc_HF_vs_umnqie1->Write();
    avg_adc_HF_vs_umnqie2->Write();
    avg_adc_umnqie1_vs_umnqie2->Write();
    avg_adc_HBHE_vs_umnqie1->Write();
    avg_adc_HBHE_vs_umnqie2->Write();
    adc_umnqie1_vs_umnqie2_laserHBHE->Write();
    adc_umnqie1_vs_umnqie2_laserHF->Write();
    adc_depth_highadc->Write();
    adc_depth_bxadc->Write();
    adc_depth->Write();
    adc_HBHE->Write();
    adc_HF->Write();
    adc_umnqie1->Write();
    adc_umnqie2->Write();
    bx_HF_highadc->Write();
    bx_HBHE_highadc->Write();
    totdiff_HF->Write();
    totdiff_HBHE->Write();

    for( unsigned i = 0; i < adc_depth_highadc_outbx_list.size() ; ++i ) {
        adc_depth_highadc_outbx_list[i].Write();
    }
    for( unsigned i = 0; i < umnqie_highadc_outbx_list.size() ; ++i ) {
        umnqie_highadc_outbx_list[i].Write();
    }

    for( std::map<int, TH1F>::const_iterator itr = orn_ls_run296609_HBHE.begin(); itr != orn_ls_run296609_HBHE.end(); ++itr ) {
        itr->second.Write();
    }
    for( std::map<int, TH1F>::const_iterator itr = orn_ls_run296609_HF.begin(); itr != orn_ls_run296609_HF.end(); ++itr ) {
        itr->second.Write();
    }

    for( std::map<std::pair<unsigned,unsigned>, TH1F>::const_iterator itr = runorn_bx_hists_hbhe.begin(); itr != runorn_bx_hists_hbhe.end(); ++itr ) {
        itr->second.Write();
    }
    for( std::map<std::pair<unsigned,unsigned>, TH1F>::const_iterator itr = runorn_bx_hists_hf.begin(); itr != runorn_bx_hists_hf.end(); ++itr ) {
        itr->second.Write();
    }

}

RunLsOrn::RunLsOrn( int _run, int _ls, int _orn ) {

    run = _run;
    ls = _ls;
    orn = _orn;

}

bool RunLsOrn::operator<( const RunLsOrn &B ) const {

    if( run < B.run ) {
        return true;
    }
    else if( run == B.run ) {
        if( orn <= B.orn ) {
            return true;
        }
        else {
            return false;
        }
    }
    else {
        return false;
    }
}




