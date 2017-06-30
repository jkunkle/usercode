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

    

    hist_LETDCvsEvt_qieA   = new TH1F( "LETDCvsEvt_qieA" , "", nevt, 0,  nevt );
    hist_LETDCvsEvt_qieB   = new TH1F( "LETDCvsEvt_qieB" , "", nevt, 0,  nevt );
    hist_HFIntADCvsEvt     = new TH2F( "HFIntADCvsEvt"   , "", totchhf, 0, totchhf, 100, 0, 1024 );
    hist_HFSignalEtaPhiD1  = new TH2F( "HFSignalEtaPhiD1", "", 90  , -45, 45, 73, 0, 73 );
    hist_HFSignalEtaPhiD2  = new TH2F( "HFSignalEtaPhiD2", "", 90  , -45, 45, 73, 0, 73 );
    hist_qie10TDC           = new TH1F( "qie10tdc" , "", 64, 0, 64);

    for( int i = 0; i < 10 ; ++i ) {
        std::stringstream name;
        name << "Shape" << i;
        qie10_signals.push_back( new TH1F( name.str().c_str(), "", 10, 0, 10 ) );
    }



    
    //// *************************
    //// Examples :
    //OUT::ph_n              = 0;
    //OUT::ph_pt             = 0;
    //OUT::ph_eta            = 0;
    //OUT::ph_phi            = 0;
    //OUT::ph_e              = 0;

    //// *************************
    //// Declare Branches
    //// *************************

    //// Examples :
    //outtree->Branch("ph_n"             , &OUT::ph_n                                      );
    //outtree->Branch("ph_pt"            , &OUT::ph_pt                                     );
    //outtree->Branch("ph_eta"           , &OUT::ph_eta                                    );
    //outtree->Branch("ph_phi"           , &OUT::ph_phi                                    );
    //outtree->Branch("ph_e"             , &OUT::ph_e                                      );
    //outtree->Branch("ph_sigmaIEIE"     , &OUT::ph_sigmaIEIE                              );

    std::vector<std::string> eta_tok;
    std::vector<std::string> phi_tok;
    std::vector<std::string> depth_tok;

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        if( mod_conf.GetName() == "RunAnalysis" ) {
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "raddam_eta" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string etas = eitr->second;
                eta_tok = Tokenize(etas , "," );
            }
            eitr = mod_conf.GetInitData().find( "raddam_phi" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string phis = eitr->second;
                phi_tok = Tokenize(phis, "," );
            }
            eitr = mod_conf.GetInitData().find( "raddam_depth" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string depths = eitr->second;
                depth_tok = Tokenize(depths, "," );
            }
        }
    }

    for( unsigned ich = 0; ich < eta_tok.size(); ++ich ) {

        HFChannelMap map( atoi( eta_tok[ich].c_str() ), atoi( phi_tok[ich].c_str()), atoi( depth_tok[ich].c_str( ) ) );

        std::cout << "RADDAM CHANNEL" << std::endl;
        map.Print();

        _raddam_channels.push_back( map);

    }

    int nraddam = _raddam_channels.size();

    std::cout << "RADDAM SIZE " << nraddam << std::endl;

    hist_HFTiming = new TH2F( "HFTiming" , "", nevt, 0, nevt, nraddam, 0, nraddam);


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

#ifdef EXISTS_HFDigiADC
    int nch_hf = IN::HFDigiADC->size();
    int iradch =-1;

    for( int ich = 0 ; ich < nch_hf ; ++ich ) {
        int ch_iphi   = IN::HFDigiIPhi->at( ich );
        int ch_ieta   = IN::HFDigiIEta->at( ich );
        int ch_depth  = IN::HFDigiDepth->at( ich );

        int nts = IN::HFDigiADC->at( ich ).size();
        //std::cout << "qie = " << ich << " channel ieta = " << ch_ieta << " iphi = " << ch_iphi << " depth = " << ch_depth << std::endl;
        
        HFChannelMap map( ch_ieta, ch_iphi, ch_depth );

        if( _evn == 0 ) {
            //map.Print();
            _hf_channel_map.push_back( std::make_pair<int, HFChannelMap> ( ich, map ) );
        }

        if( std::find( _raddam_channels.begin(), _raddam_channels.end(), map ) == _raddam_channels.end() ) {
            continue;
        }

        iradch++;

        int sum_ts_adc = 0;
        int sumadc = 0;
        for( int its = 0; its < nts ; ++its ) {
            int adc = IN::HFDigiADC->at(ich).at(its);
            //std::cout << "\tTS" << its << " ADC = " << adc << std::endl;
            sumadc += adc;
            sum_ts_adc += (its+1)*adc;
        }
        hist_HFIntADCvsEvt->Fill( ich, sumadc );


        hist_HFTiming->SetBinContent( hist_HFTiming->FindBin(_evn, iradch), sum_ts_adc/float(sumadc) );
    }
