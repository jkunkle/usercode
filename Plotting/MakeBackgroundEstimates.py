"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
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
import collections

from SampleManager import SampleManager

ROOT.gROOT.SetBatch(True)

samplesWelgg = None
samplesWmugg = None
samplesWggInvSubl = None
samplesWggInvLead = None

ph_cuts = ''
lead_dr_cut = 0.4
subl_dr_cut = 0.4
phot_dr_cut = 0.4

el_cuts = {'elfull' : 
            'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%f && dr_ph2_leadLep>%f && mu_n==0 && !(fabs(m_leadLep_ph1_ph2-91.2) < 5) && !(fabs(m_leadLep_ph1-91.2) < 5)  && !(fabs(m_leadLep_ph2-91.2) < 5) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           'elzcr' :
           'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%f && dr_ph2_leadLep>%f && mu_n==0 && (fabs(m_leadLep_ph1_ph2-91.2) < 10) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           'elph1zcr' :
           'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%f && dr_ph2_leadLep>%f && mu_n==0 && (fabs(m_leadLep_ph1-91.2) < 10) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           'elph2zcr' :
           'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%f && dr_ph2_leadLep>%f && mu_n==0 && (fabs(m_leadLep_ph2-91.2) < 10) && m_ph1_ph2>15  %s ' %(lead_dr_cut, subl_dr_cut, ph_cuts),
           'elbase' : 
           {'invlead' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f && mu_n==0 && m_ph1_ph2>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts),
            'invsubl' : 'el_passtrig_n>0 && el_n==1 && ph_mediumNoEleVeto_n==2 && dr_ph1_ph2>0.4 && dr_ph1_leadLep>%.1f && dr_ph2_leadLep>%.1f && mu_n==0 && m_ph1_ph2>15  %s'%(lead_dr_cut, subl_dr_cut, ph_cuts) 
          },
}

_asym_iso_syst = { (0, 0, 0) : 0.05, (5,3,3) : 0.05, (8,5,5) : 0.10, (10, 7, 7) : 0.15, (12, 9, 9) : 0.2, (15,11,11) : 0.25, (20, 16, 16) : 0.35 }

_ele_eta_bins        = {'EB': [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44) ], 'EE' : [(1.57, 2.1), (2.1, 2.2), (2.2, 2.4), (2.4, 2.5)] }
_ele_eta_bins_highpt = {'EB': [(0.0, 0.1), (0.1, 0.5), (0.5, 1.0), (1.0, 1.44) ], 'EE' : [(1.57, 2.1), (2.1, 2.4), (2.4, 2.5)] }

_ele_eta_bins_coarse = {'EB': [(0.0, 1.44) ], 'EE' : [(1.57, 2.5)] }

_eta_pt_bin_map = { ('15', '25') : _ele_eta_bins, ('25', '40') : _ele_eta_bins, ('40', '70') : _ele_eta_bins, ('70', 'max') : _ele_eta_bins_highpt }
_eta_pt_bin_map_coarse = { ('15', '25') : _ele_eta_bins_coarse, ('25', '40') : _ele_eta_bins_coarse, ('40', '70') : _ele_eta_bins_coarse, ('70', 'max') : _ele_eta_bins_coarse}

class FakeFactorManager :

    def __init__(self, file, access_path=[] ) :

        if not os.path.isfile( file )  :
            print 'FakeFactorManager::init -- ERROR file %s does not exist' %file
            self.ff_dict = {}

        else :
            ofile = open( file )
            file_dict = pickle.load( ofile )
            ofile.close()

            # if the fake factors are buried within the dict
            # use the access path to
            # get to the fake factors 
            if not access_path :
                self.ff_dict = file_dict
            else :

                # first make some formatting changes
                mod_fields = []
                for field in access_path :
                    if isinstance( field, str ) :
                        mod_fields.append( '\'%s\'' %field )
                    elif isinstance( field, tuple ) :
                        mod_fields.append( '%s' %(field,) )
                    else :
                        mod_fields.append(field)

                eval_path = 'file_dict[' + ']['.join( mod_fields ) + ']'
                
                try :
                    self.ff_dict = eval(eval_path)
                except :
                    print 'Dict access path was not correct'
                    raise

        # figure out if pt or eta comes first 
        # get the maximum values of the
        # second of each pt or eta entry
        # and assume that the one with the greater
        # value is pt
        self.pt_first = None
        second_entries = []
        fourth_entries = []
        for bin in self.ff_dict :
            second_entries.append( float( bin[1] ) )
            fourth_entries.append( float( bin[3] ) )

        max_second = max( second_entries )
        max_fourth = max( fourth_entries )

        if max_second > max_fourth :
            self.pt_first = True
        else :
            self.pt_first = False

    def get_pt_eta_ff( self, ptmin, ptmax, etamin, etamax ) :

        if self.pt_first :
            return self._get_ff( ptmin, ptmax, etamin, etamax )
        else :
            return self._get_ff( etamin, etamax, ptmin, ptmax)
    def _get_ff( self, ent1min, ent1max, ent2min, ent2max) :

        if ent1max == 'max' :
            all_1max = []
            for key in self.ff_dict.keys() :
                all_1max.append( float(key[1]) )
            ent1max = max( all_1max )
        if ent2max == 'max' :
            all_2max = []
            for key in self.ff_dict.keys() :
                all_2max.append( float(key[3]) )
            ent2max = max( all_2max )

        for key, val in self.ff_dict.iteritems() :

            min1 = float(key[0])
            max1 = float(key[1])
            min2 = float(key[2])
            max2 = float(key[3])

            #print 'ent  min, max = %s, %s, %s, %s ' %( ent1min, ent1max, ent2min, ent2max) 
            #print 'dict min, max = %s, %s, %s, %s ' %( min1, max1, min2, max2)

            if float(ent1min) == min1 and float(ent1max) == max1 and float(ent2min) == min2 and float(ent2max) == max2 :
                return val

        print 'Could Not locate FF for entries %s, %s, %s, %s' %( ent1min, ent1max, ent2min, ent2max)
        print self.ff_dict.keys()
        return -1




