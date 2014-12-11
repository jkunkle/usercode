import os
import re
import pickle
import math
import ROOT
import collections
import datetime
from uncertainties import ufloat

rand = ROOT.TRandom3()
rand.SetSeed(31415)


def main() :

    print ' ----------------------------------------------------- '
    print ' BEGIN PROCESSING'
    print ' ----------------------------------------------------- '

    #run_onebin_fit(lands=True)

    #run_multptbin_fit(lands=True) 
    
    #run_allbin_fit_mcbkg() 

    #run_allbin_fit(lands=True) 

    #signal_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_09_24'
    #bkg_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_09_24'
    #signal_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_10_06'
    #bkg_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_10_06'
    signal_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_12_08'
    bkg_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_12_08'
    run_full_fit( signal_base, bkg_base, lands=False, combine=True)

def run_onebin_fit(lands=False) :

    onebin_name = 'onebin_fit'
    file_mgg = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_11_20/WggEventPlots/ph_pt_lead__mgg__baselineCuts.pickle'

    fit_onebin = FitConfig( name=onebin_name )

    ch_onebin = fit_onebin.create_channel(chName='OneBin')
    ch_onebin.AddSample( 'signal', file_mgg, 'Wgg', isSig=True, err={'Lumi' : 1.1} )
    ch_onebin.AddSample( 'background', file_mgg, 'All Bkg', err={'Stat' : None} )
    ch_onebin.AddData( file_mgg, ['Wgg', 'All Bkg'] )

    if lands :
        fit_onebin.create_lands_config()
    else :
        fit_onebin.create_config()
    #fit_onebin.run_fit()

def run_multptbin_fit(lands=False) :

    fit_name = 'multptbin_fit'
    in_files = {}
    filekey = 'ph_pt_lead__mgg__EB-EB__baselineCuts__ptbins_(\d+)-(\d+|\w+)\.pickle'
    file_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_11_20/WggEventPlots/'
    for file in os.listdir (file_base) :
        res = re.match( filekey, file )
        if res is not None :
            in_files[(res.group(1),res.group(2))]=file_base +'/'+file

    fit_multptbin = FitConfig( name=fit_name )

    for (min,max),f in  in_files.iteritems() :
        ch_bin = fit_multptbin.create_channel(chName='bin_%s_%s' %(min, max))
        ch_bin.AddSample( 'signal', f, 'Wgg', isSig=True, err={'Lumi' : 1.1 } )
        ch_bin.AddSample( 'background', f, 'All Bkg', err={'Stat' : None } )
        ch_bin.AddData( f, ['Wgg', 'All Bkg'] )

    if lands :
        fit_multptbin.create_lands_config()
    else :
        fit_multptbin.create_config()

def run_allbin_fit_mcbkg() :

    fit_name = 'allbin_fit'
    in_files = {}
    filekey = 'ph_pt_lead__mgg__(\w+)-(\w+)__baselineCuts__ptbins_(\d+)-(\d+|\w+)\.pickle'

    file_base = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_11_20/WggEventPlots/'
    for file in os.listdir (file_base) :
        res = re.match( filekey, file )
        if res is not None :
            in_files[(res.group(1),res.group(2),res.group(3), res.group(4))]=file_base +'/'+file

    fit_allbin = FitConfig( name=fit_name )

    for (r1, r2, min,max),f in  in_files.iteritems() :
        ch_bin = fit_allbin.create_channel(chName='bin_%s-%s_%s_%s' %(r1, r2, min, max))
        ch_bin.AddSample( 'signal', f, 'Wgg', isSig=True )
        ch_bin.AddSample( 'background', f, 'All Bkg' )
        ch_bin.AddData( f, ['Wgg', 'All Bkg'], generate=True )

    fit_allbin.create_config()
    ##fit_onebin.run_fit()

