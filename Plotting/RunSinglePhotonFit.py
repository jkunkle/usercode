"""
Plot 
"""
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
import collections
import pickle
import time
from uncertainties import ufloat
from uncertainties import unumpy

from SampleManager import SampleManager
from SampleManager import Sample
from RunMatrixFit import draw_template

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('--baseDir',      default=None,           dest='baseDir',         help='Path to base directory containing all ntuples')
p.add_argument('--fileName',     default='ntuple.root',  dest='fileName',        help='( Default ntuple.root ) Name of files')
p.add_argument('--treeName',     default='events'     ,  dest='treeName',        help='( Default events ) Name tree in root file')
p.add_argument('--samplesConf',  default=None,           dest='samplesConf',     help=('Use alternate sample configuration. '
                                                                                       'Must be a python file that implements the configuration '
                                                                                       'in the same manner as in the main() of this script.  If only '
                                                                                       'the file name is given it is assumed to be in the same directory '
                                                                                       'as this script, if a path is given, use that path' ) )

                                                                                       
p.add_argument('--xsFile',     default=None,  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--readHists',     default=False,action='store_true',   dest='readHists',         help='read histograms from root files instead of trees')
p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')
p.add_argument('--syst_file',     default=None,  type=str ,        dest='syst_file',         help='Location of systematics file')

p.add_argument('--nom', default=False, action='store_true', dest='nom', help='run nom' )
p.add_argument('--loose', default=False, action='store_true', dest='loose', help='run loose' )
p.add_argument('--asym533', default=False, action='store_true', dest='asym533', help='run asym533' )
p.add_argument('--asym855', default=False, action='store_true', dest='asym855', help='run asym855' )
p.add_argument('--asym1077', default=False, action='store_true', dest='asym1077', help='run asym1077' )
p.add_argument('--asym1299', default=False, action='store_true', dest='asym1299', help='run asym1299' )
p.add_argument('--asym151111', default=False, action='store_true', dest='asym151111', help='run asym151111' )
p.add_argument('--asym201616', default=False, action='store_true', dest='asym201616', help='run asym201616' )
p.add_argument('--asymcorr533', default=False, action='store_true', dest='asymcorr533', help='run asymcorr533' )
p.add_argument('--asymcorr855', default=False, action='store_true', dest='asymcorr855', help='run asymcorr855' )
p.add_argument('--asymcorr1077', default=False, action='store_true', dest='asymcorr1077', help='run asymcorr1077' )
p.add_argument('--asymcorr1299', default=False, action='store_true', dest='asymcorr1299', help='run asymcorr1299' )
p.add_argument('--asymcorr151111', default=False, action='store_true', dest='asymcorr151111', help='run asymcorr151111' )
p.add_argument('--asymcorr201616', default=False, action='store_true', dest='asymcorr201616', help='run asymcorr201616' )
p.add_argument('--channel', default='mu',  dest='channel', help='run this channel' )

options = p.parse_args()


if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
else :
    ROOT.gROOT.SetBatch(False)

sampMan = None
sampManFit = None

def get_default_draw_commands(ch='mu' ) :

    real_fake_cmds = {
                      'real' :'mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 ' , 
                      'fake' :'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ',
                      'fakewin' :'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] ',
                      'realwin' :'mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] ',

    }
    if ch=='mu' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && el_n==0 && m_leplep>60 && m_leplepph > 105' }
    elif ch=='mu_tp_eveto' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && el_n==0 && m_leplep>76 && m_leplep < 106' }
    elif ch=='mu_tp_eveto_loose' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && el_n==0 && m_leplep>71 && m_leplep < 111' }
    elif ch=='mu_tp_eveto_tight' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && el_n==0 && m_leplep>81 && m_leplep < 101' }
    elif ch=='mu_tp_medium' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoSIEIENoEleVeto_n==1 && leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4 && el_n==0 && m_leplep>76 && m_leplep < 106' }
    elif ch=='mu_tp_medium_loose' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoSIEIENoEleVeto_n==1 && leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4 && el_n==0 && m_leplep>71 && m_leplep < 111' }
    elif ch=='mu_tp_medium_tight' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 && ph_mediumNoSIEIENoEleVeto_n==1 && leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4 && el_n==0 && m_leplep>81 && m_leplep < 101' }
    elif ch=='murealcr' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==2 leadPhot_leadLepDR>0.4  && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && el_n==0 && m_leplep>60 && m_leplepph > 81 && m_leplepph < 101' }
    elif ch == 'el' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==2 && leadPhot_leadLepDR>0.4 && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && mu_n==0 && m_leplep>60 && m_leplepph > 105',}
    elif ch == 'elrealcr' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==2 && leadPhot_leadLepDR>0.4 && leadPhot_sublLepDR>0.4 && ph_hasPixSeed[0]==0 && mu_n==0 && m_leplep>60 && m_leplepph > 81 && m_leplepph < 101',}
    elif ch=='muw' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && leadPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_lep_met > 80',}
    elif ch=='muw_tp_medium' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && leadPhot_leadLepDR>0.4 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_lep_met > 60',}
    elif ch=='muw_tp_eveto' :
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && ph_hasPixSeed[0] == 0 && leadPhot_leadLepDR>0.4 && ph_HoverE12[0] < 0.05 && el_n==0 && mt_lep_met > 60',}
    elif ch=='elw' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 &&  leadPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && mu_n==0 && mt_lep_met > 80',}
    elif ch == 'elwzcr' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 &&  leadPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && mu_n==0 && m_lepph1 > 76 && m_lepph1 < 106 ',}
    elif ch == 'elwinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 &&  leadPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==1 && ph_HoverE12[0] < 0.05 && mu_n==0 ',}
    elif ch == 'elwzcrinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 &&  leadPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==1 && ph_HoverE12[0] < 0.05 && mu_n==0 && m_lepph1 > 76 && m_lepph1 < 106 ',}

    real_fake_cmds.update(gg_cmds)

    return real_fake_cmds

def get_default_samples(ch='mu' ) :

    if ch.count('mu') :
        return { 'real' : {'Data' : 'Wgamma'}, 'fake' : {'Data' : 'Muon', 'Background' : 'RealPhotonsZg'}, 'target' : 'Muon' }
    elif ch.count('el') :
        return { 'real' : {'Data' : 'Wgamma'}, 'fake' : {'Data' : 'Muon', 'Background' : 'RealPhotonsZg'}, 'target' : 'Electron' }

def get_default_binning(var='sigmaIEIE') :

    if var == 'sigmaIEIE' :
        return { 'EB' : (30, 0, 0.03), 'EE' : (200, 0, 0.1) }
    elif var == 'chIsoCorr' :
        return { 'EB' : (30, 0, 45), 'EE' : (35, 0, 42) }
    elif var == 'neuIsoCorr' :
        return { 'EB' : (40, -2, 38), 'EE' : (30, -2, 43) }

_sieie_cuts  = { 'EB' : 0.011, 'EE' : 0.033 }
_chIso_cuts  = { 'EB' : 1.5, 'EE' : 1.2 }
_neuIso_cuts = { 'EB' : 1.0, 'EE' : 1.5 }
_phoIso_cuts = { 'EB' : 0.7, 'EE' : 1.0 }

def get_default_cuts(var='sigmaIEIE') :

    if var == 'sigmaIEIE' :

        return { 'EB' : { 'tight' : ( 0, _sieie_cuts['EB']-0.0001  ), 'loose' : ( _sieie_cuts['EB']+0.0001, 0.0299 ) },
                 'EE' : { 'tight' : ( 0, _sieie_cuts['EE']-0.0001 ), 'loose' : (  _sieie_cuts['EE']+0.0001, 0.099 ) } 
               }
    elif var == 'chIsoCorr' :
        return { 'EB' : { 'tight' : ( 0, 1.5-0.01  ), 'loose' : ( 1.5001, 45 ) },
                 'EE' : { 'tight' : ( 0, 1.2-0.01 ), 'loose' : ( 1.2001, 42 ) } 
               }
    elif var == 'neuIsoCorr' :
        return { 'EB' : { 'tight' : ( -2, 1.0-0.01  ), 'loose' : ( 1.0001, 40 ) },
                 'EE' : { 'tight' : ( -2, 1.5-0.01 ), 'loose' : ( 1.5001, 45 ) } 
               }


syst_uncertainties={}
def get_syst_uncertainty( type, reg, ptrange, real_fake, tight_loose ) :

    # Put these in by hand, may be necessary to load later
    if type.count( 'Background' ) :
        #use a flat 15% uncertainty for now
        return 0.15

    if not syst_uncertainties :
        print 'Systematics not loaded!  Use --syst_file to provide systematics file'
        return 0.0

    type_data = syst_uncertainties.get( type, None )
    if type_data is None :
        print 'no systematics available for %s' %type
        raw_input('con')
        return 0.0

    reg_data = type_data.get( reg, None )

    if reg_data is None :
        print 'No systematics available for region %s' %reg
        raw_input('con')
        return 0.0

    syst_ptrange = ( str(ptrange[0]), str(ptrange[1]) )
    if ptrange[0] is None :
        syst_ptrange = (None,None)
    elif ptrange[1] is None :
        syst_ptrange = (str(ptrange[0]), 'max')

    pt_data = reg_data.get(syst_ptrange, None)
    if pt_data is None :
        print 'No systematics available for pt range ', syst_ptrange
        raw_input('con')
        return 0.0

    return reg_data[syst_ptrange]

             
