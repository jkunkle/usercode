import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math
import numpy
import os
import re

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('--inputFile', dest='inputFile', default=None, help='path to input file' )
parser.add_argument('--treeName', dest='treeName', default='hcalTupleTree/tree', help='tree name within root file (default = hcalTupleTree/tree' )
parser.add_argument('--filterRm', dest='filterRm', default=None, help='Only select these RMs (comma separated list)' )
parser.add_argument('--filterFib', dest='filterFib', default=None, help='Only select these Fibers (comma separated list)' )
parser.add_argument('--filterIEta', dest='filterIEta', default=None, help='Only select these IEtas (comma separated list)' )
parser.add_argument('--filterSide', dest='filterSide', default=None, help='Only select this side(comma separated list)' )
parser.add_argument('--filterIPhi', dest='filterIPhi', default=None, help='Only select these IPhis (comma separated list)' )
parser.add_argument('--filterDepth', dest='filterDepth', default=None, help='Only select these Depths (comma separated list)' )
parser.add_argument('--filterCh', dest='filterCh', default=None, help='Only select these Channels (comma separated list)' )
parser.add_argument('--printData', dest='printData', default=False, action='store_true', help='Print detailed data info' )
parser.add_argument('--outputDir', dest='outputDir', default=None, help='write pdfs to this directory and make a combined file' )
parser.add_argument('--compareRuns', dest='compareRuns', default=None, help='comma separated list of runs to compare' )

_COLORS = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kViolet, ROOT.kOrange]

options = parser.parse_args()

if options.outputDir is not None :

    ROOT.gROOT.SetBatch(True)

class RMHists :

    def __init__(self, rmId ) :
        hist_average = ROOT.TH2F( 'average_rm%d' %rmId, 'Signal Average',  8, 0, 8, 6, 0, 6 )
        hist_rms     = ROOT.TH2F( 'average_rm%d' %rmId, 'Signal Average',  8, 0, 8, 6, 0, 6 )

class Channel : 

    def __init__(self, rm=None, fib=None, ch=None, ieta=None, iphi=None, depth=None ) :

        if rm is not None and fib is not None and ch is not None :
            self.rm = rm
            self.fib = fib
            self.ch = ch
            self.mode = 0
        if ieta is not None and iphi is not None and depth is not None :
            self.ieta = ieta
            self.iphi = iphi
            self.depth = depth
            self.mode = 1

        self.average = None

        self.charge = []
        self.time   = []
        self.wtime   = []

    def GetAverage(self) :
        arr = numpy.array( self.charge )
        return numpy.mean( arr )

    def GetRMS( self ) :
        arr = numpy.array( self.charge )
        return numpy.std( arr )

    def GetNEvt( self ) :
        return len( self.charge )

    def __eq__( self, other ) :

        if self.mode != other.mode :
            print 'Cannot compare channels configured with different coordinates'
            return False

        if self.mode == 0 :
            if (self.rm == other.rm) and (self.fib == other.fib ) and (self.ch == other.ch ) :
                return True
            else :
                return False

        if self.mode == 1 :
            if (self.ieta == other.ieta) and (self.iphi == other.iphi ) and (self.depth == other.depth ) :
                return True
            else :
                return False

    def __str__(self) :

        return 'rm = %d, fib = %d, ch = %d' %( self.rm, self.fib, self.ch )

class ChannelsData :

    def __init__(self) :

        self.channels = {}
        self.run = 0

    def add_qie8_data( self, ieta, iphi, depth, in_data, in_wtime ) :

        this_channel = ( ieta, iphi, depth )
        if this_channel not in self.channels :
            self.channels[this_channel] = Channel( ieta=ieta, iphi=iphi, depth=depth )

        self.channels[this_channel].charge.append(in_data )
        self.channels[this_channel].wtime.append(in_wtime)

    def add_data( self, rm, fib, ch, in_data, in_wtime, in_tdc ) :

        this_channel = ( rm, fib, ch )
        if this_channel not in self.channels :
            self.channels[this_channel] = Channel( rm=rm, fib=fib, ch=ch )

        self.channels[this_channel].charge.append(in_data )
        self.channels[this_channel].time.append(in_tdc)

    def get_channels( self, channel_id = None ) :

        if channel_id is not None :
            found_channel = self.channels.get( channel_id , None )
            if found_channel is None :
                print 'Could not find channel'
            else :
                return { channel_id : found_channel }
        else :
            return self.channels