def run_full_fit(event_base, bkg_base, lands=False, combine=False) :

    fit_name = 'full_fit'
    #filekey_signal_mgg = 'ph_pt_lead__mgg__(\w+)-(\w+)__baselineCuts__ptbins_(\d+)-(\d+|\w+)(__subpt_(\d+)-(\d+|max)){0,1}\.pickle'
    #filekey_signal_egg = 'ph_pt_lead__egg__(\w+)-(\w+)__allZrejCuts__ptbins_(\d+)-(\d+|\w+)(__subpt_(\d+)-(\d+|max)){0,1}\.pickle'
    filekey_signal_mgg = 'ph_pt_lead__mgg__(\w+)-(\w+)__baselineCuts__ptbins_(\d+)-(\d+|\w+)\.pickle'
    filekey_signal_egg = 'ph_pt_lead__egg__(\w+)-(\w+)__allZrejCuts__ptbins_(\d+)-(\d+|\w+)\.pickle'
    filekey_bkg    = 'results_(\w+)-(\w+)_pt_(\d+)_(\d+|\w+)\.pickle'

    in_files_signal = {}
    in_files_signal['egg'] = {}
    in_files_signal['mgg'] = {}
    file_base_signal = '%s/WggEventPlots/' %event_base
    for file in os.listdir (file_base_signal) :
        res_mgg = re.match( filekey_signal_mgg, file )
        if res_mgg is not None :
            if res_mgg.group(1) == 'EE' and res_mgg.group(2) == 'EE' :
                continue
            if len( res_mgg.groups() ) <= 4 :
                in_files_signal['mgg'][(res_mgg.group(1),res_mgg.group(2),res_mgg.group(3), res_mgg.group(4))]=file_base_signal +'/'+file
            else :
                in_files_signal['mgg'][(res_mgg.group(1),res_mgg.group(2),res_mgg.group(3), res_mgg.group(4),res_mgg.group(6), res_mgg.group(7))]=file_base_signal +'/'+file

        res_egg = re.match( filekey_signal_egg, file )
        if res_egg is not None :
            if res_egg.group(1) == 'EE' and res_egg.group(2) == 'EE' :
                continue
            if len( res_egg.groups() ) <= 4 :
                in_files_signal['egg'][(res_egg.group(1),res_egg.group(2),res_egg.group(3), res_egg.group(4))]=file_base_signal +'/'+file
            else :
                in_files_signal['egg'][(res_egg.group(1),res_egg.group(2),res_egg.group(3), res_egg.group(4),res_egg.group(6), res_egg.group(7))]=file_base_signal +'/'+file

    if len( in_files_signal['mgg'].keys() ) != 12 :
        print 'Did not get 12 muon bins'
        print in_files_signal
        return
    if len( in_files_signal['egg'].keys() ) != 12 :
        print 'Did not get 12 electron bins'
        print in_files_signal
        return

    in_files_bkg = {}
    file_base_bkg = '%s/BackgroundEstimates/' %bkg_base
    file_jet = {}
    file_jet['egg'] = '%s/jet_fake_results__egg_allZRejCuts.pickle' %file_base_bkg
    file_jet['mgg'] = '%s/jet_fake_results__mgg.pickle' %file_base_bkg
    file_ele        = '%s/electron_fake_results.pickle' %file_base_bkg
    file_ele_syst   = '%s/electron_fake_results.pickle' %file_base_bkg
        
    fit_allbin = FitConfig( name=fit_name )

    regions = [('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB')]
    ptbins = ['15', '25', '40', '70', 'max']
    regions = [('EB', 'EB')]
    #sublbins = [ ('70', 'max', '15', '40'), ('70', 'max', '40', 'max') ]
    sublbins=[]
    for ch, ch_entries in in_files_signal.iteritems() :
        if ch=='egg' :
            continue
        for r1, r2 in regions :
            for bidx, min in enumerate( ptbins[:-1] ) :
                max = ptbins[bidx+1]

                f = ch_entries[(r1,r2,min,max)]
                
                ch_bin = fit_allbin.create_channel(chName='bin__%s__%s-%s_%s_%s' %(ch, r1, r2, min, max))

                # --------------------
                # not working
                # --------------------
                #ch_bin.AddSample( 'signal_%s' %ch, f, 'Wgg', isSig=True, err={'Lumi' : 1.1 }  )
                #ch_bin.AddSample( 'jetfake__%s__sum'%ch, file_jet[ch], ['stat+syst', 'sum', (r1, r2, min,max), 'result'], 
                #                 err={'Stat_jetfake__%s__sum_%s-%s_%s-%s'%(ch, r1, r2, min, max) : ( file_jet[ch], ['stat', 'sum', (r1, r2, min,max), 'result'] ) ,
                #                      'Syst_jetfake__%s__sum_%s-%s_%s-%s'%(ch, r1, r2, min, max) : ( file_jet[ch], ['syst', 'sum', (r1, r2, min,max), 'result'] ) , 
                #                      'Syst_jetfake_closure' : 1.10, 
                #                      } 
                #                )
                #if ch=='egg' :
                #    ch_bin.AddSample( 'elefake__egg', file_ele, ['stat+syst', 'sum', (r1, r2, min,max), 'result'], 
                #                     err={'Stat_elefake__egg__%s-%s_%s-%s'%(r1, r2, min, max)    : (file_ele, ['stat', 'sum', (r1,r2,min,max), 'result']),
                #                          'EleSyst_elefake__egg__%s-%s_%s-%s'%(r1, r2, min, max) : (file_ele, ['elesyst', 'sum', (r1,r2,min,max), 'result']),
                #                          'Syst_jetfake__egg__sum_%s-%s_%s-%s'%(r1, r2, min, max) : (file_ele, ['jetsyst', 'sum', (r1,r2,min,max), 'result']),
                #                          'Syst_elefake_closure' : 1.15,
                #                         } 
                #                    )

                # ---------------------------------
                # don't separate systematics by channel
                # ---------------------------------
                ch_bin.AddSample( 'signal_%s' %ch, f, 'Wgg', isSig=True, err={'Lumi' : 1.1 }  )
                ch_bin.AddSample( 'jetfake__%s__sum'%ch, file_jet[ch], ['stat+syst', 'sum', (r1, r2, min,max), 'result'], 
                                 err={'Stat_jetfake__%s__sum'%(ch) : ( file_jet[ch], ['stat', 'sum', (r1, r2, min,max), 'result'] ) ,
                                      'Syst_jetfake__%s__sum'%(ch) : ( file_jet[ch], ['syst', 'sum', (r1, r2, min,max), 'result'] ) , 
                                      'Syst_jetfake_closure' : 1.10, 
                                      } 
                                )
                if ch=='egg' :
                    ch_bin.AddSample( 'elefake__egg', file_ele, ['stat+syst', 'sum', (r1, r2, min,max), 'result'], 
                                     err={'Stat_elefake__egg__%s-%s_%s-%s'%(r1, r2, min, max)    : (file_ele, ['stat', 'sum', (r1,r2,min,max), 'result']),
                                          'EleSyst_elefake__egg__%s-%s_%s-%s'%(r1, r2, min, max) : (file_ele, ['elesyst', 'sum', (r1,r2,min,max), 'result']),
                                          'Syst_jetfake__egg__sum_%s-%s_%s-%s'%(r1, r2, min, max) : (file_ele, ['jetsyst', 'sum', (r1,r2,min,max), 'result']),
                                          'Syst_elefake_closure' : 1.15,
                                         } 
                                    )
                #if ch=='mgg' :
                #    ch_bin.AddSample( 'elefake__mgg', )

                ch_bin.AddData( use_sample_sum=True, generate=True)

            #for minl, maxl, mins, maxs in  sublbins :

            #    f = ch_entries[(r1,r2,minl,maxl,mins,maxs)]
            #    ch_bin = fit_allbin.create_channel(chName='bin__%s__%s-%s_%s_%s_sub_%s_%s' %(ch, r1, r2, minl, maxl, mins, maxs))

            #    ch_bin.AddSample( 'signal_%s' %ch, f, 'Wgg', isSig=True, err={'Lumi' : 1.1 }  )
            #    ch_bin.AddSample( 'jetfake__%s__real_fake'%ch, file_jet[ch], ['stat+syst', 'sum', (r1, r2, minl,maxl,mins,maxs)], 
            #    err={'Stat_jetfake__%s__real_fake_%s-%s_%s-%s_sub_%s-%s'%(ch, r1, r2, minl, maxl, mins, maxs) : (file_jet[ch], ['stat', 'sum', (r1,r2,minl,maxl,mins,maxs)] ), 
            #         'Syst_jetfake__%s__real_fake_%s-%s_%s-%s_sub_%s-%s'%(ch, r1, r2, minl, maxl, mins, maxs) : (file_jet[ch], ['syst', 'sum', (r1,r2,minl,maxl,mins,maxs)] ), 
            #         'Syst_jetfake_real_temp' : 1.10, 
            #         'Syst_jetfake_fake_temp': 1.20, 
            #         'Syst_jetfake_closure' : 1.05, 
            #         'Syst_jetfake_asym' : 1.15} 
            #                    )
            #    if ch=='egg' :
            #        ch_bin.AddSample( 'elefake__egg', file_ele, [(r1, r2, minl,maxl, mins,maxs)], err={'Stat_elefake__egg__%s-%s_%s-%s_sub_%s-%s'%(r1, r2, minl, maxl, mins, maxs) : 'Stat', 'Syst_elefake_closure' : 1.15, 'Syst_elefake_fit' : 1.2} )
            #    if ch=='mgg' :
            #        ch_bin.AddSample( 'elefake__mgg', )

            #    ch_bin.AddData( use_sample_sum=True, generate=True)
    if lands :
        fit_allbin.create_lands_config()
        fit_allbin.run_lands()
    elif combine :
        # lands config is the same as for combine
        fit_allbin.create_lands_config()
        fit_allbin.run_combine()
    else :
        fit_allbin.create_config()

