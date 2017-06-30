#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "Core/AnalysisBase.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TH2F.h"

class HFChannelMap;

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
        TH1F * hist_LETDCvsEvt_qieA;
        TH1F * hist_LETDCvsEvt_qieB;
        TH2F * hist_HFIntADCvsEvt;
        TH2F * hist_HFSignalEtaPhiD1;
        TH2F * hist_HFSignalEtaPhiD2;
        TH2F * hist_HFTiming;
        TH1F * hist_qie10TDC;

        std::vector<TH1F *> qie10_signals;

        int _evn;
        TFile * _f;

        std::vector<std::pair<int,HFChannelMap> > _hf_channel_map;
        std::vector<HFChannelMap>  _raddam_channels;


};

class HFChannelMap {

    public :

        HFChannelMap(int ieta, int iphi, int depth);

        int GetIEta()  const;
        int GetIPhi()  const;
        int GetDepth() const;
        std::string GetIDString() const;

        void Print();

        bool operator== (const HFChannelMap &comp ) const;

    private : 

        int ieta;
        int iphi;
        int depth;

};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

};

#endif
