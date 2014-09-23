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
#define EXISTS_nVtx
#define EXISTS_nVtxBS
#define EXISTS_nMC
#define EXISTS_nPUInfo
#define EXISTS_nEle
#define EXISTS_nPho
#define EXISTS_nMu
#define EXISTS_nPFPho
#define EXISTS_nJet
#define EXISTS_nConv
#define EXISTS_nLowPtJet
#define EXISTS_run
#define EXISTS_event
#define EXISTS_lumis
#define EXISTS_isData
#define EXISTS_HLT
#define EXISTS_HLTIndex
#define EXISTS_bspotPos
#define EXISTS_vtx
#define EXISTS_IsVtxGood
#define EXISTS_nGoodVtx
#define EXISTS_vtxbs
#define EXISTS_pdf
#define EXISTS_pthat
#define EXISTS_processID
#define EXISTS_mcPID
#define EXISTS_mcPt
#define EXISTS_mcEta
#define EXISTS_mcPhi
#define EXISTS_mcE
#define EXISTS_mcGMomPID
#define EXISTS_mcMomPID
#define EXISTS_mcMomPt
#define EXISTS_mcMomMass
#define EXISTS_mcMomEta
#define EXISTS_mcMomPhi
#define EXISTS_mcIndex
#define EXISTS_mcDecayType
#define EXISTS_mcParentage
#define EXISTS_mcStatus
#define EXISTS_genMET
#define EXISTS_genMETPhi
#define EXISTS_nPU
#define EXISTS_puBX
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
#define EXISTS_trkMETxPV
#define EXISTS_trkMETyPV
#define EXISTS_trkMETPhiPV
#define EXISTS_trkMETPV
#define EXISTS_trkMETx
#define EXISTS_trkMETy
#define EXISTS_trkMETPhi
#define EXISTS_trkMET
#define EXISTS_metFilters
#define EXISTS_eleTrg
#define EXISTS_eleClass
#define EXISTS_eleIsEcalDriven
#define EXISTS_eleCharge
#define EXISTS_eleEn
#define EXISTS_eleEcalEn
#define EXISTS_eleSCRawEn
#define EXISTS_eleSCEn
#define EXISTS_eleESEn
#define EXISTS_elePt
#define EXISTS_eleEta
#define EXISTS_elePhi
#define EXISTS_eleSCEta
#define EXISTS_eleSCPhi
#define EXISTS_eleSCEtaWidth
#define EXISTS_eleSCPhiWidth
#define EXISTS_eleVtx
#define EXISTS_eleD0
#define EXISTS_eleDz
#define EXISTS_eleD0GV
#define EXISTS_eleDzGV
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
#define EXISTS_eleE1x5
#define EXISTS_eleE3x3
#define EXISTS_eleE5x5
#define EXISTS_eleE2x5Max
#define EXISTS_eleRegrE
#define EXISTS_eleRegrEerr
#define EXISTS_elePhoRegrE
#define EXISTS_elePhoRegrEerr
#define EXISTS_eleSeedTime
#define EXISTS_eleRecoFlag
#define EXISTS_elePos
#define EXISTS_eleGenIndex
#define EXISTS_eleGenGMomPID
#define EXISTS_eleGenMomPID
#define EXISTS_eleGenMomPt
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
#define EXISTS_eleIDMVATrigIDIso
#define EXISTS_elePFChIso03
#define EXISTS_elePFPhoIso03
#define EXISTS_elePFNeuIso03
#define EXISTS_elePFChIso04
#define EXISTS_elePFPhoIso04
#define EXISTS_elePFNeuIso04
#define EXISTS_eleESEffSigmaRR
#define EXISTS_phoTrg
#define EXISTS_phoTrgFilter
#define EXISTS_phoIsPhoton
#define EXISTS_phoSCPos
#define EXISTS_phoCaloPos
#define EXISTS_phoE
#define EXISTS_phoEt
#define EXISTS_phoEta
#define EXISTS_phoVtx
#define EXISTS_phoPhi
#define EXISTS_phoR9
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
#define EXISTS_phoEmax
#define EXISTS_phoE3x3
#define EXISTS_phoE3x1
#define EXISTS_phoE1x3
#define EXISTS_phoE5x5
#define EXISTS_phoE1x5
#define EXISTS_phoE2x2
#define EXISTS_phoE2x5Max
#define EXISTS_phoPFChIso
#define EXISTS_phoPFPhoIso
#define EXISTS_phoPFNeuIso
#define EXISTS_phoSCRChIso
#define EXISTS_phoSCRPhoIso
#define EXISTS_phoSCRNeuIso
#define EXISTS_phoRegrE
#define EXISTS_phoRegrEerr
#define EXISTS_phoSeedTime
#define EXISTS_phoSeedDetId1
#define EXISTS_phoSeedDetId2
#define EXISTS_phoLICTD
#define EXISTS_phoRecoFlag
#define EXISTS_phoPos
#define EXISTS_phoGenIndex
#define EXISTS_phoGenGMomPID
#define EXISTS_phoGenMomPID
#define EXISTS_phoGenMomPt
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
#define EXISTS_pho_pfSLConvPos
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
#define EXISTS_phoConvTrkd0
#define EXISTS_phoConvTrkPin
#define EXISTS_phoConvTrkPout
#define EXISTS_phoConvTrkdz
#define EXISTS_phoConvTrkdzErr
#define EXISTS_phoConvChi2
#define EXISTS_phoConvChi2Prob
#define EXISTS_phoConvNTrks
#define EXISTS_phoConvCharge
#define EXISTS_phoConvValidVtx
#define EXISTS_phoConvLikeLihood
#define EXISTS_phoConvP4
#define EXISTS_phoConvVtx
#define EXISTS_phoConvVtxErr
#define EXISTS_phoConvPairMomentum
#define EXISTS_phoConvRefittedMomentum
#define EXISTS_SingleLegConv
#define EXISTS_phoPFConvVtx
#define EXISTS_phoPFConvMom
#define EXISTS_phoESEffSigmaRR
#define EXISTS_muTrg
#define EXISTS_muEta
#define EXISTS_muPhi
#define EXISTS_muCharge
#define EXISTS_muPt
#define EXISTS_muPz
#define EXISTS_muVtx
#define EXISTS_muVtxGlb
#define EXISTS_muGenIndex
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
#define EXISTS_PFPhoEt
#define EXISTS_PFPhoEta
#define EXISTS_PFPhoPhi
#define EXISTS_PFPhoType
#define EXISTS_PFPhoIso
#define EXISTS_rho25
#define EXISTS_rho25_neu
#define EXISTS_rho25_muPFiso
#define EXISTS_rho25_elePFiso
#define EXISTS_rho2011
#define EXISTS_rho2012
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
#define EXISTS_jetTrackCountingHighPurBJetTags
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
#define EXISTS_jetNNeutrals
#define EXISTS_jetNCharged
#define EXISTS_jetMVAs
#define EXISTS_jetWPLevels
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
#define EXISTS_jetPartonID
#define EXISTS_jetGenJetIndex
#define EXISTS_jetGenJetEn
#define EXISTS_jetGenJetPt
#define EXISTS_jetGenJetEta
#define EXISTS_jetGenJetPhi
#define EXISTS_jetGenPartonID
#define EXISTS_jetGenEn
#define EXISTS_jetGenPt
#define EXISTS_jetGenEta
#define EXISTS_jetGenPhi
#define EXISTS_convVtx
#define EXISTS_convVtxErr
#define EXISTS_convPairMomentum
#define EXISTS_convRefittedMomentum
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
#define EXISTS_convNHitsBeforeVtx
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
 extern Int_t				nVtx;
 extern Int_t				nVtxBS;
 extern Int_t				nMC;
 extern Int_t				nPUInfo;
 extern Int_t				nEle;
 extern Int_t				nPho;
 extern Int_t				nMu;
 extern Int_t				nPFPho;
 extern Int_t				nJet;
 extern Int_t				nConv;
 extern Int_t				nLowPtJet;
 extern Int_t				run;
 extern Long64_t				event;
 extern Int_t				lumis;
 extern Bool_t				isData;
 extern Int_t				HLT[444];
 extern Int_t				HLTIndex[70];
 extern Float_t				bspotPos[3];
 extern Float_t				vtx[63][3];
 extern Int_t				IsVtxGood;
 extern Int_t				nGoodVtx;
 extern Float_t				vtxbs[63][3];
 extern Float_t				pdf[7];
 extern Float_t				pthat;
 extern Float_t				processID;
 extern Int_t				mcPID[97];
 extern Float_t				mcPt[97];
 extern Float_t				mcEta[97];
 extern Float_t				mcPhi[97];
 extern Float_t				mcE[97];
 extern Int_t				mcGMomPID[97];
 extern Int_t				mcMomPID[97];
 extern Float_t				mcMomPt[97];
 extern Float_t				mcMomMass[97];
 extern Float_t				mcMomEta[97];
 extern Float_t				mcMomPhi[97];
 extern Int_t				mcIndex[97];
 extern Int_t				mcDecayType[97];
 extern Int_t				mcParentage[97];
 extern Int_t				mcStatus[97];
 extern Float_t				genMET;
 extern Float_t				genMETPhi;
 extern Int_t				nPU[4];
 extern Int_t				puBX[4];
 extern Float_t				puTrue[4];
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
 extern Float_t				trkMETxPV;
 extern Float_t				trkMETyPV;
 extern Float_t				trkMETPhiPV;
 extern Float_t				trkMETPV;
 extern Float_t				trkMETx[63];
 extern Float_t				trkMETy[63];
 extern Float_t				trkMETPhi[63];
 extern Float_t				trkMET[63];
 extern Int_t				metFilters[10];
 extern Int_t				eleTrg[11][16];
 extern Int_t				eleClass[11];
 extern Int_t				eleIsEcalDriven[11];
 extern Int_t				eleCharge[11];
 extern Float_t				eleEn[11];
 extern Float_t				eleEcalEn[11];
 extern Float_t				eleSCRawEn[11];
 extern Float_t				eleSCEn[11];
 extern Float_t				eleESEn[11];
 extern Float_t				elePt[11];
 extern Float_t				eleEta[11];
 extern Float_t				elePhi[11];
 extern Float_t				eleSCEta[11];
 extern Float_t				eleSCPhi[11];
 extern Float_t				eleSCEtaWidth[11];
 extern Float_t				eleSCPhiWidth[11];
 extern Float_t				eleVtx[11][3];
 extern Float_t				eleD0[11];
 extern Float_t				eleDz[11];
 extern Float_t				eleD0GV[11];
 extern Float_t				eleDzGV[11];
 extern Float_t				eleHoverE[11];
 extern Float_t				eleHoverE12[11];
 extern Float_t				eleEoverP[11];
 extern Float_t				elePin[11];
 extern Float_t				elePout[11];
 extern Float_t				eleTrkMomErr[11];
 extern Float_t				eleBrem[11];
 extern Float_t				eledEtaAtVtx[11];
 extern Float_t				eledPhiAtVtx[11];
 extern Float_t				eleSigmaIEtaIEta[11];
 extern Float_t				eleSigmaIEtaIPhi[11];
 extern Float_t				eleSigmaIPhiIPhi[11];
 extern Float_t				eleEmax[11];
 extern Float_t				eleE1x5[11];
 extern Float_t				eleE3x3[11];
 extern Float_t				eleE5x5[11];
 extern Float_t				eleE2x5Max[11];
 extern Float_t				eleRegrE[11];
 extern Float_t				eleRegrEerr[11];
 extern Float_t				elePhoRegrE[11];
 extern Float_t				elePhoRegrEerr[11];
 extern Float_t				eleSeedTime[11];
 extern Int_t				eleRecoFlag[11];
 extern Int_t				elePos[11];
 extern Int_t				eleGenIndex[11];
 extern Int_t				eleGenGMomPID[11];
 extern Int_t				eleGenMomPID[11];
 extern Float_t				eleGenMomPt[11];
 extern Float_t				eleIsoTrkDR03[11];
 extern Float_t				eleIsoEcalDR03[11];
 extern Float_t				eleIsoHcalDR03[11];
 extern Float_t				eleIsoHcalDR0312[11];
 extern Float_t				eleIsoTrkDR04[11];
 extern Float_t				eleIsoEcalDR04[11];
 extern Float_t				eleIsoHcalDR04[11];
 extern Float_t				eleIsoHcalDR0412[11];
 extern Float_t				eleModIsoTrk[11];
 extern Float_t				eleModIsoEcal[11];
 extern Float_t				eleModIsoHcal[11];
 extern Int_t				eleMissHits[11];
 extern Float_t				eleConvDist[11];
 extern Float_t				eleConvDcot[11];
 extern Int_t				eleConvVtxFit[11];
 extern Float_t				eleIP3D[11];
 extern Float_t				eleIP3DErr[11];
 extern Float_t				eleIDMVANonTrig[11];
 extern Float_t				eleIDMVATrig[11];
 extern Float_t				eleIDMVATrigIDIso[11];
 extern Float_t				elePFChIso03[11];
 extern Float_t				elePFPhoIso03[11];
 extern Float_t				elePFNeuIso03[11];
 extern Float_t				elePFChIso04[11];
 extern Float_t				elePFPhoIso04[11];
 extern Float_t				elePFNeuIso04[11];
 extern Float_t				eleESEffSigmaRR[11][3];
 extern Int_t				phoTrg[12][8];
 extern Int_t				phoTrgFilter[12][50];
 extern Bool_t				phoIsPhoton[12];
 extern Float_t				phoSCPos[12][3];
 extern Float_t				phoCaloPos[12][3];
 extern Float_t				phoE[12];
 extern Float_t				phoEt[12];
 extern Float_t				phoEta[12];
 extern Float_t				phoVtx[12][3];
 extern Float_t				phoPhi[12];
 extern Float_t				phoR9[12];
 extern Float_t				phoTrkIsoHollowDR03[12];
 extern Float_t				phoEcalIsoDR03[12];
 extern Float_t				phoHcalIsoDR03[12];
 extern Float_t				phoHcalIsoDR0312[12];
 extern Float_t				phoTrkIsoHollowDR04[12];
 extern Float_t				phoCiCdRtoTrk[12];
 extern Float_t				phoEcalIsoDR04[12];
 extern Float_t				phoHcalIsoDR04[12];
 extern Float_t				phoHcalIsoDR0412[12];
 extern Float_t				phoHoverE[12];
 extern Float_t				phoHoverE12[12];
 extern Int_t				phoEleVeto[12];
 extern Float_t				phoSigmaIEtaIEta[12];
 extern Float_t				phoSigmaIEtaIPhi[12];
 extern Float_t				phoSigmaIPhiIPhi[12];
 extern Float_t				phoCiCPF4phopfIso03[12];
 extern Float_t				phoCiCPF4phopfIso04[12];
 extern Float_t				phoEmax[12];
 extern Float_t				phoE3x3[12];
 extern Float_t				phoE3x1[12];
 extern Float_t				phoE1x3[12];
 extern Float_t				phoE5x5[12];
 extern Float_t				phoE1x5[12];
 extern Float_t				phoE2x2[12];
 extern Float_t				phoE2x5Max[12];
 extern Float_t				phoPFChIso[12];
 extern Float_t				phoPFPhoIso[12];
 extern Float_t				phoPFNeuIso[12];
 extern Float_t				phoSCRChIso[12];
 extern Float_t				phoSCRPhoIso[12];
 extern Float_t				phoSCRNeuIso[12];
 extern Float_t				phoRegrE[12];
 extern Float_t				phoRegrEerr[12];
 extern Float_t				phoSeedTime[12];
 extern Int_t				phoSeedDetId1[12];
 extern Int_t				phoSeedDetId2[12];
 extern Float_t				phoLICTD[12];
 extern Int_t				phoRecoFlag[12];
 extern Int_t				phoPos[12];
 extern Int_t				phoGenIndex[12];
 extern Int_t				phoGenGMomPID[12];
 extern Int_t				phoGenMomPID[12];
 extern Float_t				phoGenMomPt[12];
 extern Float_t				phoSCE[12];
 extern Float_t				phoSCRawE[12];
 extern Float_t				phoESEn[12];
 extern Float_t				phoSCEt[12];
 extern Float_t				phoSCEta[12];
 extern Float_t				phoSCPhi[12];
 extern Float_t				phoSCEtaWidth[12];
 extern Float_t				phoSCPhiWidth[12];
 extern Float_t				phoSCBrem[12];
 extern Int_t				phoOverlap[12];
 extern Int_t				phohasPixelSeed[12];
 extern Int_t				pho_hasConvPf[12];
 extern Int_t				pho_hasSLConvPf[12];
 extern Float_t				pho_pfconvVtxZ[12];
 extern Float_t				pho_pfconvVtxZErr[12];
 extern Int_t				pho_nSLConv[12];
 extern Float_t				pho_pfSLConvPos[12][20][3];
 extern Float_t				pho_pfSLConvVtxZ[12][20];
 extern Int_t				phoIsConv[12];
 extern Int_t				phoNConv[12];
 extern Float_t				phoConvInvMass[12];
 extern Float_t				phoConvCotTheta[12];
 extern Float_t				phoConvEoverP[12];
 extern Float_t				phoConvZofPVfromTrks[12];
 extern Float_t				phoConvMinDist[12];
 extern Float_t				phoConvdPhiAtVtx[12];
 extern Float_t				phoConvdPhiAtCalo[12];
 extern Float_t				phoConvdEtaAtCalo[12];
 extern Float_t				phoConvTrkd0[12][2];
 extern Float_t				phoConvTrkPin[12][2];
 extern Float_t				phoConvTrkPout[12][2];
 extern Float_t				phoConvTrkdz[12][2];
 extern Float_t				phoConvTrkdzErr[12][2];
 extern Float_t				phoConvChi2[12];
 extern Float_t				phoConvChi2Prob[12];
 extern Int_t				phoConvNTrks[12];
 extern Float_t				phoConvCharge[12][2];
 extern Float_t				phoConvValidVtx[12];
 extern Float_t				phoConvLikeLihood[12];
 extern Float_t				phoConvP4[12][4];
 extern Float_t				phoConvVtx[12][3];
 extern Float_t				phoConvVtxErr[12][3];
 extern Float_t				phoConvPairMomentum[12][3];
 extern Float_t				phoConvRefittedMomentum[12][3];
 extern Int_t				SingleLegConv[12];
 extern Float_t				phoPFConvVtx[12][3];
 extern Float_t				phoPFConvMom[12][3];
 extern Float_t				phoESEffSigmaRR[12][3];
 extern Int_t				muTrg[16][10];
 extern Float_t				muEta[16];
 extern Float_t				muPhi[16];
 extern Int_t				muCharge[16];
 extern Float_t				muPt[16];
 extern Float_t				muPz[16];
 extern Float_t				muVtx[16][3];
 extern Float_t				muVtxGlb[16][3];
 extern Int_t				muGenIndex[16];
 extern Float_t				mucktPt[16];
 extern Float_t				mucktPtErr[16];
 extern Float_t				mucktEta[16];
 extern Float_t				mucktPhi[16];
 extern Float_t				mucktdxy[16];
 extern Float_t				mucktdz[16];
 extern Float_t				muIsoTrk[16];
 extern Float_t				muIsoCalo[16];
 extern Float_t				muIsoEcal[16];
 extern Float_t				muIsoHcal[16];
 extern Float_t				muChi2NDF[16];
 extern Float_t				muInnerChi2NDF[16];
 extern Float_t				muPFIsoR04_CH[16];
 extern Float_t				muPFIsoR04_NH[16];
 extern Float_t				muPFIsoR04_Pho[16];
 extern Float_t				muPFIsoR04_PU[16];
 extern Float_t				muPFIsoR04_CPart[16];
 extern Float_t				muPFIsoR04_NHHT[16];
 extern Float_t				muPFIsoR04_PhoHT[16];
 extern Float_t				muPFIsoR03_CH[16];
 extern Float_t				muPFIsoR03_NH[16];
 extern Float_t				muPFIsoR03_Pho[16];
 extern Float_t				muPFIsoR03_PU[16];
 extern Float_t				muPFIsoR03_CPart[16];
 extern Float_t				muPFIsoR03_NHHT[16];
 extern Float_t				muPFIsoR03_PhoHT[16];
 extern Int_t				muType[16];
 extern Float_t				muD0[16];
 extern Float_t				muDz[16];
 extern Float_t				muD0GV[16];
 extern Float_t				muDzGV[16];
 extern Float_t				muInnerD0[16];
 extern Float_t				muInnerDz[16];
 extern Float_t				muInnerD0GV[16];
 extern Float_t				muInnerDzGV[16];
 extern Float_t				muInnerPt[16];
 extern Float_t				muInnerPtErr[16];
 extern Int_t				muNumberOfValidTrkLayers[16];
 extern Int_t				muNumberOfValidTrkHits[16];
 extern Int_t				muNumberOfValidPixelLayers[16];
 extern Int_t				muNumberOfValidPixelHits[16];
 extern Int_t				muNumberOfValidMuonHits[16];
 extern Int_t				muStations[16];
 extern Int_t				muChambers[16];
 extern Float_t				muIP3D[16];
 extern Float_t				muIP3DErr[16];
 extern Float_t				PFPhoEt[50];
 extern Float_t				PFPhoEta[50];
 extern Float_t				PFPhoPhi[50];
 extern Int_t				PFPhoType[50];
 extern Float_t				PFPhoIso[50];
 extern Float_t				rho25;
 extern Float_t				rho25_neu;
 extern Float_t				rho25_muPFiso;
 extern Float_t				rho25_elePFiso;
 extern Float_t				rho2011;
 extern Float_t				rho2012;
 extern Int_t				jetTrg[22][14];
 extern Float_t				jetEn[22];
 extern Float_t				jetPt[22];
 extern Float_t				jetEta[22];
 extern Float_t				jetPhi[22];
 extern Float_t				jetCharge[22];
 extern Float_t				jetEt[22];
 extern Float_t				jetRawPt[22];
 extern Float_t				jetRawEn[22];
 extern Float_t				jetArea[22];
 extern Float_t				jetCHF[22];
 extern Float_t				jetNHF[22];
 extern Float_t				jetCEF[22];
 extern Float_t				jetNEF[22];
 extern Int_t				jetNCH[22];
 extern Float_t				jetHFHAE[22];
 extern Float_t				jetHFEME[22];
 extern Int_t				jetNConstituents[22];
 extern Float_t				jetCombinedSecondaryVtxBJetTags[22];
 extern Float_t				jetCombinedSecondaryVtxMVABJetTags[22];
 extern Float_t				jetJetProbabilityBJetTags[22];
 extern Float_t				jetJetBProbabilityBJetTags[22];
 extern Float_t				jetTrackCountingHighPurBJetTags[22];
 extern Float_t				jetBetaStar[22][100];
 extern Bool_t				jetPFLooseId[22];
 extern Float_t				jetDRMean[22];
 extern Float_t				jetDR2Mean[22];
 extern Float_t				jetDZ[22];
 extern Float_t				jetFrac01[22];
 extern Float_t				jetFrac02[22];
 extern Float_t				jetFrac03[22];
 extern Float_t				jetFrac04[22];
 extern Float_t				jetFrac05[22];
 extern Float_t				jetFrac06[22];
 extern Float_t				jetFrac07[22];
 extern Float_t				jetBeta[22];
 extern Float_t				jetBetaStarCMG[22];
 extern Float_t				jetBetaStarClassic[22];
 extern Float_t				jetBetaExt[22][100];
 extern Float_t				jetNNeutrals[22];
 extern Float_t				jetNCharged[22];
 extern Float_t				jetMVAs[22][4];
 extern Int_t				jetWPLevels[22][4];
 extern Float_t				jetMt[22];
 extern Float_t				jetJECUnc[22];
 extern Float_t				jetLeadTrackPt[22];
 extern Float_t				jetVtxPt[22];
 extern Float_t				jetVtxMass[22];
 extern Float_t				jetVtx3dL[22];
 extern Float_t				jetVtx3deL[22];
 extern Float_t				jetSoftLeptPt[22];
 extern Float_t				jetSoftLeptPtRel[22];
 extern Float_t				jetSoftLeptdR[22];
 extern Float_t				jetSoftLeptIdlooseMu[22];
 extern Float_t				jetSoftLeptIdEle95[22];
 extern Float_t				jetDPhiMETJet[22];
 extern Float_t				jetPuJetIdL[22];
 extern Float_t				jetPuJetIdM[22];
 extern Float_t				jetPuJetIdT[22];
 extern Int_t				jetPartonID[22];
 extern Int_t				jetGenJetIndex[22];
 extern Float_t				jetGenJetEn[22];
 extern Float_t				jetGenJetPt[22];
 extern Float_t				jetGenJetEta[22];
 extern Float_t				jetGenJetPhi[22];
 extern Int_t				jetGenPartonID[22];
 extern Float_t				jetGenEn[22];
 extern Float_t				jetGenPt[22];
 extern Float_t				jetGenEta[22];
 extern Float_t				jetGenPhi[22];
 extern Float_t				convVtx[156][3];
 extern Float_t				convVtxErr[156][3];
 extern Float_t				convPairMomentum[156][3];
 extern Float_t				convRefittedMomentum[156][3];
 extern Int_t				convNTracks[156];
 extern Float_t				convPairInvMass[156];
 extern Float_t				convPairCotThetaSep[156];
 extern Float_t				convEoverP[156];
 extern Float_t				convDistOfMinApproach[156];
 extern Float_t				convDPhiTrksAtVtx[156];
 extern Float_t				convDPhiTrksAtEcal[156];
 extern Float_t				convDEtaTrksAtEcal[156];
 extern Float_t				convDxy[156];
 extern Float_t				convDz[156];
 extern Float_t				convLxy[156];
 extern Float_t				convLz[156];
 extern Float_t				convZofPrimVtxFromTrks[156];
 extern Int_t				convNHitsBeforeVtx[156][2];
 extern Int_t				convNSharedHits[156];
 extern Int_t				convValidVtx[156];
 extern Float_t				convMVALikelihood[156];
 extern Float_t				convChi2[156];
 extern Float_t				convChi2Probability[156];
 extern Float_t				convTk1Dz[156];
 extern Float_t				convTk2Dz[156];
 extern Float_t				convTk1DzErr[156];
 extern Float_t				convTk2DzErr[156];
 extern Int_t				convCh1Ch2[156];
 extern Float_t				convTk1D0[156];
 extern Float_t				convTk1Pout[156];
 extern Float_t				convTk1Pin[156];
 extern Float_t				convTk2D0[156];
 extern Float_t				convTk2Pout[156];
 extern Float_t				convTk2Pin[156];
};
namespace OUT {
 extern Int_t				nVtxBS;
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
};
#endif
