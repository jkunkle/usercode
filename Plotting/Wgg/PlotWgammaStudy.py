
from SampleManager import SampleManager
from argparse import ArgumentParser
import os
import math
import uuid
from uncertainties import ufloat

p = ArgumentParser()

                                                                                       
p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',         help='base directory for histograms')


options = p.parse_args()


import ROOT

def main() :

    global samples
    sampleConf = 'Modules/StudyWgammaFinal.py'

    samples = SampleManager(options.baseDir, filename='hist.root', readHists=True)

    for dirname in os.listdir( options.baseDir ) :
        if os.path.isdir( '%s/%s' %( options.baseDir, dirname ) ) :
            samples.AddSample( dirname, path=dirname )

    sample_list = samples.get_samples()

    sample_pairs = []

    for s in sample_list :
        if s.name.count('chIsoCorr') :

            samp_sieie = s.name.replace( 'chIsoCorr', 'sigmaIEIE' )

            sample_pairs.append( ( s.name, samp_sieie ) ) 

    output_dir = options.baseDir
    #output_dir = None

    MakeRatioComparisons( sample_pairs, ['elz_sb_fine_medium_CutMet0', 'elz_sb_fine_tight_CutMet0', 'elz_sb_two_tight_CutMet0'], ['Medium range', 'Tight range', 'Two bin fit'], output_dir, name_postfix = 'comp_elz_fitmethods' )
    MakeRatioComparisons( sample_pairs, ['muz_sb_fine_medium_CutMet0', 'muz_sb_fine_tight_CutMet0', 'muz_sb_two_tight_CutMet0'], ['Medium range', 'Tight range', 'Two bin fit'], output_dir,name_postfix = 'comp_muz_fitmethods' )

    MakeRatioComparisons( sample_pairs, ['mu_cr_fine_medium_CutMet0', 'mu_cr_fine_tight_CutMet0', 'mu_cr_two_medium_CutMet0'], ['Medium range', 'Tight range', 'Two bin fit'], output_dir, name_postfix='comp_mu_fitmethods' )
    MakeRatioComparisons( sample_pairs, ['el_cr_fine_medium_CutMet0', 'el_cr_fine_tight_CutMet0', 'el_cr_two_medium_CutMet0'], ['Medium range', 'Tight range', 'Two bin fit'], output_dir, name_postfix='comp_el_fitmethods' )
    MakeRatioComparisons( sample_pairs, ['mu_cr_fine_tight_CutMet0', 'mu_sb_fine_tight_CutMet0', ], ['Control region template', 'Sideband template'], output_dir, name_postfix='comp_mu_faketemplates' )
    MakeRatioComparisons( sample_pairs, ['el_cr_fine_tight_CutMet0', 'el_sb_fine_tight_CutMet0', ], ['Control region template', 'Sideband template'], output_dir, name_postfix='comp_el_faketemplates' )

    MakeRatioComparisons( sample_pairs, ['mu_cr_two_tight_CutMet0', 'mu_sb_two_tight_CutMet0', ], ['Control region template', 'Sideband template'], output_dir, name_postfix='comp_mu_twobin_faketemplates' )
    MakeRatioComparisons( sample_pairs, ['el_cr_two_tight_CutMet0', 'el_sb_two_tight_CutMet0', ], ['Control region template', 'Sideband template'], output_dir, name_postfix='comp_el_twobin_faketemplates' )

    MakeComparison( sample_pairs, 'muz_sb_fine_tight_CutMet0', output_dir=output_dir )
    MakeComparison( sample_pairs, 'mu_sb_fine_tight_CutMet0', output_dir=output_dir )

def MakeRatioComparisons( sample_pairs, comp_list, legend_list, output_dir=None, name_postfix='' ) :

    samples.clear_all()
    for sample in samples.samples :
        samples.get_hist( sample, 'pthist_EB' )

    name_postfix_eb = name_postfix + '_EB'

    make_ratio_comparison( sample_pairs, comp_list, legend_list, output_dir, name_postfix_eb ) 

    samples.clear_all()
    for sample in samples.samples :
        samples.get_hist( sample, 'pthist_EE' )

    name_postfix_ee = name_postfix + '_EE'

    make_ratio_comparison( sample_pairs, comp_list, legend_list, output_dir, name_postfix_ee ) 

