# Parse command-line options
from argparse import ArgumentParser
import uuid
import os
import itertools
import pickle
from array import array

def parseArgs() :
    p = ArgumentParser()
    #p.add_argument('--fileName',     default='ntuple.root',  dest='fileName',        help='( Default ntuple.root ) Name of files')
    #p.add_argument('--treeName',     default='events'     ,  dest='treeName',        help='( Default events ) Name tree in root file')
    #p.add_argument('--samplesConf',  default=None,           dest='samplesConf',     help=('Use alternate sample configuration. '
    #                                                                                       'Must be a python file that implements the configuration '
    #                                                                                       'in the same manner as in the main() of this script.  If only '
    #                                                                                       'the file name is given it is assumed to be in the same directory '
    #                                                                                       'as this script, if a path is given, use that path' ) )

    #                                                                                       
    #p.add_argument('--xsFile',     default=None,  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
    #p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
    p.add_argument('--quiet',     default=False,  action='store_true',    dest='quiet',         help='Disable output')
    p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
    p.add_argument('--showPlots',     default=False,  action='store_true',    dest='showPlots',         help='show the fitted plots')
    
    return p.parse_args()

import ROOT
from uncertainties import ufloat
from uncertainties import unumpy
from SampleManager import SampleManager
from SampleManager import Sample
from SampleManager import DrawConfig

_sieie_cuts  = { 'EB' : (0.011,0.029), 'EE' : (0.033, 0.054) }
_chIso_cuts  = { 'EB' : (1.5, 15.0)  , 'EE' : (1.2,14.4) }
_neuIso_cuts = { 'EB' : (1.0,20)     , 'EE' : (1.5,20.5) }
_phoIso_cuts = { 'EB' : (0.7,20.3)   , 'EE' : (1.0,20  ) }

_sieie_cuts_tight  = { 'EB' : (0.006,0.011), 'EE' : (0.018, 0.033) }
_chIso_cuts_tight  = { 'EB' : (0, 1.5)  , 'EE' : (0, 1.2 ) }

_var_cuts = {'tight' : {} , 'loose' : {} }
_var_cuts['loose']['sigmaIEIE'] = _sieie_cuts
_var_cuts['loose']['chIsoCorr'] = _chIso_cuts
_var_cuts['tight']['sigmaIEIE'] = _sieie_cuts_tight
_var_cuts['tight']['chIsoCorr'] = _chIso_cuts_tight


def get_default_binning(bintype='fine', var='sigmaIEIE') :

    if bintype == 'fine' or bintype == 'two' :
        if var == 'sigmaIEIE' :
            return { 'EB' : (30, 0, 0.03), 'EE' : (30, 0, 0.09) }
        elif var == 'chIsoCorr' :
            return { 'EB' : (30, 0, 45), 'EE' : (35, 0, 42) }

        elif var == 'neuIsoCorr' :
            return { 'EB' : (40, -2, 38), 'EE' : (30, -2, 43) }
        elif var == 'phoIsoCorr' :
            return { 'EB' : (53, -2.1, 35), 'EE' : (42, -2, 40) }
    elif bintype == 'coarse' :
        if var == 'sigmaIEIE' :
            return { 'EB' : (10, 0, 0.03), 'EE' : (10, 0, 0.09) }
        elif var == 'chIsoCorr' :
            return { 'EB' : (30, 0, 45), 'EE' : (35, 0, 42) }

        elif var == 'neuIsoCorr' :
            return { 'EB' : (10, -2, 38), 'EE' : (10, -2, 43) }
        elif var == 'phoIsoCorr' :
            return { 'EB' : (53, -2.1, 35), 'EE' : (42, -2, 40) }


def get_default_fitrange(var='sigmaIEIE', upper_limit='medium') :

    if upper_limit == 'medium' :
        if var == 'sigmaIEIE' :
            return { 'EB' : (0.006, 0.02), 'EE' : (0.018, 0.054) }
        elif var == 'chIsoCorr' :
            return { 'EB' : (0, 15), 'EE' : (0, 14.4) }
    elif upper_limit == 'tight' :
        if var == 'sigmaIEIE' :
            return { 'EB' : (0.006, 0.015), 'EE' : (0.018, 0.038) }
        elif var == 'chIsoCorr' :
            return { 'EB' : (0, 9), 'EE' : (0, 8.4) }