#endif

    int nch = IN::QIE10DigiCapID->size();

    for( int ich = 0 ; ich < nch ; ++ich ) {

        int ch_iphi   = IN::QIE10DigiIPhi->at( ich );
        int ch_ieta   = IN::QIE10DigiIPhi->at( ich );
        int ch_depth  = IN::QIE10DigiDepth->at( ich );

        int nts = IN::QIE10DigiCapID->at( ich ).size();

        //std::cout << "qie = " << ich << " channel ieta = " << ch_ieta << " iphi = " << ch_iphi << " depth = " << ch_depth << std::endl;
        bool found_pulse = false;
        int tdc_unfold = 0;
        for( int its = 0; its < nts ; ++its ) {

            int adc = IN::QIE10DigiADC->at(ich).at(its);
            int tdc = IN::QIE10DigiLETDC->at(ich).at(its);

            if( ich == 1 && (_evn < qie10_signals.size()) ) {
                qie10_signals[_evn]->SetBinContent( its+1, adc );
            }

            hist_qie10TDC->Fill( tdc );

            if( tdc < 63 and !found_pulse ) {
                found_pulse = true;
                tdc_unfold = its*50 + tdc;
            }


            //std::cout << "\tTS" << its << " TDC = " << tdc << " ADC = " << adc << " tdc_unfold = " << tdc_unfold << std::endl;
            if( ich == 0 ) {
                hist_LETDCvsEvt_qieA->SetBinContent( _evn+1, tdc_unfold );
            }
            if( ich == 1 ) {
                hist_LETDCvsEvt_qieB->SetBinContent( _evn+1, tdc_unfold );
            }
        }
    }
}

void RunModule::finalize(  ) {

    TProfile *prof = hist_HFIntADCvsEvt->ProfileX( "px" );
    for( unsigned imap = 0; imap < _hf_channel_map.size() ; ++imap ) {

        HFChannelMap map = _hf_channel_map[imap].second;
        int ichan = _hf_channel_map[imap].first;

        int val = prof->GetBinContent( ichan+1 );

        if( map.GetDepth()  == 1 ) {

            int ieta = map.GetIEta();
            int ieta_mod;
            if( ieta > 0 ) {
                ieta_mod = ieta - 15;
            }
            else {
                ieta_mod = ieta + 15;
            }
            ieta_mod = ieta;
            hist_HFSignalEtaPhiD1->SetBinContent( hist_HFSignalEtaPhiD1->FindBin(ieta_mod, map.GetIPhi()), val );
        }
        if( map.GetDepth()  == 2 ) {
            //hist_HFSignalEtaPhiD1->SetBinContent( hist_HFSignalEtaPhiD1->FindBin(map.GetIEta(), map.GetIPhi()), prof->GetBinContent( imap+1 ) );
            hist_HFSignalEtaPhiD2->SetBinContent( hist_HFSignalEtaPhiD2->FindBin(map.GetIEta(), map.GetIPhi()), val );
        }
    }


    hist_LETDCvsEvt_qieA->Write();
    hist_LETDCvsEvt_qieB->Write();
    hist_HFIntADCvsEvt->Write();
    hist_HFSignalEtaPhiD1->Write();
    hist_HFSignalEtaPhiD2->Write();
    hist_HFTiming->Write();
    hist_qie10TDC->Write();
    for( unsigned i = 0 ; i < qie10_signals.size(); ++i ) {
        qie10_signals[i]->Write();
    }

}

HFChannelMap::HFChannelMap( int _ieta, int _iphi, int _depth ) {

    ieta = _ieta;
    iphi = _iphi;
    depth = _depth;

}

int HFChannelMap::GetIEta() const {
    return ieta;
}
int HFChannelMap::GetIPhi() const {
    return iphi;
}
int HFChannelMap::GetDepth() const {
    return depth;
}

void HFChannelMap::Print() {
    std::cout << "channel ieta = " << ieta << " iphi = " << iphi << " depth = " << depth << std::endl;
}

bool HFChannelMap::operator==( const HFChannelMap &comp ) const {

    return  ( (ieta == comp.GetIEta()) && ( iphi == comp.GetIPhi() ) && ( depth == comp.GetDepth() ) );

}

std::string HFChannelMap::GetIDString() const {
    
    std::ostringstream id;
    id << ieta << "_" << iphi << "_" << depth; 

    return id.str();
}


    


