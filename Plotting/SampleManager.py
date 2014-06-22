
import os
import sys
import math
import re
import imp
import ROOT
import copy
import uuid
import itertools
import eos_utilities
import random
from array import array
import time

ROOT.gROOT.SetBatch(False)
testarea = str(os.getenv("TestArea"))
atlasstylesearch=["/afs/cern.ch/user/j/jkunkle/public/AtlasStyle.C",
                  testarea+"/atlasstyle-00-03-04/AtlasStyle.C",
                  '/home/jkunkle/Programs/python/AtlasStyle.C']
for p in atlasstylesearch:
    if os.path.exists(p):
        ROOT.gROOT.LoadMacro(p)
        break

#ROOT.SetAtlasStyle()
ROOT.gStyle.SetPalette(1)

class Sample :
    """ Store information about one sample """

    def __init__ ( self, name, **kwargs ) :

        self.name = name
        self.hist = None

        # list of open files. Only used if extracting histograms
        self.ofiles = []

        # chain is the TChain for this sample.  
        # Will be created/overwritten if Addfiles is callled.  
        # Should not be filled for a sample group
        self.chain = kwargs.get('chain', None)

        # isActive determines if the sample will be drawn, default=True
        self.isActive = kwargs.get('isActive', True) 

        # if isData is true the sample will be drawn as points with an error bar, default=False
        self.isData   = kwargs.get('isData', False)

        # if isSignal is true the sample will be drawn as a line and not stacked, default=False
        self.isSignal = kwargs.get('isSignal', False)

        # if the sample is to be used as a ratio
        self.isRatio = kwargs.get('isRatio', False)

        # color determines the histogram or line color, default=black
        self.color = kwargs.get('color', ROOT.kBlack)

        # Provide a legend name.  by default the legend name will be the sample name
        self.legendName = kwargs.get('legendName', name)
        if self.legendName is None :
            self.legendName = name

        # if drawRatio is true, the ratio between this and the stack will be
        # drawn in the ratio box, default=False
        self.drawRatio = kwargs.get('drawRatio', False)

        # scale is the weight applied to this sample, default=1.0
        self.scale = kwargs.get('scale', 1.0)

        # groupedSamples is filled if this is a grouping of other samples.
        # if a sample is grouped, it is drawn as the sum of all entries
        # in this list.  Be careful to set isActive to False for the
        # sub samples or they will be drawn as well.  Grouped samples
        # can be further grouped default=[] 
        self.groupedSamples = kwargs.get('groupedSamples', [])

        # set a sample to temporary to delete it
        # when clear_all is called
        self.temporary = False

        self.failed_draw = False

    def SetHist( self, hist ) :
        self.hist = hist
        self.InitHist()

    def InitHist(self) :
        self.hist.SetLineColor( self.color )
        self.hist.SetMarkerColor( self.color )
        self.hist.SetTitle('')
        self.hist.Scale( self.scale )
        if self.isData :
            self.hist.SetMarkerStyle( 20 )
            self.hist.SetMarkerSize( 1.15 )
            self.hist.SetStats(0)
        if self.isSignal :
            self.hist.SetLineWidth(2)
        if self.isRatio :
            self.hist.SetMarkerStyle( 10 )
            self.hist.SetMarkerSize( 1.1 )
            #self.hist.SetNdivisions(509, True )


    def AddFiles( self, files, treeName=None, readHists=False ) :
        """ Add one or more files and grab the tree named treeName """

        if not isinstance(files, list) :
            files = [files]

        if treeName is not None :
            self.chain = ROOT.TChain(treeName, self.name)
            for file in files :
                self.chain.Add(file)

        if readHists :
            for file in files :
                self.ofiles.append( ROOT.TFile.Open( file ) )

    def AddGroupSamples( self, samples ) :
        """ Add subsamples to this sample """

        if not isinstance( samples, list) :
            samples = [samples]

        self.groupedSamples += samples

    def IsGroupedSample(self) :
        return ( len( self.groupedSamples ) > 0 )
    