def main() :

    RMFiltList = []
    FibFiltList = []
    ChFiltList = []

    IEtaFiltList = []
    IPhiFiltList = []
    DepthFiltList = []

    compare_runs_list = []
    if options.compareRuns is not None :
        compare_runs_list = options.compareRuns.split(',')

    compare_two_runs = False
    make_trends      = False
    if len(compare_runs_list) == 1 :
        compare_two_runs = True
    elif len(compare_runs_list) > 1 :
        make_trends = True


    if options.filterRm is not None :
        RMFiltList = [int(x) for x in options.filterRm.split(',')]
    if options.filterFib is not None :
        FibFiltList = [int(x) for x in options.filterFib.split(',')]
    if options.filterCh is not None :
        ChFiltList = [int(x) for x in options.filterCh.split(',')]

    if options.filterIEta is not None :
        if options.filterSide == 'minus' :
            IEtaFiltList = [-1*int(x) for x in options.filterIEta.split(',')]
        else :
            IEtaFiltList = [int(x) for x in options.filterIEta.split(',')]
    if options.filterIPhi is not None :
        IPhiFiltList = [int(x) for x in options.filterIPhi.split(',')]
    if options.filterDepth is not None :
        DepthFiltList = [int(x) for x in options.filterDepth.split(',')]

    print IEtaFiltList

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

    EvtMax = -1

    if make_trends :
        EvtMax = 2000


    channels_data = LoadQIE8Data( options.inputFile, options.treeName, IEtaFiltList, IPhiFiltList, DepthFiltList, EvtMax )

    compare_data = []

    if options.compareRuns is not None :
        for runfile in compare_runs_list :
            compare_data.append ( (runfile,LoadQIE8Data( runfile, options.treeName, IEtaFiltList, IPhiFiltList, DepthFiltList, EvtMax )) )

    if compare_two_runs :
        MakeIEtaIPhiCompareHists( channels_data, compare_data )
    elif make_trends :
        MakeTrendHists( channels_data, compare_data )
    else :
        FillEtaPhiHists( channels_data )

    #channels_data = LoadQIE11Data( options.inputFile, options.treeName, RMFiltList, FibFiltList, ChFiltList, EvtMax )

    #compare_data = []

    #if options.compareRuns is not None :
    #    for runfile in compare_runs_list :
    #        compare_data.append ( (runfile,LoadQIE11Data( runfile, options.treeName, RMFiltList, FibFiltList, ChFiltList, EvtMax )) )

    #if compare_two_runs :
    #    MakeCompareHists( channels_data, compare_data )
    #elif make_trends :
    #    MakeTrendHists( channels_data, compare_data )
    #else :
    #    FillRMHists( channels_data )


def LoadQIE8Data( fname, tname, IEtaFiltList, IPhiFiltList, DepthFiltList, EvtMax=-1 ) :

    ofile = ROOT.TFile.Open( fname, 'READ' )

    tree = ofile.Get( tname )

    channels_data = ChannelsData()

    res = re.match( 'outputFile_(\d+)\.root', os.path.basename( fname ) )
    if res is not None :
        channels_data.run = int( res.group(1) )
    

    for eidx, event in enumerate(tree) :

        #if eidx >= 100  :
        #    break

        if EvtMax > 0 and eidx > EvtMax : 
            break

        if eidx%100 == 0 :
            print 'Analyze Event %d' %eidx

        for idx, DigiIEta in enumerate(tree.HBHEDigiIEta) :

            DigiIPhi  = tree.HBHEDigiIPhi[idx]
            DigiDepth = tree.HBHEDigiDepth[idx]

            if IEtaFiltList and not ( DigiIEta in IEtaFiltList ) :
                continue
            if IPhiFiltList and not ( DigiIPhi in IPhiFiltList ) :
                continue
            if DepthFiltList and not ( DigiDepth in DepthFiltList ) :
                continue

            fc_vals =  tree.HBHEDigiFC[idx]

            if options.printData :
                print 'channel : ieta %d, iphi %d, depth %d' %( DigiIEta, DigiIPhi, DigiDepth )

            sum_fc = 0
            sum_ts_fc = 0
            for idx, fc in enumerate(fc_vals) :
                # skip TS0
                if idx == 0 :
                    continue
                sum_fc +=  fc
                sum_ts_fc += (idx+1)*fc

                if options.printData :
                    print 'TS %s charge = %d' %( idx, fc )

            channels_data.add_qie8_data( DigiIEta, DigiIPhi, DigiDepth, sum_fc, sum_ts_fc/float(sum_fc) )

    ofile.Close()

    return channels_data

