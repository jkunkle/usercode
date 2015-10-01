#include <vector>
#include <map>
#include "TLorentzVector.h"
#include "Core/Util.h"

namespace Wgg {
void CalcEventVars(const std::vector<TLorentzVector> & photons, 
                                     const std::vector<TLorentzVector> & electrons,
                                     const std::vector<TLorentzVector> & muons,
                                     const std::vector<TLorentzVector> & trigelectrons,
                                     const std::vector<TLorentzVector> & trigmuons,
                                     const TLorentzVector &metlv,
                                     std::map<std::string, float> & results
        );
}

void Wgg::CalcEventVars(const std::vector<TLorentzVector> & photons, 
                                     const std::vector<TLorentzVector> & electrons,
                                     const std::vector<TLorentzVector> & muons,
                                     const std::vector<TLorentzVector> & trigelectrons,
                                     const std::vector<TLorentzVector> & trigmuons,
                                     const TLorentzVector &metlv,
                                     std::map<std::string, float> & results
        ) {

    
    std::vector<std::pair<float, int> > sorted_photons;
    for( unsigned idx = 0; idx < photons.size() ; ++idx ) {
        sorted_photons.push_back( std::make_pair( photons[idx].Pt(), idx ) );
    }

    std::vector<std::pair<float, int> > sorted_leptons;
    std::vector<TLorentzVector> leptons;
    for( unsigned idx = 0; idx < electrons.size() ; ++idx ) {
        leptons.push_back( electrons[idx] );
        sorted_leptons.push_back( std::make_pair( electrons[idx].Pt(), idx ) );
    }
    for( unsigned idx = 0; idx < muons.size() ; ++idx ) {
        sorted_leptons.push_back( std::make_pair( muons[idx].Pt(), idx ) );
        leptons.push_back( muons[idx] );
    }

    // sort the list of photon momenta in descending order
    std::sort(sorted_photons.rbegin(), sorted_photons.rend());
    std::sort(sorted_leptons.rbegin(), sorted_leptons.rend());

    // fill variables for pT sorted photons
    if( sorted_photons.size() > 0 ) { 
        unsigned leadidx = sorted_photons[0].second;
        
        results["dphi_met_leadPhot"] = photons[leadidx].DeltaPhi( metlv );
        if( sorted_leptons.size() > 0 ) {
            unsigned leadlepidx = sorted_leptons[0].second;
            results["leadPhot_leadLepDR"] = photons[leadidx].DeltaR(leptons[leadlepidx]);
            results["m_leadPhot_leadLep"] = ( leptons[0] + photons[leadidx] ).M();
            if( sorted_leptons.size() > 1 ) {
                unsigned subllepidx = sorted_leptons[1].second;
                results["leadPhot_sublLepDR"] = photons[leadidx].DeltaR(leptons[subllepidx]);
            }
        }
        if( trigelectrons.size() > 0 ) {
            results["m_leadPhot_trigEl"] = ( trigelectrons[0] + photons[leadidx] ).M();
            results["leadPhot_trigElDR"] = photons[leadidx].DeltaR(trigelectrons[0]);
        }
        if( trigmuons.size() > 0 ) {
            results["leadPhot_trigMuDR"] = photons[leadidx].DeltaR(trigmuons[0]);
        }
        if( sorted_photons.size() > 1 ) {
            int leadidx = sorted_photons[0].second;
            int sublidx = sorted_photons[1].second;
            results["leadPhot_sublPhotDR"]    = photons[leadidx].DeltaR(photons[sublidx]);
            results["leadPhot_sublPhotDPhi"]    = photons[leadidx].DeltaPhi(photons[sublidx]);
            results["dphi_met_sublPhot"] = photons[sublidx].DeltaPhi( metlv );
            if( sorted_leptons.size() > 0 ) {
                unsigned leadlepidx = sorted_leptons[0].second;
                results["sublPhot_leadLepDR"] = photons[sublidx].DeltaR(leptons[leadlepidx]);
                results["m_sublPhot_leadLep"] = ( leptons[leadlepidx] + photons[sublidx] ).M();
                if( sorted_leptons.size() > 1 ) {
                    unsigned subllepidx = sorted_leptons[1].second;
                    results["sublPhot_sublLepDR"] = photons[sublidx].DeltaR(leptons[subllepidx]);
                }
            }
            if( trigelectrons.size() > 0 ) {
                results["m_sublPhot_trigEl"] = ( trigelectrons[0] + photons[sublidx] ).M();
                results["m_leadPhot_sublPhot_trigEl"] = ( trigelectrons[0] + photons[leadidx] + photons[sublidx] ).M();
                results["sublPhot_trigElDR"] = photons[sublidx].DeltaR(trigelectrons[0]);
            }
            if( trigmuons.size() > 0 ) {
                results["sublPhot_trigMuDR"] = photons[sublidx].DeltaR(trigmuons[0]);
            }

            results["pt_leadph12"] = photons[leadidx].Pt();
            results["pt_sublph12"] = photons[sublidx].Pt();
            results["eta_leadph12"] = photons[leadidx].Eta();
            results["eta_sublph12"] = photons[sublidx].Eta();

        }
    }
    // fill variables for default sorted photons
    if( photons.size() > 0 ) { 
        results["dphi_met_ph1"] = photons[0].DeltaPhi( metlv );
        if( sorted_leptons.size() > 0 ) {
            results["dr_ph1_leadLep"] = photons[0].DeltaR(leptons[sorted_leptons[0].second]);
            results["dphi_ph1_leadLep"] = photons[0].DeltaPhi(leptons[sorted_leptons[0].second]);
            results["m_leadLep_ph1"] = ( photons[0] + leptons[sorted_leptons[0].second] ).M();
            if( sorted_leptons.size() > 1 ) {
                results["dr_ph1_sublLep"] = photons[0].DeltaR(leptons[sorted_leptons[1].second]);
                results["dphi_ph1_sublLep"] = photons[0].DeltaPhi(leptons[sorted_leptons[1].second]);
            }

            results["mt_lepph1_met"] = Utils::calc_mt( leptons[0] + photons[0], metlv );
            results["m_lepph1"] = ( leptons[0] + photons[0] ).M();
        }


        if( trigelectrons.size() > 0 ) {
            results["dr_ph1_trigEle"] = photons[0].DeltaR( trigelectrons[0] );
            results["m_trigelph1"] = ( photons[0] + trigelectrons[0] ).M();
        }
        if( trigmuons.size() > 0 ) {
            results["dr_ph1_trigMu"] = photons[0].DeltaR( trigmuons[0] );
        }
        if( sorted_leptons.size() > 1) {
            unsigned subllepidx = sorted_leptons[1].second;
            results["m_sublLep_ph1"] = ( leptons[subllepidx] + photons[0] ).M();
        }
        if( photons.size() > 1 ) {

            results["dr_ph1_ph2"] = photons[0].DeltaR(photons[1]);
            results["dphi_ph1_ph2"] = photons[0].DeltaPhi(photons[1]);
            results["m_ph1_ph2"] = (photons[0] + photons[1]).M();
            results["pt_ph1_ph2"] = (photons[0] + photons[1]).Pt();
            results["dphi_met_ph2"] = photons[1].DeltaPhi( metlv );

            if( sorted_leptons.size() > 0 ) {
                results["dr_ph2_leadLep"] = photons[1].DeltaR( leptons[sorted_leptons[0].second]);
                results["dphi_ph2_leadLep"] = photons[1].DeltaPhi( leptons[sorted_leptons[0].second]);
                results["m_leadLep_ph1_ph2"] = ( photons[0] + photons[1] + leptons[sorted_leptons[0].second] ).M();
                results["m_leadLep_ph2"] = ( photons[1] + leptons[sorted_leptons[0].second] ).M();

                results["mt_lepph2_met"] = Utils::calc_mt( leptons[0] + photons[1], metlv );
                results["mt_lepphph_met"] =Utils::calc_mt( leptons[0] + photons[0] + photons[1], metlv );
                results["pt_lepph1"]  = ( leptons[0] + photons[0] ).Pt();
                results["m_lepph2"] = ( leptons[0] + photons[1] ).M();
                results["m_lepphph"] = ( leptons[0] + photons[0] + photons[1] ).M();

                if( sorted_leptons.size() > 1 ) {
                    unsigned subllepidx = sorted_leptons[1].second;
                    results["dr_ph2_sublLep"] = photons[1].DeltaR(leptons[subllepidx]);
                    results["dphi_ph2_sublLep"] = photons[1].DeltaPhi(leptons[subllepidx]);
                    results["m_sublLep_ph2"] = ( leptons[subllepidx] + photons[1] ).M();
                    results["pt_lepph2"]  = ( leptons[0] + photons[1] ).Pt();
                    results["pt_lepphph"] = ( leptons[0] + photons[0] + photons[1] ).Pt();
                }
            }
            if( trigelectrons.size() > 0 ) {
                results["dr_ph2_trigEle"] = photons[1].DeltaR( trigelectrons[0] );
                results["m_trigelph2"] = ( photons[1] + trigelectrons[0] ).M();
                results["m_trigelphph"] = ( photons[0] + photons[1] + trigelectrons[0] ).M();
            }
            if( trigmuons.size() > 0 ) {
                results["dr_ph2_trigMu"] = photons[1].DeltaR( trigmuons[0] );
            }
        }
    }

    if( leptons.size() > 0 ) {
        results["mt_lep_met"] = Utils::calc_mt( leptons[0], metlv );
        results["dphi_met_lep1"] = leptons[0].DeltaPhi( metlv );

        if( leptons.size() > 1 ) {

            results["m_leplep"] = ( leptons[0] + leptons[1] ).M();
            results["pt_leplep"] = ( leptons[0] + leptons[1] ).Pt();

            results["dphi_met_lep2"] = leptons[1].DeltaPhi( metlv );

            if( photons.size() > 0 ) { 
                results["m_leplepph"]  = (leptons[0] + leptons[1] + photons[0] ).M();
                results["pt_leplepph"]  = (leptons[0] + leptons[1] + photons[0] ).Pt();
                if( photons.size() > 1 ) { 
                    results["m_leplepphph"]  = (leptons[0] + leptons[1] + photons[0] + photons[1] ).M();
                    results["m_leplepph1"]  = (leptons[0] + leptons[1] + photons[0] ).M();
                    results["m_leplepph2"]  = (leptons[0] + leptons[1] + photons[1] ).M();
                }
            }
        }
    }
    if( trigelectrons.size() > 0 ) {
        results["mt_trigel_met"] = Utils::calc_mt( trigelectrons[0], metlv );
    }
    if( trigmuons.size() > 0 ) {
        results["mt_trigmu_met"] = Utils::calc_mt( trigmuons[0], metlv );
    }
    if( muons.size() > 1 ) {
        results["m_mumu"] = ( muons[0] + muons[1] ).M();
    }
    if( electrons.size() > 1 ) {
        results["m_elel"] = ( electrons[0] + electrons[1] ).M();
    }
    if( leptons.size() == 2 ) {
        results["pt_secondLepton"] = sorted_leptons[1].first;
    }
    if( leptons.size() == 3 ) {
        results["pt_thirdLepton"] = sorted_leptons[2].first;
        results["m_3lep"] = ( leptons[0] + leptons[1] + leptons[2] ).M();
    }

    if( leptons.size() == 4 ) {
        results["m_4lep"] = ( leptons[0] + leptons[1] + leptons[2] + leptons[3] ).M();
    }
}

