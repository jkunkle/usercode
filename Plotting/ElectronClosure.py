"""
Do electron fake closure using MC 
"""
import sys
import os
import re
import math
import uuid
import copy
import imp
from array import array
import random
import collections
import pickle
import time

# Parse command-line options
from argparse import ArgumentParser

def parseArgs() :
    p = ArgumentParser()
    p.add_argument('--fileName',     default='ntuple.root',  dest='fileName',        help='( Default ntuple.root ) Name of files')
    p.add_argument('--treeName',     default='events'     ,  dest='treeName',        help='( Default events ) Name tree in root file')
    p.add_argument('--outputDir',     default=None    ,  dest='outputDir',        help='directory for output histograms')
    p.add_argument('--samplesConf',  default=None,           dest='samplesConf',     help=('Use alternate sample configuration. '
                                                                                           'Must be a python file that implements the configuration '
                                                                                           'in the same manner as in the main() of this script.  If only '
                                                                                           'the file name is given it is assumed to be in the same directory '
                                                                                           'as this script, if a path is given, use that path' ) )

    return p.parse_args()

import ROOT
from uncertainties import ufloat
from SampleManager import SampleManager
from SampleManager import Sample
from SampleManager import DrawConfig

def main() :

    base_dir_num  = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09/'
    base_dir_den  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaMediumPhIDNoTrigOlapRmRmBranchesDup_2016_07_21'
    base_dir_invl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaMediumPhIDNoTrigOlapRmRmBranchesInvPSVLead_2016_07_21'
    base_dir_invs = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaMediumPhIDNoTrigOlapRmRmBranchesInvPSVSubl_2016_07_21'

    global sampManNum
    global sampManDen
    global sampManInvL
    global sampManInvS

    sampManNum    = SampleManager(base_dir_num, options.treeName,filename=options.fileName )
    sampManDen    = SampleManager(base_dir_den, options.treeName,filename=options.fileName)
    sampManInvL   = SampleManager(base_dir_invl, options.treeName,filename=options.fileName)
    sampManInvS   = SampleManager(base_dir_invs, options.treeName,filename=options.fileName)

    if options.samplesConf is not None :

        sampManNum .ReadSamples( options.samplesConf )
        sampManDen .ReadSamples( options.samplesConf )
        sampManInvL.ReadSamples( options.samplesConf )
        sampManInvS.ReadSamples( options.samplesConf )

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

    eta_bins  = [0.0, 0.1, 0.5, 1.0, 1.44, 1.57, 2.1, 2.2, 2.4, 2.5 ]
    #pt_bins   = [15, 25, 40, 70, 100]
    pt_bins   = [15, 25, 30, 35, 40, 45, 50, 60, 70, 100]

    all_samp_man = []
    all_samp_man.append( sampManNum )
    all_samp_man.append( sampManDen )
    all_samp_man.append( sampManInvL )
    all_samp_man.append( sampManInvS )

    for s in all_samp_man  :
        s.deactivate_all_samples()

    calculators = []

    calculators.append( RunBasicClosure  ( pt_bins=pt_bins, eta_bins=eta_bins, 
                                           num_samp_man=sampManNum, den_samp_man=sampManDen, invl_samp_man=sampManInvL, invs_samp_man=sampManInvS,
                                           outputDir=options.outputDir) )
    #calculators.append( RunFittingClosure( eta_bins = eta_bins ) )

    for calc in calculators :
        draw_configs = calc.ConfigHists()

    for s in all_samp_man  :
        s.run_commands()

    for calc in calculators :
        calc.execute()

    print '^_^ FINISHED ^_^'

