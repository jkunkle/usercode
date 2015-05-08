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
    CmdOptions options = ParseOptions( argc, argv );
    AnaConfig ana_config = ParseConfig( options.config_file, options );
    RunModule runmod;
    ana_config.Run(runmod, options);
    std::cout << "^_^ Finished ^_^" << std::endl;
}
void RunModule::initialize( TChain * chain, TTree * outtree, TFile *outfile,
                            const CmdOptions & options, std::vector<ModuleConfig> &configs ) {
    f = outfile; 
    f->cd(); 
    InitINTree(chain);
  hist_pt_leadph12_sieie_sublph12 = new TH2F( "pt_leadph12_sieie_sublph12", "", 30, 0.000000, 0.030000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_0 = new TH2F( "pt_leadph12_sieie_sublph12_0", "", 30, 0.000000, 0.030000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_1 = new TH2F( "pt_leadph12_sieie_sublph12_1", "", 30, 0.000000, 0.090000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_2 = new TH2F( "pt_leadph12_sieie_sublph12_2", "", 30, 0.000000, 0.090000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_3 = new TH2F( "pt_leadph12_sieie_sublph12_3", "", 30, 0.000000, 0.030000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_4 = new TH2F( "pt_leadph12_sieie_sublph12_4", "", 30, 0.000000, 0.030000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_5 = new TH2F( "pt_leadph12_sieie_sublph12_5", "", 30, 0.000000, 0.030000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_6 = new TH2F( "pt_leadph12_sieie_sublph12_6", "", 30, 0.000000, 0.030000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_7 = new TH2F( "pt_leadph12_sieie_sublph12_7", "", 30, 0.000000, 0.090000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_8 = new TH2F( "pt_leadph12_sieie_sublph12_8", "", 30, 0.000000, 0.090000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_9 = new TH2F( "pt_leadph12_sieie_sublph12_9", "", 30, 0.000000, 0.030000, 100, 0.000000, 500.000000 );

  hist_pt_leadph12_sieie_sublph12_10 = new TH2F( "pt_leadph12_sieie_sublph12_10", "", 30, 0.000000, 0.030000, 100, 0.000000, 500.000000 );

}
bool RunModule::execute( std::vector<ModuleConfig> & configs ) {
    Drawpt_leadph12_sieie_sublph12(  ); 
    Drawpt_leadph12_sieie_sublph12_0(  ); 
    Drawpt_leadph12_sieie_sublph12_1(  ); 
    Drawpt_leadph12_sieie_sublph12_2(  ); 
    Drawpt_leadph12_sieie_sublph12_3(  ); 
    Drawpt_leadph12_sieie_sublph12_4(  ); 
    Drawpt_leadph12_sieie_sublph12_5(  ); 
    Drawpt_leadph12_sieie_sublph12_6(  ); 
    Drawpt_leadph12_sieie_sublph12_7(  ); 
    Drawpt_leadph12_sieie_sublph12_8(  ); 
    Drawpt_leadph12_sieie_sublph12_9(  ); 
    Drawpt_leadph12_sieie_sublph12_10(  ); 
    return false;
}

void RunModule::finalize(  ) {
    hist_pt_leadph12_sieie_sublph12->Write(); 
    hist_pt_leadph12_sieie_sublph12_0->Write(); 
    hist_pt_leadph12_sieie_sublph12_1->Write(); 
    hist_pt_leadph12_sieie_sublph12_2->Write(); 
    hist_pt_leadph12_sieie_sublph12_3->Write(); 
    hist_pt_leadph12_sieie_sublph12_4->Write(); 
    hist_pt_leadph12_sieie_sublph12_5->Write(); 
    hist_pt_leadph12_sieie_sublph12_6->Write(); 
    hist_pt_leadph12_sieie_sublph12_7->Write(); 
    hist_pt_leadph12_sieie_sublph12_8->Write(); 
    hist_pt_leadph12_sieie_sublph12_9->Write(); 
    hist_pt_leadph12_sieie_sublph12_10->Write(); 
}

void RunModule::Drawpt_leadph12_sieie_sublph12( ) const { 
    // Original selection : mu_passtrig25_n>0 && mu_n==1 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > 15  && ph_iso1299_n == 2 && chIsoCorr_leadph12 > 1.500000 && chIsoCorr_sublph12 > 1.500000 && chIsoCorr_leadph12 < 12 && chIsoCorr_sublph12 < 12 && ph_passNeuIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[1] && phoIsoCorr_leadph12 > 0.700000 && phoIsoCorr_leadph12 < 9 && phoIsoCorr_sublph12 > 0.700000 && phoIsoCorr_sublph12 < 9  && sieie_leadph12 > 0.011000 && sieie_leadph12 < 0.029000   && isEB_leadph12 && isEB_sublph12  
     float weight = IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_HoverE12->at(1) < 0.05 && IN::dr_ph1_leadLep > 0.4 && IN::dr_ph2_leadLep > 0.4 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2 > 15  && IN::ph_iso1299_n == 2 && IN::chIsoCorr_leadph12 > 1.500000 && IN::chIsoCorr_sublph12 > 1.500000 && IN::chIsoCorr_leadph12 < 12 && IN::chIsoCorr_sublph12 < 12 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(1) && IN::phoIsoCorr_leadph12 > 0.700000 && IN::phoIsoCorr_leadph12 < 9 && IN::phoIsoCorr_sublph12 > 0.700000 && IN::phoIsoCorr_sublph12 < 9  && IN::sieie_leadph12 > 0.011000 && IN::sieie_leadph12 < 0.029000   && IN::isEB_leadph12 && IN::isEB_sublph12 ; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_0( ) const { 
    // Original selection : mu_passtrig25_n>0 && mu_n==1 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > 15  && ph_iso1299_n == 2 && chIsoCorr_leadph12 > 1.500000 && chIsoCorr_sublph12 > 1.500000 && chIsoCorr_leadph12 < 12 && chIsoCorr_sublph12 < 12 && ph_passNeuIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[1] && phoIsoCorr_leadph12 > 0.700000 && phoIsoCorr_leadph12 < 9 && phoIsoCorr_sublph12 > 0.700000 && phoIsoCorr_sublph12 < 9  && sieie_leadph12 < 0.011000   && isEB_leadph12 && isEB_sublph12  
     float weight = IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_HoverE12->at(1) < 0.05 && IN::dr_ph1_leadLep > 0.4 && IN::dr_ph2_leadLep > 0.4 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2 > 15  && IN::ph_iso1299_n == 2 && IN::chIsoCorr_leadph12 > 1.500000 && IN::chIsoCorr_sublph12 > 1.500000 && IN::chIsoCorr_leadph12 < 12 && IN::chIsoCorr_sublph12 < 12 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(1) && IN::phoIsoCorr_leadph12 > 0.700000 && IN::phoIsoCorr_leadph12 < 9 && IN::phoIsoCorr_sublph12 > 0.700000 && IN::phoIsoCorr_sublph12 < 9  && IN::sieie_leadph12 < 0.011000   && IN::isEB_leadph12 && IN::isEB_sublph12 ; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_0->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_1( ) const { 
    // Original selection : mu_passtrig25_n>0 && mu_n==1 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > 15  && ph_iso1299_n == 2 && chIsoCorr_leadph12 > 1.500000 && chIsoCorr_sublph12 > 1.200000 && chIsoCorr_leadph12 < 12 && chIsoCorr_sublph12 < 12 && ph_passNeuIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[1] && phoIsoCorr_leadph12 > 0.700000 && phoIsoCorr_leadph12 < 9 && phoIsoCorr_sublph12 > 1.000000 && phoIsoCorr_sublph12 < 9  && sieie_leadph12 > 0.011000 && sieie_leadph12 < 0.029000   && isEB_leadph12 && isEE_sublph12  
     float weight = IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_HoverE12->at(1) < 0.05 && IN::dr_ph1_leadLep > 0.4 && IN::dr_ph2_leadLep > 0.4 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2 > 15  && IN::ph_iso1299_n == 2 && IN::chIsoCorr_leadph12 > 1.500000 && IN::chIsoCorr_sublph12 > 1.200000 && IN::chIsoCorr_leadph12 < 12 && IN::chIsoCorr_sublph12 < 12 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(1) && IN::phoIsoCorr_leadph12 > 0.700000 && IN::phoIsoCorr_leadph12 < 9 && IN::phoIsoCorr_sublph12 > 1.000000 && IN::phoIsoCorr_sublph12 < 9  && IN::sieie_leadph12 > 0.011000 && IN::sieie_leadph12 < 0.029000   && IN::isEB_leadph12 && IN::isEE_sublph12 ; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_1->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_2( ) const { 
    // Original selection : mu_passtrig25_n>0 && mu_n==1 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > 15  && ph_iso1299_n == 2 && chIsoCorr_leadph12 > 1.500000 && chIsoCorr_sublph12 > 1.200000 && chIsoCorr_leadph12 < 12 && chIsoCorr_sublph12 < 12 && ph_passNeuIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[1] && phoIsoCorr_leadph12 > 0.700000 && phoIsoCorr_leadph12 < 9 && phoIsoCorr_sublph12 > 1.000000 && phoIsoCorr_sublph12 < 9  && sieie_leadph12 < 0.011000   && isEB_leadph12 && isEE_sublph12  
     float weight = IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_HoverE12->at(1) < 0.05 && IN::dr_ph1_leadLep > 0.4 && IN::dr_ph2_leadLep > 0.4 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2 > 15  && IN::ph_iso1299_n == 2 && IN::chIsoCorr_leadph12 > 1.500000 && IN::chIsoCorr_sublph12 > 1.200000 && IN::chIsoCorr_leadph12 < 12 && IN::chIsoCorr_sublph12 < 12 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(1) && IN::phoIsoCorr_leadph12 > 0.700000 && IN::phoIsoCorr_leadph12 < 9 && IN::phoIsoCorr_sublph12 > 1.000000 && IN::phoIsoCorr_sublph12 < 9  && IN::sieie_leadph12 < 0.011000   && IN::isEB_leadph12 && IN::isEE_sublph12 ; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_2->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_3( ) const { 
    // Original selection : mu_passtrig25_n>0 && mu_n==1 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > 15  && ph_iso1299_n == 2 && chIsoCorr_leadph12 > 1.200000 && chIsoCorr_sublph12 > 1.500000 && chIsoCorr_leadph12 < 12 && chIsoCorr_sublph12 < 12 && ph_passNeuIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[1] && phoIsoCorr_leadph12 > 1.000000 && phoIsoCorr_leadph12 < 9 && phoIsoCorr_sublph12 > 0.700000 && phoIsoCorr_sublph12 < 9  && sieie_leadph12 > 0.033000 && sieie_leadph12 < 0.087000   && isEE_leadph12 && isEB_sublph12  
     float weight = IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_HoverE12->at(1) < 0.05 && IN::dr_ph1_leadLep > 0.4 && IN::dr_ph2_leadLep > 0.4 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2 > 15  && IN::ph_iso1299_n == 2 && IN::chIsoCorr_leadph12 > 1.200000 && IN::chIsoCorr_sublph12 > 1.500000 && IN::chIsoCorr_leadph12 < 12 && IN::chIsoCorr_sublph12 < 12 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(1) && IN::phoIsoCorr_leadph12 > 1.000000 && IN::phoIsoCorr_leadph12 < 9 && IN::phoIsoCorr_sublph12 > 0.700000 && IN::phoIsoCorr_sublph12 < 9  && IN::sieie_leadph12 > 0.033000 && IN::sieie_leadph12 < 0.087000   && IN::isEE_leadph12 && IN::isEB_sublph12 ; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_3->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_4( ) const { 
    // Original selection : mu_passtrig25_n>0 && mu_n==1 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > 15  && ph_iso1299_n == 2 && chIsoCorr_leadph12 > 1.200000 && chIsoCorr_sublph12 > 1.500000 && chIsoCorr_leadph12 < 12 && chIsoCorr_sublph12 < 12 && ph_passNeuIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[1] && phoIsoCorr_leadph12 > 1.000000 && phoIsoCorr_leadph12 < 9 && phoIsoCorr_sublph12 > 0.700000 && phoIsoCorr_sublph12 < 9  && sieie_leadph12 < 0.033000   && isEE_leadph12 && isEB_sublph12  
     float weight = IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_HoverE12->at(1) < 0.05 && IN::dr_ph1_leadLep > 0.4 && IN::dr_ph2_leadLep > 0.4 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2 > 15  && IN::ph_iso1299_n == 2 && IN::chIsoCorr_leadph12 > 1.200000 && IN::chIsoCorr_sublph12 > 1.500000 && IN::chIsoCorr_leadph12 < 12 && IN::chIsoCorr_sublph12 < 12 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(1) && IN::phoIsoCorr_leadph12 > 1.000000 && IN::phoIsoCorr_leadph12 < 9 && IN::phoIsoCorr_sublph12 > 0.700000 && IN::phoIsoCorr_sublph12 < 9  && IN::sieie_leadph12 < 0.033000   && IN::isEE_leadph12 && IN::isEB_sublph12 ; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_4->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_5( ) const { 
    // Original selection :  mu_passtrig25_n>0 && mu_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && mt_lep_met > 40  && ph_mediumNoSIEIENoEleVeto_n >1 &&  isEB_leadph12 && isEB_sublph12  && sieie_leadph12 < 0.011000  
     float weight =  IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2>15 && IN::dr_ph1_leadLep>0.4 && IN::dr_ph2_leadLep>0.4 && IN::mt_lep_met > 40  && IN::ph_mediumNoSIEIENoEleVeto_n >1 &&  IN::isEB_leadph12 && IN::isEB_sublph12  && IN::sieie_leadph12 < 0.011000 ; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_5->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_6( ) const { 
    // Original selection :  mu_passtrig25_n>0 && mu_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && mt_lep_met > 40  && ph_mediumNoSIEIENoEleVeto_n >1 &&  isEB_leadph12 && isEB_sublph12  && sieie_leadph12 > 0.011000 && sieie_leadph12 < 0.029000 
     float weight =  IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2>15 && IN::dr_ph1_leadLep>0.4 && IN::dr_ph2_leadLep>0.4 && IN::mt_lep_met > 40  && IN::ph_mediumNoSIEIENoEleVeto_n >1 &&  IN::isEB_leadph12 && IN::isEB_sublph12  && IN::sieie_leadph12 > 0.011000 && IN::sieie_leadph12 < 0.029000; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_6->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_7( ) const { 
    // Original selection :  mu_passtrig25_n>0 && mu_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && mt_lep_met > 40  && ph_mediumNoSIEIENoEleVeto_n >1 &&  isEB_leadph12 && isEE_sublph12  && sieie_leadph12 < 0.011000  
     float weight =  IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2>15 && IN::dr_ph1_leadLep>0.4 && IN::dr_ph2_leadLep>0.4 && IN::mt_lep_met > 40  && IN::ph_mediumNoSIEIENoEleVeto_n >1 &&  IN::isEB_leadph12 && IN::isEE_sublph12  && IN::sieie_leadph12 < 0.011000 ; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_7->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_8( ) const { 
    // Original selection :  mu_passtrig25_n>0 && mu_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && mt_lep_met > 40  && ph_mediumNoSIEIENoEleVeto_n >1 &&  isEB_leadph12 && isEE_sublph12  && sieie_leadph12 > 0.011000 && sieie_leadph12 < 0.029000 
     float weight =  IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2>15 && IN::dr_ph1_leadLep>0.4 && IN::dr_ph2_leadLep>0.4 && IN::mt_lep_met > 40  && IN::ph_mediumNoSIEIENoEleVeto_n >1 &&  IN::isEB_leadph12 && IN::isEE_sublph12  && IN::sieie_leadph12 > 0.011000 && IN::sieie_leadph12 < 0.029000; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_8->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_9( ) const { 
    // Original selection :  mu_passtrig25_n>0 && mu_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && mt_lep_met > 40  && ph_mediumNoSIEIENoEleVeto_n >1 &&  isEE_leadph12 && isEB_sublph12  && sieie_leadph12 < 0.033000  
     float weight =  IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2>15 && IN::dr_ph1_leadLep>0.4 && IN::dr_ph2_leadLep>0.4 && IN::mt_lep_met > 40  && IN::ph_mediumNoSIEIENoEleVeto_n >1 &&  IN::isEE_leadph12 && IN::isEB_sublph12  && IN::sieie_leadph12 < 0.033000 ; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_9->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
void RunModule::Drawpt_leadph12_sieie_sublph12_10( ) const { 
    // Original selection :  mu_passtrig25_n>0 && mu_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && mt_lep_met > 40  && ph_mediumNoSIEIENoEleVeto_n >1 &&  isEE_leadph12 && isEB_sublph12  && sieie_leadph12 > 0.033000 && sieie_leadph12 < 0.087000 
     float weight =  IN::mu_passtrig25_n>0 && IN::mu_n==1 && IN::dr_ph1_ph2 > 0.4 && IN::m_ph1_ph2>15 && IN::dr_ph1_leadLep>0.4 && IN::dr_ph2_leadLep>0.4 && IN::mt_lep_met > 40  && IN::ph_mediumNoSIEIENoEleVeto_n >1 &&  IN::isEE_leadph12 && IN::isEB_sublph12  && IN::sieie_leadph12 > 0.033000 && IN::sieie_leadph12 < 0.087000; 
         if( weight != 0 ) { 
         hist_pt_leadph12_sieie_sublph12_10->Fill(IN::sieie_sublph12,IN::pt_leadph12, weight); 
         } 
 }
