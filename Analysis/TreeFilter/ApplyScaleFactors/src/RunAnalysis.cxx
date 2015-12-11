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
    // Set defaults for added output variables
    // *************************
#ifdef MODULE_AddElectronSF
    OUT::el_trigSF = -1;
    OUT::el_trigSFUP = -1;
    OUT::el_trigSFDN = -1;

    OUT::el_diTrigSF = -1;
    OUT::el_diTrigSFUP = -1;
    OUT::el_diTrigSFDN = -1;

    OUT::el_mvaIDSF = -1;
    OUT::el_mvaIDSFUP = -1;
    OUT::el_mvaIDSFDN = -1;

    OUT::el_looseIDSF = -1;
    OUT::el_looseIDSFUP = -1;
    OUT::el_looseIDSFDN = -1;
#endif

#ifdef MODULE_AddPhotonSF
    OUT::ph_idSF = -1;
    OUT::ph_idSFUP = -1;
    OUT::ph_idSFDN = -1;

    OUT::ph_psvSF = -1;
    OUT::ph_psvSFUP = -1;
    OUT::ph_psvSFDN = -1;

    OUT::ph_csevSF = -1;
    OUT::ph_csevSFUP = -1;
    OUT::ph_csevSFDN = -1;
#endif

#ifdef MODULE_AddMuonSF
    OUT::mu_trigSF = -1;
    OUT::mu_trigSFUP = -1;
    OUT::mu_trigSFDN = -1;

    OUT::mu_diTrigSF = -1;
    OUT::mu_diTrigSFUP = -1;
    OUT::mu_diTrigSFDN = -1;

    OUT::mu_isoSF = -1;
    OUT::mu_isoSFUP = -1;
    OUT::mu_isoSFDN = -1;

    OUT::mu_idSF = -1;
    OUT::mu_idSFUP = -1;
    OUT::mu_idSFDN = -1;
#endif

#ifdef MODULE_AddPileupSF
    OUT::PUWeightDN10 = -1;
    OUT::PUWeightUP10 = -1;
    OUT::PUWeightDN5 = -1;
    OUT::PUWeightUP5 = -1;
    OUT::PUWeight = -1;
#endif

    // *************************
    // Declare Branches
    // *************************

    // Examples :
#ifdef MODULE_AddElectronSF
    outtree->Branch( "el_trigSF"    ,  &OUT::el_trigSF    , "el_trigSF/F"    );
    outtree->Branch( "el_trigSFUP"  ,  &OUT::el_trigSFUP  , "el_trigSFUP/F"  );
    outtree->Branch( "el_trigSFDN"  ,  &OUT::el_trigSFDN  , "el_trigSFDN/F"  );
    outtree->Branch( "el_mvaIDSF"      ,  &OUT::el_mvaIDSF      , "el_mvaIDSF/F"      );
    outtree->Branch( "el_mvaIDSFUP"    ,  &OUT::el_mvaIDSFUP    , "el_mvaIDSFUP/F"    );
    outtree->Branch( "el_mvaIDSFDN"    ,  &OUT::el_mvaIDSFDN    , "el_mvaIDSFDN/F"    );
    outtree->Branch( "el_looseIDSF"      ,  &OUT::el_looseIDSF      , "el_looseIDSF/F"      );
    outtree->Branch( "el_looseIDSFUP"    ,  &OUT::el_looseIDSFUP    , "el_looseIDSFUP/F"    );
    outtree->Branch( "el_looseIDSFDN"    ,  &OUT::el_looseIDSFDN    , "el_looseIDSFDN/F"    );
    outtree->Branch( "el_diTrigSF"  ,  &OUT::el_diTrigSF  , "el_diTrigSF/F"  );
    outtree->Branch( "el_diTrigSFUP",  &OUT::el_diTrigSFUP, "el_diTrigSFUP/F");
    outtree->Branch( "el_diTrigSFDN",  &OUT::el_diTrigSFDN, "el_diTrigSFDN/F");
#endif
   
#ifdef MODULE_AddPhotonSF
    outtree->Branch( "ph_idSF"      ,  &OUT::ph_idSF      , "ph_idSF/F"      );
    outtree->Branch( "ph_idSFUP"    ,  &OUT::ph_idSFUP    , "ph_idSFUP/F"    );
    outtree->Branch( "ph_idSFDN"    ,  &OUT::ph_idSFDN    , "ph_idSFDN/F"    );
    outtree->Branch( "ph_psvSF"     ,  &OUT::ph_psvSF     , "ph_psvSF/F"     );
    outtree->Branch( "ph_psvSFUP"   ,  &OUT::ph_psvSFUP   , "ph_psvSFUP/F"   );
    outtree->Branch( "ph_psvSFDN"   ,  &OUT::ph_psvSFDN   , "ph_psvSFDN/F"   );
    outtree->Branch( "ph_csevSF"    ,  &OUT::ph_csevSF    , "ph_csevSF/F"    );
    outtree->Branch( "ph_csevSFUP"  ,  &OUT::ph_csevSFUP  , "ph_csevSFUP/F"  );
    outtree->Branch( "ph_csevSFDN"  ,  &OUT::ph_csevSFDN  , "ph_csevSFDN/F"  );
