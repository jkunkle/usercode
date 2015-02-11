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
    OUT::el_trigSF = -1;
    OUT::el_trigSFUP = -1;
    OUT::el_trigSFDN = -1;

    OUT::ph_idSF = -1;
    OUT::ph_idSFUP = -1;
    OUT::ph_idSFDN = -1;

    OUT::ph_evetoSF = -1;
    OUT::ph_evetoSFUP = -1;
    OUT::ph_evetoSFDN = -1;

    OUT::mu_trigSF = -1;
    OUT::mu_trigSFUP = -1;
    OUT::mu_trigSFDN = -1;

    OUT::mu_isoSF = -1;
    OUT::mu_isoSFUP = -1;
    OUT::mu_isoSFDN = -1;

    OUT::mu_idSF = -1;
    OUT::mu_idSFUP = -1;
    OUT::mu_idSFDN = -1;

    // *************************
    // Declare Branches
    // *************************

    // Examples :
    outtree->Branch( "el_trigSF"    ,  &OUT::el_trigSF    , "el_trigSF/F"    );
    outtree->Branch( "el_trigSFUP"  ,  &OUT::el_trigSFUP  , "el_trigSFUP/F"  );
    outtree->Branch( "el_trigSFDN"  ,  &OUT::el_trigSFDN  , "el_trigSFDN/F"  );
    outtree->Branch( "ph_idSF"      ,  &OUT::ph_idSF      , "ph_idSF/F"      );
    outtree->Branch( "ph_idSFUP"    ,  &OUT::ph_idSFUP    , "ph_idSFUP/F"    );
    outtree->Branch( "ph_idSFDN"    ,  &OUT::ph_idSFDN    , "ph_idSFDN/F"    );
    outtree->Branch( "ph_evetoSF"   ,  &OUT::ph_evetoSF   , "ph_evetoSF/F"   );
    outtree->Branch( "ph_evetoSFUP" ,  &OUT::ph_evetoSFUP , "ph_evetoSFUP/F" );
    outtree->Branch( "ph_evetoSFDN" ,  &OUT::ph_evetoSFDN , "ph_evetoSFDN/F" );
    outtree->Branch( "mu_trigSF"    ,  &OUT::mu_trigSF    , "mu_trigSF/F"    );
    outtree->Branch( "mu_trigSFUP"  ,  &OUT::mu_trigSFUP  , "mu_trigSFUP/F"  );
    outtree->Branch( "mu_trigSFDN"  ,  &OUT::mu_trigSFDN  , "mu_trigSFDN/F"  );
    outtree->Branch( "mu_isoSF"     ,  &OUT::mu_isoSF     , "mu_isoSF/F"     );
    outtree->Branch( "mu_isoSFUP"   ,  &OUT::mu_isoSFUP   , "mu_isoSFUP/F"   );
    outtree->Branch( "mu_isoSFDN"   ,  &OUT::mu_isoSFDN   , "mu_isoSFDN/F"   );
    outtree->Branch( "mu_idSF"      ,  &OUT::mu_idSF      , "mu_idSF/F"      );
    outtree->Branch( "mu_idSFUP"    ,  &OUT::mu_idSFUP    , "mu_idSFUP/F"    );
    outtree->Branch( "mu_idSFDN"    ,  &OUT::mu_idSFDN    , "mu_idSFDN/F"    );

    outtree->Branch( "PUWeightUP5"  ,  &OUT::PUWeightUP5  , "PUWeightUP5/F"  );
    outtree->Branch( "PUWeightUP10" ,  &OUT::PUWeightUP10 , "PUWeightUP10/F"  );
    outtree->Branch( "PUWeightDN5"  ,  &OUT::PUWeightDN5  , "PUWeightDN5/F"  );
    outtree->Branch( "PUWeightDN10" ,  &OUT::PUWeightDN10 , "PUWeightDN10/F"  );

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
        }
        if( mod_conf.GetName() == "AddElectronSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "FilePathId" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_el_id = TFile::Open( (itr->second).c_str(), "READ" );
            }
            itr = mod_conf.GetInitData().find( "FilePathTrig" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_el_trig = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_el_trig = dynamic_cast<TH2F*>(_sffile_el_trig->Get( "electronsDATAMCratio_FO_ID_ISO" ));
            }
        }
        if( mod_conf.GetName() == "AddPhotonSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "FilePathId" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_id = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_ph_id = dynamic_cast<TH2F*>(_sffile_ph_id->Get( "PhotonIDSF_MediumWP_Jan22rereco_Full2012_S10_MC_V01" ) );
            }
            itr = mod_conf.GetInitData().find( "FilePathEveto" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_eveto = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_ph_eveto = dynamic_cast<TH2F*>(_sffile_ph_eveto->Get( "hist_sf_eveto_nom" ) );
            }
            itr = mod_conf.GetInitData().find( "FilePathEvetoHighPt" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_eveto_highpt = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_ph_eveto_highpt = dynamic_cast<TH2F*>(_sffile_ph_eveto_highpt->Get( "hist_sf_eveto_highpt" ) );
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

    OUT::el_trigSF   = 1.0;
    OUT::el_trigSFUP = 1.0;
    OUT::el_trigSFDN = 1.0;

    if( OUT::isData ) {
        return;
    }

    for( int idx = 0; idx < OUT::el_n; ++idx ) {

        if( OUT::el_triggerMatch->at(idx) && OUT::el_passMvaTrig->at(idx) ) {

            float pt = OUT::el_pt->at(idx);
            float eta = fabs( OUT::el_eta->at(idx) );
            // histogram ends at 200, if pT is above
            // 200, get the value just below
            if( pt < 200 ) {
                OUT::el_trigSF = _sfhist_el_trig->GetBinContent( _sfhist_el_trig->FindBin( eta, pt ) );
                float err = _sfhist_el_trig->GetBinError( _sfhist_el_trig->FindBin( eta, pt ) );
                OUT::el_trigSFUP = OUT::el_trigSF + err;
                OUT::el_trigSFDN = OUT::el_trigSF - err;
            }
            else {
                OUT::el_trigSF = _sfhist_el_trig->GetBinContent( _sfhist_el_trig->FindBin( eta, 199. ) );
                float err = _sfhist_el_trig->GetBinError( _sfhist_el_trig->FindBin( eta, 199. ) );
                OUT::el_trigSFUP = OUT::el_trigSF + err;
                OUT::el_trigSFDN = OUT::el_trigSF - err;
            }

        }
    }


}