def main() :

    global sampMan
    global sampManFit

    base_dir = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2014_12_23/'
    fit_dir  = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaNoPhID_2014_12_23/'

    sampMan    = SampleManager(base_dir, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    sampManFit = SampleManager(fit_dir, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)


    if options.samplesConf is not None :

        sampMan.ReadSamples( options.samplesConf )
        sampManFit.ReadSamples( options.samplesConf )

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

    #RunClosureFitting( outputDir = None )

    if options.syst_file is not None :
        load_syst_file( options.syst_file )

    if options.nom :
        RunNomFitting( outputDir = options.outputDir, ch=options.channel)

def load_syst_file( file ) :

    global syst_uncertainties

    ofile = open( file ) 
    syst_uncertainties = pickle.load(ofile)

    ofile.close()

def RunNomFitting( outputDir = None, ch='mu') :

    outputDirNom = None
    if outputDir is not None :
        outputDirNom = outputDir + '/SinglePhotonResults/JetSinglePhotonFakeNomIso'
        #outputDirNom = outputDir + '/SinglePhotonResults/ChHadIsoFits/JetSinglePhotonFakeNomIso'

    ptbins = [15, 25, 40, 70, 1000000 ]
    #ptbins = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 100, 1000000 ]

    iso_cuts_full = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    fitvar = 'sigmaIEIE'

    #iso_cuts_full = 'ph_passSIEIEMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    #fitvar = 'chIsoCorr'

    do_nominal_fit( iso_cuts_full, ptbins=ptbins, fitvar=fitvar, ch=ch, outputDir = outputDirNom, systematics='Nom')

    #iso_cuts = 'ph_chIsoCorr[0] < 8 && ph_neuIsoCorr[0] < 5 && ph_phoIsoCorr[0] < 5'
    #asym_cuts = [(5,3,3), (8,5,5), (10,7,7), (12,9,9), (15,11,11), (20, 16, 16) ]
    #for cuts in asym_cuts :
    #    iso_cuts = 'ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d' %cuts
    #    outputDirAsym=None
    #    if outputDir is not None :
    #        outputDirAsym = outputDir + '/SinglePhotonResults/JetSinglePhotonFakeAsymIso%d-%d-%d' %cuts

    #    do_nominal_fit( iso_cuts, ptbins=ptbins, ch=ch, outputDir = outputDirAsym, systematics='Nom', iso_cuts_data=iso_cuts)


#def RunAsymFittingLoose(vals, outputDir = None, ch='mu') :
#
#    outputDirNom = None
#    if outputDir is not None :
#        outputDirNom = outputDir + '/JetFakeTemplateFitPlotsLoose%d-%d-%dAsymIso'%(vals[0], vals[1], vals[2] )
#
#    iso_cuts_iso = ' ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
#    iso_cuts_noiso = ' ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d' %(vals[0], vals[1], vals[2] )
#
#    ptbins = [15, 25, 40, 80, 1000000 ]
#
#    do_asymiso_fit( iso_cuts_iso, iso_cuts_noiso, ptbins=ptbins, ch=ch, outputDir=outputDirNom )
#
#def RunCorrectedAsymFitting(vals, outputDir = None, ch='mu') :
#
#    outputDirNom = None
#    if outputDir is not None :
#        outputDirNom = outputDir + '/JetFakeTemplateFitPlotsCorr%d-%d-%dAsymIso'%(vals[0], vals[1], vals[2] )
#
#    iso_cuts_iso = ' ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
#    iso_cuts_noiso = ' ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d' %(vals[0], vals[1], vals[2] )
#
#    ptbins = [15, 20, 25, 30, 40, 50, 70, 1000000 ]
#
#    do_corrected_asymiso_fit( iso_cuts_iso, iso_cuts_noiso, ptbins=ptbins, ch=ch, outputDir=outputDirNom, systematics=('-'.join([str(v) for v in vals])) )

def do_nominal_fit( iso_cuts, ptbins=[], subl_ptrange=(None,None), fitvar='sigmaIEIE', ch='mu', outputDir=None, systematics=None, iso_cuts_data=None ) :

    binning = get_default_binning(var=fitvar)
    samples = get_default_samples(ch)

    # generate templates for both EB and EE
    real_template_str = get_default_draw_commands(ch )['real'] + ' && %s' %iso_cuts
    #real_template_str = get_default_draw_commands(ch )['realwin'] 
    #fake_template_str = get_default_draw_commands(ch )['fakewin'] 
    fake_template_str = get_default_draw_commands(ch )['fake']  + ' && %s' %iso_cuts

    templates_reg = {}
    templates_reg['EB'] = {}
    templates_reg['EE'] = {}
    templates_reg['EB']['real'] = get_single_photon_template(real_template_str, binning['EB'], samples['real'], 'EB', fitvar=fitvar, real=True)
    templates_reg['EE']['real'] = get_single_photon_template(real_template_str, binning['EE'], samples['real'], 'EE', fitvar=fitvar, real=True)
    templates_reg['EB']['fake'] = get_single_photon_template(fake_template_str, binning['EB'], samples['fake'], 'EB', fitvar=fitvar, real=False)
    templates_reg['EE']['fake'] = get_single_photon_template(fake_template_str, binning['EE'], samples['fake'], 'EE', fitvar=fitvar, real=False)

    regions = [ 'EB', 'EE' ]
    for reg in regions :

        # convert from regions to lead/subl
        templates = {}
        templates['lead'] = {}
        templates['lead']['real'] = templates_reg[reg]['real']
        templates['lead']['fake'] = templates_reg[reg]['fake']

        # add regions onto the selection
        #gg_selection = get_default_draw_commands(ch)['gg'] + ' && ph_mediumNoSIEIE_n > 0 && ph_Is%s[0]' %( reg)
        gg_selection = get_default_draw_commands(ch)['gg'] + ' && ph_n > 0 && ph_Is%s[0]' %( reg)
        if iso_cuts_data is not None :
            gg_selection = gg_selection + ' && %s ' %( iso_cuts_data )
        elif iso_cuts is not None :
            gg_selection = gg_selection + ' && %s ' %( iso_cuts )

        # parse out the x and y binning
        xbinn = binning[reg]

        # variable given to TTree.Draw
        var = 'ph_pt[0]:ph_%s[0]'%fitvar #y:x

        # get sample
        target_samp = sampManFit.get_samples(name=samples['target'])

        # draw and get back the hist
        gg_hist = clone_sample_and_draw( target_samp[0], var, gg_selection, ( xbinn[0], xbinn[1], xbinn[2], 100, 0, 500) )

        # -----------------------
        # inclusive result
        # -----------------------

        # project data hist
        gg_hist_inclusive = gg_hist.ProjectionX( 'px' )

        templates_inclusive = get_projected_templates( templates, lead_ptrange =(None,None) )

        (results_inclusive_stat, results_inclusive_syst) = run_photon_fit(templates_inclusive, gg_hist_inclusive, reg, fitvar=fitvar, lead_ptrange=(None,None), outputDir=outputDir, outputPrefix='__%s'%ch, systematics=systematics )

        namePostfix = '__%s__%s' %( ch, reg )
        save_templates( templates_inclusive, outputDir, lead_ptrange=(None,None), namePostfix=namePostfix )
        save_results( results_inclusive_stat, outputDir, namePostfix )

        namePostfix_syst = '__syst%s' %namePostfix
        save_results( results_inclusive_syst, outputDir, namePostfix_syst )

        # -----------------------
        # pt binned results
        # -----------------------
        for idx, ptmin in enumerate(ptbins[:-1] ) :
            ptmax = ptbins[idx+1]

            # put lead range together (expected by following code)
            if ptmax == ptbins[-1] : 
                # if we're in the last bin, move the min pt down one
                lead_ptrange_templates = ( ptbins[idx-1], None )
                lead_ptrange = ( ptmin, None )
            else :
                lead_ptrange = ( ptmin, ptmax )
                lead_ptrange_templates = ( ptmin, ptmax )

            print 'ptmin = %d, ptmax = %d, Min Z bin = %d, max Z bin = %d' %( ptmin, ptmax, gg_hist.GetZaxis().FindBin( ptmin), gg_hist.GetZaxis().FindBin( ptmax )-1 )

            # project data hist
            gg_hist_pt = gg_hist.ProjectionX( 'px_%d_%d' %( ptmin, ptmax), gg_hist.GetYaxis().FindBin( ptmin), gg_hist.GetYaxis().FindBin( ptmax )-1 )
                
            # get templates
            # if in the last pt bin, use the 
            # second to last template
            templates_pt = get_projected_templates( templates, lead_ptrange=lead_ptrange_templates ) 

            #if ptmax == ptbins[-1] :
            #    templates_pt_prev = get_projected_templates( templates, lead_ptrange=(ptbins[idx-1], ptbins[idx] ) )
            #    for key, val in templates_pt_prev['lead']['fake'].iteritems() :
            #        templates_pt['lead']['fake'][key] = val

            # get results
            (results_pt_stat, results_pt_syst) = run_photon_fit(templates_pt, gg_hist_pt, reg, fitvar=fitvar, lead_ptrange=lead_ptrange, outputDir=outputDir, outputPrefix='__%s' %ch, systematics=systematics )

            namePostfix = '__%s__%s' %( ch, reg )
            if lead_ptrange[0] is not None :
                if lead_ptrange[1] is None :
                    namePostfix += '__pt_%d-max' %lead_ptrange[0]
                else :
                    namePostfix += '__pt_%d-%d' %(lead_ptrange[0], lead_ptrange[1] )

            save_templates( templates_pt, outputDir, lead_ptrange=lead_ptrange, namePostfix=namePostfix )
            save_results( results_pt_stat, outputDir, namePostfix )

            namePostfix_syst = '__syst%s' %namePostfix

            save_results( results_pt_syst, outputDir, namePostfix_syst )

#def do_corrected_asymiso_fit( iso_cuts_iso=None, iso_cuts_noiso=None, ptbins=[], subl_ptrange=(None,None), ch='mu', outputDir=None, systematics=None ) :
#
#    binning = get_default_binning()
#    samples = get_default_samples(ch)
#
#    real_template_str_iso = get_default_draw_commands(ch )['real']
#    fake_template_str_iso = get_default_draw_commands(ch )['fake']
#    if iso_cuts_iso is not None :
#        real_template_str_iso = real_template_str_iso + ' && ' + iso_cuts_iso
#        fake_template_str_iso = fake_template_str_iso + ' && ' + iso_cuts_iso
#
#    real_template_str_noiso = get_default_draw_commands(ch )['real']
#    fake_template_str_noiso = get_default_draw_commands(ch )['fake']
#    if iso_cuts_noiso is not None :
#        real_template_str_noiso = real_template_str_noiso + ' && ' + iso_cuts_noiso
#        fake_template_str_noiso = fake_template_str_noiso + ' && ' + iso_cuts_noiso
#
#    templates_iso_reg = {}
#    templates_iso_reg['EB'] = {}
#    templates_iso_reg['EE'] = {}
#    templates_iso_reg['EB']['real'] = get_single_photon_template(real_template_str_iso, binning['EB'], samples['real'], 'EB' )
#    templates_iso_reg['EE']['real'] = get_single_photon_template(real_template_str_iso, binning['EE'], samples['real'], 'EE' )
#    templates_iso_reg['EB']['fake'] = get_single_photon_template(fake_template_str_iso, binning['EB'], samples['fake'], 'EB' )
#    templates_iso_reg['EE']['fake'] = get_single_photon_template(fake_template_str_iso, binning['EE'], samples['fake'], 'EE' )
#
#    templates_noiso_reg = {}
#    templates_noiso_reg['EB'] = {}
#    templates_noiso_reg['EE'] = {}
#    templates_noiso_reg['EB']['real'] = get_single_photon_template(real_template_str_noiso, binning['EB'], samples['real'], 'EB' )
#    templates_noiso_reg['EE']['real'] = get_single_photon_template(real_template_str_noiso, binning['EE'], samples['real'], 'EE' )
#    templates_noiso_reg['EB']['fake'] = get_single_photon_template(fake_template_str_noiso, binning['EB'], samples['fake'], 'EB' )
#    templates_noiso_reg['EE']['fake'] = get_single_photon_template(fake_template_str_noiso, binning['EE'], samples['fake'], 'EE' )
#
#    lead_iso_cuts   = None
#    lead_noiso_cuts = None
#
#    if iso_cuts_iso is not None :
#        lead_iso_cuts = iso_cuts_iso.replace('[1]', '[0]')
#    if iso_cuts_noiso is not None :
#        lead_noiso_cuts = iso_cuts_noiso.replace('[1]', '[0]')
#
#    regions = [ 'EB', 'EE' ]
#
#    for reg in regions :
#
#        templates_leadiso = {}
#        templates_leadiso['lead'] = {}
#        templates_leadiso['lead']['real'] = templates_iso_reg[reg]['real']
#        templates_leadiso['lead']['fake'] = templates_iso_reg[reg]['fake']
#
#        templates_subliso = {}
#        templates_subliso['lead'] = {}
#        templates_subliso['lead']['real'] = templates_noiso_reg[reg]['real']
#        templates_subliso['lead']['fake'] = templates_noiso_reg[reg]['fake']
#
#        templates_nom = {}
#        templates_nom['lead'] = {}
#        templates_nom['lead']['real'] = templates_leadiso['lead']['real']
#        templates_nom['lead']['fake'] = templates_leadiso['lead']['fake']
#
#        # add regions onto the selection
#        gg_selection_leadiso = get_default_draw_commands(ch)['gg'] + ' && ph_Is%s[0] ' %( reg )
#
#        # add object cuts to the selection
#        if lead_iso_cuts is not None :
#            gg_selection_leadiso = gg_selection_leadiso + ' && %s ' %(lead_iso_cuts)
#
#        # parse out the x and y binning
#        xbinn = binning[reg[0]]
#
#        # variable given to TTree.Draw
#        var = 'ph_pt[0]::ph_sigmaIEIE[0]' #z:y:x
#
#        # get sample
#        target_samp = sampManFit.get_samples(name=samples['target'])
#
#        # draw and get back the hist
#        gg_hist_leadiso = clone_sample_and_draw( target_samp[0], var, gg_selection_leadiso, ( xbinn[0], xbinn[1], xbinn[2], 100, 0, 500 ) )
#
#        # -----------------------
#        # inclusive result
#        # -----------------------
#        # project data hist
#        gg_hist_leadiso_inclusive = gg_hist_leadiso.Project3D( 'yx' )
#
#        templates_leadiso_inclusive = get_projected_templates( templates_leadiso, lead_ptrange = (None,None) )
#        templates_nom_inclusive = get_projected_templates( templates_nom, lead_ptrange = (None,None) )
#
#        (results_corr_stat, results_corr_syst)  = run_corrected_diphoton_fit(templates_leadiso_inclusive, gg_hist_leadiso_inclusive, reg, lead_ptrange=(None,None), outputDir=outputDir, outputPrefix='__%s' %ch, systematics=systematics)
#
#        namePostfix = '__%s__%s-%s' %( ch,reg[0], reg[1] )
#
#        save_templates( templates_nom_inclusive, outputDir, lead_ptrange=(None,None),namePostfix=namePostfix )
#        save_results( results_corr_stat, outputDir, namePostfix)
#
#        namePostfix_syst = '__syst%s' %namePostfix
#        save_results( results_corr_syst, outputDir, namePostfix_syst)
#
#        # -----------------------
#        # pt binned results
#        # -----------------------
#        for idx, ptmin in enumerate(ptbins[:-1] ) :
#
#            ptmax = ptbins[idx+1]
#
#            # put lead range together (expected by following code)
#            if ptmax == ptbins[-1] : 
#                lead_ptrange = ( ptmin, None )
#            else :
#                lead_ptrange = ( ptmin, ptmax )
#
#            print 'ptmin = %d, ptmax = %d, Min Z bin = %d, max Z bin = %d' %( ptmin, ptmax, gg_hist_leadiso.GetZaxis().FindBin( ptmin), gg_hist_leadiso.GetZaxis().FindBin( ptmax )-1 )
#            # project data hist
#            gg_hist_leadiso.GetZaxis().SetRange( gg_hist_leadiso.GetZaxis().FindBin( ptmin), gg_hist_leadiso.GetZaxis().FindBin( ptmax )-1 )
#            gg_hist_leadiso_pt = gg_hist_leadiso.Project3D( 'yx' )
#
#            gg_hist_subliso.GetZaxis().SetRange( gg_hist_subliso.GetZaxis().FindBin( ptmin), gg_hist_subliso.GetZaxis().FindBin( ptmax )-1 )
#            gg_hist_subliso_pt = gg_hist_subliso.Project3D( 'yx' )
#                
#            # get templates
#            templates_leadiso_pt = get_projected_templates( templates_leadiso, lead_ptrange=lead_ptrange, subl_ptrange=(15, lead_ptrange[1]) )
#            templates_subliso_pt = get_projected_templates( templates_subliso, lead_ptrange=lead_ptrange, subl_ptrange=(15, lead_ptrange[1]) )
#            templates_nom_pt = get_projected_templates( templates_nom, lead_ptrange=lead_ptrange, subl_ptrange=(15, lead_ptrange[1]) )
#
#            # get results
#            (results_corr_pt_stat, results_corr_pt_syst) = run_corrected_diphoton_fit(templates_leadiso_pt, templates_subliso_pt, gg_hist_leadiso_pt, gg_hist_subliso_pt, reg[0], reg[1], lead_ptrange=lead_ptrange, subl_ptrange=(15, lead_ptrange[1]), outputDir=outputDir, outputPrefix='__%s'%ch, systematics=systematics)
#
#            namePostfix = '__%s__%s-%s' %( ch, reg[0], reg[1] )
#
#            if lead_ptrange[0] is not None :
#                if lead_ptrange[1] is None :
#                    namePostfix += '__pt_%d-max' %lead_ptrange[0]
#                else :
#                    namePostfix += '__pt_%d-%d' %(lead_ptrange[0], lead_ptrange[1] )
#
#            if subl_ptrange[0] is not None :
#                if subl_ptrange[1] is None :
#                    namePostfix += '__subpt_%d-max' %subl_ptrange[0]
#                else :
#                    namePostfix += '__subpt_%d-%d' %(subl_ptrange[0], subl_ptrange[1] )
#
#            save_templates( templates_nom_pt, outputDir, lead_ptrange=lead_ptrange, namePostfix=namePostfix)
#            save_results( results_corr_pt_stat, outputDir, namePostfix)
#
#            namePostfix_syst = '__syst%s' %namePostfix
#            save_results( results_corr_pt_syst, outputDir, namePostfix_syst)
#
#def do_closure_fit( iso_cuts_lead=None, iso_cuts_subl=None, ptbins=[], subl_ptrange=None, ch='mu', ngen=None, corr_factor=0.0, outputDir=None ) :
#
#    if ngen is None :
#        ngen = { 'RF' : 10000, 'FR' : 10000, 'FF' : 10000 }
#
#    binning = get_default_binning()
#    samples = get_default_samples(ch)
#
#    # generate templates for both EB and EE
#    real_template_str = get_default_draw_commands(ch )['real'] + ' && %s' %iso_cuts_lead
#    fake_template_str = get_default_draw_commands(ch )['fake'] + ' && %s' %iso_cuts_lead
#
#    templates_reg = {}
#    templates_reg['EB'] = {}
#    templates_reg['EE'] = {}
#    templates_reg['EB']['real'] = get_single_photon_template(real_template_str, binning['EB'], samples['real'], 'EB')
#    templates_reg['EE']['real'] = get_single_photon_template(real_template_str, binning['EE'], samples['real'], 'EE')
#    templates_reg['EB']['fake'] = get_single_photon_template(fake_template_str, binning['EB'], samples['fake'], 'EB')
#    templates_reg['EE']['fake'] = get_single_photon_template(fake_template_str, binning['EE'], samples['fake'], 'EE')
#
#    regions = [ ('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB'), ('EE', 'EE') ]
#    for reg in regions :
#
#        # convert from regions to lead/subl
#        templates = {}
#        templates['lead'] = {}
#        templates['subl'] = {}
#        templates['lead']['real'] = templates_reg[reg[0]]['real']
#        templates['subl']['real'] = templates_reg[reg[1]]['real']
#        templates['lead']['fake'] = templates_reg[reg[0]]['fake']
#        templates['subl']['fake'] = templates_reg[reg[1]]['fake']
#
#        templates_inclusive = get_projected_templates( templates, lead_ptrange = (None,None), subl_ptrange=subl_ptrange )
#
#        results_inclusive = run_generated_diphoton_fit(templates_inclusive, reg[0], reg[1], ngen, corr_factor=corr_factor, outputDir=outputDir, outputPrefix='__%s'%ch )
#
#        print results_inclusive
#
#        #namePostfix = '__%s__%s-%s' %( ch, reg[0], reg[1] )
#        #save_templates( templates_inclusive, outputDir, lead_ptrange=(None,None), namePostfix=namePostfix )
#        #save_results( results_inclusive, outputDir, namePostfix )
#
#        # -----------------------
#        # pt binned results
#        # -----------------------
#        for idx, ptmin in enumerate(ptbins[:-1] ) :
#            ptmax = ptbins[idx+1]
#
#            # put lead range together (expected by following code)
#            if ptmax == ptbins[-1] : 
#                lead_ptrange = ( ptmin, None )
#            else :
#                lead_ptrange = ( ptmin, ptmax )
#
#            # get templates
#            templates_pt = get_projected_templates( templates, lead_ptrange=lead_ptrange, subl_ptrange=(15, lead_ptrange[1] ) )
#
#            # get results
#            results_pt = run_generated_diphoton_fit(templates_pt, reg[0], reg[1],ngen, corr_factor=corr_factor, outputDir=outputDir, outputPrefix='__%s' %ch )
#
#            print results_pt
#
#            #namePostfix = '__%s__%s-%s' %( ch, reg[0], reg[1] )
#            #if lead_ptrange[0] is not None :
#            #    if lead_ptrange[1] is None :
#            #        namePostfix += '__pt_%d-max' %lead_ptrange[0]
#            #    else :
#            #        namePostfix += '__pt_%d-%d' %(lead_ptrange[0], lead_ptrange[1] )
#
#            #if subl_ptrange[0] is not None :
#            #    if subl_ptrange[1] is None :
#            #        namePostfix += '__subpt_%d-max' %subl_ptrange[0]
#            #    else :
#            #        namePostfix += '__subpt_%d-%d' %(subl_ptrange[0], subl_ptrange[1] )
#
#            #save_templates( templates_pt, outputDir, lead_ptrange=lead_ptrange, namePostfix=namePostfix )
#            #save_results( results_pt, outputDir, namePostfix )
#
#
#def update_asym_results( results_leadiso, results_subliso ) :
#        
#    iso_eff_subl = (results_subliso['template_int_subl_fake_tight']+results_subliso['template_int_subl_fake_loose'])/(results_leadiso['template_int_subl_fake_tight']+results_leadiso['template_int_subl_fake_loose'])
#    iso_eff_lead = (results_leadiso['template_int_lead_fake_tight']+results_leadiso['template_int_lead_fake_loose'])/(results_subliso['template_int_lead_fake_tight']+results_subliso['template_int_lead_fake_loose'])
#
#    results_leadiso['iso_eff_subl'] = iso_eff_subl
#    results_subliso['iso_eff_lead'] = iso_eff_lead
#
#    results_leadiso['Npred_RF_TT_scaled'] = results_leadiso['Npred_RF_TT']*iso_eff_subl
#    results_leadiso['Npred_FR_TT_scaled'] = results_leadiso['Npred_FR_TT']*iso_eff_subl
#    results_leadiso['Npred_FF_TT_scaled'] = results_leadiso['Npred_FF_TT']*iso_eff_subl
#
#    results_leadiso['Npred_RF_TL_scaled'] = results_leadiso['Npred_RF_TL']*iso_eff_subl
#    results_leadiso['Npred_FR_TL_scaled'] = results_leadiso['Npred_FR_TL']*iso_eff_subl
#    results_leadiso['Npred_FF_TL_scaled'] = results_leadiso['Npred_FF_TL']*iso_eff_subl
#
#    results_leadiso['Npred_RF_LT_scaled'] = results_leadiso['Npred_RF_LT']*iso_eff_subl
#    results_leadiso['Npred_FR_LT_scaled'] = results_leadiso['Npred_FR_LT']*iso_eff_subl
#    results_leadiso['Npred_FF_LT_scaled'] = results_leadiso['Npred_FF_LT']*iso_eff_subl
#
#    results_leadiso['Npred_RF_LL_scaled'] = results_leadiso['Npred_RF_LL']*iso_eff_subl
#    results_leadiso['Npred_FR_LL_scaled'] = results_leadiso['Npred_FR_LL']*iso_eff_subl
#    results_leadiso['Npred_FF_LL_scaled'] = results_leadiso['Npred_FF_LL']*iso_eff_subl
#
#    results_subliso['Npred_RF_TT_scaled'] = results_subliso['Npred_RF_TT']*iso_eff_lead
#    results_subliso['Npred_FR_TT_scaled'] = results_subliso['Npred_FR_TT']*iso_eff_lead
#    results_subliso['Npred_FF_TT_scaled'] = results_subliso['Npred_FF_TT']*iso_eff_lead
#
#    results_subliso['Npred_RF_TL_scaled'] = results_subliso['Npred_RF_TL']*iso_eff_lead
#    results_subliso['Npred_FR_TL_scaled'] = results_subliso['Npred_FR_TL']*iso_eff_lead
#    results_subliso['Npred_FF_TL_scaled'] = results_subliso['Npred_FF_TL']*iso_eff_lead
#
#    results_subliso['Npred_RF_LT_scaled'] = results_subliso['Npred_RF_LT']*iso_eff_lead
#    results_subliso['Npred_FR_LT_scaled'] = results_subliso['Npred_FR_LT']*iso_eff_lead
#    results_subliso['Npred_FF_LT_scaled'] = results_subliso['Npred_FF_LT']*iso_eff_lead
#
#    results_subliso['Npred_RF_LL_scaled'] = results_subliso['Npred_RF_LL']*iso_eff_lead
#    results_subliso['Npred_FR_LL_scaled'] = results_subliso['Npred_FR_LL']*iso_eff_lead
#    results_subliso['Npred_FF_LL_scaled'] = results_subliso['Npred_FF_LL']*iso_eff_lead

def get_projected_templates( templates, lead_ptrange=(None,None) ) :

    templates_proj = {}
    templates_proj['lead'] = {}

    # project in a range
    if lead_ptrange[0] is not None :
        for rf, hist_entries in templates['lead'].iteritems() :
            templates_proj['lead'][rf] = {}
            for hist_type, hist in hist_entries.iteritems() : 
                if hist is None :
                    templates_proj['lead'][rf][hist_type] = None
                else :
                    if lead_ptrange[1] is None :
                        templates_proj['lead'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_%d-max' %( lead_ptrange[0] ), hist.GetYaxis().FindBin( lead_ptrange[0] ) )
                    else :
                        templates_proj['lead'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_%d-%d' %( lead_ptrange[0], lead_ptrange[1] ), hist.GetYaxis().FindBin( lead_ptrange[0] ), hist.GetYaxis().FindBin( lead_ptrange[1] )-1 )

    else : # project inclusive
        for rf, hist_entries in templates['lead'].iteritems() :
            templates_proj['lead'][rf] = {}
            for hist_type, hist in hist_entries.iteritems() : 
                if hist is not None :
                    templates_proj['lead'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_inclusive' )
                else :
                    templates_proj['lead'][rf][hist_type] = None

    return templates_proj


def run_corrected_diphoton_fit( templates_leadiso, templates_subliso, gg_hist_leadiso, gg_hist_subliso, lead_reg, subl_reg, lead_ptrange=(None,None), subl_ptrange=(None,None), ndim=3, outputDir=None, outputPrefix='', systematics=None ) :

    accept_reg = ['EB', 'EE']
    if lead_reg not in accept_reg :
        print 'Lead region does not make sense'
        return
    if subl_reg not in accept_reg :
        print 'Subl region does not make sense'
        return

    # get the defaults
    samples = get_default_samples()
    plotbinning = get_default_binning()
    cuts = get_default_cuts()

    # Find the bins corresponding to the cuts
    # lead photon on X axis, subl on Y axis
    bins_lead_tight = ( gg_hist_leadiso.GetXaxis().FindBin( cuts[lead_reg]['tight'][0] ), gg_hist_leadiso.GetXaxis().FindBin( cuts[lead_reg]['tight'][1] ) )
    bins_lead_loose = ( gg_hist_leadiso.GetXaxis().FindBin( cuts[lead_reg]['loose'][0] ), gg_hist_leadiso.GetXaxis().FindBin( cuts[lead_reg]['loose'][1] ) )
    bins_subl_tight = ( gg_hist_leadiso.GetYaxis().FindBin( cuts[subl_reg]['tight'][0] ), gg_hist_leadiso.GetYaxis().FindBin( cuts[subl_reg]['tight'][1] ) )
    bins_subl_loose = ( gg_hist_leadiso.GetYaxis().FindBin( cuts[subl_reg]['loose'][0] ), gg_hist_leadiso.GetYaxis().FindBin( cuts[subl_reg]['loose'][1] ) )

    print 'cuts, bins lead, tight = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['tight'][0], cuts[lead_reg]['tight'][1], bins_lead_tight[0], bins_lead_tight[1] )
    print 'cuts, bins lead, loose = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['loose'][0], cuts[lead_reg]['loose'][1], bins_lead_loose[0], bins_lead_loose[1] )
    print 'cuts, bins subl, tight = %f-%f ( %d - %d ) ' %( cuts[subl_reg]['tight'][0], cuts[subl_reg]['tight'][1], bins_subl_tight[0], bins_subl_tight[1] )
    print 'cuts, bins subl, loose = %f-%f ( %d - %d ) ' %( cuts[subl_reg]['loose'][0], cuts[subl_reg]['loose'][1], bins_subl_loose[0], bins_subl_loose[1] )

    # arragnge the cuts by region
    eff_cuts = {}
    eff_cuts['lead'] = {}
    eff_cuts['subl'] = {}
    eff_cuts['lead']['tight'] = cuts[lead_reg]['tight']
    eff_cuts['lead']['loose'] = cuts[lead_reg]['loose']
    eff_cuts['subl']['tight'] = cuts[subl_reg]['tight']
    eff_cuts['subl']['loose'] = cuts[subl_reg]['loose']

    # get template integrals
    #int_leadiso = get_template_integrals( templates_leadiso, eff_cuts )
    #int_subliso = get_template_integrals( templates_subliso, eff_cuts )
    (stat_int_leadiso, syst_int_leadiso) = get_template_integrals( templates_leadiso, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )
    (stat_int_subliso, syst_int_subliso) = get_template_integrals( templates_subliso, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )

    iso_eff_subl_tight = stat_int_subliso['subl']['fake']['tight'] / stat_int_leadiso['subl']['fake']['tight']
    iso_eff_subl_loose = stat_int_subliso['subl']['fake']['loose'] / stat_int_leadiso['subl']['fake']['loose']

    iso_eff_lead_tight = stat_int_leadiso['lead']['fake']['tight'] / stat_int_subliso['lead']['fake']['tight']
    iso_eff_lead_loose = stat_int_leadiso['lead']['fake']['loose'] / stat_int_subliso['lead']['fake']['loose']

    # Integrate to the the data in the four regions
    Ndata_TT_leadiso = gg_hist_leadiso.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_TL_leadiso = gg_hist_leadiso.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_loose[0], bins_subl_loose[1] )
    Ndata_LT_leadiso = gg_hist_leadiso.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_LL_leadiso = gg_hist_leadiso.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_loose[0], bins_subl_loose[1] )

    Ndata_TT_subliso = gg_hist_subliso.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_TL_subliso = gg_hist_subliso.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_loose[0], bins_subl_loose[1] )
    Ndata_LT_subliso = gg_hist_subliso.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_LL_subliso = gg_hist_subliso.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_loose[0], bins_subl_loose[1] )

    #-----------------------------------------
    # Use data with loosened iso on the Loose photon
    # Multiply by the efficiency of the loosened iso
    #-----------------------------------------
     
    # lead has loosened iso
    # Correct data in LT region by loosening isolation on the lead photon 
    # and correct by the efficiency of the loosened selection
    Ncorr_LT         = Ndata_LT_subliso * iso_eff_lead_loose
    Ncorr_LL_subliso = Ndata_LL_subliso * iso_eff_lead_loose

    # subl has loosened iso
    # correct data in TL region by loosening isolation on the subl photon
    # and correct by the efficiency of the loosened selection
    Ncorr_TL         = Ndata_TL_leadiso * iso_eff_subl_loose
    Ncorr_LL_leadiso = Ndata_LL_leadiso * iso_eff_subl_loose

    # use the average of the two
    Ncorr_LL = ( Ncorr_LL_leadiso + Ncorr_LL_subliso )/2.

    print 'NData orig leadiso , TL = %d, LT = %d, LL = %d' %( Ndata_TL_leadiso, Ndata_LT_leadiso, Ndata_LL_leadiso )
    print 'NData orig subliso , TL = %d, LT = %d, LL = %d' %( Ndata_TL_subliso, Ndata_LT_subliso, Ndata_LL_subliso )
    print 'iso_eff_subl_tight = %s, iso_eff_subl_loose = %s, iso_eff_lead_tight = %s, iso_eff_lead_loose= %s' %( iso_eff_subl_tight, iso_eff_subl_loose, iso_eff_lead_tight, iso_eff_subl_loose )
    print 'NData corr, TL = %s, LT = %s, LLlead = %s, LLsubl = %s, LL = %s ' %( Ncorr_TL, Ncorr_LT, Ncorr_LL_leadiso, Ncorr_LL_subliso, Ncorr_LL )

    templates_corr = {}
    templates_corr['lead'] = {}
    templates_corr['subl'] = {}
    templates_corr['lead']['real'] = templates_leadiso['lead']['real']
    templates_corr['lead']['fake'] = templates_leadiso['lead']['fake']
    templates_corr['subl']['real'] = templates_subliso['subl']['real']
    templates_corr['subl']['fake'] = templates_subliso['subl']['fake']

    # get 2-d efficiencies from 1-d inputs
    (eff_2d_stat, eff_2d_syst) = generate_2d_efficiencies( templates_corr, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )
    print eff_2d_stat

    if ndim == 3 :
        datacorr = {}
        datacorr['TL'] = Ncorr_TL
        datacorr['LT'] = Ncorr_LT
        datacorr['LL'] = Ncorr_LL
        results_stat = run_fit( datacorr, eff_2d_stat )
        results_syst= run_fit( datacorr, eff_2d_syst )

        datacorr['TT'] = ufloat(0, 0)

        text_results_stat = collect_results( results_stat, datacorr, eff_2d_stat, templates_corr, bins_lead_loose, bins_lead_tight, bins_subl_loose, bins_subl_tight, ndim)
        text_results_syst = collect_results( results_syst, datacorr, eff_2d_syst, templates_corr, bins_lead_loose, bins_lead_tight, bins_subl_loose, bins_subl_tight, ndim)

        
        print 'text_results_stat'
        print text_results_stat
        print 'text_results_syst'
        print text_results_syst
        return text_results_stat, text_results_syst
    else :
        print 'IMPLEMENT DIM4'
        return