def run_allbin_fit(lands=False) :

    fit_name = 'allbin_fit'
    filekey_signal = 'ph_pt_lead__mgg__(\w+)-(\w+)__baselineCuts__ptbins_(\d+)-(\d+|\w+)\.pickle'
    filekey_bkg    = 'results_(\w+)-(\w+)_pt_(\d+)_(\d+|\w+)\.pickle'

    in_files_signal = {}
    file_base_signal = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_11_20/WggEventPlots/'
    for file in os.listdir (file_base_signal) :
        res = re.match( filekey_signal, file )
        if res is not None :
            if res.group(1) == 'EE' and res.group(2) == 'EE' :
                continue
            in_files_signal[(res.group(1),res.group(2),res.group(3), res.group(4))]=file_base_signal +'/'+file

    in_files_bkg = {}
    file_base_bkg = '/afs/cern.ch/user/j/jkunkle/Plots/WggPlots_2014_11_20/JetFakeTemplateFitPlotsNomIso/CoarseBins/'
    for file in os.listdir (file_base_bkg) :
        res = re.match( filekey_bkg, file )
        if res is not None :
            maxval = res.group(4)
            if maxval == '1000000' :
                maxval='max'
            if res.group(1) == 'EE' and res.group(2) == 'EE' :
                continue

            in_files_bkg[(res.group(1),res.group(2),res.group(3), maxval)]=file_base_bkg +'/'+file


    fit_allbin = FitConfig( name=fit_name )

    for (r1, r2, min,max),f in  in_files_signal.iteritems() :
        ch_bin = fit_allbin.create_channel(chName='bin_%s-%s_%s_%s' %(r1, r2, min, max))

        file_bkg = in_files_bkg[( r1, r2, min, max)]

        ch_bin.AddSample( 'signal', f, 'Wgg', isSig=True, err={'Lumi' : 1.1 }  )
        ch_bin.AddSample( 'jetfake_real_fake', file_bkg, 'N_RF_TT', err={'Stat_jetfake_real_fake' : None} )
        ch_bin.AddSample( 'jetfake_fake_real', file_bkg, 'N_FR_TT', err={'Stat_jetfake_fake_real' : None} )
        ch_bin.AddSample( 'jetfake_fake_fake', file_bkg, 'N_FF_TT', err={'Stat_jetfake_fake_fake' : None} )

    if lands :
        fit_allbin.create_lands_config()
    elif combine :
        fit_allbin.create_lands_config()
    else :
        fit_allbin.create_config()