def main() :

    p = ArgumentParser()
    
                                                                                           
    p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
    p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',  required=False,       help='Input directory base')
    p.add_argument('--plotDir',     default='Plots',  type=str ,        dest='plotDir',  required=False,       help='Directory where plots are written')
    p.add_argument('--ptbins',     default='15,25,40,70,1000000',  type=str ,        dest='ptbins',  required=False,       help='PT bins to use')
    
    options = p.parse_args()

    global samplesWelgg
    global samplesWelggCR
    global samplesWmugg
    global samplesWggInvLead
    global samplesWggInvSubl

    baseDirWelgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNomUnblindLowPt_2014_12_23'
    baseDirWelggCR = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNomUnblindAll_2015_01_26'
    baseDirWmugg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoEleVetoUnblindLowPt_2015_01_14'
    #baseDirWgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNomUnblindEleZCR_2014_12_23'
    baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvPixSeedLead_2014_12_23'
    baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvPixSeedSubl_2014_12_23'

    #baseDirWgg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaCSEVUnblindLowPt_2014_12_23'
    #baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvCSEVLead_2014_12_23'
    #baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvCSEVSubl_2014_12_23'

    #baseDirWgg        = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaTrigEleOlapUnblindLowPt_2015_01_02'
    #baseDirWggInvLead = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDTrigEleOlapInvPixSeedLead_2015_01_02'
    #baseDirWggInvSubl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDTrigEleOlapInvPixSeedSubl_2015_01_02'

    treename = 'ggNtuplizer/EventTree'
    filename = 'tree.root'

    sampleConfWgg = 'Modules/Wgamgam.py'

    samplesWelgg = SampleManager(baseDirWelgg, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWelggCR = SampleManager(baseDirWelggCR, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWmugg = SampleManager(baseDirWmugg, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWggInvLead = SampleManager(baseDirWggInvLead, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)
    samplesWggInvSubl = SampleManager(baseDirWggInvSubl, treename, filename=filename, xsFile='cross_sections/wgamgam.py', lumi=19400)

    samplesWelgg.ReadSamples( sampleConfWgg )
    samplesWelggCR.ReadSamples( sampleConfWgg )
    samplesWmugg.ReadSamples( sampleConfWgg )
    samplesWggInvLead.ReadSamples( sampleConfWgg )
    samplesWggInvSubl.ReadSamples( sampleConfWgg )

    bins = options.ptbins.split(',')

    ele_eta_bins = {'lead' : {'EB': [0.0, 0.1, 0.5, 1.0, 1.44 ], 'EE' : [1.57, 2.1, 2.2, 2.3, 2.4, 2.5] }, 
                    'subl' : {'EB': [0.0, 0.1, 0.5, 1.0, 1.44 ], 'EE' : [1.57, 2.1, 2.2, 2.3, 2.4, 2.5] } }
    ele_eta_bins_highpt = {'EB': [0.0, 0.1, 0.5, 1.0, 1.44 ], 'EE' : [1.57, 2.1, 2.4, 2.5] }
    ele_eta_bins_coarse = {'EB': [0.0, 1.44 ], 'EE' : [1.57, 2.5] }

    # get paths to different fit results
    suffix = ''

    path_nom           = 'ElectronFakeFitsRatio%s' %suffix 
    path_nom_coarse    = 'ElectronFakeFitsRatio%sCoarseEta' %suffix 
    path_mctemp        = 'ElectronFakeFitsRatio%sMCTemplateNDKeys' %suffix
    path_mctemp_coarse = 'ElectronFakeFitsRatio%sMCTemplateNDKeysCoarseEta' %suffix

    # use orderedDict to keep things in pT order
    file_bin_map             = collections.OrderedDict()
    file_bin_map_coarse      = collections.OrderedDict()
    file_bin_map_syst        = collections.OrderedDict()
    file_bin_map_coarse_syst = collections.OrderedDict()

    # define the map between pt bins and
    # the fit results we want to use
    file_bin_map             [(bins[0], bins[1])] = path_nom
    file_bin_map             [(bins[1], bins[2])] = path_nom
    file_bin_map             [(bins[2], bins[3])] = path_nom
    file_bin_map             [(bins[3], 'max')  ] = path_nom
    #file_bin_map_syst             [(bins[0], bins[1])] = path_nom
    #file_bin_map_syst             [(bins[1], bins[2])] = path_nom
    #file_bin_map_syst             [(bins[2], bins[3])] = path_nom
    #file_bin_map_syst             [(bins[3], 'max')  ] = path_nom

    file_bin_map_coarse      [(bins[0], bins[1])] = path_nom_coarse
    file_bin_map_coarse      [(bins[1], bins[2])] = path_nom_coarse
    file_bin_map_coarse      [(bins[2], bins[3])] = path_mctemp_coarse
    file_bin_map_coarse      [(bins[3], 'max')  ] = path_nom_coarse

    file_bin_map_syst        [(bins[0], bins[1])] = path_mctemp
    file_bin_map_syst        [(bins[1], bins[2])] = path_mctemp
    file_bin_map_syst        [(bins[2], bins[3])] = path_mctemp
    file_bin_map_syst        [(bins[3], 'max')  ] = path_mctemp
    #file_bin_map        [(bins[0], bins[1])] = path_mctemp
    #file_bin_map        [(bins[1], bins[2])] = path_mctemp
    #file_bin_map        [(bins[2], bins[3])] = path_mctemp
    #file_bin_map        [(bins[3], 'max')  ] = path_mctemp

    file_bin_map_coarse_syst [(bins[0], bins[1])] = path_mctemp_coarse
    file_bin_map_coarse_syst [(bins[1], bins[2])] = path_mctemp_coarse
    file_bin_map_coarse_syst [(bins[2], bins[3])] = path_nom_coarse
    file_bin_map_coarse_syst [(bins[3], 'max')  ] = path_mctemp_coarse

    pt_bins = [int(x) for x in options.ptbins.split(',')]

    if options.baseDir is not None :
        base_dir_ele = options.baseDir
        base_dir_jet = '%s/JetFakeResultsSyst'%options.baseDir
        outputDir='%s/BackgroundEstimates'%options.baseDir
        MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, pt_bins=pt_bins, el_selection='elfull', outputDir=outputDir )
        MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, pt_bins=pt_bins, el_selection='elzcr', outputDir=outputDir, namePostfix='__zcr' )
        MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, pt_bins=pt_bins, el_selection='elph1zcr', outputDir=outputDir, namePostfix='__ph1zcr' )
        MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, pt_bins=pt_bins, el_selection='elph2zcr', outputDir=outputDir, namePostfix='__ph2zcr' )
        #MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map_coarse, file_bin_map_coarse_syst, pt_bins=pt_bins, el_selection='elfull', outputDir=outputDir, namePostfix='__coarse', coarse=True )
        #MakeEleBkgEstimate( base_dir_ele, base_dir_jet, file_bin_map_coarse, file_bin_map_coarse_syst, pt_bins=pt_bins, el_selection='elzcr', outputDir=outputDir, namePostfix='__coarse__zcr', coarse=True )

        MakeJetBkgEstimate( base_dir_jet, pt_bins, outputDir )

        MakeBkgEstimatePlots( outputDir, options.plotDir )

        #MakeDiPhotonCREleFakeFactors( )

    print '^_^ FINSISHED ^_^'
    print 'It is safe to kill the program if it is hanging'

def MakeDiPhotonCREleFakeFactors( ) :

    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB')]

    data_samp_invlead = samplesWggInvLead.get_samples( name='Data' )[0]
    data_samp_invsubl = samplesWggInvSubl.get_samples( name='Data' )[0]
    data_samp_nom     = samplesWelggCR     .get_samples( name='Data' )[0]
    for r1, r2 in regions :
        # --------------------------------------
        # Mlgg control region
        # --------------------------------------
        draw_str_mlgg = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 )' %(el_cuts['elzcr'], r1, r2)

        samplesWggInvLead.create_hist(data_samp_invlead, 'pt_leadph12', draw_str_mlgg, ( 20, 0, 100) )

        hist_mlgg_lead = data_samp_invlead.hist.Clone('hist_lead_mlgg__%s-%s' %(r1,r2))

        samplesWggInvSubl.create_hist(data_samp_invsubl, 'pt_leadph12', draw_str_mlgg, ( 20, 0, 100) )

        hist_mlgg_subl = data_samp_invsubl.hist.Clone('hist_subl_mlgg__%s-%s' %(r1,r2))

        samplesWelggCR.create_hist(data_samp_nom, 'pt_leadph12', draw_str_mlgg, ( 20, 0, 100) )

        hist_mlgg_nom  = data_samp_nom.hist.Clone('hist_nom_mlgg__%s-%s' %(r1, r2) )

        hist_mlgg_lead.Add( hist_mlgg_subl ) 

        # --------------------------------------
        # Mlg1 control region
        # --------------------------------------
        draw_str_mlg1 = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 )' %(el_cuts['elph1zcr'], r1, r2)

        samplesWggInvLead.create_hist(data_samp_invlead, 'pt_leadph12', draw_str_mlg1, ( 20, 0, 100) )

        hist_mlg1_lead = data_samp_invlead.hist.Clone('hist_lead_mlg1__%s-%s' %(r1,r2))

        samplesWelggCR.create_hist(data_samp_nom, 'pt_leadph12', draw_str_mlg1, ( 20, 0, 100) )

        hist_mlg1_nom  = data_samp_nom.hist.Clone('hist_nom_mlg1__%s-%s' %(r1, r2) )

        # --------------------------------------
        # Mlg2 control region
        # --------------------------------------
        draw_str_mlg2 = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 )' %(el_cuts['elph2zcr'], r1, r2)

        samplesWggInvSubl.create_hist(data_samp_invlead, 'pt_sublph12', draw_str_mlg2, ( 20, 0, 100) )

        hist_mlg2_subl = data_samp_invlead.hist.Clone('hist_lead_mlg2__%s-%s' %(r1,r2))

        samplesWelggCR.create_hist(data_samp_nom, 'pt_sublph12', draw_str_mlg2, ( 20, 0, 100) )

        hist_mlg2_nom  = data_samp_nom.hist.Clone('hist_nom_mlg2__%s-%s' %(r1, r2) )


        # ------------------------------------------
        # Get the fake factors
        # ------------------------------------------
        pt_regions = [ (15, 25), (25,  40), (40, 70), (70, 100 ) ]

        ff_mlgg = []
        ff_mlg1 = []
        ff_mlg2 = []
        for ptmin, ptmax in pt_regions :

            ff_mlgg.append(make_fake_factor( numerator = hist_mlgg_nom, denominator=hist_mlgg_lead, min=ptmin, max=ptmax ) )
            ff_mlg1.append(make_fake_factor( numerator = hist_mlg1_nom, denominator=hist_mlg1_lead, min=ptmin, max=ptmax ) )
            ff_mlg2.append(make_fake_factor( numerator = hist_mlg2_nom, denominator=hist_mlg2_subl, min=ptmin, max=ptmax ) )

        print 'Mlgg CR, %s-%s' %(r1, r2)
        for idx, (min, max) in enumerate( pt_regions ) :
            print '%d-%d : %s (num=%s, den=%s), bins %d-%d' %( min, max, ff_mlgg[idx]['fake_factor'] , ff_mlgg[idx]['numerator'], ff_mlgg[idx]['denominator'], ff_mlgg[idx]['min_bin'], ff_mlgg[idx]['max_bin'] )
                                                                                                                                
        print 'Mlg1 CR, %s-%s' %(r1, r2)                                                                                        
        for idx, (min, max) in enumerate( pt_regions ) :                                                                        
            print '%d-%d : %s (num=%s, den=%s), bins %d-%d' %( min, max, ff_mlg1[idx]['fake_factor'] , ff_mlg1[idx]['numerator'], ff_mlg1[idx]['denominator'], ff_mlg1[idx]['min_bin'], ff_mlg1[idx]['max_bin'] )
                                                                                                                                
        print 'Mlg2 CR, %s-%s' %(r1, r2)                                                                                        
        for idx, (min, max) in enumerate( pt_regions ) :                                                                        
            print '%d-%d : %s (num=%s, den=%s), bins %d-%d' %( min, max, ff_mlg2[idx]['fake_factor'] , ff_mlg2[idx]['numerator'], ff_mlg2[idx]['denominator'], ff_mlg2[idx]['min_bin'], ff_mlg2[idx]['max_bin'] )

            

def make_fake_factor( numerator, denominator, min, max ) :


    bin_min = numerator.FindBin( min )
    bin_max = numerator.FindBin( max ) - 1
    num_err = ROOT.Double()
    num_int = numerator.IntegralAndError( bin_min, bin_max, num_err )

    num_val = ufloat( num_int, num_err )

    den_err = ROOT.Double()
    den_int = denominator.IntegralAndError( bin_min, bin_max, den_err )

    den_val = ufloat( den_int, den_err )

    if den_int != 0 :
        ratio = num_val / den_val
    else :
        ratio = ufloat(0, 0)

    return { 'numerator' : num_val, 'denominator' : den_val, 'fake_factor' : ratio, 'min' : min, 'max' : max, 'min_bin' : bin_min, 'max_bin' : bin_max}