def run_generated_diphoton_fit( templates, lead_reg, subl_reg, n_data_gen, ndim=3, corr_factor=0.0, outputDir=None, outputPrefix='' ) :

    rand = ROOT.TRandom3()
    rand.SetSeed( int(time.mktime(time.localtime()) ) )

    accept_reg = ['EB', 'EE']
    if lead_reg not in accept_reg :
        print 'Lead region does not make sense'
        return
    if subl_reg not in accept_reg :
        print 'Subl region does not make sense'
        return

    # get the defaults
    samples = get_default_samples()
    plotbinning = get_default_binning()
    cuts = get_default_cuts()

    eff_cuts = {}
    eff_cuts['lead'] = {}
    eff_cuts['subl'] = {}
    eff_cuts['lead']['tight'] = cuts[lead_reg]['tight']
    eff_cuts['lead']['loose'] = cuts[lead_reg]['loose']
    eff_cuts['subl']['tight'] = cuts[subl_reg]['tight']
    eff_cuts['subl']['loose'] = cuts[subl_reg]['loose']

    # get 2-d efficiencies from 1-d inputs
    (eff_2d, eff_2d_syst) = generate_2d_efficiencies( templates, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange )
    print eff_2d

    Ndata = {}
    Ndata['TT'] = 0
    Ndata['TL'] = 0
    Ndata['LT'] = 0
    Ndata['LL'] = 0
    
    eff_1d_lead_base = {}
    eff_1d_subl_base = {}
    eff_1d_lead_base['eff_F_T'] = eff_2d['eff_FF_TT'] + eff_2d['eff_FF_TL']
    eff_1d_lead_base['eff_F_L'] = eff_2d['eff_FF_LL'] + eff_2d['eff_FF_LT']
    eff_1d_subl_base['eff_F_T'] = eff_2d['eff_FF_TT'] + eff_2d['eff_FF_LT']
    eff_1d_subl_base['eff_F_L'] = eff_2d['eff_FF_LL'] + eff_2d['eff_FF_TL']

    print 'eff_1d_lead'
    print eff_1d_lead_base
    print 'eff_1d_subl'
    print eff_1d_subl_base

    # do FR
    #for tag in ['FR', 'RF', 'FF'] :
    for tag in ['FR', 'RF'] :
        for i in xrange( 0, n_data_gen[tag] ) :

            rndmval = rand.Rndm()

            lead_tight = None
            subl_tight = None

            # 2d efficiencies are normalized to unity...just linearize the efficiencies to determine
            # where the photons landed
            if rndmval < (eff_2d['eff_%s_TT'%tag]) :
                Ndata['TT'] = Ndata['TT']+1
            elif rndmval < (eff_2d['eff_%s_TT'%tag] + eff_2d['eff_%s_TL'%tag]) :
                Ndata['TL'] = Ndata['TL']+1
            elif rndmval < (eff_2d['eff_%s_TT'%tag] + eff_2d['eff_%s_TL'%tag] + eff_2d['eff_%s_LT'%tag]) :
                Ndata['LT'] = Ndata['LT']+1
            elif rndmval < (eff_2d['eff_%s_TT'%tag] + eff_2d['eff_%s_TL'%tag] + eff_2d['eff_%s_LT'%tag] + eff_2d['eff_%s_LL'%tag]) :
                Ndata['LL'] = Ndata['LL']+1
            else :
                print 'SHOULD NOT GET HERE -- templates not normalized to unity, it is ', (eff_2d['eff_%s_TT'%tag] + eff_2d['eff_%s_TL'%tag] + eff_2d['eff_%s_LT'%tag] + eff_2d['eff_%s_LL'%tag])

    # do FF, allow for a correlation 
    for i in xrange( 0, n_data_gen['FF'] ) :
        # decide which photon to select first
        lead_first = (rand.Rndm() < 0.5)
        # generate random numbers for lead and subl
        lead_rndm = rand.Rndm()
        subl_rndm = rand.Rndm()

        lead_tight = None
        subl_tight = None
        eff_1d_lead = {}
        eff_1d_subl = {}
        if lead_first :

            #make sure efficiencies are normalized to unity
            lead_norm = 1.0/(eff_1d_lead_base['eff_F_T']+eff_1d_lead_base['eff_F_L'])

            eff_1d_lead['eff_F_T'] = lead_norm*eff_1d_lead_base['eff_F_T']
            eff_1d_lead['eff_F_L'] = lead_norm*eff_1d_lead_base['eff_F_L']


            # determine if the lead photon is loose or tight
            # modify the subl efficiency based on the given correction factor
            if lead_rndm < eff_1d_lead['eff_F_T'] : 
                lead_tight = True
                eff_1d_subl['eff_F_L'] = eff_1d_subl_base['eff_F_L']*(1-corr_factor)
                eff_1d_subl['eff_F_T'] = eff_1d_subl_base['eff_F_T']
            else :
                lead_tight = False
                eff_1d_subl['eff_F_L'] = eff_1d_subl_base['eff_F_L']*(1+corr_factor)
                eff_1d_subl['eff_F_T'] = eff_1d_subl_base['eff_F_T']

            # normalize the modified subl efficiencies
            subl_norm = 1.0/(eff_1d_subl['eff_F_T']+eff_1d_subl['eff_F_L'])
            eff_1d_subl['eff_F_T'] = subl_norm*eff_1d_subl['eff_F_T']
            eff_1d_subl['eff_F_L'] = subl_norm*eff_1d_subl['eff_F_L']

            # check if subl is loose or tight
            if subl_rndm < eff_1d_subl['eff_F_T'] : 
                subl_tight = True
            else :
                subl_tight = False

        else :

            #make sure efficiencies are normalized to unity
            subl_norm = 1.0/(eff_1d_subl_base['eff_F_T']+eff_1d_subl_base['eff_F_L'])
            eff_1d_subl['eff_F_T'] = subl_norm*eff_1d_subl_base['eff_F_T']
            eff_1d_subl['eff_F_L'] = subl_norm*eff_1d_subl_base['eff_F_L']


            # determine if the subl photon is loose or tight
            # modify the lead efficiency based on the given correction factor
            if subl_rndm < eff_1d_subl['eff_F_T'] : 
                subl_tight = True
                eff_1d_lead['eff_F_L'] = eff_1d_lead_base['eff_F_L']*(1-corr_factor)
                eff_1d_lead['eff_F_T'] = eff_1d_lead_base['eff_F_T']
            else :
                subl_tight = False
                eff_1d_lead['eff_F_L'] = eff_1d_lead_base['eff_F_L']*(1+corr_factor)
                eff_1d_lead['eff_F_T'] = eff_1d_lead_base['eff_F_T']

            # normalize the modified lead efficiencies
            lead_norm = 1.0/(eff_1d_lead['eff_F_T']+eff_1d_lead['eff_F_L'])
            eff_1d_lead['eff_F_T'] = lead_norm*eff_1d_lead['eff_F_T']
            eff_1d_lead['eff_F_L'] = lead_norm*eff_1d_lead['eff_F_L']

            # check if lead is loose or tight
            if lead_rndm < eff_1d_lead['eff_F_T'] : 
                lead_tight = True
            else :
                lead_tight = False

        # make sure they were set
        if lead_tight is None or subl_tight is None :
            print 'Something went wrong!'
            return

        # fill the data
        if lead_tight and subl_tight :
            Ndata['TT'] = Ndata['TT']+1
        elif lead_tight and not subl_tight :
            Ndata['TL'] = Ndata['TL']+1
        elif not lead_tight and subl_tight :
            Ndata['LT'] = Ndata['LT']+1
        else  :
            Ndata['LL'] = Ndata['LL']+1

    Ndata['TT'] = ufloat( Ndata['TT'], math.sqrt( Ndata['TT'] ) )
    Ndata['TL'] = ufloat( Ndata['TL'], math.sqrt( Ndata['TL'] ) )
    Ndata['LT'] = ufloat( Ndata['LT'], math.sqrt( Ndata['LT'] ) )
    Ndata['LL'] = ufloat( Ndata['LL'], math.sqrt( Ndata['LL'] ) )

    print Ndata

    if ndim == 3 :
        results = run_fit( {'TL': Ndata['TL'], 'LT' : Ndata['LT'], 'LL' : Ndata['LL']}, eff_2d )
    if ndim == 4 :
        results = run_fit( Ndata, eff_2d )


    text_results=collections.OrderedDict()

    for key, val in eff_2d.iteritems() :
        text_results[key] = val

    if ndim == 4 :

        text_results['Ndata_TT'] = Ndata['TT']
        text_results['Ndata_TL'] = Ndata['TL']
        text_results['Ndata_LT'] = Ndata['LT']
        text_results['Ndata_LL'] = Ndata['LL']

        text_results['alpha_RR'] = results.item(0)
        text_results['alpha_RF'] = results.item(1)
        text_results['alpha_FR'] = results.item(2)
        text_results['alpha_FF'] = results.item(3)

        text_results['Npred_RR_TT'] = text_results['alpha_RR']*text_results['eff_RR_TT']
        text_results['Npred_RR_TL'] = text_results['alpha_RR']*text_results['eff_RR_TL']
        text_results['Npred_RR_LT'] = text_results['alpha_RR']*text_results['eff_RR_LT']
        text_results['Npred_RR_LL'] = text_results['alpha_RR']*text_results['eff_RR_LL']

    else :
        text_results['Ndata_TT'] = ufloat(0, 0)
        text_results['Ndata_TL'] = Ndata['TL']
        text_results['Ndata_LT'] = Ndata['LT']
        text_results['Ndata_LL'] = Ndata['LL']

        text_results['alpha_RF'] = results.item(0)
        text_results['alpha_FR'] = results.item(1)
        text_results['alpha_FF'] = results.item(2)


    text_results['Npred_RF_TT'] = text_results['alpha_RF']*text_results['eff_RF_TT']
    text_results['Npred_RF_TL'] = text_results['alpha_RF']*text_results['eff_RF_TL']
    text_results['Npred_RF_LT'] = text_results['alpha_RF']*text_results['eff_RF_LT']
    text_results['Npred_RF_LL'] = text_results['alpha_RF']*text_results['eff_RF_LL']

    text_results['Npred_FR_TT'] = text_results['alpha_FR']*text_results['eff_FR_TT']
    text_results['Npred_FR_TL'] = text_results['alpha_FR']*text_results['eff_FR_TL']
    text_results['Npred_FR_LT'] = text_results['alpha_FR']*text_results['eff_FR_LT']
    text_results['Npred_FR_LL'] = text_results['alpha_FR']*text_results['eff_FR_LL']

    text_results['Npred_FF_TT'] = text_results['alpha_FF']*text_results['eff_FF_TT']
    text_results['Npred_FF_TL'] = text_results['alpha_FF']*text_results['eff_FF_TL']
    text_results['Npred_FF_LT'] = text_results['alpha_FF']*text_results['eff_FF_LT']
    text_results['Npred_FF_LL'] = text_results['alpha_FF']*text_results['eff_FF_LL']

    text_results['Closure_TT'] = ( (text_results['Npred_RF_TT'] +text_results['Npred_FR_TT'] +text_results['Npred_FF_TT'] ) - Ndata['TT'] ) / Ndata['TT']
    text_results['Closure_TL'] = ( (text_results['Npred_RF_TL'] +text_results['Npred_FR_TL'] +text_results['Npred_FF_TL'] ) - Ndata['TL'] ) / Ndata['TL']
    text_results['Closure_LT'] = ( (text_results['Npred_RF_LT'] +text_results['Npred_FR_LT'] +text_results['Npred_FF_LT'] ) - Ndata['LT'] ) / Ndata['LT']
    text_results['Closure_LL'] = ( (text_results['Npred_RF_LL'] +text_results['Npred_FR_LL'] +text_results['Npred_FF_LL'] ) - Ndata['LL'] ) / Ndata['LL']

    print text_results


