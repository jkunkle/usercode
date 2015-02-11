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
  hist_ph_pt_26 = new TH1F( "ph_pt_26", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_27 = new TH1F( "ph_pt_27", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_28 = new TH1F( "ph_pt_28", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_29 = new TH1F( "ph_pt_29", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_30 = new TH1F( "ph_pt_30", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_31 = new TH1F( "ph_pt_31", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_32 = new TH1F( "ph_pt_32", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_33 = new TH1F( "ph_pt_33", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_34 = new TH1F( "ph_pt_34", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_35 = new TH1F( "ph_pt_35", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_36 = new TH1F( "ph_pt_36", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_37 = new TH1F( "ph_pt_37", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_38 = new TH1F( "ph_pt_38", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_39 = new TH1F( "ph_pt_39", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_40 = new TH1F( "ph_pt_40", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_41 = new TH1F( "ph_pt_41", "", 40, 0.000000, 200.000000 );

  hist_leadPhot_sublLepDR = new TH1F( "leadPhot_sublLepDR", "", 50, 0.000000, 5.000000 );

  hist_leadPhot_leadLepDR = new TH1F( "leadPhot_leadLepDR", "", 50, 0.000000, 5.000000 );

  hist_m_leplepph = new TH1F( "m_leplepph", "", 100, 0.000000, 500.000000 );

  hist_m_leplepph_m_leplep = new TH1F( "m_leplepph_m_leplep", "", 100, 0.000000, 500.000000 );

  hist_leadPhot_leadLepDR_0 = new TH1F( "leadPhot_leadLepDR_0", "", 50, 0.000000, 5.000000 );

  hist_leadPhot_leadLepDR_1 = new TH1F( "leadPhot_leadLepDR_1", "", 50, 0.000000, 5.000000 );

  hist_ph_sigmaIEIE_59 = new TH1F( "ph_sigmaIEIE_59", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_60 = new TH1F( "ph_sigmaIEIE_60", "", 50, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_61 = new TH1F( "ph_sigmaIEIE_61", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_62 = new TH1F( "ph_sigmaIEIE_62", "", 50, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_63 = new TH1F( "ph_sigmaIEIE_63", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_64 = new TH1F( "ph_sigmaIEIE_64", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_65 = new TH1F( "ph_sigmaIEIE_65", "", 50, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_66 = new TH1F( "ph_sigmaIEIE_66", "", 50, 0.000000, 0.100000 );

  hist_leadPhot_sublLepDR_0 = new TH1F( "leadPhot_sublLepDR_0", "", 50, 0.000000, 5.000000 );

  hist_leadPhot_leadLepDR_2 = new TH1F( "leadPhot_leadLepDR_2", "", 50, 0.000000, 5.000000 );

  hist_ph_sigmaIEIE_67 = new TH1F( "ph_sigmaIEIE_67", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_68 = new TH1F( "ph_sigmaIEIE_68", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_69 = new TH1F( "ph_sigmaIEIE_69", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_70 = new TH1F( "ph_sigmaIEIE_70", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_71 = new TH1F( "ph_sigmaIEIE_71", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_72 = new TH1F( "ph_sigmaIEIE_72", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_73 = new TH1F( "ph_sigmaIEIE_73", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_74 = new TH1F( "ph_sigmaIEIE_74", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_75 = new TH1F( "ph_sigmaIEIE_75", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_76 = new TH1F( "ph_sigmaIEIE_76", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_77 = new TH1F( "ph_sigmaIEIE_77", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_78 = new TH1F( "ph_sigmaIEIE_78", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_79 = new TH1F( "ph_sigmaIEIE_79", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_80 = new TH1F( "ph_sigmaIEIE_80", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_81 = new TH1F( "ph_sigmaIEIE_81", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_82 = new TH1F( "ph_sigmaIEIE_82", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_83 = new TH1F( "ph_sigmaIEIE_83", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_84 = new TH1F( "ph_sigmaIEIE_84", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_85 = new TH1F( "ph_sigmaIEIE_85", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_86 = new TH1F( "ph_sigmaIEIE_86", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_87 = new TH1F( "ph_sigmaIEIE_87", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_88 = new TH1F( "ph_sigmaIEIE_88", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_89 = new TH1F( "ph_sigmaIEIE_89", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_90 = new TH1F( "ph_sigmaIEIE_90", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_91 = new TH1F( "ph_sigmaIEIE_91", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_92 = new TH1F( "ph_sigmaIEIE_92", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_93 = new TH1F( "ph_sigmaIEIE_93", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_94 = new TH1F( "ph_sigmaIEIE_94", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_95 = new TH1F( "ph_sigmaIEIE_95", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_96 = new TH1F( "ph_sigmaIEIE_96", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_97 = new TH1F( "ph_sigmaIEIE_97", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_98 = new TH1F( "ph_sigmaIEIE_98", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_99 = new TH1F( "ph_sigmaIEIE_99", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_100 = new TH1F( "ph_sigmaIEIE_100", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_101 = new TH1F( "ph_sigmaIEIE_101", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_102 = new TH1F( "ph_sigmaIEIE_102", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_103 = new TH1F( "ph_sigmaIEIE_103", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_104 = new TH1F( "ph_sigmaIEIE_104", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_105 = new TH1F( "ph_sigmaIEIE_105", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_106 = new TH1F( "ph_sigmaIEIE_106", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_107 = new TH1F( "ph_sigmaIEIE_107", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_108 = new TH1F( "ph_sigmaIEIE_108", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_109 = new TH1F( "ph_sigmaIEIE_109", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_110 = new TH1F( "ph_sigmaIEIE_110", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_111 = new TH1F( "ph_sigmaIEIE_111", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_112 = new TH1F( "ph_sigmaIEIE_112", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_113 = new TH1F( "ph_sigmaIEIE_113", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_114 = new TH1F( "ph_sigmaIEIE_114", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_115 = new TH1F( "ph_sigmaIEIE_115", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_116 = new TH1F( "ph_sigmaIEIE_116", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_117 = new TH1F( "ph_sigmaIEIE_117", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_118 = new TH1F( "ph_sigmaIEIE_118", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_119 = new TH1F( "ph_sigmaIEIE_119", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_120 = new TH1F( "ph_sigmaIEIE_120", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_121 = new TH1F( "ph_sigmaIEIE_121", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_122 = new TH1F( "ph_sigmaIEIE_122", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_123 = new TH1F( "ph_sigmaIEIE_123", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_124 = new TH1F( "ph_sigmaIEIE_124", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_125 = new TH1F( "ph_sigmaIEIE_125", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_126 = new TH1F( "ph_sigmaIEIE_126", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_127 = new TH1F( "ph_sigmaIEIE_127", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_128 = new TH1F( "ph_sigmaIEIE_128", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_129 = new TH1F( "ph_sigmaIEIE_129", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_130 = new TH1F( "ph_sigmaIEIE_130", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_131 = new TH1F( "ph_sigmaIEIE_131", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_132 = new TH1F( "ph_sigmaIEIE_132", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_133 = new TH1F( "ph_sigmaIEIE_133", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_134 = new TH1F( "ph_sigmaIEIE_134", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_135 = new TH1F( "ph_sigmaIEIE_135", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_136 = new TH1F( "ph_sigmaIEIE_136", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_137 = new TH1F( "ph_sigmaIEIE_137", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_138 = new TH1F( "ph_sigmaIEIE_138", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_139 = new TH1F( "ph_sigmaIEIE_139", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_140 = new TH1F( "ph_sigmaIEIE_140", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_141 = new TH1F( "ph_sigmaIEIE_141", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_142 = new TH1F( "ph_sigmaIEIE_142", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_143 = new TH1F( "ph_sigmaIEIE_143", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_144 = new TH1F( "ph_sigmaIEIE_144", "", 40, 0.000000, 0.100000 );

  hist_ph_pt_42 = new TH1F( "ph_pt_42", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_43 = new TH1F( "ph_pt_43", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_44 = new TH1F( "ph_pt_44", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_45 = new TH1F( "ph_pt_45", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_46 = new TH1F( "ph_pt_46", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_47 = new TH1F( "ph_pt_47", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_48 = new TH1F( "ph_pt_48", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_49 = new TH1F( "ph_pt_49", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_50 = new TH1F( "ph_pt_50", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_51 = new TH1F( "ph_pt_51", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_52 = new TH1F( "ph_pt_52", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_53 = new TH1F( "ph_pt_53", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_54 = new TH1F( "ph_pt_54", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_55 = new TH1F( "ph_pt_55", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_56 = new TH1F( "ph_pt_56", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_57 = new TH1F( "ph_pt_57", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_58 = new TH1F( "ph_pt_58", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_59 = new TH1F( "ph_pt_59", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_60 = new TH1F( "ph_pt_60", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_61 = new TH1F( "ph_pt_61", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_62 = new TH1F( "ph_pt_62", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_63 = new TH1F( "ph_pt_63", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_64 = new TH1F( "ph_pt_64", "", 40, 0.000000, 200.000000 );

  hist_ph_pt_65 = new TH1F( "ph_pt_65", "", 40, 0.000000, 200.000000 );

  hist_ph_sigmaIEIE_145 = new TH1F( "ph_sigmaIEIE_145", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_146 = new TH1F( "ph_sigmaIEIE_146", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_147 = new TH1F( "ph_sigmaIEIE_147", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_148 = new TH1F( "ph_sigmaIEIE_148", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_149 = new TH1F( "ph_sigmaIEIE_149", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_150 = new TH1F( "ph_sigmaIEIE_150", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_151 = new TH1F( "ph_sigmaIEIE_151", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_152 = new TH1F( "ph_sigmaIEIE_152", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_153 = new TH1F( "ph_sigmaIEIE_153", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_154 = new TH1F( "ph_sigmaIEIE_154", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_155 = new TH1F( "ph_sigmaIEIE_155", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_156 = new TH1F( "ph_sigmaIEIE_156", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_157 = new TH1F( "ph_sigmaIEIE_157", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_158 = new TH1F( "ph_sigmaIEIE_158", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_159 = new TH1F( "ph_sigmaIEIE_159", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_160 = new TH1F( "ph_sigmaIEIE_160", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_161 = new TH1F( "ph_sigmaIEIE_161", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_162 = new TH1F( "ph_sigmaIEIE_162", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_163 = new TH1F( "ph_sigmaIEIE_163", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_164 = new TH1F( "ph_sigmaIEIE_164", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_165 = new TH1F( "ph_sigmaIEIE_165", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_166 = new TH1F( "ph_sigmaIEIE_166", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_167 = new TH1F( "ph_sigmaIEIE_167", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_168 = new TH1F( "ph_sigmaIEIE_168", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_169 = new TH1F( "ph_sigmaIEIE_169", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_170 = new TH1F( "ph_sigmaIEIE_170", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_171 = new TH1F( "ph_sigmaIEIE_171", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_172 = new TH1F( "ph_sigmaIEIE_172", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_173 = new TH1F( "ph_sigmaIEIE_173", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_174 = new TH1F( "ph_sigmaIEIE_174", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_175 = new TH1F( "ph_sigmaIEIE_175", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_176 = new TH1F( "ph_sigmaIEIE_176", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_177 = new TH1F( "ph_sigmaIEIE_177", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_178 = new TH1F( "ph_sigmaIEIE_178", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_179 = new TH1F( "ph_sigmaIEIE_179", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_180 = new TH1F( "ph_sigmaIEIE_180", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_181 = new TH1F( "ph_sigmaIEIE_181", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_182 = new TH1F( "ph_sigmaIEIE_182", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_183 = new TH1F( "ph_sigmaIEIE_183", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_184 = new TH1F( "ph_sigmaIEIE_184", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_185 = new TH1F( "ph_sigmaIEIE_185", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_186 = new TH1F( "ph_sigmaIEIE_186", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_187 = new TH1F( "ph_sigmaIEIE_187", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_188 = new TH1F( "ph_sigmaIEIE_188", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_189 = new TH1F( "ph_sigmaIEIE_189", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_190 = new TH1F( "ph_sigmaIEIE_190", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_191 = new TH1F( "ph_sigmaIEIE_191", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_192 = new TH1F( "ph_sigmaIEIE_192", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_193 = new TH1F( "ph_sigmaIEIE_193", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_194 = new TH1F( "ph_sigmaIEIE_194", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_195 = new TH1F( "ph_sigmaIEIE_195", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_196 = new TH1F( "ph_sigmaIEIE_196", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_197 = new TH1F( "ph_sigmaIEIE_197", "", 60, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_198 = new TH1F( "ph_sigmaIEIE_198", "", 60, 0.000000, 0.030000 );

 double ph_sigmaIEIE_199xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_199 = new TH1F( "ph_sigmaIEIE_199", "", 2, ph_sigmaIEIE_199xarr );

 double ph_sigmaIEIE_200xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_200 = new TH1F( "ph_sigmaIEIE_200", "", 2, ph_sigmaIEIE_200xarr );

 double ph_sigmaIEIE_201xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_201 = new TH1F( "ph_sigmaIEIE_201", "", 2, ph_sigmaIEIE_201xarr );

 double ph_sigmaIEIE_202xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_202 = new TH1F( "ph_sigmaIEIE_202", "", 2, ph_sigmaIEIE_202xarr );

 double ph_sigmaIEIE_203xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_203 = new TH1F( "ph_sigmaIEIE_203", "", 2, ph_sigmaIEIE_203xarr );

 double ph_sigmaIEIE_204xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_204 = new TH1F( "ph_sigmaIEIE_204", "", 2, ph_sigmaIEIE_204xarr );

 double ph_sigmaIEIE_205xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_205 = new TH1F( "ph_sigmaIEIE_205", "", 2, ph_sigmaIEIE_205xarr );

 double ph_sigmaIEIE_206xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_206 = new TH1F( "ph_sigmaIEIE_206", "", 2, ph_sigmaIEIE_206xarr );

 double ph_sigmaIEIE_207xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_207 = new TH1F( "ph_sigmaIEIE_207", "", 2, ph_sigmaIEIE_207xarr );

 double ph_sigmaIEIE_208xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_208 = new TH1F( "ph_sigmaIEIE_208", "", 2, ph_sigmaIEIE_208xarr );

 double ph_sigmaIEIE_209xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_209 = new TH1F( "ph_sigmaIEIE_209", "", 2, ph_sigmaIEIE_209xarr );

 double ph_sigmaIEIE_210xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_210 = new TH1F( "ph_sigmaIEIE_210", "", 2, ph_sigmaIEIE_210xarr );

 double ph_sigmaIEIE_211xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_211 = new TH1F( "ph_sigmaIEIE_211", "", 2, ph_sigmaIEIE_211xarr );

 double ph_sigmaIEIE_212xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_212 = new TH1F( "ph_sigmaIEIE_212", "", 2, ph_sigmaIEIE_212xarr );

 double ph_sigmaIEIE_213xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_213 = new TH1F( "ph_sigmaIEIE_213", "", 2, ph_sigmaIEIE_213xarr );

 double ph_sigmaIEIE_214xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_214 = new TH1F( "ph_sigmaIEIE_214", "", 2, ph_sigmaIEIE_214xarr );

 double ph_sigmaIEIE_215xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_215 = new TH1F( "ph_sigmaIEIE_215", "", 2, ph_sigmaIEIE_215xarr );

 double ph_sigmaIEIE_216xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_216 = new TH1F( "ph_sigmaIEIE_216", "", 2, ph_sigmaIEIE_216xarr );

 double ph_sigmaIEIE_217xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_217 = new TH1F( "ph_sigmaIEIE_217", "", 2, ph_sigmaIEIE_217xarr );

 double ph_sigmaIEIE_218xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_218 = new TH1F( "ph_sigmaIEIE_218", "", 2, ph_sigmaIEIE_218xarr );

 double ph_sigmaIEIE_219xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_219 = new TH1F( "ph_sigmaIEIE_219", "", 2, ph_sigmaIEIE_219xarr );

 double ph_sigmaIEIE_220xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_220 = new TH1F( "ph_sigmaIEIE_220", "", 2, ph_sigmaIEIE_220xarr );

 double ph_sigmaIEIE_221xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_221 = new TH1F( "ph_sigmaIEIE_221", "", 2, ph_sigmaIEIE_221xarr );

 double ph_sigmaIEIE_222xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_222 = new TH1F( "ph_sigmaIEIE_222", "", 2, ph_sigmaIEIE_222xarr );

 double ph_sigmaIEIE_223xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_223 = new TH1F( "ph_sigmaIEIE_223", "", 2, ph_sigmaIEIE_223xarr );

 double ph_sigmaIEIE_224xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_224 = new TH1F( "ph_sigmaIEIE_224", "", 2, ph_sigmaIEIE_224xarr );

 double ph_sigmaIEIE_225xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_225 = new TH1F( "ph_sigmaIEIE_225", "", 2, ph_sigmaIEIE_225xarr );

 double ph_sigmaIEIE_226xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_226 = new TH1F( "ph_sigmaIEIE_226", "", 2, ph_sigmaIEIE_226xarr );

 double ph_sigmaIEIE_227xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_227 = new TH1F( "ph_sigmaIEIE_227", "", 2, ph_sigmaIEIE_227xarr );

 double ph_sigmaIEIE_228xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_228 = new TH1F( "ph_sigmaIEIE_228", "", 2, ph_sigmaIEIE_228xarr );

 double ph_sigmaIEIE_229xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_229 = new TH1F( "ph_sigmaIEIE_229", "", 2, ph_sigmaIEIE_229xarr );

 double ph_sigmaIEIE_230xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_230 = new TH1F( "ph_sigmaIEIE_230", "", 2, ph_sigmaIEIE_230xarr );

 double ph_sigmaIEIE_231xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_231 = new TH1F( "ph_sigmaIEIE_231", "", 2, ph_sigmaIEIE_231xarr );

 double ph_sigmaIEIE_232xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_232 = new TH1F( "ph_sigmaIEIE_232", "", 2, ph_sigmaIEIE_232xarr );

 double ph_sigmaIEIE_233xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_233 = new TH1F( "ph_sigmaIEIE_233", "", 2, ph_sigmaIEIE_233xarr );

 double ph_sigmaIEIE_234xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_234 = new TH1F( "ph_sigmaIEIE_234", "", 2, ph_sigmaIEIE_234xarr );

 double ph_sigmaIEIE_235xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_235 = new TH1F( "ph_sigmaIEIE_235", "", 2, ph_sigmaIEIE_235xarr );

 double ph_sigmaIEIE_236xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_236 = new TH1F( "ph_sigmaIEIE_236", "", 2, ph_sigmaIEIE_236xarr );

 double ph_sigmaIEIE_237xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_237 = new TH1F( "ph_sigmaIEIE_237", "", 2, ph_sigmaIEIE_237xarr );

 double ph_sigmaIEIE_238xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_238 = new TH1F( "ph_sigmaIEIE_238", "", 2, ph_sigmaIEIE_238xarr );

 double ph_sigmaIEIE_239xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_239 = new TH1F( "ph_sigmaIEIE_239", "", 2, ph_sigmaIEIE_239xarr );

 double ph_sigmaIEIE_240xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_240 = new TH1F( "ph_sigmaIEIE_240", "", 2, ph_sigmaIEIE_240xarr );

 double ph_sigmaIEIE_241xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_241 = new TH1F( "ph_sigmaIEIE_241", "", 2, ph_sigmaIEIE_241xarr );

 double ph_sigmaIEIE_242xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_242 = new TH1F( "ph_sigmaIEIE_242", "", 2, ph_sigmaIEIE_242xarr );

 double ph_sigmaIEIE_243xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_243 = new TH1F( "ph_sigmaIEIE_243", "", 2, ph_sigmaIEIE_243xarr );

 double ph_sigmaIEIE_244xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_244 = new TH1F( "ph_sigmaIEIE_244", "", 2, ph_sigmaIEIE_244xarr );

 double ph_sigmaIEIE_245xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_245 = new TH1F( "ph_sigmaIEIE_245", "", 2, ph_sigmaIEIE_245xarr );

 double ph_sigmaIEIE_246xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_246 = new TH1F( "ph_sigmaIEIE_246", "", 2, ph_sigmaIEIE_246xarr );

 double ph_sigmaIEIE_247xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_247 = new TH1F( "ph_sigmaIEIE_247", "", 2, ph_sigmaIEIE_247xarr );

 double ph_sigmaIEIE_248xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_248 = new TH1F( "ph_sigmaIEIE_248", "", 2, ph_sigmaIEIE_248xarr );

 double ph_sigmaIEIE_249xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_249 = new TH1F( "ph_sigmaIEIE_249", "", 2, ph_sigmaIEIE_249xarr );

 double ph_sigmaIEIE_250xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_250 = new TH1F( "ph_sigmaIEIE_250", "", 2, ph_sigmaIEIE_250xarr );

 double ph_sigmaIEIE_251xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_251 = new TH1F( "ph_sigmaIEIE_251", "", 2, ph_sigmaIEIE_251xarr );

 double ph_sigmaIEIE_252xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_252 = new TH1F( "ph_sigmaIEIE_252", "", 2, ph_sigmaIEIE_252xarr );

  hist_ph_sigmaIEIE_253 = new TH1F( "ph_sigmaIEIE_253", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_254 = new TH1F( "ph_sigmaIEIE_254", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_255 = new TH1F( "ph_sigmaIEIE_255", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_256 = new TH1F( "ph_sigmaIEIE_256", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_257 = new TH1F( "ph_sigmaIEIE_257", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_258 = new TH1F( "ph_sigmaIEIE_258", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_259 = new TH1F( "ph_sigmaIEIE_259", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_260 = new TH1F( "ph_sigmaIEIE_260", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_261 = new TH1F( "ph_sigmaIEIE_261", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_262 = new TH1F( "ph_sigmaIEIE_262", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_263 = new TH1F( "ph_sigmaIEIE_263", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_264 = new TH1F( "ph_sigmaIEIE_264", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_265 = new TH1F( "ph_sigmaIEIE_265", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_266 = new TH1F( "ph_sigmaIEIE_266", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_267 = new TH1F( "ph_sigmaIEIE_267", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_268 = new TH1F( "ph_sigmaIEIE_268", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_269 = new TH1F( "ph_sigmaIEIE_269", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_270 = new TH1F( "ph_sigmaIEIE_270", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_271 = new TH1F( "ph_sigmaIEIE_271", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_272 = new TH1F( "ph_sigmaIEIE_272", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_273 = new TH1F( "ph_sigmaIEIE_273", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_274 = new TH1F( "ph_sigmaIEIE_274", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_275 = new TH1F( "ph_sigmaIEIE_275", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_276 = new TH1F( "ph_sigmaIEIE_276", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_277 = new TH1F( "ph_sigmaIEIE_277", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_278 = new TH1F( "ph_sigmaIEIE_278", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_279 = new TH1F( "ph_sigmaIEIE_279", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_280 = new TH1F( "ph_sigmaIEIE_280", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_281 = new TH1F( "ph_sigmaIEIE_281", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_282 = new TH1F( "ph_sigmaIEIE_282", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_283 = new TH1F( "ph_sigmaIEIE_283", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_284 = new TH1F( "ph_sigmaIEIE_284", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_285 = new TH1F( "ph_sigmaIEIE_285", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_286 = new TH1F( "ph_sigmaIEIE_286", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_287 = new TH1F( "ph_sigmaIEIE_287", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_288 = new TH1F( "ph_sigmaIEIE_288", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_289 = new TH1F( "ph_sigmaIEIE_289", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_290 = new TH1F( "ph_sigmaIEIE_290", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_291 = new TH1F( "ph_sigmaIEIE_291", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_292 = new TH1F( "ph_sigmaIEIE_292", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_293 = new TH1F( "ph_sigmaIEIE_293", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_294 = new TH1F( "ph_sigmaIEIE_294", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_295 = new TH1F( "ph_sigmaIEIE_295", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_296 = new TH1F( "ph_sigmaIEIE_296", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_297 = new TH1F( "ph_sigmaIEIE_297", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_298 = new TH1F( "ph_sigmaIEIE_298", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_299 = new TH1F( "ph_sigmaIEIE_299", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_300 = new TH1F( "ph_sigmaIEIE_300", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_301 = new TH1F( "ph_sigmaIEIE_301", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_302 = new TH1F( "ph_sigmaIEIE_302", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_303 = new TH1F( "ph_sigmaIEIE_303", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_304 = new TH1F( "ph_sigmaIEIE_304", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_305 = new TH1F( "ph_sigmaIEIE_305", "", 40, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_306 = new TH1F( "ph_sigmaIEIE_306", "", 40, 0.000000, 0.100000 );

 double ph_sigmaIEIE_307xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_307 = new TH1F( "ph_sigmaIEIE_307", "", 2, ph_sigmaIEIE_307xarr );

 double ph_sigmaIEIE_308xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_308 = new TH1F( "ph_sigmaIEIE_308", "", 2, ph_sigmaIEIE_308xarr );

 double ph_sigmaIEIE_309xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_309 = new TH1F( "ph_sigmaIEIE_309", "", 2, ph_sigmaIEIE_309xarr );

 double ph_sigmaIEIE_310xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_310 = new TH1F( "ph_sigmaIEIE_310", "", 2, ph_sigmaIEIE_310xarr );

 double ph_sigmaIEIE_311xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_311 = new TH1F( "ph_sigmaIEIE_311", "", 2, ph_sigmaIEIE_311xarr );

 double ph_sigmaIEIE_312xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_312 = new TH1F( "ph_sigmaIEIE_312", "", 2, ph_sigmaIEIE_312xarr );

 double ph_sigmaIEIE_313xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_313 = new TH1F( "ph_sigmaIEIE_313", "", 2, ph_sigmaIEIE_313xarr );

 double ph_sigmaIEIE_314xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_314 = new TH1F( "ph_sigmaIEIE_314", "", 2, ph_sigmaIEIE_314xarr );

 double ph_sigmaIEIE_315xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_315 = new TH1F( "ph_sigmaIEIE_315", "", 2, ph_sigmaIEIE_315xarr );

 double ph_sigmaIEIE_316xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_316 = new TH1F( "ph_sigmaIEIE_316", "", 2, ph_sigmaIEIE_316xarr );

 double ph_sigmaIEIE_317xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_317 = new TH1F( "ph_sigmaIEIE_317", "", 2, ph_sigmaIEIE_317xarr );

 double ph_sigmaIEIE_318xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_318 = new TH1F( "ph_sigmaIEIE_318", "", 2, ph_sigmaIEIE_318xarr );

 double ph_sigmaIEIE_319xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_319 = new TH1F( "ph_sigmaIEIE_319", "", 2, ph_sigmaIEIE_319xarr );

 double ph_sigmaIEIE_320xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_320 = new TH1F( "ph_sigmaIEIE_320", "", 2, ph_sigmaIEIE_320xarr );

 double ph_sigmaIEIE_321xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_321 = new TH1F( "ph_sigmaIEIE_321", "", 2, ph_sigmaIEIE_321xarr );

 double ph_sigmaIEIE_322xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_322 = new TH1F( "ph_sigmaIEIE_322", "", 2, ph_sigmaIEIE_322xarr );

 double ph_sigmaIEIE_323xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_323 = new TH1F( "ph_sigmaIEIE_323", "", 2, ph_sigmaIEIE_323xarr );

 double ph_sigmaIEIE_324xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_324 = new TH1F( "ph_sigmaIEIE_324", "", 2, ph_sigmaIEIE_324xarr );

 double ph_sigmaIEIE_325xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_325 = new TH1F( "ph_sigmaIEIE_325", "", 2, ph_sigmaIEIE_325xarr );

 double ph_sigmaIEIE_326xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_326 = new TH1F( "ph_sigmaIEIE_326", "", 2, ph_sigmaIEIE_326xarr );

 double ph_sigmaIEIE_327xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_327 = new TH1F( "ph_sigmaIEIE_327", "", 2, ph_sigmaIEIE_327xarr );

 double ph_sigmaIEIE_328xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_328 = new TH1F( "ph_sigmaIEIE_328", "", 2, ph_sigmaIEIE_328xarr );

 double ph_sigmaIEIE_329xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_329 = new TH1F( "ph_sigmaIEIE_329", "", 2, ph_sigmaIEIE_329xarr );

 double ph_sigmaIEIE_330xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_330 = new TH1F( "ph_sigmaIEIE_330", "", 2, ph_sigmaIEIE_330xarr );

 double ph_sigmaIEIE_331xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_331 = new TH1F( "ph_sigmaIEIE_331", "", 2, ph_sigmaIEIE_331xarr );

 double ph_sigmaIEIE_332xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_332 = new TH1F( "ph_sigmaIEIE_332", "", 2, ph_sigmaIEIE_332xarr );

 double ph_sigmaIEIE_333xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_333 = new TH1F( "ph_sigmaIEIE_333", "", 2, ph_sigmaIEIE_333xarr );

 double ph_sigmaIEIE_334xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_334 = new TH1F( "ph_sigmaIEIE_334", "", 2, ph_sigmaIEIE_334xarr );

 double ph_sigmaIEIE_335xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_335 = new TH1F( "ph_sigmaIEIE_335", "", 2, ph_sigmaIEIE_335xarr );

 double ph_sigmaIEIE_336xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_336 = new TH1F( "ph_sigmaIEIE_336", "", 2, ph_sigmaIEIE_336xarr );

 double ph_sigmaIEIE_337xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_337 = new TH1F( "ph_sigmaIEIE_337", "", 2, ph_sigmaIEIE_337xarr );

 double ph_sigmaIEIE_338xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_338 = new TH1F( "ph_sigmaIEIE_338", "", 2, ph_sigmaIEIE_338xarr );

 double ph_sigmaIEIE_339xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_339 = new TH1F( "ph_sigmaIEIE_339", "", 2, ph_sigmaIEIE_339xarr );

 double ph_sigmaIEIE_340xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_340 = new TH1F( "ph_sigmaIEIE_340", "", 2, ph_sigmaIEIE_340xarr );

 double ph_sigmaIEIE_341xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_341 = new TH1F( "ph_sigmaIEIE_341", "", 2, ph_sigmaIEIE_341xarr );

 double ph_sigmaIEIE_342xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_342 = new TH1F( "ph_sigmaIEIE_342", "", 2, ph_sigmaIEIE_342xarr );

 double ph_sigmaIEIE_343xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_343 = new TH1F( "ph_sigmaIEIE_343", "", 2, ph_sigmaIEIE_343xarr );

 double ph_sigmaIEIE_344xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_344 = new TH1F( "ph_sigmaIEIE_344", "", 2, ph_sigmaIEIE_344xarr );

 double ph_sigmaIEIE_345xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_345 = new TH1F( "ph_sigmaIEIE_345", "", 2, ph_sigmaIEIE_345xarr );

 double ph_sigmaIEIE_346xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_346 = new TH1F( "ph_sigmaIEIE_346", "", 2, ph_sigmaIEIE_346xarr );

 double ph_sigmaIEIE_347xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_347 = new TH1F( "ph_sigmaIEIE_347", "", 2, ph_sigmaIEIE_347xarr );

 double ph_sigmaIEIE_348xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_348 = new TH1F( "ph_sigmaIEIE_348", "", 2, ph_sigmaIEIE_348xarr );

 double ph_sigmaIEIE_349xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_349 = new TH1F( "ph_sigmaIEIE_349", "", 2, ph_sigmaIEIE_349xarr );

 double ph_sigmaIEIE_350xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_350 = new TH1F( "ph_sigmaIEIE_350", "", 2, ph_sigmaIEIE_350xarr );

 double ph_sigmaIEIE_351xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_351 = new TH1F( "ph_sigmaIEIE_351", "", 2, ph_sigmaIEIE_351xarr );

 double ph_sigmaIEIE_352xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_352 = new TH1F( "ph_sigmaIEIE_352", "", 2, ph_sigmaIEIE_352xarr );

 double ph_sigmaIEIE_353xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_353 = new TH1F( "ph_sigmaIEIE_353", "", 2, ph_sigmaIEIE_353xarr );

 double ph_sigmaIEIE_354xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_354 = new TH1F( "ph_sigmaIEIE_354", "", 2, ph_sigmaIEIE_354xarr );

 double ph_sigmaIEIE_355xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_355 = new TH1F( "ph_sigmaIEIE_355", "", 2, ph_sigmaIEIE_355xarr );

 double ph_sigmaIEIE_356xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_356 = new TH1F( "ph_sigmaIEIE_356", "", 2, ph_sigmaIEIE_356xarr );

 double ph_sigmaIEIE_357xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_357 = new TH1F( "ph_sigmaIEIE_357", "", 2, ph_sigmaIEIE_357xarr );

 double ph_sigmaIEIE_358xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_358 = new TH1F( "ph_sigmaIEIE_358", "", 2, ph_sigmaIEIE_358xarr );

 double ph_sigmaIEIE_359xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_359 = new TH1F( "ph_sigmaIEIE_359", "", 2, ph_sigmaIEIE_359xarr );

 double ph_sigmaIEIE_360xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_360 = new TH1F( "ph_sigmaIEIE_360", "", 2, ph_sigmaIEIE_360xarr );

  hist_ph_sigmaIEIE_361 = new TH1F( "ph_sigmaIEIE_361", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_362 = new TH1F( "ph_sigmaIEIE_362", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_363 = new TH1F( "ph_sigmaIEIE_363", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_364 = new TH1F( "ph_sigmaIEIE_364", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_365 = new TH1F( "ph_sigmaIEIE_365", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_366 = new TH1F( "ph_sigmaIEIE_366", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_367 = new TH1F( "ph_sigmaIEIE_367", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_368 = new TH1F( "ph_sigmaIEIE_368", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_369 = new TH1F( "ph_sigmaIEIE_369", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_370 = new TH1F( "ph_sigmaIEIE_370", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_371 = new TH1F( "ph_sigmaIEIE_371", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_372 = new TH1F( "ph_sigmaIEIE_372", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_373 = new TH1F( "ph_sigmaIEIE_373", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_374 = new TH1F( "ph_sigmaIEIE_374", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_375 = new TH1F( "ph_sigmaIEIE_375", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_376 = new TH1F( "ph_sigmaIEIE_376", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_377 = new TH1F( "ph_sigmaIEIE_377", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_378 = new TH1F( "ph_sigmaIEIE_378", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_379 = new TH1F( "ph_sigmaIEIE_379", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_380 = new TH1F( "ph_sigmaIEIE_380", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_381 = new TH1F( "ph_sigmaIEIE_381", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_382 = new TH1F( "ph_sigmaIEIE_382", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_383 = new TH1F( "ph_sigmaIEIE_383", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_384 = new TH1F( "ph_sigmaIEIE_384", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_385 = new TH1F( "ph_sigmaIEIE_385", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_386 = new TH1F( "ph_sigmaIEIE_386", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_387 = new TH1F( "ph_sigmaIEIE_387", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_388 = new TH1F( "ph_sigmaIEIE_388", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_389 = new TH1F( "ph_sigmaIEIE_389", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_390 = new TH1F( "ph_sigmaIEIE_390", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_391 = new TH1F( "ph_sigmaIEIE_391", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_392 = new TH1F( "ph_sigmaIEIE_392", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_393 = new TH1F( "ph_sigmaIEIE_393", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_394 = new TH1F( "ph_sigmaIEIE_394", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_395 = new TH1F( "ph_sigmaIEIE_395", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_396 = new TH1F( "ph_sigmaIEIE_396", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_397 = new TH1F( "ph_sigmaIEIE_397", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_398 = new TH1F( "ph_sigmaIEIE_398", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_399 = new TH1F( "ph_sigmaIEIE_399", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_400 = new TH1F( "ph_sigmaIEIE_400", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_401 = new TH1F( "ph_sigmaIEIE_401", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_402 = new TH1F( "ph_sigmaIEIE_402", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_403 = new TH1F( "ph_sigmaIEIE_403", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_404 = new TH1F( "ph_sigmaIEIE_404", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_405 = new TH1F( "ph_sigmaIEIE_405", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_406 = new TH1F( "ph_sigmaIEIE_406", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_407 = new TH1F( "ph_sigmaIEIE_407", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_408 = new TH1F( "ph_sigmaIEIE_408", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_409 = new TH1F( "ph_sigmaIEIE_409", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_410 = new TH1F( "ph_sigmaIEIE_410", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_411 = new TH1F( "ph_sigmaIEIE_411", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_412 = new TH1F( "ph_sigmaIEIE_412", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_413 = new TH1F( "ph_sigmaIEIE_413", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_414 = new TH1F( "ph_sigmaIEIE_414", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_415 = new TH1F( "ph_sigmaIEIE_415", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_416 = new TH1F( "ph_sigmaIEIE_416", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_417 = new TH1F( "ph_sigmaIEIE_417", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_418 = new TH1F( "ph_sigmaIEIE_418", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_419 = new TH1F( "ph_sigmaIEIE_419", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_420 = new TH1F( "ph_sigmaIEIE_420", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_421 = new TH1F( "ph_sigmaIEIE_421", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_422 = new TH1F( "ph_sigmaIEIE_422", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_423 = new TH1F( "ph_sigmaIEIE_423", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_424 = new TH1F( "ph_sigmaIEIE_424", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_425 = new TH1F( "ph_sigmaIEIE_425", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_426 = new TH1F( "ph_sigmaIEIE_426", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_427 = new TH1F( "ph_sigmaIEIE_427", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_428 = new TH1F( "ph_sigmaIEIE_428", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_429 = new TH1F( "ph_sigmaIEIE_429", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_430 = new TH1F( "ph_sigmaIEIE_430", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_431 = new TH1F( "ph_sigmaIEIE_431", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_432 = new TH1F( "ph_sigmaIEIE_432", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_433 = new TH1F( "ph_sigmaIEIE_433", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_434 = new TH1F( "ph_sigmaIEIE_434", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_435 = new TH1F( "ph_sigmaIEIE_435", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_436 = new TH1F( "ph_sigmaIEIE_436", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_437 = new TH1F( "ph_sigmaIEIE_437", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_438 = new TH1F( "ph_sigmaIEIE_438", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_439 = new TH1F( "ph_sigmaIEIE_439", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_440 = new TH1F( "ph_sigmaIEIE_440", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_441 = new TH1F( "ph_sigmaIEIE_441", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_442 = new TH1F( "ph_sigmaIEIE_442", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_443 = new TH1F( "ph_sigmaIEIE_443", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_444 = new TH1F( "ph_sigmaIEIE_444", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_445 = new TH1F( "ph_sigmaIEIE_445", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_446 = new TH1F( "ph_sigmaIEIE_446", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_447 = new TH1F( "ph_sigmaIEIE_447", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_448 = new TH1F( "ph_sigmaIEIE_448", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_449 = new TH1F( "ph_sigmaIEIE_449", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_450 = new TH1F( "ph_sigmaIEIE_450", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_451 = new TH1F( "ph_sigmaIEIE_451", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_452 = new TH1F( "ph_sigmaIEIE_452", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_453 = new TH1F( "ph_sigmaIEIE_453", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_454 = new TH1F( "ph_sigmaIEIE_454", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_455 = new TH1F( "ph_sigmaIEIE_455", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_456 = new TH1F( "ph_sigmaIEIE_456", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_457 = new TH1F( "ph_sigmaIEIE_457", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_458 = new TH1F( "ph_sigmaIEIE_458", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_459 = new TH1F( "ph_sigmaIEIE_459", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_460 = new TH1F( "ph_sigmaIEIE_460", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_461 = new TH1F( "ph_sigmaIEIE_461", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_462 = new TH1F( "ph_sigmaIEIE_462", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_463 = new TH1F( "ph_sigmaIEIE_463", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_464 = new TH1F( "ph_sigmaIEIE_464", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_465 = new TH1F( "ph_sigmaIEIE_465", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_466 = new TH1F( "ph_sigmaIEIE_466", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_467 = new TH1F( "ph_sigmaIEIE_467", "", 30, 0.000000, 0.030000 );

 double ph_sigmaIEIE_468xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_468 = new TH1F( "ph_sigmaIEIE_468", "", 2, ph_sigmaIEIE_468xarr );

 double ph_sigmaIEIE_469xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_469 = new TH1F( "ph_sigmaIEIE_469", "", 2, ph_sigmaIEIE_469xarr );

 double ph_sigmaIEIE_470xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_470 = new TH1F( "ph_sigmaIEIE_470", "", 2, ph_sigmaIEIE_470xarr );

 double ph_sigmaIEIE_471xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_471 = new TH1F( "ph_sigmaIEIE_471", "", 2, ph_sigmaIEIE_471xarr );

 double ph_sigmaIEIE_472xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_472 = new TH1F( "ph_sigmaIEIE_472", "", 2, ph_sigmaIEIE_472xarr );

 double ph_sigmaIEIE_473xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_473 = new TH1F( "ph_sigmaIEIE_473", "", 2, ph_sigmaIEIE_473xarr );

 double ph_sigmaIEIE_474xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_474 = new TH1F( "ph_sigmaIEIE_474", "", 2, ph_sigmaIEIE_474xarr );

 double ph_sigmaIEIE_475xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_475 = new TH1F( "ph_sigmaIEIE_475", "", 2, ph_sigmaIEIE_475xarr );

 double ph_sigmaIEIE_476xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_476 = new TH1F( "ph_sigmaIEIE_476", "", 2, ph_sigmaIEIE_476xarr );

 double ph_sigmaIEIE_477xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_477 = new TH1F( "ph_sigmaIEIE_477", "", 2, ph_sigmaIEIE_477xarr );

 double ph_sigmaIEIE_478xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_478 = new TH1F( "ph_sigmaIEIE_478", "", 2, ph_sigmaIEIE_478xarr );

 double ph_sigmaIEIE_479xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_479 = new TH1F( "ph_sigmaIEIE_479", "", 2, ph_sigmaIEIE_479xarr );

 double ph_sigmaIEIE_480xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_480 = new TH1F( "ph_sigmaIEIE_480", "", 2, ph_sigmaIEIE_480xarr );

 double ph_sigmaIEIE_481xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_481 = new TH1F( "ph_sigmaIEIE_481", "", 2, ph_sigmaIEIE_481xarr );

 double ph_sigmaIEIE_482xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_482 = new TH1F( "ph_sigmaIEIE_482", "", 2, ph_sigmaIEIE_482xarr );

 double ph_sigmaIEIE_483xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_483 = new TH1F( "ph_sigmaIEIE_483", "", 2, ph_sigmaIEIE_483xarr );

 double ph_sigmaIEIE_484xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_484 = new TH1F( "ph_sigmaIEIE_484", "", 2, ph_sigmaIEIE_484xarr );

 double ph_sigmaIEIE_485xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_485 = new TH1F( "ph_sigmaIEIE_485", "", 2, ph_sigmaIEIE_485xarr );

 double ph_sigmaIEIE_486xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_486 = new TH1F( "ph_sigmaIEIE_486", "", 2, ph_sigmaIEIE_486xarr );

 double ph_sigmaIEIE_487xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_487 = new TH1F( "ph_sigmaIEIE_487", "", 2, ph_sigmaIEIE_487xarr );

 double ph_sigmaIEIE_488xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_488 = new TH1F( "ph_sigmaIEIE_488", "", 2, ph_sigmaIEIE_488xarr );

 double ph_sigmaIEIE_489xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_489 = new TH1F( "ph_sigmaIEIE_489", "", 2, ph_sigmaIEIE_489xarr );

 double ph_sigmaIEIE_490xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_490 = new TH1F( "ph_sigmaIEIE_490", "", 2, ph_sigmaIEIE_490xarr );

 double ph_sigmaIEIE_491xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_491 = new TH1F( "ph_sigmaIEIE_491", "", 2, ph_sigmaIEIE_491xarr );

 double ph_sigmaIEIE_492xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_492 = new TH1F( "ph_sigmaIEIE_492", "", 2, ph_sigmaIEIE_492xarr );

 double ph_sigmaIEIE_493xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_493 = new TH1F( "ph_sigmaIEIE_493", "", 2, ph_sigmaIEIE_493xarr );

 double ph_sigmaIEIE_494xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_494 = new TH1F( "ph_sigmaIEIE_494", "", 2, ph_sigmaIEIE_494xarr );

 double ph_sigmaIEIE_495xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_495 = new TH1F( "ph_sigmaIEIE_495", "", 2, ph_sigmaIEIE_495xarr );

 double ph_sigmaIEIE_496xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_496 = new TH1F( "ph_sigmaIEIE_496", "", 2, ph_sigmaIEIE_496xarr );

 double ph_sigmaIEIE_497xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_497 = new TH1F( "ph_sigmaIEIE_497", "", 2, ph_sigmaIEIE_497xarr );

 double ph_sigmaIEIE_498xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_498 = new TH1F( "ph_sigmaIEIE_498", "", 2, ph_sigmaIEIE_498xarr );

 double ph_sigmaIEIE_499xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_499 = new TH1F( "ph_sigmaIEIE_499", "", 2, ph_sigmaIEIE_499xarr );

 double ph_sigmaIEIE_500xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_500 = new TH1F( "ph_sigmaIEIE_500", "", 2, ph_sigmaIEIE_500xarr );

 double ph_sigmaIEIE_501xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_501 = new TH1F( "ph_sigmaIEIE_501", "", 2, ph_sigmaIEIE_501xarr );

 double ph_sigmaIEIE_502xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_502 = new TH1F( "ph_sigmaIEIE_502", "", 2, ph_sigmaIEIE_502xarr );

  hist_ph_sigmaIEIE_503 = new TH1F( "ph_sigmaIEIE_503", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_504 = new TH1F( "ph_sigmaIEIE_504", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_505 = new TH1F( "ph_sigmaIEIE_505", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_506 = new TH1F( "ph_sigmaIEIE_506", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_507 = new TH1F( "ph_sigmaIEIE_507", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_508 = new TH1F( "ph_sigmaIEIE_508", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_509 = new TH1F( "ph_sigmaIEIE_509", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_510 = new TH1F( "ph_sigmaIEIE_510", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_511 = new TH1F( "ph_sigmaIEIE_511", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_512 = new TH1F( "ph_sigmaIEIE_512", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_513 = new TH1F( "ph_sigmaIEIE_513", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_514 = new TH1F( "ph_sigmaIEIE_514", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_515 = new TH1F( "ph_sigmaIEIE_515", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_516 = new TH1F( "ph_sigmaIEIE_516", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_517 = new TH1F( "ph_sigmaIEIE_517", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_518 = new TH1F( "ph_sigmaIEIE_518", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_519 = new TH1F( "ph_sigmaIEIE_519", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_520 = new TH1F( "ph_sigmaIEIE_520", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_521 = new TH1F( "ph_sigmaIEIE_521", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_522 = new TH1F( "ph_sigmaIEIE_522", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_523 = new TH1F( "ph_sigmaIEIE_523", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_524 = new TH1F( "ph_sigmaIEIE_524", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_525 = new TH1F( "ph_sigmaIEIE_525", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_526 = new TH1F( "ph_sigmaIEIE_526", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_527 = new TH1F( "ph_sigmaIEIE_527", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_528 = new TH1F( "ph_sigmaIEIE_528", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_529 = new TH1F( "ph_sigmaIEIE_529", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_530 = new TH1F( "ph_sigmaIEIE_530", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_531 = new TH1F( "ph_sigmaIEIE_531", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_532 = new TH1F( "ph_sigmaIEIE_532", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_533 = new TH1F( "ph_sigmaIEIE_533", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_534 = new TH1F( "ph_sigmaIEIE_534", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_535 = new TH1F( "ph_sigmaIEIE_535", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_536 = new TH1F( "ph_sigmaIEIE_536", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_537 = new TH1F( "ph_sigmaIEIE_537", "", 20, 0.000000, 0.100000 );

 double ph_sigmaIEIE_538xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_538 = new TH1F( "ph_sigmaIEIE_538", "", 2, ph_sigmaIEIE_538xarr );

 double ph_sigmaIEIE_539xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_539 = new TH1F( "ph_sigmaIEIE_539", "", 2, ph_sigmaIEIE_539xarr );

 double ph_sigmaIEIE_540xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_540 = new TH1F( "ph_sigmaIEIE_540", "", 2, ph_sigmaIEIE_540xarr );

 double ph_sigmaIEIE_541xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_541 = new TH1F( "ph_sigmaIEIE_541", "", 2, ph_sigmaIEIE_541xarr );

 double ph_sigmaIEIE_542xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_542 = new TH1F( "ph_sigmaIEIE_542", "", 2, ph_sigmaIEIE_542xarr );

 double ph_sigmaIEIE_543xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_543 = new TH1F( "ph_sigmaIEIE_543", "", 2, ph_sigmaIEIE_543xarr );

 double ph_sigmaIEIE_544xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_544 = new TH1F( "ph_sigmaIEIE_544", "", 2, ph_sigmaIEIE_544xarr );

 double ph_sigmaIEIE_545xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_545 = new TH1F( "ph_sigmaIEIE_545", "", 2, ph_sigmaIEIE_545xarr );

 double ph_sigmaIEIE_546xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_546 = new TH1F( "ph_sigmaIEIE_546", "", 2, ph_sigmaIEIE_546xarr );

 double ph_sigmaIEIE_547xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_547 = new TH1F( "ph_sigmaIEIE_547", "", 2, ph_sigmaIEIE_547xarr );

 double ph_sigmaIEIE_548xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_548 = new TH1F( "ph_sigmaIEIE_548", "", 2, ph_sigmaIEIE_548xarr );

 double ph_sigmaIEIE_549xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_549 = new TH1F( "ph_sigmaIEIE_549", "", 2, ph_sigmaIEIE_549xarr );

 double ph_sigmaIEIE_550xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_550 = new TH1F( "ph_sigmaIEIE_550", "", 2, ph_sigmaIEIE_550xarr );

 double ph_sigmaIEIE_551xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_551 = new TH1F( "ph_sigmaIEIE_551", "", 2, ph_sigmaIEIE_551xarr );

 double ph_sigmaIEIE_552xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_552 = new TH1F( "ph_sigmaIEIE_552", "", 2, ph_sigmaIEIE_552xarr );

 double ph_sigmaIEIE_553xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_553 = new TH1F( "ph_sigmaIEIE_553", "", 2, ph_sigmaIEIE_553xarr );

 double ph_sigmaIEIE_554xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_554 = new TH1F( "ph_sigmaIEIE_554", "", 2, ph_sigmaIEIE_554xarr );

 double ph_sigmaIEIE_555xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_555 = new TH1F( "ph_sigmaIEIE_555", "", 2, ph_sigmaIEIE_555xarr );

 double ph_sigmaIEIE_556xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_556 = new TH1F( "ph_sigmaIEIE_556", "", 2, ph_sigmaIEIE_556xarr );

 double ph_sigmaIEIE_557xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_557 = new TH1F( "ph_sigmaIEIE_557", "", 2, ph_sigmaIEIE_557xarr );

 double ph_sigmaIEIE_558xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_558 = new TH1F( "ph_sigmaIEIE_558", "", 2, ph_sigmaIEIE_558xarr );

 double ph_sigmaIEIE_559xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_559 = new TH1F( "ph_sigmaIEIE_559", "", 2, ph_sigmaIEIE_559xarr );

 double ph_sigmaIEIE_560xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_560 = new TH1F( "ph_sigmaIEIE_560", "", 2, ph_sigmaIEIE_560xarr );

 double ph_sigmaIEIE_561xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_561 = new TH1F( "ph_sigmaIEIE_561", "", 2, ph_sigmaIEIE_561xarr );

 double ph_sigmaIEIE_562xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_562 = new TH1F( "ph_sigmaIEIE_562", "", 2, ph_sigmaIEIE_562xarr );

 double ph_sigmaIEIE_563xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_563 = new TH1F( "ph_sigmaIEIE_563", "", 2, ph_sigmaIEIE_563xarr );

 double ph_sigmaIEIE_564xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_564 = new TH1F( "ph_sigmaIEIE_564", "", 2, ph_sigmaIEIE_564xarr );

 double ph_sigmaIEIE_565xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_565 = new TH1F( "ph_sigmaIEIE_565", "", 2, ph_sigmaIEIE_565xarr );

 double ph_sigmaIEIE_566xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_566 = new TH1F( "ph_sigmaIEIE_566", "", 2, ph_sigmaIEIE_566xarr );

 double ph_sigmaIEIE_567xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_567 = new TH1F( "ph_sigmaIEIE_567", "", 2, ph_sigmaIEIE_567xarr );

 double ph_sigmaIEIE_568xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_568 = new TH1F( "ph_sigmaIEIE_568", "", 2, ph_sigmaIEIE_568xarr );

 double ph_sigmaIEIE_569xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_569 = new TH1F( "ph_sigmaIEIE_569", "", 2, ph_sigmaIEIE_569xarr );

 double ph_sigmaIEIE_570xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_570 = new TH1F( "ph_sigmaIEIE_570", "", 2, ph_sigmaIEIE_570xarr );

 double ph_sigmaIEIE_571xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_571 = new TH1F( "ph_sigmaIEIE_571", "", 2, ph_sigmaIEIE_571xarr );

 double ph_sigmaIEIE_572xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_572 = new TH1F( "ph_sigmaIEIE_572", "", 2, ph_sigmaIEIE_572xarr );

  hist_ph_sigmaIEIE_573 = new TH1F( "ph_sigmaIEIE_573", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_574 = new TH1F( "ph_sigmaIEIE_574", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_575 = new TH1F( "ph_sigmaIEIE_575", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_576 = new TH1F( "ph_sigmaIEIE_576", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_577 = new TH1F( "ph_sigmaIEIE_577", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_578 = new TH1F( "ph_sigmaIEIE_578", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_579 = new TH1F( "ph_sigmaIEIE_579", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_580 = new TH1F( "ph_sigmaIEIE_580", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_581 = new TH1F( "ph_sigmaIEIE_581", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_582 = new TH1F( "ph_sigmaIEIE_582", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_583 = new TH1F( "ph_sigmaIEIE_583", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_584 = new TH1F( "ph_sigmaIEIE_584", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_585 = new TH1F( "ph_sigmaIEIE_585", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_586 = new TH1F( "ph_sigmaIEIE_586", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_587 = new TH1F( "ph_sigmaIEIE_587", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_588 = new TH1F( "ph_sigmaIEIE_588", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_589 = new TH1F( "ph_sigmaIEIE_589", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_590 = new TH1F( "ph_sigmaIEIE_590", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_591 = new TH1F( "ph_sigmaIEIE_591", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_592 = new TH1F( "ph_sigmaIEIE_592", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_593 = new TH1F( "ph_sigmaIEIE_593", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_594 = new TH1F( "ph_sigmaIEIE_594", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_595 = new TH1F( "ph_sigmaIEIE_595", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_596 = new TH1F( "ph_sigmaIEIE_596", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_597 = new TH1F( "ph_sigmaIEIE_597", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_598 = new TH1F( "ph_sigmaIEIE_598", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_599 = new TH1F( "ph_sigmaIEIE_599", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_600 = new TH1F( "ph_sigmaIEIE_600", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_601 = new TH1F( "ph_sigmaIEIE_601", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_602 = new TH1F( "ph_sigmaIEIE_602", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_603 = new TH1F( "ph_sigmaIEIE_603", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_604 = new TH1F( "ph_sigmaIEIE_604", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_605 = new TH1F( "ph_sigmaIEIE_605", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_606 = new TH1F( "ph_sigmaIEIE_606", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_607 = new TH1F( "ph_sigmaIEIE_607", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_608 = new TH1F( "ph_sigmaIEIE_608", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_609 = new TH1F( "ph_sigmaIEIE_609", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_610 = new TH1F( "ph_sigmaIEIE_610", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_611 = new TH1F( "ph_sigmaIEIE_611", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_612 = new TH1F( "ph_sigmaIEIE_612", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_613 = new TH1F( "ph_sigmaIEIE_613", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_614 = new TH1F( "ph_sigmaIEIE_614", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_615 = new TH1F( "ph_sigmaIEIE_615", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_616 = new TH1F( "ph_sigmaIEIE_616", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_617 = new TH1F( "ph_sigmaIEIE_617", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_618 = new TH1F( "ph_sigmaIEIE_618", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_619 = new TH1F( "ph_sigmaIEIE_619", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_620 = new TH1F( "ph_sigmaIEIE_620", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_621 = new TH1F( "ph_sigmaIEIE_621", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_622 = new TH1F( "ph_sigmaIEIE_622", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_623 = new TH1F( "ph_sigmaIEIE_623", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_624 = new TH1F( "ph_sigmaIEIE_624", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_625 = new TH1F( "ph_sigmaIEIE_625", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_626 = new TH1F( "ph_sigmaIEIE_626", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_627 = new TH1F( "ph_sigmaIEIE_627", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_628 = new TH1F( "ph_sigmaIEIE_628", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_629 = new TH1F( "ph_sigmaIEIE_629", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_630 = new TH1F( "ph_sigmaIEIE_630", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_631 = new TH1F( "ph_sigmaIEIE_631", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_632 = new TH1F( "ph_sigmaIEIE_632", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_633 = new TH1F( "ph_sigmaIEIE_633", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_634 = new TH1F( "ph_sigmaIEIE_634", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_635 = new TH1F( "ph_sigmaIEIE_635", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_636 = new TH1F( "ph_sigmaIEIE_636", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_637 = new TH1F( "ph_sigmaIEIE_637", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_638 = new TH1F( "ph_sigmaIEIE_638", "", 10, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_639 = new TH1F( "ph_sigmaIEIE_639", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_640 = new TH1F( "ph_sigmaIEIE_640", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_641 = new TH1F( "ph_sigmaIEIE_641", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_642 = new TH1F( "ph_sigmaIEIE_642", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_643 = new TH1F( "ph_sigmaIEIE_643", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_644 = new TH1F( "ph_sigmaIEIE_644", "", 10, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_645 = new TH1F( "ph_sigmaIEIE_645", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_646 = new TH1F( "ph_sigmaIEIE_646", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_647 = new TH1F( "ph_sigmaIEIE_647", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_648 = new TH1F( "ph_sigmaIEIE_648", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_649 = new TH1F( "ph_sigmaIEIE_649", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_650 = new TH1F( "ph_sigmaIEIE_650", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_651 = new TH1F( "ph_sigmaIEIE_651", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_652 = new TH1F( "ph_sigmaIEIE_652", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_653 = new TH1F( "ph_sigmaIEIE_653", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_654 = new TH1F( "ph_sigmaIEIE_654", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_655 = new TH1F( "ph_sigmaIEIE_655", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_656 = new TH1F( "ph_sigmaIEIE_656", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_657 = new TH1F( "ph_sigmaIEIE_657", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_658 = new TH1F( "ph_sigmaIEIE_658", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_659 = new TH1F( "ph_sigmaIEIE_659", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_660 = new TH1F( "ph_sigmaIEIE_660", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_661 = new TH1F( "ph_sigmaIEIE_661", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_662 = new TH1F( "ph_sigmaIEIE_662", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_663 = new TH1F( "ph_sigmaIEIE_663", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_664 = new TH1F( "ph_sigmaIEIE_664", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_665 = new TH1F( "ph_sigmaIEIE_665", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_666 = new TH1F( "ph_sigmaIEIE_666", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_667 = new TH1F( "ph_sigmaIEIE_667", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_668 = new TH1F( "ph_sigmaIEIE_668", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_669 = new TH1F( "ph_sigmaIEIE_669", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_670 = new TH1F( "ph_sigmaIEIE_670", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_671 = new TH1F( "ph_sigmaIEIE_671", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_672 = new TH1F( "ph_sigmaIEIE_672", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_673 = new TH1F( "ph_sigmaIEIE_673", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_674 = new TH1F( "ph_sigmaIEIE_674", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_675 = new TH1F( "ph_sigmaIEIE_675", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_676 = new TH1F( "ph_sigmaIEIE_676", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_677 = new TH1F( "ph_sigmaIEIE_677", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_678 = new TH1F( "ph_sigmaIEIE_678", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_679 = new TH1F( "ph_sigmaIEIE_679", "", 30, 0.000000, 0.030000 );

 double ph_sigmaIEIE_680xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_680 = new TH1F( "ph_sigmaIEIE_680", "", 2, ph_sigmaIEIE_680xarr );

 double ph_sigmaIEIE_681xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_681 = new TH1F( "ph_sigmaIEIE_681", "", 2, ph_sigmaIEIE_681xarr );

 double ph_sigmaIEIE_682xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_682 = new TH1F( "ph_sigmaIEIE_682", "", 2, ph_sigmaIEIE_682xarr );

 double ph_sigmaIEIE_683xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_683 = new TH1F( "ph_sigmaIEIE_683", "", 2, ph_sigmaIEIE_683xarr );

 double ph_sigmaIEIE_684xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_684 = new TH1F( "ph_sigmaIEIE_684", "", 2, ph_sigmaIEIE_684xarr );

 double ph_sigmaIEIE_685xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_685 = new TH1F( "ph_sigmaIEIE_685", "", 2, ph_sigmaIEIE_685xarr );

 double ph_sigmaIEIE_686xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_686 = new TH1F( "ph_sigmaIEIE_686", "", 2, ph_sigmaIEIE_686xarr );

 double ph_sigmaIEIE_687xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_687 = new TH1F( "ph_sigmaIEIE_687", "", 2, ph_sigmaIEIE_687xarr );

 double ph_sigmaIEIE_688xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_688 = new TH1F( "ph_sigmaIEIE_688", "", 2, ph_sigmaIEIE_688xarr );

 double ph_sigmaIEIE_689xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_689 = new TH1F( "ph_sigmaIEIE_689", "", 2, ph_sigmaIEIE_689xarr );

 double ph_sigmaIEIE_690xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_690 = new TH1F( "ph_sigmaIEIE_690", "", 2, ph_sigmaIEIE_690xarr );

 double ph_sigmaIEIE_691xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_691 = new TH1F( "ph_sigmaIEIE_691", "", 2, ph_sigmaIEIE_691xarr );

 double ph_sigmaIEIE_692xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_692 = new TH1F( "ph_sigmaIEIE_692", "", 2, ph_sigmaIEIE_692xarr );

 double ph_sigmaIEIE_693xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_693 = new TH1F( "ph_sigmaIEIE_693", "", 2, ph_sigmaIEIE_693xarr );

 double ph_sigmaIEIE_694xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_694 = new TH1F( "ph_sigmaIEIE_694", "", 2, ph_sigmaIEIE_694xarr );

 double ph_sigmaIEIE_695xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_695 = new TH1F( "ph_sigmaIEIE_695", "", 2, ph_sigmaIEIE_695xarr );

 double ph_sigmaIEIE_696xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_696 = new TH1F( "ph_sigmaIEIE_696", "", 2, ph_sigmaIEIE_696xarr );

 double ph_sigmaIEIE_697xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_697 = new TH1F( "ph_sigmaIEIE_697", "", 2, ph_sigmaIEIE_697xarr );

 double ph_sigmaIEIE_698xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_698 = new TH1F( "ph_sigmaIEIE_698", "", 2, ph_sigmaIEIE_698xarr );

 double ph_sigmaIEIE_699xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_699 = new TH1F( "ph_sigmaIEIE_699", "", 2, ph_sigmaIEIE_699xarr );

 double ph_sigmaIEIE_700xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_700 = new TH1F( "ph_sigmaIEIE_700", "", 2, ph_sigmaIEIE_700xarr );

 double ph_sigmaIEIE_701xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_701 = new TH1F( "ph_sigmaIEIE_701", "", 2, ph_sigmaIEIE_701xarr );

 double ph_sigmaIEIE_702xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_702 = new TH1F( "ph_sigmaIEIE_702", "", 2, ph_sigmaIEIE_702xarr );

 double ph_sigmaIEIE_703xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_703 = new TH1F( "ph_sigmaIEIE_703", "", 2, ph_sigmaIEIE_703xarr );

 double ph_sigmaIEIE_704xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_704 = new TH1F( "ph_sigmaIEIE_704", "", 2, ph_sigmaIEIE_704xarr );

 double ph_sigmaIEIE_705xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_705 = new TH1F( "ph_sigmaIEIE_705", "", 2, ph_sigmaIEIE_705xarr );

 double ph_sigmaIEIE_706xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_706 = new TH1F( "ph_sigmaIEIE_706", "", 2, ph_sigmaIEIE_706xarr );

 double ph_sigmaIEIE_707xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_707 = new TH1F( "ph_sigmaIEIE_707", "", 2, ph_sigmaIEIE_707xarr );

 double ph_sigmaIEIE_708xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_708 = new TH1F( "ph_sigmaIEIE_708", "", 2, ph_sigmaIEIE_708xarr );

 double ph_sigmaIEIE_709xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_709 = new TH1F( "ph_sigmaIEIE_709", "", 2, ph_sigmaIEIE_709xarr );

 double ph_sigmaIEIE_710xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_710 = new TH1F( "ph_sigmaIEIE_710", "", 2, ph_sigmaIEIE_710xarr );

 double ph_sigmaIEIE_711xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_711 = new TH1F( "ph_sigmaIEIE_711", "", 2, ph_sigmaIEIE_711xarr );

 double ph_sigmaIEIE_712xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_712 = new TH1F( "ph_sigmaIEIE_712", "", 2, ph_sigmaIEIE_712xarr );

 double ph_sigmaIEIE_713xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_713 = new TH1F( "ph_sigmaIEIE_713", "", 2, ph_sigmaIEIE_713xarr );

 double ph_sigmaIEIE_714xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_714 = new TH1F( "ph_sigmaIEIE_714", "", 2, ph_sigmaIEIE_714xarr );

  hist_ph_sigmaIEIE_715 = new TH1F( "ph_sigmaIEIE_715", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_716 = new TH1F( "ph_sigmaIEIE_716", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_717 = new TH1F( "ph_sigmaIEIE_717", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_718 = new TH1F( "ph_sigmaIEIE_718", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_719 = new TH1F( "ph_sigmaIEIE_719", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_720 = new TH1F( "ph_sigmaIEIE_720", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_721 = new TH1F( "ph_sigmaIEIE_721", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_722 = new TH1F( "ph_sigmaIEIE_722", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_723 = new TH1F( "ph_sigmaIEIE_723", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_724 = new TH1F( "ph_sigmaIEIE_724", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_725 = new TH1F( "ph_sigmaIEIE_725", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_726 = new TH1F( "ph_sigmaIEIE_726", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_727 = new TH1F( "ph_sigmaIEIE_727", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_728 = new TH1F( "ph_sigmaIEIE_728", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_729 = new TH1F( "ph_sigmaIEIE_729", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_730 = new TH1F( "ph_sigmaIEIE_730", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_731 = new TH1F( "ph_sigmaIEIE_731", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_732 = new TH1F( "ph_sigmaIEIE_732", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_733 = new TH1F( "ph_sigmaIEIE_733", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_734 = new TH1F( "ph_sigmaIEIE_734", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_735 = new TH1F( "ph_sigmaIEIE_735", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_736 = new TH1F( "ph_sigmaIEIE_736", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_737 = new TH1F( "ph_sigmaIEIE_737", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_738 = new TH1F( "ph_sigmaIEIE_738", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_739 = new TH1F( "ph_sigmaIEIE_739", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_740 = new TH1F( "ph_sigmaIEIE_740", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_741 = new TH1F( "ph_sigmaIEIE_741", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_742 = new TH1F( "ph_sigmaIEIE_742", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_743 = new TH1F( "ph_sigmaIEIE_743", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_744 = new TH1F( "ph_sigmaIEIE_744", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_745 = new TH1F( "ph_sigmaIEIE_745", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_746 = new TH1F( "ph_sigmaIEIE_746", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_747 = new TH1F( "ph_sigmaIEIE_747", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_748 = new TH1F( "ph_sigmaIEIE_748", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_749 = new TH1F( "ph_sigmaIEIE_749", "", 20, 0.000000, 0.100000 );

 double ph_sigmaIEIE_750xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_750 = new TH1F( "ph_sigmaIEIE_750", "", 2, ph_sigmaIEIE_750xarr );

 double ph_sigmaIEIE_751xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_751 = new TH1F( "ph_sigmaIEIE_751", "", 2, ph_sigmaIEIE_751xarr );

 double ph_sigmaIEIE_752xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_752 = new TH1F( "ph_sigmaIEIE_752", "", 2, ph_sigmaIEIE_752xarr );

 double ph_sigmaIEIE_753xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_753 = new TH1F( "ph_sigmaIEIE_753", "", 2, ph_sigmaIEIE_753xarr );

 double ph_sigmaIEIE_754xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_754 = new TH1F( "ph_sigmaIEIE_754", "", 2, ph_sigmaIEIE_754xarr );

 double ph_sigmaIEIE_755xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_755 = new TH1F( "ph_sigmaIEIE_755", "", 2, ph_sigmaIEIE_755xarr );

 double ph_sigmaIEIE_756xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_756 = new TH1F( "ph_sigmaIEIE_756", "", 2, ph_sigmaIEIE_756xarr );

 double ph_sigmaIEIE_757xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_757 = new TH1F( "ph_sigmaIEIE_757", "", 2, ph_sigmaIEIE_757xarr );

 double ph_sigmaIEIE_758xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_758 = new TH1F( "ph_sigmaIEIE_758", "", 2, ph_sigmaIEIE_758xarr );

 double ph_sigmaIEIE_759xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_759 = new TH1F( "ph_sigmaIEIE_759", "", 2, ph_sigmaIEIE_759xarr );

 double ph_sigmaIEIE_760xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_760 = new TH1F( "ph_sigmaIEIE_760", "", 2, ph_sigmaIEIE_760xarr );

 double ph_sigmaIEIE_761xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_761 = new TH1F( "ph_sigmaIEIE_761", "", 2, ph_sigmaIEIE_761xarr );

 double ph_sigmaIEIE_762xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_762 = new TH1F( "ph_sigmaIEIE_762", "", 2, ph_sigmaIEIE_762xarr );

 double ph_sigmaIEIE_763xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_763 = new TH1F( "ph_sigmaIEIE_763", "", 2, ph_sigmaIEIE_763xarr );

 double ph_sigmaIEIE_764xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_764 = new TH1F( "ph_sigmaIEIE_764", "", 2, ph_sigmaIEIE_764xarr );

 double ph_sigmaIEIE_765xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_765 = new TH1F( "ph_sigmaIEIE_765", "", 2, ph_sigmaIEIE_765xarr );

 double ph_sigmaIEIE_766xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_766 = new TH1F( "ph_sigmaIEIE_766", "", 2, ph_sigmaIEIE_766xarr );

 double ph_sigmaIEIE_767xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_767 = new TH1F( "ph_sigmaIEIE_767", "", 2, ph_sigmaIEIE_767xarr );

 double ph_sigmaIEIE_768xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_768 = new TH1F( "ph_sigmaIEIE_768", "", 2, ph_sigmaIEIE_768xarr );

 double ph_sigmaIEIE_769xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_769 = new TH1F( "ph_sigmaIEIE_769", "", 2, ph_sigmaIEIE_769xarr );

 double ph_sigmaIEIE_770xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_770 = new TH1F( "ph_sigmaIEIE_770", "", 2, ph_sigmaIEIE_770xarr );

 double ph_sigmaIEIE_771xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_771 = new TH1F( "ph_sigmaIEIE_771", "", 2, ph_sigmaIEIE_771xarr );

 double ph_sigmaIEIE_772xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_772 = new TH1F( "ph_sigmaIEIE_772", "", 2, ph_sigmaIEIE_772xarr );

 double ph_sigmaIEIE_773xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_773 = new TH1F( "ph_sigmaIEIE_773", "", 2, ph_sigmaIEIE_773xarr );

 double ph_sigmaIEIE_774xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_774 = new TH1F( "ph_sigmaIEIE_774", "", 2, ph_sigmaIEIE_774xarr );

 double ph_sigmaIEIE_775xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_775 = new TH1F( "ph_sigmaIEIE_775", "", 2, ph_sigmaIEIE_775xarr );

 double ph_sigmaIEIE_776xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_776 = new TH1F( "ph_sigmaIEIE_776", "", 2, ph_sigmaIEIE_776xarr );

 double ph_sigmaIEIE_777xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_777 = new TH1F( "ph_sigmaIEIE_777", "", 2, ph_sigmaIEIE_777xarr );

 double ph_sigmaIEIE_778xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_778 = new TH1F( "ph_sigmaIEIE_778", "", 2, ph_sigmaIEIE_778xarr );

 double ph_sigmaIEIE_779xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_779 = new TH1F( "ph_sigmaIEIE_779", "", 2, ph_sigmaIEIE_779xarr );

 double ph_sigmaIEIE_780xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_780 = new TH1F( "ph_sigmaIEIE_780", "", 2, ph_sigmaIEIE_780xarr );

 double ph_sigmaIEIE_781xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_781 = new TH1F( "ph_sigmaIEIE_781", "", 2, ph_sigmaIEIE_781xarr );

 double ph_sigmaIEIE_782xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_782 = new TH1F( "ph_sigmaIEIE_782", "", 2, ph_sigmaIEIE_782xarr );

 double ph_sigmaIEIE_783xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_783 = new TH1F( "ph_sigmaIEIE_783", "", 2, ph_sigmaIEIE_783xarr );

 double ph_sigmaIEIE_784xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_784 = new TH1F( "ph_sigmaIEIE_784", "", 2, ph_sigmaIEIE_784xarr );

  hist_ph_sigmaIEIE_785 = new TH1F( "ph_sigmaIEIE_785", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_786 = new TH1F( "ph_sigmaIEIE_786", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_787 = new TH1F( "ph_sigmaIEIE_787", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_788 = new TH1F( "ph_sigmaIEIE_788", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_789 = new TH1F( "ph_sigmaIEIE_789", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_790 = new TH1F( "ph_sigmaIEIE_790", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_791 = new TH1F( "ph_sigmaIEIE_791", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_792 = new TH1F( "ph_sigmaIEIE_792", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_793 = new TH1F( "ph_sigmaIEIE_793", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_794 = new TH1F( "ph_sigmaIEIE_794", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_795 = new TH1F( "ph_sigmaIEIE_795", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_796 = new TH1F( "ph_sigmaIEIE_796", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_797 = new TH1F( "ph_sigmaIEIE_797", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_798 = new TH1F( "ph_sigmaIEIE_798", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_799 = new TH1F( "ph_sigmaIEIE_799", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_800 = new TH1F( "ph_sigmaIEIE_800", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_801 = new TH1F( "ph_sigmaIEIE_801", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_802 = new TH1F( "ph_sigmaIEIE_802", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_803 = new TH1F( "ph_sigmaIEIE_803", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_804 = new TH1F( "ph_sigmaIEIE_804", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_805 = new TH1F( "ph_sigmaIEIE_805", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_806 = new TH1F( "ph_sigmaIEIE_806", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_807 = new TH1F( "ph_sigmaIEIE_807", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_808 = new TH1F( "ph_sigmaIEIE_808", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_809 = new TH1F( "ph_sigmaIEIE_809", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_810 = new TH1F( "ph_sigmaIEIE_810", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_811 = new TH1F( "ph_sigmaIEIE_811", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_812 = new TH1F( "ph_sigmaIEIE_812", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_813 = new TH1F( "ph_sigmaIEIE_813", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_814 = new TH1F( "ph_sigmaIEIE_814", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_815 = new TH1F( "ph_sigmaIEIE_815", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_816 = new TH1F( "ph_sigmaIEIE_816", "", 30, 0.000000, 0.030000 );

 double ph_sigmaIEIE_817xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_817 = new TH1F( "ph_sigmaIEIE_817", "", 2, ph_sigmaIEIE_817xarr );

 double ph_sigmaIEIE_818xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_818 = new TH1F( "ph_sigmaIEIE_818", "", 2, ph_sigmaIEIE_818xarr );

 double ph_sigmaIEIE_819xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_819 = new TH1F( "ph_sigmaIEIE_819", "", 2, ph_sigmaIEIE_819xarr );

 double ph_sigmaIEIE_820xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_820 = new TH1F( "ph_sigmaIEIE_820", "", 2, ph_sigmaIEIE_820xarr );

 double ph_sigmaIEIE_821xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_821 = new TH1F( "ph_sigmaIEIE_821", "", 2, ph_sigmaIEIE_821xarr );

 double ph_sigmaIEIE_822xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_822 = new TH1F( "ph_sigmaIEIE_822", "", 2, ph_sigmaIEIE_822xarr );

 double ph_sigmaIEIE_823xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_823 = new TH1F( "ph_sigmaIEIE_823", "", 2, ph_sigmaIEIE_823xarr );

 double ph_sigmaIEIE_824xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_824 = new TH1F( "ph_sigmaIEIE_824", "", 2, ph_sigmaIEIE_824xarr );

 double ph_sigmaIEIE_825xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_825 = new TH1F( "ph_sigmaIEIE_825", "", 2, ph_sigmaIEIE_825xarr );

 double ph_sigmaIEIE_826xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_826 = new TH1F( "ph_sigmaIEIE_826", "", 2, ph_sigmaIEIE_826xarr );

 double ph_sigmaIEIE_827xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_827 = new TH1F( "ph_sigmaIEIE_827", "", 2, ph_sigmaIEIE_827xarr );

 double ph_sigmaIEIE_828xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_828 = new TH1F( "ph_sigmaIEIE_828", "", 2, ph_sigmaIEIE_828xarr );

 double ph_sigmaIEIE_829xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_829 = new TH1F( "ph_sigmaIEIE_829", "", 2, ph_sigmaIEIE_829xarr );

 double ph_sigmaIEIE_830xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_830 = new TH1F( "ph_sigmaIEIE_830", "", 2, ph_sigmaIEIE_830xarr );

 double ph_sigmaIEIE_831xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_831 = new TH1F( "ph_sigmaIEIE_831", "", 2, ph_sigmaIEIE_831xarr );

 double ph_sigmaIEIE_832xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_832 = new TH1F( "ph_sigmaIEIE_832", "", 2, ph_sigmaIEIE_832xarr );

 double ph_sigmaIEIE_833xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_833 = new TH1F( "ph_sigmaIEIE_833", "", 2, ph_sigmaIEIE_833xarr );

 double ph_sigmaIEIE_834xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_834 = new TH1F( "ph_sigmaIEIE_834", "", 2, ph_sigmaIEIE_834xarr );

 double ph_sigmaIEIE_835xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_835 = new TH1F( "ph_sigmaIEIE_835", "", 2, ph_sigmaIEIE_835xarr );

 double ph_sigmaIEIE_836xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_836 = new TH1F( "ph_sigmaIEIE_836", "", 2, ph_sigmaIEIE_836xarr );

 double ph_sigmaIEIE_837xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_837 = new TH1F( "ph_sigmaIEIE_837", "", 2, ph_sigmaIEIE_837xarr );

 double ph_sigmaIEIE_838xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_838 = new TH1F( "ph_sigmaIEIE_838", "", 2, ph_sigmaIEIE_838xarr );

 double ph_sigmaIEIE_839xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_839 = new TH1F( "ph_sigmaIEIE_839", "", 2, ph_sigmaIEIE_839xarr );

 double ph_sigmaIEIE_840xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_840 = new TH1F( "ph_sigmaIEIE_840", "", 2, ph_sigmaIEIE_840xarr );

 double ph_sigmaIEIE_841xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_841 = new TH1F( "ph_sigmaIEIE_841", "", 2, ph_sigmaIEIE_841xarr );

 double ph_sigmaIEIE_842xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_842 = new TH1F( "ph_sigmaIEIE_842", "", 2, ph_sigmaIEIE_842xarr );

 double ph_sigmaIEIE_843xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_843 = new TH1F( "ph_sigmaIEIE_843", "", 2, ph_sigmaIEIE_843xarr );

 double ph_sigmaIEIE_844xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_844 = new TH1F( "ph_sigmaIEIE_844", "", 2, ph_sigmaIEIE_844xarr );

 double ph_sigmaIEIE_845xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_845 = new TH1F( "ph_sigmaIEIE_845", "", 2, ph_sigmaIEIE_845xarr );

 double ph_sigmaIEIE_846xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_846 = new TH1F( "ph_sigmaIEIE_846", "", 2, ph_sigmaIEIE_846xarr );

 double ph_sigmaIEIE_847xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_847 = new TH1F( "ph_sigmaIEIE_847", "", 2, ph_sigmaIEIE_847xarr );

 double ph_sigmaIEIE_848xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_848 = new TH1F( "ph_sigmaIEIE_848", "", 2, ph_sigmaIEIE_848xarr );

  hist_ph_sigmaIEIE_849 = new TH1F( "ph_sigmaIEIE_849", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_850 = new TH1F( "ph_sigmaIEIE_850", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_851 = new TH1F( "ph_sigmaIEIE_851", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_852 = new TH1F( "ph_sigmaIEIE_852", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_853 = new TH1F( "ph_sigmaIEIE_853", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_854 = new TH1F( "ph_sigmaIEIE_854", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_855 = new TH1F( "ph_sigmaIEIE_855", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_856 = new TH1F( "ph_sigmaIEIE_856", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_857 = new TH1F( "ph_sigmaIEIE_857", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_858 = new TH1F( "ph_sigmaIEIE_858", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_859 = new TH1F( "ph_sigmaIEIE_859", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_860 = new TH1F( "ph_sigmaIEIE_860", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_861 = new TH1F( "ph_sigmaIEIE_861", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_862 = new TH1F( "ph_sigmaIEIE_862", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_863 = new TH1F( "ph_sigmaIEIE_863", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_864 = new TH1F( "ph_sigmaIEIE_864", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_865 = new TH1F( "ph_sigmaIEIE_865", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_866 = new TH1F( "ph_sigmaIEIE_866", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_867 = new TH1F( "ph_sigmaIEIE_867", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_868 = new TH1F( "ph_sigmaIEIE_868", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_869 = new TH1F( "ph_sigmaIEIE_869", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_870 = new TH1F( "ph_sigmaIEIE_870", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_871 = new TH1F( "ph_sigmaIEIE_871", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_872 = new TH1F( "ph_sigmaIEIE_872", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_873 = new TH1F( "ph_sigmaIEIE_873", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_874 = new TH1F( "ph_sigmaIEIE_874", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_875 = new TH1F( "ph_sigmaIEIE_875", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_876 = new TH1F( "ph_sigmaIEIE_876", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_877 = new TH1F( "ph_sigmaIEIE_877", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_878 = new TH1F( "ph_sigmaIEIE_878", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_879 = new TH1F( "ph_sigmaIEIE_879", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_880 = new TH1F( "ph_sigmaIEIE_880", "", 20, 0.000000, 0.100000 );

 double ph_sigmaIEIE_881xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_881 = new TH1F( "ph_sigmaIEIE_881", "", 2, ph_sigmaIEIE_881xarr );

 double ph_sigmaIEIE_882xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_882 = new TH1F( "ph_sigmaIEIE_882", "", 2, ph_sigmaIEIE_882xarr );

 double ph_sigmaIEIE_883xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_883 = new TH1F( "ph_sigmaIEIE_883", "", 2, ph_sigmaIEIE_883xarr );

 double ph_sigmaIEIE_884xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_884 = new TH1F( "ph_sigmaIEIE_884", "", 2, ph_sigmaIEIE_884xarr );

 double ph_sigmaIEIE_885xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_885 = new TH1F( "ph_sigmaIEIE_885", "", 2, ph_sigmaIEIE_885xarr );

 double ph_sigmaIEIE_886xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_886 = new TH1F( "ph_sigmaIEIE_886", "", 2, ph_sigmaIEIE_886xarr );

 double ph_sigmaIEIE_887xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_887 = new TH1F( "ph_sigmaIEIE_887", "", 2, ph_sigmaIEIE_887xarr );

 double ph_sigmaIEIE_888xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_888 = new TH1F( "ph_sigmaIEIE_888", "", 2, ph_sigmaIEIE_888xarr );

 double ph_sigmaIEIE_889xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_889 = new TH1F( "ph_sigmaIEIE_889", "", 2, ph_sigmaIEIE_889xarr );

 double ph_sigmaIEIE_890xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_890 = new TH1F( "ph_sigmaIEIE_890", "", 2, ph_sigmaIEIE_890xarr );

 double ph_sigmaIEIE_891xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_891 = new TH1F( "ph_sigmaIEIE_891", "", 2, ph_sigmaIEIE_891xarr );

 double ph_sigmaIEIE_892xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_892 = new TH1F( "ph_sigmaIEIE_892", "", 2, ph_sigmaIEIE_892xarr );

 double ph_sigmaIEIE_893xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_893 = new TH1F( "ph_sigmaIEIE_893", "", 2, ph_sigmaIEIE_893xarr );

 double ph_sigmaIEIE_894xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_894 = new TH1F( "ph_sigmaIEIE_894", "", 2, ph_sigmaIEIE_894xarr );

 double ph_sigmaIEIE_895xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_895 = new TH1F( "ph_sigmaIEIE_895", "", 2, ph_sigmaIEIE_895xarr );

 double ph_sigmaIEIE_896xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_896 = new TH1F( "ph_sigmaIEIE_896", "", 2, ph_sigmaIEIE_896xarr );

 double ph_sigmaIEIE_897xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_897 = new TH1F( "ph_sigmaIEIE_897", "", 2, ph_sigmaIEIE_897xarr );

 double ph_sigmaIEIE_898xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_898 = new TH1F( "ph_sigmaIEIE_898", "", 2, ph_sigmaIEIE_898xarr );

 double ph_sigmaIEIE_899xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_899 = new TH1F( "ph_sigmaIEIE_899", "", 2, ph_sigmaIEIE_899xarr );

 double ph_sigmaIEIE_900xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_900 = new TH1F( "ph_sigmaIEIE_900", "", 2, ph_sigmaIEIE_900xarr );

 double ph_sigmaIEIE_901xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_901 = new TH1F( "ph_sigmaIEIE_901", "", 2, ph_sigmaIEIE_901xarr );

 double ph_sigmaIEIE_902xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_902 = new TH1F( "ph_sigmaIEIE_902", "", 2, ph_sigmaIEIE_902xarr );

 double ph_sigmaIEIE_903xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_903 = new TH1F( "ph_sigmaIEIE_903", "", 2, ph_sigmaIEIE_903xarr );

 double ph_sigmaIEIE_904xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_904 = new TH1F( "ph_sigmaIEIE_904", "", 2, ph_sigmaIEIE_904xarr );

 double ph_sigmaIEIE_905xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_905 = new TH1F( "ph_sigmaIEIE_905", "", 2, ph_sigmaIEIE_905xarr );

 double ph_sigmaIEIE_906xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_906 = new TH1F( "ph_sigmaIEIE_906", "", 2, ph_sigmaIEIE_906xarr );

 double ph_sigmaIEIE_907xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_907 = new TH1F( "ph_sigmaIEIE_907", "", 2, ph_sigmaIEIE_907xarr );

 double ph_sigmaIEIE_908xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_908 = new TH1F( "ph_sigmaIEIE_908", "", 2, ph_sigmaIEIE_908xarr );

 double ph_sigmaIEIE_909xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_909 = new TH1F( "ph_sigmaIEIE_909", "", 2, ph_sigmaIEIE_909xarr );

 double ph_sigmaIEIE_910xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_910 = new TH1F( "ph_sigmaIEIE_910", "", 2, ph_sigmaIEIE_910xarr );

 double ph_sigmaIEIE_911xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_911 = new TH1F( "ph_sigmaIEIE_911", "", 2, ph_sigmaIEIE_911xarr );

 double ph_sigmaIEIE_912xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_912 = new TH1F( "ph_sigmaIEIE_912", "", 2, ph_sigmaIEIE_912xarr );

  hist_ph_sigmaIEIE_913 = new TH1F( "ph_sigmaIEIE_913", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_914 = new TH1F( "ph_sigmaIEIE_914", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_915 = new TH1F( "ph_sigmaIEIE_915", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_916 = new TH1F( "ph_sigmaIEIE_916", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_917 = new TH1F( "ph_sigmaIEIE_917", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_918 = new TH1F( "ph_sigmaIEIE_918", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_919 = new TH1F( "ph_sigmaIEIE_919", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_920 = new TH1F( "ph_sigmaIEIE_920", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_921 = new TH1F( "ph_sigmaIEIE_921", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_922 = new TH1F( "ph_sigmaIEIE_922", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_923 = new TH1F( "ph_sigmaIEIE_923", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_924 = new TH1F( "ph_sigmaIEIE_924", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_925 = new TH1F( "ph_sigmaIEIE_925", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_926 = new TH1F( "ph_sigmaIEIE_926", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_927 = new TH1F( "ph_sigmaIEIE_927", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_928 = new TH1F( "ph_sigmaIEIE_928", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_929 = new TH1F( "ph_sigmaIEIE_929", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_930 = new TH1F( "ph_sigmaIEIE_930", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_931 = new TH1F( "ph_sigmaIEIE_931", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_932 = new TH1F( "ph_sigmaIEIE_932", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_933 = new TH1F( "ph_sigmaIEIE_933", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_934 = new TH1F( "ph_sigmaIEIE_934", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_935 = new TH1F( "ph_sigmaIEIE_935", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_936 = new TH1F( "ph_sigmaIEIE_936", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_937 = new TH1F( "ph_sigmaIEIE_937", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_938 = new TH1F( "ph_sigmaIEIE_938", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_939 = new TH1F( "ph_sigmaIEIE_939", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_940 = new TH1F( "ph_sigmaIEIE_940", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_941 = new TH1F( "ph_sigmaIEIE_941", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_942 = new TH1F( "ph_sigmaIEIE_942", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_943 = new TH1F( "ph_sigmaIEIE_943", "", 30, 0.000000, 0.030000 );

  hist_ph_sigmaIEIE_944 = new TH1F( "ph_sigmaIEIE_944", "", 30, 0.000000, 0.030000 );

 double ph_sigmaIEIE_945xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_945 = new TH1F( "ph_sigmaIEIE_945", "", 2, ph_sigmaIEIE_945xarr );

 double ph_sigmaIEIE_946xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_946 = new TH1F( "ph_sigmaIEIE_946", "", 2, ph_sigmaIEIE_946xarr );

 double ph_sigmaIEIE_947xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_947 = new TH1F( "ph_sigmaIEIE_947", "", 2, ph_sigmaIEIE_947xarr );

 double ph_sigmaIEIE_948xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_948 = new TH1F( "ph_sigmaIEIE_948", "", 2, ph_sigmaIEIE_948xarr );

 double ph_sigmaIEIE_949xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_949 = new TH1F( "ph_sigmaIEIE_949", "", 2, ph_sigmaIEIE_949xarr );

 double ph_sigmaIEIE_950xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_950 = new TH1F( "ph_sigmaIEIE_950", "", 2, ph_sigmaIEIE_950xarr );

 double ph_sigmaIEIE_951xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_951 = new TH1F( "ph_sigmaIEIE_951", "", 2, ph_sigmaIEIE_951xarr );

 double ph_sigmaIEIE_952xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_952 = new TH1F( "ph_sigmaIEIE_952", "", 2, ph_sigmaIEIE_952xarr );

 double ph_sigmaIEIE_953xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_953 = new TH1F( "ph_sigmaIEIE_953", "", 2, ph_sigmaIEIE_953xarr );

 double ph_sigmaIEIE_954xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_954 = new TH1F( "ph_sigmaIEIE_954", "", 2, ph_sigmaIEIE_954xarr );

 double ph_sigmaIEIE_955xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_955 = new TH1F( "ph_sigmaIEIE_955", "", 2, ph_sigmaIEIE_955xarr );

 double ph_sigmaIEIE_956xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_956 = new TH1F( "ph_sigmaIEIE_956", "", 2, ph_sigmaIEIE_956xarr );

 double ph_sigmaIEIE_957xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_957 = new TH1F( "ph_sigmaIEIE_957", "", 2, ph_sigmaIEIE_957xarr );

 double ph_sigmaIEIE_958xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_958 = new TH1F( "ph_sigmaIEIE_958", "", 2, ph_sigmaIEIE_958xarr );

 double ph_sigmaIEIE_959xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_959 = new TH1F( "ph_sigmaIEIE_959", "", 2, ph_sigmaIEIE_959xarr );

 double ph_sigmaIEIE_960xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_960 = new TH1F( "ph_sigmaIEIE_960", "", 2, ph_sigmaIEIE_960xarr );

 double ph_sigmaIEIE_961xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_961 = new TH1F( "ph_sigmaIEIE_961", "", 2, ph_sigmaIEIE_961xarr );

 double ph_sigmaIEIE_962xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_962 = new TH1F( "ph_sigmaIEIE_962", "", 2, ph_sigmaIEIE_962xarr );

 double ph_sigmaIEIE_963xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_963 = new TH1F( "ph_sigmaIEIE_963", "", 2, ph_sigmaIEIE_963xarr );

 double ph_sigmaIEIE_964xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_964 = new TH1F( "ph_sigmaIEIE_964", "", 2, ph_sigmaIEIE_964xarr );

 double ph_sigmaIEIE_965xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_965 = new TH1F( "ph_sigmaIEIE_965", "", 2, ph_sigmaIEIE_965xarr );

 double ph_sigmaIEIE_966xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_966 = new TH1F( "ph_sigmaIEIE_966", "", 2, ph_sigmaIEIE_966xarr );

 double ph_sigmaIEIE_967xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_967 = new TH1F( "ph_sigmaIEIE_967", "", 2, ph_sigmaIEIE_967xarr );

 double ph_sigmaIEIE_968xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_968 = new TH1F( "ph_sigmaIEIE_968", "", 2, ph_sigmaIEIE_968xarr );

 double ph_sigmaIEIE_969xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_969 = new TH1F( "ph_sigmaIEIE_969", "", 2, ph_sigmaIEIE_969xarr );

 double ph_sigmaIEIE_970xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_970 = new TH1F( "ph_sigmaIEIE_970", "", 2, ph_sigmaIEIE_970xarr );

 double ph_sigmaIEIE_971xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_971 = new TH1F( "ph_sigmaIEIE_971", "", 2, ph_sigmaIEIE_971xarr );

 double ph_sigmaIEIE_972xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_972 = new TH1F( "ph_sigmaIEIE_972", "", 2, ph_sigmaIEIE_972xarr );

 double ph_sigmaIEIE_973xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_973 = new TH1F( "ph_sigmaIEIE_973", "", 2, ph_sigmaIEIE_973xarr );

 double ph_sigmaIEIE_974xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_974 = new TH1F( "ph_sigmaIEIE_974", "", 2, ph_sigmaIEIE_974xarr );

 double ph_sigmaIEIE_975xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_975 = new TH1F( "ph_sigmaIEIE_975", "", 2, ph_sigmaIEIE_975xarr );

 double ph_sigmaIEIE_976xarr[3] = {0,0.011,0.03}; 
  hist_ph_sigmaIEIE_976 = new TH1F( "ph_sigmaIEIE_976", "", 2, ph_sigmaIEIE_976xarr );

  hist_ph_sigmaIEIE_977 = new TH1F( "ph_sigmaIEIE_977", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_978 = new TH1F( "ph_sigmaIEIE_978", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_979 = new TH1F( "ph_sigmaIEIE_979", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_980 = new TH1F( "ph_sigmaIEIE_980", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_981 = new TH1F( "ph_sigmaIEIE_981", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_982 = new TH1F( "ph_sigmaIEIE_982", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_983 = new TH1F( "ph_sigmaIEIE_983", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_984 = new TH1F( "ph_sigmaIEIE_984", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_985 = new TH1F( "ph_sigmaIEIE_985", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_986 = new TH1F( "ph_sigmaIEIE_986", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_987 = new TH1F( "ph_sigmaIEIE_987", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_988 = new TH1F( "ph_sigmaIEIE_988", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_989 = new TH1F( "ph_sigmaIEIE_989", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_990 = new TH1F( "ph_sigmaIEIE_990", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_991 = new TH1F( "ph_sigmaIEIE_991", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_992 = new TH1F( "ph_sigmaIEIE_992", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_993 = new TH1F( "ph_sigmaIEIE_993", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_994 = new TH1F( "ph_sigmaIEIE_994", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_995 = new TH1F( "ph_sigmaIEIE_995", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_996 = new TH1F( "ph_sigmaIEIE_996", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_997 = new TH1F( "ph_sigmaIEIE_997", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_998 = new TH1F( "ph_sigmaIEIE_998", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_999 = new TH1F( "ph_sigmaIEIE_999", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_1000 = new TH1F( "ph_sigmaIEIE_1000", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_1001 = new TH1F( "ph_sigmaIEIE_1001", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_1002 = new TH1F( "ph_sigmaIEIE_1002", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_1003 = new TH1F( "ph_sigmaIEIE_1003", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_1004 = new TH1F( "ph_sigmaIEIE_1004", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_1005 = new TH1F( "ph_sigmaIEIE_1005", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_1006 = new TH1F( "ph_sigmaIEIE_1006", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_1007 = new TH1F( "ph_sigmaIEIE_1007", "", 20, 0.000000, 0.100000 );

  hist_ph_sigmaIEIE_1008 = new TH1F( "ph_sigmaIEIE_1008", "", 20, 0.000000, 0.100000 );

 double ph_sigmaIEIE_1009xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1009 = new TH1F( "ph_sigmaIEIE_1009", "", 2, ph_sigmaIEIE_1009xarr );

 double ph_sigmaIEIE_1010xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1010 = new TH1F( "ph_sigmaIEIE_1010", "", 2, ph_sigmaIEIE_1010xarr );

 double ph_sigmaIEIE_1011xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1011 = new TH1F( "ph_sigmaIEIE_1011", "", 2, ph_sigmaIEIE_1011xarr );

 double ph_sigmaIEIE_1012xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1012 = new TH1F( "ph_sigmaIEIE_1012", "", 2, ph_sigmaIEIE_1012xarr );

 double ph_sigmaIEIE_1013xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1013 = new TH1F( "ph_sigmaIEIE_1013", "", 2, ph_sigmaIEIE_1013xarr );

 double ph_sigmaIEIE_1014xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1014 = new TH1F( "ph_sigmaIEIE_1014", "", 2, ph_sigmaIEIE_1014xarr );

 double ph_sigmaIEIE_1015xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1015 = new TH1F( "ph_sigmaIEIE_1015", "", 2, ph_sigmaIEIE_1015xarr );

 double ph_sigmaIEIE_1016xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1016 = new TH1F( "ph_sigmaIEIE_1016", "", 2, ph_sigmaIEIE_1016xarr );

 double ph_sigmaIEIE_1017xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1017 = new TH1F( "ph_sigmaIEIE_1017", "", 2, ph_sigmaIEIE_1017xarr );

 double ph_sigmaIEIE_1018xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1018 = new TH1F( "ph_sigmaIEIE_1018", "", 2, ph_sigmaIEIE_1018xarr );

 double ph_sigmaIEIE_1019xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1019 = new TH1F( "ph_sigmaIEIE_1019", "", 2, ph_sigmaIEIE_1019xarr );

 double ph_sigmaIEIE_1020xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1020 = new TH1F( "ph_sigmaIEIE_1020", "", 2, ph_sigmaIEIE_1020xarr );

 double ph_sigmaIEIE_1021xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1021 = new TH1F( "ph_sigmaIEIE_1021", "", 2, ph_sigmaIEIE_1021xarr );

 double ph_sigmaIEIE_1022xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1022 = new TH1F( "ph_sigmaIEIE_1022", "", 2, ph_sigmaIEIE_1022xarr );

 double ph_sigmaIEIE_1023xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1023 = new TH1F( "ph_sigmaIEIE_1023", "", 2, ph_sigmaIEIE_1023xarr );

 double ph_sigmaIEIE_1024xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1024 = new TH1F( "ph_sigmaIEIE_1024", "", 2, ph_sigmaIEIE_1024xarr );

 double ph_sigmaIEIE_1025xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1025 = new TH1F( "ph_sigmaIEIE_1025", "", 2, ph_sigmaIEIE_1025xarr );

 double ph_sigmaIEIE_1026xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1026 = new TH1F( "ph_sigmaIEIE_1026", "", 2, ph_sigmaIEIE_1026xarr );

 double ph_sigmaIEIE_1027xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1027 = new TH1F( "ph_sigmaIEIE_1027", "", 2, ph_sigmaIEIE_1027xarr );

 double ph_sigmaIEIE_1028xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1028 = new TH1F( "ph_sigmaIEIE_1028", "", 2, ph_sigmaIEIE_1028xarr );

 double ph_sigmaIEIE_1029xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1029 = new TH1F( "ph_sigmaIEIE_1029", "", 2, ph_sigmaIEIE_1029xarr );

 double ph_sigmaIEIE_1030xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1030 = new TH1F( "ph_sigmaIEIE_1030", "", 2, ph_sigmaIEIE_1030xarr );

 double ph_sigmaIEIE_1031xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1031 = new TH1F( "ph_sigmaIEIE_1031", "", 2, ph_sigmaIEIE_1031xarr );

 double ph_sigmaIEIE_1032xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1032 = new TH1F( "ph_sigmaIEIE_1032", "", 2, ph_sigmaIEIE_1032xarr );

 double ph_sigmaIEIE_1033xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1033 = new TH1F( "ph_sigmaIEIE_1033", "", 2, ph_sigmaIEIE_1033xarr );

 double ph_sigmaIEIE_1034xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1034 = new TH1F( "ph_sigmaIEIE_1034", "", 2, ph_sigmaIEIE_1034xarr );

 double ph_sigmaIEIE_1035xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1035 = new TH1F( "ph_sigmaIEIE_1035", "", 2, ph_sigmaIEIE_1035xarr );

 double ph_sigmaIEIE_1036xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1036 = new TH1F( "ph_sigmaIEIE_1036", "", 2, ph_sigmaIEIE_1036xarr );

 double ph_sigmaIEIE_1037xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1037 = new TH1F( "ph_sigmaIEIE_1037", "", 2, ph_sigmaIEIE_1037xarr );

 double ph_sigmaIEIE_1038xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1038 = new TH1F( "ph_sigmaIEIE_1038", "", 2, ph_sigmaIEIE_1038xarr );

 double ph_sigmaIEIE_1039xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1039 = new TH1F( "ph_sigmaIEIE_1039", "", 2, ph_sigmaIEIE_1039xarr );

 double ph_sigmaIEIE_1040xarr[3] = {0,0.033,0.1}; 
  hist_ph_sigmaIEIE_1040 = new TH1F( "ph_sigmaIEIE_1040", "", 2, ph_sigmaIEIE_1040xarr );

}
bool RunModule::execute( std::vector<ModuleConfig> & configs ) {
    Drawph_pt_26(  ); 
    Drawph_pt_27(  ); 
    Drawph_pt_28(  ); 
    Drawph_pt_29(  ); 
    Drawph_pt_30(  ); 
    Drawph_pt_31(  ); 
    Drawph_pt_32(  ); 
    Drawph_pt_33(  ); 
    Drawph_pt_34(  ); 
    Drawph_pt_35(  ); 
    Drawph_pt_36(  ); 
    Drawph_pt_37(  ); 
    Drawph_pt_38(  ); 
    Drawph_pt_39(  ); 
    Drawph_pt_40(  ); 
    Drawph_pt_41(  ); 
    DrawleadPhot_sublLepDR(  ); 
    DrawleadPhot_leadLepDR(  ); 
    Drawm_leplepph(  ); 
    Drawm_leplepph_m_leplep(  ); 
    DrawleadPhot_leadLepDR_0(  ); 
    DrawleadPhot_leadLepDR_1(  ); 
    Drawph_sigmaIEIE_59(  ); 
    Drawph_sigmaIEIE_60(  ); 
    Drawph_sigmaIEIE_61(  ); 
    Drawph_sigmaIEIE_62(  ); 
    Drawph_sigmaIEIE_63(  ); 
    Drawph_sigmaIEIE_64(  ); 
    Drawph_sigmaIEIE_65(  ); 
    Drawph_sigmaIEIE_66(  ); 
    DrawleadPhot_sublLepDR_0(  ); 
    DrawleadPhot_leadLepDR_2(  ); 
    Drawph_sigmaIEIE_67(  ); 
    Drawph_sigmaIEIE_68(  ); 
    Drawph_sigmaIEIE_69(  ); 
    Drawph_sigmaIEIE_70(  ); 
    Drawph_sigmaIEIE_71(  ); 
    Drawph_sigmaIEIE_72(  ); 
    Drawph_sigmaIEIE_73(  ); 
    Drawph_sigmaIEIE_74(  ); 
    Drawph_sigmaIEIE_75(  ); 
    Drawph_sigmaIEIE_76(  ); 
    Drawph_sigmaIEIE_77(  ); 
    Drawph_sigmaIEIE_78(  ); 
    Drawph_sigmaIEIE_79(  ); 
    Drawph_sigmaIEIE_80(  ); 
    Drawph_sigmaIEIE_81(  ); 
    Drawph_sigmaIEIE_82(  ); 
    Drawph_sigmaIEIE_83(  ); 
    Drawph_sigmaIEIE_84(  ); 
    Drawph_sigmaIEIE_85(  ); 
    Drawph_sigmaIEIE_86(  ); 
    Drawph_sigmaIEIE_87(  ); 
    Drawph_sigmaIEIE_88(  ); 
    Drawph_sigmaIEIE_89(  ); 
    Drawph_sigmaIEIE_90(  ); 
    Drawph_sigmaIEIE_91(  ); 
    Drawph_sigmaIEIE_92(  ); 
    Drawph_sigmaIEIE_93(  ); 
    Drawph_sigmaIEIE_94(  ); 
    Drawph_sigmaIEIE_95(  ); 
    Drawph_sigmaIEIE_96(  ); 
    Drawph_sigmaIEIE_97(  ); 
    Drawph_sigmaIEIE_98(  ); 
    Drawph_sigmaIEIE_99(  ); 
    Drawph_sigmaIEIE_100(  ); 
    Drawph_sigmaIEIE_101(  ); 
    Drawph_sigmaIEIE_102(  ); 
    Drawph_sigmaIEIE_103(  ); 
    Drawph_sigmaIEIE_104(  ); 
    Drawph_sigmaIEIE_105(  ); 
    Drawph_sigmaIEIE_106(  ); 
    Drawph_sigmaIEIE_107(  ); 
    Drawph_sigmaIEIE_108(  ); 
    Drawph_sigmaIEIE_109(  ); 
    Drawph_sigmaIEIE_110(  ); 
    Drawph_sigmaIEIE_111(  ); 
    Drawph_sigmaIEIE_112(  ); 
    Drawph_sigmaIEIE_113(  ); 
    Drawph_sigmaIEIE_114(  ); 
    Drawph_sigmaIEIE_115(  ); 
    Drawph_sigmaIEIE_116(  ); 
    Drawph_sigmaIEIE_117(  ); 
    Drawph_sigmaIEIE_118(  ); 
    Drawph_sigmaIEIE_119(  ); 
    Drawph_sigmaIEIE_120(  ); 
    Drawph_sigmaIEIE_121(  ); 
    Drawph_sigmaIEIE_122(  ); 
    Drawph_sigmaIEIE_123(  ); 
    Drawph_sigmaIEIE_124(  ); 
    Drawph_sigmaIEIE_125(  ); 
    Drawph_sigmaIEIE_126(  ); 
    Drawph_sigmaIEIE_127(  ); 
    Drawph_sigmaIEIE_128(  ); 
    Drawph_sigmaIEIE_129(  ); 
    Drawph_sigmaIEIE_130(  ); 
    Drawph_sigmaIEIE_131(  ); 
    Drawph_sigmaIEIE_132(  ); 
    Drawph_sigmaIEIE_133(  ); 
    Drawph_sigmaIEIE_134(  ); 
    Drawph_sigmaIEIE_135(  ); 
    Drawph_sigmaIEIE_136(  ); 
    Drawph_sigmaIEIE_137(  ); 
    Drawph_sigmaIEIE_138(  ); 
    Drawph_sigmaIEIE_139(  ); 
    Drawph_sigmaIEIE_140(  ); 
    Drawph_sigmaIEIE_141(  ); 
    Drawph_sigmaIEIE_142(  ); 
    Drawph_sigmaIEIE_143(  ); 
    Drawph_sigmaIEIE_144(  ); 
    Drawph_pt_42(  ); 
    Drawph_pt_43(  ); 
    Drawph_pt_44(  ); 
    Drawph_pt_45(  ); 
    Drawph_pt_46(  ); 
    Drawph_pt_47(  ); 
    Drawph_pt_48(  ); 
    Drawph_pt_49(  ); 
    Drawph_pt_50(  ); 
    Drawph_pt_51(  ); 
    Drawph_pt_52(  ); 
    Drawph_pt_53(  ); 
    Drawph_pt_54(  ); 
    Drawph_pt_55(  ); 
    Drawph_pt_56(  ); 
    Drawph_pt_57(  ); 
    Drawph_pt_58(  ); 
    Drawph_pt_59(  ); 
    Drawph_pt_60(  ); 
    Drawph_pt_61(  ); 
    Drawph_pt_62(  ); 
    Drawph_pt_63(  ); 
    Drawph_pt_64(  ); 
    Drawph_pt_65(  ); 
    Drawph_sigmaIEIE_145(  ); 
    Drawph_sigmaIEIE_146(  ); 
    Drawph_sigmaIEIE_147(  ); 
    Drawph_sigmaIEIE_148(  ); 
    Drawph_sigmaIEIE_149(  ); 
    Drawph_sigmaIEIE_150(  ); 
    Drawph_sigmaIEIE_151(  ); 
    Drawph_sigmaIEIE_152(  ); 
    Drawph_sigmaIEIE_153(  ); 
    Drawph_sigmaIEIE_154(  ); 
    Drawph_sigmaIEIE_155(  ); 
    Drawph_sigmaIEIE_156(  ); 
    Drawph_sigmaIEIE_157(  ); 
    Drawph_sigmaIEIE_158(  ); 
    Drawph_sigmaIEIE_159(  ); 
    Drawph_sigmaIEIE_160(  ); 
    Drawph_sigmaIEIE_161(  ); 
    Drawph_sigmaIEIE_162(  ); 
    Drawph_sigmaIEIE_163(  ); 
    Drawph_sigmaIEIE_164(  ); 
    Drawph_sigmaIEIE_165(  ); 
    Drawph_sigmaIEIE_166(  ); 
    Drawph_sigmaIEIE_167(  ); 
    Drawph_sigmaIEIE_168(  ); 
    Drawph_sigmaIEIE_169(  ); 
    Drawph_sigmaIEIE_170(  ); 
    Drawph_sigmaIEIE_171(  ); 
    Drawph_sigmaIEIE_172(  ); 
    Drawph_sigmaIEIE_173(  ); 
    Drawph_sigmaIEIE_174(  ); 
    Drawph_sigmaIEIE_175(  ); 
    Drawph_sigmaIEIE_176(  ); 
    Drawph_sigmaIEIE_177(  ); 
    Drawph_sigmaIEIE_178(  ); 
    Drawph_sigmaIEIE_179(  ); 
    Drawph_sigmaIEIE_180(  ); 
    Drawph_sigmaIEIE_181(  ); 
    Drawph_sigmaIEIE_182(  ); 
    Drawph_sigmaIEIE_183(  ); 
    Drawph_sigmaIEIE_184(  ); 
    Drawph_sigmaIEIE_185(  ); 
    Drawph_sigmaIEIE_186(  ); 
    Drawph_sigmaIEIE_187(  ); 
    Drawph_sigmaIEIE_188(  ); 
    Drawph_sigmaIEIE_189(  ); 
    Drawph_sigmaIEIE_190(  ); 
    Drawph_sigmaIEIE_191(  ); 
    Drawph_sigmaIEIE_192(  ); 
    Drawph_sigmaIEIE_193(  ); 
    Drawph_sigmaIEIE_194(  ); 
    Drawph_sigmaIEIE_195(  ); 
    Drawph_sigmaIEIE_196(  ); 
    Drawph_sigmaIEIE_197(  ); 
    Drawph_sigmaIEIE_198(  ); 
    Drawph_sigmaIEIE_199(  ); 
    Drawph_sigmaIEIE_200(  ); 
    Drawph_sigmaIEIE_201(  ); 
    Drawph_sigmaIEIE_202(  ); 
    Drawph_sigmaIEIE_203(  ); 
    Drawph_sigmaIEIE_204(  ); 
    Drawph_sigmaIEIE_205(  ); 
    Drawph_sigmaIEIE_206(  ); 
    Drawph_sigmaIEIE_207(  ); 
    Drawph_sigmaIEIE_208(  ); 
    Drawph_sigmaIEIE_209(  ); 
    Drawph_sigmaIEIE_210(  ); 
    Drawph_sigmaIEIE_211(  ); 
    Drawph_sigmaIEIE_212(  ); 
    Drawph_sigmaIEIE_213(  ); 
    Drawph_sigmaIEIE_214(  ); 
    Drawph_sigmaIEIE_215(  ); 
    Drawph_sigmaIEIE_216(  ); 
    Drawph_sigmaIEIE_217(  ); 
    Drawph_sigmaIEIE_218(  ); 
    Drawph_sigmaIEIE_219(  ); 
    Drawph_sigmaIEIE_220(  ); 
    Drawph_sigmaIEIE_221(  ); 
    Drawph_sigmaIEIE_222(  ); 
    Drawph_sigmaIEIE_223(  ); 
    Drawph_sigmaIEIE_224(  ); 
    Drawph_sigmaIEIE_225(  ); 
    Drawph_sigmaIEIE_226(  ); 
    Drawph_sigmaIEIE_227(  ); 
    Drawph_sigmaIEIE_228(  ); 
    Drawph_sigmaIEIE_229(  ); 
    Drawph_sigmaIEIE_230(  ); 
    Drawph_sigmaIEIE_231(  ); 
    Drawph_sigmaIEIE_232(  ); 
    Drawph_sigmaIEIE_233(  ); 
    Drawph_sigmaIEIE_234(  ); 
    Drawph_sigmaIEIE_235(  ); 
    Drawph_sigmaIEIE_236(  ); 
    Drawph_sigmaIEIE_237(  ); 
    Drawph_sigmaIEIE_238(  ); 
    Drawph_sigmaIEIE_239(  ); 
    Drawph_sigmaIEIE_240(  ); 
    Drawph_sigmaIEIE_241(  ); 
    Drawph_sigmaIEIE_242(  ); 
    Drawph_sigmaIEIE_243(  ); 
    Drawph_sigmaIEIE_244(  ); 
    Drawph_sigmaIEIE_245(  ); 
    Drawph_sigmaIEIE_246(  ); 
    Drawph_sigmaIEIE_247(  ); 
    Drawph_sigmaIEIE_248(  ); 
    Drawph_sigmaIEIE_249(  ); 
    Drawph_sigmaIEIE_250(  ); 
    Drawph_sigmaIEIE_251(  ); 
    Drawph_sigmaIEIE_252(  ); 
    Drawph_sigmaIEIE_253(  ); 
    Drawph_sigmaIEIE_254(  ); 
    Drawph_sigmaIEIE_255(  ); 
    Drawph_sigmaIEIE_256(  ); 
    Drawph_sigmaIEIE_257(  ); 
    Drawph_sigmaIEIE_258(  ); 
    Drawph_sigmaIEIE_259(  ); 
    Drawph_sigmaIEIE_260(  ); 
    Drawph_sigmaIEIE_261(  ); 
    Drawph_sigmaIEIE_262(  ); 
    Drawph_sigmaIEIE_263(  ); 
    Drawph_sigmaIEIE_264(  ); 
    Drawph_sigmaIEIE_265(  ); 
    Drawph_sigmaIEIE_266(  ); 
    Drawph_sigmaIEIE_267(  ); 
    Drawph_sigmaIEIE_268(  ); 
    Drawph_sigmaIEIE_269(  ); 
    Drawph_sigmaIEIE_270(  ); 
    Drawph_sigmaIEIE_271(  ); 
    Drawph_sigmaIEIE_272(  ); 
    Drawph_sigmaIEIE_273(  ); 
    Drawph_sigmaIEIE_274(  ); 
    Drawph_sigmaIEIE_275(  ); 
    Drawph_sigmaIEIE_276(  ); 
    Drawph_sigmaIEIE_277(  ); 
    Drawph_sigmaIEIE_278(  ); 
    Drawph_sigmaIEIE_279(  ); 
    Drawph_sigmaIEIE_280(  ); 
    Drawph_sigmaIEIE_281(  ); 
    Drawph_sigmaIEIE_282(  ); 
    Drawph_sigmaIEIE_283(  ); 
    Drawph_sigmaIEIE_284(  ); 
    Drawph_sigmaIEIE_285(  ); 
    Drawph_sigmaIEIE_286(  ); 
    Drawph_sigmaIEIE_287(  ); 
    Drawph_sigmaIEIE_288(  ); 
    Drawph_sigmaIEIE_289(  ); 
    Drawph_sigmaIEIE_290(  ); 
    Drawph_sigmaIEIE_291(  ); 
    Drawph_sigmaIEIE_292(  ); 
    Drawph_sigmaIEIE_293(  ); 
    Drawph_sigmaIEIE_294(  ); 
    Drawph_sigmaIEIE_295(  ); 
    Drawph_sigmaIEIE_296(  ); 
    Drawph_sigmaIEIE_297(  ); 
    Drawph_sigmaIEIE_298(  ); 
    Drawph_sigmaIEIE_299(  ); 
    Drawph_sigmaIEIE_300(  ); 
    Drawph_sigmaIEIE_301(  ); 
    Drawph_sigmaIEIE_302(  ); 
    Drawph_sigmaIEIE_303(  ); 
    Drawph_sigmaIEIE_304(  ); 
    Drawph_sigmaIEIE_305(  ); 
    Drawph_sigmaIEIE_306(  ); 
    Drawph_sigmaIEIE_307(  ); 
    Drawph_sigmaIEIE_308(  ); 
    Drawph_sigmaIEIE_309(  ); 
    Drawph_sigmaIEIE_310(  ); 
    Drawph_sigmaIEIE_311(  ); 
    Drawph_sigmaIEIE_312(  ); 
    Drawph_sigmaIEIE_313(  ); 
    Drawph_sigmaIEIE_314(  ); 
    Drawph_sigmaIEIE_315(  ); 
    Drawph_sigmaIEIE_316(  ); 
    Drawph_sigmaIEIE_317(  ); 
    Drawph_sigmaIEIE_318(  ); 
    Drawph_sigmaIEIE_319(  ); 
    Drawph_sigmaIEIE_320(  ); 
    Drawph_sigmaIEIE_321(  ); 
    Drawph_sigmaIEIE_322(  ); 
    Drawph_sigmaIEIE_323(  ); 
    Drawph_sigmaIEIE_324(  ); 
    Drawph_sigmaIEIE_325(  ); 
    Drawph_sigmaIEIE_326(  ); 
    Drawph_sigmaIEIE_327(  ); 
    Drawph_sigmaIEIE_328(  ); 
    Drawph_sigmaIEIE_329(  ); 
    Drawph_sigmaIEIE_330(  ); 
    Drawph_sigmaIEIE_331(  ); 
    Drawph_sigmaIEIE_332(  ); 
    Drawph_sigmaIEIE_333(  ); 
    Drawph_sigmaIEIE_334(  ); 
    Drawph_sigmaIEIE_335(  ); 
    Drawph_sigmaIEIE_336(  ); 
    Drawph_sigmaIEIE_337(  ); 
    Drawph_sigmaIEIE_338(  ); 
    Drawph_sigmaIEIE_339(  ); 
    Drawph_sigmaIEIE_340(  ); 
    Drawph_sigmaIEIE_341(  ); 
    Drawph_sigmaIEIE_342(  ); 
    Drawph_sigmaIEIE_343(  ); 
    Drawph_sigmaIEIE_344(  ); 
    Drawph_sigmaIEIE_345(  ); 
    Drawph_sigmaIEIE_346(  ); 
    Drawph_sigmaIEIE_347(  ); 
    Drawph_sigmaIEIE_348(  ); 
    Drawph_sigmaIEIE_349(  ); 
    Drawph_sigmaIEIE_350(  ); 
    Drawph_sigmaIEIE_351(  ); 
    Drawph_sigmaIEIE_352(  ); 
    Drawph_sigmaIEIE_353(  ); 
    Drawph_sigmaIEIE_354(  ); 
    Drawph_sigmaIEIE_355(  ); 
    Drawph_sigmaIEIE_356(  ); 
    Drawph_sigmaIEIE_357(  ); 
    Drawph_sigmaIEIE_358(  ); 
    Drawph_sigmaIEIE_359(  ); 
    Drawph_sigmaIEIE_360(  ); 
    Drawph_sigmaIEIE_361(  ); 
    Drawph_sigmaIEIE_362(  ); 
    Drawph_sigmaIEIE_363(  ); 
    Drawph_sigmaIEIE_364(  ); 
    Drawph_sigmaIEIE_365(  ); 
    Drawph_sigmaIEIE_366(  ); 
    Drawph_sigmaIEIE_367(  ); 
    Drawph_sigmaIEIE_368(  ); 
    Drawph_sigmaIEIE_369(  ); 
    Drawph_sigmaIEIE_370(  ); 
    Drawph_sigmaIEIE_371(  ); 
    Drawph_sigmaIEIE_372(  ); 
    Drawph_sigmaIEIE_373(  ); 
    Drawph_sigmaIEIE_374(  ); 
    Drawph_sigmaIEIE_375(  ); 
    Drawph_sigmaIEIE_376(  ); 
    Drawph_sigmaIEIE_377(  ); 
    Drawph_sigmaIEIE_378(  ); 
    Drawph_sigmaIEIE_379(  ); 
    Drawph_sigmaIEIE_380(  ); 
    Drawph_sigmaIEIE_381(  ); 
    Drawph_sigmaIEIE_382(  ); 
    Drawph_sigmaIEIE_383(  ); 
    Drawph_sigmaIEIE_384(  ); 
    Drawph_sigmaIEIE_385(  ); 
    Drawph_sigmaIEIE_386(  ); 
    Drawph_sigmaIEIE_387(  ); 
    Drawph_sigmaIEIE_388(  ); 
    Drawph_sigmaIEIE_389(  ); 
    Drawph_sigmaIEIE_390(  ); 
    Drawph_sigmaIEIE_391(  ); 
    Drawph_sigmaIEIE_392(  ); 
    Drawph_sigmaIEIE_393(  ); 
    Drawph_sigmaIEIE_394(  ); 
    Drawph_sigmaIEIE_395(  ); 
    Drawph_sigmaIEIE_396(  ); 
    Drawph_sigmaIEIE_397(  ); 
    Drawph_sigmaIEIE_398(  ); 
    Drawph_sigmaIEIE_399(  ); 
    Drawph_sigmaIEIE_400(  ); 
    Drawph_sigmaIEIE_401(  ); 
    Drawph_sigmaIEIE_402(  ); 
    Drawph_sigmaIEIE_403(  ); 
    Drawph_sigmaIEIE_404(  ); 
    Drawph_sigmaIEIE_405(  ); 
    Drawph_sigmaIEIE_406(  ); 
    Drawph_sigmaIEIE_407(  ); 
    Drawph_sigmaIEIE_408(  ); 
    Drawph_sigmaIEIE_409(  ); 
    Drawph_sigmaIEIE_410(  ); 
    Drawph_sigmaIEIE_411(  ); 
    Drawph_sigmaIEIE_412(  ); 
    Drawph_sigmaIEIE_413(  ); 
    Drawph_sigmaIEIE_414(  ); 
    Drawph_sigmaIEIE_415(  ); 
    Drawph_sigmaIEIE_416(  ); 
    Drawph_sigmaIEIE_417(  ); 
    Drawph_sigmaIEIE_418(  ); 
    Drawph_sigmaIEIE_419(  ); 
    Drawph_sigmaIEIE_420(  ); 
    Drawph_sigmaIEIE_421(  ); 
    Drawph_sigmaIEIE_422(  ); 
    Drawph_sigmaIEIE_423(  ); 
    Drawph_sigmaIEIE_424(  ); 
    Drawph_sigmaIEIE_425(  ); 
    Drawph_sigmaIEIE_426(  ); 
    Drawph_sigmaIEIE_427(  ); 
    Drawph_sigmaIEIE_428(  ); 
    Drawph_sigmaIEIE_429(  ); 
    Drawph_sigmaIEIE_430(  ); 
    Drawph_sigmaIEIE_431(  ); 
    Drawph_sigmaIEIE_432(  ); 
    Drawph_sigmaIEIE_433(  ); 
    Drawph_sigmaIEIE_434(  ); 
    Drawph_sigmaIEIE_435(  ); 
    Drawph_sigmaIEIE_436(  ); 
    Drawph_sigmaIEIE_437(  ); 
    Drawph_sigmaIEIE_438(  ); 
    Drawph_sigmaIEIE_439(  ); 
    Drawph_sigmaIEIE_440(  ); 
    Drawph_sigmaIEIE_441(  ); 
    Drawph_sigmaIEIE_442(  ); 
    Drawph_sigmaIEIE_443(  ); 
    Drawph_sigmaIEIE_444(  ); 
    Drawph_sigmaIEIE_445(  ); 
    Drawph_sigmaIEIE_446(  ); 
    Drawph_sigmaIEIE_447(  ); 
    Drawph_sigmaIEIE_448(  ); 
    Drawph_sigmaIEIE_449(  ); 
    Drawph_sigmaIEIE_450(  ); 
    Drawph_sigmaIEIE_451(  ); 
    Drawph_sigmaIEIE_452(  ); 
    Drawph_sigmaIEIE_453(  ); 
    Drawph_sigmaIEIE_454(  ); 
    Drawph_sigmaIEIE_455(  ); 
    Drawph_sigmaIEIE_456(  ); 
    Drawph_sigmaIEIE_457(  ); 
    Drawph_sigmaIEIE_458(  ); 
    Drawph_sigmaIEIE_459(  ); 
    Drawph_sigmaIEIE_460(  ); 
    Drawph_sigmaIEIE_461(  ); 
    Drawph_sigmaIEIE_462(  ); 
    Drawph_sigmaIEIE_463(  ); 
    Drawph_sigmaIEIE_464(  ); 
    Drawph_sigmaIEIE_465(  ); 
    Drawph_sigmaIEIE_466(  ); 
    Drawph_sigmaIEIE_467(  ); 
    Drawph_sigmaIEIE_468(  ); 
    Drawph_sigmaIEIE_469(  ); 
    Drawph_sigmaIEIE_470(  ); 
    Drawph_sigmaIEIE_471(  ); 
    Drawph_sigmaIEIE_472(  ); 
    Drawph_sigmaIEIE_473(  ); 
    Drawph_sigmaIEIE_474(  ); 
    Drawph_sigmaIEIE_475(  ); 
    Drawph_sigmaIEIE_476(  ); 
    Drawph_sigmaIEIE_477(  ); 
    Drawph_sigmaIEIE_478(  ); 
    Drawph_sigmaIEIE_479(  ); 
    Drawph_sigmaIEIE_480(  ); 
    Drawph_sigmaIEIE_481(  ); 
    Drawph_sigmaIEIE_482(  ); 
    Drawph_sigmaIEIE_483(  ); 
    Drawph_sigmaIEIE_484(  ); 
    Drawph_sigmaIEIE_485(  ); 
    Drawph_sigmaIEIE_486(  ); 
    Drawph_sigmaIEIE_487(  ); 
    Drawph_sigmaIEIE_488(  ); 
    Drawph_sigmaIEIE_489(  ); 
    Drawph_sigmaIEIE_490(  ); 
    Drawph_sigmaIEIE_491(  ); 
    Drawph_sigmaIEIE_492(  ); 
    Drawph_sigmaIEIE_493(  ); 
    Drawph_sigmaIEIE_494(  ); 
    Drawph_sigmaIEIE_495(  ); 
    Drawph_sigmaIEIE_496(  ); 
    Drawph_sigmaIEIE_497(  ); 
    Drawph_sigmaIEIE_498(  ); 
    Drawph_sigmaIEIE_499(  ); 
    Drawph_sigmaIEIE_500(  ); 
    Drawph_sigmaIEIE_501(  ); 
    Drawph_sigmaIEIE_502(  ); 
    Drawph_sigmaIEIE_503(  ); 
    Drawph_sigmaIEIE_504(  ); 
    Drawph_sigmaIEIE_505(  ); 
    Drawph_sigmaIEIE_506(  ); 
    Drawph_sigmaIEIE_507(  ); 
    Drawph_sigmaIEIE_508(  ); 
    Drawph_sigmaIEIE_509(  ); 
    Drawph_sigmaIEIE_510(  ); 
    Drawph_sigmaIEIE_511(  ); 
    Drawph_sigmaIEIE_512(  ); 
    Drawph_sigmaIEIE_513(  ); 
    Drawph_sigmaIEIE_514(  ); 
    Drawph_sigmaIEIE_515(  ); 
    Drawph_sigmaIEIE_516(  ); 
    Drawph_sigmaIEIE_517(  ); 
    Drawph_sigmaIEIE_518(  ); 
    Drawph_sigmaIEIE_519(  ); 
    Drawph_sigmaIEIE_520(  ); 
    Drawph_sigmaIEIE_521(  ); 
    Drawph_sigmaIEIE_522(  ); 
    Drawph_sigmaIEIE_523(  ); 
    Drawph_sigmaIEIE_524(  ); 
    Drawph_sigmaIEIE_525(  ); 
    Drawph_sigmaIEIE_526(  ); 
    Drawph_sigmaIEIE_527(  ); 
    Drawph_sigmaIEIE_528(  ); 
    Drawph_sigmaIEIE_529(  ); 
    Drawph_sigmaIEIE_530(  ); 
    Drawph_sigmaIEIE_531(  ); 
    Drawph_sigmaIEIE_532(  ); 
    Drawph_sigmaIEIE_533(  ); 
    Drawph_sigmaIEIE_534(  ); 
    Drawph_sigmaIEIE_535(  ); 
    Drawph_sigmaIEIE_536(  ); 
    Drawph_sigmaIEIE_537(  ); 
    Drawph_sigmaIEIE_538(  ); 
    Drawph_sigmaIEIE_539(  ); 
    Drawph_sigmaIEIE_540(  ); 
    Drawph_sigmaIEIE_541(  ); 
    Drawph_sigmaIEIE_542(  ); 
    Drawph_sigmaIEIE_543(  ); 
    Drawph_sigmaIEIE_544(  ); 
    Drawph_sigmaIEIE_545(  ); 
    Drawph_sigmaIEIE_546(  ); 
    Drawph_sigmaIEIE_547(  ); 
    Drawph_sigmaIEIE_548(  ); 
    Drawph_sigmaIEIE_549(  ); 
    Drawph_sigmaIEIE_550(  ); 
    Drawph_sigmaIEIE_551(  ); 
    Drawph_sigmaIEIE_552(  ); 
    Drawph_sigmaIEIE_553(  ); 
    Drawph_sigmaIEIE_554(  ); 
    Drawph_sigmaIEIE_555(  ); 
    Drawph_sigmaIEIE_556(  ); 
    Drawph_sigmaIEIE_557(  ); 
    Drawph_sigmaIEIE_558(  ); 
    Drawph_sigmaIEIE_559(  ); 
    Drawph_sigmaIEIE_560(  ); 
    Drawph_sigmaIEIE_561(  ); 
    Drawph_sigmaIEIE_562(  ); 
    Drawph_sigmaIEIE_563(  ); 
    Drawph_sigmaIEIE_564(  ); 
    Drawph_sigmaIEIE_565(  ); 
    Drawph_sigmaIEIE_566(  ); 
    Drawph_sigmaIEIE_567(  ); 
    Drawph_sigmaIEIE_568(  ); 
    Drawph_sigmaIEIE_569(  ); 
    Drawph_sigmaIEIE_570(  ); 
    Drawph_sigmaIEIE_571(  ); 
    Drawph_sigmaIEIE_572(  ); 
    Drawph_sigmaIEIE_573(  ); 
    Drawph_sigmaIEIE_574(  ); 
    Drawph_sigmaIEIE_575(  ); 
    Drawph_sigmaIEIE_576(  ); 
    Drawph_sigmaIEIE_577(  ); 
    Drawph_sigmaIEIE_578(  ); 
    Drawph_sigmaIEIE_579(  ); 
    Drawph_sigmaIEIE_580(  ); 
    Drawph_sigmaIEIE_581(  ); 
    Drawph_sigmaIEIE_582(  ); 
    Drawph_sigmaIEIE_583(  ); 
    Drawph_sigmaIEIE_584(  ); 
    Drawph_sigmaIEIE_585(  ); 
    Drawph_sigmaIEIE_586(  ); 
    Drawph_sigmaIEIE_587(  ); 
    Drawph_sigmaIEIE_588(  ); 
    Drawph_sigmaIEIE_589(  ); 
    Drawph_sigmaIEIE_590(  ); 
    Drawph_sigmaIEIE_591(  ); 
    Drawph_sigmaIEIE_592(  ); 
    Drawph_sigmaIEIE_593(  ); 
    Drawph_sigmaIEIE_594(  ); 
    Drawph_sigmaIEIE_595(  ); 
    Drawph_sigmaIEIE_596(  ); 
    Drawph_sigmaIEIE_597(  ); 
    Drawph_sigmaIEIE_598(  ); 
    Drawph_sigmaIEIE_599(  ); 
    Drawph_sigmaIEIE_600(  ); 
    Drawph_sigmaIEIE_601(  ); 
    Drawph_sigmaIEIE_602(  ); 
    Drawph_sigmaIEIE_603(  ); 
    Drawph_sigmaIEIE_604(  ); 
    Drawph_sigmaIEIE_605(  ); 
    Drawph_sigmaIEIE_606(  ); 
    Drawph_sigmaIEIE_607(  ); 
    Drawph_sigmaIEIE_608(  ); 
    Drawph_sigmaIEIE_609(  ); 
    Drawph_sigmaIEIE_610(  ); 
    Drawph_sigmaIEIE_611(  ); 
    Drawph_sigmaIEIE_612(  ); 
    Drawph_sigmaIEIE_613(  ); 
    Drawph_sigmaIEIE_614(  ); 
    Drawph_sigmaIEIE_615(  ); 
    Drawph_sigmaIEIE_616(  ); 
    Drawph_sigmaIEIE_617(  ); 
    Drawph_sigmaIEIE_618(  ); 
    Drawph_sigmaIEIE_619(  ); 
    Drawph_sigmaIEIE_620(  ); 
    Drawph_sigmaIEIE_621(  ); 
    Drawph_sigmaIEIE_622(  ); 
    Drawph_sigmaIEIE_623(  ); 
    Drawph_sigmaIEIE_624(  ); 
    Drawph_sigmaIEIE_625(  ); 
    Drawph_sigmaIEIE_626(  ); 
    Drawph_sigmaIEIE_627(  ); 
    Drawph_sigmaIEIE_628(  ); 
    Drawph_sigmaIEIE_629(  ); 
    Drawph_sigmaIEIE_630(  ); 
    Drawph_sigmaIEIE_631(  ); 
    Drawph_sigmaIEIE_632(  ); 
    Drawph_sigmaIEIE_633(  ); 
    Drawph_sigmaIEIE_634(  ); 
    Drawph_sigmaIEIE_635(  ); 
    Drawph_sigmaIEIE_636(  ); 
    Drawph_sigmaIEIE_637(  ); 
    Drawph_sigmaIEIE_638(  ); 
    Drawph_sigmaIEIE_639(  ); 
    Drawph_sigmaIEIE_640(  ); 
    Drawph_sigmaIEIE_641(  ); 
    Drawph_sigmaIEIE_642(  ); 
    Drawph_sigmaIEIE_643(  ); 
    Drawph_sigmaIEIE_644(  ); 
    Drawph_sigmaIEIE_645(  ); 
    Drawph_sigmaIEIE_646(  ); 
    Drawph_sigmaIEIE_647(  ); 
    Drawph_sigmaIEIE_648(  ); 
    Drawph_sigmaIEIE_649(  ); 
    Drawph_sigmaIEIE_650(  ); 
    Drawph_sigmaIEIE_651(  ); 
    Drawph_sigmaIEIE_652(  ); 
    Drawph_sigmaIEIE_653(  ); 
    Drawph_sigmaIEIE_654(  ); 
    Drawph_sigmaIEIE_655(  ); 
    Drawph_sigmaIEIE_656(  ); 
    Drawph_sigmaIEIE_657(  ); 
    Drawph_sigmaIEIE_658(  ); 
    Drawph_sigmaIEIE_659(  ); 
    Drawph_sigmaIEIE_660(  ); 
    Drawph_sigmaIEIE_661(  ); 
    Drawph_sigmaIEIE_662(  ); 
    Drawph_sigmaIEIE_663(  ); 
    Drawph_sigmaIEIE_664(  ); 
    Drawph_sigmaIEIE_665(  ); 
    Drawph_sigmaIEIE_666(  ); 
    Drawph_sigmaIEIE_667(  ); 
    Drawph_sigmaIEIE_668(  ); 
    Drawph_sigmaIEIE_669(  ); 
    Drawph_sigmaIEIE_670(  ); 
    Drawph_sigmaIEIE_671(  ); 
    Drawph_sigmaIEIE_672(  ); 
    Drawph_sigmaIEIE_673(  ); 
    Drawph_sigmaIEIE_674(  ); 
    Drawph_sigmaIEIE_675(  ); 
    Drawph_sigmaIEIE_676(  ); 
    Drawph_sigmaIEIE_677(  ); 
    Drawph_sigmaIEIE_678(  ); 
    Drawph_sigmaIEIE_679(  ); 
    Drawph_sigmaIEIE_680(  ); 
    Drawph_sigmaIEIE_681(  ); 
    Drawph_sigmaIEIE_682(  ); 
    Drawph_sigmaIEIE_683(  ); 
    Drawph_sigmaIEIE_684(  ); 
    Drawph_sigmaIEIE_685(  ); 
    Drawph_sigmaIEIE_686(  ); 
    Drawph_sigmaIEIE_687(  ); 
    Drawph_sigmaIEIE_688(  ); 
    Drawph_sigmaIEIE_689(  ); 
    Drawph_sigmaIEIE_690(  ); 
    Drawph_sigmaIEIE_691(  ); 
    Drawph_sigmaIEIE_692(  ); 
    Drawph_sigmaIEIE_693(  ); 
    Drawph_sigmaIEIE_694(  ); 
    Drawph_sigmaIEIE_695(  ); 
    Drawph_sigmaIEIE_696(  ); 
    Drawph_sigmaIEIE_697(  ); 
    Drawph_sigmaIEIE_698(  ); 
    Drawph_sigmaIEIE_699(  ); 
    Drawph_sigmaIEIE_700(  ); 
    Drawph_sigmaIEIE_701(  ); 
    Drawph_sigmaIEIE_702(  ); 
    Drawph_sigmaIEIE_703(  ); 
    Drawph_sigmaIEIE_704(  ); 
    Drawph_sigmaIEIE_705(  ); 
    Drawph_sigmaIEIE_706(  ); 
    Drawph_sigmaIEIE_707(  ); 
    Drawph_sigmaIEIE_708(  ); 
    Drawph_sigmaIEIE_709(  ); 
    Drawph_sigmaIEIE_710(  ); 
    Drawph_sigmaIEIE_711(  ); 
    Drawph_sigmaIEIE_712(  ); 
    Drawph_sigmaIEIE_713(  ); 
    Drawph_sigmaIEIE_714(  ); 
    Drawph_sigmaIEIE_715(  ); 
    Drawph_sigmaIEIE_716(  ); 
    Drawph_sigmaIEIE_717(  ); 
    Drawph_sigmaIEIE_718(  ); 
    Drawph_sigmaIEIE_719(  ); 
    Drawph_sigmaIEIE_720(  ); 
    Drawph_sigmaIEIE_721(  ); 
    Drawph_sigmaIEIE_722(  ); 
    Drawph_sigmaIEIE_723(  ); 
    Drawph_sigmaIEIE_724(  ); 
    Drawph_sigmaIEIE_725(  ); 
    Drawph_sigmaIEIE_726(  ); 
    Drawph_sigmaIEIE_727(  ); 
    Drawph_sigmaIEIE_728(  ); 
    Drawph_sigmaIEIE_729(  ); 
    Drawph_sigmaIEIE_730(  ); 
    Drawph_sigmaIEIE_731(  ); 
    Drawph_sigmaIEIE_732(  ); 
    Drawph_sigmaIEIE_733(  ); 
    Drawph_sigmaIEIE_734(  ); 
    Drawph_sigmaIEIE_735(  ); 
    Drawph_sigmaIEIE_736(  ); 
    Drawph_sigmaIEIE_737(  ); 
    Drawph_sigmaIEIE_738(  ); 
    Drawph_sigmaIEIE_739(  ); 
    Drawph_sigmaIEIE_740(  ); 
    Drawph_sigmaIEIE_741(  ); 
    Drawph_sigmaIEIE_742(  ); 
    Drawph_sigmaIEIE_743(  ); 
    Drawph_sigmaIEIE_744(  ); 
    Drawph_sigmaIEIE_745(  ); 
    Drawph_sigmaIEIE_746(  ); 
    Drawph_sigmaIEIE_747(  ); 
    Drawph_sigmaIEIE_748(  ); 
    Drawph_sigmaIEIE_749(  ); 
    Drawph_sigmaIEIE_750(  ); 
    Drawph_sigmaIEIE_751(  ); 
    Drawph_sigmaIEIE_752(  ); 
    Drawph_sigmaIEIE_753(  ); 
    Drawph_sigmaIEIE_754(  ); 
    Drawph_sigmaIEIE_755(  ); 
    Drawph_sigmaIEIE_756(  ); 
    Drawph_sigmaIEIE_757(  ); 
    Drawph_sigmaIEIE_758(  ); 
    Drawph_sigmaIEIE_759(  ); 
    Drawph_sigmaIEIE_760(  ); 
    Drawph_sigmaIEIE_761(  ); 
    Drawph_sigmaIEIE_762(  ); 
    Drawph_sigmaIEIE_763(  ); 
    Drawph_sigmaIEIE_764(  ); 
    Drawph_sigmaIEIE_765(  ); 
    Drawph_sigmaIEIE_766(  ); 
    Drawph_sigmaIEIE_767(  ); 
    Drawph_sigmaIEIE_768(  ); 
    Drawph_sigmaIEIE_769(  ); 
    Drawph_sigmaIEIE_770(  ); 
    Drawph_sigmaIEIE_771(  ); 
    Drawph_sigmaIEIE_772(  ); 
    Drawph_sigmaIEIE_773(  ); 
    Drawph_sigmaIEIE_774(  ); 
    Drawph_sigmaIEIE_775(  ); 
    Drawph_sigmaIEIE_776(  ); 
    Drawph_sigmaIEIE_777(  ); 
    Drawph_sigmaIEIE_778(  ); 
    Drawph_sigmaIEIE_779(  ); 
    Drawph_sigmaIEIE_780(  ); 
    Drawph_sigmaIEIE_781(  ); 
    Drawph_sigmaIEIE_782(  ); 
    Drawph_sigmaIEIE_783(  ); 
    Drawph_sigmaIEIE_784(  ); 
    Drawph_sigmaIEIE_785(  ); 
    Drawph_sigmaIEIE_786(  ); 
    Drawph_sigmaIEIE_787(  ); 
    Drawph_sigmaIEIE_788(  ); 
    Drawph_sigmaIEIE_789(  ); 
    Drawph_sigmaIEIE_790(  ); 
    Drawph_sigmaIEIE_791(  ); 
    Drawph_sigmaIEIE_792(  ); 
    Drawph_sigmaIEIE_793(  ); 
    Drawph_sigmaIEIE_794(  ); 
    Drawph_sigmaIEIE_795(  ); 
    Drawph_sigmaIEIE_796(  ); 
    Drawph_sigmaIEIE_797(  ); 
    Drawph_sigmaIEIE_798(  ); 
    Drawph_sigmaIEIE_799(  ); 
    Drawph_sigmaIEIE_800(  ); 
    Drawph_sigmaIEIE_801(  ); 
    Drawph_sigmaIEIE_802(  ); 
    Drawph_sigmaIEIE_803(  ); 
    Drawph_sigmaIEIE_804(  ); 
    Drawph_sigmaIEIE_805(  ); 
    Drawph_sigmaIEIE_806(  ); 
    Drawph_sigmaIEIE_807(  ); 
    Drawph_sigmaIEIE_808(  ); 
    Drawph_sigmaIEIE_809(  ); 
    Drawph_sigmaIEIE_810(  ); 
    Drawph_sigmaIEIE_811(  ); 
    Drawph_sigmaIEIE_812(  ); 
    Drawph_sigmaIEIE_813(  ); 
    Drawph_sigmaIEIE_814(  ); 
    Drawph_sigmaIEIE_815(  ); 
    Drawph_sigmaIEIE_816(  ); 
    Drawph_sigmaIEIE_817(  ); 
    Drawph_sigmaIEIE_818(  ); 
    Drawph_sigmaIEIE_819(  ); 
    Drawph_sigmaIEIE_820(  ); 
    Drawph_sigmaIEIE_821(  ); 
    Drawph_sigmaIEIE_822(  ); 
    Drawph_sigmaIEIE_823(  ); 
    Drawph_sigmaIEIE_824(  ); 
    Drawph_sigmaIEIE_825(  ); 
    Drawph_sigmaIEIE_826(  ); 
    Drawph_sigmaIEIE_827(  ); 
    Drawph_sigmaIEIE_828(  ); 
    Drawph_sigmaIEIE_829(  ); 
    Drawph_sigmaIEIE_830(  ); 
    Drawph_sigmaIEIE_831(  ); 
    Drawph_sigmaIEIE_832(  ); 
    Drawph_sigmaIEIE_833(  ); 
    Drawph_sigmaIEIE_834(  ); 
    Drawph_sigmaIEIE_835(  ); 
    Drawph_sigmaIEIE_836(  ); 
    Drawph_sigmaIEIE_837(  ); 
    Drawph_sigmaIEIE_838(  ); 
    Drawph_sigmaIEIE_839(  ); 
    Drawph_sigmaIEIE_840(  ); 
    Drawph_sigmaIEIE_841(  ); 
    Drawph_sigmaIEIE_842(  ); 
    Drawph_sigmaIEIE_843(  ); 
    Drawph_sigmaIEIE_844(  ); 
    Drawph_sigmaIEIE_845(  ); 
    Drawph_sigmaIEIE_846(  ); 
    Drawph_sigmaIEIE_847(  ); 
    Drawph_sigmaIEIE_848(  ); 
    Drawph_sigmaIEIE_849(  ); 
    Drawph_sigmaIEIE_850(  ); 
    Drawph_sigmaIEIE_851(  ); 
    Drawph_sigmaIEIE_852(  ); 
    Drawph_sigmaIEIE_853(  ); 
    Drawph_sigmaIEIE_854(  ); 
    Drawph_sigmaIEIE_855(  ); 
    Drawph_sigmaIEIE_856(  ); 
    Drawph_sigmaIEIE_857(  ); 
    Drawph_sigmaIEIE_858(  ); 
    Drawph_sigmaIEIE_859(  ); 
    Drawph_sigmaIEIE_860(  ); 
    Drawph_sigmaIEIE_861(  ); 
    Drawph_sigmaIEIE_862(  ); 
    Drawph_sigmaIEIE_863(  ); 
    Drawph_sigmaIEIE_864(  ); 
    Drawph_sigmaIEIE_865(  ); 
    Drawph_sigmaIEIE_866(  ); 
    Drawph_sigmaIEIE_867(  ); 
    Drawph_sigmaIEIE_868(  ); 
    Drawph_sigmaIEIE_869(  ); 
    Drawph_sigmaIEIE_870(  ); 
    Drawph_sigmaIEIE_871(  ); 
    Drawph_sigmaIEIE_872(  ); 
    Drawph_sigmaIEIE_873(  ); 
    Drawph_sigmaIEIE_874(  ); 
    Drawph_sigmaIEIE_875(  ); 
    Drawph_sigmaIEIE_876(  ); 
    Drawph_sigmaIEIE_877(  ); 
    Drawph_sigmaIEIE_878(  ); 
    Drawph_sigmaIEIE_879(  ); 
    Drawph_sigmaIEIE_880(  ); 
    Drawph_sigmaIEIE_881(  ); 
    Drawph_sigmaIEIE_882(  ); 
    Drawph_sigmaIEIE_883(  ); 
    Drawph_sigmaIEIE_884(  ); 
    Drawph_sigmaIEIE_885(  ); 
    Drawph_sigmaIEIE_886(  ); 
    Drawph_sigmaIEIE_887(  ); 
    Drawph_sigmaIEIE_888(  ); 
    Drawph_sigmaIEIE_889(  ); 
    Drawph_sigmaIEIE_890(  ); 
    Drawph_sigmaIEIE_891(  ); 
    Drawph_sigmaIEIE_892(  ); 
    Drawph_sigmaIEIE_893(  ); 
    Drawph_sigmaIEIE_894(  ); 
    Drawph_sigmaIEIE_895(  ); 
    Drawph_sigmaIEIE_896(  ); 
    Drawph_sigmaIEIE_897(  ); 
    Drawph_sigmaIEIE_898(  ); 
    Drawph_sigmaIEIE_899(  ); 
    Drawph_sigmaIEIE_900(  ); 
    Drawph_sigmaIEIE_901(  ); 
    Drawph_sigmaIEIE_902(  ); 
    Drawph_sigmaIEIE_903(  ); 
    Drawph_sigmaIEIE_904(  ); 
    Drawph_sigmaIEIE_905(  ); 
    Drawph_sigmaIEIE_906(  ); 
    Drawph_sigmaIEIE_907(  ); 
    Drawph_sigmaIEIE_908(  ); 
    Drawph_sigmaIEIE_909(  ); 
    Drawph_sigmaIEIE_910(  ); 
    Drawph_sigmaIEIE_911(  ); 
    Drawph_sigmaIEIE_912(  ); 
    Drawph_sigmaIEIE_913(  ); 
    Drawph_sigmaIEIE_914(  ); 
    Drawph_sigmaIEIE_915(  ); 
    Drawph_sigmaIEIE_916(  ); 
    Drawph_sigmaIEIE_917(  ); 
    Drawph_sigmaIEIE_918(  ); 
    Drawph_sigmaIEIE_919(  ); 
    Drawph_sigmaIEIE_920(  ); 
    Drawph_sigmaIEIE_921(  ); 
    Drawph_sigmaIEIE_922(  ); 
    Drawph_sigmaIEIE_923(  ); 
    Drawph_sigmaIEIE_924(  ); 
    Drawph_sigmaIEIE_925(  ); 
    Drawph_sigmaIEIE_926(  ); 
    Drawph_sigmaIEIE_927(  ); 
    Drawph_sigmaIEIE_928(  ); 
    Drawph_sigmaIEIE_929(  ); 
    Drawph_sigmaIEIE_930(  ); 
    Drawph_sigmaIEIE_931(  ); 
    Drawph_sigmaIEIE_932(  ); 
    Drawph_sigmaIEIE_933(  ); 
    Drawph_sigmaIEIE_934(  ); 
    Drawph_sigmaIEIE_935(  ); 
    Drawph_sigmaIEIE_936(  ); 
    Drawph_sigmaIEIE_937(  ); 
    Drawph_sigmaIEIE_938(  ); 
    Drawph_sigmaIEIE_939(  ); 
    Drawph_sigmaIEIE_940(  ); 
    Drawph_sigmaIEIE_941(  ); 
    Drawph_sigmaIEIE_942(  ); 
    Drawph_sigmaIEIE_943(  ); 
    Drawph_sigmaIEIE_944(  ); 
    Drawph_sigmaIEIE_945(  ); 
    Drawph_sigmaIEIE_946(  ); 
    Drawph_sigmaIEIE_947(  ); 
    Drawph_sigmaIEIE_948(  ); 
    Drawph_sigmaIEIE_949(  ); 
    Drawph_sigmaIEIE_950(  ); 
    Drawph_sigmaIEIE_951(  ); 
    Drawph_sigmaIEIE_952(  ); 
    Drawph_sigmaIEIE_953(  ); 
    Drawph_sigmaIEIE_954(  ); 
    Drawph_sigmaIEIE_955(  ); 
    Drawph_sigmaIEIE_956(  ); 
    Drawph_sigmaIEIE_957(  ); 
    Drawph_sigmaIEIE_958(  ); 
    Drawph_sigmaIEIE_959(  ); 
    Drawph_sigmaIEIE_960(  ); 
    Drawph_sigmaIEIE_961(  ); 
    Drawph_sigmaIEIE_962(  ); 
    Drawph_sigmaIEIE_963(  ); 
    Drawph_sigmaIEIE_964(  ); 
    Drawph_sigmaIEIE_965(  ); 
    Drawph_sigmaIEIE_966(  ); 
    Drawph_sigmaIEIE_967(  ); 
    Drawph_sigmaIEIE_968(  ); 
    Drawph_sigmaIEIE_969(  ); 
    Drawph_sigmaIEIE_970(  ); 
    Drawph_sigmaIEIE_971(  ); 
    Drawph_sigmaIEIE_972(  ); 
    Drawph_sigmaIEIE_973(  ); 
    Drawph_sigmaIEIE_974(  ); 
    Drawph_sigmaIEIE_975(  ); 
    Drawph_sigmaIEIE_976(  ); 
    Drawph_sigmaIEIE_977(  ); 
    Drawph_sigmaIEIE_978(  ); 
    Drawph_sigmaIEIE_979(  ); 
    Drawph_sigmaIEIE_980(  ); 
    Drawph_sigmaIEIE_981(  ); 
    Drawph_sigmaIEIE_982(  ); 
    Drawph_sigmaIEIE_983(  ); 
    Drawph_sigmaIEIE_984(  ); 
    Drawph_sigmaIEIE_985(  ); 
    Drawph_sigmaIEIE_986(  ); 
    Drawph_sigmaIEIE_987(  ); 
    Drawph_sigmaIEIE_988(  ); 
    Drawph_sigmaIEIE_989(  ); 
    Drawph_sigmaIEIE_990(  ); 
    Drawph_sigmaIEIE_991(  ); 
    Drawph_sigmaIEIE_992(  ); 
    Drawph_sigmaIEIE_993(  ); 
    Drawph_sigmaIEIE_994(  ); 
    Drawph_sigmaIEIE_995(  ); 
    Drawph_sigmaIEIE_996(  ); 
    Drawph_sigmaIEIE_997(  ); 
    Drawph_sigmaIEIE_998(  ); 
    Drawph_sigmaIEIE_999(  ); 
    Drawph_sigmaIEIE_1000(  ); 
    Drawph_sigmaIEIE_1001(  ); 
    Drawph_sigmaIEIE_1002(  ); 
    Drawph_sigmaIEIE_1003(  ); 
    Drawph_sigmaIEIE_1004(  ); 
    Drawph_sigmaIEIE_1005(  ); 
    Drawph_sigmaIEIE_1006(  ); 
    Drawph_sigmaIEIE_1007(  ); 
    Drawph_sigmaIEIE_1008(  ); 
    Drawph_sigmaIEIE_1009(  ); 
    Drawph_sigmaIEIE_1010(  ); 
    Drawph_sigmaIEIE_1011(  ); 
    Drawph_sigmaIEIE_1012(  ); 
    Drawph_sigmaIEIE_1013(  ); 
    Drawph_sigmaIEIE_1014(  ); 
    Drawph_sigmaIEIE_1015(  ); 
    Drawph_sigmaIEIE_1016(  ); 
    Drawph_sigmaIEIE_1017(  ); 
    Drawph_sigmaIEIE_1018(  ); 
    Drawph_sigmaIEIE_1019(  ); 
    Drawph_sigmaIEIE_1020(  ); 
    Drawph_sigmaIEIE_1021(  ); 
    Drawph_sigmaIEIE_1022(  ); 
    Drawph_sigmaIEIE_1023(  ); 
    Drawph_sigmaIEIE_1024(  ); 
    Drawph_sigmaIEIE_1025(  ); 
    Drawph_sigmaIEIE_1026(  ); 
    Drawph_sigmaIEIE_1027(  ); 
    Drawph_sigmaIEIE_1028(  ); 
    Drawph_sigmaIEIE_1029(  ); 
    Drawph_sigmaIEIE_1030(  ); 
    Drawph_sigmaIEIE_1031(  ); 
    Drawph_sigmaIEIE_1032(  ); 
    Drawph_sigmaIEIE_1033(  ); 
    Drawph_sigmaIEIE_1034(  ); 
    Drawph_sigmaIEIE_1035(  ); 
    Drawph_sigmaIEIE_1036(  ); 
    Drawph_sigmaIEIE_1037(  ); 
    Drawph_sigmaIEIE_1038(  ); 
    Drawph_sigmaIEIE_1039(  ); 
    Drawph_sigmaIEIE_1040(  ); 
    return false;
}

void RunModule::finalize(  ) {
    hist_ph_pt_26->Write(); 
    hist_ph_pt_27->Write(); 
    hist_ph_pt_28->Write(); 
    hist_ph_pt_29->Write(); 
    hist_ph_pt_30->Write(); 
    hist_ph_pt_31->Write(); 
    hist_ph_pt_32->Write(); 
    hist_ph_pt_33->Write(); 
    hist_ph_pt_34->Write(); 
    hist_ph_pt_35->Write(); 
    hist_ph_pt_36->Write(); 
    hist_ph_pt_37->Write(); 
    hist_ph_pt_38->Write(); 
    hist_ph_pt_39->Write(); 
    hist_ph_pt_40->Write(); 
    hist_ph_pt_41->Write(); 
    hist_leadPhot_sublLepDR->Write(); 
    hist_leadPhot_leadLepDR->Write(); 
    hist_m_leplepph->Write(); 
    hist_m_leplepph_m_leplep->Write(); 
    hist_leadPhot_leadLepDR_0->Write(); 
    hist_leadPhot_leadLepDR_1->Write(); 
    hist_ph_sigmaIEIE_59->Write(); 
    hist_ph_sigmaIEIE_60->Write(); 
    hist_ph_sigmaIEIE_61->Write(); 
    hist_ph_sigmaIEIE_62->Write(); 
    hist_ph_sigmaIEIE_63->Write(); 
    hist_ph_sigmaIEIE_64->Write(); 
    hist_ph_sigmaIEIE_65->Write(); 
    hist_ph_sigmaIEIE_66->Write(); 
    hist_leadPhot_sublLepDR_0->Write(); 
    hist_leadPhot_leadLepDR_2->Write(); 
    hist_ph_sigmaIEIE_67->Write(); 
    hist_ph_sigmaIEIE_68->Write(); 
    hist_ph_sigmaIEIE_69->Write(); 
    hist_ph_sigmaIEIE_70->Write(); 
    hist_ph_sigmaIEIE_71->Write(); 
    hist_ph_sigmaIEIE_72->Write(); 
    hist_ph_sigmaIEIE_73->Write(); 
    hist_ph_sigmaIEIE_74->Write(); 
    hist_ph_sigmaIEIE_75->Write(); 
    hist_ph_sigmaIEIE_76->Write(); 
    hist_ph_sigmaIEIE_77->Write(); 
    hist_ph_sigmaIEIE_78->Write(); 
    hist_ph_sigmaIEIE_79->Write(); 
    hist_ph_sigmaIEIE_80->Write(); 
    hist_ph_sigmaIEIE_81->Write(); 
    hist_ph_sigmaIEIE_82->Write(); 
    hist_ph_sigmaIEIE_83->Write(); 
    hist_ph_sigmaIEIE_84->Write(); 
    hist_ph_sigmaIEIE_85->Write(); 
    hist_ph_sigmaIEIE_86->Write(); 
    hist_ph_sigmaIEIE_87->Write(); 
    hist_ph_sigmaIEIE_88->Write(); 
    hist_ph_sigmaIEIE_89->Write(); 
    hist_ph_sigmaIEIE_90->Write(); 
    hist_ph_sigmaIEIE_91->Write(); 
    hist_ph_sigmaIEIE_92->Write(); 
    hist_ph_sigmaIEIE_93->Write(); 
    hist_ph_sigmaIEIE_94->Write(); 
    hist_ph_sigmaIEIE_95->Write(); 
    hist_ph_sigmaIEIE_96->Write(); 
    hist_ph_sigmaIEIE_97->Write(); 
    hist_ph_sigmaIEIE_98->Write(); 
    hist_ph_sigmaIEIE_99->Write(); 
    hist_ph_sigmaIEIE_100->Write(); 
    hist_ph_sigmaIEIE_101->Write(); 
    hist_ph_sigmaIEIE_102->Write(); 
    hist_ph_sigmaIEIE_103->Write(); 
    hist_ph_sigmaIEIE_104->Write(); 
    hist_ph_sigmaIEIE_105->Write(); 
    hist_ph_sigmaIEIE_106->Write(); 
    hist_ph_sigmaIEIE_107->Write(); 
    hist_ph_sigmaIEIE_108->Write(); 
    hist_ph_sigmaIEIE_109->Write(); 
    hist_ph_sigmaIEIE_110->Write(); 
    hist_ph_sigmaIEIE_111->Write(); 
    hist_ph_sigmaIEIE_112->Write(); 
    hist_ph_sigmaIEIE_113->Write(); 
    hist_ph_sigmaIEIE_114->Write(); 
    hist_ph_sigmaIEIE_115->Write(); 
    hist_ph_sigmaIEIE_116->Write(); 
    hist_ph_sigmaIEIE_117->Write(); 
    hist_ph_sigmaIEIE_118->Write(); 
    hist_ph_sigmaIEIE_119->Write(); 
    hist_ph_sigmaIEIE_120->Write(); 
    hist_ph_sigmaIEIE_121->Write(); 
    hist_ph_sigmaIEIE_122->Write(); 
    hist_ph_sigmaIEIE_123->Write(); 
    hist_ph_sigmaIEIE_124->Write(); 
    hist_ph_sigmaIEIE_125->Write(); 
    hist_ph_sigmaIEIE_126->Write(); 
    hist_ph_sigmaIEIE_127->Write(); 
    hist_ph_sigmaIEIE_128->Write(); 
    hist_ph_sigmaIEIE_129->Write(); 
    hist_ph_sigmaIEIE_130->Write(); 
    hist_ph_sigmaIEIE_131->Write(); 
    hist_ph_sigmaIEIE_132->Write(); 
    hist_ph_sigmaIEIE_133->Write(); 
    hist_ph_sigmaIEIE_134->Write(); 
    hist_ph_sigmaIEIE_135->Write(); 
    hist_ph_sigmaIEIE_136->Write(); 
    hist_ph_sigmaIEIE_137->Write(); 
    hist_ph_sigmaIEIE_138->Write(); 
    hist_ph_sigmaIEIE_139->Write(); 
    hist_ph_sigmaIEIE_140->Write(); 
    hist_ph_sigmaIEIE_141->Write(); 
    hist_ph_sigmaIEIE_142->Write(); 
    hist_ph_sigmaIEIE_143->Write(); 
    hist_ph_sigmaIEIE_144->Write(); 
    hist_ph_pt_42->Write(); 
    hist_ph_pt_43->Write(); 
    hist_ph_pt_44->Write(); 
    hist_ph_pt_45->Write(); 
    hist_ph_pt_46->Write(); 
    hist_ph_pt_47->Write(); 
    hist_ph_pt_48->Write(); 
    hist_ph_pt_49->Write(); 
    hist_ph_pt_50->Write(); 
    hist_ph_pt_51->Write(); 
    hist_ph_pt_52->Write(); 
    hist_ph_pt_53->Write(); 
    hist_ph_pt_54->Write(); 
    hist_ph_pt_55->Write(); 
    hist_ph_pt_56->Write(); 
    hist_ph_pt_57->Write(); 
    hist_ph_pt_58->Write(); 
    hist_ph_pt_59->Write(); 
    hist_ph_pt_60->Write(); 
    hist_ph_pt_61->Write(); 
    hist_ph_pt_62->Write(); 
    hist_ph_pt_63->Write(); 
    hist_ph_pt_64->Write(); 
    hist_ph_pt_65->Write(); 
    hist_ph_sigmaIEIE_145->Write(); 
    hist_ph_sigmaIEIE_146->Write(); 
    hist_ph_sigmaIEIE_147->Write(); 
    hist_ph_sigmaIEIE_148->Write(); 
    hist_ph_sigmaIEIE_149->Write(); 
    hist_ph_sigmaIEIE_150->Write(); 
    hist_ph_sigmaIEIE_151->Write(); 
    hist_ph_sigmaIEIE_152->Write(); 
    hist_ph_sigmaIEIE_153->Write(); 
    hist_ph_sigmaIEIE_154->Write(); 
    hist_ph_sigmaIEIE_155->Write(); 
    hist_ph_sigmaIEIE_156->Write(); 
    hist_ph_sigmaIEIE_157->Write(); 
    hist_ph_sigmaIEIE_158->Write(); 
    hist_ph_sigmaIEIE_159->Write(); 
    hist_ph_sigmaIEIE_160->Write(); 
    hist_ph_sigmaIEIE_161->Write(); 
    hist_ph_sigmaIEIE_162->Write(); 
    hist_ph_sigmaIEIE_163->Write(); 
    hist_ph_sigmaIEIE_164->Write(); 
    hist_ph_sigmaIEIE_165->Write(); 
    hist_ph_sigmaIEIE_166->Write(); 
    hist_ph_sigmaIEIE_167->Write(); 
    hist_ph_sigmaIEIE_168->Write(); 
    hist_ph_sigmaIEIE_169->Write(); 
    hist_ph_sigmaIEIE_170->Write(); 
    hist_ph_sigmaIEIE_171->Write(); 
    hist_ph_sigmaIEIE_172->Write(); 
    hist_ph_sigmaIEIE_173->Write(); 
    hist_ph_sigmaIEIE_174->Write(); 
    hist_ph_sigmaIEIE_175->Write(); 
    hist_ph_sigmaIEIE_176->Write(); 
    hist_ph_sigmaIEIE_177->Write(); 
    hist_ph_sigmaIEIE_178->Write(); 
    hist_ph_sigmaIEIE_179->Write(); 
    hist_ph_sigmaIEIE_180->Write(); 
    hist_ph_sigmaIEIE_181->Write(); 
    hist_ph_sigmaIEIE_182->Write(); 
    hist_ph_sigmaIEIE_183->Write(); 
    hist_ph_sigmaIEIE_184->Write(); 
    hist_ph_sigmaIEIE_185->Write(); 
    hist_ph_sigmaIEIE_186->Write(); 
    hist_ph_sigmaIEIE_187->Write(); 
    hist_ph_sigmaIEIE_188->Write(); 
    hist_ph_sigmaIEIE_189->Write(); 
    hist_ph_sigmaIEIE_190->Write(); 
    hist_ph_sigmaIEIE_191->Write(); 
    hist_ph_sigmaIEIE_192->Write(); 
    hist_ph_sigmaIEIE_193->Write(); 
    hist_ph_sigmaIEIE_194->Write(); 
    hist_ph_sigmaIEIE_195->Write(); 
    hist_ph_sigmaIEIE_196->Write(); 
    hist_ph_sigmaIEIE_197->Write(); 
    hist_ph_sigmaIEIE_198->Write(); 
    hist_ph_sigmaIEIE_199->Write(); 
    hist_ph_sigmaIEIE_200->Write(); 
    hist_ph_sigmaIEIE_201->Write(); 
    hist_ph_sigmaIEIE_202->Write(); 
    hist_ph_sigmaIEIE_203->Write(); 
    hist_ph_sigmaIEIE_204->Write(); 
    hist_ph_sigmaIEIE_205->Write(); 
    hist_ph_sigmaIEIE_206->Write(); 
    hist_ph_sigmaIEIE_207->Write(); 
    hist_ph_sigmaIEIE_208->Write(); 
    hist_ph_sigmaIEIE_209->Write(); 
    hist_ph_sigmaIEIE_210->Write(); 
    hist_ph_sigmaIEIE_211->Write(); 
    hist_ph_sigmaIEIE_212->Write(); 
    hist_ph_sigmaIEIE_213->Write(); 
    hist_ph_sigmaIEIE_214->Write(); 
    hist_ph_sigmaIEIE_215->Write(); 
    hist_ph_sigmaIEIE_216->Write(); 
    hist_ph_sigmaIEIE_217->Write(); 
    hist_ph_sigmaIEIE_218->Write(); 
    hist_ph_sigmaIEIE_219->Write(); 
    hist_ph_sigmaIEIE_220->Write(); 
    hist_ph_sigmaIEIE_221->Write(); 
    hist_ph_sigmaIEIE_222->Write(); 
    hist_ph_sigmaIEIE_223->Write(); 
    hist_ph_sigmaIEIE_224->Write(); 
    hist_ph_sigmaIEIE_225->Write(); 
    hist_ph_sigmaIEIE_226->Write(); 
    hist_ph_sigmaIEIE_227->Write(); 
    hist_ph_sigmaIEIE_228->Write(); 
    hist_ph_sigmaIEIE_229->Write(); 
    hist_ph_sigmaIEIE_230->Write(); 
    hist_ph_sigmaIEIE_231->Write(); 
    hist_ph_sigmaIEIE_232->Write(); 
    hist_ph_sigmaIEIE_233->Write(); 
    hist_ph_sigmaIEIE_234->Write(); 
    hist_ph_sigmaIEIE_235->Write(); 
    hist_ph_sigmaIEIE_236->Write(); 
    hist_ph_sigmaIEIE_237->Write(); 
    hist_ph_sigmaIEIE_238->Write(); 
    hist_ph_sigmaIEIE_239->Write(); 
    hist_ph_sigmaIEIE_240->Write(); 
    hist_ph_sigmaIEIE_241->Write(); 
    hist_ph_sigmaIEIE_242->Write(); 
    hist_ph_sigmaIEIE_243->Write(); 
    hist_ph_sigmaIEIE_244->Write(); 
    hist_ph_sigmaIEIE_245->Write(); 
    hist_ph_sigmaIEIE_246->Write(); 
    hist_ph_sigmaIEIE_247->Write(); 
    hist_ph_sigmaIEIE_248->Write(); 
    hist_ph_sigmaIEIE_249->Write(); 
    hist_ph_sigmaIEIE_250->Write(); 
    hist_ph_sigmaIEIE_251->Write(); 
    hist_ph_sigmaIEIE_252->Write(); 
    hist_ph_sigmaIEIE_253->Write(); 
    hist_ph_sigmaIEIE_254->Write(); 
    hist_ph_sigmaIEIE_255->Write(); 
    hist_ph_sigmaIEIE_256->Write(); 
    hist_ph_sigmaIEIE_257->Write(); 
    hist_ph_sigmaIEIE_258->Write(); 
    hist_ph_sigmaIEIE_259->Write(); 
    hist_ph_sigmaIEIE_260->Write(); 
    hist_ph_sigmaIEIE_261->Write(); 
    hist_ph_sigmaIEIE_262->Write(); 
    hist_ph_sigmaIEIE_263->Write(); 
    hist_ph_sigmaIEIE_264->Write(); 
    hist_ph_sigmaIEIE_265->Write(); 
    hist_ph_sigmaIEIE_266->Write(); 
    hist_ph_sigmaIEIE_267->Write(); 
    hist_ph_sigmaIEIE_268->Write(); 
    hist_ph_sigmaIEIE_269->Write(); 
    hist_ph_sigmaIEIE_270->Write(); 
    hist_ph_sigmaIEIE_271->Write(); 
    hist_ph_sigmaIEIE_272->Write(); 
    hist_ph_sigmaIEIE_273->Write(); 
    hist_ph_sigmaIEIE_274->Write(); 
    hist_ph_sigmaIEIE_275->Write(); 
    hist_ph_sigmaIEIE_276->Write(); 
    hist_ph_sigmaIEIE_277->Write(); 
    hist_ph_sigmaIEIE_278->Write(); 
    hist_ph_sigmaIEIE_279->Write(); 
    hist_ph_sigmaIEIE_280->Write(); 
    hist_ph_sigmaIEIE_281->Write(); 
    hist_ph_sigmaIEIE_282->Write(); 
    hist_ph_sigmaIEIE_283->Write(); 
    hist_ph_sigmaIEIE_284->Write(); 
    hist_ph_sigmaIEIE_285->Write(); 
    hist_ph_sigmaIEIE_286->Write(); 
    hist_ph_sigmaIEIE_287->Write(); 
    hist_ph_sigmaIEIE_288->Write(); 
    hist_ph_sigmaIEIE_289->Write(); 
    hist_ph_sigmaIEIE_290->Write(); 
    hist_ph_sigmaIEIE_291->Write(); 
    hist_ph_sigmaIEIE_292->Write(); 
    hist_ph_sigmaIEIE_293->Write(); 
    hist_ph_sigmaIEIE_294->Write(); 
    hist_ph_sigmaIEIE_295->Write(); 
    hist_ph_sigmaIEIE_296->Write(); 
    hist_ph_sigmaIEIE_297->Write(); 
    hist_ph_sigmaIEIE_298->Write(); 
    hist_ph_sigmaIEIE_299->Write(); 
    hist_ph_sigmaIEIE_300->Write(); 
    hist_ph_sigmaIEIE_301->Write(); 
    hist_ph_sigmaIEIE_302->Write(); 
    hist_ph_sigmaIEIE_303->Write(); 
    hist_ph_sigmaIEIE_304->Write(); 
    hist_ph_sigmaIEIE_305->Write(); 
    hist_ph_sigmaIEIE_306->Write(); 
    hist_ph_sigmaIEIE_307->Write(); 
    hist_ph_sigmaIEIE_308->Write(); 
    hist_ph_sigmaIEIE_309->Write(); 
    hist_ph_sigmaIEIE_310->Write(); 
    hist_ph_sigmaIEIE_311->Write(); 
    hist_ph_sigmaIEIE_312->Write(); 
    hist_ph_sigmaIEIE_313->Write(); 
    hist_ph_sigmaIEIE_314->Write(); 
    hist_ph_sigmaIEIE_315->Write(); 
    hist_ph_sigmaIEIE_316->Write(); 
    hist_ph_sigmaIEIE_317->Write(); 
    hist_ph_sigmaIEIE_318->Write(); 
    hist_ph_sigmaIEIE_319->Write(); 
    hist_ph_sigmaIEIE_320->Write(); 
    hist_ph_sigmaIEIE_321->Write(); 
    hist_ph_sigmaIEIE_322->Write(); 
    hist_ph_sigmaIEIE_323->Write(); 
    hist_ph_sigmaIEIE_324->Write(); 
    hist_ph_sigmaIEIE_325->Write(); 
    hist_ph_sigmaIEIE_326->Write(); 
    hist_ph_sigmaIEIE_327->Write(); 
    hist_ph_sigmaIEIE_328->Write(); 
    hist_ph_sigmaIEIE_329->Write(); 
    hist_ph_sigmaIEIE_330->Write(); 
    hist_ph_sigmaIEIE_331->Write(); 
    hist_ph_sigmaIEIE_332->Write(); 
    hist_ph_sigmaIEIE_333->Write(); 
    hist_ph_sigmaIEIE_334->Write(); 
    hist_ph_sigmaIEIE_335->Write(); 
    hist_ph_sigmaIEIE_336->Write(); 
    hist_ph_sigmaIEIE_337->Write(); 
    hist_ph_sigmaIEIE_338->Write(); 
    hist_ph_sigmaIEIE_339->Write(); 
    hist_ph_sigmaIEIE_340->Write(); 
    hist_ph_sigmaIEIE_341->Write(); 
    hist_ph_sigmaIEIE_342->Write(); 
    hist_ph_sigmaIEIE_343->Write(); 
    hist_ph_sigmaIEIE_344->Write(); 
    hist_ph_sigmaIEIE_345->Write(); 
    hist_ph_sigmaIEIE_346->Write(); 
    hist_ph_sigmaIEIE_347->Write(); 
    hist_ph_sigmaIEIE_348->Write(); 
    hist_ph_sigmaIEIE_349->Write(); 
    hist_ph_sigmaIEIE_350->Write(); 
    hist_ph_sigmaIEIE_351->Write(); 
    hist_ph_sigmaIEIE_352->Write(); 
    hist_ph_sigmaIEIE_353->Write(); 
    hist_ph_sigmaIEIE_354->Write(); 
    hist_ph_sigmaIEIE_355->Write(); 
    hist_ph_sigmaIEIE_356->Write(); 
    hist_ph_sigmaIEIE_357->Write(); 
    hist_ph_sigmaIEIE_358->Write(); 
    hist_ph_sigmaIEIE_359->Write(); 
    hist_ph_sigmaIEIE_360->Write(); 
    hist_ph_sigmaIEIE_361->Write(); 
    hist_ph_sigmaIEIE_362->Write(); 
    hist_ph_sigmaIEIE_363->Write(); 
    hist_ph_sigmaIEIE_364->Write(); 
    hist_ph_sigmaIEIE_365->Write(); 
    hist_ph_sigmaIEIE_366->Write(); 
    hist_ph_sigmaIEIE_367->Write(); 
    hist_ph_sigmaIEIE_368->Write(); 
    hist_ph_sigmaIEIE_369->Write(); 
    hist_ph_sigmaIEIE_370->Write(); 
    hist_ph_sigmaIEIE_371->Write(); 
    hist_ph_sigmaIEIE_372->Write(); 
    hist_ph_sigmaIEIE_373->Write(); 
    hist_ph_sigmaIEIE_374->Write(); 
    hist_ph_sigmaIEIE_375->Write(); 
    hist_ph_sigmaIEIE_376->Write(); 
    hist_ph_sigmaIEIE_377->Write(); 
    hist_ph_sigmaIEIE_378->Write(); 
    hist_ph_sigmaIEIE_379->Write(); 
    hist_ph_sigmaIEIE_380->Write(); 
    hist_ph_sigmaIEIE_381->Write(); 
    hist_ph_sigmaIEIE_382->Write(); 
    hist_ph_sigmaIEIE_383->Write(); 
    hist_ph_sigmaIEIE_384->Write(); 
    hist_ph_sigmaIEIE_385->Write(); 
    hist_ph_sigmaIEIE_386->Write(); 
    hist_ph_sigmaIEIE_387->Write(); 
    hist_ph_sigmaIEIE_388->Write(); 
    hist_ph_sigmaIEIE_389->Write(); 
    hist_ph_sigmaIEIE_390->Write(); 
    hist_ph_sigmaIEIE_391->Write(); 
    hist_ph_sigmaIEIE_392->Write(); 
    hist_ph_sigmaIEIE_393->Write(); 
    hist_ph_sigmaIEIE_394->Write(); 
    hist_ph_sigmaIEIE_395->Write(); 
    hist_ph_sigmaIEIE_396->Write(); 
    hist_ph_sigmaIEIE_397->Write(); 
    hist_ph_sigmaIEIE_398->Write(); 
    hist_ph_sigmaIEIE_399->Write(); 
    hist_ph_sigmaIEIE_400->Write(); 
    hist_ph_sigmaIEIE_401->Write(); 
    hist_ph_sigmaIEIE_402->Write(); 
    hist_ph_sigmaIEIE_403->Write(); 
    hist_ph_sigmaIEIE_404->Write(); 
    hist_ph_sigmaIEIE_405->Write(); 
    hist_ph_sigmaIEIE_406->Write(); 
    hist_ph_sigmaIEIE_407->Write(); 
    hist_ph_sigmaIEIE_408->Write(); 
    hist_ph_sigmaIEIE_409->Write(); 
    hist_ph_sigmaIEIE_410->Write(); 
    hist_ph_sigmaIEIE_411->Write(); 
    hist_ph_sigmaIEIE_412->Write(); 
    hist_ph_sigmaIEIE_413->Write(); 
    hist_ph_sigmaIEIE_414->Write(); 
    hist_ph_sigmaIEIE_415->Write(); 
    hist_ph_sigmaIEIE_416->Write(); 
    hist_ph_sigmaIEIE_417->Write(); 
    hist_ph_sigmaIEIE_418->Write(); 
    hist_ph_sigmaIEIE_419->Write(); 
    hist_ph_sigmaIEIE_420->Write(); 
    hist_ph_sigmaIEIE_421->Write(); 
    hist_ph_sigmaIEIE_422->Write(); 
    hist_ph_sigmaIEIE_423->Write(); 
    hist_ph_sigmaIEIE_424->Write(); 
    hist_ph_sigmaIEIE_425->Write(); 
    hist_ph_sigmaIEIE_426->Write(); 
    hist_ph_sigmaIEIE_427->Write(); 
    hist_ph_sigmaIEIE_428->Write(); 
    hist_ph_sigmaIEIE_429->Write(); 
    hist_ph_sigmaIEIE_430->Write(); 
    hist_ph_sigmaIEIE_431->Write(); 
    hist_ph_sigmaIEIE_432->Write(); 
    hist_ph_sigmaIEIE_433->Write(); 
    hist_ph_sigmaIEIE_434->Write(); 
    hist_ph_sigmaIEIE_435->Write(); 
    hist_ph_sigmaIEIE_436->Write(); 
    hist_ph_sigmaIEIE_437->Write(); 
    hist_ph_sigmaIEIE_438->Write(); 
    hist_ph_sigmaIEIE_439->Write(); 
    hist_ph_sigmaIEIE_440->Write(); 
    hist_ph_sigmaIEIE_441->Write(); 
    hist_ph_sigmaIEIE_442->Write(); 
    hist_ph_sigmaIEIE_443->Write(); 
    hist_ph_sigmaIEIE_444->Write(); 
    hist_ph_sigmaIEIE_445->Write(); 
    hist_ph_sigmaIEIE_446->Write(); 
    hist_ph_sigmaIEIE_447->Write(); 
    hist_ph_sigmaIEIE_448->Write(); 
    hist_ph_sigmaIEIE_449->Write(); 
    hist_ph_sigmaIEIE_450->Write(); 
    hist_ph_sigmaIEIE_451->Write(); 
    hist_ph_sigmaIEIE_452->Write(); 
    hist_ph_sigmaIEIE_453->Write(); 
    hist_ph_sigmaIEIE_454->Write(); 
    hist_ph_sigmaIEIE_455->Write(); 
    hist_ph_sigmaIEIE_456->Write(); 
    hist_ph_sigmaIEIE_457->Write(); 
    hist_ph_sigmaIEIE_458->Write(); 
    hist_ph_sigmaIEIE_459->Write(); 
    hist_ph_sigmaIEIE_460->Write(); 
    hist_ph_sigmaIEIE_461->Write(); 
    hist_ph_sigmaIEIE_462->Write(); 
    hist_ph_sigmaIEIE_463->Write(); 
    hist_ph_sigmaIEIE_464->Write(); 
    hist_ph_sigmaIEIE_465->Write(); 
    hist_ph_sigmaIEIE_466->Write(); 
    hist_ph_sigmaIEIE_467->Write(); 
    hist_ph_sigmaIEIE_468->Write(); 
    hist_ph_sigmaIEIE_469->Write(); 
    hist_ph_sigmaIEIE_470->Write(); 
    hist_ph_sigmaIEIE_471->Write(); 
    hist_ph_sigmaIEIE_472->Write(); 
    hist_ph_sigmaIEIE_473->Write(); 
    hist_ph_sigmaIEIE_474->Write(); 
    hist_ph_sigmaIEIE_475->Write(); 
    hist_ph_sigmaIEIE_476->Write(); 
    hist_ph_sigmaIEIE_477->Write(); 
    hist_ph_sigmaIEIE_478->Write(); 
    hist_ph_sigmaIEIE_479->Write(); 
    hist_ph_sigmaIEIE_480->Write(); 
    hist_ph_sigmaIEIE_481->Write(); 
    hist_ph_sigmaIEIE_482->Write(); 
    hist_ph_sigmaIEIE_483->Write(); 
    hist_ph_sigmaIEIE_484->Write(); 
    hist_ph_sigmaIEIE_485->Write(); 
    hist_ph_sigmaIEIE_486->Write(); 
    hist_ph_sigmaIEIE_487->Write(); 
    hist_ph_sigmaIEIE_488->Write(); 
    hist_ph_sigmaIEIE_489->Write(); 
    hist_ph_sigmaIEIE_490->Write(); 
    hist_ph_sigmaIEIE_491->Write(); 
    hist_ph_sigmaIEIE_492->Write(); 
    hist_ph_sigmaIEIE_493->Write(); 
    hist_ph_sigmaIEIE_494->Write(); 
    hist_ph_sigmaIEIE_495->Write(); 
    hist_ph_sigmaIEIE_496->Write(); 
    hist_ph_sigmaIEIE_497->Write(); 
    hist_ph_sigmaIEIE_498->Write(); 
    hist_ph_sigmaIEIE_499->Write(); 
    hist_ph_sigmaIEIE_500->Write(); 
    hist_ph_sigmaIEIE_501->Write(); 
    hist_ph_sigmaIEIE_502->Write(); 
    hist_ph_sigmaIEIE_503->Write(); 
    hist_ph_sigmaIEIE_504->Write(); 
    hist_ph_sigmaIEIE_505->Write(); 
    hist_ph_sigmaIEIE_506->Write(); 
    hist_ph_sigmaIEIE_507->Write(); 
    hist_ph_sigmaIEIE_508->Write(); 
    hist_ph_sigmaIEIE_509->Write(); 
    hist_ph_sigmaIEIE_510->Write(); 
    hist_ph_sigmaIEIE_511->Write(); 
    hist_ph_sigmaIEIE_512->Write(); 
    hist_ph_sigmaIEIE_513->Write(); 
    hist_ph_sigmaIEIE_514->Write(); 
    hist_ph_sigmaIEIE_515->Write(); 
    hist_ph_sigmaIEIE_516->Write(); 
    hist_ph_sigmaIEIE_517->Write(); 
    hist_ph_sigmaIEIE_518->Write(); 
    hist_ph_sigmaIEIE_519->Write(); 
    hist_ph_sigmaIEIE_520->Write(); 
    hist_ph_sigmaIEIE_521->Write(); 
    hist_ph_sigmaIEIE_522->Write(); 
    hist_ph_sigmaIEIE_523->Write(); 
    hist_ph_sigmaIEIE_524->Write(); 
    hist_ph_sigmaIEIE_525->Write(); 
    hist_ph_sigmaIEIE_526->Write(); 
    hist_ph_sigmaIEIE_527->Write(); 
    hist_ph_sigmaIEIE_528->Write(); 
    hist_ph_sigmaIEIE_529->Write(); 
    hist_ph_sigmaIEIE_530->Write(); 
    hist_ph_sigmaIEIE_531->Write(); 
    hist_ph_sigmaIEIE_532->Write(); 
    hist_ph_sigmaIEIE_533->Write(); 
    hist_ph_sigmaIEIE_534->Write(); 
    hist_ph_sigmaIEIE_535->Write(); 
    hist_ph_sigmaIEIE_536->Write(); 
    hist_ph_sigmaIEIE_537->Write(); 
    hist_ph_sigmaIEIE_538->Write(); 
    hist_ph_sigmaIEIE_539->Write(); 
    hist_ph_sigmaIEIE_540->Write(); 
    hist_ph_sigmaIEIE_541->Write(); 
    hist_ph_sigmaIEIE_542->Write(); 
    hist_ph_sigmaIEIE_543->Write(); 
    hist_ph_sigmaIEIE_544->Write(); 
    hist_ph_sigmaIEIE_545->Write(); 
    hist_ph_sigmaIEIE_546->Write(); 
    hist_ph_sigmaIEIE_547->Write(); 
    hist_ph_sigmaIEIE_548->Write(); 
    hist_ph_sigmaIEIE_549->Write(); 
    hist_ph_sigmaIEIE_550->Write(); 
    hist_ph_sigmaIEIE_551->Write(); 
    hist_ph_sigmaIEIE_552->Write(); 
    hist_ph_sigmaIEIE_553->Write(); 
    hist_ph_sigmaIEIE_554->Write(); 
    hist_ph_sigmaIEIE_555->Write(); 
    hist_ph_sigmaIEIE_556->Write(); 
    hist_ph_sigmaIEIE_557->Write(); 
    hist_ph_sigmaIEIE_558->Write(); 
    hist_ph_sigmaIEIE_559->Write(); 
    hist_ph_sigmaIEIE_560->Write(); 
    hist_ph_sigmaIEIE_561->Write(); 
    hist_ph_sigmaIEIE_562->Write(); 
    hist_ph_sigmaIEIE_563->Write(); 
    hist_ph_sigmaIEIE_564->Write(); 
    hist_ph_sigmaIEIE_565->Write(); 
    hist_ph_sigmaIEIE_566->Write(); 
    hist_ph_sigmaIEIE_567->Write(); 
    hist_ph_sigmaIEIE_568->Write(); 
    hist_ph_sigmaIEIE_569->Write(); 
    hist_ph_sigmaIEIE_570->Write(); 
    hist_ph_sigmaIEIE_571->Write(); 
    hist_ph_sigmaIEIE_572->Write(); 
    hist_ph_sigmaIEIE_573->Write(); 
    hist_ph_sigmaIEIE_574->Write(); 
    hist_ph_sigmaIEIE_575->Write(); 
    hist_ph_sigmaIEIE_576->Write(); 
    hist_ph_sigmaIEIE_577->Write(); 
    hist_ph_sigmaIEIE_578->Write(); 
    hist_ph_sigmaIEIE_579->Write(); 
    hist_ph_sigmaIEIE_580->Write(); 
    hist_ph_sigmaIEIE_581->Write(); 
    hist_ph_sigmaIEIE_582->Write(); 
    hist_ph_sigmaIEIE_583->Write(); 
    hist_ph_sigmaIEIE_584->Write(); 
    hist_ph_sigmaIEIE_585->Write(); 
    hist_ph_sigmaIEIE_586->Write(); 
    hist_ph_sigmaIEIE_587->Write(); 
    hist_ph_sigmaIEIE_588->Write(); 
    hist_ph_sigmaIEIE_589->Write(); 
    hist_ph_sigmaIEIE_590->Write(); 
    hist_ph_sigmaIEIE_591->Write(); 
    hist_ph_sigmaIEIE_592->Write(); 
    hist_ph_sigmaIEIE_593->Write(); 
    hist_ph_sigmaIEIE_594->Write(); 
    hist_ph_sigmaIEIE_595->Write(); 
    hist_ph_sigmaIEIE_596->Write(); 
    hist_ph_sigmaIEIE_597->Write(); 
    hist_ph_sigmaIEIE_598->Write(); 
    hist_ph_sigmaIEIE_599->Write(); 
    hist_ph_sigmaIEIE_600->Write(); 
    hist_ph_sigmaIEIE_601->Write(); 
    hist_ph_sigmaIEIE_602->Write(); 
    hist_ph_sigmaIEIE_603->Write(); 
    hist_ph_sigmaIEIE_604->Write(); 
    hist_ph_sigmaIEIE_605->Write(); 
    hist_ph_sigmaIEIE_606->Write(); 
    hist_ph_sigmaIEIE_607->Write(); 
    hist_ph_sigmaIEIE_608->Write(); 
    hist_ph_sigmaIEIE_609->Write(); 
    hist_ph_sigmaIEIE_610->Write(); 
    hist_ph_sigmaIEIE_611->Write(); 
    hist_ph_sigmaIEIE_612->Write(); 
    hist_ph_sigmaIEIE_613->Write(); 
    hist_ph_sigmaIEIE_614->Write(); 
    hist_ph_sigmaIEIE_615->Write(); 
    hist_ph_sigmaIEIE_616->Write(); 
    hist_ph_sigmaIEIE_617->Write(); 
    hist_ph_sigmaIEIE_618->Write(); 
    hist_ph_sigmaIEIE_619->Write(); 
    hist_ph_sigmaIEIE_620->Write(); 
    hist_ph_sigmaIEIE_621->Write(); 
    hist_ph_sigmaIEIE_622->Write(); 
    hist_ph_sigmaIEIE_623->Write(); 
    hist_ph_sigmaIEIE_624->Write(); 
    hist_ph_sigmaIEIE_625->Write(); 
    hist_ph_sigmaIEIE_626->Write(); 
    hist_ph_sigmaIEIE_627->Write(); 
    hist_ph_sigmaIEIE_628->Write(); 
    hist_ph_sigmaIEIE_629->Write(); 
    hist_ph_sigmaIEIE_630->Write(); 
    hist_ph_sigmaIEIE_631->Write(); 
    hist_ph_sigmaIEIE_632->Write(); 
    hist_ph_sigmaIEIE_633->Write(); 
    hist_ph_sigmaIEIE_634->Write(); 
    hist_ph_sigmaIEIE_635->Write(); 
    hist_ph_sigmaIEIE_636->Write(); 
    hist_ph_sigmaIEIE_637->Write(); 
    hist_ph_sigmaIEIE_638->Write(); 
    hist_ph_sigmaIEIE_639->Write(); 
    hist_ph_sigmaIEIE_640->Write(); 
    hist_ph_sigmaIEIE_641->Write(); 
    hist_ph_sigmaIEIE_642->Write(); 
    hist_ph_sigmaIEIE_643->Write(); 
    hist_ph_sigmaIEIE_644->Write(); 
    hist_ph_sigmaIEIE_645->Write(); 
    hist_ph_sigmaIEIE_646->Write(); 
    hist_ph_sigmaIEIE_647->Write(); 
    hist_ph_sigmaIEIE_648->Write(); 
    hist_ph_sigmaIEIE_649->Write(); 
    hist_ph_sigmaIEIE_650->Write(); 
    hist_ph_sigmaIEIE_651->Write(); 
    hist_ph_sigmaIEIE_652->Write(); 
    hist_ph_sigmaIEIE_653->Write(); 
    hist_ph_sigmaIEIE_654->Write(); 
    hist_ph_sigmaIEIE_655->Write(); 
    hist_ph_sigmaIEIE_656->Write(); 
    hist_ph_sigmaIEIE_657->Write(); 
    hist_ph_sigmaIEIE_658->Write(); 
    hist_ph_sigmaIEIE_659->Write(); 
    hist_ph_sigmaIEIE_660->Write(); 
    hist_ph_sigmaIEIE_661->Write(); 
    hist_ph_sigmaIEIE_662->Write(); 
    hist_ph_sigmaIEIE_663->Write(); 
    hist_ph_sigmaIEIE_664->Write(); 
    hist_ph_sigmaIEIE_665->Write(); 
    hist_ph_sigmaIEIE_666->Write(); 
    hist_ph_sigmaIEIE_667->Write(); 
    hist_ph_sigmaIEIE_668->Write(); 
    hist_ph_sigmaIEIE_669->Write(); 
    hist_ph_sigmaIEIE_670->Write(); 
    hist_ph_sigmaIEIE_671->Write(); 
    hist_ph_sigmaIEIE_672->Write(); 
    hist_ph_sigmaIEIE_673->Write(); 
    hist_ph_sigmaIEIE_674->Write(); 
    hist_ph_sigmaIEIE_675->Write(); 
    hist_ph_sigmaIEIE_676->Write(); 
    hist_ph_sigmaIEIE_677->Write(); 
    hist_ph_sigmaIEIE_678->Write(); 
    hist_ph_sigmaIEIE_679->Write(); 
    hist_ph_sigmaIEIE_680->Write(); 
    hist_ph_sigmaIEIE_681->Write(); 
    hist_ph_sigmaIEIE_682->Write(); 
    hist_ph_sigmaIEIE_683->Write(); 
    hist_ph_sigmaIEIE_684->Write(); 
    hist_ph_sigmaIEIE_685->Write(); 
    hist_ph_sigmaIEIE_686->Write(); 
    hist_ph_sigmaIEIE_687->Write(); 
    hist_ph_sigmaIEIE_688->Write(); 
    hist_ph_sigmaIEIE_689->Write(); 
    hist_ph_sigmaIEIE_690->Write(); 
    hist_ph_sigmaIEIE_691->Write(); 
    hist_ph_sigmaIEIE_692->Write(); 
    hist_ph_sigmaIEIE_693->Write(); 
    hist_ph_sigmaIEIE_694->Write(); 
    hist_ph_sigmaIEIE_695->Write(); 
    hist_ph_sigmaIEIE_696->Write(); 
    hist_ph_sigmaIEIE_697->Write(); 
    hist_ph_sigmaIEIE_698->Write(); 
    hist_ph_sigmaIEIE_699->Write(); 
    hist_ph_sigmaIEIE_700->Write(); 
    hist_ph_sigmaIEIE_701->Write(); 
    hist_ph_sigmaIEIE_702->Write(); 
    hist_ph_sigmaIEIE_703->Write(); 
    hist_ph_sigmaIEIE_704->Write(); 
    hist_ph_sigmaIEIE_705->Write(); 
    hist_ph_sigmaIEIE_706->Write(); 
    hist_ph_sigmaIEIE_707->Write(); 
    hist_ph_sigmaIEIE_708->Write(); 
    hist_ph_sigmaIEIE_709->Write(); 
    hist_ph_sigmaIEIE_710->Write(); 
    hist_ph_sigmaIEIE_711->Write(); 
    hist_ph_sigmaIEIE_712->Write(); 
    hist_ph_sigmaIEIE_713->Write(); 
    hist_ph_sigmaIEIE_714->Write(); 
    hist_ph_sigmaIEIE_715->Write(); 
    hist_ph_sigmaIEIE_716->Write(); 
    hist_ph_sigmaIEIE_717->Write(); 
    hist_ph_sigmaIEIE_718->Write(); 
    hist_ph_sigmaIEIE_719->Write(); 
    hist_ph_sigmaIEIE_720->Write(); 
    hist_ph_sigmaIEIE_721->Write(); 
    hist_ph_sigmaIEIE_722->Write(); 
    hist_ph_sigmaIEIE_723->Write(); 
    hist_ph_sigmaIEIE_724->Write(); 
    hist_ph_sigmaIEIE_725->Write(); 
    hist_ph_sigmaIEIE_726->Write(); 
    hist_ph_sigmaIEIE_727->Write(); 
    hist_ph_sigmaIEIE_728->Write(); 
    hist_ph_sigmaIEIE_729->Write(); 
    hist_ph_sigmaIEIE_730->Write(); 
    hist_ph_sigmaIEIE_731->Write(); 
    hist_ph_sigmaIEIE_732->Write(); 
    hist_ph_sigmaIEIE_733->Write(); 
    hist_ph_sigmaIEIE_734->Write(); 
    hist_ph_sigmaIEIE_735->Write(); 
    hist_ph_sigmaIEIE_736->Write(); 
    hist_ph_sigmaIEIE_737->Write(); 
    hist_ph_sigmaIEIE_738->Write(); 
    hist_ph_sigmaIEIE_739->Write(); 
    hist_ph_sigmaIEIE_740->Write(); 
    hist_ph_sigmaIEIE_741->Write(); 
    hist_ph_sigmaIEIE_742->Write(); 
    hist_ph_sigmaIEIE_743->Write(); 
    hist_ph_sigmaIEIE_744->Write(); 
    hist_ph_sigmaIEIE_745->Write(); 
    hist_ph_sigmaIEIE_746->Write(); 
    hist_ph_sigmaIEIE_747->Write(); 
    hist_ph_sigmaIEIE_748->Write(); 
    hist_ph_sigmaIEIE_749->Write(); 
    hist_ph_sigmaIEIE_750->Write(); 
    hist_ph_sigmaIEIE_751->Write(); 
    hist_ph_sigmaIEIE_752->Write(); 
    hist_ph_sigmaIEIE_753->Write(); 
    hist_ph_sigmaIEIE_754->Write(); 
    hist_ph_sigmaIEIE_755->Write(); 
    hist_ph_sigmaIEIE_756->Write(); 
    hist_ph_sigmaIEIE_757->Write(); 
    hist_ph_sigmaIEIE_758->Write(); 
    hist_ph_sigmaIEIE_759->Write(); 
    hist_ph_sigmaIEIE_760->Write(); 
    hist_ph_sigmaIEIE_761->Write(); 
    hist_ph_sigmaIEIE_762->Write(); 
    hist_ph_sigmaIEIE_763->Write(); 
    hist_ph_sigmaIEIE_764->Write(); 
    hist_ph_sigmaIEIE_765->Write(); 
    hist_ph_sigmaIEIE_766->Write(); 
    hist_ph_sigmaIEIE_767->Write(); 
    hist_ph_sigmaIEIE_768->Write(); 
    hist_ph_sigmaIEIE_769->Write(); 
    hist_ph_sigmaIEIE_770->Write(); 
    hist_ph_sigmaIEIE_771->Write(); 
    hist_ph_sigmaIEIE_772->Write(); 
    hist_ph_sigmaIEIE_773->Write(); 
    hist_ph_sigmaIEIE_774->Write(); 
    hist_ph_sigmaIEIE_775->Write(); 
    hist_ph_sigmaIEIE_776->Write(); 
    hist_ph_sigmaIEIE_777->Write(); 
    hist_ph_sigmaIEIE_778->Write(); 
    hist_ph_sigmaIEIE_779->Write(); 
    hist_ph_sigmaIEIE_780->Write(); 
    hist_ph_sigmaIEIE_781->Write(); 
    hist_ph_sigmaIEIE_782->Write(); 
    hist_ph_sigmaIEIE_783->Write(); 
    hist_ph_sigmaIEIE_784->Write(); 
    hist_ph_sigmaIEIE_785->Write(); 
    hist_ph_sigmaIEIE_786->Write(); 
    hist_ph_sigmaIEIE_787->Write(); 
    hist_ph_sigmaIEIE_788->Write(); 
    hist_ph_sigmaIEIE_789->Write(); 
    hist_ph_sigmaIEIE_790->Write(); 
    hist_ph_sigmaIEIE_791->Write(); 
    hist_ph_sigmaIEIE_792->Write(); 
    hist_ph_sigmaIEIE_793->Write(); 
    hist_ph_sigmaIEIE_794->Write(); 
    hist_ph_sigmaIEIE_795->Write(); 
    hist_ph_sigmaIEIE_796->Write(); 
    hist_ph_sigmaIEIE_797->Write(); 
    hist_ph_sigmaIEIE_798->Write(); 
    hist_ph_sigmaIEIE_799->Write(); 
    hist_ph_sigmaIEIE_800->Write(); 
    hist_ph_sigmaIEIE_801->Write(); 
    hist_ph_sigmaIEIE_802->Write(); 
    hist_ph_sigmaIEIE_803->Write(); 
    hist_ph_sigmaIEIE_804->Write(); 
    hist_ph_sigmaIEIE_805->Write(); 
    hist_ph_sigmaIEIE_806->Write(); 
    hist_ph_sigmaIEIE_807->Write(); 
    hist_ph_sigmaIEIE_808->Write(); 
    hist_ph_sigmaIEIE_809->Write(); 
    hist_ph_sigmaIEIE_810->Write(); 
    hist_ph_sigmaIEIE_811->Write(); 
    hist_ph_sigmaIEIE_812->Write(); 
    hist_ph_sigmaIEIE_813->Write(); 
    hist_ph_sigmaIEIE_814->Write(); 
    hist_ph_sigmaIEIE_815->Write(); 
    hist_ph_sigmaIEIE_816->Write(); 
    hist_ph_sigmaIEIE_817->Write(); 
    hist_ph_sigmaIEIE_818->Write(); 
    hist_ph_sigmaIEIE_819->Write(); 
    hist_ph_sigmaIEIE_820->Write(); 
    hist_ph_sigmaIEIE_821->Write(); 
    hist_ph_sigmaIEIE_822->Write(); 
    hist_ph_sigmaIEIE_823->Write(); 
    hist_ph_sigmaIEIE_824->Write(); 
    hist_ph_sigmaIEIE_825->Write(); 
    hist_ph_sigmaIEIE_826->Write(); 
    hist_ph_sigmaIEIE_827->Write(); 
    hist_ph_sigmaIEIE_828->Write(); 
    hist_ph_sigmaIEIE_829->Write(); 
    hist_ph_sigmaIEIE_830->Write(); 
    hist_ph_sigmaIEIE_831->Write(); 
    hist_ph_sigmaIEIE_832->Write(); 
    hist_ph_sigmaIEIE_833->Write(); 
    hist_ph_sigmaIEIE_834->Write(); 
    hist_ph_sigmaIEIE_835->Write(); 
    hist_ph_sigmaIEIE_836->Write(); 
    hist_ph_sigmaIEIE_837->Write(); 
    hist_ph_sigmaIEIE_838->Write(); 
    hist_ph_sigmaIEIE_839->Write(); 
    hist_ph_sigmaIEIE_840->Write(); 
    hist_ph_sigmaIEIE_841->Write(); 
    hist_ph_sigmaIEIE_842->Write(); 
    hist_ph_sigmaIEIE_843->Write(); 
    hist_ph_sigmaIEIE_844->Write(); 
    hist_ph_sigmaIEIE_845->Write(); 
    hist_ph_sigmaIEIE_846->Write(); 
    hist_ph_sigmaIEIE_847->Write(); 
    hist_ph_sigmaIEIE_848->Write(); 
    hist_ph_sigmaIEIE_849->Write(); 
    hist_ph_sigmaIEIE_850->Write(); 
    hist_ph_sigmaIEIE_851->Write(); 
    hist_ph_sigmaIEIE_852->Write(); 
    hist_ph_sigmaIEIE_853->Write(); 
    hist_ph_sigmaIEIE_854->Write(); 
    hist_ph_sigmaIEIE_855->Write(); 
    hist_ph_sigmaIEIE_856->Write(); 
    hist_ph_sigmaIEIE_857->Write(); 
    hist_ph_sigmaIEIE_858->Write(); 
    hist_ph_sigmaIEIE_859->Write(); 
    hist_ph_sigmaIEIE_860->Write(); 
    hist_ph_sigmaIEIE_861->Write(); 
    hist_ph_sigmaIEIE_862->Write(); 
    hist_ph_sigmaIEIE_863->Write(); 
    hist_ph_sigmaIEIE_864->Write(); 
    hist_ph_sigmaIEIE_865->Write(); 
    hist_ph_sigmaIEIE_866->Write(); 
    hist_ph_sigmaIEIE_867->Write(); 
    hist_ph_sigmaIEIE_868->Write(); 
    hist_ph_sigmaIEIE_869->Write(); 
    hist_ph_sigmaIEIE_870->Write(); 
    hist_ph_sigmaIEIE_871->Write(); 
    hist_ph_sigmaIEIE_872->Write(); 
    hist_ph_sigmaIEIE_873->Write(); 
    hist_ph_sigmaIEIE_874->Write(); 
    hist_ph_sigmaIEIE_875->Write(); 
    hist_ph_sigmaIEIE_876->Write(); 
    hist_ph_sigmaIEIE_877->Write(); 
    hist_ph_sigmaIEIE_878->Write(); 
    hist_ph_sigmaIEIE_879->Write(); 
    hist_ph_sigmaIEIE_880->Write(); 
    hist_ph_sigmaIEIE_881->Write(); 
    hist_ph_sigmaIEIE_882->Write(); 
    hist_ph_sigmaIEIE_883->Write(); 
    hist_ph_sigmaIEIE_884->Write(); 
    hist_ph_sigmaIEIE_885->Write(); 
    hist_ph_sigmaIEIE_886->Write(); 
    hist_ph_sigmaIEIE_887->Write(); 
    hist_ph_sigmaIEIE_888->Write(); 
    hist_ph_sigmaIEIE_889->Write(); 
    hist_ph_sigmaIEIE_890->Write(); 
    hist_ph_sigmaIEIE_891->Write(); 
    hist_ph_sigmaIEIE_892->Write(); 
    hist_ph_sigmaIEIE_893->Write(); 
    hist_ph_sigmaIEIE_894->Write(); 
    hist_ph_sigmaIEIE_895->Write(); 
    hist_ph_sigmaIEIE_896->Write(); 
    hist_ph_sigmaIEIE_897->Write(); 
    hist_ph_sigmaIEIE_898->Write(); 
    hist_ph_sigmaIEIE_899->Write(); 
    hist_ph_sigmaIEIE_900->Write(); 
    hist_ph_sigmaIEIE_901->Write(); 
    hist_ph_sigmaIEIE_902->Write(); 
    hist_ph_sigmaIEIE_903->Write(); 
    hist_ph_sigmaIEIE_904->Write(); 
    hist_ph_sigmaIEIE_905->Write(); 
    hist_ph_sigmaIEIE_906->Write(); 
    hist_ph_sigmaIEIE_907->Write(); 
    hist_ph_sigmaIEIE_908->Write(); 
    hist_ph_sigmaIEIE_909->Write(); 
    hist_ph_sigmaIEIE_910->Write(); 
    hist_ph_sigmaIEIE_911->Write(); 
    hist_ph_sigmaIEIE_912->Write(); 
    hist_ph_sigmaIEIE_913->Write(); 
    hist_ph_sigmaIEIE_914->Write(); 
    hist_ph_sigmaIEIE_915->Write(); 
    hist_ph_sigmaIEIE_916->Write(); 
    hist_ph_sigmaIEIE_917->Write(); 
    hist_ph_sigmaIEIE_918->Write(); 
    hist_ph_sigmaIEIE_919->Write(); 
    hist_ph_sigmaIEIE_920->Write(); 
    hist_ph_sigmaIEIE_921->Write(); 
    hist_ph_sigmaIEIE_922->Write(); 
    hist_ph_sigmaIEIE_923->Write(); 
    hist_ph_sigmaIEIE_924->Write(); 
    hist_ph_sigmaIEIE_925->Write(); 
    hist_ph_sigmaIEIE_926->Write(); 
    hist_ph_sigmaIEIE_927->Write(); 
    hist_ph_sigmaIEIE_928->Write(); 
    hist_ph_sigmaIEIE_929->Write(); 
    hist_ph_sigmaIEIE_930->Write(); 
    hist_ph_sigmaIEIE_931->Write(); 
    hist_ph_sigmaIEIE_932->Write(); 
    hist_ph_sigmaIEIE_933->Write(); 
    hist_ph_sigmaIEIE_934->Write(); 
    hist_ph_sigmaIEIE_935->Write(); 
    hist_ph_sigmaIEIE_936->Write(); 
    hist_ph_sigmaIEIE_937->Write(); 
    hist_ph_sigmaIEIE_938->Write(); 
    hist_ph_sigmaIEIE_939->Write(); 
    hist_ph_sigmaIEIE_940->Write(); 
    hist_ph_sigmaIEIE_941->Write(); 
    hist_ph_sigmaIEIE_942->Write(); 
    hist_ph_sigmaIEIE_943->Write(); 
    hist_ph_sigmaIEIE_944->Write(); 
    hist_ph_sigmaIEIE_945->Write(); 
    hist_ph_sigmaIEIE_946->Write(); 
    hist_ph_sigmaIEIE_947->Write(); 
    hist_ph_sigmaIEIE_948->Write(); 
    hist_ph_sigmaIEIE_949->Write(); 
    hist_ph_sigmaIEIE_950->Write(); 
    hist_ph_sigmaIEIE_951->Write(); 
    hist_ph_sigmaIEIE_952->Write(); 
    hist_ph_sigmaIEIE_953->Write(); 
    hist_ph_sigmaIEIE_954->Write(); 
    hist_ph_sigmaIEIE_955->Write(); 
    hist_ph_sigmaIEIE_956->Write(); 
    hist_ph_sigmaIEIE_957->Write(); 
    hist_ph_sigmaIEIE_958->Write(); 
    hist_ph_sigmaIEIE_959->Write(); 
    hist_ph_sigmaIEIE_960->Write(); 
    hist_ph_sigmaIEIE_961->Write(); 
    hist_ph_sigmaIEIE_962->Write(); 
    hist_ph_sigmaIEIE_963->Write(); 
    hist_ph_sigmaIEIE_964->Write(); 
    hist_ph_sigmaIEIE_965->Write(); 
    hist_ph_sigmaIEIE_966->Write(); 
    hist_ph_sigmaIEIE_967->Write(); 
    hist_ph_sigmaIEIE_968->Write(); 
    hist_ph_sigmaIEIE_969->Write(); 
    hist_ph_sigmaIEIE_970->Write(); 
    hist_ph_sigmaIEIE_971->Write(); 
    hist_ph_sigmaIEIE_972->Write(); 
    hist_ph_sigmaIEIE_973->Write(); 
    hist_ph_sigmaIEIE_974->Write(); 
    hist_ph_sigmaIEIE_975->Write(); 
    hist_ph_sigmaIEIE_976->Write(); 
    hist_ph_sigmaIEIE_977->Write(); 
    hist_ph_sigmaIEIE_978->Write(); 
    hist_ph_sigmaIEIE_979->Write(); 
    hist_ph_sigmaIEIE_980->Write(); 
    hist_ph_sigmaIEIE_981->Write(); 
    hist_ph_sigmaIEIE_982->Write(); 
    hist_ph_sigmaIEIE_983->Write(); 
    hist_ph_sigmaIEIE_984->Write(); 
    hist_ph_sigmaIEIE_985->Write(); 
    hist_ph_sigmaIEIE_986->Write(); 
    hist_ph_sigmaIEIE_987->Write(); 
    hist_ph_sigmaIEIE_988->Write(); 
    hist_ph_sigmaIEIE_989->Write(); 
    hist_ph_sigmaIEIE_990->Write(); 
    hist_ph_sigmaIEIE_991->Write(); 
    hist_ph_sigmaIEIE_992->Write(); 
    hist_ph_sigmaIEIE_993->Write(); 
    hist_ph_sigmaIEIE_994->Write(); 
    hist_ph_sigmaIEIE_995->Write(); 
    hist_ph_sigmaIEIE_996->Write(); 
    hist_ph_sigmaIEIE_997->Write(); 
    hist_ph_sigmaIEIE_998->Write(); 
    hist_ph_sigmaIEIE_999->Write(); 
    hist_ph_sigmaIEIE_1000->Write(); 
    hist_ph_sigmaIEIE_1001->Write(); 
    hist_ph_sigmaIEIE_1002->Write(); 
    hist_ph_sigmaIEIE_1003->Write(); 
    hist_ph_sigmaIEIE_1004->Write(); 
    hist_ph_sigmaIEIE_1005->Write(); 
    hist_ph_sigmaIEIE_1006->Write(); 
    hist_ph_sigmaIEIE_1007->Write(); 
    hist_ph_sigmaIEIE_1008->Write(); 
    hist_ph_sigmaIEIE_1009->Write(); 
    hist_ph_sigmaIEIE_1010->Write(); 
    hist_ph_sigmaIEIE_1011->Write(); 
    hist_ph_sigmaIEIE_1012->Write(); 
    hist_ph_sigmaIEIE_1013->Write(); 
    hist_ph_sigmaIEIE_1014->Write(); 
    hist_ph_sigmaIEIE_1015->Write(); 
    hist_ph_sigmaIEIE_1016->Write(); 
    hist_ph_sigmaIEIE_1017->Write(); 
    hist_ph_sigmaIEIE_1018->Write(); 
    hist_ph_sigmaIEIE_1019->Write(); 
    hist_ph_sigmaIEIE_1020->Write(); 
    hist_ph_sigmaIEIE_1021->Write(); 
    hist_ph_sigmaIEIE_1022->Write(); 
    hist_ph_sigmaIEIE_1023->Write(); 
    hist_ph_sigmaIEIE_1024->Write(); 
    hist_ph_sigmaIEIE_1025->Write(); 
    hist_ph_sigmaIEIE_1026->Write(); 
    hist_ph_sigmaIEIE_1027->Write(); 
    hist_ph_sigmaIEIE_1028->Write(); 
    hist_ph_sigmaIEIE_1029->Write(); 
    hist_ph_sigmaIEIE_1030->Write(); 
    hist_ph_sigmaIEIE_1031->Write(); 
    hist_ph_sigmaIEIE_1032->Write(); 
    hist_ph_sigmaIEIE_1033->Write(); 
    hist_ph_sigmaIEIE_1034->Write(); 
    hist_ph_sigmaIEIE_1035->Write(); 
    hist_ph_sigmaIEIE_1036->Write(); 
    hist_ph_sigmaIEIE_1037->Write(); 
    hist_ph_sigmaIEIE_1038->Write(); 
    hist_ph_sigmaIEIE_1039->Write(); 
    hist_ph_sigmaIEIE_1040->Write(); 
}

void RunModule::Drawph_pt_26( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)>15 && IN::ph_pt->at(0)<25 ); 
         if( weight != 0 ) { 
         hist_ph_pt_26->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_27( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)>25 && IN::ph_pt->at(0)<40 ); 
         if( weight != 0 ) { 
         hist_ph_pt_27->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_28( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)>40 && IN::ph_pt->at(0)<70 ); 
         if( weight != 0 ) { 
         hist_ph_pt_28->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_29( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)>70 && IN::ph_pt->at(0)<1000000 ); 
         if( weight != 0 ) { 
         hist_ph_pt_29->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_30( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)>15 && IN::ph_pt->at(0)<25 ); 
         if( weight != 0 ) { 
         hist_ph_pt_30->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_31( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)>25 && IN::ph_pt->at(0)<40 ); 
         if( weight != 0 ) { 
         hist_ph_pt_31->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_32( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)>40 && IN::ph_pt->at(0)<70 ); 
         if( weight != 0 ) { 
         hist_ph_pt_32->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_33( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)>70 && IN::ph_pt->at(0)<1000000 ); 
         if( weight != 0 ) { 
         hist_ph_pt_33->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_34( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)>15 && IN::ph_pt->at(0)<25 ); 
         if( weight != 0 ) { 
         hist_ph_pt_34->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_35( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)>25 && IN::ph_pt->at(0)<40 ); 
         if( weight != 0 ) { 
         hist_ph_pt_35->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_36( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)>40 && IN::ph_pt->at(0)<70 ); 
         if( weight != 0 ) { 
         hist_ph_pt_36->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_37( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)>70 && IN::ph_pt->at(0)<1000000 ); 
         if( weight != 0 ) { 
         hist_ph_pt_37->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_38( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)>15 && IN::ph_pt->at(0)<25 ); 
         if( weight != 0 ) { 
         hist_ph_pt_38->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_39( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)>25 && IN::ph_pt->at(0)<40 ); 
         if( weight != 0 ) { 
         hist_ph_pt_39->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_40( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)>40 && IN::ph_pt->at(0)<70 ); 
         if( weight != 0 ) { 
         hist_ph_pt_40->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_41( ) const { 
    float weight =  IN::PUWeight * (  IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1  && IN::ph_hasPixSeed->at(0)==0 && IN::ph_passMedium->at(0) && IN::leadPhot_leadLepDR>0.4 && IN::leadPhot_sublLepDR>0.4 && IN::el_n==0  && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)>70 && IN::ph_pt->at(0)<1000000 ); 
         if( weight != 0 ) { 
         hist_ph_pt_41->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::DrawleadPhot_sublLepDR( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  ) ; 
         if( weight != 0 ) { 
         hist_leadPhot_sublLepDR->Fill(IN::leadPhot_sublLepDR, weight); 
         } 
 }
void RunModule::DrawleadPhot_leadLepDR( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  ); 
         if( weight != 0 ) { 
         hist_leadPhot_leadLepDR->Fill(IN::leadPhot_leadLepDR, weight); 
         } 
 }
void RunModule::Drawm_leplepph( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)   && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 ) ) ; 
         if( weight != 0 ) { 
         hist_m_leplepph->Fill(IN::m_leplepph, weight); 
         } 
 }
void RunModule::Drawm_leplepph_m_leplep( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)   && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  ) ; 
         if( weight != 0 ) { 
         hist_m_leplepph_m_leplep->Fill(IN::m_leplepph+IN::m_leplep, weight); 
         } 
 }
void RunModule::DrawleadPhot_leadLepDR_0( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && ( IN::m_leplepph+IN::m_leplep ) < 185  ) ; 
         if( weight != 0 ) { 
         hist_leadPhot_leadLepDR_0->Fill(IN::leadPhot_leadLepDR, weight); 
         } 
 }
void RunModule::DrawleadPhot_leadLepDR_1( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && fabs( IN::m_leplepph-91.2 ) < 5  ) ; 
         if( weight != 0 ) { 
         hist_leadPhot_leadLepDR_1->Fill(IN::leadPhot_leadLepDR, weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_59( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && IN::leadPhot_leadLepDR > 0.3 && fabs( IN::m_leplepph-91.2 ) < 5 && IN::ph_IsEB->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_59->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_60( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && IN::leadPhot_leadLepDR > 0.3 && fabs( IN::m_leplepph-91.2 ) < 5 && IN::ph_IsEE->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_60->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_61( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && IN::leadPhot_leadLepDR > 0.3 && ( IN::m_leplepph+IN::m_leplep ) < 185 && IN::ph_IsEB->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_61->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_62( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && IN::leadPhot_leadLepDR > 0.3 && ( IN::m_leplepph+IN::m_leplep ) < 185 && IN::ph_IsEE->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_62->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_63( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && IN::leadPhot_leadLepDR > 0.3 && fabs( IN::m_leplepph-91.2 ) < 5 && IN::ph_IsEB->at(0) ) ; 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_63->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_64( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && IN::leadPhot_leadLepDR > 0.3 && ( IN::m_leplepph+IN::m_leplep ) < 185 && IN::ph_IsEB->at(0)  ) ; 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_64->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_65( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && IN::leadPhot_leadLepDR > 0.3 && fabs( IN::m_leplepph-91.2 ) < 5 && IN::ph_IsEE->at(0) ) ; 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_65->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_66( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && IN::leadPhot_sublLepDR > 0.3 && ( IN::leadPhot_sublLepDR < 1.0 || IN::leadPhot_leadLepDR < 1.0 )  && IN::leadPhot_leadLepDR > 0.3 && ( IN::m_leplepph+IN::m_leplep ) < 185 && IN::ph_IsEE->at(0)  ) ; 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_66->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::DrawleadPhot_sublLepDR_0( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 ); 
         if( weight != 0 ) { 
         hist_leadPhot_sublLepDR_0->Fill(IN::leadPhot_sublLepDR, weight); 
         } 
 }
void RunModule::DrawleadPhot_leadLepDR_2( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 ); 
         if( weight != 0 ) { 
         hist_leadPhot_leadLepDR_2->Fill(IN::leadPhot_leadLepDR, weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_67( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_67->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_68( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_68->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_69( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_69->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_70( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_70->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_71( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_71->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_72( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_72->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_73( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_73->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_74( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_74->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_75( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_75->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_76( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_76->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_77( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_77->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_78( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_78->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_79( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_79->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_80( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_80->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_81( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_81->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_82( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_82->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_83( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_83->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_84( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_84->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_85( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_85->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_86( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_86->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_87( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_87->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_88( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_88->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_89( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_89->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_90( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15.000000 && IN::ph_pt->at(0) < 25.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_90->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_91( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_91->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_92( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_92->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_93( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_93->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_94( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_94->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_95( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_95->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_96( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_96->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_97( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_97->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_98( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_98->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_99( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_99->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_100( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_100->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_101( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_101->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_102( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_102->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_103( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_103->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_104( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_104->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_105( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_105->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_106( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_106->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_107( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_107->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_108( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25.000000 && IN::ph_pt->at(0) < 40.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_108->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_109( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_109->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_110( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_110->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_111( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_111->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_112( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_112->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_113( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_113->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_114( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_114->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_115( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_115->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_116( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_116->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_117( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_117->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_118( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_118->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_119( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_119->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_120( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_120->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_121( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_121->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_122( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_122->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_123( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_123->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_124( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_124->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_125( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_125->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_126( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40.000000 && IN::ph_pt->at(0) < 70.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_126->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_127( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_127->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_128( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_128->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_129( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_129->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_130( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_130->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_131( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_131->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_132( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_132->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_133( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_133->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_134( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_134->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_135( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_135->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_136( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_136->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_137( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_137->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_138( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_138->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_139( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_139->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_140( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_140->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_141( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_141->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_142( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_142->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_143( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_143->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_144( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70.000000 && IN::ph_pt->at(0) < 200.000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_144->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_42( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_42->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_43( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011000 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_43->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_44( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_44->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_45( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011000 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_45->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_46( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_46->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_47( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011000 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_47->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_48( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_48->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_49( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011000 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_49->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_50( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_50->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_51( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011000 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_51->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_52( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_52->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_53( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011000 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_53->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_54( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_54->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_55( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.033000 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_55->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_56( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_56->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_57( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.033000 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_57->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_58( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_58->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_59( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.033000 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_59->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_60( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_60->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_61( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.033000 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_61->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_62( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_62->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_63( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.033000 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_63->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_64( ) const { 
    float weight = IN::PUWeight*(IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.011 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_64->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_pt_65( ) const { 
    float weight = IN::PUWeight * (IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_sigmaIEIE->at(0)>0.033000 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 ); 
         if( weight != 0 ) { 
         hist_ph_pt_65->Fill(IN::ph_pt->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_145( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_145->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_146( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_146->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_147( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_147->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_148( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_148->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_149( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_149->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_150( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_150->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_151( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_151->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_152( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_152->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_153( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_153->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_154( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_154->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_155( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_155->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_156( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_156->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_157( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_157->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_158( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)> 25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_158->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_159( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_159->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_160( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_160->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_161( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_161->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_162( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_162->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_163( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_163->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_164( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_164->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_165( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_165->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_166( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_166->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_167( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_167->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_168( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_168->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_169( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_169->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_170( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_170->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_171( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_171->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_172( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_172->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_173( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_173->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_174( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_174->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_175( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_175->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_176( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)> 40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_176->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_177( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_177->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_178( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_178->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_179( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_179->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_180( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_180->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_181( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_181->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_182( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_182->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_183( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_183->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_184( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_184->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_185( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_185->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_186( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_186->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_187( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_187->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_188( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_188->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_189( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_189->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_190( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_190->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_191( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_191->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_192( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_192->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_193( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_193->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_194( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)> 70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_194->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_195( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_195->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_196( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_196->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_197( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_197->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_198( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_198->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_199( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_199->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_200( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_200->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_201( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_201->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_202( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_202->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_203( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_203->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_204( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_204->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_205( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_205->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_206( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_206->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_207( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_207->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_208( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_208->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_209( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_209->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_210( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_210->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_211( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_211->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_212( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)> 25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_212->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_213( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_213->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_214( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_214->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_215( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_215->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_216( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_216->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_217( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_217->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_218( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_218->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_219( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_219->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_220( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_220->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_221( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_221->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_222( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_222->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_223( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_223->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_224( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_224->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_225( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_225->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_226( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_226->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_227( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_227->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_228( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_228->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_229( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_229->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_230( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)> 40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_230->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_231( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_231->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_232( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_232->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_233( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_233->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_234( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_234->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_235( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_235->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_236( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_236->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_237( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_237->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_238( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_238->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_239( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_239->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_240( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_240->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_241( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_241->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_242( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_242->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_243( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_243->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_244( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_244->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_245( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_245->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_246( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_246->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_247( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_247->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_248( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_pt->at(0)> 70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_248->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_249( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_249->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_250( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_250->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_251( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_251->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_252( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_252->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_253( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_253->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_254( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_254->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_255( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_255->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_256( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_256->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_257( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_257->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_258( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_258->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_259( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_259->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_260( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_260->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_261( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_261->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_262( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_262->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_263( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_263->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_264( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_264->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_265( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_265->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_266( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)> 25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_266->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_267( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_267->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_268( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_268->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_269( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_269->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_270( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_270->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_271( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_271->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_272( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_272->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_273( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_273->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_274( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_274->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_275( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_275->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_276( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_276->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_277( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_277->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_278( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_278->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_279( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_279->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_280( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_280->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_281( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_281->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_282( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_282->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_283( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_283->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_284( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)> 40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_284->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_285( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_285->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_286( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_286->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_287( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_287->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_288( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_288->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_289( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_289->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_290( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_290->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_291( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_291->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_292( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_292->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_293( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_293->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_294( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_294->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_295( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_295->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_296( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_296->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_297( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_297->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_298( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_298->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_299( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_299->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_300( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_300->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_301( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_301->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_302( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)> 70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_302->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_303( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_303->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_304( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_304->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_305( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_305->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_306( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_306->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_307( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_307->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_308( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_308->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_309( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_309->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_310( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_310->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_311( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_311->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_312( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_312->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_313( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_313->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_314( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_314->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_315( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_315->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_316( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_316->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_317( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_317->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_318( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_318->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_319( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_319->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_320( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)> 25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_320->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_321( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_321->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_322( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_322->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_323( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 15 && IN::ph_pt->at(0) < 25 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_323->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_324( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  25 && IN::ph_pt->at(0) < 40); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_324->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_325( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_325->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_326( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_326->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_327( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_327->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_328( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_328->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_329( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_329->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_330( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_330->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_331( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_331->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_332( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_332->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_333( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_333->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_334( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_334->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_335( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_335->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_336( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_336->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_337( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_337->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_338( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)> 40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_338->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_339( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_339->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_340( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_340->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_341( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 25 && IN::ph_pt->at(0) < 40 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_341->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_342( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  40 && IN::ph_pt->at(0) < 70); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_342->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_343( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_343->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_344( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 5 && IN::ph_neuIsoCorr->at(0) < 3 && IN::ph_phoIsoCorr->at(0) < 3 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_344->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_345( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_345->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_346( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 8 && IN::ph_neuIsoCorr->at(0) < 5 && IN::ph_phoIsoCorr->at(0) < 5 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_346->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_347( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_347->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_348( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7 && IN::ph_phoIsoCorr->at(0) < 7 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_348->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_349( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_349->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_350( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9 && IN::ph_phoIsoCorr->at(0) < 9 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_350->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_351( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_351->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_352( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_352->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_353( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_353->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_354( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 70 && IN::ph_pt->at(0) < 1000000 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_354->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_355( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_355->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_356( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_hasPixSeed->at(0)==0 && IN::ph_HoverE12->at(0)<0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0)  && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_pt->at(0)> 70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_356->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_357( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_357->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_358( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_pt->at(0) >  70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_358->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_359( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) > 40 && IN::ph_pt->at(0) < 70 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_359->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_360( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR>1.0 && IN::leadPhot_leadLepDR>1.0 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_pt->at(0) >  70 && IN::ph_pt->at(0) < 1000000); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_360->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_361( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_361->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_362( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_362->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_363( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_363->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_364( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_364->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_365( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 30 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_365->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_366( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) > 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_366->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_367( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_367->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_368( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_368->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_369( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_369->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_370( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_370->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_371( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 30 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_371->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_372( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) > 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_372->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_373( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_373->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_374( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_SCRChIso->at(0) > 2 && IN::ph_SCRChIso->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_374->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_375( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_375->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_376( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_376->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_377( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 30 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_377->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_378( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRChIso->at(0) > 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_378->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_379( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_379->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_380( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_SCRChIso->at(0) > 2 && IN::ph_SCRChIso->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_380->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_381( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_381->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_382( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_382->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_383( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 30 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_383->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_384( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRChIso->at(0) > 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_384->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_385( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_385->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_386( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_neuIsoCorr->at(0) > 1 && IN::ph_neuIsoCorr->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_386->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_387( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_387->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_388( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_388->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_389( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_389->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_390( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_neuIsoCorr->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_390->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_391( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_391->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_392( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_neuIsoCorr->at(0) > 1 && IN::ph_neuIsoCorr->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_392->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_393( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_393->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_394( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_394->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_395( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_395->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_396( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_neuIsoCorr->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_396->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_397( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_397->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_398( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_SCRNeuIso->at(0) > 1 && IN::ph_SCRNeuIso->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_398->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_399( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_399->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_400( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_400->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_401( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_401->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_402( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRNeuIso->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_402->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_403( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_403->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_404( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_SCRNeuIso->at(0) > 1 && IN::ph_SCRNeuIso->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_404->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_405( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_405->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_406( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_406->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_407( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_407->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_408( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRNeuIso->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_408->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_409( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_409->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_410( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_phoIsoCorr->at(0) > 1 && IN::ph_phoIsoCorr->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_410->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_411( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_411->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_412( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_412->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_413( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_413->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_414( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_phoIsoCorr->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_414->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_415( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_415->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_416( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_phoIsoCorr->at(0) > 1 && IN::ph_phoIsoCorr->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_416->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_417( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_417->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_418( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_418->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_419( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_419->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_420( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_phoIsoCorr->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_420->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_421( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_421->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_422( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_SCRPhoIso->at(0) > 1 && IN::ph_SCRPhoIso->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_422->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_423( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_423->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_424( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_424->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_425( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_425->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_426( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRPhoIso->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_426->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_427( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_427->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_428( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_SCRPhoIso->at(0) > 1 && IN::ph_SCRPhoIso->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_428->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_429( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_429->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_430( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_430->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_431( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_431->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_432( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRPhoIso->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_432->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_433( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_433->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_434( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_434->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_435( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_435->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_436( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_436->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_437( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_437->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_438( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_438->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_439( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_439->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_440( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_440->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_441( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_441->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_442( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_442->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_443( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_443->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_444( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_444->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_445( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_445->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_446( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_446->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_447( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_447->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_448( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_448->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_449( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_449->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_450( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_450->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_451( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_451->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_452( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_452->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_453( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_453->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_454( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_454->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_455( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_455->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_456( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_456->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_457( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_457->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_458( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_458->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_459( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_459->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_460( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_460->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_461( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_461->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_462( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_462->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_463( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_463->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_464( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_464->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_465( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_465->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_466( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_466->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_467( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_467->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_468( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_468->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_469( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_469->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_470( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_470->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_471( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_471->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_472( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_472->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_473( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_473->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_474( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_474->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_475( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_475->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_476( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_476->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_477( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_477->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_478( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_478->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_479( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_479->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_480( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_480->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_481( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_481->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_482( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_482->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_483( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_483->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_484( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_484->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_485( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_485->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_486( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_486->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_487( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_487->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_488( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_488->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_489( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_489->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_490( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_490->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_491( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_491->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_492( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_492->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_493( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_493->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_494( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_494->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_495( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_495->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_496( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_496->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_497( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_497->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_498( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_498->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_499( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_499->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_500( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_500->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_501( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_501->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_502( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_502->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_503( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_503->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_504( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_504->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_505( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_505->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_506( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_506->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_507( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_507->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_508( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_508->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_509( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_509->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_510( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_510->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_511( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_511->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_512( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_512->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_513( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_513->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_514( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_514->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_515( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_515->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_516( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_516->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_517( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_517->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_518( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_518->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_519( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_519->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_520( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_520->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_521( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_521->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_522( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_522->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_523( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_523->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_524( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_524->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_525( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_525->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_526( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_526->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_527( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_527->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_528( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_528->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_529( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_529->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_530( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_530->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_531( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_531->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_532( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_532->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_533( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_533->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_534( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_534->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_535( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_535->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_536( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_536->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_537( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_537->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_538( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_538->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_539( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_539->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_540( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_540->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_541( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_541->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_542( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_542->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_543( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_543->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_544( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_544->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_545( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_545->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_546( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_546->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_547( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_547->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_548( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_548->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_549( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_549->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_550( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_550->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_551( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_551->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_552( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_552->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_553( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_553->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_554( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_554->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_555( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_555->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_556( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_556->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_557( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_557->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_558( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_558->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_559( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_559->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_560( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_560->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_561( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_561->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_562( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_562->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_563( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_563->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_564( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_564->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_565( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_565->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_566( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_566->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_567( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_567->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_568( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_568->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_569( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_569->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_570( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_570->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_571( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_571->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_572( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_572->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_573( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_573->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_574( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_574->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_575( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_575->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_576( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_576->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_577( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 30 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_577->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_578( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_chIsoCorr->at(0) > 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_578->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_579( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_579->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_580( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_580->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_581( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_581->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_582( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_582->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_583( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 30 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_583->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_584( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_chIsoCorr->at(0) > 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_584->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_585( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_585->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_586( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_SCRChIso->at(0) > 2 && IN::ph_SCRChIso->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_586->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_587( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_587->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_588( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_588->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_589( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 30 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_589->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_590( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRChIso->at(0) > 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_590->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_591( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_591->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_592( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_SCRChIso->at(0) > 2 && IN::ph_SCRChIso->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_592->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_593( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_593->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_594( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_594->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_595( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRChIso->at(0) > 5 && IN::ph_SCRChIso->at(0) < 30 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_595->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_596( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRChIso->at(0) > 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_596->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_597( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_597->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_598( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_neuIsoCorr->at(0) > 1 && IN::ph_neuIsoCorr->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_598->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_599( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_599->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_600( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_600->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_601( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_601->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_602( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_neuIsoCorr->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_602->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_603( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_603->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_604( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_neuIsoCorr->at(0) > 1 && IN::ph_neuIsoCorr->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_604->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_605( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_605->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_606( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_606->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_607( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_neuIsoCorr->at(0) > 2 && IN::ph_neuIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_607->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_608( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_neuIsoCorr->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_608->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_609( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_609->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_610( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_SCRNeuIso->at(0) > 1 && IN::ph_SCRNeuIso->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_610->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_611( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_611->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_612( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_612->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_613( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_613->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_614( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRNeuIso->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_614->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_615( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_615->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_616( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_SCRNeuIso->at(0) > 1 && IN::ph_SCRNeuIso->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_616->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_617( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_617->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_618( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_618->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_619( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRNeuIso->at(0) > 2 && IN::ph_SCRNeuIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_619->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_620( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRNeuIso->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_620->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_621( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_621->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_622( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_phoIsoCorr->at(0) > 1 && IN::ph_phoIsoCorr->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_622->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_623( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_623->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_624( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_624->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_625( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_625->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_626( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_phoIsoCorr->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_626->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_627( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_627->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_628( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_phoIsoCorr->at(0) > 1 && IN::ph_phoIsoCorr->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_628->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_629( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_629->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_630( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_630->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_631( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_phoIsoCorr->at(0) > 2 && IN::ph_phoIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_631->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_632( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_phoIsoCorr->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_632->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_633( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_633->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_634( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) &&  IN::ph_SCRPhoIso->at(0) > 1 && IN::ph_SCRPhoIso->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_634->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_635( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_635->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_636( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_636->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_637( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_637->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_638( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0) && IN::ph_SCRPhoIso->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_638->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_639( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_639->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_640( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) &&  IN::ph_SCRPhoIso->at(0) > 1 && IN::ph_SCRPhoIso->at(0) < 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_640->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_641( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 4 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_641->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_642( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 6 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_642->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_643( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRPhoIso->at(0) > 2 && IN::ph_SCRPhoIso->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_643->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_644( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0) && IN::ph_SCRPhoIso->at(0) > 2 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_644->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_645( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_645->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_646( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_646->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_647( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_647->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_648( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_648->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_649( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_649->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_650( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_650->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_651( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_651->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_652( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_652->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_653( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_653->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_654( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_654->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_655( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_655->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_656( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_656->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_657( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_657->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_658( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_658->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_659( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_659->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_660( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_660->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_661( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_661->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_662( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_662->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_663( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_663->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_664( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_664->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_665( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_665->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_666( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_666->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_667( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_667->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_668( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_668->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_669( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_669->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_670( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_670->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_671( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_671->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_672( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_672->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_673( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_673->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_674( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_674->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_675( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_675->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_676( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_676->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_677( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_677->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_678( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_678->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_679( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_679->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_680( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_680->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_681( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_681->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_682( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_682->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_683( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_683->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_684( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_684->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_685( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_685->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_686( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_686->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_687( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_687->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_688( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_688->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_689( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_689->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_690( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_690->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_691( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_691->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_692( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_692->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_693( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_693->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_694( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_694->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_695( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_695->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_696( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_696->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_697( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_697->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_698( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_698->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_699( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_699->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_700( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_700->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_701( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_701->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_702( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_702->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_703( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_703->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_704( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_704->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_705( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_705->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_706( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_706->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_707( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_707->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_708( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_708->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_709( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_709->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_710( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_710->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_711( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_711->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_712( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_712->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_713( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_713->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_714( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_714->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_715( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_715->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_716( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_716->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_717( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_717->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_718( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_718->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_719( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_719->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_720( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_720->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_721( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_721->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_722( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_722->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_723( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_723->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_724( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_724->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_725( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_725->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_726( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_726->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_727( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_727->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_728( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_728->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_729( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_729->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_730( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_730->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_731( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_731->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_732( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_732->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_733( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_733->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_734( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_734->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_735( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_735->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_736( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_736->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_737( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_737->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_738( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_738->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_739( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_739->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_740( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_740->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_741( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_741->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_742( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_742->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_743( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_743->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_744( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_744->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_745( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_745->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_746( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_746->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_747( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_747->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_748( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_748->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_749( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_749->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_750( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_750->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_751( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_751->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_752( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_752->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_753( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_753->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_754( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_754->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_755( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_755->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_756( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_756->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_757( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_757->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_758( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_758->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_759( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_759->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_760( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_760->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_761( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_761->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_762( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_762->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_763( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_763->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_764( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_764->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_765( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_765->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_766( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_766->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_767( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_767->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_768( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_768->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_769( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_769->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_770( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_770->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_771( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_771->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_772( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_772->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_773( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_773->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_774( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_774->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_775( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_775->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_776( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_776->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_777( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_777->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_778( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_778->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_779( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 5  && IN::ph_neuIsoCorr->at(0) < 3  && IN::ph_phoIsoCorr->at(0) < 3  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_779->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_780( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 8  && IN::ph_neuIsoCorr->at(0) < 5  && IN::ph_phoIsoCorr->at(0) < 5  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_780->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_781( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 10 && IN::ph_neuIsoCorr->at(0) < 7  && IN::ph_phoIsoCorr->at(0) < 7  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_781->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_782( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 12 && IN::ph_neuIsoCorr->at(0) < 9  && IN::ph_phoIsoCorr->at(0) < 9  ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_782->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_783( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 15 && IN::ph_neuIsoCorr->at(0) < 11 && IN::ph_phoIsoCorr->at(0) < 11 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_783->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_784( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) < 20 && IN::ph_neuIsoCorr->at(0) < 16 && IN::ph_phoIsoCorr->at(0) < 16 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_784->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_785( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_785->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_786( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_786->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_787( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_787->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_788( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_788->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_789( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_789->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_790( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_790->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_791( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_791->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_792( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_792->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_793( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_793->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_794( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_794->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_795( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_795->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_796( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_796->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_797( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_797->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_798( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_798->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_799( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_799->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_800( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_800->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_801( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_801->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_802( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_802->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_803( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_803->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_804( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_804->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_805( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_805->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_806( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_806->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_807( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_807->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_808( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_808->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_809( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_809->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_810( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_810->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_811( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_811->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_812( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_812->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_813( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_813->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_814( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_814->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_815( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_815->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_816( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_816->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_817( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_817->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_818( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_818->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_819( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_819->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_820( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_820->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_821( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_821->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_822( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_822->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_823( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_823->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_824( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_824->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_825( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_825->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_826( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_826->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_827( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_827->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_828( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_828->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_829( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_829->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_830( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_830->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_831( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_831->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_832( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_832->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_833( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_833->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_834( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_834->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_835( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_835->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_836( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_836->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_837( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_837->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_838( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_838->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_839( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_839->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_840( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_840->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_841( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_841->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_842( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_842->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_843( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_843->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_844( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_844->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_845( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_845->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_846( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_846->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_847( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_847->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_848( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_848->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_849( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_849->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_850( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_850->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_851( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_851->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_852( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_852->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_853( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_853->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_854( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_854->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_855( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_855->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_856( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_856->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_857( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_857->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_858( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_858->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_859( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_859->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_860( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_860->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_861( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_861->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_862( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_862->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_863( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_863->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_864( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_864->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_865( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_865->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_866( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_866->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_867( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_867->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_868( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_868->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_869( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_869->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_870( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_870->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_871( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_871->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_872( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_872->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_873( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_873->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_874( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_874->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_875( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_875->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_876( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_876->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_877( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_877->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_878( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_878->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_879( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_879->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_880( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_880->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_881( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_881->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_882( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_882->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_883( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_883->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_884( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_884->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_885( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_885->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_886( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_886->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_887( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_887->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_888( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_888->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_889( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_889->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_890( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_890->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_891( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_891->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_892( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_892->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_893( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_893->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_894( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_894->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_895( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_895->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_896( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_896->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_897( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_897->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_898( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_898->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_899( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_899->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_900( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_900->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_901( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_901->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_902( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_902->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_903( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_903->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_904( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_904->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_905( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_905->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_906( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_906->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_907( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_907->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_908( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_908->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_909( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_909->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_910( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_910->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_911( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_911->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_912( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_912->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_913( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_913->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_914( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_914->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_915( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_915->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_916( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_916->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_917( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_917->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_918( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_918->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_919( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_919->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_920( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_920->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_921( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_921->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_922( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_922->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_923( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_923->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_924( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_924->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_925( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_925->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_926( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_926->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_927( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_927->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_928( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_928->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_929( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_929->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_930( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_930->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_931( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_931->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_932( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_932->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_933( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_933->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_934( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_934->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_935( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_935->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_936( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_936->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_937( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_937->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_938( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_938->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_939( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_939->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_940( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_940->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_941( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_941->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_942( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_942->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_943( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_943->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_944( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_944->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_945( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_945->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_946( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_946->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_947( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_947->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_948( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_948->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_949( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_949->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_950( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_950->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_951( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_951->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_952( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_952->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_953( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_953->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_954( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_954->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_955( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_955->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_956( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_956->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_957( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_957->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_958( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_958->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_959( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_959->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_960( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_960->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_961( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_961->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_962( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_962->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_963( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_963->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_964( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_964->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_965( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_965->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_966( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_966->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_967( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_967->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_968( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_968->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_969( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_969->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_970( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_970->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_971( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_971->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_972( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_972->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_973( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_973->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_974( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_974->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_975( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_975->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_976( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEB->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_976->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_977( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_977->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_978( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_978->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_979( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_979->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_980( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_980->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_981( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_981->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_982( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_982->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_983( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_983->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_984( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_984->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_985( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_985->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_986( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_986->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_987( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_987->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_988( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_988->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_989( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_989->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_990( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_990->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_991( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_991->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_992( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_992->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_993( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_993->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_994( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_994->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_995( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_995->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_996( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_996->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_997( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_997->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_998( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_998->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_999( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_999->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1000( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1000->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1001( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1001->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1002( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1002->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1003( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1003->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1004( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1004->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1005( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1005->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1006( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1006->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1007( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1007->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1008( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1008->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1009( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1009->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1010( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1010->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1011( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1011->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1012( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1012->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1013( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1013->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1014( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1014->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1015( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1015->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1016( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 0  && IN::ph_pt->at(0) < 5  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1016->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1017( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1017->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1018( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1018->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1019( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1019->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1020( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 5  && IN::ph_pt->at(0) < 10  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1020->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1021( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1021->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1022( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1022->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1023( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1023->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1024( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 10  && IN::ph_pt->at(0) < 15  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1024->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1025( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1025->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1026( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1026->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1027( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1027->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1028( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 15  && IN::ph_pt->at(0) < 25  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1028->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1029( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1029->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1030( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1030->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1031( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1031->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1032( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 25  && IN::ph_pt->at(0) < 40  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1032->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1033( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1033->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1034( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1034->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1035( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1035->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1036( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 40  && IN::ph_pt->at(0) < 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1036->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1037( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_passChIsoCorrMedium->at(0) ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1037->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1038( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  &&  IN::ph_chIsoCorr->at(0) > 2 && IN::ph_chIsoCorr->at(0) < 5 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1038->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1039( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 10 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1039->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
void RunModule::Drawph_sigmaIEIE_1040( ) const { 
    float weight = IN::PUWeight * ( IN::mu_passtrig25_n>0 && IN::mu_n==2 && IN::ph_n==1 && IN::ph_HoverE12->at(0) < 0.05 && IN::ph_passNeuIsoCorrMedium->at(0) && IN::ph_passPhoIsoCorrMedium->at(0) && fabs( IN::m_leplep-91.2 ) < 5 && IN::leadPhot_sublLepDR >1 && IN::leadPhot_leadLepDR>1 && IN::ph_IsEE->at(0)  && IN::ph_pt->at(0) > 70  && IN::ph_chIsoCorr->at(0) > 5 && IN::ph_chIsoCorr->at(0) < 20 ); 
         if( weight != 0 ) { 
         hist_ph_sigmaIEIE_1040->Fill(IN::ph_sigmaIEIE->at(0), weight); 
         } 
 }