#endif

#ifdef MODULE_AddMuonSF
    outtree->Branch( "mu_trigSF"    ,  &OUT::mu_trigSF    , "mu_trigSF/F"    );
    outtree->Branch( "mu_trigSFUP"  ,  &OUT::mu_trigSFUP  , "mu_trigSFUP/F"  );
    outtree->Branch( "mu_trigSFDN"  ,  &OUT::mu_trigSFDN  , "mu_trigSFDN/F"  );
    outtree->Branch( "mu_diTrigSF"  ,  &OUT::mu_diTrigSF  , "mu_diTrigSF/F"  );
    outtree->Branch( "mu_diTrigSFUP",  &OUT::mu_diTrigSFUP, "mu_diTrigSFUP/F");
    outtree->Branch( "mu_diTrigSFDN",  &OUT::mu_diTrigSFDN, "mu_diTrigSFDN/F");
    outtree->Branch( "mu_isoSF"     ,  &OUT::mu_isoSF     , "mu_isoSF/F"     );
    outtree->Branch( "mu_isoSFUP"   ,  &OUT::mu_isoSFUP   , "mu_isoSFUP/F"   );
    outtree->Branch( "mu_isoSFDN"   ,  &OUT::mu_isoSFDN   , "mu_isoSFDN/F"   );
    outtree->Branch( "mu_idSF"      ,  &OUT::mu_idSF      , "mu_idSF/F"      );
    outtree->Branch( "mu_idSFUP"    ,  &OUT::mu_idSFUP    , "mu_idSFUP/F"    );
    outtree->Branch( "mu_idSFDN"    ,  &OUT::mu_idSFDN    , "mu_idSFDN/F"    );
#endif

#ifdef MODULE_AddPileupSF
#ifndef EXISTS_PUWeightUP5
    outtree->Branch( "PUWeightUP5"  ,  &OUT::PUWeightUP5  , "PUWeightUP5/F"  );
#endif
#ifndef EXISTS_PUWeightUP10
    outtree->Branch( "PUWeightUP10" ,  &OUT::PUWeightUP10 , "PUWeightUP10/F"  );
#endif
#ifndef EXISTS_PUWeightDN5
    outtree->Branch( "PUWeightDN5"  ,  &OUT::PUWeightDN5  , "PUWeightDN5/F"  );
#endif
#ifndef EXISTS_PUWeightDN10
    outtree->Branch( "PUWeightDN10" ,  &OUT::PUWeightDN10 , "PUWeightDN10/F"  );
#endif
#ifndef EXISTS_PUWeight
    outtree->Branch( "PUWeight" ,  &OUT::PUWeight, "PUWeight/F"  );
