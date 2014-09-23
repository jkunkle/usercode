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
import pickle
import imp
import ROOT
from array import array
from uncertainties import ufloat

from SampleManager import SampleManager

ROOT.gROOT.SetBatch(False)

samplesWgg = None

ph_cuts = ''
lead_dr_cut = 0.4
subl_dr_cut = 0.4
phot_dr_cut = 0.3


invPixLead_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2  && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0 && ph_phDR>0.3 && leadPhot_leadLepDR>%.1f && sublPhot_leadLepDR>%.1f && mu_n==0 && m_phph>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixSubl_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2  && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1 && ph_phDR>0.3 && leadPhot_leadLepDR>%.1f && sublPhot_leadLepDR>%.1f && mu_n==0 && m_phph>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixLead_zrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixSubl_zrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1  && !(fabs(m_lepphph-91.2) < 5) && !(fabs(m_lepph1-91.2) < 5)  && !(fabs(m_lepph2-91.2) < 5) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixLead_invzrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==1 && ph_hasPixSeed[1]==0  && ( (fabs(m_lepphph-91.2) < 5) || (fabs(m_lepph1-91.2) < 5) || (fabs(m_lepph2-91.2) < 5) ) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts)
invPixSubl_invzrej_cuts_egg = ' el_passtrig_n>0 && el_n==1 && ph_n==2 && ph_phDR>0.3 && leadPhot_leadLepDR>%f && sublPhot_leadLepDR>%f && mu_n==0 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==1  && ( (fabs(m_lepphph-91.2) < 5) || (fabs(m_lepph1-91.2) < 5)  || (fabs(m_lepph2-91.2) < 5) ) && m_phph>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts)

def main() :

    global samplesWgg

    baseDirWgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNom_2014_06_16/'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfWgg = 'Modules/Wgamgam.py'

    samplesWgg = SampleManager(baseDirWgg, treename, filename=filename, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)

    samplesWgg.ReadSamples( sampleConfWgg )

    if options.save :
        ROOT.gROOT.SetBatch(True)

    base_dir_ele = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_08_28'
    base_dir_jet = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_09_09/JetFakeResultsSyst'
    outputDir='/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_09_09/BackgroundEstimates'
    MakeEleBkgEstimate( base_dir_ele, base_dir_jet, outputDir )

    MakeJetBkgEstimate( base_dir_jet, outputDir ) 

