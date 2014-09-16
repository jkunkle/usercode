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
void CopynVtxBSInToOut( std::string prefix = std::string() ); 
void CopypfMETInToOut( std::string prefix = std::string() ); 
void CopypfMETPhiInToOut( std::string prefix = std::string() ); 
void CopypfMETsumEtInToOut( std::string prefix = std::string() ); 
void CopypfMETmEtSigInToOut( std::string prefix = std::string() ); 
void CopypfMETSigInToOut( std::string prefix = std::string() ); 
void CopyrecoPfMETInToOut( std::string prefix = std::string() ); 
void CopyrecoPfMETPhiInToOut( std::string prefix = std::string() ); 
void CopyrecoPfMETsumEtInToOut( std::string prefix = std::string() ); 
void CopyrecoPfMETmEtSigInToOut( std::string prefix = std::string() ); 
void CopyrecoPfMETSigInToOut( std::string prefix = std::string() ); 
#endif