def get_default_samples(ch='mu', template_type='real' ) :

    if template_type == 'real' :
        return 'Wgamma'


    if ch.count('mu')  :
        return { 'real' : {'Data' : 'Wgamma'}, 'fake' : {'Data' : 'Muon', 'Background' : 'RealPhotonsZg'}, 'target' : 'Muon' }
    elif ch.count('el') :
        return { 'real' : {'Data' : 'Wgamma'}, 'fake' : {'Data' : 'Muon', 'Background' : 'RealPhotonsZg'}, 'target' : 'Electron' }


def get_template_draw_strs( var, ch, template_type='cr' ) :

    # in the muon channel remove the pixel seed veto
    varstr = ''
    phstr = ''
    if template_type == 'cr' :
        if var == 'sigmaIEIE' :
            varstr = 'ph_mediumNoSIEIENoEleVeto_n'
            phstr = 'ptSorted_ph_mediumNoSIEIENoEleVeto_idx'
        elif var == 'chIsoCorr' :
            varstr = 'ph_mediumNoChIsoNoEleVeto_n'
            phstr = 'ptSorted_ph_mediumNoChIsoNoEleVeto_idx'
    elif template_type == 'sb' :
        if var == 'sigmaIEIE' :
            varstr = 'ph_mediumNoSIEIENoChIso_n'
            phstr = 'ptSorted_ph_mediumNoSIEIENoChIso_idx'
        elif var == 'chIsoCorr' :
            varstr = 'ph_mediumNoSIEIENoChIso_n'
            phstr = 'ptSorted_ph_mediumNoSIEIENoChIso_idx'

    return varstr, phstr

def get_real_template_draw_commands( var, ch='mu', template_type='cr') :

    (varstr, phstr) = get_template_draw_strs( var, ch)


    return 'mu_passtrig25_n>0 && mu_n==2 && %s == 1 && leadPhot_leadLepDR>0.4 && ph_truthMatch_ph[%s[0]] && abs(ph_truthMatchMotherPID_ph[%s[0]]) < 25 ' %( varstr, phstr, phstr )

def get_fake_template_draw_commands(var,  ch='mu', template_type='cr', met_cut=0 ) :

    (varstr, phstr) = get_template_draw_strs( var, ch, template_type )

    if template_type == 'cr' :
        return 'mu_passtrig25_n>0 && mu_n==2 && %s == 1 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ' %(varstr)
    elif template_type == 'sb' :
        if ch == 'muz' or ch == 'elz' :
            return ' mu_passtrig25_n>0 && mu_n==2 && %s == 1 && el_n==0 && dr_ph1_ph2 > 0.4 && pfType01MET > %d '%(varstr, met_cut)
        else :
            return ' mu_passtrig25_n>0 && mu_n==1 && %s == 1 && el_n==0 && dr_ph1_ph2 > 0.4 && mt_lep_met > 40 && pfType01MET > %d '%(varstr, met_cut)

    

def get_default_draw_commands( var, ch='mu', met_cut=0 ) :

    draw_commands = {}

    (varstr, phstr) = get_template_draw_strs( var, ch )

    el_base = ' el_passtrig_n>0   && el_n==1 && %s == 1 && mu_n==0 && dr_ph1_ph2 > 0.4 && mt_lep_met > 40 && pfType01MET > %d && !(m_trigelph1 > 76 && m_trigelph1 < 106 )   '%(varstr, met_cut )
    mu_base = ' mu_passtrig25_n>0 && mu_n==1 && %s == 1 && el_n==0 && dr_ph1_ph2 > 0.4 && mt_lep_met > 40 && pfType01MET > %d '%(varstr, met_cut)

    el_base_z = ' el_passtrig_n>0   && el_n==2 && %s == 1 && mu_n==0 && dr_ph1_ph2 > 0.4 && m_elel > 76 && m_elel < 106 && pfType01MET > %d   '%(varstr, met_cut)
    mu_base_z = ' mu_passtrig25_n>0 && mu_n==2 && %s == 1 && el_n==0 && dr_ph1_ph2 > 0.4 && m_mumu > 76 && m_mumu < 106 && pfType01MET > %d   '%(varstr, met_cut)

    if ch == 'mu' :
        return mu_base
    elif ch == 'el' :
        return el_base
    elif ch == 'muz' :
        return mu_base_z
    elif ch == 'elz' :
        return el_base_z

