"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

p.add_argument('--outputFile',     default=None,  type=str ,        dest='outputFile',         help='output directory for histograms')

options = p.parse_args()

import sys
import os
import re
import ROOT

from SampleManager import SampleManager

ROOT.gROOT.SetBatch(False)

samplesLLG  = None
def main() :

    global samplesLLG
    global samplesLG

    baseDirLGG = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaGammaNoPhID_2015_11_09'
    baseDirLLG = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_11_09'
    baseDirLG  = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfLLG = 'Modules/ZJetsTemplates.py'

    samplesLLG     = SampleManager(baseDirLLG , treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesLG     = SampleManager(baseDirLG , treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesLGG     = SampleManager(baseDirLGG , treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesLLG    .ReadSamples( sampleConfLLG )
    samplesLG    .ReadSamples( sampleConfLLG )
    samplesLGG    .ReadSamples( sampleConfLLG )

    ROOT.gROOT.SetBatch(True)

    binning = { 'sigmaIEIE'  : { 'EB' : (30, 0, 0.03), 'EE' : (30, 0, 0.09) },
                'chIsoCorr'  : { 'EB' : (30, 0, 45), 'EE' : (35, 0, 42) },
                'neuIsoCorr' : { 'EB' : (40, -2, 38), 'EE' : (30, -2, 43) },
                'phoIsoCorr' : { 'EB' : (53, -2.1, 35), 'EE' : (42, -2, 40) }
              }

    pt_bins = [(15, 25), (25,40), (40,70), (70,1000000)]

    _sieie_cuts  = { 'EB' : (0.011,0.029), 'EE' : (0.033, 0.087) }
    _chIso_cuts  = { 'EB' : (1.5, 19.5)  , 'EE' : (1.2,20.4) }
    _neuIso_cuts = { 'EB' : (1.0,20)     , 'EE' : (1.5,20.5) }
    _phoIso_cuts = { 'EB' : (0.7,20.3)   , 'EE' : (1.0,20) }

    vars = ['sigmaIEIE', 'chIsoCorr', 'phoIsoCorr']

    all_hists = []


    for var in vars :
        for eta in ['EB', 'EE'] :
            for ptmin, ptmax in pt_bins :

                draw_str_fake=None
                if var == 'sigmaIEIE' :
                    draw_str_fake = 'mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoSIEIENoEleVeto_n==1 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_%s[0] < %f ' %( ptmin, ptmax, eta, var, _sieie_cuts[eta][1] )
                elif var == 'chIsoCorr' :
                    draw_str_fake = 'mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoChIso_n==1 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1  && ph_passSIEIEMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_%s[0] < %f ' %( ptmin, ptmax, eta, var, _chIso_cuts[eta][1] )
                elif var == 'phoIsoCorr' :
                    draw_str_fake = 'mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoPhoIso_n==1 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1  && ph_passSIEIEMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_%s[0] < %f ' %( ptmin, ptmax, eta, var, _phoIso_cuts[eta][1] )


                samplesLLG.Draw('ph_%s[0]'%var, draw_str_fake, binning[var][eta] )


                hist_data = samplesLLG.get_samples( name='Muon' )[0]
                hist_bkg = samplesLLG.get_samples( name='Zg' )[0]

                hist_subtracted = hist_data.hist.Clone( '%s_Subtracted_%s_%d-%d' %( var, eta, ptmin, ptmax ))

                hist_subtracted.Add( hist_bkg.hist, -1 )

                all_hists.append( hist_data.hist.Clone( '%s_Data_%s_%d-%d' %( var, eta, ptmin, ptmax ) ) )
                all_hists.append( hist_bkg.hist.Clone( '%s_Zg_%s_%d-%d' %( var, eta, ptmin, ptmax ) ) )
                all_hists.append( hist_subtracted)

                draw_str_real = None
                if var=='sigmaIEIE' :
                    #draw_str_real = 'mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoSIEIEPassCSEV_n==1  && m_elel > 40 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25  && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_%s[0] < %f ' %(ptmin, ptmax,eta, var, _sieie_cuts[eta][1]) 
                    draw_str_real = 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoSIEIENoEleVeto_n==1  && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && (fabs(ph_pt[0]-ph_truthMatchPt_ph[0])/ph_truthMatchPt_ph[0]) < 2 && (ph_truthMatchParentage_ph[0] & 4 ) == 0 && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_%s[0] < %f ' %(ptmin, ptmax,eta, var, _sieie_cuts[eta][1]) 
                elif var == 'chIsoCorr' :                                                                            
                    #draw_str_real = 'mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoChIsoPassCSEV_n==1  && m_elel > 40 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25  && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_%s[0] < %f ' %(ptmin, ptmax,eta, var, _chIso_cuts[eta][1]) 
                    draw_str_real = 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoChIsoNoEleVeto_n==1  && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && (fabs(ph_pt[0]-ph_truthMatchPt_ph[0])/ph_truthMatchPt_ph[0]) < 2 && (ph_truthMatchParentage_ph[0] & 4 ) == 0  && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_%s[0] < %f ' %(ptmin, ptmax,eta, var, _chIso_cuts[eta][1]) 
                elif var == 'phoIsoCorr' :                                                                            
                    #draw_str_real = 'mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoPhoIsoPassCSEV_n==1 && m_elel > 40 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25  && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_%s[0] < %f ' %(ptmin, ptmax,eta, var, _phoIso_cuts[eta][1]) 
                    draw_str_real = 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoPhoIsoNoEleVeto_n==1 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0]  && (fabs(ph_pt[0]-ph_truthMatchPt_ph[0])/ph_truthMatchPt_ph[0]) < 2 && (ph_truthMatchParentage_ph[0] & 4 ) == 0  && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_%s[0] < %f ' %(ptmin, ptmax,eta, var, _phoIso_cuts[eta][1]) 

                samplesLG.create_hist( 'Wg', 'ph_%s[0]' %var, draw_str_real, binning[var][eta],)

                newhist = samplesLG.get_samples( name='Wg' )[0].hist.Clone( '%s_Wg_%s_%d-%d' %( var, eta, ptmin, ptmax ) )

                all_hists.append(newhist)

    #for var in vars :
    #    for etalead in ['EB', 'EE'] :
    #        for etasubl in ['EB', 'EE'] :
    #            if etalead=='EE' and etasubl=='EE' :
    #                continue
    #            for ptmin, ptmax in pt_bins :

    #                draw_str_2d = None
    #                draw_var = None
    #                if var == 'sigmaIEIE' :
    #                    draw_str_2d = 'mu_passtrig25_n>0  && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > 0.0  && ph_noSIEIEiso1299_n == 2 && chIsoCorr_leadph12 > %f && chIsoCorr_sublph12 > %f && chIsoCorr_leadph12 < 12 && chIsoCorr_sublph12 < 12 && ph_passNeuIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[1] && phoIsoCorr_leadph12 > %f && phoIsoCorr_leadph12 < 9 && phoIsoCorr_sublph12 > %f && phoIsoCorr_sublph12 < 9  && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %d && pt_leadph12 < %d && sieie_leadph12 < %f && sieie_sublph12 < %f ' %( _chIso_cuts[etalead][0], _chIso_cuts[etasubl][0], _phoIso_cuts[etalead][0], _phoIso_cuts[etasubl][0], etalead, etasubl, ptmin, ptmax, _sieie_cuts[etalead][1], _sieie_cuts[etasubl][1] )
    #                    draw_var = 'sieie_sublph12:sieie_leadph12' # y:x
    #                elif var == 'chIsoCorr' :
    #                    draw_str_2d = 'mu_passtrig25_n>0  && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > 0.0  && ph_n==2 && sieie_leadph12 > %f && sieie_sublph12 > %f && ph_passNeuIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[1] && phoIsoCorr_leadph12 > %f && phoIsoCorr_sublph12 > %f && phoIsoCorr_leadph12 < 5 && phoIsoCorr_sublph12 < 5 && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %d && pt_leadph12 < %d && chIsoCorr_leadph12 < %f && chIsoCorr_sublph12 < %f ' %( _sieie_cuts[etalead][0], _sieie_cuts[etasubl][0], _phoIso_cuts[etalead][0], _phoIso_cuts[etasubl][0], etalead, etasubl, ptmin, ptmax, _chIso_cuts[etalead][1], _chIso_cuts[etasubl][1] )
    #                    draw_var = 'chIsoCorr_sublph12:chIsoCorr_leadph12' # y:x
    #                elif var == 'phoIsoCorr' :
    #                    draw_str_2d = 'mu_passtrig25_n>0  && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 && dr_ph1_ph2 > 0.4 && m_ph1_ph2 > 0.0  && ph_n==2 && sieie_leadph12 > %f && sieie_sublph12 > %f && ph_passNeuIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[1] && chIsoCorr_leadph12 > %f && chIsoCorr_sublph12 > %f && chIsoCorr_leadph12 < 10 && chIsoCorr_sublph12 < 10  && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %d && pt_leadph12 < %d && phoIsoCorr_leadph12 < %f && phoIsoCorr_sublph12 < %f ' %( _sieie_cuts[etalead][0], _sieie_cuts[etasubl][0], _chIso_cuts[etalead][0], _chIso_cuts[etasubl][0], etalead, etasubl, ptmin, ptmax, _phoIso_cuts[etalead][1], _phoIso_cuts[etasubl][1] )
    #                    draw_var = 'phoIsoCorr_sublph12:phoIsoCorr_leadph12' # y:x

    #                binning_2d = ( binning[var][etalead][0], binning[var][etalead][1], binning[var][etalead][2], binning[var][etasubl][0], binning[var][etasubl][1], binning[var][etasubl][2] )

    #                samplesLGG.create_hist( 'Muon', draw_var, draw_str_2d, binning_2d )
    #                newhist = samplesLGG.get_samples( name='Muon' )[0].hist.Clone( '%s_2DFakeFake_%s-%s_%d-%d' %( var, etalead, etasubl, ptmin, ptmax ) )

    #                all_hists.append(newhist)

    out_file = ROOT.TFile.Open( options.outputFile, 'RECREATE' )

    for hist in all_hists :
        hist.Write()

    out_file.Close()

    print '^_^ Finished ^_^'
     
main()