def run_photon_fit( templates, gg_hist, lead_reg, fitvar='sigmaIEIE', lead_ptrange=(None,None), outputDir=None, outputPrefix='', systematics=None ) :

    accept_reg = ['EB', 'EE']
    if lead_reg not in accept_reg :
        print 'Lead region does not make sense'
        return

    # get the defaults
    samples = get_default_samples()
    plotbinning = get_default_binning(var=fitvar)
    cuts = get_default_cuts(var=fitvar)

    # Find the bins corresponding to the cuts
    # lead photon on X axis, subl on Y axis
    bins_lead_tight = ( gg_hist.GetXaxis().FindBin( cuts[lead_reg]['tight'][0] ), gg_hist.GetXaxis().FindBin( cuts[lead_reg]['tight'][1] ) )
    bins_lead_loose = ( gg_hist.GetXaxis().FindBin( cuts[lead_reg]['loose'][0] ), gg_hist.GetXaxis().FindBin( cuts[lead_reg]['loose'][1] ) )

    print 'cuts, bins lead, tight = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['tight'][0], cuts[lead_reg]['tight'][1], bins_lead_tight[0], bins_lead_tight[1] )
    print 'cuts, bins lead, loose = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['loose'][0], cuts[lead_reg]['loose'][1], bins_lead_loose[0], bins_lead_loose[1] )

    # Integrate to the the data in the four regions
    Ndata_T = gg_hist.Integral( bins_lead_tight[0], bins_lead_tight[1])
    Ndata_L = gg_hist.Integral( bins_lead_loose[0], bins_lead_loose[1])

    # ufloat it!
    Ndata = {}
    Ndata['T'] = ufloat( Ndata_T, math.sqrt(Ndata_T ), 'Ndata_T' )
    Ndata['L'] = ufloat( Ndata_L, math.sqrt(Ndata_L ), 'Ndata_L' )

    print 'N data T = ', Ndata['T']
    print 'N data L = ', Ndata['L']

    # arragnge the cuts by 
    eff_cuts = {}
    eff_cuts['lead'] = {}
    eff_cuts['lead']['tight'] = cuts[lead_reg]['tight']
    eff_cuts['lead']['loose'] = cuts[lead_reg]['loose']

    # get 2-d efficiencies from 1-d inputs
    (eff_1d_stat, eff_1d_syst) =generate_1d_efficiencies( templates, eff_cuts, lead_reg, lead_ptrange,  systematics=systematics )

    print 'eff_1d'
    print eff_1d_stat

    results_stat = run_fit( {'T': Ndata['T'], 'L' : Ndata['L']}, eff_1d_stat )
    results_syst = run_fit( {'T': Ndata['T'], 'L' : Ndata['L']}, eff_1d_syst )

    print 'Real Norm = ', results_stat.item(0)
    print 'Fake Norm = ', results_stat.item(1)

    hist_temp_lead_real = templates['lead']['real']['Data'].Clone( 'hist_temp_lead_real' )
    hist_temp_lead_fake = templates['lead']['fake']['Data'].Clone( 'hist_temp_lead_fake' )

    if templates['lead']['real']['Background'] is not None :
        hist_temp_lead_real.Add( templates['lead']['real']['Background'] )
    if templates['lead']['fake']['Background'] is not None :
        hist_temp_lead_fake.Add( templates['lead']['fake']['Background'] )

    p_R_T = results_stat.item(0)*eff_1d_stat['eff_R_T_lead']
    p_R_L = results_stat.item(0)*eff_1d_stat['eff_R_L_lead']
    p_F_T = results_stat.item(1)*eff_1d_stat['eff_F_T_lead']
    p_F_L = results_stat.item(1)*eff_1d_stat['eff_F_L_lead']

    print 'nPred Real Tight = ', p_R_T
    print 'nPred Real Loose = ', p_R_L
    print 'nPred Fake Tight = ', p_F_T
    print 'nPred Fake Loose = ', p_F_L
    
    #normalize lead real template according to fit
    hist_temp_lead_real.Scale( ( p_R_T+p_R_L ).n/ hist_temp_lead_real.Integral() )
    hist_temp_lead_fake.Scale( ( p_F_T+p_F_L ).n/ hist_temp_lead_fake.Integral() )

    hist_temp_lead_real.SetLineColor(ROOT.kMagenta)
    hist_temp_lead_real.SetMarkerColor(ROOT.kMagenta)
    hist_temp_lead_real.SetLineWidth(2)

    hist_temp_lead_fake.SetLineColor(ROOT.kRed)
    hist_temp_lead_fake.SetMarkerColor(ROOT.kRed)
    hist_temp_lead_fake.SetLineWidth(2)

    hist_temp_lead_real.SetStats(0)
    hist_temp_lead_fake.SetStats(0)

    can_proj_lead = ROOT.TCanvas('proj_lead', '')

    namePostfix = '__%s' %( lead_reg )
    if lead_ptrange[0] is not None :
        if lead_ptrange[1] is None :
            namePostfix += '__pt_%d-max' %( lead_ptrange[0])
        else :
            namePostfix += '__pt_%d-%d' %( lead_ptrange[0], lead_ptrange[1])

    outputNamePL=None
    if outputDir is not None :
        outputNamePL = outputDir + '/fit_with_data_projlead%s%s.pdf' %(outputPrefix, namePostfix)

    if lead_reg == 'EE' :
        gg_hist.Rebin(10)
        hist_temp_lead_real.Rebin(10)
        hist_temp_lead_fake.Rebin(10)

    draw_template(can_proj_lead, [gg_hist, hist_temp_lead_real, hist_temp_lead_fake], sampManFit, normalize=False, first_hist_is_data=True, legend_entries=['Data', 'real+fake prediction', 'fake+fake prediction' ], outputName=outputNamePL )

    text_results_stat = collect_results( results_stat, Ndata, eff_1d_stat, templates, bins_lead_loose, bins_lead_tight )
    text_results_syst = collect_results( results_syst, Ndata, eff_1d_stat, templates, bins_lead_loose, bins_lead_tight )

    return text_results_stat, text_results_syst
    