def main() :


    filename = 'tree.root'
    treename = 'ggNtuplizer/EventTree'
    xsFile = 'cross_sections/wgamgam.py'
    lumi = 19400
    samplesConf = 'Modules/StudyFits.py'

    global sampManLLG
    global sampManLG

    base_dir_llg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_11_09'
    base_dir_lg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_11_09'

    sampManLLG      = SampleManager(base_dir_llg, treename,filename=filename, xsFile=xsFile, lumi=lumi, quiet=options.quiet)
    sampManLG       = SampleManager(base_dir_lg , treename,filename=filename, xsFile=xsFile, lumi=lumi, quiet=options.quiet)


    if samplesConf is not None :

        sampManLLG.ReadSamples( samplesConf )
        sampManLG.ReadSamples( samplesConf )

    all_samp_man = []
    all_samp_man.append( sampManLLG )
    all_samp_man.append( sampManLG )


    calculators = []

    fitvars = [
                'sigmaIEIE',
                'chIsoCorr',
    ]
    channels = [
                'mu',
                'el',
                'muz',
                'elz',
    ]
    template_types = [
                      'cr',
                      'sb',
    ]
    binnings = [
                'fine', 
                ##'coarse', 
                #'two',
    ]
    upper_limits = [
                    'medium',
                    'tight',
    ]
    met_cuts = [
                0, 
                20,
    ]

    for conf in itertools.product( fitvars, channels, template_types, binnings, upper_limits, met_cuts )  :
        calculators.append( RunMultiFitting( fitvar=conf[0], channel=conf[1], template_type=conf[2], binning=conf[3], upper_limit=conf[4], met_cut=conf[5], output_dir=options.outputDir ) )






    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='muz', template_type='sb', binning='coarse', output_dir=options.outputDir ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='cr', output_dir=options.outputDir ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='cr', output_dir=options.outputDir ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='cr', output_dir=options.outputDir ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='cr', output_dir=options.outputDir ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='cr', binning='coarse', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='cr', binning='coarse', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='cr', binning='coarse', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='cr', binning='coarse', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='cr', binning='two', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='cr', binning='two', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='cr', binning='two', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='cr', binning='two', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='cr', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='cr', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='cr', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='cr', upper_limit='tight', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='cr', binning='coarse', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='cr', binning='coarse', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='cr', binning='coarse', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='cr', binning='coarse', upper_limit='tight', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='cr', binning='two', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='cr', binning='two', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='cr', binning='two', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='cr', binning='two', upper_limit='tight', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='sb', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='sb', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='sb', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='sb', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='sb', binning='coarse', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='sb', binning='coarse', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='sb', binning='coarse', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='sb', binning='coarse', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='sb', binning='two', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='sb', binning='two', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='sb', binning='two', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='sb', binning='two', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='sb', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='sb', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='sb', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='sb', upper_limit='tight', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='sb', binning='coarse', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='sb', binning='coarse', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='sb', binning='coarse', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='sb', binning='coarse', upper_limit='tight', output_dir=options.outputDir  ) )

    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='mu', template_type='sb', binning='two', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='sigmaIEIE', channel='el', template_type='sb', binning='two', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='mu', template_type='sb', binning='two', upper_limit='tight', output_dir=options.outputDir  ) )
    #calculators.append( RunMultiFitting( fitvar='chIsoCorr', channel='el', template_type='sb', binning='two', upper_limit='tight', output_dir=options.outputDir  ) )


    for calc in calculators :
        draw_configs = calc.ConfigHists()

    for s in all_samp_man  :
        s.run_commands()

    for calc in calculators :
        calc.execute()

    print '^_^ FINISHED ^_^'