def MakeJetBkgEstimate( base_dir_jet, pt_bins, outputDir=None ) :

    print '--------------------------------------'
    print 'START JET FAKE ESTIMATE'
    print '--------------------------------------'

    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB')]

    file_key_mu        = 'results__mu__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elfull    = 'results__elfull__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elzcr     = 'results__elzcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elph1zcr  = 'results__elph1zcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elph2zcr  = 'results__elph2zcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'

    # jet fake results with systematic
    # uncertainties propagated
    file_key_mu_syst       = 'results__syst__mu__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elfull_syst   = 'results__syst__elfull__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elzcr_syst    = 'results__syst__elzcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elph1zcr_syst = 'results__syst__elph1zcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'
    file_key_elph2zcr_syst = 'results__syst__elph2zcr__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max)(__subpt_(\d+)-(\d+|max)){0,1}.pickle'

    jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )


    jet_files_mu       = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu     )
    jet_files_elfull   = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull )
    jet_files_elzcr    = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elzcr  )
    jet_files_elph1zcr = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elph1zcr  )
    jet_files_elph2zcr = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elph1zcr  )

    jet_files_mu_syst       = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_mu_syst     )
    jet_files_elfull_syst   = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elfull_syst )
    jet_files_elzcr_syst    = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elzcr_syst     )
    jet_files_elph1zcr_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elph1zcr_syst     )
    jet_files_elph2zcr_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_elph2zcr_syst     )

    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')

    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

    if jet_files_mu.values()[0] :
        subl_ptbins = [ ( '70', 'max', '15', '40' ), ( '70', 'max', '40', 'max' ) ]
        subl_ptbins = [ ]
        pred_mu     = get_jet_fake_results( jet_files_mu    , jet_files_mu_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet, pt_bins_subl=subl_ptbins ) 
        print '---------------------------------------------'
        print 'JET FAKE RESULTS, MUON CHANNEL'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['stat']['rf'][bin]['result'], pred_mu['stat']['fr'][bin]['result'], pred_mu['stat']['ff'][bin]['result'], (  pred_mu['stat']['rf'][bin]['result']+ pred_mu['stat']['fr'][bin]['result']+ pred_mu['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['syst']['rf'][bin]['result'], pred_mu['syst']['fr'][bin]['result'], pred_mu['syst']['ff'][bin]['result'], (  pred_mu['syst']['rf'][bin]['result']+ pred_mu['syst']['fr'][bin]['result']+ pred_mu['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_mu['stat+syst']['rf'][bin]['result'], pred_mu['stat+syst']['fr'][bin]['result'], pred_mu['stat+syst']['ff'][bin]['result'], (  pred_mu['stat+syst']['rf'][bin]['result']+ pred_mu['stat+syst']['fr'][bin]['result']+ pred_mu['stat+syst']['ff'][bin]['result'] ) )

        file_muon = open( outputDir + '/jet_fake_results__mgg.pickle', 'w' )
        pickle.dump( pred_mu, file_muon )
        file_muon.close()

    if jet_files_elfull.values()[0] :
        pred_elfull = get_jet_fake_results( jet_files_elfull, jet_files_elfull_syst, regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print '---------------------------------------------'
        print 'JET FAKE RESULTS, ELECTRON CHANNEL WITH Z REJ CUTS'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)
                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['stat']['rf'][bin]['result'], pred_elfull['stat']['fr'][bin]['result'], pred_elfull['stat']['ff'][bin]['result'], (  pred_elfull['stat']['rf'][bin]['result']+ pred_elfull['stat']['fr'][bin]['result']+ pred_elfull['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['syst']['rf'][bin]['result'], pred_elfull['syst']['fr'][bin]['result'], pred_elfull['syst']['ff'][bin]['result'], (  pred_elfull['syst']['rf'][bin]['result']+ pred_elfull['syst']['fr'][bin]['result']+ pred_elfull['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elfull['stat+syst']['rf'][bin]['result'], pred_elfull['stat+syst']['fr'][bin]['result'], pred_elfull['stat+syst']['ff'][bin]['result'], (  pred_elfull['stat+syst']['rf'][bin]['result']+ pred_elfull['stat+syst']['fr'][bin]['result']+ pred_elfull['stat+syst']['ff'][bin]['result'] ) )

        file_elfull = open( outputDir + '/jet_fake_results__egg_allZRejCuts.pickle', 'w' )
        pickle.dump( pred_elfull, file_elfull )
        file_elfull.close()

    if jet_files_elzcr.values()[0] :
        pred_elzcr  = get_jet_fake_results( jet_files_elzcr , jet_files_elzcr_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print '---------------------------------------------'
        print 'JET FAKE RESULTS, ELECTRON CHANNEL IN Mlgg Z CR'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)

                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['stat']['rf'][bin]['result'], pred_elzcr['stat']['fr'][bin]['result'], pred_elzcr['stat']['ff'][bin]['result'], (  pred_elzcr['stat']['rf'][bin]['result']+ pred_elzcr['stat']['fr'][bin]['result']+ pred_elzcr['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['syst']['rf'][bin]['result'], pred_elzcr['syst']['fr'][bin]['result'], pred_elzcr['syst']['ff'][bin]['result'], (  pred_elzcr['syst']['rf'][bin]['result']+ pred_elzcr['syst']['fr'][bin]['result']+ pred_elzcr['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elzcr['stat+syst']['rf'][bin]['result'], pred_elzcr['stat+syst']['fr'][bin]['result'], pred_elzcr['stat+syst']['ff'][bin]['result'], (  pred_elzcr['stat+syst']['rf'][bin]['result']+ pred_elzcr['stat+syst']['fr'][bin]['result'] + pred_elzcr['stat+syst']['ff'][bin]['result'] ) )


        file_elzcr = open( outputDir + '/jet_fake_results__egg_ZCR.pickle', 'w' )
        pickle.dump( pred_elzcr, file_elzcr)
        file_elzcr.close()

    if jet_files_elph1zcr.values()[0] :
        pred_elph1zcr  = get_jet_fake_results( jet_files_elph1zcr , jet_files_elph1zcr_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print '---------------------------------------------'
        print 'JET FAKE RESULTS, ELECTRON CHANNEL IN Mlg1 Z CR'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)

                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph1zcr['stat']['rf'][bin]['result'], pred_elph1zcr['stat']['fr'][bin]['result'], pred_elph1zcr['stat']['ff'][bin]['result'], (  pred_elph1zcr['stat']['rf'][bin]['result']+ pred_elph1zcr['stat']['fr'][bin]['result']+ pred_elph1zcr['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph1zcr['syst']['rf'][bin]['result'], pred_elph1zcr['syst']['fr'][bin]['result'], pred_elph1zcr['syst']['ff'][bin]['result'], (  pred_elph1zcr['syst']['rf'][bin]['result']+ pred_elph1zcr['syst']['fr'][bin]['result']+ pred_elph1zcr['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph1zcr['stat+syst']['rf'][bin]['result'], pred_elph1zcr['stat+syst']['fr'][bin]['result'], pred_elph1zcr['stat+syst']['ff'][bin]['result'], (  pred_elph1zcr['stat+syst']['rf'][bin]['result']+ pred_elph1zcr['stat+syst']['fr'][bin]['result'] + pred_elph1zcr['stat+syst']['ff'][bin]['result'] ) )


        file_elph1zcr = open( outputDir + '/jet_fake_results__egg_ZCRPh1.pickle', 'w' )
        pickle.dump( pred_elph1zcr, file_elph1zcr)
        file_elph1zcr.close()

    if jet_files_elph2zcr.values()[0] :
        pred_elph2zcr  = get_jet_fake_results( jet_files_elph2zcr , jet_files_elph2zcr_syst    , regions, pt_bins_jetfile,  jet_dir_key_map, base_dir_jet ) 

        print '---------------------------------------------'
        print 'JET FAKE RESULTS, ELECTRON CHANNEL IN Mlg2 Z CR'
        print '---------------------------------------------'
        for r1, r2 in regions :

            for idx, ptmin in enumerate(pt_bins_jetfile[:-1] ) :
                ptmax = pt_bins_jetfile[idx+1]

                bin = (r1,r2,ptmin,ptmax)

                print 'Region %s-%s, pt %s-%s' %( r1,r2,ptmin,ptmax)

                print 'Predicted Stat rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph2zcr['stat']['rf'][bin]['result'], pred_elph2zcr['stat']['fr'][bin]['result'], pred_elph2zcr['stat']['ff'][bin]['result'], (  pred_elph2zcr['stat']['rf'][bin]['result']+ pred_elph2zcr['stat']['fr'][bin]['result']+ pred_elph2zcr['stat']['ff'][bin]['result'] ) )
                print 'Predicted Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph2zcr['syst']['rf'][bin]['result'], pred_elph2zcr['syst']['fr'][bin]['result'], pred_elph2zcr['syst']['ff'][bin]['result'], (  pred_elph2zcr['syst']['rf'][bin]['result']+ pred_elph2zcr['syst']['fr'][bin]['result']+ pred_elph2zcr['syst']['ff'][bin]['result'] ) )
                print 'Predicted Stat+Syst rf = %s, predicted fr = %s, predicted ff = %s, total = %s' %( pred_elph2zcr['stat+syst']['rf'][bin]['result'], pred_elph2zcr['stat+syst']['fr'][bin]['result'], pred_elph2zcr['stat+syst']['ff'][bin]['result'], (  pred_elph2zcr['stat+syst']['rf'][bin]['result']+ pred_elph2zcr['stat+syst']['fr'][bin]['result'] + pred_elph2zcr['stat+syst']['ff'][bin]['result'] ) )


        file_elph2zcr = open( outputDir + '/jet_fake_results__egg_ZCRPh2.pickle', 'w' )
        pickle.dump( pred_elph2zcr, file_elph2zcr)
        file_elph2zcr.close()

def MakeBkgEstimatePlots( baseDir, plotDir ) :

    # first make the nominal estimates

    regions = [('EB', 'EB'), ('EB' ,'EE'), ('EE', 'EB')]
    plot_binning = [0,5,10,15,25,40,70,200]

    for reg in regions + [(None, None)] :

        if reg[0] is not None :
            reg_str = ' && is%s_leadph12 && is%s_sublph12 ' %(reg[0],reg[1])
            reg_tag = '_%s-%s' %( reg[0], reg[1]) 
        else :
            reg_str = ' && !(isEE_leadph12 && isEE_sublph12 )'
            reg_tag = ''
    
        samplesWmugg.Draw( 'pt_leadph12', 'PUWeight * (mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.4 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 %s  ) ' %(reg_str), plot_binning )

        hist_data_mgg = samplesWmugg.get_samples(name='Data')[0].hist.Clone('pt_leadph12_mgg%s'%(reg_tag))
        save_hist( '%s/%s/Data/hist.root' %(baseDir, plotDir), hist_data_mgg )

        hist_sig_mgg  = samplesWmugg.get_samples(name='Wgg')[0].hist.Clone('pt_leadph12_mgg%s'%(reg_tag))
        save_hist( '%s/%s/Wgg/hist.root' %(baseDir, plotDir), hist_sig_mgg )

        hist_Zgg_mgg     = samplesWmugg.get_samples(name='Zgg')[0].hist.Clone('pt_leadph12_mgg%s'%(reg_tag))
        hist_ZggFSR_mgg  = samplesWmugg.get_samples(name='ZgammagammaFSR')[0].hist.Clone('pt_leadph12_mgg%s'%(reg_tag))
        #hist_Zgg_mgg.Add(hist_ZggFSR_mgg)
        add_syst_to_hist( hist_Zgg_mgg, 0.15 )
        add_syst_to_hist( hist_ZggFSR_mgg, 0.15 )

        save_hist( '%s/%s/ZggFSR/hist.root' %(baseDir, plotDir), hist_ZggFSR_mgg )
        save_hist( '%s/%s/Zgg/hist.root' %(baseDir, plotDir), hist_Zgg_mgg )

        draw_str_nom = 'PUWeight * (el_passtrig_n>0 && el_n==1 && ph_n==2 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.4 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && !(fabs(m_leadLep_ph1_ph2-91.2)<5) && !(fabs(m_leadLep_ph1-91.2)<5) && !(fabs(m_leadLep_ph2-91.2)<5) %s ) ' %reg_str
        draw_str_zcr = 'PUWeight * (el_passtrig_n>0 && el_n==1 && ph_n==2 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.4 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && (fabs(m_leadLep_ph1_ph2-91.2)<10) %s ) ' %reg_str
        draw_str_zcrph1 = 'PUWeight * (el_passtrig_n>0 && el_n==1 && ph_n==2 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.4 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && (fabs(m_leadLep_ph1-91.2)<10) %s ) ' %reg_str
        draw_str_zcrph2 = 'PUWeight * (el_passtrig_n>0 && el_n==1 && ph_n==2 && m_ph1_ph2 > 15 && dr_ph1_ph2 > 0.4 && dr_ph1_leadLep > 0.4 && dr_ph2_leadLep > 0.4 && (fabs(m_leadLep_ph2-91.2)<10) %s ) ' %reg_str

        hist_tag_nom    = 'egg%s' %reg_tag
        hist_tag_zcr    = 'egg_zcr%s' %reg_tag
        hist_tag_zcrph1 = 'egg_zcrph1%s' %reg_tag
        hist_tag_zcrph2 = 'egg_zcrph2%s' %reg_tag

        save_electron_hists( draw_str_nom   , plot_binning, '%s/%s' %(baseDir, plotDir), hist_tag_nom    )
        save_electron_hists( draw_str_zcr   , plot_binning, '%s/%s' %(baseDir, plotDir), hist_tag_zcr    )
        save_electron_hists( draw_str_zcrph1, plot_binning, '%s/%s' %(baseDir, plotDir), hist_tag_zcrph1 )
        save_electron_hists( draw_str_zcrph2, plot_binning, '%s/%s' %(baseDir, plotDir), hist_tag_zcrph2 )

    make_hist_from_pickle( samplesWmugg, baseDir + '/jet_fake_results__mgg.pickle'            , '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag='mgg', regions=regions )
    make_hist_from_pickle( samplesWelgg, baseDir + '/jet_fake_results__egg_allZRejCuts.pickle', '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag='egg', regions=regions )
    make_hist_from_pickle( samplesWelgg, baseDir + '/electron_fake_results.pickle'            , '%s/%s/EleFake/hist.root' %(baseDir, plotDir), tag='egg', regions=regions, syst=baseDir + '/electron_fake_results_syst.pickle')

    make_hist_from_pickle( samplesWelgg, baseDir + '/electron_fake_results__ph1zcr.pickle'       , '%s/%s/EleFake/hist.root' %(baseDir, plotDir), tag='egg_zcrph1', regions=regions)
    make_hist_from_pickle( samplesWelgg, baseDir + '/jet_fake_results__egg_ZCRPh1.pickle'        , '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag='egg_zcrph1', regions=regions )

    make_hist_from_pickle( samplesWelgg, baseDir + '/electron_fake_results__zcr.pickle'       , '%s/%s/EleFake/hist.root' %(baseDir, plotDir), tag='egg_zcr', regions=regions)
    make_hist_from_pickle( samplesWelgg, baseDir + '/jet_fake_results__egg_ZCR.pickle'        , '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag='egg_zcr', regions=regions )

    make_hist_from_pickle( samplesWelgg, baseDir + '/electron_fake_results__ph2zcr.pickle'       , '%s/%s/EleFake/hist.root' %(baseDir, plotDir), tag='egg_zcrph2', regions=regions)
    make_hist_from_pickle( samplesWelgg, baseDir + '/jet_fake_results__egg_ZCRPh2.pickle'        , '%s/%s/JetFake/hist.root' %(baseDir, plotDir), tag='egg_zcrph2', regions=regions )

def save_electron_hists( draw_str, plot_binning, plot_dir, hist_tag ) :

    samplesWelgg.Draw( 'pt_leadph12', draw_str, plot_binning )

    hist_data_egg = samplesWelgg.get_samples(name='Data')[0].hist.Clone('pt_leadph12_%s'%(hist_tag))
    save_hist( '%s/Data/hist.root' %(plot_dir), hist_data_egg )

    hist_sig_egg  = samplesWelgg.get_samples(name='Wgg')[0].hist.Clone('pt_leadph12_%s'%(hist_tag))
    save_hist( '%s/Wgg/hist.root' %(plot_dir), hist_sig_egg )

    hist_Zgg_egg     = samplesWelgg.get_samples(name='Zgg')[0].hist.Clone('pt_leadph12_%s'%(hist_tag))
    hist_ZggFSR_egg  = samplesWelgg.get_samples(name='ZgammagammaFSR')[0].hist.Clone('pt_leadph12_%s'%(hist_tag))
    hist_Zg_egg  = samplesWelgg.get_samples(name='Zgamma')[0].hist.Clone('pt_leadph12_%s'%(hist_tag))
    #hist_Top_egg  = samplesWelgg.get_samples(name='Top')[0].hist.Clone('pt_leadph12_%s'%(hist_tag))
    #hist_MB_egg  = samplesWelgg.get_samples(name='MultiBoson')[0].hist.Clone('pt_leadph12_%s'%(hist_tag))

    add_syst_to_hist( hist_Zgg_egg, 0.15 )
    add_syst_to_hist( hist_ZggFSR_egg, 0.15 )
    add_syst_to_hist( hist_Zg_egg, 0.15 )

    #hist_Zgg_egg.Add(hist_ZggFSR_egg)
    save_hist( '%s/ZggFSR/hist.root' %(plot_dir), hist_ZggFSR_egg )
    save_hist( '%s/Zgg/hist.root' %(plot_dir), hist_Zgg_egg )
    save_hist( '%s/Zg/hist.root' %(plot_dir), hist_Zg_egg )
    #save_hist( '%s/Top/hist.root' %(plot_dir), hist_Top_egg )
    #save_hist( '%s/MultiBoson/hist.root' %(plot_dir), hist_MB_egg )

def add_syst_to_hist( hist, syst ) :

    for bin in range( 1, hist.GetNbinsX() +1 ) :
        curr_err = hist.GetBinError( bin )
        curr_val = hist.GetBinContent( bin )
        new_err = math.sqrt( curr_err*curr_err + curr_val*syst*curr_val*syst )

        hist.SetBinError( bin, new_err )

def make_hist_from_pickle( sampMan, input_file, output_hist, tag, regions, syst=None ) :

    # get jet fake background estimate
    if not os.path.isfile( input_file) :
        print 'Could not find input file %s', input_file
        return

    ofile = open( input_file, 'r' )


    data = pickle.load(ofile)

    ofile.close()

    samp_list = sampMan.get_samples()
    sum_hist = None
    sum_data = {}
    for reg in regions :
        hist = None
        for s in samp_list :
            if s.hist is not None :
                hist = s.hist.Clone( 'pt_leadph12_%s_%s-%s' %(tag, reg[0], reg[1] ) )
                sum_hist = s.hist.Clone( 'pt_leadph12_%s' %(tag ) )
                break

        for ptbin in range( 1, hist.GetNbinsX()+1 ) :
            min = int(hist.GetXaxis().GetBinLowEdge(ptbin))
            max = int(hist.GetXaxis().GetBinUpEdge(ptbin))
            sum_data.setdefault(ptbin, ufloat(0, 0) )

            if max <= 15 :
                continue

            maxval = str(max)
            if max > 100 :
                maxval = 'max'

            databin = ( reg[0] ,reg[1], str( min), maxval )

            print databin

            print data
            print data['stat+syst']['sum'].keys()
            hist.SetBinContent( ptbin, data['stat+syst']['sum'][databin]['result'].n )
            hist.SetBinError( ptbin, data['stat+syst']['sum'][databin]['result'].s )

            sum_data[ptbin] = sum_data[ptbin] + data['stat+syst']['sum'][databin]['result']

        save_hist( output_hist, hist )

    for ptbin in range( 1, hist.GetNbinsX()+1 ) :
        sum_hist.SetBinContent( ptbin, sum_data[ptbin].n )
        sum_hist.SetBinError( ptbin, sum_data[ptbin].s )

    save_hist( output_hist, sum_hist )
    

def save_hist( file, hist) :

    dirname = os.path.split( file)[0] 
    if not os.path.isdir( dirname ) :
        os.makedirs( dirname) 
    ofile = ROOT.TFile.Open( file, 'UPDATE' )

    hist.Write()

    ofile.Close()


def get_mapped_directory( base_dir_jet, jet_dirs_key ) :
    
    jet_dir_key_map = {}

    for dir in os.listdir( base_dir_jet ) :
        res = re.match( jet_dirs_key, dir )
        if res is not None :
            if len(res.groups() ) == 3 :
                jet_dir_key_map[ ( int(res.group(1)), int(res.group(2)), int(res.group(3)) ) ]  = dir
            elif len(res.groups()) == 0 :
                jet_dir_key_map[ ( 0,0,0 ) ]  = dir


    return jet_dir_key_map

def get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key ) :

    jet_files = {}
    for dir in os.listdir( base_dir_jet ) :
        res = re.match( jet_dirs_key, dir )
        if res is not None :
            iso_key = None
            if len(res.groups() ) == 3 :
                iso_key = ( int(res.group(1)), int(res.group(2)), int(res.group(3)) )
            elif len(res.groups() ) == 0 :
                iso_key = ( 0,0,0 )

            jet_files[iso_key] = {}

            for file in os.listdir( base_dir_jet+'/'+dir  ) :
                fresl = re.match(file_key, file )
                if fresl is not None :
                    if len(fresl.groups()) == 4 :
                        jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4))] = file
                    elif len(fresl.groups()) == 7 :
                        # if the gropus exist, but they're both none, then treat it like there are 4 groups
                        if fresl.group(6) is None and  fresl.group(7) is None :
                            jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4))] = file
                        else :
                            jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3), fresl.group(4), fresl.group(6), fresl.group(7))] = file
                    elif len(fresl.groups()) == 3 :
                        jet_files[iso_key][( fresl.group(1), fresl.group(2), fresl.group(3))] = file

    return jet_files



