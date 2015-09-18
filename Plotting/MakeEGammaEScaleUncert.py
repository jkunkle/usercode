# Parse command-line options
from argparse import ArgumentParser
options=None

from SampleManager import SampleManager
from SampleManager import Sample
from SampleManager import DrawConfig

import math

import ROOT

def parseArgs() :
    p = ArgumentParser()
    p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')

    return p.parse_args()

def main() :

    global sampManLL
    global sampManLG
    treeName = 'ggNtuplizer/EventTree'
    fileName = 'tree.root'
    xsFile   = 'cross_sections/wgamgam.py'
    lumi=19400

    samplesConf = 'Modules/EGammaUncert.py'

    base_dir_ll = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepEl_2015_06_23'
    base_dir_lg = '/afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepGammaNoPhID_2015_04_11'

    sampManLL      = SampleManager(base_dir_ll, treeName ,filename=fileName, xsFile=xsFile, lumi=lumi, quiet=options.quiet)
    sampManLG      = SampleManager(base_dir_lg, treeName ,filename=fileName, xsFile=xsFile, lumi=lumi, quiet=options.quiet)

    sampManLL.ReadSamples( samplesConf )
    sampManLG.ReadSamples( samplesConf )

    all_samp_man = []
    all_samp_man.append( sampManLG )
    all_samp_man.append( sampManLL )

    for s in all_samp_man  :
        s.deactivate_all_samples()

    calculators = []

    #calculators.append( DoPhotonEScaleUncert() )
    calculators.append( DoElectronEScaleUncert() )

    for calc in calculators :
        draw_configs = calc.ConfigHists()
        print draw_configs

    for s in all_samp_man  :
        s.run_commands()

    for calc in calculators :
        calc.execute()

class DoPhotonEScaleUncert() :

    def __init__ ( self, **kwargs ) :
        self.selection_base = ' el_passtrig_n>0 && el_n==1 && ph_n==1 && ph_passMedium[0] && leadPhot_leadLepDR>0.4 && mu_n==0 && m_lepph1 > 76 && m_lepph1 < 106'
        #self.selection_base = ' mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_passMedium[0] && leadPhot_leadLepDR>0.4 && el_n==0 && m_leplep < 80 && m_leplepph > 76 && m_leplepph  < 106'
        self.eta_bins = [ (None, 1.44), (1.57, 2.5) ]
        self.eta_labels = ['eb', 'ee']
        self.pt_bins = [(10, 20), (20, 30), (30, 40), ( 40, 50), (50, 70), (70, None ) ]

        self.configs_mc= {}
        self.configs_data= {}


    def ConfigHists( self, **kwargs ) :

        data_samp = sampManLG.get_samples( name='Electron' )
        mc_samp   = sampManLG.get_samples( name='Background' )

        if not data_samp :
            print 'Data sample does not exist!'
            return
        if not mc_samp :
            print 'MC sample does not exist!'
            return


        for (etamin, etamax), etalab in zip(self.eta_bins, self.eta_labels) :
            for ptmin, ptmax in self.pt_bins :

                if ptmax is None :
                    ptlab = 'pt_%d-max' %ptmin
                else :
                    ptlab = 'pt_%d-%d' %(ptmin,ptmax)

                self.configs_data['%s_%s'%( etalab, ptlab)] = config_egamma_hist( sampManLG, 'LepGamma', self.selection_base, data_samp[0], etamin, etamax, ptmin, ptmax )
                self.configs_mc['%s_%s'%( etalab, ptlab)]   = config_egamma_hist( sampManLG, 'LepGamma', self.selection_base, mc_samp[0]  , etamin, etamax, ptmin, ptmax )

        return (self.configs_data.values()+self.configs_mc.values())

    def execute( self, **kwargs ) :

        for name, conf_data in self.configs_data.iteritems() :
            hist_data = sampManLG.load_samples( conf_data )[0].hist

            hist_mc   = sampManLG.load_samples( self.configs_mc[name] )[0].hist

            print name

            hist_data.Scale( 1./hist_data.Integral() )
            hist_mc  .Scale( 1./hist_mc  .Integral() )
            hist_data.Draw()
            hist_mc.Draw('same')
            raw_input('cont')


            hist_variations = ROOT.TH1F( 'var_'+name,'var_'+name, 400, -5, 5 )

            for bin in range( 1, hist_data.GetNbinsX()+1 ) :
                data_val = hist_data.GetBinContent(bin)
                mc_val   = hist_mc  .GetBinContent(bin)
                if data_val == 0 :
                    continue
                hist_variations.Fill( math.fabs( data_val - mc_val )/data_val )

            hist_variations.Draw()
            raw_input('cont')
                
            hist_data.Divide( hist_mc ) 
            hist_data.Draw()
            raw_input('cont')


    def config_egamma_hist( sampMan, selection, sample, etamin, etamax, ptmin, ptmax=None ) :
    
        var = 'm_lepph1'
    
        if etamin is None :
            eta_sel = ' && fabs(ph_eta[0]) < %f' % etamax
        else :
            eta_sel = ' && fabs( ph_eta[0]) > %f && fabs( ph_eta[0] ) < %f ' %( etamin, etamax )
    
        if ptmax is None :
            pt_sel = ' && ph_pt[0] > %d ' %ptmin
        else :
            pt_sel = ' && ph_pt[0] > %d && ph_pt[0] < %d ' %(ptmin, ptmax )
    
        full_sel = selection + eta_sel + pt_sel
    
        sampMan.activate_sample( sample )
        draw_conf = DrawConfig( var, full_sel, ( 106-76, 76, 106 ), samples=sample )
        sampMan.queue_draw( draw_conf)
        return draw_conf
        

