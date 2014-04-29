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


    CmdOptions options = ParseOptions( argc, argv );

    // Parse the text file and form the configuration object
    AnaConfig ana_config = ParseConfig( options.config_file, options );

    std::cout << "Configured " << ana_config.size() << " analysis modules " << std::endl;

    RunModule runmod;
    ana_config.Run(runmod, options);

    std::cout << "^_^ Finished ^_^" << std::endl;


}

void RunModule::Run( TChain * chain, TTree * outtree, 
          std::vector<ModuleConfig> & configs, const CmdOptions & options,
          int minevt, int maxevt ) const {

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Declare added output variables
    // *************************
    OUT::lep_pt = 0;
    OUT::lep_eta = 0;
    OUT::lep_phi = 0;
    OUT::lep_e = 0;
    OUT::lep_motherPID = 0;
    OUT::lep_isElec = 0;
    OUT::lep_isMuon = 0;
    OUT::phot_pt = 0;
    OUT::phot_eta = 0;
    OUT::phot_phi = 0;
    OUT::phot_e = 0;
    OUT::phot_motherPID = 0;
    OUT::nu_pt = 0;
    OUT::nu_eta = 0;
    OUT::nu_phi = 0;
    OUT::nu_e = 0;
    OUT::nu_motherPID = 0;
    OUT::w_pt = 0;
    OUT::w_eta = 0;
    OUT::w_phi = 0;
    OUT::w_e = 0;
    
    outtree->Branch("lep_n" , &OUT::lep_n  , "lep_n/I"   );
    outtree->Branch("phot_n", &OUT::phot_n , "phot_n/I" );
    outtree->Branch("nu_n"  , &OUT::nu_n   , "nu_n/I"   );
    outtree->Branch("w_n"   , &OUT::w_n    , "w_n/I"   );

    outtree->Branch("lep_pt"        , &OUT::lep_pt        );
    outtree->Branch("lep_eta"       , &OUT::lep_eta       );
    outtree->Branch("lep_phi"       , &OUT::lep_phi       );
    outtree->Branch("lep_e"         , &OUT::lep_e         );
    outtree->Branch("lep_motherPID" , &OUT::lep_motherPID );
    outtree->Branch("lep_isElec"    , &OUT::lep_isElec    );
    outtree->Branch("lep_isMuon"    , &OUT::lep_isMuon    );
    outtree->Branch("lep_isPos"     , &OUT::lep_isPos    );
    
    outtree->Branch("phot_pt"        , &OUT::phot_pt  );
    outtree->Branch("phot_eta"       , &OUT::phot_eta );
    outtree->Branch("phot_phi"       , &OUT::phot_phi );
    outtree->Branch("phot_e"         , &OUT::phot_e   );
    outtree->Branch("phot_motherPID" , &OUT::phot_motherPID );
    
    outtree->Branch("nu_pt"        , &OUT::nu_pt      );
    outtree->Branch("nu_eta"       , &OUT::nu_eta     );
    outtree->Branch("nu_phi"       , &OUT::nu_phi     );
    outtree->Branch("nu_e"         , &OUT::nu_e       );
    outtree->Branch("nu_motherPID" , &OUT::nu_motherPID );

    outtree->Branch("w_pt"        , &OUT::w_pt      );
    outtree->Branch("w_eta"       , &OUT::w_eta     );
    outtree->Branch("w_phi"       , &OUT::w_phi     );
    outtree->Branch("w_e"         , &OUT::w_e       );
    outtree->Branch("w_isPos"     , &OUT::w_isPos   );

    outtree->Branch("leadPhot_pt" , &OUT::leadPhot_pt , "leadPhot_pt/F" );
    outtree->Branch("sublPhot_pt" , &OUT::sublPhot_pt , "sublPhot_pt/F" );

    outtree->Branch("leadPhot_lepDR" , &OUT::leadPhot_lepDR , "leadPhot_lepDR/F" );
    outtree->Branch("sublPhot_lepDR" , &OUT::sublPhot_lepDR , "sublPhot_lepDR/F" );
    outtree->Branch("phot_photDR"    , &OUT::phot_photDR , "phot_photDR/F" );
    outtree->Branch("photPhot_lepDR" , &OUT::photPhot_lepDR , "photPhot_lepDR/F" );
    outtree->Branch("leadPhot_lepDPhi" , &OUT::leadPhot_lepDPhi , "leadPhot_lepDPhi/F" );
    outtree->Branch("sublPhot_lepDPhi" , &OUT::sublPhot_lepDPhi , "sublPhot_lepDPhi/F" );
    outtree->Branch("phot_photDPhi"    , &OUT::phot_photDPhi , "phot_photDPhi/F" );
    outtree->Branch("photPhot_lepDPhi"    , &OUT::photPhot_lepDPhi , "photPhot_lepDPhi/F" );

    outtree->Branch("mt_lepnu"         , &OUT::mt_lepnu         , "mt_lepnu/F"          );
    outtree->Branch("mt_lepphot1nu"    , &OUT::mt_lepphot1nu    , "mt_lepphot1nu/F"     );
    outtree->Branch("mt_lepphot2nu"    , &OUT::mt_lepphot2nu    , "mt_lepphot2nu/F"     );
    outtree->Branch("mt_lepphotphotnu" , &OUT::mt_lepphotphotnu , "mt_lepphotphotnu/F"  );

    outtree->Branch("m_lepnu"         , &OUT::m_lepnu         , "m_lepnu/F"         );
    outtree->Branch("m_leplep"        , &OUT::m_leplep        , "m_leplep/F"         );
    outtree->Branch("m_lepphot1nu"    , &OUT::m_lepphot1nu    , "m_lepphot1nu/F"    );
    outtree->Branch("m_lepphot2nu"    , &OUT::m_lepphot2nu    , "m_lepphot2nu/F"    );
    outtree->Branch("m_lepphotphotnu" , &OUT::m_lepphotphotnu , "m_lepphotphotnu/F" );
    outtree->Branch("m_lepphot1"      , &OUT::m_lepphot1      , "m_lepphot1/F"      );
    outtree->Branch("m_lepphot2"      , &OUT::m_lepphot2      , "m_lepphot2/F"      );
    outtree->Branch("m_lepphotphot"   , &OUT::m_lepphotphot   , "m_lepphotphot/F"   );
    outtree->Branch("m_photphot"      , &OUT::m_photphot      , "m_photphot/F"      );

    // *************************
    // Begin loop over the input tree
    // *************************
    if( maxevt == 0 ) {
        maxevt = chain->GetEntries();
    }

    int n_saved = 0;
    std::cout << "Will analyze " << maxevt-minevt << " events between " << minevt << " and " << maxevt << std::endl;
    for( int cidx = minevt; cidx < maxevt; cidx++ ) {

        if( cidx % 10000 == 0 ) {
          //std::cout << "Processed " << cidx << " entries \xd";
          std::cout << "Processed " << cidx << " entries " << std::endl;
        }

        chain->GetEntry(cidx);

        // In BranchInit
        CopyInputVarsToOutput();

        // loop over configured modules
        bool save_event = true;
        BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
            save_event &= ApplyModule( mod_conf );
        }

        if( save_event ) {
            outtree->Fill();
            n_saved++;
        }
    }

    std::cout << "Wrote " << n_saved << " events" << std::endl;

}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    bool keep_evt = true;
    
    if( config.GetName() == "BuildLepton" ) {
        BuildLepton( config );
    }
    if( config.GetName() == "BuildPhoton" ) {
        BuildPhoton( config );
    }
    if( config.GetName() == "BuildNeutrino" ) {
        BuildNeutrino( config );
    }
    if( config.GetName() == "BuildWboson" ) {
        BuildWboson( config );
    }
    if( config.GetName() == "BuildEvent" ) {
        BuildEvent( config );
    }

    if( config.GetName() == "FilterElec" ) {
        keep_evt &= FilterElec( config );
    }
    if( config.GetName() == "FilterMuon" ) {
        keep_evt &= FilterMuon( config );
    }
    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }
    if( config.GetName() == "FilterTauEvent" ) {
        keep_evt &= FilterTauEvent( config );
    }
    if( config.GetName() == "FilterBasicEvent" ) {
        keep_evt &= FilterBasicEvent( config );
    }

    return keep_evt;

}