def LoadQIE11Data( fname, tname, RMFiltList, FibFiltList, ChFiltList, EvtMax=-1 ) :

    ofile = ROOT.TFile.Open( fname, 'READ' )

    tree = ofile.Get( tname ) 
    channels_data = ChannelsData()

    res = re.match( 'outputFile_(\d+)\.root', os.path.basename( fname ) )
    if res is not None :
        channels_data.run = int( res.group(1) )
    

    for eidx, event in enumerate(tree) :

        #if eidx >= 100  :
        #    break

        if EvtMax > 0 and eidx > EvtMax : 
            break

        if eidx%1000 == 0 :
            print 'Analyze Event %d' %eidx

        for idx, DigiRM in enumerate(tree.QIE11DigiRM) :

            DigiFib = tree.QIE11DigiRMFib[idx]
            DigiCh = tree.QIE11DigiFibCh[idx]

            if RMFiltList and not ( DigiRM in RMFiltList ) :
                continue
            if FibFiltList and not ( DigiFib in FibFiltList ) :
                continue
            if ChFiltList and not ( DigiCh in ChFiltList ) :
                continue

            fc_vals =  tree.QIE11DigiFC[idx]
            tdc_vals =  tree.QIE11DigiTDC[idx]

            if options.printData :
                print 'channel : rm %d, fib %d, ch %d' %( DigiRM, DigiFib, DigiCh )

            sum_fc = 0
            sum_ts_fc = 0
            for idx, fc in enumerate(fc_vals) :
                # skip TS0
                if idx == 0 :
                    continue
                sum_fc +=  fc
                sum_ts_fc += (idx+1)*fc

                if options.printData :
                    print 'TS %s charge = %d' %( idx, fc )

            tdc_time = 0
            found_le = False
            for idx, tdc in enumerate(tdc_vals) :
                # skip TS0
                if idx == 0 :
                    continue
                if not found_le :
                    if( tdc <= 50 ) :
                        found_le = True
                        tdc_time += tdc
                    else :
                        tdc_time += 50

                if options.printData :
                    print 'TS %s TDC =  %d, TDC Time = %d' %( idx, tdc, tdc_time )

            channels_data.add_data( DigiIEta, DigiIPhi, DigiDepth, sum_fc, sum_ts_fc/float(sum_fc), 0. )

    ofile.Close()

    return channels_data

def MakeTrendHists( data_orig, data_comps ) :

    hists = {}

    n_points = len( data_comps ) + 1

    rm_list = []
    fib_list = []
    ch_list = []
    for ch in data_orig.get_channels().values() :

        ch_id = (ch.rm, ch.fib, ch.ch)

        rm_list.append( ch.rm )
        fib_list.append( ch.fib )
        ch_list.append( ch.ch )

        hists[ch_id] = ROOT.TGraphErrors( n_points ) 
        hists[ch_id].SetName( 'trend_%d_%d_%d' %ch_id )
        hists[ch_id].SetTitle( 'pedestal trends for RM %d, FIB %d' %(ch.rm, ch.fib) )

        hists[ch_id].SetPoint( 0, 1, ch.GetAverage() )
        hists[ch_id].SetPointError( 0, 0.0, ch.GetAverage()/math.sqrt( ch.GetNEvt()) )


        for idx, (name, cdata) in enumerate(data_comps) :
            avg = cdata.get_channels()[ch_id].GetAverage()
            nevt = cdata.get_channels()[ch_id].GetNEvt()
            hists[ch_id].SetPoint( idx+1, idx+2,avg  )
            hists[ch_id].SetPointError( idx+1, 0.0, avg/math.sqrt( nevt ))


    rm_list  = list( set( rm_list  ) ) 
    fib_list = list( set( fib_list ) ) 
    ch_list  = list( set( ch_list  ) ) 

    output_pdfs = []
    can_ch = {}
    legs = {}

    for rm in rm_list :

        can_id = rm,
        can_ch[ can_id ] = ROOT.TCanvas( 'trend_%d' %can_id, 'can', 700, 750 )
        can_ch[ can_id ].Divide( 2, 4 )

        for fib in fib_list :

            can_ch[ can_id ].cd( fib )
            legs[(can_id,fib)]  = ROOT.TLegend( 0.6, 0.6, 0.9, 0.9 )

            for idx, ch in enumerate(ch_list) :

                hists[( rm, fib, ch)].SetMarkerColor(_COLORS[idx])
                hists[( rm, fib, ch)].SetMarkerStyle(20)
                hists[( rm, fib, ch)].SetLineColor(_COLORS[idx])

                if idx == 0 :
                    hists[( rm, fib, ch)].Draw('APL')
                    hists[( rm, fib, ch)].GetYaxis().SetTitle( 'Average FC' ) 
                    #hists[( rm, fib, ch)].GetXaxis().SetBinLabel( 1, str( data_orig.run ) )
                    hists[( rm, fib, ch)].GetXaxis().SetTitle( 'Run Number' )
                    hists[( rm, fib, ch)].SetMinimum( 100 )
                    hists[( rm, fib, ch)].SetMaximum( 500 )
                    #for idx, (name, cdata) in enumerate(data_comps) :
                    #    hists[( rm, fib, ch)].GetXaxis().SetBinLabel( idx+2, str( cdata.run ) )
                else :
                    hists[( rm, fib, ch)].Draw('PLsame')

                legs[(can_id,fib)].AddEntry( hists[(rm, fib, ch)],'Channel %d' %ch,  'LP' )

            legs[(can_id,fib)].Draw()


        if options.outputDir is not None :
            name ='%s/%s.pdf' %( options.outputDir, can_ch[can_id].GetName() )
            can_ch[can_id].SaveAs( name )
            output_pdfs.append( name) 
        else :
            raw_input('cont')

    if output_pdfs :

        run_str = ''
        res = re.match( 'outputFile_(\d+).root', os.path.basename(options.inputFile) )
        if res is not None :
            run_str = res.group(1)

        pdf_str = ' '.join( output_pdfs )

        merged_name = '%s/trends%s.pdf' %( options.outputDir, run_str)

        print 'Create merged pdf, %s' %merged_name
    
        os.system( 'gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=%s %s' %(merged_name , pdf_str ) )