#endif
#endif

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {

        if( mod_conf.GetName() == "AddMuonSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;

            itr = mod_conf.GetInitData().find( "FilePathIso" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_iso = TFile::Open( (itr->second).c_str(), "READ" );
                _sfgraph_mu_iso_barrel  = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_iso->Get( "DATA_over_MC_combRelIsoPF04dBeta<02_Tight_pt_abseta<0.9" ));
                _sfgraph_mu_iso_trans   = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_iso->Get( "DATA_over_MC_combRelIsoPF04dBeta<02_Tight_pt_abseta0.9-1.2" ));
                _sfgraph_mu_iso_endcap1 = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_iso->Get( "DATA_over_MC_combRelIsoPF04dBeta<02_Tight_pt_abseta1.2-2.1" ));
                _sfgraph_mu_iso_endcap2 = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_iso->Get( "DATA_over_MC_combRelIsoPF04dBeta<02_Tight_pt_abseta2.1-2.4" ));
            }
            itr = mod_conf.GetInitData().find( "FilePathId" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_id = TFile::Open( (itr->second).c_str(), "READ" );
                _sfgraph_mu_id_barrel  = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_id->Get( "DATA_over_MC_Tight_pt_abseta<0.9" ) );
                _sfgraph_mu_id_trans   = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_id->Get( "DATA_over_MC_Tight_pt_abseta0.9-1.2" ) );
                _sfgraph_mu_id_endcap1 = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_id->Get( "DATA_over_MC_Tight_pt_abseta1.2-2.1" ) );
                _sfgraph_mu_id_endcap2 = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_id->Get( "DATA_over_MC_Tight_pt_abseta2.1-2.4" ) );
            }
            itr = mod_conf.GetInitData().find( "FilePathTrig" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_trig = TFile::Open( (itr->second).c_str(), "READ" );
                _sfgraph_mu_trig_barrel = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_trig->Get( "IsoMu24_eta2p1_DATA_over_MC_TightID_IsodB_PT_ABSETA_Barrel_0to0p9_pt25-500_2012ABCD" ) );
                _sfgraph_mu_trig_trans  = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_trig->Get( "IsoMu24_eta2p1_DATA_over_MC_TightID_IsodB_PT_ABSETA_Transition_0p9to1p2_pt25-500_2012ABCD" ) );
                _sfgraph_mu_trig_endcap = dynamic_cast<TGraphAsymmErrors*>(_sffile_mu_trig->Get( "IsoMu24_eta2p1_DATA_over_MC_TightID_IsodB_PT_ABSETA_Endcaps_1p2to2p1_pt25-500_2012ABCD" ) );
            }
            itr = mod_conf.GetInitData().find( "FilePathDiTrig" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_ditrig = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_mu_ditrig = dynamic_cast<TH2D*>(_sffile_mu_ditrig->Get( "scalefactor eta2d with syst" ));
            }
        }
        if( mod_conf.GetName() == "AddElectronSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "FilePathID" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_el_id = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_el_id = dynamic_cast<TH2F*>(_sffile_el_id->Get( "electronsDATAMCratio_FO_ID_ISO" ));
            }
            itr = mod_conf.GetInitData().find( "FilePathDiTrig" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_el_ditrig = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_el_ditrig = dynamic_cast<TH2D*>(_sffile_el_ditrig->Get( "scalefactor eta2d with syst" ));
            }
            itr = mod_conf.GetInitData().find( "FilePathCutID" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_el_cutid = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_el_looseid = dynamic_cast<TH2D*>(_sffile_el_cutid->Get( "sfLOOSE" ));
            }
        }
        if( mod_conf.GetName() == "AddPhotonSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "FilePathId" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_id = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_ph_id   = dynamic_cast<TH2F*>(_sffile_ph_id->Get( "PhotonIDSF_MediumWP_Jan22rereco_Full2012_S10_MC_V01" ) );
                _sfhist_ph_csev = dynamic_cast<TH2F*>(_sffile_ph_id->Get( "PhotonCSEVSF_MediumWP_Jan22rereco_Full2012_S10_MC_V01" ) );
            }
            itr = mod_conf.GetInitData().find( "FilePathEveto" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_psv = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_ph_psv = dynamic_cast<TH2F*>(_sffile_ph_psv->Get( "hist_sf_eveto_nom" ) );
            }
            itr = mod_conf.GetInitData().find( "FilePathEvetoHighPt" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_psv_highpt = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_ph_psv_highpt = dynamic_cast<TH2F*>(_sffile_ph_psv_highpt->Get( "hist_sf_eveto_highpt" ) );
            }
        }
	
        if( mod_conf.GetName() == "AddPileupSF" ) {
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "DataFilePath" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_pileup_data = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_pileup_data = dynamic_cast<TH1D*>(_sffile_pileup_data->Get("pileup") );

            }
            itr = mod_conf.GetInitData().find( "MCFilePath" );
            if( itr != mod_conf.GetInitData().end() ) {
                std::cout << "Load MC file " << itr->second << std::endl;
                _sffile_pileup_mc = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_pileup_mc = dynamic_cast<TH1F*>(_sffile_pileup_mc->Get("ggNtuplizer/hPUTrue") );
                if( _sfhist_pileup_mc == 0 ) {
                    std::cout << "ERROR -- Did not find MC pileup histogram" << std::endl;
                }
            }
        }
    }

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

    bool keep_evt = true;

    if( config.GetName() == "AddElectronSF" ) {
        AddElectronSF( config );
    }
    if( config.GetName() == "AddMuonSF" ) {
        AddMuonSF( config );
    }
    if( config.GetName() == "AddPhotonSF" ) {
        AddPhotonSF( config );
    }
    if( config.GetName() == "AddPileupSF" ) {
        AddPileupSF( config );
    }
    

    return keep_evt;

}