void RunModule::BuildLepton( ModuleConfig & config ) const {

    OUT::lep_pt        -> clear();
    OUT::lep_eta       -> clear();
    OUT::lep_phi       -> clear();
    OUT::lep_e         -> clear();
    OUT::lep_motherPID -> clear();
    OUT::lep_isElec    -> clear();
    OUT::lep_isMuon    -> clear();
    OUT::lep_isPos     -> clear();
    OUT::lep_n          = 0;

    std::vector<int> accept_pid;
    std::vector<int> accept_mother;

    accept_pid.push_back(11);
    accept_pid.push_back(13);

    // don't use for now...must also require that taus have status==3 not 1
    //if( config.PassBool("cut_incTau", true ) ) {
    //    accept_pid.push_back(15);
    //}

    if( config.PassBool("cut_incWMother", true ) ) {
        accept_mother.push_back(24);
    }
    if( config.PassBool("cut_incZMother", true ) ) {
        accept_mother.push_back(23);
    }
    if( config.PassBool("cut_incTauMother", true ) ) {
        accept_mother.push_back(15);
    }

    for( int idx = 0; idx < IN::nMC; ++idx ) {
        if( IN::mcStatus[idx] != 1 ) continue;

        if( accept_mother.size() > 0 && 
            std::find(accept_mother.begin(), 
                      accept_mother.end(), abs(IN::mcMomPID[idx])) == accept_mother.end() ) continue;
        if( std::find(accept_pid.begin(), 
                      accept_pid.end(), abs(IN::mcPID[idx]) ) == accept_pid.end() ) continue;

        if( !config.PassFloat( "cut_pt", IN::mcPt[idx] ) ) continue;
        if( !config.PassFloat( "cut_abseta", fabs(IN::mcEta[idx]) ) ) continue;

        OUT::lep_pt        -> push_back(IN::mcPt[idx]     );
        OUT::lep_eta       -> push_back(IN::mcEta[idx]    );
        OUT::lep_phi       -> push_back(IN::mcPhi[idx]    );
        OUT::lep_e         -> push_back(IN::mcE[idx]      );
        OUT::lep_motherPID -> push_back(IN::mcMomPID[idx] );

        if( abs(IN::mcPID[idx]) == 11 ) {
            OUT::lep_isElec->push_back(true);
        }
        else {                           
            OUT::lep_isElec->push_back(false);
        }

        if( abs(IN::mcPID[idx]) == 13 ) {
            OUT::lep_isMuon->push_back(true);
        }
        else {                           
            OUT::lep_isMuon->push_back(false);
        }

        if( IN::mcPID[idx] > 0 ) {
            OUT::lep_isPos->push_back(false);
        }
        else {
            OUT::lep_isPos->push_back(true);
        }

        OUT::lep_n++;
    }
            
}        