def MakeIEtaIPhiCompareHists( data_orig, data_comps ) :

    hists = {}
    for depth in range( 1, 4 ) :
        hists[depth] = {}
        hists[depth]['average'] = ROOT.TH2F( 'average%d'%depth, 'Signal Average, RM %d' %depth, 82, -41, 41, 72, 0, 72   )
        hists[depth]['rms']     = ROOT.TH2F( 'rms%d'%depth    , 'Signal rms, RM %d'%depth, 82, -41, 41, 72, 0, 72       )
        hists[depth]['average'].SetStats(0)
        hists[depth]['rms']    .SetStats(0)

        hists[depth]['ratio'] = ROOT.TH1F( 'ratio%d' %depth, 'channel ratios', 1000, -2, 2 )

    print data_orig.get_channels()
    for ch_id, ch_orig in data_orig.get_channels().iteritems() :

        avg_orig = ch_orig.GetAverage()
        rms_orig = ch_orig.GetRMS()

        if ch_id not in data_comps[0][1].get_channels() :
            continue

        avg_comp = data_comps[0][1].get_channels()[ch_id].GetAverage()
        rms_comp = data_comps[0][1].get_channels()[ch_id].GetRMS()

        print 'ieta = %i, iphi = %i , depth = %i, Avg_before = %f, Avg_after = %f, ratio = %f' %( ch_orig.ieta, ch_orig.iphi, ch_orig.depth, avg_orig, avg_comp, avg_orig/avg_comp )

        ieta_bin = hists[ch_orig.depth]['average'].GetXaxis().FindBin( ch_orig.ieta )
        iphi_bin = hists[ch_orig.depth]['average'].GetYaxis().FindBin( ch_orig.iphi )

        hists[ch_orig.depth]['average'].SetBinContent( ieta_bin, iphi_bin, avg_orig-avg_comp) 
        hists[ch_orig.depth]['rms']    .SetBinContent( ieta_bin, iphi_bin, rms_orig-rms_comp)

        hists[ch_orig.depth]['ratio'].Fill( avg_orig/avg_comp )

    output_pdfs = []

    can_avg = ROOT.TCanvas('avg', 'avg' )
    can_avg.Divide( 2, 2)
    can_rms = ROOT.TCanvas('rms', 'rms' )
    can_rms.Divide( 2, 2)
    can_ratio = ROOT.TCanvas('ratio', 'ratio' )
    can_ratio.Divide( 2, 2)

    can_avg.cd(1)
    hists[1]['average'].Draw('colz')
    can_avg.cd(2)
    hists[2]['average'].Draw('colz')
    can_avg.cd(3)
    hists[3]['average'].Draw('colz')
    can_rms.cd(1)
    hists[1]['rms'].Draw('colz')
    can_rms.cd(2)
    hists[2]['rms'].Draw('colz')
    can_rms.cd(3)
    hists[3]['rms'].Draw('colz')

    can_ratio.cd(1)
    hists[1]['ratio'].Draw()
    can_ratio.cd(2)
    hists[2]['ratio'].Draw()
    can_ratio.cd(3)
    hists[3]['ratio'].Draw()

    if options.outputDir is not None :
        name_avg ='%s/average.pdf' %( options.outputDir)
        name_rms ='%s/rms.pdf' %( options.outputDir)
        can_avg.SaveAs( name_avg )
        can_rms.SaveAs( name_rms )
        output_pdfs.append( name_avg ) 
        output_pdfs.append( name_rms) 
    else :
        raw_input('cont')

    if output_pdfs :

        run_str = ''
        res = re.match( 'outputFile_(\d+).root', os.path.basename(options.inputFile) )
        if res is not None :
            run_str = res.group(1)

        pdf_str = ' '.join( output_pdfs )

        merged_name = '%s/compare%s.pdf' %( options.outputDir, run_str)

        print 'Create merged pdf, %s' %merged_name
    
        os.system( 'gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=%s %s' %(merged_name , pdf_str ) )