def MakeEleBkgEstimate(base_dir_ele, base_dir_jet, file_bin_map, file_bin_map_syst, pt_bins, outputDir=None, el_selection='elfull', namePostfix='', coarse=False) :

    print '-----------------------------------'
    print 'START ELECTRON FAKE ESTMATE FOR %s' %el_selection
    print '-----------------------------------'

    el_acc = ['elfull', 'elzcr', 'elph1zcr', 'elph2zcr']
    if el_selection not in el_acc :
        print 'Input region not recognized, must be %s' %(','.join(el_acc) )
        return

    # Just use data samples
    samplesWggInvLead.deactivate_all_samples()
    samplesWggInvLead.activate_sample('Data')
    samplesWggInvSubl.deactivate_all_samples()
    samplesWggInvSubl.activate_sample('Data')

    regions = [('EB', 'EB'), ('EB' , 'EE'), ('EE', 'EB')]

    # get fake factors from nominal fits
    results_nom = get_ele_fakefactors( base_dir_ele, file_bin_map, regions, el_selection, coarse=coarse )
    # get fake factors from systematic fits
    results_syst = get_ele_fakefactors( base_dir_ele, file_bin_map_syst, regions, el_selection, coarse=coarse )

    results_comb = {'stat' : { 'lead' : {}, 'subl' : {}}, 'syst' : { 'lead' : {}, 'subl' : {}} , 'details' : { 'lead' : {}, 'subl' : {}} }
    for bin, res in results_nom['lead'].iteritems() :
        results_comb['stat']['lead'][bin] = res['pred']
        results_comb['details']['lead'][bin] = res
        if res['pred'] == 0 :
            results_comb['syst']['lead'][bin] = ufloat( res['pred'].n, res['pred'].n)
        else :
            results_comb['syst']['lead'][bin] = ufloat( res['pred'].n, math.fabs( (res['pred'].n - results_syst['lead'][bin]['pred'].n))/res['pred'].n)

    for bin, res in results_nom['subl'].iteritems() :
        results_comb['stat']['subl'][bin] = res['pred']
        results_comb['details']['subl'][bin] = res
        if res['pred'] == 0 :
            results_comb['syst']['subl'][bin] = ufloat( res['pred'].n, res['pred'].n)
        else :
            results_comb['syst']['subl'][bin] = ufloat( res['pred'].n, math.fabs( (res['pred'].n - results_syst['subl'][bin]['pred'].n))/res['pred'].n)

    file_key_lead = 'results__%sinvpixlead__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_subl = 'results__%sinvpixsubl__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_lead_syst = 'results__syst__%sinvpixlead__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    file_key_subl_syst = 'results__syst__%sinvpixsubl__(EB|EE)-(EB|EE)__pt_(\d+)-(\d+|max).pickle' %el_selection
    jet_dir_key_map = {}
    jet_dirs_key = 'JetFakeTemplateFitPlotsCorr(\d+)-(\d+)-(\d+)AsymIso'

    jet_dir_key_map = get_mapped_directory( base_dir_jet, jet_dirs_key )

    jet_files_lead      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead      )
    jet_files_subl      = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_subl      )
    jet_files_lead_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_lead_syst )
    jet_files_subl_syst = get_dirs_and_files( base_dir_jet, jet_dirs_key, file_key_subl_syst )

    print 'jet_files_lead'
    print jet_files_lead

    pt_bins_jetfile = [str(x) for x in pt_bins[:-1]]
    pt_bins_jetfile.append( 'max')
    #subl_ptbins = [ ( '70', 'max', '15', '25' ), ( '70', 'max', '25', 'max' ) ]
    subl_ptbins = [  ]
    pred_lead = get_jet_fake_results( jet_files_lead, jet_files_lead_syst, regions, pt_bins_jetfile, jet_dir_key_map, base_dir_jet,  pt_bins_subl=subl_ptbins ) 
    pred_subl = get_jet_fake_results( jet_files_subl, jet_files_subl_syst, regions, pt_bins_jetfile, jet_dir_key_map, base_dir_jet,  pt_bins_subl=subl_ptbins ) 

    # get fake factors and binning from file
    ff_man_coarse = FakeFactorManager( '%s/ElectronFakeFitsRatioCoarseEta/results.pickle' %base_dir_ele, ['fake_ratio'] )

    jet_scaled = {'stat' : {}, 'syst' : {} }
    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]


            ff_lead = -1
            ff_subl = -1
            if r1 == 'EB' :
                ff_lead = ff_man_coarse.get_pt_eta_ff( ptmin, ptmax, 0.0, 1.44 )
            if r1 == 'EE' :
                ff_lead = ff_man_coarse.get_pt_eta_ff( ptmin, ptmax, 1.57, 2.5 )

            if r2 == 'EB' :
                ff_subl = ff_man_coarse.get_pt_eta_ff( 15, ptmax, 0.0, 1.44 )
            if r2 == 'EE' :
                ff_subl = ff_man_coarse.get_pt_eta_ff( 15, ptmax, 1.57, 2.50 )


            bin = (r1,r2,ptmin,ptmax)
            jet_scaled['stat'][bin] = {'rf' : {}, 'fr' : {}, 'ff' : {} }
            jet_scaled['syst'][bin] = {'rf' : {}, 'fr' : {}, 'ff' : {} }

             
            jet_scaled['stat'][ bin ]['rf']['pred_lead'] = pred_lead['stat']['rf'][bin]['result']
            jet_scaled['stat'][ bin ]['fr']['pred_lead'] = pred_lead['stat']['fr'][bin]['result']
            jet_scaled['stat'][ bin ]['ff']['pred_lead'] = pred_lead['stat']['ff'][bin]['result']

            jet_scaled['stat'][ bin ]['rf']['pred_subl'] = pred_subl['stat']['rf'][bin]['result']
            jet_scaled['stat'][ bin ]['fr']['pred_subl'] = pred_subl['stat']['fr'][bin]['result']
            jet_scaled['stat'][ bin ]['ff']['pred_subl'] = pred_subl['stat']['ff'][bin]['result']

            jet_scaled['syst'][ bin ]['rf']['pred_lead'] = pred_lead['syst']['rf'][bin]['result']
            jet_scaled['syst'][ bin ]['fr']['pred_lead'] = pred_lead['syst']['fr'][bin]['result']
            jet_scaled['syst'][ bin ]['ff']['pred_lead'] = pred_lead['syst']['ff'][bin]['result']

            jet_scaled['syst'][ bin ]['rf']['pred_subl'] = pred_subl['syst']['rf'][bin]['result']
            jet_scaled['syst'][ bin ]['fr']['pred_subl'] = pred_subl['syst']['fr'][bin]['result']
            jet_scaled['syst'][ bin ]['ff']['pred_subl'] = pred_subl['syst']['ff'][bin]['result']

            jet_scaled['stat'][ bin ]['rf']['ff_lead'] = ff_lead
            jet_scaled['stat'][ bin ]['fr']['ff_lead'] = ff_lead
            jet_scaled['stat'][ bin ]['ff']['ff_lead'] = ff_lead

            jet_scaled['stat'][ bin ]['rf']['ff_subl'] = ff_subl
            jet_scaled['stat'][ bin ]['fr']['ff_subl'] = ff_subl
            jet_scaled['stat'][ bin ]['ff']['ff_subl'] = ff_subl

            # no additional FF syst at this point
            jet_scaled['syst'][ bin ]['rf']['ff_lead'] = ff_lead
            jet_scaled['syst'][ bin ]['fr']['ff_lead'] = ff_lead
            jet_scaled['syst'][ bin ]['ff']['ff_lead'] = ff_lead

            jet_scaled['syst'][ bin ]['rf']['ff_subl'] = ff_subl
            jet_scaled['syst'][ bin ]['fr']['ff_subl'] = ff_subl
            jet_scaled['syst'][ bin ]['ff']['ff_subl'] = ff_subl

            jet_scaled['stat'][ bin ]['rf']['total'] = jet_scaled['stat'][ bin ]['rf']['pred_lead']*jet_scaled['stat'][ bin ]['rf']['ff_lead'] + jet_scaled['stat'][ bin ]['rf']['pred_subl']*jet_scaled['stat'][ bin ]['rf']['ff_subl']
            jet_scaled['stat'][ bin ]['fr']['total'] = jet_scaled['stat'][ bin ]['fr']['pred_lead']*jet_scaled['stat'][ bin ]['fr']['ff_lead'] + jet_scaled['stat'][ bin ]['fr']['pred_subl']*jet_scaled['stat'][ bin ]['fr']['ff_subl']
            jet_scaled['stat'][ bin ]['ff']['total'] = jet_scaled['stat'][ bin ]['ff']['pred_lead']*jet_scaled['stat'][ bin ]['ff']['ff_lead'] + jet_scaled['stat'][ bin ]['ff']['pred_subl']*jet_scaled['stat'][ bin ]['ff']['ff_subl']


            jet_scaled['syst'][ bin ]['rf']['total'] = jet_scaled['syst'][ bin ]['rf']['pred_lead']*jet_scaled['syst'][ bin ]['rf']['ff_lead'] + jet_scaled['syst'][ bin ]['rf']['pred_subl']*jet_scaled['syst'][ bin ]['rf']['ff_subl']
            jet_scaled['syst'][ bin ]['fr']['total'] = jet_scaled['syst'][ bin ]['fr']['pred_lead']*jet_scaled['syst'][ bin ]['fr']['ff_lead'] + jet_scaled['syst'][ bin ]['fr']['pred_subl']*jet_scaled['syst'][ bin ]['fr']['ff_subl']
            jet_scaled['syst'][ bin ]['ff']['total'] = jet_scaled['syst'][ bin ]['ff']['pred_lead']*jet_scaled['syst'][ bin ]['ff']['ff_lead'] + jet_scaled['syst'][ bin ]['ff']['pred_subl']*jet_scaled['syst'][ bin ]['ff']['ff_subl']


    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins_jetfile[:-1]) :
            ptmax = pt_bins_jetfile[idx+1]
            print '%s-%s, pt %s-%s' %( r1, r2, ptmin, ptmax)

            bin = (r1,r2,ptmin,ptmax)

            print 'Jet fake, lead CR : rf = %s, fr = %s, ff = %s, sum = %s ' %( jet_scaled['stat'][bin]['rf']['pred_lead'], jet_scaled['stat'][bin]['fr']['pred_lead'], jet_scaled['stat'][bin]['ff']['pred_lead'], jet_scaled['stat'][bin]['rf']['pred_lead']+jet_scaled['stat'][bin]['fr']['pred_lead']+jet_scaled['stat'][bin]['ff']['pred_lead'])
            print 'Jet fake, subl CR : rf = %s, fr = %s, ff = %s, sum = %s ' %( jet_scaled['stat'][bin]['rf']['pred_subl'], jet_scaled['stat'][bin]['fr']['pred_subl'], jet_scaled['stat'][bin]['ff']['pred_subl'], jet_scaled['stat'][bin]['rf']['pred_subl']+jet_scaled['stat'][bin]['fr']['pred_subl']+jet_scaled['stat'][bin]['ff']['pred_subl'])

            print 'N jet fake lead*ff = %s' %((jet_scaled['stat'][bin]['rf']['pred_lead']+jet_scaled['stat'][bin]['fr']['pred_lead']+jet_scaled['stat'][bin]['ff']['pred_lead']) * ff_lead )
            print 'N jet fake subl*ff = %s' %((jet_scaled['stat'][bin]['rf']['pred_subl']+jet_scaled['stat'][bin]['fr']['pred_subl']+jet_scaled['stat'][bin]['ff']['pred_subl']) * ff_subl )
            print 'N data lead*ff = %s' %results_comb['stat']['lead'][bin]
            print 'N data subl*ff = %s' %results_comb['stat']['subl'][bin]
    
    results_subtracted = {'stat' : {'sum' : {}}, 'elesyst' : {'sum' : {}}, 'jetsyst' : {'sum' : {}}, 'stat+syst' : {'sum' : {}}, 'details' : {}}
    results_subtracted['details'] = results_comb['details']
    for bin, info_stat_lead in results_comb['stat']['lead'].iteritems() :
        info_stat_subl = results_comb['stat']['subl'][bin]
        info_syst_lead = results_comb['syst']['lead'][bin]
        info_syst_subl = results_comb['syst']['subl'][bin]

        results_subtracted['stat']['sum'][bin] = {}
        results_subtracted['elesyst']['sum'][bin] = {}
        results_subtracted['jetsyst']['sum'][bin] = {}
        results_subtracted['stat+syst']['sum'][bin] = {}

        results_subtracted['stat+syst']['sum'][bin]['lead'] = info_stat_lead
        results_subtracted['stat+syst']['sum'][bin]['subl'] = info_stat_subl
        results_subtracted['stat+syst']['sum'][bin]['jet_rf'] = jet_scaled['stat'][bin]['rf']
        results_subtracted['stat+syst']['sum'][bin]['jet_fr'] = jet_scaled['stat'][bin]['fr']
        results_subtracted['stat+syst']['sum'][bin]['jet_ff'] = jet_scaled['stat'][bin]['ff']

        results_subtracted['stat']['sum'][bin]['result'] = info_stat_lead +info_stat_subl - ( jet_scaled['stat'][bin]['rf']['total'] + jet_scaled['stat'][bin]['fr']['total'] + jet_scaled['stat'][bin]['ff']['total'] )

        # for elesyst set jet uncertainties to zero
        results_subtracted['elesyst']['sum'][bin]['result'] = info_syst_lead +info_syst_subl - ufloat( (jet_scaled['stat'][bin]['rf']['total'] + jet_scaled['stat'][bin]['fr']['total'] + jet_scaled['stat'][bin]['ff']['total']).n, 0.0 )

        # for jetsyst set ele uncertainties to zero
        results_subtracted['jetsyst']['sum'][bin]['result'] = ufloat( (info_stat_lead +info_stat_subl).n, 0.0) - ( jet_scaled['syst'][bin]['rf']['total'] + jet_scaled['syst'][bin]['fr']['total'] + jet_scaled['syst'][bin]['ff']['total'] )

        # for comb, set ele and jet values to zero but keep their uncertainties
        elesyst_to_add = ufloat( 0, results_subtracted['elesyst']['sum'][bin]['result'].s )
        jetsyst_to_add = ufloat( 0, results_subtracted['jetsyst']['sum'][bin]['result'].s )
        results_subtracted['stat+syst']['sum'][bin]['result']    = results_subtracted['stat']['sum'][bin]['result'] + elesyst_to_add + jetsyst_to_add

        print 'Ele pred Final %s-%s pt %s-%s = %s' %( bin[0], bin[1], bin[2], bin[3], results_subtracted['stat+syst']['sum'][bin]['result'] )



    #results_syst_subtracted = {}
    #results_syst_subtracted['stat+syst'] = {}
    #results_syst_subtracted['stat+syst']['sum'] = {}
    #for (r1,r2, ptmin, ptmax), val in results_syst.iteritems() :

    #    results_syst_subtracted['stat+syst']['sum'][bin] = {}

    #    results_syst_subtracted['stat+syst']['sum'][bin]['lead'] = info_lead
    #    results_syst_subtracted['stat+syst']['sum'][bin]['subl'] = info_subl
    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_rf'] = jet_scaled[bin]['rf']
    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_fr'] = jet_scaled[bin]['fr']
    #    results_syst_subtracted['stat+syst']['sum'][bin]['jet_ff'] = jet_scaled[bin]['ff']
    #    results_syst_subtracted['stat+syst']['sum'][bin]['result'] = info_lead['pred'] +info_subl['pred'] - ( jet_scaled[bin]['rf']['total'] + jet_scaled[bin]['fr']['total'] + jet_scaled[bin]['ff']['total'] )

    if outputDir is not None :
        if not os.path.isdir( outputDir ) :
            os.makedirs( outputDir )

        file_raw = open( outputDir + '/electron_fake_results%s__noJetFakeSubtraction.pickle' %namePostfix, 'w' )
        pickle.dump( results_nom, file_raw )
        file_raw.close()

        file_sub = open( outputDir + '/electron_fake_results%s.pickle' %namePostfix, 'w' )
        pickle.dump( results_subtracted, file_sub )
        file_sub.close()

        #file_sub_syst = open( outputDir + '/electron_fake_results_syst%s.pickle' %namePostfix, 'w' )
        #pickle.dump( results_syst_subtracted, file_sub_syst )
        #file_sub_syst.close()


