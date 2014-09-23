#include <algorithm>
#include <iostream>
#include "TTree.h"
#include "TChain.h"
#include "include/BranchInit.h"
#include "include/BranchDefs.h"

namespace IN {
 Int_t				nVtx;
 Int_t				nVtxBS;
 Int_t				nMC;
 std::vector<int>				*mcPID;
 std::vector<float>				*mcPt;
 std::vector<float>				*mcEta;
 std::vector<float>				*mcPhi;
 std::vector<float>				*mcE;
 std::vector<int>				*mcGMomPID;
 std::vector<int>				*mcMomPID;
 std::vector<int>				*mcParentage;
 std::vector<int>				*mcStatus;
 std::vector<int>				*nPU;
 std::vector<float>				*puTrue;
 Float_t				pfMET;
 Float_t				pfMETPhi;
 Float_t				pfMETsumEt;
 Float_t				pfMETmEtSig;
 Float_t				pfMETSig;
 Float_t				recoPfMET;
 Float_t				recoPfMETPhi;
 Float_t				recoPfMETsumEt;
 Float_t				recoPfMETmEtSig;
 Float_t				recoPfMETSig;
 Float_t				rho2012;
 Int_t				el_n;
 Int_t				mu_n;
 Int_t				ph_n;
 Int_t				jet_n;
 Int_t				vtx_n;
 std::vector<float>				*el_pt;
 std::vector<float>				*el_eta;
 std::vector<float>				*el_sceta;
 std::vector<float>				*el_phi;
 std::vector<float>				*el_e;
 std::vector<float>				*el_pt_uncorr;
 std::vector<float>				*el_mva_trig;
 std::vector<float>				*el_mva_nontrig;
 std::vector<float>				*el_d0pv;
 std::vector<float>				*el_z0pv;
 std::vector<float>				*el_sigmaIEIE;
 std::vector<float>				*el_pfiso30;
 std::vector<float>				*el_pfiso40;
 std::vector<bool>				*el_triggerMatch;
 std::vector<bool>				*el_hasMatchedConv;
 std::vector<bool>				*el_passTight;
 std::vector<bool>				*el_passMedium;
 std::vector<bool>				*el_passLoose;
 std::vector<bool>				*el_passVeryLoose;
 std::vector<bool>				*el_passTightTrig;
 std::vector<bool>				*el_passMvaTrig;
 std::vector<bool>				*el_passMvaNonTrig;
 std::vector<bool>				*el_truthMatch_el;
 std::vector<float>				*el_truthMinDR_el;
 std::vector<float>				*el_truthMatchPt_el;
 std::vector<float>				*mu_pt;
 std::vector<float>				*mu_eta;
 std::vector<float>				*mu_phi;
 std::vector<float>				*mu_e;
 std::vector<float>				*mu_pt_uncorr;
 std::vector<float>				*mu_pfIso_ch;
 std::vector<float>				*mu_pfIso_nh;
 std::vector<float>				*mu_pfIso_pho;
 std::vector<float>				*mu_pfIso_pu;
 std::vector<float>				*mu_corrIso;
 std::vector<bool>				*mu_triggerMatch;
 std::vector<bool>				*mu_truthMatch;
 std::vector<float>				*mu_truthMinDR;
 std::vector<float>				*ph_pt;
 std::vector<float>				*ph_eta;
 std::vector<float>				*ph_sceta;
 std::vector<float>				*ph_phi;
 std::vector<float>				*ph_e;
 std::vector<float>				*ph_HoverE;
 std::vector<float>				*ph_HoverE12;
 std::vector<float>				*ph_sigmaIEIE;
 std::vector<float>				*ph_sigmaIEIP;
 std::vector<float>				*ph_r9;
 std::vector<float>				*ph_E1x3;
 std::vector<float>				*ph_E2x2;
 std::vector<float>				*ph_E5x5;
 std::vector<float>				*ph_E2x5Max;
 std::vector<float>				*ph_SCetaWidth;
 std::vector<float>				*ph_SCphiWidth;
 std::vector<float>				*ph_ESEffSigmaRR;
 std::vector<float>				*ph_hcalIsoDR03;
 std::vector<float>				*ph_trkIsoHollowDR03;
 std::vector<float>				*ph_chgpfIsoDR02;
 std::vector<float>				*ph_pfChIsoWorst;
 std::vector<float>				*ph_chIso;
 std::vector<float>				*ph_neuIso;
 std::vector<float>				*ph_phoIso;
 std::vector<float>				*ph_chIsoCorr;
 std::vector<float>				*ph_neuIsoCorr;
 std::vector<float>				*ph_phoIsoCorr;
 std::vector<float>				*ph_SCRChIso;
 std::vector<float>				*ph_SCRPhoIso;
 std::vector<float>				*ph_SCRNeuIso;
 std::vector<float>				*ph_SCRChIso04;
 std::vector<float>				*ph_SCRPhoIso04;
 std::vector<float>				*ph_SCRNeuIso04;
 std::vector<float>				*ph_RandConeChIso;
 std::vector<float>				*ph_RandConePhoIso;
 std::vector<float>				*ph_RandConeNeuIso;
 std::vector<float>				*ph_RandConeChIso04;
 std::vector<float>				*ph_RandConePhoIso04;
 std::vector<float>				*ph_RandConeNeuIso04;
 std::vector<bool>				*ph_eleVeto;
 std::vector<bool>				*ph_hasPixSeed;
 std::vector<float>				*ph_drToTrk;
 std::vector<bool>				*ph_isConv;
 std::vector<int>				*ph_conv_nTrk;
 std::vector<float>				*ph_conv_vtx_x;
 std::vector<float>				*ph_conv_vtx_y;
 std::vector<float>				*ph_conv_vtx_z;
 std::vector<float>				*ph_conv_ptin1;
 std::vector<float>				*ph_conv_ptin2;
 std::vector<float>				*ph_conv_ptout1;
 std::vector<float>				*ph_conv_ptout2;
 std::vector<bool>				*ph_passTight;
 std::vector<bool>				*ph_passMedium;
 std::vector<bool>				*ph_passLoose;
 std::vector<bool>				*ph_passLooseNoSIEIE;
 std::vector<bool>				*ph_passHOverELoose;
 std::vector<bool>				*ph_passHOverEMedium;
 std::vector<bool>				*ph_passHOverETight;
 std::vector<bool>				*ph_passSIEIELoose;
 std::vector<bool>				*ph_passSIEIEMedium;
 std::vector<bool>				*ph_passSIEIETight;
 std::vector<bool>				*ph_passChIsoCorrLoose;
 std::vector<bool>				*ph_passChIsoCorrMedium;
 std::vector<bool>				*ph_passChIsoCorrTight;
 std::vector<bool>				*ph_passNeuIsoCorrLoose;
 std::vector<bool>				*ph_passNeuIsoCorrMedium;
 std::vector<bool>				*ph_passNeuIsoCorrTight;
 std::vector<bool>				*ph_passPhoIsoCorrLoose;
 std::vector<bool>				*ph_passPhoIsoCorrMedium;
 std::vector<bool>				*ph_passPhoIsoCorrTight;
 std::vector<bool>				*ph_truthMatch_el;
 std::vector<float>				*ph_truthMinDR_el;
 std::vector<float>				*ph_truthMatchPt_el;
 std::vector<bool>				*ph_truthMatch_ph;
 std::vector<float>				*ph_truthMinDR_ph;
 std::vector<float>				*ph_truthMatchPt_ph;
 std::vector<int>				*ph_truthMatchMotherPID_ph;
 std::vector<bool>				*ph_hasSLConv;
 std::vector<bool>				*ph_pass_mva_presel;
 std::vector<float>				*ph_mvascore;
 std::vector<bool>				*ph_IsEB;
 std::vector<bool>				*ph_IsEE;
 std::vector<float>				*jet_pt;
 std::vector<float>				*jet_eta;
 std::vector<float>				*jet_phi;
 std::vector<float>				*jet_e;
 Float_t				PUWeight;
 Bool_t				isBlinded;
 Float_t				EventWeight;
 Int_t				mu_pt25_n;
 Int_t				mu_passtrig_n;
 Int_t				mu_passtrig25_n;
 Int_t				el_pt25_n;
 Int_t				el_passtrig_n;
 Int_t				el_passtrig28_n;
 Int_t				ph_mediumNoSIEIE_n;
 Int_t				ph_medium_n;
 Int_t				ph_mediumNoEleVeto_n;
 Int_t				ph_mediumNoSIEIENoEleVeto_n;
 Int_t				ph_mediumNoIso_n;
 Int_t				ph_mediumNoChIso_n;
 Int_t				ph_mediumNoNeuIso_n;
 Int_t				ph_mediumNoPhoIso_n;
 Int_t				ph_mediumNoChIsoNoNeuIso_n;
 Int_t				ph_mediumNoChIsoNoPhoIso_n;
 Int_t				ph_mediumNoNeuIsoNoPhoIso_n;
 std::vector<bool>				*ph_trigMatch_el;
 Float_t				leadPhot_pt;
 Float_t				sublPhot_pt;
 Float_t				leadPhot_lepDR;
 Float_t				sublPhot_lepDR;
 Float_t				ph_phDR;
 Float_t				phPhot_lepDR;
 Float_t				leadPhot_lepDPhi;
 Float_t				sublPhot_lepDPhi;
 Float_t				ph_phDPhi;
 Float_t				phPhot_lepDPhi;
 Float_t				dphi_met_lep1;
 Float_t				dphi_met_lep2;
 Float_t				dphi_met_ph1;
 Float_t				dphi_met_ph2;
 Float_t				mt_lep_met;
 Float_t				mt_lepph1_met;
 Float_t				mt_lepph2_met;
 Float_t				mt_lepphph_met;
 Float_t				m_leplep;
 Float_t				m_lepph1;
 Float_t				m_lepph2;
 Float_t				m_leplepph;
 Float_t				m_lepphph;
 Float_t				m_phph;
 Float_t				m_leplepZ;
 Float_t				m_3lep;
 Float_t				m_4lep;
 Float_t				pt_phph;
 Float_t				pt_leplep;
 Float_t				pt_lepph1;
 Float_t				pt_lepph2;
 Float_t				pt_lepphph;
 Float_t				pt_leplepph;
 Float_t				pt_secondLepton;
 Float_t				pt_thirdLepton;
 Float_t				leadPhot_leadLepDR;
 Float_t				leadPhot_sublLepDR;
 Float_t				sublPhot_leadLepDR;
 Float_t				sublPhot_sublLepDR;
 Float_t				m_nearestToZ;
 Float_t				m_minZdifflepph;
 Int_t				truelep_n;
 Int_t				trueph_n;
 Int_t				trueph_wmother_n;
 Int_t				truegenph_n;
 Int_t				truegenphpt15_n;
 std::vector<float>				*truelep_pt;
 std::vector<float>				*truelep_eta;
 std::vector<float>				*truelep_phi;
 std::vector<float>				*truelep_e;
 std::vector<bool>				*truelep_isElec;
 std::vector<bool>				*truelep_isMuon;
 std::vector<int>				*truelep_motherPID;
 std::vector<float>				*trueph_pt;
 std::vector<float>				*trueph_eta;
 std::vector<float>				*trueph_phi;
 std::vector<int>				*trueph_motherPID;
 std::vector<int>				*trueph_parentage;
 std::vector<float>				*trueph_nearestLepDR;
 std::vector<float>				*trueph_nearestQrkDR;
 Float_t				trueleadlep_pt;
 Float_t				truesubllep_pt;
 Float_t				trueleadlep_leadPhotDR;
 Float_t				trueleadlep_sublPhotDR;
 Float_t				truesubllep_leadPhotDR;
 Float_t				truesubllep_sublPhotDR;
};
namespace OUT {
 Int_t				nVtx;
 Int_t				nVtxBS;
 Int_t				nMC;
 std::vector<int>				*mcPID;
 std::vector<float>				*mcPt;
 std::vector<float>				*mcEta;
 std::vector<float>				*mcPhi;
 std::vector<float>				*mcE;
 std::vector<int>				*mcGMomPID;
 std::vector<int>				*mcMomPID;
 std::vector<int>				*mcParentage;
 std::vector<int>				*mcStatus;
 std::vector<int>				*nPU;
 std::vector<float>				*puTrue;
 Float_t				pfMET;
 Float_t				pfMETPhi;
 Float_t				pfMETsumEt;
 Float_t				pfMETmEtSig;
 Float_t				pfMETSig;
 Float_t				recoPfMET;
 Float_t				recoPfMETPhi;
 Float_t				recoPfMETsumEt;
 Float_t				recoPfMETmEtSig;
 Float_t				recoPfMETSig;
 Float_t				rho2012;
 Int_t				el_n;
 Int_t				mu_n;
 Int_t				ph_n;
 Int_t				jet_n;
 Int_t				vtx_n;
 std::vector<float>				*el_pt;
 std::vector<float>				*el_eta;
 std::vector<float>				*el_sceta;
 std::vector<float>				*el_phi;
 std::vector<float>				*el_e;
 std::vector<float>				*el_pt_uncorr;
 std::vector<float>				*el_mva_trig;
 std::vector<float>				*el_mva_nontrig;
 std::vector<float>				*el_d0pv;
 std::vector<float>				*el_z0pv;
 std::vector<float>				*el_sigmaIEIE;
 std::vector<float>				*el_pfiso30;
 std::vector<float>				*el_pfiso40;
 std::vector<bool>				*el_triggerMatch;
 std::vector<bool>				*el_hasMatchedConv;
 std::vector<bool>				*el_passTight;
 std::vector<bool>				*el_passMedium;
 std::vector<bool>				*el_passLoose;
 std::vector<bool>				*el_passVeryLoose;
 std::vector<bool>				*el_passTightTrig;
 std::vector<bool>				*el_passMvaTrig;
 std::vector<bool>				*el_passMvaNonTrig;
 std::vector<bool>				*el_truthMatch_el;
 std::vector<float>				*el_truthMinDR_el;
 std::vector<float>				*el_truthMatchPt_el;
 std::vector<float>				*mu_pt;
 std::vector<float>				*mu_eta;
 std::vector<float>				*mu_phi;
 std::vector<float>				*mu_e;
 std::vector<float>				*mu_pt_uncorr;
 std::vector<float>				*mu_pfIso_ch;
 std::vector<float>				*mu_pfIso_nh;
 std::vector<float>				*mu_pfIso_pho;
 std::vector<float>				*mu_pfIso_pu;
 std::vector<float>				*mu_corrIso;
 std::vector<bool>				*mu_triggerMatch;
 std::vector<bool>				*mu_truthMatch;
 std::vector<float>				*mu_truthMinDR;
 std::vector<float>				*ph_pt;
 std::vector<float>				*ph_eta;
 std::vector<float>				*ph_sceta;
 std::vector<float>				*ph_phi;
 std::vector<float>				*ph_e;
 std::vector<float>				*ph_HoverE;
 std::vector<float>				*ph_HoverE12;
 std::vector<float>				*ph_sigmaIEIE;
 std::vector<float>				*ph_sigmaIEIP;
 std::vector<float>				*ph_r9;
 std::vector<float>				*ph_E1x3;
 std::vector<float>				*ph_E2x2;
 std::vector<float>				*ph_E5x5;
 std::vector<float>				*ph_E2x5Max;
 std::vector<float>				*ph_SCetaWidth;
 std::vector<float>				*ph_SCphiWidth;
 std::vector<float>				*ph_ESEffSigmaRR;
 std::vector<float>				*ph_hcalIsoDR03;
 std::vector<float>				*ph_trkIsoHollowDR03;
 std::vector<float>				*ph_chgpfIsoDR02;
 std::vector<float>				*ph_pfChIsoWorst;
 std::vector<float>				*ph_chIso;
 std::vector<float>				*ph_neuIso;
 std::vector<float>				*ph_phoIso;
 std::vector<float>				*ph_chIsoCorr;
 std::vector<float>				*ph_neuIsoCorr;
 std::vector<float>				*ph_phoIsoCorr;
 std::vector<float>				*ph_SCRChIso;
 std::vector<float>				*ph_SCRPhoIso;
 std::vector<float>				*ph_SCRNeuIso;
 std::vector<float>				*ph_SCRChIso04;
 std::vector<float>				*ph_SCRPhoIso04;
 std::vector<float>				*ph_SCRNeuIso04;
 std::vector<float>				*ph_RandConeChIso;
 std::vector<float>				*ph_RandConePhoIso;
 std::vector<float>				*ph_RandConeNeuIso;
 std::vector<float>				*ph_RandConeChIso04;
 std::vector<float>				*ph_RandConePhoIso04;
 std::vector<float>				*ph_RandConeNeuIso04;
 std::vector<bool>				*ph_eleVeto;
 std::vector<bool>				*ph_hasPixSeed;
 std::vector<float>				*ph_drToTrk;
 std::vector<bool>				*ph_isConv;
 std::vector<int>				*ph_conv_nTrk;
 std::vector<float>				*ph_conv_vtx_x;
 std::vector<float>				*ph_conv_vtx_y;
 std::vector<float>				*ph_conv_vtx_z;
 std::vector<float>				*ph_conv_ptin1;
 std::vector<float>				*ph_conv_ptin2;
 std::vector<float>				*ph_conv_ptout1;
 std::vector<float>				*ph_conv_ptout2;
 std::vector<bool>				*ph_passTight;
 std::vector<bool>				*ph_passMedium;
 std::vector<bool>				*ph_passLoose;
 std::vector<bool>				*ph_passLooseNoSIEIE;
 std::vector<bool>				*ph_passHOverELoose;
 std::vector<bool>				*ph_passHOverEMedium;
 std::vector<bool>				*ph_passHOverETight;
 std::vector<bool>				*ph_passSIEIELoose;
 std::vector<bool>				*ph_passSIEIEMedium;
 std::vector<bool>				*ph_passSIEIETight;
 std::vector<bool>				*ph_passChIsoCorrLoose;
 std::vector<bool>				*ph_passChIsoCorrMedium;
 std::vector<bool>				*ph_passChIsoCorrTight;
 std::vector<bool>				*ph_passNeuIsoCorrLoose;
 std::vector<bool>				*ph_passNeuIsoCorrMedium;
 std::vector<bool>				*ph_passNeuIsoCorrTight;
 std::vector<bool>				*ph_passPhoIsoCorrLoose;
 std::vector<bool>				*ph_passPhoIsoCorrMedium;
 std::vector<bool>				*ph_passPhoIsoCorrTight;
 std::vector<bool>				*ph_truthMatch_el;
 std::vector<float>				*ph_truthMinDR_el;
 std::vector<float>				*ph_truthMatchPt_el;
 std::vector<bool>				*ph_truthMatch_ph;
 std::vector<float>				*ph_truthMinDR_ph;
 std::vector<float>				*ph_truthMatchPt_ph;
 std::vector<int>				*ph_truthMatchMotherPID_ph;
 std::vector<bool>				*ph_hasSLConv;
 std::vector<bool>				*ph_pass_mva_presel;
 std::vector<float>				*ph_mvascore;
 std::vector<bool>				*ph_IsEB;
 std::vector<bool>				*ph_IsEE;
 std::vector<float>				*jet_pt;
 std::vector<float>				*jet_eta;
 std::vector<float>				*jet_phi;
 std::vector<float>				*jet_e;
 Float_t				PUWeight;
 Bool_t				isBlinded;
 Float_t				EventWeight;
 Int_t				mu_pt25_n;
 Int_t				mu_passtrig_n;
 Int_t				mu_passtrig25_n;
 Int_t				el_pt25_n;
 Int_t				el_passtrig_n;
 Int_t				el_passtrig28_n;
 Int_t				ph_mediumNoSIEIE_n;
 Int_t				ph_medium_n;
 Int_t				ph_mediumNoEleVeto_n;
 Int_t				ph_mediumNoSIEIENoEleVeto_n;
 Int_t				ph_mediumNoIso_n;
 Int_t				ph_mediumNoChIso_n;
 Int_t				ph_mediumNoNeuIso_n;
 Int_t				ph_mediumNoPhoIso_n;
 Int_t				ph_mediumNoChIsoNoNeuIso_n;
 Int_t				ph_mediumNoChIsoNoPhoIso_n;
 Int_t				ph_mediumNoNeuIsoNoPhoIso_n;
 std::vector<bool>				*ph_trigMatch_el;
 Float_t				leadPhot_pt;
 Float_t				sublPhot_pt;
 Float_t				leadPhot_lepDR;
 Float_t				sublPhot_lepDR;
 Float_t				ph_phDR;
 Float_t				phPhot_lepDR;
 Float_t				leadPhot_lepDPhi;
 Float_t				sublPhot_lepDPhi;
 Float_t				ph_phDPhi;
 Float_t				phPhot_lepDPhi;
 Float_t				dphi_met_lep1;
 Float_t				dphi_met_lep2;
 Float_t				dphi_met_ph1;
 Float_t				dphi_met_ph2;
 Float_t				mt_lep_met;
 Float_t				mt_lepph1_met;
 Float_t				mt_lepph2_met;
 Float_t				mt_lepphph_met;
 Float_t				m_leplep;
 Float_t				m_lepph1;
 Float_t				m_lepph2;
 Float_t				m_leplepph;
 Float_t				m_lepphph;
 Float_t				m_phph;
 Float_t				m_leplepZ;
 Float_t				m_3lep;
 Float_t				m_4lep;
 Float_t				pt_phph;
 Float_t				pt_leplep;
 Float_t				pt_lepph1;
 Float_t				pt_lepph2;
 Float_t				pt_lepphph;
 Float_t				pt_leplepph;
 Float_t				pt_secondLepton;
 Float_t				pt_thirdLepton;
 Float_t				leadPhot_leadLepDR;
 Float_t				leadPhot_sublLepDR;
 Float_t				sublPhot_leadLepDR;
 Float_t				sublPhot_sublLepDR;
 Float_t				m_nearestToZ;
 Float_t				m_minZdifflepph;
 Int_t				truelep_n;
 Int_t				trueph_n;
 Int_t				trueph_wmother_n;
 Int_t				truegenph_n;
 Int_t				truegenphpt15_n;
 std::vector<float>				*truelep_pt;
 std::vector<float>				*truelep_eta;
 std::vector<float>				*truelep_phi;
 std::vector<float>				*truelep_e;
 std::vector<bool>				*truelep_isElec;
 std::vector<bool>				*truelep_isMuon;
 std::vector<int>				*truelep_motherPID;
 std::vector<float>				*trueph_pt;
 std::vector<float>				*trueph_eta;
 std::vector<float>				*trueph_phi;
 std::vector<int>				*trueph_motherPID;
 std::vector<int>				*trueph_parentage;
 std::vector<float>				*trueph_nearestLepDR;
 std::vector<float>				*trueph_nearestQrkDR;
 Float_t				trueleadlep_pt;
 Float_t				truesubllep_pt;
 Float_t				trueleadlep_leadPhotDR;
 Float_t				trueleadlep_sublPhotDR;
 Float_t				truesubllep_leadPhotDR;
 Float_t				truesubllep_sublPhotDR;
};
void InitINTree( TChain * tree) {

  tree->SetBranchAddress("nVtx", &IN::nVtx);
  tree->SetBranchAddress("nVtxBS", &IN::nVtxBS);
  tree->SetBranchAddress("nMC", &IN::nMC);
  tree->SetBranchAddress("mcPID", &IN::mcPID);
  tree->SetBranchAddress("mcPt", &IN::mcPt);
  tree->SetBranchAddress("mcEta", &IN::mcEta);
  tree->SetBranchAddress("mcPhi", &IN::mcPhi);
  tree->SetBranchAddress("mcE", &IN::mcE);
  tree->SetBranchAddress("mcGMomPID", &IN::mcGMomPID);
  tree->SetBranchAddress("mcMomPID", &IN::mcMomPID);
  tree->SetBranchAddress("mcParentage", &IN::mcParentage);
  tree->SetBranchAddress("mcStatus", &IN::mcStatus);
  tree->SetBranchAddress("nPU", &IN::nPU);
  tree->SetBranchAddress("puTrue", &IN::puTrue);
  tree->SetBranchAddress("pfMET", &IN::pfMET);
  tree->SetBranchAddress("pfMETPhi", &IN::pfMETPhi);
  tree->SetBranchAddress("pfMETsumEt", &IN::pfMETsumEt);
  tree->SetBranchAddress("pfMETmEtSig", &IN::pfMETmEtSig);
  tree->SetBranchAddress("pfMETSig", &IN::pfMETSig);
  tree->SetBranchAddress("recoPfMET", &IN::recoPfMET);
  tree->SetBranchAddress("recoPfMETPhi", &IN::recoPfMETPhi);
  tree->SetBranchAddress("recoPfMETsumEt", &IN::recoPfMETsumEt);
  tree->SetBranchAddress("recoPfMETmEtSig", &IN::recoPfMETmEtSig);
  tree->SetBranchAddress("recoPfMETSig", &IN::recoPfMETSig);
  tree->SetBranchAddress("rho2012", &IN::rho2012);
  tree->SetBranchAddress("el_n", &IN::el_n);
  tree->SetBranchAddress("mu_n", &IN::mu_n);
  tree->SetBranchAddress("ph_n", &IN::ph_n);
  tree->SetBranchAddress("jet_n", &IN::jet_n);
  tree->SetBranchAddress("vtx_n", &IN::vtx_n);
  tree->SetBranchAddress("el_pt", &IN::el_pt);
  tree->SetBranchAddress("el_eta", &IN::el_eta);
  tree->SetBranchAddress("el_sceta", &IN::el_sceta);
  tree->SetBranchAddress("el_phi", &IN::el_phi);
  tree->SetBranchAddress("el_e", &IN::el_e);
  tree->SetBranchAddress("el_pt_uncorr", &IN::el_pt_uncorr);
  tree->SetBranchAddress("el_mva_trig", &IN::el_mva_trig);
  tree->SetBranchAddress("el_mva_nontrig", &IN::el_mva_nontrig);
  tree->SetBranchAddress("el_d0pv", &IN::el_d0pv);
  tree->SetBranchAddress("el_z0pv", &IN::el_z0pv);
  tree->SetBranchAddress("el_sigmaIEIE", &IN::el_sigmaIEIE);
  tree->SetBranchAddress("el_pfiso30", &IN::el_pfiso30);
  tree->SetBranchAddress("el_pfiso40", &IN::el_pfiso40);
  tree->SetBranchAddress("el_triggerMatch", &IN::el_triggerMatch);
  tree->SetBranchAddress("el_hasMatchedConv", &IN::el_hasMatchedConv);
  tree->SetBranchAddress("el_passTight", &IN::el_passTight);
  tree->SetBranchAddress("el_passMedium", &IN::el_passMedium);
  tree->SetBranchAddress("el_passLoose", &IN::el_passLoose);
  tree->SetBranchAddress("el_passVeryLoose", &IN::el_passVeryLoose);
  tree->SetBranchAddress("el_passTightTrig", &IN::el_passTightTrig);
  tree->SetBranchAddress("el_passMvaTrig", &IN::el_passMvaTrig);
  tree->SetBranchAddress("el_passMvaNonTrig", &IN::el_passMvaNonTrig);
  tree->SetBranchAddress("el_truthMatch_el", &IN::el_truthMatch_el);
  tree->SetBranchAddress("el_truthMinDR_el", &IN::el_truthMinDR_el);
  tree->SetBranchAddress("el_truthMatchPt_el", &IN::el_truthMatchPt_el);
  tree->SetBranchAddress("mu_pt", &IN::mu_pt);
  tree->SetBranchAddress("mu_eta", &IN::mu_eta);
  tree->SetBranchAddress("mu_phi", &IN::mu_phi);
  tree->SetBranchAddress("mu_e", &IN::mu_e);
  tree->SetBranchAddress("mu_pt_uncorr", &IN::mu_pt_uncorr);
  tree->SetBranchAddress("mu_pfIso_ch", &IN::mu_pfIso_ch);
  tree->SetBranchAddress("mu_pfIso_nh", &IN::mu_pfIso_nh);
  tree->SetBranchAddress("mu_pfIso_pho", &IN::mu_pfIso_pho);
  tree->SetBranchAddress("mu_pfIso_pu", &IN::mu_pfIso_pu);
  tree->SetBranchAddress("mu_corrIso", &IN::mu_corrIso);
  tree->SetBranchAddress("mu_triggerMatch", &IN::mu_triggerMatch);
  tree->SetBranchAddress("mu_truthMatch", &IN::mu_truthMatch);
  tree->SetBranchAddress("mu_truthMinDR", &IN::mu_truthMinDR);
  tree->SetBranchAddress("ph_pt", &IN::ph_pt);
  tree->SetBranchAddress("ph_eta", &IN::ph_eta);
  tree->SetBranchAddress("ph_sceta", &IN::ph_sceta);
  tree->SetBranchAddress("ph_phi", &IN::ph_phi);
  tree->SetBranchAddress("ph_e", &IN::ph_e);
  tree->SetBranchAddress("ph_HoverE", &IN::ph_HoverE);
  tree->SetBranchAddress("ph_HoverE12", &IN::ph_HoverE12);
  tree->SetBranchAddress("ph_sigmaIEIE", &IN::ph_sigmaIEIE);
  tree->SetBranchAddress("ph_sigmaIEIP", &IN::ph_sigmaIEIP);
  tree->SetBranchAddress("ph_r9", &IN::ph_r9);
  tree->SetBranchAddress("ph_E1x3", &IN::ph_E1x3);
  tree->SetBranchAddress("ph_E2x2", &IN::ph_E2x2);
  tree->SetBranchAddress("ph_E5x5", &IN::ph_E5x5);
  tree->SetBranchAddress("ph_E2x5Max", &IN::ph_E2x5Max);
  tree->SetBranchAddress("ph_SCetaWidth", &IN::ph_SCetaWidth);
  tree->SetBranchAddress("ph_SCphiWidth", &IN::ph_SCphiWidth);
  tree->SetBranchAddress("ph_ESEffSigmaRR", &IN::ph_ESEffSigmaRR);
  tree->SetBranchAddress("ph_hcalIsoDR03", &IN::ph_hcalIsoDR03);
  tree->SetBranchAddress("ph_trkIsoHollowDR03", &IN::ph_trkIsoHollowDR03);
  tree->SetBranchAddress("ph_chgpfIsoDR02", &IN::ph_chgpfIsoDR02);
  tree->SetBranchAddress("ph_pfChIsoWorst", &IN::ph_pfChIsoWorst);
  tree->SetBranchAddress("ph_chIso", &IN::ph_chIso);
  tree->SetBranchAddress("ph_neuIso", &IN::ph_neuIso);
  tree->SetBranchAddress("ph_phoIso", &IN::ph_phoIso);
  tree->SetBranchAddress("ph_chIsoCorr", &IN::ph_chIsoCorr);
  tree->SetBranchAddress("ph_neuIsoCorr", &IN::ph_neuIsoCorr);
  tree->SetBranchAddress("ph_phoIsoCorr", &IN::ph_phoIsoCorr);
  tree->SetBranchAddress("ph_SCRChIso", &IN::ph_SCRChIso);
  tree->SetBranchAddress("ph_SCRPhoIso", &IN::ph_SCRPhoIso);
  tree->SetBranchAddress("ph_SCRNeuIso", &IN::ph_SCRNeuIso);
  tree->SetBranchAddress("ph_SCRChIso04", &IN::ph_SCRChIso04);
  tree->SetBranchAddress("ph_SCRPhoIso04", &IN::ph_SCRPhoIso04);
  tree->SetBranchAddress("ph_SCRNeuIso04", &IN::ph_SCRNeuIso04);
  tree->SetBranchAddress("ph_RandConeChIso", &IN::ph_RandConeChIso);
  tree->SetBranchAddress("ph_RandConePhoIso", &IN::ph_RandConePhoIso);
  tree->SetBranchAddress("ph_RandConeNeuIso", &IN::ph_RandConeNeuIso);
  tree->SetBranchAddress("ph_RandConeChIso04", &IN::ph_RandConeChIso04);
  tree->SetBranchAddress("ph_RandConePhoIso04", &IN::ph_RandConePhoIso04);
  tree->SetBranchAddress("ph_RandConeNeuIso04", &IN::ph_RandConeNeuIso04);
  tree->SetBranchAddress("ph_eleVeto", &IN::ph_eleVeto);
  tree->SetBranchAddress("ph_hasPixSeed", &IN::ph_hasPixSeed);
  tree->SetBranchAddress("ph_drToTrk", &IN::ph_drToTrk);
  tree->SetBranchAddress("ph_isConv", &IN::ph_isConv);
  tree->SetBranchAddress("ph_conv_nTrk", &IN::ph_conv_nTrk);
  tree->SetBranchAddress("ph_conv_vtx_x", &IN::ph_conv_vtx_x);
  tree->SetBranchAddress("ph_conv_vtx_y", &IN::ph_conv_vtx_y);
  tree->SetBranchAddress("ph_conv_vtx_z", &IN::ph_conv_vtx_z);
  tree->SetBranchAddress("ph_conv_ptin1", &IN::ph_conv_ptin1);
  tree->SetBranchAddress("ph_conv_ptin2", &IN::ph_conv_ptin2);
  tree->SetBranchAddress("ph_conv_ptout1", &IN::ph_conv_ptout1);
  tree->SetBranchAddress("ph_conv_ptout2", &IN::ph_conv_ptout2);
  tree->SetBranchAddress("ph_passTight", &IN::ph_passTight);
  tree->SetBranchAddress("ph_passMedium", &IN::ph_passMedium);
  tree->SetBranchAddress("ph_passLoose", &IN::ph_passLoose);
  tree->SetBranchAddress("ph_passLooseNoSIEIE", &IN::ph_passLooseNoSIEIE);
  tree->SetBranchAddress("ph_passHOverELoose", &IN::ph_passHOverELoose);
  tree->SetBranchAddress("ph_passHOverEMedium", &IN::ph_passHOverEMedium);
  tree->SetBranchAddress("ph_passHOverETight", &IN::ph_passHOverETight);
  tree->SetBranchAddress("ph_passSIEIELoose", &IN::ph_passSIEIELoose);
  tree->SetBranchAddress("ph_passSIEIEMedium", &IN::ph_passSIEIEMedium);
  tree->SetBranchAddress("ph_passSIEIETight", &IN::ph_passSIEIETight);
  tree->SetBranchAddress("ph_passChIsoCorrLoose", &IN::ph_passChIsoCorrLoose);
  tree->SetBranchAddress("ph_passChIsoCorrMedium", &IN::ph_passChIsoCorrMedium);
  tree->SetBranchAddress("ph_passChIsoCorrTight", &IN::ph_passChIsoCorrTight);
  tree->SetBranchAddress("ph_passNeuIsoCorrLoose", &IN::ph_passNeuIsoCorrLoose);
  tree->SetBranchAddress("ph_passNeuIsoCorrMedium", &IN::ph_passNeuIsoCorrMedium);
  tree->SetBranchAddress("ph_passNeuIsoCorrTight", &IN::ph_passNeuIsoCorrTight);
  tree->SetBranchAddress("ph_passPhoIsoCorrLoose", &IN::ph_passPhoIsoCorrLoose);
  tree->SetBranchAddress("ph_passPhoIsoCorrMedium", &IN::ph_passPhoIsoCorrMedium);
  tree->SetBranchAddress("ph_passPhoIsoCorrTight", &IN::ph_passPhoIsoCorrTight);
  tree->SetBranchAddress("ph_truthMatch_el", &IN::ph_truthMatch_el);
  tree->SetBranchAddress("ph_truthMinDR_el", &IN::ph_truthMinDR_el);
  tree->SetBranchAddress("ph_truthMatchPt_el", &IN::ph_truthMatchPt_el);
  tree->SetBranchAddress("ph_truthMatch_ph", &IN::ph_truthMatch_ph);
  tree->SetBranchAddress("ph_truthMinDR_ph", &IN::ph_truthMinDR_ph);
  tree->SetBranchAddress("ph_truthMatchPt_ph", &IN::ph_truthMatchPt_ph);
  tree->SetBranchAddress("ph_truthMatchMotherPID_ph", &IN::ph_truthMatchMotherPID_ph);
  tree->SetBranchAddress("ph_hasSLConv", &IN::ph_hasSLConv);
  tree->SetBranchAddress("ph_pass_mva_presel", &IN::ph_pass_mva_presel);
  tree->SetBranchAddress("ph_mvascore", &IN::ph_mvascore);
  tree->SetBranchAddress("ph_IsEB", &IN::ph_IsEB);
  tree->SetBranchAddress("ph_IsEE", &IN::ph_IsEE);
  tree->SetBranchAddress("jet_pt", &IN::jet_pt);
  tree->SetBranchAddress("jet_eta", &IN::jet_eta);
  tree->SetBranchAddress("jet_phi", &IN::jet_phi);
  tree->SetBranchAddress("jet_e", &IN::jet_e);
  tree->SetBranchAddress("PUWeight", &IN::PUWeight);
  tree->SetBranchAddress("isBlinded", &IN::isBlinded);
  tree->SetBranchAddress("EventWeight", &IN::EventWeight);
  tree->SetBranchAddress("mu_pt25_n", &IN::mu_pt25_n);
  tree->SetBranchAddress("mu_passtrig_n", &IN::mu_passtrig_n);
  tree->SetBranchAddress("mu_passtrig25_n", &IN::mu_passtrig25_n);
  tree->SetBranchAddress("el_pt25_n", &IN::el_pt25_n);
  tree->SetBranchAddress("el_passtrig_n", &IN::el_passtrig_n);
  tree->SetBranchAddress("el_passtrig28_n", &IN::el_passtrig28_n);
  tree->SetBranchAddress("ph_mediumNoSIEIE_n", &IN::ph_mediumNoSIEIE_n);
  tree->SetBranchAddress("ph_medium_n", &IN::ph_medium_n);
  tree->SetBranchAddress("ph_mediumNoEleVeto_n", &IN::ph_mediumNoEleVeto_n);
  tree->SetBranchAddress("ph_mediumNoSIEIENoEleVeto_n", &IN::ph_mediumNoSIEIENoEleVeto_n);
  tree->SetBranchAddress("ph_mediumNoIso_n", &IN::ph_mediumNoIso_n);
  tree->SetBranchAddress("ph_mediumNoChIso_n", &IN::ph_mediumNoChIso_n);
  tree->SetBranchAddress("ph_mediumNoNeuIso_n", &IN::ph_mediumNoNeuIso_n);
  tree->SetBranchAddress("ph_mediumNoPhoIso_n", &IN::ph_mediumNoPhoIso_n);
  tree->SetBranchAddress("ph_mediumNoChIsoNoNeuIso_n", &IN::ph_mediumNoChIsoNoNeuIso_n);
  tree->SetBranchAddress("ph_mediumNoChIsoNoPhoIso_n", &IN::ph_mediumNoChIsoNoPhoIso_n);
  tree->SetBranchAddress("ph_mediumNoNeuIsoNoPhoIso_n", &IN::ph_mediumNoNeuIsoNoPhoIso_n);
  tree->SetBranchAddress("ph_trigMatch_el", &IN::ph_trigMatch_el);
  tree->SetBranchAddress("leadPhot_pt", &IN::leadPhot_pt);
  tree->SetBranchAddress("sublPhot_pt", &IN::sublPhot_pt);
  tree->SetBranchAddress("leadPhot_lepDR", &IN::leadPhot_lepDR);
  tree->SetBranchAddress("sublPhot_lepDR", &IN::sublPhot_lepDR);
  tree->SetBranchAddress("ph_phDR", &IN::ph_phDR);
  tree->SetBranchAddress("phPhot_lepDR", &IN::phPhot_lepDR);
  tree->SetBranchAddress("leadPhot_lepDPhi", &IN::leadPhot_lepDPhi);
  tree->SetBranchAddress("sublPhot_lepDPhi", &IN::sublPhot_lepDPhi);
  tree->SetBranchAddress("ph_phDPhi", &IN::ph_phDPhi);
  tree->SetBranchAddress("phPhot_lepDPhi", &IN::phPhot_lepDPhi);
  tree->SetBranchAddress("dphi_met_lep1", &IN::dphi_met_lep1);
  tree->SetBranchAddress("dphi_met_lep2", &IN::dphi_met_lep2);
  tree->SetBranchAddress("dphi_met_ph1", &IN::dphi_met_ph1);
  tree->SetBranchAddress("dphi_met_ph2", &IN::dphi_met_ph2);
  tree->SetBranchAddress("mt_lep_met", &IN::mt_lep_met);
  tree->SetBranchAddress("mt_lepph1_met", &IN::mt_lepph1_met);
  tree->SetBranchAddress("mt_lepph2_met", &IN::mt_lepph2_met);
  tree->SetBranchAddress("mt_lepphph_met", &IN::mt_lepphph_met);
  tree->SetBranchAddress("m_leplep", &IN::m_leplep);
  tree->SetBranchAddress("m_lepph1", &IN::m_lepph1);
  tree->SetBranchAddress("m_lepph2", &IN::m_lepph2);
  tree->SetBranchAddress("m_leplepph", &IN::m_leplepph);
  tree->SetBranchAddress("m_lepphph", &IN::m_lepphph);
  tree->SetBranchAddress("m_phph", &IN::m_phph);
  tree->SetBranchAddress("m_leplepZ", &IN::m_leplepZ);
  tree->SetBranchAddress("m_3lep", &IN::m_3lep);
  tree->SetBranchAddress("m_4lep", &IN::m_4lep);
  tree->SetBranchAddress("pt_phph", &IN::pt_phph);
  tree->SetBranchAddress("pt_leplep", &IN::pt_leplep);
  tree->SetBranchAddress("pt_lepph1", &IN::pt_lepph1);
  tree->SetBranchAddress("pt_lepph2", &IN::pt_lepph2);
  tree->SetBranchAddress("pt_lepphph", &IN::pt_lepphph);
  tree->SetBranchAddress("pt_leplepph", &IN::pt_leplepph);
  tree->SetBranchAddress("pt_secondLepton", &IN::pt_secondLepton);
  tree->SetBranchAddress("pt_thirdLepton", &IN::pt_thirdLepton);
  tree->SetBranchAddress("leadPhot_leadLepDR", &IN::leadPhot_leadLepDR);
  tree->SetBranchAddress("leadPhot_sublLepDR", &IN::leadPhot_sublLepDR);
  tree->SetBranchAddress("sublPhot_leadLepDR", &IN::sublPhot_leadLepDR);
  tree->SetBranchAddress("sublPhot_sublLepDR", &IN::sublPhot_sublLepDR);
  tree->SetBranchAddress("m_nearestToZ", &IN::m_nearestToZ);
  tree->SetBranchAddress("m_minZdifflepph", &IN::m_minZdifflepph);
  tree->SetBranchAddress("truelep_n", &IN::truelep_n);
  tree->SetBranchAddress("trueph_n", &IN::trueph_n);
  tree->SetBranchAddress("trueph_wmother_n", &IN::trueph_wmother_n);
  tree->SetBranchAddress("truegenph_n", &IN::truegenph_n);
  tree->SetBranchAddress("truegenphpt15_n", &IN::truegenphpt15_n);
  tree->SetBranchAddress("truelep_pt", &IN::truelep_pt);
  tree->SetBranchAddress("truelep_eta", &IN::truelep_eta);
  tree->SetBranchAddress("truelep_phi", &IN::truelep_phi);
  tree->SetBranchAddress("truelep_e", &IN::truelep_e);
  tree->SetBranchAddress("truelep_isElec", &IN::truelep_isElec);
  tree->SetBranchAddress("truelep_isMuon", &IN::truelep_isMuon);
  tree->SetBranchAddress("truelep_motherPID", &IN::truelep_motherPID);
  tree->SetBranchAddress("trueph_pt", &IN::trueph_pt);
  tree->SetBranchAddress("trueph_eta", &IN::trueph_eta);
  tree->SetBranchAddress("trueph_phi", &IN::trueph_phi);
  tree->SetBranchAddress("trueph_motherPID", &IN::trueph_motherPID);
  tree->SetBranchAddress("trueph_parentage", &IN::trueph_parentage);
  tree->SetBranchAddress("trueph_nearestLepDR", &IN::trueph_nearestLepDR);
  tree->SetBranchAddress("trueph_nearestQrkDR", &IN::trueph_nearestQrkDR);
  tree->SetBranchAddress("trueleadlep_pt", &IN::trueleadlep_pt);
  tree->SetBranchAddress("truesubllep_pt", &IN::truesubllep_pt);
  tree->SetBranchAddress("trueleadlep_leadPhotDR", &IN::trueleadlep_leadPhotDR);
  tree->SetBranchAddress("trueleadlep_sublPhotDR", &IN::trueleadlep_sublPhotDR);
  tree->SetBranchAddress("truesubllep_leadPhotDR", &IN::truesubllep_leadPhotDR);
  tree->SetBranchAddress("truesubllep_sublPhotDR", &IN::truesubllep_sublPhotDR);
};

