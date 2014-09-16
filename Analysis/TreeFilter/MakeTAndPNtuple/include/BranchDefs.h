#ifndef BRANCHDEFS_H
#define BRANCHDEFS_H
#include "TTree.h"
#include <vector>
//This next bit of code defines whether each branch
//exists or not.  This can be used to solve the problem
//when a branch in available in some ntuples, but not others.
//If this happens, the code will not compile because the
//branch is not written in the header file.  To fix this problem
//simply surround the offending code with #ifdef EXISTS_MYVAR ... #endif
//and if the variable does not exist the preprocessor will ignore that code
#define EXISTS_nVtx
#define EXISTS_nVtxBS
#define EXISTS_nMC
#define EXISTS_mcPID
#define EXISTS_mcPt
#define EXISTS_mcEta
#define EXISTS_mcPhi
#define EXISTS_mcE
#define EXISTS_mcGMomPID
#define EXISTS_mcMomPID
#define EXISTS_mcParentage
#define EXISTS_mcStatus
#define EXISTS_nPU
#define EXISTS_puTrue
#define EXISTS_pfMET
#define EXISTS_pfMETPhi
#define EXISTS_pfMETsumEt
#define EXISTS_pfMETmEtSig
#define EXISTS_pfMETSig
#define EXISTS_recoPfMET
#define EXISTS_recoPfMETPhi
#define EXISTS_recoPfMETsumEt
#define EXISTS_recoPfMETmEtSig
#define EXISTS_recoPfMETSig
#define EXISTS_rho2012
#define EXISTS_el_n
#define EXISTS_mu_n
#define EXISTS_ph_n
#define EXISTS_jet_n
#define EXISTS_vtx_n
#define EXISTS_el_pt
#define EXISTS_el_eta
#define EXISTS_el_sceta
#define EXISTS_el_phi
#define EXISTS_el_e
#define EXISTS_el_pt_uncorr
#define EXISTS_el_mva_trig
#define EXISTS_el_mva_nontrig
#define EXISTS_el_d0pv
#define EXISTS_el_z0pv
#define EXISTS_el_sigmaIEIE
#define EXISTS_el_pfiso30
#define EXISTS_el_pfiso40
#define EXISTS_el_triggerMatch
#define EXISTS_el_hasMatchedConv
#define EXISTS_el_passTight
#define EXISTS_el_passMedium
#define EXISTS_el_passLoose
#define EXISTS_el_passVeryLoose
#define EXISTS_el_passTightTrig
#define EXISTS_el_passMvaTrig
#define EXISTS_el_passMvaNonTrig
#define EXISTS_el_truthMatch_el
#define EXISTS_el_truthMinDR_el
#define EXISTS_el_truthMatchPt_el
#define EXISTS_mu_pt
#define EXISTS_mu_eta
#define EXISTS_mu_phi
#define EXISTS_mu_e
#define EXISTS_mu_pt_uncorr
#define EXISTS_mu_pfIso_ch
#define EXISTS_mu_pfIso_nh
#define EXISTS_mu_pfIso_pho
#define EXISTS_mu_pfIso_pu
#define EXISTS_mu_corrIso
#define EXISTS_mu_triggerMatch
#define EXISTS_mu_truthMatch
#define EXISTS_mu_truthMinDR
#define EXISTS_ph_pt
#define EXISTS_ph_eta
#define EXISTS_ph_sceta
#define EXISTS_ph_phi
#define EXISTS_ph_e
#define EXISTS_ph_HoverE
#define EXISTS_ph_HoverE12
#define EXISTS_ph_sigmaIEIE
#define EXISTS_ph_sigmaIEIP
#define EXISTS_ph_r9
#define EXISTS_ph_E1x3
#define EXISTS_ph_E2x2
#define EXISTS_ph_E5x5
#define EXISTS_ph_E2x5Max
#define EXISTS_ph_SCetaWidth
#define EXISTS_ph_SCphiWidth
#define EXISTS_ph_ESEffSigmaRR
#define EXISTS_ph_hcalIsoDR03
#define EXISTS_ph_trkIsoHollowDR03
#define EXISTS_ph_chgpfIsoDR02
#define EXISTS_ph_pfChIsoWorst
#define EXISTS_ph_chIso
#define EXISTS_ph_neuIso
#define EXISTS_ph_phoIso
#define EXISTS_ph_chIsoCorr
#define EXISTS_ph_neuIsoCorr
#define EXISTS_ph_phoIsoCorr
#define EXISTS_ph_SCRChIso
#define EXISTS_ph_SCRPhoIso
#define EXISTS_ph_SCRNeuIso
#define EXISTS_ph_SCRChIso04
#define EXISTS_ph_SCRPhoIso04
#define EXISTS_ph_SCRNeuIso04
#define EXISTS_ph_RandConeChIso
#define EXISTS_ph_RandConePhoIso
#define EXISTS_ph_RandConeNeuIso
#define EXISTS_ph_RandConeChIso04
#define EXISTS_ph_RandConePhoIso04
#define EXISTS_ph_RandConeNeuIso04
#define EXISTS_ph_eleVeto
#define EXISTS_ph_hasPixSeed
#define EXISTS_ph_drToTrk
#define EXISTS_ph_isConv
#define EXISTS_ph_conv_nTrk
#define EXISTS_ph_conv_vtx_x
#define EXISTS_ph_conv_vtx_y
#define EXISTS_ph_conv_vtx_z
#define EXISTS_ph_conv_ptin1
#define EXISTS_ph_conv_ptin2
#define EXISTS_ph_conv_ptout1
#define EXISTS_ph_conv_ptout2
#define EXISTS_ph_passTight
#define EXISTS_ph_passMedium
#define EXISTS_ph_passLoose
#define EXISTS_ph_passLooseNoSIEIE
#define EXISTS_ph_passHOverELoose
#define EXISTS_ph_passHOverEMedium
#define EXISTS_ph_passHOverETight
#define EXISTS_ph_passSIEIELoose
#define EXISTS_ph_passSIEIEMedium
#define EXISTS_ph_passSIEIETight
#define EXISTS_ph_passChIsoCorrLoose
#define EXISTS_ph_passChIsoCorrMedium
#define EXISTS_ph_passChIsoCorrTight
#define EXISTS_ph_passNeuIsoCorrLoose
#define EXISTS_ph_passNeuIsoCorrMedium
#define EXISTS_ph_passNeuIsoCorrTight
#define EXISTS_ph_passPhoIsoCorrLoose
#define EXISTS_ph_passPhoIsoCorrMedium
#define EXISTS_ph_passPhoIsoCorrTight
#define EXISTS_ph_truthMatch_el
#define EXISTS_ph_truthMinDR_el
#define EXISTS_ph_truthMatchPt_el
#define EXISTS_ph_truthMatch_ph
#define EXISTS_ph_truthMinDR_ph
#define EXISTS_ph_truthMatchPt_ph
#define EXISTS_ph_truthMatchMotherPID_ph
#define EXISTS_ph_hasSLConv
#define EXISTS_ph_pass_mva_presel
#define EXISTS_ph_mvascore
#define EXISTS_ph_IsEB
#define EXISTS_ph_IsEE
#define EXISTS_jet_pt
#define EXISTS_jet_eta
#define EXISTS_jet_phi
#define EXISTS_jet_e
#define EXISTS_PUWeight
#define EXISTS_isBlinded
#define EXISTS_EventWeight
#define EXISTS_mu_pt25_n
#define EXISTS_mu_passtrig_n
#define EXISTS_mu_passtrig25_n
#define EXISTS_el_pt25_n
#define EXISTS_el_passtrig_n
#define EXISTS_el_passtrig28_n
#define EXISTS_ph_mediumNoSIEIE_n
#define EXISTS_ph_medium_n
#define EXISTS_ph_mediumNoEleVeto_n
#define EXISTS_ph_mediumNoSIEIENoEleVeto_n
#define EXISTS_ph_mediumNoIso_n
#define EXISTS_ph_mediumNoChIso_n
#define EXISTS_ph_mediumNoNeuIso_n
#define EXISTS_ph_mediumNoPhoIso_n
#define EXISTS_ph_mediumNoChIsoNoNeuIso_n
#define EXISTS_ph_mediumNoChIsoNoPhoIso_n
#define EXISTS_ph_mediumNoNeuIsoNoPhoIso_n
#define EXISTS_ph_trigMatch_el
#define EXISTS_leadPhot_pt
#define EXISTS_sublPhot_pt
#define EXISTS_leadPhot_lepDR
#define EXISTS_sublPhot_lepDR
#define EXISTS_ph_phDR
#define EXISTS_phPhot_lepDR
#define EXISTS_leadPhot_lepDPhi
#define EXISTS_sublPhot_lepDPhi
#define EXISTS_ph_phDPhi
#define EXISTS_phPhot_lepDPhi
#define EXISTS_dphi_met_lep1
#define EXISTS_dphi_met_lep2
#define EXISTS_dphi_met_ph1
#define EXISTS_dphi_met_ph2
#define EXISTS_mt_lep_met
#define EXISTS_mt_lepph1_met
#define EXISTS_mt_lepph2_met
#define EXISTS_mt_lepphph_met
#define EXISTS_m_leplep
#define EXISTS_m_lepph1
#define EXISTS_m_lepph2
#define EXISTS_m_leplepph
#define EXISTS_m_lepphph
#define EXISTS_m_phph
#define EXISTS_m_leplepZ
#define EXISTS_m_3lep
#define EXISTS_m_4lep
#define EXISTS_pt_phph
#define EXISTS_pt_leplep
#define EXISTS_pt_lepph1
#define EXISTS_pt_lepph2
#define EXISTS_pt_lepphph
#define EXISTS_pt_leplepph
#define EXISTS_pt_secondLepton
#define EXISTS_pt_thirdLepton
#define EXISTS_leadPhot_leadLepDR
#define EXISTS_leadPhot_sublLepDR
#define EXISTS_sublPhot_leadLepDR
#define EXISTS_sublPhot_sublLepDR
#define EXISTS_m_nearestToZ
#define EXISTS_m_minZdifflepph
#define EXISTS_truelep_n
#define EXISTS_trueph_n
#define EXISTS_trueph_wmother_n
#define EXISTS_truegenph_n
#define EXISTS_truegenphpt15_n
#define EXISTS_truelep_pt
#define EXISTS_truelep_eta
#define EXISTS_truelep_phi
#define EXISTS_truelep_e
#define EXISTS_truelep_isElec
#define EXISTS_truelep_isMuon
#define EXISTS_truelep_motherPID
#define EXISTS_trueph_pt
#define EXISTS_trueph_eta
#define EXISTS_trueph_phi
#define EXISTS_trueph_motherPID
#define EXISTS_trueph_parentage
#define EXISTS_trueph_nearestLepDR
#define EXISTS_trueph_nearestQrkDR
#define EXISTS_trueleadlep_pt
#define EXISTS_truesubllep_pt
#define EXISTS_trueleadlep_leadPhotDR
#define EXISTS_trueleadlep_sublPhotDR
#define EXISTS_truesubllep_leadPhotDR
#define EXISTS_truesubllep_sublPhotDR
//Define variables as extern below and declare them in the .cxx file to avoid multiple definitions
namespace IN {
 extern Int_t				nVtx;
 extern Int_t				nVtxBS;
 extern Int_t				nMC;
 extern std::vector<int>				*mcPID;
 extern std::vector<float>				*mcPt;
 extern std::vector<float>				*mcEta;
 extern std::vector<float>				*mcPhi;
 extern std::vector<float>				*mcE;
 extern std::vector<int>				*mcGMomPID;
 extern std::vector<int>				*mcMomPID;
 extern std::vector<int>				*mcParentage;
 extern std::vector<int>				*mcStatus;
 extern std::vector<int>				*nPU;
 extern std::vector<float>				*puTrue;
 extern Float_t				pfMET;
 extern Float_t				pfMETPhi;
 extern Float_t				pfMETsumEt;
 extern Float_t				pfMETmEtSig;
 extern Float_t				pfMETSig;
 extern Float_t				recoPfMET;
 extern Float_t				recoPfMETPhi;
 extern Float_t				recoPfMETsumEt;
 extern Float_t				recoPfMETmEtSig;
 extern Float_t				recoPfMETSig;
 extern Float_t				rho2012;
 extern Int_t				el_n;
 extern Int_t				mu_n;
 extern Int_t				ph_n;
 extern Int_t				jet_n;
 extern Int_t				vtx_n;
 extern std::vector<float>				*el_pt;
 extern std::vector<float>				*el_eta;
 extern std::vector<float>				*el_sceta;
 extern std::vector<float>				*el_phi;
 extern std::vector<float>				*el_e;
 extern std::vector<float>				*el_pt_uncorr;
 extern std::vector<float>				*el_mva_trig;
 extern std::vector<float>				*el_mva_nontrig;
 extern std::vector<float>				*el_d0pv;
 extern std::vector<float>				*el_z0pv;
 extern std::vector<float>				*el_sigmaIEIE;
 extern std::vector<float>				*el_pfiso30;
 extern std::vector<float>				*el_pfiso40;
 extern std::vector<bool>				*el_triggerMatch;
 extern std::vector<bool>				*el_hasMatchedConv;
 extern std::vector<bool>				*el_passTight;
 extern std::vector<bool>				*el_passMedium;
 extern std::vector<bool>				*el_passLoose;
 extern std::vector<bool>				*el_passVeryLoose;
 extern std::vector<bool>				*el_passTightTrig;
 extern std::vector<bool>				*el_passMvaTrig;
 extern std::vector<bool>				*el_passMvaNonTrig;
 extern std::vector<bool>				*el_truthMatch_el;
 extern std::vector<float>				*el_truthMinDR_el;
 extern std::vector<float>				*el_truthMatchPt_el;
 extern std::vector<float>				*mu_pt;
 extern std::vector<float>				*mu_eta;
 extern std::vector<float>				*mu_phi;
 extern std::vector<float>				*mu_e;
 extern std::vector<float>				*mu_pt_uncorr;
 extern std::vector<float>				*mu_pfIso_ch;
 extern std::vector<float>				*mu_pfIso_nh;
 extern std::vector<float>				*mu_pfIso_pho;
 extern std::vector<float>				*mu_pfIso_pu;
 extern std::vector<float>				*mu_corrIso;
 extern std::vector<bool>				*mu_triggerMatch;
 extern std::vector<bool>				*mu_truthMatch;
 extern std::vector<float>				*mu_truthMinDR;
 extern std::vector<float>				*ph_pt;
 extern std::vector<float>				*ph_eta;
 extern std::vector<float>				*ph_sceta;
 extern std::vector<float>				*ph_phi;
 extern std::vector<float>				*ph_e;
 extern std::vector<float>				*ph_HoverE;
 extern std::vector<float>				*ph_HoverE12;
 extern std::vector<float>				*ph_sigmaIEIE;
 extern std::vector<float>				*ph_sigmaIEIP;
 extern std::vector<float>				*ph_r9;
 extern std::vector<float>				*ph_E1x3;
 extern std::vector<float>				*ph_E2x2;
 extern std::vector<float>				*ph_E5x5;
 extern std::vector<float>				*ph_E2x5Max;
 extern std::vector<float>				*ph_SCetaWidth;
 extern std::vector<float>				*ph_SCphiWidth;
 extern std::vector<float>				*ph_ESEffSigmaRR;
 extern std::vector<float>				*ph_hcalIsoDR03;
 extern std::vector<float>				*ph_trkIsoHollowDR03;
 extern std::vector<float>				*ph_chgpfIsoDR02;
 extern std::vector<float>				*ph_pfChIsoWorst;
 extern std::vector<float>				*ph_chIso;
 extern std::vector<float>				*ph_neuIso;
 extern std::vector<float>				*ph_phoIso;
 extern std::vector<float>				*ph_chIsoCorr;
 extern std::vector<float>				*ph_neuIsoCorr;
 extern std::vector<float>				*ph_phoIsoCorr;
 extern std::vector<float>				*ph_SCRChIso;
 extern std::vector<float>				*ph_SCRPhoIso;
 extern std::vector<float>				*ph_SCRNeuIso;
 extern std::vector<float>				*ph_SCRChIso04;
 extern std::vector<float>				*ph_SCRPhoIso04;
 extern std::vector<float>				*ph_SCRNeuIso04;
 extern std::vector<float>				*ph_RandConeChIso;
 extern std::vector<float>				*ph_RandConePhoIso;
 extern std::vector<float>				*ph_RandConeNeuIso;
 extern std::vector<float>				*ph_RandConeChIso04;
 extern std::vector<float>				*ph_RandConePhoIso04;
 extern std::vector<float>				*ph_RandConeNeuIso04;
 extern std::vector<bool>				*ph_eleVeto;
 extern std::vector<bool>				*ph_hasPixSeed;
 extern std::vector<float>				*ph_drToTrk;
 extern std::vector<bool>				*ph_isConv;
 extern std::vector<int>				*ph_conv_nTrk;
 extern std::vector<float>				*ph_conv_vtx_x;
 extern std::vector<float>				*ph_conv_vtx_y;
 extern std::vector<float>				*ph_conv_vtx_z;
 extern std::vector<float>				*ph_conv_ptin1;
 extern std::vector<float>				*ph_conv_ptin2;
 extern std::vector<float>				*ph_conv_ptout1;
 extern std::vector<float>				*ph_conv_ptout2;
 extern std::vector<bool>				*ph_passTight;
 extern std::vector<bool>				*ph_passMedium;
 extern std::vector<bool>				*ph_passLoose;
 extern std::vector<bool>				*ph_passLooseNoSIEIE;
 extern std::vector<bool>				*ph_passHOverELoose;
 extern std::vector<bool>				*ph_passHOverEMedium;
 extern std::vector<bool>				*ph_passHOverETight;
 extern std::vector<bool>				*ph_passSIEIELoose;
 extern std::vector<bool>				*ph_passSIEIEMedium;
 extern std::vector<bool>				*ph_passSIEIETight;
 extern std::vector<bool>				*ph_passChIsoCorrLoose;
 extern std::vector<bool>				*ph_passChIsoCorrMedium;
 extern std::vector<bool>				*ph_passChIsoCorrTight;
 extern std::vector<bool>				*ph_passNeuIsoCorrLoose;
 extern std::vector<bool>				*ph_passNeuIsoCorrMedium;
 extern std::vector<bool>				*ph_passNeuIsoCorrTight;
 extern std::vector<bool>				*ph_passPhoIsoCorrLoose;
 extern std::vector<bool>				*ph_passPhoIsoCorrMedium;
 extern std::vector<bool>				*ph_passPhoIsoCorrTight;
 extern std::vector<bool>				*ph_truthMatch_el;
 extern std::vector<float>				*ph_truthMinDR_el;
 extern std::vector<float>				*ph_truthMatchPt_el;
 extern std::vector<bool>				*ph_truthMatch_ph;
 extern std::vector<float>				*ph_truthMinDR_ph;
 extern std::vector<float>				*ph_truthMatchPt_ph;
 extern std::vector<int>				*ph_truthMatchMotherPID_ph;
 extern std::vector<bool>				*ph_hasSLConv;
 extern std::vector<bool>				*ph_pass_mva_presel;
 extern std::vector<float>				*ph_mvascore;
 extern std::vector<bool>				*ph_IsEB;
 extern std::vector<bool>				*ph_IsEE;
 extern std::vector<float>				*jet_pt;
 extern std::vector<float>				*jet_eta;
 extern std::vector<float>				*jet_phi;
 extern std::vector<float>				*jet_e;
 extern Float_t				PUWeight;
 extern Bool_t				isBlinded;
 extern Float_t				EventWeight;
 extern Int_t				mu_pt25_n;
 extern Int_t				mu_passtrig_n;
 extern Int_t				mu_passtrig25_n;
 extern Int_t				el_pt25_n;
 extern Int_t				el_passtrig_n;
 extern Int_t				el_passtrig28_n;
 extern Int_t				ph_mediumNoSIEIE_n;
 extern Int_t				ph_medium_n;
 extern Int_t				ph_mediumNoEleVeto_n;
 extern Int_t				ph_mediumNoSIEIENoEleVeto_n;
 extern Int_t				ph_mediumNoIso_n;
 extern Int_t				ph_mediumNoChIso_n;
 extern Int_t				ph_mediumNoNeuIso_n;
 extern Int_t				ph_mediumNoPhoIso_n;
 extern Int_t				ph_mediumNoChIsoNoNeuIso_n;
 extern Int_t				ph_mediumNoChIsoNoPhoIso_n;
 extern Int_t				ph_mediumNoNeuIsoNoPhoIso_n;
 extern std::vector<bool>				*ph_trigMatch_el;
 extern Float_t				leadPhot_pt;
 extern Float_t				sublPhot_pt;
 extern Float_t				leadPhot_lepDR;
 extern Float_t				sublPhot_lepDR;
 extern Float_t				ph_phDR;
 extern Float_t				phPhot_lepDR;
 extern Float_t				leadPhot_lepDPhi;
 extern Float_t				sublPhot_lepDPhi;
 extern Float_t				ph_phDPhi;
 extern Float_t				phPhot_lepDPhi;
 extern Float_t				dphi_met_lep1;
 extern Float_t				dphi_met_lep2;
 extern Float_t				dphi_met_ph1;
 extern Float_t				dphi_met_ph2;
 extern Float_t				mt_lep_met;
 extern Float_t				mt_lepph1_met;
 extern Float_t				mt_lepph2_met;
 extern Float_t				mt_lepphph_met;
 extern Float_t				m_leplep;
 extern Float_t				m_lepph1;
 extern Float_t				m_lepph2;
 extern Float_t				m_leplepph;
 extern Float_t				m_lepphph;
 extern Float_t				m_phph;
 extern Float_t				m_leplepZ;
 extern Float_t				m_3lep;
 extern Float_t				m_4lep;
 extern Float_t				pt_phph;
 extern Float_t				pt_leplep;
 extern Float_t				pt_lepph1;
 extern Float_t				pt_lepph2;
 extern Float_t				pt_lepphph;
 extern Float_t				pt_leplepph;
 extern Float_t				pt_secondLepton;
 extern Float_t				pt_thirdLepton;
 extern Float_t				leadPhot_leadLepDR;
 extern Float_t				leadPhot_sublLepDR;
 extern Float_t				sublPhot_leadLepDR;
 extern Float_t				sublPhot_sublLepDR;
 extern Float_t				m_nearestToZ;
 extern Float_t				m_minZdifflepph;
 extern Int_t				truelep_n;
 extern Int_t				trueph_n;
 extern Int_t				trueph_wmother_n;
 extern Int_t				truegenph_n;
 extern Int_t				truegenphpt15_n;
 extern std::vector<float>				*truelep_pt;
 extern std::vector<float>				*truelep_eta;
 extern std::vector<float>				*truelep_phi;
 extern std::vector<float>				*truelep_e;
 extern std::vector<bool>				*truelep_isElec;
 extern std::vector<bool>				*truelep_isMuon;
 extern std::vector<int>				*truelep_motherPID;
 extern std::vector<float>				*trueph_pt;
 extern std::vector<float>				*trueph_eta;
 extern std::vector<float>				*trueph_phi;
 extern std::vector<int>				*trueph_motherPID;
 extern std::vector<int>				*trueph_parentage;
 extern std::vector<float>				*trueph_nearestLepDR;
 extern std::vector<float>				*trueph_nearestQrkDR;
 extern Float_t				trueleadlep_pt;
 extern Float_t				truesubllep_pt;
 extern Float_t				trueleadlep_leadPhotDR;
 extern Float_t				trueleadlep_sublPhotDR;
 extern Float_t				truesubllep_leadPhotDR;
 extern Float_t				truesubllep_sublPhotDR;
};
namespace OUT {
 extern Int_t				nVtx;
 extern Int_t				nVtxBS;
 extern Int_t				nMC;
 extern std::vector<int>				*mcPID;
 extern std::vector<float>				*mcPt;
 extern std::vector<float>				*mcEta;
 extern std::vector<float>				*mcPhi;
 extern std::vector<float>				*mcE;
 extern std::vector<int>				*mcGMomPID;
 extern std::vector<int>				*mcMomPID;
 extern std::vector<int>				*mcParentage;
 extern std::vector<int>				*mcStatus;
 extern std::vector<int>				*nPU;
 extern std::vector<float>				*puTrue;
 extern Float_t				pfMET;
 extern Float_t				pfMETPhi;
 extern Float_t				pfMETsumEt;
 extern Float_t				pfMETmEtSig;
 extern Float_t				pfMETSig;
 extern Float_t				recoPfMET;
 extern Float_t				recoPfMETPhi;
 extern Float_t				recoPfMETsumEt;
 extern Float_t				recoPfMETmEtSig;
 extern Float_t				recoPfMETSig;
 extern Float_t				rho2012;
 extern Int_t				el_n;
 extern Int_t				mu_n;
 extern Int_t				ph_n;
 extern Int_t				jet_n;
 extern Int_t				vtx_n;
 extern std::vector<float>				*el_pt;
 extern std::vector<float>				*el_eta;
 extern std::vector<float>				*el_sceta;
 extern std::vector<float>				*el_phi;
 extern std::vector<float>				*el_e;
 extern std::vector<float>				*el_pt_uncorr;
 extern std::vector<float>				*el_mva_trig;
 extern std::vector<float>				*el_mva_nontrig;
 extern std::vector<float>				*el_d0pv;
 extern std::vector<float>				*el_z0pv;
 extern std::vector<float>				*el_sigmaIEIE;
 extern std::vector<float>				*el_pfiso30;
 extern std::vector<float>				*el_pfiso40;
 extern std::vector<bool>				*el_triggerMatch;
 extern std::vector<bool>				*el_hasMatchedConv;
 extern std::vector<bool>				*el_passTight;
 extern std::vector<bool>				*el_passMedium;
 extern std::vector<bool>				*el_passLoose;
 extern std::vector<bool>				*el_passVeryLoose;
 extern std::vector<bool>				*el_passTightTrig;
 extern std::vector<bool>				*el_passMvaTrig;
 extern std::vector<bool>				*el_passMvaNonTrig;
 extern std::vector<bool>				*el_truthMatch_el;
 extern std::vector<float>				*el_truthMinDR_el;
 extern std::vector<float>				*el_truthMatchPt_el;
 extern std::vector<float>				*mu_pt;
 extern std::vector<float>				*mu_eta;
 extern std::vector<float>				*mu_phi;
 extern std::vector<float>				*mu_e;
 extern std::vector<float>				*mu_pt_uncorr;
 extern std::vector<float>				*mu_pfIso_ch;
 extern std::vector<float>				*mu_pfIso_nh;
 extern std::vector<float>				*mu_pfIso_pho;
 extern std::vector<float>				*mu_pfIso_pu;
 extern std::vector<float>				*mu_corrIso;
 extern std::vector<bool>				*mu_triggerMatch;
 extern std::vector<bool>				*mu_truthMatch;
 extern std::vector<float>				*mu_truthMinDR;
 extern std::vector<float>				*ph_pt;
 extern std::vector<float>				*ph_eta;
 extern std::vector<float>				*ph_sceta;
 extern std::vector<float>				*ph_phi;
 extern std::vector<float>				*ph_e;
 extern std::vector<float>				*ph_HoverE;
 extern std::vector<float>				*ph_HoverE12;
 extern std::vector<float>				*ph_sigmaIEIE;
 extern std::vector<float>				*ph_sigmaIEIP;
 extern std::vector<float>				*ph_r9;
 extern std::vector<float>				*ph_E1x3;
 extern std::vector<float>				*ph_E2x2;
 extern std::vector<float>				*ph_E5x5;
 extern std::vector<float>				*ph_E2x5Max;
 extern std::vector<float>				*ph_SCetaWidth;
 extern std::vector<float>				*ph_SCphiWidth;
 extern std::vector<float>				*ph_ESEffSigmaRR;
 extern std::vector<float>				*ph_hcalIsoDR03;
 extern std::vector<float>				*ph_trkIsoHollowDR03;
 extern std::vector<float>				*ph_chgpfIsoDR02;
 extern std::vector<float>				*ph_pfChIsoWorst;
 extern std::vector<float>				*ph_chIso;
 extern std::vector<float>				*ph_neuIso;
 extern std::vector<float>				*ph_phoIso;
 extern std::vector<float>				*ph_chIsoCorr;
 extern std::vector<float>				*ph_neuIsoCorr;
 extern std::vector<float>				*ph_phoIsoCorr;
 extern std::vector<float>				*ph_SCRChIso;
 extern std::vector<float>				*ph_SCRPhoIso;
 extern std::vector<float>				*ph_SCRNeuIso;
 extern std::vector<float>				*ph_SCRChIso04;
 extern std::vector<float>				*ph_SCRPhoIso04;
 extern std::vector<float>				*ph_SCRNeuIso04;
 extern std::vector<float>				*ph_RandConeChIso;
 extern std::vector<float>				*ph_RandConePhoIso;
 extern std::vector<float>				*ph_RandConeNeuIso;
 extern std::vector<float>				*ph_RandConeChIso04;
 extern std::vector<float>				*ph_RandConePhoIso04;
 extern std::vector<float>				*ph_RandConeNeuIso04;
 extern std::vector<bool>				*ph_eleVeto;
 extern std::vector<bool>				*ph_hasPixSeed;
 extern std::vector<float>				*ph_drToTrk;
 extern std::vector<bool>				*ph_isConv;
 extern std::vector<int>				*ph_conv_nTrk;
 extern std::vector<float>				*ph_conv_vtx_x;
 extern std::vector<float>				*ph_conv_vtx_y;
 extern std::vector<float>				*ph_conv_vtx_z;
 extern std::vector<float>				*ph_conv_ptin1;
 extern std::vector<float>				*ph_conv_ptin2;
 extern std::vector<float>				*ph_conv_ptout1;
 extern std::vector<float>				*ph_conv_ptout2;
 extern std::vector<bool>				*ph_passTight;
 extern std::vector<bool>				*ph_passMedium;
 extern std::vector<bool>				*ph_passLoose;
 extern std::vector<bool>				*ph_passLooseNoSIEIE;
 extern std::vector<bool>				*ph_passHOverELoose;
 extern std::vector<bool>				*ph_passHOverEMedium;
 extern std::vector<bool>				*ph_passHOverETight;
 extern std::vector<bool>				*ph_passSIEIELoose;
 extern std::vector<bool>				*ph_passSIEIEMedium;
 extern std::vector<bool>				*ph_passSIEIETight;
 extern std::vector<bool>				*ph_passChIsoCorrLoose;
 extern std::vector<bool>				*ph_passChIsoCorrMedium;
 extern std::vector<bool>				*ph_passChIsoCorrTight;
 extern std::vector<bool>				*ph_passNeuIsoCorrLoose;
 extern std::vector<bool>				*ph_passNeuIsoCorrMedium;
 extern std::vector<bool>				*ph_passNeuIsoCorrTight;
 extern std::vector<bool>				*ph_passPhoIsoCorrLoose;
 extern std::vector<bool>				*ph_passPhoIsoCorrMedium;
 extern std::vector<bool>				*ph_passPhoIsoCorrTight;
 extern std::vector<bool>				*ph_truthMatch_el;
 extern std::vector<float>				*ph_truthMinDR_el;
 extern std::vector<float>				*ph_truthMatchPt_el;
 extern std::vector<bool>				*ph_truthMatch_ph;
 extern std::vector<float>				*ph_truthMinDR_ph;
 extern std::vector<float>				*ph_truthMatchPt_ph;
 extern std::vector<int>				*ph_truthMatchMotherPID_ph;
 extern std::vector<bool>				*ph_hasSLConv;
 extern std::vector<bool>				*ph_pass_mva_presel;
 extern std::vector<float>				*ph_mvascore;
 extern std::vector<bool>				*ph_IsEB;
 extern std::vector<bool>				*ph_IsEE;
 extern std::vector<float>				*jet_pt;
 extern std::vector<float>				*jet_eta;
 extern std::vector<float>				*jet_phi;
 extern std::vector<float>				*jet_e;
 extern Float_t				PUWeight;
 extern Bool_t				isBlinded;
 extern Float_t				EventWeight;
 extern Int_t				mu_pt25_n;
 extern Int_t				mu_passtrig_n;
 extern Int_t				mu_passtrig25_n;
 extern Int_t				el_pt25_n;
 extern Int_t				el_passtrig_n;
 extern Int_t				el_passtrig28_n;
 extern Int_t				ph_mediumNoSIEIE_n;
 extern Int_t				ph_medium_n;
 extern Int_t				ph_mediumNoEleVeto_n;
 extern Int_t				ph_mediumNoSIEIENoEleVeto_n;
 extern Int_t				ph_mediumNoIso_n;
 extern Int_t				ph_mediumNoChIso_n;
 extern Int_t				ph_mediumNoNeuIso_n;
 extern Int_t				ph_mediumNoPhoIso_n;
 extern Int_t				ph_mediumNoChIsoNoNeuIso_n;
 extern Int_t				ph_mediumNoChIsoNoPhoIso_n;
 extern Int_t				ph_mediumNoNeuIsoNoPhoIso_n;
 extern std::vector<bool>				*ph_trigMatch_el;
 extern Float_t				leadPhot_pt;
 extern Float_t				sublPhot_pt;
 extern Float_t				leadPhot_lepDR;
 extern Float_t				sublPhot_lepDR;
 extern Float_t				ph_phDR;
 extern Float_t				phPhot_lepDR;
 extern Float_t				leadPhot_lepDPhi;
 extern Float_t				sublPhot_lepDPhi;
 extern Float_t				ph_phDPhi;
 extern Float_t				phPhot_lepDPhi;
 extern Float_t				dphi_met_lep1;
 extern Float_t				dphi_met_lep2;
 extern Float_t				dphi_met_ph1;
 extern Float_t				dphi_met_ph2;
 extern Float_t				mt_lep_met;
 extern Float_t				mt_lepph1_met;
 extern Float_t				mt_lepph2_met;
 extern Float_t				mt_lepphph_met;
 extern Float_t				m_leplep;
 extern Float_t				m_lepph1;
 extern Float_t				m_lepph2;
 extern Float_t				m_leplepph;
 extern Float_t				m_lepphph;
 extern Float_t				m_phph;
 extern Float_t				m_leplepZ;
 extern Float_t				m_3lep;
 extern Float_t				m_4lep;
 extern Float_t				pt_phph;
 extern Float_t				pt_leplep;
 extern Float_t				pt_lepph1;
 extern Float_t				pt_lepph2;
 extern Float_t				pt_lepphph;
 extern Float_t				pt_leplepph;
 extern Float_t				pt_secondLepton;
 extern Float_t				pt_thirdLepton;
 extern Float_t				leadPhot_leadLepDR;
 extern Float_t				leadPhot_sublLepDR;
 extern Float_t				sublPhot_leadLepDR;
 extern Float_t				sublPhot_sublLepDR;
 extern Float_t				m_nearestToZ;
 extern Float_t				m_minZdifflepph;
 extern Int_t				truelep_n;
 extern Int_t				trueph_n;
 extern Int_t				trueph_wmother_n;
 extern Int_t				truegenph_n;
 extern Int_t				truegenphpt15_n;
 extern std::vector<float>				*truelep_pt;
 extern std::vector<float>				*truelep_eta;
 extern std::vector<float>				*truelep_phi;
 extern std::vector<float>				*truelep_e;
 extern std::vector<bool>				*truelep_isElec;
 extern std::vector<bool>				*truelep_isMuon;
 extern std::vector<int>				*truelep_motherPID;
 extern std::vector<float>				*trueph_pt;
 extern std::vector<float>				*trueph_eta;
 extern std::vector<float>				*trueph_phi;
 extern std::vector<int>				*trueph_motherPID;
 extern std::vector<int>				*trueph_parentage;
 extern std::vector<float>				*trueph_nearestLepDR;
 extern std::vector<float>				*trueph_nearestQrkDR;
 extern Float_t				trueleadlep_pt;
 extern Float_t				truesubllep_pt;
 extern Float_t				trueleadlep_leadPhotDR;
 extern Float_t				trueleadlep_sublPhotDR;
 extern Float_t				truesubllep_leadPhotDR;
 extern Float_t				truesubllep_sublPhotDR;
};
#endif