def MakeJetBkgEstimate( base_dir_jet, outputDir=None ) :

    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB'), ('EE', 'EE')]
    pt_bins = [ 15, 25, 40, 80, 1000000 ]

    file_key_mu = 'results__mu__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_elfull = 'results__elfull__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_el = 'results__el__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'

    file_key_mu_syst     = 'results__syst__mu__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_elfull_syst = 'results__syst__elfull__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_el_syst     = 'results__syst__el__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'

    jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    jet_files_mu     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu     )
    jet_files_elfull = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull )
    jet_files_el     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_el     )

    jet_files_mu_syst     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu_syst     )
    jet_files_elfull_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull_syst )
    jet_files_el_syst     = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_el_syst     )

    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')
    pred_mu     = get_data_counts( jet_files_mu    , jet_files_mu_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 
    pred_elfull = get_data_counts( jet_files_elfull, jet_files_elfull_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 
    pred_el     = get_data_counts( jet_files_el    , jet_files_el_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

    print 'muons'
    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
            ptmax = pt_bins_jetfile[idx+1]

            bin = (r1,r2,ptmin,ptmax)

            print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
            print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['stat']['rf'][bin], pred_mu['stat']['fr'][bin], pred_mu['stat']['ff'][bin], (  pred_mu['stat']['rf'][bin]+ pred_mu['stat']['fr'][bin]+ pred_mu['stat']['ff'][bin] ) )
            print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['syst']['rf'][bin], pred_mu['syst']['fr'][bin], pred_mu['syst']['ff'][bin], (  pred_mu['syst']['rf'][bin]+ pred_mu['syst']['fr'][bin]+ pred_mu['syst']['ff'][bin] ) )
            print 'Predicted Total rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['total']['rf'][bin], pred_mu['total']['fr'][bin], pred_mu['total']['ff'][bin], (  pred_mu['total']['rf'][bin]+ pred_mu['total']['fr'][bin]+ pred_mu['total']['ff'][bin] ) )

    print 'Electrons Baseline'
    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
            ptmax = pt_bins_jetfile[idx+1]

            bin = (r1,r2,ptmin,ptmax)

            print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)

            print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_el['stat']['rf'][bin], pred_el['stat']['fr'][bin], pred_el['stat']['ff'][bin], (  pred_el['stat']['rf'][bin]+ pred_el['stat']['fr'][bin]+ pred_el['stat']['ff'][bin] ) )
            print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_el['syst']['rf'][bin], pred_el['syst']['fr'][bin], pred_el['syst']['ff'][bin], (  pred_el['syst']['rf'][bin]+ pred_el['syst']['fr'][bin]+ pred_el['syst']['ff'][bin] ) )
            print 'Predicted Total rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_el['total']['rf'][bin], pred_el['total']['fr'][bin], pred_el['total']['ff'][bin], (  pred_el['total']['rf'][bin]+ pred_el['total']['fr'][bin]+ pred_el['total']['ff'][bin] ) )

    print 'Electrons'
    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
            ptmax = pt_bins_jetfile[idx+1]

            bin = (r1,r2,ptmin,ptmax)

            print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
            print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['stat']['rf'][bin], pred_elfull['stat']['fr'][bin], pred_elfull['stat']['ff'][bin], (  pred_elfull['stat']['rf'][bin]+ pred_elfull['stat']['fr'][bin]+ pred_elfull['stat']['ff'][bin] ) )
            print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['syst']['rf'][bin], pred_elfull['syst']['fr'][bin], pred_elfull['syst']['ff'][bin], (  pred_elfull['syst']['rf'][bin]+ pred_elfull['syst']['fr'][bin]+ pred_elfull['syst']['ff'][bin] ) )
            print 'Predicted Total rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['total']['rf'][bin], pred_elfull['total']['fr'][bin], pred_elfull['total']['ff'][bin], (  pred_elfull['total']['rf'][bin]+ pred_elfull['total']['fr'][bin]+ pred_elfull['total']['ff'][bin] ) )


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

    file_muon = open( outputDir + '/jet_fake_results__mgg.pickle', 'w' )
    pickle.dump( pred_mu, file_muon )
    file_muon.close()

    file_elfull = open( outputDir + '/jet_fake_results__egg_allZRejCuts.pickle', 'w' )
    pickle.dump( pred_elfull, file_elfull )
    file_elfull.close()


def get_mapped_directory( base_dir_jet, jet_dirs_key ) :
    
    jet_dir_key_map = {}

    for dir in os.listdir( base_dir_jet ) :
        res = re.match( jet_dirs_key, dir )
        if res is not None :
            jet_dir_key_map[ ( int(res.group(1)), int(res.group(2)), int(res.group(3)) ) ]  = dir

    return jet_dir_key_map

def get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key ) :

    jet_files = {}
    for dir in os.listdir( base_dir_jet ) :
        res = re.match( jet_dirs_key, dir )
        if res is not None :
            jet_files[( int(res.group(1)), int(res.group(2)), int(res.group(3)) ) ] = {}

            for file in os.listdir( base_dir_jet+'/'+dir  ) :
                fresl = re.match(file_key, file )
                if fresl is not None :
                    jet_files[( int(res.group(1)), int(res.group(2)), int(res.group(3)) ) ][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4))] = file

    return jet_files