def get_ele_fakefactors( base_dir_ele, file_bin_map, regions, el_selection, coarse=False ) :

    results = {}
    results['lead'] = {}
    results['subl'] = {}

    data_samp_invlead = samplesWggInvLead.get_samples( name='Data' )[0]
    data_samp_invsubl = samplesWggInvSubl.get_samples( name='Data' )[0]

    for r1, r2 in regions :

        # -----------------------------------
        # Lead CR draw string
        # draw once and make cuts
        # for all lead pt and eta
        # -----------------------------------
        draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 )' %(el_cuts[el_selection], r1, r2)

        samplesWggInvLead.create_hist(data_samp_invlead, 'pt_leadph12:fabs(eta_leadph12)', draw_str, ( 250, 0, 2.5, 20, 0, 100) )

        hist_lead = data_samp_invlead.hist.Clone('hist_lead__%s-%s' %(r1,r2))

        # -----------------------------------------
        # Get data counts in each pt and eta region
        # and multiply by the fake factor
        # -----------------------------------------
        for (leadptmin, leadptmax), file in file_bin_map.iteritems() :

            ff_man = FakeFactorManager( '%s/%s/results.pickle' %(base_dir_ele, file), ['fake_ratio'] )

            bin = (r1, r2, leadptmin, leadptmax)

            results['lead'][bin] = {}
            results['lead'][bin]['pred'] = ufloat(0, 0)

            eta_map = _eta_pt_bin_map
            if coarse :
                eta_map = _eta_pt_bin_map_coarse
            

            for etamin, etamax in eta_map[(leadptmin,leadptmax)][r1]  :


                # get the bins.  For the max bin subtract 1 because
                # you get the bin above the value
                leadptbinmin = hist_lead.GetYaxis().FindBin( float(leadptmin) )
                if leadptmax == 'max' :
                    leadptbinmax = hist_lead.GetNbinsY()
                else :
                    leadptbinmax = hist_lead.GetYaxis().FindBin( float(leadptmax) ) - 1

                leadetabinmin = hist_lead.GetXaxis().FindBin( float(etamin) )
                leadetabinmax = hist_lead.GetXaxis().FindBin( float(etamax) ) - 1

                dataerr = ROOT.Double()
                nData = hist_lead.IntegralAndError( leadetabinmin, leadetabinmax, leadptbinmin, leadptbinmax, dataerr )

                data = ufloat( nData, dataerr )

                ff = ff_man.get_pt_eta_ff( leadptmin, leadptmax, etamin, etamax )

                print 'LEAD : ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptbinmax = %d, etabinmin = %d, etabinmax = %d, data = %s, ff = %s, pred = %s ' %( leadptmin, leadptmax, etamin, etamax, leadptbinmin, leadptbinmax, leadetabinmin, leadetabinmax, data, ff, data*ff )

                ff_bin = ( str(etamin), str(etamax), leadptmin, leadptmax )

                results['lead'][bin][ff_bin] = {}
                results['lead'][bin][ff_bin]['data'] = data
                results['lead'][bin][ff_bin]['ff'] = ff
                results['lead'][bin][ff_bin]['pred'] = results['lead'][bin][ff_bin]['data']*(results['lead'][bin][ff_bin]['ff'] )
                #results['lead'][bin][ff_bin]['pred'] = results['lead'][bin][ff_bin]['data']*(results['lead'][bin][ff_bin]['ff']/(1-results['lead'][bin][ff_bin]['ff']) )

                # sum the results
                results['lead'][bin]['pred'] = results['lead'][bin]['pred'] + results['lead'][bin][ff_bin]['pred']
                print 'Update results ', results['lead'][bin]['pred']
            # -----------------------------------------
            # Subl control region
            # Get data counts in each pt and eta region
            # and multiply by the fake factor
            # the sublead pT range starts at 15
            # and goes to the maximum lead pt
            # -----------------------------------------
            bin = (r1, r2, leadptmin, leadptmax)
            results['subl'][bin] = {}
            results['subl'][bin]['pred'] = ufloat(0, 0)


            # -----------------------------------
            # Subl CR draw string
            # draw once for each lead pT bin and make cuts
            # for all sublead pt and eta
            # -----------------------------------

            if leadptmax == 'max' :
                draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %s )' %(el_cuts[el_selection], r1, r2, leadptmin)
            else :
                draw_str = ' PUWeight * ( %s && is%s_leadph12 && is%s_sublph12 && pt_leadph12 > %s && pt_leadph12 < %s )' %(el_cuts[el_selection], r1, r2, leadptmin, leadptmax)
            samplesWggInvSubl.create_hist(data_samp_invsubl, 'pt_sublph12:fabs(eta_sublph12)', draw_str,  (250, 0, 2.5, 20, 0, 100) )

            hist_subl = data_samp_invsubl.hist.Clone('hist_subl__%s-%s_leadpt%s-%s' %(r1,r2, leadptmin, leadptmax))

            for (sublptmin, sublptmax) in file_bin_map.keys() :

                # the sublead photon pT will
                # always be smaller than the lead pT
                if sublptmax == 'max' :
                    if leadptmax != 'max' :
                        continue
                else :
                    if not leadptmax =='max' :
                        if sublptmax > leadptmax :
                            continue

                # the sublead photon should run from 15 to the max lead pt bin
                # use the global binning for this
                for subletamin, subletamax in eta_map[(sublptmin,sublptmax)][r2] :


                    sublptbinmin = hist_subl.GetYaxis().FindBin( float(sublptmin) )
                    if sublptmax == 'max' :
                        sublptbinmax = hist_subl.GetNbinsY()
                    else :
                        sublptbinmax = hist_subl.GetYaxis().FindBin( float(sublptmax) ) - 1

                    subletabinmin = hist_subl.GetXaxis().FindBin( float(subletamin) )
                    subletabinmax = hist_subl.GetXaxis().FindBin( float(subletamax) ) - 1

                    dataerr = ROOT.Double()
                    nData = hist_subl.IntegralAndError( subletabinmin, subletabinmax, sublptbinmin, sublptbinmax, dataerr )

                    data = ufloat( nData, dataerr )

                    ff = ff_man.get_pt_eta_ff( sublptmin, sublptmax, subletamin, subletamax )

                    print 'Sublead : leadptmin = %s, leadptmax = %s, ptmin = %s, ptmax = %s, etamin = %f, etamax = %f, ptbinmin = %d, ptbinmax = %d, etabinmin = %d, etabinmax = %d, data = %s, ff= %s, pred = %s ' %(leadptmin, leadptmax, sublptmin, sublptmax, subletamin, subletamax, sublptbinmin, sublptbinmax, subletabinmin, subletabinmax, data, ff, data*ff )

                    ff_bin = ( str(subletamin), str(subletamax), str(sublptmin), str(sublptmax) )

                    results['subl'][bin][ff_bin] = {}
                    results['subl'][bin][ff_bin]['data'] = data
                    results['subl'][bin][ff_bin]['ff'] =  ff
                    results['subl'][bin][ff_bin]['pred'] = results['subl'][bin][ff_bin]['data']*results['subl'][bin][ff_bin]['ff']
                    #results['subl'][bin][ff_bin]['pred'] = results['subl'][bin][ff_bin]['data']*(results['subl'][bin][ff_bin]['ff']/(1-results['subl'][bin][ff_bin]['ff']) )

                    results['subl'][bin]['pred'] = results['subl'][bin]['pred'] +results['subl'][bin][ff_bin]['pred']

    for bin, res in results['lead'].iteritems() :
        print 'Invert LEAD bin : %s, predicted = %s' %( bin, res['pred'] )
    for bin, res in results['subl'].iteritems() :
        print 'Invert SUBL bin : %s, predicted = %s' %( bin, res['pred'] )

    return results


