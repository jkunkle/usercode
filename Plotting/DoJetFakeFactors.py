"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('--baseDir',      default=None,           dest='baseDir',         help='Path to base directory containing all ntuples')
p.add_argument('--baseDirModel',      default=None,           dest='baseDirModel', help='Path to base directory containing all ntuples for the model')
p.add_argument('--fileName',     default='ntuple.root',  dest='fileName',        help='( Default ntuple.root ) Name of files')
p.add_argument('--treeName',     default='events'     ,  dest='treeName',        help='( Default events ) Name tree in root file')
p.add_argument('--treeNameModel',     default='photons'     ,  dest='treeNameModel',help='( Default photons ) Name tree in root file')
p.add_argument('--samplesConf',  default=None,           dest='samplesConf',     help=('Use alternate sample configuration. '
                                                                                       'Must be a python file that implements the configuration '
                                                                                       'in the same manner as in the main() of this script.  If only '
                                                                                       'the file name is given it is assumed to be in the same directory '
                                                                                       'as this script, if a path is given, use that path' ) )

                                                                                       
p.add_argument('--xsFile',     default=None,  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--mcweight',     default=None,  type=float ,        dest='mcweight',         help='Weight to apply to MC samples')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--readHists',     default=False,action='store_true',   dest='readHists',         help='read histograms from root files instead of trees')

p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')

options = p.parse_args()

import sys
import os
import re
import math
import uuid
import copy
import imp
import ROOT
from array import array
import random

from SampleManager import SampleManager
from SampleManager import Sample

ROOT.gROOT.SetBatch(False)

samples = None

def main() :

    global samples

    if not options.baseDir.count('/eos/') and not os.path.isdir( options.baseDir ) :
        print 'baseDir not found!'
        return

    samples = SampleManager(options.baseDir, options.treeName, mcweight=options.mcweight, treeNameModel=options.treeNameModel, filename=options.fileName, base_path_model=options.baseDirModel, xsFile=options.xsFile, lumi=options.lumi, readHists=options.readHists, quiet=options.quiet)


    if options.samplesConf is not None :

        samples.ReadSamples( options.samplesConf )

        print 'Samples ready.\n'  

        print 'The draw syntax follows that of TTree.Draw.  Examples : '
        
        print 'samples.Draw(\'met_et\', \'EventWeight && passcut_ee==1\', \'(300, 0, 300)\'\n'

        print 'The first argument is a branch in the tree to draw'
        print 'The second argument is a set of cuts and/or weights to apply'
        print 'The third argument are the bin limits to use \n'

        print 'To see all available branches do ListBranches()'

    #cuts_den = '!ph_passChIsoCorrMedium[0] && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && ph_sigmaIEIE[0]>%f && ph_sigmaIEIE[0] < %f '
    #cuts_num = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && %s && ph_passSIEIEMedium[0] ' %(ec)

    cuts_den = 'ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && ph_sigmaIEIE[0]>%f && ph_sigmaIEIE[0] < %f '
    cuts_num = 'ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0]<20 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0] '

    sieie_cuts = { 'EB' : ( 0.013, 0.03 ), 'EE' : ( 0.035, 0.1 ) }
    eta_cuts = { 'EB' : 'ph_IsEB[0]', 'EE' : 'ph_IsEE[0]' }
    ptbins = [ 15, 20, 25, 30, 50, 80, 500 ]

    fake_factors = GetFakeFactors(cuts_den, cuts_num, sieie_cuts, eta_cuts, ptbins)

    for key, val in fake_factors.iteritems() :
        print 'Fake factors for %s' %key
        val.Draw()
        raw_input('continue')

    ApplySinglePhotonFF( cuts_den, sieie_cuts, eta_cuts, ptbins, fake_factors )

def ApplySinglePhotonFF( cut_str, cut_vals, eta_cuts, ptbins, fake_factors) :

    labels = cut_vals.keys()

    samp = samples.get_samples(name='Data')
    sampEval = samples.get_samples(name='WjetsZjets')

    for lab in labels :

        ec = eta_cuts[lab]
        vals = cut_vals[lab]

        cuts_den = cut_str%vals
        cuts_den += ' && ' + ec
                
        den_base = ' mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s ' %cuts_den

        #generate weighting string

        weight_str =  ''
        var = 'ph_pt[0]'
        for idx, min in enumerate(ptbins[:-1]) :
            max = ptbins[idx+1]
            ff = fake_factors[lab].GetBinContent( fake_factors[lab].FindBin( min ) )
            weight_str += ' %f * ( %s > %f && %s <= %f ) +' %( ff, var, min, var, max )

        weight_str = weight_str.rstrip(' ').rstrip('+')

        tot_str = ' ( %s ) * ( %s ) ' %( weight_str, den_base )

        print tot_str

        binning = ( 100, 0, 500 )

        ddhist   = None
        evalhist = None

        if samp:
            samples.create_hist( samp[0], var, tot_str , binning )

            ddhist = samp[0].hist.Clone('ddhist')

        if sampEval :

            samples.create_hist( sampEval[0], var, 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_passMedium[0] && %s)'%ec , binning )
            evalhist = sampEval[0].hist.Clone( 'evalHist' )

        evalhist.SetMarkerColor( ROOT.kRed )
        evalhist.SetLineColor( ROOT.kRed )


        ddhist.Draw()
        evalhist.Draw('same')
        raw_input('contin')


def GetFakeFactors(cut_den_base, cut_num_base, cut_vals, eta_cuts, ptbins) :

    labels = cut_vals.keys()
    binning = ( 500, 0, 500 )

    den_sample = 'DataRealPhotonZgSub'
    samp = samples.get_samples(name=den_sample)

    output = {}

    for lab in labels :
        output[lab] = ROOT.TH1F( 'ff_%s'%lab, 'ff_%s'%lab, binning[0], binning[1], binning[2] )

    for lab in labels :

        ec = eta_cuts[lab]
        vals = cut_vals[lab]

        cuts_den = cut_den_base%vals
        cuts_den += ' && ' + ec
                
        cuts_num = cut_num_base
        cuts_num += ' && ' + ec

        full_den_cuts = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %cuts_den
        full_num_cuts = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %cuts_num


        #generate histograms
        den_hist = None
        num_hist = None

        var = 'ph_pt[0]'
        if samp:
            samples.create_hist( samp[0], var, full_den_cuts, binning )
            den_hist = samp[0].hist.Clone( 'den_hist' )
            samples.create_hist( samp[0], var, full_num_cuts, binning )
            num_hist = samp[0].hist.Clone( 'num_hist' )


        for idx, min in enumerate( ptbins[0:-1] ) :

            max = ptbins[idx+1]
            num_count = num_hist.Integral( num_hist.FindBin( min), num_hist.FindBin(max ) )
            den_count = den_hist.Integral( den_hist.FindBin( min), den_hist.FindBin(max ) )

            factor = num_count/den_count

            for bin in range( 1, output[lab].GetNbinsX()+1 ) :
                if output[lab].GetBinCenter( bin ) > min and output[lab].GetBinCenter( bin) < max :
                    output[lab].SetBinContent(bin, factor )


            print 'Pt bins %f - %f, N num = %f, N den = %f, fake factor = %f ' %( min, max, num_count, den_count, factor )

    return output



main() 