class RunBasicClosure() :

    def __init__( self, **kwargs ) :

        self.configs = {}
        self.status = True

        self.pt_bins           = kwargs.get( 'pt_bins'              , None)
        self.eta_bins          = kwargs.get( 'eta_bins'              , None)
        self.outputDir         = kwargs.get( 'outputDir', None )

        self.samp_mans = {}
        self.samp_mans['numerator']   = kwargs.get( 'num_samp_man', None )
        self.samp_mans['denominator'] = kwargs.get( 'den_samp_man', None )
        self.samp_mans['invl']        = kwargs.get( 'invl_samp_man', None )
        self.samp_mans['invs']        = kwargs.get( 'invs_samp_man', None )

        if self.pt_bins is None :
            print 'RunBasicClosure.init -- ERROR, did not get pt_bins'
            self.status = False

        if self.eta_bins is None :
            print 'RunBasicClosure.init -- ERROR, did not get eta_bins'
            self.status = False

        for val in self.samp_mans.values() :
            if val is None :
                print 'RunBasicClosure.init -- ERROR, did not get sample manager'
                self.status = False

    def get_drawvar( self, name ) :
        """ Get the drawn variable, y:x """

        cvar, ivar = self.get_phvar( name )

        if name == 'invs' :
            return 'fabs(ph_eta[%s[1]]):ph_pt[%s[1]]' %(ivar, ivar) # y:x
        else :
            return 'fabs(ph_eta[%s[0]]):ph_pt[%s[0]]' %(ivar, ivar) # y:x

    def get_phvar( self, name ) :
        """ Return the counting and indexing variables """

        if name == 'numerator' or name == 'target' :
            return ('ph_mediumPassPSV_n', 'ptSorted_ph_mediumPassPSV_idx' )
        elif name == 'denominator' :
            return ('ph_mediumFailPSV_n', 'ptSorted_ph_mediumFailPSV_idx' )
        elif name == 'invs' or name == 'invl' : 
            return ('ph_mediumNoEleVeto_n', 'ptSorted_ph_mediumNoEleVeto_idx' )

            
    def get_sample( self, name ) :
        if name == 'numerator' or name == 'denominator' :
            return 'DYJetsToLL'
        elif name == 'invl' or name == 'invs' :
            return 'Zg'
        else :
            #return 'Zg'
            return 'ZgPhOlap'

    def get_selection( self, name, ptmin=None, ptmax= None, addtl=None  ) :
        """ Build the full selection """

        cvar, ivar = self.get_phvar( name )

        if name == 'numerator' or name == 'denominator' :
            selection = 'el_passtrig_n == 1 && %s==1 && m_trigEl_phot[%s[0]] > 81 && m_trigEl_phot[%s[0]] < 101' %( cvar, ivar, ivar )
        elif name == 'target' :
            if addtl == 'massCR' :
                selection = 'el_passtrig_n == 1 && %s==2 && ( ( m_trigEl_phot[%s[0]] > 81 && m_trigEl_phot[%s[0]] < 101 ) || ( m_trigEl_phot[%s[1]] > 81 && m_trigEl_phot[%s[1]] < 101 ) ) ' %( cvar, ivar, ivar, ivar, ivar )
            elif addtl == 'massCRTEST' :
                selection = 'el_passtrig_n == 1 && %s==2 && ( (fabs(m_trigelph1-91.2) < 10 ) || ( fabs(m_trigelph2-91.2) < 10 ) ) ' %( cvar )
            elif addtl == 'massVeto' :
                selection = 'el_passtrig_n == 1 && %s==2 && !(fabs(m_trigelphph-91.2) < 10) && !(fabs(m_trigelph1-91.2) < 10)  && !(fabs(m_trigelph2-91.2) < 10) ' %( cvar )
            else :
                selection = 'el_passtrig_n == 1 && %s==2 ' %( cvar )

        elif name =='invl' or name == 'invs' :
            selection = 'el_passtrig_n == 1 && %s==2 && ph_mediumPassPSV_n==1 ' %( cvar )

        #if ptmin is not None :
        #    selection += ' && ph_pt[%s[0]] > %f' %( ivar, ptmin )
        #if ptmax is not None :
        #    selection += ' && ph_pt[%s[0]] < %f' %( ivar, ptmax )

        return selection

    def ConfigHists(self, **kwargs ) :

        if not self.status :
            print 'RunBasicClosure.ConfigHists -- ERROR, aborting because of previous errors'

        self.configure_hist( 'numerator'   )
        self.configure_hist( 'denominator' )
        self.configure_hist( 'target'      )
        self.configure_hist( 'target'     , 'massCR' )
        self.configure_hist( 'target'     , 'massCRTEST' )
        self.configure_hist( 'target'     , 'massVeto' )
        self.configure_hist( 'invl'        )
        self.configure_hist( 'invs'        )

        
    def execute( self, **kwargs ):
        hist_num     = sampManNum .load_samples( self.configs['numerator']   )[0].hist
        hist_den     = sampManDen .load_samples( self.configs['denominator'] )[0].hist
        hist_invl    = sampManInvL.load_samples( self.configs['invl']        )[0].hist
        hist_invs    = sampManInvS.load_samples( self.configs['invs']        )[0].hist


        hist_num.SetName('numerator')
        hist_den.SetName('denominator')
        hist_invl.SetName( 'invl' )
        hist_invs.SetName( 'invs' )


        hist_ff = hist_num.Clone( 'fake_factor' )
        hist_ff.Divide( hist_den )

        hist_added = hist_invl.Clone( 'hist_added' )
        hist_added.Add( hist_invs )

        hist_prediction = hist_invl.Clone( 'prediction' )

        for xbin in xrange( 1, hist_prediction.GetNbinsX()+1 ) :
            for ybin in xrange( 1, hist_prediction.GetNbinsY() ) :

                ff_val = hist_ff  .GetBinContent( xbin, ybin )
                ff_err = hist_ff  .GetBinError  ( xbin, ybin )
                cr_val = hist_invl.GetBinContent( xbin, ybin )
                cr_err = hist_invl.GetBinError( xbin, ybin )

                ff = ufloat( ff_val, ff_err )
                cr = ufloat( cr_val, cr_err )

                pred = ff*cr

                hist_prediction.SetBinContent( xbin, ybin, pred.n )
                hist_prediction.SetBinError( xbin, ybin, pred.s )

        pred_ptbin = []
        can_ptbin = []

        target_histograms = []
        self.make_target_histograms( hist_prediction, target_histograms, can_ptbin)

        outfile = ROOT.TFile.Open( '%s/hist.root' %( self.outputDir ), 'RECREATE' )

        hist_num.Write()
        hist_den.Write()
        hist_invl.Write()
        hist_invs.Write()

        for thist in target_histograms :
            thist.Write()

        for hist in pred_ptbin :
            hist.Write()

        outfile.Close()

    def make_target_histograms( self, prediction, hist_list, can_list ) :

        target_names = []
        target_hists = []

        for conf_name in self.configs.keys() :
            if conf_name.count( 'target' ) :
                target_names.append( conf_name )

        for conf_name in target_names :

            target_hists.append( sampManNum .load_samples( self.configs[conf_name] )[0].hist )
            target_hists[-1].SetName( conf_name )

        for idx, conf_name in enumerate(target_names) :

            for xbin in xrange( 1, prediction.GetNbinsX()+1 ) :
                this_pred = prediction.ProjectionY( 'pred_ptbin_%d' %xbin, xbin, xbin ) 
                this_pred.SetLineColor( ROOT.kRed )
                hist_list.append(this_pred )
                this_target = target_hists[idx].ProjectionY( '%s_ptbin_%d' %(conf_name, xbin),  xbin, xbin)
                target_hists.append( this_target )
                tcan_ptbin = ROOT.TCanvas( 'can_%s_ptbin_%d' %( conf_name, xbin ) )
                tcan_ptbin.cd()
                this_pred.Draw()
                this_target.Draw('same')
                can_list.append( tcan_ptbin )

        for thist in target_hists :
            hist_list.append( thist )


    def configure_hist(self, name, addtl=None ) :

        if name == 'target' :
            sname = 'numerator'
        else :
            sname = name

        sampMan = self.samp_mans.get(sname, None )
        if sampMan is None :
            print 'RunBasicClosure.configure_hist -- ERROR, Could not get sample manager for %s.  Aborting!' %name


        drawvar   = self.get_drawvar( name )
        selection = self.get_selection( name, addtl=addtl )
        sample    = self.get_sample( name )

        draw_samp = sampMan.get_samples(name=sample )

        if draw_samp :
            print '---------------------------------'
            print ' Draw for var %s        ' %drawvar
            print 'Binning = ', self.eta_bins
            print selection
            print '---------------------------------'

            config_name = name
            if addtl is not None :
                config_name = '%s_%s' %( name, addtl )
        
            self.configs[config_name] = sampMan.config_and_queue_hist( draw_samp[0], drawvar, selection,  (self.pt_bins, self.eta_bins)) 


            

if __name__ == '__main__' :
    options = parseArgs()
    if options.outputDir is not None :
        ROOT.gROOT.SetBatch(True)
    else :
        ROOT.gROOT.SetBatch(False)
    
    main()

