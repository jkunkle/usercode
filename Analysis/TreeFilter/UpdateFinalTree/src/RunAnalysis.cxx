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
                            const CmdOptions & _options, std::vector<ModuleConfig> & config ) {
    
    // *************************
    // initialize random numbers
    // *************************
    rand = new TRandom3();
    rand->SetSeed();
       
    
    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Set defaults for added output variables
    // *************************
    // Examples :

    // *************************
    // Declare Branches
    // *************************

    //outtree->Branch("mu_pt25_n"        , &OUT::mu_pt25_n        , "mu_pt25_n/I"   );
    //outtree->Branch("el_pt25_n"        , &OUT::el_pt25_n        , "el_pt25_n/I"   );
    //outtree->Branch("EventWeight"      , &OUT::EventWeight      , "EventWeight/F" );
    //outtree->Branch("HasElToPhFF"      , &OUT::HasElToPhFF      , "HasElToPhFF/O" );

    //outtree->Branch("m_1nearestToZ"   , &OUT::m_1nearestToZ   , "m_1nearestToZ/F"     );
    //outtree->Branch("m_2nearestToZ"   , &OUT::m_2nearestToZ   , "m_2nearestToZ/F"     );
    //outtree->Branch("m_3nearestToZ"   , &OUT::m_3nearestToZ   , "m_3nearestToZ/F"     );
    //outtree->Branch("m_4nearestToZ"   , &OUT::m_4nearestToZ   , "m_4nearestToZ/F"     );
    outtree->Branch("leadPhot_leadLepDR", &OUT::leadPhot_leadLepDR, "leadPhot_leadLepDR/F"  );
    outtree->Branch("leadPhot_sublLepDR", &OUT::leadPhot_sublLepDR, "leadPhot_sublLepDR/F"  );
    outtree->Branch("sublPhot_leadLepDR", &OUT::sublPhot_leadLepDR, "sublPhot_leadLepDR/F"  );
    outtree->Branch("sublPhot_sublLepDR", &OUT::sublPhot_sublLepDR, "sublPhot_sublLepDR/F"  );

    options = _options;

}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    CopyInputVarsToOutput();

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        save_event &= ApplyModule( mod_conf, options );
    }

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config, const CmdOptions & options) {

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
    // If the module applies a filter the filter decision
    // is passed back to here.  There is no requirement
    // that a function returns a bool, but
    // if you want the filter to work you need to do this
    //
    // Example :
    if( config.GetName() == "CalcEventVars" ) {
        CalcEventVars( config );
    }
    if( config.GetName() == "AddEventWeight" ) {
        keep_evt &= AddEventWeight( config, options );
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

bool RunModule::AddEventWeight( ModuleConfig & config, const CmdOptions & options ) {

    OUT::EventWeight = 1.0;
    OUT::HasElToPhFF = false;

    std::map<std::string, std::string> data = config.GetInitData();

    std::string root_file;
    std::string hist_name;
    std::string sample_key;

    if( data.find( "root_file" ) != data.end() ) {
        root_file = data["root_file"];
    }
    else {
        std::cout << "RunModule::AddEventWeight : ERROR - No root file was provided" << std::endl;
        return true;
    }
    if( data.find( "hist_name" ) != data.end() ) {
        hist_name = data["hist_name"];
    }
    else {
        std::cout << "RunModule::AddEventWeight : ERROR - No histogram name was provided" << std::endl;
        return true;
    }
    if( data.find( "sample_key" ) != data.end() ) {
        sample_key = data["sample_key"];
    }
    else {
        return true;
    }

    if( !options.sample.empty() ) { // if the string is not empty, then try to match
        
        // if no match, then return, otherwise get the histo
        if( options.sample.find( sample_key ) == std::string::npos ) {
            return true;
        }

        // check if the file has already been opened.  If not, open it and get the histogram
        if( rfile == 0 ) {

            rfile = TFile::Open( root_file.c_str() );
            rhist = dynamic_cast<TH1F*>(rfile->Get( hist_name.c_str() ) );
            //rfile->Close();
            //rfile=0;

        }

        // Require two electrons
        if( OUT::el_pt25_n != 2 ) return false;

        std::vector<float> scale_factors;
        for( int i = 0; i < OUT::el_n; ++i ) {
            float pt = OUT::el_pt->at(i);

            if( pt > 25 ) {
                scale_factors.push_back(rhist->GetBinContent( rhist->FindBin( pt ) ));
            }
        }

        //float evt_sf = 1.0;
        //int keep_evt = true;
        //while( 1 ) {
        //    // draw two random numbers, one for each scale factor
        //    bool pass0 = false;
        //    bool pass1 = false;

        //    float randdbl0 = rand->Rndm();
        //    float randdbl1 = rand->Rndm();
        //   
        //    //std::cout << "sf0 = " << scale_factors[0] << " rand0 = " << randdbl0 << " sf1 = " << scale_factors[1] << " rand1 = " << randdbl1 << std::endl;

        //    if( randdbl0 < scale_factors[0] ) pass0 = true;
        //    if( randdbl1 < scale_factors[1] ) pass1 = true;

        //    if( pass0 && pass1 ) { 
        //        keep_evt=false;
        //        //std::cout << "Kill ev " << std::endl;
        //        break;
        //    }
        //    else if( pass0 ) {
        //        evt_sf = scale_factors[0];
        //        keep_evt=true;
        //        //std::cout << "SF = " << evt_sf << std::endl;
        //        break;
        //    }
        //    else if( pass1 ) {
        //        evt_sf = scale_factors[1];
        //        keep_evt=true;
        //        //std::cout << "SF = " << evt_sf << std::endl;
        //        break;
        //    }
        //    // if pass neither, draw again
        //}

        //if( !keep_evt ) {
        //    return false;
        //}

        // the probability for either the first or the second electron to fake is
        // determined by constructing the total probability
        // 1 = P(No fake, No fake) + P( one fake ) + P( both fakes )
        // P( one fake ) = 1 - P(No fake, No fake) - P( both fake )
        // P( one fake ) = 1 - ( 1 - sf1 )*(1-sf2) - sf1*sf2
        // P( one fake ) = 1 - ( 1 - sf1 - sf2 + sf1*sf2 ) - sf1*sf2
        // P( one fake ) = sf1 + sf2 -2*sf1*sf2
        //float evt_sf = scale_factors[0] + scale_factors[1] - 2.*scale_factors[0]*scale_factors[1];
        float evt_sf = scale_factors[0] + scale_factors[1];

        OUT::EventWeight *= evt_sf;
        OUT::HasElToPhFF = true;
        // recalculate event kinematics counting a lepton as a photon
        
        TLorentzVector metlv;
        metlv.SetPtEtaPhiM( OUT::pfMET, 0.0, OUT::pfMETPhi, 0.0 );

        std::vector<TLorentzVector> leptons;
        for( int idx = 0; idx < OUT::el_n; idx++ ) {

            TLorentzVector lv;
            lv.SetPtEtaPhiE(  OUT::el_pt->at(idx),
                              OUT::el_eta->at(idx),
                              OUT::el_phi->at(idx),
                              OUT::el_e->at(idx)
                            );
            if( lv.Pt() > 25 ) {
                leptons.push_back(lv);
            }
        }

        for( int idx = 0; idx < OUT::mu_n; idx++ ) {

            TLorentzVector lv;
            lv.SetPtEtaPhiE(  OUT::mu_pt->at(idx),
                              OUT::mu_eta->at(idx),
                              OUT::mu_phi->at(idx),
                              OUT::mu_e->at(idx)
                            );
            if( lv.Pt() > 25 ) {
                leptons.push_back(lv);
            }
        }

        std::vector<TLorentzVector> photons;
        for( int idx = 0; idx < OUT::ph_n; ++idx ) {
            TLorentzVector phot;
            phot.SetPtEtaPhiE(  OUT::ph_pt->at(idx), 
                                OUT::ph_eta->at(idx),
                                OUT::ph_phi->at(idx),
                                OUT::ph_e->at(idx)
                            );
            photons.push_back(phot);
        }

        if( leptons.size() > 2 ) {
                OUT::m_leplepph  = (leptons[0] + leptons[1] + leptons[2] ).M();
                OUT::pt_leplepph  = (leptons[0] + leptons[1] + leptons[2] ).Pt();
        }

        if( leptons.size() == 2 ) {
           
            OUT::mt_lep_met = calc_mt( leptons[0], metlv );

            OUT::mt_lepph1_met = calc_mt( leptons[0] + leptons[1], metlv );

            OUT::m_lepph1 = ( leptons[0] + leptons[1] ).M();

            OUT::pt_lepph1 = ( leptons[0] + leptons[1] ).Pt();

            if( photons.size() > 0 ) {

                OUT::m_lepphph = ( leptons[0]+leptons[1]+photons[0] ).M();
                OUT::mt_lepphph_met = calc_mt( leptons[0] + leptons[1] + photons[0], metlv );

            }
        }
    }

    return true;
}

void RunModule::CalcEventVars( ModuleConfig & config ) const {

    OUT::leadPhot_leadLepDR     = 0;
    OUT::leadPhot_sublLepDR     = 0;
    OUT::sublPhot_leadLepDR     = 0;
    OUT::sublPhot_sublLepDR     = 0;

    std::vector<TLorentzVector> leptons;
    std::vector<std::pair<float, int> > sorted_leptons;
    int lep_idx = 0;
    for( int idx = 0; idx < OUT::el_n; idx++ ) {

        TLorentzVector lv;
        lv.SetPtEtaPhiE(  OUT::el_pt->at(idx),
                          OUT::el_eta->at(idx),
                          OUT::el_phi->at(idx),
                          OUT::el_e->at(idx)
                        );
        sorted_leptons.push_back(std::make_pair( lv.Pt(), lep_idx ) );
        leptons.push_back(lv);
        lep_idx++;
    }

    for( int idx = 0; idx < OUT::mu_n; idx++ ) {

        TLorentzVector lv;
        lv.SetPtEtaPhiE(  OUT::mu_pt->at(idx),
                          OUT::mu_eta->at(idx),
                          OUT::mu_phi->at(idx),
                          OUT::mu_e->at(idx)
                        );

        sorted_leptons.push_back(std::make_pair( lv.Pt(), lep_idx ) );
        leptons.push_back(lv);
        lep_idx++;
    }

    std::vector<TLorentzVector> photons;
    std::vector<std::pair<float, int > > sorted_photons;
    for( int idx = 0; idx < OUT::ph_n; ++idx ) {
        TLorentzVector phot;
        phot.SetPtEtaPhiE(  OUT::ph_pt->at(idx), 
                            OUT::ph_eta->at(idx),
                            OUT::ph_phi->at(idx),
                            OUT::ph_e->at(idx)
                        );
        sorted_photons.push_back(std::make_pair( phot.Pt(), idx ));
        photons.push_back(phot);
    }


    // sort the list of photon momenta in descending order
    std::sort(sorted_photons.rbegin(), sorted_photons.rend());
    std::sort(sorted_leptons.rbegin(), sorted_leptons.rend());

    if( sorted_photons.size() > 0 ) { 
        if( sorted_leptons.size() > 0 ) {
            OUT::leadPhot_leadLepDR = photons[sorted_photons[0].second].DeltaR(leptons[sorted_leptons[0].second]);
            if( sorted_leptons.size() > 1 ) {
                OUT::leadPhot_sublLepDR = photons[sorted_photons[0].second].DeltaR(leptons[sorted_leptons[1].second]);
            }
        }
        if( sorted_photons.size() > 1 ) {
            if( sorted_leptons.size() > 0 ) {
                OUT::sublPhot_leadLepDR = photons[sorted_photons[1].second].DeltaR(leptons[sorted_leptons[0].second]);
                if( sorted_leptons.size() > 1 ) {
                    OUT::leadPhot_sublLepDR = photons[sorted_photons[1].second].DeltaR(leptons[sorted_leptons[1].second]);
                }
            }
        }
    }

}


RunModule::RunModule() :
    rfile(0),
    rhist(0),
    rand(0)
{
}