def get_jet_fake_results( jet_files, jet_files_syst, regions, pt_bins,  jet_dir_key_map, base_dir_jet, pt_bins_subl=[] ) :
    """ Get the fake results for all pt and eta regions 
    
        Check if the data counts that were input to the 
        fit are non-zero.  If so, move to a looser isolation.
        If the values are never set, ie even in the loosest
        case there are no data counts, then use the 
        original with zero values
    """

    results = {'stat' : {}, 'syst' : {}, 'stat+syst' : {} }
    for val in results.values() :
       val['rf'] = {}
       val['fr'] = {}
       val['ff'] = {}
       val['sum'] = {}


    sorted_jet_dirs = jet_files.keys()
    sorted_jet_dirs.sort()

    for r1, r2 in regions :

        for idx, ptmin in enumerate(pt_bins[:-1]) :
            ptmax = pt_bins[idx+1]

            reg_bin = (r1, r2, ptmin, ptmax) 

            make_background_estimate( base_dir_jet, jet_files, jet_files_syst, jet_dir_key_map, sorted_jet_dirs, reg_bin, results )

        for ptlmin, ptlmax, ptsmin, ptsmax in pt_bins_subl :

            reg_bin = (r1, r2, ptlmin, ptlmax, ptsmin, ptsmax )

            make_background_estimate( base_dir_jet, jet_files, jet_files_syst, jet_dir_key_map, sorted_jet_dirs, reg_bin, results )

    return results