class RunMultiFitting(  ) :


    def __init__( self, **kwargs ):

        self.configs = {}

        self.fitvar        = kwargs.get('fitvar'        , None          )
        self.ptbins        = kwargs.get('ptbins'        , [15,25,35,45,60, 80, 120, 1000000] )
        self.channel       = kwargs.get('channel'       , 'mu'          )
        self.binning       = kwargs.get('binning'       , 'fine'        )
        self.upper_limit   = kwargs.get('upper_limit'   , 'medium'      )
        self.template_type = kwargs.get('template_type' , 'cr'          )
        self.met_cut       = kwargs.get('met_cut'       , 0             )
        self.output_dir    = kwargs.get('output_dir'    , None          )

        if self.fitvar == 'sigmaIEIE' :
            self.fittitle = '#sigmai#etai#eta'
        if self.fitvar == 'chIsoCorr' :
            self.fittitle = 'charged Hadron Iso.'


        self.output_path = None 
        if self.output_dir is not None :

            self.output_dir = self.output_dir + '/Results_%s_%s_%s_%s_%s_CutMet%d' %(self.fitvar, self.channel, self.template_type, self.binning, self.upper_limit, self.met_cut)
            self.filename = 'hist.root'

            self.output_path = '%s/%s' %( self.output_dir, self.filename )

            if not os.path.isdir( self.output_dir ) :
                os.makedirs( self.output_dir )


    def ConfigHists( self, **kwargs ) :

        self.template_name_base = 'templates_%s_%s_%s' %( self.fitvar, self.channel, self.template_type )
        self.data_name_base     = 'data_%s_%s_%s'      %( self.fitvar, self.channel, self.template_type )

        sampManTemp = None
        if self.template_type == 'cr' :
            sampManTemp = sampManLLG
        if self.template_type == 'sb' :
            if self.channel == 'muz' or self.channel == 'elz' :
                sampManTemp = sampManLLG
            else :
                sampManTemp = sampManLG

        if self.channel == 'muz' or self.channel == 'elz' :
            sampManTarget = sampManLLG
        else :
            sampManTarget = sampManLG

        samp_mu = 'Muon'
        samp_el = 'Electron'
        samp_bkg  = 'Zg'
        samp_real = 'Zg'
        if self.template_type == 'sb' and (self.channel == 'mu' or self.channel == 'el' ) :
            samp_bkg = 'Wg'

        if self.channel.count('mu') :
            samp_data = samp_mu
        elif self.channel.count('el') :
            samp_data = samp_el

        self.configs.update( config_single_photon_plots ( sampManTemp, samp_mu, 'fake', self.binning, self.fitvar, self.channel, self.template_type, met_cut=self.met_cut, upper_limit=self.upper_limit, basename=self.template_name_base+'_fake_data') )
        self.configs.update( config_single_photon_plots ( sampManTemp, samp_bkg, 'fake', self.binning, self.fitvar, self.channel, self.template_type, met_cut=self.met_cut, upper_limit=self.upper_limit, basename=self.template_name_base+'_fake_bkg') )

        self.configs.update( config_single_photon_plots ( sampManLLG , samp_real, 'real', self.binning, self.fitvar, self.channel, self.template_type, met_cut=self.met_cut, upper_limit=self.upper_limit, basename=self.template_name_base+'_real') )

        self.configs.update( config_single_photon_plots ( sampManTarget  , samp_data, 'target', self.binning, self.fitvar, self.channel, self.template_type, met_cut=self.met_cut, upper_limit=self.upper_limit, basename=self.data_name_base) )

    def execute( self, **kwargs ) :

        regions = ['EB', 'EE']

        sampManTemp = None
        if self.template_type == 'cr' :
            sampManTemp = sampManLLG
        if self.template_type == 'sb' :
            if self.channel == 'muz' or self.channel == 'elz' :
                sampManTemp = sampManLLG
            else :
                sampManTemp = sampManLG

        if self.channel == 'muz' or self.channel == 'elz' :
            sampManTarget = sampManLLG
        else :
            sampManTarget = sampManLG

        fitrange = get_default_fitrange( self.fitvar, upper_limit=self.upper_limit )

        hists = {}

        for reg in regions :

            plot_ptbins = self.ptbins
            if plot_ptbins[-1] > 1000 :
                plot_ptbins[-1] = plot_ptbins[-2] + plot_ptbins[-3]

            hists[reg] = ROOT.TH1F( 'pthist_%s' %reg, '', len(plot_ptbins)-1, array('f', plot_ptbins))

            hist_fake_data = load_template_histograms( self.configs, self.template_name_base+'_fake_data_%s'%reg, sampManTemp )
            hist_fake_bkg  = load_template_histograms( self.configs, self.template_name_base+'_fake_bkg_%s'%reg, sampManTemp )

            # subtract background
            hist_fake_data.Add( hist_fake_bkg, -1 )

            hist_real      = load_template_histograms( self.configs, self.template_name_base+'_real_%s' %reg, sampManLLG )
            hist_target    = load_template_histograms( self.configs, self.data_name_base+'_%s' %reg, sampManTarget )

            #hist_fake_data.Draw( 'colz') 
            #raw_input('cont')
            #hist_real.Draw('colz')
            #raw_input('cont')
            #hist_target.Draw('colz')
            #raw_input('cont')

            for idx, ptmin in enumerate( self.ptbins[:-1] ) :
                ptmax = self.ptbins[idx+1]

                ptbinmin = hist_target.GetYaxis().FindBin( ptmin )
                ptbinmax = hist_target.GetYaxis().FindBin( ptmax ) - 1

                hist_real_px   = hist_real     .ProjectionX( str( uuid.uuid4()), ptbinmin, ptbinmax  )
                hist_fake_px   = hist_fake_data.ProjectionX( str( uuid.uuid4()), ptbinmin, ptbinmax  )
                hist_target_px = hist_target   .ProjectionX( str( uuid.uuid4()), ptbinmin, ptbinmax  )

                #print reg
                #print ptmin
                #print ptmax
                #hist_fake_px.Draw( 'colz') 
                #raw_input('cont')
                #hist_real_px.Draw('colz')
                #raw_input('cont')
                #hist_target_px.Draw('colz')
                #raw_input('cont')

                print 'region = %s, ptrange = %d-%d, bins = %d-%d' %( reg, ptmin, ptmax, ptbinmin, ptbinmax)


                if self.binning == 'two' :
                    result = RunMatrixSolution( hist_real_px, hist_fake_px, hist_target_px, _var_cuts['tight'][self.fitvar][reg], _var_cuts['loose'][self.fitvar][reg], output_dir=self.output_dir, file_postfix = '_%s_%d_%d' %( reg, ptmin, ptmax) )
                    hists[reg].SetBinContent( idx+1, result.n )
                    hists[reg].SetBinError( idx+1, result.s )
                else :
                    result = FitTemplates( hist_real_px, hist_fake_px, hist_target_px, fitrange[reg][0], fitrange[reg][1], _var_cuts['tight'][self.fitvar][reg][1], fittitle=self.fittitle, output_dir=self.output_dir, hist_postfix='_%s_%d_%d' %(reg, ptmin, ptmax) )
                    hists[reg].SetBinContent( idx+1, result.n )
                    hists[reg].SetBinError( idx+1, result.s )

        if self.output_path is not None :
            output_file = ROOT.TFile.Open( self.output_path, 'RECREATE') 

            for h in hists.values() :
                h.Write()

            output_file.Close()