def make_ratio_comparison( sample_pairs, comp_list, legend_list, output_dir=None, name_postfix='' ) :

    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen ]

    can = ROOT.TCanvas( str( uuid.uuid4() ), '' )

    ratios = []

    for sel in comp_list :
        for pair in sample_pairs :

            if not pair[0].count( sel ) :
                continue

            hist_chIso = samples.get_samples( name=pair[0] )[0].hist
            hist_sieie = samples.get_samples( name=pair[1] )[0].hist

            hist_ratio = hist_chIso.Clone( '%s_ratio' %pair[0] )
            for binn in range( 1, hist_ratio.GetNbinsX() +1 ) :
                val_chIso = hist_chIso.GetBinContent( binn )
                err_chIso = hist_chIso.GetBinError( binn )
                val_sieie = hist_sieie.GetBinContent( binn )
                err_sieie = hist_sieie.GetBinError( binn )

                chIso = ufloat( val_chIso, err_chIso )
                sieie = ufloat( val_sieie, err_sieie )

                fracdiff = (chIso - sieie ) / chIso 

                hist_ratio.SetBinContent( binn, math.fabs( fracdiff.n ) )
                hist_ratio.SetBinError( binn, fracdiff.s )

            ratios.append(hist_ratio)


    for idx, rat in enumerate(ratios) :

        rat.SetMarkerColor( colors[idx] )
        rat.SetLineColor( colors[idx] )
        rat.SetMarkerStyle( 20 )
        rat.SetMarkerSize( 1.2 )
        rat.SetStats( 0 )
        rat.SetMinimum( -0.5 )
        rat.SetMaximum( 1.5 )
        rat.GetXaxis().SetTitle( 'photon pT [GeV]' )
        rat.GetYaxis().SetTitle( '% diff using #sigmai#etai#eta to using chHadIso' )

        if idx == 0 :
            rat.Draw()
        else :
            rat.Draw('same')

    leg = ROOT.TLegend( 0.6, 0.6, 0.9, 0.9 )
    leg.SetBorderSize( 0 )
    leg.SetFillColor( ROOT.kWhite )

    for idx, rat in enumerate(ratios) :

        leg.AddEntry( rat, legend_list[idx], 'LPE' )

    leg.Draw()

    if output_dir is not None :
        can.SaveAs( '%s/%s.pdf' %( output_dir, name_postfix) )
    else :
        raw_input('cont')
    


def MakeComparison( sample_pairs, comp_list, output_dir=None ) :

    if not isinstance( comp_list, list ) :
        comp_list = [comp_list]

    samples.clear_all()
    for sample in samples.samples :
        samples.get_hist( sample, 'pthist_EB' )

    name_postfix = '_EB'

    make_comparison( sample_pairs, comp_list, output_dir, name_postfix ) 

    samples.clear_all()
    for sample in samples.samples :
        samples.get_hist( sample, 'pthist_EE' )

    name_postfix = '_EE'
    make_comparison( sample_pairs, comp_list, output_dir, name_postfix ) 


def make_comparison( sample_pairs, comp_list, output_dir=None, name_postfix='' ) :

    markers = [20, 21, 22, 23, 24]

    varnames = ['chIsoCorr', 'sigmaIEIE']

    colors = [ROOT.kBlack, ROOT.kRed]

    comp_samples = []

    for comp in comp_list :

        for samps in sample_pairs :

            if samps[0].count( comp ) :
                comp_samples.append( samps[0] )
                comp_samples.append( samps[1] )
                 
    can = ROOT.TCanvas( str( uuid.uuid4() ), '' )

    first_bin_max = 0

    all_hists = []
    for idx, samp in enumerate(comp_samples) :


        midx = idx / 2
        cidx = idx % 2

        hist = samples.get_samples( name=samp )[0].hist

        all_hists.append(hist)

        first_bin = hist.GetBinContent(1)

        if first_bin > first_bin_max :
            first_bin_max = first_bin

        hist.SetMarkerColor( colors[cidx] )
        hist.SetLineColor( colors[cidx] )
        hist.SetMarkerStyle( markers[midx] )
        hist.SetMarkerSize( 1.2 ) 
        hist.SetStats( 0 )
        hist.GetXaxis().SetTitle( 'photon pT [GeV]' )
        hist.GetYaxis().SetTitle( 'Estimated background' )

        if idx == 0 :
            hist.Draw()
        else :
            hist.Draw( 'same' )

    for hist in all_hists :
        hist.SetMinimum( 0 )
        hist.SetMaximum( first_bin_max * 1.4 )

    leg = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
    leg.SetBorderSize(0)
    leg.SetFillColor( ROOT.kWhite )

    for idx, hist in enumerate(all_hists) :

        leg.AddEntry( hist, varnames[idx], 'LPE' )

    leg.Draw()


    if output_dir is not None :
        can.SaveAs( '%s/%s/comparison%s.pdf' %(output_dir, comp_samples[0], name_postfix) )
    else :
        raw_input("cont")
    

main()
