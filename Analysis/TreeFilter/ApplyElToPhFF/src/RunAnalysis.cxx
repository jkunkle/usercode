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

void RunModule::initialize( TChain * chain, TTree * _outtree, TFile *outfile,
                            const CmdOptions & _options, std::vector<ModuleConfig> & configs ) {

    // store tree for local use
    outtree = _outtree;
    options = _options;
    rfile = 0;
    rhist_norm = 0;
    rhist_pt   = 0;
    rhist_eta  = 0;
    rhist_pteta  = 0;
    rand = new TRandom3();
    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    outtree->Branch("EventWeight"      , &OUT::EventWeight      , "EventWeight/F" );
    outtree->Branch("HasElToPhFF"      , &OUT::HasElToPhFF      , "HasElToPhFF/O" );

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        if( mod_conf.GetName() == "AddEventWeight" ) {

            std::map<std::string, std::string> data = mod_conf.GetInitData();

            std::string root_file;
            std::string hist_name_norm;
            std::string hist_name_pt;
            std::string hist_name_eta;
            std::string nconv;

            if( data.find( "root_file" ) != data.end() ) {
                std::string root_file = data["root_file"];
                rfile = TFile::Open( root_file.c_str() );
            }
            else {
                std::cout << "RunModule::AddEventWeight : ERROR - No root file was provided" << std::endl;
                return;
            }
            if( data.find( "hist_name_norm" ) != data.end() ) {
                rhist_norm = dynamic_cast<TH1F*>(rfile->Get(data["hist_name_norm"].c_str()));
            }
            if( data.find( "hist_name_pt" ) != data.end() ) {
                rhist_pt = dynamic_cast<TH1F*>(rfile->Get(data["hist_name_pt"].c_str()));
            }
            if( data.find( "hist_name_eta" ) != data.end() ) {
                rhist_eta = dynamic_cast<TH1F*>(rfile->Get(data["hist_name_eta"].c_str()));
            }
            if( data.find( "hist_name_pteta" ) != data.end() ) {
                rhist_pteta = dynamic_cast<TH2F*>(rfile->Get(data["hist_name_pteta"].c_str()));
            }
            if( data.find( "sample_key" ) != data.end() ) {
                sample_key = data["sample_key"];
            }
            if( data.find( "nconv" ) != data.end() ) {
                nconv = data[ "nconv" ];
            }
        }
    }

}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    // Don't do this here
    //CopyInputVarsToOutput();

    // loop over configured modules
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {

        if( mod_conf.GetName() == "AddEventWeight" ) {
            AddEventWeight( mod_conf );
        }
    }

    // always return false.  Handle the tree filling locally
    return false;

}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//
bool RunModule::AddEventWeight( ModuleConfig & config) {

    OUT::EventWeight = 1.0;
    OUT::HasElToPhFF = false;

    //if( options.sample.empty() ) return true; 
    //// if the string is not empty, then try to match
    //    
    //// if no match, then return, otherwise get the histo
    //if( options.sample.find( sample_key ) == std::string::npos ) {
    //    return true;
    //}

    // Require two electrons
    if( !config.PassInt( "cut_elPt25_n", IN::el_passtrig_n ) ) return false;
    if( !config.PassInt( "cut_elpasstrig_n", IN::el_pt25_n ) ) return false;
    if( !config.PassInt( "cut_el_n", IN::el_n ) ) return false;

    std::vector<float> scale_factors;
    // loop over each electron
    // for each electron, create a new event
    // treating this electron as a photon

    // we need two electrons
    if( IN::el_n != 2 ) return false;

    // figure out which electrons are trigger matched
    // if both electons are trigger matched, then they
    // are each unbiased and both should be added as
    // a photon.  If only one is trigger matched, that
    // electron is biased and should not be used
    
    int n_el_biased = 0;
    std::vector<int> el_biased_idx;
    for( int i = 0; i < IN::el_n; ++i ) {
        bool is_unbiased = false;
        if( !config.PassFloat( "cut_el_biased_pt", IN::el_pt->at(i) ) ) is_unbiased = true;
        if( !config.PassBool( "cut_el_biased_triggerMatch", IN::el_triggerMatch->at(i) ) ) is_unbiased = true;
        if( !config.PassBool( "cut_el_biased_passMvaTrig", IN::el_passMvaTrig->at(i) ) ) is_unbiased = true;

        if( !is_unbiased ) {
            n_el_biased++;
            el_biased_idx.push_back(i);
        }

    }

    float rnddbl = rand->Rndm();
    int skip = 1;
    if( rnddbl < 0.5 ) {
        skip = 0;
    }
    
    for( int i = 0; i < IN::el_n; ++i ) {

        if( i == skip ) continue;

        float pt  = IN::el_pt ->at(i);
        float eta = IN::el_eta->at(i);

        // make the photon eta cut
        // PUT THIS BACK IN
        //if( fabs(eta) > 1.479 && fabs(eta) < 1.566 ) continue;

        //// if only one electron is unbiased and this
        //// electron is not in the unbiased list, don't make it
        //// into a photon
        //if( n_el_biased == 1 ) {
        //  
        //    if( std::find( el_biased_idx.begin(), el_biased_idx.end(), i ) != el_biased_idx.end() ) {
        //        continue;
        //    }

        //}

        // copy the event
        CopyInputVarsToOutput();

        float sf = 1.0;

        if( rhist_norm ) sf *= rhist_norm->GetBinContent( 1 );
        if( rhist_pt   ) sf *= rhist_pt  ->GetBinContent( rhist_pt ->FindBin( pt  ) );
        if( rhist_eta  ) sf *= rhist_eta ->GetBinContent( rhist_eta->FindBin( eta ) );
        if( rhist_pteta) sf *= rhist_pteta->GetBinContent( rhist_pteta->FindBin( eta, pt ) );

        OUT::EventWeight = sf;
        OUT::HasElToPhFF = true;

        // we need to erase an electron, start by clearing all electron branches
        ClearOutputPrefix( "el_" );
        OUT::el_n=0;

        // find the second electron
        for( int eli = 0; eli < IN::el_n; eli++ ) {
            if( eli == i ) continue;
            // this is the electron that we count as an electron
            // copy these inputs to the output
            CopyPrefixIndexBranchesInToOut( "el_", eli );
            OUT::el_n++;
        }

        // now push back photon variables using this electron
        // don't clear current photons because we want to preserve those
        // not all photon information will be filled
        // However we should push back default variables
        // in all photon branches so that the vector sizes are consistent
        OUT::ph_pt->push_back( IN::el_pt->at(i) );
        OUT::ph_eta->push_back( IN::el_eta->at(i) );
        OUT::ph_phi->push_back( IN::el_phi->at(i) );
        OUT::ph_e->push_back( IN::el_e->at(i) );
        OUT::ph_n++;
        if( nconv == "0" ) {
            OUT::ph_conv_nTrk->push_back(0);
        }
        if( nconv == "2" ) {
            OUT::ph_conv_nTrk->push_back(2);
        }
        OUT::ph_passMedium->push_back(1);
        OUT::ph_eleVeto->push_back(1);

        // recalculate event kinematics counting the electron as a photon
        // reset all of them first
        OUT::el_pt25_n=0;
        OUT::mu_pt25_n=0;
        OUT::leadPhot_pt=0;
        OUT::sublPhot_pt=0;
        OUT::leadPhot_lepDR=0;
        OUT::sublPhot_lepDR=0;
        OUT::ph_phDR=0;
        OUT::phPhot_lepDR=0;
        OUT::leadPhot_lepDPhi=0;
        OUT::sublPhot_lepDPhi=0;
        OUT::ph_phDPhi=0;
        OUT::phPhot_lepDPhi=0;
        OUT::dphi_met_lep1    = 0;
        OUT::dphi_met_lep2    = 0;
        OUT::dphi_met_ph1     = 0;
        OUT::dphi_met_ph2     = 0;
        OUT::mt_lep_met=0;
        OUT::mt_lepph1_met=0;
        OUT::mt_lepph2_met=0;
        OUT::mt_lepphph_met=0;
        OUT::m_leplep=0;
        OUT::m_lepph1=0;
        OUT::m_lepph2=0;
        OUT::m_lepphph=0;
        OUT::m_leplepph=0;
        OUT::m_phph=0;
        OUT::m_leplepZ=0;
        OUT::m_3lep=0;
        OUT::m_4lep=0;
        OUT::pt_phph=0;
        OUT::pt_leplep=0;
        OUT::pt_lepph1=0;
        OUT::pt_lepph2=0;
        OUT::pt_lepphph=0;
        OUT::pt_leplepph=0;
        OUT::pt_secondLepton=0;
        OUT::pt_thirdLepton=0;

        OUT::el_passtrig_n=1;

        std::vector<TLorentzVector> leptons;
        std::vector<std::pair<float, std::pair<bool, int > > > sorted_leptons;
        for( int idx = 0; idx < OUT::el_n; idx++ ) {

            TLorentzVector lv;
            lv.SetPtEtaPhiE(  OUT::el_pt->at(idx),
                              OUT::el_eta->at(idx),
                              OUT::el_phi->at(idx),
                              OUT::el_e->at(idx)
                            );
            leptons.push_back(lv);
            sorted_leptons.push_back( std::make_pair( lv.Pt(), std::make_pair( 0, idx ) ) );
            if( lv.Pt() > 25 ) {
                OUT::el_pt25_n++;
            }
        }

        for( int idx = 0; idx < OUT::mu_n; idx++ ) {

            TLorentzVector lv;
            lv.SetPtEtaPhiE(  OUT::mu_pt->at(idx),
                              OUT::mu_eta->at(idx),
                              OUT::mu_phi->at(idx),
                              OUT::mu_e->at(idx)
                            );
            leptons.push_back(lv);
            sorted_leptons.push_back( std::make_pair( lv.Pt(), std::make_pair( 0, idx ) ) );
            if( lv.Pt() > 25 ) {
                OUT::mu_pt25_n++;
            }
        }

        std::vector<TLorentzVector> photons;
        std::vector<std::pair<float, int> > sorted_photons;
        for( int idx = 0; idx < OUT::ph_n; ++idx ) {
            TLorentzVector phot;
            phot.SetPtEtaPhiE(  OUT::ph_pt->at(idx), 
                                OUT::ph_eta->at(idx),
                                OUT::ph_phi->at(idx),
                                OUT::ph_e->at(idx)
                            );
            photons.push_back(phot);
            sorted_photons.push_back(std::make_pair( phot.Pt(), idx ));
        }

        std::sort(sorted_photons.rbegin(), sorted_photons.rend());
        std::sort(sorted_leptons.rbegin(), sorted_leptons.rend());

        TLorentzVector metlv;
        metlv.SetPtEtaPhiM( OUT::pfMET, 0.0, OUT::pfMETPhi, 0.0 );

        if( photons.size() > 1 ) { 
            OUT::leadPhot_pt = sorted_photons[0].first;
            OUT::sublPhot_pt = sorted_photons[1].first;

            int leadidx = sorted_photons[0].second;
            int sublidx = sorted_photons[1].second;

            OUT::dphi_met_ph1 = photons[leadidx].DeltaPhi( metlv );
            OUT::dphi_met_ph2 = photons[sublidx].DeltaPhi( metlv );

            OUT::m_phph = ( photons[leadidx] + photons[sublidx] ).M();
            OUT::pt_phph = ( photons[leadidx] + photons[sublidx] ).Pt();
        }
        else if ( photons.size() == 1 ) {
            OUT::leadPhot_pt = sorted_photons[0].first;
            OUT::sublPhot_pt = 0;
            OUT::dphi_met_ph1 = photons[sorted_photons[0].second].DeltaPhi( metlv );
            OUT::dphi_met_ph2 = -99; 
        }

        if( leptons.size() == 2 ) {
            OUT::pt_secondLepton = sorted_leptons[1].first;
        }
        if( leptons.size() == 3 ) {
            OUT::pt_thirdLepton = sorted_leptons[2].first;
        }

        if( leptons.size() > 1 ) {
            OUT::m_leplep = ( leptons[0] + leptons[1] ).M();
            OUT::pt_leplep = ( leptons[0] + leptons[1] ).Pt();

            OUT::dphi_met_lep1 = leptons[0].DeltaPhi( metlv );
            OUT::dphi_met_lep2 = leptons[1].DeltaPhi( metlv );

            if( photons.size() > 0 ) { 
                OUT::m_leplepph  = (leptons[0] + leptons[1] + photons[0] ).M();
                OUT::pt_leplepph  = (leptons[0] + leptons[1] + photons[0] ).Pt();
            }
        }

        if( leptons.size() == 1 ) {
           
            OUT::dphi_met_lep1 = leptons[0].DeltaPhi( metlv );
            OUT::mt_lep_met = Utils::calc_mt( leptons[0], metlv );

            if( photons.size() > 1 ) { 

                int leadidx = sorted_photons[0].second;
                int sublidx = sorted_photons[1].second;

                OUT::leadPhot_lepDR = photons[leadidx].DeltaR(leptons[0]);
                OUT::sublPhot_lepDR = photons[sublidx].DeltaR(leptons[0]);
                OUT::ph_phDR    = photons[leadidx].DeltaR(photons[sublidx]);
                OUT::phPhot_lepDR = (photons[leadidx]+photons[sublidx]).DeltaR(photons[sublidx]);
                
                OUT::leadPhot_lepDPhi = photons[leadidx].DeltaPhi(leptons[0]);
                OUT::sublPhot_lepDPhi = photons[sublidx].DeltaPhi(leptons[0]);
                OUT::ph_phDPhi    = photons[leadidx].DeltaPhi(photons[sublidx]);
                OUT::phPhot_lepDPhi = (photons[leadidx]+photons[sublidx]).DeltaPhi(photons[sublidx]);
                
                OUT::mt_lepph1_met = Utils::calc_mt( leptons[0] + photons[leadidx], metlv );
                OUT::mt_lepph2_met = Utils::calc_mt( leptons[0] + photons[sublidx], metlv );

                OUT::mt_lepphph_met = Utils::calc_mt( leptons[0] + photons[leadidx] + photons[sublidx], metlv );

                OUT::m_lepph1 = ( leptons[0] + photons[leadidx] ).M();
                OUT::m_lepph2 = ( leptons[0] + photons[sublidx] ).M();
                OUT::m_lepphph = ( leptons[0] + photons[leadidx] + photons[sublidx] ).M();

                OUT::pt_lepph1 = ( leptons[0] + photons[leadidx] ).Pt();
                OUT::pt_lepph2 = ( leptons[0] + photons[sublidx] ).Pt();
                OUT::pt_lepphph = ( leptons[0] + photons[leadidx] + photons[sublidx] ).Pt();
            }
            else if( photons.size() == 1 ) {

                int leadidx = sorted_photons[0].second;
                OUT::leadPhot_lepDPhi = photons[leadidx].DeltaPhi(leptons[0]);
                OUT::leadPhot_lepDR   = photons[leadidx].DeltaR(leptons[0]);

                OUT::mt_lepph1_met = Utils::calc_mt( leptons[0] + photons[leadidx], metlv );

                OUT::m_lepph1 = ( leptons[0] + photons[leadidx] ).M();
                OUT::pt_lepph1 = ( leptons[0] + photons[leadidx] ).Pt();

            }
                
                
        }
        if( leptons.size() > 2 ) {
            std::vector< std::pair<float, float> > lep_pair_masses;
            for( unsigned i = 0; i < leptons.size() ; i++ ) {
                for( unsigned j = i+1; j < leptons.size() ; j++ ) {
                    lep_pair_masses.push_back( std::make_pair( fabs(91.1876 - (leptons[i]+leptons[j]).M() ),(leptons[i]+leptons[j]).M())  );
                }
           }
            //sort from smallest to greatest
            std::sort( lep_pair_masses.begin(), lep_pair_masses.end() );

            OUT::m_leplepZ = lep_pair_masses[0].second;
        }
        if( leptons.size() == 3 ) {
            OUT::m_3lep = ( leptons[0] + leptons[1] + leptons[2] ).M();
        }

        if( leptons.size() == 4 ) {
            OUT::m_4lep = ( leptons[0] + leptons[1] + leptons[2] + leptons[3] ).M();
        }

        outtree->Fill();
    }

    return true;
}


void RunModule::finalize() {

    if( rfile && rfile->IsOpen() ) {
        rfile->Close();
    }

}
