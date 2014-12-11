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

samplesFF = None
samplesData = None

def main() :

    global samplesFF
    global samplesData

    if not options.baseDir.count('/eos/') and not os.path.isdir( options.baseDir ) :
        print 'baseDir not found!'
        return

    samplesFF = SampleManager(options.baseDir, options.treeName, mcweight=options.mcweight, treeNameModel=options.treeNameModel, filename=options.fileName, base_path_model=options.baseDirModel, xsFile=options.xsFile, lumi=options.lumi, readHists=options.readHists, quiet=options.quiet)

    base_dir_data      = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhID_2014_10_29'

    samplesData = SampleManager(base_dir_data, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)


    if options.samplesConf is not None :

        samplesFF.ReadSamples( options.samplesConf )
        samplesData.ReadSamples( options.samplesConf )

    #cuts_den = '!ph_passChIsoCorrMedium[0] && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0]  && ph_sigmaIEIE[0]>%f && ph_sigmaIEIE[0] < %f '
    #cuts_num = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && %s && ph_passSIEIEMedium[0] ' %(ec)

    loose_cuts = (12, 9, 9)
    #loose_cuts = (20, 15, 15)
    #loose_cuts = (1000000,1000000,1000000)

    cuts_den = 'ph_hasPixSeed[0]==0 && !ph_passNeuIsoCorrMedium[0] && !ph_passPhoIsoCorrMedium[0] && !ph_passSIEIEMedium[0] && !ph_passChIsoCorrMedium[0] && ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d ' %(loose_cuts[0], loose_cuts[1], loose_cuts[2] )
    cuts_num = 'ph_hasPixSeed[0]==0 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passSIEIEMedium[0] && ph_passChIsoCorrMedium[0] && ph_HoverE12[0] < 0.05'

    regions = ['EB', 'EE']
    ptbins = [ 15, 25, 40, 70, 1000000 ]

    fake_factors = GetFakeFactors(cuts_den, cuts_num, regions, ptbins)

    #for key, val in fake_factors.iteritems() :
    #    print 'Fake factors for %s' %key
    #    val.Draw()
    #    raw_input('continue')

    #ApplySinglePhotonFF( cuts_den, sieie_cuts, eta_cuts, ptbins, fake_factors )

    gg_regions = [ ('EB', 'EB') ]

    ApplyDiPhotonFF( loose_cuts, gg_regions, ptbins, fake_factors ) 

def ApplyDiPhotonFF( loose_cuts, regions,  ptbins, fake_factors) :

    draw_cmd_base = 'mu_passtrig25_n>0 && mu_n==1 && ph_n > 1 && dr_ph1_ph2 > 0.3 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0  '

    samp = samplesData.get_samples(name='Muon')


    for r1,r2 in regions  :

        draw_cmd = draw_cmd_base + ' && is%s_leadph12 && is%s_sublph12' %( r1,r2)

        draw_cmd_LL = '%s && chIsoCorr_leadph12 > 1.5 && neuIsoCorr_leadph12 > 1.0 && phoIsoCorr_leadph12 > 0.7 && chIsoCorr_sublph12 > 1.5 && neuIsoCorr_sublph12 > 1.0 && phoIsoCorr_sublph12 > 0.7 && chIsoCorr_leadph12 < %d && neuIsoCorr_leadph12 < %d && phoIsoCorr_leadph12 < %d && chIsoCorr_sublph12 < %d && neuIsoCorr_sublph12 < %d && phoIsoCorr_sublph12 < %d && sieie_leadph12 > 0.011 && sieie_sublph12 > 0.011' %(draw_cmd, loose_cuts[0], loose_cuts[1], loose_cuts[2], loose_cuts[0], loose_cuts[1], loose_cuts[2]) 
        draw_cmd_TL = '%s && chIsoCorr_leadph12 < 1.5 && neuIsoCorr_leadph12 < 1.0 && phoIsoCorr_leadph12 < 0.7 && chIsoCorr_sublph12 > 1.5 && neuIsoCorr_sublph12 > 1.0 && phoIsoCorr_sublph12 > 0.7 && chIsoCorr_sublph12 < %d && neuIsoCorr_sublph12 < %d && phoIsoCorr_sublph12 < %d && sieie_leadph12 < 0.011 && sieie_sublph12 > 0.011' %(draw_cmd, loose_cuts[0], loose_cuts[1], loose_cuts[2]) 
        draw_cmd_LT = '%s && chIsoCorr_leadph12 > 1.5 && neuIsoCorr_leadph12 > 1.0 && phoIsoCorr_leadph12 > 0.7 && chIsoCorr_sublph12 < 1.5 && neuIsoCorr_sublph12 < 1.0 && phoIsoCorr_sublph12 < 0.7 && chIsoCorr_leadph12 < %d && neuIsoCorr_leadph12 < %d && phoIsoCorr_leadph12 < %d && sieie_leadph12 > 0.011 && sieie_sublph12 < 0.011' %(draw_cmd, loose_cuts[0], loose_cuts[1], loose_cuts[2]) 

        var = 'pt_leadph12'

        samplesData.create_hist( samp[0], var, draw_cmd_LL, (100, 0, 500 ) )
        LL_hist = samp[0].hist.Clone( 'll_hist' )

        samplesData.create_hist( samp[0], var, draw_cmd_TL, (100, 0, 500 ) )
        TL_hist = samp[0].hist.Clone( 'tl_hist' )

        samplesData.create_hist( samp[0], var, draw_cmd_LT, (100, 0, 500 ) )
        LT_hist = samp[0].hist.Clone( 'lt_hist' )

        for idx, min in enumerate( ptbins[0:-1] ) :

            max = ptbins[idx+1]

            bin_lead = ( r1, min, max )
            bin_subl = ( r2, 15, max )

            LL_count = LL_hist.Integral( LL_hist.FindBin( min ), LL_hist.FindBin( max ) - 1 )
            LT_count = LT_hist.Integral( LT_hist.FindBin( min ), LT_hist.FindBin( max ) - 1 )
            TL_count = TL_hist.Integral( TL_hist.FindBin( min ), TL_hist.FindBin( max ) - 1 )

            ff_lead = fake_factors[bin_lead]
            ff_subl = fake_factors[bin_subl]

            N_FF_TL = LL_count*ff_lead
            N_FF_LT = LL_count*ff_subl

            N_RF_TL = TL_count - N_FF_TL
            N_FR_LT = LT_count - N_FF_LT

            N_RF_TT = N_RF_TL*ff_subl
            N_FR_TT = N_FR_LT*ff_lead
            N_FF_TT = LL_count*ff_lead*ff_subl

            print 'Lead pt = %d - %d, subl pt = %d - %d' %( min, max, 15, max )

            print 'N_LL = ', LL_count
            print 'N_LT = ', LT_count
            print 'N_TL = ', TL_count

            print 'N_FF_TL = ', N_FF_TL
            print 'N_FF_LT = ', N_FF_LT

            print 'N_RF_TL = ', N_RF_TL
            print 'N_FR_LT = ', N_FR_LT

            print 'N_RF_TT = ', N_RF_TT
            print 'N_FR_TT = ', N_FR_TT
            print 'N_FF_TT = ', N_FF_TT

            print 'Sum = ', (N_RF_TT+N_FR_TT+N_FF_TT)





        