void RunModule::AddPhotonSF( ModuleConfig & /*config*/ ) const {

    OUT::ph_idSF = 1.0;
    OUT::ph_idSFUP = 1.0;
    OUT::ph_idSFDN = 1.0;
    
    OUT::ph_evetoSF = 1.0;
    OUT::ph_evetoSFUP = 1.0;
    OUT::ph_evetoSFDN = 1.0;

    if( OUT::isData ) {
        return;
    }
    // to check if photon pt is above histogram
    float max_pt_highpt = _sfhist_ph_eveto_highpt->GetYaxis()->GetBinUpEdge( _sfhist_ph_eveto_highpt->GetNbinsY() );
    
    std::vector<float> sfs_id;
    std::vector<float> errs_id;
    std::vector<float> sfs_eveto;
    std::vector<float> errs_eveto;
    for( int idx = 0; idx < OUT::ph_n; idx++ ) {

        float pt = OUT::ph_pt->at(idx);
        float feta = fabs(OUT::ph_sceta->at(idx));

        // histogram ends at 1000, if pT is above
        // 1000, get the value just below
        if( pt < 1000 ) {

            sfs_id.push_back(_sfhist_ph_id->GetBinContent( _sfhist_ph_id->FindBin( pt, feta ) ) );
            errs_id.push_back(_sfhist_ph_id->GetBinError( _sfhist_ph_id->FindBin( pt, feta ) ) );
        }
        else {
            sfs_id.push_back(_sfhist_ph_id->GetBinContent( _sfhist_ph_id->FindBin( 999., feta ) ) );
            errs_id.push_back(_sfhist_ph_id->GetBinError( _sfhist_ph_id->FindBin( 999., feta ) ) );
        }


        // switch between highpt and lowpt
        if( pt < 70 ) {
            if( _sfhist_ph_eveto->GetBinContent( _sfhist_ph_eveto->FindBin(feta, pt) ) == 0 ) {
                std::cout << " zero value for pt, eta = " << pt << " " << feta << std::endl;
            }
            sfs_eveto.push_back( _sfhist_ph_eveto->GetBinContent( _sfhist_ph_eveto->FindBin(feta, pt) ) );
            errs_eveto.push_back( _sfhist_ph_eveto->GetBinError( _sfhist_ph_eveto->FindBin(feta, pt) ) );
        }
        else {
            
            if( pt >= max_pt_highpt ) {
                if( _sfhist_ph_eveto_highpt->GetBinContent( _sfhist_ph_eveto_highpt->FindBin(feta, max_pt_highpt-1) ) == 0 ) {
                    std::cout << " zero value for pt, eta = " << pt << " " << feta << std::endl;
                }
                sfs_eveto.push_back( _sfhist_ph_eveto_highpt->GetBinContent( _sfhist_ph_eveto_highpt->FindBin(feta, max_pt_highpt-1 )) );
                errs_eveto.push_back( _sfhist_ph_eveto_highpt->GetBinError( _sfhist_ph_eveto_highpt->FindBin(feta, max_pt_highpt-1 ) ));
            }
            else {
                if( _sfhist_ph_eveto_highpt->GetBinContent( _sfhist_ph_eveto_highpt->FindBin(feta, pt) ) == 0 ) {
                    std::cout << " zero value for pt, eta = " << pt << " " << feta << std::endl;
                }
                sfs_eveto.push_back( _sfhist_ph_eveto_highpt->GetBinContent( _sfhist_ph_eveto_highpt->FindBin(feta, pt )) );
                errs_eveto.push_back( _sfhist_ph_eveto_highpt->GetBinError( _sfhist_ph_eveto_highpt->FindBin(feta, pt ) ));
            }
        }
    }

    if( sfs_id.size() == 1 ) {
        OUT::ph_idSF = sfs_id[0];
        OUT::ph_idSFUP = sfs_id[0]+errs_id[0];
        OUT::ph_idSFDN = sfs_id[0]-errs_id[0];
        
        OUT::ph_evetoSF = sfs_eveto[0];
        OUT::ph_evetoSFUP = sfs_eveto[0]+errs_eveto[0];
        OUT::ph_evetoSFDN = sfs_eveto[0]-errs_eveto[0];
    }
    else if( sfs_id.size() > 1 ) {
        OUT::ph_idSF = sfs_id[0]*sfs_id[1];
        OUT::ph_idSFUP = ( sfs_id[0] + errs_id[0] )*( sfs_id[1] + errs_id[1] );
        OUT::ph_idSFDN = ( sfs_id[0] - errs_id[0] )*( sfs_id[1] - errs_id[1] );

        OUT::ph_evetoSF = sfs_eveto[0]*sfs_eveto[1];
        OUT::ph_evetoSFUP = (sfs_eveto[0]+errs_eveto[0])*(sfs_eveto[1]+errs_eveto[1]);
        OUT::ph_evetoSFDN = (sfs_eveto[0]-errs_eveto[0])*(sfs_eveto[1]-errs_eveto[1]);
    }

}