def run_fit( data, efficiencies ) :

    # make the matrix
    matrix = generate_eff_matrix( efficiencies )
    print matrix

    #do the fit!  Invert the matrix and multiply the by counts vectors
    results = solve_matrix_eq( matrix, [data['T'], data['L']] )

    return results 

def run_fit_manual( data, eff ) :

    # matrix is 
    # ----------------------
    # RF_TL FR_TL FF_TL
    # RF_LT FR_LT FF_LT
    # RF_LL FR_LL FF_LL
    
    # RF_TL = (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']
    # FR_TL = (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']
    # FF_TL = (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']
    # RF_LT = eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])
    # FR_LT = eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
    # FF_LT = eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
    # RF_LL = eff['eff_R_L_lead']*eff['eff_F_L_subl']
    # FR_LL = eff['eff_F_L_lead']*eff['eff_R_L_subl']
    # FF_LL = eff['eff_F_L_lead']*eff['eff_F_L_subl']
    # RF_TT = (1-eff['eff_R_L_lead'])*(1-eff['eff_F_L_subl'])
    # FR_TT = (1-eff['eff_F_L_lead'])*(1-eff['eff_R_L_subl'])
    # FF_TT = (1-eff['eff_F_L_lead'])*(1-eff['eff_F_L_subl'])

    # determinant = RF_TL*FR_LT*FF_LL + FR_TL*FF_LT*RF_LL + FF_TL*RF_LT*FR_LL - FF_TL*FR_LT*RF_LL - FR_TL*RF_LT*FF_LL - RF_TL*FF_LT*FR_LL
    # determinant = (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] 
    #             + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    #             + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    #             - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    #             - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    #             - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    
    # Inverted matrix
    # Inv_11 = FR_LT*FF_LL-FF_LT*FR_LL
    # Inv_12 = FF_TL*FR_LL-FR_TL*FF_LL
    # Inv_13 = FR_TL*FF_LT-FF_TL*FR_LT
    # Inv_21 = FF_LT*RF_LL-RF_LT*FF_LL
    # Inv_22 = RF_TL*FF_LL-FF_TL*RF_LL
    # Inv_23 = FF_TL*RF_LT-RF_TL*FF_LT
    # Inv_31 = RF_LT*FR_LL-FR_LT*RF_LL
    # Inv_32 = FR_TL*RF_LL-RF_TL*FR_LL
    # Inv_33 = RF_TL*FR_LT-FR_TL*RF_LT

    # Inv_11 = eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    #        - eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    # Inv_12 = (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    #        - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    # Inv_13 = (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
    #        - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
    # Inv_21 = eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    #        - eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    # Inv_22 = (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    #        - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    # Inv_23 = (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])
    #        - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
    # Inv_31 = eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    #        - eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    # Inv_32 = (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    #        - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    # Inv_33 = (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
    #        - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])

    # alpha_rf = (1/determinant) * ( Inv_11 * Data['TL'] + Inv_12*Data['LT'] + Inv_13 * Data['LL'])
    # alpha_fr = (1/determinant) * ( Inv_21 * Data['TL'] + Inv_22*Data['LT'] + Inv_23 * Data['LL'])
    # alpha_ff = (1/determinant) * ( Inv_31 * Data['TL'] + Inv_32*Data['LT'] + Inv_33 * Data['LL'])
    alpha_rf = ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] 
                      + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                      + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                      - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                      - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                      - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
              * ( (  eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                   - eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] )*data['TL']
                + (  (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                   - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl'] )*data['LT']
                + (   (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl']) )*data['LL']
              ) )

    alpha_fr = ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']     
                    + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
            * ( (   eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                  - eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] )*data['TL'] 
              + (   (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                  - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl'] )*data['LT']
              + (   (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])
                  - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl']) ) *data['LL']
              ) )
                
    alpha_ff = ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']    
                    + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
            * ( (   eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                  - eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl'] )*data['TL']
              + (  (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                 - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) * data['LT']
              + (   (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
                  - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl']) )*data['LL']
              ) )


    nPred_RF_TT = ( (1-eff['eff_R_L_lead'])*(1-eff['eff_F_L_subl'])* 
                      ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] 
                      + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                      + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                      - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                      - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                      - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
              * ( (  eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                   - eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] )*data['TL']
                + (  (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                   - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl'] )*data['LT']
                + (   (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl']) )*data['LL']
              ) ) )

    nPred_FR_TT = ( (1-eff['eff_F_L_lead'])*(1-eff['eff_R_L_subl'])* 
                   ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']     
                    + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
            * ( (   eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                  - eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] )*data['TL'] 
              + (   (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                  - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl'] )*data['LT']
              + (   (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])
                  - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl']) ) *data['LL']
              ) ) )

    nPred_FF_TT = ( (1-eff['eff_F_L_lead'])*(1-eff['eff_F_L_subl'])* 
                  ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']    
                    + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
            * ( (   eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                  - eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl'] )*data['TL']
              + (  (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                 - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) * data['LT']
              + (   (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
                  - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl']) )*data['LL']
              ) ) )
       
    return {'alpha_RF' : alpha_rf, 'alpha_FR' : alpha_fr, 'alpha_FF' : alpha_ff, 'pred_RF_TT' : nPred_RF_TT, 'pred_FR_TT' : nPred_FR_TT, 'pred_FF_TT' : nPred_FF_TT }
       
       
#def save_normalized_template_hists( data_hist, results, templates, efficiencies, bins_lead_loose, bins_subl_loose, ndim, lead_ptrange=None, subl_ptrange=None, outputDir=None ) :
#    
#    if outputDir is None :
#        return


def collect_results( results, data, efficiencies, templates, bins_lead_loose, bins_lead_tight ) :

    text_results = collections.OrderedDict()

    for key, val in efficiencies.iteritems() :
        text_results[key] = val

    text_results['Ndata_T'] = data['T']
    text_results['Ndata_L'] = data['L']

    text_results['alpha_R'] = results.item(0)
    text_results['alpha_F'] = results.item(1)

    text_results['Npred_R_T'] = text_results['alpha_R']*text_results['eff_R_T_lead']
    text_results['Npred_R_L'] = text_results['alpha_R']*text_results['eff_R_L_lead']

    text_results['Npred_F_T'] = text_results['alpha_F']*text_results['eff_F_T_lead']
    text_results['Npred_F_L'] = text_results['alpha_F']*text_results['eff_F_L_lead']

    int_lead_real_loose = get_integral_and_error(templates['lead']['real']['Data'], bins_lead_loose )
    int_lead_real_tight = get_integral_and_error(templates['lead']['real']['Data'], bins_lead_tight )
    int_lead_fake_loose = get_integral_and_error(templates['lead']['fake']['Data'], bins_lead_loose )
    int_lead_fake_tight = get_integral_and_error(templates['lead']['fake']['Data'], bins_lead_tight )


    if templates['lead']['real']['Background'] is not None :
        int_lead_real_loose = int_lead_real_loose +  get_integral_and_error(templates['lead']['real']['Background'], bins_lead_loose )
    if templates['lead']['real']['Background'] is not None :
        int_lead_real_tight = int_lead_real_tight +  get_integral_and_error(templates['lead']['real']['Background'], bins_lead_tight )
    if templates['lead']['fake']['Background'] is not None :
        int_lead_fake_loose = int_lead_fake_loose +  get_integral_and_error(templates['lead']['fake']['Background'], bins_lead_loose )
    if templates['lead']['fake']['Background'] is not None :
        int_lead_fake_tight = int_lead_fake_tight +  get_integral_and_error(templates['lead']['fake']['Background'], bins_lead_tight )

    text_results['template_int_lead_real_loose'] = int_lead_real_loose
    text_results['template_int_lead_real_tight'] = int_lead_real_tight
    text_results['template_int_lead_fake_loose'] = int_lead_fake_loose
    text_results['template_int_lead_fake_tight'] = int_lead_fake_tight

    return text_results


def generate_1d_efficiencies( templates, cuts, lead_reg, lead_ptrange, systematics=None ) :

    (int_stat, int_syst) = get_template_integrals( templates, cuts, lead_reg, lead_ptrange, systematics=systematics )

    print 'Template integral'
    print int_stat

    (eff_1d_stat, eff_1d_syst) = get_1d_loose_efficiencies( int_stat, int_syst, lead_reg, lead_ptrange, systematics=systematics )

    return eff_1d_stat, eff_1d_syst

def get_1d_loose_efficiencies( int_stat, int_syst, lead_reg, lead_ptrange, systematics=None) :

    eff_stat = {}
    eff_syst = {}

    if int_stat['lead']['real']['loose'].n == 0 :
        eff_stat['eff_R_T_lead'] = ufloat( 1.0, int_stat['lead']['real']['tight'].s/int_stat['lead']['real']['tight'].n )
    else :
        eff_stat['eff_R_T_lead'] = int_stat['lead']['real']['tight'] / (int_stat['lead']['real']['tight']+int_stat['lead']['real']['loose'])
    eff_stat['eff_F_T_lead'] = int_stat['lead']['fake']['tight'] / (int_stat['lead']['fake']['tight']+int_stat['lead']['fake']['loose'])
    eff_stat['eff_R_L_lead'] = int_stat['lead']['real']['loose'] / (int_stat['lead']['real']['tight']+int_stat['lead']['real']['loose'])
    eff_stat['eff_F_L_lead'] = int_stat['lead']['fake']['loose'] / (int_stat['lead']['fake']['tight']+int_stat['lead']['fake']['loose'])

    eff_syst['eff_R_T_lead'] = int_syst['lead']['real']['tight'] / (int_syst['lead']['real']['tight']+int_syst['lead']['real']['loose'])
    eff_syst['eff_F_T_lead'] = int_syst['lead']['fake']['tight'] / (int_syst['lead']['fake']['tight']+int_syst['lead']['fake']['loose'])
    eff_syst['eff_R_L_lead'] = int_syst['lead']['real']['loose'] / (int_syst['lead']['real']['tight']+int_syst['lead']['real']['loose'])
    eff_syst['eff_F_L_lead'] = int_syst['lead']['fake']['loose'] / (int_syst['lead']['fake']['tight']+int_syst['lead']['fake']['loose'])


    # Do systematics
    # the integrals may already have some systematics
    # that are propagated to the eff_*
    # therefore, don't overwrite the existing 
    # systematics, but make a ufloat with a
    # zero value, and non-zero syst
    eff_syst['eff_R_L_lead'] = eff_syst['eff_R_L_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_R_L_lead'].n)*get_syst_uncertainty( 'RealTemplateNom', lead_reg, lead_ptrange, 'real', 'loose' ), 'Template_lead_real_loose')
    eff_syst['eff_F_L_lead'] = eff_syst['eff_F_L_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_F_L_lead'].n)*get_syst_uncertainty( 'FakeTemplate%s'%systematics, lead_reg, lead_ptrange, 'fake', 'loose' ), 'Template_lead_fake_loose' )
    eff_syst['eff_R_T_lead'] = eff_syst['eff_R_T_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_R_T_lead'].n)*get_syst_uncertainty( 'RealTemplateNom', lead_reg, lead_ptrange, 'real', 'loose' ), 'Template_lead_real_loose')
    eff_syst['eff_F_T_lead'] = eff_syst['eff_F_T_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_F_T_lead'].n)*get_syst_uncertainty( 'FakeTemplate%s'%systematics, lead_reg, lead_ptrange, 'fake', 'loose' ), 'Template_lead_fake_loose' )

    return eff_stat, eff_syst

def get_template_integrals( templates, cuts, lead_reg, lead_ptrange, systematics=None) :

    int_stat = {}
    int_stat['lead']={}
    int_stat['lead']['real']={}
    int_stat['lead']['fake']={}

    int_syst = {}
    int_syst['lead']={}
    int_syst['lead']['real']={}
    int_syst['lead']['fake']={}

    bins_lead_real_tight = ( templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][0] ), templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][1] ) )
    bins_lead_real_loose = ( templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][0] ), templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][1] ) )
    bins_lead_fake_tight = ( templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][0] ), templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][1] ) )
    bins_lead_fake_loose = ( templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][0] ), templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][1] ) )

    int_stat['lead']['real']['tight'] = get_integral_and_error( templates['lead']['real']['Data'], bins_lead_real_tight, 'Data_lead_real_tight' )
    int_stat['lead']['real']['loose'] = get_integral_and_error( templates['lead']['real']['Data'], bins_lead_real_loose, 'Data_lead_real_loose' )
    int_stat['lead']['fake']['tight'] = get_integral_and_error( templates['lead']['fake']['Data'], bins_lead_fake_tight, 'Data_lead_fake_tight' )
    int_stat['lead']['fake']['loose'] = get_integral_and_error( templates['lead']['fake']['Data'], bins_lead_fake_loose, 'Data_lead_fake_loose' )

    # If running with systematics, set the data systs to zero
    # May need to implement non-zero systematics for data in the future
    # The overall template systematics should not be set here
    int_syst['lead']['real']['tight'] = ufloat(int_stat['lead']['real']['tight'].n, 0.0 , 'Data_lead_real_tight' )
    int_syst['lead']['real']['loose'] = ufloat(int_stat['lead']['real']['loose'].n, 0.0 , 'Data_lead_real_loose' )
    int_syst['lead']['fake']['tight'] = ufloat(int_stat['lead']['fake']['tight'].n, 0.0 , 'Data_lead_fake_tight' )
    int_syst['lead']['fake']['loose'] = ufloat(int_stat['lead']['fake']['loose'].n, 0.0 , 'Data_lead_fake_loose' )

    # Subtract background

    if templates['lead']['real']['Background'] is not None :
        bkg_int_tight = get_integral_and_error( templates['lead']['real']['Background'], bins_lead_real_tight, 'Background_lead_real_tight' )
        bkg_int_loose = get_integral_and_error( templates['lead']['real']['Background'], bins_lead_real_loose, 'Background_lead_real_loose'  ) 

        syst_bkg_int_tight = ufloat( bkg_int_tight.n, math.fabs(bkg_int_tight.n)*get_syst_uncertainty('Background%s'%systematics , lead_reg, lead_ptrange, 'real', 'tight' ), 'Background_lead_real_tight' )
        syst_bkg_int_loose = ufloat( bkg_int_loose.n, math.fabs(bkg_int_loose.n)*get_syst_uncertainty( 'Background%s'%systematics, lead_reg , lead_ptrange, 'real', 'loose'), 'Background_lead_real_loose' )


        int_stat['lead']['real']['tight'] = int_stat['lead']['real']['tight'] + bkg_int_tight
        int_stat['lead']['real']['loose'] = int_stat['lead']['real']['loose'] + bkg_int_loose

        int_syst['lead']['real']['tight'] = int_syst['lead']['real']['tight'] + syst_bkg_int_tight
        int_syst['lead']['real']['loose'] = int_syst['lead']['real']['loose'] + syst_bkg_int_loose


    if templates['lead']['fake']['Background'] is not None :
        bkg_int_tight = get_integral_and_error( templates['lead']['fake']['Background'], bins_lead_fake_tight, 'Background_lead_fake_tight'  ) 
        bkg_int_loose = get_integral_and_error( templates['lead']['fake']['Background'], bins_lead_fake_loose, 'Background_lead_fake_loose'  ) 

        syst_bkg_int_tight = ufloat( bkg_int_tight.n, math.fabs(bkg_int_tight.n)*get_syst_uncertainty( 'Background%s'%systematics, lead_reg , lead_ptrange, 'fake', 'tight'), 'Background_lead_fake_tight' )
        syst_bkg_int_loose = ufloat( bkg_int_loose.n, math.fabs(bkg_int_loose.n)*get_syst_uncertainty( 'Background%s'%systematics, lead_reg , lead_ptrange, 'fake', 'loose'), 'Background_lead_fake_loose' )

        int_stat['lead']['fake']['tight'] = int_stat['lead']['fake']['tight'] + bkg_int_tight
        int_stat['lead']['fake']['loose'] = int_stat['lead']['fake']['loose'] + bkg_int_loose

        int_syst['lead']['fake']['tight'] = int_syst['lead']['fake']['tight'] + syst_bkg_int_tight
        int_syst['lead']['fake']['loose'] = int_syst['lead']['fake']['loose'] + syst_bkg_int_loose

    return int_stat, int_syst