def RunMatrixSolution( signal, background, target, cuts_tight, cuts_loose, output_dir=None, file_postfix='' ) :


    eff_signal     = get_hist_efficiencies( signal, cuts_tight, cuts_loose )
    eff_background = get_hist_efficiencies( background, cuts_tight, cuts_loose )
    entries_target = get_hist_integrals( target, cuts_tight, cuts_loose )

    # build the efficiencies
    eff= {}
    eff['eff_R_T'] = eff_signal['T']
    eff['eff_R_L'] = eff_signal['L']

    eff['eff_F_T'] = eff_background['T']
    eff['eff_F_L'] = eff_background['L']

    print 'efficiencies'
    print eff

    print 'data'
    print entries_target

    results = run_fit( {'T': entries_target['T'], 'L' : entries_target['L']}, eff )

    print results

    p_R_T = results.item(0)*eff['eff_R_T']
    p_R_L = results.item(0)*eff['eff_R_L']
    p_F_T = results.item(1)*eff['eff_F_T']
    p_F_L = results.item(1)*eff['eff_F_L']

    print 'nPred Real Tight = ', p_R_T
    print 'nPred Real Loose = ', p_R_L
    print 'nPred Fake Tight = ', p_F_T
    print 'nPred Fake Loose = ', p_F_L

    if output_dir is not None :
        output_results = {}
        output_results['efficiencies'] = eff
        output_results['data']         = entries_target
        output_results['alphas']      = {'R' : results.item(0), 'F' : results.item(1)}
        output_results['results']      = { 'p_R_T' : p_R_T, 'p_R_L' : p_R_L, 'p_F_T' : p_F_T, 'p_F_L' : p_F_L }

        output_file = open( '%s/results%s.pickle' %(output_dir, file_postfix) , 'w' )

        pickle.dump( output_results, output_file )

        output_file.close()



    
    return p_F_T
    