void RunModule::AddElectronSF( ModuleConfig & /*config*/ ) const {

#ifdef MODULE_AddElectronSF
    OUT::el_mvaIDSF   = 1.0;
    OUT::el_mvaIDSFUP = 1.0;
    OUT::el_mvaIDSFDN = 1.0;

    OUT::el_looseIDSF   = 1.0;
    OUT::el_looseIDSFUP = 1.0;
    OUT::el_looseIDSFDN = 1.0;

    OUT::el_trigSF   = 1.0;
    OUT::el_trigSFUP = 1.0;
    OUT::el_trigSFDN = 1.0;

    OUT::el_diTrigSF   = 1.0;
    OUT::el_diTrigSFUP = 1.0;
    OUT::el_diTrigSFDN = 1.0;

    if( OUT::isData ) {
        return;
    }

    
    std::vector<float> loose_idsf;
    std::vector<float> loose_iderr;

    for( int idx = 0; idx < OUT::el_n; ++idx ) {

        if( OUT::el_triggerMatch->at(idx) && OUT::el_passMvaTrig->at(idx) ) {

            float pt = OUT::el_pt->at(idx);
            float eta = fabs( OUT::el_sceta->at(idx) );
            // histogram ends at 200, if pT is above
            // 200, get the value just below
            if( pt < 200 ) {
                OUT::el_mvaIDSF = _sfhist_el_id->GetBinContent( _sfhist_el_id->FindBin( eta, pt ) );
                float err    = _sfhist_el_id->GetBinError  ( _sfhist_el_id->FindBin( eta, pt ) );
                OUT::el_mvaIDSFUP = OUT::el_mvaIDSF + err;
                OUT::el_mvaIDSFDN = OUT::el_mvaIDSF - err;
            }
            else {
                OUT::el_mvaIDSF = _sfhist_el_id->GetBinContent( _sfhist_el_id->FindBin( eta, 199. ) );
                float err    = _sfhist_el_id->GetBinError  ( _sfhist_el_id->FindBin( eta, 199. ) );
                OUT::el_mvaIDSFUP = OUT::el_mvaIDSF + err;
                OUT::el_mvaIDSFDN = OUT::el_mvaIDSF - err;
            }
        }
        if( OUT::el_triggerMatch->at(idx) ) {

            //https://twiki.cern.ch/twiki/bin/viewauth/CMS/KoPFAElectronTagAndProbe
            if( OUT::el_pt->at(idx) >= 30 && OUT::el_pt->at(idx) <= 40 ) {
                if( fabs(OUT::el_sceta->at(idx)) <= 0.8 ) {
                    OUT::el_trigSF = 0.987;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.012; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.017;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 0.8 && fabs( OUT::el_sceta->at(idx) ) <= 1.478 ) {
                    OUT::el_trigSF = 0.964;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.002; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.001;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 1.478 && fabs( OUT::el_sceta->at(idx) ) <= 2.5 ) {
                    OUT::el_trigSF = 1.004;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.006;
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.006;
                }
            }
            else if( OUT::el_pt->at(idx) > 40 && OUT::el_pt->at(idx) <= 50 ) {
                if( fabs(OUT::el_sceta->at(idx)) <= 0.8 ) {
                    OUT::el_trigSF = 0.997;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.001; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.001;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 0.8 && fabs( OUT::el_sceta->at(idx) ) <= 1.478 ) {
                    OUT::el_trigSF = 0.980;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.001; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.001;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 1.478 && fabs( OUT::el_sceta->at(idx) ) <= 2.5 ) {
                    OUT::el_trigSF = 1.033;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.007;
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.007;
                }
            }
            else if( OUT::el_pt->at(idx) > 50 ) {
                if( fabs(OUT::el_sceta->at(idx)) <= 0.8 ) {
                    OUT::el_trigSF = 0.998;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.002; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.002;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 0.8 && fabs( OUT::el_sceta->at(idx) ) <= 1.478 ) {
                    OUT::el_trigSF = 0.988;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.002; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.002;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 1.478 && fabs( OUT::el_sceta->at(idx) ) <= 2.5 ) {
                    OUT::el_trigSF = 0.976;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.015;
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.012;
                }
            }
        }
        // Do loose scale factors
        //

        if( OUT::el_passLoose->at(idx) ) {
            // if the pT is above 200, get the last bin
            float pt_for_hist = OUT::el_pt->at(idx);
            if( pt_for_hist > 200 ) pt_for_hist = 199.;

            loose_idsf .push_back( _sfhist_el_looseid->GetBinContent( _sfhist_el_looseid->FindBin( fabs(OUT::el_sceta->at(idx) ), pt_for_hist ) ) );
            loose_iderr.push_back( get_ele_cutid_syst( pt_for_hist, fabs( OUT::el_sceta->at(idx) ) ) );
        }
    }

    if( loose_idsf.size() == 1 ) {
        OUT::el_looseIDSF = loose_idsf[0];
        OUT::el_looseIDSFUP = loose_idsf[0] + loose_iderr[0];
        OUT::el_looseIDSFDN = loose_idsf[0] - loose_iderr[0];
    }
    else if( loose_idsf.size() > 1 ) {

        OUT::el_looseIDSF = loose_idsf[0]*loose_idsf[1];
        OUT::el_looseIDSFUP = ( loose_idsf[0] + loose_iderr[0] ) *( loose_idsf[1] + loose_iderr[1] );
        OUT::el_looseIDSFDN = ( loose_idsf[0] - loose_iderr[0] ) *( loose_idsf[1] - loose_iderr[1] );
    }


    if( OUT::el_n==2 ) {

        // https://twiki.cern.ch/twiki/bin/viewauth/CMS/DileptonTriggerResults
        float lead_eta = OUT::el_eta->at(0);
        float subl_eta = OUT::el_eta->at(1);

        if( OUT::el_pt->at( 1 ) > OUT::el_pt->at(0) ) {
            lead_eta = OUT::el_eta->at(1);
            subl_eta = OUT::el_eta->at(0);
        }

        // Fix for electrons beyond 2.4
        if( fabs( lead_eta ) > 2.4 ) lead_eta = 2.39;
        if( fabs( subl_eta ) > 2.4 ) subl_eta = 2.39;

        OUT::el_diTrigSF = _sfhist_el_ditrig->GetBinContent( _sfhist_el_ditrig->FindBin( fabs(lead_eta), fabs(subl_eta) ) );
        float err        = _sfhist_el_ditrig->GetBinError  ( _sfhist_el_ditrig->FindBin( fabs(lead_eta), fabs(subl_eta) ) );
        OUT::el_diTrigSFUP = OUT::el_diTrigSF + err;
        OUT::el_diTrigSFDN = OUT::el_diTrigSF - err;

    }
#endif
}

