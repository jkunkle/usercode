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
    
    // *************************
    // Declare Branches
    // *************************

    // Examples :
    outtree->Branch("ph_pt", &OUT::ph_pt , "ph_pt/F");
    outtree->Branch("ph_eta", &OUT::ph_eta , "ph_eta/F");
    outtree->Branch("ph_sceta", &OUT::ph_sceta , "ph_sceta/F");
    outtree->Branch("ph_phi", &OUT::ph_phi , "ph_phi/F");
    outtree->Branch("ph_e", &OUT::ph_e , "ph_e/F");
    outtree->Branch("ph_HoverE", &OUT::ph_HoverE , "ph_HoverE/F");
    outtree->Branch("ph_HoverE12", &OUT::ph_HoverE12 , "ph_HoverE12/F");
    outtree->Branch("ph_sigmaIEIE", &OUT::ph_sigmaIEIE , "ph_sigmaIEIE/F");
    outtree->Branch("ph_sigmaIEIP", &OUT::ph_sigmaIEIP , "ph_sigmaIEIP/F");
    outtree->Branch("ph_r9", &OUT::ph_r9 , "ph_r9/F");
    outtree->Branch("ph_E1x3", &OUT::ph_E1x3 , "ph_E1x3/F");
    outtree->Branch("ph_E2x2", &OUT::ph_E2x2 , "ph_E2x2/F");
    outtree->Branch("ph_E5x5", &OUT::ph_E5x5 , "ph_E5x5/F");
    outtree->Branch("ph_E2x5Max", &OUT::ph_E2x5Max , "ph_E2x5Max/F");
    outtree->Branch("ph_SCetaWidth", &OUT::ph_SCetaWidth , "ph_SCetaWidth/F");
    outtree->Branch("ph_SCphiWidth", &OUT::ph_SCphiWidth , "ph_SCphiWidth/F");
    outtree->Branch("ph_ESEffSigmaRR", &OUT::ph_ESEffSigmaRR , "ph_ESEffSigmaRR/F");
    outtree->Branch("ph_hcalIsoDR03", &OUT::ph_hcalIsoDR03 , "ph_hcalIsoDR03/F");
    outtree->Branch("ph_trkIsoHollowDR03", &OUT::ph_trkIsoHollowDR03 , "ph_trkIsoHollowDR03/F");
    outtree->Branch("ph_chgpfIsoDR02", &OUT::ph_chgpfIsoDR02 , "ph_chgpfIsoDR02/F");
    outtree->Branch("ph_pfChIsoWorst", &OUT::ph_pfChIsoWorst , "ph_pfChIsoWorst/F");
    outtree->Branch("ph_chIso", &OUT::ph_chIso , "ph_chIso/F");
    outtree->Branch("ph_neuIso", &OUT::ph_neuIso , "ph_neuIso/F");
    outtree->Branch("ph_phoIso", &OUT::ph_phoIso , "ph_phoIso/F");
    outtree->Branch("ph_chIsoCorr", &OUT::ph_chIsoCorr , "ph_chIsoCorr/F");
    outtree->Branch("ph_neuIsoCorr", &OUT::ph_neuIsoCorr , "ph_neuIsoCorr/F");
    outtree->Branch("ph_phoIsoCorr", &OUT::ph_phoIsoCorr , "ph_phoIsoCorr/F");
    outtree->Branch("ph_eleVeto", &OUT::ph_eleVeto , "ph_eleVeto/O");
    outtree->Branch("ph_hasPixSeed", &OUT::ph_hasPixSeed , "ph_hasPixSeed/O");
    outtree->Branch("ph_drToTrk", &OUT::ph_drToTrk , "ph_drToTrk/F");
    outtree->Branch("ph_isConv", &OUT::ph_isConv , "ph_isConv/O");
    outtree->Branch("ph_conv_nTrk", &OUT::ph_conv_nTrk , "ph_conv_nTrk/I");
    outtree->Branch("ph_conv_vtx_x", &OUT::ph_conv_vtx_x , "ph_conv_vtx_x/F");
    outtree->Branch("ph_conv_vtx_y", &OUT::ph_conv_vtx_y , "ph_conv_vtx_y/F");
    outtree->Branch("ph_conv_vtx_z", &OUT::ph_conv_vtx_z , "ph_conv_vtx_z/F");
    outtree->Branch("ph_conv_ptin1", &OUT::ph_conv_ptin1 , "ph_conv_ptin1/F");
    outtree->Branch("ph_conv_ptin2", &OUT::ph_conv_ptin2 , "ph_conv_ptin2/F");
    outtree->Branch("ph_conv_ptout1", &OUT::ph_conv_ptout1 , "ph_conv_ptout1/F");
    outtree->Branch("ph_conv_ptout2", &OUT::ph_conv_ptout2 , "ph_conv_ptout2/F");
    outtree->Branch("ph_passTight", &OUT::ph_passTight , "ph_passTight/O");
    outtree->Branch("ph_passMedium", &OUT::ph_passMedium , "ph_passMedium/O");
    outtree->Branch("ph_passLoose", &OUT::ph_passLoose , "ph_passLoose/O");
    outtree->Branch("ph_passLooseNoSIEIE", &OUT::ph_passLooseNoSIEIE , "ph_passLooseNoSIEIE/O");
    outtree->Branch("ph_passSIEIELoose", &OUT::ph_passSIEIELoose , "ph_passSIEIELoose/O");
    outtree->Branch("ph_passSIEIEMedium", &OUT::ph_passSIEIEMedium , "ph_passSIEIEMedium/O");
    outtree->Branch("ph_passSIEIETight", &OUT::ph_passSIEIETight , "ph_passSIEIETight/O");
    outtree->Branch("ph_passChIsoCorrLoose", &OUT::ph_passChIsoCorrLoose , "ph_passChIsoCorrLoose/O");
    outtree->Branch("ph_passChIsoCorrMedium", &OUT::ph_passChIsoCorrMedium , "ph_passChIsoCorrMedium/O");
    outtree->Branch("ph_passChIsoCorrTight", &OUT::ph_passChIsoCorrTight , "ph_passChIsoCorrTight/O");
    outtree->Branch("ph_passNeuIsoCorrLoose", &OUT::ph_passNeuIsoCorrLoose , "ph_passNeuIsoCorrLoose/O");
    outtree->Branch("ph_passNeuIsoCorrMedium", &OUT::ph_passNeuIsoCorrMedium , "ph_passNeuIsoCorrMedium/O");
    outtree->Branch("ph_passNeuIsoCorrTight", &OUT::ph_passNeuIsoCorrTight , "ph_passNeuIsoCorrTight/O");
    outtree->Branch("ph_passPhoIsoCorrLoose", &OUT::ph_passPhoIsoCorrLoose , "ph_passPhoIsoCorrLoose/O");
    outtree->Branch("ph_passPhoIsoCorrMedium", &OUT::ph_passPhoIsoCorrMedium , "ph_passPhoIsoCorrMedium/O");
    outtree->Branch("ph_passPhoIsoCorrTight", &OUT::ph_passPhoIsoCorrTight , "ph_passPhoIsoCorrTight/O");
    outtree->Branch("ph_truthMatch_el", &OUT::ph_truthMatch_el , "ph_truthMatch_el/O");
    outtree->Branch("ph_truthMinDR_el", &OUT::ph_truthMinDR_el , "ph_truthMinDR_el/F");
    outtree->Branch("ph_truthMatchPt_el", &OUT::ph_truthMatchPt_el , "ph_truthMatchPt_el/F");
    outtree->Branch("ph_truthMatch_ph", &OUT::ph_truthMatch_ph , "ph_truthMatch_ph/O");
    outtree->Branch("ph_truthMinDR_ph", &OUT::ph_truthMinDR_ph , "ph_truthMinDR_ph/F");
    outtree->Branch("ph_truthMatchPt_ph", &OUT::ph_truthMatchPt_ph , "ph_truthMatchPt_ph/F");
    outtree->Branch("ph_truthMatchMotherPID_ph", &OUT::ph_truthMatchMotherPID_ph , "ph_truthMatchMotherPID_ph/I");
    outtree->Branch("ph_hasSLConv", &OUT::ph_hasSLConv , "ph_hasSLConv/O");
    outtree->Branch("ph_pass_mva_presel", &OUT::ph_pass_mva_presel , "ph_pass_mva_presel/O");
    outtree->Branch("ph_mvascore", &OUT::ph_mvascore , "ph_mvascore/F");
    outtree->Branch("ph_IsEB", &OUT::ph_IsEB , "ph_IsEB/O");
    outtree->Branch("ph_IsEE", &OUT::ph_IsEE , "ph_IsEE/O");

    outtree->Branch("ph_s13", &OUT::ph_s13 , "ph_s13/F");
    outtree->Branch("ph_s4ratio", &OUT::ph_s4ratio , "ph_s4ratio/F");
    outtree->Branch("ph_s25", &OUT::ph_s25 , "ph_s25/F");
    _outtree = outtree;

}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    CopyInputVarsToOutput();

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        save_event &= ApplyModule( mod_conf );
    }

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    // This bool is used for filtering
    // If a module implements an event filter
    // update this variable and return it
    // to apply the filter
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

    return false;

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


    // Check for preprocessor defined variables 
    // (set in the generated c++ code) to avoid
    // compilation failures if a certain branch
    // does not exist.  
    // You don't have to be pendantic about it
    // and add a check for every branch, but in this
    // template it is done this way to ensure compilation
    // regardles of the input file used
    for( int idx = 0; idx < IN::ph_n; ++idx ) {

        bool truth_match = (IN::ph_truthMatch_ph->at(idx) && ( abs(IN::ph_truthMatchMotherPID_ph->at(idx) ) < 25 ) );

        float ptdiff = 0;
        if( truth_match ) {
            ptdiff = IN::ph_truthMatchPt_ph->at(idx) - IN::ph_pt->at(idx);
        }

        if( !config.PassBool( "cut_truth_match"    , truth_match       ) ) continue;
        if( !config.PassFloat( "cut_truth_match_ptdiff"    , fabs(ptdiff)      ) ) continue;


        OUT::ph_pt                     = IN::ph_pt                     ->at(idx);
        OUT::ph_eta                    = IN::ph_eta                    ->at(idx);
        OUT::ph_sceta                  = IN::ph_sceta                  ->at(idx);
        OUT::ph_phi                    = IN::ph_phi                    ->at(idx);
        OUT::ph_e                      = IN::ph_e                      ->at(idx);
        OUT::ph_HoverE                 = IN::ph_HoverE                 ->at(idx);
        OUT::ph_HoverE12               = IN::ph_HoverE12               ->at(idx);
        OUT::ph_sigmaIEIE              = IN::ph_sigmaIEIE              ->at(idx);
        OUT::ph_sigmaIEIP              = IN::ph_sigmaIEIP              ->at(idx);
        OUT::ph_r9                     = IN::ph_r9                     ->at(idx);
        OUT::ph_E1x3                   = IN::ph_E1x3                   ->at(idx);
        OUT::ph_E2x2                   = IN::ph_E2x2                   ->at(idx);
        OUT::ph_E5x5                   = IN::ph_E5x5                   ->at(idx);
        OUT::ph_E2x5Max                = IN::ph_E2x5Max                ->at(idx);
        OUT::ph_SCetaWidth             = IN::ph_SCetaWidth             ->at(idx);
        OUT::ph_SCphiWidth             = IN::ph_SCphiWidth             ->at(idx);
        OUT::ph_ESEffSigmaRR           = IN::ph_ESEffSigmaRR           ->at(idx);
        OUT::ph_hcalIsoDR03            = IN::ph_hcalIsoDR03            ->at(idx);
        OUT::ph_trkIsoHollowDR03       = IN::ph_trkIsoHollowDR03       ->at(idx);
        OUT::ph_chgpfIsoDR02           = IN::ph_chgpfIsoDR02           ->at(idx);
        OUT::ph_pfChIsoWorst           = IN::ph_pfChIsoWorst           ->at(idx);
        OUT::ph_chIso                  = IN::ph_chIso                  ->at(idx);
        OUT::ph_neuIso                 = IN::ph_neuIso                 ->at(idx);
        OUT::ph_phoIso                 = IN::ph_phoIso                 ->at(idx);
        OUT::ph_chIsoCorr              = IN::ph_chIsoCorr              ->at(idx);
        OUT::ph_neuIsoCorr             = IN::ph_neuIsoCorr             ->at(idx);
        OUT::ph_phoIsoCorr             = IN::ph_phoIsoCorr             ->at(idx);
        OUT::ph_eleVeto                = IN::ph_eleVeto                ->at(idx);
        OUT::ph_hasPixSeed             = IN::ph_hasPixSeed             ->at(idx);
        OUT::ph_drToTrk                = IN::ph_drToTrk                ->at(idx);
        OUT::ph_isConv                 = IN::ph_isConv                 ->at(idx);
        OUT::ph_conv_nTrk              = IN::ph_conv_nTrk              ->at(idx);
        OUT::ph_conv_vtx_x             = IN::ph_conv_vtx_x             ->at(idx);
        OUT::ph_conv_vtx_y             = IN::ph_conv_vtx_y             ->at(idx);
        OUT::ph_conv_vtx_z             = IN::ph_conv_vtx_z             ->at(idx);
        OUT::ph_conv_ptin1             = IN::ph_conv_ptin1             ->at(idx);
        OUT::ph_conv_ptin2             = IN::ph_conv_ptin2             ->at(idx);
        OUT::ph_conv_ptout1            = IN::ph_conv_ptout1            ->at(idx);
        OUT::ph_conv_ptout2            = IN::ph_conv_ptout2            ->at(idx);
        OUT::ph_passTight              = IN::ph_passTight              ->at(idx);
        OUT::ph_passMedium             = IN::ph_passMedium             ->at(idx);
        OUT::ph_passLoose              = IN::ph_passLoose              ->at(idx);
        OUT::ph_passLooseNoSIEIE       = IN::ph_passLooseNoSIEIE       ->at(idx);
        OUT::ph_passSIEIELoose         = IN::ph_passSIEIELoose         ->at(idx);
        OUT::ph_passSIEIEMedium        = IN::ph_passSIEIEMedium        ->at(idx);
        OUT::ph_passSIEIETight         = IN::ph_passSIEIETight         ->at(idx);
        OUT::ph_passChIsoCorrLoose     = IN::ph_passChIsoCorrLoose     ->at(idx);
        OUT::ph_passChIsoCorrMedium    = IN::ph_passChIsoCorrMedium    ->at(idx);
        OUT::ph_passChIsoCorrTight     = IN::ph_passChIsoCorrTight     ->at(idx);
        OUT::ph_passNeuIsoCorrLoose    = IN::ph_passNeuIsoCorrLoose    ->at(idx);
        OUT::ph_passNeuIsoCorrMedium   = IN::ph_passNeuIsoCorrMedium   ->at(idx);
        OUT::ph_passNeuIsoCorrTight    = IN::ph_passNeuIsoCorrTight    ->at(idx);
        OUT::ph_passPhoIsoCorrLoose    = IN::ph_passPhoIsoCorrLoose    ->at(idx);
        OUT::ph_passPhoIsoCorrMedium   = IN::ph_passPhoIsoCorrMedium   ->at(idx);
        OUT::ph_passPhoIsoCorrTight    = IN::ph_passPhoIsoCorrTight    ->at(idx);
        OUT::ph_truthMatch_el          = IN::ph_truthMatch_el          ->at(idx);
        OUT::ph_truthMinDR_el          = IN::ph_truthMinDR_el          ->at(idx);
        OUT::ph_truthMatchPt_el        = IN::ph_truthMatchPt_el        ->at(idx);
        OUT::ph_truthMatch_ph          = IN::ph_truthMatch_ph          ->at(idx);
        OUT::ph_truthMinDR_ph          = IN::ph_truthMinDR_ph          ->at(idx);
        OUT::ph_truthMatchPt_ph        = IN::ph_truthMatchPt_ph        ->at(idx);
        OUT::ph_truthMatchMotherPID_ph = IN::ph_truthMatchMotherPID_ph ->at(idx);
        OUT::ph_hasSLConv              = IN::ph_hasSLConv              ->at(idx);
        OUT::ph_pass_mva_presel        = IN::ph_pass_mva_presel        ->at(idx);
        OUT::ph_mvascore               = IN::ph_mvascore               ->at(idx);
        OUT::ph_IsEB                   = IN::ph_IsEB                   ->at(idx);
        OUT::ph_IsEE                   = IN::ph_IsEE                   ->at(idx);

        OUT::ph_s13                    = IN::ph_E1x3->at(idx)/IN::ph_E5x5->at(idx);
        OUT::ph_s4ratio                = IN::ph_E2x2->at(idx)/IN::ph_E5x5->at(idx);
        OUT::ph_s25                    = IN::ph_E2x5Max->at(idx)/IN::ph_E5x5->at(idx);

        _outtree->Fill();


    }

}

