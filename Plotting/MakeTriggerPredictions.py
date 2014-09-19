"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

                                                                                       
p.add_argument('--xsFile',     default=None,  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')

p.add_argument('--save'        , default=False, action='store_true',   dest='save'        , help='save plots ( must provide outputDir )')
p.add_argument('--detailLevel' , default=100, type=int, dest='detailLevel'      , help='make only plots at this detail level (make all plots by default)')
p.add_argument('--makeAll'     , default=False, action='store_true',   dest='makeAll'     , help='make all plots')
p.add_argument('--makeEvent'   , default=False, action='store_true',   dest='makeEvent'   , help='make Wgg event plots')
p.add_argument('--makeMva'     , default=False, action='store_true',   dest='makeMva'     , help='make electron veto mva plots')
p.add_argument('--makeEleVeto' , default=False, action='store_true',   dest='makeEleVeto' , help='make electron veto comparison plots')
p.add_argument('--makeEleFake' , default=False, action='store_true',   dest='makeEleFake' , help='make electron fake factor plots')
p.add_argument('--makePhComp'  , default=False, action='store_true',   dest='makePhComp'  , help='make photon ID vars comparison plots')
p.add_argument('--makeJetFakeTemplate' , default=False, action='store_true',   dest='makeJetFakeTemplate' , help='make jet fake plots, template method')
p.add_argument('--makeJetFakeFactor' , default=False, action='store_true',   dest='makeJetFakeFactor' , help='make jet fake plots, fake factor method')

options = p.parse_args()

import sys
import os
import re
import math
import uuid
import copy
import imp
import collections
import ROOT

from SampleManager import SampleManager
from SampleManager import DrawConfig

ROOT.gROOT.SetBatch(False)

samples = None

def main() :

    global samples

    baseDir  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/SingleLepton_2014_09_03/'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConf  = 'Modules/Wgamgam.py'

    samples  = SampleManager(baseDir , treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)

    samples .ReadSamples( sampleConf )

    #if options.save :
    #    ROOT.gROOT.SetBatch(True)

    MakePredictions( save=False )
#---------------------------------------
# User functions
#---------------------------------------

#---------------------------------------
def MakePredictions( save=False) :

    #W_e_xs = 20000
    Wxs_13tev = 2e5
    wbr = 0.1
    ele_eff  =0.8
    W_e_xs = Wxs_13tev*wbr*ele_eff

    config_inc    = DrawConfig( 'el_pt[0]', 'el_n==1 && el_truthMatch_el[0] ', (500, 0, 500 ) )
    config_lowpt  = DrawConfig( 'el_pt[0]', 'el_n==1 && el_truthMatch_el[0] && trueW_pt[0]<30', (500, 0, 500 ) )
    config_highpt = DrawConfig( 'el_pt[0]', 'el_n==1 && el_truthMatch_el[0] && trueW_pt[0]>30', (500, 0, 500 ) )
    config_nojet  = DrawConfig( 'el_pt[0]', 'el_n==1 && el_truthMatch_el[0] && jet_n==0', (500, 0, 500 ) )
    config_jets   = DrawConfig( 'el_pt[0]', 'el_n==1 && el_truthMatch_el[0] && jet_n>0 ', (500, 0, 500 ) )
    #config = DrawConfig( 'trueW_pt', 'el_n==1 && el_truthMatch_el[0] ', (500, 0, 500) )
    
    hist_inc    = clone_sample_and_draw( '_Wjets', config_inc    )
    hist_lowpt  = clone_sample_and_draw( '_Wjets', config_lowpt  )
    hist_highpt = clone_sample_and_draw( '_Wjets', config_highpt )
    hist_nojet  = clone_sample_and_draw( '_Wjets', config_nojet  )
    hist_jets   = clone_sample_and_draw( '_Wjets', config_jets   )

    eff_lowpt  = hist_lowpt .Integral()/hist_inc.Integral()
    eff_highpt = hist_highpt.Integral()/hist_inc.Integral()
    eff_nojet  = hist_nojet .Integral()/hist_inc.Integral()
    eff_jets   = hist_jets  .Integral()/hist_inc.Integral()

    print 'INC'
    make_funcs_and_draw( hist_inc   , W_e_xs, outputDir=options.outputDir, name_postfix='' )
    print 'LOWPT'
    make_funcs_and_draw( hist_lowpt , W_e_xs*eff_lowpt, outputDir=options.outputDir, name_postfix='_lowpt'  )
    print 'HIGHPT'
    make_funcs_and_draw( hist_highpt, W_e_xs*eff_highpt, outputDir=options.outputDir, name_postfix='_highpt' )
    print 'NOJET'
    make_funcs_and_draw( hist_nojet , W_e_xs*eff_nojet, outputDir=options.outputDir, name_postfix='_nojet'  )
    print 'JETS'
    make_funcs_and_draw( hist_jets  , W_e_xs*eff_jets, outputDir=options.outputDir, name_postfix='_jets'    )

def make_funcs_and_draw( hist, W_e_xs, outputDir=None, name_postfix='' ) :

    min_cut = [15         , 20       , 25         , 30          , 35            , 40          , 45            ]
    colors  = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue , ROOT.kGreen , ROOT.kMagenta , ROOT.kOrange, ROOT.kYellow+3] 

    efficiencies =  collections.OrderedDict()
    for cut in min_cut :
        min_bin = hist.FindBin( cut ) +1
        efficiencies[cut] = hist.Integral( min_bin, hist.GetNbinsX() )/hist.Integral()
    print efficiencies

    funcs_inv = collections.OrderedDict()
    for (cut, pteff), color in zip(efficiencies.iteritems(), colors) :
        funcs_inv[cut] = ROOT.TF1( 'funcinv_%d' %cut, 'x/([0]*[1])', 0, 100000 )
        funcs_inv[cut].SetParameter(0, W_e_xs)
        funcs_inv[cut].SetParameter(1, pteff)
        funcs_inv[cut].SetLineColor(color)
    #lumi_max = funcs_inv[min_cut[0]].Eval( 50000 )
    lumi_max = 1000

    funcs = collections.OrderedDict()
    for (cut, pteff), color in zip(efficiencies.iteritems(), colors) :
        funcs[cut] = ROOT.TF1( 'func_%d' %cut, 'x*[0]*[1]', 0, lumi_max )
        funcs[cut].SetParameter(0, W_e_xs)
        funcs[cut].SetParameter(1, pteff)
        funcs[cut].SetLineColor(color)
        funcs[cut].SetTitle()
        funcs[cut].GetYaxis().SetTitle( 'N recorded W#rightarrow e#nu' )
        funcs[cut].GetXaxis().SetTitle( 'Integrated Lumi (pb^{-1})' )
        funcs[cut].GetXaxis().SetTitleSize( 0.05 )
        funcs[cut].GetYaxis().SetTitleSize( 0.05 )
        funcs[cut].GetXaxis().SetLabelSize( 0.05 )
        funcs[cut].GetYaxis().SetLabelSize( 0.05 )
        funcs[cut].GetYaxis().SetTitleOffset( 1.4 )

        funcs_inv[cut] = ROOT.TF1( 'funcinv_%d' %cut, 'x/([0]*[1])', 0, 20000 )
        funcs_inv[cut].SetParameter(0, W_e_xs)
        funcs_inv[cut].SetParameter(1, pteff)
        funcs_inv[cut].SetLineColor(color)


    latex_lines = []
    latex_lines.append( r'\begin{tabular}{| l | c | c | c |} \hline' )
    latex_lines.append( r'Offline $p_{T}$ cut & \multicolumn{3}{|c|}{ Int Lumi. giving X events ($pb^{-1}$)} \\ \hline' )
    latex_lines.append( r' &  10k  &  20k  & 50k \\ \hline ' )
    
    for cut, func in funcs_inv.iteritems() :
        latex_lines.append( ' %d GeV & %.2f & %.2f & %.2f ' %( cut, func.Eval(10000), func.Eval(20000), func.Eval(50000) ) + r'\\' )
        print 'Cut val = %d, 10000 = %f, 20000 = %f' %( cut, func.Eval(10000), func.Eval(20000) )

    latex_lines[-1] = latex_lines[-1] + ' \hline '
    latex_lines.append('\end{tabular}' )

    print '\n'.join(latex_lines)

    can = ROOT.TCanvas('can', '' )
    can.SetLeftMargin(0.15)
    can.SetBottomMargin(0.15)
    first = True
    for cut, func in funcs.iteritems() :
        draw_cmd = ''
        if not first :
            draw_cmd += 'same'
        func.Draw( draw_cmd )

        first = False

    line = ROOT.TLine( 0, 10000, lumi_max, 10000 )
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()

    line2 = ROOT.TLine( 0, 20000, lumi_max, 20000 )
    line2.SetLineStyle(2)
    line2.SetLineWidth(2)
    line2.Draw()

    samples.legendLoc = 'TopLeft'
    leg = samples.create_standard_legend( len( min_cut ) ) 

    for cut, func in funcs.iteritems() :
        leg.AddEntry( func, 'Offline p_{T} > %d' %cut, 'L')

    leg.Draw()

    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

        can.SaveAs( outputDir + '/event_vs_lumi%s.pdf'%name_postfix )
        lfile = open( outputDir + '/event_vs_lumi%s.tex' %name_postfix, 'w' )
        lfile.write('\n'.join(latex_lines))
        lfile.close()

    else :
        raw_input('cont')






def clone_sample_and_draw( samp, draw_config ) :
        newSamp = samples.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
        samples.create_hist_new( draw_config, newSamp )
        return newSamp.hist



    





main()