//void RunModule::BuildTau( ModuleConfig & /*config*/ ) const {
//
//    OUT::mu_pt        -> clear();
//    OUT::mu_eta       -> clear();
//    OUT::mu_phi       -> clear();
//    OUT::mu_e         -> clear();
//    OUT::mu_motherPID -> clear();
//    OUT::mu_n          = 0;
//
//    for( int idx = 0; idx < IN::nMC; ++idx ) {
//        if( abs(IN::mcPID[idx]) == 13  && IN::mcStatus[idx] == 1 && abs(IN::mcMomPID[idx]) == 24 ) {
//            OUT::mu_pt        -> push_back(IN::mcPt[idx]     );
//            OUT::mu_eta       -> push_back(IN::mcEta[idx]    );
//            OUT::mu_phi       -> push_back(IN::mcPhi[idx]    );
//            OUT::mu_e         -> push_back(IN::mcE[idx]      );
//            OUT::mu_motherPID -> push_back(IN::mcMomPID[idx] );
//            OUT::mu_n++;
//        }
//    }
//            
//}        

void RunModule::BuildNeutrino( ModuleConfig & config ) const {

    OUT::nu_pt        -> clear();
    OUT::nu_eta       -> clear();
    OUT::nu_phi       -> clear();
    OUT::nu_e         -> clear();
    OUT::nu_motherPID -> clear();
    OUT::nu_n          = 0;

    std::vector<int> accept_mother;
    if( config.PassBool("cut_incWMother", true ) ) {
        accept_mother.push_back(24);
    }
    if( config.PassBool("cut_incZMother", true ) ) {
        accept_mother.push_back(23);
    }

    for( int idx = 0; idx < IN::nMC; ++idx ) {
        if( ( abs(IN::mcPID[idx]) == 12 || 
              abs(IN::mcPID[idx]) == 14 ||  
              abs(IN::mcPID[idx]) == 16  ) && IN::mcStatus[idx] == 1 ) {
            if( accept_mother.size() > 0 && 
            std::find(accept_mother.begin(), 
                      accept_mother.end(), abs(IN::mcMomPID[idx])) == accept_mother.end() ) continue;
            OUT::nu_pt        -> push_back(IN::mcPt[idx]     );
            OUT::nu_eta       -> push_back(IN::mcEta[idx]    );
            OUT::nu_phi       -> push_back(IN::mcPhi[idx]    );
            OUT::nu_e         -> push_back(IN::mcE[idx]      );
            OUT::nu_motherPID -> push_back(IN::mcMomPID[idx] );
            OUT::nu_n++;
        }
    }
            
}        