def ApplySinglePhotonFF( cut_str, cut_vals, eta_cuts, ptbins, fake_factors) :

    labels = cut_vals.keys()

    samp = samplesData.get_samples(name='Data')
    sampEval = samplesData.get_samples(name='WjetsZjets')

    for lab in labels :

        ec = eta_cuts[lab]
        vals = cut_vals[lab]

        cuts_den = cut_str%vals
        cuts_den += ' && ' + ec
                
        den_base = ' mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s ' %cuts_den

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

            samples.create_hist( sampEval[0], var, 'PUWeight * ( mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_passMedium[0] && %s)'%ec , binning )
            evalhist = sampEval[0].hist.Clone( 'evalHist' )

        evalhist.SetMarkerColor( ROOT.kRed )
        evalhist.SetLineColor( ROOT.kRed )


        ddhist.Draw()
        evalhist.Draw('same')
        raw_input('contin')


def GetFakeFactors(cut_den_base, cut_num_base, regions, ptbins) :

    binning = ( 500, 0, 500 )

    den_sample = 'MuonRealPhotonZgSub'
    samp = samplesFF.get_samples(name=den_sample)

    fake_factors = {}

    output = {}


    for reg in regions :

        cuts_den = cut_den_base
        cuts_den += ' && ph_Is%s[0]' %reg
                
        cuts_num = cut_num_base
        cuts_num += ' && ph_Is%s[0]' %reg

        full_den_cuts = ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %cuts_den
        full_num_cuts = ' mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && %s && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %cuts_num
        
        #generate histograms
        den_hist = None
        num_hist = None

        var = 'ph_pt[0]'
        if samp:
            samplesFF.create_hist( samp[0], var, full_den_cuts, binning )
            den_hist = samp[0].hist.Clone( 'den_hist' )
            samplesFF.create_hist( samp[0], var, full_num_cuts, binning )
            num_hist = samp[0].hist.Clone( 'num_hist' )


        for idx, min in enumerate( ptbins[0:-1] ) :

            max = ptbins[idx+1]

            bin = ( reg, min, max )

            num_count = num_hist.Integral( num_hist.FindBin( min), num_hist.FindBin(max ) - 1 )
            den_count = den_hist.Integral( den_hist.FindBin( min), den_hist.FindBin(max ) - 1 )

            factor = num_count/den_count

            print 'Pt bins %f - %f, N num = %f, N den = %f, fake factor = %f ' %( min, max, num_count, den_count, factor )

            output[bin] = factor

        for idx, max in enumerate( ptbins[1:] ) :

            bin = (reg, 15, max )

            if bin in output :
                continue

            num_count = num_hist.Integral( num_hist.FindBin( 15), num_hist.FindBin(max ) - 1 )
            den_count = den_hist.Integral( den_hist.FindBin( 15), den_hist.FindBin(max ) - 1 )

            factor = num_count/den_count

            output[bin] = factor


    return output



main() 