void InitOUTTree( TTree * tree ) {
  tree->Branch("nVtx", &OUT::nVtx, "nVtx/I");
  tree->Branch("nVtxBS", &OUT::nVtxBS, "nVtxBS/I");
  tree->Branch("nMC", &OUT::nMC, "nMC/I");
  tree->Branch("mcPID", &OUT::mcPID);
  tree->Branch("mcPt", &OUT::mcPt);
  tree->Branch("mcEta", &OUT::mcEta);
  tree->Branch("mcPhi", &OUT::mcPhi);
  tree->Branch("mcE", &OUT::mcE);
  tree->Branch("mcGMomPID", &OUT::mcGMomPID);
  tree->Branch("mcMomPID", &OUT::mcMomPID);
  tree->Branch("mcParentage", &OUT::mcParentage);
  tree->Branch("mcStatus", &OUT::mcStatus);
  tree->Branch("nPU", &OUT::nPU);
  tree->Branch("puTrue", &OUT::puTrue);
  tree->Branch("pfMET", &OUT::pfMET, "pfMET/F");
  tree->Branch("pfMETPhi", &OUT::pfMETPhi, "pfMETPhi/F");
  tree->Branch("pfMETsumEt", &OUT::pfMETsumEt, "pfMETsumEt/F");
  tree->Branch("pfMETmEtSig", &OUT::pfMETmEtSig, "pfMETmEtSig/F");
  tree->Branch("pfMETSig", &OUT::pfMETSig, "pfMETSig/F");
  tree->Branch("recoPfMET", &OUT::recoPfMET, "recoPfMET/F");
  tree->Branch("recoPfMETPhi", &OUT::recoPfMETPhi, "recoPfMETPhi/F");
  tree->Branch("recoPfMETsumEt", &OUT::recoPfMETsumEt, "recoPfMETsumEt/F");
  tree->Branch("recoPfMETmEtSig", &OUT::recoPfMETmEtSig, "recoPfMETmEtSig/F");
  tree->Branch("recoPfMETSig", &OUT::recoPfMETSig, "recoPfMETSig/F");
  tree->Branch("rho2012", &OUT::rho2012, "rho2012/F");
  tree->Branch("el_n", &OUT::el_n, "el_n/I");
  tree->Branch("mu_n", &OUT::mu_n, "mu_n/I");
  tree->Branch("ph_n", &OUT::ph_n, "ph_n/I");
  tree->Branch("jet_n", &OUT::jet_n, "jet_n/I");
  tree->Branch("vtx_n", &OUT::vtx_n, "vtx_n/I");
  tree->Branch("el_pt", &OUT::el_pt);
  tree->Branch("el_eta", &OUT::el_eta);
  tree->Branch("el_sceta", &OUT::el_sceta);
  tree->Branch("el_phi", &OUT::el_phi);
  tree->Branch("el_e", &OUT::el_e);
  tree->Branch("el_pt_uncorr", &OUT::el_pt_uncorr);
  tree->Branch("el_mva_trig", &OUT::el_mva_trig);
  tree->Branch("el_mva_nontrig", &OUT::el_mva_nontrig);
  tree->Branch("el_d0pv", &OUT::el_d0pv);
  tree->Branch("el_z0pv", &OUT::el_z0pv);
  tree->Branch("el_sigmaIEIE", &OUT::el_sigmaIEIE);
  tree->Branch("el_pfiso30", &OUT::el_pfiso30);
  tree->Branch("el_pfiso40", &OUT::el_pfiso40);
  tree->Branch("el_triggerMatch", &OUT::el_triggerMatch);
  tree->Branch("el_hasMatchedConv", &OUT::el_hasMatchedConv);
  tree->Branch("el_passTight", &OUT::el_passTight);
  tree->Branch("el_passMedium", &OUT::el_passMedium);
  tree->Branch("el_passLoose", &OUT::el_passLoose);
  tree->Branch("el_passVeryLoose", &OUT::el_passVeryLoose);
  tree->Branch("el_passTightTrig", &OUT::el_passTightTrig);
  tree->Branch("el_passMvaTrig", &OUT::el_passMvaTrig);
  tree->Branch("el_passMvaNonTrig", &OUT::el_passMvaNonTrig);
  tree->Branch("el_truthMatch_el", &OUT::el_truthMatch_el);
  tree->Branch("el_truthMinDR_el", &OUT::el_truthMinDR_el);
  tree->Branch("el_truthMatchPt_el", &OUT::el_truthMatchPt_el);
  tree->Branch("mu_pt", &OUT::mu_pt);
  tree->Branch("mu_eta", &OUT::mu_eta);
  tree->Branch("mu_phi", &OUT::mu_phi);
  tree->Branch("mu_e", &OUT::mu_e);
  tree->Branch("mu_pt_uncorr", &OUT::mu_pt_uncorr);
  tree->Branch("mu_pfIso_ch", &OUT::mu_pfIso_ch);
  tree->Branch("mu_pfIso_nh", &OUT::mu_pfIso_nh);
  tree->Branch("mu_pfIso_pho", &OUT::mu_pfIso_pho);
  tree->Branch("mu_pfIso_pu", &OUT::mu_pfIso_pu);
  tree->Branch("mu_corrIso", &OUT::mu_corrIso);
  tree->Branch("mu_triggerMatch", &OUT::mu_triggerMatch);
  tree->Branch("mu_truthMatch", &OUT::mu_truthMatch);
  tree->Branch("mu_truthMinDR", &OUT::mu_truthMinDR);
  tree->Branch("ph_pt", &OUT::ph_pt);
  tree->Branch("ph_eta", &OUT::ph_eta);
  tree->Branch("ph_sceta", &OUT::ph_sceta);
  tree->Branch("ph_phi", &OUT::ph_phi);
  tree->Branch("ph_e", &OUT::ph_e);
  tree->Branch("ph_HoverE", &OUT::ph_HoverE);
  tree->Branch("ph_HoverE12", &OUT::ph_HoverE12);
  tree->Branch("ph_sigmaIEIE", &OUT::ph_sigmaIEIE);
  tree->Branch("ph_sigmaIEIP", &OUT::ph_sigmaIEIP);
  tree->Branch("ph_r9", &OUT::ph_r9);
  tree->Branch("ph_E1x3", &OUT::ph_E1x3);
  tree->Branch("ph_E2x2", &OUT::ph_E2x2);
  tree->Branch("ph_E5x5", &OUT::ph_E5x5);
  tree->Branch("ph_E2x5Max", &OUT::ph_E2x5Max);
  tree->Branch("ph_SCetaWidth", &OUT::ph_SCetaWidth);
  tree->Branch("ph_SCphiWidth", &OUT::ph_SCphiWidth);
  tree->Branch("ph_ESEffSigmaRR", &OUT::ph_ESEffSigmaRR);
  tree->Branch("ph_hcalIsoDR03", &OUT::ph_hcalIsoDR03);
  tree->Branch("ph_trkIsoHollowDR03", &OUT::ph_trkIsoHollowDR03);
  tree->Branch("ph_chgpfIsoDR02", &OUT::ph_chgpfIsoDR02);
  tree->Branch("ph_pfChIsoWorst", &OUT::ph_pfChIsoWorst);
  tree->Branch("ph_chIso", &OUT::ph_chIso);
  tree->Branch("ph_neuIso", &OUT::ph_neuIso);
  tree->Branch("ph_phoIso", &OUT::ph_phoIso);
  tree->Branch("ph_chIsoCorr", &OUT::ph_chIsoCorr);
  tree->Branch("ph_neuIsoCorr", &OUT::ph_neuIsoCorr);
  tree->Branch("ph_phoIsoCorr", &OUT::ph_phoIsoCorr);
  tree->Branch("ph_SCRChIso", &OUT::ph_SCRChIso);
  tree->Branch("ph_SCRPhoIso", &OUT::ph_SCRPhoIso);
  tree->Branch("ph_SCRNeuIso", &OUT::ph_SCRNeuIso);
  tree->Branch("ph_SCRChIso04", &OUT::ph_SCRChIso04);
  tree->Branch("ph_SCRPhoIso04", &OUT::ph_SCRPhoIso04);
  tree->Branch("ph_SCRNeuIso04", &OUT::ph_SCRNeuIso04);
  tree->Branch("ph_RandConeChIso", &OUT::ph_RandConeChIso);
  tree->Branch("ph_RandConePhoIso", &OUT::ph_RandConePhoIso);
  tree->Branch("ph_RandConeNeuIso", &OUT::ph_RandConeNeuIso);
  tree->Branch("ph_RandConeChIso04", &OUT::ph_RandConeChIso04);
  tree->Branch("ph_RandConePhoIso04", &OUT::ph_RandConePhoIso04);
  tree->Branch("ph_RandConeNeuIso04", &OUT::ph_RandConeNeuIso04);
  tree->Branch("ph_eleVeto", &OUT::ph_eleVeto);
  tree->Branch("ph_hasPixSeed", &OUT::ph_hasPixSeed);
  tree->Branch("ph_drToTrk", &OUT::ph_drToTrk);
  tree->Branch("ph_isConv", &OUT::ph_isConv);
  tree->Branch("ph_conv_nTrk", &OUT::ph_conv_nTrk);
  tree->Branch("ph_conv_vtx_x", &OUT::ph_conv_vtx_x);
  tree->Branch("ph_conv_vtx_y", &OUT::ph_conv_vtx_y);
  tree->Branch("ph_conv_vtx_z", &OUT::ph_conv_vtx_z);
  tree->Branch("ph_conv_ptin1", &OUT::ph_conv_ptin1);
  tree->Branch("ph_conv_ptin2", &OUT::ph_conv_ptin2);
  tree->Branch("ph_conv_ptout1", &OUT::ph_conv_ptout1);
  tree->Branch("ph_conv_ptout2", &OUT::ph_conv_ptout2);
  tree->Branch("ph_passTight", &OUT::ph_passTight);
  tree->Branch("ph_passMedium", &OUT::ph_passMedium);
  tree->Branch("ph_passLoose", &OUT::ph_passLoose);
  tree->Branch("ph_passLooseNoSIEIE", &OUT::ph_passLooseNoSIEIE);
  tree->Branch("ph_passHOverELoose", &OUT::ph_passHOverELoose);
  tree->Branch("ph_passHOverEMedium", &OUT::ph_passHOverEMedium);
  tree->Branch("ph_passHOverETight", &OUT::ph_passHOverETight);
  tree->Branch("ph_passSIEIELoose", &OUT::ph_passSIEIELoose);
  tree->Branch("ph_passSIEIEMedium", &OUT::ph_passSIEIEMedium);
  tree->Branch("ph_passSIEIETight", &OUT::ph_passSIEIETight);
  tree->Branch("ph_passChIsoCorrLoose", &OUT::ph_passChIsoCorrLoose);
  tree->Branch("ph_passChIsoCorrMedium", &OUT::ph_passChIsoCorrMedium);
  tree->Branch("ph_passChIsoCorrTight", &OUT::ph_passChIsoCorrTight);
  tree->Branch("ph_passNeuIsoCorrLoose", &OUT::ph_passNeuIsoCorrLoose);
  tree->Branch("ph_passNeuIsoCorrMedium", &OUT::ph_passNeuIsoCorrMedium);
  tree->Branch("ph_passNeuIsoCorrTight", &OUT::ph_passNeuIsoCorrTight);
  tree->Branch("ph_passPhoIsoCorrLoose", &OUT::ph_passPhoIsoCorrLoose);
  tree->Branch("ph_passPhoIsoCorrMedium", &OUT::ph_passPhoIsoCorrMedium);
  tree->Branch("ph_passPhoIsoCorrTight", &OUT::ph_passPhoIsoCorrTight);
  tree->Branch("ph_truthMatch_el", &OUT::ph_truthMatch_el);
  tree->Branch("ph_truthMinDR_el", &OUT::ph_truthMinDR_el);
  tree->Branch("ph_truthMatchPt_el", &OUT::ph_truthMatchPt_el);
  tree->Branch("ph_truthMatch_ph", &OUT::ph_truthMatch_ph);
  tree->Branch("ph_truthMinDR_ph", &OUT::ph_truthMinDR_ph);
  tree->Branch("ph_truthMatchPt_ph", &OUT::ph_truthMatchPt_ph);
  tree->Branch("ph_truthMatchMotherPID_ph", &OUT::ph_truthMatchMotherPID_ph);
  tree->Branch("ph_hasSLConv", &OUT::ph_hasSLConv);
  tree->Branch("ph_pass_mva_presel", &OUT::ph_pass_mva_presel);
  tree->Branch("ph_mvascore", &OUT::ph_mvascore);
  tree->Branch("ph_IsEB", &OUT::ph_IsEB);
  tree->Branch("ph_IsEE", &OUT::ph_IsEE);
  tree->Branch("jet_pt", &OUT::jet_pt);
  tree->Branch("jet_eta", &OUT::jet_eta);
  tree->Branch("jet_phi", &OUT::jet_phi);
  tree->Branch("jet_e", &OUT::jet_e);
  tree->Branch("PUWeight", &OUT::PUWeight, "PUWeight/F");
  tree->Branch("isBlinded", &OUT::isBlinded, "isBlinded/O");
  tree->Branch("EventWeight", &OUT::EventWeight, "EventWeight/F");
  tree->Branch("mu_pt25_n", &OUT::mu_pt25_n, "mu_pt25_n/I");
  tree->Branch("mu_passtrig_n", &OUT::mu_passtrig_n, "mu_passtrig_n/I");
  tree->Branch("mu_passtrig25_n", &OUT::mu_passtrig25_n, "mu_passtrig25_n/I");
  tree->Branch("el_pt25_n", &OUT::el_pt25_n, "el_pt25_n/I");
  tree->Branch("el_passtrig_n", &OUT::el_passtrig_n, "el_passtrig_n/I");
  tree->Branch("el_passtrig28_n", &OUT::el_passtrig28_n, "el_passtrig28_n/I");
  tree->Branch("ph_mediumNoSIEIE_n", &OUT::ph_mediumNoSIEIE_n, "ph_mediumNoSIEIE_n/I");
  tree->Branch("ph_medium_n", &OUT::ph_medium_n, "ph_medium_n/I");
  tree->Branch("ph_mediumNoEleVeto_n", &OUT::ph_mediumNoEleVeto_n, "ph_mediumNoEleVeto_n/I");
  tree->Branch("ph_mediumNoSIEIENoEleVeto_n", &OUT::ph_mediumNoSIEIENoEleVeto_n, "ph_mediumNoSIEIENoEleVeto_n/I");
  tree->Branch("ph_mediumNoIso_n", &OUT::ph_mediumNoIso_n, "ph_mediumNoIso_n/I");
  tree->Branch("ph_mediumNoChIso_n", &OUT::ph_mediumNoChIso_n, "ph_mediumNoChIso_n/I");
  tree->Branch("ph_mediumNoNeuIso_n", &OUT::ph_mediumNoNeuIso_n, "ph_mediumNoNeuIso_n/I");
  tree->Branch("ph_mediumNoPhoIso_n", &OUT::ph_mediumNoPhoIso_n, "ph_mediumNoPhoIso_n/I");
  tree->Branch("ph_mediumNoChIsoNoNeuIso_n", &OUT::ph_mediumNoChIsoNoNeuIso_n, "ph_mediumNoChIsoNoNeuIso_n/I");
  tree->Branch("ph_mediumNoChIsoNoPhoIso_n", &OUT::ph_mediumNoChIsoNoPhoIso_n, "ph_mediumNoChIsoNoPhoIso_n/I");
  tree->Branch("ph_mediumNoNeuIsoNoPhoIso_n", &OUT::ph_mediumNoNeuIsoNoPhoIso_n, "ph_mediumNoNeuIsoNoPhoIso_n/I");
  tree->Branch("ph_trigMatch_el", &OUT::ph_trigMatch_el);
  tree->Branch("leadPhot_pt", &OUT::leadPhot_pt, "leadPhot_pt/F");
  tree->Branch("sublPhot_pt", &OUT::sublPhot_pt, "sublPhot_pt/F");
  tree->Branch("leadPhot_lepDR", &OUT::leadPhot_lepDR, "leadPhot_lepDR/F");
  tree->Branch("sublPhot_lepDR", &OUT::sublPhot_lepDR, "sublPhot_lepDR/F");
  tree->Branch("ph_phDR", &OUT::ph_phDR, "ph_phDR/F");
  tree->Branch("phPhot_lepDR", &OUT::phPhot_lepDR, "phPhot_lepDR/F");
  tree->Branch("leadPhot_lepDPhi", &OUT::leadPhot_lepDPhi, "leadPhot_lepDPhi/F");
  tree->Branch("sublPhot_lepDPhi", &OUT::sublPhot_lepDPhi, "sublPhot_lepDPhi/F");
  tree->Branch("ph_phDPhi", &OUT::ph_phDPhi, "ph_phDPhi/F");
  tree->Branch("phPhot_lepDPhi", &OUT::phPhot_lepDPhi, "phPhot_lepDPhi/F");
  tree->Branch("dphi_met_lep1", &OUT::dphi_met_lep1, "dphi_met_lep1/F");
  tree->Branch("dphi_met_lep2", &OUT::dphi_met_lep2, "dphi_met_lep2/F");
  tree->Branch("dphi_met_ph1", &OUT::dphi_met_ph1, "dphi_met_ph1/F");
  tree->Branch("dphi_met_ph2", &OUT::dphi_met_ph2, "dphi_met_ph2/F");
  tree->Branch("mt_lep_met", &OUT::mt_lep_met, "mt_lep_met/F");
  tree->Branch("mt_lepph1_met", &OUT::mt_lepph1_met, "mt_lepph1_met/F");
  tree->Branch("mt_lepph2_met", &OUT::mt_lepph2_met, "mt_lepph2_met/F");
  tree->Branch("mt_lepphph_met", &OUT::mt_lepphph_met, "mt_lepphph_met/F");
  tree->Branch("m_leplep", &OUT::m_leplep, "m_leplep/F");
  tree->Branch("m_lepph1", &OUT::m_lepph1, "m_lepph1/F");
  tree->Branch("m_lepph2", &OUT::m_lepph2, "m_lepph2/F");
  tree->Branch("m_leplepph", &OUT::m_leplepph, "m_leplepph/F");
  tree->Branch("m_lepphph", &OUT::m_lepphph, "m_lepphph/F");
  tree->Branch("m_phph", &OUT::m_phph, "m_phph/F");
  tree->Branch("m_leplepZ", &OUT::m_leplepZ, "m_leplepZ/F");
  tree->Branch("m_3lep", &OUT::m_3lep, "m_3lep/F");
  tree->Branch("m_4lep", &OUT::m_4lep, "m_4lep/F");
  tree->Branch("pt_phph", &OUT::pt_phph, "pt_phph/F");
  tree->Branch("pt_leplep", &OUT::pt_leplep, "pt_leplep/F");
  tree->Branch("pt_lepph1", &OUT::pt_lepph1, "pt_lepph1/F");
  tree->Branch("pt_lepph2", &OUT::pt_lepph2, "pt_lepph2/F");
  tree->Branch("pt_lepphph", &OUT::pt_lepphph, "pt_lepphph/F");
  tree->Branch("pt_leplepph", &OUT::pt_leplepph, "pt_leplepph/F");
  tree->Branch("pt_secondLepton", &OUT::pt_secondLepton, "pt_secondLepton/F");
  tree->Branch("pt_thirdLepton", &OUT::pt_thirdLepton, "pt_thirdLepton/F");
  tree->Branch("leadPhot_leadLepDR", &OUT::leadPhot_leadLepDR, "leadPhot_leadLepDR/F");
  tree->Branch("leadPhot_sublLepDR", &OUT::leadPhot_sublLepDR, "leadPhot_sublLepDR/F");
  tree->Branch("sublPhot_leadLepDR", &OUT::sublPhot_leadLepDR, "sublPhot_leadLepDR/F");
  tree->Branch("sublPhot_sublLepDR", &OUT::sublPhot_sublLepDR, "sublPhot_sublLepDR/F");
  tree->Branch("m_nearestToZ", &OUT::m_nearestToZ, "m_nearestToZ/F");
  tree->Branch("m_minZdifflepph", &OUT::m_minZdifflepph, "m_minZdifflepph/F");
  tree->Branch("truelep_n", &OUT::truelep_n, "truelep_n/I");
  tree->Branch("trueph_n", &OUT::trueph_n, "trueph_n/I");
  tree->Branch("trueph_wmother_n", &OUT::trueph_wmother_n, "trueph_wmother_n/I");
  tree->Branch("truegenph_n", &OUT::truegenph_n, "truegenph_n/I");
  tree->Branch("truegenphpt15_n", &OUT::truegenphpt15_n, "truegenphpt15_n/I");
  tree->Branch("truelep_pt", &OUT::truelep_pt);
  tree->Branch("truelep_eta", &OUT::truelep_eta);
  tree->Branch("truelep_phi", &OUT::truelep_phi);
  tree->Branch("truelep_e", &OUT::truelep_e);
  tree->Branch("truelep_isElec", &OUT::truelep_isElec);
  tree->Branch("truelep_isMuon", &OUT::truelep_isMuon);
  tree->Branch("truelep_motherPID", &OUT::truelep_motherPID);
  tree->Branch("trueph_pt", &OUT::trueph_pt);
  tree->Branch("trueph_eta", &OUT::trueph_eta);
  tree->Branch("trueph_phi", &OUT::trueph_phi);
  tree->Branch("trueph_motherPID", &OUT::trueph_motherPID);
  tree->Branch("trueph_parentage", &OUT::trueph_parentage);
  tree->Branch("trueph_nearestLepDR", &OUT::trueph_nearestLepDR);
  tree->Branch("trueph_nearestQrkDR", &OUT::trueph_nearestQrkDR);
  tree->Branch("trueleadlep_pt", &OUT::trueleadlep_pt, "trueleadlep_pt/F");
  tree->Branch("truesubllep_pt", &OUT::truesubllep_pt, "truesubllep_pt/F");
  tree->Branch("trueleadlep_leadPhotDR", &OUT::trueleadlep_leadPhotDR, "trueleadlep_leadPhotDR/F");
  tree->Branch("trueleadlep_sublPhotDR", &OUT::trueleadlep_sublPhotDR, "trueleadlep_sublPhotDR/F");
  tree->Branch("truesubllep_leadPhotDR", &OUT::truesubllep_leadPhotDR, "truesubllep_leadPhotDR/F");
  tree->Branch("truesubllep_sublPhotDR", &OUT::truesubllep_sublPhotDR, "truesubllep_sublPhotDR/F");
}
void CopyInputVarsToOutput( std::string prefix) {
    CopynVtxInToOut( prefix ); 
    CopynVtxBSInToOut( prefix ); 
    CopynMCInToOut( prefix ); 
    CopymcPIDInToOut( prefix ); 
    CopymcPtInToOut( prefix ); 
    CopymcEtaInToOut( prefix ); 
    CopymcPhiInToOut( prefix ); 
    CopymcEInToOut( prefix ); 
    CopymcGMomPIDInToOut( prefix ); 
    CopymcMomPIDInToOut( prefix ); 
    CopymcParentageInToOut( prefix ); 
    CopymcStatusInToOut( prefix ); 
    CopynPUInToOut( prefix ); 
    CopypuTrueInToOut( prefix ); 
    CopypfMETInToOut( prefix ); 
    CopypfMETPhiInToOut( prefix ); 
    CopypfMETsumEtInToOut( prefix ); 
    CopypfMETmEtSigInToOut( prefix ); 
    CopypfMETSigInToOut( prefix ); 
    CopyrecoPfMETInToOut( prefix ); 
    CopyrecoPfMETPhiInToOut( prefix ); 
    CopyrecoPfMETsumEtInToOut( prefix ); 
    CopyrecoPfMETmEtSigInToOut( prefix ); 
    CopyrecoPfMETSigInToOut( prefix ); 
    Copyrho2012InToOut( prefix ); 
    Copyel_nInToOut( prefix ); 
    Copymu_nInToOut( prefix ); 
    Copyph_nInToOut( prefix ); 
    Copyjet_nInToOut( prefix ); 
    Copyvtx_nInToOut( prefix ); 
    Copyel_ptInToOut( prefix ); 
    Copyel_etaInToOut( prefix ); 
    Copyel_scetaInToOut( prefix ); 
    Copyel_phiInToOut( prefix ); 
    Copyel_eInToOut( prefix ); 
    Copyel_pt_uncorrInToOut( prefix ); 
    Copyel_mva_trigInToOut( prefix ); 
    Copyel_mva_nontrigInToOut( prefix ); 
    Copyel_d0pvInToOut( prefix ); 
    Copyel_z0pvInToOut( prefix ); 
    Copyel_sigmaIEIEInToOut( prefix ); 
    Copyel_pfiso30InToOut( prefix ); 
    Copyel_pfiso40InToOut( prefix ); 
    Copyel_triggerMatchInToOut( prefix ); 
    Copyel_hasMatchedConvInToOut( prefix ); 
    Copyel_passTightInToOut( prefix ); 
    Copyel_passMediumInToOut( prefix ); 
    Copyel_passLooseInToOut( prefix ); 
    Copyel_passVeryLooseInToOut( prefix ); 
    Copyel_passTightTrigInToOut( prefix ); 
    Copyel_passMvaTrigInToOut( prefix ); 
    Copyel_passMvaNonTrigInToOut( prefix ); 
    Copyel_truthMatch_elInToOut( prefix ); 
    Copyel_truthMinDR_elInToOut( prefix ); 
    Copyel_truthMatchPt_elInToOut( prefix ); 
    Copymu_ptInToOut( prefix ); 
    Copymu_etaInToOut( prefix ); 
    Copymu_phiInToOut( prefix ); 
    Copymu_eInToOut( prefix ); 
    Copymu_pt_uncorrInToOut( prefix ); 
    Copymu_pfIso_chInToOut( prefix ); 
    Copymu_pfIso_nhInToOut( prefix ); 
    Copymu_pfIso_phoInToOut( prefix ); 
    Copymu_pfIso_puInToOut( prefix ); 
    Copymu_corrIsoInToOut( prefix ); 
    Copymu_triggerMatchInToOut( prefix ); 
    Copymu_truthMatchInToOut( prefix ); 
    Copymu_truthMinDRInToOut( prefix ); 
    Copyph_ptInToOut( prefix ); 
    Copyph_etaInToOut( prefix ); 
    Copyph_scetaInToOut( prefix ); 
    Copyph_phiInToOut( prefix ); 
    Copyph_eInToOut( prefix ); 
    Copyph_HoverEInToOut( prefix ); 
    Copyph_HoverE12InToOut( prefix ); 
    Copyph_sigmaIEIEInToOut( prefix ); 
    Copyph_sigmaIEIPInToOut( prefix ); 
    Copyph_r9InToOut( prefix ); 
    Copyph_E1x3InToOut( prefix ); 
    Copyph_E2x2InToOut( prefix ); 
    Copyph_E5x5InToOut( prefix ); 
    Copyph_E2x5MaxInToOut( prefix ); 
    Copyph_SCetaWidthInToOut( prefix ); 
    Copyph_SCphiWidthInToOut( prefix ); 
    Copyph_ESEffSigmaRRInToOut( prefix ); 
    Copyph_hcalIsoDR03InToOut( prefix ); 
    Copyph_trkIsoHollowDR03InToOut( prefix ); 
    Copyph_chgpfIsoDR02InToOut( prefix ); 
    Copyph_pfChIsoWorstInToOut( prefix ); 
    Copyph_chIsoInToOut( prefix ); 
    Copyph_neuIsoInToOut( prefix ); 
    Copyph_phoIsoInToOut( prefix ); 
    Copyph_chIsoCorrInToOut( prefix ); 
    Copyph_neuIsoCorrInToOut( prefix ); 
    Copyph_phoIsoCorrInToOut( prefix ); 
    Copyph_SCRChIsoInToOut( prefix ); 
    Copyph_SCRPhoIsoInToOut( prefix ); 
    Copyph_SCRNeuIsoInToOut( prefix ); 
    Copyph_SCRChIso04InToOut( prefix ); 
    Copyph_SCRPhoIso04InToOut( prefix ); 
    Copyph_SCRNeuIso04InToOut( prefix ); 
    Copyph_RandConeChIsoInToOut( prefix ); 
    Copyph_RandConePhoIsoInToOut( prefix ); 
    Copyph_RandConeNeuIsoInToOut( prefix ); 
    Copyph_RandConeChIso04InToOut( prefix ); 
    Copyph_RandConePhoIso04InToOut( prefix ); 
    Copyph_RandConeNeuIso04InToOut( prefix ); 
    Copyph_eleVetoInToOut( prefix ); 
    Copyph_hasPixSeedInToOut( prefix ); 
    Copyph_drToTrkInToOut( prefix ); 
    Copyph_isConvInToOut( prefix ); 
    Copyph_conv_nTrkInToOut( prefix ); 
    Copyph_conv_vtx_xInToOut( prefix ); 
    Copyph_conv_vtx_yInToOut( prefix ); 
    Copyph_conv_vtx_zInToOut( prefix ); 
    Copyph_conv_ptin1InToOut( prefix ); 
    Copyph_conv_ptin2InToOut( prefix ); 
    Copyph_conv_ptout1InToOut( prefix ); 
    Copyph_conv_ptout2InToOut( prefix ); 
    Copyph_passTightInToOut( prefix ); 
    Copyph_passMediumInToOut( prefix ); 
    Copyph_passLooseInToOut( prefix ); 
    Copyph_passLooseNoSIEIEInToOut( prefix ); 
    Copyph_passHOverELooseInToOut( prefix ); 
    Copyph_passHOverEMediumInToOut( prefix ); 
    Copyph_passHOverETightInToOut( prefix ); 
    Copyph_passSIEIELooseInToOut( prefix ); 
    Copyph_passSIEIEMediumInToOut( prefix ); 
    Copyph_passSIEIETightInToOut( prefix ); 
    Copyph_passChIsoCorrLooseInToOut( prefix ); 
    Copyph_passChIsoCorrMediumInToOut( prefix ); 
    Copyph_passChIsoCorrTightInToOut( prefix ); 
    Copyph_passNeuIsoCorrLooseInToOut( prefix ); 
    Copyph_passNeuIsoCorrMediumInToOut( prefix ); 
    Copyph_passNeuIsoCorrTightInToOut( prefix ); 
    Copyph_passPhoIsoCorrLooseInToOut( prefix ); 
    Copyph_passPhoIsoCorrMediumInToOut( prefix ); 
    Copyph_passPhoIsoCorrTightInToOut( prefix ); 
    Copyph_truthMatch_elInToOut( prefix ); 
    Copyph_truthMinDR_elInToOut( prefix ); 
    Copyph_truthMatchPt_elInToOut( prefix ); 
    Copyph_truthMatch_phInToOut( prefix ); 
    Copyph_truthMinDR_phInToOut( prefix ); 
    Copyph_truthMatchPt_phInToOut( prefix ); 
    Copyph_truthMatchMotherPID_phInToOut( prefix ); 
    Copyph_hasSLConvInToOut( prefix ); 
    Copyph_pass_mva_preselInToOut( prefix ); 
    Copyph_mvascoreInToOut( prefix ); 
    Copyph_IsEBInToOut( prefix ); 
    Copyph_IsEEInToOut( prefix ); 
    Copyjet_ptInToOut( prefix ); 
    Copyjet_etaInToOut( prefix ); 
    Copyjet_phiInToOut( prefix ); 
    Copyjet_eInToOut( prefix ); 
    CopyPUWeightInToOut( prefix ); 
    CopyisBlindedInToOut( prefix ); 
    CopyEventWeightInToOut( prefix ); 
    Copymu_pt25_nInToOut( prefix ); 
    Copymu_passtrig_nInToOut( prefix ); 
    Copymu_passtrig25_nInToOut( prefix ); 
    Copyel_pt25_nInToOut( prefix ); 
    Copyel_passtrig_nInToOut( prefix ); 
    Copyel_passtrig28_nInToOut( prefix ); 
    Copyph_mediumNoSIEIE_nInToOut( prefix ); 
    Copyph_medium_nInToOut( prefix ); 
    Copyph_mediumNoEleVeto_nInToOut( prefix ); 
    Copyph_mediumNoSIEIENoEleVeto_nInToOut( prefix ); 
    Copyph_mediumNoIso_nInToOut( prefix ); 
    Copyph_mediumNoChIso_nInToOut( prefix ); 
    Copyph_mediumNoNeuIso_nInToOut( prefix ); 
    Copyph_mediumNoPhoIso_nInToOut( prefix ); 
    Copyph_mediumNoChIsoNoNeuIso_nInToOut( prefix ); 
    Copyph_mediumNoChIsoNoPhoIso_nInToOut( prefix ); 
    Copyph_mediumNoNeuIsoNoPhoIso_nInToOut( prefix ); 
    Copyph_trigMatch_elInToOut( prefix ); 
    CopyleadPhot_ptInToOut( prefix ); 
    CopysublPhot_ptInToOut( prefix ); 
    CopyleadPhot_lepDRInToOut( prefix ); 
    CopysublPhot_lepDRInToOut( prefix ); 
    Copyph_phDRInToOut( prefix ); 
    CopyphPhot_lepDRInToOut( prefix ); 
    CopyleadPhot_lepDPhiInToOut( prefix ); 
    CopysublPhot_lepDPhiInToOut( prefix ); 
    Copyph_phDPhiInToOut( prefix ); 
    CopyphPhot_lepDPhiInToOut( prefix ); 
    Copydphi_met_lep1InToOut( prefix ); 
    Copydphi_met_lep2InToOut( prefix ); 
    Copydphi_met_ph1InToOut( prefix ); 
    Copydphi_met_ph2InToOut( prefix ); 
    Copymt_lep_metInToOut( prefix ); 
    Copymt_lepph1_metInToOut( prefix ); 
    Copymt_lepph2_metInToOut( prefix ); 
    Copymt_lepphph_metInToOut( prefix ); 
    Copym_leplepInToOut( prefix ); 
    Copym_lepph1InToOut( prefix ); 
    Copym_lepph2InToOut( prefix ); 
    Copym_leplepphInToOut( prefix ); 
    Copym_lepphphInToOut( prefix ); 
    Copym_phphInToOut( prefix ); 
    Copym_leplepZInToOut( prefix ); 
    Copym_3lepInToOut( prefix ); 
    Copym_4lepInToOut( prefix ); 
    Copypt_phphInToOut( prefix ); 
    Copypt_leplepInToOut( prefix ); 
    Copypt_lepph1InToOut( prefix ); 
    Copypt_lepph2InToOut( prefix ); 
    Copypt_lepphphInToOut( prefix ); 
    Copypt_leplepphInToOut( prefix ); 
    Copypt_secondLeptonInToOut( prefix ); 
    Copypt_thirdLeptonInToOut( prefix ); 
    CopyleadPhot_leadLepDRInToOut( prefix ); 
    CopyleadPhot_sublLepDRInToOut( prefix ); 
    CopysublPhot_leadLepDRInToOut( prefix ); 
    CopysublPhot_sublLepDRInToOut( prefix ); 
    Copym_nearestToZInToOut( prefix ); 
    Copym_minZdifflepphInToOut( prefix ); 
    Copytruelep_nInToOut( prefix ); 
    Copytrueph_nInToOut( prefix ); 
    Copytrueph_wmother_nInToOut( prefix ); 
    Copytruegenph_nInToOut( prefix ); 
    Copytruegenphpt15_nInToOut( prefix ); 
    Copytruelep_ptInToOut( prefix ); 
    Copytruelep_etaInToOut( prefix ); 
    Copytruelep_phiInToOut( prefix ); 
    Copytruelep_eInToOut( prefix ); 
    Copytruelep_isElecInToOut( prefix ); 
    Copytruelep_isMuonInToOut( prefix ); 
    Copytruelep_motherPIDInToOut( prefix ); 
    Copytrueph_ptInToOut( prefix ); 
    Copytrueph_etaInToOut( prefix ); 
    Copytrueph_phiInToOut( prefix ); 
    Copytrueph_motherPIDInToOut( prefix ); 
    Copytrueph_parentageInToOut( prefix ); 
    Copytrueph_nearestLepDRInToOut( prefix ); 
    Copytrueph_nearestQrkDRInToOut( prefix ); 
    Copytrueleadlep_ptInToOut( prefix ); 
    Copytruesubllep_ptInToOut( prefix ); 
    Copytrueleadlep_leadPhotDRInToOut( prefix ); 
    Copytrueleadlep_sublPhotDRInToOut( prefix ); 
    Copytruesubllep_leadPhotDRInToOut( prefix ); 
    Copytruesubllep_sublPhotDRInToOut( prefix ); 
}