float RunModule::get_ele_cutid_syst( float pt, float eta ) const {

    // Uncertainty table, from https://twiki.cern.ch/twiki/bin/view/Main/EGammaScaleFactors2012
    // pT                     10 - 15  15 - 20  20 - 30  30 - 40  40 - 50  50 - 200
    // 0.0 < abs(η) < 0.8      11.00    6.90     1.40     0.28     0.14     0.41
    // 0.8 < abs(η) < 1.442    11.00    6.90     1.40     0.28     0.14     0.41
    // 1.442 < abs(η) < 1.556  11.00    8.30     5.70     2.40     0.28     0.43
    // 1.556 < abs(η) < 2.00   12.00    4.00     2.20     0.59     0.30     0.53
    // 2.0 < abs(η) < 2.5      12.00    4.00     2.20     0.59     0.30     0.53
    //
    
    if( pt > 10 && pt <= 15 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.11;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.11;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.11;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.12;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.12;
        }
    }
    else if( pt >15 && pt <= 20 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.069;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.069;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.083;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.04;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.04;
        }
    }
    else if( pt > 20 && pt <= 30 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.014;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.014;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.057;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.022;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.022;
        }
    }
    else if( pt > 30 && pt <= 40 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.0028;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.0028;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.024;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.0059;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.0059;
        }
    }
    else if( pt > 40 && pt <= 50 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.0014;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.0014;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.0028;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.003;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.003;
        }
    }
    else if( pt > 50 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.0041;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.0041;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.0043;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.0053;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.0053;
        }
    }

    std::cout << "WARNING NO SF for pt = " << pt << ", eta = " << eta << std::endl;

    return -1;
}



