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
#define EXISTS_nHLT
#define EXISTS_run
#define EXISTS_event
#define EXISTS_lumis
#define EXISTS_isData
#define EXISTS_HLT
#define EXISTS_HLTIndex
#define EXISTS_bspotPos
#define EXISTS_nVtx
#define EXISTS_vtx_x
#define EXISTS_vtx_y
#define EXISTS_vtx_z
#define EXISTS_IsVtxGood
#define EXISTS_nGoodVtx
#define EXISTS_nVtxBS
#define EXISTS_vtxbs_x
#define EXISTS_vtxbs_y
#define EXISTS_vtxbs_z
#define EXISTS_vtxbsPtMod
#define EXISTS_vtxbsSumPt2
#define EXISTS_vtxbsTkIndex
#define EXISTS_vtxbsTkWeight
#define EXISTS_nTrk
#define EXISTS_trkP_x
#define EXISTS_trkP_y
#define EXISTS_trkP_z
#define EXISTS_trkVtx_x
#define EXISTS_trkVtx_y
#define EXISTS_trkVtx_z
#define EXISTS_trkd0
#define EXISTS_trkd0Err
#define EXISTS_trkdz
#define EXISTS_trkdzErr
#define EXISTS_trkPtErr
#define EXISTS_trkQuality
#define EXISTS_nGoodTrk
#define EXISTS_IsTracksGood
#define EXISTS_pfMET
#define EXISTS_pfMETPhi
#define EXISTS_pfMETsumEt
#define EXISTS_pfMETmEtSig
#define EXISTS_pfMETSig
#define EXISTS_pfType01MET
#define EXISTS_pfType01METPhi
#define EXISTS_pfType01METsumEt
#define EXISTS_pfType01METmEtSig
#define EXISTS_pfType01METSig
#define EXISTS_recoPfMET
#define EXISTS_recoPfMETPhi
#define EXISTS_recoPfMETsumEt
#define EXISTS_recoPfMETmEtSig
#define EXISTS_recoPfMETSig
#define EXISTS_trkMETxPV
#define EXISTS_trkMETyPV
#define EXISTS_trkMETPhiPV
#define EXISTS_trkMETPV
#define EXISTS_trkMETx
#define EXISTS_trkMETy
#define EXISTS_trkMETPhi
#define EXISTS_trkMET
#define EXISTS_metFilters
#define EXISTS_nEle
#define EXISTS_eleTrg
#define EXISTS_eleClass
#define EXISTS_eleIsEcalDriven
#define EXISTS_eleCharge
#define EXISTS_eleChargeConsistent
#define EXISTS_eleEn
#define EXISTS_eleEcalEn
#define EXISTS_eleSCRawEn
#define EXISTS_eleSCEn
#define EXISTS_eleESEn
#define EXISTS_elePt
#define EXISTS_eleEta
#define EXISTS_elePhi
#define EXISTS_eleR9
#define EXISTS_eleEtaVtx
#define EXISTS_elePhiVtx
#define EXISTS_eleEtVtx
#define EXISTS_eleSCEta
#define EXISTS_eleSCPhi
#define EXISTS_eleSCEtaWidth
#define EXISTS_eleSCPhiWidth
#define EXISTS_eleVtx_x
#define EXISTS_eleVtx_y
#define EXISTS_eleVtx_z
#define EXISTS_eleD0
#define EXISTS_eleDz
#define EXISTS_eleD0GV
#define EXISTS_eleDzGV
#define EXISTS_eleD0Vtx
#define EXISTS_eleDzVtx
#define EXISTS_eleHoverE
#define EXISTS_eleHoverE12
#define EXISTS_eleEoverP
#define EXISTS_elePin
#define EXISTS_elePout
#define EXISTS_eleTrkMomErr
#define EXISTS_eleBrem
#define EXISTS_eledEtaAtVtx
#define EXISTS_eledPhiAtVtx
#define EXISTS_eleSigmaIEtaIEta
#define EXISTS_eleSigmaIEtaIPhi
#define EXISTS_eleSigmaIPhiIPhi
#define EXISTS_eleEmax
#define EXISTS_eleE2ndMax
#define EXISTS_eleETop
#define EXISTS_eleEBottom
#define EXISTS_eleELeft
#define EXISTS_eleERight
#define EXISTS_eleE1x5
#define EXISTS_eleE3x3
#define EXISTS_eleE5x5
#define EXISTS_eleE2x5Max
#define EXISTS_eleE2x5Top
#define EXISTS_eleE2x5Bottom
#define EXISTS_eleE2x5Left
#define EXISTS_eleE2x5Right
#define EXISTS_eleSeedEta
#define EXISTS_eleSeedE
#define EXISTS_eleSeedPhi
#define EXISTS_eleCrysEta
#define EXISTS_eleCrysPhi
#define EXISTS_eleCrysIEta
#define EXISTS_eleCrysIPhi
#define EXISTS_eleRegrE
#define EXISTS_eleRegrEerr
#define EXISTS_elePhoRegrE
#define EXISTS_elePhoRegrEerr
#define EXISTS_eleSeedTime
#define EXISTS_eleGSFPt
#define EXISTS_eleGSFEta
#define EXISTS_eleGSFPhi
#define EXISTS_eleGSFCharge
#define EXISTS_eleGSFChi2NDF
#define EXISTS_eleRecoFlag
#define EXISTS_elePos
#define EXISTS_eleIsoTrkDR03
#define EXISTS_eleIsoEcalDR03
#define EXISTS_eleIsoHcalDR03
#define EXISTS_eleIsoHcalDR0312
#define EXISTS_eleIsoTrkDR04
#define EXISTS_eleIsoEcalDR04
#define EXISTS_eleIsoHcalDR04
#define EXISTS_eleIsoHcalDR0412
#define EXISTS_eleModIsoTrk
#define EXISTS_eleModIsoEcal
#define EXISTS_eleModIsoHcal
#define EXISTS_eleMissHits
#define EXISTS_eleConvDist
#define EXISTS_eleConvDcot
#define EXISTS_eleConvVtxFit
#define EXISTS_eleIP3D
#define EXISTS_eleIP3DErr
#define EXISTS_eleIDMVANonTrig
#define EXISTS_eleIDMVATrig
#define EXISTS_elePFChIso03
#define EXISTS_elePFPhoIso03
#define EXISTS_elePFNeuIso03
#define EXISTS_elePFChIso04
#define EXISTS_elePFPhoIso04
#define EXISTS_elePFNeuIso04
#define EXISTS_eleESEffSigmaRR_x
#define EXISTS_eleESEffSigmaRR_y
#define EXISTS_eleESEffSigmaRR_z
#define EXISTS_nPho
#define EXISTS_phoTrg
#define EXISTS_phoTrgFilter
#define EXISTS_phoIsPhoton
#define EXISTS_phoSCPos_x
#define EXISTS_phoSCPos_y
#define EXISTS_phoSCPos_z
#define EXISTS_phoCaloPos_x
#define EXISTS_phoCaloPos_y
#define EXISTS_phoCaloPos_z
#define EXISTS_phoE
#define EXISTS_phoEt
#define EXISTS_phoEta
#define EXISTS_phoVtx_x
#define EXISTS_phoVtx_y
#define EXISTS_phoVtx_z
#define EXISTS_phoPhi
#define EXISTS_phoEtVtx
#define EXISTS_phoEtaVtx
#define EXISTS_phoPhiVtx
#define EXISTS_phoR9
#define EXISTS_phoNClus
#define EXISTS_phoTrkIsoHollowDR03
#define EXISTS_phoEcalIsoDR03
#define EXISTS_phoHcalIsoDR03
#define EXISTS_phoHcalIsoDR0312
#define EXISTS_phoTrkIsoHollowDR04
#define EXISTS_phoCiCdRtoTrk
#define EXISTS_phoEcalIsoDR04
#define EXISTS_phoHcalIsoDR04
#define EXISTS_phoHcalIsoDR0412
#define EXISTS_phoHoverE
#define EXISTS_phoHoverE12
#define EXISTS_phoEleVeto
#define EXISTS_phoSigmaIEtaIEta
#define EXISTS_phoSigmaIEtaIPhi
#define EXISTS_phoSigmaIPhiIPhi
#define EXISTS_phoCiCPF4phopfIso03
#define EXISTS_phoCiCPF4phopfIso04
#define EXISTS_phoCiCPF4chgpfIso02
#define EXISTS_phoCiCPF4chgpfIso03
#define EXISTS_phoCiCPF4chgpfIso04
#define EXISTS_phoEmax
#define EXISTS_phoETop
#define EXISTS_phoEBottom
#define EXISTS_phoELeft
#define EXISTS_phoERight
#define EXISTS_phoE2ndMax
#define EXISTS_phoE3x3
#define EXISTS_phoE3x1
#define EXISTS_phoE1x3
#define EXISTS_phoE5x5
#define EXISTS_phoE1x5
#define EXISTS_phoE2x2
#define EXISTS_phoE2x5Max
#define EXISTS_phoE2x5Top
#define EXISTS_phoE2x5Bottom
#define EXISTS_phoE2x5Left
#define EXISTS_phoE2x5Right
#define EXISTS_phoSeedE
#define EXISTS_phoSeedEta
#define EXISTS_phoSeedPhi
#define EXISTS_phoCrysEta
#define EXISTS_phoCrysPhi
#define EXISTS_phoCrysIEta
#define EXISTS_phoCrysIPhi
#define EXISTS_phoPFChIso
#define EXISTS_phoPFPhoIso
#define EXISTS_phoPFNeuIso
#define EXISTS_phoSCRChIso
#define EXISTS_phoSCRPhoIso
#define EXISTS_phoSCRNeuIso
#define EXISTS_phoSCRChIso04
#define EXISTS_phoSCRPhoIso04
#define EXISTS_phoSCRNeuIso04
#define EXISTS_phoRandConeChIso
#define EXISTS_phoRandConePhoIso
#define EXISTS_phoRandConeNeuIso
#define EXISTS_phoRandConeChIso04
#define EXISTS_phoRandConePhoIso04
#define EXISTS_phoRandConeNeuIso04
#define EXISTS_phoRegrE
#define EXISTS_phoRegrEerr
#define EXISTS_phoSeedTime
#define EXISTS_phoSeedDetId1
#define EXISTS_phoSeedDetId2
#define EXISTS_phoLICTD
#define EXISTS_phoRecoFlag
#define EXISTS_phoPos
#define EXISTS_phoSCE
#define EXISTS_phoSCRawE
#define EXISTS_phoESEn
#define EXISTS_phoSCEt
#define EXISTS_phoSCEta
#define EXISTS_phoSCPhi
#define EXISTS_phoSCEtaWidth
#define EXISTS_phoSCPhiWidth
#define EXISTS_phoSCBrem
#define EXISTS_phoOverlap
#define EXISTS_phohasPixelSeed
#define EXISTS_pho_hasConvPf
#define EXISTS_pho_hasSLConvPf
#define EXISTS_pho_pfconvVtxZ
#define EXISTS_pho_pfconvVtxZErr
#define EXISTS_pho_nSLConv
#define EXISTS_pho_pfSLConvPos_x
#define EXISTS_pho_pfSLConvPos_y
#define EXISTS_pho_pfSLConvPos_z
#define EXISTS_pho_pfSLConvVtxZ
#define EXISTS_phoIsConv
#define EXISTS_phoNConv
#define EXISTS_phoConvInvMass
#define EXISTS_phoConvCotTheta
#define EXISTS_phoConvEoverP
#define EXISTS_phoConvZofPVfromTrks
#define EXISTS_phoConvMinDist
#define EXISTS_phoConvdPhiAtVtx
#define EXISTS_phoConvdPhiAtCalo
#define EXISTS_phoConvdEtaAtCalo
#define EXISTS_phoConvTrkd0_x
#define EXISTS_phoConvTrkd0_y
#define EXISTS_phoConvTrkPin_x
#define EXISTS_phoConvTrkPin_y
#define EXISTS_phoConvTrkPout_x
#define EXISTS_phoConvTrkPout_y
#define EXISTS_phoConvTrkdz_x
#define EXISTS_phoConvTrkdz_y
#define EXISTS_phoConvTrkdzErr_x
#define EXISTS_phoConvTrkdzErr_y
#define EXISTS_phoConvChi2
#define EXISTS_phoConvChi2Prob
#define EXISTS_phoConvNTrks
#define EXISTS_phoConvCharge1
#define EXISTS_phoConvCharge2
#define EXISTS_phoConvValidVtx
#define EXISTS_phoConvLikeLihood
#define EXISTS_phoConvP4_0
#define EXISTS_phoConvP4_1
#define EXISTS_phoConvP4_2
#define EXISTS_phoConvP4_3
#define EXISTS_phoConvVtx_x
#define EXISTS_phoConvVtx_y
#define EXISTS_phoConvVtx_z
#define EXISTS_phoConvVtxErr_x
#define EXISTS_phoConvVtxErr_y
#define EXISTS_phoConvVtxErr_z
#define EXISTS_phoConvPairMomentum_x
#define EXISTS_phoConvPairMomentum_y
#define EXISTS_phoConvPairMomentum_z
#define EXISTS_phoConvRefittedMomentum_x
#define EXISTS_phoConvRefittedMomentum_y
#define EXISTS_phoConvRefittedMomentum_z
#define EXISTS_SingleLegConv
#define EXISTS_phoPFConvVtx_x
#define EXISTS_phoPFConvVtx_y
#define EXISTS_phoPFConvVtx_z
#define EXISTS_phoPFConvMom_x
#define EXISTS_phoPFConvMom_y
#define EXISTS_phoPFConvMom_z
#define EXISTS_phoESEffSigmaRR_x
#define EXISTS_phoESEffSigmaRR_y
#define EXISTS_phoESEffSigmaRR_z
#define EXISTS_nMu
#define EXISTS_muTrg
#define EXISTS_muEta
#define EXISTS_muPhi
#define EXISTS_muCharge
#define EXISTS_muPt
#define EXISTS_muPz
#define EXISTS_muVtx_x
#define EXISTS_muVtx_y
#define EXISTS_muVtx_z
#define EXISTS_muVtxGlb_x
#define EXISTS_muVtxGlb_y
#define EXISTS_muVtxGlb_z
#define EXISTS_mucktPt
#define EXISTS_mucktPtErr
#define EXISTS_mucktEta
#define EXISTS_mucktPhi
#define EXISTS_mucktdxy
#define EXISTS_mucktdz
#define EXISTS_muIsoTrk
#define EXISTS_muIsoCalo
#define EXISTS_muIsoEcal
#define EXISTS_muIsoHcal
#define EXISTS_muChi2NDF
#define EXISTS_muInnerChi2NDF
#define EXISTS_muPFIsoR04_CH
#define EXISTS_muPFIsoR04_NH
#define EXISTS_muPFIsoR04_Pho
#define EXISTS_muPFIsoR04_PU
#define EXISTS_muPFIsoR04_CPart
#define EXISTS_muPFIsoR04_NHHT
#define EXISTS_muPFIsoR04_PhoHT
#define EXISTS_muPFIsoR03_CH
#define EXISTS_muPFIsoR03_NH
#define EXISTS_muPFIsoR03_Pho
#define EXISTS_muPFIsoR03_PU
#define EXISTS_muPFIsoR03_CPart
#define EXISTS_muPFIsoR03_NHHT
#define EXISTS_muPFIsoR03_PhoHT
#define EXISTS_muType
#define EXISTS_muD0
#define EXISTS_muDz
#define EXISTS_muD0GV
#define EXISTS_muDzGV
#define EXISTS_muD0Vtx
#define EXISTS_muDzVtx
#define EXISTS_muInnerD0
#define EXISTS_muInnerDz
#define EXISTS_muInnerD0GV
#define EXISTS_muInnerDzGV
#define EXISTS_muInnerPt
#define EXISTS_muInnerPtErr
#define EXISTS_muNumberOfValidTrkLayers
#define EXISTS_muNumberOfValidTrkHits
#define EXISTS_muNumberOfValidPixelLayers
#define EXISTS_muNumberOfValidPixelHits
#define EXISTS_muNumberOfValidMuonHits
#define EXISTS_muStations
#define EXISTS_muChambers
#define EXISTS_muIP3D
#define EXISTS_muIP3DErr
#define EXISTS_nTau
#define EXISTS_tauDecayModeFinding
#define EXISTS_tauAgainstElectronLooseMVA3
#define EXISTS_tauAgainstElectronMediumMVA3
#define EXISTS_tauAgainstElectronTightMVA3
#define EXISTS_tauAgainstElectronVTightMVA3
#define EXISTS_tauAgainstElectronDeadECAL
#define EXISTS_tauAgainstMuonLoose2
#define EXISTS_tauAgainstMuonMedium2
#define EXISTS_tauAgainstMuonTight2
#define EXISTS_tauCombinedIsolationDeltaBetaCorrRaw3Hits
#define EXISTS_tauLooseCombinedIsolationDeltaBetaCorr3Hits
#define EXISTS_tauMediumCombinedIsolationDeltaBetaCorr3Hits
#define EXISTS_tauTightCombinedIsolationDeltaBetaCorr3Hits
#define EXISTS_tauEta
#define EXISTS_tauPhi
#define EXISTS_tauPt
#define EXISTS_tauEt
#define EXISTS_tauCharge
#define EXISTS_tauDecayMode
#define EXISTS_tauEMFraction
#define EXISTS_tauHCAL3x3OverPLead
#define EXISTS_tauHCALMaxOverPLead
#define EXISTS_tauHCALTotOverPLead
#define EXISTS_tauIsolationPFChargedHadrCandsPtSum
#define EXISTS_tauIsolationPFGammaCandsEtSum
#define EXISTS_tauLeadPFChargedHadrCandsignedSipt
#define EXISTS_tauLeadChargedHadronExists
#define EXISTS_tauLeadChargedHadronEta
#define EXISTS_tauLeadChargedHadronPhi
#define EXISTS_tauLeadChargedHadronPt
#define EXISTS_rho25
#define EXISTS_rho25_neu
#define EXISTS_rho25_muPFiso
#define EXISTS_rho25_elePFiso
#define EXISTS_rho2011
#define EXISTS_rho2012
#define EXISTS_QGTag_MLP
#define EXISTS_QGTag_likelihood
#define EXISTS_nCA8Jet
#define EXISTS_CA8JetPt
#define EXISTS_CA8JetEta
#define EXISTS_CA8JetPhi
#define EXISTS_CA8JetMass
#define EXISTS_CA8JetArea
#define EXISTS_CA8Jet_tau1
#define EXISTS_CA8Jet_tau2
#define EXISTS_CA8Jet_tau3
#define EXISTS_CA8JetCHF
#define EXISTS_CA8JetNHF
#define EXISTS_CA8JetCEF
#define EXISTS_CA8JetNEF
#define EXISTS_CA8JetNCH
#define EXISTS_CA8Jetnconstituents
#define EXISTS_CA8prunedJetMass
#define EXISTS_CA8prunedJet_nSubJets
#define EXISTS_CA8prunedJet_SubjetPt
#define EXISTS_CA8prunedJet_SubjetEta
#define EXISTS_CA8prunedJet_SubjetPhi
#define EXISTS_CA8prunedJet_SubjetMass
#define EXISTS_nJet
#define EXISTS_jetTrg
#define EXISTS_jetEn
#define EXISTS_jetPt
#define EXISTS_jetEta
#define EXISTS_jetPhi
#define EXISTS_jetCharge
#define EXISTS_jetEt
#define EXISTS_jetRawPt
#define EXISTS_jetRawEn
#define EXISTS_jetArea
#define EXISTS_jetCHF
#define EXISTS_jetNHF
#define EXISTS_jetCEF
#define EXISTS_jetNEF
#define EXISTS_jetNCH
#define EXISTS_jetHFHAE
#define EXISTS_jetHFEME
#define EXISTS_jetNConstituents
#define EXISTS_jetCombinedSecondaryVtxBJetTags
#define EXISTS_jetCombinedSecondaryVtxMVABJetTags
#define EXISTS_jetJetProbabilityBJetTags
#define EXISTS_jetJetBProbabilityBJetTags
#define EXISTS_jetBetaStar
#define EXISTS_jetPFLooseId
#define EXISTS_jetDRMean
#define EXISTS_jetDR2Mean
#define EXISTS_jetDZ
#define EXISTS_jetFrac01
#define EXISTS_jetFrac02
#define EXISTS_jetFrac03
#define EXISTS_jetFrac04
#define EXISTS_jetFrac05
#define EXISTS_jetFrac06
#define EXISTS_jetFrac07
#define EXISTS_jetBeta
#define EXISTS_jetBetaStarCMG
#define EXISTS_jetBetaStarClassic
#define EXISTS_jetBetaExt
#define EXISTS_jetBetaStarCMGExt
#define EXISTS_jetBetaStarClassicExt
#define EXISTS_jetNNeutrals
#define EXISTS_jetNCharged
#define EXISTS_jetMVAs
#define EXISTS_jetWPLevels
#define EXISTS_jetMVAsExt_simple
#define EXISTS_jetWPLevelsExt_simple
#define EXISTS_jetMVAsExt_full
#define EXISTS_jetWPLevelsExt_full
#define EXISTS_jetMVAsExt_cutBased
#define EXISTS_jetWPLevelsExt_cutBased
#define EXISTS_jetMVAsExt_philv1
#define EXISTS_jetWPLevelsExt_philv1
#define EXISTS_jetMt
#define EXISTS_jetJECUnc
#define EXISTS_jetLeadTrackPt
#define EXISTS_jetVtxPt
#define EXISTS_jetVtxMass
#define EXISTS_jetVtx3dL
#define EXISTS_jetVtx3deL
#define EXISTS_jetSoftLeptPt
#define EXISTS_jetSoftLeptPtRel
#define EXISTS_jetSoftLeptdR
#define EXISTS_jetSoftLeptIdlooseMu
#define EXISTS_jetSoftLeptIdEle95
#define EXISTS_jetDPhiMETJet
#define EXISTS_jetPuJetIdL
#define EXISTS_jetPuJetIdM
#define EXISTS_jetPuJetIdT
#define EXISTS_nLowPtJet
#define EXISTS_jetLowPtEn
#define EXISTS_jetLowPtPt
#define EXISTS_jetLowPtEta
#define EXISTS_jetLowPtPhi
#define EXISTS_jetLowPtCharge
#define EXISTS_jetLowPtEt
#define EXISTS_jetLowPtRawPt
#define EXISTS_jetLowPtRawEn
#define EXISTS_jetLowPtArea
#define EXISTS_nConv
#define EXISTS_convP4_x
#define EXISTS_convP4_y
#define EXISTS_convP4_z
#define EXISTS_convP4_E
#define EXISTS_convVtx_x
#define EXISTS_convVtx_y
#define EXISTS_convVtx_z
#define EXISTS_convVtxErr_x
#define EXISTS_convVtxErr_y
#define EXISTS_convVtxErr_z
#define EXISTS_convPairMomentum_x
#define EXISTS_convPairMomentum_y
#define EXISTS_convPairMomentum_z
#define EXISTS_convRefittedMomentum_x
#define EXISTS_convRefittedMomentum_y
#define EXISTS_convRefittedMomentum_z
#define EXISTS_convNTracks
#define EXISTS_convPairInvMass
#define EXISTS_convPairCotThetaSep
#define EXISTS_convEoverP
#define EXISTS_convDistOfMinApproach
#define EXISTS_convDPhiTrksAtVtx
#define EXISTS_convDPhiTrksAtEcal
#define EXISTS_convDEtaTrksAtEcal
#define EXISTS_convDxy
#define EXISTS_convDz
#define EXISTS_convLxy
#define EXISTS_convLz
#define EXISTS_convZofPrimVtxFromTrks
#define EXISTS_convNHitsBeforeVtx_0
#define EXISTS_convNHitsBeforeVtx_1
#define EXISTS_convNSharedHits
#define EXISTS_convValidVtx
#define EXISTS_convMVALikelihood
#define EXISTS_convChi2
#define EXISTS_convChi2Probability
#define EXISTS_convTk1Dz
#define EXISTS_convTk2Dz
#define EXISTS_convTk1DzErr
#define EXISTS_convTk2DzErr
#define EXISTS_convCh1Ch2
#define EXISTS_convTk1D0
#define EXISTS_convTk1Pout
#define EXISTS_convTk1Pin
#define EXISTS_convTk2D0
#define EXISTS_convTk2Pout
#define EXISTS_convTk2Pin
//Define variables as extern below and declare them in the .cxx file to avoid multiple definitions
namespace IN {
 extern Int_t				nHLT;
 extern Int_t				run;
 extern Long64_t				event;
 extern Int_t				lumis;
 extern Bool_t				isData;
 extern Int_t				HLT[453];
 extern Int_t				HLTIndex[70];
 extern Float_t				bspotPos[3];
 extern Int_t				nVtx;
 extern std::vector<float>				*vtx_x;
 extern std::vector<float>				*vtx_y;
 extern std::vector<float>				*vtx_z;
 extern Int_t				IsVtxGood;
 extern Int_t				nGoodVtx;
 extern Int_t				nVtxBS;
 extern std::vector<float>				*vtxbs_x;
 extern std::vector<float>				*vtxbs_y;
 extern std::vector<float>				*vtxbs_z;
 extern std::vector<float>				*vtxbsPtMod;
 extern std::vector<float>				*vtxbsSumPt2;
 extern std::vector<std::vector<int> >				*vtxbsTkIndex;
 extern std::vector<std::vector<float> >				*vtxbsTkWeight;
 extern Int_t				nTrk;
 extern std::vector<float>				*trkP_x;
 extern std::vector<float>				*trkP_y;
 extern std::vector<float>				*trkP_z;
 extern std::vector<float>				*trkVtx_x;
 extern std::vector<float>				*trkVtx_y;
 extern std::vector<float>				*trkVtx_z;
 extern std::vector<float>				*trkd0;
 extern std::vector<float>				*trkd0Err;
 extern std::vector<float>				*trkdz;
 extern std::vector<float>				*trkdzErr;
 extern std::vector<float>				*trkPtErr;
 extern std::vector<int>				*trkQuality;
 extern Int_t				nGoodTrk;
 extern Int_t				IsTracksGood;
 extern Float_t				pfMET;
 extern Float_t				pfMETPhi;
 extern Float_t				pfMETsumEt;
 extern Float_t				pfMETmEtSig;
 extern Float_t				pfMETSig;
 extern Float_t				pfType01MET;
 extern Float_t				pfType01METPhi;
 extern Float_t				pfType01METsumEt;
 extern Float_t				pfType01METmEtSig;
 extern Float_t				pfType01METSig;
 extern Float_t				recoPfMET;
 extern Float_t				recoPfMETPhi;
 extern Float_t				recoPfMETsumEt;
 extern Float_t				recoPfMETmEtSig;
 extern Float_t				recoPfMETSig;
 extern Float_t				trkMETxPV;
 extern Float_t				trkMETyPV;
 extern Float_t				trkMETPhiPV;
 extern Float_t				trkMETPV;
 extern std::vector<float>				*trkMETx;
 extern std::vector<float>				*trkMETy;
 extern std::vector<float>				*trkMETPhi;
 extern std::vector<float>				*trkMET;
 extern Int_t				metFilters[10];
 extern Int_t				nEle;
 extern std::vector<unsigned long>				*eleTrg;
 extern std::vector<int>				*eleClass;
 extern std::vector<int>				*eleIsEcalDriven;
 extern std::vector<int>				*eleCharge;
 extern std::vector<int>				*eleChargeConsistent;
 extern std::vector<float>				*eleEn;
 extern std::vector<float>				*eleEcalEn;
 extern std::vector<float>				*eleSCRawEn;
 extern std::vector<float>				*eleSCEn;
 extern std::vector<float>				*eleESEn;
 extern std::vector<float>				*elePt;
 extern std::vector<float>				*eleEta;
 extern std::vector<float>				*elePhi;
 extern std::vector<float>				*eleR9;
 extern std::vector<std::vector<float> >				*eleEtaVtx;
 extern std::vector<std::vector<float> >				*elePhiVtx;
 extern std::vector<std::vector<float> >				*eleEtVtx;
 extern std::vector<float>				*eleSCEta;
 extern std::vector<float>				*eleSCPhi;
 extern std::vector<float>				*eleSCEtaWidth;
 extern std::vector<float>				*eleSCPhiWidth;
 extern std::vector<float>				*eleVtx_x;
 extern std::vector<float>				*eleVtx_y;
 extern std::vector<float>				*eleVtx_z;
 extern std::vector<float>				*eleD0;
 extern std::vector<float>				*eleDz;
 extern std::vector<float>				*eleD0GV;
 extern std::vector<float>				*eleDzGV;
 extern std::vector<std::vector<float> >				*eleD0Vtx;
 extern std::vector<std::vector<float> >				*eleDzVtx;
 extern std::vector<float>				*eleHoverE;
 extern std::vector<float>				*eleHoverE12;
 extern std::vector<float>				*eleEoverP;
 extern std::vector<float>				*elePin;
 extern std::vector<float>				*elePout;
 extern std::vector<float>				*eleTrkMomErr;
 extern std::vector<float>				*eleBrem;
 extern std::vector<float>				*eledEtaAtVtx;
 extern std::vector<float>				*eledPhiAtVtx;
 extern std::vector<float>				*eleSigmaIEtaIEta;
 extern std::vector<float>				*eleSigmaIEtaIPhi;
 extern std::vector<float>				*eleSigmaIPhiIPhi;
 extern std::vector<float>				*eleEmax;
 extern std::vector<float>				*eleE2ndMax;
 extern std::vector<float>				*eleETop;
 extern std::vector<float>				*eleEBottom;
 extern std::vector<float>				*eleELeft;
 extern std::vector<float>				*eleERight;
 extern std::vector<float>				*eleE1x5;
 extern std::vector<float>				*eleE3x3;
 extern std::vector<float>				*eleE5x5;
 extern std::vector<float>				*eleE2x5Max;
 extern std::vector<float>				*eleE2x5Top;
 extern std::vector<float>				*eleE2x5Bottom;
 extern std::vector<float>				*eleE2x5Left;
 extern std::vector<float>				*eleE2x5Right;
 extern std::vector<float>				*eleSeedEta;
 extern std::vector<float>				*eleSeedE;
 extern std::vector<float>				*eleSeedPhi;
 extern std::vector<float>				*eleCrysEta;
 extern std::vector<float>				*eleCrysPhi;
 extern std::vector<int>				*eleCrysIEta;
 extern std::vector<int>				*eleCrysIPhi;
 extern std::vector<float>				*eleRegrE;
 extern std::vector<float>				*eleRegrEerr;
 extern std::vector<float>				*elePhoRegrE;
 extern std::vector<float>				*elePhoRegrEerr;
 extern std::vector<float>				*eleSeedTime;
 extern std::vector<std::vector<float> >				*eleGSFPt;
 extern std::vector<std::vector<float> >				*eleGSFEta;
 extern std::vector<std::vector<float> >				*eleGSFPhi;
 extern std::vector<std::vector<float> >				*eleGSFCharge;
 extern std::vector<std::vector<float> >				*eleGSFChi2NDF;
 extern std::vector<int>				*eleRecoFlag;
 extern std::vector<int>				*elePos;
 extern std::vector<float>				*eleIsoTrkDR03;
 extern std::vector<float>				*eleIsoEcalDR03;
 extern std::vector<float>				*eleIsoHcalDR03;
 extern std::vector<float>				*eleIsoHcalDR0312;
 extern std::vector<float>				*eleIsoTrkDR04;
 extern std::vector<float>				*eleIsoEcalDR04;
 extern std::vector<float>				*eleIsoHcalDR04;
 extern std::vector<float>				*eleIsoHcalDR0412;
 extern std::vector<float>				*eleModIsoTrk;
 extern std::vector<float>				*eleModIsoEcal;
 extern std::vector<float>				*eleModIsoHcal;
 extern std::vector<int>				*eleMissHits;
 extern std::vector<float>				*eleConvDist;
 extern std::vector<float>				*eleConvDcot;
 extern std::vector<int>				*eleConvVtxFit;
 extern std::vector<float>				*eleIP3D;
 extern std::vector<float>				*eleIP3DErr;
 extern std::vector<float>				*eleIDMVANonTrig;
 extern std::vector<float>				*eleIDMVATrig;
 extern std::vector<float>				*elePFChIso03;
 extern std::vector<float>				*elePFPhoIso03;
 extern std::vector<float>				*elePFNeuIso03;
 extern std::vector<float>				*elePFChIso04;
 extern std::vector<float>				*elePFPhoIso04;
 extern std::vector<float>				*elePFNeuIso04;
 extern std::vector<float>				*eleESEffSigmaRR_x;
 extern std::vector<float>				*eleESEffSigmaRR_y;
 extern std::vector<float>				*eleESEffSigmaRR_z;
 extern Int_t				nPho;
 extern std::vector<unsigned long>				*phoTrg;
 extern std::vector<unsigned long>				*phoTrgFilter;
 extern std::vector<bool>				*phoIsPhoton;
 extern std::vector<float>				*phoSCPos_x;
 extern std::vector<float>				*phoSCPos_y;
 extern std::vector<float>				*phoSCPos_z;
 extern std::vector<float>				*phoCaloPos_x;
 extern std::vector<float>				*phoCaloPos_y;
 extern std::vector<float>				*phoCaloPos_z;
 extern std::vector<float>				*phoE;
 extern std::vector<float>				*phoEt;
 extern std::vector<float>				*phoEta;
 extern std::vector<float>				*phoVtx_x;
 extern std::vector<float>				*phoVtx_y;
 extern std::vector<float>				*phoVtx_z;
 extern std::vector<float>				*phoPhi;
 extern std::vector<std::vector<float> >				*phoEtVtx;
 extern std::vector<std::vector<float> >				*phoEtaVtx;
 extern std::vector<std::vector<float> >				*phoPhiVtx;
 extern std::vector<float>				*phoR9;
 extern std::vector<int>				*phoNClus;
 extern std::vector<float>				*phoTrkIsoHollowDR03;
 extern std::vector<float>				*phoEcalIsoDR03;
 extern std::vector<float>				*phoHcalIsoDR03;
 extern std::vector<float>				*phoHcalIsoDR0312;
 extern std::vector<float>				*phoTrkIsoHollowDR04;
 extern std::vector<float>				*phoCiCdRtoTrk;
 extern std::vector<float>				*phoEcalIsoDR04;
 extern std::vector<float>				*phoHcalIsoDR04;
 extern std::vector<float>				*phoHcalIsoDR0412;
 extern std::vector<float>				*phoHoverE;
 extern std::vector<float>				*phoHoverE12;
 extern std::vector<int>				*phoEleVeto;
 extern std::vector<float>				*phoSigmaIEtaIEta;
 extern std::vector<float>				*phoSigmaIEtaIPhi;
 extern std::vector<float>				*phoSigmaIPhiIPhi;
 extern std::vector<float>				*phoCiCPF4phopfIso03;
 extern std::vector<float>				*phoCiCPF4phopfIso04;
 extern std::vector<std::vector<float> >				*phoCiCPF4chgpfIso02;
 extern std::vector<std::vector<float> >				*phoCiCPF4chgpfIso03;
 extern std::vector<std::vector<float> >				*phoCiCPF4chgpfIso04;
 extern std::vector<float>				*phoEmax;
 extern std::vector<float>				*phoETop;
 extern std::vector<float>				*phoEBottom;
 extern std::vector<float>				*phoELeft;
 extern std::vector<float>				*phoERight;
 extern std::vector<float>				*phoE2ndMax;
 extern std::vector<float>				*phoE3x3;
 extern std::vector<float>				*phoE3x1;
 extern std::vector<float>				*phoE1x3;
 extern std::vector<float>				*phoE5x5;
 extern std::vector<float>				*phoE1x5;
 extern std::vector<float>				*phoE2x2;
 extern std::vector<float>				*phoE2x5Max;
 extern std::vector<float>				*phoE2x5Top;
 extern std::vector<float>				*phoE2x5Bottom;
 extern std::vector<float>				*phoE2x5Left;
 extern std::vector<float>				*phoE2x5Right;
 extern std::vector<float>				*phoSeedE;
 extern std::vector<float>				*phoSeedEta;
 extern std::vector<float>				*phoSeedPhi;
 extern std::vector<float>				*phoCrysEta;
 extern std::vector<float>				*phoCrysPhi;
 extern std::vector<int>				*phoCrysIEta;
 extern std::vector<int>				*phoCrysIPhi;
 extern std::vector<float>				*phoPFChIso;
 extern std::vector<float>				*phoPFPhoIso;
 extern std::vector<float>				*phoPFNeuIso;
 extern std::vector<float>				*phoSCRChIso;
 extern std::vector<float>				*phoSCRPhoIso;
 extern std::vector<float>				*phoSCRNeuIso;
 extern std::vector<float>				*phoSCRChIso04;
 extern std::vector<float>				*phoSCRPhoIso04;
 extern std::vector<float>				*phoSCRNeuIso04;
 extern std::vector<float>				*phoRandConeChIso;
 extern std::vector<float>				*phoRandConePhoIso;
 extern std::vector<float>				*phoRandConeNeuIso;
 extern std::vector<float>				*phoRandConeChIso04;
 extern std::vector<float>				*phoRandConePhoIso04;
 extern std::vector<float>				*phoRandConeNeuIso04;
 extern std::vector<float>				*phoRegrE;
 extern std::vector<float>				*phoRegrEerr;
 extern std::vector<float>				*phoSeedTime;
 extern std::vector<int>				*phoSeedDetId1;
 extern std::vector<int>				*phoSeedDetId2;
 extern std::vector<float>				*phoLICTD;
 extern std::vector<int>				*phoRecoFlag;
 extern std::vector<int>				*phoPos;
 extern std::vector<float>				*phoSCE;
 extern std::vector<float>				*phoSCRawE;
 extern std::vector<float>				*phoESEn;
 extern std::vector<float>				*phoSCEt;
 extern std::vector<float>				*phoSCEta;
 extern std::vector<float>				*phoSCPhi;
 extern std::vector<float>				*phoSCEtaWidth;
 extern std::vector<float>				*phoSCPhiWidth;
 extern std::vector<float>				*phoSCBrem;
 extern std::vector<int>				*phoOverlap;
 extern std::vector<int>				*phohasPixelSeed;
 extern std::vector<int>				*pho_hasConvPf;
 extern std::vector<int>				*pho_hasSLConvPf;
 extern std::vector<float>				*pho_pfconvVtxZ;
 extern std::vector<float>				*pho_pfconvVtxZErr;
 extern std::vector<int>				*pho_nSLConv;
 extern std::vector<std::vector<float> >				*pho_pfSLConvPos_x;
 extern std::vector<std::vector<float> >				*pho_pfSLConvPos_y;
 extern std::vector<std::vector<float> >				*pho_pfSLConvPos_z;
 extern std::vector<std::vector<float> >				*pho_pfSLConvVtxZ;
 extern std::vector<int>				*phoIsConv;
 extern std::vector<int>				*phoNConv;
 extern std::vector<float>				*phoConvInvMass;
 extern std::vector<float>				*phoConvCotTheta;
 extern std::vector<float>				*phoConvEoverP;
 extern std::vector<float>				*phoConvZofPVfromTrks;
 extern std::vector<float>				*phoConvMinDist;
 extern std::vector<float>				*phoConvdPhiAtVtx;
 extern std::vector<float>				*phoConvdPhiAtCalo;
 extern std::vector<float>				*phoConvdEtaAtCalo;
 extern std::vector<float>				*phoConvTrkd0_x;
 extern std::vector<float>				*phoConvTrkd0_y;
 extern std::vector<float>				*phoConvTrkPin_x;
 extern std::vector<float>				*phoConvTrkPin_y;
 extern std::vector<float>				*phoConvTrkPout_x;
 extern std::vector<float>				*phoConvTrkPout_y;
 extern std::vector<float>				*phoConvTrkdz_x;
 extern std::vector<float>				*phoConvTrkdz_y;
 extern std::vector<float>				*phoConvTrkdzErr_x;
 extern std::vector<float>				*phoConvTrkdzErr_y;
 extern std::vector<float>				*phoConvChi2;
 extern std::vector<float>				*phoConvChi2Prob;
 extern std::vector<int>				*phoConvNTrks;
 extern std::vector<float>				*phoConvCharge1;
 extern std::vector<float>				*phoConvCharge2;
 extern std::vector<int>				*phoConvValidVtx;
 extern std::vector<float>				*phoConvLikeLihood;
 extern std::vector<float>				*phoConvP4_0;
 extern std::vector<float>				*phoConvP4_1;
 extern std::vector<float>				*phoConvP4_2;
 extern std::vector<float>				*phoConvP4_3;
 extern std::vector<float>				*phoConvVtx_x;
 extern std::vector<float>				*phoConvVtx_y;
 extern std::vector<float>				*phoConvVtx_z;
 extern std::vector<float>				*phoConvVtxErr_x;
 extern std::vector<float>				*phoConvVtxErr_y;
 extern std::vector<float>				*phoConvVtxErr_z;
 extern std::vector<float>				*phoConvPairMomentum_x;
 extern std::vector<float>				*phoConvPairMomentum_y;
 extern std::vector<float>				*phoConvPairMomentum_z;
 extern std::vector<float>				*phoConvRefittedMomentum_x;
 extern std::vector<float>				*phoConvRefittedMomentum_y;
 extern std::vector<float>				*phoConvRefittedMomentum_z;
 extern std::vector<int>				*SingleLegConv;
 extern std::vector<std::vector<float> >				*phoPFConvVtx_x;
 extern std::vector<std::vector<float> >				*phoPFConvVtx_y;
 extern std::vector<std::vector<float> >				*phoPFConvVtx_z;
 extern std::vector<std::vector<float> >				*phoPFConvMom_x;
 extern std::vector<std::vector<float> >				*phoPFConvMom_y;
 extern std::vector<std::vector<float> >				*phoPFConvMom_z;
 extern std::vector<float>				*phoESEffSigmaRR_x;
 extern std::vector<float>				*phoESEffSigmaRR_y;
 extern std::vector<float>				*phoESEffSigmaRR_z;
 extern Int_t				nMu;
 extern std::vector<unsigned long>				*muTrg;
 extern std::vector<float>				*muEta;
 extern std::vector<float>				*muPhi;
 extern std::vector<int>				*muCharge;
 extern std::vector<float>				*muPt;
 extern std::vector<float>				*muPz;
 extern std::vector<float>				*muVtx_x;
 extern std::vector<float>				*muVtx_y;
 extern std::vector<float>				*muVtx_z;
 extern std::vector<float>				*muVtxGlb_x;
 extern std::vector<float>				*muVtxGlb_y;
 extern std::vector<float>				*muVtxGlb_z;
 extern std::vector<float>				*mucktPt;
 extern std::vector<float>				*mucktPtErr;
 extern std::vector<float>				*mucktEta;
 extern std::vector<float>				*mucktPhi;
 extern std::vector<float>				*mucktdxy;
 extern std::vector<float>				*mucktdz;
 extern std::vector<float>				*muIsoTrk;
 extern std::vector<float>				*muIsoCalo;
 extern std::vector<float>				*muIsoEcal;
 extern std::vector<float>				*muIsoHcal;
 extern std::vector<float>				*muChi2NDF;
 extern std::vector<float>				*muInnerChi2NDF;
 extern std::vector<float>				*muPFIsoR04_CH;
 extern std::vector<float>				*muPFIsoR04_NH;
 extern std::vector<float>				*muPFIsoR04_Pho;
 extern std::vector<float>				*muPFIsoR04_PU;
 extern std::vector<float>				*muPFIsoR04_CPart;
 extern std::vector<float>				*muPFIsoR04_NHHT;
 extern std::vector<float>				*muPFIsoR04_PhoHT;
 extern std::vector<float>				*muPFIsoR03_CH;
 extern std::vector<float>				*muPFIsoR03_NH;
 extern std::vector<float>				*muPFIsoR03_Pho;
 extern std::vector<float>				*muPFIsoR03_PU;
 extern std::vector<float>				*muPFIsoR03_CPart;
 extern std::vector<float>				*muPFIsoR03_NHHT;
 extern std::vector<float>				*muPFIsoR03_PhoHT;
 extern std::vector<int>				*muType;
 extern std::vector<float>				*muD0;
 extern std::vector<float>				*muDz;
 extern std::vector<float>				*muD0GV;
 extern std::vector<float>				*muDzGV;
 extern std::vector<std::vector<float> >				*muD0Vtx;
 extern std::vector<std::vector<float> >				*muDzVtx;
 extern std::vector<float>				*muInnerD0;
 extern std::vector<float>				*muInnerDz;
 extern std::vector<float>				*muInnerD0GV;
 extern std::vector<float>				*muInnerDzGV;
 extern std::vector<float>				*muInnerPt;
 extern std::vector<float>				*muInnerPtErr;
 extern std::vector<int>				*muNumberOfValidTrkLayers;
 extern std::vector<int>				*muNumberOfValidTrkHits;
 extern std::vector<int>				*muNumberOfValidPixelLayers;
 extern std::vector<int>				*muNumberOfValidPixelHits;
 extern std::vector<int>				*muNumberOfValidMuonHits;
 extern std::vector<int>				*muStations;
 extern std::vector<int>				*muChambers;
 extern std::vector<float>				*muIP3D;
 extern std::vector<float>				*muIP3DErr;
 extern Int_t				nTau;
 extern std::vector<bool>				*tauDecayModeFinding;
 extern std::vector<bool>				*tauAgainstElectronLooseMVA3;
 extern std::vector<bool>				*tauAgainstElectronMediumMVA3;
 extern std::vector<bool>				*tauAgainstElectronTightMVA3;
 extern std::vector<bool>				*tauAgainstElectronVTightMVA3;
 extern std::vector<bool>				*tauAgainstElectronDeadECAL;
 extern std::vector<bool>				*tauAgainstMuonLoose2;
 extern std::vector<bool>				*tauAgainstMuonMedium2;
 extern std::vector<bool>				*tauAgainstMuonTight2;
 extern std::vector<bool>				*tauCombinedIsolationDeltaBetaCorrRaw3Hits;
 extern std::vector<bool>				*tauLooseCombinedIsolationDeltaBetaCorr3Hits;
 extern std::vector<bool>				*tauMediumCombinedIsolationDeltaBetaCorr3Hits;
 extern std::vector<bool>				*tauTightCombinedIsolationDeltaBetaCorr3Hits;
 extern std::vector<float>				*tauEta;
 extern std::vector<float>				*tauPhi;
 extern std::vector<float>				*tauPt;
 extern std::vector<float>				*tauEt;
 extern std::vector<float>				*tauCharge;
 extern std::vector<int>				*tauDecayMode;
 extern std::vector<float>				*tauEMFraction;
 extern std::vector<float>				*tauHCAL3x3OverPLead;
 extern std::vector<float>				*tauHCALMaxOverPLead;
 extern std::vector<float>				*tauHCALTotOverPLead;
 extern std::vector<float>				*tauIsolationPFChargedHadrCandsPtSum;
 extern std::vector<float>				*tauIsolationPFGammaCandsEtSum;
 extern std::vector<float>				*tauLeadPFChargedHadrCandsignedSipt;
 extern std::vector<bool>				*tauLeadChargedHadronExists;
 extern std::vector<float>				*tauLeadChargedHadronEta;
 extern std::vector<float>				*tauLeadChargedHadronPhi;
 extern std::vector<float>				*tauLeadChargedHadronPt;
 extern Float_t				rho25;
 extern Float_t				rho25_neu;
 extern Float_t				rho25_muPFiso;
 extern Float_t				rho25_elePFiso;
 extern Float_t				rho2011;
 extern Float_t				rho2012;
 extern Float_t				QGTag_MLP;
 extern Float_t				QGTag_likelihood;
 extern Int_t				nCA8Jet;
 extern std::vector<float>				*CA8JetPt;
 extern std::vector<float>				*CA8JetEta;
 extern std::vector<float>				*CA8JetPhi;
 extern std::vector<float>				*CA8JetMass;
 extern std::vector<float>				*CA8JetArea;
 extern std::vector<float>				*CA8Jet_tau1;
 extern std::vector<float>				*CA8Jet_tau2;
 extern std::vector<float>				*CA8Jet_tau3;
 extern std::vector<float>				*CA8JetCHF;
 extern std::vector<float>				*CA8JetNHF;
 extern std::vector<float>				*CA8JetCEF;
 extern std::vector<float>				*CA8JetNEF;
 extern std::vector<int>				*CA8JetNCH;
 extern std::vector<int>				*CA8Jetnconstituents;
 extern std::vector<float>				*CA8prunedJetMass;
 extern std::vector<int>				*CA8prunedJet_nSubJets;
 extern std::vector<std::vector<float> >				*CA8prunedJet_SubjetPt;
 extern std::vector<std::vector<float> >				*CA8prunedJet_SubjetEta;
 extern std::vector<std::vector<float> >				*CA8prunedJet_SubjetPhi;
 extern std::vector<std::vector<float> >				*CA8prunedJet_SubjetMass;
 extern Int_t				nJet;
 extern std::vector<unsigned long>				*jetTrg;
 extern std::vector<float>				*jetEn;
 extern std::vector<float>				*jetPt;
 extern std::vector<float>				*jetEta;
 extern std::vector<float>				*jetPhi;
 extern std::vector<float>				*jetCharge;
 extern std::vector<float>				*jetEt;
 extern std::vector<float>				*jetRawPt;
 extern std::vector<float>				*jetRawEn;
 extern std::vector<float>				*jetArea;
 extern std::vector<float>				*jetCHF;
 extern std::vector<float>				*jetNHF;
 extern std::vector<float>				*jetCEF;
 extern std::vector<float>				*jetNEF;
 extern std::vector<int>				*jetNCH;
 extern std::vector<float>				*jetHFHAE;
 extern std::vector<float>				*jetHFEME;
 extern std::vector<int>				*jetNConstituents;
 extern std::vector<float>				*jetCombinedSecondaryVtxBJetTags;
 extern std::vector<float>				*jetCombinedSecondaryVtxMVABJetTags;
 extern std::vector<float>				*jetJetProbabilityBJetTags;
 extern std::vector<float>				*jetJetBProbabilityBJetTags;
 extern std::vector<std::vector<float> >				*jetBetaStar;
 extern std::vector<bool>				*jetPFLooseId;
 extern std::vector<float>				*jetDRMean;
 extern std::vector<float>				*jetDR2Mean;
 extern std::vector<float>				*jetDZ;
 extern std::vector<float>				*jetFrac01;
 extern std::vector<float>				*jetFrac02;
 extern std::vector<float>				*jetFrac03;
 extern std::vector<float>				*jetFrac04;
 extern std::vector<float>				*jetFrac05;
 extern std::vector<float>				*jetFrac06;
 extern std::vector<float>				*jetFrac07;
 extern std::vector<float>				*jetBeta;
 extern std::vector<float>				*jetBetaStarCMG;
 extern std::vector<float>				*jetBetaStarClassic;
 extern std::vector<std::vector<float> >				*jetBetaExt;
 extern std::vector<std::vector<float> >				*jetBetaStarCMGExt;
 extern std::vector<std::vector<float> >				*jetBetaStarClassicExt;
 extern std::vector<float>				*jetNNeutrals;
 extern std::vector<float>				*jetNCharged;
 extern std::vector<std::vector<float> >				*jetMVAs;
 extern std::vector<std::vector<int> >				*jetWPLevels;
 extern std::vector<std::vector<float> >				*jetMVAsExt_simple;
 extern std::vector<std::vector<int> >				*jetWPLevelsExt_simple;
 extern std::vector<std::vector<float> >				*jetMVAsExt_full;
 extern std::vector<std::vector<int> >				*jetWPLevelsExt_full;
 extern std::vector<std::vector<float> >				*jetMVAsExt_cutBased;
 extern std::vector<std::vector<int> >				*jetWPLevelsExt_cutBased;
 extern std::vector<std::vector<float> >				*jetMVAsExt_philv1;
 extern std::vector<std::vector<int> >				*jetWPLevelsExt_philv1;
 extern std::vector<float>				*jetMt;
 extern std::vector<float>				*jetJECUnc;
 extern std::vector<float>				*jetLeadTrackPt;
 extern std::vector<float>				*jetVtxPt;
 extern std::vector<float>				*jetVtxMass;
 extern std::vector<float>				*jetVtx3dL;
 extern std::vector<float>				*jetVtx3deL;
 extern std::vector<float>				*jetSoftLeptPt;
 extern std::vector<float>				*jetSoftLeptPtRel;
 extern std::vector<float>				*jetSoftLeptdR;
 extern std::vector<float>				*jetSoftLeptIdlooseMu;
 extern std::vector<float>				*jetSoftLeptIdEle95;
 extern std::vector<float>				*jetDPhiMETJet;
 extern std::vector<float>				*jetPuJetIdL;
 extern std::vector<float>				*jetPuJetIdM;
 extern std::vector<float>				*jetPuJetIdT;
 extern Int_t				nLowPtJet;
 extern std::vector<float>				*jetLowPtEn;
 extern std::vector<float>				*jetLowPtPt;
 extern std::vector<float>				*jetLowPtEta;
 extern std::vector<float>				*jetLowPtPhi;
 extern std::vector<float>				*jetLowPtCharge;
 extern std::vector<float>				*jetLowPtEt;
 extern std::vector<float>				*jetLowPtRawPt;
 extern std::vector<float>				*jetLowPtRawEn;
 extern std::vector<float>				*jetLowPtArea;
 extern Int_t				nConv;
 extern std::vector<float>				*convP4_x;
 extern std::vector<float>				*convP4_y;
 extern std::vector<float>				*convP4_z;
 extern std::vector<float>				*convP4_E;
 extern std::vector<float>				*convVtx_x;
 extern std::vector<float>				*convVtx_y;
 extern std::vector<float>				*convVtx_z;
 extern std::vector<float>				*convVtxErr_x;
 extern std::vector<float>				*convVtxErr_y;
 extern std::vector<float>				*convVtxErr_z;
 extern std::vector<float>				*convPairMomentum_x;
 extern std::vector<float>				*convPairMomentum_y;
 extern std::vector<float>				*convPairMomentum_z;
 extern std::vector<float>				*convRefittedMomentum_x;
 extern std::vector<float>				*convRefittedMomentum_y;
 extern std::vector<float>				*convRefittedMomentum_z;
 extern std::vector<int>				*convNTracks;
 extern std::vector<float>				*convPairInvMass;
 extern std::vector<float>				*convPairCotThetaSep;
 extern std::vector<float>				*convEoverP;
 extern std::vector<float>				*convDistOfMinApproach;
 extern std::vector<float>				*convDPhiTrksAtVtx;
 extern std::vector<float>				*convDPhiTrksAtEcal;
 extern std::vector<float>				*convDEtaTrksAtEcal;
 extern std::vector<float>				*convDxy;
 extern std::vector<float>				*convDz;
 extern std::vector<float>				*convLxy;
 extern std::vector<float>				*convLz;
 extern std::vector<float>				*convZofPrimVtxFromTrks;
 extern std::vector<int>				*convNHitsBeforeVtx_0;
 extern std::vector<int>				*convNHitsBeforeVtx_1;
 extern std::vector<int>				*convNSharedHits;
 extern std::vector<int>				*convValidVtx;
 extern std::vector<float>				*convMVALikelihood;
 extern std::vector<float>				*convChi2;
 extern std::vector<float>				*convChi2Probability;
 extern std::vector<float>				*convTk1Dz;
 extern std::vector<float>				*convTk2Dz;
 extern std::vector<float>				*convTk1DzErr;
 extern std::vector<float>				*convTk2DzErr;
 extern std::vector<int>				*convCh1Ch2;
 extern std::vector<float>				*convTk1D0;
 extern std::vector<float>				*convTk1Pout;
 extern std::vector<float>				*convTk1Pin;
 extern std::vector<float>				*convTk2D0;
 extern std::vector<float>				*convTk2Pout;
 extern std::vector<float>				*convTk2Pin;
};
namespace OUT {
 extern Int_t				nHLT;
 extern Int_t				run;
 extern Long64_t				event;
 extern Int_t				lumis;
 extern Bool_t				isData;
 extern Int_t				HLT[453];
 extern Int_t				HLTIndex[70];
 extern Float_t				bspotPos[3];
 extern Int_t				nVtx;
 extern Int_t				IsVtxGood;
 extern Int_t				nGoodVtx;
 extern Int_t				nVtxBS;
 extern std::vector<float>				*vtxbsPtMod;
 extern std::vector<float>				*vtxbsSumPt2;
 extern std::vector<std::vector<int> >				*vtxbsTkIndex;
 extern std::vector<std::vector<float> >				*vtxbsTkWeight;
 extern Int_t				nTrk;
 extern std::vector<float>				*trkP_x;
 extern std::vector<float>				*trkP_y;
 extern std::vector<float>				*trkP_z;
 extern std::vector<float>				*trkVtx_x;
 extern std::vector<float>				*trkVtx_y;
 extern std::vector<float>				*trkVtx_z;
 extern std::vector<float>				*trkd0;
 extern std::vector<float>				*trkd0Err;
 extern std::vector<float>				*trkdz;
 extern std::vector<float>				*trkdzErr;
 extern std::vector<float>				*trkPtErr;
 extern std::vector<int>				*trkQuality;
 extern Int_t				nGoodTrk;
 extern Int_t				IsTracksGood;
 extern Float_t				pfMET;
 extern Float_t				pfMETPhi;
 extern Float_t				pfMETsumEt;
 extern Float_t				pfMETmEtSig;
 extern Float_t				pfMETSig;
 extern Float_t				pfType01MET;
 extern Float_t				pfType01METPhi;
 extern Float_t				pfType01METsumEt;
 extern Float_t				pfType01METmEtSig;
 extern Float_t				pfType01METSig;
 extern Float_t				recoPfMET;
 extern Float_t				recoPfMETPhi;
 extern Float_t				recoPfMETsumEt;
 extern Float_t				recoPfMETmEtSig;
 extern Float_t				recoPfMETSig;
 extern Float_t				trkMETxPV;
 extern Float_t				trkMETyPV;
 extern Float_t				trkMETPhiPV;
 extern Float_t				trkMETPV;
 extern Int_t				metFilters[10];
 extern Int_t				nEle;
 extern std::vector<unsigned long>				*eleTrg;
 extern std::vector<int>				*eleIsEcalDriven;
 extern std::vector<int>				*eleCharge;
 extern std::vector<int>				*eleChargeConsistent;
 extern std::vector<float>				*eleEn;
 extern std::vector<float>				*eleSCEn;
 extern std::vector<float>				*elePt;
 extern std::vector<float>				*eleEta;
 extern std::vector<float>				*elePhi;
 extern std::vector<float>				*eleR9;
 extern std::vector<float>				*eleSCEta;
 extern std::vector<float>				*eleSCPhi;
 extern std::vector<float>				*eleSCEtaWidth;
 extern std::vector<float>				*eleSCPhiWidth;
 extern std::vector<float>				*eleVtx_x;
 extern std::vector<float>				*eleVtx_y;
 extern std::vector<float>				*eleVtx_z;
 extern std::vector<float>				*eleD0;
 extern std::vector<float>				*eleDz;
 extern std::vector<float>				*eleD0GV;
 extern std::vector<float>				*eleDzGV;
 extern std::vector<std::vector<float> >				*eleD0Vtx;
 extern std::vector<std::vector<float> >				*eleDzVtx;
 extern std::vector<float>				*eleHoverE;
 extern std::vector<float>				*eleHoverE12;
 extern std::vector<float>				*eleEoverP;
 extern std::vector<float>				*eledEtaAtVtx;
 extern std::vector<float>				*eledPhiAtVtx;
 extern std::vector<float>				*eleSigmaIEtaIEta;
 extern std::vector<float>				*eleSigmaIEtaIPhi;
 extern std::vector<float>				*eleSigmaIPhiIPhi;
 extern std::vector<float>				*eleEmax;
 extern std::vector<float>				*eleE2ndMax;
 extern std::vector<float>				*eleE1x5;
 extern std::vector<float>				*eleE3x3;
 extern std::vector<float>				*eleE5x5;
 extern std::vector<float>				*eleE2x5Max;
 extern std::vector<std::vector<float> >				*eleGSFPt;
 extern std::vector<std::vector<float> >				*eleGSFEta;
 extern std::vector<std::vector<float> >				*eleGSFPhi;
 extern std::vector<std::vector<float> >				*eleGSFCharge;
 extern std::vector<std::vector<float> >				*eleGSFChi2NDF;
 extern std::vector<int>				*eleRecoFlag;
 extern std::vector<int>				*elePos;
 extern std::vector<float>				*eleIsoTrkDR03;
 extern std::vector<float>				*eleIsoEcalDR03;
 extern std::vector<float>				*eleIsoHcalDR03;
 extern std::vector<float>				*eleIsoHcalDR0312;
 extern std::vector<float>				*eleIsoTrkDR04;
 extern std::vector<float>				*eleIsoEcalDR04;
 extern std::vector<float>				*eleIsoHcalDR04;
 extern std::vector<float>				*eleIsoHcalDR0412;
 extern std::vector<int>				*eleMissHits;
 extern std::vector<float>				*eleConvDist;
 extern std::vector<int>				*eleConvVtxFit;
 extern std::vector<float>				*eleIP3D;
 extern std::vector<float>				*eleIP3DErr;
 extern std::vector<float>				*eleIDMVANonTrig;
 extern std::vector<float>				*eleIDMVATrig;
 extern std::vector<float>				*elePFChIso03;
 extern std::vector<float>				*elePFPhoIso03;
 extern std::vector<float>				*elePFNeuIso03;
 extern std::vector<float>				*elePFChIso04;
 extern std::vector<float>				*elePFPhoIso04;
 extern std::vector<float>				*elePFNeuIso04;
 extern Int_t				nPho;
 extern std::vector<unsigned long>				*phoTrg;
 extern std::vector<unsigned long>				*phoTrgFilter;
 extern std::vector<bool>				*phoIsPhoton;
 extern std::vector<float>				*phoE;
 extern std::vector<float>				*phoEt;
 extern std::vector<float>				*phoEta;
 extern std::vector<float>				*phoVtx_x;
 extern std::vector<float>				*phoVtx_y;
 extern std::vector<float>				*phoVtx_z;
 extern std::vector<float>				*phoPhi;
 extern std::vector<float>				*phoR9;
 extern std::vector<int>				*phoNClus;
 extern std::vector<float>				*phoTrkIsoHollowDR03;
 extern std::vector<float>				*phoEcalIsoDR03;
 extern std::vector<float>				*phoHcalIsoDR03;
 extern std::vector<float>				*phoHcalIsoDR0312;
 extern std::vector<float>				*phoTrkIsoHollowDR04;
 extern std::vector<float>				*phoCiCdRtoTrk;
 extern std::vector<float>				*phoEcalIsoDR04;
 extern std::vector<float>				*phoHcalIsoDR04;
 extern std::vector<float>				*phoHoverE;
 extern std::vector<float>				*phoHoverE12;
 extern std::vector<int>				*phoEleVeto;
 extern std::vector<float>				*phoSigmaIEtaIEta;
 extern std::vector<float>				*phoSigmaIEtaIPhi;
 extern std::vector<float>				*phoSigmaIPhiIPhi;
 extern std::vector<float>				*phoCiCPF4phopfIso03;
 extern std::vector<float>				*phoEmax;
 extern std::vector<float>				*phoE2ndMax;
 extern std::vector<float>				*phoE3x3;
 extern std::vector<float>				*phoE3x1;
 extern std::vector<float>				*phoE1x3;
 extern std::vector<float>				*phoE5x5;
 extern std::vector<float>				*phoE1x5;
 extern std::vector<float>				*phoE2x2;
 extern std::vector<float>				*phoE2x5Max;
 extern std::vector<float>				*phoPFChIso;
 extern std::vector<float>				*phoPFPhoIso;
 extern std::vector<float>				*phoPFNeuIso;
 extern std::vector<float>				*phoSCRChIso;
 extern std::vector<float>				*phoSCRNeuIso;
 extern std::vector<float>				*phoSCRChIso04;
 extern std::vector<float>				*phoSCRPhoIso04;
 extern std::vector<float>				*phoSCRNeuIso04;
 extern std::vector<float>				*phoRandConeChIso;
 extern std::vector<float>				*phoRandConePhoIso;
 extern std::vector<float>				*phoRandConeNeuIso;
 extern std::vector<float>				*phoRandConeChIso04;
 extern std::vector<float>				*phoRandConePhoIso04;
 extern std::vector<float>				*phoRandConeNeuIso04;
 extern std::vector<int>				*phoRecoFlag;
 extern std::vector<int>				*phoPos;
 extern std::vector<float>				*phoSCE;
 extern std::vector<float>				*phoSCRawE;
 extern std::vector<float>				*phoESEn;
 extern std::vector<float>				*phoSCEt;
 extern std::vector<float>				*phoSCEta;
 extern std::vector<float>				*phoSCPhi;
 extern std::vector<float>				*phoSCEtaWidth;
 extern std::vector<float>				*phoSCPhiWidth;
 extern std::vector<int>				*phoOverlap;
 extern std::vector<int>				*phohasPixelSeed;
 extern std::vector<int>				*pho_hasConvPf;
 extern std::vector<int>				*pho_hasSLConvPf;
 extern std::vector<float>				*pho_pfconvVtxZ;
 extern std::vector<float>				*pho_pfconvVtxZErr;
 extern std::vector<int>				*pho_nSLConv;
 extern std::vector<std::vector<float> >				*pho_pfSLConvPos_x;
 extern std::vector<std::vector<float> >				*pho_pfSLConvPos_y;
 extern std::vector<std::vector<float> >				*pho_pfSLConvPos_z;
 extern std::vector<std::vector<float> >				*pho_pfSLConvVtxZ;
 extern std::vector<int>				*phoIsConv;
 extern std::vector<int>				*phoNConv;
 extern std::vector<float>				*phoConvInvMass;
 extern std::vector<float>				*phoConvCotTheta;
 extern std::vector<float>				*phoConvEoverP;
 extern std::vector<float>				*phoConvMinDist;
 extern std::vector<float>				*phoConvdPhiAtVtx;
 extern std::vector<float>				*phoConvdPhiAtCalo;
 extern std::vector<float>				*phoConvdEtaAtCalo;
 extern std::vector<float>				*phoConvTrkPin_x;
 extern std::vector<float>				*phoConvTrkPin_y;
 extern std::vector<float>				*phoConvTrkPout_x;
 extern std::vector<float>				*phoConvTrkPout_y;
 extern std::vector<float>				*phoConvChi2;
 extern std::vector<float>				*phoConvChi2Prob;
 extern std::vector<int>				*phoConvNTrks;
 extern std::vector<float>				*phoConvVtx_x;
 extern std::vector<float>				*phoConvVtx_y;
 extern std::vector<float>				*phoConvVtx_z;
 extern std::vector<float>				*phoConvPairMomentum_x;
 extern std::vector<float>				*phoConvPairMomentum_y;
 extern std::vector<float>				*phoConvPairMomentum_z;
 extern std::vector<int>				*SingleLegConv;
 extern std::vector<std::vector<float> >				*phoPFConvVtx_x;
 extern std::vector<std::vector<float> >				*phoPFConvVtx_y;
 extern std::vector<std::vector<float> >				*phoPFConvVtx_z;
 extern std::vector<std::vector<float> >				*phoPFConvMom_x;
 extern std::vector<std::vector<float> >				*phoPFConvMom_y;
 extern std::vector<std::vector<float> >				*phoPFConvMom_z;
 extern Int_t				nMu;
 extern std::vector<unsigned long>				*muTrg;
 extern std::vector<float>				*muEta;
 extern std::vector<float>				*muPhi;
 extern std::vector<int>				*muCharge;
 extern std::vector<float>				*muPt;
 extern std::vector<float>				*muPz;
 extern std::vector<float>				*muVtx_x;
 extern std::vector<float>				*muVtx_y;
 extern std::vector<float>				*muVtx_z;
 extern std::vector<float>				*muIsoTrk;
 extern std::vector<float>				*muIsoCalo;
 extern std::vector<float>				*muIsoEcal;
 extern std::vector<float>				*muIsoHcal;
 extern std::vector<float>				*muChi2NDF;
 extern std::vector<float>				*muInnerChi2NDF;
 extern std::vector<float>				*muPFIsoR04_CH;
 extern std::vector<float>				*muPFIsoR04_NH;
 extern std::vector<float>				*muPFIsoR04_Pho;
 extern std::vector<float>				*muPFIsoR04_PU;
 extern std::vector<float>				*muPFIsoR04_CPart;
 extern std::vector<float>				*muPFIsoR04_NHHT;
 extern std::vector<float>				*muPFIsoR04_PhoHT;
 extern std::vector<float>				*muPFIsoR03_CH;
 extern std::vector<float>				*muPFIsoR03_NH;
 extern std::vector<float>				*muPFIsoR03_Pho;
 extern std::vector<float>				*muPFIsoR03_PU;
 extern std::vector<float>				*muPFIsoR03_CPart;
 extern std::vector<float>				*muPFIsoR03_NHHT;
 extern std::vector<float>				*muPFIsoR03_PhoHT;
 extern std::vector<int>				*muType;
 extern std::vector<float>				*muD0;
 extern std::vector<float>				*muDz;
 extern std::vector<float>				*muD0GV;
 extern std::vector<float>				*muDzGV;
 extern std::vector<std::vector<float> >				*muD0Vtx;
 extern std::vector<std::vector<float> >				*muDzVtx;
 extern std::vector<float>				*muInnerD0;
 extern std::vector<float>				*muInnerDz;
 extern std::vector<float>				*muInnerD0GV;
 extern std::vector<float>				*muInnerDzGV;
 extern std::vector<float>				*muInnerPt;
 extern std::vector<int>				*muNumberOfValidTrkLayers;
 extern std::vector<int>				*muNumberOfValidTrkHits;
 extern std::vector<int>				*muNumberOfValidPixelLayers;
 extern std::vector<int>				*muNumberOfValidPixelHits;
 extern std::vector<int>				*muNumberOfValidMuonHits;
 extern std::vector<int>				*muStations;
 extern std::vector<int>				*muChambers;
 extern std::vector<float>				*muIP3D;
 extern std::vector<float>				*muIP3DErr;
 extern Int_t				nTau;
 extern Float_t				rho25;
 extern Float_t				rho25_neu;
 extern Float_t				rho25_muPFiso;
 extern Float_t				rho25_elePFiso;
 extern Float_t				rho2011;
 extern Float_t				rho2012;
 extern Float_t				QGTag_MLP;
 extern Float_t				QGTag_likelihood;
 extern Int_t				nCA8Jet;
 extern Int_t				nJet;
 extern std::vector<unsigned long>				*jetTrg;
 extern std::vector<float>				*jetEn;
 extern std::vector<float>				*jetPt;
 extern std::vector<float>				*jetEta;
 extern std::vector<float>				*jetPhi;
 extern std::vector<float>				*jetCharge;
 extern std::vector<float>				*jetEt;
 extern std::vector<float>				*jetRawEn;
 extern std::vector<float>				*jetCHF;
 extern std::vector<float>				*jetNHF;
 extern std::vector<float>				*jetNEF;
 extern std::vector<int>				*jetNCH;
 extern std::vector<int>				*jetNConstituents;
 extern std::vector<float>				*jetNNeutrals;
 extern std::vector<float>				*jetNCharged;
 extern std::vector<float>				*jetLeadTrackPt;
 extern std::vector<float>				*jetVtxPt;
 extern Int_t				nLowPtJet;
 extern Int_t				nConv;
};
#endif