def MakeEleBkgEstimate(base_dir_ele, base_dir_jet, outputDir=None) :

    samplesWgg.deactivate_all_samples()
    samplesWgg.activate_sample('Data')

    pt_bins = [ 15, 25, 40, 80, 1000000 ]
    eta_bins = {'EB': [0.0, 0.1, 0.5, 1.0, 1.48 ], 'EE' : [1.57, 2.1, 2.2, 2.3, 2.4, 2.5] }
    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB'), ('EE', 'EE')]


    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')

    # get root file
    rfile = ROOT.TFile.Open( '%s/ElectronFakeFitsRatio/results.root'%base_dir_ele )
    rhist = rfile.Get('ff')

    nxbins = rhist.GetXaxis().GetNbins()
    nybins = rhist.GetYaxis().GetNbins()
    xmin = rhist.GetXaxis().GetBinLowEdge(1)
    xmax = rhist.GetXaxis().GetBinUpEdge(nxbins)
    ymin = rhist.GetYaxis().GetBinLowEdge(1)
    ymax = rhist.GetYaxis().GetBinUpEdge(nybins)

    data_samp = samplesWgg.get_samples( name='Data' )[0]
    # get data counts from inverted pixel seed 
    results_lead = {}
    results_subl = {}
    for r1, r2 in regions :
        #invert lead, draw lead
        samplesWgg.create_hist(data_samp, 'fabs(ph_eta[0]):ph_pt[0]', ' PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] )' %(invPixLead_zrej_cuts_egg, r1, r2), (nxbins, xmin, xmax, nybins, ymin, ymax) )

        hist_lead = data_samp.hist.Clone('hist_lead__%s-%s' %(r1,r2))

        for pidx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[pidx+1]
            results_lead[(r1, r2, ptmin, ptmax)] = 0
            for eidx, etamin in enumerate( eta_bins[r1][:-1] ) :
                etamax = eta_bins[r1][eidx+1]

                ptbinmin = hist_lead.GetXaxis().FindBin( int(ptmin) )
                if ptmax == 'max' :
                    ptbinmax = hist_lead.GetXaxis().FindBin( hist_lead.GetNbinsX() )
                else :
                    ptbinmax = hist_lead.GetXaxis().FindBin( int(ptmax) )-1

                etabinmin = hist_lead.GetYaxis().FindBin( etamin )
                etabinmax = hist_lead.GetYaxis().FindBin( etamax )-1

                nData = hist_lead.Integral( ptbinmin, ptbinmax, etabinmin, etabinmax )
                ff = rhist.GetBinContent( ptbinmin, etabinmin )

                print 'ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptminmax = %d, etabinmin = %d, etabinmax = %d' %( ptmin, ptmax, etamin, etamax, ptbinmin, ptbinmax, etabinmin, etabinmax )
                print 'GetBinContent in %f < pt < %f, %f < eta < %f ' %( rhist.GetXaxis().GetBinLowEdge(ptbinmin), rhist.GetXaxis().GetBinUpEdge(ptbinmin), rhist.GetYaxis().GetBinLowEdge(etabinmin), rhist.GetYaxis().GetBinUpEdge(etabinmin) )

                results_lead[(r1, r2, ptmin, ptmax)]  = results_lead[(r1,r2, ptmin, ptmax)] + nData*ff
                #results_lead[(r1, r2, ptmin, ptmax)]  = results_lead[(r1,r2, ptmin, ptmax)] + nData

        #invert subl, draw subl
        samplesWgg.create_hist(data_samp, 'fabs(ph_eta[1]):ph_pt[1]', ' PUWeight * ( %s && ph_Is%s[0] && ph_Is%s[1] )' %(invPixSubl_zrej_cuts_egg, r1, r2), (nxbins, xmin, xmax, nybins, ymin, ymax) )

        hist_subl = data_samp.hist.Clone('hist_subl__%s-%s' %(r1,r2))

        for pidx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[pidx+1]
            results_subl[(r1, r2, ptmin, ptmax)] = 0
            for eidx, etamin in enumerate( eta_bins[r2][:-1] ) :
                etamax = eta_bins[r2][eidx+1]

                ptbinmin = hist_subl.GetXaxis().FindBin( int(ptmin) )
                if ptmax == 'max' :
                    ptbinmax = hist_subl.GetXaxis().FindBin( hist_subl.GetNbinsX() )
                else :
                    ptbinmax = hist_subl.GetXaxis().FindBin( int(ptmax) )-1

                etabinmin = hist_subl.GetYaxis().FindBin( etamin )
                etabinmax = hist_subl.GetYaxis().FindBin( etamax )-1

                nData = hist_subl.Integral( ptbinmin, ptbinmax, etabinmin, etabinmax )
                ff = rhist.GetBinContent( ptbinmin, etabinmin )

                results_subl[(r1, r2, ptmin, ptmax)]  = results_subl[(r1,r2, ptmin, ptmax)] + nData*ff
                #results_subl[(r1, r2, ptmin, ptmax)]  = results_subl[(r1,r2, ptmin, ptmax)] + nData


    results_full= {}
    for bin, val in results_lead.iteritems() : 
        results_full[bin] = val
    for bin, val in results_subl.iteritems() : 
        results_full[bin] = results_full[bin] + val
        

    file_key_lead = 'results__elfullinvpixlead__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_subl = 'results__elfullinvpixsubl__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_lead_syst = 'results__syst__elfullinvpixlead__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    file_key_subl_syst = 'results__syst__elfullinvpixsubl__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle'
    jet_dir_key_map = {}
    jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )
    jet_files_lead = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead )
    jet_files_subl = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_subl )
    jet_files_lead_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead_syst )
    jet_files_subl_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_subl_syst )

    pred_lead = get_data_counts( jet_files_lead, jet_files_lead_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 
    pred_subl = get_data_counts( jet_files_subl, jet_files_subl_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

    # get fake factors and binning from file
    rfile_coarse = ROOT.TFile.Open( '%s/ElectronFakeFitsRatioCoarseEta/results.root' %base_dir_ele )
    rhist_coarse = rfile_coarse.Get( 'ff') 

    scaled_rf = {}
    scaled_fr = {}
    scaled_ff = {}
    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]

            ff_lead = -1
            ff_subl = -1
            bin_eb = rhist_coarse.GetYaxis().FindBin( 1.0 )
            bin_ee = rhist_coarse.GetYaxis().FindBin( 2.0 )
            bin_pt = rhist_coarse.GetXaxis().FindBin( int(ptmin ) )
            if r1 == 'EB' :
                ff_lead = rhist_coarse.GetBinContent( bin_pt, bin_eb )
                print 'ptmin = %s, ptmax = %s, histptmin = %d, histptmax = %d'  %( ptmin, ptmax, rhist_coarse.GetXaxis().GetBinLowEdge( bin_pt ), rhist_coarse.GetXaxis().GetBinUpEdge( bin_pt ) )
                print 'reg = EB, histetamin = %f, histetamax = %f'  %( rhist_coarse.GetYaxis().GetBinLowEdge( bin_eb ), rhist_coarse.GetYaxis().GetBinUpEdge( bin_eb ) )
            if r1 == 'EE' :
                ff_lead = rhist_coarse.GetBinContent( bin_pt, bin_ee )
                print 'reg = EE, histetamin = %f, histetamax = %f'  %(  rhist_coarse.GetYaxis().GetBinLowEdge( bin_ee ), rhist_coarse.GetYaxis().GetBinUpEdge( bin_ee ) )

            if r2 == 'EB' :
                ff_subl = rhist_coarse.GetBinContent( bin_pt, bin_eb )
            if r2 == 'EE' :
                ff_subl = rhist_coarse.GetBinContent( bin_pt, bin_ee )


            scaled_rf[ (r1,r2,ptmin,ptmax) ] = pred_lead['total']['rf'][( r1,r2,ptmin,ptmax)]*ff_lead + pred_subl['total']['rf'][( r1,r2,ptmin,ptmax)]*ff_subl
            scaled_fr[ (r1,r2,ptmin,ptmax) ] = pred_lead['total']['fr'][( r1,r2,ptmin,ptmax)]*ff_lead + pred_subl['total']['fr'][( r1,r2,ptmin,ptmax)]*ff_subl
            scaled_ff[ (r1,r2,ptmin,ptmax) ] = pred_lead['total']['ff'][( r1,r2,ptmin,ptmax)]*ff_lead + pred_subl['total']['ff'][( r1,r2,ptmin,ptmax)]*ff_subl

            #scaled_rf[ (r1,r2,ptmin,ptmax) ] = pred_lead['rf'][( r1,r2,ptmin,ptmax)] + pred_subl['rf'][( r1,r2,ptmin,ptmax)]
            #scaled_fr[ (r1,r2,ptmin,ptmax) ] = pred_lead['fr'][( r1,r2,ptmin,ptmax)] + pred_subl['fr'][( r1,r2,ptmin,ptmax)]
            #scaled_ff[ (r1,r2,ptmin,ptmax) ] = pred_lead['ff'][( r1,r2,ptmin,ptmax)] + pred_subl['ff'][( r1,r2,ptmin,ptmax)]

    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]
            print '%s-%s, pt %s-%s' %( r1, r2, ptmin, ptmax)
    
            print 'Pred rf = %s, scaled rf = %s' %( pred_lead['total']['rf'][(r1,r2,ptmin,ptmax)]+pred_subl['total']['rf'][(r1,r2,ptmin,ptmax)], scaled_rf[(r1,r2,ptmin,ptmax)] )
            print 'Pred fr = %s, scaled fr = %s' %( pred_lead['total']['fr'][(r1,r2,ptmin,ptmax)]+pred_subl['total']['fr'][(r1,r2,ptmin,ptmax)], scaled_fr[(r1,r2,ptmin,ptmax)] )
            print 'Pred ff = %s, scaled ff = %s' %( pred_lead['total']['ff'][(r1,r2,ptmin,ptmax)]+pred_subl['total']['ff'][(r1,r2,ptmin,ptmax)], scaled_ff[(r1,r2,ptmin,ptmax)] )


    results_subtracted = {}
    for (r1,r2, ptmin, ptmax), val in results_full.iteritems() :

            #print 'Ele pred %s-%s pt %s-%s = %s' %( r1, r2, ptmin, ptmax, val )
            #print 'Jet pred %s-%s pt %s-%s = %s' %( r1, r2, ptmin, ptmax, scaled_rf[ (r1,r2,ptmin,ptmax) ] + scaled_fr[ (r1,r2,ptmin,ptmax) ] + scaled_ff[ (r1,r2,ptmin,ptmax) ])
            print 'Ele pred Final %s-%s pt %s-%s = %s' %( r1, r2, ptmin, ptmax, val-scaled_rf[ (r1,r2,ptmin,ptmax) ] + scaled_fr[ (r1,r2,ptmin,ptmax) ] + scaled_ff[ (r1,r2,ptmin,ptmax) ] )
            results_subtracted[(r1,r2, ptmin, ptmax)] = val-scaled_rf[ (r1,r2,ptmin,ptmax) ] + scaled_fr[ (r1,r2,ptmin,ptmax) ] + scaled_ff[ (r1,r2,ptmin,ptmax) ] 


    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

        file_raw = open( outputDir + '/electron_fake_results__noJetFakeSubtraction.pickle', 'w' )
        pickle.dump( results_full, file_raw )
        file_raw.close()

        file_sub = open( outputDir + '/electron_fake_results.pickle', 'w' )
        pickle.dump( results_subtracted, file_sub )
        file_sub.close()


    