def get_xml_channel_header() :
    return '<!DOCTYPE Channel  SYSTEM \'HistFactorySchema.dtd\'>'

def get_xml_combination_header() :
    return '<!DOCTYPE Combination  SYSTEM \'HistFactorySchema.dtd\'>'

def generate_xml_line ( tag, attr={}, text='', lineclose=False, justclose=False ) :


    if justclose :
        atrtxt = '</%s> ' %tag
        return atrtxt

    atrtxt = '<%s' %tag
    for key, val in attr.iteritems():
        atrtxt+=' '
        atrtxt += '%s="%s" '%( key, val)

    if lineclose : 
        atrtxt += '>'
        atrtxt += text
        atrtxt += '</%s>' %tag
    else :
        atrtxt += ' >'

    return atrtxt

class ChannelConfig :

    def __init__( self, name, topdir ) :
        self.name = name
        self.filename = '%s/config/channel_%s.xml' %( topdir, self.name )
        self.rootfilename = '%s/data/%s.root' %( topdir, self.name )
        self.samples=collections.OrderedDict()
        self.datasamp={}

    def AddSample( self, name, files=[], fields=[], isSig=False, err={} ) :
        if not isinstance( files, list ) :
            files = [files]
        if not isinstance( fields, list ) :
            fields = [fields]

        self.samples[name] = { 'files' : files, 'fields' : fields, 'isSig' : isSig, 'err' : err }

    def AddData( self, files=[], fields=[], use_sample_sum=False,  generate=False ) :
        if not isinstance( files, list ) :
            files = [files]
        if not isinstance( fields, list ) :
            fields = [fields]
    
        self.datasamp = {'files' : files, 'fields' : fields, 'generate' : generate, 'use_sample_sum' : use_sample_sum }

    def create_hists( self ) :
        
        binlen=[]
        for sname ,samp in self.samples.iteritems() : 
            binlen.append(len( samp['files'] ) )
        binlen = list(set( binlen ))
        if len( binlen ) > 1 :
            print 'All samples should have the same number of input files'
            for sname ,samp in self.samples.iteritems() : 
                print sname
                print samp
            

        nBins = binlen[0]

        rootfile = ROOT.TFile.Open( self.rootfilename, 'RECREATE' )
        
        samp_hists = []
        for sname, samp in self.samples.iteritems() : 
            samp_hists.append(ROOT.TH1F( sname, sname, nBins, 0, nBins ))
            self.fill_hist_from_pickle( samp_hists[-1], samp['files'], samp['fields'] )

        samp_hists.append( ROOT.TH1F( 'data' ,'data', nBins, 0, nBins ))
        self.fill_hist_from_pickle( samp_hists[-1], self.datasamp['files'], self.datasamp['fields'] )
        if self.datasamp['generate'] :
            for bin in range( 0, nBins ) :
                genval = rand.Poisson( samp_hists[-1].GetBinContent(bin+1) )
                samp_hists[-1].SetBinContent( bin+1, genval )
                samp_hists[-1].SetBinError( bin+1, math.sqrt(genval) )

        for sh in samp_hists :
            sh.Write()

        rootfile.Close()

    def fill_hist_from_pickle(self, hist, files, fields) :

        data = self.get_data_from_pickle( files, fields)
        for idx, val in enumerate(data) :
            try :
                hist.SetBinContent(idx+1, val.n )
                hist.SetBinError(idx+1, val.s )
            except :
                print 'Did not get a ufloat from provided dict path!  Got, '
                print val

    def get_data_from_pickle(self, files, fields) :

        data = []

        for idx, f in enumerate(files) :

            ofile = open ( f, 'r' ) 
            finfo = pickle.load(ofile)

            val=None
            mod_fields = []
            for field in fields :
                if isinstance( field, str ) :
                    mod_fields.append( '\'%s\'' %field )
                elif isinstance( field, tuple ) :
                    mod_fields.append( '%s' %(field,) )
                else :
                    mod_fields.append(field)

            dic_eval = 'finfo[' + ']['.join( mod_fields ) + ']'

            val = eval(dic_eval)

            data.append( val )

        return data

    def get_data(self) :

        self.sampdata=collections.OrderedDict()
        self.data = {}

        for sname, samp in self.samples.iteritems() : 
            if samp['files'] and samp['fields'] :
                sdata = self.get_data_from_pickle( samp['files'], samp['fields'] )
                self.sampdata[sname] = { 'val' : sdata[0],'err' : samp['err']  }
            else :
                self.sampdata[sname] = { 'val' : ufloat(0, 0),'err' : None  }
                
        if self.datasamp['use_sample_sum'] :
            ddata = ufloat(0, 0)
            for sname, samp in self.samples.iteritems() : 
                if samp['isSig'] : 
                    continue
                samp_val = self.sampdata[sname]
                ddata = ddata + samp_val['val']
            self.data = {'val' : ddata }
        else :
            
            ddata = self.get_data_from_pickle( self.datasamp['files'], self.datasamp['fields'] )
            self.data = {'val' : ddata[0] }

        if self.datasamp['generate'] :
            genval = rand.Poisson( self.data['val'].n )
            self.data = {'val' : ufloat( genval, math.sqrt( genval ) ) }

    def generate_xml( self ) :

        text_lines = []

        text_lines.append( get_xml_channel_header() )
        text_lines.append( generate_xml_line( tag='Channel'   , attr={'Name' : self.name, 'InputFile' : self.rootfilename,                  }, lineclose=False, justclose=False ) )
        text_lines.append( generate_xml_line(     tag='Data'          , attr={'HistoName' : 'data', 'HistoPath' : '',                        }, lineclose=True, justclose=False ) )
        text_lines.append( generate_xml_line(     tag='StatErrorConfig', attr={'RelErrorThreshold' : '0.001', 'ConstraintType' : 'Poisson', }, lineclose=True, justclose=False ) )

        for sname, samp in self.samples.iteritems() :
            text_lines.append( generate_xml_line( tag='Sample', attr={'Name' : sname, 'HistoPath' : '', 'HistoName' : sname                  }, lineclose=False, justclose=False ) )
            if samp['isSig'] : 
                text_lines.append( generate_xml_line( tag='NormFactor', attr={'Name': 'SigXsecOverSM' , 'Val' : '1', 'Low':'0.', 'High':'10.' }, lineclose=True, justclose=False ) )
            else :
                text_lines.append( generate_xml_line( tag='StatError', attr={'Activate': 'True' }, lineclose=True, justclose=False ) )

            text_lines.append( generate_xml_line( tag='Sample', justclose=True) )


            #text_lines.append( generate_xml_line( tag='StatError', attr={'Activate' : 'True', 'HistoPath' : '', 'HistoName' : sname                  }, lineclose=False, justclose=False ) )

        text_lines.append( generate_xml_line( tag='Channel', justclose=True) )

        ofile = open( self.filename, 'w' )
        print 'Write to %s' %self.filename

        for line in text_lines :
            ofile.write( line + '\n' )

        ofile.close()