def get_hist_efficiencies( hist, cuts_tight, cuts_loose ) :

    eff_dic = {}

    integrals = get_hist_integrals( hist, cuts_tight, cuts_loose )

    if integrals['T'] == 0 :
        eff_dic['T'] = ufloat( 0, 0 )
    else :
        eff_dic['T'] = integrals['T']/( integrals['T'] + integrals['L'] )
    if integrals['L'] == 0 :
        eff_dic['L'] = ufloat( 0, 0 )
    else :
        eff_dic['L'] = integrals['L']/( integrals['T'] + integrals['L'] )

    return eff_dic

def get_hist_integrals( hist, cuts_tight, cuts_loose ) :

    integrals = {}

    bin_tight_min = hist.FindBin( cuts_tight[0] )
    bin_tight_max = hist.FindBin( cuts_tight[1] )

    if hist.GetXaxis().GetBinUpEdge(bin_tight_max-1) == cuts_tight[1] :
        bin_tight_max -= 1


    bin_loose_min = hist.FindBin( cuts_loose[0] )
    bin_loose_max = hist.FindBin( cuts_loose[1] )

    if hist.GetXaxis().GetBinUpEdge(bin_loose_max-1) == cuts_loose[1] :
        bin_loose_max -= 1


    int_t = 0
    err_t = ROOT.Double()
    int_l = 0
    err_l = ROOT.Double()
    int_t = hist.IntegralAndError( bin_tight_min, bin_tight_max, err_t )
    int_l = hist.IntegralAndError( bin_loose_min, bin_loose_max, err_l )

    integrals['T'] = ufloat( int_t, err_t )
    integrals['L'] = ufloat( int_l, err_l )

    return integrals



def run_fit( data, efficiencies ) :

    # make the matrix
    matrix = generate_eff_matrix( efficiencies )
    print matrix

    #do the fit!  Invert the matrix and multiply the by counts vectors
    results = solve_matrix_eq( matrix, [data['T'], data['L']] )

    return results 


def generate_eff_matrix( eff_dic ) :

    eff_matrix = [ [ eff_dic['eff_R_T'], eff_dic['eff_F_T'] ],
                   [ eff_dic['eff_R_L'], eff_dic['eff_F_L'] ] ]
    
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
        return unumpy.umatrix( [0.0, 0.0], [0.0, 0.0] )

    print inv_matrix
    print vector

    return inv_matrix*vector

