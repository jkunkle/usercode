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
  hist_m_lepph1 = new TH1F( "m_lepph1", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_0 = new TH1F( "m_lepph1_0", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_1 = new TH1F( "m_lepph1_1", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_2 = new TH1F( "m_lepph1_2", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_3 = new TH1F( "m_lepph1_3", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_4 = new TH1F( "m_lepph1_4", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_5 = new TH1F( "m_lepph1_5", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_6 = new TH1F( "m_lepph1_6", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_7 = new TH1F( "m_lepph1_7", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_8 = new TH1F( "m_lepph1_8", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_9 = new TH1F( "m_lepph1_9", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_10 = new TH1F( "m_lepph1_10", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_11 = new TH1F( "m_lepph1_11", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_12 = new TH1F( "m_lepph1_12", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_13 = new TH1F( "m_lepph1_13", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_14 = new TH1F( "m_lepph1_14", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_15 = new TH1F( "m_lepph1_15", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_16 = new TH1F( "m_lepph1_16", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_17 = new TH1F( "m_lepph1_17", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_18 = new TH1F( "m_lepph1_18", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_19 = new TH1F( "m_lepph1_19", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_20 = new TH1F( "m_lepph1_20", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_21 = new TH1F( "m_lepph1_21", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_22 = new TH1F( "m_lepph1_22", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_23 = new TH1F( "m_lepph1_23", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_24 = new TH1F( "m_lepph1_24", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_25 = new TH1F( "m_lepph1_25", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_26 = new TH1F( "m_lepph1_26", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_27 = new TH1F( "m_lepph1_27", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_28 = new TH1F( "m_lepph1_28", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_29 = new TH1F( "m_lepph1_29", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_30 = new TH1F( "m_lepph1_30", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_31 = new TH1F( "m_lepph1_31", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_32 = new TH1F( "m_lepph1_32", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_33 = new TH1F( "m_lepph1_33", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_34 = new TH1F( "m_lepph1_34", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_35 = new TH1F( "m_lepph1_35", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_36 = new TH1F( "m_lepph1_36", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_37 = new TH1F( "m_lepph1_37", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_38 = new TH1F( "m_lepph1_38", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_39 = new TH1F( "m_lepph1_39", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_40 = new TH1F( "m_lepph1_40", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_41 = new TH1F( "m_lepph1_41", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_42 = new TH1F( "m_lepph1_42", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_43 = new TH1F( "m_lepph1_43", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_44 = new TH1F( "m_lepph1_44", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_45 = new TH1F( "m_lepph1_45", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_46 = new TH1F( "m_lepph1_46", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_47 = new TH1F( "m_lepph1_47", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_48 = new TH1F( "m_lepph1_48", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_49 = new TH1F( "m_lepph1_49", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_50 = new TH1F( "m_lepph1_50", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_51 = new TH1F( "m_lepph1_51", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_52 = new TH1F( "m_lepph1_52", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_53 = new TH1F( "m_lepph1_53", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_54 = new TH1F( "m_lepph1_54", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_55 = new TH1F( "m_lepph1_55", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_56 = new TH1F( "m_lepph1_56", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_57 = new TH1F( "m_lepph1_57", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_58 = new TH1F( "m_lepph1_58", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_59 = new TH1F( "m_lepph1_59", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_60 = new TH1F( "m_lepph1_60", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_61 = new TH1F( "m_lepph1_61", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_62 = new TH1F( "m_lepph1_62", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_63 = new TH1F( "m_lepph1_63", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_64 = new TH1F( "m_lepph1_64", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_65 = new TH1F( "m_lepph1_65", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_66 = new TH1F( "m_lepph1_66", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_67 = new TH1F( "m_lepph1_67", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_68 = new TH1F( "m_lepph1_68", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_69 = new TH1F( "m_lepph1_69", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_70 = new TH1F( "m_lepph1_70", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_71 = new TH1F( "m_lepph1_71", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_72 = new TH1F( "m_lepph1_72", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_73 = new TH1F( "m_lepph1_73", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_74 = new TH1F( "m_lepph1_74", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_75 = new TH1F( "m_lepph1_75", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_76 = new TH1F( "m_lepph1_76", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_77 = new TH1F( "m_lepph1_77", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_78 = new TH1F( "m_lepph1_78", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_79 = new TH1F( "m_lepph1_79", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_80 = new TH1F( "m_lepph1_80", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_81 = new TH1F( "m_lepph1_81", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_82 = new TH1F( "m_lepph1_82", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_83 = new TH1F( "m_lepph1_83", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_84 = new TH1F( "m_lepph1_84", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_85 = new TH1F( "m_lepph1_85", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_86 = new TH1F( "m_lepph1_86", "", 40, 40.000000, 200.000000 );

  hist_m_lepph1_87 = new TH1F( "m_lepph1_87", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_88 = new TH1F( "m_lepph1_88", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_89 = new TH1F( "m_lepph1_89", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_90 = new TH1F( "m_lepph1_90", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_91 = new TH1F( "m_lepph1_91", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_92 = new TH1F( "m_lepph1_92", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_93 = new TH1F( "m_lepph1_93", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_94 = new TH1F( "m_lepph1_94", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_95 = new TH1F( "m_lepph1_95", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_96 = new TH1F( "m_lepph1_96", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_97 = new TH1F( "m_lepph1_97", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_98 = new TH1F( "m_lepph1_98", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_99 = new TH1F( "m_lepph1_99", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_100 = new TH1F( "m_lepph1_100", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_101 = new TH1F( "m_lepph1_101", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_102 = new TH1F( "m_lepph1_102", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_103 = new TH1F( "m_lepph1_103", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_104 = new TH1F( "m_lepph1_104", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_105 = new TH1F( "m_lepph1_105", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_106 = new TH1F( "m_lepph1_106", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_107 = new TH1F( "m_lepph1_107", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_108 = new TH1F( "m_lepph1_108", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_109 = new TH1F( "m_lepph1_109", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_110 = new TH1F( "m_lepph1_110", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_111 = new TH1F( "m_lepph1_111", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_112 = new TH1F( "m_lepph1_112", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_113 = new TH1F( "m_lepph1_113", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_114 = new TH1F( "m_lepph1_114", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_115 = new TH1F( "m_lepph1_115", "", 80, 40.000000, 200.000000 );

  hist_m_lepph1_116 = new TH1F( "m_lepph1_116", "", 80, 40.000000, 200.000000 );

}
bool RunModule::execute( std::vector<ModuleConfig> & configs ) {
    Drawm_lepph1(  ); 
    Drawm_lepph1_0(  ); 
    Drawm_lepph1_1(  ); 
    Drawm_lepph1_2(  ); 
    Drawm_lepph1_3(  ); 
    Drawm_lepph1_4(  ); 
    Drawm_lepph1_5(  ); 
    Drawm_lepph1_6(  ); 
    Drawm_lepph1_7(  ); 
    Drawm_lepph1_8(  ); 
    Drawm_lepph1_9(  ); 
    Drawm_lepph1_10(  ); 
    Drawm_lepph1_11(  ); 
    Drawm_lepph1_12(  ); 
    Drawm_lepph1_13(  ); 
    Drawm_lepph1_14(  ); 
    Drawm_lepph1_15(  ); 
    Drawm_lepph1_16(  ); 
    Drawm_lepph1_17(  ); 
    Drawm_lepph1_18(  ); 
    Drawm_lepph1_19(  ); 
    Drawm_lepph1_20(  ); 
    Drawm_lepph1_21(  ); 
    Drawm_lepph1_22(  ); 
    Drawm_lepph1_23(  ); 
    Drawm_lepph1_24(  ); 
    Drawm_lepph1_25(  ); 
    Drawm_lepph1_26(  ); 
    Drawm_lepph1_27(  ); 
    Drawm_lepph1_28(  ); 
    Drawm_lepph1_29(  ); 
    Drawm_lepph1_30(  ); 
    Drawm_lepph1_31(  ); 
    Drawm_lepph1_32(  ); 
    Drawm_lepph1_33(  ); 
    Drawm_lepph1_34(  ); 
    Drawm_lepph1_35(  ); 
    Drawm_lepph1_36(  ); 
    Drawm_lepph1_37(  ); 
    Drawm_lepph1_38(  ); 
    Drawm_lepph1_39(  ); 
    Drawm_lepph1_40(  ); 
    Drawm_lepph1_41(  ); 
    Drawm_lepph1_42(  ); 
    Drawm_lepph1_43(  ); 
    Drawm_lepph1_44(  ); 
    Drawm_lepph1_45(  ); 
    Drawm_lepph1_46(  ); 
    Drawm_lepph1_47(  ); 
    Drawm_lepph1_48(  ); 
    Drawm_lepph1_49(  ); 
    Drawm_lepph1_50(  ); 
    Drawm_lepph1_51(  ); 
    Drawm_lepph1_52(  ); 
    Drawm_lepph1_53(  ); 
    Drawm_lepph1_54(  ); 
    Drawm_lepph1_55(  ); 
    Drawm_lepph1_56(  ); 
    Drawm_lepph1_57(  ); 
    Drawm_lepph1_58(  ); 
    Drawm_lepph1_59(  ); 
    Drawm_lepph1_60(  ); 
    Drawm_lepph1_61(  ); 
    Drawm_lepph1_62(  ); 
    Drawm_lepph1_63(  ); 
    Drawm_lepph1_64(  ); 
    Drawm_lepph1_65(  ); 
    Drawm_lepph1_66(  ); 
    Drawm_lepph1_67(  ); 
    Drawm_lepph1_68(  ); 
    Drawm_lepph1_69(  ); 
    Drawm_lepph1_70(  ); 
    Drawm_lepph1_71(  ); 
    Drawm_lepph1_72(  ); 
    Drawm_lepph1_73(  ); 
    Drawm_lepph1_74(  ); 
    Drawm_lepph1_75(  ); 
    Drawm_lepph1_76(  ); 
    Drawm_lepph1_77(  ); 
    Drawm_lepph1_78(  ); 
    Drawm_lepph1_79(  ); 
    Drawm_lepph1_80(  ); 
    Drawm_lepph1_81(  ); 
    Drawm_lepph1_82(  ); 
    Drawm_lepph1_83(  ); 
    Drawm_lepph1_84(  ); 
    Drawm_lepph1_85(  ); 
    Drawm_lepph1_86(  ); 
    Drawm_lepph1_87(  ); 
    Drawm_lepph1_88(  ); 
    Drawm_lepph1_89(  ); 
    Drawm_lepph1_90(  ); 
    Drawm_lepph1_91(  ); 
    Drawm_lepph1_92(  ); 
    Drawm_lepph1_93(  ); 
    Drawm_lepph1_94(  ); 
    Drawm_lepph1_95(  ); 
    Drawm_lepph1_96(  ); 
    Drawm_lepph1_97(  ); 
    Drawm_lepph1_98(  ); 
    Drawm_lepph1_99(  ); 
    Drawm_lepph1_100(  ); 
    Drawm_lepph1_101(  ); 
    Drawm_lepph1_102(  ); 
    Drawm_lepph1_103(  ); 
    Drawm_lepph1_104(  ); 
    Drawm_lepph1_105(  ); 
    Drawm_lepph1_106(  ); 
    Drawm_lepph1_107(  ); 
    Drawm_lepph1_108(  ); 
    Drawm_lepph1_109(  ); 
    Drawm_lepph1_110(  ); 
    Drawm_lepph1_111(  ); 
    Drawm_lepph1_112(  ); 
    Drawm_lepph1_113(  ); 
    Drawm_lepph1_114(  ); 
    Drawm_lepph1_115(  ); 
    Drawm_lepph1_116(  ); 
    return false;
}

void RunModule::finalize(  ) {
    hist_m_lepph1->Write(); 
    hist_m_lepph1_0->Write(); 
    hist_m_lepph1_1->Write(); 
    hist_m_lepph1_2->Write(); 
    hist_m_lepph1_3->Write(); 
    hist_m_lepph1_4->Write(); 
    hist_m_lepph1_5->Write(); 
    hist_m_lepph1_6->Write(); 
    hist_m_lepph1_7->Write(); 
    hist_m_lepph1_8->Write(); 
    hist_m_lepph1_9->Write(); 
    hist_m_lepph1_10->Write(); 
    hist_m_lepph1_11->Write(); 
    hist_m_lepph1_12->Write(); 
    hist_m_lepph1_13->Write(); 
    hist_m_lepph1_14->Write(); 
    hist_m_lepph1_15->Write(); 
    hist_m_lepph1_16->Write(); 
    hist_m_lepph1_17->Write(); 
    hist_m_lepph1_18->Write(); 
    hist_m_lepph1_19->Write(); 
    hist_m_lepph1_20->Write(); 
    hist_m_lepph1_21->Write(); 
    hist_m_lepph1_22->Write(); 
    hist_m_lepph1_23->Write(); 
    hist_m_lepph1_24->Write(); 
    hist_m_lepph1_25->Write(); 
    hist_m_lepph1_26->Write(); 
    hist_m_lepph1_27->Write(); 
    hist_m_lepph1_28->Write(); 
    hist_m_lepph1_29->Write(); 
    hist_m_lepph1_30->Write(); 
    hist_m_lepph1_31->Write(); 
    hist_m_lepph1_32->Write(); 
    hist_m_lepph1_33->Write(); 
    hist_m_lepph1_34->Write(); 
    hist_m_lepph1_35->Write(); 
    hist_m_lepph1_36->Write(); 
    hist_m_lepph1_37->Write(); 
    hist_m_lepph1_38->Write(); 
    hist_m_lepph1_39->Write(); 
    hist_m_lepph1_40->Write(); 
    hist_m_lepph1_41->Write(); 
    hist_m_lepph1_42->Write(); 
    hist_m_lepph1_43->Write(); 
    hist_m_lepph1_44->Write(); 
    hist_m_lepph1_45->Write(); 
    hist_m_lepph1_46->Write(); 
    hist_m_lepph1_47->Write(); 
    hist_m_lepph1_48->Write(); 
    hist_m_lepph1_49->Write(); 
    hist_m_lepph1_50->Write(); 
    hist_m_lepph1_51->Write(); 
    hist_m_lepph1_52->Write(); 
    hist_m_lepph1_53->Write(); 
    hist_m_lepph1_54->Write(); 
    hist_m_lepph1_55->Write(); 
    hist_m_lepph1_56->Write(); 
    hist_m_lepph1_57->Write(); 
    hist_m_lepph1_58->Write(); 
    hist_m_lepph1_59->Write(); 
    hist_m_lepph1_60->Write(); 
    hist_m_lepph1_61->Write(); 
    hist_m_lepph1_62->Write(); 
    hist_m_lepph1_63->Write(); 
    hist_m_lepph1_64->Write(); 
    hist_m_lepph1_65->Write(); 
    hist_m_lepph1_66->Write(); 
    hist_m_lepph1_67->Write(); 
    hist_m_lepph1_68->Write(); 
    hist_m_lepph1_69->Write(); 
    hist_m_lepph1_70->Write(); 
    hist_m_lepph1_71->Write(); 
    hist_m_lepph1_72->Write(); 
    hist_m_lepph1_73->Write(); 
    hist_m_lepph1_74->Write(); 
    hist_m_lepph1_75->Write(); 
    hist_m_lepph1_76->Write(); 
    hist_m_lepph1_77->Write(); 
    hist_m_lepph1_78->Write(); 
    hist_m_lepph1_79->Write(); 
    hist_m_lepph1_80->Write(); 
    hist_m_lepph1_81->Write(); 
    hist_m_lepph1_82->Write(); 
    hist_m_lepph1_83->Write(); 
    hist_m_lepph1_84->Write(); 
    hist_m_lepph1_85->Write(); 
    hist_m_lepph1_86->Write(); 
    hist_m_lepph1_87->Write(); 
    hist_m_lepph1_88->Write(); 
    hist_m_lepph1_89->Write(); 
    hist_m_lepph1_90->Write(); 
    hist_m_lepph1_91->Write(); 
    hist_m_lepph1_92->Write(); 
    hist_m_lepph1_93->Write(); 
    hist_m_lepph1_94->Write(); 
    hist_m_lepph1_95->Write(); 
    hist_m_lepph1_96->Write(); 
    hist_m_lepph1_97->Write(); 
    hist_m_lepph1_98->Write(); 
    hist_m_lepph1_99->Write(); 
    hist_m_lepph1_100->Write(); 
    hist_m_lepph1_101->Write(); 
    hist_m_lepph1_102->Write(); 
    hist_m_lepph1_103->Write(); 
    hist_m_lepph1_104->Write(); 
    hist_m_lepph1_105->Write(); 
    hist_m_lepph1_106->Write(); 
    hist_m_lepph1_107->Write(); 
    hist_m_lepph1_108->Write(); 
    hist_m_lepph1_109->Write(); 
    hist_m_lepph1_110->Write(); 
    hist_m_lepph1_111->Write(); 
    hist_m_lepph1_112->Write(); 
    hist_m_lepph1_113->Write(); 
    hist_m_lepph1_114->Write(); 
    hist_m_lepph1_115->Write(); 
    hist_m_lepph1_116->Write(); 
}

void RunModule::Drawm_lepph1( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 0.100000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_0( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 0.100000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_0->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_1( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.100000 && fabs(IN::ph_eta->at(0)) < 0.500000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_1->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_2( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.100000 && fabs(IN::ph_eta->at(0)) < 0.500000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_2->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_3( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.500000 && fabs(IN::ph_eta->at(0)) < 1.000000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_3->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_4( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.500000 && fabs(IN::ph_eta->at(0)) < 1.000000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_4->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_5( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_5->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_6( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_6->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_7( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_7->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_8( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_8->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_9( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.100000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_9->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_10( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.100000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_10->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_11( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.100000 && fabs(IN::ph_eta->at(0)) < 2.200000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_11->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_12( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.100000 && fabs(IN::ph_eta->at(0)) < 2.200000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_12->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_13( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.200000 && fabs(IN::ph_eta->at(0)) < 2.400000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_13->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_14( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.200000 && fabs(IN::ph_eta->at(0)) < 2.400000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_14->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_15( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.400000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_15->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_16( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.400000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_16->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_17( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_17->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_18( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_18->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_19( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_19->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_20( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_20->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_21( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_21->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_22( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_22->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_23( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_23->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_24( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_24->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_25( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_25->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_26( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_26->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_27( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_27->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_28( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_28->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_29( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 0.100000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_29->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_30( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 0.100000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_30->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_31( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.100000 && fabs(IN::ph_eta->at(0)) < 0.500000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_31->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_32( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.100000 && fabs(IN::ph_eta->at(0)) < 0.500000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_32->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_33( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.500000 && fabs(IN::ph_eta->at(0)) < 1.000000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_33->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_34( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.500000 && fabs(IN::ph_eta->at(0)) < 1.000000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_34->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_35( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_35->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_36( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_36->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_37( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_37->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_38( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_38->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_39( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.100000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_39->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_40( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.100000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_40->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_41( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.100000 && fabs(IN::ph_eta->at(0)) < 2.200000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_41->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_42( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.100000 && fabs(IN::ph_eta->at(0)) < 2.200000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_42->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_43( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.200000 && fabs(IN::ph_eta->at(0)) < 2.400000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_43->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_44( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.200000 && fabs(IN::ph_eta->at(0)) < 2.400000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_44->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_45( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.400000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_45->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_46( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.400000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_46->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_47( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_47->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_48( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_48->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_49( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_49->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_50( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_50->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_51( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_51->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_52( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_52->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_53( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_53->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_54( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_54->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_55( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_55->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_56( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_56->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_57( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_57->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_58( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_58->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_59( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 0.100000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_59->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_60( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 0.100000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_60->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_61( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.100000 && fabs(IN::ph_eta->at(0)) < 0.500000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_61->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_62( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.100000 && fabs(IN::ph_eta->at(0)) < 0.500000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_62->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_63( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.500000 && fabs(IN::ph_eta->at(0)) < 1.000000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_63->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_64( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.500000 && fabs(IN::ph_eta->at(0)) < 1.000000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_64->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_65( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_65->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_66( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_66->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_67( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_67->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_68( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_68->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_69( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.100000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_69->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_70( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.100000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_70->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_71( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.100000 && fabs(IN::ph_eta->at(0)) < 2.400000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_71->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_72( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.100000 && fabs(IN::ph_eta->at(0)) < 2.400000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_72->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_73( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.400000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_73->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_74( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.400000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_74->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_75( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_75->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_76( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_76->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_77( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_77->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_78( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_78->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_79( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_79->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_80( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_80->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_81( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_81->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_82( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_82->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_83( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_83->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_84( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_84->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_85( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_85->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_86( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_86->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_87( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 0.100000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_87->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_88( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 0.100000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_88->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_89( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.100000 && fabs(IN::ph_eta->at(0)) < 0.500000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_89->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_90( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.100000 && fabs(IN::ph_eta->at(0)) < 0.500000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_90->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_91( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.500000 && fabs(IN::ph_eta->at(0)) < 1.000000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_91->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_92( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.500000 && fabs(IN::ph_eta->at(0)) < 1.000000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_92->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_93( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_93->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_94( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_94->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_95( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_95->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_96( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_96->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_97( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.100000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_97->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_98( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.100000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_98->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_99( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.100000 && fabs(IN::ph_eta->at(0)) < 2.200000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_99->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_100( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.100000 && fabs(IN::ph_eta->at(0)) < 2.200000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_100->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_101( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.200000 && fabs(IN::ph_eta->at(0)) < 2.400000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_101->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_102( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.200000 && fabs(IN::ph_eta->at(0)) < 2.400000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_102->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_103( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 2.400000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_103->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_104( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 2.400000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_104->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_105( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_105->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_106( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_106->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_107( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_107->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_108( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_108->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_109( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_109->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_110( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_110->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_111( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_111->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_112( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 0.000000 && fabs(IN::ph_eta->at(0)) < 1.440000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_112->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_113( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_113->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_114( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.440000 && fabs(IN::ph_eta->at(0)) < 1.570000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_114->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_115( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==0  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40 ); 
         if( weight != 0 ) { 
         hist_m_lepph1_115->Fill(IN::m_lepph1, weight); 
         } 
 }
void RunModule::Drawm_lepph1_116( ) const { 
    float weight = IN::PUWeight * ( IN::el_passtrig_n>0 && IN::el_n==1 && IN::ph_n==1 && IN::leadPhot_leadLepDR>0.4 && IN::ph_passMedium->at(0) && IN::ph_hasPixSeed->at(0)==1  && fabs(IN::ph_eta->at(0)) > 1.570000 && fabs(IN::ph_eta->at(0)) < 2.500000 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 && IN::m_lepph1 > 40); 
         if( weight != 0 ) { 
         hist_m_lepph1_116->Fill(IN::m_lepph1, weight); 
         } 
 }
