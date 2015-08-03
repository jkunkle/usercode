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

    baseDirLLG = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_07_16'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfLLG = 'Modules/ZJetsTemplates.py'

    samplesLLG     = SampleManager(baseDirLLG , treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesLLG    .ReadSamples( sampleConfLLG )

    ROOT.gROOT.SetBatch(True)

    binning = { 'EB' : ( 30, 0, 0.03 ), 'EE' : ( 30, 0, 0.09 ) }

    pt_bins = [(15, 25), (25,40), (40,70), (70,1000000)]


    all_hists = []

    for eta in ['EB', 'EE'] :
        for ptmin, ptmax in pt_bins :

            samplesLLG.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoSIEIE_n==1 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_pt[0] > %d && ph_pt[0] < %d && ph_Is%s[0] ) ' %( ptmin, ptmax, eta ), binning[eta] )


            hist_data = samplesLLG.get_samples( name='Muon' )[0]
            hist_bkg = samplesLLG.get_samples( name='RealPhotonsZg' )[0]

            hist_subtracted = hist_data.hist.Clone( 'Subtracted_%s_%d-%d' %( eta, ptmin, ptmax ))

            hist_subtracted.Add( hist_bkg.hist, -1 )

            all_hists.append( hist_data.hist.Clone( 'Data_%s_%d-%d' %( eta, ptmin, ptmax ) ) )
            all_hists.append( hist_bkg.hist.Clone( 'Zg_%s_%d-%d' %( eta, ptmin, ptmax ) ) )
            all_hists.append( hist_subtracted)


    out_file = ROOT.TFile.Open( options.outputFile, 'RECREATE' )

    for hist in all_hists :
        hist.Write()

    out_file.Close()

    print '^_^ Finished ^_^'
     
main()