void RunModule::AddPhotonSF( ModuleConfig & /*config*/ ) const {

#ifdef MODULE_AddPhotonSF

    OUT::ph_idSF = 1.0;
    OUT::ph_idSFUP = 1.0;
    OUT::ph_idSFDN = 1.0;
    
    OUT::ph_psvSF = 1.0;
    OUT::ph_psvSFUP = 1.0;
    OUT::ph_psvSFDN = 1.0;

    OUT::ph_csevSF = 1.0;
    OUT::ph_csevSFUP = 1.0;
    OUT::ph_csevSFDN = 1.0;

    if( OUT::isData ) {
        return;
    }
    // to check if photon pt is above histogram
    float max_pt_highpt = _sfhist_ph_psv_highpt->GetYaxis()->GetBinUpEdge( _sfhist_ph_psv_highpt->GetNbinsY() );
    
    std::vector<float> sfs_id;
    std::vector<float> errs_id;
    std::vector<float> sfs_csev;
    std::vector<float> errs_csev;
    std::vector<float> sfs_psv;
    std::vector<float> errs_psv;
    for( int idx = 0; idx < OUT::ph_n; idx++ ) {

        float pt = OUT::ph_pt->at(idx);
        float feta = fabs(OUT::ph_sceta->at(idx));

        // histogram ends at 1000, if pT is above
        // 1000, get the value just below
        if( pt < 1000 ) {

            sfs_id .push_back(_sfhist_ph_id->GetBinContent( _sfhist_ph_id->FindBin( pt, feta ) ) );
            errs_id.push_back(_sfhist_ph_id->GetBinError  ( _sfhist_ph_id->FindBin( pt, feta ) ) );

            sfs_csev .push_back(_sfhist_ph_csev->GetBinContent( _sfhist_ph_csev->FindBin( pt, feta ) ) );
            errs_csev.push_back(_sfhist_ph_csev->GetBinError  ( _sfhist_ph_csev->FindBin( pt, feta ) ) );
        }
        else {
            sfs_id .push_back(_sfhist_ph_id->GetBinContent( _sfhist_ph_id->FindBin( 999., feta ) ) );
            errs_id.push_back(_sfhist_ph_id->GetBinError  ( _sfhist_ph_id->FindBin( 999., feta ) ) );

            sfs_csev .push_back(_sfhist_ph_csev->GetBinContent( _sfhist_ph_csev->FindBin( 999., feta ) ) );
            errs_csev.push_back(_sfhist_ph_csev->GetBinError  ( _sfhist_ph_csev->FindBin( 999., feta ) ) );
        }


        if( OUT::ph_IsEB->at(idx) ) {
            sfs_psv.push_back( 0.996 );
            errs_psv.push_back( 0.013);
        }
        if( OUT::ph_IsEE->at(idx) ) {
            sfs_psv.push_back( 0.971 );
            errs_psv.push_back( 0.026 );
        }
        
        // --------------------------------
        // Use pT inclusive values
        // switch between highpt and lowpt
        //if( pt < 70 ) {
        //    // FIX for hist only going to 2.4
        //    if( feta > 2.4 && feta < 2.5 ) {
        //        feta = 2.39;
        //    }

        //    if( _sfhist_ph_psv->GetBinContent( _sfhist_ph_psv->FindBin(feta, pt) ) == 0 ) {
        //        if( pt > 15 ) std::cout << " zero value for pt, eta = " << pt << " " << feta << std::endl;
        //    }
        //    sfs_psv.push_back( _sfhist_ph_psv->GetBinContent( _sfhist_ph_psv->FindBin(feta, pt) ) );
        //    errs_psv.push_back( _sfhist_ph_psv->GetBinError( _sfhist_ph_psv->FindBin(feta, pt) ) );
        //}
        //else {
        //    
        //    if( pt >= max_pt_highpt ) {
        //        // FIX for hist only going to 2.4
        //        if( feta > 2.4 && feta < 2.5 ) {
        //            feta = 2.39;
        //        }
        //        if( _sfhist_ph_psv_highpt->GetBinContent( _sfhist_ph_psv_highpt->FindBin(feta, max_pt_highpt-1) ) == 0 ) {
        //            if( pt > 15 ) std::cout << " zero value for pt, eta = " << pt << " " << feta << std::endl;
        //        }
        //        sfs_psv.push_back( _sfhist_ph_psv_highpt->GetBinContent( _sfhist_ph_psv_highpt->FindBin(feta, max_pt_highpt-1 )) );
        //        errs_psv.push_back( _sfhist_ph_psv_highpt->GetBinError( _sfhist_ph_psv_highpt->FindBin(feta, max_pt_highpt-1 ) ));
        //    }
        //    else {
        //        // FIX for hist only going to 2.4
        //        if( feta > 2.4 && feta < 2.5 ) {
        //            feta = 2.39;
        //        }
        //        if( _sfhist_ph_psv_highpt->GetBinContent( _sfhist_ph_psv_highpt->FindBin(feta, pt) ) == 0 ) {
        //            if( pt > 15 ) std::cout << " zero value for pt, eta = " << pt << " " << feta << std::endl;
        //        }
        //        sfs_psv.push_back( _sfhist_ph_psv_highpt->GetBinContent( _sfhist_ph_psv_highpt->FindBin(feta, pt )) );
        //        errs_psv.push_back( _sfhist_ph_psv_highpt->GetBinError( _sfhist_ph_psv_highpt->FindBin(feta, pt ) ));
        //    }
        //}
    }

    if( sfs_id.size() == 1 ) {
        OUT::ph_idSF = sfs_id[0];
        OUT::ph_idSFUP = sfs_id[0]+errs_id[0];
        OUT::ph_idSFDN = sfs_id[0]-errs_id[0];
        
        OUT::ph_psvSF   = sfs_psv[0];
        OUT::ph_psvSFUP = sfs_psv[0]+errs_psv[0];
        OUT::ph_psvSFDN = sfs_psv[0]-errs_psv[0];

        // Also do CSEV
        OUT::ph_csevSF   = sfs_csev[0];
        OUT::ph_csevSFUP = sfs_csev[0]+errs_csev[0];
        OUT::ph_csevSFDN = sfs_csev[0]-errs_csev[0];

    }
    else if( sfs_id.size() > 1 ) {
        OUT::ph_idSF = sfs_id[0]*sfs_id[1];
        OUT::ph_idSFUP = ( sfs_id[0] + errs_id[0] )*( sfs_id[1] + errs_id[1] );
        OUT::ph_idSFDN = ( sfs_id[0] - errs_id[0] )*( sfs_id[1] - errs_id[1] );

        OUT::ph_psvSF = sfs_psv[0]*sfs_psv[1];
        OUT::ph_psvSFUP = (sfs_psv[0]+errs_psv[0])*(sfs_psv[1]+errs_psv[1]);
        OUT::ph_psvSFDN = (sfs_psv[0]-errs_psv[0])*(sfs_psv[1]-errs_psv[1]);

        OUT::ph_csevSF = sfs_csev[0]*sfs_csev[1];
        OUT::ph_csevSFUP = (sfs_csev[0]+errs_csev[0])*(sfs_csev[1]+errs_csev[1]);
        OUT::ph_csevSFDN = (sfs_csev[0]-errs_csev[0])*(sfs_csev[1]-errs_csev[1]);
    }

#endif
}

void RunModule::AddPileupSF( ModuleConfig & /*config*/ ) const { 

#ifdef MODULE_AddPileupSF
    OUT::PUWeight     = 1.0;
    OUT::PUWeightUP5  = 1.0;
    OUT::PUWeightUP10 = 1.0;
    OUT::PUWeightDN5  = 1.0;
    OUT::PUWeightDN10 = 1.0;

#ifdef EXISTS_isData
    if( OUT::isData ) {
        return;
    }
#endif

    float puval = OUT::puTrue->at(0);
    //float puval = OUT::puTrue[0];
    OUT::PUWeight     = calc_pu_weight( puval );
    OUT::PUWeightUP5  = calc_pu_weight( puval, 1.05 );
    OUT::PUWeightUP10 = calc_pu_weight( puval, 1.10 );
    OUT::PUWeightDN5  = calc_pu_weight( puval, 0.95 );
    OUT::PUWeightDN10 = calc_pu_weight( puval, 0.90 );

#endif
}

