#include "include/RunAnalysis.h"

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <string>
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
#include "TProfile.h"

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

    // cd to the file so the histograms show up there
    _f = outfile; 
    _f->cd(); 
    // get the output tree
    _outtree = outtree;


    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );

    _evn = 0;
    int totchhf = 1728;

    int nevt = chain->GetEntries();

    hist_SignalEtaPhiD1  = new TH2F( "SignalEtaPhiD1", "", 90  , -45, 45, 73, 0, 73 );
    hist_SignalEtaPhiD2  = new TH2F( "SignalEtaPhiD2", "", 90  , -45, 45, 73, 0, 73 );
    hist_SignalEtaPhiD3  = new TH2F( "SignalEtaPhiD3", "", 90  , -45, 45, 73, 0, 73 );
    hist_SignalEtaPhiD4  = new TH2F( "SignalEtaPhiD4", "", 90  , -45, 45, 73, 0, 73 );

    hist_MissingEtaPhiD1  = new TH2F( "MissingEtaPhiD1", "", 90  , -45, 45, 73, 0, 73 );
    hist_MissingEtaPhiD2  = new TH2F( "MissingEtaPhiD2", "", 90  , -45, 45, 73, 0, 73 );
    hist_MissingEtaPhiD3  = new TH2F( "MissingEtaPhiD3", "", 90  , -45, 45, 73, 0, 73 );
    hist_MissingEtaPhiD4  = new TH2F( "MissingEtaPhiD4", "", 90  , -45, 45, 73, 0, 73 );

    hist_avgamp_HBP      = new TH1F( "AvgAmp_HBP", "", 256, 0, 1024 );
    hist_avgamp_HBM      = new TH1F( "AvgAmp_HBM", "", 256, 0, 1024 );
    hist_avgamp_HEP      = new TH1F( "AvgAmp_HEP", "", 256, 0, 1024 );
    hist_avgamp_HEM      = new TH1F( "AvgAmp_HEM", "", 256, 0, 1024 );

    hist_chthresh_HBP      = new TH1F( "ChannelThreshold_HBP", "", 512, 0, 512 );
    hist_chthresh_HBM      = new TH1F( "ChannelThreshold_HBM", "", 512, 0, 512 );
    hist_chthresh_HEP      = new TH1F( "ChannelThreshold_HEP", "", 512, 0, 512 );
    hist_chthresh_HEM      = new TH1F( "ChannelThreshold_HEM", "", 512, 0, 512 );

    for( int i = 0 ; i < 512 ; ++i ) {

        channel_counts[i] = std::vector<int>();
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

    _evn++;
    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) {

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
    if( config.GetName() == "RunAnalysis" ) {
        RunAnalysis( config );
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

void RunModule::RunAnalysis( ModuleConfig & config ) {

    int nch_hf = IN::HBHEDigiADC->size();
    int iradch =-1;

    int cut_min = 0;
    int cut_max = 512;

    std::vector<int> channel_integrals;
    for( int ich = 0 ; ich < nch_hf ; ++ich ) {
        int ch_iphi   = IN::HBHEDigiIPhi->at( ich );
        int ch_ieta   = IN::HBHEDigiIEta->at( ich );
        int ch_depth  = IN::HBHEDigiDepth->at( ich );

        HCALChannelMap map( ch_ieta, ch_iphi, ch_depth );

        int nts = IN::HBHEDigiADC->at( ich ).size();
        //std::cout << "qie = " << ich << " channel ieta = " << ch_ieta << " iphi = " << ch_iphi << " depth = " << ch_depth << std::endl;
        
        int sum_ts_adc = 0;
        int sumadc = 0;
        for( int its = 0; its < nts ; ++its ) {
            int adc = IN::HBHEDigiADC->at(ich).at(its);
            //std::cout << "\tTS" << its << " ADC = " << adc << std::endl;
            sumadc += adc;
            sum_ts_adc += (its+1)*adc;
        }

        if( sumadc < 100 ) {
            if( ch_depth == 1 ) {
                hist_MissingEtaPhiD1->Fill( map.GetIEta(), map.GetIPhi());
            }
            if( ch_depth == 2 ) {
                hist_MissingEtaPhiD2->Fill( map.GetIEta(), map.GetIPhi());
            }
            if( ch_depth == 3 ) {
                hist_MissingEtaPhiD3->Fill( map.GetIEta(), map.GetIPhi());
            }
            if( ch_depth == 4 ) {
                hist_MissingEtaPhiD4->Fill( map.GetIEta(), map.GetIPhi());
            }
        }

        channel_integrals.push_back( sumadc );


        std::vector<HCALChannelMap>::iterator channel = std::find( channels.begin(), channels.end(), map );
        if( channel == channels.end() ) {
            map.AddValue( sumadc );
            channels.push_back( map) ;
        }
        else {
            channel->AddValue( sumadc );
        }
    }
    for( int i = 0; i < 512 ; ++ i ) {
        int npass = 0;
        for( int ich = 0 ; ich < channel_integrals.size() ; ++ich ) {
            if( channel_integrals[ich] > i ) {
                npass ++ ;
            }

        }
        channel_counts[i].push_back( npass );
    }

}

void RunModule::finalize(  ) {

    for( unsigned i = 0; i < channels.size(); ++i ) {
        HCALChannelMap channel = channels[i];

        std::string subdet = channel.GetSubDet();

        if( channel.GetDepth()  == 1 ) {
            hist_SignalEtaPhiD1->SetBinContent( hist_SignalEtaPhiD1->FindBin(channel.GetIEta(), channel.GetIPhi()), channel.GetAvgValue() );
        }
        if( channel.GetDepth()  == 2 ) {
            hist_SignalEtaPhiD2->SetBinContent( hist_SignalEtaPhiD2->FindBin(channel.GetIEta(), channel.GetIPhi()), channel.GetAvgValue() );
        }
        if( channel.GetDepth()  == 3 ) {
            hist_SignalEtaPhiD3->SetBinContent( hist_SignalEtaPhiD3->FindBin(channel.GetIEta(), channel.GetIPhi()), channel.GetAvgValue() );
        }
        if( channel.GetDepth()  == 4 ) {
            hist_SignalEtaPhiD4->SetBinContent( hist_SignalEtaPhiD4->FindBin(channel.GetIEta(), channel.GetIPhi()), channel.GetAvgValue() );
        }

        if( subdet == "HBP" ) {
            hist_avgamp_HBP->Fill( channel.GetAvgValue() );
        }
        if( subdet == "HBM" ) {
            hist_avgamp_HBM->Fill( channel.GetAvgValue() );
        }
        if( subdet == "HEP" ) {
            hist_avgamp_HEP->Fill( channel.GetAvgValue() );
        }
        if( subdet == "HEM" ) {
            hist_avgamp_HEM->Fill( channel.GetAvgValue() );
        }
        
    }

    for( int i = 0; i < 512 ; ++ i ) {
        int sum = 0;
        for( int v = 0; v < channel_counts[i].size() ; ++v ) {
            sum += channel_counts[i][v];
        }

        hist_chthresh_HBP->SetBinContent( i+1, float( sum ) / channel_counts[i].size() );
    }



    _f->cd();

    hist_SignalEtaPhiD1->Write();
    hist_SignalEtaPhiD2->Write();
    hist_SignalEtaPhiD3->Write();
    hist_SignalEtaPhiD4->Write();

    hist_MissingEtaPhiD1->Write();
    hist_MissingEtaPhiD2->Write();
    hist_MissingEtaPhiD3->Write();
    hist_MissingEtaPhiD4->Write();

    hist_avgamp_HBP->Write();
    hist_avgamp_HBM->Write();
    hist_avgamp_HEP->Write();
    hist_avgamp_HEM->Write();

    hist_chthresh_HBP->Write();

}

HCALChannelMap::HCALChannelMap( int _ieta, int _iphi, int _depth ) {

    ieta = _ieta;
    iphi = _iphi;
    depth = _depth;

    nvals = 0;
    avgvals = 0;

}

int HCALChannelMap::GetIEta() const {
    return ieta;
}
int HCALChannelMap::GetIPhi() const {
    return iphi;
}
int HCALChannelMap::GetDepth() const {
    return depth;
}

std::string HCALChannelMap::GetSubDet() const { 

    if( ieta < 0 ) {
        if( ieta >= -16 && depth == 1 ) {
            return "HBM";
        }
        else if( (ieta == -15 || ieta == -16) && depth == 2 ) {
            return "HBM";
        }
        else {
            return "HEM";
        }
    }
    else {
        if( ieta <= -16 && depth == 1 ) {
            return "HBP";
        }
        else if( (ieta == 15 || ieta == 16) && depth == 2 ) {
            return "HBP";
        }
        else {
            return "HEP";
        }
    }
}



void HCALChannelMap::AddValue(int adc) {

    nvals++;

    avgvals = ( avgvals*( nvals-1 ) + adc )/ nvals;


}

float HCALChannelMap::GetAvgValue( ) const {

    return avgvals;

}


void HCALChannelMap::Print() {
    std::cout << "channel ieta = " << ieta << " iphi = " << iphi << " depth = " << depth << std::endl;
}

bool HCALChannelMap::operator==( const HCALChannelMap &comp ) const {

    return  ( (ieta == comp.GetIEta()) && ( iphi == comp.GetIPhi() ) && ( depth == comp.GetDepth() ) );

}

std::string HCALChannelMap::GetIDString() const {
    
    std::ostringstream id;
    id << ieta << "_" << iphi << "_" << depth; 

    return id.str();
}


    