void RunModule::BuildWboson( ModuleConfig & /*config*/ ) const {

    OUT::w_pt        -> clear();
    OUT::w_eta       -> clear();
    OUT::w_phi       -> clear();
    OUT::w_e         -> clear();
    OUT::w_isPos     -> clear();
    OUT::w_n          = 0;

    for( int idx = 0; idx < IN::nMC; ++idx ) {
        if( abs(IN::mcPID[idx]) == 24 && IN::mcStatus[idx] == 3 ) {
            OUT::w_pt        -> push_back(IN::mcPt[idx]     );
            OUT::w_eta       -> push_back(IN::mcEta[idx]    );
            OUT::w_phi       -> push_back(IN::mcPhi[idx]    );
            OUT::w_e         -> push_back(IN::mcE[idx]      );
            OUT::w_n++;
        }

        if( IN::mcPID[idx] > 0 ) {
            OUT::w_isPos->push_back(true);
        }
        else {
            OUT::w_isPos->push_back(false);
        }
    }
}

void RunModule::BuildPhoton( ModuleConfig & config ) const {

    OUT::phot_pt        -> clear();
    OUT::phot_eta       -> clear();
    OUT::phot_phi       -> clear();
    OUT::phot_e         -> clear();
    OUT::phot_motherPID -> clear();
    OUT::phot_n          = 0;

    for( int idx = 0; idx < IN::nMC; ++idx  ) {
        if( IN::mcPID[idx] == 22 && IN::mcStatus[idx] == 1 ) {

            if( !config.PassFloat( "cut_pt", IN::mcPt[idx] ) ) continue;
            if( !config.PassFloat( "cut_abseta", fabs(IN::mcEta[idx]) ) ) continue;

            OUT::phot_pt        -> push_back(IN::mcPt[idx]     );
            OUT::phot_eta       -> push_back(IN::mcEta[idx]    );
            OUT::phot_phi       -> push_back(IN::mcPhi[idx]    );
            OUT::phot_e         -> push_back(IN::mcE[idx]      );
            OUT::phot_motherPID -> push_back(IN::mcMomPID[idx] );
            OUT::phot_n++;
        }
    }
            
}        