class FitConfig :

    def __init__(self, name) :
        self.name = name
        self.filename = '%s/config/config.xml' %name
        self.filename_lands = '%s/lands/config.txt' %name
        self.channels = []

        if not os.path.isdir( name ) :
            os.mkdir( name )
            os.mkdir( name + '/data')


    def create_channel(self, chName ) :

        newchannel = ChannelConfig( chName, topdir=self.name )
        self.channels.append(newchannel)
        return newchannel


    def create_config( self ) :

        print '------------------------------'
        print ' Run prepareHistFactory '
        print '------------------------------'

        os.system('prepareHistFactory %s' %self.name )
        rootsys = os.getenv( 'ROOTSYS' )
        if rootsys is None :
            print 'Could not locate ROOTSYS environment variable.  May have problems finding HistFactorySchema.dtd file'

        os.system( 'cp %s/etc/HistFactorySchema.dtd %s/config' %( rootsys, self.name ) )
        
        print '------------------------------'
        print ' Create histograms '
        print '------------------------------'

        for ch in self.channels  :
            ch.create_hists()

        print '------------------------------'
        print ' Create xmls'
        print '------------------------------'
        for ch in self.channels  :
            ch.generate_xml( )

        self.generate_xml()

        print '------------------------------'
        print ' Create Workspace'
        print '------------------------------'

        os.system( 'hist2workspace %s' %( self.filename ) )

    def create_lands_config( self ) :

        # tell channels to get their data
        for ch in self.channels :
            print ch.name
            print ch.filename
        for ch in self.channels :
            print ch.name
            ch.get_data()

        text_lines = []

        nsamps = [ len(c.samples) for c in self.channels ]
        nsamps = list( set(nsamps ) )

        if len(nsamps) > 1 :
            print 'Mismatch in number of samples between channels'

        nSamps = nsamps[0]

        # collect all systematics
        # each syst should have one line
        # but multiple samples could receive contributions
        # from each syst
        all_syst = {}
        for ch in self.channels :
            for sname, samp in ch.samples.iteritems() :
                for er, val in samp['err'].iteritems() :
                    all_syst.setdefault(  er, []).append( (ch.name, sname)  )

        nSyst = len( all_syst )

        text_lines.append( 'Wgg Fit %s %d-%d-%d' %(self.name, datetime.date.today().year, datetime.date.today().month, datetime.date.today().day ) )
        text_lines.append( 'imax %d number of channels'  %len(self.channels) )
        text_lines.append( 'jmax %d number of backgrounds'  %(nSamps-1) )
        text_lines.append( 'kmax %d number of systematics'  %(nSyst) )
        text_lines.append( 'Observation ' + '  '.join( ['%f' %ch.data['val'].n for ch in self.channels ] ) )

        bins_line_entries      = []
        proc_name_line_entires = []
        proc_int_line_entries  = []
        proc_val_line_entries  = []
        for  b, ch in enumerate( self.channels ) :
            bins_line_entries += ['%d'%(b+1)]*nSamps
            for idx, (sname, data) in enumerate(ch.sampdata.iteritems()) :
                proc_name_line_entires.append(sname)
                proc_int_line_entries.append( '%d' %idx)
                proc_val_line_entries.append( '%f' %(data['val'].n) )


        #one line for each syst
        syst_lines = []
        for systname, ch_samp_list in all_syst.iteritems() :
            syst_line = []
            #one entry for each channel, sample
            for ch in self.channels :

                for sname, data in ch.sampdata.iteritems() :
                    systval = 1.0 #default (no syst )

                    for ( chname, sampname  ) in ch_samp_list :
                        if chname != ch.name :
                            continue
                        if sampname != sname :
                            continue
                        systentry = data['err'][systname] # entry for this sample
                        if type(systentry) is float or type(systentry) is int :
                            systval = systentry
                        elif type(systentry) is tuple :
                            file = systentry[0]
                            if not isinstance( file, list ) :
                                file = [file]
                            fields = systentry[1]
                            dataval = ch.get_data_from_pickle( file, fields )[0]
                            if dataval.n != 0 :
                                systval = ( math.fabs(dataval.n) + dataval.s ) / math.fabs(dataval.n)

                    syst_line.append( '%f' %systval )

            syst_line.append( systname )

            syst_lines.append(syst_line )

        text_lines.append( 'bin ' + '  '.join(bins_line_entries) )
        text_lines.append( 'process ' + '  '.join(proc_name_line_entires) )
        text_lines.append( 'process ' + '  '.join(proc_int_line_entries) )
        text_lines.append( 'rate ' + '  '.join(proc_val_line_entries) )

        for idx, sl in enumerate(syst_lines) :
            text_lines.append( '%d  lnN  %s ' %( idx, '  '.join( sl ) ) )

        if not os.path.isdir( os.path.dirname( self.filename_lands ) ) :
            os.makedirs( os.path.dirname( self.filename_lands ) )

        text_file = open( self.filename_lands, 'w' )

        for lin in text_lines :
            text_file.write( lin + '\n' )
        text_file.close()


    def run_lands(self)  :
        #os.system( 'Lands/test/lands.exe -d %s -M Asymptotic  -rMin 1 -rMax 10' %self.filename_lands )
        os.system( 'echo Lands/test/lands.exe -d %s -M ProfileLikelihood --significance 1 -rMin 1 -rMax 10' %self.filename_lands )
        os.system( 'Lands/test/lands.exe -d %s -M ProfileLikelihood --significance 1 -rMin 1 -rMax 10' %self.filename_lands )

    def run_combine(self)  :
        #os.system( 'Lands/test/lands.exe -d %s -M Asymptotic  -rMin 1 -rMax 10' %self.filename_lands )
        os.system( 'echo combine -M ProfileLikelihood --signif --rMin 1 --rMax 10 %s ' %self.filename_lands )
        os.system( 'combine -M ProfileLikelihood --signif --rMin 1 --rMax 10 %s ' %self.filename_lands )

    def generate_xml( self ) :

        text_lines = []

        text_lines.append( get_xml_combination_header() )
        text_lines.append( generate_xml_line( tag='Combination' , attr={'OutputFilePrefix' : '.'.join(self.filename.split('.')[:-1])  }, lineclose=False, justclose=False ) )

        for ch in self.channels :
            text_lines.append( generate_xml_line(     tag='Input', text=ch.filename , lineclose=True, justclose=False ) )

        text_lines.append( generate_xml_line(     tag='Measurement', attr={'Name' : self.name, 'Lumi' : '1.', 'LumiRelErr' : '0.05'}, lineclose=False, justclose=False ) )
        text_lines.append( generate_xml_line(     tag='POI', text='SigXsecOverSM', lineclose=True, justclose=False ) )
        text_lines.append( generate_xml_line(     tag='Measurement', justclose=True ) )
        text_lines.append( generate_xml_line(     tag='Combination', justclose=True ) )

        ofile = open( self.filename, 'w' )
        print 'Write to %s' %self.filename

        for line in text_lines :
            ofile.write( line + '\n' )

        ofile.close()

def import_hist_from_inputs( workSpace, name, files, fields ) :

    if not isinstance( files, list ) :
        files = [files]

    bin_map = {}
    nBins=0
    for idx, file in enumerate(files) :
        bin_map[idx] = file
        nBins+=1
    
    data_map = {}
    for bin, file in bin_map.iteritems() :

        ofile = open( file, 'r') 
        entry_dic = pickle.load( ofile )
        if fields not in entry_dic :
            print 'Could not locate field %s' %fields
            continue
            
        data_map[bin] = entry_dic[fields]

    hist = ROOT.TH1F( 'hist_%s' %name, 'hist_%s' %name, nBins, 0, nBins )

    datahist = ROOT.RooDataHist( 'hist_%s' %name, 'hist_%s' %name, ROOT.RooArgList(workSpace.allVars().find('x')), hist )
    datapdf = ROOT.RooHistPdf( 'hist_%s' %name, 'hist_%s' %name, ROOT.RooArgSet(workSpace.allVars().find('x')), datahist  )

    getattr(workSpace,'import')(datapdf, 'hist_%s'%name)



main()
