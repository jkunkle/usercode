#include "include/RunAnalysis.h"

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <boost/foreach.hpp>
#include <boost/algorithm/string.hpp>
#include <sys/types.h>
#include <sys/stat.h>
#include <math.h>
#include <stdlib.h>

#include "include/BranchDefs.h"
#include "include/BranchInit.h"

#include "Core/Util.h"

#include "TFile.h"

int main(int argc, char **argv)
{

    //TH1::AddDirectory(kFALSE);
    CmdOptions options = ParseOptions( argc, argv );

    // Parse the text file and form the configuration object
    AnaConfig ana_config = ParseConfig( options.config_file, options );
    std::cout << "Configured " << ana_config.size() << " analysis modules " << std::endl;

    RunModule runmod;
    ana_config.Run(runmod, options);

    std::cout << "^_^ Finished ^_^" << std::endl;


}

void RunModule::initialize( TChain * chain, TTree * outtree, TFile *outfile,
                            const CmdOptions & options, std::vector<ModuleConfig> &configs ) {

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );

    OUT::HLT_DoublePhoton70_v1 = 0;
    OUT::HLT_TriPhoton302020NonIso_v0 = 0;
    OUT::HLT_TriPhoton20NonIso_v0 = 0;
    OUT::HLT_Photon33_v1 = 0;
    OUT::HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v7 = 0;
    OUT::HLT_Diphoton30_22NonIso = 0;
    OUT::HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_NoPixelVeto_Mass55_v7 = 0;
    
    OUT::HLT_TriPhoton20NonIsoNoHE_v0 = 0;
    OUT::HLT_TkMu17_v2 = 0;
    OUT::HLT_TkMu27_v6 = 0;
    OUT::HLT_TriPhoton20CaloIdLCaloIsoM_v0 = 0;
    OUT::HLT_Photon50_R9Id90_HE10_IsoM_v9 = 0;
    OUT::HLT_TriPhoton20CaloIsoM_v0 = 0;
    OUT::HLT_TriPhoton302020NonIsoNoHE_v0 = 0;
    OUT::HLT_TriPhoton404010NonIso_v0 = 0;
    OUT::HLT_Mu27_v6 = 0;
    OUT::HLT_TriPhoton20CaloIdL_v0 = 0;
    OUT::HLT_TriPhoton35355NonIso_v0 = 0;

    OUT::HLT_Mu12Diphoton20NonIso_v0 = 0;
    OUT::HLT_Mu12Diphoton25_20NonIso_v0 = 0;
    OUT::HLT_Mu12Diphoton30_25NonIso_v0 = 0;

    OUT::HLT_SinglePhoton30HiggsCaloId_v0 = 0;
    OUT::HLT_SinglePhoton30HiggsCaloIsoId_v0 = 0;
    OUT::HLT_SinglePhoton30HiggsCaloIso_v0 = 0;
    OUT::HLT_SinglePhoton30NonIso_v0 = 0;
    OUT::HLT_SinglePhoton30R9Id_v0 = 0;
    OUT::HLT_SinglePhoton30CaloIdL_v0 = 0;

    OUT::HLT_Mu12_v6 = 0;
    OUT::HLT_Mu6DoubleEG17TEST4_v0 = 0;
    OUT::HLT_Mu6DoubleEG17TESTOnlyMuDiEG_v0 = 0;
    OUT::HLT_Mu6DoubleEG17TEST3_v0 = 0;
    OUT::HLT_Mu6DoubleEG17TEST5_v0 = 0;
    OUT::HLT_Mu6DoubleEG17TEST2_v0 = 0;
    OUT::HLT_Mu6DoubleEG17TEST1_v0 = 0;
    OUT::HLT_IsoMu27_v8 = 0;
    OUT::HLT_IsoMu27TEST1_v0 = 0;
    OUT::HLT_IsoMu27TEST2_v0 = 0;
    OUT::HLT_IsoTkMu27_v8 = 0;
    OUT::HLT_Mu30_TkMu0_Onia_v1 = 0;

    // *************************
    // Set defaults for added output variables
    // *************************
    // Examples :
    outtree->Branch("HLT_DoublePhoton70_v1", &OUT::HLT_DoublePhoton70_v1);
    outtree->Branch("HLT_TriPhoton302020NonIso_v0", &OUT::HLT_TriPhoton302020NonIso_v0);
    outtree->Branch("HLT_TriPhoton20NonIso_v0", &OUT::HLT_TriPhoton20NonIso_v0);
    outtree->Branch("HLT_Photon33_v1", &OUT::HLT_Photon33_v1);
    outtree->Branch("HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v7", &OUT::HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v7);
    outtree->Branch("HLT_Diphoton30_22NonIso", &OUT::HLT_Diphoton30_22NonIso);
    outtree->Branch("HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_NoPixelVeto_Mass55_v7", &OUT::HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_NoPixelVeto_Mass55_v7);
    outtree->Branch("HLT_TriPhoton20NonIsoNoHE_v0", &OUT::HLT_TriPhoton20NonIsoNoHE_v0);
    outtree->Branch("HLT_TkMu17_v2", &OUT::HLT_TkMu17_v2);
    outtree->Branch("HLT_TkMu27_v6", &OUT::HLT_TkMu27_v6);
    outtree->Branch("HLT_TriPhoton20CaloIdLCaloIsoM_v0", &OUT::HLT_TriPhoton20CaloIdLCaloIsoM_v0);
    outtree->Branch("HLT_Photon50_R9Id90_HE10_IsoM_v9", &OUT::HLT_Photon50_R9Id90_HE10_IsoM_v9);
    outtree->Branch("HLT_TriPhoton20CaloIsoM_v0", &OUT::HLT_TriPhoton20CaloIsoM_v0);
    outtree->Branch("HLT_TriPhoton302020NonIsoNoHE_v0", &OUT::HLT_TriPhoton302020NonIsoNoHE_v0);
    outtree->Branch("HLT_TriPhoton404010NonIso_v0", &OUT::HLT_TriPhoton404010NonIso_v0);
    outtree->Branch("HLT_Mu27_v6", &OUT::HLT_Mu27_v6);
    outtree->Branch("HLT_TriPhoton20CaloIdL_v0", &OUT::HLT_TriPhoton20CaloIdL_v0);
    outtree->Branch("HLT_TriPhoton35355NonIso_v0", &OUT::HLT_TriPhoton35355NonIso_v0);
    outtree->Branch("HLT_Mu12Diphoton20NonIso_v0", &OUT::HLT_Mu12Diphoton20NonIso_v0);
    outtree->Branch("HLT_Mu12Diphoton25_20NonIso_v0", &OUT::HLT_Mu12Diphoton25_20NonIso_v0);
    outtree->Branch("HLT_Mu12Diphoton30_25NonIso_v0", &OUT::HLT_Mu12Diphoton30_25NonIso_v0);

    outtree->Branch("HLT_SinglePhoton30HiggsCaloId_v0", &OUT::HLT_SinglePhoton30HiggsCaloId_v0);
    outtree->Branch("HLT_SinglePhoton30HiggsCaloIsoId_v0", &OUT::HLT_SinglePhoton30HiggsCaloIsoId_v0);
    outtree->Branch("HLT_SinglePhoton30HiggsCaloIso_v0", &OUT::HLT_SinglePhoton30HiggsCaloIso_v0);
    outtree->Branch("HLT_SinglePhoton30NonIso_v0", &OUT::HLT_SinglePhoton30NonIso_v0);
    outtree->Branch("HLT_SinglePhoton30R9Id_v0", &OUT::HLT_SinglePhoton30R9Id_v0);
    outtree->Branch("HLT_SinglePhoton30CaloIdL_v0", &OUT::HLT_SinglePhoton30CaloIdL_v0);

    outtree->Branch("HLT_Mu12_v6", &OUT::HLT_Mu12_v6);
    outtree->Branch("HLT_Mu6DoubleEG17TEST4_v0", &OUT::HLT_Mu6DoubleEG17TEST4_v0);
    outtree->Branch("HLT_Mu6DoubleEG17TESTOnlyMuDiEG_v0", &OUT::HLT_Mu6DoubleEG17TESTOnlyMuDiEG_v0);
    outtree->Branch("HLT_Mu6DoubleEG17TEST3_v0", &OUT::HLT_Mu6DoubleEG17TEST3_v0);
    outtree->Branch("HLT_Mu6DoubleEG17TEST5_v0", &OUT::HLT_Mu6DoubleEG17TEST5_v0);
    outtree->Branch("HLT_Mu6DoubleEG17TEST2_v0", &OUT::HLT_Mu6DoubleEG17TEST2_v0);
    outtree->Branch("HLT_Mu6DoubleEG17TEST1_v0", &OUT::HLT_Mu6DoubleEG17TEST1_v0);
    outtree->Branch("HLT_IsoMu27_v8", &OUT::HLT_IsoMu27_v8);
    outtree->Branch("HLT_IsoMu27TEST1_v0", &OUT::HLT_IsoMu27TEST1_v0);
    outtree->Branch("HLT_IsoMu27TEST2_v0", &OUT::HLT_IsoMu27TEST2_v0);
    outtree->Branch("HLT_IsoTkMu27_v8", &OUT::HLT_IsoTkMu27_v8);
    outtree->Branch("HLT_Mu30_TkMu0_Onia_v1", &OUT::HLT_Mu30_TkMu0_Onia_v1);
}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    CopyInputVarsToOutput();

    OUT::HLT_DoublePhoton70_v1 = int(IN::HLT_DoublePhoton70_v1);
    OUT::HLT_TriPhoton302020NonIso_v0 = int(IN::HLT_TriPhoton302020NonIso_v0);
    OUT::HLT_TriPhoton20NonIso_v0 = int(IN::HLT_TriPhoton20NonIso_v0);
    OUT::HLT_Photon33_v1 = int(IN::HLT_Photon33_v1);
    OUT::HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v7 = int(IN::HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v7);
    OUT::HLT_Diphoton30_22NonIso = int(IN::HLT_Diphoton30_22NonIso);
    OUT::HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_NoPixelVeto_Mass55_v7 = int(IN::HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_NoPixelVeto_Mass55_v7);

    OUT::HLT_TriPhoton20NonIsoNoHE_v0 = int(IN::HLT_TriPhoton20NonIsoNoHE_v0 );
    OUT::HLT_TkMu17_v2 = int(IN::HLT_TkMu17_v2 );
    OUT::HLT_TkMu27_v6 = int(IN::HLT_TkMu27_v6 );
    OUT::HLT_TriPhoton20CaloIdLCaloIsoM_v0 = int(IN::HLT_TriPhoton20CaloIdLCaloIsoM_v0 );
    OUT::HLT_Photon50_R9Id90_HE10_IsoM_v9 = int(IN::HLT_Photon50_R9Id90_HE10_IsoM_v9 );
    OUT::HLT_TriPhoton20CaloIsoM_v0 = int(IN::HLT_TriPhoton20CaloIsoM_v0 );
    OUT::HLT_TriPhoton302020NonIsoNoHE_v0 = int(IN::HLT_TriPhoton302020NonIsoNoHE_v0 );
    OUT::HLT_TriPhoton404010NonIso_v0 = int(IN::HLT_TriPhoton404010NonIso_v0 );
    OUT::HLT_Mu27_v6 = int(IN::HLT_Mu27_v6 );
    OUT::HLT_TriPhoton20CaloIdL_v0 = int(IN::HLT_TriPhoton20CaloIdL_v0 );
    OUT::HLT_TriPhoton35355NonIso_v0 = int(IN::HLT_TriPhoton35355NonIso_v0 );

    OUT::HLT_Mu12Diphoton20NonIso_v0 = int(IN::HLT_Mu12Diphoton20NonIso_v0);
    OUT::HLT_Mu12Diphoton25_20NonIso_v0 = int(IN::HLT_Mu12Diphoton25_20NonIso_v0);
    OUT::HLT_Mu12Diphoton30_25NonIso_v0 = int(IN::HLT_Mu12Diphoton30_25NonIso_v0);

    OUT::HLT_SinglePhoton30HiggsCaloId_v0 = int(IN::HLT_SinglePhoton30HiggsCaloId_v0);
    OUT::HLT_SinglePhoton30HiggsCaloIsoId_v0 = int(IN::HLT_SinglePhoton30HiggsCaloIsoId_v0);
    OUT::HLT_SinglePhoton30HiggsCaloIso_v0 = int(IN::HLT_SinglePhoton30HiggsCaloIso_v0);
    OUT::HLT_SinglePhoton30NonIso_v0 = int(IN::HLT_SinglePhoton30NonIso_v0);
    OUT::HLT_SinglePhoton30R9Id_v0 = int(IN::HLT_SinglePhoton30R9Id_v0);
    OUT::HLT_SinglePhoton30CaloIdL_v0 = int(IN::HLT_SinglePhoton30CaloIdL_v0);

    OUT::HLT_Mu12_v6 = int(IN::HLT_Mu12_v6);
    OUT::HLT_Mu6DoubleEG17TEST4_v0 = int(IN::HLT_Mu6DoubleEG17TEST4_v0);
    OUT::HLT_Mu6DoubleEG17TESTOnlyMuDiEG_v0 = int(IN::HLT_Mu6DoubleEG17TESTOnlyMuDiEG_v0);
    OUT::HLT_Mu6DoubleEG17TEST3_v0 = int(IN::HLT_Mu6DoubleEG17TEST3_v0);
    OUT::HLT_Mu6DoubleEG17TEST5_v0 = int(IN::HLT_Mu6DoubleEG17TEST5_v0);
    OUT::HLT_Mu6DoubleEG17TEST2_v0 = int(IN::HLT_Mu6DoubleEG17TEST2_v0);
    OUT::HLT_Mu6DoubleEG17TEST1_v0 = int(IN::HLT_Mu6DoubleEG17TEST1_v0);
    OUT::HLT_IsoMu27_v8 = int(IN::HLT_IsoMu27_v8);
    OUT::HLT_IsoMu27TEST1_v0 = int(IN::HLT_IsoMu27TEST1_v0);
    OUT::HLT_IsoMu27TEST2_v0 = int(IN::HLT_IsoMu27TEST2_v0);
    OUT::HLT_IsoTkMu27_v8 = int(IN::HLT_IsoTkMu27_v8);
    OUT::HLT_Mu30_TkMu0_Onia_v1 = int(IN::HLT_Mu30_TkMu0_Onia_v1);

    //bool keep_event = false;

    //if( OUT::HLT_SinglePhoton30HiggsCaloId_v0 == 1 ||
    //        OUT::HLT_SinglePhoton30HiggsCaloIsoId_v0 == 1 ||
    //        OUT::HLT_SinglePhoton30HiggsCaloIso_v0 == 1 ||
    //        OUT::HLT_SinglePhoton30NonIso_v0 == 1 ||
    //        OUT::HLT_SinglePhoton30R9Id_v0 == 1 ||
    //        OUT::HLT_SinglePhoton30CaloIdL_v0 == 1 ) {
    //    keep_event = true;
    //}
    //return keep_event;

    return true;
}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    // This bool is used for filtering
    // If a module implements an event filter
    // update this variable and return it
    // to apply the filter
    bool keep_evt = true;

    // This part is a bit hacked.  For each module that
    // you write below, you have to put a call to that
    // function with a matching name here.
    // The name is used to match the name used
    // in the python configuration.
    // There are fancy ways to do this, but it
    // would require the code to be much more complicated
    //
    // Example :
    if( config.GetName() == "BuildPhoton" ) {
        BuildPhoton( config );
    }

    // If the module applies a filter the filter decision
    // is passed back to here.  There is no requirement
    // that a function returns a bool, but
    // if you want the filter to work you need to do this
    //
    // Example :
    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }

    return keep_evt;

}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//
// Examples :

void RunModule::BuildPhoton( ModuleConfig & config ) const {


}

// This is an example of a module that applies an
// event filter.  Note that it returns a bool instead
// of a void.  In principle the modules can return any
// type of variable, you just have to handle it
// in the ApplyModule function

bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;

    return keep_event;
    
}