bool RunModule::FilterBasicEvent( ModuleConfig & config ) const {

    bool keep_evt = true;
    std::vector<int> accept_l_mothers;
    std::vector<int> accept_w_mothers;
    std::vector<int> accept_q_mothers;
    accept_l_mothers.push_back(11);
    accept_l_mothers.push_back(13);
    accept_l_mothers.push_back(15);

    accept_w_mothers.push_back(24);

    accept_q_mothers.push_back(1);
    accept_q_mothers.push_back(2);
    accept_q_mothers.push_back(3);
    accept_q_mothers.push_back(4);
    accept_q_mothers.push_back(5);
    accept_q_mothers.push_back(6);

    int nphot = 0;
    int nphot_l_mom = 0;
    int nphot_w_mom = 0;
    int nphot_q_mom = 0;
    for( int idx = 0; idx < IN::nMC; ++idx  ) {
        if( IN::mcPID[idx] == 22 ) {
            nphot++;
            
            if( std::find( accept_l_mothers.begin(), accept_l_mothers.end(), abs(IN::mcMomPID[idx]) ) != accept_l_mothers.end() ) {
                nphot_l_mom++;
            }
            if( std::find( accept_w_mothers.begin(), accept_w_mothers.end(), abs(IN::mcMomPID[idx]) ) != accept_w_mothers.end() ) {
                nphot_w_mom++;
            }
            if( std::find( accept_q_mothers.begin(), accept_q_mothers.end(), abs(IN::mcMomPID[idx]) ) != accept_q_mothers.end() ) {
                nphot_q_mom++;
            }
        }
    }


    if( !config.PassInt( "cut_nPhot", nphot ) ) keep_evt=false;
    if( !config.PassInt( "cut_nPhotLepMom", nphot_l_mom ) ) keep_evt=false;
    if( !config.PassInt( "cut_nPhotWMom", nphot_w_mom ) ) keep_evt=false;
    if( !config.PassInt( "cut_nPhotQuarkMom", nphot_q_mom ) ) keep_evt=false;

    return keep_evt;
}

void RunModule::BuildEvent( ModuleConfig & /*config*/ ) const {

    std::vector<TLorentzVector> leptons;
    std::vector<TLorentzVector> neutrinos;
    std::vector<TLorentzVector> photons;

    for( int idx = 0; idx < OUT::lep_n; ++idx ) {
        TLorentzVector lep;
        lep.SetPtEtaPhiE( OUT::lep_pt->at(idx), 
                          OUT::lep_eta->at(idx),
                          OUT::lep_phi->at(idx),
                          OUT::lep_e->at(idx)
                        );
        leptons.push_back(lep);
    }
    for( int idx = 0; idx < OUT::nu_n; ++idx ) {
        TLorentzVector nu;
        nu.SetPtEtaPhiE(  OUT::nu_pt->at(idx), 
                          OUT::nu_eta->at(idx),
                          OUT::nu_phi->at(idx),
                          OUT::nu_e->at(idx)
                        );
        neutrinos.push_back(nu);
    }

    std::vector<std::pair<float, int> > sorted_photons;
    for( int idx = 0; idx < OUT::phot_n; ++idx ) {
        TLorentzVector phot;
        phot.SetPtEtaPhiE(  OUT::phot_pt->at(idx), 
                            OUT::phot_eta->at(idx),
                            OUT::phot_phi->at(idx),
                            OUT::phot_e->at(idx)
                        );
        photons.push_back(phot);
        sorted_photons.push_back(std::make_pair( phot.Pt(), idx ));
    }


    // sort the list of photon momenta in descending order
    std::sort(sorted_photons.rbegin(), sorted_photons.rend());

    if( photons.size() > 1 ) { 
        OUT::leadPhot_pt = sorted_photons[0].first;
        OUT::sublPhot_pt = sorted_photons[1].first;

        int leadidx = sorted_photons[0].second;
        int sublidx = sorted_photons[1].second;
        OUT::m_photphot = ( photons[leadidx] + photons[sublidx] ).M();
    }
    else if ( photons.size() == 1 ) {
        OUT::leadPhot_pt = sorted_photons[0].first;
        OUT::sublPhot_pt = 0;
    }

    if( leptons.size() == 2 ) {
        OUT::m_leplep = ( leptons[0] + leptons[1] ).M();
    }

    if( leptons.size() == 1 && neutrinos.size() == 1 ) {
       
        OUT::m_lepnu = ( leptons[0] + neutrinos[0] ).M();
        OUT::mt_lepnu = calc_mt( leptons[0], neutrinos[0] );

        if( photons.size() > 1 ) { 

            int leadidx = sorted_photons[0].second;
            int sublidx = sorted_photons[1].second;

            OUT::leadPhot_lepDR = photons[leadidx].DeltaR(leptons[0]);
            OUT::sublPhot_lepDR = photons[sublidx].DeltaR(leptons[0]);
            OUT::phot_photDR    = photons[leadidx].DeltaR(photons[sublidx]);
            OUT::photPhot_lepDR = (photons[leadidx]+photons[sublidx]).DeltaR(photons[sublidx]);
            
            OUT::leadPhot_lepDPhi = photons[leadidx].DeltaPhi(leptons[0]);
            OUT::sublPhot_lepDPhi = photons[sublidx].DeltaPhi(leptons[0]);
            OUT::phot_photDPhi    = photons[leadidx].DeltaPhi(photons[sublidx]);
            OUT::photPhot_lepDPhi = (photons[leadidx]+photons[sublidx]).DeltaPhi(photons[sublidx]);
            
            OUT::m_lepphot1nu = ( leptons[0] + photons[leadidx] + neutrinos[0] ).M();
            OUT::m_lepphot2nu = ( leptons[0] + photons[sublidx] + neutrinos[0] ).M();
            OUT::mt_lepphot1nu = calc_mt( leptons[0] + photons[leadidx], neutrinos[0] );
            OUT::mt_lepphot2nu = calc_mt( leptons[0] + photons[sublidx], neutrinos[0] );

            OUT::m_lepphotphotnu = ( leptons[0] + photons[leadidx] + photons[sublidx] + neutrinos[0] ).M();
            OUT::mt_lepphotphotnu = calc_mt( leptons[0] + photons[leadidx] + photons[sublidx], neutrinos[0] );

            OUT::m_lepphot1 = ( leptons[0] + photons[leadidx] ).M();
            OUT::m_lepphot2 = ( leptons[0] + photons[sublidx] ).M();
            OUT::m_lepphotphot = ( leptons[0] + photons[leadidx] + photons[sublidx] ).M();
        }
        else if( photons.size() == 1 ) {

            int leadidx = sorted_photons[0].second;
            OUT::leadPhot_lepDR = photons[leadidx].DeltaR(leptons[0]);

            OUT::m_lepphot1nu = ( leptons[0] + photons[leadidx] + neutrinos[0] ).M();
            OUT::mt_lepphot1nu = calc_mt( leptons[0] + photons[leadidx], neutrinos[0] );

            OUT::m_lepphot1 = ( leptons[0] + photons[leadidx] ).M();

        }
            
            
    }

}