def FitTemplates( signal, background, target, fitmin, fitmax, cutval, fittitle='xaxis', output_dir=None, hist_postfix='' ) :

    fit_objs = {}

    var = ROOT.RooRealVar( fittitle, fittitle, fitmin, fitmax )

    fit_objs['signal_template_hist'] = ROOT.RooDataHist( 'signal_template_hist', 'signal_template_hist', ROOT.RooArgList( var ), signal)
    fit_objs['signal_template']      = ROOT.RooHistPdf ( 'signal_template', 'signal_template', ROOT.RooArgSet( var ), fit_objs['signal_template_hist'] )
    
    fit_objs['background_template_hist'] = ROOT.RooDataHist( 'background_template_hist', 'background_template_hist', ROOT.RooArgList( var ), background)
    fit_objs['background_template']      = ROOT.RooHistPdf ( 'background_template', 'background_template', ROOT.RooArgSet( var ), fit_objs['background_template_hist'] )

    # build model
    sig_bkg_models = ROOT.TObjArray()
    sig_bkg_models.Add( fit_objs['signal_template'] )
    sig_bkg_models.Add( fit_objs['background_template'] )

    # fitted values
    fit_objs['nsig'] = ROOT.RooRealVar('N_{S}', 'signal events'    , 100,0,1000000.)
    fit_objs['nbkg'] = ROOT.RooRealVar('N_{B}', 'background events', 100,0,1000000.)

    sig_bkg_vars = ROOT.TObjArray()
    sig_bkg_vars.Add( fit_objs['nsig'] )
    sig_bkg_vars.Add( fit_objs['nbkg'] )


    fit_objs['model'] = ROOT.RooAddPdf('model', 'Template model', ROOT.RooArgList(sig_bkg_models), ROOT.RooArgList(sig_bkg_vars))

    # data
    fit_objs['target_data'] = ROOT.RooDataHist( 'target_data', 'target_data', ROOT.RooArgList(var), target)

    # do fit
    fit_objs['fit_result'] = fit_objs['model'].fitTo(fit_objs['target_data'],ROOT.RooFit.Range(fitmin, fitmax),ROOT.RooFit.SumW2Error(True),ROOT.RooFit.Save())
    
    can = ROOT.TCanvas( str(uuid.uuid4()), '' )
    frame = var.frame()
    fit_objs['target_data'].plotOn(frame)
    fit_objs['model'].plotOn(frame)
    fit_objs['model'].plotOn(frame, ROOT.RooFit.Components('signal_template'), ROOT.RooFit.LineStyle(ROOT.kDashed)) 
    fit_objs['model'].plotOn(frame, ROOT.RooFit.Components('background_template'), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor( ROOT.kRed ) ) 
    frame.SetTitle('')
    fit_objs['model'].Print()




    # get the fraction of the background template in the signal region
    bin_max = background.FindBin( cutval )
    if background.GetXaxis().GetBinUpEdge( bin_max-1) == cutval :
        bin_max -= 1 

    integral_sr = background.Integral( 1, bin_max )

    sr_frac = integral_sr / background.Integral()

    result = ufloat( fit_objs['nbkg'].getVal()*sr_frac,  fit_objs['nbkg'].getError()*sr_frac )

    frame.Draw()

    bkgtext = ROOT.TLatex(0.6, 0.7, 'NBkg = %.1f #pm %.1f ' %( result.n, result.s ) )
    bkgtext.SetNDC()
    bkgtext.SetX( 0.6 )
    bkgtext.SetY( 0.8 )
    bkgtext.SetTextFont( 42 ) 
    bkgtext.Draw()

    if options.showPlots :
        frame.Draw()
        bkgtext.Draw()
        raw_input('cont')
    if output_dir is not None :
        frame.Draw()
        bkgtext.Draw()
        can.SaveAs( '%s/fit_results%s.pdf' %(output_dir, hist_postfix) )



    return result

    