def MakeCompareHists( data_orig, data_comps ) :

    hists = {}
    for rm in range( 1, 5 ) :
        hists[rm] = {}
        hists[rm]['average'] = ROOT.TH2F( 'average%d'%rm, 'Signal Average, RM %d' %rm,  8, 0, 8, 6, 0, 6  )
        hists[rm]['rms']     = ROOT.TH2F( 'rms%d'%rm    , 'Signal rms, RM %d'%rm    ,  8, 0, 8, 6, 0, 6  )
        hists[rm]['average'].SetStats(0)
        hists[rm]['rms']    .SetStats(0)

    for ch_id, ch_orig in data_orig.get_channels().iteritems() :

        avg_orig = ch_orig.GetAverage()
        rms_orig = ch_orig.GetRMS()

        avg_comp = data_comps[0][1].get_channels()[ch_id].GetAverage()
        rms_comp = data_comps[0][1].get_channels()[ch_id].GetRMS()

        print 'Avg_orig = %f, Avg_comp = %f' %( avg_orig, avg_comp )

        hists[ch_orig.rm]['average'].SetBinContent( ch_orig.fib, ch_orig.ch+1, avg_orig-avg_comp) 
        hists[ch_orig.rm]['rms']    .SetBinContent( ch_orig.fib, ch_orig.ch+1, rms_orig-rms_comp)

    output_pdfs = []

    can_avg = ROOT.TCanvas('avg', 'avg' )
    can_avg.Divide( 2, 2)
    can_rms = ROOT.TCanvas('rms', 'rms' )
    can_rms.Divide( 2, 2)

    can_avg.cd(1)
    hists[1]['average'].Draw('colz')
    #can_avg.GetPad(1).SetLogz()
    can_avg.cd(2)
    hists[2]['average'].Draw('colz')
    #can_avg.GetPad(2).SetLogz()
    can_avg.cd(3)
    hists[3]['average'].Draw('colz')
    #can_avg.GetPad(3).SetLogz()
    can_avg.cd(4)
    hists[4]['average'].Draw('colz')
    #can_avg.GetPad(4).SetLogz()
    can_rms.cd(1)
    hists[1]['rms'].Draw('colz')
    #can_rms.GetPad(1).SetLogz()
    can_rms.cd(2)
    hists[2]['rms'].Draw('colz')
    #can_rms.GetPad(2).SetLogz()
    can_rms.cd(3)
    hists[3]['rms'].Draw('colz')
    #can_rms.GetPad(3).SetLogz()
    can_rms.cd(4)
    hists[4]['rms'].Draw('colz')
    #can_rms.GetPad(4).SetLogz()
    if options.outputDir is not None :
        name_avg ='%s/average.pdf' %( options.outputDir)
        name_rms ='%s/rms.pdf' %( options.outputDir)
        can_avg.SaveAs( name_avg )
        can_rms.SaveAs( name_rms )
        output_pdfs.append( name_avg ) 
        output_pdfs.append( name_rms) 
    else :
        raw_input('cont')

    if output_pdfs :

        run_str = ''
        res = re.match( 'outputFile_(\d+).root', os.path.basename(options.inputFile) )
        if res is not None :
            run_str = res.group(1)

        pdf_str = ' '.join( output_pdfs )

        merged_name = '%s/compare%s.pdf' %( options.outputDir, run_str)

        print 'Create merged pdf, %s' %merged_name
    
        os.system( 'gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=%s %s' %(merged_name , pdf_str ) )