// The next set of functions allows one to copy 
// input variables to the outputs based on a key
// A copy function is generated for each pair of variables
// The copy function holds the name of the function to compare
// to the input key.  If the variables are vectors, a second function
// is generated that allows one to copy all variables matching a given key
// at a certain index and pushes that back on the output variable

void CopyPrefixBranchesInToOut( const std::string & prefix ) {
// Just call each copy function with the prefix 

    CopynVtxInToOut( prefix );
    CopynVtxBSInToOut( prefix );
    CopynMCInToOut( prefix );
    CopymcPIDInToOut( prefix );
    CopymcPtInToOut( prefix );
    CopymcEtaInToOut( prefix );
    CopymcPhiInToOut( prefix );
    CopymcEInToOut( prefix );
    CopymcGMomPIDInToOut( prefix );
    CopymcMomPIDInToOut( prefix );
    CopymcParentageInToOut( prefix );
    CopymcStatusInToOut( prefix );
    CopynPUInToOut( prefix );
    CopypuTrueInToOut( prefix );
    CopypfMETInToOut( prefix );
    CopypfMETPhiInToOut( prefix );
    CopypfMETsumEtInToOut( prefix );
    CopypfMETmEtSigInToOut( prefix );
    CopypfMETSigInToOut( prefix );
    CopyrecoPfMETInToOut( prefix );
    CopyrecoPfMETPhiInToOut( prefix );
    CopyrecoPfMETsumEtInToOut( prefix );
    CopyrecoPfMETmEtSigInToOut( prefix );
    CopyrecoPfMETSigInToOut( prefix );
    Copyrho2012InToOut( prefix );
    Copyel_nInToOut( prefix );
    Copymu_nInToOut( prefix );
    Copyph_nInToOut( prefix );
    Copyjet_nInToOut( prefix );
    Copyvtx_nInToOut( prefix );
    Copyel_ptInToOut( prefix );
    Copyel_etaInToOut( prefix );
    Copyel_scetaInToOut( prefix );
    Copyel_phiInToOut( prefix );
    Copyel_eInToOut( prefix );
    Copyel_pt_uncorrInToOut( prefix );
    Copyel_mva_trigInToOut( prefix );
    Copyel_mva_nontrigInToOut( prefix );
    Copyel_d0pvInToOut( prefix );
    Copyel_z0pvInToOut( prefix );
    Copyel_sigmaIEIEInToOut( prefix );
    Copyel_pfiso30InToOut( prefix );
    Copyel_pfiso40InToOut( prefix );
    Copyel_triggerMatchInToOut( prefix );
    Copyel_hasMatchedConvInToOut( prefix );
    Copyel_passTightInToOut( prefix );
    Copyel_passMediumInToOut( prefix );
    Copyel_passLooseInToOut( prefix );
    Copyel_passVeryLooseInToOut( prefix );
    Copyel_passTightTrigInToOut( prefix );
    Copyel_passMvaTrigInToOut( prefix );
    Copyel_passMvaNonTrigInToOut( prefix );
    Copyel_truthMatch_elInToOut( prefix );
    Copyel_truthMinDR_elInToOut( prefix );
    Copyel_truthMatchPt_elInToOut( prefix );
    Copymu_ptInToOut( prefix );
    Copymu_etaInToOut( prefix );
    Copymu_phiInToOut( prefix );
    Copymu_eInToOut( prefix );
    Copymu_pt_uncorrInToOut( prefix );
    Copymu_pfIso_chInToOut( prefix );
    Copymu_pfIso_nhInToOut( prefix );
    Copymu_pfIso_phoInToOut( prefix );
    Copymu_pfIso_puInToOut( prefix );
    Copymu_corrIsoInToOut( prefix );
    Copymu_triggerMatchInToOut( prefix );
    Copymu_truthMatchInToOut( prefix );
    Copymu_truthMinDRInToOut( prefix );
    Copyph_ptInToOut( prefix );
    Copyph_etaInToOut( prefix );
    Copyph_scetaInToOut( prefix );
    Copyph_phiInToOut( prefix );
    Copyph_eInToOut( prefix );
    Copyph_HoverEInToOut( prefix );
    Copyph_HoverE12InToOut( prefix );
    Copyph_sigmaIEIEInToOut( prefix );
    Copyph_sigmaIEIPInToOut( prefix );
    Copyph_r9InToOut( prefix );
    Copyph_E1x3InToOut( prefix );
    Copyph_E2x2InToOut( prefix );
    Copyph_E5x5InToOut( prefix );
    Copyph_E2x5MaxInToOut( prefix );
    Copyph_SCetaWidthInToOut( prefix );
    Copyph_SCphiWidthInToOut( prefix );
    Copyph_ESEffSigmaRRInToOut( prefix );
    Copyph_hcalIsoDR03InToOut( prefix );
    Copyph_trkIsoHollowDR03InToOut( prefix );
    Copyph_chgpfIsoDR02InToOut( prefix );
    Copyph_pfChIsoWorstInToOut( prefix );
    Copyph_chIsoInToOut( prefix );
    Copyph_neuIsoInToOut( prefix );
    Copyph_phoIsoInToOut( prefix );
    Copyph_chIsoCorrInToOut( prefix );
    Copyph_neuIsoCorrInToOut( prefix );
    Copyph_phoIsoCorrInToOut( prefix );
    Copyph_SCRChIsoInToOut( prefix );
    Copyph_SCRPhoIsoInToOut( prefix );
    Copyph_SCRNeuIsoInToOut( prefix );
    Copyph_SCRChIso04InToOut( prefix );
    Copyph_SCRPhoIso04InToOut( prefix );
    Copyph_SCRNeuIso04InToOut( prefix );
    Copyph_RandConeChIsoInToOut( prefix );
    Copyph_RandConePhoIsoInToOut( prefix );
    Copyph_RandConeNeuIsoInToOut( prefix );
    Copyph_RandConeChIso04InToOut( prefix );
    Copyph_RandConePhoIso04InToOut( prefix );
    Copyph_RandConeNeuIso04InToOut( prefix );
    Copyph_eleVetoInToOut( prefix );
    Copyph_hasPixSeedInToOut( prefix );
    Copyph_drToTrkInToOut( prefix );
    Copyph_isConvInToOut( prefix );
    Copyph_conv_nTrkInToOut( prefix );
    Copyph_conv_vtx_xInToOut( prefix );
    Copyph_conv_vtx_yInToOut( prefix );
    Copyph_conv_vtx_zInToOut( prefix );
    Copyph_conv_ptin1InToOut( prefix );
    Copyph_conv_ptin2InToOut( prefix );
    Copyph_conv_ptout1InToOut( prefix );
    Copyph_conv_ptout2InToOut( prefix );
    Copyph_passTightInToOut( prefix );
    Copyph_passMediumInToOut( prefix );
    Copyph_passLooseInToOut( prefix );
    Copyph_passLooseNoSIEIEInToOut( prefix );
    Copyph_passHOverELooseInToOut( prefix );
    Copyph_passHOverEMediumInToOut( prefix );
    Copyph_passHOverETightInToOut( prefix );
    Copyph_passSIEIELooseInToOut( prefix );
    Copyph_passSIEIEMediumInToOut( prefix );
    Copyph_passSIEIETightInToOut( prefix );
    Copyph_passChIsoCorrLooseInToOut( prefix );
    Copyph_passChIsoCorrMediumInToOut( prefix );
    Copyph_passChIsoCorrTightInToOut( prefix );
    Copyph_passNeuIsoCorrLooseInToOut( prefix );
    Copyph_passNeuIsoCorrMediumInToOut( prefix );
    Copyph_passNeuIsoCorrTightInToOut( prefix );
    Copyph_passPhoIsoCorrLooseInToOut( prefix );
    Copyph_passPhoIsoCorrMediumInToOut( prefix );
    Copyph_passPhoIsoCorrTightInToOut( prefix );
    Copyph_truthMatch_elInToOut( prefix );
    Copyph_truthMinDR_elInToOut( prefix );
    Copyph_truthMatchPt_elInToOut( prefix );
    Copyph_truthMatch_phInToOut( prefix );
    Copyph_truthMinDR_phInToOut( prefix );
    Copyph_truthMatchPt_phInToOut( prefix );
    Copyph_truthMatchMotherPID_phInToOut( prefix );
    Copyph_hasSLConvInToOut( prefix );
    Copyph_pass_mva_preselInToOut( prefix );
    Copyph_mvascoreInToOut( prefix );
    Copyph_IsEBInToOut( prefix );
    Copyph_IsEEInToOut( prefix );
    Copyjet_ptInToOut( prefix );
    Copyjet_etaInToOut( prefix );
    Copyjet_phiInToOut( prefix );
    Copyjet_eInToOut( prefix );
    CopyPUWeightInToOut( prefix );
    CopyisBlindedInToOut( prefix );
    CopyEventWeightInToOut( prefix );
    Copymu_pt25_nInToOut( prefix );
    Copymu_passtrig_nInToOut( prefix );
    Copymu_passtrig25_nInToOut( prefix );
    Copyel_pt25_nInToOut( prefix );
    Copyel_passtrig_nInToOut( prefix );
    Copyel_passtrig28_nInToOut( prefix );
    Copyph_mediumNoSIEIE_nInToOut( prefix );
    Copyph_medium_nInToOut( prefix );
    Copyph_mediumNoEleVeto_nInToOut( prefix );
    Copyph_mediumNoSIEIENoEleVeto_nInToOut( prefix );
    Copyph_mediumNoIso_nInToOut( prefix );
    Copyph_mediumNoChIso_nInToOut( prefix );
    Copyph_mediumNoNeuIso_nInToOut( prefix );
    Copyph_mediumNoPhoIso_nInToOut( prefix );
    Copyph_mediumNoChIsoNoNeuIso_nInToOut( prefix );
    Copyph_mediumNoChIsoNoPhoIso_nInToOut( prefix );
    Copyph_mediumNoNeuIsoNoPhoIso_nInToOut( prefix );
    Copyph_trigMatch_elInToOut( prefix );
    CopyleadPhot_ptInToOut( prefix );
    CopysublPhot_ptInToOut( prefix );
    CopyleadPhot_lepDRInToOut( prefix );
    CopysublPhot_lepDRInToOut( prefix );
    Copyph_phDRInToOut( prefix );
    CopyphPhot_lepDRInToOut( prefix );
    CopyleadPhot_lepDPhiInToOut( prefix );
    CopysublPhot_lepDPhiInToOut( prefix );
    Copyph_phDPhiInToOut( prefix );
    CopyphPhot_lepDPhiInToOut( prefix );
    Copydphi_met_lep1InToOut( prefix );
    Copydphi_met_lep2InToOut( prefix );
    Copydphi_met_ph1InToOut( prefix );
    Copydphi_met_ph2InToOut( prefix );
    Copymt_lep_metInToOut( prefix );
    Copymt_lepph1_metInToOut( prefix );
    Copymt_lepph2_metInToOut( prefix );
    Copymt_lepphph_metInToOut( prefix );
    Copym_leplepInToOut( prefix );
    Copym_lepph1InToOut( prefix );
    Copym_lepph2InToOut( prefix );
    Copym_leplepphInToOut( prefix );
    Copym_lepphphInToOut( prefix );
    Copym_phphInToOut( prefix );
    Copym_leplepZInToOut( prefix );
    Copym_3lepInToOut( prefix );
    Copym_4lepInToOut( prefix );
    Copypt_phphInToOut( prefix );
    Copypt_leplepInToOut( prefix );
    Copypt_lepph1InToOut( prefix );
    Copypt_lepph2InToOut( prefix );
    Copypt_lepphphInToOut( prefix );
    Copypt_leplepphInToOut( prefix );
    Copypt_secondLeptonInToOut( prefix );
    Copypt_thirdLeptonInToOut( prefix );
    CopyleadPhot_leadLepDRInToOut( prefix );
    CopyleadPhot_sublLepDRInToOut( prefix );
    CopysublPhot_leadLepDRInToOut( prefix );
    CopysublPhot_sublLepDRInToOut( prefix );
    Copym_nearestToZInToOut( prefix );
    Copym_minZdifflepphInToOut( prefix );
    Copytruelep_nInToOut( prefix );
    Copytrueph_nInToOut( prefix );
    Copytrueph_wmother_nInToOut( prefix );
    Copytruegenph_nInToOut( prefix );
    Copytruegenphpt15_nInToOut( prefix );
    Copytruelep_ptInToOut( prefix );
    Copytruelep_etaInToOut( prefix );
    Copytruelep_phiInToOut( prefix );
    Copytruelep_eInToOut( prefix );
    Copytruelep_isElecInToOut( prefix );
    Copytruelep_isMuonInToOut( prefix );
    Copytruelep_motherPIDInToOut( prefix );
    Copytrueph_ptInToOut( prefix );
    Copytrueph_etaInToOut( prefix );
    Copytrueph_phiInToOut( prefix );
    Copytrueph_motherPIDInToOut( prefix );
    Copytrueph_parentageInToOut( prefix );
    Copytrueph_nearestLepDRInToOut( prefix );
    Copytrueph_nearestQrkDRInToOut( prefix );
    Copytrueleadlep_ptInToOut( prefix );
    Copytruesubllep_ptInToOut( prefix );
    Copytrueleadlep_leadPhotDRInToOut( prefix );
    Copytrueleadlep_sublPhotDRInToOut( prefix );
    Copytruesubllep_leadPhotDRInToOut( prefix );
    Copytruesubllep_sublPhotDRInToOut( prefix );
}; 