class SampleManager :
    """ Manage input samples and drawn histograms """

    def __init__(self, base_path, treeName=None, mcweight=1.0, treeNameModel='events', filename='ntuple.root', base_path_model=None, xsFile=None, lumi=None, readHists=False, quiet=False) :

        #
        # This plotting module assumes that root files are 
        # organized under sample directories.  The directories
        # that are read are configured through the module passed
        # to ReadSamples
        #
        # All drawn objects are kept in SampleManager in variables
        # starting with curr_ 
        #

        #
        # path to directory containing samples
        # the samples that are read are configured through
        # the input module
        #
        self.base_path       = base_path 

        # the name of the tree to read
        self.treeName        = treeName

        # Name of the file.  This can be overwritten in the configuration module
        self.fileName        = filename

        #the name of the tree to read for models
        self.treeNameModel   = treeNameModel

        #
        # path to directory containing samples for models
        # the samples that are read are configured through
        # the input module
        #
        self.base_path_model = base_path_model

        
        # weight that is applied to all
        # samples not labeled as Data
        self.mcweight        = mcweight

        # store all samples
        self.samples               = []

        # store model samples
        self.modelSamples          = []

        # store the order that the samples were added
        # in the configuration module.  The samples
        # are stacked in this order
        self.stack_order                 = []

        # if the cross section file is given, open it
        # and grab the cross section map out of it
        self.weightMap = self.read_xsfile( xsFile, lumi )

        self.curr_hists            = {}
        self.curr_canvases         = {}
        self.curr_stack            = []
        self.curr_legend           = None

        self.legendLimits          = None

        self.legendLoc             = 'Nominal'
        self.legendCompress        = 1.0
        self.legendWiden           = 1.0
        self.legendTranslateX      = 0.0
        self.legendTranslateY      = 0.0
        # Save any plot decorations such as labels here
        # This guarantees that the objects stay in memory
        self.curr_decorations      = []

        # When variable binning is used the binning is stored
        # so that it can be used in future calls
        self.binning = None

        # read histograms instead of trees
        self.readHists = readHists

        self.quiet = quiet

        self.transient_data = {}

            
    #--------------------------------
    def create_sample( self, name, **kwargs ) :

        if name in self.get_sample_names() :
            print 'Sample with name %s already exists' %name
            return None

        new_sample = Sample( name=name )
        histval = kwargs.pop('hist', None)
        for arg, val in kwargs.iteritems() :
            if hasattr( new_sample, arg ) :
                setattr( new_sample, arg, val )

        if histval is not None :
            new_sample.SetHist( histval )

        self.samples.append(new_sample)
        return new_sample

    #--------------------------------
    def clone_sample( self, oldname, newname, **kwargs ) :

        _oldsample = self.get_samples( name=oldname )
        if _oldsample :
            oldsample = _oldsample[0]
        else :
            print 'Could not locate old sample'
            return None

        newsample = copy.copy( oldsample )
        newsample.name = newname
        
        histval = kwargs.pop('hist', None)
        for arg, val in kwargs.iteritems() :
            if hasattr( newsample, arg ) :
                setattr( newsample, arg, val )

        if histval is not None :
            newsample.SetHist( histval )
        else :
            newsample.hist=None

        self.samples.append(newsample)

        return newsample

    #--------------------------------
    def create_ratio_sample( self, name, num_sample, den_sample, color=ROOT.kBlack ) :

        if name in self.get_sample_names() :
            print 'Sample %s already exists!  Will not create!' %name
            return None

        if not isinstance( num_sample, Sample ) :
            num_sample_list = self.get_samples( name=num_sample )
            if not num_sample_list :
                print 'create_ratio_sample - ERROR : Numerator sample does not exist, %s' %num_sample
                return None
            num_sample = num_sample_list[0]

        if not isinstance( den_sample, Sample ) :
            den_sample_list = self.get_samples( name=den_sample )
            if not den_sample_list :
                print 'create_ratio_sample - ERROR : Denominator sample does not exist'
                return None
            den_sample = den_sample_list[0]

        ratio_hist = num_sample.hist.Clone( name )
        ratio_hist.Divide( den_sample.hist )

        ratio_hist.SetMarkerStyle(20)
        ratio_hist.SetMarkerSize(1.1)
        #ratio_hist.SetNdivisions(509, True )
        ratio_hist.SetStats(0)
        ratio_hist.SetTitle('')

        return self.create_sample( name=name, isRatio=True, hist=ratio_hist, temporary=True, color=color )

    #--------------------------------
    def config_legend(self, **kwargs ) :

        config = {}

        config['legendLoc']        = kwargs.get('legendLoc'        , 'Nominal')
        config['legendCompress']   = kwargs.get('legendCompress'   , 1.0)
        config['legendWiden']      = kwargs.get('legendWiden'      , 1.0)
        config['legendTranslateX'] = kwargs.get('legendTranslateX' , 0.0)
        config['legendTranslateY'] = kwargs.get('legendTranslateY' , 0.0)
        
        return config

    #--------------------------------
    def apply_lenged_conf(self, config ) :

        if config is None :
            return

        for key, val in config.iteritems() :
            if hasattr( self, key ) :
                setattr(self, key, val)

    #--------------------------------
    def get_samples(self, **kwargs) :

        # if no arguments provided, return all samples
        if not kwargs :
            return self.samples

        # collect results for each argument provided
        # then require and AND of samples matching each
        # criteria
        each_results = []
        for arg, val in kwargs.iteritems() :
            val_list = val
            if not isinstance(val_list, list) :
                val_list = [val_list]
            if hasattr( Sample(''), arg ) :
                each_results.append([ samp  for samp in self.samples if getattr( samp, arg ) in val_list])

        if not each_results :
            return []

        common_results = reduce( lambda x,y : set(x) & set(y), each_results )
        return list(common_results)
        ## default, return all samples
        #if names is None :
        #    return self.samples

        ## empty list provided, return empty list
        #if not names :
        #    return []

        #if not isinstance(names, list) :
        #    names = [names]

        #return filter( lambda x : x.name in names, self.samples )

    #--------------------------------
    def get_model_samples(self, names=[]) :
        if not isinstance(names, list) :
            names = [names]

        if names :
            return filter( lambda x : x.name in names, self.modelSamples )
        else :
           return self.modelSamples

    #--------------------------------
    def get_signal_samples(self) :
        return filter( lambda x : x.isSignal and x.isActive , self.samples )

    #--------------------------------
    def get_sample_names(self) :
        return [x.name for x in self.samples]
    
    #--------------------------------
    def get_model_sample_names(self) :
        return [x.name for x in self.modelSamples]


    #--------------------------------
    def add_decoration(self, obj) :
        self.curr_decorations.append(obj)

    #--------------------------------
    def activate_sample(self, samp_name) :
        sel_samps = self.get_samples(name=samp_name)
        if not sel_samps :
            print 'No sample with name %s' %samp_name
        elif len(sel_samps) > 1 :
            print 'Located multiple samples with name %s' %samp_name
        else :
            sel_samps[0].isActive=True

    #--------------------------------
    def deactivate_sample(self, samp_name) :
        sel_samps = self.get_samples(name=samp_name)
        if not sel_samps :
            print 'No sample with name %s' %samp_name
        elif len(sel_samps) > 1 :
            print 'Located multiple samples with name %s' %samp_name
        else :
            sel_samps[0].isActive=False

    #--------------------------------
    def clear_all(self) :
        """ clear all objects """

        self.clear_hists()

        for can in self.curr_canvases.values() :
            if can != None :
                can.Close()
        self.curr_canvases         = {}

        #if self.curr_stack != None :
        ##    self.curr_stack.Delete()
        #    self.curr_stack.Clear()
        #    self.curr_stack.Delete()
        if self.curr_legend != None :
            #self.curr_legend.Delete()
            self.curr_legend = None

        self.curr_decorations      = []

        self.legendLoc='Nominal'
        self.legendCompress=1.0
        self.legendWiden=1.0
        self.legendTranslateX=0.0
        self.legendTranslateY=0.0

        self.transient_data= {}

    #--------------------------------
    def clear_hists(self) :
        rm_samples = []
        for idx, samp in enumerate(self.samples) :
            samp.hist=None
            if samp.temporary :
                print 'removing sample %s' %samp.name
                rm_samples.append(samp)

        for samp in rm_samples:
            self.samples.remove(samp)

        for samp in self.modelSamples :
            samp.hist=None

    #--------------------------------
    def get_grouped_sample_names(self) :
        names = []
        for samp in self.samples :
            if samp.IsGroupedSample() :
                names.append(samp.name)

        return names
            
    #--------------------------------
    def place_extra_label(self, text, location=None) :

        label = ROOT.TLatex()
        label.SetNDC()
        label.SetTextSize( 0.05 )
        xval = 0.6
        yval = 0.7
        if location is None : 
            if self.curr_legend is not None :
                xval = self.curr_legend.GetX1()
                yval = self.curr_legend.GetY1()
                yval -= 0.1
        elif isinstance(location, tuple) : 
            xval = location[0]
            yval = location[1]
        elif location == 'TopLeft' :
            xval = 0.15
            yval = 0.85

        elif location == 'BottomLeft' :
            xval = 0.25
            yval = 0.25
        else :
            xval = 0.6
            yval = 0.7

        label.SetText(xval, yval, text)
        label.Draw()
        self.add_decoration( label )

    #--------------------------------
    def add_temp_sample(self, samp) :
        samp.temporary = True
        self.samples.append(samp)

    #--------------------------------
    def read_xsfile( self, file, lumi ) :
        weightMap = {}
        if file is None :
            return weightMap
        if lumi is None :
            print 'Cannot calculate weights without a luminosity'
            return weightMap
        if not os.path.isfile( file ) :
            print 'Could not locate cross section file.  No values will be loaded.'
            return weightMap

        ofile = open( file )
        xsdict = eval( ofile.read() )
        for name, values in xsdict.iteritems() :

            lumi_sample_den = values['cross_section']*values['gen_eff']*values['k_factor']
            if lumi_sample_den == 0 :
                print 'Cannot calculate cross section for %s.  It will receive a weight of 1.' %name
                lumi_sample = lumi
            else :
                lumi_sample = values['n_evt']/float(lumi_sample_den)

            lumi_scale = float(lumi)/lumi_sample;
            print 'Sample %s : lumi_sample = %f, scale = %f' %( name, lumi_sample, lumi_scale)

            weightMap[name] = lumi_scale

        return weightMap

    #--------------------------------
    def AddSample(self, name, path=None, filekey=None, isData=False, scale=None, isSignal=False, drawRatio=False, plotColor=ROOT.kBlack, lineColor=None, isActive=True, useXSFile=False, XSName=None, legend_name=None) :
        """ Create an entry for this sample """

        # get all root files under this sample
        input_files = []

        # accept path as string (-> single entry list) or list
        if not isinstance(path, list) :
            path = [path]

        # collect files from each path 
        #
        # keep a list of paths that have
        # been traveresed and print a warning
        # if we're reading inconsistent paths
        subpaths_used = []
        paths_used    = []

        input_files = self.collect_input_files( self.base_path, path, paths_used, subpaths_used, filekey=filekey) 

        if input_files :
            #
            # Print a warning if we might be getting the wrong files
            #
            n_unique_pathlenghts = len( set( [ len( upath.split('/') ) for upath in paths_used ] ) )
            if n_unique_pathlenghts > 1 :
                print 'Found ntuples in parent directories, these may be duplicates'

            thisscale = 1.0
            # multiply by command line MC weight only for MC
            #if self.mcweight is not None and not isData :
            if self.mcweight is not None  :
                thisscale *= self.mcweight

            # multply by scale provided to this function
            if scale is not None :
                thisscale *= scale

            if useXSFile :
                xsname = name
                if XSName is not None :
                    xsname = XSName
                if xsname in self.weightMap  :
                    thisscale *= self.weightMap[xsname]
                    print 'Update scale for %s' %name

            thisSample = Sample(name, isActive=isActive, isData=isData, isSignal=isSignal, color=plotColor, drawRatio=drawRatio, scale=thisscale, legendName=legend_name)
            thisSample.AddFiles( input_files, self.treeName, self.readHists )

            self.samples.append(thisSample)

            # keep the order that this sample was added
            if not isData and not isSignal and isActive :
                self.stack_order.append(name)

        print_prefix = "Reading %s (%s) " %(name, path )
        print_prefix = print_prefix.ljust(60)
        if not input_files :
            print print_prefix + " [ \033[1;31mFailed\033[0m  ]"
        else :
            if len(set(path) & set(subpaths_used)) != len(path) :
                print print_prefix + " [ \033[1;33mPartial\033[0m ]"
                print path
                print subpaths_used
            else :
                print print_prefix + " [ \033[1;32mSuccess\033[0m ]" 

    #--------------------------------
    def collect_input_files( self, base_path, path_list, paths_used, subpaths_used, filekey=None ) :

        input_files = []

        # if the necessary inputs are not provided return an empty list
        if base_path is None or path_list is None or not path_list :
            return input_files

        for subpath in path_list :
            fullpath = base_path + '/' + subpath
            # if files have been provided, read them directly
            if os.path.isfile(fullpath) :
                input_files.append(fullpath)
            else : #otherwise search directories for the needed files
                if base_path.count( 'root://eoscms' ) :
                    for top, dirs, files, sizes in eos_utilities.walk_eos( base_path + '/' + subpath ) :
                        for file in files :
                            if filekey is not None :
                                if file.count(filekey) == 0 : 
                                    continue
                            elif file.count(self.fileName) == 0 :
                                continue
                            paths_used.append(top)
                            subpaths_used.append(subpath)
                            input_files.append(top+'/'+file)
                            
                else : # local directories
                    for top, dirs, files in os.walk( base_path +'/' + subpath , followlinks=True) :
                        for file in files :
                            if filekey is not None :
                                if file.count(filekey) == 0 : 
                                    continue
                            elif file.count(self.fileName) == 0 :
                                continue
                            paths_used.append(top)
                            subpaths_used.append(subpath)
                            input_files.append(top+'/'+file)

        return input_files

    #--------------------------------
    def AddSampleGroup(self, name, input_samples=[], isData=False, scale=None, isSignal=False, drawRatio=False, plotColor=ROOT.kBlack, lineColor=None, legend_name=None, isActive=True) :
        """Make a new sample from any number of samples that have already been added via AddSample

           For example if a process is made of a number of individual samples that each have their
           own weight, first add those samples using AddSample with their own scale ( be sure
           to also give isActive=True or the individual samples will be drawn).  Then call
           Group Samples with the list of input samples and the new name.  
        """

        #check if input samples actually exist
        available_samples = []
        for samp in input_samples :
            if samp not in self.get_sample_names() :
                print 'WARNING - Child sample, %s, does not exist!' %samp
            else :
                available_samples.append(samp)

        # if no input samples exist, exit
        if not available_samples :
            return

        # keep the order that this sample was added
        if not isData and not isSignal and isActive :
            self.stack_order.append(name)

        thisscale = 1.0
        # multply by scale provided to this function (MCweight is applied to input samples)
        if scale is not None :
            thisscale *= scale
        
        print 'Grouping %s' %name
        thisSample = Sample(name, isActive=isActive, isData=isData, isSignal=isSignal, color=plotColor, drawRatio=drawRatio, scale=thisscale, legendName=legend_name)

        for samp in available_samples :

            is_a_grouped_sample = ( name in self.get_grouped_sample_names() )

            if is_a_grouped_sample :
                group_samples = self.get_samples(name=name)[0].groupedSamples
                thisSample.AddGroupSamples( group_samples )
            else :
                thisSample.AddGroupSamples( samp )

        self.samples.append(thisSample)
                
    def AddModelSampleGroup(self, name, input_samples=[], isData=False, scale=None, isSignal=False, drawRatio=False, plotColor=ROOT.kBlack, lineColor=None, legend_name=None, isActive=True) :
        """Make a new sample from any number of samples that have already been added via AddSample

           For example if a process is made of a number of individual samples that each have their
           own weight, first add those samples using AddSample with their own scale ( be sure
           to also give isActive=True or the individual samples will be drawn).  Then call
           Group Samples with the list of input samples and the new name.  
        """

        thisscale = 1.0
        # multply by scale provided to this function (MCweight is applied to input samples)
        if scale is not None :
            thisscale *= scale
        
        print 'Grouping %s' %name
        thisSample = Sample(name, isActive=isActive, isData=isData, isSignal=isSignal, color=plotColor, drawRatio=drawRatio, scale=thisscale, legendName=legend_name)

        for samp in input_samples :
            is_a_grouped_sample = ( name in self.get_grouped_sample_names() )

            if is_a_grouped_sample :
                group_samples = self.get_samples(name=name).groupedSamples
                thisSample.AddGroupSamples( group_samples )
            else :
                thisSample.AddGroupSamples( samp )

        self.modelSamples.append(thisSample)


    def AddModelSample(self, name, legend_name=None, path=None, scale=1.0 , filekey=None, plotColor=ROOT.kBlack) :
        input_files = []

        if not isinstance(path, list) :
            path = [path]

        # keep a list of paths that have
        # been traveresed and print a warning
        # if we're reading inconsistent paths
        subpaths_used = []
        paths_used    = []

        input_files = self.collect_input_files( self.base_path_model, path, paths_used, subpaths_used, filekey=filekey) 
        
        if input_files :
            #
            # Print a warning if we might be getting the wrong files
            #
            n_unique_pathlenghts = len( set( [ len( upath.split('/') ) for upath in paths_used ] ) )
            if n_unique_pathlenghts > 1 :
                print 'Found ntuples in parent directories, these may be duplicates'

            thisscale = 1.0
            if scale is not None :
                thisscale *= scale

            thisSample = Sample(name, color=plotColor, scale=thisscale, legend_name=legend_name)
            thisSample.AddFiles( self.treeNameModel, input_files )
            self.modelSamples.append(thisSample)

        print_prefix = "Reading %s (%s) " %(name, path )
        print_prefix = print_prefix.ljust(60)
        if not input_files :
            print print_prefix + " [ \033[1;31mFailed\033[0m  ]"
        else :
            if len(set(path) & set(subpaths_used)) != len(path) :
                print print_prefix + " [ \033[1;33mPartial\033[0m ]"
            else :
                print print_prefix + " [ \033[1;32mSuccess\033[0m ]" 


    def ReadSamples(self, conf) :
        ImportedModule=None

        ispath = ( conf.count('/') > 0 )
        module_path = None
        if ispath :
            module_path = conf
        else :
            #get path of this script
            script_path = os.path.realpath(__file__)
            module_path = os.path.dirname(script_path) + '/' + conf

        try :
            ImportedModule = imp.load_source(conf.split('.')[0], module_path)
        except IOError :
            print 'Could not import module %s' %module_path
        
        if hasattr(ImportedModule, 'config_samples') :
            ImportedModule.config_samples(self)
        else :
            print 'ERROR - samplesConf does not implement a function called config_samples '
            sys.exit(-1)

        
        if hasattr(ImportedModule, 'print_examples') :
            ImportedModule.print_examples()
        else :
            print 'WARNING - samplesConf does not implement a function called print_examples '


    def DrawHist(self, histpath, rebin=None, varRebinThresh=None, doratio=False, ylabel=None, xlabel=None, rlabel=None, logy=False, ymin=None, ymax=None, rmin=None, rmax=None, labelStyle=None ) :

        self.clear_all()
        self.extract_active_samples( histpath )

        if varRebinThresh is not None :
            self.variable_rebinning(varRebinThresh) 

        if rebin is not None :
            for samp in self.get_samples( isActive=True ) :
                if samp.hist is not None :
                    samp.hist.Rebin(rebin)

        self.MakeStack(histpath, doratio=doratio )

        if ylabel is None :
            binwidth = self.get_samples(isActive=True)[0].hist.GetBinWidth(1)
            ylabel = 'Events / %.1f GeV' %binwidth
        if rlabel is None :
            rlabel = 'Data / MC'
            
        self.DrawCanvas(self.curr_stack[-1], ylabel=ylabel, xlabel=xlabel, rlabel=rlabel, logy=logy, ymin=ymin, ymax=ymax, rmin=rmin, rmax=rmax, datahists=['Data'], sighists=self.get_signal_samples(), doratio=doratio, labelStyle=labelStyle)


    def Draw(self, varexp, selection, histpars=None, doratio=False, ylabel=None, xlabel=None, rlabel=None, logy=False, ymin=None, ymax=None, ymax_scale=None, rmin=None, rmax=None, showBackgroundTotal=False, backgroundLabel='AllBkg', removeFromBkg=[], addToBkg=[], useModel=False, treeHist=None, treeSelection=None, labelStyle=None, extra_label=None, extra_label_loc=None, generate_data_from_sample=None, replace_selection_for_sample={}, legendConfig=None  ) :

        print 'samples.Draw(\'%s\',  \'%s\', %s )' %( varexp, selection, str( histpars ) )
        self.clear_all()

        self.apply_lenged_conf( legendConfig )

        self.draw_active_samples( varexp, selection, histpars, replace_selection_for_sample=replace_selection_for_sample )

        if generate_data_from_sample is not None :
            samp_list = self.get_samples( name=generate_data_from_sample )
            if samp_list : 
                rand = ROOT.TRandom3()
                rand.SetSeed( int( time.time() ) )
                nbins = samp_list[0].hist.GetNbinsX()
                for bin in range( 1, nbins+1 ) :
                    newval = rand.Poisson( samp_list[0].hist.GetBinContent(bin) )
                    samp_list[0].hist.SetBinContent( bin, newval ) 
                    if newval > 0 :
                        samp_list[0].hist.SetBinError( bin, math.sqrt(newval) ) 


        if useModel :
            for sample in self.modelSamples :
                self.create_hist( sample, treeHist, treeSelection, histpars, isModel=True )

            # Model is created, replace the sample in self.samples with the
            # sample having the same name in self.modelSamples
            for samp in self.modelSamples :
                if samp.name in self.get_sample_names() :
                    self.get_samples(name=name).hist = samp.hist
                    self.get_samples(name=name).legendName = samp.legendName

        if len(histpars) == 4 :
            self.variable_rebinning(histpars[3]) 

        self.MakeStack(varexp, doratio, showBackgroundTotal, backgroundLabel, removeFromBkg, addToBkg, useModel, treeHist, treeSelection )

        if ylabel is None :
            bin_width = ( histpars[2] - histpars[1] )/histpars[0]
            bin_width_f = ( histpars[2] - histpars[1] )/float(histpars[0])
            if math.fabs(bin_width_f - bin_width) != 0 :
                ylabel = 'Events / %.1f GeV' %bin_width_f
            else :
                ylabel = 'Events / %d GeV' %bin_width
        if rlabel is None :
            rlabel = 'Data / MC'
            
        self.DrawCanvas(self.curr_stack[-1], ylabel=ylabel, xlabel=xlabel, rlabel=rlabel, logy=logy, ymin=ymin, ymax=ymax, ymax_scale=ymax_scale, rmin=rmin, rmax=rmax, datahists=['Data'], sighists=self.get_signal_samples(), doratio=doratio, labelStyle=labelStyle, extra_label=extra_label, extra_label_loc=extra_label_loc )


    def DrawSamples(self, varexp, selection, samples, histpars=None, normalize=False, doratio=False, useTreeModel=False, treeHist=None, treeSelection=None ) :
        if not isinstance( samples, list ) :
            samples = [samples]

        self.MakeSameCanvas(samples, varexp, selection, histpars, doratio)
        self.DrawSameCanvas(normalize, doratio)

    def MakeStack(self, stack_name, doratio=False, showBackgroundTotal=False, backgroundLabel='AllBkg', removeFromBkg=[], addToBkg=[], useModel=False, treeHist=None, treeSelection=None ) :

        # Get info for summed sample
        bkg_name = '__AllStack__'
        # get all stacked histograms and add them
        stack_samples = self.get_samples(name=self.stack_order, isActive=True)
    
        if stack_samples :
            sum_hist = stack_samples[0].hist.Clone(bkg_name)
            for samp in stack_samples[1:] :
                sum_hist.Add(samp.hist)

            self.create_sample( bkg_name, isActive=False, hist=sum_hist, temporary=True )

        if doratio :
            # when stacking, the ratio is made with respect to the data.  Find the sample that
            # is labeled as data.  Throw an error if one data sample is not found
            data_samples = self.get_samples(isData=True)
            if not data_samples :
                print 'MakeStack - ERROR : No data samples found!'

            self.create_ratio_sample( 'ratio', num_sample=data_samples[0], den_sample='__AllStack__' )

            # make ratio histograms for signal samples
            signal_samples = self.get_samples( isSignal=True, drawRatio=True )
            for sample in signal_samples :
                ratio_samp = self.create_ratio_sample( sample.name + '_ratio', num_sample=data_samples[0], den_sample=sample )
                ratio_samp.hist.SetLineColor( sample.color )
                ratio_samp.isSignal = True

        #make the stack and fill
        self.curr_stack.append(ROOT.THStack(str(uuid.uuid4()), ''))

        # reverse so that the stack is in the correct order
        orderd_samples = []
        for sampname in self.stack_order :
            samplist = self.get_samples(name=sampname, isActive=True )
            if samplist :
                orderd_samples.append(samplist[0])
        for samp in reversed(orderd_samples) :              
            samp.hist.SetFillColor( samp.color )
            samp.hist.SetLineColor( ROOT.kBlack )
            self.curr_stack[-1].Add(samp.hist, 'HIST')

        # additional formatting
        data_samp = self.get_samples(name='Data')

        # make the legend
        # In placing the legend move the bottom down 0.05 for each entry
        # calculate the step usa
        drawn_samples = []
        for sname in self.stack_order :
            drawn_samples+=self.get_samples( name=sname, failed_draw=False, isActive=True )
        step = len(drawn_samples)
        self.curr_legend = self.create_standard_legend(step, doratio)

        # format the entries
        tmp_legend_entries = []
        legend_entries = []

        if data_samp :
            tmp_legend_entries.append(  (data_samp[0].hist, data_samp[0].legendName, 'PE') )

        for samp in drawn_samples :
            tmp_legend_entries.append( ( samp.hist, samp.legendName,  'F') )

        for samp in self.get_signal_samples() :
            if samp.isActive :
                tmp_legend_entries.append( ( samp.hist, samp.legendName, 'L') )

        if self.legendLoc=='Double' :
            legend_entries = [None]*len(tmp_legend_entries)
            n_first_col = len(legend_entries)/2
            n_2nd_col = 0
            for idx in range(0, len(tmp_legend_entries) ) :
                if idx%2 == 0 : 
                    if idx <= n_first_col :
                        newidx = idx*2
                        legend_entries[newidx] = tmp_legend_entries[idx]
                    else :
                        n_2nd_col+=1
                        newidx = n_2nd_col*2-1
                        legend_entries[newidx] = tmp_legend_entries[idx]
                else : 
                    if idx <= n_first_col :
                        newidx = idx*2;
                        legend_entries[newidx] = tmp_legend_entries[idx]
                    else :
                        n_2nd_col+=1
                        newidx = n_2nd_col*2-1
                        legend_entries[newidx] = tmp_legend_entries[idx]

        else :
            legend_entries = tmp_legend_entries
        for le in legend_entries :
            self.curr_legend.AddEntry(le[0], le[1], le[2])


    #----------------------------------------------------
    def MakeSameCanvas(self, reqsamples, varexp, selections, histpars=None, useStoredBinning=False, ymin=None, ymax=None, ymax_scale=None, doratio=False, preserve_hists=False, useModel=False, treeHist=None, treeSelection=None, normalize=False, colors=[], drawHist=[]) :
        if not preserve_hists :
            self.clear_all()

        if not isinstance(selections, list) :
            selections = [selections]
        if not isinstance(reqsamples, list) :
            reqsamples = [reqsamples]

        samples = []
        print reqsamples
        for rsamp in reqsamples :
            samples += self.get_samples(name=rsamp) 
        # to make sure we get duplicate samples

        print selections
        print samples
        assert len(selections) == len(samples), 'selections and samples must have same length'

        if not colors :
            colors = [ s.color for s in samples ]
        if not drawHist :
            drawHist = [0]*len(samples)

        created_hists = []
        for idx, ( samp, sel ) in enumerate( zip(samples, selections) ) :
            # In this case the same sample may be drawn multiple
            # times.  to avoid any conflicts, add new samples
            # and draw into those
            newname = samp.name + str(idx)
            if newname in created_hists or newname in [x.name for x in self.get_samples()] :
                newname += str(idx)

            newsamp = self.clone_sample( oldname=samp.name, newname=newname, temporary=True )

            if useModel :
                self.create_hist( newsamp, treeHist, treeSelection, histpars, isModel=True)
            else :
                self.create_hist( newsamp, varexp, sel, histpars)

            created_hists.append(newname)

        if not created_hists :
            print 'No hists were created from samples %s' %(', '.join(reqsamples) )
            return created_hists

        if len(histpars) == 4 :
            self.variable_rebinning(histpars[3], created_hists, useStoredBinning=useStoredBinning) 

        created_samples = self.get_samples(name=created_hists)

        if doratio :
            self.create_top_canvas_for_ratio('same')
        else :
            self.create_standard_canvas('same')

        self.curr_canvases['same'].cd()

        self.DrawSameCanvas( self.curr_canvases['same'], created_samples, normalize=normalize, doratio=doratio, colors=colors, drawHist=drawHist, ymin=ymin, ymax=ymax, ymax_scale=ymax_scale )

        return created_hists

    def get_hist( self, sample, histpath ) :
        sampname = sample.name
        print 'Getting hist for %s' %sampname

        # check that this histogram hasn't been drawn
        if sample.hist is not None :
            print 'Histogram already extracted for %s' %sampname
            return


        # Draw the histogram.  Use histpars as the bin limits if given
        if sample.IsGroupedSample() :
            for subsampname in sample.groupedSamples :
                subsamp = self.get_samples( name=subsampname )[0]
                print 'Extract grouped hist %s' %subsampname
                if subsampname in self.get_sample_names() :
                    self.get_hist( subsamp, histpath )

            
            self.group_sample( sample )
            return

        else :

            thishist = sample.ofiles[0].Get(histpath).Clone()
            for ofile in sample.ofiles[1:] :
                thishist.Add( ofile.Get(histpath) )

            self.format_hist( sample, thishist )
    

    def create_hist( self, sample, varexp, selection, histpars, isModel=False ) :

        if isinstance( sample, str) :
            slist = self.get_samples( name=sample )
            if not slist :
                print 'Could not retrieve sample, %s' %sample
            if len(slist) > 1 :
                print 'Located multiple samples with name %s' %sample
            sample = slist[0]

        sampname = sample.name
    
        if not self.quiet : print 'Creating hist for %s' %sampname
        if not self.quiet : print selection

        ## check that this histogram hasn't been drawn
        #if sample.hist is not None :
        #    print 'Histogram already drawn for %s' %sampname
        #    return

        histname = str(uuid.uuid4())

        full_selection = selection

        thishist = None
        if type( histpars ) is tuple :
            if varexp.count(':') and not varexp.count('::') : # make a 2-d histogram
                if len(histpars) == 2 and type( histpars[0] ) is list and type(histpars[1]) is list :
                    thishist = ROOT.TH2F( histname, '', len(histpars[0])-1, array('f', histpars[0]), len(histpars[1])-1, array('f', histpars[1]) )
                    thishist.Sumw2()
                else :
                    if len(histpars) != 6 :
                        print 'varable expression requests a 2-d histogram, please provide 6 hist parameters, nbinsx, xmin, xmax, nbinsy, ymin, ymax'
                        return
                    thishist = ROOT.TH2F( histname, '', histpars[0], histpars[1], histpars[2], histpars[3], histpars[4], histpars[5])
                    thishist.Sumw2()
            else :
                thishist = ROOT.TH1F( histname, '', histpars[0], histpars[1], histpars[2])
                thishist.Sumw2()
        elif type( histpars ) is list :
            thishist = ROOT.TH1F( histname, '', len(histpars)-1, array('f', histpars))
            thishist.Sumw2()
        else :
            print 'No histogram parameters were passed'

        if thishist is not None :
            thishist.SetTitle( sampname )

        # Draw the histogram.  Use histpars as the bin limits if given
        if sample.IsGroupedSample() :
            for subsampname in sample.groupedSamples :
                subsamp = self.get_samples( name=subsampname )[0]
                
                if not self.quiet : print 'Draw grouped hist %s' %subsampname

                if isModel and subsampname in [s.name for s in self.get_model_samples()] :
                    self.create_hist( subsamp, varexp, selection, histpars, isModel=isModel )
                elif subsampname in self.get_sample_names() :
                    self.create_hist( subsamp, varexp, selection, histpars, isModel=isModel )

            self.group_sample( sample, isModel=isModel )

            return 

        else :
            if sample.chain is not None :
                sample.chain.Draw(varexp + ' >> ' + histname, full_selection, 'goff' )
                sample.failed_draw=False
            else :
                sample.failed_draw=True

        self.format_hist( sample, thishist )

    def format_hist( self, sample, hist ) :
        # account for overflow and underflow
        nbins       = hist.GetNbinsX()
        overflow    = hist.GetBinContent(nbins+1)
        overflowerr = hist.GetBinError  (nbins+1)
        underflow    = hist.GetBinContent(0)
        underflowerr = hist.GetBinError  (0)

        lastbincont  = hist.GetBinContent(nbins)
        lastbinerr   = hist.GetBinError  (nbins)
        firstbincont = hist.GetBinContent(1)
        firstbinerr  = hist.GetBinError  (1)

        if overflow != 0 :
            newcont = overflow + lastbincont
            if lastbincont == 0 :
                newconterr = overflowerr
            else :
                newconterr = math.sqrt( overflowerr * overflowerr + lastbinerr * lastbinerr )
            hist.SetBinContent(nbins, newcont)
            hist.SetBinError  (nbins, newconterr)
            hist.SetBinContent(nbins+1, 0)
            hist.SetBinError  (nbins+1, 0)

        if underflow != 0 :
            newcont = underflow + firstbincont
            if firstbincont == 0 :
                newconterr = firstbinerr
            else :
                newconterr = math.sqrt( underflowerr * underflowerr + firstbinerr * firstbinerr )
            hist.SetBinContent(1, newcont)
            hist.SetBinError  (1, newconterr)
            hist.SetBinContent(0, 0)
            hist.SetBinError  (0, 0)

        # get the histogram
        #sample.SetHist( hist.Clone() )
        sample.SetHist( hist.Clone() )

    def extract_active_samples( self, histpath ) :

        for sample in self.samples :
            if sample.isActive :
                self.get_hist( sample, histpath )

    def draw_active_samples( self, varexp, selection, histpars, replace_selection_for_sample={} ) :

        for sample in self.samples :
            if sample.isActive :
                this_selection = selection
                if sample.name in replace_selection_for_sample :
                    print 'REPLACING FOR'
                    print sample.name
                    this_selection = replace_selection_for_sample[sample.name]
                    print this_selection
                self.create_hist( sample, varexp, this_selection, histpars )

    def variable_rebinning(self, threshold=None, samples=[], useStoredBinning=False) :

        if not samples:
            samples = self.stack_order

        # variable r
        if threshold is not None :

            if useStoredBinning :
                binning = self.binning
            else :
                all_stack_hists = []
                for samp in self.get_samples(name=samples) :
                    all_stack_hists.append(samp.hist)

                binning = self.make_variable_binning( all_stack_hists, threshold)

                # store binning for future use
                self.binning = binning

            for samp in self.get_samples() :
                if samp.hist is not None :
                    samp.SetHist(self.do_variable_rebinning(samp, binning))

    def group_sample(self, sample, isModel=False) :

        if not sample.IsGroupedSample() :
            print 'Trying to group a sample that is not a grouped sample'
            return
        
        subsamps = sample.groupedSamples
        if not self.quiet : print 'RUN GROUPING FOR %s' %sample.name
        if not self.quiet : print subsamps

        
        if isModel :
            model_subsamps = self.get_model_samples(subsamps)
            sample.hist = model_subsamps[0].hist.Clone()
            for msamp in model_subsamps[1:] :
                sample.hist.Add( msamp.hist )
                sample.hist.Draw()
            #sample.hist.Scale(sample.scale)
            #self.modelSamples.append(sample)
        else :
            subsamps = self.get_samples(name=subsamps)

            sample.hist = subsamps[0].hist.Clone()
            for samp in subsamps[1:] :
                sample.hist.Add( samp.hist )
                #sample.hist.Draw()
            #sample.hist.Scale(sample.scale)

        sample.InitHist()

    def get_list_from_tree(self, vars, selection, sample ) :

        output = []

        if not isinstance( vars, list ) :
            vars = [vars]

        if sample.IsGroupedSample() :
            for subsampname in sample.groupedSamples :
                subsamp = self.get_samples( name=subsampname )[0]
                
                if not self.quiet : print 'running on grouped hist %s' %subsampname

                if subsampname in self.get_sample_names() :
                    output += self.get_list_from_tree( vars, selection, subsamp )

            return output

        else :

            sample.copied_tree = sample.chain.CopyTree( selection )

            nentries = sample.copied_tree.GetEntries()

            for i in xrange( 0, nentries ) :
                sample.copied_tree.GetEntry( i )
                evt_entries = []
                for var in vars :

                    newvar = var
                    #if an index is requested, get the name and index separately
                    res = re.match( '(\w+)\[(\d)\]', var )
                    if res is not None :
                        newvar = res.group(1)
                        idx = int(res.group(2) )
                        vec = getattr( sample.copied_tree, newvar )
                        evt_entries.append( vec[idx] )
                    else :
                        evt_entries.append( getattr( sample.copied_tree, var ) )

                evt_entries.append( sample.scale )

                output.append( tuple( evt_entries ) )

        return output

    def set_canvas_default_formatting(self, topcan, doratio, logy=False, ylabel=None ) :

        for prim in topcan.GetListOfPrimitives() :
            if isinstance(prim, ROOT.TH1F) :
                prim.SetTitle('')
                offset = 1.25
                if logy :
                    offset = 1.1
                if doratio == True or doratio == 1 : # canvas sizes differ for ratio, so title, label sizes are different
                    prim.GetYaxis().SetTitleSize(0.06)
                    prim.GetYaxis().SetTitleOffset(offset)
                    prim.GetYaxis().SetLabelSize(0.06)
                    prim.GetXaxis().SetLabelSize(0.06)
                    prim.GetXaxis().SetTitleSize(0.06)
                elif doratio == 2 : 
                    prim.GetYaxis().SetTitleSize(0.06)
                    prim.GetYaxis().SetTitleOffset(offset)
                    prim.GetYaxis().SetLabelSize(0.06)
                    prim.GetXaxis().SetLabelSize(0.06)
                    prim.GetXaxis().SetTitleSize(0.06)
                else :
                    prim.GetYaxis().SetTitleSize(0.05)
                    prim.GetYaxis().SetTitleOffset( offset )
                    prim.GetYaxis().SetLabelSize(0.05)
                    prim.GetXaxis().SetLabelSize(0.05)
                    prim.GetXaxis().SetTitleSize(0.05)
                    prim.GetXaxis().SetTitleSize(0.05)

    def set_stack_default_formatting(self, topcan, doratio, logy=False ) :
        if topcan.GetHists().GetSize() > 0 :
            offset = 1.25
            if logy :
                offset = 1.1
            if doratio : # canvas sizes differ for ratio, so title, label sizes are different
                topcan.GetHistogram().GetYaxis().SetTitleSize(0.06)
                topcan.GetHistogram().GetYaxis().SetTitleOffset(offset)
                topcan.GetHistogram().GetYaxis().SetLabelSize(0.06)
                topcan.GetHistogram().GetXaxis().SetLabelSize(0.06)
                topcan.GetHistogram().GetXaxis().SetTitleSize(0.06)
            else :
                topcan.GetHistogram().GetYaxis().SetTitleSize(0.05)
                topcan.GetHistogram().GetYaxis().SetTitleOffset(offset)
                topcan.GetHistogram().GetYaxis().SetLabelSize(0.05)
                topcan.GetHistogram().GetXaxis().SetLabelSize(0.05)
                topcan.GetHistogram().GetXaxis().SetTitleSize(0.05)

    def set_ratio_default_formatting(self, canvas, ratiosamps, doratio, rlabel, rmin=None, rmax=None ) :

            canvas.cd()

            for idx, ratiosamp in enumerate( ratiosamps ) :
                drawopt = 'same'
                if idx == 0 :
                    drawopt = ''
                if ratiosamp.isSignal :
                    drawopt += 'HIST'

                if doratio == True or doratio == 1 :
                    ratiosamp.hist.GetYaxis().SetTitleSize(0.10)
                    ratiosamp.hist.GetYaxis().SetTitleOffset(0.6)
                    ratiosamp.hist.GetYaxis().SetLabelSize(0.12)
                    ratiosamp.hist.GetXaxis().SetLabelSize(0.12)
                    ratiosamp.hist.GetXaxis().SetTitleSize(0.12)
                    ratiosamp.hist.GetXaxis().SetTitleOffset(1.0)
                elif doratio==2 :
                    ratiosamp.hist.GetYaxis().SetTitleSize(0.06)
                    ratiosamp.hist.GetYaxis().SetTitleOffset(0.8)
                    ratiosamp.hist.GetYaxis().SetLabelSize(0.06)
                    ratiosamp.hist.GetXaxis().SetLabelSize(0.06)
                    ratiosamp.hist.GetXaxis().SetTitleSize(0.06)
                    ratiosamp.hist.GetXaxis().SetTitleOffset(1.0)

                ratiosamp.hist.SetStats(0)
                ratiosamp.hist.SetMarkerStyle(20)
                ratiosamp.hist.SetMarkerSize(1.1)
                ratiosamp.hist.SetTitle('')
                ratiosamp.hist.GetYaxis().CenterTitle()
                ratiosamp.hist.GetYaxis().SetNdivisions(506, True)
                if rlabel is not None :
                    ratiosamp.hist.GetYaxis().SetTitle(rlabel)
                if rmin is not None and rmax is not None :
                    ratiosamp.hist.GetYaxis().SetRangeUser(rmin, rmax)

            left_edge  = ratiosamps[0].hist.GetXaxis().GetXmin()
            right_edge = ratiosamps[0].hist.GetXaxis().GetXmax()

            canvas.cd()

            oneline = ROOT.TLine(left_edge, 1, right_edge, 1)
            oneline.SetLineStyle(3)
            oneline.SetLineWidth(2)
            oneline.SetLineColor(ROOT.kBlack)
            oneline.Draw()
            self.add_decoration(oneline)

    def calc_yaxis_limits(self, ymin, ymax, ymax_scale ) :
        
        calcymax = 0
        calcymin = 0.5
        for samp in ( self.get_samples(isActive=True ) + self.get_samples( name='__AllStack__' ) )  :
            if samp.hist == None :
                continue
            max = samp.hist.GetMaximum()
            min = samp.hist.GetMaximum()

            if max > calcymax :
                calcymax = max
            if min < ymin :
                calcymin = min

        if ymax is None :
            ymax = calcymax 

        if ymin is None :
            ymin = calcymin 

        if ymax_scale is not None :
            ymax *= ymax_scale
        else :
            ymax *= 1.2

        return (ymin, ymax)

    def create_standard_canvas(self, name='base') :

        xsize = 650 
        ysize = 500
        self.curr_canvases[name] = ROOT.TCanvas(name, name, xsize, ysize)

        self.curr_canvases['top'] = self.curr_canvases[name]
        #self.curr_canvases[name].SetTopMargin(0.08)
        #self.curr_canvases[name].SetBottomMargin(0.13)
        #self.curr_canvases[name].SetLeftMargin(0.13)
        #self.curr_canvases[name].SetTitle('')
        self.curr_canvases[name].SetTopMargin(0.08)
        self.curr_canvases[name].SetBottomMargin(0.13)
        self.curr_canvases[name].SetLeftMargin(0.15)
        self.curr_canvases[name].SetRightMargin(0.05)
        self.curr_canvases[name].SetTitle('')

    def create_standard_ratio_canvas(self) :

        xsize = 620 
        ysize = 620
        self.curr_canvases['base'] = ROOT.TCanvas('basecan', 'basecan', xsize, ysize)

        self.curr_canvases['bottom'] = ROOT.TPad('bottompad', 'bottompad', 0.01, 0.01, 0.99, 0.34)
        self.curr_canvases['top'] = ROOT.TPad('toppad', 'toppad', 0.01, 0.35, 0.99, 0.99)
        self.curr_canvases['top'].SetTopMargin(0.08)
        self.curr_canvases['top'].SetBottomMargin(0.06)
        self.curr_canvases['top'].SetLeftMargin(0.15)
        self.curr_canvases['top'].SetRightMargin(0.05)
        #self.curr_canvases['bottom'].SetTopMargin(0.05)
        self.curr_canvases['bottom'].SetTopMargin(0.00)
        self.curr_canvases['bottom'].SetBottomMargin(0.3)
        self.curr_canvases['bottom'].SetLeftMargin(0.15)
        self.curr_canvases['bottom'].SetRightMargin(0.05)
        self.curr_canvases['base'].cd()
        self.curr_canvases['bottom'].Draw()
        self.curr_canvases['top'].Draw()

    def create_large_ratio_canvas(self) :

        xsize = 600 
        ysize = 850
        self.curr_canvases['base'] = ROOT.TCanvas('basecan', 'basecan', xsize, ysize)

        self.curr_canvases['bottom'] = ROOT.TPad('bottompad', 'bottompad', 0.01, 0.01, 0.99, 0.48)
        self.curr_canvases['top'] = ROOT.TPad('toppad', 'toppad', 0.01, 0.49, 0.99, 0.99)
        self.curr_canvases['top'].SetTopMargin(0.08)
        self.curr_canvases['top'].SetBottomMargin(0.02)
        self.curr_canvases['top'].SetLeftMargin(0.15)
        self.curr_canvases['top'].SetRightMargin(0.05)
        #self.curr_canvases['bottom'].SetTopMargin(0.05)
        self.curr_canvases['bottom'].SetTopMargin(0.03)  # non-zero to allow space for numbers on the axis that go above the plot
        self.curr_canvases['bottom'].SetBottomMargin(0.2)
        self.curr_canvases['bottom'].SetLeftMargin(0.15)
        self.curr_canvases['bottom'].SetRightMargin(0.05)
        self.curr_canvases['base'].cd()
        self.curr_canvases['bottom'].Draw()
        self.curr_canvases['top'].Draw()

    def create_top_canvas_for_ratio(self, name='can') :

        xsize = 650 
        ysize = 500
        self.curr_canvases[name] = ROOT.TCanvas(name, name, xsize, ysize)

        self.curr_canvases[name].SetTopMargin(0.08)
        self.curr_canvases[name].SetBottomMargin(0.08)
        self.curr_canvases[name].SetLeftMargin(0.15)
        self.curr_canvases[name].SetRightMargin(0.05)
        self.curr_canvases[name].SetTitle('')


    def DrawCanvas(self, topcan, ylabel=None, xlabel=None, rlabel=None, logy=False, ymin=None, ymax=None, ymax_scale=None ,rmin=None, rmax=None, datahists=[], sighists=[], doratio=False, labelStyle=None, extra_label=None, extra_label_loc=None ) :

        if doratio == True or doratio == 1 :
            self.create_standard_ratio_canvas()
        elif doratio == 2 :
            self.create_large_ratio_canvas()
        else :
            self.create_standard_canvas() 

        (ymin, ymax) = self.calc_yaxis_limits( ymin, ymax, ymax_scale )
        
        self.curr_canvases['top'].cd()

        if isinstance(topcan, ROOT.TCanvas ) :
            self.set_canvas_default_formatting( topcan, doratio, logy=logy )
            for prim in topcan.GetListOfPrimitives() :
                if isinstance(prim, ROOT.TH1F) :
                    prim.GetYaxis().SetTitle(ylabel)
            topcan.DrawClonePad()

        elif isinstance(topcan, ROOT.THStack ) :
            topcan.Draw()
            topcan.SetMinimum(ymin)
            topcan.SetMaximum(ymax)
            self.set_stack_default_formatting( topcan, doratio, logy=logy )

        # draw the data
        for dsamp in self.get_samples( name=datahists ):
            dsamp.hist.Draw('PE same')

        # draw the signals
        sigsamps = self.get_samples(name=sighists)
        for samp in sighists : 
            if samp.isActive :
                samp.hist.SetLineWidth(3)
                samp.hist.Draw('HIST same')

        if doratio :
            ratiosamps =  self.get_samples( isRatio=True )
            self.set_ratio_default_formatting( self.curr_canvases['bottom'], ratiosamps, doratio, rlabel, rmin, rmax )

            for idx, samp in enumerate(ratiosamps) :
                drawopt = 'same'
                if idx == 0 :
                    drawopt = ''
                if samp.isSignal :
                    drawopt += 'HIST'

                samp.hist.Draw(drawopt)

        self.curr_canvases['top'].cd()

        # draw the legend
        if self.curr_legend is not None :
            self.curr_legend.Draw()

        # draw the plot status label

        if labelStyle is None:
            atlaslabel = ROOT.TLatex()
            atlaslabel.SetNDC()
            atlaslabel.SetTextSize( 0.04 )
            atlaslabel.SetText(0.35, 0.85, 'CMS Internal')
            atlaslabel.Draw()
            self.curr_decorations.append(atlaslabel)
        elif labelStyle=='fancy' :
            statlabel  = ROOT.TLatex()
            rootslabel = ROOT.TLatex()

            statlabel  .SetNDC()
            rootslabel .SetNDC()

            statlabel  .SetTextSize(0.045)
            rootslabel .SetTextSize(0.045)

            statlabel.SetText( 0.15, 0.93, '#font[132]{CMS Internal}' )
            rootslabel.SetText(0.65, 0.93, '#font[132]{#sqrt{s} = 8 TeV, L = 19.4 fb^{-1} }' )

            statlabel.Draw()
            rootslabel.Draw()

            self.curr_decorations.append( statlabel )
            self.curr_decorations.append( rootslabel)

        if extra_label is not None :
            extra_label = '#font[132]{'+extra_label+'}'
            self.place_extra_label( extra_label, extra_label_loc )

        if xlabel is not None :
            if doratio :
                ratiosamp = self.get_samples(isRatio=True)[0]
                ratiosamp.hist.GetXaxis().SetTitle(xlabel)
            else :
                if isinstance(topcan, ROOT.THStack ) :
                    topcan.GetHistogram().GetXaxis().SetTitle(xlabel)

                for samp in self.get_samples() :
                    if samp.hist :
                        samp.hist.GetXaxis().SetTitle(xlabel)

        if ylabel is not None :
            if isinstance(topcan, ROOT.THStack ) :
                topcan.GetHistogram().GetYaxis().SetTitle(ylabel)
        if logy :
            self.curr_canvases['top'].SetLogy()

    def DrawSameCanvas(self, canvas, samples, normalize=False, doratio=False, colors=[], drawHist=[], ymin=None, ymax=None, ymax_scale=None, ylabel=None, xlabel=None) :

        canvas.cd()

        if not colors :
            colors = [ s.color for s in samples ]

        if not drawHist :
            drawHist = [0]*len(samples)

        calcymax = 0
        calcymin = 0.5
        for samp in samples :
            max = samp.hist.GetMaximum()
            min = samp.hist.GetMaximum()
            if normalize :
                max = max / samp.hist.Integral()
                min = min / samp.hist.Integral()
            if max > calcymax :
                calcymax = max
            if min < calcymin :
                calcymin = min

        if ymax is None :
            ymax = calcymax
        if ymin is None :
            ymin = calcymin
        if ymax_scale is not None :
            ymax *= ymax_scale
        else :
            ymax *= 1.2
        ymin *= 0.8

        first = True
        for samp, color, dh in zip(samples, colors, drawHist) :
            drawcmd = 'same'
            if first :
                drawcmd = ''
                first = False
            if samp.isSignal or dh :
                drawcmd+='hist'

            if ylabel is not None :
                samp.hist.GetYaxis().SetTitle( ylabel )
            if not doratio and xlabel is not None :
                samp.hist.GetXaxis().SetTitle( xlabel )

            samp.hist.SetLineColor( color)
            samp.hist.SetLineWidth( 2 )
            samp.hist.SetMarkerSize( 1.1 )
            samp.hist.SetMarkerStyle( 20 )
            samp.hist.SetMarkerColor(color )
            samp.hist.SetStats(0)

            if normalize :
                samp.hist.Scale(1.0/samp.hist.Integral())
                #samp.hist.DrawNormalized(drawcmd+'goff')
            #else :

            samp.hist.GetYaxis().SetRangeUser(ymin, ymax)

            samp.hist.Draw(drawcmd+'goff')

        if doratio :
            #rname = created_samples[0].name + '_ratio'
            for samp, color in zip(samples[1:], colors[1:]) :
                rcolor = color
                if len( samples ) == 2 :
                    rcolor = ROOT.kBlack

                rname = 'ratio%s' %samp.name
                self.create_ratio_sample( rname, num_sample = samples[0], den_sample=samp, color=rcolor)


    def CompareSelections( self, varexp, selections, reqsamples, histpars=None, same=False, normalize=False, doratio=False, ratiosamp=0, ylabel=None, xlabel=None, rlabel=None, rmin=None, rmax=None, ymin=None, ymax=None, ymax_scale=None, logy=False, useModel=False, treeHist=None, treeSelection=None, labelStyle=None, colors=[], legend_entries=[], extra_label=None, extra_label_loc=None, drawHist=False, legendConfig=None ) :
        assert len(selections) == len(reqsamples), 'selections and samples must have same length'

        if len(colors) != len( selections ) :
            if colors :
                print 'Size of colors input does not match size of vars input!'

            colors = [ self.get_samples(name=s)[0].color for s in reqsamples ]

        if not same :
            self.clear_all()

        self.apply_lenged_conf( legendConfig )

        if ylabel is None and isinstance( histpars, tuple )  :
            bin_width = ( histpars[2] - histpars[1] )/histpars[0]
            bin_width_f = ( histpars[2] - histpars[1] )/float(histpars[0])
            if math.fabs(bin_width_f - bin_width) != 0 :
                ylabel = 'Events / %.1f GeV' %bin_width_f
            else :
                ylabel = 'Events / %d GeV' %bin_width
            if normalize :
                ylabel = 'Normalized ' + ylabel

        if rlabel is None :
            rlabel = 'Data / MC'

        created_hists = self.MakeSameCanvas(reqsamples, varexp, selections, histpars=histpars, preserve_hists=True, useModel=useModel, treeHist=treeHist, treeSelection=treeSelection, normalize=normalize, ymin=ymin, ymax=ymax, ymax_scale=ymax_scale, doratio=doratio, colors=colors, drawHist=drawHist )
        if not created_hists :
            print 'No histograms were created'
            return

        # make the legend
        step = len(created_hists)
        self.curr_legend = self.create_standard_legend(step, doratio)

        # check for an input legend_entries
        if not legend_entries : 
            legend_entries = [self.get_samples(name=x)[0].legendName for x in created_hists]

        created_samples = self.get_samples(name=created_hists)
        print 'created_samples'
        print [x.name for x in created_samples]
        ymax = 0
        for idx, samp in enumerate(created_samples) :
            drawopt = 'PL'
            if samp.isSignal :
                drawopt = 'L'
            legname = legend_entries[idx]
            self.curr_legend.AddEntry(samp.hist, legname,  drawopt)
            self.curr_legend.SetMargin(0.2)

            samp.hist.SetLineColor( colors[idx] )
            samp.hist.SetMarkerColor( colors[idx] )

        self.DrawCanvas(self.curr_canvases['same'], ylabel=ylabel, xlabel=xlabel, rlabel=rlabel, doratio=doratio, labelStyle=labelStyle, rmin=rmin, rmax=rmax, ymax=ymax, ymin=ymin, logy=logy, extra_label=extra_label, extra_label_loc=extra_label_loc)

    def DrawDiPhotonParallel( self, varexp, selection, histpars=None )  :

        doratio=False

        self.clear_all()

        for sample in list(self.get_samples()) :
            if sample.isActive :
                negsample = self.clone_sample( oldname=sample.name, newname='Neg%s' %sample.name, temporary=True )
                negsample.isSignal=False
                negsample.isData=False
                self.create_hist( sample, varexp, selection, histpars )
                self.create_hist( negsample, '-1*'+varexp.replace('[0]', '[1]'), selection, histpars )
                sample.hist.Add( negsample.hist )

        if len(histpars) == 4 :
            self.variable_rebinning(histpars[3]) 

        self.MakeStack(varexp, )

        if doratio == True or doratio == 1 :
            self.create_standard_ratio_canvas()
        elif doratio == 2 :
            self.create_large_ratio_canvas()
        else :
            self.create_standard_canvas() 

        ymin = None
        ymax = None
        ymax_scale=None
        (ymin, ymax) = self.calc_yaxis_limits( ymin, ymax, ymax_scale )
        
        topcan = self.curr_stack[-1]

        if isinstance(topcan, ROOT.TCanvas ) :
            self.set_canvas_default_formatting( topcan, doratio, logy=logy )
            topcan.DrawClonePad()

        elif isinstance(topcan, ROOT.THStack ) :
            topcan.Draw('AH')
            topcan.SetMinimum(ymin)
            topcan.SetMaximum(ymax)
            topcan.GetYaxis().SetTickLength(0)
            topcan.GetXaxis().SetTickLength(0)

            #position = (topcan.GetHistogram().GetXaxis().GetXmax() + topcan.GetHistogram().GetXaxis().GetXmin() )/2.
            position=0

            f1= ROOT.TF1('f1','-x',0,topcan.GetHistogram().GetXaxis().GetXmax() );
            #newxaxis_pos = ROOT.TGaxis(topcan.GetHistogram().GetXaxis().GetXmin()  ,ROOT.gPad.GetUymin(),
            #                      topcan.GetHistogram().GetXaxis().GetXmax() , ROOT.gPad.GetUymin(), 0,topcan.GetHistogram().GetXaxis().GetXmax() , 510, '+' )
            newxaxis_pos = ROOT.TGaxis(0 ,ROOT.gPad.GetUymin(),
                                  topcan.GetHistogram().GetXaxis().GetXmax() , ROOT.gPad.GetUymin(), 0,topcan.GetHistogram().GetXaxis().GetXmax() , 505, '+' )

            newxaxis_neg = ROOT.TGaxis(topcan.GetHistogram().GetXaxis().GetXmin()  , ROOT.gPad.GetUymin(),
                                  0, ROOT.gPad.GetUymin(), 'f1', 505, '+' )

            newxaxis_pos.SetTitle( '#sigma i#etai#eta ' )

            self.curr_decorations.append(newxaxis_pos)
            self.curr_decorations.append(f1)
            self.curr_decorations.append(newxaxis_neg)
            newxaxis_pos.Draw()
            newxaxis_neg.Draw()
            newyaxis = ROOT.TGaxis( 0,ROOT.gPad.GetUymin(),
                                   0,topcan.GetHistogram().GetMaximum(), 0, topcan.GetHistogram().GetMaximum(), 510, '+-' )
            self.curr_decorations.append(newyaxis)
            newyaxis.Draw()

            alabel =  'Events'
            axis_label_pos = 0.45
            subl_label = ROOT.TLatex( 0.0, 0.85, 'Sublead Photon' )
            lead_label = ROOT.TLatex( 0.7, 0.85, 'Lead Photon' )
            axis_label = ROOT.TLatex( 0.5, 0.92, alabel)
            lead_label.SetNDC()
            axis_label.SetNDC()
            subl_label.SetNDC()
            lead_label.SetX(0.7)
            lead_label.SetY(0.85)
            subl_label.SetX(0.12)
            subl_label.SetY(0.85)
            axis_label.SetX(axis_label_pos)
            axis_label.SetY(0.92)
            subl_label.Draw()
            lead_label.Draw()
            axis_label.Draw()

            self.curr_decorations.append(lead_label)
            self.curr_decorations.append(subl_label)
            self.curr_decorations.append(axis_label)

            self.set_stack_default_formatting( topcan, doratio )


        # draw the data
        for dsamp in self.get_samples(isData=True):
            dsamp.hist.Draw('PE same')

        # draw the signals
        sigsamps = self.get_samples(isSignal=True)
        for samp in sigsamps : 
            if samp.isActive :
                samp.hist.SetLineWidth(2)
                samp.hist.Draw('HIST same')

        if doratio :
            ratiosamps =  self.get_samples( isRatio=True )
            self.set_ratio_default_formatting( self.curr_canvases['bottom'], ratiosamps, doratio, rlabel, rmin, rmax )

            for idx, samp in enumerate(ratiosamps) :
                drawopt = 'same'
                if idx == 0 :
                    drawopt = ''
                if ratiosamp.isSignal :
                    drawopt += 'HIST'

                ratiosamp.hist.Draw(drawopt)

        # draw the legend
        if self.curr_legend is not None :
            self.curr_legend.Draw()

        # draw the plot status label
        if labelStyle is None :
            atlaslabel = ROOT.TLatex()
            atlaslabel.SetNDC()
            atlaslabel.SetTextSize( 0.04 )
            atlaslabel.SetText(0.35, 0.85, 'CMS Internal')
            atlaslabel.Draw()

        xlabel=None
        if xlabel is not None :
            if doratio :
                ratiosamp = self.get_samples(isRatio=True)[0]
                ratiosamp.hist.GetXaxis().SetTitle(xlabel)
            else :
                if isinstance(topcan, ROOT.THStack ) :
                    topcan.GetHistogram().GetXaxis().SetTitle(xlabel)

                for samp in self.get_samples() :
                    if samp.hist :
                        samp.hist.GetXaxis().SetTitle(xlabel)


        ylabel=None

        if ylabel is not None :
            if isinstance(topcan, ROOT.THStack ) :
                topcan.GetHistogram().GetYaxis().SetTitle(ylabel)

        logy=False
        if logy :
            self.curr_canvases['top'].SetLogy()

    def CompareDiPhotonParallel( self, varexp, selections,samples, histpars=None )  :

        doratio=False

        if len(selections) != len(samples) :
            print 'Size of selections list must be the same as the size of the samples list'

        self.clear_all()

        for selection, sname in zip(selections, samples) :
            slist = self.get_samples( name=sname )
            if not slist :
                print 'Could not retrieve sample, %s' %sname
            if len(slist) > 1 :
                print 'Located multiple samples with name %s' %sname

            sample = slist[0]

            negsample = self.clone_sample( oldname=sname, newname='Neg%s' %sample, temporary=True )
            self.create_hist( sample, varexp, selection, histpars )
            print varexp
            print varexp.replace('[0]', '[1]')
            self.create_hist( negsample, '-1*'+varexp.replace('[0]', '[1]'), selection, histpars )

            sample.hist.Add( negsample.hist )
            created_samples.append(sample)

        #if len(histpars) == 4 :
        #    self.variable_rebinning(histpars[3]) 

        if doratio :
            self.create_top_canvas_for_ratio('same')
        else :
            self.create_standard_canvas('same')

        self.curr_canvases['same'].cd()

        calcymax = 0
        calcymin = 0.5
        for samp in created_samples :
            max = samp.hist.GetMaximum()
            min = samp.hist.GetMaximum()
            if normalize :
                max = max / samp.hist.Integral()
                min = min / samp.hist.Integral()
            if max > calcymax :
                calcymax = max
            if min < calcymin :
                calcymin = min

        #if ymax is None :
        #    ymax = calcymax
        #if ymin is None :
        #    ymin = calcymin
        #if ymax_scale is not None :
        #    ymax *= ymax_scale
        #else :
        #    ymax *= 1.2
        #ymin *= 0.8

        first = True

        colors = [s.color for s in created_samples ]
        drawHist = [0]*len(created_samples)

        for samp, color, dh in zip(created_samples, colors, drawHist) :
            drawcmd = 'same'
            if first :
                drawcmd = ''
                first = False
            if samp.isSignal or dh :
                drawcmd+='hist'

            if ylabel is not None :
                samp.hist.GetYaxis().SetTitle( ylabel )
            if not doratio and xlabel is not None :
                samp.hist.GetXaxis().SetTitle( xlabel )

            samp.hist.SetLineColor( color)
            samp.hist.SetLineWidth( 2 )
            samp.hist.SetMarkerSize( 1.1 )
            samp.hist.SetMarkerStyle( 20 )
            samp.hist.SetMarkerColor(color )
            #samp.hist.GetXaxis().SetLabelSize(0.05)
            #samp.hist.GetXaxis().SetTitleSize(0.05)
            #samp.hist.GetYaxis().SetLabelSize(0.05)
            #samp.hist.GetYaxis().SetTitleSize(0.05)
            #samp.hist.GetYaxis().SetTitleOffset(2.0)
            samp.hist.SetStats(0)

            if normalize :
                samp.hist.Scale(1.0/samp.hist.Integral())
                #samp.hist.DrawNormalized(drawcmd+'goff')
            #else :

            samp.hist.GetYaxis().SetRangeUser(ymin, ymax)

            samp.hist.Draw(drawcmd+'goff')

        if doratio :
            #rname = created_samples[0].name + '_ratio'
            for samp, color in zip(created_samples[1:], colors[1:]) :
                rcolor = color
                if len( created_samples ) == 2 :
                    rcolor = ROOT.kBlack

                rname = 'ratio%s' %samp.name
                self.create_ratio_sample( rname, num_sample = created_samples[0], den_sample=samp, color=rcolor)

        self.curr_canvases['same'].Draw()

        self.MakeStack(varexp, )

        #if ylabel is None :
        #    bin_width = ( histpars[2] - histpars[1] )/histpars[0]
        #    bin_width_f = ( histpars[2] - histpars[1] )/float(histpars[0])
        #    if math.fabs(bin_width_f - bin_width) != 0 :
        #        ylabel = 'Events / %.1f GeV' %bin_width_f
        #    else :
        #        ylabel = 'Events / %d GeV' %bin_width
        #if rlabel is None :
        #    rlabel = 'Data / MC'
            
        self.DrawCanvas(self.curr_stack[-1], sighists=self.get_signal_samples(), datahists=['Data'])


    def Draw2D( self, varexp, selections, sample_names, histpars=None, drawopts='', xlabel=None, ylabel=None) :

        self.clear_hists()

        if not isinstance(sample_names, list) :
            sample_names = [sample_names]
        if not isinstance(selections, list) :
            selections = [selections]

        if len(sample_names) != len(selections) :
            print 'Length of samples does not match length of selections'

        created_samples=[]
        for idx, (samp_name, selection) in enumerate(zip(sample_names, selections)) :

            samp = self.get_samples(name=samp_name)[0]
            newname = '%s_%d' %(samp.name, idx)
            newsamp = self.clone_sample( oldname=samp.name, newname=newname, temporary=True )
            newsamp.hist = None

            self.create_hist( newsamp, varexp, selection, histpars)

            if xlabel is not None :
                samp.hist.GetXaxis().SetTitle( xlabel )
            if ylabel is not None :
                samp.hist.GetYaxis().SetTitle( ylabel )
            
            created_samples.append(newsamp)

        for idx, samp in enumerate(created_samples) :

            self.curr_canvases['base%d'%idx] = ROOT.TCanvas('basecan%d'%idx, '')
            self.curr_canvases['base%d'%idx].SetRightMargin(0.12)
            self.curr_canvases['base%d'%idx].cd()

            samp.hist.Draw(drawopts)

    def CompareVars( self, varexps, selections, sample_names, histpars=None, same=False, normalize=False, doratio=False, ylabel=None, xlabel=None, colors=[], labels=[] ) :

        self.clear_all()

        if not isinstance( varexps, list ) : varexps = [varexps]
        if not isinstance( selections, list ) : selections= [selections]
        if not isinstance( sample_names, list ) : sample_names= [sample_names]

        if len(selections) < len(varexps) and len(selections)==1 :
            selections = [selections[0]]*len(varexps)


        if len(colors) != len( varexps ) :
            if colors :
                print 'Size of colors input does not match size of vars input!'

            colors = [ROOT.kBlack]*len(varexps)

        if len(labels) != len(varexps) :
            if labels :
                print 'Size of labels does not match size of vars input!'
            labels = varexps

        samples = []
        for sn in sample_names :
            samples.append( self.get_samples( name=sn )[0] )

        if len(samples) < len(varexps) and len(samples)==1 :
            samples = [samples[0]]*len(varexps)

        created_hists = []
        for var, selection, sample in zip(varexps, selections, samples) :

            newname = '%s_%s' %(sample.name, var)
            newsamp = self.clone_sample( oldname=sample.name, newname = newname, temporary=True )
            created_hists.append(newsamp.name)
            self.create_hist( newsamp, var, selection, histpars)
            self.curr_hists[newsamp.name] = newsamp.hist.Clone(var)

        if doratio :
            self.create_ratio_sample( 'ratio', num_sample=created_hists[0], den_sample=created_hists[1] )


        self.curr_canvases['same'] = ROOT.TCanvas('same', '')
        for idx, name in enumerate( created_hists ) :
            self.curr_hists[name].SetMarkerColor( colors[idx] )
            self.curr_hists[name].SetLineColor( colors[idx] )

            if idx == 0 :
                if normalize :
                    self.curr_hists[name].DrawNormalized('hist')
                else :
                    self.curr_hists[name].Draw('hist')
            else :
                if normalize :
                    self.curr_hists[name].DrawNormalized('samehist')
                else :
                    self.curr_hists[name].Draw('samehist')

        self.DrawCanvas(self.curr_canvases['same'])

        # make the legend
        # In placing the legend move the bottom down 0.05 for each entry
        #step = len(varexps)
        #self.curr_legend = self.create_standard_legend(step, doratio)

        #for var, lab in zip( varexps, labels ) :
        #    histname = '%s_%s' %(sample.name, var)
        #    self.curr_legend.AddEntry(self.curr_hists[histname], lab, 'L' )
        #    
        self.DrawCanvas(self.curr_canvases['same'], ylabel=ylabel, xlabel=xlabel, doratio=doratio)

    #---------------------------------------
    def CompareRatios( self, varexp, selections, samples, histpars=None, normalize=False, doratio=False, colors = [], legend_entries=[], xlabel=None, ylabel=None, rlabel=None, rmin=None, rmax=None, ymin=None, ymax=None, logy=False ) :

        self.clear_all()

        assert  len(samples) == len(selections), 'sample and selection must have the same length'

        if len( selections )%2 != 0 :
            print 'Expect an even number of selecitions, even entries should be numerators, odd entries are denominators '

        if len(colors) != (len( samples )/2) :
            if colors :
                print 'Size of colors input does not match size of vars input!'
    
            colors = [ self.get_samples(name=s)[0].color for s in samples ]


        num_samps = []
        den_samps = []
        for idx, (selection, samplename) in enumerate(zip(selections, samples)) :

            sample = self.get_samples(name=samplename)[0]

            if idx%2 == 0 :
                newname = '%snum%d' %(sample.name, idx)
            else :
                newname = '%sden%d' %(sample.name, idx)

            newsamp = self.clone_sample( oldname=sample.name, newname=newname, temporary=True )
            self.create_hist( newsamp, varexp, selection, histpars)

            if normalize :
                newsamp.hist.Scale( 1.0/newsamp.hist.Integral() )
            
            if idx%2 == 0 :
                num_samps.append( newsamp )
            else :
                den_samps.append( newsamp )

        ratio_samps = []
        for num, den in zip( num_samps, den_samps ) :
            rsamp = self.create_ratio_sample( num.name+'ratio', num_sample=num, den_sample=den )
            rsamp.isRatio=False #trick it into not counting these as ratios
            ratio_samps.append(rsamp)
            
        if doratio :
            self.create_top_canvas_for_ratio('same')
        else :
            self.create_standard_canvas('same')

        self.DrawSameCanvas(self.curr_canvases['same'], ratio_samps, doratio=doratio, colors=colors, xlabel=xlabel, ylabel=ylabel)

        
        if not legend_entries :
            legend_entries = [s.name for s in ratio_samps]

        self.curr_legend = self.create_standard_legend( len(ratio_samps) )
        for idx, samp in enumerate(ratio_samps) :
            drawopt = 'PL'
            if samp.isSignal :
                drawopt = 'L'
            legname = legend_entries[idx]
            self.curr_legend.AddEntry(samp.hist, legname,  drawopt)
            self.curr_legend.SetMargin(0.2)

            samp.hist.SetLineColor( colors[idx] )
            samp.hist.SetMarkerColor( colors[idx] )

        self.DrawCanvas(self.curr_canvases['same'], ylabel=ylabel, xlabel=xlabel, rlabel=rlabel, doratio=doratio, rmin=rmin, rmax=rmax, ymax=ymax, ymin=ymin, logy=logy)
    

    #---------------------------------------
    def DoTAndP( self, varexp, num_selection, den_selection, sample, histpars=None, binning=[], xlabel=None, ylabel=None, ymin=None, ymax=None, label=None, normalize=False, colors=[], legend_entries=[] ) :
    
        self.clear_all()

        if not isinstance(sample, list) :
            sample = [sample]
        if not isinstance(num_selection, list) :
            num_selection= [num_selection]
        if not isinstance(den_selection, list) :
            den_selection= [den_selection]
    
        assert  len(sample) == len(num_selection), 'sample and numerator selection must have the same length'
        assert  len(sample) == len(den_selection), 'sample and denominator selection must have the same length'
    
        if len(colors) != len( sample ) :
            if colors :
                print 'Size of colors input does not match size of vars input!'
    
            colors = [ self.get_samples(name=s)[0].color for s in sample ]
    
        num_hists = {}
        den_hists = {}
    
    
        # create a new sample manager to hold histograms
        #sman = SampleManager('', '' )
        for idx, (num, den, insamp) in enumerate( zip(num_selection, den_selection, sample) ) :
            use_stored_first = False
            if idx > 0 :
                use_stored_first = True
    
            samp = insamp + str(idx)

            num_name = '%s_num' %samp
            den_name = '%s_den' %samp

            self.clone_sample(oldname=insamp, newname=num_name, temporary=True )
            self.clone_sample(oldname=insamp, newname=den_name, temporary=True )
    
            created_num_samp = []
            created_den_samp = []
            created_num_samp += self.MakeSameCanvas([num_name], varexp, num, histpars, doratio=False, useStoredBinning=use_stored_first, preserve_hists=True )
            num_samp = self.get_samples(name=created_num_samp[0])[0]
            #sman.samples.append(num_samp)

            created_den_samp += self.MakeSameCanvas([den_name], varexp, den, histpars, doratio=False, useStoredBinning=True, preserve_hists=True)
            den_samp = self.get_samples(name=created_den_samp[0])[0]
            #sman.samples.append( den_samp )
            #self.clear_hists()

            if normalize :
                num_samp.hist.Scale( 1.0/num_samp.hist.Integral() )
                den_samp.hist.Scale( 1.0/den_samp.hist.Integral() )

            rsamp = self.create_ratio_sample( '%s_ratio' %samp, num_sample=num_samp, den_sample=den_samp )
            if xlabel is not None :
                rsamp.hist.GetXaxis().SetTitle( xlabel )
                #rsamp.hist.GetXaxis().SetTitleSize( 0.05 )
                #rsamp.hist.GetXaxis().SetTitleOffset( 1.1 )
            if ylabel is not None :
                rsamp.hist.GetYaxis().SetTitle( ylabel )
                #rsamp.hist.GetYaxis().SetTitleSize( 0.05 )
                #rsamp.hist.GetYaxis().SetTitleOffset( 1.25 )
    
        plot_ymax = 0.0
        plot_ymin = 100.0
    
        for ratio in self.get_samples(isRatio=True) :
            ratio.hist.SetTitle('')
            max = ratio.hist.GetMaximum()
            min = ratio.hist.GetMinimum()
            if max > plot_ymax :
                plot_ymax = max
            if min < plot_ymin :
                plot_ymin = min
        if ymin is not None :
            plot_ymin = ymin
        else :
            plot_ymin *= 0.9
        if ymax is not None :
            plot_ymax = ymax
        else :
            plot_ymax *= 1.1
    
    
        for ratio in self.get_samples(isRatio=True) :
            ratio.hist.GetYaxis().SetRangeUser( plot_ymin, plot_ymax )
    
        self.create_standard_canvas( )
        self.curr_canvases['base'].SetBottomMargin(0.13)
        self.curr_canvases['base'].SetLeftMargin(0.13)
        self.curr_canvases['base'].SetTitle('')
    
        for idx, ( ratio, color ) in enumerate( zip(self.get_samples(isRatio=True), colors ) ) :
            drawcmd = ''
            if idx > 0 :
                drawcmd = 'same'
            if varexp.count(':') :
                drawcmd += 'colz'
            ratio.hist.SetLineColor( color )
            ratio.hist.SetMarkerColor( color )
            ratio.hist.SetMarkerStyle( 20 )
            ratio.hist.SetMarkerSize( 1.2 )
            ratio.hist.Draw(drawcmd)
            self.add_decoration( ratio.hist )
    
        leg_xmin = 0.6
        leg_xmax = 0.8
        leg_ymin = 0.68
        leg_ymax = 0.88
    
        if varexp.count('eta') :
            leg_xmin -= 0.2
            leg_xmax -= 0.2
            leg_ymin -= 0.1
            leg_ymax -= 0.1
    
        leg = ROOT.TLegend( leg_xmin, leg_ymin, leg_xmax,  leg_ymax)
        leg.SetBorderSize(0)
        leg.SetFillColor(ROOT.kWhite)
    
        # check for an input legend_entries
        if not legend_entries : 
            legend_entries = sample
    
        for idx, (inname, legentry) in enumerate( zip(sample, legend_entries) ) :
            name = inname+str(idx)
            ratio = self.get_samples(name='%s_ratio' %name )[0]
            leg.AddEntry( ratio.hist, legentry, 'LPE' )
    
        self.curr_canvases['base'].cd()
        leg.Draw()
        self.curr_legend = leg
    
        if label is not None :
            lab = ROOT.TLatex()
            lab.SetNDC()
    
            lab.SetText( 0.2, 0.83, label )
            lab.SetTextFont(42)
    
            lab.Draw()
    
            if varexp.count('eta') :
                xsize = lab.GetXsize()
                newxmin = 0.5-( xsize/2 )
                lab.SetX(newxmin)
            self.curr_decorations .append(lab)

    def MakeRocCurve( self, varexps, selections, signal, background , histpars=None, colors=[], markers=[], legend_entries=[], debug=False, less_than=False, doSoverB=False, extra_label=None, extra_label_loc=None, ymin=None, ymax=None, legendConfig=None ) :

        if not isinstance( selections, list ) :
            selections = [selections]
        if not isinstance( varexps, list ) :
            varexps = [varexps]
        if not isinstance( signal, list ) :
            signal = [signal]
        if not isinstance( background, list ) :
            background = [background]
        if not isinstance( histpars, list ) :
            histpars = [histpars]
        if not isinstance( less_than, list ) :
            less_than = [less_than]

        self.clear_all()

        self.apply_lenged_conf( legendConfig )

        sig_samps = []
        bkg_samps = []
        for sig in signal :
            sig_samps.append(self.get_samples(name=sig)[0])
        for bkg in background :
            bkg_samps.append(self.get_samples(name=bkg)[0])

        if not colors :
            colors = [ s.color for s in sig_samps ]

        if not markers :
            markers = [3]*len(signal)

        if len(histpars) != len(signal) :
            histpars = histpars*len(signal)

        assert len(sig_samps) == len(bkg_samps), 'Did not retrieve all signal or background samples'

        created_hists = []

        self.create_standard_canvas()
        self.curr_canvases['base'].cd()

        for idx, (varexp, selection, histpar, sig_samp, bkg_samp, color, marker, lt) in enumerate( zip( varexps, selections, histpars, sig_samps, bkg_samps, colors, markers, less_than) ) :

            newsigsamp = copy.copy(sig_samp)
            newsigsamp.hist = None
            newsigsamp.name = '%s%d' %(sig_samp.name, idx)
            newbkgsamp = copy.copy(bkg_samp)
            newbkgsamp.hist = None
            newbkgsamp.name = '%s%d' %(bkg_samp.name, idx)

            self.create_hist( newsigsamp, varexp, selection, histpar)
            self.create_hist( newbkgsamp, varexp, selection, histpar)

            sig_eff = []
            bkg_eff = []
            nsig = []
            nbkg = []
            sig_tot = newsigsamp.hist.Integral()
            bkg_tot = newbkgsamp.hist.Integral()
            for bin in range( 1, histpar[0]+1 ) :
                min = bin
                max = histpar[0]
                if lt :
                    min = 0 
                    max = bin
                sig_eff.append( newsigsamp.hist.Integral( min, max )/sig_tot )
                bkg_eff.append( newbkgsamp.hist.Integral( min, max )/bkg_tot )
                nsig.append( newsigsamp.hist.Integral( min, max ))
                nbkg.append( newbkgsamp.hist.Integral( min, max ))

            name='roc%d' %idx

            nbins = histpar[0]
            # if there are only two bins, this is a boolean and the TGraph should only have one point
            if nbins == 2 :
                nbins = 1

            print nbins
            self.curr_hists[name] =  ROOT.TGraph(nbins)
            self.curr_hists[name].SetName(name)

            if ymin is not None :
                self.curr_hists[name].SetMinimum( ymin )
            if ymax is not None :
                self.curr_hists[name].SetMaximum( ymax )

            if doSoverB :
                for bin, (sigeff, sig, bkg) in enumerate(zip( sig_eff, nsig, nbkg) ):
                    if sig == 0 and bkg == 0 :
                        continue
                    if histpar[0] <= 2 and sigeff==1 :
                        continue;
                    if debug : print 'Place point at %f, bin %d, nSig=%f, nBkg=%f, %f, %f ' %( newsigsamp.hist.GetBinLowEdge( bin+1 ), bin+1, sig, bkg, sigeff, sig/math.sqrt(sig+bkg))
                    self.curr_hists[name].SetPoint( bin, sigeff, sig/math.sqrt(sig+bkg) );

            else :
                bin=0
                for (sig, bkg) in zip( sig_eff, bkg_eff ):
                    if histpar[0] <= 2 and sig==1 :
                        continue;
                    bin+=1
                    if debug : print 'Place point at %f, bin %d : %f, %f ' %( newsigsamp.hist.GetBinLowEdge( bin ), bin, sig, 1.0-bkg)
                    self.curr_hists[name].SetPoint( bin, sig, 1.0-bkg );

            #store numerical results

            for bin, (sigeff, bkgeff, sig, bkg) in enumerate(zip( sig_eff, bkg_eff, nsig, nbkg) ):
                den = sig+bkg
                if den != 0 :
                    self.transient_data.setdefault( 'Sig: %s, Bkg: %s' %(sig_samp.name, bkg_samp.name), [] ).append( { 'CutVal' : newsigsamp.hist.GetBinLowEdge( bin+1 ), 'nSig' : sig, 'nBkg' : bkg, 'bkgEff' : bkgeff, 'sigEff': sigeff, 'SoverRootSplusB' : sig/math.sqrt(den) } )


            self.curr_hists[name].SetLineColor(color)
            self.curr_hists[name].SetMarkerColor(color)
            self.curr_hists[name].SetMarkerStyle(marker)
            self.curr_hists[name].SetMarkerSize(1.2)

            drawcmd = ''
            if idx == 0 :
                #drawcmd = 'ACP'
                drawcmd = 'AP'
                if histpar[0]>2 : drawcmd = 'C'+drawcmd
            else :
                #drawcmd = 'CPsame'
                drawcmd = 'Psame'
                if histpar[0]>2 : drawcmd = 'C'+drawcmd

            self.curr_hists[name].Draw(drawcmd)
            self.curr_hists[name].GetXaxis().SetTitle('Signal Efficiency')
            if doSoverB :
                self.curr_hists[name].GetYaxis().SetTitle('S / #sqrt{ S + B }')
            else :
                self.curr_hists[name].GetYaxis().SetTitle('Background Rejection')

            self.curr_hists[name].GetYaxis().SetTitleSize(0.05)
            self.curr_hists[name].GetXaxis().SetTitleSize(0.05)
            self.curr_hists[name].GetYaxis().SetLabelSize(0.05)
            self.curr_hists[name].GetXaxis().SetLabelSize(0.05)
            self.curr_hists[name].SetTitle()
            created_hists.append(self.curr_hists[name])

        if legend_entries :

            if len(legend_entries) != len(self.curr_hists) :
                print 'Length of lengend entries does not match length of created histograms'
            else :

                self.curr_legend = self.create_standard_legend( len(sig_samps) )
                for hist, entry in zip( created_hists, legend_entries) :
                    self.curr_legend.AddEntry(hist, entry, 'PE')

                self.curr_legend.Draw()

        if extra_label is not None :
            self.place_extra_label( extra_label, extra_label_loc )

    def MakeFidAcceptTable(self, var, cut_selection, labels, samples, histpars, useModel=False, useTreeModel=False) :

        if not isinstance(cut_selection, list) :
            cut_selection = [cut_selection]
        if not isinstance(labels, list) :
            labels = [labels]

        if len(cut_selection) != len(labels) :
            print 'Number of labels much match number of cuts'
            return

        mod_cut_selection = list(cut_selection)
        mod_labels = list(labels)
        mod_cut_selection.insert( 0, '' )
        mod_labels.insert(0, 'Total')
        
        data = {}
        created_hists = {}
        for selection, label in zip(mod_cut_selection, mod_labels) :
            data[label] = {}

            self.clear_all()
            for sampname in samples :
                samp = self.get_samples(name=sampname)[0]

                histname = 'hist_%s' %(samp.name)

                full_selection = selection
                print 'Drawing sample : %s' %samp.name

                self.create_hist( samp, var, selection, histpars )

                # get the histogram
                created_hists[sampname] = samp.hist.Clone()

            
            mcsum = 0.0
            mcerrsq = 0.0
            for name in samples :
                hist = created_hists[name]

                val = hist.GetBinContent(1)
                err = hist.GetBinError(1)
                data[label][name] = (val, err)

        print data

        table_entries = []
        # top row
        top_row = ['Cuts']
        for name in samples :
            top_row.append(name)
            top_row.append('Acceptance')

        table_entries.append(top_row)

        for label in labels :
            data_row = [label]
            for sampname in samples :
                data_val = data[label][sampname][0]
                data_err = data[label][sampname][1]
                total_val = data['Total'][sampname][0]
                total_err = data['Total'][sampname][1]

                ratio_val = data_val / float(total_val)
                ratio_err = ratio_val * math.sqrt( ( data_err/ data_val )*( data_err/ data_val ) + ( total_err / total_val )*( total_err / total_val ) )
                data_row.append( (data_val, data_err) )
                data_row.append( (ratio_val, ratio_err) )
            table_entries.append(data_row)

        print table_entries

        table_text = self.MakeLatexFidAcceptTable(table_entries)
    
        #self.MakeLatexDocument(tables=[table_text])
            
        

    def MakeCutflowTable(self, var, cut_selection, labels, histpars, useModel=False, useTreeModel=False) :

        if not isinstance(cut_selection, list) :
            cut_selection = [cut_selection]
        if not isinstance(labels, list) :
            labels = [labels]

        if len(cut_selection) != len(labels) :
            print 'Number of labels much match number of cuts'
            return

        table_entries = {}
        
        for selection, label in zip(cut_selection, labels) :
            table_entries[label] = {}

            self.clear_all()
            for samp in self.samples :

                histname = 'hist_%s' %(samp.name)

                full_selection = selection
                print 'Drawing sample : %s' %samp.name

                self.create_hist( samp, var, selection, histpars )

                ## get the histogram
                #if samp.isSignal :
                #    self.curr_signals[samp.name] = samp.hist.Clone()
                #else :
                #    self.curr_hists[samp.name] = samp.hist.Clone()

            
            mcsum = 0.0
            mcerrsq = 0.0
            for samp in self.get_samples() :
                if samp.isActive :
                    val = samp.hist.GetBinContent(1)
                    err = samp.hist.GetBinError(1)
                    table_entries[label][samp.name] = (val, err)
                    if samp.name is not 'Data' :
                        mcsum += val
                        mcerrsq += err*err
            table_entries[label]['MC'] = (mcsum, math.sqrt(mcerrsq))

            #if 'Data' in  :
            #    dataval = table_entries[label]['Data'][0]
            #    dataerr = table_entries[label]['Data'][1]
            #    ratioval = dataval/mcsum
            #    ratioerr = dataval/mcsum * math.sqrt( ( dataerr/dataval )*( dataerr/dataval ) + ( mcerrsq/(mcsum*mcsum) ) )
            #    table_entries[label]['Data/MC'] = (ratioval, ratioerr)

        for name in labels :
            print table_entries[name]
        

        #second_table = {}
        #for cut, table in table_entries.iteritems() :
        #    second_table.setdefault(cut, {})

        #    if 'Data' in self.curr_hists :
        #        for samp in ['Data','MC', 'Data/MC'] :
        #            second_table[cut][samp] = table_entries[cut].pop(samp)

        signal_samples = [ s.name for s in self.get_signal_samples() if s.isActive ]

        table_text_1 = self.LatexCutflowTable(table_entries, labels , self.stack_order+signal_samples)
        #table_text_2 = self.LatexCutflowTable(second_table, labels , ['MC', 'Data', 'Data/MC'])

        #self.MakeLatexDocument(tables=[table_text_1, table_text_2])
        self.MakeLatexDocument(tables=[table_text_1])

    def MakeLatexFidAcceptTable(self, table_entries, options={}) :

        table = []
        for row in table_entries :
            table_row = []
            for col_val in row :
                print col_val
                if isinstance(col_val, str) :
                    table_row.append(col_val)
                elif isinstance(col_val, tuple) :
                    err_scale = int( math.log10(col_val[1]) )
                    print 'err_Scale'
                    print err_scale
                    if err_scale < -3 :
                        table_row.append('{val:.{valwid}e} $\pm$ {err:.{errwid}e} '.format (val=col_val[0], valwid=abs(err_scale)-1, err=col_val[1], errwid=abs(err_scale)-3 ) )
                    elif err_scale > 0 :
                        table_row.append('{val:0{valwid}d} $\pm$ {err:0{errwid}d} '.format (val=int(col_val[0]), valwid=abs(err_scale)+1, err=int(col_val[1]), errwid=abs(err_scale)+1 ) )
                    else :
                        table_row.append('{val:.{valwid}f} $\pm$ {err:.{errwid}f} '.format (val=col_val[0], valwid=abs(err_scale)+1, err=col_val[1], errwid=abs(err_scale)+1 ) )

                    #if col_val[0] > 1000 :
                    #    table_row.append(r'%.2e $\pm$ %.2f '  %( col_val[0], col_val[1]) )
                    #elif col_val[0] < 1 :
                    #    table_row.append(r'%.1g $\pm$ %.1g '  %( col_val[0], col_val[1]) )
                    #else :
                    #    table_row.append(r'%.2f $\pm$ %.2f '  %( col_val[0], col_val[1]) )

            
            table.append(table_row )

        print table
        max_widths = [0]*len(table[0])
        for row in table :
            for idx, col in enumerate( row ) :
                width = len(col)
                if width > max_widths[idx] :
                    max_widths[idx] = width

        table_text = ''
        for row in table :
            row_text = ''
            for idx, col in enumerate(row) :
                row_text += col.ljust(max_widths[idx]) + ' & '
            row_text = row_text.rstrip('& ')
            row_text += ' \\\\ \n'

            table_text += row_text

        print table_text
                


    def LatexCutflowTable(self, entries, roworder, colorder, options={}) :

        table = []
        header = []
        header.append('Cut Flow')
        header+= colorder
        table.append(header)

        for rowname in roworder :
            entry = entries[rowname]
            cutline = []
            cutline.append(rowname)
            print 'Row %s has entry' %rowname
            print entry
            for sampname in colorder :
                data =  entry[sampname]
                if data[0] > 1000 :
                    cutline.append(r'%.2e $\pm$ %.2f'  %( data[0], data[1]) )
                elif data[0] < 1 :
                    cutline.append(r'%.3f $\pm$ %.3f'  %( data[0], data[1]) )
                else :
                    cutline.append(r'%.2f $\pm$ %.2f'  %( data[0], data[1]) )
            table.append(cutline)

        print 'TABLE'
        print table

        # loop over the inputs and collect length information
        column_width = []
        numcol = len(table[0]) # the length of any row (first here) is the column width
        for colnum in range(0, numcol) :
            widths = []
            for row in table :
                colentry = row[colnum]
                widths.append(len(colentry))
            column_width.append(max(widths))
            #column_width[table[0][colnum]] = max(widths)

        table_text = []
        table_text.append(r'\begin{table}')
        table_text.append(r'\scriptsize')

        ncutcol = len(colorder)
        table_text.append(r'\begin{tabular}{ | l | %s |}\hline' %( '|'.join([ ' c ' ]*ncutcol)))
        for row in table :
            text_entries = []
            print row
            for coln, ent in enumerate(row) :
                print column_width[coln]
            row_entry = ' %s ' %( ' & '.join([ ent.ljust(column_width[coln])  for coln, ent in enumerate(row) ] ))
            row_entry.rstrip('&&')
            row_entry += r' \\'
            table_text.append(row_entry)

        table_text[-1] += r' \hline'
        table_text.append('\end{tabular}\end{table}')

        print '\n'.join(table_text)
        return table_text

    def MakeLatexDocument(self, tables=[]) :
    
        doc_text = []
        doc_text.append(r'\documentclass[12pt]{article}')
        doc_text.append(r'\usepackage[top=3cm,bottom=2cm,left=1cm,right=1cm] {geometry}')
        doc_text.append(r'\begin{document}')
        doc_text.append(r'\begin{center}')
        for table_text in tables :
            doc_text += table_text
        doc_text.append(r'\end{center}')
        doc_text.append(r'\end{document}')

        print 'DOC'
        print '\n'.join(doc_text)
        tmpname = '/tmp/latex_table'
        tmpfile = open(tmpname+'.tex', 'w')
        tmpfile.write('\n'.join(doc_text))
        tmpfile.close()

        os.system(r'cd /tmp ; latex %s' %tmpname+'.tex')
        os.system(r'dvips %s -o %s' %(tmpname+'.dvi', tmpname+'.ps' ) )
        os.system(r'gv %s' %tmpname+'.ps')

    # ------------------------------------------------------------
    #   Do variable rebinning for a stack plot
    # ------------------------------------------------------------
    def make_variable_binning(self, stacklist,threshold=3):

        if not isinstance(stacklist, list) :
            stacklist = [stacklist]
    
        # sum stack list
        sum = stacklist[0].Clone('sum')
        sum.Reset()
        for h in stacklist:
            sum.Add(h)
    
        # make binning
        bins=[]
        axis=sum.GetXaxis()
        bins.append(axis.GetXmin())
        count=0
        for b in range(1, sum.GetNbinsX()+1):
            # this special case is to not extend the first 
            # filled bin to the edge of the histogram
            if sum.GetBinContent(b)>0 and count==0 and len(bins)==1:
                bins.append(axis.GetBinLowEdge(b))
            count+=sum.GetBinContent(b)
            if count>threshold:
                bins.append(axis.GetBinUpEdge(b))
                count=0
        if count!=0:
            bins.append(axis.GetXmax())
        print bins,count
        return bins
    
    # ------------------------------------------------------------
    #   Do variable rebinning for a stack plot
    # ------------------------------------------------------------
    def do_variable_rebinning(self, samp,bins):
        newhist=ROOT.TH1F(samp.hist.GetName()+"_rebin",
        samp.hist.GetTitle()+";"+samp.hist.GetXaxis().GetTitle()+";"+samp.hist.GetYaxis().GetTitle(),len(bins)-1,array('d',bins))
        a=samp.hist.GetXaxis()
        newa=newhist.GetXaxis()
        for b in range(1, samp.hist.GetNbinsX()+1):
            newb=newa.FindBin(a.GetBinCenter(b))
            val=newhist.GetBinContent(newb)
            err=newhist.GetBinError(newb)
            ratio_bin_widths=newa.GetBinWidth(newb)/a.GetBinWidth(b)
            val=val+samp.hist.GetBinContent(b)/ratio_bin_widths
            err=math.sqrt(err*err+samp.hist.GetBinError(b)/ratio_bin_widths*samp.hist.GetBinError(b)/ratio_bin_widths)
            newhist.SetBinContent(newb,val)
            newhist.SetBinError(newb,err)
    
        return newhist

    # ----------------------------------------------------------------------------
    def create_standard_legend(self, nentries, doratio=False) :

        if self.legendLoc == 'TopLeft' :
            legend_limits = { 'x1' : 0.2+self.legendTranslateX, 'y1' : 0.90-self.legendCompress*0.052*nentries+self.legendTranslateY, 'x2' : 0.5*self.legendWiden+self.legendTranslateX, 'y2' : 0.90+self.legendTranslateY }
        elif self.legendLoc == 'Double' :
            legend_limits = { 'x1' : 0.15+self.legendTranslateX, 'y1' : 0.90-self.legendCompress*0.052*nentries+self.legendTranslateY, 'x2' : 0.65*self.legendWiden+self.legendTranslateX, 'y2' : 0.85+self.legendTranslateY }
        else :
            legend_limits = { 'x1' : 0.9-0.25*self.legendWiden+self.legendTranslateX, 'y1' : 0.90-self.legendCompress*0.052*nentries+self.legendTranslateY, 'x2' : 0.90+self.legendTranslateX, 'y2' : 0.90+self.legendTranslateY }

        # modify for different canvas size
        if doratio :
            legend_limits['y1'] = legend_limits['y1']*0.90
            #legend_limits['y2'] = legend_limits['y2']*1.05

        # grab stored legend limits
        if self.legendLimits :
            legend_limits = self.legendLimits

        leg = ROOT.TLegend(legend_limits['x1'], legend_limits['y1'],
                           legend_limits['x2'], legend_limits['y2'])
        leg.SetFillColor(ROOT.kWhite)
        leg.SetBorderSize(0)

        if self.legendLoc == 'Double' :
            leg.SetNColumns(2)
        

        return leg
    
    # ----------------------------------------------------------------------------
    def store_current_legend_placement(self) :
    
        self.legendLimits = {}
    
        leg = self.curr_legend
        self.legendLimits['x1'] = leg.GetX1NDC()
        self.legendLimits['y1'] = leg.GetY1NDC() 
        self.legendLimits['x2'] = leg.GetX2NDC()
        self.legendLimits['y2'] = leg.GetY2NDC()

        print self.legendLimits