def FillEtaPhiHists( data ) :

    hists = {}
    for depth in range( 1, 4 ) :

        hists[depth] = {}
        hists[depth]['average'] = ROOT.TH2F( 'average%d'%rm, 'Signal Average, RM %d' %rm, 82, -41, 41, 72, 0, 72  )
        hists[depth]['rms']     = ROOT.TH2F( 'rms%d'%rm    , 'Signal rms, RM %d'%rm, 82, -41, 41, 72, 0, 72   )
        hists[depth]['average'].SetStats(0)
        hists[depth]['rms']    .SetStats(0)

    for ch in data.get_channels().values() :

        avg = ch.GetAverage()
        ieta_bin = hists[ch.depth]['average'].FindBinX( ch.ieta )
        iphi_bin = hists[ch.depth]['average'].FindBinY( ch.iphi )
        hists[ch.depth]['average'].SetBinContent( ieta_bin, iphi_bin, avg) 
        hists[ch.depth]['rms']    .SetBinContent( ieta_bin, iphi_bin, ch.GetRMS()/avg )

    hists_ch = {}
    hists_tdc = {}
    hists_wtime = {}

    rm_list = []
    fib_list = []
    ch_list = []
    for ch in data.get_channels().values() :

        rm_list.append( ch.rm )
        fib_list.append( ch.fib )
        ch_list.append( ch.ch )

        max_ch = max( ch.charge )
        min_ch = min( ch.charge )
        range_ch = max_ch - min_ch

        max_time = max( ch.time )
        min_time = min( ch.time )
        range_time = max_time - min_time

        max_wtime = max( ch.wtime )
        min_wtime = min( ch.wtime )
        range_wtime = max_wtime - min_wtime

        ch_id = (ch.rm, ch.fib, ch.ch)

        data_len = len( ch.charge )

        nbins = data_len/500
        if nbins < 50 :
            nbins = 50

        hists_ch[ch_id] = ROOT.TH1F( 'charge_%d_%d_%d' %ch_id , 'FC spectrum RM %d, FIB %d, CH %d' %ch_id,  nbins , min_ch-range_ch*0.1, max_ch+range_ch*0.1  ) 
        for d in ch.charge :
            hists_ch[ch_id].Fill( d )

        hists_tdc[ch_id] = ROOT.TH1F( 'time_%d_%d_%d' %ch_id , 'time spectrum RM %d, FIB %d, CH %d' %ch_id,  nbins , min_time-range_time*0.1, max_time+range_time*0.1  ) 
        for d in ch.time :
            hists_tdc[ch_id].Fill( d )

        hists_wtime[ch_id] = ROOT.TH1F( 'wtime_%d_%d_%d' %ch_id , 'time spectrum RM %d, FIB %d, CH %d' %ch_id,  nbins, min_wtime-range_wtime*0.1, max_wtime+range_wtime*0.1  ) 
        for d in ch.wtime :
            hists_wtime[ch_id].Fill( d )


    rm_list  = list( set( rm_list  ) ) 
    fib_list = list( set( fib_list ) ) 
    ch_list  = list( set( ch_list  ) ) 

    can_ch = {}
    can_tdc = {}
    can_wtime = {}

    output_pdfs = []

    can_avg = ROOT.TCanvas('avg', 'avg' )
    can_avg.Divide( 2, 2)
    can_rms = ROOT.TCanvas('rms', 'rms' )
    can_rms.Divide( 2, 2)

    can_avg.cd(1)
    hists[1]['average'].Draw('colz')
    #can_avg.GetPad(1).SetLogz()
    can_avg.cd(2)
    hists[2]['average'].Draw('colz')
    #can_avg.GetPad(2).SetLogz()
    can_avg.cd(3)
    hists[3]['average'].Draw('colz')
    #can_avg.GetPad(3).SetLogz()
    can_avg.cd(4)
    hists[4]['average'].Draw('colz')
    #can_avg.GetPad(4).SetLogz()
    can_rms.cd(1)
    hists[1]['rms'].Draw('colz')
    #can_rms.GetPad(1).SetLogz()
    can_rms.cd(2)
    hists[2]['rms'].Draw('colz')
    #can_rms.GetPad(2).SetLogz()
    can_rms.cd(3)
    hists[3]['rms'].Draw('colz')
    #can_rms.GetPad(3).SetLogz()
    can_rms.cd(4)
    hists[4]['rms'].Draw('colz')
    #can_rms.GetPad(4).SetLogz()
    if options.outputDir is not None :
        name_avg ='%s/average.pdf' %( options.outputDir)
        name_rms ='%s/rms.pdf' %( options.outputDir)
        can_avg.SaveAs( name_avg )
        can_rms.SaveAs( name_rms )
        output_pdfs.append( name_avg ) 
        output_pdfs.append( name_rms) 
    else :
        raw_input('cont')
    for rm in rm_list :
        for fib in fib_list :

            can_id = (rm, fib)
            can_ch[ can_id ] = ROOT.TCanvas( 'charge_%d_%d' %can_id, 'can', 700, 750 )
            can_ch[ can_id ].Divide( 2, 3 )

            can_tdc[ (rm, fib) ] = ROOT.TCanvas( 'tdc_%d_%d' %can_id, 'can', 700, 750 )
            can_tdc[ (rm, fib) ].Divide( 2, 3 )

            can_wtime[ (rm, fib) ] = ROOT.TCanvas( 'wtime_%d_%d' %can_id, 'can', 700, 750 )
            can_wtime[ (rm, fib) ].Divide( 2, 3 )

            for ch in ch_list :

                can_ch[ can_id ].cd( ch+1 )
                hists_ch[( rm, fib, ch)].Draw()
                can_ch[ can_id ].GetPad( ch+1 ).SetLogy()

                can_tdc[ can_id ].cd( ch+1 )
                hists_tdc[( rm, fib, ch)].Draw()
                can_tdc[ can_id ].GetPad( ch+1 ).SetLogy()

                can_wtime[ can_id ].cd( ch+1 )
                hists_wtime[( rm, fib, ch)].Draw()
                can_wtime[ can_id ].GetPad( ch+1 ).SetLogy()


            if options.outputDir is not None :
                name ='%s/%s.pdf' %( options.outputDir, can_ch[can_id].GetName() )
                can_ch[can_id].SaveAs( name )
                output_pdfs.append( name) 
                name ='%s/%s.pdf' %( options.outputDir, can_wtime[can_id].GetName() )
                can_wtime[can_id].SaveAs( name )
                output_pdfs.append( name) 
                name ='%s/%s.pdf' %( options.outputDir, can_tdc[can_id].GetName() )
                can_tdc[can_id].SaveAs( name )
                output_pdfs.append( name) 
            else :
                raw_input('cont')


    if output_pdfs :

        run_str = ''
        res = re.match( 'outputFile_(\d+).root', os.path.basename(options.inputFile) )
        if res is not None :
            run_str = res.group(1)

        pdf_str = ' '.join( output_pdfs )

        merged_name = '%s/merged%s.pdf' %( options.outputDir, run_str)

        print 'Create merged pdf, %s' %merged_name
    
        os.system( 'gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=%s %s' %(merged_name , pdf_str ) )