def config_single_photon_plots ( sampMan, sample, plot_type, bintype, fitvar, ch, template_type, met_cut=0, upper_limit='medium', basename='') :


    binning = get_default_binning(bintype, fitvar)

    if plot_type == 'real' :
        draw_str = get_real_template_draw_commands(fitvar, ch, template_type ) 
    elif plot_type == 'fake' : 
        draw_str = get_fake_template_draw_commands(fitvar, ch, template_type, met_cut ) 
    elif plot_type == 'target' :
        draw_str = get_default_draw_commands( fitvar, ch, met_cut )

    (phstr, idxstr) = get_template_draw_strs( fitvar, ch, template_type )

    fitrange = get_default_fitrange( fitvar, upper_limit ) 

    var = 'ph_pt[%s[0]]:ph_%s[%s[0]]' %(idxstr, fitvar, idxstr) #y:x

    selection_eb = draw_str + ' && ph_IsEB[%s[0]] ' %( idxstr)
    selection_ee = draw_str + ' && ph_IsEE[%s[0]] ' %( idxstr)

    if plot_type == 'fake' and template_type == 'sb' :
        # use tight inverted region for sidebands
        if fitvar == 'sigmaIEIE' :
            inv_range = _var_cuts['loose']['chIsoCorr']
            selection_eb += ' && ph_chIsoCorr[%s[0]] > %f && ph_chIsoCorr[%s[0]] < %f ' %( idxstr, inv_range['EB'][0], idxstr, inv_range['EB'][1] )
            selection_ee += ' && ph_chIsoCorr[%s[0]] > %f && ph_chIsoCorr[%s[0]] < %f ' %( idxstr, inv_range['EE'][0], idxstr, inv_range['EE'][1] )
        elif fitvar == 'chIsoCorr' :
            inv_range = _var_cuts['loose']['sigmaIEIE']
            selection_eb += ' && ph_sigmaIEIE[%s[0]] > %f && ph_sigmaIEIE[%s[0]] < %f ' %( idxstr, inv_range['EB'][0], idxstr, inv_range['EB'][1] )
            selection_ee += ' && ph_sigmaIEIE[%s[0]] > %f && ph_sigmaIEIE[%s[0]] < %f ' %( idxstr, inv_range['EE'][0], idxstr, inv_range['EE'][1] )

        # make the cut for the fit range
        selection_eb += ' && ph_%s[%s[0]] < %f ' %( fitvar, idxstr, fitrange['EB'][1] )
        selection_ee += ' && ph_%s[%s[0]] < %f ' %( fitvar, idxstr, fitrange['EE'][1] )

    template_configs = {}

    data_samp = sampMan.get_samples(name=sample )

    if data_samp :
        print '---------------------------------'
        print ' Draw %s for var %s        ' %(plot_type, fitvar)
        print 'Binning = ', binning
        print 'EB selection'
        print selection_eb
        print 'EE selection'
        print selection_ee
        print '---------------------------------'
    
        template_configs[basename+'_EB'] = config_and_queue_hist( data_samp[0], var, selection_eb, ( binning['EB'][0], binning['EB'][1], binning['EB'][2],100, 0, 500  ), useSampMan=sampMan ) 
        template_configs[basename+'_EE'] = config_and_queue_hist( data_samp[0], var, selection_ee, ( binning['EE'][0], binning['EE'][1], binning['EE'][2],100, 0, 500  ), useSampMan=sampMan ) 
    else :
        print 'template sample not found!'

    return template_configs

def config_and_queue_hist( samp, var, sel, binning, useSampMan=None ) :

    if useSampMan is not None :
        useSampMan.activate_sample( samp )
        draw_conf = DrawConfig( var, sel, binning, samples=samp )
        useSampMan.queue_draw( draw_conf )
        return draw_conf
    else :
        sampMan.activate_sample( samp )
        draw_conf = DrawConfig( var, sel, binning, samples=samp )
        sampMan.queue_draw( draw_conf)
        return draw_conf

def load_template_histograms( configs, name, sampMan ) :

    samps = sampMan.load_samples( configs[name] )

    if not samps : 
        print 'Could not get config %s' %name
    else :
        return samps[0].hist

        
if __name__ == '__main__' :
    options = parseArgs()
    if options.showPlots :
        ROOT.gROOT.SetBatch(False)
    else :
        ROOT.gROOT.SetBatch(True)
    
    main()