def make_background_estimate( base_dir_jet, jet_files, jet_files_syst, jet_dir_key_map, sorted_jet_dirs, reg_bin, results ) :

    for val in results.values() :
        val['rf'][reg_bin] = {}
        val['fr'][reg_bin] = {}
        val['ff'][reg_bin] = {}
        val['sum'][reg_bin] = {}

    for dir_key in sorted_jet_dirs :
        
        fentries = jet_files[dir_key]
        fentries_syst = jet_files_syst[dir_key]

        if reg_bin not in fentries :

            print 'Bin not found', reg_bin
            print fentries
            print jet_files
            continue

        # get the file 
        sub_dir_jet = jet_dir_key_map[dir_key]

        file_loc = base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin]

        if not os.path.isfile( file_loc ) :
            continue

        ofile = open(file_loc)
        predictions = pickle.load(ofile)
        ofile.close()

        file_loc_syst = base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin]
        ofile = open(file_loc_syst)
        predictions_syst = pickle.load(ofile)
        ofile.close()

        # get the data
        Ndata_tt = predictions['Ndata_TT']
        Ndata_tl = predictions['Ndata_TL']
        Ndata_lt = predictions['Ndata_LT']
        Ndata_ll = predictions['Ndata_LL']

        if Ndata_tl == 0 or Ndata_lt == 0 or Ndata_ll == 0 :
            print 'No data entries for AsymIso %d-%d-%d, region %s-%s, pt %s-%s ' %( dir_key[0], dir_key[1], dir_key[2], reg_bin[0], reg_bin[1], reg_bin[2], reg_bin[3])
            print 'Ndata_tl = %s, Ndata_lt = %s, Ndata_ll = %s' %( Ndata_tl, Ndata_lt, Ndata_ll)
            continue

        Npred_rf = predictions['Npred_RF_TT']
        Npred_fr = predictions['Npred_FR_TT']
        Npred_ff = predictions['Npred_FF_TT']

        Npred_rf_syst = predictions_syst['Npred_RF_TT']
        Npred_fr_syst = predictions_syst['Npred_FR_TT']
        Npred_ff_syst = predictions_syst['Npred_FF_TT']

        results['stat']['rf'][reg_bin]['result'] = Npred_rf
        results['stat']['fr'][reg_bin]['result'] = Npred_fr
        results['stat']['ff'][reg_bin]['result'] = Npred_ff

        syst_asym = _asym_iso_syst[(dir_key[0], dir_key[1], dir_key[2])]

        results['syst']['rf'][reg_bin]['result'] = Npred_rf_syst* ufloat( 1.0, syst_asym )
        results['syst']['fr'][reg_bin]['result'] = Npred_fr_syst* ufloat( 1.0, syst_asym )
        results['syst']['ff'][reg_bin]['result'] = Npred_ff_syst* ufloat( 1.0, syst_asym )

        pred_sum = Npred_ff+Npred_rf+Npred_fr
        pred_sum_syst = results['syst']['rf'][reg_bin]['result']+results['syst']['fr'][reg_bin]['result']+results['syst']['ff'][reg_bin]['result']

        if Ndata_tt > 0 and pred_sum.n > Ndata_tt.n :
            raw_input('cont')
            print 'Changing prediction from %s to %s' %( pred_sum, ufloat( Ndata_tt.n, (pred_sum.s/pred_sum.n)*Ndata_tt.n ) )
            pred_sum = ufloat( Ndata_tt.n, (pred_sum.s/pred_sum.n)*Ndata_tt.n )
            pred_sum_syst = ufloat( Ndata_tt.n, (pred_sum_syst.s/pred_sum_syst.n)*Ndata_tt.n )


        results['stat']['sum'][reg_bin]['result'] = pred_sum
        results['syst']['sum'][reg_bin]['result'] = pred_sum_syst

        Npred_rf_tot = Npred_rf
        Npred_fr_tot = Npred_fr
        Npred_ff_tot = Npred_ff

        Npred_rf_syst_zero =ufloat( 0, results['syst']['rf'][reg_bin]['result'].s )
        Npred_fr_syst_zero =ufloat( 0, results['syst']['fr'][reg_bin]['result'].s )
        Npred_ff_syst_zero =ufloat( 0, results['syst']['ff'][reg_bin]['result'].s )

        # do sum for stat+syst
        Npred_rf_tot += Npred_rf_syst_zero
        Npred_fr_tot += Npred_fr_syst_zero
        Npred_ff_tot += Npred_ff_syst_zero
        
        results['stat+syst']['rf'][reg_bin]['result'] = Npred_rf_tot
        results['stat+syst']['fr'][reg_bin]['result'] = Npred_fr_tot
        results['stat+syst']['ff'][reg_bin]['result'] = Npred_ff_tot
        results['stat+syst']['sum'][reg_bin]['result'] = results['stat+syst']['rf'][reg_bin]['result'] + results['stat+syst']['fr'][reg_bin]['result'] + results['stat+syst']['ff'][reg_bin]['result']

        break

    # if results weren't set in any cases above, 
    # get the results from the first entry
    if not results['stat']['rf'][reg_bin] or not results['stat']['fr'][reg_bin] or not results['stat']['ff'][reg_bin] :

        if reg_bin not in fentries :
            print 'Bin not found', reg_bin
            return

        dir_key = sorted_jet_dirs[0]

        fentries = jet_files[dir_key]

        sub_dir_jet = jet_dir_key_map[dir_key]

        file_loc = base_dir_jet + '/' + sub_dir_jet +'/' + fentries[reg_bin]
        if not os.path.isfile( file_loc ) :
            print 'Could not locate file ', file_loc
            return
        ofile = open(file_loc)
        predictions = pickle.load(ofile)
        ofile.close()

        ofile = open(base_dir_jet + '/' + sub_dir_jet +'/' + fentries_syst[reg_bin])
        predictions_syst = pickle.load(ofile)
        ofile.close()

        Npred_rf = predictions['Npred_RF_TT']
        Npred_fr = predictions['Npred_FR_TT']
        Npred_ff = predictions['Npred_FF_TT']

        syst_asym = _asym_iso_syst[(dir_key[0], dir_key[1], dir_key[2])]

        Npred_rf_syst = predictions_syst['Npred_RF_TT']
        Npred_fr_syst = predictions_syst['Npred_FR_TT']
        Npred_ff_syst = predictions_syst['Npred_FF_TT']

        results['stat']['rf'][reg_bin]['result'] = Npred_rf
        results['stat']['fr'][reg_bin]['result'] = Npred_fr
        results['stat']['ff'][reg_bin]['result'] = Npred_ff
        results['stat']['sum'][reg_bin]['result'] = Npred_ff+Npred_rf+Npred_fr

        results['syst']['rf'][reg_bin]['result'] = Npred_rf_syst* ufloat( 1.0, syst_asym )
        results['syst']['fr'][reg_bin]['result'] = Npred_fr_syst* ufloat( 1.0, syst_asym )
        results['syst']['ff'][reg_bin]['result'] = Npred_ff_syst* ufloat( 1.0, syst_asym )
        results['syst']['sum']['raw_asym'] = syst_asym
        results['syst']['sum'][reg_bin]['result'] = results['syst']['rf'][reg_bin]['result'] + results['syst']['fr'][reg_bin]['result'] + results['syst']['ff'][reg_bin]['result']

        Npred_rf_tot = Npred_rf
        Npred_fr_tot = Npred_fr
        Npred_ff_tot = Npred_ff

        Npred_rf_syst_zero =ufloat( 0, results['syst']['rf'][reg_bin]['result'].s )
        Npred_fr_syst_zero =ufloat( 0, results['syst']['fr'][reg_bin]['result'].s )
        Npred_ff_syst_zero =ufloat( 0, results['syst']['ff'][reg_bin]['result'].s )

        Npred_rf_tot += Npred_rf_syst_zero
        Npred_fr_tot += Npred_fr_syst_zero
        Npred_ff_tot += Npred_ff_syst_zero
        
        results['stat+syst']['rf'][reg_bin]['result'] = Npred_rf_tot
        results['stat+syst']['fr'][reg_bin]['result'] = Npred_fr_tot
        results['stat+syst']['ff'][reg_bin]['result'] = Npred_ff_tot
        results['stat+syst']['sum'][reg_bin]['result'] = Npred_rf_tot+Npred_fr_tot+Npred_ff_tot

if __name__ == '__main__' :
    main()