float RunModule::calc_pu_weight( float puval, float mod ) const {


    float tot_data   = _sfhist_pileup_data->Integral();
    float tot_sample = _sfhist_pileup_mc->Integral();

    int bin_sample = 0;
    int bin_data   = 0;

    if( mod*puval > 60 ) {
        bin_data = 300;
    }
    else {
        bin_data = _sfhist_pileup_data->FindBin(mod*puval);
    }

    bin_sample = _sfhist_pileup_mc->FindBin(puval);

    float val_data = _sfhist_pileup_data->GetBinContent( bin_data );
    float val_sample = _sfhist_pileup_mc->GetBinContent( bin_sample );


    float num = val_data*mod/tot_data;
    float den = val_sample/tot_sample;

    float weight = num/den;

    if( weight < 0.000005 ) {
        std::cout << "PUweight, " << weight << " is zero for PUVal " << puval << " will average over +- 2.5 to get non-zero value " << std::endl;

        int bin_min_sample = _sfhist_pileup_mc->FindBin(puval-2.5);
        int bin_max_sample = _sfhist_pileup_mc->FindBin(puval+2.5);
        int bin_min_data = _sfhist_pileup_data->FindBin((puval*mod)-2.5);
        int bin_max_data = _sfhist_pileup_data->FindBin((puval*mod)+2.5);

        if( puval*mod+2.5  > 60 ) {
            bin_max_data = 300;
        }

        val_data = _sfhist_pileup_data->Integral(bin_min_data, bin_max_data);
        val_sample = _sfhist_pileup_mc->Integral(bin_min_sample, bin_max_sample);

        num = val_data/tot_data;
        den = val_sample/tot_sample;

        weight = num/den;

        if( weight < 0.000005 ) {
            std::cout << "PUweight is still zero!" << std::endl;
        }

    }
    return weight;
}