def FillRMHists( data ) :

    hists = {}
    for rm in range( 1, 5 ) :
        hists[rm] = {}
        hists[rm]['average'] = ROOT.TH2F( 'average%d'%rm, 'Signal Average, RM %d' %rm,  8, 0, 8, 6, 0, 6  )
        hists[rm]['rms']     = ROOT.TH2F( 'rms%d'%rm    , 'Signal rms, RM %d'%rm    ,  8, 0, 8, 6, 0, 6  )
        hists[rm]['average'].SetStats(0)
        hists[rm]['rms']    .SetStats(0)

    for ch in data.get_channels().values() :

        avg = ch.GetAverage()
        hists[ch.rm]['average'].SetBinContent( ch.fib, ch.ch+1, avg) 
        hists[ch.rm]['rms']    .SetBinContent( ch.fib, ch.ch+1, ch.GetRMS()/avg )

    hists_ch = {}
    hists_tdc = {}
    hists_wtime = {}

    rm_list = []
    fib_list = []
    ch_list = []
    for ch in data.get_channels().values() :

        rm_list.append( ch.rm )
        fib_list.append( ch.fib )
        ch_list.append( ch.ch )

        max_ch = max( ch.charge )
        min_ch = min( ch.charge )
        range_ch = max_ch - min_ch

        max_time = max( ch.time )
        min_time = min( ch.time )
        range_time = max_time - min_time

        max_wtime = max( ch.wtime )
        min_wtime = min( ch.wtime )
        range_wtime = max_wtime - min_wtime

        ch_id = (ch.rm, ch.fib, ch.ch)

        data_len = len( ch.charge )

        nbins = data_len/500
        if nbins < 50 :
            nbins = 50

        hists_ch[ch_id] = ROOT.TH1F( 'charge_%d_%d_%d' %ch_id , 'FC spectrum RM %d, FIB %d, CH %d' %ch_id,  nbins , min_ch-range_ch*0.1, max_ch+range_ch*0.1  ) 
        for d in ch.charge :
            hists_ch[ch_id].Fill( d )

        hists_tdc[ch_id] = ROOT.TH1F( 'time_%d_%d_%d' %ch_id , 'time spectrum RM %d, FIB %d, CH %d' %ch_id,  nbins , min_time-range_time*0.1, max_time+range_time*0.1  ) 
        for d in ch.time :
            hists_tdc[ch_id].Fill( d )

        hists_wtime[ch_id] = ROOT.TH1F( 'wtime_%d_%d_%d' %ch_id , 'time spectrum RM %d, FIB %d, CH %d' %ch_id,  nbins, min_wtime-range_wtime*0.1, max_wtime+range_wtime*0.1  ) 
        for d in ch.wtime :
            hists_wtime[ch_id].Fill( d )


    rm_list  = list( set( rm_list  ) ) 
    fib_list = list( set( fib_list ) ) 
    ch_list  = list( set( ch_list  ) ) 

    can_ch = {}
    can_tdc = {}
    can_wtime = {}

    output_pdfs = []

    can_avg = ROOT.TCanvas('avg', 'avg' )
    can_avg.Divide( 2, 2)
    can_rms = ROOT.TCanvas('rms', 'rms' )
    can_rms.Divide( 2, 2)

    can_avg.cd(1)
    hists[1]['average'].Draw('colz')
    #can_avg.GetPad(1).SetLogz()
    can_avg.cd(2)
    hists[2]['average'].Draw('colz')
    #can_avg.GetPad(2).SetLogz()
    can_avg.cd(3)
    hists[3]['average'].Draw('colz')
    #can_avg.GetPad(3).SetLogz()
    can_avg.cd(4)
    hists[4]['average'].Draw('colz')
    #can_avg.GetPad(4).SetLogz()
    can_rms.cd(1)
    hists[1]['rms'].Draw('colz')
    #can_rms.GetPad(1).SetLogz()
    can_rms.cd(2)
    hists[2]['rms'].Draw('colz')
    #can_rms.GetPad(2).SetLogz()
    can_rms.cd(3)
    hists[3]['rms'].Draw('colz')
    #can_rms.GetPad(3).SetLogz()
    can_rms.cd(4)
    hists[4]['rms'].Draw('colz')
    #can_rms.GetPad(4).SetLogz()
    if options.outputDir is not None :
        name_avg ='%s/average.pdf' %( options.outputDir)
        name_rms ='%s/rms.pdf' %( options.outputDir)
        can_avg.SaveAs( name_avg )
        can_rms.SaveAs( name_rms )
        output_pdfs.append( name_avg ) 
        output_pdfs.append( name_rms) 
    else :
        raw_input('cont')
    for rm in rm_list :
        for fib in fib_list :

            can_id = (rm, fib)
            can_ch[ can_id ] = ROOT.TCanvas( 'charge_%d_%d' %can_id, 'can', 700, 750 )
            can_ch[ can_id ].Divide( 2, 3 )

            can_tdc[ (rm, fib) ] = ROOT.TCanvas( 'tdc_%d_%d' %can_id, 'can', 700, 750 )
            can_tdc[ (rm, fib) ].Divide( 2, 3 )

            can_wtime[ (rm, fib) ] = ROOT.TCanvas( 'wtime_%d_%d' %can_id, 'can', 700, 750 )
            can_wtime[ (rm, fib) ].Divide( 2, 3 )

            for ch in ch_list :

                can_ch[ can_id ].cd( ch+1 )
                hists_ch[( rm, fib, ch)].Draw()
                can_ch[ can_id ].GetPad( ch+1 ).SetLogy()

                can_tdc[ can_id ].cd( ch+1 )
                hists_tdc[( rm, fib, ch)].Draw()
                can_tdc[ can_id ].GetPad( ch+1 ).SetLogy()

                can_wtime[ can_id ].cd( ch+1 )
                hists_wtime[( rm, fib, ch)].Draw()
                can_wtime[ can_id ].GetPad( ch+1 ).SetLogy()


            if options.outputDir is not None :
                name ='%s/%s.pdf' %( options.outputDir, can_ch[can_id].GetName() )
                can_ch[can_id].SaveAs( name )
                output_pdfs.append( name) 
                name ='%s/%s.pdf' %( options.outputDir, can_wtime[can_id].GetName() )
                can_wtime[can_id].SaveAs( name )
                output_pdfs.append( name) 
                name ='%s/%s.pdf' %( options.outputDir, can_tdc[can_id].GetName() )
                can_tdc[can_id].SaveAs( name )
                output_pdfs.append( name) 
            else :
                raw_input('cont')


    if output_pdfs :

        run_str = ''
        res = re.match( 'outputFile_(\d+).root', os.path.basename(options.inputFile) )
        if res is not None :
            run_str = res.group(1)

        pdf_str = ' '.join( output_pdfs )

        merged_name = '%s/merged%s.pdf' %( options.outputDir, run_str)

        print 'Create merged pdf, %s' %merged_name
    
        os.system( 'gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=%s %s' %(merged_name , pdf_str ) )





main()