void RunModule::AddPileupSF( ModuleConfig & /*config*/ ) const { 

    OUT::PUWeight     = 1.0;
    OUT::PUWeightUP5  = 1.0;
    OUT::PUWeightUP10 = 1.0;
    OUT::PUWeightDN5  = 1.0;
    OUT::PUWeightDN10 = 1.0;

    if( OUT::isData ) {
        return;
    }

    float puval = OUT::puTrue->at(0);
    OUT::PUWeight     = calc_pu_weight( puval );
    OUT::PUWeightUP5  = calc_pu_weight( puval, 1.05 );
    OUT::PUWeightUP10 = calc_pu_weight( puval, 1.10 );
    OUT::PUWeightDN5  = calc_pu_weight( puval, 0.95 );
    OUT::PUWeightDN10 = calc_pu_weight( puval, 0.90 );

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


    float num = val_data/tot_data;
    float den = val_sample/tot_sample;

    float weight = num/den;

    if( weight < 0.005 ) {
        std::cout << "PUweight, " << weight << " is zero for PUVal " << puval << " will average over +- 2.5 to get non-zero value " << std::endl;

        int bin_min_sample = _sfhist_pileup_mc->FindBin(puval-2.5);
        int bin_max_sample = _sfhist_pileup_mc->FindBin(puval+2.5);
        int bin_min_data = _sfhist_pileup_data->FindBin(puval*mod-2.5);
        int bin_max_data = _sfhist_pileup_data->FindBin(puval*mod+2.5);

        if( puval*mod+2.5  > 60 ) {
            bin_max_data = 300;
        }

        val_data = _sfhist_pileup_data->Integral(bin_min_data, bin_max_data);
        val_sample = _sfhist_pileup_mc->Integral(bin_min_sample, bin_max_sample);

        num = val_data/tot_data;
        den = val_sample/tot_sample;

        weight = num/den;

        if( weight < 0.005 ) {
            std::cout << "PUweight is still zero!" << std::endl;
        }

    }
    return weight;
}

void RunModule::AddMuonSF( ModuleConfig & /*config*/ ) const { 

    OUT::mu_trigSF = 1.0;
    OUT::mu_idSF   = 1.0;
    OUT::mu_isoSF  = 1.0;

    OUT::mu_trigSFUP = 1.0;
    OUT::mu_idSFUP   = 1.0;
    OUT::mu_isoSFUP  = 1.0;

    OUT::mu_trigSFDN = 1.0;
    OUT::mu_idSFDN   = 1.0;
    OUT::mu_isoSFDN  = 1.0;

    if( OUT::isData ) {
        return;
    }

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

        OUT::mu_idSF = entry_id.val;
        OUT::mu_idSFUP = entry_id.val + entry_id.err_up;
        OUT::mu_idSFDN = entry_id.val - entry_id.err_dn;

        OUT::mu_isoSF = entry_iso.val;
        OUT::mu_isoSFUP = entry_iso.val + entry_iso.err_up;
        OUT::mu_isoSFDN = entry_iso.val - entry_iso.err_dn;


    }
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






   


        

