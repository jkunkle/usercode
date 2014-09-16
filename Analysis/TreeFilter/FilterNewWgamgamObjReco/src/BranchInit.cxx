#include <algorithm>
#include <iostream>
#include "TTree.h"
#include "TChain.h"
#include "include/BranchInit.h"
#include "include/BranchDefs.h"

namespace IN {
 Int_t				nHLT;
 Int_t				run;
 Long64_t				event;
 Int_t				lumis;
 Bool_t				isData;
 Int_t				HLT[457];
 Int_t				HLTIndex[70];
 Float_t				bspotPos[3];
 Int_t				nVtx;
 Int_t				IsVtxGood;
 Int_t				nGoodVtx;
 Int_t				nVtxBS;
 Float_t				pfMET;
 Float_t				pfMETPhi;
 Float_t				pfMETsumEt;
 Float_t				pfMETmEtSig;
 Float_t				pfMETSig;
 Float_t				pfType01MET;
 Float_t				pfType01METPhi;
 Float_t				pfType01METsumEt;
 Float_t				pfType01METmEtSig;
 Float_t				pfType01METSig;
 Float_t				recoPfMET;
 Float_t				recoPfMETPhi;
 Float_t				recoPfMETsumEt;
 Float_t				recoPfMETmEtSig;
 Float_t				recoPfMETSig;
 Float_t				trkMETxPV;
 Float_t				trkMETyPV;
 Float_t				trkMETPhiPV;
 Float_t				trkMETPV;
 Int_t				metFilters[10];
 Int_t				nEle;
 std::vector<unsigned long>				*eleTrg;
 std::vector<int>				*eleIsEcalDriven;
 std::vector<int>				*eleCharge;
 std::vector<int>				*eleChargeConsistent;
 std::vector<float>				*eleEn;
 std::vector<float>				*eleSCEn;
 std::vector<float>				*elePt;
 std::vector<float>				*eleEta;
 std::vector<float>				*elePhi;
 std::vector<float>				*eleR9;
 std::vector<float>				*eleSCEta;
 std::vector<float>				*eleSCPhi;
 std::vector<float>				*eleSCEtaWidth;
 std::vector<float>				*eleSCPhiWidth;
 std::vector<float>				*eleVtx_x;
 std::vector<float>				*eleVtx_y;
 std::vector<float>				*eleVtx_z;
 std::vector<float>				*eleD0;
 std::vector<float>				*eleDz;
 std::vector<float>				*eleD0GV;
 std::vector<float>				*eleDzGV;
 std::vector<float>				*eleHoverE;
 std::vector<float>				*eleHoverE12;
 std::vector<float>				*eleEoverP;
 std::vector<float>				*eledEtaAtVtx;
 std::vector<float>				*eledPhiAtVtx;
 std::vector<float>				*eleSigmaIEtaIEta;
 std::vector<float>				*eleSigmaIEtaIPhi;
 std::vector<float>				*eleSigmaIPhiIPhi;
 std::vector<float>				*eleEmax;
 std::vector<float>				*eleE2ndMax;
 std::vector<float>				*eleE1x5;
 std::vector<float>				*eleE3x3;
 std::vector<float>				*eleE5x5;
 std::vector<float>				*eleE2x5Max;
 std::vector<int>				*eleRecoFlag;
 std::vector<int>				*elePos;
 std::vector<float>				*eleIsoTrkDR03;
 std::vector<float>				*eleIsoEcalDR03;
 std::vector<float>				*eleIsoHcalDR03;
 std::vector<float>				*eleIsoHcalDR0312;
 std::vector<float>				*eleIsoTrkDR04;
 std::vector<float>				*eleIsoEcalDR04;
 std::vector<float>				*eleIsoHcalDR04;
 std::vector<float>				*eleIsoHcalDR0412;
 std::vector<int>				*eleMissHits;
 std::vector<float>				*eleConvDist;
 std::vector<int>				*eleConvVtxFit;
 std::vector<float>				*eleIDMVATrig;
 std::vector<float>				*elePFChIso03;
 std::vector<float>				*elePFNeuIso03;
 std::vector<float>				*elePFChIso04;
 std::vector<float>				*elePFPhoIso04;
 std::vector<float>				*elePFNeuIso04;
 Int_t				nPho;
 std::vector<unsigned long>				*phoTrg;
 std::vector<unsigned long>				*phoTrgFilter;
 std::vector<bool>				*phoIsPhoton;
 std::vector<float>				*phoE;
 std::vector<float>				*phoEt;
 std::vector<float>				*phoEta;
 std::vector<float>				*phoVtx_x;
 std::vector<float>				*phoVtx_y;
 std::vector<float>				*phoVtx_z;
 std::vector<float>				*phoPhi;
 std::vector<float>				*phoR9;
 std::vector<int>				*phoNClus;
 std::vector<float>				*phoTrkIsoHollowDR03;
 std::vector<float>				*phoEcalIsoDR03;
 std::vector<float>				*phoHcalIsoDR03;
 std::vector<float>				*phoHcalIsoDR0312;
 std::vector<float>				*phoTrkIsoHollowDR04;
 std::vector<float>				*phoEcalIsoDR04;
 std::vector<float>				*phoHcalIsoDR04;
 std::vector<float>				*phoHoverE;
 std::vector<float>				*phoHoverE12;
 std::vector<int>				*phoEleVeto;
 std::vector<float>				*phoSigmaIEtaIEta;
 std::vector<float>				*phoSigmaIEtaIPhi;
 std::vector<float>				*phoSigmaIPhiIPhi;
 std::vector<float>				*phoCiCPF4phopfIso03;
 std::vector<float>				*phoEmax;
 std::vector<float>				*phoE2ndMax;
 std::vector<float>				*phoE3x3;
 std::vector<float>				*phoE3x1;
 std::vector<float>				*phoE1x3;
 std::vector<float>				*phoE5x5;
 std::vector<float>				*phoE1x5;
 std::vector<float>				*phoE2x2;
 std::vector<float>				*phoE2x5Max;
 std::vector<float>				*phoPFChIso;
 std::vector<float>				*phoPFPhoIso;
 std::vector<float>				*phoPFNeuIso;
 std::vector<float>				*phoSCRChIso;
 std::vector<float>				*phoSCRNeuIso;
 std::vector<float>				*phoSCRChIso04;
 std::vector<float>				*phoSCRPhoIso04;
 std::vector<float>				*phoSCRNeuIso04;
 std::vector<float>				*phoRandConeChIso;
 std::vector<float>				*phoRandConePhoIso;
 std::vector<float>				*phoRandConeNeuIso;
 std::vector<float>				*phoRandConeChIso04;
 std::vector<float>				*phoRandConePhoIso04;
 std::vector<float>				*phoRandConeNeuIso04;
 std::vector<int>				*phoRecoFlag;
 std::vector<int>				*phoPos;
 std::vector<float>				*phoSCE;
 std::vector<float>				*phoSCRawE;
 std::vector<float>				*phoESEn;
 std::vector<float>				*phoSCEt;
 std::vector<float>				*phoSCEta;
 std::vector<float>				*phoSCPhi;
 std::vector<float>				*phoSCEtaWidth;
 std::vector<float>				*phoSCPhiWidth;
 std::vector<int>				*phoOverlap;
 std::vector<int>				*phohasPixelSeed;
 std::vector<int>				*pho_hasConvPf;
 std::vector<int>				*pho_hasSLConvPf;
 std::vector<float>				*pho_pfconvVtxZ;
 std::vector<float>				*pho_pfconvVtxZErr;
 std::vector<int>				*pho_nSLConv;
 std::vector<std::vector<float> >				*pho_pfSLConvPos_x;
 std::vector<std::vector<float> >				*pho_pfSLConvPos_y;
 std::vector<std::vector<float> >				*pho_pfSLConvPos_z;
 std::vector<std::vector<float> >				*pho_pfSLConvVtxZ;
 std::vector<int>				*phoIsConv;
 std::vector<int>				*phoNConv;
 std::vector<float>				*phoConvInvMass;
 std::vector<float>				*phoConvCotTheta;
 std::vector<float>				*phoConvEoverP;
 std::vector<float>				*phoConvMinDist;
 std::vector<float>				*phoConvdPhiAtVtx;
 std::vector<float>				*phoConvdPhiAtCalo;
 std::vector<float>				*phoConvdEtaAtCalo;
 std::vector<float>				*phoConvTrkPin_x;
 std::vector<float>				*phoConvTrkPin_y;
 std::vector<float>				*phoConvTrkPout_x;
 std::vector<float>				*phoConvTrkPout_y;
 std::vector<float>				*phoConvChi2;
 std::vector<float>				*phoConvChi2Prob;
 std::vector<int>				*phoConvNTrks;
 std::vector<float>				*phoConvVtx_x;
 std::vector<float>				*phoConvVtx_y;
 std::vector<float>				*phoConvVtx_z;
 std::vector<float>				*phoConvPairMomentum_x;
 std::vector<float>				*phoConvPairMomentum_y;
 std::vector<float>				*phoConvPairMomentum_z;
 std::vector<int>				*SingleLegConv;
 Int_t				nMu;
 std::vector<unsigned long>				*muTrg;
 std::vector<float>				*muEta;
 std::vector<float>				*muPhi;
 std::vector<int>				*muCharge;
 std::vector<float>				*muPt;
 std::vector<float>				*muPz;
 std::vector<float>				*muVtx_x;
 std::vector<float>				*muVtx_y;
 std::vector<float>				*muVtx_z;
 std::vector<float>				*muIsoTrk;
 std::vector<float>				*muIsoCalo;
 std::vector<float>				*muIsoEcal;
 std::vector<float>				*muIsoHcal;
 std::vector<float>				*muChi2NDF;
 std::vector<float>				*muInnerChi2NDF;
 std::vector<float>				*muPFIsoR04_CH;
 std::vector<float>				*muPFIsoR04_NH;
 std::vector<float>				*muPFIsoR04_Pho;
 std::vector<float>				*muPFIsoR04_PU;
 std::vector<float>				*muPFIsoR04_CPart;
 std::vector<float>				*muPFIsoR04_NHHT;
 std::vector<float>				*muPFIsoR04_PhoHT;
 std::vector<float>				*muPFIsoR03_CH;
 std::vector<float>				*muPFIsoR03_NH;
 std::vector<float>				*muPFIsoR03_Pho;
 std::vector<float>				*muPFIsoR03_PU;
 std::vector<float>				*muPFIsoR03_CPart;
 std::vector<float>				*muPFIsoR03_NHHT;
 std::vector<float>				*muPFIsoR03_PhoHT;
 std::vector<int>				*muType;
 std::vector<float>				*muD0;
 std::vector<float>				*muDz;
 std::vector<float>				*muD0GV;
 std::vector<float>				*muDzGV;
 std::vector<float>				*muInnerD0;
 std::vector<float>				*muInnerDz;
 std::vector<float>				*muInnerD0GV;
 std::vector<float>				*muInnerDzGV;
 std::vector<float>				*muInnerPt;
 std::vector<int>				*muNumberOfValidTrkLayers;
 std::vector<int>				*muNumberOfValidTrkHits;
 std::vector<int>				*muNumberOfValidPixelLayers;
 std::vector<int>				*muNumberOfValidPixelHits;
 std::vector<int>				*muNumberOfValidMuonHits;
 std::vector<int>				*muStations;
 std::vector<int>				*muChambers;
 Int_t				nTau;
 Float_t				rho25;
 Float_t				rho25_neu;
 Float_t				rho25_muPFiso;
 Float_t				rho25_elePFiso;
 Float_t				rho2011;
 Float_t				rho2012;
 Float_t				QGTag_MLP;
 Float_t				QGTag_likelihood;
 Int_t				nCA8Jet;
 Int_t				nJet;
 std::vector<unsigned long>				*jetTrg;
 std::vector<float>				*jetEn;
 std::vector<float>				*jetPt;
 std::vector<float>				*jetEta;
 std::vector<float>				*jetPhi;
 std::vector<float>				*jetCharge;
 std::vector<float>				*jetEt;
 std::vector<float>				*jetRawEn;
 std::vector<float>				*jetCHF;
 std::vector<int>				*jetNCH;
 std::vector<float>				*jetNNeutrals;
 std::vector<float>				*jetNCharged;
 std::vector<float>				*jetLeadTrackPt;
 std::vector<float>				*jetVtxPt;
 Int_t				nConv;
 std::vector<float>				*eleD0LepVtx;
 std::vector<float>				*eleDzLepVtx;
 std::vector<float>				*muD0LepVtx;
 std::vector<float>				*muDzLepVtx;
};
namespace OUT {
 Int_t				nVtxBS;
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
};
void InitINTree( TChain * tree) {

  tree->SetBranchAddress("nHLT", &IN::nHLT);
  tree->SetBranchAddress("run", &IN::run);
  tree->SetBranchAddress("event", &IN::event);
  tree->SetBranchAddress("lumis", &IN::lumis);
  tree->SetBranchAddress("isData", &IN::isData);
  tree->SetBranchAddress("HLT", &IN::HLT);
  tree->SetBranchAddress("HLTIndex", &IN::HLTIndex);
  tree->SetBranchAddress("bspotPos", &IN::bspotPos);
  tree->SetBranchAddress("nVtx", &IN::nVtx);
  tree->SetBranchAddress("IsVtxGood", &IN::IsVtxGood);
  tree->SetBranchAddress("nGoodVtx", &IN::nGoodVtx);
  tree->SetBranchAddress("nVtxBS", &IN::nVtxBS);
  tree->SetBranchAddress("pfMET", &IN::pfMET);
  tree->SetBranchAddress("pfMETPhi", &IN::pfMETPhi);
  tree->SetBranchAddress("pfMETsumEt", &IN::pfMETsumEt);
  tree->SetBranchAddress("pfMETmEtSig", &IN::pfMETmEtSig);
  tree->SetBranchAddress("pfMETSig", &IN::pfMETSig);
  tree->SetBranchAddress("pfType01MET", &IN::pfType01MET);
  tree->SetBranchAddress("pfType01METPhi", &IN::pfType01METPhi);
  tree->SetBranchAddress("pfType01METsumEt", &IN::pfType01METsumEt);
  tree->SetBranchAddress("pfType01METmEtSig", &IN::pfType01METmEtSig);
  tree->SetBranchAddress("pfType01METSig", &IN::pfType01METSig);
  tree->SetBranchAddress("recoPfMET", &IN::recoPfMET);
  tree->SetBranchAddress("recoPfMETPhi", &IN::recoPfMETPhi);
  tree->SetBranchAddress("recoPfMETsumEt", &IN::recoPfMETsumEt);
  tree->SetBranchAddress("recoPfMETmEtSig", &IN::recoPfMETmEtSig);
  tree->SetBranchAddress("recoPfMETSig", &IN::recoPfMETSig);
  tree->SetBranchAddress("trkMETxPV", &IN::trkMETxPV);
  tree->SetBranchAddress("trkMETyPV", &IN::trkMETyPV);
  tree->SetBranchAddress("trkMETPhiPV", &IN::trkMETPhiPV);
  tree->SetBranchAddress("trkMETPV", &IN::trkMETPV);
  tree->SetBranchAddress("metFilters", &IN::metFilters);
  tree->SetBranchAddress("nEle", &IN::nEle);
  tree->SetBranchAddress("eleTrg", &IN::eleTrg);
  tree->SetBranchAddress("eleIsEcalDriven", &IN::eleIsEcalDriven);
  tree->SetBranchAddress("eleCharge", &IN::eleCharge);
  tree->SetBranchAddress("eleChargeConsistent", &IN::eleChargeConsistent);
  tree->SetBranchAddress("eleEn", &IN::eleEn);
  tree->SetBranchAddress("eleSCEn", &IN::eleSCEn);
  tree->SetBranchAddress("elePt", &IN::elePt);
  tree->SetBranchAddress("eleEta", &IN::eleEta);
  tree->SetBranchAddress("elePhi", &IN::elePhi);
  tree->SetBranchAddress("eleR9", &IN::eleR9);
  tree->SetBranchAddress("eleSCEta", &IN::eleSCEta);
  tree->SetBranchAddress("eleSCPhi", &IN::eleSCPhi);
  tree->SetBranchAddress("eleSCEtaWidth", &IN::eleSCEtaWidth);
  tree->SetBranchAddress("eleSCPhiWidth", &IN::eleSCPhiWidth);
  tree->SetBranchAddress("eleVtx_x", &IN::eleVtx_x);
  tree->SetBranchAddress("eleVtx_y", &IN::eleVtx_y);
  tree->SetBranchAddress("eleVtx_z", &IN::eleVtx_z);
  tree->SetBranchAddress("eleD0", &IN::eleD0);
  tree->SetBranchAddress("eleDz", &IN::eleDz);
  tree->SetBranchAddress("eleD0GV", &IN::eleD0GV);
  tree->SetBranchAddress("eleDzGV", &IN::eleDzGV);
  tree->SetBranchAddress("eleHoverE", &IN::eleHoverE);
  tree->SetBranchAddress("eleHoverE12", &IN::eleHoverE12);
  tree->SetBranchAddress("eleEoverP", &IN::eleEoverP);
  tree->SetBranchAddress("eledEtaAtVtx", &IN::eledEtaAtVtx);
  tree->SetBranchAddress("eledPhiAtVtx", &IN::eledPhiAtVtx);
  tree->SetBranchAddress("eleSigmaIEtaIEta", &IN::eleSigmaIEtaIEta);
  tree->SetBranchAddress("eleSigmaIEtaIPhi", &IN::eleSigmaIEtaIPhi);
  tree->SetBranchAddress("eleSigmaIPhiIPhi", &IN::eleSigmaIPhiIPhi);
  tree->SetBranchAddress("eleEmax", &IN::eleEmax);
  tree->SetBranchAddress("eleE2ndMax", &IN::eleE2ndMax);
  tree->SetBranchAddress("eleE1x5", &IN::eleE1x5);
  tree->SetBranchAddress("eleE3x3", &IN::eleE3x3);
  tree->SetBranchAddress("eleE5x5", &IN::eleE5x5);
  tree->SetBranchAddress("eleE2x5Max", &IN::eleE2x5Max);
  tree->SetBranchAddress("eleRecoFlag", &IN::eleRecoFlag);
  tree->SetBranchAddress("elePos", &IN::elePos);
  tree->SetBranchAddress("eleIsoTrkDR03", &IN::eleIsoTrkDR03);
  tree->SetBranchAddress("eleIsoEcalDR03", &IN::eleIsoEcalDR03);
  tree->SetBranchAddress("eleIsoHcalDR03", &IN::eleIsoHcalDR03);
  tree->SetBranchAddress("eleIsoHcalDR0312", &IN::eleIsoHcalDR0312);
  tree->SetBranchAddress("eleIsoTrkDR04", &IN::eleIsoTrkDR04);
  tree->SetBranchAddress("eleIsoEcalDR04", &IN::eleIsoEcalDR04);
  tree->SetBranchAddress("eleIsoHcalDR04", &IN::eleIsoHcalDR04);
  tree->SetBranchAddress("eleIsoHcalDR0412", &IN::eleIsoHcalDR0412);
  tree->SetBranchAddress("eleMissHits", &IN::eleMissHits);
  tree->SetBranchAddress("eleConvDist", &IN::eleConvDist);
  tree->SetBranchAddress("eleConvVtxFit", &IN::eleConvVtxFit);
  tree->SetBranchAddress("eleIDMVATrig", &IN::eleIDMVATrig);
  tree->SetBranchAddress("elePFChIso03", &IN::elePFChIso03);
  tree->SetBranchAddress("elePFNeuIso03", &IN::elePFNeuIso03);
  tree->SetBranchAddress("elePFChIso04", &IN::elePFChIso04);
  tree->SetBranchAddress("elePFPhoIso04", &IN::elePFPhoIso04);
  tree->SetBranchAddress("elePFNeuIso04", &IN::elePFNeuIso04);
  tree->SetBranchAddress("nPho", &IN::nPho);
  tree->SetBranchAddress("phoTrg", &IN::phoTrg);
  tree->SetBranchAddress("phoTrgFilter", &IN::phoTrgFilter);
  tree->SetBranchAddress("phoIsPhoton", &IN::phoIsPhoton);
  tree->SetBranchAddress("phoE", &IN::phoE);
  tree->SetBranchAddress("phoEt", &IN::phoEt);
  tree->SetBranchAddress("phoEta", &IN::phoEta);
  tree->SetBranchAddress("phoVtx_x", &IN::phoVtx_x);
  tree->SetBranchAddress("phoVtx_y", &IN::phoVtx_y);
  tree->SetBranchAddress("phoVtx_z", &IN::phoVtx_z);
  tree->SetBranchAddress("phoPhi", &IN::phoPhi);
  tree->SetBranchAddress("phoR9", &IN::phoR9);
  tree->SetBranchAddress("phoNClus", &IN::phoNClus);
  tree->SetBranchAddress("phoTrkIsoHollowDR03", &IN::phoTrkIsoHollowDR03);
  tree->SetBranchAddress("phoEcalIsoDR03", &IN::phoEcalIsoDR03);
  tree->SetBranchAddress("phoHcalIsoDR03", &IN::phoHcalIsoDR03);
  tree->SetBranchAddress("phoHcalIsoDR0312", &IN::phoHcalIsoDR0312);
  tree->SetBranchAddress("phoTrkIsoHollowDR04", &IN::phoTrkIsoHollowDR04);
  tree->SetBranchAddress("phoEcalIsoDR04", &IN::phoEcalIsoDR04);
  tree->SetBranchAddress("phoHcalIsoDR04", &IN::phoHcalIsoDR04);
  tree->SetBranchAddress("phoHoverE", &IN::phoHoverE);
  tree->SetBranchAddress("phoHoverE12", &IN::phoHoverE12);
  tree->SetBranchAddress("phoEleVeto", &IN::phoEleVeto);
  tree->SetBranchAddress("phoSigmaIEtaIEta", &IN::phoSigmaIEtaIEta);
  tree->SetBranchAddress("phoSigmaIEtaIPhi", &IN::phoSigmaIEtaIPhi);
  tree->SetBranchAddress("phoSigmaIPhiIPhi", &IN::phoSigmaIPhiIPhi);
  tree->SetBranchAddress("phoCiCPF4phopfIso03", &IN::phoCiCPF4phopfIso03);
  tree->SetBranchAddress("phoEmax", &IN::phoEmax);
  tree->SetBranchAddress("phoE2ndMax", &IN::phoE2ndMax);
  tree->SetBranchAddress("phoE3x3", &IN::phoE3x3);
  tree->SetBranchAddress("phoE3x1", &IN::phoE3x1);
  tree->SetBranchAddress("phoE1x3", &IN::phoE1x3);
  tree->SetBranchAddress("phoE5x5", &IN::phoE5x5);
  tree->SetBranchAddress("phoE1x5", &IN::phoE1x5);
  tree->SetBranchAddress("phoE2x2", &IN::phoE2x2);
  tree->SetBranchAddress("phoE2x5Max", &IN::phoE2x5Max);
  tree->SetBranchAddress("phoPFChIso", &IN::phoPFChIso);
  tree->SetBranchAddress("phoPFPhoIso", &IN::phoPFPhoIso);
  tree->SetBranchAddress("phoPFNeuIso", &IN::phoPFNeuIso);
  tree->SetBranchAddress("phoSCRChIso", &IN::phoSCRChIso);
  tree->SetBranchAddress("phoSCRNeuIso", &IN::phoSCRNeuIso);
  tree->SetBranchAddress("phoSCRChIso04", &IN::phoSCRChIso04);
  tree->SetBranchAddress("phoSCRPhoIso04", &IN::phoSCRPhoIso04);
  tree->SetBranchAddress("phoSCRNeuIso04", &IN::phoSCRNeuIso04);
  tree->SetBranchAddress("phoRandConeChIso", &IN::phoRandConeChIso);
  tree->SetBranchAddress("phoRandConePhoIso", &IN::phoRandConePhoIso);
  tree->SetBranchAddress("phoRandConeNeuIso", &IN::phoRandConeNeuIso);
  tree->SetBranchAddress("phoRandConeChIso04", &IN::phoRandConeChIso04);
  tree->SetBranchAddress("phoRandConePhoIso04", &IN::phoRandConePhoIso04);
  tree->SetBranchAddress("phoRandConeNeuIso04", &IN::phoRandConeNeuIso04);
  tree->SetBranchAddress("phoRecoFlag", &IN::phoRecoFlag);
  tree->SetBranchAddress("phoPos", &IN::phoPos);
  tree->SetBranchAddress("phoSCE", &IN::phoSCE);
  tree->SetBranchAddress("phoSCRawE", &IN::phoSCRawE);
  tree->SetBranchAddress("phoESEn", &IN::phoESEn);
  tree->SetBranchAddress("phoSCEt", &IN::phoSCEt);
  tree->SetBranchAddress("phoSCEta", &IN::phoSCEta);
  tree->SetBranchAddress("phoSCPhi", &IN::phoSCPhi);
  tree->SetBranchAddress("phoSCEtaWidth", &IN::phoSCEtaWidth);
  tree->SetBranchAddress("phoSCPhiWidth", &IN::phoSCPhiWidth);
  tree->SetBranchAddress("phoOverlap", &IN::phoOverlap);
  tree->SetBranchAddress("phohasPixelSeed", &IN::phohasPixelSeed);
  tree->SetBranchAddress("pho_hasConvPf", &IN::pho_hasConvPf);
  tree->SetBranchAddress("pho_hasSLConvPf", &IN::pho_hasSLConvPf);
  tree->SetBranchAddress("pho_pfconvVtxZ", &IN::pho_pfconvVtxZ);
  tree->SetBranchAddress("pho_pfconvVtxZErr", &IN::pho_pfconvVtxZErr);
  tree->SetBranchAddress("pho_nSLConv", &IN::pho_nSLConv);
  tree->SetBranchAddress("pho_pfSLConvPos_x", &IN::pho_pfSLConvPos_x);
  tree->SetBranchAddress("pho_pfSLConvPos_y", &IN::pho_pfSLConvPos_y);
  tree->SetBranchAddress("pho_pfSLConvPos_z", &IN::pho_pfSLConvPos_z);
  tree->SetBranchAddress("pho_pfSLConvVtxZ", &IN::pho_pfSLConvVtxZ);
  tree->SetBranchAddress("phoIsConv", &IN::phoIsConv);
  tree->SetBranchAddress("phoNConv", &IN::phoNConv);
  tree->SetBranchAddress("phoConvInvMass", &IN::phoConvInvMass);
  tree->SetBranchAddress("phoConvCotTheta", &IN::phoConvCotTheta);
  tree->SetBranchAddress("phoConvEoverP", &IN::phoConvEoverP);
  tree->SetBranchAddress("phoConvMinDist", &IN::phoConvMinDist);
  tree->SetBranchAddress("phoConvdPhiAtVtx", &IN::phoConvdPhiAtVtx);
  tree->SetBranchAddress("phoConvdPhiAtCalo", &IN::phoConvdPhiAtCalo);
  tree->SetBranchAddress("phoConvdEtaAtCalo", &IN::phoConvdEtaAtCalo);
  tree->SetBranchAddress("phoConvTrkPin_x", &IN::phoConvTrkPin_x);
  tree->SetBranchAddress("phoConvTrkPin_y", &IN::phoConvTrkPin_y);
  tree->SetBranchAddress("phoConvTrkPout_x", &IN::phoConvTrkPout_x);
  tree->SetBranchAddress("phoConvTrkPout_y", &IN::phoConvTrkPout_y);
  tree->SetBranchAddress("phoConvChi2", &IN::phoConvChi2);
  tree->SetBranchAddress("phoConvChi2Prob", &IN::phoConvChi2Prob);
  tree->SetBranchAddress("phoConvNTrks", &IN::phoConvNTrks);
  tree->SetBranchAddress("phoConvVtx_x", &IN::phoConvVtx_x);
  tree->SetBranchAddress("phoConvVtx_y", &IN::phoConvVtx_y);
  tree->SetBranchAddress("phoConvVtx_z", &IN::phoConvVtx_z);
  tree->SetBranchAddress("phoConvPairMomentum_x", &IN::phoConvPairMomentum_x);
  tree->SetBranchAddress("phoConvPairMomentum_y", &IN::phoConvPairMomentum_y);
  tree->SetBranchAddress("phoConvPairMomentum_z", &IN::phoConvPairMomentum_z);
  tree->SetBranchAddress("SingleLegConv", &IN::SingleLegConv);
  tree->SetBranchAddress("nMu", &IN::nMu);
  tree->SetBranchAddress("muTrg", &IN::muTrg);
  tree->SetBranchAddress("muEta", &IN::muEta);
  tree->SetBranchAddress("muPhi", &IN::muPhi);
  tree->SetBranchAddress("muCharge", &IN::muCharge);
  tree->SetBranchAddress("muPt", &IN::muPt);
  tree->SetBranchAddress("muPz", &IN::muPz);
  tree->SetBranchAddress("muVtx_x", &IN::muVtx_x);
  tree->SetBranchAddress("muVtx_y", &IN::muVtx_y);
  tree->SetBranchAddress("muVtx_z", &IN::muVtx_z);
  tree->SetBranchAddress("muIsoTrk", &IN::muIsoTrk);
  tree->SetBranchAddress("muIsoCalo", &IN::muIsoCalo);
  tree->SetBranchAddress("muIsoEcal", &IN::muIsoEcal);
  tree->SetBranchAddress("muIsoHcal", &IN::muIsoHcal);
  tree->SetBranchAddress("muChi2NDF", &IN::muChi2NDF);
  tree->SetBranchAddress("muInnerChi2NDF", &IN::muInnerChi2NDF);
  tree->SetBranchAddress("muPFIsoR04_CH", &IN::muPFIsoR04_CH);
  tree->SetBranchAddress("muPFIsoR04_NH", &IN::muPFIsoR04_NH);
  tree->SetBranchAddress("muPFIsoR04_Pho", &IN::muPFIsoR04_Pho);
  tree->SetBranchAddress("muPFIsoR04_PU", &IN::muPFIsoR04_PU);
  tree->SetBranchAddress("muPFIsoR04_CPart", &IN::muPFIsoR04_CPart);
  tree->SetBranchAddress("muPFIsoR04_NHHT", &IN::muPFIsoR04_NHHT);
  tree->SetBranchAddress("muPFIsoR04_PhoHT", &IN::muPFIsoR04_PhoHT);
  tree->SetBranchAddress("muPFIsoR03_CH", &IN::muPFIsoR03_CH);
  tree->SetBranchAddress("muPFIsoR03_NH", &IN::muPFIsoR03_NH);
  tree->SetBranchAddress("muPFIsoR03_Pho", &IN::muPFIsoR03_Pho);
  tree->SetBranchAddress("muPFIsoR03_PU", &IN::muPFIsoR03_PU);
  tree->SetBranchAddress("muPFIsoR03_CPart", &IN::muPFIsoR03_CPart);
  tree->SetBranchAddress("muPFIsoR03_NHHT", &IN::muPFIsoR03_NHHT);
  tree->SetBranchAddress("muPFIsoR03_PhoHT", &IN::muPFIsoR03_PhoHT);
  tree->SetBranchAddress("muType", &IN::muType);
  tree->SetBranchAddress("muD0", &IN::muD0);
  tree->SetBranchAddress("muDz", &IN::muDz);
  tree->SetBranchAddress("muD0GV", &IN::muD0GV);
  tree->SetBranchAddress("muDzGV", &IN::muDzGV);
  tree->SetBranchAddress("muInnerD0", &IN::muInnerD0);
  tree->SetBranchAddress("muInnerDz", &IN::muInnerDz);
  tree->SetBranchAddress("muInnerD0GV", &IN::muInnerD0GV);
  tree->SetBranchAddress("muInnerDzGV", &IN::muInnerDzGV);
  tree->SetBranchAddress("muInnerPt", &IN::muInnerPt);
  tree->SetBranchAddress("muNumberOfValidTrkLayers", &IN::muNumberOfValidTrkLayers);
  tree->SetBranchAddress("muNumberOfValidTrkHits", &IN::muNumberOfValidTrkHits);
  tree->SetBranchAddress("muNumberOfValidPixelLayers", &IN::muNumberOfValidPixelLayers);
  tree->SetBranchAddress("muNumberOfValidPixelHits", &IN::muNumberOfValidPixelHits);
  tree->SetBranchAddress("muNumberOfValidMuonHits", &IN::muNumberOfValidMuonHits);
  tree->SetBranchAddress("muStations", &IN::muStations);
  tree->SetBranchAddress("muChambers", &IN::muChambers);
  tree->SetBranchAddress("nTau", &IN::nTau);
  tree->SetBranchAddress("rho25", &IN::rho25);
  tree->SetBranchAddress("rho25_neu", &IN::rho25_neu);
  tree->SetBranchAddress("rho25_muPFiso", &IN::rho25_muPFiso);
  tree->SetBranchAddress("rho25_elePFiso", &IN::rho25_elePFiso);
  tree->SetBranchAddress("rho2011", &IN::rho2011);
  tree->SetBranchAddress("rho2012", &IN::rho2012);
  tree->SetBranchAddress("QGTag_MLP", &IN::QGTag_MLP);
  tree->SetBranchAddress("QGTag_likelihood", &IN::QGTag_likelihood);
  tree->SetBranchAddress("nCA8Jet", &IN::nCA8Jet);
  tree->SetBranchAddress("nJet", &IN::nJet);
  tree->SetBranchAddress("jetTrg", &IN::jetTrg);
  tree->SetBranchAddress("jetEn", &IN::jetEn);
  tree->SetBranchAddress("jetPt", &IN::jetPt);
  tree->SetBranchAddress("jetEta", &IN::jetEta);
  tree->SetBranchAddress("jetPhi", &IN::jetPhi);
  tree->SetBranchAddress("jetCharge", &IN::jetCharge);
  tree->SetBranchAddress("jetEt", &IN::jetEt);
  tree->SetBranchAddress("jetRawEn", &IN::jetRawEn);
  tree->SetBranchAddress("jetCHF", &IN::jetCHF);
  tree->SetBranchAddress("jetNCH", &IN::jetNCH);
  tree->SetBranchAddress("jetNNeutrals", &IN::jetNNeutrals);
  tree->SetBranchAddress("jetNCharged", &IN::jetNCharged);
  tree->SetBranchAddress("jetLeadTrackPt", &IN::jetLeadTrackPt);
  tree->SetBranchAddress("jetVtxPt", &IN::jetVtxPt);
  tree->SetBranchAddress("nConv", &IN::nConv);
  tree->SetBranchAddress("eleD0LepVtx", &IN::eleD0LepVtx);
  tree->SetBranchAddress("eleDzLepVtx", &IN::eleDzLepVtx);
  tree->SetBranchAddress("muD0LepVtx", &IN::muD0LepVtx);
  tree->SetBranchAddress("muDzLepVtx", &IN::muDzLepVtx);
};

void InitOUTTree( TTree * tree ) {
  tree->Branch("nVtxBS", &OUT::nVtxBS, "nVtxBS/I");
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
}
void CopyInputVarsToOutput( std::string prefix) {
    CopynVtxBSInToOut( prefix ); 
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

    CopynVtxBSInToOut( prefix );
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
}; 

void CopyPrefixIndexBranchesInToOut( const std::string & prefix, unsigned index ) { 

// Just call each copy function with the prefix 

}; 

void ClearOutputPrefix ( const std::string & prefix ) {
}; 

void CopynVtxBSInToOut( std::string prefix ) { 

    std::string my_name = "nVtxBS";
    std::size_t pos = my_name.find( prefix ); 
    // if the filter is given only continue if its matched at the beginning 
    if( prefix != "" &&  pos != 0 ) return; 
  OUT::nVtxBS = IN::nVtxBS;
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

 