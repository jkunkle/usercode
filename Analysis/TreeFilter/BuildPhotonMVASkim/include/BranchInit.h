#ifndef BRANCHINIT_H
#define BRANCHINIT_H
#include "TTree.h"
#include "TChain.h"
void InitINTree( TChain * tree );
void InitOUTTree( TTree * tree );
void CopyInputVarsToOutput(std::string prefix = std::string() );
void CopyPrefixBranchesInToOut( const std::string & prefix );
void CopyPrefixIndexBranchesInToOut( const std::string & prefix, unsigned index );
void ClearOutputPrefix ( const std::string & prefix );
void CopyrunInToOut( std::string prefix = std::string() ); 
void CopyphoEtInToOut( std::string prefix = std::string() ); 
void CopyphoEtaInToOut( std::string prefix = std::string() ); 
void CopyphoPhiInToOut( std::string prefix = std::string() ); 
void CopyphoR9InToOut( std::string prefix = std::string() ); 
void CopyphoSigmaIEtaIEtaInToOut( std::string prefix = std::string() ); 
void CopyphoSigmaIEtaIPhiInToOut( std::string prefix = std::string() ); 
void CopyphoSigmaIPhiIPhiInToOut( std::string prefix = std::string() ); 
void CopyphoEmaxInToOut( std::string prefix = std::string() ); 
void CopyphoEtopInToOut( std::string prefix = std::string() ); 
void CopyphoEbottomInToOut( std::string prefix = std::string() ); 
void CopyphoEleftInToOut( std::string prefix = std::string() ); 
void CopyphoErightInToOut( std::string prefix = std::string() ); 
void CopyphoE3x3InToOut( std::string prefix = std::string() ); 
void CopyphoE3x1InToOut( std::string prefix = std::string() ); 
void CopyphoE1x3InToOut( std::string prefix = std::string() ); 
void CopyphoE5x5InToOut( std::string prefix = std::string() ); 
void CopyphoE1x5InToOut( std::string prefix = std::string() ); 
void CopyphoE2x2InToOut( std::string prefix = std::string() ); 
void CopyphoE2x5MaxInToOut( std::string prefix = std::string() ); 
void CopyphoE2x5RightInToOut( std::string prefix = std::string() ); 
void CopyphoE2x5LeftInToOut( std::string prefix = std::string() ); 
void CopyphoE2x5TopInToOut( std::string prefix = std::string() ); 
void CopyphoE2x5BottomInToOut( std::string prefix = std::string() ); 
void CopyphoPFChIsoInToOut( std::string prefix = std::string() ); 
void CopyphoPFPhoIsoInToOut( std::string prefix = std::string() ); 
void CopyphoPFNeuIsoInToOut( std::string prefix = std::string() ); 
void CopyphoSCRChIsoInToOut( std::string prefix = std::string() ); 
void CopyphoSCRPhoIsoInToOut( std::string prefix = std::string() ); 
void CopyphoSCRNeuIsoInToOut( std::string prefix = std::string() ); 
void CopyphoSCEInToOut( std::string prefix = std::string() ); 
void CopyphoSCEtaInToOut( std::string prefix = std::string() ); 
void CopyphoSCRawEInToOut( std::string prefix = std::string() ); 
void CopyphoESEnInToOut( std::string prefix = std::string() ); 
void CopyphoSCEtaWidthInToOut( std::string prefix = std::string() ); 
void CopyphoSCPhiWidthInToOut( std::string prefix = std::string() ); 
void CopyphoSCBremInToOut( std::string prefix = std::string() ); 
void CopyphoESEffSigmaRRInToOut( std::string prefix = std::string() ); 
void CopymcphotonInToOut( std::string prefix = std::string() ); 
void Copyrho25InToOut( std::string prefix = std::string() ); 
void Copyrho2012InToOut( std::string prefix = std::string() ); 
void CopyphoHoverE12InToOut( std::string prefix = std::string() ); 
void CopynVtxInToOut( std::string prefix = std::string() ); 
void CopyphoPFChIsoWorstInToOut( std::string prefix = std::string() ); 
void CopyphoPFChIsoBSPVInToOut( std::string prefix = std::string() ); 
#endif