void CopyPrefixIndexBranchesInToOut( const std::string & prefix, unsigned index ) { 

// Just call each copy function with the prefix 

    CopymcPIDInToOutIndex( index, prefix );
    CopymcPtInToOutIndex( index, prefix );
    CopymcEtaInToOutIndex( index, prefix );
    CopymcPhiInToOutIndex( index, prefix );
    CopymcEInToOutIndex( index, prefix );
    CopymcGMomPIDInToOutIndex( index, prefix );
    CopymcMomPIDInToOutIndex( index, prefix );
    CopymcParentageInToOutIndex( index, prefix );
    CopymcStatusInToOutIndex( index, prefix );
    CopynPUInToOutIndex( index, prefix );
    CopypuTrueInToOutIndex( index, prefix );
    Copyel_ptInToOutIndex( index, prefix );
    Copyel_etaInToOutIndex( index, prefix );
    Copyel_scetaInToOutIndex( index, prefix );
    Copyel_phiInToOutIndex( index, prefix );
    Copyel_eInToOutIndex( index, prefix );
    Copyel_pt_uncorrInToOutIndex( index, prefix );
    Copyel_mva_trigInToOutIndex( index, prefix );
    Copyel_mva_nontrigInToOutIndex( index, prefix );
    Copyel_d0pvInToOutIndex( index, prefix );
    Copyel_z0pvInToOutIndex( index, prefix );
    Copyel_sigmaIEIEInToOutIndex( index, prefix );
    Copyel_pfiso30InToOutIndex( index, prefix );
    Copyel_pfiso40InToOutIndex( index, prefix );
    Copyel_triggerMatchInToOutIndex( index, prefix );
    Copyel_hasMatchedConvInToOutIndex( index, prefix );
    Copyel_passTightInToOutIndex( index, prefix );
    Copyel_passMediumInToOutIndex( index, prefix );
    Copyel_passLooseInToOutIndex( index, prefix );
    Copyel_passVeryLooseInToOutIndex( index, prefix );
    Copyel_passTightTrigInToOutIndex( index, prefix );
    Copyel_passMvaTrigInToOutIndex( index, prefix );
    Copyel_passMvaNonTrigInToOutIndex( index, prefix );
    Copyel_truthMatch_elInToOutIndex( index, prefix );
    Copyel_truthMinDR_elInToOutIndex( index, prefix );
    Copyel_truthMatchPt_elInToOutIndex( index, prefix );
    Copymu_ptInToOutIndex( index, prefix );
    Copymu_etaInToOutIndex( index, prefix );
    Copymu_phiInToOutIndex( index, prefix );
    Copymu_eInToOutIndex( index, prefix );
    Copymu_pt_uncorrInToOutIndex( index, prefix );
    Copymu_pfIso_chInToOutIndex( index, prefix );
    Copymu_pfIso_nhInToOutIndex( index, prefix );
    Copymu_pfIso_phoInToOutIndex( index, prefix );
    Copymu_pfIso_puInToOutIndex( index, prefix );
    Copymu_corrIsoInToOutIndex( index, prefix );
    Copymu_triggerMatchInToOutIndex( index, prefix );
    Copymu_truthMatchInToOutIndex( index, prefix );
    Copymu_truthMinDRInToOutIndex( index, prefix );
    Copyph_ptInToOutIndex( index, prefix );
    Copyph_etaInToOutIndex( index, prefix );
    Copyph_scetaInToOutIndex( index, prefix );
    Copyph_phiInToOutIndex( index, prefix );
    Copyph_eInToOutIndex( index, prefix );
    Copyph_HoverEInToOutIndex( index, prefix );
    Copyph_HoverE12InToOutIndex( index, prefix );
    Copyph_sigmaIEIEInToOutIndex( index, prefix );
    Copyph_sigmaIEIPInToOutIndex( index, prefix );
    Copyph_r9InToOutIndex( index, prefix );
    Copyph_E1x3InToOutIndex( index, prefix );
    Copyph_E2x2InToOutIndex( index, prefix );
    Copyph_E5x5InToOutIndex( index, prefix );
    Copyph_E2x5MaxInToOutIndex( index, prefix );
    Copyph_SCetaWidthInToOutIndex( index, prefix );
    Copyph_SCphiWidthInToOutIndex( index, prefix );
    Copyph_ESEffSigmaRRInToOutIndex( index, prefix );
    Copyph_hcalIsoDR03InToOutIndex( index, prefix );
    Copyph_trkIsoHollowDR03InToOutIndex( index, prefix );
    Copyph_chgpfIsoDR02InToOutIndex( index, prefix );
    Copyph_pfChIsoWorstInToOutIndex( index, prefix );
    Copyph_chIsoInToOutIndex( index, prefix );
    Copyph_neuIsoInToOutIndex( index, prefix );
    Copyph_phoIsoInToOutIndex( index, prefix );
    Copyph_chIsoCorrInToOutIndex( index, prefix );
    Copyph_neuIsoCorrInToOutIndex( index, prefix );
    Copyph_phoIsoCorrInToOutIndex( index, prefix );
    Copyph_SCRChIsoInToOutIndex( index, prefix );
    Copyph_SCRPhoIsoInToOutIndex( index, prefix );
    Copyph_SCRNeuIsoInToOutIndex( index, prefix );
    Copyph_SCRChIso04InToOutIndex( index, prefix );
    Copyph_SCRPhoIso04InToOutIndex( index, prefix );
    Copyph_SCRNeuIso04InToOutIndex( index, prefix );
    Copyph_RandConeChIsoInToOutIndex( index, prefix );
    Copyph_RandConePhoIsoInToOutIndex( index, prefix );
    Copyph_RandConeNeuIsoInToOutIndex( index, prefix );
    Copyph_RandConeChIso04InToOutIndex( index, prefix );
    Copyph_RandConePhoIso04InToOutIndex( index, prefix );
    Copyph_RandConeNeuIso04InToOutIndex( index, prefix );
    Copyph_eleVetoInToOutIndex( index, prefix );
    Copyph_hasPixSeedInToOutIndex( index, prefix );
    Copyph_drToTrkInToOutIndex( index, prefix );
    Copyph_isConvInToOutIndex( index, prefix );
    Copyph_conv_nTrkInToOutIndex( index, prefix );
    Copyph_conv_vtx_xInToOutIndex( index, prefix );
    Copyph_conv_vtx_yInToOutIndex( index, prefix );
    Copyph_conv_vtx_zInToOutIndex( index, prefix );
    Copyph_conv_ptin1InToOutIndex( index, prefix );
    Copyph_conv_ptin2InToOutIndex( index, prefix );
    Copyph_conv_ptout1InToOutIndex( index, prefix );
    Copyph_conv_ptout2InToOutIndex( index, prefix );
    Copyph_passTightInToOutIndex( index, prefix );
    Copyph_passMediumInToOutIndex( index, prefix );
    Copyph_passLooseInToOutIndex( index, prefix );
    Copyph_passLooseNoSIEIEInToOutIndex( index, prefix );
    Copyph_passHOverELooseInToOutIndex( index, prefix );
    Copyph_passHOverEMediumInToOutIndex( index, prefix );
    Copyph_passHOverETightInToOutIndex( index, prefix );
    Copyph_passSIEIELooseInToOutIndex( index, prefix );
    Copyph_passSIEIEMediumInToOutIndex( index, prefix );
    Copyph_passSIEIETightInToOutIndex( index, prefix );
    Copyph_passChIsoCorrLooseInToOutIndex( index, prefix );
    Copyph_passChIsoCorrMediumInToOutIndex( index, prefix );
    Copyph_passChIsoCorrTightInToOutIndex( index, prefix );
    Copyph_passNeuIsoCorrLooseInToOutIndex( index, prefix );
    Copyph_passNeuIsoCorrMediumInToOutIndex( index, prefix );
    Copyph_passNeuIsoCorrTightInToOutIndex( index, prefix );
    Copyph_passPhoIsoCorrLooseInToOutIndex( index, prefix );
    Copyph_passPhoIsoCorrMediumInToOutIndex( index, prefix );
    Copyph_passPhoIsoCorrTightInToOutIndex( index, prefix );
    Copyph_truthMatch_elInToOutIndex( index, prefix );
    Copyph_truthMinDR_elInToOutIndex( index, prefix );
    Copyph_truthMatchPt_elInToOutIndex( index, prefix );
    Copyph_truthMatch_phInToOutIndex( index, prefix );
    Copyph_truthMinDR_phInToOutIndex( index, prefix );
    Copyph_truthMatchPt_phInToOutIndex( index, prefix );
    Copyph_truthMatchMotherPID_phInToOutIndex( index, prefix );
    Copyph_hasSLConvInToOutIndex( index, prefix );
    Copyph_pass_mva_preselInToOutIndex( index, prefix );
    Copyph_mvascoreInToOutIndex( index, prefix );
    Copyph_IsEBInToOutIndex( index, prefix );
    Copyph_IsEEInToOutIndex( index, prefix );
    Copyjet_ptInToOutIndex( index, prefix );
    Copyjet_etaInToOutIndex( index, prefix );
    Copyjet_phiInToOutIndex( index, prefix );
    Copyjet_eInToOutIndex( index, prefix );
    Copyph_trigMatch_elInToOutIndex( index, prefix );
    Copytruelep_ptInToOutIndex( index, prefix );
    Copytruelep_etaInToOutIndex( index, prefix );
    Copytruelep_phiInToOutIndex( index, prefix );
    Copytruelep_eInToOutIndex( index, prefix );
    Copytruelep_isElecInToOutIndex( index, prefix );
    Copytruelep_isMuonInToOutIndex( index, prefix );
    Copytruelep_motherPIDInToOutIndex( index, prefix );
    Copytrueph_ptInToOutIndex( index, prefix );
    Copytrueph_etaInToOutIndex( index, prefix );
    Copytrueph_phiInToOutIndex( index, prefix );
    Copytrueph_motherPIDInToOutIndex( index, prefix );
    Copytrueph_parentageInToOutIndex( index, prefix );
    Copytrueph_nearestLepDRInToOutIndex( index, prefix );
    Copytrueph_nearestQrkDRInToOutIndex( index, prefix );
}; 

void ClearOutputPrefix ( const std::string & prefix ) {
    ClearOutputmcPID( prefix );
    ClearOutputmcPt( prefix );
    ClearOutputmcEta( prefix );
    ClearOutputmcPhi( prefix );
    ClearOutputmcE( prefix );
    ClearOutputmcGMomPID( prefix );
    ClearOutputmcMomPID( prefix );
    ClearOutputmcParentage( prefix );
    ClearOutputmcStatus( prefix );
    ClearOutputnPU( prefix );
    ClearOutputpuTrue( prefix );
    ClearOutputel_pt( prefix );
    ClearOutputel_eta( prefix );
    ClearOutputel_sceta( prefix );
    ClearOutputel_phi( prefix );
    ClearOutputel_e( prefix );
    ClearOutputel_pt_uncorr( prefix );
    ClearOutputel_mva_trig( prefix );
    ClearOutputel_mva_nontrig( prefix );
    ClearOutputel_d0pv( prefix );
    ClearOutputel_z0pv( prefix );
    ClearOutputel_sigmaIEIE( prefix );
    ClearOutputel_pfiso30( prefix );
    ClearOutputel_pfiso40( prefix );
    ClearOutputel_triggerMatch( prefix );
    ClearOutputel_hasMatchedConv( prefix );
    ClearOutputel_passTight( prefix );
    ClearOutputel_passMedium( prefix );
    ClearOutputel_passLoose( prefix );
    ClearOutputel_passVeryLoose( prefix );
    ClearOutputel_passTightTrig( prefix );
    ClearOutputel_passMvaTrig( prefix );
    ClearOutputel_passMvaNonTrig( prefix );
    ClearOutputel_truthMatch_el( prefix );
    ClearOutputel_truthMinDR_el( prefix );
    ClearOutputel_truthMatchPt_el( prefix );
    ClearOutputmu_pt( prefix );
    ClearOutputmu_eta( prefix );
    ClearOutputmu_phi( prefix );
    ClearOutputmu_e( prefix );
    ClearOutputmu_pt_uncorr( prefix );
    ClearOutputmu_pfIso_ch( prefix );
    ClearOutputmu_pfIso_nh( prefix );
    ClearOutputmu_pfIso_pho( prefix );
    ClearOutputmu_pfIso_pu( prefix );
    ClearOutputmu_corrIso( prefix );
    ClearOutputmu_triggerMatch( prefix );
    ClearOutputmu_truthMatch( prefix );
    ClearOutputmu_truthMinDR( prefix );
    ClearOutputph_pt( prefix );
    ClearOutputph_eta( prefix );
    ClearOutputph_sceta( prefix );
    ClearOutputph_phi( prefix );
    ClearOutputph_e( prefix );
    ClearOutputph_HoverE( prefix );
    ClearOutputph_HoverE12( prefix );
    ClearOutputph_sigmaIEIE( prefix );
    ClearOutputph_sigmaIEIP( prefix );
    ClearOutputph_r9( prefix );
    ClearOutputph_E1x3( prefix );
    ClearOutputph_E2x2( prefix );
    ClearOutputph_E5x5( prefix );
    ClearOutputph_E2x5Max( prefix );
    ClearOutputph_SCetaWidth( prefix );
    ClearOutputph_SCphiWidth( prefix );
    ClearOutputph_ESEffSigmaRR( prefix );
    ClearOutputph_hcalIsoDR03( prefix );
    ClearOutputph_trkIsoHollowDR03( prefix );
    ClearOutputph_chgpfIsoDR02( prefix );
    ClearOutputph_pfChIsoWorst( prefix );
    ClearOutputph_chIso( prefix );
    ClearOutputph_neuIso( prefix );
    ClearOutputph_phoIso( prefix );
    ClearOutputph_chIsoCorr( prefix );
    ClearOutputph_neuIsoCorr( prefix );
    ClearOutputph_phoIsoCorr( prefix );
    ClearOutputph_SCRChIso( prefix );
    ClearOutputph_SCRPhoIso( prefix );
    ClearOutputph_SCRNeuIso( prefix );
    ClearOutputph_SCRChIso04( prefix );
    ClearOutputph_SCRPhoIso04( prefix );
    ClearOutputph_SCRNeuIso04( prefix );
    ClearOutputph_RandConeChIso( prefix );
    ClearOutputph_RandConePhoIso( prefix );
    ClearOutputph_RandConeNeuIso( prefix );
    ClearOutputph_RandConeChIso04( prefix );
    ClearOutputph_RandConePhoIso04( prefix );
    ClearOutputph_RandConeNeuIso04( prefix );
    ClearOutputph_eleVeto( prefix );
    ClearOutputph_hasPixSeed( prefix );
    ClearOutputph_drToTrk( prefix );
    ClearOutputph_isConv( prefix );
    ClearOutputph_conv_nTrk( prefix );
    ClearOutputph_conv_vtx_x( prefix );
    ClearOutputph_conv_vtx_y( prefix );
    ClearOutputph_conv_vtx_z( prefix );
    ClearOutputph_conv_ptin1( prefix );
    ClearOutputph_conv_ptin2( prefix );
    ClearOutputph_conv_ptout1( prefix );
    ClearOutputph_conv_ptout2( prefix );
    ClearOutputph_passTight( prefix );
    ClearOutputph_passMedium( prefix );
    ClearOutputph_passLoose( prefix );
    ClearOutputph_passLooseNoSIEIE( prefix );
    ClearOutputph_passHOverELoose( prefix );
    ClearOutputph_passHOverEMedium( prefix );
    ClearOutputph_passHOverETight( prefix );
    ClearOutputph_passSIEIELoose( prefix );
    ClearOutputph_passSIEIEMedium( prefix );
    ClearOutputph_passSIEIETight( prefix );
    ClearOutputph_passChIsoCorrLoose( prefix );
    ClearOutputph_passChIsoCorrMedium( prefix );
    ClearOutputph_passChIsoCorrTight( prefix );
    ClearOutputph_passNeuIsoCorrLoose( prefix );
    ClearOutputph_passNeuIsoCorrMedium( prefix );
    ClearOutputph_passNeuIsoCorrTight( prefix );
    ClearOutputph_passPhoIsoCorrLoose( prefix );
    ClearOutputph_passPhoIsoCorrMedium( prefix );
    ClearOutputph_passPhoIsoCorrTight( prefix );
    ClearOutputph_truthMatch_el( prefix );
    ClearOutputph_truthMinDR_el( prefix );
    ClearOutputph_truthMatchPt_el( prefix );
    ClearOutputph_truthMatch_ph( prefix );
    ClearOutputph_truthMinDR_ph( prefix );
    ClearOutputph_truthMatchPt_ph( prefix );
    ClearOutputph_truthMatchMotherPID_ph( prefix );
    ClearOutputph_hasSLConv( prefix );
    ClearOutputph_pass_mva_presel( prefix );
    ClearOutputph_mvascore( prefix );
    ClearOutputph_IsEB( prefix );
    ClearOutputph_IsEE( prefix );
    ClearOutputjet_pt( prefix );
    ClearOutputjet_eta( prefix );
    ClearOutputjet_phi( prefix );
    ClearOutputjet_e( prefix );
    ClearOutputph_trigMatch_el( prefix );
    ClearOutputtruelep_pt( prefix );
    ClearOutputtruelep_eta( prefix );
    ClearOutputtruelep_phi( prefix );
    ClearOutputtruelep_e( prefix );
    ClearOutputtruelep_isElec( prefix );
    ClearOutputtruelep_isMuon( prefix );
    ClearOutputtruelep_motherPID( prefix );
    ClearOutputtrueph_pt( prefix );
    ClearOutputtrueph_eta( prefix );
    ClearOutputtrueph_phi( prefix );
    ClearOutputtrueph_motherPID( prefix );
    ClearOutputtrueph_parentage( prefix );
    ClearOutputtrueph_nearestLepDR( prefix );
    ClearOutputtrueph_nearestQrkDR( prefix );
}; 