bool RunModule::FilterElec( ModuleConfig & config ) const {

    //int nElOut = 0;
    //for( int idx = 0; idx < IN::nEle; ++idx ) {
    //    
    //    float elePt = IN::elePt[idx];

    //    if( !config.PassFloat( "cut_pt", elePt ) ) continue;

    //    nElOut++;
    //}

    //OUT::nEle = nElOut;

    return true;
}     

bool RunModule::FilterMuon( ModuleConfig & config ) const {

    //int nMuOut = 0;
    //for( int idx = 0; idx < IN::nMu; ++idx ) {
    //    
    //    float muPt = IN::muPt[idx];

    //    if( !config.PassFloat( "cut_pt", muPt ) ) continue;

    //    nMuOut++;
    //    OUT::muPt[idx] = muPt;
    //}

    //OUT::nMu = nMuOut;

    return true;
}     

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;
    if( !config.PassInt("cut_nLep", OUT::lep_n ) ) keep_event = false;

    //count number of photons that originate from a W
    int nwphot=0;
    for( int idx = 0 ; idx < OUT::phot_n; ++idx ) {
        if( abs(OUT::phot_motherPID->at(idx)) == 24 ) {
            nwphot++;
        }
    }

    if( !config.PassInt("cut_nWPhot", nwphot ) ) keep_event = false;

    return keep_event;

    
}
bool RunModule::FilterTauEvent( ModuleConfig & config ) const {

    bool keep_evt = true;

    int ntau=0;
    for( int idx = 0; idx < IN::nMC; ++idx ) {
        if( fabs(IN::mcPID[idx]) != 15 ) continue;
        if( fabs(IN::mcMomPID[idx]) != 24 ) continue;

        if( !config.PassInt( "cut_tauStatus", IN::mcStatus[idx] ) ) continue;

        ntau++;

    }

    if( !config.PassInt( "cut_nTau", ntau ) ) keep_evt = false;

    return keep_evt;

}