def get_integral_and_error( hist, bins=None, name='' ) :

    err = ROOT.Double()
    if bins is None :
        val = hist.IntegralAndError( 1, hist.GetNbinsX(), err )
    else :
        if bins[1] is None :
            val = hist.IntegralAndError( bins[0], hist.GetNbinsX(), err )
        else :
            val = hist.IntegralAndError( bins[0], bins[1], err )

    return ufloat( val, err, name )


def get_single_photon_template( selection, binning, sample, reg, fitvar='sigmaIEIE', real=False) :

    if reg not in ['EB', 'EE'] :
        print 'Region not specified correctly'
        return None

    if real :
        var = 'ph_pt[0]:ph_%s[0]' %fitvar#y:x
    else :
        var = 'ph_pt[0]:ph_%s[0]' %fitvar#y:x

    selection = selection + ' && ph_Is%s[0] ' %( reg )

    data_samp_name = sample['Data']
    bkg_samp_name  = sample.get('Background', None)

    template_hists = {}

    data_samp = sampMan.get_samples(name=data_samp_name )

    if data_samp :
        template_hists['Data'] = clone_sample_and_draw( data_samp[0], var, selection, ( binning[0], binning[1], binning[2],100, 0, 500  ) ) 
    else :
        print 'Data template sample not found!'
        
    if bkg_samp_name is not None :
        bkg_samp = sampMan.get_samples(name=bkg_samp_name )
        var_bkg = 'ph_pt[0]:ph_%s[0]'%fitvar #y:x

        if bkg_samp :
            template_hists['Background'] = clone_sample_and_draw( bkg_samp[0], var_bkg, selection, ( binning[0], binning[1], binning[2],100, 0, 500  ) ) 
        else :
            print 'Background template sample not found!'
    else :
        template_hists['Background']=None

    return template_hists

