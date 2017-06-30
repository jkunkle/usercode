#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TH2F.h"

class HCALChannelMap;

// The RunModule inherits from RunModuleBase (an Abstract Base Class )
// defined in the Core package so that all
// RunModules present a common interface in a Run function
// This allows the code defined in this package
// to be run from the Core package to minimize
// code duplication in each module

class RunModule : public virtual RunModuleBase {

    public :

        RunModule() {}

        // The run function must exist and be defined exactly as this
        // because it is defined in RunModuleBase 
        // in src/RunModule.cxx all the analysis is defind in this RunModule function
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & config) ;
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( );

        // The ApplyModule function calls any other module defined below
        // in src/RunModule.cxx.  This funciton is not strictly required
        // but its a consistent way to apply modules
        bool ApplyModule         ( ModuleConfig & config ) ;


        // Define modules below.
        // There is no restriction on the naming
        // return values, or inputs to these functions, but
        // you must of course handle them in the source file
        // Examples :
        void RunAnalysis         ( ModuleConfig & config ) ;

    private :

        TTree * _outtree;
        TH2F * hist_SignalEtaPhiD1;
        TH2F * hist_SignalEtaPhiD2;
        TH2F * hist_SignalEtaPhiD3;
        TH2F * hist_SignalEtaPhiD4;

        TH2F * hist_MissingEtaPhiD1;
        TH2F * hist_MissingEtaPhiD2;
        TH2F * hist_MissingEtaPhiD3;
        TH2F * hist_MissingEtaPhiD4;

        TH1F * hist_avgamp_HBP;
        TH1F * hist_avgamp_HBM;
        TH1F * hist_avgamp_HEP;
        TH1F * hist_avgamp_HEM;

        TH1F * hist_chthresh_HBP;
        TH1F * hist_chthresh_HBM;
        TH1F * hist_chthresh_HEP;
        TH1F * hist_chthresh_HEM;



        int _evn;
        TFile * _f;

        std::vector< HCALChannelMap > channels;

        std::map<int, std::vector<int> > channel_counts;


};

class HCALChannelMap {

    public :

        HCALChannelMap(int ieta, int iphi, int depth);

        int GetIEta()  const;
        int GetIPhi()  const;
        int GetDepth() const;
        std::string GetSubDet() const;

        void AddValue( int adc );

        float GetAvgValue( ) const;
        
        std::string GetIDString() const;

        void Print();

        bool operator== (const HCALChannelMap &comp ) const;

    private : 

        int ieta;
        int iphi;
        int depth;
        std::vector<int> values;
        int nvals;
        float avgvals;

};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

};

#endif
