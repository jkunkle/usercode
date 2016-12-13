import os
import ROOT

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--dir', dest='dir', default=None, required=True, help='Path to directory containing ntuples' )
parser.add_argument( '--fileKey', dest='fileKey', default='ntuple', required=False, help='key to match files' )
parser.add_argument( '--treeName', dest='treeName', default='tupel/EventTree', required=False, help='name of tree in files' )
parser.add_argument( '--weightBranch', dest='weightBranch', default='EvtWeights', required=False, help='name of branch containing event weights' )

options = parser.parse_args()

ROOT.gROOT.SetBatch(True)

def main () :

    ntuple_files = []

    for fname in os.listdir( options.dir ) :
        if fname.count( options.fileKey ) :
            ntuple_files.append( '%s/%s' %( options.dir, fname ) )

    n_raw = []
    n_total = []
    n_weighted = []


    #for i in range( 1, 118 ) :

    #    print 'ntuple_%d.root' %i

    mychain = ROOT.TChain( options.treeName )
    for f in ntuple_files :
        mychain.AddFile( f )
    #mychain.AddFile( '/data/users/jkunkle/Baobabs/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/ntuple_%d.root' %i)

    #mychain.SetBranchStatus('*', 0 )
    #mychain.SetBranchStatus( options.weightBranch, 1 )

    totalEvents = 0
    weightedEvents = 0

    weighthist = ROOT.TH1F( 'weighthist', 'weighthist', 2, -100000, 100000 )

    print mychain.GetEntries()
    n_raw.append(  mychain.GetEntries() )

    mychain.Draw( 'EvtRunNum >> weighthist' )

    print weighthist.Integral()
    print weighthist.GetBinContent(0)
    print weighthist.GetBinContent(1)
    print weighthist.GetBinContent(2)
    print weighthist.GetBinContent(3)
    print weighthist.GetBinContent(4)

    neg_events  = weighthist.GetBinContent(0) + weighthist.GetBinContent(1)
    pos_events  = weighthist.GetBinContent(2) + weighthist.GetBinContent(3)

    total_events = neg_events + pos_events
    weighted_events = pos_events - neg_events 

    n_total .append( total_events )
    n_weighted.append( weighted_events)

    print 'Total Events = %d, Weighted events = %d' %( total_events, weighted_events)


    print 'Raw Events = %d, Total Events = %d, Weighted events = %d' %(sum(n_raw), sum(n_total), sum(n_weighted) ) 

    #for event in mychain :

    #    weight = getattr( mychain, options.weightBranch )

    #    totalEvents += 1

    #    if weight[0] > 0 :
    #        weightedEvents += 1
    #    if weight[0] < 0 :
    #        weightedEvents -= 1

    #print 'Total Events = %d, Weighted events = %d' %( totalEvents, weightedEvents )



main()