def generate_eff_matrix( eff_dic ) :

    eff_matrix = [ [ eff_dic['eff_R_T_lead'], eff_dic['eff_F_T_lead'] ],
                   [ eff_dic['eff_R_L_lead'], eff_dic['eff_F_L_lead'] ] ]
    
    return eff_matrix


def solve_matrix_eq( matrix_ntries, vector_entries ) :

    ms = []
    mn = []
    for row in matrix_ntries :
        ms_row = []
        mn_row = []
        for col in row :
            ms_row.append( col.s )
            mn_row.append( col.n )
        ms.append( ms_row )
        mn.append( mn_row )

    matrix = unumpy.umatrix( mn, ms )

    print matrix

    vs = []
    vn = []
    for row in vector_entries :
        vn.append( [ row.n ] )
        vs.append( [ row.s ] )

    vector = unumpy.umatrix( vn, vs )
    
    inv_matrix = None
    try :
        inv_matrix = matrix.getI()
    except :
        print 'Failed to invert matrix, aborting'
        raise
        return None

    print inv_matrix
    print vector

    return inv_matrix*vector

def clone_sample_and_draw( samp, var, sel, binning ) :
        global sampMan
        newSamp = sampMan.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
        sampMan.create_hist( newSamp, var, sel, binning )
        return newSamp.hist

