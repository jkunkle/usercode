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

    baseDirLLG = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_07_30'
    baseDirLG = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2015_07_30'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfLLG = 'Modules/ZJetsTemplates.py'

    samplesLLG     = SampleManager(baseDirLLG , treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesLG     = SampleManager(baseDirLG , treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesLLG    .ReadSamples( sampleConfLLG )
    samplesLG    .ReadSamples( sampleConfLLG )

    ROOT.gROOT.SetBatch(True)

    binning = { 'EB' : ( 30, 0, 0.03 ), 'EE' : ( 30, 0, 0.09 ) }

    pt_bins = [(15, 25), (25,40), (40,70), (70,1000000)]

    _sieie_cuts  = { 'EB' : (0.011,0.029), 'EE' : (0.033, 0.087) }
    _chIso_cuts  = { 'EB' : (1.5, 19.5)  , 'EE' : (1.2,20.4) }
    _neuIso_cuts = { 'EB' : (1.0,20)     , 'EE' : (1.5,20.5) }
    _phoIso_cuts = { 'EB' : (0.7,20.3)   , 'EE' : (1.0,20) }

    all_hists = []

    for eta in ['EB', 'EE'] :
        for ptmin, ptmax in pt_bins :

            samplesLLG.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoSIEIE_n==1 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_sigmaIEIE[0] < %f ) ' %( ptmin, ptmax, eta, _sieie_cuts[eta][1] ), binning[eta] )


            hist_data = samplesLLG.get_samples( name='Muon' )[0]
            hist_bkg = samplesLLG.get_samples( name='RealPhotonsZg' )[0]

            hist_subtracted = hist_data.hist.Clone( 'Subtracted_%s_%d-%d' %( eta, ptmin, ptmax ))

            hist_subtracted.Add( hist_bkg.hist, -1 )

            all_hists.append( hist_data.hist.Clone( 'Data_%s_%d-%d' %( eta, ptmin, ptmax ) ) )
            all_hists.append( hist_bkg.hist.Clone( 'Zg_%s_%d-%d' %( eta, ptmin, ptmax ) ) )
            all_hists.append( hist_subtracted)

            samplesLG.create_hist( 'Wg', 'ph_sigmaIEIE[0]', 'mu_passtrig25_n>0 && mu_n==1 && ph_mediumNoSIEIE_n==1 && ph_HoverE12[0] < 0.05 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25  && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] && ph_sigmaIEIE[0] < %f ' %(ptmin, ptmax,eta,  _sieie_cuts[eta][1]) , binning[eta],)

            newhist = samplesLG.get_samples( name='Wg' )[0].hist.Clone( 'Wg_%s_%d-%d' %( eta, ptmin, ptmax ) )

            all_hists.append(newhist)

    out_file = ROOT.TFile.Open( options.outputFile, 'RECREATE' )

    for hist in all_hists :
        hist.Write()

    out_file.Close()

    print '^_^ Finished ^_^'
     
main()