void RunModule::AddMuonSF( ModuleConfig & /*config*/ ) const { 

#ifdef MODULE_AddMuonSF

    OUT::mu_idSF     = 1.0;
    OUT::mu_idSFUP   = 1.0;
    OUT::mu_idSFDN   = 1.0;

    OUT::mu_isoSF    = 1.0;
    OUT::mu_isoSFUP  = 1.0;
    OUT::mu_isoSFDN  = 1.0;

    OUT::mu_trigSF   = 1.0;
    OUT::mu_trigSFUP = 1.0;
    OUT::mu_trigSFDN = 1.0;

    OUT::mu_diTrigSF   = 1.0;
    OUT::mu_diTrigSFUP = 1.0;
    OUT::mu_diTrigSFDN = 1.0;

    if( OUT::isData ) {
        return;
    }

    std::vector<float> idsfs;
    std::vector<float> iderrsup;
    std::vector<float> iderrsdn;

    std::vector<float> isosfs;
    std::vector<float> isoerrsup;
    std::vector<float> isoerrsdn;

    for( int idx = 0; idx < OUT::mu_n; ++idx ) {
        float feta = fabs(OUT::mu_eta->at(idx));
        float pt   =      OUT::mu_pt ->at(idx) ;
        if( OUT::mu_triggerMatch->at(idx) && OUT::mu_pt->at(idx) > 25 && feta < 2.1 ) {
            ValWithErr entry;
            entry.val = -1;
            if( feta < 0.9 ) {
                entry = GetValsFromGraph( _sfgraph_mu_trig_barrel, pt );
            }
            else if( feta < 1.2 ) {
                entry = GetValsFromGraph( _sfgraph_mu_trig_trans, pt );
            }
            else if( feta <= 2.1  ) {
                entry = GetValsFromGraph( _sfgraph_mu_trig_endcap, pt);
            }
            if( entry.val < 0 ) {
                std::cout << "Failed to get muon trigger SF for pt = " << pt << ", eta = " << feta << std::endl;
            }
            OUT::mu_trigSF = entry.val;
            OUT::mu_trigSFUP = entry.val + entry.err_up;
            OUT::mu_trigSFDN = entry.val - entry.err_dn;
        }
        
        ValWithErr entry_id;
        ValWithErr entry_iso;

        // ID and Iso 
        if( feta < 0.9 ) {
            entry_id = GetValsFromGraph( _sfgraph_mu_id_barrel, pt, false );
            entry_iso = GetValsFromGraph( _sfgraph_mu_iso_barrel, pt, false );

            // fix a bug in the root file
            if( entry_iso.val < 0 ) {
                if( pt > 45 && pt < 50 ) {
                    entry_iso = GetValsFromGraph( _sfgraph_mu_iso_barrel, 41. );
                }
                else { 
                    std::cout << "Failed to get scale factor, but does not fall within the pT region of the bug" << std::endl;
                }
            }
        }
        else if( feta < 1.2 ) {
            entry_id = GetValsFromGraph( _sfgraph_mu_id_trans, pt, false );
            entry_iso = GetValsFromGraph( _sfgraph_mu_iso_trans, pt, false );

            // fix a bug in the root file
            if( entry_iso.val < 0 ) {
                if( pt > 45 && pt < 50 ) {
                    entry_iso = GetValsFromGraph( _sfgraph_mu_iso_trans, 41. );
                }
                else { 
                    std::cout << "Failed to get scale factor, but does not fall within the pT region of the bug" << std::endl;
                }
            }
        }
        else if( feta < 2.1 ) {
            entry_id = GetValsFromGraph( _sfgraph_mu_id_endcap1, pt, false );
            entry_iso = GetValsFromGraph( _sfgraph_mu_iso_endcap1, pt, false );

            // fix a bug in the root file
            if( entry_iso.val < 0 ) {
                if( pt > 45 && pt < 50 ) {
                    entry_iso = GetValsFromGraph( _sfgraph_mu_iso_endcap1, 41. );
                }
                else { 
                    std::cout << "Failed to get scale factor, but does not fall within the pT region of the bug" << std::endl;
                }
            }
        }
        else if( feta < 2.4 ) {
            entry_id = GetValsFromGraph( _sfgraph_mu_id_endcap2, pt, false );
            entry_iso = GetValsFromGraph( _sfgraph_mu_iso_endcap2, pt, false );

            // fix a bug in the root file
            if( entry_iso.val < 0 ) {
                if( pt > 45 && pt < 50 ) {
                    entry_iso = GetValsFromGraph( _sfgraph_mu_iso_endcap2, 41. );
                }
                else { 
                    std::cout << "Failed to get scale factor, but does not fall within the pT region of the bug" << std::endl;
                }
            }
        }

        idsfs   .push_back( entry_id.val    );
        iderrsup.push_back( entry_id.err_up );
        iderrsdn.push_back( entry_id.err_dn );

        isosfs.push_back( entry_iso.val );
        isoerrsup.push_back( entry_iso.err_up );
        isoerrsdn.push_back( entry_iso.err_dn );


    }

    if( OUT::mu_n == 1 ) {

        OUT::mu_idSF   = idsfs[0];
        OUT::mu_idSFUP = idsfs[0] + iderrsup[0];
        OUT::mu_idSFDN = idsfs[0] - iderrsdn[0];

        OUT::mu_isoSF   = isosfs[0];
        OUT::mu_isoSFUP = isosfs[0] + isoerrsup[0];
        OUT::mu_isoSFDN = isosfs[0] - isoerrsdn[0];
    }
    else if( OUT::mu_n > 1 ) {

        OUT::mu_idSF = idsfs[0]*idsfs[1];
        OUT::mu_idSFUP = ( idsfs[0] + iderrsup[0] ) *  ( idsfs[1] + iderrsup[1] );
        OUT::mu_idSFDN = ( idsfs[0] - iderrsdn[0] ) *  ( idsfs[1] - iderrsdn[1] );

        OUT::mu_isoSF = isosfs[0]*isosfs[1];
        OUT::mu_isoSFUP = ( isosfs[0] + isoerrsup[0] ) *  ( isosfs[1] + isoerrsup[1] );
        OUT::mu_isoSFDN = ( isosfs[0] - isoerrsdn[0] ) *  ( isosfs[1] - isoerrsdn[1] );

    }

    if( OUT::mu_n == 2 ) {

        float lead_eta = OUT::mu_eta->at( 0 );
        float subl_eta = OUT::mu_eta->at( 1 );

        if( OUT::mu_pt->at(1) > OUT::mu_pt->at(0) ) {
            lead_eta = OUT::mu_eta->at(1);
            subl_eta = OUT::mu_eta->at(0);
        }

        OUT::mu_diTrigSF = _sfhist_mu_ditrig->GetBinContent( _sfhist_mu_ditrig->FindBin( fabs(lead_eta), fabs(subl_eta) ) );
        float err        = _sfhist_mu_ditrig->GetBinError  ( _sfhist_mu_ditrig->FindBin( fabs(lead_eta), fabs(subl_eta) ) );
        OUT::mu_diTrigSFUP = OUT::mu_diTrigSF + err;
        OUT::mu_diTrigSFDN = OUT::mu_diTrigSF - err;
    }



#endif
}

ValWithErr RunModule::GetValsFromGraph( const TGraphAsymmErrors *graph, float pt, bool debug ) const {

    ValWithErr result;

    for( int point = 0; point < graph->GetN(); ++point ) {

        double x;
        double y;

        graph->GetPoint( point, x, y );
        float xerrmin = graph->GetErrorXlow(point);
        float xerrmax = graph->GetErrorXhigh(point);

        float xmin = x - xerrmin;
        float xmax = x + xerrmax;

        if( pt >= xmin && pt < xmax )  {
            float yerrmin = graph->GetErrorYlow(point);
            float yerrmax = graph->GetErrorYhigh(point);

            result.val = y;
            result.err_up = yerrmax;
            result.err_dn = yerrmin;

            return result;

        }

    }

    // if we get here then the value wasnt
    // within the graph.  Check if its above
    // and return the last entry
    
    double x;
    double y;

    int last_point = graph->GetN()-1;
    graph->GetPoint( last_point, x, y );
    float xerrmax = graph->GetErrorXhigh(last_point);

    if( pt > ( x + xerrmax ) ) {
        result.val = y;
        result.err_up = graph->GetErrorYhigh(last_point);
        result.err_dn = graph->GetErrorYlow(last_point);

        return result;
    }

    if( debug ) {
        std::cout << "No entries for pt " << pt << " in graph " << graph->GetName() << std::endl;
    }

    result.val = -1;

    return result;

}






   


        