class DoElectronEScaleUncert() :

    def __init__ ( self, **kwargs ) :
        self.selection_base_lead = ' el_passtrig_n>0 && el_n==2 && mu_n==0 && m_leplep > 76 && m_leplep < 106 && el_triggerMatch[0]'
        self.selection_base_subl = ' el_passtrig_n>0 && el_n==2 && mu_n==0 && m_leplep > 76 && m_leplep < 106 && el_triggerMatch[1]'
        self.eta_bins = [ (None, 1.44), (1.44, 1.57), (1.57, 2.5) ]
        self.eta_labels = ['eb', 'ee']
        self.pt_bins = [(10, 20), (20, 30), (30, 40), ( 40, 50), (50, 70), (70, None ) ]

        self.configs_mc_lead   = {}
        self.configs_data_lead = {}

        self.configs_mc_subl   = {}
        self.configs_data_subl = {}


    def ConfigHists( self, **kwargs ) :

        data_samp = sampManLL.get_samples( name='Electron' )
        mc_samp   = sampManLL.get_samples( name='ZgammastarNoOlap' )

        if not data_samp :
            print 'Data sample does not exist!'
            return
        if not mc_samp :
            print 'MC sample does not exist!'
            return


        for (etamin, etamax), etalab in zip(self.eta_bins, self.eta_labels) :
            for ptmin, ptmax in self.pt_bins :

                if ptmax is None :
                    ptlab = 'pt_%d-max' %ptmin
                else :
                    ptlab = 'pt_%d-%d' %(ptmin,ptmax)

                self.configs_data_lead['%s_%s'%( etalab, ptlab)] = self.config_electron_hist( sampManLL, self.selection_base_lead, data_samp[0], etamin, etamax, ptmin, ptmax, 1 )
                self.configs_data_subl['%s_%s'%( etalab, ptlab)] = self.config_electron_hist( sampManLL, self.selection_base_subl, data_samp[0], etamin, etamax, ptmin, ptmax, 0 )
                self.configs_mc_lead  ['%s_%s'%( etalab, ptlab)] = self.config_electron_hist( sampManLL, self.selection_base_lead, mc_samp[0]  , etamin, etamax, ptmin, ptmax, 1 )
                self.configs_mc_subl  ['%s_%s'%( etalab, ptlab)] = self.config_electron_hist( sampManLL, self.selection_base_subl, mc_samp[0]  , etamin, etamax, ptmin, ptmax, 0 )

        return (self.configs_data_lead.values()+
                self.configs_mc_lead.values() +
                self.configs_data_subl.values()+
                self.configs_mc_subl.values() )

    def execute( self, **kwargs ) :

        for name, conf_data in self.configs_data_lead.iteritems() :
            hist_data = sampManLL.load_samples( conf_data )[0].hist
            hist_mc   = sampManLL.load_samples( self.configs_mc_lead[name] )[0].hist

            hist_data_subl = sampManLL.load_samples( self.configs_data_subl[name] )[0].hist
            hist_mc_subl   = sampManLL.load_samples( self.configs_mc_subl[name]   )[0].hist

            hist_data.Add( hist_data_subl )
            hist_mc.Add( hist_mc_subl )
            

            hist_data.Scale( 1./hist_data.Integral() )
            hist_mc  .Scale( 1./hist_mc  .Integral() )
            hist_data.Draw()
            hist_mc.Draw('same')
            raw_input('cont')


            hist_variations = ROOT.TH1F( 'var_'+name,'var_'+name, 400, -5, 5 )

            for bin in range( 1, hist_data.GetNbinsX()+1 ) :
                data_val = hist_data.GetBinContent(bin)
                mc_val   = hist_mc  .GetBinContent(bin)
                if data_val == 0 :
                    continue
                hist_variations.Fill( math.fabs( data_val - mc_val )/data_val )

            hist_variations.Draw()
            raw_input('cont')
                
            hist_data.Divide( hist_mc ) 
            hist_data.Draw()
            raw_input('cont')


    def config_electron_hist( self, sampMan, selection, sample, etamin, etamax, ptmin, ptmax, probeIdx ) :
    
        var = 'm_leplep'
    
        if etamin is None :
            eta_sel = ' && fabs(el_eta[%d]) < %f' %(probeIdx, etamax)
        else :
            eta_sel = ' && fabs( el_eta[%d]) > %f && fabs( el_eta[%d] ) < %f ' %( probeIdx, etamin, probeIdx, etamax )
    
        if ptmax is None :
            pt_sel = ' && el_pt[%d] > %d ' %( probeIdx, ptmin)
        else :
            pt_sel = ' && el_pt[%d] > %d && el_pt[%d] < %d ' %(probeIdx, ptmin, probeIdx, ptmax )
    
        full_sel = selection + eta_sel + pt_sel

        print full_sel
    
        sampMan.activate_sample( sample )
        draw_conf = DrawConfig( var, full_sel, ( (106-76)*4, 76, 106 ), samples=sample )
        sampMan.queue_draw( draw_conf)
        return draw_conf
        


if __name__ == '__main__' :
    options = parseArgs()
    main()