def get_data_counts( jet_files, jet_files_syst, regions, pt_bins,  jet_dir_key_map, base_dir_jet ) :

    results = {'stat' : {}, 'syst' : {}, 'total' : {} }
    for val in results.values() :
       val['rf'] = {}
       val['fr'] = {}
       val['ff'] = {}

    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins[:-1]) :
            ptmax = pt_bins[idx+1]

            reg_bin = (r1, r2, ptmin, ptmax) 

            sorted_jet_dirs = jet_files.keys()
            sorted_jet_dirs.sort()

            for val in results.values() :
                val['rf'][reg_bin] = None
                val['fr'][reg_bin] = None
                val['ff'][reg_bin] = None

            for dir_key in sorted_jet_dirs :

                
                fentries = jet_files[dir_key]
                fentries_syst = jet_files_syst[dir_key]

                

                if reg_bin not in fentries :
                    continue

                sub_dir_jet = jet_dir_key_map[dir_key]

                ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin])
                predictions = pickle.load(ofile)
                ofile.close()

                ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin])
                predictions_syst = pickle.load(ofile)
                ofile.close()

                Ndata_tl = predictions['Ndata_TL']
                Ndata_lt = predictions['Ndata_LT']
                Ndata_ll = predictions['Ndata_LL']

                if Ndata_tl == 0 or Ndata_lt == 0 or Ndata_ll == 0 :
                    print 'No data entries for AsymIso %d-%d-%d, region %s-%s, pt %s-%s ' %( dir_key[0], dir_key[1], dir_key[2], r1, r2, ptmin, ptmax )
                    print 'Ndata_tl = %s, Ndata_lt = %s, Ndata_ll = %s' %( Ndata_tl, Ndata_lt, Ndata_ll)
                    continue

                Npred_rf = predictions['Npred_RF_TT']
                Npred_fr = predictions['Npred_FR_TT']
                Npred_ff = predictions['Npred_FF_TT']

                Npred_rf_syst = predictions_syst['Npred_RF_TT']
                Npred_fr_syst = predictions_syst['Npred_FR_TT']
                Npred_ff_syst = predictions_syst['Npred_FF_TT']

                results['stat']['rf'][reg_bin] = Npred_rf
                results['stat']['fr'][reg_bin] = Npred_fr
                results['stat']['ff'][reg_bin] = Npred_ff

                results['syst']['rf'][reg_bin] = Npred_rf_syst
                results['syst']['fr'][reg_bin] = Npred_fr_syst
                results['syst']['ff'][reg_bin] = Npred_ff_syst

                Npred_rf_tot = Npred_rf
                Npred_fr_tot = Npred_fr
                Npred_ff_tot = Npred_ff

                Npred_rf_syst_zero =ufloat( 0, Npred_rf_syst.s )
                Npred_fr_syst_zero =ufloat( 0, Npred_fr_syst.s )
                Npred_ff_syst_zero =ufloat( 0, Npred_ff_syst.s )

                Npred_rf_tot += Npred_rf_syst_zero
                Npred_fr_tot += Npred_fr_syst_zero
                Npred_ff_tot += Npred_ff_syst_zero
                
                results['total']['rf'][reg_bin] = Npred_rf_tot
                results['total']['fr'][reg_bin] = Npred_fr_tot
                results['total']['ff'][reg_bin] = Npred_ff_tot

                break

            # if results weren't set in any cases above, 
            # get the results from the first entry
            if results['stat']['rf'][reg_bin] is None or results['stat']['fr'][reg_bin] is None or results['stat']['ff'][reg_bin] is None :

                dir_key = sorted_jet_dirs[0]

                fentries = jet_files[dir_key]

                sub_dir_jet = jet_dir_key_map[dir_key]

                ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries[( r1, r2, ptmin, ptmax ) ])
                predictions = pickle.load(ofile)
                ofile.close()

                ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin])
                predictions_syst = pickle.load(ofile)
                ofile.close()

                Npred_rf = predictions['Npred_RF_TT']
                Npred_fr = predictions['Npred_FR_TT']
                Npred_ff = predictions['Npred_FF_TT']

                Npred_rf_syst = predictions_syst['Npred_RF_TT']
                Npred_fr_syst = predictions_syst['Npred_FR_TT']
                Npred_ff_syst = predictions_syst['Npred_FF_TT']

                results['stat']['rf'][reg_bin] = Npred_rf
                results['stat']['fr'][reg_bin] = Npred_fr
                results['stat']['ff'][reg_bin] = Npred_ff

                results['syst']['rf'][reg_bin] = Npred_rf_syst
                results['syst']['fr'][reg_bin] = Npred_fr_syst
                results['syst']['ff'][reg_bin] = Npred_ff_syst

                Npred_rf_tot = Npred_rf
                Npred_fr_tot = Npred_fr
                Npred_ff_tot = Npred_ff

                Npred_rf_syst_zero =ufloat( 0, Npred_rf_syst.s )
                Npred_fr_syst_zero =ufloat( 0, Npred_fr_syst.s )
                Npred_ff_syst_zero =ufloat( 0, Npred_ff_syst.s )

                Npred_rf_tot += Npred_rf_syst_zero
                Npred_fr_tot += Npred_fr_syst_zero
                Npred_ff_tot += Npred_ff_syst_zero
                
                results['total']['rf'][reg_bin] = Npred_rf_tot
                results['total']['fr'][reg_bin] = Npred_fr_tot
                results['total']['ff'][reg_bin] = Npred_ff_tot

    return results

main()