def save_templates( templates, outputDir, lead_ptrange=(None,None), namePostfix='' ) :

    if outputDir is None :
        return

    draw_templates = {'lead' : {}, 'subl' : {} }

    draw_templates['lead']['real'] = templates['lead']['real']['Data'].Clone( 'draw_%s' %templates['lead']['real']['Data'].GetName())
    draw_templates['lead']['fake'] = templates['lead']['fake']['Data'].Clone( 'draw_%s' %templates['lead']['fake']['Data'].GetName())

    if templates['lead']['real']['Background'] is not None :
        draw_templates['lead']['real'].Add( templates['lead']['real']['Background'])
    if templates['lead']['fake']['Background'] is not None :
        draw_templates['lead']['fake'].Add( templates['lead']['fake']['Background'])

    can_lead_real = ROOT.TCanvas('can_lead_real', '')
    can_lead_fake = ROOT.TCanvas('can_lead_fake', '')

    pt_label_lead = None
    if lead_ptrange[0] is not None :
        if lead_ptrange[1] == None :
            pt_label_lead = ' p_{T} > %d ' %( lead_ptrange[0] )
        else :
            pt_label_lead = ' %d < p_{T} < %d ' %( lead_ptrange[0], lead_ptrange[1] )

    draw_template( can_lead_real, draw_templates['lead']['real'], sampManFit, normalize=1, label=pt_label_lead, outputName = outputDir+'/template_lead_real%s.pdf' %namePostfix )
    draw_template( can_lead_fake, draw_templates['lead']['fake'], sampManFit, normalize=1, label=pt_label_lead, outputName = outputDir+'/template_lead_fake%s.pdf' %namePostfix )


def save_results( results, outputDir, namePostfix='' ) :

    if outputDir is None :
        return

    fname = outputDir + '/results%s.pickle' %namePostfix

    if not os.path.isdir( os.path.dirname( fname ) ) :
        os.makedirs( os.path.dirname( fname ) )
    file = open( fname, 'w' )
    pickle.dump( results, file )
    file.close()


#def draw_template(can, hists, normalize=False, first_hist_is_data=False, label=None, legend_entries=[], outputName=None ) :
#
#    if not isinstance(hists, list) :
#        hists = [hists]
#
#    can.cd()
#    can.SetBottomMargin( 0.12 )
#    can.SetLeftMargin( 0.12 )
#
#    added_sum_hist=False
#    if len(hists) > 1 and not first_hist_is_data or len(hists)>2 and first_hist_is_data :
#        if first_hist_is_data :
#            hists_to_sum = hists[1:]
#        else :
#            hists_to_sum = hists
#
#        sumhist = hists_to_sum[0].Clone( 'sumhist%s' %hists_to_sum[0].GetName())
#        for h in hists_to_sum[1:] :
#            sumhist.Add(h)
#
#        sumhist.SetLineColor(ROOT.kBlue+1)
#        sumhist.SetLineWidth(3)
#        hists.append(sumhist)
#        added_sum_hist=True
#
#    #get y size
#    maxbin = hists[0].GetBinContent(hists[0].GetMaximumBin())
#    for h in hists[1: ] :
#        if h.GetBinContent(h.GetMaximumBin() ) > maxbin :
#            maxbin = h.GetBinContent(h.GetMaximumBin() )
#
#    maxval_hist = maxbin * 1.25
#    if normalize :
#        maxval_axis = maxval_hist/hists[0].Integral()
#    else :
#        maxval_axis = maxval_hist
#        
#    for h in hists :        
#        h.GetYaxis().SetRangeUser( 0, maxval_hist )
#        h.GetXaxis().SetTitleSize( 0.05 )
#        h.GetXaxis().SetLabelSize( 0.05 )
#        h.GetYaxis().SetTitleSize( 0.05 )
#        h.GetYaxis().SetLabelSize( 0.05 )
#        h.GetYaxis().SetTitleOffset( 1.15 )
#        h.GetXaxis().SetTitle( '#sigma i#etai#eta' )
#        h.SetStats(0)
#        h.SetLineWidth( 2 )
#        bin_width = h.GetXaxis().GetBinWidth(1)
#
#        if first_hist_is_data :
#            h.GetYaxis().SetTitle( 'Events / %.3f ' %bin_width )
#        else :
#            h.GetYaxis().SetTitle( 'A.U. / %.3f ' %bin_width )
#
#    drawcmd=''
#    if not first_hist_is_data :
#        drawcmd += 'hist'
#
#    if normalize :
#        hists[0].DrawNormalized(drawcmd)
#        drawcmd+='hist'
#        for h in hists[1:] :
#            h.DrawNormalized(drawcmd + 'same')
#    else :
#        hists[0].Draw(drawcmd)
#        drawcmd+='hist'
#        for h in hists[1:] :
#            h.Draw(drawcmd + 'same')
#
#    leg=None
#    if legend_entries :
#        global sampMan
#        drawconf = DrawConfig( None, None, None, legend_config={'legendTranslateX' : -0.1 } )
#        leg = sampMan.create_standard_legend( len(hists) )
#        if added_sum_hist :
#            legend_entries.append( 'Template sum' )
#
#        for ent, hist in zip( legend_entries, hists ) :
#            leg.AddEntry( hist, ent )
#
#        leg.Draw()
#
#    if label is not None :
#        lab = ROOT.TLatex(0.3, 0.8, label )
#        lab.SetNDC()
#        lab.SetX(0.3)
#        lab.SetY(0.8)
#        lab.Draw()
#        
#    if outputName is None :
#        raw_input('continue')
#
#    if outputName is not None :
#        if not os.path.isdir( os.path.dirname(outputName) ) :
#            os.makedirs( os.path.dirname(outputName) )
#
#        can.SaveAs( outputName )

                                   

main()