void CopynVtxInToOut( std::string prefix ) { 

    std::string my_name = "nVtx";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::nVtx = IN::nVtx;
}; 

 void CopynVtxBSInToOut( std::string prefix ) { 

    std::string my_name = "nVtxBS";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::nVtxBS = IN::nVtxBS;
}; 

 void CopynMCInToOut( std::string prefix ) { 

    std::string my_name = "nMC";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::nMC = IN::nMC;
}; 

 void CopymcPIDInToOut( std::string prefix ) { 

    std::string my_name = "mcPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mcPID = std::vector<int>(*IN::mcPID);
}; 

 void CopymcPIDInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mcPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mcPID->size() ) {
         std::cout << "Vector size exceeded for branch IN::mcPID" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mcPID" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mcPID->push_back( IN::mcPID->at(index) ); 
 }; 

 void ClearOutputmcPID( std::string  prefix ) { 

    std::string my_name = "mcPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mcPID, prefix = " << prefix << std::endl; 
     OUT::mcPID->clear(); 
 }; 

 void CopymcPtInToOut( std::string prefix ) { 

    std::string my_name = "mcPt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mcPt = std::vector<float>(*IN::mcPt);
}; 

 void CopymcPtInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mcPt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mcPt->size() ) {
         std::cout << "Vector size exceeded for branch IN::mcPt" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mcPt" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mcPt->push_back( IN::mcPt->at(index) ); 
 }; 

 void ClearOutputmcPt( std::string  prefix ) { 

    std::string my_name = "mcPt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mcPt, prefix = " << prefix << std::endl; 
     OUT::mcPt->clear(); 
 }; 

 void CopymcEtaInToOut( std::string prefix ) { 

    std::string my_name = "mcEta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mcEta = std::vector<float>(*IN::mcEta);
}; 

 void CopymcEtaInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mcEta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mcEta->size() ) {
         std::cout << "Vector size exceeded for branch IN::mcEta" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mcEta" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mcEta->push_back( IN::mcEta->at(index) ); 
 }; 

 void ClearOutputmcEta( std::string  prefix ) { 

    std::string my_name = "mcEta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mcEta, prefix = " << prefix << std::endl; 
     OUT::mcEta->clear(); 
 }; 

 void CopymcPhiInToOut( std::string prefix ) { 

    std::string my_name = "mcPhi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mcPhi = std::vector<float>(*IN::mcPhi);
}; 

 void CopymcPhiInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mcPhi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mcPhi->size() ) {
         std::cout << "Vector size exceeded for branch IN::mcPhi" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mcPhi" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mcPhi->push_back( IN::mcPhi->at(index) ); 
 }; 

 void ClearOutputmcPhi( std::string  prefix ) { 

    std::string my_name = "mcPhi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mcPhi, prefix = " << prefix << std::endl; 
     OUT::mcPhi->clear(); 
 }; 

 void CopymcEInToOut( std::string prefix ) { 

    std::string my_name = "mcE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mcE = std::vector<float>(*IN::mcE);
}; 

 void CopymcEInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mcE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mcE->size() ) {
         std::cout << "Vector size exceeded for branch IN::mcE" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mcE" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mcE->push_back( IN::mcE->at(index) ); 
 }; 

 void ClearOutputmcE( std::string  prefix ) { 

    std::string my_name = "mcE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mcE, prefix = " << prefix << std::endl; 
     OUT::mcE->clear(); 
 }; 

 void CopymcGMomPIDInToOut( std::string prefix ) { 

    std::string my_name = "mcGMomPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mcGMomPID = std::vector<int>(*IN::mcGMomPID);
}; 

 void CopymcGMomPIDInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mcGMomPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mcGMomPID->size() ) {
         std::cout << "Vector size exceeded for branch IN::mcGMomPID" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mcGMomPID" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mcGMomPID->push_back( IN::mcGMomPID->at(index) ); 
 }; 

 void ClearOutputmcGMomPID( std::string  prefix ) { 

    std::string my_name = "mcGMomPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mcGMomPID, prefix = " << prefix << std::endl; 
     OUT::mcGMomPID->clear(); 
 }; 

 void CopymcMomPIDInToOut( std::string prefix ) { 

    std::string my_name = "mcMomPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mcMomPID = std::vector<int>(*IN::mcMomPID);
}; 

 void CopymcMomPIDInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mcMomPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mcMomPID->size() ) {
         std::cout << "Vector size exceeded for branch IN::mcMomPID" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mcMomPID" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mcMomPID->push_back( IN::mcMomPID->at(index) ); 
 }; 

 void ClearOutputmcMomPID( std::string  prefix ) { 

    std::string my_name = "mcMomPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mcMomPID, prefix = " << prefix << std::endl; 
     OUT::mcMomPID->clear(); 
 }; 

 void CopymcParentageInToOut( std::string prefix ) { 

    std::string my_name = "mcParentage";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mcParentage = std::vector<int>(*IN::mcParentage);
}; 

 void CopymcParentageInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mcParentage";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mcParentage->size() ) {
         std::cout << "Vector size exceeded for branch IN::mcParentage" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mcParentage" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mcParentage->push_back( IN::mcParentage->at(index) ); 
 }; 

 void ClearOutputmcParentage( std::string  prefix ) { 

    std::string my_name = "mcParentage";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mcParentage, prefix = " << prefix << std::endl; 
     OUT::mcParentage->clear(); 
 }; 

 void CopymcStatusInToOut( std::string prefix ) { 

    std::string my_name = "mcStatus";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mcStatus = std::vector<int>(*IN::mcStatus);
}; 

 void CopymcStatusInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mcStatus";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mcStatus->size() ) {
         std::cout << "Vector size exceeded for branch IN::mcStatus" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mcStatus" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mcStatus->push_back( IN::mcStatus->at(index) ); 
 }; 

 void ClearOutputmcStatus( std::string  prefix ) { 

    std::string my_name = "mcStatus";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mcStatus, prefix = " << prefix << std::endl; 
     OUT::mcStatus->clear(); 
 }; 

 void CopynPUInToOut( std::string prefix ) { 

    std::string my_name = "nPU";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::nPU = std::vector<int>(*IN::nPU);
}; 

 void CopynPUInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "nPU";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::nPU->size() ) {
         std::cout << "Vector size exceeded for branch IN::nPU" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible nPU" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::nPU->push_back( IN::nPU->at(index) ); 
 }; 

 void ClearOutputnPU( std::string  prefix ) { 

    std::string my_name = "nPU";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible nPU, prefix = " << prefix << std::endl; 
     OUT::nPU->clear(); 
 }; 

 void CopypuTrueInToOut( std::string prefix ) { 

    std::string my_name = "puTrue";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::puTrue = std::vector<float>(*IN::puTrue);
}; 

 void CopypuTrueInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "puTrue";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::puTrue->size() ) {
         std::cout << "Vector size exceeded for branch IN::puTrue" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible puTrue" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::puTrue->push_back( IN::puTrue->at(index) ); 
 }; 

 void ClearOutputpuTrue( std::string  prefix ) { 

    std::string my_name = "puTrue";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible puTrue, prefix = " << prefix << std::endl; 
     OUT::puTrue->clear(); 
 }; 

 void CopypfMETInToOut( std::string prefix ) { 

    std::string my_name = "pfMET";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pfMET = IN::pfMET;
}; 

 void CopypfMETPhiInToOut( std::string prefix ) { 

    std::string my_name = "pfMETPhi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pfMETPhi = IN::pfMETPhi;
}; 

 void CopypfMETsumEtInToOut( std::string prefix ) { 

    std::string my_name = "pfMETsumEt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pfMETsumEt = IN::pfMETsumEt;
}; 

 void CopypfMETmEtSigInToOut( std::string prefix ) { 

    std::string my_name = "pfMETmEtSig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pfMETmEtSig = IN::pfMETmEtSig;
}; 

 void CopypfMETSigInToOut( std::string prefix ) { 

    std::string my_name = "pfMETSig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pfMETSig = IN::pfMETSig;
}; 

 void CopyrecoPfMETInToOut( std::string prefix ) { 

    std::string my_name = "recoPfMET";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::recoPfMET = IN::recoPfMET;
}; 

 void CopyrecoPfMETPhiInToOut( std::string prefix ) { 

    std::string my_name = "recoPfMETPhi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::recoPfMETPhi = IN::recoPfMETPhi;
}; 

 void CopyrecoPfMETsumEtInToOut( std::string prefix ) { 

    std::string my_name = "recoPfMETsumEt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::recoPfMETsumEt = IN::recoPfMETsumEt;
}; 

 void CopyrecoPfMETmEtSigInToOut( std::string prefix ) { 

    std::string my_name = "recoPfMETmEtSig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::recoPfMETmEtSig = IN::recoPfMETmEtSig;
}; 

 void CopyrecoPfMETSigInToOut( std::string prefix ) { 

    std::string my_name = "recoPfMETSig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::recoPfMETSig = IN::recoPfMETSig;
}; 

 void Copyrho2012InToOut( std::string prefix ) { 

    std::string my_name = "rho2012";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::rho2012 = IN::rho2012;
}; 

 void Copyel_nInToOut( std::string prefix ) { 

    std::string my_name = "el_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::el_n = IN::el_n;
}; 

 void Copymu_nInToOut( std::string prefix ) { 

    std::string my_name = "mu_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::mu_n = IN::mu_n;
}; 

 void Copyph_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_n = IN::ph_n;
}; 

 void Copyjet_nInToOut( std::string prefix ) { 

    std::string my_name = "jet_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::jet_n = IN::jet_n;
}; 

 void Copyvtx_nInToOut( std::string prefix ) { 

    std::string my_name = "vtx_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::vtx_n = IN::vtx_n;
}; 

 void Copyel_ptInToOut( std::string prefix ) { 

    std::string my_name = "el_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_pt = std::vector<float>(*IN::el_pt);
}; 

 void Copyel_ptInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_pt->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_pt" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_pt" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_pt->push_back( IN::el_pt->at(index) ); 
 }; 

 void ClearOutputel_pt( std::string  prefix ) { 

    std::string my_name = "el_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_pt, prefix = " << prefix << std::endl; 
     OUT::el_pt->clear(); 
 }; 

 void Copyel_etaInToOut( std::string prefix ) { 

    std::string my_name = "el_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_eta = std::vector<float>(*IN::el_eta);
}; 

 void Copyel_etaInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_eta->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_eta" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_eta" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_eta->push_back( IN::el_eta->at(index) ); 
 }; 

 void ClearOutputel_eta( std::string  prefix ) { 

    std::string my_name = "el_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_eta, prefix = " << prefix << std::endl; 
     OUT::el_eta->clear(); 
 }; 

 void Copyel_scetaInToOut( std::string prefix ) { 

    std::string my_name = "el_sceta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_sceta = std::vector<float>(*IN::el_sceta);
}; 

 void Copyel_scetaInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_sceta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_sceta->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_sceta" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_sceta" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_sceta->push_back( IN::el_sceta->at(index) ); 
 }; 

 void ClearOutputel_sceta( std::string  prefix ) { 

    std::string my_name = "el_sceta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_sceta, prefix = " << prefix << std::endl; 
     OUT::el_sceta->clear(); 
 }; 

 void Copyel_phiInToOut( std::string prefix ) { 

    std::string my_name = "el_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_phi = std::vector<float>(*IN::el_phi);
}; 

 void Copyel_phiInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_phi->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_phi" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_phi" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_phi->push_back( IN::el_phi->at(index) ); 
 }; 

 void ClearOutputel_phi( std::string  prefix ) { 

    std::string my_name = "el_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_phi, prefix = " << prefix << std::endl; 
     OUT::el_phi->clear(); 
 }; 

 void Copyel_eInToOut( std::string prefix ) { 

    std::string my_name = "el_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_e = std::vector<float>(*IN::el_e);
}; 

 void Copyel_eInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_e->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_e" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_e" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_e->push_back( IN::el_e->at(index) ); 
 }; 

 void ClearOutputel_e( std::string  prefix ) { 

    std::string my_name = "el_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_e, prefix = " << prefix << std::endl; 
     OUT::el_e->clear(); 
 }; 

 void Copyel_pt_uncorrInToOut( std::string prefix ) { 

    std::string my_name = "el_pt_uncorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_pt_uncorr = std::vector<float>(*IN::el_pt_uncorr);
}; 

 void Copyel_pt_uncorrInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_pt_uncorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_pt_uncorr->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_pt_uncorr" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_pt_uncorr" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_pt_uncorr->push_back( IN::el_pt_uncorr->at(index) ); 
 }; 

 void ClearOutputel_pt_uncorr( std::string  prefix ) { 

    std::string my_name = "el_pt_uncorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_pt_uncorr, prefix = " << prefix << std::endl; 
     OUT::el_pt_uncorr->clear(); 
 }; 

 void Copyel_mva_trigInToOut( std::string prefix ) { 

    std::string my_name = "el_mva_trig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_mva_trig = std::vector<float>(*IN::el_mva_trig);
}; 

 void Copyel_mva_trigInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_mva_trig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_mva_trig->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_mva_trig" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_mva_trig" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_mva_trig->push_back( IN::el_mva_trig->at(index) ); 
 }; 

 void ClearOutputel_mva_trig( std::string  prefix ) { 

    std::string my_name = "el_mva_trig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_mva_trig, prefix = " << prefix << std::endl; 
     OUT::el_mva_trig->clear(); 
 }; 

 void Copyel_mva_nontrigInToOut( std::string prefix ) { 

    std::string my_name = "el_mva_nontrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_mva_nontrig = std::vector<float>(*IN::el_mva_nontrig);
}; 

 void Copyel_mva_nontrigInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_mva_nontrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_mva_nontrig->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_mva_nontrig" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_mva_nontrig" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_mva_nontrig->push_back( IN::el_mva_nontrig->at(index) ); 
 }; 

 void ClearOutputel_mva_nontrig( std::string  prefix ) { 

    std::string my_name = "el_mva_nontrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_mva_nontrig, prefix = " << prefix << std::endl; 
     OUT::el_mva_nontrig->clear(); 
 }; 

 void Copyel_d0pvInToOut( std::string prefix ) { 

    std::string my_name = "el_d0pv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_d0pv = std::vector<float>(*IN::el_d0pv);
}; 

 void Copyel_d0pvInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_d0pv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_d0pv->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_d0pv" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_d0pv" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_d0pv->push_back( IN::el_d0pv->at(index) ); 
 }; 

 void ClearOutputel_d0pv( std::string  prefix ) { 

    std::string my_name = "el_d0pv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_d0pv, prefix = " << prefix << std::endl; 
     OUT::el_d0pv->clear(); 
 }; 

 void Copyel_z0pvInToOut( std::string prefix ) { 

    std::string my_name = "el_z0pv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_z0pv = std::vector<float>(*IN::el_z0pv);
}; 

 void Copyel_z0pvInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_z0pv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_z0pv->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_z0pv" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_z0pv" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_z0pv->push_back( IN::el_z0pv->at(index) ); 
 }; 

 void ClearOutputel_z0pv( std::string  prefix ) { 

    std::string my_name = "el_z0pv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_z0pv, prefix = " << prefix << std::endl; 
     OUT::el_z0pv->clear(); 
 }; 

 void Copyel_sigmaIEIEInToOut( std::string prefix ) { 

    std::string my_name = "el_sigmaIEIE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_sigmaIEIE = std::vector<float>(*IN::el_sigmaIEIE);
}; 

 void Copyel_sigmaIEIEInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_sigmaIEIE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_sigmaIEIE->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_sigmaIEIE" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_sigmaIEIE" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_sigmaIEIE->push_back( IN::el_sigmaIEIE->at(index) ); 
 }; 

 void ClearOutputel_sigmaIEIE( std::string  prefix ) { 

    std::string my_name = "el_sigmaIEIE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_sigmaIEIE, prefix = " << prefix << std::endl; 
     OUT::el_sigmaIEIE->clear(); 
 }; 

 void Copyel_pfiso30InToOut( std::string prefix ) { 

    std::string my_name = "el_pfiso30";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_pfiso30 = std::vector<float>(*IN::el_pfiso30);
}; 

 void Copyel_pfiso30InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_pfiso30";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_pfiso30->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_pfiso30" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_pfiso30" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_pfiso30->push_back( IN::el_pfiso30->at(index) ); 
 }; 

 void ClearOutputel_pfiso30( std::string  prefix ) { 

    std::string my_name = "el_pfiso30";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_pfiso30, prefix = " << prefix << std::endl; 
     OUT::el_pfiso30->clear(); 
 }; 

 void Copyel_pfiso40InToOut( std::string prefix ) { 

    std::string my_name = "el_pfiso40";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_pfiso40 = std::vector<float>(*IN::el_pfiso40);
}; 

 void Copyel_pfiso40InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_pfiso40";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_pfiso40->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_pfiso40" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_pfiso40" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_pfiso40->push_back( IN::el_pfiso40->at(index) ); 
 }; 

 void ClearOutputel_pfiso40( std::string  prefix ) { 

    std::string my_name = "el_pfiso40";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_pfiso40, prefix = " << prefix << std::endl; 
     OUT::el_pfiso40->clear(); 
 }; 

 void Copyel_triggerMatchInToOut( std::string prefix ) { 

    std::string my_name = "el_triggerMatch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_triggerMatch = std::vector<bool>(*IN::el_triggerMatch);
}; 

 void Copyel_triggerMatchInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_triggerMatch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_triggerMatch->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_triggerMatch" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_triggerMatch" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_triggerMatch->push_back( IN::el_triggerMatch->at(index) ); 
 }; 

 void ClearOutputel_triggerMatch( std::string  prefix ) { 

    std::string my_name = "el_triggerMatch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_triggerMatch, prefix = " << prefix << std::endl; 
     OUT::el_triggerMatch->clear(); 
 }; 

 void Copyel_hasMatchedConvInToOut( std::string prefix ) { 

    std::string my_name = "el_hasMatchedConv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_hasMatchedConv = std::vector<bool>(*IN::el_hasMatchedConv);
}; 

 void Copyel_hasMatchedConvInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_hasMatchedConv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_hasMatchedConv->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_hasMatchedConv" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_hasMatchedConv" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_hasMatchedConv->push_back( IN::el_hasMatchedConv->at(index) ); 
 }; 

 void ClearOutputel_hasMatchedConv( std::string  prefix ) { 

    std::string my_name = "el_hasMatchedConv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_hasMatchedConv, prefix = " << prefix << std::endl; 
     OUT::el_hasMatchedConv->clear(); 
 }; 

 void Copyel_passTightInToOut( std::string prefix ) { 

    std::string my_name = "el_passTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_passTight = std::vector<bool>(*IN::el_passTight);
}; 

 void Copyel_passTightInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_passTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_passTight->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_passTight" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_passTight" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_passTight->push_back( IN::el_passTight->at(index) ); 
 }; 

 void ClearOutputel_passTight( std::string  prefix ) { 

    std::string my_name = "el_passTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_passTight, prefix = " << prefix << std::endl; 
     OUT::el_passTight->clear(); 
 }; 

 void Copyel_passMediumInToOut( std::string prefix ) { 

    std::string my_name = "el_passMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_passMedium = std::vector<bool>(*IN::el_passMedium);
}; 

 void Copyel_passMediumInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_passMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_passMedium->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_passMedium" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_passMedium" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_passMedium->push_back( IN::el_passMedium->at(index) ); 
 }; 

 void ClearOutputel_passMedium( std::string  prefix ) { 

    std::string my_name = "el_passMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_passMedium, prefix = " << prefix << std::endl; 
     OUT::el_passMedium->clear(); 
 }; 

 void Copyel_passLooseInToOut( std::string prefix ) { 

    std::string my_name = "el_passLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_passLoose = std::vector<bool>(*IN::el_passLoose);
}; 

 void Copyel_passLooseInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_passLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_passLoose->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_passLoose" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_passLoose" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_passLoose->push_back( IN::el_passLoose->at(index) ); 
 }; 

 void ClearOutputel_passLoose( std::string  prefix ) { 

    std::string my_name = "el_passLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_passLoose, prefix = " << prefix << std::endl; 
     OUT::el_passLoose->clear(); 
 }; 

 void Copyel_passVeryLooseInToOut( std::string prefix ) { 

    std::string my_name = "el_passVeryLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_passVeryLoose = std::vector<bool>(*IN::el_passVeryLoose);
}; 

 void Copyel_passVeryLooseInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_passVeryLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_passVeryLoose->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_passVeryLoose" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_passVeryLoose" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_passVeryLoose->push_back( IN::el_passVeryLoose->at(index) ); 
 }; 

 void ClearOutputel_passVeryLoose( std::string  prefix ) { 

    std::string my_name = "el_passVeryLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_passVeryLoose, prefix = " << prefix << std::endl; 
     OUT::el_passVeryLoose->clear(); 
 }; 

 void Copyel_passTightTrigInToOut( std::string prefix ) { 

    std::string my_name = "el_passTightTrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_passTightTrig = std::vector<bool>(*IN::el_passTightTrig);
}; 

 void Copyel_passTightTrigInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_passTightTrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_passTightTrig->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_passTightTrig" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_passTightTrig" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_passTightTrig->push_back( IN::el_passTightTrig->at(index) ); 
 }; 

 void ClearOutputel_passTightTrig( std::string  prefix ) { 

    std::string my_name = "el_passTightTrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_passTightTrig, prefix = " << prefix << std::endl; 
     OUT::el_passTightTrig->clear(); 
 }; 

 void Copyel_passMvaTrigInToOut( std::string prefix ) { 

    std::string my_name = "el_passMvaTrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_passMvaTrig = std::vector<bool>(*IN::el_passMvaTrig);
}; 

 void Copyel_passMvaTrigInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_passMvaTrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_passMvaTrig->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_passMvaTrig" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_passMvaTrig" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_passMvaTrig->push_back( IN::el_passMvaTrig->at(index) ); 
 }; 

 void ClearOutputel_passMvaTrig( std::string  prefix ) { 

    std::string my_name = "el_passMvaTrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_passMvaTrig, prefix = " << prefix << std::endl; 
     OUT::el_passMvaTrig->clear(); 
 }; 

 void Copyel_passMvaNonTrigInToOut( std::string prefix ) { 

    std::string my_name = "el_passMvaNonTrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_passMvaNonTrig = std::vector<bool>(*IN::el_passMvaNonTrig);
}; 

 void Copyel_passMvaNonTrigInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_passMvaNonTrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_passMvaNonTrig->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_passMvaNonTrig" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_passMvaNonTrig" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_passMvaNonTrig->push_back( IN::el_passMvaNonTrig->at(index) ); 
 }; 

 void ClearOutputel_passMvaNonTrig( std::string  prefix ) { 

    std::string my_name = "el_passMvaNonTrig";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_passMvaNonTrig, prefix = " << prefix << std::endl; 
     OUT::el_passMvaNonTrig->clear(); 
 }; 

 void Copyel_truthMatch_elInToOut( std::string prefix ) { 

    std::string my_name = "el_truthMatch_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_truthMatch_el = std::vector<bool>(*IN::el_truthMatch_el);
}; 

 void Copyel_truthMatch_elInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_truthMatch_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_truthMatch_el->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_truthMatch_el" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_truthMatch_el" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_truthMatch_el->push_back( IN::el_truthMatch_el->at(index) ); 
 }; 

 void ClearOutputel_truthMatch_el( std::string  prefix ) { 

    std::string my_name = "el_truthMatch_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_truthMatch_el, prefix = " << prefix << std::endl; 
     OUT::el_truthMatch_el->clear(); 
 }; 

 void Copyel_truthMinDR_elInToOut( std::string prefix ) { 

    std::string my_name = "el_truthMinDR_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_truthMinDR_el = std::vector<float>(*IN::el_truthMinDR_el);
}; 

 void Copyel_truthMinDR_elInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_truthMinDR_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_truthMinDR_el->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_truthMinDR_el" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_truthMinDR_el" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_truthMinDR_el->push_back( IN::el_truthMinDR_el->at(index) ); 
 }; 

 void ClearOutputel_truthMinDR_el( std::string  prefix ) { 

    std::string my_name = "el_truthMinDR_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_truthMinDR_el, prefix = " << prefix << std::endl; 
     OUT::el_truthMinDR_el->clear(); 
 }; 

 void Copyel_truthMatchPt_elInToOut( std::string prefix ) { 

    std::string my_name = "el_truthMatchPt_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::el_truthMatchPt_el = std::vector<float>(*IN::el_truthMatchPt_el);
}; 

 void Copyel_truthMatchPt_elInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "el_truthMatchPt_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::el_truthMatchPt_el->size() ) {
         std::cout << "Vector size exceeded for branch IN::el_truthMatchPt_el" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible el_truthMatchPt_el" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::el_truthMatchPt_el->push_back( IN::el_truthMatchPt_el->at(index) ); 
 }; 

 void ClearOutputel_truthMatchPt_el( std::string  prefix ) { 

    std::string my_name = "el_truthMatchPt_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible el_truthMatchPt_el, prefix = " << prefix << std::endl; 
     OUT::el_truthMatchPt_el->clear(); 
 }; 

 void Copymu_ptInToOut( std::string prefix ) { 

    std::string my_name = "mu_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_pt = std::vector<float>(*IN::mu_pt);
}; 

 void Copymu_ptInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_pt->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_pt" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_pt" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_pt->push_back( IN::mu_pt->at(index) ); 
 }; 

 void ClearOutputmu_pt( std::string  prefix ) { 

    std::string my_name = "mu_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_pt, prefix = " << prefix << std::endl; 
     OUT::mu_pt->clear(); 
 }; 

 void Copymu_etaInToOut( std::string prefix ) { 

    std::string my_name = "mu_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_eta = std::vector<float>(*IN::mu_eta);
}; 

 void Copymu_etaInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_eta->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_eta" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_eta" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_eta->push_back( IN::mu_eta->at(index) ); 
 }; 

 void ClearOutputmu_eta( std::string  prefix ) { 

    std::string my_name = "mu_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_eta, prefix = " << prefix << std::endl; 
     OUT::mu_eta->clear(); 
 }; 

 void Copymu_phiInToOut( std::string prefix ) { 

    std::string my_name = "mu_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_phi = std::vector<float>(*IN::mu_phi);
}; 

 void Copymu_phiInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_phi->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_phi" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_phi" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_phi->push_back( IN::mu_phi->at(index) ); 
 }; 

 void ClearOutputmu_phi( std::string  prefix ) { 

    std::string my_name = "mu_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_phi, prefix = " << prefix << std::endl; 
     OUT::mu_phi->clear(); 
 }; 

 void Copymu_eInToOut( std::string prefix ) { 

    std::string my_name = "mu_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_e = std::vector<float>(*IN::mu_e);
}; 

 void Copymu_eInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_e->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_e" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_e" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_e->push_back( IN::mu_e->at(index) ); 
 }; 

 void ClearOutputmu_e( std::string  prefix ) { 

    std::string my_name = "mu_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_e, prefix = " << prefix << std::endl; 
     OUT::mu_e->clear(); 
 }; 

 void Copymu_pt_uncorrInToOut( std::string prefix ) { 

    std::string my_name = "mu_pt_uncorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_pt_uncorr = std::vector<float>(*IN::mu_pt_uncorr);
}; 

 void Copymu_pt_uncorrInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_pt_uncorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_pt_uncorr->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_pt_uncorr" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_pt_uncorr" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_pt_uncorr->push_back( IN::mu_pt_uncorr->at(index) ); 
 }; 

 void ClearOutputmu_pt_uncorr( std::string  prefix ) { 

    std::string my_name = "mu_pt_uncorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_pt_uncorr, prefix = " << prefix << std::endl; 
     OUT::mu_pt_uncorr->clear(); 
 }; 

 void Copymu_pfIso_chInToOut( std::string prefix ) { 

    std::string my_name = "mu_pfIso_ch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_pfIso_ch = std::vector<float>(*IN::mu_pfIso_ch);
}; 

 void Copymu_pfIso_chInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_pfIso_ch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_pfIso_ch->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_pfIso_ch" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_pfIso_ch" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_pfIso_ch->push_back( IN::mu_pfIso_ch->at(index) ); 
 }; 

 void ClearOutputmu_pfIso_ch( std::string  prefix ) { 

    std::string my_name = "mu_pfIso_ch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_pfIso_ch, prefix = " << prefix << std::endl; 
     OUT::mu_pfIso_ch->clear(); 
 }; 

 void Copymu_pfIso_nhInToOut( std::string prefix ) { 

    std::string my_name = "mu_pfIso_nh";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_pfIso_nh = std::vector<float>(*IN::mu_pfIso_nh);
}; 

 void Copymu_pfIso_nhInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_pfIso_nh";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_pfIso_nh->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_pfIso_nh" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_pfIso_nh" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_pfIso_nh->push_back( IN::mu_pfIso_nh->at(index) ); 
 }; 

 void ClearOutputmu_pfIso_nh( std::string  prefix ) { 

    std::string my_name = "mu_pfIso_nh";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_pfIso_nh, prefix = " << prefix << std::endl; 
     OUT::mu_pfIso_nh->clear(); 
 }; 

 void Copymu_pfIso_phoInToOut( std::string prefix ) { 

    std::string my_name = "mu_pfIso_pho";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_pfIso_pho = std::vector<float>(*IN::mu_pfIso_pho);
}; 

 void Copymu_pfIso_phoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_pfIso_pho";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_pfIso_pho->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_pfIso_pho" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_pfIso_pho" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_pfIso_pho->push_back( IN::mu_pfIso_pho->at(index) ); 
 }; 

 void ClearOutputmu_pfIso_pho( std::string  prefix ) { 

    std::string my_name = "mu_pfIso_pho";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_pfIso_pho, prefix = " << prefix << std::endl; 
     OUT::mu_pfIso_pho->clear(); 
 }; 

 void Copymu_pfIso_puInToOut( std::string prefix ) { 

    std::string my_name = "mu_pfIso_pu";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_pfIso_pu = std::vector<float>(*IN::mu_pfIso_pu);
}; 

 void Copymu_pfIso_puInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_pfIso_pu";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_pfIso_pu->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_pfIso_pu" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_pfIso_pu" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_pfIso_pu->push_back( IN::mu_pfIso_pu->at(index) ); 
 }; 

 void ClearOutputmu_pfIso_pu( std::string  prefix ) { 

    std::string my_name = "mu_pfIso_pu";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_pfIso_pu, prefix = " << prefix << std::endl; 
     OUT::mu_pfIso_pu->clear(); 
 }; 

 void Copymu_corrIsoInToOut( std::string prefix ) { 

    std::string my_name = "mu_corrIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_corrIso = std::vector<float>(*IN::mu_corrIso);
}; 

 void Copymu_corrIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_corrIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_corrIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_corrIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_corrIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_corrIso->push_back( IN::mu_corrIso->at(index) ); 
 }; 

 void ClearOutputmu_corrIso( std::string  prefix ) { 

    std::string my_name = "mu_corrIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_corrIso, prefix = " << prefix << std::endl; 
     OUT::mu_corrIso->clear(); 
 }; 

 void Copymu_triggerMatchInToOut( std::string prefix ) { 

    std::string my_name = "mu_triggerMatch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_triggerMatch = std::vector<bool>(*IN::mu_triggerMatch);
}; 

 void Copymu_triggerMatchInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_triggerMatch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_triggerMatch->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_triggerMatch" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_triggerMatch" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_triggerMatch->push_back( IN::mu_triggerMatch->at(index) ); 
 }; 

 void ClearOutputmu_triggerMatch( std::string  prefix ) { 

    std::string my_name = "mu_triggerMatch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_triggerMatch, prefix = " << prefix << std::endl; 
     OUT::mu_triggerMatch->clear(); 
 }; 

 void Copymu_truthMatchInToOut( std::string prefix ) { 

    std::string my_name = "mu_truthMatch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_truthMatch = std::vector<bool>(*IN::mu_truthMatch);
}; 

 void Copymu_truthMatchInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_truthMatch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_truthMatch->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_truthMatch" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_truthMatch" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_truthMatch->push_back( IN::mu_truthMatch->at(index) ); 
 }; 

 void ClearOutputmu_truthMatch( std::string  prefix ) { 

    std::string my_name = "mu_truthMatch";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_truthMatch, prefix = " << prefix << std::endl; 
     OUT::mu_truthMatch->clear(); 
 }; 

 void Copymu_truthMinDRInToOut( std::string prefix ) { 

    std::string my_name = "mu_truthMinDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::mu_truthMinDR = std::vector<float>(*IN::mu_truthMinDR);
}; 

 void Copymu_truthMinDRInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "mu_truthMinDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::mu_truthMinDR->size() ) {
         std::cout << "Vector size exceeded for branch IN::mu_truthMinDR" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible mu_truthMinDR" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::mu_truthMinDR->push_back( IN::mu_truthMinDR->at(index) ); 
 }; 

 void ClearOutputmu_truthMinDR( std::string  prefix ) { 

    std::string my_name = "mu_truthMinDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible mu_truthMinDR, prefix = " << prefix << std::endl; 
     OUT::mu_truthMinDR->clear(); 
 }; 

 void Copyph_ptInToOut( std::string prefix ) { 

    std::string my_name = "ph_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_pt = std::vector<float>(*IN::ph_pt);
}; 

 void Copyph_ptInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_pt->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_pt" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_pt" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_pt->push_back( IN::ph_pt->at(index) ); 
 }; 

 void ClearOutputph_pt( std::string  prefix ) { 

    std::string my_name = "ph_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_pt, prefix = " << prefix << std::endl; 
     OUT::ph_pt->clear(); 
 }; 

 void Copyph_etaInToOut( std::string prefix ) { 

    std::string my_name = "ph_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_eta = std::vector<float>(*IN::ph_eta);
}; 

 void Copyph_etaInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_eta->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_eta" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_eta" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_eta->push_back( IN::ph_eta->at(index) ); 
 }; 

 void ClearOutputph_eta( std::string  prefix ) { 

    std::string my_name = "ph_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_eta, prefix = " << prefix << std::endl; 
     OUT::ph_eta->clear(); 
 }; 

 void Copyph_scetaInToOut( std::string prefix ) { 

    std::string my_name = "ph_sceta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_sceta = std::vector<float>(*IN::ph_sceta);
}; 

 void Copyph_scetaInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_sceta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_sceta->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_sceta" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_sceta" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_sceta->push_back( IN::ph_sceta->at(index) ); 
 }; 

 void ClearOutputph_sceta( std::string  prefix ) { 

    std::string my_name = "ph_sceta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_sceta, prefix = " << prefix << std::endl; 
     OUT::ph_sceta->clear(); 
 }; 

 void Copyph_phiInToOut( std::string prefix ) { 

    std::string my_name = "ph_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_phi = std::vector<float>(*IN::ph_phi);
}; 

 void Copyph_phiInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_phi->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_phi" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_phi" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_phi->push_back( IN::ph_phi->at(index) ); 
 }; 

 void ClearOutputph_phi( std::string  prefix ) { 

    std::string my_name = "ph_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_phi, prefix = " << prefix << std::endl; 
     OUT::ph_phi->clear(); 
 }; 

 void Copyph_eInToOut( std::string prefix ) { 

    std::string my_name = "ph_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_e = std::vector<float>(*IN::ph_e);
}; 

 void Copyph_eInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_e->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_e" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_e" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_e->push_back( IN::ph_e->at(index) ); 
 }; 

 void ClearOutputph_e( std::string  prefix ) { 

    std::string my_name = "ph_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_e, prefix = " << prefix << std::endl; 
     OUT::ph_e->clear(); 
 }; 

 void Copyph_HoverEInToOut( std::string prefix ) { 

    std::string my_name = "ph_HoverE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_HoverE = std::vector<float>(*IN::ph_HoverE);
}; 

 void Copyph_HoverEInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_HoverE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_HoverE->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_HoverE" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_HoverE" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_HoverE->push_back( IN::ph_HoverE->at(index) ); 
 }; 

 void ClearOutputph_HoverE( std::string  prefix ) { 

    std::string my_name = "ph_HoverE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_HoverE, prefix = " << prefix << std::endl; 
     OUT::ph_HoverE->clear(); 
 }; 

 void Copyph_HoverE12InToOut( std::string prefix ) { 

    std::string my_name = "ph_HoverE12";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_HoverE12 = std::vector<float>(*IN::ph_HoverE12);
}; 

 void Copyph_HoverE12InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_HoverE12";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_HoverE12->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_HoverE12" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_HoverE12" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_HoverE12->push_back( IN::ph_HoverE12->at(index) ); 
 }; 

 void ClearOutputph_HoverE12( std::string  prefix ) { 

    std::string my_name = "ph_HoverE12";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_HoverE12, prefix = " << prefix << std::endl; 
     OUT::ph_HoverE12->clear(); 
 }; 

 void Copyph_sigmaIEIEInToOut( std::string prefix ) { 

    std::string my_name = "ph_sigmaIEIE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_sigmaIEIE = std::vector<float>(*IN::ph_sigmaIEIE);
}; 

 void Copyph_sigmaIEIEInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_sigmaIEIE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_sigmaIEIE->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_sigmaIEIE" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_sigmaIEIE" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_sigmaIEIE->push_back( IN::ph_sigmaIEIE->at(index) ); 
 }; 

 void ClearOutputph_sigmaIEIE( std::string  prefix ) { 

    std::string my_name = "ph_sigmaIEIE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_sigmaIEIE, prefix = " << prefix << std::endl; 
     OUT::ph_sigmaIEIE->clear(); 
 }; 

 void Copyph_sigmaIEIPInToOut( std::string prefix ) { 

    std::string my_name = "ph_sigmaIEIP";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_sigmaIEIP = std::vector<float>(*IN::ph_sigmaIEIP);
}; 

 void Copyph_sigmaIEIPInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_sigmaIEIP";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_sigmaIEIP->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_sigmaIEIP" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_sigmaIEIP" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_sigmaIEIP->push_back( IN::ph_sigmaIEIP->at(index) ); 
 }; 

 void ClearOutputph_sigmaIEIP( std::string  prefix ) { 

    std::string my_name = "ph_sigmaIEIP";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_sigmaIEIP, prefix = " << prefix << std::endl; 
     OUT::ph_sigmaIEIP->clear(); 
 }; 

 void Copyph_r9InToOut( std::string prefix ) { 

    std::string my_name = "ph_r9";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_r9 = std::vector<float>(*IN::ph_r9);
}; 

 void Copyph_r9InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_r9";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_r9->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_r9" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_r9" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_r9->push_back( IN::ph_r9->at(index) ); 
 }; 

 void ClearOutputph_r9( std::string  prefix ) { 

    std::string my_name = "ph_r9";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_r9, prefix = " << prefix << std::endl; 
     OUT::ph_r9->clear(); 
 }; 

 void Copyph_E1x3InToOut( std::string prefix ) { 

    std::string my_name = "ph_E1x3";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_E1x3 = std::vector<float>(*IN::ph_E1x3);
}; 

 void Copyph_E1x3InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_E1x3";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_E1x3->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_E1x3" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_E1x3" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_E1x3->push_back( IN::ph_E1x3->at(index) ); 
 }; 

 void ClearOutputph_E1x3( std::string  prefix ) { 

    std::string my_name = "ph_E1x3";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_E1x3, prefix = " << prefix << std::endl; 
     OUT::ph_E1x3->clear(); 
 }; 

 void Copyph_E2x2InToOut( std::string prefix ) { 

    std::string my_name = "ph_E2x2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_E2x2 = std::vector<float>(*IN::ph_E2x2);
}; 

 void Copyph_E2x2InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_E2x2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_E2x2->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_E2x2" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_E2x2" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_E2x2->push_back( IN::ph_E2x2->at(index) ); 
 }; 

 void ClearOutputph_E2x2( std::string  prefix ) { 

    std::string my_name = "ph_E2x2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_E2x2, prefix = " << prefix << std::endl; 
     OUT::ph_E2x2->clear(); 
 }; 

 void Copyph_E5x5InToOut( std::string prefix ) { 

    std::string my_name = "ph_E5x5";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_E5x5 = std::vector<float>(*IN::ph_E5x5);
}; 

 void Copyph_E5x5InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_E5x5";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_E5x5->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_E5x5" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_E5x5" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_E5x5->push_back( IN::ph_E5x5->at(index) ); 
 }; 

 void ClearOutputph_E5x5( std::string  prefix ) { 

    std::string my_name = "ph_E5x5";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_E5x5, prefix = " << prefix << std::endl; 
     OUT::ph_E5x5->clear(); 
 }; 

 void Copyph_E2x5MaxInToOut( std::string prefix ) { 

    std::string my_name = "ph_E2x5Max";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_E2x5Max = std::vector<float>(*IN::ph_E2x5Max);
}; 

 void Copyph_E2x5MaxInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_E2x5Max";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_E2x5Max->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_E2x5Max" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_E2x5Max" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_E2x5Max->push_back( IN::ph_E2x5Max->at(index) ); 
 }; 

 void ClearOutputph_E2x5Max( std::string  prefix ) { 

    std::string my_name = "ph_E2x5Max";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_E2x5Max, prefix = " << prefix << std::endl; 
     OUT::ph_E2x5Max->clear(); 
 }; 

 void Copyph_SCetaWidthInToOut( std::string prefix ) { 

    std::string my_name = "ph_SCetaWidth";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_SCetaWidth = std::vector<float>(*IN::ph_SCetaWidth);
}; 

 void Copyph_SCetaWidthInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_SCetaWidth";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_SCetaWidth->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_SCetaWidth" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_SCetaWidth" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_SCetaWidth->push_back( IN::ph_SCetaWidth->at(index) ); 
 }; 

 void ClearOutputph_SCetaWidth( std::string  prefix ) { 

    std::string my_name = "ph_SCetaWidth";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_SCetaWidth, prefix = " << prefix << std::endl; 
     OUT::ph_SCetaWidth->clear(); 
 }; 

 void Copyph_SCphiWidthInToOut( std::string prefix ) { 

    std::string my_name = "ph_SCphiWidth";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_SCphiWidth = std::vector<float>(*IN::ph_SCphiWidth);
}; 

 void Copyph_SCphiWidthInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_SCphiWidth";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_SCphiWidth->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_SCphiWidth" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_SCphiWidth" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_SCphiWidth->push_back( IN::ph_SCphiWidth->at(index) ); 
 }; 

 void ClearOutputph_SCphiWidth( std::string  prefix ) { 

    std::string my_name = "ph_SCphiWidth";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_SCphiWidth, prefix = " << prefix << std::endl; 
     OUT::ph_SCphiWidth->clear(); 
 }; 

 void Copyph_ESEffSigmaRRInToOut( std::string prefix ) { 

    std::string my_name = "ph_ESEffSigmaRR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_ESEffSigmaRR = std::vector<float>(*IN::ph_ESEffSigmaRR);
}; 

 void Copyph_ESEffSigmaRRInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_ESEffSigmaRR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_ESEffSigmaRR->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_ESEffSigmaRR" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_ESEffSigmaRR" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_ESEffSigmaRR->push_back( IN::ph_ESEffSigmaRR->at(index) ); 
 }; 

 void ClearOutputph_ESEffSigmaRR( std::string  prefix ) { 

    std::string my_name = "ph_ESEffSigmaRR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_ESEffSigmaRR, prefix = " << prefix << std::endl; 
     OUT::ph_ESEffSigmaRR->clear(); 
 }; 

 void Copyph_hcalIsoDR03InToOut( std::string prefix ) { 

    std::string my_name = "ph_hcalIsoDR03";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_hcalIsoDR03 = std::vector<float>(*IN::ph_hcalIsoDR03);
}; 

 void Copyph_hcalIsoDR03InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_hcalIsoDR03";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_hcalIsoDR03->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_hcalIsoDR03" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_hcalIsoDR03" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_hcalIsoDR03->push_back( IN::ph_hcalIsoDR03->at(index) ); 
 }; 

 void ClearOutputph_hcalIsoDR03( std::string  prefix ) { 

    std::string my_name = "ph_hcalIsoDR03";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_hcalIsoDR03, prefix = " << prefix << std::endl; 
     OUT::ph_hcalIsoDR03->clear(); 
 }; 

 void Copyph_trkIsoHollowDR03InToOut( std::string prefix ) { 

    std::string my_name = "ph_trkIsoHollowDR03";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_trkIsoHollowDR03 = std::vector<float>(*IN::ph_trkIsoHollowDR03);
}; 

 void Copyph_trkIsoHollowDR03InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_trkIsoHollowDR03";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_trkIsoHollowDR03->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_trkIsoHollowDR03" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_trkIsoHollowDR03" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_trkIsoHollowDR03->push_back( IN::ph_trkIsoHollowDR03->at(index) ); 
 }; 

 void ClearOutputph_trkIsoHollowDR03( std::string  prefix ) { 

    std::string my_name = "ph_trkIsoHollowDR03";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_trkIsoHollowDR03, prefix = " << prefix << std::endl; 
     OUT::ph_trkIsoHollowDR03->clear(); 
 }; 

 void Copyph_chgpfIsoDR02InToOut( std::string prefix ) { 

    std::string my_name = "ph_chgpfIsoDR02";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_chgpfIsoDR02 = std::vector<float>(*IN::ph_chgpfIsoDR02);
}; 

 void Copyph_chgpfIsoDR02InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_chgpfIsoDR02";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_chgpfIsoDR02->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_chgpfIsoDR02" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_chgpfIsoDR02" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_chgpfIsoDR02->push_back( IN::ph_chgpfIsoDR02->at(index) ); 
 }; 

 void ClearOutputph_chgpfIsoDR02( std::string  prefix ) { 

    std::string my_name = "ph_chgpfIsoDR02";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_chgpfIsoDR02, prefix = " << prefix << std::endl; 
     OUT::ph_chgpfIsoDR02->clear(); 
 }; 

 void Copyph_pfChIsoWorstInToOut( std::string prefix ) { 

    std::string my_name = "ph_pfChIsoWorst";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_pfChIsoWorst = std::vector<float>(*IN::ph_pfChIsoWorst);
}; 

 void Copyph_pfChIsoWorstInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_pfChIsoWorst";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_pfChIsoWorst->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_pfChIsoWorst" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_pfChIsoWorst" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_pfChIsoWorst->push_back( IN::ph_pfChIsoWorst->at(index) ); 
 }; 

 void ClearOutputph_pfChIsoWorst( std::string  prefix ) { 

    std::string my_name = "ph_pfChIsoWorst";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_pfChIsoWorst, prefix = " << prefix << std::endl; 
     OUT::ph_pfChIsoWorst->clear(); 
 }; 

 void Copyph_chIsoInToOut( std::string prefix ) { 

    std::string my_name = "ph_chIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_chIso = std::vector<float>(*IN::ph_chIso);
}; 

 void Copyph_chIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_chIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_chIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_chIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_chIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_chIso->push_back( IN::ph_chIso->at(index) ); 
 }; 

 void ClearOutputph_chIso( std::string  prefix ) { 

    std::string my_name = "ph_chIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_chIso, prefix = " << prefix << std::endl; 
     OUT::ph_chIso->clear(); 
 }; 

 void Copyph_neuIsoInToOut( std::string prefix ) { 

    std::string my_name = "ph_neuIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_neuIso = std::vector<float>(*IN::ph_neuIso);
}; 

 void Copyph_neuIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_neuIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_neuIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_neuIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_neuIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_neuIso->push_back( IN::ph_neuIso->at(index) ); 
 }; 

 void ClearOutputph_neuIso( std::string  prefix ) { 

    std::string my_name = "ph_neuIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_neuIso, prefix = " << prefix << std::endl; 
     OUT::ph_neuIso->clear(); 
 }; 

 void Copyph_phoIsoInToOut( std::string prefix ) { 

    std::string my_name = "ph_phoIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_phoIso = std::vector<float>(*IN::ph_phoIso);
}; 

 void Copyph_phoIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_phoIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_phoIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_phoIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_phoIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_phoIso->push_back( IN::ph_phoIso->at(index) ); 
 }; 

 void ClearOutputph_phoIso( std::string  prefix ) { 

    std::string my_name = "ph_phoIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_phoIso, prefix = " << prefix << std::endl; 
     OUT::ph_phoIso->clear(); 
 }; 

 void Copyph_chIsoCorrInToOut( std::string prefix ) { 

    std::string my_name = "ph_chIsoCorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_chIsoCorr = std::vector<float>(*IN::ph_chIsoCorr);
}; 

 void Copyph_chIsoCorrInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_chIsoCorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_chIsoCorr->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_chIsoCorr" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_chIsoCorr" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_chIsoCorr->push_back( IN::ph_chIsoCorr->at(index) ); 
 }; 

 void ClearOutputph_chIsoCorr( std::string  prefix ) { 

    std::string my_name = "ph_chIsoCorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_chIsoCorr, prefix = " << prefix << std::endl; 
     OUT::ph_chIsoCorr->clear(); 
 }; 

 void Copyph_neuIsoCorrInToOut( std::string prefix ) { 

    std::string my_name = "ph_neuIsoCorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_neuIsoCorr = std::vector<float>(*IN::ph_neuIsoCorr);
}; 

 void Copyph_neuIsoCorrInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_neuIsoCorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_neuIsoCorr->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_neuIsoCorr" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_neuIsoCorr" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_neuIsoCorr->push_back( IN::ph_neuIsoCorr->at(index) ); 
 }; 

 void ClearOutputph_neuIsoCorr( std::string  prefix ) { 

    std::string my_name = "ph_neuIsoCorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_neuIsoCorr, prefix = " << prefix << std::endl; 
     OUT::ph_neuIsoCorr->clear(); 
 }; 

 void Copyph_phoIsoCorrInToOut( std::string prefix ) { 

    std::string my_name = "ph_phoIsoCorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_phoIsoCorr = std::vector<float>(*IN::ph_phoIsoCorr);
}; 

 void Copyph_phoIsoCorrInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_phoIsoCorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_phoIsoCorr->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_phoIsoCorr" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_phoIsoCorr" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_phoIsoCorr->push_back( IN::ph_phoIsoCorr->at(index) ); 
 }; 

 void ClearOutputph_phoIsoCorr( std::string  prefix ) { 

    std::string my_name = "ph_phoIsoCorr";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_phoIsoCorr, prefix = " << prefix << std::endl; 
     OUT::ph_phoIsoCorr->clear(); 
 }; 

 void Copyph_SCRChIsoInToOut( std::string prefix ) { 

    std::string my_name = "ph_SCRChIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_SCRChIso = std::vector<float>(*IN::ph_SCRChIso);
}; 

 void Copyph_SCRChIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_SCRChIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_SCRChIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_SCRChIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_SCRChIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_SCRChIso->push_back( IN::ph_SCRChIso->at(index) ); 
 }; 

 void ClearOutputph_SCRChIso( std::string  prefix ) { 

    std::string my_name = "ph_SCRChIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_SCRChIso, prefix = " << prefix << std::endl; 
     OUT::ph_SCRChIso->clear(); 
 }; 

 void Copyph_SCRPhoIsoInToOut( std::string prefix ) { 

    std::string my_name = "ph_SCRPhoIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_SCRPhoIso = std::vector<float>(*IN::ph_SCRPhoIso);
}; 

 void Copyph_SCRPhoIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_SCRPhoIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_SCRPhoIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_SCRPhoIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_SCRPhoIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_SCRPhoIso->push_back( IN::ph_SCRPhoIso->at(index) ); 
 }; 

 void ClearOutputph_SCRPhoIso( std::string  prefix ) { 

    std::string my_name = "ph_SCRPhoIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_SCRPhoIso, prefix = " << prefix << std::endl; 
     OUT::ph_SCRPhoIso->clear(); 
 }; 

 void Copyph_SCRNeuIsoInToOut( std::string prefix ) { 

    std::string my_name = "ph_SCRNeuIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_SCRNeuIso = std::vector<float>(*IN::ph_SCRNeuIso);
}; 

 void Copyph_SCRNeuIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_SCRNeuIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_SCRNeuIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_SCRNeuIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_SCRNeuIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_SCRNeuIso->push_back( IN::ph_SCRNeuIso->at(index) ); 
 }; 

 void ClearOutputph_SCRNeuIso( std::string  prefix ) { 

    std::string my_name = "ph_SCRNeuIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_SCRNeuIso, prefix = " << prefix << std::endl; 
     OUT::ph_SCRNeuIso->clear(); 
 }; 

 void Copyph_SCRChIso04InToOut( std::string prefix ) { 

    std::string my_name = "ph_SCRChIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_SCRChIso04 = std::vector<float>(*IN::ph_SCRChIso04);
}; 

 void Copyph_SCRChIso04InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_SCRChIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_SCRChIso04->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_SCRChIso04" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_SCRChIso04" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_SCRChIso04->push_back( IN::ph_SCRChIso04->at(index) ); 
 }; 

 void ClearOutputph_SCRChIso04( std::string  prefix ) { 

    std::string my_name = "ph_SCRChIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_SCRChIso04, prefix = " << prefix << std::endl; 
     OUT::ph_SCRChIso04->clear(); 
 }; 

 void Copyph_SCRPhoIso04InToOut( std::string prefix ) { 

    std::string my_name = "ph_SCRPhoIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_SCRPhoIso04 = std::vector<float>(*IN::ph_SCRPhoIso04);
}; 

 void Copyph_SCRPhoIso04InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_SCRPhoIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_SCRPhoIso04->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_SCRPhoIso04" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_SCRPhoIso04" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_SCRPhoIso04->push_back( IN::ph_SCRPhoIso04->at(index) ); 
 }; 

 void ClearOutputph_SCRPhoIso04( std::string  prefix ) { 

    std::string my_name = "ph_SCRPhoIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_SCRPhoIso04, prefix = " << prefix << std::endl; 
     OUT::ph_SCRPhoIso04->clear(); 
 }; 

 void Copyph_SCRNeuIso04InToOut( std::string prefix ) { 

    std::string my_name = "ph_SCRNeuIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_SCRNeuIso04 = std::vector<float>(*IN::ph_SCRNeuIso04);
}; 

 void Copyph_SCRNeuIso04InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_SCRNeuIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_SCRNeuIso04->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_SCRNeuIso04" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_SCRNeuIso04" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_SCRNeuIso04->push_back( IN::ph_SCRNeuIso04->at(index) ); 
 }; 

 void ClearOutputph_SCRNeuIso04( std::string  prefix ) { 

    std::string my_name = "ph_SCRNeuIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_SCRNeuIso04, prefix = " << prefix << std::endl; 
     OUT::ph_SCRNeuIso04->clear(); 
 }; 

 void Copyph_RandConeChIsoInToOut( std::string prefix ) { 

    std::string my_name = "ph_RandConeChIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_RandConeChIso = std::vector<float>(*IN::ph_RandConeChIso);
}; 

 void Copyph_RandConeChIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_RandConeChIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_RandConeChIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_RandConeChIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_RandConeChIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_RandConeChIso->push_back( IN::ph_RandConeChIso->at(index) ); 
 }; 

 void ClearOutputph_RandConeChIso( std::string  prefix ) { 

    std::string my_name = "ph_RandConeChIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_RandConeChIso, prefix = " << prefix << std::endl; 
     OUT::ph_RandConeChIso->clear(); 
 }; 

 void Copyph_RandConePhoIsoInToOut( std::string prefix ) { 

    std::string my_name = "ph_RandConePhoIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_RandConePhoIso = std::vector<float>(*IN::ph_RandConePhoIso);
}; 

 void Copyph_RandConePhoIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_RandConePhoIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_RandConePhoIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_RandConePhoIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_RandConePhoIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_RandConePhoIso->push_back( IN::ph_RandConePhoIso->at(index) ); 
 }; 

 void ClearOutputph_RandConePhoIso( std::string  prefix ) { 

    std::string my_name = "ph_RandConePhoIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_RandConePhoIso, prefix = " << prefix << std::endl; 
     OUT::ph_RandConePhoIso->clear(); 
 }; 

 void Copyph_RandConeNeuIsoInToOut( std::string prefix ) { 

    std::string my_name = "ph_RandConeNeuIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_RandConeNeuIso = std::vector<float>(*IN::ph_RandConeNeuIso);
}; 

 void Copyph_RandConeNeuIsoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_RandConeNeuIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_RandConeNeuIso->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_RandConeNeuIso" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_RandConeNeuIso" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_RandConeNeuIso->push_back( IN::ph_RandConeNeuIso->at(index) ); 
 }; 

 void ClearOutputph_RandConeNeuIso( std::string  prefix ) { 

    std::string my_name = "ph_RandConeNeuIso";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_RandConeNeuIso, prefix = " << prefix << std::endl; 
     OUT::ph_RandConeNeuIso->clear(); 
 }; 

 void Copyph_RandConeChIso04InToOut( std::string prefix ) { 

    std::string my_name = "ph_RandConeChIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_RandConeChIso04 = std::vector<float>(*IN::ph_RandConeChIso04);
}; 

 void Copyph_RandConeChIso04InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_RandConeChIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_RandConeChIso04->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_RandConeChIso04" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_RandConeChIso04" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_RandConeChIso04->push_back( IN::ph_RandConeChIso04->at(index) ); 
 }; 

 void ClearOutputph_RandConeChIso04( std::string  prefix ) { 

    std::string my_name = "ph_RandConeChIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_RandConeChIso04, prefix = " << prefix << std::endl; 
     OUT::ph_RandConeChIso04->clear(); 
 }; 

 void Copyph_RandConePhoIso04InToOut( std::string prefix ) { 

    std::string my_name = "ph_RandConePhoIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_RandConePhoIso04 = std::vector<float>(*IN::ph_RandConePhoIso04);
}; 

 void Copyph_RandConePhoIso04InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_RandConePhoIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_RandConePhoIso04->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_RandConePhoIso04" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_RandConePhoIso04" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_RandConePhoIso04->push_back( IN::ph_RandConePhoIso04->at(index) ); 
 }; 

 void ClearOutputph_RandConePhoIso04( std::string  prefix ) { 

    std::string my_name = "ph_RandConePhoIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_RandConePhoIso04, prefix = " << prefix << std::endl; 
     OUT::ph_RandConePhoIso04->clear(); 
 }; 

 void Copyph_RandConeNeuIso04InToOut( std::string prefix ) { 

    std::string my_name = "ph_RandConeNeuIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_RandConeNeuIso04 = std::vector<float>(*IN::ph_RandConeNeuIso04);
}; 

 void Copyph_RandConeNeuIso04InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_RandConeNeuIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_RandConeNeuIso04->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_RandConeNeuIso04" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_RandConeNeuIso04" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_RandConeNeuIso04->push_back( IN::ph_RandConeNeuIso04->at(index) ); 
 }; 

 void ClearOutputph_RandConeNeuIso04( std::string  prefix ) { 

    std::string my_name = "ph_RandConeNeuIso04";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_RandConeNeuIso04, prefix = " << prefix << std::endl; 
     OUT::ph_RandConeNeuIso04->clear(); 
 }; 

 void Copyph_eleVetoInToOut( std::string prefix ) { 

    std::string my_name = "ph_eleVeto";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_eleVeto = std::vector<bool>(*IN::ph_eleVeto);
}; 

 void Copyph_eleVetoInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_eleVeto";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_eleVeto->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_eleVeto" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_eleVeto" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_eleVeto->push_back( IN::ph_eleVeto->at(index) ); 
 }; 

 void ClearOutputph_eleVeto( std::string  prefix ) { 

    std::string my_name = "ph_eleVeto";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_eleVeto, prefix = " << prefix << std::endl; 
     OUT::ph_eleVeto->clear(); 
 }; 

 void Copyph_hasPixSeedInToOut( std::string prefix ) { 

    std::string my_name = "ph_hasPixSeed";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_hasPixSeed = std::vector<bool>(*IN::ph_hasPixSeed);
}; 

 void Copyph_hasPixSeedInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_hasPixSeed";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_hasPixSeed->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_hasPixSeed" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_hasPixSeed" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_hasPixSeed->push_back( IN::ph_hasPixSeed->at(index) ); 
 }; 

 void ClearOutputph_hasPixSeed( std::string  prefix ) { 

    std::string my_name = "ph_hasPixSeed";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_hasPixSeed, prefix = " << prefix << std::endl; 
     OUT::ph_hasPixSeed->clear(); 
 }; 

 void Copyph_drToTrkInToOut( std::string prefix ) { 

    std::string my_name = "ph_drToTrk";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_drToTrk = std::vector<float>(*IN::ph_drToTrk);
}; 

 void Copyph_drToTrkInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_drToTrk";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_drToTrk->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_drToTrk" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_drToTrk" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_drToTrk->push_back( IN::ph_drToTrk->at(index) ); 
 }; 

 void ClearOutputph_drToTrk( std::string  prefix ) { 

    std::string my_name = "ph_drToTrk";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_drToTrk, prefix = " << prefix << std::endl; 
     OUT::ph_drToTrk->clear(); 
 }; 

 void Copyph_isConvInToOut( std::string prefix ) { 

    std::string my_name = "ph_isConv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_isConv = std::vector<bool>(*IN::ph_isConv);
}; 

 void Copyph_isConvInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_isConv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_isConv->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_isConv" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_isConv" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_isConv->push_back( IN::ph_isConv->at(index) ); 
 }; 

 void ClearOutputph_isConv( std::string  prefix ) { 

    std::string my_name = "ph_isConv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_isConv, prefix = " << prefix << std::endl; 
     OUT::ph_isConv->clear(); 
 }; 

 void Copyph_conv_nTrkInToOut( std::string prefix ) { 

    std::string my_name = "ph_conv_nTrk";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_conv_nTrk = std::vector<int>(*IN::ph_conv_nTrk);
}; 

 void Copyph_conv_nTrkInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_conv_nTrk";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_conv_nTrk->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_conv_nTrk" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_conv_nTrk" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_conv_nTrk->push_back( IN::ph_conv_nTrk->at(index) ); 
 }; 

 void ClearOutputph_conv_nTrk( std::string  prefix ) { 

    std::string my_name = "ph_conv_nTrk";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_conv_nTrk, prefix = " << prefix << std::endl; 
     OUT::ph_conv_nTrk->clear(); 
 }; 

 void Copyph_conv_vtx_xInToOut( std::string prefix ) { 

    std::string my_name = "ph_conv_vtx_x";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_conv_vtx_x = std::vector<float>(*IN::ph_conv_vtx_x);
}; 

 void Copyph_conv_vtx_xInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_conv_vtx_x";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_conv_vtx_x->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_conv_vtx_x" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_conv_vtx_x" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_conv_vtx_x->push_back( IN::ph_conv_vtx_x->at(index) ); 
 }; 

 void ClearOutputph_conv_vtx_x( std::string  prefix ) { 

    std::string my_name = "ph_conv_vtx_x";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_conv_vtx_x, prefix = " << prefix << std::endl; 
     OUT::ph_conv_vtx_x->clear(); 
 }; 

 void Copyph_conv_vtx_yInToOut( std::string prefix ) { 

    std::string my_name = "ph_conv_vtx_y";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_conv_vtx_y = std::vector<float>(*IN::ph_conv_vtx_y);
}; 

 void Copyph_conv_vtx_yInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_conv_vtx_y";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_conv_vtx_y->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_conv_vtx_y" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_conv_vtx_y" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_conv_vtx_y->push_back( IN::ph_conv_vtx_y->at(index) ); 
 }; 

 void ClearOutputph_conv_vtx_y( std::string  prefix ) { 

    std::string my_name = "ph_conv_vtx_y";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_conv_vtx_y, prefix = " << prefix << std::endl; 
     OUT::ph_conv_vtx_y->clear(); 
 }; 

 void Copyph_conv_vtx_zInToOut( std::string prefix ) { 

    std::string my_name = "ph_conv_vtx_z";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_conv_vtx_z = std::vector<float>(*IN::ph_conv_vtx_z);
}; 

 void Copyph_conv_vtx_zInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_conv_vtx_z";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_conv_vtx_z->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_conv_vtx_z" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_conv_vtx_z" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_conv_vtx_z->push_back( IN::ph_conv_vtx_z->at(index) ); 
 }; 

 void ClearOutputph_conv_vtx_z( std::string  prefix ) { 

    std::string my_name = "ph_conv_vtx_z";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_conv_vtx_z, prefix = " << prefix << std::endl; 
     OUT::ph_conv_vtx_z->clear(); 
 }; 

 void Copyph_conv_ptin1InToOut( std::string prefix ) { 

    std::string my_name = "ph_conv_ptin1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_conv_ptin1 = std::vector<float>(*IN::ph_conv_ptin1);
}; 

 void Copyph_conv_ptin1InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_conv_ptin1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_conv_ptin1->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_conv_ptin1" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_conv_ptin1" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_conv_ptin1->push_back( IN::ph_conv_ptin1->at(index) ); 
 }; 

 void ClearOutputph_conv_ptin1( std::string  prefix ) { 

    std::string my_name = "ph_conv_ptin1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_conv_ptin1, prefix = " << prefix << std::endl; 
     OUT::ph_conv_ptin1->clear(); 
 }; 

 void Copyph_conv_ptin2InToOut( std::string prefix ) { 

    std::string my_name = "ph_conv_ptin2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_conv_ptin2 = std::vector<float>(*IN::ph_conv_ptin2);
}; 

 void Copyph_conv_ptin2InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_conv_ptin2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_conv_ptin2->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_conv_ptin2" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_conv_ptin2" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_conv_ptin2->push_back( IN::ph_conv_ptin2->at(index) ); 
 }; 

 void ClearOutputph_conv_ptin2( std::string  prefix ) { 

    std::string my_name = "ph_conv_ptin2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_conv_ptin2, prefix = " << prefix << std::endl; 
     OUT::ph_conv_ptin2->clear(); 
 }; 

 void Copyph_conv_ptout1InToOut( std::string prefix ) { 

    std::string my_name = "ph_conv_ptout1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_conv_ptout1 = std::vector<float>(*IN::ph_conv_ptout1);
}; 

 void Copyph_conv_ptout1InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_conv_ptout1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_conv_ptout1->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_conv_ptout1" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_conv_ptout1" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_conv_ptout1->push_back( IN::ph_conv_ptout1->at(index) ); 
 }; 

 void ClearOutputph_conv_ptout1( std::string  prefix ) { 

    std::string my_name = "ph_conv_ptout1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_conv_ptout1, prefix = " << prefix << std::endl; 
     OUT::ph_conv_ptout1->clear(); 
 }; 

 void Copyph_conv_ptout2InToOut( std::string prefix ) { 

    std::string my_name = "ph_conv_ptout2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_conv_ptout2 = std::vector<float>(*IN::ph_conv_ptout2);
}; 

 void Copyph_conv_ptout2InToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_conv_ptout2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_conv_ptout2->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_conv_ptout2" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_conv_ptout2" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_conv_ptout2->push_back( IN::ph_conv_ptout2->at(index) ); 
 }; 

 void ClearOutputph_conv_ptout2( std::string  prefix ) { 

    std::string my_name = "ph_conv_ptout2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_conv_ptout2, prefix = " << prefix << std::endl; 
     OUT::ph_conv_ptout2->clear(); 
 }; 

 void Copyph_passTightInToOut( std::string prefix ) { 

    std::string my_name = "ph_passTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passTight = std::vector<bool>(*IN::ph_passTight);
}; 

 void Copyph_passTightInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passTight->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passTight" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passTight" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passTight->push_back( IN::ph_passTight->at(index) ); 
 }; 

 void ClearOutputph_passTight( std::string  prefix ) { 

    std::string my_name = "ph_passTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passTight, prefix = " << prefix << std::endl; 
     OUT::ph_passTight->clear(); 
 }; 

 void Copyph_passMediumInToOut( std::string prefix ) { 

    std::string my_name = "ph_passMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passMedium = std::vector<bool>(*IN::ph_passMedium);
}; 

 void Copyph_passMediumInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passMedium->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passMedium" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passMedium" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passMedium->push_back( IN::ph_passMedium->at(index) ); 
 }; 

 void ClearOutputph_passMedium( std::string  prefix ) { 

    std::string my_name = "ph_passMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passMedium, prefix = " << prefix << std::endl; 
     OUT::ph_passMedium->clear(); 
 }; 

 void Copyph_passLooseInToOut( std::string prefix ) { 

    std::string my_name = "ph_passLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passLoose = std::vector<bool>(*IN::ph_passLoose);
}; 

 void Copyph_passLooseInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passLoose->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passLoose" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passLoose" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passLoose->push_back( IN::ph_passLoose->at(index) ); 
 }; 

 void ClearOutputph_passLoose( std::string  prefix ) { 

    std::string my_name = "ph_passLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passLoose, prefix = " << prefix << std::endl; 
     OUT::ph_passLoose->clear(); 
 }; 

 void Copyph_passLooseNoSIEIEInToOut( std::string prefix ) { 

    std::string my_name = "ph_passLooseNoSIEIE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passLooseNoSIEIE = std::vector<bool>(*IN::ph_passLooseNoSIEIE);
}; 

 void Copyph_passLooseNoSIEIEInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passLooseNoSIEIE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passLooseNoSIEIE->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passLooseNoSIEIE" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passLooseNoSIEIE" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passLooseNoSIEIE->push_back( IN::ph_passLooseNoSIEIE->at(index) ); 
 }; 

 void ClearOutputph_passLooseNoSIEIE( std::string  prefix ) { 

    std::string my_name = "ph_passLooseNoSIEIE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passLooseNoSIEIE, prefix = " << prefix << std::endl; 
     OUT::ph_passLooseNoSIEIE->clear(); 
 }; 

 void Copyph_passHOverELooseInToOut( std::string prefix ) { 

    std::string my_name = "ph_passHOverELoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passHOverELoose = std::vector<bool>(*IN::ph_passHOverELoose);
}; 

 void Copyph_passHOverELooseInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passHOverELoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passHOverELoose->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passHOverELoose" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passHOverELoose" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passHOverELoose->push_back( IN::ph_passHOverELoose->at(index) ); 
 }; 

 void ClearOutputph_passHOverELoose( std::string  prefix ) { 

    std::string my_name = "ph_passHOverELoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passHOverELoose, prefix = " << prefix << std::endl; 
     OUT::ph_passHOverELoose->clear(); 
 }; 

 void Copyph_passHOverEMediumInToOut( std::string prefix ) { 

    std::string my_name = "ph_passHOverEMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passHOverEMedium = std::vector<bool>(*IN::ph_passHOverEMedium);
}; 

 void Copyph_passHOverEMediumInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passHOverEMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passHOverEMedium->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passHOverEMedium" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passHOverEMedium" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passHOverEMedium->push_back( IN::ph_passHOverEMedium->at(index) ); 
 }; 

 void ClearOutputph_passHOverEMedium( std::string  prefix ) { 

    std::string my_name = "ph_passHOverEMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passHOverEMedium, prefix = " << prefix << std::endl; 
     OUT::ph_passHOverEMedium->clear(); 
 }; 

 void Copyph_passHOverETightInToOut( std::string prefix ) { 

    std::string my_name = "ph_passHOverETight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passHOverETight = std::vector<bool>(*IN::ph_passHOverETight);
}; 

 void Copyph_passHOverETightInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passHOverETight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passHOverETight->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passHOverETight" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passHOverETight" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passHOverETight->push_back( IN::ph_passHOverETight->at(index) ); 
 }; 

 void ClearOutputph_passHOverETight( std::string  prefix ) { 

    std::string my_name = "ph_passHOverETight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passHOverETight, prefix = " << prefix << std::endl; 
     OUT::ph_passHOverETight->clear(); 
 }; 

 void Copyph_passSIEIELooseInToOut( std::string prefix ) { 

    std::string my_name = "ph_passSIEIELoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passSIEIELoose = std::vector<bool>(*IN::ph_passSIEIELoose);
}; 

 void Copyph_passSIEIELooseInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passSIEIELoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passSIEIELoose->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passSIEIELoose" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passSIEIELoose" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passSIEIELoose->push_back( IN::ph_passSIEIELoose->at(index) ); 
 }; 

 void ClearOutputph_passSIEIELoose( std::string  prefix ) { 

    std::string my_name = "ph_passSIEIELoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passSIEIELoose, prefix = " << prefix << std::endl; 
     OUT::ph_passSIEIELoose->clear(); 
 }; 

 void Copyph_passSIEIEMediumInToOut( std::string prefix ) { 

    std::string my_name = "ph_passSIEIEMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passSIEIEMedium = std::vector<bool>(*IN::ph_passSIEIEMedium);
}; 

 void Copyph_passSIEIEMediumInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passSIEIEMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passSIEIEMedium->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passSIEIEMedium" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passSIEIEMedium" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passSIEIEMedium->push_back( IN::ph_passSIEIEMedium->at(index) ); 
 }; 

 void ClearOutputph_passSIEIEMedium( std::string  prefix ) { 

    std::string my_name = "ph_passSIEIEMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passSIEIEMedium, prefix = " << prefix << std::endl; 
     OUT::ph_passSIEIEMedium->clear(); 
 }; 

 void Copyph_passSIEIETightInToOut( std::string prefix ) { 

    std::string my_name = "ph_passSIEIETight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passSIEIETight = std::vector<bool>(*IN::ph_passSIEIETight);
}; 

 void Copyph_passSIEIETightInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passSIEIETight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passSIEIETight->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passSIEIETight" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passSIEIETight" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passSIEIETight->push_back( IN::ph_passSIEIETight->at(index) ); 
 }; 

 void ClearOutputph_passSIEIETight( std::string  prefix ) { 

    std::string my_name = "ph_passSIEIETight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passSIEIETight, prefix = " << prefix << std::endl; 
     OUT::ph_passSIEIETight->clear(); 
 }; 

 void Copyph_passChIsoCorrLooseInToOut( std::string prefix ) { 

    std::string my_name = "ph_passChIsoCorrLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passChIsoCorrLoose = std::vector<bool>(*IN::ph_passChIsoCorrLoose);
}; 

 void Copyph_passChIsoCorrLooseInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passChIsoCorrLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passChIsoCorrLoose->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passChIsoCorrLoose" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passChIsoCorrLoose" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passChIsoCorrLoose->push_back( IN::ph_passChIsoCorrLoose->at(index) ); 
 }; 

 void ClearOutputph_passChIsoCorrLoose( std::string  prefix ) { 

    std::string my_name = "ph_passChIsoCorrLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passChIsoCorrLoose, prefix = " << prefix << std::endl; 
     OUT::ph_passChIsoCorrLoose->clear(); 
 }; 

 void Copyph_passChIsoCorrMediumInToOut( std::string prefix ) { 

    std::string my_name = "ph_passChIsoCorrMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passChIsoCorrMedium = std::vector<bool>(*IN::ph_passChIsoCorrMedium);
}; 

 void Copyph_passChIsoCorrMediumInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passChIsoCorrMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passChIsoCorrMedium->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passChIsoCorrMedium" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passChIsoCorrMedium" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passChIsoCorrMedium->push_back( IN::ph_passChIsoCorrMedium->at(index) ); 
 }; 

 void ClearOutputph_passChIsoCorrMedium( std::string  prefix ) { 

    std::string my_name = "ph_passChIsoCorrMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passChIsoCorrMedium, prefix = " << prefix << std::endl; 
     OUT::ph_passChIsoCorrMedium->clear(); 
 }; 

 void Copyph_passChIsoCorrTightInToOut( std::string prefix ) { 

    std::string my_name = "ph_passChIsoCorrTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passChIsoCorrTight = std::vector<bool>(*IN::ph_passChIsoCorrTight);
}; 

 void Copyph_passChIsoCorrTightInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passChIsoCorrTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passChIsoCorrTight->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passChIsoCorrTight" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passChIsoCorrTight" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passChIsoCorrTight->push_back( IN::ph_passChIsoCorrTight->at(index) ); 
 }; 

 void ClearOutputph_passChIsoCorrTight( std::string  prefix ) { 

    std::string my_name = "ph_passChIsoCorrTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passChIsoCorrTight, prefix = " << prefix << std::endl; 
     OUT::ph_passChIsoCorrTight->clear(); 
 }; 

 void Copyph_passNeuIsoCorrLooseInToOut( std::string prefix ) { 

    std::string my_name = "ph_passNeuIsoCorrLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passNeuIsoCorrLoose = std::vector<bool>(*IN::ph_passNeuIsoCorrLoose);
}; 

 void Copyph_passNeuIsoCorrLooseInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passNeuIsoCorrLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passNeuIsoCorrLoose->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passNeuIsoCorrLoose" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passNeuIsoCorrLoose" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passNeuIsoCorrLoose->push_back( IN::ph_passNeuIsoCorrLoose->at(index) ); 
 }; 

 void ClearOutputph_passNeuIsoCorrLoose( std::string  prefix ) { 

    std::string my_name = "ph_passNeuIsoCorrLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passNeuIsoCorrLoose, prefix = " << prefix << std::endl; 
     OUT::ph_passNeuIsoCorrLoose->clear(); 
 }; 

 void Copyph_passNeuIsoCorrMediumInToOut( std::string prefix ) { 

    std::string my_name = "ph_passNeuIsoCorrMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passNeuIsoCorrMedium = std::vector<bool>(*IN::ph_passNeuIsoCorrMedium);
}; 

 void Copyph_passNeuIsoCorrMediumInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passNeuIsoCorrMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passNeuIsoCorrMedium->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passNeuIsoCorrMedium" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passNeuIsoCorrMedium" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passNeuIsoCorrMedium->push_back( IN::ph_passNeuIsoCorrMedium->at(index) ); 
 }; 

 void ClearOutputph_passNeuIsoCorrMedium( std::string  prefix ) { 

    std::string my_name = "ph_passNeuIsoCorrMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passNeuIsoCorrMedium, prefix = " << prefix << std::endl; 
     OUT::ph_passNeuIsoCorrMedium->clear(); 
 }; 

 void Copyph_passNeuIsoCorrTightInToOut( std::string prefix ) { 

    std::string my_name = "ph_passNeuIsoCorrTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passNeuIsoCorrTight = std::vector<bool>(*IN::ph_passNeuIsoCorrTight);
}; 

 void Copyph_passNeuIsoCorrTightInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passNeuIsoCorrTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passNeuIsoCorrTight->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passNeuIsoCorrTight" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passNeuIsoCorrTight" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passNeuIsoCorrTight->push_back( IN::ph_passNeuIsoCorrTight->at(index) ); 
 }; 

 void ClearOutputph_passNeuIsoCorrTight( std::string  prefix ) { 

    std::string my_name = "ph_passNeuIsoCorrTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passNeuIsoCorrTight, prefix = " << prefix << std::endl; 
     OUT::ph_passNeuIsoCorrTight->clear(); 
 }; 

 void Copyph_passPhoIsoCorrLooseInToOut( std::string prefix ) { 

    std::string my_name = "ph_passPhoIsoCorrLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passPhoIsoCorrLoose = std::vector<bool>(*IN::ph_passPhoIsoCorrLoose);
}; 

 void Copyph_passPhoIsoCorrLooseInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passPhoIsoCorrLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passPhoIsoCorrLoose->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passPhoIsoCorrLoose" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passPhoIsoCorrLoose" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passPhoIsoCorrLoose->push_back( IN::ph_passPhoIsoCorrLoose->at(index) ); 
 }; 

 void ClearOutputph_passPhoIsoCorrLoose( std::string  prefix ) { 

    std::string my_name = "ph_passPhoIsoCorrLoose";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passPhoIsoCorrLoose, prefix = " << prefix << std::endl; 
     OUT::ph_passPhoIsoCorrLoose->clear(); 
 }; 

 void Copyph_passPhoIsoCorrMediumInToOut( std::string prefix ) { 

    std::string my_name = "ph_passPhoIsoCorrMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passPhoIsoCorrMedium = std::vector<bool>(*IN::ph_passPhoIsoCorrMedium);
}; 

 void Copyph_passPhoIsoCorrMediumInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passPhoIsoCorrMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passPhoIsoCorrMedium->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passPhoIsoCorrMedium" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passPhoIsoCorrMedium" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passPhoIsoCorrMedium->push_back( IN::ph_passPhoIsoCorrMedium->at(index) ); 
 }; 

 void ClearOutputph_passPhoIsoCorrMedium( std::string  prefix ) { 

    std::string my_name = "ph_passPhoIsoCorrMedium";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passPhoIsoCorrMedium, prefix = " << prefix << std::endl; 
     OUT::ph_passPhoIsoCorrMedium->clear(); 
 }; 

 void Copyph_passPhoIsoCorrTightInToOut( std::string prefix ) { 

    std::string my_name = "ph_passPhoIsoCorrTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_passPhoIsoCorrTight = std::vector<bool>(*IN::ph_passPhoIsoCorrTight);
}; 

 void Copyph_passPhoIsoCorrTightInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_passPhoIsoCorrTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_passPhoIsoCorrTight->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_passPhoIsoCorrTight" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_passPhoIsoCorrTight" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_passPhoIsoCorrTight->push_back( IN::ph_passPhoIsoCorrTight->at(index) ); 
 }; 

 void ClearOutputph_passPhoIsoCorrTight( std::string  prefix ) { 

    std::string my_name = "ph_passPhoIsoCorrTight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_passPhoIsoCorrTight, prefix = " << prefix << std::endl; 
     OUT::ph_passPhoIsoCorrTight->clear(); 
 }; 

 void Copyph_truthMatch_elInToOut( std::string prefix ) { 

    std::string my_name = "ph_truthMatch_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_truthMatch_el = std::vector<bool>(*IN::ph_truthMatch_el);
}; 

 void Copyph_truthMatch_elInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_truthMatch_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_truthMatch_el->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_truthMatch_el" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_truthMatch_el" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_truthMatch_el->push_back( IN::ph_truthMatch_el->at(index) ); 
 }; 

 void ClearOutputph_truthMatch_el( std::string  prefix ) { 

    std::string my_name = "ph_truthMatch_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_truthMatch_el, prefix = " << prefix << std::endl; 
     OUT::ph_truthMatch_el->clear(); 
 }; 

 void Copyph_truthMinDR_elInToOut( std::string prefix ) { 

    std::string my_name = "ph_truthMinDR_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_truthMinDR_el = std::vector<float>(*IN::ph_truthMinDR_el);
}; 

 void Copyph_truthMinDR_elInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_truthMinDR_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_truthMinDR_el->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_truthMinDR_el" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_truthMinDR_el" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_truthMinDR_el->push_back( IN::ph_truthMinDR_el->at(index) ); 
 }; 

 void ClearOutputph_truthMinDR_el( std::string  prefix ) { 

    std::string my_name = "ph_truthMinDR_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_truthMinDR_el, prefix = " << prefix << std::endl; 
     OUT::ph_truthMinDR_el->clear(); 
 }; 

 void Copyph_truthMatchPt_elInToOut( std::string prefix ) { 

    std::string my_name = "ph_truthMatchPt_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_truthMatchPt_el = std::vector<float>(*IN::ph_truthMatchPt_el);
}; 

 void Copyph_truthMatchPt_elInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_truthMatchPt_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_truthMatchPt_el->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_truthMatchPt_el" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_truthMatchPt_el" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_truthMatchPt_el->push_back( IN::ph_truthMatchPt_el->at(index) ); 
 }; 

 void ClearOutputph_truthMatchPt_el( std::string  prefix ) { 

    std::string my_name = "ph_truthMatchPt_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_truthMatchPt_el, prefix = " << prefix << std::endl; 
     OUT::ph_truthMatchPt_el->clear(); 
 }; 

 void Copyph_truthMatch_phInToOut( std::string prefix ) { 

    std::string my_name = "ph_truthMatch_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_truthMatch_ph = std::vector<bool>(*IN::ph_truthMatch_ph);
}; 

 void Copyph_truthMatch_phInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_truthMatch_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_truthMatch_ph->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_truthMatch_ph" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_truthMatch_ph" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_truthMatch_ph->push_back( IN::ph_truthMatch_ph->at(index) ); 
 }; 

 void ClearOutputph_truthMatch_ph( std::string  prefix ) { 

    std::string my_name = "ph_truthMatch_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_truthMatch_ph, prefix = " << prefix << std::endl; 
     OUT::ph_truthMatch_ph->clear(); 
 }; 

 void Copyph_truthMinDR_phInToOut( std::string prefix ) { 

    std::string my_name = "ph_truthMinDR_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_truthMinDR_ph = std::vector<float>(*IN::ph_truthMinDR_ph);
}; 

 void Copyph_truthMinDR_phInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_truthMinDR_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_truthMinDR_ph->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_truthMinDR_ph" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_truthMinDR_ph" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_truthMinDR_ph->push_back( IN::ph_truthMinDR_ph->at(index) ); 
 }; 

 void ClearOutputph_truthMinDR_ph( std::string  prefix ) { 

    std::string my_name = "ph_truthMinDR_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_truthMinDR_ph, prefix = " << prefix << std::endl; 
     OUT::ph_truthMinDR_ph->clear(); 
 }; 

 void Copyph_truthMatchPt_phInToOut( std::string prefix ) { 

    std::string my_name = "ph_truthMatchPt_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_truthMatchPt_ph = std::vector<float>(*IN::ph_truthMatchPt_ph);
}; 

 void Copyph_truthMatchPt_phInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_truthMatchPt_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_truthMatchPt_ph->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_truthMatchPt_ph" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_truthMatchPt_ph" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_truthMatchPt_ph->push_back( IN::ph_truthMatchPt_ph->at(index) ); 
 }; 

 void ClearOutputph_truthMatchPt_ph( std::string  prefix ) { 

    std::string my_name = "ph_truthMatchPt_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_truthMatchPt_ph, prefix = " << prefix << std::endl; 
     OUT::ph_truthMatchPt_ph->clear(); 
 }; 

 void Copyph_truthMatchMotherPID_phInToOut( std::string prefix ) { 

    std::string my_name = "ph_truthMatchMotherPID_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_truthMatchMotherPID_ph = std::vector<int>(*IN::ph_truthMatchMotherPID_ph);
}; 

 void Copyph_truthMatchMotherPID_phInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_truthMatchMotherPID_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_truthMatchMotherPID_ph->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_truthMatchMotherPID_ph" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_truthMatchMotherPID_ph" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_truthMatchMotherPID_ph->push_back( IN::ph_truthMatchMotherPID_ph->at(index) ); 
 }; 

 void ClearOutputph_truthMatchMotherPID_ph( std::string  prefix ) { 

    std::string my_name = "ph_truthMatchMotherPID_ph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_truthMatchMotherPID_ph, prefix = " << prefix << std::endl; 
     OUT::ph_truthMatchMotherPID_ph->clear(); 
 }; 

 void Copyph_hasSLConvInToOut( std::string prefix ) { 

    std::string my_name = "ph_hasSLConv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_hasSLConv = std::vector<bool>(*IN::ph_hasSLConv);
}; 

 void Copyph_hasSLConvInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_hasSLConv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_hasSLConv->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_hasSLConv" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_hasSLConv" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_hasSLConv->push_back( IN::ph_hasSLConv->at(index) ); 
 }; 

 void ClearOutputph_hasSLConv( std::string  prefix ) { 

    std::string my_name = "ph_hasSLConv";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_hasSLConv, prefix = " << prefix << std::endl; 
     OUT::ph_hasSLConv->clear(); 
 }; 

 void Copyph_pass_mva_preselInToOut( std::string prefix ) { 

    std::string my_name = "ph_pass_mva_presel";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_pass_mva_presel = std::vector<bool>(*IN::ph_pass_mva_presel);
}; 

 void Copyph_pass_mva_preselInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_pass_mva_presel";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_pass_mva_presel->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_pass_mva_presel" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_pass_mva_presel" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_pass_mva_presel->push_back( IN::ph_pass_mva_presel->at(index) ); 
 }; 

 void ClearOutputph_pass_mva_presel( std::string  prefix ) { 

    std::string my_name = "ph_pass_mva_presel";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_pass_mva_presel, prefix = " << prefix << std::endl; 
     OUT::ph_pass_mva_presel->clear(); 
 }; 

 void Copyph_mvascoreInToOut( std::string prefix ) { 

    std::string my_name = "ph_mvascore";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_mvascore = std::vector<float>(*IN::ph_mvascore);
}; 

 void Copyph_mvascoreInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_mvascore";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_mvascore->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_mvascore" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_mvascore" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_mvascore->push_back( IN::ph_mvascore->at(index) ); 
 }; 

 void ClearOutputph_mvascore( std::string  prefix ) { 

    std::string my_name = "ph_mvascore";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_mvascore, prefix = " << prefix << std::endl; 
     OUT::ph_mvascore->clear(); 
 }; 

 void Copyph_IsEBInToOut( std::string prefix ) { 

    std::string my_name = "ph_IsEB";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_IsEB = std::vector<bool>(*IN::ph_IsEB);
}; 

 void Copyph_IsEBInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_IsEB";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_IsEB->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_IsEB" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_IsEB" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_IsEB->push_back( IN::ph_IsEB->at(index) ); 
 }; 

 void ClearOutputph_IsEB( std::string  prefix ) { 

    std::string my_name = "ph_IsEB";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_IsEB, prefix = " << prefix << std::endl; 
     OUT::ph_IsEB->clear(); 
 }; 

 void Copyph_IsEEInToOut( std::string prefix ) { 

    std::string my_name = "ph_IsEE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_IsEE = std::vector<bool>(*IN::ph_IsEE);
}; 

 void Copyph_IsEEInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_IsEE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_IsEE->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_IsEE" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_IsEE" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_IsEE->push_back( IN::ph_IsEE->at(index) ); 
 }; 

 void ClearOutputph_IsEE( std::string  prefix ) { 

    std::string my_name = "ph_IsEE";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_IsEE, prefix = " << prefix << std::endl; 
     OUT::ph_IsEE->clear(); 
 }; 

 void Copyjet_ptInToOut( std::string prefix ) { 

    std::string my_name = "jet_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::jet_pt = std::vector<float>(*IN::jet_pt);
}; 

 void Copyjet_ptInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "jet_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::jet_pt->size() ) {
         std::cout << "Vector size exceeded for branch IN::jet_pt" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible jet_pt" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::jet_pt->push_back( IN::jet_pt->at(index) ); 
 }; 

 void ClearOutputjet_pt( std::string  prefix ) { 

    std::string my_name = "jet_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible jet_pt, prefix = " << prefix << std::endl; 
     OUT::jet_pt->clear(); 
 }; 

 void Copyjet_etaInToOut( std::string prefix ) { 

    std::string my_name = "jet_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::jet_eta = std::vector<float>(*IN::jet_eta);
}; 

 void Copyjet_etaInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "jet_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::jet_eta->size() ) {
         std::cout << "Vector size exceeded for branch IN::jet_eta" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible jet_eta" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::jet_eta->push_back( IN::jet_eta->at(index) ); 
 }; 

 void ClearOutputjet_eta( std::string  prefix ) { 

    std::string my_name = "jet_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible jet_eta, prefix = " << prefix << std::endl; 
     OUT::jet_eta->clear(); 
 }; 

 void Copyjet_phiInToOut( std::string prefix ) { 

    std::string my_name = "jet_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::jet_phi = std::vector<float>(*IN::jet_phi);
}; 

 void Copyjet_phiInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "jet_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::jet_phi->size() ) {
         std::cout << "Vector size exceeded for branch IN::jet_phi" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible jet_phi" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::jet_phi->push_back( IN::jet_phi->at(index) ); 
 }; 

 void ClearOutputjet_phi( std::string  prefix ) { 

    std::string my_name = "jet_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible jet_phi, prefix = " << prefix << std::endl; 
     OUT::jet_phi->clear(); 
 }; 

 void Copyjet_eInToOut( std::string prefix ) { 

    std::string my_name = "jet_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::jet_e = std::vector<float>(*IN::jet_e);
}; 

 void Copyjet_eInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "jet_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::jet_e->size() ) {
         std::cout << "Vector size exceeded for branch IN::jet_e" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible jet_e" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::jet_e->push_back( IN::jet_e->at(index) ); 
 }; 

 void ClearOutputjet_e( std::string  prefix ) { 

    std::string my_name = "jet_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible jet_e, prefix = " << prefix << std::endl; 
     OUT::jet_e->clear(); 
 }; 

 void CopyPUWeightInToOut( std::string prefix ) { 

    std::string my_name = "PUWeight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::PUWeight = IN::PUWeight;
}; 

 void CopyisBlindedInToOut( std::string prefix ) { 

    std::string my_name = "isBlinded";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::isBlinded = IN::isBlinded;
}; 

 void CopyEventWeightInToOut( std::string prefix ) { 

    std::string my_name = "EventWeight";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::EventWeight = IN::EventWeight;
}; 

 void Copymu_pt25_nInToOut( std::string prefix ) { 

    std::string my_name = "mu_pt25_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::mu_pt25_n = IN::mu_pt25_n;
}; 

 void Copymu_passtrig_nInToOut( std::string prefix ) { 

    std::string my_name = "mu_passtrig_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::mu_passtrig_n = IN::mu_passtrig_n;
}; 

 void Copymu_passtrig25_nInToOut( std::string prefix ) { 

    std::string my_name = "mu_passtrig25_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::mu_passtrig25_n = IN::mu_passtrig25_n;
}; 

 void Copyel_pt25_nInToOut( std::string prefix ) { 

    std::string my_name = "el_pt25_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::el_pt25_n = IN::el_pt25_n;
}; 

 void Copyel_passtrig_nInToOut( std::string prefix ) { 

    std::string my_name = "el_passtrig_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::el_passtrig_n = IN::el_passtrig_n;
}; 

 void Copyel_passtrig28_nInToOut( std::string prefix ) { 

    std::string my_name = "el_passtrig28_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::el_passtrig28_n = IN::el_passtrig28_n;
}; 

 void Copyph_mediumNoSIEIE_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoSIEIE_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoSIEIE_n = IN::ph_mediumNoSIEIE_n;
}; 

 void Copyph_medium_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_medium_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_medium_n = IN::ph_medium_n;
}; 

 void Copyph_mediumNoEleVeto_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoEleVeto_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoEleVeto_n = IN::ph_mediumNoEleVeto_n;
}; 

 void Copyph_mediumNoSIEIENoEleVeto_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoSIEIENoEleVeto_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoSIEIENoEleVeto_n = IN::ph_mediumNoSIEIENoEleVeto_n;
}; 

 void Copyph_mediumNoIso_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoIso_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoIso_n = IN::ph_mediumNoIso_n;
}; 

 void Copyph_mediumNoChIso_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoChIso_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoChIso_n = IN::ph_mediumNoChIso_n;
}; 

 void Copyph_mediumNoNeuIso_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoNeuIso_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoNeuIso_n = IN::ph_mediumNoNeuIso_n;
}; 

 void Copyph_mediumNoPhoIso_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoPhoIso_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoPhoIso_n = IN::ph_mediumNoPhoIso_n;
}; 

 void Copyph_mediumNoChIsoNoNeuIso_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoChIsoNoNeuIso_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoChIsoNoNeuIso_n = IN::ph_mediumNoChIsoNoNeuIso_n;
}; 

 void Copyph_mediumNoChIsoNoPhoIso_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoChIsoNoPhoIso_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoChIsoNoPhoIso_n = IN::ph_mediumNoChIsoNoPhoIso_n;
}; 

 void Copyph_mediumNoNeuIsoNoPhoIso_nInToOut( std::string prefix ) { 

    std::string my_name = "ph_mediumNoNeuIsoNoPhoIso_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_mediumNoNeuIsoNoPhoIso_n = IN::ph_mediumNoNeuIsoNoPhoIso_n;
}; 

 void Copyph_trigMatch_elInToOut( std::string prefix ) { 

    std::string my_name = "ph_trigMatch_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::ph_trigMatch_el = std::vector<bool>(*IN::ph_trigMatch_el);
}; 

 void Copyph_trigMatch_elInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "ph_trigMatch_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::ph_trigMatch_el->size() ) {
         std::cout << "Vector size exceeded for branch IN::ph_trigMatch_el" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible ph_trigMatch_el" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::ph_trigMatch_el->push_back( IN::ph_trigMatch_el->at(index) ); 
 }; 

 void ClearOutputph_trigMatch_el( std::string  prefix ) { 

    std::string my_name = "ph_trigMatch_el";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible ph_trigMatch_el, prefix = " << prefix << std::endl; 
     OUT::ph_trigMatch_el->clear(); 
 }; 

 void CopyleadPhot_ptInToOut( std::string prefix ) { 

    std::string my_name = "leadPhot_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::leadPhot_pt = IN::leadPhot_pt;
}; 

 void CopysublPhot_ptInToOut( std::string prefix ) { 

    std::string my_name = "sublPhot_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::sublPhot_pt = IN::sublPhot_pt;
}; 

 void CopyleadPhot_lepDRInToOut( std::string prefix ) { 

    std::string my_name = "leadPhot_lepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::leadPhot_lepDR = IN::leadPhot_lepDR;
}; 

 void CopysublPhot_lepDRInToOut( std::string prefix ) { 

    std::string my_name = "sublPhot_lepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::sublPhot_lepDR = IN::sublPhot_lepDR;
}; 

 void Copyph_phDRInToOut( std::string prefix ) { 

    std::string my_name = "ph_phDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_phDR = IN::ph_phDR;
}; 

 void CopyphPhot_lepDRInToOut( std::string prefix ) { 

    std::string my_name = "phPhot_lepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::phPhot_lepDR = IN::phPhot_lepDR;
}; 

 void CopyleadPhot_lepDPhiInToOut( std::string prefix ) { 

    std::string my_name = "leadPhot_lepDPhi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::leadPhot_lepDPhi = IN::leadPhot_lepDPhi;
}; 

 void CopysublPhot_lepDPhiInToOut( std::string prefix ) { 

    std::string my_name = "sublPhot_lepDPhi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::sublPhot_lepDPhi = IN::sublPhot_lepDPhi;
}; 

 void Copyph_phDPhiInToOut( std::string prefix ) { 

    std::string my_name = "ph_phDPhi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::ph_phDPhi = IN::ph_phDPhi;
}; 

 void CopyphPhot_lepDPhiInToOut( std::string prefix ) { 

    std::string my_name = "phPhot_lepDPhi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::phPhot_lepDPhi = IN::phPhot_lepDPhi;
}; 

 void Copydphi_met_lep1InToOut( std::string prefix ) { 

    std::string my_name = "dphi_met_lep1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::dphi_met_lep1 = IN::dphi_met_lep1;
}; 

 void Copydphi_met_lep2InToOut( std::string prefix ) { 

    std::string my_name = "dphi_met_lep2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::dphi_met_lep2 = IN::dphi_met_lep2;
}; 

 void Copydphi_met_ph1InToOut( std::string prefix ) { 

    std::string my_name = "dphi_met_ph1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::dphi_met_ph1 = IN::dphi_met_ph1;
}; 

 void Copydphi_met_ph2InToOut( std::string prefix ) { 

    std::string my_name = "dphi_met_ph2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::dphi_met_ph2 = IN::dphi_met_ph2;
}; 

 void Copymt_lep_metInToOut( std::string prefix ) { 

    std::string my_name = "mt_lep_met";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::mt_lep_met = IN::mt_lep_met;
}; 

 void Copymt_lepph1_metInToOut( std::string prefix ) { 

    std::string my_name = "mt_lepph1_met";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::mt_lepph1_met = IN::mt_lepph1_met;
}; 

 void Copymt_lepph2_metInToOut( std::string prefix ) { 

    std::string my_name = "mt_lepph2_met";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::mt_lepph2_met = IN::mt_lepph2_met;
}; 

 void Copymt_lepphph_metInToOut( std::string prefix ) { 

    std::string my_name = "mt_lepphph_met";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::mt_lepphph_met = IN::mt_lepphph_met;
}; 

 void Copym_leplepInToOut( std::string prefix ) { 

    std::string my_name = "m_leplep";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_leplep = IN::m_leplep;
}; 

 void Copym_lepph1InToOut( std::string prefix ) { 

    std::string my_name = "m_lepph1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_lepph1 = IN::m_lepph1;
}; 

 void Copym_lepph2InToOut( std::string prefix ) { 

    std::string my_name = "m_lepph2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_lepph2 = IN::m_lepph2;
}; 

 void Copym_leplepphInToOut( std::string prefix ) { 

    std::string my_name = "m_leplepph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_leplepph = IN::m_leplepph;
}; 

 void Copym_lepphphInToOut( std::string prefix ) { 

    std::string my_name = "m_lepphph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_lepphph = IN::m_lepphph;
}; 

 void Copym_phphInToOut( std::string prefix ) { 

    std::string my_name = "m_phph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_phph = IN::m_phph;
}; 

 void Copym_leplepZInToOut( std::string prefix ) { 

    std::string my_name = "m_leplepZ";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_leplepZ = IN::m_leplepZ;
}; 

 void Copym_3lepInToOut( std::string prefix ) { 

    std::string my_name = "m_3lep";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_3lep = IN::m_3lep;
}; 

 void Copym_4lepInToOut( std::string prefix ) { 

    std::string my_name = "m_4lep";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_4lep = IN::m_4lep;
}; 

 void Copypt_phphInToOut( std::string prefix ) { 

    std::string my_name = "pt_phph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pt_phph = IN::pt_phph;
}; 

 void Copypt_leplepInToOut( std::string prefix ) { 

    std::string my_name = "pt_leplep";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pt_leplep = IN::pt_leplep;
}; 

 void Copypt_lepph1InToOut( std::string prefix ) { 

    std::string my_name = "pt_lepph1";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pt_lepph1 = IN::pt_lepph1;
}; 

 void Copypt_lepph2InToOut( std::string prefix ) { 

    std::string my_name = "pt_lepph2";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pt_lepph2 = IN::pt_lepph2;
}; 

 void Copypt_lepphphInToOut( std::string prefix ) { 

    std::string my_name = "pt_lepphph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pt_lepphph = IN::pt_lepphph;
}; 

 void Copypt_leplepphInToOut( std::string prefix ) { 

    std::string my_name = "pt_leplepph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pt_leplepph = IN::pt_leplepph;
}; 

 void Copypt_secondLeptonInToOut( std::string prefix ) { 

    std::string my_name = "pt_secondLepton";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pt_secondLepton = IN::pt_secondLepton;
}; 

 void Copypt_thirdLeptonInToOut( std::string prefix ) { 

    std::string my_name = "pt_thirdLepton";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::pt_thirdLepton = IN::pt_thirdLepton;
}; 

 void CopyleadPhot_leadLepDRInToOut( std::string prefix ) { 

    std::string my_name = "leadPhot_leadLepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::leadPhot_leadLepDR = IN::leadPhot_leadLepDR;
}; 

 void CopyleadPhot_sublLepDRInToOut( std::string prefix ) { 

    std::string my_name = "leadPhot_sublLepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::leadPhot_sublLepDR = IN::leadPhot_sublLepDR;
}; 

 void CopysublPhot_leadLepDRInToOut( std::string prefix ) { 

    std::string my_name = "sublPhot_leadLepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::sublPhot_leadLepDR = IN::sublPhot_leadLepDR;
}; 

 void CopysublPhot_sublLepDRInToOut( std::string prefix ) { 

    std::string my_name = "sublPhot_sublLepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::sublPhot_sublLepDR = IN::sublPhot_sublLepDR;
}; 

 void Copym_nearestToZInToOut( std::string prefix ) { 

    std::string my_name = "m_nearestToZ";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_nearestToZ = IN::m_nearestToZ;
}; 

 void Copym_minZdifflepphInToOut( std::string prefix ) { 

    std::string my_name = "m_minZdifflepph";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::m_minZdifflepph = IN::m_minZdifflepph;
}; 

 void Copytruelep_nInToOut( std::string prefix ) { 

    std::string my_name = "truelep_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::truelep_n = IN::truelep_n;
}; 

 void Copytrueph_nInToOut( std::string prefix ) { 

    std::string my_name = "trueph_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::trueph_n = IN::trueph_n;
}; 

 void Copytrueph_wmother_nInToOut( std::string prefix ) { 

    std::string my_name = "trueph_wmother_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::trueph_wmother_n = IN::trueph_wmother_n;
}; 

 void Copytruegenph_nInToOut( std::string prefix ) { 

    std::string my_name = "truegenph_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::truegenph_n = IN::truegenph_n;
}; 

 void Copytruegenphpt15_nInToOut( std::string prefix ) { 

    std::string my_name = "truegenphpt15_n";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::truegenphpt15_n = IN::truegenphpt15_n;
}; 

 void Copytruelep_ptInToOut( std::string prefix ) { 

    std::string my_name = "truelep_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::truelep_pt = std::vector<float>(*IN::truelep_pt);
}; 

 void Copytruelep_ptInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "truelep_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::truelep_pt->size() ) {
         std::cout << "Vector size exceeded for branch IN::truelep_pt" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible truelep_pt" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::truelep_pt->push_back( IN::truelep_pt->at(index) ); 
 }; 

 void ClearOutputtruelep_pt( std::string  prefix ) { 

    std::string my_name = "truelep_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible truelep_pt, prefix = " << prefix << std::endl; 
     OUT::truelep_pt->clear(); 
 }; 

 void Copytruelep_etaInToOut( std::string prefix ) { 

    std::string my_name = "truelep_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::truelep_eta = std::vector<float>(*IN::truelep_eta);
}; 

 void Copytruelep_etaInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "truelep_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::truelep_eta->size() ) {
         std::cout << "Vector size exceeded for branch IN::truelep_eta" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible truelep_eta" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::truelep_eta->push_back( IN::truelep_eta->at(index) ); 
 }; 

 void ClearOutputtruelep_eta( std::string  prefix ) { 

    std::string my_name = "truelep_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible truelep_eta, prefix = " << prefix << std::endl; 
     OUT::truelep_eta->clear(); 
 }; 

 void Copytruelep_phiInToOut( std::string prefix ) { 

    std::string my_name = "truelep_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::truelep_phi = std::vector<float>(*IN::truelep_phi);
}; 

 void Copytruelep_phiInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "truelep_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::truelep_phi->size() ) {
         std::cout << "Vector size exceeded for branch IN::truelep_phi" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible truelep_phi" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::truelep_phi->push_back( IN::truelep_phi->at(index) ); 
 }; 

 void ClearOutputtruelep_phi( std::string  prefix ) { 

    std::string my_name = "truelep_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible truelep_phi, prefix = " << prefix << std::endl; 
     OUT::truelep_phi->clear(); 
 }; 

 void Copytruelep_eInToOut( std::string prefix ) { 

    std::string my_name = "truelep_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::truelep_e = std::vector<float>(*IN::truelep_e);
}; 

 void Copytruelep_eInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "truelep_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::truelep_e->size() ) {
         std::cout << "Vector size exceeded for branch IN::truelep_e" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible truelep_e" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::truelep_e->push_back( IN::truelep_e->at(index) ); 
 }; 

 void ClearOutputtruelep_e( std::string  prefix ) { 

    std::string my_name = "truelep_e";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible truelep_e, prefix = " << prefix << std::endl; 
     OUT::truelep_e->clear(); 
 }; 

 void Copytruelep_isElecInToOut( std::string prefix ) { 

    std::string my_name = "truelep_isElec";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::truelep_isElec = std::vector<bool>(*IN::truelep_isElec);
}; 

 void Copytruelep_isElecInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "truelep_isElec";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::truelep_isElec->size() ) {
         std::cout << "Vector size exceeded for branch IN::truelep_isElec" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible truelep_isElec" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::truelep_isElec->push_back( IN::truelep_isElec->at(index) ); 
 }; 

 void ClearOutputtruelep_isElec( std::string  prefix ) { 

    std::string my_name = "truelep_isElec";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible truelep_isElec, prefix = " << prefix << std::endl; 
     OUT::truelep_isElec->clear(); 
 }; 

 void Copytruelep_isMuonInToOut( std::string prefix ) { 

    std::string my_name = "truelep_isMuon";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::truelep_isMuon = std::vector<bool>(*IN::truelep_isMuon);
}; 

 void Copytruelep_isMuonInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "truelep_isMuon";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::truelep_isMuon->size() ) {
         std::cout << "Vector size exceeded for branch IN::truelep_isMuon" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible truelep_isMuon" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::truelep_isMuon->push_back( IN::truelep_isMuon->at(index) ); 
 }; 

 void ClearOutputtruelep_isMuon( std::string  prefix ) { 

    std::string my_name = "truelep_isMuon";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible truelep_isMuon, prefix = " << prefix << std::endl; 
     OUT::truelep_isMuon->clear(); 
 }; 

 void Copytruelep_motherPIDInToOut( std::string prefix ) { 

    std::string my_name = "truelep_motherPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::truelep_motherPID = std::vector<int>(*IN::truelep_motherPID);
}; 

 void Copytruelep_motherPIDInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "truelep_motherPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::truelep_motherPID->size() ) {
         std::cout << "Vector size exceeded for branch IN::truelep_motherPID" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible truelep_motherPID" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::truelep_motherPID->push_back( IN::truelep_motherPID->at(index) ); 
 }; 

 void ClearOutputtruelep_motherPID( std::string  prefix ) { 

    std::string my_name = "truelep_motherPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible truelep_motherPID, prefix = " << prefix << std::endl; 
     OUT::truelep_motherPID->clear(); 
 }; 

 void Copytrueph_ptInToOut( std::string prefix ) { 

    std::string my_name = "trueph_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::trueph_pt = std::vector<float>(*IN::trueph_pt);
}; 

 void Copytrueph_ptInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "trueph_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::trueph_pt->size() ) {
         std::cout << "Vector size exceeded for branch IN::trueph_pt" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible trueph_pt" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::trueph_pt->push_back( IN::trueph_pt->at(index) ); 
 }; 

 void ClearOutputtrueph_pt( std::string  prefix ) { 

    std::string my_name = "trueph_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible trueph_pt, prefix = " << prefix << std::endl; 
     OUT::trueph_pt->clear(); 
 }; 

 void Copytrueph_etaInToOut( std::string prefix ) { 

    std::string my_name = "trueph_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::trueph_eta = std::vector<float>(*IN::trueph_eta);
}; 

 void Copytrueph_etaInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "trueph_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::trueph_eta->size() ) {
         std::cout << "Vector size exceeded for branch IN::trueph_eta" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible trueph_eta" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::trueph_eta->push_back( IN::trueph_eta->at(index) ); 
 }; 

 void ClearOutputtrueph_eta( std::string  prefix ) { 

    std::string my_name = "trueph_eta";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible trueph_eta, prefix = " << prefix << std::endl; 
     OUT::trueph_eta->clear(); 
 }; 

 void Copytrueph_phiInToOut( std::string prefix ) { 

    std::string my_name = "trueph_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::trueph_phi = std::vector<float>(*IN::trueph_phi);
}; 

 void Copytrueph_phiInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "trueph_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::trueph_phi->size() ) {
         std::cout << "Vector size exceeded for branch IN::trueph_phi" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible trueph_phi" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::trueph_phi->push_back( IN::trueph_phi->at(index) ); 
 }; 

 void ClearOutputtrueph_phi( std::string  prefix ) { 

    std::string my_name = "trueph_phi";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible trueph_phi, prefix = " << prefix << std::endl; 
     OUT::trueph_phi->clear(); 
 }; 

 void Copytrueph_motherPIDInToOut( std::string prefix ) { 

    std::string my_name = "trueph_motherPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::trueph_motherPID = std::vector<int>(*IN::trueph_motherPID);
}; 

 void Copytrueph_motherPIDInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "trueph_motherPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::trueph_motherPID->size() ) {
         std::cout << "Vector size exceeded for branch IN::trueph_motherPID" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible trueph_motherPID" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::trueph_motherPID->push_back( IN::trueph_motherPID->at(index) ); 
 }; 

 void ClearOutputtrueph_motherPID( std::string  prefix ) { 

    std::string my_name = "trueph_motherPID";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible trueph_motherPID, prefix = " << prefix << std::endl; 
     OUT::trueph_motherPID->clear(); 
 }; 

 void Copytrueph_parentageInToOut( std::string prefix ) { 

    std::string my_name = "trueph_parentage";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::trueph_parentage = std::vector<int>(*IN::trueph_parentage);
}; 

 void Copytrueph_parentageInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "trueph_parentage";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::trueph_parentage->size() ) {
         std::cout << "Vector size exceeded for branch IN::trueph_parentage" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible trueph_parentage" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::trueph_parentage->push_back( IN::trueph_parentage->at(index) ); 
 }; 

 void ClearOutputtrueph_parentage( std::string  prefix ) { 

    std::string my_name = "trueph_parentage";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible trueph_parentage, prefix = " << prefix << std::endl; 
     OUT::trueph_parentage->clear(); 
 }; 

 void Copytrueph_nearestLepDRInToOut( std::string prefix ) { 

    std::string my_name = "trueph_nearestLepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::trueph_nearestLepDR = std::vector<float>(*IN::trueph_nearestLepDR);
}; 

 void Copytrueph_nearestLepDRInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "trueph_nearestLepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::trueph_nearestLepDR->size() ) {
         std::cout << "Vector size exceeded for branch IN::trueph_nearestLepDR" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible trueph_nearestLepDR" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::trueph_nearestLepDR->push_back( IN::trueph_nearestLepDR->at(index) ); 
 }; 

 void ClearOutputtrueph_nearestLepDR( std::string  prefix ) { 

    std::string my_name = "trueph_nearestLepDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible trueph_nearestLepDR, prefix = " << prefix << std::endl; 
     OUT::trueph_nearestLepDR->clear(); 
 }; 

 void Copytrueph_nearestQrkDRInToOut( std::string prefix ) { 

    std::string my_name = "trueph_nearestQrkDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  *OUT::trueph_nearestQrkDR = std::vector<float>(*IN::trueph_nearestQrkDR);
}; 

 void Copytrueph_nearestQrkDRInToOutIndex( unsigned index, std::string  prefix ) { 

    std::string my_name = "trueph_nearestQrkDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    if( index >= IN::trueph_nearestQrkDR->size() ) {
         std::cout << "Vector size exceeded for branch IN::trueph_nearestQrkDR" << std::endl;
         return; 
     }; 

     //std::cout << "Copy varaible trueph_nearestQrkDR" << " at index " << index << ", prefix = " << prefix << std::endl; 
     OUT::trueph_nearestQrkDR->push_back( IN::trueph_nearestQrkDR->at(index) ); 
 }; 

 void ClearOutputtrueph_nearestQrkDR( std::string  prefix ) { 

    std::string my_name = "trueph_nearestQrkDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
    //std::cout << "Clear varaible trueph_nearestQrkDR, prefix = " << prefix << std::endl; 
     OUT::trueph_nearestQrkDR->clear(); 
 }; 

 void Copytrueleadlep_ptInToOut( std::string prefix ) { 

    std::string my_name = "trueleadlep_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::trueleadlep_pt = IN::trueleadlep_pt;
}; 

 void Copytruesubllep_ptInToOut( std::string prefix ) { 

    std::string my_name = "truesubllep_pt";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::truesubllep_pt = IN::truesubllep_pt;
}; 

 void Copytrueleadlep_leadPhotDRInToOut( std::string prefix ) { 

    std::string my_name = "trueleadlep_leadPhotDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::trueleadlep_leadPhotDR = IN::trueleadlep_leadPhotDR;
}; 

 void Copytrueleadlep_sublPhotDRInToOut( std::string prefix ) { 

    std::string my_name = "trueleadlep_sublPhotDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::trueleadlep_sublPhotDR = IN::trueleadlep_sublPhotDR;
}; 

 void Copytruesubllep_leadPhotDRInToOut( std::string prefix ) { 

    std::string my_name = "truesubllep_leadPhotDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::truesubllep_leadPhotDR = IN::truesubllep_leadPhotDR;
}; 

 void Copytruesubllep_sublPhotDRInToOut( std::string prefix ) { 

    std::string my_name = "truesubllep_sublPhotDR";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::truesubllep_sublPhotDR = IN::truesubllep_sublPhotDR;
}; 

 